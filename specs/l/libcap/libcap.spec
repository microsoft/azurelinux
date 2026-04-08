# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: libcap
Version: 2.76
Release: 3%{?dist}
Summary: Library for getting and setting POSIX.1e capabilities
URL: https://sites.google.com/site/fullycapable/
License: BSD-3-Clause OR GPL-2.0-only

Source0: https://mirrors.edge.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.gz
Source1: https://mirrors.edge.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.sign
Source2: https://git.kernel.org/pub/scm/docs/kernel/pgpkeys.git/plain/keys/29EE848AE2CCF3F4.asc

BuildRequires: pam-devel gcc
BuildRequires: make
BuildRequires: glibc-static
BuildRequires: gnupg2

%ifarch %{golang_arches}
BuildRequires: golang >= 1.22
%endif

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/setcap
%endif

%description
libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package static
Summary: Static libraries for libcap development
Requires: %{name} = %{version}-%{release}

%description static
The libcap-static package contains static libraries needed to develop programs
that use libcap and need to be statically linked. 

libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package devel
Summary: Development files for libcap
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, etc) for libcap.

libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install libcap-devel if you want to develop or compile applications using
libcap.

%ifarch %{golang_arches}
%package -n captree
Summary: Capability inspection utility

%description -n captree
The captree program was inspired by the utility pstree, but it uses the
libcap/cap (Go package) API to explore process runtime state and display
the capability status of processes and threads.
%endif

%prep
gzip -cd %{SOURCE0} | %{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data=-
%autosetup -p1


%build
%make_build prefix=%{_prefix} lib=%{_lib} SBINDIR=%{_sbindir} CGO_REQUIRED=1 CGO_CFLAGS="${CFLAGS}" CGO_LDFLAGS="${LDFLAGS}" GO_BUILD_FLAGS="-buildmode=pie -a -v -x -ldflags='-compressdwarf=false -B gobuildid'" all

%check
make test

%install
%make_install prefix=%{_prefix} lib=%{_lib} SBINDIR=%{_sbindir} CGO_REQUIRED=1 CGO_CFLAGS="${CFLAGS}" CGO_LDFLAGS="${LDFLAGS}" GO_BUILD_FLAGS="-buildmode=pie -ldflags='-compressdwarf=false -B gobuildid'"

mkdir -p %{buildroot}/%{_mandir}/man{2,3,5,8}
mv -f doc/*.3 %{buildroot}/%{_mandir}/man3/

chmod +x %{buildroot}/%{_libdir}/*.so.*

%ldconfig_scriptlets

%files
%license License
%doc doc/capability.md
%{_libdir}/libcap.so.2{,.*}
%{_libdir}/libpsx.so.2{,.*}
%{_sbindir}/{capsh,getcap,getpcaps,setcap}
%{_mandir}/man1/capsh.1*
%{_mandir}/man5/capability.conf.5*
%{_mandir}/man7/cap_text_formats.7*
%{_mandir}/man8/{getcap,getpcaps,setcap,pam_cap}.8*
%{_libdir}/security/pam_cap.so
%exclude %{_mandir}/man8/captree.8*

%files static
%{_libdir}/libcap.a
%{_libdir}/libpsx.a

%files devel
%{_includedir}/sys/capability.h
%{_includedir}/sys/psx_syscall.h
%{_libdir}/libcap.so
%{_libdir}/libpsx.so
%{_mandir}/man3/cap*.3*
%{_mandir}/man3/libcap.3*
%{_mandir}/man3/libpsx.3*
%{_mandir}/man3/psx_*.3*
%{_mandir}/man3/__psx_syscall.3*
%{_libdir}/pkgconfig/{libcap,libpsx}.pc

%ifarch %{golang_arches}
%files -n captree
%license License
%{_sbindir}/captree
%{_mandir}/man8/captree.8*
%endif

%changelog
* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 2.76-3
- Rebuild for golang-1.25.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild


* Mon Apr 14 2025 Carlos Rodriguez-Fernandez <carlosrodrifernandez@gmail.com> - 2.76-1
- Update to version 2.76 (rhbz#2349318, rhbz#2352529)

* Fri Jan 24 2025 Carlos Rodriguez-Fernandez <carlosrodrifernandez@gmail.com> - 2.73-2
- Update internal CI tests

* Fri Jan 24 2025 Carlos Rodriguez-Fernandez <carlosrodrifernandez@gmail.com> - 2.73-1
- Update to version 2.73 (rhbz#2340722)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.71-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.71-2
- Rebuilt for the bin-sbin merge (2nd attempt)

* Mon Oct 28 2024 Carlos Rodriguez-Fernandez <carlosrodrifernandez@gmail.com> - 2.71-1
- Update to version 2.71

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.70-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.70-3
- Rebuilt for the bin-sbin merge

* Tue Jun 04 2024 Anderson Toshiyuki Sasaki <ansasaki@redhat.com> - 2.70-2
- Set CGO_CFLAGS=$CFLAGS and CGO_LDFLAGS=$LDFLAGS to build Go code

* Mon May 20 2024 Carlos Rodriguez-Fernandez <carlosrodrifernandez@gmail.com> - 2.70-1
- Update to version 2.70

* Fri Apr 05 2024 Carlos Rodriguez-Fernandez <carlosrodrifernandez@gmail.com> - 2.69-8
- Make correction to the capability.conf manpage

* Fri Apr 05 2024 Carlos Rodriguez-Fernandez <carlosrodrifernandez@gmail.com> - 2.69-7
- Reenable PIE in the captree tool

* Thu Apr 04 2024 Carlos Rodriguez-Fernandez <carlosrodrifernandez@gmail.com> - 2.69-6
- Fix incompatibility of the build with go 1.22.

* Wed Apr 03 2024 Carlos Rodriguez-Fernandez <carlosrodrifernandez@gmail.com> - 2.69-5
- Add manpages for pam_cap and capability.conf

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 2.69-4
- Rebuild for golang 1.22.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.69-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 06 2023 Carlos Rodriguez-Fernandez <carlosrodrifernandez@gmail.com> - 2.69-1
- Update to 2.69 (with contribs from Yanko Kaneti <yaneti@declera.com>, and Andrew G. Morgan <morgan@kernel.org>)
- Update license to SPDX (by Anderson Toshiyuki Sasaki <ansasaki@redhat.com>)
- Make file lists more explicit to avoid accidental ABI changes (Dominik Mierzejewski <dominik@greysector.net>)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.48-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.48-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.48-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Feb 14 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2.48-2
- Rebase distro flags patch

* Wed Feb 10 2021 Giuseppe Scrivano <gscrivan@redhat.com> - 2.48-1
- Update to 0.2.48

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 17 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2.46-1
- Update to 0.2.46

* Wed Oct 21 2020 Karsten Hopp <karsten@fedoraproject.org> - 2.44-1
- update to 2.44
- remove additional getpcaps manpage as it now included in the sources

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Karsten Hopp <karsten@redhat.com> - 2.26-5
- enable gating

* Mon Feb 04 2019 Karsten Hopp <karsten@redhat.com> - 2.26-4
- bump release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Karsten Hopp <karsten@redhat.com> - 2.26-2
- add CI tests using the standard test interface (astepano)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Karsten Hopp <karsten@redhat.com> - 2.25-11
- rebuild

* Wed Feb 21 2018 Karsten Hopp <karsten@redhat.com> - 2.25-10
- buildrequire gcc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.25-8
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Karsten Hopp <karsten@redhat.com> - 2.25-4
- add -static subpackage (rhbz#1380251)

* Sun Nov 27 2016 Lubomir Rintel <lkundrak@v3.sk> - 2.25-3
- Add perl BR to fix FTBFS

* Mon Apr 25 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.25-2
- Fix pkgconfig install location on aarch64
- Spec file cleanups

* Mon Apr 11 2016 Karsten Hopp <karsten@redhat.com> - 2.25-1
- libcap-2.25

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Tom Callaway <spot@fedoraproject.org> - 2.24-6
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Karsten Hopp <karsten@redhat.com> 2.24-4
- fix libdir in libcap.pc

* Wed Apr 23 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2.24-3
- set pkg-config dir to proper value to get it built on AArch64

* Wed Apr 16 2014 Karsten Hopp <karsten@redhat.com> 2.24-2
- fix URL and license

* Wed Apr 16 2014 Karsten Hopp <karsten@redhat.com> 2.24-1
- update to 2.24
- dropped patch for rhbz#911878, it is upstream now

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Karsten Hopp <karsten@redhat.com> 2.22-6
- mv libraries to /usr/lib*
- add getpcaps man page 
- spec file cleanup
- fix URL of tarball

* Tue May 14 2013 Karsten Hopp <karsten@redhat.com> 2.22-5
- add patch from Mark Wielaard to fix use of uninitialized memory in _fcaps_load
  rhbz #911878

* Sun Feb 24 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.22-5
- Build with $RPM_OPT_FLAGS and $RPM_LD_FLAGS.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 27 2011 Karsten Hopp <karsten@redhat.com> 2.22-1
- update to 2.22 (#689752)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 10 2009 Karsten Hopp <karsten@redhat.com> 2.17-1
- update to 2.17

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Karsten Hopp <karsten@redhat.com> 2.16-4
- fix build problems with p.e. cdrkit

* Sun Mar 22 2009 Karsten Hopp <karsten@redhat.com> 2.16-1
- update, with a fix for rebuild problems

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 06 2008 Karsten Hopp <karsten@redhat.com> 2.10-2
- drop libcap.so.1
- fix buildrequires and path to pam security module

* Thu Jun 05 2008 Karsten Hopp <karsten@redhat.com> 2.10-1
- libcap-2.10

* Thu Feb 21 2008 Karsten Hopp <karsten@redhat.com> 2.06-4
- don't build static binaries (#433808)

* Wed Feb 20 2008 Karsten Hopp <karsten@redhat.com> 2.06-3
- temporarily add libcap-1 libraries to bootstrap some packages

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.06-2
- Autorebuild for GCC 4.3

* Fri Feb 15 2008 Karsten Hopp <karsten@redhat.com> 2.06-1
- upate to 2.06 (#432983)

* Wed Jan 16 2008 Karsten Hopp <karsten@redhat.com> 1.10-33
- drop post,postun requirements on ldconfig as find-requires can handle this

* Tue Jan 15 2008 Karsten Hopp <karsten@redhat.com> 1.10-32
- add disttag
- fix changelog
- fix defattr

* Mon Jan 14 2008 Karsten Hopp <karsten@redhat.com> 1.10-31
- use cp -p in spec file to preserve file attributes (#225992)
- add license file

* Fri Aug 24 2007 Karsten Hopp <karsten@redhat.com> 1.10-30
- rebuild

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 1.10-29
- add CAP_AUDIT_WRITE and CAP_AUDIT_CONTROL (#229833)

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 1.10-28
- drop obsolete ia64 patch
- rpmlint fixes

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 1.10-27
- misc. review fixes
- add debian patch to make it build with a recent glibc
- remove static lib

* Wed Jul 19 2006 Karsten Hopp <karsten@redhat.de> 1.10-25
- add patch to support COPTFLAG (#199365)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.10-24.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.10-24.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.10-24.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Karsten Hopp <karsten@redhat.de> 1.10-24
- added development manpages
- as there are no manpages for the executables available, added at least
  a FAQ (#172324)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 31 2005 Steve Grubb <sgrubb@redhat.com> 1.10-23
- rebuild to pick up audit capabilities

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.10-22
- build with gcc-4

* Wed Feb 09 2005 Karsten Hopp <karsten@redhat.de> 1.10-21
- rebuilt

* Tue Aug 31 2004 Phil Knirsch <pknirsch@redhat.com> 1.10-20
- Fix wrong typedef in userland patch (#98801)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Karsten Hopp <karsten@redhat.de> 1.10-17
- use _manpath

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 1.10-14
- set execute bits on library so that requires are generated.

* Thu Nov 21 2002 Mike A. Harris <mharris@redhat.com> 1.10-13
- Removed %%name macro sillyness from package Summary, description text, etc.
- Removed archaic Prefix: tag
- lib64 fixes everywhere to use _lib, _libdir, etc
- Removed deletion of RPM_BUILD_DIR from %%clean section
- Added -q flag to setup macro
- Severely cleaned up spec file, and removed usage of perl

* Fri Jul 19 2002 Jakub Jelinek <jakub@redhat.com> 1.10-12
- CFLAGS was using COPTFLAG variable, not COPTFLAGS
- build with -fpic
- apply the IA-64 patch everywhere, use capget/capset from glibc,
  not directly as _syscall (as it is broken on IA-32 with -fpic)
- reenable alpha

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.10-10
- Exclude alpha for now, apparent gcc bug.

* Fri Nov  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.10-6
- Fix sys/capabilities.h header (#55727)
- Move to /lib, some applications seem to be using this rather early
  (#55733)

* Mon Jul 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add post,postun scripts

* Tue Jul 10 2001 Jakub Jelinek <jakub@redhat.com>
- don't build libcap.so.1 with ld -shared, but gcc -shared

* Wed Jun 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Rebuild - it was missing for alpha

* Wed Jun 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390/s390x support

* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.10-1
- initial RPM
- fix build on ia64
