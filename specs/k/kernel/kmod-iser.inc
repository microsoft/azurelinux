# kmod-iser.inc — NVIDIA / Mellanox iSER kernel modules
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
Requires:       mlnx-ofa_kernel-modules%{?_isa} = %{ofa_version}-%{ofa_release}.%{_azl_kver}.%{_azl_krel}
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

# AZL: mlnx-ofa_kernel ships a dummy ib_iser (zz01 override) and kernel-modules
# ships the in-tree one. Like upstream's iser.spec, add a zz02 override so a
# plain `modprobe ib_iser` loads this package's real module.
install -d %{buildroot}%{_sysconfdir}/depmod.d
cat > %{buildroot}%{_sysconfdir}/depmod.d/zz02-iser-%{KVERREL}.conf <<'DEPMOD_EOF'
override ib_iser %{KVERREL} weak-updates/iser
override ib_iser %{KVERREL} extra/iser
DEPMOD_EOF
%endif

%endif

# =========================================================================
# Phase: files — scriptlets and file list
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n iser
%{_sbindir}/depmod -a %{KVERREL} || :
# AZL: the zz02 override changes which ib_iser dracut embeds, so the initramfs
# must be rebuilt. Defer to %%posttrans (as kernel_modules_post does) unless
# kernel-core is installed in the same transaction; its posttrans runs dracut
# anyway. The stamp file is shared with mlnx-ofa_kernel-modules so a
# transaction touching both rebuilds the initramfs once.
if [ ! -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL} ]; then
    mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
    touch %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
fi

%posttrans -n iser
if [ -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL} ]; then
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || exit $?
fi

%postun -n iser
%{_sbindir}/depmod -a %{KVERREL} || :
# AZL: drop the removed module from this kernel's initramfs while the kernel is
# still installed (erased packages get no %%posttrans).
if [ -e /lib/modules/%{KVERREL}/vmlinuz ]; then
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || :
fi

%files -n iser
/lib/modules/%{KVERREL}/extra/iser/
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-iser-%{KVERREL}.conf

%endif

%endif
