Summary:        GeoTIFF format library
Name:           libgeotiff
Version:        1.7.1
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://trac.osgeo.org/geotiff/
Source:         https://download.osgeo.org/geotiff/%{name}/%{name}-%{version}.tar.gz
# Honour LIB_SUFFIX
# Honour GEOTIFF_INCLUDE_SUBDIR
# Add version suffix to mingw library
# Fix cmake module install dir
# Don't install docs
Patch0:         libgeotiff_cmake.patch
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  proj-devel
BuildRequires:  zlib-devel

%description
GeoTIFF represents an effort by over 160 different remote sensing,
GIS, cartographic, and surveying related companies and organizations
to establish a TIFF based interchange format for georeferenced
raster imagery.

%package devel
Summary:        Development library and header for the GeoTIFF file format library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libtiff-devel
Requires:       pkgconfig

%description devel
The GeoTIFF library provides support for development of geotiff image format.

%prep
%autosetup -p1 -n %{name}-%{version}


%build
# Native build
%cmake -DGEOTIFF_BIN_SUBDIR=bin -DGEOTIFF_INCLUDE_SUBDIR=include/%{name} -DGEOTIFF_LIB_SUBDIR=%{_lib}
%cmake_build


%install
%cmake_install


# install pkgconfig file
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
cat > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/%{name}

Name: %{name}
Description: GeoTIFF file format library
Version: %{version}
Libs: -L\${libdir} -lgeotiff
Cflags: -I\${includedir}
EOF

%check
%ctest


%files
%license LICENSE
%doc ChangeLog
%{_bindir}/applygeo
%{_bindir}/geotifcp
%{_bindir}/listgeo
%{_bindir}/makegeo
%{_libdir}/%{name}.so.5*
%{_mandir}/man1/*.1*

%files devel
%{_includedir}/%{name}/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/GeoTIFF/

%changelog
* Wed Aug 09 2023 Archana Choudhary <archana1@microsoft.com> - 1.7.1-5
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified
- Remove mingw build conditional execution statements

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 10 2022 Orion Poplawski <orion@nwra.com> - 1.7.1-3
- Make mingw build conditional, disable for EL9

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.7.1-2
- Rebuild with mingw-gcc-12

* Mon Mar 14 2022 Sandro Mani <manisandro@gmail.com> - 1.7.1-1
- Update to 1.7.1

* Wed Mar 09 2022 Sandro Mani <manisandro@gmail.com> - 1.7.0-8
- Rebuild for proj-9.0.0

* Tue Mar 08 2022 Sandro Mani <manisandro@gmail.com> - 1.7.0-7
- Fix broken mingw pkg-config files

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 1.7.0-6
- Make mingw subpackages noarch

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 1.7.0-5
- Add mingw subpackage

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 06 2021 Sandro Mani <manisandro@gmail.com> - 1.7.0-1
- Update to 1.7.0

* Sun Mar 07 2021 Sandro Mani <manisandro@gmail.com> - 1.6.0-5
- Rebuild (proj)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 00:10:50 CET 2020 Sandro Mani <manisandro@gmail.com> - 1.6.0-3
- Rebuild (proj)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 12 2020 Sandro Mani <manisandro@gmail.com> - 1.6.0-1
- Update to 1.6.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 5 2019 Devrim Gündüz <devrim@gunduz.org> - 1.4.3-3
- Rebuild for Proj 5.2.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Volker Fröhlich <volker27@gmx.at> - 1.4.3-1
- New upstream version
- Remove ldconfig scriptlets
- Remove unnecessary attrs
- Simplify file list
- Remove mostly build-related README
- Disable apparently pointless debug build
- Remove obsolete Group tag
- No longer mangle data files

* Thu Aug 02 2018 Volker Fröhlich <volker27@gmx.at> - 1.4.0-14
- Add gcc-c++ as BR

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-8
- Rebuild for Proj 4.9.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 29 2015 Volker Fröhlich <volker27@gmx.at> - 1.4.0-6
- Install the real makegeo binary, also solving BZ #1235027
- Re-enable multiple compiler workers
- Actually build with -O2
- Remove outdated prep-section changes
- Remove rpaths

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-4
- Rebuild for Proj 4.9.1

* Wed Jan 07 2015 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-3
- move patching to %%prep section
- explicitly track lib soname so bumps aren't a surprise
- exclude libgeotiff.la file from packaging
- %%configure --disable-static

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0
- Removed patches. No longer applicable.
- Update URL
- Update download URL

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 27 2014 Volker Fröhlich <volker27@gmx.at> - 1.2.5-14
- Support aarch64 (BZ #925739)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.2.5-11
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.2.5-10
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 10 2012 Volker Fröhlich <volker27@gmx.at> - 1.2.5-8
- Add isa macro
- Harmonize buildroot/RPM_BUILD_ROOT
- Replace install macro, use name macro where suitable
- Improve devel sub-package description
- Remove defattr
- Rebuild for libtiff 4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1.2.5-4
- Fix FTBFS: use gcc -shared instead of ld -shared to compile with -fstack-protector

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 15 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.5-2
- disable smp build for koji

* Mon Sep 15 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.5-1
- new bugfix release

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.4-3
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.4-2
- Fix multilib issue by removal of datetime in doxygen footers

* Sun Jan 06 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.4-1
- Rebuild for final release.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.2.4-0.5.rc1
- Rebuild for selinux ppc32 issue.

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 1.2.4-0.4.rc1
- Rebuild for RH #249435

* Tue Jul 24 2007 Balint Cristian <cbalint@redhat.com> 1.2.4-0.3.rc1
- codes are under MIT
- pkg-config cflags return fix
- epsg_csv ownership

* Mon Jul 23 2007 Balint Cristian <cbalint@redhat.com> 1.2.4-0.2.rc1
- fix debuginfo usability
- move header files to the subdirectory
- specify the full URL of the source
- leave *.inc headers included
- libgeotiff-devel should require libtiff-devel
- works to keep timestamps on the header files installed
- docs proper triage

* Mon Jul 23 2007 Balint Cristian <cbalint@redhat.com> 1.2.4-0.1.rc1
- initial pack for fedora
- add pkgconfig file
- add soname versioning patch
