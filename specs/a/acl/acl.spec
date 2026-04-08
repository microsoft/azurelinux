# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Access control list utilities
Name: acl
Version: 2.3.2
Release: 4%{?dist}
BuildRequires: gawk
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: libattr-devel
BuildRequires: libtool
BuildRequires: make
BuildRequires: perl(FileHandle)
BuildRequires: gnupg2
Requires: libacl%{?_isa} = %{version}-%{release}
Source0: https://download-mirror.savannah.gnu.org/releases/acl/acl-%{version}.tar.gz
Source1: https://download-mirror.savannah.gnu.org/releases/acl/acl-%{version}.tar.gz.sig
# Retreived from https://savannah.nongnu.org/people/viewgpg.php?user_id=15000
# Source2: agruen-key.gpg
# Retrieved from https://savannah.nongnu.org/people/viewgpg.php?user_id=42032
Source2: vapier-key.gpg

# avoid permission denied problem with LD_PRELOAD in the test-suite
Patch1: 0001-acl-2.2.53-test-runwrapper.patch

License: GPL-2.0-or-later AND LGPL-2.1-or-later
URL: https://savannah.nongnu.org/projects/acl

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n libacl
Summary: Dynamic library for access control list support
License: LGPL-2.1-or-later
Conflicts: filesystem < 3

%description -n libacl
This package contains the libacl.so dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
Summary: Files needed for building programs with libacl
License: LGPL-2.1-or-later
Requires: libacl%{?_isa} = %{version}-%{release}, libattr-devel

%description -n libacl-devel
This package contains header files and documentation needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
%configure

# uncomment to turn on optimizations
# sed -i 's/-O2/-O0/' libtool include/builddefs
# unset CFLAGS

%make_build

%check
# make the test-suite use the just built library (instead of the system one)
export LD_LIBRARY_PATH="${RPM_BUILD_ROOT}%{_libdir}:${LD_LIBRARY_PATH}"

if ./setfacl -m "u:$(id -u):rwx" .; then
    if test 0 = "$(id -u)"; then
        # test/root/permissions.test requires the 'daemon' user to be a member
        # of the 'bin' group in order not to fail.  Prevent the test from
        # running if we detect that its requirements are not met (#1085389).
        if id -nG daemon | { ! grep bin >/dev/null; }; then
            sed -e 's|test/root/permissions.test||' \
                -i test/Makemodule.am Makefile.in Makefile
        fi

        # test/root/setfacl.test fails if 'bin' user cannot access build dir
        if ! runuser -u bin -- "${PWD}/setfacl" --version; then
            sed -e 's|test/root/setfacl.test||' \
                -i test/Makemodule.am Makefile.in Makefile
        fi
    fi

    # run the upstream test-suite
    %make_build check || exit $?
else
    echo '*** ACLs are probably not supported by the file system,' \
         'the test-suite will NOT run ***'
fi

%install
%make_install

# get rid of libacl.a and libacl.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libacl.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libacl.la

chmod 0755 $RPM_BUILD_ROOT/%{_libdir}/libacl.so.*.*.*

# drop already installed documentation, we will use an RPM macro to install it
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}*

%find_lang %{name}

%ldconfig_scriptlets -n libacl

%files -f %{name}.lang
%license doc/COPYING*
%{_bindir}/chacl
%{_bindir}/getfacl
%{_bindir}/setfacl
%{_mandir}/man1/chacl.1*
%{_mandir}/man1/getfacl.1*
%{_mandir}/man1/setfacl.1*
%{_mandir}/man5/acl.5*

%files -n libacl-devel
%{_libdir}/libacl.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/acl
%{_includedir}/sys/acl.h
%{_mandir}/man3/acl_*

%files -n libacl
%{_libdir}/libacl.so.*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.3.2-1
- rebase to latest version (rhbz#2260000)

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 01 2023 Lukáš Zaoral <lzaoral@redhat.com> - 2.3.1-11
- make acl compatible with -D_FORTIFY_SOURCE=3 (rhbz#2249839)

* Fri Oct 06 2023 Lukáš Zaoral <lzaoral@redhat.com> - 2.3.1-10
- preserve failed setfacl return code (RHEL-3909)
- make the license tag more precise

* Mon Sep 11 2023 Temuri Doghonadze <temuri.doghonadze@gmail.com> - 2.3.1-9
- Backport Georgian locale from git
- Note, it will not be needed after release of new version of acl

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 14 2023 Lukáš Zaoral <lzaoral@redhat.com> - 2.3.1-7
- migrated to SPDX license

* Thu Jan 26 2023 Lukáš Zaoral <lzaoral@redhat.com> - 2.3.1-6
- acl is not yet compatible with -D_FORTIFY_SOURCE=3

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 16 2021 Kamil Dudka <kdudka@redhat.com> - 2.3.1-1
- new upstream release

* Fri Mar 12 2021 Kamil Dudka <kdudka@redhat.com> - 2.3.0-1
- new upstream release

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.53-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 31 2020 Kamil Dudka <kdudka@redhat.com> 2.2.53-9
- make __acl_create_entry_obj() work with LTO enabled (#1873975)

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.53-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.53-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Tom Stellard <tstellar@redhat.com> - 2.2.53-6
- Spec file cleanups and build fix
- Add BuildRequires: perl-FileHandle to fix make check
- Add BuildRequres: gcc [1]
- Use make_build [2] and make_install[3] macros
- [1] https://docs.fedoraproject.org/en-US/packaging-guidelines/C_and_C++/#_buildrequires_and_requires
- [2] https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- [3] https://docs.fedoraproject.org/en-US/packaging-guidelines/#_why_the_makeinstall_macro_should_not_be_used

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.53-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.53-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.53-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Kamil Dudka <kdudka@redhat.com> 2.2.53-1
- new upstream release

* Tue Mar 13 2018 Kamil Dudka <kdudka@redhat.com> 2.2.52-21
- update link to POSIX.1e draft in acl(5) man page (#1510527)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.52-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.2.52-19
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.52-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.52-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Kamil Dudka <kdudka@redhat.com> 2.2.52-16
- fix test-suite failure with perl-5.26.0 (#1473845)
- update URL of the upstream source tarball

* Thu May 18 2017 Kamil Dudka <kdudka@redhat.com> 2.2.52-15
- setfacl.1: document the meaning of '-' in perms (#1337039)
- avoid failure of %%check when building as root (#1085389)
- apply patches automatically to ease maintenance

* Wed May 17 2017 Kamil Dudka <kdudka@redhat.com> 2.2.52-14
- drop obsolete BuildRoot and Group tags
- fix spurious acl_check() failure on setfacl --restore (#1451826)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.52-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Kamil Dudka <kdudka@redhat.com> 2.2.52-12
- update project URL (#1418474)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.52-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 14 2015 Adam Jackson <ajax@redhat.com> 2.2.52-10
- Remove bizarre 12 year old libtool invocation workaround that prevented
  hardened cflags working

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.52-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.2.52-8
- Rebuilt for
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.52-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 2.2.52-6
- tag licenses properly

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.52-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov 01 2013 Kamil Dudka <kdudka@redhat.com> 2.2.52-4
- fix SIGSEGV of getfacl -e on overly long group name

* Fri Aug 09 2013 Kamil Dudka <kdudka@redhat.com> 2.2.52-3
- drop a docdir-related patch to fix a packaging failure (#993659)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Kamil Dudka <kdudka@redhat.com> 2.2.52-1
- new upstream release, drop applied patches
- drop workarounds that are no longer necessary

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.51-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> 2.2.51-8
- fix specfile issues reported by the fedora-review script

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.51-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 02 2012 Kamil Dudka <kdudka@redhat.com> 2.2.51-6
- do not mention static libraries in the summary of libacl{,-devel} (#817952)

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.2.51-5
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.2.51-4
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.51-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 06 2011 Kamil Dudka <kdudka@redhat.com> 2.2.51-2
- update project URL (#699058)

* Thu Apr 21 2011 Kamil Dudka <kdudka@redhat.com> 2.2.51-1
- new upstream release

* Tue Apr 19 2011 Kamil Dudka <kdudka@redhat.com> 2.2.50-1
- new upstream release

* Wed Apr 06 2011 Kamil Dudka <kdudka@redhat.com> 2.2.49-11
- add function acl_extended_file_nofollow() (#692982)

* Tue Mar 29 2011 Kamil Dudka <kdudka@redhat.com> 2.2.49-10
- fix typos in setfacl(1) man page (#675451)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.49-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 08 2010 Kamil Dudka <kdudka@redhat.com> 2.2.49-8
- remove dependency of libacl-devel on nfs-utils-lib and openldap

* Tue May 25 2010 Kamil Dudka <kdudka@redhat.com> 2.2.49-7
- let acl depend on the same version of libacl (#595674)

* Wed Mar 24 2010 Kamil Dudka <kdudka@redhat.com> 2.2.49-6
- prevent setfacl --restore from SIGSEGV on malformed restore file (#576550)

* Wed Mar 10 2010 Kamil Dudka <kdudka@redhat.com> 2.2.49-5
- run the test-suite if possible

* Tue Jan 19 2010 Kamil Dudka <kdudka@redhat.com> 2.2.49-4
- do not package a static library (#556036)
- remove multilib patch no longer useful
- cleanup in BuildRequires

* Tue Jan 05 2010 Kamil Dudka <kdudka@redhat.com> 2.2.49-3
- upstream patch for setfacl --restore SUID/SGID bits handling (#467936)

* Sat Dec 26 2009 Kamil Dudka <kdudka@redhat.com> 2.2.49-2
- tweaked setfacl tree walk flags (#488674), thanks to Markus Steinborn

* Sun Dec 20 2009 Kamil Dudka <kdudka@redhat.com> 2.2.49-1
- new upstream bugfix release
- big cleanup in patches

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.47-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 31 2008 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.47-3
- little improvement to params patch
- Resolves: #457244

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.47-2
- rework params patch to apply with fuzz=0
- fix license tag

* Tue Feb 12 2008 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.47-1
- new upstream version

* Mon Jan 28 2008 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.45-3
- Fixed segfault when using only "--" as parameter
- Resolves: #430458

* Wed Nov  7 2007 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.45-2
- Fixed setfacl exitcodes
- Resolves: #368451

* Wed Oct 31 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 2.2.45-1
- New version
- dropped walk patch

* Thu Sep 20 2007 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.39-10
- Rewriten path_max patch to support long UTF8 names
- Resolves #287701, #183181

* Fri Aug 31 2007 Steve Dickson <steved@redhat.com> - 2.2.39-9
- Removed NFS4 ACL patch since it was rejected by upstream.

* Thu Aug 30 2007 Jeremy Katz <katzj@redhat.com> - 2.2.39-8
- disable nfs patch; linking libacl against libs in /usr will lead to breakage

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.2.39-7
- Build Require gawk

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.2.39-6
- Rebuild for selinux ppc32 issue.

* Mon Aug 27 2007 Steve Dickson <steved@redhat.com>  2.2.39-5
- Added NFS v4 ACL support

* Thu Jul 26 2007 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.39-4.1
- Updated man page for getfacl

* Wed Jul 25 2007 Jiri Moskovcak <jmoskovc@redhat.com> 2.2.39-4
- Added support fort short params to getfacl
- Resolves: #204087

* Wed Mar 21 2007 Thomas Woerner <twoerner@redhat.com> 2.2.39-3.1
- new improved walk patch with fixed getfacl exit code (rhbz#232884)

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 2.2.39-3
- fix buildroot
- remove trailing dot from summary
- -devel requires same version of libacl
- escape macro in changelog
- make .so symlink relative

* Thu Feb 22 2007 Steve Grubb <sgrubb@redhat.com> 2.2.39-2
- Apply patch to make order consistent.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.39-1.1
- rebuild

* Wed Jul  5 2006 Thomas Woerner <twoerner@redhat.com> 2.2.39-1
- new version 2.2.39
- fixed usage of long UTF-8 filenames (#183181)
  Thanks to Andrey for the initial patch.

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 2.2.34-2
- rebuild for -devel deps

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2.34-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2.34-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Thomas Woerner <twoerner@redhat.com> 2.2.34-1
- new version 2.2.34

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Thomas Woerner <twoerner@redhat.com> 2.2.32-2.1
- fixed permissions of libacl

* Tue Dec  6 2005 Thomas Woerner <twoerner@redhat.com> 2.2.32-2
- spec file cleanup
- mark po files as lang specific

* Sun Nov 06 2005 Florian La Roche <laroche@redhat.com>
- 2.2.32

* Wed Sep 28 2005 Than Ngo <than@redhat.com> 2.2.31-1
- update to 2.2.31

* Wed Sep 28 2005 Than Ngo <than@redhat.com> 2.2.23-9
- get rid of *.la files
- remove duplicate doc files

* Wed Feb  9 2005 Stephen C. Tweedie <sct@redhat.com> 2.2.23-6
- Rebuild

* Thu Sep 16 2004 Jeremy Katz <katzj@redhat.com> - 2.2.23-5
- make the libs executable so that we find their dependencies (#132696)

* Fri Sep 10 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.23-4
- libacl-devel Requires: libattr-devel for libattr.la

* Fri Sep 10 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.23-3
- Requires libtool >= 1.5 for building

* Thu Aug 19 2004 Phil Knirsch <pknirsch@redhat.com> 2.2.23-2
- Make libacl.so.* executable.

* Thu Aug 19 2004 Phil Knirsch <pknirsch@redhat.com> 2.2.23-1
- Update to latest upstream version.

* Sun Aug  8 2004 Alan Cox <alan@redhat.com> 2.2.7-7
- Close bug #125300 (Steve Grubb: build requires libtool,gettext)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 31 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.7-5
- Add missing %%defattr

* Tue Mar 30 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.7-3
- Add /usr/include/acl to files manifest
- Fix location of doc files, add main doc dir to files manifest

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Aug  5 2003 Elliot Lee <sopwith@redhat.com> 2.2.7-2
- Fix libtool invocation

* Tue Jun  3 2003 Stephen C. Tweedie <sct@redhat.com> 2.2.7-1
- Update to acl-2.2.7

* Wed Mar 26 2003 Michael K. Johnson <johnsonm@redhat.com> 2.2.3-2
- include patch from Jay Berkenbilt to print better error messages

* Tue Jan 28 2003 Michael K. Johnson <johnsonm@redhat.com> 2.2.3-1
- udpate/rebuild

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 2.0.11-7
- set execute bits on library so that requires are generated.

* Tue Nov 19 2002 Elliot Lee <sopwith@redhat.com> 2.0.11-5
- Correct patch in previous fix so that shared libraries go in /lib* 
  instead of /usr/lib*

* Tue Nov 19 2002 Elliot Lee <sopwith@redhat.com> 2.0.11-4
- Fix multilibbing

* Wed Sep 11 2002 Than Ngo <than@redhat.com> 2.0.11-3
- Added fix to install libs in correct directory on 64bit machine

* Thu Aug 08 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.11-2
- Made the package only own the one directory that is unique to it:
  /usr/include/acl

* Mon Jun 24 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.11-1
- Initial Red Hat package
  Made as few changes as possible relative to upstream packaging to
  make it easier to maintain long-term.  This means that some of
  the techniques used here are definitely not standard Red Hat
  techniques.  If you are looking for an example package to fit
  into Red Hat Linux transparently, this would not be the one to
  pick.
- acl-devel -> libacl-devel
