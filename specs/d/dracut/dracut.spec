# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define dracutlibdir %{_prefix}/lib/dracut
%bcond_without doc

# We ship a .pc file but don't want to have a dep on pkg-config. We
# strip the automatically generated dep here and instead co-own the
# directory.
%global __requires_exclude pkg-config

Name: dracut
Version: 107
Release: 9%{?dist}

Summary: Initramfs generator using udev

# The entire source code is GPLv2+
# except install/* which is LGPLv2+
# except util/* which is GPLv2
License: GPL-2.0-or-later AND LGPL-2.1-or-later AND GPL-2.0-only

URL: https://github.com/dracut-ng/dracut-ng/wiki/

Source0: https://github.com/dracut-ng/dracut-ng/archive/refs/tags/%{version}.tar.gz

Source1: https://www.gnu.org/licenses/lgpl-2.1.txt
# feat(hwdb): add hwdb module to install hwdb.bin on demand
# Author: Pavel Valena <pvalena@redhat.com>
Patch1:  0001-feat-hwdb-add-hwdb-module-to-install-hwdb.bin-on-dem.patch
# revert: "fix(install.d): correctly install pre-genned image and die if no args"
# Author: Pavel Valena <pvalena@redhat.com>
Patch2:  0002-revert-fix-install.d-correctly-install-pre-genned-im.patch
# feat(kernel-install): do nothing when $KERNEL_INSTALL_INITRD_GENERATOR says so
# Author: Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl>
Patch3:  0003-feat-kernel-install-do-nothing-when-KERNEL_INSTALL_I.patch
# fix(kernel-install): do not generate an initrd when one was specified
# Author: Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl>
Patch4:  0004-fix-kernel-install-do-not-generate-an-initrd-when-on.patch
# revert: "fix(rescue): make rescue always no-hostonly"
# Author: Pavel Valena <pvalena@redhat.com>
Patch5:  0005-revert-fix-rescue-make-rescue-always-no-hostonly.patch
# fix(dracut-install): initize fts pointer
# Author: Pavel Valena <pvalena@redhat.com>
Patch6:  0006-fix-dracut-install-initize-fts-pointer.patch
# feat: add openssl module
# Author: Pavel Valena <pvalena@redhat.com>
Patch7:  0007-feat-add-openssl-module.patch
# fix(ossl): ignore compiler warnings
# Author: Pavel Valena <pvalena@redhat.com>
Patch8:  0008-fix-ossl-ignore-compiler-warnings.patch
# Revert "feat(fips): include openssl's fips.so and openssl.cnf"
# Author: Pavel Valena <pvalena@redhat.com>
Patch9:  0009-Revert-feat-fips-include-openssl-s-fips.so-and-opens.patch
# Revert "chore: remove unused function"
# Author: Adam Williamson <awilliam@redhat.com>
Patch10: 0010-Revert-chore-remove-unused-function.patch
# Revert "feat(systemd-sysusers): run systemd-sysusers as part
# Author: Adam Williamson <awilliam@redhat.com>
Patch11: 0011-Revert-feat-systemd-sysusers-run-systemd-sysusers-as.patch
# Revert "feat(hwdb): add hwdb module to install hwdb.bin on demand"
# Author: Pavel Valena <pvalena@redhat.com>
Patch12: 0012-Revert-feat-hwdb-add-hwdb-module-to-install-hwdb.bin.patch
# fix(systemd-udevd): handle root=gpt-auto for systemd-v258
# Author: Antonio Alvarez Feijoo <antonio.feijoo@suse.com>
Patch13: 0013-fix-systemd-udevd-handle-root-gpt-auto-for-systemd-v.patch
# fix: partial revert for hostonly sloppy mode
# Author: Jo Zzsi <jozzsicsataban@gmail.com>
# hand-rediffed on 107
Patch14: 0011-fix-partial-revert-for-hostonly-sloppy-mode.patch

# Please use source-git to work with this spec file:
# HowTo: https://packit.dev/source-git/work-with-source-git
# Source-git repository: https://github.com/redhat-plumbers/dracut-fedora/

BuildRequires: bash
BuildRequires: git-core
BuildRequires: pkgconfig(libkmod) >= 23
BuildRequires: gcc

BuildRequires: pkgconfig
BuildRequires: systemd
BuildRequires: bash-completion
BuildRequires: cargo
BuildRequires: openssl-devel

%if %{with doc}
BuildRequires: docbook-style-xsl docbook-dtds libxslt
BuildRequires: asciidoc
%endif

Obsoletes: dracut-fips <= 047
Provides:  dracut-fips = %{version}-%{release}
Obsoletes: dracut-fips-aesni <= 047
Provides:  dracut-fips-aesni = %{version}-%{release}

Provides: bundled(crate(crosvm)) = 0.1.0

Requires: bash >= 4
Requires: coreutils
Requires: cpio
Requires: filesystem >= 2.1.0
Requires: findutils
Requires: grep
Requires: kmod
Requires: sed
# Used as default initramfs compression algorithm
Requires: zstd
# Used to handle kernel modules which are xz compressed
Requires: xz
# Not sure what this is needed for
# Requires: gzip

Recommends: memstrack
Recommends: hardlink
# Probably not needed anymore if we move zstd
# Recommends: pigz
Recommends: kpartx
Recommends: (tpm2-tools if tpm2-tss)
Requires: util-linux >= 2.21
Requires: systemd >= 219
Requires: systemd-udev >= 219
Requires: procps-ng

Requires: libkcapi-hmaccalc

%description
dracut contains tools to create bootable initramfses for the Linux
kernel. Unlike other implementations, dracut hard-codes as little
as possible into the initramfs. dracut contains various modules which
are driven by the event-based udev. Having root on MD, DM, LVM2, LUKS
is supported as well as NFS, iSCSI, NBD, FCoE with the dracut-network
package.

%package network
Summary: dracut modules to build a dracut initramfs with network support
Requires: %{name} = %{version}-%{release}
Requires: iputils
Requires: iproute
Requires: jq
Requires: NetworkManager >= 1.20
Suggests: NetworkManager
Obsoletes: dracut-generic < 008
Provides:  dracut-generic = %{version}-%{release}

%description network
This package requires everything which is needed to build a generic
all purpose initramfs with network support with dracut.

%package caps
Summary: dracut modules to build a dracut initramfs which drops capabilities
Requires: %{name} = %{version}-%{release}
Requires: libcap

%description caps
This package requires everything which is needed to build an
initramfs with dracut, which drops capabilities.

%package live
Summary: dracut modules to build a dracut initramfs with live image capabilities
Requires: %{name} = %{version}-%{release}
Requires: %{name}-network = %{version}-%{release}
Requires: tar coreutils bash device-mapper curl parted
%if ! 0%{?rhel}
Requires: fuse ntfs-3g
%endif

%description live
This package requires everything which is needed to build an
initramfs with dracut, with live image capabilities, like Live CDs.

%package config-generic
Summary: dracut configuration to turn off hostonly image generation
Requires: %{name} = %{version}-%{release}
Obsoletes: dracut-nohostonly < 030
Provides:  dracut-nohostonly = %{version}-%{release}

%description config-generic
This package provides the configuration to turn off the host specific initramfs
generation with dracut and generates a generic image by default.

%package config-rescue
Summary: dracut configuration to turn on rescue image generation
Requires: %{name} = %{version}-%{release}
Obsoletes: dracut < 030

%description config-rescue
This package provides the configuration to turn on the rescue initramfs
generation with dracut.

%package tools
Summary: dracut tools to build the local initramfs
Requires: %{name} = %{version}-%{release}

%description tools
This package contains tools to assemble the local initrd and host configuration.

%package squash
Summary: dracut module to build an initramfs with most files in a squashfs image
Requires: %{name} = %{version}-%{release}
Requires: squashfs-tools

%description squash
This package provides a dracut module to build an initramfs, but store most files
in a squashfs image, result in a smaller initramfs size and reduce runtime memory
usage.

%prep
%autosetup -n %{name}-ng-%{version} -S git_am
cp %{SOURCE1} .

%build
%configure  --systemdsystemunitdir=%{_unitdir} \
            --bashcompletiondir=$(pkg-config --variable=completionsdir bash-completion) \
            --libdir=%{_prefix}/lib \
            --enable-dracut-cpio \
%if %{without doc}
            --disable-documentation \
%endif
            ${NULL}

%make_build

%install
%make_install %{?_smp_mflags} \
     libdir=%{_prefix}/lib

echo "DRACUT_VERSION=%{version}-%{release}" > $RPM_BUILD_ROOT/%{dracutlibdir}/dracut-version.sh

# we do not support dash in the initramfs
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/00dash

# we do not support mksh in the initramfs
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/00mksh

# Remove obsolete module
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/35network-legacy

%ifnarch s390 s390x
# remove architecture specific modules
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/80cms
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/81cio_ignore
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/91zipl
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95dasd
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95dasd_mod
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95dcssblk
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95zfcp
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95znet
%else
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/00warpclock
%endif

# we don't want example configs
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/dracut.conf.d

# we don't ship tests
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/test
rm -fr -- $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/80test*

mkdir -p $RPM_BUILD_ROOT/boot/dracut
mkdir -p $RPM_BUILD_ROOT/var/lib/dracut/overlay
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log
touch $RPM_BUILD_ROOT%{_localstatedir}/log/dracut.log
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/initramfs
mkdir -p $RPM_BUILD_ROOT%{dracutlibdir}/dracut.conf.d

install -m 0644 dracut.conf.d/fedora.conf.example $RPM_BUILD_ROOT%{dracutlibdir}/dracut.conf.d/01-dist.conf
rm -f $RPM_BUILD_ROOT%{_mandir}/man?/*suse*

echo 'hostonly="no"' > $RPM_BUILD_ROOT%{dracutlibdir}/dracut.conf.d/02-generic-image.conf
echo 'dracut_rescue_image="yes"' > $RPM_BUILD_ROOT%{dracutlibdir}/dracut.conf.d/02-rescue.conf

%files
%if %{with doc}
%doc README.md AUTHORS NEWS.md
%endif
%license COPYING lgpl-2.1.txt
%{_bindir}/dracut
%{_datadir}/bash-completion/completions/dracut
%{_datadir}/bash-completion/completions/lsinitrd
%{_bindir}/lsinitrd
%dir %{dracutlibdir}
%dir %{dracutlibdir}/modules.d
%{dracutlibdir}/dracut-functions.sh
%{dracutlibdir}/dracut-init.sh
%{dracutlibdir}/dracut-functions
%{dracutlibdir}/dracut-version.sh
%{dracutlibdir}/dracut-logger.sh
%{dracutlibdir}/dracut-initramfs-restore
%{dracutlibdir}/dracut-install
%{dracutlibdir}/dracut-util
%{dracutlibdir}/ossl-config
%{dracutlibdir}/ossl-files
%{dracutlibdir}/skipcpio
%{dracutlibdir}/dracut-cpio
%config(noreplace) %{_sysconfdir}/dracut.conf
%{dracutlibdir}/dracut.conf.d/01-dist.conf
%dir %{_sysconfdir}/dracut.conf.d
%dir %{dracutlibdir}/dracut.conf.d
%dir %{_datadir}/pkgconfig
%{_datadir}/pkgconfig/dracut.pc

%if %{with doc}
%{_mandir}/man8/dracut.8*
%{_mandir}/man8/*service.8*
%{_mandir}/man1/lsinitrd.1*
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man7/dracut.cmdline.7*
%{_mandir}/man7/dracut.modules.7*
%{_mandir}/man7/dracut.bootup.7*
%{_mandir}/man5/dracut.conf.5*
%endif

%{dracutlibdir}/modules.d/00bash
%{dracutlibdir}/modules.d/00systemd
%{dracutlibdir}/modules.d/00systemd-network-management
%ifnarch s390 s390x
%{dracutlibdir}/modules.d/00warpclock
%endif
%{dracutlibdir}/modules.d/01fips
%{dracutlibdir}/modules.d/01fips-crypto-policies
%{dracutlibdir}/modules.d/01systemd-ac-power
%{dracutlibdir}/modules.d/01systemd-ask-password
%{dracutlibdir}/modules.d/01systemd-bsod
%{dracutlibdir}/modules.d/01systemd-battery-check
%{dracutlibdir}/modules.d/01systemd-coredump
%{dracutlibdir}/modules.d/01systemd-creds
%{dracutlibdir}/modules.d/01systemd-cryptsetup
%{dracutlibdir}/modules.d/01systemd-hostnamed
%{dracutlibdir}/modules.d/01systemd-initrd
%{dracutlibdir}/modules.d/01systemd-integritysetup
%{dracutlibdir}/modules.d/01systemd-journald
%{dracutlibdir}/modules.d/01systemd-ldconfig
%{dracutlibdir}/modules.d/01systemd-modules-load
%{dracutlibdir}/modules.d/01systemd-pcrphase
%{dracutlibdir}/modules.d/01systemd-portabled
%{dracutlibdir}/modules.d/01systemd-pstore
%{dracutlibdir}/modules.d/01systemd-repart
%{dracutlibdir}/modules.d/01systemd-resolved
%{dracutlibdir}/modules.d/01systemd-sysext
%{dracutlibdir}/modules.d/01systemd-sysctl
%{dracutlibdir}/modules.d/01systemd-sysusers
%{dracutlibdir}/modules.d/01systemd-timedated
%{dracutlibdir}/modules.d/01systemd-timesyncd
%{dracutlibdir}/modules.d/01systemd-tmpfiles
%{dracutlibdir}/modules.d/01systemd-udevd
%{dracutlibdir}/modules.d/01systemd-veritysetup
%{dracutlibdir}/modules.d/03modsign
%{dracutlibdir}/modules.d/03rescue
%{dracutlibdir}/modules.d/04watchdog
%{dracutlibdir}/modules.d/04watchdog-modules
%{dracutlibdir}/modules.d/06dbus-broker
%{dracutlibdir}/modules.d/06dbus-daemon
%{dracutlibdir}/modules.d/06rngd
%{dracutlibdir}/modules.d/09dbus
%{dracutlibdir}/modules.d/10i18n
%{dracutlibdir}/modules.d/30convertfs
%{dracutlibdir}/modules.d/45drm
%{dracutlibdir}/modules.d/45simpledrm
%{dracutlibdir}/modules.d/45net-lib
%{dracutlibdir}/modules.d/45plymouth
%{dracutlibdir}/modules.d/45url-lib
%{dracutlibdir}/modules.d/62bluetooth
%{dracutlibdir}/modules.d/80lvmmerge
%{dracutlibdir}/modules.d/80lvmthinpool-monitor
%{dracutlibdir}/modules.d/90btrfs
%{dracutlibdir}/modules.d/90crypt
%{dracutlibdir}/modules.d/90dm
%{dracutlibdir}/modules.d/90dmraid
%{dracutlibdir}/modules.d/90kernel-modules
%{dracutlibdir}/modules.d/90kernel-modules-extra
%{dracutlibdir}/modules.d/90lvm
%{dracutlibdir}/modules.d/90mdraid
%{dracutlibdir}/modules.d/90multipath
%{dracutlibdir}/modules.d/90nvdimm
%{dracutlibdir}/modules.d/90numlock
%{dracutlibdir}/modules.d/90overlayfs
%{dracutlibdir}/modules.d/90ppcmac
%{dracutlibdir}/modules.d/90pcmcia
%{dracutlibdir}/modules.d/90qemu
%{dracutlibdir}/modules.d/91crypt-gpg
%{dracutlibdir}/modules.d/91crypt-loop
%{dracutlibdir}/modules.d/91fido2
%{dracutlibdir}/modules.d/91pcsc
%{dracutlibdir}/modules.d/91pkcs11
%{dracutlibdir}/modules.d/91tpm2-tss
%{dracutlibdir}/modules.d/95debug
%{dracutlibdir}/modules.d/95fstab-sys
%{dracutlibdir}/modules.d/95hwdb
%{dracutlibdir}/modules.d/95lunmask
%{dracutlibdir}/modules.d/95resume
%{dracutlibdir}/modules.d/95rootfs-block
%{dracutlibdir}/modules.d/95terminfo
%{dracutlibdir}/modules.d/95udev-rules
%{dracutlibdir}/modules.d/95virtfs
%{dracutlibdir}/modules.d/95virtiofs
%ifarch s390 s390x
%{dracutlibdir}/modules.d/80cms
%{dracutlibdir}/modules.d/81cio_ignore
%{dracutlibdir}/modules.d/91zipl
%{dracutlibdir}/modules.d/95dasd
%{dracutlibdir}/modules.d/95dasd_mod
%{dracutlibdir}/modules.d/95dcssblk
%{dracutlibdir}/modules.d/95zfcp
%endif
%{dracutlibdir}/modules.d/96securityfs
%{dracutlibdir}/modules.d/97masterkey
%{dracutlibdir}/modules.d/98integrity
%{dracutlibdir}/modules.d/97biosdevname
%{dracutlibdir}/modules.d/97systemd-emergency
%{dracutlibdir}/modules.d/98dracut-systemd
%{dracutlibdir}/modules.d/98ecryptfs
%{dracutlibdir}/modules.d/98pollcdrom
%{dracutlibdir}/modules.d/98selinux
%{dracutlibdir}/modules.d/98syslog
%{dracutlibdir}/modules.d/98usrmount
%{dracutlibdir}/modules.d/99base
%{dracutlibdir}/modules.d/99busybox
%{dracutlibdir}/modules.d/99memstrack
%{dracutlibdir}/modules.d/99fs-lib
%{dracutlibdir}/modules.d/99openssl
%{dracutlibdir}/modules.d/99shutdown
%{dracutlibdir}/modules.d/99shell-interpreter
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_localstatedir}/log/dracut.log
%dir %{_sharedstatedir}/initramfs
%if %{defined _unitdir}
%{_unitdir}/dracut-shutdown.service
%{_unitdir}/dracut-shutdown-onfailure.service
%{_unitdir}/sysinit.target.wants/dracut-shutdown.service
%{_unitdir}/dracut-cmdline.service
%{_unitdir}/dracut-initqueue.service
%{_unitdir}/dracut-mount.service
%{_unitdir}/dracut-pre-mount.service
%{_unitdir}/dracut-pre-pivot.service
%{_unitdir}/dracut-pre-trigger.service
%{_unitdir}/dracut-pre-udev.service
%{_unitdir}/initrd.target.wants/dracut-cmdline.service
%{_unitdir}/initrd.target.wants/dracut-initqueue.service
%{_unitdir}/initrd.target.wants/dracut-mount.service
%{_unitdir}/initrd.target.wants/dracut-pre-mount.service
%{_unitdir}/initrd.target.wants/dracut-pre-pivot.service
%{_unitdir}/initrd.target.wants/dracut-pre-trigger.service
%{_unitdir}/initrd.target.wants/dracut-pre-udev.service
%endif
%{_prefix}/lib/kernel/install.d/50-dracut.install

%files network
%{dracutlibdir}/modules.d/01systemd-networkd
%{dracutlibdir}/modules.d/35connman
%{dracutlibdir}/modules.d/35network-manager
%{dracutlibdir}/modules.d/40network
%{dracutlibdir}/modules.d/90kernel-network-modules
%{dracutlibdir}/modules.d/90qemu-net
%{dracutlibdir}/modules.d/95cifs
%{dracutlibdir}/modules.d/95fcoe
%{dracutlibdir}/modules.d/95fcoe-uefi
%{dracutlibdir}/modules.d/95iscsi
%{dracutlibdir}/modules.d/95nbd
%{dracutlibdir}/modules.d/95nfs
%{dracutlibdir}/modules.d/95nvmf
%{dracutlibdir}/modules.d/95ssh-client
%ifarch s390 s390x
%{dracutlibdir}/modules.d/95znet
%endif
%{dracutlibdir}/modules.d/99uefi-lib

%files caps
%{dracutlibdir}/modules.d/02caps

%files live
%{dracutlibdir}/modules.d/99img-lib
%{dracutlibdir}/modules.d/90dmsquash-live
%{dracutlibdir}/modules.d/90dmsquash-live-autooverlay
%{dracutlibdir}/modules.d/90dmsquash-live-ntfs
%{dracutlibdir}/modules.d/90livenet

%files tools
%if %{with doc}
%doc %{_mandir}/man8/dracut-catimages.8*
%endif

%{_bindir}/dracut-catimages
%dir /boot/dracut
%dir /var/lib/dracut
%dir /var/lib/dracut/overlay

%files squash
%{dracutlibdir}/modules.d/99squash
%{dracutlibdir}/modules.d/95squash-erofs
%{dracutlibdir}/modules.d/95squash-squashfs
%{dracutlibdir}/modules.d/99squash-lib

%files config-generic
%{dracutlibdir}/dracut.conf.d/02-generic-image.conf

%files config-rescue
%{dracutlibdir}/dracut.conf.d/02-rescue.conf
%{_prefix}/lib/kernel/install.d/51-dracut-rescue.install

%changelog
* Tue Oct 14 2025 Adam Williamson <awilliam@redhat.com> - 107-8
- fix: partial revert for hostonly sloppy mode

* Wed Sep 24 2025 Pavel Valena <pvalena@redhat.com> - 107-7
- fix(systemd-udevd): handle root=gpt-auto for systemd-v258

* Mon Aug 25 2025 Pavel Valena <pvalena@redhat.com> - 107-6
- Add require on zstd to use it for initrd compression

* Thu Jul 24 2025 Pavel Valena <pvalena@redhat.com> - 107-5
- Revert "feat(hwdb): add hwdb module to install hwdb.bin on demand"

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 107-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Adam Williamson <awilliam@redhat.com> - 107-3
- Revert an upstream change to fix kernel build (#2379116)

* Thu Jul 10 2025 Adam Williamson <awilliam@redhat.com> - 107-2
- Backport fix to bring back inst_library for anaconda (dracut-ng PR #1436)

* Wed Jul 02 2025 Pavel Valena <pvalena@redhat.com> - 107-1
- build: upgrade to dracut 107

* Wed Apr 02 2025 Pavel Valena <pvalena@redhat.com> - 105-3
- fix(multipath): skip default multipath.conf with mpathconf

* Tue Mar 18 2025 Pavel Valena <pvalena@redhat.com> - 105-2
- feat: add openssl module

* Wed Jan 29 2025 Pavel Valena <pvalena@redhat.com> - 105-1
- build: upgrade to dracut 105

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 103-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 31 2024 Manuel Fombuena <fombuena@outlook.com> - 103-2
- fix(pcsc): add libpcsclite_real.so.*

* Mon Sep 16 2024 Pavel Valena <pvalena@redhat.com> - 103-1
- Update to dracut 103.
- build: enable dracut-cpio binary
- feat(fips-crypto-policies): make c-p follow FIPS mode automatically
- fix(fips-crypto-policies): make it depend on fips dracut module
- build: package fips-crypto-policies module

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 102-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 13 2024 Pavel Valena <pvalena@redhat.com> - 102-2
- Fixes for rhbz#2276271, rhbz#2295215

* Fri Jun 28 2024 Pavel Valena <pvalena@redhat.com> - 102-1
- Update to dracut 102.

* Thu May 16 2024 Pavel Valena <pvalena@redhat.com> - 101-1
- Update to dracut 101.

* Fri Apr 26 2024 Adam Williamson <awilliam@redhat.com> - 060-2
- Backport fix to pull in required libs for systemd (dracut-ng PR #118)
- Backport fix to move hook directory for systemd (dracut-ng PR #194)

* Wed Mar 20 2024 Pavel Valena <pvalena@redhat.com> - 060-1
- Update to dracut 060.

* Mon Feb 12 2024 Pavel Valena <pvalena@redhat.com> - 059-22
- Remove network-legacy module.

* Sat Jan 27 2024 Manuel Fombuena <fombuena@outlook.com> - 059-21
- fix(pkcs11): delete trailing dot on libcryptsetup-token-systemd-pkcs11.so
- fix(pcsc): add opensc load module file
- fix(pcsc): add --disable-polkit to pcscd.service

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 059-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 059-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 08 2023 Dennis Gilmore <dennis@ausil.us> - 059-18
- Add Qualcomm IPC router to enable USB(Lenovo x13s)

* Thu Nov 16 2023 Pavel Valena <pvalena@redhat.com> - 059-17
- fix(dracut.sh): remove microcode check based on

* Wed Nov  8 2023 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 059-16
- Backport patches to fix compatibility with systemd 255

* Sat Oct 28 2023 Adam Williamson <awilliam@redhat.com> - 059-15
- Backport PR #2545 to fix media check failure visibility

* Thu Oct 05 2023 Adam Williamson <awilliam@redhat.com> - 059-14
- Backport PR #2196 to fix boot with iso-scan feature

* Wed Sep 20 2023 Pavel Valena <pvalena@redhat.com> - 059-13
- fix(dracut.spec): add jq dependency to network subpackage

* Wed Aug 02 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 059-12
- Include modules for IMA

* Mon Jul 24 2023 Lukáš Nykrýn <lnykryn@redhat.com> - 059-11
- fix(dracut.sh): use dynamically uefi's sections offset

* Mon Jul 24 2023 Pavel Valena <pvalena@redhat.com> - 059-10
- feat(nvmf): support for NVMeoF

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 059-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 08 2023 Brian Masney <bmasney@redhat.com> - 059-8
- Backport fix to add the interconnect drivers

* Thu Apr 27 2023 Lukáš Zaoral <lzaoral@redhat.com> - 059-7
- migrate to SPDX license format

* Thu Apr 27 2023 Michael Hofmann <mhofmann@redhat.com> - 059-6
- Backport fix to remove dependency on multipathd.socket

* Tue Mar 14 2023 Dusty Mabe <dusty@dustymabe.com> - 059-5
- feat(network): include 98-default-mac-none.link if it exists

* Thu Mar 09 2023 Pavel Valena <pvalena@redhat.com> - 059-4
- fix(dmsquash-live): restore compatibility with earlier releases
- Re-add overlayfs module (drop patch 1934)
- revert(network-manager): avoid restarting NetworkManager

* Fri Feb 24 2023 Pavel Valena <pvalena@redhat.com> - 059-3
- fix(dracut.sh): handle --kmoddir with trailing /

* Tue Feb 21 2023 Pavel Valena <pvalena@redhat.com> - 059-2
- Revert: PR#1934 add overlayfs module

* Mon Feb 13 2023 Pavel Valena <pvalena@redhat.com> - 059-1
- Update to 059
- feat(dracut.sh): option to skip creating initrd
- feat(kernel-modules): driver support for macbook keyboards

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 057-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Nov 13 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 057-5
- Backport fix to add sysctl to initramfs to handle modprobe files

* Sat Oct 15 2022 Neal Gompa <ngompa@datto.com> - 057-4
- Backport dmsquash-live-autooverlay module

* Thu Aug 25 2022 Pavel Valena <pvalena@redhat.com> - 057-3
- Re-add patch Never-enable-the-bluetooth-module-by-default-1521
- Recommend tpm2-tools package, as it's required by crypt module

* Tue Aug 16 2022 Pavel Valena <pvalena@redhat.com> - 057-2
- dmsquash-live-root: Run checkisomd5 on correct device

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 057-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Pavel Valena <pvalena@redhat.com> - 057-1
- Update to 057

* Tue Apr 19 2022 Kevin Fenzi <kevin@scrye.com> - 056-2
- Add already upstream patch to change dracut-initramfs-restore to hopefully not break oz/composes

* Thu Mar 03 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 056-1
- Update to 056

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 055-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Hans de Goede <hdegoede@redhat.com> - 055-8
- Backport upstream changes for drm-privacy screen support in kernel >= 5.17

* Thu Nov  4 2021 Jeremy Linton <jeremy.linton@arm.com> - 055-7
- Backport Upstream: 15398458 fix(90kernel-modules): add isp1760 USB controller

* Tue Oct 26 2021 Olivier Lemasle <o.lemasle@gmail.com> - 055-6
- Backport PR #1611 to fix network manager when console is not usable

* Mon Oct 18 2021 Adam Williamson <awilliam@redhat.com> - 055-5
- Backport PR #1584 to fix missing block drivers, boot in EC2 (#2010058)

* Wed Oct 06 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 055-4
- Add USB Type-C to fix display/input/storage attached via it (rhbz #1964218)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 055-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Dusty Mabe <dusty@dustymabe.com> - 055-3
- Fixes for NM running via systemd+dbus in the initramfs
- Drop requirement on deprecated systemd-udev-settle

* Thu Jun 10 2021 Adam Williamson <awilliam@redhat.com> - 055-2
- Never include bluetooth module by default (rhbz 1964879) (workaround)

* Thu May 27 2021 Harald Hoyer <harald@redhat.com> - 055-1
- version 055
- install the missing fsck utils

* Fri May 21 2021 Harald Hoyer <harald@redhat.com> - 054-12.git20210521
- fix `get_maj_min` for kdump
- suppress hardlink output
- sane default --kerneldir for dracut-install
- squash: don't mount the mount points if already mounted

* Tue May 18 2021 Harald Hoyer <harald@redhat.com> - 054-6.git20210518
- fix for `str_replace: command not found`

* Mon May 17 2021 Harald Hoyer <harald@redhat.com> - 054-4.git20210517
- version 054

* Thu Apr 22 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 053-5
- Backport: fix(90kernel-modules): add watchdog drivers for generic initrd (rhbz 1592148)

* Mon Apr 19 2021 Dusty Mabe <dusty@dustymabe.com> - 053-4
- Backport: fix(dracut-logger.sh): double dash trigger unknown logger warnings during run
- Backport: fix(network-manager): nm-run.service: don't kill forked processes
- Backport: fix(network-manager): only run NetworkManager if rd.neednet=1
- Backport: fix(network-manager): use /run/NetworkManager/initrd/neednet in initqueue

* Mon Apr 19 2021 Adam Williamson <awilliam@redhat.com> - 053-3
- Fix removal of key system files when kdump enabled (thanks kasong) (#1936781)

* Thu Apr 08 2021 Adam Williamson <awilliam@redhat.com> - 053-2
- Backport upstream change reported to fix boot on some encrypted LVM setups (#1946074)

* Tue Feb 23 2021 Harald Hoyer <harald@redhat.com> - 053-1
- version 053

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 051-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 15 2020 Harald Hoyer <harald@redhat.com> - 051-1
- version 051

* Tue Oct 06 2020 Harald Hoyer <harald@redhat.com> - 050-167.git20201006
- git snapshot

* Fri Oct 02 2020 Harald Hoyer <harald@redhat.com> - 050-157.git20201002
- git snapshot

* Tue Sep 29 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 050-63.git20200529
- Fixes for Arm GPUs in early boot

* Fri Sep 25 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 050-62.git20200529
- Fix for Rockchip devices

* Wed Aug 19 2020 Merlin Mathesius <mmathesi@redhat.com> - 050-61.git20200529.3
- Correct conditionals to drop 51-dracut-rescue-postinst.sh for Fedora and
  recent RHEL releases

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 050-61.git20200529.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 050-61.git20200529.1
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri May 29 2020 Harald Hoyer <harald@redhat.com> - 050-61.git20200529
- git snapshot

* Mon Mar 16 2020 Harald Hoyer <harald@redhat.com> - 050-26.git20200316
- fixed `--tmpdir` mishandling

* Fri Mar 13 2020 Harald Hoyer <harald@redhat.com> - 050-25.git20200313
- network-manager: ensure that nm-run.sh is executed for rd.neednet

* Tue Mar 10 2020 Adam Williamson <awilliam@redhat.com> - 050-2
- Backport fix for pre-trigger stage early exit from upstream (#1811070)

* Wed Mar 04 2020 Harald Hoyer <harald@redhat.com> - 050-1
- version 050

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 049-27.git20181204.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 049-27.git20181204.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Adam Williamson <awilliam@redhat.com> - 049-27.git20181204
- Backport PR #578 to fix RHBZ #1719057 (installer boot bug)

* Thu Feb 14 2019 Adam Williamson <awilliam@redhat.com> - 049-26.git20181204
- Backport PR #541 to fix RHBZ #1676357 (crasher bug)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 049-25.git20181204.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 04 2018 Harald Hoyer <harald@redhat.com> - 049-25.git20181204
- git snapshot

* Wed Oct 24 2018 Harald Hoyer <harald@redhat.com> - 049-11.git20181024
- git snapshot

* Wed Oct 10 2018 Harald Hoyer <harald@redhat.com> - 049-4.git20181010
- fixed spec file
- git snapshot

* Mon Oct 08 2018 Harald Hoyer <harald@redhat.com> - 049-1
- version 049

* Fri Sep 21 2018 Harald Hoyer <harald@redhat.com> - 048-99.git20180921
- git snapshot

* Thu Jul 26 2018 Harald Hoyer <harald@redhat.com> - 048-14.git20180726
- bring back 51-dracut-rescue-postinst.sh

* Wed Jul 18 2018 Harald Hoyer <harald@redhat.com> - 048-6.git20180718
- git snapshot

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 048-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Harald Hoyer <harald@redhat.com> - 048-1
- version 048

* Fri Jun 22 2018 Adam Williamson <awilliam@redhat.com> - 047-34.git20180604.1
- Test build with proposed fix for #1593028

* Mon Jun 04 2018 Harald Hoyer <harald@redhat.com> - 047-34.git20180604
- git snapshot

* Tue May 15 2018 Harald Hoyer <harald@redhat.com> - 047-32.git20180515
- git snapshot

* Mon Mar 05 2018 Harald Hoyer <harald@redhat.com> - 047-8
- git snapshot

* Tue Feb 27 2018 Javier Martinez Canillas <javierm@redhat.com> - 047-2
- Allow generating initramfs images on the /boot directory

* Mon Feb 19 2018 Harald Hoyer <harald@redhat.com> - 047-1
- version 047

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 046-92.git20180118.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Harald Hoyer <harald@redhat.com> - 046-92
- git snapshot

* Fri Jan 05 2018 Harald Hoyer <harald@redhat.com> - 046-64
- git snapshot

* Fri Dec 01 2017 Harald Hoyer <harald@redhat.com> - 046-36
- git snapshot

* Wed Nov 29 2017 Harald Hoyer <harald@redhat.com> - 046-33
- git snapshot

* Thu Oct 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 046-20
- Add fix for some ARM SBCs

* Tue Oct 10 2017 Harald Hoyer <harald@redhat.com> - 046-19
- git snapshot

* Thu Aug 24 2017 Harald Hoyer <harald@redhat.com> - 046-7
- git snapshot

* Fri Aug 11 2017 Harald Hoyer <harald@redhat.com> - 046-2
- add support for dist-tag less build

* Fri Aug 11 2017 Harald Hoyer <harald@redhat.com> - 046-1
- version 046

* Mon Aug  7 2017 Peter Robinson <pbrobinson@fedoraproject.org> 045-21.git20170515
- Add upstream patches to fix a number of ARM devices with generic initrd

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 045-20.git20170515
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 045-19.git20170515
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Harald Hoyer <harald@redhat.com> - 045-18.git20170515
- git snapshot

* Wed Apr 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 044-178
- Add upstream patches needed for ARMv7/aarch64 fixes

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 044-177
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 08 2016 Harald Hoyer <harald@redhat.com> - 044-176
- git snapshot

* Fri Aug 19 2016 Harald Hoyer <harald@redhat.com> - 044-117
- git snapshot

* Thu Aug 18 2016 Harald Hoyer <harald@redhat.com> - 044-109
- git snapshot

* Fri Aug 05 2016 Adam Williamson <awilliam@redhat.com> - 044-76
- backport a single commit to fix RHBZ #1358416 (anaconda network init)

* Tue Jun 07 2016 Harald Hoyer <harald@redhat.com> - 044-75
- fix for systemd >= 230
- git snapshot

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 044-18.git20160108
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan  8 2016 Harald Hoyer <harald@redhat.com> - 044-17.git20160108
- include more HID driver
- include machine info file
- fix network carrier detection
- fix nbd
- do not copy over lldpad state
- restorecon the final initramfs image

* Tue Dec  1 2015 Harald Hoyer <harald@redhat.com> - 044-6.git20151201
- fix for readonly /run on shutdown
- fix for the dmsquash-live module
Resolves: rhbz#1286866

* Wed Nov 25 2015 Harald Hoyer <harald@redhat.com> - 044-4.git20151127
- fixes for the dmsquash-live module
- remove udev watch for raid members
- mode 0755 for the livenet generator
Resolves: rhbz#1285903

* Wed Nov 25 2015 Harald Hoyer <harald@redhat.com> - 044-1
- version 044

* Mon Nov 16 2015 Harald Hoyer <harald@redhat.com> - 043-174.git20151116
- git snapshot

* Mon Nov 16 2015 Harald Hoyer <harald@redhat.com> - 043-173.git20151116
- git snapshot

* Fri Nov 13 2015 Harald Hoyer <harald@redhat.com> - 043-172.git20151113
- git snapshot

* Tue Aug 11 2015 Harald Hoyer <harald@redhat.com> 043-60.git20150811
- fixed checkiso timeout
- fixed log output although quiet is set
- fixed qemu detection
- cleanup compressor handling

* Wed Jul 22 2015 Harald Hoyer <harald@redhat.com> 043-40.git20150710.2
- require "xz" to handle the kernel modules

* Fri Jul 10 2015 Harald Hoyer <harald@redhat.com> 043-40.git20150710
- git snapshot

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 043-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Harald Hoyer <harald@redhat.com> 043-1
- version 043, now with the complete tarball

* Thu Jun 11 2015 Harald Hoyer <harald@redhat.com> 042-1
- version 042, the answer to life, the universe and everything

* Thu Feb 19 2015 Harald Hoyer <harald@redhat.com> 041-10.git20150219
- git snapshot

* Sat Jan 31 2015 Harald Hoyer <harald@redhat.com> 041-1
- version 041

* Thu Jan 08 2015 Harald Hoyer <harald@redhat.com> 040-83.git20150108
- git snapshot

* Fri Dec 19 2014 Harald Hoyer <harald@redhat.com> 040-78.git20141219
- git snapshot

* Mon Dec 08 2014 Harald Hoyer <harald@redhat.com> 040-30.git20141208
- fixed dracut-shutdown

* Thu Dec 04 2014 Harald Hoyer <harald@redhat.com> 040-29.git20141204
- git snapshot

* Tue Sep 30 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 038-36.git20140815
- Allow media check to be cancelled (rhbz 1147941)

* Fri Sep 26 2014 Josh Boyer <jwboyer@fedoraproject.org> - 038-35.git20140815
- Enable early-microcode by default (rhbz 1083716)
- Fix changelog date

* Tue Aug 19 2014 Harald Hoyer <harald@redhat.com> - 038-34.git20140815
- git snapshot

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 038-31.git20140815
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Harald Hoyer <harald@redhat.com> 038-30.git20140815
- git snapshot

* Thu Jul 24 2014 Harald Hoyer <harald@redhat.com> 038-14.git20140724
- fixed lvm modules issues
Resolves: rhbz#1118890
- fixed vlan issues
- fixed prelink for FIPS
- new rd.route parameter
- more ARM modules

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 038-2
- fix license handling

* Mon Jun 30 2014 Harald Hoyer <harald@redhat.com> 038-1
- version 038

* Sat Jun 28 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 037-14.git20140628
- Pull most bugfixy commits from current git
Resolves: rhbz#1112061

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 037-13.git20140402
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Peter Robinson <pbrobinson@fedoraproject.org> 037-12.git20140402
- Fix achi/mmc/sdhci selection for non host based initrd

* Thu Apr 17 2014 Adam Williamson <awilliam@redhat.com> - 037-11.git20140402
- revert broken upstream change that causes RHBZ#1084766

* Wed Apr 02 2014 Harald Hoyer <harald@redhat.com> 037-10.git20140402
- fixed fstab.sys with systemd
- DHCPv6 fixes
- dm-cache module now included
- FCoE fixes

* Thu Mar 20 2014 Harald Hoyer <harald@redhat.com> 037-3.git20140320
- fixed dracut-initramfs-restore with microcode

* Thu Mar 20 2014 Harald Hoyer <harald@redhat.com> 037-1
- version 037

* Thu Feb 06 2014 Harald Hoyer <harald@redhat.com> 036-16.git20140206
- version 036
- parse dns information on "ip=" command line arg
- preserve ownership of files, if root creates the initramfs
- parse ibft nameserver settings
- do not run dhcp twice on an interface
- try to not reload systemd

* Wed Dec 18 2013 Harald Hoyer <harald@redhat.com> 034-74.git20131218
- do not systemctl daemon-reload
- do iscsistart for iscsi_firmware even without network

* Mon Dec 16 2013 Harald Hoyer <harald@redhat.com> 034-70.git20131216
- fixed systemd password waiting
- split out fcoe uefi
- fixed lvm thin tools check

* Thu Dec 05 2013 Harald Hoyer <harald@redhat.com> 034-62.git20131205
- fixed PATH shortener
- also install /etc/system-fips in the initramfs
- nbd, do not fail in hostonly mode
- add ohci-pci to the list of hardcoded modules
- lvm: do not run pvscan for lvmetad
- network fixes
- skip crypt swaps with password files
- fixed i18n

* Wed Oct 30 2013 Harald Hoyer <harald@redhat.com> 034-24.git20131030
- fixed booting with rd.iscsi.firmware and without root=
- fips: include crct10dif_generic
- fixed missing modules in hostonly, which have no modalias
- moved dracut to /usr/sbin

* Mon Oct 21 2013 Harald Hoyer <harald@redhat.com> 034-19.git20131021
- Fixed LVM with thin provisioning
Resolves: rhbz#1013767
Resolves: rhbz#1021083

* Fri Oct 18 2013 Harald Hoyer <harald@redhat.com> 034-18.git20131018
- Fixed LVM with thin provisioning
Resolves: rhbz#1013767
- fixed swap detection in host only mode

* Fri Oct 11 2013 Kyle McMartin <kyle@fedoraproject.org> 034-8.git20131008
- Force mmc_block and usb_storage into ARM initramfs.
Resolves: rhbz#1015234

* Tue Oct 08 2013 Harald Hoyer <harald@redhat.com> 034-7.git20131008
- lvm: install thin utils for non-hostonly
- do not bail out, if kernel modules dir is missing
- dmsquash-live: add /dev/mapper/live-base
Resolves: rhbz#1016726

* Tue Oct 08 2013 Harald Hoyer <harald@redhat.com> 034-1
- version 034
- add option to turn on/off prelinking
    --prelink, --noprelink
    do_prelink=[yes|no]
- add ACPI table overriding
- do not log to syslog/kmsg/journal for UID != 0
- lvm/mdraid: Fix LVM on MD activation
- bcache module removed (now in bcache-tools upstream)
- mdadm: also install configs from /etc/mdadm.conf.d
- fixes for mdadm-3.2.6+
- fcoe: add FCoE UEFI boot device support
- rootfs-block: add support for the rootfallback= kernel cmdline option

* Fri Sep 13 2013 Harald Hoyer <harald@redhat.com> 033-3.git20130913
- do not dhcp members of team, bond, etc.
- harden against weird ppc kernel driver
Resolves: rhbz#1007891

* Thu Sep 12 2013 Harald Hoyer <harald@redhat.com> 033-1
- do not cache the kernel cmdline
Resolves: rhbz#989944
- fixed iso-scan
Resolves: rhbz#1005487
- support blkid with bcache
Resolves: rhbz#1003207
- ifup with dhcp, if no ip= params specified
Resolves: rhbz#989944
- silently try to umount rpc_pipefs
Resolves: rhbz#999996

* Wed Sep 04 2013 Harald Hoyer <harald@redhat.com> 032-23.git20130904
- fixed curl error with zero size kickstart file
Resolves: rhbz#989133
- fixed systemd-cat failure, when systemd is installed
  but not actually running
Resolves: rhbz#1002021
- do not fail on empty dracut module directories
Resolves: rhbz#1003153

* Tue Aug 20 2013 Harald Hoyer <harald@redhat.com> 032-1
- fix for kdump in FIPS mode
Resolves: rhbz#920931
- fixed iBFT booting
Resolves: rhbz#989944
- fixed FIPS mode initramfs creation
Resolves: rhbz#990250
- shutdown: fixed killall_proc_mountpoint()
Resolves: rhbz#996549
- disable lvmetad in the initramfs
Resolves: rhbz#996627
- require dhclient

* Mon Aug 12 2013 Harald Hoyer <harald@redhat.com> 031-29.git20130812
- added missing "then" in initqueue

* Mon Aug 12 2013 Harald Hoyer <harald@redhat.com> 031-28.git20130812
- fixed typo in hostonly device recognition

* Fri Aug 09 2013 Harald Hoyer <harald@redhat.com> 031-24.git20130809
- fixed logging to journal

* Fri Aug 09 2013 Harald Hoyer <harald@redhat.com> 031-23.git20130809
- fixed lsinitrd

* Fri Aug 09 2013 Harald Hoyer <harald@redhat.com> 031-22.git20130809
- lsinitrd.sh: add old cpio signature
- dracut.sh: call find with -print0 and cpio with --null
- dracut.asc: small corrections
- systemd/dracut-initqueue.sh: continue to boot if finished failed
- dracut.sh/dracut-functions.sh: handle root on non-block device
- dracut-functions.sh: removed non dracut-install shell functions
- dracut-functions.sh: inst_multiple == dracut_install
- 51-dracut-rescue.install: fixed rescue image creation
- dracut.sh: do not strip in FIPS mode
Resolves: rhbz#990250
- dracut.sh: check the value of --kver
- crypt: Fix typo--/etc/crypttab not /etc/cryptab
- network/net-lib.sh: fix ibft interface configuration
- iscsi/module-setup.sh: install some modules regardless of hostonly
- multipath: need_shutdown if multipath devices exist
Resolves: rhbz#994913
- omit drivers fix

* Thu Aug 01 2013 Harald Hoyer <harald@redhat.com> 031-7.git20130801
- also install vt102 terminfo

* Wed Jul 31 2013 Harald Hoyer <harald@redhat.com> 031-6.git20130731
- cmssetup: fixed port for zfcp.conf
- lvm: call lvchange with --yes to boot from snapshots

* Wed Jul 31 2013 Harald Hoyer <harald@redhat.com> 031-4.git20130731
- remove action_on_fail kernel command line parameter

* Wed Jul 31 2013 Harald Hoyer <harald@redhat.com> 031-3.git20130731
- do not include adjtime and localtime in the initramfs
- write out vlan configs

* Wed Jul 31 2013 Harald Hoyer <harald@redhat.com> 031-1
- do not include the resume dracut module in hostonly mode,
  if no swap is present
- don't warn twice about omitted modules
- use systemd-cat for logging on systemd systems, if logfile is unset
- fixed PARTUUID parsing
- support kernel module signing keys
- do not install the usrmount dracut module in hostonly mode,
  if /sbin/init does not live in /usr
- add debian udev rule files
- add support for bcache
- network: handle bootif style interfaces
  e.g. ip=77-77-6f-6f-64-73:dhcp
- add support for kmod static devnodes
- add vlan support for iBFT

* Wed Jul 24 2013 Kyle McMartin <kyle@redhat.com> 030-2
- Add ehci-tegra.ko to initramfs to allow rawhide tegra based platforms
  to boot off USB disks.

* Wed Jul 17 2013 Harald Hoyer <harald@redhat.com> 030-1
- support new persistent network interface names
- fix findmnt calls, prevents hang on stale NFS mounts
- add systemd.slice and slice.target units
- major shell cleanup
- support root=PARTLABEL= and root=PARTUUID=
- terminfo: only install l/linux v/vt100 and v/vt220
- unset all LC_* and LANG, 10% faster
- fixed dependency loop for dracut-cmdline.service
- do not wait_for_dev for the root devices
- do not wait_for_dev for devices, if dracut-initqueue is not needed
- support early microcode loading with --early-microcode
- dmraid, let dmraid setup its own partitions
- sosreport renamed to rdsosreport

* Fri Jun 14 2013 Harald Hoyer <harald@redhat.com> 029-1
- wait for IPv6 auto configuration
Resolves: rhbz#973719
- i18n: make the default font configurable
- systemd/dracut-pre-pivot.service: also execute for cleanup hooks or rd.break
- add dracut-shutdown.service.8 manpage
- lvm: redirect error message of lvs to /dev/null
Resolves: rhbz#921235

* Wed Jun 12 2013 Harald Hoyer <harald@redhat.com> 028-1
- lvm: fixed "thin" recognition
Resolves: rhbz#921235
- install libs also from one dir above
  fixes booting power6 generated initramfs on power7
- setup correct system time and time zone in initrd
- cms fixups
Resolves: rhbz#970982 rhbz#971025 rhbz#825199
- iso-scan/filename fixes
Resolves: rhbz#972337
- add udev rules for persistent network naming
Resolves: rhbz#972662

* Tue Jun 04 2013 Dennis Gilmore <dennis@ausil.us> 027-82.git20130531
- add patch to include  panel-tfp410 module on arm systems

* Fri May 31 2013 Harald Hoyer <harald@redhat.com> 027-81.git20130531
- fix btrfs mount flags for /usr
- degrade message about missing tools for stripping
Resolves: rhbz#958519
- set environment vars DRACUT_SYSTEMD, NEWROOT in service file
Resolves: rhbz#963159
- don't add volatile swap partitions to host_devs
- add libssl.so.10 to make kdump work with fips mode
- readd selinux dracut module for kdump
- url-lib/url-lib.sh: turn off curl globbing
Resolves: rhbz#907497
- include btrfs-zero-log in the initramfs
Resolves: rhbz#963257
- proper NAME the network interfaces
Resolves: rhbz#965842
- install default font latarcyrheb-sun16
Resolves: rhbz#927564
- optionally install /etc/pcmcia/config.opts
Resolves: rhbz#920076
- fix ONBOOT for slaves, set TYPE=Bond for bonding
Resolves: rhbz#919001
- add nvme kernel module
Resolves: rhbz#910734
- add xfs_metadump
- selinux: load_policy script fix
- add hid-hyperv and hv-vmbus kernel modules
- add parameter rd.live.squashimg
Resolves: rhbz#789036 rhbz#782108
- wait for all required interfaces if "rd.neednet=1"
Resolves: rhbz#801829
- lvm: add tools for thin provisioning
Resolves: rhbz#921235
- ifcfg/write-ifcfg.sh: fixed ifcfg file generation
- do not wait for mpath* devices
Resolves: rhbz#969068

* Wed May 22 2013 Adam Williamson <awilliam@redhat.com> 027-46.git20130430
- don't specify "p" as a separator for dmraid
Resolves: rhbz#966162

* Tue Apr 30 2013 Harald Hoyer <harald@redhat.com> 027-45.git20130430
- fixed fips mode more
Resolves: rhbz#956521

* Thu Apr 25 2013 Harald Hoyer <harald@redhat.com> 027-39.git20130425
- fix shutdown, if /dev/console is not writeable
- fixed fips mode
Resolves: rhbz#956521

* Thu Apr 18 2013 Harald Hoyer <harald@redhat.com> 027-36.git20130418
- fix initramfs creation on noexec tmpdir
Resolves: rhbz#953426
- more options for lsinitrd
- bash completion for lsinitrd
- do not output debug information on initramfs creation, if rd.debug is
  on the kernel command line
- drop requirement on 'file', lsinitrd can find the magic on its own

* Mon Apr 15 2013 Harald Hoyer <harald@redhat.com> 027-26.git20130415
- do not call plymouth with full path
- include systemd-random-seed-load.service
- fix ca-bundle.crt for ssl curl
Resolves: rhbz#950770
- add support for "iso-scan/filename" kernel parameter

* Wed Apr 10 2013 Harald Hoyer <harald@redhat.com> 027-19.git20130410
- also handle UUID= entries in crypttab in host-only mode
Resolves:rhbz#919752

* Tue Apr 09 2013 Harald Hoyer <harald@redhat.com> 027-17.git20130409
- only include needed /etc/crypttab entries
Resolves:rhbz#919752
- add support for bridge over team and vlan
- support multiple bonding interfaces
- add "action_on_fail=" kernel command line parameter
- add support for bridge over a vlan tagged interface

* Fri Apr 05 2013 Harald Hoyer <harald@redhat.com> 027-10.git20130405
- fix crypto password timeout on the dracut side

* Tue Mar 26 2013 Harald Hoyer <harald@redhat.com> 027-1
- version 027

* Wed Mar 20 2013 Harald Hoyer <harald@redhat.com> 026-72.git20130320
- fix rescue image naming
Resolves: rhbz#923439
- turn off host-only mode if essential system filesystems not mounted
- turn off host-only mode if udev database is not accessible

* Tue Mar 19 2013 Harald Hoyer <harald@redhat.com> 026-62.git20130319
- fix dracut service ordering
Resolves: rhbz#922991

* Mon Mar 18 2013 Harald Hoyer <harald@redhat.com> 026-56.git20130318
- don't fail hard on kernel modules install
Resolves: rhbz#922565

* Mon Mar 18 2013 Harald Hoyer <harald@redhat.com> 026-55.git20130318
- install all host filesystem drivers
Resolves: rhbz#922565

* Sat Mar 16 2013 Harald Hoyer <harald@redhat.com> 026-54.git20130316
- fix for squashfs
Resolves: rhbz#922248
- documentation fixes
- sosreport, mkdir /run/initramfs

* Fri Mar 15 2013 Harald Hoyer <harald@redhat.com> 026-48.git20130315
- use new initrd.target from systemd
- fixed rescue generation

* Wed Mar 13 2013 Harald Hoyer <harald@redhat.com> 026-33.git20130313
- add module-load.d modules to the initramfs
- add sysctl.d to the initramfs
- optimize plymouth module for systemd mode
- add new dracut parameter "--regenerate-all"
- add new dracut parameter "--noimageifnotneeded"
- shutdown: mount move /run /sys /dev /proc out of /oldroot
  before pre-shutdown
- add bash completion for dracut

* Wed Mar 13 2013 Harald Hoyer <harald@redhat.com> 026-19.git20130313
- fix switch-root and local-fs.target problem
- add norescue and nohostonly subpackages

* Mon Mar 11 2013 Harald Hoyer <harald@redhat.com> 026-15.git20130311
- update to recent git

* Fri Mar 08 2013 Harald Hoyer <harald@redhat.com> 026-1
- version 026

* Mon Feb 11 2013 Harald Hoyer <harald@redhat.com> 025-35.git20130211
- update to recent git

* Wed Jan 23 2013 Harald Hoyer <harald@redhat.com> 025-1
- version 025

* Tue Aug 21 2012 Harald Hoyer <harald@redhat.com> 023-13.git20120821
- reintroduce rd.neednet, which reenables anaconda networking
- fix some dracut-install corner cases
- fix FIPS for /boot not on extra partition

* Wed Aug 01 2012 Dennis Gilmore <dennis@ausil.us> - 023-2
- add patch to include omap_hsmmc for arm

* Wed Aug 01 2012 Harald Hoyer <harald@redhat.com> 023-1
- version 023

* Mon Jul 30 2012 Harald Hoyer <harald@redhat.com> 022-99.git20120730
- removed install of missing finished-ask-password.sh

* Mon Jul 30 2012 Harald Hoyer <harald@redhat.com> 022-97.git20120730
- moved crypt setup to systemd units

* Fri Jul 27 2012 Harald Hoyer <harald@redhat.com> 022-63.git20120727
- fixed dracut-install bug if /var/tmp contains a symlink
- fixed some partx issues

* Mon Jul 23 2012 Harald Hoyer <harald@redhat.com> 022-5.git20120723
- dracut.8: added more documentation about executing dracut

* Fri Jul 20 2012 Harald Hoyer <harald@redhat.com> 022-2.git20120720
- fixed some race condition for resume from hibernation

* Fri Jul 20 2012 Harald Hoyer <harald@redhat.com> 022-1
- version 022
- host-only kernel modules fix

* Fri Jul 20 2012 Harald Hoyer <harald@redhat.com> 021-1
- version 21
- systemd in the initramfs reenabled
- new option "--kver"

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 020-97.git20120717
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Harald Hoyer <harald@redhat.com> 020-96.git20120717
- disabled systemd in the initramfs, until it works correctly

* Wed Jul 11 2012 Harald Hoyer <harald@redhat.com> 020-84.git20120711
- add back "--force" to switch-root, otherwise systemd umounts /run

* Wed Jul 11 2012 Harald Hoyer <harald@redhat.com> 020-83.git20120711
- more systemd journal fixes
- nfs module fix
- install also /lib/modprobe.d/*
- fixed dracut-shutdown service
- safeguards for dracut-install
- for --include also copy symlinks

* Tue Jul 10 2012 Harald Hoyer <harald@redhat.com> 020-72.git20120710
- stop journal rather than restart
- copy over dracut services to /run/systemd/system

* Tue Jul 10 2012 Harald Hoyer <harald@redhat.com> 020-70.git20120710
- more systemd unit fixups
- restart systemd-journald in switch-root post
- fixed dracut-install loader ldd error message

* Mon Jul 09 2012 Harald Hoyer <harald@redhat.com> 020-64.git20120709
- fixed plymouth install
- fixed resume
- fixed dhcp
- no dracut systemd services installed in the system

* Mon Jul 09 2012 Harald Hoyer <harald@redhat.com> 020-57.git20120709
- more fixups for systemd-udevd unit renaming

* Mon Jul 09 2012 Harald Hoyer <harald@redhat.com> 020-55.git20120709
- require systemd >= 186
- more fixups for systemd-udevd unit renaming

* Mon Jul 09 2012 Harald Hoyer <harald@redhat.com> 020-52.git20120709
- fixed prefix in 01-dist.conf

* Fri Jul 06 2012 Harald Hoyer <harald@redhat.com> 020-51.git20120706
- cope with systemd-udevd unit renaming
- fixed network renaming
- removed dash module

* Mon Jul 02 2012 Harald Hoyer <harald@redhat.com> 020-22.git20120702
- fixed kernel modules install

* Mon Jul 02 2012 Harald Hoyer <harald@redhat.com> 020-21.git20120702
- moved /usr/bin/dracut-install to /usr/lib
- more speedups

* Fri Jun 29 2012 Harald Hoyer <harald@redhat.com> 020-1
- version 020
- new /usr/bin/dracut-install tool
- major speedup of the image creation

* Mon Jun 25 2012 Harald Hoyer <harald@redhat.com> 019-92.git20120625
- support vlan tagged binding
- speedup initramfs emergency service
- speedup image creation
- fix installkernel() return codes
Resolves: rhbz#833256
- add qemu and qemu-net modules to add qemu drivers even in host-only
- speedup btrfs and xfs fsck (nop)
- no more mknod in the initramfs (fixes plymouth on s390)

* Thu Jun 21 2012 Harald Hoyer <harald@redhat.com> 019-62.git20120621
- do not require pkg-config for systemd
- i18n fixes
- less systemd services in the initramfs

* Thu Jun 21 2012 Harald Hoyer <harald@redhat.com> 019-57.git20120620
- systemd is now the default init in the initramfs

* Mon Jun 18 2012 Harald Hoyer <harald@redhat.com> 019-40.git20120618
- new upstream version

* Mon Jun 11 2012 Harald Hoyer <harald@redhat.com> 019-16.git20120611
- new upstream version

* Tue Jun 05 2012 Dennis Gilmore <dennis@ausil.us> 019-2
- include omapdrm with the arm modules

* Mon Jun 04 2012 Harald Hoyer <harald@redhat.com> 019-1
- version 019-1

* Tue May 22 2012 Harald Hoyer <harald@redhat.com> 018-74.git20120522
- new upstream version

* Thu May 17 2012 Dennis Gilmore <dennis@ausil.us> 018-53.git20120509
- add patch to pull in arm storage modules

* Wed May 09 2012 Harald Hoyer <harald@redhat.com> 018-52.git20120509
- new upstream version

* Fri May 04 2012 Harald Hoyer <harald@redhat.com> 018-40.git20120504
- new upstream version

* Wed Apr 25 2012 Harald Hoyer <harald@redhat.com> 018-37.git20120425.1
- fixup for multipath and iscsi host-only detection

* Wed Apr 25 2012 Harald Hoyer <harald@redhat.com> 018-37.git20120425
- fixed udevd location

* Tue Apr 24 2012 Harald Hoyer <harald@redhat.com> 018-33.git20120424
- new upstream version

* Thu Apr 19 2012 Harald Hoyer <harald@redhat.com> 018-25.git20120419
- fixed network for non-network root (like installer media)

* Wed Apr 18 2012 Harald Hoyer <harald@redhat.com> 018-22.git20120418
- new upstream version

* Mon Apr 16 2012 Harald Hoyer <harald@redhat.com> 018-12.git20120416
- new upstream version, which fixes various anaconda loader issues

* Thu Apr 05 2012 Harald Hoyer <harald@redhat.com> 018-1
- version 018

* Thu Mar 22 2012 Harald Hoyer <harald@redhat.com> 017-62.git20120322
- fixed /run prefix copying

* Wed Mar 21 2012 Harald Hoyer <harald@redhat.com> 017-59.git20120321
- new upstream version, which fixes various anaconda loader issues

* Mon Mar 12 2012 Harald Hoyer <harald@redhat.com> 017-43.git20120312
- live image: fixed image uncompression
- live updates for livenet

* Thu Mar 08 2012 Harald Hoyer <harald@redhat.com> 017-40.git20120308
- add s390 ctcm network kernel module

* Thu Mar 08 2012 Harald Hoyer <harald@redhat.com> 017-39.git20120308
- kill dhclient silently
- cleanup and fix network config writeout to /run/initramfs/state
Resolves: rhbz#799989
- various cleanups

* Fri Mar 02 2012 Harald Hoyer <harald@redhat.com> 017-22.git20120302
- nfs path fixes for live image over nfs
  root=live:nfs://10.10.10.10:/srv/all/install.img ip=dhcp rd.neednet

* Thu Mar 01 2012 Harald Hoyer <harald@redhat.com> 017-19.git20120301
- fixed include of some kernel modules

* Wed Feb 29 2012 Harald Hoyer <harald@redhat.com> 017-17.git20120229
- update to latest git
- fixes for convertfs (/usr-move)

* Fri Feb 24 2012 Harald Hoyer <harald@redhat.com> 017-1
- version 017

* Fri Feb 17 2012 Harald Hoyer <harald@redhat.com> 016-9.git20120217
- update to latest git

* Wed Feb 15 2012 Harald Hoyer <harald@redhat.com> 016-1
- version 016

* Mon Feb 13 2012 Harald Hoyer <harald@redhat.com> 015-9.git20120213
- update to latest git

* Sun Feb 12 2012 Kay Sievers <kay@redhat.com> - 015-9.git20120210
- fix dependency loop in systemd service files

* Fri Feb 10 2012 Harald Hoyer <harald@redhat.com> 015-8.git20120210
- update to latest git

* Thu Feb 09 2012 Harald Hoyer <harald@redhat.com> 015-7.git20120209
- update to latest git

* Thu Feb 09 2012 Harald Hoyer <harald@redhat.com> 015-4.git20120209
- update to latest git

* Wed Feb 08 2012 Harald Hoyer <harald@redhat.com> 015-3.git20120208
- update to latest git

* Tue Feb 07 2012 Harald Hoyer <harald@redhat.com> 015-1
- version 015

* Thu Feb 02 2012 Harald Hoyer <harald@redhat.com> 014-81.git20120202
- update to latest git

* Thu Feb 02 2012 Harald Hoyer <harald@redhat.com> 014-80.git20120202
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-77.git20120126.1
- rebuild for rawhide

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-77.git20120126
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-76.git20120126
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-75.git20120126
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-74.git20120126
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-73.git20120126
- update to latest git

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 014-72.git20120126
- update to latest git

* Mon Jan 23 2012 Harald Hoyer <harald@redhat.com> 014-65.git20120123
- update to latest git

* Mon Jan 23 2012 Harald Hoyer <harald@redhat.com> 014-61.git20120123
- update to latest git

* Tue Jan 17 2012 Harald Hoyer <harald@redhat.com> 014-38.git20120117
- update to latest git

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 014-10.git20111215
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Harald Hoyer <harald@redhat.com> 014-9.git20111215
- update to latest git
- lots of patch changes

* Fri Oct 21 2011 Harald Hoyer <harald@redhat.com> 013-100.git20111021
- update to latest git

* Thu Oct 20 2011 Harald Hoyer <harald@redhat.com> 013-93.git20111020
- update to latest git

* Wed Oct 19 2011 Harald Hoyer <harald@redhat.com> 013-85.git20111019
- update to latest git

* Tue Oct 04 2011 Harald Hoyer <harald@redhat.com> 013-15
- fixed mdraid container handling
Resolves: rhbz#743240

* Thu Sep 22 2011 Harald Hoyer <harald@redhat.com> 013-13
- fixed mdraid issues
- fixed btrfsck
Resolves: rhbz#735602

* Wed Sep 21 2011 Harald Hoyer <harald@redhat.com> 013-12
- removed patch backup files
- reintroduced /dev/live

* Tue Sep 20 2011 Harald Hoyer <harald@redhat.com> 013-11
- move mounting of securitfs to a seperate module
Resolves: rhbz#737140

* Tue Sep 20 2011 Harald Hoyer <harald@redhat.com> 013-10
- mount securitfs with the correct source
Resolves: rhbz#737140

* Tue Sep 20 2011 Harald Hoyer <harald@redhat.com> 013-9
- do not carry over initramfs udev rules
Resolves: rhbz#734096

* Fri Sep 02 2011 Harald Hoyer <harald@redhat.com> 013-8
- hopefully fixed one part of a loop/udev and loop/mount race
Resolves: rhbz#735199

* Wed Aug 31 2011 Harald Hoyer <harald@redhat.com> 013-7
- add /lib/udev/input_id to the initramfs
- fix hmac install

* Tue Aug 30 2011 Harald Hoyer <harald@redhat.com> 013-6
- fixed environment passing to real init
Resolves: rhbz#733674
- fixed lvm on md

* Mon Aug 29 2011 Harald Hoyer <harald@redhat.com> 013-5
- fixed rhel/fedora version checks

* Wed Aug 17 2011 Harald Hoyer <harald@redhat.com> 013-4
- fixed crash with livenet installed

* Wed Aug 17 2011 Harald Hoyer <harald@redhat.com> 013-3
- fixed live iso mounting
Resolves: rhbz#730579

* Fri Aug 12 2011 Harald Hoyer <harald@redhat.com> 013-1
- fixed symlink creation for lorax

* Wed Aug 10 2011 Harald Hoyer <harald@redhat.com> 011-41.git20110810
- fixed getargs() for empty args

* Wed Aug 10 2011 Harald Hoyer <harald@redhat.com> 011-40.git20110810
- fixed symbolic link creation in the initramfs
Resolves: rhbz#728863

* Wed Jul 20 2011 Harald Hoyer <harald@redhat.com> 011-15.git20110720
- "eject" is optional now
- refined shutdown procedure

* Mon Jul 18 2011 Harald Hoyer <harald@redhat.com> 011-1
- version 011

* Fri May 20 2011 Harald Hoyer <harald@redhat.com> 011-0.1
- git snapshot of pre-version 011

* Fri Apr 01 2011 Harald Hoyer <harald@redhat.com> 010-1
- version 010

* Thu Mar 31 2011 Harald Hoyer <harald@redhat.com> 009-5
- fixed PATH and kmsg logging

* Thu Mar 31 2011 Harald Hoyer <harald@redhat.com> 009-4
- fixed dmsquash rule generation
- fixed fips boot arg parsing
- fixed plymouth pid generation

* Wed Mar 30 2011 Harald Hoyer <harald@redhat.com> 009-3
- fixed dhcp
- added /lib/firmware/updates to firmware directories 
- fixed LiveCD /dev/.initramfs fallback
- fixed cdrom polling
- dropped net-tools dependency

* Tue Mar 29 2011 Harald Hoyer <harald@redhat.com> 009-2
- fixed empty output file argument handling:
  "dracut '' <kernel version>" 

* Mon Mar 28 2011 Harald Hoyer <harald@redhat.com> 009-1
- version 009

* Thu Mar 17 2011 Harald Hoyer <harald@redhat.com> 009-0.1
- version 009 prerelease

* Tue Feb 22 2011 Harald Hoyer <harald@redhat.com> 008-7
- fixed lvm version parsing

* Tue Feb 22 2011 Harald Hoyer <harald@redhat.com> 008-6
- fixed lvm version parsing

* Mon Feb 21 2011 Harald Hoyer <harald@redhat.com> 008-5
- fixed i18n unicode setting
- set cdrom in kernel polling

* Fri Feb 18 2011 Harald Hoyer <harald@redhat.com> 008-4
- readded dist tag

* Fri Feb 18 2011 Harald Hoyer <harald@redhat.com> 008-3
- fixed i18n
- turned off selinux by default

* Wed Feb 09 2011 Harald Hoyer <harald@redhat.com> 008-2
- do not write dracut.log to /tmp under any circumstances
- touch /dev/.systemd/plymouth after plymouth started

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 008-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Harald Hoyer <harald@redhat.com> 008-1
- version 008-1

* Mon Jan 17 2011 Harald Hoyer <harald@redhat.com> 008-0.11
- removed "mount" requirement

* Thu Nov 18 2010 Harald Hoyer <harald@redhat.com> - 008-0.10
- dracut-008 pre git snapshot
- fixes /dev/dri permissions
Resolves: rhbz#626559

* Fri Nov 12 2010 Harald Hoyer <harald@redhat.com> 008-0.9
- dracut-008 pre git snapshot
- fixes /dev/.udev permissions
Resolves: rhbz#651594

* Wed Nov  3 2010 Harald Hoyer <harald@redhat.com> - 008-0.8
- fixed fsck -a option

* Fri Oct 29 2010 Harald Hoyer <harald@redhat.com> 008-0.7
- added fsck to initramfs

* Fri Oct 29 2010 Harald Hoyer <harald@redhat.com> 008-0.6
- fixed rpm macros

* Fri Oct 29 2010 Harald Hoyer <harald@redhat.com> 008-0.5
- dracut-008 pre git snapshot

* Mon Aug 09 2010 Harald Hoyer <harald@redhat.com> 007-1
- version 007

* Thu Jun 17 2010 Harald Hoyer <harald@redhat.com> 006-1
- version 006

* Fri Jun 11 2010 Harald Hoyer <harald@redhat.com>
- Remove requirements, which are not really needed
Resolves: rhbz#598509
- fixed copy of network config to /dev/.initramfs/ (patch 146)
Resolves: rhbz#594649
- more password beauty (patch 142)
Resolves: rhbz#561092
- support multiple iSCSI disks (patch 143)
Resolves: rbhz#580190
- fixed selinux=0 (patch 130)
Resolves: rhbz#593080
- add support for booting LVM snapshot root volume (patch 145)
Resolves: rbhz#602723
- remove hardware field from BOOTIF= (patch 148)
Resolves: rhbz#599593
- add aes kernel modules and fix crypt handling (patch 137, patch 140 and patch 147)
Resolves: rhbz#600170

* Thu May 27 2010 Harald Hoyer <harald@redhat.com> 
- fixed Requirements
- fixed autoip6 
Resolves: rhbz#538388
- fixed multipath
Resolves: rhbz#595719

* Thu May 06 2010 Harald Hoyer <harald@redhat.com> 
- only display short password messages
Resolves: rhbz#561092

* Thu May 06 2010 Harald Hoyer <harald@redhat.com>
- fixed dracut manpages 
Resolves: rhbz#589109
- use ccw-init and ccw rules from s390utils
Resolves: rhbz#533494
- fixed fcoe
Resolves: rhbz#486244
- various other bugfixes seen in Fedora

* Tue Apr 20 2010 Harald Hoyer <harald@redhat.com> 
- fixed network with multiple nics
- fixed nfsidmap paths
- do not run blkid on non active container raids
- fixed cdrom polling mechanism
- update to latest git

* Thu Apr 15 2010 Harald Hoyer <harald@redhat.com>
- fixed dracut manpages
- dmraid parse different error messages
- add cdrom polling mechanism for slow cdroms
- add module btrfs
- teach dmsquash live-root to use rootflags
- trigger udev with action=add
- fixed add_drivers handling 
- add sr_mod
- use pigz instead of gzip, if available

* Thu Mar 25 2010 Harald Hoyer <harald@redhat.com> 
- removed firmware requirements (rhbz#572634)
- add /etc/dracut.conf.d
- Resolves: rhbz#572634

* Fri Mar 19 2010 Harald Hoyer <harald@redhat.com> 
- version 005

* Fri Mar 19 2010 Harald Hoyer <harald@redhat.com> 
- fixed rpmlint errors (rhbz#570547)
- removed firmware package from dracut-kernel (rhbz#572634)
- add dcb support to dracut's FCoE support (rhbz#563794)
- force install some modules in hostonly mode (rhbz#573094)
- various other bugfixes
- Resolves: rhbz#570547, rhbz#572634, rhbz#563794, rhbz#573094

* Thu Feb 18 2010 Harald Hoyer <harald@redhat.com> 004-15
- fixed "selinux=0" booting (rhbz#566376)
- fixed internal IFS handling
- Resolves: rhbz#566376

* Fri Jan 29 2010 Harald Hoyer <harald@redhat.com> 004-5
- fixed firmware.sh bug (#559975 #559597)

* Tue Jan 26 2010 Harald Hoyer <harald@redhat.com> 004-4
- add multipath check

* Tue Jan 26 2010 Harald Hoyer <harald@redhat.com> 004-3
- fix selinux handling if .autorelabel is present
- Resolves: rhbz#557744

* Wed Jan 20 2010 Harald Hoyer <harald@redhat.com> 004-2
- fix emergency_shell argument parsing
- Related: rhbz#543948

* Fri Jan 15 2010 Harald Hoyer <harald@redhat.com> 004-1
- version 004
- Resolves: rhbz#529339 rhbz#533494 rhbz#548550 
- Resolves: rhbz#548555 rhbz#553195

* Wed Jan 13 2010 Harald Hoyer <harald@redhat.com> 003-3
- add Obsoletes of mkinitrd/nash/libbdevid-python
- Related: rhbz#543948

* Wed Jan 13 2010 Warren Togami <wtogami@redhat.com> 003-2
- nbd is Fedora only

* Fri Nov 27 2009 Harald Hoyer <harald@redhat.com> 003-1
- version 003

* Mon Nov 23 2009 Harald Hoyer <harald@redhat.com> 002-26
- add WITH_SWITCH_ROOT make flag
- add fips requirement conditional
- add more device mapper modules (bug #539656)

* Fri Nov 20 2009 Dennis Gregorovic <dgregor@redhat.com> - 002-25.1
- nss changes for Alpha 3

* Thu Nov 19 2009 Harald Hoyer <harald@redhat.com> 002-25
- add more requirements for dracut-fips (bug #539257)

* Tue Nov 17 2009 Harald Hoyer <harald@redhat.com> 002-24
- put fips module in a subpackage (bug #537619)

* Tue Nov 17 2009 Harald Hoyer <harald@redhat.com> 002-23
- install xdr utils for multipath (bug #463458)

* Thu Nov 12 2009 Harald Hoyer <harald@redhat.com> 002-22
- add module 90multipath
- add module 01fips
- renamed module 95ccw to 95znet (bug #533833)
- crypt: ignore devices in /etc/crypttab (root is not in there)
- dasd: only install /etc/dasd.conf in hostonly mode (bug #533833)
- zfcp: only install /etc/zfcp.conf in hostonly mode (bug #533833)
- kernel-modules: add scsi_dh scsi_dh_rdac scsi_dh_emc (bug #527750)
- dasd: use dasdconf.sh from s390utils (bug #533833)

* Fri Nov 06 2009 Harald Hoyer <harald@redhat.com> 002-21
- fix rd_DASD argument handling (bug #531720)
- Resolves: rhbz#531720

* Wed Nov 04 2009 Harald Hoyer <harald@redhat.com> 002-20
- fix rd_DASD argument handling (bug #531720)
- Resolves: rhbz#531720

* Tue Nov 03 2009 Harald Hoyer <harald@redhat.com> 002-19
- changed rd_DASD to rd_DASD_MOD (bug #531720)
- Resolves: rhbz#531720

* Tue Oct 27 2009 Harald Hoyer <harald@redhat.com> 002-18
- renamed lvm/device-mapper udev rules according to upstream changes
- fixed dracut search path issue

* Mon Oct 26 2009 Harald Hoyer <harald@redhat.com> 002-17
- load dm_mod module (bug #530540)

* Fri Oct 09 2009 Jesse Keating <jkeating@redhat.com> - 002-16
- Upgrade plymouth to Requires(pre) to make it show up before kernel

* Thu Oct 08 2009 Harald Hoyer <harald@redhat.com> 002-15
- s390 ccw: s/layer1/layer2/g

* Thu Oct 08 2009 Harald Hoyer <harald@redhat.com> 002-14
- add multinic support
- add s390 zfcp support
- add s390 network support

* Wed Oct 07 2009 Harald Hoyer <harald@redhat.com> 002-13
- fixed init=<command> handling
- kill loginit if "rdinitdebug" specified
- run dmsquash-live-root after udev has settled (bug #527514)

* Tue Oct 06 2009 Harald Hoyer <harald@redhat.com> 002-12
- add missing loginit helper
- corrected dracut manpage

* Thu Oct 01 2009 Harald Hoyer <harald@redhat.com> 002-11
- fixed dracut-gencmdline for root=UUID or LABEL

* Thu Oct 01 2009 Harald Hoyer <harald@redhat.com> 002-10
- do not destroy assembled raid arrays if mdadm.conf present
- mount /dev/shm 
- let udevd not resolve group and user names
- preserve timestamps of tools on initramfs generation
- generate symlinks for binaries correctly
- moved network from udev to initqueue
- mount nfs3 with nfsvers=3 option and retry with nfsvers=2
- fixed nbd initqueue-finished
- improved debug output: specifying "rdinitdebug" now logs
  to dmesg, console and /init.log
- stop udev before killing it
- add ghost /var/log/dracut.log
- dmsquash: use info() and die() rather than echo
- strip kernel modules which have no x bit set
- redirect stdin, stdout, stderr all RW to /dev/console
  so the user can use "less" to view /init.log and dmesg

* Tue Sep 29 2009 Harald Hoyer <harald@redhat.com> 002-9
- make install of new dm/lvm udev rules optionally
- correct dasd module typo

* Fri Sep 25 2009 Warren Togami <wtogami@redhat.com> 002-8
- revert back to dracut-002-5 tarball 845dd502
  lvm2 was reverted to pre-udev

* Wed Sep 23 2009 Harald Hoyer <harald@redhat.com> 002-7
- build with the correct tarball

* Wed Sep 23 2009 Harald Hoyer <harald@redhat.com> 002-6
- add new device mapper udev rules and dmeventd 
  bug 525319, 525015

* Wed Sep 23 2009 Warren Togami <wtogami@redaht.com> 002-5
- Revert back to -3, Add umount back to initrd
  This makes no functional difference to LiveCD.  See Bug #525319

* Mon Sep 21 2009 Warren Togami <wtogami@redhat.com> 002-4
- Fix LiveCD boot regression

* Mon Sep 21 2009 Harald Hoyer <harald@redhat.com> 002-3
- bail out if selinux policy could not be loaded and 
  selinux=0 not specified on kernel command line 
  (bug #524113)
- set finished criteria for dmsquash live images

* Fri Sep 18 2009 Harald Hoyer <harald@redhat.com> 002-2
- do not cleanup dmraids
- copy over lvm.conf

* Thu Sep 17 2009 Harald Hoyer <harald@redhat.com> 002-1
- version 002
- set correct PATH
- workaround for broken mdmon implementation

* Wed Sep 16 2009 Harald Hoyer <harald@redhat.com> 001-12
- removed lvm/mdraid/dmraid lock files
- add missing ifname= files

* Wed Sep 16 2009 Harald Hoyer <harald@redhat.com> 001-11
- generate dracut-version during rpm build time

* Tue Sep 15 2009 Harald Hoyer <harald@redhat.com> 001-10
- add ifname= argument for persistent netdev names
- new /initqueue-finished to check if the main loop can be left
- copy mdadm.conf if --mdadmconf set or mdadmconf in dracut.conf

* Wed Sep 09 2009 Harald Hoyer <harald@redhat.com> 001-9
- added Requires: plymouth-scripts

* Wed Sep 09 2009 Harald Hoyer <harald@redhat.com> 001-8
- plymouth: use plymouth-populate-initrd
- add add_drivers for dracut and dracut.conf
- do not mount /proc and /selinux manually in selinux-load-policy

* Wed Sep 09 2009 Harald Hoyer <harald@redhat.com> 001-7
- add scsi_wait_scan to be sure everything was scanned

* Tue Sep 08 2009 Harald Hoyer <harald@redhat.com> 001-6
- fixed several problems with md raid containers
- fixed selinux policy loading

* Tue Sep 08 2009 Harald Hoyer <harald@redhat.com> 001-5
- patch does not honor file modes, fixed them manually

* Mon Sep 07 2009 Harald Hoyer <harald@redhat.com> 001-4
- fixed mdraid for IMSM

* Mon Sep 07 2009 Harald Hoyer <harald@redhat.com> 001-3
- fixed bug, which prevents installing 61-persistent-storage.rules (bug #520109)

* Thu Sep 03 2009 Harald Hoyer <harald@redhat.com> 001-2
- fixed missing grep for md
- reorder cleanup

* Wed Sep 02 2009 Harald Hoyer <harald@redhat.com> 001-1
- version 001
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Fri Aug 14 2009 Harald Hoyer <harald@redhat.com> 0.9-1
- version 0.9

* Thu Aug 06 2009 Harald Hoyer <harald@redhat.com> 0.8-1
- version 0.8 
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Fri Jul 24 2009 Harald Hoyer <harald@redhat.com> 0.7-1
- version 0.7
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Wed Jul 22 2009 Harald Hoyer <harald@redhat.com> 0.6-1
- version 0.6
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Fri Jul 17 2009 Harald Hoyer <harald@redhat.com> 0.5-1
- version 0.5
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Sat Jul 04 2009 Harald Hoyer <harald@redhat.com> 0.4-1
- version 0.4
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Thu Jul 02 2009 Harald Hoyer <harald@redhat.com> 0.3-1
- version 0.3
- see http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=blob_plain;f=NEWS

* Wed Jul 01 2009 Harald Hoyer <harald@redhat.com> 0.2-1
- version 0.2

* Fri Jun 19 2009 Harald Hoyer <harald@redhat.com> 0.1-1
- first release

* Thu Dec 18 2008 Jeremy Katz <katzj@redhat.com> - 0.0-1
- Initial build
