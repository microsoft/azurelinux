Summary:	pixel manipulation library.
Name:		pixman
Version:    0.36.0
Release:    3%{?dist}
License:	MIT
URL:        https://cgit.freedesktop.org/pixman/
Source0:    https://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2
Patch0:     CVE-2022-44638.patch
Group:		System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:	libtool

%description
Pixman is a pixel manipulation library for X and Cairo.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
Provides:	pkgconfig(pixman-1)

%description	devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
./configure \
	--prefix=%{_prefix} \
	CFLAGS="-O3 -fPIC" \
	--disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc COPYING
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/pixman-1
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Feb 08 2023 Dan Streetman <ddstreet@microsoft.com> - 0.36.0-3
- CVE-2022-44638

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.36.0-2
- Added %%license line automatically

*   Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 0.36.0-1
-   Update to 0.36.0. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.34.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*       Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 0.34.0-1
-       Initial version
