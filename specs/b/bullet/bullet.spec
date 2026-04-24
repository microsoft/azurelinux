# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _docdir_fmt %{name}

Name: bullet
Version: 3.08
Release: 16%{?dist}
Summary: 3D Collision Detection and Rigid Body Dynamics Library
# Automatically converted from old format: zlib and MIT and BSD and Boost - review is highly recommended.
License: Zlib AND LicenseRef-Callaway-MIT AND LicenseRef-Callaway-BSD AND BSL-1.0
URL: http://www.bulletphysics.com

Source0: %{name}3-%{version}-free.tar.xz
# bullet contains non-free code that we cannot ship.  Therefore we use
# this script to remove the non-free code before shipping it.
# Download the upstream tarball and invoke this script while in the
# tarball's directory:
# ./generate-tarball.sh 2.87
Source1: generate-tarball.sh

# Build against system tinyxml
Patch0: %{name}-3.08-tinyxml2.patch

# Fix C++ One Definition Rule violation
Patch1: %{name}-3.08-fix-c++-one-definition-rule-violation.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires: cmake
BuildRequires: dos2unix
BuildRequires: doxygen
BuildRequires: freeglut-devel
BuildRequires: libICE-devel
BuildRequires: tinyxml2-devel
BuildRequires: libglvnd-devel

%description
Bullet is a 3D Collision Detection and Rigid Body Dynamics Library for games
and animation.


%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: cmake
%description devel
Development headers and libraries for %{name}.


%package devel-doc
Summary: Documentation for developing programs that will use %{name}-devel
# Automatically converted from old format: zlib and LGPLv2+ - review is highly recommended.
License: Zlib AND LicenseRef-Callaway-LGPLv2+
Requires: %{name}-extras%{?_isa} = %{version}-%{release}

%description devel-doc
Documentation (PDF) for developing programs that will use %{name}-devel.


%package extras
Summary: Extra libraries for %{name}
# Automatically converted from old format: zlib and LGPLv2+ - review is highly recommended.
License: Zlib AND LicenseRef-Callaway-LGPLv2+

%description extras
Extra libraries for %{name}.


%package extras-devel
Summary: Development files for %{name} extras
# Automatically converted from old format: zlib and LGPLv2+ - review is highly recommended.
License: Zlib AND LicenseRef-Callaway-LGPLv2+
Requires: %{name}-extras%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description extras-devel
Development headers and libraries for %{name} extra libraries.


%prep
%setup -q -n %{name}3-%{version}
%patch -P0 -p1 -b .tinyxml
%patch -P1 -p1 -b .fix-odr
# The examples directory isn't needed for building
rm -r examples

# Fix the pkg-config module so it doesn't list the prefix twice in the include install dir.
sed -i 's|${prefix}/@INCLUDE_INSTALL_DIR@|@INCLUDE_INSTALL_DIR@|' bullet.pc.cmake

# BulletRobotics, BulletRoboticsGUI and obj2sdf require several bundled libs not yet packaged in the distribution
sed -i 's|BulletRoboticsGUI BulletRobotics||' Extras/CMakeLists.txt
sed -i 's|obj2sdf||' Extras/CMakeLists.txt

# Fix up file permissions and formats
dos2unix README.md
chmod -x src/BulletDynamics/ConstraintSolver/btSliderConstraint.h
chmod -x src/BulletDynamics/ConstraintSolver/btSliderConstraint.cpp

%build
%cmake \
  -DCLSOCKET_DEP_ONLY=ON \
  -DBUILD_BULLET2_DEMOS=OFF \
  -DBUILD_EXTRAS=ON \
  -DBUILD_OPENGL_DEMOS=OFF \
  -DBUILD_CPU_DEMOS=OFF \
  -DBUILD_UNIT_TESTS=OFF \
  -DINSTALL_EXTRA_LIBS=ON \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DOpenGL_GL_PREFERENCE=GLVND \
  -DINCLUDE_INSTALL_DIR=%{_includedir}/bullet/

%cmake_build

doxygen Doxyfile

%install
%cmake_install


%ldconfig_scriptlets

%ldconfig_scriptlets extras


%files
%license LICENSE.txt
%doc README.md AUTHORS.txt VERSION
%{_libdir}/libBullet3Collision.so.*
%{_libdir}/libBullet3Common.so.*
%{_libdir}/libBullet3Dynamics.so.*
%{_libdir}/libBullet3Geometry.so.*
%{_libdir}/libBullet3OpenCL_clew.so.*
%{_libdir}/libBulletCollision.so.*
%{_libdir}/libBulletDynamics.so.*
%{_libdir}/libBulletInverseDynamics.so.*
%{_libdir}/libBulletSoftBody.so.*
%{_libdir}/libLinearMath.so.*

%files devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/Bullet3Collision
%{_includedir}/%{name}/Bullet3Common
%{_includedir}/%{name}/Bullet3Dynamics
%{_includedir}/%{name}/Bullet3Geometry
%{_includedir}/%{name}/Bullet3OpenCL
%{_includedir}/%{name}/BulletCollision
%{_includedir}/%{name}/BulletDynamics
%{_includedir}/%{name}/BulletInverseDynamics
%{_includedir}/%{name}/BulletSoftBody
%{_includedir}/%{name}/InverseDynamics
%{_includedir}/%{name}/LinearMath
%{_libdir}/libBullet3Collision.so
%{_libdir}/libBullet3Common.so
%{_libdir}/libBullet3Dynamics.so
%{_libdir}/libBullet3Geometry.so
%{_libdir}/libBullet3OpenCL_clew.so
%{_libdir}/libBulletCollision.so
%{_libdir}/libBulletDynamics.so
%{_libdir}/libBulletInverseDynamics.so
%{_libdir}/libBulletSoftBody.so
%{_libdir}/libLinearMath.so
%{_libdir}/pkgconfig/bullet.pc
%{_libdir}/cmake/%{name}

%files devel-doc
%doc docs/Bullet_User_Manual.pdf
%doc docs/BulletQuickstart.pdf
%doc docs/GPU_rigidbody_using_OpenCL.pdf
%doc html

%files extras
%{_libdir}/libConvexDecomposition.so.*
%{_libdir}/libGIMPACTUtils.so.*
%{_libdir}/libHACD.so.*
%{_libdir}/libBulletFileLoader.so.*
%{_libdir}/libBullet2FileLoader.so.*
%{_libdir}/libBulletInverseDynamicsUtils.so.*
%{_libdir}/libBulletWorldImporter.so.*
%{_libdir}/libBulletXmlWorldImporter.so.*

%files extras-devel
%{_includedir}/%{name}/ConvexDecomposition
%{_includedir}/%{name}/GIMPACTUtils
%{_includedir}/%{name}/HACD
%{_includedir}/%{name}/BulletFileLoader
%{_includedir}/%{name}/Bullet2FileLoader
%{_includedir}/%{name}/BulletWorldImporter
%{_includedir}/%{name}/BulletXmlWorldImporter
%{_libdir}/libConvexDecomposition.so
%{_libdir}/libGIMPACTUtils.so
%{_libdir}/libHACD.so
%{_libdir}/libBulletFileLoader.so
%{_libdir}/libBullet2FileLoader.so
%{_libdir}/libBulletInverseDynamicsUtils.so
%{_libdir}/libBulletWorldImporter.so
%{_libdir}/libBulletXmlWorldImporter.so

%changelog
* Sat Aug 23 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.08-15
- Rebuilt for tinyxml2 11.0.0

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 12 2024 Dominik Mierzejewski <dominik@greysector.net> - 3.08-12
- rebuilt for tinyxml2

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 3.08-11
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Sep 25 2022 Rich Mattes <richmattes@gmail.com> - 3.08-5
- Rebuild for tinyxml2-9.0.0

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 11 2021 Tom Callaway <spot@fedoraproject.org> - 3.08-1
- update to 3.08

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.87-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.87-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.87-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.87-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.87-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.87-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 27 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.87-5
- Spec clean-up

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.87-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 2.87-3
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 18 2017 Rich Mattes <richmattes@gmail.com> - 2.87-1
- Update to release 2.87 (rhbz#1442838)

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 2.83-6
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.83-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.83-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.83-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 04 2016 Rich Mattes <richmattes@gmail.com> - 2.83-1
- Update to release 2.83

* Sat Oct 03 2015 François Cami <fcami@fedoraproject.org> - 2.82-7
- Move Bullet_User_Manual.pdf to a separate devel-doc package.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.82-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.82-5
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.82-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Rich Mattes <richmattes@gmail.com> - 2.82-2
- Install all of the bullet extras (rhbz#1097452)
- Spec file cleanup

* Sun Feb 09 2014 Rich Mattes <richmattes@gmail.com> - 2.82-1
- Update to version 2.82

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.81-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.81-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 13 2012 Rich Mattes <richmattes@gmail.com> - 2.81-1
- Update to version 2.81

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Rich Mattes <richmattes@gmail.com> - 2.80-1
- Update to version 2.80

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.79-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Rich Mattes <richmattes@gmail.com> - 2.79-1
- Update to version 2.79

* Wed May 11 2011 Rich Mattes <richmattes@gmail.com> - 2.78-1
- Update to version 2.78
- Remove upstreamed patches

* Sat Feb 19 2011 Rich Mattes <richmattes@gmail.com> - 2.77-4
- Fix gcc 4.6 build error

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.77-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Dan Horák <dan[at]danny.cz> - 2.77-3
- add extras subpackage with additional libs
- install headers into /usr/include/bullet

* Wed Sep 29 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.77-2
- Added LibSuffix patch

* Wed Sep 29 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.77-1
- Updatet to version 2.77
- Droped all patches because they are all in upstream

* Sat Aug 21 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.75-4
- Hope fix (#599495)

* Sat Aug 21 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.75-3
- Hope fix (#619885)

* Tue Mar 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.75-2
- pkgconfig file not installed (#549051)

* Sat Oct 03 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.75-1
- Updatet to new upstream version 2.75
- Updatet the patch file to work agian

* Thu Jun 25 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.74-1
- Updatet to version 2.74
- Updatet the patch file to work agian

* Sun Feb 22 2009 Bruno Mahé <bruno at gnoll.org> - 2.73-5
- Shortened the description
- Fix directory ownership for directories BulletCollision and BulletDynamics
- Convert ChangeLog to UTF-8
- chmod generate-tarball.sh to 644

* Fri Feb 20 2009 Bruno Mahé <bruno at gnoll.org> - 2.73-4
- Remove gcc-g++ in BuildRequires
- Add option -DCMAKE_BUILD_TYPE=NONE to %%cmake. This will make CMake using default compiler flags
- Use %% instead of single % in %%changelog to prevent macros from being expanded
- Specify we are not shipping pristine source because of some non-free parts
- Change licence to "zlib and MIT and BSD"
- Make include directory being owned by this package
- Remove duplicate documents
- Convert spec file to UTF8
- Set some files permission to 644

* Sun Feb 15 2009 Bruno Mahé <bruno at gnoll.org> - 2.73-3
- Remove non-free directories Demos/, Extras/ and Glut/ from the source

* Sun Jan 18 2009 Bruno Mahé <bruno at gnoll.org> - 2.73-2
- Add "rm -rf $RPM_BUILD_ROOT" to the install target
- Moved unversioned shared libraries (e.g. libfoo.so) to the -devel package
- Update %%post and %%postrun
- Change %%description
- Reduce length of %%summary
- Changed %%group to Development/Libraries
- Changed Zlib licence to lowercase zlib
- %%description kept below 80 characters wide

* Sat Dec 13 2008 Bruno Mahé <bruno at gnoll.org> - 2.73-1
- Initial build.
