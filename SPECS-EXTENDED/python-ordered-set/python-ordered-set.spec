Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname ordered-set
%global dir_name ordered_set

Name:           python-%{srcname}
Version:        3.1
Release:        6%{?dist}
Summary:        Custom MutableSet that remembers its order

License:        MIT
URL:            https://github.com/LuminosoInsight/ordered-set
Source0:        %{pypi_source}

BuildArch:      noarch

%global _description\
An OrderedSet is a custom MutableSet that remembers its order, so that every\
entry has an index that can be looked up.

%description %_description

%package     -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
BuildRequires:  python3-pytest

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py nosetests

%files -n python3-%{srcname}
%license MIT-LICENSE
%doc README.md
%{python3_sitelib}/%{dir_name}-*.egg-info/
%{python3_sitelib}/%{dir_name}.py
%{python3_sitelib}/__pycache__/%{dir_name}.*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 16 2019 Pavel Raiskup <praiskup@redhat.com> - 3.1-1
- the latest upstream release (rhbz#1592092)

* Mon Mar 11 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.2-9
- Drop python2 subpackage

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 19 2018 Igor Gnatenko <ignatenkobrain@fedoraprojcet.org> - 2.0.2-7
- Modernize spec

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.2-5
- Rebuilt for Python 3.7

* Tue Feb 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0.2-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Sep 27 2017 Troy Dawson <tdawson@redhat.com> - 2.0.2-2
- Cleanup spec file conditionals

* Mon Aug 21 2017 Miroslav Suchý <msuchy@redhat.com> 2.0.2-1
- add license

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.0-8
- Python 2 binary package renamed to python2-ordered-set
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.0.0-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Feb 09 2016 Miroslav Suchý <miroslav@suchy.cz> 2.0.0-3
- fix BR condition

* Tue Feb 09 2016 Miroslav Suchý <miroslav@suchy.cz> 2.0.0-2
- add BR python-nose for test

* Tue Feb 09 2016 Miroslav Suchý <miroslav@suchy.cz> 2.0.0-1
- rebase to 2.0.0

* Tue Sep 22 2015 Miroslav Suchý <msuchy@redhat.com> 1.3.1-4
- add missing BR on el6
- add missing macro on el6

* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 1.3.1-3
- include egg-info again
- fix typo

* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 1.3.1-2
- exclude __pycache__/ from filelist

* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 1.3.1-1
- new package

