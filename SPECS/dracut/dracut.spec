%define dracutlibdir        %{_libdir}/%{name}
%global __requires_exclude  pkg-config

Summary:        dracut to create initramfs
Name:           dracut
Version:        059
Release:        17%{?dist}
# The entire source code is GPLv2+
# except install/* which is LGPLv2+
License:        GPLv2+ AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://github.com/dracutdevs/dracut/wiki

Source0:        https://github.com/dracutdevs/dracut/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://www.gnu.org/licenses/lgpl-2.1.txt
Source3:        megaraid.conf
Source4:        20overlayfs/module-setup.sh
Source5:        20overlayfs/overlayfs-mount.sh
Source6:        defaults.conf
Source7:        20overlayfs/overlayfs-parse.sh

Patch:          fix-functions-Avoid-calling-grep-with-PCRE-P.patch
# allow-liveos-overlay-no-user-confirmation-prompt.patch has been introduced by
# the Mariner team to allow skipping the user confirmation prompt during boot
# when the overlay of the liveos is backed by ram. This allows the machine to
# boot without being blocked on user input in such a scenario.
Patch:          allow-liveos-overlay-no-user-confirmation-prompt.patch

Patch:          0002-disable-xattr.patch
Patch:          0006-dracut.sh-validate-instmods-calls.patch
Patch:          0007-feat-dracut.sh-support-multiple-config-dirs.patch
Patch:          0008-fix-dracut-systemd-rootfs-generator-cannot-write-out.patch
Patch:          0009-install-systemd-executor.patch

BuildRequires:  bash
BuildRequires:  kmod-devel
BuildRequires:  pkg-config
BuildRequires:  asciidoc
BuildRequires:  systemd-rpm-macros

Requires:       bash >= 4
Requires:       kmod
Requires:       sed
Requires:       grep
Requires:       xz
Requires:       gzip
Requires:       cpio
Requires:       filesystem
Requires:       util-linux
Requires:       findutils
Requires:       procps-ng
Requires:       systemd
Requires:       systemd-udev
# Our toolkit cannot handle OR requirements
#Requires:       (coreutils or coreutils-selinux)
Requires:       coreutils

%description
dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.

%package fips
Summary:        dracut modules to build a dracut initramfs with an integrity check
Requires:       %{name} = %{version}-%{release}
Requires:       libkcapi-hmaccalc
Requires:       nss

%description fips
This package requires everything which is needed to build an
initramfs with dracut, which does an integrity check.

%package megaraid
Summary:        dracut configuration needed to build an initramfs with MegaRAID driver support
Requires:       %{name} = %{version}-%{release}

%description megaraid
This package contains dracut configuration needed to build an initramfs with MegaRAID driver support.

%package tools
Summary:        dracut tools to build the local initramfs
Requires:       %{name} = %{version}-%{release}

%description tools
This package contains tools to assemble the local initrd and host configuration.

%package overlayfs
Summary:        dracut module to build a dracut initramfs with OverlayFS support
Requires:       %{name} = %{version}-%{release}

%description overlayfs
This package contains dracut module needed to build an initramfs with OverlayFS support.

%prep
%autosetup -p1
cp %{SOURCE1} .

%build
%configure \
    --systemdsystemunitdir=%{_unitdir} \
    --bashcompletiondir=$(pkg-config --variable=completionsdir bash-completion) \
    --libdir=%{_libdir} \
    --disable-documentation

%make_build

%install
%make_install %{?_smp_mflags} libdir=%{_libdir}

echo "DRACUT_VERSION=%{version}-%{release}" > %{buildroot}%{dracutlibdir}/%{name}-version.sh


# we do not support dash in the initramfs
rm -fr -- %{buildroot}%{dracutlibdir}/modules.d/00dash

# remove gentoo specific modules
rm -fr -- %{buildroot}%{dracutlibdir}/modules.d/96securityfs \
          %{buildroot}%{dracutlibdir}/modules.d/97masterkey \
          %{buildroot}%{dracutlibdir}/modules.d/98integrity

mkdir -p %{buildroot}/boot/%{name} \
         %{buildroot}%{_sharedstatedir}/%{name}/overlay \
         %{buildroot}%{_var}/log \
         %{buildroot}%{_var}/opt/%{name}/log \
         %{buildroot}%{_sharedstatedir}/initramfs \
         %{buildroot}%{_sbindir}

install -m 0644 dracut.conf.d/fips.conf.example %{buildroot}%{_sysconfdir}/dracut.conf.d/40-fips.conf
> %{buildroot}%{_sysconfdir}/system-fips

install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/dracut.conf.d/50-megaraid.conf
install -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/dracut.conf.d/00-defaults.conf

mkdir -p %{buildroot}%{dracutlibdir}/modules.d/20overlayfs/
install -p -m 0755 %{SOURCE4} %{buildroot}%{dracutlibdir}/modules.d/20overlayfs/
install -p -m 0755 %{SOURCE5} %{buildroot}%{dracutlibdir}/modules.d/20overlayfs/
install -p -m 0755 %{SOURCE7} %{buildroot}%{dracutlibdir}/modules.d/20overlayfs/

touch %{buildroot}%{_var}/opt/%{name}/log/%{name}.log
ln -srv %{buildroot}%{_var}/opt/%{name}/log/%{name}.log %{buildroot}%{_var}/log/

# create compat symlink
ln -srv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_sbindir}/%{name}

%files
%defattr(-,root,root,0755)
%{_bindir}/%{name}
%{_bindir}/lsinitrd
# compat symlink
%{_sbindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/bash-completion/completions/lsinitrd
%dir %{dracutlibdir}
%dir %{dracutlibdir}/modules.d
%{dracutlibdir}/modules.d/*
%exclude %{_libdir}/kernel
%exclude %{dracutlibdir}/modules.d/20overlayfs
%{_libdir}/%{name}/%{name}-init.sh
%{_datadir}/pkgconfig/%{name}.pc
%{dracutlibdir}/%{name}-functions.sh
%{dracutlibdir}/%{name}-functions
%{dracutlibdir}/%{name}-version.sh
%{dracutlibdir}/%{name}-logger.sh
%{dracutlibdir}/%{name}-initramfs-restore
%{dracutlibdir}/%{name}-install
%{dracutlibdir}/skipcpio
%{dracutlibdir}/%{name}-util
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config %{_sysconfdir}/dracut.conf.d/00-defaults.conf
%dir %{_sysconfdir}/%{name}.conf.d
%dir %{dracutlibdir}/%{name}.conf.d
%dir %{_var}/opt/%{name}/log
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_var}/opt/%{name}/log/%{name}.log
%{_var}/log/%{name}.log
%dir %{_sharedstatedir}/initramfs
%{_unitdir}/%{name}-shutdown.service
%{_unitdir}/sysinit.target.wants/%{name}-shutdown.service
%{_unitdir}/%{name}-cmdline.service
%{_unitdir}/%{name}-initqueue.service
%{_unitdir}/%{name}-mount.service
%{_unitdir}/%{name}-pre-mount.service
%{_unitdir}/%{name}-pre-pivot.service
%{_unitdir}/%{name}-pre-trigger.service
%{_unitdir}/%{name}-pre-udev.service
%{_unitdir}/dracut-shutdown-onfailure.service
%{_unitdir}/initrd.target.wants/%{name}-cmdline.service
%{_unitdir}/initrd.target.wants/%{name}-initqueue.service
%{_unitdir}/initrd.target.wants/%{name}-mount.service
%{_unitdir}/initrd.target.wants/%{name}-pre-mount.service
%{_unitdir}/initrd.target.wants/%{name}-pre-pivot.service
%{_unitdir}/initrd.target.wants/%{name}-pre-trigger.service
%{_unitdir}/initrd.target.wants/%{name}-pre-udev.service

%files fips
%defattr(-,root,root,0755)
%{dracutlibdir}/modules.d/01fips
%{_sysconfdir}/dracut.conf.d/40-fips.conf
%config(missingok) %{_sysconfdir}/system-fips

%files megaraid
%defattr(-,root,root,0755)
%{_sysconfdir}/dracut.conf.d/50-megaraid.conf

%files tools
%defattr(-,root,root,0755)

%files overlayfs
%dir %{dracutlibdir}/modules.d/20overlayfs
%{dracutlibdir}/modules.d/20overlayfs/*

%{_bindir}/%{name}-catimages
%dir /boot/%{name}
%dir %{_sharedstatedir}/%{name}
%dir %{_sharedstatedir}/%{name}/overlay

%changelog
* Wed May 01 2024 Lanze Liu <lanzeliu@microsoft.com> - 059-17
- Add overlayfs-parse.sh in overlayfs sub-package

* Wed Mar 27 2024 Cameron Baird <cameronbaird@microsoft.com> - 059-16
- Remove x86-specific xen-acpi-processor driver from defaults

* Fri Mar 22 2024 Lanze Liu <lanzeliu@microsoft.com> - 059-15
- Exclude overlayfs module from main dracut package

* Wed Mar 06 2024 Chris Gunn <chrisgun@microsoft.com> - 059-14
- Move defaults to /etc/dracut.conf.d/00-defaults.conf file
- Add VM guest drivers to default config

* Fri Feb 23 2024 Chris Gunn <chrisgun@microsoft.com> - 059-13
- Remove mkinitrd script
- Set hostonly as default in /etc/dracut.conf

* Wed Feb 07 2024 Dan Streetman <ddstreet@ieee.org> - 059-12
- update to 059

* Wed Jan 03 2024 Susant Sahani <susant.sahani@broadcom.com> 059-11
- Include systemd-executor if available

* Tue Oct 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-10
- Add gzip, procps-ng, xz to requires

* Thu Jul 27 2023 Piyush Gupta <gpiyush@vmware.com> 059-9
- fix(dracut-systemd): rootfs-generator cannot write outside of generator dir

* Mon Jul 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-8
- Fix a bug in finding installed kernel versions during mkinitrd

* Tue Apr 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-7
- Code improvements in multiple conf dir support

* Sat Apr 1 2023 Laszlo Gombos <laszlo.gombos@gmail.com> 059-6
- Update wiki link and remove obsolete references

* Wed Mar 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-5
- Add systemd-udev to requires

* Wed Mar 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-4
- Add /etc/dracut.conf.d to conf dirs list during initrd creation
- Drop multiple conf file support

* Wed Mar 01 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-3
- Fix mkinitrd verbose & add a sanity check

* Wed Jan 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-2
- Fix requires
* Mon Jan 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 059-1
- Upgrade to v059

* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 057-1
- Upgrade to v057

* Mon Jan 29 2024 Lanze Liu <lanzeliu@microsoft.com> - 055-7
- Add overlayfs sub-package.

* Wed Jan 24 2024 George Mileka <gmileka@microsoft.com> - 055-6
- Add an option to supress user confirmation prompt for ram overlays.

* Thu Apr 27 2023 Daniel McIlvaney <damcilva@microsoft.com> - 055-5
- Avoid using JIT'd perl in grep since it is blocked by SELinux.

* Fri Mar 31 2023 Vince Perri <viperri@microsoft.com> - 055-4
- Add dracut-megaraid package.

* Tue Oct 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 055-3
- Fixing default log location.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 055-2
- Removing the explicit %%clean stage.

* Wed Dec 01 2021 Henry Beberman <henry.beberman@microsoft.com> - 055-1
- Update to version 055. Port mkinitrd forward for compatibility.

* Wed Sep 29 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 049-8
- Added missing BR on "systemd-rpm-macros".

* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 049-7
- Adding 'Provides' for 'dracut-caps'.

* Mon Apr 26 2021 Thomas Crain <thcrain@microsoft.com> - 049-6
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Fri Feb 12 2021 Nicolas Ontiveros <niontive@microsoft.com> - 049-5
- Enable kernel crypto testing in dracut-fips

* Wed Feb 10 2021 Nicolas Ontiveros <niontive@microsoft.com> - 049-4
- Move 40-fips.conf to /etc/dracut.conf.d/

* Mon Feb 01 2021 Nicolas Ontiveros <niontive@microsoft.com> - 049-3
- Add dracut-fips package.
- Disable kernel crypto testing in dracut-fips.

*   Wed Apr 08 2020 Nicolas Ontiveros <niontive@microsoft.com> 049-2
-   Remove toybox from requires.

*   Thu Mar 26 2020 Nicolas Ontiveros <niontive@microsoft.com> 049-1
-   Update version to 49. License verified. 

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 048-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Oct 01 2018 Alexey Makhalov <amakhalov@vmware.com> 048-1
-   Version update

*   Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  045-6
-   Fixed the log file directory structure

*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 045-5
-   Requires coreutils/util-linux/findutils or toybox,
    /bin/grep, /bin/sed

*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 045-4
-   Add kmod-devel to BuildRequires

*   Fri May 26 2017 Bo Gan <ganb@vmware.com> 045-3
-   Fix dependency

*   Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 045-2
-   Disable xattr for cp

*   Wed Apr 12 2017 Chang Lee <changlee@vmware.com> 045-1
-   Updated to 045

*   Wed Jan 25 2017 Harish Udaiya Kumar <hudaiyakumr@vmware.com> 044-6
-   Added the patch for bash 4.4 support.

*   Wed Nov 23 2016 Anish Swaminathan <anishs@vmware.com>  044-5
-   Add systemd initrd root device target to list of modules

*   Fri Oct 07 2016 ChangLee <changlee@vmware.com> 044-4
-   Modified %check

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 044-3
-   GA - Bump release of all rpms

*   Thu Apr 25 2016 Gengsheng Liu <gengshengl@vmware.com> 044-2
-   Fix incorrect systemd directory.

*   Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 044-1
-   Updating Version.
