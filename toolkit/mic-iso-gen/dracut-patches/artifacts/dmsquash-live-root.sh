#!/bin/bash

set -x

type getarg > /dev/null 2>&1 || . /lib/dracut-lib.sh

command -v unpack_archive > /dev/null || . /lib/img-lib.sh

PATH=/usr/sbin:/usr/bin:/sbin:/bin

if getargbool 0 rd.live.debug -n -y rdlivedebug; then
    exec > /tmp/liveroot.$$.out
    exec 2>> /tmp/liveroot.$$.out
    set -x
fi

[ -z "$1" ] && exit 1
livedev="$1"

# parse various live image specific options that make sense to be
# specified as their own things
live_dir=$(getarg rd.live.dir -d live_dir)
[ -z "$live_dir" ] && live_dir="LiveOS"
squash_image=$(getarg rd.live.squashimg)
[ -z "$squash_image" ] && squash_image="squashfs.img"

getargbool 0 rd.live.ram -d -y live_ram && live_ram="yes"
getargbool 0 rd.live.overlay.reset -d -y reset_overlay && reset_overlay="yes"
getargbool 0 rd.live.overlay.readonly -d -y readonly_overlay && readonly_overlay="--readonly" || readonly_overlay=""
overlay=$(getarg rd.live.overlay -d overlay)
getargbool 0 rd.writable.fsimg -d -y writable_fsimg && writable_fsimg="yes"
overlay_size=$(getarg rd.live.overlay.size=)
[ -z "$overlay_size" ] && overlay_size=32768

getargbool 0 rd.live.overlay.thin && thin_snapshot="yes"
getargbool 0 rd.live.overlay.overlayfs && overlayfs="yes"

# CD/DVD media check
[ -b "$livedev" ] && fs=$(blkid -s TYPE -o value "$livedev")
if [ "$fs" = "iso9660" -o "$fs" = "udf" ]; then
    check="yes"
fi
getarg rd.live.check -d check || check=""
if [ -n "$check" ]; then
    type plymouth > /dev/null 2>&1 && plymouth --hide-splash
    if [ -n "$DRACUT_SYSTEMD" ]; then
        p=$(dev_unit_name "$livedev")
        systemctl start checkisomd5@"${p}".service
    else
        checkisomd5 --verbose "$livedev"
    fi
    if [ $? -eq 1 ]; then
        die "CD check failed!"
        exit 1
    fi
    type plymouth > /dev/null 2>&1 && plymouth --show-splash
fi

ln -s "$livedev" /run/initramfs/livedev

# determine filesystem type for a filesystem image
det_img_fs() {
    udevadm settle >&2
    blkid -s TYPE -u noraid -o value "$1"
}

modprobe squashfs
CMDLINE=$(getcmdline)
for arg in $CMDLINE; do
    case $arg in
        ro | rw) liverw=$arg ;;
    esac
done

# mount the backing of the live image first
mkdir -m 0755 -p /run/initramfs/live
if [ -f "$livedev" ]; then
    # no mount needed - we've already got the LiveOS image in initramfs
    # check filesystem type and handle accordingly
    fstype=$(det_img_fs "$livedev")
    case $fstype in
        squashfs) SQUASHED=$livedev ;;
        auto) die "cannot mount live image (unknown filesystem type)" ;;
        *) FSIMG=$livedev ;;
    esac
    [ -e /sys/fs/"$fstype" ] || modprobe "$fstype"
else
    livedev_fstype=$(blkid -o value -s TYPE "$livedev")
    if [ "$livedev_fstype" = "squashfs" ]; then
        # no mount needed - we've already got the LiveOS image in $livedev
        SQUASHED=$livedev
    elif [ "$livedev_fstype" != "ntfs" ]; then
        if ! mount -n -t "$fstype" -o "${liverw:-ro}" "$livedev" /run/initramfs/live; then
            die "Failed to mount block device of live image"
            exit 1
        fi
    else
        # Symlinking /usr/bin/ntfs-3g as /sbin/mount.ntfs seems to boot
        # at the first glance, but ends with lots and lots of squashfs
        # errors, because systemd attempts to kill the ntfs-3g process?!
        if [ -x "/usr/bin/ntfs-3g" ]; then
            (exec -a @ntfs-3g ntfs-3g -o "${liverw:-ro}" "$livedev" /run/initramfs/live) | vwarn
        else
            die "Failed to mount block device of live image: Missing NTFS support"
            exit 1
        fi
    fi
fi

# overlay setup helper function
do_live_overlay() {
    # create a sparse file for the overlay
    # overlay: if non-ram overlay searching is desired, do it,
    #              otherwise, create traditional overlay in ram

    l=$(blkid -s LABEL -o value "$livedev") || l=""
    u=$(blkid -s UUID -o value "$livedev") || u=""

    if [ -z "$overlay" ]; then
        pathspec="/${live_dir}/overlay-$l-$u"
    elif strstr "$overlay" ":"; then
        # pathspec specified, extract
        pathspec=${overlay##*:}
    fi

    if [ -z "$pathspec" -o "$pathspec" = "auto" ]; then
        pathspec="/${live_dir}/overlay-$l-$u"
    fi
    devspec=${overlay%%:*}

    # need to know where to look for the overlay
    if [ -z "$setup" -a -n "$devspec" -a -n "$pathspec" -a -n "$overlay" ]; then
        mkdir -m 0755 -p /run/initramfs/overlayfs
        opt=''
        [ -n "$readonly_overlay" ] && opt=-r
        mount -n -t auto "$devspec" /run/initramfs/overlayfs || :
        if [ -f /run/initramfs/overlayfs$pathspec -a -w /run/initramfs/overlayfs$pathspec ]; then
            OVERLAY_LOOPDEV=$(losetup -f --show $opt /run/initramfs/overlayfs$pathspec)
            over=$OVERLAY_LOOPDEV
            umount -l /run/initramfs/overlayfs || :
            oltype=$(det_img_fs "$OVERLAY_LOOPDEV")
            if [ -z "$oltype" ] || [ "$oltype" = DM_snapshot_cow ]; then
                if [ -n "$reset_overlay" ]; then
                    info "Resetting the Device-mapper overlay."
                    dd if=/dev/zero of="$OVERLAY_LOOPDEV" bs=64k count=1 conv=fsync 2> /dev/null
                fi
                if [ -n "$overlayfs" ]; then
                    unset -v overlayfs
                    [ -n "$DRACUT_SYSTEMD" ] && reloadsysrootmountunit=":>/xor_overlayfs;"
                fi
                setup="yes"
            else
                mount -n -t "$oltype" $opt "$OVERLAY_LOOPDEV" /run/initramfs/overlayfs
                if [ -d /run/initramfs/overlayfs/overlayfs ] \
                    && [ -d /run/initramfs/overlayfs/ovlwork ]; then
                    ln -s /run/initramfs/overlayfs/overlayfs /run/overlayfs$opt
                    ln -s /run/initramfs/overlayfs/ovlwork /run/ovlwork$opt
                    if [ -z "$overlayfs" ] && [ -n "$DRACUT_SYSTEMD" ]; then
                        reloadsysrootmountunit=":>/xor_overlayfs;"
                    fi
                    overlayfs="required"
                    setup="yes"
                fi
            fi
        elif [ -d /run/initramfs/overlayfs$pathspec ] \
            && [ -d /run/initramfs/overlayfs$pathspec/../ovlwork ]; then
            ln -s /run/initramfs/overlayfs$pathspec /run/overlayfs$opt
            ln -s /run/initramfs/overlayfs$pathspec/../ovlwork /run/ovlwork$opt
            if [ -z "$overlayfs" ] && [ -n "$DRACUT_SYSTEMD" ]; then
                reloadsysrootmountunit=":>/xor_overlayfs;"
            fi
            overlayfs="required"
            setup="yes"
        fi
    fi
    if [ -n "$overlayfs" ]; then
        if ! modprobe overlay; then
            if [ "$overlayfs" = required ]; then
                die "OverlayFS is required but not available."
                exit 1
            fi
            [ -n "$DRACUT_SYSTEMD" ] && reloadsysrootmountunit=":>/xor_overlayfs;"
            m='OverlayFS is not available; using temporary Device-mapper overlay.'
            info "$m"
            unset -v overlayfs setup
        fi
    fi

    if [ -z "$setup" -o -n "$readonly_overlay" ]; then
        if [ -n "$setup" ]; then
            warn "Using temporary overlay."
        elif [ -n "$devspec" -a -n "$pathspec" ]; then
            [ -z "$m" ] \
                && m='   Unable to find a persistent overlay; using a temporary one.'
            m="$m"$'\n      All root filesystem changes will be lost on shutdown.'
            m="$m"$'\n         Press [Enter] to continue.'
            printf "\n\n\n\n%s\n\n\n" "${m}" > /dev/kmsg
            if [ -n "$DRACUT_SYSTEMD" ]; then
                if type plymouth > /dev/null 2>&1 && plymouth --ping; then
                    if getargbool 0 rhgb || getargbool 0 splash; then
                        m='>>>'$'\n''>>>'$'\n''>>>'$'\n\n\n'"$m"
                        m="${m%n.*}"$'n.\n\n\n''<<<'$'\n''<<<'$'\n''<<<'
                        plymouth display-message --text="${m}"
                    else
                        plymouth ask-question --prompt="${m}" --command=true
                    fi
                else
                    m=">>>${m//.[[:space:]]/.}  <<<"
                    systemd-ask-password --timeout=0 "${m}"
                fi
            else
                type plymouth > /dev/null 2>&1 && plymouth --ping && plymouth --quit
                read -s -r -p $'\n\n'"${m}" -n 1 _
            fi
        fi
        if [ -n "$overlayfs" ]; then
            mkdir -m 0755 -p /run/overlayfs
            mkdir -m 0755 -p /run/ovlwork
            if [ -n "$readonly_overlay" ] && ! [ -h /run/overlayfs-r ]; then
                info "No persistent overlay found."
                unset -v readonly_overlay
                [ -n "$DRACUT_SYSTEMD" ] && reloadsysrootmountunit="${reloadsysrootmountunit}:>/xor_readonly;"
            fi
        else
            dd if=/dev/null of=/overlay bs=1024 count=1 seek=$((overlay_size * 1024)) 2> /dev/null
            if [ -n "$setup" -a -n "$readonly_overlay" ]; then
                RO_OVERLAY_LOOPDEV=$(losetup -f --show /overlay)
                over=$RO_OVERLAY_LOOPDEV
            else
                OVERLAY_LOOPDEV=$(losetup -f --show /overlay)
                over=$OVERLAY_LOOPDEV
            fi
        fi
    fi

    # set up the snapshot
    if [ -z "$overlayfs" ]; then
        if [ -n "$readonly_overlay" ] && [ -n "$OVERLAY_LOOPDEV" ]; then
            echo 0 "$sz" snapshot "$BASE_LOOPDEV" "$OVERLAY_LOOPDEV" P 8 | dmsetup create --readonly live-ro
            base="/dev/mapper/live-ro"
        else
            base=$BASE_LOOPDEV
        fi
    fi

    if [ -n "$thin_snapshot" ]; then
        modprobe dm_thin_pool
        mkdir -m 0755 -p /run/initramfs/thin-overlay

        # In block units (512b)
        thin_data_sz=$((overlay_size * 1024 * 1024 / 512))
        thin_meta_sz=$((thin_data_sz / 10))

        # It is important to have the backing file on a tmpfs
        # this is needed to let the loopdevice support TRIM
        dd if=/dev/null of=/run/initramfs/thin-overlay/meta bs=1b count=1 seek=$((thin_meta_sz)) 2> /dev/null
        dd if=/dev/null of=/run/initramfs/thin-overlay/data bs=1b count=1 seek=$((thin_data_sz)) 2> /dev/null

        THIN_META_LOOPDEV=$(losetup --show -f /run/initramfs/thin-overlay/meta)
        THIN_DATA_LOOPDEV=$(losetup --show -f /run/initramfs/thin-overlay/data)

        echo 0 $thin_data_sz thin-pool "$THIN_META_LOOPDEV" "$THIN_DATA_LOOPDEV" 1024 1024 | dmsetup create live-overlay-pool
        dmsetup message /dev/mapper/live-overlay-pool 0 "create_thin 0"

        # Create a snapshot of the base image
        echo 0 "$sz" thin /dev/mapper/live-overlay-pool 0 "$base" | dmsetup create live-rw
    elif [ -z "$overlayfs" ]; then
        echo 0 "$sz" snapshot "$base" "$over" PO 8 | dmsetup create live-rw
    fi

    # Create a device for the ro base of overlayed file systems.
    if [ -z "$overlayfs" ]; then
        echo 0 "$sz" linear "$BASE_LOOPDEV" 0 | dmsetup create --readonly live-base
    fi
    ln -s "$BASE_LOOPDEV" /dev/live-base
}
# end do_live_overlay()

set -x

# we might have an embedded fs image on squashfs (compressed live)
if [ -e /run/initramfs/live/${live_dir}/${squash_image} ]; then
    SQUASHED="/run/initramfs/live/${live_dir}/${squash_image}"
fi
if [ -e "$SQUASHED" ]; then
    if [ -n "$live_ram" ]; then
        echo 'Copying live image to RAM...' > /dev/kmsg
        echo ' (this may take a minute)' > /dev/kmsg
        dd if=$SQUASHED of=/run/initramfs/squashed.img bs=512 2> /dev/null
        echo 'Done copying live image to RAM.' > /dev/kmsg
        SQUASHED="/run/initramfs/squashed.img"
    fi

    SQUASHED_LOOPDEV=$(losetup -f)
    losetup -r "$SQUASHED_LOOPDEV" $SQUASHED
    mkdir -m 0755 -p /run/initramfs/squashfs
    mount -n -t squashfs -o ro "$SQUASHED_LOOPDEV" /run/initramfs/squashfs

    if [ -d /run/initramfs/squashfs/LiveOS ]; then
        if [ -f /run/initramfs/squashfs/LiveOS/rootfs.img ]; then
            FSIMG="/run/initramfs/squashfs/LiveOS/rootfs.img"
        elif [ -f /run/initramfs/squashfs/LiveOS/ext3fs.img ]; then
            FSIMG="/run/initramfs/squashfs/LiveOS/ext3fs.img"
        fi
    elif [ -d /run/initramfs/squashfs/proc ]; then
        FSIMG=$SQUASHED
        if [ -z "$overlayfs" ] && [ -n "$DRACUT_SYSTEMD" ]; then
            reloadsysrootmountunit=":>/xor_overlayfs;"
        fi
        overlayfs="required"
    else
        die "Failed to find a root filesystem in $SQUASHED."
        exit 1
    fi
else
    # we might have an embedded fs image to use as rootfs (uncompressed live)
    if [ -e /run/initramfs/live/${live_dir}/rootfs.img ]; then
        FSIMG="/run/initramfs/live/${live_dir}/rootfs.img"
    elif [ -e /run/initramfs/live/${live_dir}/ext3fs.img ]; then
        FSIMG="/run/initramfs/live/${live_dir}/ext3fs.img"
    fi
    if [ -n "$live_ram" ]; then
        echo 'Copying live image to RAM...' > /dev/kmsg
        echo ' (this may take a minute or so)' > /dev/kmsg
        dd if=$FSIMG of=/run/initramfs/rootfs.img bs=512 2> /dev/null
        echo 'Done copying live image to RAM.' > /dev/kmsg
        FSIMG='/run/initramfs/rootfs.img'
    fi
fi

echo "---- dmsquash-live-root.sh ---- 13 ---- checking FSIMG=$FSIMG" > /dev/kmsg
sleep 3s

if [ -n "$FSIMG" ]; then

    echo "---- dmsquash-live-root.sh ---- 13.1 ---- FSIMG not empty." > /dev/kmsg
    sleep 3s

    if [ -n "$writable_fsimg" ]; then

        echo "---- dmsquash-live-root.sh ---- 13.1.1 ---- writable_fsimg." > /dev/kmsg
        sleep 2s

        # mount the provided filesystem read/write
        echo "Unpacking live filesystem (may take some time)" > /dev/kmsg
        mkdir -m 0755 -p /run/initramfs/fsimg/
        if [ -n "$SQUASHED" ]; then
            echo "---- dmsquash-live-root.sh ---- 13.1.1.1 ---- squashed." > /dev/kmsg
            sleep 2s
            cp -v $FSIMG /run/initramfs/fsimg/rootfs.img
        else
            echo "---- dmsquash-live-root.sh ---- 13.1.1.2 ---- not squashed." > /dev/kmsg
            echo "---- dmsquash-live-root.sh ---- 13.1.1.2.1 ---- cp $FSIMG /run/initramfs/fsimg/." > /dev/kmsg
            sleep 2s
            cp $FSIMG /run/initramfs/fsimg/
        fi
        FSIMG=/run/initramfs/fsimg/rootfs.img
    fi

    echo "---- dmsquash-live-root.sh ---- 13.2 ----." > /dev/kmsg
    sleep 3s

    opt=-r
    # For writable DM images...
    if [ -z "$SQUASHED" -a -n "$live_ram" -a -z "$overlayfs" ] \
        || [ -n "$writable_fsimg" ] \
        || [ "$overlay" = none -o "$overlay" = None -o "$overlay" = NONE ]; then

        echo "---- dmsquash-live-root.sh ---- 13.2.1 ----" > /dev/kmsg

        if [ -z "$readonly_overlay" ]; then
            opt=''
            setup=rw
        else
            setup=yes
        fi
    fi

    echo "---- dmsquash-live-root.sh ---- 13.3 ---- opt=$opt" > /dev/kmsg

    if [ "$FSIMG" = "$SQUASHED" ]; then
        echo "---- dmsquash-live-root.sh ---- 13.3.1 ----" > /dev/kmsg
        BASE_LOOPDEV=$SQUASHED_LOOPDEV
    else
        echo "---- dmsquash-live-root.sh ---- 13.3.2 ---- losetup -f --show $FSIMG" > /dev/kmsg
        # ls -la $FSIMG > /dev/kmsg
        # losetup -a > /dev/kmsg
        # losetup -f --show /run/initramfs/fsimg/rootfs.img
        # losetup -f --verbose --show "$opt" $FSIMG > /dev/kmsg 2>&1
        losetup -f --verbose --show $FSIMG > /dev/kmsg 2>&1
        # udevadm trigger --action=add > /dev/null 2>&1
        if [ -n "$opt" ]; then
            BASE_LOOPDEV=$(losetup -f --show "$opt" $FSIMG)
        else
            BASE_LOOPDEV=$(losetup -f --show $FSIMG)
        fi
        echo "---- dmsquash-live-root.sh ---- 13.3.2.1 ---- BASE_LOOPDEV=$BASE_LOOPDEV" > /dev/kmsg
        BASE_LOOPDEV
        sleep 1s
        echo "---- dmsquash-live-root.sh ---- 13.3.2.2 ---- losetup -a" > /dev/kmsg
        losetup -a > /dev/kmsg
        sleep 1s
        echo "---- dmsquash-live-root.sh ---- 13.3.2.3 ---- losetup -a" > /dev/kmsg
        lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,UUID,PARTLABEL,PARTUUID
        sleep 1s
        sz=$(blockdev --getsz "$BASE_LOOPDEV")
        echo "---- dmsquash-live-root.sh ---- 13.3.2.4 ---- sz=$sz" > /dev/kmsg
        # hack
        mkdir -p /mnt/hack
        mount $BASE_LOOPDEV /mnt/hack
        ls -la /mnt/hack > /dev/kmsg
        rm /mnt/hack/etc/fstab
        umount /mnt/hack
        rm /mnt/hack
    fi

    echo "---- dmsquash-live-root.sh ---- 13.4 ----" > /dev/kmsg

    if [ "$setup" = rw ]; then
        echo "---- dmsquash-live-root.sh ---- 13.4.1 ----" > /dev/kmsg
        echo 0 "$sz" linear "$BASE_LOOPDEV" 0 | dmsetup create live-rw
    else
        echo "---- dmsquash-live-root.sh ---- 13.4.2 ----" > /dev/kmsg
        # Add a DM snapshot or OverlayFS for writes.
        do_live_overlay
    fi
fi

echo "---- dmsquash-live-root.sh ---- 14 ----" > /dev/kmsg
sleep 1s

if [ -n "$reloadsysrootmountunit" ]; then
    eval "$reloadsysrootmountunit"
    systemctl daemon-reload
fi

echo "---- dmsquash-live-root.sh ---- 15 ----" > /dev/kmsg
sleep 1s

ROOTFLAGS="$(getarg rootflags)"

if [ -n "$overlayfs" ]; then
    mkdir -m 0755 -p /run/rootfsbase
    if [ -n "$reset_overlay" ] && [ -h /run/overlayfs ]; then
        ovlfs=$(readlink /run/overlayfs)
        info "Resetting the OverlayFS overlay directory."
        rm -r -- "${ovlfs:?}"/* "${ovlfs:?}"/.* > /dev/null 2>&1
    fi
    if [ -n "$readonly_overlay" ] && [ -h /run/overlayfs-r ]; then
        ovlfs=lowerdir=/run/overlayfs-r:/run/rootfsbase
    else
        ovlfs=lowerdir=/run/rootfsbase
    fi
    mount -r $FSIMG /run/rootfsbase
    if [ -z "$DRACUT_SYSTEMD" ]; then
        printf 'mount -t overlay LiveOS_rootfs -o%s,%s %s\n' "$ROOTFLAGS" \
            "$ovlfs",upperdir=/run/overlayfs,workdir=/run/ovlwork \
            "$NEWROOT" > "$hookdir"/mount/01-$$-live.sh
    fi
else
    # if [ -z "$DRACUT_SYSTEMD" ]; then
        [ -n "$ROOTFLAGS" ] && ROOTFLAGS="-o $ROOTFLAGS"
        printf 'mount %s /dev/mapper/live-rw %s\n' "$ROOTFLAGS" "$NEWROOT" > "$hookdir"/mount/01-$$-live.sh
    # fi
fi

echo "---- dmsquash-live-root.sh ---- 16 ----" > /dev/kmsg
sleep 1s

[ -e "$SQUASHED" ] && umount -l /run/initramfs/squashfs

echo "---- dmsquash-live-root.sh ---- 17 ----" > /dev/kmsg
sleep 20s

ln -s null /dev/root

echo "---- dmsquash-live-root.sh ---- 18 ----" > /dev/kmsg
sleep 20s

need_shutdown

exit 0
