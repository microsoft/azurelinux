Summary:        Virtual Python Environment builder
Name:           python-virtualenv
Version:        20.14.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/virtualenv
Source0:        https://files.pythonhosted.org/packages/4a/c3/04f361a90ed4e6b3f3f696d61db5c786eaa741d2a6c125bc905b8a1c0200/virtualenv-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
virtualenv is a tool to create isolated Python environment.

%package -n     python3-virtualenv
Summary:        Virtual Python Environment builder
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-xml
BuildRequires:  python3-wheel

%if %{with_check}
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-filelock
Requires:       python3-platformdirs = 2.0.0
Requires:       python3-distlib < 1
Provides:       %{name}-doc = %{version}-%{release}

%description -n python3-virtualenv
virtualenv is a tool to create isolated Python environment.

%prep
%autosetup -n virtualenv-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install 'tox>=3.27.1,<4.0.0'
tox -e py

%files -n python3-virtualenv
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/virtualenv

%changelog
* Wed Dec 21 2022 Riken Maharjan <rmaharjan@microsoft.com> - 20.14.0-3
- Add missing runtime dependencies

* Fri Dec 16 2022 Sam Meluch <sammeluch@microsoft.com> - 20.14.0-2
- Update version of tox used for package tests

* Fri Mar 25 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 20.14.0-1
- Upgrade to 20.14.0

* Tue Feb 08 2022 Muhammad Falak <mwani@microsoft.com> - 16.0.0-8
- Add an explicit BR on `python3-pip` to enable ptest

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 16.0.0-7
- Add license, virtualenv binary to python3 package
- Remove python2 package
- Lint spec

* Mon Feb 15 2021 Henry Li <lihl@microsoft.com> - 16.0.0-6
- Provides python-virtualenv-doc

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 16.0.0-5
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 16.0.0-4
- Renaming python-pytest to pytest

* Thu Apr 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 16.0.0-3
- License verified.
- Fixed 'Source0' tag.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 16.0.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 16.0.0-1
- Update to version 16.0.0

* Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 15.1.0-1
- Initial version of python-virtualenv package for Photon.
