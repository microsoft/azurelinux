%bcond mpich %{undefined flatpak}
%if 0%{?fedora} >= 40
%ifarch %{ix86}
%bcond openmpi 0
%else
%bcond openmpi %{undefined flatpak}
%endif
%else
%bcond openmpi %{undefined flatpak}
%endif
%bcond metis 1

# This flag prevents internal links
%undefine _ld_as_needed

Name:          scotch
Summary:       Graph, mesh and hypergraph partitioning library
Version:       7.0.4
Release:       5%{?dist}

License:       CeCILL-C
URL:           https://gitlab.inria.fr/scotch/scotch
Source0:       https://gitlab.inria.fr/scotch/scotch/-/archive/v%{version}/scotch-v%{version}.tar.bz2

# Use CMAKE_INSTALL_LIBDIR and CMAKE_INSTALL_INCLUDEDIR
Patch0:        scotch_installdirs.patch

BuildRequires: bison
BuildRequires: bzip2-devel
BuildRequires: cmake
BuildRequires: flex
BuildRequires: gcc-c++
BuildRequires: gcc-gfortran
BuildRequires: make
BuildRequires: xz-devel
BuildRequires: zlib-devel

%description
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. The parallel scotch libraries are packaged in the
ptscotch sub-packages.

%package devel
Summary:       Development libraries for scotch
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development libraries for scotch.


%if %{with metis}
%package devel-metis
Summary:       Metis compatibility header
Requires:      %{name}-devel%{?_isa} = %{version}-%{release}

%description devel-metis
This header is a drop-in replacement for the original metis.h header
to build against the scotch.
%endif


%package doc
Summary:       Documentations and example for scotch and ptscotch
BuildArch:     noarch

%description doc
Contains documentations and example for scotch and ptscotch

###############################################################################

%if %{with mpich}
%package -n ptscotch-mpich
Summary:       PT-Scotch libraries compiled against mpich
BuildRequires: mpich-devel

%description -n ptscotch-mpich
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. This sub-package provides parallelized scotch libraries
compiled with mpich.


%package -n ptscotch-mpich-devel
Summary:       Development libraries for PT-Scotch (mpich)
Requires:      pt%{name}-mpich%{?_isa} = %{version}-%{release}

%description -n ptscotch-mpich-devel
This package contains development libraries for PT-Scotch, compiled against
mpich.


%if %{with metis}
%package -n ptscotch-mpich-devel-parmetis
Summary:       Parmetis compatibility header
Requires:      pt%{name}-mpich-devel%{?_isa} = %{version}-%{release}

%description -n ptscotch-mpich-devel-parmetis
This header is a drop-in replacement for the original parmetis.h header
to build against the scotch.
%endif
%endif

###############################################################################

%if %{with openmpi}
%package -n ptscotch-openmpi
Summary:       PT-Scotch libraries compiled against openmpi
BuildRequires: openmpi-devel

%description -n ptscotch-openmpi
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. This sub-package provides parallelized scotch libraries
compiled with openmpi.


%package -n ptscotch-openmpi-devel
Summary:       Development libraries for PT-Scotch (openmpi)
Requires:      pt%{name}-openmpi%{?_isa} = %{version}-%{release}

%description -n ptscotch-openmpi-devel
This package contains development libraries for PT-Scotch, compiled against
openmpi.


%if %{with metis}
%package -n ptscotch-openmpi-devel-parmetis
Summary:       Parmetis compatibility header
Requires:      pt%{name}-openmpi-devel%{?_isa} = %{version}-%{release}

%description -n ptscotch-openmpi-devel-parmetis
This header is a drop-in replacement for the original parmetis.h header
to build against the scotch.
%endif
%endif


###############################################################################

%prep
%autosetup -N -n %{name}-v%{version}

%patch 0 -p1 -b .backup

# Convert the license files to utf8
for file in doc/CeCILL-C_V1-en.txt doc/CeCILL-C_V1-fr.txt; do
    iconv -f iso8859-1 -t utf-8 $file > $file.conv && mv -f $file.conv $file
done


%build
%define _vpath_builddir %{_target_platform}
%cmake -DBUILD_PTSCOTCH=OFF \
    -DCOMMON_PTHREAD:BOOL=ON \
    -DSCOTCH_PTHREAD:BOOL=ON \
    -DCOMMON_PTHREAD_AFFINITY_LINUX:BOOL=ON \
%if %{with metis}
    -DBUILD_LIBSCOTCHMETIS=ON \
    -DSCOTCH_METIS_VERSION=5 \
%else
    -DBUILD_LIBSCOTCHMETIS=OFF \
%endif
    -DCMAKE_INSTALL_BINDIR=%{_bindir} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir}/scotch \
%cmake_build

%if %{with mpich}
%{_mpich_load}
%define _vpath_builddir %{_target_platform}-mpich
%cmake -DBUILD_PTSCOTCH=ON \
    -DCOMMON_PTHREAD:BOOL=ON \
    -DSCOTCH_PTHREAD:BOOL=ON \
    -DCOMMON_PTHREAD_AFFINITY_LINUX:BOOL=ON \
%if %{with metis}
    -DBUILD_LIBSCOTCHMETIS=ON \
    -DSCOTCH_PARMETIS_VERSION=3 \
%else
    -DBUILD_LIBSCOTCHMETIS=OFF \
%endif
    -DCMAKE_INSTALL_BINDIR=$MPI_BIN \
    -DCMAKE_INSTALL_LIBDIR=$MPI_LIB \
    -DCMAKE_INSTALL_INCLUDEDIR=$MPI_INCLUDE/scotch
%cmake_build
%{_mpich_unload}
%endif

%if %{with openmpi}
%{_openmpi_load}
%define _vpath_builddir %{_target_platform}-openmpi
%cmake -DBUILD_PTSCOTCH=ON \
    -DCOMMON_PTHREAD:BOOL=ON \
    -DSCOTCH_PTHREAD:BOOL=ON \
    -DCOMMON_PTHREAD_AFFINITY_LINUX:BOOL=ON \
%if %{with metis}
    -DBUILD_LIBSCOTCHMETIS=ON \
    -DSCOTCH_PARMETIS_VERSION=3 \
%else
    -DBUILD_LIBSCOTCHMETIS=OFF \
%endif
    -DCMAKE_INSTALL_BINDIR=$MPI_BIN \
    -DCMAKE_INSTALL_LIBDIR=$MPI_LIB \
    -DCMAKE_INSTALL_INCLUDEDIR=$MPI_INCLUDE/scotch
%cmake_build
%{_openmpi_unload}
%endif


%install
%define _vpath_builddir %{_target_platform}
%cmake_install

%if %{with metis}
# Default to the v5 API for the metis compat library
ln -s libscotchmetisv5.so %{buildroot}%{_libdir}/libscotchmetis.so
# Rename include files to avoid conflicts with original Metis
mv %{buildroot}%{_includedir}/scotch/metis.h %{buildroot}%{_includedir}/scotch/scotchmetis.h
mv %{buildroot}%{_includedir}/scotch/metisf.h %{buildroot}%{_includedir}/scotch/scotchmetisf.h
%endif
cp -p %{buildroot}%{_libdir}/libesmumps.so %{buildroot}%{_libdir}/libesmumps.so.%{version}
ln -sf libesmumps.so.%{version} %{buildroot}%{_libdir}/libesmumps.so
ln -sf libesmumps.so.%{version} %{buildroot}%{_libdir}/libptesmumps.so

##############
%if %{with mpich}
%{_mpich_load}
%define _vpath_builddir %{_target_platform}-mpich
%cmake_install

# Compat symlink to ptesmumps.so
cp -p %{buildroot}$MPI_LIB/libptesmumps.so %{buildroot}$MPI_LIB/libptesmumps.so.%{version}
ln -sf libptesmumps.so.%{version} %{buildroot}$MPI_LIB/libptesmumps.so

%if %{with metis}
# Default to the v5 API for the metis compat library
ln -s libscotchmetisv5.so %{buildroot}$MPI_LIB/libscotchmetis.so
# Only the ParMeTiS v3 API is available
ln -s libptscotchparmetisv3.so %{buildroot}$MPI_LIB/libparmetis.so
ln -s libptscotchparmetisv3.so %{buildroot}$MPI_LIB/libptscotchparmetis.so
# Rename include files to avoid conflicts with original Metis
mv %{buildroot}$MPI_INCLUDE/scotch/metis.h %{buildroot}$MPI_INCLUDE/scotch/scotchmetis.h
mv %{buildroot}$MPI_INCLUDE/scotch/metisf.h %{buildroot}$MPI_INCLUDE/scotch/scotchmetisf.h
%endif
%{_mpich_unload}
%endif
################

################
%if %{with openmpi}
%{_openmpi_load}
%define _vpath_builddir %{_target_platform}-openmpi
%cmake_install

# Compat symlink to ptesmumps.so
cp -p %{buildroot}$MPI_LIB/libptesmumps.so %{buildroot}$MPI_LIB/libptesmumps.so.%{version}
ln -sf libptesmumps.so.%{version} %{buildroot}$MPI_LIB/libptesmumps.so

%if %{with metis}
# Default to the v5 API for the metis compat library
ln -s libscotchmetisv5.so %{buildroot}$MPI_LIB/libscotchmetis.so
# Only the ParMeTiS v3 API is available
ln -s libptscotchparmetisv3.so %{buildroot}$MPI_LIB/libparmetis.so
ln -s libptscotchparmetisv3.so %{buildroot}$MPI_LIB/libptscotchparmetis.so
# Rename include files to avoid conflicts with original Metis
mv %{buildroot}$MPI_INCLUDE/scotch/metis.h %{buildroot}$MPI_INCLUDE/scotch/scotchmetis.h
mv %{buildroot}$MPI_INCLUDE/scotch/metisf.h %{buildroot}$MPI_INCLUDE/scotch/scotchmetisf.h
%endif
%{_openmpi_unload}
%endif
##################

# Don't install executables
rm -f %{buildroot}%{_bindir}/*
rm -rf %{buildroot}%{_prefix}/man/*


%check
%define _vpath_builddir %{_target_platform}
%ctest || :

%if %{with mpich}
%{_mpich_load}
%define _vpath_builddir %{_target_platform}-mpich
%ctest || :
%{_mpich_unload}
%endif

%if %{with openmpi}
%{_openmpi_load}
%define _vpath_builddir %{_target_platform}-openmpi
%ctest || :
%{_openmpi_unload}
%endif


%files
%license doc/CeCILL-C_V1-en.txt
%{_libdir}/libscotch.so.7.0.4
%{_libdir}/libesmumps.so.7.0.4
%if %{with metis}
%{_libdir}/libscotchmetisv3.so
%{_libdir}/libscotchmetisv5.so
%endif
%{_libdir}/libscotcherr.so
%{_libdir}/libscotcherrexit.so

%files devel
%dir %{_includedir}/scotch
%{_includedir}/scotch/scotch.h
%{_includedir}/scotch/scotchf.h
%{_includedir}/scotch/esmumps.h
%{_libdir}/libesmumps.so
%{_libdir}/libptesmumps.so
%{_libdir}/libscotch.so
%dir %{_libdir}/cmake/scotch/
%{_libdir}/cmake/scotch/ptesmumpsTargets*
%{_libdir}/cmake/scotch/esmumpsTargets*
%{_libdir}/cmake/scotch/SCOTCH*
%{_libdir}/cmake/scotch/scotchTargets*
%{_libdir}/cmake/scotch/scotcherrTargets*
%{_libdir}/cmake/scotch/scotcherrexitTargets*

%if %{with metis}
%files devel-metis
%dir %{_includedir}/scotch
%{_includedir}/scotch/scotchmetis.h
%{_includedir}/scotch/scotchmetisf.h
%{_libdir}/libscotchmetis.so
%{_libdir}/cmake/scotch/scotchmetisTargets*
%endif

%files doc
%license doc/CeCILL-C_V1-en.txt
%doc doc/*.pdf
%doc doc/scotch_example.f

%if %{with mpich}
%files -n ptscotch-mpich
%license doc/CeCILL-C_V1-en.txt
%{_libdir}/mpich/lib/libptscotch.so.7.0.4
%{_libdir}/mpich/lib/libptesmumps.so.7.0.4
%{_libdir}/mpich/lib/libscotch.so.7.0.4
%if %{with metis}
%{_libdir}/mpich/lib/libscotchmetisv3.so
%{_libdir}/mpich/lib/libscotchmetisv5.so
%{_libdir}/mpich/lib/libptscotchparmetisv3.so
%endif
%{_libdir}/mpich/lib/libptscotcherr.so
%{_libdir}/mpich/lib/libptscotcherrexit.so
%{_libdir}/mpich/lib/libscotcherr.so
%{_libdir}/mpich/lib/libscotcherrexit.so

%files -n ptscotch-mpich-devel
%dir %{_includedir}/mpich*/scotch
%{_includedir}/mpich*/scotch/ptscotch.h
%{_includedir}/mpich*/scotch/ptscotchf.h
%{_includedir}/mpich*/scotch/scotch.h
%{_includedir}/mpich*/scotch/scotchf.h
%{_includedir}/mpich*/scotch/esmumps.h
%{_libdir}/mpich/lib/libptscotch.so
%{_libdir}/mpich/lib/libscotch.so
%{_libdir}/mpich/lib/libesmumps.so
%{_libdir}/mpich/lib/libptesmumps.so
%dir %{_libdir}/mpich/lib/cmake/scotch/
%{_libdir}/mpich/lib/cmake/scotch/ptesmumpsTargets*
%{_libdir}/mpich/lib/cmake/scotch/SCOTCHConfig.cmake
%{_libdir}/mpich/lib/cmake/scotch/SCOTCHConfigVersion.cmake
%{_libdir}/mpich/lib/cmake/scotch/esmumpsTargets*
%{_libdir}/mpich/lib/cmake/scotch/ptscotchTargets*
%{_libdir}/mpich/lib/cmake/scotch/ptscotcherrTargets*
%{_libdir}/mpich/lib/cmake/scotch/ptscotcherrexitTargets*
%{_libdir}/mpich/lib/cmake/scotch/scotchTargets*
%{_libdir}/mpich/lib/cmake/scotch/scotcherrTargets*
%{_libdir}/mpich/lib/cmake/scotch/scotcherrexitTargets*

%if %{with metis}
%files -n ptscotch-mpich-devel-parmetis
%dir %{_includedir}/mpich*/scotch
%{_includedir}/mpich*/scotch/scotchmetis.h
%{_includedir}/mpich*/scotch/scotchmetisf.h
%{_includedir}/mpich*/scotch/parmetis.h
%{_libdir}/mpich/lib/libparmetis.so
%{_libdir}/mpich/lib/libptscotchparmetis.so
%{_libdir}/mpich/lib/libscotchmetis.so
%{_libdir}/mpich/lib/cmake/scotch/ptscotchparmetisTargets*
%{_libdir}/mpich/lib/cmake/scotch/scotchmetisTargets*
%endif
%endif


%if %{with openmpi}
%files -n ptscotch-openmpi
%license doc/CeCILL-C_V1-en.txt
%{_libdir}/openmpi/lib/libptscotch.so.7.0.4
%{_libdir}/openmpi/lib/libptesmumps.so.7.0.4
%{_libdir}/openmpi/lib/libscotch.so.7.0.4
%if %{with metis}
%{_libdir}/openmpi/lib/libscotchmetisv3.so
%{_libdir}/openmpi/lib/libscotchmetisv5.so
%{_libdir}/openmpi/lib/libptscotchparmetisv3.so
%endif
%{_libdir}/openmpi/lib/libptscotcherr.so
%{_libdir}/openmpi/lib/libptscotcherrexit.so
%{_libdir}/openmpi/lib/libscotcherr.so
%{_libdir}/openmpi/lib/libscotcherrexit.so

%files -n ptscotch-openmpi-devel
%dir %{_includedir}/openmpi*/scotch
%{_includedir}/openmpi*/scotch/ptscotch.h
%{_includedir}/openmpi*/scotch/ptscotchf.h
%{_includedir}/openmpi*/scotch/scotch.h
%{_includedir}/openmpi*/scotch/scotchf.h
%{_includedir}/openmpi*/scotch/esmumps.h
%{_libdir}/openmpi/lib/libptscotch.so
%{_libdir}/openmpi/lib/libscotch.so
%{_libdir}/openmpi/lib/libesmumps.so
%{_libdir}/openmpi/lib/libptesmumps.so
%dir %{_libdir}/openmpi/lib/cmake/scotch/
%{_libdir}/openmpi/lib/cmake/scotch/ptesmumpsTargets*
%{_libdir}/openmpi/lib/cmake/scotch/SCOTCHConfig.cmake
%{_libdir}/openmpi/lib/cmake/scotch/SCOTCHConfigVersion.cmake
%{_libdir}/openmpi/lib/cmake/scotch/esmumpsTargets*
%{_libdir}/openmpi/lib/cmake/scotch/ptscotchTargets*
%{_libdir}/openmpi/lib/cmake/scotch/ptscotcherrTargets*
%{_libdir}/openmpi/lib/cmake/scotch/ptscotcherrexitTargets*
%{_libdir}/openmpi/lib/cmake/scotch/scotchTargets*
%{_libdir}/openmpi/lib/cmake/scotch/scotcherrTargets*
%{_libdir}/openmpi/lib/cmake/scotch/scotcherrexitTargets*

%if %{with metis}
%files -n ptscotch-openmpi-devel-parmetis
%dir %{_includedir}/openmpi*/scotch
%{_includedir}/openmpi*/scotch/scotchmetis.h
%{_includedir}/openmpi*/scotch/scotchmetisf.h
%{_includedir}/openmpi*/scotch/parmetis.h
%{_libdir}/openmpi/lib/libparmetis.so
%{_libdir}/openmpi/lib/libptscotchparmetis.so
%{_libdir}/openmpi/lib/libscotchmetis.so
%{_libdir}/openmpi/lib/cmake/scotch/ptscotchparmetisTargets*
%{_libdir}/openmpi/lib/cmake/scotch/scotchmetisTargets*
%endif
%endif


%changelog
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 02 2024 Sandro Mani <manisandro@gmail.com> - 7.0.4-4
- Fix libscotcherr, libscotcherrexit which should not be in -devel

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Oct 29 2023 Orion Poplawski <orion@nwra.com> - 7.0.4-2
- Rebuild for openmpi 5.0.0, drops support for i686

* Wed Aug 16 2023 Sandro Mani <manisandro@gmail.com> - 7.0.4-1
- Update to 7.0.4

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 13 2023 Antonio Trande <sagitter@fedoraproject.org> - 7.0.3-2
- Undefine _ld_as_needed

* Thu Apr 13 2023 Antonio Trande <sagitter@fedoraproject.org> - 7.0.3-1
- Update to 7.0.3
- Patch0 updated
- Rename internal Metis include files to avoid conflicts

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 13 2021 Sandro Mani <manisandro@gmail.com> - 6.1.2-1
- Update to 6.1.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 24 2021 Sandro Mani <manisandro@gmail.com> - 6.1.1-1
- Update to 6.1.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 08 2020 Sandro Mani <manisandro@gmail.coM> - 6.1.0-1
- Update to 6.1.0

* Wed Sep 02 2020 Sandro Mani <manisandro@gmail.com> - 6.0.10-1
- Update to 6.0.10

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Sandro Mani <manisandro@gmail.com> - 6.0.9-1
- Update to 6.0.9

* Tue Aug 27 2019 Sandro Mani <manisandro@gmail.com> - 6.0.8-1
- Update to 6.0.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 20 2019 Sandro Mani <manisandro@gmail.com> - 6.0.7-1
- Update to 6.0.7

* Fri Apr 12 2019 Jerry James <loganjerry@gmail.com> - 6.0.6-6
- Fix underlinked libraries (bz 1680315)
- Fix too-long description line
- Drop ancient obsoletes
- Add check script
- Fix undefined macros in man pages

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 6.0.6-5
- Rebuild for openmpi 3.1.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 16 2018 Orion Poplawski <orion@cnwra.com> - 6.0.6-3
- Make shared libraries link properly with -Wl,--as-needed

* Sat Dec 1 2018 Orion Poplawski <orion@cnwra.com> - 6.0.6-2
- Drop BR lzma, use xz for lzma support

* Mon Jul 16 2018 Sandro Mani <manisandro@gmail.com> - 6.0.6-1
- Update to 6.0.6

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 12 2018 Sandro Mani <manisandro@gmail.com> - 6.0.5-1
- Update to 6.0.5

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 27 2016 Sandro Mani <manisandro@gmail.com> - 6.0.4-13
- Drop -DSCOTCH_PTHREAD (#1386707)

* Mon Oct 24 2016 Dan Horák <dan[at]danny.cz> - 6.0.4-12
- drop ExcludeArch

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 6.0.4-11
- Rebuild for openmpi 2.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Sandro Mani <manisandro@gmail.com> - 6.0.4-9
- Install parmetis.h in separate package

* Tue Dec 01 2015 Than Ngo <than@redhat.com> - 6.0.4-8
- ExcludeArch: s390 s390x

* Thu Nov 26 2015 Dave Love <loveshack@fedoraproject.org> - 6.0.4-7
- Install parmetis.h
- Conditionalize %%license and %%__global_ldflags

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.4-6
- Rebuild for openmpi 1.10.0

* Sat Aug 15 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 6.0.4-5
- Rebuild for MPI provides

* Sun Jul 26 2015 Sandro Mani <manisandro@gmail.com> - 6.0.4-4
- Rebuild for RPM MPI Requires Provides Change

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May  3 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 6.0.4-2
- Rebuild for changed mpich

* Sat Mar 14 2015 Sandro Mani <manisandro@gmail.com> - 6.0.4-1
- Update to 6.0.4

* Thu Mar 12 2015 Sandro Mani <manisandro@gmail.com> - 6.0.3-4
- Rebuild (mpich)

* Mon Dec 01 2014 Sandro Mani <manisandro@gmail.com> - 6.0.3-2
- Build esmumps

* Wed Nov 05 2014 Sandro Mani <manisandro@gmail.com> - 6.0.3-1
- Update to 6.0.3

* Mon Sep 22 2014 Sandro Mani <manisandro@gmail.com> - 6.0.1-1
- Update to 6.0.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Sandro Mani <manisandro@gmail.com> - 6.0.0-8
- Rework specfile

* Sat Jul 05 2014 Sandro Mani <manisandro@gmail.com> - 6.0.0-7
- Fix under-linked libraries (#1098680)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Deji Akingunola <dakingun@gmail.com> - 6.0.0-5
- Slightly modified Erik Zeek spec re-write (See 2012-10-08 below)
- Rename mpich and openmpi subpackages as ptscotch-(mpich/openmpi) (Laurence Mcglashan)

* Mon Feb 24 2014 Deji Akingunola <dakingun@gmail.com> - 6.0.0-4
- Rebuild for mpich-3.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Deji Akingunola <dakingun@gmail.com> - 6.0.0-2
- Rename mpich2 sub-packages to mpich and rebuild for mpich-3.0

* Thu Jun 13 2013 Deji Akingunola <dakingun@gmail.com> - 6.0.0-1
- Update to 6.0.0
- Configured to run with 2 threads (for now)
- Install the headers in arch-dependent sub-directories

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.12-2.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Deji Akingunola <dakingun@gmail.com> - 5.1.12-1.b
- Update to 5.1.12b

* Mon Oct 08 2012 Erik Zeek <eczeek@sandia.gov> - 5.1.11-4
- Use internal build machinery to build shared libraries.
- A bunch of MPI love.
-   Install Mpich2 libraries in the proper path.
-   Provide Mpich2 and OpenMPI libraries.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 29 2011 Deji Akingunola <dakingun@gmail.com> - 5.1.11-1
- Update to 5.1.11

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.10b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 19 2010 Deji Akingunola <dakingun@gmail.com> - 5.1.10b-1
- Update to 5.1.10b

* Thu Aug 12 2010 Deji Akingunola <dakingun@gmail.com> - 5.1.9-1
- Update to 5.1.9
- No more static builds

* Tue Apr 27 2010 Deji Akingunola <dakingun@gmail.com> - 5.1.8-1
- Update to 5.1.8

* Wed Nov 04 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.7-2
- Fix the Source url

* Sun Sep 20 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.7-1
- Update to 5.1.7
- Put the library under libdir

* Thu Jun 11 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.6-3
- Further spec fixes from package review (convert license files to utf8)
- Prefix binaries and their corresponding manpages with scotch_ .
- Link in appropriates libraries when creating shared libs

* Thu Jun 04 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.6-2
- Add zlib-devel as BR

* Wed May 13 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.6-1
- Update to 5.1.6

* Fri Nov 21 2008 Deji Akingunola <dakingun@gmail.com> - 5.1.2-1
- Update to 5.1.2

* Fri Sep 19 2008 Deji Akingunola <dakingun@gmail.com> - 5.1.1-1
- initial package creation
