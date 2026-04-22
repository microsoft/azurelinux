# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond tests 1
%global forgeurl https://github.com/repo-helper/hatch-requirements-txt

Name:           python-hatch-requirements-txt
Version:        0.4.1
%forgemeta
Release: 9%{?dist}
Summary:        Hatchling plugin to read project dependencies from requirements.txt

License:        MIT
URL:            %{forgeurl}
Source:         %{forgesource}

# Update tests for latest hatchling [i.e., 1.22.x]
# %%{forgeurl}/commit/1aa21b86db3503ed46683fa7af748d7aa1e853e1
# Cherry-picked to 0.4.1; changes to files in .github/ managed by repo_helper
# omitted.
Patch:          0001-Update-tests-for-latest-hatchling.patch

BuildArch:      noarch

BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  %{py3_dist coincidence}
BuildRequires:  %{py3_dist pkginfo}
BuildRequires:  %{py3_dist pytest}
%endif


%description
%{summary}.


%package -n python3-hatch-requirements-txt
Summary:        %{summary}

%description -n python3-hatch-requirements-txt
%{summary}.


%prep
%autosetup -p1 %{forgesetupargs}
# pytest-timeout is not needed to run tests in the RPM build environment
sed -i '/^timeout =/d' tox.ini
# Remove unnecessary shebangs
find hatch_requirements_txt/ -type f ! -executable -name '*.py' -print \
    -exec sed -i -e '1{\@^#!.*@d}' '{}' +


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files hatch_requirements_txt


%check
%pyproject_check_import
%if %{with tests}
%pytest
%endif


%files -n python3-hatch-requirements-txt -f %{pyproject_files}
%license LICENSE
%doc README.rst


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.4.1-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.4.1-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.4.1-5
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 0.4.1-2
- Rebuilt for Python 3.13

* Tue Mar 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.1-1
- Update to 0.4.1

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Maxwell G <maxwell@gtmx.me> - 0.4.0-2
- Fix test failures with latest hatchling release

* Thu Oct 19 2023 Maxwell G <maxwell@gtmx.me> - 0.4.0-1
- Initial package. Closes rhbz#2244976.
