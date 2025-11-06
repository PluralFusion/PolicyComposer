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

# --- Output Directories ---
base_output_dir = 'output'
dirs_to_create = [
    os.path.join(base_output_dir, 'md'),
    os.path.join(base_output_dir, 'pdf'),
    os.path.join(base_output_dir, 'odt'),
    os.path.join(base_output_dir, 'temp_combined')
]
[os.makedirs(d, exist_ok=True) for d in dirs_to_create]

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
    FILE_HISTORY = history_data.get('file_history', {})    
    IS_GLOBAL_RELEASE = history_data.get('is_global_release', False)
except Exception as e:
    print(f"Could not load history file: {e}")
    CURRENT_BUILD_COMMIT = None
    IS_GLOBAL_RELEASE = False
    FILE_HISTORY = {}

# --- 3. Setup Jinja2 ---
env = Environment(loader=FileSystemLoader(policy_dir))
processed_for_combined_pdf = []

# --- Helper Function to Generate History Table ---
def get_history_table(policy_filename):
    # 1. Get the list of commits that *only* touched this file
    commits = FILE_HISTORY.get(policy_filename, [])
    
    if not CURRENT_BUILD_COMMIT:
        return "" # Can't build history if build commit info is missing

    # 2. Handle Global Release based on the configured style
    if IS_GLOBAL_RELEASE:
        print(f"  -> Global release detected. Stamping with commit {CURRENT_BUILD_COMMIT['hash'][:7]}")
        
        # Add the global commit to the history for every file.
        if not any(commit['hash'] == CURRENT_BUILD_COMMIT['hash'] for commit in commits):
            commits.insert(0, CURRENT_BUILD_COMMIT)
        
        # Check the style: 'replace' or 'append'
        history_style = config.get('global_release_history_style', 'append')
        if history_style == 'replace':
            print("     -> History style is 'replace'. Showing only the global release commit.")
            # Filter to *only* the global release commit
            commits = [c for c in commits if c['hash'] == CURRENT_BUILD_COMMIT['hash']]
            # Early exit, no need to check for other hotfixes
            return build_markdown_table(commits)

    # 3. Filter the final list to include only valid release commits.
    # A commit is included if:
    #   a) It is the current global release commit (if applicable).
    #   b) Its subject starts with the release/hotfix prefix.
    prefix = config.get('release_commit_prefix', 'RELEASE:')
    commits = [c for c in commits if c['subject'].startswith(prefix) or (IS_GLOBAL_RELEASE and c['hash'] == CURRENT_BUILD_COMMIT['hash'])]
    
    if not commits:
        return ""

    # 4. Build the markdown table
    return build_markdown_table(commits)

def build_markdown_table(commits):
    """Helper function to build the markdown table from a list of commits."""
    table = "\n\n## Version History\n\n"
    table += "| Date | Updated By | Commit | Comments |\n"
    table += "| :--- | :--- | :--- | :--- |\n"
    
    for commit in commits:
        hash_short = commit['hash'][:7]
        table += f"| {commit['date']} | {commit['author_name']} | {hash_short} | {commit['subject']} |\n"
        
    return table

# --- 4. Process Each Policy File ---
print(f"Processing {len(POLICY_FILES_LIST)} policy files from {order_file}...")

# --- Get PDF Font settings from config ---
pdf_font = config.get('pdf_main_font', 'Noto Sans')
pdf_header_font = config.get('pdf_header_font', pdf_font) # Default to main font if not set
pdf_code_font = config.get('pdf_code_font', 'Noto Sans Mono') # Good default
odt_reference_doc = config.get('pdf_odt_reference_doc') # Path to a reference ODT file

# Define common pandoc PDF options to reduce duplication
common_pdf_options = [
    '--pdf-engine=xelatex',
    '--variable', f"mainfont='{pdf_font}'",
    '--variable', f"sansfont='{pdf_header_font}'",
    '--variable', f"monofont='{pdf_code_font}'"
]


for policy_item in POLICY_FILES_LIST:
    try:
        policy_filename = policy_item['source']
        output_filename_template = policy_item['output']
        # Get the new 'title' field, default to the output filename
        policy_title_template = policy_item.get('title', output_filename_template.replace('.md', ''))
    except (TypeError, KeyError):
        print(f"  -> WARNING: Skipping malformed item in {order_file}. Must be a list of objects with 'source' and 'output' keys.")
        print(f"     Item: {policy_item}")
        continue
        
    # Render the *output* filename
    filename_template = Template(output_filename_template)
    rendered_filename = filename_template.render(config)
    
    # Render the *PDF title*
    title_template = Template(policy_title_template)
    rendered_title = title_template.render(config)

    print(f"Processing: {policy_filename}  ->  Output: {rendered_filename}  (Title: {rendered_title})")

    try:
        # 1. Render Jinja2 template (use the *source* filename)
        template = env.get_template(policy_filename)
        rendered_content = template.render(config)
        
        # 2. Generate history table (use *source* filename to look up)
        history_table = get_history_table(policy_filename)
        
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
        md_path = os.path.join(dirs_to_create[0], rendered_filename)
        with open(md_path, 'w') as out_f:
            out_f.write(md_content)

        # --- Create Individual PDF ---
        pdf_filename = rendered_filename.replace('.md', '.pdf')
        pdf_path = os.path.join(dirs_to_create[1], pdf_filename)
        
        print(f"  -> Converting to individual PDF: {pdf_path}")
        
        pandoc_cmd_individual = [
            'pandoc',
            '--from=gfm', # Use GitHub Flavored Markdown (fixes bullets)
            '-o', pdf_path,
            '--metadata', f"title={rendered_title}", # Use friendly title
        ] + common_pdf_options
        
        try:
            subprocess.run(
                pandoc_cmd_individual,
                input=pdf_content,
                check=True, capture_output=True, text=True
            )
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Pandoc failed to create individual PDF for {policy_filename}.")
            print(f"Pandoc stderr:\n{e.stderr}")
            exit(1)
        
        # 7. Create Individual ODT
        odt_filename = rendered_filename.replace('.md', '.odt')
        odt_path = os.path.join(dirs_to_create[2], odt_filename)
        
        print(f"  -> Converting to individual ODT: {odt_path}")
        
        pandoc_cmd_odt = [
            'pandoc',
            '--from=gfm',
            '-o', odt_path,
            '--metadata', f"title={rendered_title}"
        ]
        
        # Add reference doc for styling if it's defined in the config
        if odt_reference_doc and os.path.exists(odt_reference_doc):
            pandoc_cmd_odt.extend(['--reference-doc', odt_reference_doc])

        try:
            subprocess.run(pandoc_cmd_odt, input=pdf_content, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Pandoc failed to create individual ODT for {policy_filename}.")
            print(f"Pandoc stderr:\n{e.stderr}")
            exit(1)

        
        # 7. Save file for Combined PDF
        temp_combined_path = os.path.join(dirs_to_create[3], rendered_filename)
        with open(temp_combined_path, 'w') as out_f:
            out_f.write(combined_content)
        processed_for_combined_pdf.append(temp_combined_path)

    except Exception as e:
        # This will catch the 'template not found' error if the source file is wrong
        print(f"ERROR processing {policy_filename}: {e}")
        exit(1)

# --- 8. Create Final Combined PDF ---
combined_pdf_path = os.path.join(dirs_to_create[1], 'combined_policies.pdf')
print(f"Creating combined PDF: {combined_pdf_path}")

combined_pdf_title = config.get('combined_pdf_title', 'Company Policy Manual')
combined_pdf_author = config.get('combined_pdf_author', config.get('company_name', 'Company'))

try:
    pandoc_cmd_combined = [
        'pandoc',
        '--from=gfm', # Use GitHub Flavored Markdown (fixes bullets)
        '-o', combined_pdf_path,
        '--table-of-contents',
        '--toc-depth=2',
        '--number-sections',
        '--metadata', f"title={combined_pdf_title}",
        '--metadata', f"author={combined_pdf_author}",
    ] + common_pdf_options + processed_for_combined_pdf
    
    try:
        subprocess.run(pandoc_cmd_combined, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("ERROR: Pandoc failed to create the combined PDF.")
        print(f"Pandoc stderr:\n{e.stderr}")
        exit(1)
    
except Exception as e:
    print(f"An unexpected error occurred during the combined PDF creation: {e}")
    exit(1)

print("Policy build process completed successfully.")
