# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name smbprotocol

Name:           python-%{pypi_name}
Version:        1.15.0
Release: 4%{?dist}
Summary:        Interact with a server using the SMB 2/3 Protocol

License:        MIT
URL:            https://github.com/jborean93/smbprotocol
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
SMB is a network file sharing protocol and has numerous iterations
over the years. This library implements the SMBv2 and SMBv3 protocol
based on the MS-SMB2 document.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3dist(cryptography)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-cov)
BuildRequires:  python3dist(pyspnego)
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
SMB is a network file sharing protocol and has numerous iterations
over the years. This library implements the SMBv2 and SMBv3 protocol
based on the MS-SMB2 document.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%pyproject_check_import
%pytest -v tests \
  -k "not reset_connection \
  and not config_domain \
  and not message \
  and not dfs"

%files -n python3-%{pypi_name}  -f %{pyproject_files}
%license LICENSE
%doc README.md
%{python3_sitelib}/smbclient/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.15.0-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.15.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Tom Rix <Tom.Rix@amd.com> - 1.15.0-1
- Update to 1.15.0

* Mon Jul 14 2025 Tom Rix <Tom.Rix@amd.com> - 1.9.0-11
- Use pyproject macros

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.9.0-10
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.9.0-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.9.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Aug 19 2022 Fabian Affolter <mail@fabian-affolter.ch> - 1.9.0-1
- Update to latest upstream release 1.9.0 (closes rhbz#2113654, closes #2099111)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 07 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.1.0-1
- Initial package for Fedora
