%define distro mariner
%define polyinstatiate n
%define monolithic n
%define policy_name targeted
%define refpolicy_major 2
%define refpolicy_minor 20210203
%define POLICYCOREUTILSVER 3.2
%define CHECKPOLICYVER 3.2
Summary:        SELinux policy
Name:           selinux-policy
Version:        %{refpolicy_major}.%{refpolicy_minor}
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/SELinuxProject/refpolicy
Source0:        %{url}/releases/download/RELEASE_${refpolicy_major}_${refpolicy_minor}/refpolicy-%{version}.tar.bz2
Source1:        Makefile.devel
Patch0:         0001-various-systemd-user-fixes-and-additional-support.patch
Patch1:         0002-Allow-use-of-systemd-UNIX-sockets-created-at-initrd-.patch
Patch2:         0003-files-init-systemd-various-fixes.patch
Patch3:         0004-Enable-factory-directory-support-in-systemd-tmpfiles.patch
Patch4:         0005-Makefile-Revise-relabel-targets-to-relabel-all-secla.patch
Patch5:         0006-cronyd-Add-dac_read_search.patch
Patch6:         0007-systemd-ssh-ntp-Read-fips_enabled-crypto-sysctl.patch
Patch7:         0008-udev-Manage-EFI-variables.patch
Patch8:         0009-ntp-Handle-symlink-to-drift-directory.patch
Patch9:         0010-systemd-Unit-generator-fixes.patch
Patch10:        0011-logging-Allow-auditd-to-stat-dispatcher-executables.patch
Patch11:        0012-systemd-Revise-tmpfiles-factory-to-allow-writing-all.patch
Patch12:        0013-systemd-User-runtime-reads-user-cgroup-files.patch
Patch13:        0014-logging-Add-audit_control-for-journald.patch
Patch14:        0015-Temporary-fix-for-wrong-audit-log-directory.patch
Patch15:        0016-Set-default-login-to-unconfined_u.patch
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
%{_datadir}/selinux/%{policy_name}
%dir %{_sysconfdir}/selinux/%{policy_name}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/selinux/%{policy_name}/seusers
%dir %{_sysconfdir}/selinux/%{policy_name}/logins
%dir %{_sharedstatedir}/selinux/%{policy_name}/active
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%{policy_name}/semanage.read.LOCK
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%{policy_name}/semanage.trans.LOCK
%dir %attr(700,root,root) %dir %{_sharedstatedir}/selinux/%{policy_name}/active/modules
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%{policy_name}/active/modules/100/base
%dir %{_sysconfdir}/selinux/%{policy_name}/policy/
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%{policy_name}/policy/policy.*
%dir %{_sysconfdir}/selinux/%{policy_name}/contexts
%config %{_sysconfdir}/selinux/%{policy_name}/contexts/customizable_types
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/securetty_types
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/dbus_contexts
%config %{_sysconfdir}/selinux/%{policy_name}/contexts/x_contexts
%config %{_sysconfdir}/selinux/%{policy_name}/contexts/default_contexts
%config %{_sysconfdir}/selinux/%{policy_name}/contexts/virtual_domain_context
%config %{_sysconfdir}/selinux/%{policy_name}/contexts/virtual_image_context
%config %{_sysconfdir}/selinux/%{policy_name}/contexts/lxc_contexts
%config %{_sysconfdir}/selinux/%{policy_name}/contexts/sepgsql_contexts
%config %{_sysconfdir}/selinux/%{policy_name}/contexts/openrc_contexts
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/default_type
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/failsafe_context
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/initrc_context
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/removable_context
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/userhelper_context
%dir %{_sysconfdir}/selinux/%{policy_name}/contexts/files
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%{policy_name}/contexts/files/file_contexts
%ghost %{_sysconfdir}/selinux/%{policy_name}/contexts/files/file_contexts.bin
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%{policy_name}/contexts/files/file_contexts.homedirs
%ghost %{_sysconfdir}/selinux/%{policy_name}/contexts/files/file_contexts.homedirs.bin
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/files/file_contexts.local
%ghost %{_sysconfdir}/selinux/%{policy_name}/contexts/files/file_contexts.local.bin
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/files/file_contexts.subs
%{_sysconfdir}/selinux/%{policy_name}/contexts/files/file_contexts.subs_dist
%config %{_sysconfdir}/selinux/%{policy_name}/contexts/files/media
%dir %{_sysconfdir}/selinux/%{policy_name}/contexts/users
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/users/root
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/users/guest_u
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/users/xguest_u
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/users/user_u
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/users/staff_u
%config(noreplace) %{_sysconfdir}/selinux/%{policy_name}/contexts/users/unconfined_u
%{_sharedstatedir}/selinux/%{policy_name}/active/commit_num
%{_sharedstatedir}/selinux/%{policy_name}/active/users_extra
%{_sharedstatedir}/selinux/%{policy_name}/active/homedir_template
%{_sharedstatedir}/selinux/%{policy_name}/active/seusers
%{_sharedstatedir}/selinux/%{policy_name}/active/file_contexts
%{_sharedstatedir}/selinux/%{policy_name}/active/policy.kern
%ghost %{_sharedstatedir}/selinux/%{policy_name}/active/policy.linked
%ghost %{_sharedstatedir}/selinux/%{policy_name}/active/seusers.linked
%ghost %{_sharedstatedir}/selinux/%{policy_name}/active/users_extra.linked
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%{policy_name}/active/file_contexts.homedirs
%ghost %{_sharedstatedir}/selinux/%{policy_name}/active/modules/100/*

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
mkdir -p %{buildroot}%{_usr}/share/selinux/%{policy_name}
mkdir -p %{buildroot}%{_sharedstatedir}/selinux/{%{policy_name},modules}/

mkdir -p %{buildroot}%{_usr}/share/selinux/packages

# Install devel
make clean
%makeCmds targeted mcs n allow
%installCmds targeted mcs n allow

# remove leftovers when save-previous=true (semanage.conf) is used
rm -rf %{buildroot}%{_sharedstatedir}/selinux/%{policy_name}/previous

mkdir -p %{buildroot}%{_mandir}
cp -R  man/* %{buildroot}%{_mandir}
make UNK_PERMS=allow NAME=%{policy_name} TYPE=mcs DISTRO=%{distro} UBAC=n DIRECT_INITRC=n MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name} MLS_CATS=1024 MCS_CATS=1024 install-docs
make UNK_PERMS=allow NAME=%{policy_name} TYPE=mcs DISTRO=%{distro} UBAC=n DIRECT_INITRC=n MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name} MLS_CATS=1024 MCS_CATS=1024 install-headers
mkdir %{buildroot}%{_usr}/share/selinux/devel/
mv %{buildroot}%{_usr}/share/selinux/%{policy_name}/include %{buildroot}%{_usr}/share/selinux/devel/include
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
#     Currently the only supported option is %{policy_name}
SELINUXTYPE=%{policy_name}

" > %{_sysconfdir}/selinux/config

     ln -sf ../selinux/config %{_sysconfdir}/sysconfig/selinux
     restorecon %{_sysconfdir}/selinux/config 2> /dev/null || :
else
     . %{_sysconfdir}/selinux/config
fi
%postInstall $1 %{policy_name}
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
%preInstall %{policy_name}

%triggerin -- pcre
selinuxenabled && semodule -nB
exit 0
%changelog
* Tue Sep 07 2021 Chris PeBenito <chpebeni@microsoft.com> - 2.20210203-1
- Update to newest refpolicy release.  Add policy changes to boot the system
  in enforcing.  Change policy name to targeted.  Remove unrelated changelog
  entries from selinux-policy. The spec file uses the Fedora spec file as
  guidance, but does not use the Fedora's policy. The Fedora policy is a hard
  fork Reference Policy, so the changes are not related and the version numbers
  are incomparable.

* Fri Aug 13 2021 Thomas Crain <thcrain@microsoft.com> - 2.20200818-2
- Update versions on checkpolicy, policycoreutils dependencies

* Mon Aug 31 2020 Daniel Burgener <daburgen@microsoft.com> - 2.20200818-1
- Initial CBL-Mariner import from Fedora 31 (license: MIT)
- Heavy modifications to build from upstream reference policy rather than from fedora selinux policy.
  Fedora's policy and versioning tracks their policy fork specificially, whereas this tracks the upstream
  policy that Fedora's policy is based on.
- License verified
