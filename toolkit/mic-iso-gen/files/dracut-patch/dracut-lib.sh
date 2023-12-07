#!/bin/sh

echo "george - sleeping for 3 seconds - dracut-lib-sh."
sleep 3s

type wait_for_dev > /dev/null 2>&1 || . /lib/dracut-dev-lib.sh

export DRACUT_SYSTEMD
export NEWROOT
if [ -n "$NEWROOT" ]; then
    [ -d "$NEWROOT" ] || mkdir -p -m 0755 "$NEWROOT"
fi

# shellcheck disable=SC2153
if [ -z "$PREFIX" ]; then
    if ! [ -d /run/initramfs ]; then
        mkdir -p -m 0755 /run/initramfs/log
        ln -sfn /run/initramfs/log /var/log
    fi

    [ -d /run/lock ] || mkdir -p -m 0755 /run/lock
    [ -d /run/log ] || mkdir -p -m 0755 /run/log
fi

debug_off() {
    set +x
}

debug_on() {
    [ "$RD_DEBUG" = "yes" ] && set -x
}

# returns OK if $1 contains literal string $2 (and isn't empty)
strstr() {
    [ "${1##*"$2"*}" != "$1" ]
}

# returns OK if $1 matches (completely) glob pattern $2
# An empty $1 will not be considered matched, even if $2 is * which technically
# matches; as it would match anything, it's not an interesting case.
strglob() {
    [ -n "$1" -a -z "${1##$2}" ]
}

# returns OK if $1 contains (anywhere) a match of glob pattern $2
# An empty $1 will not be considered matched, even if $2 is * which technically
# matches; as it would match anything, it's not an interesting case.
strglobin() {
    [ -n "$1" -a -z "${1##*$2*}" ]
}

# returns OK if $1 contains literal string $2 at the beginning, and isn't empty
str_starts() {
    [ "${1#"$2"*}" != "$1" ]
}

# returns OK if $1 contains literal string $2 at the end, and isn't empty
str_ends() {
    [ "${1%*"$2"}" != "$1" ]
}

trim() {
    local var="$*"
    var="${var#"${var%%[![:space:]]*}"}" # remove leading whitespace characters
    var="${var%"${var##*[![:space:]]}"}" # remove trailing whitespace characters
    printf "%s" "$var"
}

if [ -z "$DRACUT_SYSTEMD" ]; then

    warn() {
        check_quiet
        echo "<28>dracut Warning: $*" > /dev/kmsg
        echo "dracut Warning: $*" >&2
    }

    info() {
        check_quiet
        echo "<30>dracut: $*" > /dev/kmsg
        if [ "$DRACUT_QUIET" != "yes" ]; then
            echo "dracut: $*" >&2
        fi
    }

else

    warn() {
        echo "Warning: $*" >&2
    }

    info() {
        echo "$*"
    }

fi

vwarn() {
    while read -r line || [ -n "$line" ]; do
        warn "$line"
    done
}

vinfo() {
    while read -r line || [ -n "$line" ]; do
        info "$line"
    done
}

# replaces all occurrences of 'search' in 'str' with 'replacement'
#
# str_replace str search replacement
#
# example:
# str_replace '  one two  three  ' ' ' '_'
str_replace() {
    local in="$1"
    local s="$2"
    local r="$3"
    local out=''

    while strstr "${in}" "$s"; do
        chop="${in%%"$s"*}"
        out="${out}${chop}$r"
        in="${in#*"$s"}"
    done
    echo "${out}${in}"
}

killall_proc_mountpoint() {
    local _pid
    local _killed=0
    for _pid in /proc/*; do
        _pid=${_pid##/proc/}
        case $_pid in
            *[!0-9]*) continue ;;
        esac
        [ -e "/proc/$_pid/exe" ] || continue
        [ -e "/proc/$_pid/root" ] || continue
        if strstr "$(ls -l -- "/proc/$_pid" "/proc/$_pid/fd" 2> /dev/null)" "$1"; then
            kill -9 "$_pid"
            _killed=1
        fi
    done
    return $_killed
}

getcmdline() {
    local _line
    local _i
    local CMDLINE_ETC_D
    local CMDLINE_ETC
    local CMDLINE_PROC
    unset _line

    if [ -e /etc/cmdline ]; then
        while read -r _line || [ -n "$_line" ]; do
            CMDLINE_ETC="$CMDLINE_ETC $_line"
        done < /etc/cmdline
    fi
    for _i in /etc/cmdline.d/*.conf; do
        [ -e "$_i" ] || continue
        while read -r _line || [ -n "$_line" ]; do
            CMDLINE_ETC_D="$CMDLINE_ETC_D $_line"
        done < "$_i"
    done
    if [ -e /proc/cmdline ]; then
        while read -r _line || [ -n "$_line" ]; do
            CMDLINE_PROC="$CMDLINE_PROC $_line"
        done < /proc/cmdline
    fi
    CMDLINE="$CMDLINE_ETC_D $CMDLINE_ETC $CMDLINE_PROC"
    printf "%s" "$CMDLINE"
}

getarg() {
    debug_off
    local _deprecated _newoption
    CMDLINE=$(getcmdline)
    export CMDLINE
    while [ $# -gt 0 ]; do
        case $1 in
            -d)
                _deprecated=1
                shift
                ;;
            -y)
                if dracut-getarg "$2" > /dev/null; then
                    if [ "$_deprecated" = "1" ]; then
                        if [ -n "$_newoption" ]; then
                            warn "Kernel command line option '$2' is deprecated, use '$_newoption' instead."
                        else
                            warn "Option '$2' is deprecated."
                        fi
                    fi
                    echo 1
                    debug_on
                    return 0
                fi
                _deprecated=0
                shift 2
                ;;
            -n)
                if dracut-getarg "$2" > /dev/null; then
                    echo 0
                    if [ "$_deprecated" = "1" ]; then
                        if [ -n "$_newoption" ]; then
                            warn "Kernel command line option '$2' is deprecated, use '$_newoption=0' instead."
                        else
                            warn "Option '$2' is deprecated."
                        fi
                    fi
                    debug_on
                    return 1
                fi
                _deprecated=0
                shift 2
                ;;
            *)
                if [ -z "$_newoption" ]; then
                    _newoption="$1"
                fi
                if dracut-getarg "$1"; then
                    if [ "$_deprecated" = "1" ]; then
                        if [ -n "$_newoption" ]; then
                            warn "Kernel command line option '$1' is deprecated, use '$_newoption' instead."
                        else
                            warn "Option '$1' is deprecated."
                        fi
                    fi
                    debug_on
                    return 0
                fi
                _deprecated=0
                shift
                ;;
        esac
    done
    debug_on
    return 1
}

# getargbool <defaultval> <args...>
# False if "getarg <args...>" returns "0", "no", or "off".
# True if getarg returns any other non-empty string.
# If not found, assumes <defaultval> - usually 0 for false, 1 for true.
# example: getargbool 0 rd.info
#   true: rd.info, rd.info=1, rd.info=xxx
#   false: rd.info=0, rd.info=off, rd.info not present (default val is 0)
getargbool() {
    local _b
    unset _b
    local _default
    _default="$1"
    shift
    _b=$(getarg "$@") || _b=${_b:-"$_default"}
    if [ -n "$_b" ]; then
        [ "$_b" = "0" ] && return 1
        [ "$_b" = "no" ] && return 1
        [ "$_b" = "off" ] && return 1
    fi
    return 0
}

isdigit() {
    case "$1" in
        *[!0-9]* | "") return 1 ;;
    esac

    return 0
}

# getargnum <defaultval> <minval> <maxval> <arg>
# Will echo the arg if it's in range [minval - maxval].
# If it's not set or it's not valid, will set it <defaultval>.
# Note all values are required to be >= 0 here.
# <defaultval> should be with [minval -maxval].
getargnum() {
    local _b
    unset _b
    local _default _min _max
    _default="$1"
    shift
    _min="$1"
    shift
    _max="$1"
    shift
    _b=$(getarg "$1") || _b=${_b:-"$_default"}
    if [ -n "$_b" ]; then
        isdigit "$_b" && _b=$((_b)) \
            && [ $_b -ge "$_min" ] && [ $_b -le "$_max" ] && echo $_b && return
    fi
    echo "$_default"
}

getargs() {
    debug_off
    CMDLINE=$(getcmdline)
    export CMDLINE
    local _val _i _gfound _deprecated
    unset _val
    unset _gfound
    _newoption="$1"
    for _i in "$@"; do
        if [ "$_i" = "-d" ]; then
            _deprecated=1
            continue
        fi

        if _val="$(dracut-getargs "$_i")"; then
            if [ "$_deprecated" = "1" ]; then
                if [ -n "$_newoption" ]; then
                    warn "Option '$_i' is deprecated, use '$_newoption' instead."
                else
                    warn "Option $_i is deprecated!"
                fi
            fi
            if [ -n "$_val" ]; then
                printf '%s\n' "$_val"
            fi
            _gfound=1
        fi
        _deprecated=0
    done
    if [ -n "$_gfound" ]; then
        debug_on
        return 0
    fi
    debug_on
    return 1
}

# Prints value of given option.  If option is a flag and it's present,
# it just returns 0.  Otherwise 1 is returned.
# $1 = options separated by commas
# $2 = option we are interested in
#
# Example:
# $1 = cipher=aes-cbc-essiv:sha256,hash=sha256,verify
# $2 = hash
# Output:
# sha256
getoptcomma() {
    local line=",$1,"
    local opt="$2"
    local tmp

    case "${line}" in
        *,${opt}=*,*)
            tmp="${line#*,${opt}=}"
            echo "${tmp%%,*}"
            return 0
            ;;
        *,${opt},*) return 0 ;;
    esac
    return 1
}

# Splits given string 'str' with separator 'sep' into variables 'var1', 'var2',
# 'varN'.  If number of fields is less than number of variables, remaining are
# not set.  If number of fields is greater than number of variables, the last
# variable takes remaining fields.  In short - it acts similary to 'read'.
#
# splitsep sep str var1 var2 varN
#
# example:
#   splitsep ':' 'foo:bar:baz' v1 v2
# in result:
#   v1='foo', v2='bar:baz'
#
# TODO: ':' inside fields.
splitsep() {
    debug_off
    local sep="$1"
    local str="$2"
    shift 2
    local tmp

    while [ -n "$str" -a "$#" -gt 1 ]; do
        tmp="${str%%$sep*}"
        eval "$1='${tmp}'"
        str="${str#"$tmp"}"
        str="${str#$sep}"
        shift
    done
    [ -n "$str" -a -n "$1" ] && eval "$1='$str'"
    debug_on
    return 0
}

setdebug() {
    [ -f /usr/lib/initrd-release ] || return
    if [ -z "$RD_DEBUG" ]; then
        if [ -e /proc/cmdline ]; then
            RD_DEBUG=no
            if getargbool 0 rd.debug -d -y rdinitdebug -d -y rdnetdebug; then
                RD_DEBUG=yes
                [ -n "$BASH" ] \
                    && export PS4='${BASH_SOURCE}@${LINENO}(${FUNCNAME[0]}): '
            fi
        fi
        export RD_DEBUG
    fi
    debug_on
}

setdebug

source_all() {
    local f
    local _dir
    _dir=$1
    shift
    [ "$_dir" ] && [ -d "/$_dir" ] || return
    for f in "/$_dir"/*.sh; do
        if [ -e "$f" ]; then
            # shellcheck disable=SC1090
            # shellcheck disable=SC2240
            . "$f" "$@"
        fi
    done
}

hookdir=/lib/dracut/hooks
export hookdir

source_hook() {
    local _dir
    _dir=$1
    shift
    source_all "/lib/dracut/hooks/$_dir" "$@"
}

check_finished() {
    local f
    for f in "$hookdir"/initqueue/finished/*.sh; do
        [ "$f" = "$hookdir/initqueue/finished/*.sh" ] && return 0
        # shellcheck disable=SC1090
        { [ -e "$f" ] && (. "$f"); } || return 1
    done
    return 0
}

source_conf() {
    local f
    [ "$1" ] && [ -d "/$1" ] || return
    # shellcheck disable=SC1090
    for f in "/$1"/*.conf; do [ -e "$f" ] && . "$f"; done
}

die() {
    {
        echo "<24>dracut: FATAL: $*"
        echo "<24>dracut: Refusing to continue"
    } > /dev/kmsg

    {
        echo "warn dracut: FATAL: \"$*\""
        echo "warn dracut: Refusing to continue"
    } >> $hookdir/emergency/01-die.sh
    [ -d /run/initramfs ] || mkdir -p -- /run/initramfs

    : > /run/initramfs/.die

    if getargbool 0 "rd.shell"; then
        emergency_shell
    else
        source_hook "shutdown-emergency"
    fi

    if [ -n "$DRACUT_SYSTEMD" ]; then
        systemctl --no-block --force halt
    fi

    exit 1
}

check_quiet() {
    if [ -z "$DRACUT_QUIET" ]; then
        DRACUT_QUIET="yes"
        getargbool 0 rd.info -d -y rdinfo && DRACUT_QUIET="no"
        getargbool 0 rd.debug -d -y rdinitdebug && DRACUT_QUIET="no"
        getarg quiet || DRACUT_QUIET="yes"
        a=$(getarg loglevel=)
        [ -n "$a" ] && [ "$a" -ge 28 ] && DRACUT_QUIET="yes"
        export DRACUT_QUIET
    fi
}

check_occurances() {
    # Count the number of times the character $ch occurs in $str
    # Return 0 if the count matches the expected number, 1 otherwise
    local str="$1"
    local ch="$2"
    local expected="$3"
    local count=0

    while [ "${str#*$ch}" != "${str}" ]; do
        str="${str#*$ch}"
        count=$((count + 1))
    done

    [ $count -eq "$expected" ]
}

incol2() {
    debug_off
    local check
    local file="$1"
    local str="$2"

    [ -z "$file" ] && return 1
    [ -z "$str" ] && return 1

    while read -r _ check _ || [ -n "$check" ]; do
        if [ "$check" = "$str" ]; then
            debug_on
            return 0
        fi
    done < "$file"
    debug_on
    return 1
}

udevsettle() {
    # shellcheck disable=SC2086
    udevadm settle --exit-if-exists=$hookdir/initqueue/work $settle_exit_if_exists
}

udevproperty() {
    for i in "$@"; do
        udevadm control --property="$i"
    done
}

find_mount() {
    local dev wanted_dev
    wanted_dev="$(readlink -e -q "$1")"
    while read -r dev _ || [ -n "$dev" ]; do
        [ "$dev" = "$wanted_dev" ] && echo "$dev" && return 0
    done < /proc/mounts
    return 1
}

# usage: ismounted <mountpoint>
# usage: ismounted /dev/<device>
if command -v findmnt > /dev/null; then
    ismounted() {
        findmnt "$1" > /dev/null 2>&1
    }
else
    ismounted() {
        if [ -b "$1" ]; then
            find_mount "$1" > /dev/null && return 0
            return 1
        fi

        while read -r _ m _ || [ -n "$m" ]; do
            [ "$m" = "$1" ] && return 0
        done < /proc/mounts
        return 1
    }
fi

# Create udev rule match for a device with its device name, or the udev property
# ID_FS_UUID or ID_FS_LABEL
#
# example:
#   udevmatch LABEL=boot
# prints:
#   ENV{ID_FS_LABEL}="boot"
#
# TODO: symlinks
udevmatch() {
    case "$1" in
        UUID=????????-????-????-????-???????????? | LABEL=* | PARTLABEL=* | PARTUUID=????????-????-????-????-????????????)
            printf 'ENV{ID_FS_%s}=="%s"' "${1%%=*}" "${1#*=}"
            ;;
        UUID=*)
            printf 'ENV{ID_FS_UUID}=="%s*"' "${1#*=}"
            ;;
        PARTUUID=*)
            printf 'ENV{ID_FS_PARTUUID}=="%s*"' "${1#*=}"
            ;;
        /dev/?*) printf -- 'KERNEL=="%s"' "${1#/dev/}" ;;
        *) return 255 ;;
    esac
}

label_uuid_to_dev() {
    local _dev
    _dev="${1#block:}"
    case "$_dev" in
        LABEL=*)
            echo "/dev/disk/by-label/$(echo "${_dev#LABEL=}" | sed 's,/,\\x2f,g;s, ,\\x20,g')"
            ;;
        PARTLABEL=*)
            echo "/dev/disk/by-partlabel/$(echo "${_dev#PARTLABEL=}" | sed 's,/,\\x2f,g;s, ,\\x20,g')"
            ;;
        UUID=*)
            echo "/dev/disk/by-uuid/$(echo "${_dev#UUID=}" | tr "[:upper:]" "[:lower:]")"
            ;;
        PARTUUID=*)
            echo "/dev/disk/by-partuuid/$(echo "${_dev#PARTUUID=}" | tr "[:upper:]" "[:lower:]")"
            ;;
    esac
}

# Prints unique path for potential file inside specified directory.  It consists
# of specified directory, prefix and number at the end which is incremented
# until non-existing file is found.
#
# funiq dir prefix
#
# example:
# # ls /mnt
# cdrom0 cdrom1
#
# # funiq /mnt cdrom
# /mnt/cdrom2
funiq() {
    local dir="$1"
    local prefix="$2"
    local i=0

    [ -d "${dir}" ] || return 1

    while [ -e "${dir}/${prefix}$i" ]; do
        i=$((i + 1)) || return 1
    done

    echo "${dir}/${prefix}$i"
}

# Creates unique directory and prints its path.  It's using funiq to generate
# path.
#
# mkuniqdir subdir new_dir_name
mkuniqdir() {
    local dir="$1"
    local prefix="$2"
    local retdir
    local retdir_new

    [ -d "${dir}" ] || mkdir -m 0755 -p "${dir}" || return 1

    retdir=$(funiq "${dir}" "${prefix}") || return 1
    until mkdir -m 0755 "${retdir}" 2> /dev/null; do
        retdir_new=$(funiq "${dir}" "${prefix}") || return 1
        [ "$retdir_new" = "$retdir" ] && return 1
        retdir="$retdir_new"
    done

    echo "${retdir}"
}

# Copy the contents of SRC into DEST, merging the contents of existing
# directories (kinda like rsync, or cpio -p).
# Creates DEST if it doesn't exist. Overwrites files with the same names.
#
# copytree SRC DEST
copytree() {
    local src="$1" dest="$2"
    [ -d "$src" ] || return 1
    mkdir -p "$dest" || return 1
    dest=$(readlink -e -q "$dest") || return 1
    (
        cd "$src" || exit 1
        cp -af . -t "$dest"
    )
}

# Evaluates command for UUIDs either given as arguments for this function or all
# listed in /dev/disk/by-uuid.  UUIDs doesn't have to be fully specified.  If
# beginning is given it is expanded to all matching UUIDs.  To pass full UUID to
# your command use '$___' as a place holder.  Remember to escape '$'!
#
# foreach_uuid_until [ -p prefix ] command UUIDs
#
# prefix - string to put just before $___
# command - command to be evaluated
# UUIDs - list of UUIDs separated by space
#
# The function returns after *first successful evaluation* of the given command
# with status 0.  If evaluation fails for every UUID function returns with
# status 1.
#
# Example:
# foreach_uuid_until "mount -U \$___ /mnt; echo OK; umount /mnt" \
#       "01234 f512 a235567f-12a3-c123-a1b1-01234567abcb"
foreach_uuid_until() (
    cd /dev/disk/by-uuid || return 1

    [ "$1" = -p ] && local prefix="$2" && shift 2
    local cmd="$1"
    shift
    local uuids_list="$*"
    local uuid
    local full_uuid
    local ___

    [ -n "${cmd}" ] || return 1

    for uuid in ${uuids_list:-*}; do
        for full_uuid in "${uuid}"*; do
            [ -e "${full_uuid}" ] || continue
            # shellcheck disable=SC2034
            ___="${prefix}${full_uuid}"
            eval "${cmd}" && return 0
        done
    done

    return 1
)

# Get kernel name for given device.  Device may be the name too (then the same
# is returned), a symlink (full path), UUID (prefixed with "UUID=") or label
# (prefixed with "LABEL=").  If just a beginning of the UUID is specified or
# even an empty, function prints all device names which UUIDs match - every in
# single line.
#
# NOTICE: The name starts with "/dev/".
#
# Example:
#   devnames UUID=123
# May print:
#   /dev/dm-1
#   /dev/sdb1
#   /dev/sdf3
devnames() {
    local dev="$1"
    local d
    local names

    case "$dev" in
        UUID=*)
            # shellcheck disable=SC2016
            dev="$(foreach_uuid_until '! blkid -U $___' "${dev#UUID=}")" \
                && return 255
            [ -z "$dev" ] && return 255
            ;;
        LABEL=*) dev="$(blkid -L "${dev#LABEL=}")" || return 255 ;;
        /dev/?*) ;;
        *) return 255 ;;
    esac

    for d in $dev; do
        names="$names
$(readlink -e -q "$d")" || return 255
    done

    echo "${names#
}"
}

usable_root() {
    local _i

    [ -d "$1" ] || return 1

    for _i in "$1"/usr/lib*/ld-*.so "$1"/lib*/ld-*.so; do
        [ -e "$_i" ] && return 0
    done

    for _i in proc sys dev; do
        [ -e "$1"/$_i ] || return 1
    done

    return 0
}

inst_hook() {
    local _hookname _unique _name _job _exe
    while [ $# -gt 0 ]; do
        case "$1" in
            --hook)
                _hookname="/$2"
                shift
                ;;
            --unique)
                _unique="yes"
                ;;
            --name)
                _name="$2"
                shift
                ;;
            *)
                break
                ;;
        esac
        shift
    done

    if [ -z "$_unique" ]; then
        _job="${_name}$$"
    else
        _job="${_name:-$1}"
        _job=${_job##*/}
    fi

    _exe=$1
    shift

    [ -x "$_exe" ] || _exe=$(command -v "$_exe")

    if [ -n "$onetime" ]; then
        {
            # shellcheck disable=SC2016
            echo '[ -e "$_job" ] && rm -f -- "$_job"'
            echo "$_exe $*"
        } > "/tmp/$$-${_job}.sh"
    else
        echo "$_exe $*" > "/tmp/$$-${_job}.sh"
    fi

    mv -f "/tmp/$$-${_job}.sh" "$hookdir/${_hookname}/${_job}.sh"
}

# inst_mount_hook <mountpoint> <prio> <name> <script>
#
# Install a mount hook with priority <prio>,
# which executes <script> as soon as <mountpoint> is mounted.
inst_mount_hook() {
    local _prio="$2" _jobname="$3" _script="$4"
    local _hookname
    _hookname="mount-$(str_replace "$1" '/' '\\x2f')"
    [ -d "$hookdir/${_hookname}" ] || mkdir -p "$hookdir/${_hookname}"
    inst_hook --hook "$_hookname" --unique --name "${_prio}-${_jobname}" "$_script"
}

# wait_for_mount <mountpoint>
#
# Installs a initqueue-finished script,
# which will cause the main loop only to exit,
# if <mountpoint> is mounted.
wait_for_mount() {
    local _name
    _name="$(str_replace "$1" '/' '\\x2f')"
    printf '. /lib/dracut-lib.sh\nismounted "%s"\n' "$1" \
        >> "$hookdir/initqueue/finished/ismounted-${_name}.sh"
    {
        printf 'ismounted "%s" || ' "$1"
        printf 'warn "\"%s\" is not mounted"\n' "$1"
    } >> "$hookdir/emergency/90-${_name}.sh"
}

killproc() {
    debug_off
    local _exe
    _exe="$(command -v "$1")"
    local _sig=$2
    local _i
    [ -x "$_exe" ] || return 1
    for _i in /proc/[0-9]*; do
        [ "$_i" = "/proc/1" ] && continue
        if [ -e "$_i"/_exe ] && [ "$_i/_exe" -ef "$_exe" ]; then
            kill "$_sig" "${_i##*/}"
        fi
    done
    debug_on
}

need_shutdown() {
    : > /run/initramfs/.need_shutdown
}

wait_for_loginit() {
    [ "$RD_DEBUG" = "yes" ] || return
    [ -e /run/initramfs/loginit.pipe ] || return
    debug_off
    echo "DRACUT_LOG_END"
    exec 0<> /dev/console 1<> /dev/console 2<> /dev/console
    # wait for loginit
    i=0
    while [ $i -lt 10 ]; do
        if [ ! -e /run/initramfs/loginit.pipe ]; then
            j=$(jobs)
            [ -z "$j" ] && break
            [ -z "${j##*Running*}" ] || break
        fi
        sleep 0.1
        i=$((i + 1))
    done

    if [ $i -eq 10 ]; then
        kill %1 > /dev/null 2>&1
        kill "$(while read -r line || [ -n "$line" ]; do echo "$line"; done < /run/initramfs/loginit.pid)"
    fi

    setdebug
    rm -f -- /run/initramfs/loginit.pipe /run/initramfs/loginit.pid
}

# pidof version for root
if ! command -v pidof > /dev/null 2> /dev/null; then
    pidof() {
        debug_off
        local _cmd
        local _exe
        local _rl
        local _ret=1
        local i
        _cmd="$1"
        if [ -z "$_cmd" ]; then
            debug_on
            return 1
        fi
        _exe=$(command -v "$1")
        for i in /proc/*/exe; do
            [ -e "$i" ] || continue
            if [ -n "$_exe" ]; then
                [ "$i" -ef "$_exe" ] || continue
            else
                _rl=$(readlink -f "$i")
                [ "${_rl%/$_cmd}" != "$_rl" ] || continue
            fi
            i=${i%/exe}
            echo "${i##/proc/}"
            _ret=0
        done
        debug_on
        return $_ret
    }
fi

_emergency_shell() {
    local _name="$1"
    if [ -n "$DRACUT_SYSTEMD" ]; then
        : > /.console_lock
        echo "PS1=\"$_name:\\\${PWD}# \"" > /etc/profile
        systemctl start dracut-emergency.service
        rm -f -- /etc/profile
        rm -f -- /.console_lock
    else
        debug_off
        source_hook "$hook"
        echo
        /sbin/rdsosreport
        echo 'You might want to save "/run/initramfs/rdsosreport.txt" to a USB stick or /boot'
        echo 'after mounting them and attach it to a bug report.'
        if ! RD_DEBUG='' getargbool 0 rd.debug -d -y rdinitdebug -d -y rdnetdebug; then
            echo
            echo 'To get more debug information in the report,'
            echo 'reboot with "rd.debug" added to the kernel command line.'
        fi
        echo
        echo 'Dropping to debug shell.'
        echo
        export PS1="$_name:\${PWD}# "
        [ -e /.profile ] || : > /.profile

        _ctty="$(RD_DEBUG='' getarg rd.ctty=)" && _ctty="/dev/${_ctty##*/}"
        if [ -z "$_ctty" ]; then
            _ctty=console
            while [ -f /sys/class/tty/$_ctty/active ]; do
                _ctty=$(cat /sys/class/tty/$_ctty/active)
                _ctty=${_ctty##* } # last one in the list
            done
            _ctty=/dev/$_ctty
        fi
        [ -c "$_ctty" ] || _ctty=/dev/tty1
        case "$(/usr/bin/setsid --help 2>&1)" in *--ctty*) CTTY="--ctty" ;; esac
        setsid $CTTY /bin/sh -i -l 0<> $_ctty 1<> $_ctty 2<> $_ctty
    fi
}

emergency_shell() {
    local _ctty
    set +e
    local _rdshell_name="dracut" action="Boot" hook="emergency"
    local _emergency_action

    if [ "$1" = "-n" ]; then
        _rdshell_name=$2
        shift 2
    elif [ "$1" = "--shutdown" ]; then
        _rdshell_name=$2
        action="Shutdown"
        hook="shutdown-emergency"
        if type plymouth > /dev/null 2>&1; then
            plymouth --hide-splash
        elif [ -x /oldroot/bin/plymouth ]; then
            /oldroot/bin/plymouth --hide-splash
        fi
        shift 2
    fi

    echo
    echo
    warn "$*"
    echo

    _emergency_action=$(getarg rd.emergency)
    [ -z "$_emergency_action" ] \
        && [ -e /run/initramfs/.die ] \
        && _emergency_action=halt

    if getargbool 1 rd.shell -d -y rdshell || getarg rd.break -d rdbreak; then
        _emergency_shell "$_rdshell_name"
    else
        source_hook "$hook"
        warn "$action has failed. To debug this issue add \"rd.shell rd.debug\" to the kernel command line."
        [ -z "$_emergency_action" ] && _emergency_action=halt
    fi

    case "$_emergency_action" in
        reboot)
            reboot || exit 1
            ;;
        poweroff)
            poweroff || exit 1
            ;;
        halt)
            halt || exit 1
            ;;
    esac
}

# Retain the values of these variables but ensure that they are unexported
# This is a POSIX-compliant equivalent of bash's "export -n"
export_n() {
    local var
    local val
    for var in "$@"; do
        eval val=\$$var
        unset $var
        [ -n "$val" ] && eval "$var=\"$val\""
    done
}

# returns OK if list1 contains all elements of list2, i.e. checks if list2 is a
# sublist of list1.  An order and a duplication doesn't matter.
#
# $1 = separator
# $2 = list1
# $3 = list2
# $4 = ignore values, separated by $1
listlist() {
    local _sep="$1"
    local _list="${_sep}${2}${_sep}"
    local _sublist="$3"
    [ -n "$4" ] && local _iglist="${_sep}${4}${_sep}"
    local IFS="$_sep"
    local _v

    [ "$_list" = "$_sublist" ] && return 0

    for _v in $_sublist; do
        if [ -n "$_v" ] && ! ([ -n "$_iglist" ] && strstr "$_iglist" "$_v"); then
            strstr "$_list" "$_v" || return 1
        fi
    done

    return 0
}

# returns OK if both lists contain the same values.  An order and a duplication
# doesn't matter.
#
# $1 = separator
# $2 = list1
# $3 = list2
# $4 = ignore values, separated by $1
are_lists_eq() {
    listlist "$1" "$2" "$3" "$4" && listlist "$1" "$3" "$2" "$4"
}

setmemdebug() {
    if [ -z "$DEBUG_MEM_LEVEL" ]; then
        DEBUG_MEM_LEVEL=$(getargnum 0 0 5 rd.memdebug)
        export DEBUG_MEM_LEVEL
    fi
}

setmemdebug

# parameters: func log_level prefix msg [trace_level:trace]...
make_trace_mem() {
    local log_level prefix msg msg_printed
    local trace trace_level trace_in_higher_levels insert_trace

    msg=$1
    shift

    prefix='[debug_mem]'
    log_level=$DEBUG_MEM_LEVEL

    if [ -z "$log_level" ] || [ "$log_level" -le 0 ]; then
        return
    fi

    # FIXME? useless echo?
    # shellcheck disable=SC2116
    msg=$(echo "$msg")

    msg_printed=0
    while [ $# -gt 0 ]; do
        trace=${1%%:*}
        trace_level=${trace%%+}
        [ "$trace" != "$trace_level" ] && trace_in_higher_levels="yes"
        trace=${1##*:}

        if [ -z "$trace_level" ]; then
            trace_level=0
        fi

        insert_trace=0
        if [ -n "$trace_in_higher_levels" ]; then
            if [ "$log_level" -ge "$trace_level" ]; then
                insert_trace=1
            fi
        else
            if [ "$log_level" -eq "$trace_level" ]; then
                insert_trace=1
            fi
        fi

        if [ $insert_trace -eq 1 ]; then
            if [ $msg_printed -eq 0 ]; then
                echo "$prefix $msg"
                msg_printed=1
            fi
            show_memstats "$trace"
        fi
        shift
    done
}

# parameters: type
show_memstats() {
    case $1 in
        shortmem)
            grep -e "^MemFree" -e "^Cached" -e "^Slab" /proc/meminfo
            ;;
        mem)
            cat /proc/meminfo
            ;;
        slab)
            cat /proc/slabinfo
            ;;
        iomem)
            cat /proc/iomem
            ;;
    esac
}

remove_hostonly_files() {
    rm -fr /etc/cmdline /etc/cmdline.d/*.conf "$hookdir/initqueue/finished"
    if [ -f /lib/dracut/hostonly-files ]; then
        while read -r line || [ -n "$line" ]; do
            [ -e "$line" ] || [ -h "$line" ] || continue
            rm -f "$line"
        done < /lib/dracut/hostonly-files
    fi
}
