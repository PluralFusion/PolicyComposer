import os
import yaml
from jinja2 import Environment, FileSystemLoader, Template  # <-- Import Template
import subprocess
import json

# --- 1. Setup ---
print("Starting policy build process...")
config_path = 'conf/config.yml'
policy_dir = 'policies'
order_file = 'conf/policy_order.txt'
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
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

print(f"Loading history from {history_file}")
try:
    with open(history_file, 'r') as f:
        git_history = json.load(f)
except Exception as e:
    print(f"Could not load history file: {e}")
    git_history = {}

# --- 3. Setup Jinja2 ---
env = Environment(loader=FileSystemLoader(policy_dir))
processed_for_combined_pdf = []

# --- Helper Function to Generate History Table ---
def get_history_table(policy_filename):
    # History is retrieved using the *source* filename
    commits = git_history.get(policy_filename)
    if not commits:
        return ""
    
    table = "\n\n## Version History\n\n"
    table += "| Date | Updated By | Commit | Comments |\n"
    table += "| :--- | :--- | :--- | :--- |\n"
    
    for commit in commits:
        hash_short = commit['hash'][:7]
        table += f"| {commit['date']} | {commit['author_name']} | {hash_short} | {commit['subject']} |\n"
        
    return table

# --- 4. Process Each Policy File ---
print(f"Reading policy order from {order_file}")
with open(order_file, 'r') as f:
    for policy_filename in f:
        policy_filename = policy_filename.strip()
        if not policy_filename:
            continue
            
        # --- NEW: RENDER THE FILENAME ITSELF ---
        filename_template = Template(policy_filename)
        rendered_filename = filename_template.render(config)
        print(f"Processing: {policy_filename}  ->  Output: {rendered_filename}")
        # --- END NEW SECTION ---

        try:
            # 1. Render Jinja2 template (use original filename to load)
            template = env.get_template(policy_filename)
            rendered_content = template.render(config)
            
            # 2. Generate history table (use original filename to look up)
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

            # --- 5. Save Processed Markdown (use rendered_filename) ---
            md_path = os.path.join(md_output_dir, rendered_filename)
            with open(md_path, 'w') as out_f:
                out_f.write(md_content)

            # --- 6. Create Individual PDF (use rendered_filename) ---
            pdf_filename = rendered_filename.replace('.md', '.pdf') # Use rendered name
            pdf_path = os.path.join(pdf_output_dir, pdf_filename)
            
            print(f"  -> Converting to individual PDF: {pdf_path}")
            subprocess.run(
                ['pandoc', '-o', pdf_path, '--metadata', f"title={rendered_filename.replace('.md', '')}"],
                input=pdf_content.encode('utf-8'),
                check=True
            )
            
            # --- 7. Save file for Combined PDF (use rendered_filename) ---
            temp_combined_path = os.path.join(temp_combined_dir, rendered_filename)
            with open(temp_combined_path, 'w') as out_f:
                out_f.write(combined_content)
            processed_for_combined_pdf.append(temp_combined_path)

        except Exception as e:
            print(f"ERROR processing {policy_filename}: {e}")
            exit(1)

# --- 8. Create Final Combined PDF ---
combined_pdf_path = os.path.join(pdf_output_dir, 'combined_policies.pdf')
print(f"Creating combined PDF: {combined_pdf_path}")

combined_pdf_title = config.get('combined_pdf_title', 'Company Policy Manual')
combined_pdf_author = config.get('combined_pdf_author', config.get('company_name', 'Company'))

try:
    pandoc_cmd = [
        'pandoc',
        '-o', combined_pdf_path,
        '--table-of-contents',
        '--toc-depth=2',
        '--number-sections',
        '--metadata', f"title={combined_pdf_title}",
        '--metadata', f"author={combined_pdf_author}"
    ] + processed_for_combined_pdf
    
    subprocess.run(pandoc_cmd, check=True)
    
except Exception as e:
    print(f"ERROR creating combined PDF: {e}")
    exit(1)

print("Policy build process completed successfully.")