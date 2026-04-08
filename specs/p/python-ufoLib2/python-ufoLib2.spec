# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# python-cattrs is too old in Fedora 40:
%bcond cattrs %{undefined fc40}

Name:           python-ufoLib2
Version:        0.18.1
Release:        4%{?dist}
Summary:        A library to deal with UFO font sources

License:        Apache-2.0
URL:            https://github.com/fonttools/ufoLib2
Source:         %{pypi_source ufolib2 %{version}}

BuildArch:      noarch

BuildRequires:  python3-devel

# Required for running tests
BuildRequires:  python3dist(pytest)

%global _description %{expand:
ufoLib2 is meant to be a thin representation of the Unified Font Object (UFO)
version 3 data model, intended for programmatic manipulation and fast batch
processing of UFOs.}

%description %_description

%package -n python3-ufoLib2
Summary:        %{summary}

%description -n python3-ufoLib2 %_description

%pyproject_extras_subpkg -n python3-ufoLib2 lxml%{?with_cattrs: converters json msgpack}

%prep
%autosetup -n ufolib2-%{version}

%generate_buildrequires
%pyproject_buildrequires -x lxml%{?with_cattrs:,converters,json,msgpack}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l ufoLib2

%check
%pyproject_check_import %{?!with_cattrs:-e ufoLib2.converters -e ufoLib2.serde.json -e ufoLib2.serde.msgpack}
%pytest -v

%files -n python3-ufoLib2 -f %{pyproject_files}
%doc README.md

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.18.1-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.18.1-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Parag Nemade <pnemade AT redhat DOT com> - 0.18.1-1
- Update to 0.18.1 version (#2379276)

* Sun Jun 15 2025 Python Maint <python-maint@redhat.com> - 0.17.1-2
- Rebuilt for Python 3.14

* Wed Jan 22 2025 Parag Nemade <pnemade AT redhat DOT com> - 0.17.1-1
- Update to 0.17.1 version (#2339116)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.0-1
- Update to 0.17.0 (close RHBZ#2322970)
- Don’t package a duplicate LICENSE file; assert one is found and handled
- Add missing extras metpackages

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 17 2024 Python Maint <python-maint@redhat.com> - 0.16.0-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 Parag Nemade <pnemade AT redhat DOT com> - 0.16.0-2
- rewrite spec for pyproject macros

* Thu Aug 03 2023 Parag Nemade <pnemade AT redhat DOT com> - 0.16.0-1
- Update to 0.16.0 version (#2225476)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Python Maint <python-maint@redhat.com> - 0.7.1-13
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 05 2022 Parag Nemade <pnemade AT redhat DOT com> - 0.7.1-11
- Update license tag to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 0.7.1-9
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.7.1-6
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-3
- Rebuilt for Python 3.9

* Tue May 19 2020 Parag Nemade <pnemade AT redhat DOT com> - 0.7.1-2
- Drop the Requires: as they will be picked automatically
- Rename spec to python-ufoLib2.spec

* Thu May 07 2020 Parag Nemade <pnemade AT redhat DOT com> - 0.7.1-1
- Initial packaging

