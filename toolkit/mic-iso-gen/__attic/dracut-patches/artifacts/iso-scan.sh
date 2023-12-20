#!/bin/sh

echo "---- iso-scan.sh 1 ----- debugging iso-scan.sh ------------------------------"
sleep 2s

type getarg > /dev/null 2>&1 || . /lib/dracut-lib.sh

PATH=/usr/sbin:/usr/bin:/sbin:/bin

isofile=$1

[ -z "$isofile" ] && exit 1

ismounted "/run/initramfs/isoscan" && exit 0

mkdir -p "/run/initramfs/isoscan"

echo "---- iso-scan.sh 2 --listing /dev/disk/by-uuid/ ----"
ls -la /dev/disk/by-uuid
sleep 2s

do_iso_scan() {
    local _name
    local dev
    for dev in /dev/disk/by-uuid/*; do
        echo "---- iso-scan.sh 3 ----- enumerating devices..."
        sleep 2s

        _name=$(dev_unit_name "$dev")
        [ -e /tmp/isoscan-"${_name}" ] && continue
        : > /tmp/isoscan-"${_name}"

        echo "----- iso-scan.sh 4 ---- mounting $dev on /run/initramfs/isoscan"
        sleep 2s
        mount -t auto -o ro "$dev" "/run/initramfs/isoscan" || continue

        echo "----- iso-scan.sh 5 ---- mounted!"
        sleep 2s
        echo "----- iso-scan.sh 6 ---- check if /run/initramfs/isoscan/$isofile exists..."
        sleep 2s
  
        if [ -f "/run/initramfs/isoscan/$isofile" ]; then
            echo "----- iso-scan.sh 7 ---- found file!"
            echo "----- iso-scan.sh 7.1 ---- creating loop device and calling udevamd trigger..."
            sleep 2s
            
            losetup -f "/run/initramfs/isoscan/$isofile"
            udevadm trigger --action=add > /dev/null 2>&1

            echo "----- iso-scan.sh 7.2 ---- loop device created for wrapper image."
            # echo "----- iso-scan.sh 7.3 ---- listing devices..."
            # ls -la /dev
            # sleep 2s

            ln -s "$dev" /run/initramfs/isoscandev
            rm -f -- "$job"
            # echo "----- iso-scan.sh 7.4 ----"
            # lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,UUID,PARTLABEL,PARTUUID
            echo "----- iso-scan.sh 7.5 ---- iso-scan.sh ---- COMPLETED SUCCESSFULLY ----. Exiting..."
            sleep 2s
            exit 0
        else
            echo "----- iso-scan.sh 8 ---- file not found!"
            sleep 2s

            umount "/run/initramfs/isoscan"
        fi

        echo "----- iso-scan.sh 9 ---- about to check another device..."
        sleep 2s
    done

    echo "----- iso-scan.sh 10 ---- done enumerating devices."
    sleep 2s
}

do_iso_scan

echo "----- iso-scan.sh --- could not find device/file ------"
sleep 10s

rmdir "/run/initramfs/isoscan"
exit 1
