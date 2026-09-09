%global debug_package %{nil}
%global __strip /bin/true

Name:           nvidia-fabric-manager
Version:        610.43.02
Release:        %autorelease
Summary:        Fabric Manager for NVSwitch based systems
License:        NVIDIA License
URL:            http://www.nvidia.com
Vendor:         NVIDIA
Packager:       NVIDIA

ExclusiveArch:  x86_64 aarch64

# NVIDIA's CUDA redist repo uses "sbsa" (not "aarch64") for the ARM64 tarball name.
%ifarch x86_64
%global fm_arch x86_64
%endif
%ifarch aarch64
%global fm_arch sbsa
%endif

# AZL: no fabricmanager release exactly matches the nvidia-open driver pin
# (610.57.04); 610.43.02 is the latest available in the same 610.x branch.
Source0:        https://developer.download.nvidia.com/compute/cuda/redist/fabricmanager/linux-%{fm_arch}/fabricmanager-linux-%{fm_arch}-%{version}-archive.tar.xz

BuildRequires:  systemd-devel

Provides:       nvidia-fabricmanager = %{version}
Obsoletes:      nvidia-fabricmanager < %{version}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Fabric Manager for NVIDIA NVSwitch based systems.

# Normally a devel package depends on its runtime package. Fabric Manager
# isn't a normal package though: all the libs/headers are in the devel
# package, and the base package is actually a service package.
%package devel
Summary:        Fabric Manager API headers and associated library
Provides:       nvidia-fabricmanager-devel = %{version}
Obsoletes:      nvidia-fabricmanager-devel < %{version}

%description devel
Fabric Manager API headers and associated library.

%prep
%setup -q -n fabricmanager-linux-%{fm_arch}-%{version}-archive

%build

%install
install -d %{buildroot}%{_bindir}
install -p -m 0755 -t %{buildroot}%{_bindir} \
    bin/nv-fabricmanager \
    bin/nvswitch-audit \
    bin/nvidia-fabricmanager-start.sh

install -d %{buildroot}%{_unitdir}
install -p -m 0644 -t %{buildroot}%{_unitdir} systemd/nvidia-fabricmanager.service

install -d %{buildroot}%{_datadir}/nvidia/nvswitch
cp -a share/nvidia/nvswitch/* %{buildroot}%{_datadir}/nvidia/nvswitch/
install -p -m 0644 -t %{buildroot}%{_datadir}/nvidia/nvswitch \
    etc/fabricmanager.cfg \
    etc/fabricmanager_multinode.cfg

install -d %{buildroot}%{_libdir}
install -p -m 0755 lib/libnvfm.so.1 %{buildroot}%{_libdir}/
ln -sf libnvfm.so.1 %{buildroot}%{_libdir}/libnvfm.so

install -d %{buildroot}%{_includedir}
install -p -m 0644 -t %{buildroot}%{_includedir} \
    include/nv_fm_agent.h \
    include/nv_fm_types.h

%post
%systemd_post nvidia-fabricmanager.service

%preun
%systemd_preun nvidia-fabricmanager.service

%postun
%systemd_postun_with_restart nvidia-fabricmanager.service

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%license LICENSE
%doc third-party-notices.txt
%{_bindir}/nv-fabricmanager
%{_bindir}/nvswitch-audit
%{_bindir}/nvidia-fabricmanager-start.sh
%{_unitdir}/nvidia-fabricmanager.service
%{_datadir}/nvidia/nvswitch/*
%config(noreplace) %{_datadir}/nvidia/nvswitch/fabricmanager.cfg
%config(noreplace) %{_datadir}/nvidia/nvswitch/fabricmanager_multinode.cfg

%files devel
%license LICENSE
%{_libdir}/libnvfm.so
%{_libdir}/libnvfm.so.1
%{_includedir}/nv_fm_agent.h
%{_includedir}/nv_fm_types.h

%changelog
%autochangelog
