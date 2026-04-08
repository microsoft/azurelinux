# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname pytest-repeat

Name:           python-%{srcname}
Version:        0.9.3
Release:        9%{?dist}
Summary:        A pytest plugin for repeating test execution

License:        MPL-2.0
URL:            https://github.com/pytest-dev/pytest-repeat
Source0:        https://github.com/pytest-dev/pytest-repeat/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%global _description %{expand:
pytest-repeat is a plugin for py.test that makes it easy to repeat a single
test, or multiple tests, a specific number of times.
}

%description %_description


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel

%description -n python%{python3_pkgversion}-%{srcname} %_description


%prep
%autosetup -p1 -n %{srcname}-%{version}


%generate_buildrequires
SETUPTOOLS_SCM_PRETEND_VERSION=%{version}; export SETUPTOOLS_SCM_PRETEND_VERSION
%pyproject_buildrequires


%build
SETUPTOOLS_SCM_PRETEND_VERSION=%{version}; export SETUPTOOLS_SCM_PRETEND_VERSION
%pyproject_wheel


%install
SETUPTOOLS_SCM_PRETEND_VERSION=%{version}; export SETUPTOOLS_SCM_PRETEND_VERSION
%pyproject_install
%pyproject_save_files pytest_repeat


%check
%pytest test_repeat.py


%files -n python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc CHANGES.rst README.rst


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.9.3-9
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.9.3-8
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.9.3-6
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.9.3-3
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Scott K Logan <logans@cottsay.net> - 0.9.3-1
- Update to 0.9.3 (rhbz#2241970)
- Define _description variable to reduce duplication
- Drop macro from URL to improve ergonomics
- Use modern Python packaging macros
- Switch to SPDX license identifier

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.9.1-9
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.9.1-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 02 2020 Scott K Logan <logans@cottsay.net> - 0.9.1-1
- Update to 0.9.1 (rhbz#1893400)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.8.0-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.8.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.8.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 18 2019 Scott K Logan <logans@cottsay.net> - 0.8.0-1
- Update to 0.8.0
- Require pytest 3.6
- Drop python3_other subpackage

* Tue Feb 12 2019 Scott K Logan <logans@cottsay.net> - 0.7.0-1
- Initial package
