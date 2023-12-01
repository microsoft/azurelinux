Summary:        An implementation of the OAuth request-signing logic
Name:           python-oauthlib
Version:        2.1.0
Release:        7%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/oauthlib/oauthlib
Source0:        https://files.pythonhosted.org/packages/df/5f/3f4aae7b28db87ddef18afed3b71921e531ca288dc604eb981e9ec9f8853/oauthlib-%{version}.tar.gz
BuildArch:      noarch
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
OAuthLib is a generic utility which implements the logic of OAuth without assuming a specific HTTP request object or web framework

%package -n python3-oauthlib
Summary:        Python3 package for oauthlib
BuildRequires:  libffi-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-oauthlib
OAuthLib is a generic utility which implements the logic of OAuth without assuming a specific HTTP request object or web framework

%prep
%autosetup -n oauthlib-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install mock wheel
%python3 setup.py test

%files -n python3-oauthlib
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed Feb 09 2022 Muhammad Falak <mwani@microsoft.com> - 2.1.0-7
- Add an explicit BR on 'pip'
- Install 'wheel' to enable ptest

* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.1.0-6
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.1.0-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.1.0-4
- Added %%license line automatically

* Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> - 2.1.0-3
- Verified license. Removed sha1. Fixed Source0 URL. Fixed URL.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.1.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 2.1.0-1
- Update to version 2.1.0

* Fri Jul 07 2017 Chang Lee <changlee@vmware.com> - 2.0.2-3
- Add  libffi-devel in BuildRequires and install mock python module in %check

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.0.2-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Apr 13 2017 Anish Swaminathan <anishs@vmware.com> - 2.0.2-1
- Initial packaging for Photon
