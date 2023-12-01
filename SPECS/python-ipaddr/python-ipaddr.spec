Summary:        Google's Python IP address manipulation library
Name:           python-ipaddr
Version:        2.2.0
Release:        3%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/google/ipaddr-py
Source0:        https://pypi.python.org/packages/source/i/ipaddr/ipaddr-%{version}.tar.gz
#Patch0:        ipaddr-python3-compatibility.patch
BuildArch:      noarch

%description
Google's Python IP address manipulation library

%package -n     python3-ipaddr
Summary:        Google's Python IP address manipulation library
BuildRequires:  python3-devel
Requires:       python3

%description -n python3-ipaddr
ipaddr.py is a library for working with IP addresses, both IPv4 and IPv6. It was developed by Google for internal use, and is now open source.

%prep
%autosetup -n ipaddr-%{version}

%build
%py3_build

%install
%py3_install

%check
%{python3} ipaddr_test.py

%files -n python3-ipaddr
%defattr(-,root,root,-)
%license COPYING
%{python3_sitelib}/*

%changelog
* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.2.0-3
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.2.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).
- Added %%license line automatically

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 2.2.0-1
- Update to version 2.2.0

* Tue May 16 2017 Kumar Kaushik <kaushikk@vmware.com> - 2.1.11-4
- Adding python 3 support.

* Mon Oct 03 2016 ChangLee <changLee@vmware.com> - 2.1.11-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.1.11-2
- GA - Bump release of all rpms

* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
