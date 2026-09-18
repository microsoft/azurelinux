# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name path

Name:           python-path
Version:        17.1.0
Release:        5%{?dist}
Summary:        Python module wrapper for os.path

License:        MIT
URL:            https://pypi.org/pypi/path
Source0:        %pypi_source
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(more-itertools)
%generate_buildrequires
%pyproject_buildrequires

%description
path.py implements path objects as first-class entities, allowing common
operations on files to be invoked on those path objects directly.


%package    -n python3-path
Summary:        Python 3 module wrapper for os.path
%{?python_provide:%python_provide python3-path}


%description -n python3-path
path.py implements path objects as first-class entities, allowing common
operations on files to be invoked on those path objects directly.


%prep
%autosetup -n %{pypi_name}-%{version} -p1


%build
%pyproject_wheel


%install
%pyproject_install


%check
%pytest


%files -n python3-path
%{python3_sitelib}/path
%{python3_sitelib}/path-%{version}.dist-info/


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 17.1.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 17.1.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 17.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 17.1.0-2
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Dan Radez <dradez@redhat.com> - 17.1.0
- update to upstream 17.1.0 rhbz#2334741

* Thu Aug 01 2024 Dan Radez <dradez@redhat.com> - 17.0.0
- update to upstream 17.0.0 rhbz#2300203

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 16.14.0-2
- Rebuilt for Python 3.13

* Wed Apr 10 2024 Dan Radez <dradez@redhat.com> - 16.14.0-1
- update to upstream 16.14.0 rhbz#2274154

* Mon Apr 08 2024 Dan Radez <dradez@redhat.com> - 16.13.0-1
- update to upstream 16.13.0 rhbz#2273501

* Wed Feb 14 2024 Dan Radez <dradez@redhat.com> - 16.10.0-1
- update to upstream 16.10.0 rhbz#2262643

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 21 2023 Dan Radez <dradez@redhat.com> - 16.9.0-1
- update to 16.9.0 rhbz#2253604

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 16.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Dan Radez <dradez@redhat.com> - 16.7.1-1
- update to 16.7.1

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 16.6.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 16.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Dan Radez <dradez@redhat.com> - 16.6.0-1
- updating to 16.6.0 - rhbz#2149909

* Fri Sep 30 2022 Dan Radez <dradez@redhat.com> - 16.5.0-1
- Update to 16.5.0 - rhbz#2130356
- removing rpm spec exclude, file is not in the source anymore

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 16.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 16.4.0-2
- Rebuilt for Python 3.11

* Thu Mar 31 2022 Dan Radez - 16.4.0-1
- Updating to latest release.
- Release Monitoring has been monitoring the wrong project, it was renamed from path.py to path

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 11.5.0-7
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 11.5.0-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Miro Hrončok <mhroncok@redhat.com> - 11.5.0-2
- Subpackage python2-path has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Aug 20 2019 Ken Dreyer <kdreyer@redhat.com> - 11.5.0-1
- Update to latest upstream release (rhbz#1206250)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 5.2-18
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.2-15
- Drop explicit locale setting for python3, use C.UTF-8 for python2
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 5.2-13
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Troy Dawson <tdawson@redhat.com> - 5.2-11
- Update conditional

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Thomas Spura <tomspur@fedoraproject.org> - 5.2-8
- rename python-* to python2-*
- expand %%files
- use py_build/install macros

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 5.2-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Orion Poplawski <orion@cora.nwra.com> - 5.2-4
- Fix py.test call for python3

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Sep  3 2014 Thomas Spura <tomspur@fedoraproject.org> - 5.2-2
- enable testsuite

* Wed Sep  3 2014 Thomas Spura <tomspur@fedoraproject.org> - 5.2-1
- update to 5.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Apr 04 2014 Xavier Lamien <laxathom@fedoraproject.org> - 5.1-1
- Upstream release.
- Add python3's subpackage.

* Fri Jul 26 2013 Xavier Lamien <laxathom@fedoraproject.org> - 4.3-1
- Upstream release.

* Wed Apr 10 2013 Xavier Lamien <laxathom@fedoraproject.org> - 3.0.1-2
- Add %%check stage.
- Update BuildRequire.
- Add missing %%docs.

* Wed Apr 10 2013 Xavier Lamien <laxathom@fedoraproject.org> - 3.0.1-1
- Initial RPM release.
