Vendor:         Microsoft Corporation
Distribution:   Mariner
%define enable_native_atlas 0

Name:           atlas
Version:        3.10.3
%if "%{?enable_native_atlas}" != "0"
%define dist .native
%endif
Release:        11%{?dist}
Summary:        Automatically Tuned Linear Algebra Software

License:        BSD
URL:            http://math-atlas.sourceforge.net/
Source0:        http://downloads.sourceforge.net/math-atlas/%{name}%{version}.tar.bz2
Source1:        PPRO32.tgz
#Source2:        K7323DNow.tgz
Source3:        README.dist
#Source4:        USII64.tgz                                              
#Source5:        USII32.tgz                                              
#Source6:        IBMz1032.tgz
#Source7:        IBMz1064.tgz
#Source8:        IBMz19632.tgz
#Source9:        IBMz19664.tgz
#archdefs taken from debian:
Source11: 	POWER332.tar.bz2
Source12: 	IBMz932.tar.bz2
Source13: 	IBMz964.tar.bz2
#upstream arm uses softfp abi, fedora arm uses hard
Source14: 	ARMv732NEON.tar.bz2
#again, taken from debian
Source15: 	IBMz1264.tar.bz2
Source16:	ARMa732.tar.bz2

Patch2:		atlas-fedora-arm.patch
# Properly pass -melf_* to the linker with -Wl, fixes FTBFS bug 817552
# https://sourceforge.net/tracker/?func=detail&atid=379484&aid=3555789&group_id=23725
Patch3:		atlas-melf.patch
Patch4:		atlas-throttling.patch

#credits Lukas Slebodnik
Patch5:		atlas-shared_libraries.patch

Patch7:		atlas-aarch64port.patch
Patch8:		atlas-genparse.patch

# Unbundle LAPACK (BZ #1181369)
Patch9:		atlas.3.10.1-unbundle.patch
Patch10:	atlas-gcc10.patch

BuildRequires:  gcc-gfortran, lapack-static, gcc

%ifarch x86_64
Obsoletes:      atlas-sse3 < 3.10.3-1
%endif

%ifarch %{ix86}
Obsoletes:      atlas-3dnow < 3.10.3-1
Obsoletes:      atlas-sse < 3.10.3-1
Obsoletes:      atlas-sse2 < 3.10.3-1
Obsoletes:      atlas-sse3 < 3.10.3-1
%endif

%ifarch s390 s390x
#Obsoletes:      atlas-z10 < 3.10
#Obsoletes:      atlas-z196 < 3.10
%endif


%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort f(ocusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

The performance improvements in ATLAS are obtained largely via
compile-time optimizations and tend to be specific to a given hardware
configuration. In order to package ATLAS some compromises
are necessary so that good performance can be obtained on a variety
of hardware. This set of ATLAS binary packages is therefore not
necessarily optimal for any specific hardware configuration.  However,
the source package can be used to compile customized ATLAS packages;
see the documentation for information.

%package devel
Summary:        Development libraries for ATLAS
Requires:       %{name} = %{version}-%{release}
Obsoletes:	%name-header <= %version-%release
Requires(posttrans):	/usr/sbin/alternatives
Requires(postun):	/usr/sbin/alternatives

%ifarch x86_64
Obsoletes:      atlas-sse3-devel < 3.10.3-1
%endif

%ifarch %{ix86}
Obsoletes:      atlas-3dnow-devel < 3.10.3-1
Obsoletes:      atlas-sse-devel < 3.10.3-1
Obsoletes:      atlas-sse2-devel < 3.10.3-1
Obsoletes:      atlas-sse3-devel < 3.10.3-1
%endif
%description devel
This package contains headers for development with ATLAS
(Automatically Tuned Linear Algebra Software).


%define types base

%if "%{?enable_native_atlas}" == "0"
############## Subpackages for architecture extensions #################
#
%ifarch x86_64
%define types base corei2 
#corei4
# sse3

%package corei2-static
Summary:        ATLAS libraries for Corei2 (Ivy/Sandy bridge) CPUs

%description corei2-static
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) static libraries compiled with optimizations for the Corei2 (Ivy/Sandy bridge)
CPUs. The base ATLAS builds for the x86_64 architecture are made for the hammer64 CPUs.

%package corei2
Summary:        ATLAS libraries for Corei2 (Ivy/Sandy bridge) CPUs

%description corei2
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the Corei2 (Ivy/Sandy bridge)
CPUs. The base ATLAS builds for the x86_64 architecture are made for the hammer64 CPUs.

%package corei2-devel
Summary:        Development libraries for ATLAS for Corei2 (Ivy/Sandy bridge) CPUs
Requires:       %{name}-corei2 = %{version}-%{release}
Obsoletes:	%name-header <= %version-%release
Requires(posttrans):	/usr/sbin/alternatives
Requires(postun):	/usr/sbin/alternatives

%description corei2-devel
This package contains shared and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the corei2 (Ivy/Sandy bridge) CPUs.
%endif

%ifarch %{ix86}
%define types base 
#corei1

#%package corei1
#Summary:        ATLAS libraries for Corei1 (Nehalem/Westmere) CPUs
#Group:          System Environment/Libraries

#%description corei1
#This package contains ATLAS (Automatically Tuned Linear Algebra Software)
#shared libraries compiled with optimizations for the Corei1 (Nehalem/Westmere) CPUs. 
#The base ATLAS builds for the ix86 architecture are made for PIII CPUs.

#%package corei1-devel
#Summary:        Development libraries for ATLAS for Corei1 (Nehalem/Westmere) CPUs
#Group:          Development/Libraries
#Requires:       %{name}-corei1 = %{version}-%{release}
#Obsoletes:	%name-header <= %version-%release
#Requires(posttrans):	/usr/sbin/alternatives
#Requires(postun):	/usr/sbin/alternatives

#%description corei1-devel
#This package contains shared and static versions of the ATLAS
#(Automatically Tuned Linear Algebra Software) libraries compiled with
#optimizations for the corei1 (Nehalem/Westmere) CPUs.

#%package corei1-static
#Summary:        Static libraries for ATLAS for Corei1 (/Nehalem/Westmere) CPUs
#Group:          Development/Libraries
#Requires:       %{name}-corei1-devel = %{version}-%{release}
#Requires(posttrans):	/usr/sbin/alternatives
#Requires(postun):	/usr/sbin/alternatives

#%description corei1-static
#This package contains the ATLAS (Automatically Tuned Linear Algebra
#Software) static libraries compiled with optimizations for the Corei1 (Nehalem/Westemere)
#CPUs. The base ATLAS builds for the ix86 architecture are made for the PIII CPUs.

%endif

%ifarch s390 s390x
%define types base z196 z10

%package z196
Summary:        ATLAS libraries for z196

%description z196
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the z196.

%package z196-devel
Summary:        Development libraries for ATLAS for z196
Requires:       %{name}-z196 = %{version}-%{release}
Obsoletes:	%name-z196-header <= %version-%release
Requires(posttrans):	/usr/sbin/alternatives
Requires(postun):	/usr/sbin/alternatives

%description z196-devel
This package contains headers and shared versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the z196 architecture.

%package z196-static
Summary:        Static libraries for ATLAS
Requires:       %{name}-z196-devel = %{version}-%{release}
Requires(posttrans):	/usr/sbin/alternatives
Requires(postun):	/usr/sbin/alternatives

%description z196-static
This package contains static version of ATLAS (Automatically Tuned
Linear Algebra Software) for the z196 architecture.


%package z10
Summary:        ATLAS libraries for z10

%description z10
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the z10.

%package z10-devel
Summary:        Development libraries for ATLAS for z10
Requires:       %{name}-z10 = %{version}-%{release}
Obsoletes:	%name-header <= %version-%release
Requires(posttrans):	/usr/sbin/alternatives
Requires(postun):	/usr/sbin/alternatives

%description z10-devel
This package contains headers and shared versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the z10 architecture.

%package z10-static
Summary:        Static libraries for ATLAS
Requires:       %{name}-devel = %{version}-%{release}
Requires(posttrans):	/usr/sbin/alternatives
Requires(postun):	/usr/sbin/alternatives

%description z10-static
This package contains static version of ATLAS (Automatically Tuned
Linear Algebra Software) for the z10 architecture.


%endif


%ifarch ppc64
%define types base power7 power8

%package power8
Summary:        ATLAS libraries for Power 8

%description power8
This package contains ATLAS (Automatically Tuned Linear Algebra Software)
shared libraries compiled with optimizations for the Power 8 CPUs. 
The base ATLAS builds for the ppc64 architecture are made for Power 5 CPUs.

%package power8-devel
Summary:        Development libraries for ATLAS for Power 8
Requires:       %{name}-power8 = %{version}-%{release}
Obsoletes:	%name-header <= %version-%release
Requires(posttrans):	/usr/sbin/alternatives
Requires(postun):	/usr/sbin/alternatives

%description power8-devel
This package contains shared and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the Power 8 CPUs.

%package power8-static
Summary:        Static libraries for ATLAS for Power 8
Requires:       %{name}-power8-devel = %{version}-%{release}
Requires(posttrans):	/usr/sbin/alternatives
Requires(postun):	/usr/sbin/alternatives

%description power8-static
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) static libraries compiled with optimizations for the Power 8
CPUs. The base ATLAS builds for the ppc64 architecture are made for the Power 5 CPUs.

%package power7
Summary:        ATLAS libraries for Power 7

%description power7
This package contains ATLAS (Automatically Tuned Linear Algebra Software)
shared libraries compiled with optimizations for the Power 7 CPUs. 
The base ATLAS builds for the ppc64 architecture are made for Power 5 CPUs.

%package power7-devel
Summary:        Development libraries for ATLAS for Power 7
Requires:       %{name}-power7 = %{version}-%{release}
Obsoletes:	%name-header <= %version-%release
Requires(posttrans):	/usr/sbin/alternatives
Requires(postun):	/usr/sbin/alternatives

%description power7-devel
This package contains shared and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the Power 7 CPUs.

%package power7-static
Summary:        Static libraries for ATLAS for Power 7
Requires:       %{name}-power7-devel = %{version}-%{release}
Requires(posttrans):	/usr/sbin/alternatives
Requires(postun):	/usr/sbin/alternatives

%description power7-static
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) static libraries compiled with optimizations for the Power 7
CPUs. The base ATLAS builds for the ppc64 architecture are made for the Power 5 CPUs.

%endif
#end of enable_native_atlas if
%endif

%prep
#cat /proc/cpuinfo
%setup -q -n ATLAS
#patch0 -p0 -b .shared
#arm patch not applicable, probably not needed
#%ifarch %{arm}
#%patch2 -p0 -b .arm
#%endif
%patch3 -p1 -b .melf
%patch4 -p1 -b .thrott
%patch5 -p2 -b .sharedlib
%ifarch aarch64
#%patch7 -p1 -b .aarch64
%endif
%patch8 -p1 -b .genparse
%patch9 -p1 -b .unbundle
%patch10 -p1

cp %{SOURCE1} CONFIG/ARCHS/
#cp %{SOURCE2} CONFIG/ARCHS/
cp %{SOURCE3} doc
cp %{SOURCE11} CONFIG/ARCHS/
cp %{SOURCE12} CONFIG/ARCHS/
cp %{SOURCE13} CONFIG/ARCHS/
cp %{SOURCE14} CONFIG/ARCHS/
cp %{SOURCE15} CONFIG/ARCHS/
cp %{SOURCE16} CONFIG/ARCHS/
#cp %{SOURCE8} CONFIG/ARCHS/
#cp %{SOURCE9} CONFIG/ARCHS/

%ifarch %{arm}
# Set arm flags in atlcomp.txt
#sed -i -e 's,-mfpu=vfpv3,-mfpu=neon,' CONFIG/src/atlcomp.txt
sed -i -e 's,-mfloat-abi=softfp,-mfloat-abi=hard,' CONFIG/src/atlcomp.txt
# Some extra arm flags not needed
#sed -i -e 's,-mfpu=vfpv3,,' tune/blas/gemm/CASES/*.flg
%endif
# Debug
#sed -i -e 's,> \(.*\)/ptsanity.out,> \1/ptsanity.out || cat \1/ptsanity.out \&\& exit 1,' makes/Make.*

# Generate lapack library
mkdir lapacklib
cd lapacklib
ar x %{_libdir}/liblapack_pic.a
# Remove functions that have ATLAS implementations
rm -f cgelqf.o cgels.o cgeqlf.o cgeqrf.o cgerqf.o cgesv.o cgetrf.o cgetri.o cgetrs.o clarfb.o clarft.o clauum.o cposv.o cpotrf.o cpotri.o cpotrs.o ctrtri.o dgelqf.o dgels.o dgeqlf.o dgeqrf.o dgerqf.o dgesv.o dgetrf.o dgetri.o dgetrs.o dlamch.o dlarfb.o dlarft.o dlauum.o dposv.o dpotrf.o dpotri.o dpotrs.o dtrtri.o ieeeck.o ilaenv.o lsame.o sgelqf.o sgels.o sgeqlf.o sgeqrf.o sgerqf.o sgesv.o sgetrf.o sgetri.o sgetrs.o slamch.o slarfb.o slarft.o slauum.o sposv.o spotrf.o spotri.o spotrs.o strtri.o xerbla.o zgelqf.o zgels.o zgeqlf.o zgeqrf.o zgerqf.o zgesv.o zgetrf.o zgetri.o zgetrs.o zlarfb.o zlarft.o zlauum.o zposv.o zpotrf.o zpotri.o zpotrs.o ztrtri.o 
# Create new library
ar rcs ../liblapack_pic_pruned.a *.o
cd ..


%build
p=$(pwd)
%undefine _strict_symbol_defs_build
%ifarch %{arm}
%global mode %{nil}
%else
%global mode -b %{__isa_bits}
%endif

%define arg_options %{nil}
%define flags %{nil}
%define threads_option "-t 2"

#Target architectures for the 'base' versions
%ifarch s390x 
%define flags %{nil}
%define base_options "-A IBMz9 -V 1"
%endif

%ifarch x86_64
%define flags %{nil}
%define base_options "-A HAMMER -V 896"
%endif

%ifarch %ix86
%define flags %{nil}
%define base_options "-A PIII -V 512"
%endif

%ifarch ppc
%define flags %{nil}
%define base_options "-A POWER5 -V 1"
%endif

%ifarch ppc64
%define flags %{nil}
%define base_options "-A POWER5 -V 1"
%endif

%ifarch ppc64le
%define flags %{nil}
%define base_options "-A POWER8 -V 1"
%endif

%ifarch %{arm}
%define flags "-DATL_ARM_HARDFP=1"
%define base_options "-A ARMa7 -V 1"
%endif

%ifarch aarch64
%define flags %{nil}
%define base_options "-A ARM64a53 -V 1"
%endif

%if "%{?enable_native_atlas}" != "0"
%define	threads_option %{nil}
%define base_options %{nil}
%define flags %{nil} 
%endif

for type in %{types}; do
	if [ "$type" = "base" ]; then
		libname=atlas
		arg_options=%{base_options}
		thread_options=%{threads_option} 
		%define pr_base %(echo $((%{__isa_bits}+0)))
	else
		libname=atlas-${type}
		if [ "$type" = "corei2" ]; then
			thread_options="-t 4"
			arg_options="-A Corei2 -V 896"
			%define pr_corei2 %(echo $((%{__isa_bits}+2)))
		elif [ "$type" = "corei1" ]; then
			arg_options="-A Corei1 -V 896"
			%define pr_corei1 %(echo $((%{__isa_bits}+2)))
		elif [ "$type" = "z10" ]; then
			arg_options="-A IBMz10 -V 1"
			%define pr_z10 %(echo $((%{__isa_bits}+2)))
		elif [ "$type" = "z196" ]; then
			arg_options="-A IBMz196 -V 1"
			%define pr_z196 %(echo $((%{__isa_bits}+4)))
		elif [ "$type" = "power7" ]; then
			thread_options="-t 4"
			arg_options="-A POWER7 -V 1"
			%define pr_power7 %(echo $((%{__isa_bits}+2)))
		elif [ "$type" = "power8" ]; then
			thread_options="-t 4"
			arg_options="-A POWER8 -V 1"
			%define pr_power8 %(echo $((%{__isa_bits}+4)))
		fi
	fi
	mkdir -p %{_arch}_${type}
	pushd %{_arch}_${type}
	../configure  %{mode} $thread_options $arg_options -D c -DWALL -Fa alg '%{flags} -D_FORTIFY_SOURCE=2 -g -Wa,--noexecstack,--generate-missing-build-notes=yes -fstack-protector-strong -fstack-clash-protection -fPIC -fplugin=annobin -Wl,-z,now'\
	--prefix=%{buildroot}%{_prefix}			\
	--incdir=%{buildroot}%{_includedir}		\
	--libdir=%{buildroot}%{_libdir}/${libname}	
	#--with-netlib-lapack-tarfile=%{SOURCE10}

	#matches both SLAPACK and SSLAPACK
	sed -i "s#SLAPACKlib.*#SLAPACKlib = ${p}/liblapack_pic_pruned.a#" Make.inc
	cat Make.inc
%if "%{?enable_native_atlas}" == "0"

%ifarch ppc64
	#Use big endian
	sed -i 's#ARCH = POWER564LE#ARCH = POWER564#' Make.inc
	sed -i 's#ARCH = POWER764LE#ARCH = POWER764#' Make.inc
	sed -i 's#ARCH = POWER864LE#ARCH = POWER864#' Make.inc
%endif

%endif

	make build
	cd lib
	make shared
	make ptshared
	popd
done

%install 	
for type in %{types}; do
	pushd %{_arch}_${type}
	make DESTDIR=%{buildroot} install
        mv %{buildroot}%{_includedir}/atlas %{buildroot}%{_includedir}/atlas-%{_arch}-${type}
	if [ "$type" = "base" ]; then
		cp -pr lib/*.so* %{buildroot}%{_libdir}/atlas/
		rm -f %{buildroot}%{_libdir}/atlas/*.a
		cp -pr lib/libcblas.a lib/libatlas.a lib/libf77blas.a lib/liblapack.a %{buildroot}%{_libdir}/atlas/
	else
		cp -pr lib/*.so* %{buildroot}%{_libdir}/atlas-${type}/
		rm -f %{buildroot}%{_libdir}/atlas-${type}/*.a
		cp -pr lib/libcblas.a lib/libatlas.a lib/libf77blas.a lib/liblapack.a %{buildroot}%{_libdir}/atlas-${type}/
	fi
	popd

	mkdir -p %{buildroot}/etc/ld.so.conf.d
	if [ "$type" = "base" ]; then
		echo "%{_libdir}/atlas"		\
		> %{buildroot}/etc/ld.so.conf.d/atlas-%{_arch}.conf
	else
		echo "%{_libdir}/atlas-${type}"	\
		> %{buildroot}/etc/ld.so.conf.d/atlas-%{_arch}-${type}.conf
	fi
done

#create pkgconfig file
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/atlas.pc << DATA
Name: %{name}
Version: %{version}
Description: %{summary}
Cflags: -I%{_includedir}/atlas/
Libs: -L%{_libdir}/atlas/ -lsatlas
DATA


mkdir -p %{buildroot}%{_includedir}/atlas


%check
# Run make check but don't fail the build on these arches
#%ifarch s390 aarch64 ppc64
#for type in %{types}; do
#	pushd %{_arch}_${type}
#	make check ptcheck  
#	popd
#done
#%else
for type in %{types}; do
	pushd %{_arch}_${type}
	make check ptcheck 
	popd
done
#%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%posttrans devel
/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
		%{_includedir}/atlas-%{_arch}-base %{pr_base}

%postun devel
if [ $1 -ge 0 ] ; then
/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-base
fi

%if "%{?enable_native_atlas}" == "0"
%ifarch x86_64

	%post -n atlas-corei2 -p /sbin/ldconfig

	%postun -n atlas-corei2 -p /sbin/ldconfig

	%posttrans corei2-devel
		/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
			%{_includedir}/atlas-%{_arch}-corei2  %{pr_corei2}

	%postun corei2-devel
	if [ $1 -ge 0 ] ; then
		/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-corei2
	fi

%endif

%ifarch %{ix86}

	%post -n atlas-corei1 -p /sbin/ldconfig

	%postun -n atlas-corei1 -p /sbin/ldconfig

	%posttrans corei1-devel
		/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
			%{_includedir}/atlas-%{_arch}-corei1  %{pr_corei1}

	%postun corei1-devel
	if [ $1 -ge 0 ] ; then
		/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-corei1
	fi

%endif

%ifarch s390 s390x

	%post -n atlas-z10 -p /sbin/ldconfig

	%postun -n atlas-z10 -p /sbin/ldconfig

	%posttrans z10-devel
		/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
			%{_includedir}/atlas-%{_arch}-z10  %{pr_z10}

	%postun z10-devel
	if [ $1 -ge 0 ] ; then
		/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-z10
	fi
	
	%post -n atlas-z196 -p /sbin/ldconfig

	%postun -n atlas-z196 -p /sbin/ldconfig

	%posttrans z196-devel
		/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
			%{_includedir}/atlas-%{_arch}-z196  %{pr_z196}

	%postun z196-devel
	if [ $1 -ge 0 ] ; then
		/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-z196
	fi

%endif

%ifarch ppc64

	%post -n atlas-power7 -p /sbin/ldconfig

	%postun -n atlas-power7 -p /sbin/ldconfig

	%posttrans power7-devel
		/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
			%{_includedir}/atlas-%{_arch}-power7  %{pr_power7}

	%postun power7-devel
	if [ $1 -ge 0 ] ; then
		/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-power7
	fi
	
	%post -n atlas-ppc8 -p /sbin/ldconfig

	%postun -n atlas-ppc8 -p /sbin/ldconfig

	%posttrans ppc8-devel
		/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
			%{_includedir}/atlas-%{_arch}-ppc8  %{pr_ppc8}

	%postun ppc8-devel
	if [ $1 -ge 0 ] ; then
		/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-ppc8
	fi

%endif
#enable_native_atlas
%endif
%files
	%doc doc/README.dist
	%dir %{_libdir}/atlas
	%{_libdir}/atlas/*.so.*
	%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}.conf

%files devel
	%doc doc
	%{_libdir}/atlas/*.so
	%{_includedir}/atlas-%{_arch}-base/
	%{_includedir}/*.h
	%ghost %{_includedir}/atlas
	%{_libdir}/pkgconfig/atlas.pc

%if "%{?enable_native_atlas}" == "0"

%ifarch x86_64

%files corei2
%doc doc/README.dist
%dir %{_libdir}/atlas-corei2
%{_libdir}/atlas-corei2/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-corei2.conf

%files corei2-devel
%doc doc
%{_libdir}/atlas-corei2/*.so
%{_includedir}/atlas-%{_arch}-corei2/
%{_includedir}/*.h
%ghost %{_includedir}/atlas

%files corei2-static
%{_libdir}/atlas-corei2/*.a
%endif

%ifarch ppc64


%files power8
%doc doc/README.dist
%dir %{_libdir}/atlas-power8
%{_libdir}/atlas-power8/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-power8.conf

%files power8-devel
%doc doc
%{_libdir}/atlas-power8/*.so
%{_includedir}/atlas-%{_arch}-power8/
%{_includedir}/*.h
%ghost %{_includedir}/atlas

%files power8-static
%{_libdir}/atlas-power8/*.a

%files power7
%doc doc/README.dist
%dir %{_libdir}/atlas-power7
%{_libdir}/atlas-power7/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-power7.conf

%files power7-devel
%doc doc
%{_libdir}/atlas-power7/*.so
%{_includedir}/atlas-%{_arch}-power7/
%{_includedir}/*.h
%ghost %{_includedir}/atlas

%files power7-static
%{_libdir}/atlas-power7/*.a
%endif

%ifarch %{ix86}

#%files corei1
#%doc doc/README.dist
#%dir %{_libdir}/atlas-corei1
#%{_libdir}/atlas-corei1/*.so.*
#%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-corei1.conf

#%files corei1-devel
#%doc doc
#%{_libdir}/atlas-corei1/*.so
#%{_includedir}/atlas-%{_arch}-corei1/
#%{_includedir}/*.h
#%ghost %{_includedir}/atlas

#%files corei1-static
#%{_libdir}/atlas-corei1/*.a
%endif

%ifarch s390 s390x
%files z10
%doc doc/README.dist
%dir %{_libdir}/atlas-z10
%{_libdir}/atlas-z10/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-z10.conf

%files z10-devel
%doc doc
%{_libdir}/atlas-z10/*.so
%{_includedir}/atlas-%{_arch}-z10/
%{_includedir}/*.h
%ghost %{_includedir}/atlas

%files z10-static
%{_libdir}/atlas-z10/*.a

%files z196
%doc doc/README.dist
%dir %{_libdir}/atlas-z196
%{_libdir}/atlas-z196/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-z196.conf

%files z196-devel
%doc doc
%{_libdir}/atlas-z196/*.so
%{_includedir}/atlas-%{_arch}-z196/
%{_includedir}/*.h
%ghost %{_includedir}/atlas

%files z196-static
%{_libdir}/atlas-z196/*.a

%endif
#enable_native_atlas if
%endif

%changelog
* Mon Jun 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.10.3-11
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Removing the "*-static" subpackage.

* Mon Jan 27 2020 Jakub Martisko <jamartis@redhat.com> - 3.10.3-10
- Fix compatibility with gcc 10
- Sync compiler/linker flags with RHEL

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 14 2018 Peter Robinson <pbrobinson@fedoraproject.org> 3.10.3-7
- Update requires for alternatives

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 11 2018 Jakub Martisko <jamartis@redhat.com> - 3.10.3-5
- Pass RPM_LD_FLAGS to linker

* Thu Mar 01 2018 Jakub Martisko <jamartis@redhat.com> - 3.10.3-4
- Add gcc to buildrequires

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Björn Esser <besser82@fedoraproject.org> - 3.10.3-2
- Rebuilt for GCC8

* Thu Aug 17 2017 Jakub Martisko <jamartis@redhat.com> - 3.10.3-1
- Update to new 3.10.3 stable version.
- Remove ppc64/ppc64le related patches.
- All packages now use -A option to specify the target CPU/Architecture instead of 
sed substitutions and auto detection. The packages should now be less dependant on the 
builder machine used.
- Base package for each architecture should now be configured to be compatible with the 
most basic machine of given type.
- In addittion to base package, added some optimized packages for more advanced CPUs for
most architectures.
- Dropped sse2/sse3 subpackages for ix86

* Wed Aug 16 2017 Tom Callaway <spot@fedoraproject.org> - 3.10.2-20
- rebuild again for fixed lapack

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 29 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.10.2-11
- Rebuild for updated lapack

* Thu Nov 26 2015 Than Ngo <than@redhat.com> 3.10.2-10
- backport upstream patch for power8 support

* Fri Nov 13 2015 Than Ngo <than@redhat.com> 3.10.2-9
- add correct assembler option for ppc64

* Wed Nov 04 2015 Than Ngo <than@redhat.com> - 3.10.2-8
- add correct machine type for ppc64 -> fix build failure on ppc64

* Wed Oct 28 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.10.2-7
- Drop bundled(lapack) which was already fixed in atlas-3.10.1-18.

* Thu Jul 09 2015 Than Ngo <than@redhat.com> 3.10.2-6
- fix ppc64le patch

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 3.10.2-4
- Refreshed AArch64 patch

* Fri Jun 05 2015 Dan Horák <dan[at]danny.cz> - 3.10.2-3
- drop upstreamed s390 patch

* Wed May 20 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.2-2
- include all single-threaded wrapper libraries in -static subpackage
- bz#1222079

* Thu May 14 2015 Orion Poplawski <orion@cora.nwra.com> - 3.10.2-1
- Update to 3.10.2 (bug #1118596)
- Autodetect arm arch
- Add arch_option for ppc64le

* Thu Mar 05 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-22
- lapack bundled again, mark this.

* Sat Feb 07 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.10.1-21
- Devel packages don't need to require lapack-devel anymore.

* Fri Jan 30 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.10.1-20
- Link statically to system LAPACK as in earlier versions of Fedora and as
  in OpenBLAS (BZ #1181369).

* Wed Jan 28 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-19
- updated chkconfig and dependencies of atlas-devel after unbundling

* Fri Jan 23 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-18
- unbundled lapack (only a few modified routines shipped with atlas sources are supposed to stay)

* Thu Oct 30 2014 Jaromir Capik <jcapik@redhat.com> - 3.10.1-17
- patching for Power8 to pass performance tunings and tests on P8 builders

* Fri Oct 24 2014 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-16
- Fix alternatives install

* Thu Oct 23 2014 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-15
- added pkgconfig file

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.10.1-12
- Don't fail build on make check on aarch64 due to issues with tests

* Sun Feb 16 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 3.10.1-11
- Unbreak AArch64 build.
- ARMv8 is different from ARMv7 so should not be treated as such. Otherwise
  atlas tries to do some crazy ARMv764 build and fail.

* Wed Nov 20 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-10
- updated lapack to 3.5.0

* Wed Nov 13 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-9
- updated subpackage description

* Tue Nov 05 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-8
- patch for aarch64 from https://bugzilla.redhat.com/attachment.cgi?id=755555

* Wed Oct 16 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-7
- Provides: bundled(lapack)

* Thu Oct 10 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-6
- make check on arm enabled - seems to work

* Wed Oct 2 2013 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-5
- Add -DATL_ARM_HARDFP=1 for arm build
- Rework how arm flags are set

* Mon Sep 30 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-4
- disable tests on arm to allow update for x86

* Tue Sep 24 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-3
- disable affinity to prevent crash on systems with fewer cpus

* Mon Sep 23 2013 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-2
- Add %%check section

* Fri Sep 20 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-1
- Rebase to 3.10.1
- Dropped x86_64-SSE2, ix86-SSE1, ix86-3DNow, z10, z196 (uncompilable).
- Modified incompatible patches.
- Added armv7neon support, modified archdef from softfp abi to hard abi.
- Modified Make.lib to include build-id, soname, versioned library name and symlinks.
- Now builds monolithic libsatlas (serial) and libtatlas (threaded)
  libraries with lapack and blas included.
- Lapack source tarball needed instead of static library.
- Disabled cpu throttling detection again (sorry, could not work on atlas
  otherwise, feel free to enable yet again - atlas-throttling.patch).
- Removed mentions of "Fedora" to promote redistribution.
- Modified parts of atlas.spec sometimes left in place, work still in progress,
  cleanup needed.


* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jan 27 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.8.4-8
- Rebuild for ARM glibc/binutils issues

* Fri Sep 07 2012 Orion Poplawski <orion@nwra.com> - 3.8.4-7
- Rebuild with lapack 3.4.1

* Thu Aug 09 2012 Orion Poplawski <orion@nwra.com> - 3.8.4-6
- Add patch to properly pass -melf_* to the linker with -Wl (bug 817552)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 01 2011 Deji Akingunola <dakingun@gmail.com> - 3.8.4-3
- Apply patch to enable arm build (Patch provided by Jitesh Shah <jiteshs@marvell.com>)
- Stop turning off throttle checking, upstream frown at it (seems O.K. for Koji)

* Mon Jun 20 2011 Dan Horák <dan[at]danny.cz> - 3.8.4-2
- Use -march=z10 for z196 optimised build because the builder is a z10
  (Christian Bornträger)

* Tue Jun 14 2011 Deji Akingunola <dakingun@gmail.com> - 3.8.4-1
- Update to 3.8.4
- Build the default package for SSE2 and add a SSE3 subpackage on x86_64
- Apply patch (and arch defs.) to build on s390 and s390x (Dan Horák)
- Fix-up build on s390 and s390x (Christian Bornträger)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 26 2010 Deji Akingunola <dakingun@gmail.com> - 3.8.3-18
- Create a subpackage for SSE2 on x86_64

* Sat Jul 17 2010 Dan Horák <dan[at]danny.cz> - 3.8.3-17
- rebuild against fixed lapack libraries

* Thu Jul 15 2010 Dan Horák <dan[at]danny.cz> - 3.8.3-16
- fix build on s390 (patch by Karsten Hopp)

* Wed Feb 10 2010 Deji Akingunola <dakingun@gmail.com> - 3.8.3-15
- Disable the problematic sparc patch
- Change lapack-devel BR to lapack-static, where liblapack_pic.a now resides.

* Wed Feb 03 2010 Dennis Gilmore <dennis@ausil.us> - 3.8.3-14
- fix sparc build

* Fri Jan 29 2010 Deji Akingunola <dakingun@gmail.com> - 3.8.3-13
- Remove static libraries.
- Fix typo in SSE3 subpackage's summary.

* Sat Oct 24 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-12
- Use alternatives to workaround multilib conflicts (BZ#508565). 

* Tue Sep 29 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-11
- Obsolete the -header subpackage properly. 

* Sat Sep 26 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-10
- Use the new arch. default for Pentium PRO (Fedora bug #510498)
- (Re-)Introduce 3dNow subpackage

* Sun Sep  6 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 3.8.3-9
- Rebuild against fixed lapack (see #520518)

* Thu Aug 13 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-8
- Revert the last change, it doesn't solve the problem. 

* Tue Aug 04 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-7
- Create a -header subpackage to avoid multilib conflicts (BZ#508565). 

* Tue Aug 04 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-6
- Add '-g' to build flag to allow proper genration of debuginfo subpackages (Fedora bug #509813)
- Build for F12

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 02 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-4
- Use the right -msse* option for the -sse* subpackages (Fedora bug #498715)

* Tue Apr 21 2009 Karsten Hopp <karsten@redhat.com> 3.8.3-3.1
- add s390x to 64 bit archs

* Fri Feb 27 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-3
- Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-1
- Update to version 3.8.3

* Sun Dec 21 2008 Deji Akingunola <dakingun@gmail.com> - 3.8.2-5
- Link in appropriate libs when creating shared libs, reported by Orcan 'oget' Ogetbil (BZ#475411)

* Tue Dec 16 2008 Deji Akingunola <dakingun@gmail.com> - 3.8.2-4
- Don't symlink the atlas libdir on i386, cause upgrade issue (BZ#476787)
- Fix options passed to gcc when making shared libs

* Tue Dec 16 2008 Deji Akingunola <dakingun@gmail.com> - 3.8.2-3
- Use 'gcc -shared' to build shared libs instead of stock 'ld'

* Sat Dec 13 2008 Deji Akingunola <dakingun@gmail.com> - 3.8.2-2
- Properly obsolete/provide older subpackages that are no longer packaged.

* Mon Sep 01 2008 Deji Akingunola <dakingun@gmail.com> - 3.8.2-1
- Upgrade to ver 3.8.2 with refined build procedures.

* Thu Feb 28 2008 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-15
- Disable altivec package--it is causing illegal instructions during build.

* Thu Feb 28 2008 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-14
- Enable compilation on alpha (bug 426086).
- Patch for compilation on ia64 (bug 432744).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.6.0-13
- Autorebuild for GCC 4.3

* Mon Jun  4 2007 Orion Poplawski <orion@cora.nwra.com> 3.6.0-12
- Rebuild for ppc64

* Fri Sep  8 2006 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-11
- Rebuild for FC6.
- Remove outdated comments from spec file.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-10
- Rebuild for Fedora Extras 5.
- Add --noexecstack to compilation of assembly kernels. These were
  previously marked executable, which caused problems with selinux.

* Mon Dec 19 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-9
- Rebuild for gcc 4.1.

* Mon Oct 10 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-8
- Make all devel subpackages depend on their non-devel counterparts.
- Add /etc/ld.so.conf.d files for -sse and -3dnow, because they don't
  seem to get picked up automatically.

* Wed Oct 05 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-7
- Forgot to add the new patch to sources.

* Tue Oct 04 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-6
- Use new Debian patch, and enable shared libs (they previously failed
  to build on gcc 4).
- Minor updates to description and README.Fedora file.
- Fix buildroot name to match FE preferred form.
- Fixes for custom optimized builds.
- Add dist tag.

* Wed Sep 28 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-5
- fix files lists.

* Mon Sep 26 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-4
- generate library symlinks earlier for the benefit of later linking steps.

* Wed Sep 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-3
- Change lapack dependency to lapack-devel, and use lapack_pic.a for
  building liblapack.so.

* Wed Sep 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-2
- Add "bit" macro to correctly build on x86_64.

* Tue Aug 16 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-1
- Initial version.
