Summary:        Dracut module to enable dm-verity read-only roots
Name:           verity-read-only-root
Version:        1.0
Release:        2%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://dracut.wiki.kernel.org/
Source0:        verity.conf
Source1:        20verity-mount/module-setup.sh
Source2:        20verity-mount/verity-parse.sh
Source3:        20verity-mount/verity-mount.sh
Source4:        COPYING
Source5:        create_linear_debug_mount.sh
Requires:       device-mapper
Requires:       dracut
Requires:       grep
Requires:       initramfs
Requires:       kpartx
Requires:       veritysetup

%description
Dracut module capable of loading a dm-verity read-only root filesystem.
The module will mount a root FS read-only, and will place tmpfs overlays
on top of the read-only filesystem automatically. See verity-mount.sh for
details.

Reminder: Carefully consider the implications for GPLv3 licenced packages
when using a read-only root file system in conjunction with verified boot
flows.

%package debug-tools
Summary:        Adds tools to help debug read-only verity root issues
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description debug-tools
Creates a mount point at /mnt/verity_overlay_debug_tmpfs. If
rd.verityroot.overlays_debug_mount=/mnt/verity_overlay_debug_tmpfs is passed
to the kernel it will make the writable tmpfs overlays' upper and working
directories available here (read-only). Useful optimizing what directories
need writable tmpfs overlays.

Also creates a mount point at /mnt/verity_writable_debug, along with a script
/mnt/mount_verity_writable.sh which will suspend the verity device and mount
the underlying verity disk as a writable linear device.

%install
mkdir -p %{buildroot}%{_sysconfdir}/dracut.conf.d
install -D -m 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/dracut.conf.d/

mkdir -p %{buildroot}%{_libdir}/dracut/modules.d/20verity-mount/
install -p -m 0755 %{SOURCE1} %{buildroot}%{_libdir}/dracut/modules.d/20verity-mount/
install -p -m 0755  %{SOURCE2} %{buildroot}%{_libdir}/dracut/modules.d/20verity-mount/
install -p -m 0755  %{SOURCE3} %{buildroot}%{_libdir}/dracut/modules.d/20verity-mount/

cp %{SOURCE4} COPYING

mkdir -p %{buildroot}/mnt/verity_overlay_debug_tmpfs
mkdir -p %{buildroot}/mnt/verity_writable_debug
install -p -m 0755  %{SOURCE5} %{buildroot}/mnt/create_linear_mount.sh

%files
%{_sysconfdir}/dracut.conf.d/verity.conf
%dir %{_libdir}/dracut/modules.d/20verity-mount
%{_libdir}/dracut/modules.d/20verity-mount/*
%license COPYING

%files debug-tools
%dir /mnt/verity_overlay_debug_tmpfs
%dir /mnt/verity_writable_debug
/mnt/create_linear_mount.sh

%changelog
* Wed Oct 13 2021 Daniel McIlvaney <damcilva@microsoft.com> - 1.0-2
- Add required whitespace before and after module list in verity.conf
- License verified.

* Fri Dec 11 2020 Daniel McIlvaney <damcilva@microsoft.com> - 1.0-1
- Original version for CBL-Mariner.
