# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# install init scripts to /usr/libexec with systemd
%global script_path %{_libexecdir}/iptables

# service legacy actions (RHBZ#748134)
%global legacy_actions %{_libexecdir}/initscripts/legacy-actions

%global iptc_so_ver  0
%global ipXtc_so_ver 2

Name: iptables
Summary: Tools for managing Linux kernel packet filtering capabilities
URL: https://www.netfilter.org/projects/iptables
Version: 1.8.11
Release: 13%{?dist}
Source0: %{url}/files/%{name}-%{version}.tar.xz
source1: %{url}/files/%{name}-%{version}.tar.xz.sig
Source2: coreteam-gpg-key-0xD70D1A666ACF2B21.txt
Source3: iptables.init
Source4: iptables-config
Source5: iptables.service
Source6: sysconfig_iptables
Source7: sysconfig_ip6tables
Source8: arptables-helper
Source9: arptables.service
Source10: ebtables.service
Source11: ebtables-helper
Source12: ebtables-config
# Patch to fix -C handling, already upstream
# https://git.netfilter.org/iptables/patch/?id=40406dbfaefbc204134452b2747bae4f6a122848
Patch1: iptables-1.8.11-fix-interface-comparisons.patch
# Patch to fix overly strict command option checking
# https://git.netfilter.org/iptables/patch/?id=192c3a6bc18f206895ec5e38812d648ccfe7e281
Patch2: iptables-1.8.11-command-options-fix.patch

# pf.os: ISC license
# iptables-apply: Artistic Licence 2.0
License: GPL-2.0-only AND Artistic-2.0 AND ISC

# libnetfilter_conntrack is needed for xt_connlabel
BuildRequires: pkgconfig(libnetfilter_conntrack)
# libnfnetlink-devel is required for nfnl_osf
BuildRequires: pkgconfig(libnfnetlink)
BuildRequires: libselinux-devel
BuildRequires: kernel-headers
BuildRequires: systemd
# libmnl, libnftnl, bison, flex for nftables
BuildRequires: bison
BuildRequires: flex
BuildRequires: gcc
BuildRequires: pkgconfig(libmnl) >= 1.0
BuildRequires: pkgconfig(libnftnl) >= 1.2.6
# libpcap-devel for nfbpf_compile
BuildRequires: libpcap-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: make
BuildRequires: gnupg2

%description
The iptables utility controls the network packet filtering code in the
Linux kernel. If you need to set up firewalls and/or IP masquerading,
you should install this package.

%package legacy
Summary: Legacy tools for managing Linux kernel packet filtering capabilities
Requires: %{name}-legacy-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Conflicts: setup < 2.10.4-1
Conflicts: alternatives < 1.32-1
Requires(post): /usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
%if 0%{?rhel} < 9
Provides:	iptables
%endif
Provides:  %{name}-compat = %{version}-%{release}
Obsoletes: %{name}-compat < 1.8.9-7

%sbin_merge_compat %{_prefix}/sbin/iptables

%description legacy
The iptables utility controls the network packet filtering code in the
Linux kernel. This package contains the legacy tools which are obsoleted by
nft-variants in iptables-nft package for backwards compatibility reasons.
If you need to set up firewalls and/or IP masquerading, you should not install
this package but either nftables or iptables-nft instead.

%package libs
Summary: libxtables and iptables extensions userspace support

%description libs
libxtables and associated shared object files

Libxtables provides unified access to iptables extensions in userspace. Data
and logic for those is kept in per-extension shared object files.

%package legacy-libs
Summary: iptables legacy libraries

%description legacy-libs
iptables libraries.

Please remember that libip*tc libraries do neither have a stable API nor a real
so version. For more information about this, please have a look at

  http://www.netfilter.org/documentation/FAQ/netfilter-faq-4.html#ss4.5

%package devel
Summary: Development package for iptables
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
# XXX: Drop this after two releases or so
Requires: %{name}-legacy-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
libxtables development headers and pkgconfig files

%package legacy-devel
Summary: Development package for legacy iptables
Requires: %{name}-legacy-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description legacy-devel
Legacy iptables development headers and pkgconfig files

The iptc libraries are marked as not public by upstream. The interface is not
stable and may change with every new version. It is therefore unsupported.

%package services
Summary: iptables and ip6tables services for iptables
Requires: %{name} = %{version}-%{release}
Requires: %{name}-utils = %{version}-%{release}
%{?systemd_ordering}
# obsolete old main package
Obsoletes: %{name} < 1.4.16.1
# obsolete ipv6 sub package
Obsoletes: %{name}-ipv6 < 1.4.11.1
# Look at me, I'm the new arptables-services now!
Conflicts: %{name}-nft < 1.8.11-5
Obsoletes: arptables-services < 0.0.5-16
Provides: arptables-services = %{version}-%{release}
# Look at me, I'm the new ebtables-services now!
# (With epoch to turn our version number higher value)
Obsoletes: ebtables-services < 2.0.11-20
Provides: ebtables-services = 1:%{version}-%{release}
BuildArch: noarch

%description services
iptables services for IPv4 and IPv6

This package provides the services iptables and ip6tables that have been split
out of the base package since they are not active by default anymore.

%package utils
Summary: iptables and ip6tables misc utilities
Requires: %{name} = %{version}-%{release}

%description utils
Utils for iptables

This package provides nfnl_osf with the pf.os database and nfbpf_compile,
a bytecode generator for use with xt_bpf. Also included is iptables-apply,
a safer way to update iptables remotely.

%package nft
Summary: nftables compatibility for iptables, arptables and ebtables
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires(post): /usr/sbin/update-alternatives
Requires(post): /usr/bin/readlink
Requires(postun): /usr/sbin/update-alternatives
Obsoletes: iptables-compat < 1.6.2-4
Provides: arptables-helper
Provides: iptables
Provides: arptables
Provides: ebtables
# allowing old arptables-legacy will break when switching alternatives
# due to the dropped arptables-helper symlink
Conflicts: arptables-legacy < 0.0.5-16

%sbin_merge_compat %{_prefix}/sbin/iptables

%description nft
nftables compatibility for iptables, arptables and ebtables.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
./autogen.sh
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing " \
%configure --enable-devel --enable-bpf-compiler --with-kernel=/usr --with-kbuild=/usr --with-ksource=/usr

# do not use rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

rm -f include/linux/types.h

%make_build

%install
%make_install
# remove la file(s)
rm -f %{buildroot}%{_libdir}/*.la

# install init scripts and configuration files
install -d -m 755 %{buildroot}%{script_path}
install -c -m 755 %{SOURCE3} %{buildroot}%{script_path}/iptables.init
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE3} > ip6tables.init
install -c -m 755 ip6tables.init %{buildroot}%{script_path}/ip6tables.init
install -p -m 755 %{SOURCE8} %{SOURCE11} %{buildroot}%{_libexecdir}/
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -c -m 600 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/iptables-config
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE4} > ip6tables-config
install -c -m 600 ip6tables-config %{buildroot}%{_sysconfdir}/sysconfig/ip6tables-config
install -c -m 600 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/iptables
install -c -m 600 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysconfig/ip6tables
echo '# Configure prior to use' > %{buildroot}%{_sysconfdir}/sysconfig/arptables
install -c -m 600 %{SOURCE12} %{buildroot}%{_sysconfdir}/sysconfig/
touch %{buildroot}%{_sysconfdir}/sysconfig/ebtables

# install systemd service files
install -d -m 755 %{buildroot}/%{_unitdir}
install -c -m 644 %{SOURCE5} %{SOURCE9} %{SOURCE10} %{buildroot}/%{_unitdir}
sed -e 's;iptables;ip6tables;g' -e 's;IPv4;IPv6;g' -e 's;/usr/libexec/ip6tables;/usr/libexec/iptables;g' < %{SOURCE5} > ip6tables.service
install -c -m 644 ip6tables.service %{buildroot}/%{_unitdir}

# install legacy actions for service command
install -d %{buildroot}/%{legacy_actions}/iptables
install -d %{buildroot}/%{legacy_actions}/ip6tables

cat << EOF > %{buildroot}/%{legacy_actions}/iptables/save
#!/bin/bash
exec %{script_path}/iptables.init save
EOF
chmod 755 %{buildroot}/%{legacy_actions}/iptables/save
sed -e 's;iptables.init;ip6tables.init;g' -e 's;IPTABLES;IP6TABLES;g' < %{buildroot}/%{legacy_actions}/iptables/save > ip6tabes.save-legacy
install -c -m 755 ip6tabes.save-legacy %{buildroot}/%{legacy_actions}/ip6tables/save

cat << EOF > %{buildroot}/%{legacy_actions}/iptables/panic
#!/bin/bash
exec %{script_path}/iptables.init panic
EOF
chmod 755 %{buildroot}/%{legacy_actions}/iptables/panic
sed -e 's;iptables.init;ip6tables.init;g' -e 's;IPTABLES;IP6TABLES;g' < %{buildroot}/%{legacy_actions}/iptables/panic > ip6tabes.panic-legacy
install -c -m 755 ip6tabes.panic-legacy %{buildroot}/%{legacy_actions}/ip6tables/panic

# Remove /etc/ethertypes (now part of setup)
rm -f %{buildroot}%{_sysconfdir}/ethertypes

# prepare for alternatives
touch %{buildroot}%{_mandir}/man8/arptables.8
touch %{buildroot}%{_mandir}/man8/arptables-save.8
touch %{buildroot}%{_mandir}/man8/arptables-restore.8
touch %{buildroot}%{_mandir}/man8/ebtables.8
rm %{buildroot}%{_sbindir}/{ip,ip6,arp,eb}tables{,-save,-restore}
touch %{buildroot}%{_sbindir}/{ip,ip6,arp,eb}tables{,-save,-restore}

# fix absolute symlink
ln -sf --relative %{buildroot}%{_sbindir}/xtables-legacy-multi %{buildroot}%{_bindir}/iptables-xml

%ldconfig_scriptlets

%post legacy
pfx=%{_sbindir}/iptables
pfx6=%{_sbindir}/ip6tables
update-alternatives --install \
	$pfx iptables $pfx-legacy 10 \
	--follower $pfx6 ip6tables $pfx6-legacy \
	--follower $pfx-restore iptables-restore $pfx-legacy-restore \
	--follower $pfx-save iptables-save $pfx-legacy-save \
	--follower $pfx6-restore ip6tables-restore $pfx6-legacy-restore \
	--follower $pfx6-save ip6tables-save $pfx6-legacy-save

%if "%{_sbindir}" == "%{_bindir}"
# Make sure that symlinks in /usr/sbin/ are not missing, if /usr/sbin is a
# directory. Those symlinks will only be created if there is no symlink
# or file already.
for name in ip{,6}tables{,-save,-restore}; do
    test -h /usr/sbin || ln -s ../bin/$name /usr/sbin/$name 2>/dev/null || :
done
%endif

%postun legacy
if [ $1 -eq 0 ]; then
	update-alternatives --remove \
		iptables %{_sbindir}/iptables-legacy
fi

# iptables-1.8.0-1 introduced the use of alternatives
# when upgrading, its %postun script runs due to the package renaming
# fix this by repeating the install into alternatives
# also keep the old alternatives configuration to not change the system
%triggerun legacy -- iptables > 1.8.0
alternatives --list | awk '/^iptables/{print $3; exit}' \
		>/var/tmp/alternatives.iptables.current
cp /var/lib/alternatives/iptables /var/tmp/alternatives.iptables.setup

%triggerpostun legacy -- iptables > 1.8.0
pfx=%{_sbindir}/iptables
pfx6=%{_sbindir}/ip6tables
update-alternatives --install \
	$pfx iptables $pfx-legacy 10 \
	--follower $pfx6 ip6tables $pfx6-legacy \
	--follower $pfx-restore iptables-restore $pfx-legacy-restore \
	--follower $pfx-save iptables-save $pfx-legacy-save \
	--follower $pfx6-restore ip6tables-restore $pfx6-legacy-restore \
	--follower $pfx6-save ip6tables-save $pfx6-legacy-save
alternatives --set iptables $(</var/tmp/alternatives.iptables.current)
rm /var/tmp/alternatives.iptables.current
mv /var/tmp/alternatives.iptables.setup /var/lib/alternatives/iptables

%if "%{_sbindir}" == "%{_bindir}"
# Make sure that symlinks in /usr/sbin/ are not missing, if /usr/sbin is a
# directory. Those symlinks will only be created if there is no symlink
# or file already.
for name in ip{,6}tables{,-save,-restore}; do
    test -h /usr/sbin || ln -s ../bin/$name /usr/sbin/$name 2>/dev/null || :
done
%endif

%post services
%systemd_post arptables.service ebtables.service
%systemd_post iptables.service ip6tables.service

%preun services
%systemd_preun arptables.service ebtables.service
%systemd_preun iptables.service ip6tables.service

%postun services
%?ldconfig
%systemd_postun arptables.service ebtables.service
%systemd_postun iptables.service ip6tables.service

%post -e nft
[[ %%{_excludedocs} == 1 ]] || do_man=true

# remove non-symlinks in spots managed by alternatives
# to cover for updates from not-yet-alternatived versions
for pfx in %{_prefix}/sbin/{eb,arp}tables; do
	for sfx in "" "-restore" "-save"; do
		if [ "$(readlink -e $pfx$sfx)" == $pfx$sfx ]; then
			rm -f $pfx$sfx
		fi
	done
done
for manpfx in %{_mandir}/man8/{eb,arp}tables; do
	for sfx in {,-restore,-save}.8.gz; do
		if [ "$(readlink -e $manpfx$sfx)" == $manpfx$sfx ]; then
			rm -f $manpfx$sfx
		fi
	done
done

pfx=%{_sbindir}/iptables
pfx6=%{_sbindir}/ip6tables
update-alternatives --install \
	$pfx iptables $pfx-nft 10 \
	--follower $pfx6 ip6tables $pfx6-nft \
	--follower $pfx-restore iptables-restore $pfx-nft-restore \
	--follower $pfx-save iptables-save $pfx-nft-save \
	--follower $pfx6-restore ip6tables-restore $pfx6-nft-restore \
	--follower $pfx6-save ip6tables-save $pfx6-nft-save

pfx=%{_sbindir}/ebtables
manpfx=%{_mandir}/man8/ebtables
update-alternatives --install \
	$pfx ebtables $pfx-nft 10 \
	--follower $pfx-save ebtables-save $pfx-nft-save \
	--follower $pfx-restore ebtables-restore $pfx-nft-restore \
	${do_man:+--follower $manpfx.8.gz ebtables-man $manpfx-nft.8.gz}

pfx=%{_sbindir}/arptables
manpfx=%{_mandir}/man8/arptables
update-alternatives --install \
	$pfx arptables $pfx-nft 10 \
	--follower $pfx-save arptables-save $pfx-nft-save \
	--follower $pfx-restore arptables-restore $pfx-nft-restore \
	${do_man:+--follower $manpfx.8.gz arptables-man $manpfx-nft.8.gz} \
	${do_man:+--follower $manpfx-save.8.gz arptables-save-man $manpfx-nft-save.8.gz} \
	${do_man:+--follower $manpfx-restore.8.gz arptables-restore-man $manpfx-nft-restore.8.gz}

%if "%{_sbindir}" == "%{_bindir}"
# Make sure that symlinks in /usr/sbin/ are not missing, if /usr/sbin is a
# directory. Those symlinks will only be created if there is no symlink
# or file already.
for name in ip{,6}tables{,-save,-restore} ebtables{,-save,-restore} arptables{,-save,-restore}; do
    test -h /usr/sbin || ln -s ../bin/$name /usr/sbin/$name 2>/dev/null || :
done
%endif

%postun nft
if [ $1 -eq 0 ]; then
	for cmd in iptables ebtables arptables; do
		update-alternatives --remove $cmd %{_sbindir}/$cmd-nft
	done
fi

%files legacy
%{_sbindir}/ip{,6}tables-legacy*
%{_sbindir}/xtables-legacy-multi
%{_bindir}/iptables-xml
%{_mandir}/man1/iptables-xml*
%{_mandir}/man8/xtables-legacy*
%dir %{_datadir}/xtables
%{_datadir}/xtables/iptables.xslt
%ghost %attr(0755,root,root) %{_sbindir}/ip{,6}tables{,-save,-restore}

%files libs
%license COPYING
%{_libdir}/libxtables.so.12*
%dir %{_libdir}/xtables
%{_libdir}/xtables/lib{ip,ip6,x}t*
%{_mandir}/man8/ip{,6}tables.8.gz
%{_mandir}/man8/ip{,6}tables-{extensions,save,restore}.8.gz

%files legacy-libs
%license COPYING
%{_libdir}/libip{4,6}tc.so.%{ipXtc_so_ver}*

%files devel
%{_includedir}/xtables{,-version}.h
%{_libdir}/libxtables.so
%{_libdir}/pkgconfig/xtables.pc

%files legacy-devel
%dir %{_includedir}/libiptc
%{_includedir}/libiptc/*.h
%{_libdir}/libip*tc.so
%{_libdir}/pkgconfig/libip{,4,6}tc.pc

%files services
%dir %{script_path}
%{script_path}/ip{,6}tables.init
%config(noreplace) %{_sysconfdir}/sysconfig/ip{,6}tables{,-config}
%config(noreplace) %{_sysconfdir}/sysconfig/arptables
%config(noreplace) %{_sysconfdir}/sysconfig/ebtables-config
%ghost %{_sysconfdir}/sysconfig/ebtables
%{_unitdir}/{arp,eb,ip,ip6}tables.service
%dir %{legacy_actions}/ip{,6}tables
%{legacy_actions}/ip{,6}tables/{save,panic}
%{_libexecdir}/{arp,eb}tables-helper

%files utils
%license COPYING
%{_sbindir}/nfnl_osf
%{_sbindir}/nfbpf_compile
%{_sbindir}/ip{,6}tables-apply
%dir %{_datadir}/xtables
%{_datadir}/xtables/pf.os
%{_mandir}/man8/nfnl_osf*
%{_mandir}/man8/nfbpf_compile*
%{_mandir}/man8/ip{,6}tables-apply*

%files nft
%{_sbindir}/ip{,6}tables-nft*
%{_sbindir}/ip{,6}tables{,-restore}-translate
%{_sbindir}/{eb,arp}tables-nft*
%{_sbindir}/xtables-nft-multi
%{_sbindir}/xtables-monitor
%{_sbindir}/ebtables-translate
%{_sbindir}/arptables-translate
%dir %{_libdir}/xtables
%{_libdir}/xtables/lib{arp,eb}t*
%{_mandir}/man8/xtables-monitor*
%{_mandir}/man8/xtables-translate*
%{_mandir}/man8/*-nft*
%{_mandir}/man8/ip{,6}tables{,-restore}-translate*
%{_mandir}/man8/ebtables-translate*
%{_mandir}/man8/arptables-translate*
%ghost %attr(0755,root,root) %{_sbindir}/ip{,6}tables{,-save,-restore}
%ghost %attr(0755,root,root) %{_sbindir}/{eb,arp}tables{,-save,-restore}
%ghost %{_mandir}/man8/arptables{,-save,-restore}.8.gz
%ghost %{_mandir}/man8/ebtables.8.gz


%changelog
* Tue Oct 28 2025 Paul Wouters <paul.wouters@aiven.io> - 1.8.11-12
- Pull in upstream fix for too strict command option parsing

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 20 2025 Phil Sutter <psutter@redhat.com> - 1.8.11-10
- Fix for ghost files not present in iptables-nft RPM

* Wed May 07 2025 Zbigniew Jedrzejewski-Szmek  <zbyszek@in.waw.pl> - 1.8.11-9
- Reapply the change to keep symlinks managed by alternatives under /usr/bin,
  this time with a scriptlet create symlinks if /usr/sbin is unmerged.

* Sat May 03 2025 Phil Sutter <psutter@redhat.com> - 1.8.11-8
- Revert last release, it breaks alternatives symlinks

* Fri Apr 25 2025 Zbigniew Jedrzejewski-Szmek  <zbyszek@in.waw.pl> - 1.8.11-7
- Keep symlinks managed by alternatives under /usr/bin

* Sun Apr 20 2025 Kevin Fenzi <kevin@scrye.com> - 1.8.11-6
- Add patch to fix -C handling ( fixes rhbz#2360423 )

* Thu Apr 03 2025 Phil Sutter <psutter@redhat.com> - 1.8.11-5
- iptables-services to assimilate arptables- and ebtables-services

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8.11-3
- Keep symlinks managed by alternatives under /usr/sbin

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8.11-2
- Rebuilt for the bin-sbin merge (2nd attempt)

* Fri Nov 08 2024 Phil Sutter <psutter@redhat.com> - 1.8.11-1
- new version

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 13 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8.10-14
- Add unmerged-sbin compat also for -legacy subpackage

* Fri Jul 12 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8.10-13
- Bump release and add changelog entry

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8.10-12
- Rebuilt for the bin-sbin merge

* Fri Jul 05 2024 Phil Sutter <psutter@redhat.com> - 1.8.10-11
- Add missing build dependency

* Fri Jul 05 2024 Phil Sutter <psutter@redhat.com> - 1.8.10-10
- Verify tarball GPG signature

* Wed Jul 03 2024 Phil Sutter <psutter@redhat.com> - 1.8.10-9
- Backport fixes from upstream

* Tue May 21 2024 Phil Sutter <psutter@redhat.com> - 1.8.10-8
- Make iptables-legacy own %%{_datadir}/xtables

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Phil Sutter <psutter@redhat.com> - 1.8.10-5
- Backport fixes from upstream
- Fix flatpak build

* Tue Nov 07 2023 Phil Sutter <psutter@redhat.com> - 1.8.10-4
- The actual obsoletes fix

* Tue Nov 07 2023 Phil Sutter <psutter@redhat.com> - 1.8.10-3
- Fix compat sub-package obsoletion

* Tue Oct 10 2023 Phil Sutter <psutter@redhat.com> - 1.8.10-2
- Obsolete dropped compat package

* Tue Oct 10 2023 Phil Sutter <psutter@redhat.com> - 1.8.10-1
- New version 1.8.10
- Drop compat sub-package

* Tue Aug 15 2023 Phil Sutter <psutter@redhat.com> - 1.8.9-6
- Convert license to SPDX format

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 24 2023 Phil Sutter <psutter@redhat.com> - 1.8.9-4
- Backport fixes from upstream

* Thu Apr 20 2023 Phil Sutter <psutter@redhat.com> - 1.8.9-3
- Support %%_excludedocs macro in alternatives installation

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Phil Sutter <psutter@redhat.com> - 1.8.9-1
- Make iptables-xml a relative symlink
- Drop not needed xtables.conf
- Ship iptables.xslt with iptables-legacy package
- Ship ebtables-translate tool with iptables-nft package
- Update to 1.8.9.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.8-2
- iptables-services requires iptables-apply in utils to apply rules

* Fri May 13 2022 Phil Sutter <psutter@redhat.com> - 1.8.8-1
- Update to 1.8.8. Fixes rhbz#2085503

* Thu Mar 03 2022 Phil Sutter <psutter@redhat.com> - 1.8.7-16
- Improve error messages for unsupported extensions
- xshared: Fix response to unprivileged users
- libxtables: Register only the highest revision extension
- Ignore typical 'fedpkg local' results in .gitignore

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 27 2021 Kevin Fenzi <kevin@scrye.com> - 1.8.7-14
- Rebuild for new libnftnl.

* Thu Aug 05 2021 Phil Sutter <psutter@redhat.com> - 1.8.7-13
- doc: ebtables-nft.8: Adjust for missing atomic-options
- nft: Fix for non-verbose check command
- Build services sub-package as noarch

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 01 2021 Phil Sutter <psutter@redhat.com> - 1.8.7-11
- Fix performance restoring large rulesets
- Review unit file

* Wed Jun 16 2021 Phil Sutter <psutter@redhat.com> - 1.8.7-10
- Backport fixes from upstream

* Wed Jun 16 2021 Phil Sutter <psutter@redhat.com> - 1.8.7-9
- Remove bashisms from arptables-nft-helper

* Fri May 07 2021 Phil Sutter <psutter@redhat.com> - 1.8.7-8
- iptables.init: Fix functionality for iptables-nft
- iptables.init: Ignore sysctl files not suffixed '.conf'
- iptables.init: Drop unused NEW_MODUTILS check
- iptables.init: Drop some trailing whitespace

* Mon Mar 29 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 1.8.7-7
- Add missing readlink required for iptables-nft(post)

* Tue Mar 23 2021 Phil Sutter <psutter@redhat.com> - 1.8.7-6
- Restore alternatives configuration after upgrade
- Fix license location

* Tue Mar 23 2021 Phil Sutter <psutter@redhat.com> - 1.8.7-5
- Fix upgrade path with package rename
- Add missing dependencies to iptables-nft package

* Tue Feb 16 2021 Phil Sutter <psutter@redhat.com> - 1.8.7-4
- Drop bootstrap code again
- Drop workarounds for F24 and lower
- Fix iptables-utils summary
- Ship iptables-apply with iptables-utils
- Reduce files sections by use of globbing
- Ship common man pages with iptables-libs
- Ship *-translate man pages with iptables-nft
- Move legacy iptables binaries, libraries and headers into sub-packages
- Introduce compat sub-package to help with above transitions
- Drop libipulog header from devel package, this belongs to libnetfilter_log
- Do not ship internal headers in devel package

* Thu Jan 28 2021 Phil Sutter <psutter@redhat.com> - 1.8.7-3
- ebtables: Exit gracefully on invalid table names

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Kevin Fenzi <kevin@scrye.com> - 1.8.7-1
- Update to 1.8.7. Fixes rhbz#1916948

* Thu Nov 19 17:32:24 CET 2020 Tom Stellard <tstellar@redhat.com> - 1.8.6-5
- Use make macros

* Tue Nov 17 14:05:30 CET 2020 Phil Sutter <psutter@redhat.com> - 1.8.6-4
- ebtables: Fix for broken chain renaming

* Mon Nov 16 13:39:22 CET 2020 Phil Sutter <psutter@redhat.com> - 1.8.6-3
- Drop obsolete StandardOutput setting from unit file
- Remove StandardError setting from unit file, its value is default

* Thu Nov  5 2020 Florian Weimer <fweimer@redhat.com> - 1.8.6-2
- Remove build dependency on autogen

* Sat Oct 31 2020 Kevin Fenzi <kevin@scrye.com> - 1.8.6-1
- Update to 1.8.6. Fixes bug #1893453

* Tue Aug 25 15:56:10 GMT 2020 Phil Sutter <psutter@redhat.com> - 1.8.5-3
- nft: cache: Check consistency with NFT_CL_FAKE, too
- nft: Fix command name in ip6tables error message

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Phil Sutter <psutter@redhat.com> - 1.8.5-1
- Rebase onto upstream version 1.8.5 plus two late fixes
- Drop explicit iptables-apply installation, upstream fixed that
- Ship ip6tables-apply along with iptables package

* Wed Feb 12 2020 Phil Sutter <psutter@redhat.com> - 1.8.4-7
- Move nft-specific extensions into iptables-nft package
- Move remaining extensions into iptables-libs package
- Make iptables-nft depend on iptables-libs instead of iptables
- Add upstream-suggested fixes

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Phil Sutter <psutter@redhat.com> - 1.8.4-5
- Raise Alternatives priority of nft variants to match legacy ones
- Add Provides lines to allow for iptables-nft as full legacy alternative

* Thu Dec 19 2019 Phil Sutter <psutter@redhat.com> - 1.8.4-4
- Drop leftover include in arptables-nft-helper

* Fri Dec 13 2019 Phil Sutter <psutter@redhat.com> - 1.8.4-3
- Remove dependencies on initscripts package

* Tue Dec 10 2019 Phil Sutter <psutter@redhat.com> - 1.8.4-2
- iptables-services requires /etc/init.d/functions

* Wed Dec 04 2019 Phil Sutter <psutter@redhat.com> - 1.8.4-1
- New upstream version 1.8.4

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Björn Esser <besser82@fedoraproject.org> - 1.8.3-4
- Disable bootstrapping

* Tue Jun 25 2019 Phil Sutter <psutter@redhat.com> - 1.8.3-3
- Change URL to point at iptables project, not netfilter overview page
- Reuse URL value in tarball source
- Reduce globbing of library file names to expose future SONAME changes
- Add bootstrapping for libip*tc SONAME bump

* Tue Jun 25 2019 Phil Sutter <psutter@redhat.com> - 1.8.3-2
- Install new man page for nfbpf_compile utility
- Move nfnl_osf man page to utils subpackage

* Wed May 29 2019 Phil Sutter <psutter@redhat.com> - 1.8.3-1
- New upstream version 1.8.3

* Mon Apr 15 2019 Phil Sutter <psutter@redhat.com> - 1.8.2-1
- New upstream version 1.8.2
- Integrate ebtables and arptables save/restore scripts with alternatives
- Add nft-specific ebtables and arptables man pages
- Move /etc/sysconfig/ip*tables-config files into services sub-package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Bogdan Dobrelya <bdobreli@redhat.com> - 1.8.0-4
- Use systemd_ordering macro

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Phil Sutter <psutter@redhat.com> - 1.8.0-2
- Fix calling ebtables-nft and arptables-nft via their new names.

* Mon Jul 09 2018 Phil Sutter <psutter@redhat.com> - 1.8.0-1
- New upstream version 1.8.0.
- Replace ldconfig calls with newly introduced macros.
- Rename compat subpackage to iptables-nft to clarify its purpose.
- Make use of Alternatives system.

* Fri May 04 2018 Phil Sutter <psutter@redhat.com> - 1.6.2-3
- Fix License: tag in spec-file
- Fix separation into compat subpackage

* Thu Mar 01 2018 Phil Sutter <psutter@redhat.com> - 1.6.2-2
- Kill module unloading support
- Support /etc/sysctl.d
- Don't restart services after package update
- Add support for --wait options to restore commands

* Wed Feb 21 2018 Michael Cronenworth <mike@cchtml.com> - 1.6.2-1
- New upstream version 1.6.2
  http://www.netfilter.org/projects/iptables/files/changes-iptables-1.6.2.txt

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 22 2017 Kevin Fenzi <kevin@scrye.com> - 1.6.1-5
- Rebuild for new libnftnl

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Thomas Woerner <twoerner@redhat.com> - 1.6.1-1
- New upstream version 1.6.1 with enhanced translation to nft support and
  several fixes (RHBZ#1417323)
  http://netfilter.org/projects/iptables/files/changes-iptables-1.6.1.txt
- Enable parallel build again

* Thu Feb 02 2017 Petr Šabata <contyk@redhat.com> - 1.6.0-4
- Disabling parallel build to avoid build issues with xtables
- See http://patchwork.alpinelinux.org/patch/1787/ for reference
- This should be fixed in 1.6.1; parallel build can be restored after the
  update

* Mon Dec 19 2016 Thomas Woerner <twoerner@redhat.com> - 1.6.0-3
- Dropped bad provides for iptables in services sub package (RHBZ#1327786)

* Fri Jul 22 2016 Thomas Woerner <twoerner@redhat.com> - 1.6.0-2
- /etc/ethertypes has been moved into the setup package for F-25+.
  (RHBZ#1329256)

* Wed Apr 13 2016 Thomas Woerner <twoerner@redhat.com> - 1.6.0-1
- New upstream version 1.6.0 with nft-compat support and lots of fixes (RHBZ#1292990)
  Upstream changelog:
  http://netfilter.org/projects/iptables/files/changes-iptables-1.6.0.txt
- New libs sub package containing libxtables and unstable libip*tc libraries (RHBZ#1323161)
- Using scripts form RHEL-7 (RHBZ#1240366)
- New compat sub package for nftables compatibility
- Install iptables-apply (RHBZ#912047)
- Fixed module uninstall (RHBZ#1324101)
- Incorporated changes by Petr Pisar
- Enabled bpf compiler (RHBZ#1170227) Thanks to Yanko Kaneti for the patch

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.21-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.21-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 01 2014 Jiri Popelka <jpopelka@redhat.com> - 1.4.21-14
- add dhcpv6-client to /etc/sysconfig/ip6tables (RHBZ#1169036)

* Mon Nov 03 2014 Jiri Popelka <jpopelka@redhat.com> - 1.4.21-13
- iptables.init: use /run/lock/subsys/ instead of /var/lock/subsys/ (RHBZ#1159573)

* Mon Sep 29 2014 Jiri Popelka <jpopelka@redhat.com> - 1.4.21-12
- ip[6]tables.init: change shebang from /bin/sh to /bin/bash (RHBZ#1147272)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.21-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 1.4.21-10
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.21-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 12 2014 Jiri Popelka <jpopelka@redhat.com> - 1.4.21-8
- add missing reload and panic actions
- BuildRequires: pkgconfig(x) instead of x-devel
- no need to specify file mode bits twice (in %%install and %%files)

* Sun Jan 19 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.4.21-7
- Don't order services after syslog.target.

* Wed Jan 15 2014 Thomas Woerner <twoerner@redhat.com> 1.4.21-6
- Enable connlabel support again, needs libnetfilter_conntrack

* Wed Jan 15 2014 Thomas Woerner <twoerner@redhat.com> 1.4.21-6
- fixed update from RHEL-6 to RHEL-7 (RHBZ#1043901)

* Tue Jan 14 2014 Jiri Popelka <jpopelka@redhat.com> - 1.4.21-5
- chmod /etc/sysconfig/ip[6]tables 755 -> 600

* Fri Jan 10 2014 Jiri Popelka <jpopelka@redhat.com> - 1.4.21-4
- drop virtual provide for xtables.so.9
- add default /etc/sysconfig/ip[6]tables (RHBZ#1034494)

* Thu Jan 09 2014 Jiri Popelka <jpopelka@redhat.com> - 1.4.21-3
- no need to support the pre-systemd things
- use systemd macros (#850166)
- remove scriptlets for migrating to a systemd unit from a SysV initscripts
- ./configure -> %%configure
- spec clean up
- fix self-obsoletion

* Thu Jan  9 2014 Thomas Woerner <twoerner@redhat.com> 1.4.21-2
- fixed system hang at shutdown if root device is network based (RHBZ#1007934)
  Thanks to Rodrigo A B Freire for the patch

* Thu Jan  9 2014 Thomas Woerner <twoerner@redhat.com> 1.4.21-1
- no connlabel.conf upstream anymore
- new version 1.4.21
  - doc: clarify DEBUG usage macro
  - iptables: use autoconf to process .in man pages
  - extensions: libipt_ULOG: man page should mention NFLOG as replacement
  - extensions: libxt_connlabel: use libnetfilter_conntrack
  - Introduce a new revision for the set match with the counters support
  - libxt_CT: Add the "NOTRACK" alias
  - libip6t_mh: Correct command to list named mh types in manpage
  - extensions: libxt_DNAT, libxt_REDIRECT, libxt_NETMAP, libxt_SNAT, libxt_MASQUERADE, libxt_LOG: rename IPv4 manpage and tell about IPv6 support
  - extensions: libxt_LED: fix parsing of delay
  - ip{6}tables-restore: fix breakage due to new locking approach
  - libxt_recent: restore minimum value for --seconds
  - iptables-xml: fix parameter parsing (similar to 2165f38)
  - extensions: add copyright statements
  - xtables: improve get_modprobe handling
  - ip[6]tables: Add locking to prevent concurrent instances
  - iptables: Fix connlabel.conf install location
  - ip6tables: don't print out /128
  - libip6t_LOG: target output is different to libipt_LOG
  - build: additional include path required after UAPI changes
  - iptables: iptables-xml: Fix various parsing bugs
  - libxt_recent: restore reap functionality to recent module
  - build: fail in configure on missing dependency with --enable-bpf-compiler
  - extensions: libxt_NFQUEUE: add --queue-cpu-fanout parameter
  - extensions: libxt_set, libxt_SET: check the set family too
  - ip6tables: Use consistent exit code for EAGAIN
  - iptables: libxt_hashlimit.man: correct address
  - iptables: libxt_conntrack.man extraneous commas
  - iptables: libip(6)t_REJECT.man default icmp types
  - iptables: iptables-xm1.1 correct man section
  - iptables: libxt_recent.{c,man} dead URL
  - iptables: libxt_string.man add examples
  - extensions: libxt_LOG: use generic syslog reference in manpage
  - iptables: extensions/GNUMakefile.in use CPPFLAGS
  - iptables: correctly reference generated file
  - ip[6]tables: fix incorrect alignment in commands_v_options
  - build: add software version to manpage first line at configure stage
  - extensions: libxt_cluster: add note on arptables-jf
  - utils: nfsynproxy: fix error while compiling the BPF filter
  - extensions: add SYNPROXY extension
  - utils: add nfsynproxy tool
  - iptables: state match incompatibilty across versions
  - libxtables: xtables_ipmask_to_numeric incorrect with non-CIDR masks
  - iptables: improve chain name validation
  - iptables: spurious error in load_extension
  - xtables: trivial spelling fix

* Sun Dec 22 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.4.19.1-2
- Drop INSTALL from docs, escape macros in %%changelog.

* Wed Jul 31 2013 Thomas Woerner <twoerner@redhat.com> 1.4.19.1-1
- new version 1.4.19.1
  - libxt_NFQUEUE: fix bypass option documentation
  - extensions: add connlabel match
  - extensions: add connlabel match
  - ip[6]tables: show --protocol instead of --proto in usage
  - libxt_recent: Fix missing space in manpage for --mask option
  - extensions: libxt_multiport: Update manpage to list valid protocols
  - utils: nfnl_osf: use the right nfnetlink lib
  - libip6t_NETMAP: Use xtables_ip6mask_to_cidr and get rid of libip6tc dependency
  - Revert "build: resolve link failure for ip6t_NETMAP"
  - libxt_osf: fix missing --ttl and --log in save output
  - libxt_osf: fix bad location for location in --genre
  - libip6t_SNPT: add manpage
  - libip6t_DNPT: add manpage
  - utils: updates .gitignore to include nfbpf_compile
  - extensions: libxt_bpf: clarify --bytecode argument
  - libxtables: fix parsing of dotted network mask format
  - build: bump version to 1.4.19
  - libxt_conntrack: fix state match alias state parsing
  - extensions: add libxt_bpf extension
  - utils: nfbpf_compile
  - doc: mention SNAT in INPUT chain since kernel 2.6.36
- fixed changelog date weekdays where needed

* Mon Mar  4 2013 Thomas Woerner <twoerner@redhat.com> 1.4.18-1
- new version 1.4.18 
  - lots of documentation changes
  - Introduce match/target aliases
  - Add the "state" alias to the "conntrack" match
  - iptables: remove unused leftover definitions
  - libxtables: add xtables_rule_matches_free
  - libxtables: add xtables_print_num
  - extensions: libip6t_DNPT: fix wording in DNPT target
  - extension: libip6t_DNAT: allow port DNAT without address
  - extensions: libip6t_DNAT: set IPv6 DNAT --to-destination
  - extensions: S/DNPT: add missing save function
- changes of 1.4.17:
  - libxt_time: add support to ignore day transition
  - Convert the NAT targets to use the kernel supplied nf_nat.h header
  - extensions: add IPv6 MASQUERADE extension
  - extensions: add IPv6 SNAT extension
  - extensions: add IPv6 DNAT target
  - extensions: add IPv6 REDIRECT extension
  - extensions: add IPv6 NETMAP extension
  - extensions: add NPT extension
  - extensions: libxt_statistic: Fix save output

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.16.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.4.16.2-6
- Own unowned -services libexec dirs (#894464, Michael Scherer).
- Fix -services unit file permissions (#732936, Michal Schmidt).

* Thu Nov  8 2012 Thomas Woerner <twoerner@redhat.com> 1.4.16.2-5
- fixed path of ip6tables.init in ip6tables.service

* Fri Nov  2 2012 Thomas Woerner <twoerner@redhat.com> 1.4.16.2-4
- fixed missing services for update of pre F-18 installations (rhbz#867960)
  - provide and obsolete old main package in services sub package
  - provide and obsolete old ipv6 sub package (pre F-17) in services sub package

* Sun Oct 14 2012 Dan Horák <dan[at]dany.cz> 1.4.16.2-3
- fix the compat provides for all 64-bit arches

* Fri Oct 12 2012 Thomas Woerner <twoerner@redhat.com> 1.4.16.2-2
- new sub package services providing the systemd services (RHBZ#862922)
- new sub package utils: provides nfnl_osf and the pf.os database
- using %%{_libexecdir}/iptables as script path for the original init scripts
- added service iptables save funcitonality using the new way provided by 
  initscripts 9.37.1 (RHBZ#748134)
- added virtual provide for libxtables.so.7

* Mon Oct  8 2012 Thomas Woerner <twoerner@redhat.com> 1.4.16.2-1
- new version 1.4.16.2
  - build: support for automake-1.12
  - build: separate AC variable replacements from xtables.h
  - build: have `make clean` remove dep files too
  - doc: grammatical updates to libxt_SET
  - doc: clean up interpunction in state list for xt_conntrack
  - doc: deduplicate extension descriptions into a new manpage
  - doc: trim "state" manpage and reference conntrack instead
  - doc: have NOTRACK manpage point to CT instead
  - doc: mention iptables-apply in the SEE ALSO sections
  - extensions: libxt_addrtype: fix type in help message
  - include: add missing linux/netfilter_ipv4/ip_queue.h
  - iptables: fix wrong error messages
  - iptables: support for match aliases
  - iptables: support for target aliases
  - iptables-restore: warn about -t in rule lines
  - ip[6]tables-restore: cleanup to reduce one level of indentation
  - libip6t_frag: match any frag id by default
  - libxtables: consolidate preference logic
  - libxt_devgroup: consolidate devgroup specification parsing
  - libxt_devgroup: guard against negative numbers
  - libxt_LED: guard against negative numbers
  - libxt_NOTRACK: replace as an alias to CT --notrack
  - libxt_state: replace as an alias to xt_conntrack
  - libxt_tcp: print space before, not after "flags:"
  - libxt_u32: do bounds checking for @'s operands
  - libxt_*limit: avoid division by zero
  - Merge branch 'master' of git://git.inai.de/iptables
  - Merge remote-tracking branch 'nf/stable'
  - New set match revision with --return-nomatch flag support
- dropped fixrestore patch, upstream

* Wed Aug  1 2012 Thomas Woerner <twoerner@redhat.com> 1.4.15-1
- new version 1.4.15
  - extensions: add HMARK target
  - iptables-restore: fix parameter parsing (shows up with gcc-4.7)
  - iptables-restore: move code to add_param_to_argv, cleanup (fix gcc-4.7)
  - libxtables: add xtables_ip[6]mask_to_cidr
  - libxt_devgroup: add man page snippet
  - libxt_hashlimit: add support for byte-based operation
  - libxt_recent: add --mask netmask
  - libxt_recent: remove unused variable
  - libxt_HMARK: correct a number of errors introduced by Pablo's rework
  - libxt_HMARK: fix ct case example
  - libxt_HMARK: fix output of iptables -L
  - Revert "iptables-restore: move code to add_param_to_argv, cleanup (fix gcc-4.7)"

* Wed Jul 18 2012 Thomas Woerner <twoerner@redhat.com> 1.4.14-3
- added fixrestore patch submitted to upstream by fryasu (nfbz#774) 
  (RHBZ#825796)

* Wed Jul 18 2012 Thomas Woerner <twoerner@redhat.com> 1.4.14-2
- disabled libipq, removed upstream, not provided by kernel anymore

* Wed Jul 18 2012 Thomas Woerner <twoerner@redhat.com> 1.4.14-1
- new version 1.4.14
  - extensions: add IPv6 capable ECN match extension
  - extensions: add nfacct match
  - extensions: add rpfilter module
  - extensions: libxt_rateest: output all options in save hook
  - iptables: missing free() in function cache_add_entry()
  - iptables: missing free() in function delete_entry()
  - libiptc: fix retry path in TC_INIT
  - libiptc: Returns the position the entry was inserted
  - libipt_ULOG: fix --ulog-cprange
  - libxt_CT: add --timeout option
  - ip(6)tables-restore: make sure argv is NULL terminated
  - Revert "libiptc: Returns the position the entry was inserted"
  - src: mark newly opened fds as FD_CLOEXEC (close on exec)
  - tests: add rateest match rules
- dropped patch5 (cloexec), merged upstream

* Mon Apr 23 2012 Thomas Woerner <twoerner@redhat.com> 1.4.12.2-5
- reenable iptables default services

* Wed Feb 29 2012 Harald Hoyer <harald@redhat.com> 1.4.12.2-4
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Thu Feb 16 2012 Thomas Woerner <twoerner@redhat.com> 1.4.12.2-3
- fixed auto enable check for Fedora > 16 and added rhel > 6 check

* Wed Feb 15 2012 Thomas Woerner <twoerner@redhat.com> 1.4.12.2-2
- disabled autostart and auto enable for iptables.service and ip6tables.service
  for Fedora > 16

* Mon Jan 16 2012 Thomas Woerner <twoerner@redhat.com> 1.4.12.2-1
- new version 1.4.12.2 with new pkgconfig/libip4tc.pc and pkgconfig/libip6tc.pc
  - build: make check stage not fail when building statically
  - build: restore build order of modules
  - build: scan for unreferenced symbols
  - build: sort file list before build
  - doc: clarification on the meaning of -p 0
  - doc: document iptables-restore's -T option
  - doc: fix undesired newline in ip6tables-restore(8)
  - ip6tables-restore: implement missing -T option
  - iptables: move kernel version find routing into libxtables
  - libiptc: provide separate pkgconfig files
  - libipt_SAME: set PROTO_RANDOM on all ranges
  - libxtables: Fix file descriptor leak in xtables_lmap_init on error
  - libxt_connbytes: fix handling of --connbytes FROM
  - libxt_CONNSECMARK: fix spacing in output
  - libxt_conntrack: improve error message on parsing violation
  - libxt_NFQUEUE: fix --queue-bypass ipt-save output
  - libxt_RATEEST: link with -lm
  - libxt_statistic: link with -lm
  - Merge branch 'stable'
  - Merge branch 'stable' of git://dev.medozas.de/iptables
  - nfnl_osf: add missing libnfnetlink_CFLAGS to compile process
  - xtoptions: fill in fallback value for nvals
  - xtoptions: simplify xtables_parse_interface

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Thomas Woerner <twoerner@redhat.com> 1.4.12.1-1
- new version 1.4.12.1 with new pkgconfig/libipq.pc
  - build: abort autogen on subcommand failure
  - build: strengthen check for overlong lladdr components
  - build: workaround broken linux-headers on RHEL-5
  - doc: clarify libxt_connlimit defaults
  - doc: fix typo in libxt_TRACE
  - extensions: use multi-target registration
  - libip6t_dst: restore setting IP6T_OPTS_LEN flag
  - libip6t_frag: restore inversion support
  - libip6t_hbh: restore setting IP6T_OPTS_LEN flag
  - libipq: add pkgconfig file
  - libipt_ttl: document that negation is available
  - libxt_conntrack: fix --ctproto 0 output
  - libxt_conntrack: remove one misleading comment
  - libxt_dccp: fix deprecated intrapositional ordering of !
  - libxt_dccp: fix random output of ! on --dccp-option
  - libxt_dccp: provide man pages options in short help too
  - libxt_dccp: restore missing XTOPT_INVERT tags for options
  - libxt_dccp: spell out option name on save
  - libxt_dscp: restore inversion support
  - libxt_hashlimit: default htable-expire must be in milliseconds
  - libxt_hashlimit: observe new default gc-expire time when saving
  - libxt_hashlimit: remove inversion from hashlimit rev 0
  - libxt_owner: restore inversion support
  - libxt_physdev: restore inversion support
  - libxt_policy: remove superfluous inversion
  - libxt_set: put differing variable names in directly
  - libxt_set: update man page about kernel support on the feature
  - libxt_string: define _GNU_SOURCE for strnlen
  - libxt_string: escape the escaping char too
  - libxt_string: fix space around arguments
  - libxt_string: replace hex codes by char equivalents
  - libxt_string: simplify hex output routine
  - libxt_tcp: always print the mask parts
  - libxt_TCPMSS: restore build with IPv6-less libcs
  - libxt_TOS: update linux kernel version list for backported fix
  - libxt_u32: fix missing allowance for inversion
  - src: remove unused IPTABLES_MULTI define
  - tests: add negation tests for libxt_statistic
  - xtoptions: flag use of XTOPT_POINTER without XTOPT_PUT
- removed include/linux/types.h before build to be able to compile

* Tue Jul 26 2011 Thomas Woerner <twoerner@redhat.com> 1.4.12-2
- dropped temporary provide again

* Tue Jul 26 2011 Thomas Woerner <twoerner@redhat.com> 1.4.12-1.1
- added temporary provides for libxtables.so.6 to be able to rebuild iproute,
  which is part of the standard build environment

* Mon Jul 25 2011 Thomas Woerner <twoerner@redhat.com> 1.4.12-1
- new version 1.4.12 with support of all new features of kernel 3.0
  - build: attempt to fix building under Linux 2.4
  - build: bump soversion for recent data structure change
  - build: install modules in arch-dependent location
  - doc: fix group range in libxt_NFLOG's man
  - doc: fix version string in ip6tables.8
  - doc: include matches/targets in manpage again
  - doc: mention multiple verbosity flags
  - doc: the -m option cannot be inverted
  - extensions: support for per-extension instance global variable space
  - iptables-apply: select default rule file depending on call name
  - iptables: consolidate target/match init call
  - iptables: Coverity: DEADCODE
  - iptables: Coverity: NEGATIVE_RETURNS
  - iptables: Coverity: RESOURCE_LEAK
  - iptables: Coverity: REVERSE_INULL
  - iptables: Coverity: VARARGS
  - iptables: restore negation for -f
  - libip6t_HL: fix option names from ttl -> hl
  - libipt_LOG: fix ignoring all but last flags
  - libxtables: ignore whitespace in the multiaddress argument parser
  - libxtables: properly reject empty hostnames
  - libxtables: set clone's initial data to NULL
  - libxt_conntrack: move more data into the xt_option_entry
  - libxt_conntrack: restore network-byte order for v1,v2
  - libxt_hashlimit: use a more obvious expiry value by default
  - libxt_rateest: abolish global variables
  - libxt_RATEEST: abolish global variables
  - libxt_RATEEST: fix userspacesize field
  - libxt_RATEEST: use guided option parser
  - libxt_state: fix regression about inversion of main option
  - option: remove last traces of intrapositional negation
- complete changelog:
  http://www.netfilter.org/projects/iptables/files/changes-iptables-1.4.12.txt

* Thu Jul 21 2011 Thomas Woerner <twoerner@redhat.com> 1.4.11.1-4
- merged ipv6 sub package into main package
- renamed init scripts to /usr/libexec/ip*tables.init

* Fri Jul 15 2011 Thomas Woerner <twoerner@redhat.com> 1.4.11.1-3
- added support for native systemd file (rhbz#694738)
  - new iptables.service file
  - additional requires
  - moved sysv init scripts to /usr/libexec
  - added new post, preun and postun scripts and triggers

* Tue Jul 12 2011 Thomas Woerner <twoerner@redhat.com> 1.4.11.1-2
- dropped temporary provide again
- enabled smp build

* Tue Jul 12 2011 Thomas Woerner <twoerner@redhat.com> 1.4.11.1-1.1
-  added temporary provides for libxtables.so.5 to be able to rebuild iproute,
   which is part of the standard build environment

* Mon Jul 11 2011 Thomas Woerner <twoerner@redhat.com> 1.4.11.1-1
- new version 1.4.11.1, bug and doc fix release for 1.4.11

* Tue Jun  7 2011 Thomas Woerner <twoerner@redhat.com> 1.4.11-1
- new version 1.4.11 with all new features of 2.6.37-39 (not usable)
  - lots of changes and bugfixes for base and extensions
  - complete changelog:
    http://www.netfilter.org/projects/iptables/files/changes-iptables-1.4.11.txt

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Thomas Woerner <twoerner@redhat.com> 1.4.10-1
- new version 1.4.10 with all new features of 2.6.36
  - all: consistent syntax use in struct option
  - build: fix static linking
  - doc: let man(1) autoalign the text in xt_cpu
  - doc: remove extra empty line from xt_cpu
  - doc: minimal spelling updates to xt_cpu
  - doc: consistent use of markup
  - extensions: libxt_quota: don't ignore the quota value on deletion
  - extensions: REDIRECT: add random help
  - extensions: add xt_cpu match
  - extensions: add idletimer xt target extension
  - extensions: libxt_IDLETIMER: use xtables_param_act when checking options
  - extensions: libxt_CHECKSUM extension
  - extensions: libipt_LOG/libip6t_LOG: support macdecode option
  - extensions: fix compilation of the new CHECKSUM target
  - extensions: libxt_ipvs: user-space lib for netfilter matcher xt_ipvs
  - iptables-xml: resolve compiler warnings
  - iptables: limit chain name length to be consistent with targets
  - libiptc: add Libs.private to pkgconfig files
  - libiptc: build with -Wl,--no-as-needed
  - xtables: remove unnecessary cast
- dropped xt_CHECKSUM, added upstream

* Tue Oct 12 2010 Thomas Woerner <twoerner@redhat.com> 1.4.9-2
- added xt_CHECKSUM patch from Michael S. Tsirkin (rhbz#612587)

* Wed Aug  4 2010 Thomas Woerner <twoerner@redhat.com> 1.4.9-1
- new version 1.4.9 with all new features of 2.6.35
  - doc: xt_hashlimit: fix a typo
  - doc: xt_LED: nroff formatting requirements
  - doc: xt_string: correct copy-and-pasting in manpage
  - extensions: add the LED target
  - extensions: libxt_quota.c: Support option negation
  - extensions: libxt_rateest: fix bps options for iptables-save
  - extensions: libxt_rateest: fix typo in the man page
  - extensions: REDIRECT: add random help
  - includes: sync header files from Linux 2.6.35-rc1
  - libxt_conntrack: do print netmask
  - libxt_hashlimit: always print burst value
  - libxt_set: new revision added
  - utils: add missing include flags to Makefile
  - xtables: another try at chain name length checking
  - xtables: remove xtables_set_revision function
  - xt_quota: also document negation
  - xt_sctp: Trace DATA chunk that supports SACK-IMMEDIATELY extension
  - xt_sctp: support FORWARD_TSN chunk type

* Fri Jul  2 2010 Thomas Woerner <twoerner@redhat.com> 1.4.8-1
- new version 1.4.8 all new features of 2.6.34 (rhbz#)
  - extensions: REDIRECT: fix --to-ports parser
  - iptables: add noreturn attribute to exit_tryhelp()
  - extensions: MASQUERADE: fix --to-ports parser
  - libxt_comment: avoid use of IPv4-specific examples
  - libxt_CT: add a manpage
  - iptables: correctly check for too-long chain/target/match names
  - doc: libxt_MARK: no longer restricted to mangle table
  - doc: remove claim that TCPMSS is limited to mangle
  - libxt_recent: add a missing space in output
  - doc: add manpage for libxt_osf
  - libxt_osf: import nfnl_osf program
  - extensions: add support for xt_TEE
  - CT: fix --ctevents parsing
  - extensions: add CT extension
  - libxt_CT: print conntrack zone in ->print/->save
  - xtables: fix compilation when debugging is enabled
  - libxt_conntrack: document --ctstate UNTRACKED
  - iprange: fix xt_iprange v0 parsing

* Wed Mar 24 2010 Thomas Woerner <twoerner@redhat.com> 1.4.7-2
- added default values for IPTABLES_STATUS_VERBOSE and
  IPTABLES_STATUS_LINENUMBERS in init script
- added missing lsb keywords Required-Start and Required-Stop to init script

* Fri Mar  5 2010 Thomas Woerner <twoerner@redhat.com> 1.4.7-1
- new version 1.4.7 with support for all new features of 2.6.33 (rhbz#570767)
  - libip4tc: Add static qualifier to dump_entry()
  - libipq: build as shared library
  - recent: reorder cases in code (cosmetic cleanup)
  - several man page and documentation fixes
  - policy: fix error message showing wrong option
  - includes: header updates
  - Lift restrictions on interface names
- fixed license and moved iptables-xml into base package according to review

* Wed Jan 27 2010 Thomas Woerner <twoerner@redhat.com> 1.4.6-2
- moved libip*tc and libxtables libs to /lib[64], added symlinks for .so libs
  to /usr/lib[64] for compatibility (rhbz#558796)

* Wed Jan 13 2010 Thomas Woerner <twoerner@redhat.com> 1.4.6-1
- new version 1.4.6 with support for all new features of 2.6.32
  - several man page fixes
  - Support for nommu arches
  - realm: remove static initializations
  - libiptc: remove unused functions
  - libiptc: avoid strict-aliasing warnings
  - iprange: do accept non-ranges for xt_iprange v1
  - iprange: warn on reverse range
  - iprange: roll address parsing into a loop
  - iprange: do accept non-ranges for xt_iprange v1 (log)
  - iprange: warn on reverse range (log)
  - libiptc: fix wrong maptype of base chain counters on restore
  - iptables: fix undersized deletion mask creation
  - style: reduce indent in xtables_check_inverse
  - libxtables: hand argv to xtables_check_inverse
  - iptables/extensions: make bundled options work again
  - CONNMARK: print mark rules with mask 0xffffffff as set instead of xset
  - iptables: take masks into consideration for replace command
  - doc: explain experienced --hitcount limit
  - doc: name resolution clarification
  - iptables: expose option to zero packet/byte counters for a specific rule
  - build: restore --disable-ipv6 functionality on system w/o v6 headers
  - MARK: print mark rules with mask 0xffffffff as --set-mark instead of --set-xmark
  - DNAT: fix incorrect check during parsing
  - extensions: add osf extension
  - conntrack: fix --expires parsing

* Thu Dec 17 2009 Thomas Woerner <twoerner@redhat.com> 1.4.5-2
- dropped nf_ext_init remains from cloexec patch

* Thu Sep 17 2009 Thomas Woerner <twoerner@redhat.com> 1.4.5-1
- new version 1.4.5 with support for all new features of 2.6.31
  - libxt_NFQUEUE: add new v1 version with queue-balance option
  - xt_conntrack: revision 2 for enlarged state_mask member
  - libxt_helper: fix invalid passed option to check_inverse
  - libiptc: split v4 and v6
  - extensions: collapse registration structures
  - iptables: allow for parse-less extensions
  - iptables: allow for help-less extensions
  - extensions: remove empty help and parse functions
  - xtables: add multi-registration functions
  - extensions: collapse data variables to use multi-reg calls
  - xtables: warn of missing version identifier in extensions
  - multi binary: allow subcommand via argv[1]
  - iptables: accept multiple IP address specifications for -s, -d
  - several build fixes
  - several man page fixes
- fixed two leaked file descriptors on sockets (rhbz#521397)

* Mon Aug 24 2009 Thomas Woerner <twoerner@redhat.com> 1.4.4-1
- new version 1.4.4 with support for all new features of 2.6.30
  - several man page fixes
  - iptables: replace open-coded sizeof by ARRAY_SIZE
  - libip6t_policy: remove redundant functions
  - policy: use direct xt_policy_info instead of ipt/ip6t
  - policy: merge ipv6 and ipv4 variant
  - extensions: add `cluster' match support
  - extensions: add const qualifiers in print/save functions
  - extensions: use NFPROTO_UNSPEC for .family field
  - extensions: remove redundant casts
  - iptables: close open file descriptors
  - fix segfault if incorrect protocol name is used
  - replace open-coded sizeof by ARRAY_SIZE
  - do not include v4-only modules in ip6tables manpage
  - use direct xt_policy_info instead of ipt/ip6t
  - xtables: fix segfault if incorrect protocol name is used
  - libxt_connlimit: initialize v6_mask
  - SNAT/DNAT: add support for persistent multi-range NAT mappings

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 15 2009 Thomas Woerner <twoerner@redhat.com> 1.4.3.2-1
- new version 1.4.3.2
- also install iptables/internal.h, needed for iptables.h and ip6tables.h

* Mon Mar 30 2009 Thomas Woerner <twoerner@redhat.com> 1.4.3.1-1
- new version 1.4.3.1
  - libiptc is now shared
  - supports all new features of the 2.6.29 kernel
- dropped typo_latter patch

* Thu Mar  5 2009 Thomas Woerner <twoerner@redhat.com> 1.4.2-3
- still more review fixes (rhbz#225906)
  - consistent macro usage
  - use sed instead of perl for rpath removal
  - use standard RPM CFLAGS, but also -fno-strict-aliasing (needed for libiptc*)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Thomas Woerner <twoerner@redhat.com> 1.4.2-1
- new version 1.4.2
- removed TOS value mask patch (upstream)
- more review fixes (rhbz#225906)
- install all header files (rhbz#462207)
- dropped nf_ext_init (rhbz#472548)

* Tue Jul 22 2008 Thomas Woerner <twoerner@redhat.com> 1.4.1.1-2
- fixed TOS value mask problem (rhbz#456244) (upstream patch)
- two more cloexec fixes

* Tue Jul  1 2008 Thomas Woerner <twoerner@redhat.com> 1.4.1.1-1
- upstream bug fix release 1.4.1.1
- dropped extra patch for 1.4.1 - not needed anymore

* Tue Jun 10 2008 Thomas Woerner <twoerner@redhat.com> 1.4.1-1
- new version 1.4.1 with new build environment
- additional ipv6 network mask patch from Jan Engelhardt
- spec file cleanup
- removed old patches

* Fri Jun  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.0-5
- use normal kernel headers, not linux/compiler.h
- change BuildRequires: kernel-devel to kernel-headers
- We need to do this to be able to build for both sparcv9 and sparc64 
  (there is no kernel-devel.sparcv9)

* Thu Mar 20 2008 Thomas Woerner <twoerner@redhat.com> 1.4.0-4
- use O_CLOEXEC for all opened files in all applications (rhbz#438189)

* Mon Mar  3 2008 Thomas Woerner <twoerner@redhat.com> 1.4.0-3
- use the kernel headers from the build tree for iptables for now to be able to 
  compile this package, but this makes the package more kernel dependant
- use s6_addr32 instead of in6_u.u6_addr32

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.0-2
- Autorebuild for GCC 4.3

* Mon Feb 11 2008 Thomas Woerner <twoerner@redhat.com> 1.4.0-1
- new version 1.4.0
- fixed condrestart (rhbz#428148)
- report the module in rmmod_r if there is an error
- use nf_ext_init instead of my_init for extension constructors

* Mon Nov  5 2007 Thomas Woerner <twoerner@redhat.com> 1.3.8-6
- fixed leaked file descriptor before fork/exec (rhbz#312191)
- blacklisting is not working, use "install X /bin/(true|false)" test instead
- return private exit code 150 for disabled ipv6 support
- use script name for output messages

* Tue Oct 16 2007 Thomas Woerner <twoerner@redhat.com> 1.3.8-5
- fixed error code for stopping a already stopped firewall (rhbz#321751)
- moved blacklist test into start

* Wed Sep 26 2007 Thomas Woerner <twoerner@redhat.com> 1.3.8-4.1
- do not start ip6tables if ipv6 is blacklisted (rhbz#236888)
- use simpler fix for (rhbz#295611)
  Thanks to Linus Torvalds for the patch.

* Mon Sep 24 2007 Thomas Woerner <twoerner@redhat.com> 1.3.8-4
- fixed IPv6 reject type (rhbz#295181)
- fixed init script: start, stop and status
- support netfilter compiled into kernel in init script (rhbz#295611)
- dropped inversion for limit modules from man pages (rhbz#220780)
- fixed typo in ip6tables man page (rhbz#236185)

* Wed Sep 19 2007 Thomas Woerner <twoerner@redhat.com> 1.3.8-3
- do not depend on local_fs in lsb header - this delayes start after network
- fixed exit code for initscript usage

* Mon Sep 17 2007 Thomas Woerner <twoerner@redhat.com> 1.3.8-2.1
- do not use lock file for condrestart test

* Thu Aug 23 2007 Thomas Woerner <twoerner@redhat.com> 1.3.8-2
- fixed initscript for LSB conformance (rhbz#246953, rhbz#242459)
- provide iptc interface again, but unsupported (rhbz#216733)
- compile all extension, which are supported by the kernel-headers package
- review fixes (rhbz#225906)

* Tue Jul 31 2007 Thomas Woerner <twoerner@redhat.com>
- reverted ipv6 fix, because it disables the ipv6 at all (rhbz#236888)

* Fri Jul 13 2007 Steve Conklin <sconklin@redhat.com> - 1.3.8-1
- New version 1.3.8

* Mon Apr 23 2007 Jeremy Katz <katzj@redhat.com> - 1.3.7-2
- fix error when ipv6 support isn't loaded in the kernel (#236888)

* Wed Jan 10 2007 Thomas Woerner <twoerner@redhat.com> 1.3.7-1.1
- fixed installation of secmark modules

* Tue Jan  9 2007 Thomas Woerner <twoerner@redhat.com> 1.3.7-1
- new verison 1.3.7
- iptc is not a public interface and therefore not installed anymore
- dropped upstream secmark patch

* Tue Sep 19 2006 Thomas Woerner <twoerner@redhat.com> 1.3.5-2
- added secmark iptables patches (#201573)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.5-1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Thomas Woerner <twoerner@redhat.com> 1.3.5-1
- new version 1.3.5
- fixed init script to set policy for raw tables, too (#179094)

* Tue Jan 24 2006 Thomas Woerner <twoerner@redhat.com> 1.3.4-3
- added important iptables header files to devel package

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 25 2005 Thomas Woerner <twoerner@redhat.com> 1.3.4-2
- fix for plugin problem: link with "gcc -shared" instead of "ld -shared" and 
  replace "_init" with "__attribute((constructor)) my_init"

* Fri Nov 25 2005 Thomas Woerner <twoerner@redhat.com> 1.3.4-1.1
- rebuild due to unresolved symbols in shared libraries

* Fri Nov 18 2005 Thomas Woerner <twoerner@redhat.com> 1.3.4-1
- new version 1.3.4
- dropped free_opts patch (upstream fixed)
- made libipq PIC (#158623)
- additional configuration options for iptables startup script (#172929)
  Thanks to Jan Gruenwald for the patch
- spec file cleanup (dropped linux_header define and usage)

* Mon Jul 18 2005 Thomas Woerner <twoerner@redhat.com> 1.3.2-1
- new version 1.3.2 with additional patch for the misplaced free_opts call
  from Marcus Sundberg

* Wed May 11 2005 Thomas Woerner <twoerner@redhat.com> 1.3.1-1
- new version 1.3.1

* Fri Mar 18 2005 Thomas Woerner <twoerner@redhat.com> 1.3.0-2
- Remove unnecessary explicit kernel dep (#146142)
- Fixed out of bounds accesses (#131848): Thanks to Steve Grubb
  for the patch
- Adapted iptables-config to reference to modprobe.conf (#150143)
- Remove misleading message (#140154): Thanks to Ulrich Drepper
  for the patch

* Mon Feb 21 2005 Thomas Woerner <twoerner@redhat.com> 1.3.0-1
- new version 1.3.0

* Thu Nov 11 2004 Thomas Woerner <twoerner@redhat.com> 1.2.11-3.2
- fixed autoload problem in iptables and ip6tables (CAN-2004-0986)

* Fri Sep 17 2004 Thomas Woerner <twoerner@redhat.com> 1.2.11-3.1
- changed default behaviour for IPTABLES_STATUS_NUMERIC to "yes" (#129731)
- modified config file to match this change and un-commented variables with
  default values

* Thu Sep 16 2004 Thomas Woerner <twoerner@redhat.com> 1.2.11-3
- applied second part of cleanup patch from (#131848): thanks to Steve Grubb
  for the patch

* Wed Aug 25 2004 Thomas Woerner <twoerner@redhat.com> 1.2.11-2
- fixed free bug in iptables (#128322)

* Tue Jun 22 2004 Thomas Woerner <twoerner@redhat.com> 1.2.11-1
- new version 1.2.11

* Thu Jun 17 2004 Thomas Woerner <twoerner@redhat.com> 1.2.10-1
- new version 1.2.10

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Thomas Woerner <twoerner@redhat.com> 1.2.9-2.3
- fixed iptables-restore -c fault if there are no counters (#116421)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jan  25 2004 Dan Walsh <dwalsh@redhat.com> 1.2.9-1.2
- Close File descriptors to prevent SELinux error message

* Wed Jan  7 2004 Thomas Woerner <twoerner@redhat.com> 1.2.9-1.1
- rebuild

* Wed Dec 17 2003 Thomas Woerner <twoerner@redhat.com> 1.2.9-1
- vew version 1.2.9
- new config options in ipXtables-config:
  IPTABLES_MODULES_UNLOAD
- more documentation in ipXtables-config
- fix for netlink security issue in libipq (devel package)
- print fix for libipt_icmp (#109546)

* Thu Oct 23 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-13
- marked all messages in iptables init script for translation (#107462)
- enabled devel package (#105884, #106101)
- bumped build for fedora for libipt_recent.so (#106002)

* Tue Sep 23 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-12.1
- fixed lost udp port range in ip6tables-save (#104484)
- fixed non numeric multiport port output in ipXtables-savs

* Mon Sep 22 2003 Florian La Roche <Florian.LaRoche@redhat.de> 1.2.8-11
- do not link against -lnsl

* Wed Sep 17 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-10
- made variables in rmmod_r local

* Tue Jul 22 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-9
- fixed permission for init script

* Sat Jul 19 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-8
- fixed save when iptables file is missing and iptables-config permissions

* Tue Jul  8 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-7
- fixes for ip6tables: module unloading, setting policy only for existing 
  tables

* Thu Jul  3 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-6
- IPTABLES_SAVE_COUNTER defaults to no, now
- install config file in /etc/sysconfig
- exchange unload of ip_tables and ip_conntrack
- fixed start function

* Wed Jul  2 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-5
- new config option IPTABLES_SAVE_ON_RESTART
- init script: new status, save and restart
- fixes #44905, #65389, #80785, #82860, #91040, #91560 and #91374

* Mon Jun 30 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-4
- new config option IPTABLES_STATUS_NUMERIC
- cleared IPTABLES_MODULES in iptables-config

* Mon Jun 30 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-3
- new init scripts

* Sat Jun 28 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove check for very old kernel versions in init scripts
- sync up both init scripts and remove some further ugly things
- add some docu into rpm

* Thu Jun 26  2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-2
- rebuild

* Mon Jun 16 2003 Thomas Woerner <twoerner@redhat.com> 1.2.8-1
- update to 1.2.8

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Bill Nottingham <notting@redhat.com> 1.2.7a-1
- update to 1.2.7a
- add a plethora of bugfixes courtesy Michael Schwendt <mschewndt@yahoo.com>

* Fri Dec 13 2002 Elliot Lee <sopwith@redhat.com> 1.2.6a-3
- Fix multilib

* Wed Aug 07 2002 Karsten Hopp <karsten@redhat.de>
- fixed iptables and ip6tables initscript output, based on #70511
- check return status of all iptables calls, not just the last one
  in a 'for' loop.

* Mon Jul 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.6a-1
- 1.2.6a (bugfix release, #69747)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.5-3
- Add some fixes from CVS, fixing bug #60465

* Tue Feb 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.5-2
- Merge ip6tables improvements from Ian Prowell <iprowell@prowell.org>
  #59402
- Update URL (#59354)
- Use /sbin/chkconfig rather than chkconfig in %%postun script

* Fri Jan 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.5-1
- 1.2.5

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Nov  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.4-2
- Fix %%preun script

* Tue Oct 30 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.4-1
- Update to 1.2.4 (various fixes, including security fixes; among others:
  #42990, #50500, #53325, #54280)
- Fix init script (#31133)

* Mon Sep  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-1
- 1.2.3 (5 security fixes, some other fixes)
- Fix updating (#53032)

* Mon Aug 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-4
- Fix #50990
- Add some fixes from current CVS; should fix #52620

* Mon Jul 16 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-3
- Add some fixes from the current CVS tree; fixes #49154 and some IPv6
  issues

* Tue Jun 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-2
- Fix iptables-save reject-with (#45632), Patch from Michael Schwendt
  <mschwendt@yahoo.com>

* Tue May  8 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-1
- 1.2.2

* Wed Mar 21 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.2.1a, fixes #28412, #31136, #31460, #31133

* Thu Mar  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Yet another initscript fix (#30173)
- Fix the fixes; they fixed some issues but broke more important
  stuff :/ (#30176)

* Tue Feb 27 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up initscript (#27962)
- Add fixes from CVS to iptables-{restore,save}, fixing #28412

* Fri Feb 09 2001 Karsten Hopp <karsten@redhat.de>
- create /etc/sysconfig/iptables mode 600 (same problem as #24245)

* Mon Feb 05 2001 Karsten Hopp <karsten@redhat.de>
- fix bugzilla #25986 (initscript not marked as config file)
- fix bugzilla #25962 (iptables-restore)
- mv chkconfig --del from postun to preun

* Thu Feb  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Fix check for ipchains

* Mon Jan 29 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Some fixes to init scripts

* Wed Jan 24 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add some fixes from CVS, fixes among other things Bug #24732

* Wed Jan 17 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add missing man pages, fix up init script (Bug #17676)

* Mon Jan 15 2001 Bill Nottingham <notting@redhat.com>
- add init script

* Mon Jan 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.2
- fix up ipv6 split
- add init script
- Move the plugins from /usr/lib/iptables to /lib/iptables.
  This needs to work before /usr is mounted...
- Use -O1 on alpha (compiler bug)

* Sat Jan  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.2
- Add IPv6 support (in separate package)

* Thu Aug 17 2000 Bill Nottingham <notting@redhat.com>
- build everywhere

* Tue Jul 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.1

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Preston Brown <pbrown@redhat.com>
- move iptables to /sbin.
- excludearch alpha for now, not building there because of compiler bug(?)

* Fri Jun  9 2000 Bill Nottingham <notting@redhat.com>
- don't obsolete ipchains either
- update to 1.1.0

* Sun Jun  4 2000 Bill Nottingham <notting@redhat.com>
- remove explicit kernel requirement

* Tue May  2 2000 Bernhard Rosenkränzer <bero@redhat.com>
- initial package
