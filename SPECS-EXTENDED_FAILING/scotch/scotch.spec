%global openmpidir %{_builddir}/ptscotch-openmpi-%{version}-%{release}
%global mpichdir %{_builddir}/ptscotch-mpich-%{version}-%{release}

# Shared library versioning:
# Increment if interface is changed in an incompatible way
%global so_maj 1
# Increment if interface is extended
%global so_min 3

Name:          scotch
Summary:       Graph, mesh and hypergraph partitioning library
Version:       6.0.9
Release:       3%{?dist}

License:       CeCILL-C
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:           https://gitlab.inria.fr/scotch/scotch
# source0 is actually here -> https://gitlab.inria.fr/scotch/scotch/-/archive/v6.0.9/scotch-v6.0.9.tar.gz
Source0:       https://gforge.inria.fr/frs/download.php/file/38187/%{name}_%{version}.tar.gz
Source1:       scotch-Makefile.shared.inc.in

# Makefile fix for installing esmumps
Patch0:        scotch_esmumps.patch
# Make shared libraries link properly with -Wl,--as-needed
Patch1:        scotch-ldflags.patch
# Fix undefined man page macros
Patch2:        scotch-man.patch

BuildRequires: flex
BuildRequires: bison
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: xz-devel

%description
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. The parallel scotch libraries are packaged in the
ptscotch sub-packages.

%package devel
Summary:       Development libraries for scotch
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development libraries for scotch.


%package doc
Summary:       Documentations and example for scotch and ptscotch
BuildArch:     noarch

%description doc
Contains documentations and example for scotch and ptscotch

###############################################################################

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

%package -n ptscotch-mpich-devel-parmetis
Summary:       Parmetis compatibility header for scotch
Requires:      pt%{name}-mpich-devel%{?_isa} = %{version}-%{release}

%description -n ptscotch-mpich-devel-parmetis
This package contains the parmetis compatibility header for scotch.


###############################################################################

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


%package -n ptscotch-openmpi-devel-parmetis
Summary:       Parmetis compatibility header for scotch
Requires:      pt%{name}-openmpi-devel%{?_isa} = %{version}-%{release}

%description -n ptscotch-openmpi-devel-parmetis
This package contains the parmetis compatibility header for scotch.

###############################################################################

%prep
# NOTE: If the archive prefix folder does not match %%{name}_%%{version}, then the file ID in the Source URL is likely wrong!
%autosetup -p1 -n %{name}_%{version}

cp -a %{SOURCE1} src/Makefile.inc

# Convert the license files to utf8
for file in doc/CeCILL-C_V1-en.txt doc/CeCILL-C_V1-fr.txt; do
    iconv -f iso8859-1 -t utf-8 $file > $file.conv && mv -f $file.conv $file
done

cp -a . %{openmpidir}
cp -a . %{mpichdir}


%build
pushd src/
make scotch esmumps CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}" SOMAJ="%{so_maj}"
popd

%{_mpich_load}
pushd %{mpichdir}/src/
make ptscotch ptesmumps CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags} -L%{_libdir}/mpich/lib -lmpi" SOMAJ="%{so_maj}"
popd
%{_mpich_unload}

%{_openmpi_load}
pushd %{openmpidir}/src/
make ptscotch ptesmumps CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags} -L%{_libdir}/openmpi/lib -lmpi" SOMAJ="%{so_maj}"
popd
%{_openmpi_unload}


%install
%define doinstall() \
make install prefix=%{buildroot}${MPI_HOME} libdir=%{buildroot}${MPI_LIB} includedir=%{buildroot}${MPI_INCLUDE} mandir=%{buildroot}${MPI_MAN} bindir=%{buildroot}${MPI_BIN} \
# Fix debuginfo packages not finding sources (See libscotch/Makefile) \
ln -s parser_ll.c libscotch/lex.yy.c \
ln -s parser_yy.c libscotch/y.tab.c \
ln -s parser_ly.h libscotch/y.tab.h \
\
pushd %{buildroot}${MPI_LIB}; \
for lib in *.so; do \
    chmod 755 $lib \
    mv $lib $lib.%{so_maj}.%{so_min} && ln -s $lib.%{so_maj}.%{so_min} $lib && ln -s $lib.%{so_maj}.%{so_min} $lib.%{so_maj} \
done \
popd \
\
pushd %{buildroot}${MPI_BIN} \
for prog in *; do \
    mv $prog scotch_${prog} \
    chmod 755 scotch_$prog \
done \
popd \
\
pushd %{buildroot}${MPI_MAN}/man1/ \
for man in *; do \
    mv ${man} scotch_${man} \
done \
# Cleanup man pages (some pages are only relevant for ptscotch packages, and vice versa) \
for man in *; do \
  if [ ! -f %{buildroot}${MPI_BIN}/${man/.1/} ]; then \
    rm -f $man \
  fi \
done \
popd

###############################################################################

export MPI_HOME=%{_prefix}
export MPI_LIB=%{_libdir}
export MPI_INCLUDE=%{_includedir}
export MPI_MAN=%{_mandir}
export MPI_BIN=%{_bindir}
pushd src
%doinstall
popd

###############################################################################

%{_mpich_load}
pushd %{mpichdir}/src
%doinstall
install -m644 libscotchmetis/parmetis.h %{buildroot}${MPI_INCLUDE}
popd
%{_mpich_unload}

###############################################################################

%{_openmpi_load}
pushd %{openmpidir}/src
%doinstall
install -m644 libscotchmetis/parmetis.h %{buildroot}${MPI_INCLUDE}
popd
%{_openmpi_unload}

###############################################################################


%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make -C src/check


%ldconfig_scriptlets

%ldconfig_scriptlets -n ptscotch-mpich

%ldconfig_scriptlets -n ptscotch-openmpi


%{!?_licensedir:%global license %%doc}
%files
%license doc/CeCILL-C_V1-en.txt
%{_bindir}/*
%{_libdir}/libscotch*.so.1*
%{_libdir}/libesmumps*.so.1*
%{_mandir}/man1/*

%files devel
%{_libdir}/libscotch*.so
%{_libdir}/libesmumps*.so
%{_includedir}/*scotch*.h
%{_includedir}/*esmumps*.h

%files -n ptscotch-mpich
%license doc/CeCILL-C_V1-en.txt
%{_libdir}/mpich/lib/lib*scotch*.so.1*
%{_libdir}/mpich/lib/lib*esmumps*.so.1*
%{_libdir}/mpich/bin/*
%{_mandir}/mpich*/*

%files -n ptscotch-mpich-devel
%{_includedir}/mpich*/*scotch*.h
%{_includedir}/mpich*/*esmumps*.h
%{_libdir}/mpich/lib/lib*scotch*.so
%{_libdir}/mpich/lib/lib*esmumps*.so

%files -n ptscotch-mpich-devel-parmetis
%{_includedir}/mpich*/parmetis.h

%files -n ptscotch-openmpi
%license doc/CeCILL-C_V1-en.txt
%{_libdir}/openmpi/lib/lib*scotch*.so.1*
%{_libdir}/openmpi/lib/lib*esmumps*.so.1*
%{_libdir}/openmpi/bin/*
%{_mandir}/openmpi*/*

%files -n ptscotch-openmpi-devel
%{_includedir}/openmpi*/*scotch*.h
%{_includedir}/openmpi*/*esmumps*.h
%{_libdir}/openmpi/lib/lib*scotch*.so
%{_libdir}/openmpi/lib/lib*esmumps*.so

%files -n ptscotch-openmpi-devel-parmetis
%{_includedir}/openmpi*/parmetis.h

%files doc
%license doc/CeCILL-C_V1-en.txt
%doc doc/*.pdf
%doc doc/scotch_example.f

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.0.9-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
