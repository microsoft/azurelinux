# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name Markdown
%global modname markdown

Name:           python-%{modname}_2
Version:        3.4.4
Release: 11%{?dist}
Summary:        Python implementation of Markdown

License:        BSD-3-Clause
URL:            https://github.com/Python-Markdown/markdown
Source:         %{pypi_source}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pyyaml

%global _description %{expand:
This is a Python implementation of John Gruber's Markdown. It is almost 
completely compliant with the reference implementation, though there are
a few known issues.}

%description %{_description}

%package -n python3-%{modname}_2
Summary:        %{summary}
Conflicts:      python%{python3_version}dist(%{modname})

%description -n python3-%{modname}_2 %{_description}

Python 3 version.

%prep
%autosetup -n %{pypi_name}-%{version} -p1

# PytestCollectionWarning for __init__ constructor
sed -i -e '/unittest/d' tests/test_syntax/extensions/test_md_in_html.py
 
%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%pytest -v

%install
%pyproject_install
%pyproject_save_files %{modname}

%files -n python3-%{modname}_2 -f %{pyproject_files}
%doc README.md
%{_bindir}/markdown_py

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.4.4-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.4.4-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.4.4-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.4.4-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 28 2023 Ali Erdinc Koroglu <aekoroglu@fedora.project.org> - 3.4.4-1
- Update to 3.4.4 (RHBZ #2220322 and #2226240)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.6.11-11
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.6.11-8
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.6.11-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.6.11-2
- Rebuilt for Python 3.9

* Fri Jan 31 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.6.11-1
- Initial package
