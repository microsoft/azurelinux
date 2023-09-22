#
# spec file for package proj
#
# Copyright (c) 2023 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
%define data_version 1.14
%define sover   25
%define libname lib%{name}%{sover}
Summary:        Cartographic projection software
Name:           proj
Version:        9.2.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://proj.org/
Source0:        https://download.osgeo.org/proj/%{name}-%{version}.tar.gz
Source1:        https://download.osgeo.org/%{name}/%{name}-data-%{data_version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
BuildRequires:  pkgconfig
BuildRequires:  sqlite
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(sqlite3)
Provides:       libproj = %{version}

%description
This package offers the commandline tools for performing respective
forward and inverse transformation of cartographic data to or from cartesian
data with a wide range of selectable projection functions.

%package -n %{libname}
Summary:        Cartographic projection software

%description -n %{libname}
This package the library for performing respective
forward and inverse transformation of cartographic data to or from cartesian
data with a wide range of selectable projection functions.

%package devel
Summary:        Development files for PROJ
Requires:       %{libname} = %{version}
Provides:       libproj-devel = %{version}
Obsoletes:      libproj-devel < %{version}

%description devel
This package contains libproj and the appropriate header files and man pages.

%define data_subpkg(c:n:e:s:) \
  %define countrycode %{-c:%{-c*}}%{!-c:%{error:Country code not defined}} \
  %define countryname %{-n:%{-n*}}%{!-n:%{error:Country name not defined}} \
  %define extrafile %{-e:%{_datadir}/%{name}/%{-e*}} \
  %define wildcard %{!-s:%{_datadir}/%{name}/%{countrycode}_*} \
  \
  %package data-%{countrycode}\
  Summary:      %{countryname} datum grids for Proj\
  BuildArch:    noarch\
  # See README.DATA \
  License:      BSD-2-Clause AND CC0-1.0 AND CC-BY-4.0 AND CC-BY-SA-4.0 AND SUSE-Public-Domain \
  Supplements:  proj\
  \
  %description data-%{countrycode}\
  %{countryname} datum grids for Proj.\
  \
  %files data-%{countrycode}\
  %{wildcard}\
  %{extrafile}

%data_subpkg -c at -n Austria
%data_subpkg -c au -n Australia
%data_subpkg -c be -n Belgium
%data_subpkg -c br -n Brasil
%data_subpkg -c ca -n Canada
%data_subpkg -c ch -n Switzerland
%data_subpkg -c de -n Germany
%data_subpkg -c dk -n Denmark -e DK
%data_subpkg -c es -n Spain
%data_subpkg -c eur -n %{quote:Nordic + Baltic} -e NKG
%data_subpkg -c fi -n Finland
%data_subpkg -c fo -n %{quote:Faroe Island} -e FO -s 1
%data_subpkg -c fr -n France
%data_subpkg -c is -n Island -e ISL
%data_subpkg -c jp -n Japan
%data_subpkg -c mx -n Mexico
%data_subpkg -c nc -n %{quote:New Caledonia}
%data_subpkg -c nl -n Netherlands
%data_subpkg -c no -n Norway
%data_subpkg -c nz -n %{quote:New Zealand}
%data_subpkg -c pl -n Poland
%data_subpkg -c pt -n Portugal
%data_subpkg -c se -n Sweden
%data_subpkg -c sk -n Slovakia
%data_subpkg -c uk -n %{quote:United Kingdom}
%data_subpkg -c us -n %{quote:United States}
%data_subpkg -c za -n %{quote:South Africa}

%prep
%autosetup

%build
%cmake -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir}
%cmake_build

%install
%cmake_install
tar -C %{buildroot}%{_datadir}/%{name} -xf %{SOURCE1}
find %{buildroot} -type f -name "*.la" -delete -print
# It would be good to find out where these extra files
# come from:
rm -rf %{buildroot}%{_datadir}/doc/${name}

%check
# Tests dont work on i586 and noone cares
%ifnarch %{ix86}
%ctest
%endif

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%doc NEWS AUTHORS README ChangeLog
%license COPYING
%defattr(0755,root,root)
%{_bindir}/cs2cs
%{_bindir}/cct
%{_bindir}/gie
%{_bindir}/geod
%{_bindir}/invgeod
%{_bindir}/invproj
%{_bindir}/proj
%{_bindir}/projsync
%{_bindir}/projinfo
%defattr(0644,root,root)
%{_mandir}/man1/cs2cs.1*%{?ext_man}
%{_mandir}/man1/geod.1*%{?ext_man}
%{_mandir}/man1/proj.1*%{?ext_man}
%{_mandir}/man1/cct.1*%{?ext_man}
%{_mandir}/man1/gie.1*%{?ext_man}
%{_mandir}/man1/projinfo.1*%{?ext_man}
%{_mandir}/man1/projsync.1*%{?ext_man}
%{_datadir}/%{name}/*

%files -n %{libname}
%{_libdir}/libproj.so.%{sover}*

%files devel
%{_includedir}/*.h
%{_includedir}/proj
%{_libdir}/libproj.so
%dir %{_libdir}/cmake/proj/
%{_libdir}/cmake/proj/*.cmake
%dir %{_libdir}/cmake/proj4/
%{_libdir}/cmake/proj4/*.cmake
%{_libdir}/pkgconfig/proj.pc

%changelog
* Fri Jul 21 2023 Suresh Thelkar <sthelkar@microsoft.com> - 9.2.1-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified
- Used the appropriate Build Requires for gtest
- Added Build Requires for gmock-devel
- Used wildcards in man pages in the files section

* Thu Jun  8 2023 Martin Pluskal <mpluskal@suse.com>
- Update to version 9.2.1 and data to 1.14:
  * for detailed list of changes see provided NEWS file

* Thu Mar 16 2023 Martin Pluskal <mpluskal@suse.com>
- Update to version 9.2.0 and data to 1.13:
  * for detailed list of changes see provided NEWS file

* Thu Feb  2 2023 Dirk Müller <dmueller@suse.com>
- fix license declaration

* Sat Dec  3 2022 Dirk Müller <dmueller@suse.com>
- update to 9.1.1:
  * Implement alterGeodeticCRS and stripVerticalComponent for DerivedProjected (#3482)
  * Various improvements to handling of DerivedProjectedCRS (#3482, #3477 , #3342 , #3319, #3317)
  * Add missing <cstdint> includes (#3459)
  * cs2cs: better validate value of -W option (#3453)
  * DatabaseContext::lookForGridInfo(): fix caching of filenames and set correct URLs (#3448)
  * Database: register in grid_alternatives grids from PROJ-data that have no corresponding transformation
    record (#3446)
  * cass projection: fix forward computation of easting (#3433)
  * Implement Geographic/Vertical Offset conversions (#3413)
  * vandg projection: handle +over to extend the validity domain outside of |lon|>180deg (#3427)
  * eqdc projection: avoid floating point division by zero in non-nominal case (#3415)
  * createOperations(): fix issues when transforming between Geog3D and DerivedGeog3D CRS with
    Geographic3D offsets method (#3411)
  * VerticalCRS::_isEquivalentTo(): do not consider VerticalCRS and DerivedVerticalCRS as equivalent (#3408)
  * cct and cs2cs: Avoid problems when encountering UTF-8 BOM` characters at
    beginning of input files (#3395)
  * createFromUserInput(): Improved lookup when approximate name is provided (#3371)
  * projinfo / cs2cs : auto promotion to 3D of CRS specified by name (#3367)
  * findsOpsInRegistryWithIntermediate(): make it work when source/target geodetic CRS has no known
  * createOperations(): emulate PROJ < 6 behavior when doing geocentric <–> geographic transformation
    between datum with unknown transformation (#3361)
  * Fix issue when transforming from/into a WKT2 Bound VerticalCRS with a ‘Geographic3D to GravityRelatedHeight’ method (#3355)
  * proj_normalize_for_visualization(): take into account FORCE_OVER property from source operation
  * Link geodtest against libm when available (#3341)

* Sun Nov 13 2022 Predrag Ivanović <predivan@mts.rs>
- * Update to 9.1.0:
  * Database: update to EPSG v10.074 (#3273)
  * Update ESRI objects to version 3.0.0 (#3257)
  * Add Svalbard geoid grid no_kv_arcgp-2006-sk to grid alternatives (#3292)
  * Added French grid fr_ign_RAF20 to grid alternatives (#3228)
  * PROJ pipeline generator: recognize opposite Helmert transformations using a different convention (#3265)
  * Introduce PROJ_DATA` environment variable to deprecate PROJ_LIB (#3253)
  * projinfo: fix crash on –list-crs when proj.db cannot be opened (#3290)
  * WKT parser: fix issue when parsing some WKT1 with Hotine_Oblique_Mercator_Azimuth_Center and ignoring rectified_grid_angle (#3280)
  9.0.1 Release Notes
  * Update to EPSG 10.064 (#3208)
  * Add OGC:CRS84h (WGS 84 longitude-latitude-height) (#3155)
  * Increase MAX_ITER so Mollweide forward projection works near the poles (#3082)
  * Fix wrong results with SQLite 3.38.0 (#3091)
  * Fix issue when transforming from/to BoundCRS of 3D CRS with non-Greenwich prime meridian, created from WKT (#3098)
  * Fix issues with WKT of concatenated operations (#3105)
  * unitconvert: round to nearest date when converting to yyyymmdd (#3111)
  * Fix comparison of GeodeticRefrenceFrame vs DynamicGeodeticReferenceFrame (#3120)
  * Fix datum names when importing from PROJ4 crs strings (affects some transformations using geoidgrids) (#3129)
  * Deal with PARAMETER["EPSG code for Interpolation CRS",crs_code] (#3149)
  * ITRF2014: fix ITRF2014:ITRF88,ITRF94 and ITRF96 definitions (#3159)
  * WKT import: deal with Projected CRS that is a mix of WKT1:GDAL / WKT1:ESRI (#3189)
  * createOperations(): fix/improve result of ‘BD72 + Ostend height’ to ‘WGS84+EGM96 height’ (#3199)
  * WKT import: correctly deal with absence of Latitude_Of_Origin parameter in WKT1 ESRI with Stereographic projection (#3212)
  * PROJJSON parser: do not error out if a datum ensemble member is unknown in the database (#3223)
  9.0.0 Release Notes
  * Support for the autotools build system has been removed (#3027) See RFC7 for details: https://proj.org/community/rfc/rfc-7.html
  * ESRI projection engine db to version 12.9 (#2943)
  * EPSG v10.054 (#3051)
  * Vertical grid files for PL-geoid-2011, Polish geoid model (#2960)
  * Belgian geoid model hBG18 to grid alternatives (#3044)
  * Add new option to proj_create_crs_to_crs_from_pj() method to force +over on transformation operations (#2914)
  * Implement Geographic3D to Depth/Geog2D+Depth as used by ETRS89 to CD Norway depth (#3010)
  * Use external gtest by default when possible (#3035)
  * CMake: make BUILD_SHARED_LIBS=ON the default even on Windows (#3042)
  * Fix extremely long parsing time on hostile PROJ strings (#2968)
  * Better deal with importing strings like +init=epsg:XXXX +over (#3055)
  * Fix importing CRS definition with +proj=peirce_q and +shape different from square or diamond (#3057)
- Packaging changes:
  * Switch to cmake build
  * Add nlohmann_json-devel as BuildReq

* Fri Jan 21 2022 Dirk Müller <dmueller@suse.com>
- update to 8.2.1:
  * BoundCRS WKT import: fix setting of name
  * PROJStringFormatter::toString
  * Ensure CApi test are cross-platform
  * createOperations(): do not stop at the first operation in the PROJ namespace
    for vertical transformations
  * createOperationsCompoundToCompound(): fix null pointer dereference when
    connection to proj.db doesn't exist.
  * Fix windows.h conflict with Criterion::STRICT
  * Cache result of proj_get_type() to help for performance of
    proj_factors
  * createOperations(): improvement for "NAD83(CSRS) + CGVD28 height" to
  "NAD83
  * WKT1 import: correctly deal with missing rectified_grid_angle
    parameter
  * Fix and additional options for Peirce Quincuncial projections
  * Fix build with Intel C++ compiler

* Fri Nov 26 2021 Dirk Müller <dmueller@suse.com>
- update 8.2.0:
  * Added the S2 projection (#2749)
  * Added support for Degree Sign on input (#2791)
  * ESRI WKT: add support for import/export of (non interrupted)
    Goode Homolosine (#2827)
  * Make filemanager aware of UWP Win32 API (#2831)
  * Add proj_create_conversion_pole_rotation_netcdf_cf_convention() to
    address netCDF datasets using a pole rotation method (#2835)
  * Emit better debug message when a grid isn't found (#2838)
  * Add support for GeodeticCRS using a Spherical planetocentric
    coordinate system
  * PROJJSON: support additional properties allowed in id object (version,
  authority_citation, uri) for parity with WKT2:2019 (#2850)
  * Database layout modified to include "anchor" field to geodetic_datum and
  vertical_datum tables, consequently database layout version is increased
  * proj_factors(): accept P to be a projected CRS (#2868)
  * Add IAU_2015 CRS definitions (#2876)
  * CRS::extractGeodeticCRS(): implement for DerivedProjectedCRS (#2877)
  * Added proj_trans_bounds() (#2882)
  * Add fallback strategy for tinshift transform to use closest triangle for
    points not in any (#2907)
  * Database: update to EPSG v10.038 (#2910)
  * Fix O(n^2) performance patterns where n is the number of steps of
    a pipeline (#2820)
  * Detect ESRI WKT better in certain circumstances (#2823)
  * Fix performance issue on pipeline instanciation of huge (broken)
    pipelines (#2824)

* Sun Oct 24 2021 D. Berge <opensuse@navlost.eu>
- Update to version 8.1.1 (data version: 1.7)
  * EPSG Database updated to version 10.028 (#2773)
  * Include algorithm header file to avoid build errors on Alpine Linux (#2769)
  * CMake: fix installation of executables on iOS (#2766)
  * Associate extents to transformations of CRS's that include GEOIDMODEL (#2769)
  * Logging: avoid some overhead when logging is not enabled (#2775)
  * ortho: remove useless and invalid log trace (#2777)
  * CMake: remove external nlohmann_json from INTERFACE_LINK_LIBRARIES target (#2781)
  * reateOperations(): fix SourceTargetCRSExtentUse::NONE mode (#2783)
  * GeoTIFF grid reading: perf improvements (#2788)
  * Conversion::createUTM(): avoid integer overflow (#2796)
  * Inverse laea ellipsoidal: return PROJ_ERR_COORD_TRANSFM_OUTSIDE_PROJECTION_DOMAIN
    when appropriates (#2801)
  * Make sure that proj_crs_promote_to_3D returns a derived CRS (#2806)
  * createOperations(): fix missing deg<-->rad conversion when transforming with a
    CRS that has a fallback-to-PROJ4-string behaviour and is a BoundCRS of a
    GeographicCRS (#2808)
  * WKT2 import/export: preserve PROJ.4 CRS extension string in REMARKS[] (#2812)
  * BoundCRS: accept importing/exporting in WKT2 and PROJJSON the
    scope/area/extent/id attributes (#2815)
  * ConcatenatedOperation::fixStepsDirection(): fix bad chaining of steps when
    inverse map projection is involved in non-final step (#2819)

* Sat Oct 23 2021 D. Berge <opensuse@navlost.eu>
- Update to version 8.1.0 (data version: 1.7)
  * Version 8.1.0
  - Update to EPSG v10.027 (#2751)
  - Decrease DB size by using WITHOUT ROWID tables (#2730) (#2647)
  - Add a ANALYZE step during proj.db creation allowing for
    faster lookups (#2729)
  - Added a PROJ.VERSION metadata entry (#2646)
  - Added NGO48 (EPSG:4273) to ETRS89 (EPSG:4258) triangulation-based
    transformation (#2554)
  - Additions to the norwegian NKG2020 transformation (#2548)
  - ESRI projection database updated to version 12.8 (#2717)
  - Added proj_get_geoid_models_from_database() function that returns a list of
    geoid models available for a given CRS (#2681)
  - Added proj_get_celestial_body_list_from_database that returns a list
    of celestial bodies in the PROJ database (#2667)
  - Added proj_get_celestial_body_name() (#2662)
  - proj_trans/cs2cs: If two operations have the same accuracy,
    use the one that is contained within a larger one (#2750)
  - Share SQLite database handle among all contexts (#2738)
  - Add proj/internal/mutex.hpp as compat layer for mingw32 for std::mutex (#2736)
  - projsync: make it filter out files not intended for the current version (#2725)
  - Improvements related to DerivedVerticalCRS using Change Unit and
    Height/Depth reversal methods (#2696)
  - Update internal nlohmann/json to 3.9.1, and add a CMake option to
    be able to use external nlohmann/json (#2686)
  - createFromUserInput(): change name of CRS built from URN combined references to match
    the convention of EPSG projected CRS (#2677)
  - Parse compound id with two authorities, like ESRI:103668+EPSG:5703 (#2669)
  - Added projinfo option --list-crs (supports --area) (#2663)
  - Added support for hyperbolic Cassini-Soldner (#2637)
  - Added capability to get SQL statements to add custom CRS in the database (#2577)
  - Fix 'Please include winsock2.h before windows.h' warning with msys (#2692)
  - Minor changes to address lint in geodesic.c (#2752)
  - BoundCRS::identify(): avoid incompatible transformation for
    WKT1 / TOWGS84 export (#2747)
  - proj_create(): do not open proj.db if string is a PROJ string,
    even if proj_context_set_autoclose_database() has been set (#2735)
  - Fix export of transformation to PROJ string in a particular situation
    where CompoundCRS are involved (#2721)
  * Version 8.0.1
  - Database: update to EPSG v10.018 (#2636)
  - Add transformations for CHGeo2004, Swiss geoid model (#2604)
  - Additions to the norwegian NKG2020 transformation (#2600)
  - pj_vlog(): fix buffer overflow in case of super lengthy error message (#2693)
  - Revert "proj_create_crs_to_crs_from_pj(): do not use PROJ_SPATIAL_CRITERION_PARTIAL_INTERSECTION
    if area is specified" (#2679)
  - UTM: error out when value of +zone= is not an integer (#2672)
  - getCRSInfoList(): make result order deterministic (by increasing auth_name,
    code) (#2661)
  - createOperation(): make sure no to discard deprecated operations if the
    replacement uses an unknow grid (#2623)
  - Fix build on Solaris 11.4 (#2621)
  - Add mapping of ESRI Equal_Area projection method to EPSG (#2612)
  - Fix incorrect EPGS extent code for EPSG:7789>EPSG:4976 NKG transformation (#2599)
  - fix wrong capitalization of CHENyx06_ETRS.gsb (#2597)
  - createOperations(): improve handling of vertical transforms when
    when compound CRSs are used (#2592)
  - CRS::promoteTo3D(): propagate the extent from the 2D CRS (#2589)
  - createFromCRSCodesWithIntermediates(): improve performance when there is
    no match (#2583)
  - Fix proj_clone() to work on 'meta' coordinate operation PJ* objects that
    can be returned by proj_create_crs_to_crs() (#2582)
  - add PROJ_COMPUTE_VERSION, PROJ_VERSION_NUMBER,
    PROJ_AT_LEAST_VERSION macros (#2581)
  - Make proj_lp_dist() and proj_geod() work on a PJ* CRS object (#2570)
  - Fix gcc 11 -Wnonnull compilation warnings (#2559)
  - Fix use of uninitialized memory in gie tests (#2558)
  - createOperations(): fix incorrect height transformation between 3D promoted RGF93 and CH1903+ (#2555)
  * Version 8.0.0
  - With the release of PROJ 8 the proj_api.h API is finally removed.
  - Several improvements has been made to the command line utilities.
  - Public header file proj_api.h removed (#837)
  - Improved accuracy of the Mercator projection (#2397)
  - Copyright statement wording updated (#2417)
  - Allow cct to instantiate operations via object codes or names (#2419)
  - Allow @filename syntax in cct (#2420)
  - Added geocentric->topocentric conversion (+proj=topocentric) (#2444)
  - Update GeographicLib to version 1.51 (#2445)
  - Added option to allow export of Geographic/Projected 3D CRS
    in WKT1_GDAL (#2450)
  - Added --area and --bbox options in cs2cs to restrict candidate
    coordinate operations (#2466)
  - Added build time option to make PROJ_LIB env var tested last (#2476)
  - Added --authority switch in cs2cs to control where coordinate operations
    are looked for. C API function proj_create_crs_to_crs_from_pj() updated
    accordingly (#2477)
  - Error codes revised and exposed in the public API (#2487)
  - Added --accuracy options to projinfo. C API function
    proj_create_crs_to_crs_from_pj() updated accordingly (#2488)
  - Added proj_crs_is_derived() function to C API (#2496)
  - Enabled linking against static cURL on Windows (#2514)
  - Updated ESRI CRS database to 12.7 (10.8.1/2.6) (#2519)
  - Allow a WKT BoundCRS to use a PROJ string transformation (#2521)
  - Update to EPSG v10.015 (#2539)
  - Default log level set to PJ_LOG_ERROR (#2542)
  - CMake installs a pkg-config file proj.pc, where supported (#2547)
  - Do not restrict longitude to [-90;90] range in spherical transverse Mercator
    forward projection (#2471)
  - createOperations(): fix Compound to Geog3D/Projected3D CRS with non-metre ellipsoidal height (#2500)
  - Avoid error messages to be emitted log level is set to PJ_LOG_NONE (#2527)
  - Close database connection when autoclose set to True (#2532)

* Sat Jan 23 2021 Libor Pechacek <lpechacek@suse.com>
- Replace proj-datumgridwith proj-data. Proj-datumgrid is no
  longer maintained and the stale data make pyproj self-tests fail
  https://github.com/pyproj4/pyproj/issues/769. Proj-data is
  distributed in per-location subpackages.

* Thu Jan  7 2021 Martin Pluskal <mpluskal@suse.com>
- Update to version 7.2.1
  * Add metadata with the version number of the database layout (#2474)
  * Split coordinateoperation.cpp and test_operation.cpp in several parts (#2484)
  * Update to EPSG v10.008 (#2490)
  * Added the NKG 2008 and 2020 transformations in proj.db (#2495)
  * And several bugfixes - see provided NEWS for details

* Wed Nov  4 2020 Libor Pechacek <lpechacek@gmx.com>
- Update to version 7.2.0:
  * Command line tools
  - Add multi-line PROJ string export capability, and use it by
    default in projinfo (unless --single-line is specified)
    (#2381)
  * Coordinate operations
  - +proj=col_urban projection, implementing a EPSG projection
    method used by a number of projected CRS in Colombia
    (#2395)
  - +proj=tinshift for triangulation-based transformations
    (#2344)
  - Added ellipsoidal formulation of +proj=ortho (#2361)
  * Database
  - Update to EPSG 10.003 and make code base robust to dealing
    with WKT CRS with DatumEnsemble (#2370)
  - Added Finland tinshift operations (#2392)
  - Added transformation from JGD2011 Geographic 3D to JGD2011
    height using GSIGEO2011 (#2393)
  - Improve CompoundCRS identification and name morphing in
    VerticalCRS with ESRI WKT1 (#2386)
  - Added OGC:CRS27 and OGC:CRS83 CRS entries for NAD27 and
    NAD83 in longitude, latitude order (#2350)
  * API
  - Added temporal, engineering, and parametric datum
    PJ_TYPE enumerations (#2274)
  - Various improvements to context handling (#2329, #2331)
  - proj_create_vertical_crs_ex(): add a ACCURACY option to
    provide an explicit accuracy, or derive it from the grid
    name if it is known (#2342)
  - proj_crs_create_bound_crs_to_WGS84(): make it work on
    verticalCRS/compoundCRS such as EPSG:4326+5773 and
    EPSG:4326+3855 (#2365)
  - promoteTo3D(): add a remark with the original CRS
    identifier (#2369)
  - Added proj_context_clone (#2383)
  * Bug fixes
  - Avoid core dumps when copying contexts in certain scenarios
    (#2324)
  - proj_trans(): reset errno before attemptying a retry with a
    new coordinate operation (#2353)
  - PROJJSON schema corrected to allow prime meridians values
    with explicitly stating a unit (degrees assumed) (#2354)
  - Adjust createBoundCRSToWGS84IfPossible() and operation
    filtering (for POSGAR 2007 to WGS84 issues) (#2357)
  - createOperations(): several fixes affecting NAD83 ->
    NAD83(2011) (#2364)
  - WKT2:2019 import/export: handle DATUM (at top level object)
    with PRIMEM
  - WKT1_ESRI: fix import and export of CompoundCRS (#2389)

* Tue Sep 15 2020 Libor Pechacek <lpechacek@gmx.com>
- Update to version 7.1.1:
  * Updates
  - Added various Brazillian grids to the database #2277
  - Added geoid file for Canary Islands to the database #2312
  - Updated EPSG database to version 9.8.15 #2310
  * Bug fixes
  - WKT parser: do not raise warning when parsing a WKT2:2015 TIMECRS
    whose TIMEUNIT is at the CS level, and not inside #2281
  - Parse '+proj=something_not_latlong +vunits=' without +geoidgrids as a
    Projected3D CRS and not a compound CRS with a unknown datum #2289
  - C API: Avoid crashing due to missing SANITIZE_CTX() in entry points
    [#2293]
  - CMake build: Check "target_clones" before use #2297
  - PROJ string export of +proj=krovak +czech: make sure we export
    +czech... #2301
  - Helmert 2D: do not require a useless +convention= parameter #2305
  - Fix a few spelling errors ("vgridshit" vs. "vgridshift") #2307
  - Fix ability to identify EPSG:2154 as a candidate for
    'RGF93_Lambert_93' #2316
  - WKT importer: tune for Oracle WKT and 'Lambert Conformal Conic' #2322
  - Revert compiler generated Fused Multiply Addition optimized routines
    [#2328]
- Changelog for 7.1.0
  * New projections:
  - Add square conformal projections from libproject:
    Adams Hemisphere in a Square
    Adams World in a Square I
    Adams World in a Square II
    Guyou
    Pierce Quincuncial
    (#2148)
  - Adams Square II: map ESRI WKT to PROJ string, and implement iterative
    inverse method (#2157)
  - Added IGH Oceanic View projection (#2226)
  - Add wink2 inverse by generic inversion of forward method (#2243)
  * Database:
  - Update to EPSG 9.8.12, ESRI 10.8.1 and import scope and remarks for
    c-nversion (#2238) (#2267)
  - Map the Behrman projection to cae when converting ESRI CRSes (#1986)
  - Support conversion of Flat_Polar_Quartic projection method (#1987)
  - Register 4 new Austrian height grids (see OSGeo/PROJ-data#13) and
    handle 'Vertical Offset by Grid Interp-lation (BEV AT)' method
    (#1989)
  - Add ESRI projection method mappings for Mercator_Variant_A,
    Mercator_Variant_B and Transverse_Cylindrical_Equal_Area and vari-us
    grid mappings (#2020) (#2195)
  - Map ESRI Transverse_Mercator_Complex to Transverse Mercator (#2040)
  - Register grids for New Caledonia (see OSGeo/PROJ-data#16) (#2051)
    (#2239)
  - Register NZGD2000 -> ITRF96 transformation for NZGD2000 database
    (#2248)
  - Register geoid file for UK added
    (see https://github.c-m/OSGeo//PROJ-data/pull/25() (#2250)
  - Register Slovakian geoid transformations with needed code changes
    (#2259)
  - Register Spanish SPED2ETV2 grid for ED50->ETRS89 (#2261)
  * API:
  - Add API function proj_get_units_from_database() (#2065)
  - Add API function proj_get_suggested_operation() (#2068)
  - Add API functions proj_degree_input() and proj_degree_output() (#2144)
  - Moved proj_context_get_url_endpoint &
    proj_context_get_user_writable_directory fr-m proj_experimental.h to
    proj.h (#2162)
  - createFromUserInput(): allow compound CRS with the 2 parts given by
    names, e.g. 'WGS 84 + EGM96 height' (#2126)
  - createOperations(): when converting CompoundCRS<-->Geographic3DCrs,
    do not use discard change -f ellipsoidal height if a Helmert
    transformation is involved (#2227)
  - proj_list_units() deprecated, superceeded by
    proj_get_units_from_database()
  - proj_list_angular_units() deprecated, superceeded by
    proj_get_units_from_database()
  * Optimizations:
  - tmerc/utm: add a +algo=auto/evenden_snyder/poder_engsager parameter
    (#2030)
  - Extended tmerc (Poder/Engsager): speed optimizations (#2036)
  - Approximate tmerc (Snyder): speed optimizations (#2039)
  - pj_phi2(): speed-up computation (and thus inverse ellipsoidal
    Mercator and LCC) (#2052)
  - Inverse cart: speed-up computation by 33%% (#2145)
  - Extended tmerc: speed-up forward path by ~5%% (#2147)
  * Various:
  - Follow PDAL's CMake RPATH strategy (#2009)
  - WKT import/export: add support for WKT1_ESRI VERTCS synta (#2024)
  - projinfo: add a --hide-ballpark option (#2127)
  - gie: implement a strict mode with (#2168)
  - Allow importing WKT1 COMPD_CS with a VERT_DATUM[Ellipsoid,2002]
    (#2229)
  - Add runtime checking that sqlite3 is >= 3.11 (#2235)
  * Bug fixes
  - createOperations(): do not remove ballpark transformation if there
    are only grid based -perations, even if they cover the whole area of
    use (#2155)
  - createFromProjString(): handle default parameters of '+krovak
    +type=crs', and handle +czech correctly (#2200)
  - ProjectedCRS::identify(): fix identification of EPSG:3059 (#2215)
  - Database: add a 'WGS84' alias for the EPSG:4326 CRS (#2218)
  - Fixes related to CompoundCRS and BoundCRS (#2222)
  - Avoid 2 warnings about missing database indices (#2223)
  - Make projinfo --3d --boundcrs-to-wgs84 work better (#2224)
  - Many fixes regarding BoundCRS, CompoundCRS, Geographic3D CRS with
    non-metre units (#2234)
  - Fix identification of (one of the) ESRI WKT formulations of EPSG:3035
    (#2240)
  - Avoid using deprecated and removed Windows API function with Mingw32
    (#2246)
  - normalizeForVisualization(): make it switch axis for EPSG:5482
    (RSRGD2000 / RSPS2000) (#2256)
  - Fix access violation in proj_context_get_database_metadata (#2260)
  - Fail gracefully when calling API functions with invalid input (#2272)

* Sun Jun 14 2020 Martin Pluskal <mpluskal@suse.com>
- Update to version 7.0.1:
  * Database: update to EPSG v9.8.9
  * Make tests independent of proj-datumgrid
  * Add missing projection property tables
  * Avoid crash when running against SQLite3 binary built with -DSQLITE_OMIT_AUTOINIT
  * createOperations(): fix wrong pipeline generation with CRS that has +nadgrids= and +pm=
  * Fix bad copy&replace pattern on HEALPix and rHEALPix projection names
  * createUnitOfMeasure(): use full double resolution for the conversion factor
  * Update README with info on PROJ-data
  * utm/ups: make sure to set errno to PJD_ERR_ELLIPSOID_USE_REQUIRED if es==0
  * data/Makefile.am: remove bashism
  * ProjectedCRS::identify(): tune it to better work with ESRI WKT representation of EPSG:2193
  * Fix build with gcc 4.8.5
  * Autotools/pkg-conf: Define datarootdir
  * cs2cs: don't require +to for '{source_crs} {target_crs} filename...' syntax
  * CMake: fix bug with find_package(PROJ) with macOS
  * ESRI WKT import / identification: special case for NAD_1983_HARN_StatePlane_Colorado_North_FIPS_0501 with Foot_US unit
  * EngineeringCRS: when exporting to WKT1_GDAL, output unit and axis
  * Use jtsk03-jtsk horizontal grid from CDN
  * CMake: prefer to use use PROJ_SOURCE_DIR and PROJ_BINARY_DIR
  * Fix wrong grids file name in esri.sql
  * Fix identification of projected CRS whose name is close but not strictly equal to a ESRI alias
  * Fix working of Helmert transform between the horizontal part of 2 compoundCRS
  * Database: fix registration of custom entries of grid_transformation_custom.sql for geoid grids
  * ESRI_WKT ingestion: make sure to identify to non-deprecated EPSG entry when possible
  * Make sure that importing a Projected 3D CRS from WKT:2019 keeps the base geographic CRS as 3D
  * createOperations(): improve results of compoundCRS to compoundCRS case
  * hgridshift/vgridshift: defer grid opening when grid has already been opened
  * Resolve a few shadowed declaration warnings
  * ProjectedCRS identification: deal with switched 1st/2nd std parallels for LCC_2SP
  * Fix Robinson inverse projection
  * createOperations(): do not remove ballpark transformation if there are only grid based operations, even if they cover the whole area of use
  * createFromCoordinateReferenceSystemCodes(): 'optimization' to avoid using C++ exceptions
  * Ingestion of WKT1_GDAL: correctly map 'Cylindrical_Equal_Area'
  * Add limited support for non-conformant WKT1 LAS COMPD_CS[]
  * PROJ4 string import: take into correctly non-metre unit when the string looks like the one for WGS 84 / Pseudo Mercator
  * io.hpp: avoid dependency to proj_json_streaming_writer.hpp
  * Fix support of WKT1_GDAL with netCDF rotated pole formulation

* Tue Mar 31 2020 Martin Pluskal <mpluskal@suse.com>
- Update to version 7.0.0:
  * Added new file access API to proj.h #866
  * Updated the name of the most recent version of the WKT2 standard from
    WKT2_2018 to WKT2_2019 to reflect the proper name of the standard (#1585)
  * Improvements in transformations from/to WGS 84 (Gxxxx) realizations and
    vertical <--> geog transormations #1608
  * Update to version 1.50 of the geodesic library (#1629)
  * Promote proj_assign_context to proj.h from proj_experimental.h (#1630)
  * Add rotation support to the HEALPix projection (#1638)
  * Add c function proj_crs_create_bound_vertical_crs() (#1689)
  * Use Win32 Unicode APIs and expect all strings to be UTF-8 (#1765)
  * Improved name aliases lookup (#1827)
  * CMake: Employ better use of CTest with the BUILD_TESTING option (#1870)
  * Grid correction: fix handling grids spanning antimeridian (#1882)
  * Remove legacy CMake target name "proj" #1883
  * projinfo: add --searchpaths switch (#1892)
  * Add +proj=set operation to set component(s) of a coordinate to a fixed
    value (#1896)
  * Add EPSG records for 'Geocentric translation by Grid Interpolation (IGN)'
    (gr3df97a.txt) and map them to new +proj=xyzgridshift (#1897)
  * Remove 'null' grid file as it is now a special hardcoded case in grid
    code (#1898)
  * Add projsync utility (#1903)
  * Make PROJ the CMake project name #1910
  * Use relative directory to locate PROJ resource files (#1921)

* Mon Mar  9 2020 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Update to 6.3.1:
  * Updates
  - Update the EPSG database to version 9.8.6
  - Database: add mapping for gg10_smv2.mnt and gg10_sbv2.mnt French grids
  - Database: add mapping for TOR27CSv1.GSB
  * Bug fixes
  - Fix wrong use of derivingConversionRef() that caused issues with use of
    +init=epsg:XXXX by GDAL (affecting R spatial libraries) or in MapServer
  - fix exporting CoordinateSystem to PROJ JSON with ID
  - projinfo: use No. abbreviation instead of UTF-8 character (#1828)
  - CompoundCRS::identify(): avoid exception when horiz/vertical part is a
    BoundCRS
  - createOperations(): fix dealing with projected 3D CRS whose Z units != metre
  - WKT1_GDAL export: limit datum name massaging to names matching EPSG (#1835)
  - unitconvert with mjd time format: avoid potential integer overflow
    (ossfuzz 20072)
  - ProjectedCRS::identify(): fix wrong identification of some ESRI WKT linked
    to units
  - Database: add a geoid_like value for proj_method column of grid_alternatives,
    fix related entries and simplify/robustify logic to deal with EPSG
    'Geographic3D to GravityRelatedHeight' methods
  - Fix ingestion of +proj=cea with +k_0 (#1881)
  - Fix performance issue, affecting PROJ.4 string generation of EPSG:7842
    (#1913)
  - Fix identification of ESRI-style datum names starting with D_ but without
    alias (#1911)
  - cart: Avoid discontinuity at poles in the inverse case (#1906)
  - Various updates to make regression test suite pass with gcc on i386 (#1906)
- Changleog from 6.3.0:
  * Updates
  - Database: tune accuracy of Canadian NTv1 file w.r.t NTv2 (#1812)
  - Modify verbosity level of some debug/trace messages (#1811)
  - projinfo: no longer call createBoundCRSToWGS84IfPossible() for WKT1:GDAL
    (#1810)
  - proj_trans: add retry logic to select other transformation if the best one
    fails. (#1809)
  - BoundCRS::identify(): improvements to discard CRS that aren't relevant
    (#1802)
  - Database: update to IGNF v3.1.0 (#1785)
  - Build: Only export symbols if building DLL (#1773)
  - Database: update ESRI entries with ArcGIS Desktop version 10.8.0 database
    (#1762)
  - createOperations(): chain operations whose middle CRSs are not identical but
    have the same datum (#1734)
  - import/export PROJJSON: support a interpolation_crs key to geoid_model
    (#1732)
  - Database: update to EPSG v9.8.4 (#1725)
  - Build: require SQLite 3.11 (#1721)
  - Add support for GEOIDMODEL (#1710)
  - Better filtering based on extent and performance improvements (#1709)
  * Bug fixes
  - Horizontal grid shift: fix issue on iterative inverse computation when
    switching between (sub)grids (#1797)
  - createOperations(): make filtering out of 'uninteresting' operations less
    aggressive (#1788)
  - Make EPSG:102100 resolve to ESRI:102100 (#1786)
  - ob_tran: restore traditional handling of +to_meter with pj_transform() and
    proj utility (#1783)
  - CRS identification: use case insensitive comparison for authority name
    (#1780)
  - normalizeForVisualization() and other methods applying on a ProjectedCRS: do
    not mess the derivingConversion object of the original object (#1746)
  - createOperations(): fix transformation computation from/to a CRS with
    +geoidgrids and +vunits != m (#1731)
  - Fix proj_assign_context()/pj_set_ctx() with pipelines and alternative coord
    operations (#1726)
  - Database: add an auxiliary concatenated_operation_step table to allow
    arbitrary number of steps (#1696)
  - Fix errors running gie-based tests in Debug mode on Windows (#1688)

* Tue Nov  5 2019 Angelos Tzotsos <tzotsos@opensuse.org>
- Update to version 6.2.1:
  * Update the EPSG database to version 9.8.2
  * Fixed erroneous spelling of "Potsdam" (#1573)
  * Calculate y-coordinate correctly in bertin1953 in all cases (#1579)
  * proj_create_crs_to_crs_from_pj(): make the PJ* arguments const PJ* (#1583)
  * PROJStringParser::createFromPROJString(): avoid potential infinite recursion (#1574)
  * Avoid core dump when setting ctx==NULL in functions proj_coordoperation_is_instantiable and
  * proj_coordoperation_has_ballpark_transformation (#1590)
  * createOperations(): fix conversion from/to PROJ.4 CRS strings with non-ISO-kosher options and +towgs84/+nadgrids (#1602)
  * proj_trans_generic(): properly set coordinate time to HUGE_VAL when no value is passed to the function (#1604)
  * Fix support for +proj=ob_tran +o_proj=lonlat/latlong/latlon instead of only only allowing +o_proj=longlat (#1601)
  * Improve backwards compatibility of vertical transforms (#1613)
  * Improve emulation of deprecated +init style initialization (#1614)
  * cs2cs: autopromote CRS to 3D when there's a mix of 2D and 3D (#1563)
  * Avoid divisions by zero in odd situations (#1620)
  * Avoid compile error on Solaris (#1639)
  * proj_create_crs_to_crs(): fix when there are only transformations with ballpark steps (#1643)
  * PROJ string CRS ingester: recognize more unit-less parameters, and handling of +key=string_value parameters (#1645)
  * Only call pkg-config in configure when necessary (#1652)
  * aeqd: for spherical forward path, go to higher precision ellipsoidal case when the point coordinates are super close to the origin (#1654)
  * proj_create_crs_to_crs(): remove elimination of Ballpark operations that caused transformation failures in some cases (#1665)
  * createOperations(): allow transforming from a compoundCRS of a bound verticalCRS to a 2D CRS (#1667)
  * Avoid segfaults in case of out-of-memory situations (#1679)
  * createOperations(): fix double vertical unit conversion from CompoundCRS to other CRS when the horizontal part of the projected CRS uses non-metre unit (#1683)
  * importFromWkt(): fix axis orientation for non-standard ESRI WKT (#1690)

* Tue Oct 29 2019 Angelos Tzotsos <tzotsos@opensuse.org>
- Fix Leap build target

* Fri Sep 27 2019 Martin Pluskal <mpluskal@suse.com>
- Update to version 6.2.0:
  * Introduced PROJJSON, a JSON encoding of WKT2 (#1547)
  * Support CRS instantiation of OGC URN's (#1505)
  * Expose scope and remarks of database objects (#1537)
  * EPSG Database updated to version 9.7.0 (#1558)
  * Added C API function proj_grid_get_info_from_database() (#1494)
  * Added C API function
    proj_operation_factory_context_set_discard_superseded() (#1534)
  * Added C API function proj_context_set_autoclose_database() (#1566)
  * Added C API function proj_create_crs_to_crs_from_pj() (#1567)
  * Added C API function proj_cleanup() (#1569)
  * Fixed build failure on Solaris systems (#1554)

* Wed Jun 12 2019 Martin Pluskal <mpluskal@suse.com>
- Update to version 6.1.0:
  * See provided NEWS for list of all changes

* Mon Apr  1 2019 Kai Pastor <dg0yt@darc.de>
- Fix datumgrid packaging

* Mon Mar 25 2019 Martin Pluskal <mpluskal@suse.com>
- Enable tests
- Fix previous changelog entry

* Mon Mar 11 2019 Martin Pluskal <mpluskal@suse.com>
- Update to version 6.0.0 and datumgrid 1.7
  * See provided NEWS for list of all changes

* Wed Sep 19 2018 Martin Pluskal <mpluskal@suse.com>
- Update to version 5.2.0 and datumgrid 1.7
  * See provided NEWS for list of all changes

* Thu Jul 12 2018 mpluskal@suse.com
- Update to version 5.1.0 and datumgrid 1.7
  * See provided NEWS for list of all changes

* Sun Oct  2 2016 tzotsos@opensuse.org
- Update to 4.9.3
  o update to new datumgrid version 1.6

* Fri Sep 30 2016 tzotsos@opensuse.org
- Switch download link to OSGeo server

* Mon Jul  4 2016 mpluskal@suse.com
- Update project and download url
- Small spec file cleanups

* Sun Sep 27 2015 mpluskal@suse.com
- Update to 4.9.2
  o proj_def.dat was missing from source distribution
    see https://github.com/OSGeo/proj.4/issues/274 for more detail
  o Update Geodesic library from GeographicLib
  o Remove setlocale() use in pj_init_ctx()
  o Renamed PVALUE in pj_param.c to prevent clash with Windows

* Sat May  9 2015 mpluskal@suse.com
- Update to 4.9.1
  o 4.9.0RC2 release was abandoned because it was not promoted in a
    timely fashion. Subsequent maintenance of tickets has continued,
    and a new 4.9.1 release was issued in its place.
  o Implement inverse solution for Winkel Tripel from Drazan Tutic #250
  o More CMake configuration tweaks. The CMake configuration is probably
    not at feature parity with the autotools builds at this point but it
    is converging #256
  o Tweak initialization ordering around setlocal which may have caused
    issues #237
  o Support out-of-tree autoconf builds more completely #247
  o Fix NaN handling by geod_inverse and geod_polygon_addedge #251 & #253
  o Update config.sub and config.guess #257
  o Adapt Charles Karney's CMake patches for smoother build #258
  o Define default PROJ_LIB location for CMake compilation #261
  o Fix Windows compilation on PJ_aitoff.c
  o Align CMake SOVERSION with autotools #263
  o Regenerate nad/epsg with GDAL r28536 to avoid precision loss in TOWGS84
    parameters, e.g. on Amersfoort / RD EPSG:4289 (#260)
  o Add CMake project-config.cmake scripts (#264 from Charles Karney)
  o Dial back test sensitivity #255
- Changes for 4.9.0
  o Implement CMake as an option for building PROJ.4
  o Implement new virtual file api (projFileAPI) so that all access to grid
    shift and init files can be hooked.
  o Replace geodesic implementation with one from Charles Karney and add a
    supported public interface (geodesic.h).
  o Upgraded to EPSG 8.5.
  o Removed old (deprecated) Java bindings in favor of the new api introduced
    in 4.8.0.
  o Implement the calcofi (Cal Coop Ocean Fish Invest Lines/Stations) projection
  o Install projects.h again for applications that want access to internal
    structures and functions despite the inherent fragility.
  o Various bug fixes and cleanup.
  o Added the CalCOFI pseudo-projection, #135

* Sun Mar  8 2015 mpluskal@suse.com
- Cleanup spec file with spec-cleaner
- Cleanup dependecies
- Use url for source
- Update url

* Fri Apr 20 2012 tzotsos@opensuse.org
- minor fix to install projects.h needed in devel package.

* Wed Mar 14 2012 dassau@gbd-consult.de
- update to version 4.8.0
  - Added the Natural Earth projection.
  - Added HEALPIX, rHEALPIX and Icosahedral Snyder Equal Area projections.
  - nad2bin now produces "CTable2" format grid shift files by default which
  are platform independent.
  - nad2nad removed, use cs2cs for datum shift operations.
  - projects.h no longer installed as a public include file.  Please try to
  only use proj_api.h.
  - Add pj_get_spheroid_defn() accessor.
  - Added an alternate version of pj_init() that takes a projCtx (execution
  context) structure to address multithreading issues with error management
  and to provide a support for application hookable error reporting and
  logging.
  - Upgrade to EPSG 7.9.  Some changes in ideal datum selection.
  - JNI bindings reworked, org.proj4.Projections deprecated in favor of
  org.proj4.PJ.
  - Added preliminary vertical datum support.
  - Fix various multithreading issues, particular in datum grid handling code.
  - Added support for the +axis= option for alternate axis orientations as
  part of a coordinate system (used for TM South Orientated support).
  - +proj=omerc implementatioin replaced with code from libproj4.  +rot_conv
  flag no longer works, and some coordinate systems (ie. Malaysian) will
  need to use +gamma instead.  "epsg" init file updated accordingly.
- Added BuildRequires pkg-config
- Added %%{_libdir}/pkgconfig/proj.pc

* Thu Aug 18 2011 idonmez@novell.com
- Remove wrong -static-devel package

* Thu Aug 18 2011 otto.dassau@gmx.de
- added a static devel package, because GRASS and QGIS don't find
  the external PROJ.4 data directory anymore
  Sat Mar 19 00:00:00 UTC 2011 - Otto Dassau 4.7.0
- removed debug_package
  Tue Nov 24 00:00:00 UTC 2009 - Otto Dassau 4.7.0
- update to new proj4 version
- update to new datumgrid version 1.5

* Sun Oct 19 2008 dl9pf@gmx.de
- change spec to build on factory
  Wed Sep 17 00:00:00 UTC 2008 - Otto Dassau 4.6.1
- version update
  Wed Jul  9 00:00:00 UTC 2008 - Otto Dassau 4.6.0
- update and rpmlind fixes
  Mon Aug 13 00:00:00 UTC 2007 - Dirk Stöcker 4.5.0
- adapted to BuildService
  Fri Jan  5 00:00:00 UTC 2007 - Otto Dassau 4.5.0
- moved *.so from files devel to files
  Tue Dec 19 00:00:00 UTC 2006 - Otto Dassau 4.5.0
- rebuilt for SuSE 10.2
  Wed Jan 25 00:00:00 UTC 2006 - Otto Dassau 4.4.9
- rebuilt for SuSE 10.0 and added devel package
  Thu Nov 17 00:00:00 UTC 2005 - Markus Neteler 4.4.9
- upgraded to Mandriva 2006
  Fri Aug  5 00:00:00 UTC 2005 - Otto Dassau 4.4.9
- Applied for Mandrake 10.1 RPM
