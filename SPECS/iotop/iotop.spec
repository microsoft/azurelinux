%global _hardened_build 1

Summary:        Simple top-like I/O monitor (implemented in C).
Name:           iotop
Version:        1.25
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System/Monitoring
URL:            https://github.com/tomas-m/iotop
# Source0:      https://github.com/tomas-m/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  ncurses-devel
BuildRequires:  make
BuildRequires:  pkgconfig(ncursesw)

%description
iotop does for I/O usage what top(1) does for CPU usage. It watches I/O
usage information output by the Linux kernel and displays a table of
current I/O usage by processes on the system. It is handy for answering
the question "Why is the disk churning so much?".
 
iotop requires a Linux kernel built with the CONFIG_TASKSTATS,
CONFIG_TASK_DELAY_ACCT, CONFIG_TASK_IO_ACCOUNTING and
CONFIG_VM_EVENT_COUNTERS config options on.
 
This package actually an alternative re-implementation of the older
Python-based iotop in C, optimized for performance. Normally a monitoring
tool intended to be used on a system under heavy stress should use the
least additional resources as possible.
 
%prep
%autosetup -p1

%build
%set_build_flags
NO_FLTO=1 %make_build

%install
V=1 STRIP=: %make_install

# %%check
# This package does not have any tests

%files	
%license COPYING
%license LICENSE
%{_sbindir}/iotop
%{_mandir}/man8/iotop.8*
 
%changelog
* Mon Feb 12 2024 Harshit Gupta <guptaharshit@microsoft.com> - 1.25-1
- Auto-upgrade to 1.25 - 3.0 upgrade
- Change the package to iotop-c (iotop but with C-based implementation)
- Re-import from Fedora 40 (license: MIT)

* Wed May 25 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 0.6-10
- Add dependency on python3-curses

* Tue Jan 25 2022 Thomas Crain <thcrain@microsoft.com> - 0.6-9
- Build with python3 instead of python2
- Add upstream patches for building with python3
- Document lack of tests
- Lint spec

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6-8
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.6-7
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.6-6
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Jun 16 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.6-5
- Use python2 explicitly

* Thu Jun 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.6-4
- Add python2 to Requires

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-3
- Fix arch

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-2
- GA - Bump release of all rpms

* Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.6-1
- Initial build. First version
