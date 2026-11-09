# kmod-srp.inc - NVIDIA / Mellanox SCSI RDMA Protocol (SRP) kernel modules
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.spec.
#
# Requires these defines/sources in kernel.spec:
#   ofa_version - source tag (e.g. 26.04)
#   ofa_release - vendor release stamp (e.g. OFED.26.04.0.8.5.1)
#   SOURCE6100  - MLNX_OFED_SRC-%{ofa_bundle_version}-%{ofa_vendor_release}.tgz bundle

# =========================================================================
# Phase: package - subpackage declaration
# =========================================================================
%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
%global _azl_kver %{version}
%global _azl_krel %{release}

%package -n srp
Summary:        Mellanox SRP kernel modules
License:        GPL-2.0-only
Version:        %{ofa_version}
Release:        %{ofa_release}.%{_azl_kver}.%{_azl_krel}
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
Provides:       kmod-srp = %{ofa_version}-%{ofa_release}
Obsoletes:      kmod-srp < %{ofa_version}-%{ofa_release}
Provides:       srp-modules = %{ofa_version}-%{ofa_release}
Obsoletes:      srp-modules < %{ofa_version}-%{ofa_release}
Requires:       mlnx-ofa_kernel-modules%{?_isa} = %{ofa_version}-%{ofa_release}.%{_azl_kver}.%{_azl_krel}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod

%description -n srp
Mellanox SCSI RDMA Protocol (SRP) kernel modules built from srp %{ofa_version}
(%{ofa_release}) against kernel %{KVERREL}.

%endif

%endif

# =========================================================================
# Phase: prep - extract srp tarball from MLNX_OFED_SRC bundle
# =========================================================================
%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
pushd %{_builddir}
tar -xf %{SOURCE6100}
_srp_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/srp-*.src.rpm' -print -quit)
if [ -z "$_srp_srpm" ]; then
    echo "ERROR: SRP source RPM not found inside %{SOURCE6100}" >&2
    exit 1
fi
rpm2cpio "$_srp_srpm" | cpio -idm '*srp-%{ofa_version}.tgz'
tar -xf srp-%{ofa_version}.tgz
rm -rf MLNX_OFED_SRC-* srp-%{ofa_version}.tgz
popd
%endif

%endif

# =========================================================================
# Phase: build - compile SRP kernel modules
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building SRP %{ofa_version} modules for %{KVERREL}"}
pushd %{_builddir}/srp-%{ofa_version}
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj/default
export INSTALL_MOD_DIR=extra/srp
make
popd
%endif

%endif

# =========================================================================
# Phase: install - install SRP modules
# =========================================================================
%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing SRP modules for %{KVERREL}"}
pushd %{_builddir}/srp-%{ofa_version}
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/srp
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj/default
make install KERNELRELEASE=%{KVERREL}
popd

# Prefer these modules over the OFED dummy and in-tree SRP modules.
install -d %{buildroot}%{_sysconfdir}/depmod.d
cat > %{buildroot}%{_sysconfdir}/depmod.d/zz02-srp-%{KVERREL}.conf <<'DEPMOD_EOF'
override ib_srp %{KVERREL} weak-updates/srp
override ib_srp %{KVERREL} extra/srp
override scsi_transport_srp %{KVERREL} weak-updates/srp/scsi
override scsi_transport_srp %{KVERREL} extra/srp/scsi
DEPMOD_EOF
%endif

%endif

# =========================================================================
# Phase: files - scriptlets and file list
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n srp
%{_sbindir}/depmod -a %{KVERREL} || :
if [ ! -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL} ]; then
    mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
    touch %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
fi

%posttrans -n srp
if [ -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL} ]; then
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || exit $?
fi

%postun -n srp
%{_sbindir}/depmod -a %{KVERREL} || :
# Erased packages have no posttrans; refresh the remaining kernel's initramfs.
if [ -e /lib/modules/%{KVERREL}/vmlinuz ]; then
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || :
fi

%files -n srp
/lib/modules/%{KVERREL}/extra/srp/
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-srp-%{KVERREL}.conf

%endif

%endif
