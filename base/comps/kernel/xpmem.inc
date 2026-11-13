# xpmem.inc - NVIDIA / Mellanox XPMEM userspace library and kernel module
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.spec.
#
# Requires these defines/sources in kernel.spec:
#   SOURCE6100 - MLNX_OFED_SRC-%{ofa_bundle_version}-%{ofa_vendor_release}.tgz bundle
#
# The XPMEM source RPM and inner source archive are extracted from that bundle.
# XPMEM builds directly against the kernel tree and does not depend on
# mlnx-ofa_kernel. Userspace (xpmem, libxpmem, libxpmem-devel) and the
# per-kernel xpmem-modules package are built together because they share one
# source tree.

# =========================================================================
# Phase: package - subpackage declarations
# =========================================================================
%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
%global xpmem_version 2604.0.2
%global xpmem_release 1
%global _azl_kver %{version}
%global _azl_krel %{release}

%package -n xpmem
Summary:        XPMEM userspace configuration and helper files
License:        GPL-2.0-only AND LGPL-2.1-only
Version:        %{xpmem_version}
Release:        %{xpmem_release}.%{_azl_kver}.%{_azl_krel}
Conflicts:      knem
Obsoletes:      knem

%description -n xpmem
XPMEM enables a process to map the memory of another process into its virtual
address space. This package contains its userspace configuration and helpers.

%package -n libxpmem
Summary:        XPMEM userspace library
License:        LGPL-2.1-only
Version:        %{xpmem_version}
Release:        %{xpmem_release}.%{_azl_kver}.%{_azl_krel}

%description -n libxpmem
Userspace library for the XPMEM cross-partition memory facility.

%package -n libxpmem-devel
Summary:        XPMEM userspace library development headers
License:        LGPL-2.1-only
Version:        %{xpmem_version}
Release:        %{xpmem_release}.%{_azl_kver}.%{_azl_krel}
Requires:       libxpmem%{?_isa} = %{xpmem_version}-%{xpmem_release}.%{_azl_kver}.%{_azl_krel}

%description -n libxpmem-devel
Headers and development files for the XPMEM userspace library.

%package -n xpmem-modules
Summary:        XPMEM kernel module
License:        GPL-2.0-only
Version:        %{xpmem_version}
Release:        %{xpmem_release}.%{_azl_kver}.%{_azl_krel}
%global version %{_azl_kver}
%global release %{_azl_krel}
AutoReq:        no
Provides:       kmod-xpmem = %{xpmem_version}-%{xpmem_release}
Obsoletes:      kmod-xpmem < %{xpmem_version}-%{xpmem_release}
Provides:       xpmem-modules = %{xpmem_version}-%{xpmem_release}
Obsoletes:      xpmem-modules < %{xpmem_version}-%{xpmem_release}
Conflicts:      knem-modules
Obsoletes:      knem-modules
Requires:       %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod

%description -n xpmem-modules
XPMEM kernel module built from xpmem %{xpmem_version} against kernel %{KVERREL}.

%endif

%endif

# =========================================================================
# Phase: prep - extract XPMEM from the MLNX_OFED source bundle
# =========================================================================
%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
pushd %{_builddir}
tar -xf %{SOURCE6100}
_xpmem_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/xpmem-*.src.rpm' -print -quit)
if [ -z "$_xpmem_srpm" ]; then
    echo "ERROR: XPMEM source RPM not found inside %{SOURCE6100}" >&2
    exit 1
fi
rpm2cpio "$_xpmem_srpm" | cpio -idm '*xpmem-%{xpmem_version}.tar.gz'
tar -xf xpmem-%{xpmem_version}.tar.gz
rm -rf MLNX_OFED_SRC-* xpmem-%{xpmem_version}.tar.gz
popd
%endif

%endif

# =========================================================================
# Phase: build - build libxpmem and the xpmem kernel module
# =========================================================================
%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building XPMEM %{xpmem_version} for %{KVERREL}"}
pushd %{_builddir}/xpmem-%{xpmem_version}
# As in the vendor spec, set the package version, which also becomes the
# module and pkg-config version (the tarball's configure.ac says 2.7.4).
sed -i "s/AC_INIT(\[xpmem\], \[.*\]/AC_INIT([xpmem], [%{xpmem_version}]/" configure.ac
./autogen.sh
# Run in a subshell so the exported build flags do not leak into the build
# phases of the kmods that follow in the shared %%build shell.
(
    export CFLAGS="${CFLAGS} -fPIE"
    %configure --with-module-prefix= --with-kerneldir=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
    %make_build
)
popd
%endif

%endif

# =========================================================================
# Phase: install - install XPMEM userspace and the kernel module
# =========================================================================
%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing XPMEM %{xpmem_version} for %{KVERREL}"}
pushd %{_builddir}/xpmem-%{xpmem_version}
%make_install moduledir=/lib/modules/%{KVERREL}/extra/xpmem
rm -f %{buildroot}%{_libdir}/libxpmem.la
rm -rf %{buildroot}%{_sysconfdir}/init.d/xpmem
rm -rf %{buildroot}%{_prefix}/src/xpmem-%{xpmem_version}
install -d %{buildroot}%{_prefix}/lib/modules-load.d
echo xpmem > %{buildroot}%{_prefix}/lib/modules-load.d/xpmem.conf
install -D -m 0644 README %{buildroot}%{_docdir}/xpmem/README
install -D -m 0644 AUTHORS %{buildroot}%{_docdir}/xpmem/AUTHORS
install -D -m 0644 COPYING %{buildroot}%{_docdir}/xpmem/COPYING
install -D -m 0644 COPYING.LESSER %{buildroot}%{_docdir}/xpmem/COPYING.LESSER
install -D -m 0644 COPYING \
    %{buildroot}%{_datadir}/licenses/xpmem-modules-%{KVERREL}/COPYING

_depmod_conf="%{buildroot}%{_sysconfdir}/depmod.d/zz02-xpmem-%{KVERREL}.conf"
install -d "$(dirname "$_depmod_conf")"
: > "$_depmod_conf"
find %{buildroot}/lib/modules/%{KVERREL}/extra/xpmem -type f -name '*.ko*' | sort | \
while read -r module; do
    ko_name=${module##*/}
    mod_name=${ko_name/.ko*/}
    echo "override ${mod_name} %{KVERREL} weak-updates/xpmem" >> "$_depmod_conf"
    echo "override ${mod_name} %{KVERREL} extra/xpmem" >> "$_depmod_conf"
done
popd
%endif

%endif

# =========================================================================
# Phase: files - scriptlets and file lists
# =========================================================================
%if "%{_kmod_phase}" == "files" && %{with_up_base}

%ifarch x86_64 aarch64
%post -n libxpmem -p /sbin/ldconfig
%postun -n libxpmem -p /sbin/ldconfig

%postun -n xpmem
if [ "$1" = 0 ] && lsmod | grep -qw xpmem; then
    rmmod xpmem || :
fi

%post -n xpmem-modules
%{_sbindir}/depmod -a %{KVERREL} || :
if [ ! -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL} ]; then
    mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
    touch %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
fi

%posttrans -n xpmem-modules
if [ -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL} ]; then
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || exit $?
fi

%postun -n xpmem-modules
%{_sbindir}/depmod -a %{KVERREL} || :
if [ -e /lib/modules/%{KVERREL}/vmlinuz ]; then
    echo "Running: dracut -f --kver %{KVERREL}"
    dracut -f --kver "%{KVERREL}" || :
fi

%files -n xpmem
/lib/udev/rules.d/56-xpmem.rules
%{_prefix}/lib/modules-load.d/xpmem.conf
%dir %{_docdir}/xpmem
%doc %{_docdir}/xpmem/README
%doc %{_docdir}/xpmem/AUTHORS
%license %{_docdir}/xpmem/COPYING
%license %{_docdir}/xpmem/COPYING.LESSER

%files -n libxpmem
%{_libdir}/libxpmem.so.*
%dir %{_docdir}/xpmem
%license %{_docdir}/xpmem/COPYING
%license %{_docdir}/xpmem/COPYING.LESSER

%files -n libxpmem-devel
%{_includedir}/xpmem.h
%{_libdir}/libxpmem.a
%{_libdir}/libxpmem.so
%{_libdir}/pkgconfig/cray-xpmem.pc

%files -n xpmem-modules
%dir %{_datadir}/licenses/xpmem-modules-%{KVERREL}
%license %{_datadir}/licenses/xpmem-modules-%{KVERREL}/COPYING
/lib/modules/%{KVERREL}/extra/xpmem/
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-xpmem-%{KVERREL}.conf

%endif

%endif
