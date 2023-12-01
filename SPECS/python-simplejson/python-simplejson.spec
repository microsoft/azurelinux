Summary:        Simple, fast, extensible JSON encoder/decoder for Python.
Name:           python-simplejson
Version:        3.17.6
Release:        1%{?dist}
License:        MIT OR AFL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/simplejson
Source0:        https://pypi.python.org/packages/source/s/simplejson/simplejson-%{version}.tar.gz
BuildRequires:  python3-devel

%description
Simple, fast, extensible JSON encoder/decoder for Python.

%package -n     python3-simplejson
Summary:        Simple, fast, extensible JSON encoder/decoder for Python.
Requires:       python3

%description -n python3-simplejson
simplejson is a simple, fast, complete, correct and extensible JSON <http://json.org> encoder and decoder for Python 2.5+ and Python 3.3+.
It is pure Python code with no dependencies, but includes an optional C extension for a serious speed boost.

%prep
%autosetup -n simplejson-%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-simplejson
%defattr(-,root,root,-)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Tue Mar 29 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.17.6-1
- Upgrade to latest upstream version

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.17.0-3
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.17.0-2
- Added %%license line automatically

* Thu Mar 19 2020 Paul Monson <paulmons@microsoft.com> - 3.17.0-1
- Update to version 3.17.0. Fix source0 URL. Fix license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.16.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 3.16.1-1
- Update to version 3.16.1

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 3.10.0-2
- Use python2 explicitly

* Wed Mar 01 2017 Xiaolin Li <xiaolinl@vmware.com> - 3.10.0-1
- Initial packaging for Photon
