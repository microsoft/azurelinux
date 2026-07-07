# kmod-iser.inc — NVIDIA / Mellanox iSER kernel modules
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
Summary:        iser Driver
AutoReq:        no
Provides:       kmod-%{_kmod_name} = %{version}-%{release}
Provides:       iser-modules = %{version}-%{release}
Provides:       kmod-iser = %{version}-%{release}
Provides:       kmod-iser-uname-r = %{KVERREL}
Obsoletes:      kmod-iser < %{version}-%{release}
Provides:       installonlypkg(kernel-module)
Requires:       kmod-mlnx-ofa_kernel-%{mlnx_ofa_version} = %{version}-%{release}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires:       kmod-iser-matched = %{version}-%{release}
Requires(post): kmod
Requires(postun): kmod

%description -n kmod-%{_kmod_name}-%{mlnx_ofa_version}
Mellanox iSER kernel modules built from iser %{mlnx_ofa_version}
(%{mlnx_ofa_release}) against kernel %{KVERREL}.

%package -n kmod-iser-matched
Summary:        Meta package to ensure kmod-iser is installed for all kernels

%description -n kmod-iser-matched
This meta package provides a single reference that other packages can Require
to have kmod-iser installed for all kernels. When installed, the kernel
package automatically pulls in the version-matched kmod-iser for each kernel
version on this machine (x86_64 and aarch64 only).

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
rpm2cpio "$_iser_srpm" | cpio -idm '*iser-%{mlnx_ofa_version}.tgz'
tar -xf iser-%{mlnx_ofa_version}.tgz
rm -rf MLNX_OFED_SRC-* iser-%{mlnx_ofa_version}.tgz
popd
%endif

%endif

# =========================================================================
# Phase: build — compile iser kernel modules
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building iser %{mlnx_ofa_version} modules for %{KVERREL}"}
pushd %{_builddir}/iser-%{mlnx_ofa_version}
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{mlnx_ofa_version}
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
pushd %{_builddir}/iser-%{mlnx_ofa_version}
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/iser
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
/lib/modules/%{KVERREL}/extra/iser/

%files -n kmod-iser-matched
# empty sentinel package — no files
%endif

%endif
