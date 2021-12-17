Summary:        Tracks system calls that are made by a running process
Name:           strace
Version:        5.1
Release:        4%{?dist}
License:        GPLv2+ and LGPLv2+
URL:            https://strace.io/
Group:          Development/Debuggers
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://strace.io/files/%{version}/%{name}-%{version}.tar.xz
Patch1:         gen_tests_fixes.patch

BuildRequires:  libacl-devel
BuildRequires:  libaio-devel

%global __requires_exclude ^/usr/bin/perl$

%description
The strace program intercepts and displays the system calls made by a running process. strace also records
all the arugments and return values from the system calls. This is useful in debugging a process.

%prep
%setup -q
%patch1 -p1

%build
%ifarch aarch64
%configure \
    --disable-mpers \
    --prefix=%{_prefix}
%else
%configure \
    --prefix=%{_prefix}
%endif

# to resolve build issue with glibc-2.26
sed -i 's/struct ucontext/ucontext_t/g' linux/x86_64/arch_sigreturn.c
sed -i 's/struct ucontext/ucontext_t/g' linux/arm/arch_sigreturn.c

make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} -k check TIMEOUT_DURATION=1200

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/man1/*

%changelog
*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.1-4
-   Removing the explicit %%clean stage.
-   License verified.

*   Wed Jan 06 2021 Andrew Phelps <anphel@microsoft.com> 5.1-3
-   Patch tests with expected results. Increase test timeout.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 5.1-2
-   Added %%license line automatically
*   Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 5.1-1
-   Update to 5.1. License fixed.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.25-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Nov 13 2018 Srinidhi Rao <srinidhir@vmware.com> 4.25-1
-   Updating to version 4.25
*   Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> 4.24-2
-   Fix 4.24 for aarch64
*   Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> 4.24-1
-   Updating to version 4.24
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.16-3
-   Aarch64 support
*   Wed Aug 23 2017 Alexey Makhalov <amakhalov@vmware.com> 4.16-2
-   Fix compilation issue for glibc-2.26
*   Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.16-1
-   Update to version 4.16
*   Thu Oct 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11-3
-   Exclude perl dependency
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11-2
-   GA - Bump release of all rpms
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 4.11-1
-   Upgrade version.
*   Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 4.10-1
-   Initial build. First version
