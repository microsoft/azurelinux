Summary:        A library providing GObject bindings for libudev
Name:           libgudev
Version:        237
Release:        1%{?dist}
License:        LGPL2.1
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://git.gnome.org/browse/libgudev/
Source0:        https://download.gnome.org/sources/%{name}/%{version}/%{name}-%{version}.tar.xz

%{?systemd_requires}

BuildRequires:  glib >= 2.22.0
BuildRequires:  glib-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  libudev-devel
BuildRequires:  meson
BuildRequires:  pkg-config
BuildRequires:  systemd-devel
BuildRequires:  which

Requires:       systemd
Provides:       %{name}1 = %{version}-%{release}

%description
This is libgudev, a library providing GObject bindings for libudev. It
used to be part of udev, and now is a project on its own.

%package devel
Summary:        Header and development files for libgudev
Requires:       %{name} = %{version}
Requires:       glib-devel
Provides:       %{name}1-devel = %{version}-%{release}

%description devel
libgudev-devel package contains header files for building gudev applications.

%prep
%setup -q

%build
%meson -Dgtk_doc=false -Dtests=disabled -Dvapi=disabled
%meson_build

%install
%meson_install
find %{buildroot} -type f -name "*.la" -delete -print

# tests require umockdev-devel package which does not exist in CBL-Mariner yet
# %check
# %meson_test

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gudev-1.0.pc
%{_libdir}/girepository-1.0/GUdev-1.0.typelib
%{_datadir}/gir-1.0/GUdev-1.0.gir

%changelog
* Mon Mar 14 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 237-1
- Upgrade to version 237

* Fri Sep 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 232-6
- Remove libtool archive files from final packaging

* Tue May 25 2021 Olivia Crain <oliviacrain@microsoft.com> - 232-5
- Add provides for libgudev1, libgudev1-devel

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 232-4
- Added %%license line automatically

* Mon Apr 13 2020 Eric Li <eli@microsoft.com> - 232-3
- Update the Source0: and delete sha1. Verified License.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 232-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 30 2018 Bo Gan <ganb@vmware.com> - 232-1
- Update to 232

* Mon Apr 10 2017 Harish Udaiya kumar <hudaiyakumar@vmware.com> - 231-1
- Updated to version 231.

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> - 230-4
- Change systemd dependency

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 230-3
- GA - Bump release of all rpms

* Thu Aug 13 2015 Vinay Kulkarni <kulkarniv@vmware.com> - 230-2
- Split header files into devel package.

* Tue Aug 11 2015 Vinay Kulkarni <kulkarniv@vmware.com> - 230-1
- Add libgudev v230
