%bcond_without mpich
%ifarch s390 s390x
%bcond_with openmpi
%else
%bcond_without openmpi
%endif
%if %{with mpich}
%global mpi_list %{?mpi_list} mpich
%endif
%if %{with openmpi}
%global mpi_list %{?mpi_list} openmpi
%endif


Name:           fftw
Version:        3.3.8
Release:        8%{?dist}
Summary:        A Fast Fourier Transform library
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.fftw.org
Source0:        http://www.fftw.org/fftw-%{version}.tar.gz
BuildRequires:  gcc-gfortran

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

%global quad 0
# Quad precision support only available with gcc >= 4.6 (Fedora >= 15)
# and only on these arches
%ifarch %{ix86} x86_64 ia64
%global quad 1
%endif

# For check phase
BuildRequires:  time
BuildRequires:  perl-interpreter
%if %{with mpich}
BuildRequires:  mpich-devel
BuildRequires:  nss-myhostname
%endif
%if %{with openmpi}
BuildRequires:  openmpi-devel
%endif
%if %{with mpich} || %{with openmpi}
BuildRequires:  environment-modules
%endif


%description
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

%package libs
Summary:        FFTW run-time library
Provides:       fftw3 = %{version}-%{release}
# Libs rearranged in 3.3.1-2
Obsoletes:      fftw-libs-threads < %{version}-%{release}
Obsoletes:      fftw-libs-openmp < %{version}-%{release}

# Pull in the actual libraries
Requires:       %{name}-libs-single%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs-double%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs-long%{?_isa} = %{version}-%{release}
%if %{quad}
Requires:       %{name}-libs-quad%{?_isa} = %{version}-%{release}
%endif

%description libs
This is a dummy package package, pulling in the individual FFTW
run-time libraries.


%package devel
Summary:        Headers, libraries and docs for the FFTW library
Requires:       pkgconfig
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       fftw3-devel%{?_isa} = %{version}-%{release}
Provides:       fftw3-devel = %{version}-%{release}

%description devel
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.

%package libs-double
Summary:        FFTW library, double precision

%description libs-double
This package contains the FFTW library compiled in double precision.

%package libs-single
Summary:        FFTW library, single precision

%description libs-single
This package contains the FFTW library compiled in single precision.

%package libs-long
Summary:        FFTW library, long double precision 

%description libs-long
This package contains the FFTW library compiled in long double
precision.

%if %{quad}
%package libs-quad
Summary:        FFTW library, quadruple

%description libs-quad
This package contains the FFTW library compiled in quadruple
precision.
%endif

%package        static
Summary:        Static versions of the FFTW libraries
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Provides:       fftw3-static%{?_isa} = %{version}-%{release}
Provides:       fftw3-static = %{version}-%{release}

%description static
The fftw-static package contains the statically linkable version of
the FFTW fast Fourier transform library.

%if %{with mpich}
%package mpich-libs
Summary:        FFTW MPICH run-time library
Provides:       fftw3-mpich = %{version}-%{release}

# Pull in the actual libraries
Requires:       %{name}-mpich-libs-single%{?_isa} = %{version}-%{release}
Requires:       %{name}-mpich-libs-double%{?_isa} = %{version}-%{release}
Requires:       %{name}-mpich-libs-long%{?_isa} = %{version}-%{release}

%description mpich-libs
This is a dummy package package, pulling in the individual FFTW
MPICH run-time libraries.


%package mpich-devel
Summary:        Headers, libraries and docs for the FFTW MPICH library
Requires:       mpich-devel
Requires:       pkgconfig
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-mpich-libs%{?_isa} = %{version}-%{release}
Provides:       fftw3-mpich-devel%{?_isa} = %{version}-%{release}
Provides:       fftw3-mpich-devel = %{version}-%{release}

%description mpich-devel
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library for MPICH.

%package mpich-libs-double
Summary:        FFTW MPICH library, double precision
Requires:       %{name}-libs-double%{?_isa} = %{version}-%{release}

%description mpich-libs-double
This package contains the FFTW MPICH library compiled in double precision.

%package mpich-libs-single
Summary:        FFTW MPICH library, single precision
Requires:       %{name}-libs-single%{?_isa} = %{version}-%{release}

%description mpich-libs-single
This package contains the FFTW MPICH library compiled in single precision.

%package mpich-libs-long
Summary:        FFTW MPICH library, long double precision 
Requires:       %{name}-libs-long%{?_isa} = %{version}-%{release}

%description mpich-libs-long
This package contains the FFTW MPICH library compiled in long double
precision.

%package        mpich-static
Summary:        Static versions of the FFTW MPICH libraries
Requires:       %{name}-mpich-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-static%{?_isa} = %{version}-%{release}
Provides:       fftw3-mpich-static%{?_isa} = %{version}-%{release}
Provides:       fftw3-mpich-static = %{version}-%{release}

%description mpich-static
The fftw-mpich-static package contains the statically linkable version of
the FFTW fast Fourier transform library for MPICh.
%endif

%if %{with openmpi}
%package openmpi-libs
Summary:        FFTW OpenMPI run-time library
Provides:       fftw3-openmpi = %{version}-%{release}

# Pull in the actual libraries
Requires:       %{name}-openmpi-libs-single%{?_isa} = %{version}-%{release}
Requires:       %{name}-openmpi-libs-double%{?_isa} = %{version}-%{release}
Requires:       %{name}-openmpi-libs-long%{?_isa} = %{version}-%{release}

%description openmpi-libs
This is a dummy package package, pulling in the individual FFTW
OpenMPI run-time libraries.


%package openmpi-devel
Summary:        Headers, libraries and docs for the FFTW OpenMPI library
Requires:       openmpi-devel
Requires:       pkgconfig
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-openmpi-libs%{?_isa} = %{version}-%{release}
Provides:       fftw3-openmpi-devel%{?_isa} = %{version}-%{release}
Provides:       fftw3-openmpi-devel = %{version}-%{release}

%description openmpi-devel
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library for OpenMPI.

%package openmpi-libs-double
Summary:        FFTW OpenMPI library, double precision
Requires:       %{name}-libs-double%{?_isa} = %{version}-%{release}

%description openmpi-libs-double
This package contains the FFTW OpenMPI library compiled in double precision.

%package openmpi-libs-single
Summary:        FFTW OpenMPI library, single precision
Requires:       %{name}-libs-single%{?_isa} = %{version}-%{release}

%description openmpi-libs-single
This package contains the FFTW OpenMPI library compiled in single precision.

%package openmpi-libs-long
Summary:        FFTW OpenMPI library, long double precision 
Requires:       %{name}-libs-long%{?_isa} = %{version}-%{release}

%description openmpi-libs-long
This package contains the FFTW OpenMPI library compiled in long double
precision.

%package        openmpi-static
Summary:        Static versions of the FFTW OpenMPI libraries
Requires:       %{name}-openmpi-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-static%{?_isa} = %{version}-%{release}
Provides:       fftw3-openmpi-static%{?_isa} = %{version}-%{release}
Provides:       fftw3-openmpi-static = %{version}-%{release}

%description openmpi-static
The fftw-openmpi-static package contains the statically linkable version of
the FFTW fast Fourier transform library for MPICh.
%endif

%package doc
Summary:        FFTW library manual
BuildArch:      noarch

%description doc
This package contains the manual for the FFTW fast Fourier transform
library.

%prep
%setup -q

%build
# Explicitly load shell support for the environment-modules package, used
# below via 'module' pseudo-command.
source /etc/profile.d/modules.sh

# Regenerate autoconf files using current tools so proper build flags
# from redhat-rpm-config are used
autoreconf -vfi
# Configure uses g77 by default, if present on system
export F77=gfortran

BASEFLAGS="--enable-shared --disable-dependency-tracking --enable-threads"
BASEFLAGS+=" --enable-openmp"

# Precisions to build
prec_name[0]=single
prec_name[1]=double
prec_name[2]=long
prec_name[3]=quad

# Corresponding flags
prec_flags[0]=--enable-single
prec_flags[1]=--enable-double
prec_flags[2]=--enable-long-double
prec_flags[3]=--enable-quad-precision

%ifarch x86_64
# Enable SSE2 and AVX support for x86_64
for((i=0;i<2;i++)); do
 prec_flags[i]+=" --enable-sse2 --enable-avx"
done
%endif

# No NEON run time detection, not all ARM SoCs have NEON
#%ifarch %{arm}
## Compile support for NEON instructions
#for((i=0;i<2;i++)); do
# prec_flags[i]+=" --enable-neon"
#done
#%endif

#%ifarch ppc ppc64
## Compile support for Altivec instructions
#for((i=0;i<2;i++)); do
 #prec_flags[i]+=" --enable-altivec"
#done
#%endif

# Loop over precisions
%if %{quad}
for((iprec=0;iprec<4;iprec++))
%else
for((iprec=0;iprec<3;iprec++))
%endif
do
 mkdir ${prec_name[iprec]}${ver_name[iver]}
 cd ${prec_name[iprec]}${ver_name[iver]}
 ln -s ../configure .
 %{configure} ${BASEFLAGS} ${prec_flags[iprec]}
 sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
 sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
 make %{?_smp_mflags}
 cd ..
done

# MPI Builds - this duplicates the non-mpi builds, but oh well
for mpi in %{mpi_list}
do
 module load mpi/${mpi}-%{_arch}
 # Loop over precisions - no quad precision support with MPI
 for((iprec=0;iprec<3;iprec++))
 do
  mkdir ${mpi}-${prec_name[iprec]}${ver_name[iver]}
  cd ${mpi}-${prec_name[iprec]}${ver_name[iver]}
  ln -s ../configure .
  # Force linking the _mpi.so libraries with the mpi libs.  This works because
  # we get rid of all of the non-mpi components of these builds
  export CC=mpicc
  %{configure} ${BASEFLAGS} ${prec_flags[iprec]} --enable-mpi \
   --libdir=%{_libdir}/$mpi/lib \
   --bindir=%{_libdir}/$mpi/bin \
   --sbindir=%{_libdir}/$mpi/sbin \
   --includedir=%{_includedir}/$mpi-%{_arch} \
   --mandir=%{_libdir}/$mpi/share/man
  make %{?_smp_mflags}
  cd ..
 done
 module unload mpi/${mpi}-%{_arch}
done


%install
# Explicitly load shell support for the environment-modules package, used
# below via 'module' pseudo-command.
source /etc/profile.d/modules.sh

%if %{quad}
for ver in single double long quad
%else
for ver in single double long
%endif
do
 make -C $ver install DESTDIR=%{buildroot}
done
# MPI
for mpi in %{mpi_list}
do
 module load mpi/${mpi}-%{_arch}
 for ver in single double long
 do
  make -C ${mpi}-${ver} install DESTDIR=%{buildroot}
  # Remove duplicated non-mpi libraries, binaries, and data
  find %{buildroot}%{_libdir}/${mpi}/lib -name libfftw\* -a \! -name \*_mpi.\* -delete
  rm -r %{buildroot}%{_libdir}/${mpi}/{bin,share}
 done
 module unload mpi/${mpi}-%{_arch}
done
rm -f %{buildroot}%{_infodir}/dir
find %{buildroot} -name \*.la -delete

%check
# Explicitly load shell support for the environment-modules package, used
# below via 'module' pseudo-command.
source /etc/profile.d/modules.sh

bdir=`pwd`
%if %{quad}
for ver in single double long quad
%else
for ver in single double long
%endif
do 
 export LD_LIBRARY_PATH=$bdir/$ver/.libs:$bdir/$ver/threads/.libs
 make %{?_smp_mflags} -C $ver check
done
# MPI
%if %{with openmpi}
%ifarch %{ix86}
# disable Open MPI's vader byte transfer layer while running tests on 32-bit x86 platforms
# as it is known to be troublesome <https://github.com/open-mpi/ompi/issues/4260>
export OMPI_MCA_btl="^vader"
%endif
%endif
for mpi in %{mpi_list}
do
 module load mpi/${mpi}-%{_arch}
 for ver in single double long
 do 
  export LD_LIBRARY_PATH=$bdir/$ver/.libs:$bdir/$ver/threads/.libs
  make %{?_smp_mflags} -C ${mpi}-${ver}/mpi check
 done
 module unload mpi/${mpi}-%{_arch}
done

%ldconfig_scriptlets libs-single
%ldconfig_scriptlets libs-double
%ldconfig_scriptlets libs-long
%if %{quad}
%ldconfig_scriptlets libs-quad
%endif

%files
%{_mandir}/man1/fftw*.1*
%{_bindir}/fftw*-wisdom*

%files libs

%files libs-single
%license COPYING COPYRIGHT
%doc AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/libfftw3f.so.*
%{_libdir}/libfftw3f_threads.so.*
%{_libdir}/libfftw3f_omp.so.*

%files libs-double
%license COPYING COPYRIGHT
%doc AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/libfftw3.so.*
%{_libdir}/libfftw3_threads.so.*
%{_libdir}/libfftw3_omp.so.*

%files libs-long
%license COPYING COPYRIGHT
%doc AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/libfftw3l.so.*
%{_libdir}/libfftw3l_threads.so.*
%{_libdir}/libfftw3l_omp.so.*

%if %{quad}
%files libs-quad
%license COPYING COPYRIGHT
%doc AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/libfftw3q.so.*
%{_libdir}/libfftw3q_threads.so.*
%{_libdir}/libfftw3q_omp.so.*
%endif

%files devel
%doc doc/FAQ/fftw-faq.html/
%doc %{_infodir}/fftw3.info*
%{_includedir}/fftw3*
%dir %{_libdir}/cmake/fftw3/
%{_libdir}/cmake/fftw3/*.cmake
%{_libdir}/pkgconfig/fftw3*.pc
%{_libdir}/libfftw3*.so

%files static
%{_libdir}/libfftw3*.a

%files doc
%doc doc/*.pdf doc/html/

%if %{with mpich}
%files mpich-libs

%files mpich-libs-single
%license COPYING COPYRIGHT
%doc AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/mpich/lib/libfftw3f_mpi.so.*

%files mpich-libs-double
%license COPYING COPYRIGHT
%doc AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/mpich/lib/libfftw3_mpi.so.*

%files mpich-libs-long
%license COPYING COPYRIGHT
%doc AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/mpich/lib/libfftw3l_mpi.so.*

%files mpich-devel
%doc doc/FAQ/fftw-faq.html/
%{_includedir}/mpich-%{_arch}
%dir %{_libdir}/mpich/lib/cmake/fftw3/
%{_libdir}/mpich/lib/cmake/fftw3/*.cmake
%{_libdir}/mpich/lib/pkgconfig/fftw3*.pc
%{_libdir}/mpich/lib/libfftw3*.so

%files mpich-static
%{_libdir}/mpich/lib/libfftw3*.a
%endif

%if %{with openmpi}
%files openmpi-libs

%files openmpi-libs-single
%license COPYING COPYRIGHT
%doc AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/openmpi/lib/libfftw3f_mpi.so.*

%files openmpi-libs-double
%license COPYING COPYRIGHT
%doc AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/openmpi/lib/libfftw3_mpi.so.*

%files openmpi-libs-long
%license COPYING COPYRIGHT
%doc AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/openmpi/lib/libfftw3l_mpi.so.*

%files openmpi-devel
%doc doc/FAQ/fftw-faq.html/
%{_includedir}/openmpi-%{_arch}
%dir %{_libdir}/openmpi/lib/cmake/fftw3/
%{_libdir}/openmpi/lib/cmake/fftw3/*.cmake
%{_libdir}/openmpi/lib/pkgconfig/fftw3*.pc
%{_libdir}/openmpi/lib/libfftw3*.so

%files openmpi-static
%{_libdir}/openmpi/lib/libfftw3*.a
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.3.8-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar  7 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 3.3.8-5
- Remove obsolete requirements for %%post/%%preun scriptlets

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 3.3.8-4
- Rebuild for openmpi 3.1.3

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 11 2018 Conrad Meyer <cemeyer@uw.edu> - 3.3.8-1
- Update to latest upstream, 3.3.8 (rhbz# 1413425)
- Add missing BuildRequires on environment-modules, used in 43b91c1c ("Build
  mpich and openmpi versions") without explicit BR dependency
- Add new cmake files to %%files

* Wed Apr 18 2018 Merlin Mathesius <mmathesi@redhat.com> - 3.3.5-11
- Regenerate autoconf files using current tools so proper build flags
  from redhat-rpm-config are used. This resolves BZ#1548473.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.3.5-9
- Switch to %%ldconfig_scriptlets

* Tue Nov 28 2017 Merlin Mathesius <mmathesi@redhat.com> - 3.3.5-8
- Disable Open MPI's vader byte transfer layer while running tests on 32-bit x86 platforms
  as it is known to be troublesome <https://github.com/open-mpi/ompi/issues/4260>.
  This resolves FTBFS issue (BZ#1518038).

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 3.3.5-4
- Rebuild for openmpi 2.0

* Mon Oct 10 2016 Dan Horák <dan[at]danny.cz> - 3.3.5-3
- Update BRs so nss-myhostname (provided by systemd) is included also
  in mpich-only builds (Related: #1383271)

* Fri Oct 7 2016 Orion Poplawski <orion@cora.nwra.com> - 3.3.5-2
- Build mpich and openmpi versions

* Wed Oct 5 2016 Orion Poplawski <orion@cora.nwra.com> - 3.3.5-1
- Update to 3.3.5
- Cleanup spec

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.3.4-4
- Disable SSE2/AVX on x86(32) as we support Pentium Pro as base
- SSE2 only arrived with P-4
- https://fedoraproject.org/wiki/Features/F12X86Support
- Fix ARM macro
- Disable NEON on ARM (we don't enable by default, needs runtime detection)

* Thu Jul 03 2014 Conrad Meyer <cemeyer@uw.edu> - 3.3.4-3
- Build with --enable-avx (rhbz# 1114964)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.4-1
- Update to 3.3.4.

* Sat Dec 14 2013 Conrad Meyer <cemeyer@uw.edu> - 3.3.3-8
- Remove non-OpenMP / g77 build for obsolete RHEL (< 5)
- Remove ancient Obsoletes (fftw < 3.3, Fedora < 16)
- Remove ancient non-Quad build (Fedora < 15) on supported arch(s)
- Remove obsolete conditional on BuildArch: noarch (RHEL < 6, Fedora < 13)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 PPC Secondary Arch Admin <karsten@redhat.com> 3.3.3-5
- disable altivec flag again, that works with single precision only

* Mon Dec 24 2012 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-4
- Fix typo: should be %%ix86 instead of %%x86. Now should have SSE2 support
  on x86 as well.

* Tue Dec 18 2012 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-3
- After consultation with upstream, enable SSE2 also on x86, altivec on ppc
  and ppc64 and NEON on arm.

* Tue Dec 18 2012 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-2
- Enable SSE2 on x86_64.

* Mon Nov 26 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-1
- Update to 3.3.3.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Orion Poplawski <orion@cora.nwra.com> - 3.3.2-1
- Update to 3.3.2
- Drop alignment patch

* Fri Apr 27 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.1-3
- Fix FTBFS with gcc 4.7.

* Thu Apr 26 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.1-2
- Reorganized libraries (BZ #812981).

* Mon Feb 27 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Dan Horák <dan[at]danny.cz> - 3.3-4
- libquadmath exists only on x86/x86_64 and ia64

* Mon Oct 10 2011 Rex Dieter <rdieter@fedoraproject.org> 3.3-3
- -devel: Provides: fftw3-devel (#744758)
- -static: Provides: fftw3-static
- drop %%_isa from Obsoletes

* Sat Jul 30 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3-2
- Conditionalize OpenMP and quadruple precision support based on capabilities
  of system compiler.

* Thu Jul 28 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3-1
- Update to 3.3.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 9 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-4
- Get rid of rpath.

* Sat Jan 9 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-3
- Branch out developers' manual to -doc.

* Sat Jan 2 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-2
- Add check phase.
- Cosmetic changes to spec file (unified changelog format, removed unnecessary
  space).
- Use rm instead of find -delete, as latter is not present on EPEL-4.
- Generalize obsoletes of fftw3 packages. Add Obsoletes: fftw3-static.

* Fri Jan 1 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-1
- Update to 3.2.2.
- Make file listings more explicit.
- Don't use file dependencies for info.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Conrad Meyer <konrad@tylerc.org> - 3.2.1-1
- Bump to 3.2.1.

* Thu Dec 4 2008 Conrad Meyer <konrad@tylerc.org> - 3.2-1
- Bump to 3.2.

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1.2-7
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1.2-6
- Autorebuild for GCC 4.3

* Fri Aug 24 2007 Quentin Spencer <qspencer@users.sf.net> 3.1.2-5
- Rebuild for F8.

* Fri Jul 27 2007 Quentin Spencer <qspencer@users.sf.net> 3.1.2-4
- Split static libs into separate package (bug 249686).

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 3.1.2-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.2-2
- BuildRequires: pkgconfig for -devel (bug 206444).

* Fri Sep  8 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.2-1
- New release.

* Fri Jun  2 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.1-1
- New upstream release.

* Fri Feb 24 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-4
- Re-enable static libs (bug 181897).
- Build long-double version of libraries (bug 182587).

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-3
- Add Obsoletes and Provides.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-2
- Rebuild for Fedora Extras 5.
- Disable static libs.
- Remove obsolete configure options.

* Wed Feb  1 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-1
- Upgrade to the 3.x branch, incorporating changes from the fftw3 spec file.
- Add dist tag.
