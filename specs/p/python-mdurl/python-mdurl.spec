# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-mdurl
Version:        0.1.2
Release:        13%{?dist}
Summary:        Markdown URL utilities

# SPDX
License:        MIT
URL:            https://github.com/executablebooks/mdurl
Source0:        %{url}/archive/%{version}/mdurl-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
URL utilities for markdown-it parser.}


%description %_description

%package -n     python3-mdurl
Summary:        %{summary}

%description -n python3-mdurl %_description


%prep
%autosetup -p1 -n mdurl-%{version}

# Remove coverage from the test requirements
sed -i "s/pytest-cov//" tests/requirements.txt


%generate_buildrequires
%pyproject_buildrequires tests/requirements.txt


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files mdurl


%check
%pytest


%files -n python3-mdurl -f %{pyproject_files}
%doc README.md
%license LICENSE


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.1.2-13
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.1.2-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.1.2-10
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 0.1.2-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 0.1.2-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Oct 13 2022 Karolina Surma <ksurma@redhat.com> - 0.1.2-1
- Update to 0.1.2
Resolves: rhbz#2118132

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 0.1.1-2
- Rebuilt for Python 3.11

* Tue Apr 19 2022 Lumír Balhar <lbalhar@redhat.com> - 0.1.1-1
- Update to 0.1.1
Resolves: rhbz#2074703

* Mon Jan 31 2022 Karolina Surma <ksurma@redhat.com> - 0.1.0-1
- Initial package
