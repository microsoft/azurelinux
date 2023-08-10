%global srcname cstruct
%global _description %{expand:
Convert C struct/union definitions into Python classes with 
methods for serializing/deserializing.}

Summary:        C-style structs for Python
Name:           python-%{srcname}
Version:        5.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://github.com/andreax79/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif
BuildArch:      noarch

%description %{_description}

%package -n     python3-%{srcname}
Summary:        %{summary}
Requires:       python3

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

%check
%pytest

%files -n python3-%{srcname}
%license LICENSE
%{python3_sitelib}/*

%changelog
* Tue Mar 08 2022 Dallas Delaney <dadelan@microsoft.com> - 5.2-1
- Original version for CBL-Mariner
- License verified
