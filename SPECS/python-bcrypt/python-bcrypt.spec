%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-bcrypt
Version:        3.1.6
Release:        4%{?dist}
Summary:        Good password hashing for your software and your servers.
License:        ASL 2.0
Group:          Development/Languages/Python
Url:            https://github.com/pyca/bcrypt/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/ce/3a/3d540b9f5ee8d92ce757eebacf167b9deedb8e30aedec69a2a072b2399bb/bcrypt-%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-cffi
BuildRequires:  python-xml
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cffi
BuildRequires:  python3-xml
Requires:       python2
Requires:       python2-libs


%description
Good password hashing for your software and your servers.

%package -n     python3-bcrypt
Summary:        python-bcrypt
Requires:       python3
Requires:       python3-libs

%description -n python3-bcrypt
Python 3 version.

%prep
%setup -n bcrypt-%{version}
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

%files
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-bcrypt
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:21:26 PST 2020 Nick Samson <nisamson@microsoft.com> - 3.1.6-4
- Added %%license line automatically

*   Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 3.1.6-3
-   Verified License. Fixed Source0 link. Fixed URL. Removed sha1.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.1.6-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 3.1.6-1
-   Initial packaging for Photon
