## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 17;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname setuptools

# used when bootstrapping new Python versions
%bcond bootstrap 0

# The original RHEL N+1 content set is defined by (build)dependencies
# of the packages in Fedora ELN. Hence we disable tests and documentation here
# to prevent pulling many unwanted packages in.
%bcond tests %[%{without bootstrap} && %{defined fedora}]

%global python_wheel_name %{srcname}-%{version}-py3-none-any.whl

Name:           python-setuptools
# When updating, update the bundled libraries versions bellow!
Version:        78.1.1
Release:        %autorelease
Summary:        Easily build and distribute Python packages
# setuptools is MIT
# autocommand is LGPL-3.0-only
# backports-tarfile is MIT
# importlib-metadata is Apache-2.0
# inflect is MIT
# jaraco-context is MIT
# jaraco-collections is MIT
# jaraco-functools is MIT
# jaraco-text is MIT
# more-itertools is MIT
# packaging is BSD-2-Clause OR Apache-2.0
# platformdirs is MIT
# tomli is MIT
# typeguard is MIT
# typing-extensions is Python-2.0.1
# wheel is MIT
# zipp is MIT
# the setuptools logo is MIT
License:        MIT AND Apache-2.0 AND (BSD-2-Clause OR Apache-2.0) AND Python-2.0.1 AND LGPL-3.0-only
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %{pypi_source %{srcname} %{version}}

# Some test deps are optional and either not desired or not available in Fedora, thus this patch removes them.
Patch:          Remove-optional-or-unpackaged-test-deps.patch

# The `setup.py install` deprecation notice might be confusing for RPM packagers
# adjust it, but only when $RPM_BUILD_ROOT is set
Patch:          Adjust-the-setup.py-install-deprecation-message.patch

# setuptools rewrites all shebangs to "#!python" which breaks workflows
# where no external installers (usually rewriting this) are involved.
# https://github.com/pypa/setuptools/issues/4883
# - Resolution: deprecated functionality won't be fixed.
# brp-mangle-shebang script cannot mangle this and fails for many pkgs.
Patch:          Revert-Always-rewrite-a-Python-shebang-to-python.patch

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel

%if %{with bootstrap}
BuildRequires:  unzip
%endif

%if %{with tests}
BuildRequires:  gcc
%endif

# python3 bootstrap: this is built before the final build of python3, which
# adds the dependency on python3-rpm-generators, so we require it manually
# The minimal version is for bundled provides verification script to accept multiple files as input
BuildRequires:  python3-rpm-generators >= 12-8
# we also use %%{_pyproject_wheeldir}, so an explicit requirement on the pyproject-macros is needed
BuildRequires:  pyproject-rpm-macros

%if %{without bootstrap}
# Not to use the pre-generated egg-info, we use setuptools from previous build to generate it
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif

%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.

# Virtual provides for the packages bundled by setuptools.
# Bundled packages are defined in multiple files. Generate the list with:
# pip freeze --path setuptools/_vendor > vendored.txt
# %%{_rpmconfigdir}/pythonbundles.py --namespace 'python%%{python3_pkgversion}dist' vendored.txt
%global bundled %{expand:
Provides: bundled(python%{python3_pkgversion}dist(autocommand)) = 2.2.2
Provides: bundled(python%{python3_pkgversion}dist(backports-tarfile)) = 1.2
Provides: bundled(python%{python3_pkgversion}dist(importlib-metadata)) = 8
Provides: bundled(python%{python3_pkgversion}dist(inflect)) = 7.3.1
Provides: bundled(python%{python3_pkgversion}dist(jaraco-collections)) = 5.1
Provides: bundled(python%{python3_pkgversion}dist(jaraco-context)) = 5.3
Provides: bundled(python%{python3_pkgversion}dist(jaraco-functools)) = 4.0.1
Provides: bundled(python%{python3_pkgversion}dist(jaraco-text)) = 3.12.1
Provides: bundled(python%{python3_pkgversion}dist(more-itertools)) = 10.3
Provides: bundled(python%{python3_pkgversion}dist(packaging)) = 24.2
Provides: bundled(python%{python3_pkgversion}dist(platformdirs)) = 4.2.2
Provides: bundled(python%{python3_pkgversion}dist(tomli)) = 2.0.1
Provides: bundled(python%{python3_pkgversion}dist(typeguard)) = 4.3
Provides: bundled(python%{python3_pkgversion}dist(typing-extensions)) = 4.12.2
Provides: bundled(python%{python3_pkgversion}dist(wheel)) = 0.45.1
Provides: bundled(python%{python3_pkgversion}dist(zipp)) = 3.19.2
}

%package -n python%{python3_pkgversion}-setuptools
Summary:        Easily build and distribute Python 3 packages
%{bundled}

# For users who might see ModuleNotFoundError: No module named 'pkg_resoureces'
# NB: Those are two different provides: one contains underscore, the other hyphen
%py_provides    python%{python3_pkgversion}-pkg_resources
%py_provides    python%{python3_pkgversion}-pkg-resources

%description -n python%{python3_pkgversion}-setuptools
Setuptools is a collection of enhancements to the Python 3 distutils that allow
you to more easily build and distribute Python 3 packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.


%package -n     %{python_wheel_pkg_prefix}-%{srcname}-wheel
Summary:        The setuptools wheel
%{bundled}

%description -n %{python_wheel_pkg_prefix}-%{srcname}-wheel
A Python wheel of setuptools to use with venv.


%prep
%autosetup -p1 -n %{srcname}-%{version}
%if %{without bootstrap}
# If we don't have setuptools installed yet, we use the pre-generated .egg-info
# See https://github.com/pypa/setuptools/pull/2543
# And https://github.com/pypa/setuptools/issues/2550
# WARNING: We cannot remove this folder since Python 3.11.1,
#          see https://github.com/pypa/setuptools/issues/3761
#rm -r %%{srcname}.egg-info
%endif

# Strip shbang
find setuptools pkg_resources -name \*.py | xargs sed -i -e '1 {/^#!\//d}'
# Remove bundled exes
rm -f setuptools/*.exe
# Don't ship these
rm -r docs/conf.py

%if %{without bootstrap}
%generate_buildrequires
%pyproject_buildrequires -r %{?with_tests:-x test}
%endif

%build
%if %{with bootstrap}
%{python3} setup.py bdist_wheel
mkdir -p %{_pyproject_wheeldir}
mv dist/%{python_wheel_name} %{_pyproject_wheeldir}
%else
%pyproject_wheel
%endif


%install
%if %{with bootstrap}
mkdir -p %{buildroot}%{python3_sitelib}
unzip %{_pyproject_wheeldir}/%{python_wheel_name} -d %{buildroot}%{python3_sitelib} -x setuptools-%{version}.dist-info/RECORD
echo rpm > %{buildroot}%{python3_sitelib}/setuptools-%{version}.dist-info/INSTALLER
%else
%pyproject_install
%pyproject_save_files -l setuptools pkg_resources _distutils_hack
sed -Ei '/\/tests\b/d' %{pyproject_files}
%endif

# https://github.com/pypa/setuptools/issues/2709
find %{buildroot}%{python3_sitelib} -name tests -print0 | xargs -0 rm -r

# Install the wheel for the python-setuptools-wheel package
# and inject SBOM into it (if the macro is available)
mkdir -p %{buildroot}%{python_wheel_dir}
install -p %{_pyproject_wheeldir}/%{python_wheel_name} -t %{buildroot}%{python_wheel_dir}
%{?python_wheel_inject_sbom:%python_wheel_inject_sbom %{buildroot}%{python_wheel_dir}/%{python_wheel_name}}


%check
%if %{without bootstrap}
# Verify bundled provides are up to date
%{python3} -m pip freeze --path setuptools/_vendor > vendored.txt
%{_rpmconfigdir}/pythonbundles.py vendored.txt --namespace 'python%{python3_pkgversion}dist' --compare-with '%{bundled}'

# Regression test, the wheel should not be larger than 1300 kB
# https://bugzilla.redhat.com/show_bug.cgi?id=1914481#c3
test $(stat --format %%s %{_pyproject_wheeldir}/%{python_wheel_name}) -lt 1300000

%pyproject_check_import -e '*.tests' -e '*.tests.*'
%endif

# Regression test, the tests are not supposed to be installed
test ! -d %{buildroot}%{python3_sitelib}/pkg_resources/tests
test ! -d %{buildroot}%{python3_sitelib}/setuptools/tests
test ! -d %{buildroot}%{python3_sitelib}/setuptools/_distutils/tests

%if %{with tests}
# Upstream tests
# --ignore=setuptools/tests/integration/
# --ignore=setuptools/tests/config/test_apply_pyprojecttoml.py
# -k "not test_pip_upgrade_from_source and not test_equivalent_output"
#   the tests require internet connection
# --ignore=setuptools/tests/test_editable_install.py
#   the tests require pip-run which we don't have in Fedora
# -k "not test_wheel_includes_cli_scripts"
#   the test expects removed .exe files to be installed
# --ignore=tools
#   the tests test various upstream release tools we don't use/ship
PRE_BUILT_SETUPTOOLS_WHEEL=%{_pyproject_wheeldir}/%{python_wheel_name} \
PYTHONPATH=$(pwd) %pytest \
 --ignore=setuptools/tests/integration/ \
 --ignore=setuptools/tests/test_editable_install.py \
 --ignore=setuptools/tests/config/test_apply_pyprojecttoml.py \
 --ignore=tools \
 -k "not test_pip_upgrade_from_source and not test_wheel_includes_cli_scripts and not test_equivalent_output"
%endif # with tests


%files -n python%{python3_pkgversion}-setuptools %{?!with_bootstrap:-f %{pyproject_files}}
%doc docs/* NEWS.rst README.rst
%{python3_sitelib}/distutils-precedence.pth
%if %{with bootstrap}
%{python3_sitelib}/setuptools-%{version}.dist-info/
%license %{python3_sitelib}/setuptools-%{version}.dist-info/licenses/LICENSE
%{python3_sitelib}/pkg_resources/
%{python3_sitelib}/setuptools/
%{python3_sitelib}/_distutils_hack/
%endif

%files -n %{python_wheel_pkg_prefix}-%{srcname}-wheel
%license LICENSE
# we own the dir for simplicity
%dir %{python_wheel_dir}/
%{python_wheel_dir}/%{python_wheel_name}


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 78.1.1-17
- Latest state for python-setuptools

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 78.1.1-15
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 29 2025 Miro Hrončok <miro@hroncok.cz> - 78.1.1-13
- Include SBOM in the .whl file in python-setuptools-wheel

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 78.1.1-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 78.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 78.1.1-7
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 78.1.1-6
- Bootstrap for Python 3.14

* Mon May 12 2025 Miro Hrončok <miro@hroncok.cz> - 78.1.1-5
- Only install the LICENSE file once

* Thu Apr 24 2025 Tomáš Hrnčiar <thrnciar@redhat.com> - 78.1.1-1
- Update to 78.1.1 (rhbz#2361175)

* Thu Apr 03 2025 Lumir Balhar <lbalhar@redhat.com> - 78.1.0-1
- Update to 78.1.0

* Tue Mar 18 2025 Lumir Balhar <lbalhar@redhat.com> - 76.1.0-1
- Update to 76.1.0 (rhbz#2274761)

* Tue Mar 18 2025 Lumir Balhar <lbalhar@redhat.com> - 74.1.3-6
- Remove Python 3.8 (retired in F42) from CI config

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 74.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 11 2024 Lumir Balhar <lbalhar@redhat.com> - 74.1.3-4
- Fix compatibility of one test with packaging 24.2

* Thu Nov 07 2024 Miroslav Suchý <msuchy@redhat.com> - 74.1.3-3
- Correct SPDX license formula

* Tue Oct 15 2024 Miro Hrončok <miro@hroncok.cz> - 74.1.3-1
- Update to 74.1.3

* Tue Oct 15 2024 Miro Hrončok <miro@hroncok.cz> - 74.1.2-1
- Update to 74.1.2

* Tue Oct 15 2024 Miro Hrončok <miro@hroncok.cz> - 74.1.0-1
- Update to 74.1.0
- The `setup.py test` command no longer works
- The License now includes LGPL-3.0 (bundled python3dist(autocommand))

* Wed Aug 07 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 69.2.0-9
- Add a simple smoke test

* Fri Jul 26 2024 Lumir Balhar <lbalhar@redhat.com> - 69.2.0-8
- Security fix for CVE-2024-6345

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 69.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 69.2.0-6
- Rebuilt for Python 3.13

* Thu Jun 06 2024 Python Maint <python-maint@redhat.com> - 69.2.0-5
- Bootstrap for Python 3.13

* Thu Jun 06 2024 Python Maint <python-maint@redhat.com> - 69.2.0-4
- Bootstrap for Python 3.13

* Tue May 14 2024 Miro Hrončok <miro@hroncok.cz> - 69.2.0-3
- Python 3.13 compatibility patches
- Fixes: rhbz#2259516

* Thu May 02 2024 Karolina Surma <ksurma@redhat.com> - 69.2.0-2
- Remove mypy from test dependencies

* Mon Mar 18 2024 Charalampos Stratakis <cstratak@redhat.com> - 69.2.0-1
- Update to 69.2.0
- Resolves: rhbz#2269358

* Fri Mar 08 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 69.1.1-1
- Update to 69.1.1

* Tue Feb 06 2024 Miro Hrončok <miro@hroncok.cz> - 69.0.3-3
- Undo the removal of pkg_resources DeprecationWarning

* Tue Feb 06 2024 Karolina Surma <ksurma@redhat.com> - 69.0.3-1
- Update to 69.0.3

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 68.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 68.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Lumír Balhar <lbalhar@redhat.com> - 68.2.2-1
- Update to 68.2.2 (rhbz#2208644)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 67.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Python Maint <python-maint@redhat.com> - 67.7.2-6
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 67.7.2-5
- Bootstrap for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 67.7.2-4
- Bootstrap for Python 3.12

* Fri May 05 2023 Miro Hrončok <mhroncok@redhat.com> - 67.7.2-2
- Adjust the `setup.py install` deprecation notice when building RPM packages

* Fri Apr 21 2023 Charalampos Stratakis <cstratak@redhat.com> - 67.7.2-1
- Update to 67.7.2
- Fixes: rhbz#2144132

* Thu Apr 20 2023 Charalampos Stratakis <cstratak@redhat.com> - 67.6.1-1
- Update to 67.6.1
- Fixes: rhbz#2144132

* Tue Mar 28 2023 Miro Hrončok <mhroncok@redhat.com> - 65.5.1-3
- Fix tests with wheel 0.40

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 65.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 08 2022 Miro Hrončok <mhroncok@redhat.com> - 65.5.1-1
- Update to 65.5.1
- Fixes: rhbz#2140209

* Fri Oct 14 2022 Miro Hrončok <mhroncok@redhat.com> - 65.5.0-1
- Update to 65.5.0
- Fixes: rhbz#2129562

* Thu Oct 13 2022 Miro Hrončok <mhroncok@redhat.com> - 65.4.1-1
- Update to 65.4.1
- Update the RPM License field to use SPDX expressions

* Tue Sep 13 2022 Lumír Balhar <lbalhar@redhat.com> - 65.3.0-1
- Update to 65.3.0
Resolves: rhbz#2102402

* Thu Jul 28 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 65.0.2-1
- Update to 65.0.2
- Fixes: rhbz#2102402

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 62.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Charalampos Stratakis <cstratak@redhat.com> - 62.6.0-1
- Update to 62.6.0
- Fixes: rhbz#2064842

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 60.9.3-5
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 60.9.3-4
- Bootstrap for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 60.9.3-3
- Bootstrap for Python 3.11

* Tue Apr 19 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 60.9.3-2
- No longer use the deprecated sre_constants module in bundled pyparsing
- Fixes: rhbz#2075487

* Wed Feb 16 2022 Karolina Surma <ksurma@redhat.com> - 60.9.3-1
- Update to 60.9.3
- Fixes rhbz#2033860

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 59.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 08 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 59.6.0-1
- Update to 59.6.0
- Fixes: rhbz#2023119
- Fixes: rhbz#2031556

* Wed Nov 10 2021 Karolina Surma <ksurma@redhat.com> - 58.5.3-1
- Update to 58.5.3
- Fixes rhbz#2016715

* Tue Oct 19 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 58.2.0-1
- Update to 58.2.0
- Fixes rhbz#2001228

* Tue Aug 03 2021 Miro Hrončok <mhroncok@redhat.com> - 57.4.0-1
- Update to 57.4.0
- https://setuptools.readthedocs.io/en/latest/history.html#v57-4-0
- Fixes rhbz#1982493

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 57.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Miro Hrončok <mhroncok@redhat.com> - 57.1.0-2
- Modernize packaging

* Fri Jul 09 2021 Tomas Hrnciar <thrnciar@redhat.com> - 57.1.0-1
- Update to 57.1.0
- Fixes rhbz#1979122

* Thu Jun 17 2021 Lumír Balhar <lbalhar@redhat.com> - 57.0.0-1
- Update to 57.0.0
Resolves: rhbz#1963411

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 56.2.0-4
- Rebuilt for Python 3.10

* Tue Jun 01 2021 Python Maint <python-maint@redhat.com> - 56.2.0-3
- Bootstrap for Python 3.10

* Tue Jun 01 2021 Python Maint <python-maint@redhat.com> - 56.2.0-2
- Bootstrap for Python 3.10

* Mon May 17 2021 Miro Hrončok <mhroncok@redhat.com> - 56.2.0-1
- Update to 56.2.0
- Fixes rhbz#1958677

* Thu May 06 2021 Tomas Hrnciar <thrnciar@redhat.com> - 56.1.0-1
- Update to 56.1.0

* Thu Apr 22 2021 Miro Hrončok <mhroncok@redhat.com> - 56.0.0-2
- Provide python3-pkg_resources
- Provide python3-pkg-resources

* Fri Apr 09 2021 Tomas Hrnciar <thrnciar@redhat.com> - 56.0.0-1
- Update to 56.0.0

* Tue Mar 16 2021 Tomas Hrnciar <thrnciar@redhat.com> - 54.1.2-1
- Update to 54.1.2

* Tue Feb 02 2021 Miro Hrončok <mhroncok@redhat.com> - 53.0.0-1
- Update to 53.0.0
- https://setuptools.readthedocs.io/en/latest/history.html#v53-0-0
- Fixes: rhbz#1923249

* Tue Jan 26 2021 Lumír Balhar <lbalhar@redhat.com> - 52.0.0-1
- Update to 52.0.0 (#1917060)
- Removes easy_install module and executable

* Mon Jan 11 2021 Miro Hrončok <mhroncok@redhat.com> - 51.1.2-1
- Update to 51.1.2
- Removes tests from the wheel
- https://setuptools.readthedocs.io/en/latest/history.html#v51-1-2
- Fixes: rhbz#1914481

* Tue Dec 29 2020 Miro Hrončok <mhroncok@redhat.com> - 51.1.1-1
- Update to 51.1.1
- Fixes test failures with pip 20.3 as well as with pytest 6.2+
- Fixes: rhbz#1909575

* Fri Dec  4 2020 Miro Hrončok <mhroncok@redhat.com> - 50.3.2-2
- Disable tests in Fedora ELN (and RHEL)

* Tue Oct 20 2020 Tomas Hrnciar <thrnciar@redhat.com> - 50.3.2-1
- Update to 50.3.2 (#1889093)

* Fri Sep 04 2020 Tomas Hrnciar <thrnciar@redhat.com> - 50.1.0-1
- Update to 50.1.0 (#1873889)

* Fri Aug 21 2020 Petr Viktorin <pviktori@redhat.com> - 49.6.0-1
- Update to 49.6.0 (#1862791)

* Wed Jul 29 2020 Miro Hrončok <mhroncok@redhat.com> - 49.1.3-1
- Update to 49.1.3 (#1853597)
- https://setuptools.readthedocs.io/en/latest/history.html#v49-1-3

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 47.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Miro Hrončok <mhroncok@redhat.com> - 47.3.1-1
- Update to 47.3.1 (#1847049)
- https://setuptools.readthedocs.io/en/latest/history.html#v47-3-1

* Mon Jun 01 2020 Charalampos Stratakis <cstratak@redhat.com> - 47.1.1-1
- Update to 47.1.1 (#1841123)
- https://setuptools.readthedocs.io/en/latest/history.html#v47-1-1

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 46.4.0-4
- Rebuilt for Python 3.9

* Thu May 21 2020 Miro Hrončok <mhroncok@redhat.com> - 46.4.0-3
- Bootstrap for Python 3.9

* Thu May 21 2020 Miro Hrončok <mhroncok@redhat.com> - 46.4.0-2
- Bootstrap for Python 3.9

* Mon May 18 2020 Tomas Hrnciar <thrnciar@redhat.com> - 46.4.0-1
- Update to 46.4.0 (#1835411)
- https://setuptools.readthedocs.io/en/latest/history.html#v46-4-0

* Tue May 12 2020 Tomas Hrnciar <thrnciar@redhat.com> - 46.2.0-1
- Update to 46.2.0 (#1833826)
- https://setuptools.readthedocs.io/en/latest/history.html#v46-2-0

* Thu Mar 26 2020 Miro Hrončok <mhroncok@redhat.com> - 46.1.3-1
- Upgrade to 46.1.3 (#1817189)
- https://setuptools.readthedocs.io/en/latest/history.html#v46-1-3

* Tue Mar 10 2020 Miro Hrončok <mhroncok@redhat.com> - 46.0.0-1
- Upgrade to 46.0.0 (#1811340)
- https://setuptools.readthedocs.io/en/latest/history.html#v46-0-0

* Tue Feb 11 2020 Miro Hrončok <mhroncok@redhat.com> - 45.2.0-1
- Upgrade to 45.2.0 (#1775943)
- https://setuptools.readthedocs.io/en/latest/history.html#v45-2-0
- No longer supports Python 2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 41.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 04 2019 Tomas Orsava <torsava@redhat.com> - 41.6.0-1
- Upgrade to 41.6.0 (#1758945).
- https://setuptools.readthedocs.io/en/latest/history.html#v41-6-0
- Disabled a failing upstream test: https://github.com/pypa/setuptools/issues/1896

* Tue Sep 03 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 41.2.0-1
- Upgrade to 41.2.0 (#1742718).
- https://setuptools.readthedocs.io/en/latest/history.html#v41-2-0

* Mon Aug 26 2019 Miro Hrončok <mhroncok@redhat.com> - 41.0.1-9
- Move python2-setuptools to a separate package

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 41.0.1-8
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 41.0.1-7
- Bootstrap for Python 3.8

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 41.0.1-6
- Provide pythonXdist(setuptools) when bootstrapping

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 41.0.1-5
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 41.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Miro Hrončok <mhroncok@redhat.com> - 41.0.1-3
- Make /usr/bin/easy_install Python 3
- Drop obsoleted Obsoletes

* Fri Jun 21 2019 Petr Viktorin <pviktori@redhat.com> - 41.0.1-2
- Remove optional test dependencies for Python 2
- Skip test_virtualenv on Python 2

* Thu Apr 25 2019 Miro Hrončok <mhroncok@redhat.com> - 41.0.1-1
- Update to 41.0.1 (#1695846)
- https://github.com/pypa/setuptools/blob/v41.0.1/CHANGES.rst

* Tue Feb 05 2019 Miro Hrončok <mhroncok@redhat.com> - 40.8.0-1
- Update to 40.8.0 (#1672756)
- https://github.com/pypa/setuptools/blob/v40.8.0/CHANGES.rst

* Sun Feb 03 2019 Miro Hrončok <mhroncok@redhat.com> - 40.7.3-1
- Hotfix update to 40.7.3 (#1672084)
- https://github.com/pypa/setuptools/blob/v40.7.3/CHANGES.rst

* Sat Feb 02 2019 Miro Hrončok <mhroncok@redhat.com> - 40.7.2-1
- Hotfix update to 40.7.2 (#1671608)
- https://github.com/pypa/setuptools/blob/v40.7.2/CHANGES.rst

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 40.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Miro Hrončok <mhroncok@redhat.com> - 40.7.1-1
- Hotfix update to 40.7.1 (#1670243)
- https://github.com/pypa/setuptools/blob/v40.7.1/CHANGES.rst

* Mon Jan 28 2019 Miro Hrončok <mhroncok@redhat.com> - 40.7.0-1
- Update to 40.7.0 (#1669876)
- https://github.com/pypa/setuptools/blob/v40.7.0/CHANGES.rst

* Mon Sep 24 2018 Miro Hrončok <mhroncok@redhat.com> - 40.4.3-1
- Update to 40.4.3 to fix dire DeprecationWarnings (#1627071)
- List vendored libraries
- https://github.com/pypa/setuptools/blob/v40.4.3/CHANGES.rst

* Wed Sep 19 2018 Randy Barlow <bowlofeggs@fedoraproject.org> - 40.4.1-1
- Update to 40.4.1 (#1599307).
- https://github.com/pypa/setuptools/blob/v40.4.1/CHANGES.rst

* Wed Aug 15 2018 Petr Viktorin <pviktori@redhat.com> - 39.2.0-7
- Add a subpackage with wheels
- Remove the python3 bcond
- Remove macros for RHEL 6

* Thu Jul 19 2018 Miro Hrončok <mhroncok@redhat.com> - 39.2.0-6
- Create /usr/local/lib/pythonX.Y when needed (#1576924)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 39.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 39.2.0-4
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 39.2.0-3
- Bootstrap for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 39.2.0-2
- Bootstrap for Python 3.7

* Wed May 23 2018 Charalampos Stratakis <cstratak@redhat.com> - 39.2.0-1
- update to 39.2.0 Fixes bug #1572889

* Tue Mar 20 2018 Charalampos Stratakis <cstratak@redhat.com> - 39.0.1-1
- update to 39.0.1 Fixes bug #1531527

* Wed Mar 14 2018 Tomas Orsava <torsava@redhat.com> - 38.4.0-4
- Skip test_virtualenv due to broken executable detection

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 38.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Troy Dawson <tdawson@redhat.com> - 38.4.0-2
- Update conditional

* Tue Jan 16 2018 Charalampos Stratakis <cstratak@redhat.com> - 38.4.0-1
- update to 38.4.0 Fixes bug #1531527

* Tue Jan 02 2018 Charalampos Stratakis <cstratak@redhat.com> - 38.2.5-1
- update to 38.2.5 Fixes bug #1528968

* Tue Nov 21 2017 Miro Hrončok <mhroncok@redhat.com> - 37.0.0-1
- Update to 37.0.0 (fixes #1474126)
- Removed not needed pip3 patch (upstream included different version of fix)

* Tue Nov 21 2017 Miro Hrončok <mhroncok@redhat.com> - 36.5.0-1
- Update to 36.5.0 (related to #1474126)

* Thu Nov 09 2017 Tomas Orsava <torsava@redhat.com> - 36.2.0-8
- Remove the platform-python subpackage

* Sun Aug 20 2017 Tomas Orsava <torsava@redhat.com> - 36.2.0-7
- Re-enable tests to finish bootstrapping the platform-python stack
  (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Wed Aug 09 2017 Tomas Orsava <torsava@redhat.com> - 36.2.0-6
- Add the platform-python subpackage
- Disable tests so platform-python stack can be bootstrapped
  (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Wed Aug 09 2017 Tomas Orsava <torsava@redhat.com> - 36.2.0-5
- Add Patch 0 that fixes a test suite failure on Python 3 in absence of
  the Python 2 version of pip
- Move docs to their proper place

* Wed Aug 09 2017 Tomas Orsava <torsava@redhat.com> - 36.2.0-4
- Switch macros to bcond's and make Python 2 optional to facilitate building
  the Python 2 and Python 3 modules.

* Tue Aug 08 2017 Michal Cyprian <mcyprian@redhat.com> - 36.2.0-3
- Revert "Add --executable option to easy_install command"
  This enhancement is currently not needed and it can possibly
  collide with `pip --editable`option

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 36.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 15 2017 Charalampos Stratakis <cstratak@redhat.com> - 36.2.0-1
- update to 36.2.0. Fixes bug #1470908

* Thu Jun 15 2017 Charalampos Stratakis <cstratak@redhat.com> - 36.0.1-1
- update to 36.0.1. Fixes bug #1458093

* Sat May 27 2017 Kevin Fenzi <kevin@scrye.com> - 35.0.2-1
- update to 35.0.2. Fixes bug #1446622

* Sun Apr 23 2017 Kevin Fenzi <kevin@scrye.com> - 35.0.1-1
- Update to 35.0.1. Fixes bug #1440388

* Sat Mar 25 2017 Kevin Fenzi <kevin@scrye.com> - 34.3.2-1
- Update to 34.3.2. Fixes bug #1428818

* Sat Feb 25 2017 Kevin Fenzi <kevin@scrye.com> - 34.3.0-1
- Update to 34.3.0. Fixes bug #1426463

* Fri Feb 17 2017 Michal Cyprian <mcyprian@redhat.com> - 34.2.0-2
- Add --executable option to easy_install command

* Thu Feb 16 2017 Charalampos Stratakis <cstratak@redhat.com> - 34.2.0-1
- Update to 34.2.0. Fixes bug #1421676

* Sat Feb 04 2017 Kevin Fenzi <kevin@scrye.com> - 34.1.1-1
- Update to 34.1.1. Fixes bug #1412268
- Fix License tag. Fixes bug #1412268
- Add Requires for fomerly bundled projects: six, packaging appdirs

* Tue Jan 03 2017 Michal Cyprian <mcyprian@redhat.com> - 32.3.1-2
- Use python macros in build and install sections

* Thu Dec 29 2016 Kevin Fenzi <kevin@scrye.com> - 32.3.1-1
- Update to 32.3.1. Fixes bug #1409091

* Wed Dec 28 2016 Kevin Fenzi <kevin@scrye.com> - 32.3.0-1
- Update to 32.3.0. Fixes bug #1408564

* Fri Dec 23 2016 Kevin Fenzi <kevin@scrye.com> - 32.2.0-1
- Update to 32.2.0. Fixes bug #1400310

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 30.4.0-2
- Enable tests

* Sun Dec 11 2016 Kevin Fenzi <kevin@scrye.com> - 30.4.0-1
- Update to 30.4.0. Fixes bug #1400310

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 28.8.0-3
- Rebuild for Python 3.6 with wheel
- Disable tests

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 28.8.0-2
- Rebuild for Python 3.6 without wheel

* Wed Nov 09 2016 Kevin Fenzi <kevin@scrye.com> - 28.8.0-1
- Update to 28.8.1. Fixes bug #1392722

* Mon Oct 31 2016 Kevin Fenzi <kevin@scrye.com> - 28.7.1-1
- Update to 28.7.1. Fixes bug #1389917

* Tue Oct 25 2016 Kevin Fenzi <kevin@scrye.com> - 28.6.1-1
- Update to 28.6.1. Fixes bug #1387071

* Tue Oct 18 2016 Kevin Fenzi <kevin@scrye.com> - 28.6.0-1
- Update to 28.6.0. Fixes bug #1385655

* Sat Oct 08 2016 Kevin Fenzi <kevin@scrye.com> - 28.3.0-1
- Update to 28.3.0. Fixes bug #1382971

* Sun Oct 02 2016 Kevin Fenzi <kevin@scrye.com> - 28.2.0-1
- Update to 28.2.0. Fixes bug #1381099

* Sun Oct 02 2016 Kevin Fenzi <kevin@scrye.com> - 28.1.0-1
- Update to 28.1.0. Fixes bug #1381066

* Wed Sep 28 2016 Kevin Fenzi <kevin@scrye.com> - 28.0.0-1
- Update to 28.0.0. Fixes bug #1380073

* Sun Sep 25 2016 Kevin Fenzi <kevin@scrye.com> - 27.3.0-1
- Update to 27.3.0. Fixes bug #1378067

* Sat Sep 17 2016 Kevin Fenzi <kevin@scrye.com> - 27.2.0-1
- Update to 27.2.0. Fixes bug #1376298

* Sat Sep 10 2016 Kevin Fenzi <kevin@scrye.com> - 27.1.2-1
- Update to 27.1.2. Fixes bug #1370777

* Sat Aug 27 2016 Kevin Fenzi <kevin@scrye.com> - 26.0.0-1
- Update to 26.0.0. Fixes bug #1370777

* Wed Aug 10 2016 Kevin Fenzi <kevin@scrye.com> - 25.1.6-1
- Update to 25.1.6. Fixes bug #1362325

* Fri Jul 29 2016 Kevin Fenzi <kevin@scrye.com> - 25.1.1-1
- Update to 25.1.1. Fixes bug #1361465

* Thu Jul 28 2016 Kevin Fenzi <kevin@scrye.com> - 25.1.0-1
- Update to 25.1.0

* Sat Jul 23 2016 Kevin Fenzi <kevin@scrye.com> - 25.0.0-1
- Update to 25.0.0

* Fri Jul 22 2016 Kevin Fenzi <kevin@scrye.com> - 24.2.0-1
- Update to 24.2.0. Fixes bug #1352734

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 24.0.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 04 2016 Kevin Fenzi <kevin@scrye.com> - 24.0.1-1
- Update to 24.0.1. Fixes bug #1352532

* Wed Jun 15 2016 Kevin Fenzi <kevin@scrye.com> - 23.0.0-1
- Update to 23.0.0. Fixes bug #1346542

* Tue Jun 07 2016 Kevin Fenzi <kevin@scrye.com> - 22.0.5-1
- Update to 22.0.5. Fixes bug #1342706

* Thu Jun 02 2016 Kevin Fenzi <kevin@scrye.com> - 20.0.0-1
- Upgrade to 22.0.0

* Tue May 31 2016 Nils Philippsen <nils@redhat.com>
- fix source URL

* Sun May 29 2016 Kevin Fenzi <kevin@scrye.com> - 21.2.2-1
- Update to 21.2.2. Fixes bug #1332357

* Thu Apr 28 2016 Kevin Fenzi <kevin@scrye.com> - 20.10.1-1
- Update to 20.10.1. Fixes bug #1330375

* Sat Apr 16 2016 Kevin Fenzi <kevin@scrye.com> - 20.9.0-1
- Update to 20.9.0. Fixes bug #1327827

* Fri Apr 15 2016 Kevin Fenzi <kevin@scrye.com> - 20.8.1-1
- Update to 20.8.1. Fixes bug #1325910

* Thu Mar 31 2016 Kevin Fenzi <kevin@scrye.com> - 20.6.7-1
- Update to 20.6.7. Fixes bug #1322836

* Wed Mar 30 2016 Kevin Fenzi <kevin@scrye.com> - 20.4-1
- Update to 20.4. Fixes bug #1319366

* Wed Mar 16 2016 Kevin Fenzi <kevin@scrye.com> - 20.3-1
- Update to 20.3. Fixes bug #1311967

* Sat Feb 27 2016 Kevin Fenzi <kevin@scrye.com> - 20.2.2-1
- Update to 20.2.2. Fixes bug #1311967

* Sat Feb 13 2016 Kevin Fenzi <kevin@scrye.com> - 20.1.1-1
- Update to 20.1.1. Fixes bug #130719

* Fri Feb 12 2016 Kevin Fenzi <kevin@scrye.com> - 20.1-1
- Update to 20.1. Fixes bug #1307000

* Mon Feb 08 2016 Kevin Fenzi <kevin@scrye.com> - 20.0-1
- Update to 20.0. Fixes bug #1305394

* Sat Feb 06 2016 Kevin Fenzi <kevin@scrye.com> - 19.7-1
- Update to 19.7. Fixes bug #1304563

* Wed Feb 3 2016 Orion Poplawski <orion@cora.nwra.com> - 19.6.2-2
- Fix python3 package file ownership

* Sun Jan 31 2016 Kevin Fenzi <kevin@scrye.com> - 19.6.2-1
- Update to 19.6.2. Fixes bug #1303397

* Mon Jan 25 2016 Kevin Fenzi <kevin@scrye.com> - 19.6-1
- Update to 19.6.

* Mon Jan 25 2016 Kevin Fenzi <kevin@scrye.com> - 19.5-1
- Update to 19.5. Fixes bug #1301313

* Mon Jan 18 2016 Kevin Fenzi <kevin@scrye.com> - 19.4-1
- Update to 19.4. Fixes bug #1299288

* Tue Jan 12 2016 Orion Poplawski <orion@cora.nwra.com> - 19.2-2
- Cleanup spec from python3-setuptools review

* Fri Jan 08 2016 Kevin Fenzi <kevin@scrye.com> - 19.2-1
- Update to 19.2. Fixes bug #1296755

* Fri Dec 18 2015 Kevin Fenzi <kevin@scrye.com> - 19.1.1-1
- Update to 19.1.1. Fixes bug #1292658

* Tue Dec 15 2015 Kevin Fenzi <kevin@scrye.com> - 18.8.1-1
- Update to 18.8.1. Fixes bug #1291678

* Sat Dec 12 2015 Kevin Fenzi <kevin@scrye.com> - 18.8-1
- Update to 18.8. Fixes bug #1290942

* Fri Dec 04 2015 Kevin Fenzi <kevin@scrye.com> - 18.7.1-1
- Update to 18.7.1. Fixes bug #1287372

* Wed Nov 25 2015 Kevin Fenzi <kevin@scrye.com> - 18.6.1-1
- Update to 18.6.1. Fixes bug #1270578

* Sun Nov 15 2015 Thomas Spura <tomspur@fedoraproject.org> - 18.5-3
- Try to disable zip_safe bug #1271776
- Add python2 subpackage

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 18.5-2
- Add patch so it is possible to set test_args variable

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 18.5-1
- Update to 18.5. Fixes bug #1270578

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.coM> - 18.4-1
- Update to 18.4. Fixes bug #1270578
- Build with wheel and check phase

* Wed Sep 23 2015 Robert Kuska <rkuska@redhat.com> - 18.3.2-2
- Python3.5 rebuild: rebuild without wheel and check phase

* Tue Sep 22 2015 Kevin Fenzi <kevin@scrye.com> 18.3.2-1
- Update to 18.3.2. Fixes bug #1264902

* Mon Sep 07 2015 Kevin Fenzi <kevin@scrye.com> 18.3.1-1
- Update to 18.3.1. Fixes bug #1256188

* Wed Aug 05 2015 Kevin Fenzi <kevin@scrye.com> 18.1-1
- Update to 18.1. Fixes bug #1249436

* Mon Jun 29 2015 Pierre-Yves Chibon <pingou@pingoured.fr> - 18.0.1-2
- Explicitely provide python2-setuptools

* Thu Jun 25 2015 Kevin Fenzi <kevin@scrye.com> 18.0.1-1
- Update to 18.0.1

* Sat Jun 20 2015 Kevin Fenzi <kevin@scrye.com> 17.1.1-3
- Drop no longer needed Requires/BuildRequires on python-backports-ssl_match_hostname
- Fixes bug #1231325

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Kevin Fenzi <kevin@scrye.com> 17.1.1-1
- Update to 17.1.1. Fixes bug 1229507

* Sun Jun 07 2015 Kevin Fenzi <kevin@scrye.com> 17.1-1
- Update to 17.1. Fixes bug 1229066

* Sat May 30 2015 Kevin Fenzi <kevin@scrye.com> 17.0-1
- Update to 17

* Mon May 18 2015 Kevin Fenzi <kevin@scrye.com> 16.0-1
- Update to 16

* Mon Apr 27 2015 Ralph Bean <rbean@redhat.com> - 15.2-1
- new version

* Sat Apr 04 2015 Ralph Bean <rbean@redhat.com> - 15.0-1
- new version

* Sun Mar 22 2015 Ralph Bean <rbean@redhat.com> - 14.3.1-1
- new version

* Sat Mar 21 2015 Ralph Bean <rbean@redhat.com> - 14.3.1-1
- new version

* Mon Mar 16 2015 Ralph Bean <rbean@redhat.com> - 14.3-1
- new version

* Sun Mar 15 2015 Ralph Bean <rbean@redhat.com> - 14.2-1
- new version

* Sun Mar 15 2015 Ralph Bean <rbean@redhat.com> - 14.1.1-1
- new version

* Fri Mar 06 2015 Ralph Bean <rbean@redhat.com> - 13.0.2-1
- new version

* Thu Mar 05 2015 Ralph Bean <rbean@redhat.com> - 12.4-1
- new version

* Fri Feb 27 2015 Ralph Bean <rbean@redhat.com> - 12.3-1
- new version

* Tue Jan 20 2015 Kevin Fenzi <kevin@scrye.com> 12.0.3-1
- Update to 12.0.3

* Fri Jan 09 2015 Slavek Kabrda <bkabrda@redhat.com> - 11.3.1-2
- Huge spec cleanup
- Make spec buildable on all Fedoras and RHEL 6 and 7
- Make tests actually run

* Wed Jan 07 2015 Kevin Fenzi <kevin@scrye.com> 11.3.1-1
- Update to 11.3.1. Fixes bugs: #1179393 and #1178817

* Sun Jan 04 2015 Kevin Fenzi <kevin@scrye.com> 11.0-1
- Update to 11.0. Fixes bug #1178421

* Fri Dec 26 2014 Kevin Fenzi <kevin@scrye.com> 8.2.1-1
- Update to 8.2.1. Fixes bug #1175229

* Thu Oct 23 2014 Ralph Bean <rbean@redhat.com> - 7.0-1
- Latest upstream.  Fixes bug #1154590.

* Mon Oct 13 2014 Ralph Bean <rbean@redhat.com> - 6.1-1
- Latest upstream.  Fixes bug #1152130.

* Sat Oct 11 2014 Ralph Bean <rbean@redhat.com> - 6.0.2-2
- Modernized python2 macros.
- Inlined locale environment variables in the %%check section.
- Remove bundled egg-info and .exes.

* Fri Oct 03 2014 Kevin Fenzi <kevin@scrye.com> 6.0.2-1
- Update to 6.0.2

* Sat Sep 27 2014 Kevin Fenzi <kevin@scrye.com> 6.0.1-1
- Update to 6.0.1. Fixes bug #1044444

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0-8
- Remove the python-setuptools-devel Virtual Provides as per this Fedora 21
  Change: http://fedoraproject.org/wiki/Changes/Remove_Python-setuptools-devel

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0-7
- And another bug in sdist

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0-6
- Fix a bug in the sdist command

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 2.0-4
- Rebuild as wheel for Python 3.4

* Thu Apr 24 2014 Tomas Radej <tradej@redhat.com> - 2.0-3
- Rebuilt for tag f21-python

* Wed Apr 23 2014 Matej Stuchlik <mstuchli@redhat.com> - 2.0-2
- Add a switch to build setuptools as wheel

* Mon Dec  9 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0-1
- Update to new upstream release with a few things removed from the API:
  Changelog: https://pypi.python.org/pypi/setuptools#id139

* Mon Nov 18 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-1
- Update to 1.4 that gives easy_install pypi credential handling

* Thu Nov  7 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-1
- Minor upstream update to reign in overzealous warnings

* Mon Nov  4 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-1
- Upstream update that pulls in our security patches

* Mon Oct 28 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.7-1
- Update to newer upstream release that has our patch to the unittests
- Fix for http://bugs.python.org/issue17997#msg194950 which affects us since
  setuptools copies that code. Changed to use
  python-backports-ssl_match_hostname so that future issues can be fixed in
  that package.

* Sat Oct 26 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.6-1
- Update to newer upstream release.  Some minor incompatibilities listed but
  they should affect few, if any consumers.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.9.6-1
- Upstream update -- just fixes python-2.4 compat

* Tue Jul 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.9.5-1
- Update to 0.9.5
  - package_index can handle hashes other than md5
  - Fix security vulnerability in SSL certificate validation
  - https://bugzilla.redhat.com/show_bug.cgi?id=963260

* Fri Jul  5 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8-1
- Update to upstream 0.8  release.  Codebase now runs on anything from
  python-2.4 to python-3.3 without having to be translated by 2to3.

* Wed Jul  3 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.7-1
- Update to 0.7.7 upstream release

* Mon Jun 10 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.2-2
- Update to the setuptools-0.7 branch that merges distribute and setuptools

* Thu Apr 11 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.36-1
- Update to upstream 0.6.36.  Many bugfixes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 0.6.28-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.6.28-2
- remove rhel logic from with_python3 conditional

* Mon Jul 23 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.28-1
- New upstream release:
  - python-3.3 fixes
  - honor umask when setuptools is used to install other modules

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.27-2
- Fix easy_install.py having a python3 shebang in the python2 package

* Thu Jun  7 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.27-1
- Upstream bugfix

* Tue May 15 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.24-2
- Upstream bugfix

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.24-1
- Upstream bugfix
- Compile the win32 launcher binary using mingw

* Sun Aug 21 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.21-1
- Upstream bugfix release

* Thu Jul 14 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.19-1
- Upstream bugfix release

* Tue Feb 22 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.14-7
- Switch to patch that I got in to upstream

* Tue Feb 22 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.14-6
- Fix build on python-3.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.14-4
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Tue Aug 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.14-3
- Update description to mention this is distribute

* Thu Jul 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.14-2
- bump for building against python 2.7

* Thu Jul 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.14-1
- update to new version
- all patches are upsteam

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.13-7
- generalize path of easy_install-2.6 and -3.1 to -2.* and -3.*

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.13-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul 3 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-5
- Upstream patch for compatibility problem with setuptools
- Minor spec cleanups
- Provide python-distribute for those who see an import distribute and need
  to get the proper package.

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-4
- Fix race condition in unittests under the python-2.6.x on F-14.

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-3
- Fix few more buildroot macros

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-2
- Include data that's needed for running tests

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-1
- Update to upstream 0.6.13
- Minor specfile formatting fixes

* Thu Feb 04 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.10-3
- First build with python3 support enabled.

* Fri Jan 29 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.10-2
- Really disable the python3 portion

* Fri Jan 29 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.10-1
- Update the python3 portions but disable for now.
- Update to 0.6.10
- Remove %%pre scriptlet as the file has a different name than the old
  package's directory

* Tue Jan 26 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.9-4
- Fix install to make /usr/bin/easy_install the py2 version
- Don't need python3-tools since the library is now in the python3 package
- Few other changes to cleanup style

* Fri Jan 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.9-2
- add python3 subpackage

* Mon Dec 14 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.9-1
- New upstream bugfix release.

* Sun Dec 13 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.8-2
- Test rebuild

* Mon Nov 16 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.8-1
- Update to 0.6.8.
- Fix directory => file transition when updating from setuptools-0.6c9.

* Tue Nov 3 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.7-2
- Fix duplicate inclusion of files.
- Only Obsolete old versions of python-setuptools-devel

* Tue Nov 3 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.7-1
- Move easy_install back into the main package as the needed files have been
  moved from python-devel to the main python package.
- Update to 0.6.7 bugfix.

* Fri Oct 16 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.6-1
- Upstream bugfix release.

* Mon Oct 12 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.4-1
- First build from the distribute codebase -- distribute-0.6.4.
- Remove svn patch as upstream has chosen to go with an easier change for now.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6c9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c9-4
- Apply SVN-1.6 versioning patch (rhbz #511021)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6c9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

## END: Generated by rpmautospec
