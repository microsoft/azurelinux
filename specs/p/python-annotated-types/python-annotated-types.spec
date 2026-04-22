# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# Copyright (C) Fedora Project Authors
# SPDX-License-Identifier: MIT
# License text: https://spdx.org/licenses/MIT

%bcond tests 1

Name:           python-annotated-types
Version:        0.7.0
Release: 9%{?dist}
Summary:        Reusable constraint types to use with typing.Annotated

License:        MIT
%global forgeurl https://github.com/annotated-types/annotated-types
URL:            %{forgeurl}
%forgemeta
Source:         %{forgesource}

BuildArch:      noarch

BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  %{py3_dist pytest}
%endif

%global _description %{expand:
PEP-593 added typing.Annotated as a way of adding context-specific metadata to
existing types, and specifies that Annotated[T, x] should be treated as T by
any tool or library without special logic for x.

This package provides metadata objects which can be used to represent common
constraints such as upper and lower bounds on scalar values and collection
sizes, a Predicate marker for runtime checks, and descriptions of how we intend
these metadata to be interpreted. In some cases, we also note alternative
representations which do not require this package.}

%description %_description


%package -n python3-annotated-types
Summary:        %{summary}

%description -n python3-annotated-types %{_description}


%prep
%autosetup -p1 %{forgesetupargs}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l annotated_types


%check
%if %{with tests}
%pytest
%endif


%files -n python3-annotated-types -f %{pyproject_files}
%doc README.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.7.0-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.7.0-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.7.0-5
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.7.0-2
- Rebuilt for Python 3.13

* Tue May 21 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.0-1
- Update to 0.7.0 (close RHBZ#2282026)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.0-2
- Assert %%pyproject_files contains a license file; don’t package a duplicate

* Fri Oct 06 2023 Maxwell G <maxwell@gtmx.me> - 0.6.0-1
- Update to 0.6.0. Fixes rhbz#2242535.

* Fri Sep 08 2023 Maxwell G <maxwell@gtmx.me> - 0.5.0-1
- Initial package. Closes rhbz#2238391.
