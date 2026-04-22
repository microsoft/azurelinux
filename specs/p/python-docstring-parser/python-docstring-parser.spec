# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname docstring-parser

Name:           python-%{srcname}
Version:        0.17.0
Release: 4%{?dist}
Summary:        Parse Python docstrings
License:        MIT
URL:            https://github.com/rr-/docstring_parser
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}


%global _description %{expand:
Parse Python docstrings. Currently support ReST, Google, Numpydoc-style and Epydoc docstrings.}


%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname} %{_description}


%prep
%autosetup -p 1 -n docstring_parser-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files docstring_parser


%check
%{pytest}


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md
%license LICENSE.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.17.0-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.17.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Sat Aug 02 2025 Federico Pellegrin <fede@evolware.org> - 0.17.0-1
- Bump to 0.17.0, remove upstreamed patch

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.16-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 04 2024 Federico Pellegrin <fede@evolware.org> - 0.16-1
- Bump to 0.16, fix build for Python 3.14(pre)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.15-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 0.15-2
- Rebuilt for Python 3.12

* Wed Jan 18 2023 Piotr Szubiakowski <pszubiak@eso.org> - 0.15-1
- Update to 0.15

* Wed Jul 20 2022 Piotr Szubiakowski <pszubiak@eso.org> - 0.14.1-2
- Apply code review fixes

* Thu May 19 2022 Piotr Szubiakowski <pszubiak@eso.org> - 0.14.1-1
- Init
