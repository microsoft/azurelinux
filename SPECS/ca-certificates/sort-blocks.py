#!/usr/bin/python3

# Expected input is a file, where blocks of lines are separated by newline.
# Blocks will be sorted.
# Intention is to prepare files for comparison, were lines inside each block are
# in stable order, but the order of blocks is random.

import sys
import string

if (len(sys.argv) != 2):
    print("syntax: " + sys.argv[0] + " input-filename")
    sys.exit(1)

filename = sys.argv[1]

block = []
block_list = []
with open(filename, 'r') as f:
    for line in f:
        if (len(line) == 1):
            if len(block) == 0:
                continue
            else:
                combined_string = string.join(block, '')
                block_list.append(combined_string)
                block = []
        else:
            block.append(line)

block_list.sort()

for block in block_list:
    print(block)
