# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global major   1

Name:           wslay
Version:        1.1.1
Release:        7%{?dist}
Summary:        Lightweight WebSocket library in C
License:        MIT
URL:            https://tatsuhiro-t.github.io/wslay
Source0:        https://github.com/tatsuhiro-t/wslay/archive/release-%{version}/%{name}-release-%{version}.tar.gz
# Patch from Debian: https://salsa.debian.org/debian/wslay
Patch0:         10_update_cmake.patch
# Fix build with cmake 4.0. Could be upstreamed but project unmaintained.
Patch1:         wslay-cmake4.0-compat.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
# For tests
BuildRequires:  pkgconfig(cunit)

%description
Wslay is a WebSocket library written in C. It implements the protocol
version 13 described in RFC 6455. This library offers 2 levels of API:
event-based API and frame-based low-level API.

For event-based API, it is suitable for non-blocking reactor pattern
style. You can set callbacks in various events.
For frame-based API, you can send WebSocket frame directly. Wslay only
supports data transfer part of WebSocket protocol and does not perform
opening handshake in HTTP.

%package devel
Summary:        Development headers and library for Wslay
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and library for the Wslay C WebSocket library.

%prep
%autosetup -p1 -n %{name}-release-%{version}

%build
%cmake -DWSLAY_EXAMPLES=NO
%cmake_build

%install
%cmake_install

# Create and install pkgconfig file
install -d %{buildroot}%{_libdir}/pkgconfig
cat << EOF > %{buildroot}%{_libdir}/pkgconfig/lib%{name}.pc
prefix=%{_prefix}
exec_prefix=\${prefix}
libdir=\${prefix}/%{_lib}
includedir=\${prefix}/include

Name: %{name}
Description: Lightweight WebSocket library in C
URL: %{url}
Version: %{version}
Libs: -L\${libdir} -l%{name}
Cflags: -I\${includedir}
EOF

%check
%{_vpath_builddir}/tests/wslay_tests

%files
%license AUTHORS COPYING
%{_libdir}/lib%{name}.so.%{major}
%{_libdir}/lib%{name}.so.%{version}

%files devel
%doc NEWS README.rst
%license AUTHORS COPYING
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc

%changelog
* Sun Jul 27 2025 Rémi Verschelde <akien@fedoraproject.org> - 1.1.1-7
- Patch config to support CMake 4.0 with min policy 3.5 (rhbz#2381635)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 09 2023 Rémi Verschelde <akien@fedoraproject.org> - 1.1.1-1
- Import Mageia package to Fedora

* Thu Mar 17 2022 Sysadmin Bot <umeabot@mageia.org> 1.1.1-2.mga9
+ Revision: 1796742
- Mageia 9 Mass Rebuild

* Thu Sep 17 2020 Rémi Verschelde <akien@mageia.org> 1.1.1-1.mga8
+ Revision: 1627505
- Version 1.1.1

* Sat Feb 15 2020 David GEIGER <daviddavid@mageia.org> 1.1.0-3.mga8
+ Revision: 1526883
- use new cmake macros
+ Sysadmin Bot <umeabot@mageia.org>
- Mageia 8 Mass Rebuild

* Wed Jul 03 2019 Rémi Verschelde <akien@mageia.org> 1.1.0-2.mga8
+ Revision: 1418030
- Rename pkgconfig file to libwslay to match openSUSE package

* Wed Jul 03 2019 Rémi Verschelde <akien@mageia.org> 1.1.0-1.mga8
+ Revision: 1418023
- imported package wslay
