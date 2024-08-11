%global debug_package %{nil}
Summary:        Namex is a simple utility to separate the implementation of your Python package and its public API
Name:           python-namex
Version:        0.0.7
Release:        1%{?dist}
License:        ASL-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/namex/
Source0:        https://files.pythonhosted.org/packages/source/n/namex/namex-%{version}.tar.gz

%description
Namex is a simple utility to separate the implementation of your Python package and its public API.

%package -n     python3-namex
Summary:        The simple utility to separate Python package and its public API.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3

%description -n python3-namex
Namex is a simple utility to separate the implementation of your Python package and its public API.

%prep
%autosetup -a 0 -n namex-%{version}


%build
%py3_build

%install
%py3_install


%files -n python3-namex
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Thu Mar 28 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.0.7-1
- Original version for CBL-Mariner. 
- License Verified.
