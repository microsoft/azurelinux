Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name sphinx-epytext
Name:           python-%{pypi_name}
Version:        0.0.4
Release:        3%{?dist}
Summary:        Sphinx epytext extension

License:        MIT
URL:            https://github.com/jayvdb/sphinx-epytext
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%global _description %{expand:
This package provides basic support for epytext docstrings in Sphinx autodoc.}

%description %_description


%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %_description


%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/sphinx_epytext/
%{python3_sitelib}/sphinx_epytext-%{version}-py%{python3_version}.egg-info/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.4-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.4-1
- Initial package
