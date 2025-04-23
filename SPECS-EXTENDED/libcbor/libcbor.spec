Summary:        A CBOR parsing library
Name:           libcbor
Version:        0.11.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            http://libcbor.org
Source0:        https://github.com/PJK/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libcmocka
BuildRequires:  make
BuildRequires:  pkg-config
BuildRequires:  python-breathe
BuildRequires:  python-sphinx
BuildRequires:  python-sphinx_rtd_theme
# Jocelynb - Adding an explicit dependency on python3-sphinxcontrib-jquery as the Azure Linux version of python-sphinx does not include it.
BuildRequires:  python3-sphinxcontrib-jquery
BuildRequires:  pkgconfig(cmocka)

%description
libcbor is a C library for parsing and generating CBOR.

%package	devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{name}-devel contains development libraries and header files for %{name}.

%prep
%setup -q


%build
%cmake -DCMAKE_BUILD_TYPE=Release -DWITH_TESTS=ON
%cmake_build
cd doc
make man


%install
%cmake_install
mkdir -p %{buildroot}%{_mandir}/man3
cp doc/build/man/libcbor.3 %{buildroot}%{_mandir}/man3/


%check
%ctest


%files
%license LICENSE.md
%doc README.md
%{_libdir}/libcbor.so.0.11{,.*}

%files devel
%{_includedir}/cbor.h
%{_includedir}/cbor
%{_libdir}/libcbor.so
%{_libdir}/pkgconfig/libcbor.pc
%{_libdir}/cmake/libcbor
%{_mandir}/man3/libcbor.3{,.*}

%changelog
* Fri Oct 18 2024 Jocelyn Berrendonner <jocelynb@microsoft.com> - 0.11.0-3
- Integrating the spec into Azure Linux
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- License verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 0.11.0-1
- Update version to 0.11.0 ( resolves: rhbz#2262592 )
- add running of unit tests

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 30 2023 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 0.10.2-3
- Move devel/api manpage to devel package

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 07 2023 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 0.10.2-1
- Update to version 0.10.2 ( resolves: rhbz#1880885 )
- Revise specs per packaging guidelines for globs of soname

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 28 2022 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 0.7.0-8
- Update license to SPDX format
- spec file tidy/modernization
  - use modern cmake build and install
  - properly own include directories in the devel package
  - de-glob some files to follow packaging guidelines

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 15 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 0.7.0-6
- Add missing BR for doxygen

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Sep 20 2020 Kalev Lember <klember@redhat.com> - 0.7.0-2
- Avoid hardcoding man page extension

* Mon Sep 07 2020 Attila Lakatos <alakatos@redhat.com> - 0.7.0-1
- update to 0.7.0
Resolves: rhbz#1813738
Resolves: rhbz#1863978

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Feb 29 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 0.5.0-7
- Fix FTBFS, add version for soname, minor cleanups

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 19 2017 Marek Tamaskovic <mtamasko@redhat.com> 0.5.0-1
- Init package.
