Summary:        A hierarchical configuration system
Name:           python-omegaconf
Version:        2.3.0
Release:        1%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.org/project/omegaconf/
Source0:        https://github.com/omry/omegaconf/archive/refs/tags/v%{version}.tar.gz#%{name}-%version.tar.gz
%if 0%{?with_check}
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
OmegaConf is a hierarchical configuration system, with support for merging configurations from multiple sources
providing a consistent API regardless of hwo the configuration was created

%package -n     python3-omegaconf
Summary:        hierarchical configuratin system
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3

%description -n python3-omegaconf
OmegaConf is a hierarchical configuration system, with support for merging configurations from multiple sources
providing a consistent API regardless of hwo the configuration was created

%prep
%autosetup -n omegaconf-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install mock wheel
#%python3 setup.py test

%files -n python3-omegaconf
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri May 10 2024 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 2.3.0-1
- Original version for Azure Linux.
- license verified.
