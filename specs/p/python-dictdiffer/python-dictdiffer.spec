# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
%bcond doc %[ %{defined fc43} || %{defined fc42} ]

Name:           python-dictdiffer
Version:        0.9.0
Release:        19%{?dist}
Summary:        Dictdiffer is a module that helps you to diff and patch dictionaries

License:        MIT
URL:            https://github.com/inveniosoftware/dictdiffer
Source:         %{url}/archive/v%{version}/dictdiffer-%{version}.tar.gz

# tests: remove pytest-runner / setup.py test support
# https://github.com/inveniosoftware/dictdiffer/pull/192
# rebased on v0.9.0
Patch:          0001-tests-remove-pytest-runner-setup.py-test-support.patch
# Downstream-only: remove linting/coverage options for pytest
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
Patch:          0002-Downstream-only-remove-linting-coverage-options-for-.patch

# List test dependencies manually since the test extra has various unwanted
# dependencies, including linting/coverage tools:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
BuildRequires:  %{py3_dist pytest}

BuildArch:      noarch

%global common_description %{expand:
%{summary}.}

%description %{common_description}


%package -n python3-dictdiffer
Summary:        %{summary}

%if %{without doc} && %{defined fedora}
Obsoletes:      python-dictdiffer-doc < 0.9.0-18
%endif

%global common_description %{expand:
%{summary}.}

%description -n python3-dictdiffer %{common_description}


%pyproject_extras_subpkg -n python3-dictdiffer numpy


%if %{with doc}
%package doc
Summary: Documentation for %{name}

%description doc
%{summary}.
%endif


%prep
%autosetup -n dictdiffer-%{version}


%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION='%{version}'
%pyproject_buildrequires -x numpy %{?with_doc:-x docs}


%build
export SETUPTOOLS_SCM_PRETEND_VERSION='%{version}'
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l dictdiffer

%if %{with doc}
PYTHONPATH='%{buildroot}%{python3_sitelib}' sphinx-build docs/ html
rm -rf html/.buildinfo html/.doctrees
%endif


%check
%pyproject_check_import

# Since this project does not use src layout, we must make sure pytest does not
# see both the “local” module and the one installed in the buildroot. The
# easiest thing to do is to explicitly test the local copy rather than the
# installed one by setting PYTHONPATH.
PYTHONPATH="${PWD}" %pytest


%files -n python3-dictdiffer -f %{pyproject_files}


%if %{with doc}
%files doc
%license LICENSE
%doc html/
%endif


%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sun Jan 11 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.0-18
- Port to pyproject-rpm-macros, diverge from EPEL8; fixes RHBZ#2377624
- Drop -doc subpackage starting with F44
- Add metapackage for numpy extra

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.9.0-17
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.9.0-16
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.9.0-14
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 14 2024 Jason Montleon <jmontleo@redhat.com> - 0.9.0-12
- Enable tests again
- Switch to using %%pytest
- Disable code and doc style tests

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 0.9.0-10
- Rebuilt for Python 3.13

* Thu Feb 22 2024 Michel Lind <salimma@fedoraproject.org> - 0.9.0-9
- Remove unnecessary and deprecated python3-mock BR

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 19 2023 Jason Montleon <jmontleo@redhat.com> - 0.9.0-6
- Remove unneeded pydocstyle dependency preventing rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 0.9.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Jaosn Montleon <jmontleo@redhat.com> 0.9.0-1
- Update to 0.9.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.8.1-7
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.8.1-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 28 2019 Jaosn Montleon <jmontleo@redhat.com> 0.8.1-2
- Bump release due to infra problem

* Fri Dec 13 2019 Jaosn Montleon <jmontleo@redhat.com> 0.8.1-1
- Update to upstream 0.8.1

* Tue Nov 19 2019 Jason Montleon <jmontleo@redhat.com> 0.8.0-1
- Update to upstream 0.8.0

* Fri Oct 18 2019 Jason Montleon <jmontleo@redhat.com> 0.7.1-8
- Fix build failures, epel 8 macros

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 8 2019 Orion Poplawski <orion@nwra.com> - 0.7.1-4
- Drop BR on pytest-cache

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 18 2018 Dniel Mellado <dmellado@redhat.com> 0.7.1-2
- Remove inconsistency in build requirements
- Align spec in SRPM

* Tue Dec 4 2018 John Kim <jkim@redhat.com> 0.7.1-1
- Bump Versio to 0.7.1-1
- Fixed URL, Source0
- Enable disable python3 for rhel
- Add docs for fedora
- Enable tests for fedora

* Wed May 10 2017 Jason Montleon <jmontleo@redhat.com> 0.6.1-1
- Initial Build
