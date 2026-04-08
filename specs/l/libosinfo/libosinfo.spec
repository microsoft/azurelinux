## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 5;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# -*- rpm-spec -*-

%define with_mingw 0
%if 0%{?fedora}
    %define with_mingw 0%{!?_without_mingw:1}
%endif

Summary: A library for managing OS information for virtualization
Name: libosinfo
Version: 1.12.0
Release: %autorelease
License: LGPL-2.1-or-later
Source: https://releases.pagure.org/%{name}/%{name}-%{version}.tar.xz
URL: https://libosinfo.org/

BuildRequires: meson
BuildRequires: gcc
BuildRequires: gtk-doc
BuildRequires: gettext-devel
BuildRequires: glib2-devel
BuildRequires: libxml2-devel >= 2.6.0
BuildRequires: libxslt-devel >= 1.0.0
%if 0%{?fedora} >= 37 || 0%{?rhel} >= 10
BuildRequires: libsoup3-devel
%else
BuildRequires: libsoup-devel
%endif
BuildRequires: vala
BuildRequires: perl-podlators
BuildRequires: hwdata
BuildRequires: gobject-introspection-devel
BuildRequires: osinfo-db
BuildRequires: git
Requires: gobject-introspection
Requires: hwdata
Requires: osinfo-db
Requires: osinfo-db-tools

%if %{with_mingw}
BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc
BuildRequires: mingw32-binutils
BuildRequires: mingw32-glib2
BuildRequires: mingw32-libxml2
BuildRequires: mingw32-libxslt
BuildRequires: mingw32-libsoup

BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc
BuildRequires: mingw64-binutils
BuildRequires: mingw64-glib2
BuildRequires: mingw64-libxml2
BuildRequires: mingw64-libxslt
BuildRequires: mingw64-libsoup
%endif

%description
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

%package devel
Summary: Libraries, includes, etc. to compile with the libosinfo library
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: glib2-devel
# -vala subpackage removed in F30
Obsoletes: libosinfo-vala < 1.3.0-3
Provides: libosinfo-vala = %{version}-%{release}

%description devel
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

Libraries, includes, etc. to compile with the libosinfo library

%if %{with_mingw}
%package -n mingw32-libosinfo
Summary: %{summary}
BuildArch: noarch

Requires: pkgconfig
Requires: mingw32-osinfo-db
Requires: mingw32-osinfo-db-tools

%description -n mingw32-libosinfo
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

%package -n mingw64-libosinfo
Summary: %{summary}
BuildArch: noarch

Requires: pkgconfig
Requires: mingw64-osinfo-db
Requires: mingw64-osinfo-db-tools

%description -n mingw64-libosinfo
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

%{?mingw_debug_package}
%endif

%prep
%autosetup -S git

%build
%meson \
    -Denable-gtk-doc=true \
    -Denable-tests=true \
    -Denable-introspection=enabled \
    -Denable-vala=enabled
%meson_build

%if %{with_mingw}
%mingw_meson \
    -Denable-gtk-doc=false \
    -Denable-tests=false \
    -Denable-introspection=disabled \
    -Denable-vala=disabled
%mingw_ninja
%endif

%install
%meson_install

%find_lang %{name}

%if %{with_mingw}
%mingw_ninja_install

# Remove static libraries but DON'T remove *.dll.a files.
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/libosinfo-1.0.a
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/libosinfo-1.0.a

# Libtool files don't need to be bundled
find $RPM_BUILD_ROOT -name "*.la" -delete

# Manpages don't need to be bundled
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/man
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/man

rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/gtk-doc
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/gtk-doc

%mingw_debug_install_post

%mingw_find_lang libosinfo
%endif

%check
%meson_test

%ldconfig_scriptlets

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING.LIB NEWS README
%{_bindir}/osinfo-detect
%{_bindir}/osinfo-query
%{_bindir}/osinfo-install-script
%{_mandir}/man1/osinfo-detect.1*
%{_mandir}/man1/osinfo-query.1*
%{_mandir}/man1/osinfo-install-script.1*
%{_libdir}/%{name}-1.0.so.*
%{_libdir}/girepository-1.0/Libosinfo-1.0.typelib

%files devel
%{_libdir}/%{name}-1.0.so
%dir %{_includedir}/%{name}-1.0/
%dir %{_includedir}/%{name}-1.0/osinfo/
%{_includedir}/%{name}-1.0/osinfo/*.h
%{_libdir}/pkgconfig/%{name}-1.0.pc
%{_datadir}/gir-1.0/Libosinfo-1.0.gir
%{_datadir}/gtk-doc/html/Libosinfo

%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libosinfo-1.0.deps
%{_datadir}/vala/vapi/libosinfo-1.0.vapi

%if %{with_mingw}
%files -n mingw32-libosinfo -f mingw32-libosinfo.lang
%doc AUTHORS ChangeLog COPYING.LIB NEWS README
%{mingw32_bindir}/osinfo-detect.exe
%{mingw32_bindir}/osinfo-install-script.exe
%{mingw32_bindir}/osinfo-query.exe
%{mingw32_bindir}/libosinfo-1.0-0.dll
%{mingw32_libdir}/libosinfo-1.0.dll.a
%{mingw32_libdir}/pkgconfig/libosinfo-1.0.pc
%dir %{mingw32_includedir}/libosinfo-1.0/
%dir %{mingw32_includedir}/libosinfo-1.0/osinfo
%{mingw32_includedir}/libosinfo-1.0/osinfo/*.h
%dir %{mingw32_datadir}/libosinfo
%{mingw32_datadir}/libosinfo/usb.ids
%{mingw32_datadir}/libosinfo/pci.ids

%files -n mingw64-libosinfo -f mingw64-libosinfo.lang
%doc AUTHORS ChangeLog COPYING.LIB NEWS README
%{mingw64_bindir}/osinfo-detect.exe
%{mingw64_bindir}/osinfo-install-script.exe
%{mingw64_bindir}/osinfo-query.exe
%{mingw64_bindir}/libosinfo-1.0-0.dll
%{mingw64_libdir}/libosinfo-1.0.dll.a
%{mingw64_libdir}/pkgconfig/libosinfo-1.0.pc
%dir %{mingw64_includedir}/libosinfo-1.0/
%dir %{mingw64_includedir}/libosinfo-1.0/osinfo
%{mingw64_includedir}/libosinfo-1.0/osinfo/*.h
%dir %{mingw64_datadir}/libosinfo
%{mingw64_datadir}/libosinfo/usb.ids
%{mingw64_datadir}/libosinfo/pci.ids
%endif

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.12.0-5
- Latest state for libosinfo

* Wed Feb 04 2026 Jelle van der Waa <jelle@vdwaa.nl> - 1.12.0-4
- Depend on gobject-introspection

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 29 2024 Victor Toso <victortoso@redhat.com> - 1.12.0-1
- Update to release v1.12.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Mar 28 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.11.0-6
- Fix perl-podlators dependency

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.11.0-3
- Fix build with libxml2-2.12.0

* Wed Dec 13 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.11.0-2
- Fix rpmautospec changelog

* Fri Oct 27 2023 Victor Toso <victortoso@redhat.com> - 1.11.0-1
- Update to release v1.11.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 09 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 1.10.0-6
- Use libsoup 3 in ELN

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug  8 2022 Daniel P. Berrangé <berrange@redhat.com> - 1.10.0-4
- Pull in mingw sub-packages

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Daniel P. Berrangé <berrange@redhat.com> - 1.10.0-2
- Switch from libsoup2 to libsoup3 (rhbz #2108589)

* Mon Feb 14 2022 Victor Toso <victortoso@redhat.com> - 1.10.0-1
- Update to 1.10.0 release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Cole Robinson <crobinso@redhat.com> - 1.9.0-3
- Fix build with glib 2.70

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 Fabiano Fidêncio <fidencio@redhat.com> - 1.9.0-1
- Update to 1.9.0 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

## END: Generated by rpmautospec
