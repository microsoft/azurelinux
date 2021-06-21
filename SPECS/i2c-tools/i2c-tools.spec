Summary:        A set of I2C tools for Linux Kernel
Name:           i2c-tools
Version:        4.1
Release:        3%{?dist}
License:        LGPL-2.1+
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://i2c.wiki.kernel.org/index.php/I2C_Tools
Source0:        https://www.kernel.org/pub/software/utils/i2c-tools/%{name}-%{version}.tar.xz
%define sha1 %{name}-%{version}=d383d1ae86bd695b505dd1251ac399e3cdc1b05f

%description
This package contains a heterogeneous set of I2C tools for Linux Kernelas well as an I2C library.
Various tools are included in this package with different catagories:
eeprom, eeprog, eepromer, py-smbus, tools that rely on "i2c-dev" kernel driver.

%package    devel
Summary:    Header and development files for zlib
Requires:   %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%license COPYING
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/libi2c.so.0*
%{_mandir}/man1/*.1.gz
%{_mandir}/man8/*.8.gz

%files devel
%dir %{_includedir}/i2c
%{_includedir}/i2c/smbus.h
%{_libdir}/libi2c.a
%{_libdir}/libi2c.so

%changelog
* Sat May 09 00:21:01 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.1-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Feb 27 2019 Ankit Jain <ankitja@vmware.com> 4.1-1
-   Initial version
