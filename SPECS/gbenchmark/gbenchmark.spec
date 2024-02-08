%global intname benchmark
%global lbname lib%{intname}

Summary:        A microbenchmark support library
Name:           gbenchmark
Version:        1.8.3
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/google/%{intname}
Source0:        https://github.com/google/%{intname}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: gmock-devel
BuildRequires: gtest-devel
BuildRequires: ninja-build

%description
A library to support the benchmarking of functions, similar to unit-tests.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%package doc
Summary: Documentation for %{name}
BuildArch: noarch
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description doc
%{summary}.

%prep
%autosetup -n %{intname}-%{version} -p1
sed -e '/get_git_version/d' -e '/-Werror/d' -i CMakeLists.txt

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DGIT_VERSION=%{version} \
    -DBENCHMARK_ENABLE_DOXYGEN:BOOL=ON \
    -DBENCHMARK_ENABLE_TESTING:BOOL=ON \
    -DBENCHMARK_USE_BUNDLED_GTEST:BOOL=OFF \
    -DBENCHMARK_ENABLE_GTEST_TESTS:BOOL=ON \
    -DBENCHMARK_ENABLE_INSTALL:BOOL=ON \
    -DBENCHMARK_INSTALL_DOCS:BOOL=ON \
    -DBENCHMARK_DOWNLOAD_DEPENDENCIES:BOOL=OFF
%cmake_build

%check
%ctest

%install
%cmake_install

%files
%doc CONTRIBUTING.md README.md
%license AUTHORS CONTRIBUTORS LICENSE
%{_libdir}/%{lbname}*.so.1*

%files devel
%{_libdir}/%{lbname}*.so
%{_includedir}/%{intname}/
%{_libdir}/cmake/%{intname}/
%{_libdir}/pkgconfig/%{intname}.pc

%files doc
%{_docdir}/%{intname}/

%changelog
* Wed Jan 31 2024 Jon Slobodzian <joslobo@microsoft.com> - 1.8.3-1
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Upgraded to 1.8.3 from Fedora version
- License verified.

* Fri Nov 11 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.7.1-1
- Updated to version 1.7.1.

* Tue Jul 26 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.7.0-1
- Updated to version 1.7.0.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.6.2-1
- Updated to version 1.6.2.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.6.1-2
- Disabled skip_with_error_test test on Fedora 36 due to GCC 12 regression.

* Thu Jan 13 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.6.1-1
- Updated to version 1.6.1.

* Sun Sep 12 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.6.0-1
- Updated to version 1.6.0.

* Thu Aug 12 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.6-1
- Updated to version 1.5.6.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.5-3
- Rebuilt again for the same reason.

* Sat Jul 10 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.5-2
- Rebuilt due to glibc update.

* Sat Jun 12 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.5-1
- Updated to version 1.5.5.

* Mon May 31 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.4-1
- Updated to version 1.5.4.

* Mon Apr 26 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.3-1
- Updated to version 1.5.3.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 14 2020 Jeff Law <law@redhat.com> - 1.5.2-2
- Fix missing #include for gcc-11

* Sat Sep 12 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.2-1
- Updated to version 1.5.2.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 19 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.1-1
- Updated to version 1.5.1.
- Fixed RHBZ#1858127.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 28 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 1.5.0-1
- Updated to version 1.5.0.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 25 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.4.1-1
- Initial SPEC release.
