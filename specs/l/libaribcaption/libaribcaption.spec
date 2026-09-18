# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libaribcaption
Version:        1.1.1
Release:        3%{?dist}
Summary:        Portable ARIB STD-B24 Caption Decoder/Renderer
License:        MIT
URL:            https://github.com/xqq/libaribcaption

Source0:        %url/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         %{name}-version.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(fontconfig)

%description
Decoder and renderer for handling ARIB STD-B24 based broadcast captions, making
it possible for general players to render ARIB captions with the same effect
(or even better) as Television.

Features
- Support captions in Japanese (ARIB STD-B24 JIS), Latin languages (ABNT NBR
  15606-1) and Philippine (ARIB STD-B24 UTF-8)
- Full support for rendering ARIB additional symbols (Gaiji) and DRCScharacters
- Lightweight and portable implementation that works on various platforms
- Performance optimized (SSE2 on x86/x64) graphics rendering
- Multiple text rendering backend driven by DirectWrite / CoreText / FreeType
- Zero third-party dependencies on Windows (using DirectWrite) and macOS / iOS
  (using CoreText)
- Built-in font fallback mechanism
- Built-in DRCS converting table for replacing / rendering known DRCS characters
  into / by alternative Unicode

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkg-config

%description    devel
Decoder and renderer for handling ARIB STD-B24 based broadcast captions, making
it possible for general players to render ARIB captions with the same effect
(or even better) as Television.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/aribcaption/*
%{_libdir}/cmake/aribcaption/aribcaption-*.cmake
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 13 2024 Simone Caronni <negativo17@gmail.com> - 1.1.1-1
- First build.
