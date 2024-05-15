#!/bin/sh

set -x

systemctl enable liveos-artifacts-download
/sbin/initqueue --settled --onetime --unique /sbin/schedule-liveos-artifacts-download
