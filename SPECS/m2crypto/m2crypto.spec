
%global snapdate 20240613
%global commit 3156614a94a4767ee563530983cba87cf2aad193
%global shortcommit %(c=%{commit}; echo ${c:0:7})


Summary:        Crypto and SSL toolkit for Python
Name:           m2crypto
Version:        0.41.0%{?snapdate:^git%{snapdate}.%{shortcommit}}
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://gitlab.com/m2crypto/m2crypto
Source:         %{url}/-/archive/%{commit}/%{name}-%{commit}.tar.gz
Patch0:         0001-Don-t-expect-test_mkcert-to-fail-on-32-bit-Fedora-sp.patch

%description
M2Crypto is a crypto and SSL toolkit for Python

%package -n     python3-m2crypto
Summary:        Crypto and SSL toolkit for Python
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  swig
BuildRequires:  pkgconfig
Requires:       openssl >= 1.1.1g-6
Requires:       python3
%if 0%{?with_check}
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
%autosetup -n %{?snapdate:%{name}-%{commit}}%{!?snapdate:M2Crypto-%{version}} -p1

# remove outdated generated files
rm -f src/M2Crypto/m2crypto.py src/SWIG/_m2crypto_wrap.c

%build
%set_build_flags
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

%py3_build

%install
%set_build_flags
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

%py3_install

%check
# FIXME: Make the tests pass on RHEL 9 again...
PYTHONPATH=%{buildroot}%{python3_sitearch} %{__python3} -munittest discover -v tests/ %{?rhel: || :}

%files -n python3-m2crypto
%defattr(-,root,root)
%doc CHANGES README.rst
%license LICENCE
%{python3_sitelib}/*

%changelog
* Mon Feb 24 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.41.0^git20240613.3156614-1
- Upgrade version to 0.41.0 post-release snapshot to support with Python 3.12
- Updated Source URL path and removed patches which are not applicable with 0.41.0 version

* Wed Jan 29 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 0.38.0-4
- Fix CVE-2019-11358

* Tue Aug 16 2022 Muhammad Falak <mwani@microsoft.com> - 0.38.0-3
- Patch CVE-2020-25657

* Fri Feb 11 2022 Muhammad Falak <mwani@microsoft.com> - 0.38.0-2
- Introduce patch to skip tests which can not run on FIPS mode & TLS1

* Wed Feb 02 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 0.38.0-1
- Update to version v0.38.0
- Added parameterized as BR and pip install in check section.

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.35.2-9
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
