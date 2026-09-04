# xpmem.inc - XPMEM userspace library and kernel module
#
# Phases: package, prep, build, install, files
# Activated by: setting _kmod_phase + _kmod_name globals and including this
# file from kernel.spec.
#
# Requires SOURCE6100, the MLNX OFED source bundle, from which the XPMEM
# source RPM and inner source archive are extracted.

%if "%{_kmod_phase}" == "package" && %{with_up_base}

%ifarch x86_64 aarch64
%global xpmem_version 2604.0.2
%global xpmem_release 1
%global _azl_kver %{version}
%global _azl_krel %{release}

%package -n xpmem
Summary: XPMEM userspace configuration and helper files
Version: %{xpmem_version}
Release: %{xpmem_release}.%{_azl_kver}.%{_azl_krel}
License: GPL-2.0-only AND LGPL-2.1-only
Conflicts: knem
Obsoletes: knem

%description -n xpmem
XPMEM enables a process to map the memory of another process into its virtual
address space. This package contains its userspace configuration and helpers.

%package -n libxpmem
Summary: XPMEM userspace library
Version: %{xpmem_version}
Release: %{xpmem_release}.%{_azl_kver}.%{_azl_krel}
License: LGPL-2.1-only

%description -n libxpmem
Userspace library for the XPMEM cross-partition memory facility.

%package -n libxpmem-devel
Summary: XPMEM userspace library development headers
Version: %{xpmem_version}
Release: %{xpmem_release}.%{_azl_kver}.%{_azl_krel}
License: LGPL-2.1-only
Requires: libxpmem%{?_isa} = %{xpmem_version}-%{xpmem_release}.%{_azl_kver}.%{_azl_krel}

%description -n libxpmem-devel
Headers and development files for the XPMEM userspace library.

%package -n xpmem-modules
Summary: XPMEM kernel module
Version: %{xpmem_version}
Release: %{xpmem_release}.%{_azl_kver}.%{_azl_krel}
%global version %{_azl_kver}
%global release %{_azl_krel}
License: GPL-2.0-only
AutoReq: no
Provides: kmod-xpmem = %{xpmem_version}-%{xpmem_release}
Obsoletes: kmod-xpmem < %{xpmem_version}-%{xpmem_release}
Provides: xpmem-modules = %{xpmem_version}-%{xpmem_release}
Obsoletes: xpmem-modules < %{xpmem_version}-%{xpmem_release}
Conflicts: knem-modules
Obsoletes: knem-modules
Requires: %{name}-core-uname-r = %{KVERREL}
Requires(post): kmod
Requires(postun): kmod

%description -n xpmem-modules
XPMEM kernel module built for kernel %{KVERREL}.

%endif

%endif

%if "%{_kmod_phase}" == "prep" && %{with_up_base}

%ifarch x86_64 aarch64
pushd %{_builddir}
tar -xf %{SOURCE6100}
_xpmem_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/xpmem-*.src.rpm' -print -quit)
if [ -z "$_xpmem_srpm" ]; then
    echo "ERROR: XPMEM source RPM not found inside %{SOURCE6100}" >&2
    exit 1
fi
rpm2cpio "$_xpmem_srpm" | cpio -idm './xpmem-%{xpmem_version}.tar.gz'
tar -xf xpmem-%{xpmem_version}.tar.gz
rm -rf MLNX_OFED_SRC-* xpmem-%{xpmem_version}.tar.gz
popd
%endif

%endif

%if "%{_kmod_phase}" == "build" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Building XPMEM %{xpmem_version} for %{KVERREL}"}
pushd %{_builddir}/xpmem-%{xpmem_version}
./autogen.sh
export CFLAGS="${CFLAGS} -fPIE"
%configure --with-module-prefix= --with-kerneldir=%{_builddir}/kernel-%{tarfile_release}/linux-%{KVERREL}
%make_build
popd
%endif

%endif

%if "%{_kmod_phase}" == "install" && %{with_up_base}

%ifarch x86_64 aarch64
%{log_msg "Installing XPMEM %{xpmem_version} for %{KVERREL}"}
pushd %{_builddir}/xpmem-%{xpmem_version}
%make_install moduledir=/lib/modules/%{KVERREL}/extra/xpmem
rm -f %{buildroot}%{_libdir}/libxpmem.la
rm -rf %{buildroot}%{_sysconfdir}/init.d/xpmem
rm -rf %{buildroot}%{_prefix}/src/xpmem-%{xpmem_version}
install -D -m 0644 README %{buildroot}%{_docdir}/xpmem/README
install -D -m 0644 AUTHORS %{buildroot}%{_docdir}/xpmem/AUTHORS
install -D -m 0644 COPYING %{buildroot}%{_docdir}/xpmem/COPYING
install -D -m 0644 COPYING.LESSER %{buildroot}%{_docdir}/xpmem/COPYING.LESSER
install -D -m 0644 /dev/stdin %{buildroot}%{_prefix}/lib/modules-load.d/xpmem.conf <<'EOF'
xpmem
EOF
popd
%endif

%endif

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

%postun -n xpmem-modules
%{_sbindir}/depmod -a %{KVERREL} || :

%files -n xpmem
/lib/udev/rules.d/56-xpmem.rules
%{_prefix}/lib/modules-load.d/xpmem.conf
%doc %{_docdir}/xpmem/README
%doc %{_docdir}/xpmem/AUTHORS
%license %{_docdir}/xpmem/COPYING
%license %{_docdir}/xpmem/COPYING.LESSER

%files -n libxpmem
%{_libdir}/libxpmem.so.*

%files -n libxpmem-devel
%{_includedir}/xpmem.h
%{_libdir}/libxpmem.a
%{_libdir}/libxpmem.so
%{_libdir}/pkgconfig/cray-xpmem.pc

%files -n xpmem-modules
/lib/modules/%{KVERREL}/extra/xpmem/xpmem.ko.%{compext}

%endif

%endif
