#!/bin/bash

set -x
set -e

initrdRootDir=$1

function create_init_script() {
    local initScriptPath=$1

    sudo cat > $initScriptPath <<EOF
mount -t proc proc /proc
/lib/systemd/systemd
EOF
    sudo chmod 775 $initScriptPath
}

# ---- main ----

sudo cp /home/george/git/argus-toolkit/prov-builder/files/mariner-iso-start-up.sh $initrdRootDir/root/
sudo cp /home/george/git/CBL-Mariner/toolkit/mic-iso-gen/2-1-1-chroot-1-remove-packages.sh $initrdRootDir/
sudo rm -f $initrdRootDir/etc/fstab
sudo touch $initrdRootDir/etc/fstab

# pushd $initrdRootDir
# sudo patch -p1 -i /home/george/git/CBL-Mariner/toolkit/mic-iso-gen/passwd.patch
# popd

create_init_script $initrdRootDir/init

sudo chroot $initrdRootDir /bin/bash -c "sudo /2-1-1-chroot-1-remove-packages.sh"
sudo chroot $initrdRootDir /bin/bash -c "chown -R root:root ."

sudo chmod 744 $initrdRootDir/boot
