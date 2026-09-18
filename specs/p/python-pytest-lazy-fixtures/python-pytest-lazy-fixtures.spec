## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name pytest-lazy-fixtures
%global package_dir_name pytest_lazy_fixtures

Name:           python-%{pypi_name}
Version:        1.1.4
Release:        %autorelease
Summary:        Library to use fixtures in @pytest.mark.parametrize

License:        MIT
URL:            https://github.com/dev-petrov/pytest-lazy-fixtures
Source0:        https://files.pythonhosted.org/packages/source/p/pytest-lazy-fixtures/pytest_lazy_fixtures-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-poetry-core
BuildRequires:  python3dist(pytest)

%global _description %{expand:
Use your fixtures in @pytest.mark.parametrize

This project was inspired by pytest-lazy-fixture.

Improvements that have been made in this project:

    You can use fixtures in any data structures
    You can access the attributes of fixtures
    You can use functions in fixtures}

%description %_description

%package -n python3-%{pypi_name}
Summary: Library to use fixtures in @pytest.mark.parametrize

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{package_dir_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pytest_lazy_fixtures

%check
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Tue Jun 03 2025 Ian Wienand  <iwienand@redhat.com> - 1.1.4-%autorelease
- Update to 1.1.4 (Closes: #2298529)

* Thu Jul 18 2024 Ian Wienand <iwienand@redhat.com> - 1.1.0-%autorelease
- Update to 1.1.0 (Closes: #2298529)

* Tue May  7 2024 Ian Wienand <iwienand@redhat.com> - 1.0.7-1
- Initial package
