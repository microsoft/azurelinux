Summary:        Utilities for managing filesystem extended attributes
Name:           attr
Version:        2.5.1
Release:        3%{?dist}
License:        GPLv2+ AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://savannah.nongnu.org/projects/attr
Source:         https://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  flex-devel
BuildRequires:  gettext
BuildRequires:  libtool

Requires:       libattr = %{version}-%{release}

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package -n libattr
Summary:        Dynamic library for extended attribute support
License:        LGPLv2+

%description -n libattr
This package contains the libattr.so dynamic library which contains
the extended attribute system calls and library functions.

%package -n libattr-devel
Summary:        Files needed for building programs with libattr
License:        LGPLv2+

Provides:       %{name}-devel = %{version}-%{release}

# for <sys/xattr.h> which <attr/xattr.h> is symlinked to
Requires:       glibc-devel
Requires:       libattr = %{version}-%{release}

# provides {,f,l}{get,list,remove,set}xattr.2 man pages
Recommends:     man-pages

%description -n libattr-devel
This package contains header files and documentation needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

Currently only ext2, ext3 and XFS support extended attributes.
The SGI IRIX compatibility API built above the Linux system calls is
used by programs such as xfsdump(8), xfsrestore(8) and xfs_fsr(8).

You should install libattr-devel if you want to develop programs
which make use of extended attributes.  If you install libattr-devel,
you'll also want to install attr.

%prep
%autosetup

# FIXME: root tests are not ready for SELinux
sed -e 's|test/root/getfattr.test||' \
    -i test/Makemodule.am Makefile.in

%build
%configure

%make_build

%check
%make_build check

%install
%make_install

# get rid of libattr.a and libattr.la
rm -f %{buildroot}%{_libdir}/libattr.{l,}a

# drop already installed documentation, we will use an RPM macro to install it
rm -rf %{buildroot}%{_docdir}/%{name}*

# temporarily provide attr/xattr.h symlink until users are migrated (#1601482)
ln -fs ../sys/xattr.h %{buildroot}%{_includedir}/attr/xattr.h

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%doc doc/CHANGES
%license doc/COPYING*
%{_bindir}/attr
%{_bindir}/getfattr
%{_bindir}/setfattr
%{_mandir}/man1/attr.1*
%{_mandir}/man1/getfattr.1*
%{_mandir}/man1/setfattr.1*

%files -n libattr-devel
%{_libdir}/libattr.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/attr
%{_mandir}/man3/attr_*.3.*

%files -n libattr
%{_libdir}/libattr.so.*
%config(noreplace) %{_sysconfdir}/xattr.conf

%changelog
* Tue Sep 26 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.5.1-3
- Removing 'exit' calls from the '%%check' section.

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.5.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Nov 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.5.1-1
- Updating to version 2.5.1.
- License verified.
- Removed outdated patches.
- Replaced empty "attr-devel" subpackage with a "Provides: attr-devel" in "libattr-devel".

* Thu Nov 14 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.4.48-6
- Initial CBL-Mariner import from Fedora 30 (license: MIT).
- Add attr-devel as alias for libattr-devel

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.48-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 31 2018 Filipe Brandenburger <filbranden@gmail.com> 2.4.48-4
- Switch compatibility functions back to syscall() to prevent issue in
  interaction with fakechroot (https://github.com/dex4er/fakechroot/issues/57)

* Tue Jul 17 2018 Kamil Dudka <kdudka@redhat.com> 2.4.48-3
- temporarily provide attr/xattr.h symlink until users are migrated (#1601482)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Kamil Dudka <kdudka@redhat.com> 2.4.48-1
- new upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.47-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.47-22
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.47-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.47-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Kamil Dudka <kdudka@redhat.com> 2.4.47-19
- fix test-suite failure with perl-5.26.0 (#1473853)
- apply patches automatically to ease maintenance
- update URL of the upstream source tarball

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.47-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Kamil Dudka <kdudka@redhat.com> 2.4.47-17
- update project URL (#1418475)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.47-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Kamil Dudka <kdudka@redhat.com> 2.4.47-15
- remove outdated tests from test/attr.test

* Mon Sep 14 2015 Kamil Dudka <kdudka@redhat.com> 2.4.47-14
- make libattr-devel not insist on man-pages being installed (#1262605)

* Fri Aug 14 2015 Adam Jackson <ajax@redhat.com> 2.4.47-13
- Remove bizarre 12 year old libtool invocation workaround that prevented
  hardened cflags being applied

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.47-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Kamil Dudka <kdudka@redhat.com> 2.4.47-11
- do not install the attr.5 man page (#1219987)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.4.47-10
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.47-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 2.4.47-8
- mark license files properly

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.47-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Kamil Dudka <kdudka@redhat.com> 2.4.47-6
- do not install {,f,l}{get,list,remove,set}xattr.2 man pages

* Tue Jan 21 2014 Kamil Dudka <kdudka@redhat.com> 2.4.47-5
- refer to ENODATA instead of ENOATTR in man pages (#1055933)

* Tue Nov 19 2013 Kamil Dudka <kdudka@redhat.com> 2.4.47-4
- provide /etc/xattr.conf to exclude copying certain extended attrs (#1031423)

* Fri Aug 09 2013 Kamil Dudka <kdudka@redhat.com> 2.4.47-3
- drop a docdir-related patch to fix a packaging failure (#991997)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Kamil Dudka <kdudka@redhat.com> 2.4.47-1
- new upstream release, drop applied patches
- drop workarounds that are no longer necessary

* Fri May 03 2013 Kamil Dudka <kdudka@redhat.com> 2.4.46-10
- use <sys/syscalls.h> to fix build on aarch64 (#957989)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.46-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> 2.4.46-8
- fix specfile issues reported by the fedora-review script

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.46-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 02 2012 Kamil Dudka <kdudka@redhat.com> 2.4.46-6
- do not mention static libraries in the summary of libattr-devel (#817953)

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.4.46-5
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.4.46-4
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 06 2011 Kamil Dudka <kdudka@redhat.com> 2.4.46-2
- update project URL (#702636)

* Thu Apr 21 2011 Kamil Dudka <kdudka@redhat.com> 2.4.46-1
- new upstream release

* Tue Apr 19 2011 Kamil Dudka <kdudka@redhat.com> 2.4.45-1
- new upstream release

* Tue Mar 29 2011 Kamil Dudka <kdudka@redhat.com> 2.2.44-8
- fix typos in attr(1) man page (#669095)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.44-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Kamil Dudka <kdudka@redhat.com> 2.2.44-6
- setfattr.1: document supported encodings of values (#587516)
- getfattr: encode NULs properly with --encoding=text (#650539)
- getfattr: return non-zero exit code on failure (#660619)
- walk_tree: do not follow symlink to directory with -h (#660613)

* Tue May 25 2010 Kamil Dudka <kdudka@redhat.com> 2.2.44-5
- let attr depend on the same version of libattr (#595689)
- silence compile-time warnings

* Wed Mar 10 2010 Kamil Dudka <kdudka@redhat.com> 2.2.44-4
- run the test-suite if possible

* Tue Jan 19 2010 Kamil Dudka <kdudka@redhat.com> 2.2.44-3
- do not package a static library (#556038)
- remove multilib patch no longer useful
- enable parallel make

* Thu Jan 07 2010 Kamil Dudka <kdudka@redhat.com> 2.4.44-2
- cleanup in BuildRequires
- updated source URL
- re-downloaded source tarball from upstream (size changed by one)

* Wed Nov 25 2009 Kamil Dudka <kdudka@redhat.com> 2.4.44-1
- new upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Zdenek Prikryl <zprikryl@redhat.com> 2.4.43-2
- Fixed memory leaks (#485473)

* Wed Jul 16 2008 Zdenek Prikryl <zprikryl@redhat.com> 2.4.43-1
- New version 2.4.43

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.41-2
- fix license tags

* Wed Feb 13 2008 Zdenek Prikryl <zprikryl@redhat.com> 2.4.41-1
- New version 2.4.41
- Removed useless attr-2.0.8-docperms.patch

* Wed Oct 31 2007 Zdenek Prikryl <zprikryl@redhat.com> 2.4.39-1
- New version 2.4.39
- Resolves #284121

* Tue Oct 30 2007 Zdenek Prikryl <zprikryl@redhat.com> 2.4.38-2
- Removed explicit Requires(post + postun)
- Resolves #225290

* Tue Jul 31 2007 Zdenek Prikryl <zprikryl@redhat.com> 2.4.38-1
- New version 2.4.38
- Resolves #245415

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 2.4.32-2
- add disttag
- remove trailing dot from summary
- fix buildroot
- -devel package requires same libattr version
- change prereq to Requires(post)
- escape macro in changelog
- replace absolute link with relative link (libattr.so)
- use %%doc macro

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.4.32-1.1
- rebuild

* Wed Jul  5 2006 Thomas Woerner <twoerne@redhat.com> 2.4.32-1
- new version 2.4.32
- fixes segmentation fault in attr, which affects #189106

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 2.4.28-2
- rebuild for -devel deps

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.4.28-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.4.28-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Thomas Woerner <twoerner@redhat.com> 2.4.28-1
- new version 2.4.28

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Thomas Woerner <twoerner@redhat.com> 2.4.24-2
- spec file cleanup
- mark po files as lang specific

* Sun Nov 06 2005 Florian La Roche <laroche@redhat.com>
- 2.4.24

* Wed Sep 28 2005 Than Ngo <than@redhat.com> 2.4.23-1
- update to 2.4.23

* Wed Sep 28 2005 Than Ngo <than@redhat.com> 2.4.16-6
- get rid of *.la files
- remove duplicate doc files

* Wed Feb  9 2005 Stephen C. Tweedie <sct@redhat.com> 2.4.16-4
- Rebuild

* Fri Sep 10 2004 Stephen C. Tweedie <sct@redhat.com> 2.4.16-3
- Build requires libtool >= 1.5

* Thu Aug 19 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.16-2
- Make libattr.so.* executable.

* Thu Aug 19 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.16-1
- Update to latest upstream version.

* Sun Aug  8 2004 Alan Cox <alan@redhat.com> 2.4.1-6
- Fix bug #125304 (Steve Grubb: build requires gettext)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 31 2004 Stephen C. Tweedie <sct@redhat.com> 2.4.1-4
- Add missing %%defattr

* Tue Mar 30 2004 Stephen C. Tweedie <sct@redhat.com> 2.4.1-3
- Add /usr/include/attr to files manifest
- Fix location of doc files, add main doc dir to files manifest

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Aug  5 2003 Elliot Lee <sopwith@redhat.com> 2.4.1-2
- Fix libtool

* Tue Jun  3 2003 Stephen C. Tweedie <sct@redhat.com> 2.4.1-1
- update to attr-2.4.1

* Tue Jan 28 2003 Michael K. Johnson <johnsonm@redhat.com> 2.2.0-1
- update/rebuild

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 2.0.8-6
- set execute bits on library so that requires are generated.

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com> 2.0.8-5
- Redo multilib patch to work everywhere

* Wed Sep 11 2002 Than Ngo <than@redhat.com> 2.0.8-4
- Added fix to install libs in correct directory on 64bit machine

* Thu Aug 08 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.8-3
- Made the package only own the one directory that is unique to it:
  /usr/include/attr

* Wed Jun 26 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.8-2
- get perl out of base with attr-2.0.8-docperms.patch

* Mon Jun 24 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.8-1
- Initial Red Hat package
  Made as few changes as possible relative to upstream packaging to
  make it easier to maintain long-term.  This means that some of
  the techniques used here are definitely not standard Red Hat
  techniques.  If you are looking for an example package to fit
  into Red Hat Linux transparently, this would not be the one to
  pick.
- attr-devel -> libattr-devel
