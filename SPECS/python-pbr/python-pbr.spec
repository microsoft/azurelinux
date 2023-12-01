Summary:        Python Build Reasonableness
Name:           python-pbr
Version:        5.8.1
Release:        4%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://docs.openstack.org/developer/pbr/
Source0:        https://pypi.io/packages/source/p/pbr/pbr-%{version}.tar.gz
Patch0:         disable-test-wsgi.patch
Patch1:         test-pin-sphinx.patch
BuildArch:      noarch

%description
A library for managing setuptools packaging needs in a consistent manner.

%package -n     python3-pbr
Summary:        Python Build Reasonableness
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
%if %{with_check}
BuildRequires:  git
BuildRequires:  gnupg2
BuildRequires:  python3-pip
%endif

%description -n python3-pbr
A library for managing setuptools packaging needs in a consistent manner.

%prep
%autosetup -p 1 -n pbr-%{version}

%build
export SKIP_PIP_INSTALL=1
%py3_build

%install
%py3_install
ln -s pbr %{buildroot}/%{_bindir}/pbr3

%check
pip3 install 'tox>=3.27.1,<4.0.0'
tox -e py%{python3_version_nodots}

%files -n python3-pbr
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{_bindir}/pbr
%{_bindir}/pbr3
%{python3_sitelib}/pbr-%{version}-*.egg-info
%{python3_sitelib}/pbr

%changelog
* Fri May 19 2023 Olivia Crain <oliviacrain@microsoft.com> - 5.8.1-4
- Add patch to pin version of sphinx used in tests to a known compatible version
- Remove check-time install of packages that should be handled by tox
- Use SPDX license expression in license tag

* Fri Dec 16 2022 Sam Meluch <sammeluch@microsoft.com> - 5.8.1-3
- Update version of tox used for package tests

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 5.8.1-2
- Use `py%{python3_version_nodots}` instead of harcoding `py39`

* Thu Feb 10 2022 Muhammad Falak <mwani@microsoft.com> - 5.8.1-1
- Bump version to 5.8.1
- Use `tox` instead of `setup.py test` to enable ptest

* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 5.1.2-4
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 5.1.2-3
- Remove python2 package
- Lint spec

* Thu Apr 16 2020 Nicolas Ontiveros <niontive@microsoft.com> - 5.1.2-2
- Use gnupg2 in BR.

* Wed Mar 18 2020 Paul Monson <paulmon@microsoft.com> - 5.1.2-1
- Update to version 5.1.2.  License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.2.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jan 16 2019 Tapas Kundu <tkundu@vmware.com> - 4.2.0-2
- Disabled the make check as the requirements can not be fulfilled

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 4.2.0-1
- Update to version 4.2.0

* Wed Jul 19 2017 Divya Thaluru <dthaluru@vmware.com> - 2.1.0-5
- Fixed make check failure

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.1.0-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.1.0-3
- Create pbr3 script

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.1.0-2
- Fix arch

* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.1.0-1
- Initial packaging for Photon
