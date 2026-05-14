Summary:        Enable python source code refactoring through AST modifications
Name:           python-google-pasta
Version:        0.2.0
Release:        2%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
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
BuildRequires:  python3-pip
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
pip3 install pytest
# Exclude PrefixSuffixGoldenTest (51 failures from Python 3.12 AST changes)
# and fstring/inline tests that error due to same AST changes
python3 -m pytest -v -k "not (PrefixSuffixGoldenTest or fstring or test_inline_conditional_fails or test_inline_function_fails or test_inline_non_assign_fails or test_inline_non_constant_fails)"

%files -n python3-google-pasta
%doc README.md
%license LICENSE
%{python3_sitelib}/*


%changelog
* Wed Jun 17 2026 Kshitiz Godara <kgodara@microsoft.com> - 0.2.0-2
- Replace `setup.py test` with `pytest`; install the package via
  `pip3 install -e .` so the plugin entry point is discovered; exclude
  PrefixSuffixGoldenTest and fstring/inline tests that break on Python
  3.12 AST changes.
- Add python3-pip to BuildRequires.

* Wed Oct 26 2022 Riken Maharjan <rmaharjan@microsoft.com> - 0.2.0-1
- Original version for CBL-Mariner. License Verified.
