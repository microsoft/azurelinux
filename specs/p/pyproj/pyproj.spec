# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# note: PROJ_MIN_VERSION is defined in the setup.py file of pyproj
# a compatibility matrix is also provided in docs/installation.rst
%global minimal_needed_proj_version 9.4.0

# Several dependencies are not yet rebuilt for Python 3.14:
%bcond xarray 0

Name:           pyproj
Version:        3.7.2
Release: 3%{?dist}
Summary:        Cython wrapper to provide python interfaces to Proj
# this software uses the "MIT:Modern Style with sublicense" license
License:        MIT
URL:            https://github.com/jswhit/%{name}
Source0:        https://files.pythonhosted.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

# see: https://github.com/pyproj4/pyproj/issues/1501
Patch1:         pyproj-proj-9.6.2.patch

BuildRequires:  gcc
BuildRequires:  proj-devel >= %{minimal_needed_proj_version}
BuildRequires:  proj >= %{minimal_needed_proj_version}

# these next 4 are no longer needed and taken care of automagically
#BuildRequires:  make
#BuildRequires:  python3-cython
#BuildRequires:  python3-certifi
#BuildRequires:  python3-shapely

# needed to run the tests
BuildRequires:  python3-pytest
# needed for i686 testing
BuildRequires:  python3-numpy

# Pandas will drop i686 (xarray depends on pandas)
# https://bugzilla.redhat.com/show_bug.cgi?id=2263999 
%ifnarch %{ix86}
BuildRequires:  python3-pandas
%if %{with xarray}
BuildRequires:  python3-xarray
%endif
%endif

# needed to remove the hardcoded rpath '/usr/lib' from the _proj.so file
BuildRequires:  chrpath

# needed to build the documentation
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-argparse
BuildRequires:  python3-sphinx_rtd_theme

%global _description \
Cython wrapper to provide python interfaces to Proj. \
Performs cartographic transformations between geographic (Lat/Lon) \
and map projection (x/y) coordinates. Can also transform directly \
from one map projection coordinate system to another. \
Coordinates can be given as numpy arrays, python arrays, lists or scalars. \
Optimized for numpy arrays.

%description %_description

%package -n python3-%{name}

Summary: %summary

Requires:  proj >= %{minimal_needed_proj_version}

# ensure python provides are provided when python3 becomes the default runtime
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name} %_description

%package -n python3-%{name}-doc

Summary:    Documentation and example code
BuildArch:  noarch

%description -n python3-%{name}-doc
This package contains the html documentation for the pyproj module.

%prep
%autosetup -p1

%generate_buildrequires
%pyproject_buildrequires

%build
export PROJ_DIR="%{_usr}/"

%pyproject_wheel

# generate documentation
cd docs

# Need to point to the build dir so sphinx can import the module
# before it is installed.
# Note that the new Python macros have %%{pyproject_build_lib} for this,
# but this package uses the old macros, so we need to replicate the behavior
# manually.
# The path has changed in setuptools 62.4.0,
# see https://bugzilla.redhat.com/2097115
%global py_build_libdir_old %{_builddir}/%{buildsubdir}/build/lib.%{python3_platform}-%{python3_version}
%global py_build_libdir_new %{_builddir}/%{buildsubdir}/build/lib.%{python3_platform}-cpython-%{python3_version_nodots}

# NOTE: need to add %%{_builddir}/%%{buildsubdir} as well to the path
# since sphinx needs to be able to find the PKG-INFO file
# before it will generate the documentation,
# and this is the only place where it is available before installation.
# (see: https://github.com/python/importlib_metadata/issues/364)
export PYTHONPATH=%{py_build_libdir_old}:%{py_build_libdir_new}:%{_builddir}/%{buildsubdir}

# default theme is now "furo" which is not available in fedora
# (see BZ #1910798 and https://github.com/pyproj4/pyproj/discussions/1134)
# so fall back to the previous theme:
export PYPROJ_HTML_THEME=sphinx_rtd_theme

make html
make man

%install
export PROJ_DIR="%{_usr}/"
%pyproject_install
%pyproject_save_files -l pyproj

# move html documentation to datadir/doc
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
mv %{_builddir}/%{name}-%{version}/docs/_build/html \
   %{buildroot}%{_datadir}/doc/%{name}/html

# copy pyproj man page
mkdir -p %{buildroot}/%{_mandir}/man1
cp %{_builddir}/%{name}-%{version}/docs/_build/man/pyproj.1 \
   %{buildroot}/%{_mandir}/man1/

# remove the documentation sources and generated doctrees
# since they dont belong in the main package
%{__rm} -rf %{_builddir}/%{name}-%{version}/docs

# correct wrong write permission for group
%{__chmod} 755 %{buildroot}/%{python3_sitearch}/%{name}/*.so

# remove the rpath setting from _proj.so
chrpath -d %{buildroot}/%{python3_sitearch}/%{name}/*.so


%check

# check importing the pyproj module
%py3_check_import pyproj

# follow the hint given in pyproj github issue
# https://github.com/pyproj4/pyproj/issues/647
# i.e. take the test folder outside the build folder
# to prevent the
#    cannot import name '_datadir' from partially initialized module
#    'pyproj' (most likely due to a circular import) 
# error.
# (probably this is not needed anymore but it doesn't hurt to leave this in)
cd ..
mkdir pyproj-test-folder
cd pyproj-test-folder
cp -r ../pyproj-%{version}/test .
cp ../pyproj-%{version}/pytest.ini .

# Test without pandas on i686
%ifnarch %{ix86}
%pytest -m "not network"
%else
%pytest -m "not network and not pandas"
%endif

# some notes on the test suite:
# not network ==> deselects 24 tests

%files -n python3-%{name} -f %{pyproject_files}
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/pyproj*

%files -n python3-%{name}-doc
%doc %{_datadir}/doc/%{name}/


%changelog
* Tue Sep 30 2025 Jos de Kloe <josdekloe@gmail.com> 3.7.2-2
- Rebuild as requested by bz 2396746  (python "magic numer" bump)

* Fri Sep 12 2025 Jos de Kloe <josdekloe@gmail.com> 3.7.2-1
- Update to 3.7.2; 2 tests are still disabled due to a regression in proj 9.6.2
- Introduce new style pyproject macros

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.7.1-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 18 2025 Jos de Kloe <josdekloe@gmail.com> 3.7.1
- Update to 3.7.1; disable 4 tests due to a regression in proj 9.6.2

* Tue Jun 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.7.0-4
- Temporarily omit xarray tests to unblock Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.7.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 03 2024 Jos de Kloe <josdekloe@gmail.com> 3.7.0
- Update to 3.7.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Karolina Surma <ksurma@redhat.com> - 3.6.1-6
- Fix package build in Fedora Rawhide

* Tue Jun 18 2024 Python Maint <python-maint@redhat.com> - 3.6.1-5
- Rebuilt for Python 3.13

* Tue Mar 05 2024 Sandro <devel@penguinpee.nl> - 3.6.1-4
- Drop dependency on pandas for i686

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 27 2023 Jos de Kloe <josdekloe@gmail.com> 3.6.1-1
- Update to 3.6.1; remove patch0

* Wed Sep 13 2023 Sandro Mani <manisandro@gmail.com> - 3.6.0-3
- Rebuild (proj)

* Wed Jul 19 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.6.0-2
- Rebuild for Python 3.12b4

* Sat Jun 17 2023 Jos de Kloe <josdekloe@gmail.com> 3.6.0-1
- Update to 3.6.0

* Thu Mar 30 2023 Jos de Kloe <josdekloe@gmail.com> 3.5.0-1
- Update to 3.5.0

* Wed Dec 28 2022 Jos de Kloe <josdekloe@gmail.com> 3.4.1-2
- SPDX migration: checked the license text, and concluded that MIT is the
  correct SPDX license tag.

* Mon Dec 26 2022 Jos de Kloe <josdekloe@gmail.com> 3.4.1-1
- Update to 3.4.1

* Sat Sep 10 2022 Jos de Kloe <josdekloe@gmail.com> 3.4.0-1
- Update to 3.4.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 25 2022 Jos de Kloe <josdekloe@gmail.com> 3.3.1-2
- Adjust py_build_libdir to let sphinx build the documentation
  with the latest setuptools version (62.4.0)

* Sun Apr 24 2022 Jos de Kloe <josdekloe@gmail.com> 3.3.1-1
- Update to 3.3.1

* Wed Mar 09 2022 Sandro Mani <manisandro@gmail.com> - 3.3.0-3
- Rebuild for proj-9.0.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 18 2021 Jos de Kloe <josdekloe@gmail.com> 3.3.0-1
- Update to 3.3.0

* Sat Sep 18 2021 Jos de Kloe <josdekloe@gmail.com> 3.2.1-1
- Update to 3.2.1

* Wed Sep 08 2021 Jos de Kloe <josdekloe@gmail.com> 3.2.0-2
- Move documentation in stead of copying it to prevent providing it twice.

* Sun Sep 05 2021 Jos de Kloe <josdekloe@gmail.com> 3.2.0-1
- Update to 3.2.0

* Wed May 26 2021 Jos de Kloe <josdekloe@gmail.com> 3.1.0-2
- Patch a problem in pyproj/enum.py found during python3.10.0b1 COPR testing

* Tue May 25 2021 Jos de Kloe <josdekloe@gmail.com> 3.1.0-1
- Update to 3.1.0

* Mon May 10 2021 Jos de Kloe <josdekloe@gmail.com> 3.0.1-3
- Fix rawhide build after proj was upgraded to v8.0.1

* Wed Mar 10 2021 Sandro Mani <manisandro@gmail.com> - 3.0.1-2
- Rebuild (proj)

* Tue Mar 09 2021 Jos de Kloe <josdekloe@gmail.com> 3.0.1-1
- Update to 3.0.1
- Add man page for standalone pyproj tool

* Sun Mar 07 2021 Sandro Mani <manisandro@gmail.com> - 3.0.0.post1-3
- Rebuild (proj)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0.post1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 05 2020 Sandro Mani <manisandro@gmail.com> - 3.0.0.post1-1
- Update to 3.0.0 for proj-7.2.0 compatibility

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1.post1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.6.1.post1-2
- Rebuilt for Python 3.9

* Thu May 21 2020 Jos de Kloe <josdekloe@gmail.com> 2.6.1.post1-1
- Update to 2.6.1.post1

* Thu Mar 19 2020 Jos de Kloe <josdekloe@gmail.com> 2.6.0-1
- Update to 2.6.0

* Sat Feb 29 2020 Jos de Kloe <josdekloe@gmail.com> 2.5.0-1
- Update to 2.5.0

* Sun Dec 01 2019 Jos de Kloe <josdekloe@gmail.com> 2.4.2.post1-1
- Update to 2.4.2.post1 and remove patch (fix was included upstream)

* Sat Nov 23 2019 Jos de Kloe <josdekloe@gmail.com> 2.4.1-2
- Patch bug that caused 6 failing tests on i686 architecture
  and clean up some no longer needed fixes

* Sat Nov 9 2019 Jos de Kloe <josdekloe@gmail.com> 2.4.1-1
- Update to 2.4.1

* Sun Sep 08 2019 Jos de Kloe <josdekloe@gmail.com> 2.3.1-2
- add documentation generation, fix python usage in it and add a doc subpackage

* Wed Sep 4 2019 Devrim Günduz <devrim@gunduz.org> - 2.3.1-1
- Update to 2.3.1

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.6-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.6-2
- Subpackage python2-pyproj has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sun Feb 17 2019 Jos de Kloe <josdekloe@gmail.com> 1.9.6-1
- update to version 1.9.6, remove python2 sub-package for Fedora 30+
- remove use of py3dir macro when building python3 sub-package

* Tue Feb 12 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.9.5.1-18
- Rebuilt for updated Proj

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 17 2018 Jos de Kloe <josdekloe@gmail.com> 1.9.5.1-16
- merge with cython patch by Miro Hrončok <pagure@pkgs.fedoraproject.org>
  (there is no more cython3 command; Cython behaves the same on both Pythons)
- remove the no_inv_hammer_test patch

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.5.1-14
- Rebuilt for Python 3.7

* Sat Feb 24 2018 Jos de Kloe <josdekloe@gmail.com> 1.9.5.1-13
- Add explicit BuildRequires for gcc

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.9.5.1-9
- Rebuild due to bug in RPM (RHBZ #1468476)

* Thu Jul 06 2017 Björn Esser <besser82@fedoraproject.org> - 1.9.5.1-8
- move package specific (Build)Requires in the correspondig sub-packages

* Thu Jul 06 2017 Björn Esser <besser82@fedoraproject.org> - 1.9.5.1-7
- setup filtering for private libs correctly

* Fri Jun 30 2017 Jos de Kloe <josdekloe@gmail.com> 1.9.5.1-6
- rename pyproj to python2-pyproj following the new package naming scheme

* Wed Feb 01 2017 Jos de Kloe <josdekloe@gmail.com> 1.9.5.1-5
- force rebuild after libproj soname jump

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.9.5.1-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.5.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Jos de Kloe <josdekloe@gmail.com> 1.9.5.1-1
- update to new upstream version
- remove the inverse hammer test

* Thu Nov 12 2015 Jos de Kloe <josdekloe@gmail.com> 1.9.4-4
- apply patch to fix a bug in _proj.pyx that surfaced in cython 0.23
- apply chrpath to fix binary-or-shlib-defines-rpath error reported by rpmlint

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 12 2015 Jos de Kloe <josdekloe@gmail.com> 1.9.4-1
- update to version 1.9.4
- replace python_sitearch macro with python2_sitearch
- replace the deprecated macro __python by __python3
- activate the check section

* Sat Jan 11 2014 Jos de Kloe <josdekloe@gmail.com> 1.9.2-8.20120712svn300
- replace the deprecated macro __python by __python2
- require proj-epsg to solve bug #1022238

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-7.20120712svn300
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-6.20120712svn300
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 12 2012 Jos de Kloe <josdekloe@gmail.com> 1.9.2-5.20120712svn300
- adapted version number format to comply to the Snapshot packages 
  guidelines, and move to svn revision 300.

* Wed Jun 20 2012 Jos de Kloe <josdekloe@gmail.com> 1.9.2-4.r298
- Added proj-nad as explicit Requirement since it contains data files needed
  to run the module, and bumped the version number to the one mentioned in 
  the setup-proj.py script

* Fri Jun 15 2012 Jos de Kloe <josdekloe@gmail.com> 1.9.0-3.r298
- Adapted to build with python3

* Thu May 31 2012 Jos de Kloe <josdekloe@gmail.com> 1.9.0-2.r298
- Adapted to svn revision r298 which has some modifications
  to allow building without using the included proj sources

* Mon Apr 23 2012 Volker Fröhlich <volker27@gmx.at> - 1.9.0-1
- Initial package for Fedora
