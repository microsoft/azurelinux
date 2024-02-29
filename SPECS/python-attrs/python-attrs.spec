Summary:        Attributes without boilerplate.
Name:           python-attrs
Version:        21.4.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/attrs
Source0:        https://github.com/%{name}/attrs/archive/refs/tags/%{version}.tar.gz#/attrs-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
Attributes without boilerplate.

%package -n     python3-attrs
Summary:        Attributes without boilerplate.
Requires:       python3

%description -n python3-attrs
Attributes without boilerplate.

%prep
%autosetup -p1 -n attrs-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install tox
# Skip mypy tests- effort required in keeping these tests green is not justifiable,
# as we don't ship mypy and these tests are very sensitive to mypy upstream changes
LANG=en_US.UTF-8 tox -e py%{python3_version_nodots} -- -k 'not test_mypy'

%files -n python3-attrs
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Thu Nov 30 2023 Olivia Crain <oliviacrain@microsoft.com> - 21.4.0-3
- Skip mypy tests, remove previously used test fix patch

* Tue Jul 12 2022 Olivia Crain <oliviacrain@microsoft.com> - 21.4.0-2
- Add upstream patch to fix mypy tests

* Wed Apr 13 2022 Olivia Crain <oliviacrain@microsoft.com> - 21.4.0-1
- Upgrade to latest upstream version
- Simplify test setup and requirements

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 18.2.0-10
- Use `py%{python3_version_nodots}` instead of harcoding `py39`

* Sat Feb 12 2022 Muhammad Falak <mwani@microsoft.com> - 18.2.0-9
- Use `py39` as tox env to enable ptest

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 18.2.0-8
- Add license to python3 package
- Remove python2 package
- Lint spec

* Tue Jan 05 2021 Andrew Phelps <anphel@microsoft.com> - 18.2.0-7
- Use tox to run tests.

* Wed Jul 08 2020 Henry Beberman <henry.beberman@microsoft.com> - 18.2.0-6
- Fix typo in BuildRequires for python3-zope-interface

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 18.2.0-5
- Added %%license line automatically

* Fri Apr 24 2020 Nick Samson <nisamson@microsoft.com> - 18.2.0-4
- Updated Source0, license verified. Removed %%define sha1

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 18.2.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Nov 13 2018 Tapas Kundu <tkundu@vmware.com> - 18.2.0-2
- Fixed the makecheck errors

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 18.2.0-1
- Update to version 18.2.0

* Thu Jul 06 2017 Chang Lee <changlee@vmware.com> - 16.3.0-3
- Updated %check

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 16.3.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 16.3.0-1
- Initial packaging for Photon
