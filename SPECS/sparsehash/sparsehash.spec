# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
# disable -debuginfo subpackage
%global debug_package %{nil}

Name:           sparsehash
Version:        2.0.3
Release:        15%{?dist}
Summary:        Extremely memory-efficient C++ hash_map implementation

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            http://code.google.com/p/sparsehash
Source0:        https://github.com/sparsehash/sparsehash/archive/sparsehash-%{version}.tar.gz

BuildRequires: make
BuildRequires:  gcc-c++
%description
The Google SparseHash project contains several C++ template hash-map
implementations with different performance characteristics, including
an implementation that optimizes for space and one that optimizes for
speed.

# all files are in -devel package
%package        devel
Summary:        Extremely memory-efficient C++ hash_map implementation

%description    devel
The Google SparseHash project contains several C++ template hash-map
implementations with different performance characteristics, including
an implementation that optimizes for space and one that optimizes for
speed.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT docdir=%{_pkgdocdir}

# Remove unneeded files
rm $RPM_BUILD_ROOT%{_pkgdocdir}/INSTALL
rm $RPM_BUILD_ROOT%{_pkgdocdir}/README_windows.txt

%check
make check

%files devel
%doc %{_pkgdocdir}/
%{_includedir}/google/
%{_includedir}/sparsehash/
%{_libdir}/pkgconfig/libsparsehash.pc

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 2.0.3-13
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Jan Grulich <jgrulich@redhat.com> - 2.0.3-1
- 2.0.3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Jan Grulich <jgrulich@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 16 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.12-5
- Install docs to %%{_pkgdocdir} where available (#994101).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 21 2012 Kalev Lember <kalevlember@gmail.com> - 1.12-1
- Update to 1.12
- Corrected the download URL

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Kalev Lember <kalev@smartlink.ee> - 1.11-1
- Update to 1.11
- Cleaned up the spec file for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Kalev Lember <kalev@smartlink.ee> - 1.10-1
- Update to 1.10

* Fri Dec 17 2010 Kalev Lember <kalev@smartlink.ee> - 1.9-1
- Update to 1.9
- Added libsparsehash.pc pkgconfig file
- The -devel subpackage is no longer noarch as the new .pc file
  needs to go in arch-specific _libdir

* Thu Aug 05 2010 Kalev Lember <kalev@smartlink.ee> - 1.8.1-1
- Update to 1.8.1

* Sat Jul 03 2010 Kalev Lember <kalev@smartlink.ee> - 1.7-3
- Marked -devel as noarch, thanks to Chen Lei (#609728)

* Sat Jul 03 2010 Kalev Lember <kalev@smartlink.ee> - 1.7-2
- Move all files to -devel (#609728)

* Thu Jul 01 2010 Kalev Lember <kalev@smartlink.ee> - 1.7-1
- Initial RPM release
