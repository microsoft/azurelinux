Vendor:         Microsoft Corporation
Distribution:   Mariner
%global upstream_name pytest-randomly
%global module_name pytest_randomly

Name:           python-%{upstream_name}
Version:        3.4.1
Release:        3%{?dist}
Summary:        Pytest plugin to randomly order tests and control random.seed
License:        BSD
URL:            https://github.com/pytest-dev/pytest-randomly
Source0:        https://files.pythonhosted.org/packages/source/p/%{upstream_name}/%{upstream_name}-%{version}.tar.gz#/python-%{upstream_name}-%{version}.tar.gz
# Fedora-specific test fix to account for our version of pytest,
# not acceptable upstream:
# https://github.com/pytest-dev/pytest-randomly/issues/218
Patch1:         0001-tests-fix-error-message-assertion-for-invalid-value.patch
BuildArch:      noarch

%description
%{summary}.

%package -n python3-%{upstream_name}
Summary:        Pytest plugin to randomly order tests and control random.seed
%{?python_provide:%python_provide python3-%{upstream_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools


# Only for running the tests:
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-xdist
BuildRequires:  python3-factory-boy
%if 0%{?fedora} >= 33
BuildRequires:  python3-faker
%endif
BuildRequires:  python3-numpy

%description -n python3-%{upstream_name}
%{summary}.

%prep
%autosetup -n %{upstream_name}-%{version} -p1
rm -r src/*.egg-info

%build
%py3_build

%install
%py3_install

%check
%if 0%{?fedora} >= 33
PYTHONPATH=%{buildroot}%{python3_sitelib} PYTHONDONTWRITEBYTECODE=1 pytest-3 -p no:randomly -v tests/
%else
# Faker pytest integration is only in Fedora 33+
# so skip tests for it when it is not available
PYTHONPATH=%{buildroot}%{python3_sitelib} PYTHONDONTWRITEBYTECODE=1 pytest-3 -p no:randomly -v tests/ -k 'not faker'
%endif

%files -n python3-%{upstream_name}
%doc README.rst HISTORY.rst
%license LICENSE
%{python3_sitelib}/%{module_name}.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{module_name}*.egg-info

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.4.1-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jul 15 2020 Dan Callaghan <djc@djc.id.au> - 3.4.1-2
- skip tests for optional faker integration when it is not available

* Wed Jul 15 2020 Dan Callaghan <djc@djc.id.au> - 3.4.1-1
- new upstream release 3.4.1:
  https://github.com/pytest-dev/pytest-randomly/blob/3.4.1/HISTORY.rst

* Sat Jun 13 2020 Dan Callaghan <djc@djc.id.au> - 3.4.0-1
- new upstream release 3.4.0:
  https://github.com/pytest-dev/pytest-randomly/blob/3.4.0/HISTORY.rst

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-2
- Rebuilt for Python 3.9

* Sun May 17 2020 Dan Callaghan <dan.callaghan@opengear.com> - 3.3.1-1
- new upstream release 3.3.1:
  https://github.com/pytest-dev/pytest-randomly/blob/3.3.1/HISTORY.rst

* Thu Jan 30 2020 Dan Callaghan <dan.callaghan@opengear.com> - 3.2.1-1
- new upstream release 3.2.1

* Mon Dec 30 2019 Dan Callaghan <dan.callaghan@opengear.com> - 1.2.3-2
- re-enabled tests, suppress pytest bytecode

* Mon Dec 31 2018 Dan Callaghan <dan.callaghan@opengear.com> - 1.2.3-1
- initial version
