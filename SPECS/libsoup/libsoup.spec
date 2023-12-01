%define BaseVersion 3.0
Summary:        libsoup HTTP client/server library
Name:           libsoup
Version:        %{BaseVersion}.4
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Development
URL:            https://wiki.gnome.org/LibSoup
Source0:        https://ftp.gnome.org/pub/GNOME/sources/libsoup/%{BaseVersion}/%{name}-%{version}.tar.xz
BuildRequires:  meson
BuildRequires:  autogen
BuildRequires:  glib-devel
BuildRequires:  glib-networking
BuildRequires:  gobject-introspection-devel
BuildRequires:  httpd
BuildRequires:  icu-devel
BuildRequires:  intltool
BuildRequires:  krb5-devel
BuildRequires:  libpsl-devel
BuildRequires:  libxml2-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-tools
BuildRequires:  sqlite-devel
BuildRequires:  cmake
BuildRequires:  libnghttp2-devel
BuildRequires:  brotli-devel
BuildRequires:  gnutls-devel
BuildRequires:  vala
BuildRequires:  gtk-doc
BuildRequires:  python3-pygments
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(FindBin)
BuildRequires:  perl(File::Find)
Requires:       glib-networking
Requires:       libpsl
Requires:       libxml2

%description
libsoup is HTTP client/server library for GNOME

%package         devel
Summary:        Header files for libsoup
Group:          System Environment/Development
Requires:       %{name} = %{version}-%{release}
Requires:       libxml2-devel

%description     devel
Header files for libsoup.

%package         doc
Summary:        gtk-doc files for libsoup
Group:          System Environment/Development
Requires:       %{name} = %{version}-%{release}

%description     doc
gtk-doc files for libsoup.

%package         lang
Summary:        Additional language files for libsoup
Group:          System Environment/Development
Requires:       %{name} = %{version}-%{release}

%description     lang
These are the additional language files of libsoup.

%prep
%autosetup

%build
%meson \
    -Dgtk_doc=true \
    -Dsysprof=disabled \
    -Dautobahn=disabled \
    -Dhttp2_tests=disabled \
    -Dntlm=disabled \
    -Dtests=false
%meson_build

%install
%meson_install
find %{buildroot} -type f -name "*.la" -delete -print

%find_lang %{name}-%{BaseVersion}

%check
%meson_test

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%exclude %{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/*
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/%{name}-%{BaseVersion}.deps
%{_datadir}/vala/vapi/%{name}-%{BaseVersion}.vapi

%files doc
%defattr(-,root,root)
%{_datadir}/gtk-doc/html/*

%files lang -f %{name}-%{BaseVersion}.lang
%defattr(-,root,root)

%changelog
* Mon Jan 24 2022 Henry Li <lihl@microsoft.com> - 3.0.4-1
- Upgrade to version 3.0.4
- Add cmake, libnghttp2-devel, brotli-devel, gnutls-devel, 
  gtk-doc, vala and python3-pygments as BR
- Use meson to build and install
- Add additional files to libsoup-devel 
- License Verified

* Wed Jan 19 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.64.0-8
- Add perl find bin and file find to build requires.

* Fri Sep 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.64.0-7
- Remove libtool archive files from final packaging

* Tue Jan 05 2021 Ruying Chen <v-ruyche@microsoft.com> - 2.64.0-6
- Enable gobject-introspection support.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

* Tue Apr 21 2020 Eric Li <eli@microsoft.com> 2.64.0-4
- Fix Source0: and delete sha1. Verified license. Fixed URL. Fixed formatting.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.64.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Dec 07 2018 Keerthana <keerthanak@vmware.com> 2.64.0-2
- Fix Make check failures.

* Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 2.64.0-1
- Update to 2.64.0

* Mon Sep 03 2018 Ankit Jain <ankitja@vmware.com> 2.57.1-4
- Fix for CVE-2018-12910

* Mon Jun 18 2018 Tapas Kundu <tkundu@vmware.com> 2.57.1-3
- CVE-2017-2885

* Fri Aug 11 2017 Chang Lee <changlee@vmware.com> 2.57.1-2
- Added krb5-devel to BuildRequires for %check

* Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com> 2.57.1-1
- Upgrading to version 2.57.1

* Fri Nov 18 2016 Alexey Makhalov <amakhalov@vmware.com> 2.53.90-3
- Add sqlite-devel build deps

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.53.90-2
- GA - Bump release of all rpms

* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 2.53.90-1
- Updated version.

* Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 2.50.0-5
- Moving static lib files to devel package.

* Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 2.50.0-4
- Removing la files from packages.

* Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 2.50.0-3
- Addinf libxml2 to Requires

* Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 2.50.0-2
- Exclude /usr/lib/debug

* Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 2.50.0-1
- Initial build.  First version
