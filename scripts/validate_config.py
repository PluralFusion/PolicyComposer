#!/usr/bin/env python3
"""
Validate `conf/config.yaml` for canonical PHI flag consistency.

Checks:
 - Looks for `ephi_access` canonical flag
 - Computes derived PHI presence from known per-service flags
 - Reports mismatches and optionally fixes the config when --fix is provided

Usage:
  python3 scripts/validate_config.py [--config conf/config.yaml] [--fix]

Exit codes:
 0 - OK (no mismatch)
 1 - Mismatch detected (or validation error)
 2 - Fatal error (file I/O / parse error)
"""
import argparse
import sys
import yaml
from pathlib import Path

KNOWN_PHI_FLAGS = [
    'saas_phi_access',
    'paas_phi_access',
    'medical_device_phi_access',
    'mobile_app_phi_access',
]


def load_config(path):
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error reading config file '{path}': {e}", file=sys.stderr)
        sys.exit(2)


def write_config(path, data):
    try:
        with open(path, 'w') as f:
            yaml.safe_dump(data, f, sort_keys=False)
    except Exception as e:
        print(f"Error writing config file '{path}': {e}", file=sys.stderr)
        sys.exit(2)


def main():
    p = argparse.ArgumentParser(description='Validate config PHI flags')
    p.add_argument('--config', '-c', default='conf/config.yaml', help='Path to config.yaml')
    p.add_argument('--fix', action='store_true', help='If provided, update config.yaml to set ephi_access to derived value')
    args = p.parse_args()

    config_path = Path(args.config)
    config = load_config(config_path)

    # Find any keys that mention 'phi' (case-insensitive)
    phi_like_keys = [k for k in config.keys() if 'phi' in k.lower()]

    print(f"Found PHI-like keys in config: {phi_like_keys}")

    # Compute derived value from known flags
    derived = False
    found_known = {}
    for k in KNOWN_PHI_FLAGS:
        val = bool(config.get(k, False))
        found_known[k] = val
        if val:
            derived = True

    print('Per-service PHI flags:')
    for k, v in found_known.items():
        print(f'  {k}: {v}')

    print(f'Computed derived ephi_access = {derived}')

    # Check canonical flag
    canonical_exists = 'ephi_access' in config
    canonical_val = bool(config.get('ephi_access', False))
    if canonical_exists:
        print(f"Canonical 'ephi_access' found: {canonical_val}")
    else:
        print("Canonical 'ephi_access' not found in config.")

    if canonical_exists and canonical_val == derived:
        print('OK: canonical flag matches derived value.')
        sys.exit(0)

    # Mismatch or missing
    print('\nWARNING: Canonical ephi_access does not match derived per-service flags (or is missing).')
    if canonical_exists:
        print(f"  ephi_access={canonical_val} but derived={derived}")
    else:
        print(f"  ephi_access missing; derived={derived}")

    print('\nRecommended action:')
    print(f"  - Set 'ephi_access' to {derived} in {config_path}")
    print('  - Or adjust per-service PHI flags to reflect reality')

    if args.fix:
        print('\n--fix provided; updating config file...')
        config['ephi_access'] = derived
        write_config(config_path, config)
        print('Config updated.')
        # fall through with exit code 0 if fix applied
        sys.exit(0)

    # non-fixed mismatch
    sys.exit(1)


if __name__ == '__main__':
    main()
