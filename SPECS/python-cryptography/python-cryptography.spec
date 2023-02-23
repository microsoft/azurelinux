%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python cryptography library
Name:           python-cryptography
Version:        3.3.2
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/cryptography
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.io/packages/source/c/cryptography/cryptography-%{version}.tar.gz
Patch0:         CVE-2023-23931.patch
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-cffi
BuildRequires:  openssl-devel

Requires:       python-cffi
Requires:       openssl
Requires:       python2
Requires:       python2-libs
Requires:       python-idna
Requires:       python-pyasn1
Requires:       python-ipaddress
Requires:       python-setuptools
Requires:       python-packaging
Requires:       python-enum34
Requires:       python-asn1crypto
Requires:       python-six

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.

%package -n     python3-cryptography
Summary:        python-cryptography
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-cffi
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs
Requires:       python3-cffi
Requires:       python3-idna
Requires:       python3-pyasn1
Requires:       python3-six
Requires:       python3-packaging
Requires:       python3-asn1crypto

%description -n python3-cryptography
Cryptography is a Python library which exposes cryptographic recipes and primitives.
This is a Python 3 version.

%prep
%autosetup -n cryptography-%{version}
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
mv mariner.pem /etc/ssl/certs
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-cryptography
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Feb 22 2023 Mandeep Plaha <mandeepplaha@microsoft.com> 3.3.2-2
-   Patch CVE-2023-23931
*   Wed Feb 10 2021 Mateusz Malisz <mamalisz@microsoft.com> 3.3.2-1
-   Update to version 3.3.2, fixing CVE-2020-36242
-   Remove Patch for CVE-2020-25659.
*   Wed Jan 20 2021 Henry Beberman <henry.beberman@microsoft.com> 2.3.1-4
-   Patch CVE-2020-25659
-   License verified
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.3.1-3
-   Added %%license line automatically
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.3.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.3.1-1
-   Update to version 2.3.1
*   Mon Aug 14 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.3-1
-   Updated to version 2.0.3.
*   Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> 1.8.1-4
-   Added missing requires python-six and python-enum34
-   Removed python-enum from requires
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.1-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.1-2
-   Added missing requires python-enum
*   Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.1-1
-   Updated to version 1.8.1.
*   Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.2-1
-   Updated to version 1.7.2 and added python3 package.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 1.2.3-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.3-2
-   GA - Bump release of all rpms
*   Mon Mar 07 2016 Anish Swaminathan <anishs@vmware.com> 1.2.3-1
-   Upgrade to 1.2.3
*   Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com> 1.2.2-1
-   Upgrade version to 1.2.2
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.2.1-1
-   Upgrade version
*   Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.1-1
-   Initial packaging for Photon
