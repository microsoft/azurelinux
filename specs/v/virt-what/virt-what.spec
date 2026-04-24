# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           virt-what
Version:        1.27
Release: 5%{?dist}
Summary:        Detect if we are running in a virtual machine
License:        GPL-2.0-or-later

URL:            http://people.redhat.com/~rjones/virt-what/
Source0:        http://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz
Source1:        http://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz.sig

# Keyring used to verify tarball signature.
Source2:       libguestfs.keyring

# Maintainer script which helps with handling patches.
Source3:        copy-patches.sh

# Add detection of systemd-nspawn (upstream)
Patch:          0001-virt-what-detect-systemd-nspawn.patch
# Add detection of WSL2 (upstream)
Patch:          0002-Add-support-for-WSL2.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  git
BuildRequires:  autoconf, automake, libtool
BuildRequires:  /usr/bin/pod2man

# Required to verify tarball signature.
BuildRequires: gnupg2

# Required at build time in order to do 'make check' (for getopt).
BuildRequires:  util-linux

# virt-what script uses dmidecode and getopt (from util-linux).
# RPM cannot detect this so make the dependencies explicit here.
%ifarch aarch64 %{ix86} x86_64
Requires:       dmidecode
%endif
Requires:       util-linux

# Runs the 'which' program to find the helper.
Requires:       which


%description
virt-what is a shell script which can be used to detect if the program
is running in a virtual machine.

The program prints out a list of "facts" about the virtual machine,
derived from heuristics.  One fact is printed per line.

If nothing is printed and the script exits with code 0 (no error),
then it can mean either that the program is running on bare-metal or
the program is running inside a type of virtual machine which we don't
know about or can't detect.

Current types of virtualization detected:

 - alibaba_cloud      Alibaba cloud
 - alibaba_cloud-ebm
 - aws                Amazon Web Services
 - bhyve              FreeBSD hypervisor
 - docker             Docker container
 - google_cloud       Google cloud
 - hyperv             Microsoft Hyper-V
 - ibm_power-kvm      IBM POWER KVM
 - ibm_power-lpar_shared IBM POWER LPAR (hardware partition)
 - ibm_power-lpar_dedicated
 - ibm_systemz-*      IBM SystemZ Direct / LPAR / z/VM / KVM
 - illumos-lx         Illumos with Linux syscall emulation
 - ldoms              Oracle VM Server for SPARC Logical Domains
 - linux_vserver      Linux VServer container
 - lxc                Linux LXC container
 - kvm                Linux Kernel Virtual Machine (KVM)
 - lkvm               LKVM / kvmtool
 - nutanix_ahv        Nutanix Acropolis Hypervisor (AHV)
 - openvz             OpenVZ or Virtuozzo
 - ovirt              oVirt node
 - parallels          Parallels Virtual Platform
 - podman             Podman container
 - powervm_lx86       IBM PowerVM Lx86 Linux/x86 emulator
 - qemu               QEMU (unaccelerated)
 - redhat             Red Hat hypervisor
 - rhev               Red Hat Enterprise Virtualization
 - uml                User-Mode Linux (UML)
 - virtage            Hitachi Virtualization Manager (HVM) Virtage LPAR
 - virtualbox         VirtualBox
 - virtualpc          Microsoft VirtualPC
 - vmm                vmm OpenBSD hypervisor
 - vmware             VMware
 - xen                Xen
 - xen-dom0           Xen dom0 (privileged domain)
 - xen-domU           Xen domU (paravirtualized guest domain)
 - xen-hvm            Xen guest fully virtualized (HVM)


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -S git

# Always rebuild upstream autotools files.
autoreconf -i


%build
%configure || { cat config.log; exit 1; }
make


%install
%make_install


%check
if ! make -k check ; then
    find -name test-suite.log -exec cat {} \;
    exit 1
fi

%files
%doc README COPYING
%{_sbindir}/virt-what
%{_sbindir}/virt-what-cvm
%{_libexecdir}/virt-what-cpuid-helper
%{_mandir}/man1/*.1*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 06 2025 Richard W.M. Jones <rjones@redhat.com> - 1.27-3
- Add support for systemd-nspawn and WSL2

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Aug 31 2024 Richard W.M. Jones <rjones@redhat.com> - 1.27-1
- New upstream version 1.27

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Richard W.M. Jones <rjones@redhat.com> - 1.26-1
- New upstream version 1.26
- Add new binary virt-what-cvm (for confidential VMs).

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.25-3
- Migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 17 2022 Richard W.M. Jones <rjones@redhat.com> - 1.25-1
- New upstream version 1.25

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 23 2022 Richard W.M. Jones <rjones@redhat.com> - 1.24-1
- New upstream version 1.24
- Update list of supported hypervisors
- Fix %%check for failures

* Thu Apr 14 2022 Richard W.M. Jones <rjones@redhat.com> - 1.22-2
- New upstream version 1.22.
- Fix Source0 line.

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 19 2021 Richard W.M. Jones <rjones@redhat.com> - 1.21-1
- New upstream version 1.21.

* Tue Apr 13 2021 Richard W.M. Jones <rjones@redhat.com> - 1.21-0.1
- Add all patches since 1.20 in preparation for 1.21 release.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 1.20-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct  3 2019 Richard W.M. Jones <rjones@redhat.com> - 1.20-1
- New upstream version 1.20.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 31 2018 Richard W.M. Jones <rjones@redhat.com> - 1.19-1
- New upstream version 1.19.
- Fixes support for AWS.
- Remove patches which are now upstream.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 17 2017 Richard W.M. Jones <rjones@redhat.com> - 1.18-4
- Include upstream patches since 1.18 was released.
- dmidecode is also available on aarch64.

* Mon Jul 31 2017 Richard W.M. Jones <rjones@redhat.com> - 1.18-1
- New upstream version 1.18.
- Update RPM description section with complete list of supported guests.
- If ‘make check’ fails, dump ‘test-suite.log’.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 14 2016 Richard W.M. Jones <rjones@redhat.com> - 1.15-4
- Require 'which' program.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 21 2015 Richard W.M. Jones <rjones@redhat.com> - 1.15-1
- New upstream version 1.15.
- Remove patches, now upstream.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 28 2013 Richard W.M. Jones <rjones@redhat.com> - 1.13-3
- Suppress warning message on Amazon EC2:
  "grep: /proc/xen/capabilities: No such file or directory"

* Wed Sep 11 2013 Richard W.M. Jones <rjones@redhat.com> - 1.13-2
- Include two upstream patches for detecting Xen and Linux VServer better
  (RHBZ#973663).
- Modernize the spec file.

* Mon Jul 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1.13-1
- New upstream version 1.13.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1.12-1
- New upstream version 1.12.

* Wed Feb 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.11-3
- Remove ExclusiveArch, but don't require dmidecode except on
  i?86 and x86-64 (RHBZ#791370).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 27 2011 Richard W.M. Jones <rjones@redhat.com> - 1.11-1
- New upstream version 1.11.

* Wed May 25 2011 Richard W.M. Jones <rjones@redhat.com> - 1.10-1
- New upstream version 1.10.

* Tue Mar  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1.9-1
- New upstream version 1.9.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Richard W.M. Jones <rjones@redhat.com> - 1.8-1
- New upstream version 1.8.

* Thu Jan 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1.7-1
- New upstream version 1.7.

* Wed Jan 19 2011 Richard W.M. Jones <rjones@redhat.com> - 1.6-2
- New upstream version 1.6.
- BuildRequires 'getopt' from util-linux-ng.

* Tue Jan 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1.5-1
- New upstream version 1.5.
- Add 'make check' section.

* Tue Jan 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1.4-1
- New upstream version 1.4.
- More hypervisor types detected.

* Thu Oct 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-4
- Move configure into build (not prep).

* Thu Oct 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-3
- Initial import into Fedora.

* Tue Oct 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-2
- Make changes suggested by reviewer (RHBZ#644259).

* Tue Oct 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-1
- Initial release.
