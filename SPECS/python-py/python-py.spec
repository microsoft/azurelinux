%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Python development support library
Name:           python-py
Version:        1.10.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/pytest-dev/py
# Must use PyPI sources. Building from GitHub's release sources fails with a message to use PyPI.
Source0:        https://files.pythonhosted.org/packages/0d/8c/50e9f3999419bb7d9639c37e83fa9cdcf0f601a9d407162d6c37ad60be71/py-%{version}.tar.gz

BuildRequires:  python-setuptools
BuildRequires:  python-setuptools_scm
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
The py lib is a Python development support library featuring the following tools and modules:

py.path: uniform local and svn path objects
py.apipkg: explicit API control and lazy-importing
py.iniconfig: easy parsing of .ini files
py.code: dynamic code generation and introspection

%package -n     python3-py
Summary:        Python development support library

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description -n python3-py

Python 3 version.

%prep
%autosetup -n py-%{version}
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
#python-py and python-pytest have circular dependency. Hence not adding tests
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-py
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Dec 22 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.0-1
- Updated to version 1.10.0 to fix CVE-2020-29651.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.6.0-4
- Added %%license line automatically

* Mon Apr 20 2020 Eric Li <eli@microsoft.com> 1.6.0-3
- Update Source0:, add #Source0:, and delete sha1. License verified

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.6.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 1.6.0-1
- Updated to versiob 1.6.0

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.4.33-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.33-2
- Use python2_sitelib

* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.33-1
- Initial
