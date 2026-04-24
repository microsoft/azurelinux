# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           pyxdg
Version:        0.28
Release: 2%{?dist}
Summary:        Python library to access freedesktop.org standards
License:        LGPL-2.0-only
URL:            http://freedesktop.org/Software/pyxdg
Source0:        %pypi_source
# https://cgit.freedesktop.org/xdg/pyxdg/commit/?id=275865e620471c194560824232be632c9cb61600
Patch0:         pyxdg-replace-imp-with-importlib.patch
# https://cgit.freedesktop.org/xdg/pyxdg/commit/?id=9291d419017263c922869d79ac1fe8d423e5f929
Patch1:         pyxdg-handle-python-3.14-ast.Str-changes.patch
# https://cgit.freedesktop.org/xdg/pyxdg/commit/?id=63033ac306aa26d32e1439417e59ae8f8a4c9820
Patch2:         pyxdg-handle-python-3.15-deprecations.patch

BuildArch:      noarch
# These are needed for the tests.
BuildRequires:  python3-pytest
BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info

%description
PyXDG is a python library to access freedesktop.org standards.

%package -n python%{python3_pkgversion}-pyxdg
Summary:        Python3 library to access freedesktop.org standards
%{?python_provide:%python_provide python%{python3_pkgversion}-pyxdg}

%description -n python%{python3_pkgversion}-pyxdg
PyXDG is a python library to access freedesktop.org standards. This
package contains a Python 3 version of PyXDG.

%prep
%setup -q
%patch -P0 -p1 -b .replace-imp-with-importlib
%patch -P1 -p1 -b .handle-python-3.14-ast.Str-changes
%patch -P2 -p1 -b .handle-python-3.15-deprecations

# fix symlink example
rm -rf test/example/png_symlink
pushd test/example
ln -s png_file png_symlink
popd

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l xdg

%check
%pyproject_check_import
%pytest test/test_*.py

%files -n python%{python3_pkgversion}-pyxdg -f %{pyproject_files}
%license COPYING
%doc AUTHORS ChangeLog README TODO

%changelog
* Tue Jan 20 2026 Tom Callaway <spot@fedoraproject.org> - 0.28-1
- update to 0.28

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sun Nov 09 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.27-20
- Run tests with pytest

* Thu Nov  6 2025 Tom Callaway <spot@fedoraproject.org> - 0.27-19
- apply upstream cleanup commits for modern python support
- modernize package for new python macros
- thanks to John for the heads-up

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.27-18
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.27-17
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.27-15
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.27-12
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.27-8
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.27-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.27-2
- Rebuilt for Python 3.10

* Tue Apr 13 2021 Tom Callaway <spot@fedoraproject.org> - 0.27-1
- update to 0.27

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.26-10
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 07 2019 Miro Hrončok <mhroncok@redhat.com> - 0.26-8
- Subpackage python2-pyxdg has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.26-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.26-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 30 2018 Tom Callaway <spot@fedoraproject.org> - 0.26-3
- fix incorrect use of Type attribute (bz 1654857)

* Thu Nov  1 2018 Tom Callaway <spot@fedoraproject.org> - 0.26-2
- fix OnlyShowIn (bz 1624651)

* Mon Jul 23 2018 Tom Callaway <spot@fedoraproject.org> - 0.26-1
- update to 0.26

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 0.25-16
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.25-14
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.25-11
- Rebuild for Python 3.6

* Mon Nov 21 2016 Orion Poplawski <orion@cora.nwra.com> - 0.25-10
- Ship python2-pyxdg
- Enable python 3 builds for EPEL
- Use %%license
- Modernize spec

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Dec  4 2014 Tom Callaway <spot@fedoraproject.org> - 0.25-5
- fix CVE-2014-1624

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Tom Callaway <spot@fedoraproject.org> - 0.25-1
- update to 0.25

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov  7 2012 Tomas Bzatek <tbzatek@redhat.com> - 0.24-1
- update to 0.24

* Fri Oct 26 2012 Tom Callaway <spot@fedoraproject.org> - 0.23-2
- gracefully handle kde-config fails

* Mon Oct  8 2012 Tom Callaway <spot@fedoraproject.org> - 0.23-1
- update to 0.23
- enable python3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr 28 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-1
- update to 0.19

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-1
- update to 0.17

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.16-2
- Rebuild for Python 2.6

* Thu Oct 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-1
- update to 0.16
- fix indent bug in DesktopEntry.py (bz 469229)

* Sat Apr  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.15-6
- add egg-info (fixes FTBFS bz 440813)

* Wed Jan  3 2007 Patrice Dumas <pertusus@free.fr> - 0.15-5
- remove requires for python-abi (automatic now) and python directory
- remove package name from summary
- change tabs to spaces

* Thu Dec 21 2006 Patrice Dumas <pertusus@free.fr> - 0.15-4
- rebuild for python 2.5

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 0.15-3
- rebuild for fc6

* Wed Feb 15 2006 John Mahowald <jpmahowald@gmail.com> - 0.15.2
- Rebuild for Fedora Extras 5

* Fri Oct 14 2005 John Mahowald <jpmahowald@gmail.com> - 0.15-1
- Rebuilt for 0.15

* Sun Jul 03 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.14-2
- Added %%{?dist} tag to release
- BuildArch: noarch
- Removed unneccesary CLFAGS

* Sun Jun 05 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.14-1
- Rebuilt for 0.14

* Wed Jun 01 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.13-1
- Rebuilt for 0.13

* Tue May 31 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.12-1
- Rebuilt for 0.12

* Sat May 28 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.11-1
- Rebuilt for 0.11

* Mon May 23 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.10-1
- Adapt to Fedora Extras template, based on spec from NewRPMs

* Tue Dec 14 2004 Che
- initial rpm release


