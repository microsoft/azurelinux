%global pypi_name testscenarios

Name:           python-%{pypi_name}
Version:        0.5.0
Release:        24%{?dist}
Summary:        Testscenarios, a pyunit extension for dependency injection
License:        ASL 2.0 and BSD
URL:            https://launchpad.net/testscenarios
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://files.pythonhosted.org/packages/f0/de/b0b5b98c0f38fd7086d082c47fcb455eedd39a044abe7c595f5f40cd6eed/testscenarios-0.5.0.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
#BuildRequires:  python3-testtools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3dist(wheel)

%global _description\
testscenarios provides clean dependency injection for python unittest style\
tests. This can be used for interface testing (testing many implementations via\
a single test suite) or for classic dependency injection (provide tests with\
dependencies externally to the test code itself, allowing easy testing in\
different situations).

%description %_description

%package -n python3-%{pypi_name}
Summary:        Testscenarios, a pyunit extension for dependency injection
Requires:       python3-pbr
Requires:       python3-testtools

%description -n python3-%{pypi_name}
testscenarios provides clean dependency injection for python unittest style
tests. This can be used for interface testing (testing many implementations via
a single test suite) or for classic dependency injection (provide tests with
dependencies externally to the test code itself, allowing easy testing in
different situations).

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove unknown test options from setup.py
sed -i '/^buffer = 1$/d' setup.cfg
sed -i '/^catch = 1$/d' setup.cfg

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%{python3} setup.py test

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license Apache-2.0 BSD
%doc GOALS HACKING NEWS README doc/

%changelog
* Fri Dec 21 2024 Jyoti kanase <v-jykanase@microsoft.com> -  0.5.0-24
- Updated source0 and build dependency
- License verified.

* Tue Sep 03 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.0-23
- Release bump to fix package information.

* Fri Apr 29 2022 Muhammad Falak <mwani@microsoft.com> - 0.5.0-22
- Add BR on `pip` to enable ptest
- License verified

* Tue Oct 13 2020 Steve Laughman <steve.laughman@microsoft.com> - 0.5.0-21
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-19
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-17
- Subpackage python2-testscenarios has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-16
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Lumír Balhar <lbalhar@redhat.com> - 0.5.0-12
- Added tests
- Fixed dependencies
- Improved and modernized specfile

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-11
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.0-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.5.0-8
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.0-7
- Python 2 binary package renamed to python2-testscenarios
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 20 2015 Matthias Runge <mrunge@redhat.com> - 0.5.0-1
- update to 0.5.0

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 03 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.4-5
- Add python3 support (RHBZ #1208889)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Matthias Runge <mrunge@redhat.com> - 0.4-2
- correct License: ASL 2.0 and BSD
- include doc files

* Fri May 17 2013 Matthias Runge <mrunge@redhat.com> - 0.4-1
- Initial package.
