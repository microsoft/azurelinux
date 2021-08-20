%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
# what it's called on pypi
%global srcname PyJWT
# what it's imported as
%global libname jwt
# name of egg info directory
%global eggname %{srcname}
# package name fragment
%global pkgname %{libname}
%global python3_version 3.7

%bcond_without  python3

%global common_description %{expand:
A Python implementation of JSON Web Token draft 01. This library provides a
means of representing signed content using JSON data structures, including
claims to be transferred between two parties encoded as digitally signed and
encrypted JSON objects.}

Name:           python-%{pkgname}
Version:        1.7.1
Release:        9%{?dist}
Summary:        JSON Web Token implementation in Python
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/jpadilla/pyjwt
Source0:        https://files.pythonhosted.org/packages/2f/38/ff37a24c0243c5f45f5798bd120c0f873eeed073994133c084e1cf13b95c/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%description %{common_description}

%if %{with python3}
%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cryptography >= 1.4.0
Requires:       python3-cryptography >= 1.4.0
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
# prevent pullng in `addopts` for pytest run later
rm setup.cfg

%build
%{?with_python3:python3 setup.py build}

%install
%{?with_python3:python3 setup.py install --skip-build --root=%{buildroot}}

%check
pip3 install pluggy>=0.7 more-itertools>=4.0.0 attrs==19.1.0 pytest==4.0.1
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python%{python3_version} -m pytest -v

%if %{with python3}
%files -n python3-%{pkgname}
%doc README.rst AUTHORS
%license LICENSE
%{python3_sitelib}/%{libname}
%{python3_sitelib}/%{eggname}-%{version}-py%{python3_version}.egg-info
#%{python3_sitelib}/%{eggname}-%{version}-py3.7.egg-info
%{_bindir}/pyjwt
%endif

%changelog
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
