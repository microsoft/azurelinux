Summary:        Pythonic argument parser to create command line interfaces.
Name:           python-docopt
Version:        0.6.2
Release:        6%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/docopt
Source0:        https://files.pythonhosted.org/packages/source/d/docopt/docopt-%{version}.tar.gz
BuildArch:      noarch

%description
docopt helps easily create most beautiful command-line interfaces.

%package -n     python3-docopt
Summary:        Pythonic argument parser to create command line interfaces.
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-setuptools

%description -n python3-docopt
docopt helps easily create most beautiful command-line interfaces.

%prep
%autosetup -n docopt-%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-docopt
%defattr(-,root,root,-)
%license LICENSE-MIT
%{python3_sitelib}/*

%changelog
* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.6.2-6
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.6.2-5
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.6.2-4
- Renaming python-pytest to pytest

* Fri Apr 24 2020 Andrew Phelps <anphel@microsoft.com> - 0.6.2-3
- Updated Source0. Remove sha1 definition. Verified license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.6.2-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 0.6.2-1
- Initial version of python-docopt package for Photon.
