Summary:        Measures number of Terminal column cells of wide-character codes.
Name:           python-wcwidth
Version:        0.2.6
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/wcwidth
Source0:        https://github.com/jquast/wcwidth/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
This Library is mainly for those implementing a Terminal Emulator, or programs that carefully produce output to be interpreted by one.

%package -n     python3-wcwidth
Summary:        python-wcwidth
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if %{with_check}
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-coverage
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-six
%endif

Requires:       python3

%description -n python3-wcwidth
This Library is mainly for those implementing a Terminal Emulator, or programs that carefully produce output to be interpreted by one.

%prep
%autosetup -n wcwidth-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install \
    more-itertools \
    pluggy
# note tox should have been preferred but unfortunately tox.ini is set to only support python up to 3.8 => no tests will then be executed
# => stick with pytest which has a problem with test_package_version (version is correct but test stil throw an error)
pytest3 -vv tests -k "not test_package_version"

%files -n python3-wcwidth
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.2.6-1
- Auto-upgrade to 0.2.6 - Azure Linux 3.0 - package upgrades

* Fri Mar 25 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 0.2.5-1
- Upgrade to  0.2.5

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.1.7-5
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.1.7-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.1.7-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.1.7-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.1.7-1
- Initial packaging for Photon
