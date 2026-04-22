# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           iotop-c
Version:        1.30
Release: 3%{?dist}
Summary:        Simple top-like I/O monitor (implemented in C)

License:        GPL-2.0-or-later
URL:            https://github.com/Tomas-M/iotop/
Source0:        https://github.com/Tomas-M/iotop/releases/download/v%{version}/iotop-%{version}.tar.xz
Source1:        https://github.com/Tomas-M/iotop/releases/download/v%{version}/iotop-%{version}.tar.xz.asc
Source2:        https://raw.githubusercontent.com/Tomas-M/iotop/v%{version}/debian/upstream/signing-key.asc

Provides:       iotop
Obsoletes:      iotop < 0.7

BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  ncurses-devel
BuildRequires:  make
BuildRequires:  pkgconfig(ncursesw)

%description
iotop-c does for I/O usage what top(1) does for CPU usage. It watches I/O
usage information output by the Linux kernel and displays a table of
current I/O usage by processes on the system. It is handy for answering
the question "Why is the disk churning so much?".

iotop-c requires a Linux kernel built with the CONFIG_TASKSTATS,
CONFIG_TASK_DELAY_ACCT, CONFIG_TASK_IO_ACCOUNTING and
CONFIG_VM_EVENT_COUNTERS config options on.

iotop-c is an alternative re-implementation of iotop in C, optimized for
performance. Normally a monitoring tool intended to be used on a system
under heavy stress should use the least additional resources as
possible.

%global _hardened_build 1

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n iotop-%{version}

%build
%set_build_flags
NO_FLTO=1 %make_build

%install
V=1 STRIP=: BINDIR=$RPM_BUILD_ROOT%{_bindir} %make_install

%files
%license COPYING
%license LICENSE
%{_bindir}/iotop
%{_mandir}/man8/iotop.8*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 26 2025 Boian Bonev <bbonev@ipacct.com> - 1.30-1
- Update to latest ver 1.30

* Tue May  6 2025 Boian Bonev <bbonev@ipacct.com> - 1.29-1
- Update to latest ver 1.29

* Fri May  2 2025 Boian Bonev <bbonev@ipacct.com> - 1.28-1
- Update to latest ver 1.28

* Mon Feb 10 2025 Michal Hlavinka <mhlavink@redhat.com> - 1.27-4
- rebuild

* Wed Jan 22 2025 Michal Hlavinka <mhlavink@redhat.com> - 1.27-3
- update for bin and sbin merge https://fedoraproject.org/wiki/Changes/Unify_bin_and_sbin

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Boian Bonev <bbonev@ipacct.com> - 1.27-1
- Update to latest ver 1.27

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 03 2024 Boian Bonev <bbonev@ipacct.com> - 1.26-1
- Update to latest ver 1.26

* Thu Feb 01 2024 Michal Hlavinka <mhlavink@redhat.com> - 1.25-4
- replace iotop https://fedoraproject.org/wiki/Changes/Replace_iotop_with_iotop-c
- iotop-c executable renamed back to iotop

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Oct 14 2023 Boian Bonev <bbonev@ipacct.com> - 1.25-1
- Update to latest ver 1.25

* Sat Sep 30 2023 Boian Bonev <bbonev@ipacct.com> - 1.24-1
- Update to latest ver 1.24

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 14 2023 Boian Bonev <bbonev@ipacct.com> - 1.23-2
- SPDX migration

* Tue Jan 24 2023 Boian Bonev <bbonev@ipacct.com> - 1.23-1
- Update to latest ver 1.23

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 10 2022 Boian Bonev <bbonev@ipacct.com> - 1.22-1
- Update to latest ver 1.22

* Wed Jan 26 2022 Boian Bonev <bbonev@ipacct.com> - 1.21-1
- Update to latest ver 1.21

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Boian Bonev <bbonev@ipacct.com> - 1.20-1
- Update to latest ver 1.20

* Tue Sep 21 2021 Boian Bonev <bbonev@ipacct.com> - 1.19-1
- Update to latest ver 1.19

* Tue Aug 24 2021 Boian Bonev <bbonev@ipacct.com> - 1.18-1
- Update to latest ver 1.18

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Feb 6 2021 Boian Bonev <bbonev@ipacct.com> - 1.17-1
- Update to latest ver 1.17

* Thu Jan 28 2021 Boian Bonev <bbonev@ipacct.com> - 1.16-1
- Update to latest ver 1.16

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Sep 26 2020 Boian Bonev <bbonev@ipacct.com> - 1.15-1
- Initial packaging for Fedora
