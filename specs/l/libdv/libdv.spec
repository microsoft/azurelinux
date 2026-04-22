# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libdv
Version:        1.0.0
Release: 46%{?dist}
Summary:        Software decoder for DV format video
License:        LGPL-2.0-or-later
URL:            http://libdv.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Patch1:         %{name}-no-exec-stack.patch
Patch2:         %{name}-pic.patch
Patch3:         %{name}-gtk2.patch
Patch4:         %{name}-dso-linking.patch
Patch5:         %{name}-gcc14.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pkgconfig(glib-2.0) >= 2.1.0
BuildRequires:  pkgconfig(gtk+-x11-2.0) >= 2.1.0
BuildRequires:  libtool
BuildRequires:  libXt-devel
BuildRequires:  libXv-devel
BuildRequires:  make
BuildRequires:  popt-devel
BuildRequires:  SDL-devel

%description
The Quasar DV codec (libdv) is a software codec for DV video, the encoding
format used by most digital camcorders, typically those that support the IEEE
1394 (a.k.a. FireWire or i.Link) interface. libdv was developed according to the
official standards for DV video: IEC 61834 and SMPTE 314M.

%package tools
Summary:        Basic tools to manipulate Digital Video streams
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains some basic programs to display and encode digital video
streams. This programs uses the Quasar DV codec (libdv), a software codec for DV
video, the encoding format used by most digital camcorders, typically those that
support the IEEE 1394 (a.k.a. FireWire or i.Link) interface.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%autosetup -p1 

%build
autoreconf -vif
%configure --with-pic --disable-static
%make_build

%install
%make_install
find %{buildroot} -name "*.la" -delete

%{?ldconfig_scriptlets}

%files
%doc ChangeLog
%license COPYING COPYRIGHT
%{_libdir}/%{name}.so.4
%{_libdir}/%{name}.so.4.0.3

%files tools
%doc README.* AUTHORS
%{_bindir}/dubdv
%{_bindir}/dvconnect
%{_bindir}/encodedv
%{_bindir}/playdv
%{_mandir}/man1/dubdv.1*
%{_mandir}/man1/dvconnect.1*
%{_mandir}/man1/encodedv.1*
%{_mandir}/man1/playdv.1*

%files devel
%{_includedir}/%{name}/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 17 2024 Antonio Trande <sagitter@fedoraproject.org> - 1.0.0-42
- Update libdv-pic patch for GCC-14 (rhbz#2261310)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar 24 2022 Simone Caronni <negativo17@gmail.com> - 1.0.0-36
- Clean up SPEC file.
- Trim changelog.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
