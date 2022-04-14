Vendor:         Microsoft Corporation
Distribution:   Mariner
# Disable tests by default because they fail to run inside mock builds
# at the moment, but can run locally.  To build and run tests, do:
#     rpmbuild -ba --with runtests pykickstart.spec
%bcond_with runtests

Name:      pykickstart
Version:   3.24
Release:   2%{?dist}
License:   GPLv2 and MIT
Summary:   Python utilities for manipulating kickstart files.
Url:       http://fedoraproject.org/wiki/pykickstart
# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
Source0:   %{name}-%{version}.tar.gz
Source1:   %{name}-%{version}.tar.gz.asc

BuildArch: noarch

BuildRequires: gettext
BuildRequires: python3-coverage
BuildRequires: python3-devel
BuildRequires: python3-nose
BuildRequires: python3-ordered-set
BuildRequires: python3-requests
BuildRequires: python3-setuptools
BuildRequires: python3-six
BuildRequires: python3-sphinx

Requires: python3-kickstart = %{version}-%{release}

%description
Python utilities for manipulating kickstart files.

%package -n python3-kickstart
Summary:  Python 3 library for manipulating kickstart files.
Requires: python3-six
Requires: python3-requests
Requires: python3-ordered-set

%description -n python3-kickstart
Python 3 library for manipulating kickstart files.  The binaries are found in
the pykickstart package.

%prep
%setup -q

%build
make PYTHON=%{__python3}

%install
make PYTHON=%{__python3} DESTDIR=%{buildroot} install

%check
%if %{with runtests}
make PYTHON=%{__python3} test
%endif

%files
%license COPYING
%doc README.rst
%doc data/kickstart.vim
%{_bindir}/ksvalidator
%{_bindir}/ksflatten
%{_bindir}/ksverdiff
%{_bindir}/ksshell
%{_mandir}/man1/ksflatten.1.gz
%{_mandir}/man1/ksshell.1.gz
%{_mandir}/man1/ksvalidator.1.gz
%{_mandir}/man1/ksverdiff.1.gz

%files -n python3-kickstart
%doc docs/2to3
%doc docs/programmers-guide
%doc docs/kickstart-docs.txt
%{python3_sitelib}/pykickstart
%{python3_sitelib}/pykickstart*.egg-info

%changelog
* Tue Mar 02 2021 Henry Li <lihl@microsoft.com> - 3.24-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Fix bogus changelog entry

* Mon Apr 06 2020 Brian C. Lane <bcl@redhat.com> - 3.24-1
- Make --url doctext more understandable (jkonecny)
- Remove url command doc that it's replaced (jkonecny)
- Add missing information for driverdisk KS command (jkonecny)
- tests: close the HTTP Server in tests/include.py (bcl)
- tests: Replace nose with unittest (bcl)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Brian C. Lane <bcl@redhat.com> - 3.23-1
- tests: pin coverage at the 4.x.x series (bcl)
- Switch to using Weblate for translations (bcl)
- po: Remove pykickstart.pot (bcl)
- gpg sign the git tag (bcl)
- Cleaning up empty help strings (bcl)
- tests: Fix the empty description, help, etc. test (bcl)
- tests: Turn off HTTP logging in Include_URL_TestCase (bcl)
- tests: Catch warning in Unknown_New_Section_2_TestCase (bcl)
- tests: Capture stderr output from ksflatten test (bcl)
- Prefer --utc to --isUtc in timezone for F32 and later (vslavik)
- Give output in str(F25_Timezone) even without timezone spec (vslavik)
- Prefer the non-camelCased options for %packages (vslavik)
- Add test for kickstart option names (vslavik)
- Add lowercase aliases for camelCased %packages options (vslavik)
- Commit the new pykickstart.pot when making a release (bcl)
- Add the rhsm command (mkolman)
- Fix travis and coverage runs (bcl)
- Fix pylint unnecessary-pass warnings (bcl)
- Drop python2 compatibility (jkonecny)
- Fix check for python zanata client in Makefile (jkonecny)
- Update versionremoved sphinx extension (bcl)

* Wed Nov 06 2019 Brian C. Lane <bcl@redhat.com> - 3.22-1
- Enable coveralls.io coverage tracking (bcl)
- Add tests for ignorebroken packages parameter (jkonecny)
- Add ignore broken parameter to packages section (#1642013) (jkonecny)
- Add support for the ZIPL Secure Boot for F32 and RHEL8 (vponcova)
- Add F32 support (jkonecny)
- Add note for the repo and url ssl options (jkonecny)
- Skip FailsToOpenOutputFile_TestCase if running as root (juliana.rodrigueiro)
- Change .spec Source to new pykickstart organization URL (bcl)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.21-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 3.21-2
- Rebuilt for Python 3.8

* Wed Aug 14 2019 David Cantrell <dcantrell@redhat.com> - 3.21-1
- Make module --disable available on Fedora 31+ (mkolman)
- Add F31 handler (mkolman)
- Add the --disable option for the module command (#1719347) (mkolman)
- A couple fixes for %packaging section docs (mkolman)
- Fix the docs generation (vponcova)
- Fix the documentation of bootloader --append (vponcova)
- Just kidding, use xenial for everything. (dcantrel)
- Python 3.7 is only available in 'xenial' in Travis-CI (dcantrel)
- Reduce .travis.yml to Python 3.{5,6,7}, set SPHINXAPIDOC (dcantrel)
- Replace PYTHONPATH override with sys.path.append; allow
  SPHINXAPIDOC (dcantrel)
- Add rhel7-branch to .travis.yml (dcantrel)
- Restrict the branches to test with Python 3. (dcantrel)
- More changes to .travis.yml, add requirements.txt file (dcantrel)
- Update the Travis-CI yaml file. (dcantrel)
- Fix documentation for the --excludepkgs and --includepkgs repo
  options (mkolman)
- packit.yml: remove unused content (ttomecek)
- Update sed in pykistart.spec Makefile target (phracek)
- Add pykickstart.spec.in for packit (phracek)
- Make %packages --default attribute sane (jkonecny)
- Configuration file .packit.yaml (phracek)
- For Travis-CI, explicitly use Sphinx 1.7.6 (dcantrel)
- Change to unittest.skipUnless and use correct syntax. (dcantrel)
- Replace 'import unittest.skipIf as skipIf' with
  just 'import unittest' (dcantrel)
- s/unittest/pytest/g in .travis.yml (dcantrel)
- pip install unittest for the Travis-CI runs (dcantrel)
- Run 'git checkout' in the Makefile ignoring non-fatal errors (dcantrel)
- Skip KS_With_Wrong_Permissions_TestCase if running as root. (dcantrel)
- Treat pylint warnings as non-fatal, exit codes 0 and 4. (dcantrel)
- Remove unused falsePositives in runpylint.py (dcantrel)
- Use env to set NOSE_IGNORE_CONFIG_FILES (dcantrel)
- Add NOSE_IGNORE_CONFIG_FILES=y to the .travis.yml file (dcantrel)
- Set NOSE_IGNORE_CONFIG_FILES in make coverage (dcantrel)
- In the Travis-CI environment, coverage is 'coverage' (dcantrel)
- Close output_path after reading in ksflatten.py (dcantrel)
- Makefile improvements (dcantrel)
- Specify Python 3.7 in .travis.yml per the docs. (dcantrel)
- Run sphinx-build and sphinx-apidoc from docs/Makefile (dcantrel)
- Add some missing help strings as detected by the coverage target. (dcantrel)
- Add missing descriptions to a handful of pykickstart commands. (dcantrel)
- Mark the sshkey --username option as required in docs (mkolman)
- Test on recent Python versions on Travis (mkolman)
- Fix snapshot documentation (jkonecny)
- Add a CONTRIBUTING file. (dcantrel)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 07 2019 David Cantrell <dcantrell@redhat.com> - 3.20-3
- Remove the Python 2 subpackage for pykickstart (#1686380)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 David Cantrell <dcantrell@redhat.com> - 3.20-1
- New release: 3.20 (dcantrell)
- Fix backward compatibility for python2 (jkonecny)
- In 'make local', create a dummy .asc file explaining the
  signature. (dcantrell)

* Mon Jan 28 2019 David Cantrell <dcantrell@redhat.com> - 3.19-1
- New release: 3.19 (dcantrell)
- Run gen_commands_docs and gen_sections_docs with python3. (dcantrell)
- Use python3-sphinx in docs/Makefile (dcantrell)
- Nope, this way for make po-pull and make release. (dcantrell)
- Make sure 'make release' runs 'make po-pull' (dcantrell)
- RHEL8Handler: include ssl certificate options (lars)
- Add options for ssl certs on url and repo commands (lars)
- parser: use collections.abc to import Iterator (lars)
- test: Remove unused import (lars)
- tests: Fix ksflatten tests (lars)
- tests: Remove KickstartValueError test case (lars)
- tests: Remove test case that's actually valid (lars)
- Fix pylint warning W0102 dangerous-default-value (lars)
- docs/versionremoved: fix sphinx import path (lars)
- travis: don't override PYTHON with /usr/bin/python3 (lars)
- Refactor ksverdiff and add tests for it (atodorov)
- Patch ksverdiff so it works with argparse (atodorov)
- Add main() function to scripts to allow module to be imported (atodorov)
- Refactor tools/ksflatten.py and add tests for it (atodorov)
- Add more tests for load.py (atodorov)
- Issue DeprecationWarning for KickstartValueError and test it for
  completeness (atodorov)
- More test coverage for autopart (atodorov)
- Improve tests for updates (atodorov)
- Improved tests for timezone (atodorov)
- Improve tests for selinux (atodorov)
- Improve test for rootpw (atodorov)
- Refactoring for reboot.py and more tests (atodorov)
- Refactor monitor.py and add more tests (atodorov)
- Add more tests for logvol.py (atodorov)
- Refactoring for driverdisk.py (atodorov)
- Refactor and more tests for btrfs.py (atodorov)
- Add test to kill remaining mutant (atodorov)
- Refactor in dmraid.py (atodorov)
- More tests and refactoring for volgroup.py (atodorov)
- Improve displaymode tests (atodorov)
- Fix the kickstart section %packages (vponcova)
- Fix versions in parsers of kickstart sections (vponcova)
- Fix warnings for deprecated options of kickstart commands (vponcova)
- Fix pylint errors (vponcova)
- Update kickstart-docs.rst (jason.gerfen)
- Kickstart usage example link (jason.gerfen)
- Document module stream installation (mkolman)
- Mention all man pages in all "SEE ALSO" sections (tim)
- Fix typo in ksshell man page (tim)
- Normalize the mount point (vponcova)
- Clarify the --when= parameter error message. (dcantrell)

* Wed Aug 29 2018 Chris Lumens <clumens@redhat.com> - 3.18-1
- New release: 3.18 (clumens)
- Use the RHEL8 handler to generate RHEL docs. (clumens)
- Add missing trailing newline for syspurpose __str__ method (mkolman)
- Add the syspurpose command (mkolman)
- Fix 'make rpmlog' target. (dcantrell)

* Wed Aug 15 2018 David Cantrell <dcantrell@redhat.com> - 3.17-1
- New release: 3.17 (dcantrell)
- Add authselect command to rhel8 handler (rvykydal)
- Add module command to rhel8 handler (rvykydal)
- Update po/pykickstart.pot (dcantrell)

* Thu Aug 09 2018 David Cantrell <dcantrell@redhat.com> - 3.16-1
- New release: 3.16 (dcantrell)
- Remove the extra space from the logvol command (vponcova)
- Support LUKS2 in the raid command (vponcova)
- Support LUKS2 in the part command (vponcova)
- Support LUKS2 in the logvol command (vponcova)
- Support LUKS2 in the autopart command (vponcova)
- Remove unused false positive (vponcova)
- Wrong hanging indentation (vponcova)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Chris Lumens <clumens@redhat.com> - 3.15-1
- New release: 3.15 (clumens)
- Add nvdimm command to RHEL7 (rvykydal)
- Fix tests timeout (vponcova)
- Fix pylint errors (vponcova)
- The deprecated command upgrade is removed in another handler (vponcova)
- The partition option --active is deprecated in another handler (vponcova)
- The ignoredisk option --interactive is deprecated in another handler (vponcova)
- The bootloader option --upgrade is deprecated in another handler (vponcova)
- The command install is deprecated in another handler (vponcova)
- The command deviceprobe is deprecated in another handler (vponcova)
- Add kickstart warnings (vponcova)
- Add the enablemodule command (mkolman)
- Remove translation-canary wrapper for xgettext command. (dcantrell)
- Use 'New release:' in the 'make bumpver' commit messages. (dcantrell)
- Update the 'make pypi' target. (dcantrell)
- Include the _sortCommand to the _setCommand method (#1578930) (vponcova)

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 3.14-3
- Rebuilt for Python 3.7

* Tue May 22 2018 David Cantrell <dcantrell@redhat.com> - 3.14-2
- Include the _sortCommand to the _setCommand method (vponcova, #1578930)
- Remove call to xgettext_werror.sh during build

* Mon May 14 2018 David Cantrell <dcantrell@redhat.com> - 3.14-1
- Increment version to 3.14 (dcantrell)
- Commit the new version in make bumpver. (dcantrell)
- Adjust the make release target. (dcantrell)
- Fix path problem in the pypi target. (dcantrell)
- Adjust zanata check in po-pull Makefile target. (dcantrell)
- Document that lilo and lilocheck are deprecated (vponcova)
- Document that the command mouse is deprecated (vponcova)
- The deprecated command upgrade is removed (vponcova)
- The partition option --active is deprecated (vponcova)
- The ignoredisk option --interactive is deprecated (vponcova)
- The bootloader option --upgrade is deprecated (vponcova)
- The command install is deprecated (vponcova)
- The command deviceprobe is deprecated (vponcova)
- Add Fedora 29 support (vponcova)
- Change the timeout for nosetests (vponcova)
- Fix deprecated commands with data (vponcova)

* Thu May 10 2018 David Cantrell <dcantrell@redhat.com> - 3.13-1
- Prepare for 3.13 release. (dcantrell)
- Adjust the make release target. (dcantrell)
- Fix path problem in the pypi target. (dcantrell)
- Adjust zanata check in po-pull Makefile target. (dcantrell)
- Update fcoe command help (rvykydal)
- Add support for fcoe --autovlan (rvykydal)
- Fix the writePriority test for the new nvdimm command. (clumens)
- Fix a typo in the nvdimm command help output. (clumens)
- Add use action to nvdimm command. (rvykydal)
- Add nvdimm command (rvykydal)
- Remove the spec file from the source repo. (clumens)
- No longer reference the spec file in the Makefile. (clumens)
- Change the rc-release target to not assume the spec file location. (clumens)
- Get the version number from setup.py instead of the spec file. (clumens)
- Remove PKGNAME from the Makefile. (clumens)

* Thu Apr 19 2018 David Cantrell <dcantrell@redhat.com> - 3.12-5
- BuildRequires: python2-ordered-set

* Mon Apr 16 2018 David Cantrell <dcantrell@redhat.com> - 3.12-4
- Fix python2 subpackage builds. (#1564347)
- Disable tests by default because they fail in mock right now.

* Thu Apr 12 2018 David Cantrell <dcantrell@redhat.com> - 3.12-3
- Re-enable the python2 subpackages on Fedora for now.  Some
  programs still need it and have not moved to python3 yet. (#1564347)

* Mon Apr 02 2018 David Cantrell <dcantrell@redhat.com> - 3.12-2
- Conditionalize out python2 subpackage builds on Fedora releases
  after 28 and EL releases after 7

* Mon Feb 19 2018 Chris Lumens <clumens@redhat.com> - 3.12-1
- Sync spec file back up. (clumens)
- Don't use deprecated formatErrorMsg (vponcova)
- Handle error message formatting in KickstartError (vponcova)
- Add the KickstartHandler class (vponcova)
- Remove --fstype=btrfs support from LogVol, Raid and Part (rvykydal)
- Remove btrfs support (rvykydal)
- Create RHEL8 commands to pass handler using highest version test. (rvykydal)
- Add RHEL8 handler (rvykydal)
- Expect kickstart commands to have the default write priority. (vponcova)
- Authconfig is replaced with authselect (vponcova)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.11-2
- Escape macros in %%changelog

* Thu Feb 08 2018 Chris Lumens <clumens@redhat.com> - 3.11-1
- Logging level should be always set (#1543194) (vponcova)
- Copy txt files from _build folder on make local call (jkonecny)

* Thu Jan 25 2018 Chris Lumens <clumens@redhat.com> - 3.10-1
- Update Python 2 dependency declarations to new packaging standards

* Thu Jan 04 2018 Chris Lumens <clumens@redhat.com> - 3.9-1
- Fix directory ownership (lbalhar, #202). (clumens)
- firewall: add --use-system-defaults arg to command (#1526486) (dusty)
- Add lineno as an attribute on KickstartParseError. (clumens)
- Don't modify the original command and data mappings. (vponcova)

* Thu Nov 30 2017 Chris Lumens <clumens@redhat.com> - 3.8-1
- Add support for hmc command in Fedora (vponcova)
- Commands for specifying base repo are mentioned in docs (jkonecny)
- Add list of installation methods to the method doc (jkonecny)
- Fix pylint warnings in the mount command (vponcova)
- Fix test for the mount command (vponcova)
- Add clearpart --cdl option. (sbueno+anaconda)
- Add Fedora 28 support (vponcova)
- Add a new 'mount' command (vpodzime)
- Pylint fixes (vponcova)
- Add command hmc to support SE/HMC file access in RHEL7 (vponcova)
- Add timeout and retries options to %%packages section in RHEL7 (vponcova)
- Call the _ method from i18n.py (jkonecny)
- Backport spec file changes from downstream (jkonecny)
- network: add network --bindto option (Fedora) (#1483981) (rvykydal)
- network: add network --bindto option (RHEL) (#1483981) (rvykydal)
- Add url --metalink support (#1464843) (rvykydal)
- Update doc of repo --mirrorlist and --baseurl with --metalink (#1464843) (rvykydal)
- Add repo --metalink support (#1464843) (rvykydal)
- Add Fedora 27 support. (rvykydal)
- Update Repo command tests. (rvykydal)
- Split the import of commands to multiple lines (vponcova)
- Move the installclass command to the %%anaconda section (vponcova)
- Mention that repo name must not contain spaces (brunovern.a)

* Fri Sep 15 2017 Jiri Konecny <jkonecny@redhat.com> - 3.7-2
- Backport of the Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> from downstream spec
  Python 2 binary package renamed to python2-pykickstart
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Tue Jul 18 2017 Chris Lumens <clumens@redhat.com> - 3.7-1
- Add a Makefile target for uploading to pypi (#162). (clumens)
- Remove some old, unneeded stuff from the Makefile. (clumens)
- Add tests for method command (vponcova)
- Rewrite the method command. (vponcova)
- More documentation for bypassing the bootloader (#159) (amtlib-dot-dll)
- Output any sections registered with NullSection (#154). (clumens)
- Add new installclass command in master (vponcova)

* Tue May 16 2017 Chris Lumens <clumens@redhat.com> - 3.6-1
- Ignore errors from coverage tests (#138) (jkonecny)
- Fix bumpver target when "changelog" is in the spec file more than once. (clumens)
- Ignore a couple false positives coming from the re module. (clumens)
- Fix snapshot command (jkonecny)
- Generate documentation in ci tests (jkonecny)
- Fix snapshot documentation (jkonecny)
- Add tests for a new snapshot command (#1113207) (jkonecny)
- Add support of --when param to snapshot command (#1113207) (jkonecny)
- Add new snapshot KS command (#1113207) (jkonecny)
- Add realm command test (jkonecny)
- Add --nohome, --noboot and --noswap options to autopart command. (vponcova)
- Add --nohome option to autopart command in RHEL7. (vponcova)
- Add support for --chunksize option to RHEL7. (vponcova)
- Add link to online docs to the README (#137) (martin.kolman)
- Add --hibernation to the list of logvol size options (#1408666). (clumens)
- Handle KickstartVersionError in ksflatten (#1412249). (clumens)
- Fix the glob used to reference comps files in docs (#135). (clumens)
- docs: Note under %%include that most sections don't do merging (#134) (walters)
- Fix handling # in passwords. (clumens)
- Pass comments=True to shlex.split calls in the test functions. (clumens)
- Don't forget to add tests to the NOSEARGS. (clumens)

* Wed Nov 30 2016 Chris Lumens <clumens@redhat.com> - 3.5-1
- Include README.rst in the MANIFEST.in again. (clumens)
- Disable running "make coverage" or "make check" with python2. (clumens)
- rootpw: document that password isn't required with --lock (atodorov)
- Run the docs makefile during RTD build (mkolman)
- Remove the type annotations (dshea)
- Remove mypy checks. (dshea)
- Fix python2 compatibility when printing to stderr (jkonecny)
- Add a type stub for the new F26 support. (clumens)
- Fix and add tests for F26 and new displaymode (jkonecny)
- Add non-interactive option to graphical and text modes (jkonecny)
- Add Fedora 26 support (jkonecny)
- fix markup a bit (add ) (gitDeveloper)
- Print errors to stderr when errors aren't fatal (jkonecny)
- Add build insturctions for the docs (martin.kolman)
- More test coverage for base.py (atodorov)
- Warn about using removed keywords in kickstart commands (atodorov)
- More test coverage for network.py (atodorov)
- Refactoring and more tests for partition (atodorov)
- Add documentation for mouse (atodorov)
- Add documentation for langsupport (atodorov)
- Refactor lang and add more tests (atodorov)
- Refactor iscsiname and more tests (atodorov)
- Add short description for interactive command (atodorov)
- Nuke all the pykickstart-2.x %%changelog history. (clumens)
- Update network command documentation also in option help strings. (rvykydal)
- Retroactively fix checks for reqpart and autopart (atodorov)
- More tests for zfcp (atodorov)
- More tests for volgroup (atodorov)
- More tests for url (atodorov)
- Add help documentation and more tests for upgrade.py (atodorov)
- More tests and refactoring for timezone.py, fixes #112 (atodorov)
- More test coverage for sshpw (atodorov)
- Refactor and add more tests for sshkey (atodorov)
- Remove duplicate assert (atodorov)
- Add more tests for rootpw (atodorov)
- Refactoring and additional test coverage for raid command (atodorov)
- More tests for FC3_NFS (atodorov)
- Refactor logging.py and add tests (atodorov)
- Additional tests for FC3_HardDrive (atodorov)
- More tests for F12_GroupData (atodorov)
- Additional test coverage for commands/firewall.py (atodorov)
- Add missing documentation for device command (atodorov)
- Explain ks= vs. inst.ks= in the documentation (#109). (clumens)
- Include the built documentation in the package tarball. (clumens)
- Update the documentation when bumpver is run. (clumens)
- Add commands*.rst and sections.rst to the repo. (clumens)
- Another path change in docs/conf.py for readthedocs. (clumens)
- Fix a couple pylint errors. (clumens)
- Disable assertion in HelpAndDescription_TestCase (atodorov)
- Refactor HelpAndDescription_TestCase to properly patch KSOptionParser (atodorov)
- Add docs to the path in docs/conf.py too. (clumens)
- Set the version in docs/conf.py with "make bumpver". (clumens)
- Set PYTHONPATH when running sphinx-build. (clumens)
- The build now requires sphinx to build documentation. (clumens)
- Test if prog, help or description are empty (atodorov)
- Clean up TODO comments (atodorov)
- Add Sphinx extension which parses the 'versionremoved' directive (atodorov)
- Automatically build kickstart command & sections documentation (atodorov)
- Add a backward compatibility class for the lilo command (atodorov)
- Split upgrade and install commands and update handlers after F20 (atodorov)
- Don't skip DeprecatedCommands when testing handler mappings (atodorov)
- network refactoring and more tests (atodorov)
- iscsiname - small refactoring (atodorov)
- firewall refactoring and more tests (atodorov)
- clearpart: refactoring and more tests (atodorov)
- More tests for multipath (atodorov)
- user: more tests and refactoring (atodorov)
- updates refactoring (atodorov)
- timezone refactoring and more tests (atodorov)
- fcoe more tests (atodorov)
- sshpw: new tests and refactoring (atodorov)
- services refactoring to reduce mutations (atodorov)
- rootpw: refactoring and new tests (atodorov)
- reboot: add two more tests (atodorov)
- monitor: new test (atodorov)
- method: refactoring and a few more tests (atodorov)
- logvol: refactoring and more tests (atodorov)
- iscsi: refactoring and update tests (atodorov)
- ignoredisk: refactor to kill all mutants (atodorov)
- realm: fix missing writePriority and add more test coverage (atodorov)
- driverdisk: remove writePriority from _DriverDiskData constructor and other refactoring (atodorov)
- btrfs: more mutation tests & refactoring (atodorov)
- dmraid: more mutation and test coverage (atodorov)
- volgroup: refactoring and more tests (atodorov)
- xconfig: more tests to kill remaining mutations (atodorov)
- displaymode: extra mutation and test coverage (atodorov)
- zfcp: more mutation tests and bump code coverage (atodorov)
- keyboard: refactoring to reduce mutations (atodorov)
- liveimg: more tests (atodorov)
- multipath:  to  refactoring (atodorov)
- ostreesetup: refactoring  into  and more tests (atodorov)
- zerombr: more tests (atodorov)
- vnc: new test (atodorov)
- cdrom: Remove source of mutations (atodorov)
- eula: minor fixes and more tests (atodorov)
- mouse: add more tests to kill some mutants (atodorov)
- user: fix for deleting of != '' change (atodorov)
- Delete str != "" comparisons to remove 8*110 possible mutations (atodorov)
- rescue: new test to kill remaining mutants (atodorov)
- reqpart: new test to kill remaining mutants (atodorov)
- interactive, lilocheck, mediacheck: kill remaining mutants (atodorov)
- unsupported_hardware: new test to kill remaining mutants (atodorov)
- skipx: new test to kill remaining mutants (atodorov)
- autostep: new test to kill remaining mutants (atodorov)
- Remove unnecessary nargs=1 parameter (atodorov)
- Pass writePriority to KickstartCommand.__init__ (atodorov)
- Add test for writePriority (atodorov)
- Refactor mock.patch so it works with Cosmic-Ray (atodorov)

* Thu Oct 06 2016 Chris Lumens <clumens@redhat.com> - 3.4-1
- Fix Python 2 builds by assigning to KSOptionParser.version properly (#106) (atodorov)
- Do not run translation-canary under python2. (clumens)
- Add network --no-activate option. (#104) (rvykydal)
- Don't run the ksvalidator test under python2. (clumens)
- Fix the check for the error raised by the logvol command on python2. (clumens)
- Support timezone command usage without timezone specification (mkolman)
- Formatting fixes (mkolman)
- Stylistic improvements as sugested by static chackers (#95) (martin.kolman)
- Fix unused-variable warning (atodorov)
- Fix command handler errors identified by previous test (atodorov)
- Test for older versions in new Fedora releases. Closes #28 (atodorov)
- Rename FC16 to F16 so we can find it later in versionMap (atodorov)
- Update sys.path in handlers/control.py if not already updated (atodorov)
- KSOptionParser accepts description, not help argument (atodorov)
- Remove unused import (atodorov)
- Fix class definition problems identified by previous test (atodorov)
- Test how command and data classes are defined (atodorov)
- Fix a couple problems with the previous ksvalidator patches. (clumens)
- Remove a bunch of history from the spec file. (clumens)
- Refactor ksvalidator and its tests (#90) (atodorov)
- Fix some code smells (#89) (atodorov)
- Enable Travis-CI (#88) (atodorov)
- Add versionToLongString to the type annotation file. (clumens)
- Update tests to reflect new positional arguments (atodorov)
- Add empty help/description for KSOptionParser (atodorov)
- Add custom help formatter for ArgumentParser (atodorov)
- Initial Sphinx configuration (atodorov)
- The pykickstart package should require a specific python3-kickstart. (clumens)
- Shuffle network command options for more logical order. (rvykydal)
- Update documentation of network command. (rvykydal)
- Update documentation of network command. (rvykydal)
- Download translations less frequently. (#83) (dshea)
- Adapt to the new version of mypy (#82) (dshea)
- Remove the locales from zanata.xml. (clumens)

* Tue May 10 2016 Chris Lumens <clumens@redhat.com> - 3.3-1
- Do not check translated strings during make check. (dshea)
- Merge the most recent translation-canary changes. (dshea)
- Squashed 'translation-canary/' changes from 5a45c19..840c2d6 (dshea)
- Add documentation for --excludeWeakdeps (dshea)
- Add support for --excludeWeakdeps option to %%packages. (james)
- Numbers can be part of a kickstart command option. (clumens)
- It's authconfig, not autoconfig (in the kickstart.vim file). (clumens)
- Fix pylint no-member errors. (clumens)
- Support file URLs for ostree (#1327460). (clumens)
- Add ksvalidator test cases (jikortus)
- Add classes for pykickstart tools testing (jikortus)
- ksvalidator - don't require KS file with -l option (jikortus)

* Thu Apr 14 2016 Chris Lumens <clumens@redhat.com> - 3.2-1
- Fix a couple mistakes in the documentation. (clumens)
- Correctly move scripts after they've been installed. (clumens)
- Document %%traceback and %%onerror. (clumens)
- Add a new %%onerror script section (#74). (clumens)
- Enable coverage reporting for pykickstart tools (jikortus)
- Fix really long lines in the documentation. (clumens)
- Lots of documentation updates. (clumens)

* Wed Mar 30 2016 Chris Lumens <clumens@redhat.com> - 3.1-1
- Fix the version of the parser in packages tests, too. (clumens)
- PWD doesn't work in the Makefile. (clumens)
- Disable the attrs test for python2. (clumens)
- Accept alternate names for some keyword arguments. (clumens)
- Don't change ignoredisk.ignoredisk in the __init__ method. (clumens)
- Fix bugs where F16 and F18 were using the wrong versions of objects. (clumens)
- Allow marking options as "notest". (clumens)
- Add a test case for various ways of setting attributes. (clumens)
- Add a dataClass attribute to KickstartCommand. (clumens)
- Add a test case for deprecated command corner cases. (clumens)
- Add --chunksize option to raid command. (vtrefny)
- Add a test case for the deprecated multipath command. (clumens)
- Mark the device, dmraid, and multipath commands as deprecated. (clumens)
- Get rid of the ver global variable. (clumens)
- Remove deprecated commands from the documentation. (clumens)
- Add Fedora 25 support. (vtrefny)
- Add some more tests for parser-related corner cases. (clumens)
- Fix processing of the #platform= comment. (clumens)
- Get rid of a bunch of unnecessary blank lines. (clumens)
- fix formating (Frodox)
- Change network example to working one (Frodox)
- Add DNF system-upgrade near FedUp references (github)

* Fri Mar 04 2016 Chris Lumens <clumens@redhat.com> - 3.0-1
- Make sure the script test references parser. (clumens)
- Don't use class attributes for the version or kickstart string. (clumens)
- Add a syntax highlighting file for vim. (clumens)
- Move tests/parser/* into the tests/ directory. (clumens)
- Use importlib to import modules. (dshea)
- Update kickstart documentation for ntp (jkonecny)
- It's self.sshkey, not self.key. (clumens)
- Remove orderedset.py (dshea)
- Remove the removal of the eintr checker, which has been removed (dshea)
- Improved method.py test coverage (jikortus)
- Verify that a password with a # sign doesn't get read as a comment. (clumens)
- Raise deprecation warnings in _setToSelf and _setToObj. (clumens)
- Do not log httpd messages in the load tests. (dshea)
- There is no F7_Key class - use RHEL5_Key instead. (clumens)
- The RHEL6 branch supported the key command. (clumens)
- Add more test coverage around Group and Script objects. (clumens)
- load.py initial test coverage + exception catch (jikortus)
- Fix more formatting problems under the part command. (clumens)
- Fix some indentation problems in the documentation. (clumens)
- Clear up confusing documentation about MB vs. MiB. (clumens)
- argparse error messages are different in python2 and python3. (clumens)
- Add a document describing how to adapt your code to pykickstart-3. (clumens)
- Promote _setToObj and _setToSelf to public functions. (clumens)
- Increase test coverage to 96%%. (clumens)
- Don't duplicate autopart+volgroup checks in the volgroup handlers. (clumens)
- RHEL7 needs to use the correct version of FcoeData and Autopart. (clumens)
- Replace required=1 and deprecated=1 with =True. (clumens)
- Get rid of unnecessary args to add_argument. (clumens)
- Get rid of references to KickstartParseError in assert_parse_error. (clumens)
- Convert command objects to use argparse instead of optparse. (clumens)
- Remove KickstartValueError. (clumens)
- Add some custom actions and types to make things easier elsewhere. (clumens)
- _setToSelf and _setToObj now take a Namespace object. (clumens)
- Use the new ksboolean function where we were using the string. (clumens)
- Convert options.py to use argparse instead of optparse. (clumens)
- Remove the custom map and map_extend actions. (clumens)
- Try harder to test translations. (dshea)
