# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-hatch-jupyter-builder
Version:        0.9.1
Release: 6%{?dist}
Summary:        A hatch plugin to help build Jupyter packages
License:        BSD-3-Clause
URL:            https://pypi.org/project/hatch-jupyter-builder/
Source:         %{pypi_source hatch_jupyter_builder}

BuildArch:      noarch
BuildRequires:  python3-devel
# Test deps, upstream contains pre-commit, pytest-cov etc.
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-mock
BuildRequires:  (python3-tomli if python3 < 3.11)

%global _description %{expand:
This provides a build hook plugin for Hatch that adds
a build step for use with Jupyter packages.}


%description %_description

%package -n     python3-hatch-jupyter-builder
Summary:        %{summary}

%description -n python3-hatch-jupyter-builder %_description


%prep
%autosetup -p1 -n hatch_jupyter_builder-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files hatch_jupyter_builder


%check
# Skipped tests installs from internet
%pytest -k "not test_hatch_build"


%files -n python3-hatch-jupyter-builder -f %{pyproject_files}
%doc README.md
%{_bindir}/hatch-jupyter-builder


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.9.1-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.9.1-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.9.1-2
- Rebuilt for Python 3.14

* Fri Apr 25 2025 Lumír Balhar <lbalhar@redhat.com> - 0.9.1-1
- Update to 0.9.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.9.0-2
- Rebuilt for Python 3.13

* Tue Mar 12 2024 Lumír Balhar <lbalhar@redhat.com> - 0.9.0-1
- Update to 0.9.0 (rhbz#2269156)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 13 2023 Miro Hrončok <mhroncok@redhat.com> - 0.8.3-4
- Avoid an unneeded dependency on python3-tomli
- Use tomllib from the Python 3.11+ standard library instead

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.8.3-2
- Rebuilt for Python 3.12

* Mon Apr 24 2023 Lumír Balhar <lbalhar@redhat.com> - 0.8.3-1
- Update to 0.8.3 (rhbz#2187226)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 14 2022 Lumír Balhar <lbalhar@redhat.com> - 0.8.2-1
- Update to 0.8.2 (rhbz#2152911)

* Mon Nov 28 2022 Lumír Balhar <lbalhar@redhat.com> - 0.8.1-1
- Initial package
