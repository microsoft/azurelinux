# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine __cmake_in_source_build

Name:           lasi
Version:        1.1.3
Release:        17%{?dist}
Summary:        C++ library for creating Postscript documents

# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+
URL:            http://www.unifont.org/lasi/
Source0:        http://downloads.sourceforge.net/lasi/libLASi-%{version}.tar.gz
Patch0:         lasi-multilib.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.13.2
BuildRequires:  pango-devel
BuildRequires:  doxygen
# Build fails with this
#BuildRequires:  inkscape
# For testing
BuildRequires:  dejavu-sans-mono-fonts


%description
LASi is a library written by Larry Siden  that provides a C++ stream output
interface ( with operator << ) for creating Postscript documents that can
contain characters from any of the scripts and symbol blocks supported in
Unicode  and by Owen Taylor's Pango layout engine. The library accommodates
right-to-left scripts such as Arabic and Hebrew as easily as left-to-right
scripts. Indic and Indic-derived Complex Text Layout (CTL) scripts, such as
Devanagari, Thai, Lao, and Tibetan are supported to the extent provided by
Pango and by the OpenType fonts installed on your system. All of this is
provided without need for any special configuration or layout calculation on
the programmer's part.

Although the capability to produce Unicode-based multilingual Postscript
documents exists in large Open Source application framework libraries such as
GTK+, QT, and KDE, LASi was designed for projects which require the ability
to produce Postscript independent of any one application framework.


%package        devel
Summary:        Development headers and libraries for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pango-devel

%description    devel
%{summary}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
%{summary}.


%prep
%setup -q -n libLASi-%{version}
%patch -P0 -p1 -b .multilib
# Change docdir
sed -i -e '/set(docdir/s| .*| %{_pkgdocdir}|' cmake/modules/instdirs.cmake


%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS -std=c++14"
export FFLAGS="$RPM_OPT_FLAGS"
%cmake -DUSE_RPATH=OFF -DCMAKE_INSTALL_LIBDIR=%{_libdir}
%cmake_build


%install
%cmake_install


%check
%ctest --verbose


%ldconfig_scriptlets


%files
%doc AUTHORS ChangeLog.release COPYING README
%{_libdir}/libLASi.so.2*


%files devel
%{_includedir}/LASi.h
%{_libdir}/libLASi.so
%{_libdir}/pkgconfig/lasi.pc
%doc %{_datadir}/lasi%{version}/

%files doc
%{_pkgdocdir}/html/


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.1.3-15
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Jeff Law <law@redhat.com> - 1.1.3-5
- Force C++14 as this code is not C++17 ready

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Orion Poplawski <orion@nwra.com> - 1.1.3-3
- Use new %%cmake_* macros

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 1 2019 Orion Poplawski <orion@nwra.com> - 1.1.3-1
- Update to 1.1.3 (soname bump)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.1.2-4
- Rebuilt for GCC 5 C++11 ABI change

* Tue Feb 17 2015 Orion Poplawski <orion@cora.nwra.com> - 1.1.2-3
- Rebuild for gcc 5 C++11 ABI

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 26 2014 Orion Poplawski <orion@cora.nwra.com> - 1.1.2-1
- Update to 1.1.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 24 2014 Orion Poplawski <orion@cora.nwra.com> - 1.1.1-8
- Add patch to build with freetype 2.5.1+ (bug #1057815)
- BUild and package documentation

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Orion Poplawski <orion@cora.nwra.com> - 1.1.1-4
- Fix multilib conflict (Bug 831398)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 - Orion Poplawski <orion@cora.nwra.com> - 1.1.1-1
- Update to 1.1.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 - Orion Poplawski <orion@cora.nwra.com> - 1.1.0-5
- Fix font BR

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 - Orion Poplawski <orion@cora.nwra.com> - 1.1.0-3
- Change BR to dejavu-fonts-compat
- Add -DCMAKE_SKIP_RPATH:BOOL=OFF -DUSE_RPATH=OFF to cmake to
  use rpath during build, but not install

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.0-2
- fix license tag

* Sat Feb  9 2008 - Orion Poplawski <orion@cora.nwra.com> - 1.1.0-1
- Update to 1.1.0

* Tue Aug 29 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.0.6-1
- Update to 1.0.6
- Remove pkg-config patch applied upstream

* Mon May  8 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.0.5-2
- Disable static libs
- Patch pc file to return -lLASi

* Thu May  4 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.0.5-1
- Update to 1.0.5
- Remove unneeded patches and autotools
- Move doc dir to -devel package
- Make -devel package require pango-devel, included in LASi.h

* Mon Apr 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.0.4-1
- Initial Fedora Extras version
