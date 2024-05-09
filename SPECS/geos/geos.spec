Summary:        GEOS is a C++ port of the Java Topology Suite
Name:           geos
Version:        3.12.1
Release:        1%{?dist}
License:        LGPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://trac.osgeo.org/geos/
Source0:        https://download.osgeo.org/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc-c++

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

%package devel
Summary:        Development files for GEOS
Requires:       %{name} = %{version}-%{release}

%description devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid().

This package contains the development files to build applications that
use GEOS.

%prep
%autosetup

%build
# Native build
%cmake -DDISABLE_GEOS_INLINE=ON -DBUILD_DOCUMENTATION=ON
%cmake_build

%install
%cmake_install
make docs -C %{__cmake_builddir}

%check
%ctest

%files
%doc AUTHORS NEWS.md README.md
%license COPYING
%{_bindir}/geosop
%{_libdir}/libgeos.so.3.12.1
%{_libdir}/libgeos_c.so.1*

%files devel
%doc %{__cmake_builddir}/doxygen/doxygen_docs
%{_bindir}/geos-config
%{_includedir}/geos/
%{_includedir}/geos_c.h
%{_includedir}/geos.h
%{_libdir}/libgeos_c.so
%{_libdir}/libgeos.so
%{_libdir}/cmake/GEOS/
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Feb 09 2024 Aditya Dubey <adityadubey@microsoft.com> - 3.12.1
- Upgrading to version 3.12.1 for mariner 3.0

* Tue Feb 14 2023 Sindhu Karri <lakarri@microsoft.com> - 3.11.1-4
- Initial CBL-Mariner import from Fedora 38 (license: MIT)
- Removed building for mingw environment
- License verified
- Updated geos project URL from http to https
- Remove macro referencing unsupported arch s390x in run check tests

* Tue Jan 24 2023 Sandro Mani <manisandro@gmail.com> - 3.11.1-3
- Add geos_gcc13.patch

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 14 2022 Sandro Mani <manisandro@gmail.com> - 3.11.1-1
- Update to 3.11.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 01 2022 Sandro Mani <manisandro@gmail.com> - 3.11.0-1
- Update to 3.11.0

* Mon Jun 06 2022 Sandro Mani <manisandro@gmail.com> - 3.10.3-1
- Update to 3.10.3

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-5
- Rebuild with mingw-gcc-12

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-4
- Make mingw subpackages noarch

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-3
- Add mingw subpackages

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-1
- Update to 3.10.2

* Tue Nov 02 2021 Sandro Mani <manisandro@gmail.com> - 3.10.1-1
- Update to 3.10.1

* Thu Oct 21 2021 Sandro Mani <manisandro@gmail.com> - 3.10.0-2
- Disable inline

* Thu Oct 21 2021 Sandro Mani <manisandro@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 17 2021 Sandro Mani <manisandro@gmail.com> - 3.9.1-4
- Backport fix for performance regression (#1972892)

* Tue Mar 23 2021 Sandro Mani <manisandro@gmail.com> - 3.9.1-3
- Bump

* Wed Mar 10 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.9.1-2
- Fix RHBZ#1937424 (Wrong output from geos-config --libs etc.)
- Fix RHBZ#1937443 (Wrong output from pkgconf geos --libs etc.)

* Thu Feb 11 2021 Sandro Mani <manisandro@gmail.com> - 3.9.1-1
- Update to 3.9.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-1
- Update to 3.9.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.1-2
- Remove ttmath in favour of DD (#1841335)

* Wed Mar 11 2020 Sandro Mani <manisandro@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 03 2020 Sandro Mani <manisandro@gmail.com> - 3.8.0-2
- Install libgeos.so

* Thu Feb 20 2020 Sandro Mani <manisandro@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Devrim Gündüz <devrim@gunduz.org> - 3.7.1-1
- Update to 3.7.1

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.1-11
- Subpackage python2-geos has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Wed Jul 25 2018 Devrim Gündüz <devrim@gunduz.org> - 3.6.1-10
- Fix #1606885

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.6.1-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.6.1-6
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.6.1-5
- Python 2 binary package renamed to python2-geos
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Devrim Gündüz <devrim@gunduz.org> - 3.6.1-1
- Update to 3.6.1
- Remove -php subpackage, it is now a separate project.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Apr  5 2016 Tom Hughes <tom@compton.nu> - 3.5.0-3
- Patch FTBFS with gcc 6. Fixes #1305276 .

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 13 2015 Devrim GUNDUZ <devrim@gunduz.org> - 3.5.0-1
- Update to 3.5.0, per changes described at:
  https://trac.osgeo.org/geos/browser/tags/3.5.0/NEWS
- Add swig as BR to python subpackage, as it does not build without that.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.4.2-5
- Rebuilt for GCC 5 C++11 ABI change

* Thu Feb 26 2015 Orion Poplawski <orion@cora.nwra.com> - 3.4.2-4
- Rebuild for gcc 5 C++11 ABI

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 11 2013 Devrim GUNDUZ <devrim@gunduz.org> - 3.4.2-1
- Update to 3.4.2, per changes described in:
  https://trac.osgeo.org/geos/browser/tags/3.4.2/NEWS
- Remove Patch2, it is now in upstream.
- Disable ruby bindings
- Remove all conditionals -- no more RHEL 4!

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Vít Ondruch <vondruch@redhat.com> - 3.3.8-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Mar 6 2013 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.8-1
- Update to 3.3.8, per changes described in:
  https://trac.osgeo.org/geos/browser/tags/3.3.8/NEWS

* Fri Jan 25 2013 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.7-1
- Update to 3.3.7, per changes described in:
  https://trac.osgeo.org/geos/browser/tags/3.3.7/NEWS

* Fri Nov 16 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.6-1
- Update to 3.3.6, per changes described in:
  https://trac.osgeo.org/geos/browser/tags/3.3.6/NEWS

* Tue Nov 13 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.5-1
- Update to 3.3.5
- Remove patch3, already in upstream.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Vít Ondruch <vondruch@redhat.com> - 3.3.2-2
- Rebuilt for Ruby 1.9.3.
- Rebuilt for PHP 5.4.

* Mon Jan 09 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.2-1
- Update to 3.3.2

* Tue Dec 27 2011 Rex Dieter <rdieter@fedoraproject.org> 3.3.1-3
- track soname so abi bumps aren't a surprise

* Tue Oct 18 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.1-2
- Enable PHP bindings, per Peter Hopfgartner, bz #746574

* Tue Oct 4 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.1-1
- Update to 3.3.1

* Wed Jun 1 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.0-1
- Update to 3.3.0
- Remove 2 patches.

* Mon May 9 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.2.2-1
- Update to 3.2.2
- Add a patch to fix builds on ARM, per bz #682538

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 21 2010 Dan Horák <dan[at]danny.cz> - 3.2.1-2
- fix build with swig 2.0.0

* Tue Mar 30 2010 Devrim GUNDUZ <devrim@gunduz.org> - 3.2.1-1
- Update to 3.2.1

* Thu Mar 18 2010 Balint Cristian <cristian.balint@gmail.com> - 3.2.0-2
- fix bz#473975

* Sun Dec 20 2009 Devrim GUNDUZ <devrim@gunduz.org> - 3.2.0-1
- Update to 3.2.0

* Thu Dec 03 2009 Devrim GÜNDÜZ <devrim@gunduz.org> - 3.2.0-rc3_1.1
- Fix spec (dep error).

* Wed Dec 2 2009 Devrim GUNDUZ <devrim@gunduz.org> - 3.2.0rc3-1
- Update to 3.2.0 rc3

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Devrim GUNDUZ <devrim@gunduz.org> - 3.1.1-1
- Update to 3.1.1
- Update URL and download URL.
- Apply cosmetic changes to spec file.

* Sun Apr 26 2009 Devrim GUNDUZ <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 06 2008 Balint Cristian <rezso@rdsor.ro> - 3.0.3-1
- new upstream stable

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.0.1-2
- Rebuild for Python 2.6

* Fri Oct 17 2008 Balint Cristian <rezso@rdsor.ro> - 3.0.1-1
- new stable bugfix
- fix another gcc43 header

* Wed May 28 2008 Balint Cristian <rezso@rdsor.ro> - 3.0.0-4
- disable bindings for REL4

* Wed Apr 23 2008 Balint Cristian <rezso@rdsor.ro> - 3.0.0-3
- require ruby too

* Wed Apr 23 2008 Balint Cristian <rezso@rdsor.ro> - 3.0.0-2
- remove python-abi request, koji fails

* Sun Apr 20 2008 Balint Cristian <rezso@rdsor.ro> - 3.0.0-1
- New branch upstream
- Fix gcc43 build
- Avoid r-path hardcoding
- Enable and include python module
- Enable and include ruby module
- Enable and run testsuite during build

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2.3-2
- Autorebuild for GCC 4.3

* Mon Jan   8 2007 Shawn McCann <mccann0011@hotmail.com> - 2.2.3-1
- Upgraded to geos-2.2.3 and removed patches

* Sat Sep  16 2006 Shawn McCann <mccann0011@hotmail.com> - 2.2.1-5
- Rebuild for Fedora Extras 6

* Sat Mar  4 2006 Shawn McCann <mccann0011@hotmail.com> - 2.2.1-4
- Rebuild for Fedora Extras 5

* Sat Jan 14 2006 Shawn McCann <smccann@canasoft.ca> - 2.2.1-3
- Updated gcc4 patch

* Wed Jan 11 2006 Ralf Corsépius <rc040203@freenet.de> - 2.2.1-2
- Add gcc4 patch

* Sat Dec 31 2005 Shawn McCann <smccann@canasoft.ca> - 2.2.1-1
- Updated to address review comments in bug 17039

* Fri Dec 30 2005 Shawn McCann <smccann@canasoft.ca> - 2.2.1-1
- Initial release
