%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python PAM module using ctypes, py3/py2
Name:           python-pam
Version:        1.8.4
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/python-pam/
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.python.org/packages/source/p/python-pam/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
Python PAM module using ctypes, py3/py2.

%package -n     python3-pam
Summary:        python-pam
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description -n python3-pam

Python 3 version.

%prep
%setup -q -n python-pam-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-pam
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:21:23 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.8.4-2
- Added %%license line automatically

* Wed Mar 18 2020 Paul Monson <paulmon@microsoft.com> 1.8.4-1
- Update to version 1.8.4.  Source0 fixed. License verified.
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.8.2-3
- Initial CBL-Mariner import from Photon (license: Apache2).
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.2-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Mar 09 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.2-1
- Initial packaging for Photon
