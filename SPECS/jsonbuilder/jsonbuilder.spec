Summary:        Modern C++ library for an efficient container for building JSON objects
Name:           jsonbuilder
Version:        0.2.1
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment
URL:            https://github.com/microsoft/jsonbuilder
#Source0:       https://github.com/microsoft/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
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
%setup -q

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
* Wed Oct 07 2020 Olivia Crain <oliviacrain@microsoft.com> - 0.2.1-2
- Updated #Source0 URL
- Verified License field and %%license macro

* Fri Aug 28 2020 Francisco Huelsz Prince <frhuelsz@microsoft.com> - 0.2.1-1
- Update to v0.2.1

* Wed Feb 12 2020 Nick Bopp <nichbop@microsoft.com> - 0.2-1
- Original version for CBL-Mariner.
