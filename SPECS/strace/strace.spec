%global __requires_exclude ^%{_bindir}/perl$
Summary:        Tracks system calls that are made by a running process
Name:           strace
Version:        6.1
Release:        1%{?dist}
License:        GPL-2.0-or-later AND LGPL-2.1-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Debuggers
URL:            https://strace.io/
Source0:        https://strace.io/files/%{version}/%{name}-%{version}.tar.xz
# Both patches released upstream in v6.4
Patch0:         testfix-netlink-list-memberships.patch
BuildRequires:  libacl-devel
BuildRequires:  libaio-devel

%description
The strace program intercepts and displays the system calls made by a running process. strace also records
all the arugments and return values from the system calls. This is useful in debugging a process.

%prep
%autosetup -p1

%build
%ifarch aarch64
%configure \
    --disable-mpers \
    --prefix=%{_prefix}
%else
%configure \
    --prefix=%{_prefix}
%endif

%make_build

%install
%make_install

%check
%make_build -k check TIMEOUT_DURATION=1200

%files
%defattr(-,root,root)
%license COPYING LGPL-2.1-or-later bundled/linux/GPL-2.0
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri Nov 03 2023 Rachel Menge <rachelmenge@microsoft.com> - 6.1-1
- Upgrade to 6.1

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.16-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Jun 10 2023 Olivia Crain <oliviacrain@microsoft.com> - 5.16-3
- Add upstream patch to fix sockopt-sol_netlink test with kernel >= 5.15.116.1
- Modify landlock test patch to properly apply with `git am`
- Package full license texts

* Wed Jun 07 2023 Olivia Crain <oliviacrain@microsoft.com> - 5.16-2
- Add upstream patch to fix landlock_create_ruleset-y test
- Modernize calls to make by using macros
- Use SPDX license expression in license tag

* Wed Mar 02 2022 Bala <balakumaran.kannan@microsoft.com> - 5.16-1
- Upgrade to latest version
- Remove patches and fixes not necessary for newer version

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.1-4
- Removing the explicit %%clean stage.
- License verified.

* Wed Jan 06 2021 Andrew Phelps <anphel@microsoft.com> - 5.1-3
- Patch tests with expected results. Increase test timeout.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 5.1-2
- Added %%license line automatically

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> - 5.1-1
- Update to 5.1. License fixed.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.25-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Nov 13 2018 Srinidhi Rao <srinidhir@vmware.com> - 4.25-1
- Updating to version 4.25

* Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> - 4.24-2
- Fix 4.24 for aarch64

* Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> - 4.24-1
- Updating to version 4.24

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.16-3
- Aarch64 support

* Wed Aug 23 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.16-2
- Fix compilation issue for glibc-2.26

* Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 4.16-1
- Update to version 4.16

* Thu Oct 20 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.11-3
- Exclude perl dependency

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.11-2
- GA - Bump release of all rpms

* Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> - 4.11-1
- Upgrade version.

* Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> - 4.10-1
- Initial build. First version
