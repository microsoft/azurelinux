%undefine __cmake_in_source_build

# TODO: A Julia interface is now available, but requires
# https://github.com/JuliaInterop/libcxxwrap-julia, which is not currently
# available in Fedora.

# TODO: A JavaScript interface is now available.  Given the generally poor
# state of JavaScript in Fedora, I do not plan to add a subpackage for it
# unless somebody is really, really persuasive and available to help fix it
# if it breaks.

# Tests are off by default because some of the tests require more memory than
# the koji builders have available.
%bcond test 0

%global giturl  https://github.com/Z3Prover/z3

Name:           z3
Version:        4.13.3
Release:        1%{?dist}
Summary:        Satisfiability Modulo Theories (SMT) solver
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

License:        MIT
URL:            https://github.com/Z3Prover/z3/wiki
VCS :           git:%{giturl}.git
Source:         %{giturl}/archive/%{name}-%{version}.tar.gz
# Do not try to build or install native OCaml artifacts on bytecode-only arches
Patch:          %{name}-ocaml.patch

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  gmp-devel
BuildRequires:  graphviz
BuildRequires:  help2man
%ifarch %{java_arches}
BuildRequires:  java-devel
BuildRequires:  javapackages-tools
%endif
BuildRequires:  make
BuildRequires:  ninja-build
%ifnarch %{ix86}
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-zarith-devel
%endif
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}

%description
Z3 is a satisfiability modulo theories (SMT) solver; given a set of
constraints with variables, it reports a set of values for those
variables that would meet the constraints.  The Z3 input format is an
extension of the one defined by the SMT-LIB 2.0 standard.  Z3 supports
arithmetic, fixed-size bit-vectors, extensional arrays, datatypes,
uninterpreted functions, and quantifiers.

%package libs
Summary:        Library for applications that use z3 functionality

# This can be removed when F40 reaches EOL
%ifnarch %{java_arches}
Obsoletes:      java-z3 < 4.8.17-5
%endif

%description libs
Library for applications that use z3 functionality.

%package devel
Summary:        Header files for build applications that use z3
Requires:       z3-libs%{?_isa} = %{version}-%{release}

%description devel
Header files for build applications that use z3.

%package doc
# The content is MIT.
# Two files in examples are GPL-3.0-or-later WITH Bison-exception 2.2:
# examples/tptp/tptp5.tab.c
# examples/tptp/tptp5.tab.c
# Other licenses are due to files installed by doxygen.
# html/bc_s.png: GPL-1.0-or-later
# html/bdwn.png: GPL-1.0-or-later
# html/closed.png: GPL-1.0-or-later
# html/doc.png: GPL-1.0-or-later
# html/doxygen.css: GPL-1.0-or-later
# html/doxygen.svg: GPL-1.0-or-later
# html/dynsections.js: MIT
# html/folderclosed.png: GPL-1.0-or-later
# html/folderopen.png: GPL-1.0-or-later
# html/jquery.js: MIT
# html/nav_f.png: GPL-1.0-or-later
# html/nav_g.png: GPL-1.0-or-later
# html/nav_h.png: GPL-1.0-or-later
# html/open.png: GPL-1.0-or-later
# html/search/search.css: GPL-1.0-or-later
# html/search/search.js: MIT
# html/search/search_l.png: GPL-1.0-or-later
# html/search/search_m.png: GPL-1.0-or-later
# html/search/search_r.png: GPL-1.0-or-later
# html/splitbar.png: GPL-1.0-or-later
# html/sync_off.png: GPL-1.0-or-later
# html/sync_on.png: GPL-1.0-or-later
# html/tab_a.png: GPL-1.0-or-later
# html/tab_b.png: GPL-1.0-or-later
# html/tab_h.png: GPL-1.0-or-later
# html/tab_s.png: GPL-1.0-or-later
# html/tabs.css: GPL-1.0-or-later
License:        MIT AND GPL-3.0-or-later WITH Bison-exception-2.2 AND GPL-1.0-or-later
Summary:        API documentation for Z3
# FIXME: this should be noarch, but we end up with different numbers of inheritance
# graphs on different architectures.  Why?

%description doc
API documentation for Z3.

%ifarch %{java_arches}
%package -n java-z3
Summary:        Java interface to z3
Requires:       z3-libs%{?_isa} = %{version}-%{release}
Requires:       java
Requires:       javapackages-tools

%description -n java-z3
Java interface to z3.
%endif

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
%ifnarch %{ix86}
%package -n ocaml-z3
Summary:        Ocaml interface to z3
Requires:       z3-libs%{?_isa} = %{version}-%{release}

%description -n ocaml-z3
Ocaml interface to z3.

%package -n ocaml-z3-devel
Summary:        Files for building ocaml applications that use z3
Requires:       ocaml-z3%{?_isa} = %{version}-%{release}
Requires:       ocaml-zarith-devel%{?_isa}

%description -n ocaml-z3-devel
Files for building ocaml applications that use z3.
%endif

%package -n python3-z3
Summary:        Python 3 interface to z3
BuildArch:      noarch
Requires:       z3-libs = %{version}-%{release}

%description -n python3-z3
Python 3 interface to z3.

%prep
%autosetup -N -n %{name}-%{name}-%{version}
%ifnarch %{ocaml_native_compiler}
%patch -P0 -p1
%endif

# Enable verbose builds, use Fedora CFLAGS, preserve timestamps when installing,
# include the entire contents of the archives in the library, link the library
# with the correct flags, and build the ocaml files with debuginfo.
sed \
  -e 's/@$(CXX)/$(CXX)/' \
  -e '/O3/d' \
  -e "s/\(['\"]\)cp\([^[:alnum:]]\)/\1cp -p\2/" \
  -e "s/\(SLIBEXTRAFLAGS = '\)'/\1-Wl,--no-whole-archive'/" \
  -e '/SLIBFLAGS/s|-shared|& %{build_ldflags} -Wl,--whole-archive|' \
  -e 's/\(libz3$(SO_EXT)\)\(\\n\)/\1 -Wl,--no-whole-archive\2/' \
  -e "s/OCAML_FLAGS = ''/OCAML_FLAGS = '-g'/" \
  -i scripts/mk_util.py

# Comply with the Java packaging guidelines and fill in the version for python
majver=$(cut -d. -f-2 <<< %{version})
sed -e '/libz3java/s,\(System\.load\)Library("\(.*\)"),\1("%{_libdir}/z3/\2.so"),' \
    -e "s/'so'/'so.$majver'/" \
    -i scripts/update_api.py

# Turn off HTML timestamps for reproducible builds
sed -i '/HTML_TIMESTAMP/s/YES/NO/' doc/z3api.cfg.in doc/z3code.dox

%build
export PYTHON=%{python3}

%cmake -G Ninja \
  -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir}/z3 \
  -DCMAKE_JAVA_COMPILE_FLAGS="-source;1.8;-target;1.8" \
  -DZ3_BUILD_DOCUMENTATION:BOOL=ON \
%ifarch %{java_arches}
  -DZ3_BUILD_JAVA_BINDINGS:BOOL=ON \
%endif
  -DZ3_BUILD_PYTHON_BINDINGS:BOOL=ON \
  -DZ3_INCLUDE_GIT_HASH:BOOL=OFF \
  -DZ3_INCLUDE_GIT_DESCRIBE:BOOL=OFF \
  -DZ3_USE_LIB_GMP:BOOL=ON

%cmake_build

%ifnarch %{ix86}
# The cmake build system does not build the OCaml interface.  Do that manually.
#
# First, run the configure script to generate several files.
# This is NOT an autoconf-generated configure script.
./configure -p %{_prefix} --gmp --ml

# Second, to prevent make from rebuilding the entire library, copy the
# cmake-built library to where make expects it.
cp -dp %{_vpath_builddir}/libz3.so* build

# Third, make wants to rebuild libz3.so since its dependencies do not exist.
# Do selective Makefile surgery to prevent this.
sed -i '/^api/s/ libz3\$(SO_EXT)//g' build/Makefile

# Fourth, build the OCaml interface
%make_build -C build ml
%endif

%install
# Install the C++, python3, and Java interfaces
%cmake_install

%ifarch %{java_arches}
# Move the Java interface to its correct location
mkdir -p %{buildroot}%{_libdir}/z3
mkdir -p %{buildroot}%{_jnidir}
mv %{buildroot}%{_javadir}/*.jar %{buildroot}%{_jnidir}
ln -s %{_jnidir}/com.microsoft.z3.jar %{buildroot}%{_libdir}/z3
mv %{buildroot}%{_libdir}/libz3java.so %{buildroot}%{_libdir}/z3
%endif

%ifnarch %{ix86}
# Install the OCaml interface
cd build/api/ml
mkdir -p %{buildroot}%{ocamldir}/Z3
%ifarch %{ocaml_native_compiler}
cp -p *.cmx{,a,s} %{buildroot}%{ocamldir}/Z3
%endif
cp -p META *.{a,cma,cmi,mli} %{buildroot}%{ocamldir}/Z3
mkdir -p %{buildroot}%{ocamldir}/stublibs
cp -p *.so %{buildroot}%{ocamldir}/stublibs
cd -
%endif

# We handle the documentation files below
rm -rf %{buildroot}%{_docdir}/Z3

# Make a man page
mkdir -p %{buildroot}%{_mandir}/man1
help2man -N -o %{buildroot}%{_mandir}/man1/z3.1 \
  -n 'Satisfiability Modulo Theories (SMT) solver' %{_vpath_builddir}/z3

# Fix the pkgconfig file
sed -i 's,//usr,,' %{buildroot}%{_libdir}/pkgconfig/z3.pc

%if %{with test}
%check
cd build
make test-z3
./test-z3 /a
cd -
%endif

%files
%doc README.md RELEASE_NOTES.md
%{_bindir}/z3
%{_mandir}/man1/z3.1*

%files libs
%license LICENSE.txt
%{_libdir}/libz3.so.4.13*

%files devel
%{_includedir}/z3/
%{_libdir}/libz3.so
%{_libdir}/cmake/z3/
%{_libdir}/pkgconfig/z3.pc

%files doc
%doc %{_vpath_builddir}/doc/api/html examples
%license LICENSE.txt

%ifarch %{java_arches}
%files -n java-z3
%{_libdir}/z3/
%{_jnidir}/com.microsoft.z3*jar
%endif

%ifnarch %{ix86}
%files -n ocaml-z3
%dir %{ocamldir}/Z3/
%{ocamldir}/Z3/META
%{ocamldir}/Z3/*.cma
%{ocamldir}/Z3/*.cmi
%ifarch %{ocaml_native_compiler}
%{ocamldir}/Z3/*.cmxs
%endif
%{ocamldir}/stublibs/*.so

%files -n ocaml-z3-devel
%{ocamldir}/Z3/*.a
%ifarch %{ocaml_native_compiler}
%{ocamldir}/Z3/*.cmx
%{ocamldir}/Z3/*.cmxa
%endif
%{ocamldir}/Z3/*.mli
%endif

%files -n python3-z3
%{python3_sitelib}/z3/

%changelog
* Fri Feb 21 2025 Mayank Singh <mayansingh@microsoft.com> - 4.13.3-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Fri Oct 11 2024 Jerry James <loganjerry@gmail.com> - 4.13.3-1
- Version 4.13.3

* Fri Sep 27 2024 Jerry James <loganjerry@gmail.com> - 4.13.2-1
- Version 4.13.2

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Jerry James <loganjerry@gmail.com> - 4.13.0-5
- Rebuild for ocaml-zarith 1.14

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 4.13.0-4
- OCaml 5.2.0 ppc64le fix

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.13.0-3
- Rebuilt for Python 3.13

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 4.13.0-2
- OCaml 5.2.0 for Fedora 41

* Thu Mar 14 2024 Jerry James <loganjerry@gmail.com> - 4.13.0-1
- Version 4.13.0

* Sun Feb 25 2024 Jerry James <loganjerry@gmail.com> - 4.12.6-1
- Version 4.12.6

* Sat Jan 27 2024 Jerry James <loganjerry@gmail.com> - 4.12.5-1
- Version 4.12.5

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 21 2023 Jerry James <loganjerry@gmail.com> - 4.12.4-4
- Fix python package library load name (bz 2255464)

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 4.12.4-3
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 4.12.4-2
- OCaml 5.1.1 rebuild for Fedora 40

* Sat Dec  9 2023 Jerry James <loganjerry@gmail.com> - 4.12.4-1
- Version 4.12.4
- Drop upstreamed patches: python, stdint, escapes

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 4.12.2-7
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 27 2023 Jerry James <loganjerry@gmail.com> - 4.12.2-6
- Rebuild for ocaml-zarith 1.13

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 21 2023 Jerry James <loganjerry@gmail.com> - 4.12.2-4
- Exclude the OCaml and Java subpackages only on i386

* Wed Jul 12 2023 Richard W.M. Jones <rjones@redhat.com> - 4.12.2-4
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 4.12.2-3
- OCaml 5.0.0 rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 4.12.2-2
- Rebuilt for Python 3.12

* Mon May 15 2023 Jerry James <loganjerry@gmail.com> - 4.12.2-1
- Version 4.12.2

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 4.12.1-2
- Rebuild OCaml packages for F38

* Sat Jan 21 2023 Jerry James <loganjerry@gmail.com> - 4.12.1-1
- Version 4.12.1

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Jerry James <loganjerry@gmail.com> - 4.12.0-1
- Version 4.12.0
- Drop upstreamed -data-race and -uninit patches

* Sun Jan  8 2023 Jerry James <loganjerry@gmail.com> - 4.11.2-2
- Add -data-race patch to fix segfault (bz 2157972)
- Add -uninit patch to fix use of an uninitialized value

* Wed Dec 14 2022 Jerry James <loganjerry@gmail.com> - 4.11.2-1
- Further clarify license of the doc subpackage (SPDX)

* Sun Sep  4 2022 Jerry James <loganjerry@gmail.com> - 4.11.2-1
- Version 4.11.2

* Fri Aug 19 2022 Jerry James <loganjerry@gmail.com> - 4.11.0-1
- Version 4.11.0
- Clarify license of the doc subpackage

* Mon Aug  8 2022 Jerry James <loganjerry@gmail.com> - 4.10.2-1
- Version 4.10.2

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Jerry James <loganjerry@gmail.com> - 4.8.17-5
- Do not support Java on i686 (rhbz#2104112)
- Use new OCaml macros

* Mon Jun 20 2022 Python Maint <python-maint@redhat.com> - 4.8.17-4
- Rebuilt for Python 3.11

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 4.8.17-3
- OCaml 4.14.0 rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.8.17-2
- Rebuilt for Python 3.11

* Mon May 16 2022 Jerry James <loganjerry@gmail.com> - 4.8.17-1
- Version 4.8.17
- Drop upstreamed -ambiguous-overload patch

* Thu Mar 24 2022 Jerry James <loganjerry@gmail.com> - 4.8.15-2
- Add -ambiguous-overload patch to fix cppcheck build failure

* Mon Mar 21 2022 Jerry James <loganjerry@gmail.com> - 4.8.15-1
- Version 4.8.15

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 4.8.14-4
- Rebuilt for java-17-openjdk as system jdk

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 4.8.14-3
- OCaml 4.13.1 rebuild to remove package notes

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 24 2021 Jerry James <loganjerry@gmail.com> - 4.8.14-1
- Version 4.8.14
- Conditionalize the %%check script

* Fri Nov 19 2021 Jerry James <loganjerry@gmail.com> - 4.8.13-1
- Version 4.8.13

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 4.8.12-3
- OCaml 4.13.1 build

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Jerry James <loganjerry@gmail.com> - 4.8.12-1
- Version 4.8.12

* Sun Jun  6 2021 Jerry James <loganjerry@gmail.com> - 4.8.11-1
- Version 4.8.11

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.8.10-6
- Rebuilt for Python 3.10

* Wed Mar  3 2021 Jerry James <loganjerry@gmail.com> - 4.8.10-5
- Rebuild for ocaml-zarith 1.12

* Mon Mar  1 20:17:48 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 4.8.10-4
- Bump release and rebuild.

* Mon Mar  1 19:41:16 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 4.8.10-3
- Bump release and rebuild.

* Mon Mar  1 16:57:45 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 4.8.10-2
- OCaml 4.12.0 build

* Sat Feb 13 2021 Jerry James <loganjerry@gmail.com> - 4.8.10-1
- Version 4.8.10

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 25 2020 Jerry James <loganjerry@gmail.com> - 4.8.9-4
- Fix the python interface (bz 1910923)

* Mon Nov 16 2020 Jerry James <loganjerry@gmail.com> - 4.8.9-3
- Rebuild for ocaml-zarith 1.11

* Fri Sep 25 2020 Jerry James <loganjerry@gmail.com> - 4.8.9-2
- Rebuild for ocaml-zarith 1.10

* Fri Sep 11 2020 Jerry James <loganjerry@gmail.com> - 4.8.9-1
- Version 4.8.9

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 4.8.8-7
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 4.8.8-6
- OCaml 4.11.0 rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Jerry James <loganjerry@gmail.com> - 4.8.8-4
- Build with cmake
- Manually build the OCaml interface
- Limit the class file version in the Java interface
- Allow the library to hide internal symbols; this means that the binary can no
  longer be linked with the library, so the main package does not depend on
  the -libs package
- The python package no longer contains an ELF object, so make it noarch

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 4.8.8-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.8.8-3
- Rebuilt for Python 3.9

* Thu May 14 2020 Wolfgang Stöggl <c72578@yahoo.de> - 4.8.8-2
- Add Z3 cmake files required by find_package(Z3)

* Sat May  9 2020 Jerry James <loganjerry@gmail.com> - 4.8.8-1
- Version 4.8.8
- Drop all patches; all have been upstreamed

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 4.8.7-10
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 4.8.7-9
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 4.8.7-8
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 4.8.7-7
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 4.8.7-6
- OCaml 4.10.0 final.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Jerry James <loganjerry@gmail.com> - 4.8.7-4
- Make -doc be archful (bz 1792740)
- Add -signed-char and -gcc-10-s390x patches

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 4.8.7-4
- OCaml 4.10.0+beta1 rebuild.

* Fri Jan 10 2020 Richard W.M. Jones <rjones@redhat.com> - 4.8.7-3
- OCaml 4.09.0 for riscv64

* Sat Dec  7 2019 Jerry James <loganjerry@gmail.com> - 4.8.7-2
- OCaml 4.09.0 (final) rebuild

* Thu Nov 21 2019 Jerry James <loganjerry@gmail.com> - 4.8.7-1
- New upstream version
- Add -ocamldoc patch to fix documentation build failure
- Add -trailing-zeros32 patch to fix build failures on some platforms

* Fri Sep 20 2019 Jerry James <loganjerry@gmail.com> - 4.8.6-1
- New upstream version

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.8.5-6
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 4.8.5-5
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 4.8.5-4
- OCaml 4.08.1 (rc2) rebuild.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 4.8.5-2
- OCaml 4.08.0 (final) rebuild.

* Sat Jun 22 2019 Jerry James <loganjerry@gmail.com> - 4.8.5-1
- New upstream version

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 4.8.4-3
- OCaml 4.08.0 (beta 3) rebuild.

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 24 2018 Jerry James <loganjerry@gmail.com> - 4.8.4-1
- New upstream version
- Drop -no-sse patch, now handled upstream

* Wed Nov 28 2018 Jerry James <loganjerry@gmail.com> - 4.8.3-1
- New upstream version

* Tue Oct 30 2018 Jerry James <loganjerry@gmail.com> - 4.8.1-1
- New upstream version
- Drop python2 subpackage (bz 1634981)

* Fri Sep  7 2018 Jerry James <loganjerry@gmail.com> - 4.7.1-5
- Build with SSE2 support on 32-bit x86

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 4.7.1-4
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 4.7.1-3
- OCaml 4.07.0-rc1 rebuild.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.7.1-2
- Rebuilt for Python 3.7

* Tue May 22 2018 Jerry James <loganjerry@gmail.com> - 4.7.1-1
- New upstream version (bz 1581516)
- Drop upstreamed -vector patch

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 24 2017 Jerry James <loganjerry@gmail.com> - 4.6.0-1
- New upstream version (bz 1527531)
- Add a python3 subpackage

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.5.0-8
- Python 2 binary package renamed to python2-z3
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Fri Nov 17 2017 Richard W.M. Jones <rjones@redhat.com> - 4.5.0-7
- OCaml 4.06.0 rebuild.
- Add dependency on ocaml-num.

* Tue Aug 08 2017 Richard W.M. Jones <rjones@redhat.com> - 4.5.0-6
- OCaml 4.05.0 rebuild.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Richard W.M. Jones <rjones@redhat.com> - 4.5.0-4
- OCaml 4.04.2 rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 4.5.0-3
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov  8 2016 Jerry James <loganjerry@gmail.com> - 4.5.0-1
- New upstream version
- All patches except -sse2 have been upstreamed; drop them
- Upstream now ships __init__.py; drop our version
- Drop all the buildroot tricks; Makefile supports DESTDIR now
- Use C.UTF-8 instead of en_US.UTF-8

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 4.4.1-8
- Rebuild for OCaml 4.04.0.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 13 2016 Jerry James <loganjerry@gmail.com> - 4.4.1-6
- Fix Java interface (bz 1353773)

* Thu Jun 30 2016 Jerry James <loganjerry@gmail.com> - 4.4.1-5
- Fix __init__.py (bz 1351580)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Feb 02 2016 Jonathan Wakely <jwakely@redhat.com> - 4.4.1-3
- Patched for C++11 compatibility.

* Wed Jan 20 2016 Jerry James <loganjerry@gmail.com> - 4.4.1-2
- Add __init__.py to the python interface (bz 1298429)

* Thu Oct  8 2015 Jerry James <loganjerry@gmail.com> - 4.4.1-1
- New upstream version

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-4
- OCaml 4.02.3 rebuild.

* Thu Jun 25 2015 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-3
- ocaml-4.02.2 final rebuild.

* Thu Jun 18 2015 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-2
- ocaml-4.02.2 rebuild.

* Wed May 27 2015 Jerry James <loganjerry@gmail.com> - 4.4.0-1
- New upstream version

* Wed Apr 22 2015 Jerry James <loganjerry@gmail.com> - 4.3.2-3.20150329git.29606b5
- Fix issues found on review (bz 1206826)

* Mon Mar 30 2015 Jerry James <loganjerry@gmail.com> - 4.3.2-2.20150329git.29606b5
- Update to latest git HEAD
- Include examples in -doc

* Sat Mar 28 2015 Jerry James <loganjerry@gmail.com> - 4.3.2-1.20150327git.ac21ffe
- Initial RPM
