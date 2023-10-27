Summary:        Development Libraries and headers for EFI
Name:           gnu-efi
Version:        3.0.17
Release:        1%{?dist}
License:        BSD
URL:            https://sourceforge.net/projects/gnu-efi
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source:         https://sourceforge.net/projects/%{name}/files/%{name}-%{version}.tar.bz2
Source1:        LICENSE.PTR

BuildRequires: gcc
BuildRequires: glibc-devel

%define lib %{nil}lib%{nil}

Patch0001: 0001-PATCH-Disable-AVX-instruction-set-on-IA32-and-x86_64.patch

%define debug_package %{nil}

# brp-strip-static-archive will senselessly /add/ timestamps and uid/gid
# data to our .a and make them not multilib clean if we don't have this.
# Note that if we don't have the shell quotes there, -p becomes $2 on its
# invocation, and so it completely ignores it.
#
# Also note that if we try to use -D as we should (so it doesn't add
# uid/gid), strip(1) from binutils-2.25.1-22.base.el7.x86_64 throws a
# syntax error.
#
# True story.
#
%global __strip "%{__strip} -p"

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%package devel
Summary: Development Libraries and headers for EFI
Requires: gnu-efi

%description devel
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%prep
%setup -q -n gnu-efi-%{version}
%patch0001 -p1

%build
# Remove gcc's ldflags because gnu-efi uses ld directly.
export LDFLAGS=""

# Package cannot build with %%{?_smp_mflags}.
make
make apps

%install
rm -rf %{buildroot}

cp %{SOURCE1} .

mkdir -p %{buildroot}/%{_libdir}/gnuefi
make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} install
mv %{buildroot}/%{_libdir}/*.lds %{buildroot}/%{_libdir}/*.o %{buildroot}/%{_libdir}/gnuefi

%files
%license LICENSE.PTR README.efilib
%{_prefix}/%{lib}*/*

%files devel
%doc README.* ChangeLog
%license LICENSE.PTR README.efilib
%{_includedir}/efi

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0.17-1
- Auto-upgrade to 3.0.17 - Azure Linux 3.0 - package upgrades

* Wed Mar 23 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.9-10
- Updating 'Source' URL.

* Tue Oct 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.9-9
- Changing `Source0` URL to a working HTTPS one.

* Wed Jun 24 2020 Chris Co <chrco@microsoft.com> 3.0.9-8
- Add build for aarch64

* Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> 3.0.9-7
- Disable hardened ldflags to fix build.

* Thu May 28 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.0.9-6
- Adding a license reference.
- License verified against source headers' comments and "README.efilib".

* Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 3.0.9-5
- Replace BuildArch with ExclusiveArch

* Wed Apr 29 2020 Chris Co <chrco@microsoft.com> - 3.0.9-4
- Remove efi alt builds (i.e. ia32)
- Use gnu/stubs-64.h instead of gnu/stubs-32.h
- Replace git patching process with hardcoded patching in prep phase
- Remove unnecessary Canonical arch renaming patch
- Remove unnecessary efi macros, git, epoch, and comments
- Remove utils subpackage
- Update URL, Source URL
- Add BuildArch to limit build to x86_64

* Wed Apr 29 2020 Chris Co <chrco@microsoft.com> - 3.0.9-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 20 2019 Peter Jones <pjones@redhat.com> - 3.0.9-1
- Update to gnu-efi 3.0.9

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 04 2018 Peter Jones <pjones@redhat.com> - 3.0.8-4
- Rebuild for new efi-rpm-macros, now that it has settled down a bit.

* Tue May 01 2018 Peter Jones <pjones@redhat.com> - 3.0.8-3
- Use efi-rpm-macros instead of defining all the efi directory and arch
  stuff ourselves.

* Mon Apr 30 2018 Peter Jones <pjones@redhat.com> - 3.0.8-2
- Fix permissions on /boot/efi/...

* Tue Mar 20 2018 Peter Jones <pjones@redhat.com> - 3.0.8-1
- Update to 3.0.8 (from git).

* Tue Mar 13 2018 Peter Jones <pjones@redhat.com> - 3.0.7-1
- Update to 3.0.7 (from git) and add some pending patches we need.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 24 2017 Peter Jones <pjones@redhat.com> - 3.0.5-11
- Don't make .reloc sections on Aarch64 binaries.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Peter Jones <pjones@redhat.com> - 3.0.5-8
- Update this to try to get determanistic builds.

* Mon Mar 20 2017 Peter Jones <pjones@redhat.com> - 3.0.5-7
- Also build the ia32 bits in a separate 32-bit package for other consumers.

* Mon Mar 13 2017 Peter Jones <pjones@redhat.com> - 3.0.5-6
- Include ia32 bits in the x86_64 packages instead of making a separate
  32-bit package

* Tue Feb 28 2017 Peter Jones <pjones@redhat.com> - 3.0.5-5
- Fix some bugs from the 3.0.5 release...

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Peter Jones <pjones@redhat.com> - 3.0.5-3
- Update to 3.0.5

* Tue Feb 23 2016 Peter Jones <pjones@redhat.com> - 3.0.3-3
- Include patches from upstream that are after 3.0.3 This should fix the arm
  and aarch64 builds.

* Tue Feb 23 2016 Peter Jones <pjones@redhat.com> - 3.0.3-2
- We still need build-id patches in some places.

* Mon Feb 22 2016 Peter Jones <pjones@redhat.com> - 3.0.3-1
- Rebase to 3.0.3

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Dan Horák <dan[at]danny.cz> - 1:3.0.2-3
- use safer method to evaluate %%efidir

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Peter Jones <pjones@redhat.com> - 3.0.2-1
- Update to 3.0.2
- Fix base package requirement on subpackages
- Add setjmp, because this is my life.

* Tue Mar 10 2015 Peter Jones <pjones@redhat.com> - 3.0.1-1
- Update to 3.0.1
- New versioning scheme!

* Thu Nov 20 2014 Peter Jones <pjones@redhat.com> - 3.0w-2
- Use patches upstream is going to take for the build fixes
- Add some new protocol definitons.

* Fri Aug 22 2014 Kyle McMartin <kyle@fedoraproject.org> - 3.0w-0.1
- New upstream version 3.0w
- Add pjones' build fixes patch from that other distro.
- Enable AArch64

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0u-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0u-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 24 2013 Peter Jones <pjones@redhat.com> - 3.0u-0.1
- Update to 3.0u
- Split out subpackages so -devel can be multilib
- Fix path in apps subpackage to vary by distro.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0t-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Peter Jones <pjones@redhat.com> - 3.0t-0.1
- Update to 3.0t
- Don't allow use of mmx or sse registers.

* Thu May 16 2013 Peter Jones <pjones@redhat.com> - 3.0s-2
- Update to 3.0s
  Related: rhbz#963359

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0q-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Matthew Garrett <mjg@redhat.com> - 3.0q-1
- Update to current upstream
- License change - GPLv2+ to BSD

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0e-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 25 2012 Peter Jones <pjones@redhat.com> - 3.0e-17
- Align .reloc section as well to make secureboot work (mfleming)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0e-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 11 2011 Peter Jones <pjones@redhat.com> - 3.0e-15
- Correctly pad the stack when doing uefi calls
  Related: rhbz#677468
- Add ability to write UEFI callbacks and drivers
- Add test harness for ABI Calling Conventions

* Thu Jun 16 2011 Peter Jones <pjones@redhat.com> - 3.0e-14
- Handle uninitialized GOP driver gracefully.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0e-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Peter Jones <pjones@redhat.com> - 3.0e-12
- Add "modelist.efi" test utility in apps/

* Mon Jul 26 2010 Peter Jones <pjones@redhat.com> - 3.0e-11
- Add PciIo headers.

* Fri Jul 23 2010 Peter Jones <pjones@redhat.com> - 3.0e-10
- Add UEFI 2.x boot services.

* Tue Aug 11 2009 Peter Jones <pjones@redhat.com> - 3.0e-9
- Change ExclusiveArch to reflect arch changes in repos.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0e-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 03 2009 Peter Jones <pjones@redhat.com> - 3.0e-7
- Use nickc's workaround for #492183

* Tue Mar 31 2009 Peter Jones <pjones@redhat.com> - 3.0e-6.1
- Make a test package for nickc.

* Thu Mar 12 2009 Chris Lumens <clumens@redhat.com> 3.0e-6
- Add IA64 back into the list of build arches (#489544).

* Mon Mar 02 2009 Peter Jones <pjones@redhat.com> - 3.0e-5
- Switch to i586 from i386.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0e-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Peter Jones <pjones@redhat.com> - 3.0e-3
- Pad sections out in the provided linker scripts to make sure they all of
  some content.

* Fri Oct 03 2008 Peter Jones <pjones@redhat.com> - 3.0e-2
- Fix install paths on x86_64.

* Thu Oct 02 2008 Peter Jones <pjones@redhat.com> - 3.0e-1
- Update to 3.0e
- Fix relocation bug in 3.0e

* Tue Jul 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0d-6
- fix license tag

* Mon Jul 28 2008 Peter Jones <pjones@redhat.com> - 3.0d-5
- Remove ia64 palproc code since its license isn't usable.
- Remove ia64 from ExclusiveArch since it can't build...

* Thu Mar 27 2008 Peter Jones <pjones@redhat.com> - 3.0d-4
- Fix uefi_call_wrapper(x, 10, ...) .
- Add efi_main wrappers and EFI_CALL() macro so drivers are possible.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0d-3
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Peter Jones <pjones@redhat.com> - 3.0d-2
- Get rid of a bogus #ifdef .

* Wed Dec 19 2007 Peter Jones <pjones@redhat.com> - 3.0d-1
- Update to 3.0d

* Tue Jun 12 2007 Chris Lumens <clumens@redhat.com> - 3.0c-2
- Fixes for package review (#225846).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.0c-1.1
- rebuild

* Thu Apr 27 2006 Chris Lumens <clumens@redhat.com> 3.0c-1
- Upgrade to gnu-efi-3.0c.
- Enable build on i386.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.0a-7.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar  3 2005 Jeremy Katz <katzj@redhat.com> - 3.0a-7
- rebuild with gcc 4

* Tue Sep 21 2004 Jeremy Katz <katzj@redhat.com> - 3.0a-6
- add fix from Jesse Barnes for newer binutils (#129197)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 21 2004 Jeremy Katz <katzj@redhat.com> - 3.0a-4
- actually add the patch

* Tue Apr 20 2004 Bill Nottingham <notting@redhat.com> 3.0a-3
- add patch to coalesce some relocations (#120080, <erikj@sgi.com>)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Oct  4 2002 Jeremy Katz <katzj@redhat.com>
- rebuild in new environment

* Sun Jul  8 2001 Bill Nottingham <notting@redhat.com>
- update to 3.0

* Tue Jun  5 2001 Bill Nottingham <notting@redhat.com>
- add fix for invocations from the boot manager menu (#42222)

* Tue May 22 2001 Bill Nottingham <notting@redhat.com>
- add bugfix for efibootmgr (<schwab@suse.de>)

* Mon May 21 2001 Bill Nottingham <notting@redhat.com>
- update to 2.5
- add in efibootmgr from Dell (<Matt_Domsch@dell.com>)

* Thu May  3 2001 Bill Nottingham <notting@redhat.com>
- fix booting of kernels with extra arguments (#37711)

* Wed Apr 25 2001 Bill Nottingham <notting@redhat.com>
- take out Stephane's initrd patch

* Fri Apr 20 2001 Bill Nottingham <notting@redhat.com>
- fix the verbosity patch to not break passing arguments to images

* Wed Apr 18 2001 Bill Nottingham <notting@redhat.com>
- update to 2.0, build elilo, obsolete eli

* Tue Dec  5 2000 Bill Nottingham <notting@redhat.com>
- update to 1.1

* Thu Oct 26 2000 Bill Nottingham <notting@redhat.com>
- add patch for new toolchain, update to 1.0

* Thu Aug 17 2000 Bill Nottingham <notting@redhat.com>
- update to 0.9
