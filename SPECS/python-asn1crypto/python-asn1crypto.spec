Summary:        A fast, pure Python library for parsing and serializing ASN.1 structures.
Name:           python-asn1crypto
Version:        0.24.0
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/wbond/asn1crypto
#Source0:       https://files.pythonhosted.org/packages/fc/f1/8db7daa71f414ddabfa056c4ef792e1461ff655c2ae2928a2b675bfed6b4/asn1crypto-0.24.0.tar.gz
Source0:        asn1crypto-%{version}.tar.gz
BuildArch:      noarch

%description
A fast, pure Python library for parsing and serializing ASN.1 structures.

%package -n     python3-asn1crypto
Summary:        A fast, pure Python library for parsing and serializing ASN.1 structures.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-asn1crypto
A fast, pure Python library for parsing and serializing ASN.1 structures.

%prep
%autosetup -n asn1crypto-%{version}

%build
%py3_build

%install
%py3_install

# %%check
# Commented out %check due to no test existence

%files -n python3-asn1crypto
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
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
