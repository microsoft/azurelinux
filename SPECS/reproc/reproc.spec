%global commit 1c07bdbec3f2ecba7125b9499b9a8a77bf9aa8c7
%global shortcommit %(c=%commit; echo ${c:0:7})

Summary:        A cross-platform (C99/C++11) process library
Name:           reproc
Version:        14.2.4
Release:        6%{?dist}
License:        MIT 
URL:            https://github.com/DaanDeMeyer/reproc
Source0:        https://github.com/DaanDeMeyer/reproc/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
reproc (Redirected Process) is a cross-platform C/C++ library that simplifies
starting, stopping and communicating with external programs. The main use case
is executing command line applications directly from C or C++ code and
retrieving their output.

reproc consists out of two libraries: reproc and reproc++. reproc is a C99
library that contains the actual code for working with external programs.
reproc++ depends on reproc and adapts its API to an idiomatic C++11 API. It
also adds a few extras that simplify working with external programs from C++.


%package        devel
Summary:        Development files for %{name}
License:        MIT
Requires:       %{name} = %{version}-%{release}
Requires:       cmake-filesystem
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{commit}


%build
%cmake -DREPROC++=ON -DREPROC_TEST=ON
%cmake_build


%install
%cmake_install

%check
%ctest


%files
%doc CHANGELOG.md README.md
%license LICENSE
%{_libdir}/*.so.14*

%files devel
%{_includedir}/reproc/
%{_includedir}/reproc++/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/reproc/
%{_libdir}/cmake/reproc++/


%changelog
* Mon Apr 14 2025 Riken Maharjan <rmaharjan@microsoft.com> - 14.2.4-6
- Initial Azure Linux import from Fedora 42 (license: MIT)
- License Verified

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 14.2.4-5.20230609git1c07bdb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14.2.4-4.20230609git1c07bdb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14.2.4-3.20230609git1c07bdb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14.2.4-2.20230609git1c07bdb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 04 2023 Orion Poplawski <orion@nwra.com> - 14.2.4-1.20230609git1c07bdb
- Update to 14.2.4 + latest git (FTBFS bz#2171704)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 16 2021 Orion Poplawski <orion@nwra.com> - 14.2.2-1
- Initial package
