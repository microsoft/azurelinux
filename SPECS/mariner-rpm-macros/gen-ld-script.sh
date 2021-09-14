#!/bin/bash
echo "gen-ld-script.sh generating linker script"

# 
# Embed the following metadata:
#
# {
#  "os": "mariner",
#  "osVersion": "2.0",
#  "type": "rpm"
# }

LINKER_SCRIPT_START="SECTIONS { .note.package ALIGN(4): { "
LINKER_SCRIPT_NAMESZ="BYTE(0x04) BYTE(0x00) BYTE(0x00) BYTE(0x00) "
LINKER_SCRIPT_DESCSZ="BYTE(0x3c) BYTE(0x00) BYTE(0x00) BYTE(0x00) "
LINKER_SCRIPT_TYPE="BYTE(0x7e) BYTE(0x1a) BYTE(0xfe) BYTE(0xca) "
LINKER_SCRIPT_NAME="BYTE(0x46) BYTE(0x44) BYTE(0x4f) BYTE(0x00) "
LINKER_SCRIPT_DESC="BYTE(0x7b) BYTE(0x0a) BYTE(0x20) BYTE(0x22)
                    BYTE(0x6f) BYTE(0x73) BYTE(0x22) BYTE(0x3a)
                    BYTE(0x20) BYTE(0x22) BYTE(0x6d) BYTE(0x61)
                    BYTE(0x72) BYTE(0x69) BYTE(0x6e) BYTE(0x65)
                    BYTE(0x72) BYTE(0x22) BYTE(0x2c) BYTE(0x0a)
                    BYTE(0x20) BYTE(0x22) BYTE(0x6f) BYTE(0x73)
                    BYTE(0x56) BYTE(0x65) BYTE(0x72) BYTE(0x73)
                    BYTE(0x69) BYTE(0x6f) BYTE(0x6e) BYTE(0x22)
                    BYTE(0x3a) BYTE(0x20) BYTE(0x22) BYTE(0x32)
                    BYTE(0x2e) BYTE(0x30) BYTE(0x22) BYTE(0x2c)
                    BYTE(0x0a) BYTE(0x20) BYTE(0x22) BYTE(0x74)
                    BYTE(0x79) BYTE(0x70) BYTE(0x65) BYTE(0x22)
                    BYTE(0x3a) BYTE(0x20) BYTE(0x22) BYTE(0x72)
                    BYTE(0x70) BYTE(0x6d) BYTE(0x22) BYTE(0x0a)
                    BYTE(0x7d) BYTE(0x00) BYTE(0x00) BYTE(0x00) "
LINKER_SCRIPT_END="KEEP (*(.note.package)) } } INSERT AFTER .note.gnu.build-id;"

echo $LINKER_SCRIPT_START $LINKER_SCRIPT_NAMESZ $LINKER_SCRIPT_DESCSZ $LINKER_SCRIPT_TYPE $LINKER_SCRIPT_NAME $LINKER_SCRIPT_DESC $LINKER_SCRIPT_END > /usr/src/mariner/BUILD/module_info.ld
