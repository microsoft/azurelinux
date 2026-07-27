Summary:        Crypto and SSL toolkit for Python
Name:           m2crypto
Version:        0.38.0
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/M2Crypto
Source0:        https://files.pythonhosted.org/packages/2c/52/c35ec79dd97a8ecf6b2bbd651df528abb47705def774a4a15b99977274e8/M2Crypto-%{version}.tar.gz
Patch0:         0001-skip-test_tls1_nok-which-cant-be-run-in-FIPS.patch
Patch1:         CVE-2020-25657.patch
Patch2:         CVE-2019-11358.patch

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
%if 0%{?with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-six
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
# M2Crypto 0.38.0 (last released 2021) has two known incompatibilities
# with Python 3.12 that cannot be fixed at the spec level:
#
#  1. The bundled `M2Crypto/six.py` lazy importer for `six.moves` was
#     broken by importlib changes in 3.12. We replace it with the system
#     `six` (installed below) to get past this layer.
#  2. `M2Crypto/SSL/ssl_dispatcher.py` does `import asyncore` at module
#     load time. `asyncore` was removed from the Python 3.12 stdlib
#     (PEP 594). Because `M2Crypto/__init__.py` eagerly imports `SSL`,
#     every `from M2Crypto import ...` fails with
#     `ModuleNotFoundError: No module named 'asyncore'`, which means
#     the test suite cannot even collect.
#
# Upstream M2Crypto >= 0.40 drops the asyncore-based dispatcher. Until
# this package can be rebased on 0.40+, the tests cannot pass under
# Python 3.12 and we tolerate failure with `|| :`. We still run pytest
# (with the six.py shim so reviewers see the real underlying error) and
# still install `parameterized`, so the day this package is updated the
# %check section starts being meaningful with no further work.
pip3 install parameterized
cp -f $(%python3 -c "import six; print(six.__file__)") \
  %{buildroot}%{python3_sitearch}/M2Crypto/six.py
PYTHONPATH=%{buildroot}%{python3_sitearch} \
  %python3 -m pytest tests/ -k "not test_tls1_nok" || :

%files -n python3-m2crypto
%defattr(-,root,root)
%license LICENCE
%{python3_sitelib}/*

%changelog
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
