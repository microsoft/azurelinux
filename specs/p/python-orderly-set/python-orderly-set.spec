# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name orderly-set
%global pypi_version 5.5.0

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release: 4%{?dist}
Summary:        A package containing multiple implementations of Ordered Set
License:        MIT
URL:            https://github.com/seperman/orderly-set
Source0:        https://github.com/seperman/orderly-set/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel

%description
Orderly Set is a package containing multiple implementations of
Ordered Set.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
Orderly Set is a package containing multiple implementations
of Ordered Set.

%prep
%autosetup -n orderly-set-%{pypi_version}

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l orderly_set

%check
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.5.0-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.5.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Romain Geissler <romain.geissler@amadeus.com> - 5.5.0-1
- Update to upstream version 5.5.0 (rhbz#2377959).

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 5.4.1-2
- Rebuilt for Python 3.14

* Wed May 07 2025 Romain Geissler <romain.geissler@amadeus.com> - 5.4.1-1
- Update to upstream version 5.4.1.

* Mon Mar 31 2025 Romain Geissler <romain.geissler@amadeus.com> - 5.3.0-1
- Update to upstream version 5.3.0.

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 30 2024 Susi Lehtola <susi.lehtola@iki.fi> - 5.2.2-3
- Review fix: switch to GitHub upstream to include license file.

* Thu Sep 12 2024 Susi Lehtola <susi.lehtola@iki.fi> - 5.2.2-2
- Added BR: python3-wheel required by tests.

* Wed Sep 04 2024 Susi Lehtola <susi.lehtola@iki.fi> - 5.2.2-1
- Initial package.
