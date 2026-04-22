# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without check
%global pypi_name identify

Name:           python-%{pypi_name}
Version:        2.6.16
Release: 3%{?dist}
Summary:        File identification library for Python

License:        MIT
URL:            https://github.com/chriskuehl/identify
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(ukkonen)
%if %{with check}
BuildRequires:  python3-pytest
%endif

%description
Given a file (or some information about a file), return a set of standardized
tags identifying what the file is.


%package -n     python3-%{pypi_name}
Summary:        %{summary}


%description -n python3-%{pypi_name}
%{summary}.


%prep
%autosetup -n %{pypi_name}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}


%if %{with check}
%check
%pyproject_check_import

%{python3} -m pytest -v
%endif


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%{_bindir}/%{pypi_name}-cli


%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 Gwyn Ciesla <gwync@protonmail.com> - 2.6.16-1
- 2.6.16

* Thu Oct 02 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.6.15-1
- 2.6.15

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.6.14-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Sep 08 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.6.14-1
- 2.6.14

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.6.13-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.6.13-1
- 2.6.13

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.6.12-2
- Rebuilt for Python 3.14

* Tue May 27 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.6.12-1
- 2.6.12

* Fri May 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.6.11-1
- 2.6.11

* Mon Apr 21 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.6.10-1
- 2.6.10

* Sat Mar 08 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.6.9-1
- 2.6.9

* Sat Feb 22 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.6.8-1
- 2.6.8

* Mon Feb 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.6.7-1
- 2.6.7

* Thu Jan 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.6.6-1
- 2.6.6

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jan 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.6.5-1
- 2.6.5

* Mon Dec 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 2.6.4-1
- 2.6.4

* Tue Nov 26 2024 Gwyn Ciesla <gwync@protonmail.com> - 2.6.3-1
- 2.6.3

* Sat Nov 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 2.6.2-1
- 2.6.2

* Mon Sep 16 2024 Gwyn Ciesla <gwync@protonmail.com> - 2.6.1-1
- 2.6.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 08 2024 Gwyn Ciesla <gwync@protonmail.com> - 2.6.0-1
- 2.6.0

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.5.36-2
- Rebuilt for Python 3.13

* Mon Apr 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 2.5.36-1
- 2.5.36

* Mon Feb 19 2024 Gwyn Ciesla <gwync@protonmail.com> - 2.5.35-1
- 2.5.35

* Mon Feb 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 2.5.34-1
- 2.5.34

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.33-1
- 2.5.33

* Mon Nov 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.32-1
- 2.5.32

* Mon Oct 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.31-1
- 2.5.31

* Sun Oct 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.30-1
- 2.5.30

* Sat Sep 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.29-1
- 2.5.29

* Tue Sep 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.28-1
- 2.5.28

* Wed Aug 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.27-1
- 2.5.27

* Mon Jul 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.26-1
- 2.5.26

* Wed Jul 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.25-1
- 2.5.25

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.5.24-2
- Rebuilt for Python 3.12

* Wed May 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.24-1
- 2.5.24

* Wed Apr 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.23-1
- 2.5.23

* Mon Mar 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.22-1
- 2.5.22

* Thu Mar 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.21-1
- 2.5.21

* Sat Mar 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.20-1
- 2.5.20

* Wed Mar 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.19-1
- 2.5.19

* Tue Mar 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.18-2
- migrated to SPDX license

* Mon Feb 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.18-1
- 2.5.18

* Mon Jan 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.17-1
- 2.5.17

* Mon Jan 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.16-1
- 2.5.16

* Mon Jan 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.15-1
- 2.5.15

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.13-1
- 2.5.13

* Wed Jan 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.12-1
- 2.5.12

* Mon Dec 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.11-1
- 2.5.11

* Thu Dec 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.10-1
- 2.5.10

* Fri Nov 18 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.9-1
- 2.5.9

* Thu Oct 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.8-1
- 2.5.8

* Wed Oct 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.7-1
- 2.5.7

* Mon Oct 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.6-1
- 2.5.6

* Wed Sep 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.5-1
- 2.5.5

* Thu Aug 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.3-1
- 2.5.3

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.2-1
- 2.5.2

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.5.1-2
- Rebuilt for Python 3.11

* Thu May 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.1-1
- 2.5.1

* Mon May 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.0-1
- 2.5.0

* Wed Mar 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.4.12-1
- 2.4.12

* Wed Feb 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.4.11-1
- 2.4.11

* Mon Feb 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.4.10-1
- 2.4.10

* Wed Feb 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.4.9-1
- 2.4.9

* Thu Feb 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.4.8-1
- 2.4.8

* Tue Feb 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.4.7-1
- 2.4.7

* Thu Jan 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.4.6-1
- 2.4.6

* Tue Jan 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.4.5-1
- 2.4.5

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.4.4-1
- 2.4.4

* Tue Jan 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.4.3-1
- 2.4.3

* Thu Jan 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.4.2-1
- 2.4.2

* Tue Dec 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.4.1-1
- 2.4.1

* Fri Nov 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.4.0-1
- 2.4.0

* Thu Nov 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.3.7-1
- 2.3.7

* Tue Nov 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.3.6-1
- 2.3.6

* Tue Nov 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.3.5-1
- 2.3.5

* Mon Nov 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.3.4-1
- 2.3.4

* Tue Nov 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.3.3-1
- 2.3.3

* Sun Oct 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.3.1-1
- 2.3.1

* Mon Oct 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.3.0-1
- 2.3.0

* Mon Sep 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.15-1
- 2.2.15

* Thu Sep 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.14-1
- 2.2.14

* Fri Aug 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.13-1
- 2.2.13

* Wed Aug 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.12-1
- 2.2.12

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.11-1
- 2.2.11

* Tue Jun 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.9-1
- 2.2.9

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.2.8-2
- Rebuilt for Python 3.10

* Thu Jun 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.8-1
- 2.2.8

* Tue Jun 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.7-1
- 2.2.7

* Tue May 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.6-1
- 2.2.6

* Mon May 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.5-1
- 2.2.5

* Wed Apr 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.4-1
- 2.2.4

* Fri Apr 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.3-1
- 2.2.3

* Mon Mar 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.2.2-1
- 2.2.1

* Fri Mar 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.1.4-1
- 2.1.4

* Mon Mar 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.1.3-1
- 2.1.3

* Fri Mar 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.1.2-1
- 2.1.2

* Tue Mar 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.1.1-1
- 2.1.1

* Wed Mar 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.1.0-1
- 2.1.0

* Mon Mar 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.0.0-1
- 2.0.0

* Sat Feb 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.5.14-1
- 1.5.14

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.5.13-1
- 1.5.13

* Mon Jan 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.5.12-1
- 1.5.12

* Thu Dec 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.5.11-1
- 1.5.11

* Mon Nov 23 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.10-1
- build(update): 1.5.10

* Tue Nov 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.5.9-1
- 1.5.9

* Tue Nov 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.5.8-1
- 1.5.8

* Mon Nov 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.5.7-1
- 1.5.7

* Sat Oct 10 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.6-1
- build(update): 1.5.6

* Thu Sep 24 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.5-1
- Update to 1.5.5

* Sun Sep 13 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.2-1
- Update to 1.5.2

* Sun Sep  6 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.0-1
- Update to 1.5.0

* Thu Aug 27 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.29-1
- Update to 1.4.29

* Fri Aug 14 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.26-1
- Update to 1.4.26

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.24-1
- Update to 1.4.24

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.16-2
- Rebuilt for Python 3.9

* Thu May 21 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.16-1
- Update to 1.4.16

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.10-1
- Update to 1.4.10

* Thu Oct 24 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.7-5
- Initial package
