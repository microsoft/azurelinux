%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        PyNaCl is a Python binding to libsodium
Name:           python-pynacl
Version:        1.3.0
Release:        6%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/pyca/pynacl
# The official source is under https://github.com/pyca/pynacl/archive/1.3.0.tar.gz.
# Source to be fixed as part of https://microsoft.visualstudio.com/OS/_workitems/edit/25936171.
Source0:        https://files.pythonhosted.org/packages/61/ab/2ac6dea8489fa713e2b4c6c5b549cc962dd4a842b5998d9e80cf8440b7cd/PyNaCl-%{version}.tar.gz
BuildRequires:  python-cffi
BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python-xml
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python3
BuildRequires:  python3-cffi
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-xml
Requires:       python2
Requires:       python2-libs

%description
Good password hashing for your software and your servers.

%package -n     python3-pynacl
Summary:        python3-pynacl
Requires:       python3
Requires:       python3-libs

%description -n python3-pynacl
Python 3 version.

%prep
%setup -q -n PyNaCl-%{version}
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
# libsodium tests are ran as part of the build phase
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-pynacl
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sun Dec 05 2021 Thomas Crain <thcrain@microsoft.com> - 1.3.0-6
- Enable package tests

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.3.0-5
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.3.0-4
- Renaming python-PyNaCl to python-pynacl

* Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.0-3
- Fixed 'Source0' and 'URL' tags.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.3.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

*   Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 1.3.0-1
-   Initial packaging for Photon
