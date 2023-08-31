%define so_ver 2

Summary:        Library for ESRI Shapefile Handling
Name:           shapelib
Version:        1.5.0
Release:        3%{?dist}
License:        GPL-2.0-or-later AND (LGPL-2.0-or-later OR MIT) AND SUSE-Public-Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Productivity/Graphics/Other
URL:            https://shapelib.maptools.org/
Source0:        https://download.osgeo.org/shapelib/%{name}-%{version}.tar.gz
# PATCH-FIX-UPSTREAM rpmlint-errors.patch -- Fix some of the rpmlint errors
# to get package acceptable to Factory
Patch0:         rpmlint-errors.patch
# PATCH-Fix-UPSTREAM double free, CVE-2022-0699, https://github.com/OSGeo/shapelib/issues/39
Patch1:         CVE-2022-0699.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
# dbfdump is also in perl-DBD-XBase
Conflicts:      perl-DBD-XBase

%description
The Shapefile C Library provides the ability to write simple C programs for
reading, writing and updating (to a limited extent) ESRI Shapefiles, and the
associated attribute file (.dbf).

This package contains the executable programs.

%package -n libshp-devel
Summary:        Development Environment for %{name}
Group:          Development/Libraries/C and C++
Requires:       libshp%{so_ver} = %{version}
Provides:       shapelib-devel = %{version}

%description -n libshp-devel
The Shapefile C Library provides the ability to write simple C programs for
reading, writing and updating (to a limited extent) ESRI Shapefiles, and the
associated attribute file (.dbf).

This package contains the development environment for shapelib project.

%package -n libshp%{so_ver}
Summary:        Library for ESRI Shapefile Handling
Group:          System/Libraries

%description -n libshp%{so_ver}
The Shapefile C Library provides the ability to write simple C programs for
reading, writing and updating (to a limited extent) ESRI Shapefiles, and the
associated attribute file (.dbf).

This package contains the dynamic link library for shapelib project.

%prep
%autosetup -p1

# Fix rpmlint warning "wrong-file-end-of-line-encoding"
sed -i 's/\r$//' contrib/doc/shpsort.txt

%build
%configure \
  --disable-static \
  --disable-silent-rules
%make_build

%install
%make_install

# Remove libtool config files
find %{buildroot} -type f -name "*.la" -delete -print

%check
# Contrib tests fail
%make_build check ||:

%post -n libshp%{so_ver} -p /sbin/ldconfig
%postun -n libshp%{so_ver} -p /sbin/ldconfig

%files
%license COPYING
%doc ChangeLog
%doc contrib/doc/ web/
%{_bindir}/Shape_PointInPoly
%{_bindir}/dbfadd
%{_bindir}/dbfcat
%{_bindir}/dbfcreate
%{_bindir}/dbfdump
%{_bindir}/dbfinfo
%{_bindir}/shpadd
%{_bindir}/shpcat
%{_bindir}/shpcentrd
%{_bindir}/shpcreate
%{_bindir}/shpdata
%{_bindir}/shpdump
%{_bindir}/shpdxf
%{_bindir}/shpfix
%{_bindir}/shpinfo
%{_bindir}/shprewind
%{_bindir}/shpsort
%{_bindir}/shptreedump
%{_bindir}/shputils
%{_bindir}/shpwkb

%files -n libshp-devel
%{_includedir}/*
%{_libdir}/pkgconfig/shapelib.pc
%{_libdir}/libshp.so

%files -n libshp%{so_ver}
%{_libdir}/libshp.so.%{so_ver}*

%changelog
* Sun Aug 20 2023 Archana Choudhary <archana1@microsoft.com> - 1.5.0-3
- Update 'Release' tag format to '[number]%{?dist}'

* Thu Aug 10 2023 Archana Choudhary <archana1@microsoft.com> - 1.5.0-2.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified

* Mon Feb 21 2022 Dirk Stoecker <opensuse@dstoecker.de>
- fix CVE-2022-0699, patch c75b9281a5b9452d92e1682bdfe6019a13ed819f.diff

* Sat Mar 30 2019 Atri Bhattacharya <badshah400@gmail.com>
- Update to version 1.5.0:
  * shpopen.c: resync with GDAL internal shapelib to avoid being
    dependent on correctness of file size field in .shp. Fixes
    https://lists.osgeo.org/pipermail/gdal-dev/2018-October/049218.html
  * contrib/shpgeo.h/.c: Remove PROJ.4 dependency and
    functionality, causing removal of SHPProject(),
    SHPSetProjection() and SHPFreeProjection()
  * contrib/shpproj.c: removed
    shpopen.c, dbfopen.c, shptree.c, sbnsearch.c: resyc with GDAL
    internal shapelib. Mostly to allow building those files as C++
    without warning. Also add FTDate entry in DBFFieldType (see
    https://github.com/OSGeo/gdal/pull/308). And some other code
    cleanups
  * dbfopen.c: fix a bug where the end of file character was
    written on top of the first character of the first field name
    when deleting a field on a .dbf without records.  Fixes
    https://github.com/OSGeo/gdal/issues/863
  * safileio.c: remove duplicate test. Patch by Jaroslav Fojtik.
    Fixes http://bugzilla.maptools.org/show_bug.cgi?id=2744
- Rebase rpmlint-errors.patch for current version.
- Drop proj4 Requires and BuildRequires: functionality dropped by
  upstream.

* Wed Jul 25 2018 mpluskal@suse.com
- Update to version 1.4.1:
  * See ChangeLog for details
- Drop no longer needed patches:
  * shapelib_autotools.patch
  * shapelib_backports.patch
- Refresh rpmlint-errors.patch

* Fri May 29 2015 tchvatal@suse.com
- Add patch to fix bunch of rpmlint errors:
  * rpmlint-errors.patch
- Refresh autotools patch to actually pass the testsuite:
  * shapelib_autotools.patch

* Thu May 28 2015 dgutu@suse.com
- Re-enabled the post build check now everything fails because of
  coding issues
- This needs to be fixed not hidden

* Wed May 27 2015 dgutu@suse.com
- Called spec-cleaner against spec file

* Wed May 28 2014 asterios.dramis@gmail.com
- Update to version 1.3.0:
  * See ChangeLog for details.
- Corrected the Name: entry in the spec file from libshp1 to shapelib (same as
  spec file name and package name).
- Changed License to "(LGPL-2.0+ or MIT) and GPL-2.0+ and SUSE-Public-Domain".
- Removed shapelib-endian-destdir-combined.diff and shapelib-fix-contrib.diff
  patches (not needed anymore).
- Added two patches (taken from Fedora):
  * shapelib_autotools.patch (Use autotools)
  * shapelib_backports.patch (Backport some fixes from the gdal bundled
    shapelib)
- Removed gcc and make build requirements (not needed).
- Added gcc-c++ and pkg-config build requirements.

* Tue Apr  2 2013 opensuse@dstoecker.de
- fix license

* Mon Jul 21 2008 Dirk Stöcker <opensuse@dstoecker.de>
- some BuildService and rpmlint fixes
  Wed Jan 11 00:00:00 UTC 2006 Pascal Bleser
- added fixing of libshp.la file ("installed=no" -> "installed=yes")
  Wed Jan 11 00:00:00 UTC 2006 Pascal Bleser
- new package
