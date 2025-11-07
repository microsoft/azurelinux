#define buildforkernels newest
#define buildforkernels current
#define buildforkernels akmod

Summary:	 XPMEM: Cross-partition memory
Name:		 xpmem-lib
Version:	 2.7
Release:	 2%{?dist}
License:	 GPLv2
Group:		 System Environment/Libraries
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
# DOCA OFED feature sources come from the following repo MLNX_OFED_SRC tgz
# https://linux.mellanox.com/public/repo/doca/3.1.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-25.07-0.9.7.0.tgz
Source0:         %{_distro_sources_url}/%{name}-%{version}.tar.gz

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: pkg-config

%{!?make_build: %global make_build %{__make} %{?_smp_mflags} %{?mflags} V=1}
%{!?run_ldconfig: %global run_ldconfig %{?ldconfig}}

%description
XPMEM is a Linux kernel module that enables a process to map the
memory of another process into its virtual address space. Source code
can be obtained by cloning the Git repository, original Mercurial
repository or by downloading a tarball from the link above.

%package -n libxpmem
Summary: XPMEM: user-space library

%description -n libxpmem
XPMEM is a Linux kernel module that enables a process to map the
memory of another process into its virtual address space. Source code
can be obtained by cloning the Git repository, original Mercurial
repository or by downloading a tarball from the link above.

This package contains the user-space library needed to interface with XPMEM.

%package -n libxpmem-devel
Summary: XPMEM: user-space library headers
Group: System Environment/Libraries
Requires: libxpmem%{?_isa} = %{version}-%{release}

%description -n libxpmem-devel
XPMEM is a Linux kernel module that enables a process to map the
memory of another process into its virtual address space. Source code
can be obtained by cloning the Git repository, original Mercurial
repository or by downloading a tarball from the link above.

This package contains the development headers for the user-space library
needed to interface with XPMEM.

%prep
%setup

%build
%configure --disable-kernel-module
%make_build

%install
%make_install
rm -rf ${RPM_BUILD_ROOT}/etc  # /etc/.version , udev rules

%post -n libxpmem
%if 0%{?fedora} || 0%{?rhel} > 7
# https://fedoraproject.org/wiki/Changes/Removing_ldconfig_scriptlets
%else
%{run_ldconfig}
%endif

%files -n libxpmem
%doc README AUTHORS
%license COPYING COPYING.LESSER
%{_libdir}/libxpmem.so.*

%files -n libxpmem-devel
%{_includedir}/xpmem.h
%{_libdir}/libxpmem.a
%{_libdir}/libxpmem.la
%{_libdir}/libxpmem.so
%{_libdir}/pkgconfig/cray-xpmem.pc

%changelog
* Tue Nov 04 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.7-2
- Build with MOFED 25.07-0.9.7.1.
- Update source path

* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com>
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
