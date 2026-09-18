# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%ifarch %{ix86}
%bcond openmpi 0
%else
%bcond openmpi %{undefined flatpak}
%endif
%bcond mpich %{undefined flatpak}

Name:           cgnslib
Version:        4.5.1
Release:        1%{?dist}
Summary:        Computational Fluid Dynamics General Notation System
License:        Zlib
URL:            http://www.cgns.org/
Source0:        https://github.com/CGNS/CGNS/archive/v%{version}/%{name}-%{version}.tar.gz
# Allow overriding all BIN/LIB/INCLUDE install dirs
Patch0:         cgnslib-cmake-install-dirs.patch
# Fix invalid Icon and Exec paths in desktop files
Patch1:         cgnslib_desktop.patch
Patch2:         cgnslib-c99.patch
Patch3:         cgnslib-i686.patch
# Allow building with Ninja generator
Patch4:         https://github.com/CGNS/CGNS/pull/845.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-gfortran
BuildRequires:  hdf5-devel
BuildRequires:  libXmu-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  tcl-devel < 1:9
BuildRequires:  tk-devel < 1:9
BuildRequires:  zlib-devel
Requires:       hdf5%{?_isa} = %{_hdf5_version}
Requires:       %{name}-common = %{version}-%{release}

%description
The Computational Fluid Dynamics General Notation System (CGNS) provides a
general, portable, and extensible standard for the storage and retrieval of
computational fluid dynamics (CFD) analysisdata. It consists of a collection
of conventions, and free and open software implementing those conventions. It
is self-descriptive, machine-independent, well-documented, and administered by
an international steering committee.


%package common
Summary:        Common files for %{name}
BuildArch:      noarch

%description common
Common files for %{name}.


%package libs
Summary:       %{name} library

%description libs
%{name} library.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       hdf5-devel%{?_isa}
Requires:       gcc-gfortran%{?_isa}

%description    devel
This package contains libraries and header files for
developing applications that use %{name} libraries.


###############################################################################

%if %{with openmpi}
%package        openmpi
Summary:        %{name} compiled against openmpi
Requires:       %{name}-common = %{version}-%{release}
BuildRequires:  openmpi-devel
BuildRequires:  hdf5-openmpi-devel

%description    openmpi
%{name} compiled against openmpi.


%package openmpi-libs
Summary:       %{name} library

%description openmpi-libs
%{name} library.


%package        openmpi-devel
Summary:        Development files for %{name} compiled against openmpi
# Require explicitly for dir ownership
Requires:       openmpi-devel
Requires:       %{name}-openmpi%{?_isa} = %{version}-%{release}

%description    openmpi-devel
Development files for %{name} compiled against openmpi.
%endif

###############################################################################

%if %{with mpich}
%package        mpich
Summary:        %{name} compiled against mpich
Requires:       %{name}-common = %{version}-%{release}
BuildRequires:  mpich-devel
BuildRequires:  hdf5-mpich-devel

%description    mpich
%{name} compiled against mpich.


%package mpich-libs
Summary:       %{name} library

%description mpich-libs
%{name} library.


%package        mpich-devel
Summary:        Development files for %{name} compiled against mpich
# Require explicitly for dir ownership
Requires:       mpich-devel
Requires:       %{name}-mpich%{?_isa} = %{version}-%{release}

%description    mpich-devel
Development files for %{name} compiled against mpich.
%endif

###############################################################################

%prep
%autosetup -p1 -n CGNS-%{version}

# Remove executable bit
chmod a-x src/cgnstools/utilities/cgns_to_vtk.c


%build
# This is needed for GCC10, whenever a new cgnslib release is published, check whether it is still needed
# export FCFLAGS+=-fallow-argument-mismatch
cgnslib_cmake_args="\
        -DCGNS_ENABLE_SCOPING=ON \
        -DCMAKE_SKIP_RPATH=ON \
        -DCGNS_ENABLE_TESTS=ON \
        -DCGNS_ENABLE_FORTRAN=ON \
        -DCGNS_BUILD_CGNSTOOLS=ON \
        -DCGNS_ENABLE_HDF5=ON"
#        -DCMAKE_Fortran_FLAGS_RELEASE:STRING='$FCFLAGS -DNDEBUG $LDFLAGS -lhdf5 -fPIC'"

### Serial version ###
%define _vpath_builddir %{_target_platform}
%cmake \
    -DBIN_INSTALL_DIR=%{_bindir} \
    -DLIB_INSTALL_DIR=%{_libdir} \
    -DINCLUDE_INSTALL_DIR=%{_includedir} \
    $cgnslib_cmake_args
%cmake_build


### openmpi version ###
%if %{with openmpi}
(
%{_openmpi_load}
%define _vpath_builddir %{_target_platform}-openmpi
export CXX=mpicxx
export FC=mpifort
%cmake \
    -DHDF5_NEED_MPI=ON -DCGNS_ENABLE_PARALLEL=ON \
    -DBIN_INSTALL_DIR=$MPI_BIN \
    -DLIB_INSTALL_DIR=$MPI_LIB \
    -DINCLUDE_INSTALL_DIR=$MPI_INCLUDE \
    -DCMAKE_Fortran_FLAGS_RELEASE="%{optflags} -I $MPI_FORTRAN_MOD_DIR" \
    $cgnslib_cmake_args

%cmake_build
%{_openmpi_unload}
)
%endif


### mpich version ###
%if %{with mpich}
(
%{_mpich_load}
%define _vpath_builddir %{_target_platform}-mpich
export CXX=mpicxx
export FC=mpifort
%cmake \
    -DHDF5_NEED_MPI=ON -DCGNS_ENABLE_PARALLEL=ON \
    -DBIN_INSTALL_DIR=$MPI_BIN \
    -DLIB_INSTALL_DIR=$MPI_LIB \
    -DINCLUDE_INSTALL_DIR=$MPI_INCLUDE \
    -DCMAKE_Fortran_FLAGS_RELEASE="%{optflags} -I $MPI_FORTRAN_MOD_DIR" \
    $cgnslib_cmake_args

%cmake_build
%{_mpich_unload}
)
%endif



%install
### openmpi version ###
%if %{with openmpi}
(
%{_openmpi_load}
%define _vpath_builddir %{_target_platform}-openmpi
%cmake_install

# Move fortran module to correct location
mkdir -p %{buildroot}$MPI_FORTRAN_MOD_DIR
mv %{buildroot}$MPI_INCLUDE/cgns.mod %{buildroot}$MPI_FORTRAN_MOD_DIR

# Drop desktop files
rm -f %{buildroot}$MPI_BIN/*.desktop
%{_openmpi_unload}
)
%endif

### mpich version ###
%if %{with mpich}
(
%{_mpich_load}
%define _vpath_builddir %{_target_platform}-mpich
%cmake_install

# Move fortran module to correct location
mkdir -p %{buildroot}$MPI_FORTRAN_MOD_DIR
mv %{buildroot}$MPI_INCLUDE/cgns.mod %{buildroot}$MPI_FORTRAN_MOD_DIR

# Drop desktop files
rm -f %{buildroot}$MPI_BIN/*.desktop
%{_mpich_unload}
)
%endif

### Serial version ###
%define _vpath_builddir %{_target_platform}
%cmake_install

# Move fortran module to correct location
mkdir -p %{buildroot}%{_libdir}/gfortran/modules
mv %{buildroot}%{_includedir}/cgns.mod %{buildroot}%{_libdir}/gfortran/modules

# Move desktop files to correct location
mkdir -p %{buildroot}%{_datadir}/applications
mv %{buildroot}%{_bindir}/*.desktop %{buildroot}%{_datadir}/applications


find %{buildroot} -name '*.a' -delete -print


%check
### Serial version ###
(
%define _vpath_builddir %{_target_platform}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH
%ctest || :
)

### openmpi version ###
%if %{with openmpi}
(
%{_openmpi_load}
%define _vpath_builddir %{_target_platform}-openmpi
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:$LD_LIBRARY_PATH
ctest || :
%{_mpich_unload}
)
%endif

### mpich version ###
%if %{with mpich}
(
%{_mpich_load}
%define _vpath_builddir %{_target_platform}-mpich
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:$LD_LIBRARY_PATH
ctest || :
%{_mpich_unload}
)
%endif


%files
%{_bindir}/adf2hdf
%{_bindir}/cgconfig
%{_bindir}/cgnscalc
%{_bindir}/cgnscheck
%{_bindir}/cgnscompress
%{_bindir}/cgnsconvert
%{_bindir}/cgnsdiff
%{_bindir}/cgnslist
%{_bindir}/cgnsplot
%{_bindir}/cgnsnodes
%{_bindir}/cgnsnames
%{_bindir}/cgnstools/
%{_bindir}/cgnsupdate
%{_bindir}/cgnsview
%{_bindir}/hdf2adf
%{_bindir}/unitconv

%files libs
%{_libdir}/libcgns.so.4.5

%files devel
%{_includedir}/cgnsBuild.defs
%{_includedir}/cgns_io.h
%{_includedir}/cgnslib.h
%{_includedir}/cgnstypes.h
%{_includedir}/cgnstypes_f.h
%{_includedir}/cgnstypes_f03.h
%{_includedir}/cgnswin_f.h
%{_includedir}/cgnsconfig.h
%{_libdir}/libcgns.so
%{_libdir}/cmake/cgns/
%{_fmoddir}/cgns.mod

%files common
%doc release_docs/RELEASE.md README.md
%license license.txt
%{_datadir}/cgnstools/
%{_datadir}/applications/cgnscalc.desktop
%{_datadir}/applications/cgnsnodes.desktop
%{_datadir}/applications/cgnsplot.desktop
%{_datadir}/applications/cgnsview.desktop
%{_datadir}/applications/unitconv.desktop

%if %{with openmpi}
%files openmpi
%{_libdir}/openmpi/bin/adf2hdf
%{_libdir}/openmpi/bin/cgconfig
%{_libdir}/openmpi/bin/cgnscalc
%{_libdir}/openmpi/bin/cgnscheck
%{_libdir}/openmpi/bin/cgnscompress
%{_libdir}/openmpi/bin/cgnsconvert
%{_libdir}/openmpi/bin/cgnsdiff
%{_libdir}/openmpi/bin/cgnslist
%{_libdir}/openmpi/bin/cgnsplot
%{_libdir}/openmpi/bin/cgnsnodes
%{_libdir}/openmpi/bin/cgnsnames
%{_libdir}/openmpi/bin/cgnstools/
%{_libdir}/openmpi/bin/cgnsupdate
%{_libdir}/openmpi/bin/cgnsview
%{_libdir}/openmpi/bin/hdf2adf
%{_libdir}/openmpi/bin/unitconv

%files openmpi-libs
%{_libdir}/openmpi/lib/libcgns.so.4.5

%files openmpi-devel
%{_includedir}/openmpi*/cgnsBuild.defs
%{_includedir}/openmpi*/cgns_io.h
%{_includedir}/openmpi*/cgnslib.h
%{_includedir}/openmpi*/cgnstypes.h
%{_includedir}/openmpi*/cgnstypes_f.h
%{_includedir}/openmpi*/cgnstypes_f03.h
%{_includedir}/openmpi*/cgnswin_f.h
%{_includedir}/openmpi*/cgnsconfig.h
%{_includedir}/openmpi*/pcgnslib.h
%{_libdir}/openmpi/lib/libcgns.so
%{_libdir}/openmpi/lib/cmake/cgns/
%{_fmoddir}/openmpi/cgns.mod
%endif

%if %{with mpich}
%files mpich
%{_libdir}/mpich/bin/adf2hdf
%{_libdir}/mpich/bin/cgconfig
%{_libdir}/mpich/bin/cgnscalc
%{_libdir}/mpich/bin/cgnscheck
%{_libdir}/mpich/bin/cgnscompress
%{_libdir}/mpich/bin/cgnsconvert
%{_libdir}/mpich/bin/cgnsdiff
%{_libdir}/mpich/bin/cgnslist
%{_libdir}/mpich/bin/cgnsplot
%{_libdir}/mpich/bin/cgnsnodes
%{_libdir}/mpich/bin/cgnsnames
%{_libdir}/mpich/bin/cgnstools/
%{_libdir}/mpich/bin/cgnsupdate
%{_libdir}/mpich/bin/cgnsview
%{_libdir}/mpich/bin/hdf2adf
%{_libdir}/mpich/bin/unitconv

%files mpich-libs
%{_libdir}/mpich/lib/libcgns.so.4.5

%files mpich-devel
%{_includedir}/mpich*/cgnsBuild.defs
%{_includedir}/mpich*/cgns_io.h
%{_includedir}/mpich*/cgnslib.h
%{_includedir}/mpich*/cgnstypes.h
%{_includedir}/mpich*/cgnstypes_f.h
%{_includedir}/mpich*/cgnstypes_f03.h
%{_includedir}/mpich*/cgnswin_f.h
%{_includedir}/mpich*/cgnsconfig.h
%{_includedir}/mpich*/pcgnslib.h
%{_libdir}/mpich/lib/libcgns.so
%{_libdir}/mpich/lib/cmake/cgns/
%{_fmoddir}/mpich/cgns.mod
%endif


%changelog
* Tue Dec 30 2025 Sandro Mani <manisandro@gmail.com> - 4.5.1-1
- Update to 4.5.1

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 23 2025 Cristian Le <git@lecris.dev> - 4.5.0-5
- Allow to build with ninja

* Thu Feb 13 2025 Orion Poplawski <orion@nwra.com> - 4.5.0-4
- Rebuild with hdf5 1.14.6

* Tue Jan 28 2025 Sandro Mani <manisandro@gmail.com> - 4.5.0-3
- Build with -DCGNS_ENABLE_SCOPING=ON to avoid symbol collisions with gmsh

* Sun Jan 26 2025 Sandro Mani <manisandro@gmail.com> - 4.5.0-2
- BR: {tcl,tk}-devel < 1:9

* Fri Jan 24 2025 Sandro Mani <manisandro@gmail.com> - 4.5.0-1
- Update to 4.5.0

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 25 2024 Orion Poplawski <orion@nwra.com> - 4.4.0-6
- Rebuild for hdf5 1.14.5

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Sandro Mani <manisandro@gmail.com> - 4.4.0-1
- Update to 4.4.0

* Thu Feb 02 2023 Florian Weimer <fweimer@redhat.com> - 4.3.0-7
- Fix C99 compatibility issue around TkWmAddToColormapWindows

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Sandro Mani <manisandro@gmail.com> - 4.3.0-5
- Split lib to separate subpackage

* Wed Nov 16 2022 Orion Poplawski <orion@nwra.com> - 4.3.0-4
- Re-enable parallel tests
- Drop EL9 workaround

* Sun Oct 30 2022 Sandro Mani <manisandro@gmail.com> - 4.3.0-3
- Fix invalid Icon and Exec paths in desktop files

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 21 2022 Sandro Mani <manisandro@gmail.com> - 4.3.0-1
- Update to 4.3.0

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Nov 21 2021 Orion Poplawski <orion@nwra.com> - 4.2.0-5
- Rebuild for hdf5 1.12.1

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 4.2.0-4
- Rebuild for hdf5 1.10.7

* Sun Jul 25 2021 Sandro Mani <manisandro@gmail.com> - 4.2.0-3
- Enable parallel build

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 26 2021 Sandro Mani <manisandro@gmail.com> - 4.2.0-1
- Update to 4.2.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 26 2020 Sandro Mani <manisandro@gmail.com> - 4.1.2-1
- Update to 4.1.2

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Orion Poplawski <orion@cora.nwra.com> - 4.1.1-2
- Rebuild for hdf5 1.10.6

* Thu May 07 2020 Sandro Mani <manisandro@gmail.com> - 4.1.1-1
- Update to 4.1.1

* Thu Mar 05 2020 Sandro Mani <manisandro@gmail.com> - 4.1.0-1
- Update to 4.1.0

* Fri Feb 21 2020 Sandro Mani <manisandro@gmail.com> - 4.0.0-1
- Update to 4.0.0

* Mon Feb 17 2020 Sandro Mani <manisandro@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 16 2019 Orion Poplawski <orion@nwra.com> - 3.4.0-2
- Rebuild for hdf5 1.10.5

* Tue Mar 12 2019 Sandro Mani <manisandro@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Björn Esser <besser82@fedoraproject.org> - 3.3.1-9
- Append curdir to CMake invokation. (#1668512)

* Sun Sep 02 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.3.1-8
- Disable wl,--as-needed on fedora 30+
- Use CMake3 on epel

* Thu Aug 30 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.3.1-7
- Fix Fortran linker flags for epel7

* Wed Aug 29 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.3.1-6
- Fix undefined references to HDF5 (bz#1623439)
- Add shebang to cgconfig
- Remove spurious executable bit
- Add Requires gcc-gfortran to the devel sub-package

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Sandro Mani <manisandro@gmail.com> - 3.3.1-4
- Rebuild (hdf5)
- Add missing BR: gcc, make

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Sandro Mani <manisandro@gmail.com> - 3.3.1-2
- Add patch to drop matherr hack.

* Sat Aug 05 2017 Sandro Mani <manisandro@gmail.com> - 3.3.1-1
- Update to 3.3.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 3.3.0-3
- Rebuild (gfortran)

* Tue Dec 06 2016 Orion Poplawski <orion@cora.nwra.com> - 3.3.0-2
- Rebuild for hdf5 1.8.18

* Wed Jun 29 2016 Orion Poplawski <orion@cora.nwra.com> - 3.3.0-1
- Update to 3.3.0
- Add patch to change Fortran module install location

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Orion Poplawski <orion@cora.nwra.com> - 3.2.1-6
- Rebuild for hdf5 1.8.16

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 3.2.1-4
- Rebuild for hdf5 1.8.15

* Wed Jan 07 2015 Orion Poplawski <orion@cora.nwra.com> - 3.2.1-3
- Rebuild for hdf5 1.8.4

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 30 2014 Christopher Meng <rpm@cicku.me> - 3.2.1-1
- Update to 3.2.1
- Enable hdf5 support
- Enable fortran support
- Build cgnstools(included in main package)

* Tue Jun 10 2014 Orion Poplawski <orion@cora.nwra.com> - 3.2-6
- Rebuild for hdf 1.8.13

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 27 2013 Orion Poplawski <orion@cora.nwra.com> - 3.2-4
- Rebuild for hdf5 1.8.12

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 3.2-2
- Rebuild for hdf5 1.8.11

* Mon Mar 18 2013 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> - 3.2-1
- new upstream version 3.2
- userguide not provided any more

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-5.r4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Orion Poplawski <orion@cora.nwra.com> - 3.1-4.r4
- Rebuild for hdf5 1.8.10

* Wed Aug 15 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject DOT org> 3.1-3.r4
- Updated to 3.1.3-4

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-8.r2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 2.5-7.rc2
- Rebuild for hdf5
- Explicitly require version of hdf5 built with

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-6.r2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 01 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject DOT org> 2.5-5.r2
- Added hdf5 to Requires, and hdf5-devel to devel Requires.

* Thu Feb 17 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject DOT org> 2.5-5.r1
- Updated to 2.5-5 release.

* Sun Jul 18 2010 Shakthi Kannan <shakthimaan [AT] fedoraproject DOT org> 2.5-3.r4
- Use zlib license that supercedes LGPLv2.

* Fri Jul 16 2010 Shakthi Kannan <shakthimaan [AT] fedoraproject DOT org> 2.5-2.r4
- Expanded CFD abbreviation.
- Added -devel sub-package.
- Added global debug_package nil.
- Added patch for creating shared library with soname.
- Added patch to fix library returning exit.
- Added usersguide.pdf to -devel sub-package.
- hdf5 atleast 1.8 is required.
- Added if condition for matching LINUX64 when copying library.

* Sat Aug 15 2009 Chitlesh Goorah <chitlesh [AT] fedoraproject DOT org> 2.5-1.r4
- New Package
