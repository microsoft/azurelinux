# kmod-iser.inc — NVIDIA / Mellanox iSER kernel modules
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.comp.toml overlays.
#
# Requires these defines/sources in kernel.spec (injected via comp.toml overlays):
#   ofa_version  — source tag (e.g. 26.04)
#   ofa_release  — vendor release stamp (e.g. OFED.26.04.0.8.5.1)
#   SOURCE6100   — MLNX_OFED_SRC-%{ofa_version}-%{ofa_vendor_release}.tgz bundle

# =========================================================================
# Phase: package — subpackage declaration
# =========================================================================
%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
# Snapshot the kernel package NVR before our subpackages that set their own
# Version:/Release: (mlnx-ofa_kernel userspace, -modules and -source).
%global _azl_kver %{version}
%global _azl_krel %{release}

%package -n iser
Summary:        iser Driver
Version:        %{ofa_version}
Release:        %{ofa_release}.%{_azl_kver}.%{_azl_krel}
# Restore the kernel NVR macros clobbered by the Version/Release tags above so
# the kernel's own %files templates (which reference raw %{version}/%{release})
# resolve to the kernel NVR again.
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
Provides:       kmod-iser = %{ofa_version}-%{ofa_release}
Obsoletes:      kmod-iser < %{ofa_version}-%{ofa_release}
Provides:       iser-modules = %{ofa_version}-%{ofa_release}
Obsoletes:      iser-modules < %{ofa_version}-%{ofa_release}
Requires:       mlnx-ofa_kernel-modules = %{ofa_version}-%{ofa_release}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod

%description -n iser
Mellanox iSER kernel modules built from iser %{ofa_version}
(%{ofa_release}) against kernel %{KVERREL}.     

%endif

%endif

# =========================================================================
# Phase: prep — extract iser tarball from MLNX_OFED_SRC bundle
# =========================================================================
%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
pushd %{_builddir}
tar -xf %{SOURCE6100}
_iser_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/iser-*.src.rpm' -print -quit)
if [ -z "$_iser_srpm" ]; then
    echo "ERROR: iser SRPM not found inside %{SOURCE6100}" >&2
    exit 1
fi
rpm2cpio "$_iser_srpm" | cpio -idm '*iser-%{ofa_version}.tgz'
tar -xf iser-%{ofa_version}.tgz
rm -rf MLNX_OFED_SRC-* iser-%{ofa_version}.tgz
popd
%endif

%endif

# =========================================================================
# Phase: build — compile iser kernel modules
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building iser %{ofa_version} modules for %{KVERREL}"}
pushd %{_builddir}/iser-%{ofa_version}
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj/default
export INSTALL_MOD_DIR=extra/iser
make
popd
%endif

%endif

# =========================================================================
# Phase: install — install iser modules
# =========================================================================
%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing iser modules for %{KVERREL}"}
pushd %{_builddir}/iser-%{ofa_version}
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/iser
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj/default
make install KERNELRELEASE=%{KVERREL}
popd
%endif

%endif

# =========================================================================
# Phase: files — scriptlets and file list
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n iser
%{_sbindir}/depmod -a %{KVERREL} || :

%postun -n iser
%{_sbindir}/depmod -a %{KVERREL} || :

%files -n iser
/lib/modules/%{KVERREL}/extra/iser/

%endif

%endif
