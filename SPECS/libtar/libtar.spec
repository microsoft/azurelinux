Summary:        C library for manipulating tar files
Name:           libtar
Version:        1.2.20
Release:        8%{?dist}
URL:            https://github.com/tklauser/libtar/
License:        BSD
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/tklauser/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         libtar-gen-debuginfo.patch
patch1:         libtar-CVE-2013-4420.patch
Provides:       libtar.so.0()(64bit)

%description
libtar is a library for manipulating tar files from within C programs.

%package        devel
Summary:        Development files for libtar
Group:          Development/Libraries
Requires:       libtar = %{version}-%{release}

%description    devel
The litar-devel package contains libraries and header files for
developing applications that use libtar.

%prep
%setup
%patch0
%patch1 -p1
autoreconf -iv

%build
%configure CFLAGS="%{optflags}" STRIP=/bin/true --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
chmod +x %{buildroot}/%{_libdir}/libtar.so.*

#%check
#Commented out %check due to no test existence

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/libtar
%{_libdir}/libtar.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/libtar.so
%{_libdir}/libtar.la

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.2.20-8
- Added %%license line automatically

*   Thu Apr 23 2020 Nick Samson <nisamson@microsoft.com> 1.2.20-7
-   Updated Source0, URL, removed sha1 line. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2.20-6
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Nov 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.20-5
-   Fix CVE-2013-4420
*   Thu Jun 29 2017 Chang Lee <changlee@vmware.com> 1.2.20-4
-   Removed %check due to no test existence.
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.20-3
-   Ensure non empty debuginfo
*   Fri Mar 10 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.20-2
-   Provides libtar.so.0()(64bit).
*   Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.20-1
-   Initial packaging for Photon
