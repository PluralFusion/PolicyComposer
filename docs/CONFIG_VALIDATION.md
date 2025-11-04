# Configuration Validation

This is a validator script that checks your `conf/config.yaml` and `conf/ui_schema.yaml` for correctness, consistency, and completeness. It is your first line of defense against configuration errors and helps prevent failed builds.

Why
- **Prevents Build Failures:** Catches typos in variable names used in your policy templates.
- **Ensures Correctness:** Verifies that your configuration has the right structure (e.g., the `vendors` list is formatted correctly).
- **Checks Logic:** Finds logical inconsistencies, like enabling a feature but leaving its configuration empty.
- **Keeps UI in Sync:** Ensures that the web interface schema matches the configuration file, preventing UI errors.

Files
- `scripts/validate_config.py` — CLI validator. You can run it locally.

Usage
```bash
# run validation (default config path)
python3 scripts/validate_config.py

# validate a specific config file
python3 scripts/validate_config.py --config conf/config.yaml

# automatically fix the canonical flag to match derived per-service flags
python3 scripts/validate_config.py --fix
```

Exit codes
- 0: OK (canonical flag matches derived value)
- 1: Errors detected
- 2: Fatal error reading/writing the config file

Checks Performed
### 1. Required Keys & Types
Ensures top-level keys like `company_name`, `vendors`, and `service_types` exist in `config.yaml` and have the correct data type (e.g., `vendors` is a list).

### 2. ePHI Flag Consistency
Ensures the main `ephi_access` flag is consistent with the detailed settings in `service_types`. This prevents logical contradictions in your policies.

### 3. Vendor Structure
Validates that each item in the `vendors` list is a complete object with `name`, `services` (as a list), and `baa_signed` (as a boolean). This is critical for templates that loop through vendors.

### 4. Review Committee Logic
Checks for logical inconsistencies, like `show_review_committee` being true while the `review_committee` list is empty.

### 5. Jinja2 Variable Validation
This is the most powerful check. The script reads all `.md` policy files, finds every Jinja2 variable used (e.g., `{{ company_website }}`), and verifies that each one is defined in your `config.yaml`. This is extremely effective at catching typos or missing configuration that would otherwise result in blank spots in your documents.

### 6. UI Schema Validation
This check ensures the web interface stays synchronized with your configuration.
- It verifies that every field defined in `ui_schema.yaml` corresponds to a real key in `config.yaml`.
- It warns you if you have keys in `config.yaml` that are *not* defined in the UI schema, which helps you remember to add new settings to the web UI.

By running this script before you commit, you can have high confidence that your configuration is valid and your document build will succeed.
