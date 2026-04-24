# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global reponame crash-gcore

Summary: Gcore extension module for the crash utility
Name: crash-gcore-command
Version: 1.6.4
Release: 10%{?dist}
License: GPL-2.0-only
Source0: https://github.com/fujitsu/crash-gcore/archive/v%{version}/%{name}-%{version}.tar.gz
URL: https://github.com/fujitsu/crash-gcore
ExclusiveOS: Linux
ExclusiveArch: aarch64 ppc64le x86_64
BuildRequires: crash-devel >= 8.0.6
BuildRequires: gcc
Requires: crash >= 8.0.6

Patch0: crash-gcore-1.6.4-coredump-fix-building-failure-due-to-undefined-macro.patch
# https://github.com/fujitsu/crash-gcore/pull/6
Patch1: crash-gcore-1.6.4-set_context-third-arg.patch
Patch2: crash-gcore-1.6.4-x86-fix-the-issue-that-core-files-for-64-bit-tasks-a.patch

%description
Command for creating a core dump file of a user-space task that was
running in a kernel dump file.

%prep
%autosetup -n %{reponame}-%{version} -p1

%build
%make_build -C src -f gcore.mk

%install
install -m 0755 -d %{buildroot}%{_libdir}/crash/extensions
install -m 0755 -t %{buildroot}%{_libdir}/crash/extensions %{_builddir}/%{reponame}-%{version}/src/gcore.so

%files
%dir %{_libdir}/crash
%dir %{_libdir}/crash/extensions
%{_libdir}/crash/extensions/gcore.so
%license COPYING

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 21 2025 HATAYAMA Daisuke <d.hatayama@fujitsu.com> - 1.6.4-8
- x86: fix the issue that core files for 64-bit tasks are generated in the 32-bit format

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 12 2023 HATAYAMA Daisuke <d.hatayama@fujitsu.com> - 1.6.4-3
- Migrate to SPDX license format

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 1 2023 HATAYAMA Daisuke <d.hatayama@fujitsu.com> - 1.6.4-1
- coredump: fix building failure due to undefined macros MAPLE_TREE_{COUNT,GATHER}

* Wed Mar 1 2023 HATAYAMA Daisuke <d.hatayama@fujitsu.com> - 1.6.4-0
- Update to latest upstream release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jul 26 2022 HATAYAMA Daisuke <d.hatayama@fujitsu.com> - 1.6.3-2
- gcore.mk: fix mismatch of _FILE_OFFSET_BITS when building gcore.so
- coredump: fix unexpected truncation of generated core files
- elf: fix warning message caused by type mismatch of offset types
- coredump: fix segmentation fault caused by type mismatch
- x86: Fix failure of collecting vsyscall mapping due to change of enum type of vsyscall_mode
- gcore: fix memory allocation failure during processing NT_AUXV note
- gcore, defs: remove definitions and initializations for saved_auxv entries of offset and size tables
- coredump: use MEMBER_{OFFSET, SIZE} instead of GCORE_{OFFSET, SIZE}

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 10 2021 HATAYAMA Daisuke <d.hatayama@fujitsu.com> - 1.6.3-0
- Update to latest upstream release

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jan 22 2021 HATAYAMA Daisuke <d.hatayama@fujitsu.com> - 1.6.2-1
- Initial crash-gcore-command package
