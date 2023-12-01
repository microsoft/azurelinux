%define pypi_name MarkupSafe
Summary:        A XML/HTML/XHTML Markup safe string for Python.
Name:           python-markupsafe
Version:        2.1.3
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/MarkupSafe
Source0:        https://pypi.python.org/packages/source/M/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

%description
MarkupSafe implements a XML/HTML/XHTML Markup safe string for Python.

%package -n     python3-markupsafe
Summary:        python-markupsafe
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Provides:       python3dist(markupsafe) = %{version}-%{release}
Provides:       python3.9dist(markupsafe) = %{version}-%{release}

%description -n python3-markupsafe
MarkupSafe implements a XML/HTML/XHTML Markup safe string for Python.

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install py
%python3 setup.py test

%files -n python3-markupsafe
%defattr(-,root,root,-)
%license LICENSE.rst
%{python3_sitelib}/*

%changelog
* Mon Nov 27 2023 Andrew Phelps <anphel@microsoft.com> - 2.1.3-1
- Upgrade to 2.1.3

* Tue Mar 08 2022 Nick Samson <nisamson@microsoft.com> - 2.1.0-1
* Upgrade to 2.1.0.

* Mon Dec 06 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.1.1-4
- Replace easy_install usage with pip in %%check sections

* Sat Dec 04 2021 Henry Beberman <henry.beberman@microsoft.com> - 1.1.1-3
- Explicitly provide python3dist(markupsafe) because built in toolchain.

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.1.1-2
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Wed Nov 11 2020 Olivia Crain <oliviacrain@microsoft.com> - 1.1.1-1
- Upgrade to 1.1.1 to fix setuptools compatibility issues
- Change Source0
- Correct license location
- Remove inline sha1
- Lint to Mariner style

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0-5
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.0-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.0-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.0-2
- Removed erroneous version line

* Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> - 1.0-1
- Upgrade version to 1.0

* Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.23-1
- Initial packaging for Photon
