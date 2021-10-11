Summary:        Python 2 and 3 compatibility utilities
Name:           python-appdirs
Version:        1.4.3
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/appdirs
Source0:        https://pypi.python.org/packages/48/69/d87c60746b393309ca30761f8e2b49473d43450b150cb08f3c6df5c11be5/appdirs-%{version}.tar.gz
BuildArch:      noarch

%description
A small Python module for determining appropriate platform-specific dirs, e.g. a "user data dir".

%package -n     python3-appdirs
Summary:        Python 3 compatibility utilities
BuildRequires:  python3-devel
Requires:       python3

%description -n python3-appdirs
A small Python module for determining appropriate platform-specific dirs, e.g. a "user data dir".

%prep
%autosetup -n appdirs-%{version}

%build
%py3_build

%install
%py3_install

%check
cd test
PATH=%{buildroot}%{_bindir}:${PATH} \
 PYTHONPATH=%{buildroot}%{python3_sitelib} \
 %{python3} test_api.py

%files -n python3-appdirs
%defattr(-,root,root,-)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 1.4.3-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.4.3-4
- Added %%license line automatically
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jun 22 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.4.3-3
- Changes to check section

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.4.3-2
- Change python to python2

* Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> - 1.4.3-1
- Create appdirs 1.4.3
