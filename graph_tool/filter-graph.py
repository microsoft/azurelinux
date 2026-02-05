#!/usr/bin/env python3
"""
Filter a DOT graph to only include nodes and edges for packages in a given list.
"""

import re
import sys


def load_packages(filename):
    """Load package names from a file (one per line, RPM format)."""
    packages = set()
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Extract package name from RPM format (name-version-release.arch)
            # Match everything up to the first '-' followed by a digit
            # Use a non-greedy match that stops at the first '-\d' pattern
            match = re.match(r'^(.*?)-\d', line)
            if match:
                packages.add(match.group(1))
            else:
                # If no version pattern, take the whole line as package name
                packages.add(line)
    return packages


def filter_graph(input_file, output_file, packages):
    """Filter DOT graph to only include specified packages."""
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        
        for line in fin:
            stripped = line.strip()
            
            # Write graph header only
            if stripped.startswith('digraph'):
                fout.write(line)
                continue
            
            # Check for node definition (single line: "name" [color="..."];)
            node_match = re.match(r'^"([^"]+)"\s+\[.*\];$', stripped)
            if node_match:
                node_name = node_match.group(1)
                if node_name in packages:
                    # Write node without style attributes
                    fout.write(f'"{node_name}";\n\n')
                continue
            
            # Check for edge definition
            edge_match = re.match(r'^"([^"]+)"\s+->\s+\{', stripped)
            if edge_match:
                source_node = edge_match.group(1)
                if source_node in packages:
                    # Collect all target nodes (skip the first line with "->")
                    edge_lines = []
                    while True:
                        line = next(fin)
                        edge_lines.append(line)
                        if line.strip().startswith('}'):
                            break
                    
                    # Parse target nodes and filter
                    targets = []
                    for edge_line in edge_lines:
                        target_match = re.match(r'^"([^"]+)"$', edge_line.strip())
                        if target_match:
                            target_node = target_match.group(1)
                            if target_node in packages:
                                targets.append(target_node)
                    
                    # Write filtered edge if there are valid targets
                    if targets:
                        fout.write(f'"{source_node}" -> {{\n')
                        for target in targets:
                            fout.write(f'"{target}"\n')
                        fout.write('};\n\n')
                continue
            
            # Write closing brace
            if stripped == '}':
                fout.write(line)
                continue


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <graph.dot> <packages.txt> <output.dot>")
        print("  Filter DOT graph to only include packages from the package list")
        sys.exit(1)
    
    input_graph = sys.argv[1]
    package_list = sys.argv[2]
    output_graph = sys.argv[3]
    
    print(f"Loading packages from {package_list}...")
    packages = load_packages(package_list)
    print(f"Found {len(packages)} packages")
    
    print(f"Filtering graph from {input_graph}...")
    filter_graph(input_graph, output_graph, packages)
    print(f"Filtered graph written to {output_graph}")


if __name__ == '__main__':
    main()
