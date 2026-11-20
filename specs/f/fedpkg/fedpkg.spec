# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# hatchling is not supported in Python 3.6 releases (epel8)
%if 0%{?rhel} == 8
%global with_hatchling 0
%else
%global with_hatchling 1
%endif

Name:           fedpkg
Version:        1.48
Release: 2%{?dist}
Summary:        Fedora utility for working with dist-git

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            https://forge.fedoraproject.org/packaging/fedpkg
Source0:        https://forge.fedoraproject.org/packaging/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch


BuildRequires:  pkgconfig
BuildRequires:  bash-completion
BuildRequires:  git

Requires:       koji
Requires:       azurelinux-rpm-config

# This package redefines __python and can use the python_ macros
%global __python %{__python3}

BuildRequires:  python3-devel
BuildRequires:  python3-rpkg >= 1.70-1
BuildRequires:  python3-distro
%if 0%{?with_hatchling}
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-hatchling
%else
BuildRequires:  python3-setuptools
%endif
# For testing
BuildRequires:  python3-pytest
BuildRequires:  python3-bugzilla
BuildRequires:  python3-freezegun
BuildRequires:  python3-bodhi-client


Requires:       python3-bugzilla
Requires:       python3-rpkg >= 1.70-1
Requires:       python3-distro
Requires:       python3-openidc-client >= 0.6.0
Requires:       python3-bodhi-client
%if !0%{?with_hatchling}
Requires:       python3-setuptools
%endif
Recommends:     fedora-packager
Recommends:     fedpkg-completion

%description
Provides the fedpkg command for working with dist-git

%package        -n fedpkg-stage
Summary:        Fedora utility for working with dist-git
Requires:       %{name} = %{version}-%{release}

%description    -n fedpkg-stage
Provides the fedpkg command for working with dist-git

%package        -n fedpkg-completion
Summary:        The command-line completion support for fedpkg based on python-argcomplete
Requires:       %{name} = %{version}-%{release}

%description    -n fedpkg-completion
This sub-package provides the command-line completion for the fedpkg CLI
via the python-argcomplete framework.

%prep
%autosetup -p1

%if 0%{?with_hatchling}
%generate_buildrequires
%pyproject_buildrequires
%endif

%build
%if 0%{?with_hatchling}
%pyproject_wheel
%else
%py_build
%endif
%{python3} doc/fedpkg_man_page.py > fedpkg.1
register-python-argcomplete --shell bash fedpkg > fedpkg.bash
%if 0%{?with_hatchling}
# argcomplete version in EPEL8 does not have support for fish
register-python-argcomplete --shell fish fedpkg > fedpkg.fish
%if 0%{?rhel} != 9
register-python-argcomplete --shell zsh fedpkg > fedpkg.zsh
%endif
%endif

%install
%if 0%{?with_hatchling}
%pyproject_install
%pyproject_save_files -l %{name}
%else
%py_install
%endif
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -p -m 0644 fedpkg.1 %{buildroot}%{_mandir}/man1
%{__install} -D -p -m 0644 fedpkg.bash -t %{buildroot}%{bash_completions_dir}
%if 0%{?with_hatchling}
%{__install} -D -p -m 0644 fedpkg.fish -t %{buildroot}%{fish_completions_dir}
%if 0%{?rhel} != 9
%{__install} -D -p -m 0644 fedpkg.zsh %{buildroot}%{zsh_completions_dir}/_fedpkg
%endif
# config file /etc/rpkg/fedpkg.conf is extracted to %%{buildroot}/usr/etc/... by pyproject_install
%{__install} -d %{buildroot}%{_sysconfdir}
mv %{buildroot}/usr/etc/* %{buildroot}%{_sysconfdir}
%endif

%check
%if 0%{?with_hatchling}
%pyproject_check_import
%endif
%pytest


%if 0%{?with_hatchling}
%files -f %{pyproject_files}
%else
%files
# For noarch packages: sitelib
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}-py*.egg-info
%endif
%license COPYING
%doc README.rst CONTRIBUTING.md CHANGELOG.rst
%config(noreplace) %{_sysconfdir}/rpkg/fedpkg.conf
%{_bindir}/%{name}
%{_mandir}/*/*

%files -n fedpkg-stage
%{_bindir}/%{name}-stage
%config(noreplace) %{_sysconfdir}/rpkg/fedpkg-stage.conf

%files -n fedpkg-completion
%config(noreplace) %{bash_completions_dir}/fedpkg.bash
%if 0%{?with_hatchling}
%config(noreplace) %{fish_completions_dir}/fedpkg.fish
%if 0%{?rhel} != 9
%config(noreplace) %{zsh_completions_dir}/_fedpkg
%endif
%endif


%changelog
* Fri Jul 31 2026 Ondřej Nosek <onosek@redhat.com> - 1.48-1
- Handle repo-status API errors (artur)
- Add --package option to fedpkg repo-status (artur)
- Omit unused repos in repo-status (artur)
- Separate Fedora and EPEL in repo-status (artur)
- Add initial version of repo-status command (artur)
- Migrate SCM requests from Pagure to Forgejo (patrik)
- Clean up unnecessary Python 2 compatibility code (onosek)
- Fixing ruff and flake8 complaints (onosek)
- feat(new-package): add tests (sanjay.ankur)
- feat(new-package): add util functions (sanjay.ankur)
- feat(new-package): add new command (sanjay.ankur)
- Unittests for PR#631 (onosek)
- Allow detecting release from EPEL minor version feature branches
  (carlwgeorge)
- Fix Jenkinsfile for a Jenkins CI triggered from the Forge (onosek)
- Web documentation at Readthedocs.io (onosek)
- Post-migration steps (onosek)
- `request_unretirement`: split branches into koji_tags and distgit_branches
  (amedvede)
- Add lookaside_http_version config option (onosek)
- docs: modernize Sphinx conf.py (onosek)
- `update`: Add --notes-file option to read notes from file (onosek)
- License file without physical address (onosek)
- Modularity retired - remove corresponding commands (onosek)
- Various code linter issues fixed (onosek)
- Check the correct sorting of imports from now on (onosek)
- `request-unretirement`: fix unittests (onosek)

* Wed Jul 15 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.47-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Thu Jun 04 2026 Python Maint <python-maint@redhat.com> - 1.47-6
- Rebuilt for Python 3.15

* Tue Feb 10 2026 Tom Hughes <tom@compton.nu> - 1.47-5
- Add zsh auto completion

* Tue Feb 10 2026 Ondřej Nosek <onosek@redhat.com> - 1.47-4
- Patch: Check the correct sorting of imports from now on

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 01 2025 Sandro <devel@penguinpee.nl> - 1.47-2
- Fix bash auto completion
- Add fish auto completion

* Wed Nov 26 2025 Ondřej Nosek <onosek@redhat.com> - 1.47-1
- Use ruff code checker instead of bandit (onosek)
- Clone the API key info into all help messages (mpospisi)
- README: Documentation link change, and new Jenkins link – `#606`_ (gleiro)
- `update`: Add unspecified update type (priv.luk@gmail.com)
- `request-unretirement`: Added a new command (amedvede)
- `request-repo`: creating project and package in Anitya (amedvede)
- Switch to %%pyproject_* macros (onosek)
- `retire`: extend the command's console help - `rhbz#2189969`_ (onosek)
- Jenkinsfile: use local declaration instead of global (onosek)
- `srpm`: --offline arg to prevent connecting to Koji – `#600`_ (onosek)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.46-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.46-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.46-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 24 2025 Ondřej Nosek <onosek@redhat.com> - 1.46-4
- Unify the hatchling macros with rpkg

* Tue Jun 24 2025 Ondřej Nosek <onosek@redhat.com> - 1.46-3
- Switch to %%pyproject_* macros

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 1.46-2
- Rebuilt for Python 3.14

* Wed Mar 19 2025 Ondřej Nosek <onosek@redhat.com> - 1.46-1
- `request-repo`: add `--onboard-packit` argument (nforro)
- Fork a package using anonymous auth - #574 (onosek)
- Check that auth tokens aren’t written to world-readable files (git)
- Don't allow to request repositories in modules/ namespace (miro)
- Do not auto-request EPEL x.y modules (carlwgeorge)
- Dynamically exclude Rawhide branch from fedpkg branching - #566 (samyak.jn11)
- Fix unittests when building for ELN target - #589 (onosek)
- Python 3.13 environment and renew testing image (onosek)
- `releases-info` should always show the same order - #569 (onosek)
- Update expired token exception instructions (astra)
- Clone epel10 branches with clone -B (carlwgeorge)
- Update expired token exception instructions (ferdnyc)
- Add setuptools to dependencies for Python 3.12+ (ferdnyc)
- Fix tests on EPEL 9/10. (romain.geissler)
- Fixing unittests for py36 (onosek)
- gitignore the name-version-build/ directory created by fedpkg prep/local (miro)
- Handle rhel runtimes when minor version exists in disttag (dherrera)
- Add tests cases for runtime_disttag removal when working with epel10 (dherrera)
- Improvements on string parsing (dherrera)
- Get macros from epel-candidate build target. (dherrera)
- Fix EPEL10 branch expression to cover 2 or more digits. (dherrera)
- Use minor value from koji when no minor in branch name (dherrera)
- Fix minor requirements for EPEL10+ in test (dherrera)
- Do not auto-request ELN modules (yselkowi)
- Fixes missing key in distro.os_release_info() (onosek)
- Update check_bodhi_version to check for >= 6.0.0 (awilliam)
- Modernize and clean unittest imports (awilliam)
- Replace and update use of deprecated 'linux_distribution' (awilliam)
- Drop all usage of six (awilliam)
- Drop support for bodhi-client <= 5 (awilliam)
- Add py313 environment as that's current (awilliam)
- Fix URL of Bodhi in staging (nils)
- Extend load_rpmdefines to work with EPEL10+ (dherrera)
- Add EPEL10+ url pattern on assert_valid_epel_package (dherrera)
- Test url usage in assert_valid_epel_package (dherrera)
- Add EPEL10 branch name cases as valid (dherrera)
- Test for valid EPEL branch names (dherrera)
- Don't print the branch name after dash when there is no dash - 554 (miro)
- Don't use hatchling on python 3.6 (dherrera)
- Remove mbs.fedoraproject.org scopes from git cred helper (kj)
- Fix unittests after creating the project in hatch (onosek)

* Wed Feb 26 2025 Ondřej Nosek <onosek@redhat.com> - 1.45-10
- Dynamically exclude Rawhide branch from fedpkg branching
- Do not auto-request EPEL x.y modules
- Don't allow to request repositories in modules/ namespace

* Tue Feb 18 2025 Ondřej Nosek <onosek@redhat.com> - 1.45-9
- `releases-info` should always show the same order
- Python 3.13 environment and renew testing image
- Fix unittests when building for ELN target

* Mon Feb 17 2025 Ondřej Nosek <onosek@redhat.com> - 1.45-8
- Patch: Update expired token exception instructions

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.45-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Ondřej Nosek <onosek@redhat.com> - 1.45-6
- gitignore the name-version-build/ directory created by fedpkg prep/local
- Fixing unittests for py36
- Fix tests on EPEL 9/10.
- Add setuptools to dependencies for Python 3.12+
- Update expired token exception instructions
- Clone epel10 branches with clone -B

* Wed Sep 18 2024 Ondřej Nosek <onosek@redhat.com> - 1.45-5
- Add py313 environment as that's current
- Drop support for bodhi-client <= 5
- Drop all usage of six
- Replace and update use of deprecated 'linux_distribution'
- Modernize and clean unittest imports
- Update check_bodhi_version to check for >= 6.0.0
- Fix URL of Bodhi in staging
- Fixes missing key in distro.os_release_info()
- Do not auto-request ELN modules
- Fix minor requirements for EPEL10+ in test
- Use minor value from koji when no minor in branch name
- Fix EPEL10 branch expression to cover 2 or more digits.
- Get macros from epel-candidate build target.
- Improvements on string parsing
- Add tests cases for runtime_disttag removal when working with epel10
- Handle rhel runtimes when minor version exists in disttag

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 1.45-4
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 08 2024 Ondřej Nosek <onosek@redhat.com> - 1.45-2
- Add support for building for epel10
- Don't print the branch name after dash when there is no dash
- Remove mbs.fedoraproject.org scopes from git cred helper
- Fix unittests after creating the project in hatch

* Wed Jun 26 2024 Ondřej Nosek <onosek@redhat.com> - 1.45-1
- Allow package.cfg on rawhide/main branch (sgallagh)
- Fix datetime.utcnow deprecation warning (dherrera)
- Remove Python 2.7 support (onosek)
- Fix tests on Python 3.12 by fixing pkg_resources dependency (dherrera)
- Remove traces of PDC in docstrings (lsegura)
- Remove function get_sl_type, no longer needed (lsegura)
- Remove pdc calls, use bodhi instead (lsegura)
- Update docker image for Jenkinks tests (onosek)
- Methods for setting API tokens use getpass - 2089694 (onosek)
- Update the sendemail.to Fedora email addresses (miro)
- Remove epel-playground support (otto.liljalaakso)
- disable-monitoring: run manually only (onosek)
- `fedpkg update`: add option `--severity` (onosek)
- Allow fetching release from branch basename (pemensik)
- Lookaside cache operations retries (onosek)
- check_branch: Fix backwards error message (otaylor)
- Fix flake8 complaints (onosek)
- fix: change changelog link (amedvede)
- Update link to the `Share Test Code` documentation (psplicha)
- Corrected the description of --namespace. (Bjorn)
- Improve invalid branch name error message (otto.liljalaakso)
- Fix unittests after '--path' argument is validated (onosek)
- Remove unused arches from completion (mikel)
- Update docker image for Jenkinks tests (onosek)

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 1.44-9
- Rebuilt for Python 3.13

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 1.44-5
- Rebuilt for Python 3.12

* Fri Apr 28 2023 Ondřej Nosek <onosek@redhat.com> - 1.44-4
- Patch: Improve invalid branch name error message

* Mon Apr 3 2023 Ondřej Nosek <onosek@redhat.com> - 1.44-3
- Patch: Fix unittests after '--path' argument is validated

* Wed Mar 1 2023 Ondřej Nosek <onosek@redhat.com> - 1.44-2
- Require a bumped rpkg version

* Mon Feb 20 2023 Ondřej Nosek <onosek@redhat.com> - 1.44-1
- Do not execute unittests for old bodhi-client (onosek)
- New command `disable-monitoring` (onosek)
- Set default_branch_merge to 'rawhide' (otto.liljalaakso)
- `fedpkg update`: can handle $EDITOR with arguments - #492 (onosek)
- Add Jenkinsfile for CI (onosek)

* Mon Jan 30 2023 Miro Hrončok <mhroncok@redhat.com> - 1.43-3
- Rebuilt to change Python shebangs to /usr/bin/python3.6 on EPEL 8

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 08 2022 Ondřej Nosek <onosek@redhat.com> - 1.43-2
- Updated rpkg dependency version.

* Wed Sep 07 2022 Ondřej Nosek <onosek@redhat.com> - 1.43-1
- Improve change management process documentation (onosek)
- Fix medium level bandit findings (onosek)
- rpmdefines changes depending on rpkg (onosek)
- `request-branch`: detect existing branch - #481 (onosek)
- Refactoring of _request_branch method (drumian)
- Fix tests with bodhi-client 6+ (awilliam)
- Add compatibility for Bodhi >= 6.0.0 (aurelien)
- fedpkg update --suggest-logout option added - 472 (drumian)
- WIP: Remove python3-mock dependency from fedpkg (drumian)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 17 2022 Adam Williamson <awilliam@redhat.com> - 1.42-4
- Backport PR #482 to fix tests with bodhi-client 6+ (#2097858)

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 1.42-3
- Rebuilt for Python 3.11

* Tue Apr 26 2022 Ondřej Nosek <onosek@redhat.com> - 1.42-2
- Patch: fedpkg update --suggest-logout option added
- Patch: Add compatibility for Bodhi >= 6.0.0
- fedora-packager rpm dependency is "Recommends"

* Wed Jan 26 2022 Ondřej Nosek <onosek@redhat.com> - 1.42-1
- Fix Jenkins tests (onosek)
- Return bash-completion back because of compatibility (onosek)
- Fix unittests for Python 2 - missing dependency (onosek)
- set-distgit-token: create a missing config file (mark.e.fuller)
- Fix rsplit() usage to work with Python 2.7 - 2029175 (treydock)
- mockbuild: default to use the local Mock configuration (praiskup)
- Add support for epel9-next (carl)
- Remove unused import from setup.py (onosek)
- Enable Python argcomplete (onosek)
- Test and support Python 3.10 (miro)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Ondřej Nosek <onosek@redhat.com> - 1.41-3
- drop nosetests for Python3
- disable pytest coverage during build

* Mon Nov 08 2021 Carl George <carl@george.computer> - 1.41-2
- Allow branch requests for epel9-next

* Wed Aug 25 2021 Ondřej Nosek <onosek@redhat.com> - 1.41-1
- Look for bug number in commit message instead of changelog (zebob.m)
- Add default configuration for `resultsdir` (oturpe)
- Use rpkg layouts for rpmdefines (oturpe)
- Advertised set-x-token method in do_fork and set_pagure_issue (jkunstle)
- Pagure / DistGit token config-file cli-interface - #192 (jkunstle)
- Deprecated arguments --dist have been removed, and related tests have been
  updated. (abisoi)
- Add support for epel*-next branches (carl)
- Pagure token request - ACL specification - #440 (jkunstle)
- request-tests-repo: add empty 'upstreamurl' item - rhbz#1854987 (onosek)
- Jenkins unittests run in docker container (onosek)
- Drop Python 2.6 support (onosek)
- Bash completion for request-tests-repo - #433 (onosek)
- Unittests for new default branches (onosek)
- Default branches on different namespaces - #428 (mboddu)
- Clone rawhide branch with clone -B - 427 (lsedlar)
- Fix completion of arches (lsedlar)
- Add --rpmlintconf to lint command completion (lsedlar)
- Remove duplicated definition for lint (lsedlar)
- Add fork to bash completion - 1920997 (lsedlar)
- New default dist-git branch: rawhide - unittests (lsedlar)
- New default dist-git branch: rawhide (pingou)
- Fedpkg update didn't read bug numbers from changelog - rhbz#1912555 (onosek)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.40-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.40-7
- Rebuilt for Python 3.10

* Sat Apr 03 2021 Ondřej Nosek <onosek@redhat.com> - 1.40-6
- Patch: Add support for epel*-next branches

* Mon Mar 01 2021 Ondřej Nosek <onosek@redhat.com> - 1.40-5
- Patch: Default branches on different namespaces

* Wed Feb 03 2021 Ondřej Nosek <onosek@redhat.com> - 1.40-4
- Patch: Clone rawhide branch with clone -B

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Ondřej Nosek <onosek@redhat.com> - 1.40-2
- Patches:
- Fedpkg update didn't read bug numbers from changelog
- New default dist-git branch: rawhide
- New default dist-git branch: rawhide - unittests

* Fri Dec 04 2020 Ondřej Nosek <onosek@redhat.com> - 1.40-1
- Tests for "--release eln" (onosek)
- Add support for using "--release eln" (mmathesi)
- Fix Python 2 tests for epel7 (onosek)
- Do not show warning when 'package.cfg' is missing - #417 (onosek)
- Fix tests - #414 (michel)
- Revert "Support for epel*-playground branch requests" - #414 (michel)

* Wed Sep 09 2020 Ondřej Nosek <onosek@redhat.com> - 1.39-1
- Pytest replaces nosetests (onosek)
- More specific regex to detect bugs in changelog (onosek)
- Print response data from Pagure for debugging (onosek)
- fedpkg fork checks if the fork already exists (onosek)
- Fix unittest for bodhi based on its version (onosek)
- display_name added to bodhi.template (onosek)
- Remove unncecessary test (onosek)
- Correct flake8 complaints to pass unittests (onosek)
- fedpkg fork adds correct remote URL (onosek)
- Disable test method's docstring in nosetests list (onosek)
- Allow retirement on epel branches - tests (onosek)
- Allow retirement on epel branches (mboddu)
- Updated supported plaforms in documentation (onosek)
- Check missing config options more reliably - 1813338 (onosek)
- Body changes for requesting new test repo (onosek)
- Repair test of "retire" command after rpkg update (onosek)
- Move rpm dependency for test environment only (onosek)
- Run newer version of sphinx-build tool (onosek)
- Remove deprecated clone_config (onosek)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 1.38-5
- Rebuilt for Python 3.9

* Mon May 18 2020 Ondřej Nosek <onosek@redhat.com> - 1.38-4
- Patch: Fix unittest for bodhi based on its version

* Mon Mar 30 2020 Ondřej Nosek <onosek@redhat.com> - 1.38-3
  Patches:
  - Repair test of "retire" command after rpkg update
  - Body changes for requesting new test repo
  - Check missing config options more reliably

* Fri Mar 06 2020 Ondřej Nosek <onosek@redhat.com> - 1.38-2
- Patch: Move rpm dependency for test environment only

* Mon Mar 02 2020 Ondřej Nosek <onosek@redhat.com> - 1.38-1
- Removes check of bodhi-client version - rhbz#1796972 (onosek)
- Clone config customization for namespaces (onosek)
- Repair Jenkins tests (onosek)
- Update bash completion with side tag commands (lsedlar)
- add --fail-fast to bash-completion (cheese)
- Improve coding style by sorting imports (onosek)
- Repair tests for previous commits (onosek)
- Create fork of the active repository - #276 (onosek)
- request-tests-repo: add branch into ticket body - #359 (onosek)
- verrel command on master asks Koji first - #357 (onosek)
- Check nvr before build - #356 (onosek)
- Change dist tag for epel8-playground (onosek)
- Add test for retiring on archived release (lsedlar)
- Mock requests in all tests (lsedlar)
- Line up descriptions for better code readability (onosek)
- Clarify request-branch 'service levels' argument - #283 (onosek)
- Resolve Jenkins unittests failing (onosek)
- utils: fix whitespace in Pagure error message (kdreyer)
- New options for bodhi template - 459 (onosek)
- Block retiring in released branches - #337 (onosek)
- Use package.cfg for epel8+ branches (mboddu)
- Add epel*-playground into rpmdefines (smooge)
- linux_distribution import moved (onosek)
- Unittests for epel*-playground branch requests (onosek)
- Allow epel*-playground requests for epel8 and newer (onosek)
- Support for epel*-playground branch requests - #334 (mboddu)
- git-changelog: Fix running on Python 3 (onosek)
- Avoid warning about invalid escape with python3.8 (zbyszek)
- Tests for update stable karma - #321 (cqi)
- Bump check for bodhi client - 330 (lsedlar)
- Ignore files in a cloned repository - patterns update (onosek)

* Mon Feb 03 2020 Ondřej Nosek <onosek@redhat.com> - 1.37-13
- Patch: Removes check of bodhi-client version

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.37-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 08 2019 Miro Hrončok <mhroncok@redhat.com> - 1.37-11
- Drop unneeded build dependency on python3-unittest2

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.37-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Aug 21 2019 Ondřej Nosek <onosek@redhat.com> - 1.37-9
- Backport: display_name added to bodhi.template

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.37-8
- Rebuilt for Python 3.8

* Fri Aug 02 2019 Ondřej Nosek <onosek@redhat.com> - 1.37-7
- Require python*-rpkg-1.58-8 as minimum version

* Thu Aug 01 2019 Ondřej Nosek <onosek@redhat.com> - 1.37-6
- Backport: Add epel*-playground into rpmdefines
- Backport: Use package.cfg for epel8+ branches

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Ondřej Nosek <onosek@redhat.com> - 1.37-4
- Require python*-rpkg-1.58-5 as minimum version

* Thu Jul 18 2019 Ondřej Nosek <onosek@redhat.com> - 1.37-3
- Backport: Support for epel*-playground branch requests

* Fri May 31 2019 Ondřej Nosek <onosek@redhat.com> - 1.37-2
- Backport: Bump check for bodhi client (version 4)

* Mon Apr 29 2019 Ondrej Nosek <onosek@redhat.com> - 1.37-1
- Ignore files in a cloned repository - patterns (onosek)
- Create env without --system-site-packages enabled to run flake8 (cqi)
- Include possible distprefix in --define dist for Forge-based packages
  (zebob.m)
- Revise shell completion for module scratch builds to require SRPMs to be
  specified individually using multiple '--srpm SRPM' options, and enable
  completion of modulemd file path by yaml extension. (mmathesi)
- Enable shell completion for module scratch builds. Add custom SRPM shell
  completion with local module builds. Add missing shell completion options for
  local module builds. (mmathesi)
- Make fedpkg update output a report after success - #315 (zebob.m)
- Retire 'retire' command from 'fedpkg' (mmathesi)
- More specific expression for bug search (onosek)
- Fix fedpkg update --bugs detection (zebob.m)
- README: add links and format change (onosek)
- Show hint when Pagure token expires - #285 (onosek)

* Tue Feb 05 2019 Ondřej Nosek <onosek@redhat.com> - 1.36-2
- New dependency: python-distro

* Mon Feb 04 2019 Ondřej Nosek <onosek@redhat.com> - 1.36-1
- Added update-docs script (onosek)
- Sdist fix and Python 2.6 compatibility (onosek)
- Add support for a 'flatpaks' namespace (otaylor)
- Move argparse fix to rpkg - #299 (onosek)
- Fix update command related tests (cqi)
- Make update work for containers - #296 (lsedlar)
- Add 'severity=' option to 'fedpkg update' template (praiskup)
- Add contributing guide - #293 (lsedlar)
- Use module distro instead of platform - #278 (cqi)
- Add missing content to 1.35 release notes (cqi)
- Help: Use foo in foo examples, not name (miro)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 17 2018 Chenxiong Qi <cqi@redhat.com> - 1.35-2
- Add mssing require python3-setuptools

* Tue Aug 21 2018 Chenxiong Qi <cqi@redhat.com> - 1.35-1
- Reserve last bodhi template on error - rhbz#1467897 (cqi)
- New command releases-info - #247 (cqi)
- Fix a test for request-repo command (cqi)
- New option to request a repo without an initial commit - #215 (cqi)
- Add --shell to bash completion for mockbuild (cqi)
- Greenwave conf and support for gating validation (gnaponie)
- Allow to create update directly with CLI options - #93 rhbz#1007157 (cqi)
- Add more tests for utils (cqi)
- Rewrite method to create bodhi update - rhbz#1492480 (cqi)
- Mock fedora.client.OpenIdBaseClient._load_cookies (cqi)
- Do not use configparser.SafeConfigParser in tests (cqi)
- Fix test_retire to use unittest2 in el6 (cqi)
- Submit builds from stream branch (cqi)
- The create new project is not needed for packager (pingou)
- Add py37 testenv (cqi)
- Set PYCURL_SSL_LIBRARY directly for installing pycurl (cqi)
- Fix flake8 errors and typo in tests (cqi)
- Add tests for some commands (cqi)
- Add tests for utils.py (cqi)
- Convert test case for utils.py as normal test case (cqi)
- Add some tests for BugzillaClient (cqi)
- Fix TypeError raised from override create command - #256 (cqi)
- Add missing command and options in bash completion (cqi)

* Fri Aug 03 2018 Chenxiong Qi <cqi@redhat.com> - 1.34-3
- Require python-openidc-client 0.6.0 as minimum version

* Tue Jul 31 2018 Chenxiong Qi <cqi@redhat.com> - 1.34-2
- Fix files section for Python 3 build

* Tue Jul 24 2018 Chenxiong Qi <cqi@redhat.com> - 1.34-1
- Get csrf token properly when retry bodhi API call (cqi)
- Accept old config with module instead of repo (lsedlar)
- Add option --namespace to command request-branch (cqi)
- Add argument name and option --namespace to request-repo - #193 #200 (cqi)
- Add explicit option --repo for request-branch - #244 (cqi)
- Do not use deprecated option module-name (cqi)
- Remove compatible code with EL5 in bash completion (cqi)
- Handle Bodhi login automatically (cqi)
- Refine command override create (cqi)
- request-repo: Fix API token help text - #232 (tmz)
- Use base_module in clone_config - #230 (tmz)
- Extend override by number of days or specific date - #67 (cqi)
- Use refactored man from pyrpkg (puiterwijk)
- Add new command for creating override in Bodhi - #92 (cqi)
- Also remove bodhi url from config (cqi)
- Check bodhi version earlier (cqi)
- Drop support of bodhi-client 0.9 - #223 (cqi)
- Use custom ArgumentParser from pyrpkg.cli (jkucera)
- Add OIDC config (puiterwijk)
- Fix argparse error in Python 3 - #221 (cqi)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.33-4
- Rebuilt for Python 3.7

* Tue May 22 2018 Chenxiong Qi <cqi@redhat.com> 1.33-3
- Backport: Fix argparse error in Python 3

* Mon May 21 2018 Chenxiong Qi <cqi@redhat.com> 1.33-2
- Require python2-rpkg-1.54-2 as minimum version

* Mon May 14 2018 Chenxiong Qi <cqi@redhat.com> - 1.33-1
- Allow running tests against specified rpkg (cqi)
- Fix test due to rpkg uses getpass.getuser (cqi)
- Getting bodhi version works with Python 3 - #213 (cqi)
- Detect Bodhi client by major version - #204 (cqi)
- Allow requesting modular repositories without bug ID - #197 (rdossant)
- Fix test test_verify_sls_invalid_date - #209 (cqi)
- Copy pip-pycurl to ensure pycurl is installed correctly (cqi)
- Fix unicode issue for update command in Python 3 - #206 (cqi)
- Fix a few E722 code styles errors (cqi)
- Fix fake PDC URL in test (cqi)
- Use tox to run tests with multiple Python versions (cqi)
- Reword error message for missing pagure token - #194 (cqi)
- Tell which token ACL is required for request-repo - #195 (cqi)
- Rename incorrect references of Koshei to be Anitya (mprahl)

* Thu May 10 2018 Miro Hrončok <mhroncok@redhat.com> - 1.32-2
- Switch to Python 3 on Fedora > 28 and EL > 7
- Drop Groups
- Switch to %%{buildroot}
- Switch to %%py_build and _install

* Thu Mar 01 2018 Chenxiong Qi <cqi@redhat.com> - 1.32-1
- Add requests-tests-repo command (mvadkert)
- Use PDC instead of Bodhi to get the active release branches - #187 (mprahl)
- fix broken syntax in bash completion (tmz)
- Fix Python 3 incompatible code in tests (cqi)
- Better mocking.  Return different values for each new request. (rbean)
- Typofix. (rbean)
- Add docstrings. (rbean)
- Automatically request module for non-standard branches. (rbean)
- Refactor: parameterize the request_repo and request_branch functionality.
  (rbean)
- Some additions to the gitignore file. (rbean)

* Wed Feb 14 2018 Chenxiong Qi <cqi@redhat.com> 1.31-5
- Backport: fix broken syntax in bash completion

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.31-4
- Update Python 2 dependency declarations to new packaging standards

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.31-3
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Chenxiong Qi <cqi@redhat.com> - 1.31-1
- Include missing conf file in test (cqi)
- Add more document to request-repo and request-branch (cqi)
- Stop allowing EPEL branches on official EL packages (mprahl)
- Port fedrepo-req and fedrepo-req-branch to fedpkg (mprahl)
- Fix test for unsupported Bodhi version (lsedlar)
- Work with Bodhi 3 - rhbz#1507410 (lsedlar)
- Allow any parameters in construct_build_url (cqi)
- Fix the anongiturl (patrick)

* Wed Nov 22 2017 Lubomír Sedlář <lsedlar@redhat.com> - 1.30-5
- Work with Bodhi 3

* Wed Nov 08 2017 Chenxiong Qi <cqi@redhat.com> - 1.30-4
- Backport: Allow any parameters in construct_build_url

* Wed Nov 01 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.30-3
- Enable namespaced lookaside
- Update anongiturl

* Fri Oct 27 2017 Chenxiong Qi <cqi@redhat.com> - 1.30-2
- Disable lookaside_namespaced and revert to use git:// anongiturl

* Fri Oct 20 2017 Chenxiong Qi <cqi@redhat.com> - 1.30-1
- Tests for update command (cqi)
- Add support for module commands (mprahl)
- Clean rest cert related code (cqi)
- Remove fedora cert (cqi)
- Override build URL for Koji (cqi)
- changing anongiturl to use src.fp.o instead of pkgs.fp.o. - #119 (tflink)
- Add tests (cqi)
- Enable lookaside_namespaced - #130 (cqi)
- Detect dist tag correctly for RHEL and CentOS - #141 (cqi)
- Remove deprecated call to platform.dist (cqi)
- Do not prompt hint for SSL cert if fail to log into Koji (cqi)
- Add more container-build options to bash completion (cqi)
- Remove osbs from bash completion - #138 (cqi)
- Install executables via entry_points - #134 (cqi)
- Fix container build target (lsedlar)
- Get correct build target for rawhide containers (lsedlar)
- Update error message to reflect deprecation of --dist option (pgier)

* Fri Sep 15 2017 Lubomír Sedlář <lsedlar@redhat.com> - 1.29-5
- Use correct build target for containers

* Mon Sep 04 2017 Chenxiong Qi <cqi@redhat.com> - 1.29-4
- Fix fedpkg N-V-R dependency in fedpkg-stage subpackage

* Fri Sep 01 2017 Chenxiong Qi <cqi@redhat.com> - 1.29-3
- Fix: work properly with koji prod and stg profile

* Fri Aug 18 2017 Chenxiong Qi <cqi@redhat.com> - 1.29-2
- python2-rpkg-1.50 is minimum version required

* Thu Aug 17 2017 Chenxiong Qi <cqi@redhat.com> - 1.29-1
- Remove unused variable in Commands.retire (cqi)
- No more pkgdb. (rbean)
- Add --arches to build completions (ville.skytta)
- Add ppc64le to arch completions (ville.skytta)
- Explain how to write a note in multiple lines in update template - #123 (cqi)
- Remove code that handles secondary arch (cqi)
- Simplify passing arguments when creating Command object - #14 (cqi)
- Set koji profile for secondary arch immediately (cqi)
- Use profile to load Koji configuration - #97 (cqi)
- Remove push.default from clone_default - #109 (cqi)
- remove special handling of s390 specific packages (dan)
- Replace fedorahosted.org with pagure.io in manpage - #113 (cqi)
- Remove tracbaseurl from conf file - #112 (cqi)
- Set disttag properly (cqi)
- koji stage config moved, update fedpkg defaults (maxamillion)
- Specific help of --release for fedpkg - rhbz#1054440 (cqi)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 27 2017 Chenxiong Qi <cqi@redhat.com> - 1.28-1
- Restore anonymous clone link - rhbz#1425913 (cqi)

* Wed Feb 22 2017 Chenxiong Qi <cqi@redhat.com> - 1.27-2
- Rebuilt with updated tarball

* Wed Feb 22 2017 Chenxiong Qi <cqi@redhat.com> - 1.27-1
- Python 3.6 invalid escape sequence deprecation fixes (ville.skytta)
- Disable tag inheritance check - #98 (cqi)
- Enable the fix to allow anonymous clone via https

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Lubomír Sedlář <lsedlar@redhat.com> - 1.26-5
- Disable tag inheritance check

* Thu Dec 15 2016 Chenxiong Qi <cqi@redhat.com> - 1.26-4
- Fix handle unicode chars in git log - BZ#1404724 (cqi)
- Fix: make fedpkg workable with bodhi 2 CLI - #87 (cqi)
- Fix --dist/--release option for 'master' %%dist detection (praiskup)

* Mon Dec 12 2016 Lubomír Sedlář <lsedlar@redhat.com> - 1.26-3
- sha512 should be also used in fedpkg-stage (cqi)
- conf: s/kerberos_realm/kerberos_realms/ (i.gnatenko.brain)

* Fri Dec 09 2016 Chenxiong Qi <cqi@redhat.com> - 1.26-2
- Split fedpkg-stage into a separate package

* Fri Dec 02 2016 Chenxiong Qi <cqi@redhat.com> - 1.26-1
- New release of 1.26

* Thu Sep 01 2016 Chenxiong Qi <cqi@redhat.com> - 1.25-1
- update project URL (mattdm)
- Allow fedpkg to be compatible with both bodhi 1 and bodhi 2. (randy)
- Modify the bodhi cli usage for `fedpkg update`. (lmacken)
- Add nosetest configuration (cqi)
- replace gitbuildurl with gitbuildhash (cqi)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 08 2016 Chenxiong Qi <cqi@redhat.com> - 1.24-3
- Depends on pyrpkg 1.45

* Mon Jun 27 2016 Chenxiong Qi <cqi@redhat.com> - 1.24-1
- Add a guide for releasing new version (lsedlar)
- Merge #10 `Python 3 compatibility fixes` (lubomir.sedlar)
- Add ZSH completion by Alexey I. Froloff (lsedlar)
- Merge #28 `fix broken when non-ASCII in path` (lubomir.sedlar)
- fix broken when non-ASCII in path (cqi)
- Fix tests for retire with new rpkg (lsedlar)
- use setup.cfg to make bztar as the default format for sdist (cqi)
- Configure git user for tests (lsedlar)
- Fix tests on Python 2.6 (lsedlar)
- Python 3 compatibility fixes (ville.skytta)

* Wed Jun 08 2016 Lubomír Sedlář <lsedlar@redhat.com> - 1.23-3
- Rename bash completion on EPEL

* Thu Jun 02 2016 Lubomír Sedlář <lsedlar@redhat.com> - 1.23-2
- Add build dep on bash-completion

* Thu Mar 31 2016 Lubomír Sedlář <lubomir.sedlar@gmail.com> - 1.23-1
- Fix fedpkg retire with namespace
- Enable test suite during build

* Sun Mar 20 2016 Lubomír Sedlář <lubomir.sedlar@gmail.com> - 1.22-3
- Bump dependency on rpkg

* Wed Mar 16 2016 Lubomír Sedlář <lubomir.sedlar@gmail.com> - 1.22-2
- Bump version

* Mon Mar 14 2016 Lubomír Sedlář <lubomir.sedlar@gmail.com> - 1.22-1
- Update upstream URL (lsedlar)
- Fix bash completion. (lsedlar)
- add container-build bash completion and enable distgit namepacing (provided
  by pyrpkg) (maxamillion)
- Install bash completion to where bash-completion.pc says (ville.skytta)
- flake8 fixes (ville.skytta)
- Python 3 compatibility fixes (ville.skytta)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 23 2015 Pavol Babincak <pbabinca@redhat.com> - 1.21-1
- Use rpkg's backwards compatible clone_config (pbabinca)
- Merge #7 `Fix Deprecation warning during fedpkg update run`
  (kumarpraveen.nitdgp)
- Fix Deprecation Warning - /usr/lib/python2.7/site-packages/fedpkg/cli.py:1:
  DeprecationWarning:   Commands._hash_file is deprecated and will be removed
  eventually (kumarpraveen.nitdgp)
- Merge #3 `Add post-clone bz and sendemail config, requires rpkg > 1.36`
  (ville.skytta)
- Add post-clone bz and sendemail config, requires rpkg > 1.36 (ville.skytta)
- lookaside: Use our new download path (bochecha)
- Simplify handling of our custom certificates (bochecha)
- Drop obsolete functions (bochecha)
- Release 1.20 (pbabinca)
- Bash completion for mockbuild --no-clean* options (pbabinca)
- Hijack load_kojisession to catch auth problems (pbabinca)
- Upload source files with our preferred hash (bochecha)
- pass keyword args as keyword args (mikeb)
- For rawhide use fedora-rawhide-* mock config instead of fedora-devel-*
  (pbabinca)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Pavol Babincak <pbabinca@redhat.com> - 1.20-1
- Bash completion for mockbuild --no-clean* options (pbabinca)
- Hijack load_kojisession to catch auth problems (pbabinca)
- Upload source files with our preferred hash (bochecha)
- pass keyword args as keyword args (mikeb)
- For rawhide use fedora-rawhide-* mock config instead of fedora-devel-*
  (pbabinca)

* Thu Dec 18 2014 Pavol Babincak <pbabinca@redhat.com> - 1.19-2
- Remove python-offtrac from {build,}requires (rhbz#1157793)

* Fri Sep 26 2014 Pavol Babincak - 1.19-1
- Explicitly define fedpkg name for man pages (pbabinca)
- Remove (pbabinca)
- Revert "refactor: PEP 8 compliance of __init__.py" (pbabinca)
- refactor: PEP 8 compliance of __init__.py (pbabinca)
- refactor: PEP 8 compliance (pbabinca)
- retire: Ask for password only when required (opensource)
- fedpkg: Show full exception if verbose (opensource)
- add new s390 only packages (dan)
- add new ppc only packages (dan)

* Tue Jul 29 2014 Pavol Babincak <pbabinca@redhat.com> - 1.18-1
- Remove spec file again (pbabinca)
- Remove fedpkg-fixbranches as it isn't needed anymore (pbabinca)
- Remove offtrac module as we don't use Trac for buildroot override (pbabinca)
- Default name of executable if isn't possible to determine it (pbabinca)
- Allow executable name to be used as key for configuration (pbabinca)
- completion: Add mockbuild --root completion (ville.skytta)
- completion: Assume fedpkg is installed if the completion is, no need to test
  (ville.skytta)
- fix date in 1.11-2 changelog

* Tue Jul 29 2014 Dennis Gilmore <dennis@ausil.us> 1.17-3
- add missing Requires

* Fri Jul 04 2014 Pavol Babincak <pbabinca@redhat.com> - 1.17-2
- Use tar.bz2 archive which spec expects instead of tar.gz

* Fri Jul 04 2014 Pavol Babincak <pbabinca@redhat.com> - 1.17-1
- Removed spec as fedpkg is now in dist-git (pbabinca)
- Fix retirement (bochecha)

* Tue Jun 24 2014 Dennis Gilmore <dennis@ausil.us> - 1.16-1
- retire: Make retirement message/reason mandatory (opensource)
- retire: Use pkgdb2 API (opensource)
- Don't check for the config file if the user is asking for help (bochecha)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 16 2013 <dennis@ausil.us> - 1.15-1
- remove tag-request we no longer use that work flow, the process is managed
  via blocker bugs now (dennis)
- use the rpm changelog as default update template patch from
  https://bugzilla.redhat.com/show_bug.cgi?id=1023915 (dennis)
- allow epel branches to be epel<release> clean up overrides (dennis)
- Fix log message (bochecha)

* Mon Aug 26 2013 Dennis Gilmore <dennis@ausil.us> - 1.14-1
- clean up arches in fedpkg bash completeion - drop sparc - add i686 - add arm
  variants - add ppc64p7 (dennis)
- Add arm7hl to bash completion arches (opensource)
- Add more ppc64-only packages (opensource)
- remove --push from retire command in bash completion (opensource)
- undefine macros rather than define as nil (dennis)

* Sat Aug 24 2013 Dennis Gilmore <dennis@ausil.us> - 1.13-1
- Rework --retire (opensource)

* Sat Aug 24 2013 Dennis Gilmore <dennis@ausil.us> - 1.12-1
- update ppc secondary arch packages, remove sparc, point to new seconary arch
  config location (dennis)
- retire packages in packagedb as well (opensource)
- Move fedpkg to own module (opensource)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 06 2013 Tom Callaway <spot@fedoraproject.org> - 1.11-2
- use --eval '%%undefine to unset dist values instead of nil (bz876308)

* Tue Nov 06 2012 Jesse Keating <jkeating@redhat.com> - 1.11-1
- Unset runtime disttag (spot)
- use nil to unset dist values. (spot)

* Tue Oct 09 2012 Jesse Keating <jkeating@redhat.com> - 1.10-1
- Force invalid dist values to 0 (spot) (jkeating)
- Fix a traceback in fixbranches (#817478) (jkeating)

* Mon Mar 12 2012 Jesse Keating <jkeating@redhat.com> - 1.9-1
- Wrap the prune command in a try (rhbz#785820) (jkeating)
- Use koji if we have it to get master details (rhbz#785234) (jkeating)
- Always send builds from master to 'rawhide' (rhbz#785234) (jkeating)
- Handle fedpkg calls not from a git repo (rhbz#785776) (jkeating)

* Thu Mar 01 2012 Jesse Keating <jkeating@redhat.com> - 1.8-1
- More completion fixes (jkeating)
- Add mock-config and mockbuild completion (jkeating)
- Simplify test for fedpkg availability. (ville.skytta)
- Fix ~/... path completion. (ville.skytta)
- Add --raw to bash completion (jkeating)
- Make things quiet when possible (jkeating)
- Fix property variables (jkeating)

* Sat Jan 14 2012 Jesse Keating <jkeating@redhat.com> - 1.7-1
- Adapt property overloading to new-style class. (bochecha)
- Use super(), now that rpkg uses new-style classes everywhere (bochecha)
- Add gitbuildurl to the bash completion. (jkeating)
- Handle koji config with unknown module name (jkeating)

* Mon Nov 21 2011 Jesse Keating <jkeating@redhat.com> - 1.6-1
- Replace -c with -C for the --config option (jkeating)
- Package up fedpkg-fixbranches (#751507) (jkeating)
- Use old style of super class calls (jkeating)

* Mon Nov 07 2011 Jesse Keating <jkeating@redhat.com> - 1.5-1
- Pass along the return value from import_srpm (jkeating)
- Whitespace cleanup (jkeating)

* Mon Nov 07 2011 Jesse Keating <jkeating@redhat.com> - 1.4-1
- Use the GPLv2 content for COPYING to match intent. (jkeating)

* Thu Nov 03 2011 Jesse Keating <jkeating@redhat.com> - 1.3-1
- Fix buildrequires (jkeating)
- Don't register a nonexestant target (jkeating)
- Drop koji-rhel.conf file (jkeating)
- Fix up the setup.py (jkeating)

* Thu Nov 03 2011 Jesse Keating <jkeating@redhat.com> - 1.2-1
- Catch raises in the libraries (jkeating)
- Fix the fixbranches script for new module name (jkeating)
- srpm takes arguments, pass them along (jkeating)
- Get error output from user detection failures (jkeating)
- Get the user name from the Fedora SSL certificate. (bochecha)
- Fix crash when detecting Rawhide. (bochecha)

* Fri Oct 28 2011 Jesse Keating <jkeating@redhat.com> - 1.1-1
- Overload curl stuff (jkeating)
- Hardcode fedpkg version requires (jkeating)
- Fix up changelog date (jkeating)
