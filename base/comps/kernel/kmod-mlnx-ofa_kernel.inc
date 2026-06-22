# kmod-mlnx-ofa_kernel.inc — NVIDIA / Mellanox OFED kernel modules (mlnx-ofa_kernel)
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.comp.toml overlays.
#
# Requires these defines/sources in kernel.spec (injected via comp.toml overlays):
#   mlnx_ofa_version  — driver tag (e.g. 26.04)
#   mlnx_ofa_release  — vendor release stamp (e.g. OFED.26.04.0.8.5.1)
#   SOURCE6100        — MLNX_OFED_SRC-%{mlnx_ofa_version}-%{mlnx_ofa_bundle_release}.tgz bundle
#

# =========================================================================
# Phase: package — subpackage declaration
# =========================================================================
%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
%package -n kmod-%{_kmod_name}-%{mlnx_ofa_version}
Summary:        Mellanox OFED kernel modules (mlnx-ofa_kernel %{mlnx_ofa_version})
AutoReq:        no
Provides:       mlnx-ofa-kmod-version = %{mlnx_ofa_version}
Provides:       mlnx-ofa-kmod-release = %{mlnx_ofa_release}
Provides:       kmod-%{_kmod_name} = %{version}-%{release}
Provides:       kmod-mlnx-ofa = %{version}-%{release}
Obsoletes:      kmod-mlnx-ofa < %{version}-%{release}
Provides:       installonlypkg(kernel-module)
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod

%description -n kmod-%{_kmod_name}-%{mlnx_ofa_version}
NVIDIA / Mellanox InfiniBand and Ethernet (mlx5) kernel modules built from
mlnx-ofa_kernel %{mlnx_ofa_version} (%{mlnx_ofa_release}) against kernel
%{KVERREL}.

# -------------------------------------------------------------------------
# -devel: headers + Module.symvers + helper scripts for building out-of-tree
# kernel modules (e.g. nv-peer-mem, GPUDirect) against this kmod. Lives in
# the kmod (not the userspace comp) because the symvers + backport-shim
# headers are produced by *this* build and are tied to this exact kernel.
# -------------------------------------------------------------------------
%package -n kmod-%{_kmod_name}-devel-%{mlnx_ofa_version}
Summary:        Development files for kmod-%{_kmod_name}-%{mlnx_ofa_version}
AutoReq:        no
Requires:       kmod-%{_kmod_name}-%{mlnx_ofa_version} = %{version}-%{release}
Requires:       coreutils
Requires:       pciutils
Provides:       mlnx-ofa-kmod-devel-version = %{mlnx_ofa_version}
Provides:       mlnx-ofa-kmod-devel-release = %{mlnx_ofa_release}
Provides:       kmod-%{_kmod_name}-devel = %{version}-%{release}

%description -n kmod-%{_kmod_name}-devel-%{mlnx_ofa_version}
Development files for kmod-%{_kmod_name}-%{mlnx_ofa_version}: backport
headers, compat layer, Module.symvers, and the ofed_scripts helpers used
by out-of-tree modules (e.g. nv-peer-mem) that link against the mlnx-ofa
NIC/RDMA stack rather than the in-tree mlx5/RDMA drivers.

Files install under /usr/src/ofa_kernel/%{_arch}/%{KVERREL}/ and are tied
to the kernel build that produced them. Multiple kernel versions can
coexist (one devel tree per kernel build).
%endif

%endif

# =========================================================================
# Phase: prep — extract mlnx-ofa_kernel tarball from MLNX_OFED_SRC bundle
# =========================================================================
%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
# %{SOURCE6100} is the MLNX_OFED_SRC bundle (a tar of every Mellanox OFED
# SRPM). We don't need the whole bundle — just the mlnx-ofa_kernel SRPM —
# and from that SRPM we only need the mlnx-ofa_kernel-<v>.tgz source tarball. 
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
popd
%endif

%endif

# =========================================================================
# Phase: build — compile mlnx-ofa kernel modules
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building mlnx-ofa_kernel %{mlnx_ofa_version} modules for %{KVERREL}"}
pushd %{_builddir}/mlnx-ofa_kernel-%{mlnx_ofa_version}

# Upstream mlnx-ofa_kernel.spec stamps compat shims to a fixed epoch to keep
# autoconf/automake-style timestamp checks happy in the kbuild Makefiles. Same
# trick here; safe no-op if `compat/` is absent.
find compat -type f -exec touch -t 200012201010 '{}' \; || true

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
    --kernel-sources "%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}" \
    --modules-dir "/lib/modules/%{KVERREL}/extra/mlnx-ofa_kernel" \
    --with-core-mod \
    --with-user_mad-mod \
    --with-user_access-mod \
    --with-addr_trans-mod \
    --with-mlx5-mod \
    --with-mlxfw-mod \
    --with-ipoib-mod \
    %{?_smp_mflags}

make %{?_smp_mflags} kernel

popd
%endif

%endif

# =========================================================================
# Phase: install — install modules
# =========================================================================
%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing mlnx-ofa_kernel modules for %{KVERREL}"}
pushd %{_builddir}/mlnx-ofa_kernel-%{mlnx_ofa_version}

# mlnx-ofa's `install_modules` recipe runs depmod, which overwrites the
# parent kernel's modules.{builtin,order,*}. Snapshot those before install
# and restore them after, otherwise kernel-core's %files (which lists
# /lib/modules/%{KVERREL}/modules.builtin*) will fail with "File not found".
_mods_dir="%{buildroot}/lib/modules/%{KVERREL}"
_mods_snap="%{_builddir}/mlnx-ofa-mods-snapshot"
rm -rf "$_mods_snap"
if [ -d "$_mods_dir" ]; then
    mkdir -p "$_mods_snap"
    find "$_mods_dir" -maxdepth 1 -name 'modules.*' -type f \
        -exec cp -a {} "$_mods_snap/" \;
fi

export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/mlnx-ofa_kernel
make install_modules KERNELRELEASE=%{KVERREL}

popd

# Drop the modules.{dep,order,builtin,...} files that mlnx-ofa's install just
# wrote, then restore the parent kernel's originals from the snapshot. The
# kernel %post regenerates depmod state at install time on the target system.
find "$_mods_dir" -maxdepth 1 -name 'modules.*' -type f -exec rm -f {} \;
if [ -d "$_mods_snap" ]; then
    cp -a "$_mods_snap"/. "$_mods_dir/"
    rm -rf "$_mods_snap"
fi

# Make installed modules executable so they get stripped + debuginfo extracted
# when the package is built (rpmbuild only strips u+x files).
find %{buildroot}/lib/modules/%{KVERREL}/extra/mlnx-ofa_kernel \
    \( -type f -name '*.ko' -o -name '*.ko.gz' -o -name '*.ko.xz' -o -name '*.ko.zst' \) \
    -exec chmod u+x {} \;

# Strip .BTF sections from installed modules to avoid runtime validation
# failures observed on target VMs ("Invalid name" / BTF: -22).
if command -v objcopy >/dev/null 2>&1; then
find %{buildroot}/lib/modules/%{KVERREL}/extra/mlnx-ofa_kernel \
    \( -name '*.ko' -o -name '*.ko.gz' -o -name '*.ko.xz' -o -name '*.ko.zst' \) | \
while read -r f; do
    case "$f" in
        *.ko)
            objcopy --remove-section .BTF --remove-section .BTF.ext "$f" || true
            ;;
        *.ko.gz)
            gzip -dkf "$f"
            ko="${f%.gz}"
            objcopy --remove-section .BTF --remove-section .BTF.ext "$ko" || true
            gzip -f "$ko"
            ;;
        *.ko.xz)
            xz -dkf "$f"
            ko="${f%.xz}"
            objcopy --remove-section .BTF --remove-section .BTF.ext "$ko" || true
            xz -zf "$ko"
            ;;
        *.ko.zst)
            zstd -q -d -f "$f" -o "${f%.zst}"
            ko="${f%.zst}"
            objcopy --remove-section .BTF --remove-section .BTF.ext "$ko" || true
            zstd -q -f "$ko" -o "$f"
            rm -f "$ko"
            ;;
    esac
done
fi

install -D -m 0644 %{_builddir}/mlnx-ofa_kernel-%{mlnx_ofa_version}/COPYING \
    %{buildroot}%{_datadir}/licenses/kmod-%{_kmod_name}-%{mlnx_ofa_version}/COPYING

%{log_msg "Staging mlnx-ofa_kernel devel tree for %{KVERREL}"}
_devel_src="%{_builddir}/mlnx-ofa_kernel-%{mlnx_ofa_version}"
_devel_dst="%{buildroot}%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERREL}"
mkdir -p "$_devel_dst"

# Headers + compat shims + helper scripts (sources only — no built objects).
for d in include compat ofed_scripts ; do
    if [ -e "$_devel_src/$d" ]; then
        cp -a "$_devel_src/$d" "$_devel_dst/"
    fi
done
# config.h / config.mk / configure.mk.kernel — produced by `./configure`.
for f in "$_devel_src"/config* "$_devel_src"/Makefile "$_devel_src"/makefile ; do
    [ -e "$f" ] && cp -a "$f" "$_devel_dst/"
done

# Concat every Module.symvers produced by `make kernel` (one per built
# module subdir) into a single symvers in the staged tree. Fallback to the
# upstream helper if no per-module symvers were emitted.
_modsyms=$(find "$_devel_src" -name 'Module.symvers' -o -name 'Modules.symvers' 2>/dev/null || true)
: > "$_devel_dst/Module.symvers"
if [ -n "$_modsyms" ]; then
    for ms in $_modsyms ; do
        cat "$ms" >> "$_devel_dst/Module.symvers"
    done
else
    ( cd "$_devel_src" && ./ofed_scripts/create_Module.symvers.sh )
    cp -a "$_devel_src/Module.symvers" "$_devel_dst/Module.symvers"
fi

# Drop anything that's not a source artifact (object files, kernel modules,
# upstream test stubs) — devel ships sources only.
find "$_devel_dst" \( -name '*.o' -o -name '*.ko' -o -name '*.ko.gz' \
                       -o -name '*.ko.xz' -o -name '*.ko.zst' \) -delete
rm -rf "$_devel_dst/compat/modtest"

# Rewrite the buildroot-relative BACKPORT_INCLUDES path in configure.mk.kernel
# so downstream out-of-tree builds resolve it from the installed location.
if [ -f "$_devel_dst/configure.mk.kernel" ]; then
    sed -i -e "s|=-I.*backport_includes|=-I%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERREL}/backport_includes|" \
        "$_devel_dst/configure.mk.kernel" || true
fi
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
%license %{_datadir}/licenses/kmod-%{_kmod_name}-%{mlnx_ofa_version}/COPYING
/lib/modules/%{KVERREL}/extra/mlnx-ofa_kernel/

%files -n kmod-%{_kmod_name}-devel-%{mlnx_ofa_version}
%license %{_datadir}/licenses/kmod-%{_kmod_name}-%{mlnx_ofa_version}/COPYING
%dir %{_prefix}/src/ofa_kernel
%dir %{_prefix}/src/ofa_kernel/%{_arch}
%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERREL}
%endif

%endif
