#!/bin/bash
set -euo pipefail
export LC_ALL=C

fixture=$1
work=$(mktemp -d "${TMPDIR:-/tmp}/e2fsck-orphan-test.XXXXXXXX")
cleanup() {
    status=$?
    if (( status != 0 )); then
        for log in "$work"/*.log; do
            [ -f "$log" ] && { echo "=== $log ==="; cat "$log"; }
        done
    fi
    rm -rf -- "$work"
}
trap cleanup EXIT

features() {
    ./misc/dumpe2fs -h "$1" 2>/dev/null | grep '^Filesystem features:'
}

# Upstream f_clear_orphan_file fixture has an unclean journal and populated,
# checksummed orphan blocks.
gzip -dc "$fixture" > "$work/original.img"
features "$work/original.img" | grep -qw orphan_present
features "$work/original.img" | grep -qw needs_recovery

cp "$work/original.img" "$work/normal.img"
./e2fsck/e2fsck -y "$work/normal.img" > "$work/normal.log" 2>&1
grep -q 'Clearing orphaned inode 13 ' "$work/normal.log"
grep -q ': clean,' "$work/normal.log"
! grep -q 'Pass 1:' "$work/normal.log"
! features "$work/normal.img" | grep -qw orphan_present
./e2fsck/e2fsck -fn "$work/normal.img" > "$work/verify.log" 2>&1
! grep -Eiq 'wrong checksum|not clean|Fix\?' "$work/verify.log"

cp "$work/original.img" "$work/preen.img"
./e2fsck/e2fsck -p "$work/preen.img" > "$work/preen.log" 2>&1
grep -q 'Clearing orphaned inode 13 ' "$work/preen.log"
grep -q ': clean,' "$work/preen.log"
! features "$work/preen.img" | grep -qw orphan_present

cp "$work/original.img" "$work/journal.img"
./e2fsck/e2fsck -E journal_only -y "$work/journal.img" > "$work/journal.log" 2>&1
grep -q 'Clearing orphaned inode 13 ' "$work/journal.log"
! features "$work/journal.img" | grep -qw orphan_present
./e2fsck/e2fsck -fn "$work/journal.img" > "$work/journal-verify.log" 2>&1
! grep -Eiq 'orphan file.*(wrong checksum|not clean)' "$work/journal-verify.log"

# A bad orphan-block checksum must not be accepted by journal-only recovery.
cp "$work/journal.img" "$work/corrupt.img"
./debugfs/debugfs -w -R 'feature orphan_present' "$work/corrupt.img" > "$work/debugfs.log" 2>&1
block=$(./debugfs/debugfs -R 'blocks <12>' "$work/corrupt.img" 2>/dev/null | awk '{print $1}')
[[ "$block" =~ ^[0-9]+$ ]]
printf '\0\0\0\0' | dd of="$work/corrupt.img" bs=1 seek=$((block * 1024 + 1020)) conv=notrunc status=none
status=0
./e2fsck/e2fsck -E journal_only -y "$work/corrupt.img" > "$work/corrupt.log" 2>&1 || status=$?
[[ $status -eq 0 || $status -eq 4 ]]
grep -q 'wrong checksum' "$work/corrupt.log"
features "$work/corrupt.img" | grep -qw orphan_present
./misc/dumpe2fs -h "$work/corrupt.img" 2>/dev/null | grep -q 'Filesystem state:.*not clean'

cp "$work/normal.img" "$work/required.img"
./misc/tune2fs -c 1 -C 2 "$work/required.img" > "$work/tune.log" 2>&1
./e2fsck/e2fsck -y "$work/required.img" > "$work/required.log" 2>&1
grep -q 'check forced' "$work/required.log"
grep -q 'Pass 1:' "$work/required.log"

cp "$work/normal.img" "$work/errors.img"
./debugfs/debugfs -w -R 'feature orphan_present' "$work/errors.img" > "$work/errors-debugfs.log" 2>&1
./debugfs/debugfs -w -R 'set_super_value state 3' "$work/errors.img" >> "$work/errors-debugfs.log" 2>&1
status=0
./e2fsck/e2fsck -y "$work/errors.img" > "$work/errors.log" 2>&1 || status=$?
[[ $status -eq 0 || $status -eq 1 ]]
grep -q 'Pass 1:' "$work/errors.log"
echo 'Orphan-file recovery regression tests passed'
