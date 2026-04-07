# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Compact Disc Digital Audio (CDDA) extraction tool (or ripper)
Name: cdparanoia
Version: 10.2
Release: 48%{?dist}
# the app is GPLv2 and GPLv2+, everything else is LGPLv2
# Automatically converted from old format: GPLv2 and GPLv2+ and LGPLv2 - review is highly recommended.
License: GPL-2.0-only AND GPL-2.0-or-later AND LicenseRef-Callaway-LGPLv2
URL: http://www.xiph.org/paranoia/index.html

Source: http://downloads.xiph.org/releases/cdparanoia/cdparanoia-III-%{version}.src.tgz
# Patch from upstream to fix cdda_interface.h C++ incompatibility ("private")
# https://trac.xiph.org/changeset/15338
# https://bugzilla.redhat.com/show_bug.cgi?id=463009
Patch0: cdparanoia-10.2-#463009.patch
# #466659
Patch1: cdparanoia-10.2-endian.patch
Patch2: cdparanoia-10.2-install.patch
Patch3: cdparanoia-10.2-format-security.patch
Patch4: cdparanoia-use-proper-gnu-config-files.patch
Patch5: cdparanoia-10.2-ldflags.patch
# https://svn.xiph.org/trunk/cdparanoia@17289
Patch6: cdparanoia-10.2-add-pkgconfig.patch

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires: make

%description
Cdparanoia (Paranoia III) reads digital audio directly from a CD, then
writes the data to a file or pipe in WAV, AIFC or raw 16 bit linear
PCM format.  Cdparanoia doesn't contain any extra features (like the ones
included in the cdda2wav sampling utility).  Instead, cdparanoia's strength
lies in its ability to handle a variety of hardware, including inexpensive
drives prone to misalignment, frame jitter and loss of streaming during
atomic reads.  Cdparanoia is also good at reading and repairing data from
damaged CDs.

%package static
Summary: Development tools for libcdda_paranoia (Paranoia III)
Requires: cdparanoia-devel = %{version}-%{release}
# Automatically converted from old format: LGPLv2 - review is highly recommended.
License: LicenseRef-Callaway-LGPLv2

%description static
The cdparanoia-devel package contains the static libraries needed for
developing applications to read CD Digital Audio disks.

%package libs
Summary: Libraries for libcdda_paranoia (Paranoia III)
# Automatically converted from old format: LGPLv2 - review is highly recommended.
License: LicenseRef-Callaway-LGPLv2

%description libs
The cdparanoia-libs package contains the dynamic libraries needed for
applications which read CD Digital Audio disks.

%package devel
Summary: Development tools for libcdda_paranoia (Paranoia III)
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
# Automatically converted from old format: LGPLv2 - review is highly recommended.
License: LicenseRef-Callaway-LGPLv2

%description devel
The cdparanoia-devel package contains the libraries and header files needed
for developing applications to read CD Digital Audio disks.

%prep
%setup -q -n cdparanoia-III-%{version}
%patch -P0 -p3 -b .#463009
%patch -P1 -p1 -b .endian
%patch -P2 -p1 -b .install
%patch -P3 -p1 -b .fmt-sec
%patch -P4 -p1 -b .config
%patch -P5 -p1 -b .ldflags
%patch -P6 -p1 -b .pkgconfig

# Update config.guess/sub for newer architectures
cp /usr/lib/rpm/redhat/config.* .

%build
autoreconf -ifv
%configure --includedir=%{_includedir}/cdda
# Also remove many warnings which we are aware of
# Lastly, don't use _smp_mflags since it also makes the build fail
make OPT="$RPM_OPT_FLAGS -Wno-pointer-sign -Wno-unused" LDFLAGS="%{?__global_ldflags}"


%install
make install DESTDIR=$RPM_BUILD_ROOT

%ldconfig_scriptlets libs

%files
%doc COPYING* README
%{_bindir}/cdparanoia
%{_mandir}/man1/cdparanoia.1*

%files libs
%{_libdir}/*.so.*

%files devel
%{_includedir}/cdda/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%files static
%{_libdir}/*.a

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 10.2-46
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 20 2021 Jiri Kucera <jkucera@redhat.com> - 10.2-37
- Include also GPLv2+ to License field (main.c and cachetest.c
  are distributed under GPLv2+)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 26 2020 Dan Horák <dan[at]danny.cz> - 10.2-35
- Add pkgconfig support

* Mon Oct 05 2020 Stephen Gallagher <sgallagh@redhat.com> - 10.2-34
- Fix build on Fedora 33+

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-33
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Adam Jackson <ajax@redhat.com> - 10.2-27
- Fix LDFLAGS propagation
- Stop building with -O0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.2-25
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 10.2-19
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May  3 2014 Peter Robinson <pbrobinson@fedoraproject.org> 10.2-16
- Update config.guess config.sub to build on new architectures
- Cleanup spec

* Mon Apr 14 2014 Jaromir Capik <jcapik@redhat.com> - 10.2-15
- Fixing format-security flaws (#1037011)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 05 2010 Adam Jackson <ajax@redhat.com> 10.2-9
- Fix packaging typo from -7

* Wed Feb 03 2010 Peter Jones <pjones@redhat.com> - 10.2-8
- Incorporate changes from Matthias Saou:
- Include install patch, to avoid all of the ugly manual installation.
- Cosmetic fixes (libs group, scriplets, don't mix %%name with hardcode...).

* Tue Feb 02 2010 Adam Jackson <ajax@redhat.com> 10.2-7
- Move static libs to -static subpackage, make it require -devel

* Tue Dec  8 2009 Matthias Saou <http://freshrpms.net/> 10.2-6
- Fix all of the problems detected during the review which aren't acceptable
  according to the current policies and guidelines (part of #225638).
- Don't prefix summaries with "A" nor suffix them with a dot.
- Move .so symlink to the devel sub-package (#203620).
- Add highest known version to the cdparanoia-III obsoletes.
- Remove incorrect buildroot removal from %%build.
- Use acceptable %%clean section.
- Provide cdparanoia-static in the devel sub-package since the *.a is there.
- Use single-command scriplet syntax for /sbin/ldconfig calls.
- Escape all macros in changelog.
- Include license file since it is present with the sources.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Adam Jackson <ajax@redhat.com>
- Merge review cleanups (not finished, #225638)

* Tue Feb 10 2009 Adam Jackson <ajax@redhat.com> 10.2-3
- cdparanoia-10.2-endian.patch: Backport a crash fix for host/drive
  endianness mismatch. (#466659)

* Tue Sep 30 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 10.2-2
- fix cdda_interface.h C++ incompatibility (patch from upstream) (#463009)

* Thu Sep 11 2008 Adam Jackson <ajax@redhat.com> 10.2-1
- cdparanoia 10.2

* Wed Aug 13 2008 Adam Jackson <ajax@redhat.com> 10.1-1
- Update to 10.1, just changes the license back.

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10.0-3
- fix license tag
- fix headers, setspeed patch to apply with fuzz=0

* Thu Jun 19 2008 Adam Jackson <ajax@redhat.com> 10.0-2
- cdparanoia 10.

* Thu Mar 20 2008 Adam Jackson <ajax@redhat.com> alpha9.8-30
- Add -Werror-implicit-function-declarations.
- cdparanoia-III-alpha9.8-headers.patch: Fix the resulting errors.

* Tue Mar 04 2008 Adam Jackson <ajax@redhat.com> alpha9.8-29
- cdparanoia-III-alpha9.8.scsi-setspeed.patch: Allow setting the speed of
  SCSI CD drives. (#431178)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - alpha9.8-28.2
- Autorebuild for GCC 4.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - alpha9.8-27.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - alpha9.8-27.1
- bump again for double-long bug on ppc(64)

* Wed Feb 08 2006 Monty Montgomery <cmontgom@redhat.com> - alpha9.8-27
- rebuilt 

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - alpha9.8-26.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- make sure shared libs are linked against respective other libs

* Wed Mar 16 2005 Peter Jones <pjones@redhat.com> alpha9.8-25
- gcc4 rebuild and CFLAGS change

* Wed Feb 9 2005 Peter Jones <pjones@redhat.com> alpha9.8-24.2
- Rebuild for new toolchain

* Wed Oct 6 2004 Peter Jones <pjones@redhat.com> alpha9.8-24
- workaround for sgio read size issues in newer kernels.

* Fri Oct 1 2004 Peter Jones <pjones@redhat.com> alpha9.8-23
- "This time, with a meaningful changelog" release.  Just like -22.
- new SG_IO code in rawhide.  This means ripping will no longer use the 
  "cooked ioctl" mode that it has since we moved to 2.6, instead utilizing
  the real scsi-based command set to talk to most drives.  This should
  result in better error correction handling, and usage of much more
  commonly used kernel features.
- environment variable "CDDA_TRANSPORT" added.  If you set this to "cooked",
  cdparanoia will try to use the "cooked ioctl" mode instead of SCSI/SG_IO
  based modes first, and then fall back to SG_IO.
- It'd be good if this got some testing.  A prior version of the SG_IO code
  was known to fail on some USB drives.  This version should mitigate that
  quite a bit, but I lack the hardware to test it for sure.
  
* Wed Jul 7 2004 Peter Jones <pjones@redhat.com> alpha9.8-21sgio1
- a new set of sgio patches

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 17 2004 Peter Jones <pjones@redhat.com> alpha9.8-20
- take ownership of %%{_includedir}/cdda

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 20 2003 Peter Jones <pjones@redhat.com> alpha9.8-17
- typo fix (g_fd -> fd)
- add errno output

* Tue May 06 2003 Peter Jones <pjones@redhat.com> alpha9.8-16
- fix warnings on switches
- use O_EXCL

* Tue Feb 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlinks to shared libs

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 25 2002 Tim Powers <timp@redhat.com> alpha9.8-13
- fix %%install references in the changelog so that it will rebuild properly

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> alpha9.8-12
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr  3 2002 Peter Jones <pjones@redhat.com> alpha9.8-8
- don't strip, let rpm do that

* Mon Feb 25 2002 Tim Powers <timp@redhat.com> alpha9.8-7
- fix broken Obsoletes of cdparanoia-devel

* Thu Dec  6 2001 Peter Jones <pjones@redhat.com> alpha9.8-6
- move includes to %%{_includedir}/cdda/
- add utils.h to %%install
- clean up %%install some.

* Sun Nov  4 2001 Peter Jones <pjones@redhat.com> alpha9.8-5
- make a -libs package which contains the .so files
- make the cdparanoia dependancy towards that, not -devel

* Thu Aug  2 2001 Peter Jones <pjones@redhat.com>
- bump the release not to conflict with on in the RH build tree :/
- reverse devel dependency

* Wed Aug  1 2001 Peter Jones <pjones@redhat.com>
- fix %%post and %%postun to only run ldconfig for devel packages

* Wed Jul 18 2001 Crutcher Dunnavant <crutcher@redhat.com>
- devel now depends on package

* Wed Mar 28 2001 Peter Jones <pjones@redhat.com>
- 9.8 release.

* Tue Feb 27 2001 Karsten Hopp <karsten@redhat.de>
- fix spelling error in description

* Thu Dec  7 2000 Crutcher Dunnavant <crutcher@redhat.com>
- rebuild for new tree

* Fri Jul 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 06 2000 Preston Brown <pbrown@redhat.com>
- revert name change
- use new rpm macro paths

* Wed Apr 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Switched spec file from the one used in Red Hat Linux 6.2, which
  also changes the name
- gzip man page

* Thu Dec 23 1999 Peter Jones <pjones@redhat.com>
- update package to provide cdparanoia-alpha9.7-2.*.rpm and 
  cdparanoia-devel-alpha9.7-2.*.rpm.  Also, URLs point at xiph.org
  like they should.

* Wed Dec 22 1999 Peter Jones <pjones@redhat.com>
- updated package for alpha9.7, based on input from:
  Monty <xiphmont@xiph.org> 
  David Philippi <david@torangan.saar.de>

* Mon Apr 12 1999 Michael Maher <mike@redhat.com>
- updated pacakge

* Tue Oct 06 1998 Michael Maher <mike@redhat.com>
- updated package

* Mon Jun 29 1998 Michael Maher <mike@redhat.com>
- built package
