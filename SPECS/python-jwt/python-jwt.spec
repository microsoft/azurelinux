# This package refers to PyJWT(https://github.com/jpadilla/pyjwt). Not to be confused with python-jwt(https://github.com/davedoesdev/python-jwt)
# what it's called on pypi
%global srcname PyJWT
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

Name:           python-%{pkgname}
Version:        2.4.0
Release:        2%{?dist}
Summary:        JSON Web Token implementation in Python
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/jpadilla/pyjwt
Source0:        https://files.pythonhosted.org/packages/d8/6b/6287745054dbcccf75903630346be77d4715c594402cec7c2518032416c2/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%description %{common_description}

%if %{with python3}
%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel >= 3.6
BuildRequires:  python3-setuptools
BuildRequires:  python3-cryptography >= 3
Requires:       python3-cryptography >= 3
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-atomicwrites
%endif
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{common_description}
%endif

%prep
%autosetup -n %{srcname}-%{version}
rm -rf %{eggname}.egg-info

%build
%py3_build

%install
%py3_install

%check
pip3 install coverage[toml]==5.0.4 pytest==6
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python%{python3_version} -m pytest -v

%if %{with python3}
%files -n python3-%{pkgname}
%doc README.rst AUTHORS.rst
%license LICENSE
%{python3_sitelib}/%{libname}
%{python3_sitelib}/%{eggname}-%{version}-py%{python3_version}.egg-info
%endif

%changelog
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

* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.7.1-10
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
