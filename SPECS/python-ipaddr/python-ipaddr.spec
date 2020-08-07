%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-ipaddr
Version:        2.2.0
Release:        2%{?dist}
Url:            https://github.com/google/ipaddr-py
Summary:        Google's Python IP address manipulation library
License:        Apache2
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/i/ipaddr/ipaddr-%{version}.tar.gz
%define sha1    ipaddr=d2acca0d7eee9c21d103d11ddc1bd7a8cc9a5a27
#Patch0:         ipaddr-python3-compatibility.patch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
ipaddr.py is a library for working with IP addresses, both IPv4 and IPv6. It was developed by Google for internal use, and is now open source.

%package -n     python3-ipaddr
Summary:        python-ipaddr
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-ipaddr
Python 3 version.

%prep
%setup -q -n ipaddr-%{version}
#%patch0 -p1
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
python2 ipaddr_test.py
pushd ../p3dir
python3 ipaddr_test.py
popd

%files
%defattr(-,root,root)
%license COPYING
%{python2_sitelib}/*

%files -n python3-ipaddr
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.2.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
-   Added %%license line automatically
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.2.0-1
-   Update to version 2.2.0
*   Tue May 16 2017 Kumar Kaushik <kaushikk@vmware.com> 2.1.11-4
-   Adding python 3 support.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 2.1.11-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.11-2
-   GA - Bump release of all rpms
*   Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
