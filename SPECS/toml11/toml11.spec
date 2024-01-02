# Header-only library, so no debug package
%global debug_package %{nil}

Summary:        toml11 - header-only C++11 TOML parser/generator
Name:           toml11
Version:        3.7.1
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/ToruNiina/toml11
Group:          System Environment
Vendor:         Microsoft Corporation
Distribution:   Mariner

#Source0:       https://github.com/ToruNiina/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  boost-devel

%description
A modern C++ toml library.

%package devel
Summary:        Development files for %{name}

%description devel
Development files for %{name}

%prep
%setup

# Remove tests which require boost 1.67
sed -E -e '/test_get|test_get_or|test_find|test_find_or/d' \
    -i tests/CMakeLists.txt

# Remove tests which rely on external toml file database
sed -E -e '/test_parse_file|test_serialize_file|test_parse_unicode/d' \
    -i tests/CMakeLists.txt

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
%license LICENSE
%{_includedir}/toml
%{_includedir}/toml.hpp
%{_libdir}/cmake/toml11

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.7.1-1
- Auto-upgrade to 3.7.1 - Azure Linux 3.0 - package upgrades

*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.7.0-2
-   Removing the explicit %%clean stage.

*   Fri Nov 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.7.0-1
-   Update to version 3.7.0 to fix GCC 11 building issues.
*   Wed Oct 14 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.3.0-2
-   License verified.
-   Fixed 'URL' tag.
-   Added source URL.
*   Tue Feb 11 2020 Nick Bopp <nichbop@microsoft.com> 3.3.0-1
-   Original version for CBL-Mariner.