from pathlib import Path
import re
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('a')
    parser.add_argument('b')

    args = parser.parse_args()

    compare_configs(args.a, args.b)

def compare_configs(config_path_a: Path, config_path_b: Path):
    entries_a = parse_kernel_config(config_path_a)
    entries_b = parse_kernel_config(config_path_b)

    for name in entries_a:
        if name not in entries_b:
            continue

        if entries_a[name] != entries_b[name]:
            print(f"{name}: {entries_a[name]}, {entries_b[name]}")

def parse_kernel_config(config_path: Path):
    with open(config_path, 'r') as fd:
        config_str = fd.read()

    config_lines = config_str.splitlines()

    entry_regexp = re.compile(r'^(\w+)=([a-zA-Z0-9_\-]+|"[a-zA-Z0-9_ ()\.\-=/,]*")$')

    entries = {}
    for line in config_lines:
        if line == "" or line.startswith("#"):
            continue

        match = entry_regexp.match(line)
        if not match:
            raise Exception(f"invalid line:\n{line}")

        name, value = match.group(1, 2)
        entries[name] = value

    return entries

if __name__ == "__main__":
    main()