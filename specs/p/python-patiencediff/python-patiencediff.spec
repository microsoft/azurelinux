# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name patiencediff
Name:           python-patiencediff
Version:        0.2.15
Release: 8%{?dist}
Summary:        Python implementation of the patiencediff algorithm

License:        GPL-2.0-or-later
URL:            https://www.breezy-vcs.org/
Source:         %{pypi_source}

BuildRequires:  gcc
BuildRequires:  python3-devel

%global _description %{expand:
This package contains the implementation of the patiencediff algorithm, as
first described by Bram Cohen. Like Python's difflib, this module provides
both a convenience unified_diff function for the generation of unified diffs of
text files as well as a SequenceMatcher that can be used on arbitrary
lists. Patiencediff provides a good balance of performance, nice output for
humans, and implementation simplicity.}

%description %_description

%package -n     python3-patiencediff
Summary:        %{summary}

%description -n python3-patiencediff %_description


%prep
%autosetup -p1 -n patiencediff-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files patiencediff

%check
%py3_test_envvars %{python3} -m unittest patiencediff.test_patiencediff

%files -n python3-patiencediff -f %{pyproject_files}
%doc README.rst
%{_bindir}/patiencediff

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.2.15-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.2.15-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.2.15-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 13 2024 Ondřej Pohořelský <opohorel@redhat.com> - 0.2.15-1
- Update to 0.2.15
- Resolves: rhbz#2279324

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.2.14-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 18 2023 Ondřej Pohořelský <opohorel@redhat.com> - 0.2.14-1
- Update to 0.2.14
- Resolves: rhbz#2239324

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.2.13-2
- Rebuilt for Python 3.12

* Tue Feb 28 2023 Ondřej Pohořelský <opohorel@redhat.com> - 0.2.13-1
- Update to 0.2.13
- Resolves: rhbz#2167981

* Mon Jan 16 2023 Ondřej Pohořelský <opohorel@redhat.com> - 0.2.12-1
- Update to 0.2.12
- Migrate to the newest python macros
- Convert license to SPDX
- Resolves: rhbz#2137836

* Wed Oct 19 2022 Ondřej Pohořelský <opohorel@redhat.com> - 0.2.6-1
- Update to 0.2.6
- Resolves: rhbz#2135936

* Wed Sep 07 2022 Ondřej Pohořelský <opohorel@redhat.com> - 0.2.3-1
- Update to 0.2.3
- Resolves: rhbz#2124925

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.2.2-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.2.2-2
- Rebuilt for Python 3.10

* Mon Mar 29 2021 Ondřej Pohořelský <opohorel@redhat.com> - 0.2.2-1
- Update to 0.2.2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 15 2020 Ondřej Pohořelský <opohorel@redhat.com> - 0.2.1-1
- Initial package.
