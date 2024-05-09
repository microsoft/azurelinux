Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global pypi_name sphinxcontrib-apidoc


Name:           python-%{pypi_name}
Version:        0.2.1
Release:        15%{?dist}
Summary:        A Sphinx extension for running 'sphinx-apidoc' on each build

License:        BSD
URL:            https://www.sphinx-doc.org/
Source0:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/python-%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-sphinx

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-pytest
BuildRequires:  python3-sphinx
BuildRequires:  python3-setuptools

%global common_desc \
This package contains Sphinx extension for running sphinx-apidoc_ \
on each build.Overview *sphinx-apidoc* is a tool for automatic generation \
of Sphinx sources that, using the autodoc <sphinx_autodoc>_ extension, \
documents a whole package in the style of other automatic API documentation \
tools. *sphinx-apidoc* does not actually build documentation - rather it \
simply generates it.

%description
%common_desc

%package -n python3-%{pypi_name}
Summary:    %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
Requires:   python3-pbr
Requires:   python3-sphinx

%description -n python3-%{pypi_name}
%common_desc


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build

%py3_build

%install

%py3_install

# %check
# FIXME(chkumar246): Tests are broken in current version, So
# disabling it, Once new version will be available. We will
# add it.
# py.test ||
# %if %{with python3}
# py.test-3 ||
# %endif

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/sphinxcontrib_apidoc*nspkg.pth
%{python3_sitelib}/sphinxcontrib/apidoc
%{python3_sitelib}/sphinxcontrib_apidoc-%{version}-py?.?.egg-info

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.1-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.1-13
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.1-12
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.1-9
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.1-7
- Rebuilt for Python 3.7

* Tue Apr 10 2018 Chandan Kumar <chkumar246@gmail.com> - 0.2.1-6
- Fixed python3 files

* Tue Apr 10 2018 Chandan Kumar <chkumar246@gmail.com> - 0.2.1-5
- Disabled tests

* Tue Apr 10 2018 Chandan Kumar <chkumar246@gmail.com> - 0.2.1-4
- Added conditional for python3 support

* Tue Apr 10 2018 Chandan Kumar <chkumar246@gmail.com> - 0.2.1-3
- Added python3 conditionals on BR

* Tue Apr 10 2018 Chandan Kumar <chkumar246@gmail.com> - 0.2.1-2
- Added python3 BR and fixed tests

* Tue Apr 10 2018 Chandan Kumar <chkumar246@gmail.com> - 0.2.1-1
- Initial package.
