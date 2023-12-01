Summary:        Implementation of ASN.1 types and codecs in Python programming language
Name:           python-pyasn1
Version:        0.4.8
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.org/project/pyasn1
Source0:        https://files.pythonhosted.org/packages/source/p/pyasn1/pyasn1-%{version}.tar.gz
BuildArch:      noarch

%description
This is an implementation of ASN.1 types and codecs in Python programming language.

%package -n     python3-pyasn1
Summary:        Implementation of ASN.1 types and codecs in Python programming language
BuildRequires:  python3-devel
Requires:       python3

%description -n python3-pyasn1
This is an implementation of ASN.1 types and codecs in Python programming language.
It has been first written to support particular protocol (SNMP) but then generalized
to be suitable for a wide range of protocols based on ASN.1 specification.

%prep
%autosetup -n pyasn1-%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-pyasn1
%defattr(-,root,root,-)
%license LICENSE.rst
%{python3_sitelib}/*

%changelog
* Mon Jan 03 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.4.8-1
- Upgrade to latest upstream version
- Use nicer Source0
- License verified

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.4.4-4
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.4.4-3
- Added %%license line automatically.

* Tue Apr 07 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.4-2
- Initial CBL-Mariner import from Photon (license: Apache2).
- Added 'Distribution' and 'Vendor' tags.
- Fixed "Source0" tag.
- License verified.

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 0.4.4-1
- Update to version 0.4.4

* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.2.3-1
- Updated to version 0.2.3.

* Mon Oct 04 2016 ChangLee <changlee@vmware.com> - 0.1.9-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 0.1.9-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 0.1.9-1
- Upgraded to version 0.1.9

* Thu Aug 6 2015 Anish Swaminathan <anishs@vmware.com>
- Added sha1sum

* Fri Mar 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
