%global srcname nose2

Summary:        Next generation of nicer testing for Python
Name:           python-%{srcname}
Version:        0.10.0
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://nose2.readthedocs.org
Source0:        https://github.com/nose-devs/nose2/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-coverage
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six

%description
nose2 is the next generation of nicer testing for Python, based on the plugins
branch of unittest2. nose2 aims to improve on nose by:
- providing a better plugin API
- being easier for users to configure
- simplifying internal interfaces and processes
- supporting Python 2 and 3 from the same codebase, without translation
- encouraging greater community involvement in its development

In service of some those goals, some features of nose will not be supported in
nose2. See the documentation for a thorough rundown.

%package -n python%{python3_pkgversion}-%{srcname}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Summary:        Next generation of nicer testing for Python

Requires:       python%{python3_pkgversion}-coverage
Requires:       python%{python3_pkgversion}-setuptools
Requires:       python%{python3_pkgversion}-six >= 1.6

%description -n python%{python3_pkgversion}-%{srcname}
nose2 is the next generation of nicer testing for Python, based on the plugins
branch of unittest2. nose2 aims to improve on nose by:
- providing a better plugin API
- being easier for users to configure
- simplifying internal interfaces and processes
- supporting Python 2 and 3 from the same codebase, without translation
- encouraging greater community involvement in its development

In service of some those goals, some features of nose will not be supported in
nose2. See the documentation for a thorough rundown.

%prep
%autosetup -n %{srcname}-%{version} -p0

%build
%py3_build

%install
%py3_install

%check
PYTHONPATH=`pwd` python3 -m nose2.__main__ -v

%files -n python%{python3_pkgversion}-%{srcname}
%license license.txt
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/nose2-%{python3_version}
%{_bindir}/nose2

%changelog
* Wed Mar 30 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.10.0-2
- Updating dependencies.

* Tue Feb 08 2022 Cameron Baird <cameronbaird@microsoft.com> - 0.10.0-1
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Update source to 0.10.0
- License verified

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 01 2019 Aurelien Bompard <abompard@fedoraproject.org> - 0.9.1-1
- Version 0.9.1

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.4-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 21 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7.4-3
- Drop python2 subpackage https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7.4-1
- Update to 0.7.4 (#1509750), fixes FTBFS (#1556222)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.5-8
- Rebuilt for Python 3.7

* Mon Mar 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.6.5-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 10 2017 Aurelien Bompard <abompard@fedoraproject.org> - 0.6.5-4
- Rename a BuildRequires

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.6.5-2
- Rebuild for Python 3.6

* Tue Sep 13 2016 Aurelien Bompard <abompard@fedoraproject.org> - 0.6.5-1
- Initial package.
