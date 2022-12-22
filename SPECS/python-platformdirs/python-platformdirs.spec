%global srcname platformdirs
%global common_description %{expand:
A small Python module for determining appropriate platform-specific dirs, e.g.
a "user data dir".}

Name:           python-%{srcname}
Version:        2.0.0
Release:        1%{?dist}
Summary:        Python module for determining appropriate platform-specific dirs
License:        MIT
URL:            https://github.com/platformdirs/platformdirs
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-six
BuildRequires:  python3-setuptools


%description %{common_description}


%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel


%description -n python3-%{srcname} %{common_description}


%prep
%autosetup -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires -t


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
* Mon Jul 12 2021 Carl George <carl@george.computer> - 2.0.0-1
- Initial package rhbz#1981607
