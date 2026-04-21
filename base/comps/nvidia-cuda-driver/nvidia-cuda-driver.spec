%global debug_package %{nil}
# Prebuilt proprietary binaries — do not strip or modify
%global __strip /bin/true
%global __brp_ldconfig %{nil}

%global nvidia_driver_version 595.58.03
%global nvidia_libdir %{_libdir}
%global nvidia_bindir %{_bindir}
%global nvidia_fwdir  /lib/firmware/nvidia/%{nvidia_driver_version}
%global nvidia_datadir %{_datadir}/nvidia

Name:           nvidia-cuda-driver
Version:        %{nvidia_driver_version}
Release:        1%{?dist}
Summary:        NVIDIA user-space GPU driver components
License:        NVIDIA Proprietary
URL:            https://www.nvidia.com/en-us/drivers/
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
ExclusiveArch:  x86_64 aarch64

BuildRequires:  systemd-rpm-macros

# Architecture-specific .run installer
# x86_64: use no-compat32 variant (64-bit only, smaller download)
# aarch64: single variant (no 32-bit compat layer on ARM)
%ifarch x86_64
Source0:        https://us.download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-no-compat32.run
%endif
%ifarch aarch64
Source0:        https://us.download.nvidia.com/XFree86/Linux-aarch64/%{version}/NVIDIA-Linux-aarch64-%{version}.run
%endif

# nvidia-persistenced systemd unit
Source1:        nvidia-persistenced.service

# Persistent software state directory for the NVIDIA driver
Source2:        tmpfiles-nvidia.conf

# Configuration file to register the NVIDIA OpenCL ICD with the ICD loader
Source3:        nvidia.icd

Requires:       kmod-nvidia-open = %{version}
Requires:       nvidia-cuda-driver-libs%{?_isa} = %{version}-%{release}
Requires:       nvidia-cuda-driver-firmware = %{version}-%{release}

%description
User-space NVIDIA GPU driver components for headless CUDA workloads on
Azure Linux.

This package is the companion to kmod-nvidia-open (which provides the open-source
NVIDIA kernel modules). It installs the proprietary user-space libraries,
management tools, and firmware needed to run CUDA applications on NVIDIA
GPUs (Turing and later).

This is a compute-only package — no graphics, X11, Vulkan, or display
components are included. Azure Linux is a headless distro.

# ---------------------------------------------------------------------------
# Sub-packages
# ---------------------------------------------------------------------------

%package libs
Summary:        NVIDIA CUDA driver shared libraries (compute-only)
Requires:       libelf

%description libs
Core NVIDIA shared libraries for headless GPU compute, including the CUDA
runtime, NVML management library, PTX JIT compiler, NVVM compiler, OpenCL
implementation, and hardware video encode/decode (NVENC/NVCUVID).

No OpenGL, EGL, Vulkan, or display libraries are included.

%package firmware
Summary:        NVIDIA GSP firmware
# Firmware is architecture-independent content but packaged per-arch
# because it is extracted from an arch-specific installer.

%description firmware
GPU System Processor (GSP) firmware images for NVIDIA GPUs. These are
required by the NVIDIA kernel modules to offload tasks to the GPU's
on-board processor.

%package tools
Summary:        NVIDIA GPU management and diagnostic tools
Requires:       nvidia-cuda-driver-libs%{?_isa} = %{version}-%{release}

%description tools
Command-line tools for managing and monitoring NVIDIA GPUs:
  - nvidia-smi                 (system management interface)
  - nvidia-persistenced        (persistence daemon)
  - nvidia-cuda-mps-control    (multi-process service control)
  - nvidia-cuda-mps-server     (multi-process service server)
  - nvidia-debugdump           (GPU state dump for bug reports)
  - nvidia-bug-report.sh       (automated bug report generator)
  - nvidia-modprobe            (kernel module loader / device node creator)

%package devel
Summary:        NVIDIA CUDA driver development symlinks
Requires:       nvidia-cuda-driver-libs%{?_isa} = %{version}-%{release}

%description devel
Unversioned .so symlinks for linking against NVIDIA CUDA driver libraries
at build time (compute-only — no graphics libraries).

# ---------------------------------------------------------------------------
# Prep — extract the self-extracting .run archive
# ---------------------------------------------------------------------------

%prep
# The .run file is a shell-based self-extracting archive.
# --extract-only: extract without running the installer
# --target: directory name for the extracted contents
sh %{SOURCE0} --extract-only --target nvidia-installer
cd nvidia-installer

# ---------------------------------------------------------------------------
# Build — nothing to build, all binaries are prebuilt
# ---------------------------------------------------------------------------

%build
# Prebuilt proprietary binaries — nothing to compile.

# ---------------------------------------------------------------------------
# Install — compute-only components (no graphics/display)
# ---------------------------------------------------------------------------

%install
cd nvidia-installer

install -d %{buildroot}%{nvidia_libdir}
install -d %{buildroot}%{nvidia_bindir}
install -d %{buildroot}%{nvidia_fwdir}
install -d %{buildroot}%{nvidia_datadir}
install -d %{buildroot}%{_sysconfdir}/OpenCL/vendors
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_tmpfilesdir}

# -- Core CUDA and compute libraries --
for lib in \
    libcuda.so.%{version} \
    libnvidia-ml.so.%{version} \
    libnvidia-ptxjitcompiler.so.%{version} \
    libnvidia-nvvm.so.%{version} \
    libnvidia-opencl.so.%{version} \
    libnvidia-cfg.so.%{version} \
    libnvidia-tls.so.%{version} \
    libnvidia-gpucomp.so.%{version} \
    libnvidia-pkcs11.so.%{version} \
    libnvidia-pkcs11-openssl3.so.%{version} \
    libcudadebugger.so.%{version} \
; do
    if [ -f "$lib" ]; then
        install -m 0755 "$lib" %{buildroot}%{nvidia_libdir}/
    fi
done

# -- Video encode/decode libraries (headless compute pipelines) --
for lib in \
    libnvcuvid.so.%{version} \
    libnvidia-encode.so.%{version} \
    libnvidia-opticalflow.so.%{version} \
; do
    if [ -f "$lib" ]; then
        install -m 0755 "$lib" %{buildroot}%{nvidia_libdir}/
    fi
done

# -- Versioned soname symlinks --
ln -sf libcuda.so.%{version}                    %{buildroot}%{nvidia_libdir}/libcuda.so.1
ln -sf libnvidia-ml.so.%{version}               %{buildroot}%{nvidia_libdir}/libnvidia-ml.so.1
ln -sf libnvidia-ptxjitcompiler.so.%{version}   %{buildroot}%{nvidia_libdir}/libnvidia-ptxjitcompiler.so.1
ln -sf libnvidia-nvvm.so.%{version}               %{buildroot}%{nvidia_libdir}/libnvidia-nvvm.so.4
ln -sf libnvidia-opencl.so.%{version}           %{buildroot}%{nvidia_libdir}/libnvidia-opencl.so.1
ln -sf libnvidia-cfg.so.%{version}              %{buildroot}%{nvidia_libdir}/libnvidia-cfg.so.1
ln -sf libcudadebugger.so.%{version}            %{buildroot}%{nvidia_libdir}/libcudadebugger.so.1
ln -sf libnvcuvid.so.%{version}                 %{buildroot}%{nvidia_libdir}/libnvcuvid.so.1
ln -sf libnvidia-encode.so.%{version}           %{buildroot}%{nvidia_libdir}/libnvidia-encode.so.1
ln -sf libnvidia-opticalflow.so.%{version}      %{buildroot}%{nvidia_libdir}/libnvidia-opticalflow.so.1

# -- Unversioned development symlinks --
ln -sf libcuda.so.1                              %{buildroot}%{nvidia_libdir}/libcuda.so
ln -sf libnvidia-ml.so.1                         %{buildroot}%{nvidia_libdir}/libnvidia-ml.so
ln -sf libnvidia-ptxjitcompiler.so.1             %{buildroot}%{nvidia_libdir}/libnvidia-ptxjitcompiler.so
ln -sf libnvidia-nvvm.so.4                       %{buildroot}%{nvidia_libdir}/libnvidia-nvvm.so
ln -sf libnvidia-opencl.so.1                     %{buildroot}%{nvidia_libdir}/libnvidia-opencl.so
ln -sf libcudadebugger.so.1                      %{buildroot}%{nvidia_libdir}/libcudadebugger.so
ln -sf libnvcuvid.so.1                           %{buildroot}%{nvidia_libdir}/libnvcuvid.so
ln -sf libnvidia-encode.so.1                     %{buildroot}%{nvidia_libdir}/libnvidia-encode.so
ln -sf libnvidia-opticalflow.so.1                %{buildroot}%{nvidia_libdir}/libnvidia-opticalflow.so

# -- Tools / binaries (compute & management only) --
for bin in \
    nvidia-smi \
    nvidia-persistenced \
    nvidia-cuda-mps-control \
    nvidia-cuda-mps-server \
    nvidia-debugdump \
    nvidia-bug-report.sh \
    nvidia-modprobe \
; do
    if [ -f "$bin" ]; then
        install -m 0755 "$bin" %{buildroot}%{nvidia_bindir}/
    fi
done

# -- GSP firmware --
if [ -d "firmware" ]; then
    install -d %{buildroot}%{nvidia_fwdir}
    install -m 0644 firmware/gsp_*.bin %{buildroot}%{nvidia_fwdir}/
fi

# -- Data files (container runtime file list) --
if [ -f sandboxutils-filelist.json ]; then
    install -d %{buildroot}%{_datadir}/nvidia/files.d
    install -m 0644 sandboxutils-filelist.json %{buildroot}%{_datadir}/nvidia/files.d/
fi

# -- OpenCL ICD registration --
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/OpenCL/vendors/nvidia.icd

# -- systemd service for nvidia-persistenced --
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/nvidia-persistenced.service

# -- tmpfiles.d for /var/run/nvidia-persistenced --
install -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/nvidia.conf

# ---------------------------------------------------------------------------
# Post-install / uninstall scriptlets
# ---------------------------------------------------------------------------

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post tools
%systemd_post nvidia-persistenced.service

%preun tools
%systemd_preun nvidia-persistenced.service

%postun tools
%systemd_postun_with_restart nvidia-persistenced.service

# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------

%files
%license nvidia-installer/LICENSE
%doc nvidia-installer/README.txt
%{_sysconfdir}/OpenCL/vendors/nvidia.icd
%dir %{_datadir}/nvidia
%dir %{_datadir}/nvidia/files.d
%{_datadir}/nvidia/files.d/sandboxutils-filelist.json

%files libs
# Core CUDA / compute libraries
%{nvidia_libdir}/libcuda.so.%{version}
%{nvidia_libdir}/libcuda.so.1
%{nvidia_libdir}/libnvidia-ml.so.%{version}
%{nvidia_libdir}/libnvidia-ml.so.1
%{nvidia_libdir}/libnvidia-ptxjitcompiler.so.%{version}
%{nvidia_libdir}/libnvidia-ptxjitcompiler.so.1
%{nvidia_libdir}/libnvidia-nvvm.so.%{version}
%{nvidia_libdir}/libnvidia-nvvm.so.4
%{nvidia_libdir}/libnvidia-opencl.so.%{version}
%{nvidia_libdir}/libnvidia-opencl.so.1
%{nvidia_libdir}/libnvidia-cfg.so.%{version}
%{nvidia_libdir}/libnvidia-cfg.so.1
%{nvidia_libdir}/libnvidia-tls.so.%{version}
%{nvidia_libdir}/libnvidia-gpucomp.so.%{version}
%{nvidia_libdir}/libnvidia-pkcs11.so.%{version}
%{nvidia_libdir}/libnvidia-pkcs11-openssl3.so.%{version}
%{nvidia_libdir}/libcudadebugger.so.%{version}
%{nvidia_libdir}/libcudadebugger.so.1
# Video encode/decode (headless compute pipelines)
%{nvidia_libdir}/libnvcuvid.so.%{version}
%{nvidia_libdir}/libnvcuvid.so.1
%{nvidia_libdir}/libnvidia-encode.so.%{version}
%{nvidia_libdir}/libnvidia-encode.so.1
%{nvidia_libdir}/libnvidia-opticalflow.so.%{version}
%{nvidia_libdir}/libnvidia-opticalflow.so.1

%files firmware
%dir %{nvidia_fwdir}
%{nvidia_fwdir}/gsp_*.bin

%files tools
%{nvidia_bindir}/nvidia-smi
%{nvidia_bindir}/nvidia-persistenced
%{nvidia_bindir}/nvidia-cuda-mps-control
%{nvidia_bindir}/nvidia-cuda-mps-server
%{nvidia_bindir}/nvidia-debugdump
%{nvidia_bindir}/nvidia-bug-report.sh
%{nvidia_bindir}/nvidia-modprobe
%{_unitdir}/nvidia-persistenced.service
%{_tmpfilesdir}/nvidia.conf

%files devel
%{nvidia_libdir}/libcuda.so
%{nvidia_libdir}/libnvidia-ml.so
%{nvidia_libdir}/libnvidia-ptxjitcompiler.so
%{nvidia_libdir}/libnvidia-nvvm.so
%{nvidia_libdir}/libnvidia-opencl.so
%{nvidia_libdir}/libcudadebugger.so
%{nvidia_libdir}/libnvcuvid.so
%{nvidia_libdir}/libnvidia-encode.so
%{nvidia_libdir}/libnvidia-opticalflow.so

%changelog
* Fri Apr 10 2026 Elaheh Dehghani <edehghani@microsoft.com> - 595.58.03-1
- Initial Azure Linux 4.0 package (headless / compute-only)
- User-space NVIDIA GPU driver components for CUDA workloads
- Companion to kmod-nvidia-open (open-source kernel modules)
- Based on NVIDIA-Linux-x86_64-595.58.03 driver release
- No graphics/display components (X11, GLX, EGL, Vulkan, OptiX, NGX)
