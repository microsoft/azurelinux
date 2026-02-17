%global _enable_debug_package 0
%global debug_package %{nil}
%global manticore_driver_version 3.2.0
# The default __os_install_post macro ends up stripping the signatures off of the kernel module.
%define __os_install_post %{__os_install_post_leave_signatures} %{nil}

# hard code versions due to ADO bug:58993948
%global target_azl_build_kernel_version 6.12.57.1
%global target_kernel_release 2
%global target_kernel_version_full %{target_azl_build_kernel_version}-%{target_kernel_release}%{?dist}
%global release_suffix _%{target_azl_build_kernel_version}.%{target_kernel_release}

%{!?_name: %define _name manticore-hwe}

Summary:        %{_name} Driver
Name:		    %{_name}-signed 
Version:        %{manticore_driver_version}
Release:        1%{release_suffix}%{?dist}
License:        GPL-2.0
ExclusiveArch:  x86_64

# Unsigned RPM built from SPECS-MSFT/manticore
Source0:        %{_name}-%{version}-%{release}.%{_arch}.rpm
# Signed kernel module (provided by signing service)
Source1:        azihsm.ko

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-hwe-devel = %{target_kernel_version_full}

Requires:       kernel-hwe = %{target_kernel_version_full}
Requires(post): kmod

%description
Manticore out-of-tree kernel driver with signed kernel module for secure boot.

%package -n %{_name}
Summary:        %{summary}
Requires:       kernel-hwe = %{target_kernel_version_full}
Requires:       kmod

%description -n %{_name} 
Manticore out-of-tree kernel driver with signed kernel module for secure boot.

%prep
mkdir rpm_contents
rpm2cpio %{SOURCE0} | cpio -idmv -D rpm_contents

%build

%install
# Install files from the unsigned RPM, but exclude the unsigned kernel module
pushd rpm_contents
    rm -rf ./lib/modules/
    find . -name '*.ko' -delete
    cp -rp ./. %{buildroot}/
popd

# Install the signed kernel module
mkdir -p %{buildroot}/lib/modules/%{target_kernel_version_full}/extra
install -D -m 644 %{SOURCE1} %{buildroot}/lib/modules/%{target_kernel_version_full}/extra/azihsm.ko

%post -n %{_name}
/sbin/depmod %{target_kernel_version_full}
if [ "$(uname -r)" = "%{target_kernel_version_full}" ]; then
    /sbin/modprobe azihsm || :
fi

%preun -n %{_name}
if [ $1 -eq 0 ] && [ "$(uname -r)" = "%{target_kernel_version_full}" ]; then
    /sbin/modprobe -r azihsm || :
fi

%postun -n %{_name}
if [ $1 -eq 0 ]; then
    /sbin/depmod -a %{target_kernel_version_full}
fi

%files -n %{_name}
%defattr(-,root,root,-)
/lib/modules/*/extra/azihsm.ko

%changelog
* Thu Feb 10 2026 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 3.2.0-1
- Initial build

