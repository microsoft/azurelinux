Summary:        Python PAM module using ctypes
Name:           python-pam
# Update the version field in fix-pyproject.patch whenever this changes.
Version:        2.0.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/python-pam/
Source0:        https://pypi.python.org/packages/source/p/python-pam/%{name}-%{version}.tar.gz
Patch0:         fix-pyproject.patch
BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-flit-core
BuildRequires:  python3-pip
BuildRequires:  python3-six
BuildRequires:  python3-xml

%description
Python PAM module using ctypes

%package -n     python3-pam
Summary:        Python PAM module using ctypes
Requires:       python3

%description -n python3-pam
Python PAM module using ctypes

%prep
%autosetup -n python-pam-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pam

%files -n python3-pam
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Tue Feb 27 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.2-1
- Auto-upgrade to 2.0.2 - AzL 3.0 upgrade

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.8.4-3
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.8.4-2
- Added %%license line automatically

* Wed Mar 18 2020 Paul Monson <paulmon@microsoft.com> - 1.8.4-1
- Update to version 1.8.4.  Source0 fixed. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.8.2-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.8.2-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Mar 09 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.8.2-1
- Initial packaging for Photon
