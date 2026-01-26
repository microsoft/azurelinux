Vendor:         Microsoft Corporation
Distribution:   Azure Linux


%global srcname jwcrypto

Name:           python-%{srcname}
Version:        1.4.2
Release:        12%{?dist}
Summary:        Implements JWK, JWS, JWE specifications using python-cryptography

License:        LGPL-3.0-or-later
URL:            https://github.com/latchset/%{srcname}
Source0:        https://github.com/latchset/%{srcname}/releases/download/v%{version}/%{srcname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-cryptography >= 2.3
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-deprecated
BuildRequires:  python3-wrapt
%if 0%{?with_check}
BuildRequires:  python3-pip
%endif

%description
Implements JWK, JWS, JWE specifications using python-cryptography


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Implements JWK, JWS, JWE specifications using python-cryptography
Requires:       python%{python3_pkgversion}-cryptography >= 2.3
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
Implements JWK, JWS, JWE specifications using python-cryptography


%prep
%setup -q -n %{srcname}-%{version}
%if %{defined rhel}
# avoid python-deprecated dependency
sed -i -e '/deprecated/d' setup.py %{srcname}.egg-info/requires.txt
sed -i -e '/^from deprecated/d' -e '/@deprecated/d' %{srcname}/*.py
%endif


%build
%py3_build


%check
%{__python3} -bb -m pytest %{srcname}/test*.py


%install
%py3_install

rm -rf %{buildroot}%{_docdir}/%{srcname}
rm -rf %{buildroot}%{python3_sitelib}/%{srcname}/tests{,-cookbook}.py*
rm -rf %{buildroot}%{python3_sitelib}/%{srcname}/__pycache__/tests{,-cookbook}.*.py*


%files -n python%{python3_pkgversion}-%{srcname}
%doc README.md
%license LICENSE
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info


%changelog
* Mon May 12 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.4.2-12
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.4.2-10
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jul 24 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.4.2-7
- Avoid python-deprecated dependency in RHEL builds

* Mon Jul 24 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.4.2-6
- Remove obsolete python2 packaging

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.4.2-4
- Rebuilt for Python 3.12

* Tue Apr 04 2023 Christian Heimes <cheimes@redhat.com> - 1.4.2-3
- Use SPDX license tags

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 15 2022 Simo Sorce <simo@redhat.com> - 1.4.2-1
- Version 1.4.2

* Wed Sep 14 2022 Simo Sorce <simo@redhat.com> - 1.4.1-1
- Version 1.4.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 0.9.1-4
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Simo Sorce <simo@redhat.com> - 0.9.1-1
- Sync with upstream release 0.9.1

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.8-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 01 2020 Simo Sorce <simo@redhat.com> - 0.8-1
- Sync with upstream release 0.8

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 29 2019 Christian Heimes <cheimes@redhat.com> - 0.6.0-5
- Remove Python 2 subpackages from F32+
- Resolves: RHBZ #1746760

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 05 2018 Christian Heimes <cheimes@redhat.com> - 0.6.0-1
- New upstream release 0.6.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-2
- Rebuilt for Python 3.7

* Wed Jun 27 2018 Christian Heimes <cheimes@redhat.com> - 0.5.0-1
- New upstream release 0.5.0

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.2-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Christian Heimes <cheimes@redhat.com> - 0.4.2-3
- Run tests with bytes warning

* Tue Aug 01 2017 Christian Heimes <cheimes@redhat.com> - 0.4.2-2
- Modernize spec

* Tue Aug 01 2017 Christian Heimes <cheimes@redhat.com> - 0.4.2-1
- Upstream release 0.4.2
- Resolves: RHBZ #1476150

* Mon Jul 24 2017 Christian Heimes <cheimes@redhat.com> - 0.4.1-1
- Upstream release 0.4.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-2
- Rebuild for Python 3.6

* Wed Aug 31 2016 Simo Sorce <simo@redhat.com> - 0.3.2-1
- Security release 0.3.2
- Resolves: CVE-2016-6298

* Fri Aug 19 2016 Simo Sorce <simo@redhat.com> - 0.3.1-1
- Bugfix release 0.3.1

* Wed Aug 10 2016 Simo Sorce <simo@redhat.com> - 0.3.0-1
- New release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Aug  3 2015 Simo Sorce <simo@redhat.com> - 0.2.1-1
- New release
- Fixes some key generation issues

* Mon Jun 22 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.2.0-5
- Fix macro in changelog
- Remove the last remnants of the test suite

* Wed Jun 17 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.2.0-4
- Ship readme and license with python3 subpackage
- Move tests to %%check

* Wed Jun 17 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.2.0-3
- Fix F21 build error by adding buildrequire python-setuptools
- Move files into python3-jwcrypto subpackage
- Run test suite
- Do not install test suite
- Fix summary and description of python3-jwcrypto

* Tue Jun 16 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.2.0-2
- Enable python3 build

* Tue Jun 16 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.2.0-1
- Initial packaging
