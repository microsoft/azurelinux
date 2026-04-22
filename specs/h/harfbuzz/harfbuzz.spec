# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           harfbuzz
Version:        11.5.1
Release: 3%{?dist}
Summary:        Text shaping library

License:        MIT-Modern-Variant
URL:            https://github.com/harfbuzz/harfbuzz/
Source0:        https://github.com/harfbuzz/harfbuzz/releases/download/%{version}/harfbuzz-%{version}.tar.xz

# [cmap] malloc fail test (#5710)
# https://github.com/harfbuzz/harfbuzz/commit/1265ff8d990284f04d8768f35b0e20ae5f60daae
#
# Fixes:
#
# Null Pointer Dereference in SubtableUnicodesCache::create leading to DoS
# https://www.cve.org/CVERecord?id=CVE-2026-22693
# https://github.com/harfbuzz/harfbuzz/security/advisories/GHSA-xvjr-f2r9-c7ww
Patch:          https://github.com/harfbuzz/harfbuzz/commit/1265ff8d990284f04d8768f35b0e20ae5f60daae.patch

BuildRequires:  cairo-devel
BuildRequires:  freetype-devel
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libicu-devel
BuildRequires:  graphite2-devel
BuildRequires:  gtk-doc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson

# https://github.com/harfbuzz/harfbuzz/issues/3163
%global _distro_extra_cflags -fno-exceptions
%global _distro_extra_cxxflags -fno-exceptions -fno-rtti

%description
HarfBuzz is an implementation of the OpenType Layout engine.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-icu%{?_isa} = %{version}-%{release}
Requires:       %{name}-cairo%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        icu
Summary:        Harfbuzz ICU support library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    icu
This package contains Harfbuzz ICU support library.

%package        cairo
Summary:        Harfbuzz Cairo support library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    cairo
This package contains Harfbuzz Cairo support library.

%prep
%autosetup -p1


%build
%meson -Dgraphite2=enabled -Dchafa=disabled
%meson_build


%install
%meson_install


%check
%meson_test


%ldconfig_scriptlets

%ldconfig_scriptlets icu

%ldconfig_scriptlets cairo

%files
%license COPYING
%doc NEWS AUTHORS README.md
%{_libdir}/libharfbuzz.so.0*
%{_libdir}/libharfbuzz-gobject.so.0*
%{_libdir}/libharfbuzz-subset.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/HarfBuzz-0.0.typelib

%files devel
%doc %{_datadir}/gtk-doc
%{_bindir}/hb-info
%{_bindir}/hb-view
%{_bindir}/hb-shape
%{_bindir}/hb-subset
%{_includedir}/harfbuzz/
%{_libdir}/libharfbuzz.so
%{_libdir}/libharfbuzz-gobject.so
%{_libdir}/libharfbuzz-cairo.so
%{_libdir}/libharfbuzz-icu.so
%{_libdir}/libharfbuzz-subset.so
%{_libdir}/pkgconfig/harfbuzz.pc
%{_libdir}/pkgconfig/harfbuzz-cairo.pc
%{_libdir}/pkgconfig/harfbuzz-gobject.pc
%{_libdir}/pkgconfig/harfbuzz-icu.pc
%{_libdir}/pkgconfig/harfbuzz-subset.pc
%{_libdir}/cmake/harfbuzz/
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/HarfBuzz-0.0.gir

%files icu
%{_libdir}/libharfbuzz-icu.so.*

%files cairo
%{_libdir}/libharfbuzz-cairo.so.*

%changelog
* Wed Jan 14 2026 Parag Nemade <pnemade AT redhat DOT com> - 11.5.1-2
- Backport security fix for CVE-2026-22693 (fix RHBZ#2429288)

* Tue Sep 23 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.5.1-1
- Update to 11.5.1 version (#2397450)

* Sat Sep 13 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.5.0-1
- Update to 11.5.0 version (#2394917)

* Sun Aug 31 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.4.5-1
- Update to 11.4.5 version (#2392114)

* Tue Aug 26 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.4.4-1
- Update to 11.4.4 version (#2390958)

* Sat Aug 23 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.4.3-1
- Update to 11.4.3 version (#2390520)

* Thu Aug 21 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.4.2-1
- Update to 11.4.2 version (#2390111)

* Thu Aug 14 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.4.1-1
- Update to 11.4.1 version (#2388377)

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 11.3.3-2
- Rebuilt for icu 77.1

* Sun Jul 27 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.3.3-1
- Update to 11.3.3 version (#2382209)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.3.1-1
- Update to 11.3.1 version (#2382200)

* Tue May 13 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.2.1-1
- Update to 11.2.1 version (#2365793)

* Tue Apr 29 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.2.0-1
- Update to 11.2.0 version (#2362728)

* Thu Apr 17 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.1.0-1
- Update to 11.1.0 version (#2360473)

* Sat Apr 05 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.0.1-2
- Upstream removed hb-ot-shape-closure binary

* Sat Apr 05 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.0.1-1
- Update to 11.0.1 version (#2357571)

* Mon Mar 24 2025 Parag Nemade <pnemade AT redhat DOT com> - 11.0.0-1
- Update to 11.0.0 version (#2354378)

* Sat Mar 01 2025 Parag Nemade <pnemade AT redhat DOT com> - 10.4.0-1
- Update to 10.4.0 version (#2349122)

* Fri Feb 21 2025 Parag Nemade <pnemade AT redhat DOT com> - 10.3.0-1
- Update to 10.3.0 version (#2346941)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Parag Nemade <pnemade AT redhat DOT com> - 10.2.0-1
- Update to 10.2.0 version (#2337165)

* Sun Dec 08 2024 Pete Walter <pwalter@fedoraproject.org> - 10.1.0-2
- Rebuild for ICU 76

* Wed Nov 06 2024 Parag Nemade <pnemade AT redhat DOT com> - 10.1.0-1
- Update to 10.1.0 version (#2324060)

* Wed Sep 25 2024 Parag Nemade <pnemade AT redhat DOT com> - 10.0.1-1
- Update to 10.0.1 version (#2314457)

* Tue Aug 20 2024 Parag Nemade <pnemade AT redhat DOT com> - 9.0.0-3
- Split harfbuzz-cairo as a separate subpackage from harfbuzz-devel

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Parag Nemade <pnemade AT redhat DOT com> - 9.0.0-1
- Update to 9.0.0 version (#2295503)

* Fri Jun 21 2024 Parag Nemade <pnemade AT redhat DOT com> - 8.5.0-1
- Update to 8.5.0 version

* Tue Jun 18 2024 Tom Hughes <tom@compton.nu> - 8.4.0-2
- Switch to using meson for build (#2277316)

* Sun Mar 31 2024 Parag Nemade <pnemade AT redhat DOT com> - 8.4.0-1
- Update to 8.4.0 version (#2272294)

* Mon Mar 18 2024 Parag Nemade <pnemade AT redhat DOT com> - 8.3.1-1
- Update to 8.3.1 version (#2270012)

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 8.3.0-5
- Rebuild for ICU 74

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 12 2023 Parag Nemade <pnemade AT redhat DOT com> - 8.3.0-2
- Remove the upstream released patch

* Sun Nov 12 2023 Parag Nemade <pnemade AT redhat DOT com> - 8.3.0-1
- Update to 8.3.0 version (#2244950)

* Sat Sep 30 2023 Parag Nemade <pnemade AT redhat DOT com> - 8.2.1-2
- Resolves:rh#2241391 - Fix LibreOffice tests run

* Wed Sep 20 2023 Parag Nemade <pnemade AT redhat DOT com> - 8.2.1-1
- Update to 8.2.1 version (#2239664)

* Tue Sep 12 2023 Parag Nemade <pnemade AT redhat DOT com> - 8.2.0-1
- Update to 8.2.0 version (#2238190)

* Thu Aug 03 2023 Parag Nemade <pnemade AT redhat DOT com> - 8.1.1-1
- Update to 8.1.1 version (#2228195)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Parag Nemade <pnemade AT redhat DOT com> - 8.0.1-2
- Attempt another build for previouslt failed i686 build

* Fri Jul 14 2023 Parag Nemade <pnemade AT redhat DOT com> - 8.0.1-1
- Update to 8.0.1 version (#2222800)

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 8.0.0-2
- Rebuilt for ICU 73.2

* Tue Jul 11 2023 Parag Nemade <pnemade AT redhat DOT com> - 8.0.0-1
- Update to 8.0.0 version (#2221636)

* Fri Jul 07 2023 Parag Nemade <pnemade AT redhat DOT com> - 7.3.0-2
- Migrate to SPDX license expression

* Thu May 11 2023 Parag Nemade <pnemade AT redhat DOT com> - 7.3.0-1
- Update to 7.3.0 version (#2201459)

* Fri Apr 28 2023 Parag Nemade <pnemade AT redhat DOT com> - 7.2.0-1
- Update to 7.2.0 version (#2190067)

* Fri Mar 03 2023 Parag Nemade <pnemade AT redhat DOT com> - 7.1.0-1
- Update to 7.1.0 version (#2175109)

* Sat Feb 25 2023 Marek Kasik <mkasik@redhat.com> - 7.0.1-2
- Rebuild for freetype-2.13.0

* Wed Feb 22 2023 Parag Nemade <pnemade AT redhat DOT com> - 7.0.1-1
- Update to 7.0.1 version (#2169172)

* Mon Feb 13 2023 Parag Nemade <pnemade AT redhat DOT com> - 7.0.0-2
- Add hb-info, libharfbuzz-cairo library files

* Mon Feb 13 2023 Parag Nemade <pnemade AT redhat DOT com> - 7.0.0-1
- Update to 7.0.0 version (#2169172)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 6.0.0-2
- Rebuild for ICU 72

* Sat Dec 17 2022 Parag Nemade <pnemade AT redhat DOT com> - 6.0.0-1
- Update to 6.0.0 version (#2154489)

* Mon Oct 24 2022 Parag Nemade <pnemade AT redhat DOT com> - 5.3.1-1
- Update to 5.3.1 version (#2136315)

* Tue Oct 11 2022 Parag Nemade <pnemade AT redhat DOT com> - 5.3.0-1
- Update to 5.3.0 version (#2133292)

* Sat Sep 17 2022 Parag Nemade <pnemade AT redhat DOT com> - 5.2.0-1
- Update to 5.2.0 version (#2127603)

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.1.0-2
- Rebuilt for ICU 71.1

* Mon Aug 01 2022 Parag Nemade <pnemade AT redhat DOT com> - 5.1.0-1
- Update to 5.1.0 version (#2112779)

* Sun Jul 24 2022 Parag Nemade <pnemade AT redhat DOT com> - 5.0.1-1
- Update to 5.0.1 version (#2110181)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 29 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.4.1-1
- Update to 4.4.1 version (#2102301)

* Tue Jun 28 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.4.0-1
- Update to 4.4.0 version (#2101663)

* Mon May 23 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.3.0-1
- Update to 4.3.0 version (#2088860)

* Mon Apr 25 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.2.1-1
- Update to 4.2.1 version (#2078234)

* Thu Mar 31 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.2.0-1
- Update to 4.2.0 version (#2070259)

* Mon Mar 28 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.1.0-1
- Update to 4.1.0 version (#2067726)

* Mon Mar 14 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.0.1-1
- Update to 4.0.1 version (#2063439)

* Thu Mar 03 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.0.0-1
- Update to 4.0.0 version (#2059806)

* Sun Feb 13 2022 Parag Nemade <pnemade AT redhat DOT com> - 3.4.0-1
- Update to 3.4.0 version (#2053891)

* Sun Feb 06 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 3.3.2-1
- Update to 3.3.2 (#2051293)

* Thu Feb 03 2022 Parag Nemade <pnemade AT redhat DOT com> - 3.3.1-1
- Update to 3.3.1 version (#2048881)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 13 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.2.0-1
- Update to 3.2.0 version (#2031525)

* Tue Nov 30 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.1.2-1
- Update to 3.1.2 version (#2026992)

* Tue Nov 09 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.1.1-1
- Update to 3.1.1 version (#2021316)

* Sat Nov 06 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.1.0-2
- Fix build failure on armv7hl architecture 

* Fri Nov 05 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.1.0-1
- Update to 3.1.0 version (#2020154)

* Sat Sep 18 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.0.0-1
- Update to 3.0.0 version (#2005503)

* Mon Sep 13 2021 Parag Nemade <pnemade AT redhat DOT com> - 2.9.1-1
- Update to 2.9.1 version (#2002020)

* Fri Aug 20 2021 Parag Nemade <pnemade AT redhat DOT com> - 2.9.0-1
- Update to 2.9.0 version (#1995436)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Parag Nemade <pnemade AT redhat DOT com> - 2.8.2-1
- Update to 2.8.2 version (#1980729)

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 2.8.1-2
- Rebuild for ICU 69

* Wed May 05 2021 Parag Nemade <pnemade AT redhat DOT com> - 2.8.1-1
- Update to 2.8.1 version (#1956915)

* Wed Mar 17 2021 Parag Nemade <pnemade AT redhat DOT com> - 2.8.0-1
- Update to 2.8.0 version (#1939692)

* Fri Feb 5 2021 Marek Kasik <mkasik@redhat.com> - 2.7.4-3
- Build HarfBuzz with bootstrapped freetype

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Dec 27 20:48:11 IST 2020 Parag Nemade <pnemade AT redhat DOT com> - 2.7.4-1
- Update to 2.7.4 version (#1911046)

* Fri Dec 25 14:01:50 IST 2020 Parag Nemade <pnemade AT redhat DOT com> - 2.7.3-1
- Update to 2.7.3 version (#1910482)

* Sat Aug 29 2020 Parag Nemade <pnemade AT redhat DOT com> - 2.7.2-1
- Update to 2.7.2 version (#1873689)

* Thu Aug 20 2020 Parag Nemade <pnemade AT redhat DOT com> - 2.7.1-1
- Update to 2.7.1 version (#1860607)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Parag Nemade <pnemade AT redhat DOT com> - 2.6.8-1
- Update to 2.6.8 version (#1849805)

* Thu Jun 04 2020 Parag Nemade <pnemade AT redhat DOT com> - 2.6.7-1
- Update to 2.6.7 version (#1843592)

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 2.6.6-2
- Rebuild for ICU 67

* Tue May 12 2020 Parag Nemade <pnemade AT redhat DOT com> - 2.6.6-1
- Update to 2.6.6 version (#1834887)

* Wed Mar 18 2020 Parag Nemade <pnemade AT redhat DOT com> - 2.6.4-4
- Use make_build and make_install macros

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 2.6.4-2
- Rebuild for ICU 65

* Wed Oct 30 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.6.4-1
- Update to 2.6.4 version (#1766762)

* Tue Oct 29 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.6.3-1
- Update to 2.6.3 version (#1766396)

* Tue Oct 01 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.6.2-1
- Update to 2.6.2 version (#1757207)

* Wed Sep 18 2019 Kalev Lember <klember@redhat.com> - 2.6.1-2
- Build with --with-gobject --enable-introspection (#1737186)
- Tighten soname globs

* Fri Aug 23 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.6.1-1
- Update to 2.6.1 version (#1744835)

* Sat Aug 17 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.6.0-1
- Update to 2.6.0 version (#1742730)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 12 2019 Adam Williamson <awilliam@redhat.com> - 2.5.3-2
- Revert the offending commit to avoid RHBZ #1689037

* Thu Jun 27 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.5.3-1
- Update to 2.5.3 version (#1724317)

* Fri Jun 21 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.5.2-1
- Update to 2.5.2 version (#1722623)

* Sat Jun 01 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.5.1-1
- Update to 2.5.1 version (#1716024)

* Sun May 26 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.5.0-1
- Update to 2.5.0 version (#1713797)

* Fri Apr 12 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.4.0-1
- Update to 2.4.0 version (#1693940)

* Thu Jan 31 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.3.1-1
- Update to 2.3.1 version (#1671165)

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 2.1.3-2
- Rebuild for ICU 63

* Fri Nov 23 2018 Parag Nemade <pnemade AT redhat DOT com> - 2.1.3-1
- Update to 2.1.3 version

* Thu Nov 08 2018 Parag Nemade <pnemade AT redhat DOT com> - 2.1.1-1
- Update to 2.1.1 version

* Sun Nov 04 2018 Parag Nemade <pnemade AT redhat DOT com> - 2.1.0-1
- Update to 2.1.0 version

* Thu Nov 01 2018 Parag Nemade <pnemade AT redhat DOT com> - 2.0.2-1
- Update to 2.0.2 version

* Sun Oct 28 2018 Parag Nemade <pnemade AT redhat DOT com> - 2.0.1-1
- Update to 2.0.1 version

* Sat Oct 27 2018 Parag Nemade <pnemade AT redhat DOT com> - 2.0.0-1
- Update to 2.0.0 version

* Fri Sep 07 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.8.8-1
- Update to 1.8.8 version

* Thu Aug 09 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.8.7-1
- Update to 1.8.7 version (#1613591)

* Thu Aug 02 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.8.5-1
- Update to 1.8.5 version (#1611028)

* Wed Jul 18 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.8.4-1
- Update to 1.8.4 version (#1601890)

* Fri Jul 13 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.8.3-1
- Update to 1.8.3 version (#1600306)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 1.8.2-2
- Rebuild for ICU 62

* Tue Jul 03 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.8.2-1
- Update to 1.8.2 version (#1597679)

* Thu Jun 14 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.8.1-1
- Update to 1.8.1 version (#1590575)

* Wed Jun 06 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.8.0-1
- Update to 1.8.0 version (#1587987)

* Wed Jun 06 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.7.7-1
- Update to 1.7.7 version (#1552962)

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 1.7.6-2
- Rebuild for ICU 61.1

* Thu Mar 08 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.7.6-1
- Update to 1.7.6 version (#1552962)
- Added new lib libharfbuzz-subset by upstream
- Added harfbuzz cmake file
- Added hb-subset binary file

* Mon Feb 19 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.7.5-3
- Add BuildRequires: gcc-c++ as per packaging guidelines
- Used %%autosetup

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.7.5-1
- Update to 1.7.5 version (#1540396)

* Thu Dec 21 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.7.4-1
- Update to 1.7.4 version (#1528086)

* Tue Dec 19 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.7.3-1
- Update to 1.7.3 version (#1527486)

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 1.7.1-2
- Rebuild for ICU 60.1

* Wed Nov 15 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.7.1-1
- Update to 1.7.1 version (#1513204)

* Tue Nov 14 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.7.0-1
- Update to 1.7.0 version (#1512740)

* Wed Nov 01 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.6.3-1
- Update to 1.6.3 version (#1508201)

* Mon Oct 23 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.6.1-1
- Update to 1.6.1 version (#1505192)

* Sat Oct 21 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.6.0-1
- Update to 1.6.0 version (#1504371)

* Wed Sep 06 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.5.1-1
- Update to 1.5.1 version

* Thu Aug 24 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.5.0-1
- Update to 1.5.0 version

* Wed Aug 09 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.4.8-1
- Update to 1.4.8 version

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.4.7-1
- Update to 1.4.7 version

* Mon Apr 24 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.4.6-1
- Update to 1.4.6 version

* Sun Mar 12 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.4.5-1
- Update to 1.4.5 version

* Mon Mar 06 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.4.4-1
- Update to 1.4.4

* Sun Feb 26 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.4.3-1
- Update to 1.4.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 06 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.4.1-1
- Update to 1.4.1

* Thu Jan 05 2017 Parag Nemade <pnemade AT redhat DOT com> - 1.4.0-1
- Update to 1.4.0

* Tue Dec 06 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.3.4-1
- Update to 1.3.4

* Fri Oct 28 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.3.3-1
- Update to 1.3.3

* Wed Sep 28 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.3.2-1
- Update to 1.3.2

* Thu Sep 08 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.3.1-1
- Update to 1.3.1

* Sun Jul 24 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.3.0-1
- Update to 1.3.0

* Mon May 02 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.2.7-1
- Update to 1.2.7

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 1.2.6-2
- rebuild for ICU 57.1

* Sun Apr 10 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.2.6-1
- Update to 1.2.6

* Tue Apr 05 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.2.5-1
- Update to 1.2.5

* Sat Mar 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.2.4-1
- Update to 1.2.4

* Fri Feb 26 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.2.3-1
- Update to 1.2.3

* Thu Feb 25 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.2.2-1
- Update to 1.2.2

* Thu Feb 25 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.2.1-1
- Update to 1.2.1

* Mon Feb 22 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.2.0-1
- Update to 1.2.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.1.3-1
- Update to 1.1.3

* Mon Dec 21 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.1.2-1
- Update to 1.1.2

* Thu Nov 26 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.1.1-1
- Update to 1.1.1

* Thu Nov 19 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.1.0-1
- Update to 1.1.0

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 1.0.6-2
- rebuild for ICU 56.1

* Fri Oct 16 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.0.6-1
- Update to 1.0.6

* Wed Oct 14 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.0.5-1
- Update to 1.0.5

* Thu Oct 01 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.0.4-1
- Update to 1.0.4

* Tue Sep 01 2015 Kalev Lember <klember@redhat.com> - 1.0.3-1
- Update to 1.0.3
- Use license macro for COPYING

* Mon Aug 24 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.0.2-1
- Update to 1.0.2

* Wed Jul 29 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.0.1-1
- Update to 1.0.1

* Fri Jun 19 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.9.41-1
- Update to 0.9.41 upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.40-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat Mar 21 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.9.40-1
- Update to 0.9.40 upstream release

* Fri Mar 06 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.9.39-1
- Update to 0.9.39 upstream release

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.9.38-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 0.9.38-3
- Bump for rebuild.

* Wed Feb  4 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.9.38-2
- Rebuild for libicu soname bump

* Tue Jan 27 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.9.38-1
- Update to 0.9.38 upstream release

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 0.9.37-2
- rebuild for ICU 54.1

* Tue Dec 23 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.37-1
- Update to 0.9.37 upstream release

* Tue Nov 25 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.36-1
- Update to 0.9.36 upstream release

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 0.9.35-3
- rebuild for ICU 53.1

* Mon Aug 18 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.35-1
- Update to 0.9.35 upstream release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.34-1
- Update to 0.9.34 upstream release

* Tue Jul 29 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.33-1
- Update to 0.9.33 upstream release

* Fri Jul 18 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.32-1
- Update to 0.9.32 (have all the recent releases on koji)

* Thu Jul 17 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.31-1
- Update to 0.9.31 (have all the recent releases on koji)

* Fri Jul 11 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.30-1
- Update to 0.9.30 upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.29-1
- Update to 0.9.29 upstream release

* Tue Apr 29 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.28-1
- Update to 0.9.28 upstream release

* Thu Mar 20 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.27-1
- Update to 0.9.27 upstream release

* Wed Feb 12 2014 Nils Philippsen <nils@redhat.com> - 0.9.26-3
- rebuild for new libicu

* Wed Feb 12 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 0.9.26-2
- Rebuilding for icu soname bump.

* Fri Jan 31 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.26-1
- Update to 0.9.26 upstream release

* Thu Dec 05 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.25-1
- Update to 0.9.25 upstream release

* Fri Nov 15 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.24-1
- Update to 0.9.24 upstream release

* Wed Oct 30 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.23-1
- Update to 0.9.23 upstream release

* Tue Oct 08 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.22-1
- Update to 0.9.22 upstream release

* Tue Sep 17 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.21-1
- Update to 0.9.21 upstream release

* Fri Aug 30 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.20-1
- Update to 0.9.20 upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.19-1
- Update to 0.9.19 upstream release

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 0.9.18-3
- Don't ship a (humongous) ChangeLog

* Fri Jun 07 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.18-2
- Resolves:rh#971795:Merge -icu-devel subpackage into -devel subpackage

* Wed Jun 05 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.18-1
- Update to 0.9.18 upstream release

* Tue May 21 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.17-1
- Update to 0.9.17 upstream release

* Sat Apr 20 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.16-1
- Update to 0.9.16 upstream release

* Fri Mar 22 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.14-1
- Update to 0.9.14 upstream release

* Tue Feb 26 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.13-1
- Update to 0.9.13 upstream release

* Wed Jan 30 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.12-6
- Kill icu-config hack and rebuild against new icu again

* Tue Jan 29 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.12-5
- Resolves:rh#905334 - Please rebuild harfbuzz for new graphite-1.2.0

* Sun Jan 27 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.12-4
- Resolves:rh#904700-Enable additional shaper graphite2

* Sat Jan 26 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.12-3
- Add "icu-config --cppflags" to compiler flags to fix build

* Fri Jan 25 2013 Orion Poplawski <orion@cora.nwra.com> - 0.9.12-2
- Rebuild for libicu 50

* Sun Jan 20 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.12-1
- Update to 0.9.12 upstream release

* Fri Jan 11 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.11-1
- Update to 0.9.11 upstream release

* Thu Jan 03 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.10-1
- Update to 0.9.10 upstream release

* Thu Dec 06 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.9-1
- Update to 0.9.9 upstream release

* Wed Dec 05 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.8-1
- Update to 0.9.8 upstream release

* Wed Nov 21 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.7-1
- Update to 0.9.7 upstream release

* Wed Nov 14 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.6-1
- Update to 0.9.6 upstream release

* Mon Oct 15 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.5-1
- Update to 0.9.5 upstream release

* Mon Sep 10 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.4-1
- Update to 0.9.4 upstream release

* Sun Aug 19 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.3-1
- Update to 0.9.3 upstream release

* Mon Aug 13 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.2-1
- Update to 0.9.2 upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.0-6
- Rebuilt for libicu 49

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.6.0-4
- Rebuild for new libpng

* Sat Sep 10 2011 Kalev Lember <kalevlember@gmail.com> - 0.6.0-3
- Rebuilt for libicu 4.8

* Thu Jun 16 2011 Kalev Lember <kalev@smartlink.ee> - 0.6.0-2
- Moved hb-view to -devel subpackage (#713126)

* Tue Jun 14 2011 Kalev Lember <kalev@smartlink.ee> - 0.6.0-1
- Initial RPM release
