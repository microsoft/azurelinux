#!/bin/bash
set -e

OUTPUT_DIR="$(dirname "$(readlink -f "$0")")/out"
FILTER_SCRIPT="./filter-graph.py"

REPOGRAPH="$OUTPUT_DIR/repograph.dot"
FILTERED_GRAPH="$OUTPUT_DIR/filtered-repograph.dot"
TEMP_PACKAGES="$OUTPUT_DIR/packages.txt"

# echo "Extracting package names from image.manifest..."
# jq -r '.packages[].name' "$IMAGE_MANIFEST" > "$TEMP_PACKAGES"

#echo "Found $(wc -l < "$TEMP_PACKAGES") packages in manifest"

if [ -f "$REPOGRAPH" ]; then
    echo "Filtering repograph.dot..."
    python3 "$FILTER_SCRIPT" "$REPOGRAPH" "$TEMP_PACKAGES" "$FILTERED_GRAPH"
else
    echo "Warning: repograph.dot not found at $REPOGRAPH"
fi

# rm -f "$TEMP_PACKAGES"