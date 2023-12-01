%global libx11_min_ver 1.5.99.902
Summary:        X.Org X11 libXinerama runtime library
Name:           libXinerama
Version:        1.1.4
Release:        7%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.x.org
Source0:        http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libX11-devel >= %{libx11_min_ver}
BuildRequires:  libXext-devel
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  xorg-x11-util-macros
Requires:       libX11 >= %{libx11_min_ver}

%description
X.Org X11 libXinerama runtime library

%package        devel
Summary:        X.Org X11 libXinerama development package
Requires:       %{name} = %{version}-%{release}

%description devel
X.Org X11 libXinerama development package

%prep
%autosetup

%build
autoreconf -v --install --force

%configure --disable-static
%make_build

%install

%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%ldconfig_scriptlets

%files
%license COPYING
%{_libdir}/libXinerama.so.1
%{_libdir}/libXinerama.so.1.0.0

%files devel
%{_libdir}/libXinerama.so
%{_libdir}/pkgconfig/xinerama.pc
%{_mandir}/man3/*.3*
%{_includedir}/X11/extensions/Xinerama.h
%{_includedir}/X11/extensions/panoramiXext.h

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.1.4-7
- License verified
- Lint spec

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.4-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Adam Jackson <ajax@redhat.com> - 1.1.4-1
- libXinerama 1.1.4

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 1.1.3-11
- Use ldconfig scriptlet macros

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.1.3-1
- libXinerama 1.1.3
