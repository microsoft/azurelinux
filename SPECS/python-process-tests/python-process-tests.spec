%global srcname process-tests
Summary:        Tools for testing processes
Name:           python-%{srcname}
Version:        2.1.2
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ionelmc/python-process-tests
Source0:        https://github.com/ionelmc/python-process-tests/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildArch:      noarch

%description
Tools for testing processes.

%package -n python3-%{srcname}
Summary:        Tools for testing processes
Requires:       python3

%description -n python3-%{srcname}
Tools for testing processes for Python 3.

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python-%{srcname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/process_tests*

%changelog
* Mon Feb 07 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.1.2-1
- Upgrade to latest upstream version
- Remove %%python3_pkgversion boilerplating
- Use upstream github source

* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 2.0.2-10
- Change source to match python sources
- License verified

* Tue Dec 08 2020 Steve Laughman <steve.laughman@microsoft.com> - 2.0.2-9
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.2-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.2-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.2-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr  8 2019 Orion Poplawski <orion@nwra.com> - 2.0.2-2
- Drop python2 (bug #1697617)

* Tue Feb 12 2019 Orion Poplawski <orion@nwra.com> - 2.0.2-1
- Update to 2.0.2

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-11
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 9 2017 Orion Poplawski <orion@cora.nwra.com> - 1.0.0-9
- Ship python2-process-tests
- Build for python3 on EPEL

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.0.0-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 1.0.0-3
- Rebuilt for Python3.5 rebuild

* Wed Jul 29 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0.0-2
- Do not own python3 __pycache__ dir

* Wed Jul 29 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0.0-1
- Initial package
