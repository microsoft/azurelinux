# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond tests 1
%global forgeurl https://github.com/python-coincidence/coincidence

Name:           python-coincidence
Version:        0.6.6
%forgemeta
Release: 7%{?dist}
Summary:        Helper functions for pytest

License:        MIT
URL:            %{forgeurl}
Source:         %{forgesource}
Patch:          Use-setuptools-instead-of-whey-as-build-backend.patch
Patch:          test_regressions-use-tomllib-instead-of-toml.patch

BuildArch:      noarch

BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  %{py3_dist pytest}
%endif


%description
%{summary}.


%package -n python3-coincidence
Summary:        %{summary}

%description -n python3-coincidence
%{summary}.


%prep
%autosetup -p1 %{forgesetupargs}
# pytest-timeout is not needed to run tests in the RPM build environment
sed -i '/^timeout =/d' tox.ini
# Remove unnecessary shebangs
find coincidence/ -type f ! -executable -name '*.py' -print \
    -exec sed -i -e '1{\@^#!.*@d}' '{}' +


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files coincidence


%check
%pyproject_check_import
%if %{with tests}
%pytest
%endif


%files -n python3-coincidence -f %{pyproject_files}
%license LICENSE
%doc README.rst


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.6.6-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.6.6-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.6.6-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jul 23 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.6.6-1
- Update to 0.6.6
Fixes: rhbz#2267729

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 0.6.5-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 19 2023 Maxwell G <maxwell@gtmx.me> - 0.6.5-1
- Initial package. Closes rhbz#2244975.
