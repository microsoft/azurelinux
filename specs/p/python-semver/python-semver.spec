# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global modname semver

Name:           python-%{modname}
Version:        3.0.4
Release:        4%{?dist}
Summary:        Python helper for Semantic Versioning

License:        BSD-3-Clause
URL:            https://github.com/python-semver/python-semver
Source0:        %{pypi_source semver}

BuildArch:      noarch

BuildRequires:  python3-devel
# test requirements
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-cov)

%global _description %{expand:
A Python module for semantic versioning. Simplifies comparing versions.}

%description %{_description}

%package -n     python3-%{modname}
Summary:        %{summary}

%description -n python3-%{modname}
%{_description}

%prep
%autosetup -n %{modname}-%{version} -p 1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files 'semver'

%check
%pytest

%files -n python3-%{modname} -f %{pyproject_files}
%license LICENSE.txt
%doc README.rst CHANGELOG.rst
%{_bindir}/pysemver

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.0.4-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.0.4-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 12 2025 Jeremy Cline <jeremy@linux.microsoft.com> - 3.0.4-1
- Update to v3.0.4 (close RHBZ#2338733)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.0.2-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.2-1
- Update to 3.0.2 (close RHBZ#2180207)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.0.1-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 David Bold <davidsch@fedoraproeject.org> - 3.0.1-1
- Update to 3.0.1
- Fix FTBFS

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2.13.0-10
- Rebuilt for Python 3.12

* Thu Apr 06 2023 Felix Wang <topazus@outlook.com> - 3.0.0-1
- Update to 3.0.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.13.0-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.13.0-4
- Rebuilt for Python 3.10

* Tue Feb 16 2021 Lumír Balhar <lbalhar@redhat.com> - 2.13.0-3
- Fixed tests for Python 3.10
Resolves: rhbz#1906368

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 08 2020 Lumír Balhar <lbalhar@redhat.com> - 2.13.0-1
- Update to 2.13.0 (#1767192)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.8.1-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.8.1-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.8.1-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 10 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.8.1-1
- Update to 2.8.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.8.0-1
- Update to 2.8.0

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.7.8-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 27 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.7.8-1
- Update to 2.7.8

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 08 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.7.7-1
- Update to 2.7.7

* Thu Feb 09 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.7.5-1
- Update to 2.7.5

* Sat Jan 28 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.7.4-1
- Initial package
