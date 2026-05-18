Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%bcond_without check
 
Name:           cargo2rpm
Version:        0.3.2
Release:        1%{?dist}
Summary:        Translation layer between cargo and RPM
License:        MIT
 
URL:            https://codeberg.org/rust2rpm/cargo2rpm
Source:         %{url}/archive/v%{version}.tar.gz
 
BuildArch:      noarch

BuildRequires:  python3-pip 
BuildRequires:  python3-devel
BuildRequires:  python3-wheel
%if %{with check}
BuildRequires:  %{py3_dist pytest}
%endif

Requires:       cargo
 
%description
cargo2rpm implements a translation layer between cargo and RPM. It
provides a CLI interface (for implementing RPM macros and generators)
and a Python API (which rust2rpm is built upon).
 
%prep
%autosetup -n cargo2rpm -p1
 
%generate_buildrequires
%pyproject_buildrequires
%build
%pyproject_wheel
%install
%pyproject_install
%pyproject_save_files cargo2rpm
 
%check
%pyproject_check_import
%if %{with check}
%pytest
%endif
 
%files -f %{pyproject_files}
%doc README.md
%doc CHANGELOG.md
%{_bindir}/cargo2rpm
 
%changelog
* Sat Dec 20 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 0.3.2-1
- Initial CBL-Mariner import from Fedora 44 (license: MIT).
- License verified
