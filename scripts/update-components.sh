#!/bin/bash
# Script to find missing components from VM image packages and add them to components.toml

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
COMPONENTS_TOML="$REPO_ROOT/base/comps/components.toml"
PACKAGES_FILE="$REPO_ROOT/base/out/images/vm-base/azl4-vm-base.x86_64-0.1.packages"

# Check if packages file exists
if [[ ! -f "$PACKAGES_FILE" ]]; then
    echo "Error: Packages file not found: $PACKAGES_FILE"
    echo "Please build the VM image first."
    exit 1
fi

# Check if components.toml exists
if [[ ! -f "$COMPONENTS_TOML" ]]; then
    echo "Error: components.toml not found: $COMPONENTS_TOML"
    exit 1
fi

echo "Finding missing components..."

# Get the list of missing components
MISSING_COMPONENTS=$(
    for comp in $(dnf repoquery -q -y --srpm $(cat "$PACKAGES_FILE" | sed -e "s/|.*//") --queryformat '%{name}\n' | sort | uniq); do
        azldev comp list "$comp" 2>&1
    done | grep "component not found" | sed -e "s/component not found: //" | sort | uniq
)

if [[ -z "$MISSING_COMPONENTS" ]]; then
    echo "No missing components found!"
    exit 0
fi

echo "Missing components found:"
echo "$MISSING_COMPONENTS"
echo ""

# Add each missing component to components.toml
for comp in $MISSING_COMPONENTS; do
    # Check if component already exists in the file
    if grep -q "^\[components\.$comp\]$" "$COMPONENTS_TOML"; then
        echo "Skipping $comp - already exists in components.toml"
        continue
    fi
    
    # Create the component entry
    ENTRY="[components.$comp]"
    
    # Find the correct alphabetical position and insert
    # We'll append to the file and then sort it properly
    echo "" >> "$COMPONENTS_TOML"
    echo "$ENTRY" >> "$COMPONENTS_TOML"
    echo "Added: $comp"
done

# Now sort the components.toml file to maintain alphabetical order
echo ""
echo "Sorting components.toml..."

# Extract header (everything before first [components.)
HEADER=$(sed -n '1,/^\[components\./{ /^\[components\./!p }' "$COMPONENTS_TOML")

# Extract all component sections and sort them
# Each component is just a single line like [components.name] or [components.'python3.14']
# Sort by ignoring single quotes so 'python3.14' sorts as python3.14
COMPONENTS=$(grep '^\[components\.' "$COMPONENTS_TOML" | uniq | \
    awk -F'.' '{
        # Get the component name (everything after [components.)
        name = substr($0, 13)  # Skip "[components."
        gsub(/\]$/, "", name)  # Remove trailing ]
        gsub(/'\''/, "", name) # Remove single quotes for sort key
        print name "\t" $0
    }' | sort -f -t$'\t' -k1,1 | cut -f2)

# Rewrite the file
{
    echo "$HEADER"
    echo "$COMPONENTS"
} > "$COMPONENTS_TOML"

echo "Done! Components added and file sorted."
echo ""
echo "Run 'git diff $COMPONENTS_TOML' to see the changes."
