%global richname QR-Code-generator
%global cmakename qrcodegen-cmake
%global cmakesuffix cmake2

Name: 		qr-code-generator
Version: 	1.8.0
Release: 	12%{?dist}
License: 	MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: 	High-quality QR Code generator library
URL: 		https://github.com/nayuki/%{richname}
Source0: 	%{url}/archive/refs/tags/v1.8.0.tar.gz#/%{name}-%{version}.tar.gz
Source1: 	https://github.com/EasyCoding/%{cmakename}/archive/v%{version}-%{cmakesuffix}/%{cmakename}-%{version}-%{cmakesuffix}.tar.gz
BuildRequires: 	cmake
BuildRequires: 	gcc
BuildRequires: 	gcc-c++
BuildRequires: 	ninja-build
BuildRequires: 	python3-devel
BuildRequires: 	python3-setuptools

%description
This project aims to be the best, clearest QR Code generator library in
multiple languages.

The primary goals are flexible options and absolute correctness.
Secondary goals are compact implementation size and good documentation
comments.

%package -n libqrcodegen
Summary: High-quality QR Code generator library (plain C version)

%description -n libqrcodegen
This project aims to be the best, clearest QR Code generator library in
multiple languages.

The primary goals are flexible options and absolute correctness.
Secondary goals are compact implementation size and good documentation
comments.

%package -n libqrcodegen-devel
Summary: Development files for libqrcodegen
Requires: libqrcodegen%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n libqrcodegen-devel
Development files and headers for high-quality QR Code generator library
(plain C version).

%package -n libqrcodegencpp
Summary: High-quality QR Code generator library (C++ version)

%description -n libqrcodegencpp
This project aims to be the best, clearest QR Code generator library in
multiple languages.

The primary goals are flexible options and absolute correctness.
Secondary goals are compact implementation size and good documentation
comments.

%package -n libqrcodegencpp-devel
Summary: Development files for libqrcodegencpp
Requires: libqrcodegencpp%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n libqrcodegencpp-devel
Development files and headers for high-quality QR Code generator library
(C++ version).

%package -n python3-qrcodegen
Summary: High-quality QR Code generator library (Python version)
BuildArch: noarch
%{?python_provide:%python_provide python3-qrcodegen}

%description -n python3-qrcodegen
This project aims to be the best, clearest QR Code generator library in
multiple languages.

The primary goals are flexible options and absolute correctness.
Secondary goals are compact implementation size and good documentation
comments.

%prep
%autosetup -n %{richname}-%{version}

# Unpacking CMake build script and assets...
tar -xf %{SOURCE1} %{cmakename}-%{version}-%{cmakesuffix}/cmake %{cmakename}-%{version}-%{cmakesuffix}/CMakeLists.txt --strip=1

%build
# Building C and C++ versions...
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTS:BOOL=ON
%cmake_build

# Building Python version...
pushd python
%py3_build
popd

%check
%ctest

%install
# Installing C and C++ versions...
%cmake_install

# Installing Python version...
pushd python
%py3_install
popd

# Installing a legacy symlink for compatibility...
ln -s qrcodegen.hpp %{buildroot}%{_includedir}/qrcodegencpp/QrCode.hpp

%files -n libqrcodegen
%license Readme.markdown
%{_libdir}/libqrcodegen.so.1*

%files -n libqrcodegen-devel
%{_includedir}/qrcodegen/
%{_libdir}/cmake/qrcodegen/
%{_libdir}/libqrcodegen.so
%{_libdir}/pkgconfig/qrcodegen.pc

%files -n libqrcodegencpp
%license Readme.markdown
%{_libdir}/libqrcodegencpp.so.1*

%files -n libqrcodegencpp-devel
%{_includedir}/qrcodegencpp/
%{_libdir}/cmake/qrcodegencpp/
%{_libdir}/libqrcodegencpp.so
%{_libdir}/pkgconfig/qrcodegencpp.pc

%files -n python3-qrcodegen
%license Readme.markdown
%{python3_sitelib}/qrcodegen.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/qrcodegen-*.egg-info/

%changelog
* Wed Dec 18 2024 Akhila Guruju <v-guakhila@microsoft.com> - 1.8.0-12
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.8.0-10
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.8.0-6
- Rebuilt for Python 3.12

* Sat Apr 22 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1.8.0-5
- Fixed namespaced targets detection.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.8.0-2
- Rebuilt for Python 3.11

* Mon Apr 18 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.8.0-1
- Updated to version 1.8.0.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 02 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.7.0-2
- Enabled pkgconfig and CMake configs support.
- Enabled unit tests.
- Added a legacy symlink for compatibility.

* Mon Aug 09 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.7.0-1
- Updated to version 1.7.0.
- Switched to CMake build system.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.6.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.6.0-1
- Updated to version 1.6.0.

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-3.20191014git67c6246
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2.20191014git67c6246
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.0-1.20191014git67c6246
- Initial SPEC release.
