# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global         pypi_name langdetect

Name:           python-%{pypi_name}
Version:        1.0.9
Release:        15%{?dist}
Summary:        Language detection library ported from Google's language-detection

# Both python-langdetect and language-detection are under ASL 2.0
License:        Apache-2.0
URL:            https://pypi.org/project/langdetect/
Source0:        %{pypi_source}

BuildArch:      noarch

BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(six)

%generate_buildrequires
%pyproject_buildrequires

%global _description %{expand:
Port of Nakatani Shuyo's language-detection library (version from 03/03/2014) to
Python.

langdetect supports 55 languages out of the box (ISO 639-1 codes):
af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he, hi, hr,
hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl, pt, ro, ru, sk,
sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh-cn, zh-tw}

%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}


%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -n %{pypi_name}-%{version}

#rm -rf %{pypi_name}.egginfo

chmod 644 LICENSE NOTICE langdetect/profiles/*

%build
%pyproject_wheel

%install
%pyproject_install

%check
%pytest

%files -n python3-%{pypi_name}
%doc README.md
%license LICENSE NOTICE
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.9-15
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.9-14
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 14 2025 Sudip Shil <sshil@redhat.com> - 1.0.9-12
- Migrate to %pyproject_* macros and remove deprecated %py3_build/install

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.0.9-11
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.9-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.0.9-4
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Oct 16 2022 Sudip Shil <sshil@redhat.com> - 1.0.9-2
- License changed to Apache-2.0(SPDX format)
- Removed Requires: python3dist(six) because it's auto generated

* Tue Sep 27 2022 Sudip Shil <sshil@redhat.com> - 1.0.9-1
- Update to 1.0.9

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.8-2
- Rebuilt for Python 3.10

* Thu Mar 18 2021 Lyes Saadi <fedora@lyes.eu> - 1.0.8-1
- Initial Package
