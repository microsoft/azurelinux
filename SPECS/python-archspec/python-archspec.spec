%global srcname archspec
%global _description %{expand:
Archspec aims at providing a standard set of human-understandable labels for
various aspects of a system architecture like CPU, network fabrics, etc. and
APIs to detect, query and compare them.
This project grew out of Spack and is currently under active development. At
present it supports APIs to detect and model compatibility relationships among
different CPU microarchitectures.}
Summary:        A library to query system architecture
Name:           python-%{srcname}
Version:        0.2.5
Release:        3%{?dist}
License:        Apache-2.0 OR MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/archspec/archspec
Source:         %{pypi_source}
BuildRequires:  python3-devel
BuildRequires:  python3-jsonschema
BuildRequires:  python3-pip
BuildRequires:  python3-poetry
# For tests
BuildRequires:  python3-pytest
BuildArch:      noarch

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -p1 -n %{srcname}-%{version}
rm -rf archspec/json/.git*


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
%pytest -v


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.*
%{_bindir}/archspec
%license LICENSE-APACHE

%changelog
* Tue Apr 01 2025 Riken Maharjan <rmaharjan@microsoft.com> - 0.2.5-3
- Initial Azure Linux import from Fedora 42 (license: MIT)
- License Verified

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 16 2024 Orion Poplawski <orion@nwra.com> - 0.2.5-1
- Update to 0.2.5

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 0.2.4-2
- Rebuilt for Python 3.13

* Tue May 07 2024 Orion Poplawski <orion@nwra.com> - 0.2.4-1
- Update to 0.2.4

* Wed Mar 20 2024 Orion Poplawski <orion@nwra.com> - 0.2.3-2
- Run tests

* Tue Mar 19 2024 Orion Poplawski <orion@nwra.com> - 0.2.3-1
- Update to 0.2.3

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 02 2023 Orion Poplawski <orion@nwra.com> - 0.2.2-1
- Initial Fedora package
