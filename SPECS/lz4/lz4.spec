Summary:        Extremely fast compression.
Name:           lz4
Version:        1.9.4
Release:        1%{?dist}
License:        BSD 2-Clause and GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications
URL:            https://lz4.github.io/lz4/
Source0:        https://github.com/lz4/lz4/archive/v%{version}/%{name}-%{version}.tar.gz
# Version format changed from r131 to v1.7.3 on Nov 16, 2016
# see https://github.com/lz4/lz4/tags?after=v1.7.4.2
# The versions with the new version format have the fix.
# *** NOTE: Leave this patch definition because the CVE Scan tool will flag the
# CVE due to the above version format change.
# CVE-2014-4715 applies to versions r* before r119.
Patch0:         CVE-2014-4715.nopatch

%description
LZ4 is lossless compression algorithm, providing compression speed at 400 MB/s per core, scalable with multi-cores CPU.
It features an extremely fast decoder, with speed in multiple GB/s per core, typically reaching RAM speed limits on multi-core systems.

%package devel
Summary:    Libraries and header files for lz4
Requires:   %{name} = %{version}-%{release}

%description devel
Static libraries and header files for the support library for lz4.

%prep
%setup -q

%build
make %{?_smp_mflags} all

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} PREFIX=%{_prefix}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_libdir}/liblz4.so.*
%{_datadir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/liblz4.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
*   Mon Feb 05 2024 Rohit Rawat <rohitrawat@microsoft.com> - 1.9.4-1
-   Upgrade to 1.9.4-1 to fix CVE-2021-3520

*   Thu Feb 17 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 1.9.3-1
-   Update to version 1.9.3
-   License verified.

*   Fri Jun 12 2020 Eric Li <eli@microsoft.com> 1.9.2-2
-   Mark CVE-2014-4715 as not applicable due to version format change

*   Tue May 18 2020 Andrew Phelps <anphel@microsoft.com> 1.9.2-1
-   Update to version 1.9.2

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.8.2-3
-   Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.8.2-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.8.2-1
-   Update to version 1.8.2

*   Wed Mar 29 2017 Michelle Wang <michellew@vmware.com> 1.7.5-1
-   Update lz4 package to 1.7.5.

*   Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.4-1
-   Add lz4 package.
