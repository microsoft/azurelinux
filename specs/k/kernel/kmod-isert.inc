# kmod-isert.inc — NVIDIA / Mellanox iSERT target (iSERT) kernel modules
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.spec.
#
# Requires these defines/sources in kernel.spec:
#   ofa_version  — source tag (e.g. 26.04)
#   ofa_release  — vendor release stamp (e.g. OFED.26.04.0.8.5.1)
#   SOURCE6100   — MLNX_OFED_SRC-%{ofa_version}-%{ofa_vendor_release}.tgz bundle

# =========================================================================
# Phase: package — subpackage declaration
# =========================================================================
%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
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
Requires:       mlnx-ofa_kernel-modules%{?_isa} = %{ofa_version}-%{ofa_release}.%{_azl_kver}.%{_azl_krel}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod

%description -n isert
Mellanox iSER target (iSERT) kernel modules built from isert %{ofa_version}
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

# AZL: mlnx-ofa_kernel ships a dummy ib_isert (zz01 override) and kernel-modules
# ships the in-tree one. Like upstream's isert.spec, add a zz02 override so a
# plain `modprobe ib_isert` loads this package's real module.
install -d %{buildroot}%{_sysconfdir}/depmod.d
cat > %{buildroot}%{_sysconfdir}/depmod.d/zz02-isert-%{KVERREL}.conf <<'DEPMOD_EOF'
override ib_isert %{KVERREL} weak-updates/isert
override ib_isert %{KVERREL} extra/isert
DEPMOD_EOF
%endif

%endif

# =========================================================================
# Phase: files — scriptlets and file list
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n isert
%{_sbindir}/depmod -a %{KVERREL} || :
if [ ! -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL} ]; then
    mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
    touch %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
fi

%posttrans -n isert
if [ -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL} ]; then
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || exit $?
fi

%postun -n isert
%{_sbindir}/depmod -a %{KVERREL} || :
# AZL: drop the removed module from this kernel's initramfs while the kernel is
# still installed (erased packages get no %%posttrans).
if [ -e /lib/modules/%{KVERREL}/vmlinuz ]; then
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || :
fi

%files -n isert
/lib/modules/%{KVERREL}/extra/isert/
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-isert-%{KVERREL}.conf

%endif

%endif
