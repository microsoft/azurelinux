Summary:        Manipulate netfilter connection tracking table and run High Availability
Name:           conntrack-tools
Version:        1.4.8
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://conntrack-tools.netfilter.org/
Source0:        https://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.xz
Source1:        conntrackd.service
Source2:        conntrackd.conf
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  libmnl-devel >= 1.0.3
BuildRequires:  libnetfilter_conntrack-devel >= 1.0.7
BuildRequires:  libnetfilter_cthelper-devel >= 1.0.0
BuildRequires:  libnetfilter_cttimeout-devel >= 1.0.0
BuildRequires:  libnetfilter_queue-devel >= 1.0.2
BuildRequires:  libnfnetlink-devel >= 1.0.1
BuildRequires:  libtirpc-devel
BuildRequires:  pkg-config
BuildRequires:  systemd
BuildRequires:  systemd-devel
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd
Provides:       conntrack = 1.0-1
Obsoletes:      conntrack < 1.0-1

%description
With conntrack-tools you can setup a High Availability cluster and
synchronize conntrack state between multiple firewalls.

The conntrack-tools package contains two programs:
- conntrack: the command line interface to interact with the connection
             tracking system.
- conntrackd: the connection tracking userspace daemon that can be used to
              deploy highly available GNU/Linux firewalls and collect
              statistics of the firewall use.

conntrack is used to search, list, inspect and maintain the netfilter
connection tracking subsystem of the Linux kernel.
Using conntrack, you can dump a list of all (or a filtered selection  of)
currently tracked connections, delete connections from the state table,
and even add new ones.
In addition, you can also monitor connection tracking events, e.g.
show an event message (one line) per newly established connection.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-systemd
sed -i "s/DEFAULT_INCLUDES = -I./DEFAULT_INCLUDES = -I. -I\/usr\/include\/tirpc/" src/helpers/Makefile
CFLAGS="${CFLAGS} -Wl,-z,lazy"
CXXFLAGS="${CXXFLAGS} -Wl,-z,lazy"
%make_build
chmod 644 doc/sync/primary-backup.sh
rm -f doc/sync/notrack/conntrackd.conf.orig doc/sync/alarm/conntrackd.conf.orig doc/helper/conntrackd.conf.orig

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
mkdir -p %{buildroot}%{_sysconfdir}/conntrackd
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/conntrackd/

# Add a systemd preset to disable the service by default
install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable conntrackd.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-conntrackd.preset

%files
%license COPYING
%doc AUTHORS TODO doc
%dir %{_sysconfdir}/conntrackd
%config(noreplace) %{_sysconfdir}/conntrackd/conntrackd.conf
%{_unitdir}/conntrackd.service
%{_sbindir}/conntrack
%{_sbindir}/conntrackd
%{_sbindir}/nfct
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %{_libdir}/conntrack-tools
%{_libdir}/conntrack-tools/*
%config(noreplace) %{_libdir}/systemd/system-preset/50-conntrackd.preset

%post
%systemd_post conntrackd.service

%preun
%systemd_preun conntrackd.service

%postun
%systemd_postun conntrackd.service

%changelog
* Wed Jan 24 2024 Sharath Srikanth Chellappa <sharathsr@microsoft.com> - 1.4.8-1
- Bump version to v1.4.8 from v1.4.5
- Updating source from tar.bz2 to tar.xz

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.4.5-8
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Oct 31 2022 Francisco Huelsz Prince <frhuelsz@microsoft.com> - 1.4.5-7
- Service is disabled by default. Now a minimal working config is provided.

* Tue Feb 02 2021 Henry Beberman <henry.beberman@microsoft.com> - 1.4.5-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified.
- Spec linted.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 14 2018 Paul Wouters <pwouters@redhat.com> - 1.4.5-2
- Disable hardened build to really fix rhbz#1413408

* Mon Dec 10 2018 Paul Wouters <pwouters@redhat.com> - 1.4.5-1
- Resolves: rhbz#1574091 conntrack-tools-1.4.5 is available
- Resolves: rhbz#1413408 ct_helper_ftp not working
  (I've reduced the hardening to use -z,lazy)
- Eanbled systemd support
- Bumped required libnetfilter_conntrack-devel to 1.0.7
- fixup harmless but broken mkdir in spec file
- Don't override CPPFLAGS and LIBS, instead fixup src/helpers/Makefile

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 12 2018 Orion Poplawski <orion@nwra.com> - 1.4.4-7
- Use libtirpc
- Use %%license

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 22 2017 Paul Wouters <pwouters@redhat.com> - 1.4.4-3
- Add upstream patches (free pktb after use, nat_tuple leak)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 22 2016 Paul Wouters <pwouters@redhat.com> - 1.4.4-1
- Updated to 1.4.4 (rhbz#1370668)
- Include new man5 pages

* Wed Apr 20 2016 Paul Wouters <pwouters@redhat.com> - 1.4.3-1
- Resolves: rhbz#1261220 1.4.3 is available
- Update source url
- Remove incorporated patches

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 21 2015 Paul Wouters <pwouters@redhat.com> - 1.4.2-10
- Resolves: 1255578 - conntrackd could neither be started nor be stopped

* Tue Aug 18 2015 Paul Wouters <pwouters@redhat.com> - 1.4.2-9
- Resolves: rhbz#CVE-2015-6496, rhbz#1253757
- Fold in upstream patches since 1.4.2 release up to git 900d7e8
- Fold in upstream patch set of 2015-08-18 for coverity issues

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 12 2015 Paul Komkoff <i@stingr.net> - 1.4.2-7
- bz#1181119 - wait for network to be on before starting conntrackd

* Sun Jan 11 2015 Paul Komkoff <i@stingr.net> - 1.4.2-6
- bz#998105 - remove patch residues from doc

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Paul Komkoff <i@stingr.net> - 1.4.2-3
- rebuilt

* Sat Sep  7 2013 Paul P. Komkoff Jr <i@stingr.net> - 1.4.2-2
- bz#850067

* Sat Sep  7 2013 Paul P. Komkoff Jr <i@stingr.net> - 1.4.2-1
- new upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 08 2013 Paul Komkoff <i@stingr.net> - 1.4.0-2
- fix bz#909128

* Mon Nov 26 2012 Paul P. Komkoff Jr <i@stingr.net> - 1.4.0-1
- new upstream version

* Tue Jul 24 2012 Paul P. Komkoff Jr <i@stingr.net> - 1.2.1
- new upstream version

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 07 2012 Paul Wouters <pwouters@redhat.com> - 1.0.1-1
- Updated to 1.0.1
- Added daemon using systemd and configuration file
- Removed legacy spec requirements
- Patch for: parse.c:240:34: error: 'NULL' undeclared 

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu May  5 2011 Paul P. Komkoff Jr <i@stingr.net> - 1.0.0
- new upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Paul P. Komkoff Jr <i@stingr.net> - 0.9.15-1
- new upstream version

* Thu Mar 25 2010 Paul P. Komkoff Jr <i@stingr.net> - 0.9.14-1
- update, at last

* Tue Nov 10 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.13-2
- failed to properly commit the package :(

* Tue Oct 13 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.13-1
- new upstream version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 24 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.12-3
- new upstream version

* Sun May 24 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.12-2
- versioning screwup

* Sun May 24 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.12-1
- new upstream version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.9-1
- new upstream version

* Sun Oct 26 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.9.8-1
- new upstream version
- remove rollup patch

* Wed Jul 16 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.9.7-2
- fix Patch0/%%patch.

* Wed Jul 16 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.9.7-1
- new upstream version

* Sat Feb 23 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.9.6-0.1.svn7382
- new version from svn

* Fri Feb 22 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.9.5-5
- fix the PATH_MAX-related compilation problem

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.5-4
- Autorebuild for GCC 4.3

* Tue Oct 23 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.5-3
- review fixes

* Sun Oct 21 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.5-2
- review fixes

* Fri Oct 19 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.5-1
- new upstream version

* Sun Jul 22 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.4-1
- replace conntrack with conntrack-tools
