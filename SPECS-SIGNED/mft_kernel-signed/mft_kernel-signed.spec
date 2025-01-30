
%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_azurelinux_build_kernel_version %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_kernel_release %(/bin/rpm -q --queryformat '%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers) | /bin/cut -d . -f 1)

%global KVERSION %{target_kernel_version_full}

Name:            mft_kernel
Summary:         %{name} Kernel Module for the %{KVERSION} kernel
Version:         4.30.0
Release:         2%{?dist}
License:         Dual BSD/GPLv2
Group:           System Environment/Kernel

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:        %{name}-%{version}-%{release}.%{_arch}.rpm
Source1:        mst_pci.ko
Source2:        mst_pciconf.ko
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
ExclusiveArch:  x86_64

Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod

# Azure Linux attempts to match the spec file name and the "Name" tag.
# Upstream's mft_kernel spec set rpm name as kernel-mft. To comply, we
# set "Name" as mft_kernel but add a "Provides" for kernel-mft.
Provides:       kernel-mft = %{version}-%{release}

%description
mft kernel module(s)

%global debug_package %{nil}

%prep

%build


%install
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

cp -r %{SOURCE1} %{buildroot}/lib/modules/%{KVERSION}/updates/mst_pci.ko
cp -r %{SOURCE2} %{buildroot}/lib/modules/%{KVERSION}/updates/mst_pciconf.ko

%clean
rm -rf %{buildroot}

%post
/sbin/depmod %{KVERSION}

%postun
/sbin/depmod %{KVERSION}

%files
%defattr(-,root,root,-)
%license %{_defaultlicensedir}/%{name}/COPYING
/lib/modules/%{KVERSION}/updates/

%changelog
* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 4.30.0-2
- Bump release to match kernel

* Tue Dec  16 2024 Binu Jose Philip <bphilip@microsoft.com> - 4.30.0-1
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
