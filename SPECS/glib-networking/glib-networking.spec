Summary:        Glib networking modules
Name:           glib-networking
Version:        2.70.0
Release:        1%{?dist}
License:        GPLv2+ WITH exceptions
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Development
URL:            https://gitlab.gnome.org/GNOME/glib-networking/
Source0:        https://download.gnome.org/sources/%{name}/2.70/%{name}-%{version}.tar.xz
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  meson
BuildRequires:  glib2-devel
BuildRequires:  gnutls-devel
BuildRequires:  gnutls
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  p11-kit-devel
Requires:       glib2
Requires:       gnutls
Requires:       gsettings-desktop-schemas

%description
This package contains modules that extend the networking support in
GIO. In particular, it contains libproxy- and GSettings-based
GProxyResolver implementations and a gnutls-based GTlsConnection
implementation.

%prep
%setup -q

%build
%meson -Dlibproxy=disabled
%meson_build

%install
%meson_install
%find_lang %{name}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%license COPYING
%doc NEWS README
%{_libdir}/gio/modules/libgiognomeproxy.so
%{_libdir}/gio/modules/libgiognutls.so

%changelog
* Fri Feb 11 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.70.0-1
- Update source to v2.70.0

* Sun Dec 12 2021 Chris Co <chrco@microsoft.com> - 2.59.1-8
- Fix build options with new meson

* Tue Apr 13 2021 Rachel Menge <rachelmengem@microsoft.com> - 2.59.1-7
- Bump release to rebuild with new nettle (3.7.2)

* Tue Aug 18 2020 Henry Beberman <hebeberm@microsoft.com> - 2.59.1-6
- Backport patch for CVE-2020-13645

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.59.1-5
- Added %%license line automatically, updated license line

* Wed May 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.59.1-4
- Removing *Requires for "ca-certificates".

* Thu Apr 23 2020 Andrew Phelps <anphel@microsoft.com> 2.59.1-3
- Fix URL. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.59.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Nov 21 2018 Ashwin H <ashwinh@vmware.com> 2.59.1-1
- Updated to 2.59.1 for make check fixes

* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 2.58.0-1
- Update to version 2.58.0

* Mon Apr 10 2017 Danut Moraru <dmoraru@vmware.com> 2.50.0-1
- Updated to version 2.50.0
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.46.1-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.46.1-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 2.46.1-1
- Updating to new version.

* Wed Aug 12 2015 Touseef Liaqat <tliaqat@vmware.com> 2.45.1-1
- Initial build.  First version
