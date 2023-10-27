%global debug_package %{nil}
Summary:        A single-file header-only version of a C++20-like span for C++98, C++11 and later
Name:           span-lite
Version:        0.10.3
Release:        1%{?dist}
License:        Boost
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment
URL:            https://github.com/martinmoene/span-lite
#Source0:       %{url}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc

%description
A single-file header-only version of a C++20-like span for C++98, C++11 and later.

%package devel
Summary:        Development files for %{name}

%description devel
Development files for %{name}

%prep
%autosetup

%build
mkdir build && cd build
%cmake ..
%make_build

%check
make test -C build

%install
%make_install -C build

%files devel
%defattr(-,root,root)
%doc README.md
%license LICENSE.txt
%{_includedir}/nonstd/span.hpp
%{_libdir}/cmake/span-lite

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.3-1
- Auto-upgrade to 0.10.3 - Azure Linux 3.0 - package upgrades

* Tue Feb 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.10.0-1
- Update version to 0.10.0.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.0-3
- Removing the explicit %%clean stage.

* Thu Oct 15 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.7.0-2
- License verified.
- Added source URL.

* Wed Aug 26 2020 Paco Huelsz Prince <frhuelsz@microsoft.com> 0.7.0-1
- Update to version 0.7.0.

* Tue Feb 11 2020 Nick Bopp <nichbop@microsoft.com> 0.6.0-1
- Original version for CBL-Mariner.
