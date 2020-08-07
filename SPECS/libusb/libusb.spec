Summary:        A library which allows userspace access to USB devices
Name:           libusb
Version:        1.0.22
Release:        3%{?dist}
License:        LGPLv2+
URL:            http://sourceforge.net/projects/libusb/
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source:         http://downloads.sourceforge.net/libusb/libusb-%{version}.tar.bz2
%define sha1 libusb=10116aa265aac4273a0c894faa089370262ec0dc
BuildRequires:  systemd-devel
Requires:       systemd

%description
This package provides a way for applications to access USB devices.

%package        devel
Summary:        Development files for libusb
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description    devel
This package contains the header files, libraries and documentation needed to
develop applications that use libusb.

%prep
%setup -q

%build
%configure --disable-static
make

%install
make DESTDIR=%{buildroot} install

%check
pushd tests
make %{?_smp_mflags} -k check
./stress
popd

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/libusb*.so.*

%files devel
%{_includedir}/*
%{_libdir}/libusb*.so
%{_libdir}/libusb*.la
%{_libdir}/pkgconfig/*

%changelog
* Sat May 09 00:20:44 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.0.22-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0.22-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.0.22-1
-   Update to version 1.0.22
*   Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com>  1.0.21-1
-   Upgrading version to 1.0.21
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.0.20-4
-   Change systemd dependency
*   Tue Jul 12 2016 Xiaolin Li <xiaolinl@vmware.com>  1.0.20-3
-   Build libusb single threaded.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.20-2
-   GA - Bump release of all rpms
*   Thu May 05 2016 Nick Shi <nshi@vmware.com> 1.0.20-1
-   Initial version
