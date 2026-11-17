# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-bugzilla
Version:        3.3.0
Release: 7%{?dist}
Summary:        Python library for interacting with Bugzilla

License:        GPL-2.0-or-later
URL:            https://github.com/python-bugzilla/python-bugzilla
Source0:        https://github.com/python-bugzilla/python-bugzilla/archive/v%{version}/%{name}-%{version}.tar.gz

Patch: 0001-Loosen-test-requirements-for-Fedora.patch
BuildArch:      noarch

BuildRequires: python3-devel
# tests need to be able to set en_US.UTF-8 locale
BuildRequires: glibc-langpack-en

%global _description\
python-bugzilla is a python library for interacting with bugzilla instances\
over XMLRPC or REST.\

%description %_description


%package -n python3-bugzilla
Summary: %summary
Requires: python3-requests
%{?python_provide:%python_provide python3-bugzilla}

Obsoletes:      python-bugzilla < %{version}-%{release}
Obsoletes:      python2-bugzilla < %{version}-%{release}

%description -n python3-bugzilla %_description


%package cli
Summary: Command line tool for interacting with Bugzilla
Requires: python3-bugzilla = %{version}-%{release}

%description cli
This package includes the 'bugzilla' command-line tool for interacting with bugzilla. Uses the python-bugzilla API



%prep
%autosetup -p1



%generate_buildrequires
%pyproject_buildrequires -t



%build
%pyproject_wheel



%install
%pyproject_install
%pyproject_save_files bugzilla


%check
%tox



%files -n python3-bugzilla -f %{pyproject_files}
%doc README.md NEWS.md


%files cli
%{_bindir}/bugzilla
%{_mandir}/man1/bugzilla.1.gz


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.3.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.3.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.3.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 23 2024 Cole Robinson <crobinso@redhat.com> - 3.3.0-1
- Update to version 3.3.0

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 3.2.0-13
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.2.0-11
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 12 2023 Adam Williamson <awilliam@redhat.com> - 3.2.0-8
- Backport PR #190 to allow settings blocks/depends as strings (e.g. aliases)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.2.0-6
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.2.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Cole Robinson <crobinso@redhat.com> - 3.2.0-1
- Update to version 3.2.0
- Use soon-to-be-required Authorization header for RH bugzilla
- Remove cookie auth support

* Tue Jul 27 2021 Cole Robinson <crobinso@redhat.com> - 3.1.0-1
- Update to version 3.1.0
- Detect bugzilla.stage.redhat.com as RHBugzilla
- Add limit as option to build_query (Ivan Lausuch)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 3.0.2-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 2020 Cole Robinson <crobinso@redhat.com> - 3.0.2-1
- Update to version 3.0.2
- Fix API key leaking into requests exceptions (bz #1896791)

* Sat Oct 03 2020 Cole Robinson <crobinso@redhat.com> - 3.0.0-1
- Update to version 3.0.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 04 2020 Cole Robinson <crobinso@redhat.com> - 2.5.0-1
- Update to version 2.5.0
- cli: Add query --extrafield, --includefield, --excludefield
- Revive bugzilla.rhbugzilla.RHBugzilla import path

* Mon Jun 29 2020 Cole Robinson <crobinso@redhat.com> - 2.4.0-1
- Update to version 2.4.0
- Bugzilla REST API support
- Add --json command line output option
- Add APIs for Bugzilla Groups (Pierre-Yves Chibon)
- Add `Bugzilla.get_requests_session()` API to access raw requests Session
- Add `Bugzilla.get_xmlrpc_proxy()` API to access raw ServerProxy
- Add `Bugzilla requests_session=` init parameter to pass in auth, etc.
- Add `bugzilla attach --ignore-obsolete` (Čestmír Kalina)
- Add `bugzilla login --api-key` for API key prompting (Danilo C. L. de
  Paula)
- Add `bugzilla new --private`

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 04 2019 Cole Robinson <crobinso@redhat.com> - 2.3.0-2
- Disable python2 build for f32+ (bz #1746753)

* Mon Aug 26 2019 Cole Robinson <crobinso@redhat.com> - 2.3.0-1
- Update to version 2.3.0
- restrict-login suppot (Viliam Krizan)
- cli: Add support for private attachments (Brian 'Redbeard' Harrington)
- Fix python3 deprecation warnings
- Drop python 3.3 support, minimum python3 is python 3.4 now

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.2.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 06 2019 Cole Robinson <crobinso@redhat.com> - 2.2.0-3
- Fix SafeConfigParser warnings

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Aug 11 2018 Cole Robinson <crobinso@redhat.com> - 2.2.0-1
- Rebased to version 2.2.0
- Port tests to pytest
- cli: --cert Client side certificate support (Tobias Wolter)
- cli: add ability to post comment while sending attachment (Jeff Mahoney)
- cli: Add --comment-tag option
- cli: Add info --active-components
- Add a raw Product.get wrapper API
- Don't traceback on missing cli command (bz #1513819)
- Fix bug.get with sub_components (bz #1503491)
- Fix uploading binary attachments (bz #1496821)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.0-7
- Rebuilt for Python 3.7

* Fri Mar 16 2018 Tomas Orsava <torsava@redhat.com> - 2.1.0-6
- Conditionalize the Python 2 subpackage

* Fri Mar 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.1.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 09 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.0-3
- Python 2 binary package renamed to python2-bugzilla
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 30 2017 Cole Robinson <crobinso@redhat.com> - 2.1.0-1
- Rebased to version 2.1.0
- Support for bugzilla 5 API Keys (Dustin J. Mitchell)
- bugzillarc can be used to set default URL for the cli tool
- Revive update_flags wrapper
- Bug fixes and minor improvements

* Wed Feb 08 2017 Cole Robinson <crobinso@redhat.com> - 2.0.0-1
- Rebased to version 2.0.0
- Several fixes for use with bugzilla 5
- This release contains several smallish API breaks:
- Bugzilla.bug_autorefresh now defaults to False
- Credentials are now cached in ~/.cache/python-bugzilla/
- bin/bugzilla was converted to argparse
- bugzilla query --boolean_chart option is removed
- Unify command line flags across sub commands

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.2.2-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 02 2015 Robert Kuska <rkuska@redhat.com> - 1.2.2-2
- Rebuilt for Python3.5 rebuild

* Tue Sep 22 2015 Cole Robinson <crobinso@redhat.com> - 1.2.2-1
- Rebased to version 1.2.2
- Fix requests usage when ndg-httpsclient is installed (bz #1247158)
- Fix errors with non-ascii usernames (bz #1264848)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 Cole Robinson <crobinso@redhat.com> - 1.2.1-1
- Rebased to version 1.2.1
- bin/bugzilla: Add --ensure-logged-in option
- Fix get_products with bugzilla.redhat.com
- A few other minor improvements

* Wed Apr 08 2015 Cole Robinson <crobinso@redhat.com> - 1.2.0-1
- Rebased to version 1.2.0
- Add bugzilla new/query/modify --field flag (Arun Babu Neelicattu)
- API support for ExternalBugs (Arun Babu Neelicattu, Brian Bouterse)
- Add new/modify --alias support (Adam Williamson)
- Bugzilla.logged_in now returns live state (Arun Babu Neelicattu)
- Fix getbugs API with latest Bugzilla releases

* Wed Jun 18 2014 Cole Robinson <crobinso@redhat.com> - 1.1.0-2
- Fix tests on rawhide (bz #1106734)

* Sun Jun 01 2014 Cole Robinson <crobinso@redhat.com> - 1.1.0-1
- Rebased to version 1.1.0
- Support for bugzilla tokens (Arun Babu Nelicattu)
- bugzilla: Add query/modify --tags
- bugzilla --login: Allow to login and run a command in one shot
- bugzilla --no-cache-credentials: Don't use or save cached credentials
  when using the CLI
- Show bugzilla errors when login fails
- Don't pull down attachments in bug.refresh(), need to get
  bug.attachments manually
- Add Bugzilla bug_autorefresh parameter.

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Mar 27 2014 Cole Robinson <crobinso@redhat.com> - 1.0.0-2
- /usr/bin/bugzilla should use python2 (bz #1081594)

* Tue Mar 25 2014 Cole Robinson <crobinso@redhat.com> - 1.0.0-1
- Rebased to version 1.0.0
- Python 3 support (Arun Babu Neelicattu)
- Port to python-requests (Arun Babu Neelicattu)
- bugzilla: new: Add --keywords, --assigned_to, --qa_contact (Lon
  Hohberger)
- bugzilla: query: Add --quicksearch, --savedsearch
- bugzilla: query: Support saved searches with --from-url
- bugzilla: --sub-component support for all relevant commands

* Tue Nov 05 2013 Cole Robinson <crobinso@redhat.com> - 0.9.0-3
- Drop unneeded setuptools dep

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 19 2013 Cole Robinson <crobinso@redhat.com> - 0.9.0-1
- Rebased to version 0.9.0
- bugzilla: modify: add --dependson (Don Zickus)
- bugzilla: new: add --groups option (Paul Frields)
- bugzilla: modify: Allow setting nearly every bug parameter
- NovellBugzilla implementation removed, can't get it to work
- Gracefully handle private bugs (bz #963979)
- Raise error if python-magic is needed (bz #951572)
- CVE-2013-2191: Add SSL host and cert validation (bz #975961, bz #951594)

* Mon Mar 04 2013 Cole Robinson <crobinso@redhat.com> - 0.8.0-2
- Don't upload scrambled attachments (bz #915318)

* Fri Feb 15 2013 Cole Robinson <crobinso@redhat.com> - 0.8.0-1
- Rebased to version 0.8.0
- Drop most usage of non-upstream RH Bugzilla API
- Test suite improvements, nearly complete code coverage
- Fix all open bug reports and RFEs

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Adam Jackson <ajax@redhat.com> 0.7.0-3
- Make closing bugs work, and allow closing as duplicate.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Cole Robinson <crobinso@redhat.com> - 0.7.0-1
- Rebased to version 0.7.0
- Fix querying with latest Red Hat bugzilla
- Bugzilla 4 API support
- Improve querying non-RH bugzilla instances

* Tue Apr  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.2-4
- Cleanup spec and actually rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 09 2011 Will Woods <wwoods@redhat.com> - 0.6.2-2
- Add "Requires: python-magic"

* Tue Jun 07 2011 Will Woods <wwoods@redhat.com> - 0.6.2-1
- add 'bugzilla attach' command (#707320)
- update CLI --help, improve manpage a bit
- fix --blocked and other boolean CLI options (#621601)
- use NamedTemporaryFile for temp. cookiefiles (#625019)
- fix openattachment() on non-ascii filenames (#663674 - thanks kklic)
- clean up handling of unknown product names (#659331)
- misc CLI fixes (--oneline, --qa_whiteboard), add 'modify --qa_contact'

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug  5 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.1-3
- add compatibility patch for python 2.7 (bug 621298)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Apr 16 2010 Will Woods <wwoods@redhat.com> - 0.6.1-1
- CLI speedup: skip version autodetection for bugzilla.redhat.com
- CLI: fix bug 581670 - UnicodeEncodeError crash using --outputformat
- CLI: fix bug 549186 - parser failure/xmlrpc Fault on 'bugzilla query'
- Library: fix bug 577327 - crash changing assignee without --comment
- Library: fix bug 580711 - crash when bug has empty CC list
- Library: add new Bugzilla36 class
- Library: export and autodetect Bugzilla34 and Bugzilla36 classes

* Tue Mar 2 2010 Will Woods <wwoods@redhat.com> - 0.6.0-1
- New version 0.6, with lots of improvements and fixes.
- Library: add NovellBugzilla implementation
- Library: use standardized LWPCookieJar by default
- Library: implement unicode(bug), fix Bug.__str__ unicode handling
- Library: make Bug class pickle-friendly
- Library: add flag info helper methods to Bug class
- Library: handle problems with missing fields in User class
- CLI: --oneline formatting tweaks and dramatic speed improvements
- CLI: add support for modifying private, status, assignee, flags, cc, fixed_in
- CLI: improve query: allow multiple flags, flag negation, handle booleans
- CLI: make --cc work when creating bugs
- CLI: new --raw output style
- CLI: special output format fields for flag and whiteboard
- CLI: fix broken --cc and -p flags
- CLI: fix problem where bz comments default to being private
- CLI: improve 'info --product' output
- CLI: handle socket/network failure cleanly
- CLI: allow adding comments when updating whiteboards

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Will Woods <wwoods@redhat.com> - 0.5.1-2
- Fix missing util.py

* Thu Apr 9 2009 Will Woods <wwoods@redhat.com> - 0.5.1-1
- CLI: fix unicode handling
- CLI: add --from-url flag, which parses a bugzilla query.cgi URL
- CLI: fix showing aliases
- CLI: add --comment, --private, --status, --assignee, --flag, --cc for update
- CLI: fix --target_milestone

* Wed Mar 25 2009 Will Woods <wwoods@redhat.com> - 0.5-1
- Fix problem where login wasn't saving the cookies to a file 
- Fix openattachment (bug #487673)
- Update version number for 0.5 final

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.rc1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Will Woods <wwoods@redhat.com> 0.5-0.rc1
- Improve cookie handling
- Add User class and associated Bugzilla methods (in Bugzilla 3.4)
- Add {add,edit,get}component methods
- Fix getbugs() so a single invalid bug ID won't abort the whole request
- CLI: fix -c <component>

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4-0.rc4.1
- Rebuild for Python 2.6

* Wed Oct 15 2008 Will Woods <wwoods@redhat.com> 0.4-0.rc4
- CLI: fix traceback with --full (Don Zickus)
- CLI: add --oneline (Don Zickus)
- CLI: speedup when querying bugs by ID (Don Zickus)
- CLI: add --bztype
- CLI: --bug_status defaults to ALL
- Fix addcc()/deletecc()
- RHBugzilla3: raise useful error on getbug(unreadable_bug_id)
- Add adduser() (Jon Stanley)

* Wed Oct  8 2008 Will Woods <wwoods@redhat.com> 0.4-0.rc3
- Add updateperms() - patch courtesy of Jon Stanley
- Fix attachfile() for RHBugzilla3
- Actually install man page. Whoops.

* Thu Sep 18 2008 Will Woods <wwoods@redhat.com> 0.4-0.rc2
- Auto-generated man page with much more info
- Fix _attachfile()

* Thu Sep  4 2008 Will Woods <wwoods@redhat.com> 0.4-0.rc1
- Update to python-bugzilla 0.4-rc1
- We now support upstream Bugzilla 3.x and Red Hat's Bugzilla 3.x instance
- library saves login cookie in ~/.bugzillacookies
- new 'bugzilla login' command to get a login cookie

* Sat Jan 12 2008 Will Woods <wwoods@redhat.com> 0.3-1
- Update to python-bugzilla 0.3 
- 'modify' works in the commandline-util
- add Bug.close() and Bug.setstatus()

* Thu Dec 13 2007 Will Woods <wwoods@redhat.com> 0.2-4
- use _bindir instead of /usr/bin and proper BR for setuptools

* Tue Dec 11 2007 Will Woods <wwoods@redhat.com> 0.2-3
- Fix a couple of things rpmlint complained about

* Tue Dec 11 2007 Will Woods <wwoods@redhat.com> 0.2-2
- Add docs

* Wed Oct 10 2007 Will Woods <wwoods@redhat.com> 0.2-1
- Initial packaging.
