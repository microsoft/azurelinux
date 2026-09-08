%global debug_package %{nil}
%global _build_id_links none

%global cuda_major 13
%global cuda_minor 3
%global cudadir %{_prefix}/local/cuda-%{cuda_major}.%{cuda_minor}

%global __requires_exclude_from ^%{_prefix}/local/cuda-%{cuda_major}.%{cuda_minor}/compat/.*$
%global __provides_exclude_from ^%{_prefix}/local/cuda-%{cuda_major}.%{cuda_minor}/compat/.*$

Name:           cuda-compat
Version:        610.57.04
Release:        1%{?dist}
Summary:        CUDA Compatibility Platform
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html
Vendor:         NVIDIA
Packager:       NVIDIA

# AZL: upstream also ships aarch64, but only the x86_64 installer is currently
# vendored/verified here.
ExclusiveArch:  x86_64

# AZL: upstream Source0 is nvidia-driver-%{version}-x86_64.tar.xz, produced by
# NVIDIA's own nvidia-generate-tarballs.sh from the .run installer below. We
# vendor the installer directly and reproduce that extraction in %prep instead.
Source0:        NVIDIA-Linux-x86_64-%{version}.run

%description
Package containing all the necessary CUDA driver files related to forward 
compatibility. This compatibility enables newer CUDA runtimes to work with 
older display drivers.

%package        %{cuda_major}-%{cuda_minor}
Summary:        CUDA Compatibility Platform
Provides:       cuda-compat = %{cuda_major}.%{cuda_minor}

%description    %{cuda_major}-%{cuda_minor}
Package containing all the necessary CUDA driver files related to forward
compatibility. This compatibility enables newer CUDA runtimes to work with
older display drivers.

%prep
sh %{SOURCE0} --extract-only --target nvidia-driver-%{version}-x86_64
%setup -q -T -D -n nvidia-driver-%{version}-x86_64

%install
# Create empty tree
mkdir -p %{buildroot}%{cudadir}/compat

install -m 0755 -p \
  libcuda.so.%{version} \
  libcudadebugger.so.%{version} \
  libnvidia-gpucomp.so.%{version} \
  libnvidia-nvvm.so.%{version} \
  libnvidia-nvvm70.so.4 \
  libnvidia-ptxjitcompiler.so.%{version} \
  libnvidia-tileiras.so.%{version} \
  libnvidia-pkcs11-openssl3.so.%{version} \
  %{buildroot}%{cudadir}/compat/

ldconfig -vn %{buildroot}%{cudadir}/compat/

# Required for building against CUDA
ln -sf libcuda.so.1 %{buildroot}%{cudadir}/compat/libcuda.so

%files %{cuda_major}-%{cuda_minor}
%dir %{cudadir}
%dir %{cudadir}/compat
%{cudadir}/compat/libcuda.so
%{cudadir}/compat/libcuda.so.1
%{cudadir}/compat/libcuda.so.%{version}
%{cudadir}/compat/libcudadebugger.so.1
%{cudadir}/compat/libcudadebugger.so.%{version}
%{cudadir}/compat/libnvidia-gpucomp.so.%{version}
%{cudadir}/compat/libnvidia-nvvm.so.4
%{cudadir}/compat/libnvidia-nvvm.so.%{version}
%{cudadir}/compat/libnvidia-nvvm70.so.4
%{cudadir}/compat/libnvidia-ptxjitcompiler.so.1
%{cudadir}/compat/libnvidia-ptxjitcompiler.so.%{version}
%{cudadir}/compat/libnvidia-tileiras.so.%{version}
%{cudadir}/compat/libnvidia-pkcs11-openssl3.so.%{version}

%changelog
