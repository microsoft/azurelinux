# build without mpich and openmpi support
%bcond_with mpich
%bcond_with openmpi
%if %{with mpich}
%global mpi_list %{?mpi_list} mpich
%endif
%if %{with openmpi}
%global mpi_list %{?mpi_list} openmpi
%endif
%global sover 19

Summary:        Libraries for the Unidata network Common Data Form
Name:           netcdf
Version:        4.9.0
Release:        4%{?dist}
License:        NetCDF
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.unidata.ucar.edu/software/netcdf/
Source0:        https://github.com/Unidata/netcdf-c/archive/v%{version}/%{name}-%{version}.tar.gz
# Fix plugins - https://github.com/Unidata/netcdf-c/pull/2431
Patch0:         netcdf-plugin.patch

BuildRequires:  blosc-devel
BuildRequires:  chrpath
BuildRequires:  curl-devel
BuildRequires:  doxygen
BuildRequires:  gawk
BuildRequires:  hdf-static
BuildRequires:  hdf5-devel
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  libzstd-devel
BuildRequires:  m4
BuildRequires:  make
#mpiexec segfaults if ssh is not present
#https://trac.mcs.anl.gov/projects/mpich2/ticket/1576
BuildRequires:  openssh-clients
BuildRequires:  zlib-devel
Requires:       hdf5%{?_isa} = %{_hdf5_version}
%ifarch %{valgrind_arches}
BuildRequires:  valgrind
%endif

%description
NetCDF (network Common Data Form) is an interface for array-oriented
data access and a freely-distributed collection of software libraries
for C, Fortran, C++, and perl that provides an implementation of the
interface.  The NetCDF library also defines a machine-independent
format for representing scientific data.  Together, the interface,
library, and format support the creation, access, and sharing of
scientific data. The NetCDF software was developed at the Unidata
Program Center in Boulder, Colorado.

NetCDF data is:

   o Self-Describing: A NetCDF file includes information about the
     data it contains.

   o Network-transparent:  A NetCDF file is represented in a form that
     can be accessed by computers with different ways of storing
     integers, characters, and floating-point numbers.

   o Direct-access:  A small subset of a large dataset may be accessed
     efficiently, without first reading through all the preceding
     data.

   o Appendable:  Data can be appended to a NetCDF dataset along one
     dimension without copying the dataset or redefining its
     structure. The structure of a NetCDF dataset can be changed,
     though this sometimes causes the dataset to be copied.

   o Sharable:  One writer and multiple readers may simultaneously
     access the same NetCDF file.

%package devel
Summary:        Development files for netcdf
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       curl-devel%{?_isa}
Requires:       hdf5-devel%{?_isa}
Requires:       pkgconfig%{?_isa}

%description devel
This package contains the netCDF C header files, shared devel libs, and
man pages.

%package static
Summary:        Static libs for netcdf
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description static
This package contains the netCDF C static libs.

%if %{with mpich}
%package mpich
Summary:        NetCDF mpich libraries
BuildRequires:  hdf5-mpich-devel >= 1.8.4
BuildRequires:  mpich-devel
Requires:       hdf5-mpich%{?_isa} = %{_hdf5_version}
Provides:       %{name}-mpich2 = %{version}-%{release}
Obsoletes:      %{name}-mpich2 < 4.3.0-4

%description mpich
NetCDF parallel mpich libraries

%package mpich-devel
Summary:        NetCDF mpich development files
Requires:       %{name}-mpich%{?_isa} = %{version}-%{release}
Requires:       curl-devel%{?_isa}
Requires:       hdf5-mpich-devel%{?_isa}
Requires:       pkgconfig%{?_isa}
Provides:       %{name}-mpich2-devel = %{version}-%{release}
Obsoletes:      %{name}-mpich2-devel < 4.3.0-4

%description mpich-devel
NetCDF parallel mpich development files

%package mpich-static
Summary:        NetCDF mpich static libraries
Requires:       %{name}-mpich-devel%{?_isa} = %{version}-%{release}
Provides:       %{name}-mpich2-static = %{version}-%{release}
Obsoletes:      %{name}-mpich2-static < 4.3.0-4

%description mpich-static
NetCDF parallel mpich static libraries
%endif


%if %{with openmpi}
%package openmpi
Summary:        NetCDF openmpi libraries
BuildRequires:  hdf5-openmpi-devel >= 1.8.4
BuildRequires:  openmpi-devel
Requires:       hdf5-openmpi%{?_isa} = %{_hdf5_version}

%description openmpi
NetCDF parallel openmpi libraries

%package openmpi-devel
Summary:        NetCDF openmpi development files
Requires:       %{name}-openmpi%{_isa} = %{version}-%{release}
Requires:       curl-devel%{?_isa}
Requires:       hdf5-openmpi-devel%{?_isa}
Requires:       openmpi-devel%{?_isa}
Requires:       pkgconfig%{?_isa}

%description openmpi-devel
NetCDF parallel openmpi development files

%package openmpi-static
Summary:        NetCDF openmpi static libraries
Requires:       %{name}-openmpi-devel%{?_isa} = %{version}-%{release}

%description openmpi-static
NetCDF parallel openmpi static libraries
%endif


%prep
%autosetup -p1 -n %{name}-c-%{version}
# For Patch0
./bootstrap


%build
#Do out of tree builds
%global _configure ../configure
#Common configure options
export LDFLAGS="%{__global_ldflags} -L%{_libdir}/hdf"
export CFLAGS="%{optflags} -fno-strict-aliasing"
%global configure_opts \\\
           --enable-shared \\\
           --enable-netcdf-4 \\\
           --enable-dap \\\
           --enable-extra-example-tests \\\
           CPPFLAGS="-I%{_includedir}/hdf -DH5_USE_110_API" \\\
           LIBS="-ltirpc" \\\
           --enable-hdf4 \\\
           --disable-dap-remote-tests \\\
%{nil}

# Serial build
mkdir build
pushd build
ln -s ../configure .
%configure %{configure_opts} \
  --with-plugin-dir=%{_libdir}/hdf5/plugin
# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(.*g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool
%make_build
popd

# MPI builds
%if %{with mpich} || %{with openmpi}
for mpi in %{mpi_list}
do
  mkdir $mpi
  pushd $mpi
  module load mpi/$mpi-%{_arch}
  ln -s ../configure .
  # parallel tests hang on s390(x)
  %configure %{configure_opts} \
    CC=mpicc \
    --libdir=%{_libdir}/$mpi/lib \
    --bindir=%{_libdir}/$mpi/bin \
    --sbindir=%{_libdir}/$mpi/sbin \
    --includedir=%{_includedir}/$mpi-%{_arch} \
    --datarootdir=%{_libdir}/$mpi/share \
    --mandir=%{_libdir}/$mpi/share/man \
    --with-plugin-dir=%{_libdir}/$mpi/hdf5/plugin \
    --enable-parallel-tests
  # Get rid of undesirable hardcoded rpaths; workaround libtool reordering
  # -Wl,--as-needed after all the libraries.
  sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
      -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
      -e 's|CC="\(.*g..\)"|CC="\1 -Wl,--as-needed"|' \
      -i libtool
  %make_build
  module purge
  popd
done
%endif

%install
make -C build install DESTDIR=%{buildroot}
pushd %{buildroot}%{_libdir}
/bin/rm -f *.la
popd
chrpath --delete %{buildroot}/%{_bindir}/nc{copy,dump,gen,gen3}
/bin/rm -f %{buildroot}%{_infodir}/dir
%if %{with mpich} || %{with openmpi}
for mpi in %{mpi_list}
do
  module load mpi/$mpi-%{_arch}
  make -C $mpi install DESTDIR=%{buildroot}
  pushd %{buildroot}%{_libdir}/%{_libdir}/$mpi/lib
  rm *.la
  popd
  chrpath --delete %{buildroot}/%{_libdir}/$mpi/bin/nc{copy,dump,gen,gen3}
  module purge
done
%endif


%check
# Set to 1 to fail if tests fail
%ifarch %{ix86} s390x
# tst_filter fails on s390x
# https://github.com/Unidata/netcdf-c/issues/1338
# i686 - Testing parallel I/O with zlib compression...malloc(): invalid size (unsorted)
# https://github.com/Unidata/netcdf-c/issues/1685
fail=0
%else
fail=1
%endif
make -C build check || ( cat build/*/test-suite.log && exit $fail )
# Allow openmpi to run with more processes than cores
export OMPI_MCA_rmaps_base_oversubscribe=1
# openmpi test hangs on armv7hl in h5_test after tst_h_rename
%ifnarch armv7hl
%if %{with mpich} || %{with openmpi}
for mpi in %{mpi_list}
do
  module load mpi/$mpi-%{_arch}
  make -C $mpi check || ( cat $mpi/*/test-suite.log && exit $fail )
  module purge
done
%endif
%endif


%ldconfig_scriptlets


%files
%license COPYRIGHT
%doc README.md RELEASE_NOTES.md
%{_bindir}/nccopy
%{_bindir}/ncdump
%{_bindir}/ncgen
%{_bindir}/ncgen3
%{_bindir}/nc4print
%{_bindir}/ocprint
%{_libdir}/hdf5/plugin/lib__nch5deflate.so
%{_libdir}/hdf5/plugin/lib__nch5shuffle.so
%{_libdir}/hdf5/plugin/lib__nch5bzip2.so
%{_libdir}/hdf5/plugin/lib__nch5zstd.so
%{_libdir}/hdf5/plugin/lib__nch5szip.so
%{_libdir}/hdf5/plugin/lib__nczhdf5filters.so
%{_libdir}/hdf5/plugin/lib__nczstdfilters.so
%{_libdir}/hdf5/plugin/lib__nch5fletcher32.so
%{_libdir}/hdf5/plugin/lib__nch5blosc.so
%{_libdir}/hdf5/plugin/lib__nch5blosc.la
%{_libdir}/hdf5/plugin/lib__nch5bzip2.la
%{_libdir}/hdf5/plugin/lib__nch5deflate.la
%{_libdir}/hdf5/plugin/lib__nch5fletcher32.la
%{_libdir}/hdf5/plugin/lib__nch5shuffle.la
%{_libdir}/hdf5/plugin/lib__nch5szip.la
%{_libdir}/hdf5/plugin/lib__nch5zstd.la
%{_libdir}/hdf5/plugin/lib__nczhdf5filters.la
%{_libdir}/hdf5/plugin/lib__nczstdfilters.la
%{_libdir}/*.so.%{sover}*
%{_mandir}/man1/*

%files devel
%doc examples
%{_bindir}/nc-config
%{_includedir}/netcdf.h
%{_includedir}/netcdf_aux.h
%{_includedir}/netcdf_dispatch.h
%{_includedir}/netcdf_filter.h
%{_includedir}/netcdf_filter_build.h
%{_includedir}/netcdf_filter_hdf5_build.h
%{_includedir}/netcdf_json.h
%{_includedir}/netcdf_meta.h
%{_includedir}/netcdf_mem.h
%{_libdir}/libnetcdf.settings
%{_libdir}/*.so
%{_libdir}/pkgconfig/netcdf.pc
%{_mandir}/man3/*

%files static
%{_libdir}/*.a

%if %{with mpich}
%files mpich
%license COPYRIGHT
%doc README.md RELEASE_NOTES.md
%{_libdir}/mpich/bin/nccopy
%{_libdir}/mpich/bin/ncdump
%{_libdir}/mpich/bin/ncgen
%{_libdir}/mpich/bin/ncgen3
%{_libdir}/mpich/bin/nc4print
%{_libdir}/mpich/bin/ocprint
%{_libdir}/mpich/hdf5/plugin/*
%{_libdir}/mpich/lib/*.so.%{sover}*
%doc %{_libdir}/mpich/share/man/man1/*.1*

%files mpich-devel
%{_libdir}/mpich/bin/nc-config
%{_includedir}/mpich-%{_arch}/netcdf.h
%{_includedir}/mpich-%{_arch}/netcdf_aux.h
%{_includedir}/mpich-%{_arch}/netcdf_dispatch.h
%{_includedir}/mpich-%{_arch}/netcdf_filter.h
%{_includedir}/mpich-%{_arch}/netcdf_filter_build.h
%{_includedir}/mpich-%{_arch}/netcdf_filter_hdf5_build.h
%{_includedir}/mpich-%{_arch}/netcdf_json.h
%{_includedir}/mpich-%{_arch}/netcdf_meta.h
%{_includedir}/mpich-%{_arch}/netcdf_mem.h
%{_includedir}/mpich-%{_arch}/netcdf_par.h
%{_libdir}/mpich/lib/libnetcdf.settings
%{_libdir}/mpich/lib/*.so
%{_libdir}/mpich/lib/pkgconfig/%{name}.pc
%doc %{_libdir}/mpich/share/man/man3/*.3*

%files mpich-static
%{_libdir}/mpich/lib/*.a
%endif

%if %{with openmpi}
%files openmpi
%license COPYRIGHT
%doc README.md RELEASE_NOTES.md
%{_libdir}/openmpi/bin/nccopy
%{_libdir}/openmpi/bin/ncdump
%{_libdir}/openmpi/bin/ncgen
%{_libdir}/openmpi/bin/ncgen3
%{_libdir}/openmpi/bin/nc4print
%{_libdir}/openmpi/bin/ocprint
%{_libdir}/openmpi/hdf5/plugin/*
%{_libdir}/openmpi/lib/*.so.%{sover}*
%doc %{_libdir}/openmpi/share/man/man1/*.1*

%files openmpi-devel
%{_libdir}/openmpi/bin/nc-config
%{_includedir}/openmpi-%{_arch}/netcdf.h
%{_includedir}/openmpi-%{_arch}/netcdf_aux.h
%{_includedir}/openmpi-%{_arch}/netcdf_dispatch.h
%{_includedir}/openmpi-%{_arch}/netcdf_filter.h
%{_includedir}/openmpi-%{_arch}/netcdf_filter_build.h
%{_includedir}/openmpi-%{_arch}/netcdf_filter_hdf5_build.h
%{_includedir}/openmpi-%{_arch}/netcdf_json.h
%{_includedir}/openmpi-%{_arch}/netcdf_meta.h
%{_includedir}/openmpi-%{_arch}/netcdf_mem.h
%{_includedir}/openmpi-%{_arch}/netcdf_par.h
%{_libdir}/openmpi/lib/libnetcdf.settings
%{_libdir}/openmpi/lib/*.so
%{_libdir}/openmpi/lib/pkgconfig/%{name}.pc
%doc %{_libdir}/openmpi/share/man/man3/*.3*

%files openmpi-static
%{_libdir}/openmpi/lib/*.a
%endif


%changelog
* Thu Aug 10 2023 Archana Choudhary <archana1@microsoft.com> - 4.9.0-4
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Orion Poplawski <orion@nwra.com> - 4.9.0-2
- Build with libzstd-devel

* Sun Jun 26 2022 Orion Poplawski <orion@nwra.com> - 4.9.0-1
- Update to 4.9.0
- Make -Wl,--as-needed work

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Nov 21 2021 Orion Poplawski <orion@nwra.com> - 4.8.1-2
- Rebuild for hdf5 1.12.1

* Tue Aug 24 2021 Orion Poplawski <orion@nwra.com> - 4.8.1-1
- Update to 4.8.1

* Mon Aug 09 2021 Orion Poplawski <orion@nwra.com> - 4.8.0-1
- Update to 4.8.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 18 2021 Orion Poplawski <orion@nwra.com> - 4.7.3-7
- Remove UCX workaround - fixed with ucx 1.9.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 15 2020 Jeff Law <law@redhat.com> - 4.7.3-5
- Use -fno-strict-aliasing as nxc.c is not strict-aliasing safe

* Sun Sep  6 2020 Orion Poplawski <orion@nwra.com> - 4.7.3-4
- Work around UCX segfault issue (FTBFS bz#1864189)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Orion Poplawski <orion@nwra.com> - 4.7.3-1
- Update to 4.7.3

* Thu Jun 25 2020 Orion Poplawski <orion@cora.nwra.com> - 4.7.0-4
- Rebuild for hdf5 1.10.6

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Orion Poplawski <orion@nwra.com> - 4.7.0-1
- Update to 4.7.0

* Sat Mar 16 2019 Orion Poplawski <orion@nwra.com> - 4.6.3-1
- Update to 4.6.3

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 4.4.1.1-12
- Rebuild for openmpi 3.1.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 09 2018 Orion Poplawski <orion@nwra.com> - 4.4.1.1-9
- Run libtoolize to not strip link flags (bug #1548732)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Orion Poplawski <orion@cora.nwra.com> - 4.4.1.1-7
- Rebuild for gcc 8.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 08 2016 Dan Horák <dan[at]danny.cz> - 4.4.1.1-3
- Enable openmpi for s390(x) on F>=26

* Tue Dec 06 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.1.1-2
- Rebuild for hdf5 1.8.18

* Tue Nov 29 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.1.1-1
- Update to 4.4.1.1
- Add patch to fix mpi tests compilation

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.1-4
- Rebuild for openmpi 2.0

* Fri Aug 12 2016 Michal Toman <mtoman@fedoraproject.org> - 4.4.1-3
- No valgrind on MIPS
- Enable valgrind on arm

* Thu Jul 7 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.1-2
- Add upstream patch to fix hashmap issue

* Wed Jun 29 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.1-1
- Update to 4.4.1

* Tue Jun 28 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.0-4
- Drop mpiexec hack

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.0-2
- Rebuild ncx.c to fix arm build

* Thu Jan 21 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.0-1
- Update to 4.4.0
- Add patch to fix incorrect char definitions

* Sat Nov 07 2015 Rex Dieter <rdieter@fedoraproject.org> 4.3.3.1-7
- rebuild (hdf)

* Wed Sep 16 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.3.1-6
- Rebuild for openmpi 1.10.0

* Mon Aug 10 2015 Sandro Mani <manisandro@gmail.com> - 4.3.3.1-5
- Rebuild for RPM MPI Requires Provides Change

* Wed Jul 29 2015 Karsten Hopp <karsten@redhat.com> 4.3.3.1-4
- mpich is available on ppc64 now

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.3.1-2
- Rebuild for hdf5 1.8.15

* Wed Mar 11 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.3.1-1
- Update to 4.3.3.1

* Fri Feb 13 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.3-1
- Update to 4.3.3

* Tue Jan 27 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.2-7
- Fix up provides/requires for mpi packages, use %%{?_isa}.

* Wed Jan 07 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.2-6
- Rebuild for hdf5 1.8.14

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Jakub Čajka <jcajka@redhat.com> - 4.3.2-4
- Enabled tests on s390
- Disabled parallel tests on s390(x) as they hang

* Mon Jun 9 2014 Orion Poplawski <orion@cora.nwra.com> - 4.3.2-3
- Rebuild for hdf5 1.8.13, add patch for support

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Orion Poplawski <orion@cora.nwra.com> - 4.3.2-1
- Update to 4.3.2
- Drop utf8 patch fixed upstream
- Re-enable MPI tests

* Fri Mar 7 2014 Orion Poplawski <orion@cora.nwra.com> - 4.3.1.1-3
- Strip UTF-8 character from netcdf.h for now, causes problems with
  netcdf4-python build

* Sat Feb 22 2014 Deji Akingunola <dakingun@gmail.com> - 4.3.1.1-2
- Rebuild for mpich-3.1

* Thu Feb 6 2014 Orion Poplawski <orion@cora.nwra.com> - 4.3.1.1-1
- Update to 4.3.1.1
- Add BR m4

* Fri Dec 27 2013 Orion Poplawski <orion@cora.nwra.com> - 4.3.0-8
- Rebuild for hdf5 1.8.12

* Thu Dec 5 2013 Orion Poplawski <orion@cora.nwra.com> - 4.3.0-7
- Use BR hdf-static (bug #1038280)

* Mon Nov 4 2013 Orion Poplawski <orion@cora.nwra.com> - 4.3.0-6
- Enable hdf4 support

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Deji Akingunola <dakingun@gmail.com> - 4.3.0-4
- Rename mpich2 sub-packages to mpich and rebuild for mpich-3.0

* Thu Jul 11 2013 Orion Poplawski <orion@cora.nwra.com> - 4.3.0-3
- Rebuild for openmpi 1.7.2

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 4.3.0-2
- Rebuild for hdf5 1.8.11

* Mon May 13 2013 Orion Poplawski <orion@cora.nwra.com> - 4.3.0-1
- Update to 4.3.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2.1.1-3
- Rebuild for hdf5 1.8.10
- Disable make check of the mpi code, it is hanging for some reason

* Thu Nov 1 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2.1.1-2
- Rebuild for openmpi and mpich2 soname bumps
- Use new mpi module location

* Fri Aug 3 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2.1.1-1
- Update to 4.2.1.1

* Sun Jul 22 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2.1-1
- Update to 4.2.1 final

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2.1-0.1.rc1
- Update to 4.2.1 rc1
- Rebase pkgconfig patch
- Drop fflags patch, upstream now calls nf-config

* Wed Jun 13 2012 Dan Horák <dan[at]danny.cz> - 4.2-5
- temporarily disable checks on s390 (memory corruption and stuck build)

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-4
- Rebuild with hdf5 1.8.9

* Wed Mar 21 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-3
- Update to real 4.2 final

* Tue Mar 20 2012 Dan Horák <dan[at]danny.cz> - 4.2-2
- use %%{mpi_list} also in %%check

* Fri Mar 16 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-1
- Update to 4.2 final

* Wed Mar 7 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-0.4.rc2
- Ship examples with -devel

* Wed Mar 7 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-0.3.rc2
- Enable MPI builds

* Tue Mar 6 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-0.2.rc2
- Update to 4.2-rc2
- Fortran and C++ APIs are now in separate packages

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-5
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.3-3
- Rebuild for hdf5 1.8.8, add explicit requires

* Thu Aug 11 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 4.1.3-2
- Add ARM to valgrind excludes

* Tue Jun 21 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.3-1
- Update to 4.1.3
- Update pkgconfig and fflags patches
- Drop libm patch fixed upstream

* Tue May 17 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.2-2
- Rebuild for hdf5 1.8.7

* Thu Mar 31 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.2-1
- Update to 4.1.2 (soname bump)
- Add patch to add -lm to libnetcdf4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 19 2010 Dan Horák <dan[at]danny.cz> - 4.1.1-4
- no valgrind on s390(x)

* Mon Apr 19 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.1-3
- Explicitly link libnetcdf.so against -lhdf5_hl -lhdf5

* Fri Apr 9 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.1-2
- Add patch to cleanup nc-config --fflags

* Thu Apr 8 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.1-1
- Update to 4.1.1

* Fri Feb 5 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-1
- Update to 4.1.0 final

* Mon Feb 1 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.8.2010020100
- Update snapshot, pkgconfig patch
- Re-enable make check

* Sat Dec 5 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.7.2009120100
- Leave include files in /usr/include

* Tue Dec 1 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.6.2009120100
- Update snapshot, removes SZIP defines from header

* Fri Nov 13 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.5.2009111309
- Update snapshot
- Docs are installed now

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.5.2009111008
- Explicitly link libnetcdf to the hdf libraries, don't link with -lcurl

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.4.2009111008
- Add Requires: curl-devel to devel package

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.3.2009111008
- Drop hdf4 support - too problematic with linking all required libraries

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.2.2009111008
- Add patch to use proper hdf4 libraries
- Add Requires: hdf-devel, hdf5-devel to devel package
- Move nc-config to devel package

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.1.2009111008
- Update to 4.1.0 beta 2 snapshot
- Enable: netcdf-4, dap, hdf4, ncgen4, a lot more tests

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 Orion Poplawski <orion@cora.nwra.com> - 4.0.1-1
- Update to 4.0.1
- Add pkgconfig file

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep  3 2008 Orion Poplawski <orion@cora.nwra.com> - 4.0.0-1
- Update to 4.0 final
- Drop netcdf-3 symlink (bug #447158)
- Update cstring patch, partially upstreamed

* Thu May 29 2008 Balint Cristian <rezso@rdsor.ro> - 4.0.0-0.6.beta2
- fix symlink to netcdf-3

* Sun May 18 2008 Patrice Dumas <pertusus@free.fr> - 4.0.0-0.5.beta2
- use %%{_fmoddir}
- don't use %%makeinstall

* Thu May 15 2008 Balint Cristian <rezso@rdsor.ro> - 4.0.0-0.4.beta2
- re-enable ppc64 since hdf5 is now present for ppc64

* Thu May  8 2008 Ed Hill <ed@eh3.com> - 4.0.0-0.3.beta2
- make package compliant with bz # 373861

* Thu May  8 2008 Ed Hill <ed@eh3.com> - 4.0.0-0.2.beta2
- ExcludeArch: ppc64 since it doesn't (for now) have hdf5

* Wed May  7 2008 Ed Hill <ed@eh3.com> - 4.0.0-0.1.beta2
- try out upstream 4.0.0-beta2

* Wed Apr  2 2008 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-7
- Change patch to include <cstring>
- Remove %%{?_smp_mflags} - not parallel build safe (fortran modules)

* Wed Feb 20 2008 Ed Hill <ed@eh3.com> - 3.6.2-6
- add patch that (hopefully?) allows the GCC 4.3 build to proceed

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.6.2-5
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Ed Hill <ed@eh3.com> - 3.6.2-4
- add BR: gawk

* Sat Aug 25 2007 Ed Hill <ed@eh3.com> - 3.6.2-3
- rebuild for BuildID

* Mon May 21 2007 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-2
- Run checks

* Sat Mar 17 2007 Ed Hill <ed@eh3.com> - 3.6.2-1
- 3.6.2 has a new build system supporting shared libs

* Sat Sep  2 2006 Ed Hill <ed@eh3.com> - 3.6.1-4
- switch to compat-gcc-34-g77 instead of compat-gcc-32-g77

* Sat Sep  2 2006 Ed Hill <ed@eh3.com> - 3.6.1-3
- rebuild for imminent FC-6 release

* Thu May 11 2006 Ed Hill <ed@eh3.com> - 3.6.1-2
- add missing BuildRequires for the g77 interface

* Fri Apr 21 2006 Ed Hill <ed@eh3.com> - 3.6.1-1
- update to upstream 3.6.1

* Thu Feb 16 2006 Ed Hill <ed@eh3.com> - 3.6.0-10.p1
- rebuild for new GCC

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> - 3.6.0-9.p1
- rebuild for gcc4.1

* Sun Oct 16 2005 Ed Hill <ed@eh3.com> - 3.6.0-8.p1
- building the library twice (once each for g77 and gfortran) 
  fixes an annoying problem for people who need both compilers

* Fri Sep 30 2005 Ed Hill <ed@eh3.com> - 3.6.0-7.p1
- add FFLAGS="-fPIC"

* Fri Jun 10 2005 Ed Hill <ed@eh3.com> - 3.6.0-6.p1
- rebuild

* Fri Jun  3 2005 Ed Hill <ed@eh3.com> - 3.6.0-5.p1
- bump for the build system

* Mon May  9 2005 Ed Hill <ed@eh3.com> - 3.6.0-4.p1
- remove hard-coded dist/fedora macros

* Wed May  4 2005 Ed Hill <ed@eh3.com> - 3.6.0-3.p1
- make netcdf-devel require netcdf (bug #156748)
- cleanup environment and paths

* Tue Apr  5 2005 Ed Hill <ed@eh3.com> - 0:3.6.0-2.p1
- update for gcc-gfortran
- fix file permissions

* Sat Mar  5 2005 Ed Hill <ed@eh3.com> - 0:3.6.0-1.p1
- update for 3.6.0-p1 large-files-bug fix and remove the Epoch

* Sun Dec 12 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0-0.2.beta6
- fix naming scheme for pre-releases (per Michael Schwendt)

* Sat Dec 11 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0beta6-0.fdr.2
- For Fortran, use only g77 (ignore gfortran, even if its installed)

* Tue Dec  7 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0beta6-0.fdr.1
- remove "BuildRequires: gcc4-gfortran"

* Sat Dec  4 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0beta6-0.fdr.0
- upgrade to 3.6.0beta6
- create separate devel package that does *not* depend upon 
  the non-devel package and put the headers/libs in "netcdf-3" 
  subdirs for easy co-existance with upcoming netcdf-4

* Thu Dec  2 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.12
- remove unneeded %%configure flags

* Wed Dec  1 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.11
- headers in /usr/include/netcdf, libs in /usr/lib/netcdf

* Mon Oct  4 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.10
- Put headers in their own directory but leave the libraries in the 
  %%{_libdir} -- there are only two libs and the majority of other
  "*-devel" packages follow this pattern

* Sun Oct  3 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:3.5.1-0.fdr.9
- add patch to install lib and headers into own tree

* Sun Aug  1 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.8
- added -fPIC so x86_64 build works with nco package

* Fri Jul 30 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.7
- fix typo in the x86_64 build and now works on x86_64

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.6
- fix license

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.5
- fix (hopefully?) x86_64 /usr/lib64 handling

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.4
- replace paths with macros

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.3
- fix spelling

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.2
- removed "--prefix=/usr" from %%configure

* Wed Jul 14 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.1
- Remove unnecessary parts and cleanup for submission

* Wed Jul 14 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.0
- Initial RPM release.
