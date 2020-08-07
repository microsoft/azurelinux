Summary:	Crypto Libraries
Name:		libgcrypt
Version:	1.8.3
Release:        4%{?dist}
License:        GPLv2+ and LGPLv2+
URL:            http://www.gnu.org/software/libgcrypt/
Source0:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2
%define sha1 libgcrypt=13bd2ce69e59ab538e959911dfae80ea309636e3
Patch0:     libgcrypt-00-ac_cv_sys_symbol_underscore.patch
Group:		System Environment/Libraries
Vendor:         Microsoft Corporation
BuildRequires:	libgpg-error-devel
Requires:	libgpg-error
Distribution:   Mariner
%description
The libgcrypt package contains a general purpose crypto library based on the code used in GnuPG. The library provides a high level interface to cryptographic building blocks using an extendable and flexible API.

%package devel
Summary:	Development libraries and header files for libgcrypt
Requires:	%{name} = %{version}-%{release}
Requires:	libgpg-error-devel

%description devel
The package contains libraries and header files for
developing applications that use libgcrypt.

%prep
%setup -q

%patch0 -p1

%build
if [ %{_host} != %{_build} ] ; then
%configure \
    --with-sysroot=/target-%{_arch} \
    ac_cv_sys_symbol_underscore=no
else
%configure
fi
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSES
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_datadir}/aclocal/*
%{_libdir}/*.la
%{_libdir}/*.so

%changelog
* Sat May 09 00:20:49 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.8.3-4
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.8.3-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Nov 06 2018 Sriram Nambakam <snambakam@vmware.com> 1.8.3-2
-   Cross compilation support
*   Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 1.8.3-1
-   Update to 1.8.3
*   Tue Oct 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.1-1
-   Updated to v1.8.1 to address CVE-2017-0379
*   Tue Apr 04 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.7.6-1
-   Udpated to version 1.7.6
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.6.5-3
-   Required libgpg-error-devel.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.5-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  1.6.5-1
-   Upgrade to 1.6.5
*   Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.3-1
-   Initial build. First version
