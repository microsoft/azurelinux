Name:           python-pyproject-api
Version:        1.6.1
Release:        6%{?dist}
Summary:        API to interact with the python pyproject.toml based projects
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        MIT
URL:            https://pyproject-api.readthedocs.org
Source0:        https://files.pythonhosted.org/packages/source/p/pyproject-api/pyproject_api-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-pip
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-wheel
BuildRequires:  python3-hatchling
BuildRequires:  python3-packaging
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-mock
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-pathspec
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-trove-classifiers

%global _description %{expand:
API to interact with the python pyproject.toml based projects.}

%description %_description

%package -n     python3-pyproject-api
Summary:        %{summary}

%description -n python3-pyproject-api %_description

%prep
%autosetup -n pyproject_api-%{version}
# Remove unneeded testing deps
sed -i "/covdefaults/d;/pytest-cov/d" pyproject.toml

%generate_buildrequires
%pyproject_buildrequires -w -x testing

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pyproject_api

%check
%pytest --ignore=tests/test_frontend_setuptools.py

%files -n python3-pyproject-api -f %{pyproject_files}
%doc README.md
%license %{python3_sitelib}/pyproject_api-%{version}.dist-info/licenses/LICENSE

%changelog
* Fri Feb 21 2025 Jyoti kanase <v-jykanase@microsoft.com> -  1.6.1-6
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.6.1-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 23 2023 Miro Hrončok <miro@hroncok.cz> - 1.6.1-1
- Update to 1.6.1
- Fixes: rhbz#2215138

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.5.1-2
- Rebuilt for Python 3.12

* Mon Mar 13 2023 Lumir Balhar <lbalhar@redhat.com> - 1.5.1-1
- Update to 1.5.1 (rhbz#2177516)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Lumir Balhar <lbalhar@redhat.com> - 1.5.0-1
- Update to 1.5.0 (rhbz#2161818)

* Thu Jan 05 2023 Lumir Balhar <lbalhar@redhat.com> - 1.4.0-1
- Update to 1.4.0 (rhbz#2158206)

* Tue Jan 03 2023 Lumír Balhar <lbalhar@redhat.com> - 1.3.0-1
- Update to 1.3.0 (rhbz#2157941)

* Wed Dec 07 2022 Lumír Balhar <lbalhar@redhat.com> - 1.2.1-1
- Update to 1.2.1 (rhbz#2150693)

* Tue Nov 01 2022 Lumír Balhar <lbalhar@redhat.com> - 1.1.2-1
- Update to 1.1.2
Resolves: rhbz#2138752

* Tue Sep 13 2022 Lumír Balhar <lbalhar@redhat.com> - 1.1.1-1
- Update to 1.1.1
Resolves: rhbz#2126242

* Sun Sep 11 2022 Lumír Balhar <lbalhar@redhat.com> - 1.1.0-1
- Update to 1.1.0
Resolves: rhbz#2125780

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.1.1-2
- Rebuilt for Python 3.11

* Mon Feb 07 2022 Lumír Balhar <lbalhar@redhat.com> - 0.1.1-1
- Initial package

