Summary:        GNU Parted manipulates partition tables
Name:           parted
Version:        3.2
Release:        11%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://ftp.gnu.org/gnu/parted/parted-3.2.tar.xz
Source0:        http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
Conflicts:      toybox
Provides:       %{name}-devel = %{version}-%{release}

%description
This is useful for creating space for new operating systems,
reorganizing disk usage, copying data on hard disks and disk imaging.
The package contains a library, libparted, as well as well as a
command-line frontend, parted, which can also be used in scripts.

%prep
%setup -q

%build
#Add a header to allow building with glibc-2.28 or later
sed -i '/utsname.h/a#include <sys/sysmacros.h>' libparted/arch/linux.c &&

%configure --without-readline --disable-debug \
	   --disable-nls --disable-device-mapper
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

rm -rf %{buildroot}%{_infodir}/dir

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_infodir}/parted.info.gz
%{_datadir}/*

%changelog
* Tue Nov 03 2020 Joe Schmitt <joschmit@microsoft.com> - 3.2-11
- Provide parted-devel.

*  Wed Aug 05 2020 Andrew Phelps <anphel@microsoft.com> 3.2-10
-  Remove conflicting 'dir' file from _infodir

*  Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.2-9
-  Added %%license line automatically

*  Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.2-8
-  Initial CBL-Mariner import from Photon (license: dual Apache2/GPL2).

*  Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 3.2-7
-  Add conflict toybox.

*  Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 3.2-6
-  Fix compilation issue against glibc-2.28.

*  Wed Aug 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-5
-  Fix summary and description.

*  Tue Jun 06 2017 ChangLee <changlee@vmware.com> 3.2-4
-  Remove %check.

*  Fri Oct 07 2016 ChangLee <changlee@vmware.com> 3.2-3
-  Modified %check.

*  Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-2
-  GA Bump release of all rpms.

*  Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.2-1
-  Initial version.
