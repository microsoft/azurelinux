Summary:        The stand-alone implementation of several NumPy dtype extensions used in machine learning libraries
Name:           python-ml-dtypes
Version:        0.2.0
Release:        1%{?dist}
License:        ASL-2.0 and MPL-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/ml-dtypes/
Source0:        https://files.pythonhosted.org/packages/source/m/ml_dtypes/ml_dtypes-%{version}.tar.gz
Source1:        ml_dtypes-%{version}-submodules.tar.gz
BuildRequires:  python3-numpy
BuildRequires:  python3-pybind11
%if 0%{?with_check}
BuildRequires:  python3-pip
%endif

%description
ml_dtypes is a stand-alone implementation of several NumPy dtype extensions used in machine learning libraries.

%package -n     python3-ml-dtypes
Summary:        THe stand-alone implementation of several NumPy dtype extensions.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3

%description -n python3-ml-dtypes
ml_dtypes is a stand-alone implementation of several NumPy dtype extensions used in machine learning libraries.

%prep
%autosetup -a 1 -n ml_dtypes-%{version}


%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-ml-dtypes
%defattr(-,root,root)
%license LICENSE
%license LICENSE.eigen
%{python3_sitelib}/*

%changelog
* Tue Mar 12 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.2.0-1
- Original version for CBL-Mariner. License Verified.

