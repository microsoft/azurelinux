%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%global amd_ama_driver_version 1.3.0
%global amd_ama_driver_build_version 2503242033
# Get kernel version from kernel-devel since buildroot env may use another kernel than desired target kernel version
%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_azurelinux_build_kernel_version %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_kernel_release %(/bin/rpm -q --queryformat '%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers) | /bin/cut -d . -f 1)

autoreq: no

Name:           amd-ama-driver
Version:        %{amd_ama_driver_version}
Release:        1_%{target_azurelinux_build_kernel_version}.%{target_kernel_release}%{?dist}
Epoch:          1
Summary:        Drivers for AMD AMA MA35D video accelerator
Group:          System Environment/Kernel
License:        GPL
Url:            https://repo.radeon.com/
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
ExclusiveArch:  x86_64

Source0:        amd-ama-driver_%{amd_ama_driver_version}-%{amd_ama_driver_build_version}-amd64.rpm

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-devel = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  systemd
BuildRequires:  kmod

Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod

Provides:       amd-ama-driver = %{?epoch:%{epoch}:}%{version}

%description
Drivers for AMD AMA MA35D video accelerator card

%prep
mkdir amdama-build
rpm2cpio %{SOURCE0} | cpio -idmv -D amdama-build

%build
pushd amdama-build/opt/amd/ama/ma35/module
mkdir kmod
tar -xf kmod.tar.gz -C kmod/
cd kmod/dkms_source_tree
./build_driver.sh
popd

%install
# Setup buildroot paths for installer to use
mkdir -p %{buildroot}/usr/lib/firmware
mkdir -p %{buildroot}/lib/modules/$(uname -r)/kernel/drivers/misc
mkdir -p %{buildroot}/%{_sysconfdir}/udev/rules.d
mkdir -p %{buildroot}/opt/amd/ama/ma35/scripts

#install other required files from amdama-dkms package
install -Dp -m 0644 amdama-build/lib/firmware/ama_fw_inline_0.bin.bin %{buildroot}/usr/lib/firmware
install -Dp -m 0644 amdama-build/lib/firmware/ama_fw_inline_1.bin.bin %{buildroot}/usr/lib/firmware
install -Dp -m 0644 amdama-build/lib/firmware/ama_fw_lego0_0.bin.bin %{buildroot}/usr/lib/firmware
install -Dp -m 0644 amdama-build/lib/firmware/ama_fw_lego0_1.bin.bin %{buildroot}/usr/lib/firmware
install -Dp -m 0644 amdama-build/lib/firmware/ama_fw_lego1_0.bin.bin %{buildroot}/usr/lib/firmware
install -Dp -m 0644 amdama-build/lib/firmware/ama_fw_lego1_1.bin.bin %{buildroot}/usr/lib/firmware
install -Dp -m 0644 amdama-build/lib/firmware/ama_fw_system_0.bin.bin %{buildroot}/usr/lib/firmware
install -Dp -m 0644 amdama-build/lib/firmware/ama_fw_system_1.bin.bin %{buildroot}/usr/lib/firmware
install -Dp -m 0644 amdama-build/opt/amd/ama/ma35/module/kmod/dkms_source_tree/ama_transcoder.ko %{buildroot}/lib/modules/$(uname -r)/kernel/drivers/misc/ama_transcoder.ko
install -Dp -m 0755 amdama-build/opt/amd/ama/ma35/scripts/.on_transcoder_insert.sh %{buildroot}/opt/amd/ama/ma35/scripts/.on_transcoder_insert.sh
install -Dp -m 0644 amdama-build/etc/udev/rules.d/99-ama_transcoder-trigger.rules %{buildroot}/%{_sysconfdir}/udev/rules.d/99-ama_transcoder-trigger.rules

%post
if [ $1 -ge 1 ]; then # 1 : This package is being installed or reinstalled
  /sbin/depmod %{target_kernel_version_full}
  /sbin/modprobe ama_transcoder
fi # 1 : closed
# END of post

%postun
/sbin/modprobe -r ama_transcoder
/sbin/depmod %{target_kernel_version_full}

%files
%attr(0644, root, root) /usr/lib/firmware/ama_fw_inline_0.bin.bin
%attr(0644, root, root) /usr/lib/firmware/ama_fw_inline_1.bin.bin
%attr(0644, root, root) /usr/lib/firmware/ama_fw_lego0_0.bin.bin 
%attr(0644, root, root) /usr/lib/firmware/ama_fw_lego0_1.bin.bin 
%attr(0644, root, root) /usr/lib/firmware/ama_fw_lego1_0.bin.bin 
%attr(0644, root, root) /usr/lib/firmware/ama_fw_lego1_1.bin.bin 
%attr(0644, root, root) /usr/lib/firmware/ama_fw_system_0.bin.bin
%attr(0644, root, root) /usr/lib/firmware/ama_fw_system_1.bin.bin
%attr(0644, root, root) /lib/modules/$(uname -r)/kernel/drivers/misc/ama_transcoder.ko
%attr(0755, root, root) /opt/amd/ama/ma35/scripts/.on_transcoder_insert.sh
%attr(0644, root, root) /%{_sysconfdir}/udev/rules.d/99-ama_transcoder-trigger.rules

%changelog
* Thu Nov 13 2025 Mike Preston <mipres@microsoft.com> - 1.3.0.2503242033
- Initial version 1.3 release.
