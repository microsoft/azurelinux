# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global reponame crash-trace

Summary: Trace extension module for the crash utility
Name: crash-trace-command
Version: 3.0
Release: 14%{?dist}
License: GPL-2.0-only
Source: https://github.com/fujitsu/crash-trace/archive/v%{version}/%{name}-%{version}.tar.gz
URL: https://github.com/fujitsu/crash-trace
ExclusiveOS: Linux
ExclusiveArch: aarch64 ppc64le riscv64 s390x x86_64
BuildRequires: crash-devel >= 7.2.0-2
BuildRequires: gcc
Requires: trace-cmd
Requires: crash >= 7.2.0-2

Patch0001: 0001-Makefile-set-DT_SONAME-to-trace.so.patch
Patch0002: 0002-Makefile-fix-build-failure-on-aarch64-and-ppc64le.patch
Patch0003: 0003-Makefile-fix-build-failure-on-riscv64.patch

%description
Command for reading ftrace data from a dump file.

%prep
%autosetup -n %{reponame}-%{version}

%build
%make_build

%install
install -m 0755 -d %{buildroot}%{_libdir}/crash/extensions
install -m 0755 -t %{buildroot}%{_libdir}/crash/extensions %{_builddir}/%{reponame}-%{version}/trace.so

%files
%dir %{_libdir}/crash
%dir %{_libdir}/crash/extensions
%{_libdir}/crash/extensions/trace.so
%license COPYING

%changelog
* Mon Feb 16 2026 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 3.0-14
- Enable the RISC-V 64-bit architecture port

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 12 2023 HATAYAMA Daisuke <d.hatayama@fujitsu.com> - 3.0-8
- Migrate to SPDX license format

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Feb 19 2021 HATAYAMA Daisuke <d.hatayama@fujitsu.com> - 3.0-2
- Makefile: set DT_SONAME to trace.so
- Makefile: fix build failure on aarch64 and ppc64le
* Fri Jan 22 2021 HATAYAMA Daisuke <d.hatayama@fujitsu.com> - 3.0-1
- Initial crash-trace-command package
