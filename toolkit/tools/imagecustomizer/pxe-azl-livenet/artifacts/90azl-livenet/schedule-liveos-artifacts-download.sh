#!/bin/sh

set -x

systemctl enable liveos-artifacts-download
systemctl start liveos-artifacts-download &
