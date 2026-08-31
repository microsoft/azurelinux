# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%global blaslib flexiblas
%global cmake_blas_flags -DBLA_VENDOR=FlexiBLAS
%else
%global blaslib openblas
%global blasvar o
%global cmake_blas_flags -DBLAS_LIBRARIES=%{_libdir}/lib%{blaslib}%{blasvar}.so -DLAPACK_LIBRARIES=%{_libdir}/lib%{blaslib}%{blasvar}.so
%endif

Name:               igraph
Version:            0.10.16
Release:            2%{?dist}
Summary:            Library for creating and manipulating graphs

License:             GPL-2.0-or-later
URL:                http://igraph.sourceforge.net/
Source0:            https://github.com/igraph/igraph/releases/download/%{version}/igraph-%{version}.tar.gz

BuildRequires:      gcc
BuildRequires:      gcc-c++
BuildRequires:      libxml2-devel
BuildRequires:      gmp-devel
BuildRequires:      %{blaslib}-devel
BuildRequires:      arpack-devel
BuildRequires:      glpk-devel
BuildRequires:      cmake >= 3.18

%description
igraph is a C library for complex network analysis and graph theory, with emphasis on efficiency, portability and ease of use.

%package devel
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig
Summary:    Development files for igraph

%description devel
The %{name}-devel package contains the header files and some
documentation needed to develop application with %{name}.

%prep
%setup -q

%build
%cmake \
    -DIGRAPH_ENABLE_LTO=AUTO \
    -DIGRAPH_ENABLE_TLS=1 \
    -DIGRAPH_USE_INTERNAL_BLAS=0 \
    -DIGRAPH_USE_INTERNAL_LAPACK=0 \
    -DIGRAPH_USE_INTERNAL_ARPACK=0 \
    -DIGRAPH_USE_INTERNAL_GLPK=0 \
    -DIGRAPH_USE_INTERNAL_GMP=0 \
    %{cmake_blas_flags} \
    -DIGRAPH_GRAPHML_SUPPORT=1 \
    -DCMAKE_INSTALL_INCLUDEDIR=include/
%cmake_build


%install
%cmake_install
install -Dm0644 doc/igraph.3 %{buildroot}/%{_mandir}/man3/igraph.3
find . -name '.arch-ids' | xargs rm -rf

%ifnarch ppc64le
%check
export FLEXIBLAS=netlib
%cmake_build --target check
%endif


%files
%license COPYING
%doc AUTHORS CHANGELOG.md doc/html/ ACKNOWLEDGEMENTS.md doc/licenses/
%{_libdir}/libigraph.so.3*

%files devel
%doc examples
%{_includedir}/igraph
%{_libdir}/libigraph.so
%{_libdir}/pkgconfig/igraph.pc
%{_libdir}/cmake/igraph/
%exclude %{_mandir}/man3/igraph.3*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 0.10.16-1
- 0.10.16

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 08 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.15-1
- 0.10.15

* Mon Oct 28 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.14-1
- 0.10.14

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.13-1
- 0.10.13

* Tue May 07 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.12-1
- 0.10.12

* Wed Apr 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.11-1
- 0.10.11

* Tue Feb 13 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.10-1
- 0.10.10

* Sat Feb 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.9-1
- 0.10.9

* Wed Jan 31 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.8-4
- Patch for modern C.

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.8-1
- 0.10.8

* Tue Sep 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.7-1
- 0.10.7

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.6-1
- 0.10.6

* Fri Jun 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.5-1
- 0.10.5

* Thu Mar 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.4-2
- migrated to SPDX license

* Thu Jan 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.4-1
- 0.10.4

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.3-1
- 0.10.3

* Mon Oct 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.10.2-1
- 0.10.2

* Thu Sep 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.10.1-1
- 0.10.1

* Tue Sep 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.10.0-1
- 0.10.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.9.9-1
- 0.9.9

* Mon Apr 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.9.8-1
- 0.9.8

* Thu Mar 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.9.7-1
- 0.9.7

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.9.6-1
- 0.9.6

* Fri Nov 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.5-1
- 0.9.5

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Björn Esser <besser82@fedoraproject.org> - 0.9.4-2
- Properly set BLA_VENDOR to FlexiBLAS for cmake >= 3.19

* Tue Jun 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.4-1
- 0.9.4

* Thu May 06 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.3-1
- Packaging changes suggested by upstream.

* Wed May 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.3-1
- 0.9.3

* Mon Apr 19 2021 Iñaki Úcar <iucar@fedoraproject.org> - 0.9.2-2
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager
- Enable LTO and TLS
- Use system suitesparse
- Use reference BLAS/LAPACK for tests

* Thu Apr 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.2-1
- 0.9.2

* Wed Mar 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.1-1
- 0.9.1

* Fri Feb 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.0-2
- Fix includedir in pkg config.

* Wed Feb 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.0-1
- 0.9.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.8.5-1
- 0.8.5

* Mon Nov 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.8.4-1
- 0.8.4

* Mon Oct 05 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.8.3-1
- 0.8.3

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 29 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.8.2-1
- 0.8.2

* Fri Mar 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.8.1-1
- 0.8.1

* Wed Jan 29 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.8.0-1
- 0.8.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 05 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.7.1-12
- Patch for CVE-2018-20349

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 25 2018 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.7.1-9
- Add BR on gcc-c++
- Fix FTBFS by patching printf(obj) to printf("%s", obj)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 28 2016 Than Ngo <than@redhat.com> - 0.7.1-3
- %%check: make non-fatal as temporary workaround for scipy build on secondary arch

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 30 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.1-1
- Update to 0.7.1
- Install info page from upstream

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.6.5-4
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 09 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.6.5-1
- Update to 0.6.5
- Update Source0 and URL
- Remove no longer-used patches
- Little spec clean up

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-8.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-6.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-5.2
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.5.4-3.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 0.5.4-3.1
- rebuild with new gmp

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.5.4-2
- Rebuilt for gcc bug 634757

* Thu Sep 16 2010 Neal Becker <ndbecker2@gmail.com> - 0.5.4-1
- Update to 0.5.4

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May  3 2009 Neal Becker <ndbecker2@gmail.com> - 0.5.2-4
- Try removing Provides

* Sat May  2 2009 Neal Becker <ndbecker2@gmail.com> - 0.5.2-3
- Put back Provides for devel

* Tue Apr 28 2009 Neal Becker <ndbecker2@gmail.com> - 0.5.2-2
- Try enable gmp, graphml

* Mon Apr 27 2009 Neal Becker <ndbecker2@gmail.com> - 0.5.2-1
- Update to 0.5.2
- Try not applying patch #3

* Thu Feb 26 2009 Neal Becker <ndbecker2@gmail.com> - 0.5.1-6
- Make that 0.5.1-6

* Thu Feb 26 2009 Neal Becker <ndbecker2@gmail.com> - 0.5.1-5
- Patch3 for gcc-4.4 (cstdio)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Neal Becker <ndbecker2@gmail.com> - 0.5.1-4
- Bump tag

* Sun Nov 16 2008 Neal Becker <ndbecker2@gmail.com> - 0.5.1-2
- Remove igraph-cstdlib.patch
- Remove igraph-test.patch

* Sun Nov 16 2008 Neal Becker <ndbecker2@gmail.com> - 0.5.1-1
- Update to 0.5.1

* Thu Sep 18 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-14
- Add BR libxml2-devel to get graphml support.

* Tue Feb 26 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-13
- More test fixes

* Tue Feb 26 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-12
- Fix to ignore 1 bad test

* Tue Feb 26 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-11
- Add patch for tests for gcc-4.3

* Mon Feb 25 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-10
- Run check

* Sun Feb 17 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-9
- Don't need provides

* Sun Feb 17 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-8
- Add provides to main package

* Sun Feb 17 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-7
- Add provides to devel package

* Sat Feb 16 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-6
- fix patch

* Sat Feb 16 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-5
- More patches

* Sat Feb 16 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-4
- Try again to fix patch

* Sat Feb 16 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-3
- fix patch

* Sat Feb 16 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-2
- Still need patch1

* Fri Feb 15 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-1
- update to 0.5

* Wed Feb 13 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-7
- Try again with that patch

* Wed Feb 13 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-6
- Updated igraph-cstdlib.patch

* Wed Feb 13 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-5
- Add cstdlib patch for std::exit

* Wed Jan 30 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-4
- Install examples instead of examples/simple

* Tue Jan 29 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-3
- Include examples/simple in devel doc
- Fix devel description

* Tue Jan 29 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-2
- Updates per panemade@gmail.com

* Wed Jan 23 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-1
- Initial package

