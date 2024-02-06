Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname uamqp
%global _description %{expand:An AMQP 1.0 client library for Python.}

Name:           python-%{srcname}
Version:        1.5.1
Release:        3%{?dist}
Summary:        AMQP 1.0 client library for Python

License:        MIT
URL:            https://github.com/Azure/azure-uamqp-python
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz#/azure-%{srcname}-python-%{version}.tar.gz
# Fix build with GCC 11
Patch1:         %{name}-treat-warnings-as-warnings.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist cython}
BuildRequires:  %{py3_dist setuptools}

%if %{with_check}
BuildRequires:  %{py3_dist certifi}
BuildRequires:  %{py3_dist pytest-asyncio}
BuildRequires:  python3-pip
%endif

%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p1 -n azure-uamqp-python-%{version}

# Remove bundled egg-info
rm -rf *.egg-info

%build
export CFLAGS="$RPM_OPT_FLAGS -Wno-error=strict-aliasing"
export CXXFLAGS=$CFLAGS
VERBOSE=1 %py3_build

%install
%py3_install

rm $RPM_BUILD_ROOT%{python3_sitearch}/%{srcname}/*.c

%check
pip3 install pytest six
%pytest --disable-warnings -k "not test_error_loop_arg_async"

%files -n python3-%{srcname}
%doc HISTORY.rst README.rst
%license LICENSE
%{python3_sitearch}/%{srcname}/
%{python3_sitearch}/%{srcname}-*.egg-info/


%changelog
* Fri Apr 29 2022 Muhammad Falak <mwani@microsoft.com> - 1.5.1-3
- Drop BR on pytest, six & pip install deps to enable ptest

* Wed Mar 23 2022 Muhammad Falak <mwani@microsoft.com> - 1.5.1-2
- Fix typo in BR for `%check` section

* Fri Feb 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.1-1
- Updating to version 1.5.1 using Fedora 36 spec (license: MIT) for guidance.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.12-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Dec 25 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.12-1
- Update to 1.2.12

* Fri Oct 02 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.11-1
- Update to 1.2.11

* Tue Aug 18 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.10-1
- Update to 1.2.10

* Tue Jul 07 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.9-1
- Update to 1.2.9

* Fri May 29 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.8-1
- Initial RPM release
