# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# NOTE: This specfile is generated from upstream at https://github.com/rhinstaller/lorax
# NOTE: Please submit changes as a pull request
%define debug_package %{nil}
%global forgeurl https://github.com/weldr/lorax

Name:           lorax
Version:        43.11
Release: 4%{?dist}
Summary:        Tool for creating the anaconda install images
License:        GPL-2.0-or-later

%global tag %{version}
%forgemeta
Url:            %{forgeurl}
Source0:        %{forgesource}

# https://github.com/weldr/lorax/pull/1495
# drop tigervnc to save space, anaconda now uses RDP
Patch:          0001-runtime-install-drop-tigervnc.patch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  make
BuildRequires:  systemd-rpm-macros

Requires:       lorax-templates
%if 0%{?rhel} >= 9
Requires:       lorax-templates-rhel
%endif

Requires:       cpio
Requires:       device-mapper
Requires:       dosfstools
Requires:       e2fsprogs
Requires:       findutils
Requires:       gawk
Requires:       xorriso
Requires:       glib2
Requires:       glibc
Requires:       glibc-common
Requires:       gzip
Requires:       isomd5sum
Requires:       module-init-tools
Requires:       parted
Requires:       squashfs-tools >= 4.2
Requires:       erofs-utils >= 1.8.2
Requires:       util-linux
Requires:       xz-lzma-compat
Requires:       xz
Requires:       pigz
Requires:       pbzip2
Requires:       dracut >= 030
Requires:       kpartx
Requires:       psmisc

# Python modules
Requires:       libselinux-python3
Requires:       python3-mako
Requires:       python3-kickstart >= 3.19
Requires:       python3-libdnf5
Requires:       python3-librepo
Requires:       python3-pycdio

%if 0%{?fedora}
# Fedora specific deps
%ifarch x86_64
Requires:       hfsplus-tools
%endif
%endif

%ifarch x86_64 ppc64le
Requires:       grub2
Requires:       grub2-tools
%endif

%ifarch s390 s390x
Requires:       openssh
Requires:       s390utils >= 2.15.0-2
%endif

# Moved image-minimizer tool to lorax
Provides:       appliance-tools-minimizer = %{version}-%{release}
Obsoletes:      appliance-tools-minimizer < 007.7-3

%description
Lorax is a tool for creating the anaconda install images.

It also includes livemedia-creator which is used to create bootable livemedia,
including live isos and disk images. It can use libvirtd for the install, or
Anaconda's image install feature.

%package docs
Summary: Lorax html documentation
Requires: lorax = %{version}-%{release}

%description docs
Includes the full html documentation for lorax, livemedia-creator, and the pylorax library.

%if ! (0%{?rhel} >= 10 && "%{_arch}" == "ppc64le")
%package lmc-virt
Summary:  livemedia-creator libvirt dependencies
Requires: lorax = %{version}-%{release}
%if 0%{?rhel}
# RHEL doesn't have qemu, just qemu-kvm
Requires: qemu-kvm
%else
Requires: qemu
Recommends: qemu-kvm
%endif

# edk2 builds currently only support these arches
%ifarch x86_64
Requires: edk2-ovmf
%endif
%ifarch aarch64
Requires: edk2-aarch64
%endif

%description lmc-virt
Additional dependencies required by livemedia-creator when using it with qemu.
%endif

%package lmc-novirt
Summary:  livemedia-creator no-virt dependencies
Requires: lorax = %{version}-%{release}
Requires: anaconda-core
Requires: anaconda-tui
Requires: anaconda-install-env-deps
Requires: system-logos
Requires: python3-psutil

%description lmc-novirt
Additional dependencies required by livemedia-creator when using it with --no-virt
to run Anaconda.

%package templates-generic
Summary:  Generic build templates for lorax and livemedia-creator
Requires: lorax = %{version}-%{release}
Provides: lorax-templates = %{version}-%{release}

%description templates-generic
Lorax templates for creating the boot.iso and live isos are placed in
/usr/share/lorax/templates.d/99-generic

%prep
%forgeautosetup -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir} install

%files
%defattr(-,root,root,-)
%license COPYING
%doc AUTHORS
%doc docs/lorax.rst docs/livemedia-creator.rst docs/product-images.rst
%doc docs/*ks
%{python3_sitelib}/pylorax
%{python3_sitelib}/pylorax-%{version}.dist-info
%{_bindir}/lorax
%{_bindir}/mkefiboot
%{_bindir}/livemedia-creator
%{_bindir}/mkksiso
%{_bindir}/image-minimizer
%dir %{_sysconfdir}/lorax
%config(noreplace) %{_sysconfdir}/lorax/lorax.conf
%dir %{_datadir}/lorax
%{_mandir}/man1/lorax.1*
%{_mandir}/man1/livemedia-creator.1*
%{_mandir}/man1/mkksiso.1*
%{_mandir}/man1/image-minimizer.1*
%{_tmpfilesdir}/lorax.conf

%files docs
%doc docs/html/*

%if ! (0%{?rhel} >= 10 && "%{_arch}" == "ppc64le")
%files lmc-virt
%endif

%files lmc-novirt

%files templates-generic
%dir %{_datadir}/lorax/templates.d
%{_datadir}/lorax/templates.d/*

%changelog
* Fri Oct 03 2025 Adam Williamson <awilliam@redhat.com> - 43.11-3
- Backport PR #1495 to drop tigervnc from installer images

* Thu Sep 25 2025 Brian C. Lane <bcl@redhat.com> - 43.11-2
- Pass 43 to CI testing so it uses the correct repository

* Wed Sep 24 2025 Brian C. Lane <bcl@redhat.com> 43.11-1
- runtime-install: skip qcom-accel-firmware (awilliam@redhat.com)

* Thu Aug 14 2025 Brian C. Lane <bcl@redhat.com> 43.10-1
- executils: Remove binary_output flag (bcl@redhat.com)
- logging: Set encoding=UTF-8 on FileHandler (bcl@redhat.com)
- executils: Set encoding to UTF-8 for _run_program (bcl@redhat.com)
- tests: Add template runcmd unicode test (bcl@redhat.com)
- tests: Add some unicode to the executils tests (bcl@redhat.com)
- templates: Remove explicit installation of anaconda-widgets (k.koukiou@gmail.com)

* Tue Jul 22 2025 Brian C. Lane <bcl@redhat.com> 43.9-1
- Makefile: Separate install and all targets (bcl@redhat.com)

* Tue Jul 15 2025 Brian C. Lane <bcl@redhat.com> 43.8-1
- pylilnt: Drop old rules and ignore .tito (bcl@redhat.com)
- tito: Add support for tagging the version in pyproject.toml (bcl@redhat.com)
- lorax.spec: Update for pyproject.toml use (bcl@redhat.com)
- pyproject: Add cmdline scripts (bcl@redhat.com)
- bin: symlink to scripts from src/bin (bcl@redhat.com)
- Move cmdline scripts under pylorax.cmdline (bcl@redhat.com)
- pylorax: Move cmdline into a pylorax.cmdline module (bcl@redhat.com)
- pyproject: Add a pyproject.toml config file (bcl@redhat.com)
- Makefile: Stop running setup.py directly (bcl@redhat.com)

* Fri Jul 11 2025 Brian C. Lane <bcl@redhat.com> 43.7-1
- runtime-cleanup: don't strip avahi-libs (awilliam@redhat.com)
- treebuilder: use fedora-eln-logos for ELN (yselkowi@redhat.com)

* Wed Jul 02 2025 Brian C. Lane <bcl@redhat.com> 43.6-1
- config_files: Do not remove `chcon` in runtime cleanup (ppolawsk@redhat.com)
- use /mnt/sysroot PATH in profile (butirsky@gmail.com)
- fix chroot path in .bash_history (butirsky@gmail.com)

* Mon Jun 16 2025 Brian C. Lane <bcl@redhat.com> 43.5-1
- templates.d: Remove libdir variable from templates (bcl@redhat.com)
- runtime-cleanup: Move rpm database cleanup to the end (bcl@redhat.com)

* Tue May 06 2025 Brian C. Lane <bcl@redhat.com> 43.4-1
- runtime-postinstall: Remove root password (bcl@redhat.com)
  Resolves: rhbz#2364082
- tests: Update magic module usage (bcl@redhat.com)
- utils: Remove old filediff.py script (bcl@redhat.com)
- dnfbase: Use load_repos instead of update_and_load_enabled_repos (bcl@redhat.com)
  Fixes #1464

* Mon Mar 31 2025 Brian C. Lane <bcl@redhat.com> 43.3-1
- config_files: Drop efi suffix from linuxefi and initrdefi in grub2-efi.cfg (bcl@redhat.com)
- runtime-install: only install amd-ucode-firmware on x86_64 (awilliam@redhat.com)
- runtime-install: exclude crust-firmware (awilliam@redhat.com)
- runtime-cleanup: drop more video and audio firmwares (awilliam@redhat.com)
- runtime-install: drop exceptions related to F38-era fw renames (awilliam@redhat.com)
- runtime-postinstall: allow pipewire to run as root (awilliam@redhat.com)

* Tue Mar 25 2025 Brian C. Lane <bcl@redhat.com> 43.2-1
- spec: update lorax-lmc-virt dependencies (yselkowi@redhat.com)
- livemedia-creator: Set 0755 permission on / cpio overlay (bcl@redhat.com)

* Mon Mar 10 2025 Brian C. Lane <bcl@redhat.com> 43.1-1
- runtime-postinstall: Remove systemd-gpt-auto-generator (bcl@redhat.com)

* Thu Mar 06 2025 Brian C. Lane <bcl@redhat.com> 43.0-1
- maint: Switch default platform to F43 (bcl@redhat.com)
- runtime-cleanup: Leave stat binary (bcl@redhat.com)

* Mon Feb 03 2025 Brian C. Lane <bcl@redhat.com> 42.5-1
- Remove sbin usage (bcl@redhat.com)
- mkksiso: Replace existing inst.ks on the iso (bcl@redhat.com)
- Dockerfile.test: Use fedora:latest instead of rawhide (bcl@redhat.com)
- mkksiso: Fix rebuilding the efiboot.img on some systems (bcl@redhat.com)
- Remove leftovers from xorg drop (jkonecny@redhat.com)

* Fri Nov 22 2024 Brian C. Lane <bcl@redhat.com> 42.4-1
- runtime-cleanup: Newer glibc installs into /usr/lib64 (bcl@redhat.com)
- erofs: Change the erofs compression default to zstd (bcl@redhat.com)

* Mon Oct 21 2024 Brian C. Lane <bcl@redhat.com> 42.3-1
- Update template for anaconda webui to start as user (adamkankovsky@gmail.com)
- tests: Fix mkksiso unit test (bcl@redhat.com)

* Tue Oct 08 2024 Brian C. Lane <bcl@redhat.com> 42.2-1
- pylint: Print astroid version (bcl@redhat.com)
- Extend help for --updates and --ks parameters (jkonecny@redhat.com)
- Fix --updates the updates image wasn't loaded (jkonecny@redhat.com)

* Mon Sep 30 2024 Brian C. Lane <bcl@redhat.com> 42.1-1
- templates: Drop dnf install (bcl@redhat.com)

* Mon Sep 09 2024 Brian C. Lane <bcl@redhat.com> 42.0-1
- New lorax documentation - 41.3 (bcl@redhat.com)
- ltmpl: Remove * from docstring (bcl@redhat.com)
- docs: Update intersphinx and add _static dir (bcl@redhat.com)
- docs: Document --rootfs-type options (bcl@redhat.com)
- Adjust Lorax templates for Xorg to Wayland switch (jkonecny@redhat.com)
- creator: Change rootfs description to match cmdline argument (bcl@redhat.com)

* Tue Jul 16 2024 Brian C. Lane <bcl@redhat.com> 41.3-1
- Accept but ignore the old --squashfs-only argument (awilliam@redhat.com)

* Mon Jul 15 2024 Brian C. Lane <bcl@redhat.com> 41.2-1
- Prepare for the sbin merge (zbyszek@in.waw.pl)
- Add compression.erofs section to lorax.conf (bcl@redhat.com)
- Add erofs and erofs-ext4 support to --rootfs-type (bcl@redhat.com)
- Replace squashfs_only with rootfs_type (bcl@redhat.com)
- imgutils: Add mkerofs function and test (bcl@redhat.com)
- Implement --replace also for S390 (sebastian.stark@advantest.com)
- mkksiso: option --replace to replace arbitrary text in boot config.  (sebastian.stark@advantest.com)
- spec: Drop forge tag lua tweak (bcl@redhat.com)

* Wed Jun 12 2024 Brian C. Lane <bcl@redhat.com> 41.1-1
- livemedia-creator: Check for BIOS vs. UEFI qemu support (bcl@redhat.com)
- livemedia-creator: Enable s390x virt support (bcl@redhat.com)
- livemedia-creator: Make use of virtio devices more generic (bcl@redhat.com)
- Makefile: Turn off seccomp for test-in-podman (bcl@redhat.com)
- tests: Fix image_minimizer test dnf usage (bcl@redhat.com)
- creator: Fix pylint error in run_creator (bcl@redhat.com)
- New lorax documentation - 41.1 (bcl@redhat.com)
- docs: Add sphinx-reredirects and composer-cli redirect (bcl@redhat.com)
- New lorax documentation - 41.1 (bcl@redhat.com)
- spec: Switch to using the source from the github tag (bcl@redhat.com)
- workflows: Add missing branch names (bcl@redhat.com)
- runtime-cleanup: wget2-wget has replaced wget (yselkowi@redhat.com)
- Add a simple PR template reminder (bcl@redhat.com)

* Fri Mar 15 2024 Brian C. Lane <bcl@redhat.com>
- maint: Switch default platform to F41 (bcl@redhat.com)
- Add prefixdevname support to the boot.iso (rvykydal@redhat.com)

* Mon Feb 19 2024 Brian C. Lane <bcl@redhat.com>
- Add example use of lmc in github actions. (cjshowalter@alaska.edu)
- Require lorax-templates-rhel when building for ELN, CentOS Stream and RHEL (sgallagh@redhat.com)
- workflows: Switch to actions/checkout@v4 (bcl@redhat.com)
- dnfbase: Fix substitutions (bcl@redhat.com)

* Tue Feb 06 2024 Brian C. Lane <bcl@redhat.com> 40.5-1
- New lorax documentation - 40.5 (bcl@redhat.com)
- maint: Switch default platform to F40 (bcl@redhat.com)
- runtime-cleanup: Update to cleanup more (akira@tagoh.org)
- runtime-install: Update font packages (akira@tagoh.org)

* Thu Feb 01 2024 Brian C. Lane <bcl@redhat.com> 40.4-1
- mkksiso: Add support for adding an anaconda updates.img (jkonecny@redhat.com)
- runtime-install: drop kdump-anaconda-addon (awilliam@redhat.com)
- ltmpl: Handle installing provides with resolve_pkg_spec (bcl@redhat.com)
- s390: Escape volid before using it (bcl@redhat.com)
- aarch64: Escape volid before using it (bcl@redhat.com)
- runtime-install: drop retired pcmciautils (awilliam@redhat.com)
- runtime-install: wget2-wget has replaced wget (awilliam@redhat.com)
- runtime-cleanup: anaconda's new interface needs stdbuf (kkoukiou@redhat.com)
- ltmpl: Pass packages to add_rpm_install as strings (bcl@redhat.com)

* Wed Dec 20 2023 Brian C. Lane <bcl@redhat.com> 40.3-1
- runtime-install: Work around problem with conflicting packages (bcl@redhat.com)
- ltmpl: Check for errors after running the transaction (bcl@redhat.com)

* Tue Dec 12 2023 Brian C. Lane <bcl@redhat.com> 40.2-1
- ltmpl: Remove duplicate package objects from dnf5 results (bcl@redhat.com)
- test-in-podman: Fix problem running in github actions (bcl@redhat.com)

* Mon Dec 11 2023 Brian C. Lane <bcl@redhat.com> 40.1-1
- ltmpl: Filter out other arches, clean up naming (bcl@redhat.com)
- test: Add pigz to test-packages (bcl@redhat.com)
- dnfbase: Fix url substitution support (bcl@redhat.com)
- ltmpl: Add transaction error handling (bcl@redhat.com)
- test-packages: Make sure python3-libdnf5 is installed (bcl@redhat.com)
- Updates for latest libdnf5 changes (bcl@redhat.com)
- spec: Switch to using python3-libdnf5 (bcl@redhat.com)
- Fix writing out debug info for package files and sizes (bcl@redhat.com)
- libdnf5: Switch lorax to use libdnf5 (bcl@redhat.com)
- Add python3-libdnf5 to the list of test packages (bcl@redhat.com)
- Adjust runtime-postinstall.tmpl for systemd config files move (zbyszek@in.waw.pl)

* Mon Oct 02 2023 Brian C. Lane <bcl@redhat.com> 40.0-1
- Remove some unneccessary storage packages from runtime-install (vtrefny@redhat.com)
- Do not install polkit-gnome for blivet-gui (vtrefny@redhat.com)
- docs: Update the quickstart example command (vtrefny@redhat.com)

* Thu Sep 07 2023 Brian C. Lane <bcl@redhat.com> 39.5-1
- Explicitly pull in more filesystem packages (awilliam@redhat.com)
- runtime-postinstall: Turn off lvm monitoring (bcl@redhat.com)
- runtime-cleanup.tmpl: fix typo 'gschadow' (chris.riches@nutanix.com)
- runtime-cleanup: Change how logo pixmaps is cleaned up (bcl@redhat.com)
- runtime-install: only pull in qcom-firmware on aarch64 (awilliam@redhat.com)

* Wed Aug 09 2023 Brian C. Lane <bcl@redhat.com> 39.4-1
- Exclude more obsoleted libertas firmware packages (awilliam@redhat.com)
- Revert "test_minimizer: dnf5 wants --use-host-config" (bcl@redhat.com)

* Mon Aug 07 2023 Brian C. Lane <bcl@redhat.com> 39.3-1
- runtime-install: excluded renamed olpc firmware package (awilliam@redhat.com)

* Fri Jul 14 2023 Brian C. Lane <bcl@redhat.com> 39.2-1
- pylint: Ignore false positive from pylint on rawhide (bcl@redhat.com)
- tests: Fix image_minimizer test dnf usage (bcl@redhat.com)
- tests: Fix HFS test to work with new get_file_magic output (bcl@redhat.com)
- ltmpl: Use ProcMount while running the dnf transaction (bcl@redhat.com)
- imgutils: Split part DracutChroot into ProcMount (bcl@redhat.com)
- runtime-postinstall: Remove libuser.conf (bcl@redhat.com)
- runtime-install: exclude renamed iwl firmware packages (awilliam@redhat.com)
- test_minimizer: dnf5 wants --use-host-config (bcl@redhat.com)
- Install nvme-cli tool and remove machine specific nvme files (bcl@redhat.com)
- Revert "Add blacklist_exceptions to multipath.conf" (jstodola@redhat.com)

* Wed May 31 2023 Brian C. Lane <bcl@redhat.com> 39.1-1
- livemedia-creator: Reorganize the qemu arch patch (bcl@redhat.com)
- Make sure -machine is passed to qemu (hadess@hadess.net)
- Only allow UEFI support to be enabled on x86_64 (hadess@hadess.net)
- Throw an error when KVM is enabled on non-native installs (hadess@hadess.net)
- docs: Clarify that kickstarts need a part command (bcl@redhat.com)
- livemedia-creator: Raise an error when no partitions are in the ks (bcl@redhat.com)
- monitor: Skip repo errors involving CDROM/file source (bcl@redhat.com)
- logging: Remove duplicate stream logging (bcl@redhat.com)
- Pass vga=791 for live basic graphics mode on BIOS (#2176782) (awilliam@redhat.com)
- livemedia-creator: Use -cpu host by default, add -cpu option to override (bcl@redhat.com)

* Tue Mar 14 2023 Brian C. Lane <bcl@redhat.com> 39.0-1
- Add setpriv as ostree containers dependency (#2125655) (jkonecny@redhat.com)
- livemedia-creator: Do not omit plymouth module from dracut (bcl@redhat.com)
- New lorax documentation - 39.0 (bcl@redhat.com)
- workflow: Update list of push branches for workflow tests (bcl@redhat.com)
- Prepare for version 39.0 release (bcl@redhat.com)

* Mon Feb 20 2023 Brian C. Lane <bcl@redhat.com> 38.7-1
- Don't strip gtk4 binaries or libtiff (#2170716) (awilliam@redhat.com)
- image-minimizer: Use RuntimeError instead of Exception (bcl@redhat.com)
- creator: Use RuntimeError instead of Exception (bcl@redhat.com)
- treebuilder: Use RuntimeError instead of Exception (bcl@redhat.com)
- mount: Use RuntimeError instead of Exception (bcl@redhat.com)
- ltmpl: Use RuntimeError instead of Exception (bcl@redhat.com)
- spec: Use autosetup to make patching easier (bcl@redhat.com)
- Revert "templates.d/99-generic/live: Enable automatic persistence for live media" (awilliam@redhat.com)
- Strip some things from gtk4 (awilliam@redhat.com)

* Tue Feb 14 2023 Brian C. Lane <bcl@redhat.com> 38.6-1
- templates.d/99-generic/live: Enable automatic persistence for live media (ngompa@fedoraproject.org)
- Update for Noto CJK Variable Fonts (pwu@redhat.com)

* Wed Feb 08 2023 Brian C. Lane <bcl@redhat.com> 38.5-1
- Fix using --dracut-conf with DracutChroot (bcl@redhat.com)
- tests: Fix DataHolder for CreatorTest (bcl@redhat.com)
- runtime-install: Update for
  https://fedoraproject.org/wiki/Changes/NotoFontsForMoreLang (akira@tagoh.org)
- SPDX migration (bcl@redhat.com)
- rsyslogd.conf: Rewrite using current config syntax (bcl@redhat.com)
- Add comment for squashfs-only (dick@mrns.nl)
- runtime-install: exclude some more unneeded firmware packages (awilliam@redhat.com)
- runtime-install: stop excluding bfa-firmware again (retired) (awilliam@redhat.com)

* Mon Dec 12 2022 Brian C. Lane <bcl@redhat.com> 38.4-1
- runtime-cleanup: drop old versions of qed firmware (awilliam@redhat.com)
- runtime-cleanup: drop Mediatek SoC firmwares (awilliam@redhat.com)
- runtime-install: drop bfa-firmware (awilliam@redhat.com)
- mkksiso: Disable running mkefiboot in container tests (bcl@redhat.com)
- mkksiso: Rebuild efiboot.img for UEFI enabled isos (bcl@redhat.com)
- gitleaks: Add config file to ignore known fake secrets (bcl@redhat.com)
- fedora-livemedia.ks: Use livesys-scripts (bcl@redhat.com)
- workflows: Switch to actions/checkout@v3 (bcl@redhat.com)

* Mon Nov 28 2022 Brian C. Lane <bcl@redhat.com> 38.3-1
- Use unicode.pf2 from /usr/share/grub/ (bcl@redhat.com)
- On ppc64le Use core.elf from grub2 package (bcl@redhat.com)

* Wed Nov 09 2022 Brian C. Lane <bcl@redhat.com> 38.2-1
- runtime-postinstall: Disable sshd.socket (bcl@redhat.com)
- docs: Document mock and SELinux not working together (bcl@redhat.com)
- imgutils: Don't delete dirs created for DracutChroot (bcl@redhat.com)
- tito: Use .tito instead of old ./rel-eng directory (bcl@redhat.com)
- setup.py: Set the version number (bcl@redhat.com)
- Improvement of unmounting /proc, /dev and binds (soksanichenko@cloudlinux.com)

* Tue Oct 11 2022 Brian C. Lane <bcl@redhat.com> 38.1-1
- livemedia-creator: Allow file: url without networking (bcl@redhat.com)
- Update kdump addon package name (vslavik@redhat.com)
- Drop anaconda auditd replacement (vslavik@redhat.com)

* Fri Sep 30 2022 Brian C. Lane <bcl@redhat.com> 38.0-1
- New lorax documentation - 38.0 (bcl@redhat.com)
- tests: Update test_creator.py for new cmdline options (bcl@redhat.com)
- livemedia-creator: Add release, variant, bugurl, and isfinal cmdline flags (cappy@cappuchino.xyz)
- Drop 32-bit ARM and x86 support (awilliam@redhat.com)
- Update anaconda's crash messages to watch (vslavik@redhat.com)
- livemedia-creator: Add --product to cmdline args (bcl@redhat.com)
- fedora-livemedia: Make sure GNOME Software service isn't started (bcl@redhat.com)
- fonts packages syncup in template files (akira@tagoh.org)
- tests: Add tzdata package to minimizer test setup (bcl@redhat.com)

* Mon Jul 25 2022 Brian C. Lane <bcl@redhat.com> 37.8-1
- mkksiso: Optionally support 3 arguments or --ks (bcl@redhat.com)
- mkksiso: Add -U to xorriso on ppc64le (bcl@redhat.com)
- mkksiso: Fix passing -iso-level to xorriso (bcl@redhat.com)
- pylorax: SafeConfigParser is now ConfigParser (bcl@redhat.com)
- test: Update test code for new pylint version (bcl@redhat.com)
- tests: Switch back to rawhide for tests (bcl@redhat.com)
- workflow: Remove sudo from workflow (bcl@redhat.com)

* Wed Jul 13 2022 Brian C. Lane <bcl@redhat.com> 37.7-1
- mkksiso: Set u+rw permission on extracted files and directories (bcl@redhat.com)
- Add option to boot local drive to the x86 BIOS grub2 menu (bcl@redhat.com)

* Tue Jun 28 2022 Brian C. Lane <bcl@redhat.com> 37.6-1
- tests: Use Fedora 36 for test-in-podman (bcl@redhat.com)
- Add include for architecture specific packages to example kickstarts (bcl@redhat.com)
- templates: adjust for mellanox firmware split to subpackage (awilliam@redhat.com)
- mkksiso: Fix s390x support (bcl@redhat.com)
- spec: Don't require grub2 on x86-32 (bcl@redhat.com)
- mkksiso: Remove use of os.path.join (bcl@redhat.com)
- Makefile: Add mkksiso and image-minimizer to coverage report (bcl@redhat.com)
- tests: Add tests for mkksiso (bcl@redhat.com)
- mkksiso: Add kernel cmdline customization support (bcl@redhat.com)
- mkksiso: Move kickstart to --ks KICKSTART (bcl@redhat.com)
- mkksiso: Add helper functions for kernel cmdline modifications (bcl@redhat.com)

* Fri Jun 03 2022 Brian C. Lane <bcl@redhat.com> 37.5-1
- example ks: Drop syslinux and add grub2-tools package for livemedia (bcl@redhat.com)
- templates: Set @ISOLABEL@ in the bios-grub.cfg file to the isolabel (bcl@redhat.com)
- Update spec for syslinux->grub2 switch (awilliam@redhat.com)

* Wed Jun 01 2022 Brian C. Lane <bcl@redhat.com> 37.4-1
- mkksiso: Fix grub2 editing error (bcl@redhat.com)

* Wed Jun 01 2022 Brian C. Lane <bcl@redhat.com> 37.3-1
- Add grub2 BIOS boot support to live iso template (bcl@redhat.com)
  Resolves: rhbz#2092065
- Drop grafting variables (bcl@redhat.com)
- Drop macboot.img and simplify efiboot.img use (bcl@redhat.com)
- Add grub2 BIOS boot support (bcl@redhat.com)
- Remove syslinux support (bcl@redhat.com)

* Mon May 23 2022 Brian C. Lane <bcl@redhat.com> 37.2-1
- cleanup: drop phanfw.bin from linux-firmware (awilliam@redhat.com)
- cleanup: strip more mellanox firmware files (awilliam@redhat.com)
- cleanup: strip qcom/vpu* from linux-firmware (awilliam@redhat.com)
- cleanup: drop qcom/apq8096 firmwares (awilliam@redhat.com)

* Wed May 11 2022 Brian C. Lane <bcl@redhat.com> 37.1-1
- New lorax documentation - 37.1 (bcl@redhat.com)
- docs: Update the mkksiso documentation (bcl@redhat.com)
- setup.py: Install mkksiso to /usr/bin (bcl@redhat.com)
- pylorax: Move variable out of try block (bcl@redhat.com)
- setup.py: Use setup from setuptools not distutils (bcl@redhat.com)
- Makefile: Remove -it options for test-in-podman (bcl@redhat.com)
- mkksiso: Rewrite to use xorriso features (bcl@redhat.com)
- docs: Fix typo in index.html (bcl@redhat.com)

* Mon Mar 28 2022 Brian C. Lane <bcl@redhat.com> 37.0-1
- New lorax documentation - 37.0 (bcl@redhat.com)
- runtime-cleanup: keep 'unshare' binary present from util-linux-core (kkoukiou@redhat.com)

* Mon Feb 28 2022 Brian C. Lane <bcl@redhat.com> 36.9-1
- Don't move the restart-anaconda file (vponcova@redhat.com)

* Wed Feb 16 2022 Brian C. Lane <bcl@redhat.com> 36.8-1
- runtime-cleanup: Remove ncurses package (bcl@redhat.com)

* Mon Feb 14 2022 Brian C. Lane <bcl@redhat.com> 36.7-1
- postinstall: Restore reproducible build timestamps on /usr/share/fonts (bcl@redhat.com)
- tests: Fix the image minimizer test dnf usage (bcl@redhat.com)
- runtime-cleanup: drop kernel drivers/iio (awilliam@redhat.com)
- runtime-cleanup: drop gallium-pipe drivers from mesa-dri-drivers (awilliam@redhat.com)
- runtime-cleanup: drop yelp's local MathJax library copy (awilliam@redhat.com)
- runtime-cleanup: drop eapol_test from wpa_supplicant (awilliam@redhat.com)
- runtime-cleanup: drop /usr/bin/cyrusbdb2current (awilliam@redhat.com)
- runtime-cleanup: drop systemd-analyze (awilliam@redhat.com)
- runtime-cleanup: drop mtools and glibc-gconv-extra (awilliam@redhat.com)
- runtime-cleanup: drop guile22's ccache (awilliam@redhat.com)
- runtime-cleanup: fix warnings from old or changed packages (awilliam@redhat.com)
- runtime-cleanup: drop Italic from google-noto-sans-vf-fonts (awilliam@redhat.com)
- runtime-install: drop some unnecessary font packages (awilliam@redhat.com)

* Fri Feb 04 2022 Brian C. Lane <bcl@redhat.com> 36.6-1
- mkksiso: Fix check for unsupported arch error (bcl@redhat.com)

* Thu Feb 03 2022 Brian C. Lane <bcl@redhat.com> 36.5-1
- mkksiso: Improve debug message about unsupported arch (bcl@redhat.com)
- mkksiso: Fix the order of the ppc mkisofs command (bcl@redhat.com)
- mkksiso: mkfsiso argument order matters (bcl@redhat.com)
- mkksiso: Add kickstart to s390x cdboot.prm (bcl@redhat.com)
- cleanup: handle RPM database move to /usr (awilliam@redhat.com)
- Install the variable font of the Cantarell font (akira@tagoh.org)
- Update the template for f36 Change proposal:
  https://fedoraproject.org/wiki/Changes/DefaultToNotoFonts (akira@tagoh.org)
- Update Malayalam font to its new renamed package name rit-meera-new-fonts (pnemade@fedoraproject.org)
- Enable sftp when using inst.sshd (bcl@redhat.com)
- Add inst.rngd cmdline option (bcl@redhat.com)
- docs: Update docs for image-minimizer (bcl@redhat.com)
- tests: Add tests for image-minimizer (bcl@redhat.com)
- image-minimizer: Check for missing root directory (bcl@redhat.com)
- image-minimizer: Fix utf8 error and add docs (bcl@redhat.com)

* Tue Dec 14 2021 Brian C. Lane <bcl@redhat.com> 36.4-1
- cleanup: remove binaries from lilv (awilliam@redhat.com)
- runtime-cleanup: remove pipewire-related packages (awilliam@redhat.com)
- New lorax documentation - 36.3 (bcl@redhat.com)

* Thu Dec 09 2021 Brian C. Lane <bcl@redhat.com> 36.3-1
- mkksiso: Check the length of the filenames (bcl@redhat.com)
- mkksiso: Check the iso's arch against the host's (bcl@redhat.com)
- mkksiso: Add missing implantisomd5 tool requirements (bcl@redhat.com)
- mkksiso: Raise error if no volume id is found (bcl@redhat.com)
- mount: Add s390x support to IsoMountopoint (bcl@redhat.com)
- mkksiso: Skip mkefiboot for non-UEFI isos (bcl@redhat.com)
- mkksiso: Add -joliet-long (bcl@redhat.com)
- mkksiso: Return 1 on errors (bcl@redhat.com)
- Fix monitor problem with split UTF8 characters (bcl@redhat.com)

* Wed Nov 10 2021 Brian C. Lane <bcl@redhat.com> 36.2-1
- Remove memtest86+ from example kickstarts (bcl@redhat.com)
- fedora-livemedia: Update example kickstart (bcl@redhat.com)
- mount: Switch to using pycdio instead of pycdlib (bcl@redhat.com)
- Move default releasever into pylorax DEFAULT_RELEASEVER (bcl@redhat.com)
- runtime-postinstall: Drop raidstart/stop stub code (bcl@redhat.com)
- runtime-install: Fix grub2 epoch, it is 1 not 0 (bcl@redhat.com)
- Update runtime-install/cleanup for Marvell Prestera fw split (awilliam@redhat.com)

* Thu Oct 28 2021 Brian C. Lane <bcl@redhat.com> 36.1-1
- dnfbase: Handle defaults better (bcl@redhat.com)
- ltmpl: Add version compare support to installpkg (bcl@redhat.com)

* Mon Oct 11 2021 Brian C. Lane <bcl@redhat.com> 36.0-1
- New lorax documentation - 36.0 (bcl@redhat.com)
- docs: Remove logging command from examples (bcl@redhat.com)
- runtime-install: exclude liquidio and netronome firmwares (awilliam@redhat.com)
- runtime-cleanup: drop Marvell Prestera firmware files (awilliam@redhat.com)
- runtime-cleanup: drop some Qualcomm smartphone firmwares (awilliam@redhat.com)
- Fix pylint warnings about string formatting (bcl@redhat.com)
- tests: Ignore new pylint warnings (bcl@redhat.com)
- Add fstrim to disk and filesystem image creation (bcl@redhat.com)

* Tue Sep 07 2021 Brian C. Lane <bcl@redhat.com> 35.7-1
- templates: Remove memtest86+ (bcl@redhat.com)

* Thu Jul 08 2021 Brian C. Lane <bcl@redhat.com> 35.6-1
- Install unicode.pf2 from new directory (bcl@redhat.com)
- Makefile: Use sudo to fix ownership of docs (bcl@redhat.com)
- Makefile: Make sure container is built before docs (bcl@redhat.com)
- Makefile: Add local-srpm target to create a .src.rpm from HEAD (bcl@redhat.com)
- mkksiso: cmdline should default to empty string (bcl@redhat.com)
- runtime-install: Remove gfs2-utils (bcl@redhat.com)
- mount.py: Fix docstring (jkucera@redhat.com)

* Fri Jun 11 2021 Brian C. Lane <bcl@redhat.com> 35.5-1
- pylorax: Fix mksparse ftruncate size handling (bcl@redhat.com)

* Thu Jun 10 2021 Brian C. Lane <bcl@redhat.com> 35.4-1
- livemedia-creator: Check for mkfs.hfsplus (bcl@redhat.com)
- Drop retired icfg (zbyszek@in.waw.pl)

* Tue May 25 2021 Brian C. Lane <bcl@redhat.com> 35.3-1
- Add a context manager for dracut (bcl@redhat.com)
  Resolves: rhbz#1962975
- Remove unneeded aajohan-comfortaa-fonts (bcl@redhat.com)

* Wed May 05 2021 Brian C. Lane <bcl@redhat.com> 35.2-1
- runtime-cleanup: Use branding package name instead of product.name (bcl@redhat.com)
- treebuilder: Add branding package to template variables (bcl@redhat.com)
- livemedia-creator: Use inst.ks on cmdline for virt (bcl@redhat.com)
- docs: Remove composer-cli.1 (bcl@redhat.com)

* Mon Apr 26 2021 Brian C. Lane <bcl@redhat.com> 35.1-1
- New lorax documentation - 35.1 (bcl@redhat.com)
- Makefile: Use podman as a user for testing and docs (bcl@redhat.com)
- composer-cli: Remove all traces of composer-cli (bcl@redhat.com)
- livemedia-creator: Add rhgb to live iso cmdline (#1943312) (bcl@redhat.com)
- tests: Fix pocketlint use of removed pylint messages (bcl@redhat.com)
- Disable X11 forwarding from installation environment. (vslavik@redhat.com)
- Remove display-related packages (vslavik@redhat.com)
- Drop trying to install reiserfs-utils (kevin@scrye.com)
- test: Fix URL to bots testmap (martin@piware.de)
- Change khmeros-base-fonts to khmer-os-system-fonts. (pnemade@fedoraproject.org)
- Fix output path in docs (vslavik@redhat.com)
- runtime-cleanup: don't wipe /usr/bin/report-cli (#1937550) (awilliam@redhat.com)
- xorg-x11-font-utils is now four packages, remove all of them (peter.hutterer@who-t.net)
- xorg-x11-server-utils was split up in Fedora 34, so adjust templates (kevin@scrye.com)
* Wed Mar 03 2021 Brian C. Lane <bcl@redhat.com> 35.0-1
- New lorax documentation - 35.0 (bcl@redhat.com)
- Makefile: Add test-in-podman and docs-in-podman build targets (bcl@redhat.com)
- isolinux.cfg: Rename the 'vesa' menu entry to 'basic' (bcl@redhat.com)
- composer-cli: Add support for start-ostree --url URL (bcl@redhat.com)

* Wed Mar 03 2021 Brian C. Lane <bcl@redhat.com>
- New lorax documentation - 35.0 (bcl@redhat.com)
- Makefile: Add test-in-podman and docs-in-podman build targets (bcl@redhat.com)
- isolinux.cfg: Rename the 'vesa' menu entry to 'basic' (bcl@redhat.com)
- composer-cli: Add support for start-ostree --url URL (bcl@redhat.com)
