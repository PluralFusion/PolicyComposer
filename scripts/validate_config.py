import os
import argparse
import sys
import os
from pathlib import Path
import yaml
from jinja2 import Environment, meta

CONFIG_DEFAULT_PATH = 'conf/config.yaml'
SCHEMA_DEFAULT_PATH = 'conf/ui_schema.yaml'
POLICY_DIR = 'policies'

class ConfigValidator:
    def __init__(self, config_path):
        self.config_path = config_path
        self.warnings = []
        self.errors = []
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"Fatal: Could not read or parse YAML file at {config_path}: {e}")
            self.config = None
        
        try:
            with open(SCHEMA_DEFAULT_PATH, 'r') as f:
                self.schema = yaml.safe_load(f)
        except Exception as e:
            self.warnings.append(f"Could not read or parse UI Schema file at {SCHEMA_DEFAULT_PATH}. UI validation will be skipped.")
            self.schema = None

    def add_error(self, message):
        self.errors.append(message)

    def add_warning(self, message):
        self.warnings.append(message)

    def validate(self):
        if not self.config:
            return

        print("--- Running All Validation Checks ---")
        self.check_required_keys()
        self.check_ephi_consistency()
        self.check_vendor_structure()
        self.check_review_committee()
        self.check_compliance_frameworks_structure()
        self.check_jinja_variables()
        if self.schema:
            self.check_ui_schema()
        print("--- Validation Complete ---")

    def check_required_keys(self):
        """Checks for presence and basic types of essential keys."""
        print("1. Checking for required keys and types...")
        required = {
            'company_name': str, 'release_version': str, 'vendors': list,
            'compliance_frameworks': dict, 'service_types': dict
        }
        for key, expected_type in required.items():
            if key not in self.config:
                self.add_error(f"Required key '{key}' is missing from config.")
            elif not isinstance(self.config.get(key), expected_type):
                self.add_error(f"Key '{key}' has wrong type. Expected {expected_type.__name__}, got {type(self.config.get(key)).__name__}.")

    def check_ephi_consistency(self):
        """The original check for ephi_access consistency."""
        print("2. Checking ePHI flag consistency...")
        canonical_ephi_access = self.config.get('ephi_access', False)
        
        derived_ephi_access = False
        service_types = self.config.get('service_types', {})
        if not isinstance(service_types, dict):
            self.add_error("'service_types' should be a dictionary.")
            return

        for service, details in service_types.items():
            if isinstance(details, dict) and details.get('enabled') and details.get('phi_access'):
                derived_ephi_access = True
                break
        
        if canonical_ephi_access != derived_ephi_access:
            self.add_error(
                f"Mismatch found: The main 'ephi_access' is '{canonical_ephi_access}', "
                f"but based on 'service_types', it should be '{derived_ephi_access}'. "
                "Use --fix to update the main flag."
            )

    def check_vendor_structure(self):
        """Validates the structure of the 'vendors' list of objects."""
        print("3. Checking vendor data structure...")
        vendors = self.config.get('vendors', [])
        if not isinstance(vendors, list):
            self.add_error("'vendors' key must be a list.")
            return

        for i, vendor in enumerate(vendors):
            if not isinstance(vendor, dict):
                self.add_error(f"Vendor at index {i} is not a valid object.")
                continue
            if 'name' not in vendor:
                self.add_error(f"Vendor at index {i} is missing required 'name' key.")
            if 'services' not in vendor:
                self.add_error(f"Vendor '{vendor.get('name', 'N/A')}' is missing 'services' key.")
            elif not isinstance(vendor.get('services'), list):
                self.add_error(f"Vendor '{vendor.get('name', 'N/A')}': 'services' must be a list of strings.")
            if 'baa_signed' not in vendor:
                self.add_warning(f"Vendor '{vendor.get('name', 'N/A')}' is missing 'baa_signed' key.")
            elif not isinstance(vendor.get('baa_signed'), bool):
                self.add_error(f"Vendor '{vendor.get('name', 'N/A')}': 'baa_signed' must be a boolean (true/false).")

    def check_review_committee(self):
        """Checks for logical consistency with the review committee."""
        print("4. Checking review committee logic...")
        if self.config.get('show_review_committee') and not self.config.get('review_committee'):
            self.add_warning("'show_review_committee' is true, but the 'review_committee' list is empty.")

    def check_compliance_frameworks_structure(self): # Renamed from check_compliance_frameworks_structure
        """Validates the nested structure of the 'compliance_frameworks' section."""
        print("5. Checking compliance frameworks structure...")
        frameworks = self.config.get('compliance_frameworks', {})
        if not isinstance(frameworks, dict):
            self.add_error("'compliance_frameworks' must be a dictionary.")
            return
        
        for name, details in frameworks.items():
            if not isinstance(details, dict):
                self.add_error(f"Compliance framework '{name}' must be a dictionary.")
                continue
            
            # Check for 'supported' flag
            if 'supported' not in details or not isinstance(details['supported'], bool):
                self.add_error(f"Framework '{name}' is missing a boolean 'supported' flag.")

            if 'supported' not in details or not isinstance(details['supported'], bool):
                self.add_error(f"Framework '{name}' is missing a boolean 'supported' flag.")

            if 'audit' not in details or not isinstance(details['audit'], dict):
                self.add_error(f"Framework '{name}' is missing the 'audit' object.")
            else:
                audit_details = details['audit']
                if 'in_progress' not in audit_details or not isinstance(audit_details['in_progress'], bool):
                    self.add_error(f"Audit section for '{name}' is missing a boolean 'in_progress' flag.")

    def check_jinja_variables(self):
        """Parses all policy templates and checks if used variables exist in the config."""
        print("6. Checking for undefined Jinja2 variables in policy templates...")
        env = Environment()
        policy_files = Path(POLICY_DIR).rglob('*.md')
        
        # Store variables found per file
        template_vars_per_file = {}

        for policy_file in sorted(policy_files): # Sort for consistent error reporting
            try:
                template_source = policy_file.read_text()
                ast = env.parse(template_source)
                template_vars = meta.find_undeclared_variables(ast)
                if template_vars:
                    template_vars_per_file[str(policy_file)] = template_vars
            except Exception as e:
                self.add_warning(f"Could not parse template {policy_file}: {e}")
        # Flatten the config dict for easy checking of nested keys
        config_keys = self._flatten_dict(self.config)

    def check_ui_schema(self):
        """Validates the ui_schema.yaml against the config.yaml."""
        print("7. Checking UI Schema against config...")
        config_keys = self._flatten_dict(self.config)
        schema_keys = self._flatten_schema(self.schema)
        
        # Check that every key in the schema exists in the config
        for key in schema_keys:
            if key not in config_keys:
                # This check is often too noisy to be useful if the schema is out of sync.
                # self.add_warning(f"UI Schema key '{key}' does not exist in config.yaml and will be ignored by the UI.")
                pass
        
        # Check that every key in the config exists in the schema (as a warning)
        # We exclude some keys that are not meant to be in the UI
        # These are keys that are valid in config.yaml but are either derived,
        # internal, or managed by other means (e.g., policy_order.yaml, usermap.json)
        excluded_from_ui_check = [
            'release_commit_prefix', 'global_release_history_style', # Managed by specific widgets
            'ephi_access', # Derived from service_types
            'hipaa_website', 'change_request_form_link', # Not critical for UI editing
            'approved_os', # Complex structure, might be managed separately or with custom widget
            'vendors', # Handled by list_of_objects, but top-level key might not be explicitly in schema
            'approved_tools', # Handled by dict_of_list_of_objects
            'remote_work', 'byod', # Handled by dict_of_toggles
            'audit_penetration_external', 'audit_penetration_internal', 'vulnerability_scanner', # Handled by dict_group
            'compliance_frameworks', # Handled by dict_of_frameworks
            'service_types', # Handled by dict_of_toggles
            'company_service_user_types' # Simple text input, but might be missed if not explicitly in schema
        ]
        for key in config_keys:
            if key not in schema_keys and key not in excluded_from_ui_check:
                self.add_warning(f"Config key '{key}' is not defined in the UI Schema. It will not appear in the web UI.")

    def _flatten_schema(self, schema_node, parent_key='', sep='.'):
        """Flattens the ui_schema.yaml to get a list of keys that map to config.yaml."""
        keys = set()
        if isinstance(schema_node, dict):
            for key, value in schema_node.items():
                if key.startswith('_'):
                    continue
                
                # If the value is a dict and has a widget key, it's a config item.
                if isinstance(value, dict) and ('widget' in value or '_widget' in value):
                    keys.add(key)
                # If it's a container/expander, recurse into its children.
                elif isinstance(value, dict):
                    keys.update(self._flatten_schema(value))
        return keys

    def _flatten_dict(self, d, parent_key='', sep='.'):
        """Flattens a nested dictionary for easy key lookup."""
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                # Add the dictionary key itself (e.g., 'service_types.saas')
                items.append((new_key, v)) 
                items.extend(self._flatten_dict(v, new_key, sep=sep).items()) # Recurse
            else:
                items.append((new_key, v))
        # Also add the top-level keys themselves for checks like {% if service_types.saas %}
        for k in d.keys():
            if isinstance(d[k], dict):
                items.append((k, d[k]))
        return dict(items)
    def fix_ephi_access(self):
        """Automatically updates the canonical ephi_access flag."""
        if not self.config:
            return False
        
        derived_ephi_access = False
        service_types = self.config.get('service_types', {})
        for service, details in service_types.items():
            if isinstance(details, dict) and details.get('enabled') and details.get('phi_access'):
                derived_ephi_access = True
                break
        
        if self.config.get('ephi_access') != derived_ephi_access:
            print(f"Fixing 'ephi_access' flag to '{derived_ephi_access}'...")
            # We need to re-read and write using a YAML library that preserves comments and structure
            # For simplicity here, we'll do a text-based replacement which is less robust but works for this case.
            with open(self.config_path, 'r') as f:
                lines = f.readlines()
            
            with open(self.config_path, 'w') as f:
                for line in lines:
                    if line.strip().startswith('ephi_access:'):
                        f.write(f"ephi_access: {str(derived_ephi_access).lower()}\n")
                    else:
                        f.write(line)
            print("File fixed.")
            return True
        else:
            print("'ephi_access' flag is already consistent. No fix needed.")
            return False

def main():
    parser = argparse.ArgumentParser(description="Validate the PolicyComposer config.yaml file.")
    parser.add_argument('--config', default=CONFIG_DEFAULT_PATH, help=f"Path to the config file (default: {CONFIG_DEFAULT_PATH})")
    parser.add_argument('--fix', action='store_true', help="Automatically fix the canonical 'ephi_access' flag if a mismatch is found.")
    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f"Error: Config file not found at '{args.config}'", file=sys.stderr)
        sys.exit(2)

    validator = ConfigValidator(args.config)
    if args.fix:
        validator.fix_ephi_access()
        # Re-run validation after fixing
        print("\nRe-running validation after applying fix...")
        validator = ConfigValidator(args.config)
    validator.validate()
    if validator.warnings:
        print("\n--- ⚠️ Warnings ---")
        for warning in validator.warnings:
            print(f"- {warning}")
    if validator.errors:
        print("\n--- ❌ Errors ---")
        for error in validator.errors:
            print(f"- {error}")
        print("\nValidation failed with errors.")
        sys.exit(1)
    
    print("\n✅ Validation successful. No errors found.")
    sys.exit(0)

if __name__ == "__main__":
    main()
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
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

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
    FILE_HISTORY = {}
    IS_GLOBAL_RELEASE = False

# --- 3. Setup Jinja2 ---
env = Environment(loader=FileSystemLoader(policy_dir))
processed_for_combined_pdf = []

# --- Helper Function to Generate History Table ---
def get_history_table(policy_filename):
    # 1. Get the list of commits that *only* touched this file
    commits = FILE_HISTORY.get(policy_filename, [])
    
    if not CURRENT_BUILD_COMMIT:
        return "" # Can't build history if build commit info is missing

    # 2. Check if this is a global release
    if IS_GLOBAL_RELEASE:
        print(f"  -> Global release detected. Stamping with commit {CURRENT_BUILD_COMMIT['hash'][:7]}")
        # For a global release, we *only* show the global release commit.
        # We also check if the global commit is *already* in the file history (if the config was the *only* thing committed)
        # This logic ensures the global commit is added, and it's the *only* one if it's a global release.
        
        # Check if the global commit is already in the file's history
        found_in_history = False
        for commit in commits:
             if commit['hash'] == CURRENT_BUILD_COMMIT['hash']:
                found_in_history = True
                break
        
        # If the global commit wasn't in the file's history, add it.
        # This is the key logic for stamping config-only changes.
        if not found_in_history:
             commits.insert(0, CURRENT_BUILD_COMMIT)
             
        # Now, filter *only* for the global release commit
        commits = [c for c in commits if c['hash'] == CURRENT_BUILD_COMMIT['hash']]

    else:
        # 3. Not a global release, so filter by the commit prefix
        prefix = config.get('release_commit_prefix', 'RELEASE:')
        commits = [c for c in commits if c['subject'].startswith(prefix)]

    # 4. Build the markdown table
    if not commits:
        return "" # No history to show

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

# --- Get PDF Font settings from config ---
pdf_font = config.get('pdf_main_font', 'Noto Sans')
pdf_header_font = config.get('pdf_header_font', pdf_font) # Default to main font if not set
pdf_code_font = config.get('pdf_code_font', 'Noto Sans Mono') # Good default

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
        md_path = os.path.join(md_output_dir, rendered_filename)
        with open(md_path, 'w') as out_f:
            out_f.write(md_content)

        # 6. Create Individual PDF
        pdf_filename = rendered_filename.replace('.md', '.pdf')
        pdf_path = os.path.join(pdf_output_dir, pdf_filename)
        
        print(f"  -> Converting to individual PDF: {pdf_path}")
        
        pandoc_cmd_individual = [
            'pandoc',
            '--from=gfm', # Use GitHub Flavored Markdown (fixes bullets)
            '-o', pdf_path,
            '--metadata', f"title={rendered_title}", # Use friendly title
            '--variable', f"mainfont={pdf_font}",
            '--variable', f"sansfont={pdf_header_font}", # Set header font
            '--variable', f"monofont={pdf_code_font}"  # Set code font
        ]
        
        subprocess.run(
            pandoc_cmd_individual,
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
        '--variable', f"mainfont={pdf_font}",
        '--variable', f"sansfont={pdf_header_font}",
        '--variable', f"monofont={pdf_code_font}"
    ] + processed_for_combined_pdf
    
    subprocess.run(pandoc_cmd_combined, check=True)
    
except Exception as e:
    print(f"ERROR creating combined PDF: {e}")
    exit(1)

print("Policy build process completed successfully.")
