# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global frr_libdir %{_libexecdir}/frr

%global _hardened_build 1
%global selinuxtype targeted
%define _legacy_common_support 1

%bcond grpc %{undefined rhel}
%bcond selinux 1

Name:           frr
Version:        10.4.1
Release: 3%{?dist}
Summary:        Routing daemon
License:        GPL-2.0-or-later AND ISC AND LGPL-2.0-or-later AND BSD-2-Clause AND BSD-3-Clause AND (GPL-2.0-or-later  OR ISC) AND MIT
URL:            http://www.frrouting.org
Source0:        https://github.com/FRRouting/frr/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        %{name}-tmpfiles.conf
Source2:        %{name}-sysusers.conf
#Decentralized SELinux policy
Source3:        frr.fc
Source4:        frr.te
Source5:        frr.if

Source6:        remove-babeld-ldpd.sh

Patch0000:      0000-remove-babeld-and-ldpd.patch
Patch0002:      0002-enable-openssl.patch
Patch0003:      0003-disable-eigrp-crypto.patch
Patch0004:      0004-fips-mode.patch
Patch0005:      0005-remove-grpc-test.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
%if %{undefined fc40} && %{undefined fc41}
ExcludeArch:       %{ix86}
%endif

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison >= 2.7
BuildRequires:  c-ares-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  groff
%if %{with grpc}
BuildRequires:  grpc-devel
BuildRequires:  grpc-plugins
%endif
BuildRequires:  json-c-devel
BuildRequires:  libcap-devel
BuildRequires:  libtool
BuildRequires:  libxcrypt-devel
BuildRequires:  libyang-devel >= 2.1.128
BuildRequires:  make
BuildRequires:  ncurses
BuildRequires:  ncurses-devel
BuildRequires:  net-snmp-devel
BuildRequires:  pam-devel
BuildRequires:  patch
BuildRequires:  pcre2-devel
BuildRequires:  perl-XML-LibXML
BuildRequires:  perl-generators
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-sphinx
BuildRequires:  readline-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  texinfo
BuildRequires:  protobuf-c-devel

Requires:       ncurses
Requires:       net-snmp
Requires(post): hostname
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd

%if 0%{?with_selinux}
Requires: (%{name}-selinux = %{version}-%{release} if selinux-policy-%{selinuxtype})
%endif

Obsoletes:      quagga < 1.2.4-17
Provides:       routingdaemon = %{version}-%{release}

%description
FRRouting is free software that manages TCP/IP based routing protocols. It takes
a multi-server and multi-threaded approach to resolve the current complexity
of the Internet.

FRRouting supports BGP4, OSPFv2, OSPFv3, ISIS, RIP, RIPng, PIM, NHRP, PBR,
EIGRP and BFD.

FRRouting is a fork of Quagga.

%if 0%{?with_selinux}
%package selinux
Summary:  Selinux policy for FRR
BuildArch:  noarch
Requires:  selinux-policy-%{selinuxtype}
Requires(post):  selinux-policy-%{selinuxtype}
BuildRequires:  selinux-policy-devel
%{?selinux_requires}

%description selinux
SELinux policy modules for FRR package

%endif

%prep
%autosetup -S git
#Selinux
mkdir selinux
cp -p %{SOURCE3} %{SOURCE4} %{SOURCE5} selinux
# C++14 or later needed for abseil-cpp 20230125; string_view needs C++17:
sed -r -i 's/(AX_CXX_COMPILE_STDCXX\(\[)11(\])/\117\2/' configure.ac

%build
#hopefully just temporary due to rhbz#2327314
export LDFLAGS="%{build_ldflags} -Wl,-z,noseparate-code"
export CFLAGS="%{optflags} -DINET_NTOP_NO_OVERRIDE"
autoreconf -ivf

%configure \
    --sbindir=%{frr_libdir} \
    --sysconfdir=%{_sysconfdir} \
    --libdir=%{_libdir}/frr \
    --libexecdir=%{_libexecdir}/frr \
    --localstatedir=/var \
    --enable-multipath=64 \
    --enable-vtysh=yes \
    --disable-ospfclient \
    --disable-ospfapi \
    --enable-snmp=agentx \
    --enable-user=frr \
    --enable-group=frr \
    --enable-vty-group=frrvty \
    --enable-rtadv \
    --enable-static=no \
    --disable-ldpd \
    --disable-babeld \
    --with-moduledir=%{_libdir}/frr/modules \
    --with-yangmodelsdir=%{_datadir}/frr-yang/ \
    --with-crypto=openssl \
    --enable-fpm \
    --enable-pcre2posix \
    %{?with_grpc:--enable-grpc}

%make_build MAKEINFO="makeinfo --no-split" PYTHON=%{__python3}

# Build info documentation
%make_build -C doc info

#SELinux policy
%if 0%{?with_selinux}
make -C selinux -f %{_datadir}/selinux/devel/Makefile %{name}.pp
bzip2 -9 selinux/%{name}.pp
%endif

%install
mkdir -p %{buildroot}%{_sysconfdir}/{frr,rc.d/init.d,sysconfig,logrotate.d,pam.d,default} \
         %{buildroot}%{_localstatedir}/log/frr %{buildroot}%{_localstatedir}/lib/frr \
         %{buildroot}%{_infodir} %{buildroot}%{_unitdir}

mkdir -p -m 0755 %{buildroot}%{_libdir}/frr
mkdir -p %{buildroot}%{_tmpfilesdir}
mkdir -p %{buildroot}%{_sysusersdir}

%make_install

# Remove this file, as it is uninstalled and causes errors when building on RH9
rm -rf %{buildroot}%{_infodir}/dir

install -p -m 644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf
install -p -m 644 tools/etc/frr/daemons %{buildroot}%{_sysconfdir}/frr/daemons
install -p -m 644 tools/frr.service %{buildroot}%{_unitdir}/frr.service
install -p -m 755 tools/frrinit.sh %{buildroot}%{frr_libdir}/frr
install -p -m 755 tools/frrcommon.sh %{buildroot}%{frr_libdir}/frrcommon.sh
install -p -m 755 tools/watchfrr.sh %{buildroot}%{frr_libdir}/watchfrr.sh

install -p -m 644 redhat/frr.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/frr
install -p -m 644 redhat/frr.pam %{buildroot}%{_sysconfdir}/pam.d/frr
install -d -m 775 %{buildroot}/run/frr

%if 0%{?with_selinux}
install -D -m 644 selinux/%{name}.pp.bz2 \
  %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
install -D -m 644 selinux/%{name}.if %{buildroot}%{_datadir}/selinux/devel/include/distributed/%{name}.if
%endif

# Delete libtool archives
find %{buildroot} -type f -name "*.la" -delete -print

#Upstream does not maintain a stable API, these headers from -devel subpackage are no longer needed
rm %{buildroot}%{_libdir}/frr/*.so
rm -r %{buildroot}%{_includedir}/frr/


%post
%systemd_post frr.service

# Create dummy files if they don't exist so basic functions can be used.
if [ ! -e %{_sysconfdir}/frr/frr.conf ]; then
    echo "hostname `hostname`" > %{_sysconfdir}/frr/frr.conf
    chown frr:frr %{_sysconfdir}/frr/frr.conf
    chmod 640 %{_sysconfdir}/frr/frr.conf
fi

#still used by vtysh, this way no error is produced when using vtysh
if [ ! -e %{_sysconfdir}/frr/vtysh.conf ]; then
    touch %{_sysconfdir}/frr/vtysh.conf
    chmod 640 %{_sysconfdir}/frr/vtysh.conf
    chown frr:frrvty %{_sysconfdir}/frr/vtysh.conf
fi

%postun
%systemd_postun_with_restart frr.service

%preun
%systemd_preun frr.service

#SELinux
%if 0%{?with_selinux}
%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
%selinux_relabel_post -s %{selinuxtype}
#/var/tmp and /var/run need to be relabeled as well if FRR is running before upgrade
if [ $1 == 2 ]; then
    %{_sbindir}/restorecon -R /var/tmp/frr &> /dev/null || :
    %{_sbindir}/restorecon -R /var/run/frr &> /dev/null || :
fi

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{name}
    %selinux_relabel_post -s %{selinuxtype}
fi

%endif

%check
#this should be temporary, the grpc test is just badly designed
rm tests/lib/*grpc*
%make_build check PYTHON=%{__python3}

%files
%license COPYING
%doc doc/mpls
%dir %attr(750,frr,frr) %{_sysconfdir}/frr
%dir %attr(755,frr,frr) %{_localstatedir}/lib/frr
%dir %attr(755,frr,frr) %{_localstatedir}/log/frr
%dir %attr(755,frr,frr) /run/frr
%{_infodir}/*info*
%{_mandir}/man1/frr.1*
%{_mandir}/man1/vtysh.1*
%{_mandir}/man8/frr-*.8*
%{_mandir}/man8/mtracebis.8*
%dir %{frr_libdir}/
%{frr_libdir}/*
%{_bindir}/mtracebis
%{_bindir}/vtysh
%dir %{_libdir}/frr
%{_libdir}/frr/*.so.*
%dir %{_libdir}/frr/modules
%{_libdir}/frr/modules/*
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/logrotate.d/frr
%config(noreplace) %attr(644,frr,frr) %{_sysconfdir}/frr/daemons
%config(noreplace) %{_sysconfdir}/pam.d/frr
%{_unitdir}/*.service
%dir %{_datadir}/frr-yang
%{_datadir}/frr-yang/*.yang
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf

%if 0%{?with_selinux}
%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.*
%{_datadir}/selinux/devel/include/distributed/%{name}.if
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{name}
%endif

%changelog
* Mon Sep 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 10.4.1-2
- Rebuilt for abseil-cpp 20250814.0

* Mon Sep 01 2025 Michal Ruprich <mruprich@redhat.com> - 10.4.1-1
- New version 10.4.1

* Tue Jul 29 2025 Michal Ruprich <mruprich@redhat.com> - 10.4.0-2
- Improving the %post scriptlet in frr-selinux

* Mon Jul 28 2025 Michal Ruprich <mruprich@redhat.com> - 10.4.0-1
- New version 10.4.0

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Michal Ruprich <mruprich@redhat.com> - 10.3
- New version 10.3

* Tue Feb 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 10.2.1-5
- Rebuilt for abseil-cpp-20250127.0

* Thu Feb 13 2025 Alexey Kurov <nucleo@fedoraproject.org> - 10.2.1-4
- Removed unrecognized options enable-systemd and disable-exampledir
- Fixed sysconfdir option warning
- Added option for support of PCRE2
- Own local state file dir
- Minimum libyang version 2.1.128

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 10.2.1-3
- Drop call to %sysusers_create_compat

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 10.2.1-2
- Add explicit BR: libxcrypt-devel

* Thu Jan 30 2025 Michal Ruprich <mruprich@redhat.com> - 10.2.1-1
- New version 10.2.1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jan 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 10.2-3
- Drop i686 support (leaf package)

* Thu Dec 05 2024 Michal Ruprich <mruprich@redhat.com> - 10.2-2
- Resolves: rhbz#2329643 - upgrading frr to 10.2 causes pimd crashes

* Fri Nov 22 2024 Michal Ruprich <mruprich@redhat.com> - 10.2-1
- New version 10.2

* Tue Sep 10 2024 Michal Ruprich <mruprich@redhat.com> - 10.1-4
- Resolves: #2311119 - Multiple AVCs for accessing lib_t in FRR-10.1
- Resolves: #2311120 - AVCs for using a netlink socket in FRR

* Sun Aug 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 10.1-3
- Rebuilt for abseil-cpp-20240722.0

* Thu Aug 15 2024 Michal Ruprich <mruprich@redhat.com> - 10.1-2
- Rebuilding for the libre soname bump

* Mon Aug 12 2024 Michal Ruprich <mruprich@redhat.com> - 10.1-1
- New version 10.1

* Wed Jul 31 2024 Michal Ruprich <mruprich@redhat.com> - 10.0.1-1
- New version 10.0.1

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 17 2024 Michal Ruprich <mruprich@redhat.com> - 9.1-4
- Moving yang modules to frr specific dir to avoid conflicts
- Adding rpminspect.yaml

* Sat Feb 24 2024 Paul Wouters <paul.wouters@aiven.io> - 9.1-3
- Rebuild for libre2.so.11 bump

* Sun Feb 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 9.1-2
- Rebuilt for abseil-cpp-20240116.0

* Thu Jan 25 2024 Michal Ruprich <mruprich@redhat.com> - 9.1-1
- New version 9.1

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 16 2023 Michal Ruprich <mruprich@redhat.com> - 9.0.1-1
- New version 9.0.1

* Fri Sep 01 2023 Michal Ruprich <mruprich@redhat.com> - 8.5.2-4
- Adding a couple of SELinux rules, includes fix for rhbz#2149299

* Wed Aug 30 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 8.5.2-3
- Rebuilt for abseil-cpp 20230802.0

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Michal Ruprich <mruprich@redhat.com> - 8.5.2-1
- New version 8.5.2
- Fixing some rpmlint warnings

* Mon Jun 26 2023 Michal Ruprich <mruprich@redhat.com> - 8.5.1-4
- Resolves: #2216073 - SELinux is preventing FRR-Zebra to access to network namespaces.

* Mon Jun 05 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 8.5.1-3
- Disable grpc in RHEL builds

* Fri May 19 2023 Petr Pisar <ppisar@redhat.com> - 8.5.1-2
- Rebuild against rpm-4.19 (https://fedoraproject.org/wiki/Changes/RPM-4.19)

* Wed Apr 26 2023 Michal Ruprich <mruprich@redhat.com> - 8.5.1-1
- New version 8.5.1

* Wed Apr 12 2023 Michal Ruprich <mruprich@redhat.com> - 8.5-1
- New version 8.5

* Thu Mar 23 2023 Michal Ruprich <mruprich@redhat.com> - 8.4.2-5
- Rebuilding for new abseil-cpp version

* Wed Mar 22 2023 Michal Ruprich <mruprich@redhat.com> - 8.4.2-4
- SPDX migration

* Wed Mar 08 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 8.4.2-3
- Build as C++17, required by abseil-cpp 20230125

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Michal Ruprich <mruprich@redhat.com> - 8.4.2-1
- New version 8.4.2

* Fri Nov 25 2022 Michal Ruprich <mruprich@redhat.com> - 8.4.1-1
- New version 8.4.1
- Fix for rhbz #2140705

* Thu Nov 10 2022 Michal Ruprich <mruprich@redhat.com> - 8.4-1
- New version 8.4

* Fri Sep 16 2022 Michal Ruprich <mruprich@redhat.com> - 8.3.1-5
- Adding SELinux rule to enable zebra to write to sysctl_net_t
- Adding SELinux rule to enable bgpd to call name_connect to bgp_port_t

* Fri Sep 09 2022 Michal Ruprich <mruprich@redhat.com> - 8.3.1-4
- Fixing an error in post scriptlet

* Fri Sep 09 2022 Michal Ruprich <mruprich@redhat.com> - 8.3.1-3
- Resolves: #2124254 - frr can no longer update routes

* Wed Sep 07 2022 Michal Ruprich <mruprich@redhat.com> - 8.3.1-2
- Resolves: #2124253 - SELinux is preventing zebra from setattr access on the directory frr
- Better handling FRR files during upgrade

* Tue Sep 06 2022 Michal Ruprich <mruprich@redhat.com> - 8.3.1-1
- New version 8.3.1

* Mon Aug 22 2022 Michal Ruprich <mruprich@redhat.com> - 8.2.2-10
- Rebuilding for new abseil-cpp and grpc updates

* Wed Aug 10 2022 Michal Ruprich <mruprich@redhat.com> - 8.2.2-9
- Adding vrrpd and pathd as daemons to the policy

* Wed Aug 10 2022 Michal Ruprich <mruprich@redhat.com> - 8.2.2-8
- Finalizing SELinux policy

* Tue Aug 02 2022 Michal Ruprich <mruprich@redhat.com> - 8.2.2-7
- Fixing wrong path for vtysh in frr.fc

* Fri Jul 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 8.2.2-6
- Rebuild with abseil-cpp-20211102.0-4.fc37 (RHBZ#2108658)

* Wed Jul 27 2022 Michal Ruprich - 8.2.2-5
- Packaging SELinux policy for FRR

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 17 2022 Michal Ruprich <mruprich@redhat.com> - 8.2.2-3
- Rebuild for grpc-1.46.1

* Mon Apr 11 2022 Michal Ruprich <mruprich@redhat.com> - 8.2.2-2
- Fix for CVE-2022-16126

* Tue Mar 15 2022 Michal Ruprich <mruprich@redhat.com> - 8.2.2-1
- New version 8.2.2

* Thu Mar 10 2022 Michal Ruprich <mruprich@redhat.com> - 8.2-2
- Rebuild for abseil-cpp 20211102.0

* Wed Mar 09 2022 Michal Ruprich <mruprich@redhat.com> - 8.2-1
- New version 8.2 (rhbz#2020439)
- Resolves: #2011868 - systemctl frr reload does not stop daemons that are not enabled in /etc/frr/daemons

* Tue Feb 01 2022 Michal Ruprich <mruprich@redhat.com> - 8.0.1-11
- Rebuilding for FTBFS in Rawhide(rhbz#2045399)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 8.0.1-9
- Rebuilt for libre2.so.9

* Sat Nov 06 2021 Adrian Reber <adrian@lisas.de> - 8.0.1-8
- Rebuilt for protobuf 3.19.0

* Mon Oct 25 2021 Adrian Reber <adrian@lisas.de> - 8.0.1-7
- Rebuilt for protobuf 3.18.1

* Fri Oct 15 2021 Michal Ruprich <mruprich@redhat.com> - 8.0.1-6
- Obsoleting quagga so that it may be retired

* Thu Oct 07 2021 Michal Ruprich <mruprich@redhat.com> - 8.0.1-5
- Rebuilding for grpc 1.41

* Thu Sep 30 2021 Michal Ruprich <mruprich@redhat.com> - 8.0.1-4
- Rebuild for new version of libyang

* Sat Sep 18 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 8.0.1-3
- Rebuild for grpc 1.40

* Thu Sep 16 2021 Sahana Prasad <sahana@redhat.com> - 8.0.1-2
- Rebuilt with OpenSSL 3.0.0

* Thu Sep 16 2021 Michal Ruprich <mruprich@redhat.com> - 8.0.1-1
- New version 8.0.1

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 8.0-2
- Rebuilt with OpenSSL 3.0.0

* Wed Aug 11 2021 Michal Ruprich <mruprich@redhat.com> - 8.0-1
- New version 8.0

* Wed Aug 04 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 7.5.1-9
- Rebuild for grpc 1.39

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Michal Ruprich <mruprich@redhat.com> - 7.5.1-7
- Resolves: #1983278 - ospfd crashes in route_node_delete with assertion fail

* Sat Jul 10 2021 Björn Esser <besser82@fedoraproject.org> - 7.5.1-6
- Rebuild for versioned symbols in json-c

* Wed Jul 07 2021 Neal Gompa <ngompa@datto.com> - 7.5.1-5
- Clean up the spec file for legibility and modern spec standards
- Remove unneeded info scriptlets
- Use systemd-sysusers for frr user and frrvty group
- Use git-core instead of git for applying patches
- Drop redundant build dependencies

* Wed Jul 07 2021 Michal Ruprich <mruprich@redhat.com> - 7.5.1-4
- Rebuild for newer abseil-cpp

* Tue May 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 7.5.1-3
- Rebuild for grpc 1.37

* Fri Apr 23 2021 Michal Ruprich <mruprich@redhat.com> - 7.5.1-2
- Fixing permissions on config files in /etc/frr
- Enabling integrated configuration option for frr

* Fri Mar 12 2021 Michal Ruprich <mruprich@redhat.com> - 7.5.1-1
- New version 7.5.1
- Enabling grpc, adding hostname for post scriptlet
- Moving files to libexec due to selinux issues

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7.5-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Feb 16 2021 Michal Ruprich <mruprich@redhat.com> - 7.5-3
- Fixing FTBS - icc options are confusing the new gcc

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 01 2021 Michal Ruprich <mruprich@redhat.com> - 7.5-1
- New version 7.5

* Mon Sep 21 2020 Michal Ruprich <mruprich@redhat.com> - 7.4-1
- New version 7.4

* Thu Aug 27 2020 Josef Řídký <jridky@redhat.com> - 7.3.1-4
- Rebuilt for new net-snmp release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 18 2020 Michal Ruprich <mruprich@redhat.com> - 7.3.1-1
- New version 7.3.1
- Fixes a couple of bugs(#1832259, #1835039, #1830815, #1830808, #1830806, #1830800, #1830798, #1814773)

* Tue May 19 2020 Michal Ruprich <mruprich@redhat.com> - 7.3-6
- Removing texi2html, it is not available in Rawhide anymore

* Mon May 18 2020 Michal Ruprich <mruprich@redhat.com> - 7.3-5
- Rebuild for new version of libyang

* Tue Apr 21 2020 Björn Esser <besser82@fedoraproject.org> - 7.3-4
- Rebuild (json-c)

* Mon Apr 13 2020 Björn Esser <besser82@fedoraproject.org> - 7.3-3
- Update json-c-0.14 patch with a solution from upstream

* Mon Apr 13 2020 Björn Esser <besser82@fedoraproject.org> - 7.3-2
- Add support for upcoming json-c 0.14.0

* Wed Feb 19 2020 Michal Ruprich <mruprich@redhat.com> - 7.3-1
- New version 7.3

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 16 2019 Michal Ruprich <mruprich@redhat.com> - 7.2-1
- New version 7.2

* Tue Nov 12 2019 Michal Ruprich <mruprich@redhat.com> - 7.1-5
- Rebuilding for new version of libyang

* Mon Oct 07 2019 Michal Ruprich <mruprich@redhat.com> - 7.1-4
- Adding noreplace to the /etc/frr/daemons file

* Fri Sep 13 2019 Michal Ruprich <mruprich@redhat.com> - 7.1-3
- New way of finding python version during build
- Replacing crypto of all routing daemons with openssl
- Disabling EIGRP crypto because it is broken
- Disabling crypto in FIPS mode

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Michal Ruprich <mruprich@redhat.com> - 7.1-1
- New version 7.1

* Wed Jun 19 2019 Michal Ruprich <mruprich@redhat.com> - 7.0-2
- Initial build
