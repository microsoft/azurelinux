%global pypi_name junit-xml
%global common_description %{expand:
A Python module for creating JUnit XML test result documents that can be read
by tools such as Jenkins or Bamboo. If you are ever working with test tool or
test suite written in Python and want to take advantage of Jenkins’ or Bamboo’s
pretty graphs and test reporting capabilities, this module will let you
generate the XML test reports.}

Summary:        Python module for creating JUnit XML test result documents
Name:           python-%{pypi_name}
Version:        1.9
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/kyrus/python-junit-xml
Source0:        https://files.pythonhosted.org/packages/source/j/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

%description %{common_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}
Provides:       python3-junit_xml = %{version}-%{release}

%description -n python3-%{pypi_name} %{common_description}

%prep
%autosetup -n %{pypi_name}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files junit_xml

%check
pip3 install tox tox-current-env pytest==7.1.3 virtualenv
%tox

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE.txt
%doc README.rst

%changelog
* Fri Nov 17 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9-1
- Initial CBL-Mariner import from Fedora 38 (license: MIT).
- License verified.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> 1.9^20200222gitba89b41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> 1.9^20200222gitba89b41-2
- Rebuilt for Python 3.11

* Wed Apr 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> 1.9^20200222gitba89b41-1
- Drop “forge” macros and use “modern” snapshot versioning

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> 1.9-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 13 2021 Benjamin A. Beasley <code@musicinmybrain.net> 1.9-17
- Let pyproject-rpm-macros handle the license file

* Sun Sep 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> 1.9-16
- Drop BR on pyproject-rpm-macros, now implied by python3-devel

* Sun Sep 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> 1.9-15
- Add Python provides for junit-xml name

* Sun Sep 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> 1.9-14
- Drop BR on pyproject-rpm-macros, now implied by python3-devel

* Tue Jul 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> 1.9-13
- Move %%generate_buildrequires after %%prep to make the spec file easier
  to follow

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> 1.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-9
- Merged PR#1; drop patch for RHBZ#1935212

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.9-8
- Rebuilt for Python 3.10

* Wed May 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-7
- Move “forge” macros to the top of the spec file

* Tue Mar 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-6
- Drop python3dist(setuptools) BR, redundant with %%pyproject_buildrequires

* Mon Mar 08 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-5
- Replace ' with ’ in description

* Thu Feb 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-4
- Rebuilt for pyproject-rpm-macros-0-38 to fix unowned nested __pycache__
  directories (RHBZ#1925963)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-2
- Drop conditionals for Fedora 32

* Thu Jan 14 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-1
- Update to 1.9 (RHBZ#1486729)

* Thu Jan 14 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8-13
- Drop EPEL compatibility and unnecessary macros; EPEL7/8 will be supported by
  a forked spec file instead of conditional macros
- Use pyproject-rpm-macros, including generated BR’s
- Fix banned %%{python3_sitelib}/* in %%files
- Use %%pytest, %%pypi_source macros
- Update summary and description from upstream

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.8-11
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Adrian Reber <adrian@lisas.de> - 1.8-9
- Apply adapted upstream fix for test failures

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8-5
- Subpackage python2-junit_xml has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.8-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 30 2017 James Hogarth <james.hogarth@gmail.com> - 1.8-1
- update to 1.8

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 15 2017 James Hogarth <james.hogarth@gmail.com> - 1.7-1
- Initial package
