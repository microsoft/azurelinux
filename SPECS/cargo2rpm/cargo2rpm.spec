%bcond_without check
 
Name:           cargo2rpm
Version:        0.1.15
Release:        1%{?dist}
Summary:        Translation layer between cargo and RPM
License:        MIT
 
URL:            https://pagure.io/fedora-rust/cargo2rpm
Source:         %{url}/archive/%{version}/cargo2rpm-%{version}.tar.gz
 
BuildArch:      noarch
 
BuildRequires:  python3-devel
%if %{with check}
BuildRequires:  %{py3_dist pytest}
%endif
 
Requires:       cargo
 
%description
cargo2rpm implements a translation layer between cargo and RPM. It
provides a CLI interface (for implementing RPM macros and generators)
and a Python API (which rust2rpm is built upon).
 
%prep
%autosetup -p1
 
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
* Wed Jan 24 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 0.1.15-1
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- License verified.
