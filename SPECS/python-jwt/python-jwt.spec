# This package refers to PyJWT(https://github.com/jpadilla/pyjwt). Not to be confused with python-jwt(https://github.com/davedoesdev/python-jwt)
# what it's called on pypi
# Lowercased: PyPI serves the 2.13.0 sdist as pyjwt-2.13.0.tar.gz and the tarball's
# internal directory is also lowercase (was PyJWT-2.8.0.tar.gz / PyJWT-2.8.0 dir before)
%global srcname pyjwt
# what it's imported as
%global libname jwt
# name of egg info directory
%global eggname %{srcname}
# package name fragment
%global pkgname %{libname}

%bcond_without  python3

%global common_description %{expand:
A Python implementation of JSON Web Token draft 01. This library provides a
means of representing signed content using JSON data structures, including
claims to be transferred between two parties encoded as digitally signed and
encrypted JSON objects.}

Name:           python-jwt
Version:        2.13.0
Release:        1%{?dist}
Summary:        JSON Web Token implementation in Python
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/jpadilla/pyjwt
Source0:        https://files.pythonhosted.org/packages/3b/81/58d0ac84e1ef3a3843791d6954d94c0b33d526c75eeb1efbce9d0a4c4077/pyjwt-2.13.0.tar.gz
BuildArch:      noarch

%description %{common_description}

%if %{with python3}
%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel >= 3.6
BuildRequires:  python3-setuptools
BuildRequires:  python3-cryptography >= 3
Requires:       python3-cryptography >= 3
# Added: required by %%check (pip3 install tox) and by pyproject build/install macros
BuildRequires:  python3-pip
# Added: %%pyproject_wheel (in %build) needs the `wheel` package's bdist_wheel command
BuildRequires:  python3-wheel
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{common_description}
%endif

%prep
%autosetup -n %{srcname}-%{version}
# python3-setuptools in Azure Linux (69.0.3) predates PEP 639 support (needs setuptools
# >= 77, per upstream's build-system.requires); rewrite the PEP 639 `license = "MIT"`
# string to the legacy `license = {text = "MIT"}` table form so metadata validation passes
sed -i 's/^license = "MIT"$/license = {text = "MIT"}/' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires

%build
# Switched from %%py3_build (ran `setup.py build`): the 2.13.0 sdist no longer ships
# setup.py, only pyproject.toml
%pyproject_wheel

%install
# Switched from %%py3_install (ran `setup.py install`) for the same reason as %build
%pyproject_install
# Generates the file list consumed by %%files -f %%{pyproject_files} below, avoiding a
# hardcoded/guessed dist-info directory name
%pyproject_save_files %{libname}

%check
pip3 install tox==4.25.0 --ignore-installed
tox

%if %{with python3}
# Switched to the macro-generated file list since %%pyproject_install produces a
# *.dist-info directory (not the egg-info path this used to hardcode)
%files -n python3-%{pkgname} -f %{pyproject_files}
%doc README.rst AUTHORS.rst
%license LICENSE
%endif

%changelog
* Fri Jul 24 2026 BinduSri Adabala <v-badabala@microsoft.com> - 2.13.0-1
- Upgrade from 2.8.0 to 2.13.0 to fix CVE-2026-48524, CVE-2026-32597, CVE-2026-48526, CVE-2026-48522 and CVE-2026-48525

* Mon May 05 2025 Riken Maharjan <rmaharjan@microsoft.com> - 2.8.0-2
- Fixed ptest

* Wed Jul 24 2024 Osama Esmail <osamaesmail@microsoft.com> - 2.8.0-1
- Updating to 2.8.0-1 for 3.0
- Using literal package name so auto-upgrader can do its thing
- Adding buildrequires & replacing check section with simple tox command

* Fri Sep 30 2022 Saul Paredes <saulparedes@microsoft.com> - 2.4.0-2
- Updating to 2.4.0-2 to fix CVE-2022-39227 (no patch, false positive confusion with python-jwt. Scanning tool to be updated).

* Wed Jun 08 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.0-1
- Updating to 2.4.0 to fix CVE-2022-29217.

* Tue Feb 22 2022 Nick Samson <nisamson@microsoft.com> - 2.3.0-1
- Updated to 2.3.0.
- Removed pyjwt binary as it no longer exists.
- Updated Python dependency to at least 3.6.
- Updated cryptography dependency to at least 3.0
- Updated build and install sequence to use CBL-Mariner macros.
- Removed removal of setup.cfg as it no longer installs additional dependencies.

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 1.7.1-10
- Remove hardcoded %%python3_version macro to enable use of Python 3.9

* Wed Jun 23 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 1.7.1-9
- Pass check section

* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 1.7.1-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Update Source0 to a full url instead of a macro.
- License verified.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.1-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 29 2019 Carl George <carl@george.computer> - 1.7.1-5
- Disable python2 subpackage on F32+ rhbz#1744643

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.1-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 27 2019 Carl George <carl@george.computer> - 1.7.1-2
- Re-enable python2 subpackage since python-oauthlib still needs it

* Mon Mar 04 2019 Yatin Karel <ykarel@redhat.com> - 1.7.1-1
- Update to 1.7.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 04 2018 Carl George <carl@george.computer> - 1.6.4-2
- Disable python2 subpackage on F30+
- Don't share doc and license dir between subpackages, can cause upgrade issues
- Add patch1 to skip failing tests

* Wed Jul 25 2018 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.6.4-1
- Update to 1.6.4

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.6.1-2
- Rebuilt for Python 3.7

* Thu Apr 05 2018 Carl George <carl@george.computer> - 1.6.1-1
- Latest upstream
- Add patch0 to remove pytest-{cov,runner} deps
- Share doc and license dir between subpackages
- Enable EPEL PY3 build

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.5.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 16 2017 Kevin Fenzi <kevin@scrye.com> - 1.5.3-1
- Update to 1.5.3. Fixes bug #1488693
- 1.5.1 fixed CVE-2017-11424 Fixes bug #1482529

* Mon Aug 14 2017 Troy Dawson <tdawson@redhat.com> - 1.5.2-3
- Fixup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 24 2017 Kevin Fenzi <kevin@scrye.com> - 1.5.2-1
- Update to 1.5.2. Fixes bug #1464286

* Sat May 27 2017 Kevin Fenzi <kevin@scrye.com> - 1.5.0-1
- Update to 1.5.0. Fixes bug #1443792

* Mon Apr 17 2017 Kevin Fenzi <kevin@scrye.com> - 1.4.2-4
- Modernize spec and make sure to provide python2-jwt

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.4.2-2
- Rebuild for Python 3.6

* Mon Aug 15 2016 Kevin Fenzi <kevin@scrye.com> - 1.4.2-1
- Update to 1.4.2. Fixes bug #1356333

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Sep 16 2015 Ralph Bean <rbean@redhat.com> - 1.4.0-1
- new version

* Wed Jun 17 2015 Ralph Bean <rbean@redhat.com> - 1.3.0-1
- new version
- start running the test suite.

* Fri Mar 27 2015 Ralph Bean <rbean@redhat.com> - 1.0.1-1
- new version

* Thu Mar 19 2015 Ralph Bean <rbean@redhat.com> - 1.0.0-1
- new version

* Fri Feb 20 2015 Ralph Bean <rbean@redhat.com> - 0.4.3-1
- Latest upstream.
- Expand the description as per review feedback.
- Add a comment about the test suite.
- Declare noarch.
- Declare _docdir_fmt

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 0.4.2-1
- initial package for Fedora.
