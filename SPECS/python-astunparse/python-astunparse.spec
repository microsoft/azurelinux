%global pypi_name astunparse

Summary:        An AST unparser for Python
Name:           python-%{pypi_name}
Version:        1.6.3
Release:        10%{?dist}
# Primarily under the terms of BSD
# The unparse and the test_unparse modules are under the PSF license.
License:        BSD AND PSF
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/simonpercivall/astunparse
Source0:        %{pypi_source}

# Python 3.9+ support
# https://github.com/simonpercivall/astunparse/pull/57
Patch1:         python3.9.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-wheel

%description
This is a factored out version of unparse found in the Python source
distribution; under Tools/parser in Python 3.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
This is a factored out version of unparse found in the Python source
distribution; under Tools/parser in Python 3.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/

%changelog
* Thu Oct 06 2022 Riken Maharjan <rmaharjan@microsoft.com> - 1.6.3-10
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.6.3-8
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.6.3-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 07 2020 Miro Hrončok <mhroncok@redhat.com> - 1.6.3-1
- Update to 1.6.3 (#1844891)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 12 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.2-5
- Python 3.8 fixes (#1758472)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jan 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.2-1
- Initial package
