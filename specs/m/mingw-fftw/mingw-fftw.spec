# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global mingw_pkg_name fftw
%global openmp 0

Name:           mingw-%{mingw_pkg_name}
Version:        3.3.8
Release: 20%{?dist}
Summary:        MinGW Fast Fourier Transform library
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            http://www.fftw.org
Source0:        http://www.fftw.org/fftw-%{version}.tar.gz

BuildRequires: make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-gcc-gfortran
BuildRequires:  mingw64-gcc-gfortran
BuildArch:      noarch


%description
This package contains the MinGW windows port of the FFTW library.

FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

# Mingw32
%package -n mingw32-%{mingw_pkg_name}
Summary:                %{summary}

%description -n mingw32-%{mingw_pkg_name}
This package contains the MinGW win32 port of the FFTW library.

FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains cross-compiled libraries and development tools
for Windows.

%package -n mingw32-%{mingw_pkg_name}-static
Summary:                %{summary}

%description -n mingw32-%{mingw_pkg_name}-static
This package contains the MinGW win32 port of the FFTW library.

FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains static cross-compiled library

# Mingw64
%package -n mingw64-%{mingw_pkg_name}
Summary:                %{summary}

%description -n mingw64-%{mingw_pkg_name}
This package contains the MinGW win64 port of the FFTW library.

FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains cross-compiled libraries and development tools
for Windows.

%package -n mingw64-%{mingw_pkg_name}-static
Summary:                %{summary}

%description -n mingw64-%{mingw_pkg_name}-static
This package contains the MinGW win64 port of the FFTW library.

FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains static cross-compiled library

%{?mingw_debug_package}

%prep
%setup -q -n %{mingw_pkg_name}-%{version}


%build

BASEFLAGS="--enable-shared --disable-dependency-tracking --disable-threads"
%if %{openmp}
BASEFLAGS="$BASEFLAGS --enable-openmp"
%endif

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

# Loop over precisions
for((iprec=0;iprec<4;iprec++))
do
  export MINGW_BUILDDIR_SUFFIX=${prec_name[iprec]}
  export MINGW_CONFIGURE_ARGS="${BASEFLAGS} ${prec_flags[iprec]}"
  %mingw_configure 
  %mingw_make %{?_smp_mflags}
done

%install
# Precisions to build
prec_name[0]=single
prec_name[1]=double
prec_name[2]=long
prec_name[3]=quad

rm -rf %{buildroot}
for((iprec=0;iprec<4;iprec++))
do
  export MINGW_BUILDDIR_SUFFIX=${prec_name[iprec]}
 %mingw_make install DESTDIR=%{buildroot}
done
rm -f %{buildroot}%{mingw32_infodir}/dir
rm -f %{buildroot}%{mingw64_infodir}/dir
rm -f %{buildroot}%{mingw32_libdir}/*.la
rm -f %{buildroot}%{mingw64_libdir}/*.la

rm -f %{buildroot}%{mingw32_bindir}/fftw*-wisdom*
rm -f %{buildroot}%{mingw64_bindir}/fftw*-wisdom*
rm -rf %{buildroot}%{mingw32_infodir}
rm -rf %{buildroot}%{mingw64_infodir}
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}


%files -n mingw32-%{mingw_pkg_name}
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{mingw32_bindir}/libfftw3f-3.dll
%{mingw32_bindir}/libfftw3-3.dll
%{mingw32_bindir}/libfftw3l-3.dll
%{mingw32_libdir}/libfftw3f.dll.a
%{mingw32_libdir}/libfftw3.dll.a
%{mingw32_libdir}/libfftw3l.dll.a
%if %{openmp}
%{mingw32_bindir}/libfftw3f_omp-3.dll
%{mingw32_bindir}/libfftw3_omp-3.dll
%{mingw32_bindir}/libfftw3l_omp-3.dll
%{mingw32_libdir}/libfftw3f_omp.dll.a
%{mingw32_libdir}/libfftw3_omp.dll.a
%{mingw32_libdir}/libfftw3l_omp.dll.a
%endif
%{mingw32_includedir}/fftw3*
%{mingw32_libdir}/pkgconfig/fftw3f.pc
%{mingw32_libdir}/pkgconfig/fftw3.pc
%{mingw32_libdir}/pkgconfig/fftw3l.pc
%{mingw32_libdir}/pkgconfig/fftw3q.pc
%dir %{mingw32_libdir}/cmake/fftw3
%{mingw32_libdir}/cmake/fftw3/FFTW3Config.cmake
%{mingw32_libdir}/cmake/fftw3/FFTW3ConfigVersion.cmake
%{mingw32_libdir}/cmake/fftw3/FFTW3fConfig.cmake
%{mingw32_libdir}/cmake/fftw3/FFTW3fConfigVersion.cmake
%{mingw32_libdir}/cmake/fftw3/FFTW3lConfig.cmake
%{mingw32_libdir}/cmake/fftw3/FFTW3lConfigVersion.cmake
%{mingw32_libdir}/cmake/fftw3/FFTW3qConfig.cmake
%{mingw32_libdir}/cmake/fftw3/FFTW3qConfigVersion.cmake

%files -n mingw32-%{mingw_pkg_name}-static
%{mingw32_libdir}/libfftw3f.a
%{mingw32_libdir}/libfftw3.a
%{mingw32_libdir}/libfftw3l.a
%{mingw32_libdir}/libfftw3q.a

%files -n mingw64-%{mingw_pkg_name}
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{mingw64_bindir}/libfftw3f-3.dll
%{mingw64_bindir}/libfftw3-3.dll
%{mingw64_bindir}/libfftw3l-3.dll
%{mingw64_libdir}/libfftw3f.dll.a
%{mingw64_libdir}/libfftw3.dll.a
%{mingw64_libdir}/libfftw3l.dll.a
%if %{openmp}
%{mingw64_bindir}/libfftw3f_omp-3.dll
%{mingw64_bindir}/libfftw3_omp-3.dll
%{mingw64_bindir}/libfftw3l_omp-3.dll
%{mingw64_libdir}/libfftw3f_omp.dll.a
%{mingw64_libdir}/libfftw3_omp.dll.a
%{mingw64_libdir}/libfftw3l_omp.dll.a
%endif
%{mingw64_includedir}/fftw3*
%{mingw64_libdir}/pkgconfig/fftw3f.pc
%{mingw64_libdir}/pkgconfig/fftw3.pc
%{mingw64_libdir}/pkgconfig/fftw3l.pc
%{mingw64_libdir}/pkgconfig/fftw3q.pc
%dir %{mingw64_libdir}/cmake/fftw3
%{mingw64_libdir}/cmake/fftw3/FFTW3Config.cmake
%{mingw64_libdir}/cmake/fftw3/FFTW3ConfigVersion.cmake
%{mingw64_libdir}/cmake/fftw3/FFTW3fConfig.cmake
%{mingw64_libdir}/cmake/fftw3/FFTW3fConfigVersion.cmake
%{mingw64_libdir}/cmake/fftw3/FFTW3lConfig.cmake
%{mingw64_libdir}/cmake/fftw3/FFTW3lConfigVersion.cmake
%{mingw64_libdir}/cmake/fftw3/FFTW3qConfig.cmake
%{mingw64_libdir}/cmake/fftw3/FFTW3qConfigVersion.cmake

%files -n mingw64-%{mingw_pkg_name}-static
%{mingw64_libdir}/libfftw3f.a
%{mingw64_libdir}/libfftw3.a
%{mingw64_libdir}/libfftw3l.a
%{mingw64_libdir}/libfftw3q.a

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 3.3.8-17
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3.3.8-10
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 3.3.8-4
- Rebuild (Changes/Mingw32GccDwarf2)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 02 2018 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.3.8-1
- update to 3.3.8

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 01 2016 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.3.5-1
- update to 3.3.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr  2 2014 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.3.4-1
- update to 3.3.4

* Mon Aug  5 2013 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.3.3-2
- clean up according to comments from Erik van Pienbroek

* Sat Jan 19 2013 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.3.3-1
- update to 3.3.3

* Sat Aug 25 2012 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.3.1-1
- create from native spec file

