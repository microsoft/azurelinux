Summary:        Symbolic constants in Python
Name:           python-constantly
Version:        23.10.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://github.com/twisted/constantly
# Source to be fixed as part of https://microsoft.visualstudio.com/OS/_workitems/edit/25936171.
Source0:        https://files.pythonhosted.org/packages/4d/6f/cb2a94494ff74aa9528a36c5b1422756330a75a8367bf20bd63171fc324d/constantly-%{version}.tar.gz
BuildArch:      noarch

%description
A library that provides symbolic constant support. It includes collections and constants with text, numeric, and bit flag values. Originally twisted.python.constants from the Twisted project.

%package -n     python3-constantly
Summary:        Symbolic constants in Python
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3-versioneer
%if 0%{?with_check}
Buildrequires:  python3-twisted
Buildrequires:  python3-typing-extensions
%endif
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
* Tue May 14 2024 Betty Lakes <bettylakes@microsoft.com> - 23.10.4-1
- Upgrade to 23.10.4

* Fri Feb 16 2024 Andrew Phelps <anphel@microsoft.com> - 15.1.0-7
- Fix build for python 3.12

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 15.1.0-6
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 15.1.0-5
- Added %%license line automatically

* Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 15.1.0-4
- Fixed "Source0" tag.
- License verified.
- Removed "%%define sha1".

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 15.1.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 15.1.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 15.1.0-1
- Initial packaging for Photon
