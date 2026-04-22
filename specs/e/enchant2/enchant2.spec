# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond mingw %[%{undefined rhel} && %{undefined flatpak}]

Name:          enchant2
Version:       2.8.15
Release: 2%{?dist}
Summary:       An Enchanting Spell Checking Library

License:       LGPL-2.0-or-later
URL:           https://github.com/rrthomas/enchant
Source0:       https://github.com/rrthomas/enchant/releases/download/v%{version}/enchant-%{version}.tar.gz

%if !0%{?rhel}
# Look for aspell using pkg-config, instead of AC_CHECK_LIB which adds -laspell
# to the global LIBS and over-links libenchant (#1574893).  This patch
# can't currently go upstream, because aspell.pc is a Fedora addition
# that itself has not gone upstream.
Patch:         0001-Use-pkg-config-to-configure-Aspell.patch
%endif

BuildRequires: automake autoconf libtool
BuildRequires: gcc-c++
BuildRequires: libicu-devel
BuildRequires: make
BuildRequires: glib2-devel
BuildRequires: hunspell-devel
BuildRequires: libvoikko-devel
BuildRequires: vala

%if !0%{?rhel}
BuildRequires: aspell-devel
BuildRequires: nuspell-devel
%endif

%if %{with mingw}
BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-glib2
BuildRequires: mingw32-icu
BuildRequires: mingw32-hunspell
%if !0%{?rhel}
BuildRequires: mingw32-nuspell
%endif


BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-glib2
BuildRequires: mingw64-icu
BuildRequires: mingw64-hunspell
%if !0%{?rhel}
BuildRequires: mingw64-nuspell
%endif
%endif

Provides:      bundled(gnulib)


%description
A library that wraps other spell checking backends.


%if !0%{?rhel}
%package aspell
Summary:       Integration with aspell for libenchant
Requires:      enchant2%{?_isa} = %{version}-%{release}
Supplements:   (enchant2 and aspell)

%description aspell
Libraries necessary to integrate applications using libenchant with aspell.

%package nuspell
Summary:       Integration with Nuspell for libenchant
Requires:      enchant2%{?_isa} = %{version}-%{release}
Supplements:   (enchant2 and nuspell)

%description nuspell
Libraries necessary to integrate applications using libenchant with Nuspell.
%endif

%package voikko
Summary:       Integration with voikko for libenchant
Requires:      enchant2%{?_isa} = %{version}-%{release}
Supplements:   (enchant2 and langpacks-fi)

%description voikko
Libraries necessary to integrate applications using libenchant with voikko.


%package devel
Summary:       Development files for %{name}
Requires:      enchant2%{?_isa} = %{version}-%{release}
Requires:      glib2-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%if %{with mingw}
%package -n mingw32-%{name}
Summary:       MinGW Windows %{name} library
BuildArch:     noarch

%description -n mingw32-%{name}
MinGW Windows %{name} library.


%package -n mingw64-%{name}
Summary:       MinGW Windows %{name} library
BuildArch:     noarch

%description -n mingw64-%{name}
MinGW Windows %{name} library.
%endif


%{?mingw_debug_package}


%prep
%autosetup -p1 -n enchant-%{version}

# Needed for 0001-Use-pkg-config-to-configure-Aspell.patch
autoreconf -ifv


%build
# Native build
mkdir build_native
pushd build_native
%define _configure ../configure
%configure \
%if !0%{?rhel}
    --with-aspell \
    --with-nuspell \
%endif
    --with-hunspell-dir=%{_datadir}/hunspell \
    --without-hspell \
    --disable-static \
    --docdir=%{_defaultdocdir}/%{name}
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g;
        s|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build pkgdatadir=%{_datadir}/enchant-2
popd

%if %{with mingw}
# MinGW build
MINGW32_CONFIGURE_ARGS="--with-hunspell-dir=%{mingw32_datadir}/hunspell" \
MINGW64_CONFIGURE_ARGS="--with-hunspell-dir=%{mingw64_datadir}/hunspell" \
%mingw_configure --disable-static --without-hspell --enable-relocatable

MINGW32_MAKE_ARGS="pkgdatadir=%{mingw32_datadir}/enchant-2" \
MINGW64_MAKE_ARGS="pkgdatadir=%{mingw64_datadir}/enchant-2" \
%mingw_make_build
%endif


%install
# Native build
%make_install -C build_native pkgdatadir=%{_datadir}/enchant-2

%if %{with mingw}
# MinGW build
MINGW32_MAKE_ARGS="pkgdatadir=%{mingw32_datadir}/enchant-2" \
MINGW64_MAKE_ARGS="pkgdatadir=%{mingw64_datadir}/enchant-2" \
%mingw_make_install
rm -rf %{buildroot}%{mingw32_datadir}/{doc,man}
rm -rf %{buildroot}%{mingw64_datadir}/{doc,man}
%endif

find %{buildroot} -name '*.la' -delete


%{?mingw_debug_install_post}


%files
%doc AUTHORS NEWS README
%license COPYING.LIB
%{_bindir}/enchant-2
%{_bindir}/enchant-lsmod-2
%{_libdir}/libenchant-2.so.*
%dir %{_libdir}/enchant-2
%{_libdir}/enchant-2/enchant_hunspell.so
%{_mandir}/man1/*
%{_datadir}/enchant-2-2

%if !0%{?rhel}
%files aspell
%{_libdir}/enchant-2/enchant_aspell.so*

%files nuspell
%{_libdir}/enchant-2/enchant_nuspell.so*
%endif

%files voikko
%{_libdir}/enchant-2/enchant_voikko.so*

%files devel
%doc %{_defaultdocdir}/%{name}/enchant.html
%doc %{_defaultdocdir}/%{name}/enchant-2.html
%doc %{_defaultdocdir}/%{name}/enchant-lsmod-2.html
%{_libdir}/libenchant-2.so
%{_libdir}/pkgconfig/enchant-2.pc
%{_includedir}/enchant-2
%{_mandir}/man5/enchant.5*


%if %{with mingw}
%files -n mingw32-%{name}
%license COPYING.LIB
%{mingw32_bindir}/enchant-lsmod-2.exe
%{mingw32_bindir}/enchant-2.exe
%{mingw32_bindir}/libenchant-2-2.dll
%{mingw32_includedir}/enchant-2/
%dir %{mingw32_libdir}/enchant-2/
%{mingw32_libdir}/enchant-2/enchant_hunspell.dll
%if !0%{?rhel}
%{mingw32_libdir}/enchant-2/enchant_nuspell.dll
%endif
%{mingw32_libdir}/libenchant-2.dll.a
%{mingw32_libdir}/pkgconfig/enchant-2.pc
%{mingw32_datadir}/enchant-2-2/

%files -n mingw64-%{name}
%license COPYING.LIB
%{mingw64_bindir}/enchant-lsmod-2.exe
%{mingw64_bindir}/enchant-2.exe
%{mingw64_bindir}/libenchant-2-2.dll
%{mingw64_includedir}/enchant-2/
%dir %{mingw64_libdir}/enchant-2/
%{mingw64_libdir}/enchant-2/enchant_hunspell.dll
%if !0%{?rhel}
%{mingw64_libdir}/enchant-2/enchant_nuspell.dll
%endif
%{mingw64_libdir}/libenchant-2.dll.a
%{mingw64_libdir}/pkgconfig/enchant-2.pc
%{mingw64_datadir}/enchant-2-2/
%endif


%changelog
* Tue Feb 17 2026 Sandro Mani <manisandro@gmail.com> - 2.8.15-1
- Update to 2.8.15

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sat Nov 22 2025 Sandro Mani <manisandro@gmail.com> - 2.8.14-1
- Update to 2.8.14

* Mon Aug 18 2025 Sandro Mani <manisandro@gmail.com> - 2.8.12-4
- Make icu BR explicit

* Fri Aug 15 2025 Sandro Mani <manisandro@gmail.com> - 2.8.12-3
- Rebuild (icu)

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 2.8.12-2
- Rebuilt for icu 77.1

* Wed Jul 30 2025 Sandro Mani <manisandro@gmail.com> - 2.8.12-1
- Update to 2.8.12

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 23 2025 Sandro Mani <manisandro@gmail.com> - 2.8.11-1
- Update to 2.8.11

* Sun Jun 22 2025 Sandro Mani <manisandro@gmail.com> - 2.8.10-1
- Update to 2.8.10

* Wed Jun 18 2025 Sandro Mani <manisandro@gmail.com> - 2.8.9-1
- Update to 2.8.9

* Tue Jun 17 2025 Sandro Mani <manisandro@gmail.com> - 2.8.8-1
- Update to 2.8.8

* Mon Jun 16 2025 Sandro Mani <manisandro@gmail.com> - 2.8.7-1
- Update to 2.8.7

* Sat May 31 2025 Sandro Mani <manisandro@gmail.com> - 2.8.6-1
- Update to 2.8.6

* Thu May 29 2025 Sandro Mani <manisandro@gmail.com> - 2.8.5-1
- Update to 2.8.5

* Sat May 03 2025 Sandro Mani <manisandro@gmail.com> - 2.8.4-1
- Update to 2.8.4

* Mon Mar 24 2025 Tim Landscheidt <tim@tim-landscheidt.de> - 2.8.2-6
- Fix package description for mingw32-enchant2

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Sandro Mani <manisandro@gmail.com> - 2.8.2-4
- Rebuild (mingw-icu)

* Fri Dec 06 2024 Sandro Mani <manisandro@gmail.com> - 2.8.2-3
- Rebuild (mingw-icu)

* Wed Oct 16 2024 Peter Oliver <rpm@mavit.org.uk> - 2.8.2-2
- Restore enchant2-aspell subpackage

* Thu Aug 15 2024 Sandro Mani <manisandro@gmail.com> - 2.8.2-1
- Update to 2.8.2

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 13 2024 Sandro Mani <manisandro@gmail.com> - 2.8.1-1
- Update to 2.8.1

* Mon May 27 2024 Sandro Mani <manisandro@gmail.com> - 2.8.0-1
- Update to 2.8.0

* Tue May 07 2024 Sandro Mani <manisandro@gmail.com> - 2.7.3-1
- Update to 2.7.3

* Sun Apr 28 2024 Sandro Mani <manisandro@gmail.com> - 2.7.2-1
- Update to 2.7.2

* Mon Apr 22 2024 Sandro Mani <manisandro@gmail.com> - 2.7.0-1
- Update to 2.7.0

* Mon Apr 08 2024 Sandro Mani <manisandro@gmail.com> - 2.6.9-1
- Update to 2.6.9

* Sat Mar 23 2024 Sandro Mani <manisandro@gmail.com> - 2.6.8-1
- Update to 2.6.8

* Mon Feb 12 2024 Sandro Mani <manisandro@gmail.com> - 2.6.7-1
- Update to 2.6.7

* Mon Feb 05 2024 Sandro Mani <manisandro@gmail.com> - 2.6.6-2
- Rebuild (icu)

* Mon Feb 05 2024 Sandro Mani <manisandro@gmail.com> - 2.6.6-1
- Update to 2.6.6

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 2.6.5-4
- Rebuild for ICU 74

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 09 2024 Sandro Mani <manisandro@gmail.com> - 2.6.5-1
- Update to 2.6.5

* Tue Dec 12 2023 Sandro Mani <manisandro@gmail.com> - 2.6.4-1
- Update to 2.6.4

* Sun Dec 03 2023 Sandro Mani <manisandro@gmail.com> - 2.6.3-1
- Update to 2.6.3

* Wed Nov 01 2023 Sandro Mani <manisandro@gmail.com> - 2.6.2-1
- Update to 2.6.2

* Mon Sep 25 2023 Sandro Mani <manisandro@gmail.com> - 2.6.1-1
- Update to 2.6.1

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Sandro Mani <manisandro@gmail.com> - 2.5.0-4
- Rebuild (mingw-icu)

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 2.5.0-3
- Rebuilt for ICU 73.2

* Tue Jul 04 2023 Sandro Mani <manisandro@gmail.com> - 2.5.0-2
- Drop aspell subpackage (#2218153)

* Wed May 24 2023 Sandro Mani <manisandro@gmail.com> - 2.5.0-1
- Update to 2.5.0

* Tue May 23 2023 Sandro Mani <manisandro@gmail.com> - 2.4.0-1
- Update to 2.4.0

* Mon Apr 24 2023 Sandro Mani <manisandro@gmail.com> - 2.3.4-2
- Disable mingw by default in RHEL builds

* Mon Feb 20 2023 Sandro Mani <manisandro@gmail.com> - 2.3.4-1
- Update to 2.3.4

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Sandro Mani <manisandro@gmail.com> - 2.3.3-5
- Rebuild (mingw-icu)

* Tue Jan 03 2023 Sandro Mani <manisandro@gmail.com> - 2.3.3-4
- Rebuild (mingw-icu)

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 2.3.3-3
- Rebuild for ICU 72

* Sat Aug 06 2022 Sandro Mani <manisandro@gmail.com> - 2.3.3-2
- Rebuild (mingw-icu)

* Mon Aug 01 2022 Sandro Mani <manisandro@gmail.com> - 2.3.3-1
- Update to 2.3.3

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 2.3.2-8
- Rebuilt for ICU 71.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 2.3.2-6
- Rebuild with mingw-gcc-12

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 2.3.2-5
- Make mingw subpackages noarch

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 2.3.2-4
- Add mingw subpackages

* Tue Jan 25 2022 Parag Nemade <pnemade AT redhat DOT com> - 2.3.2-3
- Update hunspell-dir path
  F36 Change https://fedoraproject.org/wiki/Changes/Hunspell_dictionary_dir_change

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec 05 2021 Sandro Mani <manisandro@gmail.com> - 2.3.2-1
- Update to 2.3.2

* Wed Aug 11 2021 Sandro Mani <manisandro@gmail.com> - 2.3.1-1
- Update to 2.3.1

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Sandro Mani <manisandro@gmail.com> - 2.3.0-1
- Update to 2.3.0

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 2.2.15-7
- Rebuild for ICU 69

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 2.2.15-6
- Rebuild for ICU 69

* Sat Mar 06 2021 Peter Oliver <rpm@mavit.org.uk> - 2.2.15-5
- Recommend enchant2-aspell if enchant2 and aspell are both installed.

* Mon Feb 08 2021 Kalev Lember <klember@redhat.com> - 2.2.15-4
- Disable nuspell support for RHEL (#1925839)

* Tue Feb  2 2021 Peter Oliver <rpm@mavit.org.uk> - 2.2.15-3
- Include support for Nuspell.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 23 2020 Sandro Mani <manisandro@gmail.com> - 2.2.15-1
- Update to 2.2.15

* Mon Dec 14 2020 Sandro Mani <manisandro@gmail.com> - 2.2.14-1
- Update to 2.2.14

* Tue Nov 03 2020 Sandro Mani <manisandro@gmail.com> - 2.2.13-1
- Update to 2.2.13

* Sat Oct 17 2020 Sandro Mani <manisandro@gmail.com> - 2.2.12-1
- Update to 2.2.12

* Tue Sep 08 2020 Sandro Mani <manisandro@gmail.com> - 2.2.11-1
- Update to 2.2.11

* Wed Sep 02 2020 Sandro Mani <manisandro@gmail.com> - 2.2.10-1
- Update to 2.2.10

* Mon Aug 24 2020 Sandro Mani <manisandro@gmail.com> - 2.2.9-1
- Update to 2.2.9

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 02 2020 Sandro Mani <manisandro@gmail.com> - 2.2.8-1
- Update to 2.2.8

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 15 2019 Sandro Mani <manisandro@gmail.com> - 2.2.7-1
- Update to 2.2.7

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Sandro Mani <manisandro@gmail.com> - 2.2.5-1
- Update to 2.2.5

* Fri Jun 28 2019 Sandro Mani <manisandro@gmail.com> - 2.2.4-2
- Add patch to fix memory leaks (#1718084)
- Pass --without-hspell

* Tue Jun 18 2019 Sandro Mani <manisandro@gmail.com> - 2.2.4-1
- Update to 2.2.4

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Sandro Mani <manisandro@gmail.com> - 2.2.3-4
- Add patch to avoid unnecessary linking of libenchant against libaspell (#1574893)

* Wed May 16 2018 Parag Nemade <pnemade AT redhat DOT com> - 2.2.3-3
- Make enchant2-voikko installed by langpacks-fi package (#1578352)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Sandro Mani <manisandro@gmail.com> - 2.2.3-1
- Update to 2.2.3

* Wed Jan 03 2018 Sandro Mani <manisandro@gmail.com> - 2.2.1-1
- Update to 2.2.1

* Thu Dec 14 2017 Sandro Mani <manisandro@gmail.com> - 2.2.0-2
- Add patch to fix FSF addresses
- Kill rpath

* Wed Dec 13 2017 Sandro Mani <manisandro@gmail.com> - 2.2.0-1
- Initial package
