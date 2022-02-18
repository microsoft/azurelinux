#!/bin/bash

# /usr/lib/rpm/mariner/gen-ld-script.sh %{_topdir}
if [ -z "$1" ]; then
    TOPDIR="/usr/src/mariner"
else
    TOPDIR="$1"
fi

echo "gen-ld-script.sh generating linker script with topdir($TOPDIR)"

# Generate linker script that will add the following note to ELF files:
#
# Displaying notes found in: .note.package
#  Owner                 Data size       Description
#  FDO                  0x0000003c       Unknown note type: (0xcafe1a7e)
#   description data: 7b 0a 20 22 6f 73 22 3a 20 22 6d 61 72 69 6e 65 72 22 2c 0a 20 22 6f 73 56 65 72 73 69 6f 6e 22 3a 20 22 31 2e 30 22 2c 0a 20 22 74 79 70 65 22 3a 20 22 72 70 6d 22 0a 7d 00 00 00

LINKER_SCRIPT_START="SECTIONS { .note.package ALIGN(4): { "

# "namesz" - number of bytes in "name" below (0x4)
LINKER_SCRIPT_NAMESZ="BYTE(0x04) BYTE(0x00) BYTE(0x00) BYTE(0x00) "

# "descz" - number of bytes in "desc" below, not including padding (0x3c)
LINKER_SCRIPT_DESCSZ="BYTE(0x3c) BYTE(0x00) BYTE(0x00) BYTE(0x00) "

# "type" - this is the note-id - "0xcafe1a7e"
LINKER_SCRIPT_TYPE="BYTE(0x7e) BYTE(0x1a) BYTE(0xfe) BYTE(0xca) "

# "name" - this is the owner - "FDO\0"
LINKER_SCRIPT_NAME="BYTE(0x46) BYTE(0x44) BYTE(0x4f) BYTE(0x00) "

# "description" - this is the JSON format metadata:
# {
#  "os": "mariner",
#  "osVersion": "1.0",
#  "type": "rpm"
# }
LINKER_SCRIPT_DESC="BYTE(0x7b) BYTE(0x0a) BYTE(0x20) BYTE(0x22)
                    BYTE(0x6f) BYTE(0x73) BYTE(0x22) BYTE(0x3a)
                    BYTE(0x20) BYTE(0x22) BYTE(0x6d) BYTE(0x61)
                    BYTE(0x72) BYTE(0x69) BYTE(0x6e) BYTE(0x65)
                    BYTE(0x72) BYTE(0x22) BYTE(0x2c) BYTE(0x0a)
                    BYTE(0x20) BYTE(0x22) BYTE(0x6f) BYTE(0x73)
                    BYTE(0x56) BYTE(0x65) BYTE(0x72) BYTE(0x73)
                    BYTE(0x69) BYTE(0x6f) BYTE(0x6e) BYTE(0x22)
                    BYTE(0x3a) BYTE(0x20) BYTE(0x22) BYTE(0x31)
                    BYTE(0x2e) BYTE(0x30) BYTE(0x22) BYTE(0x2c)
                    BYTE(0x0a) BYTE(0x20) BYTE(0x22) BYTE(0x74)
                    BYTE(0x79) BYTE(0x70) BYTE(0x65) BYTE(0x22)
                    BYTE(0x3a) BYTE(0x20) BYTE(0x22) BYTE(0x72)
                    BYTE(0x70) BYTE(0x6d) BYTE(0x22) BYTE(0x0a)
                    BYTE(0x7d) BYTE(0x00) BYTE(0x00) BYTE(0x00) "

LINKER_SCRIPT_END="KEEP (*(.note.package)) } } INSERT AFTER .note.gnu.build-id;"

mkdir -pv $TOPDIR/BUILD
echo $LINKER_SCRIPT_START $LINKER_SCRIPT_NAMESZ $LINKER_SCRIPT_DESCSZ $LINKER_SCRIPT_TYPE $LINKER_SCRIPT_NAME $LINKER_SCRIPT_DESC $LINKER_SCRIPT_END > $TOPDIR/BUILD/module_info.ld
