%define BaseVersion 1.71
Summary:        Introspection system for GObject-based libraries
Name:           gobject-introspection
Version:        %{BaseVersion}.0
Release:        15%{?dist}
License:        GPLv2+ AND LGPLv2+ AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://github.com/GNOME/gobject-introspection
Source0:        https://ftp.gnome.org/pub/GNOME/sources/gobject-introspection/%{BaseVersion}/%{name}-%{version}.tar.xz
BuildRequires:  autoconf-archive
BuildRequires:  bison
BuildRequires:  cairo-gobject-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glib-devel >= 2.58.0
BuildRequires:  golang
BuildRequires:  intltool
BuildRequires:  libffi-devel
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  which
Requires:       glib >= 2.58.0
Requires:       libffi

%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package -n     python3-gobject-introspection
Summary:        Python3 package for handling GObject introspection data
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       python3-xml

%description -n python3-gobject-introspection
This package contains a Python package for handling the introspection
data from Python.

%package devel
Summary:        Libraries and headers for gobject-introspection
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel
Requires:       libffi-devel
Requires:       python3-%{name} = %{version}-%{release}

%description devel
Libraries and headers for gobject-introspection.

%prep
%autosetup -p 1

%build
%meson -Ddoctool=disabled -Dpython=%{python3}
%meson_build

%install
%meson_install
# Move the python3 modules to the correct location
mkdir -p %{buildroot}/%{python3_sitelib}
mv %{buildroot}/%{_libdir}/gobject-introspection/giscanner %{buildroot}/%{python3_sitelib}

rm -rf %{buildroot}/%{_datarootdir}/gtk-doc/html
find %{buildroot} -type f -name "*.la" -delete -print

%check
%meson_test

%ldconfig_scriptlets

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/lib*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files -n python3-gobject-introspection
%defattr(-,root,root,-)
%{python3_sitelib}/giscanner

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/g-ir-*
%{_datadir}/gir-1.0
%{_datadir}/aclocal/introspection.m4
%{_datadir}/gobject-introspection-1.0
%{_mandir}/man1/*.gz

%changelog
* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.71.0-15
- Bump release to rebuild with updated version of Go.

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.71.0-14
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.71.0-13
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.71.0-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.71.0-11
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.71.0-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.71.0-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.71.0-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.71.0-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.71.0-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.71.0-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.71.0-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.71.0-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.71.0-2
- Bump release to rebuild with golang 1.18.3

* Wed Feb 16 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.71.0-1
- Update source to v1.71.0
- Switch to meson build

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 1.58.0-12
- Fix Python 3.9 compatibility issue

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.58.0-11
- Remove python2 package
- Lint spec

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> - 1.58.0-10
- Increment release to force republishing using golang 1.15.13.

* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.58.0-9
- Increment release to force republishing using golang 1.15.11.

* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> - 1.58.0-8
- Increment release to force republishing using golang 1.15.

* Wed Jul 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.58.0-7
- Forcing single job 'make' build to avoid intermittent build errors.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.58.0-6
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.58.0-5
- Renaming go to golang

* Tue Apr 21 2020 Eric Li <eli@microsoft.com> - 1.58.0-4
- Fix Source0: and delete sha1. Verified License. Fixed URL.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.58.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> - 1.58.0-2
- -devel requires -python.

* Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> - 1.58.0-1
- Update version to 1.58.0

* Tue Jan 02 2018 Alexey Makhalov <amakhalov@vmware.com> - 1.52.1-5
- Add autoreconf to support automake-1.15.1

* Mon Aug 28 2017 Kumar Kaushik <kaushikk@vmware.com> - 1.52.1-4
- Disabling make check for Regress-1.0.gir test, bug#1635886

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.52.1-3
- Add python3-xml to python3 sub package Buildrequires.

* Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.52.1-2
- Added python3 subpackage.

* Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> - 1.52.1-1
- Updated to version 1.52.1

* Thu Oct 06 2016 ChangLee <changlee@vmware.com> - 1.46.0-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.46.0-2
- GA - Bump release of all rpms

* Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> - 1.46.0-1
- Updated version.

* Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> - 1.43.3-4
- Moving static lib files to devel package.

* Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> - 1.43.3-3
- Removing la files from packages.

* Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> - 1.43.3-2
- Added more requirements for devel subpackage.
