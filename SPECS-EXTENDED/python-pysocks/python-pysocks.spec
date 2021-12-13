Vendor:         Microsoft Corporation
Distribution:   Mariner

%global with_python3_tests 1


%global pypi_name   PySocks
%global modname     pysocks
%global sum         A Python SOCKS client module

Name:               python-%{modname}
Version:            1.7.1
Release:            5%{?dist}
Summary:            %{sum}

License:            BSD
URL:                https://github.com/Anorov/%{pypi_name}
Source0:            %pypi_source
BuildArch:          noarch

%global _description \
A fork of SocksiPy with bug fixes and extra features.\
\
Acts as a drop-in replacement to the socket module. Featuring:\
\
- SOCKS proxy client for Python 2.6 - 3.x\
- TCP and UDP both supported\
- HTTP proxy client included but not supported or recommended (you should use\
  urllib2's or requests' own HTTP proxy interface)\
- urllib2 handler included.

%description
%_description


%package -n python%{python3_pkgversion}-%{modname}
Summary:            %{sum}
BuildRequires:      python%{python3_pkgversion}-devel
BuildRequires:      python%{python3_pkgversion}-setuptools
# for tests
%if 0%{?with_python3_tests}
BuildRequires:      python%{python3_pkgversion}-pytest
BuildRequires:      python%{python3_pkgversion}-psutil
#BuildRequires:      python%%{python3_pkgversion}-test_server
%endif
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}}

# This package doesn't actually exist...
# but if it did, we would conflict with it.
Conflicts:  python%{python3_pkgversion}-SocksiPy

%description -n python%{python3_pkgversion}-%{modname}
%_description
This package is for Python3 version %{python3_version} only.

%if 0%{?python3_other_pkgversion}
%package -n python%{python3_other_pkgversion}-%{modname}
Summary:            %{sum}
BuildRequires:      python%{python3_other_pkgversion}-devel
BuildRequires:      python%{python3_other_pkgversion}-setuptools
# for tests
%if 0%{?with_python3_tests}
BuildRequires:      python%{python3_other_pkgversion}-pytest
BuildRequires:      python%{python3_other_pkgversion}-psutil
#BuildRequires:      python%%{python3_other_pkgversion}-test_server
%endif
%{?python_provide:%python_provide python%{python3_other_pkgversion}-%{modname}}

%description -n python%{python3_other_pkgversion}-%{modname}
%_description
This package is for Python3 version %{python3_other_version} only.
%endif


%prep
%autosetup -n %{pypi_name}-%{version}
# drop useless 3rdparty code
rm -rfv test/bin

%build
%py3_build
%{?python3_other_pkgversion: %py3_other_build}

%install
%py3_install
%{?python3_other_pkgversion: %py3_other_install}

%check
# https://github.com/Anorov/PySocks/issues/37
# FIXME python module named test_server is needed but not packaged
%if 0
%if 0%{?with_python3_tests}
%{?with_python3: %{__python3} setup.py test}
%{?python3_other_pkgversion: %{__python3_other} setup.py test}
%endif
%endif



%files -n python%{python3_pkgversion}-%{modname}
%doc README.md
%license LICENSE
%{python3_sitelib}/socks.py*
%{python3_sitelib}/sockshandler.py*
%{python3_sitelib}/__pycache__/*socks*
%{python3_sitelib}/%{pypi_name}-%{version}-*

%if 0%{?python3_other_pkgversion}
%files -n python%{python3_other_pkgversion}-%{modname}
%doc README.md
%license LICENSE
%{python3_other_sitelib}/socks.py*
%{python3_other_sitelib}/sockshandler.py*
%{python3_other_sitelib}/__pycache__/*socks*
%{python3_other_sitelib}/%{pypi_name}-%{version}-*
%endif


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.1-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Nov 24 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.1-3
- Subpackage python2-pysocks has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Petr Viktorin <pviktori@redhat.com> - 1.7.1-2
- Remove unused Python 2 test dependencies

* Sun Sep 22 2019 Kevin Fenzi <kevin@scrye.com> - 1.7.1-1
- Update to 1.7.1. Fixes bug #1753823

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-3
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 18 2019 Kevin Fenzi <kevin@scrye.com> - 1.7.0-1
- Update to 1.7.0. Fixes bug #1708882

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 11 2018 Kevin Fenzi <kevin@scrye.com> - 1.6.8-6
- Add upstream patch to avoid DeprecationWarning. Fixes bug #1648583

* Wed Oct 03 2018 Raphael Groner <projects.rg@smart.ms> - 1.6.8-5
- add python3_other subpackage for epel7
- prepare removal of python2 subpackage in Fedora
- use pypi macros
- try to enable tests provided actually from tarball

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 1.6.8-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 22 2017 Kevin Fenzi <kevin@scrye.com> - 1.6.8-1
- Update to 1.6.8. Fixes bug #1528490

* Mon Sep 11 2017 Carl George <carl@george.computer> - 1.6.7-1
- Latest upstream
- Add setuptools dependency

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.5.7-3
- Rebuild for Python 3.6

* Mon Nov 28 2016 Tim Orling <ticotimo@gmail.com> - 1.5.7-2
- Ship python34-pysocks in EL6

* Sat Sep 17 2016 Kevin Fenzi <kevin@scrye.com> - 1.5.7-1
- Update to 1.5.7

* Fri Sep 16 2016 Orion Poplawski <orion@cora.nwra.com> - 1.5.6-6
- Ship python34-pysocks in EPEL7

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 15 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-4
- Change our conflicts on python-SocksiPy to an obsoletes/provides.
  https://bugzilla.redhat.com/show_bug.cgi?id=1334407

* Mon May 09 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-3
- Fix typo in explicit conflicts.

* Tue May 03 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-2
- We don't actually need setuptools here.

* Mon May 02 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-1
- Initial package for Fedora
