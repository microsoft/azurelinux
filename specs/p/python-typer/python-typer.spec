## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This package corresponds to three PyPI projects (typer-slim, typer,
# typer-cli) all co-developed in one repository. Since the three are versioned
# identically and released at the same time, it makes sense to build them from
# a single source package.
Name:           python-typer
Version:        0.21.2
Release:        %autorelease
Summary:        Build great CLIs; easy to code; based on Python type hints

# SPDX
License:        MIT
URL:            https://typer.tiangolo.com/
%global forgeurl https://github.com/fastapi/typer
Source0:        %{forgeurl}/archive/%{version}/typer-%{version}.tar.gz
# Hand-written for Fedora in groff_man(7) format based on typer --help.
Source10:       typer.1
# To get help text for
#   typer [PATH_OR_MODULE] utils --help
# first create empty file x.py, then run:
#   PYTHONPATH="${PWD}" typer x utils --help.
Source11:       typer-utils.1
# …and similarly,
#   PYTHONPATH="${PWD}" typer x utils docs --help.
Source12:       typer-utils-docs.1

BuildArch:      noarch

BuildRequires:  python3-devel

# Since the “tests” dependency group contains overly-strict version bounds and
# many unwanted linting/coverage/typechecking/formatting dependencies
# (https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters),
# we just list the few test dependencies we *do* want manually rather than
# trying to patch pyproject.toml. We preserve upstream’s lower bounds but
# remove upper bounds, as we must try to make do with what we have.
BuildRequires:  %{py3_dist pytest} >= 4.4
BuildRequires:  %{py3_dist pytest-xdist} >= 1.32

%global common_description %{expand:
Typer is a library for building CLI applications that users will love using and
developers will love creating. Based on Python type hints.}

%description %{common_description}


%package -n     python3-typer-slim
Summary:        %{summary}

%if %[ %{defined fc42} || %{defined fc43} ]
# The python3-typer-slim package was introduced in F41; it corresponds roughly
# to the python3-typer (vs. python3-typer+all) in F40.
Obsoletes:      python3-typer < 0.12.1-1
Conflicts:      python3-typer < 0.12.1-1
%endif

%description -n python3-typer-slim %{common_description}


%package -n     python3-typer
Summary:        %{summary}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_requiring_base_package
Requires:       python3-typer-cli = %{version}-%{release}
Requires:       python3-typer-slim = %{version}-%{release}

%if %[ %{defined fc42} || %{defined fc43} ]
# The python3-typer+all metapackage package was removed in F41; since
# python3-typer-slim was introduced, python3-typer is the closest replacement.
Obsoletes:      python3-typer+all < 0.12.1-1
Conflicts:      python3-typer+all < 0.12.1-1
%endif

%description -n python3-typer %{common_description}


%package -n     python3-typer-cli
Summary:        %{summary}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_requiring_base_package
Requires:       python3-typer-slim = %{version}-%{release}

# A file conflict existed between erlang-dialyzer and python3-typer-cli. It was
# resolved by renaming erlang-dialyzer’s typer executable to erlang-typer:
# https://src.fedoraproject.org/rpms/erlang/pull-request/6
#
# This change was made for Fedora 43, so we can remove the Conflicts for
# previous versions after Fedora 45.
#
# File conflicts: /usr/bin/typer with erlang-dialyzer
# https://bugzilla.redhat.com/show_bug.cgi?id=2359557
# File conflicts: /usr/bin/typer between erlang-dialyzer and python3-typer-cli
# https://bugzilla.redhat.com/show_bug.cgi?id=2359567
Conflicts:      erlang-dialyzer < 26.2.5.13-2

%description -n python3-typer-cli %{common_description}

This package only provides a command typer in the shell with the same
functionality of python -m typer.

The only reason why this is a separate package is to allow developers to opt
out of the typer command by installing typer-slim, that doesn’t include
typer-cli.


%pyproject_extras_subpkg -n python3-typer-slim -i %{python3_sitelib}/typer_slim-%{version}.dist-info standard


%prep
%autosetup -n typer-%{version} -p1


%generate_buildrequires
export TIANGOLO_BUILD_PACKAGE='typer-slim'
%pyproject_buildrequires -x standard
(
  export TIANGOLO_BUILD_PACKAGE='typer'
  %pyproject_buildrequires
) | grep -vE '\btyper\b'
(
  export TIANGOLO_BUILD_PACKAGE='typer-cli'
  %pyproject_buildrequires
) | grep -vE '\btyper\b'


%build
export TIANGOLO_BUILD_PACKAGE='typer-slim'
%pyproject_wheel
export TIANGOLO_BUILD_PACKAGE='typer'
%pyproject_wheel
export TIANGOLO_BUILD_PACKAGE='typer-cli'
%pyproject_wheel


%install
%pyproject_install

install -t '%{buildroot}%{_mandir}/man1' -D -p -m 0644 \
    '%{SOURCE10}' '%{SOURCE11}' '%{SOURCE12}'

install -d \
    '%{buildroot}%{bash_completions_dir}' \
    '%{buildroot}%{zsh_completions_dir}' \
    '%{buildroot}%{fish_completions_dir}'
export PYTHONPATH='%{buildroot}%{python3_sitelib}'
export _TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION=1
'%{buildroot}%{_bindir}/typer' --show-completion bash \
    > '%{buildroot}%{bash_completions_dir}/typer'
'%{buildroot}%{_bindir}/typer' --show-completion zsh \
    > '%{buildroot}%{zsh_completions_dir}/_typer'
'%{buildroot}%{_bindir}/typer' --show-completion fish \
    > '%{buildroot}%{fish_completions_dir}/typer.fish'


%check
# See scripts/test.sh. We do not run the linters (scripts/lint.sh, i.e.,
# mypy/black/isort).
export TERMINAL_WIDTH=3000
export _TYPER_FORCE_DISABLE_TERMINAL=1
export _TYPER_RUN_INSTALL_COMPLETION_TESTS=1

# These cannot find the typer package because the tests override PYTHONPATH.
ignore="${ignore-} --ignore=tests/test_tutorial/test_subcommands/test_tutorial001.py"
ignore="${ignore-} --ignore=tests/test_tutorial/test_subcommands/test_tutorial003.py"
# This fails in mock but not in a git checkout. We have not found it worth
# investigating, but help is welcome.
ignore="${ignore-} --ignore=tests/test_tutorial/test_printing/test_tutorial004.py"

mkdir _stub
cat > _stub/coverage.py <<'EOF'
from subprocess import run
from sys import argv, executable, exit
if len(argv) < 3 or argv[1] != "run":
    exit(f"Unsupported arguments: {argv!r}")
exit(run([executable] + argv[2:]).returncode)
EOF
export PYTHONPATH="${PWD}/_stub:%{buildroot}%{python3_sitelib}"

%pytest -k "${k-}" ${ignore-} -n auto -v -rs


%files -n python3-typer-slim
%license LICENSE
%doc README.md
%doc docs/release-notes.md

%{python3_sitelib}/typer/
%{python3_sitelib}/typer_slim-%{version}.dist-info/


%files -n python3-typer
%{python3_sitelib}/typer-%{version}.dist-info/


%files -n python3-typer-cli
%{python3_sitelib}/typer_cli-%{version}.dist-info/

%{_bindir}/typer
%{_mandir}/man1/typer*.1*
%{bash_completions_dir}/typer
%{zsh_completions_dir}/_typer
%{fish_completions_dir}/typer.fish


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 0.21.2-2
- Latest state for python-typer

* Wed Feb 11 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.21.2-1
- Update to 0.21.2 (close RHBZ#2438760)

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 06 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.21.1-1
- Update to 0.21.1 (close RHBZ#2427388)

* Fri Dec 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.21.0-1
- Update to 0.21.0 (close RHBZ#2425372)

* Sat Dec 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.20.1-1
- Update to 0.20.1 (close RHBZ#2423930)

* Thu Nov 06 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.20.0-2
- Drop conditionals for F41, soon to be EOL

* Tue Oct 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.20.0-1
- Update to 0.20.0 (close RHBZ#2405172)

* Wed Sep 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.19.2-1
- Update to 0.19.2 (close RHBZ#2397609)

* Sat Sep 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.19.1-3
- Drop test skips for click 8.2.2 (click was downgraded in Fedora)

* Sat Sep 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.19.1-1
- Update to 0.19.1 (close RHBZ#2397078)

* Sat Sep 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.19.0-1
- Update to 0.19.0

* Sat Sep 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.18.0-1
- Update to 0.18.0 (close RHBZ#2397015)
- This release adds compatibility with Click 8.3.0.

* Fri Sep 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.5-1
- Update to 0.17.5 (close RHBZ#2396961)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.17.4-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Sat Sep 06 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.4-1
- Update to 0.17.4 (close RHBZ#2393554)

* Sun Aug 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.3-1
- Update to 0.17.3 (close RHBZ#2392124)

* Tue Aug 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.16.1-2
- Skip tests that fail with click 8.2.2

* Tue Aug 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.16.1-1
- Update to 0.16.1 (close RHBZ#2389252)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.16.0-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 18 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.16.0-5
- Remove Conflicts with erlang-dialyzer
- Since erlang-26.2.5.13-2, python3-typer-cli no longer conflicts with
  erlang-dialyzer; we keep the Conflicts for older versions.

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.16.0-2
- Rebuilt for Python 3.14

* Tue May 27 2025 Charalampos Stratakis <cstratak@redhat.com> - 0.16.0-1
- Update to 0.16.0 (close RHBZ#2368612)

* Thu May 15 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.15.4-1
- Update to 0.15.4 (close RHBZ#2366313)

* Tue Apr 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.15.3-1
- Update to 0.15.3 (close RHBZ#2362813)

* Mon Apr 14 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.15.2-3
- Make the conflict between python3-typer-cli and erlang-dialyzer explicit

* Mon Apr 14 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.15.2-2
- Correct descriptions

* Fri Feb 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.15.2-1
- Update to 0.15.2 (close RHBZ#2348921)

* Fri Feb 14 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.15.1-4
- Add Obsoletes/Conflicts for python3-typer+all in F40 and before
- Fixes RHBZ#2345612

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.15.1-1
- Update to 0.15.1 (close RHBZ#2330178)

* Wed Dec 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.14.0-2
- Fix some stray whitespace in the primary man page

* Fri Nov 29 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.14.0-1
- Update to 0.14.0 (close RHBZ#2329419)

* Tue Nov 19 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.13.1-1
- Update to 0.13.1 (close RHBZ#2327149)

* Tue Nov 19 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.13.0-3
- Stub out "coverage run" well enough to drop the coverage dep.

* Sun Nov 10 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.13.0-2
- No longer skip the shell completion tests
- These are now more adaptable to different environments and do not fail

* Sun Nov 10 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.13.0-1
- Update to 0.13.0 (close RHBZ#2324487)

* Sat Aug 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.5-1
- Update to 0.12.5 (close RHBZ#2307757)

* Sat Aug 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.4-2
- Package the release notes alongside the README

* Wed Aug 21 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.4-1
- Update to 0.12.4 (close RHBZ#2306098)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 0.12.3-3
- Rebuilt for Python 3.13

* Fri Apr 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.3-1
- Update to 0.12.3 (close RHBZ#2272276)

* Fri Apr 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.2-1
- Update to 0.12.2

* Mon Apr 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.1-1
- Update to 0.12.1
- Now encompasses the typer, typer-slim, and typer-cli PyPI packages.

* Thu Apr 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.1-4
- Switch from the PyPI sdist to the GitHub archive

* Wed Apr 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.1-3
- Remove an Obsoletes that has served its upgrade-path purpose

* Fri Mar 29 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.1-2
- Add missing source

* Fri Mar 29 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.1-1
- Update to 0.11.1 (close RHBZ#2272130)
- Build from the PyPI sdist, now that it contains tests

* Wed Mar 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.0-1
- Update to 0.11.0 (close RHBZ#2271198)

* Wed Mar 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.0-1
- Update to 0.10.0

* Wed Mar 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.4-1
- Update to 0.9.4

* Wed Mar 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.3-1
- Update to 0.9.3

* Wed Mar 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.2-1
- Update to 0.9.2
- Give up on patching out the dependency on the coverage module

* Wed Mar 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.1-1
- Update to 0.9.1
- New CITATION.cff file is packaged as documentation.

* Wed Mar 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.0-9
- Simplify patching pyproject.toml and handling test dependencies
- Drop unnecessary version-bounded BuildRequires on python-pytest-sugar,
  fixing failure to build from source with python-pytest-sugar 1.0.0.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 0.9.0-3
- Rebuilt for Python 3.12

* Tue May 02 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.0-1
- Update to 0.9.0 (close RHBZ#2192484)

* Mon May 01 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.0-1
- Update to 0.8.0 (close RHBZ#2192330)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.0-4
- Allow rich 13.x (fix RHBZ#2157866)

* Wed Dec 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.0-3
- Rely on PYTEST_XDIST_AUTO_NUM_WORKERS

* Sat Nov 12 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.0-2
- Add some environment variables from scripts/test.sh

* Sun Nov 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.0-1
- Update to 0.7.0 (close RHBZ#2140338)

* Sun Nov 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.1-3
- Confirm License is SPDX MIT

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.1-1
- Update to 0.6.1 (close RHBZ#2106487)

* Wed Jul 13 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.0-2
- Run tests in parallel with pytest-xdist

* Wed Jul 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.0-1
- Update to 0.5.0 (close RHBZ#2103375)

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 0.4.1-3
- Rebuilt for Python 3.11

* Fri Apr 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.1-2
- Patch out coverage analysis

* Thu Mar 31 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.1-1
- Update to 0.4.1 (close RHBZ#2070317)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 15 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.0-8
- Allow newer python-coverage, i.e., >=6.0

* Tue Oct 19 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.0-7
- Drop pytest-cov BR

* Tue Sep 28 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.0-6
- Drop the documentation subpackage entirely.

* Mon Sep 13 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.0-5
- Revert "Let pyproject-rpm-macros handle the license file"

* Mon Sep 13 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.0-4
- Drop BR on pyproject-rpm-macros, now implied by python3-devel

* Mon Sep 13 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.0-3
- Let pyproject-rpm-macros handle the license file

* Mon Sep 13 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.0-2
- Reduce macro indirection in the spec file

* Tue Aug 31 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.0-1
- Update to 0.4.0 (fix RHBZ#1977513)

* Wed Jun 30 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.2-4
- Remove reference to bug for out-of-date mkdocs-material

* Thu Jun 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.2-3
- Drop documentation dependency on mkdocs-material (RHBZ#1960274, comment 3)

* Wed May 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.2-2
- Unbundle js-termynal

* Tue May 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.2-1
- Initial package

## END: Generated by rpmautospec
