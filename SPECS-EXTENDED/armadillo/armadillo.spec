Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           armadillo
Version:        10.8.2
Release:        3%{?dist}
Summary:        Fast C++ matrix library with syntax similar to MATLAB and Octave

License:        ASL 2.0
URL:            http://arma.sourceforge.net/
Source:         http://sourceforge.net/projects/arma/files/%{name}-%{version}.tar.xz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  arpack-devel
BuildRequires:  hdf5-devel
BuildRequires:  SuperLU-devel

%global fedora 0


# flexiblas is only available on Fedora, for EPEL replace it by atlas, lapack and openblas
%if %{?fedora}
%global extra_options -DALLOW_FLEXIBLAS_LINUX=ON
BuildRequires:  flexiblas-devel
%else
%undefine __cmake_in_source_build
%global extra_options %{nil}
BuildRequires:  atlas-devel
BuildRequires:  lapack-devel
%{!?openblas_arches:%global openblas_arches x86_64 %{ix86} armv7hl %{power64} aarch64}
%ifarch %{openblas_arches}
BuildRequires:  openblas-devel
%endif
%endif

%description
Armadillo is a C++ linear algebra library (matrix maths)
aiming towards a good balance between speed and ease of use.
Integer, floating point and complex numbers are supported,
as well as a subset of trigonometric and statistics functions.
Various matrix decompositions are provided through optional
integration with LAPACK and ATLAS libraries.
A delayed evaluation approach is employed (during compile time)
to combine several operations into one and reduce (or eliminate)
the need for temporaries. This is accomplished through recursive
templates and template meta-programming.
This library is useful if C++ has been decided as the language
of choice (due to speed and/or integration capabilities), rather
than another language like Matlab or Octave.


%package devel
Summary:        Development headers and documentation for the Armadillo C++ library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libstdc++-devel
Requires:       arpack-devel
Requires:       hdf5-devel
Requires:       SuperLU-devel

%if %{?fedora}
Requires:  flexiblas-devel
%else
Requires:  atlas-devel
Requires:  lapack-devel
%ifarch %{openblas_arches}
Requires:  openblas-devel
%endif
%endif


%description devel
This package contains files necessary for development using the
Armadillo C++ library. It contains header files, example programs,
and user documentation (API reference guide).


%prep
%autosetup -p1
sed -i 's/\r//' README.md
rm -rf examples/*win64*


%build
%cmake %{extra_options}
%cmake_build


%install
%cmake_install


%check
%cmake %{extra_options} -DBUILD_SMOKE_TEST=ON
make -C "%{_vpath_builddir}"
%ctest


%if (0%{?rhel} && 0%{?rhel} <= 7)
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%endif


%files
%{_libdir}/libarmadillo.so.10*
%license LICENSE.txt NOTICE.txt

%files devel
%{_libdir}/libarmadillo.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/armadillo
%{_includedir}/armadillo_bits/
%{_datadir}/Armadillo/
%doc README.md
%doc index.html
%doc docs.html
%doc examples
%doc armadillo_icon.png
%doc mex_interface
%doc armadillo_nicta_2010.pdf
%doc rcpp_armadillo_csda_2014.pdf
%doc armadillo_joss_2016.pdf
%doc armadillo_spcs_2017.pdf
%doc armadillo_lncs_2018.pdf
%doc armadillo_solver_2020.pdf


%changelog
* Fri Aug 04 2023 Archana Choudhary <archana1@microsoft.com> - 10.8.2-3
- Initial CBL-Mariner import from Fedora (license: MIT).

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Feb  3 2022 José Matos <jamatos@fedoraproject.org> - 10.8.2-1
- update to 10.8.2

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 27 2021 José Matos <jamatos@fedoraproject.org> - 10.7.4-1
- Update to 10.7.4

* Mon Nov 22 2021 Orion Poplawski <orion@nwra.com> - 10.6.0-7
- Rebuild to tag build

* Sun Nov 21 2021 Orion Poplawski <orion@nwra.com> - 10.6.0-6
- Rebuild for hdf5 1.12.1

* Sat Oct 30 2021 Antoio Trande <sagitter@fedoraproject.org> - 10.6.0-5
- Rebuild for SuperLU-5.3.0

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 10.6.0-4
- Rebuild for hdf5 1.10.7

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 10.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 José Matos <jamatos@fedoraproject.org> - 10.6.0-1
- update to 10.6.0
- BR flexiblas for Fedora and lapack, openblas and atlas for EPEL
- adapt armadillo-devel accordingly

* Wed Jul  7 2021 José Matos <jamatos@fedoraproject.org> - 10.5.3-1
- update to 10.5.3

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 José Matos <jamatos@fedoraproject.org> - 10.2.0-1
- update to 10.2.0

* Tue Jan  5 2021 José Matos <jamatos@fedoraproject.org> - 10.1.2-1
- update to 10.1.2

* Fri Sep  4 2020 José Matos <jamatos@fedoraproject.org> - 9.900.3-2
- make extra_options empty in the correct way

* Thu Sep  3 2020 José Matos <jamatos@fedoraproject.org> - 9.900.3-1
- update to 9.900.3

* Wed Aug  5 2020 José Matos <jamatos@fedoraproject.org> - 9.900.2-5
- add upstream patch to support flexiblas
- enable tests

* Wed Aug  5 2020 José Matos <jamatos@fedoraproject.org> - 9.900.2-4
- clean the spec file and remove support for epel 6

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.900.2-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.900.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
- Adapt cmake to work with out of tree builds (and other minor cleanups)

* Fri Jul 17 2020 José Matos <jamatos@fedoraproject.org> - 9.900.2-1
- update to 9.900.2

* Fri Jul  3 2020 José Matos <jamatos@fedoraproject.org> - 9.900.1-1
- update to 9.900.1

* Thu Jun 25 2020 Orion Poplawski <orion@cora.nwra.com> - 9.880.1-2
- Rebuild for hdf5 1.10.6

* Sat May 16 2020 José Matos <jamatos@fedoraproject.org> - 9.880.1-1
- update to 9.880.1

* Wed Apr  1 2020 José Matos <jamatos@fedoraproject.org> - 9.860.1-1
- update to 9.860.1

* Sun Feb 23 2020 José Matos <jamatos@fedoraproject.org> - 9.850.1-1
- update to 9.850.1
- update list of document files

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.800.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 23 2019 José Matos <jamatos@fedoraproject.org> - 9.800.3-1
- update to 9.800.3

* Tue Aug 13 2019 José Matos <jamatos@fedoraproject.org> - 9.600.6-1
- update to 9.600.6

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.600.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 José Matos <jamatos@fedoraproject.org> - 9.600.4-1
- update to 9.600.4

* Tue Jun 11 2019 José Matos <jamatos@fedoraproject.org> - 9.500.2-1
- update to 9.500.2

* Thu May 30 2019 José Matos <jamatos@fedoraproject.org> - 9.400.4-1
- update to 9.400.4

* Sat May  4 2019 José Matos <jamatos@fedoraproject.org> - 9.400.3-1
- update to 9.400.3

* Sat Apr 27 2019 José Matos <jamatos@fedoraproject.org> - 9.400.2-1
- update to 9.400.2

* Sat Mar 30 2019 José Matos <jamatos@fedoraproject.org> - 9.300.2-1
- update to 9.300.2

* Sat Mar 16 2019 Orion Poplawski <orion@nwra.com> - 9.200.8-2
- Rebuild for hdf5 1.10.5

* Fri Mar 15 2019 José Matos <jamatos@fedoraproject.org> - 9.200.8-1
- update to 9.200.8

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.200.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 José Matos <jamatos@fedoraproject.org> - 9.200.7-1
- update to 9.200.7

* Sat Dec 22 2018 José Matos <jamatos@fedoraproject.org> - 9.200.6-1
- update to 9.200.6

* Tue Nov 20 2018 José Matos <jamatos@fedoraproject.org> - 9.200.4-1
- update to 9.200.4

* Fri Aug 17 2018 José Matos <jamatos@fedoraproject.org> - 9.100.5-1
- update to 9.100.5
- add white lines to improve spec file readability

* Fri Aug 10 2018 José Matos <jamatos@fedoraproject.org> - 8.600.1-1
- update to 8.600.1

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.600.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 José Matos <jamatos@fedoraproject.org> - 8.600.0-1
- Update to 8.600.0
- Make calls to ldconfig conditional (not needed for Fedora >= 28)

* Thu Apr 26 2018 Richard Shaw <hobbes1069@gmail.com> - 8.300.0-3.1
- Rebuild for fixed soname in SuperLU 5.2.1.

* Wed Apr 25 2018 Richard Shaw <hobbes1069@gmail.com> - 8.300.0-3
- Rebuild for SuperLU 5.2.1.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.300.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Ryan Curtin <ryan@ratml.org> - 8.300.0-1
- Update Armadillo to 8.300.0.

* Thu Oct 26 2017 Ryan Curtin <ryan@ratml.org> - 8.200.1-1
- Update Armadillo to 8.200.1.

* Sun Sep 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 8.100.1-2
- tighten %%files to track library soname

* Wed Sep 13 2017 Ryan Curtin <ryan@ratml.org> - 8.100.1-1
- Update Armadillo to 8.100.1.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.900.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.900.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat May 27 2017 José Matos <jamatos@fedoraproject.org> - 7.900.1-1
- update to 7.900.1

* Fri Mar 24 2017 José Matos <jamatos@fedoraproject.org> - 7.800.2-1
- update to 7.800.2

* Fri Mar  3 2017 José Matos <jamatos@fedoraproject.org> - 7.800.1-2
- really change the license this time (thought experiments do not count)
- remove last instance of Group in the -devel subpackage

* Fri Mar  3 2017 José Matos <jamatos@fedoraproject.org> - 7.800.1-1
- update to 7.800.1
- clean spec file

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.600.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 José Matos <jamatos@fedoraproject.org> - 7.600.2-1
- update to 7.600.2

* Thu Dec 15 2016 José Matos <jamatos@fedoraproject.org> - 7.600.1-1
- update to 7.600.1
- install pkgconfig file

* Tue Dec 06 2016 Orion Poplawski <orion@cora.nwra.com> - 7.500.0-2
- Rebuild for hdf5 1.8.18

* Fri Nov  4 2016 José Matos <jamatos@fedoraproject.org> - 7.500.0-1
- update to 7.500.0

* Fri Jul 29 2016 José Matos <jamatos@fedoraproject.org> - 7.300.1-1
- update to 7.300.1

* Sun Jul 24 2016 José Matos <jamatos@fedoraproject.org> - 7.300.0-1
- update to 7.300.0

* Wed Jul 13 2016 Dan Horák <dan[at]danny.cz> - 7.200.2-5
- switch to positive list for R/BR: openblas-devel that matches openblas' ExclusiveArch tag

* Fri Jul 01 2016 Dan Horák <dan[at]danny.cz> - 7.200.2-4
- and fix also R: in the devel subpackage

* Thu Jun 30 2016 Dan Horák <dan[at]danny.cz> - 7.200.2-3
- don't use BR: openblas-devel on s390(x)

* Wed Jun 29 2016 Orion Poplawski <orion@cora.nwra.com> - 7.200.2-2
- Rebuild for hdf5 1.8.17

* Wed Jun 29 2016 José Matos <jamatos@fedoraproject.org> - 7.200.2-1
- update to 7.200.2

* Wed Jun  8 2016 José Matos <jamatos@fedoraproject.org> - 7.200.1-1
- update to 7.200.1

* Tue May 31 2016 José Matos <jamatos@fedoraproject.org> - 7.100.3-2
- bring back lapack-devel BR or else LAPACK functions are disabled

* Mon May 30 2016 José Matos <jamatos@fedoraproject.org> - 7.100.3-1
- update to 7.100.3
- link with openblas instead of atlas

* Sat May  7 2016 José Matos <jamatos@fedoraproject.org> - 6.700.6-1
- update to 6.700.6

* Fri Apr 15 2016 José Matos <jamatos@fedoraproject.org> - 6.700.4-1
- update to 6.700.4
- superlu43 is only required for Fedora >= 24

* Tue Mar 29 2016 Mukundan Ragavan <nonamedotc@gmail.com> - 6.600.4-3
- Add SuperLU43 (compat package) as dep
- Fix cmake files for building against SuperLU43

* Sat Mar 26 2016 Mukundan Ragavan <nonamedotc@gmail.com> - 6.600.4-2
- Rebuild for SuperLU soname bump (libsuperlu.so.5.1)

* Tue Mar 15 2016 José Matos <jamatos@fedoraproject.org> - 6.600.4-1
- update to 6.600.4

* Fri Feb 12 2016 José Matos <jamatos@fedoraproject.org> - 6.500.5-1
- update to 6.500.5

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.500.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 José Matos <jamatos@fedoraproject.org> - 6.500.4-1
- update to 6.500.4
- cleaned spec file: removed %%defattr not needed in any supported
  version of fedora or epel

* Mon Sep 14 2015 José Matos <jamatos@fedoraproject.org> - 5.600.2-1
- update to 5.600.2

* Mon Aug  3 2015 José Matos <jamatos@fedoraproject.org> - 5.300.4-1
- update to 5.300.4
- add %%license tag

* Fri Jul  3 2015 José Matos <jamatos@fedoraproject.org> - 5.200.2-2
- add requires:SuperLU-devel to -devel subpackage

* Thu Jul  2 2015 José Matos <jamatos@fedoraproject.org> - 5.200.2-1
- update to 5.200.2
- add BR SuperLU-devel, required on version 5+

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.650.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.650.2-2
- Rebuilt for GCC 5 C++11 ABI change

* Fri Feb 27 2015 José Matos <jamatos@fedoraproject.org> - 4.650.2-1
- update to 4.650.2

* Fri Feb 13 2015 José Matos <jamatos@fedoraproject.org> - 4.600.4-1
- update to 4.600.4

* Fri Dec  5 2014 Ryan Curtin <ryan@ratml.org> - 4.550.2-1
- update to 4.550.2 for gcc 4.4 bug which is only relevant on EL6

* Fri Nov 28 2014 José Matos <jamatos@fedoraproject.org> - 4.550.0-1
- update to 4.550.0

* Fri Nov 14 2014 José Matos <jamatos@fedoraproject.org> - 4.500.0-1
- update to 4.500.0

* Tue Sep 23 2014 José Matos <jamatos@fedoraproject.org> - 4.450.0-1
- update to 4.450.0

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.320.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul  4 2014 José Matos <jamatos@fedoraproject.org> - 4.320.0-1
- update to 4.320.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.300.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May  4 2014 José Matos <jamatos@fedoraproject.org> - 4.300.0-2
- add hdf5-devel as build requirement and also as required for the
  -devel sub-package

* Fri May  2 2014 José Matos <jamatos@fedoraproject.org> - 4.300.0-1
- update to 4.300.0

* Wed Apr  9 2014 José Matos <jamatos@fedoraproject.org> - 4.200.0-1
- update to 4.200.0

* Fri Mar 14 2014 José Matos <jamatos@fedoraproject.org> - 4.100.2-1
- update to 4.100.2

* Sun Mar  2 2014 José Matos <jamatos@fedoraproject.org> - 4.100.0-1
- update to 4.100.0

* Sat Jan 25 2014 José Matos <jamatos@fedoraproject.org> - 4.000.2-1
- update to 4.000.2

* Fri Jan 10 2014 José Matos <jamatos@fedoraproject.org> - 4.000.0-2
- add mex_interface to documentation (demonstration of how to connect
  Armadillo with MATLAB/Octave mex functions)

* Thu Jan  9 2014 José Matos <jamatos@fedoraproject.org> - 4.000.0-1
- update to 4.000.0
- dropped boost dependency and added arpack
- remove reference to boost in the comments

* Tue Dec 10 2013 José Matos <jamatos@fedoraproject.org> - 3.930.1-1
- update to 3.930.1
- update the name of the documentation paper from 2013 to 2014

* Mon Nov 25 2013 José Matos <jamatos@fedoraproject.org> - 3.920.3-1
- update to 3.920.3

* Tue Oct 29 2013 José Matos <jamatos@fedoraproject.org> - 3.920.2-1
- update to 3.920.2

* Mon Sep 30 2013 José Matos <jamatos@fedoraproject.org> - 3.920.1-1
- update to 3.920.1

* Mon Sep 30 2013 José Matos <jamatos@fedoraproject.org> - 3.920.0-1
- update to 3.920.0

* Sun Sep 22 2013 Orion Poplawski - 3.910.0-2
- Rebuild for atlas 3.10

* Fri Aug 16 2013 José Matos <jamatos@fedoraproject.org> - 3.910.0-1
- update to 3.910.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.900.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 3.900.4-2
- Rebuild for boost 1.54.0

* Wed Jun 12 2013 José Matos <jamatos@fedoraproject.org> - 3.900.4-1
- update to 3.900.4

* Mon May 13 2013 José Matos <jamatos@fedoraproject.org> - 3.820.0-1
- update to 3.820.0

* Tue Apr 30 2013 José Matos <jamatos@fedoraproject.org> - 3.810.2-1
- Update to latest stable version

* Sun Apr 21 2013 José Matos <jamatos@fedoraproject.org> - 3.810.0-1
- Update to latest stable version

* Sun Apr 14 2013 José Matos <jamatos@fedoraproject.org> - 3.800.2-1
- Update to latest stable version

* Sat Mar  2 2013 José Matos <jamatos@fedoraproject.org> - 3.800.0-1
- Update to latest stable version
- License changed from LGPLv3+ to MPLv2.0
- Added another documentation file (rcpp related)
- Spec changelog trimmed

* Thu Feb 21 2013 José Matos <jamatos@fedoraproject.org> - 3.6.3-1
- Update to latest stable release

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.6.2-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.6.2-2
- Rebuild for Boost-1.53.0

* Fri Feb  8 2013 José Matos <jamatos@fedoraproject.org> - 3.6.2-1
- Update to latest stable release

* Mon Dec 17 2012 José Matos <jamatos@fedoraproject.org> - 3.6.1-1
- Update to latest stable release

* Sat Dec  8 2012 José Matos <jamatos@fedoraproject.org> - 3.6.0-1
- Update to latest stable release

* Mon Dec  3 2012 José Matos <jamatos@fedoraproject.org> - 3.4.4-1
- Update to latest stable release
- Clean the spec files (documentation has a special treatment with rpm)

* Wed Jul 25 2012 José Matos <jamatos@fedoraproject.org> - 3.2.4-1
- Update to version 3.2.4

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Conrad Sanderson - 2.2.3-1
- spec updated for Armadillo 2.2.3

* Mon Apr 18 2011 Conrad Sanderson - 1.2.0-1
- spec updated for Armadillo 1.2.0

* Mon Nov 15 2010 Conrad Sanderson - 1.0.0-1
- spec updated for Armadillo 1.0.0
