# upstream does not currently support a mariner distro
%define distro redhat
%define polyinstatiate n
%define monolithic n
%define POLICYVER 31
%define POLICYCOREUTILSVER 2.9
%define CHECKPOLICYVER 2.9
Summary: SELinux policy
Name: selinux-policy
Version:2.20200818
Release: 1%{?dist}
License: GPLv2+
Source0: https://github.com/SELinuxProject/refpolicy/releases/download/RELEASE_2_20200818/refpolicy-%{version}.tar.bz2
Source1: Makefile.devel
Url: https://github.com/SELinuxProject/refpolicy
BuildArch: noarch
BuildRequires: python3 checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils-devel >= %{POLICYCOREUTILSVER} bzip2
#BuildRequires: gcc
BuildRequires: python3-xml
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
# TODO: Do we need below?
Conflicts:  audispd-plugins <= 1.7.7-1

%description
SELinux policy describes security properties of system components, to be
enforced by the kernel when running with SELinux enabled.

%files
%{!?_licensedir:%global license %%doc}
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
Summary: SELinux policy devel
Requires: m4 checkpolicy >= %{CHECKPOLICYVER}
Requires: /usr/bin/make
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
selinuxenabled && /usr/bin/sepolgen-ifgen 2>/dev/null
exit 0

%package doc
Summary: SELinux policy documentation
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}

%description doc
SELinux policy documentation package

%files doc
%{_mandir}/man*/*
%{_mandir}/ru/*/*
%doc %{_usr}/share/doc/%{name}

%define makeCmds() \
%make_build UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024 bare \
%make_build UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024 conf


%define installCmds() \
%make_build UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024 base.pp \
%make_build validate UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024 modules \
make UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} MLS_CATS=1024 MCS_CATS=1024 install \
make UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} MLS_CATS=1024 MCS_CATS=1024 install-appconfig \
make UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} MLS_CATS=1024 MCS_CATS=1024 SEMODULE="semodule -p %{buildroot} -X 100 " load \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/logins \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.subs \
install -m0644 config/appconfig-%2/securetty_types %{buildroot}%{_sysconfdir}/selinux/%1/contexts/securetty_types \
install -m0644 config/file_contexts.subs_dist %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.bin \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.local \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.local.bin \
rm -f %{buildroot}/%{_usr}/share/selinux/%1/*pp*  \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/contexts/netfilter_contexts  \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/modules/active/policy.kern \
rm -f %{buildroot}%{_sharedstatedir}/selinux/%1/active/*.linked \
%nil

%define relabel() \
. %{_sysconfdir}/selinux/config; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
/usr/sbin/selinuxenabled; \
if [ $? = 0  -a "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT}.pre ]; then \
     /sbin/fixfiles -C ${FILE_CONTEXT}.pre restore &> /dev/null > /dev/null; \
     rm -f ${FILE_CONTEXT}.pre; \
fi; \
if /sbin/restorecon -e /run/media -R /root /var/log /var/run /etc/passwd* /etc/group* /etc/*shadow* 2> /dev/null;then \
    continue; \
fi; \

%define preInstall() \
if [ -s /etc/selinux/config ]; then \
     . %{_sysconfdir}/selinux/config; \
     FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
     if [ "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT} ]; then \
        [ -f ${FILE_CONTEXT}.pre ] || cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.pre; \
     fi; \
     touch /etc/selinux/%1/.rebuild; \
fi;

%define postInstall() \
. %{_sysconfdir}/selinux/config; \
if [ -e /etc/selinux/%2/.rebuild ]; then \
   rm /etc/selinux/%2/.rebuild; \
   /usr/sbin/semodule -B -n -s %2; \
fi; \
[ "${SELINUXTYPE}" == "%2" ] && selinuxenabled && load_policy; \
if [ %1 -eq 1 ]; then \
   /sbin/restorecon -R /root /var/log /run /etc/passwd* /etc/group* /etc/*shadow* 2> /dev/null; \
else \
%relabel %2 \
fi;

%prep
%setup -n refpolicy -q

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
if [ ! -s /etc/selinux/config ]; then
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

" > /etc/selinux/config

     ln -sf ../selinux/config /etc/sysconfig/selinux
     restorecon /etc/selinux/config 2> /dev/null || :
else
     . /etc/selinux/config
fi
%postInstall $1 repolicy
exit 0

%postun
if [ $1 = 0 ]; then
     setenforce 0 2> /dev/null
     if [ ! -s /etc/selinux/config ]; then
          echo "SELINUX=disabled" > /etc/selinux/config
     else
          sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
     fi
fi
exit 0

%pre
%preInstall refpolicy

%triggerin -- pcre
selinuxenabled && semodule -nB
exit 0

%changelog
* Mon Aug 31 2020 Daniel Burgener <daburgen@microsoft.com> 2.20200818-1
- Initial creation.  Loosely based on spec from Fedora 31
