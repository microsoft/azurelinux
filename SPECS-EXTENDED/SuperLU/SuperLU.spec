Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global genname superlu

## The RPM macro for the linker flags does not exist on EPEL
%if 0%{?rhel} && 0%{?rhel} < 7
%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro}
%endif

Name:			SuperLU
Version:		7.0.0
Release:		1%{?dist}
Summary:		Subroutines to solve sparse linear systems
License:		BSD-2-Clause AND GPL-2.0-or-later
URL:			http://crd-legacy.lbl.gov/~xiaoye/SuperLU/

Source0:		https://github.com/xiaoyeli/%{genname}/archive/refs/tags/v%{version}.tar.gz#/%{genname}-%{version}.tar.gz

# Use a pre-made configuration file for Make
Source1:      %{name}-fedora-make.inc.in
Patch0:	      %{genname}-removemc64.patch

# Fix ldflags of example files
Patch1:       %{name}-fix_example_builds.patch

BuildRequires:  openblas-devel, openblas-srpm-macros
BuildRequires:  metis-devel
BuildRequires:	gcc
%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:	gcc-gfortran
BuildRequires:	csh

%description
SuperLU contains a set of subroutines to solve a sparse linear system 
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP). 
The columns of A may be preordered before factorization; the 
preordering for sparsity is completely separate from the factorization.

%package devel
Summary:		Header files and libraries for SuperLU development
Requires:		%{name}%{?_isa}		=  %{version}-%{release}

%description devel 
The %{name}-devel package contains the header files
and libraries for use with %{name} package.

%package doc
Summary:		Documentation and Examples for SuperLU
Requires:		%{name}%{?_isa} = %{version}-%{release}

%description doc
The %{name}-doc package contains all the help documentation along with C
and FORTRAN examples.

%prep
%autosetup -n %{genname}-%{version} -p1

rm -f make.inc
cp -pf %{SOURCE1} make.inc.in

# Remove bundled BLAS
rm -rf CBLAS

rm -fr SRC/mc64ad.f.bak
find . -type f | sed -e "/TESTING/d" | xargs chmod a-x

# Remove the shippped executables from EXAMPLE
find EXAMPLE -type f | while read file
do
   [ "$(file $file | awk '{print $2}')" = ELF ] && rm $file || :
done

# Change optimization level
sed -e 's|-O0|-O2|g' -i SRC/CMakeLists.txt

%build
%cmake \
   -Denable_internal_blaslib:BOOL=NO \
   -DXSDK_ENABLE_Fortran:BOOL=OFF \
   -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{__global_fflags}" \
   -DTPL_BLAS_LIBRARIES="`pkg-config --libs flexiblas`" \
   -DTPL_ENABLE_METISLIB:BOOL=ON \
   -DTPL_METIS_INCLUDE_DIRS:PATH=%{_includedir} \
   -DTPL_METIS_LIBRARIES:FILEPATH=%{_libdir}/libmetis.so \
   -DCMAKE_BUILD_TYPE:STRING=Release \
   -DCMAKE_INSTALL_INCLUDEDIR:PATH=include/%{name} \
   -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
   -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES
%cmake_build

%install
%cmake_install

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:MATGEN
%ctest

%files
%license License.txt
%{_libdir}/libsuperlu.so.7
%{_libdir}/libsuperlu.so.%{version}

%files devel
%{_includedir}/
%{_libdir}/libsuperlu.so
%{_libdir}/cmake/%{genname}/
%{_libdir}/pkgconfig/%{genname}.pc

%files doc
%license License.txt
%doc DOC EXAMPLE FORTRAN

%changelog
* Tue Oct 15 2024 Jyoti Kanase <v-jykanase@microsoft.com> - 7.0.0-1
- Update to 7.0.0
-License verified

* Sat Jul 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.2.1-10
- Removing unused BR on "atlas".

* Mon Jun 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.2.1-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removing BR on "blas-devel".

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 14 2018 Antonio Trande <sagitterATfedoraproject.org> - 5.2.1-5
- Remove gcc-gfortran as required package

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 25 2018 Antonio Trande <sagitterATfedoraproject.org> - 5.2.1-3
- Patch soname (5 -> 5.2) of shared library

* Sun Apr 15 2018 Antonio Trande <sagitterATfedoraproject.org> - 5.2.1-2
- Use cmake3 on rhel
- Use blas from system

* Fri Apr 13 2018 Rafael dos Santos <rdossant@redhat.com> - 5.2.1-1
- Update to 5.2.1
- Use cmake build system
- Drop obsolete patches
- Resolves #1547494 - build with standard Fedora flags

* Wed Feb 21 2018 Antonio Trande <sagitterATfedoraproject.org> - 5.2.0-8
- Add gcc BR
- Remove el5 bits

* Thu Feb 15 2018 Antonio Trande <sagitterATfedoraproject.org> - 5.2.0-7
- Use %%ldconfig_scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Oct 21 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 5.2.0-5
- Fix lib linking in EPEL (added conditionals; Thanks Antonio Trande))
- Use license macro

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr 14 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0
- spec file cleanup

* Mon Mar 28 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 5.1.1-2
- Added -doc subpackage
- Added GPLv2 in the license field

* Mon Mar 21 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 5.1.1-1
- Update to 5.1.1
- Remove format security patch - not needed anymore
- Edit patches to be version specific
- Renamed patch4 to be consistent with others
- Minor spec file housekeeping

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan 25 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.3-12
- Fix spec file errors and remove backup files
- fixes 1084707

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 13 2014 Mukundan Ragavan <nonamedotc@gmail.com> - 4.3-10
- Removed non-free files, fixes bz#1114264

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 06 2014 Björn Esser <bjoern.esser@gmail.com> - 4.3-8
- fixed FTBFS if "-Werror=format-security" flag is used (#1037343)
- devel-pkg must Requires: %%{name}%%{?_isa}
- apply proper LDFLAGS
- added needed bits for el5
- reenable testsuite using Patch3

* Fri Oct 4 2013 Orion Poplawski <orion@cora.nwra.com> - 4.3-7
- Rebuild for atlas 3.10
- Handle UnversionedDocDirs change

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-5
- Ship SuperLU examples

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-3
- Use README in main package and DOC in devel package
- chmod a-x on SRC/qselect.c
- Remove -latlas linking in prep section
- Added Patch comments
- Use name RPM macro in patch name

* Wed Feb 01 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-2
- Use atlas library instead of blas.
- Use RPM_OPT_FLAGS and LIBS when building sources.
- Use macros as required for name and version.

* Fri Jan 06 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-1
- First release.
