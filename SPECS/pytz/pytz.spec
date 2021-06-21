%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python2_version: %define python2_version %(python2 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        World timezone definitions, modern and historical
Name:           pytz
Version:        2018.5
Release:        5%{?dist}
Url:            https://pypi.python.org/pypi/pytz
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/source/p/pytz/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  unzip
BuildRequires:  pytest
Requires:       python2
Requires:       python2-libs
Requires:       tzdata

%description
pytz brings the Olson tz database into Python. This library allows
accurate and cross platform timezone calculations using Python 2.4
or higher. It also solves the issue of ambiguous times at the end
of daylight saving time, which you can read more about in the Python
Library Reference (``datetime.tzinfo``).

%package -n     python3-pytz
Summary:        python3-pytz
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pytest
%if %{with_check}
BuildRequires: python3-setuptools
BuildRequires: python3-xml
%endif

Requires:       python3
Requires:       python3-libs
Requires:       tzdata

%description -n python3-pytz
Python 3 version.

%prep
%setup -q
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python2_sitelib} \
    py.test%{python2_version} -v
pushd ../p3dir
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    py.test%{python3_version} -v
popd

%files
%defattr(-,root,root)
%license LICENSE.txt
%{python2_sitelib}/*

%files -n python3-pytz
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:20:48 PST 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 2018.5-4
-   Renaming python-pytest to pytest
*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 2018.5-3
-   Renaming python-pytz to pytz
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2018.5-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2018.5-1
-   Update to version 2018.5
*   Fri Aug 18 2017 Rongrong Qiu <rqiu@vmware.com> 2017.2-3
-   add BuildRequires for make check bug 1937039
*   Wed Apr 26 2017 Dheeraj Shetty <dheerajs@vmware.com> 2017.2-2
-   Requires tzdata
*   Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 2017.2-1
-   Initial packaging for Photon
