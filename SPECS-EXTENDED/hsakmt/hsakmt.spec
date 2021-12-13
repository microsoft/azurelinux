Vendor:         Microsoft Corporation
Distribution:   Mariner
%global rocm_version 2.0.0
Name:           hsakmt
Version:        1.0.6
Release:        11%{?dist}
Summary:        AMD's HSA thunk library

License:        MIT
URL:            https://github.com/RadeonOpenCompute/ROCm
Source0:        https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface/archive/roc-%{rocm_version}.tar.gz
Patch0:         0001-Fix-install-targets.patch
Patch1:         0001-CMakeLists-Set-the-correct-default-version.patch
Patch2:         0001-Use-CFLAGS-and-LDFLAGS-specified-in-environment-vari.patch

ExclusiveArch: x86_64 aarch64
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires: cmake
BuildRequires: pciutils-devel
BuildRequires: numactl-devel

%if 0%{?epel} == 7
# We still the original cmake package on epel, because it provides the
# %%cmake macro.
BuildRequires: cmake3
%global __cmake %{_bindir}/cmake3
%endif

%description
This package includes the libhsakmt (Thunk) libraries
for AMD KFD


%package devel
Summary: AMD HSA thunk library development package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development library for hsakmt.

%prep
%autosetup -n  ROCT-Thunk-Interface-roc-%{rocm_version} -p1

%build
mkdir build
cd build

%cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
%make_build

%install
cd build
%make_install

rm %{buildroot}/usr/libhsakmt/LICENSE.md

%ldconfig_scriptlets

%files
%doc README.md
%license LICENSE.md
%{_libdir}/libhsakmt.so.%{version}
%{_libdir}/libhsakmt.so.1

%files devel
%{_libdir}/libhsakmt.so
%{_includedir}/libhsakmt/hsakmt.h
%{_includedir}/libhsakmt/hsakmttypes.h
%{_includedir}/libhsakmt/linux/kfd_ioctl.h

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.6-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-10.rocm2.0.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-9.rocm2.0.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-8.rocm2.0.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Tom Stellard <tstellar@redhat.com> - 1.0.6-7.rocm2.0.0
- ROCm 2.0.0 Release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-6.20171026git172d101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 23 2018 Tom Stellard <tstellar@redhat.com> - 1.0.6-5.20171026git172d101
- Fix build for epel7

* Mon Feb 12 2018 Tom Stellard <tstellar@redhat.com> - 1.0.6-4.20171026git172d101
- Fix build flag injection
- rhbz#1543787

* Fri Feb 09 2018 Tom Stellard <tstellar@redhat.com> - 1.0.6-3.20171026git172d101
- Build for aarch64

* Mon Feb 05 2018 Tom Stellard <tstellar@redhat.com> - 1.0.6-2.20171026git172d101
- Fix build with gcc 8

* Thu Oct 26 2017 Tom Stellard <tstellar@redhat.com> - 1.0.6-1.20171026git172d101
- Update with latest code from https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 13 2015 Oded Gabbay <oded.gabbay@gmail.com> 1.0.0-5
- Don't build for arm and i686

* Fri Nov 13 2015 Oded Gabbay <oded.gabbay@gmail.com> 1.0.0-4
- Rename package back to hsakmt

* Sun Nov 1 2015 Oded Gabbay <oded.gabbay@gmail.com> 1.0.0-3
- Rename package to libhsakmt

* Thu Oct 29 2015 Oded Gabbay <oded.gabbay@gmail.com> 1.0.0-2
- Changed doc to license
- Added GPLv2 to license
- Changed RPM_BUILD_ROOT to {buildroot}

* Sat Oct 24 2015 Oded Gabbay <oded.gabbay@gmail.com> 1.0.0-1
- Initial release of hsakmt, ver. 1.0.0

