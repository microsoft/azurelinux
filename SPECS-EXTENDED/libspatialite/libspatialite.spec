Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          libspatialite
Version:       5.0.1
Release:       16%{?dist}
Summary:       Enables SQLite to support spatial data

License:       MPLv1.1 or GPLv2+ or LGPLv2+
URL:           https://www.gaia-gis.it/fossil/libspatialite
Source0:       http://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Move private libs to Libs.private in pkg-config file (#1926868)
Patch0:        libspatialite_pkgconfig.patch
# Fix mingw detection in configure.ac
Patch1:        libspatialite_mingw.patch
# Fix obsolete macros
Patch2:        libspatialite_macros.patch
# Use pkgconfig to find geos
Patch3:        libspatialite_geos.patch

BuildRequires: autoconf automake libtool
BuildRequires: freexl-devel
BuildRequires: gcc
BuildRequires: geos-devel >= 3.7.1
BuildRequires: librttopo-devel
BuildRequires: libxml2-devel
BuildRequires: make
BuildRequires: minizip-devel
BuildRequires: proj-devel >= 6.2.0
BuildRequires: sqlite-devel
BuildRequires: zlib-devel


%description
SpatiaLite is a a library extending the basic SQLite core in order to
get a full fledged Spatial DBMS, really simple and lightweight, but
mostly OGC-SFS compliant.


%package devel
Summary:	Development libraries and headers for SpatiaLite
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n %{name}-%{version}
autoreconf -ifv

# Need to copy testdata into builddir
mkdir build_native
cp -a test build_native


%build
# Native build
pushd build_native
%global _configure ../configure
%configure \
    --disable-static \
    --enable-geocallbacks   \
    --enable-rttopo \
    --enable-gcp
%make_build
popd


%install
%make_install -C build_native

find %{buildroot} -type f -name "*.la" -delete


%check
make check  -C build_native %{?_smp_mflags} || :


%files
%doc AUTHORS
%license COPYING
%{_libdir}/%{name}.so.7*
%{_libdir}/mod_spatialite.so.7*
# The symlink must be present to allow loading the extension
# https://groups.google.com/forum/#!topic/spatialite-users/zkGP-gPByXk
%{_libdir}/mod_spatialite.so

%files devel
%doc examples/*.c
%{_includedir}/spatialite.h
%{_includedir}/spatialite
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/spatialite.pc


%changelog
* Thu Aug 03 2023 Archana Choudhary <archana1@microsoft.com> - 5.0.1-16
- Initial CBL-Mariner import from Fedora (license: MIT).

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-14
- Rebuild with mingw-gcc-12

* Wed Mar 09 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-13
- Rebuild for proj-9.0.0

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-12
- Make mingw subpackages noarch

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-11
- Add mingw subpackage

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 21 2021 Sandro Mani <manisandro@gmail.com> - 5.0.1-9
- Rebuild (geos)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 24 2021 Sandro Mani <manisandro@gmail.com> - 5.0.1-7
- Bump

* Sun Mar 07 2021 Sandro Mani <manisandro@gmail.com> - 5.0.1-6
- Rebuild (proj)

* Sat Feb 13 2021 Sandro Mani <manisandro@gmail.com> - 5.0.1-5
- Rebuild (geos)

* Wed Feb 10 2021 Sandro Mani <manisandro@gmail.com> - 5.0.1-4
- Use %%autosetup

* Wed Feb 10 2021 Sandro Mani <manisandro@gmail.com> - 5.0.1-2
- Move private libs to Libs.private in pkg-config file (#1926868)

* Tue Feb 09 2021 Miro Hrončok <mhroncok@redhat.com> - 5.0.1-2
- Rebuilt for minizip 3.0.0

* Mon Feb 08 2021 Sandro Mani <manisandro@gmail.com> - 5.0.1-1
- Update to 5.0.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 13 2020 Sandro Mani <manisandro@gmail.com> - 5.0.0-3
- Enable RTTOPO and GCP

* Thu Nov  5 17:46:32 CET 2020 Sandro Mani <manisandro@gmail.com> - 5.0.0-2
- Rebuild (proj)

* Mon Nov 2 2020 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-1
- Update to 5.0.0
- Remove patches, no longer needed.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-beta0_1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-beta0_1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 4 2019 Devrim Gunduz <devrim@gunduz.org> - 5.0.0beta0-1
- Update to 5.0.0beta0 for new Proj

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 5 2019 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-11
- Rebuilt against Proj 5.2.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 08 2017 Merlin Mathesius <mmathesi@redhat.com> - 4.3.0a-7
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-3
- Rebuilt against Proj 4.9.3.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 17 2015 Volker Froehlich <volker27@gmx.at> - 4.3.0a-1
- New upstream release

* Fri Jul  3 2015 Volker Fröhlich <volker27@gmx.at> - 4.3.0-1
- New upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 12 2015 Devrim Gunduz <devrim@gunduz.org> - 4.2.0-4
- Rebuilt against Proj 4.9.1.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 29 2014 Volker Fröhlich <volker27@gmx.at> - 4.2.0-2
- libxml2 default is now "yes"
- Disable geos support for EL5, as geos 3.2 is no longer supported
- Move the mod_spatialite symlink to the main package

* Fri Jul 25 2014 Peter Robinson <pbrobinson@fedoraproject.org> 4.2.0-1
- Update to 4.2.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 23 2014 Volker Fröhlich <volker27@gmx.at> - 4.1.1-2
- Update for EPEL 7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  1 2013 Volker Fröhlich <volker27@gmx.at> - 4.1.1-1
- New upstram release

* Thu Jun 27 2013 Volker Fröhlich <volker27@gmx.at> - 4.1.0-2
- Temporarily disable lwgeom features to break the circular
  dependency between gdal -- libspatialite -- postgis -- gdal

* Tue Jun  4 2013 Volker Fröhlich <volker27@gmx.at> - 4.1.0-1
- New upstream release

* Mon Apr  8 2013 Volker Fröhlich <volker27@gmx.at> - 4.0.0-3
- Disable hexgrid22 test on 32 bit systems
- Disable tests on ARM

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec  1 2012 Volker Fröhlich <volker27@gmx.at> - 4.0.0-1
- New upstream release
- Remove arch restrictions, solving BZ 663938 and 846301
- Update conditional for geosadvanced

* Sat Aug 18 2012 Volker Fröhlich <volker27@gmx.at> - 3.1.0-0.3.RC2
- Add ppc to excluded archs (BZ #846301)
- Don't build with profiling

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-0.2.RC2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Volker Fröhlich <volker27@gmx.at> - 3.1.0-0.1.RC2
- Add pkconfig as Requirement to the devel sub-package
- Drop freexl patch (solved), build with Freexl
- Update descriptions and summaries
- Re-design conditionals for build flags
- Don't run checks if built without advancedgeos
- Include examples as documentation

* Sat Jan 14 2012 Volker Fröhlich <volker27@gmx.at> - 3.0.1-1
- New upstream release
- Drop defattr
- Run tests
- Own spatialite include-dir
- Add GPLv2+ and LGPLv2+ as alternative licenses
- Update URL and source URL
- Reduce build conditions to EPEL or not
- Use isa macro in base package Requires

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-0.7.RC4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-0.6.RC4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 7 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.5.RC4
- Corrected wrong Fedora version number in if-statement

* Sun Dec 5 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.4.RC4
- Refined configure condition to support RHEL

* Fri Dec 3 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.3.RC4
- Added buildroot
- Added doc files

* Wed Dec 1 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.2.RC4
- Added description of devel package
- Switched to disable-static flag

* Sun Nov 28 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.1.RC4
- Initial packaging for Fedora
