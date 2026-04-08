#!/bin/sh
if [ $# -ge 1 ]; then
  BIN=$1
else
  BIN=uutils-coreutils
fi
$BIN --help | grep , | paste -s | tr -d '[:space:]' | tr ',' ' '
