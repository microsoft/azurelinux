%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.
Name:           python-pyvmomi
Version:        6.7.3
Release:        2%{?dist}
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://pypi.python.org/pypi/pyvmomi
#Source0:       https://github.com/vmware/pyvmomi/archive/6.7.3.tar.gz
Source0:        https://github.com/vmware/pyvmomi/archive/python-pyvmomi-6.7.3.tar.gz
Patch0:         python-pyvmomi-make-check-fix.patch
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python-xml
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.

%package -n     python3-pyvmomi
Summary:        python-pyvmomi

Requires:       python3
Requires:       python3-libs
%description -n python3-pyvmomi
Python 3 version.

%prep
%setup -q -n pyvmomi-%{version}
%patch0 -p1
%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root)
%license LICENSE.txt
%{python2_sitelib}/*

%files -n python3-pyvmomi
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:20:41 PST 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

* Wed Mar 18 2020 Paul Monson <paulmon@microsoft.com> 6.7.3-1
- Update to 6.7.3.  Fix Source0. Fix license.
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.2018.9-1
- Initial CBL-Mariner import from Photon (license: Apache2).
* Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> 6.7.0.2018.9-2
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 6.7.0.2018.9-1
- Update to version 6.7.0.2018.9
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 6.5-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 6.5-1
- Initial packaging for Photon.
