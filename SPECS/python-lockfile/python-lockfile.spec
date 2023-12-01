Summary:        File locking module
Name:           python-lockfile
Version:        0.12.2
Release:        6%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/openstack/pylockfile
Source0:        https://pypi.python.org/packages/source/l/lockfile/lockfile-%{version}.tar.gz
BuildArch:      noarch

%description
File locking module

%package -n     python3-lockfile
Summary:        File locking module
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-lockfile
The lockfile package exports a LockFile class which provides a simple API for locking files.
Unlike the Windows msvcrt.locking function, the fcntl.lockf and flock functions, and the
deprecated posixfile module, the API is identical across both Unix (including Linux and Mac)
and Windows platforms. The lock mechanism relies on the atomic nature of the link (on Unix)
and mkdir (on Windows) system calls. An implementation based on SQLite is also provided, more
as a demonstration of the possibilities it provides than as production-quality code.

%prep
%autosetup -n lockfile-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-lockfile
%defattr(-,root,root)
%license LICENSE
%doc ACKS AUTHORS PKG-INFO README.rst RELEASE-NOTES doc/
%{python3_sitelib}/lockfile-%{version}-*.egg-info
%{python3_sitelib}/lockfile

%changelog
* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.12.2-6
- Add license to python3 package, fix summary
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.12.2-5
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.12.2-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.12.2-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 0.12.2-2
- Fix arch

* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.12.2-1
- Initial packaging for Photon
