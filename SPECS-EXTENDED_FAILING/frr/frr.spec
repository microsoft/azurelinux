Vendor:         Microsoft Corporation
Distribution:   Mariner
%global frrversion	7.4
%global frr_libdir /usr/lib/frr

%global _hardened_build 1
%define _legacy_common_support 1

%bcond_with tex_docs

Name: frr
Version: 7.4
Release: 4%{?dist}
Summary: Routing daemon
License: GPLv2+
URL: http://www.frrouting.org
Source0: https://github.com/FRRouting/frr/releases/download/%{name}-%{frrversion}/%{name}-%{frrversion}.tar.gz
Source1: %{name}-tmpfiles.conf
BuildRequires: perl-generators
BuildRequires: gcc
BuildRequires: net-snmp-devel
BuildRequires: texinfo libcap-devel autoconf automake libtool patch groff
BuildRequires: readline readline-devel ncurses ncurses-devel
BuildRequires: git pam-devel c-ares-devel
BuildRequires: json-c-devel bison >= 2.7 flex perl-XML-LibXML
BuildRequires: python3-devel python3-sphinx python3-pytest
BuildRequires: systemd systemd-devel
BuildRequires: libyang-devel >= 0.16.74
%if %{with tex_docs}
BuildRequires: texi2html
%endif
Requires: net-snmp ncurses
Requires(post): systemd /usr/bin/install-info
Requires(preun): systemd /usr/bin/install-info
Requires(postun): systemd
Provides: routingdaemon = %{version}-%{release}
Conflicts: quagga

Patch0000: 0000-remove-babeld-and-ldpd.patch
Patch0001: 0001-use-python3.patch
Patch0002: 0002-enable-openssl.patch
Patch0003: 0003-disable-eigrp-crypto.patch
Patch0004: 0004-fips-mode.patch
Patch0006: 0006-python-version.patch

%description
FRRouting is free software that manages TCP/IP based routing protocols. It takes
a multi-server and multi-threaded approach to resolve the current complexity
of the Internet.

FRRouting supports BGP4, OSPFv2, OSPFv3, ISIS, RIP, RIPng, PIM, NHRP, PBR, EIGRP and BFD.

FRRouting is a fork of Quagga.

%prep
%autosetup -S git

%build
autoreconf -ivf

%configure \
    --sbindir=%{frr_libdir} \
    --sysconfdir=%{_sysconfdir}/frr \
    --libdir=%{_libdir}/frr \
    --libexecdir=%{_libexecdir}/frr \
    --localstatedir=%{_localstatedir}/run/frr \
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
    --enable-fpm

%make_build MAKEINFO="makeinfo --no-split" PYTHON=%{__python3}

pushd doc
make info
popd

%install
mkdir -p %{buildroot}/etc/{frr,rc.d/init.d,sysconfig,logrotate.d,pam.d,default} \
         %{buildroot}/var/log/frr %{buildroot}%{_infodir} \
         %{buildroot}%{_unitdir}

mkdir -p -m 0755 %{buildroot}%{_libdir}/frr
mkdir -p %{buildroot}%{_tmpfilesdir}

%make_install

# Remove this file, as it is uninstalled and causes errors when building on RH9
rm -rf %{buildroot}/usr/share/info/dir

install -p -m 644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -p -m 644 %{_builddir}/%{name}-%{frrversion}/tools/etc/frr/daemons %{buildroot}/etc/frr/daemons
install -p -m 644 %{_builddir}/%{name}-%{frrversion}/tools/frr.service %{buildroot}%{_unitdir}/frr.service
install -p -m 755 %{_builddir}/%{name}-%{frrversion}/tools/frrinit.sh %{buildroot}%{frr_libdir}/frr
install -p -m 755 %{_builddir}/%{name}-%{frrversion}/tools/frrcommon.sh %{buildroot}%{frr_libdir}/frrcommon.sh
install -p -m 755 %{_builddir}/%{name}-%{frrversion}/tools/watchfrr.sh %{buildroot}%{frr_libdir}/watchfrr.sh

install -p -m 644 %{_builddir}/%{name}-%{frrversion}/redhat/frr.logrotate %{buildroot}/etc/logrotate.d/frr
install -p -m 644 %{_builddir}/%{name}-%{frrversion}/redhat/frr.pam %{buildroot}/etc/pam.d/frr
install -d -m 775 %{buildroot}/run/frr

rm %{buildroot}%{_libdir}/frr/*.la
rm %{buildroot}%{_libdir}/frr/modules/*.la

#Upstream does not maintain a stable API, these headers from -devel subpackage are no longer needed
rm %{buildroot}%{_libdir}/frr/*.so
rm -r %{buildroot}%{_includedir}/frr/

%pre
getent group frrvty >/dev/null 2>&1 || groupadd -r frrvty >/dev/null 2>&1 || :
getent group frr >/dev/null 2>&1 || groupadd -r frr >/dev/null 2>&1 || :
getent passwd frr >/dev/null 2>&1 || useradd -M -r -g frr -s /usr/sbin/nologin \
 -c "FRRouting routing suite" -d %{_localstatedir}/run/frr frr || :
usermod -aG frrvty frr

%post
%systemd_post frr.service

if [ -f %{_infodir}/%{name}.inf* ]; then
    install-info %{_infodir}/frr.info %{_infodir}/dir || :
fi

# Create dummy files if they don't exist so basic functions can be used.
if [ ! -e %{_sysconfdir}/frr/frr.conf ]; then
    echo "hostname `hostname`" > %{_sysconfdir}/frr/frr.conf
    chown frr:frr %{_sysconfdir}/frr/frr.conf
    chmod 640 %{_sysconfdir}/frr/frr.conf
fi

%postun
%systemd_postun_with_restart frr.service

%preun
%systemd_preun frr.service

#only when removing frr
if [ $1 -eq 0 ]; then
	if [ -f %{_infodir}/%{name}.inf* ]; then
    	install-info --delete %{_infodir}/frr.info %{_infodir}/dir || :
	fi
fi

%check
make check PYTHON=%{__python3}

%files
%defattr(-,root,root)
%license COPYING
%doc zebra/zebra.conf.sample
%doc isisd/isisd.conf.sample
%doc ripd/ripd.conf.sample
%doc bgpd/bgpd.conf.sample*
%doc ospfd/ospfd.conf.sample
%doc ospf6d/ospf6d.conf.sample
%doc ripngd/ripngd.conf.sample
%doc pimd/pimd.conf.sample
%doc doc/mpls
%dir %attr(640,frr,frr) %{_sysconfdir}/frr
%dir %attr(755,frr,frr) /var/log/frr
%dir %attr(755,frr,frr) /run/frr
%{_infodir}/*info*
%{_mandir}/man*/*
%dir %{frr_libdir}/
%{frr_libdir}/*
%{_bindir}/*
%dir %{_libdir}/frr
%{_libdir}/frr/*.so.*
%dir %{_libdir}/frr/modules
%{_libdir}/frr/modules/*
%config(noreplace) %attr(644,root,root) /etc/logrotate.d/frr
%config(noreplace) %attr(644,frr,frr) /etc/frr/daemons
%config(noreplace) /etc/pam.d/frr
%{_unitdir}/*.service
%dir /usr/share/yang
/usr/share/yang/*.yang
%{_tmpfilesdir}/%{name}.conf
#%%{_libdir}/frr/frr/libyang_plugins/*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.4-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Jun 17 2021 Thomas Crain <thcrain@microsoft.com> - 7.4-3
- Conditionalize building of tex-based documentation

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Mon Sep 21 2020 Michal Ruprich <mruprich@redhat.com> - 7.4-1
- New version

* Thu Jun 18 2020 Michal Ruprich <michalruprich@gmail.com> - 7.3.1-1
- New version 7.3.1
- Fixes a couple of bugs(#1832259, #1835039, #1830815, #1830808, #1830806, #1830800, #1830798, #1814773)

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

