# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name pecan
%{!?_licensedir:%global license %%doc}
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        1.7.0
Release:        4%{?dist}
Summary:        A lean WSGI object-dispatching web framework

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/pecan/pecan
Source0:        %pypi_source
BuildArch:      noarch

%description
A WSGI object-dispatching web framework, designed to be lean and
fast with few dependencies

%package -n python3-%{pypi_name}
Summary:        A lean WSGI object-dispatching web framework

BuildRequires:  python3-devel

Conflicts:     python2-%{pypi_name} < 1.3.2-5

%description -n python3-%{pypi_name}
A WSGI object-dispatching web framework, designed to be lean and
fast with few dependencies

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst
%{_bindir}/pecan
%{_bindir}/gunicorn_pecan

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.7.0-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.7.0-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.7.0-1
- 1.7.0

* Sat Jun 07 2025 Python Maint <python-maint@redhat.com> - 1.6.0-2
- Rebuilt for Python 3.14

* Tue Mar 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.6.0-1
- 1.6.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.5.1-2
- convert license to SPDX

* Thu Aug 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.5.1-1
- 1.5.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.4.2-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.4.2-4
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 06 2022 Ken Dreyer <kdreyer@redhat.com> 1.4.2-1
- Update to 1.4.2 (rhbz#2103406)

* Mon Jun 27 2022 Ken Dreyer <kdreyer@redhat.com> 1.4.1-1
- Update to 1.4.1 (rhbz#2030430)
- Use %%autosetup and %%pypi_source macros

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.4.0-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.4.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Dan Radez <dradez@redhat.com> - 1.4.0-1
- Update to 1.4.0 (rhbz#1862179)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 05 2020 Ken Dreyer <kdreyer@redhat.com> 1.3.3-1
- Update to 1.3.3 (rhbz#1378265)
- Remove explicit Requires (rhbz#1803982)
- Use HTTPS URL

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-11
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 12 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-5
- Subpackage python2-pecan has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-3
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-2
- Rebuilt for Python 3.7

* Fri Jun 01 2018 Alfredo Moralejo <amoralej@redhat.com> - 1.3.2-1
- Update to 1.3.2 release. It adds support for webob >= 1.8.0.

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 23 2017 Alan Pevec <alan.pevec@redhat.com> 1.2.1-1
- Update to 1.2.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1.2-2
- Rebuild for Python 3.6

* Tue Jul 19 2016 Alan Pevec <alan.pevec@redhat.com> 1.1.2-1
- Update to 1.1.2

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Nov  7 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.2-3
- Fix the naming of python2 vs python3 versions of the scripts to comply with
  the python guidelines: https://fedoraproject.org/wiki/Packaging:Python#Naming
  This fixes several things:
  * The scripts in the python2-pecan package not working because they
    needed the python3-pecan libraries but there was no rpm dependency
  * The python2-pecan package requiring /usr/bin/python3
  * The python2-pecan package's scripts wouldn't have been able to serve
    web apps written in python2 because they were using python3 and would
    have failed to run pyhon2 scripts in their python3 process.
  * If those were fixed properly then the python-pecan and python3-pecan
    packages would have conflicted due to the scripts being different between
    the packages.
  Following the guidelines solves all of these problems.

* Sun Sep 06 2015 Matthias Runge <mrunge@redhat.com> - 1.0.2-2
- fix provides and obsoletes

* Fri Sep 04 2015 Chandan Kumar <chkumar246@gmail.com> - 1.0.2-1
- Added python2 and python3 subpackage
- Bumped to 1.0.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 26 2015 Pádraig Brady <pbrady@redhat.com> - 0.8.3-1
- Latest upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 23 2014 Pádraig Brady <pbrady@redhat.com> - 0.4.5-3
- Add missing dependency on python-logutils

* Tue Mar 18 2014 Pádraig Brady <pbrady@redhat.com> - 0.4.5-2
- Add missing dependency on python-singledispatch

* Mon Mar 10 2014 Pádraig Brady <pbrady@redhat.com> - 0.4.5-1
- Latest upstream

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr  5 2013 Luke Macken <lmacken@redhat.com> - 0.2.1-5
- Require python-webob >= 1.2 instead of python-webob1.2

* Thu Mar 14 2013 Padraig Brady <P@draigBrady.com> - 0.2.1-4
- Initial package.
