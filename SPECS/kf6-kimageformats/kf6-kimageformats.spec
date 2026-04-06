# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine __cmake_in_source_build
%global framework kimageformats

Name:           kf6-%{framework}
Version:        6.23.0
Release:        2%{?dist}
Summary:        KDE Frameworks 6 Tier 1 addon with additional image plugins for QtGui

License:        LGPLv2+
URL:            https://invent.kde.org/frameworks/%{framework}

Source0: http://download.kde.org/%{stable_kf6}/frameworks/%{majmin_ver_kf6}/%{framework}-%{version}.tar.xz
Source1: http://download.kde.org/%{stable_kf6}/frameworks/%{majmin_ver_kf6}/%{framework}-%{version}.tar.xz.sig

# upstream patches

BuildRequires:  extra-cmake-modules >= %{version}
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  kf6-rpm-macros
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(KF6Archive)
BuildRequires:  cmake(Qt6PrintSupport)
BuildRequires:  pkgconfig(cups)
BuildRequires:  cmake(OpenEXR)
BuildRequires:  cmake(libavif)
BuildRequires:  pkgconfig(libheif) >= 1.10.0
%if !((0%{?fedora} && 0%{?fedora} < 41) || (0%{?rhel} && 0%{?rhel} < 10))
BuildRequires:  pkgconfig(libjxl) >= 0.9.4
BuildRequires:  pkgconfig(libjxl_threads) >= 0.9.4
BuildRequires:  pkgconfig(libjxl_cms) >= 0.9.4
%endif
BuildRequires:  cmake(OpenJPEG)
BuildRequires:  pkgconfig(libraw) >= 0.20.2
BuildRequires:  pkgconfig(libraw_r) >= 0.20.2
BuildRequires:  jxrlib-devel

Requires:       kf6-filesystem
# for eps plugin read/write support
Recommends:     poppler-utils
Recommends:     ghostscript

%description
This framework provides additional image format plugins for QtGui.  As
such it is not required for the compilation of any other software, but
may be a runtime requirement for Qt-based software to support certain
image formats.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n %{framework}-%{version} -p1

%build
%cmake_kf6 \
  -DKIMAGEFORMATS_HEIF:BOOL=ON \
  -DKIMAGEFORMATS_JXR:BOOL=ON
%cmake_build

%install
%cmake_install

%files
%doc README.md
%license LICENSES/*.txt
%{_kf6_qtplugindir}/imageformats/*.so

%files devel
%{_kf6_libdir}/cmake/KF6ImageFormats/

%changelog
* Mon Feb 16 2026 Gwyn Ciesla <gwync@protonmail.com> - 6.23.0-2
- LibRaw rebuild

* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 6.23.0-1
- 6.23.0

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 02 2026 farchord@gmail.com - 6.22.0-1
- 6.22.0

* Fri Dec 05 2025 Steve Cossette <farchord@gmail.com> - 6.21.0-1
- 6.21.0

* Thu Nov 13 2025 Steve Cossette <farchord@gmail.com> - 6.20.0-1
- 6.20.0

* Sun Oct 05 2025 Steve Cossette <farchord@gmail.com> - 6.19.0-1
- 6.19.0

* Tue Sep 16 2025 farchord@gmail.com - 6.18.0-1
- 6.18.0

* Fri Aug 01 2025 Steve Cossette <farchord@gmail.com> - 6.17.0-1
- 6.17.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Steve Cossette <farchord@gmail.com> - 6.16.0-2
- Respun

* Sat Jul 05 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.16.0-1
- 6.16.0

* Tue Jun 17 2025 Marie Loise Nolden <loise@kde.org> - 6.15.0-2
- 6.15 and plasma 3.4 compatibility rebuild

* Sat Jun 07 2025 Steve Cossette <farchord@gmail.com> - 6.15.0-1
- 6.15.0

* Fri May 16 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 6.14.0-2
- Soften EPS dependencies

* Sat May 03 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.14.0-1
- 6.14.0

* Tue Apr 22 2025 Alessandro Astone <ales.astone@gmail.com> - 6.13.0-3
- Add corrective patch for the building the JXR plugin on i686

* Sat Apr 19 2025 Marie Loise Nolden <loise@kde.org> - 6.13.0-2
- cleanup BR, build openjpeg2 and libjxr plugins

* Sun Apr 06 2025 Steve Cossette <farchord@gmail.com> - 6.13.0-1
- 6.13.0

* Thu Mar 13 2025 Steve Cossette <farchord@gmail.com> - 6.12.0-2
- Rebuild for KDE respin

* Fri Mar 07 2025 Steve Cossette <farchord@gmail.com> - 6.12.0-1
- 6.12.0

* Fri Feb 07 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.11.0-1
- 6.11.0

* Sun Feb 02 2025 Sérgio Basto <sergio@serjux.com> - 6.10.0-3
- Rebuild for jpegxl (libjxl) 0.11.1

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Steve Cossette <farchord@gmail.com> - 6.10.0-1
- 6.10.0

* Sat Dec 14 2024 Steve Cossette <farchord@gmail.com> - 6.9.0-1
- 6.9.0

* Sat Nov 02 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.8.0-1
- 6.8.0

* Fri Oct 04 2024 Steve Cossette <farchord@gmail.com> - 6.7.0-1
- 6.7.0

* Mon Sep 16 2024 Steve Cossette <farchord@gmail.com> - 6.6.0-1
- 6.6.0

* Sat Aug 10 2024 Steve Cossette <farchord@gmail.com> - 6.5.0-1
- 6.5.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 06 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.4.0-1
- 6.4.0

* Sat Jun 01 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.0-1
- 6.3.0

* Sat May 04 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.2.0-1
- 6.2.0

* Wed Apr 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 6.1.0-3
- Rebuilt for openexr 3.2.4

* Thu Apr 11 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-2
- Backport patch from upstream to fix i686 compilation

* Wed Apr 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-1
- 6.1.0

* Wed Mar 13 2024 Sérgio Basto <sergio@serjux.com> - 6.0.0-3
- Rebuild for jpegxl (libjxl) 0.10.2

* Thu Feb 29 2024 Marie Loise Nolden <loise@kde.org> - 6.0.0-2
- add libheif plugin support

* Wed Feb 21 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Wed Feb 14 2024 Sérgio Basto <sergio@serjux.com> - 5.249.0-2
- Rebuild for jpegxl (libjxl) 0.9.2 with soname bump

* Wed Jan 31 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.249.0-1
- 5.249.0

* Wed Jan 31 2024 František Zatloukal <fzatlouk@redhat.com> - 5.248.0-4
- Rebuilt for libavif 1.0.3

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.248.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.248.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.248.0-1
- 5.248.0

* Wed Dec 20 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.247.0-1
- 5.247.0

* Sat Dec 02 2023 Justin Zobel <justin.zobel@gmail.com> - 5.246.0-1
- Update to 5.246.0

* Thu Nov 09 2023 Steve Cossette <farchord@gmail.com> - 5.245.0-1
- 5.245.0

* Tue Oct 03 2023 Steve Cossette <farchord@gmail.com> - 5.240.0^20230925.210237.d932e0d-1
- Initial Release
