#!/bin/sh

. /lib/kdump-lib-initramfs.sh

set -o pipefail
export PATH=$PATH:$KDUMP_SCRIPT_DIR

get_kdump_confs
do_failure_action
do_final_action
