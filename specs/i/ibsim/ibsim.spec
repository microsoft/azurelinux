# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: InfiniBand fabric simulator for management
Name: ibsim
Version: 0.12
Release: 2%{?dist}
# Automatically converted from old format: GPLv2 or BSD - review is highly recommended.
License: GPL-2.0-only OR LicenseRef-Callaway-BSD
Source: https://github.com/linux-rdma/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0027: 0027-run_opensm.sh-remove-opensm-c-option.patch

Url: https://github.com/linux-rdma/ibsim
BuildRequires: libibmad-devel, libibumad-devel, gcc
BuildRequires: make

# RDMA is not currently built on 32-bit ARM: #1484155
ExcludeArch: s390 %{arm}

%description
ibsim provides simulation of infiniband fabric for using with
OFA OpenSM, diagnostic and management tools.

%prep
%autosetup -v -p1

%build
%set_build_flags
%make_build

%install
%make_install prefix=%{_prefix} libpath=%{_libdir} binpath=%{_bindir}

%files
%{_libdir}/umad2sim/
%{_bindir}/ibsim
%{_bindir}/ibsim-run
%doc README TODO net-examples scripts
%license COPYING

%changelog
* Thu Nov 27 2025 Honggang Li <honggangli@163.com> - 0.12-1
- Rebase to upstream release ibsim-0.12

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0.11-10
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Honggang Li <honli@redhat.com> - 0.11-1
- Rebase to upstream release ibsim-0.11

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 08 2020 Honggang Li <honli@redhat.com> -0.10-1
- Rebase to upstream release ibsim-0.10

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 17 2020 Honggang Li <honli@redhat.com> - 0.9-1
- Rebase to upstream release ibsim-0.9

* Sun Feb 09 2020 Honggang Li <honli@redhat.com> - 0.8-4
- Fix FTBFS in Fedora rawhide/f32
- Resolves: bz1799516

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 22 2019 Honggang Li <honli@redhat.com> - 0.8-1
- Import ibsim for fedora
