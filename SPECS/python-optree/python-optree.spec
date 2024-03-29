%global debug_package %{nil}
Summary:        Optimized PyTree Utilities
Name:           python-optree
Version:        0.11.0
Release:        1%{?dist}
License:        ASL-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/optree/
Source0:        https://files.pythonhosted.org/packages/source/o/optree/optree-%{version}.tar.gz

%description
A PyTree is a recursive structure that can be an arbitrarily nested Python container (e.g., tuple, list, dict, OrderedDict, NamedTuple, etc.) or an opaque Python object.

%package -n     python3-optree
Summary:        Optimized PyTree Utilities.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  cmake
BuildRequires:  pybind11-devel
BuildRequires:  python3-pybind11
Requires:       python3

%description -n python3-optree
A PyTree is a recursive structure that can be an arbitrarily nested Python container (e.g., tuple, list, dict, OrderedDict, NamedTuple, etc.) or an opaque Python object.

%prep
%autosetup -a 0 -n optree-%{version}


%build
%py3_build

%install
%py3_install


%files -n python3-optree
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Mar 29 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.11.0-1
- Original version for Azure Linux.
- License Verified.

