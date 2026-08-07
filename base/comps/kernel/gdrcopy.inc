# gdrcopy.inc — GDRCopy userspace and prebuilt gdrdrv kernel module
#
# The kmod RPM NVR encodes GDRCopy, NVIDIA driver, and kernel versions:
# kmod-gdrcopy-<gdrcopy>-<nvidia>_<kernel-version>.<kernel-release>

# =========================================================================
# Phase: package — userspace and per-kernel subpackage declarations
# =========================================================================
%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
%global _azl_kver %{version}
%global _azl_krel %{release}

%package -n gdrcopy
Summary:        Low-latency GPU memory copy library
Version:        %{gdrcopy_version}
Release:        %{gdrcopy_release}%{?dist}
%global version %{_azl_kver}
%global release %{_azl_krel}

%description -n gdrcopy
GDRCopy provides low-overhead userspace mappings of NVIDIA GPU memory for
CPU-driven copies using GPUDirect RDMA facilities.

%package -n gdrcopy-devel
Summary:        Development files for GDRCopy
Version:        %{gdrcopy_version}
Release:        %{gdrcopy_release}%{?dist}
%global version %{_azl_kver}
%global release %{_azl_krel}
Requires:       gdrcopy%{?_isa} = %{gdrcopy_version}-%{gdrcopy_release}%{?dist}

%description -n gdrcopy-devel
Headers and linker files for applications that use the GDRCopy API.

%package -n kmod-gdrcopy
Summary:        GDRCopy kernel module for NVIDIA driver %{nvidia_open_version} and kernel %{KVERREL}
Version:        %{gdrcopy_version}
Release:        %{nvidia_open_version}_%{_azl_kver}.%{_azl_krel}
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
Provides:       gdrcopy-kmod = %{gdrcopy_version}
Provides:       kmod-gdrcopy-uname-r = %{KVERREL}
Provides:       installonlypkg(kernel-module)
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires:       kmod-nvidia-open = %{nvidia_open_version}-%{_azl_kver}.%{_azl_krel}
Requires:       gdrcopy%{?_isa} = %{gdrcopy_version}-%{gdrcopy_release}%{?dist}
Requires:       kmod-gdrcopy-matched
Requires(post): kmod
Requires(postun): kmod

%description -n kmod-gdrcopy
The GDRCopy gdrdrv kernel module built for NVIDIA open driver
%{nvidia_open_version} and kernel %{KVERREL}.

%package -n kmod-gdrcopy-matched
Summary:        Ensure kmod-gdrcopy is installed for each installed kernel
Version:        %{gdrcopy_version}
Release:        %{gdrcopy_release}%{?dist}
%global version %{_azl_kver}
%global release %{_azl_krel}

%description -n kmod-gdrcopy-matched
An opt-in marker that makes kernel package transactions install the matching
GDRCopy kernel module for each kernel.
%endif

%endif

# =========================================================================
# Phase: prep — extract GDRCopy source
# =========================================================================
%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
pushd %{_builddir}
tar -xf %{SOURCE6010}
popd
%endif

%endif

# =========================================================================
# Phase: build — build libgdrapi and gdrdrv
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building GDRCopy %{gdrcopy_version} for NVIDIA %{nvidia_open_version} and kernel %{KVERREL}"}
pushd %{_builddir}/gdrcopy-%{gdrcopy_version}
# TODO: Build and package gdrcopy_sanity once Nvidia provides CUDA userspace
# development packages for azl4.0 containing cuda.h and the link-time libcuda.so stub.
# Upstream builds it via the "exes" target; nvcc is additionally required if
# gdrcopy_pplat and the complete benchmark set are packaged.
%{__make} %{?_smp_mflags} lib
pushd src/gdrdrv
%{__make} %{?_smp_mflags} \
    KVER="%{KVERREL}" \
    KDIR="%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}" \
    NVIDIA_SRC_DIR="%{_builddir}/open-gpu-kernel-modules-%{nvidia_open_version}/kernel-open/nvidia" \
    NVIDIA_IS_OPENSOURCE=y \
    HAVE_VM_FLAGS_SET=y \
    HAVE_PROC_OPS=y \
    MAKE_PARAMS="CONFIG_OBJTOOL_WERROR="
popd
popd
%endif

%endif

# =========================================================================
# Phase: install — install userspace and the unsigned module into buildroot
# =========================================================================
%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
pushd %{_builddir}/gdrcopy-%{gdrcopy_version}
%{__make} lib_install \
    DESTDIR=%{buildroot} \
    prefix=%{_prefix} \
    libdir=%{_libdir}
install -D -m 0644 src/gdrdrv/gdrdrv.ko \
    %{buildroot}/lib/modules/%{KVERREL}/extra/gdrcopy/gdrdrv.ko
install -D -m 0644 LICENSE \
    %{buildroot}%{_datadir}/licenses/gdrcopy/LICENSE
install -D -m 0644 LICENSE \
    %{buildroot}%{_datadir}/licenses/kmod-gdrcopy-%{KVERREL}/LICENSE
popd
%endif

%endif

# =========================================================================
# Phase: files — scriptlets and file lists
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n kmod-gdrcopy
%{_sbindir}/depmod -a %{KVERREL} || :

%postun -n kmod-gdrcopy
%{_sbindir}/depmod -a %{KVERREL} || :

%files -n gdrcopy
%license %{_datadir}/licenses/gdrcopy/LICENSE
%{_libdir}/libgdrapi.so.*

%files -n gdrcopy-devel
%{_includedir}/gdrapi.h
%{_includedir}/gdrconfig.h
%{_libdir}/libgdrapi.so

%files -n kmod-gdrcopy
%license %{_datadir}/licenses/kmod-gdrcopy-%{KVERREL}/LICENSE
/lib/modules/%{KVERREL}/extra/gdrcopy/gdrdrv.ko.%{compext}

%files -n kmod-gdrcopy-matched
# Empty sentinel package.
%endif

%endif
