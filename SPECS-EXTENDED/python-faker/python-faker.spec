Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname faker
%global _description\
Faker is a Python package that generates fake data for you. Whether you need\
to bootstrap your database, create good-looking XML documents, fill-in your\
persistence to stress test it, or anonymize data taken from a production\
service, Faker is for you.

Name:           python-%{srcname}
Version:        4.0.0
Release:        3%{?dist}
Summary:        Faker is a Python package that generates fake data for you

License:        MIT
URL:            https://faker.readthedocs.io
Source:         https://github.com/joke2k/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest-runner

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
Suggests:       %{name}-doc = %{version}-%{release}

%description -n python3-%{srcname} %_description

%package doc
Summary:        Documentation for %{name}

%description doc %_description

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%license LICENSE.txt
%{_bindir}/faker
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/Faker-%{version}-py*.egg-info

%files doc
%license LICENSE.txt
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst docs/*.rst

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.0.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
