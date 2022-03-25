Summary:        A simplified, portable interface to several low-level networking routines
Name:           libdnet
Version:        1.14
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://code.google.com/p/libdnet
Source0:        https://github.com/dugsong/%{name}/archive/%{name}-%{version}.tar.gz
Patch0:         DisableMakeCheckCases.patch

%description
libdnet provides a simplified, portable interface to several low-level networking routines.

%package        devel
Summary:        Header and development files for libdnet
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q -n %{name}-%{name}-%{version}
%patch0 -p1

%build
./configure --prefix=/usr "CFLAGS=-fPIC" \
	--host=%{_host} --build=%{_build} \
            --mandir=%{_mandir}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/lib/ -name '*.la' -delete

%check
make  %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_libdir}/*.so*
%{_sbindir}/*
%{_mandir}/man8/*

%files devel
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/libdnet.a

%changelog
* Wed Mar 16 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 1.14-1
- Upgrading to v1.14

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.12-2
- Added %%license line automatically

*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.12-1
-   Update to 1.12. URL Fixed. Source0 URL Fixed. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.11-7
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.11-6
-   Aarch64 support

*   Thu Aug 03 2017 Kumar Kaushik <kaushikk@vmware.com> 1.11-5
-   Applying patch for makecheck bug #1633615.

*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.11-4
-   Move man files to /usr/share, add devel package

*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.11-3
-   Modified %check

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11-2
-   GA - Bump release of all rpms

*   Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 1.11-1
    Initial version
