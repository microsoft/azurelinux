# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name resolvelib
%global forgeurl https://github.com/sarugaku/resolvelib
%bcond tests 1

Name:           python-%{pypi_name}
Version:        1.0.1
%global tag %{version}
%forgemeta
Release: 12%{?dist}
Summary:        Resolve abstract dependencies into concrete ones

License:        ISC
URL:            %{forgeurl}
Source:         %{forgesource}
# Avoid commentjson/json5 build dependency just for a couple tests
Patch:          %{url}/pull/141.patch#/remove-commentjson-dep.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%global _description %{expand:
ResolveLib at the highest level provides a Resolver class that
includes dependency resolution logic. You give it some things, and a little
information on how it should interact with them, and it will spit out a
resolution result. Intended Usage :: import resolvelib Things I want to
resolve. requirements [...] Implement logic so the resolver understands the
requirement format. class...}

%description %_description


%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %{_description}


%prep
%autosetup %{forgesetupargs} -p1


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-x test}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%pytest -v


%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.1-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.1-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.0.1-8
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.1-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 07 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.1-2
- Simplify build dependencies

* Fri Oct 20 2023 Maxwell G <maxwell@gtmx.me> - 1.0.1-1
- Update to 1.0.1.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.5.5-8
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.5.5-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.5.5-2
- Rebuilt for Python 3.10

* Sat Apr 10 2021 Kevin Fenzi <kevin@scrye.com> - 0.5.5-1
- Initial package.
