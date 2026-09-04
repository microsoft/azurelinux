# kmod-isert.inc — NVIDIA / Mellanox iSERT kernel modules
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
# Snapshot the kernel package NVR before declaring the iSERT subpackage.
%global _azl_kver %{version}
%global _azl_krel %{release}

%package -n isert
Summary:        isert Driver
Version:        %{ofa_version}
Release:        %{ofa_release}.%{_azl_kver}.%{_azl_krel}
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
Provides:       kmod-isert = %{ofa_version}-%{ofa_release}
Obsoletes:      kmod-isert < %{ofa_version}-%{ofa_release}
Provides:       isert-modules = %{ofa_version}-%{ofa_release}
Obsoletes:      isert-modules < %{ofa_version}-%{ofa_release}
Requires:       mlnx-ofa_kernel-modules = %{ofa_version}-%{ofa_release}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod

%description -n isert
Mellanox iSERT kernel modules built from isert %{ofa_version}
(%{ofa_release}) against kernel %{KVERREL}.

%endif

%endif

# =========================================================================
# Phase: prep — extract isert tarball from MLNX_OFED_SRC bundle
# =========================================================================
%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
pushd %{_builddir}
tar -xf %{SOURCE6100}
_isert_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/isert-*.src.rpm' -print -quit)
if [ -z "$_isert_srpm" ]; then
    echo "ERROR: isert SRPM not found inside %{SOURCE6100}" >&2
    exit 1
fi
rpm2cpio "$_isert_srpm" | cpio -idm '*isert-%{ofa_version}.tgz'
tar -xf isert-%{ofa_version}.tgz
rm -rf MLNX_OFED_SRC-* isert-%{ofa_version}.tgz
popd
%endif

%endif

# =========================================================================
# Phase: build — compile isert kernel modules
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building isert %{ofa_version} modules for %{KVERREL}"}
pushd %{_builddir}/isert-%{ofa_version}
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj/default
export INSTALL_MOD_DIR=extra/isert
make
popd
%endif

%endif

# =========================================================================
# Phase: install — install isert modules
# =========================================================================
%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing isert modules for %{KVERREL}"}
pushd %{_builddir}/isert-%{ofa_version}
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/isert
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
%post -n isert
%{_sbindir}/depmod -a %{KVERREL} || :

%postun -n isert
%{_sbindir}/depmod -a %{KVERREL} || :

%files -n isert
/lib/modules/%{KVERREL}/extra/isert/
%endif

%endif
