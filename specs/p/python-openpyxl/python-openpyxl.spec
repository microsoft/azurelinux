# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name openpyxl
%global sum Python library to read/write Excel 2010 xlsx/xlsm files
%global desc openpyxl is a Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.\
\
It was born from lack of existing library to read/write natively from Python the\
Office Open XML format.

Name:           python-%{pypi_name}
Version:        3.1.5
Release: 5%{?dist}
Summary:        %{sum}

# Automatically converted from old format: MIT and Python - review is highly recommended.
License:        LicenseRef-Callaway-MIT AND LicenseRef-Callaway-Python
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        %pypi_source

BuildArch:      noarch

%description
%{desc}

%package -n     python3-%{pypi_name}
Summary:        %{sum}
BuildRequires:  python3-devel
BuildRequires:  python3dist(numpy)
Requires:       python3dist(numpy)

%description -n python3-%{pypi_name}
%{desc}


%prep
%setup -q -n %{pypi_name}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}


# No tests


%check
%pyproject_check_import


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst AUTHORS.rst
%license LICENCE.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.1.5-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.1.5-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Julien Enselme <jujens@jujens.eu> - 3.1.5-1
- Update to 3.1.5
- Correct Python macro usages

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.1.2-10
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 3.1.2-8
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.1.2-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.1.2-2
- Rebuilt for Python 3.12

* Tue Apr 25 2023 Julien Enselme <jujens@jujens.eu> - 3.1.2-1
- Update to 3.1.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 29 2022 Julien Enselme <jujens@jujens.eu> - 3.0.10-1
- Update to 3.0.10

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.0.3-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.0.3-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Charalampos Stratakis <cstratak@redhat.com> - 3.0.3-1
- Update to 3.0.3 (#1845744)(#1743387)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.6.2-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Julien Enselme <jujens@jujens.eu> - 2.6.2-1
- Update to 2.6.2

* Sat Mar 23 2019 Julien Enselme <jujens@jujens.eu> - 2.6.1-1
- Update to 2.6.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.4-5
- Enable python dependency generator

* Mon Jan 14 2019 Miro Hrončok <mhroncok@redhat.com> - 2.5.4-4
- Subpackage python2-openpyxl has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.4-2
- Rebuilt for Python 3.7

* Sat Jun 16 2018 Julien Enselme <jujens@jujens.eu> - 2.5.4-1
- Update to 2.5.4

* Sun Apr 15 2018 Julien Enselme <jujens@jujens.eu> - 2.5.2-1
- Update to 2.5.2

* Mon Mar 12 2018 Julien Enselme <jujens@jujens.eu> - 2.5.1-1
- Update to 2.5.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Julien Enselme - 2.5.0-1
- Update to 2.5.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 25 2017 Julien Enselme <jujens@jujens.eu> - 2.4.7-1
- Update to 2.4.7

* Sun Apr 16 2017 Julien Enselme <jujens@jujens.eu> - 2.4.6-1
- Update to 2.4.6

* Wed Mar 08 2017 Julien Enselme <jujens@jujens.eu> - 2.4.5-1
- Update to 2.4.5

* Fri Feb 24 2017 Julien Enselme <jujens@jujens.eu> - 2.4.4-1
- Update to 2.4.4

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-2
- Rebuild for Python 3.6

* Sun Sep 18 2016 Julien Enselme <jujens@jujens.eu> - 2.4.0-1
- Update to 2.4.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 22 2015 Julien Enselme <jujens@jujens.eu> - 2.3.1-1
- Update to 2.3.1
- Correct license
- Remove check section

* Mon Nov 9 2015 Julien Enselme <jujens@jujens.eu> - 2.3.0-1
- Inital package
