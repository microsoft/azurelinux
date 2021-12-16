Summary:        GSL: Guidelines Support Library
Name:           GSL
Version:        2.0.0
Release:        4%{?dist}
License:        MIT
Group:          Applications/File
URL:            https://github.com/Microsoft/GSL
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/microsoft/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  build-essential


%description
The Guidelines Support Library (GSL) contains functions and types that are suggested
for use by the C++ Core Guidelines maintained by the Standard C++ Foundation.
This repo contains Microsoft's implementation of GSL.

The library includes types like span<T>, string_span, owner<> and others.

The entire implementation is provided inline in the headers under the gsl directory.
The implementation generally assumes a platform that implements C++14 support.
There are specific workarounds to support MSVC 2015.

%global debug_package %{nil}

%prep
%setup

%build
mkdir -p cmake
cd cmake
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DGSL_TEST=OFF ..
cmake --build .

%install
cd cmake
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/cmake

%files
%defattr(-, root, root, -)
%license LICENSE
%dir %{_includedir}/gsl
%{_includedir}/gsl/*

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-4
- Removing the explicit %%clean stage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.0.0-3
- Added %%license line automatically

*   Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> 2.0.0-2
-   Update Source0 with valid URL.
-   Remove sha1 macro.
-   License verified.
*   Thu Dec 5 2019 Emre Girgin <mrgirgin@microsoft.com> 2.0.0-1
-   Original version for CBL-Mariner.
