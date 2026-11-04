# kmod-mlnx-nfsrdma.inc — NVIDIA / Mellanox NFS/RDMA kernel modules
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.spec.
#
# Requires these defines/sources in kernel.spec:
#   ofa_version  — source tag (e.g. 26.04)
#   ofa_release  — vendor release stamp (e.g. OFED.26.04.0.8.5.1)
#   SOURCE6100   — MLNX_OFED_SRC-%{ofa_bundle_version}-%{ofa_vendor_release}.tgz bundle

# =========================================================================
# Phase: package — subpackage declaration
# =========================================================================
%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
%global _azl_kver %{version}
%global _azl_krel %{release}

%package -n mlnx-nfsrdma
Summary:        Mellanox NFS/RDMA kernel modules
Version:        %{ofa_version}
Release:        %{ofa_release}.%{_azl_kver}.%{_azl_krel}
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
Provides:       kmod-mlnx-nfsrdma = %{ofa_version}-%{ofa_release}
Obsoletes:      kmod-mlnx-nfsrdma < %{ofa_version}-%{ofa_release}
Provides:       mlnx-nfsrdma-modules = %{ofa_version}-%{ofa_release}
Obsoletes:      mlnx-nfsrdma-modules < %{ofa_version}-%{ofa_release}
Requires:       mlnx-ofa_kernel-modules%{?_isa} = %{ofa_version}-%{ofa_release}.%{_azl_kver}.%{_azl_krel}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod

%description -n mlnx-nfsrdma
Mellanox NFS/RDMA kernel modules built from mlnx-nfsrdma %{ofa_version}
(%{ofa_release}) against kernel %{KVERREL}.

%endif

%endif

# =========================================================================
# Phase: prep — extract mlnx-nfsrdma tarball from MLNX_OFED_SRC bundle
# =========================================================================
%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
pushd %{_builddir}
tar -xf %{SOURCE6100}
_nfsrdma_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/mlnx-nfsrdma-*.src.rpm' -print -quit)
if [ -z "$_nfsrdma_srpm" ]; then
    echo "ERROR: mlnx-nfsrdma SRPM not found inside %{SOURCE6100}" >&2
    exit 1
fi
rpm2cpio "$_nfsrdma_srpm" | cpio -idm './mlnx-nfsrdma-%{ofa_version}.tgz'
tar -xf mlnx-nfsrdma-%{ofa_version}.tgz
rm -rf MLNX_OFED_SRC-* mlnx-nfsrdma-%{ofa_version}.tgz
popd
%endif

%endif

# =========================================================================
# Phase: build — compile mlnx-nfsrdma kernel modules
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building mlnx-nfsrdma %{ofa_version} modules for %{KVERREL}"}
pushd %{_builddir}/mlnx-nfsrdma-%{ofa_version}
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj/default
export INSTALL_MOD_DIR=extra/mlnx-nfsrdma
make
popd
%endif

%endif

# =========================================================================
# Phase: install — install mlnx-nfsrdma modules
# =========================================================================
%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing mlnx-nfsrdma modules for %{KVERREL}"}
pushd %{_builddir}/mlnx-nfsrdma-%{ofa_version}
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/mlnx-nfsrdma
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj/default
make install KERNELRELEASE=%{KVERREL}
popd

# Prefer these modules over the OFED dummy modules selected by zz01.
install -d %{buildroot}%{_sysconfdir}/depmod.d
cat > %{buildroot}%{_sysconfdir}/depmod.d/zz02-mlnx-nfsrdma-%{KVERREL}.conf <<'DEPMOD_EOF'
override rpcrdma %{KVERREL} weak-updates/mlnx-nfsrdma
override rpcrdma %{KVERREL} extra/mlnx-nfsrdma
override xprtrdma %{KVERREL} weak-updates/mlnx-nfsrdma
override xprtrdma %{KVERREL} extra/mlnx-nfsrdma
override svcrdma %{KVERREL} weak-updates/mlnx-nfsrdma
override svcrdma %{KVERREL} extra/mlnx-nfsrdma
DEPMOD_EOF
%endif

%endif

# =========================================================================
# Phase: files — scriptlets and file list
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n mlnx-nfsrdma
%{_sbindir}/depmod -a %{KVERREL} || :
if [ ! -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL} ]; then
    mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
    touch %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
fi

%posttrans -n mlnx-nfsrdma
if [ -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL} ]; then
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || exit $?
fi

%postun -n mlnx-nfsrdma
%{_sbindir}/depmod -a %{KVERREL} || :
# Erased packages have no posttrans; refresh the remaining kernel's initramfs.
if [ -e /lib/modules/%{KVERREL}/vmlinuz ]; then
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || :
fi

%files -n mlnx-nfsrdma
/lib/modules/%{KVERREL}/extra/mlnx-nfsrdma/
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-mlnx-nfsrdma-%{KVERREL}.conf

%endif

%endif
