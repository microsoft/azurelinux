# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name ldap3

Name:           python-%{pypi_name}
Version:        2.9.1
Release: 16%{?dist}
Summary:        Strictly RFC 4511 conforming LDAP V3 pure Python client

License:        LGPL-3.0-or-later
URL:            https://github.com/cannatag/ldap3
# The PyPI tarball is missing several files needed for running the test suite.
Source:         %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%global _description \
ldap3 is a strictly RFC 4510 conforming LDAP V3 pure Python client library.

%description %{_description}

%package     -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
# Needed for the import check of ldap3.protocol.sasl.kerberos
BuildRequires:  python3-gssapi

%description -n python3-%{pypi_name} %{_description}

Python 3 version.

%prep
%autosetup -n %{pypi_name}-%{version} -p1

# Remove bundled ordereddict, which was only needed on Python < 2.7 anyways.
rm -vf %{pypi_name}/utils/ordDict.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}

%check
# The upstream test coverage isn't great, so we are going to do both an import
# check and run what tests we can.
%pyproject_check_import
SERVER='NONE' %{py3_test_envvars} %{python3} -m unittest discover -s test

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.9.1-15
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.9.1-14
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.9.1-12
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 10 2024 Carl George <carlwgeorge@fedoraproject.org> - 2.9.1-10
- Update license tag to LGPL-3.0-or-later
- Remove duplicate COPYING.LESSER.txt license file
- Run an import check and the upstream test suite in %%check

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 2.9.1-9
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.9.1-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.9.1-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 02 2022 Maíra Canal <mairacanal@riseup.net> - 2.9.1-1
- Update to 2.9.1
- Remove deprecated macros
  See https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_deprecated_macros

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.8.1-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.8.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 15 2020 Avram Lubkin <aviso@rockhopper.net> - 2.8.1-1
- Update to 2.8.1

* Sat Jun 20 2020 Avram Lubkin <aviso@rockhopper.net> - 2.7-1
- Update to 2.7

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 20 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-2
- Subpackage python2-ldap3 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Oct 08 2019 Avram Lubkin <aviso@rockhopper.net> - 2.6.1-1
- Update to 2.6.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 09 2019 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-7
- Readd pythno2-ldap3 (#1672052)

* Mon Feb 25 2019 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-6
- Subpackage python2-ldap3 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 26 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.1-4
- Enable python dependency generator

* Mon Dec 17 2018 Avram Lubkin <aviso@rockhopper.net> - 2.5.1-3
- Fix El6 requirements

* Sun Dec 16 2018 Avram Lubkin <aviso@rockhopper.net> - 2.5.1-2
- python-backports-ssl_match_hostname only required for Python 2.6

* Mon Nov 12 2018 Avram Lubkin <aviso@rockhopper.net> - 2.5.1-1
- Update to 2.5.1
- Build Python 3 packages for EPEL

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5-2
- Rebuilt for Python 3.7

* Mon Apr 16 2018 Michal Cyprian <mcyprian@redhat.com> - 2.5-1
- Update to 2.5

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Igor Gnatenko <ignatenko@redhat.com> - 2.4.1-1
- Update to 2.4.1

* Thu Nov 16 2017 Michal Cyprian <mcyprian@redhat.com> - 2.4-1
- Update to 2.4

* Tue Oct 24 2017 Michal Cyprian <mcyprian@redhat.com> - 2.3-3
- Remove no longer necessary unbundle-ssl patch
Resolves: rhbz#1494151

* Thu Sep 21 2017 Ralph Bean <rbean@redhat.com> - 2.3-2
- Fix patch to require correct backports package name on el7.

* Wed Sep 20 2017 Michal Cyprian <mcyprian@redhat.com> - 2.3-1
- Update to 2.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Michal Cyprian <mcyprian@redhat.com> - 2.2.3-1
- Update to 2.2.3

* Sun Mar 19 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

* Thu Feb 16 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Mon Jan 02 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.1.1-1
- Update to 2.1.1
- Modernize spec

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.8.6-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.6-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Michal Cyprian <mcyprian@redhat.com> - 0.9.8.6-3
- Replace macro define with global

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

 * Wed Jul 08 2015 Michal Cyprian <mcyprian@redhat.com> - 0.9.8.6-1
 - Initial release of RPM package
