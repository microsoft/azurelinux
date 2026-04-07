## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global module Ipopt

## Define libraries' destination
%global _incmpidir %{_includedir}/openmpi-%{_arch}
%global _libmpidir %{_libdir}/openmpi/lib
%global _binmpidir %{_libdir}/openmpi/bin
%global _incmpichdir %{_includedir}/mpich-%{_arch}
%global _libmpichdir %{_libdir}/mpich/lib
%global _binmpichdir %{_libdir}/mpich/bin

%if 0%{?fedora} >= 40
%ifarch %{ix86}
%global with_openmpi 0
%else
%global with_openmpi 1
%endif
%else
%global with_openmpi 1
%endif
%global with_mpich 1
%global with_mpicheck 1
%global with_mpichcheck 1

%global with_asl 1
%global blaslib flexiblas

Name:  coin-or-%{module}
Summary: Interior Point OPTimizer
Version: 3.14.16
Release: %autorelease
License: EPL-2.0
URL:  https://coin-or.github.io/%{module}/
Source0: https://github.com/coin-or/Ipopt/archive/releases/%{version}/Ipopt-releases-%{version}.tar.gz

# See https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:   %{ix86}

BuildRequires: %{?dts}gcc, %{?dts}gcc-c++
BuildRequires: %{?dts}gcc-gfortran
BuildRequires: %{blaslib}-devel
BuildRequires: doxygen
BuildRequires: help2man
BuildRequires: make
BuildRequires: MUMPS-devel
BuildRequires: metis-devel
%if 0%{?with_asl}
BuildRequires: asl-devel
%endif
BuildRequires: openssh-clients
BuildRequires: pkgconfig
BuildRequires: hwloc-devel
BuildRequires: texlive-bibtex
BuildRequires: texlive-latex-bin-bin
BuildRequires: texlive-dvips
%if 0%{?fedora}
BuildRequires: tex(newunicodechar.sty)
%endif

Requires: %{name}-common = %{version}-%{release}

%description
Ipopt (Interior Point OPTimizer, pronounced eye-pea-Opt) is a software
package for large-scale nonlinear optimization. It is designed to find
(local) solutions of mathematical optimization problems of the form

   min     f(x)
x in R^n

s.t.       g_L <= g(x) <= g_U
           x_L <=  x   <= x_U

where f(x): R^n --> R is the objective function, and g(x): R^n --> R^m are
the constraint functions. The vectors g_L and g_U denote the lower and upper
bounds on the constraints, and the vectors x_L and x_U are the bounds on
the variables x. The functions f(x) and g(x) can be non-linear and non-convex,
but should be twice continuously differentiable. Note that equality
constraints can be formulated in the above formulation by setting the
corresponding components of g_L and g_U to the same value.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        common
Summary:        Documentation files for %{name}
BuildArch:      noarch

%description    common
This package contains the HTML documentation,
a PDF tutorial to use %{name} and related
license files.

########################################################
%if 0%{?with_openmpi}
%package openmpi
Summary: Interior Point OPTimizer compiled against openmpi
BuildRequires:  MUMPS-openmpi-devel
BuildRequires:  pkgconfig(ompi)
BuildRequires:  scalapack-openmpi-devel
BuildRequires:  ptscotch-openmpi-devel
Requires: %{name}-common = %{version}-%{release}
%description openmpi
%{name} libraries compiled against openmpi.

%package openmpi-devel
Summary: The %{name} headers and development-related files
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
%description openmpi-devel
Shared links and header files for developing applications that
use %{name}-openmpi.
%endif
##########################################################
########################################################
%if 0%{?with_mpich}
%package mpich
Summary: Interior Point OPTimizer compiled against mpich
BuildRequires:  MUMPS-mpich-devel
BuildRequires:  mpich-devel
BuildRequires:  scalapack-mpich-devel
BuildRequires:  ptscotch-mpich-devel
Requires: %{name}-common = %{version}-%{release}
%description mpich
%{name} libraries compiled against MPICH.

%package mpich-devel
Summary: The %{name} headers and development-related files
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
%description mpich-devel
Shared links and header files for developing applications that
use %{name}-mpich.
%endif
##########################################################

%prep
%setup -qc

pushd Ipopt-releases-%{version}

# Generate a doxygen tag file, disabled upstream in the 3.13.0 release
sed -i 's/#\(GENERATE_TAGFILE\)/\1/' doc/Doxyfile.in

# Fix the include file location
sed -i 's,\(@includedir@/coin\)-or,\1,' src/ipopt.pc.in
popd

%if 0%{?with_openmpi}
cp -a Ipopt-releases-%{version} %{module}-releases-openmpi
%endif
%if 0%{?with_mpich}
cp -a Ipopt-releases-%{version} %{module}-releases-mpich
%endif


%build

%if 0%{?el7}
%{?dts:source /opt/rh/devtoolset-9/enable}
%endif

#######################################################
## Build serial version

cd Ipopt-releases-%{version}

export LIBLAPACK=-l%{blaslib}
export INCLAPACK=-I%{_includedir}/%{blaslib}

OPT_CFLAGS="%{build_ldflags}"
OPT_CXXFLAGS="%{build_cxxflags}"
CPPFLAGS="-I%{_includedir}/MUMPS"
CXXLIBS="-L%{_libdir} -ldmumps $LIBLAPACK -lmetis -ldl"
%configure CC=gcc CXX=g++ F77=gfortran CFLAGS="%{build_cflags} $INCLAPACK" CXXFLAGS="%{build_cxxflags} $INCLAPACK" \
           LDFLAGS="%{build_ldflags}" CXXLIBS="$CXXLIBS" \
 --with-mumps --with-mumps-cflags=-I%{_includedir}/MUMPS --with-mumps-lflags=-ldmumps \
 --with-lapack --with-lapack-lflags=$LIBLAPACK --enable-mpiinit \
%if 0%{?with_asl}
 --with-asl-cflags=-I%{_includedir}/asl --with-asl-lflags="-lasl" \
%endif
 --enable-shared --disable-java

pushd doc
sed -i '/LATEX_BATCHMOD/s/NO/YES/' Doxyfile
doxygen -u
popd

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

%make_build V=1 all doc
cd ..
#######################################################

#######################################################
## Build MPI version
%if 0%{?with_openmpi}

cd %{module}-releases-openmpi
%{_openmpi_load}
export LIBLAPACK=-l%{blaslib}
export INCLAPACK=-I%{_includedir}/%{blaslib}
CFLAGS="%{build_cxxflags} $INCLAPACK"
OPT_CFLAGS="%{build_cflags} $INCLAPACK"
LDFLAGS="%{build_ldflags}"
CXXFLAGS="%{build_cxxflags} $INCLAPACK"
OPT_CXXFLAGS="%{build_cxxflags} $INCLAPACK"
%if 0%{?rhel}
CPPFLAGS=" -pthread -I$MPI_INCLUDE"
CXXLIBS=" -L$MPI_LIB -lmpi_mpifh -lmpi -lscalapack -ldmumps -lmumps_common -lptscotcherr -lptscotch -lptesmumps -ldl"
%else
CPPFLAGS="$(pkg-config --cflags ompi-fort)"
CXXLIBS="$(pkg-config --libs ompi) $(pkg-config --libs ompi-fort) -lscalapack -ldmumps -lmumps_common -lptscotcherr -lptscotch -lptesmumps -ldl"
%endif
export CC=$MPI_BIN/mpicc
export CXX=$MPI_BIN/mpic++
export F77=$MPI_BIN/mpif77

%configure --with-mumps-cflags=" -I$MPI_INCLUDE/MUMPS" \
 --with-mumps --with-mumps-lflags="-L$MPI_LIB -ldmumps -lmumps_common" --with-mumps-cflags="-I$MPI_INCLUDE/MUMPS" \
 --with-lapack --with-lapack-lflags=$LIBLAPACK --disable-java --enable-mpiinit \
%if 0%{?with_asl}
 --with-asl-cflags=-I%{_includedir}/asl --with-asl-lflags="-lasl" \
%endif
            MPICC=$MPI_BIN/mpicc \
            MPICXX=$MPI_BIN/mpic++ \
            MPIF77=$MPI_BIN/mpif77 \
            ADD_CFLAGS="-fopenmp" \
            ADD_FFLAGS="-fopenmp" \
            ADD_CXXFLAGS="-fopenmp" \
            CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" \
            LDFLAGS="$LDFLAGS" CXXLIBS="$CXXLIBS"

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
 sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
     -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
     -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
     -i libtool

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPI_LIB
%make_build V=1 all
%{_openmpi_unload}
cd ..
%endif

#######################################################
## Build MPICH version
%if 0%{?with_mpich}

cd %{module}-releases-mpich
%{_mpich_load}
export LIBLAPACK=-l%{blaslib}
export INCLAPACK=-I%{_includedir}/%{blaslib}
CFLAGS="%{build_cflags} $INCLAPACK"
OPT_CFLAGS="%{build_cflags} $INCLAPACK"
LDFLAGS="%{build_ldflags}"
CXXFLAGS="%{build_cxxflags} $INCLAPACK"
OPT_CXXFLAGS="%{build_cxxflags} $INCLAPACK"
CPPFLAGS="$(pkg-config --cflags mpich)"
CXXLIBS="$(pkg-config --libs mpich) -lscalapack -ldmumps -lmumps_common -lptscotcherr -lptscotch -lptesmumps -ldl"
export CC=$MPI_BIN/mpicc
export CXX=$MPI_BIN/mpic++
export F77=$MPI_BIN/mpif77

%configure --with-mumps-cflags=" -I$MPI_INCLUDE/MUMPS" \
 --with-mumps --with-mumps-lflags="-L$MPI_LIB -ldmumps -lmumps_common" --with-mumps-cflags="-I$MPI_INCLUDE/MUMPS" \
 --with-lapack --with-lapack-lflags=$LIBLAPACK --disable-java --enable-mpiinit \
%if 0%{?with_asl}
 --with-asl-cflags=-I%{_includedir}/asl --with-asl-lflags="-lasl" \
%endif
            MPICC=$MPI_BIN/mpicc \
            MPICXX=$MPI_BIN/mpic++ \
            MPIF77=$MPI_BIN/mpif77 \
            ADD_CFLAGS="-fopenmp" \
            ADD_FFLAGS="-fopenmp" \
            ADD_CXXFLAGS="-fopenmp" \
            CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" \
            LDFLAGS="$LDFLAGS" CXXLIBS="$CXXLIBS"

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
 sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
     -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
     -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
     -i libtool

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPI_LIB
%make_build V=1 all
%{_mpich_unload}
cd ..
%endif

%install

#######################################################
## Install MPI version
%if 0%{?with_openmpi}
%{_openmpi_load}
mkdir -p $RPM_BUILD_ROOT$MPI_LIB
mkdir -p $RPM_BUILD_ROOT$MPI_BIN
mkdir -p $RPM_BUILD_ROOT$MPI_INCLUDE
mkdir -p %{module}-releases-openmpi/headers

cd %{module}-releases-openmpi
 cp -p --no-dereference src/.libs/libipopt.so* \
       $RPM_BUILD_ROOT$MPI_LIB/
 cp -p --no-dereference contrib/sIPOPT/src/.libs/libsipopt.so* \
       $RPM_BUILD_ROOT$MPI_LIB/
%if 0%{?with_asl}
 cp -p --no-dereference src/Apps/AmplSolver/.libs/libipoptamplinterface.so* \
       $RPM_BUILD_ROOT$MPI_LIB/
 cp -p --no-dereference src/Apps/AmplSolver/.libs/ipopt \
       $RPM_BUILD_ROOT$MPI_BIN/
 cp -p --no-dereference contrib/sIPOPT/AmplSolver/ipopt_sens \
       $RPM_BUILD_ROOT$MPI_BIN/
%endif

 find -O3 src \( -name \*.h -o -name \*.hpp \) -exec cp -p {} headers \;
 cp -p contrib/sIPOPT/src/*.hpp src/Common/*.h headers
cd ..

##Copy MPI header files
install -p -m 644 %{module}-releases-openmpi/headers/* $RPM_BUILD_ROOT$MPI_INCLUDE
%{_openmpi_unload}
%endif

#######################################################
#######################################################
## Install MPICH version
%if 0%{?with_mpich}
%{_mpich_load}
mkdir -p $RPM_BUILD_ROOT$MPI_LIB
mkdir -p $RPM_BUILD_ROOT$MPI_BIN
mkdir -p $RPM_BUILD_ROOT$MPI_INCLUDE
mkdir -p %{module}-releases-mpich/headers

cd %{module}-releases-mpich
 cp -p --no-dereference src/.libs/libipopt.so* \
       $RPM_BUILD_ROOT$MPI_LIB/
 cp -p --no-dereference contrib/sIPOPT/src/.libs/libsipopt.so* \
       $RPM_BUILD_ROOT$MPI_LIB/
%if 0%{?with_asl}
 cp -p --no-dereference src/Apps/AmplSolver/.libs/libipoptamplinterface.so* \
       $RPM_BUILD_ROOT$MPI_LIB/
 cp -p --no-dereference src/Apps/AmplSolver/.libs/ipopt \
       $RPM_BUILD_ROOT$MPI_BIN/
 cp -p --no-dereference contrib/sIPOPT/AmplSolver/ipopt_sens \
       $RPM_BUILD_ROOT$MPI_BIN/
%endif

 find -O3 src \( -name \*.h -o -name \*.hpp \) -exec cp -p {} headers \;
 cp -p contrib/sIPOPT/src/*.hpp src/Common/*.h headers
cd ..

##Copy MPI header files
install -p -m 644 %{module}-releases-mpich/headers/* $RPM_BUILD_ROOT$MPI_INCLUDE
%{_mpich_unload}
%endif

#######################################################

## Install serial version

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/coin
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}

mkdir -p Ipopt-releases-%{version}/headers

cd Ipopt-releases-%{version}
 ##Copy libraries
 cp -p --no-dereference src/.libs/libipopt.so* \
       $RPM_BUILD_ROOT%{_libdir}/
 cp -p --no-dereference contrib/sIPOPT/src/.libs/libsipopt.so* \
       $RPM_BUILD_ROOT%{_libdir}/
 cp -p --no-dereference src/ipopt.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig
%if 0%{?with_asl}
 cp -p --no-dereference src/Apps/AmplSolver/.libs/libipoptamplinterface.so* \
       $RPM_BUILD_ROOT%{_libdir}/
 cp -p --no-dereference src/Apps/AmplSolver/ipoptamplinterface.pc \
       $RPM_BUILD_ROOT%{_libdir}/pkgconfig
 cp -p --no-dereference src/Apps/AmplSolver/.libs/ipopt \
       $RPM_BUILD_ROOT%{_bindir}/
 cp -p contrib/sIPOPT/AmplSolver/ipopt_sens \
       $RPM_BUILD_ROOT%{_bindir}/
%endif

 find -O3 src \( -name \*.h -o -name \*.hpp \) -exec cp -p {} headers \;
 cp -p contrib/sIPOPT/src/*.hpp src/Common/*.h headers
cd ..

# Make man pages
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
help2man -N $RPM_BUILD_ROOT%{_bindir}/ipopt > $RPM_BUILD_ROOT%{_mandir}/man1/ipopt.1
cat > $RPM_BUILD_ROOT%{_mandir}/man1/ipopt_sens.1 << EOF
.so man1/ipopt.1
EOF

##Copy header and documentation files
install -p -m 644 Ipopt-releases-%{version}/headers/* $RPM_BUILD_ROOT%{_includedir}/coin/

# Correct config.h due to manual install (#1295290)
pushd $RPM_BUILD_ROOT%{_includedir}/coin/
    rm config.h config_default.h
    # Use the generated config_ipopt.h
    sed -i 's/\(config_ipopt\)_default\(\.h\)/\1\2/' IpoptConfig.h
popd

cp -far Ipopt-releases-%{version}/doc/{html,*.tag} $RPM_BUILD_ROOT%{_docdir}/%{name}/

#######################################################
%check
cd Ipopt-releases-%{version}
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} make test
cd ..

%if 0%{?with_openmpi}
%if 0%{?with_mpicheck}
cd %{module}-releases-openmpi
%{_openmpi_load}
LD_LIBRARY_PATH=$RPM_BUILD_ROOT$MPI_LIB make test
%{_openmpi_unload}
cd ..
%endif
%endif

%if 0%{?with_mpich}
%if 0%{?with_mpichcheck}
cd %{module}-releases-mpich
# Remove unknown -Lsystem/lib flag
for i in `find . -type f \( -name "Makefile" \)`; do
 sed -e 's|-Lsystem/lib||g' -i $i
done
#
%{_mpich_load}
MPICH_INTERFACE_HOSTNAME=localhost LD_LIBRARY_PATH=$RPM_BUILD_ROOT$MPI_LIB make test
%{_mpich_unload}
cd ..
%endif
%endif

%files
%if 0%{?with_asl}
%{_bindir}/ipopt
%{_bindir}/ipopt_sens
%endif
%{_libdir}/libipopt.so.3
%{_libdir}/libipopt.so.%{version}
%{_libdir}/libsipopt.so.3
%{_libdir}/libsipopt.so.%{version}
%if 0%{?with_asl}
%{_libdir}/libipoptamplinterface.so.3
%{_libdir}/libipoptamplinterface.so.%{version}
%endif
%{_mandir}/man1/ipopt.1*
%{_mandir}/man1/ipopt_sens.1*

%files  devel
%{_includedir}/coin/*
%{_libdir}/libipopt.so
%{_libdir}/libsipopt.so
%{_libdir}/pkgconfig/ipopt.pc
%if 0%{?with_asl}
%{_libdir}/libipoptamplinterface.so
%{_libdir}/pkgconfig/ipoptamplinterface.pc
%endif

#######################################################
## Install MPI version
%if 0%{?with_openmpi}

%files openmpi
%if 0%{?with_asl}
%{_binmpidir}/ipopt
%{_binmpidir}/ipopt_sens
%endif
%{_libmpidir}/libipopt.so.3
%{_libmpidir}/libipopt.so.%{version}
%{_libmpidir}/libsipopt.so.3
%{_libmpidir}/libsipopt.so.%{version}
%if 0%{?with_asl}
%{_libmpidir}/libipoptamplinterface.so.3
%{_libmpidir}/libipoptamplinterface.so.%{version}
%endif

%files openmpi-devel
%{_libmpidir}/libipopt.so
%{_libmpidir}/libsipopt.so
%if 0%{?with_asl}
%{_libmpidir}/libipoptamplinterface.so
%endif
%{_incmpidir}/*

%endif
%if 0%{?with_mpich}

%files mpich
%if 0%{?with_asl}
%{_binmpichdir}/ipopt
%{_binmpichdir}/ipopt_sens
%endif
%{_libmpichdir}/libipopt.so.3
%{_libmpichdir}/libipopt.so.%{version}
%{_libmpichdir}/libsipopt.so.3
%{_libmpichdir}/libsipopt.so.%{version}
%if 0%{?with_asl}
%{_libmpichdir}/libipoptamplinterface.so.3
%{_libmpichdir}/libipoptamplinterface.so.%{version}
%endif

%files mpich-devel
%{_libmpichdir}/libipopt.so
%{_libmpichdir}/libsipopt.so
%if 0%{?with_asl}
%{_libmpichdir}/libipoptamplinterface.so
%endif
%{_incmpichdir}/*
%endif

%files common
%license Ipopt-releases-%{version}/LICENSE
%{_docdir}/%{name}/

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 3.14.16-6
- Latest state for coin-or-Ipopt

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Dec 28 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.14.16-3
- Rebuild for MUMPS-5.7.3

* Tue Dec 03 2024 Jerry James <loganjerry@gmail.com> - 3.14.16-2
- Rebuild for asl 20241111

* Mon Sep 23 2024 Jerry James <loganjerry@gmail.com> - 3.14.16-1
- Version 3.14.16

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 30 2024 Jerry James <loganjerry@gmail.com> - 3.14.14-1
- Release 3.14.14

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 06 2024 Antonio Trande <sagitter@fedoraproject.org> - 3.14.12-4
- Rebuild for MUMPS-5.6.2

* Sun Oct 29 2023 Orion Poplawski <orion@nwra.com> - 3.14.12-3
- Rebuild for openmpi 5.0.0, drops support for i686

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 06 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.14.12-1
- Release 3.14.12

* Sun Feb 19 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.14.11-1
- Release 3.14.11

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 30 2022 Antonio Trande <sagitter@fedoraproject.org> - 3.14.9-1
- Release 3.14.9

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 17 2022 Antonio Trande <sagitter@fedoraproject.org> - 3.14.8-1
- Release 3.14.8

* Sat May 07 2022 Antonio Trande <sagitter@fedoraproject.org> - 3.14.6-1
- Release 3.14.6

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 21 2021 Antonio Trande <sagitter@fedoraproject.org> - 3.14.4-1
- Release 3.14.4

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 17 2021 Antonio Trande <sagitter@fedoraproject.org> - 3.13.4-2
- Rebuild for MUMPS-5.4.0

* Wed May 26 2021 Antonio Trande <sagitter@fedoraproject.org> - 3.13.4-1
- Release 3.13.4

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 04 2020 Antonio T <sagitter@fedoraproject.org> - 3.13.0-12
- Fix cflags

* Thu Dec 03 2020 Antonio T <sagitter@fedoraproject.org> - 3.13.0-11
- Remove blas/lapack BR dependencies |Rebuild for MUMPS-5.3.5 on EPEL7

* Wed Nov 11 2020 Jerry James <loganjerry@gmail.com> - 3.13.0-10
- Explicitly BR make.

* Tue Sep 22 2020 sagitter <sagitter@fedoraproject.org> - 3.13.0-9
- Enable MPI tests on Fedora 34+

* Sat Aug 22 2020 sagitter <sagitter@fedoraproject.org> - 3.13.0-8
- Disable MPI tests on Fedora 34+

* Mon Aug 10 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.13.0-7
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.0-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 14 2020 Jerry James <loganjerry@gmail.com> - 3.13.0-4
- Fix include directory in pkgconfig file (bz 1833734).

* Sun Apr 12 2020 Nicolas Chauvet <kwizart@gmail.com> - 3.13.0-3
- Rebuilt for MUMPS 5.3

* Sat Apr 11 2020 sagitter <sagitter@fedoraproject.org> - 3.13.0-2
- Rebuild for MUMPS-5.3.0

* Fri Feb 21 2020 Jerry James <loganjerry@gmail.com> - 3.13.0-1
- Release 3.13.0. Drop upstreamed -sipopt patch. Drop unnecessary
  -underlink patch.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 05 2020 sagitter <sagitter@fedoraproject.org> - 3.12.13-8
- Fix EPEL7 conditions

* Sun Jan 05 2020 sagitter <sagitter@fedoraproject.org> - 3.12.13-7
- Explicit references to mpiblacs are needed on EPEL 7

* Sun Jan 05 2020 sagitter <sagitter@fedoraproject.org> - 3.12.13-6
- New rebuild

* Tue Dec 24 2019 sagitter <sagitter@fedoraproject.org> - 3.12.13-5
- Use devtoolset-8 on EPEL-7

* Sat Dec 21 2019 sagitter <sagitter@fedoraproject.org> - 3.12.13-4
- Missing hwloc dependency

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Jerry James <loganjerry@gmail.com> - 3.12.13-2
- New URLs on github.

* Mon Apr 22 2019 sagitter <sagitter@fedoraproject.org> - 3.12.13-1
- Release 3.12.13

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 3.12.11-5
- Rebuild for openmpi 3.1.3

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.12.11-3
- Fix RHEL conditions

* Sat Nov 03 2018 sagitter <sagitter@fedoraproject.org> - 3.12.11-2
- Modify MPI link/compiler flags

* Thu Nov 01 2018 sagitter <sagitter@fedoraproject.org> - 3.12.11-1
- Update to Ipopt-3.12.11

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 03 2018 sagitter <sagitter@fedoraproject.org> - 3.12.10-1
- Update to Ipopt-3.12.10

* Fri Feb 23 2018 sagitter <sagitter@fedoraproject.org> - 3.12.9-1
- Update to Ipopt-3.12.9

* Wed Feb 14 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.12.8-7
- Remove %%clean section

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 29 2017 sagitter <sagitter@fedoraproject.org> - 3.12.8-5
- Rebuild for MUMPS-5.1.2

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.8-4
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 sagitter <sagitter@fedoraproject.org> - 3.12.8-2
- Rebuild for MUMPS-5.1..1 (after a bug-fix)

* Wed Jun 14 2017 sagitter <sagitter@fedoraproject.org> - 3.12.8-1
- Update to 3.12.8

* Mon May 15 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Thu Mar 23 2017 sagitter <sagitter@fedoraproject.org> - 3.12.7-2
- Rebuild for MUMPS-5.1.1

* Sat Feb 25 2017 sagitter <sagitter@fedoraproject.org> - 3.12.7-1
- Update to 3.12.7 (bz#1426828)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 01 2016 sagitter <sagitter@fedoraproject.org> - 3.12.6-4
- New architectures

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 3.12.6-3
- Rebuild for openmpi 2.0

* Tue Sep 20 2016 sagitter <sagitter@fedoraproject.org> - 3.12.6-2
- Exclude strings.h wrapper installation (bz#1375290)

* Thu Jul 21 2016 sagitter <sagitter@fedoraproject.org> - 3.12.6-1
- Update to 3.12.6

* Tue Jul 19 2016 sagitter <sagitter@fedoraproject.org> - 3.12.5-4
- ASL enabled on EPEL.

* Sun May 15 2016 sagitter <sagitter@fedoraproject.org> - 3.12.5-3
- PPC64 excluded on EPEL6

* Sun May 15 2016 sagitter <sagitter@fedoraproject.org> - 3.12.5-2
- Install ipopt binary files (bz#1320049)

* Mon May 02 2016 sagitter <sagitter@fedoraproject.org> - 3.12.5-1
- Update to 3.12.5

* Thu Apr 07 2016 sagitter <sagitter@fedoraproject.org> - 3.12.4-12
- Fixed with_asl macro

* Wed Mar 16 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com>
- Correct side effect of previous change on armv7hl

* Wed Mar 16 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com>
- Correct HAVE_CONFIG_H dependency due to manual install (#1295290)

* Fri Mar 04 2016 sagitter <sagitter@fedoraproject.org>
- Rebuild for mp 3.0.1

* Thu Feb 11 2016 sagitter <sagitter@fedoraproject.org> - 3.12.4-8
- PPC64 excluded on EPEL6

* Tue Feb 09 2016 sagitter <sagitter@fedoraproject.org> - 3.12.4-7
- Build MPICH libraries; built on EPEL

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 3.12.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 02 2015 sagitter <sagitter@fedoraproject.org> - 3.12.4-5
- Hardened builds on <F23

* Wed Sep 16 2015 Orion Poplawski <orion@cora.nwra.com> - 3.12.4-4
- Rebuild for openmpi 1.10.0

* Sun Aug 16 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.12.4-3
- Rebuild for MPI provides

* Tue Aug 11 2015 Sandro Mani <manisandro@gmail.com> - 3.12.4-2
- RPM MPI Requires Provides

* Mon Aug 10 2015 sagitter <sagitter@fedoraproject.org> - 3.12.4-1
- Update to 3.12.4

* Sun Jun 21 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.12.3-3
- Full rebuild of coin-or stack

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 3.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 18 2015 sagitter <sagitter@fedoraproject.org> - 3.12.3-1
- Update to 3.12.3 (#1213024)

* Sun Apr 05 2015 sagitter <sagitter@fedoraproject.org> - 3.12.2-1
- Update to 3.12.2

* Sun Feb 22 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.12.1-5
- Add conditional to enable the asl solver

* Sun Feb 22 2015 sagitter <sagitter@fedoraproject.org> - 3.12.1-4
- Rebuild again (broken dependencies)

* Sun Feb 22 2015 sagitter <sagitter@fedoraproject.org> - 3.12.1-3
- Rebuild again (broken dependencies)

* Sat Feb 21 2015 sagitter <sagitter@fedoraproject.org> - 3.12.1-2
- Rebuild after MUMPS update

* Tue Feb 17 2015 sagitter <sagitterATfedoraprojectDOTorg> - 3.12.1-1
- Update to 3.12.1

* Wed Feb 04 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 3.12.0-2
- Correct aarch64 build again (#1185848)

* Wed Jan 28 2015 sagitter <sagitterATfedoraprojectDOTorg> - 3.12.0-1
- Update to 3.12.0 (bz#1152812)

* Mon Jan 26 2015 Paulo Andrade <pcpa@gnu.org> - 3.11.10-4
- Add changelog entry

* Mon Jan 26 2015 Paulo Andrade <pcpa@gnu.org> - 3.11.10-3
- Correct aarch64 build (#1185848)

* Fri Jan 23 2015 sagitter <sagitterATfedoraprojectDOTorg> - 3.11.10-2
- Fix libraries's symlinks (bz#1152812)

* Mon Jan 19 2015 sagitter <sagitterATfedoraprojectDOTorg> - 3.11.10-1
- Update to 3.11.10

* Mon Oct 27 2014 Peter Robinson <pbrobinson@gmail.com> - 3.11.9-4
- Update config.guess config.sub for new arch (aarch64/ppc64le) support

* Sat Oct 04 2014 sagitter <anto.trande@gmail.com> - 3.11.9-3
- Obsolete coin-or-Ipopt-doc sub-package.

* Tue Sep 23 2014 sagitter <anto.trande@gmail.com> - 3.11.9-2
- Build openmpi sub-package.

* Sat Aug 30 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.11.9-1
- Update to latest upstream release (#1131008)

* Sat Aug 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 3.11.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 10 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.11.8-2
- Update to recent MUMPS changes

* Thu Jul 10 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.11.8-1
- Update to latest upstream release

* Fri Jun 13 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.11.0-10
- Correct bad date cut&paste

* Fri Jun 13 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.11.0-9
- Adapt to newer scalapack correcting rawhide FTBFS (#1106072)

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 3.11.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 07 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.11.0-7
- Correct files conflict (#1084893)

* Sat Mar 08 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.11.0-6
- Add requires to owner of includedir/coin directory to devel package

* Sat Mar 08 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.11.0-5
- Correct misspelling of _smp_mflags

* Wed Aug 07 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.11.0-4
- Correct rawhide FTBFS and switch to unversioned docdir

* Sat Aug 03 2013 Dennis Gilmore <dennis@ausil.us> - 3.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.11.0-2
- Add missing buildrequires (mock buildroot had them already)

* Sun May 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 3.11.0-1
- Initial import (#894604).
## END: Generated by rpmautospec
