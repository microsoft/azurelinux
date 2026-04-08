# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global wayland_min_version 1.4
%global debug_package %{nil}

Name:    plasma-wayland-protocols
Version: 1.20.0
Release: 1%{?dist}
Summary: Plasma Specific Protocols for Wayland

License: BSD-3-Clause AND CC0-1.0 AND LGPL-2.1-or-later AND MIT-CMU
URL:     https://invent.kde.org/libraries/%{name}

Source0: https://download.kde.org/stable/%{name}/%{name}-%{version}.tar.xz

## upstream patches (lookaside cache)
BuildRequires:  kf6-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version} -p1


%build
%cmake_kf6
%cmake_build


%install
%cmake_install


%files
%license LICENSES/* COPYING.LIB
%{_kf6_datadir}/plasma-wayland-protocols/

%files devel
%{_kf6_datadir}/cmake/PlasmaWaylandProtocols/


%changelog
* Tue Jan 13 2026 Steve Cossette <farchord@gmail.com> - 1.20.0-1
- 1.20.0

* Wed Sep 24 2025 Steve Cossette <farchord@gmail.com> - 1.19.0-1
- 1.19.0

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu May 15 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1.18.0-1
- 1.18.0

* Fri Mar 21 2025 Alessandro Astone <ales.astone@gmail.com> - 1.17.0-1
- new version

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1.16.0-1
- 1.16.0

* Sat Dec 07 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1.15.0-1
- 1.15.0

* Thu Sep 12 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1.14.0-1
- 1.14.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 24 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1.13.0-1
- 1.13.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 07 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1.12.0-1
- 1.12.0

* Sun Dec 03 2023 Justin Zobel <justin.zobel@gmail.com> - 1.11.1-1
- Update to 1.11.1

* Tue Nov 7 2023 Steve Cossette <farchord@gmail.com> - 1.11.0-1
- 1.11.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Marc Deop <marcdeop@fedoraproject.org> - 1.10.0-1
- 1.10.0

* Thu Jan 19 2023 Marc Deop <marcdeop@fedoraproject.org> - 1.10-1
- 1.10

* Wed Sep 28 2022 Rex Dieter <rdieter@gmail.com> - 1.9.0-1
- 1.9.0

* Tue Sep 06 2022 Marc Deop <marcdeop@fedoraproject.org> - 1.8.0-1
- 1.8.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 11 2022 Marc Deop marcdeop@fedoraproject.org - 1.7.0-1
- 1.7.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Marc Deop <marcdeop@fedoraproject.org> - 1.6.0-1
- 1.6.0

* Wed Nov 10 2021 Rex Dieter <rdieter@fedoraproject.org> - 1.5.0-1

* Wed Sep 15 2021 Marc Deop <marcdeop@fedoraproject.org> - 1.4.0-1
- 1.4.0

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 07 2021 Rex Dieter <rdieter@fedoraproject.org> - 1.3.0-1
- 1.3.0

* Mon Apr 05 2021 Rex Dieter <rdieter@fedoraproject.org> - 1.2.1-1
- v1.2.1

* Tue Mar 30 2021 Rex Dieter <rdieter@fedoraproject.org> - 1.2.0-2
- pull in upstream fix so internal version is consistent

* Sat Mar 27 2021 Rex Dieter <rdieter@fedoraproject.org> - 1.2.0-1
- 1.2.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Jan Grulich <jgrulich@redhat.com> - 1.1.1-1
- 1.1.1

* Sat Jul 25 2020 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-1
- 1.1.0

* Tue Jun 9 2020 Martin Kyral <martin.kyral@gmail.com> - 5.19.0-1
- 5.19.0

* Fri May 22 2020 Martin Kyral <martin.kyral@gmail.com> - 1.0-1
- 1.0
