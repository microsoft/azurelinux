Summary:        Crypto and SSL toolkit for Python
Name:           m2crypto
Version:        0.48.0
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/M2Crypto
Source0:        https://files.pythonhosted.org/packages/89/7a/06ed5c66d63506bc77a7823d56e5e6b4ad3143f3fca2337c46d8b2c191f5/m2crypto-%{version}.tar.gz

%description
M2Crypto is a crypto and SSL toolkit for Python

%package -n     python3-m2crypto
Summary:        Crypto and SSL toolkit for Python
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  swig
Requires:       openssl >= 1.1.1g-6
Requires:       python3
Requires:       python3-packaging
%if 0%{?with_check}
BuildRequires:  openssl
BuildRequires:  python3-pytest
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
%autosetup -n m2crypto-%{version}

%build
%py3_build

%install
%py3_install

%check
# setuptools >= 72 removed the 'setup.py test' command, so run the suite
# directly with pytest. Tests import M2Crypto from the installed buildroot.
# Azure Linux's OpenSSL 3.x keeps MD5 in the "legacy" provider, which is not
# loaded by default; enable it for the test run so the HMAC-MD5 assertion in
# tests/test_evp.py (EVPTestCase.test_hmac) runs and passes unmodified.
cat > %{_builddir}/openssl-legacy.cnf <<'EOF'
openssl_conf = openssl_init
[openssl_init]
providers = provider_sect
[provider_sect]
default = default_sect
legacy = legacy_sect
[default_sect]
activate = 1
[legacy_sect]
activate = 1
EOF
OPENSSL_CONF=%{_builddir}/openssl-legacy.cnf \
    PYTHONPATH=%{buildroot}%{python3_sitelib} %python3 -m pytest -v tests/

%files -n python3-m2crypto
%defattr(-,root,root)
%license LICENSES/BSD-2-Clause.txt
%{python3_sitelib}/*

%changelog
* Tue Jun 30 2026 Sumit Jena <v-sumitjena@microsoft.com> - 0.48.0-1
- Upgrade to version 0.48.0
- Drop CVE-2020-25657.patch (fixed upstream) and CVE-2019-11358.patch (bundled jQuery doc no longer shipped)
- Drop FIPS TLS1 test-skip patch (upstream tests now handle OpenSSL 3.x)
- Drop the Python 3.12 'six'/'asyncore' workarounds and the network 'pip3 install parameterized'; 0.48.0 no longer needs them, so %%check runs the full suite without tolerating failure
- Enable the OpenSSL legacy provider during %%check so the HMAC-MD5 test runs unmodified
- License verified as BSD-2-Clause

* Wed Jun 17 2026 Kshitiz Godara <kgodara@microsoft.com> - 0.38.0-5
- Replace deprecated `setup.py test` with `pytest` and document the
  two real upstream Python-3.12 incompatibilities (vendored
  `six.moves` importer + removed `asyncore` stdlib module) that
  prevent the test suite from collecting. Continue to tolerate
  failure (`|| :`) until this package is rebased on M2Crypto >= 0.40.
- Replace the bundled `M2Crypto/six.py` in the buildroot with the
  system `six` so that the pytest run gets past the first import
  failure and surfaces the real underlying error (asyncore removal)
  in the build log instead of masking it.
- Add `python3-pytest` and `python3-six` BuildRequires (used by the
  pytest run and the six shim above respectively).

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
