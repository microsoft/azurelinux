%undefine _ld_as_needed

%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
%global arch64 1
%else
%global arch64 0
%endif

Name:    metis
Version: 5.1.0.3
Release: 7%{?dist}
Summary: Serial Graph Partitioning and Fill-reducing Matrix Ordering
License: Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:     http://glaros.dtc.umn.edu/gkhome/views/%{name}
Source0: https://github.com/scivision/METIS/archive/refs/tags/v%{version}/METIS-%{version}.tar.gz

## This patch sets up libmetis soname of libmetis
Patch0:  %{name}-libmetis.patch

## This patch sets up shared GKlib library 
Patch1:  %{name}-shared-GKlib.patch

## This patch sets up GKREGEX, GKRAND, libsuffix options to the Makefiles 
Patch3:  %{name}-GKREGEX-GKRAND-LIBSUFFIX-fix.patch

## Rename library of 64 integer version
Patch4: %{name}_lib64.patch

Patch5: %{name}-pcre2.patch

BuildRequires: make
BuildRequires: cmake, gcc, gcc-c++
%if 0%{?rhel} && 0%{?rhel} < 9
BuildRequires: pcre-devel
%else
BuildRequires: pcre2-devel
%endif
BuildRequires: help2man
BuildRequires: chrpath
#BuildRequires: GKlib-devel

%description
METIS is a set of serial programs for partitioning graphs, 
partitioning finite element meshes, and producing fill reducing 
orderings for sparse matrices. 
The algorithms implemented in METIS are based on the multilevel 
recursive-bisection, multilevel k-way, and multi-constraint 
partitioning schemes developed in our lab.
METIS is distributed with OpenMP support.

%package devel
Summary: METIS headers and development-related files
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Header and library files of Metis.

%if 0%{?arch64}
%package -n metis64
Summary: Serial Graph Partitioning and Fill-reducing Matrix Ordering (64bit INTEGER)

%description -n metis64
METIS is a set of serial programs for partitioning graphs, 
partitioning finite element meshes, and producing fill reducing 
orderings for sparse matrices. 
The algorithms implemented in METIS are based on the multilevel 
recursive-bisection, multilevel k-way, and multi-constraint 
partitioning schemes developed in our lab.
METIS is distributed with OpenMP support.
This build has 64bit INTEGER support.

%package -n metis64-devel
Summary: METIS development libraries (64bit INTEGER)
Requires: metis64%{?_isa} = %{version}-%{release}

%description -n metis64-devel
Header and library files of Metis,
OpenMP version (64bit INTEGER).
%endif

%prep
%setup -qc 
 
pushd METIS-%{version}
rm -rf archive

%patch -P 0 -p0 -b .backup
%patch -P 1 -p0 -b .backup
%patch -P 3 -p0 -b .backup
%patch -P 5 -p0 -b .backup
popd

%if 0%{?arch64}
cp -a METIS-%{version} metis64
pushd metis64
%patch -P 4 -p0 -b .backup
popd
%endif

%build
%if 0%{?rhel} && 0%{?rhel} < 9
PCRE_LDFLAGS="-lpcreposix"
%else
PCRE_LDFLAGS="-lpcre2-posix"
%endif
%cmake -S METIS-%{version} -B METIS-%{version} \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DGKLIB_PATH=METIS-%{version}/src//GKlib \
 -DGKRAND:BOOL=ON \
 -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES\
 -DSHARED:BOOL=TRUE \
 -DOPENMP:BOOL=ON \
 -DPCRE:BOOL=ON \
 -DCMAKE_C_FLAGS:STRING="%{optflags} -pthread" \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} $PCRE_LDFLAGS" \
 -DCMAKE_EXE_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} $PCRE_LDFLAGS" \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=TRUE \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}
%make_build -C METIS-%{version}

%if 0%{?arch64}
%if 0%{?rhel} && 0%{?rhel} < 9
PCRE_LDFLAGS="-lpcreposix"
%else
PCRE_LDFLAGS="-lpcre2-posix"
%endif
%cmake -S metis64 -B metis64 \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -Dintsize:STRING=64 -Drealsize:STRING=64 \
 -DGKLIB_PATH=METIS-%{version}/src/GKlib \
 -DGKRAND:BOOL=ON \
 -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES\
 -DSHARED:BOOL=TRUE \
 -DOPENMP:BOOL=ON \
 -DPCRE:BOOL=ON \
 -DCMAKE_C_FLAGS:STRING="%{optflags} -pthread" \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} $PCRE_LDFLAGS" \
 -DCMAKE_EXE_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} $PCRE_LDFLAGS" \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=TRUE \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}
%make_build -C metis64
%endif

%install
pushd METIS-%{version}
%make_install

## Generate manpages from binaries
LD_PRELOAD=%{buildroot}%{_libdir}/lib%{name}.so.0 \
help2man --version-string="%{version}" -n "Partitions a graph into a specified number of parts." \
 -N --output="gpmetis.1" --no-discard-stderr --help-option="-help" %{buildroot}%{_bindir}/gpmetis

LD_PRELOAD=%{buildroot}%{_libdir}/lib%{name}.so.0 \
help2man --version-string="%{version}" \
 -n "Computes a fill-reducing ordering of the vertices of the graph using multilevel nested dissection." \
 -N --output="ndmetis.1" --no-discard-stderr --help-option="-help" %{buildroot}%{_bindir}/ndmetis

LD_PRELOAD=%{buildroot}%{_libdir}/lib%{name}.so.0 \
help2man --version-string="%{version}" -n "Partitions a mesh into a specified number of parts." \
 -N --output="mpmetis.1" --no-discard-stderr --help-option="-help" %{buildroot}%{_bindir}/mpmetis

LD_PRELOAD=%{buildroot}%{_libdir}/lib%{name}.so.0 \
help2man --version-string="%{version}" -n "Converts a mesh into a graph that is compatible with METIS." \
 -N --output="m2gmetis.1" --no-discard-stderr -h "-help" %{buildroot}%{_bindir}/m2gmetis

mkdir -p %{buildroot}%{_mandir}/man1
mv *.1 %{buildroot}%{_mandir}/man1
popd

# Save metis.h with IDXTYPEWIDTH = 32
mv %{buildroot}%{_includedir}/metis.h %{buildroot}%{_includedir}/metis32.h

%if 0%{?arch64}
pushd metis64
%make_install
# Save metis.h with IDXTYPEWIDTH = 64
mv %{buildroot}%{_includedir}/metis.h %{buildroot}%{_includedir}/metis64.h
popd
%endif

# Save metis.h with IDXTYPEWIDTH = 32
mv %{buildroot}%{_includedir}/metis32.h %{buildroot}%{_includedir}/metis.h

## Remove rpaths
chrpath -d %{buildroot}%{_bindir}/*

%check
cp -p %{buildroot}%{_bindir}/*metis METIS-%{version}/src/graphs/
cp -p %{buildroot}%{_bindir}/graphchk METIS-%{version}/src/graphs/
cd METIS-%{version}/src/graphs
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH ./ndmetis mdual.graph
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH ./mpmetis metis.mesh 2
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH ./gpmetis test.mgraph 4
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH ./gpmetis copter2.graph 4
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH ./graphchk 4elt.graph
cd ../../
%ctest -- --test-dir ./
cd ../
%if 0%{?arch64}
cp -p %{buildroot}%{_bindir}/*metis64 metis64/src/graphs/
cp -p %{buildroot}%{_bindir}/graphchk64 metis64/src/graphs/
cd metis64/src/graphs
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH ./ndmetis64 mdual.graph
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH ./mpmetis64 metis.mesh 2
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH ./gpmetis64 test.mgraph 4
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH ./gpmetis64 copter2.graph 4
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH ./graphchk64 4elt.graph
cd ../../
%ctest -- --test-dir ./
cd ../
%endif

%files
%doc METIS-%{version}/src/Changelog METIS-%{version}/src/manual/manual.pdf
%license METIS-%{version}/src/LICENSE.txt
%{_bindir}/cmpfillin
%{_bindir}/gpmetis
%{_bindir}/graphchk
%{_bindir}/m2gmetis
%{_bindir}/mpmetis
%{_bindir}/ndmetis
%{_mandir}/man1/*.1.gz
%{_libdir}/lib%{name}.so.0

%files devel
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so

%if 0%{?arch64}
%files -n metis64
%doc metis64/src/Changelog metis64/src/manual/manual.pdf
%license metis64/src/LICENSE.txt
%{_bindir}/cmpfillin64
%{_bindir}/gpmetis64
%{_bindir}/graphchk64
%{_bindir}/m2gmetis64
%{_bindir}/mpmetis64
%{_bindir}/ndmetis64
%{_libdir}/lib%{name}64.so.0

%files -n metis64-devel
%{_includedir}/%{name}64.h
%{_libdir}/lib%{name}64.so
%endif

%changelog
* Thu Jan 03 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 5.1.0.3-7
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 17 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.1.0.3-3
- Fix License tag

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 16 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.1.0.3-1
- Use modernized build system| New source code archive

* Sun Jul 16 2023 Antonio Trande <sagitter@fedoraproject.org> - 5.1.0-51
- Renew SPEC file

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Petr Písař <ppisar@redhat.com> - 5.1.0-46
- Rebuild against pcre2-10.37 (bug #1965025)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Antonio T <sagitter@fedoraproject.org> - 5.1.0-44
- Change CMake options /4

* Sat Jan 23 2021 Antonio T <sagitter@fedoraproject.org> - 5.1.0-43
- Change CMake options /3

* Sat Jan 23 2021 Antonio T <sagitter@fedoraproject.org> - 5.1.0-42
- Change CMake options /2

* Sat Jan 23 2021 Antonio T <sagitter@fedoraproject.org> - 5.1.0-41
- Change CMake options

* Fri Jan 08 2021 Tom Stellard <tstellar@redhat.com> - 5.1.0-40
- Add BuildRequires: make

* Tue Aug 04 2020 sagitter <sagitter@fedoraproject.org> - 5.1.0-39
- Enable __cmake_in_source_build

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-38
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Merlin Mathesius <mmathesi@redhat.com> - 5.1.0-36
- Minor conditional fixes for ELN

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 sagitter <sagitter@fedoraproject.org> - 5.1.0-34
- Fix BR packages

* Sat Jan 25 2020 sagitter <sagitter@fedoraproject.org> - 5.1.0-33
- Remove old conditions

* Thu Oct 24 2019 sagitter <sagitter@fedoraproject.org> - 5.1.0-32
- Fix descriptions

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 05 2019 sagitter <sagitter@fedoraproject.org> - 5.1.0-30
- Disable as-needed flag again

* Tue Feb 05 2019 sagitter <sagitter@fedoraproject.org> - 5.1.0-29
- Use pcre2 on Fedora 30+

* Tue Feb 05 2019 sagitter <sagitter@fedoraproject.org> - 5.1.0-28
- Disable as-needed linker flag

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.1.0-26
- Fix RHEL conditions

* Sun Nov 04 2018 sagitter <sagitter@fedoraproject.org> - 5.1.0-25
- Another fix

* Sun Nov 04 2018 sagitter <sagitter@fedoraproject.org> - 5.1.0-24
- Fix autosetup macro

* Sun Nov 04 2018 sagitter <sagitter@fedoraproject.org> - 5.1.0-23
- Some minor changes

* Sun Jul 15 2018 sagitter <sagitter@fedoraproject.org> - 5.1.0-22
- Add gcc-c++ as BR

* Sun Jul 15 2018 sagitter <sagitter@fedoraproject.org> - 5.1.0-21
- Add gcc as BR

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Feb 17 2018 sagitter <sagitter@fedoraproject.org> - 5.1.0-19
- Fix %%%%ldconfig_scriptlets for metis64

* Sat Feb 17 2018 sagitter <sagitter@fedoraproject.org> - 5.1.0-18
- Use %%%%ldconfig_scriptlets

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-16
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 18 2016 sagitter <sagitter@fedoraproject.org> - 5.1.0-13
- Build 64 integer version

* Thu Feb 04 2016 Dennis Gilmore <dennis@ausil.us> - 5.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 sagitter <sagitter@fedoraproject.org> - 5.1.0-11
- Removed ExcludeArch

* Wed Jan 20 2016 sagitter <sagitter@fedoraproject.org> - 5.1.0-10
- Defined OpenMP support

* Wed Dec 23 2015 sagitter <sagitter@fedoraproject.org> - 5.1.0-9
- Used always 'cmake' compiler

* Thu Oct 29 2015 sagitter <sagitter@fedoraproject.org> - 5.1.0-8
- Rebuild for cmake 3.4.0

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 5.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 sagitter <sagitterATfedoraprojectDOTorg> - 5.1.0-6
- Built on EPEL7

* Sun Aug 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 5.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 5.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 19 2014 sagitter <anto.trande@gmail.com> - 5.1.0-3
- F21 rebuild

* Sat Aug 03 2013 Dennis Gilmore <dennis@ausil.us> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 14 2013 sagitter <anto.trande@gmail.com> - 5.1.0-1
- Update version

* Sun Mar 31 2013 sagitter <anto.trande@gmail.com> - 5.0.3-8
- Initial import (#920518).

* Sun Mar 24 2013 sagitter <anto.trande@gmail.com> - 5.0.3-7
- Initial import (#920518)

* Sun Mar 24 2013 sagitter <anto.trande@gmail.com> - 5.0.3-6
- Initial import (#920518)

* Sun Mar 24 2013 sagitter <anto.trande@gmail.com> - 5.0.3-5
- Initial import (#920518)

* Sun Mar 24 2013 sagitter <anto.trande@gmail.com> - 5.0.3-4
- Initial import (#920518)

* Sun Mar 24 2013 sagitter <anto.trande@gmail.com> - 5.0.3-3
- Initial import (#920518)

* Sun Mar 24 2013 sagitter <anto.trande@gmail.com> - 5.0.3-2
- Initial import (#920518)

* Thu Mar 21 2013 sagitter <anto.trande@gmail.com> - 5.0.3-1
- Initial import (#920518).
