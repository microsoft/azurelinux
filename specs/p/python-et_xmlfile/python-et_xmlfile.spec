# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name et_xmlfile
%global sum An implementation of lxml.xmlfile for the standard library
%global desc et_xmlfile is a low memory library for creating large XML files.\
\
It is based upon the xmlfile module from lxml with the aim of allowing code to\
be developed that will work with both libraries. It was developed initially for\
the openpyxl project but is now a standalone module.

Name:           python-%{pypi_name}
Version:        2.0.0
Release:        6%{?dist}
Summary:        %{sum}

License:        MIT
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://foss.heptapod.net/openpyxl/et_xmlfile/-/archive/2.0.0/et_xmlfile-2.0.0.tar.gz
Patch:          Differentiate-assertion-based-on-Python-version.patch

BuildArch:      noarch

%description
%{desc}


%package -n     python3-%{pypi_name}
Summary:        %{sum}
BuildRequires:  python3-devel
BuildRequires:  %py3_dist setuptools
BuildRequires:  %py3_dist pytest
BuildRequires:  %py3_dist lxml
Requires:       %py3_dist lxml

%description -n python3-%{pypi_name}
%{desc}


%prep
%autosetup -n %{pypi_name}-%{version} -p1


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}


%check
%pyproject_check_import

%pytest


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst doc/
%license LICENCE.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.0.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.0.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Julien Enselme <jujens@jujens.eu> - 2.0.0-3
- Correct Python macro usages

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.0.0-2
- Rebuilt for Python 3.14

* Wed Feb 12 2025 Julien Enselme <jujens@jujens.eu> - 2.0.0-1
- Update to 2.0.0 (#2321825)

* Tue Feb 11 2025 Julien Enselme <jujens@jujens.eu> - 1.1.0-12
- Remove useless jdcal dependency.

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.1.0-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.1.0-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Python Maint <python-maint@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.11

* Sat Jun 18 2022 Julien Enselme <jujens@jujens.eu> - 1.1.0
- Update to 1.1.0

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.1-25
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-23
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.1-22
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-19
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-17
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-16
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 27 2019 Julien Enselme - 1.0.0-13
- Remove Python 2 subpackage.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-11
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.0.1-9
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 22 2015 Julien Enselme <jujens@jujens.eu> - 1.0.1-3
- Use pytest to launch tests
- Add lxml to launch tests

* Sun Nov 22 2015 Julien Enselme <jujens@jujens.eu> - 1.0.1-2
- Add tests

* Mon Nov 9 2015 Julien Enselme <jujens@jujens.eu> - 1.0.1-1
- Initial package
