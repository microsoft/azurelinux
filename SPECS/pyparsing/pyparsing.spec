Summary:        Python package with an object-oriented approach to text processing
Name:           pyparsing
Version:        2.2.0
Release:        8%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/pyparsing/pyparsing
#Source0:       https://github.com/pyparsing/pyparsing/archive/pyparsing_%{version}.tar.gz
Source0:        pyparsing-%{version}.tar.gz
BuildArch:      noarch

%description
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.

%package -n     python3-pyparsing
Summary:        Python package with an object-oriented approach to text processing
BuildRequires:  python3-devel
Requires:       python3

%description -n python3-pyparsing
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.

%prep
%autosetup -n pyparsing-%{version}

%build
%py3_build

%install
%py3_install

#%check
#Tests are not available

%files -n python3-pyparsing
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 2.2.0-8
- Add license to python3 package
- Remove python2 package
- Lint spec

* Tue May 26 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.0-7
- Adding the "%%license" macro.

* Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.2.0-6
- Rename python-pyparsing to pyparsing.
- Update description.
- Update summary.

* Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> - 2.2.0-5
- Update URL.
- Update Source0 with valid URL.
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.2.0-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> - 2.2.0-3
- Disabled check section as tests are not available

* Tue Jun 20 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.2.0-2
- Add build dependency with python-setuptools to handle 1.0 update

* Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> - 2.2.0-1
- Update to 2.2.0 and remove build dependency with python-setuptools

* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.1.10-1
- Initial packaging for Photon
