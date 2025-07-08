#!/bin/sh

echo "Running mountbootpartition-genrules.sh" > /dev/kmsg

# this gets called after all devices have settled.
/sbin/initqueue --finished --onetime --unique /sbin/mountbootpartition > /dev/kmsg
