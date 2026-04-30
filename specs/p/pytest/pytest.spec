## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 10;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           pytest
Version:        8.3.5
Release:        %autorelease
Summary:        Simple powerful testing with Python
# SPDX
License:        MIT
URL:            https://pytest.org
Source:         %{pypi_source pytest %{version}}

# Compatibility fix for attrs 25.2+
Patch:          https://github.com/pytest-dev/pytest/pull/13291.patch

# Officially support Python 3.14
# This fixes/xfails Python 3.14 test failures
# Rebased from https://github.com/pytest-dev/pytest/pull/13440
Patch:          13440.patch

# Fix compatibility with Twisted 25
# Rebased from https://github.com/pytest-dev/pytest/pull/13502
Patch:          13502.patch

# Fix test_doctest_unexpected_exception on Python 3.14
Patch:          https://github.com/pytest-dev/pytest/pull/13548.patch

# Remove -s from Python shebang,
# ensure that packages installed with pip to user locations are testable
# https://bugzilla.redhat.com/2152171
%undefine _py3_shebang_s

# When building pytest for the first time with new Python version
# we might not yet have all the BRs, those conditionals allow us to do that.

# This can be used to disable all tests for faster bootstrapping.
# The tests are enabled by default except when building on RHEL/ELN
# (to avoid pulling in extra dependencies into next RHEL).
%bcond tests %{undefined rhel}

# Only disabling the optional tests is a more complex but careful approach
# Pytest will skip the related tests, so we only conditionalize the BRs
%bcond optional_tests %{with tests}

# To run the tests in %%check we use pytest-timeout
# When building pytest for the first time with new Python version
# that is not possible as it depends on pytest
%bcond timeout %{with tests}

# When building pytest for the first time with new Python version
# we also don't have sphinx yet and cannot build docs.
# The docs are enabled by default except when building on RHEL/ELN
# (to avoid pulling in extra dependencies into next RHEL).
%bcond docs %{undefined rhel}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros >= 0-51

%if %{with tests}
# we avoid using %%pyproject_buildrequires -x testing as it mixes optional and non-optional deps
BuildRequires:  python3-attrs >= 19.2
BuildRequires:  python3-hypothesis >= 3.56
BuildRequires:  python3-pygments >= 2.7.2
BuildRequires:  python3-xmlschema
%if %{with optional_tests}
BuildRequires:  python3-argcomplete
#BuildRequires:  python3-asynctest -- not packaged in Fedora
BuildRequires:  python3-decorator
BuildRequires:  python3-jinja2
BuildRequires:  python3-mock
BuildRequires:  python3-numpy
BuildRequires:  python3-pexpect
BuildRequires:  python3-pytest-xdist
BuildRequires:  python3-twisted
BuildRequires:  /usr/bin/lsof
%endif
%if %{with timeout}
BuildRequires:  python3-pytest-timeout
%endif
%endif

%if %{with docs}
BuildRequires:  %{_bindir}/rst2html
# pluggy >= 1 is needed to build the docs, older versions are allowed on runtime:
BuildRequires:  python3-pluggy >= 1
BuildRequires:  python3-pygments-pytest
BuildRequires:  python3-furo
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-removed-in
BuildRequires:  python3-sphinxcontrib-trio
# See doc/en/conf.py -- sphinxcontrib.inkscapeconverter is only used when inkscape is available
# we don't BR inkscape so we generally don't need it, but in case inkscape is installed accidentally:
BuildRequires:  (python3-sphinxcontrib-inkscapeconverter if inkscape)
BuildRequires:  make
%endif

BuildArch:      noarch

%description
The pytest framework makes it easy to write small tests, yet scales to support
complex functional testing for applications and libraries.


%package -n python3-%{name}
Summary:        Simple powerful testing with Python
Provides:       pytest = %{version}-%{release}

%description -n python3-%{name}
The pytest framework makes it easy to write small tests, yet scales to support
complex functional testing for applications and libraries.


%prep
%autosetup -p1 -n %{name}-%{version}

# documentation dependencies missing in Fedora
sed -i '/sphinxcontrib-towncrier/d' doc/en/requirements.txt
sed -i '/sphinxcontrib\.towncrier/d' doc/en/conf.py
sed -i '/sphinx_issues/d' doc/en/conf.py
sed -i '/sphinx-issues/d' doc/en/requirements.txt


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel

%if %{with docs}
for l in doc/* ; do
  %make_build -C $l html PYTHONPATH="$(pwd)/src"
done
for f in README CHANGELOG CONTRIBUTING ; do
  rst2html ${f}.rst > ${f}.html
done
%endif


%install
%pyproject_install
%pyproject_save_files _pytest pytest py

mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest-%{python3_version}
ln -snf pytest-%{python3_version} %{buildroot}%{_bindir}/pytest-3
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test-%{python3_version}
ln -snf py.test-%{python3_version} %{buildroot}%{_bindir}/py.test-3

# We use 3.X per default
ln -snf pytest-%{python3_version} %{buildroot}%{_bindir}/pytest
ln -snf py.test-%{python3_version} %{buildroot}%{_bindir}/py.test

%if %{with docs}
mkdir -p _htmldocs/html
for l in doc/* ; do
  # remove hidden file
  rm ${l}/_build/html/.buildinfo
  mv ${l}/_build/html _htmldocs/html/${l##doc/}
done
%endif

# remove shebangs from all scripts
find %{buildroot}%{python3_sitelib} \
     -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;


%check
%if %{with tests}
%global __pytest %{buildroot}%{_bindir}/pytest
# optional_tests deps contain pytest-xdist, so we can use it to run tests faster
%pytest testing %{?with_timeout:--timeout=30} %{?with_optional_tests:-n auto} -rs
%else
%pyproject_check_import
%endif


%files -n python3-%{name} -f %{pyproject_files}
%if %{with docs}
%doc CHANGELOG.html
%doc README.html
%doc CONTRIBUTING.html
%doc _htmldocs/html
%endif
%{_bindir}/pytest
%{_bindir}/pytest-3
%{_bindir}/pytest-%{python3_version}
%{_bindir}/py.test
%{_bindir}/py.test-3
%{_bindir}/py.test-%{python3_version}


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 8.3.5-10
- test: add initial lock files

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 8.3.5-9
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 8.3.5-8
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug 04 2025 Miro Hrončok <miro@hroncok.cz> - 8.3.5-7
- Fix test failures with Python 3.14 and Twisted 25
- Fixes: rhbz#2353140

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Python Maint <python-maint@redhat.com> - 8.3.5-5
- Unbootstrap for Python 3.14

* Wed Jun 18 2025 Python Maint <python-maint@redhat.com> - 8.3.5-4
- Bootstrap for Python 3.14.0b3 bytecode

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 8.3.5-3
- Bootstrap for Python 3.14

* Thu Mar 13 2025 Lumir Balhar <lbalhar@redhat.com> - 8.3.5-2
- Fix compatibility with attrs 25.2+

* Wed Mar 05 2025 Lumir Balhar <lbalhar@redhat.com> - 8.3.5-1
- Update to 8.3.5 (rhbz#2349252)

* Wed Mar 05 2025 Karolina Surma <ksurma@redhat.com> - 8.3.4-3
- Enable compatibility with Pygments 2.19+

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 05 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 8.3.4-1
- Update to 8.3.4

* Fri Nov 01 2024 Miro Hrončok <miro@hroncok.cz> - 8.3.3-3
- Drop unused nose test dependency

* Tue Oct 15 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 8.3.3-2
- Backport upstream patch to enable skipped tests

* Fri Sep 13 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 8.3.3-1
- Update to 8.3.3

* Tue Sep 03 2024 Tomas Orsava <torsava@redhat.com> - 8.3.1-5
- Add simple smoke test

* Wed Jul 31 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 8.3.1-1
- Update to 8.3.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 7.4.3-7
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 7.4.3-6
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 09 2023 Miro Hrončok <mhroncok@redhat.com> - 7.4.3-1
- Update to 7.4.3
- Changelog: https://docs.pytest.org/en/stable/changelog.html#pytest-7-4-3-2023-10-24
- Fixes: rhbz#2245983

* Fri Sep 08 2023 Miro Hrončok <mhroncok@redhat.com> - 7.4.2-1
- Update to 7.4.2
- Changelog: https://docs.pytest.org/en/stable/changelog.html#pytest-7-4-2-2023-09-07
- Fixes: rhbz#2237942

* Wed Sep 06 2023 Miro Hrončok <mhroncok@redhat.com> - 7.4.1-1
- Update to 7.4.1
- Changelog: https://docs.pytest.org/en/stable/changelog.html#pytest-7-4-1-2023-09-02
- Fixes: rhbz#2236995

* Mon Aug 07 2023 Lumír Balhar <lbalhar@redhat.com> - 7.4.0-1
- Update to 7.4.0
Resolves: rhbz#2216956

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 7.3.2-3
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 7.3.2-2
- Bootstrap for Python 3.12

* Mon Jun 12 2023 Maxwell G <maxwell@gtmx.me> - 7.3.2-1
- Update to 7.3.2. Fixes rhbz#2213992.

* Mon Apr 24 2023 Miro Hrončok <mhroncok@redhat.com> - 7.3.1-2
- Fix build with setuptools >= 67.5.0
- Fixes: rhbz#2188982

* Mon Apr 17 2023 Miro Hrončok <mhroncok@redhat.com> - 7.3.1-1
- Update to 7.3.1
- Changelog: https://docs.pytest.org/en/stable/changelog.html#pytest-7-3-1-2023-04-14
- Fixes: rhbz#2186895

* Sun Apr 09 2023 Miro Hrončok <mhroncok@redhat.com> - 7.3.0-1
- Update to 7.3.0
- Changelog: https://docs.pytest.org/en/stable/changelog.html#pytest-7-3-0-2023-04-08
- Fixes: rhbz#2185393

* Fri Mar 24 2023 Miro Hrončok <mhroncok@redhat.com> - 7.2.2-1
- Update to 7.2.2
- Changelog: https://docs.pytest.org/en/7.2.x/changelog.html#pytest-7-2-2-2023-03-03
- Fixes: rhbz#2175310

* Fri Feb 10 2023 Stephen Gallagher <sgallagh@redhat.com> - 7.2.1-2
- Don't build tests and docs on RHEL to reduce dependencies

* Fri Jan 27 2023 Miro Hrončok <mhroncok@redhat.com> - 7.2.1-1
- Update to 7.2.1
- Fixes: rhbz#2160925

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 10 2022 Miro Hrončok <mhroncok@redhat.com> - 7.2.0-2
- Remove -s from Python shebang,
  ensure that packages installed with pip to user locations are testable
- Fixes: rhbz#2152171

* Tue Nov 01 2022 Lumír Balhar <lbalhar@redhat.com> - 7.2.0-1
- Update to 7.2.0
Resolves: rhbz#2137514

* Sat Sep  3 2022 Thomas Moschny <thomas.moschny@gmx.de> - 7.1.3-1
- Update to 7.1.3
- Fixes: rhbz#2123701

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Miro Hrončok <mhroncok@redhat.com> - 7.1.2-4
- Adjust tests for a last minute Python 3.11 change in the traceback format

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 7.1.2-3
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 7.1.2-2
- Bootstrap for Python 3.11

* Fri Apr 08 2022 Lumír Balhar <lbalhar@redhat.com> - 7.1.2-1
- Update to 7.1.2
Resolves: rhbz#2063549

* Tue Mar 01 2022 Miro Hrončok <mhroncok@redhat.com> - 7.0.1-1
- Update to 7.0.1
- Fixes: rhbz#2050629

* Fri Jan 21 2022 Miro Hrončok <mhroncok@redhat.com> - 7.0.0~rc1-1
- Update to 7.0.0rc1
- Fixes: rhbz#2029764

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 15 2021 Charalampos Stratakis <cstratak@redhat.com> - 6.2.5-1
- Update to 6.2.5
- Fixes: rhbz#1999270

* Fri Aug 27 2021 Miro Hrončok <mhroncok@redhat.com> - 6.2.4-7
- Enable all tests during package build

* Fri Aug 27 2021 Miro Hrončok <mhroncok@redhat.com> - 6.2.4-6
- Allow pluggy >=1.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Miro Hrončok <mhroncok@redhat.com> - 6.2.4-4
- Adjust pytest's own tests for changes in Python 3.10.0b4

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 6.2.4-3
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 6.2.4-2
- Bootstrap for Python 3.10

* Tue May 04 2021 Miro Hrončok <mhroncok@redhat.com> - 6.2.4-1
- Update to 6.2.4
- Fixes: rhbz#1956942

* Mon Apr 12 2021 Miro Hrončok <mhroncok@redhat.com> - 6.2.3-1
- Update to 6.2.3
- Fixes: rhbz#1946061

* Wed Mar 10 2021 Miro Hrončok <mhroncok@redhat.com> - 6.2.2-2
- Drop redundant build dependency on wcwidth (unused since 6.0.0rc1)

* Wed Jan 27 2021 Miro Hrončok <mhroncok@redhat.com> - 6.2.2-1
- Update to 6.2.2
- Update the description
- Fixes: rhbz#1882935

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Miro Hrončok <mhroncok@redhat.com> - 6.0.2-2
- Workaround the bracketed-paste mode breaking tests with Bash 5.1+

* Sat Sep 12 2020 Thomas Moschny <thomas.moschny@gmx.de> - 6.0.2-1
- Update to 6.0.2.

* Thu Aug 06 2020 Miro Hrončok <mhroncok@redhat.com> - 6.0.1-1
- Update to 6.0.1 (#1862097)

* Tue Jul 28 2020 Miro Hrončok <mhroncok@redhat.com> - 6.0.0~rc1-1
- Update to 6.0.0rc1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun  5 2020 Thomas Moschny <thomas.moschny@gmx.de> - 5.4.3-1
- Update to 5.4.3.

* Fri May 29 2020 Miro Hrončok <mhroncok@redhat.com> - 5.4.2-1
- Update to 5.4.2 (#1707986)

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 4.6.10-3
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 4.6.10-2
- Bootstrap for Python 3.9

* Fri May 08 2020 Miro Hrončok <mhroncok@redhat.com> - 4.6.10-1
- Update to 4.6.10.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan  5 2020 Thomas Moschny <thomas.moschny@gmx.de> - 4.6.9-1
- Update to 4.6.9.

* Fri Jan  3 2020 Thomas Moschny <thomas.moschny@gmx.de> - 4.6.8-1
- Update to 4.6.8.

* Fri Dec 06 2019 Miro Hrončok <mhroncok@redhat.com> - 4.6.7-1
- Update to 4.6.7

* Fri Oct 25 2019 Thomas Moschny <thomas.moschny@gmx.de> - 4.6.6-1
- Update to 4.6.6.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.6.5-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 4.6.5-3
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 4.6.5-2
- Bootstrap for Python 3.8

* Wed Aug 14 2019 Thomas Moschny <thomas.moschny@gmx.de> - 4.6.5-1
- Update to 4.6.5.
- Add missing BR on make.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Miro Hrončok <mhroncok@redhat.com> - 4.6.4-2
- Fix a bad conflict

* Mon Jul 01 2019 Miro Hrončok <mhroncok@redhat.com> - 4.6.4-1
- Update to 4.6.4, move python2-pytest to its own source package
- Make /usr/bin/pytest and /usr/bin/py.test Python 3

* Fri Jun 21 2019 Petr Viktorin <pviktori@redhat.com> - 4.4.1-2
- Remove optional test dependencies for Python 2 entirely

* Tue Apr 16 2019 Thomas Moschny <thomas.moschny@gmx.de> - 4.4.1-1
- Update to 4.4.1 (see PR#9).
- Remove test dependencies on python2-hypothesis and python2-twisted (see PR#10).

* Sat Mar 16 2019 Miro Hrončok <mhroncok@redhat.com> - 4.3.1-1
- Update to 4.3.1

* Tue Mar 12 2019 Miro Hrončok <mhroncok@redhat.com> - 4.3.0-1
- Update to 4.3.0 and fix FTBFS (#1671167, #1687384)

* Mon Feb 18 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.9.3-3
- Enable python dependency generator

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 31 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.9.3-1
- Update to 3.9.3.

* Tue Oct 23 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.9.2-1
- Update to 3.9.2.

* Wed Oct 17 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.9.1-1
- Update to 3.9.1.

* Tue Oct 16 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.8.2-3
- Add python2-pathlib2 runtime requirement (rhbz#1639718).

* Tue Oct 16 2018 Nils Philippsen <nils@redhat.com> - 3.8.2-2
- versionize pluggy dependencies

* Tue Oct 16 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.8.2-1
- Update to 3.8.2.

* Sat Sep 29 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.6.4-1
- Update to 3.6.4.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul  5 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.6.3-1
- Update to 3.6.3.

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.2-3
- Enable timeout

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.2-2
- Rebuilt for Python 3.7 (without timeout)

* Thu Jun 28 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.6.2-1
- Update to 3.6.2.

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.1-3
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.1-2
- Bootstrap for Python 3.7

* Tue Jun  5 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.6.1-1
- Update to 3.6.1.

* Mon May 28 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.0-1
- Update to 3.6.0 (#1581692)
- Require and BuildRequire atomicwrites

* Sat May 19 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.5.1-1
- Update to 3.5.1.
- Build the documentation with Python3.
- Update requirements.

* Thu Mar 15 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.4.2-2
- Add Requires for required modules

* Wed Mar 14 2018 Charalampos Stratakis <cstratak@redhat.com> - 3.4.2-1
- Update to 3.4.2

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.2.3-3
- Use better Obsoletes for platform-python

* Fri Nov 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.2.3-2
- Remove platform-python subpackage
- Cleanup conditionals

* Sat Oct  7 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.2.3-1
- Update to 3.2.3.

* Sat Sep  9 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.2.2-1
- Update to 3.2.2.
- Move BRs to their respective subpackages.
- Enable the platform-python subpackage only on F27+.

* Thu Aug 24 2017 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-3
- Rebuilt for rhbz#1484607

* Fri Aug 11 2017 Petr Viktorin <pviktori@redhat.com> - 3.2.1-2
- Add subpackage for platform-python (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Wed Aug  9 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.2.1-1
- Update to 3.2.1.

* Wed Aug 02 2017 Gwyn Ciesla <limburgher@gmail.com> - 3.2.0-1
- 3.2.0.

* Sun Jul 30 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.1.3-1
- Update to 3.1.3.
- Update BRs.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun  3 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.1.1-1
- Update to 3.1.1.
- Add BR on setuptools_scm.

* Wed Mar 15 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.7-1
- Update to 3.0.7.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 29 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.6-1
- Update to 3.0.6.
- Drop patch applied upstream.

* Tue Dec 13 2016 Miro Hrončok <mhroncok@redhat.com> - 3.0.5-2
- Rebuild for Python 3.6

* Tue Dec  6 2016 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.5-1
- Update to 3.0.5.

* Mon Nov 28 2016 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.4-1
- Update to 3.0.4.

* Fri Sep 30 2016 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.3-1
- Update to 3.0.3.
- Update requirements.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jun  3 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.9.2-1
- Update to 2.9.2.

* Tue May 31 2016 Nils Philippsen <nils@redhat.com>
- fix source URL

* Sat Apr  9 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.9.1-1
- Update to 2.9.1.
- Packaging updates.

* Tue Feb 2 2016 Orion Poplawski <orion@cora.nwra.com> - 2.8.7-2
- Use new python macros
- Fix python3 package file ownership

* Sun Jan 24 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.8.7-1
- Update to 2.8.7.

* Fri Jan 22 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.8.6-1
- Update to 2.8.6.

* Wed Dec 30 2015 Orion Poplawski <orion@cora.nwra.com> - 2.8.5-1
- Update to 2.8.5

* Wed Dec 30 2015 Orion Poplawski <orion@cora.nwra.com> - 2.8.2-3
- Re-enable pexpect in tests

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Oct 20 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.8.2-1
- Update to 2.8.2.

* Mon Oct 12 2015 Robert Kuska <rkuska@redhat.com> - 2.7.3-2
- Rebuilt for Python3.5 rebuild

* Thu Sep 17 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.3-1
- Update to 2.7.3.
- Provide additional symlinks to the pytest executables (rhbz#1249891).

* Mon Sep 14 2015 Orion Poplawski <orion@cora.nwra.com> - 2.7.2-2
- Provide python2-pytest, use python_provide macro

* Thu Jun 25 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.2-1
- Update to 2.7.2.
- Small fixes.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 23 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.1-1
- Update to 2.7.1.

* Mon Apr 20 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.0-1
- Update to 2.7.0.
- Apply updated Python packaging guidelines.
- Mark LICENSE with %%license.

* Tue Dec  2 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.4-1
- Update to 2.6.4.

* Sat Oct 11 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.3-1
- Update to 2.6.3.

* Fri Aug  8 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.1-1
- Update to 2.6.1.

* Fri Aug  1 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.0-1
- Update to 2.6.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Dennis Gilmore <dennis@ausil.us> - 2.5.2-2
- Redbuild for python 3.4

* Fri Apr 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.2-1
- Update to 2.5.2.

* Mon Oct  7 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.2-2
- Only run tests from the 'testing' subdir in %%check.

* Sat Oct  5 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.2-1
- Update to 2.4.2.
- Add buildroot's bindir to PATH while running the testsuite.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-3
- Disable tests using pexpect for now, fails on F19.

* Wed Jun 12 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-2
- Use python-sphinx for rhel > 6 (rhbz#973318).
- Update BR to use python-pexpect instead of pexpect.

* Sat May 25 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-1
- Update to 2.3.5.
- Docutils needed now to build README.html.
- Add some BR optionally used by the testsuite.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.4-1
- Update to 2.3.4.

* Sun Oct 28 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.2-1
- Update to 2.3.2.

* Sun Oct 21 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.1-1
- Update to 2.3.1.
- Re-enable some tests, ignore others.
- Docs are available in English and Japanese now.

* Thu Oct 11 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.4-4
- Add conditional for sphinx on rhel.
- Remove rhel logic from with_python3 conditional.
- Disable failing tests for Python3.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.4-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.4-1
- Update to 2.2.4.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.3-1
- Update to 2.2.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.1-1
- Update to 2.2.1.

* Tue Dec 13 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.0-1
- Update to 2.2.0.

* Wed Oct 26 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.3-1
- Update to 2.1.3.

* Tue Sep 27 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.2-1
- Update to 2.1.2.

* Sat Sep  3 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-2
- Fix: python3 dependencies.

* Sun Aug 28 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-1
- Update to 2.1.1.

* Thu Aug 11 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-2
- Update Requires and BuildRequires tags.

* Tue Aug  9 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-1
- Update to 2.1.0.

* Mon May 30 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.3-1
- Update to 2.0.3.

* Thu Mar 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.2-1
- Update to 2.0.2.

* Sun Jan 16 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.0-1
- New package.

## END: Generated by rpmautospec
