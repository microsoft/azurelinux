%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python Build Reasonableness
Name:           python-pbr
Version:        5.1.2
Release:        2%{?dist}
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://docs.openstack.org/developer/pbr/
Source0:        https://pypi.io/packages/source/p/pbr/pbr-%{version}.tar.gz
Patch0:         disable-test-wsgi.patch
BuildRequires:  python-docutils
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0
%if %{with_check}
BuildRequires:  git
BuildRequires:  gnupg2
%endif
%endif
Requires:       python2
BuildArch:      noarch
%description
A library for managing setuptools packaging needs in a consistent manner.

%package -n     python3-pbr
Summary:        Python Build Reasonableness
Requires:       python3

%description -n python3-pbr
Python 3 version.

%prep
%setup -q -n pbr-%{version}
%patch0 -p1
rm -rf ../p3dir
cp -a . ../p3dir

%build
export SKIP_PIP_INSTALL=1
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/pbr %{buildroot}/%{_bindir}/pbr3
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%if 0
%check
ln -sfv /usr/bin/gpg2 /usr/bin/gpg
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 coverage
$easy_install_2 hacking
$easy_install_2 mock
$easy_install_2 testrepository
$easy_install_2 testresources
$easy_install_2 testscenarios
$easy_install_2 virtualenv
$easy_install_2 wheel
python2 setup.py test

pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 coverage
$easy_install_3 hacking
$easy_install_3 mock
$easy_install_3 testrepository
$easy_install_3 testresources
$easy_install_3 testscenarios
$easy_install_3 virtualenv
$easy_install_3 wheel
python3 setup.py test
popd

%endif

%files
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{_bindir}/pbr
%{python2_sitelib}/pbr-%{version}-*.egg-info
%{python2_sitelib}/pbr

%files -n python3-pbr
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{_bindir}/pbr3
%{python3_sitelib}/pbr-%{version}-*.egg-info
%{python3_sitelib}/pbr

%changelog
* Thu Apr 16 2020 Nicolas Ontiveros <niontive@microsoft.com> 5.1.2-2
- Use gnupg2 in BR.
* Wed Mar 18 2020 Paul Monson <paulmon@microsoft.com> 5.1.2-1
- Update to version 5.1.2.  License verified.
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.2.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).
* Wed Jan 16 2019 Tapas Kundu <tkundu@vmware.com> 4.2.0-2
- Disabled the make check as the requirements can not be fulfilled
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 4.2.0-1
- Update to version 4.2.0
* Wed Jul 19 2017 Divya Thaluru <dthaluru@vmware.com> 2.1.0-5
- Fixed make check failure
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.0-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.0-3
- Create pbr3 script
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-2
- Fix arch
* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.0-1
- Initial packaging for Photon
