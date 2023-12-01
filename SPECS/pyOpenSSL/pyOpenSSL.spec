Summary:        Python wrapper module around the OpenSSL library
Name:           pyOpenSSL
Version:        18.0.0
Release:        8%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/pyca/pyopenssl
Source0:        https://files.pythonhosted.org/packages/source/p/pyOpenSSL/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
High-level wrapper around a subset of the OpenSSL library.

%package -n     python3-pyOpenSSL
Summary:        Python wrapper module around the OpenSSL library
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-cryptography
Requires:       python3-six
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-asn1crypto
BuildRequires:  python3-cffi
BuildRequires:  python3-cryptography
BuildRequires:  python3-idna
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pycparser
BuildRequires:  python3-six
%endif

%description -n python3-pyOpenSSL
High-level wrapper around a subset of the OpenSSL library.

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%check
pip3 install pretend flaky pytest
PATH=%{buildroot}%{_bindir}:${PATH} \
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python3_sitelib} \
    pytest

%files -n python3-pyOpenSSL
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 18.0.0-8
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 18.0.0-7
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>  - 18.0.0-6
- Added %%license line automatically

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 18.0.0-5
- Renaming python-pyOpenSSL to pyOpenSSL

* Tue Apr 07 2020 Nicolas Ontiveros <niontive@microsoft.com> 18.0.0-4
- Remove python-enum from build requires.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 18.0.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Jan 11 2019 Tapas Kundu <tkundu@vmware.com> 18.0.0-2
- Fix makecheck

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.0.0-1
- Update to version 18.0.0

* Thu Jun 14 2018 Tapas Kundu <tkundu@vmware.com> 17.2.0-2
- Added memory fix for X509StoreContext Class.

* Mon Aug 14 2017 Xiaolin Li <xiaolinl@vmware.com> 17.2.0-1
- Updated to version 17.2.0 and fixed make check.

* Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 16.2.0-5
- Fixed runtime dependencies

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.2.0-3
- Use python2 explicitly

* Tue Feb 21 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-2
- Add Requires for python-enum and python-ipaddress

* Tue Feb 14 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-1
- Initial packaging for Photon
