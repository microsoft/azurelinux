%{!?python3_pkgversion: %global python3_pkgversion 3}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%global pypi_name pytest-subtests

Summary:        Support for unittest subTest() and subtests fixture
Name:           python-%{pypi_name}
Version:        0.3.1
Release:        4%{?dist}
License:        MIT
URL:            https://github.com/pytest-dev/pytest-subtests
#Source0:       https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
pytest-subtests unittest subTest() support and subtests fixture.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
%{?python_provide:%python_provide python3-%{pypi_name}}
 
%description -n python3-%{pypi_name}
pytest-subtests unittest subTest() support and subtests fixture.

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest==7.1.2
# https://github.com/pytest-dev/pytest-subtests/issues/21
PYTHONDONTWRITEBYTECODE=1 pytest -v tests \
  -k "not TestFixture and not TestCapture and not test_simple_terminal"

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/pytest_subtests.py
%{python3_sitelib}/pytest_subtests-%{version}-py*.egg-info/

%changelog
* Thu Apr 29 2022 Muhammad Falak <mwani@microsoft.com> - 0.3.1-4
- Drop BR on pytest & pip install latest deps to enable ptest
- License verified

* Wed Dec 09 2020 Steve Laughman <steve.laughman@microsoft.com> - 0.3.1-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.1-1
- Update to latest upstream release 0.3.1

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-2
- Rebuilt for Python 3.9

* Mon Mar 23 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.3.0-1
- Initial package for Fedora
