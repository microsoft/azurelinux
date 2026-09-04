# kmod-srp.inc - Mellanox SRP kernel module
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.spec.
#
# Requires SOURCE6100, the MLNX OFED source bundle, from which the SRP source
# RPM and inner source archive are extracted.

%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
%global _azl_kver %{version}
%global _azl_krel %{release}

%package -n srp
Summary:        Mellanox SRP kernel module
Version:        %{ofa_version}
Release:        %{ofa_release}.%{_azl_kver}.%{_azl_krel}
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
Provides:       kmod-srp = %{ofa_version}-%{ofa_release}
Obsoletes:      kmod-srp < %{ofa_version}-%{ofa_release}
Provides:       srp-modules = %{ofa_version}-%{ofa_release}
Obsoletes:      srp-modules < %{ofa_version}-%{ofa_release}
Requires:       mlnx-ofa_kernel-modules = %{ofa_version}-%{ofa_release}
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod

%description -n srp
Mellanox SRP kernel module built from srp %{ofa_version} (%{ofa_release})
against kernel %{KVERREL}.

%endif

%endif

%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
pushd %{_builddir}
tar -xf %{SOURCE6100}
_srp_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/srp-*.src.rpm' -print -quit)
if [ -z "$_srp_srpm" ]; then
    echo "ERROR: SRP source RPM not found inside %{SOURCE6100}" >&2
    exit 1
fi
rpm2cpio "$_srp_srpm" | cpio -idm './srp-%{ofa_version}.tgz'
tar -xf srp-%{ofa_version}.tgz
rm -rf MLNX_OFED_SRC-* srp-%{ofa_version}.tgz
popd
%endif

%endif

%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building SRP %{ofa_version} module for %{KVERREL}"}
pushd %{_builddir}/srp-%{ofa_version}
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj/default
export INSTALL_MOD_DIR=extra/srp
make
popd
%endif

%endif

%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing SRP module for %{KVERREL}"}
pushd %{_builddir}/srp-%{ofa_version}
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/srp
export K_BUILD=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
export KVER=%{KVERREL}
export OFA_DIR=%{_builddir}/mlnx-ofa_kernel-%{ofa_version}/obj/default
make install
popd
%endif

%endif

%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n srp
%{_sbindir}/depmod -a %{KVERREL} || :

%postun -n srp
%{_sbindir}/depmod -a %{KVERREL} || :

%files -n srp
/lib/modules/%{KVERREL}/extra/srp/

%endif

%endif
