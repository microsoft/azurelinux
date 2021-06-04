Summary:        Glib networking modules
Name:           glib-networking
Version:        2.59.1
Release:        7%{?dist}
License:        GPLv2+ with exceptions
URL:            https://gitlab.gnome.org/GNOME/glib-networking/
Group:          System Environment/Development
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://ftp.gnome.org/pub/GNOME/sources/glib-networking/2.59/%{name}-%{version}.tar.xz

Patch0:         CVE-2020-13645.patch

BuildRequires:	nettle-devel >= 3.7.2
BuildRequires:	autogen-libopts-devel
BuildRequires:	libtasn1-devel
BuildRequires:  gnutls-devel
BuildRequires:	openssl-devel
BuildRequires:  intltool
BuildRequires:  glib
BuildRequires:  glib-devel
BuildRequires:  glib-schemas
BuildRequires:  meson
BuildRequires:  gnome-common
BuildRequires:  ninja-build
Requires:	nettle >= 3.7.2
Requires:	gnutls
Requires:	libtasn1
Requires:	openssl

%description
Glib-netowkring contains networking related gio modules for Glib.

%package lang
Summary: Additional language files for glib-networking
Group: System Environment/Development
Requires: glib-networking
%description lang
These are the additional language files of glib-networking.

%prep
%setup -q
%patch0 -p1

%build
mkdir build &&
cd    build &&
meson --prefix=/usr            \
      -Dlibproxy_support=false \
      -Dgnome_proxy_support=false \
      -Dpkcs11_support=false .. &&
ninja

%install
cd build
DESTDIR=%{buildroot} ninja install
%find_lang %{name}

%check
ninja test

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING LICENSE_EXCEPTION
%{_libdir}
%exclude %{_libdir}/debug

%files lang -f build/%{name}.lang
%defattr(-,root,root)

%changelog
*   Tue Apr 13 2021 Rachel Menge <rachelmengem@microsoft.com> - 2.59.1-7
-   Bump release to rebuild with new nettle (3.7.2)
*   Tue Aug 18 2020 Henry Beberman <hebeberm@microsoft.com> - 2.59.1-6
-   Backport patch for CVE-2020-13645
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.59.1-5
-   Added %%license line automatically, updated license line
*   Wed May 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.59.1-4
-   Removing *Requires for "ca-certificates".
*   Thu Apr 23 2020 Andrew Phelps <anphel@microsoft.com> 2.59.1-3
-   Fix URL. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.59.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*       Wed Nov 21 2018 Ashwin H <ashwinh@vmware.com> 2.59.1-1
-       Updated to 2.59.1 for make check fixes
*       Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 2.58.0-1
-       Update to version 2.58.0
*	Mon Apr 10 2017 Danut Moraru <dmoraru@vmware.com> 2.50.0-1
-	Updated to version 2.50.0
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.46.1-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.46.1-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 2.46.1-1
-   Updating to new version.
*   Wed Aug 12 2015 Touseef Liaqat <tliaqat@vmware.com> 2.45.1-1
-   Initial build.  First version
