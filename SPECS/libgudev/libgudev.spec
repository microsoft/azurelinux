Summary:        A library providing GObject bindings for libudev
Name:           libgudev
Version:        232
Release:        4%{?dist}
License:        LGPL2.1
URL:            https://git.gnome.org/browse/libgudev/
Source0:        https://download.gnome.org/sources/%{name}/%{version}/%{name}-%{version}.tar.xz
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
BuildRequires:  glib >= 2.22.0
BuildRequires:  glib-devel
BuildRequires:  gnome-common
BuildRequires:  gobject-introspection
BuildRequires:  gtk-doc
BuildRequires:  pkg-config
BuildRequires:  systemd-devel
BuildRequires:  which
Requires:       systemd
Distribution:   Mariner

%description
This is libgudev, a library providing GObject bindings for libudev. It
used to be part of udev, and now is a project on its own.

%package devel
Summary:        Header and development files for libgudev
Requires:       %{name} = %{version}
Requires:       glib-devel

%description devel
libgudev-devel package contains header files for building gudev applications.

%prep
%setup -q

%build
%configure  --disable-umockdev
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/gudev-1.0.pc

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 232-4
- Added %%license line automatically

*       Mon Apr 13 2020 Eric Li <eli@microsoft.com> 232-3
-       Update the Source0: and delete sha1. Verified License.
*       Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 232-2
-       Initial CBL-Mariner import from Photon (license: Apache2).
*       Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 232-1
-       Update to 232
*	Mon Apr 10 2017 Harish Udaiya kumar <hudaiyakumar@vmware.com> 231-1
-	Updated to version 231.
*       Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  230-4
-       Change systemd dependency
*       Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 230-3
-       GA - Bump release of all rpms
*       Thu Aug 13 2015 Vinay Kulkarni <kulkarniv@vmware.com> 230-2
-       Split header files into devel package.
*       Tue Aug 11 2015 Vinay Kulkarni <kulkarniv@vmware.com> 230-1
-       Add libgudev v230
