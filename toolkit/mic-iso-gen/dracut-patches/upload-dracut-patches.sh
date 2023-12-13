#!/bin/bash

set -x
set -e

scp ~/git/CBL-Mariner/toolkit/mic-iso-gen/dracut-patches/dmsquash-generator.sh afo123@10.137.194.51:~/
scp ~/git/CBL-Mariner/toolkit/mic-iso-gen/dracut-patches/dmsquash-live-root.sh afo123@10.137.194.51:~/
scp ~/git/CBL-Mariner/toolkit/mic-iso-gen/dracut-patches/dracut-emergency.sh afo123@10.137.194.51:~/
scp ~/git/CBL-Mariner/toolkit/mic-iso-gen/dracut-patches/dracut-mount.sh afo123@10.137.194.51:~/
scp ~/git/CBL-Mariner/toolkit/mic-iso-gen/dracut-patches/iso-scan.sh afo123@10.137.194.51:~/
scp ~/git/CBL-Mariner/toolkit/mic-iso-gen/dracut-patches/20-gmileka.conf afo123@10.137.194.51:~/

scp ~/git/CBL-Mariner/toolkit/mic-iso-gen/dracut-patches/rebuild-initrd.sh afo123@10.137.194.51:~/