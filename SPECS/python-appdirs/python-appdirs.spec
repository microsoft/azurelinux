Summary:        Python 3 compatibility utilities
Name:           python-appdirs
Version:        1.4.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/appdirs
Source0:        https://github.com/ActiveState/appdirs/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
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
* Fri Feb 04 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.4.4-1
- Upgrade to latest upstream release version
- Use github release tarball

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.4.3-5
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.4.3-4
- Added %%license line automatically
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jun 22 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.4.3-3
- Changes to check section

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.4.3-2
- Change python to python2

* Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> - 1.4.3-1
- Create appdirs 1.4.3
