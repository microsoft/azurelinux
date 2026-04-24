# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _description %{expand:
Versioneer is a tool to automatically update version strings (in setup.py and
the conventional 'from PROJECT import _version' pattern) by asking your
version-control system about the current tree.}

Name:           python-versioneer
Version:        0.29
Release: 8%{?dist}
Summary:        Easy VCS-based management of project version strings

License:        Unlicense
URL:            https://github.com/warner/python-versioneer
Source0:        %{pypi_source versioneer}

BuildArch:      noarch
 
BuildRequires:  python3-devel

%description %_description

%package -n     python3-versioneer
Summary:        %{summary}

%description -n python3-versioneer %_description

%pyproject_extras_subpkg -n python3-versioneer toml

%prep
%autosetup -n versioneer-%{version}

%generate_buildrequires
%pyproject_buildrequires -x toml

%build
%pyproject_wheel

%install
%pyproject_install
# Remove the unwanted shebang from the amalgamated versioneer.py file:
sed -r -i '1{/^#!/d}' %{buildroot}%{python3_sitelib}/versioneer.py
%pyproject_save_files -l versioneer

%check
# Based on tox.ini; but we do not use tox, because tox.ini has too many linting
# tests and other unwanted dependencies.
%{python3} setup.py make_versioneer
%{python3} -m unittest discover test
# Some of these do not work; it is not clear that this indicates a real
# problem. We would need at least “BuildRequires: git-core” if they did work.
#{python3} test/git/test_git.py -v
# These generally require python3dist(virtualenv) and network access.
#{python3} test/git/test_invocations.py -v

%files -n python3-versioneer -f %{pyproject_files}
%doc README.md
%doc details.md
%{_bindir}/versioneer

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.29-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.29-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.29-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.29-1
- Update to 0.29 (close RHBZ#2221228)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.28-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.28-2
- Rebuilt for Python 3.12

* Fri Mar 03 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.28-1
- Update to 0.28
- Port to pyproject-rpm-macros
- Add metapackage for “toml” extra
- License has changed from CC0-1.0 (spec file had Public Domain) to Unlicense
- Remove obsolete posttrans scriptlet
- Add details.md to documentation

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.21-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 02 2021 Orion Poplawski <orion@nwra.com> - 0.21-1
- Update to 0.21
- Own egg-info directory and cleanup previous egg-info directory

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.18-8
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.18-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 31 2019 Mukundan Ragavan <nonamedotc@gmail.com> - 0.18-3
- rebuild

* Mon Dec 30 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.18-2
- Address changes from package review

* Sun Dec 22 2019 Mukundan Ragavan <nonamedotc@gmail.com> - 0.18-1
- Initial package.
