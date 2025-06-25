# Upstream does not tag releases on GitHub (and did not upload a source archive
# to PyPI for version 1.9).
%global commit ba89b41638df8ad2011c2818672f208a91a5a4a0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global snapdate 20200222

Name:           python-junit_xml
Summary:        Python module for creating JUnit XML test result documents
Version:        1.9^%{snapdate}git%{shortcommit}
Release:        21%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

# SPDX
License:        MIT
URL:            https://github.com/kyrus/python-junit-xml
Source:         %{url}/archive/%{commit}/python-junit-xml-%{commit}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-six
BuildRequires:  python3-wheel

%global common_description %{expand:
A Python module for creating JUnit XML test result documents that can be read
by tools such as Jenkins or Bamboo. If you are ever working with test tool or
test suite written in Python and want to take advantage of Jenkins’ or Bamboo’s
pretty graphs and test reporting capabilities, this module will let you
generate the XML test reports.}

%description %{common_description}


%package -n python3-junit-xml
Summary:        %{summary}

# The source package is named python-junit_xml for historical reasons.  The
# binary package, python3-junit-xml, is named using the canonical project
# name[1]; see also [2].
#
# The %%py_provides macro is used to provide an upgrade path from
# python3-junit_xml and to produce the appropriate Provides for the importable
# module[3].
#
# [1] https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_canonical_project_name
# [2] https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_library_naming
# [3] https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules

# Provide an upgrade path
%py_provides python3-junit_xml
Obsoletes:      python3-junit_xml < 1.9^20200222gitba89b41-8

%description -n python3-junit-xml %{common_description}


%prep
%autosetup -n python-junit-xml-%{commit}
# Remove shebang line in non-script source
sed -r -i '1{/^#!/d}' junit_xml/__init__.py
# Do not require pytest-sugar for testing; it is only for prettier output.
sed -r -i 's/^([[:blank:]]+)(pytest-sugar)/\1# \2/' tox.ini


%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files junit_xml


%check
# Manually use 'rpm' to remove the 'python3-packaging' package:
rpm -e python3-packaging --nodeps

# Freezing 'pytest' to a known working version as updates tend to introduce regressions.
pip3 install pytest==7.4.3 tox tox-current-env virtualenv
%tox


%files -n python3-junit-xml -f %{pyproject_files}
%doc README.rst


%changelog
* Wed Jun 25 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9^20200222gitba89b41-21
- Initial CBL-Mariner import from Fedora 42 (license: MIT).
- License verified.

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9^20200222gitba89b41-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Aug 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9^20200222gitba89b41-19
- Do not require pytest-sugar for testing; it is only for prettier output

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9^20200222gitba89b41-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.9^20200222gitba89b41-17
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9^20200222gitba89b41-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9^20200222gitba89b41-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9^20200222gitba89b41-13
- Assert that %%pyproject_files contains a license file

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9^20200222gitba89b41-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.9^20200222gitba89b41-11
- Rebuilt for Python 3.12

* Thu May 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9^20200222gitba89b41-10
- Rename the binary RPM to match the canonical name

* Thu May 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9^20200222gitba89b41-9
- Remove a shebang from a non-script Python source

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9^20200222gitba89b41-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Oct 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9^20200222gitba89b41-4
- Confirm License is SPDX MIT

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9^20200222gitba89b41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.9^20200222gitba89b41-2
- Rebuilt for Python 3.11

* Wed Apr 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9^20200222gitba89b41-1
- Drop “forge” macros and use “modern” snapshot versioning

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 13 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-17
- Let pyproject-rpm-macros handle the license file

* Sun Sep 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-16
- Drop BR on pyproject-rpm-macros, now implied by python3-devel

* Sun Sep 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-15
- Add Python provides for junit-xml name

* Sun Sep 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-14
- Drop BR on pyproject-rpm-macros, now implied by python3-devel

* Tue Jul 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9-13
- Move %%generate_buildrequires after %%prep to make the spec file easier
  to follow

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-12
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

## END: Generated by rpmautospec
