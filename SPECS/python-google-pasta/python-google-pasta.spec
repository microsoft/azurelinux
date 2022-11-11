Summary:        Enable python source code refactoring through AST modifications
Name:           python-google-pasta
Version:        0.2.0
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/google/pasta/
Source0:        https://github.com/google/pasta/archive/v%{version}.tar.gz#/google-pasta-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel

%description
Enable python source code refactoring through AST modifications.

%package -n     python3-google-pasta
Summary:        Enable python source code refactoring through AST modifications
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
Requires:       python3-six

%description -n python3-google-pasta
Enable python source code refactoring through AST modifications.

%prep
%autosetup -n pasta-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files -n python3-google-pasta
%doc README.md
%license LICENSE
%{python3_sitelib}/*


%changelog
* Wed Oct 26 2022 Riken Maharjan <rmaharjan@microsoft.com> - 0.2.0-1
- Original version for CBL-Mariner. License Verified.
