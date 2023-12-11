Summary:        Python cryptography library
Name:           python-cryptography
Version:        3.3.2
Release:        6%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/cryptography
Source0:        https://pypi.io/packages/source/c/cryptography/cryptography-%{version}.tar.gz
Patch0:    CVE-2023-49083-1.patch
Patch0:    CVE-2023-49083.patch
Patch0:         CVE-2023-23931.patch
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.

%package -n     python3-cryptography
Summary:        python-cryptography
BuildRequires:  openssl-devel
BuildRequires:  python3-cffi
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-asn1crypto
Requires:       python3-cffi
Requires:       python3-idna
Requires:       python3-packaging
Requires:       python3-pyasn1
Requires:       python3-six

%description -n python3-cryptography
Cryptography is a Python library which exposes cryptographic recipes and primitives.

%prep
%autosetup -p1 -n cryptography-%{version}

%build
%py3_build

%install
%py3_install

%check
openssl req \
    -new \
    -newkey rsa:4096 \
    -days 365 \
    -nodes \
    -x509 \
    -subj "/C=US/ST=WA/L=Redmond/O=Microsoft/CN=mariner.com" \
    -keyout mariner.key \
    -out mariner.cert
openssl rsa -in mariner.key -out mariner.pem
mv mariner.pem %{_sysconfdir}/ssl/certs
pip3 install pretend pytest hypothesis iso8601 cryptography_vectors pytz
%{__python3} setup.py test

%files -n python3-cryptography
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Mon Dec 11 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.3.2-6
- Add patch for CVE-2023-49083

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.3.2-5
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Feb 15 2023 Suresh Thelkar <sthelkar@microsoft.com> - 3.3.2-4
- Patch CVE-2023-25193
- License verified.

* Wed Feb 09 2022 Muhammad Falak <mwani@microsoft.com> - 3.3.2-3
- Add and explict BR on 'pip'
- Install ptest dependecies

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 3.3.2-2
- Add license to python3 package
- Remove python2 package
- Lint spec

* Wed Feb 10 2021 Mateusz Malisz <mamalisz@microsoft.com> - 3.3.2-1
- Update to version 3.3.2, fixing CVE-2020-36242
- Remove Patch for CVE-2020-25659.

* Wed Jan 20 2021 Henry Beberman <henry.beberman@microsoft.com> - 2.3.1-4
- Patch CVE-2020-25659
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.3.1-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.3.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 2.3.1-1
- Update to version 2.3.1

* Mon Aug 14 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.0.3-1
- Updated to version 2.0.3.

* Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> - 1.8.1-4
- Added missing requires python-six and python-enum34
- Removed python-enum from requires

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.8.1-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.8.1-2
- Added missing requires python-enum

* Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.8.1-1
- Updated to version 1.8.1.

* Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.7.2-1
- Updated to version 1.7.2 and added python3 package.

* Mon Oct 03 2016 ChangLee <changLee@vmware.com> - 1.2.3-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.3-2
- GA - Bump release of all rpms

* Mon Mar 07 2016 Anish Swaminathan <anishs@vmware.com> - 1.2.3-1
- Upgrade to 1.2.3

* Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com> - 1.2.2-1
- Upgrade version to 1.2.2

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> - 1.2.1-1
- Upgrade version

* Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> - 1.1-1
- Initial packaging for Photon
