%global _enable_debug_package 0
%global debug_package %{nil}
%global manticore_driver_version 3.2.0

# hard code versions due to ADO bug:58993948
%global target_azl_build_kernel_version 6.12.57.1
%global target_kernel_release 2
%global target_kernel_version_full %{target_azl_build_kernel_version}-%{target_kernel_release}%{?dist}
%global release_suffix _%{target_azl_build_kernel_version}.%{target_kernel_release}

Name:           manticore-hwe
Version:        %{manticore_driver_version}
Release:        1%{release_suffix}%{?dist}
Summary:        Manticore OOT kernel driver
License:        GPL-2.0
Vendor:         Microsoft Corporation
ExclusiveArch:  x86_64 

Source0:        manticore-3.2.0.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-hwe-devel = %{target_kernel_version_full}

Requires:       kernel-hwe = %{target_kernel_version_full}
Requires(post): kmod

%description
Manticore out-of-tree kernel driver

%prep
# Extract the tarball
mkdir manticore
tar -xzf %{SOURCE0} --strip-components=1 -C manticore

%build
# Build using your actual build process
cd manticore/src
export KERNEL_SRC=/lib/modules/%{target_kernel_version_full}/build
make

%install
# Create module directory
mkdir -p %{buildroot}/lib/modules/%{target_kernel_version_full}/extra

# Install kernel module
install -m 755 manticore/src/azihsm.ko %{buildroot}/lib/modules/%{target_kernel_version_full}/extra/

%post
/sbin/depmod %{target_kernel_version_full}
if [ "$(uname -r)" = "%{target_kernel_version_full}" ]; then
    /sbin/modprobe azihsm || :
fi

%preun
if [ $1 -eq 0 ] && [ "$(uname -r)" = "%{target_kernel_version_full}" ]; then
    /sbin/modprobe -r azihsm || :
fi

%postun
if [ $1 -eq 0 ]; then
    /sbin/depmod -a %{target_kernel_version_full}
fi

%files
%defattr(-,root,root,-)
/lib/modules/%{target_kernel_version_full}/extra/*.ko

%changelog
* Thu Feb 10 2026 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 3.2.0-1
- Original version for Azure Linux
- License verified
