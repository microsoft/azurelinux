%define libselinuxver 3.2-1
%define libsepolver 3.2-1
Summary:        SELinux policy compiler
Name:           checkpolicy
Version:        3.2
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/SELinuxProject/selinux/wiki
Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  flex-devel
BuildRequires:  gcc
BuildRequires:  libselinux-devel >= %{libselinuxver}
BuildRequires:  libsepol-devel >= %{libsepolver}

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

This package contains checkpolicy, the SELinux policy compiler.
Only required for building policies.

%prep
%autosetup -p1

%build
%make_build clean
%make_build LIBDIR="%{_libdir}" CFLAGS="%{build_cflags} -fno-semantic-interposition"

pushd test
%make_build LIBDIR="%{_libdir}" CFLAGS="%{build_cflags} -fno-semantic-interposition"
popd

%install
mkdir -p %{buildroot}%{_bindir}
%make_install LIBDIR="%{_libdir}"
install test/dismod %{buildroot}%{_bindir}/sedismod
install test/dispol %{buildroot}%{_bindir}/sedispol

%files
%license COPYING
%{_bindir}/checkpolicy
%{_bindir}/checkmodule
%{_bindir}/sedismod
%{_bindir}/sedispol
%{_mandir}/man8/checkpolicy.8.gz
%{_mandir}/man8/checkmodule.8.gz
%{_mandir}/ru/man8/checkpolicy.8.gz
%{_mandir}/ru/man8/checkmodule.8.gz

%changelog
* Fri Aug 13 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.2-1
- Upgrade to latest upstream version
- Add -fno-semantic-interposition to CFLAGS as recommended by upstream
- Update source URL to new format
- Lint spec
- License verified

* Wed Aug 19 2020 Daniel Burgener <Daniel.Burgener@microsoft.com> - 2.9-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT)
- License verified

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 18 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-1
- SELinux userspace 2.9 release

* Mon Mar 11 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc2.1
- SELinux userspace 2.9-rc2 release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-0.rc1.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc1.1
- SELinux userspace 2.9-rc1 release

* Mon Jan 21 2019 Petr Lautrbach <plautrba@redhat.com> - 2.8-3
- Check the result value of hashtable_search
- Destroy the class datum if it fails to initialize

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-1
- SELinux userspace 2.8 release

* Tue May 15 2018 Petr Lautrbach <plautrba@workstation> - 2.8-0.rc3.1
- SELinux userspace 2.8-rc3 release candidate

* Mon Apr 23 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc1.1
- SELinux userspace 2.8-rc1 release candidate

* Wed Mar 21 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-7
- Add support for the SCTP portcon keyword

* Tue Mar 13 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-6
- build: follow standard semantics for DESTDIR and PREFIX

* Thu Feb 22 2018 Florian Weimer <fweimer@redhat.com> - 2.7-5
- Use LDFLAGS from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-3
- Rebuild with libsepol-2.7-3 and libselinux-2.7-6

* Fri Oct 20 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-2
- Rebuilt with libsepol-2.7-2

* Mon Aug 07 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-1
- Update to upstream release 2017-08-04

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 15 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-1
- Update to upstream release 2016-10-14

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 03 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-8
- Add types associated to a role in the current scope when parsing

* Mon Aug 01 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-7
- Extend checkpolicy pathname matching
- Rebuilt with libsepol-2.5-9

* Mon Jun 27 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-6
- Fix typos in sedispol

* Thu Jun 23 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-5
- Set flex as default lexer
- Fix checkmodule output message

* Wed May 11 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-4
- Rebuilt with libsepol-2.5-6

* Fri Apr 29 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-3
- Build policy on systems not supporting DCCP protocol
- Fail if module name different than output base filename

* Fri Apr 08 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-2
- Add support for portcon dccp protocol

* Tue Feb 23 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-1
- Update to upstream release 2016-02-23

* Sun Feb 21 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-0.1.rc1
- Update to upstream rc1 release 2016-01-07

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 21 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-1.1
- Update to 2.4 release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 2.3-3
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 6 2014 Dan Walsh <dwalsh@redhat.com> - 2.3-1
- Update to upstream 
    * Add Android support for building dispol.
    * Report source file and line information for neverallow failures.
    * Prevent incompatible option combinations for checkmodule.
    * Drop -lselinux from LDLIBS for test programs; not used.
    * Add debug feature to display constraints/validatetrans from Richard Haines.

* Thu Oct 31 2013 Dan Walsh <dwalsh@redhat.com> - 2.2-1
- Update to upstream 
    * Fix hyphen usage in man pages from Laurent Bigonville.
    * handle-unknown / -U required argument fix from Laurent Bigonville.
    * Support overriding Makefile PATH and LIBDIR from Laurent Bigonville.
    * Support space and : in filenames from Dan Walsh.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-4
- Fix a segmentation fault if the --handle-unknown option was set without
arguments.
- Thanks to Alexandre Rebert and his team at Carnegie Mellon University
for detecting this crash.

* Tue Mar 19 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-3
- ":" should be allowed for file trans names

* Tue Mar 12 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-2
- Space should be allowed for file trans names

* Thu Feb 7 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-1
- Update to upstream 
        * Fix errors found by coverity
        * implement default type policy syntax
        * Free allocated memory when clean up / exit.

* Sat Jan 5 2013 Dan Walsh <dwalsh@redhat.com> -  2.1.11-3
- Update to latest patches from eparis/Upstream
-   checkpolicy: libsepol: implement default type policy syntax
-   
-   We currently have a mechanism in which the default user, role, and range
-   can be picked up from the source or the target object.  This implements
-   the same thing for types.  The kernel will override this with type
-   transition rules and similar.  This is just the default if nothing
-   specific is given.

* Wed Sep 19 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-2
- Rebuild with fixed libsepol

* Thu Sep 13 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-1
- Update to upstream 
    * fd leak reading policy
    * check return code on ebitmap_set_bit

* Mon Jul 30 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-4
- Rebuild to grab latest libsepol

* Tue Jul 24 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-3
- Rebuild to grab latest libsepol

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 4 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-1
- Update to upstream 
    * sepolgen: We need to support files that have a + in them
    * Android/MacOS X build support

* Mon Apr 23 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-4
- Rebuild to get latest libsepol which fixes the file_name transition problems

* Tue Apr 17 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-3
- Recompile with libsepol that has support for ptrace_child

* Tue Apr 3 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-2
- Allow checkpolicy to use + in a file name

* Thu Mar 29 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-1
- Update to upstream 
    * implement new default labeling behaviors for usr, role, range
    * Fix dead links to www.nsa.gov/selinux

* Mon Jan 16 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.8-3
- Fix man page to link to www.nsa.giv/research/selinux

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-1
-Update to upstream
    * add ignoredirs config for genhomedircon
    * Fallback_user_level can be NULL if you are not using MLS

* Wed Dec 21 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.7-3
- default_rules should be optional

* Thu Dec 15 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.7-2
- Rebuild with latest libsepol

* Tue Dec 6 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.7-1
- Upgrade to upstream
    * dis* fixed signed vs unsigned errors
    * dismod: fix unused parameter errors
    * test: Makefile: include -W and -Werror
    * allow ~ in filename transition rules
- Allow policy to specify the source of target for generating the default user,role 
- or mls label for a new target.

* Mon Nov 14 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.6-2
- Allow ~ in a filename 

* Fri Nov 4 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.6-1
- Upgrade to upstream
    * Revert "checkpolicy: Redo filename/filesystem syntax to support filename trans rules"
    * drop libsepol dynamic link in checkpolicy

* Tue Sep 20 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-2
- Fix checkpolicy to ignore '"' in filename trans rules

* Mon Sep 19 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-1
-Update to upstream
    * Separate tunable from boolean during compile.

* Tue Aug 30 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-0
-Update to upstream
    * checkpolicy: fix spacing in output message

* Thu Aug 18 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.3-0
    * add missing ; to attribute_role_def
    *Redo filename/filesystem syntax to support filename trans

* Wed Aug 3 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.2-0
-Update to upstream
    * .gitignore changes
    * dispol output of role trans
    * man page update: build a module with an older policy version

* Thu Jul 28 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.1-0
-Update to upstream
    * Minor updates to filename trans rule output in dis{mod,pol}

* Thu Jul 28 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.0-1
-Update to upstream

* Mon May 23 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.26-1
-Update to upstream
    * Wrap file names in filename transitions with quotes by Steve Lawrence.
    * Allow filesystem names to start with a digit by James Carter.
    * Add support for using the last path compnent in type transitions by Eric

* Thu Apr 21 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.24-2

* Fixes for new role_transition class field by Eric Paris.

* Fri Apr 15 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.24-2
- Add "-" as a file type

* Tue Apr 12 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.24-1
-Update to upstream
    * Add new class field in role_transition by Harry Ciao.

* Mon Apr 11 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.23-5
- Fix type_transition to allow all files

* Tue Mar 29 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.23-4
- Patches from Eric Paris 
We just use random numbers to make menu selections.  Use #defines and
names that make some sense instead.
This patch adds support for using the last path component as part of the
information in making labeling decisions for new objects.  A example
rule looks like so:
type_transition unconfined_t etc_t:file system_conf_t eric;
This rule says if unconfined_t creates a file in a directory labeled
etc_t and the last path component is "eric" (no globbing, no matching
magic, just exact strcmp) it should be labeled system_conf_t.
The kernel and policy representation does not have support for such
rules in conditionals, and thus policy explicitly notes that fact if
such a rule is added to a conditional.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.23-2
- Add James Carters Patch
  *This patch is needed because some filesystem names (such as 9p) start
  with a digit.

* Tue Dec 21 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.23-1
- Latest update from NSA
  * Remove unused variables to fix compliation under GCC 4.6 by Justin Mattock

* Wed Dec 8 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.22-2
- Rebuild to make sure it will build in Fedora 

* Wed Jun 16 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.22-1
- Latest update from NSA
    * Update checkmodule man page and usage by Daniel Walsh and Steve Lawrence
- Allow policy version to be one number

* Mon May 3 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.21-2
- Fix checkmodule man page and usage statements

* Sun Nov 1 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.21-1
- Latest update from NSA
    * Add support for building Xen policies from Paul Nuzzi.
    * Add long options to checkpolicy and checkmodule by Guido
      Trentalancia <guido@trentalancia.com>

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.19-1
- Latest update from NSA
    * Fix alias field in module format, caused by boundary format change
      from Caleb Case.

* Fri Jan 30 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.18-1
- Latest update from NSA
    * Properly escape regex symbols in the lexer from Stephen Smalley.
    * Add bounds support from KaiGai Kohei.

* Tue Oct 28 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.16-4

* Mon Jul 7 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.16-3
- Rebuild with new libsepol

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.16-2
- fix license tag

* Wed May 28 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.16-1
- Latest update from NSA
    * Update checkpolicy for user and role mapping support from Joshua Brindle.

* Fri May 2 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.15-1
- Latest update from NSA
    * Fix for policy module versions that look like IPv4 addresses from Jim Carter.
      Resolves bug 444451.

* Fri May 2 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.14-2
- Allow modules with 4 sections or more

* Thu Mar 27 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.14-1
- Latest update from NSA
    * Add permissive domain support from Eric Paris.

* Thu Mar 13 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.13-1
- Latest update from NSA
    * Split out non-grammar parts of policy_parse.yacc into
      policy_define.c and policy_define.h from Todd C. Miller.
    * Initialize struct policy_file before using it, from Todd C. Miller.
    * Remove unused define, move variable out of .y file, simplify COND_ERR, from Todd C. Miller.

* Thu Feb 28 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.10-1
- Latest update from NSA
    * Use yyerror2() where appropriate from Todd C. Miller.
- Build against latest libsepol

* Fri Feb 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.9-2
- Start shipping sedismod and sedispol

* Mon Feb 4 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.9-1
- Latest update from NSA
    * Update dispol for libsepol avtab changes from Stephen Smalley.

* Fri Jan 25 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.8-1
- Latest update from NSA
    * Deprecate role dominance in parser.

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.7-2
- Update to use libsepol-static library

* Fri Jan 11 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.7-1
- Latest update from NSA
    * Added support for policy capabilities from Todd Miller.

* Thu Nov 15 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.6-1
- Latest update from NSA
    * Initialize the source file name from the command line argument so that checkpolicy/checkmodule report something more useful than "unknown source".
    * Merged remove use of REJECT and trailing context in lex rules; make ipv4 address parsing like ipv6 from James Carter.

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.4-1
    * Merged handle unknown policydb flag support from Eric Paris.
      Adds new command line options -U {allow, reject, deny} for selecting
      the flag when a base module or kernel policy is built.

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.0.3-3
- Rebuild for selinux ppc32 issue.

* Mon Jun 18 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-2
- Rebuild with the latest libsepol

* Sun Jun 17 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.3-1
- Latest update from NSA
    * Merged fix for segfault on duplicate require of sensitivity from Caleb Case.
    * Merged fix for dead URLs in checkpolicy man pages from Dan Walsh.

* Thu Apr 12 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.2-1
- Latest update from NSA
    * Merged checkmodule man page fix from Dan Walsh.

* Fri Mar 30 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.1-3
- Rebuild with new libsepol

* Wed Mar 28 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.1-2
- Rebuild with new libsepol

* Mon Nov 20 2006 Dan Walsh <dwalsh@redhat.com> - 2.0.1-1
- Latest update from NSA
    * Merged patch to allow dots in class identifiers from Caleb Case.

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> - 2.0.0-1
- Latest update from NSA
    * Merged patch to use new libsepol error codes by Karl MacMillan.
    * Updated version for stable branch.

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.1-2
- Rebuild for new libraries

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.1-1
- Latest update from NSA
    * Collapse user identifiers and identifiers together.

* Tue Oct 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.32-1
- Latest update from NSA
    * Updated version for release.

* Thu Sep 28 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.12-1
- Latest update from NSA
    * Merged user and range_transition support for modules from 
      Darrel Goeddel

* Wed Sep 6 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.11-1
- Latest update from NSA
    * merged range_transition enhancements and user module format
      changes from Darrel Goeddel
    * Merged symtab datum patch from Karl MacMillan.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.30.9-1.1
- rebuild

* Tue Jul 4 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.8-1
- Latest upgrade from NSA
    * Lindent.
    * Merged patch to remove TE rule conflict checking from the parser
      from Joshua Brindle.  This can only be done properly by the 
      expander.
    * Merged patch to make checkpolicy/checkmodule handling of
      duplicate/conflicting TE rules the same as the expander 
      from Joshua Brindle.
    * Merged optionals in base take 2 patch set from Joshua Brindle.

* Tue May 23 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.5-1
- Latest upgrade from NSA
    * Merged compiler cleanup patch from Karl MacMillan.
    * Merged fix warnings patch from Karl MacMillan.    

* Wed Apr 5 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.4-1
- Latest upgrade from NSA
    * Changed require_class to reject permissions that have not been
      declared if building a base module.

* Tue Mar 28 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.3-1
- Latest upgrade from NSA
    * Fixed checkmodule to call link_modules prior to expand_module
      to handle optionals.
    * Fixed require_class to avoid shadowing permissions already defined
      in an inherited common definition.

* Mon Mar 27 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.1-2
- Rebuild with new libsepol

* Thu Mar 23 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.1-1
- Latest upgrade from NSA
    * Moved processing of role and user require statements to 2nd pass.

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.30-1
- Latest upgrade from NSA
    * Updated version for release.
    * Fixed bug in role dominance (define_role_dom).

* Fri Feb 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.29.4-1
- Latest upgrade from NSA
    * Added a check for failure to declare each sensitivity in
      a level definition.
    * Changed to clone level data for aliased sensitivities to
      avoid double free upon sens_destroy.  Bug reported by Kevin
      Carr of Tresys Technology.

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> - 1.29.2-1
- Latest upgrade from NSA
    * Merged optionals in base patch from Joshua Brindle.

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> - 1.29.1-1.2
- Need to build againi

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.29.1-1.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Dan Walsh <dwalsh@redhat.com> 1.29.1-1
- Latest upgrade from NSA
    * Merged sepol_av_to_string patch from Joshua Brindle.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.28-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.28-5
- Rebuild to get latest libsepol

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.28-5
- Rebuild to get latest libsepol

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.28-4
- Rebuild to get latest libsepol

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 1.28-3
- Rebuild to get latest libsepol

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 1.28-2
- Rebuild to get latest libsepol

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec 9 2005 Dan Walsh <dwalsh@redhat.com> 1.28-1
- Latest upgrade from NSA

* Sun Dec 4 2005 Dan Walsh <dwalsh@redhat.com> 1.27.20-1
- Latest upgrade from NSA
    * Merged checkmodule man page from Dan Walsh, and edited it.

* Thu Dec 1 2005 Dan Walsh <dwalsh@redhat.com> 1.27.19-1
- Latest upgrade from NSA
    * Added error checking of all ebitmap_set_bit calls for out of
      memory conditions.
    * Merged removal of compatibility handling of netlink classes
      (requirement that policies with newer versions include the
       netlink class definitions, remapping of fine-grained netlink
       classes in newer source policies to single netlink class when
       generating older policies) from George Coker.

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.27.17-7
- Rebuild to get latest libsepol

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.27.17-1
- Latest upgrade from NSA
    * Merged dismod fix from Joshua Brindle.

* Thu Oct 20 2005 Dan Walsh <dwalsh@redhat.com> 1.27.16-1
- Latest upgrade from NSA
    * Removed obsolete cond_check_type_rules() function and call and 
      cond_optimize_lists() call from checkpolicy.c; these are handled
      during parsing and expansion now.
    * Updated calls to expand_module for interface change.
    * Changed checkmodule to verify that expand_module succeeds 
      when building base modules.
    * Merged module compiler fixes from Joshua Brindle.
    * Removed direct calls to hierarchy_check_constraints() and 
      check_assertions() from checkpolicy since they are now called 
      internally by expand_module().

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.27.11-1
- Latest upgrade from NSA
    * Updated for changes to sepol policydb_index_others interface.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.27.10-1
- Latest upgrade from NSA
    * Updated for changes to sepol expand_module and link_modules interfaces.

* Sat Oct 15 2005 Dan Walsh <dwalsh@redhat.com> 1.27.9-2
- Rebuild to get latest libsepol

* Fri Oct 14 2005 Dan Walsh <dwalsh@redhat.com> 1.27.9-1
- Latest upgrade from NSA
    * Merged support for require blocks inside conditionals from
    Joshua Brindle (Tresys).

* Wed Oct 12 2005 Karsten Hopp <karsten@redhat.de> 1.27.8-2
- add buildrequirement for libselinux-devel for dispol

* Mon Oct 10 2005 Dan Walsh <dwalsh@redhat.com> 1.27.8-1
- Latest upgrade from NSA
    * Updated for changes to libsepol.

* Fri Oct 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.7-2
- Rebuild to get latest libsepol

* Thu Oct 6 2005 Dan Walsh <dwalsh@redhat.com> 1.27.7-1
- Latest upgrade from NSA
    * Merged several bug fixes from Joshua Brindle (Tresys).

* Tue Oct 4 2005 Dan Walsh <dwalsh@redhat.com> 1.27.6-1
- Latest upgrade from NSA
    * Merged MLS in modules patch from Joshua Brindle (Tresys).

* Mon Oct 3 2005 Dan Walsh <dwalsh@redhat.com> 1.27.5-2
- Rebuild to get latest libsepol

* Wed Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.5-1
- Latest upgrade from NSA
    * Merged error handling improvement in checkmodule from Karl MacMillan (Tresys).

* Tue Sep 27 2005 Dan Walsh <dwalsh@redhat.com> 1.27.4-1
- Latest upgrade from NSA
    * Merged bugfix for dup role transition error messages from
    Karl MacMillan (Tresys).

* Fri Sep 23 2005 Dan Walsh <dwalsh@redhat.com> 1.27.3-1
- Latest upgrade from NSA
    * Merged policyver/modulever patches from Joshua Brindle (Tresys).

* Wed Sep 21 2005 Dan Walsh <dwalsh@redhat.com> 1.27.2-2
- Rebuild to get latest libsepol

* Wed Sep 21 2005 Dan Walsh <dwalsh@redhat.com> 1.27.2-1
- Latest upgrade from NSA
    * Fixed parse_categories handling of undefined category.

* Tue Sep 20 2005 Dan Walsh <dwalsh@redhat.com> 1.27.1-2
- Rebuild to get latest libsepol

* Sat Sep 17 2005 Dan Walsh <dwalsh@redhat.com> 1.27.1-1
- Latest upgrade from NSA
    * Merged bug fix for role dominance handling from Darrel Goeddel (TCS). 

* Wed Sep 14 2005 Dan Walsh <dwalsh@redhat.com> 1.26-2
- Rebuild to get latest libsepol

* Mon Sep 12 2005 Dan Walsh <dwalsh@redhat.com> 1.26-1
- Latest upgrade from NSA
    * Updated version for release.
- Rebuild to get latest libsepol

* Thu Sep 1 2005 Dan Walsh <dwalsh@redhat.com> 1.25.12-3
- Rebuild to get latest libsepol

* Mon Aug 29 2005 Dan Walsh <dwalsh@redhat.com> 1.25.12-2
- Rebuild to get latest libsepol

* Mon Aug 22 2005 Dan Walsh <dwalsh@redhat.com> 1.25.12-1
- Update to NSA Release
    * Fixed handling of validatetrans constraint expressions.
    Bug reported by Dan Walsh for checkpolicy -M.

* Mon Aug 22 2005 Dan Walsh <dwalsh@redhat.com> 1.25.11-2
- Fix mls crash

* Fri Aug 19 2005 Dan Walsh <dwalsh@redhat.com> 1.25.11-1
- Update to NSA Release
    * Merged use-after-free fix from Serge Hallyn (IBM).  
      Bug found by Coverity.

* Sun Aug 14 2005 Dan Walsh <dwalsh@redhat.com> 1.25.10-1
- Update to NSA Release
    * Fixed further memory leaks found by valgrind.
    * Changed checkpolicy to destroy the policydbs prior to exit
      to allow leak detection.
    * Fixed several memory leaks found by valgrind.

* Sun Aug 14 2005 Dan Walsh <dwalsh@redhat.com> 1.25.8-3
- Rebuild to get latest libsepol changes

* Sat Aug 13 2005 Dan Walsh <dwalsh@redhat.com> 1.25.8-2
- Rebuild to get latest libsepol changes

* Thu Aug 11 2005 Dan Walsh <dwalsh@redhat.com> 1.25.8-1
- Update to NSA Release
    * Updated checkpolicy and dispol for the new avtab format.
      Converted users of ebitmaps to new inline operators.
        Note:  The binary policy format version has been incremented to 
      version 20 as a result of these changes.  To build a policy
      for a kernel that does not yet include these changes, use
      the -c 19 option to checkpolicy.
    * Merged patch to prohibit use of "self" as a type name from Jason Tang (Tresys).
    * Merged patch to fix dismod compilation from Joshua Brindle (Tresys).

* Wed Aug 10 2005 Dan Walsh <dwalsh@redhat.com> 1.25.5-1
- Update to NSA Release
    * Fixed call to hierarchy checking code to pass the right policydb.
    * Merged patch to update dismod for the relocation of the
      module read/write code from libsemanage to libsepol, and
      to enable build of test subdirectory from Jason Tang (Tresys).

* Thu Jul 28 2005 Dan Walsh <dwalsh@redhat.com> 1.25.3-1
- Update to NSA Release
    * Merged hierarchy check fix from Joshua Brindle (Tresys).

* Thu Jul 7 2005 Dan Walsh <dwalsh@redhat.com> 1.25.2-1
- Update to NSA Release
    * Merged loadable module support from Tresys Technology.
    * Merged patch to prohibit the use of * and ~ in type sets 
      (other than in neverallow statements) and in role sets
      from Joshua Brindle (Tresys).
    * Updated version for release.

* Fri May 20 2005 Dan Walsh <dwalsh@redhat.com> 1.23-4-1
- Update to NSA Release
    * Merged cleanup patch from Dan Walsh.

* Thu May 19 2005 Dan Walsh <dwalsh@redhat.com> 1.23-3-1
- Update to NSA Release
    * Added sepol_ prefix to Flask types to avoid namespace
      collision with libselinux.

* Sat May 7 2005 Dan Walsh <dwalsh@redhat.com> 1.23-2-1
- Update to NSA Release
    * Merged identifier fix from Joshua Brindle (Tresys).

* Thu Apr 14 2005 Dan Walsh <dwalsh@redhat.com> 1.23,1-1
    * Merged hierarchical type/role patch from Tresys Technology.
    * Merged MLS fixes from Darrel Goeddel of TCS.

* Thu Mar 10 2005 Dan Walsh <dwalsh@redhat.com> 1.22-1
- Update to NSA Release

* Tue Mar 1 2005 Dan Walsh <dwalsh@redhat.com> 1.21.4-2
- Rebuild for FC4

* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.21.4-1
    * Merged define_user() cleanup patch from Darrel Goeddel (TCS).
    * Moved genpolusers utility to libsepol.
    * Merged range_transition support from Darrel Goeddel (TCS).

* Thu Feb 10 2005 Dan Walsh <dwalsh@redhat.com> 1.21.2-1
- Latest from NSA
    * Changed relabel Makefile target to use restorecon.

* Mon Feb 7 2005 Dan Walsh <dwalsh@redhat.com> 1.21.1-1
- Latest from NSA
    * Merged enhanced MLS support from Darrel Goeddel (TCS).

* Fri Jan 7 2005 Dan Walsh <dwalsh@redhat.com> 1.20.1-1
- Update for version increase at NSA

* Mon Dec 20 2004 Dan Walsh <dwalsh@redhat.com> 1.19.2-1
- Latest from NSA
    * Merged typeattribute statement patch from Darrel Goeddel of TCS.
    * Changed genpolusers to handle multiple user config files.
    * Merged nodecon ordering patch from Chad Hanson of TCS.

* Thu Nov 11 2004 Dan Walsh <dwalsh@redhat.com> 1.19.1-1
- Latest from NSA
    * Merged nodecon ordering patch from Chad Hanson of TCS.

* Thu Nov 4 2004 Dan Walsh <dwalsh@redhat.com> 1.18.1-1
- Latest from NSA
    * MLS build fix.

* Sat Sep 4 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-1
- Latest from NSA
    * Fixed Makefile dependencies (Chris PeBenito).

* Sat Sep 4 2004 Dan Walsh <dwalsh@redhat.com> 1.17.4-1
- Latest from NSA
    * Fixed Makefile dependencies (Chris PeBenito).

* Sat Sep 4 2004 Dan Walsh <dwalsh@redhat.com> 1.17.3-1
- Latest from NSA
    * Merged fix for role dominance ordering issue from Chad Hanson of TCS.

* Mon Aug 30 2004 Dan Walsh <dwalsh@redhat.com> 1.17.2-1
- Latest from NSA

* Thu Aug 26 2004 Dan Walsh <dwalsh@redhat.com> 1.16.3-1
- Fix NSA package to not include y.tab files.

* Tue Aug 24 2004 Dan Walsh <dwalsh@redhat.com> 1.16.2-1
- Latest from NSA
- Allow port ranges to overlap

* Sun Aug 22 2004 Dan Walsh <dwalsh@redhat.com> 1.16.1-1
- Latest from NSA

* Mon Aug 16 2004 Dan Walsh <dwalsh@redhat.com> 1.15.6-1
- Latest from NSA

* Fri Aug 13 2004 Dan Walsh <dwalsh@redhat.com> 1.15.5-1
- Latest from NSA

* Wed Aug 11 2004 Dan Walsh <dwalsh@redhat.com> 1.15.4-1
- Latest from NSA

* Sat Aug 7 2004 Dan Walsh <dwalsh@redhat.com> 1.15.3-1
- Latest from NSA

* Wed Aug 4 2004 Dan Walsh <dwalsh@redhat.com> 1.15.2-1
- Latest from NSA

* Sat Jul 31 2004 Dan Walsh <dwalsh@redhat.com> 1.15.1-1
- Latest from NSA

* Tue Jul 27 2004 Dan Walsh <dwalsh@redhat.com> 1.14.2-1
- Latest from NSA

* Wed Jun 30 2004 Dan Walsh <dwalsh@redhat.com> 1.14.1-1
- Latest from NSA

* Fri Jun 18 2004 Dan Walsh <dwalsh@redhat.com> 1.12.2-1
- Latest from NSA

* Thu Jun 17 2004 Dan Walsh <dwalsh@redhat.com> 1.12.1-1
- Update to latest from NSA

* Wed Jun 16 2004 Dan Walsh <dwalsh@redhat.com> 1.12-1
- Update to latest from NSA

* Wed Jun 16 2004 Dan Walsh <dwalsh@redhat.com> 1.10-5
- Add nlclass patch

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun 4 2004 Dan Walsh <dwalsh@redhat.com> 1.10-3
- Add BuildRequires flex

* Thu Apr 8 2004 Dan Walsh <dwalsh@redhat.com> 1.10-2
- Add BuildRequires byacc

* Thu Apr 8 2004 Dan Walsh <dwalsh@redhat.com> 1.10-1
- Upgrade to the latest from NSA

* Mon Mar 15 2004 Dan Walsh <dwalsh@redhat.com> 1.8-1
- Upgrade to the latest from NSA

* Tue Feb 24 2004 Dan Walsh <dwalsh@redhat.com> 1.6-1
- Upgrade to the latest from NSA

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 20 2004 Dan Walsh <dwalsh@redhat.com> 1.4-6
- Add typealias patch

* Tue Jan 20 2004 Dan Walsh <dwalsh@redhat.com> 1.4-5
- Update excludetypes with negset-final patch

* Wed Jan 14 2004 Dan Walsh <dwalsh@redhat.com> 1.4-4
- Add excludetypes patch

* Wed Jan 14 2004 Dan Walsh <dwalsh@redhat.com> 1.4-3
- Add Colin Walter's lineno patch

* Wed Jan 7 2004 Dan Walsh <dwalsh@redhat.com> 1.4-2
- Remove check for roles transition

* Sat Dec 6 2003 Dan Walsh <dwalsh@redhat.com> 1.4-1
- upgrade to 1.4

* Wed Oct 1 2003 Dan Walsh <dwalsh@redhat.com> 1.2-1
- upgrade to 1.2

* Thu Aug 28 2003 Dan Walsh <dwalsh@redhat.com> 1.1-2
- upgrade to 1.1

* Mon Jun 2 2003 Dan Walsh <dwalsh@redhat.com> 1.0-1
- Initial version
