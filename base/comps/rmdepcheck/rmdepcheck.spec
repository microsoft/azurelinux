Name:           rmdepcheck
Version:        1.1.0
Release:        %autorelease
Summary:        RPM reverse-dependency and installability checker
License:        GPL-3.0-or-later
URL:            https://codeberg.org/AdamWill/rmdepcheck
Source0:        %{pypi_source rmdepcheck}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  curl
BuildRequires:  dnf5
BuildRequires:  dnf5-plugins
BuildRequires:  zstd

Requires:       curl
Requires:       dnf5
Requires:       dnf5-plugins
Requires:       python3-rmdepcheck = %{version}-%{release}
Requires:       zstd

%description
Rmdepcheck compares a baseline RPM repository with a candidate repository to
detect reverse-dependency and installability regressions.

%package -n python3-rmdepcheck
Summary:        Python module for rmdepcheck
%{?python_provide:%python_provide python3-rmdepcheck}

%description -n python3-rmdepcheck
This package provides the Python module used by rmdepcheck.

%prep
%autosetup -n rmdepcheck-%{version}
sed -i 's/"setuptools-git", //' pyproject.toml
sed -i 's/"dnf"/"dnf5"/g' rmdepcheck.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files rmdepcheck

%check
# The upstream fixture hard-codes its maintainer's checkout path.
%pytest -q -k "not test_e2e_removes"

%files
%{_bindir}/rmdepcheck

%files -n python3-rmdepcheck -f %{pyproject_files}
%license COPYING
%doc README.md CHANGELOG.md

%changelog
%autochangelog
