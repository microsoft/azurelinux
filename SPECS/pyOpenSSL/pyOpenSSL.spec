%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Python wrapper module around the OpenSSL library
Name:           pyOpenSSL
Version:        18.0.0
Release:        6%{?dist}
Url:            https://github.com/pyca/pyopenssl
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/source/p/pyOpenSSL/%{name}-%{version}.tar.gz
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python-cryptography
BuildRequires:  python-ipaddress
BuildRequires:  python-six
BuildRequires:  python-pycparser
BuildRequires:  python-cffi
BuildRequires:  openssl
BuildRequires:  python-idna
BuildRequires:  python-pyasn1
BuildRequires:  python-setuptools
BuildRequires:  python-packaging
BuildRequires:  python-enum34
BuildRequires:  python-asn1crypto
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-cryptography
BuildRequires:  python3-six
BuildRequires:  python3-pycparser
BuildRequires:  python3-cffi
BuildRequires:  python3-idna
BuildRequires:  python3-pyasn1
BuildRequires:  python3-six
BuildRequires:  python3-packaging
BuildRequires:  python3-asn1crypto
%endif
Requires:       python2
Requires:       python2-libs
Requires:       python-cryptography
Requires:       python-ipaddress
Requires:       python-six

BuildArch:      noarch

%description
High-level wrapper around a subset of the OpenSSL library.

%package -n     python3-pyOpenSSL
Summary:        Python 3 version
Requires:       python3
Requires:       python3-libs
Requires:       python3-cryptography
Requires:       python3-six

%description -n python3-pyOpenSSL
Python 3 version.

%prep
%setup -q
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
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 pretend
$easy_install_2 flaky
$easy_install_2 pytest
PATH=%{buildroot}%{_bindir}:${PATH} \
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python2_sitelib} \
    pytest

pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pretend
$easy_install_3 flaky
$easy_install_3 pytest
PATH=%{buildroot}%{_bindir}:${PATH} \
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python3_sitelib} \
    pytest
popd


%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-pyOpenSSL
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:21:13 PST 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 18.0.0-5
-   Renaming python-pyOpenSSL to pyOpenSSL
*   Tue Apr 07 2020 Nicolas Ontiveros <niontive@microsoft.com> 18.0.0-4
-   Remove python-enum from build requires.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 18.0.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Jan 11 2019 Tapas Kundu <tkundu@vmware.com> 18.0.0-2
-   Fix makecheck
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.0.0-1
-   Update to version 18.0.0
*   Thu Jun 14 2018 Tapas Kundu <tkundu@vmware.com> 17.2.0-2
-   Added memory fix for X509StoreContext Class.
*   Mon Aug 14 2017 Xiaolin Li <xiaolinl@vmware.com> 17.2.0-1
-   Updated to version 17.2.0 and fixed make check.
*   Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 16.2.0-5
-   Fixed runtime dependencies
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-4
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.2.0-3
-   Use python2 explicitly
*   Tue Feb 21 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-2
-   Add Requires for python-enum and python-ipaddress
*   Tue Feb 14 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-1
-   Initial packaging for Photon
