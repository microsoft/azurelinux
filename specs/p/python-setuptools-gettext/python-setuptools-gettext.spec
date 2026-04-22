# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-setuptools-gettext
Version:        0.1.14
Release: 7%{?dist}
Summary:        Setuptools gettext extension plugin

License:        GPL-2.0-or-later
URL:            https://github.com/breezy-team/setuptools-gettext
Source:         %{pypi_source setuptools_gettext}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}
# Enables tests/test_example.py::test_update_pot
BuildRequires:  gettext

%global _description %{expand:
Setuptools helpers for gettext. Compile .po files into .mo files.}

%description %{_description}

%package -n     python3-setuptools-gettext
Summary:        %{summary}

%description -n python3-setuptools-gettext %{_description}

%prep
%autosetup -n setuptools_gettext-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l setuptools_gettext

%check
%pyproject_check_import
# -rs: print reasons for skipped tests
%pytest -v -rs

%files -n python3-setuptools-gettext -f %{pyproject_files}
%doc README.md

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.1.14-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.1.14-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.1.14-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.1.14-1
- Update to 0.1.14 (close RHBZ#2260681)

* Fri Nov 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.1.8-7
- Port to pyproject-rpm-macros (”new Python guidelines”)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.1.8-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 5 2024 Björn Lindström <bkhl@elektrubadur.se> - 0.1.8-2
- Remove patching of setuptools dependency, no longer needed as setuptools in
  rawhide new enough.

* Fri Jan 5 2024 Björn Lindström <bkhl@elektrubadur.se> - 0.1.8-1
- Updated to 0.1.8.
- Removed patch for clarifying license, as that has now been done upstream.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.1.3-3
- Rebuilt for Python 3.12

* Thu May 4 2023 Björn Lindström <bkhl@elektrubadur.se> - 0.1.3-2
- Add missing dist tag in release number.

* Sat Apr 29 2023 Björn Lindström <bkhl@elektrubadur.se> - 0.1.3-1
- Initial package.
