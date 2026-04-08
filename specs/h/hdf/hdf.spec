# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# No more Java on i686
%ifarch %{java_arches}
%bcond_without java
%else
%bcond_with java
%endif

Name: hdf
Version: 4.3.0
Release: 4%{?dist}
Summary: A general purpose library and file format for storing scientific data
# Automatically converted from old format: BSD - review is highly recommended.
License: LicenseRef-Callaway-BSD
URL: https://portal.hdfgroup.org/
Source0: https://github.com/HDFGroup/hdf4/archive/refs/tags/hdf%{version}.tar.gz
Source1: h4comp
# Fix java build
Patch1: hdf-build.patch

# For destdir/examplesdir patches
BuildRequires: automake, libtool, gcc, gcc-c++
BuildRequires: chrpath
BuildRequires: flex byacc libjpeg-devel zlib-devel %{!?el6:libaec-devel}
BuildRequires: libtirpc-devel
BuildRequires: gcc-gfortran, gcc
%if %{with java}
BuildRequires: java-devel
BuildRequires: javapackages-tools
BuildRequires: hamcrest
BuildRequires: junit
BuildRequires: slf4j
%else
Obsoletes:     java-hdf < %{version}-%{release}
%endif
BuildRequires: make
Requires: %{name}-libs%{?_isa} = %{version}-%{release}


%description
HDF4 is a general purpose library and file format for storing scientific data.
HDF4 can store two primary objects: datasets and groups. A dataset is
essentially a multidimensional array of data elements, and a group is a
structure for organizing objects in an HDF4 file. Using these two basic
objects, one can create and store almost any kind of scientific data
structure, such as images, arrays of vectors, and structured and unstructured
grids. You can also mix and match them in HDF4 files according to your needs.


%package devel
Summary: HDF4 development files
Provides: %{name}-static = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: libjpeg-devel%{?_isa}
Requires: libtirpc-devel%{?_isa}
Requires: zlib-devel%{?_isa}

%description devel
HDF4 development headers and libraries.


%package examples
Summary: HDF4 example source files
BuildArch: noarch

%description examples
HDF4 example source files.


%package libs
Summary: HDF4 shared libraries

%description libs
HDF4 shared libraries.


%package static
Summary: HDF4 static libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
HDF4 static libraries.


%if %{with java}
%package -n java-hdf
Summary: HDF4 java library
Requires:  slf4j
Obsoletes: jhdf < 3.3.1-2

%description -n java-hdf
HDF4 java library
%endif


%prep
%setup -q -n hdf4-hdf%{version}
%patch -P 1 -p1 -b .build

%if %{with java}
# Replace jars with system versions
# hamcrest-core is obsoleted in hamcrest-2.2
# Junit tests are failing with junit-4.13.1
%if 0%{?rhel} >= 9 || 0%{?fedora}
find . ! -name junit.jar -name "*.jar" -delete
ln -s $(build-classpath hamcrest) java/lib/hamcrest-core.jar
%else
find . -name "*.jar" -delete
ln -s $(build-classpath hamcrest/core) java/lib/hamcrest-core.jar
ln -s $(build-classpath junit) java/lib/junit.jar
# Fix test output
junit_ver=$(sed -n '/<version>/{s/^.*>\([0-9]\.[0-9.]*\)<.*/\1/;p;q}' /usr/share/maven-poms/junit.pom)
sed -i -e "s/JUnit version .*/JUnit version $junit_ver/" java/test/testfiles/JUnit-*.txt
%endif
ln -s $(build-classpath slf4j/api) java/lib/slf4j-api-1.7.33.jar
ln -s $(build-classpath slf4j/nop) java/lib/ext/slf4j-nop-1.7.33.jar
ln -s $(build-classpath slf4j/simple) java/lib/ext/slf4j-simple-1.7.33.jar
%endif

find . -type f -name "*.h" -exec chmod 0644 '{}' \;
find . -type f -name "*.c" -exec chmod 0644 '{}' \;

# restore include file timestamps modified by patching
#touch -c -r ./hdf/src/hdfi.h.ppc ./hdf/src/hdfi.h


%build
# This should be removed once rebased to an upstream version with
# C99 compatibility fixes (bug 2167466).
#global build_type_safety_c 0

# For destdir/examplesdir patches
autoreconf -vif

# avoid upstream compiler flags settings
rm config/*linux-gnu

# TODO: upstream fix
# libmfhdf.so is link to libdf.so
export CFLAGS="%{optflags} -std=gnu17 -I%{_usr}/include/tirpc"
export LIBS="-ltirpc"
%global _configure ../configure
# Java test needs this but doesn't create it
mkdir -p build-shared/java/lib
cd build-shared
# Java requires shared libraries, fortran requires static
%configure --disable-production %{?with_java:--enable-java} --disable-netcdf \
 --enable-shared=yes --enable-static=no --disable-fortran %{!?el6:--with-szlib} \
 --includedir=%{_includedir}/%{name}
%make_build
cd -
mkdir build-static
cd build-static
# Java requires shared libraries, fortran requires static

# Temporary workaround for compiling on GCC-10
%if 0%{?fedora} || 0%{?rhel} > 8
export FCFLAGS="%{build_fflags} -fallow-argument-mismatch"
export FFLAGS="%{build_fflags} -fallow-argument-mismatch"
%endif
%configure --disable-production --disable-java --disable-netcdf \
 --enable-shared=no --enable-static=yes --enable-fortran %{!?el6:--with-szlib} \
 --includedir=%{_includedir}/%{name}
%make_build
cd -

# correct the timestamps based on files used to generate the header files
touch -c -r hdf/src/hdf.inc hdf/src/hdf.f90
touch -c -r hdf/src/dffunc.inc hdf/src/dffunc.f90
touch -c -r mfhdf/fortran/mffunc.inc mfhdf/fortran/mffunc.f90
# netcdf fortran include need same treatement, but they are not shipped


%install
%make_install -C build-static
%make_install -C build-shared
chrpath --delete --keepgoing %{buildroot}%{_bindir}/* %{buildroot}%{_libdir}/%{name}/*.so.* %{buildroot}%{_libdir}/*.so.* || :

#install -pm 644 README.txt release_notes/*.txt %{buildroot}%{_pkgdocdir}/

rm -f %{buildroot}%{_libdir}/%{name}/*.la
rm -f %{buildroot}%{_libdir}/*.la

#Don't conflict with netcdf
for file in ncdump ncgen; do
  mv %{buildroot}%{_bindir}/$file %{buildroot}%{_bindir}/h$file
  # man pages are the same than netcdf ones
  rm %{buildroot}%{_mandir}/man1/${file}.1
done

#Fixup headers and scripts for multiarch
%if "%{_lib}" == "lib64"
for x in h4cc h4fc
do
  mv %{buildroot}%{_bindir}/${x} \
     %{buildroot}%{_bindir}/${x}-64
  install -m 0755 %SOURCE1 %{buildroot}%{_bindir}/${x}
done
%else
for x in h4cc h4fc
do
  mv %{buildroot}%{_bindir}/${x} \
     %{buildroot}%{_bindir}/${x}-32
  install -m 0755 %SOURCE1 %{buildroot}%{_bindir}/${x}
done
%endif


%check
# https://github.com/HDFGroup/hdf4/issues/473
%ifarch ppc64le s390x
make -j1 -C build-shared check || :
make -j1 -C build-static check || :
%else
make -j1 -C build-shared check
make -j1 -C build-static check
%endif


%files
%license COPYING
%doc README.md release_notes/*.txt
%{_bindir}/*
%exclude %{_bindir}/h4?c*
%{_libdir}/*.so.0*

%files devel
%{_bindir}/h4?c*
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/*.settings

%files examples
%doc HDF4Examples

%files libs
%{_libdir}/*.so.0*

%files static
%{_libdir}/*.a

%if %{with java}
%files -n java-hdf
%{_jnidir}/hdf.jar
%{_libdir}/%{name}/libhdf_java.so
%endif


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Antonio Trande <sagitter@fedoraproject.org> - 4.3.0-3
- Fix GCC15 builds

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 30 2024 Orion Poplawski <orion@nwra.com> - 4.3.0-1
- Update to 4.3.0

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 4.2.16.2-3
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 30 2024 Orion Poplawski <orion@nwra.com> - 4.2.16.2-1
- Update to 4.2.16-2

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.15-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.15-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Aug 29 2023 Florian Weimer <fweimer@redhat.com> - 4.2.15-14
- Set build_type_safety_c to 0 (#2167466)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.15-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 10 2022 Orion Poplawski <orion@nwra.com> - 4.2.15-10
- Drop java for i686 (bz#2104047)

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 4.2.15-9
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 29 2021 Antonio Trande <sagitter@fedoraproject.org> - 4.2.15-7
- Fix eln builds

* Wed Jul 28 2021 Antonio Trande <sagitter@fedoraproject.org> - 4.2.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
- Use bundled junit
- Fix hamcrest symlinks in Fedora 35+

* Sun May 30 2021 Orion Poplawski <orion@nwra.com> - 4.2.15-5
- Handle junit versions better

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Merlin Mathesius <mmathesi@redhat.com> - 4.2.15-2
- Minor conditional fix for ELN

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 4.2.15-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Fri May 01 2020 Orion Poplawski <orion@nwra.com> - 4.2.15-1
- Update to 4.2.15

* Thu Apr 02 2020 Björn Esser <besser82@fedoraproject.org> - 4.2.14-9
- Fix string quoting for rpm >= 4.16

* Sun Feb 02 2020 Antonio Trande <sagitter@fedoraproject.org> 4.2.14-8
- Temporary workaround for compiling with GCC-10 

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov  8 2019 Orion Poplawski <orion@nwra.com> - 4.2.14-6
- Move compile scripts to hdf-devel and allow multilib install (bz#1769326)
- Split shared libraries into hdf-libs sub-package

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 10 2019 Orion Poplawski <orion@nwra.com> - 4.2.14-4
- Move libraries into %%{_libdir}

* Tue Apr 9 2019 Orion Poplawski <orion@nwra.com> - 4.2.14-3
- Build shared libraries
- Enable java

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Nov 03 2018 Antonio Trande <sagitter@fedoraproject.org> 4.2.14-1
- Release 4.2.14

* Sun Oct 7 2018 Orion Poplawski <orion@nwra.com> - 4.2.13-11
- Use LIBS instead of LDFLAGS for -ltirpc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 22 2018 Antonio Trande <sagitter@fedoraproject.org> - 4.2.13-9
- Add gcc BR

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 5 2018 Orion Poplawski <orion@nwra.com> - 4.2.13-7
- Make hdf-devel require libtirpc-devel

* Fri Feb 02 2018 Orion Poplawski <orion@cora.nwra.com> - 4.2.13-6
- Rebuild for gcc 8.0

* Sat Jan 20 2018 Antonio Trande <sagitter@fedoraproject.org> 4.2.13-5
- Enable szlib support

* Wed Jan 17 2018 Pavel Raiskup <praiskup@redhat.com> - 4.2.13-4
- rpc api moved from glibc to libtirpc:
  https://fedoraproject.org/wiki/Changes/SunRPCRemoval

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Antonio Trande <sagitter@fedoraproject.org> 4.2.13-1
- Update to 4.2.13

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> 4.2.12-1
- Update to 4.2.12

* Wed May 25 2016 Orion Poplawski <orion@cora.nwra.com> 4.2.11-4
- Cleanup spec
- Remove .la files
- Use %%license

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 Orion Poplawski <orion@cora.nwra.com> 4.2.11-1
- Update to 4.2.11
- Drop format patch applied upstream
- Update destdir patch

* Mon Sep 8 2014 Orion Poplawski <orion@cora.nwra.com> - 4.2.10-7
- Updated patch for ppc64le support (bug #1134385)

* Wed Sep 3 2014 Orion Poplawski <orion@cora.nwra.com> - 4.2.10-6
- Add initial attempt at ppc64le support (bug #1134385)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 25 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> 4.2.10-4
- Add AArch64 support.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Jakub Čajka <jcajka@redhat.com> 4.2.10-2
- Fixed build/tests on s390x
- Tests enabled on ppc

* Fri Feb 14 2014 Orion Poplawski <orion@cora.nwra.com> 4.2.10-1
- Update to 4.2.10
- Rebase arm, ppc, and s390 patches
- Add destdir, examplesdir patches to fix installation of examples

* Sat Feb 1 2014 Orion Poplawski <orion@cora.nwra.com> 4.2.9-4
- Fix build with -Werror=format-security (bug #1037120)

* Tue Aug 13 2013 Karsten Hopp <karsten@redhat.com> 4.2.9-3
- temporarily skip checks on ppc* (#961007)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Orion Poplawski <orion@cora.nwra.com> 4.2.9-1
- Update to 4.2.9
- Add patch for some missing declarations
- Add patch to fix integer wrapping in test

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 4.2.8-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 4.2.8-2
- rebuild against new libjpeg

* Wed Aug 15 2012 Orion Poplawski <orion@cora.nwra.com> 4.2.8-1
- Update to 4.2.8

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 DJ Delorie <dj@redhat.com> 4.2.7-2
- Add patch for ARM support

* Wed Feb 15 2012 Orion Poplawski <orion@cora.nwra.com> 4.2.7-1
- Update to 4.2.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Orion Poplawski <orion@cora.nwra.com> 4.2.6-1
- Update to 4.2.6
- Drop jpeg patch, fixed upstream
- Update ppc,s390 patches

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Orion Poplawski <orion@cora.nwra.com> 4.2.5-2
- Add patch to disable jpeg tests due to change to jpeg-turbo, FTBFS bug 631337

* Tue Mar 2 2010 Orion Poplawski <orion@cora.nwra.com> 4.2.5-1
- Update to 4.2.5

* Fri Sep 18 2009 Orion Poplawski <orion@cora.nwra.com> 4.2r4-5
- Add EL4 build conditionals

* Thu Aug 13 2009 Orion Poplawski <orion@cora.nwra.com> 4.2r4-4
- Add -fPIC to FFLAGS

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2r4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 7 2009 Orion Poplawski <orion@cora.nwra.com> 4.2r4-2
- Add Provides hdf-static to hdf-devel (bug #494529)

* Wed Feb 25 2009 Orion Poplawski <orion@cora.nwra.com> 4.2r4-1
- Update to 4.2r4
- Add patch to increase buffer size in test
- Drop upstreamed libm patch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2r3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct  1 2008 Orion Poplawski <orion@cora.nwra.com> 4.2r3-4
- Rebase maxavailfiles patch

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 4.2r3-3
- Fix Patch0:/%%patch mismatch.

* Sun Mar  2 2008 Patrice Dumas <pertusus@free.fr> 4.2r3-2
- don't ship an empty netcdf.h file. The related definitions are now
  in hdf4_netcdf.h

* Tue Feb  5 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.r3-1
- Update to 4.2r3

* Tue Feb  5 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.r2-7
- Add patch to add -lm to hdiff link

* Tue Feb  5 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.r2-6
- Add patch for s390 support (bug #431511)

* Mon Jan  7 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.r2-5
- Add patches for sparc support (bug #427639)

* Mon Oct 29 2007 Patrice Dumas <pertusus@free.fr> 4.2r2-4
- install the netcdf.h file that describes the netcdf2 hdf enabled
  API

* Mon Oct 29 2007 Patrice Dumas <pertusus@free.fr> 4.2r2-3
- ship hdf enabled nc* utils as hnc*
- add --disable-netcdf that replaces HAVE_NETCDF
- keep include files timestamps, and have the same accross arches
- fix multiarch difference in include files (#341491)

* Wed Oct 17 2007 Patrice Dumas <pertusus@free.fr> 4.2r2-2
- update to 4.2r2

* Fri Aug 24 2007 Orion Poplawski <orion@cora.nwra.com> 4.2r1-15
- Update license tag to BSD
- Rebuild for BuildID

* Thu May 10 2007 Balint Cristian <cbalint@redhat.com> 4.2r1-14
- Fix ppc64 too.

* Thu May 10 2007 Orion Poplawski <orion@cora.nwra.com> 4.2r1-13
- Remove netcdf-devel requires. (bug #239631)

* Fri Apr 20 2007 Orion Poplawski <orion@cora.nwra.com> 4.2r1-12
- Use 4.2r1-hrepack-p4.tar.gz for hrepack patch
- Remove configure patch applied upstream
- Use --disable-production configure flag to avoid stripping -g compile flag
- Add patch to fix open file test when run under mock

* Tue Aug 29 2006 Orion Poplawski <orion@cora.nwra.com> 4.2r1-11
- Rebuild for FC6

* Thu Apr 20 2006 Orion Poplawski <orion@cora.nwra.com> 4.2r1-10
- Add Requires netcdf-devel for hdf-devel (bug #189337)

* Mon Feb 13 2006 Orion Poplawski <orion@cora.nwra.com> 4.2r1-9
- Rebuild for gcc/glibc changes

* Wed Feb  8 2006 Orion Poplawski <orion@cora.nwra.com> 4.2r1-8
- Compile with -DHAVE_NETCDF for gdl hdf/netcdf compatibility

* Thu Feb  2 2006 Orion Poplawski <orion@cora.nwra.com> 4.2r1-7
- Add patch to build on ppc

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-6
- Rebuild

* Wed Oct 05 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-5
- Add Requires: libjpeg-devel zlib-devel to -devel package

* Tue Aug 23 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-4
- Use -fPIC
- Fix project URL

* Fri Jul 29 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-3
- Exclude ppc/ppc64 - HDF does not recognize it

* Wed Jul 20 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-2
- Fix BuildRequires to have autoconf

* Fri Jul 15 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-1
- inital package for Fedora Extras
