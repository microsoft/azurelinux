# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Header-only library
%global debug_package %{nil}

Name:           wayland-protocols
Version:        1.47
Release: 3%{?dist}
Summary:        Wayland protocols that adds functionality not available in the core protocol

License:        MIT
URL:            https://wayland.freedesktop.org/
Source0:        https://gitlab.freedesktop.org/wayland/%{name}/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gcc-g++
BuildRequires:  meson
BuildRequires:  wayland-devel

%description
wayland-protocols contains Wayland protocols that adds functionality not
available in the Wayland core protocol. Such protocols either adds
completely new functionality, or extends the functionality of some other
protocol either in Wayland core, or some other protocol in
wayland-protocols.

%package devel
Summary:        Wayland protocols that adds functionality not available in the core protocol
Provides:       %{name}-static = %{version}-%{release}
BuildArch:      noarch

%description devel
wayland-protocols contains Wayland protocols that adds functionality not
available in the Wayland core protocol. Such protocols either adds
completely new functionality, or extends the functionality of some other
protocol either in Wayland core, or some other protocol in
wayland-protocols.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

%files devel
%license COPYING
%doc README.md
%{_datadir}/pkgconfig/%{name}.pc
%{_datadir}/%{name}/
%{_includedir}/%{name}/

%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 15 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.47-1
- Update to 1.47

* Mon Nov 24 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.46-1
- Update to 1.46

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 13 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.45-1
- Update to 1.45

* Sun Apr 27 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.44-1
- Update to 1.44

* Tue Apr 08 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.43-1
- Update to 1.43

* Mon Mar 24 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.42-1
- Update to 1.42

* Mon Feb 17 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.41-1
- Update to 1.41

* Thu Jan 30 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.40-1
- Update to 1.40

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.39-1
- Update to 1.39

* Sat Oct 12 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.38-1
- Update to 1.38

* Sat Aug 31 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.37-1
- Update to 1.37

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 01 2024 Pavel Solovev <daron439@gmail.com> - 1.36-1
- Update to 1.36

* Thu Mar 21 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.34-1
- Update to 1.34

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.33-1
- Update to 1.33

* Mon Sep 11 2023 Olivier Fourdan <ofourdan@redhat.com> - 1.32-3
- migrated to SPDX license

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Kalev Lember <klember@redhat.com> - 1.32-1
- Update to 1.32 (rhbz#2219369)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Kalev Lember <klember@redhat.com> - 1.31-1
- Update to 1.31

* Mon Nov 21 2022 Kalev Lember <klember@redhat.com> - 1.30-1
- Update to 1.30

* Tue Nov 15 2022 Kalev Lember <klember@redhat.com> - 1.29-1
- Update to 1.29

* Sat Nov 05 2022 Kalev Lember <klember@redhat.com> - 1.28-1
- Update to 1.28

* Wed Oct 12 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.27-1
- Update to 1.27

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul  8 2022 Olivier Fourdan <ofourdan@redhat.com> - 1.26-1
- Update to 1.26

* Sat Feb 19 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.25-1
- Update to 1.25

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 27 2021 Neal Gompa <ngompa@fedoraproject.org> - 1.24-1
- Update to 1.24

* Mon Sep 20 2021 Neal Gompa <ngompa@fedoraproject.org> - 1.23-1
- Update to 1.23

* Mon Sep 20 2021 Neal Gompa <ngompa@fedoraproject.org> - 1.22-1
- Update to 1.22

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 04 2021 Kalev Lember <klember@redhat.com> - 1.21-1
- Update to 1.21
- Switch to meson build system

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Feb 29 2020 Jonas Ådahl <jadahl@redhat.com> - 1.20-1
- Update to 1.20

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jul 29 2019 Olivier Fourdan <ofourdan@redhat.com> - 1.18-1
- Update to 1.18

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 21 2018 Kalev Lember <klember@redhat.com> - 1.17-1
- Update to 1.17

* Tue Jul 31 2018 Kalev Lember <klember@redhat.com> - 1.16-1
- Update to 1.16

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Adam Jackson <ajax@redhat.com> - 1.15-1
- Update to 1.15

* Tue May 08 2018 Kalev Lember <klember@redhat.com> - 1.14-1
- Update to 1.14

* Thu Feb 15 2018 Kalev Lember <klember@redhat.com> - 1.13-1
- Update to 1.13

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 07 2017 Kalev Lember <klember@redhat.com> - 1.12-1
- Update to 1.12

* Wed Nov 15 2017 Kalev Lember <klember@redhat.com> - 1.11-1
- Update to 1.11

* Mon Jul 31 2017 Kalev Lember <klember@redhat.com> - 1.10-1
- Update to 1.10

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Kalev Lember <klember@redhat.com> - 1.9-1
- Update to 1.9

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 16 2016 Kalev Lember <klember@redhat.com> - 1.7-1
- Update to 1.7

* Fri Aug 12 2016 Kalev Lember <klember@redhat.com> - 1.6-1
- Update to 1.6

* Tue Jul 26 2016 Kalev Lember <klember@redhat.com> - 1.5-1
- Update to 1.5

* Tue May 24 2016 Kalev Lember <klember@redhat.com> - 1.4-1
- Update to 1.4

* Mon Apr 11 2016 Kalev Lember <klember@redhat.com> - 1.3-1
- Update to 1.3

* Mon Mar 07 2016 Kalev Lember <klember@redhat.com> - 1.2-1
- Update to 1.2

* Thu Feb 18 2016 Kalev Lember <klember@redhat.com> - 1.1-1
- Update to 1.1

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0-2
- Fix description

* Thu Nov 26 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0-1
- Update to released 1.0
- Move XMLs to devel pkg
- Drop non-interesting part of description

* Sun Nov 22 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.1.0-0.gitf828a43
- Initial package
