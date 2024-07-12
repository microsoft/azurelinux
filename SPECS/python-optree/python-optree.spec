%global debug_package %{nil}
Summary:        Optimized PyTree Utilities
Name:           python-optree
Version:        0.11.0
Release:        2%{?dist}
License:        ASL-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/optree/
Source0:        https://github.com/metaopt/optree/archive/refs/tags/v%{version}.tar.gz#/optree-%{version}.tar.gz
BuildRequires:  python3-pip

%description
A PyTree is a recursive structure that can be an arbitrarily nested Python container (e.g., tuple, list, dict, OrderedDict, NamedTuple, etc.) or an opaque Python object.

%package -n     python3-optree
Summary:        Optimized PyTree Utilities.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  build-essential
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  python3-typing-extensions
BuildRequires:  python3-pybind11
BuildRequires:  python3-Cython
BuildRequires:  python3-libs
BuildRequires:  ca-certificates
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-typing-extensions

%description -n python3-optree
A PyTree is a recursive structure that can be an arbitrarily nested Python container (e.g., tuple, list, dict, OrderedDict, NamedTuple, etc.) or an opaque Python object.

%prep
%autosetup -a 0 -n optree-%{version}


%build
python3 setup.py bdist_wheel

%install
python3 -m pip install -I dist/optree-0.11.0-cp312-cp312-linux_x86_64.whl --root %{buildroot} --no-deps --no-index

%check
pip3 install pytest
pip3 install -r requirements.txt
pushd /
python3 -c "import optree; optree.tree_map(lambda x: x , ())"
popd


%files -n python3-optree
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed July 10 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.11.0-2
- Add missing runtime dependency python3-typing-extensions.
- Add missing build dependency gcc. 

* Fri Mar 29 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.11.0-1
- Original version for Azure Linux.
- License Verified.

