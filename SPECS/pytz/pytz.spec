Summary:        World timezone definitions, modern and historical
Name:           pytz
Version:        2018.5
Release:        6%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/pytz
Source0:        https://files.pythonhosted.org/packages/source/p/pytz/%{name}-%{version}.tar.gz

%description
pytz brings the Olson tz database into Python.

%package -n     python3-pytz
Summary:        World timezone definitions, modern and historical
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  unzip
%if %{with_check}
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
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
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    py.test%{python3_version} -v

%files -n python3-pytz
%defattr(-,root,root,-)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 2018.5-6
- Add license to python3 package
- Remove python2 package
- Lint spec

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
