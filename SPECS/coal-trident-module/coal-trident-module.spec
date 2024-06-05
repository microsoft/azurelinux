Summary:        Dracut module to enable dm-verity read-only roots
Name:           coal-trident-module
Version:        1.0
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://dracut.wiki.kernel.org/
Source0:        trident-module.conf
Source1:        20trident/module-setup.sh
Requires:       device-mapper
Requires:       dracut
Requires:       grep
Requires:       initramfs
Requires:       kpartx
Requires:       trident
Requires:       trident-provisioning
Requires:       trident-service

%description
Dracut module capable of loading a dm-verity read-only root filesystem.
The module will mount a root FS read-only, and will place tmpfs overlays
on top of the read-only filesystem automatically. See verity-mount.sh for
details.

Reminder: Carefully consider the implications for GPLv3 licenced packages
when using a read-only root file system in conjunction with verified boot
flows.

%install
mkdir -p %{buildroot}%{_sysconfdir}/dracut.conf.d
install -D -m 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/dracut.conf.d/

mkdir -p %{buildroot}%{_libdir}/dracut/modules.d/20trident/
install -p -m 0755 %{SOURCE1} %{buildroot}%{_libdir}/dracut/modules.d/20trident/

%files
%{_sysconfdir}/dracut.conf.d/trident-module.conf
%dir %{_libdir}/dracut/modules.d/20trident
%{_libdir}/dracut/modules.d/20trident/*


%changelog
* Wed Jun 05 2024 Sean Dougherty <sdougherty@microsoft.com> - 1.0-1
- Original version for AzureLinux
