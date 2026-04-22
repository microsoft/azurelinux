# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name botocore
%bcond_without tests

Name:           python-%{pypi_name}
# NOTICE - Updating this package requires updating python-boto3
Version:        1.42.52
Release: 2%{?dist}
Summary:        Low-level, data-driven core of boto 3

License:        Apache-2.0
URL:            https://github.com/boto/botocore
Source0:        %{pypi_source}

BuildArch:      noarch

%global _description %{expand:
A low-level interface to a growing number of Amazon Web Services. The
botocore package is the foundation for the AWS CLI as well as boto3.}

%description %{_description}

%package -n     python3-%{pypi_name}
Summary:        Low-level, data-driven core of boto 3
BuildRequires:  python3-devel
%if %{with tests}
# For tests:
BuildRequires:  python3-jsonschema
BuildRequires:  python3-pytest
%if %{undefined rhel}
BuildRequires:  python3-pytest-xdist
%endif
%endif
Provides:       bundled(python3-six) = 1.16.0
Provides:       bundled(python3-requests) = 2.7.0

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -n %{pypi_name}-%{version} -p1
# Remove online tests
rm -vr tests/integration
# This test tried to import tests/cmd-runner which failed as the code was
# unable to import "botocore". I'm not 100% sure why this happened but for now
# just exclude this one test and run all the other functional tests.
rm -vr tests/functional/leak

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%if %{with tests}
# test_lru_cache_weakref fails with Python 3.14 - temporarily skip
# Reported: https://github.com/boto/botocore/issues/3482
%pytest %{!?rhel:-n auto} -k "not test_lru_cache_weakref"
%else
%pyproject_check_import -e botocore.crt.auth -e botocore.vendored*
%endif

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst
%license LICENSE.txt

%changelog
* Thu Feb 19 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.52-1
- 1.42.52

* Tue Feb 17 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.51-1
- 1.42.51

* Tue Feb 17 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.50-1
- 1.42.50

* Mon Feb 16 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.49-1
- 1.42.49

* Fri Feb 13 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.48-1
- 1.42.48

* Thu Feb 12 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.47-1
- 1.42.47

* Tue Feb 10 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.46-1
- 1.42.46

* Tue Feb 10 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.45-1
- 1.42.45

* Fri Feb 06 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.44-1
- 1.42.44

* Fri Feb 06 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.43-1
- 1.42.43

* Wed Feb 04 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.42-1
- 1.42.42

* Wed Feb 04 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.41-1
- 1.42.41

* Mon Feb 02 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.40-1
- 1.42.40

* Sat Jan 31 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.39-1
- 1.42.39

* Thu Jan 29 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.38-1
- 1.42.38

* Wed Jan 28 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.37-1
- 1.42.37

* Mon Jan 26 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.35-1
- 1.42.35

* Fri Jan 23 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.34-1
- 1.42.34

* Fri Jan 23 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.33-1
- 1.42.33

* Wed Jan 21 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.32-1
- 1.42.32

* Wed Jan 21 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.31-1
- 1.42.31

* Tue Jan 20 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.30-1
- 1.42.30

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.42.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jan 15 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.29-1
- 1.42.29

* Thu Jan 15 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.28-1
- 1.42.28

* Tue Jan 13 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.27-1
- 1.42.27

* Tue Jan 13 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.26-1
- 1.42.26

* Fri Jan 09 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.25-1
- 1.42.25

* Wed Jan 07 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.24-1
- 1.42.24

* Tue Jan 06 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.23-1
- 1.42.23

* Mon Jan 05 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.22-1
- 1.42.22

* Mon Jan 05 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.21-1
- 1.42.21

* Fri Jan 02 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.20-1
- 1.42.20

* Fri Jan 02 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.42.19-1
- 1.42.19

* Mon Dec 22 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.15-1
- 1.42.15

* Thu Dec 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.13-1
- 1.42.13

* Wed Dec 17 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.12-1
- 1.42.12

* Tue Dec 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.11-1
- 1.42.11

* Tue Dec 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.10-1
- 1.42.10

* Fri Dec 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.9-1
- 1.42.9

* Thu Dec 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.8-1
- 1.42.8

* Wed Dec 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.7-1
- 1.42.7

* Wed Dec 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.6-1
- 1.42.6

* Mon Dec 08 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.5-1
- 1.42.5

* Fri Dec 05 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.4-1
- 1.42.4

* Thu Dec 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.3-1
- 1.42.3

* Wed Dec 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.2-1
- 1.42.2

* Tue Dec 02 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.1-1
- 1.42.1

* Mon Dec 01 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.41.6-1
- 1.41.6

* Tue Nov 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.41.4-1
- 1.41.4

* Mon Nov 24 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.41.3-1
- 1.41.3

* Fri Nov 21 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.41.2-1
- 1.41.2

* Thu Nov 20 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.41.1-1
- 1.41.1

* Wed Nov 19 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.41.0-1
- 1.41.0

* Tue Nov 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.76-1
- 1.40.76

* Mon Nov 17 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.75-1
- 1.40.75

* Fri Nov 14 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.74-1
- 1.40.74

* Thu Nov 13 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.73-1
- 1.40.73

* Wed Nov 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.72-1
- 1.40.72

* Tue Nov 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.71-1
- 1.40.71

* Mon Nov 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.70-1
- 1.40.70

* Fri Nov 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.69-1
- 1.40.69

* Thu Nov 06 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.68-1
- 1.40.68

* Wed Nov 05 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.67-1
- 1.40.67

* Tue Nov 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.66-1
- 1.40.66

* Mon Nov 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.65-1
- 1.40.65

* Mon Nov 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.64-1
- 1.40.64

* Thu Oct 30 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.63-1
- 1.40.63

* Thu Oct 30 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.62-1
- 1.40.62

* Wed Oct 29 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.61-1
- 1.40.61

* Mon Oct 27 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.60-1
- 1.40.60

* Fri Oct 24 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.59-1
- 1.40.59

* Thu Oct 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.58-1
- 1.40.58

* Wed Oct 22 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.57-1
- 1.40.57

* Wed Oct 22 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.56-1
- 1.40.56

* Fri Oct 17 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.55-1
- 1.40.55

* Thu Oct 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.54-1
- 1.40.54

* Wed Oct 15 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.53-1
- 1.40.53

* Wed Oct 15 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.52-1
- 1.40.52

* Mon Oct 13 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.51-1
- 1.40.51

* Fri Oct 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.50-1
- 1.40.50

* Thu Oct 09 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.49-1
- 1.40.49

* Wed Oct 08 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.48-1
- 1.40.48

* Tue Oct 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.47-1
- 1.40.47

* Mon Oct 06 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.46-1
- 1.40.46

* Fri Oct 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.45-1
- 1.40.45

* Thu Oct 02 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.44-1
- 1.40.44

* Wed Oct 01 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.43-1
- 1.40.43

* Tue Sep 30 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.42-1
- 1.40.42

* Mon Sep 29 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.41-1
- 1.40.41

* Fri Sep 26 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.40-1
- 1.40.40

* Fri Sep 26 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.39-1
- 1.40.39

* Wed Sep 24 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.38-1
- 1.40.38

* Tue Sep 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.37-1
- 1.40.37

* Mon Sep 22 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.36-1
- 1.40.36

* Fri Sep 19 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.35-1
- 1.40.35

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.40.34-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Thu Sep 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.34-1
- 1.40.34

* Fri Sep 19 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.33-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Thu Sep 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.33-1
- 1.40.33

* Wed Sep 17 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.32-1
- 1.40.32

* Mon Sep 15 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.31-1
- 1.40.31

* Mon Sep 15 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.30-1
- 1.40.30

* Thu Sep 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.29-1
- 1.40.29

* Wed Sep 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.28-1
- 1.40.28

* Tue Sep 09 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.26-1
- 1.40.26

* Fri Sep 05 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.25-1
- 1.40.25

* Thu Sep 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.24-1
- 1.40.24

* Wed Sep 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.23-1
- 1.40.23

* Tue Sep 02 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.22-1
- 1.40.22

* Fri Aug 29 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.21-1
- 1.40.21

* Fri Aug 29 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.20-1
- 1.40.20

* Wed Aug 27 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.19-1
- 1.40.19

* Tue Aug 26 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.18-1
- 1.40.18

* Mon Aug 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.17-1
- 1.40.17

* Fri Aug 22 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.16-1
- 1.40.16

* Thu Aug 21 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.15-1
- 1.40.15

* Wed Aug 20 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.14-1
- 1.40.14

* Wed Aug 20 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.13-1
- 1.40.13

* Mon Aug 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.12-1
- 1.40.12

* Fri Aug 15 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.11-1
- 1.40.11

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.40.10-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Aug 14 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.10-1
- 1.40.10

* Wed Aug 13 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.9-1
- 1.40.9

* Tue Aug 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.8-1
- 1.40.8

* Mon Aug 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.7-1
- 1.40.7

* Fri Aug 08 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.6-1
- 1.40.6

* Thu Aug 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.5-1
- 1.40.5

* Wed Aug 06 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.4-1
- 1.40.4

* Tue Aug 05 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.3-1
- 1.40.3

* Mon Aug 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.2-1
- 1.40.2

* Fri Aug 01 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.1-1
- 1.40.1

* Thu Jul 31 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.40.0-1
- 1.40.0

* Wed Jul 30 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.17-1
- 1.39.17

* Wed Jul 30 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.16-1
- 1.39.16

* Mon Jul 28 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.15-1
- 1.39.15

* Fri Jul 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.14-1
- 1.39.14

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.39.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 24 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.13-1
- 1.39.13

* Wed Jul 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.12-1
- 1.39.12

* Tue Jul 22 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.11-1
- 1.39.11

* Mon Jul 21 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.10-1
- 1.39.10

* Fri Jul 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.9-1
- 1.39.9

* Thu Jul 17 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.8-1
- 1.39.8

* Wed Jul 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.7-1
- 1.39.7

* Wed Jul 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.6-1
- 1.39.6

* Wed Jul 09 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.4-1
- 1.39.4

* Thu Jul 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.3-1
- 1.39.3

* Thu Jul 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.39.2-1
- 1.39.2

* Fri Jun 27 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.46-1
- 1.38.46

* Thu Jun 26 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.45-1
- 1.38.45

* Wed Jun 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.44-1
- 1.38.44

* Tue Jun 24 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.43-1
- 1.38.43

* Mon Jun 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.42-1
- 1.38.42

* Fri Jun 13 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.36-1
- 1.38.36

* Thu Jun 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.35-1
- 1.38.35

* Wed Jun 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.34-1
- 1.38.34

* Tue Jun 10 2025 Python Maint <python-maint@redhat.com> - 1.38.33-2
- Rebuilt for Python 3.14

* Mon Jun 09 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.33-1
- 1.38.33

* Sat Jun 07 2025 Python Maint <python-maint@redhat.com> - 1.38.32-2
- Rebuilt for Python 3.14

* Fri Jun 06 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.32-1
- 1.38.32

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 1.38.31-2
- Rebuilt for Python 3.14

* Thu Jun 05 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.31-1
- 1.38.31

* Wed Jun 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.30-1
- 1.38.30

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 1.38.29-2
- Rebuilt for Python 3.14

* Tue Jun 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.29-1
- 1.38.29

* Mon Jun 02 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.28-1
- 1.38.28

* Fri May 30 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.27-1
- 1.38.27

* Thu May 29 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.26-1
- 1.38.26

* Wed May 28 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.25-1
- 1.38.25

* Wed May 28 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.24-1
- 1.38.24

* Fri May 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.23-1
- 1.38.23

* Thu May 22 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.22-1
- 1.38.22

* Wed May 21 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.21-1
- 1.38.21

* Wed May 21 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.20-1
- 1.38.20

* Mon May 19 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.19-1
- 1.38.19

* Fri May 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.18-1
- 1.38.18

* Thu May 15 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.17-1
- 1.38.17

* Thu May 15 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.16-1
- 1.38.16

* Tue May 13 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.15-1
- 1.38.15

* Mon May 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.14-1
- 1.38.14

* Fri May 09 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.13-1
- 1.38.13

* Fri May 09 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.12-1
- 1.38.12

* Wed May 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.11-1
- 1.38.11

* Tue May 06 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.10-1
- 1.38.10

* Mon May 05 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.9-1
- 1.38.9

* Mon May 05 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.8-1
- 1.38.8

* Thu May 01 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.7-1
- 1.38.7

* Wed Apr 30 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.6-1
- 1.38.6

* Tue Apr 29 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.5-1
- 1.38.5

* Mon Apr 28 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.4-1
- 1.38.4

* Fri Apr 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.3-1
- 1.38.3

* Thu Apr 24 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.2-1
- 1.38.2

* Wed Apr 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.1-1
- 1.38.1

* Wed Apr 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.0-1
- 1.38.0

* Mon Apr 21 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.38-1
- 1.37.38

* Fri Apr 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.37-1
- 1.37.37

* Thu Apr 17 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.36-1
- 1.37.36

* Wed Apr 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.35-1
- 1.37.35

* Mon Apr 14 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.34-1
- 1.37.34

* Fri Apr 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.33-1
- 1.37.33

* Fri Apr 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.32-1
- 1.37.32

* Thu Apr 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.31-1
- 1.37.31

* Wed Apr 09 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.30-1
- 1.37.30

* Mon Apr 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.29-1
- 1.37.29

* Fri Apr 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.28-1
- 1.37.28

* Thu Apr 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.27-1
- 1.37.27

* Thu Apr 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.26-1
- 1.37.26

* Wed Apr 02 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.25-1
- 1.37.25

* Mon Mar 31 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.23-1
- 1.37.23

* Thu Mar 27 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.22-1
- 1.37.22

* Thu Mar 27 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.21-1
- 1.37.21

* Tue Mar 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.20-1
- 1.37.20

* Mon Mar 24 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.19-1
- 1.37.19

* Mon Mar 24 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.18-1
- 1.37.18

* Thu Mar 20 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.17-1
- 1.37.17

* Thu Mar 20 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.16-1
- 1.37.16

* Tue Mar 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.15-1
- 1.37.15

* Mon Mar 17 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.14-1
- 1.37.14

* Fri Mar 14 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.13-1
- 1.37.13

* Thu Mar 13 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.12-1
- 1.37.12

* Tue Mar 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.11-1
- 1.37.11

* Mon Mar 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.10-1
- 1.37.10

* Sat Mar 08 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.9-1
- 1.37.9

* Thu Mar 06 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.8-1
- 1.37.8

* Wed Mar 05 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.7-1
- 1.37.7

* Tue Mar 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.6-1
- 1.37.6

* Mon Mar 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.5-1
- 1.37.5

* Fri Feb 28 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.4-1
- 1.37.4

* Thu Feb 27 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.3-1
- 1.37.3

* Wed Feb 26 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.2-1
- 1.37.2

* Tue Feb 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.1-1
- 1.37.1

* Tue Feb 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.37.0-1
- 1.37.0

* Fri Feb 21 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.26-1
- 1.36.26

* Thu Feb 20 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.25-1
- 1.36.25

* Wed Feb 19 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.24-1
- 1.36.24

* Tue Feb 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.23-1
- 1.36.23

* Mon Feb 17 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.22-1
- 1.36.22

* Fri Feb 14 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.21-1
- 1.36.21

* Thu Feb 13 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.20-1
- 1.36.20

* Wed Feb 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.19-1
- 1.36.19

* Tue Feb 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.18-1
- 1.36.18

* Mon Feb 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.17-1
- 1.36.17

* Fri Feb 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.16-1
- 1.36.16

* Thu Feb 06 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.15-1
- 1.36.15

* Wed Feb 05 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.14-1
- 1.36.14

* Tue Feb 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.13-1
- 1.36.13

* Mon Feb 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.12-1
- 1.36.12

* Fri Jan 31 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.11-1
- 1.36.11

* Fri Jan 31 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.10-1
- 1.36.10

* Thu Jan 30 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.9-1
- 1.36.9

* Wed Jan 29 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.8-1
- 1.36.8

* Mon Jan 27 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.7-1
- 1.36.7

* Fri Jan 24 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.6-1
- 1.36.6

* Thu Jan 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.5-1
- 1.36.5

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.2-1
- 1.36.2

* Thu Jan 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.1-1
- 1.36.1

* Thu Jan 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.36.0-1
- 1.36.0

* Tue Jan 14 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.35.99-1
- 1.35.99

* Mon Jan 13 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.35.98-1
- 1.35.98

* Fri Jan 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.35.97-1
- 1.35.97

* Fri Jan 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.35.96-1
- 1.35.96

* Wed Jan 08 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.35.95-1
- 1.35.95

* Tue Jan 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.35.94-1
- 1.35.94

* Mon Jan 06 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.35.93-1
- 1.35.93

* Sat Jan 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.35.92-1
- 1.35.92

* Thu Jan 02 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.35.91-1
- 1.35.91

* Mon Dec 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.90-1
- 1.35.90

* Fri Dec 20 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.86-1
- 1.35.86

* Thu Dec 19 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.85-1
- 1.35.85

* Wed Dec 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.84-1
- 1.35.84

* Tue Dec 17 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.83-1
- 1.35.83

* Mon Dec 16 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.82-1
- 1.35.82

* Mon Dec 16 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.81-1
- 1.35.81

* Thu Dec 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.80-1
- 1.35.80

* Wed Dec 11 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.79-1
- 1.35.79

* Tue Dec 10 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.78-1
- 1.35.78

* Mon Dec 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.77-1
- 1.35.77

* Fri Dec 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.76-1
- 1.35.76

* Wed Dec 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.75-1
- 1.35.75

* Tue Dec 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.74-1
- 1.35.74

* Tue Dec 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.73-1
- 1.35.73

* Mon Dec 02 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.72-1
- 1.35.72

* Mon Nov 25 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.69-1
- 1.35.69

* Fri Nov 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.68-1
- 1.35.68

* Fri Nov 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.67-1
- 1.35.67

* Wed Nov 20 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.66-1
- 1.35.66

* Tue Nov 19 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.65-1
- 1.35.65

* Mon Nov 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.64-1
- 1.35.64

* Fri Nov 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.63-1
- 1.35.63

* Fri Nov 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.62-1
- 1.35.62

* Thu Nov 14 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.61-1
- 1.35.61

* Wed Nov 13 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.60-1
- 1.35.60

* Tue Nov 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.59-1
- 1.35.59

* Tue Nov 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.58-1
- 1.35.58

* Fri Nov 08 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.57-1
- 1.35.57

* Thu Nov 07 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.56-1
- 1.35.56

* Wed Nov 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.55-1
- 1.35.55

* Fri Nov 01 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.54-1
- 1.35.54

* Thu Oct 31 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.53-1
- 1.35.53

* Wed Oct 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.52-1
- 1.35.52

* Wed Oct 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.51-1
- 1.35.51

* Mon Oct 28 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.50-1
- 1.35.50

* Fri Oct 25 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.49-1
- 1.35.49

* Thu Oct 24 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.48-1
- 1.35.48

* Wed Oct 23 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.47-1
- 1.35.47

* Wed Oct 23 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.46-1
- 1.35.46

* Mon Oct 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.45-1
- 1.35.45

* Mon Oct 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.44-1
- 1.35.44

* Thu Oct 17 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.43-1
- 1.35.43

* Thu Oct 17 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.42-1
- 1.35.42

* Tue Oct 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.41-1
- 1.35.41

* Mon Oct 14 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.40-1
- 1.35.40

* Fri Oct 11 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.39-1
- 1.35.39

* Thu Oct 10 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.38-1
- 1.35.38

* Wed Oct 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.37-1
- 1.35.37

* Tue Oct 08 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.36-1
- 1.35.36

* Mon Oct 07 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.35-1
- 1.35.35

* Fri Oct 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.34-1
- 1.35.34

* Thu Oct 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.33-1
- 1.35.33

* Thu Oct 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.32-1
- 1.35.32

* Tue Oct 01 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.30-1
- 1.35.30

* Mon Sep 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.29-1
- 1.35.29

* Thu Sep 26 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.28-1
- 1.35.28

* Wed Sep 25 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.27-1
- 1.35.27

* Tue Sep 24 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.26-1
- 1.35.26

* Tue Sep 24 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.25-1
- 1.35.25

* Fri Sep 20 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.24-1
- 1.35.24

* Thu Sep 19 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.23-1
- 1.35.23

* Thu Sep 19 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.22-1
- 1.35.22

* Wed Sep 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.21-1
- 1.35.21

* Mon Sep 16 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.20-1
- 1.35.20

* Fri Sep 13 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.19-1
- 1.35.19

* Thu Sep 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.18-1
- 1.35.18

* Wed Sep 11 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.17-1
- 1.35.17

* Tue Sep 10 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.16-1
- 1.35.16

* Tue Sep 10 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.15-1
- 1.35.15

* Fri Sep 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.14-1
- 1.35.14

* Fri Sep 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.13-1
- 1.35.13

* Wed Sep 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.12-1
- 1.35.12

* Tue Sep 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.11-1
- 1.35.11

* Tue Sep 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.10-1
- 1.35.10

* Tue Aug 27 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.7-1
- 1.35.7

* Mon Aug 26 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.6-1
- 1.35.6

* Fri Aug 23 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.5-1
- 1.35.5

* Thu Aug 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.4-1
- 1.35.4

* Wed Aug 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.3-1
- 1.35.3

* Wed Aug 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.2-1
- 1.35.2

* Tue Aug 20 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.1-1
- 1.35.1

* Fri Aug 16 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.35.0-1
- 1.35.0

* Thu Aug 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.162-1
- 1.34.162

* Wed Aug 14 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.161-1
- 1.34.161

* Wed Aug 14 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.160-1
- 1.34.160

* Mon Aug 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.159-1
- 1.34.159

* Mon Aug 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.158-1
- 1.34.158

* Thu Aug 08 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.157-1
- 1.34.157

* Wed Aug 07 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.156-1
- 1.34.156

* Tue Aug 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.155-1
- 1.34.155

* Mon Aug 05 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.154-1
- 1.34.154

* Mon Aug 05 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.153-1
- 1.34.153

* Fri Aug 02 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.152-1
- 1.34.152

* Tue Jul 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.151-1
- 1.34.151

* Mon Jul 29 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.150-1
- 1.34.150

* Fri Jul 26 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.149-1
- 1.34.149

* Wed Jul 24 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.148-1
- 1.34.148

* Tue Jul 23 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.147-1
- 1.34.147

* Mon Jul 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.146-1
- 1.34.146

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.34.145-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.145-1
- 1.34.145

* Mon Jul 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.144-1
- 1.34.144

* Tue Jul 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.142-1
- 1.34.142

* Tue Jul 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.141-1
- 1.34.141

* Mon Jul 08 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.140-1
- 1.34.140

* Wed Jul 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.139-1
- 1.34.139

* Wed Jul 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.138-1
- 1.34.138

* Fri Jun 28 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.135-1
- 1.34.135

* Tue Jun 25 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.133-1
- 1.34.133

* Tue Jun 25 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.132-1
- 1.34.132

* Fri Jun 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.131-1
- 1.34.131

* Tue Jun 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.129-1
- 1.34.129

* Tue Jun 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.128-1
- 1.34.128

* Fri Jun 14 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.127-1
- 1.34.127

* Thu Jun 13 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.126-1
- 1.34.126

* Wed Jun 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.125-1
- 1.34.125

* Wed Jun 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.124-1
- 1.34.124

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.34.121-2
- Rebuilt for Python 3.13

* Thu Jun 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.121-1
- 1.34.121

* Thu Jun 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.120-1
- 1.34.120

* Tue Jun 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.119-1
- 1.34.119

* Mon Jun 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.118-1
- 1.34.118

* Fri May 31 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.117-1
- 1.34.117

* Thu May 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.116-1
- 1.34.116

* Wed May 29 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.115-1
- 1.34.115

* Tue May 28 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.114-1
- 1.34.114

* Tue May 28 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.113-1
- 1.34.113

* Thu May 23 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.112-1
- 1.34.112

* Wed May 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.111-1
- 1.34.111

* Wed May 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.110-1
- 1.34.110

* Mon May 20 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.109-1
- 1.34.109

* Fri May 17 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.108-1
- 1.34.108

* Thu May 16 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.107-1
- 1.34.107

* Mon May 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.99-1
- 1.34.99

* Fri May 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.98-1
- 1.34.98

* Thu May 02 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.97-1
- 1.34.97

* Wed May 01 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.96-1
- 1.34.96

* Tue Apr 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.95-1
- 1.34.95

* Mon Apr 29 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.94-1
- 1.34.94

* Fri Apr 26 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.93-1
- 1.34.93

* Thu Apr 25 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.92-1
- 1.34.92

* Wed Apr 24 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.91-1
- 1.34.91

* Tue Apr 23 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.90-1
- 1.34.90

* Tue Apr 23 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.89-1
- 1.34.89

* Fri Apr 19 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.88-1
- 1.34.88

* Thu Apr 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.87-1
- 1.34.87

* Wed Apr 17 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.86-1
- 1.34.86

* Tue Apr 16 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.85-1
- 1.34.85

* Fri Apr 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.84-1
- 1.34.84

* Fri Apr 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.83-1
- 1.34.83

* Wed Apr 10 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.82-1
- 1.34.82

* Tue Apr 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.81-1
- 1.34.81

* Mon Apr 08 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.80-1
- 1.34.80

* Fri Apr 05 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.79-1
- 1.34.79

* Thu Apr 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.78-1
- 1.34.78

* Wed Apr 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.77-1
- 1.34.77

* Tue Apr 02 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.76-1
- 1.34.76

* Mon Apr 01 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.75-1
- 1.34.75

* Fri Mar 29 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.74-1
- 1.34.74

* Thu Mar 28 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.73-1
- 1.34.73

* Wed Mar 27 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.72-1
- 1.34.72

* Tue Mar 26 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.71-1
- 1.34.71

* Mon Mar 25 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.70-1
- 1.34.70

* Fri Mar 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.69-1
- 1.34.69

* Fri Mar 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.68-1
- 1.34.68

* Wed Mar 20 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.67-1
- 1.34.67

* Tue Mar 19 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.66-1
- 1.34.66

* Mon Mar 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.65-1
- 1.34.65

* Mon Mar 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.64-1
- 1.34.64

* Wed Mar 13 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.62-1
- 1.34.62

* Tue Mar 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.61-1
- 1.34.61

* Tue Mar 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.60-1
- 1.34.60

* Thu Mar 07 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.58-1
- 1.34.58

* Wed Mar 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.57-1
- 1.34.57

* Tue Mar 05 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.56-1
- 1.34.56

* Tue Mar 05 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.55-1
- 1.34.55

* Mon Mar 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.54-1
- 1.34.54

* Mon Mar 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.53-1
- 1.34.53

* Wed Feb 28 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.52-1
- 1.34.52

* Tue Feb 27 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.51-1
- 1.34.51

* Mon Feb 26 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.50-1
- 1.34.50

* Fri Feb 23 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.49-1
- 1.34.49

* Thu Feb 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.48-1
- 1.34.48

* Wed Feb 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.47-1
- 1.34.47

* Tue Feb 20 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.46-1
- 1.34.46

* Mon Feb 19 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.45-1
- 1.34.45

* Fri Feb 16 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.44-1
- 1.34.44

* Thu Feb 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.43-1
- 1.34.43

* Thu Feb 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.42-1
- 1.34.42

* Tue Feb 13 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.41-1
- 1.34.41

* Mon Feb 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.40-1
- 1.34.40

* Fri Feb 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.39-1
- 1.34.39

* Fri Feb 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.38-1
- 1.34.38

* Wed Feb 07 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.37-1
- 1.34.37

* Tue Feb 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.36-1
- 1.34.36

* Mon Feb 05 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.35-1
- 1.34.35

* Fri Feb 02 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.34-1
- 1.34.34

* Thu Feb 01 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.33-1
- 1.34.33

* Wed Jan 31 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.32-1
- 1.34.32

* Tue Jan 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.31-1
- 1.34.31

* Mon Jan 29 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.30-1
- 1.34.30

* Fri Jan 26 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.29-1
- 1.34.29

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.34.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 25 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.28-1
- 1.34.28

* Wed Jan 24 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.27-1
- 1.34.27

* Wed Jan 24 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.26-1
- 1.34.26

* Tue Jan 23 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.25-1
- 1.34.25

* Mon Jan 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.24-1
- 1.34.24

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.34.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.23-1
- 1.34.23

* Thu Jan 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.22-1
- 1.34.22

* Wed Jan 17 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.21-1
- 1.34.21

* Tue Jan 16 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.20-1
- 1.34.20

* Tue Jan 16 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.19-1
- 1.34.19

* Thu Jan 11 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.17-1
- 1.34.17

* Wed Jan 10 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.16-1
- 1.34.16

* Tue Jan 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.15-1
- 1.34.15

* Fri Jan 05 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.14-1
- 1.34.14

* Fri Jan 05 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.13-1
- 1.34.13

* Wed Jan 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.12-1
- 1.34.12

* Tue Jan 02 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.34.11-1
- 1.34.11

* Wed Dec 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.34.9-1
- 1.34.9

* Tue Dec 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.34.8-1
- 1.34.8

* Fri Dec 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.34.7-1
- 1.34.7

* Thu Dec 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.34.6-1
- 1.34.6

* Wed Dec 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.34.5-1
- 1.34.5

* Tue Dec 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.34.4-1
- 1.34.4

* Tue Dec 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.34.3-1
- 1.34.3

* Fri Dec 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.34.2-1
- 1.34.2

* Thu Dec 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.34.1-1
- 1.34.1

* Thu Dec 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.34.0-1
- 1.34.0

* Tue Dec 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.13-1
- 1.33.13

* Tue Dec 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.12-1
- 1.33.12

* Fri Dec 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.11-1
- 1.33.11

* Thu Dec 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.10-1
- 1.33.10

* Wed Dec 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.9-1
- 1.33.9

* Tue Dec 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.8-1
- 1.33.8

* Mon Dec 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.7-1
- 1.33.7

* Fri Dec 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.6-1
- 1.33.6

* Thu Nov 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.5-1
- 1.33.5

* Thu Nov 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.4-1
- 1.33.4

* Wed Nov 29 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.2-1
- 1.33.2

* Tue Nov 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.1-1
- 1.33.1

* Mon Nov 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.33.0-1
- 1.33.0

* Mon Nov 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.32.7-1
- 1.32.7

* Tue Nov 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.32.5-1
- 1.32.5

* Tue Nov 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.32.4-1
- 1.32.4

* Mon Nov 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.32.3-1
- 1.32.3

* Thu Nov 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.32.2-1
- 1.32.2

* Wed Nov 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.32.1-1
- 1.32.1

* Tue Nov 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.32.0-1
- 1.32.0

* Mon Nov 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.85-1
- 1.31.85

* Mon Nov 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.84-1
- 1.31.84

* Thu Nov 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.83-1
- 1.31.83

* Thu Nov 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.82-1
- 1.31.82

* Wed Nov 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.81-1
- 1.31.81

* Wed Nov 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.80-1
- 1.31.80

* Mon Nov 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.79-1
- 1.31.79

* Fri Nov 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.78-1
- 1.31.78

* Thu Nov 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.77-1
- 1.31.77

* Wed Nov 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.76-1
- 1.31.76

* Wed Nov 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.75-1
- 1.31.75

* Mon Oct 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.74-1
- 1.31.74

* Fri Oct 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.73-1
- 1.31.73

* Thu Oct 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.72-1
- 1.31.72

* Thu Oct 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.71-1
- 1.31.71

* Tue Oct 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.70-1
- 1.31.70

* Mon Oct 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.69-1
- 1.31.69

* Mon Oct 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.68-1
- 1.31.68

* Thu Oct 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.67-1
- 1.31.67

* Wed Oct 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.66-1
- 1.31.66

* Tue Oct 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.65-1
- 1.31.65

* Mon Oct 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.64-1
- 1.31.64

* Thu Oct 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.63-1
- 1.31.63

* Fri Oct 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.62-1
- 1.31.62

* Thu Oct 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.61-1
- 1.31.61

* Wed Oct 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.60-1
- 1.31.60

* Tue Oct 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.59-1
- 1.31.59

* Tue Oct 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.58-1
- 1.31.58

* Thu Sep 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.57-1
- 1.31.57

* Thu Sep 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.56-1
- 1.31.56

* Tue Sep 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.55-1
- 1.31.55

* Mon Sep 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.54-1
- 1.31.54

* Fri Sep 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.53-1
- 1.31.53

* Wed Sep 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.52-1
- 1.31.52

* Tue Sep 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.51-1
- 1.31.51

* Tue Sep 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.50-1
- 1.31.50

* Fri Sep 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.49-1
- 1.31.49

* Thu Sep 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.48-1
- 1.31.48

* Wed Sep 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.47-1
- 1.31.47

* Tue Sep 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.46-1
- 1.31.46

* Mon Sep 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.45-1
- 1.31.45

* Fri Sep 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.44-1
- 1.31.44

* Thu Sep 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.43-1
- 1.31.43

* Wed Sep 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.42-1
- 1.31.42

* Tue Sep 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.41-1
- 1.31.41

* Tue Sep 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.40-1
- 1.31.40

* Fri Sep 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.39-1
- 1.31.39

* Wed Aug 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.38-1
- 1.31.38

* Wed Aug 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.37-1
- 1.31.37

* Mon Aug 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.36-1
- 1.31.36

* Fri Aug 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.35-1
- 1.31.35

* Thu Aug 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.34-1
- 1.31.34

* Wed Aug 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.33-1
- 1.31.33

* Wed Aug 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.32-1
- 1.31.32

* Fri Aug 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.30-1
- 1.31.30

* Thu Aug 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.29-1
- 1.31.29

* Wed Aug 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.28-1
- 1.31.28

* Wed Aug 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.27-2
- Don't use xdist on RHEL.

* Wed Aug 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.27-1
- 1.31.27

* Mon Aug 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.26-1
- 1.31.26

* Fri Aug 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.25-1
- 1.31.25

* Thu Aug 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.24-1
- 1.31.24

* Wed Aug 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.23-1
- 1.31.23

* Tue Aug 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.22-1
- 1.31.22

* Mon Aug 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.21-1
- 1.31.21

* Fri Aug 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.20-1
- 1.31.20

* Thu Aug 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.19-1
- 1.31.19

* Wed Aug 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.18-1
- 1.31.18

* Tue Aug 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.17-1
- 1.31.17

* Mon Jul 31 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.16-1
- 1.31.16

* Fri Jul 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.15-1
- 1.31.15

* Fri Jul 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.14-1
- 1.31.14

* Thu Jul 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.13-1
- 1.31.13

* Wed Jul 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.12-1
- 1.31.12

* Tue Jul 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.11-1
- 1.31.11

* Mon Jul 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.10-1
- 1.31.10

* Mon Jul 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.9-1
- 1.31.9

* Fri Jul 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.7-1
- 1.31.7

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.31.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.6-1
- 1.31.6

* Tue Jul 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.5-1
- 1.31.5

* Tue Jul 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.4-1
- 1.31.4

* Mon Jul 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.3-1
- 1.31.3

* Tue Jul 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.2-1
- 1.31.2

* Fri Jul 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.1-1
- 1.31.1

* Thu Jul 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.31.0-1
- 1.31.0

* Wed Jul 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.30.1-1
- 1.30.1

* Tue Jul 04 2023 Karolina Surma <ksurma@redhat.com> - 1.29.164-2
- Fix test failures with Python 3.12

* Fri Jun 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.164-1
- 1.29.164

* Wed Jun 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.163-1
- 1.29.163

* Tue Jun 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.162-1
- 1.29.162

* Mon Jun 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.161-1
- 1.29.161

* Mon Jun 26 2023 Python Maint <python-maint@redhat.com> - 1.29.160-2
- Rebuilt for Python 3.12

* Fri Jun 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.160-1
- 1.29.160

* Thu Jun 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.159-1
- 1.29.159

* Wed Jun 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.158-1
- 1.29.158

* Wed Jun 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.157-1
- 1.29.157

* Tue Jun 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.156-1
- 1.29.156

* Sat Jun 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.155-1
- 1.29.155

* Thu Jun 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.154-1
- 1.29.154

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.29.153-2
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.153-1
- 1.29.153

* Mon Jun 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.152-1
- 1.29.152

* Fri Jun 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.151-1
- 1.29.151

* Thu Jun 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.150-1
- 1.29.150

* Wed Jun 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.149-1
- 1.29.149

* Tue Jun 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.148-1
- 1.29.148

* Mon Jun 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.147-1
- 1.29.147

* Fri Jun 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.146-1
- 1.29.146

* Thu Jun 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.145-1
- 1.29.145

* Wed May 31 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.144-1
- 1.29.144

* Tue May 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.143-1
- 1.29.143

* Fri May 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.142-1
- 1.29.142

* Thu May 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.141-1
- 1.29.141

* Thu May 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.140-1
- 1.29.140

* Tue May 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.139-1
- 1.29.139

* Mon May 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.138-1
- 1.29.138

* Fri May 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.137-1
- 1.29.137

* Thu May 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.136-1
- 1.29.136

* Tue May 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.135-1
- 1.29.135

* Tue May 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.134-1
- 1.29.134

* Fri May 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.133-1
- 1.29.133

* Wed May 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.132-1
- 1.29.132

* Tue May 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.131-1
- 1.29.131

* Mon May 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.130-1
- 1.29.130

* Mon May 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.129-1
- 1.29.129

* Fri May 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.128-1
- 1.29.128

* Thu May 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.127-1
- 1.29.127

* Wed May 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.126-1
- 1.29.126

* Tue May 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.125-1
- 1.29.125

* Mon May 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.124-1
- 1.29.124

* Fri Apr 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.123-1
- 1.29.123

* Thu Apr 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.122-1
- 1.29.122

* Wed Apr 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.121-1
- 1.29.121

* Tue Apr 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.120-1
- 1.29.120

* Tue Apr 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.119-1
- 1.29.119

* Fri Apr 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.118-1
- 1.29.118

* Thu Apr 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.117-1
- 1.29.117

* Wed Apr 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.116-1
- 1.29.116

* Mon Apr 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.115-1
- 1.29.115

* Fri Apr 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.114-1
- 1.29.114

* Thu Apr 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.113-1
- 1.29.113

* Thu Apr 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.112-1
- 1.29.112

* Wed Apr 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.111-1
- 1.29.111

* Tue Apr 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.110-1
- 1.29.110

* Thu Apr 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.108-1
- 1.29.108

* Thu Apr 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.107-1
- 1.29.107

* Tue Apr 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.106-1
- 1.29.106

* Mon Apr 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.105-1
- 1.29.105

* Fri Mar 31 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.104-1
- 1.29.104

* Thu Mar 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.103-1
- 1.29.103

* Thu Mar 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.102-1
- 1.29.102

* Wed Mar 29 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.101-1
- 1.29.101

* Mon Mar 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.100-1
- 1.29.100

* Fri Mar 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.99-1
- 1.29.99

* Thu Mar 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.98-1
- 1.29.98

* Wed Mar 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.97-1
- 1.29.97

* Tue Mar 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.96-1
- 1.29.96

* Mon Mar 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.95-1
- 1.29.95

* Fri Mar 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.94-1
- 1.29.94

* Thu Mar 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.93-1
- 1.29.93

* Wed Mar 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.92-1
- 1.29.92

* Wed Mar 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.91-1
- 1.29.91

* Mon Mar 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.90-1
- 1.29.90

* Sun Mar 12 2023 Igor Raits <igor@gooddata.com> - 1.29.89-2
- Update bundled provides

* Fri Mar 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.89-1
- 1.29.89

* Thu Mar 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.88-1
- 1.29.88

* Wed Mar 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.87-1
- 1.29.87

* Tue Mar 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.86-1
- 1.29.86

* Tue Mar 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.85-1
- 1.29.85

* Fri Mar 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.84-1
- 1.29.84

* Thu Mar 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.83-1
- 1.29.83

* Thu Mar 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.82-2
- migrate to SPDX license

* Wed Mar 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.82-1
- 1.29.82

* Tue Feb 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.81-1
- 1.29.81

* Mon Feb 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.80-1
- 1.29.80

* Fri Feb 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.79-1
- 1.29.79

* Thu Feb 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.78-1
- 1.29.78

* Wed Feb 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.77-1
- 1.29.77

* Tue Feb 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.76-1
- 1.29.76

* Tue Feb 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.75-1
- 1.29.75

* Fri Feb 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.74-1
- 1.29.74

* Thu Feb 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.73-1
- 1.29.73

* Wed Feb 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.72-1
- 1.29.72

* Tue Feb 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.71-1
- 1.29.71

* Mon Feb 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.70-1
- 1.29.70

* Fri Feb 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.69-1
- 1.29.69

* Thu Feb 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.68-1
- 1.29.68

* Thu Feb 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.67-1
- 1.29.67

* Tue Feb 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.66-1
- 1.29.66

* Mon Feb 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.65-1
- 1.29.65

* Fri Feb 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.64-1
- 1.29.64

* Thu Feb 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.63-1
- 1.29.63

* Wed Feb 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.62-1
- 1.29.62

* Tue Jan 31 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.61-1
- 1.29.61

* Mon Jan 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.60-1
- 1.29.60

* Fri Jan 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.59-1
- 1.29.59

* Thu Jan 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.58-1
- 1.29.58

* Wed Jan 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.57-1
- 1.29.57

* Tue Jan 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.56-1
- 1.29.56

* Mon Jan 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.55-1
- 1.29.55

* Mon Jan 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.54-1
- 1.29.54

* Fri Jan 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.53-1
- 1.29.53

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.52-1
- 1.29.52

* Tue Jan 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.51-1
- 1.29.51

* Mon Jan 16 2023 Miro Hrončok <mhroncok@redhat.com> - 1.29.50-2
- Remove duplicated manual BuildRequires
- Drop a redundant build dependency on deprecated python3-toml
- https://fedoraproject.org/wiki/Changes/DeprecatePythonToml

* Fri Jan 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.50-1
- 1.29.50

* Thu Jan 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.49-1
- 1.29.49

* Wed Jan 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.48-1
- 1.29.48

* Wed Jan 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.47-1
- 1.29.47

* Tue Jan 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.46-1
- 1.29.46

* Fri Jan 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.45-1
- 1.29.45

* Fri Jan 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.44-1
- 1.29.44

* Thu Jan 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.43-1
- 1.29.43

* Wed Jan 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.42-1
- 1.29.42

* Tue Jan 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.41-1
- 1.29.41

* Wed Dec 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.35-1
- 1.29.35

* Tue Dec 20 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.34-1
- 1.29.34

* Mon Dec 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.33-1
- 1.29.33

* Fri Dec 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.32-1
- 1.29.32

* Thu Dec 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.31-1
- 1.29.31

* Wed Dec 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.30-1
- 1.29.30

* Wed Dec 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.29-1
- 1.29.29

* Mon Dec 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.28-1
- 1.29.28

* Fri Dec 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.27-1
- 1.29.27

* Thu Dec 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.26-1
- 1.29.26

* Wed Dec 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.25-1
- 1.29.25

* Wed Dec 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.24-1
- 1.29.24

* Mon Dec 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.23-1
- 1.29.23

* Fri Dec 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.22-1
- 1.29.22

* Fri Dec 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.21-1
- 1.29.21

* Thu Dec 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.20-1
- 1.29.20

* Wed Nov 30 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.19-1
- 1.29.19

* Mon Nov 28 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.17-1
- 1.29.17

* Mon Nov 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.14-1
- 1.29.14

* Mon Nov 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.13-1
- 1.29.13

* Thu Nov 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.12-1
- 1.29.12

* Thu Nov 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.11-1
- 1.29.11

* Wed Nov 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.10-1
- 1.29.10

* Tue Nov 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.9-1
- 1.29.9

* Mon Nov 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.8-1
- 1.29.8

* Thu Nov 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.7-1
- 1.29.7

* Thu Nov 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.6-1
- 1.29.6

* Wed Nov 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.5-1
- 1.29.5

* Tue Nov 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.4-1
- 1.29.4

* Mon Nov 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.3-1
- 1.29.3

* Thu Nov 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.2-1
- 1.29.2

* Wed Nov 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.1-1
- 1.29.1

* Tue Nov 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.29.0-1
- 1.29.0

* Mon Oct 31 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.28.5-1
- 1.28.5

* Fri Oct 28 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.28.4-1
- 1.28.4

* Fri Oct 28 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.28.3-1
- 1.28.3

* Wed Oct 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.28.2-1
- 1.28.2

* Wed Oct 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.28.1-1
- 1.28.1

* Fri Oct 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.96-1
- 1.27.96

* Fri Oct 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.95-1
- 1.27.95

* Thu Oct 20 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.94-1
- 1.27.94

* Wed Oct 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.93-1
- 1.27.93

* Mon Oct 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.92-1
- 1.27.92

* Fri Oct 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.91-1
- 1.27.91

* Thu Oct 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.90-1
- 1.27.90

* Fri Oct 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.89-1
- 1.27.89

* Thu Oct 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.88-1
- 1.27.88

* Tue Oct 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.86-1
- 1.27.86

* Tue Oct 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.85-1
- 1.27.85

* Fri Sep 30 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.84-1
- 1.27.84

* Thu Sep 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.83-1
- 1.27.83

* Tue Sep 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.82-1
- 1.27.82

* Mon Sep 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.81-1
- 1.27.81

* Mon Sep 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.80-2
- Bump NVR

* Mon Sep 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.80-1
- 1.27.80

* Fri Sep 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.79-1
- 1.27.79

* Thu Sep 22 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.78-1
- 1.27.78

* Wed Sep 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.77-1
- 1.27.77

* Mon Sep 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.76-1
- 1.27.76

* Fri Sep 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.75-1
- 1.27.75

* Thu Sep 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.74-1
- 1.27.74

* Wed Sep 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.73-1
- 1.27.73

* Tue Sep 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.72-1
- 1.27.72

* Mon Sep 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.71-1
- 1.27.71, patch for test failure

* Mon Aug 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.62-1
- 1.27.62

* Mon Aug 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.61-1
- 1.27.61

* Thu Aug 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.60-1
- 1.27.60

* Thu Aug 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.59-1
- 1.27.59

* Mon Aug 22 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.57-1
- 1.27.57

* Fri Aug 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.56-1
- 1.27.56

* Fri Aug 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.55-1
- 1.27.55

* Wed Aug 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.54-1
- 1.27.54

* Wed Aug 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.53-1
- 1.27.53

* Mon Aug 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.52-1
- 1.27.52

* Fri Aug 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.51-1
- 1.27.51

* Thu Aug 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.50-1
- 1.27.50

* Wed Aug 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.49-1
- 1.27.49

* Tue Aug 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.48-1
- 1.27.48

* Thu Aug 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.46-1
- 1.27.46

* Thu Aug 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.45-1
- 1.27.45

* Tue Aug 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.44-1
- 1.27.44

* Mon Aug 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.43-1
- 1.27.43

* Mon Aug 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.42-1
- 1.27.42

* Fri Jul 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.41-1
- 1.27.41

* Thu Jul 28 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.40-1
- 1.27.40

* Wed Jul 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.39-1
- 1.27.39

* Wed Jul 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.38-1
- 1.27.38

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.35-1
- 1.27.35

* Tue Jul 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.33-1
- 1.27.33

* Thu Jul 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.29-1
- 1.27.29

* Mon Jul 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.27-1
- 1.27.27

* Tue Jul 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.23-1
- 1.27.23

* Fri Jun 24 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.17-1
- 1.27.17

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 1.27.10-2
- Rebuilt for Python 3.11

* Thu Jun 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.10-1
- 1.27.10

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.27.4-2
- Rebuilt for Python 3.11

* Wed Jun 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.4-1
- 1.27.4

* Tue Jun 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.3-1
- 1.27.3

* Fri Jun 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.2-1
- 1.27.2

* Thu Jun 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.1-1
- 1.27.1

* Wed Jun 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.27.0-1
- 1.27.0

* Fri May 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.10-1
- 1.26.10

* Thu May 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.9-1
- 1.26.9

* Wed May 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.8-1
- 1.26.8

* Tue May 24 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.7-1
- 1.26.7

* Mon May 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.6-1
- 1.26.6

* Mon May 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.5-1
- 1.26.5

* Thu May 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.4-1
- 1.26.4

* Thu May 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.3-1
- 1.26.3

* Tue May 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.2-1
- 1.26.2

* Mon May 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.1-1
- 1.26.1

* Fri May 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.0-1
- 1.26.0

* Thu May 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.13-1
- 1.25.13

* Wed May 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.12-1
- 1.25.12

* Wed May 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.11-1
- 1.25.11

* Mon May 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.10-1
- 1.25.10

* Thu May 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.8-1
- 1.25.8

* Wed May 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.7-1
- 1.25.7

* Mon May 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.5-1
- 1.25.5

* Fri Apr 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.4-1
- 1.25.4

* Fri Apr 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.3-1
- 1.25.3

* Wed Apr 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.2-1
- 1.25.2

* Tue Apr 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.1-1
- 1.25.1

* Mon Apr 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.0-1
- 1.25.0

* Fri Apr 22 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.46-1
- 1.24.46

* Thu Apr 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.45-1
- 1.24.45

* Thu Apr 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.44-1
- 1.24.44

* Tue Apr 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.43-1
- 1.24.43

* Fri Apr 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.42-1
- 1.24.42

* Thu Apr 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.41-1
- 1.24.41

* Wed Apr 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.40-1
- 1.24.40

* Wed Apr 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.39-1
- 1.24.39

* Mon Apr 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.38-1
- 1.24.38

* Fri Apr 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.37-1
- 1.24.37

* Thu Apr 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.36-1
- 1.24.36

* Wed Apr 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.35-1
- 1.24.35

* Tue Apr 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.34-1
- 1.24.34

* Mon Apr 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.33-1
- 1.24.33

* Fri Mar 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.27-1
- 1.24.27

* Thu Mar 24 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.26-1
- 1.24.26

* Wed Mar 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.25-1
- 1.24.25

* Tue Mar 22 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.24-1
- 1.24.24

* Mon Mar 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.23-1
- 1.24.23

* Fri Mar 18 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.22-1
- 1.24.22

* Thu Mar 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.21-1
- 1.24.21

* Wed Mar 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.20-1
- 1.24.20

* Mon Mar 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.19-1
- 1.24.19

* Fri Mar 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.18-1
- 1.24.18

* Fri Mar 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.17-1
- 1.24.17

* Wed Mar 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.16-1
- 1.24.16

* Tue Mar 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.15-1
- 1.24.15

* Tue Mar 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.14-1
- 1.24.14

* Mon Mar 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.13-1
- 1.24.13

* Fri Mar 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.12-1
- 1.24.12

* Thu Mar 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.11-1
- 1.24.11

* Fri Feb 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.8-1
- 1.24.8

* Thu Feb 24 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.7-1
- 1.24.7

* Wed Feb 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.6-1
- 1.24.6

* Wed Feb 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.5-1
- 1.24.5

* Thu Feb 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.2-1
- 1.24.2

* Wed Feb 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.1-1
- 1.24.1

* Tue Feb 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.0-1
- 1.24.0

* Fri Feb 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.54-1
- 1.23.54

* Thu Feb 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.53-1
- 1.23.53

* Wed Feb 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.52-1
- 1.23.52

* Tue Feb 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.51-1
- 1.23.51

* Tue Feb 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.50-1
- 1.23.50

* Mon Feb 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.49-1
- 1.23.49

* Thu Feb 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.48-1
- 1.23.48

* Thu Feb 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.47-1
- 1.23.47

* Fri Jan 28 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.46-1
- 1.23.46

* Thu Jan 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.45-1
- 1.23.45

* Tue Jan 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.42-1
- 1.23.42

* Mon Jan 24 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.41-1
- 1.23.41

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 20 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.40-1
- 1.23.40

* Wed Jan 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.39-1
- 1.23.39

* Tue Jan 18 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.38-1
- 1.23.38

* Tue Jan 18 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.37-1
- 1.23.37

* Fri Jan 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.36-1
- 1.23.36

* Thu Jan 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.35-1
- 1.23.35

* Wed Jan 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.34-1
- 1.23.34

* Tue Jan 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.33-1
- 1.23.33

* Mon Jan 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.32-1
- 1.23.32

* Fri Jan 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.31-1
- 1.23.31

* Thu Jan 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.30-1
- 1.23.30

* Wed Jan 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.29-1
- 1.23.29

* Tue Jan 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.28-1
- 1.23.28

* Tue Jan 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.27-1
- 1.23.27

* Tue Dec 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.26-1
- 1.23.26

* Mon Dec 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.25-1
- 1.23.25

* Mon Dec 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.24-1
- 1.23.24

* Thu Dec 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.23-1
- 1.23.23

* Thu Dec 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.22-1
- 1.23.22

* Mon Dec 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.21-1
- 1.23.21

* Fri Dec 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.20-1
- 1.23.20

* Thu Dec 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.19-1
- 1.23.19

* Thu Dec 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.18-1
- 1.23.18

* Wed Dec 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.17-1
- 1.23.17

* Tue Nov 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.16-1
- 1.23.16

* Mon Nov 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.15-1
- 1.23.15

* Tue Nov 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.12-1
- 1.23.12

* Mon Nov 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.11-1
- 1.23.11

* Fri Nov 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.10-1
- 1.23.10

* Thu Nov 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.9-1
- 1.23.9

* Thu Nov 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.8-1
- 1.23.8

* Tue Nov 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.7-1
- 1.23.7

* Mon Nov 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.6-1
- 1.23.6

* Fri Nov 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.5-1
- 1.23.5

* Thu Nov 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.4-1
- 1.23.4

* Wed Nov 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.3-1
- 1.23.3

* Tue Nov 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.2-1
- 1.23.2

* Tue Nov 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.1-1
- 1.23.1

* Mon Nov 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.23.0-1
- 1.23.0

* Fri Nov 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22.12-1
- 1.22.12

* Thu Nov 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22.11-1
- 1.22.11

* Wed Nov 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22.10-1
- 1.22.10

* Tue Nov 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22.9-1
- 1.22.9

* Tue Nov 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22.8-1
- 1.22.8

* Fri Oct 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22.7-1
- 1.22.7

* Thu Oct 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22.6-1
- 1.22.6

* Wed Oct 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22.5-1
- 1.22.5

* Wed Oct 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22.4-1
- 1.22.4

* Tue Oct 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22.3-1
- 1.22.3

* Wed Oct 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22.0-1
- 1.22.0

* Tue Oct 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.65-1
- 1.21.65

* Tue Oct 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.64-1
- 1.21.64

* Fri Oct 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.63-1
- 1.21.63

* Thu Oct 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.62-1
- 1.21.62

* Wed Oct 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.61-1
- 1.21.61

* Tue Oct 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.60-1
- 1.21.60

* Tue Oct 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.59-1
- 1.21.59

* Fri Oct 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.58-1
- 1.21.58

* Thu Oct 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.57-1
- 1.21.57

* Wed Oct 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.56-1
- 1.21.56

* Wed Oct 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.55-1
- 1.21.55

* Fri Oct 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.53-1
- 1.21.53

* Fri Oct 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.52-1
- 1.21.52

* Thu Sep 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.51-1
- 1.21.51

* Tue Sep 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.50-1
- 1.21.50

* Fri Sep 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.48-1
- 1.21.48

* Thu Sep 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.47-1
- 1.21.47

* Wed Sep 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.46-1
- 1.21.46

* Tue Sep 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.45-1
- 1.21.45

* Fri Sep 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.44-1
- 1.21.44

* Thu Sep 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.43-1
- 1.21.43

* Tue Sep 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.42-1
- 1.21.42

* Mon Sep 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.41-1
- 1.21.41

* Mon Sep 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.40-1
- 1.21.40

* Thu Sep 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.39-1
- 1.21.39

* Wed Sep 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.38-1
- 1.21.38

* Wed Sep 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.37-1
- 1.21.37

* Fri Sep 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.36-1
- 1.21.36

* Thu Sep 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.35-1
- 1.21.35

* Thu Sep 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.34-1
- 1.21.34

* Sat Aug 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.31-1
- 1.21.31

* Thu Aug 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.30-1
- 1.21.30

* Wed Aug 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.29-1
- 1.21.29

* Tue Aug 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.28-1
- 1.21.28

* Mon Aug 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.27-1
- 1.21.27

* Fri Aug 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.26-1
- 1.21.26

* Thu Aug 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.25-1
- 1.21.25

* Wed Aug 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.24-1
- 1.21.24

* Tue Aug 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.23-1
- 1.21.23

* Mon Aug 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.22-1
- 1.21.22

* Fri Aug 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.21-1
- 1.21.21

* Thu Aug 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.20-1
- 1.21.20

* Wed Aug 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.19-1
- 1.21.19

* Tue Aug 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.18-1
- 1.21.18

* Mon Aug 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.17-1
- 1.21.17

* Fri Aug 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.16-1
- 1.21.16

* Thu Aug 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.15-1
- 1.21.15

* Wed Aug 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.14-1
- 1.21.14

* Tue Aug 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.13-1
- 1.21.13

* Mon Aug 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.12-1
- 1.21.12

* Fri Jul 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.11-1
- 1.21.11

* Thu Jul 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.10-1
- 1.21.10

* Wed Jul 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.9-1
- 1.21.9

* Tue Jul 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.8-1
- 1.21.8

* Tue Jul 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.7-1
- 1.21.7

* Fri Jul 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.6-1
- 1.21.6

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.5-1
- 1.21.5

* Wed Jul 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.4-1
- 1.21.4

* Tue Jul 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.3-1
- 1.21.3

* Mon Jul 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.2-1
- 1.21.2

* Fri Jul 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.1-1
- 1.21.1

* Thu Jul 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.21.0-1
- 1.21.0

* Wed Jul 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.112-1
- 1.20.112

* Tue Jul 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.111-1
- 1.20.111

* Mon Jul 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.110-1
- 1.20.110

* Fri Jul 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.109-1
- 1.20.109

* Thu Jul 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.108-1
- 1.20.108

* Wed Jul 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.107-1
- 1.20.107

* Tue Jul 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.106-1
- 1.20.106

* Fri Jul 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.105-1
- 1.20.105

* Thu Jul 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.104-1
- 1.20.104

* Wed Jun 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.103-1
- 1.20.103

* Mon Jun 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.102-1
- 1.20.102

* Fri Jun 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.101-1
- 1.20.101

* Thu Jun 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.100-1
- 1.20.100

* Wed Jun 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.99-1
- 1.20.99

* Mon Jun 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.98-1
- 1.20.98

* Thu Jun 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.97-1
- 1.20.97

* Wed Jun 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.96-1
- 1.20.96

* Tue Jun 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.95-1
- 1.20.95

* Mon Jun 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.94-1
- 1.20.94

* Fri Jun 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.93-1
- 1.20.93

* Thu Jun 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.92-1
- 1.20.92

* Wed Jun 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.91-1
- 1.20.91

* Tue Jun 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.90-1
- 1.20.90

* Tue Jun 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.89-2
- rebuilt

* Mon Jun 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.89-1
- 1.20.89

* Mon Jun 07 2021 Python Maint <python-maint@redhat.com> - 1.20.88-2
- Rebuilt for Python 3.10

* Fri Jun 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.88-1
- 1.20.88

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.20.87-2
- Rebuilt for Python 3.10

* Thu Jun 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.87-1
- 1.20.87

* Wed Jun 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.86-1
- 1.20.86

* Tue Jun 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.85-1
- 1.20.85

* Fri May 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.84-1
- 1.20.84

* Thu May 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.83-1
- 1.20.83

* Thu May 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.82-1
- 1.20.82

* Wed May 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.81-1
- 1.20.81

* Tue May 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.80-1
- 1.20.80

* Tue May 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.79-1
- 1.20.79

* Fri May 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.78-1
- 1.20.78

* Thu May 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.77-1
- 1.20.77

* Wed May 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.76-1
- 1.20.76

* Wed May 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.75-1
- 1.20.75

* Mon May 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.74-1
- 1.20.74

* Fri May 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.73-1
- 1.20.73

* Fri May 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.72-1
- 1.20.72

* Tue May 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.71-1
- 1.20.71

* Mon May 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.70-1
- 1.20.70

* Fri May 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.69-1
- 1.20.69

* Thu May 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.68-1
- 1.20.68

* Wed May 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.67-1
- 1.20.67

* Wed May 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.66-1
- 1.20.66

* Tue May 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.65-1
- 1.20.65

* Tue May 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.64-1
- 1.20.64

* Mon May 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.63-1
- 1.20.63

* Fri Apr 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.62-1
- 1.20.62

* Thu Apr 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.61-1
- 1.20.61

* Wed Apr 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.60-1
- 1.20.60

* Tue Apr 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.59-1
- 1.20.59

* Tue Apr 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.58-1
- 1.20.58

* Fri Apr 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.57-1
- 1.20.57

* Thu Apr 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.56-1
- 1.20.56

* Thu Apr 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.55-1
- 1.20.55

* Mon Apr 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.54-1
- 1.20.54

* Thu Apr 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.53-1
- 1.20.53

* Thu Apr 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.52-1
- 1.20.52

* Tue Apr 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.51-1
- 1.20.51

* Mon Apr 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.50-1
- 1.20.50

* Fri Apr 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.49-1
- 1.20.49

* Fri Apr 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.48-1
- 1.20.48

* Wed Apr 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.47-1
- 1.20.47

* Wed Apr 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.46-1
- 1.20.46

* Mon Apr 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.45-1
- 1.20.45

* Mon Apr 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.44-1
- 1.20.44

* Thu Apr 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.43-1
- 1.20.43

* Thu Apr 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.42-1
- 1.20.42

* Wed Mar 31 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.41-1
- 1.20.41

* Tue Mar 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.40-1
- 1.20.40

* Mon Mar 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.39-1
- 1.20.39

* Fri Mar 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.37-1
- 1.20.37

* Thu Mar 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.36-1
- 1.20.36

* Wed Mar 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.35-1
- 1.20.35

* Tue Mar 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.34-1
- 1.20.34

* Mon Mar 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.33-1
- 1.20.33

* Thu Mar 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.31-1
- 1.20.31

* Thu Mar 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.30-1
- 1.20.30

* Wed Mar 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.29-1
- 1.20.29

* Tue Mar 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.28-1
- 1.20.28

* Mon Mar 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.27-1
- 1.20.27

* Fri Mar 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.26-1
- 1.20.26

* Thu Mar 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.25-1
- 1.20.25

* Wed Mar 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.24-1
- 1.20.24

* Tue Mar 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.23-1
- 1.20.23

* Mon Mar 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.22-1
- 1.20.22

* Fri Mar 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.21-1
- 1.20.21

* Thu Mar 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.20-1
- 1.20.20

* Wed Mar 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.19-1
- 1.20.19

* Tue Mar 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.18-1
- 1.20.18

* Mon Mar 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.17-1
- 1.20.17

* Fri Feb 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.16-1
- 1.20.16

* Thu Feb 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.15-1
- 1.20.15

* Wed Feb 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.14-1
- 1.20.14

* Tue Feb 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.13-1
- 1.20.13

* Sat Feb 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.12-1
- 1.20.12

* Fri Feb 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.11-1
- 1.20.11

* Thu Feb 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.10-1
- 1.20.10

* Wed Feb 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.9-1
- 1.20.9

* Tue Feb 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.8-1
- 1.20.8

* Fri Feb 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.6-1
- 1.20.6

* Wed Feb 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.5-1
- 1.20.5

* Tue Feb 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.4-1
- 1.20.4

* Fri Feb 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.3-1
- 1.20.3

* Fri Feb 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.2-1
- 1.20.2

* Wed Feb 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.0-1
- 1.20.0

* Mon Feb 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.63-1
- 1.19.63

* Fri Jan 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.62-1
- 1.19.62

* Thu Jan 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.61-1
- 1.19.61

* Wed Jan 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.60-1
- 1.19.60

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.59-1
- 1.19.59

* Fri Jan 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.58-1
- 1.19.58

* Wed Jan 20 08:14:42 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.57-1
- 1.19.57

* Tue Jan 19 08:21:00 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.56-1
- 1.19.56

* Fri Jan 15 10:36:04 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.55-1
- 1.19.55

* Thu Jan 14 08:13:55 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.54-1
- 1.19.54

* Wed Jan 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.53-2
- Patch to increase bucket test threshold.

* Wed Jan 13 08:29:49 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.53-1
- 1.19.53

* Tue Jan 12 08:13:31 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.52-1
- 1.19.52

* Fri Jan  8 10:46:30 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.51-1
- 1.19.51

* Thu Jan  7 08:25:18 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.50-1
- 1.19.50

* Wed Jan  6 08:09:03 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.49-1
- 1.19.49

* Tue Jan  5 08:23:32 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.48-1
- 1.19.48

* Mon Jan  4 08:27:26 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.47-1
- 1.19.47

* Wed Dec 30 16:15:17 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.46-1
- 1.19.46

* Wed Dec 30 08:21:28 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.45-1
- 1.19.45

* Tue Dec 29 09:09:01 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.44-1
- 1.19.44

* Thu Dec 24 08:15:06 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.43-1
- 1.19.43

* Wed Dec 23 08:29:08 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.42-1
- 1.19.42

* Tue Dec 22 08:21:05 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.41-1
- 1.19.41

* Fri Dec 18 16:24:06 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.40-1
- 1.19.40

* Fri Dec 18 08:13:19 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.39-1
- 1.19.39

* Thu Dec 17 08:10:23 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.38-1
- 1.19.38

* Wed Dec 16 08:16:16 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.37-1
- 1.19.37

* Tue Dec 15 08:25:16 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.36-1
- 1.19.36

* Mon Dec 14 08:55:49 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.35-1
- 1.19.35

* Fri Dec 11 08:06:30 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.34-1
- 1.19.34

* Thu Dec 10 08:15:47 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.33-1
- 1.19.33

* Wed Dec  9 08:48:23 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.32-1
- 1.19.32

* Tue Dec  8 08:18:17 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.31-1
- 1.19.31

* Mon Dec  7 08:19:37 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.30-1
- 1.19.30

* Fri Dec  4 09:42:28 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.29-1
- 1.19.29

* Wed Dec  2 08:19:53 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.28-1
- 1.19.28

* Tue Dec  1 11:44:50 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.26-1
- 1.19.26

* Mon Nov 30 09:13:53 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.25-1
- 1.19.25

* Sun Nov 29 23:16:01 CET 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 1.19.24-2
- also run tests during build, rely on auto-generated requirements

* Tue Nov 24 08:24:37 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.24-1
- 1.19.24

* Mon Nov 23 08:25:04 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.23-1
- 1.19.23

* Fri Nov 20 08:13:27 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.22-1
- 1.19.22

* Thu Nov 19 08:26:36 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.21-1
- 1.19.21

* Wed Nov 18 08:21:58 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.20-1
- 1.19.20

* Tue Nov 17 09:15:08 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.19-1
- 1.19.19

* Mon Nov 16 08:34:42 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.18-1
- 1.19.18

* Thu Nov 12 15:45:59 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.17-1
- 1.19.17

* Thu Nov 12 10:23:55 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.16-1
- 1.19.16

* Wed Nov 11 09:20:06 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.15-1
- 1.19.15

* Mon Nov  9 14:11:42 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.14-1
- 1.19.14

* Mon Nov  9 09:42:26 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.13-1
- 1.19.13

* Fri Nov  6 08:23:51 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.12-1
- 1.19.12

* Thu Nov  5 14:58:29 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.11-1
- 1.19.11

* Tue Nov  3 08:29:36 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.10-1
- 1.19.10

* Mon Nov  2 09:26:02 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.9-1
- 1.19.9

* Fri Oct 30 08:12:36 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.8-1
- 1.19.8

* Thu Oct 29 08:10:31 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.7-1
- 1.19.7

* Wed Oct 28 09:45:23 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.6-1
- 1.19.6

* Tue Oct 27 09:38:01 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.5-1
- 1.19.5

* Fri Oct 23 16:46:42 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.4-1
- 1.19.4

* Fri Oct 23 08:11:47 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.3-1
- 1.19.3

* Thu Oct 22 08:28:32 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.2-1
- 1.19.2

* Tue Oct 20 21:05:38 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.1-1
- 1.19.1

* Tue Oct 20 08:09:45 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.19.0-1
- 1.19.0

* Fri Oct 16 14:54:26 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.18-1
- 1.18.18

* Fri Oct 16 08:08:23 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.17-1
- 1.18.17

* Sat Oct 10 16:03:11 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.16-1
- 1.18.16

* Thu Oct  8 14:29:56 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.15-1
- 1.18.15

* Thu Oct  8 08:59:46 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.14-1
- 1.18.14

* Wed Oct  7 08:55:36 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.13-1
- 1.18.13

* Fri Oct  2 15:33:49 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.11-1
- 1.18.11

* Fri Oct  2 08:18:33 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.10-1
- 1.18.10

* Thu Oct  1 08:14:54 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.9-1
- 1.18.9

* Wed Sep 30 09:03:15 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.8-1
- 1.18.8

* Tue Sep 29 09:13:43 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.7-1
- 1.18.7

* Mon Sep 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.6-1
- 1.18.6

* Fri Sep 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.5-1
- 1.18.5

* Wed Sep 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.4-1
- 1.18.4

* Wed Sep 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.3-1
- 1.18.3

* Mon Sep 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.2-1
- 1.18.2

* Fri Sep 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.1-1
- 1.18.1

* Fri Sep 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.0-1
- 1.18.0

* Wed Sep 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.63-1
- 1.17.63

* Tue Sep 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.62-1
- 1.17.62

* Tue Sep 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.61-1
- 1.17.61

* Mon Sep 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.60-1
- 1.17.60

* Fri Sep 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.59-1
- 1.17.59

* Thu Sep 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.58-1
- 1.17.58

* Wed Sep 09 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.57-1
- 1.17.57

* Tue Sep 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.56-1
- 1.17.56

* Fri Sep 04 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.55-1
- 1.17.55

* Wed Sep 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.54-1
- 1.17.54

* Wed Sep 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.53-1
- 1.17.53

* Tue Sep 01 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.52-1
- 1.17.52

* Mon Aug 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.51-1
- 1.17.51

* Fri Aug 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.50-1
- 1.17.50

* Thu Aug 27 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.49-1
- 1.17.49

* Tue Aug 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.48-1
- 1.17.48

* Fri Aug 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.47-1
- 1.17.47

* Wed Aug 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.46-1
- 1.17.46

* Wed Aug 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.45-1
- 1.17.45

* Tue Aug 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.44-1
- 1.17.44

* Mon Aug 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.43-1
- 1.17.43

* Fri Aug 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.42-1
- 1.17.42

* Thu Aug 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.41-1
- 1.17.41

* Wed Aug 12 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.40-1
- 1.17.40

* Tue Aug 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.39-1
- 1.17.39

* Mon Aug 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.38-1
- 1.17.38

* Thu Aug 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.37-1
- 1.17.37

* Thu Aug 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.36-1
- 1.17.36

* Wed Aug 05 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.35-1
- 1.17.35

* Tue Aug 04 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.34-1
- 1.17.34

* Fri Jul 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.33-1
- 1.17.33

* Fri Jul 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.32-1
- 1.17.32

* Thu Jul 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.31-1
- 1.17.31

* Wed Jul 29 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.30-1
- 1.17.30

* Tue Jul 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.29-1
- 1.17.29

* Fri Jul 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.28-1
- 1.17.28

* Fri Jul 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.27-1
- 1.17.27

* Thu Jul 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.26-1
- 1.17.26

* Wed Jul 22 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.25-1
- 1.17.25

* Tue Jul 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.24-1
- 1.17.24

* Mon Jul 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.23-1
- 1.17.23

* Fri Jul 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.22-1
- 1.17.22

* Thu Jul 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.21-1
- 1.17.21

* Fri Jul 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.20-1
- 1.17.20

* Thu Jul 09 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.19-1
- 1.17.19

* Wed Jul 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.18-1
- 1.17.18

* Tue Jul 07 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.17-1
- 1.17.17

* Fri Jul 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.16-1
- 1.17.16

* Thu Jul 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.15-1
- 1.17.15

* Wed Jul 01 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.14-1
- 1.17.14

* Tue Jun 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.13-1
- 1.17.13

* Sat Jun 27 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.12-1
- 1.17.12

* Fri Jun 26 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.11-1
- 1.17.11

* Thu Jun 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.10-1
- 1.17.10

* Wed Jun 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.9-1
- 1.17.9

* Tue Jun 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.8-1
- 1.17.8

* Mon Jun 22 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.7-1
- 1.17.7

* Fri Jun 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.6-1
- 1.17.6

* Thu Jun 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.5-1
- 1.17.5

* Wed Jun 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.4-1
- 1.17.4

* Tue Jun 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.3-1
- 1.17.3

* Sat Jun 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.2-1
- 1.17.2

* Thu Jun 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.1-1
- 1.17.1

* Thu Jun 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.17.0-1
- 1.17.0

* Sat Jun 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.24-1
- 1.16.24

* Fri Jun 05 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.23-1
- 1.16.23

* Thu Jun 04 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.22-1
- 1.16.22

* Tue Jun 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.20-1
- 1.16.20

* Sun May 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.19-1
- 1.16.19

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.16.16-2
- Rebuilt for Python 3.9

* Fri May 22 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.16-1
- 1.16.16

* Thu May 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.15-1
- 1.16.15

* Wed May 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.14-1
- 1.16.14

* Wed May 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.12-1
- 1.16.12

* Mon May 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.11-1
- 1.16.11

* Thu May 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.10-1
- 1.16.10

* Thu May 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.9-1
- 1.16.9

* Wed May 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.8-1
- 1.16.8

* Tue May 12 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.7-1
- 1.16.7

* Fri May 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.6-1
- 1.16.6

* Fri May 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.5-1
- 1.16.5

* Thu May 07 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.4-1
- 1.16.4

* Wed May 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.3-1
- 1.16.3

* Tue May 05 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.2-1
- 1.16.2

* Sat May 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.1-1
- 1.16.1

* Fri May 01 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.0-1
- 1.16.0

* Thu Apr 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.49-1
- 1.15.49

* Wed Apr 29 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.48-1
- 1.15.48

* Tue Apr 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.47-1
- 1.15.47

* Sat Apr 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.46-1
- 1.15.46

* Thu Apr 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.45-1
- 1.15.45

* Thu Apr 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.44-1
- 1.15.44

* Wed Apr 22 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.43-1
- 1.15.43

* Mon Apr 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.42-1
- 1.15.42

* Sun Apr 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.41-1
- 1.15.41

* Fri Apr 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.40-1
- 1.15.40

* Thu Apr 09 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.15.39-2
- Fix docutils 0.16 runtime dependency issue

* Thu Apr 09 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.39-1
- 1.15.39

* Wed Apr 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.38-2
- Python 3.9 fix

* Wed Apr 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.38-1
- 1.15.38

* Tue Apr 07 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.37-1
- 1.15.37

* Mon Apr 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.36-1
- 1.15.36

* Fri Apr 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.35-1
- 1.15.35

* Wed Apr 01 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.34-1
- 1.15.34

* Wed Apr 01 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.33-1
- 1.15.33

* Mon Mar 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.32-1
- 1.15.32

* Fri Mar 27 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.31-1
- 1.15.31

* Fri Mar 27 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.30-1
- 1.15.30

* Wed Mar 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.29-1
- 1.15.29

* Wed Mar 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.28-1
- 1.15.28

* Tue Mar 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.27-1
- 1.15.27

* Sat Mar 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.26-1
- 1.15.26

* Fri Mar 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.25-1
- 1.15.25

* Thu Mar 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.24-1
- 1.15.24

* Wed Mar 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.23-1
- 1.15.23

* Mon Mar 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.22-1
- 1.15.22

* Mon Mar 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.21-1
- 1.15.21

* Fri Mar 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.20-1
- 1.15.20

* Thu Mar 12 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.19-1
- 1.15.19

* Wed Mar 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.18-1
- 1.15.18

* Tue Mar 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.17-1
- 1.15.17

* Sun Mar 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.16-1
- 1.15.16

* Fri Mar 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.15-1
- 1.15.15

* Thu Mar 05 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.14-1
- 1.15.14

* Wed Mar 04 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.13-1
- 1.15.13

* Tue Mar 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.12-1
- 1.15.12

* Fri Feb 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.9-1
- 1.15.9

* Thu Feb 27 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.15.8-1
- Update to 1.15.8

* Wed Feb 26 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.7-1
- 1.15.7.

* Mon Feb 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.6-1
- 1.15.6.

* Mon Feb 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.5-1
- 1.15.5.

* Thu Feb 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.3-1
- 1.15.3.

* Thu Feb 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.17-1
- 1.14.17.

* Fri Feb 07 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.14.12-1
- Update to 1.14.12

* Wed Jan 29 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.14.9-1
- Update to 1.14.9

* Thu Jan 16 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.14.4-1
- Update to 1.14.4

* Tue Dec 31 2019 David Duncan <davdunc@amazon.com> - 1.13.45-2
- Bumping to version 1.13.45

* Tue Nov 19 2019 Orion Poplawski <orion@nwra.com> - 1.13.21-1
- Update to 1.13.21

* Mon Oct 28 2019 David Duncan <davdunc@amazon.com> - 1.13.2-1
- Merge changes from 1.13.2 release. (#1677950)

* Mon Oct 21 2019 James Hogarth <james.hogarth@gmail.com> - 1.12.253-2
* Fix changelog format

* Sat Oct 19 2019 David Duncan <davedunc@amazon.com> - 1.12.253-1
- Merge changes from 1.12.253 release. (#1677950)

* Fri Oct 04 2019 David Duncan <davedunc@amazon.com> - 1.12.243-1
- Merge changes from 1.12.243 release. (#1677950)

* Thu Oct 03 2019 David Duncan <davedunc@amazon.com> - 1.12.242-1
- Merge changes from 1.12.242 release. (#1677950)

* Thu Oct 03 2019 David Duncan <davedunc@amazon.com> - 1.12.241-1
- Merge changes from 1.12.241 release. (#1677950)

* Tue Oct 01 2019 David Duncan <davedunc@amazon.com> - 1.12.240-1
- Merge changes from 1.12.240 release. (#1677950)

* Mon Sep 30 2019 David Duncan <davedunc@amazon.com> - 1.12.239-1
- Merge changes from 1.12.239 release. (#1677950)

* Sat Sep 28 2019 David Duncan <davedunc@amazon.com> - 1.12.238-1
- Merge changes from 1.12.238 release. (#1677950)

* Thu Sep 26 2019 David Duncan <davdunc@amazon.com> - 1.12.237-1
- Merge changes from 1.12.237 release. (#1677950)

* Thu Sep 26 2019 David Duncan <davdunc@amazon.com> - 1.12.236-1
- Merge changes from 1.12.236 release.

* Sun Sep 22 2019 David Duncan <davdunc@amazon.com> - 1.12.233-1
- Merge changes from 1.12.233 release.

* Thu Sep 19 2019 David Duncan <davdunc@amazon.com> - 1.12.231 
- Update to 1.12.231
- Update to latest endpoints and models

* Mon Sep 09 2019 Charalampos Stratakis <cstratak@redhat.com> - 1.12.225-1
- Update to 1.12.225

* Wed Aug 21 2019 Kevin Fenzi <kevin@scrye.com> - 1.12.212-1
- Update to 1.12.212

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.12.188-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.188-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 David Duncan <davdunc@amazon.com> - 1.12.188-1
- Bumping version to 1.12.188
- resolves #1677950
- update to latest endpoints and models

* Tue May 28 2019 David Duncan <davdunc@amazon.com> - 1.12.157-1
- Bumping to version 1.12.157
- resolves #1677950
- update to latest endpoints and models

* Wed Apr 24 2019 David Duncan <dadvunc@amazon.com> - 1.12.135-1
- Bumping version to 1.12.135
- add support for ap-east-1

* Thu Mar 21 2019 David Duncan <davdunc@amazon.com> - 1.12.119-1
- resolves #1677950
- Bumping version to 1.12.119


* Sat Feb 23 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.12.101-1
- Update to 1.12.101

* Fri Feb 15 2019 Kevin Fenzi <kevin@scrye.com> - 1.12.96-1
- Update to 1.12.96.

* Sun Feb 10 2019 David Duncan <davdunc@amazon.com> - 1.12.91
- resolves #1667630
- Update to latest models
- api-change:``discovery``: Update discovery client to latest version
- api-change:``ecs``: Update ecs client to latest version
- api-change:``dlm``: Update dlm client to latest version

* Mon Feb 04 2019 David Duncan <davdunc@amazon.com> - 1.12.87
- Update to latest models
- Improve event stream parser tests
- resolves #1667630

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.12.75-3
- Enable python dependency generator

* Wed Jan 09 2019 Miro Hrončok <mhroncok@redhat.com> - 1.12.75-2
- Subpackage python2-botocore has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Jan 08 2019 David Duncan <davdunc@amazon.com> - 1.12.75
- Update to latest endpoints
- Update to latest models

* Sun Nov 18 2018 David Duncan <davdunc@amazon.com> - 1.12.47
- Update to latest models.

* Sun Oct 07 2018 David Duncan <davdunc@amazon.com> - 1.12.18
- Update to latest models 

* Tue Oct 02 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.12.15-2
- Reinstate python-urllib3 dependency as python-boto3 requires it

* Tue Oct 02 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.12.15-1
- Update to 1.12.15

* Wed Sep 5 2018 David Duncan <davdunc@amazon.com> - 1.10.43-1
- Bumping version to 1.10.43 Updates bz#1531330

* Mon Sep 3 2018 David Duncan <davdunc@amazon.com> - 1.10.42-1
- Bumping version to 1.10.42 Updates bz#1531330

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.10.41-3
- Rebuilt for Python 3.7

* Wed Jun 20 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.10.41-2
- Fix EL7 dateutil patch

* Wed Jun 20 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.10.41-1
- Upstream 1.10.41

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.1-3
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.9.1-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 28 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.8.33-1
- Update to 1.8.33

* Tue Jan 16 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.8.29-1
- Update to 1.8.29

* Wed Jan 10 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.8.26-1
- Update to 1.8.26

* Wed Jan 03 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.8.21-1
- Update to 1.8.21

* Sun Aug 13 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.72-1
- Update to 1.5.72

* Tue May 23 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.53-1
- Update to 1.5.53

* Wed Mar 15 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.26-1
- Update to 1.5.26

* Sat Feb 25 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.18-1
- Update to 1.5.18

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.3-1
- Update to 1.5.3
- Rebase patch

* Wed Dec 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.91-1
- Update to 1.4.91

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.4.85-2
- Rebuild for Python 3.6

* Sun Dec 11 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.85-1
- Update to 1.4.85

* Sat Dec 03 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.81-1
- Update to 1.4.81

* Thu Nov 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.78-1
- Update to 1.4.78

* Thu Oct 27 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.67-1
- Update to 1.4.67

* Mon Oct 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.60-1
- Update to 1.4.60

* Sun Oct 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.58-1
- Update to 1.4.58
- Add python-six dependency

* Wed Sep 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.57-1
- Update to 1.4.57

* Tue Sep 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.52-3
- Fix patch

* Tue Sep 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.52-2
- Add testing support for EL7 using a lower version of dateuil library

* Wed Sep 07 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.52-1
- Update to 1.4.52

* Sat Sep 03 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.4.50-1
- Update to 1.4.50

* Wed Aug 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.49-1
- Upstream update

* Tue Aug 23 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.48-1
- Upstream update

* Fri Aug 05 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.43-1
- Upstream update

* Thu Aug 04 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.42-1
- Upstream update

* Tue Aug 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.41-1
- Upstream update

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.35-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.35-1
- New version from upstream

* Wed Jun 08 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.26-1
- New version from upstream

* Sat May 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.24-1
- New version from upstream

* Tue Mar 29 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.7-1
- New version from upstream

* Tue Mar 01 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.30-1
- New version from upstream

* Wed Feb 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.29-1
- New version from upstream

* Fri Feb 19 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.28-1
- New version from upstream

* Wed Feb 17 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.27-1
- New version from upstream

* Fri Feb 12 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.26-1
- New version from upstream

* Wed Feb 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.25-1
- New version from upstream

* Tue Feb 09 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.24-1
- New version from upstream

* Tue Feb 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.23-1
- New version from upstream

* Fri Jan 22 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.22-1
- New version from upstream

* Wed Jan 20 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.21-1
- New version from upstream

* Fri Jan 15 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.20-1
- New version from upstream

* Fri Jan 15 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.19-1
- New version from upstream

* Wed Jan 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.18-1
- New version from upstream

* Tue Jan 12 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.17-2
- Add testing for Fedora

* Thu Jan 07 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.17-1
- Update to upstream version

* Wed Jan 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.16-2
- Fix shabang on botocore/vendored/requests/packages/chardet/chardetect.py
- Fix shabang on botocore/vendored/requests/certs.py
- Remove the useless dependency with python-urllib3

* Wed Jan 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.16-1
- Update to new upstream version
- Fix Provides for EL6

* Tue Dec 29 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.15-1
- Update to current version
- Improve the spec

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 19 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.79.0-1
- New version

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.58.0-2
- Add Python 3 support

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.58.0-1
- Initial packaging
