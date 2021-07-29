%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        file locking module
Name:           python-lockfile
Version:        0.12.2
Release:        5%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://github.com/openstack/pylockfile
Source0:        https://pypi.python.org/packages/source/l/lockfile/lockfile-%{version}.tar.gz
%define sha1    lockfile=c2ac46e48585e5f8f8d57ccc55ca83faa8b53b86

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildArch:      noarch

%description
The lockfile package exports a LockFile class which provides a simple API for locking files.
Unlike the Windows msvcrt.locking function, the fcntl.lockf and flock functions, and the
deprecated posixfile module, the API is identical across both Unix (including Linux and Mac)
and Windows platforms. The lock mechanism relies on the atomic nature of the link (on Unix)
and mkdir (on Windows) system calls. An implementation based on SQLite is also provided, more
as a demonstration of the possibilities it provides than as production-quality code.

%package -n     python3-lockfile
Summary:        Python Build Reasonableness
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pbr

%description -n python3-lockfile
The lockfile package exports a LockFile class which provides a simple API for locking files.
Unlike the Windows msvcrt.locking function, the fcntl.lockf and flock functions, and the
deprecated posixfile module, the API is identical across both Unix (including Linux and Mac)
and Windows platforms. The lock mechanism relies on the atomic nature of the link (on Unix)
and mkdir (on Windows) system calls. An implementation based on SQLite is also provided, more
as a demonstration of the possibilities it provides than as production-quality code.

%prep
%setup -q -n lockfile-%{version}
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

%files
%defattr(-,root,root)
%license LICENSE
%doc ACKS AUTHORS LICENSE PKG-INFO README.rst RELEASE-NOTES doc/
%{python2_sitelib}/lockfile-%{version}-*.egg-info
%{python2_sitelib}/lockfile

%files -n python3-lockfile
%defattr(-,root,root)
%doc ACKS AUTHORS LICENSE PKG-INFO README.rst RELEASE-NOTES doc/
%{python3_sitelib}/lockfile-%{version}-*.egg-info
%{python3_sitelib}/lockfile

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.12.2-5
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.12.2-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.12.2-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.12.2-2
-   Fix arch
*   Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.12.2-1
-   Initial packaging for Photon
