Summary:        General-purpose library for the WPE-flavored port of WebKit
Name:           libwpe
Version:        1.12.0
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/WebPlatformForEmbedded/%{name}
Source0:        https://github.com/WebPlatformForEmbedded/libwpe/releases/download/%{version}/%{name}-%{version}.tar.xz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libxkbcommon-devel
BuildRequires:  mesa-libEGL-devel
Provides:       wpebackend = %{version}-%{release}
Obsoletes:      wpebackend < 0.2.0-2

%description
General-purpose library developed for the WPE-flavored port of WebKit

%package       devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description   devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.

%prep
%autosetup -p1 -n libwpe-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  ..
popd

%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%files
%license COPYING
%doc NEWS
%{_libdir}/libwpe-1.0.so.1.*
%{_libdir}/libwpe-1.0.so.1

%files devel
%{_includedir}/wpe-1.0/
%{_libdir}/libwpe-1.0.so
%{_libdir}/pkgconfig/wpe-1.0.pc

%changelog
* Sat May 14 2022 Sriram Nambakam <snambakam@microsoft.com> - 1.12.0-1
- Update to 1.12.0
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Mar 12 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Mon Mar 02 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 1.5.90-1
- Update to 1.5.90

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 18 2019 Chris King <bunnyapocalypse@protonmail.org> - 1.4.0-1
- New version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Chris King <bunnyapocalypse@protonmail.org> - 1.3.1-1
- New version

* Wed May 8 2019 Chris King <bunnyapocalypse@protonmail.org> - 1.3.0-1
- New version

* Mon Mar 25 2019 Chris King <bunnyapocalypse@protonmail.org> - 1.2.0-1
- New vsn with soname bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 27 2018 Chris King <bunnyapocalypse@protonmail.org> - 1.0.0-1
- Initial RPM package
