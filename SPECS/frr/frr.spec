%global frr_libdir %{_libexecdir}/frr

Summary:        Routing daemon
Name:           frr
Version:        8.5.3
Release:        4%{?dist}
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.frrouting.org
Source0:        https://github.com/FRRouting/frr/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        %{name}-tmpfiles.conf
Source2:        %{name}-sysusers.conf
Patch0:         0000-remove-babeld-and-ldpd.patch
Patch1:         0001-enable-openssl.patch
Patch2:         0002-disable-eigrp-crypto.patch
Patch3:         0003-fips-mode.patch
Patch4:         0004-remove-grpc-test.patch
Patch5:         CVE-2023-46752.patch
Patch6:         CVE-2023-46753.patch
Patch7:			CVE-2023-47235.patch
Patch8:			CVE-2023-47234.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  c-ares-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  groff
BuildRequires:  grpc-devel
BuildRequires:  grpc-plugins
BuildRequires:  json-c-devel
BuildRequires:  libcap-devel
BuildRequires:  libtool
BuildRequires:  libyang-devel
BuildRequires:  make
BuildRequires:  ncurses
BuildRequires:  ncurses-devel
BuildRequires:  net-snmp-devel
BuildRequires:  pam-devel
BuildRequires:  patch
BuildRequires:  perl-XML-LibXML
BuildRequires:  perl-generators
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  re2-devel
BuildRequires:  readline-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  texinfo
%if 0%{?with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif
Requires:       ncurses
Requires:       net-snmp
Requires(post): hostname
%{?sysusers_requires_compat}
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd
Provides:       routingdaemon = %{version}-%{release}

%description
FRRouting is free software that manages TCP/IP based routing protocols. It takes
a multi-server and multi-threaded approach to resolve the current complexity
of the Internet.

FRRouting supports BGP4, OSPFv2, OSPFv3, ISIS, RIP, RIPng, PIM, NHRP, PBR, EIGRP and BFD.

FRRouting is a fork of Quagga.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%build
autoreconf -ivf

%configure \
    --sbindir=%{frr_libdir} \
    --sysconfdir=%{_sysconfdir}/frr \
    --libdir=%{_libdir}/frr \
    --libexecdir=%{_libexecdir}/frr \
    --localstatedir=/run/frr \
    --enable-multipath=64 \
    --enable-vtysh=yes \
    --disable-ospfclient \
    --disable-ospfapi \
    --enable-snmp=agentx \
    --enable-user=frr \
    --enable-group=frr \
    --enable-vty-group=frrvty \
    --enable-rtadv \
    --disable-exampledir \
    --enable-systemd=yes \
    --enable-static=no \
    --disable-ldpd \
    --disable-babeld \
    --with-moduledir=%{_libdir}/frr/modules \
    --with-crypto=openssl \
    --enable-fpm \
    --enable-grpc

%make_build MAKEINFO="makeinfo --no-split" PYTHON=python3

# Build info documentation
%make_build -C doc info


%install
mkdir -p %{buildroot}%{_sysconfdir}/{frr,rc.d/init.d,sysconfig,logrotate.d,pam.d,default} \
         %{buildroot}%{_rundir}/frr/log/frr \
         %{buildroot}%{_infodir} \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_tmpfilesdir} \
         %{buildroot}%{_sysusersdir} \
         %{buildroot}%{frr_libdir}

mkdir -p -m 0755 %{buildroot}%{_libdir}/frr

%make_install

# Remove this file, this package should not own the top-level info dir file for the whole system
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

# Delete libtool archives
find %{buildroot} -type f -name "*.la" -delete -print

# Upstream does not maintain a stable API, these files from -devel subpackage are no longer needed
rm %{buildroot}%{_libdir}/frr/*.so
rm -r %{buildroot}%{_includedir}/frr/

%pre
%sysusers_create_package %{name} %{SOURCE2}

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

%check
%{python3} -m pip install atomicwrites attrs docutils pluggy pygments six more-itertools
#this should be temporary, the grpc test is just badly designed
rm tests/lib/*grpc*
%make_build check PYTHON=python3

%files
%license COPYING
%doc doc/mpls
%dir %attr(750,frr,frr) %{_sysconfdir}/frr
%dir %attr(755,frr,frr) %{_rundir}/frr/log/frr
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
%dir %{_datadir}/yang
%{_datadir}/yang/*.yang
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf

%changelog
* Tue Nov 14 2023 Sam Meluch <sammeluch@microsoft.com> - 8.5.3-4
- Patch CVE-2023-47234 and CVE-2023-47235

* Mon Nov 06 2023 Rachel Menge <rachelmenge@microsoft.com> - 8.5.3-3
- Patch CVE-2023-46752 and CVE-2023-46753

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 8.5.3-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Sep 07 2023 Brian Fjeldstad <bfjelds@microsoft.com> - 8.5.3-1
- Bump version to bring fixes for CVE-2023-41358 CVE-2023-41359 CVE-2023-41360

* Mon May 22 2023 Suresh Thelkar <sthelkar@microsoft.com> - 8.5.1-2
- Fix for CVE-2023-31490

* Thu May 04 2023 Olivia Crain <oliviacrain@microsoft.com> - 8.5.1-1
- Clean up spec and promote to core specs
- Renumber patches
- Remove unused selinux subpackage
- Use SPDX license expression in license tag

* Wed May 3 2023 Samuel Mueller <samuelle@microsoft.com> - 8.4.2-3
- Correct unavailable sysusers_create_compat macro to available sysusers_create_package macro

* Mon Jan 30 2023 Sumedh Sharma <sumsharma@microsoft.com> - 8.4.2-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Disable sub-package selinux for selinux type targeted
- License verified

* Thu Jan 12 2023 Michal Ruprich <mruprich@redhat.com> - 8.4.2-1
- New version 8.4.2

* Fri Nov 25 2022 Michal Ruprich <mruprich@redhat.com> - 8.4.1-1
- New version 8.4.1
- Fix for rhbz #2140705

* Thu Nov 10 2022 Michal Ruprich <mruprich@redhat.com> - 8.4-1
- New version 8.4

* Thu Sep 22 2022 Michal Ruprich <mruprich@redhat.com> - 8.3.1-6
- Rebuilding because of weird abseil-cpp version mismatch in the compose (rhbz #2128691)

* Fri Sep 16 2022 Michal Ruprich <mruprich@redhat.com> - 8.3.1-5
- Adding SELinux rule to enable zebra to write to sysctl_net_t
- Adding SELinux rule to enable bgpd to call name_connect to bgp_port_t

* Fri Sep 09 2022 Michal Ruprich <mruprich@redhat.com> - 8.3.1-4
- Adding a couple of rules to tackle AVCs

* Fri Sep 09 2022 Michal Ruprich <mruprich@redhat.com> - 8.3.1-3
- Resolves: #2124254 - frr can no longer update routes

* Wed Sep 07 2022 Michal Ruprich <mruprich@redhat.com> - 8.3.1-2
- Resolves: #2124253 - SELinux is preventing zebra from setattr access on the directory frr
- Better handling FRR files during upgrade

* Tue Sep 06 2022 Michal Ruprich <mruprich@redhat.com> - 8.3.1-1
- New version 8.3.1

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
