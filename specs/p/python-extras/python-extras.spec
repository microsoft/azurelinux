# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond bootstrap 0

Name:           python-extras
Version:        1.0.0
Release:        42%{?dist}
Summary:        Useful extra bits for Python

License:        MIT
URL:            https://github.com/testing-cabal/extras
Source:         %{pypi_source extras}

BuildArch:      noarch

%global _description %{expand:
extras is a set of extensions to the Python standard library, originally
written to make the code within testtools cleaner, but now split out for
general use outside of a testing context.}


%description %_description


%package -n python3-extras
Summary:        %{summary}
BuildRequires:  python3-devel
%if %{without bootstrap}
BuildRequires:  python3-testtools
%endif


%description -n python3-extras %_description


%prep
%setup -q -n extras-%{version}
# don't include extras.tests
sed -e '/extras\.tests/d' -i setup.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l extras


%check
%if %{with bootstrap}
%pyproject_check_import
%else
%{py3_test_envvars} %{python3} -m testtools.run extras.tests.test_suite
%endif


%files -n python3-extras -f %{pyproject_files}
%doc NEWS README.rst


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.0-42
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.0-41
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.0.0-39
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.0.0-38
- Bootstrap for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 13 2024 Carl George <carlwgeorge@fedoraproject.org> - 1.0.0-36
- Run tests with testtools instead of pytest
- Run import check while bootstrapping

* Fri Aug 30 2024 Jan Friesse <jfriesse@redhat.com> - 1.0.0-36
- migrated to SPDX license

* Mon Jul 29 2024 Michel Lind <salimma@fedoraproject.org> - 1.0.0-35
- Switch to pytest for running tests (rhbz#2259522)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.0-33
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.0-32
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 1.0.0-28
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.0.0-27
- Bootstrap for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 1.0.0-24
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.0-23
- Bootstrap for Python 3.11

* Fri Apr 29 2022 Carl George <carl@george.computer> - 1.0.0-22
- Switch to bootstrap macros

* Fri Apr 29 2022 Carl George <carl@george.computer> - 1.0.0-21
- Disable tests for EPEL9 bootstrap

* Sat Apr 23 2022 Carl George <carl@george.computer> - 1.0.0-20
- Convert to pyproject macros

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-18
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.0-17
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.0.0-16
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-13
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-12
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-10
- Subpackage python2-extras has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-9
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-8
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-4
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-3
- Bootstrap for Python 3.7

* Tue Feb  6 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.0.0-2
- Fix build on EL7

* Sat Sep  2 2017 Jan Beran <jberan@redhat.com> - 1.0.0-1
- New version

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.0.3-17
- Python 2 binary package renamed to python2-extras
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.0.3-14
- Enable tests

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.0.3-13
- Rebuild for Python 3.6
- Disable tests

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-12
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 0.0.3-10
- And now re-enable

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 0.0.3-9
- Temporarily disable tests to bootstrap past a dep loop

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.3-5
- Enable tests again.

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
- Bootstrap tests to break circular dependency with python-testtools

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 29 2013 Matthias Runge <mrunge@redhat.com> - 0.0.3-2
- spec cleanup and enable tests

* Wed May  1 2013 Michel Salim <salimma@fedoraproject.org> - 0.0.3-1
- Initial package
