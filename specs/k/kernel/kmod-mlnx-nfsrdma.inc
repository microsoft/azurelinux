# kmod-mlnx-nfsrdma.inc - Mellanox NFS/RDMA kernel modules
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.spec.
#
# Requires SOURCE6100, the MLNX OFED source bundle, from which the
# mlnx-nfsrdma source RPM and inner source archive are extracted.

%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
%global _azl_kver %{version}
%global _azl_krel %{release}

%package -n kmod-%{_kmod_name}
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
Requires:       mlnx-ofa_kernel-modules = %{ofa_version}-%{ofa_release}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod

%description -n kmod-%{_kmod_name}
Mellanox NFS/RDMA kernel modules built from mlnx-nfsrdma %{ofa_version}
(%{ofa_release}) against kernel %{KVERREL}.

%endif

%endif

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

%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing mlnx-nfsrdma modules for %{KVERREL}"}
pushd %{_builddir}/mlnx-nfsrdma-%{ofa_version}
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/mlnx-nfsrdma
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj/default
make install
popd
%endif

%endif

%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n kmod-%{_kmod_name}
%{_sbindir}/depmod -a %{KVERREL} || :

%postun -n kmod-%{_kmod_name}
%{_sbindir}/depmod -a %{KVERREL} || :

%files -n kmod-%{_kmod_name}
/lib/modules/%{KVERREL}/extra/mlnx-nfsrdma/

%endif

%endif
