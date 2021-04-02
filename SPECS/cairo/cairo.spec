Summary:        A 2D graphics library.
Name:           cairo
Version:        1.17.4
Release:        1%{?dist}
License:        LGPLv2 OR MPLv1.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://cairographics.org
Source0:        https://cairographics.org/snapshots/%{name}-%{version}.tar.xz
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  glib-devel
BuildRequires:  libpng-devel
BuildRequires:  libxml2-devel
BuildRequires:  pixman-devel
BuildRequires:  pkg-config
Requires:       expat
Requires:       glib
Requires:       libpng
Requires:       pixman

%description
Cairo is a 2D graphics library with support for multiple output devices.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       freetype-devel
Requires:       pixman-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
./configure \
        --prefix=%{_prefix} \
        --enable-win32=no \
        --enable-tee      \
        --enable-xlib=no     \
        --enable-xlib-xrender=no \
        CFLAGS="-O3 -fPIC" \
        --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/cairo/*.so*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Apr 02 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.17.4-1
- Upgrade to version 1.17.4, which resolves CVE-2020-35492.
- Fix source URL

*  Mon Oct 26 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.16.0-5
-  Fix CVE-2018-19876

*  Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.16.0-4
-  Added %%license line automatically

*  Mon Apr 20 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.16.0-3
-  Rename freetype2-devel to freetype-devel.
-  Remove sha1 macro.

*  Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.16.0-2
-  Initial CBL-Mariner import from Photon (license: Apache2).

*  Thu Mar 14 2019 Michelle Wang <michellew@vmware.com> 1.16.0-1
-  Upgrade cairo to 1.16.0 for CVE-2018-18064
-  CVE-2018-18064 is for version up to (including) 1.15.14

*  Tue Sep 11 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.14.12-1
-  Update to version 1.14.12

*  Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14.8-3
-  Fix CVE-2017-9814

*  Tue Jun 06 2017 Chang Lee <changlee@vmware.com> 1.14.8-2
-  Remove %check

*  Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.14.8-1
-  Initial version
