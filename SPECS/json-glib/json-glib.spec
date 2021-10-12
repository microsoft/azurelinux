Summary:        Library providing serialization and deserialization support for the JSON format
Name:           json-glib
Version:        1.4.4
Release:        7%{?dist}
License:        LGPLv2+
Group:          Development/Libraries
Source0:        https://ftp.gnome.org/pub/GNOME/sources/json-glib/1.4/%{name}-%{version}.tar.xz
URL:            https://wiki.gnome.org/Projects/JsonGlib
Patch0:         Remove-references-to-mesontest-binary.patch
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gobject-introspection-devel
BuildRequires:  glib-devel
BuildRequires:  libtool
BuildRequires:  which
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  python3-gobject-introspection
BuildRequires:  gtk-doc
Requires:       glib

%description
JSON-GLib is a library providing serialization and deserialization
support for the JavaScript Object Notation (JSON) format described by
RFC 4627.

%package devel
Summary:    Header files for the json-glib library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   glib-devel
Requires:  gobject-introspection-devel

%description devel
Header files for the json-glib library.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
export LDFLAGS="-Wl,-z,relro,-z,now"
mkdir build
meson --prefix=/usr            \
       -Ddocs=true             \
       . build

%ninja_build -C build


%install
cd build
DESTDIR=%{buildroot} ninja install
cd ..
%find_lang json-glib-1.0

%check
cd build
meson test


%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f json-glib-1.0.lang
#%defattr(-, root, root)
%doc NEWS
%attr(755,root,root) %{_bindir}/json-glib-format
%license COPYING
%attr(755,root,root) %{_bindir}/json-glib-validate

%ghost %{_libdir}/libjson-glib-1.0.so.?
%attr(755,root,root) %{_libdir}/libjson-glib-1.0.so.*.*.*

%files devel
#%defattr(-, root, root)
%{_libdir}/libjson-glib-1.0.so
%{_includedir}/json-glib-1.0
%{_libdir}/pkgconfig/json-glib-1.0.pc
%{_datadir}/gir-1.0/Json-1.0.gir
%{_datadir}/gtk-doc
%{_libdir}/girepository-1.0/Json-1.0.typelib
%{_libexecdir}/installed-tests/*
%{_datadir}/installed-tests/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 1.4.4-7
- Replace python2 with python3
- Remove pkgconf provides

*   Fri Dec 04 2020 Andrew Phelps <anphel@microsoft.com> 1.4.4-6
-   Use meson test in check section.
*   Mon Jun 01 2020 Henry Beberman <henry.beberman@microsoft.com> 1.4.4-5
-   Fix compilation issue with LDFLAGS and switch build to call meson directly.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.4.4-4
-   Added %%license line automatically
*   Fri Apr 17 2020 Emre Girgin <mrgirgin@microsoft.com> 1.4.4-3
-   Add a patch to replace occurences of mesontest with "meson test" after meson deprecated mesontest binary.
-   Update Source0 and URL.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.4.4-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Ankit Jain <ankitja@vmware.com> 1.4.4-1
-   Updated package to version 1.4.4
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 1.2.8-1
-   Updated package to version 1.2.8
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.0.4-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.4-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.0.4-1
-   Upgrade to 1.0.4
*   Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.2-3
-   Added more requirements for devel subpackage.
*   Fri Jun 26 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.2-2
-   Added Provides: pkgconfig(json-glib-1.0)
