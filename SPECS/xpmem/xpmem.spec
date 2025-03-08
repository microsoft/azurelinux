%{!?KMP: %global KMP 0}

%global last-known-kernel 6.6.64.2

%if 0%{azl}
%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{VERSION}-%{RELEASE}' kernel-headers)
%else
%global target_kernel_version_full f.a.k.e
%endif

%global KVERSION %{target_kernel_version_full}
%global K_SRC /lib/modules/%{target_kernel_version_full}/build

# %{!?KVERSION: %global KVERSION %(uname -r)}
%{!?KVERSION: %global KVERSION %{target_kernel_version_full}}
%global kernel_version %{KVERSION}
%global krelver %(echo -n %{KVERSION} | sed -e 's/-/_/g')
%{!?K_SRC: %global K_SRC /lib/modules/%{KVERSION}/build}
# A separate variable _release is required because of the odd way the
# script append_number_to_package_release.sh works:
%global _release 1.2410068

%bcond_with kernel_only

%if %{with kernel_only}
%undefine _debugsource_packages
%global debug_package %{nil}
%global make_kernel_only SUBDIRS=kernel
%else
%global make_kernel_only %{nil}
%endif

%define need_firmware_dir 0%{?euleros} > 0

%if "%_vendor" == "openEuler"
%global __find_requires %{nil}
%endif

Summary:	 Cross-partition memory
Name:		 xpmem
Version:	 2.7.4
Release:	 6%{?dist}
License:	 GPLv2 and LGPLv2.1
Group:		 System Environment/Libraries
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
BuildRequires:	 automake autoconf
URL:		 https://github.com/openucx/xpmem
Source0:         https://linux.mellanox.com/public/repo/mlnx_ofed/24.10-0.7.0.0/SRPMS/xpmem-2.7.4.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:   x86_64

# name gets a different value in subpackages
%global _name %{name}
%global _kmp_rel %{release}%{?_kmp_build_num}%{?_dist}
# Required for e.g. SLES12:
%if %{undefined make_build}
%global make_build %{__make} %{?_smp_mflags}
%endif

# Ugly workaround until anolis kmod package stops requiring
# 'kernel(' dependencies its kernel package does not provide.
# This uses the __find_provides from /usr/lib/rpm/redhat/macros
# rather than the one from /usr/lib/rpm/macros.d/macros.kmp
%if 0%{?anolis} > 0
%{?filter_setup}
%endif

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-devel = %{target_kernel_version_full}
BuildRequires:  kernel-headers = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  systemd
BuildRequires:  kmod
BuildRequires:  mlnx-ofa_kernel-devel
BuildRequires:  mlnx-ofa_kernel-source

Requires:       mlnx-ofa_kernel
Requires:       mlnx-ofa_kernel-modules
Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod


%description
XPMEM is a Linux kernel module that enables a process to map the
memory of another process into its virtual address space. Source code
can be obtained by cloning the Git repository, original Mercurial
repository or by downloading a tarball from the link above.

This package includes helper tools for the kernel module.

%if ! %{with kernel_only}
%package -n libxpmem
Summary: XPMEM: Userspace library
%description -n libxpmem
XPMEM is a Linux kernel module that enables a process to map the
memory of another process into its virtual address space. Source code
can be obtained by cloning the Git repository, original Mercurial
repository or by downloading a tarball from the link above.


%package -n libxpmem-devel
Summary: XPMEM: userspace library development headers
%description -n libxpmem-devel
XPMEM is a Linux kernel module that enables a process to map the
memory of another process into its virtual address space. Source code
can be obtained by cloning the Git repository, original Mercurial
repository or by downloading a tarball from the link above.

This package includes development headers.
%endif

# build KMP rpms?
%if "%{KMP}" == "1"
%global kernel_release() $(make -C %{1} M=$PWD kernelrelease | grep -v make)
BuildRequires: %kernel_module_package_buildreqs
%(cat > %{_builddir}/preamble << EOF
EOF)
%{kernel_module_package -r %{_kmp_rel} -p %{_builddir}/preamble}
%else # not KMP
%global kernel_source() %{K_SRC}
%global kernel_release() %{KVERSION}
%global flavors_to_build default

%package modules
# %{nil}: to avoid having the script that build OFED-internal
# munge the release version here as well:
Release: 6%{?dist}
Summary: XPMEM: kernel modules
Group: System Environment/Libraries
%description modules
XPMEM is a Linux kernel module that enables a process to map the
memory of another process into its virtual address space. Source code
can be obtained by cloning the Git repository, original Mercurial
repository or by downloading a tarball from the link above.

This package includes the kernel module (non KMP version).
%endif #end if "%{KMP}" == "1"

#
# setup module sign scripts if paths to the keys are given
#
%global WITH_MOD_SIGN %(if ( test -f "$MODULE_SIGN_PRIV_KEY" && test -f "$MODULE_SIGN_PUB_KEY" ); \
	then \
		echo -n '1'; \
	else \
		echo -n '0'; fi)

%if "%{WITH_MOD_SIGN}" == "1"
# call module sign script
%global __modsign_install_post \
    $RPM_BUILD_DIR/xpmem-%{version}/tools/sign-modules $RPM_BUILD_ROOT/lib/modules/ %{kernel_source default} || exit 1 \
%{nil}

# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
#
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  %{__modsign_install_post} \
%{nil}

%endif # end of setup module sign scripts
#

%if 0%{?rhel} > 0 || 0%{?euleros} >= 2
%global install_mod_dir extra/%{_name}
%endif

%{!?install_mod_dir: %global install_mod_dir updates}

%global moduledir /lib/modules/%{KVERSION}/%{install_mod_dir}

%prep
%setup -q

%build
env=
if [ "$CROSS_COMPILE" != '' ]; then
  env="$env CC=${CROSS_COMPILE}gcc"
fi
./autogen.sh
%{configure} \
  --with-module-prefix= \
  --with-kerneldir=%{K_SRC} \
  $env \
  #
%{make_build} %{make_kernel_only}

%install
%{make_install} moduledir=%{moduledir} %{make_kernel_only}
rm -rf $RPM_BUILD_ROOT/%{_libdir}/libxpmem.la
rm -rf $RPM_BUILD_ROOT/etc/init.d/xpmem
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/modules-load.d
echo "xpmem" >$RPM_BUILD_ROOT%{_prefix}/lib/modules-load.d/xpmem.conf
%if %{with kernel_only}
rm -f $RPM_BUILD_ROOT/usr/lib*/pkgconfig/cray-xpmem.pc
%endif
%if %{need_firmware_dir}
mkdir -p $RPM_BUILD_ROOT/lib/firmware
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if ! %{with kernel_only}
%post   -n libxpmem -p /sbin/ldconfig
%postun -n libxpmem -p /sbin/ldconfig
%endif

%postun
if [ "$1" = 0 ]; then
	if lsmod | grep -qw xpmem; then
		# If the module fails to unload, give an error,
		# but don't fail uninstall. User should handle this
		# Maybe the module is in use
		rmmod xpmem || :
	fi
fi

%files
/lib/udev/rules.d/*-xpmem.rules
%{_prefix}/lib/modules-load.d/xpmem.conf
%doc README AUTHORS
%license COPYING COPYING.LESSER

%if ! %{with kernel_only}
%files -n libxpmem
%{_libdir}/libxpmem.so.*
%license COPYING COPYING.LESSER

%files -n libxpmem-devel
%{_prefix}/include/xpmem.h
%{_libdir}/libxpmem.a
%{_libdir}/libxpmem.so
%{_libdir}/pkgconfig/cray-xpmem.pc
%license COPYING COPYING.LESSER
%endif

%if "%{KMP}" != "1"
%files modules
%{moduledir}/xpmem.ko
%license COPYING COPYING.LESSER
%endif

%changelog
* Wed Feb 05 2025 Tobias Brick <tobiasb@microsoft.com> - 2.7.4-6
- Bump release to rebuild for new kernel release

* Tue Feb 04 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 2.7.4-5
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 2.7.4-4
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 2.7.4-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 2.7.4-2
- Bump release to match kernel

* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 2.7.4-1
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
