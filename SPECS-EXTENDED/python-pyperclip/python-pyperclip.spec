Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name pyperclip


Name:           python-%{pypi_name}
Version:        1.6.4
Release:        9%{?dist}
Summary:        A cross-platform clipboard module for Python

License:        BSD
URL:            https://github.com/asweigart/pyperclip
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/python-%{pypi_name}-%{version}.tar.gz
Source1:        %{name}-LICENSE.txt
# Fix tests suite execution
# Disable all tests requiring a display or toolkit to be available at build time
Patch001:       0001-Skip-tests-irrelevant-in-the-context-of-Fedora-packa.patch
BuildArch:      noarch

BuildRequires:  git
 
%description
Pyperclip is a cross-platform Python module for copy and paste clipboard
functions.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{pypi_name}
Pyperclip is a cross-platform Python module for copy and paste clipboard
functions.


%package -n python-%{pypi_name}-doc
Summary:        Pyperclip documentation
BuildRequires:  python3-sphinx

%description -n python-%{pypi_name}-doc
Documentation for pyperclip


%prep
%autosetup -n %{pypi_name}-%{version} -S git
cp %{SOURCE1} ./LICENSE.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Fix ends of line encoding
sed -i 's/\r$//' README.md docs/*

%build
%py3_build
# generate html docs 
PYTHONPATH=${PWD} sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py3_install

%check
%{__python3} setup.py test


%files -n python3-%{pypi_name}
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python-%{pypi_name}-doc
%license LICENSE.txt
%doc html

%changelog
* Fri Dec 01 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.6.4-9
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.4-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.4-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.4-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Mar 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.4-3
- Subpackage python2-pyperclip has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 25 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.6.4-1
- Initial package.
