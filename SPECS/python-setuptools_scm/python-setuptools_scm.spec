Summary:        The blessed package to manage your versions by scm tags.
Name:           python-setuptools_scm
Version:        3.1.0
Release:        5%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.python.org/pypi/setuptools_scm
Source0:        https://files.pythonhosted.org/packages/source/s/setuptools_scm/setuptools_scm-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildArch:      noarch

%description
setuptools_scm handles managing your python package versions in scm metadata.

%package -n     python3-setuptools_scm
Summary:        python-setuptools_scm
Requires:       python3

%description -n python3-setuptools_scm
setuptools_scm handles managing your python package versions in scm metadata
instead of declaring them as the version argument or in a scm managed file.
It also handles file finders for the supported scms.

%prep
%autosetup -n setuptools_scm-%{version}

%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-setuptools_scm
%license LICENSE
%{python3_sitelib}/*

%changelog
* Mon Feb 15 2022 Thomas Crain <thcrain@microsoft.com> - 3.1.0-5
- Remove python2 subpackage

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - 3.1.0-4
- Remove unused `%%define sha1` lines
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.1.0-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.1.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 3.1.0-1
- Update to version 3.1.0

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.15.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.15.0-1
- Initial packaging for Photon
