# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname pytest-httpserver

%global desc %{expand: \
This library is designed to help to test http clients without contacting
the real http server. In other words, it is a fake http server which is
accessible via localhost can be started with the pre-defined expected
http requests and their responses.}

Name:		python-%{srcname}
Version:	1.0.8
Release: 12%{?dist}
Summary:	HTTP server for pytest

License:	MIT
URL:		https://github.com/csernazs/pytest-httpserver
Source0:	%{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

Patch0:		pyproject.patch

# https://fedoraproject.org/wiki/Changes/DeprecatePythonToml
# Use tomllib instead of toml (used only in tests)
# https://github.com/csernazs/pytest-httpserver/pull/377
Patch1:		tomllib.patch

BuildArch:	noarch

BuildRequires:	python3-devel
BuildRequires:	python3-pytest
BuildRequires:	python3-requests
BuildRequires:	pyproject-rpm-macros

%description
%{desc}

%package -n python3-%{srcname}
Summary:	%{summary}

%description -n python3-%{srcname} %desc

%prep
%autosetup -p1 -n %{srcname}-%{version}

# Remove unnecessary dependencies
sed -i '/flake8/d' pyproject.toml
sed -i '/pytest-cov/d' pyproject.toml
sed -i '/coverage/d' pyproject.toml
sed -i '/mypy/d' pyproject.toml
sed -i '/types-requests/d' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires -x test

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pytest_httpserver

%check
%pytest

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md CHANGES.rst CONTRIBUTION.md

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.8-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.8-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.0.8-8
- Rebuilt for Python 3.14

* Tue Feb 04 2025 Miro Hrončok <mhroncok@redhat.com> - 1.0.8-7
- Use tomllib instead of toml (used only in tests)
- https://fedoraproject.org/wiki/Changes/DeprecatePythonToml

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.0.8-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 07 2023 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.0.8-1
- pytest-httpserver 1.0.8

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Python Maint <python-maint@redhat.com> - 1.0.4-4
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 30 2022 Ali Erdinc Koroglu <aekoroglu@fedorapackage.org> - 1.0.4-1
- Initial package
