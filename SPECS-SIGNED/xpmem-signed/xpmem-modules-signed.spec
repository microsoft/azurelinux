%{!?KMP: %global KMP 0}

%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_azurelinux_build_kernel_version %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_kernel_release %(/bin/rpm -q --queryformat '%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers) | /bin/cut -d . -f 1)

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

# xpmem-modules is a sub-package in SPECS/xpmem.
# We are making that into a main package for signing.

Summary:	 Cross-partition memory
Name:		 xpmem-modules
Version:	 2.7.4
Release:	 1%{?dist}
License:	 GPLv2 and LGPLv2.1
Group:		 System Environment/Libraries
Vendor:		 Microsoft Corporation
Distribution:	 Azure Linux
BuildRequires:	 automake autoconf
URL:		 https://github.com/openucx/xpmem

# This package's "version" and "release" must reflect the unsigned version that
# was signed.
# An important consequence is that when making a change to this package, the
# unsigned version/release must be increased to keep the two versions consistent.
# Ideally though, this spec will not change much or at all, so the version will
# just track the unsigned package's version/release.
#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:        %{name}-%{version}-%{release}.%{_arch}.rpm
Source1:        xpmem.ko

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

This package includes the kernel module.

%prep

%build
rpm2cpio %{Source0} | cpio -idmv -D %{buildroot}

%install
cp %{Source1} %{buildroot}/lib/modules/%{KVERSION}/updates/xpmem.ko

%clean
rm -rf %{buildroot}

%if "%{KMP}" != "1"
%files modules
/lib/modules/%{KVERSION}/%{install_mod_dir}/xpmem.ko
%endif

%changelog
* Tue Dec  16 2024 Binu Jose Philip <bphilip@microsoft.com> - 2.7.4
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
