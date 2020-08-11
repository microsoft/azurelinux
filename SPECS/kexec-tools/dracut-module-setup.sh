#!/bin/bash

. $dracutfunctions
. /lib/kdump/kdump-lib.sh

if ! [[ -d "${initdir}/tmp" ]]; then
    mkdir -p "${initdir}/tmp"
fi

check() {
    [[ $debug ]] && set -x
    #kdumpctl sets this explicitly
    if [ -z "$IN_KDUMP" ] || [ ! -f /etc/kdump.conf ]
    then
        return 1
    fi
    return 0
}

depends() {
    local _dep="base shutdown"

    is_squash_available() {
        for kmodule in squashfs overlay loop; do
            if [ -z "$KDUMP_KERNELVER" ]; then
                modprobe --dry-run $kmodule &>/dev/null || return 1
            else
                modprobe -S $KDUMP_KERNELVER --dry-run $kmodule &>/dev/null || return 1
            fi
        done
    }

    if is_squash_available && ! is_fadump_capable; then
        _dep="$_dep squash"
    else
        dwarning "Required modules to build a squashed kdump image is missing!"
    fi

    if [ -n "$( find /sys/devices -name drm )" ] || [ -d /sys/module/hyperv_fb ]; then
        _dep="$_dep drm"
    fi

    if is_generic_fence_kdump || is_pcs_fence_kdump; then
        _dep="$_dep network"
    fi

    echo $_dep
    return 0
}

kdump_is_bridge() {
     [ -d /sys/class/net/"$1"/bridge ]
}

kdump_is_bond() {
     [ -d /sys/class/net/"$1"/bonding ]
}

kdump_is_team() {
     [ -f /usr/bin/teamnl ] && teamnl $1 ports &> /dev/null
}

kdump_is_vlan() {
     [ -f /proc/net/vlan/"$1" ]
}

# $1: netdev name
source_ifcfg_file() {
    local ifcfg_file

    ifcfg_file=$(get_ifcfg_filename $1)
    if [ -f "${ifcfg_file}" ]; then
        . ${ifcfg_file}
    else
        dwarning "The ifcfg file of $1 is not found!"
    fi
}

# $1: netdev name
kdump_setup_dns() {
    local _nameserver _dns
    local _dnsfile=${initdir}/etc/cmdline.d/42dns.conf

    source_ifcfg_file $1

    [ -n "$DNS1" ] && echo "nameserver=$DNS1" > "$_dnsfile"
    [ -n "$DNS2" ] && echo "nameserver=$DNS2" >> "$_dnsfile"

    while read content;
    do
        _nameserver=$(echo $content | grep ^nameserver)
        [ -z "$_nameserver" ] && continue

        _dns=$(echo $_nameserver | cut -d' ' -f2)
        [ -z "$_dns" ] && continue

        if [ ! -f $_dnsfile ] || [ ! $(cat $_dnsfile | grep -q $_dns) ]; then
            echo "nameserver=$_dns" >> "$_dnsfile"
        fi
    done < "/etc/resolv.conf"
}

#$1: netdev name
#$2: srcaddr
#if it use static ip echo it, or echo null
kdump_static_ip() {
    local _netdev="$1" _srcaddr="$2" _ipv6_flag
    local _netmask _gateway _ipaddr _target _nexthop

    _ipaddr=$(ip addr show dev $_netdev permanent | awk "/ $_srcaddr\/.* /{print \$2}")

    if is_ipv6_address $_srcaddr; then
        _ipv6_flag="-6"
    fi

    if [ -n "$_ipaddr" ]; then
        _gateway=$(ip $_ipv6_flag route list dev $_netdev | \
                awk '/^default /{print $3}' | head -n 1)

        if [ "x" !=  "x"$_ipv6_flag ]; then
            # _ipaddr="2002::56ff:feb6:56d5/64", _netmask is the number after "/"
            _netmask=${_ipaddr#*\/}
            _srcaddr="[$_srcaddr]"
            _gateway="[$_gateway]"
        else
            _netmask=$(ipcalc -m $_ipaddr | cut -d'=' -f2)
        fi
        echo -n "${_srcaddr}::${_gateway}:${_netmask}::"
    fi

    /sbin/ip $_ipv6_flag route show | grep -v default |\
    grep ".*via.* $_netdev " | grep -v "^[[:space:]]*nexthop" |\
    while read _route; do
        _target=`echo $_route | cut -d ' ' -f1`
        _nexthop=`echo $_route | cut -d ' ' -f3`
        if [ "x" !=  "x"$_ipv6_flag ]; then
            _target="[$_target]"
            _nexthop="[$_nexthop]"
        fi
        echo "rd.route=$_target:$_nexthop:$_netdev"
    done >> ${initdir}/etc/cmdline.d/45route-static.conf

    kdump_handle_mulitpath_route $_netdev $_srcaddr
}

kdump_handle_mulitpath_route() {
    local _netdev="$1" _srcaddr="$2" _ipv6_flag
    local _target _nexthop _route _weight _max_weight _rule

    if is_ipv6_address $_srcaddr; then
        _ipv6_flag="-6"
    fi

    while IFS="" read _route; do
        if [[ "$_route" =~ [[:space:]]+nexthop ]]; then
            _route=$(echo "$_route" | sed -e 's/^[[:space:]]*//')
            # Parse multipath route, using previous _target
            [[ "$_target" == 'default' ]] && continue
            [[ "$_route" =~ .*via.*\ $_netdev ]] || continue

            _weight=`echo "$_route" | cut -d ' ' -f7`
            if [[ "$_weight" -gt "$_max_weight" ]]; then
                _nexthop=`echo "$_route" | cut -d ' ' -f3`
                _max_weight=$_weight
                if [ "x" !=  "x"$_ipv6_flag ]; then
                    _rule="rd.route=[$_target]:[$_nexthop]:$_netdev"
                else
                    _rule="rd.route=$_target:$_nexthop:$_netdev"
                fi
            fi
        else
            [[ -n "$_rule" ]] && echo "$_rule"
            _target=`echo "$_route" | cut -d ' ' -f1`
            _rule="" _max_weight=0 _weight=0
        fi
    done >> ${initdir}/etc/cmdline.d/45route-static.conf\
        <<< "$(/sbin/ip $_ipv6_flag route show)"

    [[ -n $_rule ]] && echo $_rule >> ${initdir}/etc/cmdline.d/45route-static.conf
}

kdump_get_mac_addr() {
    cat /sys/class/net/$1/address
}

#Bonding or team master modifies the mac address
#of its slaves, we should use perm address
kdump_get_perm_addr() {
    local addr=$(ethtool -P $1 | sed -e 's/Permanent address: //')
    if [ -z "$addr" ] || [ "$addr" = "00:00:00:00:00:00" ]
    then
        derror "Can't get the permanent address of $1"
    else
        echo "$addr"
    fi
}

# Prefix kernel assigned names with "kdump-". EX: eth0 -> kdump-eth0
# Because kernel assigned names are not persistent between 1st and 2nd
# kernel. We could probably end up with eth0 being eth1, eth0 being
# eth1, and naming conflict happens.
kdump_setup_ifname() {
    local _ifname

    # If ifname already has 'kdump-' prefix, we must be switching from
    # fadump to kdump. Skip prefixing 'kdump-' in this case as adding
    # another prefix may truncate the ifname. Since an ifname with
    # 'kdump-' is already persistent, this should be fine.
    if [[ $1 =~ eth* ]] && [[ ! $1 =~ ^kdump-* ]]; then
        _ifname="kdump-$1"
    else
        _ifname="$1"
    fi

    echo "$_ifname"
}

kdump_setup_bridge() {
    local _netdev=$1
    local _brif _dev _mac _kdumpdev
    for _dev in `ls /sys/class/net/$_netdev/brif/`; do
        _kdumpdev=$_dev
        if kdump_is_bond "$_dev"; then
            kdump_setup_bond "$_dev"
        elif kdump_is_team "$_dev"; then
            kdump_setup_team "$_dev"
        elif kdump_is_vlan "$_dev"; then
            kdump_setup_vlan "$_dev"
        else
            _mac=$(kdump_get_mac_addr $_dev)
            _kdumpdev=$(kdump_setup_ifname $_dev)
            echo -n " ifname=$_kdumpdev:$_mac" >> ${initdir}/etc/cmdline.d/41bridge.conf
        fi
        _brif+="$_kdumpdev,"
    done
    echo " bridge=$_netdev:$(echo $_brif | sed -e 's/,$//')" >> ${initdir}/etc/cmdline.d/41bridge.conf
}

kdump_setup_bond() {
    local _netdev=$1
    local _dev _mac _slaves _kdumpdev
    for _dev in `cat /sys/class/net/$_netdev/bonding/slaves`; do
        _mac=$(kdump_get_perm_addr $_dev)
        _kdumpdev=$(kdump_setup_ifname $_dev)
        echo -n " ifname=$_kdumpdev:$_mac" >> ${initdir}/etc/cmdline.d/42bond.conf
        _slaves+="$_kdumpdev,"
    done
    echo -n " bond=$_netdev:$(echo $_slaves | sed 's/,$//')" >> ${initdir}/etc/cmdline.d/42bond.conf
    # Get bond options specified in ifcfg

    source_ifcfg_file $_netdev

    bondoptions=":$(echo $BONDING_OPTS | xargs echo | tr " " ",")"
    echo "$bondoptions" >> ${initdir}/etc/cmdline.d/42bond.conf
}

kdump_setup_team() {
    local _netdev=$1
    local _dev _mac _slaves _kdumpdev
    for _dev in `teamnl $_netdev ports | awk -F':' '{print $2}'`; do
        _mac=$(kdump_get_perm_addr $_dev)
        _kdumpdev=$(kdump_setup_ifname $_dev)
        echo -n " ifname=$_kdumpdev:$_mac" >> ${initdir}/etc/cmdline.d/44team.conf
        _slaves+="$_kdumpdev,"
    done
    echo " team=$_netdev:$(echo $_slaves | sed -e 's/,$//')" >> ${initdir}/etc/cmdline.d/44team.conf
    #Buggy version teamdctl outputs to stderr!
    #Try to use the latest version of teamd.
    teamdctl "$_netdev" config dump > ${initdir}/tmp/$$-$_netdev.conf
    if [ $? -ne 0 ]
    then
        derror "teamdctl failed."
        exit 1
    fi
    inst_dir /etc/teamd
    inst_simple ${initdir}/tmp/$$-$_netdev.conf "/etc/teamd/$_netdev.conf"
    rm -f ${initdir}/tmp/$$-$_netdev.conf
}

kdump_setup_vlan() {
    local _netdev=$1
    local _phydev="$(awk '/^Device:/{print $2}' /proc/net/vlan/"$_netdev")"
    local _netmac="$(kdump_get_mac_addr $_phydev)"
    local _kdumpdev

    #Just support vlan over bond, it is not easy
    #to support all other complex setup
    if kdump_is_bridge "$_phydev"; then
        derror "Vlan over bridge is not supported!"
        exit 1
    elif kdump_is_team "$_phydev"; then
        derror "Vlan over team is not supported!"
        exit 1
    elif kdump_is_bond "$_phydev"; then
        kdump_setup_bond "$_phydev"
        echo " vlan=$(kdump_setup_ifname $_netdev):$_phydev" > ${initdir}/etc/cmdline.d/43vlan.conf
    else
        _kdumpdev="$(kdump_setup_ifname $_phydev)"
        echo " vlan=$(kdump_setup_ifname $_netdev):$_kdumpdev ifname=$_kdumpdev:$_netmac" > ${initdir}/etc/cmdline.d/43vlan.conf
    fi
}

# setup s390 znet cmdline
# $1: netdev name
kdump_setup_znet() {
    local _options=""
    local _netdev=$1

    source_ifcfg_file $_netdev

    for i in $OPTIONS; do
        _options=${_options},$i
    done
    echo rd.znet=${NETTYPE},${SUBCHANNELS}${_options} rd.znet_ifname=$_netdev:${SUBCHANNELS} > ${initdir}/etc/cmdline.d/30znet.conf
}

kdump_get_ip_route()
{
    local _route=$(/sbin/ip -o route get to $1 2>&1)
    [ $? != 0 ] && die "Bad kdump network destination: $1"
    echo $_route
}

kdump_get_ip_route_field()
{
    if `echo $1 | grep -q $2`; then
        echo ${1##*$2} | cut -d ' ' -f1
    fi
}

kdump_get_remote_ip()
{
    local _remote=$(get_remote_host $1) _remote_temp
    if is_hostname $_remote; then
        _remote_temp=`getent ahosts $_remote | grep -v : | head -n 1`
        if [ -z "$_remote_temp" ]; then
            _remote_temp=`getent ahosts $_remote | head -n 1`
        fi
        _remote=`echo $_remote_temp | cut -d' ' -f1`
    fi
    echo $_remote
}

# Setup dracut to bring up network interface that enable
# initramfs accessing giving destination
# $1: destination host
kdump_install_net() {
    local _destaddr _srcaddr _route _netdev
    local _static _proto _ip_conf _ip_opts _ifname_opts

    _destaddr=$(kdump_get_remote_ip $1)
    _route=$(kdump_get_ip_route $_destaddr)
    _srcaddr=$(kdump_get_ip_route_field "$_route" "src")
    _netdev=$(kdump_get_ip_route_field "$_route" "dev")
    _netmac=$(kdump_get_mac_addr $_netdev)

    if [ "$(uname -m)" = "s390x" ]; then
        kdump_setup_znet $_netdev
    fi

    _static=$(kdump_static_ip $_netdev $_srcaddr)
    if [ -n "$_static" ]; then
        _proto=none
    elif is_ipv6_address $_srcaddr; then
        _proto=either6
    else
        _proto=dhcp
    fi

    _ip_conf="${initdir}/etc/cmdline.d/40ip.conf"
    _ip_opts=" ip=${_static}$(kdump_setup_ifname $_netdev):${_proto}"

    # dracut doesn't allow duplicated configuration for same NIC, even they're exactly the same.
    # so we have to avoid adding duplicates
    # We should also check /proc/cmdline for existing ip=xx arg.
    # For example, iscsi boot will specify ip=xxx arg in cmdline.
    if [ ! -f $_ip_conf ] || ! grep -q $_ip_opts $_ip_conf &&\
        ! grep -q "ip=[^[:space:]]*$_netdev" /proc/cmdline; then
        echo "$_ip_opts" >> $_ip_conf
    fi

    if kdump_is_bridge "$_netdev"; then
        kdump_setup_bridge "$_netdev"
    elif kdump_is_bond "$_netdev"; then
        kdump_setup_bond "$_netdev"
    elif kdump_is_team "$_netdev"; then
        kdump_setup_team "$_netdev"
    elif kdump_is_vlan "$_netdev"; then
        kdump_setup_vlan "$_netdev"
    else
        _ifname_opts=" ifname=$(kdump_setup_ifname $_netdev):$_netmac"
        echo "$_ifname_opts" >> $_ip_conf
    fi

    kdump_setup_dns "$_netdev"

    if [ ! -f ${initdir}/etc/cmdline.d/50neednet.conf ]; then
        # network-manager module needs this parameter
        echo "rd.neednet" >> ${initdir}/etc/cmdline.d/50neednet.conf
    fi

    # Save netdev used for kdump as cmdline
    # Whoever calling kdump_install_net() is setting up the default gateway,
    # ie. bootdev/kdumpnic. So don't override the setting if calling
    # kdump_install_net() for another time. For example, after setting eth0 as
    # the default gate way for network dump, eth1 in the fence kdump path will
    # call kdump_install_net again and we don't want eth1 to be the default
    # gateway.
    if [ ! -f ${initdir}/etc/cmdline.d/60kdumpnic.conf ] &&
       [ ! -f ${initdir}/etc/cmdline.d/70bootdev.conf ]; then
        echo "kdumpnic=$(kdump_setup_ifname $_netdev)" > ${initdir}/etc/cmdline.d/60kdumpnic.conf
        echo "bootdev=$(kdump_setup_ifname $_netdev)" > ${initdir}/etc/cmdline.d/70bootdev.conf
    fi
}

# install etc/kdump/pre.d and /etc/kdump/post.d
kdump_install_pre_post_conf() {
    if [ -d /etc/kdump/pre.d ]; then
        for file in /etc/kdump/pre.d/*; do
            if [ -x "$file" ]; then
                dracut_install $file
            else
               echo "$file is not executable"
            fi
        done
    fi

    if [ -d /etc/kdump/post.d ]; then
        for file in /etc/kdump/post.d/*; do
            if [ -x "$file" ]; then
                dracut_install $file
            else
                echo "$file is not executable"
            fi
        done
    fi
}

default_dump_target_install_conf()
{
    local _target _fstype
    local _mntpoint _save_path

    is_user_configured_dump_target && return

    _save_path=$(get_bind_mount_source $(get_save_path))
    _target=$(get_target_from_path $_save_path)
    _mntpoint=$(get_mntpoint_from_target $_target)

    _fstype=$(get_fs_type_from_target $_target)
    if is_fs_type_nfs $_fstype; then
        kdump_install_net "$_target"
        _fstype="nfs"
    else
        _target=$(kdump_get_persistent_dev $_target)
    fi

    echo "$_fstype $_target" >> ${initdir}/tmp/$$-kdump.conf

    # don't touch the path under root mount
    if [ "$_mntpoint" != "/" ]; then
        _save_path=${_save_path##"$_mntpoint"}
    fi

    #erase the old path line, then insert the parsed path
    sed -i "/^path/d" ${initdir}/tmp/$$-kdump.conf
    echo "path $_save_path" >> ${initdir}/tmp/$$-kdump.conf
}

#install kdump.conf and what user specifies in kdump.conf
kdump_install_conf() {
    local _opt _val _pdev
    (read_strip_comments /etc/kdump.conf) > ${initdir}/tmp/$$-kdump.conf

    while read _opt _val;
    do
        # remove inline comments after the end of a directive.
        case "$_opt" in
        raw)
            _pdev=$(persistent_policy="by-id" kdump_get_persistent_dev $_val)
            sed -i -e "s#^$_opt[[:space:]]\+$_val#$_opt $_pdev#" ${initdir}/tmp/$$-kdump.conf
            ;;
        ext[234]|xfs|btrfs|minix)
            _pdev=$(kdump_get_persistent_dev $_val)
            sed -i -e "s#^$_opt[[:space:]]\+$_val#$_opt $_pdev#" ${initdir}/tmp/$$-kdump.conf
            ;;
        ssh|nfs)
            kdump_install_net "$_val"
            ;;
        dracut_args)
            if [[ $(get_dracut_args_fstype "$_val") = nfs* ]] ; then
                kdump_install_net "$(get_dracut_args_target "$_val")"
            fi
            ;;
        kdump_pre|kdump_post|extra_bins)
            dracut_install $_val
            ;;
        core_collector)
            dracut_install "${_val%%[[:blank:]]*}"
            ;;
        esac
    done <<< "$(read_strip_comments /etc/kdump.conf)"

    kdump_install_pre_post_conf

    default_dump_target_install_conf

    kdump_configure_fence_kdump  "${initdir}/tmp/$$-kdump.conf"
    inst "${initdir}/tmp/$$-kdump.conf" "/etc/kdump.conf"
    rm -f ${initdir}/tmp/$$-kdump.conf
}

# Remove user custom configurations sysctl.conf & sysctl.d/*
# and apply some optimization for kdump
overwrite_sysctl_conf() {
    # As custom configurations like vm.min_free_kbytes can lead
    # to OOM issues in kdump kernel, avoid them
    rm -f "${initdir}/etc/sysctl.conf"
    rm -rf "${initdir}/etc/sysctl.d"
    rm -rf "${initdir}/run/sysctl.d"
    rm -rf "${initdir}/usr/lib/sysctl.d"

    mkdir -p "${initdir}/etc/sysctl.d"
    echo "vm.zone_reclaim_mode = 3" > "${initdir}/etc/sysctl.d/99-zone-reclaim.conf"
}

kdump_iscsi_get_rec_val() {

    local result

    # The open-iscsi 742 release changed to using flat files in
    # /var/lib/iscsi.

    result=$(/sbin/iscsiadm --show -m session -r ${1} | grep "^${2} = ")
    result=${result##* = }
    echo $result
}

kdump_get_iscsi_initiator() {
    local _initiator
    local initiator_conf="/etc/iscsi/initiatorname.iscsi"

    [ -f "$initiator_conf" ] || return 1

    while read _initiator; do
        [ -z "${_initiator%%#*}" ] && continue # Skip comment lines

        case $_initiator in
            InitiatorName=*)
                initiator=${_initiator#InitiatorName=}
                echo "rd.iscsi.initiator=${initiator}"
                return 0;;
            *) ;;
        esac
    done < ${initiator_conf}

    return 1
}

# Figure out iBFT session according to session type
is_ibft() {
    [ "$(kdump_iscsi_get_rec_val $1 "node.discovery_type")" = fw ]
}

kdump_setup_iscsi_device() {
    local path=$1
    local tgt_name; local tgt_ipaddr;
    local username; local password; local userpwd_str;
    local username_in; local password_in; local userpwd_in_str;
    local netroot_str ; local initiator_str;
    local netroot_conf="${initdir}/etc/cmdline.d/50iscsi.conf"
    local initiator_conf="/etc/iscsi/initiatorname.iscsi"

    dinfo "Found iscsi component $1"

    # Check once before getting explicit values, so we can bail out early,
    # e.g. in case of pure-hardware(all-offload) iscsi.
    if ! /sbin/iscsiadm -m session -r ${path} &>/dev/null ; then
        return 1
    fi

    if is_ibft ${path}; then
        return
    fi

    # Remove software iscsi cmdline generated by 95iscsi,
    # and let kdump regenerate here.
    rm -f ${initdir}/etc/cmdline.d/95iscsi.conf

    tgt_name=$(kdump_iscsi_get_rec_val ${path} "node.name")
    tgt_ipaddr=$(kdump_iscsi_get_rec_val ${path} "node.conn\[0\].address")

    # get and set username and password details
    username=$(kdump_iscsi_get_rec_val ${path} "node.session.auth.username")
    [ "$username" == "<empty>" ] && username=""
    password=$(kdump_iscsi_get_rec_val ${path} "node.session.auth.password")
    [ "$password" == "<empty>" ] && password=""
    username_in=$(kdump_iscsi_get_rec_val ${path} "node.session.auth.username_in")
    [ -n "$username" ] && userpwd_str="$username:$password"

    # get and set incoming username and password details
    [ "$username_in" == "<empty>" ] && username_in=""
    password_in=$(kdump_iscsi_get_rec_val ${path} "node.session.auth.password_in")
    [ "$password_in" == "<empty>" ] && password_in=""

    [ -n "$username_in" ] && userpwd_in_str=":$username_in:$password_in"

    kdump_install_net "$tgt_ipaddr"

    # prepare netroot= command line
    # FIXME: Do we need to parse and set other parameters like protocol, port
    #        iscsi_iface_name, netdev_name, LUN etc.

    if is_ipv6_address $tgt_ipaddr; then
        tgt_ipaddr="[$tgt_ipaddr]"
    fi
    netroot_str="netroot=iscsi:${userpwd_str}${userpwd_in_str}@$tgt_ipaddr::::$tgt_name"

    [[ -f $netroot_conf ]] || touch $netroot_conf

    # If netroot target does not exist already, append.
    if ! grep -q $netroot_str $netroot_conf; then
         echo $netroot_str >> $netroot_conf
         dinfo "Appended $netroot_str to $netroot_conf"
    fi

    # Setup initator
    initiator_str=$(kdump_get_iscsi_initiator)
    [ $? -ne "0" ] && derror "Failed to get initiator name" && return 1

    # If initiator details do not exist already, append.
    if ! grep -q "$initiator_str" $netroot_conf; then
         echo "$initiator_str" >> $netroot_conf
         dinfo "Appended "$initiator_str" to $netroot_conf"
    fi
}

kdump_check_iscsi_targets () {
    # If our prerequisites are not met, fail anyways.
    type -P iscsistart >/dev/null || return 1

    kdump_check_setup_iscsi() (
        local _dev
        _dev=$1

        [[ -L /sys/dev/block/$_dev ]] || return
        cd "$(readlink -f /sys/dev/block/$_dev)"
        until [[ -d sys || -d iscsi_session ]]; do
            cd ..
        done
        [[ -d iscsi_session ]] && kdump_setup_iscsi_device "$PWD"
    )

    [[ $hostonly ]] || [[ $mount_needs ]] && {
        for_each_host_dev_and_slaves_all kdump_check_setup_iscsi
    }
}

# hostname -a is deprecated, do it by ourself
get_alias() {
    local ips
    local entries
    local alias_set

    ips=$(hostname -I)
    for ip in $ips
    do
            # in /etc/hosts, alias can come at the 2nd column
            entries=$(grep $ip /etc/hosts | awk '{ $1=""; print $0 }')
            if [ $? -eq 0 ]; then
                    alias_set="$alias_set $entries"
            fi
    done

    echo $alias_set
}

is_localhost() {
    local hostnames=$(hostname -A)
    local shortnames=$(hostname -A -s)
    local aliasname=$(get_alias)
    local nodename=$1

    hostnames="$hostnames $shortnames $aliasname"

    for name in ${hostnames}; do
        if [ "$name" == "$nodename" ]; then
            return 0
        fi
    done
    return 1
}

# retrieves fence_kdump nodes from Pacemaker cluster configuration
get_pcs_fence_kdump_nodes() {
    local nodes

    pcs cluster sync > /dev/null 2>&1 && pcs cluster cib-upgrade > /dev/null 2>&1
    # get cluster nodes from cluster cib, get interface and ip address
    nodelist=`pcs cluster cib | xmllint --xpath "/cib/status/node_state/@uname" -`

    # nodelist is formed as 'uname="node1" uname="node2" ... uname="nodeX"'
    # we need to convert each to node1, node2 ... nodeX in each iteration
    for node in ${nodelist}; do
        # convert $node from 'uname="nodeX"' to 'nodeX'
        eval $node
        nodename=$uname
        # Skip its own node name
        if is_localhost $nodename; then
            continue
        fi
        nodes="$nodes $nodename"
    done

    echo $nodes
}

# retrieves fence_kdump args from config file
get_pcs_fence_kdump_args() {
    if [ -f $FENCE_KDUMP_CONFIG_FILE ]; then
        . $FENCE_KDUMP_CONFIG_FILE
        echo $FENCE_KDUMP_OPTS
    fi
}

get_generic_fence_kdump_nodes() {
    local filtered
    local nodes

    nodes=$(get_option_value "fence_kdump_nodes")
    for node in ${nodes}; do
        # Skip its own node name
        if is_localhost $node; then
            continue
        fi
        filtered="$filtered $node"
    done
    echo $filtered
}

# setup fence_kdump in cluster
# setup proper network and install needed files
kdump_configure_fence_kdump () {
    local kdump_cfg_file=$1
    local nodes
    local args

    if is_generic_fence_kdump; then
        nodes=$(get_generic_fence_kdump_nodes)

    elif is_pcs_fence_kdump; then
        nodes=$(get_pcs_fence_kdump_nodes)

        # set appropriate options in kdump.conf
        echo "fence_kdump_nodes $nodes" >> ${kdump_cfg_file}

        args=$(get_pcs_fence_kdump_args)
        if [ -n "$args" ]; then
            echo "fence_kdump_args $args" >> ${kdump_cfg_file}
        fi

    else
        # fence_kdump not configured
        return 1
    fi

    # setup network for each node
    for node in ${nodes}; do
        kdump_install_net $node
    done

    dracut_install /etc/hosts
    dracut_install /etc/nsswitch.conf
    dracut_install $FENCE_KDUMP_SEND
}

# Install a random seed used to feed /dev/urandom
# By the time kdump service starts, /dev/uramdom is already fed by systemd
kdump_install_random_seed() {
    local poolsize=`cat /proc/sys/kernel/random/poolsize`

    if [ ! -d ${initdir}/var/lib/ ]; then
        mkdir -p ${initdir}/var/lib/
    fi

    dd if=/dev/urandom of=${initdir}/var/lib/random-seed \
       bs=$poolsize count=1 2> /dev/null
}

install() {
    kdump_install_conf
    overwrite_sysctl_conf

    if is_ssh_dump_target; then
        kdump_install_random_seed
    fi
    dracut_install -o /etc/adjtime /etc/localtime
    inst "$moddir/monitor_dd_progress" "/kdumpscripts/monitor_dd_progress"
    chmod +x ${initdir}/kdumpscripts/monitor_dd_progress
    inst "/bin/dd" "/bin/dd"
    inst "/bin/tail" "/bin/tail"
    inst "/bin/date" "/bin/date"
    inst "/bin/sync" "/bin/sync"
    inst "/bin/cut" "/bin/cut"
    inst "/bin/head" "/bin/head"
    inst "/bin/awk" "/bin/awk"
    inst "/bin/sed" "/bin/sed"
    inst "/sbin/makedumpfile" "/sbin/makedumpfile"
    inst "/sbin/vmcore-dmesg" "/sbin/vmcore-dmesg"
    inst "/lib/kdump/kdump-lib.sh" "/lib/kdump-lib.sh"
    inst "/lib/kdump/kdump-lib-initramfs.sh" "/lib/kdump-lib-initramfs.sh"
    inst "$moddir/kdump.sh" "/usr/bin/kdump.sh"
    inst "$moddir/kdump-capture.service" "$systemdsystemunitdir/kdump-capture.service"
    mkdir -p "$initdir/$systemdsystemunitdir/initrd.target.wants"
    ln_r "$systemdsystemunitdir/kdump-capture.service" "$systemdsystemunitdir/initrd.target.wants/kdump-capture.service"
    inst "$moddir/kdump-error-handler.sh" "/usr/bin/kdump-error-handler.sh"
    inst "$moddir/kdump-error-handler.service" "$systemdsystemunitdir/kdump-error-handler.service"
    # Replace existing emergency service and emergency target
    cp "$moddir/kdump-emergency.service" "$initdir/$systemdsystemunitdir/emergency.service"
    cp "$moddir/kdump-emergency.target" "$initdir/$systemdsystemunitdir/emergency.target"
    # Also redirect dracut-emergency to kdump error handler
    ln_r "$systemdsystemunitdir/emergency.service" "$systemdsystemunitdir/dracut-emergency.service"

    # Check for all the devices and if any device is iscsi, bring up iscsi
    # target. Ideally all this should be pushed into dracut iscsi module
    # at some point of time.
    kdump_check_iscsi_targets

    # nfs/ssh dump will need to get host ip in second kernel and need to call 'ip' tool, see get_host_ip for more detail
    if is_nfs_dump_target || is_ssh_dump_target; then
        inst "ip"
    fi

    # For the lvm type target under kdump, in /etc/lvm/lvm.conf we can
    # safely replace "reserved_memory=XXXX"(default value is 8192) with
    # "reserved_memory=1024" to lower memory pressure under kdump. We do
    # it unconditionally here, if "/etc/lvm/lvm.conf" doesn't exist, it
    # actually does nothing.
    sed -i -e \
      's/\(^[[:space:]]*reserved_memory[[:space:]]*=\)[[:space:]]*[[:digit:]]*/\1 1024/' \
      ${initdir}/etc/lvm/lvm.conf &>/dev/null

    # Kdump turns out to require longer default systemd mount timeout
    # than 1st kernel(90s by default), we use default 300s for kdump.
    grep -r "^[[:space:]]*DefaultTimeoutStartSec=" ${initdir}/etc/systemd/system.conf* &>/dev/null
    if [ $? -ne 0 ]; then
        mkdir -p ${initdir}/etc/systemd/system.conf.d
        echo "[Manager]" > ${initdir}/etc/systemd/system.conf.d/kdump.conf
        echo "DefaultTimeoutStartSec=300s" >> ${initdir}/etc/systemd/system.conf.d/kdump.conf
    fi

    # Forward logs to console directly, this avoids unneccessary memory
    # consumption and make console output more useful.
    # Only do so for non fadump image.
    if ! is_fadump_capable; then
        mkdir -p ${initdir}/etc/systemd/journald.conf.d
        echo "[Journal]" > ${initdir}/etc/systemd/journald.conf.d/kdump.conf
        echo "Storage=none" >> ${initdir}/etc/systemd/journald.conf.d/kdump.conf
        echo "ForwardToConsole=yes" >> ${initdir}/etc/systemd/journald.conf.d/kdump.conf

        # Save more memory by dropping switch root capability
        dracut_no_switch_root
    fi
}
