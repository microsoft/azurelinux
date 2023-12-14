#!/bin/bash

set -x
set -e

cd /home/afo123

cp dmsquash-generator.sh /usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-generator.sh
chown root:root /usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-generator.sh

cp dmsquash-live-root.sh /usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-live-root.sh
chown root:root /usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-live-root.sh

cp dracut-emergency.sh   /usr/lib/dracut/modules.d/98dracut-systemd/dracut-emergency.sh
chown root:root /usr/lib/dracut/modules.d/98dracut-systemd/dracut-emergency.sh

cp dracut-mount.sh       /usr/lib/dracut/modules.d/98dracut-systemd/dracut-mount.sh
chown root:root /usr/lib/dracut/modules.d/98dracut-systemd/dracut-mount.sh

cp iso-scan.sh           /usr/lib/dracut/modules.d/90dmsquash-live/iso-scan.sh
chown root:root /usr/lib/dracut/modules.d/90dmsquash-live/iso-scan.sh

cp 20-gmileka.conf       /etc/dracut.conf.d/20-gmileka.conf
chown root:root /etc/dracut.conf.d/20-gmileka.conf

rm -f /home/afo123/initrd.img 
dracut /home/afo123/initrd.img \
    --filesystems "squashfs" \
    --include /usr/bin/more /usr/sbin/more \
    --include /usr/bin/vim /usr/sbin/vim \
    --include /usr/bin/lsblk /usr/sbin/lsblk \
    --include /usr/bin/grep /usr/bin/grep

chown afo123:afo123 /home/afo123/initrd.img 
ls -la /home/afo123
