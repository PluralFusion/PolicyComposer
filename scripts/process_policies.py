import os
import yaml
from jinja2 import Environment, FileSystemLoader, Template
import subprocess
import json

# --- 1. Setup ---
print("Starting policy build process...")
config_path = 'conf/config.yaml'
policy_dir = 'policies'
order_file = 'conf/policy_order.yaml' 
history_file = 'build/git_history.json'

# Output directories
md_output_dir = 'md'
pdf_output_dir = 'pdf'
temp_combined_dir = 'temp_combined'

os.makedirs(md_output_dir, exist_ok=True)
os.makedirs(pdf_output_dir, exist_ok=True)
os.makedirs(temp_combined_dir, exist_ok=True)

# --- 2. Load Config & History ---
print(f"Loading config from {config_path}")
try:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
except yaml.YAMLError as e:
    print(f"ERROR: Failed to parse {config_path}. Please check for syntax errors.")
    print(f"Parser error: {e}")
    exit(1)

# Load the policy order config
print(f"Loading policy order from {order_file}")
try:
    with open(order_file, 'r') as f:
        policy_order_config = yaml.safe_load(f)
    POLICY_FILES_LIST = policy_order_config.get('policy_files', [])
except Exception as e:
    print(f"ERROR: Could not load or parse {order_file}: {e}")
    exit(1)

print(f"Loading history from {history_file}")
try:
    with open(history_file, 'r') as f:
        history_data = json.load(f)
    CURRENT_BUILD_COMMIT = history_data.get('current_build_commit')
    IS_GLOBAL_RELEASE = history_data.get('is_global_release', False)
    FILE_HISTORY = history_data.get('file_history', {})
except Exception as e:
    print(f"Could not load history file: {e}")
    CURRENT_BUILD_COMMIT = None
    IS_GLOBAL_RELEASE = False
    FILE_HISTORY = {}

# --- 3. Setup Jinja2 ---
env = Environment(loader=FileSystemLoader(policy_dir))
processed_for_combined_pdf = []

# --- Helper Function to Generate History Table ---
def get_history_table(policy_filename, config):
    # Get the prefix for hotfixes
    release_prefix = config.get('release_commit_prefix', 'RELEASE:')
    
    # 1. Get the list of commits that *only* touched this file
    all_commits = FILE_HISTORY.get(policy_filename, [])
    
    # 2. Filter for hotfixes: commits that *match* the prefix
    commits = [c for c in all_commits if c['subject'].startswith(release_prefix)]
    
    if not CURRENT_BUILD_COMMIT:
        return "" # Can't build history if build commit info is missing

    # 3. If this is a global release, add the current commit to the top
    #    (regardless of its prefix)
    if IS_GLOBAL_RELEASE:
        print(f"  -> Adding global release commit {CURRENT_BUILD_COMMIT['hash'][:7]} to history")
        # Add to top, but check if it's already in the hotfix list to avoid duplicates
        if not any(c['hash'] == CURRENT_BUILD_COMMIT['hash'] for c in commits):
            commits.insert(0, CURRENT_BUILD_COMMIT)
    
    # If no release commits are found, don't build a table
    if not commits:
        return ""

    # 4. Build the markdown table
    table = "\n\n## Version History\n\n"
    table += "| Date | Updated By | Commit | Comments |\n"
    table += "| :--- | :--- | :--- | :--- |\n"
    
    for commit in commits:
        hash_short = commit['hash'][:7]
        # We'd need the repo URL from config to make this a link
        table += f"| {commit['date']} | {commit['author_name']} | {hash_short} | {commit['subject']} |\n"
        
    return table

# --- 4. Process Each Policy File ---
print(f"Processing {len(POLICY_FILES_LIST)} policy files from {order_file}...")
for policy_item in POLICY_FILES_LIST:
    try:
        policy_filename = policy_item['source']
        output_filename_template = policy_item['output']
    except (TypeError, KeyError):
        print(f"  -> WARNING: Skipping malformed item in {order_file}. Must be a list of objects with 'source' and 'output' keys.")
        print(f"     Item: {policy_item}")
        continue
        
    # Render the *output* filename
    filename_template = Template(output_filename_template)
    rendered_filename = filename_template.render(config)
    print(f"Processing: {policy_filename}  ->  Output: {rendered_filename}")

    try:
        # 1. Render Jinja2 template (use the *source* filename)
        template = env.get_template(policy_filename)
        rendered_content = template.render(config)
        
        # 2. Generate history table (use *source* filename to look up)
        history_table = get_history_table(policy_filename, config)
        
        # 3. Apply history based on config toggles
        md_content = rendered_content
        if config.get('md_show_revision_history', False):
            md_content += history_table
        
        pdf_content = rendered_content
        if config.get('pdf_show_revision_history', False):
            pdf_content += history_table
            
        combined_content = rendered_content
        if config.get('combined_pdf_show_revision_history', False):
            combined_content += history_table

        # 5. Save Processed Markdown
        md_path = os.path.join(md_output_dir, rendered_filename)
        with open(md_path, 'w') as out_f:
            out_f.write(md_content)

        # 6. Create Individual PDF
        pdf_filename = rendered_filename.replace('.md', '.pdf')
        pdf_path = os.path.join(pdf_output_dir, pdf_filename)
        
        print(f"  -> Converting to individual PDF: {pdf_path}")
        
        # Get PDF font from config, default to "Noto Sans"
        pdf_font = config.get('pdf_main_font', 'Noto Sans')
        
        pandoc_pdf_cmd = [
            'pandoc', '-o', pdf_path,
            '--metadata', f"title={rendered_filename.replace('.md', '')}",
            '--variable', f"mainfont={pdf_font}"
        ]
        
        subprocess.run(
            pandoc_pdf_cmd,
            input=pdf_content.encode('utf-8'),
            check=True
        )
        
        # 7. Save file for Combined PDF
        temp_combined_path = os.path.join(temp_combined_dir, rendered_filename)
        with open(temp_combined_path, 'w') as out_f:
            out_f.write(combined_content)
        processed_for_combined_pdf.append(temp_combined_path)

    except Exception as e:
        # This will catch the 'template not found' error if the source file is wrong
        print(f"ERROR processing {policy_filename}: {e}")
        exit(1)

# --- 8. Create Final Combined PDF ---
combined_pdf_path = os.path.join(pdf_output_dir, 'combined_policies.pdf')
print(f"Creating combined PDF: {combined_pdf_path}")

combined_pdf_title = config.get('combined_pdf_title', 'Company Policy Manual')
combined_pdf_author = config.get('combined_pdf_author', config.get('company_name', 'Company'))
pdf_font = config.get('pdf_main_font', 'Noto Sans')

try:
    pandoc_cmd = [
        'pandoc',
        '-o', combined_pdf_path,
        '--table-of-contents',
        '--toc-depth=2',
        '--number-sections',
        '--metadata', f"title={combined_pdf_title}",
        '--metadata', f"author={combined_pdf_author}",
        '--variable', f"mainfont={pdf_font}"
    ] + processed_for_combined_pdf
    
    subprocess.run(pandoc_cmd, check=True)
    
except Exception as e:
    print(f"ERROR creating combined PDF: {e}")
    exit(1)

print("Policy build process completed successfully.")
