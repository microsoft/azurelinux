Vendor:         Microsoft Corporation
Distribution:   Azure Linux

## START: Set by rpmautospec
## (rpmautospec version 0.6.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

Name:           numatop
Version:        2.4
Release:        1%{?dist}
Summary:        Memory access locality characterization and analysis

License:        BSD-3-Clause
URL:            https://01.org/numatop
Source:         https://github.com/intel/numatop/archive/refs/tags/v%{version}.tar.gz#/%{name}-v%{version}.tar.xz

# https://github.com/intel/numatop/pull/71
Patch:          0001-common-Use-sym_type_t-in-elf64_binary_read-signature.patch
Patch:          0002-common-Add-format-strings-to-mvwprintw-calls.patch
Patch:          0003-common-Remove-unnecessary-temp-buffer.patch
Patch:          0004-common-Use-memcpy-to-the-process-name-to-a-line.patch
Patch:          0005-common-Replace-malloc-strncpy-with-strdup.patch
Patch:          0006-common-Build-node-string-with-bound-checks.patch
Patch:          0007-common-Increase-node-string-buffer-size.patch
Patch:          0008-x86-Add-missing-fields-to-s_emr_config.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  check-devel
BuildRequires:  ncurses-devel
BuildRequires:  numactl-devel

# This only works for Intel and Power CPUs
ExclusiveArch:  x86_64 ppc64le


%description
NumaTOP is an observation tool for runtime memory locality characterization and
analysis of processes and threads running on a NUMA system. It helps the user
characterize the NUMA behavior of processes and threads and identify where the
NUMA-related performance bottlenecks reside.

NumaTOP supports the Intel Xeon processors, AMD Zen processors and PowerPC
processors.


%prep
%autosetup -p1


%build
autoreconf --force --install --symlink
%configure
%make_build


%install
%make_install


%check
%make_build check


%files
%doc AUTHORS
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8*


%changelog
* Fri Dec 20 2024 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 2.4-1
- Update to 2.4
- License verified

* Tue Jun 21 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.1-5
- Add patch to fix format-security wanings with ncurses 6.3
- License verified

* Wed Aug 11 2021 Thomas Crain <thcrain@microsoft.com> - 2.1-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add patch to fix linking error

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 23 2019 Dridi Boukelmoune <dridi@fedoraproject.org>- 2.1-1
- Update to 2.1
- Upstream moved to github
- Upstream switched to autotools
- Disable --as-needed until it's patched upstream
- Drop defunct 32bit x86 support
- Add ppc64le support
- Run the new test suite

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jul 15 2018 Dridi Boukelmoune <dridi@fedoraproject.org>- 1.0.4-8
- Build requires gcc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 13 2017 Dridi Boukelmoune <dridi@fedoraproject.org>- 1.0.4-3
- Catch up with packaging guidelines

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 28 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.4-1
- Update to latest version (support for BDW-EP/EX)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 14 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.3-3
- Replace ExcludeArch with ExclusiveArch

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 25 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.3-1
- New upstream release (#1076549)
- Remove upstreamed patch

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 30 2014 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.0.2-3
- Backport and rebase 1.0.1 patch

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 16 2014 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.0.2-1
- Bump version to 1.0.2
- Remove upstreamed patch

* Fri Sep 20 2013 Dan Horák <dan[at]danny.cz> - 1.0.1-5
- no numa on s390(x)

* Fri Sep 13 2013 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.0.1-4
- Patch for the 32bit hardened build.

* Sun Aug 25 2013 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.0.1-3
- Hardened build.
- Automatic requires.

* Fri Aug 02 2013 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.0.1-2
- Fix the license tag.

* Thu Aug 01 2013 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.0.1-1
- Initial spec.

## END: Generated by rpmautospec
