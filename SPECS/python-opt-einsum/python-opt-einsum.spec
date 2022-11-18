Summary:        Optimizing einsum function for NumPy
Name:           python-opt-einsum
Version:        3.3.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/opt-einsum
Source0:        https://pypi.python.org/packages/source/o/opt_einsum/opt_einsum-%{version}.tar.gz#/opt-einsum-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-setuptools
BuildArch:      noarch
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
Optimizing einsum function Python package

%package -n     python3-opt-einsum
Summary:        Optimizing einsum function for NumPy
Requires:       python3
Requires:       python3-numpy

%description -n python3-opt-einsum
Optimizing einsum function Python package

%prep
%autosetup -n opt_einsum-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest==7.1.3
%pytest

%files -n python3-opt-einsum
%license LICENSE
%{python3_sitelib}/*

%changelog
* Tue Apr 04 2017 Riken Maharjan <rmaharjan@microsoft.com> - 3.3.0-1
- Original version for CBL-Mariner. License Verified.
