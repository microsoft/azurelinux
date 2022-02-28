Vendor:         Microsoft Corporation
Distribution:   Mariner
%global debug_package   %{nil}

Name:           PEGTL
Version:        2.8.3
Release:        2%{?dist}
Summary:        Parsing Expression Grammar Template Library
License:        MIT
URL:            https://github.com/taocpp/%{name}/
Source0:        https://github.com/taocpp/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires: /usr/bin/make

Patch0: PEGTL-compiler-warning.patch

%description
The Parsing Expression Grammar Template Library (PEGTL) is a zero-dependency
C++11 header-only library for creating parsers according to a Parsing
Expression Grammar (PEG).

%package devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
Provides:       %{name} = %{version}-%{release}
Requires:       libstdc++-devel

%description devel
The %{name}-devel package contains C++ header files for developing
applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1 -b .compiler

%check
make

%install
install -d -m 0755 %{buildroot}%{_includedir}
pushd include/
cp -R tao/ %{buildroot}%{_includedir}
popd

%files devel
%doc README.md doc/
%license LICENSE
%{_includedir}/tao/pegtl.hpp
%{_includedir}/tao/pegtl

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.8.3-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Thu Sep 03 2020 Attila Lakatos <alakatos@redhat.com> - 2.8.3-1
- Update to 2.8.3
Resolves: rhbz#1742557

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Orion Poplawski <orion@nwra.com> - 2.8.1-1
- Update to 2.8.1

* Wed Jul 31 2019 Daniel Kopecek <dkopecek@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 Daniel Kopecek <dkopecek@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 14 2016 Daniel Kopecek <dkopecek@redhat.com> - 1.3.1-1
- Initial package
