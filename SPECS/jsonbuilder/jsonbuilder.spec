Summary:        Modern C++ library for an efficient container for building JSON objects
Name:           jsonbuilder
Version:        0.2.1
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment
URL:            https://github.com/microsoft/jsonbuilder
Source0:        https://github.com/microsoft/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Version 0.2.1 of 'jsonbuilder' is not compatible with the 3+ versions of 'catch'.
# Patch required until upstream switches a newer version of 'catch'.
# Related upstream issue: https://github.com/microsoft/jsonbuilder/issues/29.
Patch:          catch-ver3.patch
BuildRequires:  catch-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  util-linux-devel

%description
JsonBuilder is a small C++ library for building a space-efficient binary representation of structured data and,
when ready, rendering it to JSON. The library offers STL-like syntax for adding and finding data as well as STL-like
iterators for efficiently tracking location.

%package        devel
Summary:        Development files for jsonbuilder
Group:          System Environment/Libraries
Requires:       jsonbuilder = %{version}-%{release}

%description    devel
This package contains the headers and symlinks for using jsonbuilder from libraries and applications.

%prep
%autosetup -p1

%build
mkdir build && cd build
%cmake ..
%make_build

%check
make test -C build

%install
%make_install -C build

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_libdir}/libjsonbuilder.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libjsonbuilder.so
%{_libdir}/cmake/jsonbuilder
%{_includedir}/jsonbuilder

%changelog
* Tue Feb 20 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.1-3
- Adding a patch to fix the build with 3+ versions of 'catch'.

* Wed Oct 07 2020 Thomas Crain <thcrain@microsoft.com> - 0.2.1-2
- Updated #Source0 URL
- Verified License field and %%license macro

* Fri Aug 28 2020 Francisco Huelsz Prince <frhuelsz@microsoft.com> - 0.2.1-1
- Update to v0.2.1

* Wed Feb 12 2020 Nick Bopp <nichbop@microsoft.com> - 0.2-1
- Original version for CBL-Mariner.
