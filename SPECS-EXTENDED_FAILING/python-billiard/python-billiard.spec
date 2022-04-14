%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%{!?python2_version: %define python2_version %(python2 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?py2_build: %define py2_build CFLAGS="%{optflags}" %{__python2} setup.py build}
%{!?py2_install: %define py2_install %{__python2} setup.py install --skip-build --root %{buildroot}}

%global srcname billiard

%bcond_without  python3
%bcond_without  tests
%bcond_with     python2

Summary:        A multiprocessing pool extensions
Name:           python-%{srcname}
Version:        3.6.3.0
Release:        4%{?dist}
License:        BSD
URL:            https://github.com/celery/billiard
Vendor:         Microsoft
Distribution:   Mariner
Group:          Development/Languages
Source0:        https://files.pythonhosted.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz

# Issue #309: Add Python 3.9 support to spawnv_passfds() , patch edited not to alter tox.ini
#Patch0001:      https://github.com/celery/billiard/commit/ca3220ba4596ac7bb03f64b80e91878353fc5be1.patch
%if %{with python3}
BuildArch:      noarch
%endif

%description
This package contains extensions to the multiprocessing pool.

%if %{with python2}
%package -n python2-%{srcname}
Summary:        %{summary}

BuildRequires:  gcc
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with tests}
BuildRequires:  python2-case
BuildRequires:  python2-mock
BuildRequires:  python2-psutil
BuildRequires:  python2-pytest
BuildRequires:  python2-unittest2
%endif
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
This package contains extensions to the multiprocessing pool.
%endif

%if %{with python3}
%package -n python3-%{srcname}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with tests}
BuildRequires:  python3-case
BuildRequires:  python3-mock
BuildRequires:  python3-psutil
BuildRequires:  python3-pytest
%endif
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
This package contains extensions to the multiprocessing pool.
%endif

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{?with_python2:%py2_build}
%{?with_python3:%py3_build}

%install
%{?with_python2:%py2_install}
%{?with_python3:%py3_install}

%if %{with tests}
%check
%{?with_python2:py.test-2}
%{?with_python3:py.test-3}
%endif

%if %{with python2}
%files -n python2-%{srcname}
%license LICENSE.txt
%doc CHANGES.txt
%doc README.rst
%{python2_sitearch}/_billiard*
%{python2_sitearch}/%{srcname}/
%{python2_sitearch}/%{srcname}*.egg-info
%endif

%if %{with python3}
%license LICENSE.txt
%files -n python3-%{srcname}
%doc CHANGES.txt
%doc README.rst
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{srcname}/
%endif

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 3.6.3.0-4
- Remove epoch

* Mon Oct 19 2020 Steve Laughman <steve.laughman@microsoft.com> - 3.6.3.0-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 01 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1:3.6.3.0-1
- billiard 3.6.3.0

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 1:3.6.1.0-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:3.6.1.0-4
- Remove dependency on unittest2 (#1789200)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:3.6.1.0-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:3.6.1.0-2
- Rebuilt for Python 3.8

* Mon Aug 19 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.6.1.0-1
- Update to latest upstream version 3.6.1.0 (rhbz#1742741)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:3.6.0.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 01 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.6.0.0-1
- Update to latest upstream version 3.6.0.0 (rhbz#1672168)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Neal Gompa <ngompa13@gmail.com> - 1:3.5.0.5-1
- Update to 3.5.0.5
- Disable tests on EPEL7 due to missing dependencies

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1:3.5.0.3-5
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Matthias Runge <mrunge@redhat.com> - 1:3.5.0.3-4
- add gcc to buildrequires

* Sun Feb 11 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1:3.5.0.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 27 2017 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.5.0.3-1
- Update to latest upstream version 3.5.0.3 (rhbz#1471568)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 07 2017 Matthias Runge <mrunge@redhat.com> - 1:3.5.0.2-1
- update to 3.5.0.2
- enable tests again

* Thu Dec 22 2016 Adam Williamson <awilliam@redhat.com> -  - 1:3.5.0.1-2
- Disable tests for now, they cannot work till python-case is packaged

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com>
- Rebuild for Python 3.6

* Wed Nov 16 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.5.0.1-1
- Update to latest upstream version 3.5.0.1 (rhbz#1354091)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.0.23-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Mar 09 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.3.0.23-1
- Update to latest upstream version 3.3.0.23 (rhbz#1314751)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.3.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.3.0.22-1
- Update to latest upstream version 3.3.0.22 (rhbz#1275443)

* Thu Nov 12 2015 Kalev Lember <klember@redhat.com> - 1:3.3.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 28 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.3.0.21-1
- Update to latest upstream version 3.3.0.21 (rhbz#1086634)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 18 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.3.0.20-1
- Update to latest upstream version 3.3.0.20 (rhbz#1213018)

* Fri Nov 21 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.3.0.19-1
- Update to latest upstream version 3.3.0.19 (rhbz#1166400)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 23 2014 Fabian Affolter <mail@fabian-affolter.ch> - 3.3.0.18-1
- Update to latest upstream version 3.3.0.18 (rhbz#1111875)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.3.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Apr 17 2014 Fabian Affolter <mail@fabian-affolter.ch> - 3.3.0.17-1
- Update to latest upstream version 3.3.0.17 (rhbz#1088894)

* Wed Mar 05 2014 Fabian Affolter <mail@fabian-affolter.ch> - 3.3.0.16-1
- Update to latest upstream version 3.3.0.16 (rhbz#1063785)

* Thu Jan 23 2014 Fabian Affolter <mail@fabian-affolter.ch> - 3.3.0.14-1
- Update to latest upstream version 3.3.0.14 (rhbz#1055303)

* Wed Jan 08 2014 Matthias Runge <mrunge@redhat.com> - 3.3.0.13-1
- update to 3.3.013 (rhbz#1034114)
- use epoch:1 (rhbz#1028626)

* Thu Nov 21 2013 Matthias Runge <mrunge@redhat.com> - 3.3.0.7-1
- update to 3.3.0.7 (rhbz#1026722)

* Sat Nov 09 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.3.0.1-1
- Update to latest upstream version 3.3.0.1 (rhbz#1026722)

* Mon Oct 28 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.3.0.0-1
- Update to latest upstream version 3.3.0.0 (rhbz#1019144)

* Mon Oct 14 2013 Matthias Runge <mrunge@redhat.com> - 2.7.34-1
- update to 2.7.34 (rhbz#1018595)
- enable tests

* Tue Oct 08 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.7.3.33-1
- Update to latest upstream version 2.7.3.33

* Sat Aug 17 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.7.3.32-1
- Update to latest upstream version 2.7.3.32

* Wed Jul 31 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.7.3.31-1
- Update to latest upstream version 2.7.3.31

* Sat Jun 29 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.7.3.30-1
- Update to latest upstream version 2.7.3.30

* Wed Apr 17 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.7.3.28-1
- Update to latest upstream version 2.7.3.28

* Tue Mar 26 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.7.3.23-1
- Update to latest upstream version 2.7.3.23

* Sat Mar 09 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.7.3.22-1
- Update to latest upstream version 2.7.3.22

* Wed Feb 13 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.7.3.21-1
- Update to latest upstream version 2.7.3.21

* Mon Feb 11 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.7.3.20-1
- Update to latest upstream version 2.7.3.20

* Sun Dec 02 2012 Matthias Runge <mrunge@redhat.com> - 2.7.3.19-1
- Update to upstream version 2.7.3.19

* Tue Nov 06 2012 Matthias Runge <mrunge@redhat.com> - 2.7.3.18-1
- Update to upstream version 2.7.3.18

* Fri Sep 28 2012 Matthias Runge <mrunge@redhat.com> - 2.7.3.17-1
- Update to upstream version 2.7.3.17

* Thu Sep 20 2012 Matthias Runge <mrunge@redhat.com> - 2.7.3.14-1
- Update to upstream version 2.7.3.14

* Sun Aug 26 2012 Matthias Runge <mrunge@matthias-runge.de> - 2.7.3.12-1
- Update to new upstream version 2.7.3.12
- Provide python3 packages
- Enable checks

* Fri Aug 03 2012 Matthias Runge <mrunge@matthias-runge.de> 2.7.3.11-1
- Update to new upstream version 2.7.3.11

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Fabian Affolter <mail@fabian-affolter.ch> - 2.7.3.9-1
- Update to new upstream version 2.7.3.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Aug 14 2010 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.1-2
- TODO removed

* Sat Jul 03 2010 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.1-1
- Initial package
