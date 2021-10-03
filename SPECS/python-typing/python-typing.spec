Summary:        Type Hints for Python
Name:           python-typing
Version:        3.6.6
Release:        4%{?dist}
License:        Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://pypi.org/project/typing
Source0:        https://files.pythonhosted.org/packages/bf/9b/2bf84e841575b633d8d91ad923e198a415e3901f228715524689495b4317/typing-%{version}.tar.gz

%description
Typing defines a standard notation for Python function and variable type annotations.

%package -n     python3-typing
Summary:        Type Hints for Python
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-typing
Typing defines a standard notation for Python function and variable type annotations. The notation can be used for documenting code in a concise,
standard format, and it has been designed to also be used by static and runtime type checkers, static analyzers, IDEs and other tools.

%prep
%autosetup -q -n typing-%{version}

%build
%py3_build

%install
%py3_install

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python3 python3/test_typing.py

%files -n python3-typing
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 3.6.6-4
- Add license to python3 package
- Remove python2 package
- Lint spec

* Fri Jun 05 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6.6-3
- License verified.
- Added license references.
- Removed "sha1" macros.
- Updated "URL" and "Source0" tags.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.6.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 3.6.6-1
- Update to version 3.6.6

* Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> - 3.6.1-3
- Adding python3 version.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 3.6.1-2
- Use python2 explicitly

* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> - 3.6.1-1
- Initial
