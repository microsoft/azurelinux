# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global module Cbc

%if 0%{?fedora}
%global blaslib flexiblas
%else
%global blaslib openblas
%endif

Name:		coin-or-%{module}
Summary:	Coin-or branch and cut
Version:	2.10.12
Release: 11%{?dist}

# The project as a whole is licensed EPL-2.0.  However, many source files still
# claim to be licensed EPL-1.0.  This is probably an upstream oversight.
License:	EPL-2.0 AND EPL-1.0
URL:		https://github.com/coin-or/%{module}
VCS:		git:%{url}.git
Source0:	%{url}/archive/releases/%{version}/%{module}-%{version}.tar.gz
BuildRequires:	coin-or-Cgl-doc
BuildRequires:	coin-or-Clp-doc
BuildRequires:	coin-or-DyLP-doc
BuildRequires:	coin-or-Vol-doc
BuildRequires:	doxygen
BuildRequires:	gcc-c++
BuildRequires:	make
BuildRequires:	asl-devel
BuildRequires:	MUMPS-devel
BuildRequires:    %{blaslib}-devel
BuildRequires:	pkgconfig(cgl)
BuildRequires:	pkgconfig(clp)
BuildRequires:	pkgconfig(coindatamiplib3)
BuildRequires:	pkgconfig(coindatanetlib)
BuildRequires:	pkgconfig(dylp)
%ifnarch %{ix86}
%endif
BuildRequires:	pkgconfig(libnauty)
BuildRequires:	pkgconfig(vol)

Requires(post):   %{_sbindir}/alternatives
Requires(preun):  %{_sbindir}/alternatives
Obsoletes:	      coin-or-Cbc < 0:2.10.12-5

# Install documentation in standard rpm directory
Patch0:		%{name}-docdir.patch

# Avoid empty #define if svnversion is available at configure time
Patch1:		%{name}-svnversion.patch

# Do not catch polymorphic exceptions by value
Patch2:		%{name}-exception.patch

# Fix non-C99 code in the configure script
Patch3:		%{name}-configure-c99.patch

# ISO C++17 does not allow 'register' storage class specifier
# https://github.com/coin-or/Cbc/commit/a5b95995f8347e90c72a197224def415e4302d7b
# https://github.com/coin-or/Cbc/commit/583acba8c6052d711f58d51294de61461a5bb3d5
Patch4:		%{name}-register.patch

# One test relies on Clp having been compiled without -DNDEBUG, so that it
# throws an exception.  We compiled with -DNDEBUG, so the test segfaults.
# Skip that test.
Patch5:		%{name}-test.patch

%description
Cbc (Coin-or branch and cut) is an open-source mixed integer programming
solver written in C++. It can be used as a callable library or using a
stand-alone executable. It can be called through AMPL (natively), GAMS
(using the links provided by the "Optimization Services" and "GAMSlinks"
projects), MPL (through the "CoinMP" project), AIMMS (through the "AIMMSlinks"
project), or "PuLP".

Cbc links to a number of other COIN projects for additional functionality,
including:

   * Clp (the default solver for LP relaxations)
   * Cgl (for cut generation)
   * CoinUtils (for reading input files and various utilities)

%package	devel
Summary:	Development files for %{name}
Requires:	coin-or-Cgl-devel%{?_isa}
Requires:	coin-or-Clp-devel%{?_isa}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Documentation files for %{name}
Requires:	coin-or-Cgl-doc
Requires:	coin-or-Clp-doc
Requires:	coin-or-DyLP-doc
Requires:	coin-or-Vol-doc
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
This package contains the documentation for %{name}.

%prep
%autosetup -p1 -n %{module}-releases-%{version}

# The pkgconfig file lists transitive dependencies.  Those are necessary when
# using static libraries, but not with shared libraries.
sed -i 's/ @CBCLIB_PCLIBS@/\nLibs.private:&/' Cbc/cbc.pc.in

%build
export CPPFLAGS='-DNDEBUG'
%configure \
  --enable-cbc-parallel \
  --with-asl-incdir=%{_includedir}/asl \
  --with-asl-lib=-lasl \
  --with-blas-incdir=%{_includedir}/%{blaslib} \
  --with-blas-lib=-l%{blaslib} \
  --with-glpk-incdir=%{_includedir} \
  --with-glpk-lib=-lglpk \
%ifnarch %{ix86}
  \
  \
%endif
  --with-lapack-incdir=%{_includedir}/%{blaslib} \
  --with-lapack-lib=-l%{blaslib} \
  --with-mumps-incdir=%{_includedir}/MUMPS \
  --with-mumps-lib=-ldmumps \
  --with-nauty-incdir=%{_includedir}/nauty \
  --with-nauty-lib=-lnauty

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

%make_build all doxydoc

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_docdir}/%{name}/{LICENSE,cbc_addlibs.txt}
cp -a README.md doxydoc/{html,*.tag} %{buildroot}%{_docdir}/%{name}

# Resolve the conflict of file /usr/bin/cbc
# Set an alternative
touch -c %{buildroot}%{_bindir}/coin.cbc
# Rename duplicated file
mv %{buildroot}%{_bindir}/cbc %{buildroot}%{_bindir}/Cbc

%post
%{_sbindir}/update-alternatives --verbose --install %{_bindir}/coin.cbc CoinCbc %{_bindir}/Cbc 2

%preun
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --verbose --remove-all CoinCbc
fi

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test

%files
%license LICENSE
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/README.md
%ghost %{_bindir}/coin.cbc
%{_bindir}/Cbc
%{_libdir}/libCbc.so.3
%{_libdir}/libCbc.so.3.*
%{_libdir}/libCbcSolver.so.3
%{_libdir}/libCbcSolver.so.3.*
%{_libdir}/libOsiCbc.so.3
%{_libdir}/libOsiCbc.so.3.*

%files		devel
%{_includedir}/coin/*
%{_libdir}/libCbc.so
%{_libdir}/libCbcSolver.so
%{_libdir}/libOsiCbc.so
%{_libdir}/pkgconfig/cbc.pc
%{_libdir}/pkgconfig/osi-cbc.pc

%files		doc
%{_docdir}/%{name}/html
%{_docdir}/%{name}/cbc_doxy.tag

%changelog
* Thu Jan 08 2026 Jerry James <loganjerry@gmail.com> - 2.10.12-10
- Rebuild for nauty 2.9.3

* Wed Sep 17 2025 Jerry James <loganjerry@gmail.com> - 2.10.12-9
- Rebuild for nauty 2.9.1

* Wed Jul 30 2025 Jerry James <loganjerry@gmail.com> - 2.10.12-8
- Rebuild for nauty 2.9.0

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 01 2025 Antonio Trande <sagitter@fedoraproject.org> - 2.10.12-5
- Renaming of /usr/bin/cbc file (rhbz#2335063)

* Wed Jan 01 2025 Antonio Trande <sagitter@fedoraproject.org> - 2.10.12-4
- Resolve the conflict of /usr/bin/cbc (rhbz#2335063)

* Sat Dec 28 2024 Antonio Trande <sagitter@fedoraproject.org> - 2.10.12-3
- Rebuild for MUMPS-5.7.3

* Tue Dec  3 2024 Jerry James <loganjerry@gmail.com> - 2.10.12-2
- Rebuild for asl 20241111

* Mon Sep 23 2024 Jerry James <loganjerry@gmail.com> - 2.10.12-1
- Version 2.10.12

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 19 2024 Jerry James <loganjerry@gmail.com> - 2.10.11-2
- Rebuild for coin-or-HiGHS 1.7.0

* Wed Jan 31 2024 Jerry James <loganjerry@gmail.com> - 2.10.11-1
- Version 2.10.11
- Change License from EPL-1.0 to EPL-2.0 AND EPL-1.0
- Verify that license is valid SPDX
- BR asl-devel instead of mp-devel
- Add coin-or-HiGHS support except on 32-bit x86
- Drop support for Fedora < 33

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 06 2024 Antonio Trande <sagitter@fedoraproject.org> - 2.10.5-14
- Rebuild for MUMPS-5.6.2

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jan 23 2023 Florian Weimer <fweimer@redhat.com> - 2.10.5-12
- Port configure script to C99

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 17 2022 Antonio Trande <sagitter@fedoraproject.org> - 2.10.5-9
- Rebuild for MUMPS-5.5.0

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 2.10.5-6
- Rebuild for MUMPS-5.4.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 27 2020 Iñaki Úcar <iucar@fedoraproject.org> - 2.10.5-4
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun  2 2020 Jerry James <loganjerry@gmail.com> - 2.10.5-2
- Rebuild for nauty 2.7.1

* Wed Mar 11 2020 Jerry James <loganjerry@gmail.com> - 2.10.5-1
- Version 2.10.5

* Thu Feb 20 2020 Jerry James <loganjerry@gmail.com> - 2.10.4-1
- Version 2.10.4
- Drop upstreamed -sizeof patch

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Jerry James <loganjerry@gmail.com> - 2.10.3-1
- Update to latest upstream release (bz 1461035)
- Update project URL
- Change License from EPL to EPL-1.0
- Eliminate unnecessary BRs and Rs
- Add -exception, -overflow, -signed, and -sizeof patches
- Build with asl and nauty support
- Eliminate rpath from the library
- Force libtool to not defeat -Wl,--as-needed
- Be explicit about library versions as required by latest guidelines
- Filter out unnecessary Libs values from pkgconfig files
- Package doxygen tag file to enable cross-linking
- Run tests on ARM again

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 2.9.8-9
- Rebuild with fixed binutils

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Wed Apr  5 2017 Jerry James <loganjerry@gmail.com> - 2.9.8-3
- Rebuild for glpk 4.61

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 15 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.8-1
- Update to latest upstream release (#1312515)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 11 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.7-1
- Update to latest upstream release (#1270499)

* Fri Sep 25 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.6-1
- Update to latest upstream release (#1265641)

* Sat Jun 20 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.5-3
- Full rebuild of coin-or stack.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 12 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.5-1
- Update to latest upstream release (#1227748)

* Sun Apr 12 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.4-1
- Update to latest upstream release (#1201062)

* Sun Mar  1 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.2-5
- Install CbcParam.hpp not CbcParam.cpp.

* Sat Feb 28 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.2-4
- Install header required by coin-or-Dip.

* Sat Feb 21 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.2-3
- Intermediate build disabling %%check for arm only.

* Sat Feb 21 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.2-2
- Rebuild to ensure using latest C++ abi changes.

* Mon Feb  9 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.2-1
- Update to latest upstream release (#1116569).

* Sun Aug 31 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.12-3
- Rebuild to ensure packages are built in proper order.

* Sat Aug 30 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.12-1
- Update to latest upstream release (#1116569#c2).

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.10-1
- Update to latest upstream release (#1116569).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.9-1
- Update to latest upstream release.

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.5-1
- Update to latest upstream release.

* Mon Jan 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.7.7-4
- Update to run make check (#894610#c4).

* Sat Jan 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.7.7-3
- Rename repackaged tarball.

* Sun Nov 18 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.7.7-2
- Rename package to coin-or-Cbc.
- Do not package Thirdy party data or data without clean license.

* Thu Sep 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.7.7-1
- Initial coinor-Cbc spec.
