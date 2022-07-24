%{!?KMP: %global KMP 0}

# take kernel version or default to uname -r
%global kver %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-devel))
%global ksrc %{_libdir}/modules/%{kver}/build
%global moddestdir %{buildroot}%{_libdir}/modules/%{kver}/kernel/
%global kernel_version %{kver}
%global krelver %(echo -n %{kver} | sed -e 's/-/_/g')

# A separate variable _release is required because of the odd way the
# script append_number_to_package_release.sh works:
%global _release 1.56068

%bcond_with kernel_only

%if %{with kernel_only}
%undefine _debugsource_packages
%global make_kernel_only SUBDIRS=kernel
%else
%global make_kernel_only %{nil}
%endif

Summary:        Cross-partition memory
Name:           xpmem
Version:        2.6.3
Release:        1%{?dist}
License:        GPLv2 and LGPLv2.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://linux.mellanox.com/public/repo/bluefield/3.9.0/extras/mlnx_ofed/5.6-1.0.3.3/SOURCES/xpmem-2.6.3.orig.tar.gz
Source:         %{name}-%{version}.tar.gz
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  kernel-devel
BuildRequires:  kmod
Requires:       kernel

# name gets a different value in subpackages
%global _name %{name}
%global _kmp_rel %{release}%{?dist}
# Required for e.g. SLES12:
%if %{undefined make_build}
%global make_build %{__make} %{?_smp_mflags}
%endif

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
%global kernel_source() %{ksrc}
%global kernel_release() %{kver}
%global flavors_to_build default

%package modules
# %{nil}: to avoid having the script that build OFED-internal
# munge the release version here as well:
Summary: XPMEM: kernel modules
Group: System Environment/Libraries
%description modules
XPMEM is a Linux kernel module that enables a process to map the
memory of another process into its virtual address space. Source code
can be obtained by cloning the Git repository, original Mercurial
repository or by downloading a tarball from the link above.

This package includes the kernel module (non KMP version).
%endif #end if "%{KMP}" == "1"

%global install_mod_dir extra/%{_name}
%global moduledir /lib/modules/%{kver}/%{install_mod_dir}

%prep
%autosetup -p1

%build
env=
if [ "$CROSS_COMPILE" != '' ]; then
  env="$env CC=${CROSS_COMPILE}gcc"
fi
./autogen.sh
%{configure} \
  --with-module-prefix= \
  --with-kerneldir=%{ksrc} \
  $env \
  #
%{make_build} %{make_kernel_only}

%install
%{make_install} moduledir=%{moduledir} %{make_kernel_only}
rm -rf %{buildroot}/etc/init.d/xpmem
mkdir -p %{buildroot}%{_prefix}/lib/modules-load.d
echo "xpmem" >%{buildroot}%{_prefix}/lib/modules-load.d/xpmem.conf
%if %{with kernel_only}
rm -f %{buildroot}/usr/lib*/pkgconfig/cray-xpmem.pc
%endif

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
%license COPYING COPYING.LESSER
/lib/udev/rules.d/*-xpmem.rules
%{_prefix}/lib/modules-load.d/xpmem.conf
%doc README AUTHORS

%if ! %{with kernel_only}
%files -n libxpmem
%{_libdir}/libxpmem.so.*

%files -n libxpmem-devel
%{_prefix}/include/xpmem.h
%{_libdir}/libxpmem.a
%{_libdir}/libxpmem.la
%{_libdir}/libxpmem.so
%{_libdir}/pkgconfig/cray-xpmem.pc
%endif

%if "%{KMP}" != "1"
%files modules
%{moduledir}/xpmem.ko
%endif

%changelog
* Thu Jul 14 2022 Rachel Menge <rachelmenge@microsoft.com> 1.0-1
- Initial CBL-Mariner import from NVIDIA (license: ASL 2.0).
- Lint spec to conform to Mariner 
- License verified