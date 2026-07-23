# mlnx-ofa_kernel.inc — NVIDIA / Mellanox OFED (mlnx-ofa_kernel), built inside the kernel
#
# Single include that builds BOTH the kernel modules and the userspace
# utilities inside the kernel SRPM, mirroring the upstream vendor spec
# (MLNX_OFED_SRC-*/SRPMS/mlnx-ofa_kernel.spec) build/install commands:
#   %build:   ./configure --build-dummy-mods ... && make kernel && make build_py_scripts
#   %install: make install_modules && make install_scripts
#
# Phases: package, prep, build, install, files
# Activated by setting _kmod_phase (+ _kmod_name) globals and %include-ing this
# file from kernel.comp.toml overlays (see the AZL-KMOD-*-ANCHOR wiring).
#
# Subpackages produced (DKMS intentionally omitted):
#   mlnx-ofa_kernel                  userspace CLI tools (version-namespaced under
#                                    /usr/libexec/mlnx-ofa/<ver>/; install-only, multi-version)
#   mlnx-ofa_kernel-common           system integration + /usr/bin selector wrappers (singleton)
#   mlnx-ofa_kernel-modules          kernel modules   (per-kernel; installonly + sentinel)
#   mlnx-ofa_kernel-modules-matched  opt-in sentinel  (auto kernel-upgrade tracking)
#   mlnx-ofa_kernel-devel            headers+symvers  (per-kernel; installonly)
#   mlnx-ofa_kernel-source           pristine source  (OFED-versioned singleton)
#
# Requires these defines/sources in kernel.spec (injected via comp.toml overlays):
#   mlnx_ofa_version  — driver tag (e.g. 26.04)
#   mlnx_ofa_release  — vendor release stamp (e.g. OFED.26.04.0.8.5.1)
#   SOURCE6100        — MLNX_OFED_SRC-<ver>-<bundle>.tgz bundle
#

# Version-namespaced install area for the multi-version userspace binaries.
# The versioned mlnx-ofa_kernel package installs its CLI tools under
# %{_mofa_libexec}/bin/; mlnx-ofa_kernel-common ships /usr/bin selector wrappers
# that exec the copy matching the running kernel (resolved via the per-kernel
# by-kernel/<uname-r> symlink dropped by mlnx-ofa_kernel-modules). Defined
# outside the phase guards so it is available in every include (package/install/files).
%global _mofa_ns      %{mlnx_ofa_version}-%{mlnx_ofa_release}
%global _mofa_base    %{_libexecdir}/mlnx-ofa
%global _mofa_libexec %{_mofa_base}/%{_mofa_ns}

# =========================================================================
# Phase: package — subpackage declarations
# =========================================================================
%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64

# Snapshot the kernel package NVR before our subpackages that set their own
# Version:/Release: (mlnx-ofa_kernel userspace, -modules and -source). RPM
# treats those as primary tags that redefine the global %{version}/%{release}
# macros for the remainder of the spec. Left unchecked that corrupts the
# kernel's own %files templates (e.g. kernel-core's
# %license COPYING-%{version}-%{release}) and our devel cross-Requires.
# We restore these macros right after each such subpackage below.
%global _azl_kver %{version}
%global _azl_krel %{release}

# -------------------------------------------------------------------------
# mlnx-ofa_kernel — userspace CLI tools, version-namespaced + install-only.
# All files live under %{_mofa_libexec}/ (no fixed system paths), so multiple
# OFED userspace versions coexist, one per kernel build. The system-integration
# files (systemd/udev/modprobe/configs) and the /usr/bin selector wrappers live
# in the singleton mlnx-ofa_kernel-common package instead.
# -------------------------------------------------------------------------
%package -n mlnx-ofa_kernel
Summary:        NVIDIA / Mellanox OFED userspace tools (mlnx-ofa_kernel %{mlnx_ofa_version}), version-namespaced
Version:        %{mlnx_ofa_version}
Release:        %{mlnx_ofa_release}%{?dist}
# Restore the kernel NVR macros clobbered by the Version/Release tags above,
# before any %{version}/%{release}/%{KVERREL} is used below or in later subpackages.
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
# Install-only so old versions are not erased on upgrade; the namespaced paths
# are what actually let versions coexist. The exact version-release is exported
# so the matching -modules can pin it precisely.
Provides:       installonlypkg(kernel-module)
Provides:       mlnx-ofa-userspace-version = %{mlnx_ofa_version}-%{mlnx_ofa_release}
Provides:       mlnx-ofa-userspace-release = %{mlnx_ofa_release}
Requires:       coreutils
Requires:       pciutils
Requires:       grep
Requires:       procps-ng
Requires:       lsof
Requires:       kmod

%description -n mlnx-ofa_kernel
Version-namespaced NVIDIA / Mellanox OFED userspace CLI tools (ibdev2netdev,
setup_mr_cache.sh, mlnx_interface_mgr.sh, mlnx_conf_mgr.sh) for mlnx-ofa_kernel
%{mlnx_ofa_version} (%{mlnx_ofa_release}), installed under %{_mofa_libexec}/.
Multiple versions coexist; mlnx-ofa_kernel-common provides the /usr/bin selector
wrappers that pick the copy matching the running kernel. The kernel modules ship
in the matching mlnx-ofa_kernel-modules package.

# -------------------------------------------------------------------------
# mlnx-ofa_kernel-common — singleton system integration + selector wrappers.
# Owns the files the OS only reads from fixed paths (systemd units, udev rules
# + helpers, modprobe configs, /etc/infiniband configs) plus the /usr/bin
# selector wrappers and the dispatcher. Inherits the kernel NVR (no own
# Version/Release) and is NOT install-only, so exactly one copy is installed and
# upgraded in place.
# -------------------------------------------------------------------------
%package -n mlnx-ofa_kernel-common
Summary:        NVIDIA / Mellanox OFED userspace system integration and version selector
AutoReq:        no
Requires:       coreutils
Requires:       kmod
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description -n mlnx-ofa_kernel-common
Version-independent userspace pieces of the NVIDIA / Mellanox OFED stack: the
openibd service, interface-manager systemd units, udev rules and helpers,
modprobe configuration, and the /usr/bin selector wrappers that dispatch to the
version-namespaced mlnx-ofa_kernel tools matching the running kernel. Exactly
one version is installed at a time.

# -------------------------------------------------------------------------
# mlnx-ofa_kernel-modules — the kernel modules (per-kernel).
# -------------------------------------------------------------------------
%package -n mlnx-ofa_kernel-modules
Summary:        NVIDIA / Mellanox OFED kernel modules (mlnx-ofa_kernel %{mlnx_ofa_version})
Version:        %{mlnx_ofa_version}
Release:        %{_azl_kver}.%{_azl_krel}
# Restore the kernel NVR macros clobbered by the Version/Release tags above,
# before %{KVERREL} (which expands %{release}) is used in the Provides/Requires below.
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
Provides:       mlnx-ofa-kmod-version = %{mlnx_ofa_version}
Provides:       mlnx-ofa-kmod-release = %{mlnx_ofa_release}
Provides:       mlnx-ofa_kernel-modules-uname-r = %{KVERREL}
Provides:       kmod-mlnx-ofa_kernel = %{mlnx_ofa_version}-%{mlnx_ofa_release}
Obsoletes:      kmod-mlnx-ofa_kernel < %{mlnx_ofa_version}-%{mlnx_ofa_release}
Provides:       installonlypkg(kernel-module)
Requires:       %{name}-core-uname-r = %{KVERREL}
# Pin the exact matching version-namespaced userspace, and pull the singleton
# system-integration + selector-wrapper package.
Requires:       mlnx-ofa-userspace-version = %{mlnx_ofa_version}-%{mlnx_ofa_release}
Requires:       mlnx-ofa_kernel-common
Requires(post): kmod
Requires(postun): kmod

%description -n mlnx-ofa_kernel-modules
NVIDIA / Mellanox InfiniBand and Ethernet (mlx5) kernel modules built from
mlnx-ofa_kernel %{mlnx_ofa_version} (%{mlnx_ofa_release}) against kernel
%{KVERREL}.

# Opt-in sentinel: when installed, the kernel package's conditional Requires
# pulls the version-matched mlnx-ofa_kernel-modules for every kernel on this
# machine. Nothing hard-requires it, so it stays a single passive marker.
%package -n mlnx-ofa_kernel-modules-matched
Summary:        Meta package to ensure mlnx-ofa_kernel-modules is installed for all kernels

%description -n mlnx-ofa_kernel-modules-matched
This meta package provides a single reference that other packages can Require
to have mlnx-ofa_kernel-modules installed for all kernels. When installed, the
kernel package automatically pulls in the version-matched mlnx-ofa_kernel-modules
for each kernel version on this machine (x86_64 and aarch64 only).

# -------------------------------------------------------------------------
# mlnx-ofa_kernel-devel — headers + Module.symvers + helper scripts, used to
# build out-of-tree modules (e.g. nvidia-peermem / GPUDirect) against this
# kmod.
# -------------------------------------------------------------------------
%package -n mlnx-ofa_kernel-devel
Summary:        Development files for mlnx-ofa_kernel (%{mlnx_ofa_version}, kernel %{KVERREL})
AutoReq:        no
Provides:       mlnx-ofa-kmod-devel-version = %{mlnx_ofa_version}
Provides:       mlnx-ofa-kmod-devel-release = %{mlnx_ofa_release}
Provides:       installonlypkg(kernel-module)
# Bind to this exact kernel's modules via the uname-r Provides rather than the
# modules NVR (whose Release now carries the OFED version, not the kernel NVR).
Requires:       mlnx-ofa_kernel-modules-uname-r = %{KVERREL}
Requires:       coreutils
Requires:       pciutils
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description -n mlnx-ofa_kernel-devel
Development files for mlnx-ofa_kernel: backport headers, compat layer,
Module.symvers, and the ofed_scripts helpers used by out-of-tree modules
(e.g. nvidia-peermem) that link against the mlnx-ofa NIC/RDMA stack rather
than the in-tree mlx5/RDMA drivers.

Files install under /usr/src/ofa_kernel/%{_arch}/%{KVERREL}/ and are tied to
the kernel build that produced them. Multiple kernel versions can coexist
(one devel tree per kernel build).

# -------------------------------------------------------------------------
# mlnx-ofa_kernel-source — pristine driver source (OFED-versioned singleton).
# -------------------------------------------------------------------------
%package -n mlnx-ofa_kernel-source
Summary:        Source of the NVIDIA / Mellanox OFED main kernel driver
Version:        %{mlnx_ofa_version}
Release:        %{mlnx_ofa_release}%{?dist}
# Restore the kernel NVR macros clobbered by the Version/Release tags above so
# the kernel's own %files templates (which reference raw %{version}/%{release})
# resolve to the kernel NVR again.
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no

%description -n mlnx-ofa_kernel-source
Pristine source of the mlnx-ofa_kernel %{mlnx_ofa_version} driver under
/usr/src/ofa_kernel-%{mlnx_ofa_version}/source/. Install this only to view the
driver sources; use mlnx-ofa_kernel-devel to build other drivers against it.
%endif

%endif

# =========================================================================
# Phase: prep — extract sources and lay out the upstream source/obj tree
# =========================================================================
%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
# %{SOURCE6100} is the MLNX_OFED_SRC bundle (a tar of every Mellanox OFED
# SRPM). We only need the mlnx-ofa_kernel SRPM, and from it only the
# mlnx-ofa_kernel-<v>.tgz source tarball.
pushd %{_builddir}
%{log_msg "Extracting MLNX_OFED_SRC bundle to fetch mlnx-ofa_kernel sources"}
tar -xf %{SOURCE6100}
_mofa_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/mlnx-ofa_kernel-*.src.rpm' \
    -print -quit)
if [ -z "$_mofa_srpm" ]; then
    echo "ERROR: mlnx-ofa_kernel SRPM not found inside %{SOURCE6100}" >&2
    exit 1
fi
rpm2cpio "$_mofa_srpm" | cpio -idm '*mlnx-ofa_kernel-%{mlnx_ofa_version}.tgz'
tar -xf mlnx-ofa_kernel-%{mlnx_ofa_version}.tgz
rm -rf MLNX_OFED_SRC-* mlnx-ofa_kernel-%{mlnx_ofa_version}.tgz

# Upstream %prep: apply OFED patches, autogen compat, then split into
# source/ (pristine) + obj/ (per-flavor build dirs).
pushd mlnx-ofa_kernel-%{mlnx_ofa_version}
ofed_scripts/ofed_patch.sh || true
if [ ! -f compat/configure ]; then (cd compat && ./autogen.sh); fi
set -- *
mkdir -p source
mv "$@" source/
mkdir -p obj
popd
popd
%endif

%endif

# =========================================================================
# Phase: build — configure + make kernel + make build_py_scripts (upstream)
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building mlnx-ofa_kernel %{mlnx_ofa_version} modules and py scripts for %{KVERREL}"}
pushd %{_builddir}/mlnx-ofa_kernel-%{mlnx_ofa_version}

export EXTRA_CFLAGS='-DVERSION=\"%{mlnx_ofa_version}\"'
export INSTALL_MOD_DIR=extra/mlnx-ofa_kernel
export CONF_OPTIONS="--with-core-mod --with-user_mad-mod --with-user_access-mod --with-addr_trans-mod --with-mlx5-mod --with-mlxfw-mod --with-ipoib-mod"

# Single flavor ("default") — mirrors upstream's non-KMP flavors_to_build.
_KSRC="%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}"
_LIB_MOD_DIR="/lib/modules/%{KVERREL}/${INSTALL_MOD_DIR}"
rm -rf obj/default
cp -a source obj/default
pushd obj/default

# Upstream stamps compat shims to a fixed epoch to satisfy autoconf/automake
# timestamp checks in the kbuild Makefiles.
find compat -type f -exec touch -t 200012201010 '{}' \; || true

# AZL: strip RH hardening specs and -fexceptions (mlnx-ofa fails to build with
# them), then force -fno-exceptions like the vendor spec's _hardened_cflags.
CFLAGS=$(echo "${CFLAGS}" \
    | sed -e 's|-specs=/usr/lib/rpm/redhat/redhat-hardened-cc1||g' \
          -e 's|-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1||g' \
          -e 's|-fexceptions||g')
export CFLAGS="${CFLAGS} -fno-exceptions"
unset CXXFLAGS
unset LDFLAGS

./configure \
    --build-dummy-mods \
    --prefix=%{_prefix} \
    --kernel-version "%{KVERREL}" \
    --kernel-sources "${_KSRC}" \
    --modules-dir "${_LIB_MOD_DIR}" \
    ${CONF_OPTIONS} \
    %{?_smp_mflags}

make %{?_smp_mflags} kernel
make build_py_scripts

popd
popd
%endif

%endif

# =========================================================================
# Phase: install — make install_modules + make install_scripts (upstream)
# =========================================================================
%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing mlnx-ofa_kernel %{mlnx_ofa_version} modules, userspace, devel and source for %{KVERREL}"}

export RECORD_PY_FILES=1
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/mlnx-ofa_kernel
_srcroot="%{_builddir}/mlnx-ofa_kernel-%{mlnx_ofa_version}"
_objdir="${_srcroot}/obj/default"

mkdir -p %{buildroot}%{_prefix}/src/ofa_kernel/%{_arch}

# AZL: `make install_modules` runs depmod, which rewrites the parent kernel's
# modules.{builtin,order,*}. Snapshot them first and restore afterwards so
# kernel-core's %files (which lists /lib/modules/%{KVERREL}/modules.builtin*)
# does not fail with "File not found".
_mods_dir="%{buildroot}/lib/modules/%{KVERREL}"
_mods_snap="%{_builddir}/mlnx-ofa-mods-snapshot"
rm -rf "$_mods_snap"
if [ -d "$_mods_dir" ]; then
    mkdir -p "$_mods_snap"
    find "$_mods_dir" -maxdepth 1 -name 'modules.*' -type f \
        -exec cp -a {} "$_mods_snap/" \;
fi

pushd "${_objdir}"
make install_modules KERNELRELEASE=%{KVERREL}
# Install userspace scripts + configuration files (openibd, udev rules,
# modprobe configs, ibdev2netdev, mlnx_ofed helpers, ...).
make install_scripts

# OFED's Makefile installs sbin tools (ibdev2netdev, setup_mr_cache.sh) to a
# literal /usr/sbin. AZL is usrmerged, so RPM's %{_sbindir} resolves to
# /usr/bin; relocate them so the packaged paths match %{_sbindir}.
if [ "%{_sbindir}" != "/usr/sbin" ] && [ -d "%{buildroot}/usr/sbin" ]; then
    mkdir -p "%{buildroot}%{_sbindir}"
    for _f in "%{buildroot}/usr/sbin"/*; do
        [ -e "${_f}" ] || continue
        mv "${_f}" "%{buildroot}%{_sbindir}/"
    done
    rmdir "%{buildroot}/usr/sbin" 2>/dev/null || :
fi

# --- AZL: version-namespace the userspace CLI tools ----------------------
# Relocate the standalone tools into %{_mofa_libexec}/bin so multiple OFED
# userspace versions coexist, then install /usr/bin selector wrappers (owned by
# mlnx-ofa_kernel-common) that exec the copy matching the running kernel.
install -d %{buildroot}%{_mofa_libexec}/bin
for _t in ibdev2netdev setup_mr_cache.sh mlnx_interface_mgr.sh mlnx_conf_mgr.sh; do
    if [ -e "%{buildroot}%{_bindir}/${_t}" ]; then
        mv "%{buildroot}%{_bindir}/${_t}" "%{buildroot}%{_mofa_libexec}/bin/${_t}"
    fi
done
# NOTE: %{_datadir}/mlnx_ofed (mod_load_funcs et al.) is sourced by the openibd
# init script from the FIXED path /usr/share/mlnx_ofed, so it is NOT namespaced;
# it stays there and is owned by the singleton mlnx-ofa_kernel-common package.

# Per-kernel mapping: running-kernel -> this build's userspace version dir.
# Owned by mlnx-ofa_kernel-modules (unique per %{KVERREL}); the selector reads
# it to find the right tools for `uname -r`.
install -d %{buildroot}%{_mofa_base}/by-kernel
ln -sfn "../%{_mofa_ns}" "%{buildroot}%{_mofa_base}/by-kernel/%{KVERREL}"

# Selector dispatcher (owned by mlnx-ofa_kernel-common; version-independent).
cat > %{buildroot}%{_mofa_base}/mlnx-ofa-select << 'EOFSEL'
#!/bin/bash
# Dispatch to the mlnx-ofa_kernel userspace tool matching the running kernel.
# Resolution: /usr/libexec/mlnx-ofa/by-kernel/<uname -r> -> <version> dir;
# fall back to the newest installed version if the running kernel has no map.
set -e
tool=${MLNX_OFA_TOOL:-$(basename "$0")}
base=%{_mofa_base}
map="$base/by-kernel/$(uname -r)"
if [ -e "$map" ]; then
    verdir=$(readlink -f "$map")
else
    newest=$(find "$base" -mindepth 1 -maxdepth 1 -type d ! -name by-kernel \
        -printf '%%f\n' 2>/dev/null | sort -V | tail -n1)
    [ -n "$newest" ] && verdir="$base/$newest"
fi
if [ -z "${verdir:-}" ] || [ ! -x "$verdir/bin/$tool" ]; then
    echo "mlnx-ofa: no userspace found for kernel $(uname -r) (tool: $tool)" >&2
    exit 1
fi
exec "$verdir/bin/$tool" "$@"
EOFSEL
chmod 0755 %{buildroot}%{_mofa_base}/mlnx-ofa-select

# /usr/bin selector wrappers (owned by -common) — symlinks to the dispatcher,
# which keys off the invoked basename.
install -d %{buildroot}%{_bindir}
for _t in ibdev2netdev setup_mr_cache.sh mlnx_interface_mgr.sh mlnx_conf_mgr.sh; do
    ln -sfn %{_mofa_base}/mlnx-ofa-select "%{buildroot}%{_bindir}/${_t}"
done

# Stage the devel tree (headers + compat + ofed_scripts + Module.symvers) for
# this exact kernel build.
_devel_stage="%{_builddir}/src/mlnx-ofa_kernel/default"
mkdir -p "${_devel_stage}"
cp -ar include/ "${_devel_stage}"
cp -ar config* "${_devel_stage}"
cp -ar compat* "${_devel_stage}"
find "${_devel_stage}" \( -name '*.o' -o -name '*.ko' \) -delete
rm -rf "${_devel_stage}/compat/modtest"
cp -ar ofed_scripts "${_devel_stage}"
_modsyms=$(find . -name Module.symvers -o -name Modules.symvers)
: > "${_devel_stage}/Module.symvers"
if [ -n "${_modsyms}" ]; then
    for _ms in ${_modsyms}; do cat "${_ms}" >> "${_devel_stage}/Module.symvers"; done
else
    ./ofed_scripts/create_Module.symvers.sh
    cp ./Module.symvers "${_devel_stage}/Module.symvers"
fi
cp -a "${_devel_stage}" %{buildroot}%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERREL}
popd
rm -rf "%{_builddir}/src"

# AZL: drop the modules.* that install_modules wrote, restore the kernel's
# originals from the snapshot. The kernel %post regenerates depmod state on the
# target at install time.
find "$_mods_dir" -maxdepth 1 -name 'modules.*' -type f -exec rm -f {} \;
if [ -d "$_mods_snap" ]; then
    cp -a "$_mods_snap"/. "$_mods_dir/"
    rm -rf "$_mods_snap"
fi

# Make installed modules executable so rpmbuild strips them + extracts debuginfo.
find %{buildroot}/lib/modules/%{KVERREL}/extra/mlnx-ofa_kernel \
    \( -type f -name '*.ko' -o -name '*.ko.gz' -o -name '*.ko.xz' -o -name '*.ko.zst' \) \
    -exec chmod u+x {} \;

# Strip .BTF sections to avoid runtime validation failures on target VMs
# ("Invalid name" / BTF: -22).
if command -v objcopy >/dev/null 2>&1; then
find %{buildroot}/lib/modules/%{KVERREL}/extra/mlnx-ofa_kernel \
    \( -name '*.ko' -o -name '*.ko.gz' -o -name '*.ko.xz' -o -name '*.ko.zst' \) | \
while read -r f; do
    case "$f" in
        *.ko)
            objcopy --remove-section .BTF --remove-section .BTF.ext "$f" || true
            ;;
        *.ko.gz)
            gzip -dkf "$f"; ko="${f%.gz}"
            objcopy --remove-section .BTF --remove-section .BTF.ext "$ko" || true
            gzip -f "$ko"
            ;;
        *.ko.xz)
            xz -dkf "$f"; ko="${f%.xz}"
            objcopy --remove-section .BTF --remove-section .BTF.ext "$ko" || true
            xz -zf "$ko"
            ;;
        *.ko.zst)
            zstd -q -d -f "$f" -o "${f%.zst}"; ko="${f%.zst}"
            objcopy --remove-section .BTF --remove-section .BTF.ext "$ko" || true
            zstd -q -f "$ko" -o "$f"; rm -f "$ko"
            ;;
    esac
done
fi

# Rewrite the buildroot-relative BACKPORT_INCLUDES path so downstream
# out-of-tree builds resolve it from the installed devel location.
if [ -f "%{buildroot}%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERREL}/configure.mk.kernel" ]; then
    sed -i -e "s|=-I.*backport_includes|=-I%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERREL}/backport_includes|" \
        "%{buildroot}%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERREL}/configure.mk.kernel" || true
fi

# ---- pristine source (mlnx-ofa_kernel-source) ----
mkdir -p %{buildroot}%{_prefix}/src/ofa_kernel-%{mlnx_ofa_version}
cp -a "${_srcroot}/source" %{buildroot}%{_prefix}/src/ofa_kernel-%{mlnx_ofa_version}/source
ln -s ofa_kernel-%{mlnx_ofa_version}/source \
    %{buildroot}%{_prefix}/src/mlnx-ofa_kernel-%{mlnx_ofa_version}

# ---- /etc/infiniband/info (upstream) ----
mkdir -p %{buildroot}/etc/infiniband
cat > %{buildroot}/etc/infiniband/info << EOFINFO
#!/bin/bash
echo prefix=%{_prefix}
echo Kernel=%{KVERREL}
echo
echo "Configure options: --with-core-mod --with-user_mad-mod --with-user_access-mod --with-addr_trans-mod --with-mlx5-mod --with-mlxfw-mod --with-ipoib-mod"
echo
EOFINFO
chmod 0755 %{buildroot}/etc/infiniband/info

# ---- systemd units + interface-manager helpers (upstream) ----
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}/etc/systemd/system
install -m 0644 "${_srcroot}/source/ofed_scripts/openibd.service" %{buildroot}%{_unitdir}
install -m 0644 "${_srcroot}/source/ofed_scripts/mlnx_interface_mgr@.service" %{buildroot}/etc/systemd/system
install -d %{buildroot}%{_bindir}
install -m 0755 "${_srcroot}/source/ofed_scripts/mlnx_conf_mgr.sh" %{buildroot}%{_bindir}/
install -m 0755 "${_srcroot}/source/ofed_scripts/mlnx_interface_mgr.sh" %{buildroot}%{_bindir}/

# ---- license ----
install -D -m 0644 "${_srcroot}/source/COPYING" \
    %{buildroot}%{_datadir}/licenses/mlnx-ofa_kernel/COPYING
# Namespaced license copy for the version-namespaced userspace package (unique
# path per version so install-only copies never collide).
install -D -m 0644 "${_srcroot}/source/COPYING" \
    %{buildroot}%{_mofa_libexec}/COPYING

# openibd.service is a thin systemd wrapper whose ExecStart is /etc/init.d/openibd
# (upstream's actual implementation: loads modules, brings interfaces up/down).
# It is invoked directly by systemd, NOT via SysV runlevel machinery, so keep
# it — deleting it breaks the service ("Failed at step EXEC spawning
# /etc/init.d/openibd"). Normalise it to the canonical init.d dir (%{_initrddir},
# reachable as /etc/init.d through the distro symlink) and mark it executable.
_ob=$(find %{buildroot} -path '*/init.d/openibd' -print -quit 2>/dev/null)
if [ -n "$_ob" ]; then
    install -d %{buildroot}%{_initrddir}
    [ "$_ob" != "%{buildroot}%{_initrddir}/openibd" ] && mv "$_ob" %{buildroot}%{_initrddir}/openibd
    chmod 0755 %{buildroot}%{_initrddir}/openibd
fi
%endif

%endif

# =========================================================================
# Phase: files — scriptlets and file lists
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
# ---- mlnx-ofa_kernel-modules scriptlets ----
%post -n mlnx-ofa_kernel-modules
%{_sbindir}/depmod -a %{KVERREL} || :

%postun -n mlnx-ofa_kernel-modules
%{_sbindir}/depmod -a %{KVERREL} || :

# ---- mlnx-ofa_kernel-devel scriptlets (upstream update-alternatives) ----
%post -n mlnx-ofa_kernel-devel
if [ -d "%{_prefix}/src/ofa_kernel/default" ] && [ ! -L "%{_prefix}/src/ofa_kernel/default" ] && [ $1 -gt 1 ]; then
	touch %{_prefix}/src/ofa_kernel/%{_arch}/%{KVERREL}.missing_link
else
	update-alternatives --install \
		%{_prefix}/src/ofa_kernel/default \
		ofa_kernel_headers \
		%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERREL} \
		20
fi

%posttrans -n mlnx-ofa_kernel-devel
symlink="%{_prefix}/src/ofa_kernel/default"
for flag_file in %{_prefix}/src/ofa_kernel/*/*.missing_link; do
	dir=${flag_file%.missing_link}
	if [ ! -d "$dir" ]; then
		rm -f "$flag_file"
		continue
	fi
	if [ -d "$symlink" ]; then
		rm -rf "$symlink"
	fi
	update-alternatives --install \
		"$symlink" \
		ofa_kernel_headers \
		"$dir" \
		20
	rm -f "$flag_file"
done

%postun -n mlnx-ofa_kernel-devel
update-alternatives --remove \
	ofa_kernel_headers \
	%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERREL} || :

# ---- mlnx-ofa_kernel-common scriptlets ----
%post -n mlnx-ofa_kernel-common
export SYSTEMCTL_SKIP_SYSV=1
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl enable openibd >/dev/null 2>&1 || true
    # Update limits.conf (but not for containers)
    if [ ! -e "/.dockerenv" ] && ! (grep -q docker /proc/self/cgroup 2>/dev/null); then
        if [ -e /etc/security/limits.conf ]; then
            if ! (grep -qE "soft.*memlock" /etc/security/limits.conf 2>/dev/null); then
                echo "* soft memlock unlimited" >> /etc/security/limits.conf
            fi
            if ! (grep -qE "hard.*memlock" /etc/security/limits.conf 2>/dev/null); then
                echo "* hard memlock unlimited" >> /etc/security/limits.conf
            fi
        fi
    fi
fi

%preun -n mlnx-ofa_kernel-common
export SYSTEMCTL_SKIP_SYSV=1
if [ $1 -eq 0 ]; then
    /usr/bin/systemctl disable openibd >/dev/null 2>&1 || true
fi

%postun -n mlnx-ofa_kernel-common
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :

# ---- file lists ----
%files -n mlnx-ofa_kernel
%dir %{_mofa_libexec}
%license %{_mofa_libexec}/COPYING
%{_mofa_libexec}/bin

%files -n mlnx-ofa_kernel-common
%license %{_datadir}/licenses/mlnx-ofa_kernel/COPYING
%dir %{_mofa_base}
%dir %{_mofa_base}/by-kernel
%{_mofa_base}/mlnx-ofa-select
%{_bindir}/ibdev2netdev
%{_bindir}/setup_mr_cache.sh
%{_bindir}/mlnx_interface_mgr.sh
%{_bindir}/mlnx_conf_mgr.sh
%dir /etc/infiniband
%{_unitdir}/openibd.service
%{_initrddir}/openibd
/etc/systemd/system/mlnx_interface_mgr@.service
/lib/udev/sf-rep-netdev-rename
/lib/udev/auxdev-sf-netdev-rename
/lib/udev/rules.d/83-mlnx-sf-name.rules
/lib/udev/rules.d/90-ib.rules
/etc/modprobe.d/mlnx.conf
/etc/modprobe.d/mlnx-bf.conf
/etc/modprobe.d/ib_ipoib.conf
/etc/infiniband/openib.conf
/etc/infiniband/mlx5.conf
/etc/infiniband/info
%{_datadir}/mlnx_ofed

%files -n mlnx-ofa_kernel-modules
%license %{_datadir}/licenses/mlnx-ofa_kernel/COPYING
/lib/modules/%{KVERREL}/extra/mlnx-ofa_kernel/
%{_mofa_base}/by-kernel/%{KVERREL}

%files -n mlnx-ofa_kernel-modules-matched
# empty sentinel package — no files

%files -n mlnx-ofa_kernel-devel
%license %{_datadir}/licenses/mlnx-ofa_kernel/COPYING
%dir %{_prefix}/src/ofa_kernel
%dir %{_prefix}/src/ofa_kernel/%{_arch}
%ghost %{_prefix}/src/ofa_kernel/default
%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERREL}

%files -n mlnx-ofa_kernel-source
%license %{_datadir}/licenses/mlnx-ofa_kernel/COPYING
%dir %{_prefix}/src/ofa_kernel-%{mlnx_ofa_version}
%{_prefix}/src/ofa_kernel-%{mlnx_ofa_version}/source
%{_prefix}/src/mlnx-ofa_kernel-%{mlnx_ofa_version}
%endif

%endif
