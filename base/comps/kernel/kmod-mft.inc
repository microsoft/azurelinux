# kmod-mft.inc - NVIDIA / Mellanox Firmware Tools (MFT) kernel modules
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.spec.
#
# Requires these defines/sources in kernel.spec:
#   SOURCE6100 - MLNX_OFED_SRC-%{ofa_bundle_version}-%{ofa_vendor_release}.tgz bundle
#
# The kernel-mft source RPM and inner source archive are extracted from that
# bundle. The modules build directly against the kernel tree and do not depend
# on mlnx-ofa_kernel.

# =========================================================================
# Phase: package - subpackage declaration
# =========================================================================
%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
%global mft_version 4.36.0
%global mft_release 147
%global _azl_kver %{version}
%global _azl_krel %{release}

%package -n kernel-mft
Summary:        Mellanox Firmware Tools kernel modules
License:        GPL-2.0-only OR Linux-OpenIB
Version:        %{mft_version}
Release:        %{mft_release}.%{_azl_kver}.%{_azl_krel}
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
Provides:       kmod-mft = %{mft_version}-%{mft_release}
Obsoletes:      kmod-mft < %{mft_version}-%{mft_release}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod

%description -n kernel-mft
Mellanox Firmware Tools (MFT) kernel modules built from kernel-mft
%{mft_version}-%{mft_release} against kernel %{KVERREL}: mst_pci and
mst_pciconf, plus bf3_livefish on aarch64.

%endif

%endif

# =========================================================================
# Phase: prep - extract kernel-mft from the MLNX_OFED source bundle
# =========================================================================
%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
pushd %{_builddir}
tar -xf %{SOURCE6100}
_mft_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/kernel-mft-*.src.rpm' -print -quit)
if [ -z "$_mft_srpm" ]; then
    echo "ERROR: kernel-mft SRPM not found inside %{SOURCE6100}" >&2
    exit 1
fi
rpm2cpio "$_mft_srpm" | cpio -idm '*kernel-mft-%{mft_version}.tgz'
tar -xf kernel-mft-%{mft_version}.tgz
rm -rf MLNX_OFED_SRC-* kernel-mft-%{mft_version}.tgz
popd
%endif

%endif

# =========================================================================
# Phase: build - compile kernel-mft modules
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building kernel-mft %{mft_version} modules for %{KVERREL}"}
pushd %{_builddir}/kernel-mft-%{mft_version}
mkdir source obj
find . -mindepth 1 -maxdepth 1 ! -name source ! -name obj -exec mv -t source {} +
cp -a source obj/default
pushd obj/default
# CPU_ARCH selects the arch-specific modules (bf3_livefish on aarch64); set it
# explicitly so the build matches the %%ifarch used when installing them.
make %{?_smp_mflags} \
    CPU_ARCH=%{_arch} \
    KSRC=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL} \
    KPVER=%{KVERREL}
popd
popd
%endif

%endif

# =========================================================================
# Phase: install - install kernel-mft modules
# =========================================================================
%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing kernel-mft modules for %{KVERREL}"}
install -d %{buildroot}/lib/modules/%{KVERREL}/extra/mft
install -m 0644 %{_builddir}/kernel-mft-%{mft_version}/obj/default/mst_backward_compatibility/mst_pci/mst_pci.ko \
    %{buildroot}/lib/modules/%{KVERREL}/extra/mft/
install -m 0644 %{_builddir}/kernel-mft-%{mft_version}/obj/default/mst_backward_compatibility/mst_pciconf/mst_pciconf.ko \
    %{buildroot}/lib/modules/%{KVERREL}/extra/mft/
%ifarch aarch64
install -m 0644 %{_builddir}/kernel-mft-%{mft_version}/obj/default/misc_drivers/bf3_livefish/bf3_livefish.ko \
    %{buildroot}/lib/modules/%{KVERREL}/extra/mft/
%endif
install -D -m 0644 %{_builddir}/kernel-mft-%{mft_version}/source/COPYING \
    %{buildroot}%{_datadir}/licenses/kernel-mft-%{KVERREL}/COPYING

_depmod_conf="%{buildroot}%{_sysconfdir}/depmod.d/zz02-kernel-mft-%{KVERREL}.conf"
install -d "$(dirname "$_depmod_conf")"
: > "$_depmod_conf"
find %{buildroot}/lib/modules/%{KVERREL}/extra/mft -type f -name '*.ko*' | sort | \
while read -r module; do
    ko_name=${module##*/}
    mod_name=${ko_name/.ko*/}
    echo "override ${mod_name} %{KVERREL} weak-updates/mft" >> "$_depmod_conf"
    echo "override ${mod_name} %{KVERREL} extra/mft" >> "$_depmod_conf"
done
%endif

%endif

# =========================================================================
# Phase: files - scriptlets and file list
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n kernel-mft
%{_sbindir}/depmod -a %{KVERREL} || :
if [ ! -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL} ]; then
    mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
    touch %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
fi

%posttrans -n kernel-mft
if [ -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL} ]; then
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || exit $?
fi

%postun -n kernel-mft
%{_sbindir}/depmod -a %{KVERREL} || :
if [ -e /lib/modules/%{KVERREL}/vmlinuz ]; then
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || :
fi

%files -n kernel-mft
%dir %{_datadir}/licenses/kernel-mft-%{KVERREL}
%license %{_datadir}/licenses/kernel-mft-%{KVERREL}/COPYING
/lib/modules/%{KVERREL}/extra/mft/
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-kernel-mft-%{KVERREL}.conf

%endif

%endif
