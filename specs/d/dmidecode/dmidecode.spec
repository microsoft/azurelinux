# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:        Tool to analyse BIOS DMI data
Name:           dmidecode
Version:        3.6
Release: 8%{?dist}
Epoch:          1
License:        GPL-2.0-or-later
Source0:        https://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.xz
URL:            https://www.nongnu.org/dmidecode/
BuildRequires:  gcc make
BuildRequires:  pkgconfig(bash-completion)
ExclusiveArch:  %{ix86} x86_64 ia64 aarch64 riscv64

%if "%{_sbindir}" == "%{_bindir}"
# We rely on filesystem to create the compat symlinks for us
Requires: filesystem(unmerged-sbin-symlinks)
Provides: /usr/sbin/dmidecode
%endif

%description
dmidecode reports information about x86 & ia64 hardware as described in the
system BIOS according to the SMBIOS/DMI standard. This information
typically includes system manufacturer, model name, serial number,
BIOS version, asset tag as well as a lot of other details of varying
level of interest and reliability depending on the manufacturer.

This will often include usage status for the CPU sockets, expansion
slots (e.g. AGP, PCI, ISA) and memory module slots, and the list of
I/O ports (e.g. serial, parallel, USB).

%prep
%autosetup

%build
%make_build CFLAGS="%{optflags}" LDFLAGS="%{__global_ldflags}"

%install
%make_install %{?_smp_mflags} prefix=%{_prefix} sbindir=%{_sbindir} install-bin install-man

%files
%doc AUTHORS NEWS README
%license LICENSE
%{_sbindir}/dmidecode
%ifnarch ia64 aarch64 riscv64
%{_sbindir}/vpddecode
%{_sbindir}/ownership
%{_sbindir}/biosdecode
%{bash_completions_dir}/vpddecode
%{bash_completions_dir}/ownership
%{bash_completions_dir}/biosdecode
%endif
%{_mandir}/man8/*
%{bash_completions_dir}/%{name}

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:3.6-5
- Rebuilt for the bin-sbin merge (2nd attempt)

* Wed Sep 25 2024 David Abdurachmanov <davidlt@rivosinc.com> - 1:3.6-4
- Add riscv64

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:3.6-2
- Rebuilt for the bin-sbin merge

* Sat Jun 01 2024 Jonathan Wright <jonathan@almalinux.org> - 1:3.6-1
- update to 3.6 rhbz#2276863

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 10 2023 Coiby Xu <coxu@redhat.com> - 1:3.5-1
- Update to 3.5

* Thu Aug 10 2023 Coiby Xu <coxu@redhat.com> - 1:3.4-5
- Use SPDX identifiers for license

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 12 2022 Davide Cavalca <dcavalca@fedoraproject.org> 1:3.4-1
- Update to 3.4; Fixes: RHBZ#2101507

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 19 2021 Coiby Xu <coxu@redhat.com> - 1:3.3-1
- updated to upstream v3.3
- Supported SMBIOS spec up to v3.3.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1:3.2-7
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Feb 03 2020 Tom Stellard <tstellar@redhat.com> - 1:3.2-6
- Use make_build macro instead of plain make

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Anton Arapov <aarapov@redhat.com> - 1:3.2-4
- v3.2 patched up to upstream commit 62bce59f

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 18 2018 Anton Arapov <aarapov@redhat.com> - 1:3.2-1
- updated to upstream v3.2
- Supported SMBIOS spec up to v3.2.0

* Thu Aug 02 2018 Anton Arapov <aarapov@redhat.com> - 1:3.1-7
- patched up to upstream commit bd78a5dfd4

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 08 2017 Anton Arapov <aarapov@redhat.com> - 1:3.1-2
- patched up to upstream commit aad65d8a53

* Wed May 24 2017 Anton Arapov <aarapov@redhat.com> - 1:3.1-1
- updated to upstream v3.1
- Supported SMBIOS spec up to v3.1.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Anton Arapov <aarapov@redhat.com> - 1:3.0-7
- patched up to commit adbd050d70b

* Tue Oct 18 2016 Anton Arapov <aarapov@redhat.com> - 1:3.0-6
- patched up to commit df9ebd5ffbe

* Thu Jul 07 2016 Anton Arapov <arapov@gmail.com> - 1:3.0-5
- patched up to commit a50565a65c9

* Wed Jun 29 2016 Anton Arapov <arapov@gmail.com> - 1:3.0-4
- Applied out-a-tree patch from Petr Oros: dmidecode: Unmask LRDIMM in memory type detail

* Mon May 30 2016 Anton Arapov <arapov@gmail.com> - 1:3.0-3
- Hide irrelevant fixup message
- patched up to commit cff11afa886

* Tue Feb 02 2016 Anton Arapov <arapov@gmail.com> - 1:3.0-2
- Use DWORD for Structure table maximum size in SMBIOS3
- patched up to commit ab02b117511

* Thu Jan 21 2016 Anton Arapov <arapov@gmail.com> - 1:3.0-1
- dmidecode v3 patched up to commit e5c73239404

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Oct 25 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1:2.12-8
- dmidecode supported on aarch64

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> 1:2.12-6
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 09 2013 Anton Arapov <anton@redhat.com> - 1:2.12-3
- Accomodate few more necesary, to enable SMBIOS v2.8, changes from upstream.

* Fri Apr 26 2013 Anton Arapov <anton@redhat.com> - 1:2.12-2
- Fixup, so that it actually read SMBIOS 2.8.0 table.

* Wed Apr 17 2013 Anton Arapov <anton@redhat.com> - 1:2.12-1
- Update to upstream 2.12 release.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Anton Arapov <anton@redhat.com> - 1:2.11-8
- Update dmidecode.8 manpage

* Mon Mar 12 2012 Anton Arapov <anton@redhat.com> - 1:2.11-7
- Add "PXE" to HP OEM Type 209 record output
- Properly print the hexadecimal value of invalid string characters

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Anton Arapov <anton@redhat.com> - 1:2.11-5
- Fix the wrong call of the dmi_chassis_type function call. Thus fix
  an issue on the systems with the chassis lock available, application
  doesn't fall out with the out of spec error anymore.

* Tue May 03 2011 Anton Arapov <anton@redhat.com> - 1:2.11-4
- Update to SMBIOS 2.7.1
- Fix the boundaries check in type16

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Anton Arapov <anton@redhat.com> - 1:2.11-2
- Update to upstream 2.11 release. (#623047)

* Wed Jan 19 2011 Anton Arapov <anton@redhat.com> - 1:2.11-1
- Fix the changelog's NVR.

* Mon Nov 08 2010 Prarit Bhargava <prarit@redhat.com> - 1:2.10-3
- updated kernel.spec for review [BZ 225698]

* Fri Oct 15 2010 Anton Arapov <aarapov@redhat.com> - 1:2.10-2
- Does not build with gnu make v3.82+ (#631407)

* Fri Dec 18 2009 Prarit Bhargava <prarit@redhat.com> - 1:2.10-1.40
- Fix rpmlint errors in specfile

* Fri Aug 28 2009 Jarod Wilson <jarod@redhat.com> - 1:2.10-1.39
- Fix cache associativity mapping (was missing some commas)

* Mon Aug 24 2009 Jarod Wilson <jarod@redhat.com> - 1:2.10-1.38
- Add support for newer sockets, processors and pcie slot types

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.10-1.36.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Matthias Clasen <mclasen@redhat.com>
- Build for i586

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.10-1.34.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 09 2009 Prarit Bhargava <prarit@redhat.com> 1:2.10
- rebuild with version 2.10

* Wed Jan 28 2009 Prarit Bhargava <prarit@redhat.com> 1:2.9-1.32
- fix Summary field (BZ 225698)

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:2.9-1.30
- fix license tag

* Fri Mar 14 2008 Doug Chapman <doug.chapman@hp.com> 1:2.9-1.29.1
- Do not package vpddecode, ownership and biosdecode on ia64 since those are x86 only

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:2.9-1.27.1
- Autorebuild for GCC 4.3

* Mon Oct 22 2007 Prarit Bhargava <prarit@redhat.com> - 1:2.9
- rebuild with version 2.9
* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:2.7-1.25.1
- rebuild

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 28 2005 Dave Jones <davej@redhat.com>
- Integrate several specfile cleanups from Robert Scheck. (#172543)

* Sat Sep 24 2005 Dave Jones <davej@redhat.com>
- Revert yesterdays patch, its unneeded in 2.7

* Fri Sep 23 2005 Dave Jones <davej@redhat.com>
- Don't try to modify areas mmap'd read-only.
- Don't build on ia64 any more.
  (It breaks on some boxes very badly, and works on very few).

* Mon Sep 12 2005 Dave Jones <davej@redhat.com>
- Update to upstream 2.7

* Fri Apr 15 2005 Florian La Roche <laroche@redhat.com>
- remove empty scripts

* Wed Mar  2 2005 Dave Jones <davej@redhat.com>
- Update to upstream 2.6

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- Rebuild with -D_FORTIFY_SOURCE=2

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Add missing Obsoletes: kernel-utils

* Mon Jan 10 2005 Dave Jones <davej@redhat.com>
- Update to upstream 2.5 release.

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based upon kernel-utils package.

