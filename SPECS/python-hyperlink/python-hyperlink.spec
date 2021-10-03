Summary:        provides a pure-Python implementation of immutable URLs
Name:           python-hyperlink
Version:        19.0.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/python-hyper/hyperlink
#Source0:       https://github.com/python-hyper/hyperlink/archive/v%{version}.tar.gz
Source0:        https://github.com/python-hyper/hyperlink/archive/%{name}-%{version}.tar.gz

%description
Hyperlink provides a pure-Python implementation of immutable URLs. Based on RFC 3986 and 3987, the Hyperlink URL makes working with both URIs and IRIs easy.

%package -n     python3-hyperlink
Summary:        provides a pure-Python implementation of immutable URLs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-idna
%endif

%description -n python3-hyperlink
Hyperlink provides a pure-Python implementation of immutable URLs. Based on RFC 3986 and 3987, the Hyperlink URL makes working with both URIs and IRIs easy.

%prep
%autosetup -n hyperlink-%{version}

%build
%py3_build

%install
%py3_install

%check
easy_install_3=$(ls %{_bindir} |grep easy_install |grep 3)
$easy_install_3 pytest
pytest

%files -n python3-hyperlink
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 19.0.0-3
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 19.0.0-2
- Added %%license line automatically

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> - 19.0.0-1
- Update to 19.0.0. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 18.0.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Dec 06 2018 Tapas Kundu <tkundu@vmware.com> - 18.0.0-2
- Fix make check.

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 18.0.0-1
- Update to version 18.0.0

* Wed Sep 20 2017 Bo Gan <ganb@vmware.com> - 17.3.1-2
- Fix make check issues

* Mon Sep 11 2017 Dheeraj Shetty <dheerajs@vmware.com> - 17.3.1-1
- Initial packaging for Photon
