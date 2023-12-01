Summary:        Python development support library
Name:           python-py
Version:        1.10.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/pytest-dev/py
# Must use PyPI sources. Building from GitHub's release sources fails with a message to use PyPI.
Source0:        https://files.pythonhosted.org/packages/0d/8c/50e9f3999419bb7d9639c37e83fa9cdcf0f601a9d407162d6c37ad60be71/py-%{version}.tar.gz
BuildArch:      noarch

%description
Python development support library

%package -n     python3-py
Summary:        Python development support library
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-py
The py lib is a Python development support library featuring the following tools and modules:

py.path: uniform local and svn path objects
py.apipkg: explicit API control and lazy-importing
py.iniconfig: easy parsing of .ini files
py.code: dynamic code generation and introspection

%prep
%autosetup -n py-%{version}

%build
%py3_build

%install
%py3_install

%check
#python-py and python-pytest have circular dependency. Hence not adding tests
%make_build -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files -n python3-py
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed Feb 16 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.10.0-3
- Fix accidental double-packaging of python3 subpackage in main package

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.10.0-2
- Add license to python3 package
- Remove python2 package
- Lint spec

* Tue Dec 22 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.0-1
- Updated to version 1.10.0 to fix CVE-2020-29651.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.6.0-4
- Added %%license line automatically

* Mon Apr 20 2020 Eric Li <eli@microsoft.com> - 1.6.0-3
- Update Source0:, add #Source0:, and delete sha1. License verified

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.6.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> - 1.6.0-1
- Updated to versiob 1.6.0

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.4.33-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.4.33-2
- Use python2_sitelib

* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.4.33-1
- Initial
