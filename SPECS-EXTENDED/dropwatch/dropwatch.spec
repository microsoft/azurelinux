Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: dropwatch
Version: 1.5.3
Release: 6%{?dist}
Summary: Kernel dropped packet monitor

License: GPLv2+
URL: https://github.com/nhorman/dropwatch
Source0: https://github.com/nhorman/dropwatch/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0: %{name}-gcc11.patch
Patch1: %{name}-install-dwdump-manpage.patch
Patch2: %{name}-configure-update-obsoleted-m4-macros.patch
Patch3: %{name}-Fix-license-specifiers.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: libtool
BuildRequires: kernel-headers
BuildRequires: binutils-devel
BuildRequires: libnl3-devel
BuildRequires: libpcap-devel
BuildRequires: readline-devel

Requires: libnl3
Requires: readline

%description
dropwatch is an utility to interface to the kernel to monitor for dropped
network packets.

%prep
%autosetup -p1

%build
./autogen.sh
%configure
%make_build

%install
%{make_install}

%files
%{_bindir}/dropwatch
%{_bindir}/dwdump
%{_mandir}/man1/dropwatch.1*
%{_mandir}/man1/dwdump.1*
%doc README.md
%license COPYING

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.3-6
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Mon Jul 12 2021 Hangbin Liu <haliu@redhat.com> - 1.5.3-5
- Update spec file
- Update Makefile license
- Update obsoleted m4 macros
- Install new command dwdump

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 13 2020 Jeff Law <law@redhat.com> - 1.5.3-3
- Fix off-by-one buffer overflow caught by gcc-11

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar 19 2020 Neil Horman <nhorman@redhat.com> - 1.5.3-1
- Update to latest upstream

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.5-7
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 18 2018 Neil Horman <nhorman@redhat.com> - 1.5-4
- add rpm-build to test.yml inventory

* Fri May 18 2018 Neil Horman <nhorman@redhat.com> - 1.5-3
- add wget to test.yml inventory

* Fri May 18 2018 Neil Horman <nhorman@redhat.com> - 1.5-2
- Make inventory script executable

* Tue May 15 2018 Neil Horman <nhorman@redhat.com> - 1.5-1
- Update to latest upstream and add CI harness

* Tue May 08 2018 Neil Horman <nhorman@redhat.com> - 1.4-23
- Updated specfile url and source location for github

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 01 2018 Neil Horman <nhorman@redhat.com> - 1.4-21
- Fix linker flag recognition (bz 1541058)

* Thu Feb  1 2018 Florian Weimer <fweimer@redhat.com> - 1.4-20
- Build with linker flags from redhat-rpm-config

* Tue Jan 30 2018 Merlin Mathesius <mmathesi@redhat.com> - 1.4-19
- Drop unnecessary BuildRequires for binutils-static
  Not building kernel modules, so use kernel-headers instead of kernel-devel

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Neil Horman <nhorman@redhat.com> - 1.4-15
- fix build error (bz 1412926)

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.4-14
- Rebuild for readline 7.x

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 06 2015 Neil Horman <nhorman@redhat.com> - 1.4-12
- Fixed FTBFS issue (bz 1239436)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov 29 2013 Neil Horman <nhorman@redhat.com> - 1.4-8
- Updating spec file

* Fri Nov 29 2013 Neil Horman <nhorman@redhat.com> - 1.4-7
- Drop libnl-devel BuildRequire (bz 1035791)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Dan Horák <dan@danny.cz> - 1.4-4
- rebuilt again for fixed soname in libnl3

* Fri Jan 18 2013 Neil Horman <nhorman@redhat.com> - 1.4-3
- rebuilt to pull in new libnl3 dependencies

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 01 2012 Neil Horman <nhorman@redhat.com> - 1.4-1
- Update to latest upstream

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 30 2010 Neil Horman <nhorman@redhat.com> - 1.2
- Update to latest upstream

* Thu Apr 08 2010 Neil Horman <nhorman@redhat.com> - 1.1-2
- Adding more missing buildrequires

* Wed Apr 07 2010 Neil Horman <nhorman@redhat.com> - 1.1-1
- Add missing buildrequires

* Wed Apr 07 2010 Neil Horman <nhorman@redhat.com> - 1.1-0
- Move to latest upstream sources

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 20 2009 Neil Horman <nhorman@redhat.com> 1.0-2
- Fixed up Errors found in package review (bz 491240)

* Tue Mar 17 2009 Neil Horman <nhorman@redhat.com> 1.0-1
- Initial build

