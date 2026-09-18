"""Patch .dist-info/METADATA files based on dependency override specifications.

Called from %pyproject_install to apply runtime dependency overrides
to installed wheel metadata, so that pythondistdeps.py generates
correct Requires.
"""

import argparse
import sys


def print_err(*args, **kwargs):
    kwargs.setdefault('file', sys.stderr)
    print(*args, **kwargs)


try:
    from packaging.requirements import Requirement
    from packaging.specifiers import SpecifierSet
    from packaging.utils import canonicalize_name
except ImportError as e:
    print_err('Import error:', e)
    sys.exit(1)

# uses packaging, needs to be imported after packaging is verified to be present
from pyproject_dependency_overrides import (
    parse_override_string, apply_overrides_to_specifiers,
)


def parse_overrides(override_lines):
    """Parse override lines, skipping br_only entries."""
    overrides = {}
    for line in override_lines:
        parts = line.split(':')
        if parts and parts[-1].strip() == 'br_only':
            continue

        package, action, value = parse_override_string(line)
        overrides.setdefault(package, []).append(
            {'action': action, 'value': value})

    return overrides


def apply_overrides_to_requirement(req, overrides_for_pkg):
    """Apply overrides to a single Requirement object. Returns None if ignored."""
    for override in overrides_for_pkg:
        if override['action'] == 'ignore':
            return None

    specifiers = apply_overrides_to_specifiers(
        list(req.specifier), overrides_for_pkg)

    if specifiers:
        req.specifier = SpecifierSet(','.join(str(s) for s in specifiers))
    else:
        req.specifier = SpecifierSet()

    return req


def patch_metadata(metadata_path, overrides):
    """Read METADATA, apply overrides to Requires-Dist lines, and rewrite."""
    if not overrides:
        return

    with open(metadata_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    patched = False
    for line in lines:
        if line.startswith('Requires-Dist:'):
            req_str = line[len('Requires-Dist:'):].strip()
            try:
                req = Requirement(req_str)
            except Exception:
                new_lines.append(line)
                continue

            name = canonicalize_name(req.name)
            if name in overrides:
                result = apply_overrides_to_requirement(req, overrides[name])
                if result is None:
                    print_err(f'Removing dependency {name} from METADATA per override')
                    patched = True
                    continue
                new_line = f'Requires-Dist: {result}\n'
                if new_line != line:
                    print_err(f'Patching dependency {name} in METADATA: {req_str.strip()} -> {result}')
                    patched = True
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if patched:
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print_err(f'Patched {metadata_path}')


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Patch .dist-info/METADATA based on dependency overrides')
    parser.add_argument(
        '--overrides', required=True,
        help='Path to the dependency overrides file')
    parser.add_argument(
        '--metadata', required=True,
        help='Path to the .dist-info/METADATA file')

    args = parser.parse_args(argv)

    try:
        with open(args.overrides, 'r', encoding='utf-8') as f:
            override_lines = f.read().split()
    except FileNotFoundError:
        return

    try:
        overrides = parse_overrides(override_lines)
    except ValueError as e:
        print_err(f'ERROR: {e}')
        sys.exit(1)

    if overrides:
        patch_metadata(args.metadata, overrides)


if __name__ == '__main__':
    main()
