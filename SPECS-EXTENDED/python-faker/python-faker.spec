#https://homer.apps.099c.org/ tests disabled in RHEL
%if 0%{?rhel}
%bcond_with tests
%else
%bcond_without tests
%endif

%global srcname faker
%global _description\
Faker is a Python package that generates fake data for you. Whether you need\
to bootstrap your database, create good-looking XML documents, fill-in your\
persistence to stress test it, or anonymize data taken from a production\
service, Faker is for you.

Name: python-%{srcname}
Version: 28.4.1
Release: 1%{?dist}
Summary: Faker is a Python package that generates fake data for you
License: MIT
URL: https://faker.readthedocs.io
Source: https://github.com/joke2k/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz
BuildArch: noarch
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%if %{with tests}
BuildRequires: python3-pytest
BuildRequires: python3-dateutil
BuildRequires: python3-freezegun
BuildRequires: python3-validators
BuildRequires: python3-pillow
%endif

%description %_description

%package -n python3-%{srcname}
Summary: %{summary}
%py_provides python3-%{srcname}
Suggests: %{name}-doc = %{version}-%{release}

%description -n python3-%{srcname} %_description

%package doc
Summary: Documentation for %{name}

%description doc %_description

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%if %{with tests}
%check
# Exclude tests that require the faker.sphinx module
%pytest --ignore-glob='tests/sphinx/*'
%endif

%files -n python3-%{srcname}
%license LICENSE.txt
%{_bindir}/faker
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/Faker-%{version}-py*.egg-info

%files doc
%license LICENSE.txt
%doc README.rst CHANGELOG.md CONTRIBUTING.rst RELEASE_PROCESS.rst docs/*.rst

%changelog
* Wed Sep 04 2024 Juan Orti Alcaine <jortialc@redhat.com> - 28.4.1-1
- Version 28.4.1 (RHBZ#2283728)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 25.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 25.0.1-2
- Rebuilt for Python 3.13

* Sat May 04 2024 Juan Orti Alcaine <jortialc@redhat.com> - 25.0.1-1
- Version 25.0.1 (RHBZ#2266540)

* Sat Feb 24 2024 Juan Orti Alcaine <jortialc@redhat.com> - 23.2.1-1
- Version 23.2.1 (RHBZ#2259363)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 22.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 22.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 13 2024 Juan Orti Alcaine <jortialc@redhat.com> - 22.2.0-1
- Version 22.2.0 (RHBZ#2250253)

* Thu Nov 23 2023 Miro Hrončok <mhroncok@redhat.com> - 20.0.0-2
- Remove unused test dependency on random2 (removed upstream in 15.1.4)

* Sat Nov 11 2023 Juan Orti Alcaine <jortialc@redhat.com> - 20.0.0-1
- Version 20.0.0 (RHBZ#2218396)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 18.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Python Maint <python-maint@redhat.com> - 18.11.1-2
- Rebuilt for Python 3.12

* Wed Jun 21 2023 Juan Orti Alcaine <jortialc@redhat.com> - 18.11.1-1
- Version 18.11.1 (RHBZ#2183844)

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 18.3.1-2
- Rebuilt for Python 3.12

* Thu Mar 30 2023 Juan Orti Alcaine <jortialc@redhat.com> - 18.3.1-1
- Version 18.3.1 (RHBZ#2174256)

* Sat Feb 25 2023 Juan Orti Alcaine <jortialc@redhat.com> - 17.3.0-1
- Version 17.3.0 (RHBZ#2160347)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 16.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Juan Orti Alcaine <jortialc@redhat.com> - 16.1.0-1
- Version 16.1.0 (RHBZ#2130353)

* Sat Sep 24 2022 Juan Orti Alcaine <jortialc@redhat.com> - 14.2.1-1
- Version 14.2.1 (RHBZ#2110119)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 13.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Juan Orti Alcaine <jortialc@redhat.com> - 13.15.0-1
- Version 13.15.0 (RHBZ#2069584)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 13.3.3-2
- Rebuilt for Python 3.11

* Fri Mar 25 2022 Juan Orti Alcaine <jortialc@redhat.com> - 13.3.3-1
- Version 13.3.3 (#2064365)
- Disable tests in RHEL

* Wed Mar 09 2022 Juan Orti Alcaine <jortialc@redhat.com> - 13.3.1-1
- Version 13.3.1 (#2051001)

* Wed Feb 02 2022 Juan Orti Alcaine <jortialc@redhat.com> - 12.0.0-1
- Version 12.0.0 (#2037759)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Juan Orti Alcaine <jortialc@redhat.com> - 11.1.0-1
- Version 11.1.0 (#2017297)

* Fri Oct 22 2021 Juan Orti Alcaine <jortialc@redhat.com> - 9.5.2-1
- Version 9.5.2 (#1980163)

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.9.1-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Juan Orti Alcaine <jortialc@redhat.com> - 8.9.1-1
- Version 8.9.1 (#1967787)

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 8.5.0-3
- Rebuilt for Python 3.10

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 8.5.0-2
- Rebuilt for Python 3.10

* Thu Jun 03 2021 Juan Orti Alcaine <jortialc@redhat.com> - 8.5.0-1
- Version 8.5.0
- Use py_provides macro
- Run tests

* Mon May 31 2021 Tomas Hrnciar <thrnciar@redhat.com> - 8.4.0-1
- Update to 8.4.0

* Wed Feb 10 2021 Juan Orti Alcaine <jortialc@redhat.com> - 6.1.1-1
- Version 6.1.1 (#1918209)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Juan Orti Alcaine <jortialc@redhat.com> - 5.6.1-1
- Version 5.6.1 (#1898673)

* Tue Nov 17 2020 Juan Orti Alcaine <jortialc@redhat.com> - 4.15.0-1
- Version 4.15.0 (#1886757)

* Thu Oct 08 2020 Juan Orti Alcaine <jortialc@redhat.com> - 4.8.0-1
- Version 4.8.0 (RHBZ#1884072)
- BR: python3-setuptools

* Sat Sep 19 2020 Juan Orti Alcaine <jortialc@redhat.com> - 4.1.3-1
- Version 4.1.3 (RHBZ#1869448)

* Tue Aug 18 2020 Juan Orti Alcaine <jortialc@redhat.com> - 4.1.2-1
- Version 4.1.2 (RHBZ#1869448)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 12 2020 Juan Orti Alcaine <jortialc@redhat.com> - 4.1.1-1
- Version 4.1.1

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.1.0-2
- Rebuilt for Python 3.9

* Sun May 17 2020 Juan Orti Alcaine <jortialc@redhat.com> - 4.1.0-1
- Version 4.1.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Juan Orti Alcaine <jortialc@redhat.com> - 4.0.0-1
- Version 4.0.0

* Sun Jan 05 2020 Juan Orti Alcaine <jortialc@redhat.com> - 3.0.0-1
- Version 3.0.0

* Wed Sep 18 2019 Juan Orti Alcaine <jortialc@redhat.com> - 2.0.2-1
- Version 2.0.2

* Sat Aug 24 2019 Juan Orti Alcaine <jortialc@redhat.com> - 2.0.1-2
- Add patch to revert the switch to text-unidecode

* Sat Aug 24 2019 Juan Orti Alcaine <jortialc@redhat.com> - 2.0.1-1
- Version 2.0.1

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 16 2019 Juan Orti Alcaine <jorti@fedoraproject.org> - 1.0.2-1
- Version 1.0.2
- Drop python2 subpackage

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 09 2018 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.9.0-1
- Version 0.9.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8.15-2
- Rebuilt for Python 3.7

* Wed May 16 2018 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.8.15-1
- Version 0.8.15

* Tue Mar 13 2018 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.8.12-1
- Version 0.8.12

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 21 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.8.7-2
- Disable doc building because missing dependencies

* Tue Nov 21 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.8.7-1
- Version 0.8.7

* Wed Sep 06 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.8.3-1
- Version 0.8.3

* Mon Sep 04 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.8.1-1
- Version 0.8.1

* Tue Aug 29 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.8.0-2
- Use python2-ipaddress for F28+

* Tue Aug 29 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.8.0-1
- Version 0.8.0
- Update dependencies

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.7.18-1
- Version 0.7.18
- Add versioned python dependencies

* Fri Jun 30 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.7.17-1
- Version 0.7.17

* Wed Apr 05 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.7.10-1
- Version 0.7.10
- Remove huge man page

* Sun Feb 26 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.7.9-1
- Version 0.7.9

* Sun Feb 05 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.7.7-1
- Version 0.7.7
- Add dateutil dependency (RHBZ#1419285)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.3-2
- Rebuild for Python 3.6

* Fri Dec 09 2016 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.7.3-1
- Version 0.7.3

* Wed Jul 20 2016 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.5.9-3
- Disable man page generation

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul 12 2016 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.5.9-1
- Version 0.5.9

* Mon Jul 04 2016 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.5.8-1
- Version 0.5.8

* Sun Mar 13 2016 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.5.7-1
- Version 0.5.7

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 30 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.5.3-7
- Leave only python3 version of faker script

* Wed Nov 25 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.5.3-6
- link binary for different python versions

* Thu Nov 12 2015 Kalev Lember <klember@redhat.com> - 0.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 03 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.5.3-4
- Move all doc files to the doc subpackage
- Include the man page in the main packages

* Fri Oct 30 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.5.3-3
- Add documentation

* Thu Oct 29 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.5.3-2
- Add python provides and follow naming guidelines
- Rename faker binary

* Fri Oct 23 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.5.3-1
- Initial package
