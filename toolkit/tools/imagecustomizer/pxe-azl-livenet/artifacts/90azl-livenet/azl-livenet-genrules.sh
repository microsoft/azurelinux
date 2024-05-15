#!/bin/sh

set -x

systemctl enable liveos-artifacts-download
/sbin/initqueue --settled --onetime --unique /usr/local/bin/schedule-liveos-artifacts-download.sh
