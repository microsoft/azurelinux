## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 8;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Copyright (c) 2014  Dave Love, University of Liverpool
# Copyright (c) 2018  Dave Love, University of Manchester
# MIT licence, per Fedora policy

%if 0%{?fedora} >= 40
%ifarch %{ix86}
%bcond_with openmpi
%else
%bcond_without openmpi
%endif
%else
%bcond_without openmpi
%endif

%bcond_without mpich
%bcond_without check
%bcond_without docs

%global somajor 2
%global soversion %{somajor}.1

Name:           hypre
Version:        2.32.0
Release:        %autorelease
Summary:        High performance matrix preconditioners
License:        Apache-2.0 OR MIT
URL:            http://www.llnl.gov/casc/hypre/
Source:         https://github.com/hypre-space/hypre/archive/v%version/%{name}-%{version}.tar.gz
# Don't use hostname for tests and use two MPI processes
Patch2:         hypre-2.32.0-test.patch

Patch3:         hypre-2.32.0_request_156.patch

BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
#BuildRequires:  automake
BuildRequires:  cmake
#BuildRequires:  libtool
#BuildRequires:  libtool-ltdl-devel
BuildRequires:  make
BuildRequires:  SuperLU-devel
BuildRequires:  flexiblas-devel
%if %{with docs}
BuildRequires:  doxygen-latex
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-theme-alabaster
BuildRequires:  python3-sphinx_rtd_theme
BuildRequires:  python3-breathe
BuildRequires:  python3-sphinx-latex
BuildRequires:  /usr/bin/latexmk
BuildRequires:  tex(threeparttable.sty)
BuildRequires:  tex(hanging.sty)
BuildRequires:  tex(adjustbox.sty)
BuildRequires:  tex(fncychap.sty)
BuildRequires:  tex(tabulary.sty)
BuildRequires:  tex(capt-of.sty)
BuildRequires:  tex(needspace.sty)
BuildRequires:  tex(stackengine.sty)
BuildRequires:  tex(listofitems.sty)
BuildRequires:  tex(ulem.sty)
BuildRequires:  tex(etoc.sty)
%endif

%global desc \
Hypre is a set of matrix preconditioning libraries to aid in the\
solution of large systems of linear equations.

%description
%desc

%package devel
Summary:        Development files for %name
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       SuperLU-devel%{?_isa} 
Requires:       flexiblas-devel%{?_isa}

%description devel
Development files for %name

%if %{with openmpi}
%package openmpi
Summary:        High performance matrix preconditioners - openmpi
Requires:       openmpi%{?_isa}
BuildRequires:  superlu_dist-openmpi-devel
BuildRequires:  ptscotch-openmpi-devel

%description openmpi
%desc

This is the openmpi version.

%package openmpi-devel
Summary:        Development files for %name-openmpi
Requires:       %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires:       openmpi-devel%{?_isa}
Requires:       superlu_dist-openmpi-devel%{?_isa}
Requires:       ptscotch-openmpi-devel%{?_isa}
Requires:       flexiblas-devel%{?_isa}

%description openmpi-devel
Development files for %name-openmpi
%endif

%if %{with mpich}
%package mpich
Summary:        High performance matrix preconditioners - mpich
Requires:       mpich%{?_isa}
BuildRequires:  superlu_dist-mpich-devel ptscotch-mpich-devel

%description mpich
%desc

This is the mpich version.

%package mpich-devel
Summary:        Development files for %name-mpich
Requires:       %{name}-mpich%{?_isa} = %{version}-%{release}
Requires:       mpich-devel%{?_isa}
Requires:       superlu_dist-mpich-devel%{?_isa}
Requires:       ptscotch-mpich-devel%{?_isa}
Requires:       flexiblas-devel%{?_isa}

%description mpich-devel
Development files for %name-mpich
%endif

%if %{with docs}
%package doc
Summary:        Documentation for hypre
BuildArch:      noarch

%description doc
Documentation for hypre
%endif


%prep
%setup -q -n %name-%version
%patch -P 2 -p1 -b .test
%patch -P 3 -p1 -b .backup

find \( -name \*.[ch] -o -name \*.cxx \) -perm /=x -exec chmod 0644 {} \;

%if %{with openmpi}
cp -a src openmpi
%endif
%if %{with mpich}
cp -a src mpich
%endif

%build
%if %{with docs}
pushd src
%configure
make -C docs
rm docs/usr-manual-html/.buildinfo
popd
%endif

pushd src/cmbuild
%cmake -S .. \
       -DHYPRE_WITH_EXTRA_CFLAGS:STRING=" -O3" -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} -lsuperlu -fopenmp" \
       -DHYPRE_BUILD_EXAMPLES:BOOL=ON -DHYPRE_BUILD_TESTS:BOOL=ON -DHYPRE_BUILD_TYPE:STRING=Release \
       -DHYPRE_ENABLE_SHARED:BOOL=ON -DHYPRE_WITH_OPENMP:BOOL=ON \
       -DHYPRE_SEQUENTIAL:BOOL=ON -DHYPRE_WITH_MPI:BOOL=OFF -DHYPRE_WITH_DSUPERLU:BOOL=OFF \
       -DHYPRE_WITH_SUPERLU:BOOL=ON -DTPL_SUPERLU_INCLUDE_DIRS:FILEPATH=%{_includedir}/SuperLU -DTPL_SUPERLU_LIBRARIES:STRING=%{_libdir}/libsuperlu.so \
       -DTPL_BLAS_LIBRARIES:STRING=-lflexiblas \
       -DHYPRE_WITH_OPENMP:BOOL=ON -DHYPRE_TIMING:BOOL=ON -DHYPRE_INSTALL_PREFIX:PATH=%{_libdir} -DHYPRE_INSTALL_INCLUDEDIR:PATH=%{_includedir}/%{name}
%cmake_build
popd

%if %{with openmpi}
pushd openmpi/cmbuild
%_openmpi_load
export CC=$MPI_BIN/mpicc
%cmake -S .. \
       -DHYPRE_WITH_EXTRA_CFLAGS:STRING=" -O3" -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} -fopenmp -lsuperlu_dist -lptscotch" \
       -DHYPRE_BUILD_EXAMPLES:BOOL=ON -DHYPRE_BUILD_TESTS:BOOL=ON -DHYPRE_BUILD_TYPE:STRING=Release \
       -DHYPRE_ENABLE_SHARED:BOOL=ON -DHYPRE_WITH_OPENMP:BOOL=ON \
       -DHYPRE_SEQUENTIAL:BOOL=OFF -DHYPRE_WITH_MPI:BOOL=ON -DMPI_C_COMPILER:FILEPATH=$MPI_BIN/mpicc \
       -DHYPRE_WITH_SUPERLU:BOOL=ON -DTPL_SUPERLU_INCLUDE_DIRS:FILEPATH=$MPI_INCLUDE/superlu_dist -DTPL_SUPERLU_LIBRARIES:STRING=$MPI_LIB/libsuperlu_dist.so \
       -DTPL_BLAS_LIBRARIES:STRING=-lflexiblas \
       -DHYPRE_WITH_OPENMP:BOOL=ON -DHYPRE_TIMING:BOOL=ON -DHYPRE_INSTALL_PREFIX:PATH=%{_libdir}/openmpi/lib  -DHYPRE_INSTALL_INCLUDEDIR:PATH=$MPI_INCLUDE/%{name}
%cmake_build
popd
%_openmpi_unload
%endif

%if %{with mpich}
pushd mpich/cmbuild
%_mpich_load
export CC=$MPI_BIN/mpicc
%cmake -S .. \
       -DHYPRE_WITH_EXTRA_CFLAGS:STRING=" -O3" -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} -fopenmp -lsuperlu_dist -lptscotch" \
       -DHYPRE_BUILD_EXAMPLES:BOOL=ON -DHYPRE_BUILD_TESTS:BOOL=ON -DHYPRE_BUILD_TYPE:STRING=Release \
       -DHYPRE_ENABLE_SHARED:BOOL=ON -DHYPRE_WITH_OPENMP:BOOL=ON \
       -DHYPRE_SEQUENTIAL:BOOL=OFF -DHYPRE_WITH_MPI:BOOL=ON -DMPI_C_COMPILER:FILEPATH=$MPI_BIN/mpicc \
       -DHYPRE_WITH_SUPERLU:BOOL=ON -DTPL_SUPERLU_INCLUDE_DIRS:FILEPATH=$MPI_INCLUDE/superlu_dist -DTPL_SUPERLU_LIBRARIES:STRING=$MPI_LIB/libsuperlu_dist.so \
       -DTPL_BLAS_LIBRARIES:STRING=-lflexiblas \
       -DHYPRE_WITH_OPENMP:BOOL=ON -DHYPRE_TIMING:BOOL=ON -DHYPRE_INSTALL_PREFIX:PATH=%{_libdir}/mpich/lib -DHYPRE_INSTALL_INCLUDEDIR:PATH=$MPI_INCLUDE/%{name}
%cmake_build
%_mpich_unload
popd
%endif


%check
%if %{with check}
pushd src/cmbuild/%_vpath_builddir/test
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
./ij*
popd
%if %{with openmpi}
pushd openmpi/cmbuild/%_vpath_builddir/test
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}/openmpi/lib
%_openmpi_load
./ij*
%_openmpi_unload
popd
%endif
%if %{with mpich}
pushd mpich/cmbuild/%_vpath_builddir/test
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}/mpich/lib
%_mpich_load
./ij*
%_mpich_unload
popd
%endif
%endif


%install
pushd src/cmbuild
%cmake_install
popd

%if %{with openmpi}
pushd openmpi/cmbuild
%_openmpi_load
%cmake_install
%_openmpi_unload
popd
%endif

%if %{with mpich}
pushd mpich/cmbuild
%_mpich_load
%cmake_install
%_mpich_unload
popd
%endif

%files
%doc CHANGELOG README.md
%license COPYRIGHT LICENSE-*
%{_libdir}/libHYPRE.so.%{somajor}*

%files devel
%{_libdir}/libHYPRE.so
%{_includedir}/%{name}/
%{_libdir}/cmake/HYPRE/

%if %{with openmpi}
%files openmpi
%doc CHANGELOG README.md
%license COPYRIGHT LICENSE-*
%{_libdir}/openmpi/lib/libHYPRE.so.%{somajor}*

%files openmpi-devel
%{_libdir}/openmpi/lib/libHYPRE.so
%{_includedir}/openmpi-%_arch/%{name}
%{_libdir}/openmpi/lib/cmake/HYPRE/
%endif

%if %{with mpich}
%files mpich
%doc CHANGELOG README.md
%license COPYRIGHT LICENSE-*
%{_libdir}/mpich/lib/libHYPRE.so.%{somajor}*

%files mpich-devel
%{_libdir}/mpich/lib/libHYPRE.so
%{_includedir}/mpich-%_arch/%{name}
%{_libdir}/mpich/lib/cmake/HYPRE/
%endif

%if %{with docs}
%files doc
%doc CHANGELOG README.md src/examples
%license COPYRIGHT LICENSE-*
%doc src/docs/usr-manual/*.pdf src/docs/*-manual-html
%endif

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.32.0-8
- test: add initial lock files

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Mar 02 2025 Christoph Junghans <junghans@votca.org> - 2.32.0-6
- fix superlu lib locations

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 20 2024 Antonio Trande <sagitter@fedoraproject.org> - 2.32.0-4
- Avoid make clean | Rebuild for MUMPS-5.7.3

* Fri Dec 20 2024 Antonio Trande <sagitter@fedoraproject.org> - 2.32.0-3
- Fix docs macros | Rebuild for MUMPS-5.7.3

* Fri Dec 20 2024 Antonio Trande <sagitter@fedoraproject.org> - 2.32.0-2
- Fix docs creation | Rebuild for MUMPS-5.7.3

* Fri Dec 20 2024 Antonio Trande <sagitter@fedoraproject.org> - 2.32.0-1
- Release 2.32.0|Use CMake method|Use always flexiblas

* Thu Sep 05 2024 Antonio Trande <sagitter@fedoraproject.org> - 2.24.0-19
- Rebuild for SuperLU-7.0.0

* Fri Aug 16 2024 Sandro Mani <manisandro@gmail.com> - 2.24.0-18
- Rebuild (scoch-7.0.4)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.24.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Apr 05 2024 Antonio Trande <sagitter@fedoraproject.org> - 2.24.0-16
- Rebuild in EPEL9

* Sat Mar 16 2024 Dave Love <loveshack@fedoraproject.org> - 2.24.0-15
- Fix licence (changed from LGPL to Apache 2 or MIT)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.24.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.24.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 16 2023 Antonio Trande <sagitter@fedoraproject.org> - 2.24.0-12
- Fix my name

* Sat Dec 16 2023 Antonio Trande <sagitter@fedoraproject.org> - 2.24.0-11
- Fix link commands

* Sat Dec 16 2023 Antonio Trande <sagitter@fedoraproject.org> - 2.24.0-10
- Disable openmpi on i686

* Sat Dec 16 2023 Antonio Trande <sagitter@fedoraproject.org> - 2.24.0-9
- Rebuild for superlu_dist-8.2.0

* Thu Aug 17 2023 Antonio Trande <sagitter@fedoraproject.org> - 2.24.0-8
- Rebuild for scotch-7.0.4

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.24.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 16 2023 Antonio Trande <sagitter@fedoraproject.org> - 2.24.0-6
- Rebuild for SuperLU-6.0.0

* Thu Apr 13 2023 Antonio Trande <sagitter@fedoraproject.org> - 2.24.0-5
- Rebuild for Scotch-7

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 03 2022 Antonio Trande <sagitter@fedoraproject.org> - 2.24.0-2
- Rebuild for superlu_dist-8.0.0

* Sat Apr 23 2022 Antonio Trande <sagitter@fedoraproject.org> - 2.24.0-1
- Release 2.24.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Oct 30 2021 Antonio Trande <sagitter@fedoraproject.org> - 2.18.2-6
- Rebuild for SuperLU-5.3.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 19 2020 Tom Stellard <tstellar@redhat.com> - 2.18.2-3
- Add BuildRequires: make

* Thu Aug 13 2020 Iñaki Úcar <iucar@fedoraproject.org> - 2.18.2-2
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Tue Aug 11 2020 Dave Love <loveshack@fedoraproject.org> - 2.18.2-1
- Configure with CC=mpicc to fix FTBFS (#1863655) - Update to 2.18.2

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Dave Love <loveshack@fedoraproject.org> - 2.18.1-1
- New version

* Wed Oct 09 2019 Dave Love <loveshack@fedoraproject.org> - 2.18.0-4
- Merge branch 'epel8'

* Wed Oct 09 2019 Dave Love <loveshack@fedoraproject.org> - 2.18.0-3
- Make libHYPRE.so.%%somajor links

* Tue Oct 08 2019 Dave Love <loveshack@fedoraproject.org> - 2.18.0-2
- Push new source

* Tue Oct 01 2019 Dave Love <loveshack@fedoraproject.org> - 2.18.0-1
- New version - Add minor version to soname

* Tue Sep 17 2019 Dave Love <loveshack@fedoraproject.org> - 2.17.0-1
- New version, with soname bump and licence change

* Mon Sep 16 2019 Dave Love <loveshack@fedoraproject.org> - 2.16.0-1
- New version from updated origin - Build docs; add BRs - Drop soname patch

* Thu Sep 12 2019 Orion Poplawski <orion@nwra.com> - 2.15.1-9
- Drop el6 conditionals, build openmpi for EL8

* Sat Sep 07 2019 Orion Poplawski <orion@nwra.com> - 2.15.1-8
- Drop old el6 conditionals

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 2.15.1-6
- Rebuild for openmpi 3.1.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Dave Love <loveshack@fedoraproject.org> - 2.15.1-4
- Revert omitting builtin BLAS, which is namedspaced

* Mon Dec 03 2018 Dave Love <loveshack@fedoraproject.org> - 2.15.1-3
- Fix FTBFS with current superlu_dist [#1654932] - Clean up configuration
  and avoid builtin BLAS

* Tue Nov 27 2018 Dave Love <loveshack@fedoraproject.org> - 2.15.1-2
- Adjust source URL

* Fri Nov 23 2018 Dave Love <loveshack@fedoraproject.org> - 2.15.1-1
- New version, removing hypre_PFMGSetupInterpOp_CC0, hypre_finalize,
  hypre_init, which appear actually to be internal, so soname unchanged -
  Avoid tests

* Thu Jul 19 2018 Sandro Mani <manisandro@gmail.com> - 2.14.0-4
- Rebuild (scotch)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 26 2018 Dave Love <loveshack@fedoraproject.org> - 2.14.0-2
- Build hypre-openmpi on s390x (#1571450)

* Mon Mar 26 2018 Dave Love <loveshack@fedoraproject.org> - 2.14.0-1
- Update to 2.14.0 (#1557645) Reinstate superlu and use superlu_dist

* Sat Mar 24 2018 Dave Love <loveshack@fedoraproject.org> - 2.13.0-9
- New source

* Thu Mar 08 2018 Adam Williamson <awilliam@redhat.com> - 2.13.0-8
- Rebuild to fix GCC 8 mis-compilation

* Fri Feb 16 2018 Dave Love <loveshack@fedoraproject.org> - 2.13.0-7
- Fix openblas BR (#1545197)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 06 2017 Dave Love <loveshack@fedoraproject.org> - 2.13.0-5
- Disable tests on ix86 temporarily

* Sun Nov 05 2017 Dave Love <loveshack@fedoraproject.org> - 2.13.0-4
- Revert last change in favour of updated superlu_dist

* Fri Nov 03 2017 Dave Love <loveshack@fedoraproject.org> - 2.13.0-3
- Fix link failure against parmetis

* Fri Nov 03 2017 Dave Love <loveshack@fedoraproject.org> - 2.13.0-2
- Fix sources

* Thu Nov 02 2017 Dave Love <loveshack@fedoraproject.org> - 2.13.0-1
- New version Configure --with-mli for compatibility Configure with superlu
  Remove -Dhypre_dgesvd=dgesvd_ bodge Bump soname major version (due to
  added elements in structs)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-4
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.11.2-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Thu May 04 2017 Dave Love <loveshack@fedoraproject.org> - 2.11.2-1
- New version

* Wed Mar 15 2017 Orion Poplawski <orion@cora.nwra.com> - 2.11.1-8
- Build with openblas on all available architectures

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 02 2016 Dave Love <d.love@liverpool.ac.uk> - 2.11.1-6
- Fix spurious newline

* Fri Dec 02 2016 Dave Love <d.love@liverpool.ac.uk>
- Conditionalize mpich-devel%%{?_isa}

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 2.11.1-4
- Rebuild for openmpi 2.0

* Sat Jul 23 2016 Dave Love <d.love@liverpool.ac.uk> - 2.11.1-3
- Initial checkin

* Wed Sep 18 2019 Dave Love <loveshack@fedoraproject.org> - 2.17.0-2
- Docs won't build on el8

* Tue Sep 17 2019 Dave Love <loveshack@fedoraproject.org> - 2.17.0-1
- Merge branch 'master' into epel8

* Thu Sep 12 2019 Orion Poplawski <orion@nwra.com> - 2.15.1-10
- Add package.cfg file

* Thu Sep 12 2019 Orion Poplawski <orion@nwra.com> - 2.15.1-9
- Drop el6 conditionals, build openmpi for EL8

* Sat Sep 07 2019 Orion Poplawski <orion@nwra.com> - 2.15.1-8
- Drop old el6 conditionals

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 2.15.1-6
- Rebuild for openmpi 3.1.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Dave Love <loveshack@fedoraproject.org> - 2.15.1-4
- Revert omitting builtin BLAS, which is namedspaced

* Mon Dec 03 2018 Dave Love <loveshack@fedoraproject.org> - 2.15.1-3
- Fix FTBFS with current superlu_dist [#1654932] - Clean up configuration
  and avoid builtin BLAS

* Tue Nov 27 2018 Dave Love <loveshack@fedoraproject.org> - 2.15.1-2
- Adjust source URL

* Fri Nov 23 2018 Dave Love <loveshack@fedoraproject.org> - 2.15.1-1
- New version, removing hypre_PFMGSetupInterpOp_CC0, hypre_finalize,
  hypre_init, which appear actually to be internal, so soname unchanged -
  Avoid tests

* Thu Jul 19 2018 Sandro Mani <manisandro@gmail.com> - 2.14.0-4
- Rebuild (scotch)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 26 2018 Dave Love <loveshack@fedoraproject.org> - 2.14.0-2
- Build hypre-openmpi on s390x (#1571450)

* Mon Mar 26 2018 Dave Love <loveshack@fedoraproject.org> - 2.14.0-1
- Update to 2.14.0 (#1557645) Reinstate superlu and use superlu_dist

* Sat Mar 24 2018 Dave Love <loveshack@fedoraproject.org> - 2.13.0-9
- New source

* Thu Mar 08 2018 Adam Williamson <awilliam@redhat.com> - 2.13.0-8
- Rebuild to fix GCC 8 mis-compilation

* Fri Feb 16 2018 Dave Love <loveshack@fedoraproject.org> - 2.13.0-7
- Fix openblas BR (#1545197)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 06 2017 Dave Love <loveshack@fedoraproject.org> - 2.13.0-5
- Disable tests on ix86 temporarily

* Sun Nov 05 2017 Dave Love <loveshack@fedoraproject.org> - 2.13.0-4
- Revert last change in favour of updated superlu_dist

* Fri Nov 03 2017 Dave Love <loveshack@fedoraproject.org> - 2.13.0-3
- Fix link failure against parmetis

* Fri Nov 03 2017 Dave Love <loveshack@fedoraproject.org> - 2.13.0-2
- Fix sources

* Thu Nov 02 2017 Dave Love <loveshack@fedoraproject.org> - 2.13.0-1
- New version Configure --with-mli for compatibility Configure with superlu
  Remove -Dhypre_dgesvd=dgesvd_ bodge Bump soname major version (due to
  added elements in structs)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-4
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.11.2-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Thu May 04 2017 Dave Love <loveshack@fedoraproject.org> - 2.11.2-1
- New version

* Wed Mar 15 2017 Orion Poplawski <orion@cora.nwra.com> - 2.11.1-6
- Build with openblas on all available architectures

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 02 2016 Dave Love <d.love@liverpool.ac.uk> - 2.11.1-4
- Fix spurious newline

* Fri Dec 02 2016 Dave Love <d.love@liverpool.ac.uk>
- Conditionalize mpich-devel%%{?_isa}

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 2.11.1-2
- Rebuild for openmpi 2.0

* Sat Jul 23 2016 Dave Love <d.love@liverpool.ac.uk> - 2.11.1-1
- Initial checkin
## END: Generated by rpmautospec
