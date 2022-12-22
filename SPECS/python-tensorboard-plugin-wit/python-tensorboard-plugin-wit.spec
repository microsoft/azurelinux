%global pypi_name tensorboard-plugin-wit
%global _description %{expand:
The What-If Tool (WIT) provides an easy-to-use interface for expanding understanding of a black-box classification or regression ML model}
%define _enable_debug_package 0
%global debug_package %{nil}
Summary:        The What-If Tool (WIT) provides an easy-to-use interface for expanding understanding of a black-box classification or regression ML model
Name:           python-%{pypi_name}
Version:        1.8.1
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pair-code.github.io/what-if-tool/
Source0:        https://github.com/PAIR-code/what-if-tool/archive/refs/tags/v1.8.1.tar.gz#/%{pypi_name}-%{version}.tar.gz
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-wheel
ExclusiveArch:  x86_64

%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -p1 -n what-if-tool-%{version}

%build
ln -s %{_bindir}/python3 %{_bindir}/python
python3 tensorboard_plugin_wit/pip_package/setup.py -q bdist_wheel
mkdir -p pyproject-wheeldir/ && cp ./dist/*.whl pyproject-wheeldir/

%install
%{pyproject_install}


%files -n python3-%{pypi_name}
%doc README.md
%license LICENSE
%{python3_sitelib}/*

%changelog
* Mon Dec 19 2022 Riken Maharjan <rmaharjan@microsoft.com> - 1.8.1-1
- Original version for CBL-Mariner. License Verified.
