Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global pypi_name testresources

Name:           python-%{pypi_name}
Version:        2.0.2
Release:        1%{?dist}
Summary:        Testresources, a pyunit extension for managing expensive test resources

License:        (Apache-2.0 OR BSD-3-Clause) AND GPL-2.0-or-later
# file testresources/tests/TestUtil.py is GPLv2+
URL:            https://github.com/testing-cabal/%{pypi_name}
Source:         https://files.pythonhosted.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
%define _python_dist_allow_version_zero 1

BuildRequires: python-setuptools_scm
BuildRequires: python-pip
BuildRequires: python-pbr
BuildRequires: python-toml
BuildRequires: python-wheel
BuildRequires: python3-pytest
BuildRequires: python3-testtools
BuildRequires: python3-fixtures

Requires: python-pbr

%global _description %{expand:
testresources: extensions to python unittest to allow declarative use
of resources by test cases.}

%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python-devel

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%{python3} -m testtools.run testresources.tests.test_suite

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license Apache-2.0 BSD
%doc README.rst NEWS doc

%changelog
* Wed Jan 21 2026 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 2.0.2-1
- Upgrade to 2.0.2 (Reference: Fedora 44)
- License verified

* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 1.0.0-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add understated dependency on python3-pbr

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-14
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-13
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Mar 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-11
- Subpackage python2-testresources has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-8
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.0.0-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb  8 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.0.0-6
- Use versioned macros

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 18 2016 Matthias Runge <mrunge@redhat.com> - 1.0.0-1
- update to 1.0.0 (rhbz#1309577)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 31 2013 Matthias Runge <mrunge@redhat.com> - 0.2.7-3
- lice
* Fri May 31 2013 Matthias Runge <mrunge@redhat.com> - 0.2.7-2
- spec cleanups, added NEWS, doc/ to doc, really removed bundled egg-info

* Wed May 29 2013 Matthias Runge <mrunge@redhat.com> - 0.2.7-1
- Initial package.
