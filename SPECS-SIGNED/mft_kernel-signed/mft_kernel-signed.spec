
%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_azurelinux_build_kernel_version %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_kernel_release %(/bin/rpm -q --queryformat '%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers) | /bin/cut -d . -f 1)

%global KVERSION %{target_kernel_version_full}
%global K_SRC /lib/modules/%{target_kernel_version_full}/build

# KMP is disabled by default
%{!?KMP: %global KMP 0}

# take cpu arch from uname -m
%global _cpu_arch %(uname -m)
%global docdir /etc/mft
%global mlxfwreset_ko_path %{docdir}/mlxfwreset/


# take kernel version or default to uname -r
# %{!?KVERSION: %global KVERSION %(uname -r)}
%{!?KVERSION: %global KVERSION %{target_kernel_version_full}}
%global kernel_version %{KVERSION}
%global krelver %(echo -n %{KVERSION} | sed -e 's/-/_/g')
# take path to kernel sources if provided, otherwise look in default location (for non KMP rpms).
%{!?K_SRC: %global K_SRC /lib/modules/%{KVERSION}/build}

%if "%{KMP}" == "1"
%global _name kernel-mft-mlnx
%else
%global _name kernel-mft
%endif

%{!?version: %global version 4.30.0}
%{!?_release: %global _release 1}
%global _kmp_rel %{_release}%{?_kmp_build_num}%{?_dist}

Name:		 %{_name}
Summary:	 %{name} Kernel Module for the %{KVERSION} kernel
Version:	 %{version}
Release:	 1%{?dist}
License:	 Dual BSD/GPL
Group:		 System Environment/Kernel
BuildRoot:	 /var/tmp/%{name}-%{version}-build

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
Source1:        mst_pci.ko
Source2:        mst_pciconf.ko
Vendor:		 Microsoft Corporation
Distribution:	 Azure Linux

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-devel = %{target_kernel_version_full}
BuildRequires:  kernel-headers = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  systemd
BuildRequires:  kmod

Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod

%description
mft kernel module(s)

%global debug_package %{nil}

%prep

%build
rpm2cpio %{Source0} | cpio -idmv -D %{buildroot}

%install
cp %{Source1} %{buildroot}/lib/modules/%{KVERSION}/updates/mst_pci.ko
cp %{Source2} %{buildroot}/lib/modules/%{KVERSION}/updates/mst_pciconf.ko

%clean
rm -rf %{buildroot}

%post
/sbin/depmod %{KVERSION}

%postun
/sbin/depmod %{KVERSION}

%if "%{KMP}" != "1"
%files
%defattr(-,root,root,-)
/lib/modules/%{KVERSION}/%{install_mod_dir}/
%endif

%changelog
* Tue Dec  16 2024 Binu Jose Philip <bphilip@microsoft.com> - 4.30.0
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
