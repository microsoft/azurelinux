%define libsepolver 3.5-1
%define libselinuxver 3.5-1
Summary:        SELinux binary policy manipulation library
Name:           libsemanage
Version:        3.5
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/SELinuxProject/selinux/wiki
Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        semanage.conf
BuildRequires:  audit-devel
BuildRequires:  bison
BuildRequires:  bzip2
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  libselinux-devel >= %{libselinuxver}
BuildRequires:  libsepol-devel >= %{libsepolver}
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  swig
Requires:       audit-libs
Requires:       bzip2-libs
Requires:       libselinux%{?_isa} >= %{libselinuxver}
Provides:       libsemanage.so.1

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libsemanage provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package devel
Summary:        Header files and libraries used to build policy manipulation tools
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description devel
The semanage-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies.

%package python3
Summary:        semanage python 3 bindings for libsemanage
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libselinux-python3 >= %{libselinuxver}
Provides:       python3-%{name} = %{version}-%{release}

%description python3
The libsemanage-python3 package contains the python 3 bindings for developing
SELinux management applications.

%prep
%autosetup -p2

%build
%make_build clean
%make_build swigify CFLAGS="%{build_cflags} -Wno-error=strict-overflow -fno-semantic-interposition"
%make_build LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" all
%make_build LIBDIR="%{_libdir}" PYTHON=%{python3} pywrap

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_sharedstatedir}/selinux
mkdir -p %{buildroot}%{_sharedstatedir}/selinux/tmp
make DESTDIR=%{buildroot} LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" PYTHON=%{_bindir}/python3 install install-pywrap

cp %{SOURCE1} %{buildroot}%{_sysconfdir}/selinux/semanage.conf
ln -sf  %{_libdir}/libsemanage.so.2 %{buildroot}/%{_libdir}/libsemanage.so

%ldconfig_scriptlets

%files
%license LICENSE
%dir %{_sysconfdir}/selinux
%config(noreplace) %{_sysconfdir}/selinux/semanage.conf
%{_libdir}/libsemanage.so.2
%{_mandir}/man5/*
%{_mandir}/ru/man5/*
%dir %{_libexecdir}/selinux
%dir %{_sharedstatedir}/selinux
%dir %{_sharedstatedir}/selinux/tmp

%files devel
%{_libdir}/libsemanage.so
%{_libdir}/pkgconfig/libsemanage.pc
%dir %{_includedir}/semanage
%{_includedir}/semanage/*.h
%{_libdir}/libsemanage.a
%{_mandir}/man3/*

%files python3
%{python3_sitelib}/*.so
%{python3_sitelib}/semanage.py*
%{python3_sitelib}/__pycache__/semanage.cpython*.pyc
%{_libexecdir}/selinux/semanage_migrate_store

%changelog
* Fri Nov 24 2023 Andrew Phelps <anphel@microsoft.com> - 3.5-1
- Upgrade to version 3.5

* Wed Aug 10 2022 Chris PeBenito <chpebeni@microsoft.com> - 3.2-2
- Do not ignore /root for genhomedircon, otherwise it will not
- get correct labeling.

* Fri Aug 13 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.2-1
- Upgrade to latest upstream version and rebase patch
- Add -fno-semantic-interposition to CFLAGS as recommended by upstream
- Add static subpackage provides to devel subpackage
- Update source URL to new format
- Lint spec
- License verified

* Tue Aug 25 2020 Daniel Burgener <daburgen@microsoft.com> - 2.9-4
- Initial CBL-Mariner import from Fedora 31 (license: MIT)
- License verified

* Tue Aug 13 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-3
- Drop python2-libsemanage (#1738466)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 18 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-1
- SELinux userspace 2.9 release

* Mon Mar 11 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc2.1
- SELinux userspace 2.9-rc2 release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-0.rc1.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc1.1
- SELinux userspace 2.9-rc1 release

* Mon Jan 21 2019 Petr Lautrbach <plautrba@redhat.com> - 2.8-8
- Always set errno to 0 before calling getpwent()
- Set selinux policy root around calls to selinux_boolean_sub

* Mon Dec 10 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-7
- genhomedircon - improve handling large groups

* Tue Nov 13 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-6
- Fix RESOURCE_LEAK and USE_AFTER_FREE coverity scan defects

* Mon Sep 17 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-5
- Include user name in ROLE_REMOVE audit events

* Tue Sep  4 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-4
- Reset umask before creating directories (#1186422)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.8-2
- Rebuilt for Python 3.7

* Fri May 25 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-1
- SELinux userspace 2.8 release

* Mon May 14 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc3.1
- SELinux userspace 2.8-rc3 release candidate

* Fri May  4 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc2.1
- SELinux userspace 2.8-rc2 release candidate

* Mon Apr 23 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc1.1
- SELinux userspace 2.8-rc1 release candidate

* Wed Mar 21 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-12
- build: Replace PYSITEDIR with PYTHONLIBDIR
- direct_api.c: Fix iterating over array (#1557468)

* Fri Mar 16 2018 Petr Lautrbach <plautrba@workstation> - 2.7-11
- Revert "remove access() check to make setuid programs work" (#1557468)

* Tue Mar 13 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-10
- properly check return value of iterate function
- Use umask(0077) for fopen() write operations
- Return commit number if save-previous false
- Allow tmp files to be kept if a compile fails
- build: follow standard semantics for DESTDIR and PREFIX
- Improve warning for installing disabled module
- silence clang static analyzer report
- remove access() check to make setuid programs work

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.7-9
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.7-7
- Switch to %%ldconfig_scriptlets

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.7-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Nov 22 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-5
- free genhomedircon fallback user
- Rebuild with libsepol-2.7-3 and libselinux-2.7-6

* Fri Oct 20 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-4
- Add support for listing fcontext.homedirs file (#1409813)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.7-3
- Add Provides for the old names without %%_isa

* Thu Aug 10 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.7-2
- Python 2 binary package renamed to python2-libsemanage
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3
- Python 3 binary package renamed to python3-libsemanage

* Mon Aug 07 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-1
- Update to upstream release 2017-08-04
- Use 'sefcontext_compile -r' when it's run during SELinux policy build

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 28 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-4
- Follow upstream and rename _semanage.so to _semanage.cpython-36m-x86_64-linux-gnu.so

* Tue Apr 18 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-3
- Do not list duplicate port entries after setting a boolean (#1439875)

* Thu Mar 02 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-2
- Fix FTBFS - fatal error (#1427903)

* Mon Feb 20 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-1.1
- Update to upstream release 2016-10-14

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.5-9
- Rebuild for Python 3.6

* Mon Oct 03 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-8
- Fixes bug preventing the installation of base modules
- make distclean target work
- Do not always print a module name warning
- Use pp module name instead of filename when installing module
- tests: Do not force using gcc
- genhomedircon: remove hardcoded refpolicy strings
- genhomedircon: add support for %%group syntax
- genhomedircon: generate contexts for logins mapped to the default user
- Validate and compile file contexts before installing
- Swap tcp and udp protocol numbers

* Mon Aug 01 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-7
- Rebuilt with libsepol-2.5-9 and libselinux-2.5-11

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 23 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-5
- Sort object files for deterministic linking order
- Support overriding Makefile RANLIB
- Respect CC and PKG_CONFIG environment variable

* Fri May 06 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-4
- Fix multiple spelling errors
- genhomedircon: %%{USERID} and %%{USERNAME} support and code cleanup

* Mon Mar 21 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-3
- Enable expand-check by default (#1319652)

* Sun Feb 28 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-2
- Use fully versioned arch-specific requires

* Tue Feb 23 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-1
- Update to upstream release 2016-02-23

* Sun Feb 21 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-0.1.rc1
- Update to upstream rc1 release 2016-01-07

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 2.4-5
- Rebuilt for Python3.5 rebuild

* Fri Sep 04 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-4
- Save homedir_template in the policy store for genhomedircon
  https://bugs.gentoo.org/558686

* Fri Aug 14 2015 Adam Jackson <ajax@redhat.com> 2.4-3
- Pass ldflags into the build so hardening works

* Thu Jul 30 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-2
- semanage_migrate_store: use /usr/bin/python3
- move semanage_migrate_store script to libsemanage-python3

* Wed Jun 24 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-0.6
- Allow to use compressed modules without a compression extension

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 16 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-0.5
- add /var/lib/selinux/tmp directory

* Tue May 12 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-0.4
- semanage_migrate_store: add -r <root> option for migrating inside chroots

* Mon Apr 13 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-0.3
- Update to upstream release 2.4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Miroslav Grepl <mgrepl@fedoraproject.org> - 2.3-5
- Skip policy module re-link when only setting booleans.
    * patch from Stephen Smalley

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.3-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue May 6 2014 Dan Walsh <dwalsh@redhat.com> - 2.3-1
- Update to upstream 
	* Fix memory leak in semanage_genhomedircon from Thomas Hurd.

* Sun Mar 30 2014 Dan Walsh <dwalsh@redhat.com> - 2.2-3
- libsemanage: fix memory leak in semanage_genhomedircon
- Patch from THomas Hurd

* Tue Feb 11 2014 Dan Walsh <dwalsh@redhat.com> - 2.2-2
- Move semanage.conf man page from devel package to main package

* Thu Oct 31 2013 Dan Walsh <dwalsh@redhat.com> - 2.2-1
- Update to upstream 
	* Avoid duplicate list entries from Dan Walsh.
	* Add audit support to libsemanage from Dan Walsh.
	* Remove policy.kern and replace with symlink from Dan Walsh.
	* Apply a MAX_UID check for genhomedircon from Laurent Bigonville.
	* Fix man pages from Laurent Bigonville.

* Wed Oct 16 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-14
- Cleanup handling of missing mls_range to fix problems with useradd -Z
- Fix auditing of login record changes, roles were not working correctly.
Resolves: #952237

* Fri Oct 4 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-13
- Fix errors found by coverity
Resolves: #952237

* Wed Sep 25 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-12
- Do not fail on missing SELinux User Record when adding login record

* Mon Sep 23 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-11
- Add msg to audit records

* Thu Sep 19 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-10
- Do not write error message to screen when looking for previous record for auditing.
- Add mls_range from user record if the MLS range is not specified by the seuser add record.
- Error out if seuser or mls range is not specified when adding user records

* Mon Sep 9 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-9
- Create symlink from policy.kern to active kernel.

* Fri Sep 6 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-8
- Unlink policy.kern when done to save space.

* Fri Jul 26 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-7
- Move handling of role audit records into the library
- Patch stops semanage from removing user record while in use

* Tue Jul 9 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-6
- Remove dependance on selinux-policy, /etc/selinux should be owned by libsemanage, and selinux-policy can require it.

* Fri Jun 28 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-5
- Allways build python3 version

* Mon Apr 22 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-4
- 

* Thu Apr 11 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-3
- Fix test suite to build

* Thu Feb 14 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-2
- Revert some changes which are causing the wrong policy version file to be created

* Thu Feb 7 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.10-1
- Update to upstream 
	* Add sefcontext_compile to compile regex everytime policy is rebuilt
	* Cleanup/fix enable/disable/remove module.
	* redo genhomedircon minuid
	* fixes from coverity
	* semanage_store: do not leak memory in semanage_exec_prog
	* genhomedircon: remove useless conditional in get_home_dirs
	* genhomedircon: double free in get_home_dirs
	* fcontext_record: do not leak on error in semanage_fcontext_key_create
	* genhomedircon: do not leak on failure in write_gen_home_dir_context
	* semanage_store: do not leak fd 
	* genhomedircon: do not leak shells list
	* semanage_store: do not leak on strdup failure 
	* semanage_store: rewrite for readability

* Wed Jan 16 2013 Dan Walsh <dwalsh@redhat.com> 2.1.9-4
- Add selinux-policy as a requires to get /etc/selinux owned

* Sat Jan 5 2013 Dan Walsh <dwalsh@redhat.com> 2.1.9-3
- Update to latest patches from eparis/Upstream
-    libsemanage: fixes from coverity
-    libsemange: redo genhomedircon minuid

* Wed Nov 21 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-2
- Fix handling of missing semanage permissive -d foo, not failing correctly
- Previous to this fix the first module beginning with foo would get deleted.

* Thu Sep 13 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-1
- Update to upstream 
	* libsemanage: do not set soname needlessly
	* libsemanage: remove PYTHONLIBDIR and ruby equivalent
	* do boolean name substitution
	* Fix segfault for building standard policies.

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 2.1.8-6
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Wed Aug  1 2012 David Malcolm <dmalcolm@redhat.com> - 2.1.8-5
- remove rhel logic from with_python3 conditional

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.8-3
- Attempt to allocate memory for selinux_binary_policy_path and free memory 
- allocated by asprintf.

* Thu Jul 12 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.8-2
- Fix asprintf within an asprintf call

* Wed Jul 4 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.8-1
- Update to upstream 
	* remove build warning when build swig c files
	* additional makefile support for rubywrap
	* ignore 80 column limit for readability
	* semanage_store: fix snprintf length argument by using asprintf
	* Use default semanage.conf as a fallback
	* use after free in python bindings

* Tue May 29 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.7-2
- Apply patch from Sven Vermeulen to fix problem with python3 bindings.

* Thu Mar 29 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.7-1
- Update to upstream 
	* Alternate path for semanage.conf
	* do not link against libpython, this is considered bad in Debian
	* Allow to build for several ruby version
	* fallback-user-level

* Wed Feb 15 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.6-3
- Check in correct patch.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jan 6 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.6-2
- Add patch form Xin Ouyang to make library use private semanage.conf 

* Wed Dec 21 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.6-1
-Update to upstream
	* add ignoredirs config for genhomedircon
	* Fallback_user_level can be NULL if you are not using MLS

* Thu Dec 15 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-4
- Rebuild with latest libsepol

* Thu Dec 15 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-3
- Rebuild with latest libsepol

* Thu Dec 15 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-2
- Add support for ignoredirs param in /etc/selinux/semanage.conf

* Fri Nov 4 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-1
- Upgrade to upstream
	* regenerate .pc on VERSION change
	* maintain mode even if umask is tighter
	* semanage.conf man page
	* create man5dir if not exist

* Wed Oct 19 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-2
-    Fix handling of umask, so files get created with the correct label.

* Mon Sep 19 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-2
-    Add Guido Trentalancia semanage.conf man page

* Mon Sep 19 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-1
-Update to upstream
	* Create a new preserve_tunables flag
	* tree: default make target to all not
	* fix semanage_store_access_check calling arguments

* Wed Sep 14 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.3-2
- Add support for preserving tunables

* Tue Aug 30 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.3-1
-Update to upstream
	* python wrapper makefile changes

* Thu Aug 18 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.2-1
-Update to upstream
2.1.2 2011-08-17
	* print error debug info for buggy fc
	* introduce semanage_set_root and friends
	* throw exceptions in python rather than return
	* python3 support.
	* patch for MCS/MLS in user files
2.1.1 2011-08-01
	* Remove generated files, expand .gitignore
	* Use -Werror and change a few prototypes to support it

* Thu Jul 28 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.0-1
- Update to upstream
	* Release, minor version bump

* Wed Jun 8 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.46-6
- More fixes for disabled modules

* Tue Jun 7 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.46-5
- Change libsemanage mechanism for handling disabled modules. Now it will only create a flag for a module 
indicating the module is disabled.  MODULE.pp.disabled, it will no longer rename the module.  This way we can
ship active modules in rpm.

* Wed Jun 1 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.46-4
- Add semanage_set_selinux_path, to allow semodule to work on alternate selinux pools

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.46-2
- big reworking of the support-multiple-python-builds patch to deal with
PEP 3149: the latest Python 3.2 onwards uses include paths and library names
that don't fit prior naming patterns, and so we must query python3-config for
this information.  To complicate things further, python 2's python-config
doesn't understand all of the options needed ("--extension-suffix").  I've
thus added new Makefile variables as needed, to be supplied by the specfile by
invoking the appropriate config tool (or by hardcoding the old value for
"--extension-suffix" i.e. ".so")
- rework python3 manifest for PEP 3149, and rebuild for newer python3

* Tue Dec 21 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.46-1
- Update to upstream
  * Fix compliation under GCC 4.6 by Justin Mattock

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.45-6
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.45-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 27 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.45-4
- add python3 subpackage

* Wed Apr 7 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.45-3
- Fix -devel package to point at the correct shared library

* Fri Mar 26 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.45-2
- Move shared library to /usr/lib

* Mon Mar 8 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.45-1
- Update to upstream
	* Add enable/disable patch support from Dan Walsh.
	* Add usepasswd flag to semanage.conf to disable genhomedircon using
	  passwd from Dan Walsh.
	* regenerate swig wrappers

* Thu Feb 25 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.44-2
- Allow disable of usepasswd

* Wed Feb 17 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.44-1
- Update to upstream
	* Replace usage of fmemopen() with sepol_policy_file_set_mem() since
	  glibc < 2.9 does not support binary mode ('b') for fmemopen'd
	  streams.

* Thu Jan 28 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.43-4
- Cleanup spec file

* Mon Jan 18 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.43-3
- Splect libsemanage.a into a static subpackage to keep fedora packaging guidelines happy

* Wed Dec 16 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.43-2
- Rebuild all c programs with -fPIC

* Tue Dec 1 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.43-1
- Update to upstream
  * Move libsemanage.so to /usr/lib
  * Add NAME lines to man pages from Manoj Srivastava<srivasta@debian.org>

* Wed Nov 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.42-1
- Update to upstream
  * Move load_policy from /usr/sbin to /sbin from Dan Walsh.

* Mon Nov 2 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.41-1
- Update to upstream
  * Add pkgconfig file from Eamon Walsh.
  * Add semanage_set_check_contexts() function to disable calling
  setfiles

* Mon Sep 28 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.39-1
- Update to upstream
  * make swigify

* Sun Sep 20 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.38-2
- Dont relabel /root with genhomedircon

* Thu Sep 17 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.38-1
- Update to upstream
  * Change semodule upgrade behavior to install even if the module
    is not present from Dan Walsh.
  * Make genhomedircon trim excess '/' from homedirs from Dan Walsh.

* Wed Sep 9 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.37-1
- Update to upstream
  * Fix persistent dontaudit support to rebuild policy if the 
        dontaudit state is changed from Chad Sellers.
- Move load_policy to /sbin

* Fri Aug 28 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.36-2
- Add enable/disable modules

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.36-1
- Update to upstream
  * Changed bzip-blocksize=0 handling to support existing compressed
  modules in the store.

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.35-2
- Make sure /root is not used in genhomedircon

* Wed Aug 5 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.35-1
- Revert hard linking of files between tmp/active/previous.
- Enable configuration of bzip behavior from Stephen Smalley.
-   bzip-blocksize=0 to disable compression and decompression support.
-   bzip-blocksize=1..9 to set the blocksize for compression.
-   bzip-small=true to reduce memory usage for decompression.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.33-2
- Put check for /root back into genhomedircon

* Tue Jul 7 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.33-1
- Update to upstream

* Mon Jun 8 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.32-1
- Update to upstream
  * Ruby bindings from David Quigley.

* Thu Apr 9 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.31-5
- Return error on invalid file

* Wed Mar 11 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.31-4
- Fix typo

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.31-2
- Fix link to only link on sandbox

* Mon Jan 12 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.31-1
- Update to upstream
  * Policy module compression (bzip) support from Dan Walsh.
  * Hard link files between tmp/active/previous from Dan Walsh.

* Mon Jan 12 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.30-3
- Fix up patch to get it upstreamed

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.30-2
- Rebuild for Python 2.6

* Thu Dec 4 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.30-1
- Add semanage_mls_enabled() interface from Stephen Smalley.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.29-2
- Rebuild for Python 2.6

* Mon Sep 15 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.28-1
- Update to upstream
  * Add USER to lines to homedir_template context file from Chris PeBenito.

* Mon Sep 15 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.28-2
- Add compression support

* Mon Sep 15 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.28-1
- Update to upstream
  * allow fcontext and seuser changes without rebuilding the policy from Dan Walsh

* Wed Sep 10 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.27-3
- Additional fixes for Don't rebuild on fcontext or seuser modifications

* Tue Sep 2 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.27-2
- Don't rebuild on fcontext or seuser modifications

* Tue Aug 5 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.27-1
- Update to upstream
  * Modify genhomedircon to skip groupname entries.
  Ultimately we need to expand them to the list of users to support per-role homedir labeling when using the groupname syntax.

* Tue Jul 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.26-1
- Update to upstream
  * Fix bug in genhomedircon fcontext matches logic from Dan Walsh.
  Strip any trailing slash before appending /*$.

* Tue Jun 17 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.25-3
- Another fix for genhomedircon

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.25-2
- fix license tag

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.25-1
- Update to upstream
  * Do not call genhomedircon if the policy was not rebuilt from Stephen Smalley.
    Fixes semanage boolean -D seg fault (bug 441379).

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.24-1
- Update to upstream
  * make swigify

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.23-1
- Update to upstream
  * Use vfork rather than fork for libsemanage helpers to reduce memory overhead as suggested by Todd Miller.

* Mon Feb 4 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.22-1
- Update to upstream
  * Free policydb before fork from Joshua Brindle.
  * Drop the base module immediately after expanding to permit memory re-use from Stephen Smalley.

* Sat Feb 2 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.20-1
- Update to upstream
  * Use sepol_set_expand_consume_base to reduce peak memory usage when
  using semodule

* Fri Feb 1 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.19-1
- Update to upstream
  * Fix genhomedircon to not override a file context with a homedir context from Todd Miller.

* Tue Jan 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.18-1
- Update to upstream
  * Fix spurious out of memory error reports.
  * Merged second version of fix for genhomedircon handling from Caleb Case.

* Tue Jan 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.16-1
- Update to upstream
  * Merged fix for genhomedircon handling of missing HOME_DIR or HOME_ROOT templates from Caleb Case.

* Tue Jan 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.15-2
- Stop differentiating on user for homedir labeling

* Thu Dec 6 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.15-1
- Update to upstream
  * Fix genhomedircon handling of shells and missing user context template from Dan Walsh.
  * Copy the store path in semanage_select_store from Dan Walsh.
- Add expand-check=0 to semanage.conf

* Mon Dec 3 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.14-5
- Fix handling of /etc/shells so genhomedircon will work

* Thu Nov 29 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.14-3
- Allow semanage_genhomedircon to work with out a USER int homedir.template

* Sat Nov 10 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.14-2
- Fix semanage_select_store to allocate memory, fixes crash on invalid store

* Tue Nov 6 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.14-1
- Upgrade to latest from NSA
  * Call rmdir() rather than remove() on directory removal so that errno isn't polluted from Stephen Smalley.
  * Allow handle_unknown in base to be overridden by semanage.conf from Stephen Smalley.

* Fri Oct 5 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.12-1
- Upgrade to latest from NSA
  * ustr cleanups from James Antill.
  * Ensure that /root gets labeled even if using the default context from Dan Walsh.

* Fri Sep 28 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.11-1
- Upgrade to latest from NSA
  * Fix ordering of file_contexts.homedirs from Todd Miller and Dan Walsh.

* Fri Sep 28 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.10-2
- Fix sort order on generated homedir context

* Fri Sep 28 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.10-1
- Upgrade to latest from NSA
  * Fix error checking on getpw*_r functions from Todd Miller.
  * Make genhomedircon skip invalid homedir contexts from Todd Miller.
  * Set default user and prefix from seusers from Dan Walsh.
  * Add swigify Makefile target from Dan Walsh.

* Wed Sep 26 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.9-1
- Upgrade to latest from NSA
  * Pass CFLAGS to CC even on link command, per Dennis Gilmore.
  * Clear errno on non-fatal errors to avoid reporting them upon a
    later error that does not set errno.
  * Improve reporting of system errors, e.g. full filesystem or read-only filesystem from Stephen Smalley.
- Fix segfault in genhomedircon when using bad user names

* Wed Sep 26 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.6-2
- Fix genhomedircon code to only generate valid context
- Fixes autorelabel problem

* Thu Sep 13 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.6-1
- Upgrade to latest from NSA
  * Change to use getpw* function calls to the _r versions from Todd Miller.

* Thu Aug 23 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.5-1
- Upgrade to latest from NSA

* Mon Aug 20 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.4-1
- Upgrade to latest from NSA
  * Allow dontaudits to be turned off via semanage interface when
    updating policy

* Sat Aug 11 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-5
- Add ability to load a policy without dontaudit rules
-

* Tue Jun 26 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-4
- Rebuild to fix segfault on x86 platforms, swigify on each build

* Fri Jun 1 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-3
- Rebuild for rawhide

* Thu May 3 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-2
- Apply patch to fix dependencies in spec file from Robert Scheck

* Wed Apr 25 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-1
- Upgrade to latest from NSA
  * Fix to libsemanage man patches so whatis will work better from Dan Walsh

* Wed Apr 25 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.2-1
- Upgrade to latest from NSA
- Merged optimizations from Stephen Smalley.
-    do not set all booleans upon commit, only those whose values have changed
-    only install the sandbox upon commit if something was rebuilt

* Sat Mar 17 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.1-2
- Add SELinux to Man page Names so man -k will work

* Mon Mar 12 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.1-1
- Merged dbase_file_flush patch from Dan Walsh.
- This removes any mention of specific tools (e.g. semanage)
- from the comment header of the auto-generated files,
- since there are multiple front-end tools.

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.0-1
- Upgrade to latest from NSA
  * Merged Makefile test target patch from Caleb Case.
  * Merged get_commit_number function rename patch from Caleb Case.
  * Merged strnlen -> strlen patch from Todd Miller.

* Wed Feb 7 2007 Dan Walsh <dwalsh@redhat.com> - 1.10.1-1
- Upgrade to latest from NSA
  * Merged python binding fix from Dan Walsh.
  * Updated version for stable branch.

* Fri Dec 22 2006 Dan Walsh <dwalsh@redhat.com> - 1.9.2-1
- Upgrade to latest from NSA
  * Merged patch to optionally reduce disk usage by removing 
    the backup module store and linked policy from Karl MacMillan
  * Merged patch to correctly propagate return values in libsemanage

* Fri Dec 22 2006 Dan Walsh <dwalsh@redhat.com> - 1.9.1-3
- Apply Karl MacMillan patch to get proper error codes.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.9.1-2
- rebuild against python 2.5

* Tue Nov 28 2006 Dan Walsh <dwalsh@redhat.com> - 1.9.1-1
- Upgrade to latest from NSA
  * Merged patch to compile wit -fPIC instead of -fpic from
    Manoj Srivastava to prevent hitting the global offest table
    limit. Patch changed to include libselinux and libsemanage in
    addition to libsepol.

* Tue Oct 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.8-1
- Upgrade to latest from NSA
  * Updated version for release.

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.17-1
- Upgrade to latest from NSA
  * Merged patch to skip reload if no active store exists and
    the store path doesn't match the active store path from Dan Walsh.
  * Merged patch to not destroy sepol handle on error path of
    connect from James Athey.
  * Merged patch to add genhomedircon path to semanage.conf from
    James Athey. 

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.16-3
- Fix semanage to not load if is not the correct policy type and it is installing

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.16-2
- Fix requires lines

* Wed Aug 23 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.16-1
- Upgrade to latest from NSA
  * Make most copy errors fatal, but allow exceptions for
    file_contexts.local, seusers, and netfilter_contexts if
    the source file does not exist in the store.

* Sat Aug 12 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.15-1
- Upgrade to latest from NSA
  * Merged separate local file contexts patch from Chris PeBenito.
  * Merged patch to make most copy errors non-fatal from Dan Walsh.

* Thu Aug 10 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.13-3
- Change other updates to be non-fatal

* Wed Aug 9 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.13-2
- Change netfilter stuff to be non-fatal so update can proceed.

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.13-1
- Upgrade to latest from NSA
  * Merged netfilter contexts support from Chris PeBenito.

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.12-2
- Rebuild for new gcc

* Tue Jul 11 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.12-1
- Upgrade to latest from NSA
  * Merged support for read operations on read-only fs from 
    Caleb Case (Tresys Technology).

* Tue Jul 4 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.11-1
- Upgrade to latest from NSA
  * Lindent.
  * Merged setfiles location check patch from Dan Walsh.

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.9-1
- Upgrade to latest from NSA
  * Merged several fixes from Serge Hallyn:
       dbase_file_cache:  deref of uninit data on error path.
       dbase_policydb_cache:  clear fp to avoid double fclose
       semanage_fc_sort:  destroy temp on error paths

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.8-2
- Handle setfiles being in /sbin or /usr/sbin

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.8-1
- Upgrade to latest from NSA
  * Updated default location for setfiles to /sbin to
    match policycoreutils.  This can also be adjusted via 
    semanage.conf using the syntax:
    [setfiles]
    path = /path/to/setfiles
    args = -q -c $@ $<
    [end]

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.7-3
- Spec file cleanup from n0dalus+redhat@gmail.com

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.7-2
- Add /usr/include/semanage to spec file

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.7-1
- Upgrade to latest from NSA
  * Merged fix warnings patch from Karl MacMillan.

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.6-1
- Upgrade to latest from NSA
  * Merged updated file context sorting patch from Christopher
    Ashworth, with bug fix for escaped character flag.
  * Merged file context sorting code from Christopher Ashworth 
    (Tresys Technology), based on fc_sort.c code in refpolicy.
  * Merged python binding t_output_helper removal patch from Dan Walsh.
  * Regenerated swig files.

* Wed Mar 29 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.3-1
- Fix to work with new version of swig
- Upgrade to latest from NSA
  * Merged corrected fix for descriptor leak from Dan Walsh.

* Wed Mar 29 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.2-2
- Fix leaky descriptor

* Tue Mar 21 2006 Dan Walsh <dwalsh@redhat.com> - 1.6.2-1
- Upgrade to latest from NSA
  * Merged Makefile PYLIBVER definition patch from Dan Walsh.
  * Merged man page reorganization from Ivan Gyurdiev.

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.6-1
- Make work on RHEL4
- Upgrade to latest from NSA
  * Merged abort early on merge errors patch from Ivan Gyurdiev.
  * Cleaned up error handling in semanage_split_fc based on a patch
    by Serge Hallyn (IBM) and suggestions by Ivan Gyurdiev.
  * Merged MLS handling fixes from Ivan Gyurdiev.

* Fri Feb 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.5.28-1
- Upgrade to latest from NSA
  * Merged bug fix for fcontext validate handler from Ivan Gyurdiev.
  * Merged base_merge_components changes from Ivan Gyurdiev.

* Thu Feb 16 2006 Dan Walsh <dwalsh@redhat.com> - 1.5.26-1
- Upgrade to latest from NSA
  * Merged paths array patch from Ivan Gyurdiev.
  * Merged bug fix patch from Ivan Gyurdiev.
  * Merged improve bindings patch from Ivan Gyurdiev.
  * Merged use PyList patch from Ivan Gyurdiev.  
  * Merged memory leak fix patch from Ivan Gyurdiev.
  * Merged nodecon support patch from Ivan Gyurdiev.
  * Merged cleanups patch from Ivan Gyurdiev.
  * Merged split swig patch from Ivan Gyurdiev.

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> - 1.5.23-1
- Upgrade to latest from NSA
  * Merged optionals in base patch from Joshua Brindle.
  * Merged treat seusers/users_extra as optional sections patch from
    Ivan Gyurdiev.
  * Merged parse_optional fixes from Ivan Gyurdiev.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.5.21-2.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Dan Walsh <dwalsh@redhat.com> - 1.5.21-2
- Fix handling of seusers and users_map file

* Tue Feb 07 2006 Dan Walsh <dwalsh@redhat.com> - 1.5.21-1
- Upgrade to latest from NSA
  * Merged seuser/user_extra support patch from Joshua Brindle.
  * Merged remote system dbase patch from Ivan Gyurdiev.  

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.5.20-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 2 2006 Dan Walsh <dwalsh@redhat.com> 1.5.20-1
- Upgrade to latest from NSA
  * Merged clone record on set_con patch from Ivan Gyurdiev.  

* Mon Jan 30 2006 Dan Walsh <dwalsh@redhat.com> 1.5.19-1
- Upgrade to latest from NSA
  * Merged fname parameter patch from Ivan Gyurdiev.
  * Merged more size_t -> unsigned int fixes from Ivan Gyurdiev.
  * Merged seusers.system patch from Ivan Gyurdiev.
  * Merged improve port/fcontext API patch from Ivan Gyurdiev.  

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 1.5.18-1
- Upgrade to latest from NSA
  * Merged seuser -> seuser_local rename patch from Ivan Gyurdiev.
  * Merged set_create_store, access_check, and is_connected interfaces
    from Joshua Brindle.

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.5.16-1
- Upgrade to latest from NSA
  * Regenerate python wrappers.

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.5.15-1
- Upgrade to latest from NSA
  * Merged pywrap Makefile diff from Dan Walsh.
  * Merged cache management patch from Ivan Gyurdiev.
  * Merged bugfix for dbase_llist_clear from Ivan Gyurdiev.
  * Merged remove apply_local function patch from Ivan Gyurdiev.
  * Merged only do read locking in direct case patch from Ivan Gyurdiev.
  * Merged cache error path memory leak fix from Ivan Gyurdiev.
  * Merged auto-generated file header patch from Ivan Gyurdiev.
  * Merged pywrap test update from Ivan Gyurdiev.
  * Merged hidden defs update from Ivan Gyurdiev.

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.5.14-2
- Break out python out of regular Makefile

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.5.14-1
- Upgrade to latest from NSA
  * Merged disallow port overlap patch from Ivan Gyurdiev.
  * Merged join prereq and implementation patches from Ivan Gyurdiev.
  * Merged join user extra data part 2 patch from Ivan Gyurdiev.
  * Merged bugfix patch from Ivan Gyurdiev.
  * Merged remove add_local/set_local patch from Ivan Gyurdiev.
  * Merged user extra data part 1 patch from Ivan Gyurdiev.
  * Merged size_t -> unsigned int patch from Ivan Gyurdiev.
  * Merged calloc check in semanage_store patch from Ivan Gyurdiev,
    bug noticed by Steve Grubb.
  * Merged cleanups after add/set removal patch from Ivan Gyurdiev.

* Sat Jan 7 2006 Dan Walsh <dwalsh@redhat.com> 1.5.9-1
- Upgrade to latest from NSA
  * Merged const in APIs patch from Ivan Gyurdiev.
  * Merged validation of local file contexts patch from Ivan Gyurdiev.
  * Merged compare2 function patch from Ivan Gyurdiev.
  * Merged hidden def/proto update patch from Ivan Gyurdiev.

* Fri Jan 6 2006 Dan Walsh <dwalsh@redhat.com> 1.5.8-1
- Upgrade to latest from NSA
  * Re-applied string and file optimization patch from Russell Coker,
    with bug fix.
  * Reverted string and file optimization patch from Russell Coker.
  * Clarified error messages from parse_module_headers and 
    parse_base_headers for base/module mismatches.

* Fri Jan 6 2006 Dan Walsh <dwalsh@redhat.com> 1.5.6-1
- Upgrade to latest from NSA
  * Clarified error messages from parse_module_headers and 
    parse_base_headers for base/module mismatches.
  * Merged string and file optimization patch from Russell Coker.
  * Merged swig header reordering patch from Ivan Gyurdiev.
  * Merged toggle modify on add patch from Ivan Gyurdiev.
  * Merged ports parser bugfix patch from Ivan Gyurdiev.
  * Merged fcontext swig patch from Ivan Gyurdiev.
  * Merged remove add/modify/delete for active booleans patch from Ivan Gyurdiev.
  * Merged man pages for dbase functions patch from Ivan Gyurdiev.
  * Merged pywrap tests patch from Ivan Gyurdiev.

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.5.4-2
- Patch to fix add

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.5.4-1
- Upgrade to latest from NSA
  * Merged patch series from Ivan Gyurdiev.
    This includes patches to:
    - separate file rw code from linked list
    - annotate objects
    - fold together internal headers
    - support ordering of records in compare function
    - add active dbase backend, active booleans
    - return commit numbers for ro database calls
    - use modified flags to skip rebuild whenever possible
    - enable port interfaces
    - update swig interfaces and typemaps
    - add an API for file_contexts.local and file_contexts
    - flip the traversal order in iterate/list
    - reorganize sandbox_expand
    - add seusers MLS validation
    - improve dbase spec/documentation
    - clone record on set/add/modify

* Tue Dec 27 2005 Dan Walsh <dwalsh@redhat.com> 1.5.3-3
- Add Ivans patch to turn on ports

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 1.5.3-2
- Remove patch since upstream does the right thing

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 1.5.3-1
- Upgrade to latest from NSA
  * Merged further header cleanups from Ivan Gyurdiev.
  * Merged toggle modified flag in policydb_modify, fix memory leak
    in clear_obsolete, polymorphism vs headers fix, and include guards
    for internal headers patches from Ivan Gyurdiev.

* Tue Dec 13 2005 Dan Walsh <dwalsh@redhat.com> 1.5.1-2
- Upgrade to latest from NSA
  * Merged toggle modified flag in policydb_modify, fix memory leak
    in clear_obsolete, polymorphism vs headers fix, and include guards
    for internal headers patches from Ivan Gyurdiev.

* Mon Dec 12 2005 Dan Walsh <dwalsh@redhat.com> 1.5.1-1
- Upgrade to latest from NSA
  * Added file-mode= setting to semanage.conf, default to 0644.
    Changed semanage_copy_file and callers to use this mode when
    installing policy files to runtime locations.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.4-1
- Fix mode of output seusers file

* Tue Dec 6 2005 Dan Walsh <dwalsh@redhat.com> 1.3.64-1
- Upgrade to latest from NSA
  * Changed semanage_handle_create() to set do_reload based on
    is_selinux_enabled().  This prevents improper attempts to
    load policy on a non-SELinux system.

* Mon Dec 5 2005 Dan Walsh <dwalsh@redhat.com> 1.3.63-1
- Upgrade to latest from NSA
  * Dropped handle from user_del_role interface.
  * Removed defrole interfaces.

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 1.3.61-1
- Upgrade to latest from NSA
  * Merged Makefile python definitions patch from Dan Walsh.
  * Removed is_selinux_mls_enabled() conditionals in seusers and users
    file parsers. 

* Wed Nov 23 2005 Dan Walsh <dwalsh@redhat.com> 1.3.59-1
- Add additional swig objects
  * Merged wrap char*** for user_get_roles patch from Joshua Brindle.
  * Merged remove defrole from sepol patch from Ivan Gyurdiev.
  * Merged swig wrappers for modifying users and seusers from Joshua Brindle.

* Wed Nov 23 2005 Dan Walsh <dwalsh@redhat.com> 1.3.56-2
- Add additional swig objects

* Wed Nov 16 2005 Dan Walsh <dwalsh@redhat.com> 1.3.56-1
- Upgrade to latest from NSA
  * Fixed free->key_free bug.
  * Merged clear obsolete patch from Ivan Gyurdiev.
  * Merged modified swigify patch from Dan Walsh 
    (original patch from Joshua Brindle).
  * Merged move genhomedircon call patch from Chad Sellers.

* Mon Nov 14 2005 Dan Walsh <dwalsh@redhat.com> 1.3.53-3
- Add genhomedircon patch from Joshua Brindle

* Fri Nov 11 2005 Dan Walsh <dwalsh@redhat.com> 1.3.53-2
- Add swigify patch from Joshua Brindle

* Fri Nov 11 2005 Dan Walsh <dwalsh@redhat.com> 1.3.53-1
- Upgrade to latest from NSA
  * Merged move seuser validation patch from Ivan Gyurdiev.
  * Merged hidden declaration fixes from Ivan Gyurdiev,
    with minor corrections.

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 1.3.52-1
- Upgrade to latest from NSA
  * Merged cleanup patch from Ivan Gyurdiev.
    This renames semanage_module_conn to semanage_direct_handle,
    and moves sepol handle create/destroy into semanage handle
    create/destroy to allow use even when disconnected (for the
    record interfaces).

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.3.51-1
- Upgrade to latest from NSA
  * Clear modules modified flag upon disconnect and commit.
        * Added tracking of module modifications and use it to
    determine whether expand-time checks should be applied
    on commit.
  * Reverted semanage_set_reload_bools() interface.

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.3.48-1
- Upgrade to latest from NSA
  * Disabled calls to port dbase for merge and commit and stubbed
    out calls to sepol_port interfaces since they are not exported.
  * Merged rename instead of copy patch from Joshua Brindle (Tresys).
  * Added hidden_def/hidden_proto for exported symbols used within 
    libsemanage to eliminate relocations.  Wrapped type definitions
    in exported headers as needed to avoid conflicts.  Added
    src/context_internal.h and src/iface_internal.h.
  * Added semanage_is_managed() interface to allow detection of whether
    the policy is managed via libsemanage.  This enables proper handling
    in setsebool for non-managed systems.
  * Merged semanage_set_reload_bools() interface from Ivan Gyurdiev,
    to enable runtime control over preserving active boolean values
    versus reloading their saved settings upon commit.

* Mon Nov 7 2005 Dan Walsh <dwalsh@redhat.com> 1.3.43-1
- Upgrade to latest from NSA
  * Merged seuser parser resync, dbase tracking and cleanup, strtol
    bug, copyright, and assert space patches from Ivan Gyurdiev.
  * Added src/*_internal.h in preparation for other changes.
   * Added hidden/hidden_proto/hidden_def to src/debug.[hc] and
          src/seusers.[hc].

* Thu Nov 3 2005 Dan Walsh <dwalsh@redhat.com> 1.3.41-1
- Upgrade to latest from NSA
  * Merged interface parse/print, context_to_string interface change,
    move assert_noeof, and order preserving patches from Ivan Gyurdiev.
        * Added src/dso.h in preparation for other changes.
  * Merged install seusers, handle/error messages, MLS parsing,
    and seusers validation patches from Ivan Gyurdiev.

* Mon Oct 31 2005 Dan Walsh <dwalsh@redhat.com> 1.3.39-1
- Upgrade to latest from NSA
  * Merged record interface, dbase flush, common database code,
    and record bugfix patches from Ivan Gyurdiev.

* Fri Oct 28 2005 Dan Walsh <dwalsh@redhat.com> 1.3.38-1
- Upgrade to latest from NSA
  * Merged dbase policydb list and count change from Ivan Gyurdiev.
  * Merged enable dbase and set relay patches from Ivan Gyurdiev.

* Thu Oct 27 2005 Dan Walsh <dwalsh@redhat.com> 1.3.36-1
- Update from NSA
  * Merged query APIs and dbase_file_set patches from Ivan Gyurdiev.

* Wed Oct 26 2005 Dan Walsh <dwalsh@redhat.com> 1.3.35-1
- Update from NSA
  * Merged sepol handle passing, seusers support, and policydb cache
    patches from Ivan Gyurdiev.

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.3.34-1
- Update from NSA
  * Merged resync to sepol changes and booleans fixes/improvements 
    patches from Ivan Gyurdiev.
  * Merged support for genhomedircon/homedir template, store selection,
    explicit policy reload, and semanage.conf relocation from Joshua
    Brindle.

* Mon Oct 24 2005 Dan Walsh <dwalsh@redhat.com> 1.3.32-1
- Update from NSA
  * Merged resync to sepol changes and transaction fix patches from
    Ivan Gyurdiev.
  * Merged reorganize users patch from Ivan Gyurdiev.
  * Merged remove unused relay functions patch from Ivan Gyurdiev.

* Fri Oct 21 2005 Dan Walsh <dwalsh@redhat.com> 1.3.30-1
- Update from NSA
  * Fixed policy file leaks in semanage_load_module and
    semanage_write_module.
  * Merged further database work from Ivan Gyurdiev.
  * Fixed bug in semanage_direct_disconnect.

* Thu Oct 20 2005 Dan Walsh <dwalsh@redhat.com> 1.3.28-1
- Update from NSA
  * Merged interface renaming patch from Ivan Gyurdiev.
  * Merged policy component patch from Ivan Gyurdiev.
  * Renamed 'check=' configuration value to 'expand-check=' for 
    clarity.
  * Changed semanage_commit_sandbox to check for and report errors 
    on rename(2) calls performed during rollback.
  * Added optional check= configuration value to semanage.conf 
    and updated call to sepol_expand_module to pass its value
    to control assertion and hierarchy checking on module expansion.
  * Merged fixes for make DESTDIR= builds from Joshua Brindle.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.3.24-1
- Update from NSA
  * Merged default database from Ivan Gyurdiev.
  * Merged removal of connect requirement in policydb backend from
    Ivan Gyurdiev.
  * Merged commit locking fix and lock rename from Joshua Brindle.
  * Merged transaction rollback in lock patch from Joshua Brindle.
  * Changed default args for load_policy to be null, as it no longer
    takes a pathname argument and we want to preserve booleans.
  * Merged move local dbase initialization patch from Ivan Gyurdiev.
  * Merged acquire/release read lock in databases patch from Ivan Gyurdiev.
  * Merged rename direct -> policydb as appropriate patch from Ivan Gyurdiev.
  * Added calls to sepol_policy_file_set_handle interface prior
    to invoking sepol operations on policy files.
  * Updated call to sepol_policydb_from_image to pass the handle.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.3.20-1
- Update from NSA
  * Changed default args for load_policy to be null, as it no longer
    takes a pathname argument and we want to preserve booleans.
  * Merged move local dbase initialization patch from Ivan Gyurdiev.
  * Merged acquire/release read lock in databases patch from Ivan Gyurdiev.
  * Merged rename direct -> policydb as appropriate patch from Ivan Gyurdiev.
  * Added calls to sepol_policy_file_set_handle interface prior
    to invoking sepol operations on policy files.
  * Updated call to sepol_policydb_from_image to pass the handle.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.3.20-1
- Update from NSA
  * Merged user and port APIs - policy database patch from Ivan
  Gyurdiev.
  * Converted calls to sepol link_packages and expand_module interfaces
  from using buffers to using sepol handles for error reporting, and 
  changed direct_connect/disconnect to create/destroy sepol handles.

* Sat Oct 15 2005 Dan Walsh <dwalsh@redhat.com> 1.3.18-1
- Update from NSA
  * Merged bugfix patch from Ivan Gyurdiev.
  * Merged seuser database patch from Ivan Gyurdiev.
  Merged direct user/port databases to the handle from Ivan Gyurdiev.
  * Removed obsolete include/semanage/commit_api.h (leftover).
  Merged seuser record patch from Ivan Gyurdiev.
  * Merged boolean and interface databases from Ivan Gyurdiev.

* Fri Oct 14 2005 Dan Walsh <dwalsh@redhat.com> 1.3.14-1
- Update from NSA
  * Updated to use get interfaces for hidden sepol_module_package type.
  * Changed semanage_expand_sandbox and semanage_install_active
  to generate/install the latest policy version supported  by libsepol
  by default (unless overridden by semanage.conf), since libselinux
  will now downgrade automatically for load_policy.
  * Merged new callback-based error reporting system and ongoing
  database work from Ivan Gyurdiev.

* Wed Oct 12 2005 Dan Walsh <dwalsh@redhat.com> 1.3.11-1
- Update from NSA
  * Fixed semanage_install_active() to use the same logic for
  selecting a policy version as semanage_expand_sandbox().  Dropped
  dead code from semanage_install_sandbox().

* Mon Oct 10 2005 Dan Walsh <dwalsh@redhat.com> 1.3.10-1
- Update from NSA
  * Updated for changes to libsepol, and to only use types and interfaces
  provided by the shared libsepol.

* Fri Oct 7 2005 Dan Walsh <dwalsh@redhat.com> 1.3.9-1
- Update from NSA
  * Merged further database work from Ivan Gyurdiev.

* Tue Oct 4 2005 Dan Walsh <dwalsh@redhat.com> 1.3.8-1
- Update from NSA
  * Merged iterate, redistribute, and dbase split patches from
  Ivan Gyurdiev.

* Mon Oct 3 2005 Dan Walsh <dwalsh@redhat.com> 1.3.7-1
- Update from NSA
  * Merged patch series from Ivan Gyurdiev.
    (pointer typedef elimination, file renames, dbase work, backend
     separation)
  * Split interfaces from semanage.[hc] into handle.[hc], modules.[hc].
  * Separated handle create from connect interface.
  * Added a constructor for initialization.
  * Moved up src/include/*.h to src.
  * Created a symbol map file; dropped dso.h and hidden markings.

* Wed Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1.3.5-1
- Update from NSA
  * Split interfaces from semanage.[hc] into handle.[hc], modules.[hc].
  * Separated handle create from connect interface.
  * Added a constructor for initialization.
  * Moved up src/include/*.h to src.
  * Created a symbol map file; dropped dso.h and hidden markings.

* Fri Sep 23 2005 Dan Walsh <dwalsh@redhat.com> 1.3.4-1
- Update from NSA
  * Merged dbase redesign patch from Ivan Gyurdiev.

* Wed Sep 21 2005 Dan Walsh <dwalsh@redhat.com> 1.3.3-1
- Update from NSA
  * Merged boolean record, stub record handler, and status codes 
    patches from Ivan Gyurdiev.

* Tue Sep 20 2005 Dan Walsh <dwalsh@redhat.com> 1.3.2-1
- Update from NSA
  * Merged stub iterator functionality from Ivan Gyurdiev.
  * Merged interface record patch from Ivan Gyurdiev.

* Wed Sep 14 2005 Dan Walsh <dwalsh@redhat.com> 1.3.1-1
- Update from NSA
  * Merged stub functionality for managing user and port records,
  and record table code from Ivan Gyurdiev.
  * Updated version for release.

* Thu Sep 1 2005 Dan Walsh <dwalsh@redhat.com> 1.1.6-1
- Update from NSA
  * Merged semod.conf template patch from Dan Walsh (Red Hat),
  but restored location to /usr/share/semod/semod.conf.
  * Fixed several bugs found by valgrind.
  * Fixed bug in prior patch for the semod_build_module_list leak.
  * Merged errno fix from Joshua Brindle (Tresys).
  * Merged fix for semod_build_modules_list leak on error path
    from Serge Hallyn (IBM).  Bug found by Coverity.

* Thu Aug 25 2005 Dan Walsh <dwalsh@redhat.com> 1.1.3-1
- Update from NSA
  * Merged errno fix from Joshua Brindle (Tresys).
  * Merged fix for semod_build_modules_list leak on error path
    from Serge Hallyn (IBM).  Bug found by Coverity.
  * Merged several fixes from Serge Hallyn (IBM).  Bugs found by
    Coverity.
  * Fixed several other bugs and warnings.
  * Merged patch to move module read/write code from libsemanage
    to libsepol from Jason Tang (Tresys).  
  * Merged relay records patch from Ivan Gyurdiev.
  * Merged key extract patch from Ivan Gyurdiev.
- Initial version
- Created by Stephen Smalley <sds@epoch.ncsc.mil> 
