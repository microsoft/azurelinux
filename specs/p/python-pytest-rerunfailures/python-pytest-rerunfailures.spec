# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname pytest-rerunfailures

# Needed for Python bootstrap
%bcond_without tests

Name:           python-%{srcname}
Version:        15.0
Release: 7%{?dist}
Summary:        A py.test plugin that re-runs failed tests to eliminate flakey failures

License:        MPL-2.0
URL:            https://github.com/pytest-dev/pytest-rerunfailures
Source0:        https://github.com/pytest-dev/pytest-rerunfailures/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%global _description %{expand:
pytest-rerunfailures is a plugin for py.test that re-runs tests to eliminate
intermittent failures.}

%description %_description


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel

%description -n python%{python3_pkgversion}-%{srcname} %_description


%prep
%autosetup -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l pytest_rerunfailures


%if %{with tests}
%check
%pytest tests
%endif


%files -n python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%doc CHANGES.rst README.rst


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 15.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 15.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 15.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 22 2024 Scott K Logan <logans@cottsay.net> - 15.0-1
- Update to 15.0 (rhbz#2327591)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 17 2024 Scott K Logan <logans@cottsay.net> - 14.0-1
- Update to 14.0 (rhbz#2251442)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 12.0-5
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 12.0-4
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Scott K Logan <logans@cottsay.net> - 12.0-1
- Update to 12.0 (rhbz#2168740)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 11.0-4
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 11.0-3
- Bootstrap for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Scott K Logan <logans@cottsay.net> - 11.0-1
- Update to 11.0 (rhbz#2160820)

* Tue Nov 22 2022 Scott K Logan <logans@cottsay.net> - 10.3-1
- Update to 10.3 (rhbz#2144871)
- Define _description variable to reduce duplication
- Drop macro from URL to improve ergonomics
- Use modern packaging macros
- Switch to SPDX license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 10.2-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Scott K Logan <logans@cottsay.net> - 10.2-1
- Update to 10.2 (rhbz#1965106)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 9.1.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 30 2020 Scott K Logan <logans@cottsay.net> - 9.1.1-1
- Update to 9.1.1 (rhbz#1872994)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 29 2020 Scott K Logan <logans@cottsay.net> - 9.0-1
- Update to 9.0 (rhbz#1773599)

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 8.0-2
- Rebuilt for Python 3.9

* Wed Apr 15 2020 Scott K Logan <logans@cottsay.net> - 8.0-1
- Update to 8.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 7.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 7.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Scott K Logan <logans@cottsay.net> - 7.0-1
- Update to 7.0 (rhbz#1693860)

* Tue Feb 12 2019 Scott K Logan <logans@cottsay.net> - 6.0-1
- Initial package
