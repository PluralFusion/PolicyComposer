# Configuration Validation

This small validator checks `conf/config.yaml` for consistency of the canonical `ephi_access` flag and per-service PHI flags.

Why
- Keeps templates simple: most templates should check `ephi_access`.
- Detects mismatches where per-service flags indicate PHI handling but the canonical flag doesn't, and vice-versa.

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
- 1: Mismatch detected (no automatic fix applied)
- 2: Fatal error reading/writing the config file

Notes
- The script looks for known per-service PHI flags: `saas_phi_access`, `paas_phi_access`, `medical_device_phi_access`, `mobile_app_phi_access`.
- It also lists any config keys containing `phi` (case-insensitive) to help you find other related flags.
