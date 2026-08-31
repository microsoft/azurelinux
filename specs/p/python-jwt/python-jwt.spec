# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# what it's called on pypi
%global srcname PyJWT
# what it's imported as
%global libname jwt
# package name fragment
%global pkgname %{libname}

%global common_description %{expand:
A Python implementation of JSON Web Token draft 01. This library provides a
means of representing signed content using JSON data structures, including
claims to be transferred between two parties encoded as digitally signed and
encrypted JSON objects.}


Name:           python-%{pkgname}
Version:        2.8.0
Release:        7%{?dist}
Summary:        JSON Web Token implementation in Python
License:        MIT
URL:            https://github.com/jpadilla/pyjwt
Source:         %pypi_source
BuildArch:      noarch


%description %{common_description}


%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
Recommends:     python3-%{pkgname}+crypto


%description -n python3-%{pkgname} %{common_description}


%pyproject_extras_subpkg -n python3-%{pkgname} crypto


%prep
%autosetup -n %{srcname}-%{version}
# remove coverage buildreq and relax pytest req
sed -e '/coverage/d' \
    -e '/pytest/ s/,<7.0.0//' \
    -i setup.cfg


%generate_buildrequires
%pyproject_buildrequires -x crypto,tests


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{libname}


%check
%pytest -k 'not (test_ec_to_jwk_with_invalid_curve or test_get_jwt_set_sslcontext_default)'


%files -n python3-%{pkgname} -f %{pyproject_files}
%doc README.rst


%changelog
* Tue Sep 23 2025 Miroslav Suchy <msuchy@redhat.com> - 2.8.0-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.8.0-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.8.0-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 30 2024 Kevin Fenzi <kevin@scrye.com> - 2.8.0-1
- Update to 2.8.0. Fixes rhbz#2196700

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.6.0-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.6.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jan  7 2023 Kevin Fenzi <kevin@scrye.com> - 2.6.0-1
- Update to 2.6.0. rhbz#2127626

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 2.4.0-2
- Rebuilt for Python 3.11

* Thu May 19 2022 Major Hayden <major@mhtx.net> - 2.4.0-1
- Update to 2.4.0 (#2085157)
- Fix CVE-2022-29217 (#2088546)

* Tue Apr 26 2022 Carl George <carl@george.computer> - 2.3.0-3
- Convert to pyproject macros

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 26 2021 Joel Capitao <jcapitao@redhat.com> - 2.3.0-1
- Update to 2.3.0 (rhbz#2011642)

* Sun Oct 03 2021 Kevin Fenzi <kevin@scrye.com> - 2.1.0-3
- Relax python-cryptography requirements ( rhbz#2010061 )

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Major Hayden <major@mhtx.net> - 2.1.0-1
- Update to 2.1.0

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 2.0.1-2
- Rebuilt for Python 3.10

* Mon Apr 26 2021 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-1
- Update to 2.0.1
- CLI and Python 2 support dropped in 2.0.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.7.1-9
- Minor conditional fix for ELN

* Fri Jul 10 2020 Miro Hrončok <mhroncok@redhat.com> - 1.7.1-9
- Add pyjwt[crypto] subpackage

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.7.1-8
- Rebuilt for Python 3.9

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
