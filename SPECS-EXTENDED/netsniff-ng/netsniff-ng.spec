Summary:        Packet sniffing beast
Name:           netsniff-ng
Version:        0.6.8
Release:        13%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://netsniff-ng.org/
Source0:        https://www.netsniff-ng.org/pub/%{name}/%{name}-%{version}.tar.xz
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  ncurses-devel
BuildRequires:  GeoIP-devel
BuildRequires:  libnetfilter_conntrack-devel
BuildRequires:  userspace-rcu-devel
BuildRequires:  libnl3-devel
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  libcli-devel
BuildRequires:  perl-podlators
BuildRequires:  zlib-devel
BuildRequires:  libpcap-devel
BuildRequires:  libnet-devel
BuildRequires:  libsodium-devel

%description
netsniff-ng is a high performance Linux network sniffer for packet inspection.
It can be used for protocol analysis, reverse engineering or network
debugging. The gain of performance is reached by 'zero-copy' mechanisms, so
that the kernel does not need to copy packets from kernelspace to userspace.

netsniff-ng toolkit currently consists of the following utilities:

* netsniff-ng: the zero-copy sniffer, pcap capturer and replayer itself.
* trafgen: a high performance zero-copy network packet generator.
* ifpps: a top-like kernel networking and system statistics tool.
* curvetun: a lightweight curve25519-based multiuser IP tunnel.
* ashunt: an autonomous system trace route and ISP testing utility.
* flowtop: a top-like netfilter connection tracking tool.
* bpfc: a tiny Berkeley Packet Filter compiler supporting Linux extensions.

%prep
%autosetup -p1

%build
export NACL_INC_DIR=$(pkg-config --variable=includedir libsodium )/sodium
export NACL_LIB=sodium
# the current configure script doesn't support unknown options, thus we cannot
# use the generic %%configure macro
./configure --prefix='%{_prefix}' --sysconfdir='%{_sysconfdir}'
# the -fcommon is workaround to build with gcc-10, problem reported upstream
%make_build ETCDIR=%{_sysconfdir} Q= STRIP=: \
  CFLAGS="%{optflags} -fPIC -fcommon" LDFLAGS="%{?__global_ldflags}"

%install
make install PREFIX=%{_prefix} ETCDIR=%{_sysconfdir} DESTDIR=%{buildroot}

%files
%license COPYING
%doc AUTHORS README
%{_sbindir}/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_mandir}/man8/*

%changelog
* Wed Mar 08 2023 Sumedh Sharma <sumsharma@microsoft.com> - 0.6.8-13
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- license verified

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.8-11
- Updated geoip conditional

* Tue Jun 14 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.8-10
- Build mausezahn on RHEL/EPEL

* Thu May 26 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.8-9
- Minor spec cosmetic changes
- On RHEL built without GeoIP
  Related: rhbz#2066610

* Tue Mar 22 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.6.8-8
- EVR

* Tue Mar 22 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.6.8-7
- EVR

* Tue Mar 22 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.6.8-6
- libcli rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jun 27 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.8-3
- Rebuilt for new liburcu
  Resolves: rhbz#1976452

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.8-1
- New version
  Resolves: rhbz#1914903

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May  5 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.7-1
- New version
  Resolves: rhbz#1831064

* Mon Feb 10 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.6-5
- Fixed FTBFS with gcc-10
  Resolves: rhbz#1799683

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.6-3
- Added macro to support building on EPEL-8
- Dropped unneeded provides and obsoletes

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.6-1
- New version
  Resolves: rhbz#1708176
- Dropped trafgen-fix-stdin patch (upstreamed)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 20 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.4-5
- Fixed trafgen '--in -' to work again with the STDIN
  Resolves: rhbz#1641273

* Fri Jul 20 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.4-4
- Fixed FTBFS by adding gcc requirement
  Resolves: rhbz#1604949

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.4-1
- New version
  Resolves: rhbz#1531526
- Dropped dont-redefine-memcpyset patch (upstreamed) and stdint
  patch (not needed)

* Mon Oct 02 2017 Remi Collet <remi@fedoraproject.org> - 0.6.3-5
- rebuild for libsodium

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul  3 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.3-2
- Rebuilt for new liburcu
- Compilation fix

* Wed Apr 12 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.3-1
- New version
  Resolves: rhbz#1441439
- Dropped drop-genl-id-generate patch (upstreamed)

* Mon Mar  6 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.2-3
- Dropped GENL_ID_GENERATE to fix compilation with kernel 4.10+

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 16 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.2-1
- New version
  Resolves: rhbz#1392686

* Thu Jul  7 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.1-2
- Rebuilt for new urcu
- Fixed gitignore

* Tue Mar 22 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.1-1
- New version
  Resolves: rhbz#1320148

* Tue Mar  8 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.0-4
- Rebuilt for new libsodium

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 17 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.0-2
- Built with the libsodium instead of the NaCl (upstream hint,
  https://github.com/netsniff-ng/netsniff-ng/issues/152)

* Tue Nov 10 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.0-1
- New version
  Resolves: rhbz#1279885

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.9-1
- New version
  Resolves: rhbz#1220053
- Explicit compilation with -fPIC

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul  1 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.8-4
- Added obsoletes/provides for integrated mausezahn
  Resolves: rhbz#1111779

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.5.8-2
- Fix -debuginfo, make build more verbose
- Fix compiled-in path to /etc/netsniff-ng

* Tue May  6 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.8-1
- New version
  Resolves: rhbz#1092943
- Switched to libnl3
- Switched to xz archive format to save space
- Fixed bogus date in changelog (best effort)
- Dropped flags and libcli-include-fix patches (both not needed)

* Wed Feb 12 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.7-11
- Rebuilt due to liburcu update

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 18 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.7-9
- Fixed build failure (missing pod2man)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep  4 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.7-7
- Build with NaCl, i.e. build curvetun

* Mon Sep  3 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.7-6
- Extended package description according to upstream requirements

* Mon Sep  3 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.7-5
- Fixed license field, the package is licensed under GPLv2, not GPLv2+
- Updated summary & description to be in sync with upstream

* Wed Aug  8 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.7-4
- Removed code that handles drop of sysvinit script (obsoleted now)
  Resolves: rhbz#842793

* Mon Jul 30 2012 Dan Horák <dan[at]danny.cz> - 0.5.7-3
- fix build on secondary arches

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.7-1
- New version
  Resolves: rhbz#836707
- Added missing build requires (NaCl is not in Fedora yet, not using
  the bundled version, thus built without curvetun)

* Tue Apr 24 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.6-2
- Built with RPM_OPT_FLAGS
  Resolves: rhbz#815476

* Thu Mar 29 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.6-1
- New version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 James Findley <sixy@gmx.com> - 0.5.5.0-2
- Fixed packaging bug
- Fixed URL

* Tue Nov 02 2010 James Findley <sixy@gmx.com> - 0.5.5.0-1
- Updated to 0.5.5.0 stable
- This version has major changes, including the removal of  daemon mode.

* Tue Feb 23 2010 James Findley <sixy@gmx.com> - 0.5.5.0-0.4.211svn
- Improved the way sources are provided
- Used the upstream copy of 0.5.3 for check_packets, with a patch

* Wed Feb 17 2010 James Findley <sixy@gmx.com> - 0.5.5.0-0.3.211svn
- Added the check_packets client app:
 - This makes the unix domain socket actually useful
 - This is taken from the 0.5.3 sources, but with a modified makefile

* Sun Feb 14 2010 James Findley <sixy@gmx.com> - 0.5.5.0-0.2.211svn
- Patched the UDS server
- Patched the help text to correctly mark features not yet implemented
- Added BuildRequires and Requires

* Wed Jan 27 2010 James Findley <sixy@gmx.com> - 0.5.5.0-0.1.211svn
- Prerelease of 0.5.0
- Should now work properly on older (e.g. RHEL 5.x) OSes
- Many new features added

* Fri Jan 08 2010 James Findley <sixy@gmx.com> - 0.5.4.1-5
- Added -Wno-format to hide spurious gcc warnings on AMD64

* Thu Jan 07 2010 James Findley <sixy@gmx.com> - 0.5.4.1-4
- Fixed a few typos in the spec
- Zero padded changelog dates

* Thu Jan 07 2010 James Findley <sixy@gmx.com> - 0.5.4.1-3
- Fixed a few more spec errors

* Thu Jan 07 2010 James Findley <sixy@gmx.com> - 0.5.4.1-2
- Adapted for Fedora packaging policy
- Added an initscript

* Wed Jan 06 2010 James Findley <sixy@gmx.com> - 0.5.4.1-1
- Updated to latest stable upstream

* Fri Nov 27 2009 James Findley	<sixy@gmx.com> - 0.5.2-1
- Initial Release
