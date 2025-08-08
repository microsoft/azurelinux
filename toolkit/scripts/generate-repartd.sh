#!/bin/bash
# Regenerate files/repart.d/* based on the disks section of the osguard config.yaml
# Requires: yq (https://github.com/mikefarah/yq)

set -euo pipefail

CONFIG="$(dirname "$0")/../imageconfigs/osguard-amd64.yaml"
REPART_DIR="$(dirname "$0")/../imageconfigs/files/osguard/repart.d"

mkdir -p "$REPART_DIR"
rm -f "$REPART_DIR"/*.conf

emit_partition() {
    local num="$1" part="$2" type="$3" label="$4" size="$5"
    # Set Type for root and root-hash partitions
    if [[ "$part" =~ ^usr-(a|b)$ ]]; then
        type_out="usr"
    elif [[ "$part" =~ ^usr-hash-(a|b)$ ]]; then
        type_out="usr-verity"
    else
        type_out="$type"
    fi
    
    # Ensure label is never null
    if [[ -z "$label" || "$label" == "null" ]]; then
        label="$part"
    fi
    
    if [[ "$part" =~ ^root-(a|b)$ ]]; then
        cat > "$REPART_DIR/$(printf '%02d' $num)-${part}.conf" <<EOF
[Partition]
Type=$type_out
Label=$label
SizeMinBytes=12G
Weight=1000
GrowFileSystem=true
EOF
    else
        cat > "$REPART_DIR/$(printf '%02d' $num)-${part}.conf" <<EOF
[Partition]
Type=$type_out
Label=$label
SizeMinBytes=$size
SizeMaxBytes=$size
EOF
    fi
}

# Generate all A partitions and collect B info
num=10
declare -a bparts
for part in $(yq -r '.storage.disks[0].partitions[].id' "$CONFIG"); do
    type=$(yq -r ".storage.disks[0].partitions[] | select(.id == \"$part\") | .type" "$CONFIG")
    label=$(yq -r ".storage.disks[0].partitions[] | select(.id == \"$part\") | .label" "$CONFIG")
    size=$(yq -r ".storage.disks[0].partitions[] | select(.id == \"$part\") | .size" "$CONFIG")
    emit_partition $num $part $type $label $size
    if [[ "$part" =~ ^(boot|usr|usr-hash|var|root)-a$ ]]; then
        bpart="${part/-a/-b}"
        blabel="${label/-a/-b}"
        bparts+=("$bpart|$type|$blabel|$size")
    fi
    num=$((num+1))
done

# Generate all B partitions
for b in "${bparts[@]}"; do
    IFS='|' read -r bpart type blabel size <<< "$b"
    emit_partition $num $bpart $type $blabel $size
    num=$((num+1))
done

echo "Repart.d configs generated in $REPART_DIR"
