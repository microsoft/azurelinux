# Disable tests as it requires new package python-exceptiongroup
%global srcname platformdirs
%bcond_without tests
%global common_description %{expand:
A small Python module for determining appropriate platform-specific dirs, e.g.
a "user data dir".}
Summary:        Python module for determining appropriate platform-specific dirs
Name:           python-%{srcname}
Version:        4.2.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/platformdirs/platformdirs
Source0:        https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-six
BuildRequires:  python3-wheel
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy
BuildRequires:  python3-tomli
BuildRequires:  python3-trove-classifiers
BuildArch:      noarch
%if %{with tests}
BuildRequires:  python3-pytest
BuildRequires:  python3-iniconfig
BuildRequires:  python3-appdirs
BuildRequires:  python3-pytest-mock
%endif

%description %{common_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel

%description -n python3-%{srcname} %{common_description}

%prep
%autosetup -n %{srcname}-%{version}



%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
%if %{with tests}
%pytest
%else
%pyproject_check_import
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license %{python3_sitearch}/%{srcname}-%{version}.dist-info/licenses/LICENSE
%doc README.rst

%changelog
* Fri Apr 12 2024 Bala <balakumaran.kannan@microsoft.com> - 4.2.0-2
- Fix PTest failures by adding necessary packages as dependencies

* Mon Feb 26 2024 Bala <balakumaran.kannan@microsoft.com> - 4.2.0-1
- Upgraded to 4.2.0
- Disable tests as pytest requires new package python-exceptiongroup

* Wed Dec 21 2021 Riken Maharjan <rmaharjan@microsoft.com> - 2.0.0-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified.

* Mon Jul 12 2021 Carl George <carl@george.computer> - 2.0.0-1
- Initial package rhbz#1981607
