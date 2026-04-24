# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# -*-Mode: rpm-spec -*-

Name:     aml
Version:  0.3.0
Release: 9%{?dist}
Summary:  Another Main Loop
# main source is ISC
# include/sys/queue.h is BSD
# Automatically converted from old format: ISC and BSD - review is highly recommended.
License:  ISC AND LicenseRef-Callaway-BSD

URL:      https://github.com/any1/aml
Source:   %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: meson

%description

Event loop handler developed for wayvnc (Wayland VNC server) and
wlvncc (Wayland VNC client) - see https://github.com/any1

Goals:
 * Portability
 * Utility
 * Simplicity

Non-goals:
 * MS Windows (TM) support
 * Solving the C10K problem

Features:
 * File descriptor event handlers
 * Timers
 * Tickers
 * Signal handlers
 * Idle dispatch callbacks
 * Thread pool
 * Interoperability with other event loops

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
This package contains header files for %{name}.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

%files
%{_libdir}/lib%{name}.so.0*

%doc README.md

%license COPYING

%files devel
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 0.3.0-6
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 31 2023 Bob Hepple <bob.hepple@gmail.com> - 0.3.0-1
- new version

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 10 2022 Bob Hepple <bob.hepple@gmail.com> - 0.2.2-1
- new version

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 04 2021 Bob Hepple <bob.hepple@gmail.com> - 0.2.0-1
- new version

* Tue Aug 04 2020 Bob Hepple <bob.hepple@gmail.com> - 0.1.0-3
- rebuilt

* Sun Aug 02 2020 Bob Hepple <bob.hepple@gmail.com> - 0.1.0-2
- improv description

* Tue Jul 28 2020 Bob Hepple <bob.hepple@gmail.com> - 0.1.0-1
- Initial version of the package
