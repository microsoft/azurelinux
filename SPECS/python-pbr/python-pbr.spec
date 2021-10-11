Summary:        Python Build Reasonableness
Name:           python-pbr
Version:        5.1.2
Release:        3%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://docs.openstack.org/developer/pbr/
Source0:        https://pypi.io/packages/source/p/pbr/pbr-%{version}.tar.gz
Patch0:         disable-test-wsgi.patch
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
easy_install_3=$(ls %{_bindir} |grep easy_install |grep 3)
$easy_install_3 coverage
$easy_install_3 hacking
$easy_install_3 mock
$easy_install_3 testrepository
$easy_install_3 testresources
$easy_install_3 testscenarios
$easy_install_3 virtualenv
$easy_install_3 wheel
%python3 setup.py test

%files -n python3-pbr
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{_bindir}/pbr
%{_bindir}/pbr3
%{python3_sitelib}/pbr-%{version}-*.egg-info
%{python3_sitelib}/pbr

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 5.1.2-3
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
