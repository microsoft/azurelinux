# The MIT License (MIT)
# 
# Copyright (c) 2020 NVIDIA Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%global nvidia_driver_version 515.65.01
%global branch 515

Name:           nvidia-fabric-manager
Version:        %{nvidia_driver_version}
Release:        2%{?dist}
Summary:        Fabric Manager for NVSwitch based systems

License:        NVIDIA Proprietary
URL:            http://www.nvidia.com
Source0:        https://developer.download.nvidia.com/compute/cuda/redist/fabricmanager/linux-x86_64/fabricmanager-linux-%{_arch}-%{nvidia_driver_version}-archive.tar.xz

Provides:       nvidia-fabricmanager = %{nvidia_driver_version}
Provides:       nvidia-fabricmanager-%{branch} = %{nvidia_driver_version}
Obsoletes:      nvidia-fabricmanager-branch < %{nvidia_driver_version}
Obsoletes:      nvidia-fabricmanager

%description
Fabric Manager for NVIDIA NVSwitch based systems.

%package -n nvidia-fabric-manager-devel
Summary:        Fabric Manager API headers and associated library
# Normally we would have a dev package depend on its runtime package. However
# FM isn't a normal package. All the libs are in the dev package, and the
# runtime package is actually a service package.
Provides:       nvidia-fabricmanager-devel-%{branch} = %{nvidia_driver_version}
Obsoletes:      nvidia-fabricmanager-devel-branch < %{nvidia_driver_version}
Obsoletes:      nvidia-fabricmanager-devel

%description -n nvidia-fabric-manager-devel
Fabric Manager API headers and associated library

%prep
%setup -q -n fabricmanager-linux-%{_arch}-%{nvidia_driver_version}-archive

%build

%install
export DONT_STRIP=1

rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}/
cp -a bin/nv-fabricmanager %{buildroot}%{_bindir}/
cp -a bin/nvswitch-audit %{buildroot}%{_bindir}/

mkdir -p %{buildroot}/usr/lib/systemd/system
cp -a systemd/nvidia-fabricmanager.service  %{buildroot}/usr/lib/systemd/system

mkdir -p %{buildroot}/usr/share/nvidia/nvswitch
cp -a share/nvidia/nvswitch/*_topology %{buildroot}/usr/share/nvidia/nvswitch
cp -a etc/fabricmanager.cfg %{buildroot}/usr/share/nvidia/nvswitch

mkdir -p %{buildroot}%{_libdir}/
cp lib/libnvfm.so.1 %{buildroot}%{_libdir}/
cp lib/libnvfm.so %{buildroot}%{_libdir}/

mkdir -p %{buildroot}%{_includedir}/
cp include/nv_fm_agent.h %{buildroot}%{_includedir}/
cp include/nv_fm_types.h %{buildroot}%{_includedir}/

mkdir -p %{buildroot}/usr/share/doc/nvidia-fabricmanager/
cp -a LICENSE %{buildroot}/usr/share/doc/nvidia-fabricmanager/
cp -a third-party-notices.txt %{buildroot}/usr/share/doc/nvidia-fabricmanager/

%post -n nvidia-fabric-manager-devel -p /sbin/ldconfig

%postun -n nvidia-fabric-manager-devel -p /sbin/ldconfig

%files
%{_bindir}/*
/usr/lib/systemd/system/*
/usr/share/nvidia/nvswitch/*
%config(noreplace) /usr/share/nvidia/nvswitch/fabricmanager.cfg
/usr/share/doc/nvidia-fabricmanager/*

%files -n nvidia-fabric-manager-devel
%{_libdir}/*
%{_includedir}/*

%changelog
* Wed Dec 01 2022 Henry Li <lihl@microsoft.com> - 515.65.01-2
- Initial CBL-Mariner import from NVIDIA source (license: NVIDIA Proprietary)
- License verified
- Update Source0 field
- Include new macros for package version and branch info
- Update file path during the install section
- Remove cuda-drivers-fabricmanager and cuda-drivers-fabricmanager-%{branch} subpackages
  as they are not needed in CBL-Mariner

* Fri Jun 18 2021 Kevin Mittman <kmittman@nvidia.com>
- Rename packages

* Fri Jun 29 2018 Shibu Baby <sbaby@nvidia.com>
- Initial Fabric Manager RPM packaging