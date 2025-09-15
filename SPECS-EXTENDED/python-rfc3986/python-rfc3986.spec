Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Created by pyp2rpm-1.1.0b

%global pypi_name rfc3986
%global common_description %{expand:
A Python implementation of RFC 3986 including validation and authority parsing.}

Name:           python-%{pypi_name}
Version:        1.5.0
Release:        12%{?dist}
Summary:        Validating URI References per RFC 3986

# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            https://rfc3986.readthedocs.io
Source0:        https://files.pythonhosted.org/packages/79/30/5b1b6c28c105629cc12b33bdcbb0b11b5bb1880c6cfbd955f9e792921aa8/rfc3986-1.5.0.tar.gz
BuildArch:      noarch

%description %{common_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3dist(wheel)
BuildRequires:  python3dist(pytest)   
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3-pip

%description -n python3-%{pypi_name} %{common_description}

%pyproject_extras_subpkg -n python3-%{pypi_name} idna2008

%prep
%setup -q -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -x idna2008

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst


%changelog
* Mon Feb 17 2025 Sumit Jena <v-sumitjena@microsoft.com> - 1.5.0-12
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.5.0-11
- convert license to SPDX
 
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild
 
* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.5.0-9
- Rebuilt for Python 3.13
 
* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.5.0-5
- Rebuilt for Python 3.12
 
* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.5.0-2
- Rebuilt for Python 3.11
 
* Wed Jan 26 2022 Carl George <carl@george.computer> - 1.5.0-1
- Update to version 1.5.0
 
* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.4.0-6
- Rebuilt for Python 3.10
 
* Wed Apr 21 2021 Carl George <carl@george.computer> - 1.4.0-5
- Add idna build requirement to avoid skipping tests
 
* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Thu Sep 03 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.0-3
- Add metapackage for rfc3986[idna2008]
- https://fedoraproject.org/wiki/Changes/PythonExtras
- Fixes: rhbz#1875490
 
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Wed Jun 24 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.4.0-1
- Update to 1.4.0 (#1844405)
 
* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-8
- Rebuilt for Python 3.9
 
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-3
- Subpackage python2-rfc3986 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 02 2019 Yatin Karel <ykarel@redhat.com> - 1.2.0-1
- Bump to 1.2.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-8
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.1-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 20 2016 Javier Peña <jpena@redhat.com> - 0.3.1-4
- Updated to upstream version 0.3.1
- Added python3 subpackage

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 15 2014 Alan Pevec <apevec@redhat.com> - 0.2.0-1
- Initial package.
