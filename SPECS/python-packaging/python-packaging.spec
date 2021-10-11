Summary:        Core utilities for Python packages
Name:           python-packaging
Version:        17.1
Release:        7%{?dist}
License:        BSD OR ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/packaging
# This link seems very sensitive to the precise package version.
# Source0:      https://files.pythonhosted.org/packages/77/32/439f47be99809c12ef2da8b60a2c47987786d2c6c9205549dd6ef95df8bd/packaging-%{version}.tar.gz
Source0:        packaging-%{version}.tar.gz
BuildArch:      noarch

%description
Core utilities for Python packages

%package -n     python3-packaging
Summary:        Core utilities for Python packages
BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-pyparsing
Requires:       python3-six
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-pyparsing
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-xml
%endif

%description -n python3-packaging
Core utilities for Python packages

%prep
%autosetup -n packaging-%{version}

%build
%py3_build

%install
%py3_install

%check
easy_install_3=$(ls %{_bindir} |grep easy_install |grep 3)
$easy_install_3 pretend pytest
PYTHONPATH=./ pytest

%files -n python3-packaging
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 17.1-7
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 17.1-6
- Added %%license line automatically

* Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> - 17.1-5
- Use pyparsing in Requres and BR.

* Mon Apr 13 2020 Nick Samson <nisamson@microsoft.com> - 17.1-4
- Updated Source0, removed %%define sha1, confirmed license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 17.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> - 17.1-2
- Fix makecheck

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 17.1-1
- Update to version 17.1

* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> - 16.8-4
- Fixed rpm check errors
- Fixed runtime dependencies

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 16.8-3
- Fix arch

* Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> - 16.8-2
- Remove python-setuptools from BuildRequires

* Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> - 16.8-1
- Initial packaging for Photon
