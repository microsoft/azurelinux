%{!?KMP: %global KMP 0}

%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_azurelinux_build_kernel_version %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_kernel_release %(/bin/rpm -q --queryformat '%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers) | /bin/cut -d . -f 1)

%global KVERSION %{target_kernel_version_full}

# xpmem-modules is a sub-package in SPECS/xpmem.
# We are making that into a main package for signing.

Summary:	 Cross-partition memory
Name:		 xpmem-modules
Version:	 2.7.4
Release:	 1%{?dist}
License:	 GPLv2 and LGPLv2.1
Group:		 System Environment/Libraries
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
BuildRequires:	 automake autoconf
URL:		 https://github.com/openucx/xpmem
ExclusiveArch:   x86_64

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:        %{name}-%{version}-%{release}.%{_arch}.rpm
Source1:        xpmem.ko

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
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

%install
cp -r %{SOURCE1} %{buildroot}/lib/modules/%{KVERSION}/updates/xpmem.ko

%clean
rm -rf %{buildroot}

%files modules
/lib/modules/%{KVERSION}/updates/xpmem.ko
%license COPYING COPYING.LESSER


%changelog
* Tue Dec  16 2024 Binu Jose Philip <bphilip@microsoft.com> - 2.7.4
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
