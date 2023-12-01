Summary:        Crypto and SSL toolkit for Python
Name:           m2crypto
Version:        0.38.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/M2Crypto
Source0:        https://files.pythonhosted.org/packages/2c/52/c35ec79dd97a8ecf6b2bbd651df528abb47705def774a4a15b99977274e8/M2Crypto-%{version}.tar.gz
Patch0:         0001-skip-test_tls1_nok-which-cant-be-run-in-FIPS.patch
Patch1:         CVE-2020-25657.patch

%description
M2Crypto is a crypto and SSL toolkit for Python

%package -n     python3-m2crypto
Summary:        Crypto and SSL toolkit for Python
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  swig
Requires:       openssl >= 1.1.1g-6
Requires:       python3
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description -n python3-m2crypto
M2Crypto is a crypto and SSL toolkit for Python featuring the following:

RSA, DSA, DH, HMACs, message digests, symmetric ciphers (including
AES). SSL functionality to implement clients and servers. HTTPS
extensions to Python's httplib, urllib, and xmlrpclib. Unforgeable
HMAC'ing AuthCookies for web session management. FTP/TLS client and
server. S/MIME. ZServerSSL: A HTTPS server for Zope. ZSmime: An S/MIME
messenger for Zope.

%prep
%autosetup -n M2Crypto-%{version} -p1

%build
%py3_build

%install
%py3_install

%check
pip3 install parameterized
#Testing: MiscSSLClientTestCase failing with SSLError not raised
%python3 setup.py test

%files -n python3-m2crypto
%defattr(-,root,root)
%license LICENCE
%{python3_sitelib}/*

%changelog
* Tue Aug 16 2022 Muhammad Falak <mwani@microsoft.com> - 0.38.0-3
- Patch CVE-2020-25657

* Fri Feb 11 2022 Muhammad Falak <mwani@microsoft.com> - 0.38.0-2
- Introduce patch to skip tests which can not run on FIPS mode & TLS1

* Wed Feb 02 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 0.38.0-1
- Update to version v0.38.0
- Added parameterized as BR and pip install in check section.

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.35.2-9
- Add license to python3 package
- Remove python3-typing requirement
- Remove python2 package
- Lint spec

* Wed Jul 29 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.35.2-8
- Reverting previous patch - issue fixed in 'openssl' >= 1.1.1g-6.

* Wed Jul 15 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.35.2-7
- Adding a patch for deprecated 'TLSv1_method' function in OpenSSL.

* Fri Jun 05 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.35.2-6
- Add python-typing back.

* Tue May 26 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.35.2-5
- Adding the "%%license" macro.

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.35.2-4
- Renaming python-M2Crypto to m2crypto

* Tue Apr 07 2020 Nicolas Ontiveros <niontive@microsoft.com> - 0.35.2-3
- Remove python-typing from build.

* Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> - 0.35.2-2
- Add missing BuildRequires for swig.

* Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> - 0.35.2-1
- Update to version 0.35.2. License verified.

* Fri Mar 03 2020 Jon Slobodzian <joslobo@microsoft.com> - 0.30.1-4
- Replaced incorrect URL link (removed mismatched version specifier). Fixed Source URL. Verified license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.30.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Dec 03 2018 Ashwin H <ashwinh@vmware.com> - 0.30.1-2
- Add %check

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 0.30.1-1
- Update to version 0.30.1

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> - 0.26.0-2
- Remove BuildArch

* Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> - 0.26.0-1
- Initial packaging
