Summary:        Symbolic constants in Python
Name:           python-constantly
Version:        15.1.0
Release:        6%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/twisted/constantly
# Source to be fixed as part of https://microsoft.visualstudio.com/OS/_workitems/edit/25936171.
Source0:        https://files.pythonhosted.org/packages/95/f1/207a0a478c4bb34b1b49d5915e2db574cadc415c9ac3a7ef17e29b2e8951/constantly-%{version}.tar.gz
BuildArch:      noarch

%description
A library that provides symbolic constant support. It includes collections and constants with text, numeric, and bit flag values. Originally twisted.python.constants from the Twisted project.

%package -n     python3-constantly
Summary:        Symbolic constants in Python
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-constantly
A library that provides symbolic constant support. It includes collections and constants with text, numeric, and bit flag values. Originally twisted.python.constants from the Twisted project.

%prep
%autosetup -n constantly-%{version}

%build
%py3_build

%install
%py3_install

%check
%{python3} setup.py test

%files -n python3-constantly
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 15.1.0-6
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 15.1.0-5
- Added %%license line automatically

* Wed Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 15.1.0-4
- Fixed "Source0" tag.
- License verified.
- Removed "%%define sha1".

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 15.1.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 15.1.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 15.1.0-1
- Initial packaging for Photon
