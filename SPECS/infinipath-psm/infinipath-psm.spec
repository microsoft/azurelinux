%global git_version 26_g604758e_open
%global MAKEARG PSM_HAVE_SCIF=0 MIC=0
Summary:        Intel Performance Scaled Messaging (PSM) Libraries
Name:           infinipath-psm
Version:        3.3
Release:        30%{?dist}
License:        GPLv2 OR BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/01org/psm
Source0:        https://github.com/intel/psm/archive/refs/tags/v%{version}.tar.gz#/psm-%{version}.tar.gz
Source1:        ipath.rules
Patch1:         0001-fix-a-compilation-issue.patch
Patch2:         adjust-base-cflags.patch
Patch3:         remove-executable-permissions-for-header-files.patch
Patch4:         0001-Include-sysmacros.h.patch
Patch5:         0001-Extend-buffer-for-uvalue-and-pvalue.patch
Patch6:         extend-fdesc-array.patch
Patch7:         psm-multiple-definition.patch
Patch8:         infinipath-psm-gcc11.patch
# Upstream commits past the 3.3 version required for GCC 6+:
# - https://github.com/intel/psm/commit/28489fd4ca1672fe84fa4c471bf6fb9d2a30a853
# - https://github.com/intel/psm/commit/3b6306adaa9acf9ce7297129eb2215823de5b70a
Patch9:         3.3_upstream_fixes_for_gcc6.patch
BuildRequires:  gcc
BuildRequires:  libuuid-devel
BuildRequires:  make
BuildRequires:  systemd-rpm-macros
Requires:       udev
Obsoletes:      infinipath-libs <= %{version}-%{release}
ExclusiveArch:  x86_64

%description
The PSM Messaging API, or PSM API, is Intel's low-level
user-level communications interface for the True Scale
family of products. PSM users are enabled with mechanisms
necessary to implement higher level communications
interfaces in parallel environments.

%package devel
Summary:        Development files for Intel PSM
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      infinipath-devel <= %{version}-%{release}

%description devel
Development files for the %{name} library.

%prep
%setup -q -n psm-%{version}
%patch 1 -p1
%patch 2 -p1
%patch 3 -p1
%patch 4 -p1
%patch 5 -p1
%patch 6
%patch 7 -p1
%patch 8 -p1
%patch 9 -p1
find libuuid -type f -not -name 'psm_uuid.[c|h]' -not -name Makefile -delete

%build
# LTO seems to trigger a post-build failure as some symbols with external scope
# are "leaking".  SuSE has already disabled LTO for this package, but no real
# details about why those symbols are "leaking".
%define _lto_cflags %{nil}

# Use 'uname -m' to properly determine architecture (x86_64)
sed -i "s/(arch)/(shell uname -m)/g" Makefile
sed -i "s/(arch)/(shell uname -m)/g" ipath/Makefile
sed -i "s/uname -p/uname -m/g" buildflags.mak

%{set_build_flags}
%make_build PSM_USE_SYS_UUID=1 %{MAKEARG} CC=gcc

%install
%make_install %{MAKEARG}
install -d %{buildroot}%{_udevrulesdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_udevrulesdir}/60-ipath.rules

%ldconfig_scriptlets

%files
%{_udevrulesdir}/60-ipath.rules
%{_lib64dir}/libpsm_infinipath.so.*
%{_lib64dir}/libinfinipath.so.*
%license COPYING
%doc README

%files devel
%{_lib64dir}/libpsm_infinipath.so
%{_lib64dir}/libinfinipath.so
%{_includedir}/psm.h
%{_includedir}/psm_mq.h

%changelog
* Fri Feb 02 2024 Andrew Phelps <anphel@microsoft.com> - 3.3-30
- Fix build errors due to unknown architecture.

* Fri Feb 03 2023 Riken Maharjan <rmaharjan@microsoft.com> - 3.3-29
- Move from extended to Core.

* Thu Mar 03 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.3-28
- Adding GCC 11 patch from Fedora 36 (license: MIT).
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.3-27
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Jan 08 2021 Ruying Chen <v-ruyche@microsoft.com> - 3.3-26_g604758e_open.6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Update library path to lib64.

* Sun Feb 09 2020 Honggang Li <honli@redhat.com> - 3.3-26_g604758e_open.5
- Fix FTBFS in Fedora rawhide/f32
- Resolves: bz1799521

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-26_g604758e_open.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 24 2019 Honggang Li <honli@redhat.com> - 3.3-26_g604758e_open.3
- Fix udev rule issues
- Resolves: bz1785112

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-26_g604758e_open.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Honggang Li <honli@redhat.com> - 3.3-26_g604758e_open.1
- Fix FTBFS issue for Fedora rawhide/f30
- Resolves: 1675150

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-22_g4abbc60_open.6.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-22_g4abbc60_open.6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Feb 24 2018 Honggang Li <honli@redhat.com> - 3.3-22_g4abbc60_open.6
- Fix partial injection of Fedora build flags.
- Double the sizeof array fdesc to fix a gcc7 compiling issue.
- Resolves: bz1548537

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-22_g4abbc60_open.5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan  4 2018 Honggang Li <honli@redhat.com> - 3.3-22_g4abbc60_open.5
- No longer obsoletes libpsm2-compat.
- Resolves: bz1530982

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-22_g4abbc60_open.4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-22_g4abbc60_open.4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 21 2017 Honggang Li <honli@redhat.com> - 3.3-22_g4abbc60_open.4
- Include sysmacros.
- Extend buffer for two arrays.
- Resolves: bz1423739

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-22_g4abbc60_open.3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 31 2016 Honggang Li <honli@redhat.com> - 3.3-22_g4abbc60_open.3
- Obsoletes libpsm2-compat.

* Wed Apr 20 2016 Honggang Li <honli@redhat.com> - 3.3-22_g4abbc60_open.2
- Honors RPM_OPT_FLAGS.
- Link against system libuuid package.
- Remove duplicated Conflicts tags.

* Mon Apr 18 2016 Honggang Li <honli@redhat.com> - 3.3-22_g4abbc60_open.1
- Import infinipath-psm for Fedora.
