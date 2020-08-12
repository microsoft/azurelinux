#!/bin/sh
#
# Kdump common variables and functions
#

DEFAULT_PATH="/var/crash/"
FENCE_KDUMP_CONFIG_FILE="/etc/sysconfig/fence_kdump"
FENCE_KDUMP_SEND="/usr/libexec/fence_kdump_send"
FADUMP_ENABLED_SYS_NODE="/sys/kernel/fadump_enabled"

is_fadump_capable()
{
    # Check if firmware-assisted dump is enabled
    # if no, fallback to kdump check
    if [ -f $FADUMP_ENABLED_SYS_NODE ]; then
        rc=`cat $FADUMP_ENABLED_SYS_NODE`
        [ $rc -eq 1 ] && return 0
    fi
    return 1
}

perror_exit() {
    echo $@ >&2
    exit 1
}

perror() {
    echo $@ >&2
}

is_fs_type_nfs()
{
    [ "$1" = "nfs" ] || [ "$1" = "nfs4" ]
}

is_ssh_dump_target()
{
    grep -q "^ssh[[:blank:]].*@" /etc/kdump.conf
}

is_nfs_dump_target()
{
    if grep -q "^nfs" /etc/kdump.conf; then
        return 0;
    fi

    if is_fs_type_nfs $(get_dracut_args_fstype "$(grep "^dracut_args .*\-\-mount" /etc/kdump.conf)"); then
        return 0
    fi

    local _save_path=$(get_save_path)
    local _target=$(get_target_from_path $_save_path)
    local _fstype=$(get_fs_type_from_target $_target)

    if is_fs_type_nfs $_fstype; then
        return 0
    fi

    return 1
}

is_raw_dump_target()
{
    grep -q "^raw" /etc/kdump.conf
}

is_fs_dump_target()
{
    egrep -q "^ext[234]|^xfs|^btrfs|^minix" /etc/kdump.conf
}

strip_comments()
{
    echo $@ | sed -e 's/\(.*\)#.*/\1/'
}

# Read from kdump config file stripping all comments
read_strip_comments()
{
    # strip heading spaces, and print any content starting with
    # neither space or #, and strip everything after #
    sed -n -e "s/^\s*\([^# \t][^#]\+\).*/\1/gp" $1
}

# Check if fence kdump is configured in Pacemaker cluster
is_pcs_fence_kdump()
{
    # no pcs or fence_kdump_send executables installed?
    type -P pcs > /dev/null || return 1
    [ -x $FENCE_KDUMP_SEND ] || return 1

    # fence kdump not configured?
    (pcs cluster cib | grep 'type="fence_kdump"') &> /dev/null || return 1
}

# Check if fence_kdump is configured using kdump options
is_generic_fence_kdump()
{
    [ -x $FENCE_KDUMP_SEND ] || return 1

    grep -q "^fence_kdump_nodes" /etc/kdump.conf
}

to_dev_name() {
    local dev="${1//\"/}"

    case "$dev" in
    UUID=*)
        dev=`blkid -U "${dev#UUID=}"`
        ;;
    LABEL=*)
        dev=`blkid -L "${dev#LABEL=}"`
        ;;
    esac
    echo $dev
}

is_user_configured_dump_target()
{
    grep -E -q "^ext[234]|^xfs|^btrfs|^minix|^raw|^nfs|^ssh" /etc/kdump.conf || is_mount_in_dracut_args;
}

get_user_configured_dump_disk()
{
    local _target

    _target=$(egrep "^ext[234]|^xfs|^btrfs|^minix|^raw" /etc/kdump.conf 2>/dev/null |awk '{print $2}')
    [ -n "$_target" ] && echo $_target && return

    _target=$(get_dracut_args_target "$(grep "^dracut_args .*\-\-mount" /etc/kdump.conf)")
    [ -b "$_target" ] && echo $_target
}

get_root_fs_device()
{
    findmnt -k -f -n -o SOURCE /
}

get_save_path()
{
    local _save_path=$(awk '$1 == "path" {print $2}' /etc/kdump.conf)
    [ -z "$_save_path" ] && _save_path=$DEFAULT_PATH

    # strip the duplicated "/"
    echo $_save_path | tr -s /
}

get_block_dump_target()
{
    local _target _path

    if is_ssh_dump_target || is_nfs_dump_target; then
        return
    fi

    _target=$(get_user_configured_dump_disk)
    [ -n "$_target" ] && echo $(to_dev_name $_target) && return

    # Get block device name from local save path
    _path=$(get_save_path)
    _target=$(get_target_from_path $_path)
    [ -b "$_target" ] && echo $(to_dev_name $_target)
}

is_dump_to_rootfs()
{
    grep -E "^(failure_action|default)[[:space:]]dump_to_rootfs" /etc/kdump.conf >/dev/null
}

get_failure_action_target()
{
    local _target

    if is_dump_to_rootfs; then
        # Get rootfs device name
        _target=$(get_root_fs_device)
        [ -b "$_target" ] && echo $(to_dev_name $_target) && return
        # Then, must be nfs root
        echo "nfs"
    fi
}

# Get kdump targets(including root in case of dump_to_rootfs).
get_kdump_targets()
{
    local _target _root
    local kdump_targets

    _target=$(get_block_dump_target)
    if [ -n "$_target" ]; then
        kdump_targets=$_target
    elif is_ssh_dump_target; then
        kdump_targets="ssh"
    else
        kdump_targets="nfs"
    fi

    # Add the root device if dump_to_rootfs is specified.
    _root=$(get_failure_action_target)
    if [ -n "$_root" -a "$kdump_targets" != "$_root" ]; then
        kdump_targets="$kdump_targets $_root"
    fi

    echo "$kdump_targets"
}

# Return the bind mount source path, return the path itself if it's not bind mounted
# Eg. if /path/to/src is bind mounted to /mnt/bind, then:
# /mnt/bind -> /path/to/src, /mnt/bind/dump -> /path/to/src/dump
#
# findmnt uses the option "-v, --nofsroot" to exclusive the [/dir]
# in the SOURCE column for bind-mounts, then if $_mntpoint equals to
# $_mntpoint_nofsroot, the mountpoint is not bind mounted directory.
#
# Below is just an example for mount info
# /dev/mapper/atomicos-root[/ostree/deploy/rhel-atomic-host/var], if the
# directory is bind mounted. The former part represents the device path, rest
# part is the bind mounted directory which quotes by bracket "[]".
get_bind_mount_source()
{
    local _path=$1
    # In case it's a sub path in a mount point, get the mount point first
    local _mnt_top=$(df $_path | tail -1 | awk '{print $NF}')
    local _mntpoint=$(findmnt $_mnt_top | tail -n 1 | awk '{print $2}')
    local _mntpoint_nofsroot=$(findmnt -v $_mnt_top | tail -n 1 | awk '{print $2}')

    if [[ "$_mntpoint" = $_mntpoint_nofsroot ]]; then
        echo $_path && return
    fi

    _mntpoint=${_mntpoint#*$_mntpoint_nofsroot}
    _mntpoint=${_mntpoint#[}
    _mntpoint=${_mntpoint%]}
    _path=${_path#$_mnt_top}

    echo $_mntpoint$_path
}

# Return the current underlaying device of a path, ignore bind mounts
get_target_from_path()
{
    local _target

    _target=$(df $1 2>/dev/null | tail -1 |  awk '{print $1}')
    [[ "$_target" == "/dev/root" ]] && [[ ! -e /dev/root ]] && _target=$(get_root_fs_device)
    echo $_target
}

is_mounted()
{
    findmnt -k -n $1 &>/dev/null
}

get_mount_info()
{
    local _info_type=$1 _src_type=$2 _src=$3; shift 3
    local _info=$(findmnt --real -k -n -r -o $_info_type --$_src_type $_src $@)

    [ -z "$_info" ] && [ -e "/etc/fstab" ] && _info=$(findmnt --real -s -n -r -o $_info_type --$_src_type $_src $@)

    echo $_info
}

get_fs_type_from_target()
{
    get_mount_info FSTYPE source $1 -f
}

get_mntopt_from_target()
{
    get_mount_info OPTIONS source $1 -f
}
# Find the general mount point of a dump target, not the bind mount point
get_mntpoint_from_target()
{
    # Expcilitly specify --source to findmnt could ensure non-bind mount is returned
    get_mount_info TARGET source $1 -f
}

# Get the path where the target will be mounted in kdump kernel
# $1: kdump target device
get_kdump_mntpoint_from_target()
{
    local _mntpoint=$(get_mntpoint_from_target $1)

    # mount under /sysroot if dump to root disk or mount under
    # mount under /kdumproot if dump target is not mounted in first kernel
    # mount under /kdumproot/$_mntpoint in other cases in 2nd kernel.
    # systemd will be in charge to umount it.
    if [ -z "$_mntpoint" ];then
        _mntpoint="/kdumproot"
    else
        if [ "$_mntpoint" = "/" ];then
            _mntpoint="/sysroot"
        else
            _mntpoint="/kdumproot/$_mntpoint"
        fi
    fi

    # strip duplicated "/"
    echo $_mntpoint | tr -s "/"
}

# get_option_value <option_name>
# retrieves value of option defined in kdump.conf
get_option_value() {
    strip_comments `grep "^$1[[:space:]]\+" /etc/kdump.conf | tail -1 | cut -d\  -f2-`
}

kdump_get_persistent_dev() {
    local dev="${1//\"/}"

    case "$dev" in
    UUID=*)
        dev=`blkid -U "${dev#UUID=}"`
        ;;
    LABEL=*)
        dev=`blkid -L "${dev#LABEL=}"`
        ;;
    esac
    echo $(get_persistent_dev "$dev")
}

is_atomic()
{
    grep -q "ostree" /proc/cmdline
}

is_ipv6_address()
{
    echo $1 | grep -q ":"
}

# get ip address or hostname from nfs/ssh config value
get_remote_host()
{
    local _config_val=$1

    # ipv6 address in kdump.conf is around with "[]",
    # factor out the ipv6 address
    _config_val=${_config_val#*@}
    _config_val=${_config_val%:/*}
    _config_val=${_config_val#[}
    _config_val=${_config_val%]}
    echo $_config_val
}

is_hostname()
{
    local _hostname=`echo $1 | grep ":"`

    if [ -n "$_hostname" ]; then
        return 1
    fi
    echo $1 | grep -q "[a-zA-Z]"
}

# Copied from "/etc/sysconfig/network-scripts/network-functions"
get_hwaddr()
{
    if [ -f "/sys/class/net/${1}/address" ]; then
        awk '{ print toupper($0) }' < /sys/class/net/${1}/address
    elif [ -d "/sys/class/net/${1}" ]; then
       LC_ALL= LANG= ip -o link show ${1} 2>/dev/null | \
            awk '{ print toupper(gensub(/.*link\/[^ ]* ([[:alnum:]:]*).*/,
                                        "\\1", 1)); }'
    fi
}

get_ifcfg_by_device()
{
    grep -E -i -l "^[[:space:]]*DEVICE=\"*${1}\"*[[:space:]]*$" \
         /etc/sysconfig/network-scripts/ifcfg-* 2>/dev/null | head -1
}

get_ifcfg_by_hwaddr()
{
    grep -E -i -l "^[[:space:]]*HWADDR=\"*${1}\"*[[:space:]]*$" \
         /etc/sysconfig/network-scripts/ifcfg-* 2>/dev/null | head -1
}

get_ifcfg_by_uuid()
{
    grep -E -i -l "^[[:space:]]*UUID=\"*${1}\"*[[:space:]]*$" \
         /etc/sysconfig/network-scripts/ifcfg-* 2>/dev/null | head -1
}

get_ifcfg_by_name()
{
    grep -E -i -l "^[[:space:]]*NAME=\"*${1}\"*[[:space:]]*$" \
         /etc/sysconfig/network-scripts/ifcfg-* 2>/dev/null | head -1
}

is_nm_running()
{
    [ "$(LANG=C nmcli -t --fields running general status 2>/dev/null)" = "running" ]
}

is_nm_handling()
{
    LANG=C nmcli -t --fields device,state  dev status 2>/dev/null \
          | grep -q "^\(${1}:connected\)\|\(${1}:connecting.*\)$"
}

# $1: netdev name
get_ifcfg_nmcli()
{
    local nm_uuid nm_name
    local ifcfg_file

    # Get the active nmcli config name of $1
    if is_nm_running && is_nm_handling "${1}" ; then
        # The configuration "uuid" and "name" generated by nm is wrote to
        # the ifcfg file as "UUID=<nm_uuid>" and "NAME=<nm_name>".
        nm_uuid=$(LANG=C nmcli -t --fields uuid,device c show --active 2>/dev/null \
                  | grep "${1}" | head -1 | cut -d':' -f1)
        nm_name=$(LANG=C nmcli -t --fields name,device c show --active 2>/dev/null \
                  | grep "${1}" | head -1 | cut -d':' -f1)
        ifcfg_file=$(get_ifcfg_by_uuid "${nm_uuid}")
        [ -z "${ifcfg_file}" ] && ifcfg_file=$(get_ifcfg_by_name "${nm_name}")
    fi

    echo -n "${ifcfg_file}"
}

# $1: netdev name
get_ifcfg_legacy()
{
    local ifcfg_file

    ifcfg_file="/etc/sysconfig/network-scripts/ifcfg-${1}"
    [ -f "${ifcfg_file}" ] && echo -n "${ifcfg_file}" && return

    ifcfg_file=$(get_ifcfg_by_name "${1}")
    [ -f "${ifcfg_file}" ] && echo -n "${ifcfg_file}" && return

    local hwaddr=$(get_hwaddr "${1}")
    if [ -n "$hwaddr" ]; then
        ifcfg_file=$(get_ifcfg_by_hwaddr "${hwaddr}")
        [ -f "${ifcfg_file}" ] && echo -n "${ifcfg_file}" && return
    fi

    ifcfg_file=$(get_ifcfg_by_device "${1}")

    echo -n "${ifcfg_file}"
}

# $1: netdev name
# Return the ifcfg file whole name(including the path) of $1 if any.
get_ifcfg_filename() {
    local ifcfg_file

    ifcfg_file=$(get_ifcfg_nmcli "${1}")
    if [ -z "${ifcfg_file}" ]; then
        ifcfg_file=$(get_ifcfg_legacy "${1}")
    fi

    echo -n "${ifcfg_file}"
}

# returns 0 when omission of watchdog module is desired in dracut_args
# returns 1 otherwise
is_wdt_mod_omitted() {
	local dracut_args
	local ret=1

	dracut_args=$(grep  "^dracut_args" /etc/kdump.conf)
	[[ -z $dracut_args ]] && return $ret

	eval set -- $dracut_args
	while :; do
		[[ -z $1 ]] && break
		case $1 in
			-o|--omit)
				echo $2 | grep -qw "watchdog"
				[[ $? == 0 ]] && ret=0
				break
		esac
		shift
	done

	return $ret
}

# If "dracut_args" contains "--mount" information, use it
# directly without any check(users are expected to ensure
# its correctness).
is_mount_in_dracut_args()
{
    grep -q "^dracut_args .*\-\-mount" /etc/kdump.conf
}

# If $1 contains dracut_args "--mount", return <filesystem type>
get_dracut_args_fstype()
{
    echo $1 | grep "\-\-mount" | sed "s/.*--mount .\(.*\)/\1/" | cut -d' ' -f3
}

# If $1 contains dracut_args "--mount", return <device>
get_dracut_args_target()
{
    echo $1 | grep "\-\-mount" | sed "s/.*--mount .\(.*\)/\1/" | cut -d' ' -f1
}

check_crash_mem_reserved()
{
    local mem_reserved

    mem_reserved=$(cat /sys/kernel/kexec_crash_size)
    if [ $mem_reserved -eq 0 ]; then
        echo "No memory reserved for crash kernel"
        return 1
    fi

    return 0
}

check_kdump_feasibility()
{
    if [ ! -e /sys/kernel/kexec_crash_loaded ]; then
        echo "Kdump is not supported on this kernel"
        return 1
    fi
    check_crash_mem_reserved
    return $?
}

check_current_kdump_status()
{
    if [ ! -f /sys/kernel/kexec_crash_loaded ];then
        echo "Perhaps CONFIG_CRASH_DUMP is not enabled in kernel"
        return 1
    fi

    rc=`cat /sys/kernel/kexec_crash_loaded`
    if [ $rc == 1 ]; then
        return 0
    else
        return 1
    fi
}

# remove_cmdline_param <kernel cmdline> <param1> [<param2>] ... [<paramN>]
# Remove a list of kernel parameters from a given kernel cmdline and print the result.
# For each "arg" in the removing params list, "arg" and "arg=xxx" will be removed if exists.
remove_cmdline_param()
{
    local cmdline=$1
    shift

    for arg in $@; do
        cmdline=`echo $cmdline | \
                 sed -e "s/\b$arg=[^ ]*//g" \
                 -e "s/^$arg\b//g" \
                 -e "s/[[:space:]]$arg\b//g" \
                 -e "s/\s\+/ /g"`
    done
    echo $cmdline
}

#
# This function returns the "apicid" of the boot
# cpu (cpu 0) if present.
#
get_bootcpu_apicid()
{
    awk '                                                       \
        BEGIN { CPU = "-1"; }                                   \
        $1=="processor" && $2==":"      { CPU = $NF; }          \
        CPU=="0" && /^apicid/           { print $NF; }          \
        '                                                       \
        /proc/cpuinfo
}

#
# append_cmdline <kernel cmdline> <parameter name> <parameter value>
# This function appends argument "$2=$3" to string ($1) if not already present.
#
append_cmdline()
{
    local cmdline=$1
    local newstr=${cmdline/$2/""}

    # unchanged str implies argument wasn't there
    if [ "$cmdline" == "$newstr" ]; then
        cmdline="${cmdline} ${2}=${3}"
    fi

    echo $cmdline
}

# This function check iomem and determines if we have more than
# 4GB of ram available. Returns 1 if we do, 0 if we dont
need_64bit_headers()
{
    return `tail -n 1 /proc/iomem | awk '{ split ($1, r, "-"); \
    print (strtonum("0x" r[2]) > strtonum("0xffffffff")); }'`
}

# Check if secure boot is being enforced.
#
# Per Peter Jones, we need check efivar SecureBoot-$(the UUID) and
# SetupMode-$(the UUID), they are both 5 bytes binary data. The first four
# bytes are the attributes associated with the variable and can safely be
# ignored, the last bytes are one-byte true-or-false variables. If SecureBoot
# is 1 and SetupMode is 0, then secure boot is being enforced.
#
# Assume efivars is mounted at /sys/firmware/efi/efivars.
is_secure_boot_enforced()
{
    local secure_boot_file setup_mode_file
    local secure_boot_byte setup_mode_byte

    secure_boot_file=$(find /sys/firmware/efi/efivars -name SecureBoot-* 2>/dev/null)
    setup_mode_file=$(find /sys/firmware/efi/efivars -name SetupMode-* 2>/dev/null)

    if [ -f "$secure_boot_file" ] && [ -f "$setup_mode_file" ]; then
        secure_boot_byte=$(hexdump -v -e '/1 "%d\ "' $secure_boot_file|cut -d' ' -f 5)
        setup_mode_byte=$(hexdump -v -e '/1 "%d\ "' $setup_mode_file|cut -d' ' -f 5)

        if [ "$secure_boot_byte" = "1" ] && [ "$setup_mode_byte" = "0" ]; then
            return 0
        fi
    fi

    return 1
}

#
# prepare_kexec_args <kexec args>
# This function prepares kexec argument.
#
prepare_kexec_args()
{
    local kexec_args=$1
    local found_elf_args

    ARCH=`uname -m`
    if [ "$ARCH" == "i686" -o "$ARCH" == "i386" ]
    then
        need_64bit_headers
        if [ $? == 1 ]
        then
            found_elf_args=`echo $kexec_args | grep elf32-core-headers`
            if [ -n "$found_elf_args" ]
            then
                echo -n "Warning: elf32-core-headers overrides correct elf64 setting"
                echo
            else
                kexec_args="$kexec_args --elf64-core-headers"
            fi
        else
            found_elf_args=`echo $kexec_args | grep elf64-core-headers`
            if [ -z "$found_elf_args" ]
            then
                kexec_args="$kexec_args --elf32-core-headers"
            fi
        fi
    fi
    echo $kexec_args
}

check_boot_dir()
{
    local kdump_bootdir=$1
    #If user specify a boot dir for kdump kernel, let's use it. Otherwise
    #check whether it's a atomic host. If yes parse the subdirectory under
    #/boot; If not just find it under /boot.
    if [ -n "$kdump_bootdir" ]; then
        echo "$kdump_bootdir"
        return
    fi

    if ! is_atomic || [ "$(uname -m)" = "s390x" ]; then
        kdump_bootdir="/boot"
    else
        eval $(cat /proc/cmdline| grep "BOOT_IMAGE" | cut -d' ' -f1)
        kdump_bootdir="/boot"$(dirname ${BOOT_IMAGE#*)})
    fi
    echo $kdump_bootdir
}

#
# prepare_cmdline <commandline> <commandline remove> <commandline append>
# This function performs a series of edits on the command line.
# Store the final result in global $KDUMP_COMMANDLINE.
prepare_cmdline()
{
    local cmdline id

    if [ -z "$1" ]; then
        cmdline=$(cat /proc/cmdline)
    else
        cmdline="$1"
    fi

    # These params should always be removed
    cmdline=$(remove_cmdline_param "$cmdline" crashkernel panic_on_warn)
    # These params can be removed configurably
    cmdline=$(remove_cmdline_param "$cmdline" "$2")

    # Always remove "root=X", as we now explicitly generate all kinds
    # of dump target mount information including root fs.
    #
    # We do this before KDUMP_COMMANDLINE_APPEND, if one really cares
    # about it(e.g. for debug purpose), then can pass "root=X" using
    # KDUMP_COMMANDLINE_APPEND.
    cmdline=$(remove_cmdline_param "$cmdline" root)

    # With the help of "--hostonly-cmdline", we can avoid some interitage.
    cmdline=$(remove_cmdline_param "$cmdline" rd.lvm.lv rd.luks.uuid rd.dm.uuid rd.md.uuid fcoe)

    # Remove netroot, rd.iscsi.initiator and iscsi_initiator since
    # we get duplicate entries for the same in case iscsi code adds
    # it as well.
    cmdline=$(remove_cmdline_param "$cmdline" netroot rd.iscsi.initiator iscsi_initiator)

    cmdline="${cmdline} $3"

    id=$(get_bootcpu_apicid)
    if [ ! -z ${id} ] ; then
        cmdline=$(append_cmdline "${cmdline}" disable_cpu_apicid ${id})
    fi
    echo ${cmdline}
}
