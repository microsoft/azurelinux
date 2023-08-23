Summary:  A Simple INI file parser library
Name:     inih
Version:  57
Release:  1%{?dist}
License:  BSD
URL:      https://github.com/benhoyt/inih
Source0:  https://github.com/benhoyt/%{name}/archive/refs/tags/r%{version}.tar.gz#/%{name}-r%{version}.tar.gz
Vendor:   Microsoft Corporation
Distribution:   Mariner
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: meson


%description
The inih package provides simple INI file parser which is only a couple of
pages of code, and it was designed to be small and simple, so it's good for
embedded systems.


%package devel
Summary:  Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}


%description devel
This package contains development files for %{name}.

The inih package provides simple INI file parser which is only a couple of
pages of code, and it was designed to be small and simple, so it's good for
embedded systems.


%prep
%autosetup -n %{name}-r%{version}


%build
%meson
%meson_build


%install
%meson_install


%ldconfig_scriptlets


%files
%license LICENSE.txt
%doc README.md
%{_libdir}/lib%{name}.so.0
%{_libdir}/libINIReader.so.0


%files devel
%{_includedir}/ini.h
%{_includedir}/INIReader.h
%{_libdir}/pkgconfig/inih.pc
%{_libdir}/pkgconfig/INIReader.pc
%{_libdir}/lib%{name}.so
%{_libdir}/libINIReader.so


%changelog
* Fri Jul 28 2023 Andy Zaugg <azaugg@linkedin.com> - 57-1
- Updated version to 57
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified

* Wed Jul 13 2022 Robert Scheck <robert@fedoraproejct.org> - 56-1
- New upstream release 56 (#2106574)

* Sat Apr 23 2022 Robert Scheck <robert@fedoraproejct.org> - 55-1
- New upstream release 55 (#1920254)
- Re-add ldconfig scriptlets for EPEL 7 (#2066538)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 49-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 49-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun  3 2020 Christian Kellner <ckellner@redhat.com> - 49-1
- New upstream release 49
- Switch to meson build system.
- Ship the pkg-config file.
- Remove ldconfig scriptlets.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 36-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 36-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 36-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 36-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 36-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 36-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 36-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 36-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 31 2016 Jan F. Chadima <jfch@jagda.eu> - 36-5
- implement license tag

* Wed Aug 31 2016 Jan F. Chadima <jfch@jagda.eu> - 36-4
- implement next review hints

* Tue Aug 30 2016 Jan F. Chadima <jfch@jagda.eu> - 36-3
- implement another review results

* Tue Aug 30 2016 Jan F. Chadima <jfch@jagda.eu> - 36-2
- implement review results

* Mon Aug 29 2016 Jan F. Chadima <jfch@jagda.eu> - 36-1
- initial version
