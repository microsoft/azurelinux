Summary:        World timezone definitions, modern and historical
Name:           pytz
Version:        2023.3
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/pytz
Source0:        https://files.pythonhosted.org/packages/5e/32/12032aa8c673ee16707a9b6cdda2b09c0089131f35af55d443b6a9c69c1d/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
pytz brings the Olson tz database into Python.

%package -n     python3-pytz
Summary:        World timezone definitions, modern and historical
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  unzip
%if %{with_check}
BuildRequires:  python3-pip
%endif
Requires:       python3
Requires:       tzdata

%description -n python3-pytz
pytz brings the Olson tz database into Python. This library allows
accurate and cross platform timezone calculations using Python 2.4
or higher. It also solves the issue of ambiguous times at the end
of daylight saving time, which you can read more about in the Python
Library Reference (``datetime.tzinfo``).

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%check
pip3 install --upgrade pip wheel flake8
pushd pytz/tests
check_status=0
%python3 test_lazy.py -vv
if [[ $? -ne 0 ]]; then
	check_status=1
fi
%python3 test_tzinfo.py -vv
if [[ $? -ne 0 ]]; then
	check_status=1
fi
popd
[[ $check_status -eq 0 ]]

%files -n python3-pytz
%defattr(-,root,root,-)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2023.3-1
- Auto-upgrade to 2023.3 - Azure Linux 3.0 - package upgrades

* Sat Feb 12 2022 Muhammad Falak <mwani@microsoft.com> - 2021.3-1
- Bump version to 2021.3
- Add an explicit BR on `pip` & remove un-needed deps
- Use correct test files to enable ptest

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 2018.5-6
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2018.5-5
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 2018.5-4
- Renaming python-pytest to pytest

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 2018.5-3
- Renaming python-pytz to pytz

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2018.5-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 2018.5-1
- Update to version 2018.5

* Fri Aug 18 2017 Rongrong Qiu <rqiu@vmware.com> - 2017.2-3
- add BuildRequires for make check bug 1937039

* Wed Apr 26 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2017.2-2
- Requires tzdata

* Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> - 2017.2-1
- Initial packaging for Photon
