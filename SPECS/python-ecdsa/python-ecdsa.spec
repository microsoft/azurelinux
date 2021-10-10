Summary:        ECDSA cryptographic signature library (pure python)
Name:           python-ecdsa
Version:        0.13.3
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://pypi.python.org/pypi/ecdsa
Source0:        https://pypi.python.org/packages/source/e/ecdsa/ecdsa-%{version}.tar.gz
Patch0:         disable_nist192_test.patch

%description
ECDSA cryptographic signature library (pure python)

%package -n     python3-ecdsa
Summary:        ECDSA cryptographic signature library (pure python)
BuildRequires:  openssl
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-ecdsa
This is an easy-to-use implementation of ECDSA cryptography (Elliptic Curve
Digital Signature Algorithm), implemented purely in Python, released under
the MIT license. With this library, you can quickly create keypairs (signing
key and verifying key), sign messages, and verify the signatures. The keys
and signatures are very short, making them easy to handle and incorporate
into other protocols.

%prep
%autosetup -p 1 -n ecdsa-%{version}

%build
%py3_build

%install
%{py3_install "--single-version-externally-managed"}

%check
python3 setup.py test

%files -n python3-ecdsa
%defattr(-, root, root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 0.13.3-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Wed Jan 13 2021 Nicolas Ontiveros <niontive@microsoft.com> - 0.13.3-4
- Add openssl to BR
- Disable OpenSSL NIST192 tests since OpenSSL no longer supports NIST192 EC.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.13.3-3
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.13.3-2
- Renaming ecdsa to python-ecdsa

* Thu Mar 19 2020 Nicolas Ontiveros <niontive@microsoft.com> - 0.13.3-1
- Update version to 0.13.3. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.13-6
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Jun 19 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.13-5
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.13-4
- Use python2 explicitly

* Mon Feb 27 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.13-3
- Added python3 site-packages.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 0.13-2
- GA - Bump release of all rpms

* Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> - 0.13-1
- Initial build.  First version
