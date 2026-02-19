Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# what it's called on pypi
%global srcname python-mimeparse
# what it's imported as
%global libname mimeparse
# package name fragment
%global pkgname mimeparse

%global common_description %{expand:
This module provides basic functions for parsing mime-type names
and matching them against a list of media-ranges.}


Name:           python-%{pkgname}
Version:        2.0.0
Release:        1%{?dist}
Summary:        Python module for parsing mime-type names
License:        MIT
URL:            https://github.com/dbtsai/python-mimeparse
Source0:        %{pypi_source python_mimeparse}
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-setuptools_scm


%description %{common_description}


%package -n python%{python3_pkgversion}-%{pkgname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pkgname}}


%description -n python%{python3_pkgversion}-%{pkgname} %{common_description}


%prep
%autosetup -n python_mimeparse-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{libname}


%check
%pytest


%files -n python%{python3_pkgversion}-%{pkgname} -f %{pyproject_files}
%license LICENSE
%doc README.rst


%changelog
* Mon Mar 24 2025 Kevin Lockwood <v-klockwood@microsoft.com> - 2.0.0-1
- Update to 2.0.0
- Remove unneeded python2 conditionals
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.0-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 05 2019 Carl George <carl@george.computer> - 1.6.0-11
- Disable python2 subpackage on F32+ and EL8+ rhbz#1757447

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-10
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 07 2017 Carl George <carl@george.computer> - 1.6.0-4
- Enable python34 subpackage for EPEL

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 04 2017 Carl George <carl.george@rackspace.com> - 1.6.0-2
- Spec file clean up

* Tue Feb 28 2017 Carl George <carl.george@rackspace.com> - 1.6.0-1
- New upstream https://github.com/dbtsai/python-mimeparse
- Modernize spec file per Python Packaging Guidelines

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.1.4-10
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Sep 02 2015 Jan Kaluza <jkaluza@redhat.com> - 0.1.4-6
- provide python2-mimeparse (#1241680)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 18 2013 Pádraig Brady <P@draigBrady.com> - 0.1.4-1
- Update to release 0.1.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Jan Kaluza <jkaluza@redhat.com> - 0.1.3-2
- python3 support disabled
- removed useless spec file directives
- run upstream test

* Wed Nov 02 2011 Jan Kaluza <jkaluza@redhat.com> - 0.1.3-1
- Initial version
