%global libdnf_major_version 0
%global libdnf_minor_version 63
%global libdnf_micro_version 1

Name:           libdnf
Version:        %{libdnf_major_version}.%{libdnf_minor_version}.%{libdnf_micro_version}
Release:        2%{?dist}
Summary:        Library providing simplified C and Python API to libsolv.
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rpm-software-management/libdnf
#Source0:       %{url}/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  check
BuildRequires:  cmake
BuildRequires:  cppunit-devel
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glib-devel
BuildRequires:  gpgme-devel
BuildRequires:  json-c-devel
BuildRequires:  libmodulemd-devel
BuildRequires:  librepo-devel
BuildRequires:  libsolv-devel >= 0.7.19
BuildRequires:  python3-sphinx
BuildRequires:  rpm-devel
BuildRequires:  sqlite-devel

Requires:       libmodulemd
Requires:       libsolv
Requires:       librepo

%description
%{summary}

%package devel
Summary:        Development files for %{name}.
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libsolv-devel%{?_isa}

%description devel
%{summary}

%package -n python3-%{name}
Summary:        Python 3 bindings for the libdnf library.
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  swig

%description -n python3-%{name}
%{summary}

%package -n python3-hawkey
Summary:        Python 3 bindings for the hawkey library
BuildRequires:  python3-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3-%{name} = %{version}-%{release}

%description -n python3-hawkey
Python 3 bindings for the hawkey library.

%prep
%autosetup -p1
mkdir build-py3

%build
# Allows cmake to find libsolv.
find %{_prefix} -name "FindLibSolv.cmake" -exec cp {} cmake/modules ';'

pushd build-py3
%cmake \
  -DPYTHON_DESIRED:FILEPATH="3" \
  -DWITH_GIR=0 \
  -DWITH_MAN=OFF \
  -DWITH_HTML=OFF \
  -DWITH_ZCHUNK=OFF \
  -DWITH_GTKDOC=OFF \
  -DDISABLE_VALGRIND=1 \
  -DENABLE_RHSM_SUPPORT=OFF \
  -DLIBDNF_MAJOR_VERSION=%{libdnf_major_version} \
  -DLIBDNF_MINOR_VERSION=%{libdnf_minor_version} \
  -DLIBDNF_MICRO_VERSION=%{libdnf_micro_version} \
  ..
%make_build
popd

%install
pushd build-py3
  %make_install
popd

%find_lang %{name}

%check
pushd build-py3
  make ARGS="-V" test
popd

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING
%doc README.md AUTHORS
%{_libdir}/%{name}.so.2*
%dir %{_libdir}/libdnf/
%dir %{_libdir}/libdnf/plugins/
%{_libdir}/libdnf/plugins/README

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files -n python3-%{name}
%{python3_sitelib}/%{name}/

%files -n python3-hawkey
%{python3_sitelib}/hawkey/

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.63.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Sep 14 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.63.1-1
- Upgrade to latest upstream version
- Lint spec

* Tue Jul 06 2021 Henry Li <lihl@microsoft.com> - 0.43.1-2
- Patch CVE-2021-3445

* Mon Aug 17 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.43.1-1
- Updating to version 0.43.1.

* Mon May 04 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.39.1-1
- Updating to version 0.39.1.

* Fri Apr 17 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.35.3-7
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Added 'Distribution' and 'Vendor' tags.
- Fixed "Source0" tag.
- License verified.

* Mon Oct 21 2019 Ales Matej <amatej@gmail.com> - 0.35.3-6
- Fixes for some issues on Arm platforms (RhBug:1691430) 

* Sat Sep 14 2019 Jonathan Dieter <jdieter@gmail.com> - 0.35.3-5
- Set LRO_CACHEDIR so zchunk works again

* Wed Sep 11 2019 Jaroslav Mracek <jmracek@redhat.com> - 0.35.3-4
- Backport patch to fix reinstalling packages with a different buildtime - part II

* Tue Sep 10 2019 Jaroslav Mracek <jmracek@redhat.com> - 0.35.3-3
- Backport patch to fix reinstalling packages with a different buildtime

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.35.3-2
- Rebuilt for Python 3.8

* Tue Aug 13 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.35.3-1
- Update to 0.35.3
- Make libdnf own its plugin directory (RhBug:1714265)
- Don't disable nonexistent but required repositories (RhBug:1689331)
- Set priority of dnf.conf.d drop-ins
- Fix toString() to not insert [] (RhBug:1584442)
- Ignore trailing blank lines in config (RhBug:1722493)
- Fix handling large number of filenames on input (RhBug:1690915)
- Detect armv7 with crypto extension only on arm version >= 8
- A new standardized User-Agent field consisting of the libdnf and OS version
  (including the variant) (RhBug:1156007)
- Add basic countme support (RhBug:1647454)

* Mon Jul 29 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.35.1-4
- Rebuilt for librepo 1.10.5

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.35.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.35.1-2
- Backport patch to fix attaching and detaching of libsolvRepo and
  repo_internalize_trigger() (RhBug:1727343,1727424)

* Thu Jul 04 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.35.1-1
- Update to 0.35.1
- Enhance logging handling
- Do not log DEBUG messages by default
- Also add subkeys when adding GPG keys
- [module] Fix swig binding for getModuleDependencies()
- Skip invalid key files in "/etc/pki/rpm-gpg" with warning (RhBug:1644040)
- Enable timestamp preserving for downloaded data (RhBug:1688537)
- Set default to skip_if_unavailable=false (RhBug:1679509)
- Add configuration option skip_if_unavailable (RhBug:1689931)
- Fix 'database is locked' error (RhBug:1631533)
- Replace the 'Failed to synchronize cache' message (RhBug:1712055)
- Fix 'no such table: main.trans_cmdline' error (RhBug:1596540)
- Add support of modular FailSafe (RhBug:1623128) (temporarily with warnings
  instead of errors when installing modular RPMs without modular metadata)
- Add support of DNF main config file in context; used by PackageKit and
  microdnf (RhBug:1689331)
- Exit gpg-agent after repokey import (RhBug:1650266)

* Mon Jun 10 22:13:19 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.31.0-5
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:02 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.31.0-4
- Rebuild for RPM 4.15

* Fri May 03 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.31.0-3
- Backport patches to reintroduce hawkeyRepo

* Thu Apr 25 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.31.0-1
- Update to 0.31.0
- Installroot now requires absolute path
- Support "_none_" value for repo option "proxy" (RhBug:1680272)
- Add support for Module advisories
- Add support for xml:base attribute from primary.xml (RhBug:1691315)
- Improve detection of Platform ID (RhBug:1688462)

* Wed Mar 27 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.28.1-1
- Update to 0.28.1
- Return empty query if incorrect reldep (RhBug:1687135)
- ConfigParser: Improve compatibility with Python ConfigParser and dnf-plugin-spacewalk (RhBug:1692044)
- ConfigParser: Unify default set of string represenation of boolean values
- Fix segfault when interrupting dnf process (RhBug:1610456)

* Mon Mar 11 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.28.0-1
- Update to 0.28.0
- Exclude module pkgs that have conflict
- Enhance config parser to preserve order of data, and keep comments and format
- Improve ARM detection
- Add support for SHA-384

* Tue Feb 19 2019 Jaroslav Mracek <jmracek@redhat.com> - 0.26.0-2
- Backport patches for zchunk

* Wed Feb 13 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.26.0-1
- Update to 0.26.0-1
- Enhance modular solver to handle enabled and default module streams differently (RhBug:1648839)
- Add support of wild cards for modules (RhBug:1644588)
- Revert commit that adds best as default behavior

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.24.1-1
- Update to 0.24.1
- Add support for zchunk
- Enhance LIBDNF plugins support
- Enhance sorting for module list (RhBug:1590358)
- [repo] Check whether metadata cache is expired (RhBug:1539620,1648274)
- [DnfRepo] Add methods for alternative repository metadata type and download (RhBug:1656314)
- Remove installed profile on module  enable or disable (RhBug:1653623)
- [sack] Implement dnf_sack_get_rpmdb_version()

* Thu Nov 22 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.22.3-1
- Permanently disable Python2 build for Fedora 30+
- Update to 0.22.3
- Modify solver_describe_decision to report cleaned (RhBug:1486749)
- [swdb] create persistent WAL files (RhBug:1640235)
- Relocate ModuleContainer save hook (RhBug:1632518)
- [transaction] Fix transaction item lookup for obsoleted packages (RhBug: 1642796)
- Fix memory leaks and memory allocations
- [repo] Possibility to extend downloaded repository metadata

* Wed Nov 07 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.22.0-8
- Backport fixes for RHBZ#1642796 from upstream master

* Tue Oct 30 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.22.0-7
- Rebuild for libsolv 0.7

* Tue Oct 23 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.22.0-6
- Add patch Relocate-ModuleContainer-save-hook-RhBug1632518
- Add patch Test-if-sack-is-present-and-run-save-module-persistor-RhBug1632518

* Sat Oct 20 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.22.0-5
- remove problematic patch Relocate-ModuleContainer-save-hook-RhBug1632518

* Fri Oct 19 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.22.0-4
- backport Relocate-ModuleContainer-save-hook-RhBug1632518

* Thu Oct 18 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.22.0-3
- bacport swdb-create-persistent-WAL-files-RhBug1640235

* Wed Oct 17 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.22.0-2
- backport Modify-solver_describe_decision-to-report-cleaned-RhBug1486749
- backport history-Fix-crash-in-TransactionItemaddReplacedBy

* Mon Oct 15 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.22.0-1
- Update to 0.22.0
- Fix segfault in repo_internalize_trigger (RhBug:1375895)
- Change sorting of installonly packages (RhBug:1627685)
- [swdb] Fixed pattern searching in history db (RhBug:1635542)
- Check correctly gpg for repomd when refresh is used (RhBug:1636743)
- [conf] Provide additional VectorString methods for compatibility with Python list.
- [plugins] add plugin loading and hooks into libdnf

* Sat Sep 29 2018 Kevin Fenzi <kevin@scrye.com> - 0.20.0-2
- Temp re-enable python2 subpackages to get rawhide composing again.

* Tue Sep 25 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.20.0-1
- [module] Report module solver errors
- [module] Enhance module commands and errors
- [transaction] Fixed several problems with SWDB
- Remove unneeded regex URL tests (RhBug:1598336)
- Allow quoted values in ini files (RhBug:1624056)
- Filter out not unique set of solver problems (RhBug:1564369)
- Disable python2 build for Fedora 30+

* Tue Sep 18 2018 Adam Williamson <awilliam@redhat.com> - 0.19.1-3
- Backport PR #585 for an update crash bug (#1629340)

* Fri Sep 14 2018 Kalev Lember <klember@redhat.com> - 0.19.1-2
- Backport a fix for a packagekit crasher / F29 Beta blocker (#1626851)

* Mon Sep 10 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.19.1-1
- Fix compilation errors on gcc-4.8.5
- [module] Allow module queries on disabled modules

* Fri Sep 07 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.19.0-1
- [query] Reldeps can contain a space char (RhBug:1612462)
- [transaction] Avoid adding duplicates via Transaction::addItem()
- Fix compilation errors on gcc-4.8.5
- [module] Make available ModuleProfile using SWIG
- [module] Redesign module disable and reset

* Mon Aug 13 2018 Daniel Mach <dmach@redhat.com> - 0.17.2-1
- [sqlite3] Change db locking mode to DEFAULT.
- [doc] Add libsmartcols-devel to devel deps.

* Mon Aug 13 2018 Daniel Mach <dmach@redhat.com> - 0.17.1-1
- [module] Solve a problem in python constructor of NSVCAP if no version.
- [translations] Update translations from zanata.
- [transaction] Fix crash after using dnf.comps.CompsQuery and forking the process in Anaconda.
- [module] Support for resetting module state.
- [output] Introduce wrapper for smartcols.

* Fri Aug 10 2018 Adam Williamson <awilliam@redhat.com> - 0.17.0-2
- Backport fix that prevented anaconda running dnf in a subprocess (#546)

* Tue Aug 07 2018 Daniel Mach <dmach@redhat.com> - 0.17.0-1
- [conf] Add module_platform_id option.
- [module] Add ModulePackageContainer class.
- [module] Add ModulePersistor class.
- [sack] Module filtering made available in python API
- [sack] Module auto-enabling according to installed packages

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.16.1-3
- Rebuild for new binutils

* Fri Jul 27 2018 Daniel Mach <dmach@redhat.com> - 0.16.1-2
- [module] Implement 'module_hotfixes' conf option to skip filtering RPMs from hotfix repos.
- [goal] Fix distupgrade filter, allow downgrades.
- [context] Allow to set module platform in context.
- [module] Introduce proper modular dependency solving.
- [module] Platform pseudo-module based on /etc/os-release.
- [goal] Add Goal::listSuggested().
- [l10n] Support for translations, add gettext build dependency.

* Sun Jul 22 2018 Daniel Mach <dmach@redhat.com> - 0.16.0-1
- Fix RHSM plugin
- Add support for logging
- Bump minimal libmodulemd version to 1.6.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.15.2-1
- Update to 0.15.1
- Resolves: rhbz#1595487

* Fri Jun 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.15.1-2
- Restore proper ldconfig_scriptlets

* Tue Jun 26 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.15.1-1
- Update to 0.15.1

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 0.11.1-6
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Igor Gnatenko <ignatenko@redhat.com> - 0.11.1-4
- Switch to %%ldconfig_scriptlets

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.11.1-3
- Use better Obsoletes for platform-python

* Fri Nov 03 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.11.1-2
- Remove platform-python subpackage

* Mon Oct 16 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.11.1-1
- Rerelease of 0.11.1-1
- Improvement query performance
- Run file query in hy_subject_get_best_solution only for files (arguments that start with ``/`` or
  ``*/``)
- Resolves: rhbz#1498207 - DNF crash during upgrade installation F26 -> F27

* Tue Oct 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.11.0-1
- Update to 0.11.0

* Mon Oct 02 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.10.1-2
- Rerelease of 0.10.1-1

* Wed Sep 27 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.10.1-1
- Update to 0.10.1
- It improves query performance with name and arch filters. Also nevra filter will now
  handle string with or without epoch.
- Additionally for python bindings it renames NEVRA._has_just_name() to NEVRA.has_just_name() due
  to movement of code into c part of library.
- Resolves: rhbz#1260242 - --exclude does not affect dnf remove's removal of requirements
- Resolves: rhbz#1485881 - DNF claims it cannot install package, which have been already installed
- Resolves: rhbz#1361187 - [abrt] python-ipython-console: filter_updown(): python3.5 killed by SIGABRT

* Fri Sep 15 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.3-8
- Disable platform python on old releases

* Tue Aug 15 2017 Lumír Balhar <lbalhar@redhat.com> - 0.9.3-7
- Add platform-python subpackage

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.3-6
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.3-5
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.3-4
- Rebuilt for RPM soname bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.9.3-1
- Update to 0.9.3

* Sat Jul 01 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.2-1
- Update to 0.9.2

* Mon Jun 12 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.9.1-1
- Update to 0.9.1

* Mon May 22 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Tue May 02 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.8.2-1
- Update to 0.8.2

* Fri Mar 24 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Tue Mar 21 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Mon Feb 20 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.4-1
- Update to 0.7.4

* Fri Feb 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Wed Feb 08 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.2-1
- 0.7.2

* Fri Jan 06 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.1-1
- 0.7.1

* Wed Dec 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> - 0.7.0-0.7gitf9b798c
- Rebuild for Python 3.6

* Mon Dec 19 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.7.0-0.6gitf9b798c
- Use new upstream URL

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.7.0-0.5gitf9b798c
- Rebuild for Python 3.6

* Tue Dec 06 2016 Martin Hatina <mhatina@redhat.com> - 0.7.0-0.4gitf9b798c
- Increase conflict version of dnf

* Thu Dec 01 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.7.0-0.3gitf9b798c
- Update to latest snapshot

* Fri Nov 04 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.7.0-0.2git8bd77f8
- Update to latest snapshot

* Thu Sep 29 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.7.0-0.1git179c0a6
- Initial package
