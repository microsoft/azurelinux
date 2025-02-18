# pass --without tests to skip the test suite
%bcond_without tests

Name:           rpmlint
Version:        2.5.0
Release:        10%{?dist}
Summary:        Tool for checking common errors in RPM packages
License:        GPL-2.0-or-later
URL:            https://github.com/rpm-software-management/rpmlint
Source0:        %{url}/archive/%{version}/rpmlint-%{version}.tar.gz
# Taken from https://github.com/rpm-software-management/rpmlint/tree/main/configs/Fedora
Source1:        fedora.toml
Source3:        scoring.toml
Source4:        users-groups.toml
Source5:        warn-on-functions.toml

# Fix from @danigm to reset checks for each package
# https://github.com/rpm-software-management/rpmlint/pull/1163
Patch0:         https://patch-diff.githubusercontent.com/raw/rpm-software-management/rpmlint/pull/1163.patch

BuildArch:      noarch

# use git to apply patches; it handles binary diffs
BuildRequires:  git-core
BuildRequires:  python3-devel
# tests
%if %{with tests}
%if ! 0%{?rhel}
BuildRequires:  dash
BuildRequires:  devscripts-checkbashisms
%endif
BuildRequires:  hunspell-cs
BuildRequires:  hunspell-en-US
BuildRequires:  python3dist(pytest)
%if ! 0%{?rhel}
BuildRequires:  python3dist(pytest-xdist)
%endif
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/desktop-file-validate
%endif
%if ! 0%{?rhel}
Requires:       dash
Requires:       devscripts-checkbashisms
%endif
Requires:       rpm-build
Requires:       /usr/bin/appstream-util
Requires:       /usr/bin/desktop-file-validate
%if 0%{?fedora}
Requires:       rpmlint-fedora-license-data
%endif

%description
rpmlint is a tool for checking common errors in RPM packages. Binary
and source packages as well as spec files can be checked.

%prep
%autosetup -p1 -Sgit

# Replace python-magic dep with file-magic (rhbz#1899279)
sed -i 's/python-magic/file-magic/g' pyproject.toml

%if 0%{?rhel}
# Avoid extra dependencies for checks not needed in RHEL
# pybeam: ErlangCheck
sed -i -e '/pybeam/d' pyproject.toml
sed -i -e '/ErlangCheck/d' rpmlint/configdefaults.toml test/test_lint.py
%endif

# Don't lint the code or measure coverage in %%check
# On RHEL, also avoid xdist by disabling parallelism
sed -i -e '/^ *--cov=rpmlint$/d' %{?rhel:-e '/^ *-n auto$/d'} pytest.ini

# Avoid warnings about pytest.mark.no_cover marker
sed -i '/^@pytest.mark.no_cover/d' test/test_lint.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{name}

mkdir -p %{buildroot}%{_sysconfdir}/xdg/rpmlint/
%if 0%{?fedora}
cp -a %{SOURCE1} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{buildroot}%{_sysconfdir}/xdg/rpmlint/
%endif

%check
%if %{with tests}
%pytest %{?rhel:--ignore test/test_erlang.py}
%endif

%files -f %{pyproject_files}
%doc README.md
%dir %{_sysconfdir}/xdg/rpmlint
%if 0%{?fedora}
%config(noreplace) %{_sysconfdir}/xdg/rpmlint/*.toml
%endif
%{_bindir}/rpmdiff
%{_bindir}/rpmlint

%changelog
* Wed Dec 11 2024 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-10
- Fixup a bad regex in the spelling errors filter

* Wed Dec 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.5.0-9
- Add more jargon to the filtered-out spelling errors

* Wed Nov 13 2024 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-8
- Filter out more common false positive spelling-errors

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 2.5.0-6
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-5
- Filter out python-missing-require warnings,
  Fedora's style of Python requirements is not supported
- Resolves: rhbz#2260169

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan  4 2024 Tom Callaway <spot@fedoraproject.org> - 2.5.0-3
- reset checks after each package, thanks to Daniel García Moreno

* Sat Nov 25 2023 Zephyr Lykos <fedora@mochaa.ws> - 2.5.0-2
- Migrate patches to pyproject.toml (rhbz#1899279)

* Tue Nov 21 2023 Tom Callaway <spot@fedoraproject.org> - 2.5.0-1
- update to 2.5.0

* Mon Jul 24 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.0-11
- Disable ErlangCheck by default in RHEL builds

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2.4.0-9
- Rebuilt for Python 3.12

* Thu May 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.0-8
- Limit deps and don't ship Fedora config in RHEL builds

* Thu May 25 2023 Todd Zullinger <tmz@pobox.com> - 2.4.0-7
- adjust for rpm-4.19.0 API changes

* Mon Mar 20 2023 Todd Zullinger <tmz@pobox.com> - 2.4.0-6
- handle license exception in grouping, better (rhbz#2175241)

* Mon Mar 06 2023 Todd Zullinger <tmz@pobox.com> - 2.4.0-5
- handle license exception in grouping (rhbz#2175241)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Oct 07 2022 Todd Zullinger <tmz@pobox.com> - 2.4.0-3
- disable various errors/warnings for debug/devel packages
- fix broken regex for no-manual-page-for-binary check (rhbz#2132936)
- ignore missing-hash-section error (rhbz#2132969)

* Wed Oct 05 2022 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-2
- remove the license list, depend on rpmlint-fedora-license-data instead

* Tue Oct 04 2022 Todd Zullinger <tmz@pobox.com> - 2.4.0-1
- update to 2.4.0 (rhbz#2088759)
- use python build-dependency generator
- own %%{_sysconfdir}/xdg/rpmlint directory

* Sat Sep 24 2022 Todd Zullinger <tmz@pobox.com> - 2.3.0-1
- update to 2.3.0 (rhbz#2088759)
- convert license to SPDX and correct to GPL-2.0-or-later
- enable tests by default, avoid warnings about pytest.mark.no_cover marker

* Sat Sep 24 2022 Tom Callaway <spot@fedoraproject.org> - 2.2.0-7
- update licenses.toml to reflect change in Fedora licensing identifiers

* Mon Aug 08 2022 Miro Hrončok <mhroncok@redhat.com> - 2.2.0-6
- Require desktop-file-validate to avoid a fatal error when the RPM has .desktop files

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 2.2.0-4
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan  6 2022 Tom Callaway <spot@fedoraproject.org> - 2.2.0-2
- disable no-library-dependency-for/on checks in Fedora

* Thu Dec 09 2021 Stephen Smoogen <ssmoogen@redhat.com> - 2.2.0-1
- Update to upstream 2.2.0

* Tue Dec 07 2021 Neal Gompa <ngompa@fedoraproject.org> - 2.1.0-6
- Fix some rpmlint policy issues

* Tue Oct  5 2021 Tom Callaway <spot@fedoraproject.org> - 2.1.0-5
- add explicit Requires for pyenchant

* Thu Sep 16 2021 Tom Callaway <spot@fedoraproject.org> - 2.1.0-4
- fix rpmlintrc load from cmdline option (bz2000018)

* Sun Sep 05 2021 Miro Hrončok <mhroncok@redhat.com> - 2.1.0-3
- Ignore hidden-file-or-dir for .cargo-checksum.json

* Tue Aug 17 2021 Tom Callaway <spot@fedoraproject.org> - 2.1.0-2
- include iso-639-2 collective language codes in LANGUAGES

* Tue Aug 17 2021 Tom Callaway <spot@fedoraproject.org> - 2.1.0-1
- update to 2.1.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul  7 2021 Tom Callaway <spot@fedoraproject.org> - 2.0.0-5
- add Requires: rpm-build

* Thu Jul  1 2021 Tom Callaway <spot@fedoraproject.org> - 2.0.0-4
- fix rpmlint -i where it wrongly assumes a tmp dir

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.0-3
- Rebuilt for Python 3.10

* Fri Jun  4 2021 Tom Callaway <spot@fedoraproject.org> - 2.0.0-2
- add dash and checkbashisms as Requires

* Thu Jun  3 2021 Tom Callaway <spot@fedoraproject.org> - 2.0.0-1
- update to 2.0.0

* Tue May 11 2021 Todd Zullinger <tmz@pobox.com> - 1.11-17
- use proper folder _sourcedir for spec files (upstream PR#633)
  Resolves: rhbz#1959363

* Tue Apr 13 2021 Miro Hrončok <mhroncok@redhat.com> - 1.11-16
- Filter out empty specfile-errors, they are duplicates

* Fri Feb  5 2021 Tom Callaway <spot@fedoraproject.org> - 1.11-15
- correct hard-coded version in Makefile

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Miro Hrončok <mhroncok@redhat.com> - 1.11-13
- Filter out empty py.typed files in Python site-packages

* Fri Aug 21 2020 Miro Hrončok <mhroncok@redhat.com> - 1.11-12
- Filter out empty REQUESTED files in pip installed Python metadata dist-info dirs

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Miro Hrončok <mhroncok@redhat.com> - 1.11-10
- Don't use the %%python_sitelib macro, because it errors
- See https://fedoraproject.org/wiki/Changes/PythonMacroError

* Tue Jun 23 2020 Tom Callaway <spot@fedoraproject.org> - 1.11-9
- use python3-file-magic on f33+

* Tue Jun 16 2020 Tom Callaway <spot@fedoraproject.org> - 1.11-8
- turn *-not-linked-against-libc from errors to warnings (bz1749738)

* Wed Jun 10 2020 Tom Callaway <spot@fedoraproject.org> - 1.11-7
- add /usr/bin/python[23] as valid shells

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.11-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.11-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Tom Callaway <spot@fedoraproject.org> - 1.11-2
- merge conflig file cleanups from PR

* Fri Jun 21 2019 Tom Callaway <spot@fedoraproject.org> - 1.11-1
- update to 1.11

* Sun Mar 10 2019 Miro Hrončok <mhroncok@redhat.com> - 1.10-22
- Suppress locale error in order to work in default mock (#1668400)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Tom Callaway <spot@fedoraproject.org> - 1.10-20
- ignore info-files-without-install-info-postin/postun checks

* Fri Dec  7 2018 Tom Callaway <spot@fedoraproject.org> - 1.10-19
- ignore non-standard-dir-perm error for 700 dirs in /etc and /var/lib

* Fri Oct  5 2018 Tom Callaway <spot@fedoraproject.org> - 1.10-18
- force python3 as exec binary

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.10-16
- Rebuilt for Python 3.7

* Sun Jun 17 2018 Todd Zullinger <tmz@pobox.com> - 1.10-15
- Fix mixed-use-of-spaces-and-tabs warning (in this spec file)
- Remove el4/el5 configs and /usr/bin symlinks
- Disable automatic compilation of Python files in /usr/share/rpmlint
- Fix non-ghost-in-run filter in config

* Tue Jun 12 2018 Miro Hrončok <mhroncok@redhat.com> - 1.10-14
- apply upstream fix for python 3.7 new magic numbers

* Sat Jun  2 2018 Tom Callaway <spot@fedoraproject.org> 1.10-13
- apply upstream fix for python 3.7 mtime handling

* Thu May 03 2018 Todd Zullinger <tmz@pobox.com> - 1.10-12
- Properly handle the exception on missing files (bz1574509)
- Explicitly disable the non-standard-group check

* Wed Apr 18 2018 Todd Zullinger <tmz@pobox.com>
- Ignore 'no-documentation' in debugsource packages
- Ignore /usr/src/debug/ in debugsource packages

* Tue Apr 17 2018 Tom Callaway <spot@fedoraproject.org> - 1.10-11
- disable library-without-ldconfig-postin/postun checks (F28+)

* Tue Apr 17 2018 Tom Callaway <spot@fedoraproject.org> - 1.10-10
- fix flake errors (merge upstream changes)

* Mon Apr 16 2018 Todd Zullinger <tmz@pobox.com> - 1.10-9
- Update UsrLibBinaryException config to include .build-id
- Ignore useless-provides on debuginfo provides (bz1489096)

* Sun Mar 04 2018 Till Maas <opensource@till.name> - 1.10-8
- Update URL (RH #1547150)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Karsten Hopp <karsten@redhat.com> - 1.10-6
- fix python3 conditional

* Sun Oct 29 2017 Tom Callaway <spot@fedoraproject.org> - 1.10-5
- ignore common jargon words in spellcheck

* Sun Oct 29 2017 Tom Callaway <spot@fedoraproject.org> - 1.10-4
- fix SSL_CTX_set_cipher_list waiver
- use raw strings in config file to silence python3 deprecation warnings

* Mon Sep 11 2017 Tom Callaway <spot@fedoraproject.org> - 1.10-3
- use correct config file option for debugsource

* Fri Sep  8 2017 Tom Callaway <spot@fedoraproject.org> - 1.10-2
- update config file to reflect new licenses and to ignore devel files in debugsource packages

* Tue Sep  5 2017 Tom Callaway <spot@fedoraproject.org> - 1.10-1
- update to 1.10

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Tom Callaway <spot@fedoraproject.org> - 1.9-11
- apply upstream fix for buildid

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 1.9-10
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Fri Apr 07 2017 Björn Esser <besser82@fedoraproject.org> - 1.9-9
- Upstream fix for str object has no attribute decode (bz1439941)

* Thu Mar 9 2017 Charalampos Stratakis <cstratak@redhat.com> - 1.9-8
- Update Python 3.5.3 magic bytecode value

* Wed Feb  8 2017 Tom Callaway <spot@fedoraproject.org> - 1.9-7
- apply upstream fix to not demand versioned filename Provides/Obsoletes

* Thu Dec 29 2016 Adam Williamson <awilliam@redhat.com> - 1.9-6
- Update Python 3.6 magic bytecode value (github PR #7)

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.9-5
- Rebuild for Python 3.6

* Mon Oct 24 2016 Orion Poplawski <orion@cora.nwra.com> - 1.9-4
- Use %%license
- BR python-flake8-import-order for tests

* Fri Aug 26 2016 Tom Callaway <spot@fedoraproject.org> - 1.9-3
- ignore long description lines for debuginfo packages

* Mon Jul 25 2016 Tom Callaway <spot@fedoraproject.org> - 1.9-2
- fix 403 ignore rule for github to be more complete (bz1359582)

* Wed Jul  6 2016 Tom Callaway <spot@fedoraproject.org> - 1.9-1
- update to 1.9

* Tue Jun 14 2016 Tom Callaway <spot@fedoraproject.org> - 1.8-7
- ignore explicit-lib-dependency on python subpackages with "lib"
- update license list

* Mon Apr 18 2016 Tom Callaway <spot@fedoraproject.org> - 1.8-6
- update license list
- add github.com to the filter ignore list for 403 errors (bz1326855)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Sep 28 2015 Tom Callaway <spot@fedoraproject.org> - 1.8-2
- fix issue in config regex causing bitbucket URLs to slip through invalid-url filter

* Fri Sep 25 2015 Tom Callaway <spot@fedoraproject.org> - 1.8-1
- 1.8
- add bad crypto warning to config file
- update license list

* Fri Jul 10 2015 Tom Callaway <spot@fedoraproject.org> - 1.7-1
- 1.7
- add python conditionals

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Tom Callaway <spot@fedoraproject.org> - 1.6-3
- filter out failure from broken webservers
- add new licenses

* Tue Dec  9 2014 Tom Callaway <spot@fedoraproject.org> - 1.6-2
- update license list in config file

* Thu Sep  4 2014 Tom Callaway <spot@fedoraproject.org> - 1.6-1
- update to 1.6

* Wed Jun 25 2014 Tom Callaway <spot@fedoraproject.org> - 1.5-12
- add systemd to UsrLibBinaryException

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Tom Callaway <spot@fedoraproject.org> - 1.5-10
- fix python 3.4 magic number (#1102846)

* Mon May 12 2014 Tom Callaway <spot@fedoraproject.org> - 1.5-9
- update config to ignore non-readable /etc/ovirt-engine/isouploader.conf

* Mon Feb 10 2014 Tom Callaway <spot@fedoraproject.org> - 1.5-8
- filter out broken-syntax-in-scriptlet-requires (except on el4/5)
- update license list

* Sun Feb  9 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.5-7
- Make default config Python 3 compatible.

* Thu Dec 12 2013 Tom Callaway <spot@fedoraproject.org> - 1.5-6
- fix unicode naming bug (bz 1036310)

* Mon Nov 11 2013 Tom Callaway <spot@fedoraproject.org> - 1.5-5
- do not modify sys.argv[0] (bz 1026333)
- fix unbound var in MenuXDGCheck.py (bz 1026328)

* Wed Oct  9 2013 Tom Callaway <spot@fedoraproject.org> - 1.5-4
- Fix handling of Exec= with an absolute path (bz991278)
- Update license list, add AGPLv3+ (bz894187)

* Tue Aug  6 2013 Thomas Woerner <twoerner@redhat.com> - 1.5-3
- Fixed URL and Source0, now using sourceforge.net

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 17 2013 Tom Callaway <spot@fedoraproject.org> - 1.5-1
- update to 1.5

* Mon Apr  1 2013 Tom Callaway <spot@fedoraproject.org> - 1.4-14
- explicitly Require: perl (bz919865)
- fix lua binary detection (bz919869)

* Wed Mar  6 2013 Tom Callaway <spot@fedoraproject.org> - 1.4-13
- update license list
- exclude non-config files that live in /etc

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov  6 2012 Tom Callaway <spot@fedoraproject.org> - 1.4-11
- add Requires: %%{_bindir}/groff for man page checks (bz 873448)

* Thu Sep  6 2012 Tom Callaway <spot@fedoraproject.org> - 1.4-10
- fix handling of ruby RI files as text files (they are binary files)
- apply upstream fix for macro regexp

* Tue Sep  4 2012 Thomas Woerner <twoerner@redhat.com> - 1.4-9
- fix build for RHEL: no bash-completion

* Tue Aug 14 2012 Tom Callaway <spot@fedoraproject.org> - 1.4-8
- add magic number fix for python 3 (bz845972)
- update license list

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-6
-  Patch to fix messages that contain unicode summaries
   https://bugzilla.redhat.com/show_bug.cgi?id=783912

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Tom Callaway <spot@fedoraproject.org> - 1.4-4
- Do not throw an error on .desktop files set +x. (bz 767978)

* Mon Dec  5 2011 Tom Callaway <spot@fedoraproject.org> - 1.4-3
- own %%{_datadir}/bash-completion/ (thanks Ville Skyttä)

* Mon Dec  5 2011 Tom Callaway <spot@fedoraproject.org> - 1.4-2
- add BR: bash-completion for the pc file

* Mon Dec  5 2011 Tom Callaway <spot@fedoraproject.org> - 1.4-1
- update to 1.4

* Wed Oct 12 2011 Tom Callaway <spot@fedoraproject.org> - 1.3-2
- apply upstream fix for false error on checking ghosted man pages for 
  encoding (bz745446)
- update config to reflect new licenses (bz741298)

* Tue Jul 12 2011 Tom Callaway <spot@fedoraproject.org> - 1.3-1
- update to 1.3

* Sun Apr 24 2011 Tom Callaway <spot@fedoraproject.org> - 1.2-1
- update to 1.2
- filter away files-attr-not-set for all targets except EL-4 (bz694579)

* Thu Mar  3 2011 Tom Callaway <spot@fedoraproject.org> - 1.1-3
- apply upstream fix for source url aborts (bz 680781)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Tom Callaway <spot@fedoraproject.org> - 1.1-1
- update to 1.1

* Tue Dec  7 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-3
- fix typo in changelog
- %% comment out item in changelog
- simplify el4/el5 config files (thanks to Ville Skyttä)

* Mon Dec  6 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-2
- add support for el4-rpmlint, el5-rpmlint
- disable no-cleaning-of-buildroot checks for Fedora
- disable no-buildroot-tag check for Fedora
- disable no-%%clean-section check for Fedora

* Mon Nov  1 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.0-1
- Update to 1.0; fixes #637956, and #639823.
- Sync Fedora license list with Wiki revision 1.85.
- Whitelist more expectedly setuid executables; fixes #646455.

* Thu Aug 19 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.99-1
- Update to 0.99; fixes #623607, helps work around #537430.
- Sync Fedora license list with Wiki revision 1.80.

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 0.98-2
- recompiling .py files against Python 2.7 (rhbz#623355)

* Wed Jun 23 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.98-1
- Update to 0.98; fixes #599427 and #599516.
- Filter out all lib*-java and lib*-python explicit-lib-dependency messages.
- Sync Fedora license list with Wiki revision 1.75; fixes #600317.

* Tue May 18 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.97-1
- Update to 0.97; fixes #459452, #589432.
- Filter out explicit-lib-dep messages for libvirt(-python) (Dan Kenigsberg).
- Sync Fedora license list with Wiki revision 1.73.

* Thu Apr 22 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.96-1
- Update to 0.96; fixes #487974, #571375, #571386, #572090, #572097, #578390.
- Sync Fedora license list with Wiki revision 1.71.

* Sat Mar  6 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.95-2
- Patch to fix non-coherent-filename regression for source packages.

* Wed Mar  3 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.95-1
- Update to 0.95; fixes #564585, #567285, #568498, and #570086.

* Mon Feb  1 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.94-1
- Update to 0.94; rpm >= 4.8.0 spec file check fix included upstream.
- Sync Fedora license list with Wiki revision 1.65 (#559156).

* Tue Jan 26 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.93-2
- Apply upstream patch to fix spec file check with rpm >= 4.8.0.

* Mon Jan 25 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.93-1
- Update to 0.93; fixes #531102 and #555284.
- Enable checks requiring network access in default config.
- Disallow kernel module packages in default config.
- Remove old X11R6 dirs from paths treated as system ones in default config.
- Sync Fedora license list with Wiki revision 1.64.
- Omit python-enchant and python-magic dependencies when built on EL.

* Mon Nov  2 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.92-1
- Update to 0.92; fixes #528535, and #531102 (partially).
- Python byte compile patch applied/superseded upstream.
- Add <lua> to list of valid scriptlet shells.
- Sync Fedora license list with Wiki revision 1.53.

* Mon Sep 14 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.91-1
- Update to 0.91; fixes #513811, #515185, #516492, #519694, and #521630.
- Add dependencies on gzip, bzip2, and xz.
- Sync Fedora license list with Wiki revision 1.49.
- Move pre-2008 %%changelog entries to CHANGES.package.old.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.90-1
- 0.90; fixes #508683.

* Sun Jun 21 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.89-1
- Update to 0.89; fixes #461610, #496735, #496737 (partially), #498107,
  #491188, and #506957.
- Sync Fedora license list with Wiki revision 1.44.
- Parse list of standard users and groups from the setup package's uidgid file.

* Thu Mar 19 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.87-1
- 0.87; fixes #480664, #483196, #483199, #486748, #488146, #488930, #489118.
- Sync Fedora license list with Wiki revision 1.38.
- Configs patch included upstream.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Ville Skyttä <ville.skytta@iki.fi>
- Sync Fedora license list with Wiki revision 1.34.
- Filter out filename-too-long-for-joliet and symlink-should-be-* warnings in
  default config.

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.85-3
- Rebuild for Python 2.6

* Thu Oct 30 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.85-2
- Apply upstream patch to load all *config from /etc/rpmlint.

* Thu Oct 23 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.85-1
- 0.85, fixes #355861, #450011, #455371, #456843, #461421, #461423, #461434.
- Mute some explicit-lib-dependency false positives (#458290).
- Sync Fedora license list with Wiki revision 1.19.
- Dist regex patch applied/superseded upstream.

* Fri Sep 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.84-3
- Sync Fedora license list with Wiki revision 1.09

* Sat Jul 26 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.84-2
- 0.84, fixes #355861, #456304.
- Sync Fedora license list with Wiki revision "16:08, 18 July 2008".
- Rediff patches.

* Tue May 27 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.83-1
- 0.83, fixes #237204, #428096, #430206, #433783, #434694, #444441.
- Fedora licensing patch applied upstream.
- Move pre-2007 changelog entries to CHANGES.package.old.
- Sync Fedora license list with Revision 0.88.

* Tue May 20 2008 Todd Zullinger <tmz@pobox.com> 
- Sync Fedora license list with Revision 0.83 (Wiki rev 131).

* Mon Mar  3 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.82-3
- Sync Fedora license list with Revision 0.69 (Wiki rev 110) (#434690).
