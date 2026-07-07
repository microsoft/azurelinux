# kmod-isert.inc — NVIDIA / Mellanox iSERT kernel modules
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.comp.toml overlays.
#
# Requires these defines/sources in kernel.spec (injected via comp.toml overlays):
#   mlnx_ofa_version  — source tag (e.g. 26.04)
#   mlnx_ofa_release  — vendor release stamp (e.g. OFED.26.04.0.8.5.1)
#   SOURCE6100        — MLNX_OFED_SRC-%{mlnx_ofa_version}-%{mlnx_ofa_bundle_release}.tgz bundle

# =========================================================================
# Phase: package — subpackage declaration
# =========================================================================
%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
%package -n kmod-%{_kmod_name}-%{mlnx_ofa_version}
Summary:        isert Driver
AutoReq:        no
Provides:       kmod-%{_kmod_name} = %{version}-%{release}
Provides:       isert-modules = %{version}-%{release}
Provides:       kmod-isert = %{version}-%{release}
Provides:       kmod-isert-uname-r = %{KVERREL}
Obsoletes:      kmod-isert < %{version}-%{release}
Provides:       installonlypkg(kernel-module)
Requires:       kmod-mlnx-ofa_kernel-%{mlnx_ofa_version} = %{version}-%{release}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires:       kmod-isert-matched = %{version}-%{release}
Requires(post): kmod
Requires(postun): kmod

%description -n kmod-%{_kmod_name}-%{mlnx_ofa_version}
Mellanox iSERT kernel modules built from isert %{mlnx_ofa_version}
(%{mlnx_ofa_release}) against kernel %{KVERREL}.

%package -n kmod-isert-matched
Summary:        Meta package to ensure kmod-isert is installed for all kernels

%description -n kmod-isert-matched
This meta package provides a single reference that other packages can Require
to have kmod-isert installed for all kernels. When installed, the kernel
package automatically pulls in the version-matched kmod-isert for each kernel
version on this machine (x86_64 and aarch64 only).

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
rpm2cpio "$_isert_srpm" | cpio -idm '*isert-%{mlnx_ofa_version}.tgz'
tar -xf isert-%{mlnx_ofa_version}.tgz
rm -rf MLNX_OFED_SRC-* isert-%{mlnx_ofa_version}.tgz
popd
%endif

%endif

# =========================================================================
# Phase: build — compile isert kernel modules
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building isert %{mlnx_ofa_version} modules for %{KVERREL}"}
pushd %{_builddir}/isert-%{mlnx_ofa_version}
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{mlnx_ofa_version}
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
pushd %{_builddir}/isert-%{mlnx_ofa_version}
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/isert
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{mlnx_ofa_version}
make install KERNELRELEASE=%{KVERREL}
popd
%endif

%endif

# =========================================================================
# Phase: files — scriptlets and file list
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n kmod-%{_kmod_name}-%{mlnx_ofa_version}
%{_sbindir}/depmod -a %{KVERREL} || :

%postun -n kmod-%{_kmod_name}-%{mlnx_ofa_version}
%{_sbindir}/depmod -a %{KVERREL} || :

%files -n kmod-%{_kmod_name}-%{mlnx_ofa_version}
/lib/modules/%{KVERREL}/extra/isert/

%files -n kmod-isert-matched
# empty sentinel package — no files
%endif

%endif
