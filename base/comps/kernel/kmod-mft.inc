# kmod-mft.inc - Mellanox Firmware Tools kernel modules
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.spec.
#
# Requires SOURCE6100, the MLNX_OFED source bundle, from which the kernel-mft
# source RPM and inner source archive are extracted.

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
Mellanox Firmware Tools kernel modules built for kernel %{KVERREL}.

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
rpm2cpio "$_mft_srpm" | cpio -idm './kernel-mft-%{mft_version}.tgz'
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
make %{?_smp_mflags} \
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
%endif

%endif

# =========================================================================
# Phase: files - scriptlets and file list
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n kernel-mft
%{_sbindir}/depmod -a %{KVERREL} || :

%postun -n kernel-mft
%{_sbindir}/depmod -a %{KVERREL} || :

%files -n kernel-mft
/lib/modules/%{KVERREL}/extra/mft/

%endif

%endif
