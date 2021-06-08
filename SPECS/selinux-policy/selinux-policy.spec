# upstream does not currently have a build tag for mariner customizations
# Work item to refine Mariner-specific policy customizations:
# https://microsoft.visualstudio.com/OS/_workitems/edit/29662332
%define distro redhat
%define polyinstatiate n
%define monolithic n
%define POLICYVER 31
%define POLICYCOREUTILSVER 2.9
%define CHECKPOLICYVER 2.9
Summary:        SELinux policy
Name:           selinux-policy
Version:        2.20200818
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/SELinuxProject/refpolicy
Source0:        %{url}/releases/download/RELEASE_2_20200818/refpolicy-%{version}.tar.bz2
Source1:        Makefile.devel
BuildRequires:  bzip2
BuildRequires:  checkpolicy >= %{CHECKPOLICYVER}
BuildRequires:  m4
BuildRequires:  policycoreutils-devel >= %{POLICYCOREUTILSVER}
BuildRequires:  python3
BuildRequires:  python3-xml
Requires(pre):  coreutils
Requires(pre):  policycoreutils >= %{POLICYCOREUTILSVER}
BuildArch:      noarch

%description
SELinux policy describes security properties of system components, to be
enforced by the kernel when running with SELinux enabled.

%files
%license COPYING
%dir %{_usr}/share/selinux
%dir %{_usr}/share/selinux/packages
%dir %{_sysconfdir}/selinux
%ghost %config(noreplace) %{_sysconfdir}/selinux/config
%ghost %{_sysconfdir}/sysconfig/selinux
%{_datadir}/selinux/refpolicy
%dir %{_sysconfdir}/selinux/refpolicy
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/selinux/refpolicy/seusers
%dir %{_sysconfdir}/selinux/refpolicy/logins
%dir %{_sharedstatedir}/selinux/refpolicy/active
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/refpolicy/semanage.read.LOCK
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/refpolicy/semanage.trans.LOCK
%dir %attr(700,root,root) %dir %{_sharedstatedir}/selinux/refpolicy/active/modules
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/refpolicy/active/modules/100/base
%dir %{_sysconfdir}/selinux/refpolicy/policy/
%verify(not md5 size mtime) %{_sysconfdir}/selinux/refpolicy/policy/policy.%{POLICYVER}
%dir %{_sysconfdir}/selinux/refpolicy/contexts
%config %{_sysconfdir}/selinux/refpolicy/contexts/customizable_types
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/securetty_types
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/dbus_contexts
%config %{_sysconfdir}/selinux/refpolicy/contexts/x_contexts
%config %{_sysconfdir}/selinux/refpolicy/contexts/default_contexts
%config %{_sysconfdir}/selinux/refpolicy/contexts/virtual_domain_context
%config %{_sysconfdir}/selinux/refpolicy/contexts/virtual_image_context
%config %{_sysconfdir}/selinux/refpolicy/contexts/lxc_contexts
%config %{_sysconfdir}/selinux/refpolicy/contexts/sepgsql_contexts
%config %{_sysconfdir}/selinux/refpolicy/contexts/openrc_contexts
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/default_type
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/failsafe_context
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/initrc_context
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/removable_context
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/userhelper_context
%dir %{_sysconfdir}/selinux/refpolicy/contexts/files
%verify(not md5 size mtime) %{_sysconfdir}/selinux/refpolicy/contexts/files/file_contexts
%ghost %{_sysconfdir}/selinux/refpolicy/contexts/files/file_contexts.bin
%verify(not md5 size mtime) %{_sysconfdir}/selinux/refpolicy/contexts/files/file_contexts.homedirs
%ghost %{_sysconfdir}/selinux/refpolicy/contexts/files/file_contexts.homedirs.bin
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/files/file_contexts.local
%ghost %{_sysconfdir}/selinux/refpolicy/contexts/files/file_contexts.local.bin
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/files/file_contexts.subs
%{_sysconfdir}/selinux/refpolicy/contexts/files/file_contexts.subs_dist
%config %{_sysconfdir}/selinux/refpolicy/contexts/files/media
%dir %{_sysconfdir}/selinux/refpolicy/contexts/users
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/users/root
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/users/guest_u
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/users/xguest_u
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/users/user_u
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/users/staff_u
%config(noreplace) %{_sysconfdir}/selinux/refpolicy/contexts/users/unconfined_u
%{_sharedstatedir}/selinux/refpolicy/active/commit_num
%{_sharedstatedir}/selinux/refpolicy/active/users_extra
%{_sharedstatedir}/selinux/refpolicy/active/homedir_template
%{_sharedstatedir}/selinux/refpolicy/active/seusers
%{_sharedstatedir}/selinux/refpolicy/active/file_contexts
%{_sharedstatedir}/selinux/refpolicy/active/policy.kern
%ghost %{_sharedstatedir}/selinux/refpolicy/active/policy.linked
%ghost %{_sharedstatedir}/selinux/refpolicy/active/seusers.linked
%ghost %{_sharedstatedir}/selinux/refpolicy/active/users_extra.linked
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/refpolicy/active/file_contexts.homedirs
%ghost %{_sharedstatedir}/selinux/refpolicy/active/modules/100/*

%package devel
Summary:        SELinux policy devel
Requires:       %{_bindir}/make
Requires:       checkpolicy >= %{CHECKPOLICYVER}
Requires:       m4
Requires(post): policycoreutils-devel >= %{POLICYCOREUTILSVER}

%description devel
SELinux policy development and man page package

%files devel
%dir %{_usr}/share/selinux/devel
%dir %{_usr}/share/selinux/devel/include
%{_usr}/share/selinux/devel/include/*
%{_usr}/share/selinux/devel/Makefile
%{_usr}/share/selinux/devel/example.*
%{_usr}/share/selinux/devel/policy.*
%ghost %{_sharedstatedir}/sepolgen/interface_info

%post devel
selinuxenabled && %{_bindir}/sepolgen-ifgen 2>/dev/null
exit 0

%package doc
Summary:        SELinux policy documentation
Requires:       selinux-policy = %{version}-%{release}
Requires(pre):  selinux-policy = %{version}-%{release}

%description doc
SELinux policy documentation package

%files doc
%{_mandir}/man*/*
%{_mandir}/ru/*/*
%doc %{_usr}/share/doc/%{name}

%define makeCmds() \
%make_build UNK_PERMS=%{4} NAME=%{1} TYPE=%{2} DISTRO=%{distro} UBAC=n DIRECT_INITRC=%{3} MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024 bare \
%make_build UNK_PERMS=%{4} NAME=%{1} TYPE=%{2} DISTRO=%{distro} UBAC=n DIRECT_INITRC=%{3} MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024 conf
%define installCmds() \
%make_build UNK_PERMS=%{4} NAME=%{1} TYPE=%{2} DISTRO=%{distro} UBAC=n DIRECT_INITRC=%{3} MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024 base.pp \
%make_build validate UNK_PERMS=%{4} NAME=%{1} TYPE=%{2} DISTRO=%{distro} UBAC=n DIRECT_INITRC=%{3} MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024 modules \
make UNK_PERMS=%{4} NAME=%{1} TYPE=%{2} DISTRO=%{distro} UBAC=n DIRECT_INITRC=%{3} MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} MLS_CATS=1024 MCS_CATS=1024 install \
make UNK_PERMS=%{4} NAME=%{1} TYPE=%{2} DISTRO=%{distro} UBAC=n DIRECT_INITRC=%{3} MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} MLS_CATS=1024 MCS_CATS=1024 install-appconfig \
make UNK_PERMS=%{4} NAME=%{1} TYPE=%{2} DISTRO=%{distro} UBAC=n DIRECT_INITRC=%{3} MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} MLS_CATS=1024 MCS_CATS=1024 SEMODULE="semodule -p %{buildroot} -X 100 " load \
mkdir -p %{buildroot}/%{_sysconfdir}/selinux/%{1}/logins \
touch %{buildroot}%{_sysconfdir}/selinux/%{1}/contexts/files/file_contexts.subs \
install -m0644 config/appconfig-%{2}/securetty_types %{buildroot}%{_sysconfdir}/selinux/%{1}/contexts/securetty_types \
install -m0644 config/file_contexts.subs_dist %{buildroot}%{_sysconfdir}/selinux/%{1}/contexts/files \
touch %{buildroot}%{_sysconfdir}/selinux/%{1}/contexts/files/file_contexts.bin \
touch %{buildroot}%{_sysconfdir}/selinux/%{1}/contexts/files/file_contexts.local \
touch %{buildroot}%{_sysconfdir}/selinux/%{1}/contexts/files/file_contexts.local.bin \
rm -f %{buildroot}/%{_usr}/share/selinux/%{1}/*pp*  \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%{1}/contexts/netfilter_contexts  \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%{1}/modules/active/policy.kern \
rm -f %{buildroot}%{_sharedstatedir}/selinux/%{1}/active/*.linked \
%{nil}

%define relabel() \
. %{_sysconfdir}/selinux/config; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%{1}/contexts/files/file_contexts; \
%{_sbindir}/selinuxenabled; \
if [ $? = 0  -a "${SELINUXTYPE}" = %{1} -a -f ${FILE_CONTEXT}.pre ]; then \
     /sbin/fixfiles -C ${FILE_CONTEXT}.pre restore &> /dev/null > /dev/null; \
     rm -f ${FILE_CONTEXT}.pre; \
fi; \
if /sbin/restorecon -e /run/media -R /root %{_var}/log %{_var}/run %{_sysconfdir}/passwd* %{_sysconfdir}/group* %{_sysconfdir}/*shadow* 2> /dev/null;then \
    continue; \
fi;

%define preInstall() \
if [ -s %{_sysconfdir}/selinux/config ]; then \
     . %{_sysconfdir}/selinux/config; \
     FILE_CONTEXT=%{_sysconfdir}/selinux/%{1}/contexts/files/file_contexts; \
     if [ "${SELINUXTYPE}" = %{1} -a -f ${FILE_CONTEXT} ]; then \
        [ -f ${FILE_CONTEXT}.pre ] || cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.pre; \
     fi; \
     touch %{_sysconfdir}/selinux/%{1}/.rebuild; \
fi;

%define postInstall() \
. %{_sysconfdir}/selinux/config; \
if [ -e %{_sysconfdir}/selinux/%{2}/.rebuild ]; then \
   rm %{_sysconfdir}/selinux/%{2}/.rebuild; \
   %{_sbindir}/semodule -B -n -s %{2}; \
fi; \
[ "${SELINUXTYPE}" == "%{2}" ] && selinuxenabled && load_policy; \
if [ %{1} -eq 1 ]; then \
   /sbin/restorecon -R /root %{_var}/log /run %{_sysconfdir}/passwd* %{_sysconfdir}/group* %{_sysconfdir}/*shadow* 2> /dev/null; \
else \
%relabel %{2} \
fi;

%prep
%setup -q -n refpolicy

%install
# Build policy
mkdir -p %{buildroot}%{_sysconfdir}/selinux
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/selinux/config
touch %{buildroot}%{_sysconfdir}/sysconfig/selinux
mkdir -p %{buildroot}%{_usr}/lib/tmpfiles.d/
mkdir -p %{buildroot}%{_bindir}

# Always create policy module package directories
mkdir -p %{buildroot}%{_usr}/share/selinux/refpolicy
mkdir -p %{buildroot}%{_sharedstatedir}/selinux/{refpolicy,modules}/

mkdir -p %{buildroot}%{_usr}/share/selinux/packages

# Install devel
make clean
%makeCmds refpolicy mcs n allow
%installCmds refpolicy mcs n allow

# remove leftovers when save-previous=true (semanage.conf) is used
rm -rf %{buildroot}%{_sharedstatedir}/selinux/refpolicy/previous

mkdir -p %{buildroot}%{_mandir}
cp -R  man/* %{buildroot}%{_mandir}
make UNK_PERMS=allow NAME=refpolicy TYPE=mcs DISTRO=%{distro} UBAC=n DIRECT_INITRC=n MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name} MLS_CATS=1024 MCS_CATS=1024 install-docs
make UNK_PERMS=allow NAME=refpolicy TYPE=mcs DISTRO=%{distro} UBAC=n DIRECT_INITRC=n MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name} MLS_CATS=1024 MCS_CATS=1024 install-headers
mkdir %{buildroot}%{_usr}/share/selinux/devel/
mv %{buildroot}%{_usr}/share/selinux/refpolicy/include %{buildroot}%{_usr}/share/selinux/devel/include
install -m 644 %{SOURCE1} %{buildroot}%{_usr}/share/selinux/devel/Makefile
install -m 644 doc/example.* %{buildroot}%{_usr}/share/selinux/devel/
install -m 644 doc/policy.* %{buildroot}%{_usr}/share/selinux/devel/

%post
if [ ! -s %{_sysconfdir}/selinux/config ]; then
# Permissive by default.  Enforcing support will be added in a later phase
echo "
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=permissive
# SELINUXTYPE= defines the policy to load
#     Currently the only supported option is refpolicy
SELINUXTYPE=refpolicy

" > %{_sysconfdir}/selinux/config

     ln -sf ../selinux/config %{_sysconfdir}/sysconfig/selinux
     restorecon %{_sysconfdir}/selinux/config 2> /dev/null || :
else
     . %{_sysconfdir}/selinux/config
fi
%postInstall $1 repolicy
exit 0

%postun
if [ $1 = 0 ]; then
     setenforce 0 2> /dev/null
     if [ ! -s %{_sysconfdir}/selinux/config ]; then
          echo "SELINUX=disabled" > %{_sysconfdir}/selinux/config
     else
          sed -i 's/^SELINUX=.*/SELINUX=disabled/g' %{_sysconfdir}/selinux/config
     fi
fi
exit 0

%pre
%preInstall refpolicy

%triggerin -- pcre
selinuxenabled && semodule -nB
exit 0
%changelog
* Mon Aug 31 2020 Daniel Burgener <daburgen@microsoft.com> - 2.20200818-1
- Initial CBL-Mariner import from Fedora 31 (license: MIT)
- Heavy modifications to build from upstream reference policy rather than from fedora selinux policy.
  Fedora's policy and versioning tracks their policy fork specificially, whereas this tracks the upstream
  policy that Fedora's policy is based on.
- License verified

* Wed Oct 09 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-37
- Remove duplicate file context for /usr//bin/nova-api-metadata
- Introduce new bolean httpd_use_opencryptoki
- Allow setroubleshoot_fixit_t to read random_device_t
- Label /etc/named direcotory as named_conf_t BZ(1759495)
- Allow dkim to execute sendmail
- Update virt_read_content interface to allow caller domain mmap virt_content_t block devices and files
- Update aide_t domain to allow this tool to analyze also /dev filesystem
- Update interface modutils_read_module_deps to allow caller domain also mmap modules_dep_t files BZ(1758634)
- Allow avahi_t to send msg to xdm_t
- Update dev_manage_sysfs() to support managing also lnk files BZ(1759019)
- Allow systemd_logind_t domain to read blk_files in domain removable_device_t
- Add new interface udev_getattr_rules_chr_files()

* Fri Oct 04 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-36
- Update aide_t domain to allow this tool to analyze also /dev filesystem
- Allow bitlbee_t domain map files in /usr
- Allow stratisd to getattr of fixed disk device nodes
- Add net_broadcast capability to openvswitch_t domain BZ(1716044)
- Allow exim_t to read mysqld conf files if exim_can_connect_db is enabled. BZ(1756973)
- Allow cobblerd_t domain search apache configuration dirs
- Dontaudit NetworkManager_t domain to write to kdump temp pipies BZ(1750428)
- Label /var/log/collectd.log as collectd_log_t
- Allow boltd_t domain to manage sysfs files and dirs BZ(1754360)
- Add fowner capability to the pcp_pmlogger_t domain BZ(1754767)
- networkmanager: allow NetworkManager_t to create bluetooth_socket
- Fix ipa_custodia_stream_connect interface
- Add new interface udev_getattr_rules_chr_files()
- Make dbus-broker service working on s390x arch
- Add new interface dev_mounton_all_device_nodes()
- Add new interface dev_create_all_files()
- Allow systemd(init_t) to load kernel modules
- Allow ldconfig_t domain to manage initrc_tmp_t objects
- Add new interface init_write_initrc_tmp_pipes()
- Add new interface init_manage_script_tmp_files()
- Allow xdm_t setpcap capability in user namespace BZ(1756790)
- Allow xdm_t domain to user netlink_route sockets BZ(1756791)
- Update files_create_var_lib_dirs() interface to allow caller domain also set attributes of var_lib_t directory BZ(1754245)
- Allow sudo userdomain to run rpm related commands
- Add sys_admin capability for ipsec_t domain
- Allow systemd_modules_load_t domain to read systemd pid files
- Add new interface init_read_pid_files()
- Allow systemd labeled as init_t domain to manage faillog_t objects
- Add file context ipsec_var_run_t for /var/run/charon\.dck to ipsec.fc
- Make ipa_custodia policy active
- Make stratisd policy active

* Fri Sep 20 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-35
- Fix ipa_custodia_stream_connect interface
- Allow systemd_modules_load_t domain to read systemd pid files
- Add new interface init_read_pid_files()
- Allow systemd labeled as init_t domain to manage faillog_t objects
- Add file context ipsec_var_run_t for /var/run/charon\.dck to ipsec.fc

* Fri Sep 20 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-34
- Run ipa-custodia as ipa_custodia_t
- Update webalizer_t SELinux policy
- Dontaudit thumb_t domain to getattr of nsfs_t files BZ(1753598)
- Allow rhsmcertd_t domain to read rtas_errd lock files
- Add new interface rtas_errd_read_lock()
- Update allow rules set for nrpe_t domain
- Update timedatex SELinux policy to to sychronizate time with GNOME and add new macro chronyd_service_status to chronyd.if
- Allow avahi_t to send msg to lpr_t
- Label /dev/shm/dirsrv/ with dirsrv_tmpfs_t label
- Allow dlm_controld_t domain to read random device
- Add sys_ptrace capability to pcp_pmlogger_t domain BZ(1751816)
- Allow gssproxy_t domain read state of all processes on system
- Make ipa_custodia policy active
- Make stratisd policy active
- Introduce xdm_manage_bootloader booelan
- Add new macro systemd_timedated_status to systemd.if to get timedated service status
- Allow xdm_t domain to read sssd pid files BZ(1753240)

* Fri Sep 13 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-33
- Add sys_ptrace capability to pcp_pmlogger_t domain BZ(1751816)
- Allow gssproxy_t domain read state of all processes on system
- Update travis-CI file
- Fix syntax erros in keepalived policy
- Add sys_admin capability for keepalived_t labeled processes
- Allow user_mail_domain attribute to manage files labeled as etc_aliases_t.
- Create new type ipmievd_helper_t domain for loading kernel modules.
- Run stratisd service as stratisd_t
- Fix abrt_upload_watch_t in abrt policy
- Update keepalived policy
- Update cron_role, cron_admin_role and cron_unconfined_role to avoid *_t_t types
- Revert "Create admin_crontab_t and admin_crontab_tmp_t types"
- Revert "Update cron_role() template to accept third parameter with SELinux domain prefix"
- Allow amanda_t to manage its var lib files and read random_device_t
- Create admin_crontab_t and admin_crontab_tmp_t types
- Add setgid and setuid capabilities to keepalived_t domain
- Update cron_role() template to accept third parameter with SELinux domain prefix
- Allow psad_t domain to create tcp diag sockets BZ(1750324)
- Allow systemd to mount fwupd_cache_t BZ(1750288)
- Allow chronyc_t domain to append to all non_security files
- Update zebra SELinux policy to make it work also with frr service
- Allow rtkit_daemon_t domain set process nice value in user namespaces BZ(1750024)
- Dontaudit rhsmcertd_t to write to dirs labeled as lib_t BZ(1556763)
- Label /var/run/mysql as mysqld_var_run_t
- Allow chronyd_t domain to manage and create chronyd_tmp_t dirs,files,sock_file objects.
- Update timedatex policy to manage localization
- Allow sandbox_web_type domains to sys_ptrace and sys_chroot in user namespaces
- Update gnome_dontaudit_read_config
- Allow devicekit_var_lib_t dirs to be created by systemd during service startup. BZ(1748997)
- Update travis-CI file
- Allow systemd labeled as init_t domain to remount rootfs filesystem
- Add interface files_remount_rootfs()
- Dontaudit sys_admin capability for iptables_t SELinux domain
- Allow userdomains to dbus chat with policykit daemon
- Update userdomains to pass correct parametes based on updates from cron_*_role interfaces
- New interface files_append_non_security_files()
- Label 2618/tcp and 2618/udp as priority_e_com_port_t
- Label 2616/tcp and 2616/udp as appswitch_emp_port_t
- Label 2615/tcp and 2615/udp as firepower_port_t
- Label 2610/tcp and 2610/udp as versa_tek_port_t
- Label 2613/tcp and 2613/udp as smntubootstrap_port_t
- Label 3784/tcp and 3784/udp as bfd_control_port_t
- Remove rule allowing all processes to stream connect to unconfined domains

* Wed Sep 04 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-32
- Allow zabbix_t domain to manage zabbix_var_lib_t sock files and connect to unix_stream_socket
- Dontaudit sandbox web types to setattr lib_t dirs
- Dontaudit system_mail_t domains to check for existence other applications on system BZ(1747369)
- Allow haproxy_t domain to read network state of system
- Allow processes labeled as keepalived_t domain to get process group
- Introduce dbusd_unit_file_type
- Allow pesign_t domain to read/write named cache files.
- Label /var/log/hawkey.log as rpm_log_t and update rpm named filetrans interfaces.
- Allow httpd_t domain to read/write named_cache_t files
- Add new interface bind_rw_cache()
- Allow cupsd_t domain to create directory with name ppd in dirs labeled as cupsd_etc_t with label cupsd_rw_etc_t.
- Update cpucontrol_t SELinux policy
- Allow pcp_pmcd_t domain to bind on udp port labeled as statsd_port_t
- Run lldpd service as lldpad_t.
- Allow spamd_update_t domain to create unix dgram sockets.
- Update dbus role template for confined users to allow login into x session
- Label /usr/libexec/microcode_ctl/reload_microcode as cpucontrol_exec_t
- Fix typo in networkmanager_append_log() interface
- Update collectd policy to allow daemon create /var/log/collectd with collectd_log_t label
- Allow login user type to use systemd user session
- Allow xdm_t domain to start dbusd services.
- Introduce new type xdm_unit_file_t
- Remove allowing all domain to communicate over pipes with all domain under rpm_transition_domain attribute
- Allow systemd labeled as init_t to remove sockets with tmp_t label BZ(1745632)
- Allow ipsec_t domain to read/write named cache files
- Allow sysadm_t to create hawkey log file with rpm_log_t SELinux label
- Allow domains systemd_networkd_t and systemd_logind_t to chat over dbus
- Label udp 8125 port as statsd_port_t

* Tue Aug 13 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-31
- Update timedatex policy BZ(1734197)

* Tue Aug 13 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-30
- cockpit: Allow cockpit-session to read cockpit-tls state
- Allow zebrat_t domain to read state of NetworkManager_t processes BZ(1739983)
- Allow named_t domain to read/write samba_var_t files BZ(1738794)
- Dontaudit abrt_t domain to read root_t files
- Allow ipa_dnskey_t domain to read kerberos keytab
- Allow mongod_t domain to read cgroup_t files BZ(1739357)
- Update ibacm_t policy
- Allow systemd to relabel all files on system.
- Revert "Add new boolean systemd_can_relabel"
- Allow xdm_t domain to read kernel sysctl BZ(1740385)
- Add sys_admin capability for xdm_t in user namespace. BZ(1740386)
- Allow dbus communications with resolved for DNS lookups
- Add new boolean systemd_can_relabel
- Allow auditd_t domain to create auditd_tmp_t temporary files and dirs in /tmp or /var/tmp
- Label '/var/usrlocal/(.*/)?sbin(/.*)?' as bin_t
- Update systemd_dontaudit_read_unit_files() interface to dontaudit alos listing dirs
- Run lvmdbusd service as lvm_t

* Wed Aug 07 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-29
- Allow dlm_controld_t domain setgid capability
- Fix SELinux modules not installing in chroots.
Resolves: rhbz#1665643

* Tue Aug 06 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-28
- Allow systemd to create and bindmount dirs. BZ(1734831)

* Mon Aug 05 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-27
- Allow tlp domain run tlp in trace mode BZ(1737106)
- Make timedatex_t domain system dbus bus client BZ(1737239)
- Allow cgdcbxd_t domain to list cgroup dirs
- Allow systemd to create and bindmount dirs. BZ(1734831)

* Tue Jul 30 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-26
- New policy for rrdcached
- Allow dhcpd_t domain to read network sysctls.
- Allow nut services to communicate with unconfined domains
- Allow virt_domain to Support ecryptfs home dirs.
- Allow domain transition lsmd_t to sensord_t
- Allow httpd_t to signull mailman_cgi_t process
- Make rrdcached policy active
- Label /etc/sysconfig/ip6?tables\.save as system_conf_t Resolves: rhbz#1733542
- Allow machinectl to run pull-tar BZ(1724247)

* Fri Jul 26 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-25
- Allow spamd_update_t domain to read network state of system BZ(1733172)
- Allow dlm_controld_t domain to transition to the lvm_t
- Allow sandbox_web_client_t domain to do sys_chroot in user namespace
- Allow virtlockd process read virtlockd.conf file
- Add more permissions for session dbus types to make working dbus broker with systemd user sessions
- Allow sssd_t domain to read gnome config and named cache files
- Allow brltty to request to load kernel module
- Add svnserve_tmp_t label forl svnserve temp files to system private tmp
- Allow sssd_t domain to read kernel net sysctls BZ(1732185)
- Run timedatex service as timedatex_t
- Allow mysqld_t domain to domtrans to ifconfig_t domain when executing ifconfig tool
- Allow cyrus work with PrivateTmp
- Make cgdcbxd_t domain working with SELinux enforcing.
- Make working wireshark execute byt confined users staff_t and sysadm_t
- Dontaudit virt_domain to manage ~/.cache dirs BZ(1730963)
- Allow svnserve_t domain to read system state
- allow named_t to map named_cache_t files
- Label user cron spool file with user_cron_spool_t
- Update gnome_role_template() template to allow sysadm_t confined user to login to xsession
- Allow lograte_t domain to manage collect_rw_content files and dirs
- Add interface collectd_manage_rw_content()
- Allow ifconfig_t domain to manage vmware logs
- Remove system_r role from staff_u user.
- Make new timedatex policy module active
- Add systemd_private_tmp_type attribute
- Allow systemd to load kernel modules during boot process.
- Allow sysadm_t and staff_t domains to read wireshark shared memory
- Label /usr/libexec/utempter/utempter  as utemper_exec_t
- Allow ipsec_t domain to read/write  l2tpd pipe BZ(1731197)
- Allow sysadm_t domain to create netlink selinux sockets
- Make cgdcbxd active in Fedora upstream sources

* Wed Jul 17 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-24
- Label user cron spool file with user_cron_spool_t
- Update gnome_role_template() template to allow sysadm_t confined user to login to xsession
- Allow lograte_t domain to manage collect_rw_content files and dirs
- Add interface collectd_manage_rw_content()
- Allow systemd_hostnamed_t domain to dbus chat with sosreport_t domain
- Update  tomcat_can_network_connect_db boolean to allow tomcat domains also connect to redis ports
- Allow mysqld_t domain to manage cluster pid files
- Relabel  /usr/sbin/virtlockd from virt_exec_t to virtlogd_exec_t.
- Allow ptp4l_t domain to write to pmc socket which is created by pmc command line tool
- Allow dkim-milter to send e-mails BZ(1716937)
- Update spamassasin policy to make working /usr/share/spamassassin/sa-update.cron script BZ(1711799)
- Update svnserve_t policy to make working svnserve hooks
- Allow varnishlog_t domain to check for presence of varnishd_t domains
- Update sandboxX policy to make working firefox inside SELinux sandbox
- Remove allow rule from svirt_transition_svirt_sandbox interface to don't allow containers to connect to random services
- Allow httpd_t domain to read /var/lib/softhsm/tokens to allow httpd daemon to use pkcs#11 devices
- Allow gssd_t domain to list tmpfs_t dirs
- Allow mdadm_t domain to read tmpfs_t files
- Allow sbd_t domain to check presence of processes labeled as cluster_t
- Dontaudit httpd_sys_script_t to read systemd unit files
- Allow blkmapd_t domain to read nvme devices
- Update cpucontrol_t domain to make working microcode service
- Allow domain transition from logwatch_t do postfix_postqueue_t
- Allow chronyc_t domain to create and write to non_security files in case when sysadmin is redirecting output to file e.g: 'chronyc -n tracking > /var/lib/test'
- Allow httpd_sys_script_t domain to mmap httpcontent
- Allow sbd_t to manage cgroups_t files
- Update wireshark policy to make working tshar labeled as wireshark_t
- Update virt_use_nfs boolean to allow svirt_t domain to mmap nfs_t files
- Allow sysadm_t domain to create netlink selinux sockets
- Make cgdcbxd active in Fedora upstream sources
- Allow sysadm_t domain to dbus chat with rtkit daemon
- Allow x_userdomains to nnp domain transition to thumb_t domain
- Allow unconfined_domain_type to setattr own process lnk files.
- Add interface files_write_generic_pid_sockets()
- Dontaudit writing to user home dirs by gnome-keyring-daemon
- Allow staff and admin domains to setpcap in user namespace
- Allow staff and sysadm to use lockdev
- Allow staff and sysadm users to run iotop.
- Dontaudit traceroute_t domain require sys_admin capability
- Dontaudit dbus chat between kernel_t and init_t
- Allow systemd labeled as init_t to create mountpoints without any specific label as default_t

* Wed Jul 10 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-23
- Update dbusd policy and netowrkmanager to allow confined users to connect to vpn over NetworkManager
- Fix all interfaces which cannot by compiled because of typos
- Allow X userdomains to mmap user_fonts_cache_t dirs

* Mon Jul 08 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-22
- Label /var/kerberos/krb5 as krb5_keytab_t
- Allow glusterd_t domain to setpgid
- Allow lsmd_t domain to execute /usr/bin/debuginfo-install
- Allow sbd_t domain to manage cgroup dirs
- Allow opafm_t domain to modify scheduling information of another process.
- Allow wireshark_t domain to create netlink netfilter sockets
- Allow gpg_agent_t domain to use nsswitch
- Allow httpd script types to mmap httpd rw content
- Allow dkim_milter_t domain to execute shell BZ(17116937)
- Allow sbd_t domain to use nsswitch
- Allow rhsmcertd_t domain to send signull to all domains
- Allow snort_t domain to create netlink netfilter sockets BZ(1723184)
- Dontaudit blueman to read state of all domains on system BZ(1722696)
- Allow boltd_t domain to use ps and get state of all domains on system. BZ(1723217)
- Allow rtkit_daemon_t to uise sys_ptrace usernamespace capability BZ(1723308)
- Replace "-" by "_" in types names
- Change condor_domain declaration in condor_systemctl
- Allow firewalld_t domain to read iptables_var_run_t files BZ(1722405)
- Allow auditd_t domain to send signals to audisp_remote_t domain
- Allow systemd labeled as init_t domain to read/write faillog_t. BZ(1723132)
- Allow systemd_tmpfiles_t domain to relabel from usermodehelper_t files
- Add interface kernel_relabelfrom_usermodehelper()
- Dontaudit unpriv_userdomain to manage boot_t files
- Allow xdm_t domain to mmap /var/lib/gdm/.cache/fontconfig BZ(1725509)
- Allow systemd to execute bootloader grub2-set-bootflag BZ(1722531)
- Allow associate efivarfs_t on sysfs_t

* Tue Jun 18 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-21
- Add vnstatd_var_lib_t to mountpoint attribute BZ(1648864)
- cockpit: Support split-out TLS proxy
- Allow dkim_milter_t to use shell BZ(1716937)
- Create explicit fc rule for mailman executable BZ(1666004)
- Update interface networkmanager_manage_pid_files() to allow manage also dirs
- Allow dhcpd_t domain to mmap dnssec_t files BZ(1718701)
- Add new interface bind_map_dnssec_keys()
- Update virt_use_nfs() boolean to allow virt_t to mmap nfs_t files
- Allow redis_t domain to read public sssd files
- Allow fetchmail_t to connect to dovecot stream sockets BZ(1715569)
- Allow confined users to login via cockpit
- Allow nfsd_t domain to do chroot becasue of new version of nfsd
- Add gpg_agent_roles to system_r roles
- Allow qpidd_t domain to getattr all fs_t filesystem and mmap usr_t files
- Allow rhsmcertd_t domain to manage rpm cache
- Allow sbd_t domain to read tmpfs_t symlinks
- Allow ctdb_t domain to manage samba_var_t files/links/sockets and dirs
- Allow kadmind_t domain to read home config data
- Allow sbd_t domain to readwrite cgroups
- Allow NetworkManager_t domain to read nsfs_t files BZ(1715597)
- Label /var/log/pacemaker/pacemaker as cluster_var_log_t
- Allow certmonger_t domain to manage named cache files/dirs
- Allow pcp_pmcd_t domain to domtrans to mdadm_t domain BZ(1714800)
- Allow crack_t domain read /et/passwd files
- Label fontconfig cache and config files and directories BZ(1659905)
- Allow dhcpc_t domain to manage network manager pid files
- Label /usr/sbin/nft as iptables_exec_t
- Allow userdomain attribute to manage cockpit_ws_t stream sockets
- Allow ssh_agent_type to read/write cockpit_session_t unnamed pipes
- Add interface ssh_agent_signal()

* Thu May 30 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-20
- Allow pcp_pmcd_t domain to domtrans to mdadm_t domain BZ(1714800)
- Allow spamd_update_t to exec itsef
- Fix broken logwatch SELinux module
- Allow logwatch_mail_t to manage logwatch cache files/dirs
- Update wireshark_t domain to use several sockets
- Allow sysctl_rpc_t and sysctl_irq_t to be stored on fs_t

* Mon May 27 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-19
- Fix bind_read_cache() interface to allow only read perms to caller domains
- [speech-dispatcher.if] m4 macro names can not have - in them
- Grant varnishlog_t access to varnishd_etc_t
- Allow nrpe_t domain to read process state of systemd_logind_t
- Allow mongod_t domain to connect on https port BZ(1711922)
- Allow chronyc_t domain to create own tmpfiles and allow communicate send data over unix dgram sockets
- Dontaudit spamd_update_t domain to read all domains states BZ(1711799)
- Allow pcp_pmie_t domain to use sys_ptrace usernamespace cap BZ(1705871)
- Allow userdomains to send data over dgram sockets to userdomains dbus services BZ(1710119)
- Revert "Allow userdomains to send data over dgram sockets to userdomains dbus services BZ(1710119)"
- Make boinc_var_lib_t mountpoint BZ(1711682)
- Allow wireshark_t domain to create fifo temp files
- All NetworkManager_ssh_t rules have to be in same optional block with ssh_basic_client_template(), fixing this bug in NetworkManager policy
- Allow dbus chat between NetworkManager_t and NetworkManager_ssh_t domains. BZ(1677484)
- Fix typo in gpg SELinux module
- Update gpg policy to make ti working with confined users
- Add domain transition that systemd labeled as init_t can execute spamd_update_exec_t binary to run newly created process as spamd_update_t
- Remove allow rule for virt_qemu_ga_t to write/append user_tmp_t files
- Label /var/run/user/*/dbus-1 as session_dbusd_tmp_t
- Add dac_override capability to namespace_init_t domain
- Label /usr/sbin/corosync-qdevice as cluster_exec_t
- Allow NetworkManager_ssh_t domain to open communication channel with system dbus. BZ(1677484)
- Label /usr/libexec/dnf-utils as debuginfo_exec_t
- Alow nrpe_t to send signull to sssd domain when nagios_run_sudo boolean is turned on
- Allow nrpe_t domain to be dbus cliennt
- Add interface sssd_signull()
- Build in parallel on Travis
- Fix parallel build of the policy
- Revert "Make able deply overcloud via neutron_t to label nsfs as fs_t"
- Add interface systemd_logind_read_state()
- Fix find commands in Makefiles
- Allow systemd-timesyncd to read network state BZ(1694272)
- Update userdomains to allow confined users to create gpg keys
- Allow associate all filesystem_types with fs_t
- Dontaudit syslogd_t using kill in unamespaces BZ(1711122)
- Allow init_t to manage session_dbusd_tmp_t dirs
- Allow systemd_gpt_generator_t to read/write to clearance
- Allow su_domain_type to getattr to /dev/gpmctl
- Update userdom_login_user_template() template to make working systemd user session for guest and xguest SELinux users

* Fri May 17 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-18
- Fix typo in gpg SELinux module
- Update gpg policy to make ti working with confined users
- Add domain transition that systemd labeled as init_t can execute spamd_update_exec_t binary to run newly created process as spamd_update_t
- Remove allow rule for virt_qemu_ga_t to write/append user_tmp_t files
- Label /var/run/user/*/dbus-1 as session_dbusd_tmp_t
- Add dac_override capability to namespace_init_t domain
- Label /usr/sbin/corosync-qdevice as cluster_exec_t
- Allow NetworkManager_ssh_t domain to open communication channel with system dbus. BZ(1677484)
- Label /usr/libexec/dnf-utils as debuginfo_exec_t
- Alow nrpe_t to send signull to sssd domain when nagios_run_sudo boolean is turned on
- Allow nrpe_t domain to be dbus cliennt
- Add interface sssd_signull()
- Label /usr/bin/tshark as wireshark_exec_t
- Update userdomains to allow confined users to create gpg keys
- Allow associate all filesystem_types with fs_t
- Dontaudit syslogd_t using kill in unamespaces BZ(1711122)
- Allow init_t to manage session_dbusd_tmp_t dirs
- Allow systemd_gpt_generator_t to read/write to clearance
- Allow su_domain_type to getattr to /dev/gpmctl
- Update userdom_login_user_template() template to make working systemd user session for guest and xguest SELinux users

* Fri May 17 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-17
- Alow nrpe_t to send signull to sssd domain when nagios_run_sudo boolean is turned on
- Allow nrpe_t domain to be dbus cliennt
- Add interface sssd_signull()
- Label /usr/bin/tshark as wireshark_exec_t
- Fix typo in dbus_role_template()
- Allow userdomains to send data over dgram sockets to userdomains dbus services BZ(1710119)
- Allow userdomains dbus domain to execute dbus broker. BZ(1710113)
- Allow dovedot_deliver_t setuid/setgid capabilities BZ(1709572)
- Allow virt domains to access xserver devices BZ(1705685)
- Allow aide to be executed by systemd with correct (aide_t) domain BZ(1648512)
- Dontaudit svirt_tcg_t domain to read process state of libvirt BZ(1594598)
- Allow pcp_pmie_t domain to use fsetid capability BZ(1708082)
- Allow pcp_pmlogger_t to use setrlimit BZ(1708951)
- Allow gpsd_t domain to read udev db BZ(1709025)
- Add sys_ptrace capaiblity for  namespace_init_t domain
- Allow systemd to execute sa-update in spamd_update_t domain BZ(1705331)
- Allow rhsmcertd_t domain to read rpm cache files
- Label /efi same as /boot/efi boot_t BZ(1571962)
- Allow transition from udev_t to tlp_t BZ(1705246)
- Remove initrc_exec_t for /usr/sbin/apachectl file

* Fri May 03 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-16
- Add fcontext for apachectl util to fix missing output when executed "httpd -t" from this script.

* Thu May 02 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-15
- Allow iscsid_t domain to mmap modules_dep_t files
- Allow ngaios to use chown capability
- Dontaudit gpg_domain to create netlink_audit sockets
- Remove role transition in rpm_run() interface to allow sysadm_r jump to rpm_t type. BZ(1704251)
- Allow dirsrv_t domain to execute own tmp files BZ(1703111)
- Update fs_rw_cephfs_files() interface to allow also caller domain to read/write cephpfs_t lnk files
- Update domain_can_mmap_files() boolean to allow also mmap lnk files
- Improve userdom interfaces to drop guest_u SELinux user to use nsswitch

* Fri Apr 26 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-14
- Allow transition from cockpit_session to unpriv user domains

* Thu Apr 25 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-13
- Introduce deny_bluetooth boolean
- Allow greylist_milter_t to read network system state BZ(1702672)
- Allow freeipmi domains to mmap freeipmi_var_cache_t files
- Allow rhsmcertd_t and rpm_t domains to chat over dbus
- Allow thumb_t domain to delete cache_home_t files BZ(1701643)
- Update gnome_role_template() to allow _gkeyringd_t domains to chat with systemd_logind over dbus
- Add new interface boltd_dbus_chat()
- Allow fwupd_t and modemmanager_t domains to communicate over dbus BZ(1701791)
- Allow keepalived_t domain to create and use netlink_connector sockets BZ(1701750)
- Allow cockpit_ws_t domain to set limits BZ(1701703)
- Update Nagios policy when sudo is used
- Deamon rhsmcertd is able to install certs for docker again
- Introduce deny_bluetooth boolean
- Don't allow a container to connect to random services
- Remove file context /usr/share/spamassassin/sa-update\.cron -> bin_t to label sa-update.cron as spamd_update_exec_t.
- Allow systemd_logind_t and systemd_resolved_t domains to chat over dbus
- Allow unconfined_t to use bpf tools
- Allow x_userdomains to communicate with boltd daemon over dbus

* Fri Apr 19 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-12
- Fix typo in cups SELinux policy
- Allow iscsid_t to read modules deps BZ(1700245)
- Allow cups_pdf_t domain to create cupsd_log_t dirs in /var/log BZ(1700442)
- Allow httpd_rotatelogs_t to execute generic binaries
- Update system_dbus policy because of dbus-broker-20-2
- Allow httpd_t doman to read/write /dev/zero device  BZ(1700758)
- Allow tlp_t domain to read module deps files BZ(1699459)
- Add file context for /usr/lib/dotnet/dotnet
- Update dev_rw_zero() interface by adding map permission
- Allow bounded transition for executing init scripts

* Fri Apr 12 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-11
- Allow mongod_t domain to lsearch in cgroups BZ(1698743)
- Allow rngd communication with pcscd BZ(1679217)
- Create cockpit_tmpfs_t and allow cockpit ws and session to use it BZ(1698405)
- Fix broken networkmanager interface for allowing manage lib files for dnsmasq_t.
- Update logging_send_audit_msgs(sudodomain() to control TTY auditing for netlink socket for audit service

* Tue Apr 09 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-10
- Allow systemd_modules_load to read modules_dep_t files
- Allow systemd labeled as init_t to setattr on unallocated ttys BZ(1697667)

* Mon Apr 08 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-9
- Merge #18 `Add check for config file consistency`
- Allow tlp_t domain also write to nvme_devices block devices BZ(1696943)
- Fix typo in rhsmcertd SELinux module
- Allow dnsmasq_t domain to manage NetworkManager_var_lib_t files
- Allow rhsmcertd_t domain to read yum.log file labeled as rpm_log_t
- Allow unconfined users to use vsock unlabeled sockets
- Add interface kernel_rw_unlabeled_vsock_socket()
- Allow unconfined users to use smc unlabeled sockets
- Add interface kernel_rw_unlabeled_smc_socket
- Allow systemd_resolved_t domain to read system network state BZ(1697039)
- Allow systemd to mounton kernel sysctls BZ(1696201)
- Add interface kernel_mounton_kernel_sysctl() BZ(1696201)
- Allow systemd to mounton several systemd direstory to increase security of systemd Resolves: rhbz#1696201

* Fri Apr 05 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-8
- Allow systemd to mounton several systemd direstory to increase security of systemd
Resolves: rhbz#1696201

* Wed Apr 03 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-7
- Allow fontconfig file transition for xguest_u user
- Add gnome_filetrans_fontconfig_home_content interface
- Add permissions needed by systemd's machinectl shell/login
- Update SELinux policy for xen services
- Add dac_override capability for kdumpctl_t process domain
- Allow chronyd_t domain to exec shell
- Fix varnisncsa typo
- Allow init start freenx-server BZ(1678025)
- Create logrotate_use_fusefs boolean
- Add tcpd_wrapped_domain for telnetd BZ(1676940)
- Allow tcpd bind to services ports BZ(1676940)
- Update mysql_filetrans_named_content() to allow cluster to create mysql dirs in /var/run with proper label mysqld_var_run_t
- Make shell_exec_t type as entrypoint for vmtools_unconfined_t.
- Merge branch 'rawhide' of github.com:fedora-selinux/selinux-policy-contrib into rawhide
- Allow virtlogd_t domain to create virt_etc_rw_t files in virt_etc_t
- Allow esmtp access .esmtprc BZ(1691149)
- Merge branch 'rawhide' of github.com:fedora-selinux/selinux-policy-contrib into rawhide
- Allow tlp_t domain to read nvme block devices BZ(1692154)
- Add support for smart card authentication in cockpit BZ(1690444)
- Add permissions needed by systemd's machinectl shell/login
- Allow kmod_t domain to mmap modules_dep_t files.
- Allow systemd_machined_t dac_override capability BZ(1670787)
- Update modutils_read_module_deps_files() interface to also allow mmap module_deps_t files
- Allow unconfined_domain_type to use bpf tools BZ(1694115)
- Revert "Allow unconfined_domain_type to use bpf tools BZ(1694115)"
- Merge branch 'rawhide' of github.com:fedora-selinux/selinux-policy into rawhide
- Allow unconfined_domain_type to use bpf tools BZ(1694115)
- Allow init_t read mnt_t symlinks BZ(1637070)
- Update dev_filetrans_all_named_dev() interface
- Allow xdm_t domain to execmod temp files BZ(1686675)
- Revert "Allow xdm_t domain to create own tmp files BZ(1686675)"
- Allow getty_t, local_login_t, chkpwd_t and passwd_t to use usbttys. BZ(1691582)
- Allow confined users labeled as staff_t to run iptables.
- Merge branch 'rawhide' of github.com:fedora-selinux/selinux-policy into rawhide
- Allow xdm_t domain to create own tmp files BZ(1686675)
- Add miscfiles_dontaudit_map_generic_certs interface.

* Sat Mar 23 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-6
- Allow boltd_t domain to write to sysfs_t dirs BZ(1689287)
- Allow fail2ban execute journalctl BZ(1689034)
- Update sudodomains to make working confined users run sudo/su
- Introduce new boolean unconfined_dyntrans_all.
- Allow iptables_t domain to read NetworkManager state BZ(1690881)

* Tue Mar 19 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-5
- Update xen SELinux module
- Improve labeling for PCP plugins
- Allow varnishd_t domain to read sysfs_t files
- Update vmtools policy
- Allow virt_qemu_ga_t domain to read udev_var_run_t files
- Update nagios_run_sudo boolean with few allow rules related to accessing sssd
- Update file context for modutils rhbz#1689975
- Label /dev/xen/hypercall and /dev/xen/xenbus_backend as xen_device_t Resolves: rhbz#1679293
- Grant permissions for onloadfs files of all classes.
- Allow all domains to send dbus msgs to vmtools_unconfined_t processes
- Label /dev/pkey as crypt_device_t
- Allow sudodomains to write to systemd_logind_sessions_t pipes.
- Label /usr/lib64/libcuda.so.XX.XX library as textrel_shlib_t.

* Tue Mar 12 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-4
- Update vmtools policy
- Allow virt_qemu_ga_t domain to read udev_var_run_t files
- Update nagios_run_sudo boolean with few allow rules related to accessing sssd
- Update travis CI to install selinux-policy dependencies without checking for gpg check
- Allow journalctl_t domain to mmap syslogd_var_run_t files
- Allow smokeping process to mmap own var lib files and allow set process group. Resolves: rhbz#1661046
- Allow sbd_t domain to bypass permission checks for sending signals
- Allow sbd_t domain read/write all sysctls
- Allow kpatch_t domain to communicate with policykit_t domsin over dbus
- Allow boltd_t to stream connect to sytem dbus
- Allow zabbix_t domain to create sockets labeled as zabbix_var_run_t BZ(1683820)
- Allow all domains to send dbus msgs to vmtools_unconfined_t processes
- Label /dev/pkey as crypt_device_t
- Allow sudodomains to write to systemd_logind_sessions_t pipes.
- Label /usr/lib64/libcuda.so.XX.XX library as textrel_shlib_t.
- Allow ifconfig_t domain to read /dev/random BZ(1687516)
- Fix interface modutils_run_kmod() where was used old interface modutils_domtrans_insmod instead of new one modutils_domtrans_kmod() Resolves: rhbz#1686660
- Update travis CI to install selinux-policy dependencies without checking for gpg check
- Label /usr/sbin/nodm as xdm_exec_t same as other display managers
- Update userdom_admin_user_template() and init_prog_run_bpf() interfaces to make working bpftool for confined admin
- Label /usr/sbin/e2mmpstatus as fsadm_exec_t Resolves: rhbz#1684221
- Update unconfined_dbus_send() interface to allow both direction communication over dbus with unconfined process.

* Wed Feb 27 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-3
- Reverting https://src.fedoraproject.org/rpms/selinux-policy/pull-request/15 because "%pretrans" cannot use shell scripts.
Resolves: rhbz#1683365

* Tue Feb 26 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-2
- Merge insmod_t, depmod_t and update_modules_t do kmod_t

* Mon Feb 25 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.4-1
- Allow openvpn_t domain to set capability BZ(1680276)
- Update redis_enable_notify() boolean to fix sending e-mail by redis when this boolean is turned on
- Allow chronyd_t domain to send data over dgram socket
- Add rolekit_dgram_send() interface
- Fix bug in userdom_restricted_xwindows_user_template() template to disallow all user domains to access admin_home_t - kernel/files.fc: Label /var/run/motd.d(./*)? and /var/run/motd as pam_var_run_t

* Thu Feb 14 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-22
- Allow dovecot_t domain to connect to mysql db
- Add dac_override capability for sbd_t SELinux domain
- Add dac_override capability for  spamd_update_t domain
- Allow nnp transition for domains fsadm_t, lvm_t and mount_t - Add fs_manage_fusefs_named_pipes interface

* Tue Feb 12 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-21
- Allow glusterd_t to write to automount unnamed pipe Resolves: rhbz#1674243
- Allow ddclient_t to setcap Resolves: rhbz#1674298
- Add dac_override capability to vpnc_t domain
- Add dac_override capability to spamd_t domain
- Allow ibacm_t domain to read system state and label all ibacm sockets and symlinks as ibacm_var_run_t in /var/run
- Allow read network state of system for processes labeled as ibacm_t
- Allow ibacm_t domain to send dgram sockets to kernel processes
- Allow dovecot_t to connect to MySQL UNIX socket
- Fix CI for use on forks
- Fix typo bug in sensord policy
- Update ibacm_t policy after testing lastest version of this component
- Allow sensord_t domain to mmap own log files
- Allow virt_doamin to read/write dev device
- Add dac_override capability for ipa_helper_t
- Update policy with multiple allow rules to make working installing VM in MLS policy
- Allow syslogd_t domain to send null signal to all domains on system Resolves: rhbz#1673847 - Merge branch 'rawhide' of github.com:fedora-selinux/selinux-policy into rawhide - Allow systemd-logind daemon to remove shared memory during logout Resolves: rhbz#1674172 - Always label /home symlinks as home_root_t - Update mount_read_pid_files macro to allow also list mount_var_run_t dirs - Fix typo bug in userdomain SELinux policy - Merge branch 'rawhide' of github.com:fedora-selinux/selinux-policy into rawhide - Allow user domains to stop systemd user sessions during logout process - Fix CI for use on forks - Label /dev/sev char device as sev_device_t - Add s_manage_fusefs_named_sockets interface - Allow systemd-journald to receive messages including a memfd

* Sat Feb 02 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-20
- Allow sensord_t domain to use nsswitch and execute shell
- Allow opafm_t domain to execute lib_t files
- Allow opafm_t domain to manage kdump_crash_t files and dirs
- Allow virt domains to read/write cephfs filesystems
- Allow virtual machine to write to fixed_disk_device_t
- Update kdump_manage_crash() interface to allow also manage dirs by caller domain Resolves: rhbz#1491585
- Allow svnserve_t domain to create in /tmp svn_0 file labeled as krb5_host_rcache_t
- Allow vhostmd_t read libvirt configuration files
- Update dbus_role_template interface to allow userdomains to accept data from userdomain dbus domains
- Add miscfiles_filetrans_named_content_letsencrypt() to optional_block - Allow unconfined domains to create letsencrypt directory in /var/lib labeled as cert_t - Allow staff_t user to systemctl iptables units. - Allow systemd to read selinux logind config - obj_perm_sets.spt: Add xdp_socket to socket_class_set. - Add xdp_socket security class and access vectors - Allow transition from init_t domain to user_t domain during ssh login with confined user user_u

* Tue Jan 29 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-19
- Add new xdp_socket class
- Update dbus_role_template interface to allow userdomains to accept data from userdomain dbus domains
- Allow boltd_t domain to read cache_home_t files BZ(1669911)
- Allow winbind_t domain to check for existence of processes labeled as systemd_hostnamed_t BZ(1669912)
- Allow gpg_agent_t to create own tmpfs dirs and sockets
- Allow openvpn_t domain to manage vpnc pidfiles BZ(1667572)
- Add multiple interfaces for vpnc interface file
- Label /var/run/fcgiwrap dir as httpd_var_run_t BZ(1655702)
- In MongoDB 3.4.16, 3.6.6, 4.0.0 and later, mongod reads netstat info from proc and stores it in its diagnostic system (FTDC). See: https://jira.mongodb.org/browse/SERVER-31400 This means that we need to adjust the policy so that the mongod process is allowed to open and read /proc/net/netstat, which typically has symlinks (e.g. /proc/net/snmp).
- Allow gssd_t domain to manage kernel keyrings of every domain.
- Revert "Allow gssd_t domain to read/write kernel keyrings of every domain."
- Allow plymouthd_t search efivarfs directory BZ(1664143)

* Tue Jan 15 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-18
- Allow plymouthd_t search efivarfs directory BZ(1664143)
- Allow arpwatch send e-mail notifications BZ(1657327)
- Allow tangd_t domain to bind on tcp ports labeled as tangd_port_t
- Allow gssd_t domain to read/write kernel keyrings of every domain.
- Allow systemd_timedated_t domain nnp_transition BZ(1666222)
- Add the fs_search_efivarfs_dir interface
- Create tangd_port_t with default label tcp/7406
- Add interface domain_rw_all_domains_keyrings()
- Some of the selinux-policy macros doesn't work in chroots/initial installs. BZ(1665643)

* Fri Jan 11 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-17
- Allow staff_t domain to read read_binfmt_misc filesystem
- Add interface fs_read_binfmt_misc()
- Revert "Allow staff_t to rw binfmt_misc_fs_t files BZ(1658975)"

* Fri Jan 11 2019 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-16
- Allow sensord_t to execute own binary files
- Allow pcp_pmlogger_t domain to getattr all filesystem BZ(1662432)
- Allow virtd_lxc_t domains use BPF BZ(1662613)
- Allow openvpn_t domain to read systemd state BZ(1661065)
- Dontaudit ptrace all domains for blueman_t BZ(1653671)
- Used correct renamed interface for imapd_t domain
- Change label of /usr/libexec/lm_sensors/sensord-service-wrapper from lsmd_exec_t to sensord_exec_t BZ(1662922)
- Allow hddtemp_t domain to read nvme block devices BZ(1663579)
- Add dac_override capability to spamd_t domain BZ(1645667)
- Allow pcp_pmlogger_t to mount tracefs_t filesystem BZ(1662983)
- Allow pcp_pmlogger_t domain to read al sysctls BZ(1662441)
- Specify recipients that will be notified about build CI results.
- Allow saslauthd_t domain to mmap own pid files BZ(1653024)
- Add dac_override capability for snapperd_t domain BZ(1619356)
- Make kpatch_t domain application domain to allow users to execute kpatch in kpatch_t domain.
- Add ipc_owner capability to pcp_pmcd_t domain BZ(1655282)
- Update pulseaudio_stream_connect() to allow caller domain create stream sockets to cumminicate with pulseaudio
- Allow pcp_pmlogger_t domain to send signals to rpm_script_t BZ(1651030)
- Add new interface: rpm_script_signal()
- Allow init_t domain to mmap init_var_lib_t files and dontaudit leaked fd. BZ(1651008)
- Make workin: systemd-run --system --pty bash BZ(1647162)
- Allow ipsec_t domain dbus chat with systemd_resolved_t BZ(1662443)
- Allow staff_t to rw binfmt_misc_fs_t files BZ(1658975)
- Specify recipients that will be notified about build CI results.
- Label /usr/lib/systemd/user as systemd_unit_file_t BZ(1652814)
- Allow sysadm_t,staff_t and unconfined_t domain to execute kpatch as kpatch_t domain
- Add rules to allow systemd to mounton systemd_timedated_var_lib_t.
- Allow x_userdomains to stream connect to pulseaudio BZ(1658286)

* Sun Dec 16 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-15
- Add macro-expander script to selinux-policy-devel package

* Thu Dec 06 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-14
- Remove all ganesha bits from gluster and rpc policy
- Label /usr/share/spamassassin/sa-update.cron as spamd_update_exec_t
- Add dac_override capability to ssad_t domains
- Allow pesign_t domain to read gnome home configs
- Label /usr/libexec/lm_sensors/sensord-service-wrapper as lsmd_exec_t
- Allow rngd_t domains read kernel state
- Allow certmonger_t domains to read bind cache
- Allow ypbind_t domain to stream connect to sssd
- Allow rngd_t domain to setsched
- Allow sanlock_t domain to read/write sysfs_t files
- Add dac_override capability to postfix_local_t domain
- Allow ypbind_t to search sssd_var_lib_t dirs
- Allow virt_qemu_ga_t domain to write to user_tmp_t files
- Allow systemd_logind_t to dbus chat with virt_qemu_ga_t
- Update sssd_manage_lib_files() interface to allow also mmap sssd_var_lib_t files
- Add new interface sssd_signal()
- Update xserver_filetrans_home_content() and xserver_filetrans_admin_home_content() unterfaces to allow caller domain to create .vnc dir in users homedir labeled as xdm_home_t
- Update logging_filetrans_named_content() to allow caller domains of this interface to create /var/log/journal/remote directory labeled as var_log_t
- Add sys_resource capability to the systemd_passwd_agent_t domain
- Allow ipsec_t domains to read bind cache
- kernel/files.fc: Label /run/motd as etc_t
- Allow systemd to stream connect to userdomain processes
- Label /var/lib/private/systemd/ as init_var_lib_t
- Allow initrc_t domain to create new socket labeled as init_T
- Allow audisp_remote_t domain remote logging client to read local audit events from relevant socket.
- Add tracefs_t type to mountpoint attribute
- Allow useradd_t and groupadd_t domains to send signals to sssd_t
- Allow systemd_logind_t domain to remove directories labeled as tmpfs_t BZ(1648636)
- Allow useradd_t and groupadd_t domains to access sssd files because of the new feature in shadow-utils

* Wed Nov 07 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-13
- Update pesign policy to allow pesign_t domain to read bind cache files/dirs
- Add dac_override capability to mdadm_t domain
- Create ibacm_tmpfs_t type for the ibacm policy
- Dontaudit capability sys_admin for dhcpd_t domain
- Makes rhsmcertd_t domain an exception to the constraint preventing changing the user identity in object contexts.
- Allow abrt_t domain to mmap generic tmp_t files
- Label /usr/sbin/wpa_cli as wpa_cli_exec_t
- Allow sandbox_xserver_t domain write to user_tmp_t files
- Allow certutil running as ipsec_mgmt_t domain to mmap ipsec_mgmt pid files Dontaudit ipsec_mgmt_t domain to write to the all mountpoints
- Add interface files_map_generic_tmp_files()
- Add dac_override capability to the syslogd_t domain
- Create systemd_timedated_var_run_t label
- Update systemd_timedated_t domain to allow create own pid files/access init_var_lib_t files and read dbus files BZ(1646202)
- Add init_read_var_lib_lnk_files and init_read_var_lib_sock_files interfaces

* Sun Nov 04 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-12
- Dontaudit thumb_t domain to setattr on lib_t dirs BZ(1643672)
- Dontaudit cupsd_t domain to setattr lib_t dirs BZ(1636766)
- Add dac_override capability to postgrey_t domain BZ(1638954)
- Allow thumb_t domain to execute own tmpfs files BZ(1643698)
- Allow xdm_t domain to manage dosfs_t files BZ(1645770)
- Label systemd-timesyncd binary as systemd_timedated_exec_t to make it run in systemd_timedated_t domain BZ(1640801)
- Improve fs_manage_ecryptfs_files to allow caller domain also mmap ecryptfs_t files BZ(1630675)
- Label systemd-user-runtime-dir binary as systemd_logind_exec_t BZ(1644313)

* Sun Nov 04 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-11
- Add nnp transition rule for vnstatd_t domain using NoNewPrivileges systemd feature BZ(1643063)
- Allow l2tpd_t domain to mmap /etc/passwd file BZ(1638948)
- Add dac_override capability to ftpd_t domain
- Allow gpg_t to create own tmpfs dirs and sockets
- Allow rhsmcertd_t domain to relabel cert_t files
- Add SELinux policy for kpatch
- Allow nova_t domain to use pam
- sysstat: grant sysstat_t the search_dir_perms set
- Label systemd-user-runtime-dir binary as systemd_logind_exec_t BZ(1644313)
- Allow systemd_logind_t to read fixed dist device BZ(1645631)
- Allow systemd_logind_t domain to read nvme devices BZ(1645567)
- Allow systemd_rfkill_t domain to comunicate via dgram sockets with syslogd BZ(1638981)
- kernel/files.fc: Label /run/motd.d(/.*)? as etc_t
- Allow ipsec_mgmt_t process to send signals other than SIGKILL, SIGSTOP, or SIGCHLD to the ipsec_t domains BZ(1638949)
- Allow X display manager to check status and reload services which are part of x_domain attribute
- Add interface miscfiles_relabel_generic_cert()
- Make kpatch policy active
- Fix userdom_write_user_tmp_dirs() to allow caller domain also read/write user_tmp_t dirs
- Dontaudit sys_admin capability for netutils_t domain
- Label tcp and udp ports 2611 as qpasa_agent_port_t

* Tue Oct 16 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-10
- Allow boltd_t domain to dbus chat with fwupd_t domain BZ(1633786)

* Mon Oct 15 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-9
- Allow caller domains using cron_*_role to have entrypoint permission on system_cron_spool_t files BZ(1625645)
- Add interface cron_system_spool_entrypoint()
- Bolt added d-bus API for force-powering the thunderbolt controller, so system-dbusd needs acces to boltd pipes BZ(1637676)
- Add interfaces for boltd SELinux module
- Add dac_override capability to modemmanager_t domain BZ(1636608)
- Allow systemd to mount boltd_var_run_t dirs BZ(1636823)
- Label correctly /var/named/chroot*/dev/unrandom in bind chroot.

* Sat Oct 13 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-8
- ejabberd SELinux module removed, it's shipped by ejabberd-selinux package

* Sat Oct 13 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-7
- Update rpm macros for selinux policy from sources repository: https://github.com/fedora-selinux/selinux-policy-macros

* Tue Oct 09 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-6
- Allow boltd_t to be activated by init socket activation
- Allow virt_domain to read/write to virtd_t unix_stream socket because of new version of libvirt 4.4. BZ(1635803)
- Update SELinux policy for libreswan based on the latest rebase 3.26
- Fix typo in init_named_socket_activation interface

* Thu Oct 04 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-5
- Allow dictd_t domain to mmap dictd_var_lib_t files BZ(1634650)
- Fix typo in boltd.te policy
- Allow fail2ban_t domain to mmap journal
- Add kill capability to named_t domain
- Allow neutron domain to read/write /var/run/utmp
- Create boltd_var_run_t type for boltd pid files
- Allow tomcat_domain to read /dev/random
- Allow neutron_t domain to use pam
- Add the port used by nsca (Nagios Service Check Acceptor)

* Mon Sep 24 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-4
- Update sources to include SELinux policy for containers

* Thu Sep 20 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-3
- Allow certmonger to manage cockpit_var_run_t pid files
- Allow cockpit_ws_t domain to manage cockpit services
- Allow dirsrvadmin_script_t domain to list httpd_tmp_t dirs
- Add interface apache_read_tmp_dirs()
- Fix typo in cockpit interfaces we have cockpit_var_run_t files not cockpit_var_pid_t
- Add interface apcupsd_read_power_files()
- Allow systemd labeled as init_t to execute logrotate in logrotate_t domain
- Allow dac_override capability to amanda_t domain
- Allow geoclue_t domain to get attributes of fs_t filesystems
- Update selinux policy for rhnsd_t domain based on changes in spacewalk-2.8-client
- Allow cockpit_t domain to read systemd state
- Allow abrt_t domain to write to usr_t files
- Allow cockpit to create motd file in /var/run/cockpit
- Label /usr/sbin/pcsd as cluster_exec_t
- Allow pesign_t domain to getattr all fs
- Allow tomcat servers to manage usr_t files
- Dontaudit tomcat serves to append to /dev/random device
- Allow dirsrvadmin_script_t domain to read httpd tmp files
- Allow sbd_t domain to getattr of all char files in /dev and read sysfs_t files and dirs
- Fix path where are sources for CI
- Revert "Allow firewalld_t domain to read random device"
- Add travis CI for selinux-policy-contrib repo
- Allow postfix domains to mmap system db files
- Allow geoclue_t domain to execute own tmp files
- Update ibacm_read_pid_files interface to allow also reading link files
- Allow zebra_t domain to create packet_sockets
- Allow opafm_t domain to list sysfs
- Label /usr/libexec/cyrus-imapd/cyrus-master as cyris_exec_t
- Allow tomcat Tomcat to delete a temporary file used when compiling class files for JSPs.
- Allow chronyd_t domain to read virt_var_lib_t files
- Allow systemd to read apcupsd power files
- Revert "Allow polydomain to create /tmp-inst labeled as tmp_t"
- Allow polydomain to create /tmp-inst labeled as tmp_t
- Allow polydomain to create /tmp-inst labeled as tmp_t
- Allow systemd_resolved_t domain to bind on udp howl port
- Add new boolean use_virtualbox Resolves: rhbz#1510478
- Allow sshd_t domain to read cockpit pid files
- Allow syslogd_t domain to manage cert_t files
- Fix path where are sources for CI
- Add travis.yml to to create CI for selinux-policy sources
- Allow getattr as part of files_mounton_kernel_symbol_table.
- Fix typo "aduit" -> "audit"
- Revert "Add new interface dev_map_userio()"
- Add new interface dev_map_userio()
- Allow systemd to read ibacm pid files

* Thu Sep 06 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-2
- Allow tomcat services create link file in /tmp
- Label /etc/shorewall6 as shorewall_etc_t
- Allow winbind_t domain kill in user namespaces
- Allow firewalld_t domain to read random device
- Allow abrt_t domain to do execmem
- Allow geoclue_t domain to execute own var_lib_t files
- Allow openfortivpn_t domain to read system network state
- Allow dnsmasq_t domain to read networkmanager lib files
- sssd: Allow to limit capabilities using libcap
- sssd: Remove unnecessary capability
- sssd: Do not audit usage of lib nss_systemd.so
- Fix bug in nsd.fc, /var/run/nsd.ctl is socket file not file
- Add correct namespace_init_exec_t context to /etc/security/namespace.d/*
- Update nscd_socket_use to allow caller domain to mmap nscd_var_run_t files
- Allow exim_t domain to mmap bin files
- Allow mysqld_t domain to executed with nnp transition
- Allow svirt_t domain to mmap svirt_image_t block files
- Add caps dac_read_search and dav_override to pesign_t domain
- Allow iscsid_t domain to mmap userio chr files
- Add read interfaces for mysqld_log_t that was added in commit df832bf
- Allow boltd_t to dbus chat with xdm_t
- Conntrackd need to load kernel module to work
- Allow mysqld sys_nice capability
- Update boltd policy based on SELinux denials from rhbz#1607974
- Allow systemd to create symlinks in for /var/lib
- Add comment to show that template call also allows changing shells
- Document userdom_change_password_template() behaviour
- update files_mounton_kernel_symbol_table() interface to allow caller domain also mounton system_map_t file
- Fix typo in logging SELinux module
- Allow usertype to mmap user_tmp_type files
- In domain_transition_pattern there is no permission allowing caller domain to execu_no_trans on entrypoint, this patch fixing this issue
- Revert "Add execute_no_trans permission to mmap_exec_file_perms pattern"
- Add boolean: domain_can_mmap_files.
- Allow ipsec_t domian to mmap own tmp files
- Add .gitignore file
- Add execute_no_trans permission to mmap_exec_file_perms pattern
- Allow sudodomain to search caller domain proc info
- Allow audisp_remote_t domain to read auditd_etc_t
- netlabel: Remove unnecessary sssd nsswitch related macros
- Allow to use sss module in auth_use_nsswitch
- Limit communication with init_t over dbus
- Add actual modules.conf to the git repo
- Add few interfaces to optional block
- Allow sysadm_t and staff_t domain to manage systemd unit files
- Add interface dev_map_userio_dev()

* Tue Aug 28 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.3-1
- Allow ovs-vswitchd labeled as openvswitch_t domain communicate with qemu-kvm via UNIX stream socket
- Add interface devicekit_mounton_var_lib()
- Allow httpd_t domain to mmap tmp files
- Allow tcsd_t domain to have dac_override capability
- Allow cupsd_t to rename cupsd_etc_t files
- Allow iptables_t domain to create rawip sockets
- Allow amanda_t domain to mmap own tmpfs files
- Allow fcoemon_t domain to write to sysfs_t dirs
- Allow dovecot_auth_t domain to have dac_override capability
- Allow geoclue_t domain to mmap own tmp files
- Allow chronyc_t domain to read network state
- Allow apcupsd_t domain to execute itself
- Allow modemmanager_t domain to stream connect to sssd
- Allow chonyc_t domain to rw userdomain pipes
- Update dirsrvadmin_script_t policy to allow read httpd_tmp_t symlinks
- Update dirsrv_read_share() interface to allow caller domain to mmap dirsrv_share_t files
- Allow nagios_script_t domain to mmap nagios_spool_t files
- Allow geoclue_t domain to mmap geoclue_var_lib_t files
- Allow geoclue_t domain to map generic certs
- Update munin_manage_var_lib_files to allow manage also dirs
- Allow nsd_t domain to create new socket file in /var/run/nsd.ctl
- Fix typo in virt SELinux policy module
- Allow virtd_t domain to create netlink_socket
- Allow rpm_t domain to write to audit
- Allow nagios_script_t domain to mmap nagios_etc_t files
- Update nscd_socket_use() to allow caller domain to stream connect to nscd_t
- Allow kdumpctl_t domain to getattr fixed disk device in mls
- Fix typo in stapserver policy
- Dontaudit abrt_t domain to write to usr_t dirs
- Revert "Allow rpcbind to bind on all unreserved udp ports"
- Allow rpcbind to bind on all unreserved udp ports
- Allow virtlogd to execute itself
- Allow stapserver several actions: - execute own tmp files - mmap stapserver_var_lib_t files - create stapserver_tmpfs_t files
- Allow ypxfr_t domain to stream connect to rpcbind and allos search sssd libs
- Allos systemd to socket activate ibacm service
- Allow dirsrv_t domain to mmap user_t files
- Allow kdumpctl_t domain to manage kdumpctl_tmp_t fifo files
- Allow kdumpctl to write to files on all levels
- Allow httpd_t domain to mmap httpd_config_t files
- Allow sanlock_t domain to connectto to unix_stream_socket
- Revert "Add same context for symlink as binary"
- Allow mysql execute rsync
- Update nfsd_t policy because of ganesha features
- Allow conman to getattr devpts_t
- Allow tomcat_domain to connect to smtp ports
- Allow tomcat_t domain to mmap tomcat_var_lib_t files
- Allow nagios_t domain to mmap nagios_log_t files
- Allow kpropd_t domain to mmap krb5kdc_principal_t files
- Allow kdumpctl_t domain to read fixed disk storage
- Fix issue with aliases in apache interface file
- Add same context for symlink as binary
- Allow boltd_t to send logs to journal
- Allow colord_use_nfs to allow colord also mmap nfs_t files
- Allow mysqld_safe_t do execute itself
- Allow smbd_t domain to chat via dbus with avahi daemon
- cupsd_t domain will create /etc/cupsd/ppd as cupsd_etc_rw_t
- Update screen_role_template to allow caller domain to have screen_exec_t as entrypoint do new domain
- Add alias httpd__script_t to _script_t to make sepolicy generate working
- Allow dhcpc_t domain to read /dev/random
- Allow systemd to mounton kernel system table
- Allow systemd to mounton device_var_lib_t dirs
- Label also chr_file /dev/mtd.* devices as fixed_disk_device_t
- Allow syslogd_t domain to create netlink generic sockets
- Label /dev/tpmrm[0-9]* as tpm_device_t
- Update dev_filetrans_all_named_dev() to allow create event22-30 character files with label event_device_t
- Update userdom_security_admin() and userdom_security_admin_template() to allow use auditctl
- Allow insmod_t domain to read iptables pid files
- Allow systemd to mounton /etc
- Allow initrc_domain to mmap all binaries labeled as systemprocess_entry
- Allow xserver_t domain to start using systemd socket activation
- Tweak SELinux policy for systemd to allow DynamicUsers systemd feature
- Associate several proc labels to fs_t
- Update init_named_socket_activation() interface to allow systemd also create link files in /var/run
- Fix typo in syslogd policy
- Update syslogd policy to make working elasticsearch
- Label tcp and udp ports 9200 as wap_wsp_port
- Allow few domains to rw inherited kdumpctl tmp pipes
- label /var/lib/pgsql/data/log as postgresql_log_t
- Allow sysadm_t domain to accept socket
- Allow systemd to manage passwd_file_t

* Fri Aug 10 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-32
- Fix issue with aliases in apache interface file
- Add same context for symlink as binary
- Allow boltd_t to send logs to journal
- Allow colord_use_nfs to allow colord also mmap nfs_t files
- Allow mysqld_safe_t do execute itself
- Allow smbd_t domain to chat via dbus with avahi daemon
- cupsd_t domain will create /etc/cupsd/ppd as cupsd_etc_rw_t
- Update screen_role_template to allow caller domain to have screen_exec_t as entrypoint do new domain
- Add alias httpd__script_t to _script_t to make sepolicy generate working
- Allow gpg_t domain to mmap gpg_agent_tmp_t files
- label /var/lib/pgsql/data/log as postgresql_log_t
- Allow sysadm_t domain to accept socket
- Allow systemd to manage passwd_file_t
- Allow sshd_t domain to mmap user_tmp_t files

* Tue Aug 07 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-31
- Allow kprop_t domain to read network state
- Add support boltd policy
- Allow kpropd domain to exec itself
- Allow pdns_t to bind on tcp transproxy port
- Add support for opafm service
- Allow hsqldb_t domain to read cgroup files
- Allow rngd_t domain to read generic certs
- Allow innd_t domain to mmap own var_lib_t files
- Update screen_role_temaplate interface
- Allow chronyd_t domain to mmap own tmpfs files
- Allow sblim_sfcbd_t domain to mmap own tmpfs files
- Allow systemd to mounont boltd lib dirs
- Allow sysadm_t domain to create rawip sockets
- Allow sysadm_t domain to listen on socket
- Update sudo_role_template() to allow caller domain also setattr generic ptys
- Update logging_manage_all_logs() interface to allow caller domain map all logfiles

* Sun Jul 29 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-30
- Allow sblim_sfcbd_t domain to mmap own tmpfs files
- Allow nfsd_t domain to read krb5 keytab files
- Allow nfsd_t domain to manage fadm pid files
- Allow virt_domain to create icmp sockets BZ(1609142)
- Dontaudit oracleasm_t domain to request sys_admin capability
- Update logging_manage_all_logs() interface to allow caller domain map all logfiles

* Wed Jul 25 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-29
- Allow aide to mmap all files
- Revert "Allow firewalld to create rawip sockets"
- Revert "Allow firewalld_t do read iptables_var_run_t files"
- Allow svirt_tcg_t domain to read system state of virtd_t domains
- Update rhcs contexts to reflects the latest fenced changes
- Allow httpd_t domain to rw user_tmp_t files
- Fix typo in openct policy
- Allow winbind_t domian to connect to all ephemeral ports
- Allow firewalld_t do read iptables_var_run_t files
- Allow abrt_t domain to mmap data_home files
- Allow glusterd_t domain to mmap user_tmp_t files
- Allow mongodb_t domain to mmap own var_lib_t files
- Allow firewalld to read kernel usermodehelper state
- Allow modemmanager_t to read sssd public files
- Allow openct_t domain to mmap own var_run_t files
- Allow nnp transition for devicekit daemons
- Allow firewalld to create rawip sockets
- Allow firewalld to getattr proc filesystem
- Dontaudit sys_admin capability for pcscd_t domain
- Revert "Allow pcsd_t domain sys_admin capability"
- Allow fetchmail_t domain to stream connect to sssd
- Allow pcsd_t domain sys_admin capability
- Allow cupsd_t to create cupsd_etc_t dirs
- Allow varnishlog_t domain to list varnishd_var_lib_t dirs
- Allow mongodb_t domain to read system network state BZ(1599230)
- Allow tgtd_t domain to create dirs in /var/run labeled as tgtd_var_run_t BZ(1492377)
- Allow iscsid_t domain to mmap sysfs_t files
- Allow httpd_t domain to mmap own cache files
- Add sys_resource capability to nslcd_t domain
- Fixed typo in logging_audisp_domain interface
- Add interface files_mmap_all_files()
- Add interface iptables_read_var_run()
- Allow systemd to mounton init_var_run_t files
- Update policy rules for auditd_t based on changes in audit version 3
- Allow systemd_tmpfiles_t do mmap system db files
- Merge branch 'rawhide' of github.com:fedora-selinux/selinux-policy into rawhide
- Improve domain_transition_pattern to allow mmap entrypoint bin file.
- Don't setup unlabeled_t as an entry_type
- Allow unconfined_service_t to transition to container_runtime_t

* Wed Jul 18 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-28
- Allow cupsd_t domain to mmap cupsd_etc_t files
- Allow kadmind_t domain to mmap krb5kdc_principal_t
- Allow virtlogd_t domain to read virt_etc_t link files
- Allow dirsrv_t domain to read crack db
- Dontaudit pegasus_t to require sys_admin capability
- Allow mysqld_t domain to exec mysqld_exec_t binary files
- Allow abrt_t odmain to read rhsmcertd lib files
- Allow winbind_t domain to request kernel module loads
- Allow tomcat_domain to read cgroup_t files
- Allow varnishlog_t domain to mmap varnishd_var_lib_t files
- Allow innd_t domain to mmap news_spool_t files
- Label HOME_DIR/mozilla.pdf file as mozilla_home_t instead of user_home_t
- Allow fenced_t domain to reboot
- Allow amanda_t domain to read network system state
- Allow abrt_t domain to read rhsmcertd logs
- Fix typo in radius policy
- Update zoneminder policy to reflect latest features in zoneminder BZ(1592555)
- Label /usr/bin/esmtp-wrapper as sendmail_exec_t
- Update raid_access_check_mdadm() interface to dontaudit caller domain to mmap mdadm_exec_t binary files
- Dontaudit thumb to read mmap_min_addr
- Allow chronyd_t to send to system_cronjob_t via unix dgram socket BZ(1494904)
- Allow mpd_t domain to mmap mpd_tmpfs_t files BZ(1585443)
- Allow collectd_t domain to use ecryptfs files BZ(1592640)
- Dontaudit mmap home type files for abrt_t domain
- Allow fprintd_t domain creating own tmp files BZ(1590686)
- Allow collectd_t domain to bind on bacula_port_t BZ(1590830)
- Allow fail2ban_t domain to getpgid BZ(1591421)
- Allow nagios_script_t domain to mmap nagios_log_t files BZ(1593808)
- Allow pcp_pmcd_t domain to use sys_ptrace usernamespace cap
- Allow sssd_selinux_manager_t to read/write to systemd sockets BZ(1595458)
- Allow virt_qemu_ga_t domain to read network state BZ(1592145)
- Allow radiusd_t domain to mmap radius_etc_rw_t files
- Allow git_script_t domain to read and mmap gitosis_var_lib_t files BZ(1591729)
- Add dac_read_search capability to thumb_t domain
- Add dac_override capability to cups_pdf_t domain BZ(1594271)
- Add net_admin capability to connntrackd_t domain BZ(1594221)
- Allow gssproxy_t domain to domtrans into gssd_t domain BZ(1575234)
- Fix interface init_dbus_chat in oddjob SELinux policy BZ(1590476)
- Allow motion_t to mmap video devices BZ(1590446)
- Add dac_override capability to mpd_t domain BZ(1585358)
- Allow fsdaemon_t domain to write to mta home files BZ(1588212)
- Allow virtlogd_t domain to chat via dbus with systemd_logind BZ(1589337)
- Allow sssd_t domain to write to general cert files BZ(1589339)
- Allow l2tpd_t domain to sends signull to ipsec domains BZ(1589483)
- Allow cockpit_session_t to read kernel network state BZ(1596941)
- Allow devicekit_power_t start with nnp systemd security feature with proper SELinux Domain transition BZ(1593817)
- Update rhcs_rw_cluster_tmpfs() interface to allow caller domain to mmap cluster_tmpfs_t files
- Allow chronyc_t domain to use nscd shm
- Label /var/lib/tomcats dir as tomcat_var_lib_t
- Allow lsmd_t domain to mmap lsmd_plugin_exec_t files
- Add ibacm policy
- Label /usr/sbin/rhn_check-[0-9]+.[0-9]+ as rpm_exec_t
- Allow kdumpgui_t domain to allow execute and mmap all binaries labeled as kdumpgui_tmp_t
- Dontaudit syslogd to watching top llevel dirs when imfile module is enabled
- Allow userdomain sudo domains to use generic ptys
- Allow systemd labeled as init_t to get sysvipc info BZ(1600877)
- Label /sbin/xtables-legacy-multi and /sbin/xtables-nft-multi as iptables_exec_t BZ(1600690)
- Remove duplicated userdom_delete_user_home_content_files
- Merge pull request #216 from rhatdan/resolved
- Allow load_policy_t domain to read/write to systemd sockets BZ(1582812)
- Add new interface init_prog_run_bpf()
- Allow unconfined and sysadm users to use bpftool BZ(1591440)
- Label /run/cockpit/motd as etc_t BZ(1584167)
- Allow systemd_machined_t domain to sendto syslogd_t over unix dgram sockets
- Add interface userdom_dontaudit_mmap_user_home_content_files()
- Allow systemd to listen bluetooth sockets BZ(1592223)
- Allow systemd to remove user_home_t files BZ(1418463)
- Allow xdm_t domain to mmap and read cert_t files BZ(1553761)
- Allow nsswitch_domain to mmap passwd_file_t files BZ(1518655)
- Allow systemd to delete user temp files BZ(1595189)
- Allow systemd to mounton core kernel interface
- Add dac_override capability to ipsec_t domain BZ(1589534)
- Allow systemd domain to mmap lvm config files BZ(1594584)
- Allow systemd to write systemd_logind_inhibit_var_run_t fifo files
- Allows systemd to get attribues of core kernel interface BZ(1596928)
- Allow systemd_modules_load_t to access unabeled infiniband pkeys
- Add systemd_dbus_chat_resolved interface
- Allow init_t domain to create netlink rdma sockets for ibacm policy
- Update corecmd_exec_shell() interface to allow caller domain to mmap shell_exec_t files
- Allow lvm_t domain to write files to all mls levels
- Add to su_role_template allow rule for creating netlink_selinux sockets

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.2-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-26
- Allow psad domain to setrlimit. Allow psad domain to stream connect to dbus Allow psad domain to exec journalctl_exec_t binary
- Update cups_filetrans_named_content() to allow caller domain create ppd directory with cupsd_etc_rw_t label
- Allow abrt_t domain to write to rhsmcertd pid files
- Allow pegasus_t domain to eexec lvm binaries and allow read/write access to lvm control
- Add vhostmd_t domain to read/write to svirt images
- Update kdump_manage_kdumpctl_tmp_files() interface to allow caller domain also mmap kdumpctl_tmp_t files
- Allow sssd_t and slpad_t domains to mmap generic certs
- Allow chronyc_t domain use inherited user ttys
- Allow stapserver_t domain to mmap own tmp files
- Update nscd_dontaudit_write_sock_file() to dontaudit also stream connect to nscd_t domain
- Merge pull request #60 from vmojzis/rawhide
- Allow tangd_t domain stream connect to sssd
- Allow oddjob_t domain to chat with systemd via dbus
- Allow freeipmi domains to mmap sysfs files
- Fix typo in logwatch interface file
- Allow sysadm_t and staff_t domains to use sudo io logging
- Allow sysadm_t domain create sctp sockets
- Allow traceroute_t domain to exec bin_t binaries
- Allow systemd_passwd_agent_t domain to list sysfs Allow systemd_passwd_agent_t domain to dac_override
- Add new interface dev_map_sysfs()

* Thu Jun 14 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-25
- Merge pull request #60 from vmojzis/rawhide
- Allow tangd_t domain stream connect to sssd
- Allow oddjob_t domain to chat with systemd via dbus
- Allow freeipmi domains to mmap sysfs files
- Fix typo in logwatch interface file
- Allow spamd_t to manage logwatch_cache_t files/dirs
- Allow dnsmasw_t domain to create own tmp files and manage mnt files
- Allow fail2ban_client_t to inherit rlimit information from parent process
- Allow nscd_t to read kernel sysctls
- Label /var/log/conman.d as conman_log_t
- Add dac_override capability to tor_t domain
- Allow certmonger_t to readwrite to user_tmp_t dirs
- Allow abrt_upload_watch_t domain to read general certs
- Allow chornyd_t read phc2sys_t shared memory
- Add several allow rules for pesign policy:
- Add setgid and setuid capabilities to mysqlfd_safe_t domain
- Add tomcat_can_network_connect_db boolean
- Update virt_use_sanlock() boolean to read sanlock state
- Add sanlock_read_state() interface
- Allow zoneminder_t to getattr of fs_t
- Allow rhsmcertd_t domain to send signull to postgresql_t domain
- Add log file type to collectd and allow corresponding access
- Allow policykit_t domain to dbus chat with dhcpc_t
- Allow traceroute_t domain to exec bin_t binaries
- Allow systemd_passwd_agent_t domain to list sysfs Allow systemd_passwd_agent_t domain to dac_override
- Add new interface dev_map_sysfs()
- Allow sshd_keygen_t to execute plymouthd
- Allow systemd_networkd_t create and relabel tun sockets
- Add new interface postgresql_signull()

* Tue Jun 12 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-24
- /usr/libexec/bluetooth/obexd should have only obexd_exec_t instead of bluetoothd_exec_t type
- Allow ntop_t domain to create/map various sockets/files.
- Enable the dictd to communicate via D-bus.
- Allow inetd_child process to chat via dbus with abrt
- Allow zabbix_agent_t domain to connect to redis_port_t
- Allow rhsmcertd_t domain to read xenfs_t files
- Allow zabbix_agent_t to run zabbix scripts
- Fix openvswith SELinux module
- Fix wrong path in tlp context file BZ(1586329)
- Update brltty SELinux module
- Allow rabbitmq_t domain to create own tmp files/dirs
- Allow policykit_t mmap policykit_auth_exec_t files
- Allow ipmievd_t domain to read general certs
- Add sys_ptrace capability to pcp_pmie_t domain
- Allow squid domain to exec ldconfig
- Update gpg SELinux policy module
- Allow mailman_domain to read system network state
- Allow openvswitch_t domain to read neutron state and read/write fixed disk devices
- Allow antivirus_domain to read all domain system state
- Allow targetd_t domain to red gconf_home_t files/dirs
- Label /usr/libexec/bluetooth/obexd as obexd_exec_t
- Add interface nagios_unconfined_signull()
- Fix typos in zabbix.te file
- Add missing requires
- Allow tomcat domain sends email
- Fix typo in sge policy
- Merge pull request #214 from wrabcak/fb-dhcpc
- Allow dhcpc_t creating own socket files inside /var/run/ Allow dhcpc_t creating netlink_kobject_uevent_socket, netlink_generic_socket, rawip_socket BZ(1585971)
- Allow confined users get AFS tokens
- Allow sysadm_t domain to chat via dbus
- Associate sysctl_kernel_t type with filesystem attribute
- Allow syslogd_t domain to send signull to nagios_unconfined_plugin_t
- Fix typo in netutils.te file

* Wed Jun 06 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-23
- Add dac_override capability to sendmail_t domian

* Wed Jun 06 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-22
- Fix typo in authconfig policy
- Update ctdb domain to support gNFS setup
- Allow authconfig_t dbus chat with policykit
- Allow lircd_t domain to read system state
- Revert "Allow fsdaemon_t do send emails BZ(1582701)"
- Typo in uuidd policy
- Allow tangd_t domain read certs
- Allow vpnc_t domain to read configfs_t files/dirs BZ(1583107)
- Allow vpnc_t domain to read generic certs BZ(1583100)
- Label /var/lib/phpMyAdmin directory as httpd_sys_rw_content_t BZ(1584811)
- Allow NetworkManager_ssh_t domain to be system dbud client
- Allow virt_qemu_ga_t read utmp
- Add capability dac_override to system_mail_t domain
- Update uuidd policy to reflect last changes from base branch
- Add cap dac_override to procmail_t domain
- Allow sendmail to mmap etc_aliases_t files BZ(1578569)
- Add new interface dbus_read_pid_sock_files()
- Allow mpd_t domain read config_home files if mpd_enable_homedirs boolean will be enabled
- Allow fsdaemon_t do send emails BZ(1582701)
- Allow firewalld_t domain to request kernel module BZ(1573501)
- Allow chronyd_t domain to send send msg via dgram socket BZ(1584757)
- Add sys_admin capability to fprint_t SELinux domain
- Allow cyrus_t domain to create own files under /var/run BZ(1582885)
- Allow cachefiles_kernel_t domain to have capability dac_override
- Update policy for ypserv_t domain
- Allow zebra_t domain to bind on tcp/udp ports labeled as qpasa_agent_port_t
- Allow cyrus to have dac_override capability
- Dontaudit action when abrt-hook-ccpp is writing to nscd sockets
- Fix homedir polyinstantion under mls
- Fixed typo in init.if file
- Allow systemd to remove generic tmpt files BZ(1583144)
- Update init_named_socket_activation() interface to also allow systemd create objects in /var/run with proper label during socket activation
- Allow systemd-networkd and systemd-resolved services read system-dbusd socket BZ(1579075)
- Fix typo in authlogin SELinux security module
- Allod nsswitch_domain attribute to be system dbusd client BZ(1584632)
- Allow audisp_t domain to mmap audisp_exec_t binary
- Update ssh_domtrans_keygen interface to allow mmap ssh_keygen_exec_t binary file
- Label tcp/udp ports 2612 as qpasa_agetn_port_t

* Sat May 26 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-21
- Add dac_override to exim policy BZ(1574303)
- Fix typo in conntrackd.fc file
- Allow sssd_t to kill sssd_selinux_manager_t
- Allow httpd_sys_script_t to connect to mongodb_port_t if boolean httpd_can_network_connect_db  is turned on
- Allow chronyc_t to redirect ourput to /var/lib /var/log and /tmp
- Allow policykit_auth_t to read udev db files BZ(1574419)
- Allow varnishd_t do be dbus client BZ(1582251)
- Allow cyrus_t domain to mmap own pid files BZ(1582183)
- Allow user_mail_t domain to mmap etc_aliases_t files
- Allow gkeyringd domains to run ssh agents
- Allow gpg_pinentry_t domain read ssh state
- Allow sysadm_u use xdm
- Allow xdm_t domain to listen ofor unix dgram sockets BZ(1581495)
- Add interface ssh_read_state()
- Fix typo in sysnetwork.if file

* Thu May 24 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-20
- Allow tangd_t domain to create tcp sockets and add new interface tangd_read_db_files
- Allow mailman_mail_t domain to search for apache configs
- Allow mailman_cgi_t domain to ioctl an httpd with a unix domain stream sockets.
- Improve procmail_domtrans() to allow mmaping procmail_exec_t
- Allow ptrace arbitrary processes
- Allow jabberd_router_t domain read kerberos keytabs BZ(1573945)
- Allow certmonger to geattr of filesystems BZ(1578755)
- Update dev_map_xserver_misc interface to allo mmaping char devices instead of files
- Allow noatsecure permission for all domain transitions from systemd.
- Allow systemd to read tangd db files
- Fix typo in ssh.if file
- Allow xdm_t domain to mmap xserver_misc_device_t files
- Allow xdm_t domain to execute systemd-coredump binary
- Add bridge_socket, dccp_socket, ib_socket and mpls_socket to socket_class_set
- Improve modutils_domtrans_insmod() interface to mmap insmod_exec_t binaries
- Improve iptables_domtrans() interface to allow mmaping iptables_exec_t binary
- Improve auth_domtrans_login_programinterface to allow also mmap login_exec_t binaries
- Improve auth_domtrans_chk_passwd() interface to allow also mmaping chkpwd_exec_t binaries.
- Allow mmap dhcpc_exec_t binaries in sysnet_domtrans_dhcpc interface
- Improve running xorg with proper SELinux domain even if systemd security feature NoNewPrivileges is used

* Tue May 22 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-19
- Increase dependency versions of policycoreutils and checkpolicy packages 

* Mon May 21 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-18
- Disable secure mode environment cleansing for dirsrv_t
- Allow udev execute /usr/libexec/gdm-disable-wayland in xdm_t domain which allows create /run/gdm/custom.conf with proper xdm_var_run_t label.

* Mon May 21 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-17
- Add dac_override capability to remote_login_t domain
- Allow chrome_sandbox_t to mmap tmp files
- Update ulogd SELinux security policy
- Allow rhsmcertd_t domain send signull to apache processes
- Allow systemd socket activation for modemmanager
- Allow geoclue to dbus chat with systemd
- Fix file contexts on conntrackd policy
- Temporary fix for varnish and apache adding capability for DAC_OVERRIDE
- Allow lsmd_plugin_t domain to getattr lsm_t unix stream sockets
- Add label for  /usr/sbin/pacemaker-remoted to have cluster_exec_t
- Allow nscd_t domain to be system dbusd client
- Allow abrt_t domain to read sysctl
- Add dac_read_search capability for tangd
- Allow systemd socket activation for rshd domain
- Add label for /usr/libexec/cyrus-imapd/master as cyrus_exec_t to have proper SELinux domain transition from init_t to cyrus_t
- Allow kdump_t domain to map /boot files
- Allow conntrackd_t domain to send msgs to syslog
- Label /usr/sbin/nhrpd and /usr/sbin/pimd binaries as zebra_exec_t
- Allow swnserve_t domain to stream connect to sasl domain
- Allow smbcontrol_t to create dirs with samba_var_t label
- Remove execstack,execmem and execheap from domains setroubleshootd_t, locate_t and podsleuth_t to increase security. BZ(1579760)
- Allow tangd to read public sssd files BZ(1509054)
- Allow geoclue start with nnp systemd security feature with proper SELinux Domain transition BZ(1575212)
- Allow ctdb_t domain modify ctdb_exec_t files
- Allow firewalld_t domain to create netlink_netfilter sockets
- Allow radiusd_t domain to read network sysctls
- Allow pegasus_t domain to mount tracefs_t filesystem
- Allow create systemd to mount pid files
- Add files_map_boot_files() interface
- Remove execstack,execmem and execheap from domain fsadm_t to increase security. BZ(1579760)
- Fix typo xserver SELinux module
- Allow systemd to mmap files with var_log_t label
- Allow x_userdomains read/write to xserver session

* Mon Apr 30 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-16
- Allow systemd to mmap files with var_log_t label
- Allow x_userdomains read/write to xserver session

* Sat Apr 28 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-15
- Allow unconfined_domain_type to create libs filetrans named content BZ(1513806)

* Fri Apr 27 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-14
- Add dac_override capability to mailman_mail_t domain
- Add dac_override capability to radvd_t domain
- Update openvswitch policy
- Add dac_override capability to oddjob_homedir_t domain
- Allow slapd_t domain to mmap slapd_var_run_t files
- Rename tang policy to tangd
- Allow virtd_t domain to relabel virt_var_lib_t files
- Allow logrotate_t domain to stop services via systemd
- Add tang policy
- Allow mozilla_plugin_t to create mozilla.pdf file in user homedir with label mozilla_home_t
- Allow snapperd_t daemon to create unlabeled dirs.
- Make httpd_var_run_t mountpoint
- Allow hsqldb_t domain to mmap own temp files
- We have inconsistency in cgi templates with upstream, we use _content_t, but refpolicy use httpd__content_t. Created aliasses to make it consistence
- Allow Openvswitch adding netdev bridge ovs 2.7.2.10 FDP
- Add new Boolean tomcat_use_execmem
- Allow nfsd_t domain to read/write sysctl fs files
- Allow conman to read system state
- Allow brltty_t domain to be dbusd system client
- Allow zebra_t domain to bind on babel udp port
- Allow freeipmi domain to read sysfs_t files
- Allow targetd_t domain mmap lvm config files
- Allow abrt_t domain to manage kdump crash files
- Add capability dac_override to antivirus domain
- Allow svirt_t domain mmap svirt_image_t files BZ(1514538)
- Allow ftpd_t domain to chat with systemd
- Allow systemd init named socket activation for uuidd policy
- Allow networkmanager domain to write to ecryptfs_t files BZ(1566706)
- Allow l2tpd domain to stream connect to sssd BZ(1568160)
- Dontaudit abrt_t to write to lib_t dirs BZ(1566784)
- Allow NetworkManager_ssh_t domain transition to insmod_t BZ(1567630)
- Allow certwatch to manage cert files BZ(1561418)
- Merge pull request #53 from tmzullinger/rawhide
- Merge pull request #52 from thetra0/rawhide
- Allow abrt_dump_oops_t domain to mmap all non security files BZ(1565748)
- Allow gpg_t domain mmap cert_t files Allow gpg_t mmap gpg_agent_t files
- Allow NetworkManager_ssh_t domain use generic ptys. BZ(1565851)
- Allow pppd_t domain read/write l2tpd pppox sockets BZ(1566096)
- Allow xguest user use bluetooth sockets if xguest_use_bluetooth boolean is turned on.
- Allow pppd_t domain creating pppox sockets BZ(1566271)
- Allow abrt to map var_lib_t files
- Allow chronyc to read system state BZ(1565217)
- Allow keepalived_t domain to chat with systemd via dbus
- Allow git to mmap git_(sys|user)_content_t files BZ(1518027)
- Allow netutils_t domain to create bluetooth sockets
- Allow traceroute to bind on generic sctp node
- Allow traceroute to search network sysctls
- Allow systemd to use virtio console
- Label /dev/op_panel and /dev/opal-prd as opal_device_t
- Label /run/ebtables.lock as iptables_var_run_t
- Allow udev_t domain to manage udev_rules_t char files.
- Assign babel_port_t label to udp port 6696
- Add new interface lvm_map_config
- Merge pull request #212 from stlaz/patch-1
- Allow local_login_t reads of udev_var_run_t context
- Associate sysctl_crypto_t fs with fs_t BZ(1569313)
- Label /dev/vhost-vsock char device as vhost_device_t
- Allow iptables_t domain to create dirs in etc_t with system_conf_t labels
- Allow x userdomain to mmap xserver_tmpfs_t files
- Allow sysadm_t to mount tracefs_t
- Allow unconfined user all perms under bpf class BZ(1565738)
- Allow SELinux users (except guest and xguest) to using bluetooth sockets
- Add new interface files_map_var_lib_files()
- Allow user_t and staff_t domains create netlink tcpdiag sockets
- Allow systemd-networkd to read sysctl_t files
- Allow systemd_networkd_t to read/write tun tap devices
- refpolicy: Update for kernel sctp support

* Thu Apr 12 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-13
- refpolicy: Update for kernel sctp support
- Allow smbd_t send to nmbd_t via dgram sockets BZ(1563791)
- Allow antivirus domain to be client for system dbus BZ(1562457)
- Dontaudit requesting tlp_t domain kernel modules, its a kernel bug BZ(1562383)
- Add new boolean: colord_use_nfs() BZ(1562818)
- Allow pcp_pmcd_t domain to check access to mdadm BZ(1560317)
- Allow colord_t to mmap gconf_home_t files
- Add new boolean redis_enable_notify()
- Label  /var/log/shibboleth-www(/.*) as httpd_sys_rw_content_t
- Add new label for vmtools scripts and label it as vmtools_unconfined_t stored in /etc/vmware-tools/
- Remove labeling for /etc/vmware-tools to bin_t it should be vmtools_unconfined_exec_t

* Sat Apr 07 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-12
- Add new boolean redis_enable_notify()
- Label  /var/log/shibboleth-www(/.*) as httpd_sys_rw_content_t
- Add new label for vmtools scripts and label it as vmtools_unconfined_t stored in /etc/vmware-tools/
- Allow svnserve_t domain to manage kerberos rcache and read krb5 keytab
- Add dac_override and dac_read_search capability to hypervvssd_t domain
- Label /usr/lib/systemd/systemd-fence_sanlockd as fenced_exec_t
- Allow samba to create /tmp/host_0 as krb5_host_rcache_t
- Add dac_override capability to fsdaemon_t BZ(1564143)
- Allow abrt_t domain to map dos files BZ(1564193)
- Add dac_override capability to automount_t domain
- Allow keepalived_t domain to connect to system dbus bus
- Allow nfsd_t to read nvme block devices BZ(1562554)
- Allow lircd_t domain to execute bin_t files BZ(1562835)
- Allow l2tpd_t domain to read sssd public files BZ(1563355)
- Allow logrotate_t domain to do dac_override BZ(1539327)
- Remove labeling for /etc/vmware-tools to bin_t it should be vmtools_unconfined_exec_t
- Add capability sys_resource to systemd_sysctl_t domain
- Label all /dev/rbd* devices as fixed_disk_device_t
- Allow xdm_t domain to mmap xserver_log_t files BZ(1564469)
- Allow local_login_t domain to rread udev db
- Allow systemd_gpt_generator_t to read /dev/random device
- add definition of bpf class and systemd perms

* Thu Mar 29 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-11
- Allow accountsd_t domain to dac override BZ(1561304)
- Allow cockpit_ws_t domain to read system state BZ(1561053)
- Allow postfix_map_t domain to use inherited user ptys BZ(1561295)
- Allow abrt_dump_oops_t domain dac override BZ(1561467)
- Allow l2tpd_t domain to run stream connect for sssd_t BZ(1561755)
- Allow crontab domains to do dac override
- Allow snapperd_t domain to unmount fs_t filesystems
- Allow pcp processes to read fixed_disk devices BZ(1560816)
- Allow unconfined and confined users to use dccp sockets
- Allow systemd to manage bpf dirs/files
- Allow traceroute_t to create dccp_sockets

* Mon Mar 26 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-10
- Fedora Atomic host using for temp files /sysroot/tmp patch, we should label same as /tmp adding file context equivalence BZ(1559531)

* Sun Mar 25 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-9
- Allow smbcontrol_t to mmap samba_var_t files and allow winbind create sockets BZ(1559795)
- Allow nagios to exec itself and mmap nagios spool files BZ(1559683)
- Allow nagios to mmap nagios config files BZ(1559683)
- Fixing Ganesha module
- Fix typo in NetworkManager module
- Fix bug in gssproxy SELinux module
- Allow abrt_t domain to mmap container_file_t files BZ(1525573)
- Allow networkmanager to be run ssh client BZ(1558441)
- Allow pcp domains to do dc override BZ(1557913)
- Dontaudit pcp_pmie_t to reaquest lost kernel module
- Allow pcp_pmcd_t to manage unpriv userdomains semaphores BZ(1554955)
- Allow httpd_t to read httpd_log_t dirs BZ(1554912)
- Allow fail2ban_t to read system network state BZ(1557752)
- Allow dac override capability to mandb_t domain BZ(1529399)
- Allow collectd_t domain to mmap collectd_var_lib_t files BZ(1556681)
- Dontaudit bug in kernel 4.16 when domains requesting loading kernel modules BZ(1555369)
- Add Domain transition from gssproxy_t to httpd_t domains BZ(1548439)
- Allow httpd_t to mmap user_home_type files if boolean httpd_read_user_content is enabled BZ(1555359)
- Allow snapperd to relabel snapperd_data_t
- Improve bluetooth_stream_socket interface to allow caller domain also send bluetooth sockets
- Allow tcpd_t bind on sshd_port_t if ssh_use_tcpd() is enabled
- Allow insmod_t to load modules BZ(1544189)
- Allow systemd_rfkill_t domain sys_admin capability BZ(1557595)
- Allow systemd_networkd_t to read/write tun tap devices
- Add shell_exec_t file as domain entry for init_t
- Label also /run/systemd/resolved/ as systemd_resolved_var_run_t BZ(1556862)
- Dontaudit kernel 4.16 bug when lot of domains requesting load kernel module BZ(1557347)
- Improve userdom_mmap_user_home_content_files
- Allow systemd_logind_t domain to setattributes on fixed disk devices BZ(1555414)
- Dontaudit kernel 4.16 bug when lot of domains requesting load kernel module
- Allow semanage_t domain mmap usr_t files
- Add new boolean: ssh_use_tcpd()

* Wed Mar 21 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-8
- Improve bluetooth_stream_socket interface to allow caller domain also send bluetooth sockets
- Allow tcpd_t bind on sshd_port_t if ssh_use_tcpd() is enabled
- Allow semanage_t domain mmap usr_t files
- Add new boolean: ssh_use_tcpd()

* Tue Mar 20 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-7
- Update screen_role_template() to allow also creating sockets in HOMEDIR/screen/
- Allow newrole_t dacoverride capability
- Allow traceroute_t domain to mmap packet sockets
- Allow netutils_t domain to mmap usmmon device
- Allow netutils_t domain to use mmap on packet_sockets
- Allow traceroute to create icmp packets
- Allos sysadm_t domain to create tipc sockets
- Allow confined users to use new socket classes for bluetooth, alg and tcpdiag sockets

* Thu Mar 15 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-6
- Allow rpcd_t domain dac override
- Allow rpm domain to mmap rpm_var_lib_t files
- Allow arpwatch domain to create bluetooth sockets
- Allow secadm_t domain to mmap audit config and log files
- Update init_abstract_socket_activation() to allow also creating tcp sockets
- getty_t should be ranged in MLS. Then also local_login_t runs as ranged domain.
- Add SELinux support for systemd-importd
- Create new type bpf_t and label /sys/fs/bpf with this type

* Mon Mar 12 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-5
- Allow bluetooth_t domain to create alg_socket BZ(1554410)
- Allow tor_t domain to execute bin_t files BZ(1496274)
- Allow iscsid_t domain to mmap kernel modules BZ(1553759)
- Update minidlna SELinux policy BZ(1554087)
- Allow motion_t domain to read sysfs_t files BZ(1554142)
- Allow snapperd_t domain to getattr on all files,dirs,sockets,pipes BZ(1551738)
- Allow l2tp_t domain to read ipsec config files BZ(1545348)
- Allow colord_t to mmap home user files BZ(1551033)
- Dontaudit httpd_t creating kobject uevent sockets BZ(1552536)
- Allow ipmievd_t to mmap kernel modules BZ(1552535)
- Allow boinc_t domain to read cgroup files BZ(1468381)
- Backport allow rules from refpolicy upstream repo
- Allow gpg_t domain to bind on all unereserved udp ports
- Allow systemd to create systemd_rfkill_var_lib_t dirs BZ(1502164)
- Allow netlabel_mgmt_t domain to read sssd public files, stream connect to sssd_t BZ(1483655)
- Allow xdm_t domain to sys_ptrace BZ(1554150)
- Allow application_domain_type also mmap inherited user temp files BZ(1552765)
- Update ipsec_read_config() interface
- Fix broken sysadm SELinux module
- Allow ipsec_t to search for bind cache BZ(1542746)
- Allow staff_t to send sigkill to mount_t domain BZ(1544272)
- Label /run/systemd/resolve/stub-resolv.conf as net_conf_t BZ(1471545)
- Label ip6tables.init as iptables_exec_t BZ(1551463)
- Allow hostname_t to use usb ttys BZ(1542903)
- Add fsetid capability to updpwd_t domain BZ(1543375)
- Allow systemd machined send signal to all domains BZ(1372644)
- Dontaudit create netlink selinux sockets for unpriv SELinux users BZ(1547876)
- Allow sysadm_t to create netlink generic sockets BZ(1547874)
- Allow passwd_t domain chroot
- Dontaudit confined unpriviliged users setuid capability

* Tue Mar 06 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-4
- Allow l2tpd_t domain to create pppox sockets
- Update dbus_system_bus_client() so calling domain could read also system_dbusd_var_lib_t link files BZ(1544251)
- Add interface abrt_map_cache()
- Update gnome_manage_home_config() to allow also map permission BZ(1544270)
- Allow oddjob_mkhomedir_t domain to be dbus system client BZ(1551770)
- Dontaudit kernel bug when several services requesting load kernel module
- Allow traceroute and unconfined domains creating sctp sockets
- Add interface corenet_sctp_bind_generic_node()
- Allow ping_t domain to create icmp sockets
- Allow staff_t to mmap abrt_var_cache_t BZ(1544273)
- Fix typo bug in dev_map_framebuffer() interface BZ(1551842)
- Dontaudit kernel bug when several services requesting load kernel module

* Mon Mar 05 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-3
- Allow vdagent_t domain search cgroup dirs BZ(1541564)
- Allow bluetooth_t domain listen on bluetooth sockets BZ(1549247)
- Allow bluetooth domain creating bluetooth sockets BZ(1551577)
- pki_log_t should be log_file
- Allow gpgdomain to unix_stream socket connectto
- Make working gpg agent in gpg_agent_t domain
- Dontaudit thumb_t to rw lvm pipes BZ(154997)
- Allow start cups_lpd via systemd socket activation BZ(1532015)
- Improve screen_role_template Resolves: rhbz#1534111
- Dontaudit modemmanager to setpgid. BZ(1520482)
- Dontaudit kernel bug when systemd requesting load kernel module BZ(1547227)
- Allow systemd-networkd to create netlink generic sockets BZ(1551578)
- refpolicy: Define getrlimit permission for class process
- refpolicy: Define smc_socket security class
- Allow transition from sysadm role into mdadm_t domain.
- ssh_t trying to communicate with gpg agent not sshd_t
- Allow sshd_t communicate with gpg_agent_t
- Allow initrc domains to mmap binaries with direct_init_entry attribute BZ(1545643)
- Revert "Allow systemd_rfkill_t domain to reguest kernel load module BZ(1543650)"
- Revert "Allow systemd to request load kernel module BZ(1547227)"
- Allow systemd to write to all pidfile socketes because of SocketActivation unit option ListenStream= BZ(1543576)
- Add interface lvm_dontaudit_rw_pipes() BZ(154997)
- Add interfaces for systemd socket activation
- Allow systemd-resolved to create stub-resolv.conf with right label net_conf_t BZ(1547098)

* Thu Feb 22 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-2
- refpolicy: Define extended_socket_class policy capability and socket classes
- Make bluetooth_var_lib_t as mountpoint BZ(1547416)
- Allow systemd to request load kernel module BZ(1547227)
- Allow ipsec_t domain to read l2tpd pid files
- Allow sysadm to read/write trace filesystem BZ(1547875)
- Allow syslogd_t to mmap systemd coredump tmpfs files BZ(1547761)

* Wed Feb 21 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.2-1
- Rebuild for current rawhide (fc29)

* Tue Feb 20 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.1-9
- Fix broken cups Security Module
- Allow dnsmasq_t domain dbus chat with unconfined users. BZ(1532079)
- Allow geoclue to connect to tcp nmea port BZ(1362118)
- Allow pcp_pmcd_t to read mock lib files BZ(1536152)
- Allow abrt_t domain to mmap passwd file BZ(1540666)
- Allow gpsd_t domain to get session id of another process BZ(1540584)
- Allow httpd_t domain to mmap httpd_tmpfs_t files BZ(1540405)
- Allow cluster_t dbus chat with systemd BZ(1540163)
- Add interface raid_stream_connect()
- Allow nscd_t to mmap nscd_var_run_t files BZ(1536689)
- Allow dovecot_delivery_t to mmap mail_home_rw_t files BZ(1531911)
- Make cups_pdf_t domain system dbusd client BZ(1532043)
- Allow logrotate to read auditd_log_t files BZ(1525017)
- Improve snapperd SELinux policy BZ(1514272)
- Allow virt_domain to read virt_image_t files BZ(1312572)
- Allow openvswitch_t stream connect svirt_t
- Update dbus_dontaudit_stream_connect_system_dbusd() interface
- Allow openvswitch domain to manage svirt_tmp_t sock files
- Allow named_filetrans_domain domains to create .heim_org.h5l.kcm-socket sock_file with label sssd_var_run_t BZ(1538210)
- Merge pull request #50 from dodys/pkcs
- Label tcp and udp ports 10110 as nmea_port_t BZ(1362118)
- Allow systemd to access rfkill lib dirs BZ(1539733)
- Allow systemd to mamange raid var_run_t sockfiles and files BZ(1379044)
- Allow vxfs filesystem to use SELinux labels
- Allow systemd to setattr on systemd_rfkill_var_lib_t dirs BZ(1512231)
- Allow few services to dbus chat with snapperd BZ(1514272)
- Allow systemd to relabel system unit symlink to systemd_unit_file_t. BZ(1535180)
- Fix logging as staff_u into Fedora 27
- Fix broken systemd_tmpfiles_run() interface

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.14.1-8
- Escape macros in %%changelog

* Thu Feb 08 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.1-7
- Label /usr/sbin/ldap-agent as dirsrv_snmp_exec_t
- Allow certmonger_t domain to access /etc/pki/pki-tomcat BZ(1542600)
- Allow keepalived_t domain getattr proc filesystem
- Allow init_t to create UNIX sockets for unconfined services (BZ1543049)
- Allow ipsec_mgmt_t execute ifconfig_exec_t binaries Allow ipsec_mgmt_t nnp domain transition to ifconfig_t
- Allow ipsec_t nnp transistions to domains ipsec_mgmt_t and ifconfig_t

* Tue Feb 06 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.1-6
- Allow openvswitch_t domain to read cpuid, write to sysfs files and creating openvswitch_tmp_t sockets
- Add new interface ppp_filetrans_named_content()
- Allow keepalived_t read sysctl_net_t files
- Allow puppetmaster_t domtran to puppetagent_t
- Allow kdump_t domain to read kernel ring buffer
- Allow boinc_t to mmap boinc tmpfs files BZ(1540816)
- Merge pull request #47 from masatake/keepalived-signal
- Allow keepalived_t create and write a file under /tmp
- Allow ipsec_t domain to exec ifconfig_exec_t binaries.
- Allow unconfined_domain_typ to create pppd_lock_t directory in /var/lock
- Allow updpwd_t domain to create files in /etc with shadow_t label

* Tue Jan 30 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.1-5
- Allow opendnssec daemon to execute ods-signer BZ(1537971)

* Tue Jan 30 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.1-4
- rpm: Label /usr/share/rpm usr_t (ostree/Atomic systems)
- Update dbus_role_template() BZ(1536218)
- Allow lldpad_t domain to mmap own tmpfs files BZ(1534119)
- Allow blueman_t dbus chat with policykit_t BZ(1470501)
- Expand virt_read_lib_files() interface to allow list dirs with label virt_var_lib_t BZ(1507110)
- Allow postfix_master_t and postfix_local_t to connect to system dbus. BZ(1530275)
- Allow system_munin_plugin_t domain to read sssd public files and allow stream connect to ssd daemon BZ(1528471)
- Allow rkt_t domain to bind on rkt_port_t tcp BZ(1534636)
- Allow jetty_t domain to mmap own temp files BZ(1534628)
- Allow sslh_t domain to read sssd public files and stream connect to sssd. BZ(1534624)
- Consistently label usr_t for kernel/initrd in /usr
- kernel/files.fc: Label /usr/lib/sysimage as usr_t
- Allow iptables sysctl load list support with SELinux enforced
- Label HOME_DIR/.config/systemd/user/* user unit files as systemd_unit_file_t BZ(1531864)

* Fri Jan 19 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.1-3
- Merge pull request #45 from jlebon/pr/rot-sd-dbus-rawhide
- Allow virt_domains to acces infiniband pkeys.
- Allow systemd to relabelfrom tmpfs_t link files in /var/run/systemd/units/ BZ(1535180)
- Label /usr/libexec/ipsec/addconn as ipsec_exec_t to run this script as ipsec_t instead of init_t
- Allow audisp_remote_t domain write to files on all levels

* Mon Jan 15 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.1-2
- Allow aide to mmap usr_t files BZ(1534182)
- Allow ypserv_t domain to connect to tcp ports BZ(1534245)
- Allow vmtools_t domain creating vmware_log_t files
- Allow openvswitch_t domain to acces infiniband devices
- Allow dirsrv_t domain to create tmp link files
- Allow pcp_pmie_t domain to exec itself. BZ(153326)
- Update openvswitch SELinux module
- Allow virtd_t to create also sock_files with label virt_var_run_t
- Allow chronyc_t domain to manage chronyd_keys_t files.
- Allow logwatch to exec journal binaries BZ(1403463)
- Allow sysadm_t and staff_t roles to manage user systemd services BZ(1531864)
- Update logging_read_all_logs to allow mmap all logfiles BZ(1403463)
- Add Label systemd_unit_file_t for /var/run/systemd/units/

* Mon Jan 08 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.14.1-1
- Removed big SELinux policy patches against tresys refpolicy and use tarballs from fedora-selinux github organisation

* Mon Jan 08 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-310
- Use python3 package in BuildRequires to ensure python version 3 will be used for compiling SELinux policy

* Fri Jan 05 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-309
- auth_use_nsswitch() interface cannot be used for attributes fixing munin policy
- Allow git_script_t to mmap git_user_content_t files BZ(1530937)
- Allow certmonger domain to create temp files BZ(1530795)
- Improve interface mock_read_lib_files() to include also symlinks. BZ(1530563)
- Allow fsdaemon_t to read nvme devices BZ(1530018)
- Dontaudit fsdaemon_t to write to admin homedir. BZ(153030)
- Update munin plugin policy BZ(1528471)
- Allow sendmail_t domain to be system dbusd client BZ(1478735)
- Allow amanda_t domain to getattr on tmpfs filesystem BZ(1527645)
- Allow named file transition to create rpmrebuilddb dir with proper SELinux context BZ(1461313)
- Dontaudit httpd_passwd_t domain to read state of systemd BZ(1522672)
- Allow thumb_t to mmap non security files BZ(1517393)
- Allow smbd_t to mmap files with label samba_share_t BZ(1530453)
- Fix broken sysnet_filetrans_named_content() interface
- Allow init_t to create tcp sockets for unconfined services BZ(1366968)
- Allow xdm_t to getattr on xserver_t process files BZ(1506116)
- Allow domains which can create resolv.conf file also create it in systemd_resolved_var_run_t dir BZ(1530297)
- Allow X userdomains to send dgram msgs to xserver_t BZ(1515967)
- Add interface files_map_non_security_files()

* Thu Jan 04 2018 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-308
- Make working SELinux sandbox with Wayland. BZ(1474082)
- Allow postgrey_t domain to mmap postgrey_spool_t files BZ(1529169)
- Allow dspam_t to mmap dspam_rw_content_t files BZ(1528723)
- Allow collectd to connect to lmtp_port_t BZ(1304029)
- Allow httpd_t to mmap httpd_squirrelmail_t files BZ(1528776)
- Allow thumb_t to mmap removable_t files. BZ(1522724)
- Allow sssd_t and login_pgm attribute to mmap auth_cache_t files BZ(1530118)
- Add interface fs_mmap_removable_files()

* Tue Dec 19 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-307
- Allow crond_t to read pcp lib files BZ(1525420)
- Allow mozilla plugin domain to mmap user_home_t files BZ(1452783)
- Allow certwatch_t to mmap generic certs. BZ(1527173)
- Allow dspam_t to manage dspam_rw_conent_t objects. BZ(1290876)
- Add interface userdom_map_user_home_files()
- Sytemd introduced new feature when journald(syslogd_t) is trying to read symlinks to unit files in /run/systemd/units. This commit label /run/systemd/units/* as systemd_unit_file_t and allow syslogd_t to read this content. BZ(1527202)
- Allow xdm_t dbus chat with modemmanager_t BZ(1526722)
- All domains accessing home_cert_t objects should also mmap it. BZ(1519810)

* Wed Dec 13 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-306
- Allow thumb_t domain to dosfs_t BZ(1517720)
- Allow gssd_t to read realmd_var_lib_t files BZ(1521125)
- Allow domain transition from logrotate_t to chronyc_t BZ(1436013)
- Allow git_script_t to mmap git_sys_content_t BZ(1517541)
- Label /usr/bin/mysqld_safe_helper as mysqld_exec_t instead of bin_t BZ(1464803)
- Label /run/openvpn-server/ as openvpn_var_run_t BZ(1478642)
- Allow colord_t to mmap xdm pid files BZ(1518382)
- Allow arpwatch to mmap usbmon device BZ(152456)
- Allow mandb_t to read public sssd files BZ(1514093)
- Allow ypbind_t stream connect to rpcbind_t domain BZ(1508659)
- Allow qpid to map files.
- Allow plymouthd_t to mmap firamebuf device BZ(1517405)
- Dontaudit pcp_pmlogger_t to sys_ptrace capability BZ(1416611)
- Update mta_manage_spool() interface to allow caller domain also mmap mta_spool_t files BZ(1517449)
- Allow antivirus_t domain to mmap antivirus_db_t files BZ(1516816)
- Allow cups_pdf_t domain to read cupd_etc_t dirs BZ(1516282)
- Allow openvpn_t domain to relabel networkmanager tun device BZ(1436048)
- Allow mysqld_t to mmap mysqld_tmp_t files BZ(1516899)
- Update samba_manage_var_files() interface by adding map permission. BZ(1517125)
- Allow pcp_pmlogger_t domain to execute itself. BZ(1517395)
- Dontaudit sys_ptrace capability for mdadm_t BZ(1515849)
- Allow pulseaudio_t domain to mmap pulseaudio_home_t files BZ(1515956)
- Allow bugzilla_script_t domain to create netlink route sockets and udp sockets BZ(1427019)
- Add interface fs_map_dos_files()
- Update interface userdom_manage_user_home_content_files() to allow caller domain to mmap user_home_t files. BZ(1519729)
- Add interface xserver_map_xdm_pid() BZ(1518382)
- Add new interface dev_map_usbmon_dev() BZ(1524256)
- Update miscfiles_read_fonts() interface to allow also mmap fonts_cache_t for caller domains BZ(1521137)
- Allow ipsec_t to mmap cert_t and home_cert_t files BZ(1519810)
- Fix typo in filesystem.if
- Add interface dev_map_framebuffer()
- Allow chkpwd command to mmap /etc/shadow BZ(1513704)
- Fix systemd-resolved to run properly with SELinux in enforcing state BZ(1517529)
- Allow thumb_t domain to mmap fusefs_t files BZ(1517517)
- Allow userdom_home_reader_type attribute to mmap cifs_t files BZ(1517125)
- Add interface fs_map_cifs_files()
- Merge pull request #207 from rhatdan/labels
- Merge pull request #208 from rhatdan/logdir
- Allow domains that manage logfiles to man logdirs

* Fri Nov 24 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-305
- Make ganesha nfs server

* Tue Nov 21 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-304
- Add interface raid_relabel_mdadm_var_run_content()
- Fix iscsi SELinux module
- Allow spamc_t domain to read home mail content BZ(1414366)
- Allow sendmail_t to list postfix config dirs BZ(1514868)
- Allow dovecot_t domain to mmap mail content in homedirs BZ(1513153)
- Allow iscsid_t domain to requesting loading kernel modules BZ(1448877)
- Allow svirt_t domain to mmap svirt_tmpfs_t files BZ(1515304)
- Allow cupsd_t domain to localization BZ(1514350)
- Allow antivirus_t nnp domain transition because of systemd security features. BZ(1514451)
- Allow tlp_t domain transition to systemd_rfkill_t domain BZ(1416301)
- Allow abrt_t domain to mmap fusefs_t files BZ(1515169)
- Allow memcached_t domain nnp_transition becuase of systemd security features BZ(1514867)
- Allow httpd_t domain to mmap all httpd content type BZ(1514866)
- Allow mandb_t to read /etc/passwd BZ(1514903)
- Allow mandb_t domain to mmap files with label mandb_cache_t BZ(1514093)
- Allow abrt_t domain to mmap files with label syslogd_var_run_t BZ(1514975)
- Allow nnp transition for systemd-networkd daemon to run in proper SELinux domain BZ(1507263)
- Allow systemd to read/write to mount_var_run_t files BZ(1515373)
- Allow systemd to relabel mdadm_var_run_t sock files BZ(1515373)
- Allow home managers to mmap nfs_t files BZ(1514372)
- Add interface fs_mmap_nfs_files()
- Allow systemd-mount to create new directory for mountpoint BZ(1514880)
- Allow getty to use usbttys
- Add interface systemd_rfkill_domtrans()
- Allow syslogd_t to mmap files with label syslogd_var_lib_t BZ(1513403)
- Add interface fs_mmap_fusefs_files()
- Allow ipsec_t domain to mmap files with label ipsec_key_file_t BZ(1514251)

* Thu Nov 16 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-303
- Allow pcp_pmlogger to send logs to journal BZ(1512367)
- Merge pull request #40 from lslebodn/kcm_kerberos
- Allow services to use kerberos KCM BZ(1512128)
- Allow system_mail_t domain to be system_dbus_client BZ(1512476)
- Allow aide domain to stream connect to sssd_t BZ(1512500)
- Allow squid_t domain to mmap files with label squid_tmpfs_t BZ(1498809)
- Allow nsd_t domain to mmap files with labels nsd_tmp_t and nsd_zone_t BZ(1511269)
- Include cupsd_config_t domain into cups_execmem boolean. BZ(1417584)
- Allow samba_net_t domain to mmap samba_var_t files BZ(1512227)
- Allow lircd_t domain to execute shell BZ(1512787)
- Allow thumb_t domain to setattr on cache_home_t dirs BZ(1487814)
- Allow redis to creating tmp files with own label BZ(1513518)
- Create new interface thumb_nnp_domtrans allowing domaintransition with NoNewPrivs. This interface added to thumb_run() BZ(1509502)
- Allow httpd_t to mmap httpd_tmp_t files BZ(1502303)
- Add map permission to samba_rw_var_files interface. BZ(1513908)
- Allow cluster_t domain creating bundles directory with label var_log_t instead of cluster_var_log_t
- Add dac_read_search and dac_override capabilities to ganesha
- Allow ldap_t domain to manage also slapd_tmp_t lnk files
- Allow snapperd_t domain to relabeling from snapperd_data_t BZ(1510584)
- Add dac_override capability to dhcpd_t doamin BZ(1510030)
- Allow snapperd_t to remove old snaps BZ(1510862)
- Allow chkpwd_t domain to mmap system_db_t files and be dbus system client BZ(1513704)
- Allow xdm_t send signull to all xserver unconfined types BZ(1499390)
- Allow fs associate for sysctl_vm_t BZ(1447301)
- Label /etc/init.d/vboxdrv as bin_t to run virtualbox as unconfined_service_t BZ(1451479)
- Allow xdm_t domain to read usermodehelper_t state BZ(1412609)
- Allow dhcpc_t domain to stream connect to userdomain domains BZ(1511948)
- Allow systemd to mmap kernel modules BZ(1513399)
- Allow userdomains to mmap fifo_files BZ(1512242)
- Merge pull request #205 from rhatdan/labels
- Add map permission to init_domtrans() interface BZ(1513832)
- Allow xdm_t domain to mmap and execute files in xdm_var_run_t BZ(1513883)
- Unconfined domains, need to create content with the correct labels
- Container runtimes are running iptables within a different user namespace
- Add interface files_rmdir_all_dirs()

* Mon Nov 06 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-302
- Allow jabber domains to connect to postgresql ports
- Dontaudit slapd_t to block suspend system
- Allow spamc_t to stream connect to cyrys.
- Allow passenger to connect to mysqld_port_t
- Allow ipmievd to use nsswitch
- Allow chronyc_t domain to use user_ptys
- Label all files /var/log/opensm.* as opensm_log_t because opensm creating new log files with name opensm-subnet.lst
- Fix typo bug in tlp module
- Allow userdomain gkeyringd domain to create stream socket with userdomain

* Fri Nov 03 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-301
- Merge pull request #37 from milosmalik/rawhide
- Allow mozilla_plugin_t domain to dbus chat with devicekit
- Dontaudit leaked logwatch pipes
- Label /usr/bin/VGAuthService as vmtools_exec_t to confine this daemon.
- Allow httpd_t domain to execute hugetlbfs_t files BZ(1444546)
- Allow chronyd daemon to execute chronyc. BZ(1507478)
- Allow pdns to read network system state BZ(1507244)
- Allow gssproxy to read network system state Resolves: rhbz#1507191
- Allow nfsd_t domain to read configfs_t files/dirs
- Allow tgtd_t domain to read generic certs
- Allow ptp4l to send msgs via dgram socket to unprivileged user domains
- Allow dirsrv_snmp_t to use inherited user ptys and read system state
- Allow glusterd_t domain to create own tmpfs dirs/files
- Allow keepalived stream connect to snmp

* Thu Oct 26 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-300
- Allow zabbix_t domain to change its resource limits
- Add new boolean nagios_use_nfs
- Allow system_mail_t to search network sysctls
- Hide all allow rules with ptrace inside deny_ptrace boolean
- Allow nagios_script_t to read nagios_spool_t files
- Allow sbd_t to create own sbd_tmpfs_t dirs/files
- Allow firewalld and networkmanager to chat with hypervkvp via dbus
- Allow dmidecode to read rhsmcert_log_t files
- Allow mail system to connect mariadb sockets.
- Allow nmbd_t domain to mmap files labeled as samba_var_t. BZ(1505877)
- Make user account setup in gnome-initial-setup working in Workstation Live system. BZ(1499170)
- Allow iptables_t to run setfiles to restore context on system
- Updatre unconfined_dontaudit_read_state() interface to dontaudit also acess to files. BZ(1503466)

* Tue Oct 24 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-299
- Label /usr/libexec/bluetooth/obexd as bluetoothd_exec_t to run process as bluetooth_t
- Allow chronyd_t do request kernel module and block_suspend capability
- Allow system_cronjob_t to create /var/lib/letsencrypt dir with right label
- Allow slapd_t domain to mmap files labeled as slpad_db_t BZ(1505414)
- Allow dnssec_trigger_t domain to execute binaries with dnssec_trigeer_exec_t BZ(1487912)
- Allow l2tpd_t domain to send SIGKILL to ipsec_mgmt_t domains BZ(1505220)
- Allow thumb_t creating thumb_home_t files in user_home_dir_t direcotry BZ(1474110)
- Allow httpd_t also read httpd_user_content_type dirs when httpd_enable_homedirs is enables
- Allow svnserve to use kerberos
- Allow conman to use ptmx. Add conman_use_nfs boolean
- Allow nnp transition for amavis and tmpreaper SELinux domains
- Allow chronyd_t to mmap chronyc_exec_t binary files
- Add dac_read_search capability to openvswitch_t domain
- Allow svnserve to manage own svnserve_log_t files/dirs
- Allow keepalived_t to search network sysctls
- Allow puppetagent_t domain dbus chat with rhsmcertd_t domain
- Add kill capability to openvswitch_t domain
- Label also compressed logs in /var/log for different services
- Allow inetd_child_t and system_cronjob_t to run chronyc.
- Allow chrony to create netlink route sockets
- Add SELinux support for chronyc
- Add support for running certbot(letsencrypt) in crontab
- Allow nnp trasintion for unconfined_service_t
- Allow unpriv user domains and unconfined_service_t to use chronyc

* Sun Oct 22 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-298
- Drop *.lst files from file list
- Ship file_contexts.homedirs in store
- Allow proper transition when systems starting pdns to pdns_t domain. BZ(1305522)
- Allow haproxy daemon to reexec itself. BZ(1447800)
- Allow conmand to use usb ttys.
- Allow systemd_machined to read mock lib files. BZ(1504493)
- Allow systemd_resolved_t to dbusd chat with NetworkManager_t BZ(1505081)

* Fri Oct 20 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-297
- Fix typo in virt file contexts file
- allow ipa_dnskey_t to read /proc/net/unix file
- Allow openvswitch to run setfiles in setfiles_t domain.
- Allow openvswitch_t domain to read process data of neutron_t domains
- Fix typo in ipa_cert_filetrans_named_content() interface
- Fix typo bug in summary of xguest SELinux module
- Allow virtual machine with svirt_t label to stream connect to openvswitch.
- Label qemu-pr-helper script as virt_exec_t so this script won't run as unconfined_service_t

* Tue Oct 17 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-296
- Merge pull request #19 from RodrigoQuesadaDev/snapper-fix-1
- Allow httpd_t domain to mmap httpd_user_content_t files. BZ(1494852)
- Add nnp transition rule for services using NoNewPrivileges systemd feature
- Add map permission into dev_rw_infiniband_dev() interface to allow caller domain mmap infiniband chr device BZ(1500923)
- Add init_nnp_daemon_domain interface
- Allow nnp transition capability
- Merge pull request #204 from konradwilk/rhbz1484908
- Label postgresql-check-db-dir as postgresql_exec_t

* Tue Oct 10 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-295
- Allow boinc_t to mmap files with label boinc_project_var_lib_t BZ(1500088)
- Allow fail2ban_t domain to mmap journals. BZ(1500089)
- Add dac_override to abrt_t domain BZ(1499860)
- Allow pppd domain to mmap own pid files BZ(1498587)
- Allow webserver services to mmap files with label httpd_sys_content_t BZ(1498451)
- Allow tlp domain to read sssd public files Allow tlp domain to mmap kernel modules
- Allow systemd to read sysfs sym links. BZ(1499327)
- Allow systemd to mmap systemd_networkd_exec_t files BZ(1499863)
- Make systemd_networkd_var_run as mountpoint BZ(1499862)
- Allow noatsecure for java-based unconfined services. BZ(1358476)
- Allow systemd_modules_load_t domain to mmap kernel modules. BZ(1490015)

* Mon Oct 09 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-294
- Allow cloud-init to create content in /var/run/cloud-init
- Dontaudit VM to read gnome-boxes process data BZ(1415975)
- Allow winbind_t domain mmap samba_var_t files
- Allow cupsd_t to execute ld_so_cache_t BZ(1478602)
- Update dev_rw_xserver_misc() interface to allo source domains to mmap xserver devices BZ(1334035)
- Add dac_override capability to groupadd_t domain BZ(1497091)
- Allow unconfined_service_t to start containers

* Sun Oct 08 2017 Petr Lautrbach <plautrba@redhat.com> - 3.13.1-293
- Drop policyhelp utility BZ(1498429)

* Tue Oct 03 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-292
- Allow cupsd_t to execute ld_so_cache_t BZ(1478602)
- Allow firewalld_t domain to change object identity because of relabeling after using firewall-cmd BZ(1469806)
- Allow postfix_cleanup_t domain to stream connect to all milter sockets BZ(1436026)
- Allow nsswitch_domain to read virt_var_lib_t files, because of libvirt NSS plugin. BZ(1487531)
- Add unix_stream_socket recvfrom perm for init_t domain BZ(1496318)
- Allow systemd to maange sysfs BZ(1471361)

* Tue Oct 03 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-291
- Switch default value of SELinux boolean httpd_graceful_shutdown to off.

* Fri Sep 29 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-290
- Allow virtlogd_t domain to write inhibit systemd pipes.
- Add dac_override capability to openvpn_t domain
- Add dac_override capability to xdm_t domain
- Allow dac_override to groupadd_t domain BZ(1497081)
- Allow cloud-init to create /var/run/cloud-init dir with net_conf_t SELinux label.BZ(1489166)

* Wed Sep 27 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-289
- Allow tlp_t domain stream connect to sssd_t domain
- Add missing dac_override capability
- Add systemd_tmpfiles_t dac_override capability

* Fri Sep 22 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-288
- Remove all unnecessary dac_override capability in SELinux modules

* Fri Sep 22 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-287
- Allow init noatsecure httpd_t
- Allow mysqld_t domain to mmap mysqld db files. BZ(1483331)
- Allow unconfined_t domain to create new users with proper SELinux lables
-  Allow init noatsecure httpd_t
- Label tcp port 3269 as ldap_port_t

* Mon Sep 18 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-286
- Add new boolean tomcat_read_rpm_db()
- Allow tomcat to connect on mysqld tcp ports
- Add new interface apache_delete_tmp()
- Add interface fprintd_exec()
- Add interface fprintd_mounton_var_lib()
- Allow mozilla plugin to mmap video devices BZ(1492580)
- Add ctdbd_t domain sys_source capability and allow setrlimit
- Allow systemd-logind to use ypbind
- Allow systemd to remove apache tmp files
- Allow ldconfig domain to mmap ldconfig cache files
- Allow systemd to exec fprintd BZ(1491808)
- Allow systemd to mounton fprintd lib dir

* Thu Sep 14 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-285
- Allow svirt_t read userdomain state

* Thu Sep 14 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-284
- Allow mozilla_plugins_t domain mmap mozilla_plugin_tmpfs_t files
- Allow automount domain to manage mount pid files
- Allow stunnel_t domain setsched
- Add keepalived domain setpgid capability
- Merge pull request #24 from teg/rawhide
- Merge pull request #28 from lslebodn/revert_1e8403055
- Allow sysctl_irq_t assciate with proc_t
- Enable cgourp sec labeling
- Allow sshd_t domain to send signull to xdm_t processes

* Tue Sep 12 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-283
- Allow passwd_t domain mmap /etc/shadow and /etc/passwd
- Allow pulseaudio_t domain to map user tmp files
- Allow mozilla plugin to mmap mozilla tmpfs files

* Mon Sep 11 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-282
- Add new bunch of map rules
- Merge pull request #25 from NetworkManager/nm-ovs
- Make working webadm_t userdomain
- Allow redis domain to execute shell scripts.
- Allow system_cronjob_t to create redhat-access-insights.log with var_log_t
- Add couple capabilities to keepalived domain and allow get attributes of all domains
- Allow dmidecode read rhsmcertd lock files
- Add new interface rhsmcertd_rw_lock_files()
- Add new bunch of map rules
- Merge pull request #199 from mscherer/add_conntrackd
- Add support labeling for vmci and vsock device
- Add userdom_dontaudit_manage_admin_files() interface

* Mon Sep 11 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-281
- Allow domains reading raw memory also use mmap.

* Thu Sep 07 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-280
- Add rules fixing installing ipa-server-install with SELinux in Enforcing. BZ(1488404)
- Fix denials during ipa-server-install process on F27+
- Allow httpd_t to mmap cert_t
- Add few rules to make tlp_t domain working in enforcing mode
- Allow cloud_init_t to dbus chat with systemd_timedated_t
- Allow logrotate_t to write to kmsg
- Add capability kill to rhsmcertd_t
- Allow winbind to manage smbd_tmp_t files
- Allow groupadd_t domain to dbus chat with systemd.BZ(1488404)
- Add interface miscfiles_map_generic_certs()

* Tue Sep 05 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-279
- Allow abrt_dump_oops_t to read sssd_public_t files
- Allow cockpit_ws_t to mmap usr_t files
- Allow systemd to read/write dri devices.

* Thu Aug 31 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-278
- Add couple rules related to map permissions
- Allow ddclient use nsswitch BZ(1456241)
- Allow thumb_t domain getattr fixed_disk device. BZ(1379137)
- Add interface dbus_manage_session_tmp_dirs()
- Dontaudit useradd_t sys_ptrace BZ(1480121)
- Allow ipsec_t can exec ipsec_exec_t
- Allow systemd_logind_t to mamange session_dbusd_tmp_t dirs

* Mon Aug 28 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-277
- Allow cupsd_t to execute ld_so_cache
- Add cgroup_seclabel policycap.
- Allow xdm_t to read systemd hwdb
- Add new interface systemd_hwdb_mmap_config()
- Allow auditd_t domain to mmap conf files labeled as auditd_etc_t BZ(1485050)

* Sat Aug 26 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-276
- Allow couple map rules

* Wed Aug 23 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-275
- Make confined users working
- Allow ipmievd_t domain to load kernel modules
- Allow logrotate to reload transient systemd unit

* Wed Aug 23 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-274
- Allow postgrey to execute bin_t files and add postgrey into nsswitch_domain
- Allow nscd_t domain to search network sysctls
- Allow iscsid_t domain to read mount pid files
- Allow ksmtuned_t domain manage sysfs_t files/dirs
- Allow keepalived_t domain domtrans into iptables_t
- Allow rshd_t domain reads net sysctls
- Allow systemd to create syslog netlink audit socket
- Allow ifconfig_t domain unmount fs_t
- Label /dev/gpiochip* devices as gpio_device_t

* Tue Aug 22 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-273
- Allow dirsrv_t domain use mmap on files labeled as dirsrv_var_run_t BZ(1483170)
- Allow just map permission insead of using mmap_file_pattern because mmap_files_pattern allows also executing objects.
- Label /var/run/agetty.reload as getty_var_run_t
- Add missing filecontext for sln binary
- Allow systemd to read/write to event_device_t BZ(1471401)

* Tue Aug 15 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-272
- Allow sssd_t domain to map sssd_var_lib_t files
- allow map permission where needed
- contrib: allow map permission where needed
- Allow syslogd_t to map syslogd_var_run_t files
- allow map permission where needed

* Mon Aug 14 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-271
- Allow tomcat_t domain couple capabilities to make working tomcat-jsvc
- Label /usr/libexec/sudo/sesh as shell_exec_t

* Thu Aug 10 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-270
- refpolicy: Infiniband pkeys and endport

* Thu Aug 10 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-269
- Allow osad make executable an anonymous mapping or private file mapping that is writable BZ(1425524)
- After fix in kernel where LSM hooks for dac_override and dac_search_read capability was swaped we need to fix it also in policy
- refpolicy: Define and allow map permission
- init: Add NoNewPerms support for systemd.
- Add nnp_nosuid_transition policycap and related class/perm definitions.

* Mon Aug 07 2017 Petr Lautrbach <plautrba@redhat.com> - 3.13.1-268
- Update for SELinux userspace release 20170804 / 2.7
- Omit precompiled regular expressions from file_contexts.bin files

* Mon Aug 07 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-267
- After fix in kernel where LSM hooks for dac_override and dac_search_read capability was swaped we need to fix it also in policy

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.1-266
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-265
- Allow llpdad send dgram to libvirt
- Allow abrt_t domain dac_read_search capability
- Allow init_t domain mounton dirs labeled as init_var_lib_t BZ(1471476)
- Allow xdm_t domain read unique machine-id generated during system installation. BZ(1467036)
- Dontaudit xdm_t to setattr lib_t dirs. BZ(#1458518)

* Mon Jul 17 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-264
- Dontaudit xdm_t to setattr lib_t dirs. BZ(#1458518)

* Tue Jul 11 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-263
- Add new boolean gluster_use_execmem

* Mon Jul 10 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-262
- Allow cluster_t and glusterd_t domains to dbus chat with ganesha service
- Allow iptables to read container runtime files

* Fri Jun 23 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-261
- Allow boinc_t nsswitch
- Dontaudit firewalld to write to lib_t dirs
- Allow modemmanager_t domain to write to raw_ip file labeled as sysfs_t
- Allow thumb_t domain to allow create dgram sockets
- Disable mysqld_safe_t secure mode environment cleansing
- Allow couple rules needed to start targetd daemon with SELinux in enforcing mode
- Allow dirsrv domain setrlimit
- Dontaudit staff_t user read admin_home_t files.
- Add interface lvm_manage_metadata
- Add permission open to files_read_inherited_tmp_files() interface

* Mon Jun 19 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-260
- Allow sssd_t to read realmd lib files.
- Fix init interface file. init_var_run_t is type not attribute

* Mon Jun 19 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-258
- Allow rpcbind_t to execute systemd_tmpfiles_exec_t binary files.
- Merge branch 'rawhide' of github.com:wrabcak/selinux-policy-contrib into rawhide
- Allow qemu to authenticate SPICE connections with SASL GSSAPI when SSSD is in use
- Fix dbus_dontaudit_stream_connect_system_dbusd() interface to require TYPE rather than ATTRIBUTE for systemd_dbusd_t.
- Allow httpd_t to read realmd_var_lib_t files
- Allow unconfined_t user all user namespace capabilties.
- Add interface systemd_tmpfiles_exec()
- Add interface libs_dontaudit_setattr_lib_files()
- Dontaudit xdm_t domain to setattr on lib_t dirs
- Allow sysadm_r role to jump into dirsrv_t

* Thu Jun 08 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-257
- Merge pull request #10 from mscherer/fix_tor_dac
- Merge pull request #9 from rhatdan/rawhide
- Merge pull request #13 from vinzent/allow_zabbix_t_to_kill_zabbix_script_t
- Allow kdumpgui to read removable disk device
- Allow systemd_dbusd_t domain read/write to nvme devices
- Allow udisks2 domain to read removable devices BZ(1443981)
- Allow virtlogd_t to execute itself
- Allow keepalived to read/write usermodehelper state
- Allow named_t to bind on udp 4321 port
- Fix interface tlp_manage_pid_files()
- Allow collectd domain read lvm config files. BZ(1459097)
- Merge branch 'rawhide' of github.com:wrabcak/selinux-policy-contrib into rawhide
- Allow samba_manage_home_dirs boolean to manage user content
- Merge pull request #14 from lemenkov/rabbitmq_systemd_notify
- Allow pki_tomcat_t execute ldconfig.
- Merge pull request #191 from rhatdan/udev
- Allow systemd_modules_load_t to load modules

* Mon Jun 05 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-256
- Allow keepalived domain connect to squid tcp port
- Allow krb5kdc_t domain read realmd lib files.
- Allow tomcat to connect on all unreserved ports
- Allow keepalived domain connect to squid tcp port
- Allow krb5kdc_t domain read realmd lib files.
- Allow tomcat to connect on all unreserved ports
- Allow ganesha to connect to all rpc ports
- Update ganesha with few allow rules
- Update rpc_read_nfs_state_data() interface to allow read also lnk_files.
- virt_use_glusterd boolean should be in optional block
- Add new boolean virt_use_glusterd
- Add capability sys_boot for sbd_t domain Allow sbd_t domain to create rpc sysctls.
- Allow ganesha_t domain to manage glusterd_var_run_t pid files.
- Create new interface: glusterd_read_lib_files() Allow ganesha read glusterd lib files. Allow ganesha read network sysctls
- Add few allow rules to ganesha module
- Allow condor_master_t to read sysctls.
- Add dac_override cap to ctdbd_t domain
- Add ganesha_use_fusefs boolean.
- Allow httpd_t reading kerberos kdc config files
- Allow tomcat_t domain connect to ibm_dt_2 tcp port.
- Allow stream connect to initrc_t domains
- Add pki_exec_common_files() interface
- Allow  dnsmasq_t domain to read systemd-resolved pid files.
- Allow tomcat domain name_bind on tcp bctp_port_t
- Allow smbd_t domain generate debugging files under /var/run/gluster. These files are created through the libgfapi.so library that provides integration of a GlusterFS client in the Samba (vfs_glusterfs) process.
- Allow condor_master_t write to sysctl_net_t
- Allow nagios check disk plugin read /sys/kernel/config/
- Allow pcp_pmie_t domain execute systemctl binary
- Allow nagios to connect to stream sockets. Allow nagios start httpd via systemctl
- xdm_t should view kernel keys
- Hide broken symptoms when machine is configured with network bounding.
- Label 8750 tcp/udp port as dey_keyneg_port_t
- Label tcp/udp port 1792 as ibm_dt_2_port_t
- Add interface fs_read_configfs_dirs()
- Add interface fs_read_configfs_files()
- Fix systemd_resolved_read_pid interface
- Add interface systemd_resolved_read_pid()
- Allow sshd_net_t domain read/write into crypto devices
- Label 8999 tcp/udp as bctp_port_t

* Thu May 18 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-255
- Dontaudit net_admin capability for domains postfix_master_t and postfix_qmgr_t
- Add interface pki_manage_common_files()
- Allow rngd domain read sysfs_t
- Allow tomcat_t domain to manage pki_common_t files and dirs
- Merge pull request #3 from rhatdan/devicekit
- Merge pull request #12 from lslebodn/sssd_sockets_fc
- Allow certmonger reads httpd_config_t files
- Allow keepalived_t domain creating netlink_netfilter_socket.
- Use stricter fc rules for sssd sockets in /var/run
- Allow tomcat domain read rpm_var_lib_t files Allow tomcat domain exec rpm_exec_t files Allow tomcat domain name connect on oracle_port_t Allow tomcat domain read cobbler_var_lib_t files.
- Allow sssd_t domain creating sock files labeled as sssd_var_run_t in /var/run/
- Allow svirt_t to read raw fixed_disk_device_t to make working blockcommit
- ejabberd small fixes
- Update targetd policy to accommodate changes in the service
- Allow tomcat_domain connect to    * postgresql_port_t    * amqp_port_t Allow tomcat_domain read network sysctls
- Allow virt_domain to read raw fixed_disk_device_t to make working blockcommit
- Dontaudit net_admin capability for useradd_t domain
- Allow systemd_localed_t and systemd_timedated_t create files in /etc with label locate_t BZ(1443723)
- Make able deply overcloud via neutron_t to label nsfs as fs_t
- Add fs_manage_configfs_lnk_files() interface

* Mon May 15 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-254
- Allow svirt_t to read raw fixed_disk_device_t to make working blockcommit
- ejabberd small fixes
- Update targetd policy to accommodate changes in the service
- Allow tomcat_domain connect to    * postgresql_port_t    * amqp_port_t Allow tomcat_domain read network sysctls
- Allow virt_domain to read raw fixed_disk_device_t to make working blockcommit
- Allow glusterd_t domain start ganesha service
- Made few cosmetic changes in sssd SELinux module
- Merge pull request #11 from lslebodn/sssd_kcm
- Update virt_rw_stream_sockets_svirt() interface to allow confined users set socket options.
- Allow keepalived_t domain read usermodehelper_t
- Allow radius domain stream connec to postgresql
- Merge pull request #8 from bowlofeggs/142-rawhide
- Add fs_manage_configfs_lnk_files() interface

* Fri May 12 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-253
- auth_use_nsswitch can call only domain not attribute
- Dontaudit net_admin cap for winbind_t
- Allow tlp_t domain to stream connect to system bus
- Allow tomcat_t domain read pki_common_t files
- Add interface pki_read_common_files()
- Fix broken cermonger module
- Fix broken apache module
- Allow hypervkvp_t domain execute hostname
- Dontaudit sssd_selinux_manager_t use of net_admin capability
- Allow tomcat_t stream connect to pki_common_t
- Dontaudit xguest_t's attempts to listen to its tcp_socket
- Allow sssd_selinux_manager_t to ioctl init_t sockets
- Improve ipa_cert_filetrans_named_content() interface to also allow caller domain manage ipa_cert_t type.
- Allow pki_tomcat_t domain read /etc/passwd.
- Allow tomcat_t domain read ipa_tmp_t files
- Label new path for ipa-otpd
- Allow radiusd_t domain stream connect to postgresql_t
- Allow rhsmcertd_t to execute hostname_exec_t binaries.
- Allow virtlogd to append nfs_t files when virt_use_nfs=1
- Allow httpd_t domain read also httpd_user_content_type lnk_files.
- Allow httpd_t domain create /etc/httpd/alias/ipaseesion.key with label ipa_cert_t
- Dontaudit <user>_gkeyringd_t stream connect to system_dbusd_t
- Label /var/www/html/nextcloud/data as httpd_sys_rw_content_t
- Add interface ipa_filetrans_named_content()
- Allow tomcat use nsswitch
- Allow certmonger_t start/status generic services
- Allow dirsrv read cgroup files.
- Allow ganesha_t domain read/write infiniband devices.
- Allow sendmail_t domain sysctl_net_t files
- Allow targetd_t domain read network state and getattr on loop_control_device_t
- Allow condor_schedd_t domain send mails.
- Allow ntpd to creating sockets. BZ(1434395)
- Alow certmonger to create own systemd unit files.
- Add kill namespace capability to xdm_t domain
- Revert "su using libselinux and creating netlink_selinux socket is needed to allow libselinux initialization."
- Revert "Allow <role>_su_t to create netlink_selinux_socket"
- Allow <role>_su_t to create netlink_selinux_socket
- Allow unconfined_t to module_load any file
- Allow staff to systemctl virt server when staff_use_svirt=1
- Allow unconfined_t create /tmp/ca.p12 file with ipa_tmp_t context
- Allow netutils setpcap capability
- Dontaudit leaked file descriptor happening in setfiles_t domain BZ(1388124)

* Thu Apr 20 2017 Michael Scherer <misc@fedoraproject.org> - 3.13.1-252
- fix #1380325, selinux-policy-sandbox always removing sandbox module on upgrade

* Tue Apr 18 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-251
- Fix abrt module to reflect all changes in abrt release

* Tue Apr 18 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-250
- Allow tlp_t domain to ioctl removable devices BZ(1436830)
- Allow tlp_t domain domtrans into mount_t BZ(1442571)
- Allow lircd_t to read/write to sysfs BZ(1442443)
- Fix policy to reflect all changes in new IPA release
- Allow virtlogd_t to creating tmp files with virt_tmp_t labels.
- Allow sbd_t to read/write fixed disk devices
- Add sys_ptrace capability to radiusd_t domain
- Allow cockpit_session_t domain connects to ssh tcp ports.
- Update tomcat policy to make working ipa install process
- Allow pcp_pmcd_t net_admin capability. Allow pcp_pmcd_t read net sysctls Allow system_cronjob_t create /var/run/pcp with pcp_var_run_t
- Fix all AVC denials during pkispawn of CA Resolves: rhbz#1436383
- Update pki interfaces and tomcat module
- Allow sendmail to search network sysctls
- Add interface gssd_noatsecure()
- Add interface gssproxy_noatsecure()
- Allow chronyd_t net_admin capability to allow support HW timestamping.
- Update tomcat policy.
- Allow certmonger to start haproxy service
- Fix init Module
- Make groupadd_t domain as system bus client BZ(1416963)
- Make useradd_t domain as system bus client BZ(1442572)
- Allow xdm_t to gettattr /dev/loop-control device BZ(1385090)
- Dontaudit gdm-session-worker to view key unknown. BZ(1433191)
- Allow init noatsecure for gssd and gssproxy
- Allow staff user to read fwupd_cache_t files
- Remove typo bugs
- Remove /proc <<none>> from fedora policy, it's no longer necessary

* Mon Apr 03 2017 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-249
- Merge pull request #4 from lslebodn/sssd_socket_activated
- Remove /proc <<none>> from fedora policy, it's no longer necessary
- Allow iptables get list of kernel modules
- Allow unconfined_domain_type to enable/disable transient unit
- Add interfaces init_enable_transient_unit() and init_disable_transient_unit
- Revert "Allow sshd setcap capability. This is needed due to latest changes in sshd"
- Label sysroot dir under ostree as root_t

* Mon Mar 27 2017 Adam Williamson <awilliam@redhat.com> - 3.13.1-248
- Put tomcat_t back in unconfined domains for now. BZ(1436434)

* Tue Mar 21 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-247
- Make fwupd_var_lib_t type mountpoint. BZ(1429341)
- Remove tomcat_t domain from unconfined domains
- Create new boolean: sanlock_enable_home_dirs()
- Allow mdadm_t domain to read/write nvme_device_t
- Remove httpd_user_*_content_t domains from user_home_type attribute. This tighten httpd policy and acces to user data will be more strinct, and also fix mutual influente between httpd_enable_homedirs and httpd_read_user_content
- Add interface dev_rw_nvme
- Label all files containing hostname substring in /etc/ created by systemd_hostnamed_t as hostname_etc_t. BZ(1433555)

* Sat Mar 18 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-246
- Label all files containing hostname substring in /etc/ created by systemd_hostnamed_t as hostname_etc_t. BZ(1433555)

* Fri Mar 17 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-245
- Allow vdagent domain to getattr cgroup filesystem
- Allow abrt_dump_oops_t stream connect to sssd_t domain
- Allow cyrus stream connect to gssproxy
- Label /usr/libexec/cockpit-ssh as cockpit_session_exec_t and allow few rules
- Allow colord_t to read systemd hwdb.bin file
- Allow dirsrv_t to create /var/lock/dirsrv labeled as dirsrc_var_lock_t
- Allow certmonger to manage /etc/krb5kdc_conf_t
- Allow kdumpctl to getenforce
- Allow ptp4l wake_alarm capability
- Allow ganesha to chat with unconfined domains via dbus
- Add nmbd_t capability2 block_suspend
- Add domain transition from sosreport_t to iptables_t
- Dontaudit init_t to mounton modules_object_t
- Add interface files_dontaudit_mounton_modules_object
- Allow xdm_t to execute files labeled as xdm_var_lib_t
- Make mtrr_device_t mountpoint.
- Fix path to /usr/lib64/erlang/erts-5.10.4/bin/epmd

* Tue Mar 07 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-244
- Update fwupd policy
- /usr/libexec/udisks2/udisksd should be labeled as devicekit_disk_exec_t
- Update ganesha policy
- Allow chronyd to read adjtime
- Merge pull request #194 from hogarthj/certbot_policy
- get the correct cert_t context on certbot certificates bz#1289778
- Label /dev/ss0 as gpfs_device_t

* Thu Mar 02 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-243
-  Allow abrt_t to send mails.

* Mon Feb 27 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-242
- Add radius_use_jit boolean
- Allow nfsd_t domain to create sysctls_rpc_t files
- add the policy required for nextcloud
- Allow can_load_kernmodule to load kernel modules. BZ(1426741)
- Create kernel_create_rpc_sysctls() interface

* Tue Feb 21 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-241
- Remove ganesha from gluster module and create own module for ganesha
- FIx label for /usr/lib/libGLdispatch.so.0.0.0

* Wed Feb 15 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-240
- Dontaudit xdm_t wake_alarm capability2
- Allow systemd_initctl_t to create and connect unix_dgram sockets
- Allow ifconfig_t to mount/unmount nsfs_t filesystem
- Add interfaces allowing mount/unmount nsfs_t filesystem
- Label /usr/lib/libGLdispatch.so.0.0.0 as textrel_shlib_t BZ(1419944)

* Mon Feb 13 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-239
- Allow syslog client to connect to kernel socket. BZ(1419946)

* Thu Feb 09 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-238
- Allow shiftfs to use xattr SELinux labels
- Fix ssh_server_template by add sshd_t to require section.

* Wed Feb 08 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-237
- Merge pull request #187 from rhatdan/container-selinux
- Allow rhsmcertd domain signull kernel.
- Allow container-selinux to handle all policy for container processes
- Fix label for nagios plugins in nagios file conxtext file
- su using libselinux and creating netlink_selinux socket is needed to allow libselinux initialization. Resolves: rhbz#1146987
- Add SELinux support for systemd-initctl daemon
- Add SELinux support for systemd-bootchart
- su using libselinux and creating netlink_selinux socket is needed to allow libselinux initialization. Resolves: rhbz#1146987
- Add module_load permission to can_load_kernmodule
- Add module_load permission to class system
- Add the validate_trans access vector to the security class
- Restore connecto permssions for init_t

* Thu Feb 02 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-236
- Allow kdumpgui domain to read nvme device
- Add amanda_tmpfs_t label. BZ(1243752)
- Fix typo in sssd interface file
- Allow sssd_t domain setpgid BZ(1411437)
- Allow ifconfig_t domain read nsfs_t
- Allow ping_t domain to load kernel modules.
- Allow systemd to send user information back to pid1. BZ(1412750)
- rawhide-base: Fix wrong type/attribute flavors in require blocks

* Tue Jan 17 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-235
- Allow libvirt daemon to create /var/chace/libvirt dir.
- Allow systemd using ProtectKernelTunables securit feature. BZ(1392161)
- F26 Wide change: Coredumps enabled by default. Allowing inherits process limits to enable coredumps.BZ(1341829)

* Tue Jan 17 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-234
- After the latest changes in nfsd. We should allow nfsd_t to read raw fixed disk. For more info see: BZ(1403017)
- Tighten security on containe types
- Make working cracklib_password_check for MariaDB service
- Label 20514 tcp/udp ports as syslogd_port_t Label 10514 tcp/udp portas as syslog_tls_port_t BZ(1410505)

* Sun Jan 08 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-233
-Allow thumb domain sendto via dgram sockets. BZ(1398813)
- Add condor_procd_t domain sys_ptrace cap_userns BZ(1411077)
- Allow cobbler domain to create netlink_audit sockets BZ(1384600)
- Allow networkmanager to manage networkmanager_var_lib_t lnk files BZ(1408626)
- Add dhcpd_t domain fowner capability BZ(1409963)
- Allow thumb to create netlink_kobject_uevent sockets. BZ(1410942)
- Fix broken interfaces
- Allow setfiles_t domain rw inherited kdumpctl tmp pipes BZ(1356456)
- Allow user_t run systemctl --user BZ(1401625)

* Fri Jan 06 2017 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-232
- Add tlp_var_lib_t label for /var/lib/tlp directory BZ(1409977)
- Allow tlp_t domain to read proc_net_t BZ(1403487)
- Merge pull request #179 from rhatdan/virt1
- Allow tlp_t domain to read/write cpu microcode BZ(1403103)
- Allow virt domain to use interited virtlogd domains fifo_file
- Fixes for containers
- Allow glusterd_t to bind on glusterd_port_t udp ports.
- Update ctdbd_t policy to reflect all changes.
- Allow ctdbd_t domain transition to rpcd_t

* Wed Dec 14 2016 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-231
- Allow pptp_t to read /dev/random BZ(1404248)
- Allow glusterd_t send signals to userdomain. Label new glusterd binaries as glusterd_exec_t
- Allow systemd to stop glusterd_t domains.
- Merge branch 'rawhide-base' of github.com:fedora-selinux/selinux-policy into rawhide-base
- Label /usr/sbin/sln as ldconfig_exec_t BZ(1378323)
- Revert "Allow an domain that has an entrypoint from a type to be allowed to execute the entrypoint without a transition,  I can see no case where this is  a bad thing, and elminiates a whole class of AVCs."

* Thu Dec 08 2016 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-230
- Label /usr/bin/rpcbind as rpcbind_exec_t
- Dontaudit mozilla plugin rawip socket creation. BZ(1275961)
- Merge pull request #174 from rhatdan/netlink

* Wed Dec 07 2016 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-229
- Label /usr/bin/rpcbind as rpcbind_exec_t. Label /usr/lib/systemd/systemd/rpcbind.service
- Allot tlp domain to create unix_dgram sockets BZ(1401233)
- Allow antivirus domain to create lnk_files in /tmp
- Allow cupsd_t to create lnk_files in /tmp. BZ(1401634)
- Allow svnserve_t domain to read /dev/random BZ(1401827)
- Allow lircd to use nsswitch. BZ(1401375)
- Allow hostname_t domain to manage cluster_tmp_t files

* Mon Dec 05 2016 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-228
- Fix some boolean descriptions.
- Add fwupd_dbus_chat() interface
- Allow tgtd_t domain wake_alarm
- Merge pull request #172 from vinzent/allow_puppetagent_timedated
- Dontaudit logrotate_t to getattr nsfs_t BZ(1399081)
- Allow systemd_machined_t to start unit files labeled as init_var_run_t
- Add init_manage_config_transient_files() interface
- In Atomic /usr/local is a soft symlink to /var/usrlocal, so the default policy to apply bin_t on /usr/...bin doesn't work and binaries dumped here get mislabeled as var_t.
- Allow systemd to raise rlimit to all domains.BZ(1365435)
- Add interface domain_setrlimit_all_domains() interface
- Allow staff_t user to chat with fwupd_t domain via dbus
- Update logging_create_devlog_dev() interface to allow calling domain create also sock_file dev-log. BZ(1393774)
- Allow systemd-networkd to read network state BZ(1400016)
- Allow systemd-resolved bind to dns port. BZ(1400023)
- Allow systemd create /dev/log in own mount-namespace. BZ(1383867)
- Add interface fs_dontaudit_getattr_nsfs_files()
- Label /usr/lib/systemd/resolv.conf as lib_t to allow all domains read this file. BZ(1398853)

* Tue Nov 29 2016 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-227
- Dontaudit logrotate_t to getattr nsfs_t BZ(1399081)
- Allow pmie daemon to send signal pcmd daemon BZ(1398078)
- Allow spamd_t to manage /var/spool/mail. BZ(1398437)
- Label /run/rpc.statd.lock as rpcd_lock_t and allow rpcd_t domain to manage it. BZ(1397254)
- Merge pull request #171 from t-woerner/rawhide-contrib
- Allow firewalld to getattr open search read modules_object_t:dir
- Allow systemd create /dev/log in own mount-namespace. BZ(1383867)
- Add interface fs_dontaudit_getattr_nsfs_files()
- Label /usr/lib/systemd/resolv.conf as lib_t to allow all domains read this file. BZ(1398853)
- Dontaudit systemd_journal sys_ptrace userns capability. BZ(1374187)

* Wed Nov 16 2016 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-226
- Adding policy for tlp
- Add interface  dev_manage_sysfs()
- Allow ifconfig domain to manage tlp pid files.

* Wed Nov 09 2016 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-225
- Allow systemd_logind_t domain to communicate with devicekit_t domain via dbus bz(1393373)

* Tue Nov 08 2016 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-224
- Allow watching netflix using Firefox

* Mon Nov 07 2016 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-223
- nmbd_t needs net_admin capability like smbd
- Add interface chronyd_manage_pid() Allow logrotate to manage chrony pids
- Add wake_alarm capability2 to openct_t domain
- Allow abrt_t to getattr on nsfs_t files.
- Add cupsd_t domain wake_alarm capability.
- Allow sblim_reposd_t domain to read cert_f files.
- Allow abrt_dump_oops_t to drop capabilities. bz(1391040)
- Revert "Allow abrt_dump_oops_t to drop capabilities. bz(1391040)"
- Allow isnsd_t to accept tcp connections

* Wed Nov 02 2016 Lukas Vrabec  <lvrabec@redhat.com> - 3.13.1-222
- Allow abrt_dump_oops_t to drop capabilities. bz(1391040)
- Add named_t domain net_raw capability bz(1389240)
- Allow geoclue to read system info. bz(1389320)
- Make openfortivpn_t as init_deamon_domain. bz(1159899)
- Allow nfsd domain to create nfsd_unit_file_t files. bz(1382487)
- Merge branch 'rawhide-contrib' of github.com:fedora-selinux/selinux-policy into rawhide-contrib
- Add interace lldpad_relabel_tmpfs
- Merge pull request #155 from rhatdan/sandbox_nfs
- Add pscsd_t wake_alarm capability2
- Allow sandbox domains to mount fuse file systems
- Add boolean to allow sandbox domains to mount nfs
- Allow hypervvssd_t to read all dirs.
- Allow isnsd_t to connect to isns_port_t
- Merge branch 'rawhide-contrib' of github.com:fedora-selinux/selinux-policy into rawhide-contrib
- Allow GlusterFS with RDMA transport to be started correctly. It requires ipc_lock capability together with rw permission on rdma_cm device.
- Make tor_var_lib_t and tor_var_log_t as mountpoints.
- Allow systemd-rfkill to write to /proc/kmsg bz(1388669)
- Allow init_t to relabel /dev/shm/lldpad.state
- Merge pull request #168 from rhatdan/docker
- Label tcp 51954 as isns_port_t
- Lots of new domains like OCID and RKT are user container processes

* Mon Oct 17 2016 Miroslav Grepl <mgrepl@redhat.com> - 3.13.1-221
- Add container_file_t into contexts/customizable_types.

* Sun Oct 16 2016 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-220
- Disable container_runtime_typebounds() due to typebounds issues which can not be resolved during build.
- Disable unconfined_typebounds in sandbox.te due to entrypoint check which exceed for sandbox domains unconfined_t domain.
- Disable unconfined_typebounds due to entrypoint check which exceed for sandbox domains unconfined_t domain.
- Merge pull request #167 from rhatdan/container
- Add transition rules for sandbox domains
- container_typebounds() should be part of sandbox domain template
- Fix broken container_* interfaces
- unconfined_typebounds() should be part of sandbox domain template
- Fixed unrecognized characters at sandboxX module
- unconfined_typebounds() should be part of sandbox domain template
- svirt_file_type is atribute no type.
- Merge pull request #166 from rhatdan/container
- Allow users to transition from unconfined_t to container types
- Add dbus_stream_connect_system_dbusd() interface.
- Merge pull request #152 from rhatdan/network_filetrans
- Fix typo in filesystem module
- Allow nss_plugin to resolve host names via the systemd-resolved. BZ(1383473)

* Mon Oct 10 2016 Lukas Vrabec <lvrabec@redhat.com> - 3.13.1-219
- Dontaudit leaked file descriptors for thumb. BZ(1383071)
- Fix typo in cobbler SELinux module
- Merge pull request #165 from rhatdan/container
- Allow cockpit_ws_t to manage cockpit_lib_t dirs and files. BZ(1375156)
- Allow cobblerd_t to delete dirs labeled as tftpdir_rw_t
- Rename svirt_lxc_net_t to container_t
- Rename docker.pp to container.pp, causes change in interface name
- Allow httpd_t domain to list inotify filesystem.
- Fix couple AVC to start roundup properly
- Allow dovecot_t send signull to dovecot_deliver_t
- Add sys_ptrace capability to pegasus domain
- Allow firewalld to stream connect to NetworkManager. BZ(1380954)
- rename docker intefaces to container
- Merge pull request #164 from rhatdan/docker-base
- Rename docker.pp to container.pp, causes change in interface name
- Allow gvfs to read /dev/nvme* devices BZ(1380951)

* Wed Oct 05 2016 Colin Walters <walters@redhat.com> - 3.13.1-218
- Revert addition of systemd service for factory reset, since it is
  basically worse than what we had before.  BZ(1290659)

* Fri Sep 30 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-216
- Allow devicekit to chat with policykit via DBUS. BZ(1377113)
- Add interface virt_rw_stream_sockets_svirt() BZ(1379314)
- Allow xdm_t to read mount pid files. BZ(1377113)
- Allow staff to rw svirt unix stream sockets. BZ(1379314)
- Allow staff_t to read tmpfs files BZ(1378446)

* Fri Sep 23 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-215
- Make tor_var_run_t as mountpoint. BZ(1368621)
- Fix typo in ftpd SELinux module.
- Allow cockpit-session to reset expired passwords BZ(1374262)
- Allow ftp daemon to manage apache_user_content
- Label /etc/sysconfig/oracleasm as oracleasm_conf_t
- Allow oracleasm to rw inherited fixed disk device
- Allow collectd to connect on unix_stream_socket
- Add abrt_dump_oops_t kill user namespace capability. BZ(1376868)
- Dontaudit systemd is mounting unlabeled dirs BZ(1367292)
- Add interface files_dontaudit_mounton_isid()

* Thu Sep 15 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-214
- Allow attach usb device to virtual machine BZ(1276873)
- Dontaudit mozilla_plugin to sys_ptrace
- Allow nut_upsdrvctl_t domain to read udev db BZ(1375636)
- Fix typo
- Allow geoclue to send msgs to syslog. BZ(1371818)
- Allow abrt to read rpm_tmp_t dirs
- Add interface rpm_read_tmp_files()
- Remove labels for somr docker sandbox files for now. This needs to be reverted after fixes in docker-selinux
- Update oracleasm SELinux module that can manage oracleasmfs_t blk files. Add dac_override cap to oracleasm_t domain.
- Add few rules to pcp SELinux module to make ti able to start pcp_pmlogger service
- Revert "label /var/lib/kubelet as svirt_sandbox_file_t"
- Remove file context for /var/lib/kubelet. This filecontext is part of docker now
- Add oracleasm_conf_t type and allow oracleasm_t to create /dev/oracleasm
- Label /usr/share/pcp/lib/pmie as pmie_exec_t and /usr/share/pcp/lib/pmlogger as pmlogger_exec_t
- Allow mdadm_t to getattr all device nodes
- Dontaudit gkeyringd_domain to connect to system_dbusd_t
- Add interface dbus_dontaudit_stream_connect_system_dbusd()
- Allow guest-set-user-passwd to set users password.
- Allow domains using kerberos to read also kerberos config dirs
- Allow add new interface to new namespace BZ(1375124)
- Allow systemd to relalbel files stored in /run/systemd/inaccessible/
-  Add interface fs_getattr_tmpfs_blk_file()
- Dontaudit domain to create any file in /proc. This is kernel bug.
- Improve regexp for power_unit_file_t files. To catch just systemd power unit files.
- Add new interface fs_getattr_oracleasmfs_fs()
- Add interface fs_manage_oracleasm()
- Label /dev/kfd as hsa_device_t
- Update seutil_manage_file_contexts() interface that caller domain can also manage file_context_t dirs

* Fri Sep 02 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-213
- Label /var/lib/docker/vfs as svirt_sandbox_file_t in virt SELinux module
- Label /usr/bin/pappet as puppetagent_exec_t
- Allow amanda to create dir in /var/lib/ with amanda_var_lib_t label
- Allow run sulogin_t in range mls_systemlow-mls_systemhigh.

* Wed Aug 31 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-212
- udisk2 module is part of devicekit module now
- Fix file context for /etc/pki/pki-tomcat/ca/
- new interface oddjob_mkhomedir_entrypoint()
- Allow mdadm to get attributes from all devices.
- Label /etc/puppetlabs as puppet_etc_t.
- quota: allow init to run quota tools
- Add new domain ipa_ods_exporter_t BZ(1366640)
- Create new interface opendnssec_stream_connect()
- Allow VirtualBox to manage udev rules.
- Allow systemd_resolved to send dbus msgs to userdomains
- Make entrypoint oddjob_mkhomedir_exec_t for unconfined_t
- Label all files in /dev/oracleasmfs/ as oracleasmfs_t

* Thu Aug 25 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-211
- Add new domain ipa_ods_exporter_t BZ(1366640)
- Create new interface opendnssec_stream_connect()
- Allow systemd-machined to communicate to lxc container using dbus
- Dontaudit accountsd domain creating dirs in /root
- Add new policy for Disk Manager called udisks2
- Dontaudit firewalld wants write to /root
- Label /etc/pki/pki-tomcat/ca/ as pki_tomcat_cert_t
- Allow certmonger to manage all systemd unit files
- Allow ipa_helper_t stream connect to dirsrv_t domain
- Update oracleasm SELinux module
- label /var/lib/kubelet as svirt_sandbox_file_t
- Allow systemd to create blk and chr files with correct label in /var/run/systemd/inaccessible BZ(1367280)
- Label /usr/libexec/gsd-backlight-helper as xserver_exec_t. This allows also confined users to manage screen brightness
- Add new userdom_dontaudit_manage_admin_dir() interface
- Label /dev/oracleasmfs as oracleasmfs_t. Add few interfaces related to oracleasmfs_t type

* Tue Aug 23 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-210
- Add few interfaces to cloudform.if file
- Label /var/run/corosync-qnetd and /var/run/corosync-qdevice as cluster_var_run_t. Note: corosync policy is now par of rhcs module
- Allow krb5kdc_t to read krb4kdc_conf_t dirs.
- Update networkmanager_filetrans_named_content() interface to allow source domain to create also temad dir in /var/run.
- Make confined users working again
- Fix hypervkvp module
- Allow ipmievd domain to create lock files in /var/lock/subsys/
- Update policy for ipmievd daemon. Contain:    Allowing reading sysfs, passwd,kernel modules   Execuring bin_t,insmod_t
- A new version of cloud-init that supports the effort to provision RHEL Atomic on Microsoft Azure requires some a new rules that allows dhclient/dhclient hooks to call cloud-init.
- Allow systemd to stop systemd-machined daemon. This allows stop virtual machines.
- Label /usr/libexec/iptables/iptables.init as iptables_exec_t Allow iptables creating lock file in /var/lock/subsys/

* Tue Aug 16 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-209
- Fix lsm SELinux module
- Dontaudit firewalld to create dirs in /root/ BZ(1340611)
- Label /run/corosync-qdevice and /run/corosync-qnetd as corosync_var_run_t
- Allow fprintd and cluster domains to cummunicate via dbus BZ(1355774)
- Allow cupsd_config_t domain to read cupsd_var_run_t sock_file. BZ(1361299)
- Add sys_admin capability to sbd domain
- Allow vdagent to comunnicate with systemd-logind via dbus
- Allow lsmd_plugin_t domain to create fixed_disk device.
- Allow opendnssec domain to create and manage own tmp dirs/files
- Allow opendnssec domain to read system state
- Allow systemd_logind stop system init_t
- Add interface init_stop()
- Add interface userdom_dontaudit_create_admin_dir()
- Label /var/run/storaged as lvm_var_run_t.
- Allow unconfineduser to run ipa_helper_t.

* Fri Aug 12 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-208
- Allow cups_config_t domain also mange sock_files. BZ(1361299)
- Add wake_alarm capability to fprintd domain BZ(1362430)
- Allow firewalld_t to relabel net_conf_t files. BZ(1365178)
- Allow nut_upsmon_t domain to chat with logind vie dbus about scheduleing a shutdown when UPS battery is low. BZ(1361802)
- Allow virtual machines to use dri devices. This allows use openCL GPU calculations. BZ(1337333)
- Allow crond and cronjob domains to creating mail_home_rw_t objects in admin_home_t BZ(1366173)
- Dontaudit mock to write to generic certs.
- Add labeling for corosync-qdevice and corosync-qnetd daemons, to run as cluster_t
- Revert "Label corosync-qnetd and corosync-qdevice as corosync_t domain"
- Merge pull request #144 from rhatdan/modemmanager
- Allow modemmanager to write to systemd inhibit pipes
- Label corosync-qnetd and corosync-qdevice as corosync_t domain
- Allow ipa_helper to read network state
- Label oddjob_reqiest as oddjob_exec_t
- Add interface oddjob_run()
- Allow modemmanager chat with systemd_logind via dbus
- Allow NetworkManager chat with puppetagent via dbus
- Allow NetworkManager chat with kdumpctl via dbus
- Allow sbd send msgs to syslog Allow sbd create dgram sockets. Allow sbd to communicate with kernel via dgram socket Allow sbd r/w kernel sysctls.
- Allow ipmievd_t domain to re-create ipmi devices Label /usr/libexec/openipmi-helper as ipmievd_exec_t
- Allow rasdaemon to use tracefs filesystem
- Fix typo bug in dirsrv policy
- Some logrotate scripts run su and then su runs unix_chkpwd. Allow logrotate_t domain to check passwd.
- Add ipc_lock capability to sssd domain. Allow sssd connect to http_cache_t
- Allow dirsrv to read dirsrv_share_t content
- Allow virtlogd_t to append svirt_image_t files.
- Allow hypervkvp domain to read hugetlbfs dir/files.
- Allow mdadm daemon to read nvme_device_t blk files
- Allow systemd_resolved to connect on system bus. BZ(1366334)
- Allow systemd to create netlink_route_socket and communicate with systemd_networkd BZ(1306344)
- Allow systemd-modules-load to load kernel modules in early boot. BZ(1322625)
- label tcp/udp port 853 as dns_port_t. BZ(1365609)
- Merge pull request #145 from rhatdan/init
- systemd is doing a gettattr on blk and chr devices in /run
- Allow selinuxusers and unconfineduser to run oddjob_request
- Allow sshd server to acces to Crypto Express 4 (CEX4) devices.
- Fix typo in device interfaces
- Add interfaces for managing ipmi devices
- Add interfaces to allow mounting/umounting tracefs filesystem
- Add interfaces to allow rw tracefs filesystem
- Merge branch 'rawhide-base' of github.com:fedora-selinux/selinux-policy into rawhide-base
- Merge pull request #138 from rhatdan/userns
- Allow iptables to creating netlink generic sockets.
- Fix filecontext for systemd shared lib.

* Thu Aug 04 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-207
- Fix filesystem inteface file, we don't have nsfs_fs_t type, just nsfs_t

* Tue Aug 02 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-206
- collectd: update policy for 5.5
- Allow puppet_t transtition to shorewall_t
- Grant certmonger "chown" capability
- Boinc updates from Russell Coker.
- Allow sshd setcap capability. This is needed due to latest changes in sshd.
- Revert "Allow sshd setcap capability. This is needed due to latest changes in sshd"
- Revert "Fix typo in ssh policy"
- Get attributes of generic ptys, from Russell Coker.

* Fri Jul 29 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-205
- Dontaudit mock_build_t can list all ptys.
- Allow ftpd_t to mamange userhome data without any boolean.
- Add logrotate permissions for creating netlink selinux sockets.
- Add new MLS attribute to allow relabeling objects higher than system low. This exception is needed for package managers when processing sensitive data.
- Label all VBox libraries stored in /var/lib/VBoxGuestAdditions/lib/ as textrel_shlib_t BZ(1356654)
- Allow systemd gpt generator to run fstools BZ(1353585)
- Label /usr/lib/systemd/libsystemd-shared-231.so as lib_t. BZ(1360716)
- Allow gnome-keyring also manage user_tmp_t sockets.
- Allow systemd to mounton /etc filesystem. BZ(1341753)

* Tue Jul 26 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-204
- Allow lsmd_plugin_t to exec ldconfig.
- Allow vnstatd domain to read /sys/class/net/ files
- Remove duplicate allow rules in spamassassin SELinux module
- Allow spamc_t and spamd_t domains create .spamassassin file in user homedirs
- Allow ipa_dnskey domain to search cache dirs
- Allow dogtag-ipa-ca-renew-agent-submit labeled as certmonger_t to create /var/log/ipa/renew.log file
- Allow ipa-dnskey read system state.
- Allow sshd setcap capability. This is needed due to latest changes in sshd Resolves: rhbz#1356245
- Add interface to write to nsfs inodes
- Allow init_t domain to read rpm db. This is needed due dnf-upgrade process failing. BZ(1349721)
- Allow systemd_modules_load_t to read /etc/modprobe.d/lockd.conf
- sysadmin should be allowed to use docker.

* Mon Jul 18 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-203
- Allow hypervkvp domain to run restorecon.
- Allow firewalld to manage net_conf_t files
- Remove double graphite-web context declaration
- Fix typo in rhsmcertd SELinux policy
- Allow logrotate read logs inside containers.
- Allow sssd to getattr on fs_t
- Allow opendnssec domain to manage bind chace files
- Allow systemd to get status of systemd-logind daemon
- Label more ndctl devices not just ndctl0

* Wed Jul 13 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-202
- Allow systemd_logind_t to start init_t BZ(1355861)
- Add init_start() interface
- Allow sysadm user to run systemd-tmpfiles
- Add interface systemd_tmpfiles_run

* Mon Jul 11 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-201
- Allow lttng tools to block suspending
- Allow creation of vpnaas in openstack
- remove rules with compromised_kernel permission
- Allow dnssec-trigger to chat with NetworkManager over DBUS BZ(1350100)
- Allow virtual machines to rw infiniband devices. Resolves: rhbz#1210263
- Update makefile to support snapperd_contexts file
- Remove compromize_kernel permission Remove unused mac_admin permission Add undefined system permission
- Remove duplicate declaration of class service
- Fix typo in access_vectors file
- Merge branch 'rawhide-base-modules-load' into rawhide-base
- Add new policy for systemd-modules-load
- Add systemd access vectors.
- Revert "Revert "Revert "Missed this version of exec_all"""
- Revert "Revert "Missed this version of exec_all""
- Revert "Missed this version of exec_all"
- Revert "Revert "Fix name of capability2 secure_firmware->compromise_kernel"" BZ(1351624) This reverts commit 3e0e7e70de481589440f3f79cccff08d6e62f644.
- Revert "Fix name of capability2 secure_firmware->compromise_kernel" BZ(1351624) This reverts commit 7a0348a2d167a72c8ab8974a1b0fc33407f72c48.
- Revert "Allow xserver to compromise_kernel access"BZ(1351624)
- Revert "Allow anyone who can load a kernel module to compromise_kernel"BZ(1351624)
- Revert "add ptrace_child access to process" (BZ1351624)
- Add user namespace capability object classes.
- Allow udev to manage systemd-hwdb files
- Add interface systemd_hwdb_manage_config()
- Fix paths to infiniband devices. This allows use more then two infiniband interfaces.
- corecmd: Remove fcontext for /etc/sysconfig/libvirtd
- iptables: add fcontext for nftables

* Tue Jul 05 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-200
- Fix typo in brltty policy
- Add new SELinux module sbd
- Allow pcp dmcache metrics collection
- Allow pkcs_slotd_t to create dir in /var/lock Add label pkcs_slotd_log_t
- Allow openvpn to create sock files labeled as openvpn_var_run_t
- Allow hypervkvp daemon to getattr on  all filesystem types.
- Allow firewalld to create net_conf_t files
- Allow mock to use lvm
- Allow mirromanager creating log files in /tmp
- Allow vmtools_t to transition to rpm_script domain
- Allow nsd daemon to manage nsd_conf_t dirs and files
- Allow cluster to create dirs in /var/run labeled as cluster_var_run_t
- Allow sssd read also sssd_conf_t dirs
- Allow opensm daemon to rw infiniband_mgmt_device_t
- Allow krb5kdc_t to communicate with sssd
- Allow prosody to bind on prosody ports
- Add dac_override caps for fail2ban-client Resolves: rhbz#1316678
- dontaudit read access for svirt_t on the file /var/db/nscd/group Resolves: rhbz#1301637
- Allow inetd child process to communicate via dbus with systemd-logind Resolves: rhbz#1333726
- Add label for brltty log file Resolves: rhbz#1328818
- Allow snort_t to communicate with sssd Resolves: rhbz#1284908
- Add interface lttng_sessiond_tmpfs_t()
- Dontaudit su_role_template interface to getattr /proc/kcore Dontaudit su_role_template interface to getattr /dev/initctl
- Add interface lvm_getattr_exec_files()
- Make label for new infiniband_mgmt deivices
- Add prosody ports Resolves: rhbz#1304664

* Tue Jun 28 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-199
- Label /var/lib/softhsm as named_cache_t. Allow named_t to manage named_cache_t dirs.
- Allow glusterd daemon to get systemd status
- Merge branch 'rawhide-contrib' of github.com:fedora-selinux/selinux-policy into rawhide-contrib
- Merge pull request #135 from rhatdan/rawip_socket
- Allow logrotate dbus-chat with system_logind daemon
- Allow pcp_pmlogger to read kernel network state Allow pcp_pmcd to read cron pid files
- Add interface cron_read_pid_files()
- Allow pcp_pmlogger to create unix dgram sockets
- Add interface dirsrv_run()
- Remove non-existing jabberd_spool_t() interface and add new jabbertd_var_spool_t.
- Remove non-existing interface salk_resetd_systemctl() and replace it with sanlock_systemctl_sanlk_resetd()
- Create label for openhpid log files.
- Container processes need to be able to listen on rawip sockets
- Label /var/lib/ganglia as httpd_var_lib_t
- Allow firewalld_t to create entries in net_conf_t dirs.
- Allow journalctl to read syslogd_var_run_t files. This allows to staff_t and sysadm_t to read journals
- Label /etc/dhcp/scripts dir as bin_t
- Allow sysadm_role to run journalctl_t domain. This allows sysadm user to read journals.

* Wed Jun 22 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-198
- Allow firewalld_t to create entries in net_conf_t dirs.
- Allow journalctl to read syslogd_var_run_t files. This allows to staff_t and sysadm_t to read journals
- Allow rhsmcertd connect to port tcp 9090
- Label for /bin/mail(x) was removed but /usr/bin/mail(x) not. This path is also needed to remove.
- Label /usr/libexec/mimedefang-wrapper as spamd_exec_t.
- Add new boolean spamd_update_can_network.
- Add proper label for /var/log/proftpd.log
- Allow rhsmcertd connect to tcp netport_port_t
- Fix SELinux context for /usr/share/mirrormanager/server/mirrormanager to Label all binaries under dir as mirrormanager_exec_t.
- Allow prosody to bind to fac_restore tcp port.
- Fix SELinux context for usr/share/mirrormanager/server/mirrormanager
- Allow ninfod to read raw packets
- Fix broken hostapd policy
- Allow hostapd to create netlink_generic sockets. BZ(1343683)
- Merge pull request #133 from vinzent/allow_puppet_transition_to_shorewall
- Allow pegasus get attributes from qemu binary files.
- Allow tuned to use policykit. This change is required by cockpit.
- Allow conman_t to read dir with conman_unconfined_script_t binary files.
- Allow pegasus to read /proc/sysinfo.
- Allow puppet_t transtition to shorewall_t
- Allow conman to kill conman_unconfined_script.
- Allow sysadm_role to run journalctl_t domain. This allows sysadm user to read journals.
- Merge remote-tracking branch 'refs/remotes/origin/rawhide-base' into rawhide-base
- Allow systemd to execute all init daemon executables.
- Add init_exec_notrans_direct_init_entry() interface.
- Label tcp ports:16379, 26379 as redis_port_t
- Allow systemd to relabel /var and /var/lib directories during boot.
- Add files_relabel_var_dirs() and files_relabel_var_dirs() interfaces.
- Add files_relabelto_var_lib_dirs() interface.
- Label tcp and udp port 5582 as fac_restore_port_t
- Allow sysadm_t user to run postgresql-setup.
- Allow sysadm_t user to dbus chat with oddjob_t. This allows confined admin run oddjob mkhomedirfor script.
- Allow systemd-resolved to connect to llmnr tcp port. BZ(1344849)
- Allow passwd_t also manage user_tmp_t dirs, this change is needed by gnome-keyringd

* Thu Jun 16 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-197
- Allow conman to kill conman_unconfined_script.
- Make conman_unconfined_script_t as init_system_domain.
- Allow init dbus chat with apmd.
- Patch /var/lib/rpm is symlink to /usr/share/rpm on Atomic, due to this change we need to label also /usr/share/rpm as rpm_var_lib_t.
- Dontaudit xguest_gkeyringd_t stream connect to system_dbusd_t
- Allow collectd_t to stream connect to postgresql.
- Allow mysqld_safe to inherit rlimit information from mysqld
- Allow ip netns to mounton root fs and unmount proc_t fs.
- Allow sysadm_t to run newaliases command.

* Mon Jun 13 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-196
- Allow svirt_sandbox_domains to r/w onload sockets
- Add filetrans rule that NetworkManager_t can create net_conf_t files in /etc.
- Add interface sysnet_filetrans_named_net_conf()
- Rawhide fails to boot, systemd-logind needs to config transient config files
- User Namespace is requires create on process domains

* Wed Jun 08 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-195
- Add hwloc-dump-hwdata SELinux policy
- Add labels for mediawiki123
- Fix label for all fence_scsi_check scripts
- Allow setcap for fenced
- Allow glusterd domain read krb5_keytab_t files.
- Allow tmpreaper_t to read/setattr all non_security_file_type dirs
- Update refpolicy to handle hwloc
- Fix typo in files_setattr_non_security_dirs.
- Add interface files_setattr_non_security_dirs()

* Tue Jun 07 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-194
- Allow boinc to use dri devices. This allows use Boinc for a openCL GPU calculations. BZ(1340886)
- Add nrpe_dontaudit_write_pipes()
- Merge pull request #129 from rhatdan/onload
- Add support for onloadfs
- Merge pull request #127 from rhatdan/device-node
- Additional access required for unconfined domains
- Dontaudit ping attempts to write to nrpe unnamed pipes
- Allow ifconfig_t to mounton also ifconfig_var_run_t dirs, not just files. Needed for: #ip netns add foo BZ(1340952)

* Mon May 30 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-193
- Directory Server (389-ds-base) has been updated to use systemd-ask-password. In order to function correctly we need the following added to dirsrv.te
- Update opendnssec_manage_config() interface to allow caller domain also manage opendnssec_conf_t dirs
- Allow gssproxy to get attributes on all filesystem object types. BZ(1333778)
- Allow ipa_dnskey_t search httpd config files.
- Dontaudit certmonger to write to etc_runtime_t
- Update opendnssec_read_conf() interface to allow caller domain also read opendnssec_conf_t dirs.
- Add interface ipa_delete_tmp()
- Allow systemd_hostanmed_t to read /proc/sysinfo labeled as sysctl_t.
- Allow systemd to remove ipa temp files during uinstalling ipa. BZ(1333106)

* Wed May 25 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-192
- Create new SELinux type for /usr/libexec/ipa/ipa-dnskeysyncd BZ(1333106)
- Add SELinux policy for opendnssec service. BZ(1333106)

* Tue May 24 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-191
- Label /usr/share/ovirt-guest-agent/ovirt-guest-agent.py as rhev_agentd_exec_t
- Allow dnssec_trigger_t to create lnk_file labeled as dnssec_trigger_var_run_t. BZ(1335954)
- Allow ganesha-ha.sh script running under unconfined_t domain communicate with glusterd_t domains via dbus.
- Allow ganesha daemon labeled as glusterd_t create /var/lib/nfs/ganesha dir labeled as var_lib_nfs_t.
- Merge pull request #122 from NetworkManager/th/nm-dnsmasq-dbus
- Merge pull request #125 from rhatdan/typebounds
- Typebounds user domains
- Allow systemd_resolved_t to check if ipv6 is disabled.
- systemd added a new directory for unit files /run/systemd/transient. It should be labelled system_u:object_r:systemd_unit_file_t:s0, the same as /run/systemd/system, PID 1 will write units there. Resolves: #120
- Label /dev/xen/privcmd as xen_device_t. BZ(1334115)

* Mon May 16 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-190
- Label /var/log/ganesha.log as gluster_log_t Allow glusterd_t domain to create glusterd_log_t files. Label /var/run/ganesha.pid as gluster_var_run_t.
- Allow zabbix to connect to postgresql port
- Label /usr/libexec/openssh/sshd-keygen as sshd_keygen_exec_t. BZ(1335149)
- Allow systemd to read efivarfs. Resolve: #121

* Tue May 10 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-189
- Revert temporary fix: Replace generating man/html pages with pages from actual build. This is due to broken userspace with python3 in F23/Rawhide. Please Revert when userspace will be fixed

* Mon May 09 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-188
- Label tcp port 8181 as intermapper_port_t.
- Label /usr/libexec/storaged/storaged as lvm_exec_t to run storaged daemon in lvm_t SELinux domain. BZ(1333588)
- Label tcp/udp port 2024 as xinuexpansion4_port_t
- Label tcp port 7002 as afs_pt_port_t Label tcp/udp port 2023 as xinuexpansion3_port_t

* Thu May 05 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-187
- Allow stunnel create log files. BZ(1333033)
- Label dev/shm/squid-cf__metadata.shm as squid_tmpfs_t. BZ(1331574)
- Allow stunnel sys_nice capability. Stunnel sched_* syscalls in some cases. BZ(1332287)
- Label /usr/bin/ganesha.nfsd as glusterd_exec_t to run ganesha as glusterd_t. Allow glusterd_t stream connect to rpbind_t. Allow cluster_t to create symlink /var/lib/nfs labeled as var_lib_nfs_t. Add interface rpc_filetrans_var_lib_nfs_content() Add new boolean: rpcd_use_fusefs to allow rpcd daemon use fusefs.
- Allow systemd-user-sessions daemon to mamange systemd_logind_var_run_t pid files. BZ(1331980)
- Modify kernel_steam_connect() interface by adding getattr permission. BZ(1331927)
- Label /usr/sbin/xrdp* files as bin_t BZ(1258453)
- Allow rpm-ostree domain transition to install_t domain from init_t. rhbz#1330318

* Fri Apr 29 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-186
- Allow snapperd sys_admin capability Allow snapperd to set scheduler. BZ(1323732)
- Label named-pkcs11 binary as named_exec_t. BZ(1331316)
- Revert "Add new permissions stop/start to class system. rhbz#1324453"
- Fix typo in module compilation message

* Wed Apr 27 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-185
- Allow runnig php7 in fpm mode. From selinux-policy side, we need to allow httpd to read/write hugetlbfs.
- Allow openvswitch daemons to run under openvswitch Linux user instead of root. This change needs allow set capabilities: chwon, setgid, setuid, setpcap. BZ(1330895)
- Allow KDM to get status about power services. This change allow kdm to be able do shutdown BZ(1330970)
- Add mls support for some db classes

* Tue Apr 26 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-184
- Remove ftpd_home_dir() boolean from distro policy. Reason is that we cannot make this working due to m4 macro language limits.
- Create new apache content template for files stored in user homedir. This change is needed to make working booleans: - httpd_enable_homedirs - httpd_read_user_content Resolves: rhbz#1330448
- Label /usr/lib/snapper/systemd-helper as snapperd_exec_t. rhbz#1323732
- Make virt_use_pcscd boolean off by default.
- Create boolean to allow virtual machine use smartcards. rhbz#1029297
- Allow snapperd to relabel btrfs snapshot subvolume to snapperd_data_t. rhbz#1323754
- Allow mongod log to syslog.
- Allow nsd daemon to create log file in /var/log as nsd_log_t
- unlabeled_t can not be an entrypoint.
- Modify interface den_read_nvme() to allow also read nvme_device_t block files. rhbz#1327909
- Add new permissions stop/start to class system. rhbz#1324453

* Mon Apr 18 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-183
- Allow modemmanager to talk to logind
- Dontaudit tor daemon needs net_admin capability. rhbz#1311788
- Allow GDM write to event devices. This rule is needed for GDM, because other display managers runs the X server as root, GDM instead runs the X server as the unprivileged user, within the user session. rhbz#1232042
- Xorg now writes content in users homedir.

* Fri Apr 08 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-182
- rename several contrib modules according to their filenames
- Add interface gnome_filetrans_cert_home_content()
- By default container domains should not be allowed to create devices
- Allow unconfined_t to create ~/.local/share/networkmanagement/certificates/ as home_cert_t instead of data_home_t.
- Allow systemd_resolved_t to read /etc/passwd file. Allow systemd_resolved_t to write to kmsg_device_t when 'systemd.log_target=kmsg' option is used
- Allow systemd gpt generator to read removable devices. BZ(1323458)
- Allow systemd_gpt_generator_t sys_rawio capability. This access is needed to allow systemd gpt generator various device commands  BZ(1323454)

* Fri Apr 01 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-181
- Label /usr/libexec/rpm-ostreed as rpm_exec_t. BZ(1309075)
- /bin/mailx is labeled sendmail_exec_t, and enters the sendmail_t domain on execution.  If /usr/sbin/sendmail does not have its own domain to transition to, and is not one of several products whose behavior is allowed by the sendmail_t policy, execution will fail. In this case we need to label /bin/mailx as bin_t. BZ(1323224)
- Label all run tgtd files, not just socket files.
- Allow prosody to stream connect to sasl. This will allow using cyrus authentication in prosody.
- Allow prosody to listen on port 5000 for mod_proxy65. BZ(1322815)
- Allow targetd to read/write to /dev/mapper/control device. BZ(1241415)
- Label /etc/selinux/(minimum|mls|targeted)/active/ as semanage_store_t.
- Allow systemd_resolved to read systemd_networkd run files. BZ(1322921)
- New cgroup2 file system in Rawhide

* Wed Mar 30 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-180
- Allow dovecot_auth_t domain to manage also dovecot_var_run_t fifo files. BZ(1320415)
- Allow colord to read /etc/udev/hwdb.bin. rhzb#1316514
- sandboxX.te: Allow sandbox domain to have entrypoint access only for executables and mountpoints.
- Allow sandbox domain to have entrypoint access only for executables and mountpoints.
- Allow bitlee to create bitlee_var_t dirs.
- Allow CIM provider to read sssd public files.
- Fix some broken interfaces in distro policy.
- Allow power button to shutdown the laptop.
- Allow lsm plugins to create named fixed disks. rhbz#1238066
- Allow hyperv domains to rw hyperv devices. rhbz#1241636
- Label /var/www/html(/.*)?/wp_backups(/.*)? as httpd_sys_rw_content_t.
- Create conman_unconfined_script_t type for conman script stored in /use/share/conman/exec/
- Allow rsync_export_all_ro boolean to read also non_auth_dirs/files/symlinks.
- Allow pmdaapache labeled as pcp_pmcd_t access to port 80 for apache diagnostics
- Label nagios scripts as httpd_sys_script_exec_t.
- Allow nsd_t to bind on nsf_control tcp port. Allow nsd_crond_t to read nsd pid.
- Fix couple of cosmetic thing in new virtlogd_t policy. rhbz #1311576
- Merge pull request #104 from berrange/rawhide-contrib-virtlogd
- Label /var/run/ecblp0 as cupsd_var_run_t due to this fifo_file is used by epson drivers. rhbz#1310336
- Dontaudit logrotate to setrlimit itself. rhbz#1309604
- Add filename transition that /etc/princap will be created with cupsd_rw_etc_t label in cups_filetrans_named_content() interface.
- Allow pcp_pmie and pcp_pmlogger to read all domains state.
- Allow systemd-gpt-generator to create and manage systemd gpt generator unit files. BZ(1319446)
- Merge pull request #115 from rhatdan/nvidea
- Label all nvidia binaries as xserver_exec_t
- Add new systemd_hwdb_read_config() interface. rhbz#1316514
- Add back corecmd_read_all_executables() interface.
- Call files_type() instead of file_type() for unlabeled_t.
- Add files_entrypoint_all_mountpoint() interface.
- Make unlabeled only as a file_type type. It is a type for fallback if there is an issue with labeling.
- Add corecmd_entrypoint_all_executables() interface.
- Create hyperv* devices and create rw interfaces for this devices. rhbz#1309361
- Add neverallow assertion for unlabaled_t to increase policy security.
- Allow systemd-rfkill to create /var/lib/systemd/rfkill dir. rhbz#1319499
- Label 8952 tcp port as nsd_control.
- Allow to log out to gdm after screen was resized in session via vdagent. Resolves: rhbz#1249020

* Wed Mar 16 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-179
- Add filename transition that /etc/princap will be created with cupsd_rw_etc_t label in cups_filetrans_named_content() interface.
- Revert "Add filename transition that /etc/princap will be created with cupsd_rw_etc_t label in cups_filetrans_named_content."
- Add filename transition that /etc/princap will be created with cupsd_rw_etc_t label in cups_filetrans_named_content.
- Allow pcp_pmie and pcp_pmlogger to read all domains state.
- Make fwupd domain unconfined. We need to discuss solution related to using gpg. rhbz#1316717
- Merge pull request #108 from rhatdan/rkt
- Merge pull request #109 from rhatdan/virt_sandbox
- Add new interface to define virt_sandbox_network domains
- Label /etc/redis-sentinel.conf as redis_conf_t. Allow redis_t write to redis_conf_t. Allow redis_t to connect on redis tcp port.
- Fix typo in drbd policy
- Remove declaration of empty booleans in virt policy.
- Add new drbd file type: drbd_var_run_t. Allow drbd_t to manage drbd_var_run_t files/dirs.
- Label /etc/ctdb/events.d/* as ctdb_exec_t. Allow ctdbd_t to setattr on ctdbd_exec_t files.
- Additional rules to make rkt work in enforcing mode
- Allow to log out to gdm after screen was resized in session via vdagent. Resolves: rhbz#1249020
- Allow ipsec to use pam. rhbz#1317988
- Allow systemd-gpt-generator to read fixed_disk_device_t. rhbz#1314968
- Allow setrans daemon to read /proc/meminfo.
- Merge pull request #107 from rhatdan/rkt-base
- Allow systemd_notify_t to write to kmsg_device_t when 'systemd.log_target=kmsg' option is used.
- Remove bin_t label for /etc/ctdb/events.d/. We need to label this scripts as ctdb_exec_t.

* Thu Mar 10 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-178
- Label tcp port 5355 as llmnr-> Link-Local Multicast Name Resolution
- Add support systemd-resolved.

* Tue Mar 08 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-177
- Allow spice-vdagent to getattr on tmpfs_t filesystems Resolves: rhbz#1276251
- Allow sending dbus msgs between firewalld and system_cronjob domains.
- Allow zabbix-agentd to connect to following tcp sockets. One of zabbix-agentd functions is get service status of ftp,http,innd,pop,smtp protocols. rhbz#1315354
- Allow snapperd mounton permissions for snapperd_data_t. BZ(#1314972)
- Add support for systemd-gpt-auto-generator. rhbz#1314968
- Add interface dev_read_nvme() to allow reading Non-Volatile Memory Host Controller devices.
- Add support for systemd-hwdb daemon. rhbz#1306243

* Thu Mar 03 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-176
- Add new boolean tmpreaper_use_cifs() to allow tmpreaper to run on local directories being shared with Samba.
- Merge pull request #105 from rhatdan/NO_NEW_PRIV
- Fix new rkt policy
- Remove some redundant rules.
- Fix cosmetic issues in interface file.
- Merge pull request #100 from rhatdan/rawhide-contrib
- Add interface fs_setattr_cifs_dirs().
- Merge pull request #106 from rhatdan/NO_NEW_PRIV_BASE
- Fixed to make SELinux work with docker and prctl(NO_NEW_PRIVS)
-Build file_contexts.bin file_context.local.bin file_context.homedir.bin during build phase.
 This fix issue in Fedora live images when selinux-policy-targeted is not installed but just unpackaged, since there's no .bin files,
 file_contexts is parsed in selabel_open().
Resolves: rhbz#1314372

* Fri Feb 26 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-175
- Fix new rkt policy (Remove some redundant rules, Fix cosmetic issues in interface file)
- Add policy for rkt services

* Fri Feb 26 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-174
- Revert "Allow systemd-logind to create .#nologinXXXXXX labeled as systemd_logind_var_run_t in /var/run/systemd/ rhbz#1285019"
- Allow systemd-logind to create .#nologinXXXXXX labeled as systemd_logind_var_run_t in /var/run/ rhbz#1285019

* Fri Feb 26 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-173
- Allow amanda to manipulate the tape changer to load the necessary tapes. rhbz#1311759
- Allow keepalived to create netlink generic sockets. rhbz#1311756
- Allow modemmanager to read /etc/passwd file.
- Label all files named /var/run/.*nologin.* as systemd_logind_var_run_t.
- Add filename transition to interface systemd_filetrans_named_content() that domain will create rfkill dir labeled as systemd_rfkill_var_lib_t instead of init_var_lib_t. rhbz #1290255
- Allow systemd-logind to create .#nologinXXXXXX labeled as systemd_logind_var_run_t in /var/run/systemd/ rhbz#1285019
- Allow systemd_networkd_t to write kmsg, when kernel was started with following params: systemd.debug systemd.log_level=debug systemd.log_target=kmsg rhbz#1311444
- Allow ipsec to read home certs, when connecting to VPN. rhbz#1301319

* Thu Feb 25 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-172
- Fix macro name from snmp_manage_snmp_var_lib_files to snmp_manage_var_lib_files in cupsd policy.
- Allow hplip driver to write to its MIB index files stored in the /var/lib/net-snmp/mib_indexes. Resolves: rhbz#1291033
- Allow collectd setgid capability Resolves:#1310896
- Allow adcli running as sssd_t to write krb5.keytab file.
- Allow abrt-hook-ccpp to getattr on all executables. BZ(1284304)
- Allow kexec to read kernel module files in /usr/lib/modules.
- Add httpd_log_t for /var/log/graphite-web rhbz#1306981
- Remove redudant rules and fix _admin interface.
- Add SELinux policy for LTTng 2.x central tracing registry session daemon.
- Allow create mongodb unix dgram sockets. rhbz#1306819
- Support for InnoDB Tablespace Encryption.
- Dontaudit leaded file descriptors from firewalld
- Add port for rkt services
- Add support for the default lttng-sessiond port - tcp/5345.  This port is used by LTTng 2.x central tracing registry session daemon.

* Thu Feb 11 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-171
- Allow setroubleshoot_fixit_t to use temporary files

* Wed Feb 10 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-170
- Allow abrt_dump_oops_t to getattr filesystem nsfs files. rhbz#1300334
- Allow ulogd_t to create netlink_netfilter sockets. rhbz#1305426
- Create new type fwupd_cert_t Label /etc/pki/(fwupd|fwupd-metadata) dirs as fwupd_cert_t Allow fwupd_t domain to read fwupd_cert_t files|lnk_files rhbz#1303533
- Add interface to dontaudit leaked files from firewalld
- fwupd needs to dbus chat with policykit
- Allow fwupd domain transition to gpg domain. Fwupd signing firmware updates by gpg. rhbz#1303531
- Allow abrt_dump_oops_t to check permissions for a /usr/bin/Xorg. rhbz#1284967
- Allow prelink_cron_system_t domain set resource limits. BZ(1190364)
- Allow pppd_t domain to create sockfiles in /var/run labeled as pppd_var_run_t label. BZ(1302666)
- Fix wrong name for openqa_websockets tcp port.
- Allow run sshd-keygen on second boot if first boot fails after some reason and content is not syncedon the disk. These changes are reflecting this commit in sshd. http://pkgs.fedoraproject.org/cgit/rpms/openssh.git/commit/?id=af94f46861844cbd6ba4162115039bebcc8f78ba rhbz#1299106
- Add interface ssh_getattr_server_keys() interface. rhbz#1299106
- Added Label openqa for tcp port (9526) Added Label openqa-websockets for tcp port (9527) rhbz#1277312
- Add interface fs_getattr_nsfs_files()
- Add interface xserver_exec().
- Revert "Allow all domains some process flags."BZ(1190364)

* Wed Feb 03 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-169
- Allow openvswitch domain capability sys_rawio.
- Revert "Allow NetworkManager create dhcpc pid files. BZ(1229755)"
- Allow openvswitch to manage hugetlfs files and dirs.
- Allow NetworkManager create dhcpc pid files. BZ(1229755)
- Allow apcupsd to read kernel network state. BZ(1282003)
- Label /sys/kernel/debug/tracing filesystem
- Add fs_manage_hugetlbfs_files() interface.
- Add sysnet_filetrans_dhcpc_pid() interface.

* Wed Jan 20 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-168
- Label virtlogd binary as virtd_exec_t. BZ(1291940)
- Allow iptables to read nsfs files. BZ(1296826)

* Mon Jan 18 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-167
- Add fwupd policy for daemon to allow session software to update device firmware
- Label /usr/libexec/ipa/oddjob/org.freeipa.server.conncheck as ipa_helper_exec_t. BZ(1289930)
- Allow systemd services to use PrivateNetwork feature
- Add a type and genfscon for nsfs.
- Fix SELinux context for rsyslog unit file. BZ(1284173)

* Wed Jan 13 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-166
- Allow logrotate to systemctl rsyslog service. BZ(1284173)
- Allow condor_master_t domain capability chown. BZ(1297048)
- Allow chronyd to be dbus bus client. BZ(1297129)
- Allow openvswitch read/write hugetlb filesystem.
- Revert "Allow openvswitch read/write hugetlb filesystem."
- Allow smbcontrol domain to send sigchld to ctdbd domain.
- Allow openvswitch read/write hugetlb filesystem.
- Merge branch 'rawhide-contrib' of github.com:fedora-selinux/selinux-policy into rawhide-contrib
- Label /var/log/ipareplica-conncheck.log file as ipa_log_t Allow ipa_helper_t domain to manage logs labeledas ipa_log_t Allow ipa_helper_t to connect on http and kerberos_passwd ports. BZ(1289930)
- Allow keepalived to connect to 3306/tcp port - mysqld_port_t.
- Merge remote-tracking branch 'refs/remotes/origin/rawhide-contrib' into rawhide-contrib
- Merge remote-tracking branch 'refs/remotes/origin/rawhide-contrib' into rawhide-contrib
- Merge pull request #86 from rhatdan/rawhide-contrib
- Label some new nsd binaries as nsd_exec_t Allow nsd domain net_admin cap. Create label nsd_tmp_t for nsd tmp files/dirs BZ (1293146)
- Added interface logging_systemctl_syslogd
- Label rsyslog unit file
- Added policy for systemd-coredump service. Added domain transition from kernel_t to systemd_coredump_t. Allow syslogd_t domain to read/write tmpfs systemd-coredump files. Make new domain uconfined for now.

* Wed Jan 06 2016 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-165
- Allow sddm-helper running as xdm_t to create .wayland-errors with correct labeling. BZ(#1291085)
- Revert "Allow arping running as netutils_t sys_module capability for removing tap devices."
- Allow arping running as netutils_t sys_module capability for removing tap devices.
- Add userdom_connectto_stream() interface.
- Allow systemd-logind to read /run/utmp. BZ(#1278662)
- Allow sddm-helper running as xdm_t to create .wayland-errors with correct labeling. BZ(#1291085)
- Revert "Allow arping running as netutils_t sys_module capability for removing tap devices."
- Allow arping running as netutils_t sys_module capability for removing tap devices.
- Add userdom_connectto_stream() interface.
- Allow systemd-logind to read /run/utmp. BZ(#1278662)

* Tue Dec 15 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-164
- Allow firewalld to create firewalld_var_run_t directory. BZ(1291243)
- Add interface firewalld_read_pid_files()
- Allow iptables to read firewalld pid files. BZ(1291243)
- Allow the user cronjobs to run in their userdomain
- Label ssdm binaries storedin /etc/sddm/ as bin_t. BZ(1288111)
- Merge pull request #81 from rhatdan/rawhide-base
- New access needed by systemd domains

* Wed Dec 09 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-163
- Allow whack executed by sysadm SELinux user to access /var/run/pluto/pluto.ctl. It fixes "ipsec auto --status" executed by sysadm_t.
- Add ipsec_read_pid() interface

* Mon Dec 07 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-162
- Label /usr/sbin/lvmlockd binary file as lvm_exec_t. BZ(1287739)
- Adding support for dbus communication between systemd-networkd and systemd-hostnamed. BZ(1279182)
- Update init policy to have userdom_noatsecure_login_userdomain() and userdom_sigchld_login_userdomain() called for init_t.
- init_t domain should be running without unconfined_domain attribute.
- Add a new SELinux policy for /usr/lib/systemd/systemd-rfkill.
- Update userdom_transition_login_userdomain() to have "sigchld" and "noatsecure" permissions.
- systemd needs to access /dev/rfkill on early boot.
- Allow dspam to read /etc/passwd

* Mon Nov 30 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-161
- Set default value as true in boolean mozilla_plugin_can_network_connect. BZ(1286177)

* Tue Nov 24 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-160
- Allow apcupsd sending mails about battery state. BZ(1274018)
- Allow pcp_pmcd_t domain transition to lvm_t. BZ(1277779)
- Merge pull request #68 from rhatdan/rawhide-contrib
- Allow antivirus_t to bind to all unreserved ports. Clamd binds to random unassigned port (by default in range 1024-2048). #1248785
-  Allow systemd-networkd to bind dhcpd ports if DHCP=yes in *.network conf file. BZ(#1280092)
- systemd-tmpfiles performs operations on System V IPC objects which requires sys_admin capability. BZ(#1279269)

* Fri Nov 20 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-159
- Allow antivirus_t to bind to all unreserved ports. Clamd binds to random unassigned port (by default in range 1024-2048)
- Allow abrt-hook-ccpp to change SELinux user identity for created objects.
- Allow abrt-hook-ccpp to get attributes of all processes because of core_pattern.
- Allow setuid/setgid capabilities for abrt-hook-ccpp.
- Add default labeling for /etc/Pegasus/cimserver_current.conf. It is a correct patch instead of the current /etc/Pegasus/pegasus_current.conf.
- Allow fenced node dbus msg when using foghorn witch configured foghorn, snmpd, and snmptrapd.
- cockpit has grown content in /var/run directory
- Add support for /dev/mptctl device used to check RAID status.
- Allow systemd-hostnamed to communicate with dhcp via dbus.
- systemd-logind remove all IPC objects owned by a user on a logout. This covers also SysV memory. This change allows to destroy unpriviledged user SysV shared memory segments.
- Add userdom_destroy_unpriv_user_shared_mem() interface.
- Label /var/run/systemd/shutdown directory as systemd_logind_var_run_t to allow systemd-logind to access it if shutdown is invoked.
- Access needed by systemd-machine to manage docker containers
- Allow systemd-logind to read /run/utmp when shutdown is invoked.

* Tue Nov 10 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-158
- Merge pull request #48 from lkundrak/contrib-openfortivpn
- unbound wants to use ephemeral ports as a default configuration. Allow to use also udp sockets.

* Mon Nov 09 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-157
- The ABRT coredump handler has code to emulate default core file creation The handler runs in a separate process with abrt_dump_oops_t SELinux process type. abrt-hook-ccpp also saves the core dump file in the very same way as kernel does and a user can specify CWD location for a coredump. abrt-hook-ccpp has been made as a SELinux aware apps to create this coredumps with correct labeling and with this commit the policy rules have been updated to allow access all non security files on a system.
- Since /dev/log is a symlink, we need to allow relabelto also symlink. This commit update logging_relabel_devlog_dev() interface to allow it.
- systemd-user has pam_selinux support and needs to able to compute user security context if init_t is not unconfined domain.

* Tue Oct 27 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-156
- Allow fail2ban-client to execute ldconfig. #1268715
- Add interface virt_sandbox_domain()
- Use mmap_file_perms instead of exec_file_perms in setroubleshoot policy to shave off the execute_no_trans permission. Based on a github communication with Dominick Grift.
-all userdom_dontaudit_user_getattr_tmp_sockets instead() of usedom_dontaudit_user_getattr_tmp_sockets().
- Rename usedom_dontaudit_user_getattr_tmp_sockets() to userdom_dontaudit_user_getattr_tmp_sockets().
- Remove auth_login_pgm_domain(init_t) which has been added by accident.
- init_t needs to able to change SELinux identity because it is used as login_pgm domain because of systemd-user and PAM. It allows security_compute_user() returns a list of possible context and then a correct default label is returned by "selinux.get_default_context(sel_user,fromcon)" defined in the policy user config files.
- Add interface auth_use_nsswitch() to systemd_domain_template.
- Revert "auth_use_nsswitch can be used with attribute systemd_domain."
- auth_use_nsswitch can be used with attribute systemd_domain.
- ipsec: fix stringSwan charon-nm
- docker is communicating with systemd-machined
- Add missing systemd_dbus_chat_machined, needed by docker

* Tue Oct 20 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-155
- Build including docker selinux interfaces.

* Tue Oct 20 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-154
- Allow winbindd to send signull to kernel. BZ(#1269193)
- Merge branch 'rawhide-contrib-chrony' into rawhide-contrib
- Fixes for chrony version 2.2 BZ(#1259636)
  * Allow chrony chown capability
  * Allow sendto dgram_sockets to itself and to unconfined_t domains.
- Merge branch 'rawhide-contrib-chrony' into rawhide-contrib
- Add boolean allowing mysqld to connect to http port. #1262125
- Merge pull request #52 from 1dot75cm/rawhide-base
- Allow systemd_hostnamed to read xenfs_t files. BZ(#1233877)
- Fix attribute in corenetwork.if.in

* Tue Oct 13 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-153
- Allow abrt_t to read sysctl_net_t files. BZ(#1194280)
- Merge branch 'rawhide-contrib' of github.com:fedora-selinux/selinux-policy into rawhide-contrib
- Add abrt_stub interface.
- Add support for new mock location - /usr/libexec/mock/mock. BZ(#1270972)
- Allow usbmuxd to access /run/udev/data/+usb:*. BZ(#1269633)
- Allow qemu-bridge-helper to read /dev/random and /dev/urandom. BZ(#1267217)
- Allow sssd_t to manage samba var files/dirs to SSSD's GPO support which is enabled against an Active Directory domain. BZ(#1225200).
- Add samba_manage_var_dirs() interface.
- Allow pcp_pmlogger to exec bin_t BZ(#1258698)
- Allow spamd to read system network state. BZ(1260234)
- Allow fcoemon to create netlink scsitransport sockets BZ(#1260882)
- Allow networkmanager to create networkmanager_var_lib_t files. BZ(1270201)
- Allow systemd-networkd to read XEN state for Xen hypervisor. BZ(#1269916)
- Add fs_read_xenfs_files() interface.
- Allow systemd_machined_t to send dbus msgs to all users and read/write /dev/ptmx to make 'machinectl shell' working correctly.
- Allow systemd running as init_t to override the default context for key creation. BZ(#1267850)

* Thu Oct 08 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-152
- Allow pcp_pmlogger to read system state. BZ(1258699)
- Allow cupsd to connect on socket. BZ(1258089)
- Allow named to bind on ephemeral ports. BZ(#1259766)
- Allow iscsid create netlink iscsid sockets.
- We need allow connect to xserver for all sandbox_x domain because we have one type for all sandbox processes.
- Allow NetworkManager_t and policykit_t read access to systemd-machined pid files. #1255305
- Add missing labeling for /usr/libexec/abrt-hook-ccpp as a part of #1245477 and #1242467 bugs.
- Allow search dirs in sysfs types in kernel_read_security_state.
- Fix kernel_read_security_state interface that source domain of this interface can search sysctl_fs_t dirs.

* Fri Oct 02 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-151
- Update modules_filetrans_named_content() to make sure we don't get modules_dep labeling by filename transitions.
- Remove /usr/lib/modules/[^/]+/modules\..+ labeling
- Add modutils_read_module_deps_files() which is called from files_read_kernel_modules() for module deps which are still labeled as modules_dep_t.
- Remove modules_dep_t labeling for kernel module deps. depmod is a symlink to kmod which is labeled as insmod_exec_t which handles modules_object_t and there is no transition to modules_dep_t. Also some of these module deps are placed by cpio during install/update of kernel package.

* Fri Oct 02 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-150
- Allow acpid to attempt to connect to the Linux kernel via generic netlink socket.
- Clean up pkcs11proxyd policy.
- We need to require sandbox_web_type attribute in sandbox_x_domain_template().
- Revert "depmod is a symlink to insmod so it runs as insmod_t. It causes that dep kernel modules files are not created with the correct labeling modules_dep_t. This fix adds filenamtrans rules for insmod_t."
- depmod is a symlink to insmod so it runs as insmod_t. It causes that dep kernel modules files are not created with the correct labeling modules_dep_t. This fix adds filenamtrans rules for insmod_t.
- Update files_read_kernel_modules() to contain modutils_read_module_deps() calling because module deps labeling has been updated and it allows to avoid regressions.
- Update modules_filetrans_named_content() interface to cover more modules.* files.
- New policy for systemd-machined. #1255305
- In Rawhide/F24, we added pam_selinux.so support for systemd-users to have user sessions running under correct SELinux labeling. It also supports another new feature with systemd+dbus and we have sessions dbuses running with the correct labeling - unconfined_dbus_t for example.
- Allow systemd-logind read access to efivarfs - Linux Kernel configuration options for UEFI systems (UEFI Runtime Variables). #1244973, #1267207 (partial solution)
- Merge pull request #42 from vmojzis/rawhide-base
- Add interface to allow reading files in efivarfs - contains Linux Kernel configuration options for UEFI systems (UEFI Runtime Variables)

* Tue Sep 29 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-149
- Add few rules related to new policy for pkcs11proxyd
- Added new policy for pkcs11proxyd daemon
- We need to require sandbox_web_type attribute in sandbox_x_domain_template().
- Dontaudit abrt_t to rw lvm_lock_t dir.
- Allow abrt_d domain to write to kernel msg device.
- Add interface lvm_dontaudit_rw_lock_dir()
- Merge pull request #35 from lkundrak/lr-libreswan

* Tue Sep 22 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-148
- Update config.tgz to reflect changes in default context for SELinux users related to pam_selinux.so which is now used in systemd-users.
- Added support for permissive domains
- Allow rpcbind_t domain to change file owner and group
- rpm-ostree has a daemon mode now and need to speak to polkit/logind for authorization. BZ(#1264988)
- Allow dnssec-trigger to send generic signal to Network-Manager. BZ(#1242578)
- Allow smbcontrol to create a socket in /var/samba which uses for a communication with smbd, nmbd and winbind.
- Revert "Add apache_read_pid_files() interface"
- Allow dirsrv-admin read httpd pid files.
- Add apache_read_pid_files() interface
- Add label for dirsrv-admin unit file.
- Allow qpid daemon to connect on amqp tcp port.
- Allow dirsrvadmin-script read /etc/passwd file Allow dirsrvadmin-script exec systemctl
- Add labels for afs binaries: dafileserver, davolserver, salvageserver, dasalvager
- Add lsmd_plugin_t sys_admin capability, Allow lsmd_plugin_t getattr from sysfs filesystem.
- Allow rhsmcertd_t send signull to unconfined_service_t domains.
- Revert "Allow pcp to read docker lib files."
- Label /usr/libexec/dbus-1/dbus-daemon-launch-helper  as dbusd_exec_t to have systemd dbus services running in the correct domain instead of unconfined_service_t if unconfined.pp module is enabled. BZ(#1262993)
- Allow pcp to read docker lib files.
- Revert "init_t needs to be login_pgm domain because of systemd-users + pam_selinux.so"
- Add login_userdomain attribute also for unconfined_t.
- Add userdom_login_userdomain() interface.
- Label /etc/ipa/nssdb dir as cert_t
- init_t needs to be login_pgm domain because of systemd-users + pam_selinux.so
- Add interface unconfined_server_signull() to allow domains send signull to unconfined_service_t
- Call userdom_transition_login_userdomain() instead of userdom_transition() in init.te related to pam_selinux.so+systemd-users.
- Add userdom_transition_login_userdomain() interface
- Allow user domains with login_userdomain to have entrypoint access on init_exec. It is needed by pam_selinux.so call in systemd-users. BZ(#1263350)
- Add init_entrypoint_exec() interface.
- Allow init_t to have transition allow rule for userdomain if pam_selinux.so is used in /etc/pam.d/systemd-user. It ensures that systemd user sessions will run with correct userdomain types instead of init_t. BZ(#1263350)

* Mon Sep 14 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-147
- named wants to access /proc/sys/net/ipv4/ip_local_port_range to get ehphemeral range. BZ(#1260272)
- Allow user screen domains to list directorires in HOMEDIR wit user_home_t labeling.
- Dontaudit fenced search gnome config
- Allow teamd running as NetworkManager_t to access netlink_generic_socket to allow multiple network interfaces to be teamed together. BZ(#1259180)
- Fix for watchdog_unconfined_exec_read_lnk_files, Add also dir search perms in watchdog_unconfined_exec_t.
- Sanlock policy update. #1255307   - New sub-domain for sanlk-reset daemon
- Fix labeling for fence_scsi_check script
- Allow openhpid to read system state Aloow openhpid to connect to tcp http port.
- Allow openhpid to read snmp var lib files.
- Allow openvswitch_t domains read kernel dependencies due to openvswitch run modprobe
- Fix regexp in chronyd.fc file
- systemd-logind needs to be able to act with /usr/lib/systemd/system/poweroff.target to allow shutdown system. BZ(#1260175)
- Allow systemd-udevd to access netlink_route_socket to change names for network interfaces without unconfined.pp module. It affects also MLS.
- Allow unconfined_t domains to create /var/run/xtables.lock with iptables_var_run_t
- Remove bin_t label for /usr/share/cluster/fence_scsi_check\.pl

* Tue Sep 01 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-146
- Allow passenger to getattr filesystem xattr
- Revert "Allow pegasus_openlmi_storage_t create mdadm.conf.anacbak file in /etc."
- Label mdadm.conf.anackbak as mdadm_conf_t file.
- Allow dnssec-ttrigger to relabel net_conf_t files. BZ(1251765)
- Allow dnssec-trigger to exec pidof. BZ(#1256737)
- Allow blueman to create own tmp files in /tmp. (#1234647)
- Add new audit_read access vector in capability2 class
- Add "binder" security class and access vectors
- Update netlink socket classes.
- Allow getty to read network state. BZ(#1255177)
- Remove labeling for /var/db/.*\.db as etc_t to label db files as system_db_t.

* Sun Aug 30 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-145
- Allow watchdog execute fenced python script.
- Added inferface watchdog_unconfined_exec_read_lnk_files()
- Allow pmweb daemon to exec shell. BZ(1256127)
- Allow pmweb daemon to read system state. BZ(#1256128)
- Add file transition that cermonger can create /run/ipa/renewal.lock with label ipa_var_run_t.
- Revert "Revert default_range change in targeted policy"
- Allow dhcpc_t domain transition to chronyd_t

* Mon Aug 24 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-144
- Allow pmlogger to create pmlogger.primary.socket link file. BZ(1254080)
- Allow NetworkManager send sigkill to dnssec-trigger. BZ(1251764)
- Add interface dnssec_trigger_sigkill
- Allow smsd use usb ttys. BZ(#1250536)
- Fix postfix_spool_maildrop_t,postfix_spool_flush_t contexts in postfix.fc file.
- Revert default_range change in targeted policy
- Allow systemd-sysctl cap. sys_ptrace  BZ(1253926)

* Fri Aug 21 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-143
- Add ipmievd policy creaed by vmojzis@redhat.com
- Call kernel_load_module(vmware_host_t) to satisfy neverallow assertion for sys_moudle in MLS where unconfined is disabled.
- Allow NetworkManager to write audit log messages
- Add new policy for ipmievd (ipmitool).
- mirrormanager needs to be application domain and cron_system_entry needs to be called in optional block.
- Allow sandbox domain to be also /dev/mem writer
- Fix neverallow assertion for sys_module capability for openvswitch.
- kernel_load_module() needs to be called out of boolean for svirt_lxc_net_t.
- Fix neverallow assertion for sys_module capability.
- Add more attributes for sandbox domains to avoid neverallow assertion issues.  
- Add neverallow asserition fixes related to storage.
- Allow exec pidof under hypervkvp domain. Allow hypervkvp daemon create connection to the system DBUS
- Allow openhpid_t to read system state.
- Add temporary fixes for sandbox related to #1103622. It allows to run everything under one sandbox type.
- Added labels for files provided by rh-nginx18 collection
- Dontaudit block_suspend capability for ipa_helper_t, this is kernel bug. Allow ipa_helper_t capability net_admin. Allow ipa_helper_t to list /tmp. Allow ipa_helper_t to read rpm db.
- Allow rhsmcertd exec rhsmcertd_var_run_t files and rhsmcerd_tmp_t files. This rules are in hide_broken_sympthons until we find better solution.
- Update files_manage_all_files to contain auth_reader_shadow and auth_writer_shadow tosatisfy neverallow assertions.
- Update files_relabel_all_files() interface to contain auth_relabelto_shadow() interface to satisfy neverallow assertion.
- seunshare domains needs to have set_curr_context attribute to resolve neverallow assertion issues.
- Add dev_raw_memory_writer() interface
- Add auth_reader_shadow() and auth_writer_shadow() interfaces
- Add dev_raw_memory_reader() interface.
- Add storage_rw_inherited_scsi_generic() interface.
- Update files_relabel_non_auth_files() to contain seutil_relabelto_bin_policy() to make neverallow assertion working.
- Update kernel_read_all_proc() interface to contain can_dump_kernel and can_receive_kernel_messages attributes  to fix neverallow violated issue for proc_kcore_t and proc_kmsg_t.
- Update storage_rw_inherited_fixed_disk_dev() interface to use proper attributes to fix neverallow violated issues caused by neverallow check during build process.

* Tue Aug 18 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-142
- Allow samba_net_t to manage samba_var_t sock files.
- Allow httpd daemon to manage httpd_var_lib_t lnk_files.
- Allow collectd stream connect to pdns.(BZ #1191044)
- Add interface pdns_stream_connect()
- Merge branch 'rawhide-contrib' of github.com:fedora-selinux/selinux-policy into rawhide-contrib
- Allow chronyd exec systemctl
- Merge pull request #30 from vmojzis/rawhide-contrib
- Hsqldb policy upgrade -Allow sock_file management
- Add inteface chronyd_signal Allow timemaster_t send generic signals to chronyd_t.
- Hsqldb policy upgrade.  -Disallow hsqldb_tmp_t link_file management
- Hsqldb policy upgrade:  -Remove tmp link_file transition  -Add policy summary  -Remove redundant parameter for "hsqldb_admin" interface
- Label /var/run/chrony-helper dir as chronyd_var_run_t.
- Allow lldpad_t to getattr tmpfs_t. Label /dev/shm/lldpad.* as lldapd_tmpfs_t
- Fix label on /var/tmp/kiprop_0
- Add mountpoint dontaudit access check in rhsmcertd policy.
- Allow pcp_domain to manage pcp_var_lib_t lnk_files.
- Allow chronyd to execute mkdir command.
- Allow chronyd_t to read dhcpc state.
- Label /usr/libexec/chrony-helper as chronyd_exec_t
- Allow openhpid liboa_soap plugin to read resolv.conf file.
- Allow openhpid liboa_soap plugin to read generic certs.
- Allow openhpid use libwatchdog plugin. (Allow openhpid_t rw watchdog device)
- Allow logrotate to reload services.
- Allow apcupsd_t to read /sys/devices
- Allow kpropd to connect to kropd tcp port.
- Allow systemd_networkd to send logs to syslog.
- Added interface fs_dontaudit_write_configfs_dirs
- Allow audisp client to read system state.
- Label /var/run/xtables.lock as iptables_var_run_t.
-  Add labels for /dev/memory_bandwith and /dev/vhci. Thanks ssekidde
- Add interface to read/write watchdog device.
- Add transition rule for iptables_var_lib_t

* Mon Aug 10 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-141
- Allow chronyd to execute mkdir command.
- Allow chronyd_t to read dhcpc state.
- Label /usr/libexec/chrony-helper as chronyd_exec_t
- Allow openhpid liboa_soap plugin to read resolv.conf file.
- Allow openhpid liboa_soap plugin to read generic certs.
- Allow openhpid use libwatchdog plugin. (Allow openhpid_t rw watchdog device)
- Allow logrotate to reload services.
- Allow apcupsd_t to read /sys/devices
- Allow kpropd to connect to kropd tcp port.
- Allow lsmd also setuid capability. Some commands need to executed under root privs. Other commands are executed under unprivileged user.
- Allow snapperd to pass data (one way only) via pipe negotiated over dbus.
- Add snapper_read_inherited_pipe() interface.
- Add missing ";" in kerberos.te
- Add support for /var/lib/kdcproxy and label it as krb5kdc_var_lib_t. It needs to be accessible by useradd_t.
- Add support for /etc/sanlock which is writable by sanlock daemon.
- Allow mdadm to access /dev/random and add support to create own files/dirs as mdadm_tmpfs_t.
-  Add labels for /dev/memory_bandwith and /dev/vhci. Thanks ssekidde
- Add interface to read/write watchdog device.
- Add transition rule for iptables_var_lib_t
- Allow useradd add homedir located in /var/lib/kdcproxy in ipa-server RPM scriplet.
- Revert "Allow grubby to manage and create /run/blkid with correct labeling"
- Allow grubby to manage and create /run/blkid with correct labeling
- Add fstools_filetrans_named_content_fsadm() and call it for named_filetrans_domain domains. We need to be sure that /run/blkid is created with correct labeling.
- arping running as netutils_t needs to access /etc/ld.so.cache in MLS.
- Allow sysadm to execute systemd-sysctl in the sysadm_t domain. It is needed for ifup command in MLS mode.
- Add systemd_exec_sysctl() and systemd_domtrans_sysctl() interfaces.
- Allow udev, lvm and fsadm to access systemd-cat in /var/tmp/dracut if 'dracut -fv' is executed in MLS.
- Allow admin SELinu users to communicate with kernel_t. It is needed to access /run/systemd/journal/stdout if 'dracut -vf' is executed. We allow it for other SELinux users.
- depmod runs as insmod_t and it needs to manage user tmp files which was allowed for depmod_t. It is needed by dracut command for SELinux restrictive policy (confined users, MLS).

* Wed Aug 05 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-140
- firewalld needs to relabel own config files. BZ(#1250537)
- Allow rhsmcertd to send signull to unconfined_service
- Allow lsm_plugin_t to rw raw_fixed_disk.
- Allow lsm_plugin_t to read sysfs, read hwdata, rw to scsi_generic_device
- Allow openhpid to use libsnmp_bc plugin (allow read snmp lib files).

* Tue Aug 04 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-139
- Add header for sslh.if file
- Fix sslh_admin() interface
- Clean up sslh.if
- Fix typo in pdns.if
- Allow qpid to create lnk_files in qpid_var_lib_t.
- Allow httpd_suexec_t to read and write Apache stream sockets
- Merge pull request #21 from hogarthj/rawhide-contrib
- Allow virt_qemu_ga_t domtrans to passwd_t.
- use read and manage files_patterns and the description for the admin interface
- Merge pull request #17 from rubenk/pdns-policy
- Allow redis to read kernel parameters.
- Label /etc/rt dir as httpd_sys_rw_content_t BZ(#1185500)
- Allow hostapd to manage sock file in /va/run/hostapd Add fsetid cap. for hostapd Add net_raw cap. for hostpad BZ(#1237343)
- Allow bumblebee to seng kill signal to xserver
- glusterd call pcs utility which calls find for cib.* files and runs pstree under glusterd. Dontaudit access to security files and update gluster boolean to reflect these changes.
- Allow drbd to get attributes from filesystems.
- Allow drbd to read configuration options used when loading modules.
- fix the description for the write config files, add systemd administration support and fix a missing gen_require in the admin interface
- Added Booleans: pcp_read_generic_logs.
- Allow pcp_pmcd daemon to read postfix config files. Allow pcp_pmcd daemon to search postfix spool dirs.
- Allow glusterd to communicate with cluster domains over stream socket.
- fix copy paste error with writing the admin interface
- fix up the regex in sslh.fc, add sslh_admin() interface
- adding selinux policy files for sslh
- Remove diplicate sftpd_write_ssh_home boolean rule.
- Revert "Allow smbd_t and nmbd_t to manage winbind_var_run_t files/socktes/dirs."
- gnome_dontaudit_search_config() needs to be a part of optinal_policy in pegasus.te
- Allow glusterd to manage nfsd and rpcd services.
- Add kdbus.pp policy to allow access /sys/fs/kdbus. It needs to go with own module because this is workaround for now to avoid SELinux in enforcing mode.
- kdbusfs should not be accessible for now by default for shipped policies. It should be moved to kdbus.pp
- kdbusfs should not be accessible for now.
- Add support for /sys/fs/kdbus and allow login_pgm domain to access it.
- Allow sysadm to administrate ldap environment and allow to bind ldap port to allow to setup an LDAP server (389ds).
- Label /usr/sbin/chpasswd as passwd_exec_t.
- Allow audisp_remote_t to read/write user domain pty.
- Allow audisp_remote_t to start power unit files domain to allow halt system.

* Mon Jul 20 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-138
- Add fixes for selinux-policy packages to reflect the latest changes related to policy module store migration.
- Prepare selinux-policy package for SELinux store migration
- gnome_dontaudit_search_config() needs to be a part of optinal_policy in pegasus.te
- Allow glusterd to manage nfsd and rpcd services.
- Allow smbd_t and nmbd_t to manage winbind_var_run_t files/socktes/dirs.
- Add samba_manage_winbind_pid() interface
- Allow networkmanager to  communicate via dbus with systemd_hostanmed.
- Allow stream connect logrotate to prosody.
- Add prosody_stream_connect() interface.
-  httpd should be able to send signal/signull to httpd_suexec_t, instead of httpd_suexec_exec_t.
- Allow prosody to create own tmp files/dirs.
- Allow keepalived request kernel load module
- kadmind should not read generic files in /usr
- Allow kadmind_t access to /etc/krb5.keytab
- Add more fixes to kerberos.te
- Add labeling for /var/tmp/kadmin_0 and /var/tmp/kiprop_0
- Add lsmd_t to nsswitch_domain.
- Allow pegasus_openlmi_storage_t create mdadm.conf.anacbak file in /etc.
- Add fixes to pegasus_openlmi_domain
- Allow Glance Scrubber to connect to commplex_main port
- Allow RabbitMQ to connect to amqp port
- Allow isnsd read access on the file /proc/net/unix
- Allow qpidd access to /proc/<pid>/net/psched
- Allow openshift_initrc_t to communicate with firewalld over dbus.
- Allow ctdbd_t send signull to samba_unconfined_net_t.
- Add samba_signull_unconfined_net()
- Add samba_signull_winbind()
- Revert "Add interfaces winbind_signull(), samba_unconfined_net_signull()."
- Fix ctdb policy
- Label /var/db/ as system_db_t.

* Wed Jul 15 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-137
- inn daemon should create innd_log_t objects in var_log_t instead of innd_var_run_t
- Fix rule definitions for httpd_can_sendmail boolean. We need to distinguish between base and contrib.

* Tue Jul 14 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-136
- Add samba_unconfined_script_exec_t to samba_admin header.
- Add jabberd_lock_t label to jabberd_admin header.
- Add rpm_var_run_t label to rpm_admin header.
- Make all interfaces related to openshift_cache_t as deprecated.
- Remove non exits nfsd_ro_t label.
- Label /usr/afs/ as afs_files_t Allow afs_bosserver_t create afs_config_t and afs_dbdir_t dirs under afs_files_t Allow afs_bosserver_t read kerberos config
- Fix *_admin intefaces where body is not consistent with header.
- Allow networkmanager read rfcomm port.
- Fix nova_domain_template interface, Fix typo bugs in nova policy
- Create nova sublabels.
- Merge all nova_* labels under one nova_t.
- Add cobbler_var_lib_t to "/var/lib/tftpboot/boot(/.*)?"
- Allow dnssec_trigger_t relabelfrom dnssec_trigger_var_run_t files.
- Fix label openstack-nova-metadata-api binary file
- Allow nova_t to bind on geneve tcp port, and all udp ports
- Label swift-container-reconciler binary as swift_t.
- Allow glusterd to execute showmount in the showmount domain.
- Allow NetworkManager_t send signull to dnssec_trigger_t.
- Add support for openstack-nova-* packages.
- Allow audisp-remote searching devpts.
- Label 6080 tcp port as geneve

* Thu Jul 09 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-135
- Update mta_filetrans_named_content() interface to cover more db files.
- Revert "Remove ftpd_use_passive_mode boolean. It does not make sense due to ephemeral port handling."
- Allow pcp domains to connect to own process using unix_stream_socket.
- Typo in abrt.te
- Allow  abrt-upload-watch service to dbus chat with ABRT daemon and fsetid capability to allow run reporter-upload correctly.
- Add nagios_domtrans_unconfined_plugins() interface.
- Add nagios_domtrans_unconfined_plugins() interface.
- Add new boolean - httpd_run_ipa to allow httpd process to run IPA helper and dbus chat with oddjob.
- Add support for oddjob based helper in FreeIPA. BZ(1238165)
- Allow dnssec_trigger_t create dnssec_trigger_tmp_t files in /var/tmp/ BZ(1240840)
- Allow ctdb_t sending signull to smbd_t, for checking if smbd process exists. BZ(1224879)
- Fix cron_system_cronjob_use_shares boolean to call fs interfaces which contain only entrypoint permission.
- Add cron_system_cronjob_use_shares boolean to allow system cronjob to be executed from shares - NFS, CIFS, FUSE. It requires "entrypoint" permissios on nfs_t, cifs_t and fusefs_t SELinux types.
- nrpe needs kill capability to make gluster moniterd nodes working.
- Revert "Dontaudit ctbd_t sending signull to smbd_t."
- Fix interface corenet_tcp_connect_postgresql_port_port(prosody_t)
- Allow prosody connect to postgresql port.
- Fix logging_syslogd_run_nagios_plugins calling in logging.te
- Add logging_syslogd_run_nagios_plugins boolean for rsyslog to allow transition to nagios unconfined plugins.
- Add support for oddjob based helper in FreeIPA. BZ(1238165)
- Add new interfaces
- Add fs_fusefs_entry_type() interface.

* Thu Jul 02 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-134
- Allow ctdb_t sending signull to smbd_t, for checking if smbd process exists. BZ(1224879)
- Fix cron_system_cronjob_use_shares boolean to call fs interfaces which contain only entrypoint permission.
- Add cron_system_cronjob_use_shares boolean to allow system cronjob to be executed from shares - NFS, CIFS, FUSE. It requires "entrypoint" permissios on nfs_t, cifs_t and fusefs_t SELinux types.
- Merge remote-tracking branch 'refs/remotes/origin/rawhide-contrib' into rawhide-contrib
- nrpe needs kill capability to make gluster moniterd nodes working.
- Fix interface corenet_tcp_connect_postgresql_port_port(prosody_t)
- Allow prosody connect to postgresql port.
- Add new interfaces
- Add fs_fusefs_entry_type() interface.

* Tue Jun 30 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-133
- Cleanup permissive domains.

* Mon Jun 29 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-132
- Rename xodbc-connect port to xodbc_connect
- Dontaudit apache to manage snmpd_var_lib_t files/dirs. BZ(1189214)
- Add interface snmp_dontaudit_manage_snmp_var_lib_files().
- Allow ovsdb-server to connect on xodbc-connect and ovsdb tcp ports. BZ(1179809)
- Dontaudit mozilla_plugin_t cap. sys_ptrace. BZ(1202043)
- Allow iscsid write to fifo file kdumpctl_tmp_t. Appears when kdump generates the initramfs during the kernel boot. BZ(1181476)
- Dontaudit chrome to read passwd file. BZ(1204307)
- Allow firewalld exec ldconfig. BZ(1232748)
- Allow dnssec_trigger_t read networkmanager conf files. BZ(1231798)
- Allow in networkmanager_read_conf() also read NetworkManager_etc_rw_t files. BZ(1231798)
- Allow NetworkManager write to sysfs. BZ(1234086)
- Fix bogus line in logrotate.fc.
- Add dontaudit interface for kdumpctl_tmp_t
- Rename xodbc-connect port to xodbc_connect
- Label tcp port 6632 as xodbc-connect port. BZ (1179809)
- Label tcp port 6640 as ovsdb port. BZ (1179809)

* Tue Jun 23 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-131
- Allow NetworkManager write to sysfs. BZ(1234086)
- Fix bogus line in logrotate.fc.
- Add dontaudit interface for kdumpctl_tmp_t
- Use userdom_rw_user_tmp_files() instead of userdom_rw_user_tmpfs_files() in gluster.te
- Add postgresql support for systemd unit files.
- Fix missing bracket
- Pull request by ssekidde. https://github.com/fedora-selinux/selinux-policy/pull/18
- Fixed obsoleted userdom_delete_user_tmpfs_files() inteface

* Thu Jun 18 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-130
- Allow glusterd to interact with gluster tools running in a user domain
- rpm_transition_script() is called from rpm_run. Update cloud-init rules.
- Call rpm_transition_script() from rpm_run() interface.
- Allow radvd has setuid and it requires dac_override. BZ(1224403)
- Add glusterd_manage_lib_files() interface.
- Allow samba_t net_admin capability to make CIFS mount working.
- S30samba-start gluster hooks wants to search audit logs. Dontaudit it.
- Reflect logrotate change which moves /var/lib/logrotate.status to /var/lib/logrotate/logrotate.status. BZ(1228531)
- ntop reads /var/lib/ntop/macPrefix.db and it needs dac_override. It has setuid/setgid. BZ(1058822)
- Allow cloud-init to run rpm scriptlets to install packages. BZ(1227484)
- Allow nagios to generate charts.
- Allow glusterd to send generic signals to systemd_passwd_agent processes.
- Allow glusterd to run init scripts.
- Allow glusterd to execute /usr/sbin/xfs_dbin glusterd_t domain.
- Calling cron_system_entry() in pcp_domain_template needs to be a part of optional_policy block.
- Allow samba-net to access /var/lib/ctdbd dirs/files.
- Allow glusterd to send a signal to smbd.
- Make ctdbd as home manager to access also FUSE.
- Allow glusterd to use geo-replication gluster tool.
- Allow glusterd to execute ssh-keygen.
- Allow glusterd to interact with cluster services.
- Add rhcs_dbus_chat_cluster()
- systemd-logind accesses /dev/shm. BZ(1230443)
- Label gluster python hooks also as bin_t.
- Allow sshd to execute gnome-keyring if there is configured pam_gnome_keyring.so.
- Allow gnome-keyring executed by passwd to access /run/user/UID/keyring to change a password.

* Tue Jun 09 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-129
- We need to restore contexts on /etc/passwd*,/etc/group*,/etc/*shadow* during install phase to get proper labeling for these files until selinux-policy pkgs are installed. BZ(1228489)

* Tue Jun 09 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-128
- Add ipsec_rw_inherited_pipes() interface.
- Allow ibus-x11 running as xdm_t to connect uder session buses. We already allow to connect to userdomains over unix_stream_socket. 
- Label /usr/libexec/Xorg.wrap as xserver_exec_t.
- Allow systemd-networkd to bind dhcpc ports if DHCP=yes in *.network conf file.
- Add fixes for selinux userspace moving the policy store to /var/lib/selinux.
- Remove optional else block for dhcp ping (needed by CIL)
- Label all gluster hooks in /var/lib/gluster as bin_t. They are not created on the fly.
- Access required to run with unconfine.pp disabled
- Fix selinux_search_fs() interface.
- Update selinux_search_fs(domain) rule to have ability to search /etc/selinuc/ to check if /etc/selinux/config exists. 
- Add seutil_search_config() interface.
- Make ssh-keygen as nsswitch domain to access SSSD.
- Label ctdb events scripts as bin_t.
- Add support for /usr/sbin/lvmpolld.
- Allow gvfsd-fuse running as xdm_t to use /run/user/42/gvfs as mountpoint.
- Add support for ~/.local/share/networkmanagement/certificates and update filename transitions rules. 
- Allow login_pgm domains to access kernel keyring for nsswitch domains.
- Allow hypervkvp to read /dev/urandom and read  addition states/config files.
- Add cgdcbxd policy.
- Allow hypervkvp to execute arping in own domain and make it as nsswitch domain.
- Add labeling for pacemaker.log.
- Allow ntlm_auth running in winbind_helper_t to access /dev/urandom.
- Allow lsmd plugin to connect to tcp/5989 by default.
- Allow lsmd plugin to connect to tcp/5988 by default.
- Allow setuid/setgid for selinux_child.
- Allow radiusd to connect to radsec ports.
- ALlow bind to read/write inherited ipsec pipes.
- Allow fowner capability for sssd because of selinux_child handling.
- Allow pki-tomcat relabel pki_tomcat_etc_rw_t.
- Allow cluster domain to dbus chat with systemd-logind.
- Allow tmpreaper_t to manage ntp log content 
- Allow openvswitch_t to communicate with sssd.
- Allow isnsd_t to communicate with sssd.
- Allow rwho_t to communicate with sssd.
- Allow pkcs_slotd_t to communicate with sssd.
- Add httpd_var_lib_t label for roundcubemail 
- Allow puppetagent_t to transfer firewalld messages over dbus.
- Allow glusterd to have mknod capability. It creates a special file using mknod in a brick.
- Update rules related to glusterd_brick_t.
- Allow glusterd to execute lvm tools in the lvm_t target domain.
- Allow glusterd to execute xfs_growfs in the target domain.
- Allow sysctl to have running under hypervkvp_t domain.
- Allow smartdnotify to use user terminals. 
- Allow pcp domains to create root.socket in /var/lip/pcp directroy. 
- Allow NM to execute dnssec-trigger-script in dnssec_trigger_t domain.
- Allow rpcbind to create rpcbind.xdr as a temporary file. 
- Allow dnssec-trigger connections to the system DBUS. It uses libnm-glib Python bindings. 
- Allow hostapd net_admin capability. hostapd needs to able to set an interface flag. 
- rsync server can be setup to send mail
- Make "ostree admin upgrade -r" command which suppose to upgrade the system and reboot working again. 
- Remove ctdbd_manage_var_files() interface which is not used and is declared for the wrong type.
- Fix samba_load_libgfapi decl in samba.te.
- Fix typo in nagios_run_sudo() boolean.
- remove duplicate declaration from hypervkvp.te.
- Move ctdd_domtrans() from ctdbd to gluster.
- Allow smbd to access /var/lib/ctdb/persistent/secrets.tdb.0.
- Glusterd wants to manage samba config files if they are setup together.
- ALlow NM to do access check on /sys.
- Allow NetworkManager to keep RFCOMM connection for Bluetooth DUN open . Based on fixes from Lubomir Rintel.
- Allow NetworkManager nm-dispacher to read links.
- Allow gluster hooks scripts to transition to ctdbd_t.
- Allow glusterd to read/write samba config files.
- Update mysqld rules related to mysqld log files.
- Add fixes for hypervkvp realed to ifdown/ifup scripts.
- Update netlink_route_socket for ptp4l.
- Allow glusterd to connect to /var/run/dbus/system_bus_socket.
- ALlow glusterd to have sys_ptrace capability. Needed by gluster+samba configuration.
- Add new boolean samba_load_libgfapi to allow smbd load libgfapi from gluster. Allow smbd to read gluster config files by default.
- Allow gluster to transition to smbd. It is needed for smbd+gluster configuration.
- Allow glusterd to read /dev/random.
- Update nagios_run_sudo boolean to allow run chkpwd.
- Allow docker and container tools to control caps, don't rely on SELinux for now.  Since there is no easy way for SELinux modification of policy as far as caps.  docker run --cap-add will work now
- Allow sosreport to dbus chat with NM.
- Allow anaconda to run iscsid in own domain. BZ(1220948).
- Allow rhsmcetd to use the ypbind service to access NIS services.
- Add nagios_run_pnp4nagios and nagios_run_sudo booleans to allow run sudo from NRPE utils scripts and allow run nagios in conjunction with PNP4Nagios.
- Allow ctdb to create rawip socket.
- Allow ctdbd to bind  smbd port.
- Make ctdbd as userdom_home_reader.
- Dontaudit chrome-sandbox write access its parent process information. BZ(1220958)
- Allow net_admin cap for dnssec-trigger to make wifi reconnect working.
- Add support for /var/lib/ipsilon dir and label it as httpd_var_lib_t. BZ(1186046)
- Allow gluster rpm scripletto create glusterd socket with correct labeling. This is a workaround until we get fix in glusterd.
- Add glusterd_filetrans_named_pid() interface.
- Allow antivirus_t to read system state info.
- Dontaudit use console for chrome-sandbox. 
- Add support for ~/.local/share/libvirt/images and for ~/.local/share/libvirt/boot. 
- Clamd needs to have fsetid capability. 
- Allow cinder-backup to dbus chat with systemd-logind. 
- Update httpd_use_openstack boolean to allow httpd to bind commplex_main_port and read keystone log files.
- Allow gssd to access kernel keyring for login_pgm domains.
- Add more fixes related to timemaster+ntp+ptp4l.
- Allow docker sandbox domains to search all mountpoiunts
- update winbind_t rules to allow IPC for winbind.
- Add rpm_exec_t labeling for /usr/bin/dnf-automatic,/usr/bin/dnf-2 and /usr/bin/dnf-3.
- Allow inet_gethost called by couchdb to access /proc/net/unix. 
- Allow eu-unstrip running under abrt_t to access /var/lib/pcp/pmdas/linux/pmda_linux.so 
- Label /usr/bin/yum-deprecated as rpm_exec_t. 

* Tue May 05 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-127
- Add missing typealiases in apache_content_template() for script domain/executable.
- Don't use deprecated userdom_manage_tmpfs_role() interface calliing and use userdom_manage_tmp_role() instead.
- Add support for new cobbler dir locations:
- Add support for iprdbg logging files in /var/log.
- Add relabel_user_home_dirs for use by docker_t

* Thu Apr 30 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-126
- allow httpd_t to read nagios lib_var_lib_t to allow rddtool generate graphs which will be shown by httpd .
- Add nagios_read_lib() interface.
- Additional fix for mongod_unit_file_t in mongodb.te.
- Fix decl of mongod_unit_file to mongod_unit_file_t.
- Fix mongodb unit file declaration.
- Update virt_read_pid_files() interface to allow read also symlinks with virt_var_run_t type.
- Fix labeling for /usr/libexec/mysqld_safe-scl-helper.
- Add support for mysqld_safe-scl-helper which is needed for RHSCL daemons.
- Allow sys_ptrace cap for sblim-gatherd caused by ps.
- Add support for /usr/libexec/mongodb-scl-helper RHSCL helper script.
- Add support for mongod/mongos systemd unit files.
- Allow dnssec-trigger to send sigchld to networkmanager
- add interface networkmanager_sigchld
- Add dnssec-trigger unit file Label dnssec-trigger script in libexec
- Remove duplicate  specification for /etc/localtime.
- Add default labeling for /etc/localtime symlink.

* Mon Apr 20 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-125
- Define ipa_var_run_t type
- Allow certmonger to manage renewal.lock. BZ(1213256)
- Add ipa_manage_pid_files interface.
- Add rules for netlink_socket in iotop.
- Allow iotop netlink socket.
- cloudinit and rhsmcertd need to communicate with dbus
- Allow apcupsd to use USBttys. BZ(1210960)
- Allow sge_execd_t to mamange tmp sge lnk files.BZ(1211574)
- Remove dac_override capability for setroubleshoot. We now have it running as setroubleshoot user.
- Allow syslogd_t to manage devlog_t lnk files. BZ(1210968)

* Wed Apr 15 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-124
- Add more restriction on entrypoint for unconfined domains.

* Tue Apr 14 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-123
- Allow abrtd to list home config. BZ(1199658)
- Dontaudit dnssec_trigger_t to read /tmp. BZ(1210250)
- Allow abrt_dump_oops_t to IPC_LOCK. BZ(1205481)
- Allow mock_t to use ptmx. BZ(1181333)
- Allow dnssec_trigger_t to stream connect to networkmanager.
- Allow dnssec_trigger_t to create resolv files labeled as net_conf_t
- Fix labeling for keystone CGI scripts.

* Tue Apr 07 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-122
- Label /usr/libexec/mongodb-scl-helper as mongod_initrc_exec_t. BZ(1202013)
- Add mongodb port to httpd_can_network_connect_db interface. BZ(1209180)
- Allow mongod to work with configured SSSD.
- Add collectd net_raw capability. BZ(1194169)
- Merge postfix spool types(maildrop,flush) to one postfix_spool_t
- Allow dhcpd kill capability.
- Make rwhod as nsswitch domain.
- Add support for new fence agent fence_mpath which is executed by fence_node.
- Fix cloudform policy.(m4 is case sensitive)
- Allow networkmanager and cloud_init_t to dbus chat
- Allow lsmd plugin to run with configured SSSD.
- Allow bacula access to tape devices.
- Allow sblim domain to read sysctls..
- Allow timemaster send a signal to ntpd.
- Allow mysqld_t to use pam.It is needed by MariDB if auth_apm.so auth plugin is used.
- two 'l' is enough.
- Add labeling for systemd-time*.service unit files and allow systemd-timedated to access these unit files.
- Allow polkit to dbus chat with xserver. (1207478)
- Add lvm_stream_connect() interface.
- Set label of /sys/kernel/debug

* Mon Mar 30 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-121
- Allow kmscon to read system state. BZ (1206871)
- Label ~/.abrt/ as abrt_etc_t. BZ(1199658)
- Allow xdm_t to read colord_var_lib_t files. BZ(1201985)

* Mon Mar 23 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-120
- Allow mysqld_t to use pam. BZ(1196104)
- Added label mysqld_etc_t for /etc/my.cnf.d/ dir. BZ(1203989)
- Allow fetchmail to read mail_spool_t. BZ(1200552)
- Dontaudit blueman_t write to all mountpoints. BZ(1198272)
- Allow all domains some process flags.
- Merge branch 'rawhide-base' of github.com:selinux-policy/selinux-policy into rawhide-base
- Turn on overlayfs labeling for testin, we need this backported to F22 and Rawhide.  Eventually will need this in RHEL

* Wed Mar 18 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-119
- build without docker

* Mon Mar 16 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-118
- docker watches for content in the /etc directory
- Merge branch 'rawhide-contrib' of github.com:selinux-policy/selinux-policy into rawhide-contrib
- Fix abrt_filetrans_named_content() to create /var/tmp/abrt with the correct abrt_var_cache_t labeling.
- Allow docker to communicate with openvswitch
- Merge branch 'rawhide-contrib' of github.com:selinux-policy/selinux-policy into rawhide-contrib
- Allow docker to relablefrom/to sockets and docker_log_t
- Allow journald to set loginuid. BZ(1190498)
- Add cap. sys_admin for passwd_t. BZ(1185191)
- Allow abrt-hook-ccpp running as kernel_t to allow create /var/tmp/abrt with correct labeling.

* Mon Mar 09 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-117
- Allow spamc read spamd_etc_t files. BZ(1199339).
- Allow collectd to write to smnpd_var_lib_t dirs. BZ(1199278)
- Allow abrt_watch_log_t read passwd file. BZ(1197396)
- Allow abrt_watch_log_t to nsswitch_domain. BZ(1199659)
- Allow cups to read colord_var_lib_t files. BZ(1199765)

* Fri Mar 06 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-116
- Turn on rolekit in F23

* Thu Mar 05 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-115
- Allow glusterd_t exec glusterd_var_lib_t files. BZ(1198406)
- Add gluster_exec_lib interface.
- Allow l2tpd to manage NetworkManager pid files
- Allow firewalld_t relabelfrom firewalld_rw_etc_t. BZ(1195327)
- Allow cyrus bind tcp berknet port. BZ(1198347)
- Add nsswitch domain for more serviecs.
- Allow abrt_dump_oops_t read /etc/passwd file. BZ(1197190)
- Remove ftpd_use_passive_mode boolean. It does not make sense due to ephemeral port handling.
- Make munin yum plugin as unconfined by default.
- Allow bitlbee connections to the system DBUS.
- Allow system apache scripts to send log messages.
- Allow denyhosts execute iptables. BZ(1197371)
- Allow brltty rw event device. BZ(1190349)
- Allow cupsd config to execute ldconfig. BZ(1196608)
- xdm_t now needs to manage user ttys
- Allow ping_t read urand. BZ(1181831)
- Add support for tcp/2005 port.
- Allow setfiles domain to access files with admin_home_t. semanage -i /root/testfile.
- In F23 we are running xserver as the user, need this to allow confined users to us X

* Wed Feb 25 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-114
- Fix source filepath for moving html files.

* Mon Feb 23 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-113
- Xserver needs to be transitioned to from confined users
- Added logging_syslogd_pid_filetrans
- xdm_t now talks to hostnamed
- Label new strongswan binary swanctl and new unit file strongswan-swanctl.service. BZ(1193102)
- Additional fix for labeleling /dev/log correctly.
- cups chats with network manager
- Allow parent domains to read/write fifo files in mozilla plugin
- Allow spc_t to transition to svirt domains
- Cleanup spc_t
- docker needs more control over spc_t
- pcp domains are executed out of cron

* Mon Feb 16 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-112
- Allow audisp to connect to system DBUS for service.
- Label /dev/log correctly.
- Add interface init_read_var_lib_files().
- Allow abrt_dump_oops_t read /var/lib/systemd/, Allow abrt_dump_oops_t cap. chown,fsetid,fowner, BZ(1187017)

* Tue Feb 10 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-111
- Label /usr/libexec/postgresql-ctl as postgresql_exec_t. BZ(1191004)
- Remove automatcically running filetrans_named_content form sysnet_manage_config
- Allow syslogd/journal to read netlink audit socket
- Allow brltty ioctl on usb_device_t. BZ(1190349)
- Make sure NetworkManager configures resolv.conf correctly

* Thu Feb 05 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-110
- Allow cockpit_session_t to create tmp files
- apmd needs sys_resource when shutting down the machine
- Fix path label to resolv.conf under NetworkManager

* Wed Feb 04 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-109
- Allow search all pid dirs when managing net_conf_t files.

* Wed Feb 04 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-108
- Fix labels, improve sysnet_manage_config interface.
- Label /var/run/NetworkManager/resolv.conf.tmp as net_conf_t.
- Dontaudit network connections related to thumb_t. BZ(1187981)
- Remove sysnet_filetrans_named_content from fail2ban

* Mon Feb 02 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-107
- Fix labels on new location of resolv.conf
- syslog is not writing to the audit socket
- seunshare is doing getattr on unix_stream_sockets leaked into it
- Allow sshd_t to manage gssd keyring
- Allow apps that create net_conf_t content to create .resolv.conf.NetworkManager
- Posgresql listens on port 9898 when running PCP (pgpool Control Port)
- Allow svirt sandbox domains to read /proc/mtrr
- Allow polipo_deamon connect to all ephemeral ports. BZ(1187723)
- Allow dovecot domains to use sys_resouce
- Allow sshd_t to manage gssd keyring
- gpg_pinentry_t needs more access in f22

* Thu Jan 29 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-106
- Allow docker to attach to the sandbox and user domains tun devices
- Allow pingd to read /dev/urandom. BZ(1181831)
- Allow virtd to list all mountpoints
- Allow sblim-sfcb to search images
- pkcsslotd_lock_t should be an alias for pkcs_slotd_lock_t.
- Call correct macro in virt_read_content().
- Dontaudit couchdb search in gconf_home_t. BZ(1177717)
- Allow docker_t to changes it rlimit
- Allow neutron to read rpm DB.
- Allow radius to connect/bind radsec ports
- Allow pm-suspend running as virt_qemu_ga to read /var/log/pm-suspend.log.
- Add devicekit_read_log_files().
- Allow  virt_qemu_ga to dbus chat with rpm.
- Allow netutils chown capability to make tcpdump working with -w.
- Label /ostree/deploy/rhel-atomic-host/deploy directory as system_conf_t.
- journald now reads the netlink audit socket
- Add auditing support for ipsec.

* Thu Jan 29 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-105
- Bump release

* Thu Jan 15 2015 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-104
- remove duplicate filename transition rules.
- Call proper interface in sosreport.te.
- Allow fetchmail to manage its keyring
- Allow mail munin to create udp_sockets
- Allow couchdb to sendto kernel unix domain sockets

* Sat Jan 3 2015 Dan Walsh <dwalsh@redhat.com> 3.13.1-103
- Add /etc/selinux/targeted/contexts/openssh_contexts

* Mon Dec 15 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-101
- Allow logrotate to read hawkey.log in /var/cache/dnf/ BZ(1163438)
- Allow virt_qemu_ga_t to execute kmod.
- Add missing files_dontaudit_list_security_dirs() for smbd_t in samba_export_all_ro boolean
- Add additionnal MLS attribute for oddjob_mkhomedir to create homedirs.
- Add support for /usr/share/vdsm/daemonAdapter.
- Docker has a new config/key file it writes to /etc/docker
- Allow bacula to connect also to postgresql.

* Thu Dec 11 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-100
- Allow admin SELinux users mounting / as private within a new mount namespace as root in MLS.
- Fix miscfiles_manage_generic_cert_files() to allow manage link files
- Allow pegasus_openlmi_storage_t use nsswitch. BZ(1172258)
- Add support for /var/run/gluster.
- Allow openvpn manage systemd_passwd_var_run_t files. BZ(1170085)

* Tue Dec 02 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-99
- Add files_dontaudit_list_security_dirs() interface.
- Added seutil_dontaudit_access_check_semanage_module_store interface.
- Allow docker to create /root/.docker
- Allow rlogind to use also rlogin ports
- dontaudit list security dirs for samba domain
- Dontaudit couchdb to list /var

* Sat Nov 29 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-98
- Update to have all _systemctl() interface also init_reload_services()
- Dontaudit access check on SELinux module store for sssd.
- Label /var/lib/rpmrebuilddb/ as rpm_var_lib_t. BZ (1167946)

* Fri Nov 28 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-97
- Allow reading of symlinks in /etc/puppet
- Added TAGS to gitignore
- I guess there can be content under /var/lib/lockdown #1167502
- Allow rhev-agentd to read /dev/.udev/db to make deploying hosted engine via iSCSI working.
- Allow keystone to send a generic signal to own process.
- Allow radius to bind tcp/1812 radius port.
- Dontaudit list user_tmp files for system_mail_t
- label virt-who as virtd_exec_t
- Allow rhsmcertd to send a null signal to virt-who running as virtd_t
- Add virt_signull() interface
- Add missing alias for _content_rw_t
- Allow .snapshots to be created in other directories, on all mountpoints
- Allow spamd to access razor-agent.log
- Add fixes for sfcb from libvirt-cim TestOnly bug. (#1152104)
- Allow .snapshots to be created in other directories, on all mountpoints
- Label tcp port 5280 as ejabberd port. BZ(1059930)
- Make /usr/bin/vncserver running as unconfined_service_t
- Label /etc/docker/certs.d as cert_t
- Allow all systemd domains to search file systems

* Thu Nov 20 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-96
- Allow NetworkManager stream connect on openvpn. BZ(1165110)

* Wed Nov 19 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-95
- Allow networkmanager manage also openvpn sock pid files.

* Wed Nov 19 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-94
- Allow openvpn to create uuid connections in /var/run/NetworkManager with NM labeling.
- Allow sendmail to create dead.letter. BZ(1165443)
- Allow selinux_child running as sssd access check on /etc/selinux/targeted/modules/active.
- Allow access checks on setfiles/load_policy/semanage_lock for selinux_child running as sssd_t.
- Label sock file charon.vici as ipsec_var_run_t. BZ(1165065)
- Add additional interfaces for load_policy/setfiles/read_lock related to access checks.

* Fri Nov 14 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-93
- Allow bumblebee to use nsswitch. BZ(1155339)
- Allow openvpn to stream connect to networkmanager. BZ(1164182)
- Allow smbd to create HOMEDIRS is pam_oddjob_mkhomedir in MLS.
- Allow cpuplug rw virtual memory sysctl. BZ (1077831)
- Docker needs to write to sysfs, needs back port to F20,F21, RHEL7

* Mon Nov 10 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-92
- Add kdump_rw_inherited_kdumpctl_tmp_pipes()
- Added fixes related to linuxptp. BZ (1149693)
- Label keystone cgi files as keystone_cgi_script_exec_t. BZ(1138424
- Dontaudit policykit_auth_t to access to user home dirs. BZ (1157256)
- Fix seutil_dontaudit_access_check_load_policy()
- Add dontaudit interfaces for audit_access in seutil
- Label /etc/strongimcv as ipsec_conf_file_t.

* Fri Nov 07 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-91
- Added interface userdom_dontaudit_manage_user_home_dirs
- Fix unconfined_server_dbus_chat() interface.
- Add unconfined_server_dbus_chat() inteface.
- Allow login domains to create kernel keyring with different level.
- Dontaudit policykit_auth_t to write to user home dirs. BZ (1157256)
- Make tuned as unconfined domain.
- Added support for linuxptp policy. BZ(1149693)
- make zoneminder as dbus client by default.
- Allow bluetooth read/write uhid devices. BZ (1161169)
- Add fixes for hypervkvp daemon
- Allow guest to connect to libvirt using unix_stream_socket.
- Allow all bus client domains to dbus chat with unconfined_service_t.
- Allow inetd service without own policy to run in inetd_child_t which is unconfined domain.
- Make opensm as nsswitch domain to make it working with sssd.
- Allow brctl to read meminfo.
- Allow winbind-helper to execute ntlm_auth in the caller domain.
- Make plymouthd as nsswitch domain to make it working with sssd.
- Make drbd as nsswitch domain to make it working with sssd.
- Make conman as nsswitch domain to make ipmitool.exp runing as conman_t working.
- Add support for /var/lib/sntp directory.

* Mon Nov 03 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-90
- Add support for /dev/nvme controllerdevice nodes created by nvme driver.
- Add 15672 as amqp_port_t
- Allow wine domains to read user homedir content
- Add fixes to allow docker to create more content in tmpfs ,and donaudit reading /proc
- Allow winbind to read usermodehelper
- Allow telepathy domains to execute shells and bin_t
- Allow gpgdomains to create netlink_kobject_uevent_sockets
- Allow abrt to read software raid state. BZ (1157770)
- Fix rhcs_signull_haproxy() interface.
-  Add suppor for keepalived unconfined scripts and allow keepalived to read all domain state and kill capability.
- Allow snapperd to dbus chat with system cron jobs.
- Allow nslcd to read /dev/urandom.
- Allow dovecot to create user's home directory when they log into IMAP.
- Label also logrotate.status.tmp as logrotate_var_lib_t. BZ(1158835)
- Allow wine domains to read user homedir content
- Add fixes to allow docker to create more content in tmpfs ,and donaudit reading /proc

* Wed Oct 29 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-89
- Allow keystone_cgi_script_t to bind on commplex_main_port. BZ (#1138424)
- Allow freeipmi_bmc_watchdog rw_sem_perms to freeipmi_ipmiseld
- Allow rabbitmq to read nfs state data. BZ(1122412)
- Allow named to read /var/tmp/DNS_25 labeled as krb5_host_rcache_t.
- Add rolekit policy
- ALlow rolekit domtrans to sssd_t.
- Add kerberos_tmp_filetrans_kadmin() interface.
- rolekit should be noaudit.
- Add rolekit_manage_keys().
- Need to label rpmnew file correctly
- Allow modemmanger to connectto itself

* Tue Oct 21 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-88
- Allow couchdb read sysctl_fs_t files. BZ(1154327)
- Allow osad to connect to jabber client port. BZ (1154242)
- Allow mon_statd to send syslog msgs. BZ (1077821
- Allow apcupsd to get attributes of filesystems with xattrs

* Fri Oct 17 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-87
- Allow systemd-networkd to be running as dhcp client.
- Label /usr/bin/cockpit-bridge as shell_exec_t.
- Add label for /var/run/systemd/resolve/resolv.conf.
- ALlow listen and accept on tcp socket for init_t in MLS. Previously it was for xinetd_t.
- Allow systemd-networkd to be running as dhcp client.
- Label /usr/bin/cockpit-bridge as shell_exec_t.
- Add label for /var/run/systemd/resolve/resolv.conf.
- ALlow listen and accept on tcp socket for init_t in MLS. Previously it was for xinetd_t.

* Tue Oct 14 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-86
- Dontaudit aicuu to search home config dir. BZ (#1104076)
- couchdb is using erlang so it needs execmem privs
- ALlow sanlock to send a signal to virtd_t.
- Allow mondogdb to  'accept' accesses on the tcp_socket port.
- Make sosreport as unconfined domain.
- Allow nova-console to connect to mem_cache port.
- Allow mandb to getattr on file systems
- Allow read antivirus domain all kernel sysctls.
- Allow lmsd_plugin to read passwd file. BZ(1093733)
- Label /usr/share/corosync/corosync as cluster_exec_t.
- ALlow sensord to getattr on sysfs.
- automount policy is non-base module so it needs to be called in optional block.
- Add auth_use_nsswitch for portreserve to make it working with sssd.
- Fix samba_export_all_ro/samba_export_all_rw booleans to dontaudit search/read security files.
- Allow openvpn to execute  systemd-passwd-agent in  systemd_passwd_agent_t to make openvpn working with systemd.
- Allow openvpn to access /sys/fs/cgroup dir.
- Allow nova-scheduler to read certs
- Add support for /var/lib/swiftdirectory.
- Allow neutron connections to system dbus.
- Allow mongodb to manage own log files.
- Allow opensm_t to read/write /dev/infiniband/umad1.
- Added policy for mon_statd and mon_procd services. BZ (1077821)
- kernel_read_system_state needs to be called with type. Moved it to antivirus.if.
- Allow dnssec_trigger_t to execute unbound-control in own domain.
- Allow all RHCS services to read system state.
- Added monitor device
- Add interfaces for /dev/infiniband
- Add infiniband_device_t for /dev/infiniband instead of fixed_disk_device_t type.
- Add files_dontaudit_search_security_files()
- Add selinuxuser_udp_server boolean
- ALlow syslogd_t to create /var/log/cron  with correct labeling
- Add support for /etc/.updated and /var/.updated
- Allow iptables read fail2ban logs. BZ (1147709)
- ALlow ldconfig to read proc//net/sockstat.

* Mon Oct 06 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-85
- Allow nova domains to getattr on all filesystems.
- ALlow zebra for user/group look-ups.
- Allow lsmd to search own plguins.
- Allow sssd to read selinux config to add SELinux user mapping.
- Allow swift to connect to all ephemeral ports by default.
- Allow NetworkManager to create Bluetooth SDP sockets
- Allow keepalived manage snmp var lib sock files. BZ(1102228)
- Added policy for blrtty. BZ(1083162)
- Allow rhsmcertd manage rpm db. BZ(#1134173)
- Allow rhsmcertd send signull to setroubleshoot. BZ (#1134173)
- Label /usr/libexec/rhsmd as rhsmcertd_exec_t
- Fix broken interfaces
- Added sendmail_domtrans_unconfined interface
- Added support for cpuplug. BZ (#1077831)
- Fix bug in drbd policy, BZ (#1134883)
- Make keystone_cgi_script_t domain. BZ (#1138424)
- fix dev_getattr_generic_usb_dev interface
- Label 4101 tcp port as brlp port
- Allow libreswan to connect to VPN via NM-libreswan.
- Add userdom_manage_user_tmpfs_files interface

* Tue Sep 30 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-84
- Allow all domains to read fonts
- Allow rabbitmq_t read rabbitmq_var_lib_t lnk files. BZ (#1147028)
- Allow pki-tomcat to change SELinux object identity.
- Allow radious to connect to apache ports to do OCSP check
- Allow git cgi scripts to create content in /tmp
- Allow cockpit-session to do GSSAPI logins.

* Mon Sep 22 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-83
- Make sure /run/systemd/generator and system is labeled correctly on creation.
- Additional access required by usbmuxd
- Allow sensord read in /proc BZ(#1143799)

* Thu Sep 18 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-82
- Allow du running in logwatch_t read hwdata.
- Allow sys_admin capability for antivirus domians.
- Use nagios_var_lib_t instead of nagios_lib_t in nagios.fc.
- Add support for pnp4nagios.
- Add missing labeling for /var/lib/cockpit.
- Label resolv.conf as docker_share_t under docker so we can read within a container
- Remove labeling for rabbitmqctl
- setfscreate in pki.te is not capability class.
- Allow virt domains to use virtd tap FDs until we get proper handling in libvirtd.
- Allow wine domains to create cache dirs.
- Allow newaliases to systemd inhibit pipes.
- Add fixes for pki-tomcat scriptlet handling.
- Allow user domains to manage all gnome home content
- Allow locate to look at files/directories without labels, and chr_file and blk_file on non dev file systems
- Allow usbmuxd chown capabilitiesllow locate to look at files/directories without labels, and chr_file and blk_file on non dev file systems

* Thu Sep 11 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-81
- Label /usr/lib/erlang/erts.*/bin files as bin_t
- Added changes related to rabbitmq daemon.
- Fix labeling in couchdb policy
- Allow rabbitmq bind on epmd port
- Clean up rabbitmq policy
- fix domtrans_rabbitmq interface
- Added rabbitmq_beam_t and rabbitmq_epmd_t alias
- Allow couchdb to getattr
- Allow couchdb write to couchdb_conf files
- Allow couchdb to create dgram_sockets
- Added support for ejabberd

* Wed Sep 10 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-80
- Back port workaround for #1134389 from F20. It needs to be removed from rawhide once we ship F21.
- Since docker will now label volumes we can tighten the security of docker

* Wed Sep 10 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-79
- Re-arange openshift_net_read_t rules.
- Kernel is reporting random block_suspends, we should dontaudit these until the kernel is fixed in Rawhide
- Allow jockey_t to use tmpfs files
- Allow pppd to create sock_files in /var/run
- Allow geoclue to stream connect to smart card service
- Allow docker to read all of /proc
- ALlow passeneger to read/write apache stream socket.
- Dontaudit read init state for svirt_t.
- Label /usr/sbin/unbound-control as named_exec_t (#1130510)
- Add support for /var/lbi/cockpit directory.
- Add support for ~/. speech-dispatcher.
- Allow nmbd to read /proc/sys/kernel/core_pattern.
- aLlow wine domains to create wine_home symlinks.
- Allow policykit_auth_t access check and read usr config files.
- Dontaudit access check on home_root_t for policykit-auth.
- hv_vss_daemon wants to list /boot
- update gpg_agent_env_file booelan to allow manage user tmp files for gpg-agent
- Fix label for /usr/bin/courier/bin/sendmail
- Allow munin services plugins to execute fail2ban-client in fail2ban_client_t domain.
- Allow unconfined_r to access unconfined_service_t.
- Add label for ~/.local/share/fonts
- Add init_dontaudit_read_state() interface.
- Add systemd_networkd_var_run_t labeling for /var/run/systemd/netif and allow systemd-networkd to manage it.
- Allow udev_t mounton udev_var_run_t dirs #(1128618)
- Add files_dontaudit_access_check_home_dir() inteface.

* Tue Sep 02 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-78
- Allow unconfined_service_t to dbus chat with all dbus domains
- Assign rabbitmq port.  BZ#1135523
- Add new interface to allow creation of file with lib_t type
- Allow init to read all config files
- We want to remove openshift_t domains ability to look at /proc/net
- I guess lockdown is a file not a directory
- Label /var/bacula/ as bacula_store_t
- Allow rhsmcertd to seng signull to sosreport.
- Allow sending of snmp trap messages by radiusd.
- remove redundant rule fron nova.te.
- Add auth_use_nsswitch() for ctdbd.
- call nova_vncproxy_t instead of vncproxy.
- Allow nova-vncproxy to use varnishd port.
- Fix rhnsd_manage_config() to allow manage also symlinks.
- Allow bacula to create dirs/files in /tmp
- Allow nova-api to use nsswitch.
- Clean up nut policy. Allow nut domains to create temp files. Add nut_domain_template() template interface.
- Allow usbmuxd connect to itself by stream socket. (#1135945)
- I see no reason why unconfined_t should transition to crontab_t, this looks like old cruft
- Allow nswrapper_32_64.nppdf.so to be created with the proper label
- Assign rabbitmq port.  BZ#1135523
- Dontaudit leaks of file descriptors from domains that transition to  thumb_t
- Fixes for usbmuxd, addition of /var/lib/lockdown, and allow it to use urand, dontaudit sys_resource
- Allow unconfined_service_t to dbus chat with all dbus domains
- Allow avahi_t communicate with pcp_pmproxy_t over dbus.(better way)
- Allow avahi_t communicate with pcp_pmproxy_t over dbus.

* Thu Aug 28 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-77
- Allow aide to read random number generator
- Allow pppd to connect to http port. (#1128947)
- sssd needs to be able write krb5.conf.
- Labeli initial-setup as install_exec_t.
- Allow domains to are allowed to mounton proc to mount on files as well as dirs

* Tue Aug 26 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-76
- Label ~/tmp and ~/.tmp directories in user tmp dirs as user_tmp_t
- Add a port definition for shellinaboxd
- Fix labeling for HOME_DIR/tmp and HOME_DIR/.tmp directories
- Allow thumb_t to read/write video devices
- fail2ban 0.9 reads the journal by default.
- Allow sandbox net domains to bind to rawip socket

* Fri Aug 22 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-75
- Allow haproxy to read /dev/random and /dev/urandom.
- Allow mdadm to seng signull kernel_t which is proces type of mdadm on early boot.
- geoclue needs to connect to http and http_cache ports
- Allow passenger to use unix_stream_sockets leaked into it, from httpd
- Add SELinux policy for highly-available key value store for shared configuration.
- drbd executes modinfo.
- Add glance_api_can_network boolean since glance-api uses huge range port.
- Fix glance_api_can_network() definition.
- Allow smoltclient to connect on http_cache port. (#982199)
- Allow userdomains to stream connect to pcscd for smart cards
- Allow programs to use pam to search through user_tmp_t dires (/tmp/.X11-unix)
- Added MLS fixes to support labeled socket activation which is going to be done by systemd
- Add kernel_signull() interface.
- sulogin_t executes plymouth commands
- lvm needs to be able to accept connections on stream generic sockets

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 3.13.1-74
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-73
- Allow ssytemd_logind_t to list tmpfs directories
- Allow lvm_t to create undefined sockets
- Allow passwd_t to read/write stream sockets
- Allow docker lots more access.
- Fix label for ports
- Add support for arptables-{restore,save} and also labeling for /usr/lib/systemd/system/arptables.service.
- Label tcp port 4194 as kubernetes port.
- Additional access required for passenger_t
- sandbox domains should be allowed to use libraries which require execmod
- Allow qpid to read passwd files BZ (#1130086)
- Remove cockpit port, it is now going to use websm port
- Add getattr to the list of access to dontaudit on unix_stream_sockets
- Allow sendmail to append dead.letter located in var/spool/nagios/dead.letter.

* Tue Aug 12 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-72
- docker needs to be able to look at everything in /dev
- Allow all processes to send themselves signals
- Allow sysadm_t to create netlink_tcpdiag socket
- sysadm_t should be allowed to communicate with networkmanager
- These are required for bluejeans to work on a unconfined.pp disabled machine
- docker needs setfcap
- Allow svirt domains to manage chr files and blk files for mknod commands
- Allow fail2ban to read audit logs
- Allow cachefilesd_t to send itself signals
- Allow smokeping cgi script to send syslog messages
- Allow svirt sandbox domains to relabel content
- Since apache content can be placed anywhere, we should just allow apache to search through any directory
- These are required for bluejeans to work on a unconfined.pp disabled machin

* Mon Aug 4 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-71
- shell_exec_t should not be in cockip.fc

* Mon Aug 4 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-70
- Add additional fixes for  abrt-dump-journal-oops which is now labeled as abrt_dump_oops_exec_t.
- Allow denyhosts to enable synchronization which needs to connect to tcp/9911 port.
- Allow nacl_helper_boo running in :chrome_sandbox_t to send SIGCHLD to chrome_sandbox_nacl_t.
- Dontaudit write access on generic cert files. We don't audit also access check.
- Add support for arptables.
- Add labels and filenametrans rules for ostree repo directories which needs to be writable by subscription-manager.

* Mon Aug  4 2014 Tom Callaway <spot@fedoraproject.org> 3.13.1-69
- fix license handling

* Thu Jul 31 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-68
- Add new mozilla_plugin_bind_unreserved_ports boolean to allow mozilla plugin to use tcp/udp unreserved ports. There is a lot of plugins which binds ports without SELinux port type. We want to allow users to use these plugins properly using this boolean. (#1109681)
- Allow smokeping cgi scripts to accept connection on httpd stream socket.
- docker does a getattr on all file systems
- Label all abort-dump programs
- Allow alsa to create lock file to see if it fixes.
- Add support for zabbix external scripts for which zabbix_script_t domain has been created. This domain is unconfined by default and user needs to run "semodule -d unconfined" to make system running without unconfined domains. The default location of these scripts is /usr/lib/zabbix/externalscripts. If a user change DATADIR in CONFIG_EXTERNALSCRIPTS then he needs to set labeling for this new location.
- Add interface for journalctl_exec
- Add labels also for glusterd sockets.
- Change virt.te to match default docker capabilies
- Add additional booleans for turning on mknod or all caps.
- Also add interface to allow users to write policy that matches docker defaults
- for capabilies.
- Label dhcpd6 unit file.
- Add support also for dhcp IPv6 services.
- Added support for dhcrelay service
- Additional access for bluejeans
- docker needs more access, need back port to RHEL7
- Allow mdadm to connect to own socket created by mdadm running as kernel_t.
- Fix pkcs, Remove pkcs_lock_filetrans and Add files_search_locks
- Allow bacula manage bacula_log_t dirs
- Allow pkcs_slotd_t read /etc/passwd, Label /var/lock/opencryptoki as pkcs_slotd_lock_t 
- Fix mistakes keystone and quantum
- Label neutron var run dir 
- Label keystone var run dir
- Fix bad labeling for /usr/s?bin/(oo|rhc)-restorer-wrapper.sh in openshift.fc.
- Dontaudit attempts to access check cert dirs/files for sssd.
- Allow sensord to send a signal.
- Allow certmonger to stream connect to dirsrv to make  ipa-server-install working.
- Label zabbix_var_lib_t directories
- Label conmans pid file as conman_var_run_t
- Label also /var/run/glusterd.socket file as gluster_var_run_t
- Fix policy for pkcsslotd from opencryptoki
- Update cockpik policy from cockpit usptream.
- Allow certmonger to exec ldconfig to make  ipa-server-install  working. 
- Added support for Naemon policy 
- Allow keepalived manage snmp files
- Add setpgid process to mip6d
- remove duplicate rule
- Allow postfix_smtpd to stream connect to antivirus 
- Dontaudit list /tmp for icecast 
- Allow zabbix domains to access /proc//net/dev.

* Wed Jul 23 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-67
- Allow zabbix domains to access /proc//net/dev.
- Dontaudit list /tmp for icecast (#894387)
- Allow postfix_smtpd to stream connect to antivirus (#1105889)
- Add setpgid process to mip6d
- Allow keepalived manage snmp files(#1053450)
- Added support for Naemon policy (#1120789).
- Allow certmonger to exec ldconfig to make  ipa-server-install  working. (#1122110)
- Update cockpik policy from cockpit usptream.

* Mon Jul 21 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-66
- Revert labeling back to /var/run/systemd/initctl/fifo
- geoclue dbus chats with modemmanger
- Bluejeans wants to connect to port 5000
- geoclue dbus chats with modemmange

* Fri Jul 18 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-65
- Allow sysadm to dbus chat with systemd
- Add logging_dontaudit_search_audit_logs()
- Add new files_read_all_mountpoint_symlinks() 
- Fix labeling path from /var/run/systemd/initctl/fifo to /var/run/initctl/fifo.
- Allow ndc to read random and urandom device (#1110397)
- Allow zabbix to read system network state
- Allow fprintd to execute usr_t/bin_t
- Allow mailserver_domain domains to append dead.letter labeled as mail_home_t
- Add glance_use_execmem boolean to have glance configured to use Ceph/rbd
- Dontaudit search audit logs for fail2ban
- Allow mailserver_domain domains to create mail home content with right labeling
- Dontaudit svirt_sandbox_domain doing access checks on /proc
- Fix  files_pid_filetrans() calling in nut.te to reflect allow rules.
- Use nut_domain attribute for files_pid_filetrans() for nut domains.
- Allow sandbox domains read all mountpoint symlinks to make symlinked homedirs
- Fix nut domains only have type transition on dirs in /run/nut directory.
- Allow net_admin/net_raw capabilities for haproxy_t. haproxy uses setsockopt()
- Clean up osad policy. Remove additional interfaces/rules

* Mon Jul 14 2014 Lukas Vrabec <lvrabec@redhat.com> 3.13.1-64
- Allow systemd domains to check lvm status
- Allow getty to execute plymouth.#1112870
- Allow sshd to send signal to chkpwd_t
- initrctl fifo file has been renamed
- Set proper labeling on /var/run/sddm
- Fix labeling for cloud-init logs
- Allow kexec to read kallsyms
- Add rhcs_stream_connect_haproxy interface, Allow neutron stream connect to rhcs
- Add fsetid caps for mandb. #1116165
- Allow all nut domains to read  /dev/(u)?random.
- Allow deltacloudd_t to read network state BZ #1116940
- Add support for KVM virtual machines to use NUMA pre-placement
- Allow utilize winbind for authentication to AD
- Allow chrome sandbox to use udp_sockets leaked in by its parent
- Allow gfs_controld_t to getattr on all file systems
- Allow logrotate to manage virt_cache
- varnishd needs to have fsetid capability
- Allow dovecot domains to send signal perms to themselves
- Allow apache to manage pid sock files
- Allow nut_upsmon_t to create sock_file in /run dir
- Add capability sys_ptrace to stapserver
- Mysql can execute scripts when run in a cluster to see if someone is listening on a socket, basically runs lsof
- Added support for vdsm

* Fri Jul 4 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-63
- If I can create a socket I need to be able to set the attributes
- Add tcp/8775 port as neutron port
- Add additional ports for swift ports
- Added changes to fedora from bug bz#1082183
- Add support for tcp/6200 port
- Allow collectd getattr access to configfs_t dir Fixes Bug 1115040
- Update neutron_manage_lib_files() interface
- Allow glustered to connect to ephemeral ports
- Allow apache to search ipa lib files by default
- Allow neutron to domtrans to haproxy
- Add rhcs_domtrans_haproxy()
- Add support for openstack-glance-* unit files
- Add initial support for /usr/bin/glance-scrubber
- Allow swift to connect to keystone and memcache ports.
- Fix labeling for /usr/lib/systemd/system/openstack-cinder-backup
- Add policies for openstack-cinder
- Add support for /usr/bin/nova-conductor
- Add neutron_can_network boolean
- Allow neutron to connet to neutron port
- Allow glance domain to use syslog
- Add support for /usr/bin/swift-object-expirer and label it as swift_exec_t

* Wed Jun 25 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-62
- Allow swift to use tcp/6200 swift port
- ALlow swift to search apache configs
- Remove duplicate .fc entry for Grilo plugin bookmarks
- Remove duplicate .fc entry for telepathy-gabble
- Additional allow rules for docker sandbox processes
- Allow keepalived connect to agentx port
- Allow neutron-ns-metadata to connectto own unix stream socket
- Add support for tcp/6200 port
- Remove ability for confined users to run xinit
- New tool for managing wireless /usr/sbin/iw

* Fri Jun 20 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-61
- Add back MLS policy

* Thu Jun 19 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-60
- Implement new spec file handling for *.pp modules which allows us to move a policy module out of the policy

* Tue Jun 17 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-59
- Allow system_bus_types to use stream_sockets inherited from system_dbusd
- Allow journalctl to call getpw
- New access needed by dbus to talk to kernel stream
- Label sm-notifypid files correctly
- contrib: Add KMSCon policy module

* Wed Jun 11 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-58
- Add mozilla_plugin_use_bluejeans boolean
- Add additional interfaces needed by mozilla_plugin_use_bluejeans boolean

* Mon Jun 9 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-57
- Allow staff_t to communicate and run docker
- Fix *_ecryptfs_home_dirs booleans
- Allow ldconfig_t to read/write inherited user tmp pipes
- Allow storaged to dbus chat with lvm_t
- Add support for storaged  and storaged-lvm-helper. Labeled it as lvm_exec_t.
- Use proper calling in ssh.te for userdom_home_manager attribute
- Use userdom_home_manager_type() also for ssh_keygen_t
- Allow locate to list directories without labels
- Allow bitlbee to use tcp/7778 port
- /etc/cron.daily/logrotate to execute fail2ban-client.
- Allow keepalives to connect to SNMP port. Support to do  SNMP stuff
- Allow staff_t to communicate and run docker
- Dontaudit search mgrepl/.local for cobblerd_t
- Allow neutron to execute kmod in insmod_t
- Allow neutron to execute udevadm in udev_t
- Allow also fowner cap for varnishd
- Allow keepalived to execute bin_t/shell_exec_t
- rhsmcertd seems to need these accesses.  We need this backported to RHEL7 and perhaps RHEL6 policy
- Add cups_execmem boolean
- Allow gear to manage gear service
- New requires for gear to use systemctl and init var_run_t
- Allow cups to execute its rw_etc_t files, for brothers printers
- Add fixes to make munin and munin-cgi working. Allow munin-cgit to create files/dirs in /tmp, list munin conf dirs and manage munin logs.
- Allow swift to execute bin_t
- Allow swift to bind http_cache

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-55
- Add decl for cockip port
- Allow sysadm_t to read all kernel proc
- Allow logrotate to execute all executables
- Allow lircd_t to use tty_device_t for use withmythtv
- Make sure all zabbix files direcories in /var/log have the correct label
- Allow bittlebee to create directories and files in /var/log with the correct label
- Label /var/log/horizon as an apache log
- Add squid directory in /var/run
- Add transition rules to allow rabbitmq to create log files and var_lib files with the correct label
- Wronly labeled avahi_var_lib_t as a pid file
- Fix labels on rabbitmq_var_run_t on file/dir creation
- Allow neutron to create sock files
- Allow postfix domains to getattr on all file systems
- Label swift-proxy-server as swift_exec_t
- Tighten SELinux capabilities to match docker capabilities
- Add fixes for squid which is configured to run with more than one worker.
- Allow cockpit to bind to its port

* Tue May 20 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-54
- geard seems to do a lot of relabeling
- Allow system_mail_t to append to munin_var_lib_t
- Allow mozilla_plugin to read alsa_rw_ content
- Allow asterisk to connect to the apache ports
- Dontaudit attempts to read fixed disk
- Dontaudit search gconf_home_t
- Allow rsync to create  swift_server.lock with swift.log labeling
- Add labeling for swift lock files
- Use swift_virt_lock in swift.te
- Allow openwsman to getattr on sblim_sfcbd executable
- Fix sblim_stream_connect_sfcb() to contain also sblim_tmp_t
- Allow openwsman_t to read/write sblim-sfcb shared mem
- Allow openwsman to stream connec to sblim-sfcbd
- Allow openwsman to create tmpfs files/dirs
- dontaudit acces to rpm db if rpm_exec for swift_t and sblim_sfcbd_t
- Allow sblim_sfcbd to execute shell
- Allow swift to create lock file
- Allow openwsman to use tcp/80
- Allow neutron to create also dirs in /tmp
- Allow seunshare domains to getattr on all executables
- Allow ssh-keygen to create temporary files/dirs needed by OpenStack
- Allow named_filetrans_domain to create /run/netns
- Allow ifconfig to create /run/netns

* Tue May 13 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-53
- Add missing dyntransition for sandbox_x_domain

* Wed May 7 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-52
- More rules for gears and openshift
- Added iotop policy. Thanks William Brown
- Allow spamc to read .pyzor located in /var/spool/spampd
- Allow spamc to create home content with correct labeling
- Allow logwatch_mail_t to create dead.letter with correct labelign
- Add labeling for min-cloud-agent
- Allow geoclue to read unix in proc.
- Add support for /usr/local/Brother labeling. We removed /usr/local equiv.
- add support for min-cloud-agent
- Allow ulogd to request the kernel to load a module
- remove unconfined_domain for openwsman_t
- Add openwsman_tmp_t rules
- Allow openwsman to execute chkpwd and make this domain as unconfined for F20.
- Allow nova-scheduler to read passwd file
- Allow neutron execute arping in neutron_t
- Dontaudit logrotate executing systemctl command attempting to net_admin
- Allow mozilla plugins to use /dev/sr0
- svirt sandbox domains to read gear content in /run. Allow gear_t to manage openshift files
- Any app that executes systemctl will attempt a net_admin
- Fix path to mmap_min_addr

* Wed May 7 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-51
- Add gear fixes from dwalsh

* Tue May 6 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-50
- selinux_unconfined_type should not be able to set booleans if the securemode is set
- Update sandbox_transition() to call sandbox_dyntrasition(). #885288.

* Mon May 5 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-49
- Fix labeling for /root/\.yubico
- userdom_search_admin_dir() calling needs to be optional in kernel.te
- Dontaudit leaked xserver_misc_device_t into plugins
- Allow all domains to search through all base_file_types, this should be back ported to RHEL7 policy
- Need to allow sssd_t to manage kernel keyrings in login programs since they don't get labeled with user domains
- Bootloader wants to look at init state
- Add MCS/MLS Constraints to kernel keyring, also add MCS Constraints to ipc, sem.msgq, shm
- init reads kdbump etc files
- Add support for tcp/9697
- Fix labeling for /var/run/user/<UID>/gvfs
- Add support for us_cli ports
- fix sysnet_use_ldap
- Allow mysql to execute ifconfig if Red Hat OpenStack
- ALlow stap-server to get attr on all fs
- Fix mail_pool_t to mail_spool_t
- Dontaudit leaked xserver_misc_device_t into plugins
- Need to allow sssd_t to manage kernel keyrings in login programs since they don't get labeled with user domains
- Add new labeling for /var/spool/smtpd
- Allow httpd_t to kill passenger
- Allow apache cgi scripts to use inherited httpd_t unix_stream_sockets
- Allow nova-scheduler to read passwd/utmp files
- Additional rules required by openstack,  needs backport to F20 and RHEL7
- Additional access required by docker
- ALlow motion to use tcp/8082 port

* Fri Apr 25 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-48
- Fix virt_use_samba boolean
- Looks like all domains that use dbus libraries are now reading /dev/urand
- Add glance_use_fusefs() boolean
- Allow tgtd to read /proc/net/psched
- Additional access required for gear management of openshift directories
- Allow sys_ptrace for mock-build
- Fix mock_read_lib_files() interface
- Allow mock-build to write all inherited ttys and ptys
- Allow spamd to create razor home dirs with correct labeling
- Clean up sysnet_use_ldap()
- systemd calling needs to be optional
- Allow init_t to setattr/relabelfrom dhcp state files

* Wed Apr 23 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-47
- mongod should not be a part of cloudforms.pp
- Fix labeling in snapper.fc
- Allow docker to read unconfined_t process state
- geoclue dbus chats with NetworkManager
- Add cockpit policy
- Add interface to allow tools to check the processes state of bind/named
- Allow myslqd to use the tram port for Galera/MariaDB

* Fri Apr 18 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-46
- Allow init_t to setattr/relabelfrom dhcp state files
- Allow dmesg to read hwdata and memory dev
- Allow strongswan to create ipsec.secrets with correct labeling in /etc/strongswan
- Dontaudit antivirus domains read access on all security files by default
- Add missing alias for old amavis_etc_t type
- Additional fixes for  instack overcloud
- Allow block_suspend cap for haproxy
- Allow OpenStack to read mysqld_db links and connect to MySQL
- Remove dup filename rules in gnome.te
- Allow sys_chroot cap for httpd_t and setattr on httpd_log_t
- Add labeling for /lib/systemd/system/thttpd.service
- Allow iscsid to handle own unit files
- Add iscsi_systemctl()
- Allow mongod also create sock_file with correct labeling in /run
- Allow aiccu stream connect to pcscd
- Allow rabbitmq_beam to connect to httpd port
- Allow httpd to send signull to apache script domains and don't audit leaks
- Fix labeling in drbd.fc
- Allow sssd to connect to the smbd port for handing logins using active directory, needs back port for rhel7
- Allow all freeipmi domains to read/write ipmi devices
- Allow rabbitmq_epmd to manage rabbit_var_log_t files
- Allow sblim_sfcbd to use also pegasus-https port
- Allow chronyd to read /sys/class/hwmon/hwmon1/device/temp2_input
- Add httpd_run_preupgrade boolean
- Add interfaces to access preupgrade_data_t
- Add preupgrade policy
- Add labeling for puppet helper scripts

* Tue Apr 8 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-45
Rename puppet_t to puppetagent_t and used it only for puppet agent which can be started by init. Also make it as unconfined_noaudit because there is no reason to confine it but we wantto avoid init_t.

* Tue Apr 8 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-44
- Change hsperfdata_root to have as user_tmp_t
- Allow rsyslog low-level network access
- Fix use_nfs_home_dirs/use_samba_home_dirs for xdm_t to allow append .xsession-errors by lightdm
- Allow conman to resolve DNS and use user ptys
- update pegasus_openlmi_admin_t policy
- nslcd wants chown capability
- Dontaudit exec insmod in boinc policy

* Fri Apr 4 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-43
- Add labels for /var/named/chroot_sdb/dev devices
- Add support for strongimcv
- Add additional fixes for yubikeys based on william@firstyear.id.au
- Allow init_t run /sbin/augenrules
- Remove dup decl for dev_unmount_sysfs_fs
- Allow unpriv SELinux user to use sandbox
- Fix ntp_filetrans_named_content for sntp-kod file
- Add httpd_dbus_sssd boolean
- Dontaudit exec insmod in boinc policy
- Add dbus_filetrans_named_content_system()
- We want to label only /usr/bin/start-puppet-master to avoid puppet agent running in puppet_t
- varnishd wants chown capability
- update ntp_filetrans_named_content() interface
- Add additional fixes for neutron_t. #1083335
- Dontaudit sandbox_t getattr on proc_kcore_t
- Allow pki_tomcat_t to read ipa lib files

* Tue Apr 1 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-42
- Merge user_tmp_t and user_tmpfs_t together to have only user_tmp_t

* Thu Mar 27 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-41
- Turn on gear_port_t
- Add gear policy and remove permissive domains.
- Add labels for ostree
- Add SELinux awareness for NM
- Label /usr/sbin/pwhistory_helper as updpwd_exec_t

* Wed Mar 26 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-40
- update storage_filetrans_all_named_dev for sg* devices
- Allow auditctl_t  to getattr on all removeable devices
- Allow nsswitch_domains to stream connect to nmbd
- Allow rasdaemon to rw /dev/cpu//msr
- fix /var/log/pki file spec
- make bacula_t as auth_nsswitch domain
- Allow certmonger to manage ipa lib files
- Add support for /var/lib/ipa

* Tue Mar 25 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-39
- Manage_service_perms should include enable and disable, need backport to RHEL7
- Allow also unpriv user to run vmtools
- Allow secadm to read /dev/urandom and meminfo
- Add userdom_tmp_role for secadm_t
- Allow postgresql to read network state
- Add a new file context for /var/named/chroot/run directory
- Add booleans to allow docker processes to use nfs and samba
- Dontaudit net_amdin for /usr/lib/jvm/java-1.7.0-openjdk-1.7.0.51-2.4.5.1.el7.x86_64/jre-abrt/bin/java running as pki_tomcat_t
- Allow puppet stream connect to mysql
- Fixed some rules related to puppet policy
- Allow vmware-user-sui to use user ttys
- Allow talk 2 users logged via console too
- Additional avcs for docker when running tests
- allow anaconda to dbus chat with systemd-localed
- clean up rhcs.te
- remove dup rules from haproxy.te
- Add fixes for haproxy based on bperkins@redhat.com
- Allow cmirrord to make dmsetup working
- Allow NM to execute arping
- Allow users to send messages through talk
- update rtas_errd policy
- Add support for /var/spool/rhsm/debug
- Make virt_sandbox_use_audit as True by default
- Allow svirt_sandbox_domains to ptrace themselves
- Allow snmpd to getattr on removeable and fixed disks
- Allow docker containers to manage /var/lib/docker content

* Mon Mar 17 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-38
- Label sddm as xdm_exec_t to make KDE working again
- Allow postgresql to read network state
- Allow java running as pki_tomcat to read network sysctls
- Fix cgroup.te to allow cgred to read cgconfig_etc_t
- Allow beam.smp to use ephemeral ports
- Allow winbind to use the nis to authenticate passwords

* Mon Mar 17 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-37
- Allow collectd to talk to libvirt
- Allow chrome_sandbox to use leaked unix_stream_sockets
- Dontaudit leaks of sockets into chrome_sandbox_t
- If you create a cups directory in /var/cache then it should be labeled cups_rw_etc_t
- Run vmtools as unconfined domains
- Allow snort to manage its log files
- Allow systemd_cronjob_t to be entered via bin_t
- Allow procman to list doveconf_etc_t
- allow keyring daemon to create content in tmpfs directories
- Add proper labelling for icedtea-web
- vpnc is creating content in networkmanager var run directory
- unconfined_service should be allowed to transition to rpm_script_t
- Allow couchdb to listen on port 6984
- Dontaudit attempts by unpriv user domain to write to /run/mount directory, caused by running mount command
- Allow systemd-logind to setup user tmpfs directories
- Add additional fixes for systemd_networkd_t
- Allow systemd-logind to manage user_tmpfs_t
- Allow systemd-logind to mount /run/user/1000 to get gdm working

* Fri Mar 14 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-36
- Add additional fixes for systemd_networkd_t
- Allow systemd-logind to manage user_tmpfs_t
- Allow systemd-logind to mount /run/user/1000 to get gdm working
- Dontaudit attempts to setsched on the kernel_t threads
- Allow munin mail plugins to read network systcl
- Fix git_system_enable_homedirs boolean
- Make cimtest script 03_defineVS.py of ComputerSystem group working
- Make  abrt-java-connector working
- Allow net_admin cap for fence_virtd running as fenced_t
- Allow vmtools_helper_t to execute bin_t
- Add support for /usr/share/joomla

* Thu Mar 13 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-35
- sshd to read network sysctls
- Allow vmtools_helper_t to execute bin_t
- Add support for /usr/share/joomla
- /var/lib/containers should be labeled as openshift content for now
- Allow docker domains to talk to the login programs, to allow a process to login into the container

* Wed Mar 12 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-34
- Add install_t for anaconda

* Wed Mar 12 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-33
- Allow init_t to stream connect to ipsec
- Add /usr/lib/systemd/systemd-networkd policy
- Add sysnet_manage_config_dirs()
- Add support for /var/run/systemd/network and labeled it as net_conf_t
- Allow unpriv SELinux users to dbus chat with firewalld
- Add lvm_write_metadata()
- Label /etc/yum.reposd dir as system_conf_t. Should be safe because system_conf_t is base_ro_file_type
- Add support for /dev/vmcp and /dev/sclp
- Add docker_connect_any boolean
- Fix zabbix policy
- Allow zabbix to send system log msgs
- Allow pegasus_openlmi_storage_t to write lvm metadata
- Updated pcp_bind_all_unreserved_ports
- Allow numad to write scan_sleep_millisecs
- Turn on entropyd_use_audio boolean by default
- Allow cgred to read /etc/cgconfig.conf because it contains templates used together with rules from /etc/cgrules.conf.
- Allow lscpu running as rhsmcertd_t to read /proc/sysinfo

* Mon Mar 10 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-32
- Allow numad to write scan_sleep_millisecs
- Turn on entropyd_use_audio boolean by default
- Allow cgred to read /etc/cgconfig.conf because it contains templates used together with rules from /etc/cgrules.conf.
- Allow lscpu running as rhsmcertd_t to read /proc/sysinfo
- Allow numad to write scan_sleep_millisecs
- Turn on entropyd_use_audio boolean by default
- Allow cgred to read /etc/cgconfig.conf because it contains templates used together with rules from /etc/cgrules.conf.
- Allow lscpu running as rhsmcertd_t to read /proc/sysinfo
- Fix label on irclogs in the homedir

* Fri Mar 7 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-31
- Modify xdm_write_home to allow create files/links in /root with xdm_home_t
- Add more fixes for https://fedoraproject.org/wiki/Changes/XorgWithoutRootRights
- Add xserver_dbus_chat() interface
- Add sysnet_filetrans_named_content_ifconfig() interface
- Change userdom_use_user_inherited_ttys to userdom_use_user_ttys for systemd-tty-ask
- Turn on cron_userdomain_transition by default for now. Until we get a fix for #1063503
- Allow lscpu running as rhsmcertd_t to read sysinfo
- Allow virt domains to read network state
- Added pcp rules
- Allow ctdbd to connect own ports
- Fix samba_export_all_rw booleanto cover also non security dirs
- Allow swift to exec rpm in swift_t and allow to create tmp files/dirs
- Allow neutron to create /run/netns with correct labeling
- Allow to run ip cmd in neutron_t domain
- Allow rpm_script_t to dbus chat also with systemd-located
- Fix ipa_stream_connect_otpd()

* Tue Mar 4 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-30
- Allow block_suspend cap2 for systemd-logind and rw dri device
- Add labeling for /usr/libexec/nm-libreswan-service
- Allow locallogin to rw xdm key to make Virtual Terminal login providing smartcard pin working
- Add xserver_rw_xdm_keys()
- Allow rpm_script_t to dbus chat also with systemd-located
- Fix ipa_stream_connect_otpd()
- update lpd_manage_spool() interface
- Allow krb5kdc to stream connect to ipa-otpd
- Add ipa_stream_connect_otpd() interface
- Allow vpnc to unlink NM pids
- Add networkmanager_delete_pid_files()
- Allow munin plugins to access unconfined plugins
- update abrt_filetrans_named_content to cover /var/spool/debug
- Label /var/spool/debug as abrt_var_cache_t
- Allow rhsmcertd to connect to squid port
- Make docker_transition_unconfined as optional boolean
- Allow certmonger to list home dirs

* Fri Feb 28 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-29
- Make docker as permissive domain

* Thu Feb 27 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-28
- Allow bumblebeed to send signal to insmod
- Dontaudit attempts by crond_t net_admin caused by journald
- Allow the docker daemon to mounton tty_device_t
- Add addtional snapper fixes to allo relabel file_t
- Allow setattr for all mountpoints
- Allow snapperd to write all dirs
- Add support for /etc/sysconfig/snapper
- Allow mozilla_plugin to getsession
- Add labeling for thttpd
- Allow sosreport to execute grub2-probe
- Allow NM to manage hostname config file
- Allow systemd_timedated_t to dbus chat with rpm_script_t
- Allow lsmd plugins to connect to http/ssh/http_cache ports by default
- Add lsmd_plugin_connect_any boolea
- Add support for ipset
- Add support for /dev/sclp_line0
- Add modutils_signal_insmod()
- Add files_relabelto_all_mountpoints() interface
- Allow the docker daemon to mounton tty_device_t
- Allow all systemd domains to read /proc/1
- Login programs talking to journald are attempting to net_admin, add dontaudit
- init is not gettar on processes as shutdown time
- Add systemd_hostnamed_manage_config() interface
- Make unconfined_service_t valid in enforcing
- Remove transition for temp dirs created by init_t
- gdm-simple-slave uses use setsockopt
- Add lvm_read_metadata()

* Mon Feb 24 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-27
- Make unconfined_service_t valid in enforcing
- Remove transition for temp dirs created by init_t
- gdm-simple-slave uses use setsockopt
- Treat usermodehelper_t as a sysctl_type
- xdm communicates with geo
- Add lvm_read_metadata()
- Allow rabbitmq_beam to connect to jabber_interserver_port
- Allow logwatch_mail_t to transition to qmail_inject and queueu
- Added new rules to pcp policy
- Allow vmtools_helper_t to change role to system_r
- Allow NM to dbus chat with vmtools

* Fri Feb 21 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-26
- Add labeling for /usr/sbin/amavi
- Colin asked for this program to be treated as cloud-init
- Allow ftp services to manage xferlog_t
- Fix vmtools policy to allow user roles to access vmtools_helper_t
- Allow block_suspend cap2 for ipa-otpd
- Allow certmonger to search home content
- Allow pkcsslotd to read users state
- Allow exim to use pam stack to check passwords
- Add labeling for /usr/sbin/amavi
- Colin asked for this program to be treated as cloud-init
- Allow ftp services to manage xferlog_t
- Fix vmtools policy to allow user roles to access vmtools_helper_t
- Allow block_suspend cap2 for ipa-otpd
- Allow certmonger to search home content
- Allow pkcsslotd to read users state
- Allow exim to use pam stack to check passwords

* Tue Feb 18 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-25
- Add lvm_read_metadata()
- Allow auditadm to search /var/log/audit dir
- Add lvm_read_metadata() interface
- Allow confined users to run vmtools helpers
- Fix userdom_common_user_template()
- Generic systemd unit scripts do write check on /
- Allow init_t to create init_tmp_t in /tmp.This is for temporary content created by generic unit files
- Add additional fixes needed for init_t and setup script running in generic unit files
- Allow general users to create packet_sockets
- added connlcli port
- Add init_manage_transient_unit() interface
- Allow init_t (generic unit files) to manage rpc state date as we had it for initrc_t
- Fix userdomain.te to require passwd class
- devicekit_power sends out a signal to all processes on the message bus when power is going down
- Dontaudit rendom domains listing /proc and hittping system_map_t
- Dontauit leaks of var_t into ifconfig_t
- Allow domains that transition to ssh_t to manipulate its keyring
- Define oracleasm_t as a device node
- Change to handle /root as a symbolic link for os-tree
- Allow sysadm_t to create packet_socket, also move some rules to attributes
- Add label for openvswitch port
- Remove general transition for files/dirs created in /etc/mail which got etc_aliases_t label.
- Allow postfix_local to read .forward in pcp lib files
- Allow pegasus_openlmi_storage_t to read lvm metadata
- Add additional fixes for pegasus_openlmi_storage_t
- Allow bumblebee to manage debugfs
- Make bumblebee as unconfined domain
- Allow snmp to read etc_aliases_t
- Allow lscpu running in pegasus_openlmi_storage_t to read /dev/mem
- Allow pegasus_openlmi_storage_t to read /proc/1/environ
- Dontaudit read gconf files for cupsd_config_t
- make vmtools as unconfined domain
- Add vmtools_helper_t for helper scripts. Allow vmtools shutdonw a host and run ifconfig.
- Allow collectd_t to use a mysql database
- Allow ipa-otpd to perform DNS name resolution
- Added new policy for keepalived
- Allow openlmi-service provider to manage transitient units and allow stream connect to sssd
- Add additional fixes new pscs-lite+polkit support
- Add labeling for /run/krb5kdc
- Change w3c_validator_tmp_t to httpd_w3c_validator_tmp_t in F20
- Allow pcscd to read users proc info
- Dontaudit smbd_t sending out random signuls
- Add boolean to allow openshift domains to use nfs
- Allow w3c_validator to create content in /tmp
- zabbix_agent uses nsswitch
- Allow procmail and dovecot to work together to deliver mail
- Allow spamd to execute files in homedir if boolean turned on
- Allow openvswitch to listen on port 6634
- Add net_admin capability in collectd policy
- Fixed snapperd policy
- Fixed bugsfor pcp policy
- Allow dbus_system_domains to be started by init
- Fixed some interfaces
- Add kerberos_keytab_domain attribute
- Fix snapperd_conf_t def

* Fri Feb 14 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-24
- Dontaudit rendom domains listing /proc and hittping system_map_t
- devicekit_power sends out a signal to all processes on the message bus when power is going down
- Modify xdm_write_home to allow create also links as xdm_home_t if the boolean is on true
- systemd_tmpfiles_t needs to _setcheckreqprot
- Add unconfined_server to be run by init_t when it executes files labeled bin_t, or usr_t, allow all domains to communicate with it
- Fixed snapperd policy
- Fixed broken interfaces
- Should use rw_socket_perms rather then sock_file on a unix_stream_socket
- Fixed bugsfor pcp policy
- pcscd seems to be using policy kit and looking at domains proc data that transition to it
- Allow dbus_system_domains to be started by init
- Fixed some interfaces
- Addopt corenet rules for unbound-anchor to rpm_script_t
- Allow runuser to send send audit messages.
- Allow postfix-local to search .forward in munin lib dirs
- Allow udisks to connect to D-Bus
- Allow spamd to connect to spamd port
- Fix syntax error in snapper.te
- Dontaudit osad to search gconf home files
- Allow rhsmcertd to manage /etc/sysconf/rhn director
- Fix pcp labeling to accept /usr/bin for all daemon binaries
- Fix mcelog_read_log() interface
- Allow iscsid to manage iscsi lib files
- Allow snapper domtrans to lvm_t. Add support for /etc/snapper and allow snapperd to manage it.
- Allow ABRT to read puppet certs
- Allow virtd_lxc_t to specify the label of a socket
- New version of docker requires more access

* Mon Feb 10 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-23
- Addopt corenet rules for unbound-anchor to rpm_script_t
- Allow runuser to send send audit messages.
- Allow postfix-local to search .forward in munin lib dirs
- Allow udisks to connect to D-Bus
- Allow spamd to connect to spamd port
- Fix syntax error in snapper.te
- Dontaudit osad to search gconf home files
- Allow rhsmcertd to manage /etc/sysconf/rhn director
- Fix pcp labeling to accept /usr/bin for all daemon binaries
- Fix mcelog_read_log() interface
- Allow iscsid to manage iscsi lib files
- Allow snapper domtrans to lvm_t. Add support for /etc/snapper and allow snapperd to manage it.
- Make tuned_t as unconfined domain for RHEL7.0
- Allow ABRT to read puppet certs
- Add sys_time capability for virt-ga
- Allow gemu-ga to domtrans to hwclock_t
- Allow additional access for virt_qemu_ga_t processes to read system clock and send audit messages
- Fix some AVCs in pcp policy
- Add to bacula capability setgid and setuid and allow to bind to bacula ports
- Changed label from rhnsd_rw_conf_t to rhnsd_conf_t
- Add access rhnsd and osad to /etc/sysconfig/rhn
- drbdadm executes drbdmeta
- Fixes needed for docker
- Allow epmd to manage /var/log/rabbitmq/startup_err file
- Allow beam.smp connect to amqp port
- Modify xdm_write_home to allow create also links as xdm_home_t if the boolean is on true
- Allow init_t to manage pluto.ctl because of init_t instead of initrc_t
- Allow systemd_tmpfiles_t to manage all non security files on the system
- Added labels for bacula ports
- Fix label on /dev/vfio/vfio
- Add kernel_mounton_messages() interface
- init wants to manage lock files for iscsi

* Wed Feb 5 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-22
- Fix /dev/vfio/vfio labeling

* Wed Feb 5 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-21
- Add kernel_mounton_messages() interface
- init wants to manage lock files for iscsi
- Add support for dey_sapi port
- Fixes needed for docker
- Allow epmd to manage /var/log/rabbitmq/startup_err file
- Allow beam.smp connect to amqp port
- drbdadm executes drbdmeta
- Added osad policy
- Allow postfix to deliver to procmail
- Allow vmtools to execute /usr/bin/lsb_release
- Allow geoclue to read /etc/passwd
- Allow docker to write system net ctrls
- Add support for rhnsd unit file
- Add dbus_chat_session_bus() interface
- Add dbus_stream_connect_session_bus() interface
- Fix pcp.te
- Fix logrotate_use_nfs boolean
- Add lot of pcp fixes found in RHEL7
- fix labeling for pmie for pcp pkg
- Change thumb_t to be allowed to chat/connect with session bus type
- Add logrotate_use_nfs boolean
- Allow setroubleshootd to read rpc sysctl

* Thu Jan 30 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-20
- Allow passwd_t to use ipc_lock, so that it can change the password in gnome-keyring
- Allow geoclue to create temporary files/dirs in /tmp
- Add httpd_dontaudit_search_dirs boolean
- Add support for winbind.service
- ALlow also fail2ban-client to read apache logs
- Allow vmtools to getattr on all fs

* Tue Jan 28 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-19
- Add net_admin also for systemd_passwd_agent_t
- Allow Associate usermodehelper_t to sysfs filesystem
- Allow gdm to create /var/gdm with correct labeling
- Allow domains to append rkhunterl lib files. #1057982
- Allow systemd_tmpfiles_t net_admin to communicate with journald
- update libs_filetrans_named_content() to have support for /usr/lib/debug directory
- Adding a new service script to enable setcheckreqprot
- Add interface to getattr on an isid_type for any type of file
- Allow initrc_t domtrans to authconfig if unconfined is enabled
- Add labeling for snapper.log
- Allow tumbler to execute dbusd-daemon in thumb_t
- Add dbus_exec_dbusd()
- Add snapperd_data_t type
- Add additional fixes for snapperd
- FIx bad calling in samba.te
- Allow smbd to create tmpfs
- Allow rhsmcertd-worker send signull to rpm process
- Allow net_admin capability and send system log msgs
- Allow lldpad send dgram to NM
- Add networkmanager_dgram_send()
- rkhunter_var_lib_t is correct type
- Allow openlmi-storage to read removable devices
- Allow system cron jobs to manage rkhunter lib files
- Add rkhunter_manage_lib_files()
- Fix ftpd_use_fusefs boolean to allow manage also symlinks
- Allow smbcontrob block_suspend cap2
- Allow slpd to read network and system state info
- Allow NM domtrans to iscsid_t if iscsiadm is executed
- Allow slapd to send a signal itself
- Allow sslget running as pki_ra_t to contact port 8443, the secure port of the CA.
- Fix plymouthd_create_log() interface
- Add rkhunter policy with files type definition for /var/lib/rkhunter until it is fixed in rkhunter package
- Allow postfix and cyrus-imapd to work out of box
- Remove logwatch_can_sendmail which is no longer used
- Allow fcoemon to talk with unpriv user domain using unix_stream_socket
- snapperd is D-Bus service
- Allow OpenLMI PowerManagement to call 'systemctl --force reboot'

* Fri Jan 24 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-18
- Add haproxy_connect_any boolean
- Allow haproxy also to use http cache port by default
- Fix /usr/lib/firefox/plugin-container decl
- Allow haproxy to work as simple HTTP proxy. HAProxy For TCP And HTTP Based Applications
- Label also /usr/libexec/WebKitPluginProcess as mozilla_plugin_exec_t
- Fix type in docker.te
- Fix bs_filetrans_named_content() to have support for /usr/lib/debug directory
- Adding a new service script to enable setcheckreqprot
- Add interface to getattr on an isid_type for any type of file
- Allow initrc_t domtrans to authconfig if unconfined is enabled
type in docker.te
- Add mozilla_plugin_exec_t labeling for /usr/lib/firefox/plugin-container

* Thu Jan 23 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-17
- init calling needs to be optional in domain.te
- Allow docker and mount on devpts chr_file
- Allow docker to transition to unconfined_t if boolean set
- Label also /usr/libexec/WebKitPluginProcess as mozilla_plugin_exec_t
- Fix type in docker.te
- Add mozilla_plugin_exec_t labeling for /usr/lib/firefox/plugin-container
- Allow docker to use the network and build images
- Allow docker to read selinux files for labeling, and mount on devpts chr_file
- Allow domains that transition to svirt_sandbox to send it signals
- Allow docker to transition to unconfined_t if boolean set

* Wed Jan 22 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-16
- New access needed to allow docker + lxc +SELinux to work together
- Allow apache to write to the owncloud data directory in /var/www/html...
- Cleanup sandbox X AVC's
- Allow consolekit to create log dir
- Add support for icinga CGI scripts
- Add support for icinga
- Allow kdumpctl_t to create kdump lock file
- Allow kdump to create lnk lock file
- Allow ABRT write core_pattern
- Allwo ABRT to read core_pattern
- Add policy for Geoclue. Geoclue is a D-Bus service that provides location information
- Allow nscd_t block_suspen capability
- Allow unconfined domain types to manage own transient unit file
- Allow systemd domains to handle transient init unit files
- No longer need the rpm_script_roles line since rpm_transition_script now does this for us
- Add/fix interfaces for usermodehelper_t
- Add interfaces to handle transient
- Fixes for new usermodehelper and proc_securit_t types, added to increase security on /proc and /sys file systems

* Mon Jan 20 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-15
- Add cron unconfined role support for uncofined SELinux user
- Call kernel_rw_usermodehelper_state() in init.te
- Call corenet_udp_bind_all_ports() in milter.te
- Allow fence_virtd to connect to zented port
- Fix header for mirrormanager_admin()
- Allow dkim-milter to bind udp ports
- Allow milter domains to send signull itself
- Allow block_suspend for yum running as mock_t
- Allow beam.smp to manage couchdb files
- Add couchdb_manage_files()
- Add labeling for /var/log/php_errors.log
- Allow bumblebee to stream connect to xserver
- Allow bumblebee to send a signal to xserver
- gnome-thumbnail to stream connect to bumblebee
- Fix calling usermodehelper to use _state in interface name
- Allow xkbcomp running as bumblebee_t to execute  bin_t
- Allow logrotate to read squid.conf
- Additional rules to get docker and lxc to play well with SELinux
- Call kernel_read_usermodhelper/kernel_rw_usermodhelper
- Make rpm_transition_script accept a role
- Added new policy for pcp
- Allow bumbleed to connect to xserver port
- Allow pegasus_openlmi_storage_t to read hwdata

* Fri Jan 17 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-14
- Make rpm_transition_script accept a role
- Clean up pcp.te
- Added new policy for pcp
- Allow bumbleed to connect to xserver port
- Added support for named-sdb in bind policy
- Allow NetworkManager to signal and sigkill init scripts
- Allow pegasus_openlmi_storage_t to read hwdata
- Fix rhcs_rw_cluster_tmpfs()
- Allow fenced_t to bind on zented udp port
- Fix mirrormanager_read_lib_files()
- Allow mirromanager scripts running as httpd_t to manage mirrormanager pid files
- Dontaudit read/write to init stream socket for lsmd_plugin_t
- Allow automount to read nfs link files
- Allow lsm plugins to read/write lsmd stream socket
- Allow svirt_lxc domains to umount dockersocket filesytem
- Allow gnome keyring domains to create gnome config dirs
- Allow rpm scritplets to create /run/gather with correct labeling
- Add sblim_filetrans_named_content() interface
- Allow ctdb to create sock files in /var/run/ctdb
- Add also labeling for /var/run/ctdb
- Add missing labeling for /var/lib/ctdb
- ALlow tuned to manage syslog.conf. Should be fixed in tuned. #1030446
- Dontaudit hypervkvp to search homedirs
- Dontaudit hypervkvp to search admin homedirs
- Allow hypervkvp to execute bin_t and ifconfig in the caller domain
- Dontaudit xguest_t to read ABRT conf files
- Add abrt_dontaudit_read_config()
- Allow namespace-init to getattr on fs
- Add thumb_role() also for xguest
- Add filename transitions to create .spamassassin with correct labeling
- Allow apache domain to read mirrormanager pid files
- Allow domains to read/write shm and sem owned by mozilla_plugin_t
- Allow alsactl to send a generic signal to kernel_t
- Allow plymouthd to read run/udev/queue.bin
- Allow sys_chroot for NM required by iodine service
- Change glusterd to allow mounton all non security
- Labeled ~/.nv/GLCache as being gstreamer output
- Restrict the ability to set usermodehelpers and proc security settings.
- Limit the ability to write to the files that configure kernel i
- usermodehelpers and security-sensitive proc settings to the init domain. i
- Permissive domains can also continue to set these values.
- The current list is not exhaustive, just an initial set.
- Not all of these files will exist on all kernels/devices.
- Controlling access to certain kernel usermodehelpers, e.g. cgroup
- release_agent, will require kernel changes to support and cannot be
- addressed here.
- Ideas come from Stephen Smalley and seandroid
- Make rpm_transition_script accept a role
- Make rpm_transition_script accept a role
- Allow NetworkManager to signal and sigkill init scripts
- Allow init_t to work on transitient and snapshot unit files
- Add logging_manage_syslog_config()
- Update sysnet_dns_name_resolve() to allow connect to dnssec port

* Mon Jan 13 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-13
- Remove file_t from the system and realias it with unlabeled_t

* Thu Jan 9 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-12
- Add gluster fixes
- Remove ability to transition to unconfined_t from confined domains
- Additional allow rules to get libvirt-lxc containers working with docker

* Mon Jan 6 2014 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-11
- passwd to create gnome-keyring passwd socket
- systemd_systemctl needs sys_admin capability
- Allow cobbler to search dhcp_etc_t directory
- Allow sytemd_tmpfiles_t to delete all directories
- allow sshd to write to all process levels in order to change passwd when running at a level
- Allow updpwd_t to downgrade /etc/passwd file to s0, if it is not running with this range
- Allow apcuspd_t to status and start the power unit file
- Allow udev to manage kdump unit file
- Added new interface modutils_dontaudit_exec_insmod
- Add labeling for /var/lib/servicelog/servicelog.db-journal
- Allow init_t to create tmpfs_t lnk_file
- Add label for ~/.cvsignore
- Allow fprintd_t to send syslog messages
- Add  zabbix_var_lib_t for /var/lib/zabbixsrv, also allow zabix to connect to smtp port
- Allow mozilla plugin to chat with policykit, needed for spice
- Allow gssprozy to change user and gid, as well as read user keyrings
- Allow sandbox apps to attempt to set and get capabilties
- Label upgrades directory under /var/www as httpd_sys_rw_content_t, add other filetrans rules to label content correctly
- allow modemmanger to read /dev/urand
- Allow polipo to connect to http_cache_ports
- Allow cron jobs to manage apache var lib content
- Allow yppassword to manage the passwd_file_t
- Allow showall_t to send itself signals
- Allow cobbler to restart dhcpc, dnsmasq and bind services
- Allow rsync_t to manage all non auth files
- Allow certmonger to manage home cert files
- Allow user_mail_domains to write certain files to the /root and ~/ directories
- Allow apcuspd_t to status and start the power unit file
- Allow cgroupdrulesengd to create content in cgoups directories
- Add new access for mythtv
- Allow irc_t to execute shell and bin-t files:
- Allow smbd_t to signull cluster
- Allow sssd to read systemd_login_var_run_t
- Allow gluster daemon to create fifo files in glusterd_brick_t and sock_file in glusterd_var_lib_t
- Add label for /var/spool/cron.aquota.user
- Allow sandbox_x domains to use work with the mozilla plugin semaphore
- Added new policy for speech-dispatcher
- Added dontaudit rule for insmod_exec_t  in rasdaemon policy
- Updated rasdaemon policy
- Allow virt_domains to read cert files
- Allow system_mail_t to transition to postfix_postdrop_t
- Clean up mirrormanager policy
- Allow subscription-manager running as sosreport_t to manage rhsmcertd
- Remove ability to do mount/sys_admin by default in virt_sandbox domains
- New rules required to run docker images within libivrt
- Fixed bumblebee_admin() and mip6d_admin()
- Add log support for sensord
- Add label for ~/.cvsignore
- Change mirrormanager to be run by cron
- Add mirrormanager policy
- Additional fixes for docker.te
- Allow cobblerd to read/write undionly.kpxe located in /var/lib/tftpboot
- Add tftp_write_rw_content/tftp_read_rw_content interfaces
- Allow amanda to do backups over UDP

* Fri Dec 13 2013 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-10
- Allow freeipmi_ipmidetectd_t to use freeipmi port
- Update freeipmi_domain_template()
- Allow journalctl running as ABRT to read /run/log/journal
- Allow NM to read dispatcher.d directory
- Update freeipmi policy
- Type transitions with a filename not allowed inside conditionals
- Allow tor to bind to hplip port
- Make new type to texlive files in homedir
- Allow zabbix_agent to transition to dmidecode
- Add rules for docker
- Allow sosreport to send signull to unconfined_t
- Add virt_noatsecure and virt_rlimitinh interfaces
- Fix labeling in thumb.fc to add support for /usr/lib64/tumbler-1/tumblerddd support for freeipmi port
- Add sysadm_u_default_contexts
- Add logging_read_syslog_pid()
- Fix userdom_manage_home_texlive() interface
- Make new type to texlive files in homedir
- Add filename transitions for /run and /lock links
- Allow virtd to inherit rlimit information

* Mon Dec 9 2013 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-9
- DRM master and input event devices are used by  the TakeDevice API
- Clean up bumblebee policy
- Update pegasus_openlmi_storage_t policy
- opensm policy clean up
- openwsman policy clean up
- ninfod policy clean up
- Allow conman to connect to freeipmi services and clean up conman policy
- Allow conmand just bind on 7890 port
- Add freeipmi_stream_connect() interface
- Allow logwatch read madm.conf to support RAID setup
- Add raid_read_conf_files() interface
- Allow up2date running as rpm_t create up2date log file with rpm_log_t labeling
- add rpm_named_filetrans_log_files() interface
- Added policy for conmand
- Allow dkim-milter to create files/dirs in /tmp
- update freeipmi policy
- Add policy for freeipmi services
- Added rdisc_admin and rdisc_systemctl interfaces
- Fix aliases in pegasus.te
- Allow chrome sandbox to read generic cache files in homedir
- Dontaudit mandb searching all mountpoints
- Make sure wine domains create .wine with the correct label
- Add proper aliases for pegasus_openlmi_services_exec_t and pegasus_openlmi_services_t
- Allow windbind the kill capability
- DRM master and input event devices are used by  the TakeDevice API
- add dev_rw_inherited_dri() and dev_rw_inherited_input_dev()
- Added support for default conman port
- Add interfaces for ipmi devices
- Make sure wine domains create .wine with the correct label
- Allow manage dirs in kernel_manage_debugfs interface.
- Allow systemctl running in ipsec_mgmt_t to access /usr/lib/systemd/system/ipsec.service
- Label /usr/lib/systemd/system/ipsec.service as ipsec_mgmt_unit_file_t
- Fix userdom_confined_admin_template()
- Add back exec_content boolean for secadm, logadm, auditadm
- Fix files_filetrans_system_db_named_files() interface
- Allow sulogin to getattr on /proc/kcore
- Add filename transition also for servicelog.db-journal
- Add files_dontaudit_access_check_root()
- Add lvm_dontaudit_access_check_lock() interface
- Allow mount to manage mount_var_run_t files/dirs

* Tue Dec 3 2013 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-8
- Add back fixes for gnome_role_template()
- Label /usr/sbin/htcacheclean as httpd_exec_t
- Add missing alias for pegasus_openlmi_service_exec_t
- Added support for rdisc unit file
- Added new policy for ninfod
- Added new policy for openwsman
- Add antivirus_db_t labeling for /var/lib/clamav-unofficial-sigs
- Allow runuser running as logrotate connections to system DBUS
- Add connectto perm for NM unix stream socket
- Allow watchdog to be executed from cron
- Allow cloud_init to transition to rpm_script_t
- Allow lsmd_plugin_t send system log messages
- Label /var/log/up2date as rpm_log_t and allow sosreport to manage rpm log/pid/cache files which is a part of ABRT policy for sosreport running as abrt_t
- Added new capabilities for mip6d policy
- Label bcache devices as fixed_disk_device_t
- Allow systemctl running in ipsec_mgmt_t to access /usr/lib/systemd/system/ipsec.service
- label /usr/lib/systemd/system/ipsec.service as ipsec_mgmt_unit_file_t

* Tue Nov 26 2013 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-7
- Add lsmd_plugin_t for lsm plugins
- Allow dovecot-deliver to search mountpoints
- Add labeling for /etc/mdadm.conf
- Allow opelmi admin providers to dbus chat with init_t
- Allow sblim domain to read /dev/urandom and /dev/random
- Add back exec_content boolean for secadm, logadm, auditadm
- Allow sulogin to getattr on /proc/kcore

* Tue Nov 26 2013 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-6
- Add filename transition also for servicelog.db-journal
- Add files_dontaudit_access_check_root()
- Add lvm_dontaudit_access_check_lock() interface
- Allow mount to manage mount_var_run_t files/dirs
- Allow updapwd_t to ignore mls levels for writign shadow_t at a lower level
- Make sure boot.log is created with the correct label
- call logging_relabel_all_log_dirs() in systemd.te
- Allow systemd_tmpfiles to relabel log directories
- Allow staff_t to run frequency command
- Allow staff_t to read xserver_log file
- This reverts commit c0f9f125291f189271cbbca033f87131dab1e22f.
- Label hsperfdata_root as tmp_t
- Add plymouthd_create_log()
- Dontaudit leaks from openshift domains into mail domains, needs back port to RHEL6
- Allow sssd to request the kernel loads modules
- Allow gpg_agent to use ssh-add
- Allow gpg_agent to use ssh-add
- Dontaudit access check on /root for myslqd_safe_t
- Add glusterd_brick_t files type
- Allow ctdb to getattr on al filesystems
- Allow abrt to stream connect to syslog
- Allow dnsmasq to list dnsmasq.d directory
- Watchdog opens the raw socket
- Allow watchdog to read network state info
- Dontaudit access check on lvm lock dir
- Allow sosreport to send signull to setroubleshootd
- Add setroubleshoot_signull() interface
- Fix ldap_read_certs() interface
- Allow sosreport all signal perms
- Allow sosreport to run systemctl
- Allow sosreport to dbus chat with rpm
- Allow zabbix_agentd to read all domain state
- Allow sblim_sfcbd_t to read from /dev/random and /dev/urandom
- Allow smoltclient to execute ldconfig
- Allow sosreport to request the kernel to load a module
- Clean up rtas.if
- Clean up docker.if
- drop /var/lib/glpi/files labeling in cron.fc
- Added new policy for rasdaemon
- Add apache labeling for glpi
- Allow pegasus to transition to dmidecode
- Make sure boot.log is created with the correct label
- Fix typo in openshift.te
- remove dup bumblebee_systemctl()
- Allow watchdog to read /etc/passwd
- Allow condor domains to read/write condor_master udp_socket
- Allow openshift_cron_t to append to openshift log files, label /var/log/openshift
- Add back file_pid_filetrans for /var/run/dlm_controld
- Allow smbd_t to use inherited tmpfs content
- Allow mcelog to use the /dev/cpu device
- sosreport runs rpcinfo
- sosreport runs subscription-manager
- Allow setpgid for sosreport
- Allow browser plugins to connect to bumblebee
- New policy for bumblebee and freqset
- Add new policy for mip6d daemon
- Add new policy for opensm daemon

* Mon Nov 18 2013 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-5
- Add back /dev/shm labeling

* Mon Nov 18 2013 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-4
- Fix gnome_role_template() interface

* Thu Nov 14 2013 Miroslav Grepl<mgrepl@redhat.com> 3.13.1-3
- Add policy-rawhide-contrib-apache-content.patch to re-write apache_content_template() by dwalsh

* Thu Nov 14 2013 Dan Walsh<dwalsh@redhat.com> 3.13.1-2
- Fix config.tgz to include lxc_contexts and systemd_contexts

* Wed Nov 13 2013 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-1
- Update to upstream

* Tue Nov 12 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-100
- Fix passenger_stream_connect interface
- setroubleshoot_fixit wants to read network state
- Allow procmail_t to connect to dovecot stream sockets
- Allow cimprovagt service providers to read network states
- Add labeling for /var/run/mariadb
- pwauth uses lastlog() to update system's lastlog
- Allow account provider to read login records
- Add support for texlive2013
- More fixes for user config files to make crond_t running in userdomain
- Add back disable/reload/enable permissions for system class
- Fix manage_service_perms macro
- Allow passwd_t to connect to gnome keyring to change password
- Update mls config files to have cronjobs in the user domains
- Remove access checks that systemd does not actually do

* Fri Nov 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-99
- Add support for yubikey in homedir
- Add support for upd/3052 port
- Allow apcupsd to use PowerChute Network Shutdown
- Allow lsmd to execute various lsmplugins
- Add labeling also for /etc/watchdog\.d where are watchdog scripts located too
- Update gluster_export_all_rw boolean to allow relabel all base file types
- Allow x86_energy_perf  tool to modify the MSR
- Fix /var/lib/dspam/data labeling

* Wed Nov 6 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-98
- Add files_relabel_base_file_types() interface
- Allow netlabel-config to read passwd
- update gluster_export_all_rw boolean to allow relabel all base file types caused by lsetxattr()
- Allow x86_energy_perf  tool to modify the MSR
- Fix /var/lib/dspam/data labeling
- Allow pegasus to domtrans to mount_t
- Add labeling for unconfined scripts in /usr/libexec/watchdog/scripts
- Add support for unconfined watchdog scripts
- Allow watchdog to manage own log files

* Wed Nov 6 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-97
- Add label only for redhat.repo instead of /etc/yum.repos.d. But probably we will need to switch for the directory.
- Label /etc/yum.repos.d as system_conf_t
- Use sysnet_filetrans_named_content in udev.te instead of generic transition for net_conf_t
- Allow dac_override for sysadm_screen_t
- Allow init_t to read ipsec_conf_t as we had it for initrc_t. Needed by ipsec unit file.
- Allow netlabel-config to read meminfo
- Add interface to allow docker to mounton file_t
- Add new interface to exec unlabeled files
- Allow lvm to use docker semaphores
- Setup transitons for .xsessions-errors.old
- Change labels of files in /var/lib/*/.ssh to transition properly
- Allow staff_t and user_t to look at logs using journalctl
- pluto wants to manage own log file
- Allow pluto running as ipsec_t to create pluto.log
- Fix alias decl in corenetwork.te.in
- Add support for fuse.glusterfs
- Allow dmidecode to read/write /run/lock/subsys/rhsmcertd
- Allow rhsmcertd to manage redhat.repo which is now labeled as system.conf. Allow rhsmcertd to manage all log files.
- Additional access for docker
- Added more rules to sblim policy
- Fix kdumpgui_run_bootloader boolean
- Allow dspam to connect to lmtp port
- Included sfcbd service into sblim policy
- rhsmcertd wants to manaage /etc/pki/consumer dir
- Add kdumpgui_run_bootloader boolean
- Add support for /var/cache/watchdog
- Remove virt_domain attribute for virt_qemu_ga_unconfined_t
- Fixes for handling libvirt containes
- Dontaudit attempts by mysql_safe to write content into /
- Dontaudit attempts by system_mail to modify network config
- Allow dspam to bind to lmtp ports
- Add new policy to allow staff_t and user_t to look at logs using journalctl
- Allow apache cgi scripts to list sysfs
- Dontaudit attempts to write/delete user_tmp_t files
- Allow all antivirus domains to manage also own log dirs
- Allow pegasus_openlmi_services_t to stream connect to sssd_t

* Fri Nov 1 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-96
- Add missing permission checks for nscd

* Wed Oct 30 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-95
- Fix alias decl in corenetwork.te.in
- Add support for fuse.glusterfs
- Add file transition rules for content created by f5link
- Rename quantum_port information to neutron
- Allow all antivirus domains to manage also own log dirs
- Rename quantum_port information to neutron
- Allow pegasus_openlmi_services_t to stream connect to sssd_t

* Mon Oct 28 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-94
- Allow sysadm_t to read login information
- Allow systemd_tmpfiles to setattr on var_log_t directories
- Udpdate Makefile to include systemd_contexts
- Add systemd_contexts
- Add fs_exec_hugetlbfs_files() interface
- Add daemons_enable_cluster_mode boolean
- Fix rsync_filetrans_named_content()
- Add rhcs_read_cluster_pid_files() interface
- Update rhcs.if with additional interfaces from RHEL6
- Fix rhcs_domain_template() to not create run dirs with cluster_var_run_t
- Allow glusterd_t to mounton glusterd_tmp_t
- Allow glusterd to unmout al filesystems
- Allow xenstored to read virt config
- Add label for swift_server.lock and make add filetrans_named_content to make sure content gets created with the correct label
- Allow mozilla_plugin_t to mmap hugepages as an executable

* Thu Oct 24 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-93
- Add back userdom_security_admin_template() interface and use it for sysadm_t if sysadm_secadm.pp

* Tue Oct 22 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-92
- Allow sshd_t to read openshift content, needs backport to RHEL6.5
- Label /usr/lib64/sasl2/libsasldb.so.3.0.0 as textrel_shlib_t
- Make sur kdump lock is created with correct label if kdumpctl is executed
- gnome interface calls should always be made within an optional_block
- Allow syslogd_t to connect to the syslog_tls port
- Add labeling for /var/run/charon.ctl socket
- Add kdump_filetrans_named_content()
- Allo setpgid for fenced_t
- Allow setpgid and r/w cluster tmpfs for fenced_t
- gnome calls should always be within optional blocks
- wicd.pid should be labeled as networkmanager_var_run_t
- Allow sys_resource for lldpad

* Thu Oct 17 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-91
- Add rtas policy

* Thu Oct 17 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-90
- Allow mailserver_domains to manage and transition to mailman data
- Dontaudit attempts by mozilla plugin to relabel content, caused by using mv and cp commands
- Allow mailserver_domains to manage and transition to mailman data
- Allow svirt_domains to read sysctl_net_t
- Allow thumb_t to use tmpfs inherited from the user
- Allow mozilla_plugin to bind to the vnc port if running with spice
- Add new attribute to discover confined_admins and assign confined admin to it
- Fix zabbix to handle attributes in interfaces
- Fix zabbix to read system states for all zabbix domains
- Fix piranha_domain_template()
- Allow ctdbd to create udp_socket. Allow ndmbd to access ctdbd var files.
- Allow lldpad sys_rouserce cap due to #986870
- Allow dovecot-auth to read nologin
- Allow openlmi-networking to read /proc/net/dev
- Allow smsd_t to execute scripts created on the fly labeled as smsd_spool_t
- Add zabbix_domain attribute for zabbix domains to treat them together
- Add labels for zabbix-poxy-* (#1018221)
- Update openlmi-storage policy to reflect #1015067
- Back port piranha tmpfs fixes from RHEL6
- Update httpd_can_sendmail boolean to allow read/write postfix spool maildrop
- Add postfix_rw_spool_maildrop_files interface
- Call new userdom_admin_user_templat() also for sysadm_secadm.pp
- Fix typo in userdom_admin_user_template()
- Allow SELinux users to create coolkeypk11sE-Gate in /var/cache/coolkey
- Add new attribute to discover confined_admins
- Fix labeling for /etc/strongswan/ipsec.d
- systemd_logind seems to pass fd to anyone who dbus communicates with it
- Dontaudit leaked write descriptor to dmesg 

* Mon Oct 14 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-89
- Fix gnome_read_generic_data_home_files()
- allow openshift_cgroup_t to read/write inherited openshift file types
- Remove httpd_cobbler_content * from cobbler_admin interface
- Allow svirt sandbox domains to setattr on chr_file and blk_file svirt_sandbox_file_t, so sshd will work within a container
- Allow httpd_t to read also git sys content symlinks
- Allow init_t to read gnome home data
- Dontaudit setroubleshoot_fixit_t execmem, since it does not seem to really need it.
- Allow virsh to execute systemctl
- Fix for nagios_services plugins
- add type defintion for ctdbd_var_t
- Add support for /var/ctdb. Allow ctdb block_suspend and read /etc/passwd file
- Allow net_admin/netlink_socket all hyperv_domain domains
- Add labeling for zarafa-search.log and zarafa-search.pid
- Fix hypervkvp.te
- Fix nscd_shm_use()
- Add initial policy for /usr/sbin/hypervvssd in hypervkvp policy which should be renamed to hyperv. Also add hyperv_domain attribute to treat these HyperV services.
- Add hypervkvp_unit_file_t type
- Fix logging policy
- Allow syslog to bind to tls ports
- Update labeling for /dev/cdc-wdm
- Allow to su_domain to read init states
- Allow init_t to read gnome home data
- Make sure if systemd_logind creates nologin file with the correct label
- Clean up ipsec.te

* Tue Oct 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-88
- Add auth_exec_chkpwd interface
- Fix port definition for ctdb ports
- Allow systemd domains to read /dev/urand
- Dontaudit attempts for mozilla_plugin to append to /dev/random
- Add label for /var/run/charon.*
- Add labeling for /usr/lib/systemd/system/lvm2.*dd policy for motion service
- Fix for nagios_services plugins
- Fix some bugs in zoneminder policy
- add type defintion for ctdbd_var_t
- Add support for /var/ctdb. Allow ctdb block_suspend and read /etc/passwd file
- Allow net_admin/netlink_socket all hyperv_domain domains
- Add labeling for zarafa-search.log and zarafa-search.pid
- glusterd binds to random unreserved ports
- Additional allow rules found by testing glusterfs
- apcupsd needs to send a message to all users on the system so needs to look them up
- Fix the label on ~/.juniper_networks
- Dontaudit attempts for mozilla_plugin to append to /dev/random
- Allow polipo_daemon to connect to flash ports
- Allow gssproxy_t to create replay caches
- Fix nscd_shm_use()
- Add initial policy for /usr/sbin/hypervvssd in hypervkvp policy which should be renamed to hyperv. Also add hyperv_domain attribute to treat these HyperV services.
- Add hypervkvp_unit_file_t type

* Fri Oct 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-87
- init reload  from systemd_localed_t
- Allow domains that communicate with systemd_logind_sessions to use systemd_logind_t fd
- Allow systemd_localed_t to ask systemd to reload the locale.
- Add systemd_runtime_unit_file_t type for unit files that systemd creates in memory
- Allow readahead to read /dev/urand
- Fix lots of avcs about tuned
- Any file names xenstored in /var/log should be treated as xenstored_var_log_t
- Allow tuned to inderact with hugepages
- Allow condor domains to list etc rw dirs

* Fri Oct 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-86
- Fix nscd_shm_use()
- Add initial policy for /usr/sbin/hypervvssd in hypervkvp policy which should be renamed to hyperv. Also add hyperv_domain attribute to treat these HyperV services.
- Add hypervkvp_unit_file_t type
- Add additional fixes forpegasus_openlmi_account_t
- Allow mdadm to read /dev/urand
- Allow pegasus_openlmi_storage_t to create mdadm.conf and write it
- Add label/rules for /etc/mdadm.conf
- Allow pegasus_openlmi_storage_t to transition to fsadm_t
- Fixes for interface definition problems
- Dontaudit dovecot-deliver to gettatr on all fs dirs
- Allow domains to search data_home_t directories
- Allow cobblerd to connect to mysql
- Allow mdadm to r/w kdump lock files
- Add support for kdump lock files
- Label zarafa-search as zarafa-indexer
- Openshift cgroup wants to read /etc/passwd
- Add new sandbox domains for kvm
- Allow mpd to interact with pulseaudio if mpd_enable_homedirs is turned on
- Fix labeling for /usr/lib/systemd/system/lvm2.*
- Add labeling for /usr/lib/systemd/system/lvm2.*
- Fix typos to get a new build. We should not cover filename trans rules to prevent duplicate rules
- Add sshd_keygen_t policy for sshd-keygen
- Fix alsa_home_filetrans interface name and definition
- Allow chown for ssh_keygen_t
- Add fs_dontaudit_getattr_all_dirs()
- Allow init_t to manage etc_aliases_t and read xserver_var_lib_t and chrony keys
- Fix up patch to allow systemd to manage home content
- Allow domains to send/recv unlabeled traffic if unlabelednet.pp is enabled
- Allow getty to exec hostname to get info
- Add systemd_home_t for ~/.local/share/systemd directory

* Wed Oct 2 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-85
- Fix lxc labeling in config.tgz

* Mon Sep 30 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-84
- Fix labeling for /usr/libexec/kde4/kcmdatetimehelper
- Allow tuned to search all file system directories
- Allow alsa_t to sys_nice, to get top performance for sound management
- Add support for MySQL/PostgreSQL for amavis
- Allow openvpn_t to manage openvpn_var_log_t files.
- Allow dirsrv_t to create tmpfs_t directories
- Allow dirsrv to create dirs in /dev/shm with dirsrv_tmpfs label
- Dontaudit leaked unix_stream_sockets into gnome keyring
- Allow telepathy domains to inhibit pipes on telepathy domains
- Allow cloud-init to domtrans to rpm
- Allow abrt daemon to manage abrt-watch tmp files
- Allow abrt-upload-watcher to search /var/spool directory
- Allow nsswitch domains to manage own process key
- Fix labeling for mgetty.* logs
- Allow systemd to dbus chat with upower
- Allow ipsec to send signull to itself
- Allow setgid cap for ipsec_t
- Match upstream labeling

* Wed Sep 25 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-83
- Do not build sanbox pkg on MLS 

* Wed Sep 25 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-82
- wine_tmp is no longer needed
- Allow setroubleshoot to look at /proc
- Allow telepathy domains to dbus with systemd logind
- Fix handling of fifo files of rpm
- Allow mozilla_plugin to transition to itself
- Allow certwatch to write to cert_t directories
- New abrt application
- Allow NetworkManager to set the kernel scheduler
- Make wine_domain shared by all wine domains
- Allow mdadm_t to read images labeled svirt_image_t
- Allow amanda to read /dev/urand
- ALlow my_print_default to read /dev/urand
- Allow mdadm to write to kdumpctl fifo files
- Allow nslcd to send signull to itself
- Allow yppasswd to read /dev/urandom
- Fix zarafa_setrlimit
- Add support for /var/lib/php/wsdlcache
- Add zarafa_setrlimit boolean
- Allow fetchmail to send mails
- Add additional alias for user_tmp_t because wine_tmp_t is no longer used
- More handling of ther kernel keyring required by kerberos
- New privs needed for init_t when running without transition to initrc_t over bin_t, and without unconfined domain installed

* Thu Sep 19 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-81
- Dontaudit attempts by sosreport to read shadow_t
- Allow browser sandbox plugins to connect to cups to print
- Add new label mpd_home_t
- Label /srv/www/logs as httpd_log_t
- Add support for /var/lib/php/wsdlcache
- Add zarafa_setrlimit boolean
- Allow fetchmail to send mails
- Add labels for apache logs under miq package
- Allow irc_t to use tcp sockets
- fix labels in puppet.if
- Allow tcsd to read utmp file
- Allow openshift_cron_t to run ssh-keygen in ssh_keygen_t to access host keys
- Define svirt_socket_t as a domain_type
- Take away transition from init_t to initrc_t when executing bin_t, allow init_t to run chk_passwd_t
- Fix label on pam_krb5 helper apps

* Thu Sep 12 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-80
- Allow ldconfig to write to kdumpctl fifo files
- allow neutron to connect to amqp ports
- Allow kdump_manage_crash to list the kdump_crash_t directory
- Allow glance-api to connect to amqp port
- Allow virt_qemu_ga_t to read meminfo
- Add antivirus_home_t type for antivirus date in HOMEDIRS
- Allow mpd setcap which is needed by pulseaudio
- Allow smbcontrol to create content in /var/lib/samba
- Allow mozilla_exec_t to be used as a entrypoint to mozilla_domtrans_spec
- Add additional labeling for qemu-ga/fsfreeze-hook.d scripts
- amanda_exec_t needs to be executable file
- Allow block_suspend cap for samba-net
- Allow apps that read ipsec_mgmt_var_run_t to search ipsec_var_run_t
- Allow init_t to run crash utility
- Treat usr_t just like bin_t for transitions and executions
- Add port definition of pka_ca to port 829 for openshift
- Allow selinux_store to use symlinks

* Mon Sep 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-79
- Allow block_suspend cap for samba-net
- Allow t-mission-control to manage gabble cache files
- Allow nslcd to read /sys/devices/system/cpu
- Allow selinux_store to use symlinks

* Mon Sep 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-78
- Allow xdm_t to transition to itself
- Call neutron interfaces instead of quantum
- Allow init to change targed role to make uncofined services (xrdp which now has own systemd unit file) working. We want them to have in unconfined_t
- Make sure directories in /run get created with the correct label
- Make sure /root/.pki gets created with the right label
- try to remove labeling for motion from zoneminder_exec_t to bin_t
- Allow inetd_t to execute shell scripts
- Allow cloud-init to read all domainstate
- Fix to use quantum port
- Add interface netowrkmanager_initrc_domtrans
- Fix boinc_execmem
- Allow t-mission-control to read gabble cache home
- Add labeling for ~/.cache/telepathy/avatars/gabble
- Allow memcache to read sysfs data
- Cleanup antivirus policy and add additional fixes
- Add boolean boinc_enable_execstack
- Add support for couchdb in rabbitmq policy
- Add interface couchdb_search_pid_dirs
- Allow firewalld to read NM state
- Allow systemd running as git_systemd to bind git port
- Fix mozilla_plugin_rw_tmpfs_files()

* Thu Sep 5 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-77
- Split out rlogin ports from inetd
- Treat files labeld as usr_t like bin_t when it comes to transitions
- Allow staff_t to read login config
- Allow ipsec_t to read .google authenticator data
- Allow systemd running as git_systemd to bind git port
- Fix mozilla_plugin_rw_tmpfs_files()
- Call the correct interface - corenet_udp_bind_ktalkd_port()
- Allow all domains that can read gnome_config to read kde config
- Allow sandbox domain to read/write mozilla_plugin_tmpfs_t so pulseaudio will work
- Allow mdadm to getattr any file system
- Allow a confined domain to executes mozilla_exec_t via dbus
- Allow cupsd_lpd_t to bind to the printer port
- Dontaudit attempts to bind to ports < 1024 when nis is turned on
- Allow apache domain to connect to gssproxy socket
- Allow rlogind to bind to the rlogin_port
- Allow telnetd to bind to the telnetd_port
- Allow ktalkd to bind to the ktalkd_port
- Allow cvs to bind to the cvs_port

* Wed Sep 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-76
- Cleanup related to init_domain()+inetd_domain fixes
- Use just init_domain instead of init_daemon_domain in inetd_core_service_domain
- svirt domains neeed to create kobject_uevint_sockets
- Lots of new access required for sosreport
- Allow tgtd_t to connect to isns ports
- Allow init_t to transition to all inetd domains:
- openct needs to be able to create netlink_object_uevent_sockets
- Dontaudit leaks into ldconfig_t
- Dontaudit su domains getattr on /dev devices, move su domains to attribute based calls
- Move kernel_stream_connect into all Xwindow using users
- Dontaudit inherited lock files in ifconfig o dhcpc_t

* Tue Sep 3 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-75
- Also sock_file trans rule is needed in lsm
- Fix labeling for fetchmail pid files/dirs
- Add additional fixes for abrt-upload-watch
- Fix polipo.te
- Fix transition rules in asterisk policy
- Add fowner capability to networkmanager policy
- Allow polipo to connect to tor ports
- Cleanup lsmd.if
- Cleanup openhpid policy
- Fix kdump_read_crash() interface
- Make more domains as init domain
- Fix cupsd.te
- Fix requires in rpm_rw_script_inherited_pipes
- Fix interfaces in lsm.if
- Allow munin service plugins to manage own tmpfs files/dirs
- Allow virtd_t also relabel unix stream sockets for virt_image_type
- Make ktalk as init domain
- Fix to define ktalkd_unit_file_t correctly
- Fix ktalk.fc
- Add systemd support for talk-server
- Allow glusterd to create sock_file in /run
- Allow xdm_t to delete gkeyringd_tmp_t files on logout
- Add fixes for hypervkvp policy
- Add logwatch_can_sendmail boolean
- Allow mysqld_safe_t to handle also symlinks in /var/log/mariadb
- Allow xdm_t to delete gkeyringd_tmp_t files on logout

* Thu Aug 29 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-74
- Add selinux-policy-sandbox pkg

* Tue Aug 27 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-73
0 
- Allow rhsmcertd to read init state
- Allow fsetid for pkcsslotd
- Fix labeling for /usr/lib/systemd/system/pkcsslotd.service
- Allow fetchmail to create own pid with correct labeling
- Fix rhcs_domain_template()
- Allow roles which can run mock to read mock lib files to view results
- Allow rpcbind to use nsswitch
- Fix lsm.if summary
- Fix collectd_t can read /etc/passwd file
- Label systemd unit files under dracut correctly
- Add support for pam_mount to mount user's encrypted home When a user logs in and logs out using ssh
- Add support for .Xauthority-n
- Label umount.crypt as lvm_exec_t
- Allow syslogd to search psad lib files
- Allow ssh_t to use /dev/ptmx
- Make sure /run/pluto dir is created with correct labeling
- Allow syslog to run shell and bin_t commands
- Allow ip to relabel tun_sockets
- Allow mount to create directories in files under /run
- Allow processes to use inherited fifo files

* Fri Aug 23 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-72
- Add policy for lsmd
- Add support for /var/log/mariadb dir and allow mysqld_safe to list this directory
- Update condor_master rules to allow read system state info and allow logging
- Add labeling for /etc/condor and allow condor domain to write it (bug)
- Allow condor domains to manage own logs
- Allow glusterd to read domains state
- Fix initial hypervkvp policy
- Add policy for hypervkvpd
- Fix redis.if summary

* Wed Aug 21 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-71
- Allow boinc to connect to  @/tmp/.X11-unix/X0
- Allow beam.smp to connect to tcp/5984
- Allow named to manage own log files
- Add label for /usr/libexec/dcc/start-dccifd  and domtrans to dccifd_t
- Add virt_transition_userdomain boolean decl
- Allow httpd_t to sendto unix_dgram sockets on its children
- Allow nova domains to execute ifconfig
- bluetooth wants to create fifo_files in /tmp
- exim needs to be able to manage mailman data
- Allow sysstat to getattr on all file systems
- Looks like bluetoothd has moved
- Allow collectd to send ping packets
- Allow svirt_lxc domains to getpgid
- Remove virt-sandbox-service labeling as virsh_exec_t, since it no longer does virsh_t stuff
- Allow frpintd_t to read /dev/urandom
- Allow asterisk_t to create sock_file in /var/run
- Allow usbmuxd to use netlink_kobject
- sosreport needs to getattr on lots of devices, and needs access to netlink_kobject_uevent_socket
- More cleanup of svirt_lxc policy
- virtd_lxc_t now talks to dbus
- Dontaudit leaked ptmx_t
- Allow processes to use inherited fifo files
- Allow openvpn_t to connect to squid ports
- Allow prelink_cron_system_t to ask systemd to reloaddd miscfiles_dontaudit_access_check_cert()
- Allow ssh_t to use /dev/ptmx
- Make sure /run/pluto dir is created with correct labeling
- Allow syslog to run shell and bin_t commands
- Allow ip to relabel tun_sockets
- Allow mount to create directories in files under /run
- Allow processes to use inherited fifo files
- Allow user roles to connect to the journal socket

* Thu Aug 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-70
- selinux_set_enforce_mode needs to be used with type
- Add append to the dontaudit for unix_stream_socket of xdm_t leak
- Allow xdm_t to create symlinks in log direcotries
- Allow login programs to read afs config
- Label 10933 as a pop port, for dovecot
- New policy to allow selinux_server.py to run as semanage_t as a dbus service
- Add fixes to make netlabelctl working on MLS
- AVCs required for running sepolicy gui as staff_t
- Dontaudit attempts to read symlinks, sepolicy gui is likely to cause this type of AVC
- New dbus server to be used with new gui
- After modifying some files in /etc/mail, I saw this needed on the next boot
- Loading a vm from /usr/tmp with virt-manager
- Clean up oracleasm policy for Fedora
- Add oracleasm policy written by rlopez@redhat.com
- Make postfix_postdrop_t as mta_agent to allow domtrans to system mail if it is executed by apache
- Add label for /var/crash
- Allow fenced to domtrans to sanclok_t
- Allow nagios to manage nagios spool files
- Make tfptd as home_manager
- Allow kdump to read kcore on MLS system
- Allow mysqld-safe sys_nice/sys_resource caps
- Allow apache to search automount tmp dirs if http_use_nfs is enabled
- Allow crond to transition to named_t, for use with unbound
- Allow crond to look at named_conf_t, for unbound
- Allow mozilla_plugin_t to transition its home content
- Allow dovecot_domain to read all system and network state
- Allow httpd_user_script_t to call getpw
- Allow semanage to read pid files
- Dontaudit leaked file descriptors from user domain into thumb
- Make PAM authentication working if it is enabled in ejabberd
- Add fixes for rabbit to fix ##992920,#992931
- Allow glusterd to mount filesystems
- Loading a vm from /usr/tmp with virt-manager
- Trying to load a VM I got an AVC from devicekit_disk for loopcontrol device
- Add fix for pand service
- shorewall touches own log
- Allow nrpe to list /var
- Mozilla_plugin_roles can not be passed into lpd_run_lpr
- Allow afs domains to read afs_config files
- Allow login programs to read afs config
- Allow virt_domain to read virt_var_run_t symlinks
- Allow smokeping to send its process signals
- Allow fetchmail to setuid
- Add kdump_manage_crash() interface
- Allow abrt domain to write abrt.socket

* Wed Jul 31 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-69
- Add more aliases in pegasus.te
- Add more fixes for *_admin interfaces
- Add interface fixes
- Allow nscd to stream connect to nmbd
- Allow gnupg apps to write to pcscd socket
- Add more fixes for openlmi provides. Fix naming and support for additionals
- Allow fetchmail to resolve host names
- Allow firewalld to interact also with lnk files labeled as firewalld_etc_rw_t
- Add labeling for cmpiLMI_Fan-cimprovagt
- Allow net_admin for glusterd
- Allow telepathy domain to create dconf with correct labeling in /home/userX/.cache/
- Add pegasus_openlmi_system_t
- Fix puppet_domtrans_master() to make all puppet calling working in passenger.te
- Fix corecmd_exec_chroot()
- Fix logging_relabel_syslog_pid_socket interface
- Fix typo in unconfineduser.te
- Allow system_r to access unconfined_dbusd_t to run hp_chec

* Tue Jul 30 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-68
- Allow xdm_t to act as a dbus client to itsel
- Allow fetchmail to resolve host names
- Allow gnupg apps to write to pcscd socket
- Add labeling for cmpiLMI_Fan-cimprovagt
- Allow net_admin for glusterd
- Allow telepathy domain to create dconf with correct labeling in /home/userX/.cache/
- Add pegasus_openlmi_system_t
- Fix puppet_domtrans_master() to make all puppet calling working in passenger.te
-httpd_t does access_check on certs

* Fri Jul 26 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-67
- Add support for cmpiLMI_Service-cimprovagt
- Allow pegasus domtrans to rpm_t to make pycmpiLMI_Software-cimprovagt running as rpm_t
- Label pycmpiLMI_Software-cimprovagt as rpm_exec_t
- Add support for pycmpiLMI_Storage-cimprovagt
- Add support for cmpiLMI_Networking-cimprovagt
- Allow system_cronjob_t to create user_tmpfs_t to make pulseaudio working
- Allow virtual machines and containers to run as user doains, needed for virt-sandbox
- Allow buglist.cgi to read cpu info

* Mon Jul 22 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-66
- Allow systemd-tmpfile to handle tmp content in print spool dir
- Allow systemd-sysctl to send system log messages
- Add support for RTP media ports and fmpro-internal
- Make auditd working if audit is configured to perform SINGLE action on disk error
- Add interfaces to handle systemd units
- Make systemd-notify working if pcsd is used
- Add support for netlabel and label /usr/sbin/netlabelctl as iptables_exec_t
- Instead of having all unconfined domains get all of the named transition rules,
- Only allow unconfined_t, init_t, initrc_t and rpm_script_t by default.
- Add definition for the salt ports
- Allow xdm_t to create link files in xdm_var_run_t
- Dontaudit reads of blk files or chr files leaked into ldconfig_t
- Allow sys_chroot for useradd_t
- Allow net_raw cap for ipsec_t
- Allow sysadm_t to reload services
- Add additional fixes to make strongswan working with a simple conf
- Allow sysadm_t to enable/disable init_t services
- Add additional glusterd perms
- Allow apache to read lnk files in the /mnt directory
- Allow glusterd to ask the kernel to load a module
- Fix description of ftpd_use_fusefs boolean
- Allow svirt_lxc_net_t to sys_chroot, modify policy to tighten up svirt_lxc_domain capabilties and process controls, but add them to svirt_lxc_net_t
- Allow glusterds to request load a kernel module
- Allow boinc to stream connect to xserver_t
- Allow sblim domains to read /etc/passwd
- Allow mdadm to read usb devices
- Allow collectd to use ping plugin
- Make foghorn working with SNMP
- Allow sssd to read ldap certs
- Allow haproxy to connect to RTP media ports
- Add additional trans rules for aide_db
- Add labeling for /usr/lib/pcsd/pcsd
- Add labeling for /var/log/pcsd
- Add support for pcs which is a corosync and pacemaker configuration tool

* Wed Jul 17 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-65
- Label /var/lib/ipa/pki-ca/publish as pki_tomcat_cert_t
- Add labeling for /usr/libexec/kde4/polkit-kde-authentication-agent-1
- Allow all domains that can domtrans to shutdown, to start the power services script to shutdown
- consolekit needs to be able to shut down system
- Move around interfaces
- Remove nfsd_rw_t and nfsd_ro_t, they don't do anything
- Add additional fixes for rabbitmq_beam to allow getattr on mountpoints
- Allow gconf-defaults-m to read /etc/passwd
- Fix pki_rw_tomcat_cert() interface to support lnk_files

* Fri Jul 12 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-64
- Add support for gluster ports
- Make sure that all keys located in /etc/ssh/ are labeled correctly
- Make sure apcuspd lock files get created with the correct label
- Use getcap in gluster.te
- Fix gluster policy
- add additional fixes to allow beam.smp to interact with couchdb files
- Additional fix for #974149
- Allow gluster to user gluster ports
- Allow glusterd to transition to rpcd_t and add additional fixes for #980683
- Allow tgtd working when accessing to the passthrough device
- Fix labeling for mdadm unit files

* Thu Jul 11 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-63
- Add mdadm fixes

* Tue Jul 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-62
- Fix definition of sandbox.disabled to sandbox.pp.disabled

* Mon Jul 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-61
- Allow mdamd to execute systemctl
- Allow mdadm to read /dev/kvm
- Allow ipsec_mgmt_t to read l2tpd pid content

* Mon Jul 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-60
- Allow nsd_t to read /dev/urand
- Allow mdadm_t to read framebuffer
- Allow rabbitmq_beam_t to read process info on rabbitmq_epmd_t
- Allow mozilla_plugin_config_t to create tmp files
- Cleanup openvswitch policy
- Allow mozilla plugin to getattr on all executables
- Allow l2tpd_t to create fifo_files in /var/run
- Allow samba to touch/manage fifo_files or sock_files in a samba_share_t directory
- Allow mdadm to connecto its own unix_stream_socket
- FIXME: nagios changed locations to /log/nagios which is wrong. But we need to have this workaround for now.
- Allow apache to access smokeping pid files
- Allow rabbitmq_beam_t to getattr on all filesystems
- Add systemd support for iodined
- Allow nup_upsdrvctl_t to execute its entrypoint
- Allow fail2ban_client to write to fail2ban_var_run_t, Also allow it to use nsswitch
- add labeling for ~/.cache/libvirt-sandbox
- Add interface to allow domains transitioned to by confined users to send sigchld to screen program
- Allow sysadm_t to check the system status of files labeled etc_t, /etc/fstab
- Allow systemd_localed to start /usr/lib/systemd/system/systemd-vconsole-setup.service
- Allow an domain that has an entrypoint from a type to be allowed to execute the entrypoint without a transition,  I can see no case where this is  a bad thing, and elminiates a whole class of AVCs.
- Allow staff to getsched all domains, required to run htop
- Add port definition for redis port
- fix selinuxuser_use_ssh_chroot boolean

* Wed Jul 3 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-59
- Add prosody policy written by Michael Scherer
- Allow nagios plugins to read /sys info
- ntpd needs to manage own log files
- Add support for HOME_DIR/.IBMERS
- Allow iptables commands to read firewalld config
- Allow consolekit_t to read utmp
- Fix filename transitions on .razor directory
- Add additional fixes to make DSPAM with LDA working
- Allow snort to read /etc/passwd
- Allow fail2ban to communicate with firewalld over dbus
- Dontaudit openshift_cgreoup_file_t read/write leaked dev
- Allow nfsd to use mountd port
- Call th proper interface
- Allow openvswitch to read sys and execute plymouth
- Allow tmpwatch to read /var/spool/cups/tmp
- Add support for /usr/libexec/telepathy-rakia
- Add systemd support for zoneminder
- Allow mysql to create files/directories under /var/log/mysql
- Allow zoneminder apache scripts to rw zoneminder tmpfs
- Allow httpd to manage zoneminder lib files
- Add zoneminder_run_sudo boolean to allow to start zoneminder
- Allow zoneminder to send mails
- gssproxy_t sock_file can be under /var/lib
- Allow web domains to connect to whois port.
- Allow sandbox_web_type to connect to the same ports as mozilla_plugin_t.
- We really need to add an interface to corenet to define what a web_client_domain is and
- then define chrome_sandbox_t, mozilla_plugin_t and sandbox_web_type to that domain.
- Add labeling for cmpiLMI_LogicalFile-cimprovagt
- Also make pegasus_openlmi_logicalfile_t as unconfined to have unconfined_domain attribute for filename trans rules
- Update policy rules for pegasus_openlmi_logicalfile_t
- Add initial types for logicalfile/unconfined OpenLMI providers
- mailmanctl needs to read own log
- Allow logwatch manage own lock files
- Allow nrpe to read meminfo
- Allow httpd to read certs located in pki-ca
- Add pki_read_tomcat_cert() interface
- Add support for nagios openshift plugins
- Add port definition for redis port
- fix selinuxuser_use_ssh_chroot boolean

* Fri Jun 28 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-58
- Shrink the size of policy by moving to attributes, also add dridomain so that mozilla_plugin can follow selinuxuse_dri boolean. 
- Allow bootloader to manage generic log files 
- Allow ftp to bind to port 989 
- Fix label of new gear directory 
- Add support for new directory /var/lib/openshift/gears/ 
- Add openshift_manage_lib_dirs() 
- allow virtd domains to manage setrans_var_run_t 
- Allow useradd to manage all openshift content 
- Add support so that mozilla_plugin_t can use dri devices 
- Allow chronyd to change the scheduler 
- Allow apmd to shut downthe system 
- Devicekit_disk_t needs to manage /etc/fstab

* Wed Jun 26 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-57
- Make DSPAM to act as a LDA working
- Allow ntop to create netlink socket
- Allow policykit to send a signal to policykit-auth
- Allow stapserver to dbus chat with avahi/systemd-logind
- Fix labeling on haproxy unit file
- Clean up haproxy policy
- A new policy for haproxy and placed it to rhcs.te
- Add support for ldirectord and treat it with cluster_t
- Make sure anaconda log dir is created with var_log_t

* Mon Jun 24 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-56
- Allow lvm_t to create default targets for filesystem handling
- Fix labeling for razor-lightdm binaries
- Allow insmod_t to read any file labeled var_lib_t
- Add policy for pesign
- Activate policy for cmpiLMI_Account-cimprovagt
- Allow isnsd syscall=listen
- /usr/libexec/pegasus/cimprovagt needs setsched caused by sched_setscheduler
- Allow ctdbd to use udp/4379
- gatherd wants sys_nice and setsched
- Add support for texlive2012
- Allow NM to read file_t (usb stick with no labels used to transfer keys for example)
- Allow cobbler to execute apache with domain transition

* Fri Jun 21 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-55
- condor_collector uses tcp/9000
- Label /usr/sbin/virtlockd as virtd_exec_t for now
- Allow cobbler to execute ldconfig
- Allow NM to execute ssh
- Allow mdadm to read /dev/crash
- Allow antivirus domains to connect to snmp port
- Make amavisd-snmp working correctly
- Allow nfsd_t to mounton nfsd_fs_t
- Add initial snapper policy
- We still need to have consolekit policy
- Dontaudit firefox attempting to connect to the xserver_port_t if run within sandbox_web_t
- Dontaudit sandbox apps attempting to open user_devpts_t
- Allow dirsrv to read network state
- Fix pki_read_tomcat_lib_files
- Add labeling for /usr/libexec/nm-ssh-service
- Add label cert_t for /var/lib/ipa/pki-ca/publish
- Lets label /sys/fs/cgroup as cgroup_t for now, to keep labels consistant
- Allow nfsd_t to mounton nfsd_fs_t
- Dontaudit sandbox apps attempting to open user_devpts_t
- Allow passwd_t to change role to system_r from unconfined_r

* Wed Jun 19 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-54
- Don't audit access checks by sandbox xserver on xdb var_lib
- Allow ntop to read usbmon devices
- Add labeling for new polcykit authorizor
- Dontaudit access checks from fail2ban_client
- Don't audit access checks by sandbox xserver on xdb var_lib
- Allow apps that connect to xdm stream to conenct to xdm_dbusd_t stream
- Fix labeling for all /usr/bim/razor-lightdm-* binaries
- Add filename trans for /dev/md126p1

* Tue Jun 18 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-53
- Make vdagent able to request loading kernel module
- Add support for cloud-init make it as unconfined domain
- Allow snmpd to run smartctl in fsadm_t domain
- remove duplicate openshift_search_lib() interface
- Allow mysqld to search openshift lib files
- Allow openshift cgroup to interact with passedin file descriptors
- Allow colord to list directories inthe users homedir
- aide executes prelink to check files
- Make sure cupsd_t creates content in /etc/cups with the correct label
- Lest dontaudit apache read all domains, so passenger will not cause this avc
- Allow gssd to connect to gssproxy
- systemd-tmpfiles needs to be able to raise the level to fix labeling on /run/setrans in MLS
- Allow systemd-tmpfiles to relabel also lock files
- Allow useradd to add homdir in /var/lib/openshift
- Allow setfiles and semanage to write output to /run/files

* Fri Jun 14 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-52
- Add labeling for /dev/tgt
- Dontaudit leak fd from firewalld for modprobe
- Allow runuser running as rpm_script_t to create netlink_audit socket
- Allow mdadm to read BIOS non-volatile RAM

* Thu Jun 13 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-51
- accountservice watches when accounts come and go in wtmp
- /usr/java/jre1.7.0_21/bin/java needs to create netlink socket
- Add httpd_use_sasl boolean
- Allow net_admin for tuned_t
- iscsid needs sys_module to auto-load kernel modules
- Allow blueman to read bluetooth conf
- Add nova_manage_lib_files() interface
- Fix mplayer_filetrans_home_content()
- Add mplayer_filetrans_home_content()
- mozilla_plugin_config_roles need to be able to access mozilla_plugin_config_t
- Revert "Allow thumb_t to append inherited xdm stream socket"
- Add iscsi_filetrans_named_content() interface
- Allow to create .mplayer with the correct labeling for unconfined
- Allow iscsiadmin to create lock file with the correct labeling

* Tue Jun 11 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-50
- Allow wine to manage wine home content
- Make amanda working with socket actiovation
- Add labeling for /usr/sbin/iscsiadm
- Add support for /var/run/gssproxy.sock
- dnsmasq_t needs to read sysctl_net_t

* Fri Jun 7 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-49
- Fix courier_domain_template() interface
- Allow blueman to write ip_forward
- Allow mongodb to connect to mongodb port
- Allow mongodb to connect to mongodb port
- Allow java to bind jobss_debug port
- Fixes for *_admin interfaces
- Allow iscsid auto-load kernel modules needed for proper iSCSI functionality
- Need to assign attribute for courier_domain to all courier_domains
- Fail2ban reads /etc/passwd
- postfix_virtual will create new files in postfix_spool_t
- abrt triggers sys_ptrace by running pidof
- Label ~/abc as mozilla_home_t, since java apps as plugin want to create it
- Add passenger fixes needed by foreman
- Remove dup interfaces
- Add additional interfaces for quantum
- Add new interfaces for dnsmasq
- Allow  passenger to read localization and send signull to itself
- Allow dnsmasq to stream connect to quantum
- Add quantum_stream_connect()
- Make sure that mcollective starts the service with the correct labeling
- Add labels for ~/.manpath
- Dontaudit attempts by svirt_t to getpw* calls
- sandbox domains are trying to look at parent process data
- Allow courior auth to create its pid file in /var/spool/courier subdir
- Add fixes for beam to have it working with couchdb
- Add labeling for /run/nm-xl2tpd.con
- Allow apache to stream connect to thin
- Add systemd support for amand
- Make public types usable for fs mount points
- Call correct mandb interface in domain.te
- Allow iptables to r/w quantum inherited pipes and send sigchld
- Allow ifconfig domtrans to iptables and execute ldconfig
- Add labels for ~/.manpath
- Allow systemd to read iscsi lib files
- seunshare is trying to look at parent process data

* Mon Jun 3 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-48
- Fix openshift_search_lib
- Add support for abrt-uefioops-oops
- Allow colord to getattr any file system
- Allow chrome processes to look at each other
- Allow sys_ptrace for abrt_t
- Add new policy for gssproxy
- Dontaudit leaked file descriptor writes from firewalld
- openshift_net_type is interface not template
- Dontaudit pppd to search gnome config
- Update openshift_search_lib() interface
- Add fs_list_pstorefs()
- Fix label on libbcm_host.so since it is built incorrectly on raspberry pi, needs back port to F18
- Better labels for raspberry pi devices
- Allow init to create devpts_t directory
- Temporarily label rasbery pi devices as memory_device_t, needs back port to f18
- Allow sysadm_t to build kernels
- Make sure mount creates /var/run/blkid with the correct label, needs back port to F18
- Allow userdomains to stream connect to gssproxy
- Dontaudit leaked file descriptor writes from firewalld
- Allow xserver to read /dev/urandom
- Add additional fixes for ipsec-mgmt
- Make SSHing into an Openshift Enterprise Node working

* Wed May 29 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-47
- Add transition rules to unconfined domains and to sysadm_t to create /etc/adjtime
- with the proper label.
- Update files_filetrans_named_content() interface to get right labeling for pam.d conf files
- Allow systemd-timedated to create adjtime
- Add clock_create_adjtime()
- Additional fix ifconfing for #966106
- Allow kernel_t to create boot.log with correct labeling
- Remove unconfined_mplayer for which we don't have rules
- Rename interfaces
- Add userdom_manage_user_home_files/dirs interfaces
- Fix files_dontaudit_read_all_non_security_files
- Fix ipsec_manage_key_file()
- Fix ipsec_filetrans_key_file()
- Label /usr/bin/razor-lightdm-greeter as xdm_exec_t instead of spamc_exec_t
- Fix labeling for ipse.secrets
- Add interfaces for ipsec and labeling for ipsec.info and ipsec_setup.pid
- Add files_dontaudit_read_all_non_security_files() interface
- /var/log/syslog-ng should be labeled var_log_t
- Make ifconfig_var_run_t a mountpoint
- Add transition from ifconfig to dnsmasq
- Allow ifconfig to execute bin_t/shell_exec_t
- We want to have hwdb.bin labeled as etc_t
- update logging_filetrans_named_content() interface
- Allow systemd_timedate_t to manage /etc/adjtime
- Allow NM to send signals to l2tpd
- Update antivirus_can_scan_system boolean
- Allow devicekit_disk_t to sys_config_tty
- Run abrt-harvest programs as abrt_t, and allow abrt_t to list all filesystem directories
- Make printing from vmware working
- Allow php-cgi from php54 collection to access /var/lib/net-snmp/mib_indexes
- Add virt_qemu_ga_data_t for qemu-ga
- Make chrome and mozilla able to connect to same ports, add jboss_management_port_t to both
- Fix typo in virt.te
- Add virt_qemu_ga_unconfined_t for hook scripts
- Make sure NetworkManager files get created with the correct label
- Add mozilla_plugin_use_gps boolean
- Fix cyrus to have support for net-snmp
- Additional fixes for dnsmasq and quantum for #966106
- Add plymouthd_create_log()
- remove httpd_use_oddjob for which we don't have rules
- Add missing rules for httpd_can_network_connect_cobbler
- Add missing cluster_use_execmem boolean
- Call userdom_manage_all_user_home_type_files/dirs
- Additional fix for ftp_home_dir
- Fix ftp_home_dir boolean
- Allow squit to recv/send client squid packet
- Fix nut.te to have nut_domain attribute
- Add support for ejabberd; TODO: revisit jabberd and rabbit policy
- Fix amanda policy
- Add more fixes for domains which use libusb
- Make domains which use libusb working correctly
- Allow l2tpd to create ipsec key files with correct labeling and manage them
- Fix cobbler_manage_lib_files/cobbler_read_lib_files to cover also lnk files
- Allow rabbitmq-beam to bind generic node
- Allow l2tpd to read ipse-mgmt pid files
- more fixes for l2tpd, NM and pppd from #967072

* Wed May 22 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-46
- Dontaudit to getattr on dirs for dovecot-deliver
- Allow raiudusd server connect to postgresql socket
- Add kerberos support for radiusd
- Allow saslauthd to connect to ldap port
- Allow postfix to manage postfix_private_t files
- Add chronyd support for #965457
- Fix labeling for HOME_DIR/\.icedtea
- CHange squid and snmpd to be allowed also write own logs
- Fix labeling for /usr/libexec/qemu-ga
- Allow virtd_t to use virt_lock_t
- Allow also sealert to read the policy from the kernel
- qemu-ga needs to execute scripts in /usr/libexec/qemu-ga and to use /tmp content
- Dontaudit listing of users homedir by sendmail Seems like a leak
- Allow passenger to transition to puppet master
- Allow apache to connect to mythtv
- Add definition for mythtv ports

* Fri May 17 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-45
- Add additional fixes for #948073 bug
- Allow sge_execd_t to also connect to sge ports
- Allow openshift_cron_t to manage openshift_var_lib_t sym links
- Allow openshift_cron_t to manage openshift_var_lib_t sym links
- Allow sge_execd to bind sge ports. Allow kill capability and reads cgroup files
- Remove pulseaudio filetrans pulseaudio_manage_home_dirs which is a part of pulseaudio_manage_home_files
- Add networkmanager_stream_connect()
- Make gnome-abrt wokring with staff_t
- Fix openshift_manage_lib_files() interface
- mdadm runs ps command which seems to getattr on random log files
- Allow mozilla_plugin_t to create pulseaudit_home_t directories
- Allow qemu-ga to shutdown virtual hosts
- Add labelling for cupsd-browsed
- Add web browser plugins to connect to aol ports
- Allow nm-dhcp-helper to stream connect to NM
- Add port definition for sge ports

* Mon May 13 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-44
- Make sure users and unconfined domains create .hushlogin with the correct label
- Allow pegaus to chat with realmd over DBus
- Allow cobblerd to read network state
- Allow boicn-client to stat on /dev/input/mice
- Allow certwatch to read net_config_t when it executes apache
- Allow readahead to create /run/systemd and then create its own directory with the correct label

* Mon May 13 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-43
- Transition directories and files when in a user_tmp_t directory
- Change certwatch to domtrans to apache instead of just execute
- Allow virsh_t to read xen lib files
- update policy rules for pegasus_openlmi_account_t
- Add support for svnserve_tmp_t
- Activate account openlmi policy
- pegasus_openlmi_domain_template needs also require pegasus_t
- One more fix for policykit.te
- Call fs_list_cgroups_dirs() in policykit.te
- Allow nagios service plugin to read mysql config files
- Add labeling for /var/svn
- Fix chrome.te
- Fix pegasus_openlmi_domain_template() interfaces
- Fix dev_rw_vfio_dev definiton, allow virtd_t to read tmpfs_t symlinks
- Fix location of google-chrome data
- Add support for chome_sandbox to store content in the homedir
- Allow policykit to watch for changes in cgroups file system
- Add boolean to allow  mozilla_plugin_t to use spice
- Allow collectd to bind to udp port
- Allow collected_t to read all of /proc
- Should use netlink socket_perms
- Should use netlink socket_perms
- Allow glance domains to connect to apache ports
- Allow apcupsd_t to manage its log files
- Allow chrome objects to rw_inherited unix_stream_socket from callers
- Allow staff_t to execute virtd_exec_t for running vms
- nfsd_t needs to bind mountd port to make nfs-mountd.service working
- Allow unbound net_admin capability because of setsockopt syscall
- Fix fs_list_cgroup_dirs()
- Label /usr/lib/nagios/plugins/utils.pm as bin_t
- Remove uplicate definition of fs_read_cgroup_files()
- Remove duplicate definition of fs_read_cgroup_files()
- Add files_mountpoint_filetrans interface to be used by quotadb_t and snapperd
- Additional interfaces needed to list and read cgroups config
- Add port definition for collectd port
- Add labels for /dev/ptp*
- Allow staff_t to execute virtd_exec_t for running vms

* Mon May 6 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-42
- Allow samba-net to also read realmd tmp files
- Allow NUT to use serial ports
- realmd can be started by systemctl now

* Mon May 6 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-41
- Remove userdom_home_manager for xdm_t and move all rules to xserver.te directly
- Add new xdm_write_home boolean to allow xdm_t to create files in HOME dirs with xdm_home_t
- Allow postfix-showq to read/write unix.showq in /var/spool/postfix/pid
- Allow virsh to read xen lock file
- Allow qemu-ga to create files in /run with proper labeling
- Allow glusterd to connect to own socket in /tmp
- Allow glance-api to connect to http port to make glance image-create working
- Allow keystonte_t to execute rpm

* Fri May 3 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-40
- Fix realmd cache interfaces

* Fri May 3 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-39
- Allow tcpd to execute leafnode
- Allow samba-net to read realmd cache files
- Dontaudit sys_tty_config for alsactl
- Fix allow rules for postfix_var_run
- Allow cobblerd to read /etc/passwd
- Allow pegasus to read exports
- Allow systemd-timedate to read xdm state
- Allow mout to stream connect to rpcbind
- Add labeling just for /usr/share/pki/ca-trust-source instead of /usr/share/pki

* Tue Apr 30 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-38
- Allow thumbnails to share memory with apps which run thumbnails
- Allow postfix-postqueue block_suspend
- Add lib interfaces for smsd
- Add support for nginx
- Allow s2s running as jabberd_t to connect to jabber_interserver_port_t
- Allow pki apache domain to create own tmp files and execute httpd_suexec
- Allow procmail to manger user tmp files/dirs/lnk_files
- Add virt_stream_connect_svirt() interface
- Allow dovecot-auth to execute bin_t
- Allow iscsid to request that kernel load a kernel module
- Add labeling support for /var/lib/mod_security
- Allow iw running as tuned_t to create netlink socket
- Dontaudit sys_tty_config for thumb_t
- Add labeling for nm-l2tp-service
- Allow httpd running as certwatch_t to open tcp socket
- Allow useradd to manager smsd lib files
- Allow useradd_t to add homedirs in /var/lib
- Fix typo in userdomain.te
- Cleanup userdom_read_home_certs
- Implement userdom_home_reader_certs_type to allow read certs also on encrypt /home with ecryptfs_t
- Allow staff to stream connect to svirt_t to make gnome-boxes working

* Fri Apr 26 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-37
- Allow lvm to create its own unit files
- Label /var/lib/sepolgen as selinux_config_t
- Add filetrans rules for tw devices
- Add transition from cupsd_config_t to cupsd_t

* Wed Apr 24 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-36
- Add filetrans rules for tw devices
- Cleanup bad transition lines

* Tue Apr 23 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-35
- Fix lockdev_manage_files()
- Allow setroubleshootd to read var_lib_t to make email_alert working
- Add lockdev_manage_files()
- Call proper interface in virt.te
- Allow gkeyring_domain to create /var/run/UID/config/dbus file
- system dbus seems to be blocking suspend
- Dontaudit attemps to sys_ptrace, which I believe gpsd does not need
- When you enter a container from root, you generate avcs with a leaked file descriptor
- Allow mpd getattr on file system directories
- Make sure realmd creates content with the correct label
- Allow systemd-tty-ask to write kmsg
- Allow mgetty to use lockdev library for device locking
- Fix selinuxuser_user_share_music boolean name to selinuxuser_share_music
- When you enter a container from root, you generate avcs with a leaked file descriptor
- Make sure init.fc files are labeled correctly at creation
- File name trans vconsole.conf
- Fix labeling for nagios plugins
- label shared libraries in /opt/google/chrome as testrel_shlib_t

* Thu Apr 18 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-34
- Allow certmonger to dbus communicate with realmd 
- Make realmd working

* Thu Apr 18 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-33
- Fix mozilla specification of homedir content
- Allow certmonger to read network state
- Allow tmpwatch to read tmp in /var/spool/{cups,lpd}
- Label all nagios plugin as unconfined by default
- Add httpd_serve_cobbler_files()
- Allow mdadm to read /dev/sr0 and create tmp files
- Allow certwatch to send mails
- Fix labeling for nagios plugins
- label shared libraries in /opt/google/chrome as testrel_shlib_t

* Wed Apr 17 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-32
- Allow realmd to run ipa, really needs to be an unconfined_domain
- Allow sandbox domains to use inherted terminals
- Allow pscd to use devices labeled svirt_image_t in order to use cat cards.
- Add label for new alsa pid
- Alsa now uses a pid file and needs to setsched 
- Fix oracleasmfs_t definition
- Add support for sshd_unit_file_t
- Add oracleasmfs_t
- Allow unlabeled_t files to be stored on unlabeled_t filesystems

* Tue Apr 16 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-31
- Fix description of deny_ptrace boolean
- Remove allow for execmod lib_t for now
- Allow quantum to connect to keystone port
- Allow nova-console to talk with mysql over unix stream socket
- Allow dirsrv to stream connect to uuidd
- thumb_t needs to be able to create ~/.cache if it does not exist
- virtd needs to be able to sys_ptrace when starting and stoping containers

* Mon Apr 15 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-30
- Allow alsa_t signal_perms, we probaly should search for any app that can execute something without transition and give it signal_perms...
- Add dontaudit for mozilla_plugin_t looking at the xdm_t sockets
- Fix deny_ptrace boolean, certain ptrace leaked into the system
- Allow winbind to manage kerberos_rcache_host
- Allow spamd to create spamd_var_lib_t directories
- Remove transition to mozilla_tmp_t by mozilla_t, to allow it to manage the users tmp dirs
- Add mising nslcd_dontaudit_write_sock_file() interface
- one more fix
- Fix pki_read_tomcat_lib_files() interface
- Allow certmonger to read pki-tomcat lib files
- Allow certwatch to execute bin_t
- Allow snmp to manage /var/lib/net-snmp files
- Call snmp_manage_var_lib_files(fogorn_t) instead of snmp_manage_var_dirs
- Fix vmware_role() interface
- Fix cobbler_manage_lib_files() interface
- Allow nagios check disk plugins to execute bin_t
- Allow quantum to transition to openvswitch_t
- Allow postdrop to stream connect to postfix-master
- Allow quantum to stream connect to openvswitch
- Add xserver_dontaudit_xdm_rw_stream_sockets() interface
- Allow daemon to send dgrams to initrc_t
- Allow kdm to start the power service to initiate a reboot or poweroff

* Thu Apr 11 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-29
- Add mising nslcd_dontaudit_write_sock_file() interface
- one more fix
- Fix pki_read_tomcat_lib_files() interface
- Allow certmonger to read pki-tomcat lib files
- Allow certwatch to execute bin_t
- Allow snmp to manage /var/lib/net-snmp files
- Don't audit attempts to write to stream socket of nscld by thumbnailers
- Allow git_system_t to read network state
- Allow pegasas to execute mount command
- Fix desc for drdb_admin
- Fix condor_amin()
- Interface fixes for uptime, vdagent, vnstatd
- Fix labeling for moodle in /var/www/moodle/data
- Add interface fixes
- Allow bugzilla to read certs
- /var/www/moodle needs to be writable by apache
- Add interface to dontaudit attempts to send dbus messages to systemd domains, for xguest
- Fix namespace_init_t to create content with proper labels, and allow it to manage all user content
- Allow httpd_t to connect to osapi_compute port using httpd_use_openstack bolean
- Fixes for dlm_controld
- Fix apache_read_sys_content_rw_dirs() interface
- Allow logrotate to read /var/log/z-push dir
- Fix sys_nice for cups_domain
- Allow postfix_postdrop to acces postfix_public socket
- Allow sched_setscheduler for cupsd_t
- Add missing context for /usr/sbin/snmpd
- Kernel_t needs mac_admin in order to support labeled NFS
- Fix systemd_dontaudit_dbus_chat() interface
- Add interface to dontaudit attempts to send dbus messages to systemd domains, for xguest
- Allow consolehelper domain to write Xauth files in /root
- Add port definition for osapi_compute port
- Allow unconfined to create /etc/hostname with correct labeling
- Add systemd_filetrans_named_hostname() interface

* Mon Apr 8 2013 Dan Walsh <dwalsh@redhat.com> 3.12.1-28
- Allow httpd_t to connect to osapi_compute port using httpd_use_openstack bolean
- Fixes for dlm_controld
- Fix apache_read_sys_content_rw_dirs() interface
- Allow logrotate to read /var/log/z-push dir
- Allow postfix_postdrop to acces postfix_public socket
- Allow sched_setscheduler for cupsd_t
- Add missing context for /usr/sbin/snmpd
- Allow consolehelper more access discovered by Tom London
- Allow fsdaemon to send signull to all domain
- Add port definition for osapi_compute port
- Allow unconfined to create /etc/hostname with correct labeling
- Add systemd_filetrans_named_hostname() interface

* Sat Apr 6 2013 Dan Walsh <dwalsh@redhat.com> 3.12.1-27
- Fix file_contexts.subs to label /run/lock correctly

* Fri Apr 5 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-26
- Try to label on controlC devices up to 30 correctly
- Add mount_rw_pid_files() interface
- Add additional mount/umount interfaces needed by mock
- fsadm_t sends audit messages in reads kernel_ipc_info when doing livecd-iso-to-disk
- Fix tabs
- Allow initrc_domain to search rgmanager lib files
- Add more fixes which make mock working together with confined users
  * Allow mock_t to manage rpm files
  * Allow mock_t to read rpm log files
  * Allow mock to setattr on tmpfs, devpts
  * Allow mount/umount filesystems
- Add rpm_read_log() interface
- yum-cron runs rpm from within it.
- Allow tuned to transition to dmidecode
- Allow firewalld to do net_admin
- Allow mock to unmont tmpfs_t
- Fix virt_sigkill() interface
- Add additional fixes for mock. Mainly caused by mount running in mock_t
- Allow mock to write sysfs_t and mount pid files
- Add mailman_domain to mailman_template()
- Allow openvswitch to execute shell
- Allow qpidd to use kerberos
- Allow mailman to use fusefs, needs back port to RHEL6
- Allow apache and its scripts to use anon_inodefs
- Add alias for git_user_content_t and git_sys_content_t so that RHEL6 will update to RHEL7
- Realmd needs to connect to samba ports, needs back port to F18 also
- Allow colord to read /run/initial-setup-
- Allow sanlock-helper to send sigkill to virtd which is registred to sanlock
- Add virt_kill() interface
- Add rgmanager_search_lib() interface
- Allow wdmd to getattr on all filesystems. Back ported from RHEL6

* Tue Apr 2 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-25
- Allow realmd to create tmp files
- FIx ircssi_home_t type to irssi_home_t
- Allow adcli running as realmd_t to connect to ldap port
- Allow NetworkManager to transition to ipsec_t, for running strongswan
- Make openshift_initrc_t an lxc_domain
- Allow gssd to manage user_tmp_t files
- Fix handling of irclogs in users homedir
- Fix labeling for drupal an wp-content in subdirs of /var/www/html
- Allow abrt to read utmp_t file
- Fix openshift policy to transition lnk_file, sock-file an fifo_file when created in a tmpfs_t, needs back port to RHEL6
- fix labeling for (oo|rhc)-restorer-wrapper.sh
- firewalld needs to be able to write to network sysctls
- Fix mozilla_plugin_dontaudit_rw_sem() interface
- Dontaudit generic ipc read/write to a mozilla_plugin for sandbox_x domains
- Add mozilla_plugin_dontaudit_rw_sem() interface
- Allow svirt_lxc_t to transition to openshift domains
- Allow condor domains block_suspend and dac_override caps
- Allow condor_master to read passd
- Allow condor_master to read system state
- Allow NetworkManager to transition to ipsec_t, for running strongswan
- Lots of access required by lvm_t to created encrypted usb device
- Allow xdm_t to dbus communicate with systemd_localed_t
- Label strongswan content as ipsec_exec_mgmt_t for now
- Allow users to dbus chat with systemd_localed
- Fix handling of .xsession-errors in xserver.if, so kde will work
- Might be a bug but we are seeing avc's about people status on init_t:service
- Make sure we label content under /var/run/lock as <<none>>
- Allow daemon and systemprocesses to search init_var_run_t directory
- Add boolean to allow xdm to write xauth data to the home directory
- Allow mount to write keys for the unconfined domain
- Add unconfined_write_keys() interface

* Tue Mar 26 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-24
- Add labeling for /usr/share/pki
- Allow programs that read var_run_t symlinks also read var_t symlinks
- Add additional ports as mongod_port_t for  27018, 27019, 28017, 28018 and 28019 ports
- Fix labeling for /etc/dhcp directory
- add missing systemd_stub_unit_file() interface
- Add files_stub_var() interface
- Add lables for cert_t directories
- Make localectl set-x11-keymap working at all
- Allow abrt to manage mock build environments to catch build problems.
- Allow virt_domains to setsched for running gdb on itself
- Allow thumb_t to execute user home content
- Allow pulseaudio running as mozilla_plugin_t to read /run/systemd/users/1000
- Allow certwatch to execut /usr/bin/httpd
- Allow cgred to send signal perms to itself, needs back port to RHEL6
- Allow openshift_cron_t to look at quota
- Allow cups_t to read inhered tmpfs_t from the kernel
- Allow yppasswdd to use NIS
- Tuned wants sys_rawio capability
- Add ftpd_use_fusefs boolean
- Allow dirsrvadmin_t to signal itself

* Wed Mar 20 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-23
- Allow localectl to read /etc/X11/xorg.conf.d directory
- Revert "Revert "Fix filetrans rules for kdm creates .xsession-errors""
- Allow mount to transition to systemd_passwd_agent
- Make sure abrt directories are labeled correctly
- Allow commands that are going to read mount pid files to search mount_var_run_t
- label /usr/bin/repoquery as rpm_exec_t
- Allow automount to block suspend
- Add abrt_filetrans_named_content so that abrt directories get labeled correctly
- Allow virt domains to setrlimit and read file_context

* Mon Mar 18 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-22
- Allow nagios to manage nagios spool files
- /var/spool/snmptt is a directory which snmdp needs to write to, needs back port to RHEL6
- Add swift_alias.* policy files which contain typealiases for swift types
- Add support for /run/lock/opencryptoki
- Allow pkcsslotd chown capability
- Allow pkcsslotd to read passwd
- Add rsync_stub() interface
- Allow systemd_timedate also manage gnome config homedirs
- Label /usr/lib64/security/pam_krb5/pam_krb5_cchelper as bin_t
- Fix filetrans rules for kdm creates .xsession-errors
- Allow sytemd_tmpfiles to create wtmp file
- Really should not label content  under /var/lock, since it could have labels on it different from var_lock_t
- Allow systemd to list all file system directories
- Add some basic stub interfaces which will be used in PRODUCT policies

* Wed Mar 13 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-21
- Fix log transition rule for cluster domains
- Start to group all cluster log together
- Dont use filename transition for POkemon Advanced Adventure until a new checkpolicy update
- cups uses usbtty_device_t devices
- These fixes were all required to build a MLS virtual Machine with single level desktops
- Allow domains to transiton using httpd_exec_t
- Allow svirt domains to manage kernel key rings
- Allow setroubleshoot to execute ldconfig
- Allow firewalld to read generate gnome data
- Allow bluetooth to read machine-info
- Allow boinc domain to send signal to itself
- Fix gnome_filetrans_home_content() interface
- Allow mozilla_plugins to list apache modules, for use with gxine
- Fix labels for POkemon in the users homedir
- Allow xguest to read mdstat
- Dontaudit virt_domains getattr on /dev/*
- These fixes were all required to build a MLS virtual Machine with single level desktops
- Need to back port this to RHEL6 for openshift
- Add tcp/8891 as milter port
- Allow nsswitch domains to read sssd_var_lib_t files
- Allow ping to read network state.
- Fix typo
- Add labels to /etc/X11/xorg.d and allow systemd-timestampd_t to manage them

* Fri Mar 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-20
- Adopt swift changes from lhh@redhat.com
- Add rhcs_manage_cluster_pid_files() interface
- Allow screen domains to configure tty and setup sock_file in ~/.screen directory
- ALlow setroubleshoot to read default_context_t, needed to backport to F18
- Label /etc/owncloud as being an apache writable directory
- Allow sshd to stream connect to an lxc domain

* Thu Mar 7 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-19
- Allow postgresql to manage rgmanager pid files
- Allow postgresql to read ccs data
- Allow systemd_domain to send dbus messages to policykit
- Add labels for /etc/hostname and /etc/machine-info and allow systemd-hostnamed to create them
- All systemd domains that create content are reading the file_context file and setfscreate
- Systemd domains need to search through init_var_run_t
- Allow sshd to communicate with libvirt to set containers labels
- Add interface to manage pid files
- Allow NetworkManger_t to read /etc/hostname
- Dontaudit leaked locked files into openshift_domains
- Add fixes for oo-cgroup-read - it nows creates tmp files
- Allow gluster to manage all directories as well as files
- Dontaudit chrome_sandbox_nacl_t using user terminals
- Allow sysstat to manage its own log files
- Allow virtual machines to setrlimit and send itself signals.
- Add labeling for /var/run/hplip

* Mon Mar 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-18
- Fix POSTIN scriptlet

* Fri Mar 1 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-17
- Merge rgmanger, corosync,pacemaker,aisexec policies to cluster_t in rhcs.pp

* Wed Feb 27 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-16
- Fix authconfig.py labeling
- Make any domains that write homedir content do it correctly
- Allow glusterd to read/write anyhwere on the file system by default
- Be a little more liberal with the rsync log files
- Fix iscsi_admin interface
- Allow iscsid_t to read /dev/urand
- Fix up iscsi domain for use with unit files
- Add filename transition support for spamassassin policy
- Allow web plugins to use badly formated libraries
- Allow nmbd_t to create samba_var_t directories
- Add filename transition support for spamassassin policy
- Add filename transition support for tvtime
- Fix alsa_home_filetrans_alsa_home() interface
- Move all userdom_filetrans_home_content() calling out of booleans
- Allow logrotote to getattr on all file sytems
- Remove duplicate userdom_filetrans_home_content() calling
- Allow kadmind to read /etc/passwd
- Dontaudit append .xsession-errors file on ecryptfs for  policykit-auth
- Allow antivirus domain to manage antivirus db links
- Allow logrotate to read /sys
- Allow mandb to setattr on man dirs
- Remove mozilla_plugin_enable_homedirs boolean
- Fix ftp_home_dir boolean
- homedir mozilla filetrans has been moved to userdom_home_manager
- homedir telepathy filetrans has been moved to userdom_home_manager
- Remove gnome_home_dir_filetrans() from gnome_role_gkeyringd()
- Might want to eventually write a daemon on fusefsd.
- Add policy fixes for sshd [net] child from plautrba@redhat.com
- Tor uses a new port
- Remove bin_t for authconfig.py
- Fix so only one call to userdom_home_file_trans
- Allow home_manager_types to create content with the correctl label
- Fix all domains that write data into the homedir to do it with the correct label
- Change the postgresql to use proper boolean names, which is causing httpd_t to
- not get access to postgresql_var_run_t
- Hostname needs to send syslog messages
- Localectl needs to be able to send dbus signals to users
- Make sure userdom_filetrans_type will create files/dirs with user_home_t labeling by default
- Allow user_home_manger domains to create spam* homedir content with correct labeling
- Allow user_home_manger domains to create HOMEDIR/.tvtime with correct labeling
- Add missing miscfiles_setattr_man_pages() interface and for now comment some rules for userdom_filetrans_type to make build process working
- Declare userdom_filetrans_type attribute
- userdom_manage_home_role() needs to be called withoout usertype attribute because of userdom_filetrans_type attribute
- fusefsd is mounding a fuse file system on /run/user/UID/gvfs

* Thu Feb 21 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-15
- Man pages are now generated in the build process
- Allow cgred to list inotifyfs filesystem

* Wed Feb 20 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-14
- Allow gluster to get attrs on all fs
- New access required for virt-sandbox
- Allow dnsmasq to execute bin_t
- Allow dnsmasq to create content in /var/run/NetworkManager
- Fix openshift_initrc_signal() interface
- Dontaudit openshift domains doing getattr on other domains
- Allow consolehelper domain to communicate with session bus
- Mock should not be transitioning to any other domains,  we should keep mock_t as mock_t
- Update virt_qemu_ga_t policy
- Allow authconfig running from realmd to restart oddjob service
- Add systemd support for oddjob
- Add initial policy for realmd_consolehelper_t which if for authconfig executed by realmd
- Add labeling for gnashpluginrc
- Allow chrome_nacl to execute /dev/zero
- Allow condor domains to read /proc
- mozilla_plugin_t will getattr on /core if firefox crashes
- Allow condor domains to read /etc/passwd
- Allow dnsmasq to execute shell scripts, openstack requires this access
- Fix glusterd labeling
- Allow virtd_t to interact with the socket type
- Allow nmbd_t to override dac if you turned on sharing all files
- Allow tuned to created kobject_uevent socket
- Allow guest user to run fusermount
- Allow openshift to read /proc and locale
- Allow realmd to dbus chat with rpm
- Add new interface for virt
- Remove depracated interfaces
- Allow systemd_domains read access on etc, etc_runtime and usr files, also allow them to connect stream to syslog socket
- /usr/share/munin/plugins/plugin.sh should be labeled as bin_t
- Remove some more unconfined_t process transitions, that I don't believe are necessary
- Stop transitioning uncofnined_t to checkpc
- dmraid creates /var/lock/dmraid
- Allow systemd_localed to creatre unix_dgram_sockets
- Allow systemd_localed to write kernel messages.
- Also cleanup systemd definition a little.
- Fix userdom_restricted_xwindows_user_template() interface
- Label any block devices or char devices under /dev/infiniband as fixed_disk_device_t
- User accounts need to dbus chat with accountsd daemon
- Gnome requires all users to be able to read /proc/1/

* Thu Feb 14 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-13
- virsh now does a setexeccon call
- Additional rules required by openshift domains
- Allow svirt_lxc_domains to use inherited terminals, needed to make virt-sandbox-service execute work
- Allow spamd_update_t to search spamc_home_t
- Avcs discovered by mounting an isci device under /mnt
- Allow lspci running as logrotate to read pci.ids
- Additional fix for networkmanager_read_pid_files()
- Fix networkmanager_read_pid_files() interface
- Allow all svirt domains to connect to svirt_socket_t
- Allow virsh to set SELinux context for a process.
- Allow tuned to create netlink_kobject_uevent_socket
- Allow systemd-timestamp to set SELinux context
- Add support for /var/lib/systemd/linger
- Fix ssh_sysadm_login to be working on MLS as expected

* Mon Feb 11 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-12
- Rename files_rw_inherited_tmp_files to files_rw_inherited_tmp_file
- Add missing files_rw_inherited_tmp_files interface
- Add additional interface for ecryptfs
- ALlow nova-cert to connect to postgresql
- Allow keystone to connect to postgresql
- Allow all cups domains to getattr on filesystems
- Allow pppd to send signull
- Allow tuned to execute ldconfig
- Allow gpg to read fips_enabled
- Add additional fixes for ecryptfs
- Allow httpd to work with posgresql
- Allow keystone getsched and setsched

* Fri Feb 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-11
- Allow gpg to read fips_enabled
- Add support for /var/cache/realmd
- Add support for /usr/sbin/blazer_usb and systemd support for nut
- Add labeling for fenced_sanlock and allow sanclok transition to fenced_t
- bitlbee wants to read own log file
- Allow glance domain to send a signal itself
- Allow xend_t to request that the kernel load a kernel module
- Allow pacemaker to execute heartbeat lib files
- cleanup new swift policy

* Tue Feb 5 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-10
- Fix smartmontools
- Fix userdom_restricted_xwindows_user_template() interface
- Add xserver_xdm_ioctl_log() interface
- Allow Xusers to ioctl lxdm.log to make lxdm working
- Add MLS fixes to make MLS boot/log-in working
- Add mls_socket_write_all_levels() also for syslogd
- fsck.xfs needs to read passwd
- Fix ntp_filetrans_named_content calling in init.te
- Allow postgresql to create pg_log dir
- Allow sshd to read rsync_data_t to make rsync <backuphost> working
- Change ntp.conf to be labeled net_conf_t
- Allow useradd to create homedirs in /run.  ircd-ratbox does this and we should just allow it
- Allow xdm_t to execute gstreamer home content
- Allod initrc_t and unconfined domains, and sysadm_t to manage ntp
- New policy for openstack swift domains
- More access required for openshift_cron_t
- Use cupsd_log_t instead of cupsd_var_log_t
- rpm_script_roles should be used in rpm_run
- Fix rpm_run() interface
- Fix openshift_initrc_run()
- Fix sssd_dontaudit_stream_connect() interface
- Fix sssd_dontaudit_stream_connect() interface
- Allow LDA's job to deliver mail to the mailbox
- dontaudit block_suspend for mozilla_plugin_t
- Allow l2tpd_t to all signal perms
- Allow uuidgen to read /dev/random
- Allow mozilla-plugin-config to read power_supply info
- Implement cups_domain attribute for cups domains
- We now need access to user terminals since we start by executing a command outside the tty
- We now need access to user terminals since we start by executing a command outside the tty
- svirt lxc containers want to execute userhelper apps, need these changes to allow this to happen
- Add containment of openshift cron jobs
- Allow system cron jobs to create tmp directories
- Make userhelp_conf_t a config file
- Change rpm to use rpm_script_roles
- More fixes for rsync to make rsync <backuphost> wokring
- Allow logwatch to domtrans to mdadm
- Allow pacemaker to domtrans to ifconfig
- Allow pacemaker to setattr on corosync.log
- Add pacemaker_use_execmem for memcheck-amd64 command
- Allow block_suspend capability
- Allow create fifo_file in /tmp with pacemaker_tmp_t
- Allow systat to getattr on fixed disk
- Relabel /etc/ntp.conf to be net_conf_t
- ntp_admin should create files in /etc with the correct label
- Add interface to create ntp_conf_t files in /etc
- Add additional labeling for quantum
- Allow quantum to execute dnsmasq with transition

* Wed Jan 30 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-9
- boinc_cliean wants also execmem as boinc projecs have
- Allow sa-update to search admin home for /root/.spamassassin
- Allow sa-update to search admin home for /root/.spamassassin
- Allow antivirus domain to read net sysctl
- Dontaudit attempts from thumb_t to connect to ssd
- Dontaudit attempts by readahead to read sock_files
- Dontaudit attempts by readahead to read sock_files
- Create tmpfs file while running as wine as user_tmpfs_t
- Dontaudit attempts by readahead to read sock_files
- libmpg ships badly created librarie

* Mon Jan 28 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-8
- Change ssh_use_pts to use macro and only inherited sshd_devpts_t
- Allow confined users to read systemd_logind seat information
- libmpg ships badly created libraries
- Add support for strongswan.service
- Add labeling for strongswan
- Allow l2tpd_t to read network manager content in /run directory
- Allow rsync to getattr any file in rsync_data_t
- Add labeling and filename transition for .grl-podcasts

* Fri Jan 25 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-7
- mount.glusterfs executes glusterfsd binary
- Allow systemd_hostnamed_t to stream connect to systemd
- Dontaudit any user doing a access check
- Allow obex-data-server to request the kernel to load a module
- Allow gpg-agent to manage gnome content (~/.cache/gpg-agent-info)
- Allow gpg-agent to read /proc/sys/crypto/fips_enabled
- Add new types for antivirus.pp policy module
- Allow gnomesystemmm_t caps because of ioprio_set
- Make sure if mozilla_plugin creates files while in permissive mode, they get created with the correct label, user_home_t
- Allow gnomesystemmm_t caps because of ioprio_set
- Allow NM rawip socket
- files_relabel_non_security_files can not be used with boolean
- Add interface to thumb_t dbus_chat to allow it to read remote process state
- ALlow logrotate to domtrans to mdadm_t
- kde gnomeclock wants to write content to /tmp

* Wed Jan 23 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-6
- kde gnomeclock wants to write content to /tmp
- /usr/libexec/kde4/kcmdatetimehelper attempts to create /root/.kde
- Allow blueman_t to rwx zero_device_t, for some kind of jre
- Allow mozilla_plugin_t to rwx zero_device_t, for some kind of jre
- Ftp full access should be allowed to create directories as well as files
- Add boolean to allow rsync_full_acces, so that an rsync server can write all
- over the local machine
- logrotate needs to rotate logs in openshift directories, needs back port to RHEL6
- Add missing vpnc_roles type line
- Allow stapserver to write content in /tmp
- Allow gnome keyring to create keyrings dir in ~/.local/share
- Dontaudit thumb drives trying to bind to udp sockets if nis_enabled is turned on
- Add interface to colord_t dbus_chat to allow it to read remote process state
- Allow colord_t to read cupsd_t state
- Add mate-thumbnail-font as thumnailer
- Allow sectoolm to sys_ptrace since it is looking at other proceses /proc data.
- Allow qpidd to list /tmp. Needed by ssl
- Only allow init_t to transition to rsync_t domain, not initrc_t.  This should be back ported to F17, F18
- - Added systemd support for ksmtuned
- Added booleans
 	ksmtuned_use_nfs
 	ksmtuned_use_cifs
- firewalld seems to be creating mmap files which it needs to execute in /run /tmp and /dev/shm.  Would like to clean this up but for now we will allow
- Looks like qpidd_t needs to read /dev/random
- Lots of probing avc's caused by execugting gpg from staff_t
- Dontaudit senmail triggering a net_admin avc
- Change thumb_role to use thumb_run, not sure why we have a thumb_role, needs back port
- Logwatch does access check on mdadm binary
- Add raid_access_check_mdadm() iterface

* Wed Jan 16 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-5
- Fix systemd_manage_unit_symlinks() interface
- Call systemd_manage_unit_symlinks(() which is correct interface
- Add filename transition for opasswd
- Switch gnomeclock_dbus_chat to systemd_dbus_chat_timedated since we have switched the name of gnomeclock
- Allow sytstemd-timedated to get status of init_t
- Add new systemd policies for hostnamed and rename gnomeclock_t to systemd_timedate_t
- colord needs to communicate with systemd and systemd_logind, also remove duplicate rules
- Switch gnomeclock_dbus_chat to systemd_dbus_chat_timedated since we have switched the name of gnomeclock
- Allow gpg_t to manage all gnome files
- Stop using pcscd_read_pub_files
- New rules for xguest, dontaudit attempts to dbus chat
- Allow firewalld to create its mmap files in tmpfs and tmp directories
- Allow firewalld to create its mmap files in tmpfs and tmp directories
- run unbound-chkconf as named_t, so it can read dnssec
- Colord is reading xdm process state, probably reads state of any apps that sends dbus message
- Allow mdadm_t to change the kernel scheduler
- mythtv policy
- Update mandb_admin() interface
- Allow dsspam to listen on own tpc_socket
- seutil_filetrans_named_content needs to be optional
- Allow sysadm_t to execute content in his homedir
- Add attach_queue to tun_socket, new patch from Paul Moore
- Change most of selinux configuration types to security_file_type.
- Add filename transition rules for selinux configuration
- ssh into a box with -X -Y requires ssh_use_ptys
- Dontaudit thumb drives trying to bind to udp sockets if nis_enabled is turned on
- Allow all unpriv userdomains to send dbus messages to hostnamed and timedated
- New allow rules found by Tom London for systemd_hostnamed

* Mon Jan 14 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-4
- Allow systemd-tmpfiles to relabel lpd spool files
- Ad labeling for texlive bash scripts
- Add xserver_filetrans_fonts_cache_home_content() interface
- Remove duplicate rules from *.te
- Add support for /var/lock/man-db.lock
- Add support for /var/tmp/abrt(/.*)?
- Add additional labeling for munin cgi scripts
- Allow httpd_t to read munin conf files
- Allow certwatch to read meminfo
- Fix nscd_dontaudit_write_sock_file() interfac
- Fix gnome_filetrans_home_content() to include also "fontconfig" dir as cache_home_t
- llow mozilla_plugin_t to create HOMEDIR/.fontconfig with the proper labeling 

* Fri Jan 11 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-3
- Allow gnomeclock to talk to puppet over dbus
- Allow numad access discovered by Dominic
- Add support for HOME_DIR/.maildir
- Fix attribute_role for mozilla_plugin_t domain to allow staff_r to access this domain
- Allow udev to relabel udev_var_run_t lnk_files
- New bin_t file in mcelog

* Thu Jan 10 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-2
- Remove all mcs overrides and replace with t1 != mcs_constrained_types
- Add attribute_role for iptables
- mcs_process_set_categories needs to be called for type
- Implement additional role_attribute statements
- Sodo domain is attempting to get the additributes of proc_kcore_t
- Unbound uses port 8953
- Allow svirt_t images to compromise_kernel when using pci-passthrough
- Add label for dns lib files
- Bluetooth aquires a dbus name
- Remove redundant files_read_usr_file calling
- Remove redundant files_read_etc_file calling
- Fix mozilla_run_plugin()
- Add role_attribute support for more domains

* Wed Jan 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-1
- Mass merge with upstream

* Sat Jan 5 2013 Dan Walsh <dwalsh@redhat.com> 3.11.1-69.1
- Bump the policy version to 28 to match selinux userspace
- Rebuild versus latest libsepol

* Wed Jan 2 2013 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-69
- Add systemd_status_all_unit_files() interface
- Add support for nshadow
- Allow sysadm_t to administrate the postfix domains
- Add interface to setattr on isid directories for use by tmpreaper
- Allow sshd_t sys_admin for use with afs logins
- Allow systemd to read/write all sysctls
- Allow sshd_t sys_admin for use with afs logins
- Allow systemd to read/write all sysctls
- Add systemd_status_all_unit_files() interface
- Add support for nshadow
- Allow sysadm_t to administrate the postfix domains
- Add interface to setattr on isid directories for use by tmpreaper
- Allow sshd_t sys_admin for use with afs logins
- Allow systemd to read/write all sysctls
- Allow sshd_t sys_admin for use with afs logins
- Add labeling for /var/named/chroot/etc/localtim

* Thu Dec 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-68
- Allow setroubleshoot_fixit to execute rpm
- zoneminder needs to connect to httpd ports where remote cameras are listening
- Allow firewalld to execute content created in /run directory
- Allow svirt_t to read generic certs
- Dontaudit leaked ps content to mozilla plugin
- Allow sshd_t sys_admin for use with afs logins
- Allow systemd to read/write all sysctls
- init scripts are creating systemd_unit_file_t directories

* Fri Dec 21 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-67
- systemd_logind_t is looking at all files under /run/user/apache
- Allow systemd to manage all user tmp files
- Add labeling for /var/named/chroot/etc/localtime
- Allow netlabel_peer_t type to flow over netif_t and node_t, and only be hindered by MLS, need back port to RHEL6
- Keystone is now using a differnt port
- Allow xdm_t to use usbmuxd daemon to control sound
- Allow passwd daemon to execute gnome_exec_keyringd
- Fix chrome_sandbox policy
- Add labeling for /var/run/checkquorum-timer
- More fixes for the dspam domain, needs back port to RHEL6
- More fixes for the dspam domain, needs back port to RHEL6
- sssd needs to connect to kerberos password port if a user changes his password
- Lots of fixes from RHEL testing of dspam web
- Allow chrome and mozilla_plugin to create msgq and semaphores
- Fixes for dspam cgi scripts
- Fixes for dspam cgi scripts
- Allow confine users to ptrace screen
- Backport virt_qemu_ga_t changes from RHEL
- Fix labeling for dspam.cgi needed for RHEL6
- We need to back port this policy to RHEL6, for lxc domains
- Dontaudit attempts to set sys_resource of logrotate
- Allow corosync to read/write wdmd's tmpfs files
- I see a ptrace of mozilla_plugin_t by staff_t, will allow without deny_ptrace being set
- Allow cron jobs to read bind config for unbound
- libvirt needs to inhibit systemd
- kdumpctl needs to delete boot_t files
- Fix duplicate gnome_config_filetrans
- virtd_lxc_t is using /dev/fuse
- Passenger needs to create a directory in /var/log, needs a backport to RHEL6 for openshift
- apcupsd can be setup to listen to snmp trafic
- Allow transition from kdumpgui to kdumpctl
- Add fixes for munin CGI scripts
- Allow deltacloud to connect to openstack at the keystone port
- Allow domains that transition to svirt domains to be able to signal them
- Fix file context of gstreamer in .cache directory
- libvirt is communicating with logind
- NetworkManager writes to the systemd inhibit pipe

* Mon Dec 17 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-66
- Allow munin disk plugins to get attributes of all directories
- Allow munin disk plugins to get attributes of all directorie
- Allow logwatch to get attributes of all directories
- Fix networkmanager_manage_lib() interface
- Fix gnome_manage_config() to allow to manage sock_file
- Fix virtual_domain_context
- Add support for dynamic DNS for DHCPv6

* Sat Dec 15 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-65
- Allow svirt to use netlink_route_socket which was a part of auth_use_nsswitch
- Add additional labeling for /var/www/openshift/broker
- Fix rhev policy
- Allow openshift_initrc domain to dbus chat with systemd_logind
- Allow httpd to getattr passenger log file if run_stickshift
- Allow consolehelper-gtk to connect to xserver
- Add labeling for the tmp-inst directory defined in pam_namespace.conf
- Add lvm_metadata_t labeling for /etc/multipath

* Fri Dec 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-64
- consoletype is no longer used

* Wed Dec 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-63
- Add label for efivarfs
- Allow certmonger to send signal to itself
- Allow plugin-config to read own process status
- Add more fixes for pacemaker
- apache/drupal can run clamscan on uploaded content
- Allow chrome_sandbox_nacl_t to read pid 1 content

* Tue Dec 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-62
- Fix MCS Constraints to control ingres and egres controls on the network.
- Change name of svirt_nokvm_t to svirt_tcg_t
- Allow tuned to request the kernel to load kernel modules

* Mon Dec 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-61
- Label /var/lib/pgsql/.ssh as ssh_home_t
- Add labeling for /usr/bin/pg_ctl
- Allow systemd-logind to manage keyring user tmp dirs
- Add support for 7389/tcp port
- gems seems to be placed in lots of places
- Since xdm is running a full session, it seems to be trying to execute lots of executables via dbus
- Add back tcp/8123 port as http_cache port
- Add ovirt-guest-agent\.pid labeling
- Allow xend to run scsi_id
- Allow rhsmcertd-worker to read "physical_package_id"
- Allow pki_tomcat to connect to ldap port
- Allow lpr to read /usr/share/fonts
- Allow open file from CD/DVD drive on domU
- Allow munin services plugins to talk to SSSD
- Allow all samba domains to create samba directory in var_t directories
- Take away svirt_t ability to use nsswitch
- Dontaudit attempts by openshift to read apache logs
- Allow apache to create as well as append _ra_content_t
- Dontaudit sendmail_t reading a leaked file descriptor
- Add interface to have admin transition /etc/prelink.cache to the proper label
- Add sntp support to ntp policy
- Allow firewalld to dbus chat with devicekit_power
- Allow tuned to call lsblk
- Allow tor to read /proc/sys/kernel/random/uuid
- Add tor_can_network_relay boolean  

* Wed Dec 5 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-60
- Add openshift_initrc_signal() interface
- Fix typos
- dspam port is treat as spamd_port_t
- Allow setroubleshoot to getattr on all executables
- Allow tuned to execute profiles scripts in /etc/tuned
- Allow apache to create directories to store its log files
- Allow all directories/files in /var/log starting with passenger to be labeled passenger_log_t
- Looks like apache is sending sinal to openshift_initrc_t now,needs back port to RHEL6
- Allow Postfix to be configured to listen on TCP port 10026 for email from DSPAM
- Add filename transition for /etc/tuned/active_profile
- Allow condor_master to send mails
- Allow condor_master to read submit.cf
- Allow condor_master to create /tmp files/dirs
- Allow condor_mater to send sigkill to other condor domains
- Allow condor_procd sigkill capability
- tuned-adm wants to talk with tuned daemon
- Allow kadmind and krb5kdc to also list sssd_public_t
- Allow accountsd to dbus chat with init
- Fix git_read_generic_system_content_files() interface
- pppd wants sys_nice by nmcli because of "syscall=sched_setscheduler"
- Fix mozilla_plugin_can_network_connect to allow to connect to all ports
- Label all munin plugins which are not covered by munin plugins policy  as unconfined_munin_plugin_exec_t
- dspam wants to search /var/spool for opendkim data
- Revert "Add support for tcp/10026 port as dspam_port_t"
- Turning on labeled networking requires additional access for netlabel_peer_t; these allow rules need to be back ported to RHEL6
- Allow all application domains to use fifo_files passed in from userdomains, also allow them to write to tmp_files inherited from userdomain
- Allow systemd_tmpfiles_t to setattr on mandb_cache_t

* Sat Dec 1 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-59
- consolekit.pp was not removed from the postinstall script

* Fri Nov 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-58
- Add back consolekit policy
- Silence bootloader trying to use inherited tty
- Silence xdm_dbusd_t trying to execute telepathy apps
- Fix shutdown avcs when machine has unconfined.pp disabled
- The host and a virtual machine can share the same printer on a usb device
- Change oddjob to transition to a ranged openshift_initr_exec_t when run from oddjob
- Allow abrt_watch_log_t to execute bin_t
- Allow chrome sandbox to write content in ~/.config/chromium
- Dontaudit setattr on fontconfig dir for thumb_t
- Allow lircd to request the kernel to load module
- Make rsync as userdom_home_manager
- Allow rsync to search automount filesystem
- Add fixes for pacemaker

* Wed Nov 28 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-57
- Add support for 4567/tcp port
- Random fixes from Tuomo Soini
- xdm wants to get init status
- Allow programs to run in fips_mode
- Add interface to allow the reading of all blk device nodes
- Allow init to relabel rpcbind sock_file
- Fix labeling for lastlog and faillog related to logrotate
- ALlow aeolus_configserver to use TRAM port
- Add fixes for aeolus_configserver
- Allow snmpd to connect to snmp port
- Allow spamd_update to create spamd_var_lib_t directories
- Allow domains that can read sssd_public_t files to also list the directory
- Remove miscfiles_read_localization, this is defined for all domains

* Mon Nov 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-56
- Allow syslogd to request the kernel to load a module
- Allow syslogd_t to read the network state information
- Allow xdm_dbusd_t connect to the system DBUS
- Add support for 7389/tcp port
- Allow domains to read/write all inherited sockets
- Allow staff_t to read kmsg
- Add awstats_purge_apache_log boolean
- Allow ksysguardproces to read /.config/Trolltech.conf
- Allow passenger to create and append puppet log files
- Add puppet_append_log and puppet_create_log interfaces
- Add puppet_manage_log() interface
- Allow tomcat domain to search tomcat_var_lib_t
- Allow pki_tomcat_t to connect to pki_ca ports
- Allow pegasus_t to have net_admin capability
- Allow pegasus_t to write /sys/class/net/<interface>/flags
- Allow mailserver_delivery to manage mail_home_rw_t lnk_files
- Allow fetchmail to create log files
- Allow gnomeclock to manage home config in .kde
- Allow bittlebee to read kernel sysctls
- Allow logrotate to list /root

* Mon Nov 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-55
- Fix userhelper_console_role_template()
- Allow enabling Network Access Point service using blueman
- Make vmware_host_t as unconfined domain
- Allow authenticate users in webaccess via squid, using mysql as backend
- Allow gathers to get various metrics on mounted file systems
- Allow firewalld to read /etc/hosts
- Fix cron_admin_role() to make sysadm cronjobs running in the sysadm_t instead of cronjob_t
- Allow kdumpgui to read/write to zipl.conf
- Commands needed to get mock to build from staff_t in enforcing mode
- Allow mdadm_t to manage cgroup files
- Allow all daemons and systemprocesses to use inherited initrc_tmp_t files
- dontaudit ifconfig_t looking at fifo_files that are leaked to it
- Add lableing for Quest Authentication System

* Thu Nov 15 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-54
- Fix filetrans interface definitions
- Dontaudit xdm_t to getattr on BOINC lib files
- Add systemd_reload_all_services() interface
- Dontaudit write access on /var/lib/net-snmp/mib_indexes 
- Only stop mcsuntrustedproc from relableing files
- Allow accountsd to dbus chat with gdm
- Allow realmd to getattr on all fs
- Allow logrotate to reload all services
- Add systemd unit file for radiusd
- Allow winbind to create samba pid dir
- Add labeling for /var/nmbd/unexpected
- Allow chrome and mozilla plugin to connect to msnp ports

* Mon Nov 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-53
- Fix storage_rw_inherited_fixed_disk_dev() to cover also blk_file
- Dontaudit setfiles reading /dev/random
- On initial boot gnomeclock is going to need to be set buy gdm
- Fix tftp_read_content() interface
- Random apps looking at kernel file systems
- Testing virt with lxc requiers additional access for virsh_t
- New allow rules requied for latest libvirt, libvirt talks directly to journald,lxc setup tool needs compromize_kernel,and we need ipc_lock in the container
- Allow MPD to read /dev/radnom
- Allow sandbox_web_type to read logind files which needs to read pulseaudio
- Allow mozilla plugins to read /dev/hpet
- Add labeling for /var/lib/zarafa-webap
- Allow BOINC client to use an HTTP proxy for all connections
- Allow rhsmertd to domain transition to dmidecod
-  Allow setroubleshootd to send D-Bus msg to ABRT

* Thu Nov 8 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-52
- Define usbtty_device_t as a term_tty
- Allow svnserve to accept a connection
- Allow xend manage default virt_image_t type
- Allow prelink_cron_system_t to overide user componant when executing cp
- Add labeling for z-push
- Gnomeclock sets the realtime clock
- Openshift seems to be storing apache logs in /var/lib/openshift/.log/httpd
- Allow lxc domains to use /dev/random and /dev/urandom

* Wed Nov 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-51
- Add port defintion for tcp/9000
- Fix labeling for /usr/share/cluster/checkquorum to label also checkquorum.wdmd
- Add rules and labeling for $HOME/cache/\.gstreamer-.* directory
- Add support for CIM provider openlmi-networking which uses NetworkManager dbus API
- Allow shorewall_t to create netlink_socket
- Allow krb5admind to block suspend
- Fix labels on /var/run/dlm_controld /var/log/dlm_controld
- Allow krb5kdc to block suspend
- gnomessytemmm_t needs to read /etc/passwd
- Allow cgred to read all sysctls

* Tue Nov 6 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-50
- Allow all domains to read /proc/sys/vm/overcommit_memory
- Make proc_numa_t an MLS Trusted Object
- Add /proc/numactl support for confined users
- Allow ssh_t to connect to any port > 1023
- Add openvswitch domain
- Pulseaudio tries to create directories in gnome_home_t directories
- New ypbind pkg wants to search /var/run which is caused by sd_notify
- Allow NM to read certs on NFS/CIFS using use_nfs_*, use_samba_* booleans
- Allow sanlock to read /dev/random
- Treat php-fpm with httpd_t
- Allow domains that can read named_conf_t to be able to list the directories
- Allow winbind to create sock files in /var/run/samba

* Thu Nov 1 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-49
- Add smsd policy
- Add support for OpenShift sbin labelin
- Add boolean to allow virt to use rawip
- Allow mozilla_plugin to read all file systems with noxattrs support
- Allow kerberos to write on anon_inodefs fs
- Additional access required by fenced
- Add filename transitions for passwd.lock/group.lock
- UPdate man pages
- Create coolkey directory in /var/cache with the correct label

* Tue Oct 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-48
- Fix label on /etc/group.lock
- Allow gnomeclock to create lnk_file in /etc
- label /root/.pki as a home_cert_t
- Add interface to make sure rpcbind.sock is created with the correct label
- Add definition for new directory /var/lib/os-probe and bootloader wants to read udev rules
- opendkim should be a part of milter
- Allow libvirt to set the kernel sched algorythm
- Allow mongod to read sysfs_t
- Add authconfig policy
- Remove calls to miscfiles_read_localization all domains get this
- Allow virsh_t to read /root/.pki/ content
- Add label for log directory under /var/www/stickshift

* Mon Oct 29 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-47
- Allow getty to setattr on usb ttys
- Allow sshd to search all directories for sshd_home_t content
- Allow staff domains to send dbus messages to kdumpgui
- Fix labels on /etc/.pwd.lock and friends to be passwd_file_t
- Dontaudit setfiles reading urand
- Add files_dontaudit_list_tmp() for domains to which we added sys_nice/setsched
- Allow staff_gkeyringd_t to read /home/$USER/.local/share/keyrings dir
- Allow systemd-timedated to read /dev/urandom
- Allow entropyd_t to read proc_t (meminfo)
- Add unconfined munin plugin
- Fix networkmanager_read_conf() interface
- Allow blueman to list /tmp which is needed by sys_nic/setsched
- Fix label of /etc/mail/aliasesdb-stamp
- numad is searching cgroups
- realmd is communicating with networkmanager using dbus
- Lots of fixes to try to get kdump to work

* Fri Oct 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-46
- Allow loging programs to dbus chat with realmd
- Make apache_content_template calling as optional
- realmd is using policy kit

* Fri Oct 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-45
- Add new selinuxuser_use_ssh_chroot boolean
- dbus needs to be able to read/write inherited fixed disk device_t passed through it
- Cleanup netutils process allow rule
- Dontaudit leaked fifo files from openshift to ping
- sanlock needs to read mnt_t lnk files
- Fail2ban needs to setsched and sys_nice

* Wed Oct 24 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-44
- Change default label of all files in /var/run/rpcbind
- Allow sandbox domains (java) to read hugetlbfs_t
- Allow awstats cgi content to create tmp files and read apache log files
- Allow setuid/setgid for cupsd-config
- Allow setsched/sys_nice pro cupsd-config
-  Fix /etc/localtime sym link to be labeled locale_t
- Allow sshd to search postgresql db t since this is a homedir
- Allow xwindows users to chat with realmd
- Allow unconfined domains to configure all files and null_device_t service

* Tue Oct 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-43
- Adopt pki-selinux policy

* Mon Oct 22 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-42
- pki is leaking which we dontaudit until a pki code fix
- Allow setcap for arping
- Update man pages
- Add labeling for /usr/sbin/mcollectived
- pki fixes
- Allow smokeping to execute fping in the netutils_t domain

* Fri Oct 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-41
- Allow mount to relabelfrom unlabeled file systems
- systemd_logind wants to send and receive messages from devicekit disk over dbus to make connected mouse working
- Add label to get bin files under libreoffice labeled correctly
- Fix interface to allow executing of base_ro_file_type
- Add fixes for realmd
- Update pki policy
- Add tftp_homedir boolean
- Allow blueman sched_setscheduler
- openshift user domains wants to r/w ssh tcp sockets

* Wed Oct 17 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-40
- Additional requirements for disable unconfined module when booting
- Fix label of systemd script files
- semanage can use -F /dev/stdin to get input
- syslog now uses kerberos keytabs
- Allow xserver to compromise_kernel access
-  Allow nfsd to write to mount_var_run_t when running the mount command
- Add filename transition rule for bin_t directories
- Allow files to read usr_t lnk_files
- dhcpc wants chown
- Add support for new openshift labeling
- Clean up for tunable+optional statements
- Add labeling for /usr/sbin/mkhomedir_helper
- Allow antivirus domain to managa amavis spool files
- Allow rpcbind_t to read passwd 
- Allow pyzor running as spamc to manage amavis spool

* Tue Oct 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-39
- Add interfaces to read kernel_t proc info
- Missed this version of exec_all
- Allow anyone who can load a kernel module to compromise kernel
- Add oddjob_dbus_chat to openshift apache policy
- Allow chrome_sandbox_nacl_t to send signals to itself
- Add unit file support to usbmuxd_t
- Allow all openshift domains to read sysfs info
- Allow openshift domains to getattr on all domains

* Fri Oct 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-38
- MLS fixes from Dan
- Fix name of capability2 secure_firmware->compromise_kerne

* Thu Oct 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-37
- Allow xdm to search all file systems
- Add interface to allow the config of all files
- Add rngd policy
- Remove kgpg as a gpg_exec_t type
- Allow plymouthd to block suspend
- Allow systemd_dbus to config any file
- Allow system_dbus_t to configure all services
- Allow freshclam_t to read usr_files
- varnishd requires execmem to load modules

* Thu Oct 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-36
- Allow semanage to verify types
- Allow sudo domain to execute user home files
- Allow session_bus_type to transition to user_tmpfs_t
- Add dontaudit caused by yum updates
- Implement pki policy but not activated

* Wed Oct 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-35
- tuned wants to getattr on all filesystems
- tuned needs also setsched. The build is needed for test day

* Wed Oct 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-34
- Add policy for qemu-qa
- Allow razor to write own config files
-  Add an initial antivirus policy to collect all antivirus program
- Allow qdisk to read usr_t
- Add additional caps for vmware_host
- Allow tmpfiles_t to setattr on mandb_cache_t
- Dontaudit leaked files into mozilla_plugin_config_t
- Allow wdmd to getattr on tmpfs
- Allow realmd to use /dev/random
- allow containers to send audit messages
- Allow root mount any file via loop device with enforcing mls policy
- Allow tmpfiles_t to setattr on mandb_cache_t
- Allow tmpfiles_t to setattr on mandb_cache_t
- Make userdom_dontaudit_write_all_ not allow open
- Allow init scripts to read all unit files
- Add support for saphostctrl ports

* Mon Oct 8 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-33
- Add kernel_read_system_state to sandbox_client_t
- Add some of the missing access to kdumpgui
- Allow systemd_dbusd_t to status the init system
- Allow vmnet-natd to request the kernel to load a module
- Allow gsf-office-thum to append .cache/gdm/session.log
- realmd wants to read .config/dconf/user
- Firewalld wants sys_nice/setsched
- Allow tmpreaper to delete mandb cache files
- Firewalld wants sys_nice/setsched
- Allow firewalld to perform  a DNS name resolution
- Allown winbind to read /usr/share/samba/codepages/lowcase.dat
- Add support for HTTPProxy* in /etc/freshclam.conf
- Fix authlogin_yubike boolean
- Extend smbd_selinux man page to include samba booleans
- Allow dhcpc to execute consoletype
- Allow ping to use inherited tmp files created in init scripts
- On full relabel with unconfined domain disabled, initrc was running some chcon's
- Allow people who delete man pages to delete mandb cache files

* Thu Oct 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-32
- Add missing permissive domains

* Thu Oct 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-31
- Add new mandb policy
- ALlow systemd-tmpfiles_t to relabel mandb_cache_t
- Allow logrotate to start all unit files

* Thu Oct 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-30
- Add fixes for ctbd
- Allow nmbd to stream connect to ctbd
- Make cglear_t as nsswitch_domain
- Fix bogus in interfaces
- Allow openshift to read/write postfix public pipe
- Add postfix_manage_spool_maildrop_files() interface
- stickshift paths have been renamed to openshift
- gnome-settings-daemon wants to write to /run/systemd/inhibit/ pipes
- Update man pages, adding ENTRYPOINTS

* Tue Oct 2 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-29
-  Add mei_device_t
- Make sure gpg content in homedir created with correct label
- Allow dmesg to write to abrt cache files
- automount wants to search  virtual memory sysctls
- Add support for hplip logs stored in /var/log/hp/tmp
- Add labeling for /etc/owncloud/config.php
- Allow setroubleshoot to send analysys to syslogd-journal
- Allow virsh_t to interact with new fenced daemon
- Allow gpg to write to /etc/mail/spamassassiin directories
- Make dovecot_deliver_t a mail server delivery type
- Add label for /var/tmp/DNS25

* Thu Sep 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-28
- Fixes for tomcat_domain template interface

* Thu Sep 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-27
- Remove init_systemd and init_upstart boolean, Move init_daemon_domain and init_system_domain to use attributes
- Add attribute to all base os types.  Allow all domains to read all ro base OS types

* Wed Sep 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-26
- Additional unit files to be defined as power unit files
- Fix more boolean names

* Tue Sep 25 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-25
- Fix boolean name so subs will continue to work

* Tue Sep 25 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-24
- dbus needs to start getty unit files
- Add interface to allow system_dbusd_t to start the poweroff service
- xdm wants to exec telepathy apps
- Allow users to send messages to systemdlogind
- Additional rules needed for systemd and other boot apps
- systemd wants to list /home and /boot
- Allow gkeyringd to write dbus/conf file
- realmd needs to read /dev/urand
- Allow readahead to delete /.readahead if labeled root_t, might get created before policy is loaded

* Thu Sep 20 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-23
- Fixes to safe more rules
- Re-write tomcat_domain_template()
- Fix passenger labeling
- Allow all domains to read man pages
- Add ephemeral_port_t to the 'generic' port interfaces
- Fix the names of postgresql booleans

* Tue Sep 18 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-22
- Stop using attributes form netlabel_peer and syslog, auth_use_nsswitch setsup netlabel_peer
- Move netlable_peer check out of booleans
- Remove call to recvfrom_netlabel for kerberos call
- Remove use of attributes when calling syslog call 
- Move -miscfiles_read_localization to domain.te to save hundreds of allow rules
- Allow all domains to read locale files.  This eliminates around 1500 allow rules- Cleanup nis_use_ypbind_uncond interface
- Allow rndc to block suspend
- tuned needs to modify the schedule of the kernel
- Allow svirt_t domains to read alsa configuration files
- ighten security on irc domains and make sure they label content in homedir correctly
- Add filetrans_home_content for irc files
- Dontaudit all getattr access for devices and filesystems for sandbox domains
- Allow stapserver to search cgroups directories
- Allow all postfix domains to talk to spamd

* Mon Sep 17 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-21
- Add interfaces to ignore setattr until kernel fixes this to be checked after the DAC check
- Change pam_t to pam_timestamp_t
- Add dovecot_domain attribute and allow this attribute block_suspend capability2
- Add sanlock_use_fusefs boolean
- numad wants send/recieve msg
- Allow rhnsd to send syslog msgs
- Make piranha-pulse as initrc domain
- Update openshift instances to dontaudit setattr until the kernel is fixed.

* Fri Sep 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-20
-  Fix auth_login_pgm_domain() interface to allow domains also managed user tmp dirs because of #856880 related to pam_systemd
- Remove pam_selinux.8 which conflicts with man page owned by the pam package
- Allow glance-api to talk to mysql
- ABRT wants to read Xorg.0.log if if it detects problem with Xorg
- Fix gstreamer filename trans. interface

* Thu Sep 13 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-19
- Man page fixes by Dan Walsh

* Tue Sep 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-18
- Allow postalias to read postfix config files
- Allow man2html to read man pages
- Allow rhev-agentd to search all mountpoints
- Allow rhsmcertd to read /dev/random
- Add tgtd_stream_connect() interface
- Add cyrus_write_data() interface
- Dontaudit attempts by sandboxX clients connectiing to the xserver_port_t
- Add port definition for tcp/81 as http_port_t
- Fix /dev/twa labeling
- Allow systemd to read modules config

* Mon Sep 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-17
- Merge openshift policy
- Allow xauth to read /dev/urandom
- systemd needs to relabel content in /run/systemd directories
- Files unconfined should be able to perform all services on all files
- Puppet tmp file can be leaked to all domains
- Dontaudit rhsmcertd-worker to search /root/.local
- Allow chown capability for zarafa domains
-  Allow system cronjobs to runcon into openshift domains
- Allow virt_bridgehelper_t to manage content in the svirt_home_t labeled directories

* Fri Sep 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-16
- nmbd wants to create /var/nmbd
-  Stop transitioning out of anaconda and firstboot, just causes AVC messages
- Allow clamscan to read /etc files
- Allow bcfg2 to bind cyphesis port
- heartbeat should be run as rgmanager_t instead of corosync_t
- Add labeling for /etc/openldap/certs
- Add labeling for /opt/sartest directory
- Make crontab_t as userdom home reader
- Allow tmpreaper to list admin_home dir
- Add defition for imap_0 replay cache file
- Add support for gitolite3
- Allow virsh_t to send syslog messages
- allow domains that can read samba content to be able to list the directories also
- Add realmd_dbus_chat to allow all apps that use nsswitch to talk to realmd
- Separate out sandbox from sandboxX policy so we can disable it by default
- Run dmeventd as lvm_t
- Mounting on any directory requires setattr and write permissions
- Fix use_nfs_home_dirs() boolean
- New labels for pam_krb5
- Allow init and initrc domains to sys_ptrace since this is needed to look at processes not owned by uid 0
- Add realmd_dbus_chat to allow all apps that use nsswitch to talk to realmd

* Fri Aug 31 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-15
- Separate sandbox policy into sandbox and sandboxX, and disable sandbox by default on fresh installs
- Allow domains that can read etc_t to read etc_runtime_t 
- Allow all domains to use inherited tmpfiles

* Wed Aug 29 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-14
- Allow realmd to read resolv.conf
- Add pegasus_cache_t type
- Label /usr/sbin/fence_virtd as virsh_exec_t
- Add policy for pkcsslotd
- Add support for cpglockd
- Allow polkit-agent-helper to read system-auth-ac
- telepathy-idle wants to read gschemas.compiled
- Allow plymouthd to getattr on fs_t
- Add slpd policy
- Allow ksysguardproces to read/write config_usr_t

* Sat Aug 25 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-13
- Fix labeling substitution so rpm will label /lib/systemd content correctly

* Fri Aug 24 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-12
- Add file name transitions for ttyACM0
- spice-vdagent(d)'s are going to log over to syslog
- Add sensord policy
- Add more fixes for passenger policy related to puppet
- Allow wdmd to create wdmd_tmpfs_t
- Fix labeling for /var/run/cachefilesd\.pid
- Add thumb_tmpfs_t files type

* Mon Aug 20 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-11
- Allow svirt domains to manage the network since this is containerized
- Allow svirt_lxc_net_t to send audit messages

* Mon Aug 20 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-10
- Make "snmpwalk -mREDHAT-CLUSTER-MIB ...." working
- Allow dlm_controld to execute dlm_stonith labeled as bin_t
- Allow GFS2 working on F17
- Abrt needs to execute dmesg
- Allow jockey to list the contents of modeprobe.d
- Add policy for lightsquid as squid_cron_t
- Mailscanner is creating files and directories in /tmp
- dmesg is now reading /dev/kmsg
- Allow xserver to communicate with secure_firmware
- Allow fsadm tools (fsck) to read /run/mount contnet
- Allow sysadm types to read /dev/kmsg
- 

* Thu Aug 16 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-9
- Allow postfix, sssd, rpcd to block_suspend
- udev seems to need secure_firmware capability
- Allow virtd to send dbus messages to firewalld so it can configure the firewall

* Thu Aug 16 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-8
- Fix labeling of content in /run created by virsh_t
- Allow condor domains to read kernel sysctls
- Allow condor_master to connect to amqp
- Allow thumb drives to create shared memory and semaphores
- Allow abrt to read mozilla_plugin config files
- Add labels for lightsquid
- Default files in /opt and /usr that end in .cgi as httpd_sys_script_t, allow
- dovecot_auth_t uses ldap for user auth
- Allow domains that can read dhcp_etc_t to read lnk_files
- Add more then one watchdog device
- Allow useradd_t to manage etc_t files so it can rename it and edit them
- Fix invalid class dir should be fifo_file
- Move /run/blkid to fsadm and make sure labeling is correct

* Tue Aug 14 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-7
- Fix bogus regex found by eparis
- Fix manage run interface since lvm needs more access
- syslogd is searching cgroups directory
- Fixes to allow virt-sandbox-service to manage lxc var run content

* Mon Aug 13 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-6
- Fix Boolean settings
- Add new libjavascriptcoregtk as textrel_shlib_t
- Allow xdm_t to create xdm_home_t directories
- Additional access required for systemd
- Dontaudit mozilla_plugin attempts to ipc_lock
- Allow tmpreaper to delete unlabeled files
- Eliminate screen_tmp_t and allow it to manage user_tmp_t
- Dontaudit mozilla_plugin_config_t to append to leaked file descriptors
- Allow web plugins to connect to the asterisk ports
- Condor will recreate the lock directory if it does not exist
- Oddjob mkhomedir needs to connectto user processes
- Make oddjob_mkhomedir_t a userdom home manager

* Thu Aug 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-5
- Put placeholder back in place for proper numbering of capabilities
- Systemd also configures init scripts

* Thu Aug 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-4
- Fix ecryptfs interfaces
- Bootloader seems to be trolling around /dev/shm and /dev
- init wants to create /etc/systemd/system-update.target.wants
- Fix systemd_filetrans call to move it out of tunable
- Fix up policy to work with systemd userspace manager
- Add secure_firmware capability and remove bogus epolwakeup
- Call seutil_*_login_config interfaces where should be needed
- Allow rhsmcertd to send signal to itself
- Allow thin domains to send signal to itself
- Allow Chrome_ChildIO to read dosfs_t

* Tue Aug 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-3
- Add role rules for realmd, sambagui

* Tue Aug 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-2
- Add new type selinux_login_config_t for /etc/selinux/<type>/logins/
- Additional fixes for seutil_manage_module_store()
- dbus_system_domain() should be used with optional_policy
- Fix svirt to be allowed to use fusefs file system
- Allow login programs to read /run/ data created by systemd_login
- sssd wants to write /etc/selinux/<policy>/logins/ for SELinux PAM module
- Fix svirt to be allowed to use fusefs file system
- Allow piranha domain to use nsswitch
- Sanlock needs to send Kill Signals to non root processes
- Pulseaudio wants to execute /run/user/PID/.orc

* Fri Aug 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-1
- Fix saslauthd when it tries to read /etc/shadow
- Label gnome-boxes as a virt homedir
- Need to allow svirt_t ability to getattr on nfs_t file systems
- Update sanlock policy to solve all AVC's
- Change confined users can optionally manage virt content
- Handle new directories under ~/.cache
- Add block suspend to appropriate domains
- More rules required for containers
- Allow login programs to read /run/ data created by systemd_logind
- Allow staff users to run svirt_t processes

* Thu Aug 2 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-0
- Update to upstream

* Mon Jul 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-15
- More fixes for systemd to make rawhide booting from Dan Walsh

* Mon Jul 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-14
- Add systemd fixes to make rawhide booting

* Fri Jul 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-13
- Add systemd_logind_inhibit_var_run_t attribute
- Remove corenet_all_recvfrom_unlabeled() for non-contrib policies because we moved it to domain.if for all domain_type
- Add interface for mysqld to dontaudit signull to all processes
- Label new /var/run/journal directory correctly
- Allow users to inhibit suspend via systemd
- Add new type for the /var/run/inhibit directory
- Add interface to send signull to systemd_login so avahi can send them
- Allow systemd_passwd to send syslog messages
- Remove corenet_all_recvfrom_unlabeled() calling fro policy files
- Allow       editparams.cgi running as httpd_bugzilla_script_t to read /etc/group
- Allow smbd to read cluster config
- Add additional labeling for passenger
- Allow dbus to inhibit suspend via systemd
- Allow avahi to send signull to systemd_login

* Mon Jul 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-12
- Add interface to dontaudit getattr access on sysctls
- Allow sshd to execute /bin/login
- Looks like xdm is recreating the xdm directory in ~/.cache/ on login
- Allow syslog to use the leaked kernel_t unix_dgram_socket from system-jounald
-  Fix semanage to work with unconfined domain disabled on F18
- Dontaudit attempts by mozilla plugins to getattr on all kernel sysctls
- Virt seems to be using lock files
- Dovecot seems to be searching directories of every mountpoint
- Allow jockey to read random/urandom, execute shell and install third-party drivers
- Add aditional params to allow cachedfiles to manage its content
- gpg agent needs to read /dev/random
- The kernel hands an svirt domains /SYSxxxxx which is a tmpfs that httpd wants to read and write
- Add a bunch of dontaudit rules to quiet svirt_lxc domains
- Additional perms needed to run svirt_lxc domains
- Allow cgclear to read cgconfig
- Allow sys_ptrace capability for snmp
- Allow freshclam to read /proc
- Allow procmail to manage /home/user/Maildir content
- Allow NM to execute wpa_cli
- Allow amavis to read clamd system state
- Regenerate man pages

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-10
- Add realmd and stapserver policies
- Allow useradd to manage stap-server lib files
- Tighten up capabilities for confined users
- Label /etc/security/opasswd as shadow_t
- Add label for /dev/ecryptfs
- Allow condor_startd_t to start sshd with the ranged
- Allow lpstat.cups to read fips_enabled file
- Allow pyzor running as spamc_t to create /root/.pyzor directory
- Add labelinf for amavisd-snmp init script
- Add support for amavisd-snmp
- Allow fprintd sigkill self
- Allow xend (w/o libvirt) to start virtual machines
- Allow aiccu to read /etc/passwd
- Allow condor_startd to Make specified domain MCS trusted for setting any category set for the processes it executes
- Add condor_startd_ranged_domtrans_to() interface
- Add ssd_conf_t for /etc/sssd
- accountsd needs to fchown some files/directories
- Add ICACLient and zibrauserdata as mozilla_filetrans_home_content
- SELinux reports afs_t needs dac_override to read /etc/mtab, even though everything works, adding dontaudit
- Allow xend_t to read the /etc/passwd file

* Wed Jul 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-9
- Until we figure out how to fix systemd issues, allow all apps that send syslog messages to send them to kernel_t
- Add init_access_check() interface
- Fix label on /usr/bin/pingus to not be labeled as ping_exec_t
- Allow tcpdump to create a netlink_socket
- Label newusers like useradd
- Change xdm log files to be labeled xdm_log_t
- Allow sshd_t with privsep to work in MLS
- Allow freshclam to update databases thru HTTP proxy
- Allow s-m-config to access check on systemd
- Allow abrt to read public files by default
- Fix amavis_create_pid_files() interface
- Add labeling and filename transition for dbomatic.log
- Allow system_dbusd_t to stream connect to bluetooth, and use its socket
- Allow amavisd to execute fsav
- Allow tuned to use sys_admin and sys_nice capabilities
- Add php-fpm policy from Bryan
- Add labeling for aeolus-configserver-thinwrapper
- Allow thin domains to execute shell
- Fix gnome_role_gkeyringd() interface description
- Lot of interface fixes
- Allow OpenMPI job running as condor_startd_ssh_t to manage condor lib files
- Allow OpenMPI job to use kerberos
- Make deltacloudd_t as nsswitch_domain
- Allow xend_t to run lsscsi
- Allow qemu-dm running as xend_t to create tun_socket
- Add labeling for /opt/brother/Printers(.*/)?inf
- Allow jockey-backend to read pyconfig-64.h labeled as usr_t
- Fix clamscan_can_scan_system boolean
- Allow lpr to connectto to /run/user/$USER/keyring-22uREb/pkcs11

* Tue Jul 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-8
- initrc is calling exportfs which is not confined so it attempts to read nfsd_files
- Fixes for passenger running within openshift.
- Add labeling for all tomcat6 dirs
- Add support for tomcat6
- Allow cobblerd to read /etc/passwd
- Allow jockey to read sysfs and and execute binaries with bin_t
- Allow thum to use user terminals
- Allow cgclear to read cgconfig config files
- Fix bcf2g.fc
- Remove sysnet_dns_name_resolve() from policies where auth_use_nsswitch() is used for other domains
- Allow dbomatic to execute ruby
- abrt_watch_log should be abrt_domain
- Allow mozilla_plugin to connect to gatekeeper port

* Wed Jun 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-7
- add ptrace_child access to process
- remove files_read_etc_files() calling from all policies which have auth_use_nsswith()
- Allow boinc domains to manage boinc_lib_t lnk_files
- Add support for boinc-client.service unit file
- Add support for boinc.log
- Allow mozilla_plugin execmod on mozilla home files if allow_ex
- Allow dovecot_deliver_t to read dovecot_var_run_t
- Allow ldconfig and insmod to manage kdumpctl tmp files
- Move thin policy out from cloudform.pp and add a new thin poli
- pacemaker needs to communicate with corosync streams
- abrt is now started on demand by dbus
- Allow certmonger to talk directly to Dogtag servers
- Change labeling for /var/lib/cobbler/webui_sessions to httpd_c
- Allow mozila_plugin to execute gstreamer home files
- Allow useradd to delete all file types stored in the users hom
- rhsmcertd reads the rpm database
- Add support for lightdm

* Mon Jun 25 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-6
- Add tomcat policy
- Remove pyzor/razor policy
- rhsmcertd reads the rpm database
- Dontaudit  thumb to setattr on xdm_tmp dir
- Allow wicd to execute ldconfig in the networkmanager_t domain
- Add /var/run/cherokee\.pid labeling
- Allow mozilla_plugin to create mozilla_plugin_tmp_t lnk files too
- Allow postfix-master to r/w pipes other postfix domains
- Allow snort to create netlink_socket
- Add kdumpctl policy
- Allow firstboot to create tmp_t files/directories
- /usr/bin/paster should not be labeled as piranha_exec_t
- remove initrc_domain from tomcat
- Allow ddclient to read /etc/passwd
- Allow useradd to delete all file types stored in the users homedir
- Allow ldconfig and insmod to manage kdumpctl tmp files
- Firstboot should be just creating tmp_t dirs and xauth should be allowed to write to those
- Transition xauth files within firstboot_tmp_t
- Fix labeling of /run/media to match /media
- Label all lxdm.log as xserver_log_t
- Add port definition for mxi port
- Allow local_login_t to execute tmux

* Tue Jun 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-5
- apcupsd needs to read /etc/passwd
- Sanlock allso sends sigkill
- Allow glance_registry to connect to the mysqld port
- Dontaudit mozilla_plugin trying to getattr on /dev/gpmctl
- Allow firefox plugins/flash to connect to port 1234
- Allow mozilla plugins to delete user_tmp_t files
- Add transition name rule for printers.conf.O
- Allow virt_lxc_t to read urand
- Allow systemd_loigind to list gstreamer_home_dirs
- Fix labeling for /usr/bin
- Fixes for cloudform services
  * support FIPS
- Allow polipo to work as web caching
- Allow chfn to execute tmux

* Fri Jun 15 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-4
- Add support for ecryptfs
  * ecryptfs does not support xattr
  * we need labeling for HOMEDIR
- Add policy for (u)mount.ecryptfs*
- Fix labeling of kerbero host cache files, allow rpc.svcgssd to manage host cache
- Allow dovecot to manage Maildir content, fix transitions to Maildir
- Allow postfix_local to transition to dovecot_deliver
- Dontaudit attempts to setattr on xdm_tmp_t, looks like bogus code
- Cleanup interface definitions
- Allow apmd to change with the logind daemon
- Changes required for sanlock in rhel6
- Label /run/user/apache as httpd_tmp_t
- Allow thumb to use lib_t as execmod if boolean turned on
- Allow squid to create the squid directory in /var with the correct labe
- Add a new policy for glusterd from Bryan Bickford (bbickfor@redhat.com)
- Allow virtd to exec xend_exec_t without transition
- Allow virtd_lxc_t to unmount all file systems

* Tue Jun 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-3
- PolicyKit path has changed
- Allow httpd connect to dirsrv socket
- Allow tuned to write generic kernel sysctls
- Dontaudit logwatch to gettr on /dev/dm-2
- Allow policykit-auth to manage kerberos files
- Make condor_startd and rgmanager as initrc domain
- Allow virsh to read /etc/passwd
- Allow mount to mount on user_tmp_t for /run/user/dwalsh/gvfs
- xdm now needs to execute xsession_exec_t
- Need labels for /var/lib/gdm
- Fix files_filetrans_named_content() interface
- Add new attribute - initrc_domain
- Allow systemd_logind_t to signal, signull, sigkill all processes
- Add filetrans rules for etc_runtime files

* Sat Jun 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-2
- Rename boolean names to remove allow_

* Thu Jun 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-1
- Mass merge with upstream
  * new policy topology to include contrib policy modules
  * we have now two base policy patches

* Wed May 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-128
- Fix description of authlogin_nsswitch_use_ldap
- Fix transition rule for rhsmcertd_t needed for RHEL7
- Allow useradd to list nfs state data
- Allow openvpn to manage its log file and directory
- We want vdsm to transition to mount_t when executing mount command to make sure /etc/mtab remains labeled correctly
- Allow thumb to use nvidia devices
-  Allow local_login to create user_tmp_t files for kerberos
- Pulseaudio needs to read systemd_login /var/run content
- virt should only transition named system_conf_t config files
- Allow  munin to execute its plugins
- Allow nagios system plugin to read /etc/passwd
- Allow plugin to connect to soundd port
- Fix httpd_passwd to be able to ask passwords
- Radius servers can use ldap for backing store
- Seems to need to mount on /var/lib for xguest polyinstatiation to work.
- Allow systemd_logind to list the contents of gnome keyring
- VirtualGL need xdm to be able to manage content in /etc/opt/VirtualGL
- Add policy for isns-utils

* Mon May 28 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-127
- Add policy for subversion daemon
- Allow boinc to read passwd
- Allow pads to read kernel network state
- Fix man2html interface for sepolgen-ifgen
- Remove extra /usr/lib/systemd/system/smb
- Remove all /lib/systemd and replace with /usr/lib/systemd
- Add policy for man2html
- Fix the label of kerberos_home_t to krb5_home_t
- Allow mozilla plugins to use Citrix
- Allow tuned to read /proc/sys/kernel/nmi_watchdog
- Allow tune /sys options via systemd's tmpfiles.d "w" type

* Wed May 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-126
- Dontaudit lpr_t to read/write leaked mozilla tmp files
- Add file name transition for .grl-podcasts directory
- Allow corosync to read user tmp files
- Allow fenced to create snmp lib dirs/files
- More fixes for sge policy
- Allow mozilla_plugin_t to execute any application
- Allow dbus to read/write any open file descriptors to any non security file on the system that it inherits to that it can pass them to another domain
- Allow mongod to read system state information
-  Fix wrong type, we should dontaudit sys_admin for xdm_t not xserver_t
- Allow polipo to manage polipo_cache dirs
- Add jabbar_client port to mozilla_plugin_t
- Cleanup procmail policy
- system bus will pass around open file descriptors on files that do not have labels on them
- Allow l2tpd_t to read system state
- Allow tuned to run ls /dev
- Allow sudo domains to read usr_t files
- Add label to machine-id 
- Fix corecmd_read_bin_symlinks cut and paste error

* Wed May 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-125
- Fix pulseaudio port definition
- Add labeling for condor_starter
- Allow chfn_t to creat user_tmp_files
- Allow chfn_t to execute bin_t
- Allow prelink_cron_system_t to getpw calls
- Allow sudo domains to manage kerberos rcache files
- Allow user_mail_domains to work with courie
- Port definitions necessary for running jboss apps within openshift
-  Add support for openstack-nova-metadata-api
- Add support for nova-console*
- Add support for openstack-nova-xvpvncproxy
- Fixes to make privsep+SELinux working if we try to use chage to change passwd
- Fix auth_role() interface
- Allow numad to read sysfs
- Allow matahari-rpcd to execute shell
- Add label for ~/.spicec
- xdm is executing lspci as root which is requesting a sys_admin priv but seems to succeed without it
- Devicekit_disk wants to read the logind sessions file when writing a cd
- Add fixes for condor to make condor jobs working correctly
- Change label of /var/log/rpmpkgs to cron_log_t
- Access requires to allow systemd-tmpfiles --create to work.
- Fix obex to be a user application started by the session bus.
- Add additional filename trans rules for kerberos
- Fix /var/run/heartbeat labeling
- Allow apps that are managing rcache to file trans correctly
- Allow openvpn to authenticate against ldap server
- Containers need to listen to network starting and stopping events

* Wed May 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-124
- Make systemd unit files less specific

* Tue May 8 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-123
- Fix zarafa labeling
- Allow guest_t to fix labeling
- corenet_tcp_bind_all_unreserved_ports(ssh_t) should be called with the user_tcp_server boolean
- add lxc_contexts
- Allow accountsd to read /proc
- Allow restorecond to getattr on all file sytems
- tmpwatch now calls getpw
- Allow apache daemon to transition to pwauth domain
- Label content under /var/run/user/NAME/keyring* as gkeyringd_tmp_t
- The obex socket seems to be a stream socket
- dd label for /var/run/nologin

* Mon May 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-122
- Allow jetty running as httpd_t to read hugetlbfs files
- Allow sys_nice and setsched for rhsmcertd
- Dontaudit attempts by mozilla_plugin_t to bind to ssdp ports
- Allow setfiles to append to xdm_tmp_t
- Add labeling for /export as a usr_t directory
- Add labels for .grl files created by gstreamer

* Fri May 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-121
- Add labeling for /usr/share/jetty/bin/jetty.sh
- Add jetty policy which contains file type definitios
- Allow jockey to use its own fifo_file and make this the default for all domains
- Allow mozilla_plugins to use spice (vnc_port/couchdb)
- asterisk wants to read the network state
- Blueman now uses /var/lib/blueman- Add label for nodejs_debug
- Allow mozilla_plugin_t to create ~/.pki directory and content

* Wed May 2 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-120
- Add clamscan_can_scan_system boolean
- Allow mysqld to read kernel network state
- Allow sshd to read/write condor lib files
- Allow sshd to read/write condor-startd tcp socket
- Fix description on httpd_graceful_shutdown
- Allow glance_registry to communicate with mysql
- dbus_system_domain is using systemd to lauch applications
- add interfaces to allow domains to send kill signals to user mail agents
- Remove unnessary access for svirt_lxc domains, add privs for virtd_lxc_t
- Lots of new access required for secure containers
- Corosync needs sys_admin capability
- ALlow colord to create shm
- .orc should be allowed to be created by any app that can create gstream home content, thumb_t to be specific
- Add boolean to control whether or not mozilla plugins can create random content in the users homedir
-  Add new interface to allow domains to list msyql_db directories, needed for libra
- shutdown has to be allowed to delete etc_runtime_t
- Fail2ban needs to read /etc/passwd
-  Allow ldconfig to create /var/cache/ldconfig
- Allow tgtd to read hardware state information
- Allow collectd to create packet socket
- Allow chronyd to send signal to itself
- Allow collectd to read /dev/random
- Allow collectd to send signal to itself
- firewalld needs to execute restorecon
- Allow restorecon and other login domains to execute restorecon

* Tue Apr 24 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-119
- Allow logrotate to getattr on systemd unit files
- Add support for tor systemd unit file
- Allow apmd to create /var/run/pm-utils with the correct label
- Allow l2tpd to send sigkill to pppd
- Allow pppd to stream connect to l2tpd
- Add label for scripts in /etc/gdm/
- Allow systemd_logind_t to ignore mcs constraints on sigkill
- Fix files_filetrans_system_conf_named_files() interface
- Add labels for /usr/share/wordpress/wp-includes/*.php
- Allow cobbler to get SELinux mode and booleans

* Mon Apr 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-118
- Add unconfined_execmem_exec_t as an alias to bin_t
- Allow fenced to read snmp var lib files, also allow it to read usr_t
- ontaudit access checks on all executables from mozilla_plugin
- Allow all user domains to setexec, so that sshd will work properly if it call setexec(NULL) while running withing a user mode
- Allow systemd_tmpfiles_t to getattr all pipes and sockets
- Allow glance-registry to send system log messages
- semanage needs to manage mock lib files/dirs

* Sun Apr 22 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-117
- Add policy for abrt-watch-log
- Add definitions for jboss_messaging ports
- Allow systemd_tmpfiles to manage printer devices
- Allow oddjob to use nsswitch
- Fix labeling of log files for postgresql
- Allow mozilla_plugin_t to execmem and execstack by default
- Allow firewalld to execute shell
- Fix /etc/wicd content files to get created with the correct label
- Allow mcelog to exec shell
- Add ~/.orc as a gstreamer_home_t
- /var/spool/postfix/lib64 should be labeled lib_t
- mpreaper should be able to list all file system labeled directories
- Add support for apache to use openstack
- Add labeling for /etc/zipl.conf and zipl binary
- Turn on allow_execstack and turn off telepathy transition for final release

* Mon Apr 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-116
- More access required for virt_qmf_t
- Additional assess required for systemd-logind to support multi-seat
- Allow mozilla_plugin to setrlimit
- Revert changes to fuse file system to stop deadlock

* Mon Apr 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-115
- Allow condor domains to connect to ephemeral ports
- More fixes for condor policy
- Allow keystone to stream connect to mysqld
- Allow mozilla_plugin_t to read generic USB device to support GPS devices
- Allow thum to file name transition gstreamer home content
- Allow thum to read all non security files
- Allow glance_api_t to connect to ephemeral ports
- Allow nagios plugins to read /dev/urandom
- Allow syslogd to search postfix spool to support postfix chroot env
- Fix labeling for /var/spool/postfix/dev
- Allow wdmd chown
- Label .esd_auth as pulseaudio_home_t
- Have no idea why keyring tries to write to /run/user/dwalsh/dconf/user, but we can dontaudit for now

* Fri Apr 13 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-114
- Add support for clamd+systemd
- Allow fresclam to execute systemctl to handle clamd
- Change labeling for /usr/sbin/rpc.ypasswd.env
	- Allow yppaswd_t to execute yppaswd_exec_t
	- Allow yppaswd_t to read /etc/passwd
- Gnomekeyring socket has been moved to /run/user/USER/
- Allow samba-net to connect to ldap port
- Allow signal for vhostmd
- allow mozilla_plugin_t to read user_home_t socket
- New access required for secure Linux Containers
- zfs now supports xattrs
- Allow quantum to execute sudo and list sysfs
- Allow init to dbus chat with the firewalld
- Allow zebra to read /etc/passwd

* Tue Apr 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-113
- Allow svirt_t to create content in the users homedir under ~/.libvirt
- Fix label on /var/lib/heartbeat
- Allow systemd_logind_t to send kill signals to all processes started by a user
- Fuse now supports Xattr Support

* Tue Apr 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-112
- upowered needs to setsched on the kernel
- Allow mpd_t to manage log files
- Allow xdm_t to create /var/run/systemd/multi-session-x
- Add rules for missedfont.log to be used by thumb.fc
- Additional access required for virt_qmf_t
- Allow dhclient to dbus chat with the firewalld
- Add label for lvmetad
- Allow systemd_logind_t to remove userdomain sock_files
- Allow cups to execute usr_t files
- Fix labeling on nvidia shared libraries
- wdmd_t needs access to sssd and /etc/passwd
- Add boolean to allow ftp servers to run in passive mode
- Allow namepspace_init_t to relabelto/from a different user system_u from the user the namespace_init running with
- Fix using httpd_use_fusefs
- Allow chrome_sandbox_nacl to write inherited user tmp files as we allow it for chrome_sandbox

* Fri Apr 6 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-111
- Rename rdate port to time port, and allow gnomeclock to connect to it
- We no longer need to transition to ldconfig from rpm, rpm_script, or anaconda
- /etc/auto.* should be labeled bin_t
- Add httpd_use_fusefs boolean
- Add fixes for heartbeat
- Allow sshd_t to signal processes that it transitions to
- Add condor policy
- Allow svirt to create monitors in ~/.libvirt
- Allow dovecot to domtrans sendmail to handle sieve scripts
- Lot of fixes for cfengine

* Tue Apr 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-110
- /var/run/postmaster.* labeling is no longer needed
- Alllow drbdadmin to read /dev/urandom
- l2tpd_t seems to use ptmx
- group+ and passwd+ should be labeled as /etc/passwd
- Zarafa-indexer is a socket

* Fri Mar 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-109
- Ensure lastlog is labeled correctly
- Allow accountsd to read /proc data about gdm
- Add fixes for tuned
- Add bcfg2 fixes which were discovered during RHEL6 testing
- More fixes for gnome-keyring socket being moved
- Run semanage as a unconfined domain, and allow initrc_t to create tmpfs_t sym links on shutdown
- Fix description for files_dontaudit_read_security_files() interface

* Wed Mar 28 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-108
- Add new policy and man page for bcfg2
- cgconfig needs to use getpw calls
- Allow domains that communicate with the keyring to use cache_home_t instead of gkeyringd_tmpt
- gnome-keyring wants to create a directory in cache_home_t
- sanlock calls getpw

* Wed Mar 28 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-107
- Add numad policy and numad man page
- Add fixes for interface bugs discovered by SEWatch
- Add /tmp support for squid
- Add fix for #799102
     * change default labeling for /var/run/slapd.* sockets
- Make thumb_t as userdom_home_reader
- label /var/lib/sss/mc same as pubconf, so getpw domains can read it
- Allow smbspool running as cups_t to stream connect to nmbd
- accounts needs to be able to execute passwd on behalf of users
- Allow systemd_tmpfiles_t to delete boot flags
- Allow dnssec_trigger to connect to apache ports
- Allow gnome keyring to create sock_files in ~/.cache
- google_authenticator is using .google_authenticator
- sandbox running from within firefox is exposing more leaks
- Dontaudit thumb to read/write /dev/card0
- Dontaudit getattr on init_exec_t for gnomeclock_t
- Allow certmonger to do a transition to certmonger_unconfined_t
- Allow dhcpc setsched which is caused by nmcli
- Add rpm_exec_t for /usr/sbin/bcfg2
- system cronjobs are sending dbus messages to systemd_logind
- Thumnailers read /dev/urand

* Thu Mar 22 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-106
- Allow auditctl getcap
- Allow vdagent to use libsystemd-login
- Allow abrt-dump-oops to search /etc/abrt
- Got these avc's while trying to print a boarding pass from firefox
- Devicekit is now putting the media directory under /run/media
- Allow thumbnailers to create content in ~/.thumbails directory
- Add support for proL2TPd by Dominick Grift
- Allow all domains to call getcap
- wdmd seems to get a random chown capability check that it does not need
- Allow vhostmd to read kernel sysctls

* Wed Mar 21 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-105
- Allow chronyd to read unix
- Allow hpfax to read /etc/passwd
- Add support matahari vios-proxy-* apps and add virtd_exec_t label for them
- Allow rpcd to read quota_db_t
- Update to man pages to match latest policy
- Fix bug in jockey interface for sepolgen-ifgen
- Add initial svirt_prot_exec_t policy

* Mon Mar 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-104
- More fixes for systemd from Dan Walsh

* Mon Mar 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-103
- Add a new type for /etc/firewalld and allow firewalld to write to this directory
- Add definition for ~/Maildir, and allow mail deliver domains to write there
- Allow polipo to run from a cron job
- Allow rtkit to schedule wine processes
- Allow mozilla_plugin_t to acquire a bug, and allow it to transition gnome content in the home dir to the proper label
- Allow users domains to send signals to consolehelper domains

* Fri Mar 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-102
- More fixes for boinc policy
- Allow polipo domain to create its own cache dir and pid file
- Add systemctl support to httpd domain
- Add systemctl support to polipo, allow NetworkManager to manage the service
- Add policy for jockey-backend
- Add support for motion daemon which is now covered by zoneminder policy
- Allow colord to read/write motion tmpfs
- Allow vnstat to search through var_lib_t directories
- Stop transitioning to quota_t, from init an sysadm_t

* Wed Mar 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-101
- Add svirt_lxc_file_t as a customizable type

* Wed Mar 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-100
- Add additional fixes for icmp nagios plugin
- Allow cron jobs to open fifo_files from cron, since service script opens /dev/stdin
- Add certmonger_unconfined_exec_t
- Make sure tap22 device is created with the correct label
- Allow staff users to read systemd unit files
- Merge in previously built policy
- Arpwatch needs to be able to start netlink sockets in order to start
- Allow cgred_t to sys_ptrace to look at other DAC Processes

* Mon Mar 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-99
- Back port some of the access that was allowed in nsplugin_t
- Add definitiona for couchdb ports
- Allow nagios to use inherited users ttys
- Add git support for mock
- Allow inetd to use rdate port
- Add own type for rdate port
- Allow samba to act as a portmapper
- Dontaudit chrome_sandbox attempts to getattr on chr_files in /dev
- New fixes needed for samba4
- Allow apps that use lib_t to read lib_t symlinks

* Fri Mar 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-98
- Add policy for nove-cert
- Add labeling for nova-openstack  systemd unit files
- Add policy for keystoke 

* Thu Mar 8 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-97
- Fix man pages fro domains
- Add man pages for SELinux users and roles
- Add storage_dev_filetrans_named_fixed_disk() and use it for smartmon
- Add policy for matahari-rpcd
- nfsd executes mount command on restart
- Matahari domains execute renice and setsched
- Dontaudit leaked tty in mozilla_plugin_config
- mailman is changing to a per instance naming
- Add 7600 and 4447 as jboss_management ports
- Add fixes for nagios event handlers
- Label httpd.event as httpd_exec_t, it is an apache daemon

* Mon Mar 5 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-96
- Add labeling for /var/spool/postfix/dev/log
- NM reads sysctl.conf
- Iscsi log file context specification fix
-  Allow mozilla plugins to send dbus messages to user domains that transition to it
- Allow mysql to read the passwd file
- Allow mozilla_plugin_t to create mozilla home dirs in user homedir
- Allow deltacloud to read kernel sysctl
- Allow postgresql_t to connectto itselfAllow postgresql_t to connectto itself
- Allow postgresql_t to connectto itself
- Add login_userdomain attribute for users which can log in using terminal

* Tue Feb 28 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-95
- Allow sysadm_u to reach system_r by default #784011
- Allow nagios plugins to use inherited user terminals
- Razor labeling is not used no longer
- Add systemd support for matahari
- Add port_types to man page, move booleans to the top, fix some english
- Add support for matahari-sysconfig-console
- Clean up matahari.fc
- Fix matahari_admin() interfac
- Add labels for/etc/ssh/ssh_host_*.pub keys

* Mon Feb 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-94
- Allow ksysguardproces to send system log msgs
- Allow  boinc setpgid and signull
- Allow xdm_t to sys_ptrace to run pidof command
- Allow smtpd_t to manage spool files/directories and symbolic links
- Add labeling for jetty
- Needed changes to get unbound/dnssec to work with openswan

* Thu Feb 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-93
- Add user_fonts_t alias xfs_tmp_t
- Since depmod now runs as insmod_t we need to write to kernel_object_t
- Allow firewalld to dbus chat with networkmanager
- Allow qpidd to connect to matahari ports
- policykit needs to read /proc for uses not owned by it
- Allow systemctl apps to connecto the init stream

* Wed Feb 22 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-92
- Turn on deny_ptrace boolean

* Tue Feb 21 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-91
- Remove pam_selinux.8 man page. There was a conflict.

* Tue Feb 21 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-90
- Add proxy class and read access for gssd_proxy
- Separate out the sharing public content booleans
- Allow certmonger to execute a script and send signals to  apache and dirsrv to reload the certificate
-  Add label transition for gstream-0.10 and 12
- Add booleans to allow rsync to share nfs and cifs file sytems
- chrome_sandbox wants to read the /proc/PID/exe file of the program that executed it
- Fix filename transitions for cups files
- Allow denyhosts to read "unix"
- Add file name transition for locale.conf.new
- Allow boinc projects to gconf config files
- sssd needs to be able to increase the socket limit under certain loads
- sge_execd needs to read /etc/passwd
- Allow denyhost to check network state
- NetworkManager needs to read sessions data
- Allow denyhost to check network state
- Allow xen to search virt images directories
- Add label for /dev/megaraid_sas_ioctl_node
- Add autogenerated man pages

* Thu Feb 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-89
- Allow boinc project to getattr on fs
- Allow init to execute initrc_state_t
- rhev-agent package was rename to ovirt-guest-agent
- If initrc_t creates /etc/local.conf then we need to make sure it is labeled correctly
- sytemd writes content to /run/initramfs and executes it on shutdown
- kdump_t needs to read /etc/mtab, should be back ported to F16
- udev needs to load kernel modules in early system boot

* Tue Feb 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-88
- Need to add sys_ptrace back in since reading any content in /proc can cause these accesses
- Add additional systemd interfaces which are needed fro *_admin interfaces
- Fix bind_admin() interface

* Mon Feb 13 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-87
- Allow firewalld to read urand
- Alias java, execmem_mono to bin_t to allow third parties
- Add label for kmod
- /etc/redhat-lsb contains binaries
- Add boolean to allow gitosis to send mail
- Add filename transition also for "event20"
- Allow systemd_tmpfiles_t to delete all file types
- Allow collectd to ipc_lock

* Fri Feb 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-86
- make consoletype_exec optional, so we can remove consoletype policy
- remove unconfined_permisive.patch
- Allow openvpn_t to inherit user home content and tmp content
- Fix dnssec-trigger labeling
- Turn on obex policy for staff_t
- Pem files should not be secret
- Add lots of rules to fix AVC's when playing with containers
- Fix policy for dnssec
- Label ask-passwd directories correctly for systemd

* Thu Feb 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-85
- sshd fixes seem to be causing unconfined domains to dyntrans to themselves
- fuse file system is now being mounted in /run/user
- systemd_logind is sending signals to processes that are dbus messaging with it
- Add support for winshadow port and allow iscsid to connect to this port
- httpd should be allowed to bind to the http_port_t udp socket
- zarafa_var_lib_t can be a lnk_file
- A couple of new .xsession-errors files
- Seems like user space and login programs need to read logind_sessions_files
- Devicekit disk seems to be being launched by systemd
- Cleanup handling of setfiles so most of rules in te file
- Correct port number for dnssec
- logcheck has the home dir set to its cache

* Tue Feb 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-84
- Add policy for grindengine MPI jobs

* Mon Feb 6 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-83
- Add new sysadm_secadm.pp module
	* contains secadm definition for sysadm_t
- Move user_mail_domain access out of the interface into the te file
- Allow httpd_t to create httpd_var_lib_t directories as well as files
- Allow snmpd to connect to the ricci_modcluster stream
- Allow firewalld to read /etc/passwd
- Add auth_use_nsswitch for colord
- Allow smartd to read network state
- smartdnotify needs to read /etc/group

* Fri Feb 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-82
- Allow gpg and gpg_agent to store sock_file in gpg_secret_t directory
- lxdm startup scripts should be labeled bin_t, so confined users will work
- mcstransd now creates a pid, needs back port to F16
- qpidd should be allowed to connect to the amqp port
- Label devices 010-029 as usb devices
- ypserv packager says ypserv does not use tmp_t so removing selinux policy types
- Remove all ptrace commands that I believe are caused by the kernel/ps avcs
- Add initial Obex policy
- Add logging_syslogd_use_tty boolean
- Add polipo_connect_all_unreserved bolean
- Allow zabbix to connect to ftp port
- Allow systemd-logind to be able to switch VTs
- Allow apache to communicate with memcached through a sock_file

* Tue Jan 31 2012 Dan Walsh <dwalsh@redhat.com> 3.10.0-81.2
- Fix file_context.subs_dist for now to work with pre usrmove

* Mon Jan 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-81
- More /usr move fixes

* Thu Jan 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-80
- Add zabbix_can_network boolean
- Add httpd_can_connect_zabbix boolean
- Prepare file context labeling for usrmove functions
- Allow system cronjobs to read kernel network state
- Add support for selinux_avcstat munin plugin
- Treat hearbeat with corosync policy
- Allow corosync to read and write to qpidd shared mem
-  mozilla_plugin is trying to run pulseaudio 
- Fixes for new sshd patch for running priv sep domains as the users context
- Turn off dontaudit rules when turning on allow_ypbind
- udev now reads /etc/modules.d directory

* Tue Jan 24 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-79
- Turn on deny_ptrace boolean for the Rawhide run, so we can test this out
- Cups exchanges dbus messages with init
- udisk2 needs to send syslog messages
- certwatch needs to read /etc/passwd

* Mon Jan 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-78
- Add labeling for udisks2
- Allow fsadmin to communicate with the systemd process

* Mon Jan 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-77
- Treat Bip with bitlbee policy
      * Bip is an IRC proxy
- Add port definition for interwise port
- Add support for ipa_memcached socket
- systemd_jounald needs to getattr on all processes
- mdadmin fixes
     * uses getpw
- amavisd calls getpwnam()
- denyhosts calls getpwall()

* Fri Jan 20 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-76
- Setup labeling of /var/rsa and /var/lib/rsa to allow login programs to write there
- bluetooth says they do not use /tmp and want to remove the type
- Allow init to transition to colord
- Mongod needs to read /proc/sys/vm/zone_reclaim_mode
- Allow postfix_smtpd_t to connect to spamd
- Add boolean to allow ftp to connect to all ports > 1023
- Allow sendmain to write to inherited dovecot tmp files
- setroubleshoot needs to be able to execute rpm to see what version of packages

* Mon Jan 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-75
- Merge systemd patch
- systemd-tmpfiles wants to relabel /sys/devices/system/cpu/online
- Allow deltacloudd dac_override, setuid, setgid  caps
- Allow aisexec to execute shell
- Add use_nfs_home_dirs boolean for ssh-keygen

* Fri Jan 13 2012 Dan Walsh <dwalsh@redhat.com> 3.10.0-74.2
- Fixes to make rawhide boot in enforcing mode with latest systemd changes

* Wed Jan 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-74
- Add labeling for /var/run/systemd/journal/syslog
- libvirt sends signals to ifconfig
- Allow domains that read logind session files to list them

* Wed Jan 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-73
- Fixed destined form libvirt-sandbox
- Allow apps that list sysfs to also read sympolicy links in this filesystem
- Add ubac_constrained rules for chrome_sandbox
- Need interface to allow domains to use tmpfs_t files created by the kernel, used by libra
- Allow postgresql to be executed by the caller
- Standardize interfaces of daemons 
- Add new labeling for mm-handler
- Allow all matahari domains to read network state and etc_runtime_t files

* Wed Jan 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-72
- New fix for seunshare, requires seunshare_domains to be able to mounton /
- Allow systemctl running as logrotate_t to connect to private systemd socket
- Allow tmpwatch to read meminfo
- Allow rpc.svcgssd to read supported_krb5_enctype
- Allow zarafa domains to read /dev/random and /dev/urandom
- Allow snmpd to read dev_snmp6
- Allow procmail to talk with cyrus
- Add fixes for check_disk and check_nagios plugins

* Tue Dec 20 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-71
- default trans rules for Rawhide policy
-  Make sure sound_devices controlC* are labeled correctly on creation
- sssd now needs sys_admin
- Allow snmp to read all proc_type
- Allow to setup users homedir with quota.group

* Mon Dec 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-70
- Add httpd_can_connect_ldap() interface
- apcupsd_t needs to use seriel ports connected to usb devices
- Kde puts procmail mail directory under ~/.local/share
- nfsd_t can trigger sys_rawio on tests that involve too many mountpoints, dontaudit for now
- Add labeling for /sbin/iscsiuio

* Wed Dec 14 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-69
- Add label for /var/lib/iscan/interpreter
- Dont audit writes to leaked file descriptors or redirected output for nacl
- NetworkManager needs to write to /sys/class/net/ib*/mode

* Tue Dec 13 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-68
- Allow abrt  to request the kernel to load a module
- Make sure mozilla content is labeled correctly
- Allow tgtd to read system state
- More fixes for boinc
  * allow to resolve dns name
  * re-write boinc policy to use boinc_domain attribute
- Allow munin services plugins to use NSCD services

* Thu Dec 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-67
- Allow mozilla_plugin_t to manage mozilla_home_t
- Allow ssh derived domain to execute ssh-keygen in the ssh_keygen_t domain
- Add label for tumblerd

* Wed Dec 7 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-66
- Fixes for xguest package

* Tue Dec 6 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-65
- Fixes related to  /bin, /sbin
- Allow abrt to getattr on blk files
- Add type for rhev-agent log file
- Fix labeling for /dev/dmfm
- Dontaudit wicd leaking
- Allow systemd_logind_t to look at process info of apps that exchange dbus messages with it
- Label /etc/locale.conf correctly
- Allow user_mail_t to read /dev/random
- Allow postfix-smtpd to read MIMEDefang
- Add label for /var/log/suphp.log
- Allow swat_t to connect and read/write nmbd_t sock_file
- Allow systemd-tmpfiles to setattr for /run/user/gdm/dconf
- Allow systemd-tmpfiles to change user identity in object contexts
- More fixes for rhev_agentd_t consolehelper policy

* Thu Dec 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-64
- Use fs_use_xattr for squashf
-  Fix procs_type interface
- Dovecot has a new fifo_file /var/run/dovecot/stats-mail
- Dovecot has a new fifo_file /var/run/stats-mail
- Colord does not need to connect to network
- Allow system_cronjob to dbus chat with NetworkManager
- Puppet manages content, want to make sure it labels everything correctly

* Tue Nov 29 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-63
- Change port 9050 to tor_socks_port_t and then allow openvpn to connect to it
- Allow all postfix domains to use the fifo_file
- Allow sshd_t to getattr on all file systems in order to generate avc on nfs_t
- Allow apmd_t to read grub.cfg
- Let firewallgui read the selinux config
- Allow systemd-tmpfiles to delete content in /root that has been moved to /tmp
- Fix devicekit_manage_pid_files() interface
- Allow squid to check the network state
- Dontaudit colord getattr on file systems
- Allow ping domains to read zabbix_tmp_t files

* Wed Nov 23 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-59
- Allow mcelog_t to create dir and file in /var/run and label it correctly
- Allow dbus to manage fusefs
- Mount needs to read process state when mounting gluster file systems
- Allow collectd-web to read collectd lib files
- Allow daemons and system processes started by init to read/write the unix_stream_socket passed in from as stdin/stdout/stderr
- Allow colord to get the attributes of tmpfs filesystem
- Add sanlock_use_nfs and sanlock_use_samba booleans
- Add bin_t label for /usr/lib/virtualbox/VBoxManage

* Wed Nov 16 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-58
- Add ssh_dontaudit_search_home_dir
- Changes to allow namespace_init_t to work
- Add interface to allow exec of mongod, add port definition for mongod port, 27017
- Label .kde/share/apps/networkmanagement/certificates/ as home_cert_t
- Allow spamd and clamd to steam connect to each other
- Add policy label for passwd.OLD
- More fixes for postfix and postfix maildro
- Add ftp support for mozilla plugins
- Useradd now needs to manage policy since it calls libsemanage
- Fix devicekit_manage_log_files() interface
- Allow colord to execute ifconfig
- Allow accountsd to read /sys
- Allow mysqld-safe to execute shell
- Allow openct to stream connect to pcscd
- Add label for /var/run/nm-dns-dnsmasq\.conf
- Allow networkmanager to chat with virtd_t

* Fri Nov 11 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-57
- Pulseaudio changes
- Merge patches 

* Thu Nov 10 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-56
- Merge patches back into git repository.

* Tue Nov 8 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-55.2
- Remove allow_execmem boolean and replace with deny_execmem boolean

* Tue Nov 8 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-55.1
- Turn back on allow_execmem boolean

* Mon Nov 7 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-55
- Add more MCS fixes to make sandbox working
- Make faillog MLS trusted to make sudo_$1_t working
- Allow sandbox_web_client_t to read passwd_file_t
- Add .mailrc file context
- Remove execheap from openoffice domain
- Allow chrome_sandbox_nacl_t to read cpu_info
- Allow virtd to relabel generic usb which is need if USB device
- Fixes for virt.if interfaces to consider chr_file as image file type

* Fri Nov 4 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-54.1
- Remove Open Office policy
- Remove execmem policy

* Fri Nov 4 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-54
- MCS fixes
- quota fixes

* Thu Nov 3 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-53.1
- Remove transitions to consoletype

* Tue Nov 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-53
- Make nvidia* to be labeled correctly
- Fix abrt_manage_cache() interface
- Make filetrans rules optional so base policy will build
- Dontaudit chkpwd_t access to inherited TTYS
- Make sure postfix content gets created with the correct label
- Allow gnomeclock to read cgroup
- Fixes for cloudform policy

* Thu Oct 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-52
- Check in fixed for Chrome nacl support

* Thu Oct 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-51
-  Begin removing qemu_t domain, we really no longer need this domain.  
- systemd_passwd needs dac_overide to communicate with users TTY's
- Allow svirt_lxc domains to send kill signals within their container

* Thu Oct 27 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-50.2
- Remove qemu.pp again without causing a crash

* Wed Oct 26 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-50.1
- Remove qemu.pp, everything should use svirt_t or stay in its current domain	

* Wed Oct 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-50
- Allow policykit to talk to the systemd via dbus
- Move chrome_sandbox_nacl_t to permissive domains
- Additional rules for chrome_sandbox_nacl

* Tue Oct 25 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-49
- Change bootstrap name to nacl
- Chrome still needs execmem
- Missing role for chrome_sandbox_bootstrap
- Add boolean to remove execmem and execstack from virtual machines
- Dontaudit xdm_t doing an access_check on etc_t directories

* Mon Oct 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-48
- Allow named to connect to dirsrv by default
- add ldapmap1_0 as a krb5_host_rcache_t file
- Google chrome developers asked me to add bootstrap policy for nacl stuff
- Allow rhev_agentd_t to getattr on mountpoints
- Postfix_smtpd_t needs access to milters and cleanup seems to read/write postfix_smtpd_t unix_stream_sockets

* Mon Oct 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-47
- Fixes for cloudform policies which need to connect to random ports
- Make sure if an admin creates modules content it creates them with the correct label
- Add port 8953 as a dns port used by unbound
- Fix file name transition for alsa and confined users

* Fri Oct 21 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-46.1
- Turn on mock_t and thumb_t for unconfined domains

* Fri Oct 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-46
- Policy update should not modify local contexts

* Thu Oct 20 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-45.1
- Remove ada policy

* Thu Oct 20 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-45
- Remove tzdata policy
- Add labeling for udev
- Add cloudform policy
- Fixes for bootloader policy

* Wed Oct 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-43
- Add policies for nova openstack

* Tue Oct 18 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-42
- Add fixes for nova-stack policy

* Tue Oct 18 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-41
- Allow svirt_lxc_domain to chr_file and blk_file devices if they are in the domain
- Allow init process to setrlimit on itself
- Take away transition rules for users executing ssh-keygen
- Allow setroubleshoot_fixit_t to read /dev/urand
- Allow sshd to relbale tunnel sockets
- Allow fail2ban domtrans to shorewall in the same way as with iptables
- Add support for lnk files in the /var/lib/sssd directory
- Allow system mail to connect to courier-authdaemon over an unix stream socket

* Mon Oct 17 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-40.2
- Add passwd_file_t for /etc/ptmptmp

* Fri Oct 14 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-40
- Dontaudit access checks for all executables, gnome-shell is doing access(EXEC, X_OK)
- Make corosync to be able to relabelto cluster lib fies
- Allow samba domains to search /var/run/nmbd
- Allow dirsrv to use pam
- Allow thumb to call getuid
- chrome less likely to get mmap_zero bug so removing dontaudit
- gimp help-browser has built in javascript
- Best guess is that devices named /dev/bsr4096 should be labeled as cpu_device_t
- Re-write glance policy

* Thu Oct 13 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-39.3
- Move dontaudit sys_ptrace line from permissive.te to domain.te
- Remove policy for hal, it no longer exists

* Wed Oct 12 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-39.2
- Don't check md5 size or mtime on certain config files

* Tue Oct 11 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-39.1
- Remove allow_ptrace and replace it with deny_ptrace, which will remove all 
ptrace from the system
- Remove 2000 dontaudit rules between confined domains on transition
and replace with single
dontaudit domain domain:process { noatsecure siginh rlimitinh } ;

* Mon Oct 10 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-39
- Fixes for bootloader policy
- $1_gkeyringd_t needs to read $HOME/%%USER/.local/share/keystore
- Allow nsplugin to read /usr/share/config
- Allow sa-update to update rules
- Add use_fusefs_home_dirs for chroot ssh option
- Fixes for grub2
- Update systemd_exec_systemctl() interface
- Allow gpg to read the mail spool
- More fixes for sa-update running out of cron job
- Allow ipsec_mgmt_t to read hardware state information
- Allow pptp_t to connect to unreserved_port_t
- Dontaudit getattr on initctl in /dev from chfn
- Dontaudit getattr on kernel_core from chfn
- Add systemd_list_unit_dirs to systemd_exec_systemctl call
- Fixes for collectd policy
- CHange sysadm_t to create content as user_tmp_t under /tmp

* Thu Oct 6 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-38.1
- Shrink size of policy through use of attributes for userdomain and apache

* Wed Oct 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-38
- Allow virsh to read xenstored pid file
- Backport corenetwork fixes from upstream
- Do not audit attempts by thumb to search config_home_t dirs (~/.config)
- label ~/.cache/telepathy/logger telepathy_logger_cache_home_t
- allow thumb to read generic data home files (mime.type)

* Wed Oct 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-37
- Allow nmbd to manage sock file in /var/run/nmbd
- ricci_modservice send syslog msgs
- Stop transitioning from unconfined_t to ldconfig_t, but make sure /etc/ld.so.cache is labeled correctly
- Allow systemd_logind_t to manage /run/USER/dconf/user

* Tue Oct 4 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-36.1
- Fix missing patch from F16

* Mon Oct 3 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-36
- Allow logrotate setuid and setgid since logrotate is supposed to do it
- Fixes for thumb policy by grift
- Add new nfsd ports
- Added fix to allow confined apps to execmod on chrome
- Add labeling for additional vdsm directories
- Allow Exim and Dovecot SASL
- Add label for /var/run/nmbd
- Add fixes to make virsh and xen working together
- Colord executes ls
- /var/spool/cron  is now labeled as user_cron_spool_t

* Mon Oct 3 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-35
- Stop complaining about leaked file descriptors during install

* Fri Sep 30 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-34.7
- Remove java and mono module and merge into execmem

* Fri Sep 30 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-34.6
- Fixes for thumb policy and passwd_file_t

* Fri Sep 30 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-34.4
- Fixes caused by the labeling of /etc/passwd
- Add thumb.patch to transition unconfined_t to thumb_t for Rawhide

* Thu Sep 29 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-34.3
- Add support for Clustered Samba commands
- Allow ricci_modrpm_t to send log msgs
- move permissive virt_qmf_t from virt.te to permissivedomains.te
- Allow ssh_t to use kernel keyrings
- Add policy for libvirt-qmf and more fixes for linux containers
- Initial Polipo
- Sanlock needs to run ranged in order to kill svirt processes
- Allow smbcontrol to stream connect to ctdbd

* Mon Sep 26 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-34.2
- Add label for /etc/passwd

* Mon Sep 26 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-34.1
- Change unconfined_domains to permissive for Rawhide
- Add definition for the ephemeral_ports

* Mon Sep 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-34
- Make mta_role() active
- Allow asterisk to connect to jabber client port
- Allow procmail to read utmp
- Add NIS support for systemd_logind_t
- Allow systemd_logind_t to manage /run/user/$USER/dconf dir which is labeled as config_home_t
- Fix systemd_manage_unit_dirs() interface
- Allow ssh_t to manage directories passed into it
- init needs to be able to create and delete unit file directories
- Fix typo in apache_exec_sys_script
- Add ability for logrotate to transition to awstat domain

* Fri Sep 23 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-33
- Change screen to use screen_domain attribute and allow screen_domains to read all process domain state
- Add SELinux support for ssh pre-auth net process in F17
- Add logging_syslogd_can_sendmail boolean

* Wed Sep 21 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-31.1
- Add definition for ephemeral ports
- Define user_tty_device_t as a customizable_type

* Tue Sep 20 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-31
- Needs to require a new version of checkpolicy
- Interface fixes

* Fri Sep 16 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-29
- Allow sanlock to manage virt lib files
- Add virt_use_sanlock booelan
- ksmtuned is trying to resolve uids
- Make sure .gvfs is labeled user_home_t in the users home directory
- Sanlock sends kill signals and needs the kill capability
- Allow mockbuild to work on nfs homedirs
- Fix kerberos_manage_host_rcache() interface
- Allow exim to read system state

* Tue Sep 13 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-28
- Allow systemd-tmpfiles to set the correct labels on /var/run, /tmp and other files
- We want any file type that is created in /tmp by a process running as initrc_t to be labeled initrc_tmp_t

* Tue Sep 13 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-27
-  Allow collectd to read hardware state information
- Add loop_control_device_t
- Allow mdadm to request kernel to load module
- Allow domains that start other domains via systemctl to search unit dir
- systemd_tmpfiles, needs to list any file systems mounted on /tmp
- No one can explain why radius is listing the contents of /tmp, so we will dontaudit
- If I can manage etc_runtime files, I should be able to read the links
- Dontaudit hostname writing to mock library chr_files
- Have gdm_t setup labeling correctly in users home dir
- Label content unde /var/run/user/NAME/dconf as config_home_t
- Allow sa-update to execute shell
- Make ssh-keygen working with fips_enabled
- Make mock work for staff_t user
- Tighten security on mock_t

* Fri Sep 9 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-26
- removing unconfined_notrans_t no longer necessary
- Clean up handling of secure_mode_insmod and secure_mode_policyload
- Remove unconfined_mount_t

* Tue Sep 6 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-25
- Add exim_exec_t label for /usr/sbin/exim_tidydb
- Call init_dontaudit_rw_stream_socket() interface in mta policy
- sssd need to search /var/cache/krb5rcache directory
- Allow corosync to relabel own tmp files
- Allow zarafa domains to send system log messages
- Allow ssh to do tunneling
- Allow initrc scripts to sendto init_t unix_stream_socket
- Changes to make sure dmsmasq and virt directories are labeled correctly
- Changes needed to allow sysadm_t to manage systemd unit files
- init is passing file descriptors to dbus and on to system daemons
- Allow sulogin additional access Reported by dgrift and Jeremy Miller
- Steve Grubb believes that wireshark does not need this access
- Fix /var/run/initramfs to stop restorecon from looking at
- pki needs another port
- Add more labels for cluster scripts
- Allow apps that manage cgroup_files to manage cgroup link files
- Fix label on nfs-utils scripts directories
- Allow gatherd to read /dev/rand and /dev/urand

* Wed Aug 31 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-24
- pki needs another port
- Add more labels for cluster scripts
- Fix label on nfs-utils scripts directories
- Fixes for cluster
- Allow gatherd to read /dev/rand and /dev/urand
- abrt leaks fifo files

* Tue Aug 30 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-23
- Add glance policy
- Allow mdadm setsched
- /var/run/initramfs should not be relabeled with a restorecon run
- memcache can be setup to override sys_resource
- Allow httpd_t to read tetex data
- Allow systemd_tmpfiles to delete kernel modules left in /tmp directory.

* Mon Aug 29 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-22
- Allow Postfix to deliver to Dovecot LMTP socket
- Ignore bogus sys_module for lldpad
- Allow chrony and gpsd to send dgrams, gpsd needs to write to the real time clock
- systemd_logind_t sets the attributes on usb devices
- Allow hddtemp_t to read etc_t files
- Add permissivedomains module
- Move all permissive domains calls to permissivedomain.te
- Allow pegasis to send kill signals to other UIDs

* Wed Aug 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-21
- Allow insmod_t to use fds leaked from devicekit
- dontaudit getattr between insmod_t and init_t unix_stream_sockets
- Change sysctl unit file interfaces to use systemctl
- Add support for chronyd unit file
- Allow mozilla_plugin to read gnome_usr_config
- Add policy for new gpsd
- Allow cups to create kerberos rhost cache files
- Add authlogin_filetrans_named_content, to unconfined_t to make sure shadow and other log files get labeled correctly

* Tue Aug 23 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-20
- Make users_extra and seusers.final into config(noreplace) so semanage users and login does not get overwritten

* Tue Aug 23 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-19
- Add policy for sa-update being run out of cron jobs
- Add create perms to postgresql_manage_db
- ntpd using a gps has to be able to read/write generic tty_device_t
- If you disable unconfined and unconfineduser, rpm needs more privs to manage /dev
- fix spec file
- Remove qemu_domtrans_unconfined() interface
- Make passenger working together with puppet
- Add init_dontaudit_rw_stream_socket interface
- Fixes for wordpress

* Thu Aug 11 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-18
- Turn on allow_domain_fd_use boolean on F16
- Allow syslog to manage all log files
- Add use_fusefs_home_dirs boolean for chrome
- Make vdagent working with confined users
- Add abrt_handle_event_t domain for ABRT event scripts
- Labeled /usr/sbin/rhnreg_ks as rpm_exec_t and added changes related to this change
- Allow httpd_git_script_t to read passwd data
- Allow openvpn to set its process priority when the nice parameter is used

* Wed Aug 10 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-17
- livecd fixes
- spec file fixes 

* Thu Aug 4 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-16
- fetchmail can use kerberos
- ksmtuned reads in shell programs
- gnome_systemctl_t reads the process state of ntp
- dnsmasq_t asks the kernel to load multiple kernel modules
- Add rules for domains executing systemctl
- Bogus text within fc file

* Wed Aug 3 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-14
- Add cfengine policy

* Tue Aug 2 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-13
- Add abrt_domain attribute
- Allow corosync to manage cluster lib files
- Allow corosync to connect to the system DBUS

* Mon Aug 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-12
- Add sblim, uuidd policies
- Allow kernel_t dyntrasition to init_t

* Fri Jul 29 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-11
- init_t need setexec
- More fixes of rules which cause an explosion in rules by Dan Walsh

* Tue Jul 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-10
- Allow rcsmcertd to perform DNS name resolution
- Add dirsrvadmin_unconfined_script_t domain type for 389-ds admin scripts
- Allow tmux to run as screen
- New policy for collectd
- Allow gkeyring_t to interact with all user apps
- Add rules to allow firstboot to run on machines with the unconfined.pp module removed

* Sat Jul 23 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-9
- Allow systemd_logind to send dbus messages with users
- allow accountsd to read wtmp file
- Allow dhcpd to get and set capabilities

* Fri Jul 22 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-8
- Fix oracledb_port definition
- Allow mount to mounton the selinux file system
- Allow users to list /var directories

* Thu Jul 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-7
- systemd fixes

* Tue Jul 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-6
- Add initial policy for abrt_dump_oops_t
- xtables-multi wants to getattr of the proc fs
- Smoltclient is connecting to abrt
- Dontaudit leaked file descriptors to postdrop
- Allow abrt_dump_oops to look at kernel sysctls
- Abrt_dump_oops_t reads kernel ring buffer
- Allow mysqld to request the kernel to load modules
- systemd-login needs fowner
- Allow postfix_cleanup_t to searh maildrop

* Mon Jul 18 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-5
- Initial systemd_logind policy
- Add policy for systemd_logger and additional proivs for systemd_logind
- More fixes for systemd policies

* Thu Jul 14 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-4
- Allow setsched for virsh
- Systemd needs to impersonate cups, which means it needs to create tcp_sockets in cups_t domain, as well as manage spool directories
- iptables: the various /sbin/ip6?tables.* are now symlinks for
/sbin/xtables-multi

* Tue Jul 12 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-3
- A lot of users are running yum -y update while in /root which is causing ldconfig to list the contents, adding dontaudit
- Allow colord to interact with the users through the tmpfs file system
- Since we changed the label on deferred, we need to allow postfix_qmgr_t to be able to create maildrop_t files
- Add label for /var/log/mcelog
- Allow asterisk to read /dev/random if it uses TLS
- Allow colord to read ini files which are labeled as bin_t
- Allow dirsrvadmin sys_resource and setrlimit to use ulimit
- Systemd needs to be able to create sock_files for every label in /var/run directory, cupsd being the first.  
- Also lists /var and /var/spool directories
- Add openl2tpd to l2tpd policy
- qpidd is reading the sysfs file

* Thu Jun 30 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-2
- Change usbmuxd_t to dontaudit attempts to read chr_file
- Add mysld_safe_exec_t for libra domains to be able to start private mysql domains
- Allow pppd to search /var/lock dir
- Add rhsmcertd policy

* Mon Jun 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-1
- Update to upstream

* Mon Jun 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-30
- More fixes
  * http://git.fedorahosted.org/git/?p=selinux-policy.git

* Thu Jun 16 2011 Dan Walsh <dwalsh@redhat.com> 3.9.16-29.1
- Fix spec file to not report Verify errors

* Thu Jun 16 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-29
- Add dspam policy
- Add lldpad policy
- dovecot auth wants to search statfs #713555
- Allow systemd passwd apps to read init fifo_file
- Allow prelink to use inherited terminals
- Run cherokee in the httpd_t domain
- Allow mcs constraints on node connections
- Implement pyicqt policy
- Fixes for zarafa policy
- Allow cobblerd to send syslog messages

* Wed Jun 8 2011 Dan Walsh <dwalsh@redhat.com> 3.9.16-28.1
- Add policy.26 to the payload
- Remove olpc stuff
- Remove policygentool

* Wed Jun 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-27
- Fixes for zabbix
- init script needs to be able to manage sanlock_var_run_...
- Allow sandlock and wdmd to create /var/run directories... 
- mixclip.so has been compiled correctly
- Fix passenger policy module name

* Tue Jun 7 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-26
- Add mailscanner policy from dgrift
- Allow chrome to optionally be transitioned to
- Zabbix needs these rules when starting the zabbix_server_mysql
- Implement a type for freedesktop openicc standard (~/.local/share/icc)
- Allow system_dbusd_t to read inherited icc_data_home_t files.
- Allow colord_t to read icc_data_home_t content. #706975
- Label stuff under /usr/lib/debug as if it was labeled under /

* Thu Jun 2 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-25
- Fixes for sanlock policy
- Fixes for colord policy
- Other fixes
	* http://git.fedorahosted.org/git/?p=selinux-policy.git;a=log

* Thu May 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-24
- Add rhev policy module to modules-targeted.conf

* Tue May 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-23
- Lot of fixes
	* http://git.fedorahosted.org/git/?p=selinux-policy.git;a=log

* Thu May 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-22
- Allow logrotate to execute systemctl
- Allow nsplugin_t to getattr on gpmctl
- Fix dev_getattr_all_chr_files() interface
- Allow shorewall to use inherited terms
- Allow userhelper to getattr all chr_file devices
- sandbox domains should be able to getattr and dontaudit search of sysctl_kernel_t
- Fix labeling for ABRT Retrace Server

* Mon May 9 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-21
- Dontaudit sys_module for ifconfig
- Make telepathy and gkeyringd daemon working with confined users
- colord wants to read files in users homedir
- Remote login should be creating user_tmp_t not its own tmp files

* Thu May 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-20
- Fix label for /usr/share/munin/plugins/munin_* plugins
- Add support for zarafa-indexer
- Fix boolean description
- Allow colord to getattr on /proc/scsi/scsi
- Add label for /lib/upstart/init
- Colord needs to list /mnt

* Tue May 3 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-19
- Forard port changes from F15 for telepathy
- NetworkManager should be allowed to use /dev/rfkill
- Fix dontaudit messages to say Domain to not audit
- Allow telepathy domains to read/write gnome_cache files
- Allow telepathy domains to call getpw
- Fixes for colord and vnstatd policy

* Wed Apr 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-18
- Allow init_t getcap and setcap
- Allow namespace_init_t to use nsswitch
- aisexec will execute corosync
- colord tries to read files off noxattr file systems
- Allow init_t getcap and setcap

* Thu Apr 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-17
- Add support for ABRT retrace server
- Allow user_t and staff_t access to generic scsi to handle locally plugged in scanners
- Allow telepath_msn_t to read /proc/PARENT/cmdline
- ftpd needs kill capability
- Allow telepath_msn_t to connect to sip port
- keyring daemon does not work on nfs homedirs
- Allow $1_sudo_t to read default SELinux context
- Add label for tgtd sock file in /var/run/
- Add apache_exec_rotatelogs interface
- allow all zaraha domains to signal themselves, server writes to /tmp
- Allow syslog to read the process state
- Add label for /usr/lib/chromium-browser/chrome
- Remove the telepathy transition from unconfined_t
- Dontaudit sandbox domains trying to mounton sandbox_file_t, this is caused by fuse mounts
- Allow initrc_t domain to manage abrt pid files
- Add support for AEOLUS project
- Virt_admin should be allowed to manage images and processes
- Allow plymountd to send signals to init
- Change labeling of fping6

* Tue Apr 19 2011 Dan Walsh <dwalsh@redhat.com> 3.9.16-16.1
- Add filename transitions

* Tue Apr 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-16
- Fixes for zarafa policy
- Add support for AEOLUS project
- Change labeling of fping6
- Allow plymountd to send signals to init
- Allow initrc_t domain to manage abrt pid files
- Virt_admin should be allowed to manage images and processes

* Fri Apr 15 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-15
- xdm_t needs getsession for switch user 
- Every app that used to exec init is now execing systemdctl 
- Allow squid to manage krb5_host_rcache_t files 
- Allow foghorn to connect to agentx port - Fixes for colord policy

* Mon Apr 11 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-14
- Add Dan's patch to remove 64 bit variants
- Allow colord to use unix_dgram_socket 
- Allow apps that search pids to read /var/run if it is a lnk_file 
- iscsid_t creates its own directory 
- Allow init to list var_lock_t dir 
- apm needs to verify user accounts auth_use_nsswitch
- Add labeling for systemd unit files
- Allow gnomeclok to enable ntpd service using systemctl - systemd_systemctl_t domain was added
- Add label for matahari-broker.pid file
- We want to remove untrustedmcsprocess from ability to read /proc/pid
- Fixes for matahari policy
- Allow system_tmpfiles_t to delete user_home_t files in the /tmp dir
- Allow sshd to transition to sysadm_t if ssh_sysadm_login is turned on

* Tue Apr 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-13
- Fix typo

* Mon Apr 4 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-12
- Add /var/run/lock /var/lock definition to file_contexts.subs
- nslcd_t is looking for kerberos cc files
- SSH_USE_STRONG_RNG is 1 which requires /dev/random
- Fix auth_rw_faillog definition
- Allow sysadm_t to set attributes on fixed disks
- allow user domains to execute lsof and look at application sockets
- prelink_cron job calls telinit -u if init is rewritten
- Fixes to run qemu_t from staff_t

* Mon Apr 4 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-11
- Fix label for /var/run/udev to udev_var_run_t
- Mock needs to be able to read network state

* Fri Apr 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-10
- Add file_contexts.subs to handle /run and /run/lock
- Add other fixes relating to /run changes from F15 policy

* Fri Mar 25 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-7
- Allow $1_sudo_t and $1_su_t open access to user terminals
- Allow initrc_t to use generic terminals
- Make Makefile/Rules.modular run sepolgen-ifgen during build to check if files for bugs
-systemd is going to be useing /run and /run/lock for early bootup files.
- Fix some comments in rlogin.if
- Add policy for KDE backlighthelper
- sssd needs to read ~/.k5login in nfs, cifs or fusefs file systems
- sssd wants to read .k5login file in users homedir
- setroubleshoot reads executables to see if they have TEXTREL
- Add /var/spool/audit support for new version of audit
- Remove kerberos_connect_524() interface calling
- Combine kerberos_master_port_t and kerberos_port_t
- systemd has setup /dev/kmsg as stderr for apps it executes
- Need these access so that init can impersonate sockets on unix_dgram_socket

* Wed Mar 23 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-6
- Remove some unconfined domains
- Remove permissive domains
- Add policy-term.patch from Dan 

* Thu Mar 17 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-5
- Fix multiple specification for boot.log
- devicekit leaks file descriptors to setfiles_t
- Change all all_nodes to generic_node and all_if to generic_if
- Should not use deprecated interface
- Switch from using all_nodes to generic_node and from all_if to generic_if
- Add support for xfce4-notifyd
- Fix file context to show several labels as SystemHigh
- seunshare needs to be able to mounton nfs/cifs/fusefs homedirs
- Add etc_runtime_t label for /etc/securetty
- Fixes to allow xdm_t to start gkeyringd_USERTYPE_t directly
- login.krb needs to be able to write user_tmp_t
- dirsrv needs to bind to port 7390 for dogtag
- Fix a bug in gpg policy
- gpg sends audit messages
- Allow qpid to manage matahari files

* Tue Mar 15 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-4
- Initial policy for matahari
- Add dev_read_watchdog
- Allow clamd to connect clamd port
- Add support for kcmdatetimehelper
- Allow shutdown to setrlimit and sys_nice
- Allow systemd_passwd to talk to /dev/log before udev or syslog is running
- Purge chr_file and blk files on /tmp
- Fixes for pads
- Fixes for piranha-pulse
- gpg_t needs to be able to encyprt anything owned by the user

* Thu Mar 10 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-3
- mozilla_plugin_tmp_t needs to be treated as user tmp files
- More dontaudits of writes from readahead
- Dontaudit readahead_t file_type:dir write, to cover up kernel bug
- systemd_tmpfiles needs to relabel faillog directory as well as the file
- Allow hostname and consoletype to r/w inherited initrc_tmp_t files handline hostname >> /tmp/myhost

* Thu Mar 10 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-2
- Add policykit fixes from Tim Waugh
- dontaudit sandbox domains sandbox_file_t:dir mounton
- Add new dontaudit rules for sysadm_dbusd_t
- Change label for /var/run/faillock
	* other fixes which relate with this change

* Tue Mar 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-1
- Update to upstream
- Fixes for telepathy
- Add port defition for ssdp port
- add policy for /bin/systemd-notify from Dan
- Mount command requires users read mount_var_run_t
- colord needs to read konject_uevent_socket
- User domains connect to the gkeyring socket
- Add colord policy and allow user_t and staff_t to dbus chat with it
- Add lvm_exec_t label for kpartx
- Dontaudit reading the mail_spool_t link from sandbox -X
- systemd is creating sockets in avahi_var_run and system_dbusd_var_run

* Tue Mar 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.15-5
- gpg_t needs to talk to gnome-keyring
- nscd wants to read /usr/tmp->/var/tmp to generate randomziation in unixchkpwd
- enforce MCS labeling on nodes
- Allow arpwatch to read meminfo
- Allow gnomeclock to send itself signals
- init relabels /dev/.udev files on boot
- gkeyringd has to transition back to staff_t when it runs commands in bin_t or shell_exec_t
- nautilus checks access on /media directory before mounting usb sticks, dontaudit access_check on mnt_t
- dnsmasq can run as a dbus service, needs acquire service
- mysql_admin should  be allowed to connect to mysql service
- virt creates monitor sockets in the users home dir

* Mon Feb 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.15-2
- Allow usbhid-ups to read hardware state information
- systemd-tmpfiles has moved
- Allo cgroup to sys_tty_config
- For some reason prelink is attempting to read gconf settings
- Add allow_daemons_use_tcp_wrapper boolean
- Add label for ~/.cache/wocky to make telepathy work in enforcing mode
- Add label for char devices /dev/dasd*
- Fix for apache_role
- Allow amavis to talk to nslcd
- allow all sandbox to read selinux poilcy config files
- Allow cluster domains to use the system bus and send each other dbus messages

* Wed Feb 16 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.15-1
- Update to upstream

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 8 2011 Dan Walsh <dwalsh@redhat.com> 3.9.14-1
- Update to ref policy
- cgred needs chown capability
- Add /dev/crash crash_dev_t
- systemd-readahead wants to use fanotify which means readahead_t needs sys_admin capability

* Tue Feb 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-10
- New labeling for postfmulti #675654
- dontaudit xdm_t listing noxattr file systems
- dovecot-auth needs to be able to connect to mysqld via the network as well as locally
- shutdown is passed stdout to a xdm_log_t file
- smartd creates a fixed disk device
- dovecot_etc_t contains a lnk_file that domains need to read
- mount needs to be able to read etc_runtim_t:lnk_file since in rawhide this is a link created at boot

* Thu Feb 3 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-9
- syslog_t needs syslog capability
- dirsrv needs to be able to create /var/lib/snmp
- Fix labeling for dirsrv
- Fix for dirsrv policy missing manage_dirs_pattern
- corosync needs to delete clvm_tmpfs_t files
- qdiskd needs to list hugetlbfs
- Move setsched to sandbox_x_domain, so firefox can run without network access
- Allow hddtemp to read removable devices
- Adding syslog and read_policy permissions to policy
	* syslog
		Allow unconfined, sysadm_t, secadm_t, logadm_t
	* read_policy
		allow unconfined, sysadm_t, secadm_t, staff_t on Targeted
		allow sysadm_t (optionally), secadm_t on MLS
- mdadm application will write into /sys/.../uevent whenever arrays are
assembled or disassembled.

* Tue Feb 1 2011 Dan Walsh <dwalsh@redhat.com> 3.9.13-8
- Add tcsd policy

* Tue Feb 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-7
- ricci_modclusterd_t needs to bind to rpc ports 500-1023
- Allow dbus to use setrlimit to increase resoueces
- Mozilla_plugin is leaking to sandbox
- Allow confined users  to connect to lircd over unix domain stream socket which allow to use remote control
- Allow awstats to read squid logs
- seunshare needs to manage tmp_t
- apcupsd cgi scripts have a new directory

* Thu Jan 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-6
- Fix xserver_dontaudit_read_xdm_pid
- Change oracle_port_t to oracledb_port_t to prevent conflict with satellite
- Allow dovecot_deliver_t to read/write postfix_master_t:fifo_file. 
	* These fifo_file is passed from postfix_master_t to postfix_local_t to dovecot_deliver_t
- Allow readahead to manage readahead pid dirs
- Allow readahead to read all mcs levels
- Allow mozilla_plugin_t to use nfs or samba homedirs

* Tue Jan 25 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-5
- Allow nagios plugin to read /proc/meminfo
- Fix for mozilla_plugin
- Allow samba_net_t to create /etc/keytab
- pppd_t setting up vpns needs to run unix_chkpwd, setsched its process and write wtmp_t
- nslcd can read user credentials
- Allow nsplugin to delete mozilla_plugin_tmpfs_t
- abrt tries to create dir in rpm_var_lib_t
- virt relabels fifo_files
- sshd needs to manage content in fusefs homedir
- mock manages link files in cache dir

* Fri Jan 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-4
- nslcd needs setsched and to read /usr/tmp
- Invalid call in likewise policy ends up creating a bogus role
- Cannon puts content into /var/lib/bjlib that cups needs to be able to write
- Allow screen to create screen_home_t in /root
- dirsrv sends syslog messages
- pinentry reads stuff in .kde directory
- Add labels for .kde directory in homedir
- Treat irpinit, iprupdate, iprdump services with raid policy

* Wed Jan 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-3
- NetworkManager wants to read consolekit_var_run_t
- Allow readahead to create /dev/.systemd/readahead
- Remove permissive domains
- Allow newrole to run namespace_init

* Tue Jan 18 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-2
- Add sepgsql_contexts file

* Mon Jan 17 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-1
- Update to upstream

* Mon Jan 17 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.12-8
- Add oracle ports and allow apache to connect to them if the connect_db boolean is turned on
- Add puppetmaster_use_db boolean
- Fixes for zarafa policy
- Fixes for gnomeclock poliy
- Fix systemd-tmpfiles to use auth_use_nsswitch

* Fri Jan 14 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.12-7
- gnomeclock executes a shell
- Update for screen policy to handle pipe in homedir
- Fixes for polyinstatiated homedir
- Fixes for namespace policy and other fixes related to polyinstantiation
- Add namespace policy
- Allow dovecot-deliver transition to sendmail which is needed by sieve scripts
- Fixes for init, psad policy which relate with confined users
- Do not audit bootloader attempts to read devicekit pid files
- Allow nagios service plugins to read /proc

* Tue Jan 11 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.12-6
- Add firewalld policy
- Allow vmware_host to read samba config
- Kernel wants to read /proc Fix duplicate grub def in cobbler
- Chrony sends mail, executes shell, uses fifo_file and reads /proc
- devicekitdisk getattr all file systems
- sambd daemon writes wtmp file
- libvirt transitions to dmidecode

* Wed Jan 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.12-5
- Add initial policy for system-setup-keyboard which is now daemon
- Label /var/lock/subsys/shorewall as shorewall_lock_t
- Allow users to communicate with the gpg_agent_t
- Dontaudit mozilla_plugin_t using the inherited terminal
- Allow sambagui to read files in /usr
- webalizer manages squid log files
- Allow unconfined domains to bind ports to raw_ip_sockets
- Allow abrt to manage rpm logs when running yum
- Need labels for /var/run/bittlebee
- Label .ssh under amanda
- Remove unused genrequires for virt_domain_template
- Allow virt_domain to use fd inherited from virtd_t
- Allow iptables to read shorewall config

* Tue Dec 28 2010 Dan Walsh <dwalsh@redhat.com> 3.9.12-4
- Gnome apps list config_home_t
- mpd creates lnk files in homedir
- apache leaks write to mail apps on tmp files
- /var/stockmaniac/templates_cache contains log files
- Abrt list the connects of mount_tmp_t dirs
- passwd agent reads files under /dev and reads utmp file
- squid apache script connects to the squid port
- fix name of plymouth log file
- teamviewer is a wine app
- allow dmesg to read system state
- Stop labeling files under /var/lib/mock so restorecon will not go into this 
- nsplugin needs to read network state for google talk

* Thu Dec 23 2010 Dan Walsh <dwalsh@redhat.com> 3.9.12-3
- Allow xdm and syslog to use /var/log/boot.log
- Allow users to communicate with mozilla_plugin and kill it
- Add labeling for ipv6 and dhcp

* Tue Dec 21 2010 Dan Walsh <dwalsh@redhat.com> 3.9.12-2
- New labels for ghc http content
- nsplugin_config needs to read urand, lvm now calls setfscreate to create dev
- pm-suspend now creates log file for append access so we remove devicekit_wri
- Change authlogin_use_sssd to authlogin_nsswitch_use_ldap
- Fixes for greylist_milter policy

* Tue Dec 21 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.12-1
- Update to upstream
- Fixes for systemd policy
- Fixes for passenger policy
- Allow staff users to run mysqld in the staff_t domain, akonadi needs this
- Add bin_t label for /usr/share/kde4/apps/kajongg/kajongg.py
- auth_use_nsswitch does not need avahi to read passwords,needed for resolving data
- Dontaudit (xdm_t) gok attempting to list contents of /var/account
- Telepathy domains need to read urand
- Need interface to getattr all file classes in a mock library for setroubleshoot

* Wed Dec 15 2010 Dan Walsh <dwalsh@redhat.com> 3.9.11-2
- Update selinux policy to handle new /usr/share/sandbox/start script

* Wed Dec 15 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.11-1
- Update to upstream
- Fix version of policy in spec file

* Tue Dec 14 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-13
- Allow sandbox to run on nfs partitions, fixes for systemd_tmpfs
- remove per sandbox domains devpts types
- Allow dkim-milter sending signal to itself

* Mon Dec 13 2010 Dan Walsh <dwalsh@redhat.com> 3.9.10-12
- Allow domains that transition to ping or traceroute, kill them
- Allow user_t to conditionally transition to ping_t and traceroute_t
- Add fixes to systemd- tools, including new labeling for systemd-fsck, systemd-cryptsetup

* Mon Dec 13 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-11
- Turn on systemd policy
- mozilla_plugin needs to read certs in the homedir.
- Dontaudit leaked file descriptors from devicekit
- Fix ircssi to use auth_use_nsswitch
- Change to use interface without param in corenet to disable unlabelednet packets
- Allow init to relabel sockets and fifo files in /dev
- certmonger needs dac* capabilities to manage cert files not owned by root
- dovecot needs fsetid to change group membership on mail
- plymouthd removes /var/log/boot.log
- systemd is creating symlinks in /dev
- Change label on /etc/httpd/alias to be all cert_t

* Fri Dec 10 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-10
- Fixes for clamscan and boinc policy
- Add boinc_project_t setpgid
- Allow alsa to create tmp files in /tmp

* Tue Dec 7 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-9
- Push fixes to allow disabling of unlabeled_t packet access
- Enable unlabelednet policy

* Tue Dec 7 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-8
- Fixes for lvm to work with systemd

* Mon Dec 6 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-7
- Fix the label for wicd log
- plymouthd creates force-display-on-active-vt file
- Allow avahi to request the kernel to load a module
- Dontaudit hal leaks
- Fix gnome_manage_data interface
- Add new interface corenet_packet to define a type as being an packet_type.
- Removed general access to packet_type from icecast and squid.
- Allow mpd to read alsa config
- Fix the label for wicd log
- Add systemd policy

* Fri Dec 3 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-6
- Fix gnome_manage_data interface
- Dontaudit sys_ptrace capability for iscsid
- Fixes for nagios plugin policy

* Thu Dec 2 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-5
- Fix cron to run ranged when started by init
- Fix devicekit to use log files
- Dontaudit use of devicekit_var_run_t for fstools
- Allow init to setattr on logfile directories
- Allow hald to manage files in /var/run/pm-utils/ dir which is now labeled as devicekit_var_run_t

* Tue Nov 30 2010 Dan Walsh <dwalsh@redhat.com> 3.9.10-4
- Fix up handling of dnsmasq_t creating /var/run/libvirt/network
- Turn on sshd_forward_ports boolean by default
- Allow sysadmin to dbus chat with rpm
- Add interface for rw_tpm_dev
- Allow cron to execute bin
- fsadm needs to write sysfs
- Dontaudit consoletype reading /var/run/pm-utils
- Lots of new privs fro mozilla_plugin_t running java app, make mozilla_plugin
- certmonger needs to manage dirsrv data
- /var/run/pm-utils should be labeled as devicekit_var_run_t

* Tue Nov 30 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-3
- fixes to allow /var/run and /var/lock as tmpfs
- Allow chrome sandbox to connect to web ports
- Allow dovecot to listem on lmtp and sieve ports
- Allov ddclient to search sysctl_net_t
- Transition back to original domain if you execute the shell

* Thu Nov 25 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-2
- Remove duplicate declaration

* Thu Nov 25 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-1
- Update to upstream
- Cleanup for sandbox
- Add attribute to be able to select sandbox types

* Mon Nov 22 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.9-4
- Allow ddclient to fix file mode bits of ddclient conf file
- init leaks file descriptors to daemons
- Add labels for /etc/lirc/ and
- Allow amavis_t to exec shell
- Add label for gssd_tmp_t for /var/tmp/nfs_0

* Thu Nov 18 2010 Dan Walsh <dwalsh@redhat.com> 3.9.9-3
- Put back in lircd_etc_t so policy will install

* Thu Nov 18 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.9-2
- Turn on allow_postfix_local_write_mail_spool
- Allow initrc_t to transition to shutdown_t
- Allow logwatch and cron to mls_read_to_clearance for MLS boxes
- Allow wm to send signull to all applications and receive them from users
- lircd patch from field
- Login programs have to read /etc/samba
- New programs under /lib/systemd
- Abrt needs to read config files

* Tue Nov 16 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.9-1
- Update to upstream
- Dontaudit leaked sockets from userdomains to user domains
- Fixes for mcelog to handle scripts
- Apply patch from Ruben Kerkhof
- Allow syslog to search spool dirs

* Mon Nov 15 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.8-7
- Allow nagios plugins to read usr files
- Allow mysqld-safe to send system log messages
- Fixes fpr ddclient policy
- Fix sasl_admin interface
- Allow apache to search zarafa config
- Allow munin plugins to search /var/lib directory
- Allow gpsd to read sysfs_t
- Fix labels on /etc/mcelog/triggers to bin_t

* Fri Nov 12 2010 Dan Walsh <dwalsh@redhat.com> 3.9.8-6
- Remove saslauthd_tmp_t and transition tmp files to krb5_host_rcache_t
- Allow saslauthd_t to create krb5_host_rcache_t files in /tmp
- Fix xserver interface
- Fix definition of /var/run/lxdm

* Fri Nov 12 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.8-5
- Turn on mediawiki policy
- kdump leaks kdump_etc_t to ifconfig, add dontaudit
- uux needs to transition to uucpd_t
- More init fixes relabels man,faillog
- Remove maxima defs in libraries.fc
- insmod needs to be able to create tmpfs_t files
- ping needs setcap

* Wed Nov 10 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.8-4
- Allow groupd transition to fenced domain when executes fence_node
- Fixes for rchs policy
- Allow mpd to be able to read samba/nfs files

* Tue Nov 9 2010 Dan Walsh <dwalsh@redhat.com> 3.9.8-3
- Fix up corecommands.fc to match upstream
- Make sure /lib/systemd/* is labeled init_exec_t
- mount wants to setattr on all mountpoints
- dovecot auth wants to read dovecot etc files
- nscd daemon looks at the exe file of the comunicating daemon
- openvpn wants to read utmp file
- postfix apps now set sys_nice and lower limits
- remote_login (telnetd/login) wants to use telnetd_devpts_t and user_devpts_t to work correctly
- Also resolves nsswitch
- Fix labels on /etc/hosts.*
- Cleanup to make upsteam patch work
- allow abrt to read etc_runtime_t

* Fri Nov 5 2010 Dan Walsh <dwalsh@redhat.com> 3.9.8-2
- Add conflicts for dirsrv package

* Fri Nov 5 2010 Dan Walsh <dwalsh@redhat.com> 3.9.8-1
- Update to upstream
- Add vlock policy

* Wed Nov 3 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-10
- Fix sandbox to work on nfs homedirs
- Allow cdrecord to setrlimit
- Allow mozilla_plugin to read xauth
- Change label on systemd-logger to syslogd_exec_t
- Install dirsrv policy from dirsrv package

* Tue Nov 2 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-9
- Add virt_home_t, allow init to setattr on xserver_tmp_t and relabel it
- Udev needs to stream connect to init and kernel
- Add xdm_exec_bootloader boolean, which allows xdm to execute /sbin/grub and read files in /boot directory

* Mon Nov 1 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-8
- Allow NetworkManager to read openvpn_etc_t
- Dontaudit hplip to write of /usr dirs
- Allow system_mail_t to create /root/dead.letter as mail_home_t
- Add vdagent policy for spice agent daemon

* Thu Oct 28 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-7
- Dontaudit sandbox sending sigkill to all user domains
- Add policy for rssh_chroot_helper
- Add missing flask definitions
- Allow udev to relabelto removable_t
- Fix label on /var/log/wicd.log
- Transition to initrc_t from init when executing bin_t
- Add audit_access permissions to file
- Make removable_t a device_node 
- Fix label on /lib/systemd/*

* Fri Oct 22 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-6
- Fixes for systemd to manage /var/run
- Dontaudit leaks by firstboot

* Tue Oct 19 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-5
- Allow chome to create netlink_route_socket
- Add additional MATHLAB file context
- Define nsplugin as an application_domain
- Dontaudit sending signals from sandboxed domains to other domains
- systemd requires init to build /tmp /var/auth and /var/lock dirs
- mount wants to read devicekit_power /proc/ entries
- mpd wants to connect to soundd port
- Openoffice causes a setattr on a lib_t file for normal users, add dontaudit
- Treat lib_t and textrel_shlib_t directories the same
- Allow mount read access on virtual images

* Fri Oct 15 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-4
- Allow sandbox_x_domains to work with nfs/cifs/fusefs home dirs.
- Allow devicekit_power to domtrans to mount
- Allow dhcp to bind to udp ports > 1024 to do named stuff
- Allow ssh_t to exec ssh_exec_t
- Remove telepathy_butterfly_rw_tmp_files(), dev_read_printk() interfaces which are nolonger used
- Fix clamav_append_log() intefaces
- Fix 'psad_rw_fifo_file' interface

* Fri Oct 15 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-3
- Allow cobblerd to list cobler appache content

* Fri Oct 15 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-2
- Fixup for the latest version of upowed
- Dontaudit sandbox sending SIGNULL to desktop apps

* Wed Oct 13 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-1
- Update to upstream

* Tue Oct 12 2010 Dan Walsh <dwalsh@redhat.com> 3.9.6-3
-Mount command from a confined user generates setattr on /etc/mtab file, need to dontaudit this access
- dovecot-auth_t needs ipc_lock
- gpm needs to use the user terminal
- Allow system_mail_t to append ~/dead.letter
- Allow NetworkManager to edit /etc/NetworkManager/NetworkManager.conf
- Add pid file to vnstatd
- Allow mount to communicate with gfs_controld
- Dontaudit hal leaks in setfiles

* Fri Oct 8 2010 Dan Walsh <dwalsh@redhat.com> 3.9.6-2
- Lots of fixes for systemd
- systemd now executes readahead and tmpwatch type scripts
- Needs to manage random seed

* Thu Oct 7 2010 Dan Walsh <dwalsh@redhat.com> 3.9.6-1
- Allow smbd to use sys_admin
- Remove duplicate file context for tcfmgr
- Update to upstream

* Wed Oct 6 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-11
- Fix fusefs handling
- Do not allow sandbox to manage nsplugin_rw_t
- Allow mozilla_plugin_t to connecto its parent
- Allow init_t to connect to plymouthd running as kernel_t
- Add mediawiki policy
- dontaudit sandbox sending signals to itself.  This can happen when they are running at different mcs.
- Disable transition from dbus_session_domain to telepathy for F14
- Allow boinc_project to use shm
- Allow certmonger to search through directories that contain certs
- Allow fail2ban the DAC Override so it can read log files owned by non root users

* Mon Oct 4 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-10
- Start adding support for use_fusefs_home_dirs
- Add /var/lib/syslog directory file context
- Add /etc/localtime as locale file context

* Thu Sep 30 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-9
- Turn off default transition to mozilla_plugin and telepathy domains from unconfined user 
- Turn off iptables from unconfined user 
- Allow sudo to send signals to any domains the user could have transitioned to.
- Passwd in single user mode needs to talk to console_device_t
- Mozilla_plugin_t needs to connect to web ports, needs to write to video device, and read alsa_home_t alsa setsup pulseaudio
- locate tried to read a symbolic link, will dontaudit
- New labels for telepathy-sunshine content in homedir
- Google is storing other binaries under /opt/google/talkplugin
- bluetooth/kernel is creating unlabeled_t socket that I will allow it to use until kernel fixes bug
- Add boolean for unconfined_t transition to mozilla_plugin_t and telepathy domains, turned off in F14 on in F15
- modemmanger and bluetooth send dbus messages to devicekit_power
- Samba needs to getquota on filesystems labeld samba_share_t

* Wed Sep 29 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-8
- Dontaudit attempts by xdm_t to write to bin_t for kdm
- Allow initrc_t to manage system_conf_t

* Mon Sep 27 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-7
- Fixes to allow mozilla_plugin_t to create nsplugin_home_t directory.
- Allow mozilla_plugin_t to create tcp/udp/netlink_route sockets
- Allow confined users to read xdm_etc_t files
- Allow xdm_t to transition to xauth_t for lxdm program

* Sun Sep 26 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-6
- Rearrange firewallgui policy to be more easily updated to upstream, dontaudit search of /home
- Allow clamd to send signals to itself
- Allow mozilla_plugin_t to read user home content.  And unlink pulseaudio shm.
- Allow haze to connect to yahoo chat and messenger port tcp:5050.
Bz #637339
- Allow guest to run ps command on its processes by allowing it to read /proc
- Allow firewallgui to sys_rawio which seems to be required to setup masqerading
- Allow all domains to search through default_t directories, in order to find differnet labels.  For example people serring up /foo/bar to be share via samba.
- Add label for /var/log/slim.log

* Fri Sep 24 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-5
- Pull in cleanups from dgrift
- Allow mozilla_plugin_t to execute mozilla_home_t
- Allow rpc.quota to do quotamod

* Thu Sep 23 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-4
- Cleanup policy via dgrift
- Allow dovecot_deliver to append to inherited log files
- Lots of fixes for consolehelper

* Wed Sep 22 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-3
- Fix up Xguest policy

* Thu Sep 16 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-2
- Add vnstat policy
- allow libvirt to send audit messages
- Allow chrome-sandbox to search nfs_t

* Thu Sep 16 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-1
- Update to upstream

* Wed Sep 15 2010 Dan Walsh <dwalsh@redhat.com> 3.9.4-3
- Add the ability to send audit messages to confined admin policies
- Remove permissive domain from cmirrord and dontaudit sys_tty_config
- Split out unconfined_domain() calls from other unconfined_ calls so we can d
- virt needs to be able to read processes to clearance for MLS

* Tue Sep 14 2010 Dan Walsh <dwalsh@redhat.com> 3.9.4-2
- Allow all domains that can use cgroups to search tmpfs_t directory
- Allow init to send audit messages

* Thu Sep 9 2010 Dan Walsh <dwalsh@redhat.com> 3.9.4-1
- Update to upstream

* Thu Sep 9 2010 Dan Walsh <dwalsh@redhat.com> 3.9.3-4
- Allow mdadm_t to create files and sock files in /dev/md/

* Thu Sep 9 2010 Dan Walsh <dwalsh@redhat.com> 3.9.3-3
- Add policy for ajaxterm

* Wed Sep 8 2010 Dan Walsh <dwalsh@redhat.com> 3.9.3-2
- Handle /var/db/sudo
- Allow pulseaudio to read alsa config
- Allow init to send initrc_t dbus messages

* Tue Sep 7 2010 Dan Walsh <dwalsh@redhat.com> 3.9.3-1
Allow iptables to read shorewall tmp files
Change chfn and passwd to use auth_use_pam so they can send dbus messages to fpr
intd
label vlc as an execmem_exec_t 
Lots of fixes for mozilla_plugin to run google vidio chat
Allow telepath_msn to execute ldconfig and its own tmp files
Fix labels on hugepages
Allow mdadm to read files on /dev
Remove permissive domains and change back to unconfined
Allow freshclam to execute shell and bin_t
Allow devicekit_power to transition to dhcpc
Add boolean to allow icecast to connect to any port

* Tue Aug 31 2010 Dan Walsh <dwalsh@redhat.com> 3.9.2-1
- Merge upstream fix of mmap_zero
- Allow mount to write files in debugfs_t
- Allow corosync to communicate with clvmd via tmpfs
- Allow certmaster to read usr_t files
- Allow dbus system services to search cgroup_t
- Define rlogind_t as a login pgm

* Tue Aug 31 2010 Dan Walsh <dwalsh@redhat.com> 3.9.1-3
- Allow mdadm_t to read/write hugetlbfs

* Tue Aug 31 2010 Dan Walsh <dwalsh@redhat.com> 3.9.1-2
- Dominic Grift Cleanup
- Miroslav Grepl policy for jabberd
- Various fixes for mount/livecd and prelink

* Mon Aug 30 2010 Dan Walsh <dwalsh@redhat.com> 3.9.1-1
- Merge with upstream

* Thu Aug 26 2010 Dan Walsh <dwalsh@redhat.com> 3.9.0-2
- More access needed for devicekit
- Add dbadm policy

* Thu Aug 26 2010 Dan Walsh <dwalsh@redhat.com> 3.9.0-1
- Merge with upstream

* Tue Aug 24 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-21
- Allow seunshare to fowner

* Tue Aug 24 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-20
- Allow cron to look at user_cron_spool links
- Lots of fixes for mozilla_plugin_t
- Add sysv file system
- Turn unconfined domains to permissive to find additional avcs

* Mon Aug 23 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-19
- Update policy for mozilla_plugin_t

* Mon Aug 23 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-18
- Allow clamscan to read proc_t
- Allow mount_t to write to debufs_t dir
- Dontaudit mount_t trying to write to security_t dir

* Thu Aug 19 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-17
- Allow clamscan_t execmem if clamd_use_jit set
- Add policy for firefox plugin-container

* Wed Aug 18 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-16
- Fix /root/.forward definition

* Tue Aug 17 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-15
- label dead.letter as mail_home_t

* Fri Aug 13 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-14
- Allow login programs to search /cgroups

* Thu Aug 12 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-13
- Fix cert handling

* Tue Aug 10 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-12
- Fix devicekit_power bug
- Allow policykit_auth_t more access.

* Thu Aug 5 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-11
- Fix nis calls to allow bind to ports 512-1024
- Fix smartmon

* Wed Aug 4 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-10
- Allow pcscd to read sysfs
- systemd fixes 
- Fix wine_mmap_zero_ignore boolean

* Tue Aug 3 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-9
- Apply Miroslav munin patch
- Turn back on allow_execmem and allow_execmod booleans

* Tue Jul 27 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-8
- Merge in fixes from dgrift repository

* Tue Jul 27 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-7
- Update boinc policy
- Fix sysstat policy to allow sys_admin
- Change failsafe_context to unconfined_r:unconfined_t:s0

* Mon Jul 26 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-6
- New paths for upstart

* Mon Jul 26 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-5
- New permissions for syslog
- New labels for /lib/upstart

* Fri Jul 23 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-4
- Add mojomojo policy

* Thu Jul 22 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-3
- Allow systemd to setsockcon on sockets to immitate other services

* Wed Jul 21 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-2
- Remove debugfs label

* Tue Jul 20 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-1
- Update to latest policy

* Wed Jul 14 2010 Dan Walsh <dwalsh@redhat.com> 3.8.7-3
- Fix eclipse labeling from IBMSupportAssasstant packageing

* Wed Jul 14 2010 Dan Walsh <dwalsh@redhat.com> 3.8.7-2
- Make boot with systemd in enforcing mode

* Wed Jul 14 2010 Dan Walsh <dwalsh@redhat.com> 3.8.7-1
- Update to upstream

* Mon Jul 12 2010 Dan Walsh <dwalsh@redhat.com> 3.8.6-3
- Add boolean to turn off port forwarding in sshd.

* Fri Jul 9 2010 Miroslav Grepl <mgrepl@redhat.com> 3.8.6-2
- Add support for ebtables
- Fixes for rhcs and corosync policy

* Tue Jun 22 2010 Dan Walsh <dwalsh@redhat.com> 3.8.6-1
-Update to upstream

* Mon Jun 21 2010 Dan Walsh <dwalsh@redhat.com> 3.8.5-1
-Update to upstream

* Thu Jun 17 2010 Dan Walsh <dwalsh@redhat.com> 3.8.4-1
-Update to upstream

* Wed Jun 16 2010 Dan Walsh <dwalsh@redhat.com> 3.8.3-4
- Add Zarafa policy

* Wed Jun 9 2010 Dan Walsh <dwalsh@redhat.com> 3.8.3-3
- Cleanup of aiccu policy
- initial mock policy

* Wed Jun 9 2010 Dan Walsh <dwalsh@redhat.com> 3.8.3-2
- Lots of random fixes

* Tue Jun 8 2010 Dan Walsh <dwalsh@redhat.com> 3.8.3-1
- Update to upstream

* Fri Jun 4 2010 Dan Walsh <dwalsh@redhat.com> 3.8.2-1
- Update to upstream
- Allow prelink script to signal itself
- Cobbler fixes

* Wed Jun 2 2010 Dan Walsh <dwalsh@redhat.com> 3.8.1-5
- Add xdm_var_run_t to xserver_stream_connect_xdm
- Add cmorrord and mpd policy from Miroslav Grepl

* Tue Jun 1 2010 Dan Walsh <dwalsh@redhat.com> 3.8.1-4
- Fix sshd creation of krb cc files for users to be user_tmp_t

* Thu May 27 2010 Dan Walsh <dwalsh@redhat.com> 3.8.1-3
- Fixes for accountsdialog
- Fixes for boinc

* Thu May 27 2010 Dan Walsh <dwalsh@redhat.com> 3.8.1-2
- Fix label on /var/lib/dokwiki
- Change permissive domains to enforcing
- Fix libvirt policy to allow it to run on mls

* Tue May 25 2010 Dan Walsh <dwalsh@redhat.com> 3.8.1-1
- Update to upstream

* Tue May 25 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-22
- Allow procmail to execute scripts in the users home dir that are labeled home_bin_t
- Fix /var/run/abrtd.lock label

* Mon May 24 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-21
- Allow login programs to read krb5_home_t
Resolves: 594833
- Add obsoletes for cachefilesfd-selinux package
Resolves: #575084

* Thu May 20 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-20
- Allow mount to r/w abrt fifo file
- Allow svirt_t to getattr on hugetlbfs
- Allow abrt to create a directory under /var/spool

* Wed May 19 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-19
- Add labels for /sys
- Allow sshd to getattr on shutdown
- Fixes for munin
- Allow sssd to use the kernel key ring
- Allow tor to send syslog messages
- Allow iptabels to read usr files
- allow policykit to read all domains state

* Thu May 13 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-17
- Fix path for /var/spool/abrt
- Allow nfs_t as an entrypoint for http_sys_script_t
- Add policy for piranha
- Lots of fixes for sosreport

* Wed May 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-16
- Allow xm_t to read network state and get and set capabilities
- Allow policykit to getattr all processes
- Allow denyhosts to connect to tcp port 9911
- Allow pyranha to use raw ip sockets and ptrace itself
- Allow unconfined_execmem_t and gconfsd mechanism to dbus
- Allow staff to kill ping process
- Add additional MLS rules

* Mon May 10 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-15
- Allow gdm to edit ~/.gconf dir
Resolves: #590677
- Allow dovecot to create directories in /var/lib/dovecot
Partially resolves 590224
- Allow avahi to dbus chat with NetworkManager
- Fix cobbler labels
- Dontaudit iceauth_t leaks
- fix /var/lib/lxdm file context
- Allow aiccu to use tun tap devices
- Dontaudit shutdown using xserver.log

* Fri May 7 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-14
- Fixes for sandbox_x_net_t  to match access for sandbox_web_t ++
- Add xdm_etc_t for /etc/gdm directory, allow accountsd to manage this directory
- Add dontaudit interface for bluetooth dbus
- Add chronyd_read_keys, append_keys for initrc_t
- Add log support for ksmtuned
Resolves: #586663

* Thu May 6 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-13
- Allow boinc to send mail

* Wed May 5 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-12
- Allow initrc_t to remove dhcpc_state_t
- Fix label on sa-update.cron
- Allow dhcpc to restart chrony initrc
- Don't allow sandbox to send signals to its parent processes
- Fix transition from unconfined_t -> unconfined_mount_t -> rpcd_t
Resolves: #589136

* Mon May 3 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-11
- Fix location of oddjob_mkhomedir
Resolves: #587385
- fix labeling on /root/.shosts and ~/.shosts
- Allow ipsec_mgmt_t to manage net_conf_t
Resolves: #586760

* Fri Apr 30 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-10
- Dontaudit sandbox trying to connect to netlink sockets
Resolves: #587609
- Add policy for piranha

* Thu Apr 29 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-9
- Fixups for xguest policy
- Fixes for running sandbox firefox

* Wed Apr 28 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-8
- Allow ksmtuned to use terminals
Resolves: #586663
- Allow lircd to write to generic usb devices

* Tue Apr 27 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-7
- Allow sandbox_xserver to connectto unconfined stream
Resolves: #585171

* Mon Apr 26 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-6
- Allow initrc_t to read slapd_db_t
Resolves: #585476
- Allow ipsec_mgmt to use unallocated devpts and to create /etc/resolv.conf
Resolves: #585963

* Thu Apr 22 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-5
- Allow rlogind_t to search /root for .rhosts
Resolves: #582760
- Fix path for cached_var_t
- Fix prelink paths /var/lib/prelink	
- Allow confined users to direct_dri
- Allow mls lvm/cryptosetup to work

* Wed Apr 21 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-4
- Allow virtd_t to manage firewall/iptables config
Resolves: #573585

* Tue Apr 20 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-3
- Fix label on /root/.rhosts
Resolves: #582760
- Add labels for Picasa
- Allow openvpn to read home certs
- Allow plymouthd_t to use tty_device_t
- Run ncftool as iptables_t
- Allow mount to unmount unlabeled_t
- Dontaudit hal leaks

* Wed Apr 14 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-2
- Allow livecd to transition to mount

* Tue Apr 13 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-1
- Update to upstream
- Allow abrt to delete sosreport
Resolves: #579998
- Allow snmp to setuid and gid
Resolves: #582155
- Allow smartd to use generic scsi devices
Resolves: #582145

* Tue Apr 13 2010 Dan Walsh <dwalsh@redhat.com> 3.7.18-3
- Allow ipsec_t to create /etc/resolv.conf with the correct label
- Fix reserved port destination
- Allow autofs to transition to showmount
- Stop crashing tuned

* Mon Apr 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.18-2
- Add telepathysofiasip policy

* Mon Apr 5 2010 Dan Walsh <dwalsh@redhat.com> 3.7.18-1
- Update to upstream
- Fix label for  /opt/google/chrome/chrome-sandbox
- Allow modemmanager to dbus with policykit

* Mon Apr 5 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-6
- Fix allow_httpd_mod_auth_pam to use 	auth_use_pam(httpd_t)
- Allow accountsd to read shadow file
- Allow apache to send audit messages when using pam
- Allow asterisk to bind and connect to sip tcp ports
- Fixes for dovecot 2.0
- Allow initrc_t to setattr on milter directories
- Add procmail_home_t for .procmailrc file

* Thu Apr 1 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-5
- Fixes for labels during install from livecd

* Thu Apr 1 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-4
- Fix /cgroup file context 
- Fix broken afs use of unlabled_t
- Allow getty to use the console for s390

* Wed Mar 31 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-3
- Fix cgroup handling adding policy for /cgroup
- Allow confined users to write to generic usb devices, if user_rw_noexattrfile boolean set

* Tue Mar 30 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-2
- Merge patches from dgrift

* Mon Mar 29 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-1
- Update upstream
- Allow abrt to write to the /proc under any process

* Fri Mar 26 2010 Dan Walsh <dwalsh@redhat.com> 3.7.16-2
  - Fix ~/.fontconfig label
- Add /root/.cert label
- Allow reading of the fixed_file_disk_t:lnk_file if you can read file
- Allow qemu_exec_t as an entrypoint to svirt_t

* Tue Mar 23 2010 Dan Walsh <dwalsh@redhat.com> 3.7.16-1
- Update to upstream
- Allow tmpreaper to delete sandbox sock files
- Allow chrome-sandbox_t to use /dev/zero, and dontaudit getattr file systems
- Fixes for gitosis
- No transition on livecd to passwd or chfn
- Fixes for denyhosts

* Tue Mar 23 2010 Dan Walsh <dwalsh@redhat.com> 3.7.15-4
- Add label for /var/lib/upower
- Allow logrotate to run sssd
- dontaudit readahead on tmpfs blk files
- Allow tmpreaper to setattr on sandbox files
- Allow confined users to execute dos files
- Allow sysadm_t to kill processes running within its clearance
- Add accountsd policy
- Fixes for corosync policy
- Fixes from crontab policy
- Allow svirt to manage svirt_image_t chr files
- Fixes for qdisk policy
- Fixes for sssd policy
- Fixes for newrole policy

* Thu Mar 18 2010 Dan Walsh <dwalsh@redhat.com> 3.7.15-3
- make libvirt work on an MLS platform

* Thu Mar 18 2010 Dan Walsh <dwalsh@redhat.com> 3.7.15-2
- Add qpidd policy

* Thu Mar 18 2010 Dan Walsh <dwalsh@redhat.com> 3.7.15-1
- Update to upstream

* Tue Mar 16 2010 Dan Walsh <dwalsh@redhat.com> 3.7.14-5
- Allow boinc to read kernel sysctl
- Fix snmp port definitions
- Allow apache to read anon_inodefs

* Sun Mar 14 2010 Dan Walsh <dwalsh@redhat.com> 3.7.14-4
- Allow shutdown dac_override

* Sat Mar 13 2010 Dan Walsh <dwalsh@redhat.com> 3.7.14-3
- Add device_t as a file system
- Fix sysfs association

* Fri Mar 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.14-2
- Dontaudit ipsec_mgmt sys_ptrace
- Allow at to mail its spool files
- Allow nsplugin to search in .pulse directory

* Fri Mar 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.14-1
- Update to upstream

* Fri Mar 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.13-4
- Allow users to dbus chat with xdm
- Allow users to r/w wireless_device_t
- Dontaudit reading of process states by ipsec_mgmt

* Thu Mar 11 2010 Dan Walsh <dwalsh@redhat.com> 3.7.13-3
- Fix openoffice from unconfined_t

* Wed Mar 10 2010 Dan Walsh <dwalsh@redhat.com> 3.7.13-2
- Add shutdown policy so consolekit can shutdown system

* Tue Mar 9 2010 Dan Walsh <dwalsh@redhat.com> 3.7.13-1
- Update to upstream

* Thu Mar 4 2010 Dan Walsh <dwalsh@redhat.com> 3.7.12-1
- Update to upstream

* Thu Mar 4 2010 Dan Walsh <dwalsh@redhat.com> 3.7.11-1
- Update to upstream - These are merges of my patches
- Remove 389 labeling conflicts
- Add MLS fixes found in RHEL6 testing
- Allow pulseaudio to run as a service
- Add label for mssql and allow apache to connect to this database port if boolean set
- Dontaudit searches of debugfs mount point
- Allow policykit_auth to send signals to itself
- Allow modcluster to call getpwnam
- Allow swat to signal winbind
- Allow usbmux to run as a system role
- Allow svirt to create and use devpts

* Mon Mar 1 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-5
- Add MLS fixes found in RHEL6 testing
- Allow domains to append to rpm_tmp_t
- Add cachefilesfd policy
- Dontaudit leaks when transitioning

* Wed Feb 24 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-4
- Change allow_execstack and allow_execmem booleans to on
- dontaudit acct using console
- Add label for fping
- Allow tmpreaper to delete sandbox_file_t
- Fix wine dontaudit mmap_zero
- Allow abrt to read var_t symlinks

* Tue Feb 23 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-3
- Additional policy for rgmanager

* Mon Feb 22 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-2
- Allow sshd to setattr on pseudo terms

* Mon Feb 22 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-1
- Update to upstream

* Thu Feb 18 2010 Dan Walsh <dwalsh@redhat.com> 3.7.9-4
- Allow policykit to send itself signals

* Wed Feb 17 2010 Dan Walsh <dwalsh@redhat.com> 3.7.9-3
- Fix duplicate cobbler definition

* Wed Feb 17 2010 Dan Walsh <dwalsh@redhat.com> 3.7.9-2
- Fix file context of /var/lib/avahi-autoipd

* Fri Feb 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.9-1
- Merge with upstream

* Thu Feb 11 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-11
- Allow sandbox to work with MLS 

* Tue Feb 9 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-9
- Make Chrome work with staff user

* Thu Feb 4 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-8
- Add icecast policy
- Cleanup  spec file

* Wed Feb 3 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-7
- Add mcelog policy

* Mon Feb 1 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-6
- Lots of fixes found in F12

* Thu Jan 28 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-5
- Fix rpm_dontaudit_leaks

* Wed Jan 27 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-4
- Add getsched to hald_t
- Add file context for Fedora/Redhat Directory Server

* Mon Jan 25 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-3
- Allow abrt_helper to getattr on all filesystems
- Add label for /opt/real/RealPlayer/plugins/oggfformat\.so     

* Thu Jan 21 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-2
- Add gstreamer_home_t for ~/.gstreamer

* Mon Jan 18 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-1
- Update to upstream

* Fri Jan 15 2010 Dan Walsh <dwalsh@redhat.com> 3.7.7-3
- Fix git

* Thu Jan 7 2010 Dan Walsh <dwalsh@redhat.com> 3.7.7-2
- Turn on puppet policy
- Update to dgrift git policy

* Thu Jan 7 2010 Dan Walsh <dwalsh@redhat.com> 3.7.7-1
- Move users file to selection by spec file.
- Allow vncserver to run as unconfined_u:unconfined_r:unconfined_t

* Thu Jan 7 2010 Dan Walsh <dwalsh@redhat.com> 3.7.6-1
- Update to upstream

* Wed Jan 6 2010 Dan Walsh <dwalsh@redhat.com> 3.7.5-8
- Remove most of the permissive domains from F12.

* Tue Jan 5 2010 Dan Walsh <dwalsh@redhat.com> 3.7.5-7
- Add cobbler policy from dgrift

* Mon Jan 4 2010 Dan Walsh <dwalsh@redhat.com> 3.7.5-6
- add usbmon device
- Add allow rulse for devicekit_disk

* Wed Dec 30 2009 Dan Walsh <dwalsh@redhat.com> 3.7.5-5
- Lots of fixes found in F12, fixes from Tom London

* Wed Dec 23 2009 Dan Walsh <dwalsh@redhat.com> 3.7.5-4
- Cleanups from dgrift

* Tue Dec 22 2009 Dan Walsh <dwalsh@redhat.com> 3.7.5-3
- Add back xserver_manage_home_fonts

* Mon Dec 21 2009 Dan Walsh <dwalsh@redhat.com> 3.7.5-2
- Dontaudit sandbox trying to read nscd and sssd

* Fri Dec 18 2009 Dan Walsh <dwalsh@redhat.com> 3.7.5-1
- Update to upstream

* Thu Dec 17 2009 Dan Walsh <dwalsh@redhat.com> 3.7.4-4
- Rename udisks-daemon back to devicekit_disk_t policy

* Wed Dec 16 2009 Dan Walsh <dwalsh@redhat.com> 3.7.4-3
- Fixes for abrt calls

* Fri Dec 11 2009 Dan Walsh <dwalsh@redhat.com> 3.7.4-2
- Add tgtd policy

* Fri Dec 4 2009 Dan Walsh <dwalsh@redhat.com> 3.7.4-1
- Update to upstream release

* Mon Nov 16 2009 Dan Walsh <dwalsh@redhat.com> 3.7.3-1
- Add asterisk policy back in
- Update to upstream release 2.20091117

* Mon Nov 16 2009 Dan Walsh <dwalsh@redhat.com> 3.7.1-1
- Update to upstream release 2.20091117

* Mon Nov 16 2009 Dan Walsh <dwalsh@redhat.com> 3.6.33-2
- Fixup nut policy

* Thu Nov 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.33-1
- Update to upstream

* Thu Oct 1 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-17
- Allow vpnc request the kernel to load modules

* Wed Sep 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-16
- Fix minimum policy installs
- Allow udev and rpcbind to request the kernel to load modules

* Wed Sep 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-15
- Add plymouth policy
- Allow local_login to sys_admin

* Tue Sep 29 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-13
- Allow cupsd_config to read user tmp
- Allow snmpd_t to signal itself
- Allow sysstat_t to makedir in sysstat_log_t

* Fri Sep 25 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-12
- Update rhcs policy

* Thu Sep 24 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-11
- Allow users to exec restorecond

* Tue Sep 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-10
- Allow sendmail to request kernel modules load

* Mon Sep 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-9
- Fix all kernel_request_load_module domains

* Mon Sep 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-8
- Fix all kernel_request_load_module domains

* Sun Sep 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-7
- Remove allow_exec* booleans for confined users.  Only available for unconfined_t

* Fri Sep 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-6
- More fixes for sandbox_web_t

* Fri Sep 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-5
- Allow sshd to create .ssh directory and content

* Fri Sep 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-4
- Fix request_module line to module_request

* Fri Sep 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-3
- Fix sandbox policy to allow it to run under firefox.  
- Dont audit leaks.

* Thu Sep 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-2
- Fixes for sandbox

* Wed Sep 16 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-1
- Update to upstream
- Dontaudit nsplugin search /root
- Dontaudit nsplugin sys_nice

* Tue Sep 15 2009 Dan Walsh <dwalsh@redhat.com> 3.6.31-5
- Fix label on /usr/bin/notepad, /usr/sbin/vboxadd-service
- Remove policycoreutils-python requirement except for minimum

* Mon Sep 14 2009 Dan Walsh <dwalsh@redhat.com> 3.6.31-4
- Fix devicekit_disk_t to getattr on all domains sockets and fifo_files
- Conflicts seedit (You can not use selinux-policy-targeted and seedit at the same time.)

* Thu Sep 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.31-3
- Add wordpress/wp-content/uploads label
- Fixes for sandbox when run from staff_t

* Thu Sep 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.31-2
- Update to upstream
- Fixes for devicekit_disk

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-6
- More fixes

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-5
- Lots of fixes for initrc and other unconfined domains

* Fri Sep 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-4
- Allow xserver to use  netlink_kobject_uevent_socket

* Thu Sep 3 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-3
- Fixes for sandbox 

* Mon Aug 31 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-2
- Dontaudit setroubleshootfix looking at /root directory

* Mon Aug 31 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-1
- Update to upsteam

* Mon Aug 31 2009 Dan Walsh <dwalsh@redhat.com> 3.6.29-2
- Allow gssd to send signals to users
- Fix duplicate label for apache content

* Fri Aug 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.29-1
- Update to upstream

* Fri Aug 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-9
- Remove polkit_auth on upgrades

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-8
- Add back in unconfined.pp and unconfineduser.pp
- Add Sandbox unshare

* Tue Aug 25 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-7
- Fixes for cdrecord, mdadm, and others

* Sat Aug 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-6
- Add capability setting to dhcpc and gpm

* Sat Aug 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-5
- Allow cronjobs to read exim_spool_t

* Fri Aug 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-4
- Add ABRT policy

* Thu Aug 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-3
- Fix system-config-services policy

* Wed Aug 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-2
- Allow libvirt to change user componant of virt_domain

* Tue Aug 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-1
- Allow cupsd_config_t to be started by dbus
- Add smoltclient policy

* Fri Aug 14 2009 Dan Walsh <dwalsh@redhat.com> 3.6.27-1
- Add policycoreutils-python to pre install

* Thu Aug 13 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-11
- Make all unconfined_domains permissive so we can see what AVC's happen 

* Mon Aug 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-10
- Add pt_chown policy

* Mon Aug 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-9
- Add kdump policy for Miroslav Grepl
- Turn off execstack boolean

* Fri Aug 7 2009 Bill Nottingham <notting@redhat.com> 3.6.26-8
- Turn on execstack on a temporary basis (#512845)

* Thu Aug 6 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-7
- Allow nsplugin to connecto the session bus
- Allow samba_net to write to coolkey data

* Wed Aug 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-6
- Allow devicekit_disk to list inotify

* Wed Aug 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-5
- Allow svirt images to create sock_file in svirt_var_run_t

* Tue Aug 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-4
- Allow exim to getattr on mountpoints
- Fixes for pulseaudio

* Fri Jul 31 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-3
- Allow svirt_t to stream_connect to virtd_t

* Fri Jul 31 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-2
- Allod hald_dccm_t to create sock_files in /tmp

* Thu Jul 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-1
- More fixes from upstream

* Tue Jul 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.25-1
- Fix polkit label
- Remove hidebrokensymptoms for nss_ldap fix
- Add modemmanager policy
- Lots of merges from upstream
- Begin removing textrel_shlib_t labels, from fixed libraries

* Tue Jul 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.24-1
- Update to upstream

* Mon Jul 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.23-2
- Allow certmaster to override dac permissions

* Thu Jul 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.23-1
- Update to upstream

* Tue Jul 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.22-3
- Fix context for VirtualBox

* Tue Jul 14 2009 Dan Walsh <dwalsh@redhat.com> 3.6.22-1
- Update to upstream

* Fri Jul 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.21-4
- Allow clamscan read amavis spool files

* Wed Jul 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.21-3
- Fixes for xguest

* Tue Jul  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.6.21-2
- fix multiple directory ownership of mandirs

* Wed Jul 1 2009 Dan Walsh <dwalsh@redhat.com> 3.6.21-1
- Update to upstream

* Tue Jun 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.20-2
- Add rules for rtkit-daemon

* Thu Jun 25 2009 Dan Walsh <dwalsh@redhat.com> 3.6.20-1
- Update to upstream
- Fix nlscd_stream_connect

* Thu Jun 25 2009 Dan Walsh <dwalsh@redhat.com> 3.6.19-5
- Add rtkit policy

* Wed Jun 24 2009 Dan Walsh <dwalsh@redhat.com> 3.6.19-4
- Allow rpcd_t to stream connect to rpcbind

* Tue Jun 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.19-3
- Allow kpropd to create tmp files

* Tue Jun 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.19-2
- Fix last duplicate /var/log/rpmpkgs

* Mon Jun 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.19-1
- Update to upstream
  * add sssd

* Sat Jun 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.18-1
- Update to upstream
  * cleanup

* Fri Jun 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.17-1
- Update to upstream
- Additional mail ports
- Add virt_use_usb boolean for svirt

* Thu Jun 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.16-4
- Fix mcs rules to include chr_file and blk_file

* Tue Jun 16 2009 Dan Walsh <dwalsh@redhat.com> 3.6.16-3
- Add label for udev-acl

* Mon Jun 15 2009 Dan Walsh <dwalsh@redhat.com> 3.6.16-2
- Additional rules for consolekit/udev, privoxy and various other fixes

* Fri Jun 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.16-1
- New version for upstream

* Thu Jun 11 2009 Dan Walsh <dwalsh@redhat.com> 3.6.14-3
- Allow NetworkManager to read inotifyfs

* Wed Jun 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.14-2
- Allow setroubleshoot to run mlocate

* Mon Jun 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.14-1
- Update to upstream 

* Tue Jun 2 2009 Dan Walsh <dwalsh@redhat.com> 3.6.13-3
- Add fish as a shell
- Allow fprintd to list usbfs_t
- Allow consolekit to search mountpoints
- Add proper labeling for shorewall

* Tue May 26 2009 Dan Walsh <dwalsh@redhat.com> 3.6.13-2
- New log file for vmware
- Allow xdm to setattr on user_tmp_t

* Thu May 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.13-1
- Upgrade to upstream

* Wed May 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-39
- Allow fprintd to access sys_ptrace
- Add sandbox policy

* Mon May 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-38
- Add varnishd policy

* Thu May 14 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-37
- Fixes for kpropd

* Tue May 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-36
- Allow brctl to r/w tun_tap_device_t

* Mon May 11 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-35
- Add /usr/share/selinux/packages

* Mon May 11 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-34
- Allow rpcd_t to send signals to kernel threads

* Fri May 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-33
- Fix upgrade for F10 to F11

* Thu May 7 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-31
- Add policy for /var/lib/fprint

* Tue May 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-30
-Remove duplicate line

* Tue May 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-29
- Allow svirt to manage pci and other sysfs device data

* Mon May 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-28
- Fix package selection handling

* Fri May 1 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-27
- Fix /sbin/ip6tables-save context
- Allod udev to transition to mount
- Fix loading of mls policy file

* Thu Apr 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-26
- Add shorewall policy

* Wed Apr 29 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-25
- Additional rules for fprintd and sssd

* Tue Apr 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-24
- Allow nsplugin to unix_read unix_write sem for unconfined_java

* Tue Apr 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-23
- Fix uml files to be owned by users

* Tue Apr 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-22
- Fix Upgrade path to install unconfineduser.pp when unocnfined package is 3.0.0 or less

* Mon Apr 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-21
- Allow confined users to manage virt_content_t, since this is home dir content
- Allow all domains to read rpm_script_tmp_t which is what shell creates on redirection

* Mon Apr 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-20
- Fix labeling on /var/lib/misc/prelink*
- Allow xserver to rw_shm_perms with all x_clients
- Allow prelink to execute files in the users home directory

* Fri Apr 24 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-19
- Allow initrc_t to delete dev_null
- Allow readahead to configure auditing
- Fix milter policy
- Add /var/lib/readahead

* Fri Apr 24 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-16
- Update to latest milter code from Paul Howarth

* Thu Apr 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-15
- Additional perms for readahead

* Thu Apr 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-14
- Allow pulseaudio to acquire_svc on session bus
- Fix readahead labeling

* Thu Apr 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-13
- Allow sysadm_t to run rpm directly
- libvirt needs fowner

* Wed Apr 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-12
- Allow sshd to read var_lib symlinks for freenx

* Tue Apr 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-11
- Allow nsplugin unix_read and write on users shm and sem
- Allow sysadm_t to execute su

* Tue Apr 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-10
- Dontaudit attempts to getattr user_tmpfs_t by lvm
- Allow nfs to share removable media

* Mon Apr 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-9
- Add ability to run postdrop from confined users

* Sat Apr 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-8
- Fixes for podsleuth

* Fri Apr 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-7
- Turn off nsplugin transition
- Remove Konsole leaked file descriptors for release

* Fri Apr 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-6
- Allow cupsd_t to create link files in print_spool_t
- Fix iscsi_stream_connect typo
- Fix labeling on /etc/acpi/actions
- Don't reinstall unconfine and unconfineuser on upgrade if they are not installed

* Tue Apr 14 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-5
- Allow audioentroy to read etc files

* Mon Apr 13 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-4
- Add fail2ban_var_lib_t
- Fixes for devicekit_power_t

* Thu Apr 9 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-3
- Separate out the ucnonfined user from the unconfined.pp package

* Wed Apr 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-2
- Make sure unconfined_java_t and unconfined_mono_t create user_tmpfs_t.

* Tue Apr 7 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-1
- Upgrade to latest upstream
- Allow devicekit_disk sys_rawio

* Mon Apr 6 2009 Dan Walsh <dwalsh@redhat.com> 3.6.11-1
- Dontaudit binds to ports < 1024 for named
- Upgrade to latest upstream

* Fri Apr 3 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-9
- Allow podsleuth to use tmpfs files

* Fri Apr 3 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-8
- Add customizable_types for svirt

* Fri Apr 3 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-7
- Allow setroubelshoot exec* privs to prevent crash from bad libraries
- add cpufreqselector

* Thu Apr 2 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-6
- Dontaudit listing of /root directory for cron system jobs

* Mon Mar 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-5
- Fix missing ld.so.cache label

* Fri Mar 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-4
- Add label for ~/.forward and /root/.forward

* Thu Mar 26 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-3
- Fixes for svirt

* Thu Mar 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-2
- Fixes to allow svirt read iso files in homedir

* Thu Mar 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-1
- Add xenner and wine fixes from mgrepl

* Wed Mar 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.9-4
- Allow mdadm to read/write mls override

* Tue Mar 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.9-3
- Change to svirt to only access svirt_image_t

* Thu Mar 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.9-2
- Fix libvirt policy

* Thu Mar 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.9-1
- Upgrade to latest upstream

* Tue Mar 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.8-4
- Fixes for iscsid and sssd
- More cleanups for upgrade from F10 to Rawhide.

* Mon Mar 9 2009 Dan Walsh <dwalsh@redhat.com> 3.6.8-3
- Add pulseaudio, sssd policy
- Allow networkmanager to exec udevadm

* Sat Mar 7 2009 Dan Walsh <dwalsh@redhat.com> 3.6.8-2
- Add pulseaudio context

* Thu Mar 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.8-1
- Upgrade to latest patches

* Wed Mar 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.7-2
- Fixes for libvirt

* Mon Mar 2 2009 Dan Walsh <dwalsh@redhat.com> 3.6.7-1
- Update to Latest upstream

* Sat Feb 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-9
- Fix setrans.conf to show SystemLow for s0

* Fri Feb 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-8
- Further confinement of qemu images via svirt

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-6
- Allow NetworkManager to manage /etc/NetworkManager/system-connections

* Wed Feb 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-5
- add virtual_image_context and virtual_domain_context files

* Tue Feb 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-4
- Allow rpcd_t to send signal to mount_t
- Allow libvirtd to run ranged

* Tue Feb 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-3
- Fix sysnet/net_conf_t

* Tue Feb 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-2
- Fix squidGuard labeling

* Wed Feb 11 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-1
- Re-add corenet_in_generic_if(unlabeled_t)

* Wed Feb 11 2009 Dan Walsh <dwalsh@redhat.com> 3.6.5-3

* Tue Feb 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.5-2
- Add git web policy

* Mon Feb 9 2009 Dan Walsh <dwalsh@redhat.com> 3.6.5-1
- Add setrans contains from upstream 

* Mon Feb 9 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-6
- Do transitions outside of the booleans

* Sun Feb 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-5
- Allow xdm to create user_tmp_t sockets for switch user to work

* Thu Feb 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-4
- Fix staff_t domain

* Thu Feb 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-3
- Grab remainder of network_peer_controls patch

* Wed Feb 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-2
- More fixes for devicekit

* Tue Feb 3 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-1
- Upgrade to latest upstream 

* Mon Feb 2 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-13
- Add boolean to disallow unconfined_t login

* Fri Jan 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-12
- Add back transition from xguest to mozilla

* Fri Jan 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-11
- Add virt_content_ro_t and labeling for isos directory

* Tue Jan 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-10
- Fixes for wicd daemon

* Mon Jan 26 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-9
- More mls/rpm fixes 

* Fri Jan 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-8
- Add policy to make dbus/nm-applet work

* Thu Jan 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-7
- Remove polgen-ifgen from post and add trigger to policycoreutils-python

* Wed Jan 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-6
- Add wm policy
- Make mls work in graphics mode

* Tue Jan 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-3
- Fixed for DeviceKit

* Mon Jan 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-2
- Add devicekit policy

* Mon Jan 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-1
- Update to upstream

* Thu Jan 15 2009 Dan Walsh <dwalsh@redhat.com> 3.6.2-5
- Define openoffice as an x_domain

* Mon Jan 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.2-4
- Fixes for reading xserver_tmp_t

* Thu Jan 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.2-3
- Allow cups_pdf_t write to nfs_t

* Tue Jan 6 2009 Dan Walsh <dwalsh@redhat.com> 3.6.2-2
- Remove audio_entropy policy

* Mon Jan 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.2-1
- Update to upstream

* Sun Jan 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.1-15
- Allow hal_acl_t to getattr/setattr fixed_disk

* Sat Dec 27 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-14
- Change userdom_read_all_users_state to include reading symbolic links in /proc

* Mon Dec 22 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-13
- Fix dbus reading /proc information

* Thu Dec 18 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-12
- Add missing alias for home directory content

* Wed Dec 17 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-11
- Fixes for IBM java location

* Thu Dec 11 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-10
- Allow unconfined_r unconfined_java_t

* Tue Dec 9 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-9
- Add cron_role back to user domains

* Mon Dec 8 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-8
- Fix sudo setting of user keys

* Thu Dec 4 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-7
- Allow iptables to talk to terminals
- Fixes for policy kit
- lots of fixes for booting. 

* Wed Dec 3 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-4
- Cleanup policy

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.6.1-2
- Rebuild for Python 2.6

* Fri Nov 7 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-19
- Fix labeling on /var/spool/rsyslog

* Thu Nov 6 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-18
- Allow postgresl to bind to udp nodes

* Wed Nov 5 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-17
- Allow lvm to dbus chat with hal
- Allow rlogind to read nfs_t 

* Wed Nov 5 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-16
- Fix cyphesis file context

* Tue Nov 4 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-15
- Allow hal/pm-utils to look at /var/run/video.rom
- Add ulogd policy

* Tue Nov 4 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-14
- Additional fixes for cyphesis
- Fix certmaster file context
- Add policy for system-config-samba
- Allow hal to read /var/run/video.rom

* Mon Nov 3 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-13
- Allow dhcpc to restart ypbind
- Fixup labeling in /var/run

* Thu Oct 30 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-12
- Add certmaster policy

* Wed Oct 29 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-11
- Fix confined users 
- Allow xguest to read/write xguest_dbusd_t

* Mon Oct 27 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-9
- Allow openoffice execstack/execmem privs

* Fri Oct 24 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-8
- Allow mozilla to run with unconfined_execmem_t

* Thu Oct 23 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-7
- Dontaudit domains trying to write to .xsession-errors

* Thu Oct 23 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-6
- Allow nsplugin to look at autofs_t directory

* Wed Oct 22 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-5
- Allow kerneloops to create tmp files

* Wed Oct 22 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-4
- More alias for fastcgi

* Tue Oct 21 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-3
- Remove mod_fcgid-selinux package

* Mon Oct 20 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-2
- Fix dovecot access

* Fri Oct 17 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-1
- Policy cleanup 

* Thu Oct 16 2008 Dan Walsh <dwalsh@redhat.com> 3.5.12-3
- Remove Multiple spec
- Add include
- Fix makefile to not call per_role_expansion

* Wed Oct 15 2008 Dan Walsh <dwalsh@redhat.com> 3.5.12-2
- Fix labeling of libGL

* Fri Oct 10 2008 Dan Walsh <dwalsh@redhat.com> 3.5.12-1
- Update to upstream

* Wed Oct 8 2008 Dan Walsh <dwalsh@redhat.com> 3.5.11-1
- Update to upstream policy

* Mon Oct 6 2008 Dan Walsh <dwalsh@redhat.com> 3.5.10-3
- Fixes for confined xwindows and xdm_t 

* Fri Oct 3 2008 Dan Walsh <dwalsh@redhat.com> 3.5.10-2
- Allow confined users and xdm to exec wm
- Allow nsplugin to talk to fifo files on nfs

* Fri Oct 3 2008 Dan Walsh <dwalsh@redhat.com> 3.5.10-1
- Allow NetworkManager to transition to avahi and iptables
- Allow domains to search other domains keys, coverup kernel bug

* Wed Oct 1 2008 Dan Walsh <dwalsh@redhat.com> 3.5.9-4
- Fix labeling for oracle 

* Wed Oct 1 2008 Dan Walsh <dwalsh@redhat.com> 3.5.9-3
- Allow nsplugin to comminicate with xdm_tmp_t sock_file

* Mon Sep 29 2008 Dan Walsh <dwalsh@redhat.com> 3.5.9-2
- Change all user tmpfs_t files to be labeled user_tmpfs_t
- Allow radiusd to create sock_files

* Wed Sep 24 2008 Dan Walsh <dwalsh@redhat.com> 3.5.9-1
- Upgrade to upstream

* Tue Sep 23 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-7
- Allow confined users to login with dbus

* Mon Sep 22 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-6
- Fix transition to nsplugin

* Mon Sep 22 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-5
- Add file context for /dev/mspblk.*

* Sun Sep 21 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-4
- Fix transition to nsplugin
'

* Thu Sep 18 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-3
- Fix labeling on new pm*log
- Allow ssh to bind to all nodes

* Thu Sep 11 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-1
- Merge upstream changes
- Add Xavier Toth patches

* Wed Sep 10 2008 Dan Walsh <dwalsh@redhat.com> 3.5.7-2
- Add qemu_cache_t for /var/cache/libvirt

* Fri Sep 5 2008 Dan Walsh <dwalsh@redhat.com> 3.5.7-1
- Remove gamin policy

* Thu Sep 4 2008 Dan Walsh <dwalsh@redhat.com> 3.5.6-2
- Add tinyxs-max file system support

* Wed Sep 3 2008 Dan Walsh <dwalsh@redhat.com> 3.5.6-1
- Update to upstream
-       New handling of init scripts

* Fri Aug 29 2008 Dan Walsh <dwalsh@redhat.com> 3.5.5-4
- Allow pcsd to dbus
- Add memcache policy

* Fri Aug 29 2008 Dan Walsh <dwalsh@redhat.com> 3.5.5-3
- Allow audit dispatcher to kill his children

* Tue Aug 26 2008 Dan Walsh <dwalsh@redhat.com> 3.5.5-2
- Update to upstream
- Fix crontab use by unconfined user

* Tue Aug 12 2008 Dan Walsh <dwalsh@redhat.com> 3.5.4-2
- Allow ifconfig_t to read dhcpc_state_t

* Mon Aug 11 2008 Dan Walsh <dwalsh@redhat.com> 3.5.4-1
- Update to upstream

* Thu Aug 7 2008 Dan Walsh <dwalsh@redhat.com> 3.5.3-1
- Update to upstream 

* Sat Aug 2 2008 Dan Walsh <dwalsh@redhat.com> 3.5.2-2
- Allow system-config-selinux to work with policykit

* Fri Jul 25 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-5
- Fix novel labeling

* Fri Jul 25 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-4
- Consolodate pyzor,spamassassin, razor into one security domain
- Fix xdm requiring additional perms.

* Fri Jul 25 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-3
- Fixes for logrotate, alsa

* Thu Jul 24 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-2
- Eliminate vbetool duplicate entry

* Wed Jul 16 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-1
- Fix xguest -> xguest_mozilla_t -> xguest_openiffice_t
- Change dhclient to be able to red networkmanager_var_run

* Tue Jul 15 2008 Dan Walsh <dwalsh@redhat.com> 3.5.0-1
- Update to latest refpolicy
- Fix libsemanage initial install bug

* Wed Jul 9 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-14
- Add inotify support to nscd

* Tue Jul 8 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-13
- Allow unconfined_t to setfcap

* Mon Jul 7 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-12
- Allow amanda to read tape
- Allow prewikka cgi to use syslog, allow audisp_t to signal cgi
- Add support for netware file systems

* Thu Jul 3 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-11
- Allow ypbind apps to net_bind_service

* Wed Jul 2 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-10
- Allow all system domains and application domains to append to any log file

* Sun Jun 29 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-9
- Allow gdm to read rpm database
- Allow nsplugin to read mplayer config files

* Thu Jun 26 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-8
- Allow vpnc to run ifconfig

* Tue Jun 24 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-7
- Allow confined users to use postgres
- Allow system_mail_t to exec other mail clients
- Label mogrel_rails as an apache server

* Mon Jun 23 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-6
- Apply unconfined_execmem_exec_t to haskell programs

* Sun Jun 22 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-5
- Fix prelude file context

* Fri Jun 13 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-4
- allow hplip to talk dbus
- Fix context on ~/.local dir

* Thu Jun 12 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-3
- Prevent applications from reading x_device

* Thu Jun 12 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-2
- Add /var/lib/selinux context

* Wed Jun 11 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-1
- Update to upstream 

* Wed Jun 4 2008 Dan Walsh <dwalsh@redhat.com> 3.4.1-5
- Add livecd policy

* Wed Jun 4 2008 Dan Walsh <dwalsh@redhat.com> 3.4.1-3
- Dontaudit search of admin_home for init_system_domain
- Rewrite of xace interfaces
- Lots of new fs_list_inotify
- Allow livecd to transition to setfiles_mac

* Fri May 9 2008 Dan Walsh <dwalsh@redhat.com> 3.4.1-2
- Begin XAce integration

* Fri May 9 2008 Dan Walsh <dwalsh@redhat.com> 3.4.1-1
- Merge Upstream

* Wed May 7 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-48
- Allow amanada to create data files

* Wed May 7 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-47
- Fix initial install, semanage setup

* Tue May 6 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-46
- Allow system_r for httpd_unconfined_script_t

* Wed Apr 30 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-45
- Remove dmesg boolean
- Allow user domains to read/write game data

* Mon Apr 28 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-44
- Change unconfined_t to transition to unconfined_mono_t when running mono
- Change XXX_mono_t to transition to XXX_t when executing bin_t files, so gnome-do will work

* Mon Apr 28 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-43
- Remove old booleans from targeted-booleans.conf file

* Fri Apr 25 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-42
- Add boolean to mmap_zero
- allow tor setgid
- Allow gnomeclock to set clock

* Thu Apr 24 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-41
- Don't run crontab from unconfined_t

* Wed Apr 23 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-39
- Change etc files to config files to allow users to read them

* Fri Apr 18 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-37
- Lots of fixes for confined domains on NFS_t homedir

* Mon Apr 14 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-36
- dontaudit mrtg reading /proc
- Allow iscsi to signal itself
- Allow gnomeclock sys_ptrace

* Thu Apr 10 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-33
- Allow dhcpd to read kernel network state

* Thu Apr 10 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-32
- Label /var/run/gdm correctly
- Fix unconfined_u user creation

* Tue Apr 8 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-31
- Allow transition from initrc_t to getty_t

* Tue Apr 8 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-30
- Allow passwd to communicate with user sockets to change gnome-keyring

* Sat Apr 5 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-29
- Fix initial install

* Fri Apr 4 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-28
- Allow radvd to use fifo_file
- dontaudit setfiles reading links
- allow semanage sys_resource
- add allow_httpd_mod_auth_ntlm_winbind boolean
- Allow privhome apps including dovecot read on nfs and cifs home 
dirs if the boolean is set

* Tue Apr 1 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-27
- Allow nsplugin to read /etc/mozpluggerrc, user_fonts
- Allow syslog to manage innd logs.
- Allow procmail to ioctl spamd_exec_t

* Sat Mar 29 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-26
- Allow initrc_t to dbus chat with consolekit.

* Thu Mar 27 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-25
- Additional access for nsplugin
- Allow xdm setcap/getcap until pulseaudio is fixed

* Tue Mar 25 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-24
- Allow mount to mkdir on tmpfs
- Allow ifconfig to search debugfs

* Fri Mar 21 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-23
- Fix file context for MATLAB
- Fixes for xace

* Tue Mar 18 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-22
- Allow stunnel to transition to inetd children domains
- Make unconfined_dbusd_t an unconfined domain 

* Mon Mar 17 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-21
- Fixes for qemu/virtd

* Fri Mar 14 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-20
- Fix bug in mozilla policy to allow xguest transition
- This will fix the 
libsemanage.dbase_llist_query: could not find record value
libsemanage.dbase_llist_query: could not query record value (No such file or
directory)
 bug in xguest

* Fri Mar 14 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-19
- Allow nsplugin to run acroread

* Thu Mar 13 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-18
- Add cups_pdf policy
- Add openoffice policy to run in xguest

* Thu Mar 13 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-17
- prewika needs to contact mysql
- Allow syslog to read system_map files

* Wed Mar 12 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-16
- Change init_t to an unconfined_domain

* Tue Mar 11 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-15
- Allow init to transition to initrc_t on shell exec.
- Fix init to be able to sendto init_t.
- Allow syslog to connect to mysql
- Allow lvm to manage its own fifo_files
- Allow bugzilla to use ldap
- More mls fixes 

* Tue Mar 11 2008 Bill Nottingham <notting@redhat.com> 3.3.1-14
- fixes for init policy (#436988)
- fix build

* Mon Mar 10 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-13
- Additional changes for MLS policy

* Thu Mar 6 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-12
- Fix initrc_context generation for MLS

* Mon Mar 3 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-11
- Fixes for libvirt

* Mon Mar 3 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-10
- Allow bitlebee to read locale_t

* Fri Feb 29 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-9
- More xselinux rules

* Thu Feb 28 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-8
- Change httpd_$1_script_r*_t to httpd_$1_content_r*_t

* Wed Feb 27 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-6
- Prepare policy for beta release
- Change some of the system domains back to unconfined
- Turn on some of the booleans

* Tue Feb 26 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-5
- Allow nsplugin_config execstack/execmem
- Allow nsplugin_t to read alsa config
- Change apache to use user content 

* Tue Feb 26 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-4
- Add cyphesis policy

* Tue Feb 26 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-2
- Fix Makefile.devel to build mls modules
- Fix qemu to be more specific on labeling

* Tue Feb 26 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-1
- Update to upstream fixes

* Fri Feb 22 2008 Dan Walsh <dwalsh@redhat.com> 3.3.0-2
- Allow staff to mounton user_home_t

* Fri Feb 22 2008 Dan Walsh <dwalsh@redhat.com> 3.3.0-1
- Add xace support

* Thu Feb 21 2008 Dan Walsh <dwalsh@redhat.com> 3.2.9-2
- Add fusectl file system

* Wed Feb 20 2008 Dan Walsh <dwalsh@redhat.com> 3.2.9-1
- Fixes from yum-cron
- Update to latest upstream

* Tue Feb 19 2008 Dan Walsh <dwalsh@redhat.com> 3.2.8-2
- Fix userdom_list_user_files

* Fri Feb 15 2008 Dan Walsh <dwalsh@redhat.com> 3.2.8-1
- Merge with upstream

* Thu Feb 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-6
- Allow udev to send audit messages

* Thu Feb 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-5
- Add additional login users interfaces
  -     userdom_admin_login_user_template(staff)

* Thu Feb 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-3
- More fixes for polkit

* Thu Feb 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-2
- Eliminate transition from unconfined_t to qemu by default
- Fixes for gpg

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-1
- Update to upstream

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-7
- Fixes for staff_t

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-6
- Add policy for kerneloops
- Add policy for gnomeclock

* Mon Feb 4 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-5
- Fixes for libvirt

* Sun Feb 3 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-4
- Fixes for nsplugin

* Sat Feb 2 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-3
- More fixes for qemu

* Sat Feb 2 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-2
- Additional ports for vnc and allow qemu and libvirt to search all directories

* Fri Feb 1 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-1
- Update to upstream
- Add libvirt policy
- add qemu policy

* Fri Feb 1 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-25
- Allow fail2ban to create a socket in /var/run

* Wed Jan 30 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-24
- Allow allow_httpd_mod_auth_pam to work

* Wed Jan 30 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-22
- Add audisp policy and prelude

* Mon Jan 28 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-21
- Allow all user roles to executae samba net command

* Fri Jan 25 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-20
- Allow usertypes to read/write noxattr file systems

* Thu Jan 24 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-19
- Fix nsplugin to allow flashplugin to work in enforcing mode

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-18
- Allow pam_selinux_permit to kill all processes

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-17
- Allow ptrace or user processes by users of same type
- Add boolean for transition to nsplugin

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-16
- Allow nsplugin sys_nice, getsched, setsched

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-15
- Allow login programs to talk dbus to oddjob

* Thu Jan 17 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-14
- Add procmail_log support
- Lots of fixes for munin

* Tue Jan 15 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-13
- Allow setroubleshoot to read policy config and send audit messages

* Mon Jan 14 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-12
- Allow users to execute all files in homedir, if boolean set
- Allow mount to read samba config

* Sun Jan 13 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-11
- Fixes for xguest to run java plugin

* Mon Jan 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-10
- dontaudit pam_t and dbusd writing to user_home_t

* Mon Jan 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-9
- Update gpg to allow reading of inotify

* Wed Jan 2 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-8
- Change user and staff roles to work correctly with varied perms

* Mon Dec 31 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-7
- Fix munin log,
- Eliminate duplicate mozilla file context
- fix wpa_supplicant spec

* Mon Dec 24 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-6
- Fix role transition from unconfined_r to system_r when running rpm
- Allow unconfined_domains to communicate with user dbus instances

* Sat Dec 22 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-5
- Fixes for xguest

* Thu Dec 20 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-4
- Let all uncofined domains communicate with dbus unconfined

* Thu Dec 20 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-3
- Run rpm in system_r

* Wed Dec 19 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-2
- Zero out customizable types

* Wed Dec 19 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-1
- Fix definiton of admin_home_t

* Wed Dec 19 2007 Dan Walsh <dwalsh@redhat.com> 3.2.4-5
- Fix munin file context

* Tue Dec 18 2007 Dan Walsh <dwalsh@redhat.com> 3.2.4-4
- Allow cron to run unconfined apps

* Mon Dec 17 2007 Dan Walsh <dwalsh@redhat.com> 3.2.4-3
- Modify default login to unconfined_u

* Thu Dec 13 2007 Dan Walsh <dwalsh@redhat.com> 3.2.4-1
- Dontaudit dbus user client search of /root

* Wed Dec 12 2007 Dan Walsh <dwalsh@redhat.com> 3.2.4-1
- Update to upstream

* Tue Dec 11 2007 Dan Walsh <dwalsh@redhat.com> 3.2.3-2
- Fixes for polkit
- Allow xserver to ptrace

* Tue Dec 11 2007 Dan Walsh <dwalsh@redhat.com> 3.2.3-1
- Add polkit policy
- Symplify userdom context, remove automatic per_role changes

* Tue Dec 4 2007 Dan Walsh <dwalsh@redhat.com> 3.2.2-1
- Update to upstream
- Allow httpd_sys_script_t to search users homedirs

* Mon Dec 3 2007 Dan Walsh <dwalsh@redhat.com> 3.2.1-3
- Allow rpm_script to transition to unconfined_execmem_t

* Fri Nov 30 2007 Dan Walsh <dwalsh@redhat.com> 3.2.1-1
- Remove user based home directory separation

* Wed Nov 28 2007 Dan Walsh <dwalsh@redhat.com> 3.1.2-2
- Remove user specific crond_t

* Mon Nov 19 2007 Dan Walsh <dwalhh@redhat.com> 3.1.2-1
- Merge with upstream
- Allow xsever to read hwdata_t
- Allow login programs to setkeycreate

* Sat Nov 10 2007 Dan Walsh <dwalsh@redhat.com> 3.1.1-1
- Update to upstream

* Mon Oct 22 2007 Dan Walsh <dwalsh@redhat.com> 3.1.0-1
- Update to upstream

* Mon Oct 22 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-30
- Allow XServer to read /proc/self/cmdline
- Fix unconfined cron jobs
- Allow fetchmail to transition to procmail
- Fixes for hald_mac
- Allow system_mail to transition to exim
- Allow tftpd to upload files
- Allow xdm to manage unconfined_tmp
- Allow udef to read alsa config
- Fix xguest to be able to connect to sound port

* Fri Oct 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-28
- Fixes for hald_mac 
- Treat unconfined_home_dir_t as a home dir
- dontaudit rhgb writes to fonts and root

* Fri Oct 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-27
- Fix dnsmasq
- Allow rshd full login privs

* Thu Oct 18 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-26
- Allow rshd to connect to ports > 1023

* Thu Oct 18 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-25
- Fix vpn to bind to port 4500
- Allow ssh to create shm
- Add Kismet policy

* Tue Oct 16 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-24
- Allow rpm to chat with networkmanager

* Mon Oct 15 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-23
- Fixes for ipsec and exim mail
- Change default to unconfined user

* Fri Oct 12 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-22
- Pass the UNK_PERMS param to makefile
- Fix gdm location

* Wed Oct 10 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-21
- Make alsa work

* Tue Oct 9 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-20
- Fixes for consolekit and startx sessions

* Mon Oct 8 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-19
- Dontaudit consoletype talking to unconfined_t

* Thu Oct 4 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-18
- Remove homedir_template

* Tue Oct 2 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-17
- Check asound.state

* Mon Oct 1 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-16
- Fix exim policy

* Thu Sep 27 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-15
- Allow tmpreadper to read man_t
- Allow racoon to bind to all nodes
- Fixes for finger print reader

* Tue Sep 25 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-14
- Allow xdm to talk to input device (fingerprint reader)
- Allow octave to run as java

* Tue Sep 25 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-13
- Allow login programs to set ioctl on /proc

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-12
- Allow nsswitch apps to read samba_var_t

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-11
- Fix maxima

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-10
- Eliminate rpm_t:fifo_file avcs
- Fix dbus path for helper app

* Sat Sep 22 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-9
- Fix service start stop terminal avc's

* Fri Sep 21 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-8
- Allow also to search var_lib
- New context for dbus launcher 

* Fri Sep 21 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-7
- Allow cupsd_config_t to read/write usb_device_t
- Support for finger print reader,
- Many fixes for clvmd
- dbus starting networkmanager

* Thu Sep 20 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-5
- Fix java and mono to run in xguest account

* Wed Sep 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-4
- Fix to add xguest account when inititial install
- Allow mono, java, wine to run in userdomains

* Wed Sep 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-3
- Allow xserver to search devpts_t
- Dontaudit ldconfig output to homedir

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-2
- Remove hplip_etc_t change back to etc_t.

* Mon Sep 17 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-1
- Allow cron to search nfs and samba homedirs

* Tue Sep 11 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-10
- Allow NetworkManager to dbus chat with yum-updated

* Tue Sep 11 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-9
- Allow xfs to bind to port 7100

* Mon Sep 10 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-8
- Allow newalias/sendmail dac_override
- Allow bind to bind to all udp ports

* Fri Sep 7 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-7
- Turn off direct transition

* Fri Sep 7 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-6
- Allow wine to run in system role

* Thu Sep 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-5
- Fix java labeling 

* Thu Sep 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-4
- Define user_home_type as home_type

* Tue Aug 28 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-3
- Allow sendmail to create etc_aliases_t

* Tue Aug 28 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-2
- Allow login programs to read symlinks on homedirs

* Mon Aug 27 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-1
- Update an readd modules

* Fri Aug 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.6-3
- Cleanup  spec file

* Fri Aug 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.6-2
- Allow xserver to be started by unconfined process and talk to tty

* Wed Aug 22 2007 Dan Walsh <dwalsh@redhat.com> 3.0.6-1
- Upgrade to upstream to grab postgressql changes

* Tue Aug 21 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-11
- Add setransd for mls policy

* Mon Aug 20 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-10
- Add ldconfig_cache_t

* Sat Aug 18 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-9
- Allow sshd to write to proc_t for afs login

* Sat Aug 18 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-8
- Allow xserver access to urand

* Tue Aug 14 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-7
- allow dovecot to search mountpoints

* Sat Aug 11 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-6
- Fix Makefile for building policy modules

* Fri Aug 10 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-5
- Fix dhcpc startup of service 

* Fri Aug 10 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-4
- Fix dbus chat to not happen for xguest and guest users

* Mon Aug 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-3
- Fix nagios cgi
- allow squid to communicate with winbind

* Mon Aug 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-2
- Fixes for ldconfig

* Thu Aug 2 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-1
- Update from upstream

* Wed Aug 1 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-6
- Add nasd support

* Wed Aug 1 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-5
- Fix new usb devices and dmfm

* Mon Jul 30 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-4
- Eliminate mount_ntfs_t policy, merge into mount_t

* Mon Jul 30 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-3
- Allow xserver to write to ramfs mounted by rhgb

* Tue Jul 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-2
- Add context for dbus machine id

* Tue Jul 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-1
- Update with latest changes from upstream

* Tue Jul 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-6
- Fix prelink to handle execmod

* Mon Jul 23 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-5
- Add ntpd_key_t to handle secret data

* Fri Jul 20 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-4
- Add anon_inodefs
- Allow unpriv user exec pam_exec_t
- Fix trigger

* Fri Jul 20 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-3
- Allow cups to use generic usb
- fix inetd to be able to run random apps (git)

* Thu Jul 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-2
- Add proper contexts for rsyslogd

* Thu Jul 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-1
- Fixes for xguest policy

* Tue Jul 17 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-9
- Allow execution of gconf

* Sat Jul 14 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-8
- Fix moilscanner update problem

* Thu Jul 12 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-7
- Begin adding policy to separate setsebool from semanage
- Fix xserver.if definition to not break sepolgen.if

* Wed Jul 11 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-5
- Add new devices

* Tue Jul 10 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-4
- Add brctl policy

* Fri Jul 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-3
- Fix root login to include system_r

* Fri Jul 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-2
- Allow prelink to read kernel sysctls

* Mon Jul 2 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-5
- Default to user_u:system_r:unconfined_t 

* Sun Jul 1 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-4
- fix squid
- Fix rpm running as uid

* Tue Jun 26 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-3
- Fix syslog declaration

* Tue Jun 26 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-2
- Allow avahi to access inotify
- Remove a lot of bogus security_t:filesystem avcs

* Fri May 25 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-1
- Remove ifdef strict policy from upstream

* Fri May 18 2007 Dan Walsh <dwalsh@redhat.com> 2.6.5-3
- Remove ifdef strict to allow user_u to login 

* Fri May 18 2007 Dan Walsh <dwalsh@redhat.com> 2.6.5-2
- Fix for amands
- Allow semanage to read pp files
- Allow rhgb to read xdm_xserver_tmp

* Fri May 18 2007 Dan Walsh <dwalsh@redhat.com> 2.6.4-7
- Allow kerberos servers to use ldap for backing store

* Thu May 17 2007 Dan Walsh <dwalsh@redhat.com> 2.6.4-6
- allow alsactl to read kernel state

* Wed May 16 2007 Dan Walsh <dwalsh@redhat.com> 2.6.4-5
- More fixes for alsactl
- Transition from hal and modutils
- Fixes for suspend resume.  
     - insmod domtrans to alsactl
     - insmod writes to hal log

* Wed May 16 2007 Dan Walsh <dwalsh@redhat.com> 2.6.4-2
- Allow unconfined_t to transition to NetworkManager_t
- Fix netlabel policy

* Mon May 14 2007 Dan Walsh <dwalsh@redhat.com> 2.6.4-1
- Update to latest from upstream

* Fri May 4 2007 Dan Walsh <dwalsh@redhat.com> 2.6.3-1
- Update to latest from upstream

* Mon Apr 30 2007 Dan Walsh <dwalsh@redhat.com> 2.6.2-1
- Update to latest from upstream

* Fri Apr 27 2007 Dan Walsh <dwalsh@redhat.com> 2.6.1-4
- Allow pcscd_t to send itself signals

* Wed Apr 25 2007 Dan Walsh <dwalsh@redhat.com> 2.6.1-2
- Fixes for unix_update
- Fix logwatch to be able to search all dirs

* Mon Apr 23 2007 Dan Walsh <dwalsh@redhat.com> 2.6.1-1
- Upstream bumped the version

* Thu Apr 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-12
- Allow consolekit to syslog
- Allow ntfs to work with hal

* Thu Apr 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-11
- Allow iptables to read etc_runtime_t

* Thu Apr 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-10
- MLS Fixes

* Wed Apr 18 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-8
- Fix path of /etc/lvm/cache directory
- Fixes for alsactl and pppd_t
- Fixes for consolekit

* Tue Apr 17 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-5
- Allow insmod_t to mount kvmfs_t filesystems

* Tue Apr 17 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-4
- Rwho policy
- Fixes for consolekit

* Fri Apr 13 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-3
- fixes for fusefs

* Thu Apr 12 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-2
- Fix samba_net to allow it to view samba_var_t

* Tue Apr 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-1
- Update to upstream

* Tue Apr 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-8
- Fix Sonypic backlight
- Allow snmp to look at squid_conf_t

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-7
- Fixes for pyzor, cyrus, consoletype on everything installs

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-6
- Fix hald_acl_t to be able to getattr/setattr on usb devices
- Dontaudit write to unconfined_pipes for load_policy

* Thu Apr 5 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-5
- Allow bluetooth to read inotifyfs

* Wed Apr 4 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-4
- Fixes for samba domain controller.
- Allow ConsoleKit to look at ttys

* Tue Apr 3 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-3
- Fix interface call

* Tue Apr 3 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-2
- Allow syslog-ng to read /var
- Allow locate to getattr on all filesystems
- nscd needs setcap

* Mon Mar 26 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-1
- Update to upstream

* Fri Mar 23 2007 Dan Walsh <dwalsh@redhat.com> 2.5.10-2
- Allow samba to run groupadd

* Thu Mar 22 2007 Dan Walsh <dwalsh@redhat.com> 2.5.10-1
- Update to upstream

* Thu Mar 22 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-6
- Allow mdadm to access generic scsi devices

* Wed Mar 21 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-5
- Fix labeling on udev.tbl dirs

* Tue Mar 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-4
- Fixes for logwatch

* Tue Mar 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-3
- Add fusermount and mount_ntfs policy

* Tue Mar 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-2
- Update to upstream
- Allow saslauthd to use kerberos keytabs

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-8
- Fixes for samba_var_t

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-7
- Allow networkmanager to setpgid
- Fixes for hal_acl_t

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-6
- Remove disable_trans booleans
- hald_acl_t needs to talk to nscd

* Thu Mar 15 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-5
- Fix prelink to be able to manage usr dirs.

* Tue Mar 13 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-4
- Allow insmod to launch init scripts

* Tue Mar 13 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-3
- Remove setsebool policy

* Mon Mar 12 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-2
- Fix handling of unlabled_t packets

* Thu Mar 8 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-1
- More of my patches from upstream

* Thu Mar 1 2007 Dan Walsh <dwalsh@redhat.com> 2.5.7-1
- Update to latest from upstream
- Add fail2ban policy

* Wed Feb 28 2007 Dan Walsh <dwalsh@redhat.com> 2.5.6-1
- Update to remove security_t:filesystem getattr problems

* Fri Feb 23 2007 Dan Walsh <dwalsh@redhat.com> 2.5.5-2
- Policy for consolekit

* Fri Feb 23 2007 Dan Walsh <dwalsh@redhat.com> 2.5.5-1
- Update to latest from upstream

* Wed Feb 21 2007 Dan Walsh <dwalsh@redhat.com> 2.5.4-2
- Revert Nemiver change
- Set sudo as a corecmd so prelink will work,  remove sudoedit mapping, since this will not work, it does not transition.
- Allow samba to execute useradd

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.4-1
- Upgrade to the latest from upstream

* Thu Feb 15 2007 Dan Walsh <dwalsh@redhat.com> 2.5.3-3
- Add sepolgen support
- Add bugzilla policy

* Wed Feb 14 2007 Dan Walsh <dwalsh@redhat.com> 2.5.3-2
- Fix file context for nemiver

* Sun Feb 11 2007 Dan Walsh <dwalsh@redhat.com> 2.5.3-1
- Remove include sym link

* Mon Feb 5 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-6
- Allow mozilla, evolution and thunderbird to read dev_random.
Resolves: #227002
- Allow spamd to connect to smtp port
Resolves: #227184
- Fixes to make ypxfr work
Resolves: #227237

* Sun Feb 4 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-5
- Fix ssh_agent to be marked as an executable
- Allow Hal to rw sound device 

* Thu Feb 1 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-4
- Fix spamassisin so crond can update spam files
- Fixes to allow kpasswd to work
- Fixes for bluetooth

* Fri Jan 26 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-3
- Remove some targeted diffs in file context file

* Thu Jan 25 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-2
- Fix squid cachemgr labeling

* Thu Jan 25 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-1
- Add ability to generate webadm_t policy
- Lots of new interfaces for httpd
- Allow sshd to login as unconfined_t

* Mon Jan 22 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-5
- Continue fixing, additional user domains

* Wed Jan 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-4
- Begin adding user confinement to targeted policy 

* Wed Jan 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-2
- Fixes for prelink, ktalkd, netlabel

* Mon Jan 8 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-1
- Allow prelink when run from rpm to create tmp files
Resolves: #221865
- Remove file_context for exportfs
Resolves: #221181
- Allow spamassassin to create ~/.spamassissin
Resolves: #203290
- Allow ssh access to the krb tickets
- Allow sshd to change passwd
- Stop newrole -l from working on non securetty
Resolves: #200110
- Fixes to run prelink in MLS machine
Resolves: #221233
- Allow spamassassin to read var_lib_t dir
Resolves: #219234

* Fri Dec 29 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-20
- fix mplayer to work under strict policy
- Allow iptables to use nscd
Resolves: #220794

* Thu Dec 28 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-19
- Add gconf policy and make it work with strict

* Sat Dec 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-18
- Many fixes for strict policy and by extension mls.

* Fri Dec 22 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-17
- Fix to allow ftp to bind to ports > 1024
Resolves: #219349

* Tue Dec 19 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-16
- Allow semanage to exec it self.  Label genhomedircon as semanage_exec_t
Resolves: #219421
- Allow sysadm_lpr_t to manage other print spool jobs
Resolves: #220080

* Mon Dec 18 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-15
- allow automount to setgid
Resolves: #219999

* Thu Dec 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-14
- Allow cron to polyinstatiate 
- Fix creation of boot flags
Resolves: #207433

* Thu Dec 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-13
- Fixes for irqbalance
Resolves: #219606

* Thu Dec 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-12
- Fix vixie-cron to work on mls
Resolves: #207433

* Wed Dec 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-11
Resolves: #218978

* Tue Dec 12 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-10
- Allow initrc to create files in /var directories
Resolves: #219227

* Fri Dec 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-9
- More fixes for MLS
Resolves: #181566

* Wed Dec 6 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-8
- More Fixes polyinstatiation
Resolves: #216184

* Wed Dec 6 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-7
- More Fixes polyinstatiation
- Fix handling of keyrings
Resolves: #216184

* Mon Dec 4 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-6
- Fix polyinstatiation
- Fix pcscd handling of terminal
Resolves: #218149
Resolves: #218350

* Fri Dec 1 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-5
- More fixes for quota
Resolves: #212957

* Fri Dec 1 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-4
- ncsd needs to use avahi sockets
Resolves: #217640
Resolves: #218014

* Thu Nov 30 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-3
- Allow login programs to polyinstatiate homedirs
Resolves: #216184
- Allow quotacheck to create database files
Resolves: #212957

* Tue Nov 28 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-1
- Dontaudit appending hal_var_lib files 
Resolves: #217452
Resolves: #217571
Resolves: #217611
Resolves: #217640
Resolves: #217725

* Tue Nov 21 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-4
- Fix context for helix players file_context #216942

* Mon Nov 20 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-3
- Fix load_policy to be able to mls_write_down so it can talk to the terminal

* Mon Nov 20 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-2
- Fixes for hwclock, clamav, ftp

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-1
- Move to upstream version which accepted my patches

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 2.4.4-2
- Fixes for nvidia driver

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.4-2
- Allow semanage to signal mcstrans

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.4-1
- Update to upstream

* Mon Nov 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-13
- Allow modstorage to edit /etc/fstab file

* Mon Nov 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-12
- Fix for qemu, /dev/

* Mon Nov 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-11
- Fix path to realplayer.bin

* Fri Nov 10 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-10
- Allow xen to connect to xen port

* Fri Nov 10 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-9
- Allow cups to search samba_etc_t directory
- Allow xend_t to list auto_mountpoints

* Thu Nov 9 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-8
- Allow xen to search automount

* Thu Nov 9 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-7
- Fix spec of jre files 

* Wed Nov 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-6
- Fix unconfined access to shadow file

* Wed Nov 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-5
- Allow xend to create files in xen_image_t directories

* Wed Nov 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-4
- Fixes for /var/lib/hal

* Tue Nov 7 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-3
- Remove ability for sysadm_t to look at audit.log

* Tue Nov 7 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-2
- Fix rpc_port_types
- Add aide policy for mls

* Mon Nov 6 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-1
- Merge with upstream

* Fri Nov 3 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-8
- Lots of fixes for ricci

* Fri Nov 3 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-7
- Allow xen to read/write fixed devices with a boolean
- Allow apache to search /var/log

* Thu Nov 2 2006 James Antill <james.antill@redhat.com> 2.4.2-6
- Fix policygentool specfile problem.
- Allow apache to send signals to it's logging helpers.
- Resolves: rhbz#212731

* Wed Nov 1 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-5
- Add perms for swat

* Tue Oct 31 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-4
- Add perms for swat

* Mon Oct 30 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-3
- Allow daemons to dump core files to /

* Fri Oct 27 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-2
- Fixes for ricci

* Fri Oct 27 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-1
- Allow mount.nfs to work

* Fri Oct 27 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-5
- Allow ricci-modstorage to look at lvm_etc_t

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-4
- Fixes for ricci using saslauthd

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-3
- Allow mountpoint on home_dir_t and home_t

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-2
- Update xen to read nfs files

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4-4
- Allow noxattrfs to associate with other noxattrfs 

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4-3
- Allow hal to use power_device_t

* Fri Oct 20 2006 Dan Walsh <dwalsh@redhat.com> 2.4-2
- Allow procemail to look at autofs_t
- Allow xen_image_t to work as a fixed device

* Thu Oct 19 2006 Dan Walsh <dwalsh@redhat.com> 2.4-1
- Refupdate from upstream

* Thu Oct 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-4
- Add lots of fixes for mls cups

* Wed Oct 18 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-3
- Lots of fixes for ricci

* Mon Oct 16 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-2
- Fix number of cats

* Mon Oct 16 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-1
- Update to upstream

* Thu Oct 12 2006 James Antill <jantill@redhat.com> 2.3.18-10
- More iSCSI changes for #209854

* Tue Oct 10 2006 James Antill <jantill@redhat.com> 2.3.18-9
- Test ISCSI fixes for #209854

* Sun Oct 8 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-8
- allow semodule to rmdir selinux_config_t dir

* Fri Oct 6 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-7
- Fix boot_runtime_t problem on ppc.  Should not be creating these files.

* Thu Oct 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-6
- Fix context mounts on reboot
- Fix ccs creation of directory in /var/log

* Thu Oct 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-5
- Update for tallylog

* Thu Oct 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-4
- Allow xend to rewrite dhcp conf files
- Allow mgetty sys_admin capability

* Wed Oct 4 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-3
- Make xentapctrl work

* Tue Oct 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-2
- Don't transition unconfined_t to bootloader_t
- Fix label in /dev/xen/blktap

* Tue Oct 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-1
- Patch for labeled networking

* Mon Oct 2 2006 Dan Walsh <dwalsh@redhat.com> 2.3.17-2
- Fix crond handling for mls

* Fri Sep 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.17-1
- Update to upstream

* Fri Sep 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-9
- Remove bluetooth-helper transition
- Add selinux_validate for semanage
- Require new version of libsemanage

* Fri Sep 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-8
- Fix prelink

* Fri Sep 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-7
- Fix rhgb

* Thu Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-6
- Fix setrans handling on MLS and useradd

* Wed Sep 27 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-5
- Support for fuse
- fix vigr

* Wed Sep 27 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-4
- Fix dovecot, amanda
- Fix mls

* Mon Sep 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-2
- Allow java execheap for itanium

* Mon Sep 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-1
- Update with upstream

* Mon Sep 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.15-2
- mls fixes 

* Fri Sep 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.15-1
- Update from upstream 

* Fri Sep 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-8
- More fixes for mls
- Revert change on automount transition to mount

* Wed Sep 20 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-7
- Fix cron jobs to run under the correct context

* Tue Sep 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-6
- Fixes to make pppd work

* Mon Sep 18 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-4
- Multiple policy fixes
- Change max categories to 1023

* Sat Sep 16 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-3
- Fix transition on mcstransd

* Fri Sep 15 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-2
- Add /dev/em8300 defs

* Fri Sep 15 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-1
- Upgrade to upstream

* Thu Sep 14 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-6
- Fix ppp connections from network manager

* Wed Sep 13 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-5
- Add tty access to all domains boolean
- Fix gnome-pty-helper context for ia64

* Mon Sep 11 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-4
- Fixed typealias of firstboot_rw_t

* Thu Sep 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-3
- Fix location of xel log files
- Fix handling of sysadm_r -> rpm_exec_t 

* Thu Sep 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-2
- Fixes for autofs, lp

* Wed Sep 6 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-1
- Update from upstream

* Tue Sep 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.12-2
- Fixup for test6

* Tue Sep 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.12-1
- Update to upstream

* Fri Sep 1 2006 Dan Walsh <dwalsh@redhat.com> 2.3.11-1
- Update to upstream

* Fri Sep 1 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-7
- Fix suspend to disk problems

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-6
- Lots of fixes for restarting daemons at the console.

* Wed Aug 30 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-3
- Fix audit line
- Fix requires line

* Tue Aug 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-1
- Upgrade to upstream

* Mon Aug 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-6
- Fix install problems

* Fri Aug 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-5
- Allow setroubleshoot to getattr on all dirs to gather RPM data

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-4
- Set /usr/lib/ia32el/ia32x_loader to unconfined_execmem_exec_t for ia32 platform
- Fix spec for /dev/adsp

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-3
- Fix xen tty devices

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-2
- Fixes for setroubleshoot

* Wed Aug 23 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-1
- Update to upstream

* Tue Aug 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.8-2
- Fixes for stunnel and postgresql
- Update from upstream

* Sat Aug 12 2006 Dan Walsh <dwalsh@redhat.com> 2.3.7-1
- Update from upstream
- More java fixes

* Fri Aug 11 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-4
- Change allow_execstack to default to on, for RHEL5 Beta.  
  This is required because of a Java compiler problem.
  Hope to turn off for next beta

* Thu Aug 10 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-3
- Misc fixes

* Wed Aug 9 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-2
- More fixes for strict policy

* Tue Aug 8 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-1
- Quiet down anaconda audit messages

* Mon Aug 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.5-1
- Fix setroubleshootd

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.4-1
- Update to the latest from upstream

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-20
- More fixes for xen

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-19
- Fix anaconda transitions

* Wed Aug 2 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-18
- yet more xen rules

* Tue Aug 1 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-17
- more xen rules

* Mon Jul 31 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-16
- Fixes for Samba

* Sat Jul 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-15
- Fixes for xen

* Fri Jul 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-14
- Allow setroubleshootd to send mail

* Wed Jul 26 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-13
- Add nagios policy

* Wed Jul 26 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-12
-  fixes for setroubleshoot

* Wed Jul 26 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-11
- Added Paul Howarth patch to only load policy packages shipped 
  with this package
- Allow pidof from initrc to ptrace higher level domains
- Allow firstboot to communicate with hal via dbus

* Mon Jul 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-10
- Add policy for /var/run/ldapi

* Sat Jul 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-9
- Fix setroubleshoot policy

* Fri Jul 21 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-8
- Fixes for mls use of ssh
- named  has a new conf file

* Fri Jul 21 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-7
- Fixes to make setroubleshoot work

* Wed Jul 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-6
- Cups needs to be able to read domain state off of printer client

* Wed Jul 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-5
- add boolean to allow zebra to write config files

* Tue Jul 18 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-4
- setroubleshootd fixes

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-3
- Allow prelink to read bin_t symlink
- allow xfs to read random devices
- Change gfs to support xattr

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-2
- Remove spamassassin_can_network boolean

* Fri Jul 14 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-1
- Update to upstream
- Fix lpr domain for mls

* Fri Jul 14 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-4
- Add setroubleshoot policy

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-3
- Turn off auditallow on setting booleans

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-2
- Multiple fixes

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-1
- Update to upstream

* Thu Jun 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.1-1
- Update to upstream
- Add new class for kernel key ring

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.49-1
- Update to upstream

* Tue Jun 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.48-1
- Update to upstream

* Tue Jun 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-5
- Break out selinux-devel package

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-4
- Add ibmasmfs

* Thu Jun 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-3
- Fix policygentool gen_requires

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-1
- Update from Upstream

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.46-2
- Fix spec of realplay

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.46-1
- Update to upstream

* Mon Jun 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-3
- Fix semanage

* Mon Jun 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-2
- Allow useradd to create_home_dir in MLS environment

* Thu Jun 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-1
- Update from upstream

* Tue Jun 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.44-1
- Update from upstream

* Tue Jun 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-4
- Add oprofilefs

* Sun May 28 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-3
- Fix for hplip and Picasus

* Sat May 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-2
- Update to upstream

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-1
- Update to upstream

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-4
- fixes for spamd

* Wed May 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-3
- fixes for java, openldap and webalizer

* Mon May 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-2
- Xen fixes

* Thu May 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-1
- Upgrade to upstream

* Thu May 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.41-1
- allow hal to read boot_t files
- Upgrade to upstream

* Wed May 17 2006 Dan Walsh <dwalsh@redhat.com> 2.2.40-2
- allow hal to read boot_t files

* Tue May 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.40-1
- Update from upstream

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.39-2
- Fixes for amavis

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.39-1
- Update from upstream

* Fri May 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-6
- Allow auditctl to search all directories

* Thu May 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-5
- Add acquire service for mono.

* Thu May 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-4
- Turn off allow_execmem boolean
- Allow ftp dac_override when allowed to access users homedirs

* Wed May 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-3
- Clean up spec file
- Transition from unconfined_t to prelink_t

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-2
- Allow execution of cvs command

* Fri May 5 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-1
- Update to upstream

* Wed May 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.37-1
- Update to upstream

* Mon May 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.36-2
- Fix libjvm spec

* Tue Apr 25 2006 Dan Walsh <dwalsh@redhat.com> 2.2.36-1
- Update to upstream

* Tue Apr 25 2006 James Antill <jantill@redhat.com> 2.2.35-2
- Add xm policy
- Fix policygentool

* Mon Apr 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.35-1
- Update to upstream
- Fix postun to only disable selinux on full removal of the packages

* Fri Apr 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-3
- Allow mono to chat with unconfined

* Thu Apr 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-2
- Allow procmail to sendmail
- Allow nfs to share dosfs

* Thu Apr 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-1
- Update to latest from upstream
- Allow selinux-policy to be removed and kernel not to crash

* Tue Apr 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.33-1
- Update to latest from upstream
- Add James Antill patch for xen
- Many fixes for pegasus

* Sat Apr 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.32-2
- Add unconfined_mount_t
- Allow privoxy to connect to httpd_cache
- fix cups labeleing on /var/cache/cups

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.32-1
- Update to latest from upstream

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.31-1
- Update to latest from upstream
- Allow mono and unconfined to talk to initrc_t dbus objects

* Tue Apr 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.30-2
- Change libraries.fc to stop shlib_t form overriding texrel_shlib_t

* Tue Apr 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.30-1
- Fix samba creating dirs in homedir
- Fix NFS so its booleans would work

* Mon Apr 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-6
- Allow secadm_t ability to relabel all files
- Allow ftp to search xferlog_t directories
- Allow mysql to communicate with ldap
- Allow rsync to bind to rsync_port_t

* Mon Apr 10 2006 Russell Coker <rcoker@redhat.com> 2.2.29-5
- Fixed mailman with Postfix #183928
- Allowed semanage to create file_context files.
- Allowed amanda_t to access inetd_t TCP sockets and allowed amanda_recover_t
  to bind to reserved ports.  #149030
- Don't allow devpts_t to be associated with tmp_t.
- Allow hald_t to stat all mountpoints.
- Added boolean samba_share_nfs to allow smbd_t full access to NFS mounts.
  #169947
- Make mount run in mount_t domain from unconfined_t to prevent mislabeling of
  /etc/mtab.
- Changed the file_contexts to not have a regex before the first ^/[a-z]/
  whenever possible, makes restorecon slightly faster.
- Correct the label of /etc/named.caching-nameserver.conf
- Now label /usr/src/kernels/.+/lib(/.*)? as usr_t instead of
  /usr/src(/.*)?/lib(/.*)? - I don't think we need anything else under /usr/src
  hit by this.
- Granted xen access to /boot, allowed mounting on xend_var_lib_t, and allowed
  xenstored_t rw access to the xen device node.

* Tue Apr 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-4
- More textrel_shlib_t file path fixes
- Add ada support

* Mon Apr 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-3
- Get auditctl working in MLS policy

* Mon Apr 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-2
- Add mono dbus support
- Lots of file_context fixes for textrel_shlib_t in FC5
- Turn off execmem auditallow since they are filling log files

* Fri Mar 31 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-1
- Update to upstream

* Thu Mar 30 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-3
- Allow automount and dbus to read cert files

* Thu Mar 30 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-2
- Fix ftp policy
- Fix secadm running of auditctl

* Mon Mar 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-1
- Update to upstream

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.27-1
- Update to upstream

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.25-3
- Fix policyhelp

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.25-2
- Fix pam_console handling of usb_device
- dontaudit logwatch reading /mnt dir

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 2.2.24-1
- Update to upstream

* Wed Mar 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-19
- Get transition rules to create policy.20 at SystemHigh

* Tue Mar 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-18
- Allow secadmin to shutdown system
- Allow sendmail to exec newalias

* Tue Mar 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-17
- MLS Fixes
     dmidecode needs mls_file_read_up
- add ypxfr_t
- run init needs access to nscd
- udev needs setuid
- another xen log file
- Dontaudit mount getattr proc_kcore_t

* Tue Mar 14 2006 Karsten Hopp <karsten@redhat.de> 2.2.23-16
- fix buildroot usage (#185391)

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-15
- Get rid of mount/fsdisk scan of /dev messages
- Additional fixes for suspend/resume

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-14
- Fake make to rebuild enableaudit.pp

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-13
- Get xen networking running.

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-12
- Fixes for Xen
- enableaudit should not be the same as base.pp
- Allow ps to work for all process

* Thu Mar  9 2006 Jeremy Katz <katzj@redhat.com> - 2.2.23-11
- more xen policy fixups

* Wed Mar  8 2006 Jeremy Katz <katzj@redhat.com> - 2.2.23-10
- more xen fixage (#184393)

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-9
- Fix blkid specification
- Allow postfix to execute mailman_que

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-8
- Blkid changes
- Allow udev access to usb_device_t
- Fix post script to create targeted policy config file

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-7
- Allow lvm tools to create drevice dir

* Tue Mar 7 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-5
- Add Xen support

* Mon Mar 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-4
- Fixes for cups
- Make cryptosetup work with hal

* Sun Mar 5 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-3
- Load Policy needs translock

* Sat Mar 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-2
- Fix cups html interface

* Sat Mar 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-1
- Add hal changes suggested by Jeremy
- add policyhelp to point at policy html pages

* Mon Feb 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.22-2
- Additional fixes for nvidia and cups

* Mon Feb 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.22-1
- Update to upstream
- Merged my latest fixes
- Fix cups policy to handle unix domain sockets

* Sat Feb 25 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-9
- NSCD socket is in nscd_var_run_t needs to be able to search dir

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-8
- Fixes Apache interface file

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-7
- Fixes for new version of cups

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-6
- Turn off polyinstatiate util after FC5

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-5
- Fix problem with privoxy talking to Tor

* Thu Feb 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-4
- Turn on polyinstatiation

* Thu Feb 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-3
- Don't transition from unconfined_t to fsadm_t

* Thu Feb 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-2
- Fix policy update model.

* Thu Feb 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-1
- Update to upstream

* Wed Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.20-1
- Fix load_policy to work on MLS
- Fix cron_rw_system_pipes for postfix_postdrop_t
- Allow audotmount to run showmount

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.19-2
- Fix swapon
- allow httpd_sys_script_t to be entered via a shell
- Allow httpd_sys_script_t to read eventpolfs

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.19-1
- Update from upstream

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.18-2
- allow cron to read apache files

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.18-1
- Fix vpnc policy to work from NetworkManager

* Mon Feb 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.17-2
- Update to upstream
- Fix semoudle polcy

* Thu Feb 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.16-1
- Update to upstream 
- fix sysconfig/selinux link

* Wed Feb 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-4
- Add router port for zebra
- Add imaze port for spamd
- Fixes for amanda and java

* Tue Feb 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-3
- Fix bluetooth handling of usb devices
- Fix spamd reading of ~/
- fix nvidia spec

* Tue Feb 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-1
- Update to upsteam

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.14-2
- Add users_extra files

* Fri Feb 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.14-1
- Update to upstream

* Fri Feb 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.13-1
- Add semodule policy

* Tue Feb 7 2006 Dan Walsh <dwalsh@redhat.com> 2.2.12-1
- Update from upstream

* Mon Feb 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.11-2
- Fix for spamd to use razor port

* Fri Feb 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.11-1
- Fixes for mcs
- Turn on mount and fsadm for unconfined_t

* Wed Feb 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.10-1
- Fixes for the -devel package

* Wed Feb 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.9-2
- Fix for spamd to use ldap

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.9-1
- Update to upstream

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.8-2
- Update to upstream
- Fix rhgb, and other Xorg startups

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.7-1
- Update to upstream

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-3
- Separate out role of secadm for mls

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-2
- Add inotifyfs handling

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-1
- Update to upstream
- Put back in changes for pup/zen

* Tue Jan 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.5-1
- Many changes for MLS 
- Turn on strict policy

* Mon Jan 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.4-1
- Update to upstream

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.3-1
- Update to upstream
- Fixes for booting and logging in on MLS machine

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.2-1
- Update to upstream
- Turn off execheap execstack for unconfined users
- Add mono/wine policy to allow execheap and execstack for them
- Add execheap for Xdm policy

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.1-1
- Update to upstream
- Fixes to fetchmail,

* Tue Jan 17 2006 Dan Walsh <dwalsh@redhat.com> 2.1.13-1
- Update to upstream

* Tue Jan 17 2006 Dan Walsh <dwalsh@redhat.com> 2.1.12-3
- Fix for procmail/spamassasin
- Update to upstream
- Add rules to allow rpcd to work with unlabeled_networks.

* Sat Jan 14 2006 Dan Walsh <dwalsh@redhat.com> 2.1.11-1
- Update to upstream
- Fix ftp Man page

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 2.1.10-1
- Update to upstream

* Wed Jan 11 2006 Jeremy Katz <katzj@redhat.com> - 2.1.9-2
- fix pup transitions (#177262)
- fix xen disks (#177599)

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 2.1.9-1
- Update to upstream

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-3
- More Fixes for hal and readahead

* Mon Jan 9 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-2
- Fixes for hal and readahead

* Mon Jan 9 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-1
- Update to upstream
- Apply 

* Fri Jan 6 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-4
- Add wine and fix hal problems

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-3
- Handle new location of hal scripts

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-2
- Allow su to read /etc/mtab

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-1
- Update to upstream

* Tue Jan 3 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-24
- Fix  "libsemanage.parse_module_headers: Data did not represent a module." problem

* Tue Jan 3 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-23
- Allow load_policy to read /etc/mtab

* Mon Jan 2 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-22
- Fix dovecot to allow dovecot_auth to look at /tmp

* Mon Jan 2 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-21
- Allow restorecon to read unlabeled_t directories in order to fix labeling.

* Fri Dec 30 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-20
- Add Logwatch policy

* Wed Dec 28 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-18
- Fix /dev/ub[a-z] file context

* Tue Dec 27 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-17
- Fix library specification
- Give kudzu execmem privs

* Thu Dec 22 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-16
- Fix hostname in targeted policy

* Wed Dec 21 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-15
- Fix passwd command on mls

* Wed Dec 21 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-14
- Lots of fixes to make mls policy work

* Tue Dec 20 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-13
- Add dri libs to textrel_shlib_t
- Add system_r role for java
- Add unconfined_exec_t for vncserver
- Allow slapd to use kerberos

* Mon Dec 19 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-11
- Add man pages

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-10
- Add enableaudit.pp

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-9
- Fix mls policy

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-8
- Update mls file from old version

* Thu Dec 15 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-5
- Add sids back in
- Rebuild with update checkpolicy

* Thu Dec 15 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-4
- Fixes to allow automount to use portmap
- Fixes to start kernel in s0-s15:c0.c255

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-3
- Add java unconfined/execmem policy 

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-2
- Add file context for /var/cvs
- Dontaudit webalizer search of homedir

* Tue Dec 13 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-1
- Update from upstream

* Tue Dec 13 2005 Dan Walsh <dwalsh@redhat.com> 2.1.4-2
- Clean up spec
- range_transition crond to SystemHigh

* Mon Dec 12 2005 Dan Walsh <dwalsh@redhat.com> 2.1.4-1
- Fixes for hal
- Update to upstream

* Mon Dec 12 2005 Dan Walsh <dwalsh@redhat.com> 2.1.3-1
- Turn back on execmem since we need it for java, firefox, ooffice
- Allow gpm to stream socket to itself

* Mon Dec 12 2005 Jeremy Katz <katzj@redhat.com> - 2.1.2-3
- fix requirements to be on the actual packages so that policy can get
  created properly at install time

* Sun Dec  11 2005 Dan Walsh <dwalsh@redhat.com> 2.1.2-2
- Allow unconfined_t to execmod texrel_shlib_t

* Sat Dec  10 2005 Dan Walsh <dwalsh@redhat.com> 2.1.2-1
- Update to upstream 
- Turn off allow_execmem and allow_execmod booleans
- Add tcpd and automount policies

* Fri Dec  9 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-3
- Add two new httpd booleans, turned off by default
     * httpd_can_network_relay
     * httpd_can_network_connect_db

* Fri Dec  9 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-2
- Add ghost for policy.20

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-1
- Update to upstream
- Turn off boolean allow_execstack

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-3
- Change setrans-mls to use new libsetrans
- Add default_context rule for xdm

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-2.
- Change Requires to PreReg for requiring of policycoreutils on install

* Wed Dec  7 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-1.
- New upstream release

* Wed Dec  7 2005 Dan Walsh <dwalsh@redhat.com> 2.0.11-2.
Add xdm policy

* Tue Dec  6 2005 Dan Walsh <dwalsh@redhat.com> 2.0.11-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.9-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.8-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.7-3
- Also trigger to rebuild policy for versions up to 2.0.7.

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 2.0.7-2
- No longer installing policy.20 file, anaconda handles the building of the app.

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 2.0.6-2
- Fixes for dovecot and saslauthd

* Wed Nov 23 2005 Dan Walsh <dwalsh@redhat.com> 2.0.5-4
- Cleanup pegasus and named 
- Fix spec file
- Fix up passwd changing applications

* Tue Nov 22 2005 Dan Walsh <dwalsh@redhat.com> 2.0.5-1
-Update to latest from upstream

* Tue Nov 22 2005 Dan Walsh <dwalsh@redhat.com> 2.0.4-1
- Add rules for pegasus and avahi

* Mon Nov 21 2005 Dan Walsh <dwalsh@redhat.com> 2.0.2-2
- Start building MLS Policy

* Fri Nov 18 2005 Dan Walsh <dwalsh@redhat.com> 2.0.2-1
- Update to upstream

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 2.0.1-2
- Turn on bash

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 2.0.1-1
- Initial version
