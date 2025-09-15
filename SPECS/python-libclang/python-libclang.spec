%global pypi_name libclang

Summary:        Clang's python bindings
Name:           python-libclang
Version:        18.1.1
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/sighingnow/libclang
Source0:        %{pypi_source}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildArch:      noarch

%description
This library makes it easier to install clang's python bindings.

%package -n     python3-%{pypi_name}
%{?python_provide:%python_provide python3-%{pypi_name}}
Summary:        %{summary}

%description -n python3-%{pypi_name}
This library makes it easier to install clang's python bindings.

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE.TXT
%{python3_sitelib}/*

%changelog
* Thu Apr 25 2024 Osama Esmail <osamaesmail@microsoft.com> - 18.1.1-1
- Upgrading version for 3.0-dev
- Using actual package name so auto-upgrader can read the spec

* Mon Oct 17 2022 Riken Maharjan <rmaharjan@microsoft.com> - 14.0.6-1
- Original version for CBL-Mariner. License Verified.
