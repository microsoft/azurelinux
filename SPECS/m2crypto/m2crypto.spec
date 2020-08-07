%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           m2crypto
Version:        0.35.2
Release:        8%{?dist}
Summary:        Crypto and SSL toolkit for Python
Group:          Development/Languages/Python
License:        MIT
URL:            https://pypi.python.org/pypi/M2Crypto
Source0:        https://files.pythonhosted.org/packages/74/18/3beedd4ac48b52d1a4d12f2a8c5cf0ae342ce974859fba838cbbc1580249/M2Crypto-0.35.2.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  python2-devel
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  python-setuptools
BuildRequires:  python-typing
BuildRequires:  swig
Requires:       openssl >= 1.1.1g-6
Requires:       python-typing
Requires:       python2

%description
M2Crypto is a crypto and SSL toolkit for Python featuring the following:

RSA, DSA, DH, HMACs, message digests, symmetric ciphers (including
AES). SSL functionality to implement clients and servers. HTTPS
extensions to Python's httplib, urllib, and xmlrpclib. Unforgeable
HMAC'ing AuthCookies for web session management. FTP/TLS client and
server. S/MIME. ZServerSSL: A HTTPS server for Zope. ZSmime: An S/MIME
messenger for Zope.

%package -n     python3-m2crypto
Summary:        python3 version of Crypto and SSL toolkit
BuildRequires:  python3-devel
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-typing
BuildRequires:  python3-xml
Requires:       openssl >= 1.1.1g-6
Requires:       python3-typing
Requires:       python3

%description -n python3-m2crypto
Python 3 version.

%prep
%setup -q -n M2Crypto-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
CFLAGS="%{optflags}" python2 setup.py build
pushd ../p3dir
CFLAGS="%{optflags}" python3 setup.py build
popd

%install
rm -rf %{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENCE
%{python2_sitelib}/*

%files -n python3-m2crypto
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Wed Jul 29 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.35.2-8
-   Reverting previous patch - issue fixed in 'openssl' >= 1.1.1g-6.
*   Wed Jul 15 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.35.2-7
-   Adding a patch for deprecated 'TLSv1_method' function in OpenSSL.
*   Fri Jun 05 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.35.2-6
-   Add python-typing back.
*   Tue May 26 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.35.2-5
-   Adding the "%%license" macro.
*   Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 0.35.2-4
-   Renaming python-M2Crypto to m2crypto
*   Tue Apr 07 2020 Nicolas Ontiveros <niontive@microsoft.com> 0.35.2-3
-   Remove python-typing from build.
*   Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> 0.35.2-2
-   Add missing BuildRequires for swig.
*   Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> 0.35.2-1
-   Update to version 0.35.2. License verified.
*   Fri Mar 03 2020 Jon Slobodzian <joslobo@microsoft.com> 0.30.1-4
-   Replaced incorrect URL link (removed mismatched version specifier). Fixed Source URL. Verified license.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.30.1-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Dec 03 2018 Ashwin H <ashwinh@vmware.com> 0.30.1-2
-   Add %check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.30.1-1
-   Update to version 0.30.1
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.26.0-2
-   Remove BuildArch
*   Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> 0.26.0-1
-   Initial packaging
