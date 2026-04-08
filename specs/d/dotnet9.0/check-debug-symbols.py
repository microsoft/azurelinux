#!/usr/bin/python3

"""
Check debug symbols are present in shared object and can identify
code.

It starts scanning from a directory and recursively scans all ELF
files found in it for various symbols to ensure all debuginfo is
present and nothing has been stripped.

Usage:

./check-debug-symbols /path/of/dir/to/scan/


Example:

./check-debug-symbols /usr/lib64
"""

# This technique was explained to me by Mark Wielaard (mjw).

import collections
import os
import re
import subprocess
import sys

ScanResult = collections.namedtuple('ScanResult',
                                    'file_name debug_info debug_abbrev file_symbols gnu_debuglink')

file_symbol_exclude_list = [
    'ilc',
]

def scan_file(file):
    "Scan the provided file and return a ScanResult containing results of the scan."

    # Test for .debug_* sections in the shared object. This is the  main test.
    # Stripped objects will not contain these.
    readelf_S_result = subprocess.run(['eu-readelf', '-S', file],
                                      stdout=subprocess.PIPE, encoding='utf-8', check=True)
    has_debug_info = any(line for line in readelf_S_result.stdout.split('\n') if '] .debug_info' in line)

    has_debug_abbrev = any(line for line in readelf_S_result.stdout.split('\n') if '] .debug_abbrev' in line)

    # Test FILE symbols. These will most likely be removed by anyting that
    # manipulates symbol tables because it's generally useless. So a nice test
    # that nothing has messed with symbols.
    def contains_file_symbols(line):
        parts = line.split()
        if len(parts) < 8:
            return False
        return \
            parts[2] == '0' and parts[3] == 'FILE' and parts[4] == 'LOCAL' and parts[5] == 'DEFAULT' and \
            parts[6] == 'ABS' and re.match(r'((.*/)?[-_a-zA-Z0-9]+\.(c|cc|cpp|cxx))?', parts[7])

    readelf_s_result = subprocess.run(["eu-readelf", '-s', file],
                                      stdout=subprocess.PIPE, encoding='utf-8', check=True)
    has_file_symbols = True
    if not os.path.basename(file) in file_symbol_exclude_list:
        has_file_symbols = any(line for line in readelf_s_result.stdout.split('\n') if contains_file_symbols(line))

    # Test that there are no .gnu_debuglink sections pointing to another
    # debuginfo file. There shouldn't be any debuginfo files, so the link makes
    # no sense either.
    has_gnu_debuglink = any(line for line in readelf_s_result.stdout.split('\n') if '] .gnu_debuglink' in line)

    return ScanResult(file, has_debug_info, has_debug_abbrev, has_file_symbols, has_gnu_debuglink)

def is_elf(file):
    result = subprocess.run(['file', file], stdout=subprocess.PIPE, encoding='utf-8', check=True)
    return re.search(r'ELF 64-bit [LM]SB (?:pie )?(?:executable|shared object)', result.stdout)

def scan_file_if_sensible(file):
    if is_elf(file):
        return scan_file(file)
    return None

def scan_dir(dir):
    results = []
    for root, _, files in os.walk(dir):
        for name in files:
            result = scan_file_if_sensible(os.path.join(root, name))
            if result:
                results.append(result)
    return results

def scan(file):
    file = os.path.abspath(file)
    if os.path.isdir(file):
        return scan_dir(file)
    elif os.path.isfile(file):
        return [scan_file_if_sensible(file)]

def is_bad_result(result):
    return not result.debug_info or not result.debug_abbrev or not result.file_symbols or result.gnu_debuglink

def print_scan_results(results, verbose):
    # print(results)
    for result in results:
        file_name = result.file_name
        found_issue = False
        if not result.debug_info:
            found_issue = True
            print('error: missing .debug_info section in', file_name)
        if not result.debug_abbrev:
            found_issue = True
            print('error: missing .debug_abbrev section in', file_name)
        if not result.file_symbols:
            found_issue = True
            print('error: missing FILE symbols in', file_name)
        if result.gnu_debuglink:
            found_issue = True
            print('error: unexpected .gnu_debuglink section in', file_name)
        if verbose and not found_issue:
            print('OK: ', file_name)

def main(args):
    verbose = False
    files = []
    for arg in args:
        if arg == '--verbose' or arg == '-v':
            verbose = True
        else:
            files.append(arg)

    results = []
    for file in files:
        results.extend(scan(file))

    print_scan_results(results, verbose)

    if any(is_bad_result(result) for result in results):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
