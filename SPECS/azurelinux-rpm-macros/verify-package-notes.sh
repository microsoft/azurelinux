#!/usr/bin/env bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Usage:
# ./verify-package-notes.sh <input_binary> <input_note_section_binary> <note_section_name>
# This script verifies .note.package is successfully stamped to ELF executable or shared library
#

set -e
INPUT_BINARY=$1
INPUT_NOTE_BINARY=$2
SECTION_NAME=$3
NUM_ARGS=$#
OBJCOPY=${OBJCOPY:-objcopy}
SECTION_OUTPUT="tmp${SECTION_NAME}.bin"

if [[ -z "${INPUT_BINARY}" || -z "${SECTION_NAME}" || ${NUM_ARGS} != 3 ]]; then
    echo "Usage format: ./verify-package-notes.sh <input_binary> <input_note_section_binary> <note_section_name>"
    echo "Example: ./verify-package-notes.sh ${DIR}/hello_world ${DIR}/.note.package .note.package"
    echo "This script checks if .note.package section was properly stamped to ELF binary"
    exit -1
fi

if [ ! -f "${INPUT_BINARY}" ]; then
    echo "${INPUT_BINARY} file not found!"
    exit -1
fi

if [ ! -f "${INPUT_NOTE_BINARY}" ]; then
    echo "${INPUT_NOTE_BINARY} file not found!"
    exit -1
fi

echo "${OBJCOPY} -O binary -j ${SECTION_NAME} ${INPUT_BINARY} ${SECTION_OUTPUT}"
${OBJCOPY} -O binary -j ${SECTION_NAME} ${INPUT_BINARY} ${SECTION_OUTPUT};
if [ $? != 0 ]; then
    echo "FAIL... Extracting ${SECTION_NAME} section attempt failed. ${SECTION_OUTPUT} file is incomplete..."
    rm -fv ${SECTION_OUTPUT}
    exit -2
fi

printf "\nChecking if .note.package and note section in ${INPUT_BINARY} are identical...\n"
if ! cmp -s "${INPUT_NOTE_BINARY}" "${SECTION_OUTPUT}" ; then
    echo "FAIL... ${SECTION_NAME} is not stamped into ${INPUT_BINARY} file..."
    rm -fv ${SECTION_OUTPUT}
    exit -3
fi

rm -fv ${SECTION_OUTPUT}
printf "\nSUCCESS... Verified ${INPUT_BINARY} successfully stamped...\n"
exit 0

