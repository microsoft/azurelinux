#!/bin/bash

set -x
set -e

inputRootDir=$1
outputRootDir=$2

function create_init_script() {
    local initScriptPath=$1

    sudo cat > $initScriptPath <<EOF
mount -t proc proc /proc
/lib/systemd/systemd
EOF
    sudo chmod 775 $initScriptPath
}

# ---- main ----
sudo rm -rf $outputRootDir
mkdir -p $outputRootDir
sudo cp -r -a $inputRootDir/* $outputRootDir

sudo cp /home/george/git/CBL-Mariner/toolkit/mic-iso-gen/files/prov/mariner-iso-start-up-minimal.sh $outputRootDir/root/mariner-iso-start-up.sh
sudo cp /home/george/git/CBL-Mariner/toolkit/mic-iso-gen/chroot-remove-packages.sh $outputRootDir/
sudo rm -f $outputRootDir/etc/fstab
sudo touch $outputRootDir/etc/fstab

pushd $outputRootDir
sudo patch -p1 -i /home/george/git/CBL-Mariner/toolkit/mic-iso-gen/passwd.patch
popd

create_init_script $outputRootDir/init

sudo chroot $outputRootDir /bin/bash -c "sudo /chroot-remove-packages.sh"
sudo chroot $outputRootDir /bin/bash -c "chown -R root:root ."

sudo chmod 744 $outputRootDir/boot
sudo chmod 755 $outputRootDir/etc/shadow
