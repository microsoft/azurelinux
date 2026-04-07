# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# -*-Mode: rpm-spec -*-

Name:     neatvnc
Version:  0.9.0
Release:  4%{?dist}
Summary:  Liberally licensed VNC server library
# main source is ISC
# include/sys/queue.h is BSD
License:  ISC AND BSD-2-Clause AND BSD-3-Clause

URL:      https://github.com/any1/neatvnc
Source:   %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Backport to fix i686 builds
# From: https://github.com/any1/neatvnc/commit/e0e0ce5c579cafc763992f1c1bb964eb95999fb7
Patch:    0001-server-Use-correct-type-for-length-in-compress.patch

BuildRequires: gcc
BuildRequires: git-core
BuildRequires: meson
BuildRequires: cmake
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavfilter)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(aml)
BuildRequires: pkgconfig(gnutls)
BuildRequires: pkgconfig(nettle)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(pixman-1)
BuildRequires: pkgconfig(zlib)
BuildRequires: turbojpeg-devel

%description
This is a liberally licensed VNC server library that's intended to be
fast and neat. Note: This is a beta release, so the interface is not
yet stable.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains header files for %{name}.

%prep
%autosetup -S git_am

%build
%meson
%meson_build

%install
%meson_install

%files
%doc README.md
%license COPYING
%{_libdir}/lib%{name}.so.0{,.*}

%files devel
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.9.0-2
- Backport fix for i686 builds

* Wed Nov 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0

* Mon Sep 23 2024 Fabio Valentini <decathorpe@gmail.com> - 0.8.1-3
- Rebuild for ffmpeg 7

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0.8.1-2
- convert license to SPDX

* Fri Aug 02 2024 Bob Hepple <bob.hepple@gmail.com> - 0.8.1-1
- new version RHBZ #2302449,2302450

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 29 2024 Bob Hepple <bob.hepple@gmail.com> - 0.8.0-2
- rebuilt

* Mon Feb 26 2024 Bob Hepple <bob.hepple@gmail.com> - 0.8.0-1
- new version

* Tue Feb 06 2024 František Zatloukal <fzatlouk@redhat.com> - 0.7.1-4
- Rebuilt for turbojpeg 3.0.2

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 05 2023 Bob Hepple <bob.hepple@gmail.com> - 0.7.1-1
- new version

* Fri Oct 06 2023 Bob Hepple <bob.hepple@gmail.com> - 0.7.0-1
- new version

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Mar 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.6.0-2
- Rebuild for ffmpeg 6.0

* Tue Jan 31 2023 Bob Hepple <bob.hepple@gmail.com> - 0.6.0-1
- new version

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 12 2022 Bob Hepple <bob.hepple@gmail.com> - 0.5.4-1
- new version

* Mon Aug 29 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.5.1-3
- Rebuild for ffmpeg 5.1 (#2121070)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 10 2022 Bob Hepple <bob.hepple@gmail.com> - 0.5.1-1
- new version

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 04 2021 Bob Hepple <bob.hepple@gmail.com> - 0.4.0-1
- new version

* Mon Sep 28 2020 Bob Hepple <bob.hepple@gmail.com> - 0.3.2-1
- new version

* Tue Sep 22 2020 Bob Hepple <bob.hepple@gmail.com> - 0.3.0-1
- new version

* Tue Aug 04 2020 Bob Hepple <bob.hepple@gmail.com> - 0.2.0-1
- new version

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 16 2020 Bob Hepple <bob.hepple@gmail.com> - 0.1.0-3
- fixed spelling of Unlicense

* Wed Apr 15 2020 Bob Hepple <bob.hepple@gmail.com> - 0.1.0-2
- fixed per review RHBZ#1824016

* Wed Apr 15 2020 Bob Hepple <bob.hepple@gmail.com> - 0.1.0-1
- Initial version of the package
