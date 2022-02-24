Summary:        RPM macros for PEP 517 Python packages
Name:           pyproject-rpm-macros
# The idea is to follow the spirit of semver
# Given version X.Y.Z:
#   Increment X and reset Y.Z when there is a *major* incompatibility
#   Increment Y and reset Z when new macros or features are added
#   Increment Z when this is a bugfix or a cosmetic change
# Dropping support for EOL Fedoras is *not* considered a breaking change
Version:        1.0.0~rc1
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://src.fedoraproject.org/rpms/pyproject-rpm-macros

BuildArch:      noarch

# Macro files
Source001:      macros.pyproject

# Implementation files
Source101:      pyproject_buildrequires.py
Source102:      pyproject_save_files.py
Source103:      pyproject_convert.py
Source104:      pyproject_preprocess_record.py
Source105:      pyproject_construct_toxenv.py
Source106:      pyproject_requirements_txt.py

# Tests
Source201:      test_pyproject_buildrequires.py
Source202:      test_pyproject_save_files.py
Source203:      test_pyproject_requirements_txt.py
Source204:      compare_mandata.py

# Test data
Source301:      pyproject_buildrequires_testcases.yaml
Source302:      pyproject_save_files_test_data.yaml
Source303:      test_RECORD

# Metadata
Source901:      README.md
Source902:      LICENSE

%if %{with_check}
BuildRequires:  python3dist(packaging)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pyyaml)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(tox-current-env) >= 0.0.6
BuildRequires:  python3dist(wheel)
# Available only in SPECS-EXTENDED:
BuildRequires:  python3dist(toml)
%endif

Requires:       %{_bindir}/find
Requires:       /bin/sed
Requires:       python-rpm-macros
Requires:       python-srpm-macros
Requires:       python3-rpm-macros

%description
These macros allow projects that follow the Python packaging specifications
to be packaged as RPMs.

They work for:

* traditional Setuptools-based projects that use the setup.py file,
* newer Setuptools-based projects that have a setup.cfg file,
* general Python projects that use the PEP 517 pyproject.toml file
  (which allows using any build system, such as setuptools, flit or poetry).

These macros replace %%py3_build and %%py3_install,
which only work with setup.py.

%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%setup -q -c -T
cp -p %{sources} .

%build
# nothing to do, sources are not buildable

%install
mkdir -p %{buildroot}%{_rpmmacrodir}
mkdir -p %{buildroot}%{_rpmconfigdir}/mariner
install -m 644 macros.pyproject %{buildroot}%{_rpmmacrodir}/
install -m 644 pyproject_buildrequires.py %{buildroot}%{_rpmconfigdir}/mariner/
install -m 644 pyproject_convert.py %{buildroot}%{_rpmconfigdir}/mariner/
install -m 644 pyproject_save_files.py  %{buildroot}%{_rpmconfigdir}/mariner/
install -m 644 pyproject_preprocess_record.py %{buildroot}%{_rpmconfigdir}/mariner/
install -m 644 pyproject_construct_toxenv.py %{buildroot}%{_rpmconfigdir}/mariner/
install -m 644 pyproject_requirements_txt.py %{buildroot}%{_rpmconfigdir}/mariner/

%check
export HOSTNAME="rpmbuild"  # to speedup tox in network-less mock, see rhbz#1856356
%{python3} -m pytest -vv --doctest-modules

# brp-compress is provided as an argument to get the right directory macro expansion
%{python3} compare_mandata.py -f %{_rpmconfigdir}/brp-compress


%files
%{_rpmmacrodir}/macros.pyproject
%{_rpmconfigdir}/mariner/pyproject_buildrequires.py
%{_rpmconfigdir}/mariner/pyproject_convert.py
%{_rpmconfigdir}/mariner/pyproject_save_files.py
%{_rpmconfigdir}/mariner/pyproject_preprocess_record.py
%{_rpmconfigdir}/mariner/pyproject_construct_toxenv.py
%{_rpmconfigdir}/mariner/pyproject_requirements_txt.py

%doc README.md
%license LICENSE

%changelog
* Mon Feb 14 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0~rc1-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Tue Jan 25 2022 Miro Hrončok <mhroncok@redhat.com> - 1.0.0~rc1-1
- Release version 1.0.0, first release candidate

* Mon Jan 24 2022 Miro Hrončok <mhroncok@redhat.com> - 0-55
- %%pyproject_buildrequires: Generate BuildRequires for this package
  This package is already installed, but this way, the resulting SRPM explicitly BuildRequires it

* Wed Jan 19 2022 Karolina Surma <ksurma@redhat.com> - 0-54
- Include compressed manpages to the package if flag '+auto' is provided to %%pyproject_save_files
- Fixes: rhbz#2033254

* Fri Jan 14 2022 Miro Hrončok <mhroncok@redhat.com> - 0-53
- %%pyproject_buildrequires: Make -r (include runtime) the default, use -R to opt-out

* Sun Dec 19 2021 Gordon Messmer <gordon.messmer@gmail.com> - 0-52
- Handle legacy version specifiers that would previously raise exceptions.

* Wed Dec 08 2021 Miro Hrončok <mhroncok@redhat.com> - 0-51
- Define provisional %%pyproject_build_lib

* Mon Nov 1 2021 Gordon Messmer <gordon.messmer@gmail.com> - 0-50
- Improve handling of > operator, preventing post-release from satisfying most rpm requirements
- Improve handling of < operator, preventing pre-release from satisfying rpm requirement
- Improve handling of != operator with prefix matching, preventing pre-release from satisfying rpm requirements

* Tue Oct 19 2021 Karolina Surma <ksurma@redhat.com> - 0-49
- %%pyproject_save_files: Save %%_pyproject_modules file with importable module names
- Introduce %%pyproject_check_import which passes %%_pyproject_modules to %%py3_check_import
- Introduce -t, -e filtering options to %%pyproject_check_import

* Sat Oct 16 2021 Miro Hrončok <mhroncok@redhat.com> - 0-48
- %%pyproject_buildrequires: Accept installed pre-releases for all requirements
- Fixes: rhbz#2014639

* Thu Sep 09 2021 Miro Hrončok <mhroncok@redhat.com> - 0-47
- %%pyproject_save_files: Expand the namespace error message, also display it with /
- %%pyproject_save_files: Add a workaround error for spaces and [brackets]

* Fri Jul 23 2021 Miro Hrončok <miro@hroncok.cz> - 0-46
- %%pyproject_buildrequires now fails when it encounters an invalid requirement
- Fixes: rhbz#1983053
- Rename %%_pyproject_ghost_distinfo and %%_pyproject_record to indicate they are private
- Automatically detect LICENSE files and mark them with %%license macro

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Python Maint <python-maint@redhat.com> - 0-44
- Escape weird paths generated by %%pyproject_save_files
- Fixes rhbz#1976363
- Support x.* versions in %%pyproject_buildrequires
- Fixes rhbz#1981558
- %%pyproject_buildrequires fallbacks to setuptools only if setup.py exists
- Fixes: rhbz#1976459
- Explicitly require the "basic" Python RPM macros

* Thu Jul 01 2021 Tomas Hrnciar <thrnciar@redhat.com> - 0-43
- Generate BuildRequires from file
- Fixes: rhbz#1936448

* Tue Jun 29 2021 Miro Hrončok <mhroncok@redhat.com> - 0-42
- Don't accidentally treat "~= X.0" requirement as "~= X"
- Fixes rhbz#1977060

* Mon Jun 28 2021 Miro Hrončok <mhroncok@redhat.com> - 0-41
- Don't leak %%{_pyproject_builddir} to pytest collection
- Fixes rhbz#1935212

* Thu May 27 2021 Miro Hrončok <mhroncok@redhat.com> - 0-40
- Don't leak $TMPDIR outside of pyproject macros
- Set %%_pyproject_wheeldir and %%_pyproject_builddir relative to the source tree, not $PWD

* Mon Mar 29 2021 Miro Hrončok <mhroncok@redhat.com> - 0-39
- Handle tox provision (tox.requires / tox.minversion)
- Fixes: rhbz#1922495
- Generate BuildRequires on extras in lower case
- Fixes: rhbz#1937944

* Sun Feb 07 2021 Miro Hrončok <mhroncok@redhat.com> - 0-38
- Include nested __pycache__ directories in %%pyproject_save_files
- Fixes: rhbz#1925963

* Tue Feb 02 2021 Miro Hrončok <mhroncok@redhat.com> - 0-37
- Remove support for Python 3.7 from %%pyproject_buildrequires
- Generate python3dist(toml) BR with pyproject.toml earlier to avoid extra install round
- Generate python3dist(setutpools/wheel) BR without pyproject.toml earlier as well

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Miro Hrončok <mhroncok@redhat.com> - 0-35
- Update the description of the package to match the new README content

* Fri Dec 04 2020 Miro Hrončok <miro@hroncok.cz> - 0-34
- List all files in %%pyproject_files explicitly to avoid duplicate %%lang entries
- If you amend the installed files after %%pyproject_install, %%pyproject_files might break

* Fri Nov 27 2020 Miro Hrončok <mhroncok@redhat.com> - 0-33
- Pass PYTHONDONTWRITEBYTECODE=1 to %%tox to avoid packaged PYTEST bytecode

* Tue Nov 03 2020 Miro Hrončok <mhroncok@redhat.com> - 0-32
- Allow multiple -e in %%pyproject_buildrequires
- Fixes: rhbz#1886509

* Mon Oct 05 2020 Miro Hrončok <mhroncok@redhat.com> - 0-31
- Support PEP 517 list based backend-path

* Tue Sep 29 2020 Lumír Balhar <lbalhar@redhat.com> - 0-30
- Process RECORD files in %%pyproject_install and remove them
- Support the extras configuration option of tox in %%pyproject_buildrequires -t
- Support multiple -x options for %%pyproject_buildrequires
- Fixes: rhbz#1877977
- Fixes: rhbz#1877978

* Wed Sep 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0-29
- Check the requirements after installing "requires_for_build_wheel"
- If not checked, installing runtime requirements might fail

* Tue Sep 08 2020 Gordon Messmer <gordon.messmer@gmail.com> - 0-28
- Support more Python version specifiers in generated BuildRequires
- This adds support for the '~=' operator and wildcards

* Fri Sep 04 2020 Miro Hrončok <miro@hroncok.cz> - 0-27
- Make code in $PWD importable from %%pyproject_buildrequires
- Only require toml for projects with pyproject.toml
- Remove a no longer useful warning for unrecognized files in %%pyproject_save_files

* Mon Aug 24 2020 Tomas Hrnciar <thrnciar@redhat.com> - 0-26
- Implement automatic detection of %%lang files in %%pyproject_save_files
  and mark them with %%lang in filelist

* Fri Aug 14 2020 Miro Hrončok <mhroncok@redhat.com> - 0-25
- Handle Python Extras in %%pyproject_buildrequires on Fedora 33+

* Tue Aug 11 2020 Miro Hrončok <mhroncok@redhat.com> - 0-24
- Allow multiple, comma-separated extras in %%pyproject_buildrequires -x

* Mon Aug 10 2020 Lumír Balhar <lbalhar@redhat.com> - 0-23
- Make macros more universal for alternative Python stacks

* Thu Aug 06 2020 Tomas Hrnciar <thrnciar@redhat.com> - 0-22
- Change %%pyproject_save_files +bindir argument to +auto
  to list all unclassified files in filelist

* Tue Aug 04 2020 Miro Hrončok <mhroncok@redhat.com> - 0-21
- Actually implement %%pyproject_extras_subpkg

* Wed Jul 29 2020 Miro Hrončok <mhroncok@redhat.com> - 0-20
- Implement %%pyproject_extras_subpkg

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Miro Hrončok <mhroncok@redhat.com> - 0-18
- %%pyproject_buildrequires -x (extras requires for tests) now implies -r
  (runtime requires) instead of erroring without it for better UX.

* Wed Jul 15 2020 Miro Hrončok <mhroncok@redhat.com> - 0-17
- Set HOSTNAME to prevent tox 3.17+ from a DNS query
- Fixes rhbz#1856356

* Fri Jun 19 2020 Miro Hrončok <mhroncok@redhat.com> - 0-16
- Switch from upstream deprecated pytoml to toml

* Thu May 07 2020 Tomas Hrnciar <thrnciar@redhat.com> - 0-15
- Adapt %%pyproject_install not to create a PEP 610 direct_url.json file

* Wed Apr 15 2020 Patrik Kopkan <pkopkan@redhat.com> - 0-14
- Add %%pyproject_save_file macro for generating file section
- Handle extracting debuginfo from extension modules (#1806625)

* Mon Mar 02 2020 Miro Hrončok <mhroncok@redhat.com> - 0-13
- Tox dependency generator: Handle deps read in from a text file (#1808601)

* Wed Feb 05 2020 Miro Hrončok <mhroncok@redhat.com> - 0-12
- Fallback to setuptools.build_meta:__legacy__ backend instead of setuptools.build_meta
- Properly handle backends with colon
- Preserve existing flags in shebangs of Python files in /usr/bin

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Patrik Kopkan <pkopkan@redhat.com> - 0-10
- Install wheel in '$PWD/pyproject-macros-wheeldir' to have more explicit path from which we install.
- The path can be changed by redefining %%_pyproject_wheeldir.

* Wed Nov 13 2019 Anna Khaitovich <akhaitov@redhat.com> - 0-9
- Remove stray __pycache__ directory from /usr/bin when running %%pyproject_install

* Fri Oct 25 2019 Miro Hrončok <mhroncok@redhat.com> - 0-8
- When tox fails, print tox output before failing

* Tue Oct 08 2019 Miro Hrončok <mhroncok@redhat.com> - 0-7
- Move a verbose line of %%pyproject_buildrequires from stdout to stderr

* Fri Jul 26 2019 Petr Viktorin <pviktori@redhat.com> - 0-6
- Use importlib_metadata rather than pip freeze

* Fri Jul 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0-5
- Allow to fetch test dependencies from tox
- Add %%tox macro to invoke tests

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Miro Hrončok <mhroncok@redhat.com> - 0-3
- Add %%pyproject_buildrequires

* Tue Jul 02 2019 Miro Hrončok <mhroncok@redhat.com> - 0-2
- Fix shell syntax errors in %%pyproject_install
- Drop PATH warning in %%pyproject_install

* Fri Jun 28 2019 Patrik Kopkan <pkopkan@redhat.com> - 0-1
- created package
