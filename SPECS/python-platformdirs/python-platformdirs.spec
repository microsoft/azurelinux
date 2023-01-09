%global srcname platformdirs
%global common_description %{expand:
A small Python module for determining appropriate platform-specific dirs, e.g.
a "user data dir".}
Summary:        Python module for determining appropriate platform-specific dirs
Name:           python-%{srcname}
Version:        2.0.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/platformdirs/platformdirs
Source0:        https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-wheel
BuildArch:      noarch

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
pip3 install tox
%tox


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.txt
%doc README.rst CHANGES.rst

%changelog
* Wed Dec 21 2021 Riken Maharjan <rmaharjan@microsoft.com> - 2.0.0-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified.

* Mon Jul 12 2021 Carl George <carl@george.computer> - 2.0.0-1
- Initial package rhbz#1981607
