Summary:        A fast JSON parser/generator for C++ with both SAX/DOM style API
Name:           rapidjson
Version:        1.1.0
Release:        7%{?dist}
License:        BSD and JSON and MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/Tencent/rapidjson
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0000-Supress-implicit-fallthrough-in-GCC.patch
Patch1:         0001-Onley-apply-to-GCC-7.patch
Patch2:         0002-Correct-object-copying-in-document_h.patch
%global debug_package %{nil}
BuildRequires:  cmake
BuildRequires:  gcc

%description
RapidJSON is a JSON parser and generator for C++. It was inspired by RapidXml.

%package devel
Summary:        Fast JSON parser and generator for C++
Group:          Development/Libraries/C and C++
Provides:       %{name} = %{version}-%{release}

%description devel
RapidJSON is a header-only JSON parser and generator for C++.
This package contains development headers and examples.

%prep
%autosetup -p 1

%build
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DBUILD_SHARED_LIBS=ON ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install

%check
make test

%files devel
%defattr(-,root,root)
%license license.txt
%dir %{_libdir}/cmake/RapidJSON
%{_libdir}/cmake/RapidJSON/*
%{_libdir}/pkgconfig/*.pc
%{_includedir}
%{_datadir}

%changelog
* Mon Apr 11 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.0-7
- Fixing invalid source URL.
- License verified.

* Mon Oct 12 2020 Olivia Crain <oliviacrain@microsoft.com> - 1.1.0-6
- Update Source0
- Licenses verified, added %%license macro

* Fri May 08 2020 Jonathan Chiu <jochi@microsoft.com> - 1.1.0-5
- Fix build failure with gcc 9

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.1.0-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Nov 19 2018 Vasavi Sirnapalli <vsirnapalli@vmware.com> - 1.1.0-3
- Fix makecheck

* Wed Aug 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 1.1.0-2
- Fix build failure with gcc 7.3

* Fri Jun 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 1.1.0-1
- Initial build. First version
