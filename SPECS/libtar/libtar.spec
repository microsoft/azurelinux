Summary:        C library for manipulating tar files
Name:           libtar
Version:        1.2.20
Release:        11%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/tklauser/libtar/
#Source0:       https://github.com/tklauser/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# This patch appears to replicate Fedora's ' libtar-1.2.11-bz729009.patch'
Patch0:         libtar-gen-debuginfo.patch
# This patch appears to fix the same issue as Fedora's 'libtar-1.2.20-no-static-buffer.patch'
Patch1:         libtar-CVE-2013-4420.patch
# CVE patches + other fixes from Redhat
Patch2:         libtar-1.2.11-mem-deref.patch
# CVE-2021-33643
# CVE-2021-33644
Patch3:         libtar-1.2.20-CVE-2021-33643-CVE-2021-33644.patch
# CVE-2021-33640, CVE-2021-33645, CVE-2021-33646
Patch4:         CVE-2021-33640.patch
Patch5:         libtar-1.2.20-no-static-buffer.patch
Patch6:         libtar-1.2.20-fix-resource-leaks.patch
Patch7:         libtar-1.2.20-static-analysis.patch

%description
libtar is a library for manipulating tar files from within C programs.

%package        devel
Summary:        Development files for libtar
Group:          Development/Libraries
Requires:       libtar = %{version}-%{release}

%description    devel
The libtar-devel package contains libraries and header files for
developing applications that use libtar.

%prep
%setup -q
%autopatch -p1
autoreconf -iv

%build
%configure CFLAGS="%{optflags}" STRIP=/bin/true --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
chmod +x %{buildroot}/%{_libdir}/libtar.so.*
find %{buildroot} -type f -name "*.la" -delete -print

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

%changelog
* Fri Jan 20 2023 Adit Jha <aditjha@microsoft.com> - 1.2.20-11
- Fix CVE-2021-33640, which takes care of CVE-2021-33645, CVE-2021-33646

* Tue Sep 06 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.2.20-10
- Remove undesirable .la files
- Rely on generators to provide libtar.so.0()(64bit)
- Add CVE comments to correctly track CVE status

* Mon Sep 05 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.2.20-9
- Add various CVE and correctness patches from Fedora 37
- Fixes CVE-2021-33643, CVE-2021-33644, CVE-2021-33645, CVE-2021-33646

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.2.20-8
- Added %%license line automatically

* Thu Apr 23 2020 Nick Samson <nisamson@microsoft.com> 1.2.20-7
- Updated Source0, URL, removed sha1 line. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2.20-6
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Nov 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.20-5
- Fix CVE-2013-4420

* Thu Jun 29 2017 Chang Lee <changlee@vmware.com> 1.2.20-4
- Removed %check due to no test existence.

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.20-3
- Ensure non empty debuginfo

* Fri Mar 10 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.20-2
- Provides libtar.so.0()(64bit).

* Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.20-1
- Initial packaging for Photon
