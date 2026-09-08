%global debug_package %{nil}
%global __strip /bin/true
# AZL: %install stages libs via a `cp -a lib*.so*` wildcard (unchanged from
# upstream), which copies more libraries into the buildroot than any
# subpackage's %files lists (GL/EGL/Wayland/GTK libs not shipped here). Those
# extras are intentionally left unpackaged rather than hand-curating the
# upstream wildcard.
%global _unpackaged_files_terminate_build 0

Name:           nvidia-driver
Version:        610.57.04
Release:        1%{?dist}
Summary:        NVIDIA's proprietary display driver for NVIDIA graphic cards
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html
Vendor:         NVIDIA
Packager:       NVIDIA

# AZL: upstream also ships aarch64, but only the x86_64 installer is currently
# vendored/verified here.
ExclusiveArch:  x86_64

# AZL: upstream Source0 is %{name}-%{version}-x86_64.tar.xz, produced by
# NVIDIA's own nvidia-generate-tarballs.sh (SOURCE90) from the .run installer
# below. We vendor the installer directly and reproduce that extraction in
# %prep instead.
Source0:        NVIDIA-Linux-x86_64-%{version}.run
Source2:        70-nvidia-driver.preset
Source13:       alternate-install-present

Source90:       nvidia-generate-tarballs.sh

BuildRequires:  systemd-rpm-macros

# https://packages.microsoft.com/cbl-mariner/2.0/prod/nvidia/x86_64/Packages/c/
Obsoletes:      cuda < %{version}
Provides:       cuda = %{version}

%description
This package provides the most recent NVIDIA display driver which allows for
hardware accelerated rendering with recent NVIDIA chipsets.

For the full product support list, please consult the release notes for driver
version %{version}.

%package cuda-libs
Summary:        Libraries for %{name}-cuda
# dlopened: libnvidia-cfg, libnvidia-gpucomp, libnvidia-ml
Requires:       %{name}-common%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cuda-libs
This package provides the CUDA libraries for %{name}-cuda.

%package cuda
Summary:        CUDA integration for %{name}
Requires:       %{name}-cuda-libs%{?_isa} = %{version}
Requires:       nvidia-kmod-common = %{version}
Requires:       nvidia-persistenced = %{version}
Requires:       opencl-filesystem
Requires:       ocl-icd

# https://packages.microsoft.com/cbl-mariner/2.0/prod/nvidia/x86_64/Packages/c/
Obsoletes:      cuda < %{version}
Provides:       cuda = %{version}

%description cuda
This package provides the CUDA integration components for %{name}.

%package common
Summary:        Common files and tools for NVIDIA driver
Obsoletes:      libnvidia-cfg < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      libnvidia-gpucomp < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      libnvidia-ml < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libnvidia-cfg = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libnvidia-gpucomp = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libnvidia-ml = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      nvlink5 < %{?epoch:%{epoch}:}%{version}-%{release}

%description common
This package contains various libraries and tools which are used by other driver
components in both desktop and compute only scenarios.

%prep
sh %{SOURCE0} --extract-only --target %{name}-%{version}-x86_64
%setup -q -T -D -n %{name}-%{version}-x86_64

# Create symlinks for shared objects
ldconfig -vn .

# Force creation of libnvidia-nvvm.so.4 for compatibility
ln -sf libnvidia-nvvm.so.%{version} libnvidia-nvvm.so.4

# Required for building gstreamer 1.0 NVENC plugins
ln -sf libnvidia-encode.so.%{version} libnvidia-encode.so

# Required for building ffmpeg 3.1 Nvidia CUVID
ln -sf libnvcuvid.so.%{version} libnvcuvid.so

# Required for building against CUDA
ln -sf libcuda.so.%{version} libcuda.so

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/nvidia/

# OpenCL config
install -p -m 0755 -D nvidia.icd %{buildroot}%{_sysconfdir}/OpenCL/vendors/nvidia.icd

# Binaries
mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 nvidia-{bug-report.sh,cuda-mps-control,cuda-mps-server,debugdump,powerd,smi} %{buildroot}%{_bindir}

# Man pages
mkdir -p %{buildroot}%{_mandir}/man1/
install -p -m 0644 nvidia-{smi,cuda-mps-control}*.gz %{buildroot}%{_mandir}/man1/

# Unique libraries
mkdir -p %{buildroot}%{_libdir}/
cp -a lib*.so* %{buildroot}%{_libdir}/

# systemd preset
install -p -m 0644 -D %{SOURCE2} %{buildroot}%{_systemd_util_dir}/system-preset/70-nvidia-driver.preset

# nvsandboxutils configuration
install -p -m 0644 -D sandboxutils-filelist.json %{buildroot}%{_datadir}/nvidia/files.d/sandboxutils-filelist.json

# nvidia-powerd
install -p -m 0644 -D systemd/system/nvidia-powerd.service %{buildroot}%{_unitdir}/nvidia-powerd.service
install -p -m 0644 -D nvidia-dbus.conf %{buildroot}%{_datadir}/dbus-1/system.d/nvidia-dbus.conf
install -p -m 0644 -D dlsnetparams.csv %{buildroot}%{_datadir}/nvidia/nvidia-powerd/dlsnetparams.csv
# Ignore powerd binary exiting if hardware is not present
# We should check for information in the DMI table
sed -i -e 's/ExecStart=/ExecStart=-/g' %{buildroot}%{_unitdir}/nvidia-powerd.service

%post common
%systemd_post nvidia-powerd.service

%preun common
%systemd_preun nvidia-powerd.service

%postun common
%systemd_postun nvidia-powerd.service

%files cuda
%license LICENSE
%doc NVIDIA_Changelog README.txt supported-gpus/supported-gpus.json
%{_sysconfdir}/OpenCL/vendors/*
%{_bindir}/nvidia-cuda-mps-control
%{_bindir}/nvidia-cuda-mps-server
%{_bindir}/nvidia-debugdump
%{_bindir}/nvidia-smi
%{_mandir}/man1/nvidia-cuda-mps-control.1.*
%{_mandir}/man1/nvidia-smi.*

%files cuda-libs
%{_datadir}/nvidia/files.d/sandboxutils-filelist.json
%{_libdir}/libcuda.so
%{_libdir}/libcuda.so.1
%{_libdir}/libcuda.so.%{version}
%{_libdir}/libcudadebugger.so.1
%{_libdir}/libcudadebugger.so.%{version}
%{_libdir}/libnvcuvid.so
%{_libdir}/libnvcuvid.so.1
%{_libdir}/libnvcuvid.so.%{version}
%{_libdir}/libnvidia-encode.so
%{_libdir}/libnvidia-encode.so.1
%{_libdir}/libnvidia-encode.so.%{version}
%{_libdir}/libnvidia-nvvm.so.4
%{_libdir}/libnvidia-nvvm.so.%{version}
%{_libdir}/libnvidia-nvvm70.so.4
%{_libdir}/libnvidia-opencl.so.1
%{_libdir}/libnvidia-opencl.so.%{version}
%{_libdir}/libnvidia-opticalflow.so.1
%{_libdir}/libnvidia-opticalflow.so.%{version}
%{_libdir}/libnvidia-ptxjitcompiler.so.1
%{_libdir}/libnvidia-ptxjitcompiler.so.%{version}
%{_libdir}/libnvidia-sandboxutils.so.1
%{_libdir}/libnvidia-sandboxutils.so.%{version}
%{_libdir}/libnvidia-tileiras.so.%{version}
%{_libdir}/libnvidia-pkcs11-openssl3.so.%{version}

%files common
%{_systemd_util_dir}/system-preset/70-nvidia-driver.preset
%{_unitdir}/nvidia-powerd.service
%{_bindir}/nvidia-bug-report.sh
%{_bindir}/nvidia-powerd
%{_datadir}/dbus-1/system.d/nvidia-dbus.conf
%{_datadir}/nvidia/nvidia-powerd
%{_libdir}/libnvidia-cfg.so.1
%{_libdir}/libnvidia-cfg.so.%{version}
%{_libdir}/libnvidia-gpucomp.so.%{version}
%{_libdir}/libnvidia-ml.so.1
%{_libdir}/libnvidia-ml.so.%{version}

%changelog
