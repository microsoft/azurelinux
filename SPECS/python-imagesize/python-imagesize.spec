Summary:        python module to analyze jpeg/jpeg2000/png/gif image header and return image size.
Name:           python-imagesize
Version:        1.4.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/shibukawa/imagesize_py
#Source0:       https://github.com/shibukawa/imagesize_py/archive/%{version}.tar.gz
Source0:        https://files.pythonhosted.org/packages/41/f5/3cf63735d54aa9974e544aa25858d8f9670ac5b4da51020bbfc6aaade741/imagesize-%{version}.tar.gz
BuildArch:      noarch
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
python module to analyze jpeg/jpeg2000/png/gif image header and return image size.

%package -n     python3-imagesize
Summary:        python module to analyze jpeg/jpeg2000/png/gif image header and return image size.
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-imagesize
Python 3 module to analyze jpeg/jpeg2000/png/gif image header and return image size.

%prep
%autosetup -n imagesize-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest pathlib2 pluggy
%{python3} setup.py test

%files -n python3-imagesize
%license LICENSE.rst
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.1-1
- Auto-upgrade to 1.4.1 - Azure Linux 3.0 - package upgrades

* Wed Feb 09 2022 Muhammad Falak <mwani@microsoft.com> - 1.1.0-9
- Add an explict BR on 'pip' to enable ptest
- Remove stray `popd` in the `%check` section

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 1.1.0-8
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.1.0-7
- Add license to python3 package
- Remove python2 package
- Lint spec

* Tue Dec 22 2020 Andrew Phelps <anphel@microsoft.com> - 1.1.0-6
- Fix check tests by installing python test dependencies.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.1.0-5
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.1.0-4
- Renaming python-pytest to pytest

* Tue Apr 21 2020 Eric Li <eli@microsoft.com> - 1.1.0-3
- Update Source0:, add #Source0:, and delete sha1. Verified license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.1.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 1.1.0-1
- Update to version 1.1.0

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.7.1-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.7.1-2
- Change python to python2

* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.7.1-1
- Initial
