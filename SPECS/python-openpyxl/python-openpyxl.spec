%{?python_enable_dependency_generator}
%global pypi_name openpyxl
%global sum Python library to read/write Excel 2010 xlsx/xlsm files
%global desc openpyxl is a Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.\
\
It was born from lack of existing library to read/write natively from Python the\
Office Open XML format.

Name:           python-%{pypi_name}
Version:        3.1.2
Release:        1%{?dist}
Summary:        %{sum}

License:        MIT and Python
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://files.pythonhosted.org/packages/42/e8/af028681d493814ca9c2ff8106fc62a4a32e4e0ae14602c2a98fc7b741c8/openpyxl-3.1.2.tar.gz

BuildArch:      noarch

%description
%{desc}

%package -n     python3-%{pypi_name}
Summary:        %{sum}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{desc}


%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf *.egg-info


%build
%py3_build


%install
%py3_install


# No tests


%files -n python3-%{pypi_name}
%license LICENCE.rst
%doc README.rst AUTHORS.rst
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/%{pypi_name}/

%changelog
* Mon May 20 2024 Alberto David Perez Guevara <aperezguevaar@microsoft.com> - 3.1.2-1
- Move package to SPEC folder and update package to versin 3.1.2-1
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6.2-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
