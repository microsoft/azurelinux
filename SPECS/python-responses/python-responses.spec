%global srcname responses
Summary:        A utility library for mocking out the requests Python library.
Name:           python-%{srcname}
Version:        0.23.3
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/getsentry/responses
# The 0.20.0 release had a bad manifest file, which caused the sdist file to not include tests.
# Future releases should be able to use the actual release tarball, but for now we use the GitHub source tarball
Source0:        https://github.com/getsentry/responses/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-requests
BuildRequires:  python3-urllib3
%endif
BuildArch:      noarch

%description
A utility library for mocking out the requests Python library.

%package -n python3-%{srcname}
%{?python_provide:%python_provide python3-%{srcname}}
Summary:        A utility library for mocking out the requests Python library.
Requires:       python3-requests
Requires:       python3-urllib3

%description -n python3-%{srcname}
A utility library for mocking out the requests Python library.

%prep
%autosetup -n %{srcname}-%{version}
# Fix manifest for test files. Upstreamed in next release after 0.20.0
sed -i 's/^include test_responses\.py test_matchers\.py test_registries\.py$/recursive-include responses *\.py/' MANIFEST.in

%build
%py3_build

%install
%py3_install

%check
pip3 install tox
tox -e py%{python3_version_nodots} --sitepackages

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/%{srcname}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.23.3-1
- Auto-upgrade to 0.23.3 - Azure Linux 3.0 - package upgrades

* Wed Mar 30 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.20.0-1
- Upgrade to latest upstream version
- Use tox to run tests

* Mon Jun 21 2021 Rachel Menge <rachelmenge@microsoft.com> - 0.10.15-4
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 14 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.15-1
- Version update

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.14-2
- Rebuilt for Python 3.9

* Tue May 12 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.14-1
- Version update

* Wed Mar 04 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.12-1
- Version update

* Sat Feb 29 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.11-1
- Version update

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.5-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.5-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 0.10.5-1
- Upgrade to 0.10.5 (#1684241).
- https://github.com/getsentry/responses/blob/0.10.5/CHANGES

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.0-5
- Enable python dependency generator

* Fri Dec 28 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-4
- Subpackage python2-responses has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-2
- Rebuilt for Python 3.7

* Mon Apr 09 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.9.0-1
- Version update
- Explicitly require pythonX-setuptools regardless of environment

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.1-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.1-7
- Escape macros in %%changelog

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 02 2016 Germano Massullo <germano.massullo@gmail.com> - 0.5.1-2
- Fixed python packages prefix for el <= 7

* Mon Jan 25 2016 Germano Massullo <germano.massullo@gmail.com> - 0.5.1-1
- LICENSE file added in upstream update
- Commented %%check section due test file missing in pypi release. See https://github.com/getsentry/responses/issues/98

* Sat Jan 23 2016 Germano Massullo <germano.massullo@gmail.com> - 0.5.0-1
- Package review submission
