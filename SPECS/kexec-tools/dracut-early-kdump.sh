#! /bin/sh

KEXEC=/sbin/kexec
standard_kexec_args="-p"

EARLY_KDUMP_INITRD=""
EARLY_KDUMP_KERNEL=""
EARLY_KDUMP_CMDLINE=""
EARLY_KDUMP_KERNELVER=""
EARLY_KEXEC_ARGS=""

. /etc/sysconfig/kdump
. /lib/dracut-lib.sh
. /lib/kdump-lib.sh

prepare_parameters()
{
    EARLY_KDUMP_CMDLINE=$(prepare_cmdline "${KDUMP_COMMANDLINE}" "${KDUMP_COMMANDLINE_REMOVE}" "${KDUMP_COMMANDLINE_APPEND}")
    KDUMP_BOOTDIR=$(check_boot_dir "${KDUMP_BOOTDIR}")

    EARLY_KDUMP_KERNEL="${KDUMP_BOOTDIR}/${KDUMP_IMG}-earlykdump${KDUMP_IMG_EXT}"
    EARLY_KDUMP_INITRD="${KDUMP_BOOTDIR}/initramfs-earlykdump.img"
}

early_kdump_load()
{
    check_kdump_feasibility
    if [ $? -ne 0 ]; then
        return 1
    fi

    if is_fadump_capable; then
        echo "WARNING: early kdump doesn't support fadump."
        return 1
    fi

    check_current_kdump_status
    if [ $? == 0 ]; then
        return 1
    fi

    prepare_parameters

    EARLY_KEXEC_ARGS=$(prepare_kexec_args "${KEXEC_ARGS}")

    if is_secure_boot_enforced; then
        echo "Secure Boot is enabled. Using kexec file based syscall."
        EARLY_KEXEC_ARGS="$EARLY_KEXEC_ARGS -s"
    fi

    $KEXEC ${EARLY_KEXEC_ARGS} $standard_kexec_args \
        --command-line="$EARLY_KDUMP_CMDLINE" \
        --initrd=$EARLY_KDUMP_INITRD $EARLY_KDUMP_KERNEL
    if [ $? == 0 ]; then
        echo "kexec: loaded early-kdump kernel"
        return 0
    else
        echo "kexec: failed to load early-kdump kernel"
        return 1
    fi
}

set_early_kdump()
{
    if getargbool 0 rd.earlykdump; then
        echo "early-kdump is enabled."
        early_kdump_load
    else
        echo "early-kdump is disabled."
    fi

    return 0
}

set_early_kdump
