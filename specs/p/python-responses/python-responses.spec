# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name responses

Name:           python-%{pypi_name}
Version:        0.25.8
Release: 4%{?dist}
Summary:        Python library to mock out calls with Python requests
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            https://github.com/getsentry/responses
Source:         %{pypi_source}

BuildArch:      noarch
BuildRequires:  python3-devel
# Upstream added various requirements in its "tests" extras which are only
# required tests we don't want to run in Fedora (coverage) and strict version
# requirements (pytest >= 7.0 as of March 2022 - not yet in rawhide).
# Patching setup.py is error prone as the patch file has to be regenerated
# every time upstream bumps a version requirement.
# Therefore just list the build requirements here explicitely.
BuildRequires:  python3-pytest python3-pytest-xdist

%description
A utility library for mocking out the requests Python library.

%package -n python3-%{pypi_name}
Summary:        Python library to mock out calls with Python requests

%description -n python%{python3_pkgversion}-%{pypi_name}
A utility library for mocking out the requests Python library.

%prep
%autosetup -n %{pypi_name}-%{version} -p1

# Remove unnecessary dependencies
sed -i '/coverage/d' setup.py
sed -i '/pytest-cov/d' setup.py
sed -i '/flake8/d' setup.py
sed -i '/types-requests/d' setup.py
sed -i '/mypy/d' setup.py

%generate_buildrequires
%pyproject_buildrequires -r -x tests

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}
# we do not ship tests
sed -i -e '/\/tests\//d' %{pyproject_files}

%check
%pytest -n auto --asyncio-mode=auto

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.25.8-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.25.8-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Sat Aug 09 2025 Felix Schwarz <fschwarz@fedoraproject.org> - 0.25.8-1
- update to 0.25.8

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.25.7-2
- Rebuilt for Python 3.14

* Sun Mar 16 2025 Felix Schwarz <fschwarz@fedoraproject.org> - 0.25.7-1
- update to 0.25.7

* Thu Jan 23 2025 Felix Schwarz <fschwarz@fedoraproject.org> - 0.25.6-1
- update to 0.25.6

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 10 2025 Felix Schwarz <fschwarz@fedoraproject.org> - 0.25.5-1
- update to 0.25.5

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 0.25.3-3
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 16 2024 Felix Schwarz <fschwarz@fedoraproject.org> - 0.25.3-1
- update to 0.25.3

* Wed Jun 12 2024 Felix Schwarz <fschwarz@fedoraproject.org> - 0.25.2-1
- update to 0.25.2

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 0.25.0-2
- Rebuilt for Python 3.13

* Wed Feb 14 2024 Felix Schwarz <fschwarz@fedoraproject.org> - 0.25.0-1
- update to 0.25.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Felix Schwarz <fschwarz@fedoraproject.org> - 0.24.1-1
- update to 0.24.1

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 0.23.1-2
- Rebuilt for Python 3.12

* Sat Mar 11 2023 Felix Schwarz <fschwarz@fedoraproject.org> - 0.23.1-1
- update to 0.23.1

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 29 2022 Miro Hrončok <mhroncok@redhat.com> - 0.22.0-2
- Drop a dependency on deprecated python3-toml
- https://fedoraproject.org/wiki/Changes/DeprecatePythonToml

* Wed Oct 12 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 0.22.0-1
- update to 0.22.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 0.21.0-2
- Rebuilt for Python 3.11

* Sun May 29 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 0.21.0-1
- update to 0.21.0

* Fri Mar 18 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 0.20.0-1
- update to 0.20.0

* Mon Mar 07 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 0.19.0-1
- update to 0.19.0

* Wed Feb 02 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 0.18.0-1
- update to 0.18.0

* Wed Jan 26 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 0.17.0-1
- update to 0.17.0

* Wed Jan 26 2022 Orion Poplawski <orion@nwra.com> - 0.16.0-3
- Do not run coverage tests

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 17 2021 Felix Schwarz <fschwarz@fedoraproject.org> - 0.16.0-1
- Update to 0.16.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.10.15-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 14 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.15-1
- Version update

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.14-2
- Rebuilt for Python 3.9

* Tue May 12 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.14-1
- Version update

* Wed Mar 04 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.12-1
- Version update

* Sat Feb 29 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.10.11-1
- Version update

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.5-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.5-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 0.10.5-1
- Upgrade to 0.10.5 (#1684241).
- https://github.com/getsentry/responses/blob/0.10.5/CHANGES

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.0-5
- Enable python dependency generator

* Fri Dec 28 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-4
- Subpackage python2-responses has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-2
- Rebuilt for Python 3.7

* Mon Apr 09 2018 Athos Ribeiro <athoscr@fedoraproject.org> - 0.9.0-1
- Version update
- Explicitly require pythonX-setuptools regardless of environment

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.1-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.1-7
- Escape macros in %%changelog

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 02 2016 Germano Massullo <germano.massullo@gmail.com> - 0.5.1-2
- Fixed python packages prefix for el <= 7

* Mon Jan 25 2016 Germano Massullo <germano.massullo@gmail.com> - 0.5.1-1
- LICENSE file added in upstream update
- Commented %%check section due test file missing in pypi release. See https://github.com/getsentry/responses/issues/98

* Sat Jan 23 2016 Germano Massullo <germano.massullo@gmail.com> - 0.5.0-1
- Package review submission
