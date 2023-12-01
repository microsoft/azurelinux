Summary:        Extensions to the standard Python datetime module
Name:           python-dateutil
Version:        2.7.3
Release:        5%{?dist}
License:        ASL 2.0 AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/python-dateutil
Source0:        https://files.pythonhosted.org/packages/a0/b0/a4e3241d2dee665fea11baec21389aec6886655cd4db7647ddf96c3fad15/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
The dateutil module provides powerful extensions to the datetime module available in the Python standard library.

%package -n     python3-dateutil
Summary:        Extensions to the standard Python datetime module
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-six

%description -n python3-dateutil
The dateutil module provides powerful extensions to the datetime module available in the Python standard library.

%prep
%autosetup -n python-dateutil-%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-dateutil
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.7.3-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.7.3-4
- Added %%license line automatically

* Thu Apr 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.3-3
- License verified.
- Fixed 'Source0' tag.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.7.3-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> - 2.7.3-1
- Updated to release 2.7.3

* Sun Jan 07 2018 Kumar Kaushik <kaushikk@vmware.com> - 2.6.1-1
- Initial packaging for photon.
