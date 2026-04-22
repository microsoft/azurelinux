# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond tests 1
# We would like to have a BuildRequires and weak runtime dependency on
# python3-awscrt, which enables additional functionality and tests, but it is
# ExcludeArch: s390x (https://bugzilla.redhat.com/show_bug.cgi?id=2180988) and
# we do not want to add architecture conditionals to this package, so we omit
# the dependency for now.
%bcond awscrt 0

Name:           python-boto3
Version:        1.42.52
Release: 2%{?dist}
Summary:        The AWS SDK for Python

License:        Apache-2.0
URL:            https://github.com/boto/boto3
Source:         %{url}/archive/%{version}/boto3-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel

# Save space by hardlinking duplicate JSON resource files
BuildRequires:  hardlink

%if %{with tests}
# Test dependencies are in requirements-dev.txt; most are Window-specific or
# are for coverage analysis and are undesired, so we list those we need
# manually:
BuildRequires:  %{py3_dist pytest}
# Run tests in parallel. Tests are numerous and painfully slow, so this helps!
BuildRequires:  %{py3_dist pytest-xdist}
%endif

%global _description %{expand:
Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for
Python, which allows Python developers to write software that makes use of
services like Amazon S3 and Amazon EC2.}

%description %{_description}

%package -n     python3-boto3
Summary:        %{summary}

%if %{with awscrt}
# Optional dependency that enables additional functionality and additional
# tests, and is needed for the import-only “smoke test”:
#   boto3-1.34.7/boto3/s3/transfer.py
#   185:    # This feature requires awscrt>=0.19.18
BuildRequires:  %{py3_dist awscrt} >= 0.19.18
Recommends:     %{py3_dist awscrt} >= 0.19.18
%endif

%description -n python3-boto3 %{_description}

%prep
%setup -q -n boto3-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
# This saves, as of this writing, roughly 300kB in duplicate JSON resource
# files. Note that rpmlint will complain about cross-directory hardlinks, but
# that these are not a problem because the contents of a directory owned by
# this package are guaranteed to be on a single filesystem.
hardlink -c '%{buildroot}%{python3_sitelib}/boto3'
%pyproject_save_files boto3

%check
%if %{with tests}
# Integration tests require network access and real AWS resources.
%pytest --ignore=tests/integration -v -n auto
%else
%pyproject_check_import %{?!with_awscrt:-e boto3.crt}
%endif

%files -n python3-boto3 -f %{pyproject_files}
%doc CHANGELOG.rst
%doc README.rst
%license LICENSE

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

* Mon Dec 01 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.42.0-1
- 1.42.0

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

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 1.38.30-2
- Rebuilt for Python 3.14

* Wed Jun 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.38.30-1
- 1.38.30

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

* Wed Jan 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.34.11-2
- Port to pyproject-rpm-macros
- Save space by hardlinking duplicate JSON resource files
- Various small packaging improvements

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

* Mon Nov 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.7-1
- 1.29.7

* Tue Nov 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.5-1
- 1.29.5

* Tue Nov 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.4-1
- 1.29.4

* Mon Nov 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.3-1
- 1.29.3

* Thu Nov 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.2-1
- 1.29.2

* Wed Nov 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.1-1
- 1.29.1

* Tue Nov 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.29.0-1
- 1.29.0

* Mon Nov 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.85-1
- 1.28.85

* Mon Nov 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.84-1
- 1.28.84

* Thu Nov 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.83-1
- 1.28.83

* Thu Nov 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.82-1
- 1.28.82

* Wed Nov 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.81-1
- 1.28.81

* Wed Nov 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.80-1
- 1.28.80

* Mon Nov 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.79-1
- 1.28.79

* Fri Nov 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.78-1
- 1.28.78

* Thu Nov 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.77-1
- 1.28.77

* Wed Nov 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.76-1
- 1.28.76

* Wed Nov 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.75-1
- 1.28.75

* Mon Oct 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.74-1
- 1.28.74

* Fri Oct 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.73-1
- 1.28.73

* Thu Oct 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.72-1
- 1.28.72

* Thu Oct 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.71-1
- 1.28.71

* Tue Oct 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.70-1
- 1.28.70

* Mon Oct 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.69-1
- 1.28.69

* Mon Oct 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.68-1
- 1.28.68

* Thu Oct 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.67-1
- 1.28.67

* Wed Oct 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.66-1
- 1.28.66

* Tue Oct 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.65-1
- 1.28.65

* Mon Oct 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.64-1
- 1.28.64

* Thu Oct 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.63-1
- 1.28.63

* Fri Oct 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.62-1
- 1.28.62

* Thu Oct 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.61-1
- 1.28.61

* Wed Oct 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.60-1
- 1.28.60

* Tue Oct 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.59-1
- 1.28.59

* Tue Oct 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.58-1
- 1.28.58

* Thu Sep 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.57-1
- 1.28.57

* Thu Sep 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.56-1
- 1.28.56

* Thu Sep 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.55-1
- 1.28.55

* Mon Sep 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.54-1
- 1.28.54

* Fri Sep 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.53-1
- 1.28.53

* Wed Sep 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.52-1
- 1.28.52

* Tue Sep 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.51-1
- 1.28.51

* Tue Sep 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.50-1
- 1.28.50

* Fri Sep 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.49-1
- 1.28.49

* Thu Sep 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.48-1
- 1.28.48

* Wed Sep 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.47-1
- 1.28.47

* Tue Sep 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.46-1
- 1.28.46

* Mon Sep 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.45-1
- 1.28.45

* Fri Sep 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.44-1
- 1.28.44

* Thu Sep 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.43-1
- 1.28.43

* Wed Sep 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.42-1
- 1.28.42

* Tue Sep 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.41-1
- 1.28.41

* Tue Sep 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.40-1
- 1.28.40

* Fri Sep 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.39-1
- 1.28.39

* Wed Aug 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.38-1
- 1.28.38

* Wed Aug 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.37-1
- 1.28.37

* Mon Aug 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.36-1
- 1.28.36

* Fri Aug 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.35-1
- 1.28.35

* Thu Aug 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.34-1
- 1.28.34

* Wed Aug 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.33-1
- 1.28.33

* Wed Aug 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.32-1
- 1.28.32

* Fri Aug 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.30-1
- 1.28.30

* Thu Aug 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.29-1
- 1.28.29

* Wed Aug 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.28-1
- 1.28.28

* Wed Aug 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.27-1
- 1.28.27

* Mon Aug 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.26-1
- 1.28.26

* Fri Aug 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.25-1
- 1.28.25

* Thu Aug 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.24-1
- 1.28.24

* Wed Aug 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.23-1
- 1.28.23

* Tue Aug 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.22-1
- 1.28.22

* Mon Aug 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.21-1
- 1.28.21

* Fri Aug 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.20-1
- 1.28.20

* Thu Aug 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.19-1
- 1.28.19

* Wed Aug 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.18-1
- 1.28.18

* Tue Aug 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.17-1
- 1.28.17

* Mon Jul 31 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.16-1
- 1.28.16

* Fri Jul 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.15-1
- 1.28.15

* Fri Jul 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.14-1
- 1.28.14

* Thu Jul 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.13-1
- 1.28.13

* Wed Jul 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.12-1
- 1.28.12

* Tue Jul 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.11-1
- 1.28.11

* Mon Jul 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.10-1
- 1.28.10

* Mon Jul 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.9-1
- 1.28.9

* Fri Jul 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.7-1
- 1.28.7

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.6-1
- 1.28.6

* Tue Jul 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.5-1
- 1.28.5

* Tue Jul 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.4-1
- 1.28.4

* Mon Jul 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.3-1
- 1.28.3

* Tue Jul 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.2-1
- 1.28.2

* Fri Jul 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.1-1
- 1.28.1

* Thu Jul 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.28.0-1
- 1.28.0

* Wed Jul 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.27.1-1
- 1.27.1

* Fri Jun 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.164-1
- 1.26.164

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 1.26.163-2
- Rebuilt for Python 3.12

* Wed Jun 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.163-1
- 1.26.163

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 1.26.162-2
- Rebuilt for Python 3.12

* Tue Jun 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.162-1
- 1.26.162

* Tue Jun 27 2023 Python Maint <python-maint@redhat.com> - 1.26.161-2
- Rebuilt for Python 3.12

* Mon Jun 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.161-1
- 1.26.161

* Mon Jun 26 2023 Python Maint <python-maint@redhat.com> - 1.26.160-2
- Rebuilt for Python 3.12

* Fri Jun 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.160-1
- 1.26.160

* Thu Jun 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.159-1
- 1.26.159

* Wed Jun 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.158-1
- 1.26.158

* Wed Jun 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.157-1
- 1.26.157

* Tue Jun 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.156-1
- 1.26.156

* Sun Jun 18 2023 Python Maint <python-maint@redhat.com> - 1.26.155-2
- Rebuilt for Python 3.12

* Sat Jun 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.155-1
- 1.26.155

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 1.26.154-2
- Rebuilt for Python 3.12

* Thu Jun 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.154-1
- 1.26.154

* Tue Jun 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.153-1
- 1.26.153

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.26.152-2
- Rebuilt for Python 3.12

* Mon Jun 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.152-1
- 1.26.152

* Fri Jun 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.151-1
- 1.26.151

* Thu Jun 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.150-1
- 1.26.150

* Wed Jun 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.149-1
- 1.26.149

* Tue Jun 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.148-1
- 1.26.148

* Mon Jun 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.147-1
- 1.26.147

* Fri Jun 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.146-1
- 1.26.146

* Thu Jun 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.145-1
- 1.26.145

* Wed May 31 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.144-1
- 1.26.144

* Tue May 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.143-1
- 1.26.143

* Fri May 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.142-1
- 1.26.142

* Thu May 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.141-1
- 1.26.141

* Thu May 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.140-1
- 1.26.140

* Tue May 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.139-1
- 1.26.139

* Mon May 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.138-1
- 1.26.138

* Fri May 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.137-1
- 1.26.137

* Thu May 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.136-1
- 1.26.136

* Tue May 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.135-1
- 1.26.135

* Tue May 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.134-1
- 1.26.134

* Fri May 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.133-1
- 1.26.133

* Wed May 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.132-1
- 1.26.132

* Tue May 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.131-1
- 1.26.131

* Mon May 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.130-1
- 1.26.130

* Mon May 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.129-1
- 1.26.129

* Fri May 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.128-1
- 1.26.128

* Thu May 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.127-1
- 1.26.127

* Wed May 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.126-1
- 1.26.126

* Tue May 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.125-1
- 1.26.125

* Mon May 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.124-1
- 1.26.124

* Fri Apr 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.123-1
- 1.26.123

* Thu Apr 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.122-1
- 1.26.122

* Wed Apr 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.121-1
- 1.26.121

* Tue Apr 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.120-1
- 1.26.120

* Tue Apr 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.119-1
- 1.26.119

* Fri Apr 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.118-1
- 1.26.118

* Thu Apr 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.117-1
- 1.26.117

* Wed Apr 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.116-1
- 1.26.116

* Mon Apr 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.115-1
- 1.26.115

* Fri Apr 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.114-1
- 1.26.114

* Thu Apr 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.113-1
- 1.26.113

* Thu Apr 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.112-1
- 1.26.112

* Wed Apr 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.111-1
- 1.26.111

* Tue Apr 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.110-1
- 1.26.110

* Thu Apr 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.108-1
- 1.26.108

* Thu Apr 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.107-1
- 1.26.107

* Tue Apr 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.106-1
- 1.26.106

* Mon Apr 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.105-1
- 1.26.105

* Fri Mar 31 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.104-1
- 1.26.104

* Thu Mar 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.103-1
- 1.26.103

* Thu Mar 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.102-1
- 1.26.102

* Wed Mar 29 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.101-1
- 1.26.101

* Mon Mar 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.100-1
- 1.26.100

* Fri Mar 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.99-1
- 1.26.99

* Thu Mar 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.98-1
- 1.26.98

* Wed Mar 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.97-1
- 1.26.97

* Tue Mar 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.96-1
- 1.26.96

* Mon Mar 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.95-1
- 1.26.95

* Fri Mar 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.94-1
- 1.26.94

* Thu Mar 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.93-1
- 1.26.93

* Wed Mar 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.92-1
- 1.26.92

* Wed Mar 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.91-1
- 1.26.91

* Mon Mar 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.90-1
- 1.26.90

* Fri Mar 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.89-1
- 1.26.89

* Thu Mar 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.88-1
- 1.26.88

* Wed Mar 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.87-1
- 1.26.87

* Tue Mar 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.86-1
- 1.26.86

* Tue Mar 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.85-1
- 1.26.85

* Fri Mar 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.84-1
- 1.26.84

* Thu Mar 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.83-1
- 1.26.83

* Thu Mar 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.82-2
- migrate to SPDX license

* Wed Mar 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.82-1
- 1.26.82

* Tue Feb 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.81-1
- 1.26.81

* Mon Feb 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.80-1
- 1.26.80

* Fri Feb 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.79-1
- 1.26.79

* Thu Feb 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.78-1
- 1.26.78

* Wed Feb 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.77-1
- 1.26.77

* Tue Feb 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.76-1
- 1.26.76

* Tue Feb 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.75-1
- 1.26.75

* Fri Feb 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.74-1
- 1.26.74

* Thu Feb 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.73-1
- 1.26.73

* Wed Feb 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.72-1
- 1.26.72

* Tue Feb 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.71-1
- 1.26.71

* Mon Feb 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.70-1
- 1.26.70

* Fri Feb 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.69-1
- 1.26.69

* Thu Feb 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.68-1
- 1.26.68

* Thu Feb 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.67-1
- 1.26.67

* Tue Feb 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.66-1
- 1.26.66

* Mon Feb 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.65-1
- 1.26.65

* Fri Feb 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.64-1
- 1.26.64

* Thu Feb 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.63-1
- 1.26.63

* Wed Feb 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.62-1
- 1.26.62

* Tue Jan 31 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.61-1
- 1.26.61

* Mon Jan 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.60-1
- 1.26.60

* Fri Jan 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.59-1
- 1.26.59

* Thu Jan 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.58-1
- 1.26.58

* Wed Jan 25 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.57-1
- 1.26.57

* Tue Jan 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.56-1
- 1.26.56

* Mon Jan 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.55-1
- 1.26.55

* Mon Jan 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.54-1
- 1.26.54

* Fri Jan 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.53-1
- 1.26.53

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.52-1
- 1.26.52

* Tue Jan 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.51-1
- 1.26.51

* Fri Jan 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.50-1
- 1.26.50

* Thu Jan 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.49-1
- 1.26.49

* Wed Jan 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.48-1
- 1.26.48

* Wed Jan 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.47-1
- 1.26.47

* Tue Jan 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.46-1
- 1.26.46

* Fri Jan 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.45-1
- 1.26.45

* Fri Jan 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.44-1
- 1.26.44

* Thu Jan 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.43-1
- 1.26.43

* Wed Jan 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.42-1
- 1.26.42

* Tue Jan 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.26.41-1
- 1.26.41

* Wed Dec 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.35-1
- 1.26.35

* Tue Dec 20 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.34-1
- 1.26.34

* Mon Dec 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.33-1
- 1.26.33

* Fri Dec 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.32-1
- 1.26.32

* Thu Dec 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.31-1
- 1.26.31

* Wed Dec 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.30-1
- 1.26.30

* Wed Dec 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.29-1
- 1.26.29

* Mon Dec 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.28-1
- 1.26.28

* Fri Dec 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.27-1
- 1.26.27

* Thu Dec 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.26-1
- 1.26.26

* Wed Dec 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.25-1
- 1.26.25

* Wed Dec 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.24-1
- 1.26.24

* Mon Dec 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.23-1
- 1.26.23

* Fri Dec 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.22-1
- 1.26.22

* Fri Dec 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.21-1
- 1.26.21

* Thu Dec 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.20-1
- 1.26.20

* Wed Nov 30 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.19-1
- 1.26.19

* Mon Nov 28 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.17-1
- 1.26.17

* Mon Nov 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.14-1
- 1.26.14

* Mon Nov 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.13-1
- 1.26.13

* Thu Nov 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.12-1
- 1.26.12

* Thu Nov 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.11-1
- 1.26.11

* Wed Nov 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.10-1
- 1.26.10

* Tue Nov 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.9-1
- 1.26.9

* Mon Nov 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.8-1
- 1.26.8

* Thu Nov 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.7-1
- 1.26.7

* Thu Nov 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.6-1
- 1.26.6

* Wed Nov 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.5-1
- 1.26.5

* Tue Nov 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.4-1
- 1.26.4

* Mon Nov 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.3-1
- 1.26.3

* Thu Nov 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.2-1
- 1.26.2

* Wed Nov 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.1-1
- 1.26.1

* Tue Nov 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.26.0-1
- 1.26.0

* Mon Oct 31 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.5-1
- 1.25.5

* Fri Oct 28 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.4-1
- 1.25.4

* Fri Oct 28 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.3-1
- 1.25.3

* Wed Oct 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.2-1
- 1.25.2

* Wed Oct 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.25.1-1
- 1.25.1

* Fri Oct 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.96-1
- 1.24.96

* Fri Oct 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.95-1
- 1.24.95

* Thu Oct 20 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.94-1
- 1.24.94

* Wed Oct 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.93-1
- 1.24.93

* Mon Oct 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.92-1
- 1.24.92

* Fri Oct 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.91-1
- 1.24.91

* Thu Oct 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.90-1
- 1.24.90

* Fri Oct 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.89-1
- 1.24.89

* Thu Oct 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.88-1
- 1.24.88

* Tue Oct 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.86-1
- 1.24.86

* Tue Oct 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.85-1
- 1.24.85

* Fri Sep 30 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.84-1
- 1.24.84

* Thu Sep 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.83-1
- 1.24.83

* Tue Sep 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.82-1
- 1.24.82

* Mon Sep 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.81-1
- 1.24.81

* Mon Sep 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.80-2
- Bump NVR

* Mon Sep 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.80-1
- 1.24.80

* Fri Sep 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.79-1
- 1.24.79

* Thu Sep 22 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.78-1
- 1.24.78

* Wed Sep 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.77-1
- 1.24.77

* Mon Sep 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.76-1
- 1.24.76

* Fri Sep 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.75-1
- 1.24.75

* Thu Sep 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.74-1
- 1.24.74

* Wed Sep 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.73-1
- 1.24.73

* Tue Sep 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.72-1
- 1.24.72

* Mon Sep 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.71-1
- 1.24.71

* Mon Aug 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.62-1
- 1.24.62

* Mon Aug 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.61-1
- 1.24.61

* Thu Aug 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.60-1
- 1.24.60

* Thu Aug 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.59-1
- 1.24.59

* Mon Aug 22 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.57-1
- 1.24.57

* Fri Aug 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.56-1
- 1.24.56

* Fri Aug 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.55-1
- 1.24.55

* Wed Aug 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.54-1
- 1.24.54

* Wed Aug 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.53-1
- 1.24.53

* Mon Aug 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.52-1
- 1.24.52

* Fri Aug 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.51-1
- 1.24.51

* Thu Aug 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.50-1
- 1.24.50

* Wed Aug 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.49-1
- 1.24.49

* Tue Aug 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.48-1
- 1.24.48

* Thu Aug 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.46-1
- 1.24.46

* Thu Aug 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.45-1
- 1.24.45

* Tue Aug 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.44-1
- 1.24.44

* Mon Aug 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.43-1
- 1.24.43

* Mon Aug 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.42-1
- 1.24.42

* Fri Jul 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.41-1
- 1.24.41

* Thu Jul 28 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.40-1
- 1.24.40

* Wed Jul 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.39-1
- 1.24.39

* Wed Jul 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.38-1
- 1.24.38

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.35-1
- 1.24.35

* Tue Jul 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.33-1
- 1.24.33

* Thu Jul 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.29-1
- 1.24.29

* Mon Jul 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.27-1
- 1.24.27

* Tue Jul 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.23-1
- 1.24.23

* Fri Jun 24 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.17-1
- 1.24.17

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 1.24.10-2
- Rebuilt for Python 3.11

* Thu Jun 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.10-1
- 1.24.10

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.24.4-2
- Rebuilt for Python 3.11

* Wed Jun 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.4-1
- 1.24.4

* Tue Jun 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.3-1
- 1.24.3

* Fri Jun 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.2-1
- 1.24.2

* Thu Jun 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.1-1
- 1.24.1

* Wed Jun 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.24.0-1
- 1.24.0

* Fri May 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.10-1
- 1.23.10

* Thu May 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.9-1
- 1.23.9

* Wed May 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.8-1
- 1.23.8

* Tue May 24 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.7-1
- 1.23.7

* Mon May 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.6-1
- 1.23.6

* Mon May 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.5-1
- 1.23.5

* Thu May 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.4-1
- 1.23.4

* Thu May 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.3-1
- 1.23.3

* Tue May 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.2-1
- 1.23.2

* Mon May 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.1-1
- 1.23.1

* Fri May 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23.0-1
- 1.23.0

* Thu May 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.13-1
- 1.22.13

* Wed May 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.12-1
- 1.22.12

* Wed May 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.11-1
- 1.22.11

* Mon May 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.10-1
- 1.22.10

* Thu May 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.8-1
- 1.22.8

* Wed May 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.7-1
- 1.22.7

* Mon May 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.5-1
- 1.22.5

* Fri Apr 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.4-1
- 1.22.4

* Fri Apr 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.3-1
- 1.22.3

* Wed Apr 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.2-1
- 1.22.2

* Tue Apr 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.1-1
- 1.22.1

* Mon Apr 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.22.0-1
- 1.22.0

* Fri Apr 22 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.46-1
- 1.21.46

* Thu Apr 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.45-1
- 1.21.45

* Thu Apr 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.44-1
- 1.21.44

* Tue Apr 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.43-1
- 1.21.43

* Fri Apr 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.42-1
- 1.21.42

* Thu Apr 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.41-1
- 1.21.41

* Wed Apr 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.40-1
- 1.21.40

* Wed Apr 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.39-1
- 1.21.39

* Mon Apr 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.38-1
- 1.21.38

* Fri Apr 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.37-1
- 1.21.37

* Thu Apr 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.36-1
- 1.21.36

* Wed Apr 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.35-1
- 1.21.35

* Tue Apr 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.34-1
- 1.21.34

* Mon Apr 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.33-1
- 1.21.33

* Fri Mar 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.27-1
- 1.21.27

* Thu Mar 24 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.26-1
- 1.21.26

* Wed Mar 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.25-1
- 1.21.25

* Tue Mar 22 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.24-1
- 1.21.24

* Mon Mar 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.23-1
- 1.21.23

* Fri Mar 18 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.22-1
- 1.21.22

* Thu Mar 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.21-1
- 1.21.21

* Wed Mar 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.20-1
- 1.21.20

* Mon Mar 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.19-1
- 1.21.19

* Fri Mar 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.18-1
- 1.21.18

* Fri Mar 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.17-1
- 1.21.17

* Wed Mar 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.16-1
- 1.21.16

* Tue Mar 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.15-1
- 1.21.15

* Tue Mar 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.14-1
- 1.21.14

* Mon Mar 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.13-1
- 1.21.13

* Fri Mar 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.12-1
- 1.21.12

* Thu Mar 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.11-1
- 1.21.11

* Fri Feb 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.8-1
- 1.21.8

* Thu Feb 24 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.7-1
- 1.21.7

* Wed Feb 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.6-1
- 1.21.6

* Wed Feb 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.5-1
- 1.21.5

* Thu Feb 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.2-1
- 1.21.2

* Wed Feb 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.1-1
- 1.21.1

* Tue Feb 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.21.0-1
- 1.21.0

* Fri Feb 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.54-1
- 1.20.54

* Thu Feb 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.53-1
- 1.20.53

* Wed Feb 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.52-1
- 1.20.52

* Tue Feb 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.51-1
- 1.20.51

* Tue Feb 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.50-1
- 1.20.50

* Mon Feb 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.49-1
- 1.20.49

* Thu Feb 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.48-1
- 1.20.48

* Thu Feb 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.47-1
- 1.20.47

* Fri Jan 28 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.46-1
- 1.20.46

* Thu Jan 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.45-1
- 1.20.45

* Tue Jan 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.42-1
- 1.20.42

* Mon Jan 24 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.41-1
- 1.20.41

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 20 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.40-1
- 1.20.40

* Wed Jan 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.39-1
- 1.20.39

* Tue Jan 18 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.38-1
- 1.20.38

* Tue Jan 18 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.37-1
- 1.20.37

* Fri Jan 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.36-1
- 1.20.36

* Thu Jan 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.35-1
- 1.20.35

* Wed Jan 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.34-1
- 1.20.34

* Tue Jan 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.33-1
- 1.20.33

* Mon Jan 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.32-1
- 1.20.32

* Fri Jan 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.31-1
- 1.20.31

* Thu Jan 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.30-1
- 1.20.30

* Wed Jan 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.29-1
- 1.20.29

* Tue Jan 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.28-1
- 1.20.28

* Tue Jan 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.20.27-1
- 1.20.27

* Tue Dec 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.26-1
- 1.20.26

* Mon Dec 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.25-1
- 1.20.25

* Mon Dec 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.24-1
- 1.20.24

* Thu Dec 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.23-1
- 1.20.23

* Thu Dec 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.22-1
- 1.20.22

* Mon Dec 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.21-1
- 1.20.21

* Fri Dec 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.20-1
- 1.20.20

* Thu Dec 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.19-1
- 1.20.19

* Thu Dec 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.18-1
- 1.20.18

* Wed Dec 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.17-1
- 1.20.17

* Tue Nov 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.16-1
- 1.20.16

* Mon Nov 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.15-1
- 1.20.15

* Tue Nov 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.12-1
- 1.20.12

* Mon Nov 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.11-1
- 1.20.11

* Fri Nov 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.10-1
- 1.20.10

* Thu Nov 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.9-1
- 1.20.9

* Thu Nov 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.8-1
- 1.20.8

* Tue Nov 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.7-1
- 1.20.7

* Mon Nov 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.6-1
- 1.20.6

* Fri Nov 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.5-1
- 1.20.5

* Thu Nov 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.4-1
- 1.20.4

* Wed Nov 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.3-1
- 1.20.3

* Tue Nov 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.2-1
- 1.20.2

* Tue Nov 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.1-1
- 1.20.1

* Mon Nov 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.20.0-1
- 1.20.0

* Fri Nov 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.12-1
- 1.19.12

* Thu Nov 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.11-1
- 1.19.11

* Wed Nov 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.10-1
- 1.19.10

* Tue Nov 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.9-1
- 1.19.9

* Tue Nov 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.8-1
- 1.19.8

* Fri Oct 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.7-1
- 1.19.7

* Thu Oct 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.6-1
- 1.19.6

* Wed Oct 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.5-1
- 1.19.5

* Wed Oct 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.4-1
- 1.19.4

* Tue Oct 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.3-1
- 1.19.3

* Wed Oct 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.0-1
- 1.19.0

* Tue Oct 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.65-1
- 1.18.65

* Tue Oct 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.64-1
- 1.18.64

* Fri Oct 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.63-1
- 1.18.63

* Thu Oct 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.62-1
- 1.18.62

* Wed Oct 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.61-1
- 1.18.61

* Tue Oct 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.60-1
- 1.18.60

* Tue Oct 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.59-1
- 1.18.59

* Fri Oct 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.58-1
- 1.18.58

* Thu Oct 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.57-1
- 1.18.57

* Wed Oct 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.56-1
- 1.18.56

* Wed Oct 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.55-1
- 1.18.55

* Fri Oct 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.53-1
- 1.18.53

* Fri Oct 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.52-1
- 1.18.52

* Thu Sep 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.51-1
- 1.18.51

* Tue Sep 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.50-1
- 1.18.50

* Fri Sep 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.48-1
- 1.18.48

* Thu Sep 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.47-1
- 1.18.47

* Wed Sep 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.46-1
- 1.18.46

* Tue Sep 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.45-1
- 1.18.45

* Fri Sep 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.44-1
- 1.18.44

* Thu Sep 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.43-1
- 1.18.43

* Tue Sep 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.42-1
- 1.18.42

* Mon Sep 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.41-1
- 1.18.41

* Mon Sep 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.40-1
- 1.18.40

* Thu Sep 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.39-1
- 1.18.39

* Wed Sep 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.38-1
- 1.18.38

* Wed Sep 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.37-1
- 1.18.37

* Fri Sep 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.36-1
- 1.18.36

* Thu Sep 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.35-1
- 1.18.35

* Thu Sep 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.34-1
- 1.18.34

* Thu Sep 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.32-1
- 1.18.32

* Sat Aug 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.31-1
- 1.18.31

* Thu Aug 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.30-1
- 1.18.30

* Wed Aug 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.29-1
- 1.18.29

* Tue Aug 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.28-1
- 1.18.28

* Mon Aug 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.27-1
- 1.18.27

* Fri Aug 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.26-1
- 1.18.26

* Thu Aug 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.25-1
- 1.18.25

* Wed Aug 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.24-1
- 1.18.24

* Tue Aug 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.23-1
- 1.18.23

* Mon Aug 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.22-1
- 1.18.22

* Fri Aug 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.21-1
- 1.18.21

* Thu Aug 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.20-1
- 1.18.20

* Wed Aug 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.19-1
- 1.18.19

* Tue Aug 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.18-1
- 1.18.18

* Mon Aug 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.17-1
- 1.18.17

* Fri Aug 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.16-1
- 1.18.16

* Thu Aug 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.15-1
- 1.18.15

* Wed Aug 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.14-1
- 1.18.14

* Tue Aug 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.13-1
- 1.18.13

* Mon Aug 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.12-1
- 1.18.12

* Fri Jul 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.11-1
- 1.18.11

* Thu Jul 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.10-1
- 1.18.10

* Wed Jul 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.9-1
- 1.18.9

* Tue Jul 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.8-1
- 1.18.8

* Tue Jul 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.7-1
- 1.18.7

* Fri Jul 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.6-1
- 1.18.6

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.5-1
- 1.18.5

* Wed Jul 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.4-1
- 1.18.4

* Tue Jul 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.3-1
- 1.18.3

* Mon Jul 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.2-1
- 1.18.2

* Fri Jul 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.1-1
- 1.18.1

* Thu Jul 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.18.0-1
- 1.18.0

* Wed Jul 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.112-1
- 1.17.112

* Tue Jul 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.111-1
- 1.17.111

* Mon Jul 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.110-1
- 1.17.110

* Fri Jul 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.109-1
- 1.17.109

* Thu Jul 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.108-1
- 1.17.108

* Wed Jul 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.107-1
- 1.17.107

* Tue Jul 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.106-1
- 1.17.106

* Fri Jul 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.105-1
- 1.17.105

* Thu Jul 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.104-1
- 1.17.104

* Wed Jun 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.103-1
- 1.17.103

* Mon Jun 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.102-1
- 1.17.102

* Fri Jun 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.101-1
- 1.17.101

* Thu Jun 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.100-1
- 1.17.100

* Wed Jun 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.99-1
- 1.17.99

* Mon Jun 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.98-1
- 1.17.98

* Thu Jun 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.97-1
- 1.17.97

* Wed Jun 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.96-1
- 1.17.96

* Tue Jun 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.95-1
- 1.17.95

* Mon Jun 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.94-1
- 1.17.94

* Fri Jun 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.93-1
- 1.17.93

* Thu Jun 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.92-1
- 1.17.92

* Wed Jun 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.91-1
- 1.17.91

* Tue Jun 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.90-1
- 1.17.90

* Tue Jun 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.89-2
- rebuilt

* Mon Jun 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.89-1
- 1.17.89

* Mon Jun 07 2021 Python Maint <python-maint@redhat.com> - 1.17.88-2
- Rebuilt for Python 3.10

* Fri Jun 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.88-1
- 1.17.88

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.17.87-2
- Rebuilt for Python 3.10

* Thu Jun 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.87-1
- 1.17.87

* Wed Jun 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.86-1
- 1.17.86

* Tue Jun 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.85-1
- 1.17.85

* Fri May 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.84-1
- 1.17.84

* Thu May 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.83-1
- 1.17.83

* Thu May 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.82-1
- 1.17.82

* Wed May 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.81-1
- 1.17.81

* Tue May 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.80-1
- 1.17.80

* Tue May 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.79-1
- 1.17.79

* Fri May 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.78-1
- 1.17.78

* Thu May 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.77-1
- 1.17.77

* Wed May 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.76-1
- 1.17.76

* Wed May 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.75-1
- 1.17.75

* Mon May 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.74-1
- 1.17.74

* Fri May 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.73-1
- 1.17.73

* Fri May 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.72-1
- 1.17.72

* Tue May 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.71-1
- 1.17.71

* Mon May 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.70-1
- 1.17.70

* Fri May 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.69-1
- 1.17.69

* Thu May 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.68-1
- 1.17.68

* Wed May 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.67-1
- 1.17.67

* Wed May 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.66-1
- 1.17.66

* Tue May 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.65-1
- 1.17.65

* Tue May 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.64-1
- 1.17.64

* Mon May 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.63-1
- 1.17.63

* Fri Apr 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.62-1
- 1.17.62

* Thu Apr 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.61-1
- 1.17.61

* Wed Apr 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.60-1
- 1.17.60

* Tue Apr 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.59-1
- 1.17.59

* Tue Apr 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.58-1
- 1.17.58

* Fri Apr 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.57-1
- 1.17.57

* Thu Apr 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.56-1
- 1.17.56

* Thu Apr 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.55-1
- 1.17.55

* Mon Apr 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.54-1
- 1.17.54

* Thu Apr 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.53-1
- 1.17.53

* Thu Apr 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.52-1
- 1.17.52

* Tue Apr 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.51-1
- 1.17.51

* Mon Apr 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.50-1
- 1.17.50

* Fri Apr 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.49-1
- 1.17.49

* Fri Apr 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.48-1
- 1.17.48

* Wed Apr 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.47-1
- 1.17.47

* Wed Apr 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.46-1
- 1.17.46

* Mon Apr 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.45-1
- 1.17.45

* Mon Apr 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.44-1
- 1.17.44

* Thu Apr 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.43-1
- 1.17.43

* Thu Apr 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.42-1
- 1.17.42

* Wed Mar 31 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.41-1
- 1.17.41

* Tue Mar 30 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.40-1
- 1.17.40

* Mon Mar 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.39-1
- 1.17.39

* Fri Mar 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.37-1
- 1.17.37

* Thu Mar 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.36-1
- 1.17.36

* Wed Mar 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.35-1
- 1.17.35

* Tue Mar 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.34-1
- 1.17.34

* Mon Mar 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.33-1
- 1.17.33

* Thu Mar 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.31-1
- 1.17.31

* Thu Mar 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.30-1
- 1.17.30

* Wed Mar 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.29-1
- 1.17.29

* Tue Mar 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.28-1
- 1.17.28

* Mon Mar 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.27-1
- 1.17.27

* Fri Mar 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.26-1
- 1.17.26

* Thu Mar 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.25-1
- 1.17.25

* Wed Mar 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.24-1
- 1.17.24

* Tue Mar 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.23-1
- 1.17.23

* Mon Mar 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.22-1
- 1.17.22

* Fri Mar 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.21-1
- 1.17.21

* Thu Mar 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.20-1
- 1.17.20

* Wed Mar 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.19-1
- 1.17.19

* Tue Mar 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.18-1
- 1.17.18

* Mon Mar 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.17-1
- 1.17.17

* Fri Feb 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.16-1
- 1.17.16

* Thu Feb 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.15-1
- 1.17.15

* Wed Feb 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.14-1
- 1.17.14

* Tue Feb 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.13-1
- 1.17.13

* Sat Feb 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.12-1
- 1.17.12

* Fri Feb 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.11-1
- 1.17.11

* Thu Feb 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.10-1
- 1.17.10

* Wed Feb 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.9-1
- 1.17.9

* Tue Feb 16 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.8-1
- 1.17.8

* Fri Feb 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.6-1
- 1.17.6

* Wed Feb 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.5-1
- 1.17.5

* Tue Feb 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.4-1
- 1.17.4

* Fri Feb 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.3-1
- 1.17.3

* Fri Feb 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.2-1
- 1.17.2

* Wed Feb 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.17.0-1
- 1.17.0

* Mon Feb 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.63-1
- 1.16.63

* Fri Jan 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.62-1
- 1.16.62

* Thu Jan 28 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.61-1
- 1.16.61

* Wed Jan 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.60-1
- 1.16.60

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.59-1
- 1.16.59

* Fri Jan 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.58-1
- 1.16.58

* Wed Jan 20 08:21:03 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.57-1
- 1.16.57

* Tue Jan 19 08:28:49 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.56-1
- 1.16.56

* Fri Jan 15 10:49:14 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.55-1
- 1.16.55

* Thu Jan 14 08:20:12 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.54-1
- 1.16.54

* Wed Jan 13 08:36:31 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.53-1
- 1.16.53

* Tue Jan 12 08:19:50 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.52-1
- 1.16.52

* Fri Jan  8 10:52:57 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.51-1
- 1.16.51

* Thu Jan  7 08:33:04 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.50-1
- 1.16.50

* Wed Jan  6 08:15:36 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.49-1
- 1.16.49

* Tue Jan  5 08:32:30 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.48-1
- 1.16.48

* Mon Jan  4 08:33:46 CST 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.16.47-1
- 1.16.47

* Wed Dec 30 16:21:43 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.46-1
- 1.16.46

* Wed Dec 30 08:33:40 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.45-1
- 1.16.45

* Tue Dec 29 09:15:14 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.44-1
- 1.16.44

* Thu Dec 24 08:35:52 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.43-1
- 1.16.43

* Wed Dec 23 08:40:18 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.42-1
- 1.16.42

* Tue Dec 22 08:28:41 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.41-1
- 1.16.41

* Fri Dec 18 16:33:01 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.40-1
- 1.16.40

* Fri Dec 18 08:27:56 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.39-1
- 1.16.39

* Thu Dec 17 08:16:39 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.38-1
- 1.16.38

* Wed Dec 16 08:23:45 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.37-1
- 1.16.37

* Tue Dec 15 08:31:33 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.36-1
- 1.16.36

* Mon Dec 14 09:20:28 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.35-1
- 1.16.35

* Fri Dec 11 08:13:23 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.34-1
- 1.16.34

* Thu Dec 10 08:24:55 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.33-1
- 1.16.33

* Wed Dec  9 08:54:55 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.32-1
- 1.16.32

* Tue Dec  8 08:24:27 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.31-1
- 1.16.31

* Mon Dec  7 08:27:14 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.30-1
- 1.16.30

* Fri Dec  4 10:07:40 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.29-1
- 1.16.29

* Wed Dec  2 08:26:03 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.28-1
- 1.16.28

* Tue Dec  1 11:51:40 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.26-1
- 1.16.26

* Mon Nov 30 09:20:03 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.25-1
- 1.16.25

* Tue Nov 24 08:25:36 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.24-1
- 1.16.24

* Mon Nov 23 08:26:26 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.23-1
- 1.16.23

* Fri Nov 20 08:15:00 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.22-1
- 1.16.22

* Thu Nov 19 08:27:37 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.21-1
- 1.16.21

* Wed Nov 18 08:23:10 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.20-1
- 1.16.20

* Tue Nov 17 09:16:39 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.19-1
- 1.16.19

* Mon Nov 16 08:35:57 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.18-1
- 1.16.18

* Thu Nov 12 15:47:25 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.17-1
- 1.16.17

* Thu Nov 12 10:26:50 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.16-1
- 1.16.16

* Wed Nov 11 09:22:58 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.15-1
- 1.16.15

* Mon Nov  9 14:12:50 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.14-1
- 1.16.14

* Mon Nov  9 09:43:37 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.13-1
- 1.16.13

* Fri Nov  6 08:25:16 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.12-1
- 1.16.12

* Thu Nov  5 14:59:57 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.11-1
- 1.16.11

* Tue Nov  3 08:31:00 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.10-1
- 1.16.10

* Mon Nov  2 09:27:02 CST 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.9-1
- 1.16.9

* Fri Oct 30 08:13:44 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.8-1
- 1.16.8

* Thu Oct 29 08:11:35 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.7-1
- 1.16.7

* Wed Oct 28 09:47:49 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.6-1
- 1.16.6

* Tue Oct 27 09:39:05 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.5-1
- 1.16.5

* Fri Oct 23 16:47:32 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.4-1
- 1.16.4

* Fri Oct 23 08:13:24 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.3-1
- 1.16.3

* Thu Oct 22 08:29:33 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.2-1
- 1.16.2

* Tue Oct 20 21:06:52 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.1-1
- 1.16.1

* Tue Oct 20 08:10:45 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.16.0-1
- 1.16.0

* Fri Oct 16 14:55:28 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.18-1
- 1.15.18

* Fri Oct 16 08:09:57 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.17-1
- 1.15.17

* Sat Oct 10 16:04:24 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.16-1
- 1.15.16

* Thu Oct  8 14:31:50 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.15-1
- 1.15.15

* Thu Oct  8 09:00:53 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.14-1
- 1.15.14

* Wed Oct  7 08:56:59 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.13-1
- 1.15.13

* Fri Oct  2 15:35:15 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.11-1
- 1.15.11

* Fri Oct  2 08:20:02 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.10-1
- 1.15.10

* Thu Oct  1 08:15:53 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.9-1
- 1.15.9

* Wed Sep 30 09:04:06 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.8-1
- 1.15.8

* Tue Sep 29 09:14:56 CDT 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.7-1
- 1.15.7

* Mon Sep 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.6-1
- 1.15.6

* Fri Sep 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.5-1
- 1.15.5

* Wed Sep 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.4-1
- 1.15.4

* Wed Sep 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.3-1
- 1.15.3

* Mon Sep 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.2-1
- 1.15.2

* Fri Sep 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.1-1
- 1.15.1

* Fri Sep 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.15.0-1
- 1.15.0

* Wed Sep 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.63-1
- 1.14.63

* Tue Sep 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.62-1
- 1.14.62

* Tue Sep 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.61-1
- 1.14.61

* Mon Sep 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.60-1
- 1.14.60

* Fri Sep 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.59-1
- 1.14.59

* Thu Sep 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.58-1
- 1.14.58

* Wed Sep 09 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.57-1
- 1.14.57

* Tue Sep 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.56-1
- 1.14.56

* Fri Sep 04 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.55-1
- 1.14.55

* Wed Sep 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.54-1
- 1.14.54

* Wed Sep 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.53-1
- 1.14.53

* Tue Sep 01 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.52-1
- 1.14.52

* Mon Aug 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.51-1
- 1.14.51

* Fri Aug 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.50-1
- 1.14.50

* Thu Aug 27 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.49-1
- 1.14.49

* Tue Aug 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.48-1
- 1.14.48

* Fri Aug 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.47-1
- 1.14.47

* Wed Aug 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.46-1
- 1.14.46

* Wed Aug 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.45-1
- 1.14.45

* Tue Aug 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.44-1
- 1.14.44

* Mon Aug 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.43-1
- 1.14.43

* Fri Aug 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.42-1
- 1.14.42

* Thu Aug 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.41-1
- 1.14.41

* Wed Aug 12 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.40-1
- 1.14.40

* Tue Aug 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.39-1
- 1.14.39

* Mon Aug 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.38-1
- 1.14.38

* Thu Aug 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.37-1
- 1.14.37

* Thu Aug 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.36-1
- 1.14.36

* Wed Aug 05 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.35-1
- 1.14.35

* Tue Aug 04 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.34-1
- 1.14.34

* Fri Jul 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.33-1
- 1.14.33

* Fri Jul 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.32-1
- 1.14.32

* Thu Jul 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.31-1
- 1.14.31

* Wed Jul 29 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.30-1
- 1.14.30

* Tue Jul 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.29-1
- 1.14.29

* Fri Jul 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.28-1
- 1.14.28

* Fri Jul 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.27-1
- 1.14.27

* Thu Jul 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.26-1
- 1.14.26

* Wed Jul 22 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.25-1
- 1.14.25

* Tue Jul 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.24-1
- 1.14.24

* Mon Jul 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.23-1
- 1.14.23

* Fri Jul 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.22-1
- 1.14.22

* Thu Jul 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.21-1
- 1.14.21

* Fri Jul 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.20-1
- 1.14.20

* Thu Jul 09 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.19-1
- 1.14.19

* Wed Jul 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.18-1
- 1.14.18

* Tue Jul 07 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.17-1
- 1.14.17

* Fri Jul 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.16-1
- 1.14.16

* Thu Jul 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.15-1
- 1.14.15

* Wed Jul 01 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.14-1
- 1.14.14

* Tue Jun 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.13-1
- 1.14.13

* Sat Jun 27 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.12-1
- 1.14.12

* Fri Jun 26 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.11-1
- 1.14.11

* Thu Jun 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.10-1
- 1.14.10

* Wed Jun 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.9-1
- 1.14.9

* Tue Jun 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.8-1
- 1.14.8

* Mon Jun 22 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.7-1
- 1.14.7

* Fri Jun 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.6-1
- 1.14.6

* Thu Jun 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.5-1
- 1.14.5

* Wed Jun 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.4-1
- 1.14.4

* Tue Jun 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.3-1
- 1.14.3

* Sat Jun 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.2-1
- 1.14.2

* Thu Jun 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.1-1
- 1.14.1

* Thu Jun 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.14.0-1
- 1.14.0

* Sat Jun 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.24-1
- 1.13.24

* Fri Jun 05 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.23-1
- 1.13.23

* Thu Jun 04 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.22-1
- 1.13.22

* Tue Jun 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.20-1
- 1.13.20

* Sun May 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.19-1
- 1.13.19

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.13.16-2
- Rebuilt for Python 3.9

* Fri May 22 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.16-1
- 1.13.16

* Thu May 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.15-1
- 1.13.15

* Wed May 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.14-1
- 1.13.14

* Mon May 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.11-1
- 1.13.11

* Thu May 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.10-1
- 1.13.10

* Thu May 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.9-1
- 1.13.9

* Wed May 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.8-1
- 1.13.8

* Tue May 12 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.7-1
- 1.13.7

* Fri May 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.6-1
- 1.13.6

* Fri May 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.5-1
- 1.13.5

* Thu May 07 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.4-1
- 1.13.4

* Wed May 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.3-1
- 1.13.3

* Tue May 05 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.2-1
- 1.13.2

* Sat May 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.1-1
- 1.13.1

* Fri May 01 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.13.0-1
- 1.13.0

* Thu Apr 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.49-1
- 1.12.49

* Wed Apr 29 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.48-1
- 1.12.48

* Tue Apr 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.47-1
- 1.12.47

* Sat Apr 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.46-1
- 1.12.46

* Thu Apr 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.45-1
- 1.12.45

* Thu Apr 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.44-1
- 1.12.44

* Wed Apr 22 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.43-1
- 1.12.43

* Mon Apr 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.42-1
- 1.12.42

* Sun Apr 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.41-1
- 1.12.41

* Fri Apr 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.40-1
- 1.12.40

* Thu Apr 09 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.39-1
- 1.12.39

* Wed Apr 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.38-1
- 1.12.38

* Tue Apr 07 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.37-1
- 1.12.37

* Mon Apr 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.36-1
- 1.12.36

* Fri Apr 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.35-1
- 1.12.35

* Wed Apr 01 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.34-1
- 1.12.34

* Wed Apr 01 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.33-1
- 1.12.33

* Mon Mar 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.32-1
- 1.12.32

* Fri Mar 27 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.31-1
- 1.12.31

* Fri Mar 27 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.30-1
- 1.12.30

* Wed Mar 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.29-1
- 1.12.29

* Wed Mar 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.28-1
- 1.12.28

* Tue Mar 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.27-1
- 1.12.27

* Sat Mar 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.26-1
- 1.12.26

* Fri Mar 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.25-1
- 1.12.25

* Thu Mar 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.24-1
- 1.12.24

* Wed Mar 18 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.23-1
- 1.12.23

* Mon Mar 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.22-1
- 1.12.22

* Mon Mar 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.21-1
- 1.12.21

* Fri Mar 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.20-1
- 1.12.20

* Thu Mar 12 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.19-1
- 1.12.19

* Wed Mar 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.18-1
- 1.12.18

* Tue Mar 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.17-1
- 1.12.17

* Sun Mar 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.16-1
- 1.12.16

* Fri Mar 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.15-1
- 1.12.15

* Thu Mar 05 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.14-1
- 1.12.14

* Wed Mar 04 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.13-1
- 1 12.13

* Tue Mar 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.12-1
- 1.12.12

* Fri Feb 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.9-1
- 1.12.9

* Thu Feb 27 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.12.8-1
- Update to 1.12.8

* Wed Feb 26 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.7-1
- 1.12.7

* Mon Feb 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.6-1
- 1.12.6

* Mon Feb 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.5-1
- 1.12.5

* Fri Feb 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.4-1
- 1.12.4

* Thu Feb 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.3-1
- 1.12.3

* Wed Feb 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.11.17-1
- 1.11.17

* Fri Feb 07 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.11.12-1
- Update to 1.11.12

* Wed Jan 29 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.11.9-1
- Update to 1.11.9

* Fri Jan 17 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.11.4-1
- Update to 1.11.4 (rhbz#1677949)

* Mon Jan 13 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.11.0-1
- Update to 1.11.0 (rhbz#1677949)

* Wed Nov 20 2019 Orion Poplawski <orion@nwra.com> - 1.10.22-1
- Update to 1.10.21

* Mon Sep 09 2019 Charalampos Stratakis <cstratak@redhat.com> - 1.9.225-1
- Update to 1.9.225 (rhbz#1677949)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.101-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 23 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.101-1
- Update to 1.9.101

* Fri Feb 15 2019 Kevin Fenzi <kevin@scrye.com> - 1.9.96-1
- Update to 1.9.96. Fixes bug #1667629

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.15-3
- Enable python dependency generator

* Thu Dec 20 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.15-2
- Subpackage python2-boto3 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Oct 02 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.9.15-1
- Update to 1.9.15

* Wed Jul 18 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.7.41-1
- Upstream 1.7.41 (Fix compat with botocore 1.10.41)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.6.1-3
- Rebuilt for Python 3.7

* Tue Mar 13 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.6.1-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 28 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.6.1-1
- Update to 1.6.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.5.19-1
- Update to 1.5.19

* Sat Jan 20 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.5.18-1
- Update to 1.5.18

* Tue Jan 16 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.5.15-1
- Update to 1.5.15

* Wed Jan 10 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.5.12-1
- Update to 1.5.12

* Wed Jan 03 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.5.7-1
- Update to 1.5.7

* Sun Aug 13 2017 Fabio Alessandro Locati <fale@fedoraproject.org> 1.4.6-1
- Update to 1.4.6

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Fabio Alessandro Locati <fale@fedoraproject.org> 1.4.4-1
- Update to 1.4.4

* Wed Dec 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> 1.4.3-1
- Update to 1.4.3

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.4.2-2
- Rebuild for Python 3.6

* Sat Dec 03 2016 Fabio Alessandro Locati <fale@fedoraproject.org> 1.4.2-1
- Update to 1.4.2

* Mon Oct 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1

* Thu Aug 04 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.0-1
- New upstream release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat May 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.1-1
- New upstream release

* Tue Mar 29 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.0-1
- New upstream release

* Fri Feb 19 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.2.4-1
- New upstream release

* Thu Feb 11 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.2.3-3
- Fix python2- subpackage to require python-future

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 29 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.2.3-1
- Initial package.
