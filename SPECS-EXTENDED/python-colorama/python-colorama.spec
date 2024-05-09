Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global pypi_name colorama

%bcond_with python2
%bcond_without python3

Name:           python-%{pypi_name}
Version:        0.4.1
Release:        6%{?dist}
Summary:        Cross-platform colored terminal text

License:        BSD
URL:            https://pypi.python.org/pypi/colorama
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/python-%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
%description
Makes ANSI escape character sequences, for producing colored
terminal text and cursor positioning, work under MS Windows.

ANSI escape character sequences have long been used to produce colored terminal
text and cursor positioning on Unix and Macs. Colorama makes this work on
Windows, too.
It also provides some shortcuts to help generate ANSI sequences, and works fine
in conjunction with any other ANSI sequence generation library, such as
Termcolor.

%if %{with python2}
%package -n python2-%{pypi_name}
Summary:        Cross-platform colored terminal text
BuildRequires:  python2-devel
%{?el6:BuildRequires:  python-setuptools}
%{!?el6:BuildRequires:  python2-setuptools}
%{?el6:Provides: python-%{pypi_name}}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Makes ANSI escape character sequences, for producing colored
terminal text and cursor positioning, work under MS Windows.

ANSI escape character sequences have long been used to produce colored terminal
text and cursor positioning on Unix and Macs. Colorama makes this work on
Windows, too.
It also provides some shortcuts to help generate ANSI sequences, and works fine
in conjunction with any other ANSI sequence generation library, such as
Termcolor.

Python 2 version.
%endif

%if %{with python3}
%package -n python3-%{pypi_name}
Summary:        Cross-platform colored terminal text
%{?python_provide:%python_provide python3-%{pypi_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{pypi_name}
Makes ANSI escape character sequences, for producing colored
terminal text and cursor positioning, work under MS Windows.

ANSI escape character sequences have long been used to produce colored terminal
text and cursor positioning on Unix and Macs. Colorama makes this work on
Windows, too.
It also provides some shortcuts to help generate ANSI sequences, and works fine
in conjunction with any other ANSI sequence generation library, such as
Termcolor.

Python 3 version.
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf *.egg-info

%build
%if %{with python2}
%py2_build
%endif
%if %{with python3}
%py3_build
%endif

%install
%if %{with python2}
%py2_install
%endif
%if %{with python3}
%py3_install
%endif

%if %{with python2}
%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE.txt
%{python2_sitelib}/%{pypi_name}/
%{python2_sitelib}/%{pypi_name}-%{version}-*.egg-info/
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE.txt
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-*.egg-info/
%endif

%changelog
* Fri Mar 05 2021 Henry Li <lihl@microsoft.com> - 0.4.1-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Fix distro check to enable python3 build and disable python2 build

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 05 2019 Alfredo Moralejo <amoralej@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 30 2018 Matthias Runge <mrunge@redhat.com> - 0.4.0-3
- fix python2 and python3 package for all releases

* Fri Oct 19 2018 Javier Peña <jpena@redhat.com> - 0.4.0-2
- Fix python2 package for non-Fedora

* Fri Oct 19 2018 Matthias Runge <mrunge@redhat.com> - 0.4.0-1
- update to 0.4.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.9-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 20 2017 Matthias Runge <mrunge@redhat.com> - 0.3.9-1
- update to 0.3.9 (rhbz#1444626)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.7-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Apr 10 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.3.7-2
- Follow new packaging guidelines

* Tue Mar 08 2016 Matthias Runge <mrunge@redhat.com> - 0.3.7-1
- update to 0.3.7 (rhbz#1179250)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Sep 05 2014 Matthias Runge <mrunge@redhat.com> - 0.3.2-1
- update to 0.3.2 (rhbz#1090014)

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.2.7-5
- Skip the python3 %%files section if we don't build the python3 package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Mar 12 2014 Matthias Runge <mrunge@redhat.com> - 0.2.7-2
- introduce python3 package (rhbz#1075410)

* Mon Sep 30 2013 Matthias Rugne <mrunge@redhat.com> - 0.2.7-1
- uddate to 0.2.7 (rhbz#1010924)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Matthias Runge <mrunge@redhat.com> - 0.2.5-1
- update to 0.2.5 (rhbz#913431)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 11 2012 Matthias Runge <mrunge@redhat.com> - 0.2.4-1
- Initial package.
