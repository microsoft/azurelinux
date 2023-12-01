Summary:        A fast, pure Python library for parsing and serializing ASN.1 structures.
Name:           python-asn1crypto
Version:        1.5.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/wbond/asn1crypto
Source0:        https://github.com/wbond/asn1crypto/archive/refs/tags/%{version}.tar.gz#/asn1crypto-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
A fast, pure Python library for parsing and serializing ASN.1 structures.

%package -n     python3-asn1crypto
Summary:        A fast, pure Python library for parsing and serializing ASN.1 structures.
Requires:       python3

%description -n python3-asn1crypto
A fast, pure Python library for parsing and serializing ASN.1 structures.

%prep
%autosetup -n asn1crypto-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install tox
tox -e py%{python3_version_nodots}

%files -n python3-asn1crypto
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed Apr 13 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.5.1-1
- Upgrade to latest upstream version
- Add tests using tox-based runner

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.24.0-4
- Remove python2 package
- Add license to python3 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.24.0-3
- Added %%license line automatically

* Thu Apr 16 2020 Jon Slobodzian <joslobo@microsoft.com> - 0.24.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).
- Verified license. Updated URL and created Source0 URL. Removed SHA1.

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 0.24.0-1
- Update to version 0.24.0

* Wed Jul 05 2017 Chang Lee <changlee@vmware.com> - 0.22.0-3
- Removed %check because the source does not include the test module

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.22.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 0.22.0-1
- Initial
