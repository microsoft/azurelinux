Vendor:         Microsoft Corporation
Distribution:   Mariner
# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 1

# -*- rpm-spec -*-

# RPM doesn't detect that code in /usr/share is python3, this forces it
# https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build#Python_bytecompilation
%global __python %{__python3}

%bcond_with virtconvert

%global with_guestfs               0
%global default_hvs                "qemu,xen,lxc"


# End local config

Name: virt-manager
Version: 2.2.1
Release: 5%{?dist}
%global verrel %{version}-%{release}

Summary: Desktop tool for managing virtual machines via libvirt
License: GPLv2+
BuildArch: noarch
URL: https://virt-manager.org/
Source0: https://virt-manager.org/download/sources/%{name}/%{name}-%{version}.tar.gz


Requires: virt-manager-common = %{verrel}
Requires: python3-gobject
Requires: gtk3
Requires: libvirt-glib >= 0.0.9
Requires: gtk-vnc2
Requires: spice-gtk3

# We can work with gtksourceview 3 or gtksourceview4, pick the latest one
Requires: gtksourceview4

# virt-manager is one of those apps that people will often install onto
# a headless machine for use over SSH. This means the virt-manager dep
# chain needs to provide everything we need to get a usable app experience.
# Unfortunately nothing in our chain has an explicit dep on some kind
# of usable gsettings backend, so we explicitly depend on dconf so that
# user settings actually persist across app runs.
Requires: dconf

# The vte291 package is actually the latest vte with API version 2.91, while
# the vte3 package is effectively a compat package with API version 2.90.
# virt-manager works fine with either, so pull the latest bits so there's
# no ambiguity.
Requires: vte291

# Weak dependencies for the common virt-manager usecase
Recommends: (libvirt-daemon-kvm or libvirt-daemon-qemu)
Recommends: libvirt-daemon-config-network

# Optional inspection of guests
Suggests: python3-libguestfs

BuildRequires: intltool
BuildRequires: /usr/bin/pod2man
BuildRequires: python3-devel
BuildRequires: perl(Find::File)


%description
Virtual Machine Manager provides a graphical tool for administering virtual
machines for KVM, Xen, and LXC. Start, stop, add or remove virtual devices,
connect to a graphical or serial console, and see resource usage statistics
for existing VMs on local or remote machines. Uses libvirt as the backend
management API.


%package common
Summary: Common files used by the different Virtual Machine Manager interfaces

Requires: python3-argcomplete
Requires: python3-libvirt
Requires: python3-libxml2
Requires: python3-requests
Requires: libosinfo >= 0.2.10
# Required for gobject-introspection infrastructure
Requires: python3-gobject-base
# Required for pulling files from iso media with isoinfo
Requires: genisoimage

%description common
Common files used by the different virt-manager interfaces, as well as
virt-install related tools.


%package -n virt-install
Summary: Utilities for installing virtual machines

Requires: virt-manager-common = %{verrel}
# For 'virsh console'
Requires: libvirt-client

Provides: virt-install
Provides: virt-clone
Provides: virt-xml
%if %{with virtconvert}
Provides: virt-convert
%endif

%description -n virt-install
Package includes several command line utilities, including virt-install
(build and install new VMs) and virt-clone (clone an existing virtual
machine).


%prep
%setup -q


%build
%if %{default_hvs}
%global _default_hvs --default-hvs %{default_hvs}
%endif

./setup.py configure \
    %{?_default_hvs}


%install
./setup.py \
    --no-update-icon-cache --no-compile-schemas \
    install -O1 --root=%{buildroot}
%find_lang %{name}

%if %{without virtconvert}
find %{buildroot} -name virt-convert\* -delete
rm -rf %{buildroot}/%{_datadir}/%{name}/virtconv
%endif

# Replace '#!/usr/bin/env python3' with '#!/usr/bin/python3'
# The format is ideal for upstream, but not a distro. See:
# https://fedoraproject.org/wiki/Features/SystemPythonExecutablesUseSystemPython
for f in $(find %{buildroot} -type f -executable -print); do
    sed -i "1 s|^#!/usr/bin/env python3|#!%{__python3}|" $f || :
done


%files
%license COPYING
%doc README.md NEWS.md
%{_bindir}/%{name}

%{_mandir}/man1/%{name}.1*

%{_datadir}/%{name}/ui/*.ui
%{_datadir}/%{name}/virt-manager
%{_datadir}/%{name}/virtManager

%{_datadir}/%{name}/icons
%{_datadir}/icons/hicolor/*/apps/*

%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/glib-2.0/schemas/org.virt-manager.virt-manager.gschema.xml


%files common -f %{name}.lang
%dir %{_datadir}/%{name}

%if %{with virtconvert}
%{_datadir}/%{name}/virtconv
%endif
%{_datadir}/%{name}/virtinst


%files -n virt-install
%{_mandir}/man1/virt-install.1*
%{_mandir}/man1/virt-clone.1*
%{_mandir}/man1/virt-xml.1*

%{_datadir}/%{name}/virt-install
%{_datadir}/%{name}/virt-clone
%{_datadir}/%{name}/virt-xml

%{_datadir}/bash-completion/completions/virt-install
%{_datadir}/bash-completion/completions/virt-clone
%{_datadir}/bash-completion/completions/virt-xml

%{_bindir}/virt-install
%{_bindir}/virt-clone
%{_bindir}/virt-xml

%if %{with virtconvert}
%{_bindir}/virt-convert
%{_datadir}/bash-completion/completions/virt-convert
%{_datadir}/%{name}/virt-convert
%{_mandir}/man1/virt-convert.1*
%endif


%changelog
* Tue Feb 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.1-5
- Adding BR on "perl(Find::File)".
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.1-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Cole Robinson <crobinso@redhat.com> - 2.2.1-1
- Rebased to version 2.2.1
- CVE-2019-10183: Replace --unattended user-password and admin-password with
  user-password-file and admin-password-file (Fabiano Fidêncio)
- Consistent --memballoon default across non-x86 (Andrea Bolognani)
- virt-install: add --numatune memnode.* (Athina Plaskasoviti)
- Drop hard dep on gtksourceview4, gtksourceview3 is fine as well

* Tue Jun 18 2019 Cole Robinson <crobinso@redhat.com> - 2.2.0-2
- Add missing dep on gtksourceview

* Mon Jun 17 2019 Cole Robinson <crobinso@redhat.com> - 2.2.0-1
- Rebased to version 2.2.0
- libvirt XML viewing and editing UI for new and existing domain, pools,
  volumes, networks
- virt-install: libosinfo --unattended support (Fabiano Fidêncio, Cole
  Robinson)
- Improve CPU model security defaults (Pavel Hrdina)
- virt-install: new --install  option. Ex: virt-install --install fedora29
- virt-install: new --install kernel=,initrd=
- virt-install: --disk, --memory, --name defaults from libosinfo (Fabiano
  Fidêncio, Cole Robinson)
- virt-install: add device suboption aliases which consistently match
  libvirt XML naming
- virt-xml: new --start, --no-define options (Marc Hartmayer)
- virt-install: Add driver_queues argument to --controller (Vasudeva Kamath)
- RISC-V support (Andrea Bolognani)
- Device default improvements for non-x86 KVM (Andrea Bolognani)
- Redesigned 'New Network' wizard
- libguestfs inspection improvements (Pino Toscano)
- virt-install: Add support for xenbus controller (Jim Fehlig)
- cli: Add --disk wwn=,rawio= (Athina Plaskasoviti)
- cli: Add --memballoon autodeflate=,stats.period= (Athina Plaskasoviti)
- cli: Add --iothreads (Athina Plaskasoviti)
- cli: Add --numatune memory.placement (Athina Plaskasoviti)
- cli: Add --launchSecurity option (Erik Skultety)
- cli: Fill in --memorybacking options
- cli: --smartcard: support database= and certificate[0-9]*=
- cli: --sysinfo: Add chasis suboptions
- cli: --metadata: add genid= and genid_enable=
- cli: --vcpus: add vcpus.vcpu[0-9]* config
- cli: fill in all common char source options for --serial, --parellel,
  --console, --channel, --smartcard, --rng, --redirdev

* Wed Apr 03 2019 Cole Robinson <crobinso@redhat.com> - 2.1.0-2
- Fix --initrd-inject with f30 URLs (bz #1686464)

* Sun Feb 03 2019 Cole Robinson <crobinso@redhat.com> - 2.1.0-1
- Rebased to version 2.1.0
- Bash autocompletion support (Lin Ma, Cole Robinson)
- UI and command line --vsock support (Slavomir Kaslev)
- virt-xml: Add --os-variant option (Andrea Bolognani)
- virt-install: use libosinfo cpu, mem, disk size defaults (Fabiano
  Fidencio)
- virt-install: Better usage of libosinfo -unknown distro IDs (Fabiano
  Fidencio)
- virt-install: More usage of libosinfo for ISO --location detection
- virt-install: Add --location LOCATION,kernel=X,initrd=Y for pointing to
  kernel/initrd in media that virt-install/libosinfo fails to detect

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 15 2018 Cole Robinson <crobinso@redhat.com> - 2.0.0-1
- Rebased to version 2.0.0
- Finish port to Python 3
- Improved VM defaults: q35 PCIe, usb3, CPU host-model
- Search based OS selection UI for new VMs
- Track OS name for lifetime of domain in <metadata> XML
- Host interface management UI has been completely removed
- Show domain IP on interface details page

* Fri Sep 07 2018 Cole Robinson <crobinso@redhat.com> - 1.6.0-1.3.3.git3bc7ff24c
- Enable arm32+uefi (bz #1613996)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-0.3.git3bc7ff24c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-0.2.git3bc7ff24c
- Rebuilt for Python 3.7

* Thu Apr 26 2018 Cole Robinson <crobinso@redhat.com> - 1.6.0-0.1.git3bc7ff24c
- Update to latest git snapshot, contains python3 port

* Wed Feb 28 2018 Cole Robinson <crobinso@redhat.com> - 1.5.1-1
- Rebased to version 1.5.1
- Fix disk/net/mem stats graphs

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.5.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Feb 06 2018 Cole Robinson <crobinso@redhat.com> - 1.5.0-1
- Rebased to version 1.5.0
- python3 prep work (Radostin Stoyanov, Cole Robinson, Cédric Bosdonnat)
- Switch --location ISO to use isoinfo (Andrew Wong)
- virt-install: add --cpu numa distance handling (Menno Lageman)
- virt-install: fix --disk for rbd volumes with auth (Rauno Väli)
- virt-install: add --cputune vcpupin handling (Wim ten Have)
- details ui: Showing attached scsi devices per controller (Lin Ma)
- network ui: Show details about SR-IOV VF pool (Lin Ma)
- Greatly expand UI test suite coverage

* Tue Feb 06 2018 Cole Robinson <crobinso@redhat.com> - 1.5.0-1
- Rebased to version 1.5.0
- python3 prep work (Radostin Stoyanov, Cole Robinson, Cédric Bosdonnat)
- Switch --location ISO to use isoinfo (Andrew Wong)
- virt-install: add --cpu numa distance handling (Menno Lageman)
- virt-install: fix --disk for rbd volumes with auth (Rauno Väli)
- virt-install: add --cputune vcpupin handling (Wim ten Have)
- details ui: Showing attached scsi devices per controller (Lin Ma)
- network ui: Show details about SR-IOV VF pool (Lin Ma)
- Greatly expand UI test suite coverage

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.3-3
- Remove obsolete scriptlets

* Tue Nov 21 2017 Cole Robinson <crobinso@redhat.com> - 1.4.3-2
- Fix 'Add Hardware' wizard for non-x86 guests (bz #1505532)

* Tue Sep 19 2017 Cole Robinson <crobinso@redhat.com> - 1.4.3-1
- Rebased to version 1.4.3
- Improve install of debian/ubuntu non-x86 media (Viktor Mihajlovski, Andrew
  Wong)
- New virt-install --graphics listen.* (Pavel Hrdina)
- New virt-install --disk snapshot_policy= (Pavel Hrdina)
- New virt-install --cpu cache.* (Lin Ma)
- Several bug fixes

* Wed Aug 09 2017 Cole Robinson <crobinso@redhat.com> - 1.4.2-1
- Rebased to version 1.4.2
- New VM wixard virt-bootstrap integration (Radostin Stoyanov)
- New VM wizard support for virtuozzo containers (Mikhail Feoktistov)
- network UI: add support to create SR-IOV VF pool (Lin Ma)
- Nicer OS list in New VM wizard (Pino Toscano)
- Better defaults for UEFI secureboot builds (Pavel Hrdina)
- Fix defaults for aarch64 VMs if graphics are requested
- virt-install: new --memdev option (Pavel Hrdina)
- virt-install: add --disk logical/physical_block_size (Yuri Arabadji)
- virt-install: add --features hyperv_reset=, hyperv_synic= (Venkat Datta N
  H)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 22 2017 Cole Robinson <crobinso@redhat.com> - 1.4.1-2
- Fix broken it/ko translations (bz #1433800)

* Mon Mar 13 2017 Cole Robinson <crobinso@redhat.com> - 1.4.1-1
- Rebased to version 1.4.1
- storage/nodedev event API support (Jovanka Gulicoska)
- UI options for enabling spice GL (Marc-André Lureau)
- Add default virtio-rng /dev/urandom for supported guest OS
- Cloning and rename support for UEFI VMs (Pavel Hrdina)
- libguestfs inspection UI improvements (Pino Toscano)
- virt-install: Add --qemu-commandline
- virt-install: Add --network vhostuser (Chen Hanxiao)
- virt-install: Add --sysinfo (Charles Arnold)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Cole Robinson <crobinso@redhat.com> - 1.4.0-5
- Fix version check for spice GL support
- Don't return virtio1.0-net as a valid device name (bz #1399083)
- Fix window size tracking on wayland (bz #1375175)
- Fix 'resize to VM' on wayland (bz #1397598)

* Sun Nov 06 2016 Cole Robinson <crobinso@redhat.com> - 1.4.0-4
- Fix fedora24 installs from incorrectly using virtio-input (bz #1391522)
- Fix error checking extra_args for console argument

* Wed Jun 29 2016 Cole Robinson <crobinso@redhat.com> - 1.4.0-3
- Fix italian translation from breaking the app (bz #1350185)

* Sat Jun 18 2016 Cole Robinson <crobinso@redhat.com> - 1.4.0-2
- Fix executing virt-* scripts (bz #1347938)

* Sat Jun 18 2016 Cole Robinson <crobinso@redhat.com> - 1.4.0-1
- Rebased to version 1.4.0

* Fri May 20 2016 Cole Robinson <crobinso@redhat.com> - 1.3.2-4.20160520git2204de62d9
- Rebase to latest git
- Update translations (bz #1323015)
- Fix rawhide URL installs (bz #1322011)
- Update viewer to work with spice GL

* Thu Mar 17 2016 Cole Robinson <crobinso@redhat.com> - 1.3.2-3
- Fix screenshot on F24 rawhide (bz #1297988)
- Fix URL installs when content-length header missing (bz #1297900)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 24 2015 Cole Robinson <crobinso@redhat.com> - 1.3.2-1
- Rebased to version 1.3.2
- Fix dependency issues with vte (bz #1290262)

* Sun Dec 06 2015 Cole Robinson <crobinso@redhat.com> - 1.3.1-1
- Rebased to version 1.3.1
- Fix command line API on RHEL7 pygobject

* Wed Nov 25 2015 Cole Robinson <crobinso@redhat.com> - 1.3.0-1
- Rebased to version 1.3.0
- Error when trying to modify existing 9p share (bz #1257565)
- virt-manager tries to create vmport device on non-x86 backends (bz #1259998)
- Details/Virtual networks: Allow manually specifying a bridge for
  qemu:///session (bz #1212443)
- [RFE] Improve Solaris 10 x86-64 support in virt-manager (bz #1262093)
- No system tray icon in Cinnamon session (bz #1257949)
- virt-install does not remove orphaned images on failure (bz #1212617)
- virt-manager does not warn if it cannot find the network (bz #1212616)
- Storage volume manager looses focus when a volume is deleted (bz #1279861)
- Storage volume manager does not update free space (bz #1279940)
- Reboot/Shutdown buttons does not work on aarch64 (bz #1212826)

* Tue Aug 11 2015 Cole Robinson <crobinso@redhat.com> - 1.2.1-3
- Fix errors with missing nodedevs (bz #1225771)
- Fix CDROM media change if device is bootable (bz #1229819)
- Fix adding iscsi pools (bz #1231558)
- spec: Add LXC to default connection list (bz #1235972)
- Fix backtrace when reporting OS error (bz #1241902)
- Raise upper limits for lxc ID namespaces (bz #1244490)
- Fix 'copy host CPU definition'
- Fix displaying VM machine type when connecting to old libvirt
- Fix qemu:///session handling in 'Add Connection' dialog
- Fix default storage path for qemu:///session, it should be .local/share/...

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Cole Robinson <crobinso@redhat.com> - 1.2.1-1
- Rebased to version 1.2.1
- Bugfix release
- Fix connecting to older libvirt versions (Michał Kępień)
- Fix connecting to VM console with non-IP hostname (Giuseppe Scrivano)
- Fix addhardware/create wizard errors when a nodedev disappears
- Fix adding a second cdrom via customize dialog

* Mon May 04 2015 Cole Robinson <crobinso@redhat.com> - 1.2.0-1
- Rebased to version 1.2.0

* Mon Apr 13 2015 Cole Robinson <crobinso@redhat.com> - 1.1.0-7.git6dbe19bd8
- Catch ppc64le domaincapabilities errors (bz #1209723)
- Fix missing install options for ppc64le (bz #1209720)
- Allow adding SATA CDROM devices for q35 (bz #1207834)
- Fix crashes with ssh spice connections (bz #1135808)
- Drop incorrect dep on gnome-icon-theme (bz #1207061)

* Fri Mar 27 2015 Cole Robinson <crobinso@redhat.com> - 1.1.0-6.git8ca8490c
- Update to latest git
- Fix new VM disk image names when VM name changes (bz #1169141)
- Fix missing virt-install dep on pygobject (bz #1195794)
- Fix changing VM video type away from qxl (bz #1182710)
- Don't use vmvga for ubuntu VMs on remote centos hosts (bz #1147662)
- Clear vendor field when changing CPU (bz #1190851)
- Drop bogus network domain name validation (bz #1195873)
- Fix Fedora URL examples in virt-install man page (bz #1172818)
- Fix misleading virt-install text after --import install (bz #1180558)

* Sun Feb 22 2015 Cole Robinson <crobinso@redhat.com> - 1.1.0-5.git310f6527
- Fix BuildRequires for f22/rawhide

* Sun Nov 16 2014 Cole Robinson <crobinso@redhat.com> - 1.1.0-4.git310f6527
- Fix crash when rebooting VMs after install (bz #1135546)
- Fix dep on libosinfo (bz #1159370)
- Fix PCI/USB hotplug (bz #1146297)

* Tue Sep 23 2014 Cole Robinson <crobinso@redhat.com> - 1.1.0-3.git310f6527
- Fix defaults for arm and aarch64 VMs

* Mon Sep 22 2014 Cole Robinson <crobinso@redhat.com> - 1.1.0-2.git30db9ece2
- Fix app hanging at connection startup with remote host (bz #1123266)
- Fix several issues creating host bridges (bz #1122743)
- Only use 2 usb redir devs by default to free up USB ports (bz #1135488)
- Create qemu-ga channels for rhel/centos 6/7 VMs (bz #1139109)

* Sun Sep 07 2014 Cole Robinson <crobinso@redhat.com> - 1.1.0-1
- Rebased to version 1.1.0
- Switch to libosinfo as OS metadata database (Giuseppe Scrivano)
- Use libosinfo for OS detection from CDROM media labels (Giuseppe
  Scrivano)
- Use libosinfo for improved OS defaults, like recommended disk size
  (Giuseppe Scrivano)
- virt-image tool has been removed, as previously announced
- Enable Hyper-V enlightenments for Windows VMs
- Revert virtio-console default, back to plain serial console
- Experimental q35 option in new VM 'customize' dialog
- UI for virtual network QoS settings (Giuseppe Scrivano)
- virt-install: --disk discard= support (Jim Minter)
- addhardware: Add spiceport UI (Marc-André Lureau)
- virt-install: --events on_poweroff etc. support (Chen Hanxiao)
- cli --network portgroup= support and UI support
- cli --boot initargs= and UI support
- addhardware: allow setting controller model (Chen Hanxiao)
- virt-install: support setting hugepage options (Chen Hanxiao)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Cole Robinson <crobinso@redhat.com> - 1.0.1-3
- filesystem: Fix target validation when editing device (bz #1089422)
- details: Explicit warn that 'format' doesn't change image format (bz
  #1089457)
- snapshots: Fix screenshot with qxl+spice (bz #1089780)
- Fix using storage when the directory name contains whitespace (bz #1091384)
- packageutils: Fix install when one package is already installed (bz
  #1090181)

* Wed Apr 16 2014 Cole Robinson <crobinso@redhat.com> - 1.0.1-2
- gfxdetails: Show port number for active autoport VM (bz #1081614)
- connection: Hook into domain balloon event (bz #1081424)
- details: Fix showing vcpus values in 'customize' dialog (bz #1083903)
- details: Fix changing graphics type (bz #1083903)
- createpool: Clarify iscsi IQN fields (bz #1084011)
- More fixes for errors on libvirtd disconnect (bz #1069351)

* Sat Mar 22 2014 Cole Robinson <crobinso@redhat.com> - 1.0.1-1
- Rebased to version 1.0.1
- virt-install/virt-xml: New --memorybacking option (Chen Hanxiao)
- virt-install/virt-xml: New --memtune option (Chen Hanxiao)
- virt-manager: UI for LXC <idmap> (Chen Hanxiao)
- virt-manager: gsettings key to disable keygrab (Kjö Hansi Glaz)
- virt-manager: Show domain state reason in the UI (Giuseppe Scrivano)
- Fix a number of bugs found since the 1.0.0 release

* Mon Mar 10 2014 Cole Robinson <crobinso@redhat.com> - 1.0.0-6
- connection: Handle errors when deregistering events on close (bz #1069351)

* Fri Mar 07 2014 Cole Robinson <crobinso@redhat.com> - 1.0.0-5
- addhardware: Fix adding disk through 'customize' dialog (bz #1073808)

* Thu Mar 06 2014 Cole Robinson <crobinso@redhat.com> - 1.0.0-4
- virt-convert: better error if unar is not installed
- details: Fix fallback if fetching CPU models fails (bz #1072704)
- fsdetails: Fix adding a filesystem device (bz #1073067)
- virt-install: Fix --location iso again, and test it (bz #1071513)
- Handle libvirt generating invalid volume XML (bz #1072770)

* Fri Feb 28 2014 Cole Robinson <crobinso@redhat.com> - 1.0.0-3
- Fix creating storage paths if directory is all digits (bz #1069351)
- Properly close connection if tick fails (bz #1069351)
- virt-manager: Handle unrefreshed storage pools (bz #1070883)
- Fix unsetting 'auto resize' console property

* Tue Feb 18 2014 Cole Robinson <crobinso@redhat.com> - 1.0.0-2
- Fix open connection->lxc
- Fix issues creating ppc64 guests
- Fix generating disk targets from customize->addhw

* Fri Feb 14 2014 Cole Robinson <crobinso@redhat.com> - 1.0.0-1
- Rebased to version 1.0.0
- New tool virt-xml: Edit libvirt XML in one shot from the command line
- Improved defaults: qcow2, USB2, host CPU model, guest agent channel
- Introspect command line options like --disk=? or --network=help

* Sun Nov 10 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-5.git1ffcc0cc
- Fix running virt-manager on rawhide (bz #1024569)
- Fix vcpu vs. maxvcpu UI (bz #1016318)
- Fix app startup when run as root (bz #1016435)
- Release serial console when details window is closed (bz #1016445)
- Clarify snapshot VM state UI (bz #1016604)
- Fix adding qemu-guest-agent by default (bz #1016613)
- Fix first run app install (bz #1016825)
- Fix error reporting if initrd fetch fails (bz #1017419)
- Fix error reporting if app is run with no DISPLAY (bz #1021482)
- Fix usage of install media in /home/crobinso (bz #1025355)

* Sun Oct 06 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-4.git79196cdf
- Fix cdrom ordering if added via 'customize' (bz #905439)
- Default to spice/qxl for virt-install (bz #911734)
- Fill in cache and io values for new VMs (bz #967643)
- Add dep on dconf (bz #1012884)

* Tue Sep 24 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-3.gita2e52067
- Sync with git
- Don't try to launch multiple ssh askpass dialogs at once (bz #811346)
- Fix confusion when multiple progress dialogs are run (bz #1003101)
- Fix error adding macvtap nic (bz #1006324)
- Add an appdata file (bz #1011120)
- virt-install: fix nfs:// style URLs (bz #1011177)
- Fix spice with TLS (bz #904295)
- Reduce impact of memory leak (bz #972371)
- Fix parsing rawhide .treeinfo (bz #989162)

* Wed Aug 21 2013 Cole Robinson <crobinso@redhat.com> 0.10.0-2.git948b5359
- Update to git snapshot for ARM support

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 19 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-1
- Rebased to version 0.10.0
- Fix screenshots (bz #969410)
- Add Fedora 19 osdict option (bz #950230)
- Fix loading libguestfs OS icons (bz #905238)
- Make packagekit search cancellable (bz #973777)
- Fix freeze on guest shutdown if serial console connected (bz #967968)

* Mon May 27 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-0.5.gitde1695b2
- Fix default graphics, should be spice+qxl (bz #965864)
- Check for libvirt default network package on first run (bz #950329)
- Fix changing VM cirrus->QXL (bz #928882)

* Wed May 15 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-0.4.gitb68faac8
- Drop bogus packagekit check for avahi-tools (bz #963472)

* Wed May 15 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-0.3.gitb68faac8
- Fix error creating QEMU guests (bz #962569)

* Thu May 09 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-0.2.gitb68faac8
- Fix dep on vte3 (bz #958945)
- Fix dep on virt-manager-common (bz #958730)
- Fix crash when installing from ISO media (bz #958641)
- Fix poor error reporting with unknown CLI option (bz #958730)

* Mon Apr 29 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-0.1.gitd3f9bc8e
- Update to git snapshot for next release

* Mon Apr 01 2013 Cole Robinson <crobinso@redhat.com> - 0.9.5-1
- Rebased to version 0.9.5
- Enable adding virtio-scsi disks (Chen Hanxiao) (bz 887584)
- Support security auto-relabel setting (Martin Kletzander)
- Support disk iotune settings (David Shane Holden)
- Support 'reset' as a reboot option (John Doyle)
- Don't pull in non-native qemu packages on first run (bz 924469)
- Don't create LVM volumes with alloc=0, it doesn't work (bz 872162)
- Fix storage browser hang on KDE (bz 880781)
- Fix package installation on KDE (bz 882024)

* Fri Mar 01 2013 Cole Robinson <crobinso@redhat.com> - 0.9.4-5
- Add explicit dep on pod2man (bz #914562)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Cole Robinson <crobinso@redhat.com> - 0.9.4-4
- Use correct KVM package names on first run (bz #873878)
- network: fix parsing ip blocks with prefix= (bz #872814)
- Don't recommend all of libvirt, just the kvm bits (bz #872246)

* Tue Oct 30 2012 Cole Robinson <crobinso@redhat.com> - 0.9.4-3
- Fix first run packagekit interaction (bz #870851)
- Fix another backtrace if guest is pmsuspended (bz #871237)

* Wed Oct 24 2012 Cole Robinson <crobinso@redhat.com> - 0.9.4-2
- Fix KVM package install on app first run
- Fix listing domain with 'suspended' state (bz #850954)
- Fix 'browse local' behavior when choosing directory (bz #855335)
- Fix libgnome-keyring dep (bz #811921)

* Sun Jul 29 2012 Cole Robinson <crobinso@redhat.com> - 0.9.4-1
- Rebased to version 0.9.4
- Fix VNC keygrab issues (bz 840240)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Cole Robinson <crobinso@redhat.com> - 0.9.3-1
- Rebased to version 0.9.3
- Convert to gtkbuilder: UI can now be editted with modern glade tool
- virt-manager no longer runs on RHEL5, but can manage a remote RHEL5
  host
- Option to configure spapr net and disk devices for pseries (Li Zhang)
- Offer to install openssh-askpass if we need it (bz 754484)
- Don't leave defunct SSH processes around (bz 757892)
- Offer to start libvirtd after install (bz 791152)
- Fix crash when deleting storage volumes (bz 805950)
- Show serial device PTY path again (bz 811760)
- Fix possible crash when rebooting fails (bz 813119)
- Offer to discard state if restore fails (bz 837236)

* Wed Jun 06 2012 Cole Robinson <crobinso@redhat.com> - 0.9.1-4
- Fix connecting to console with specific listen address
- Fix regression that dropped spice dependency (bz 819270)

* Wed Apr 25 2012 Cole Robinson <crobinso@redhat.com> - 0.9.1-3
- Actually make spice the default (bz 757874)
- Only depend on spice on arch it is available (bz 811030)
- Depend on libgnome-keyring (bz 811921)

* Mon Feb 13 2012 Cole Robinson <crobinso@redhat.com> - 0.9.1-2
- Fix error reporting for failed remote connections (bz 787011)
- Fix setting window title when VNC mouse is grabbed (bz 788443)
- Advertise VDI format in disk details (bz 761300)
- Don't let an unavailable host hang the app (bz 766769)
- Don't overwrite existing create dialog when reshowing (bz 754152)
- Improve tooltip for 'force console shortcuts' (bz 788448)

* Wed Feb 01 2012 Cole Robinson <crobinso@redhat.com> - 0.9.1-1
- Rebased to version 0.9.1
- Support for adding usb redirection devices (Marc-André Lureau)
- Option to switch usb controller to support usb2.0 (Marc-André Lureau)
- Option to specify machine type for non-x86 guests (Li Zhang)
- Support for filesystem device type and write policy (Deepak C Shetty)
- Many bug fixes!

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-8
- Fix crashes when deleting a VM (bz 749263)

* Tue Sep 27 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-7
- Fix 'Resize to VM' graphical option (bz 738806)
- Fix deleting guest with managed save data
- Fix error when adding default storage
- Don't flush XML cache on every tick
- Use labels for non-editable network info fields (bz 738751)
- Properly update icon cache (bz 733836)

* Tue Aug 02 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-6
- Fix python-newt_syrup dep

* Mon Aug 01 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-5
- Don't have a hard dep on libguestfs (bz 726364)
- Depend on needed python-newt_syrup version

* Thu Jul 28 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-4
- Fix typo that broke net stats reporting

* Wed Jul 27 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-3
- Add BuildRequires: GConf2 to fix pre scriplet error

* Tue Jul 26 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-2
- Fix virtinst dep

* Tue Jul 26 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-1.fc17
- Rebased to version 0.9.0
- Use a hiding toolbar for fullscreen mode
- Use libguestfs to show guest packagelist and more (Richard W.M. Jones)
- Basic 'New VM' wizard support for LXC guests
- Remote serial console access (with latest libvirt)
- Remote URL guest installs (with latest libvirt)
- Add Hardware: Support <filesystem> devices
- Add Hardware: Support <smartcard> devices (Marc-André Lureau)
- Enable direct interface selection for qemu/kvm (Gerhard Stenzel)
- Allow viewing and changing disk serial number

* Thu Apr 28 2011 Cole Robinson <crobinso@redhat.com> - 0.8.7-5.fc16
- Stop netcf errors from flooding logs (bz 676920)
- Bump default mem for new guests to 1GB so F15 installs work (bz
  700480)

* Tue Apr 19 2011 Cole Robinson <crobinso@redhat.com> - 0.8.7-4.fc16
- Fix spice RPM dependency (bz 697729)

* Thu Apr 07 2011 Cole Robinson <crobinso@redhat.com> - 0.8.7-3.fc16
- Fix broken cs.po which crashed gettext
- Fix offline attach fallback if hotplug fails
- Offer to attach spicevmc if switching to spice

* Thu Mar 31 2011 Cole Robinson <crobinso@redhat.com> - 0.8.7-2.fc16
- Fix using spice as default graphics type
- Fix lockup as non-root (bz 692570)

* Mon Mar 28 2011 Cole Robinson <crobinso@redhat.com> - 0.8.7-1.fc16
- Rebased to version 0.8.7
- Allow renaming an offline VM
- Spice password support (Marc-André Lureau)
- Allow editting NIC <virtualport> settings (Gerhard Stenzel)
- Allow enabling/disabling individual CPU features
- Allow easily changing graphics type between VNC/SPICE for existing VM
- Allow easily changing network source device for existing VM

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Cole Robinson <crobinso@redhat.com> - 0.8.6-1.fc15
- Update to 0.8.6
- SPICE support (requires spice-gtk) (Marc-André Lureau)
- Option to configure CPU model
- Option to configure CPU topology
- Save and migration cancellation (Wen Congyang)
- Save and migration progress reporting
- Option to enable bios boot menu
- Option to configure direct kernel/initrd boot

* Wed Aug 25 2010 Cole Robinson <crobinso@redhat.com> - 0.8.5-1.fc15
- Update to 0.8.5
- Improved save/restore support
- Option to view and change disk cache mode
- Configurable VNC keygrab sequence (Michal Novotny)

* Mon Aug  2 2010 David Malcolm <dmalcolm@redhat.com> - 0.8.4-3.fc15
- fix python 2.7 incompatibility (bz 620216)

* Thu May 27 2010 Cole Robinson <crobinso@redhat.com> - 0.8.4-2.fc14
- Only close connection on specific remote errors
- Fix weird border in manager UI (bz 583728)
- Fix broken icons
- Cancel post-install reboot if VM is forced off
- Fix traceback if customizing a livecd install (bz 583712)
- Add pool refresh button
- Properly autodetect VNC keymap (bz 586201)
- Fix traceback when reconnecting to remote VNC console (bz 588254)
- Fix remote VNC connection with zsh as default shell

* Wed Mar 24 2010 Cole Robinson <crobinso@redhat.com> - 0.8.4-1.fc14
- Update to version 0.8.4
- 'Import' install option, to create a VM around an existing OS image
- Support multiple boot devices and boot order
- Watchdog device support
- Enable setting a human readable VM description.
- Option to manually specifying a bridge name, if bridge isn't detected

* Mon Mar 22 2010 Cole Robinson <crobinso@redhat.com> - 0.8.3-2.fc14
- Fix using a manual 'default' pool (bz 557020)
- Don't force grab focus when app is run (bz 548430)
- Check packagekit for KVM and libvirtd (bz 513494)
- Fake a reboot implementation if libvirt doesn't support it (bz 532216)
- Mark some strings as translatable (bz 572645)

* Mon Feb  8 2010 Cole Robinson <crobinso@redhat.com> - 0.8.3-1.fc13
- Update to 0.8.3 release
- Manage network interfaces: start, stop, view, provision bridges, bonds, etc.
- Option to 'customize VM before install'.

* Tue Jan 12 2010 Cole Robinson <crobinso@redhat.com> - 0.8.2-2.fc13
- Build with actual upstream tarball (not manually built dist)

* Mon Dec 14 2009 Cole Robinson <crobinso@redhat.com> - 0.8.2-1.fc13
- Update to 0.8.2 release
- Fix first virt-manager run on a new install
- Enable floppy media eject/connect

* Wed Dec 09 2009 Cole Robinson <crobinso@redhat.com> - 0.8.1-3.fc13
- Select manager row on right click, regressed with 0.8.1

* Sat Dec  5 2009 Cole Robinson <crobinso@redhat.com> - 0.8.1-2.fc13
- Set proper version Requires: for python-virtinst

* Thu Dec  3 2009 Cole Robinson <crobinso@redhat.com> - 0.8.1-1.fc13
- Update to release 0.8.1
- VM Migration wizard, exposing various migration options
- Enumerate CDROM and bridge devices on remote connections
- Support storage pool source enumeration for LVM, NFS, and SCSI

* Mon Oct 05 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-8.fc13
- Don't allow creating a volume without a name (bz 526111)
- Don't allow volume allocation > capacity (bz 526077)
- Add tooltips for toolbar buttons (bz 524083)

* Mon Oct 05 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-7.fc13
- More translations (bz 493795)

* Tue Sep 29 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-6.fc13
- Fix VCPU hotplug
- Remove access to outdated docs (bz 522823, bz 524805)
- Update VM state text in manager view (bz 526182)
- Update translations (bz 493795)

* Thu Sep 24 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-5.fc12
- Refresh host disk space in create wizard (bz 502777)
- Offer to fix disk permission issues (bz 517379)

* Thu Sep 17 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-4.fc12
- Don't close libvirt connection for non-fatal errors (bz 522168)
- Manager UI tweaks
- Generate better errors if disk/net stats polling fails

* Mon Sep 14 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-3.fc12
- Fix disk XML mangling via connect/eject cdrom (bz 516116)
- Fix delete button sensitivity (bz 518536)
- Fix populating text box from storage browser in 'New VM' (bz 517263)
- Fix a traceback in an 'Add Hardware' error path (bz 517286)

* Thu Aug 13 2009 Daniel P. Berrange <berrange@redhat.com> - 0.8.0-2.fc12
- Remove obsolete dep on policykit agent

* Tue Jul 28 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-1.fc12
- Update to release 0.8.0
- New 'Clone VM' Wizard
- Improved UI, including an overhaul of the main 'manager' view
- System tray icon for easy VM access (start, stop, view console/details)
- Wizard for adding serial, parallel, and video devices to existing VMs.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 21 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.0-5.fc12
- Fix 'opertaing' typo in 'New VM' dialog (#495128)
- Allow details window to resize again (#491683)
- Handle collecting username for vnc authentication (#499589)
- Actually handle arch config when creating a VM (#499145)
- Log libvirt capabilities at startup to aid debugging (#500337)

* Tue Apr 14 2009 Cole Robinson <crobinso@redhat.com> - 0.7.0-4.fc11
- More translation updates

* Thu Apr 09 2009 Cole Robinson <crobinso@redhat.com> - 0.7.0-3.fc11
- Fix incorrect max vcpu setting in New VM wizard (bz 490466)
- Fix some OK/Cancel button ordering issues (bz 490207)
- Use openAuth when duplicating a connection when deleting a VM
- Updated translations (bz 493795)

* Mon Mar 23 2009 Cole Robinson <crobinso@redhat.com> - 0.7.0-2.fc11
- Back compat fixes for connecting to older xen installations (bz 489885)
- Don't show harmless NoneType error when launching new VM details window

* Tue Mar 10 2009 Cole Robinson <crobinso@redhat.com> - 0.7.0-1.fc11
- Update to release 0.7.0
- Redesigned 'New Virtual Machine' wizard
- Option to remove storage when deleting a virtual machine.
- File browser for libvirt storage pools and volumes
- Physical device assignment (PCI, USB) for existing virtual machines.

* Wed Mar  4 2009 Cole Robinson <crobinso@redhat.com> - 0.6.1-4.fc11
- Update polish translation (bz 263301)
- Fix sending ctrl-alt-del to guest
- Fix cpu + mem stats options to remember preference.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  9 2009 Cole Robinson <crobinso@redhat.com> - 0.6.1-2
- Kill off consolehelper (PolicyKit is sufficient)

* Mon Jan 26 2009 Cole Robinson <crobinso@redhat.com> - 0.6.1-1
- Update to 0.6.1 release
- Disk and Network VM stats reporting
- VM Migration support
- Support adding sound devices to existing VMs
- Allow specifying device model when adding a network device to an existing VM

* Tue Jan 20 2009 Mark McLoughlin <markmc@redhat.com> - 0.6.0-7
- Add patch to ignore fix crash on force-poweroff with serial console (#470548)

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.0-6
- Rebuild for Python 2.6

* Mon Dec  1 2008 Cole Robinson <crobinso@redhat.com> - 0.6.0-5.fc10
- Fix spec for building on F9
- Update 'New VM' virt descriptions to be less black and white (bz 470563)

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.0-4
- Rebuild for Python 2.6

* Mon Oct 27 2008 Cole Robinson <crobinso@redhat.com> - 0.6.0-3.fc10
- Add dbus-x11 to Requires (bug 467886)
- Fedora translation updates (bug 467808)
- Don't add multiple sound devices if install fails
- Only popup volume path copy option on right click
- Fix a variable typo

* Tue Oct 14 2008 Cole Robinson <crobinso@redhat.com> - 0.6.0-2.fc10
- Add gnome-python2-gnome requirement.
- Allow seeing connection details if disconnected.
- Updated catalan translation.
- Update dutch translation.
- Update german translation. (bug 438136)
- Fix showing domain console when connecting to hypervisor.
- Update POTFILES to reflect reality (bug 466835)

* Wed Sep 10 2008 Cole Robinson <crobinso@redhat.com> - 0.6.0-1.fc10
- Update to 0.6.0 release
- Add libvirt storage management support
- Basic support for remote guest installation
- Merge VM console and details windows
- Poll avahi for libvirtd advertisement
- Hypervisor autoconnect option
- Add sound emulation when creating new guests

* Thu Apr  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.5.4-3.fc9
- Updated sr, de, fi, it, pl translations

* Thu Mar 13 2008 Daniel P. Berrange <berrange@redhat.com> - 0.5.4-2.fc9
- Don't run policykit checks when root (rhbz #436994)

* Mon Mar 10 2008 Daniel P. Berrange <berrange@redhat.com> - 0.5.4-1.fc9
- Update to 0.5.4 release

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.3-2
- Autorebuild for GCC 4.3

* Thu Jan 10 2008 Daniel P. Berrange <berrange@redhat.com> - 0.5.3-1.fc9
- Update to 0.5.3 release

* Mon Oct 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.5.2-2.fc8
- Change TLS x509 credential name to sync with libvirt

* Thu Oct  4 2007 Daniel P. Berrange <berrange@redhat.com> - 0.5.2-1.fc8
- Update to 0.5.2 release
- No scrollbars for high res guest in low res host (rhbz 273181)
- Unable to remove network device (rhbz 242900)
- Fixed broken menu items (rhbz 307551)
- Require libvirt 0.3.3 to get CDROM change capability for Xen

* Tue Sep 25 2007 Daniel P. Berrange <berrange@redhat.com> - 0.5.1-1.fc8
- Updated to 0.5.1 release
- Open connections in background
- Make VNC connection retries more robust
- Allow changing of CDROM media on the fly
- Add PXE boot installation of HVM guests
- Allow tunnelling VNC over SSH

* Wed Aug 29 2007 Daniel P. Berrange <berrange@redhat.com> - 0.5.0-1.fc8
- Updated to 0.5.0 release
- Support for managing remote hosts
- Switch to use GTK-VNC for the guest console

* Fri Aug 24 2007 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-3.fc8
- Remove ExcludeArch since libvirt is now available

* Wed May  9 2007 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-2.fc7
- Refresh po file translations (bz 238369)
- Fixed removal of disk/network devices
- Fixed toolbar menu option state
- Fixed file dialogs & default widget states

* Mon Apr 16 2007 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-1.fc7
- Support for managing virtual networks
- Ability to attach guest to virtual networks
- Automatically set VNC keymap based on local keymap
- Support for disk & network device addition/removal

* Wed Mar 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.2-3.fc7
- Fix HVM check to allow KVM guests to be created (bz 233644)
- Fix default file size suggestion

* Tue Mar 27 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.2-2.fc7
- Ensure we own all directories we create (bz 233816)

* Tue Mar 20 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.2-1.fc7
- Added online help to all windows
- Bug fixes to virtual console popup, key grab & accelerator override

* Tue Mar 13 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-4.fc7
- Fixed thread locking to avoid deadlocks when a11y is enabled

* Fri Mar  2 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-3.fc7
- Fixed keyboard ungrab in VNC widget

* Tue Feb 20 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-2.fc7
- Only check for HVM on Xen hypervisor

* Tue Feb 20 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-1.fc7
- Added support for managing QEMU domains
- Automatically grab mouse pointer to workaround dual-cursor crazyness

* Wed Jan 31 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.0-2.fc7
- Added dep on desktop-file-utils for post/postun scripts

* Mon Jan 22 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.0-1.fc7
- Added support for managing inactive domains
- Require virt-inst >= 0.100.0 and libvirt >= 0.1.11 for ianctive
  domain management capabilities
- Add progress bars during VM creation stage
- Improved reliability of VNC console
- Updated translations again
- Added destroy option to menu bar to forceably kill a guest
- Visually differentiate allocated memory, from actual used memory on host
- Validate file magic when restoring a guest from a savd file
- Performance work on domain listing
- Allow creation of non-sparse files
- Fix backspace key in serial console

* Tue Dec 19 2006 Daniel P. Berrange <berrange@redhat.com> - 0.2.6-3.fc7
- Imported latest translations from Fedora i18n repository (bz 203783)
- Use 127.0.0.1 address for connecting to VNC console instead of
  localhost to avoid some issue with messed up /etc/hosts.
- Add selector for sparse or non-sparse file, defaulting to non-sparse.
  Add appropriate warnings and progress-bar text. (bz 218996)
- Disable memory ballooning & CPU hotplug for HVM guests (bz 214432)
- Updated memory-setting UI to include a hard upper limit for physical
  host RAM
- Added documentation on the page warning that setting virtual host RAM
  too high can exhaust the memory of the machine
- Handle errors when hostname resolution fails to avoid app exiting (bz 216975)

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.2.6-2.fc7
- rebuild for python 2.5

* Thu Nov  9 2006 Daniel P. Berrange <berrange@redhat.com> - 0.2.6-1.fc7
- Imported translations from Fedora i18n repository
- Make (most) scrollbar policies automatic
- Set busy cursor while creating new VMs
- Preference for controlling keygrab policy
- Preference for when to automatically open console (bz 211385)
- Re-try VNC connection attempt periodically in case VNC daemon
  hasn't finished starting up
- Added activation of URLs for about dialog (bz 210782)
- Improved error reporting when connecting to HV (bz 211229)
- Add command line args to open specific windows
- Don't skip para/full virt wizard step - instead gray out full
  virt option & tell user why
- Change 'physical' to 'logical' when refering to host CPUs
- Include hostname in titlebar
- Disable wizard sensitivity while creating VM

* Thu Oct 19 2006 Daniel P. Berrange <berrange@redhat.com> - 0.2.5-1.fc7
- Switch to use python-virtinst instead of python-xeninst due to 
  renaming of original package
- Disable keyboard accelerators when grabbing mouse to avoid things like
  Ctrl-W closing the local window, instead of remote window bz 210364
- Fix host memory reporting bz 211281
- Remove duplicate application menu entry bz 211230
- Fix duplicated mnemonics (bz 208408)
- Use blktap backed disks if available
- Use a drop down list to remember past URLs (bz 209479)
- Remove unused help button from preferences dialog (bz 209251)
- Fix exception when no VNC graphics is defined
- Force immediate refresh of VMs after creating a new one
- Improve error reporting if run on a kernel without Xen (bz 209122)
- More fixes to avoid stuck modifier keys on focus-out (bz 207949)

* Fri Sep 29 2006 Daniel P. Berrange <berrange@redhat.com> 0.2.3-2.fc6
- Fix segv in sparkline code when no data points are defined (bz  208185)
- Clamp CPU utilization between 0 & 100% just in case (bz 208185)

* Tue Sep 26 2006 Daniel Berrange <berrange@redhat.com> - 0.2.3-1.fc6
- Require xeninst >= 0.93.0 to fix block backed devices
- Skip para/fully-virt step when going back in wizard if not HVM host (bz 207409)
- Fix handling of modifier keys in VNC console so Alt key doesn't get stuck (bz 207949)
- Allow sticky modifier keys by pressing same key 3 times in row (enables Ctrl-Alt-F1
  by doing Ctrl Ctrl Ctrl  Alt-F1)
- Improved error handling during guest creation
- Log errors with python logging, instead of to stdout
- Remove unused buttons from main domain list window
- Switch out of full screen & release key grab when closing console
- Trim sparkline CPU history graph to 40 samples max
- Constraint VCPU adjuster to only allow upto guest's max VCPU count
- Show guest's max & current VCPU count in details page
- Fix rounding of disk sizes to avoid a 1.9 GB disk being rounded down to 1 GB
- Use raw block device path to CDROM not mount point for HVM guest (bz 206965)
- Fix visibility of file size spin box (bz 206186 part 2)
- Check for GTK failing to open X11 display (bz 205938)

* Fri Sep 15 2006 Daniel Berrange <berrange@redhat.com> - 0.2.2-1.fc6
- Fix event handling in create VM wizard (bz 206660 & 206186)
- Fix close button in about dialog (bz 205943)
- Refresh .pot files
- Turn on VNC scrollbars fulltime to avoid GTK window sizing issue
  which consistently resize too small.

* Mon Sep 11 2006 Daniel Berrange <berrange@redhat.com> - 0.2.1-3.fc6
- Added requires on pygtk2-libglade & librsvg2 (bz 205941 & 205942)
- Re-arrange to use console-helper to launch app
- Added 'dist' component to release number

* Wed Sep  6 2006 Jeremy Katz <katzj@redhat.com> - 0.2.1-2
- don't ghost pyo files (#205448)

* Mon Sep  4 2006 Daniel Berrange <berrange@redhat.com> - 0.2.1-1
- Updated to 0.2.1 tar.gz
- Added rules to install/uninstall gconf schemas in preun,post,pre
  scriptlets
- Updated URL for source to reflect new upstream download URL

* Thu Aug 24 2006 Jeremy Katz <katzj@redhat.com> - 0.2.0-3
- BR gettext

* Thu Aug 24 2006 Jeremy Katz <katzj@redhat.com> - 0.2.0-2
- only build on arches with virt

* Tue Aug 22 2006 Daniel Berrange <berrange@redhat.com> - 0.2.0-1
- Added wizard for creating virtual machines
- Added embedded serial console
- Added ability to take screenshots

* Mon Jul 24 2006 Daniel Berrange <berrange@redhat.com> - 0.1.5-2
- Prefix *.pyo files with 'ghost' macro
- Use fully qualified URL in Source  tag

* Thu Jul 20 2006 Daniel Berrange <berrange@redhat.com> - 0.1.5-1
- Update to new 0.1.5 release snapshot

* Thu Jul 20 2006 Daniel Berrange <berrange@redhat.com> - 0.1.4-1
- Update to new 0.1.4 release snapshot

* Mon Jul 17 2006 Daniel Berrange <berrange@redhat.com> - 0.1.3-1
- Fix License tag
- Updated for new release

* Wed Jun 28 2006 Daniel Berrange <berrange@redhat.com> - 0.1.2-3
- Added missing copyright headers on all .py files

* Wed Jun 28 2006 Daniel Berrange <berrange@redhat.com> - 0.1.2-2
- Added python-devel to BuildRequires

* Wed Jun 28 2006 Daniel Berrange <berrange@redhat.com> - 0.1.2-1
- Change URL to public location

* Fri Jun 16 2006 Daniel Berrange <berrange@redhat.com> - 0.1.0-1
- Added initial support for using VNC console

* Thu Apr 20 2006 Daniel Berrange <berrange@redhat.com> - 0.0.2-1
- Added DBus remote control service

* Wed Mar 29 2006 Daniel Berrange <berrange@redhat.com> - 0.0.1-1
- Initial RPM build
