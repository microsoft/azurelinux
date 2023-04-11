# -*- rpm-spec -*-
Summary:        CMPI Utility Library
Name:           libcmpiutil
Version:        0.5.7
Release:        20%{?dist}
License:        LGPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.com/libvirt/libvirt-cim
Source:         https://libvirt.org/sources/CIM/libcmpiutil-%{version}.tar.gz
Patch0:         libcmpiutil-0.5.6-cast-align.patch
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  sblim-cmpi-devel
BuildConflicts: tog-pegasus-devel

%description
Libcmpiutil is a library of utility functions for CMPI providers.
The goal is to reduce the amount of repetitive work done in
most CMPI providers by encapsulating common procedures with more
"normal" APIs.  This extends from operations like getting typed
instance properties to standardizing method dispatch and argument checking.

%package devel
Summary:        Libraries, includes, etc. to use the CMPI utility library
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       sblim-cmpi-devel

%description devel
Includes and documentations for the CMPI utility library
The goal is to reduce the amount of repetitive work done in
most CMPI providers by encapsulating common procedures with more
"normal" APIs.  This extends from operations like getting typed
instance properties to standardizing method dispatch and argument checking.

%prep
%setup -q
chmod -x *.c *.y *.h *.l

%patch0

%build
# FIXME: Package has c11 inline compatibility issues.
# Work-around by appending -std=gnu89 to CFLAGS.
# Proper fix would be to fix the sources.
%configure --enable-static=no --disable-silent-rules CFLAGS="%{optflags} -std=gnu89"
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL="install -p" install
find %{buildroot} -type f -name "*.la" -delete -print
rm -f %{buildroot}%{_libdir}/*.a

%ldconfig_scriptlets

%files
%doc doc/doxygen.conf doc/mainpage README
%license COPYING
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/lib*.so
%dir %{_includedir}/libcmpiutil
%{_includedir}/libcmpiutil/*.h
%{_libdir}/pkgconfig/libcmpiutil.pc

%doc doc/SubmittingPatches

%changelog
* Tue Jan 17 2023 Suresh Thelkar <sthelkar@microsoft.com> - 0.5.7-20
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- Build against sblim-cmpi-devel and instead of tog-pegasus-devel
- License verified

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 13 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.5.7-6
- Append -std=gnu89 to CFLAGS (Address F23FTBFS, RHBZ#1239639).
- Add %%license.
- Modernize spec.
- Make building verbose.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 15 2013 Daniel Veillard <veillard@redhat.com> 0.5.7-1
- update to 0.5.7 upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Jon Ciesla <limburgher@gmail.com> - 0.5.6-4
- Remove cast-align to fix FTBFS on ARM, 872543.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul  6 2011 Daniel Veillard <veillard@redhat.com> - 0.5.6-1
- Update to new upstream release 0.5.6

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 17 2010 Kaitlin Rupert <kaitlin@us.ibm.com> - 0.5.1-1
- Updated to official 0.5.1 source release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Kaitlin Rupert <kaitlin@us.ibm.com> - 0.5-1
- Updated to official 0.5 source release

* Tue May 20 2008 Dan Smith <danms@us.ibm.com> - 0.4-1
- Updated to official 0.4 source release

* Fri Feb 29 2008 Dan Smith <danms@us.ibm.com> - 0.3-1
- Updated to official 0.3 source release

* Wed Feb 13 2008 Dan Smith <danms@us.ibm.com> - 0.2-1
- Updated to official 0.2 source release

* Fri Nov 30 2007 Dan Smith <danms@us.ibm.com> - 0.1-6
- Updated to official 0.1 source release
- Added Source0 URL

* Fri Oct 26 2007 Daniel Veillard <veillard@redhat.com> - 0.1-1
- created
