#!/bin/bash

set -e

errorFunc() {
    return 1
}

okFunc() {
    return 0
}

echo "Running test"
if ! errorFunc; then
    echo "Error function failed"
    exit 1
fi
echo "Finished test"
