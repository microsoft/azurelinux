# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:       beakerlib
Summary:    A shell-level integration testing library
Version:    1.33
Release: 2%{?dist}
License:    GPL-2.0-only
BuildArch:  noarch
URL:        https://github.com/%{name}
Autoreq:    0
Requires:   nfs-utils
Requires:   /bin/bash
Requires:   /bin/sh
%if 0%{?fedora}
Recommends: /usr/bin/python3
%endif
%if 0%{?rhel} > 7
Recommends: /usr/libexec/platform-python
%else
# rhel <= 7
Requires:   /usr/bin/python
%endif
%if 0%{?rhel} < 8
Requires:   /usr/bin/perl
Requires:   wget
Requires:   python-lxml
Requires:   /usr/bin/xmllint
%else
# rhel > 7 and fedora
Recommends: /usr/bin/perl
Requires:   (wget or curl)
Suggests:   wget
Recommends: python3-lxml
Recommends: /usr/bin/xmllint
%endif
Requires:   grep
Requires:   sed
Requires:   iproute
Requires:   coreutils
Requires:   tar
Requires:   gzip
Requires:   util-linux
Requires:   which
%if 0%{?fedora}
Requires:   dnf-utils
%else
Requires:   yum-utils
%endif
Requires:   /usr/bin/bc
Requires:   /usr/bin/time
%if 0%{?rhel} < 8
%else
Recommends: beakerlib-redhat
%endif
Conflicts:  beakerlib-redhat < 1-30

BuildRequires: /usr/bin/pod2man
BuildRequires: perl-generators
BuildRequires: util-linux
BuildRequires: make

Source0:    https://github.com/beakerlib/beakerlib/archive/%{version}/%{name}-%{version}.tar.gz
Source1:    %{name}-tmpfiles.conf

Patch0: bugzilla-links.patch
Patch1: bugzilla-links-epel.patch
Patch2: python3.patch
Patch3: python-platform.patch

%prep
%autosetup -N
%if 0%{?fedora}
# Patch0: bugzilla-links.patch
%patch -P 0 -p1
%else
# rhel
# Patch1: bugzilla-links-epel.patch
%patch -P 1 -p1
%endif

%if 0%{?fedora}
# Patch2: python3.patch
%patch -P 2 -p1
%endif
%if 0%{?rhel} > 7
# Patch3: python-platform.patch
%patch -P 3 -p1
%endif


%build
make build

%install
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%{!?_tmpfilesdir: %global _tmpfilesdir %{_prefix}/lib/tmpfiles.d/}
rm -rf $RPM_BUILD_ROOT
make PKGDOCDIR=%{buildroot}/%{_pkgdocdir} DESTDIR=%{buildroot}/usr install
mkdir -p %{buildroot}/%{_tmpfilesdir}
install -m 0644 %{SOURCE1} %{buildroot}/%{_tmpfilesdir}/%{name}.conf

%description
The BeakerLib project means to provide a library of various helpers, which
could be used when writing operating system level integration tests.

%files
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/xslt-templates
%dir %{_pkgdocdir}
%dir %{_pkgdocdir}/examples
%dir %{_pkgdocdir}/examples/*
%{_datadir}/%{name}/dictionary.vim
%{_datadir}/%{name}/*.sh
%{_datadir}/%{name}/xslt-templates/*
%{_bindir}/%{name}-*
%{_mandir}/man1/%{name}*1*
%doc %{_pkgdocdir}/*
%config %{_tmpfilesdir}/%{name}.conf

%package vim-syntax
Summary: Files for syntax highlighting BeakerLib tests in VIM editor
Requires: vim-common
BuildRequires: vim-common
BuildRequires: make

%description vim-syntax
Files for syntax highlighting BeakerLib tests in VIM editor

%files vim-syntax
%{_datadir}/vim/vimfiles/after/ftdetect/beakerlib.vim
%{_datadir}/vim/vimfiles/after/syntax/beakerlib.vim

%changelog
* Fri Feb 6 2026 Dalibor Pospisil <dapospis@redhat.com> - 1.33
- added support for libraries referenced using name only

* Thu Dec 11 2025 Dalibor Pospisil <dapospis@redhat.com> - 1.32
- introduction of the new way to foist the os-relase and thus present
  different system to the tests, including the version, by KwisatzHaderach

* Fri Sep 12 2025 Dalibor Pospisil <dapospis@redhat.com> - 1.31.5-1
- fixed documentation of rlWaitForCmd
- fixed writing to RO variables
- fixed the test suite

* Wed Jan 29 2025 Dalibor Pospisil <dapospis@redhat.com> - 1.31.4-1
- fixed getting base arch on Fedora and c10s
- rlReport support SKIP result, by chuhu
- fixed rlIsRHELLike on systems without /etc/os-release, e.g. RHEL-6
- some minor updates

* Mon Nov 11 2024 Dalibor Pospisil <dapospis@redhat.com> - 1.31.3-1
- Ensure the dashes are removed from the test name prefix, by seberm

* Wed Jul 17 2024 Dalibor Pospisil <dapospis@redhat.com> - 1.31.2-1
- do not block rlJournalPrint on journal.xml creation failure

* Mon Jul 8 2024 Dalibor Pospisil <dapospis@redhat.com> - 1.31.1-1
- fixed variable dereference causing the rlFileSubmit to stick in endless loop

* Wed Jul 3 2024 Dalibor Pospisil <dapospis@redhat.com> - 1.31-1
- dnf5: use --srpm for srpm downloads instead of --source

* Thu Mar 7 2024 Dalibor Pospisil <dapospis@redhat.com> - 1.30-1
- prefer yum over direct download mechanism for the rpm downloads
- a few code cleanups
- fixed some typos
- improved full fmf_id processing
- changed installation prefix from / to /usr

* Thu Oct 20 2022 Dalibor Pospisil <dapospis@redhat.com> - 1.29.3-1
- support for fmf_id nick attribute

* Thu Aug 25 2022 Dalibor Pospisil <dapospis@redhat.com> - 1.29.2-1
- improved performance and memory consumption of the fingerprint feature

* Tue Jul 19 2022 Dalibor Pospisil <dapospis@redhat.com> - 1.29.1-1
- fixed a check for os-release file existence

* Wed Jun 29 2022 Dalibor Pospisil <dapospis@redhat.com> - 1.29-1
- rlImport: upwards traversal start in the current directory
- rlImport: support '.' to import lib.sh from the current directory
- rlImport: can handle libraries required by the fmf_id in different forms than (url, name)
  also name-only. Also the path attribute is considered
- fingerprint: an asserts fingerprint and phases fingerprint is computed
  it is printed as a message and it is also available in the TestResults file
- fixed LOG_LEVEL usage
- removed dependency on selinuxenabled
- fixed a few typos, thanks to jwakely@fedoraproject.org

* Tue Nov 9 2021 Dalibor Pospisil <dapospis@redhat.com> - 1.28-1
- cleanup rlRun_LOG files at rlJournalEnd
- close journal in rlDie - generate journal.xml at that moment
- implemented functions rlIsOS, rlIsOSLike, rlIsOSVersion, and rlIsRHELLike
- rlAssertRequired can now handle versioned dependencies
- new functions rlCheckRerquired, rlCheckRecommended, and rlCheckDependencies

* Thu Mar 25 2021 Dalibor Pospisil <dapospis@redhat.com> - 1.27-1
- rlCheckRequirements is now able to check also versions requirements

* Tue Mar 9 2021 Dalibor Pospisil <dapospis@redhat.com> - 1.26-1
- fixed rlServiceDisable if called without rlServiceEnable beforehand
- few internal fixes

* Tue Feb 9 2021 Dalibor Pospisil <dapospis@redhat.com> - 1.25-1
- rebased yash to version 1.2, fixes the backtick iterpretation
- docs fixes, by Štěpán Němec <snemec@redhat.com>

* Sat Jan 30 2021 Dalibor Pospisil <dapospis@redhat.com> - 1.24-1
- rlImport --all imports only required libraries, not recommend
- implemented chkconfig fallback to systemctl
- fixed `make test` test suite execution

* Tue Jan 26 2021 Dalibor Pospisil <dapospis@redhat.com> - 1.23-1
- TestResults state indicator
- profiling code
- rebased yash to 1.1
- fixed rlAssertLesser
- fixed failed library load name logging

* Fri Jan 15 2021 Dalibor Pospisil <dapospis@redhat.com> - 1.22-1
- ability to parse fmf id references
- ability the use simpler library name - library(foo), {url: '../foo.git', name: '/'}, meaming the library is n the root folder
- ability put library even deeper in the tree - library(foo/path/to/the/library), {url: '../foo.git', name: '/path/to/the/library'}
- rebased yash to 1.0
- and few more minor fixes

* Tue Dec 8 2020 Dalibor Pospisil <dapospis@redhat.com> - 1.21-1
- Rebase to the laster upstream
- better and more consistent search for libraries
- ability to parse yaml files including main.fmf and metadata.yaml

* Thu Sep 10 2020 Dalibor Pospisil <dapospis@redhat.com> - 1.20-1
- Rebase to the latest upstream
- improvements to libraries search
- docs update
- some optimizations
- fixed pattern for mathing port or socket in rlWaitFor*
- log colorizing on all screen* terminals
- IFS fixes
- Use /etc/os-release in rlGetDistro*() (#35)
- support for curl 7.29.0
- prefer curl over wget
- silence status of service in rlService{Start,Stop,Restore} functions (#…
- TESTPACKAGE variable to force package name (#54)

* Tue Jun 9 2020 Dalibor Pospisil <dapospis@redhat.com> - 1.18-12
- optiomized CPU info gathering
- enhanced library search
- added missing dependencies on /usr/bin/bc and /usr/bin/time

* Mon Jun 3 2019 Dalibor Pospisil <dapospis@redhat.com> - 1.18-6
- fixed correct python checking, bz1715479
- fix unbound variables, issues #43
- fixed path to services state store
- fixed file submit to local patch is called outside test harness
- restore shell options in rlWatchdog, bz1713291
- correctly skip test version if there's no rpm source of it, bz1712495

* Thu May 9 2019 Dalibor Pospisil <dapospis@redhat.com> - 1.18-4
- show getopt parsing error (good for debugging)
- do not use -T option to submit command

* Fri Apr 5 2019 Dalibor Pospisil <dapospis@redhat.com> - 1.18-3
- rebase to beakerlib-1.18
- support for dnf/dnf download
- support direct systemctl call
- netstat replaced by ss
- ability to run without python (no journal.xml)
- better handling of reboots
- better handling of persistent data
- final report polishing
- better compatibility with old bash
- <prefix>LibraryDir variable pointing to the library directory for all imported libraries
- fallback to curl if wget is not available
- updated documentation

* Sat Feb 24 2018 Dalibor Pospisil <dapospis@redhat.com> - 1.17-13
- rlRun -s now waits for output logs to be flushed, bz1361246 + bz1416796

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.17-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.17-11
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 3 2018 Dalibor Pospisil <dapospis@redhat.com> - 1.17-9
- support rxvt terminal colors
- fixed persistent data load for bash version <= 4.1.2
- moved printing of final summray to rlJournalEnd
- extended coloring capabilities
- unified footer format

* Fri Jan 26 2018 Dalibor Pospisil <dapospis@redhat.com> - 1.17-7
- phase name sanitization (remove all weird characters)
- allow debug message to to only to console (speeds execution up in debug)
- allow to reboot inside of phase and continue there
- fixed persistent data loading

* Mon Dec 18 2017 Dalibor Pospisil <dapospis@redhat.com> - 1.17-6
- added missing dependecy

* Wed Dec 13 2017 Dalibor Pospisil <dapospis@redhat.com> - 1.17-5
- result file tweaks
- fixed ifs issue
- improved performance of journaling.py
- fixed computing the length of text text journal per phase
- use internal test name and do not touch TEST variable if empty
- omit human readable meta file comments in non-debug mode
- enable nested phases by default


* Fri Oct 20 2017 Dalibor Pospisil <dapospis@redhat.com> - 1.17-4
- updated dependecies set

* Wed Oct 18 2017 Dalibor Pospisil <dapospis@redhat.com> - 1.17-2
- completely reworked getting rpms
- bstor.py rewritten in pure bash
- some doc fixes
- completely rewritten journal
- extended test suite
- support for XSL transformation of journal.xml
- provided xunit.xsl
- libraries are now searched also in /usr/share/beakerlib-libraries

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 17 2017 Dalibor Pospisil <dapospis@redhat.com> - 1.16-3
- reworked rpm download function and fallbacks, bz1448510
- added links to bugzilla

* Fri Apr 21 2017 Dalibor Pospisil <dapospis@redhat.com> - 1.16-1
- added missing dependency
- updated links to beakerlib's new home, bz1436810
- added rlAssertLesser and rlAssertLesserOrEqual, bz1423488
- added rpm-handling functions rlFetchSrcForInstalled, rlRpmDownload, and rlRpmInstall

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Dalibor Pospisil <dapospis@redhat.com> - 1.15-1
- added rlIsCentOS similar to rlIsRHEL, bz1214190
- added missing dependencies, bz1391969
- make rlRun use internal variables with more unique name, bz1285804
- fix rlRun exitcodes while using various switches, bz1303900
- rlFileRestore now better distinquish betwwen various errorneous situations, bz1370453
- rlService* won't be blocked be less(1) while systemctl redirection is in place, bz1383303
- variable <libPrefix>LibraryDir variable is created for all imported libraries, holding the path to the library source, bz1074487
- all logging messages are now printed to stderr, bz1171881
- wildcard %%doc inclusion in spec, bz1206173
- prevent unbound variables, bz1228264
- new functions rlServiceEnabled/rlServiceDisable for enabling/disabling services, bz1234804
- updated documentation for rlImport -all, bz1246061
- rlAssertNotEquals now accept empty argument, bz1303618
- rlRun now uses better filename for output log, bz1314700
- fixed cosmetic discrepancy in log output, bz1374256
- added documentation reference for bkrdoc, bz843823
- added documentation of the testwatcher feature, bz1218169
- rlServiceRestore can restore all saved services in no parameter provided, bz494318
- rlCheckMount take mount options (ro/rw) into consideration, bz1191627
- added documentation for LOG_LEVEL variable, bz581816

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 29 2015 Dalibor Pospisil <dapospis@redhat.com> - 1.11-1
- fixed bugs  971347, 1076471, 1262888, 1216177, 1184414, 1192535, 1224345,
  1211269, 1224362, 1205330, 1175513, 1211617, 1221352

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 4 2015 Dalibor Pospisil <dapospis@redhat.com> - 1.10-2
- remount if mounting already mounted mount point with options,
  fixes bug 1173623

* Mon Dec 1 2014 Dalibor Pospisil <dapospis@redhat.com> - 1.10-1
- dropped support for rlSEBoolean functions
- fixed bugs 554280, 1003433, 1103137, 1105299, 1124440, 1124454, 1131934,
  1131963, 1136206, 1155158, 1155234, 1158464, 1159191, and 1165265

* Thu Jul 17 2014 Dalibor Pospisil <dapospis@redhat.com> - 1.9-3
- reverted conditional phases support

* Wed Jul 2 2014 Dalibor Pospisil <dapospis@redhat.com> - 1.9-2
- bunch of fixes

* Tue Jun 17 2014 Dalibor Pospisil <dapospis@redhat.com> - 1.9-1
- rebase to upstream 1.9

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 20 2013 Petr Muller <muller@redhat.com> - 1.8-4
- Fix docdir usage to comply with Unversioned Docdirs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.8-2
- Perl 5.18 rebuild

* Mon Jun 10 2013 Petr Muller <muller@redhat.com> - 1.8-1
- Update to new upstream version 1.8

* Thu May 09 2013 Petr Muller <muller@redhat.com> - 1.7-2
- Robustify journal to accept umlaut in distro release name
- Fix internal documentation

* Tue Apr 30 2013 Petr Muller <muller@redhat.com> - 1.7-1
- rebase to upstream 1.7

* Tue Mar 05 2013 Petr Muller <muller@redhat.com> - 1.6-3
- Build ceased to figure out pod2man dep automatically: fixed

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 25 2012 Petr Muller <muller@redhat.com> - 1.6-1
- Updated to new upstream version

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 02 2012 Petr Muller <pmuller@redhat.com> - 1.5-1
- update to new upstream version

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 01 2011 Petr Muller <pmuller@redhat.com> - 1.4-1
- update to new upstream version

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May 12 2010 Petr Muller <pmuller@redhat.com> - 1.3-1
- packaging fixes: permission fixes, added dep on python2,
- added examples as documentation files

* Thu Apr 29 2010 Petr Muller <pmuller@redhat.com> - 1.2-1
- packaging fixes: docdir change, specfile tweaks
- using consistently install -p everywhere

* Thu Apr 08 2010 Petr Muller <pmuller@redhat.com> - 1.2-0
- disable the testsuite and removed a 3rd party lib from the tree

* Mon Mar 22 2010 Petr Muller <pmuller@redhat.com> - 1.1-0
- packaging fixes

* Fri Feb 12 2010 Petr Muller <pmuller@redhat.com> - 1.0-3
- fixed bad path preventing tests from running

* Fri Feb 12 2010 Petr Muller <pmuller@redhat.com> - 1.0-2
- zillion of specfile tweaks for Fedora inclusion
- staf-rhts files were removed
- added a LICENSE file
- added a better package summary
- directory structure revamped
- improved rLDejaSum

* Wed Jan 27 2010 Petr Muller <pmuller@redhat.com> - 1.0-1
- genesis of the standalone BeakerLib
