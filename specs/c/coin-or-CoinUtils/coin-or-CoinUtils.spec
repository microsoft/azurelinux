# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global		module		CoinUtils

%if 0%{?fedora}
%global blaslib flexiblas
%else
%global blaslib openblas
%endif

Name:		coin-or-%{module}
Summary:	Coin-or Utilities
Version:	2.11.12
Release:	3%{?dist}

# The project as a whole is licensed EPL-2.0.  However, many source files still
# claim to be licensed EPL-1.0.  This is probably an upstream oversight.
License:	EPL-2.0 AND EPL-1.0
URL:		https://github.com/coin-or/%{module}
VCS:		git:%{url}.git
Source0:	%{url}/archive/releases/%{version}/%{module}-%{version}.tar.gz

BuildRequires:	doxygen
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	gcc-gfortran
BuildRequires:	glpk-devel
BuildRequires:	make
BuildRequires:	%{blaslib}-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(coindatanetlib)
BuildRequires:	pkgconfig(coindatasample)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(zlib)

# Install documentation in standard rpm directory
Patch0:		%{name}-docdir.patch
# Fix invalid C constructs in the configure script
Patch1:		%{name}-configure-c99.patch

%description
CoinUtils (Coin-or Utilities) is an open-source collection of classes
and functions that are generally useful to more than one COIN-OR project.
These utilities include:

  * Vector classes
  * Matrix classes
  * MPS file reading
  * Comparing floating point numbers with a tolerance

%package	devel
Summary:	Development files for %{name}
Requires:	coin-or-Sample
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Documentation files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	doc
This package contains the documentation for %{name}.

%prep
%autosetup -p1 -n %{module}-releases-%{version}

# The pkgconfig file lists transitive dependencies.  Those are necessary when
# using static libraries, but not with shared libraries.
sed -i 's/ @COINUTILSLIB_PCLIBS@/\nLibs.private:&/' CoinUtils/coinutils.pc.in

%build
%configure \
  --enable-coinutils-threads \
  --enable-gnu-packages \
  --with-blas-incdir=%{_includedir}/%{blaslib} \
  --with-blas-lib=-l%{blaslib} \
  --with-glpk-incdir=%{_includedir} \
  --with-glpk-lib=-lglpk \
  --with-lapack-incdir=%{_includedir}/%{blaslib} \
  --with-lapack-lib=-l%{blaslib}

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

%make_build all doxydoc

%install
%make_install
rm %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_docdir}/%{name}/{LICENSE,coinutils_addlibs.txt}
cp -a doxydoc/{html,*.tag} %{buildroot}%{_docdir}/%{name}

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test

%files
%{_pkgdocdir}/
%exclude %{_pkgdocdir}/html
%exclude %{_pkgdocdir}/coinutils_doxy.tag
%license LICENSE
%{_libdir}/libCoinUtils.so.3
%{_libdir}/libCoinUtils.so.3.*

%files devel
%{_includedir}/coin
%{_libdir}/libCoinUtils.so
%{_libdir}/pkgconfig/coinutils.pc

%files doc
%{_pkgdocdir}/html/
%{_pkgdocdir}/coinutils_doxy.tag

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 23 2024 Jerry James <loganjerry@gmail.com> - 2.11.12-1
- Version 2.11.12

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Jerry James <loganjerry@gmail.com> - 2.11.11-1
- Version 2.11.11
- Drop upstreamed register patch

* Mon Jan 29 2024 Jerry James <loganjerry@gmail.com> - 2.11.10-1
- Version 2.11.10
- Convert License tag to SPDX
- Drop unneeded status patch
- Drop support for Fedora < 33
- Build with threading support

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Florian Weimer <fweimer@redhat.com> - 2.11.4-8
- Port configure script to C99

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 10 2020 Iñaki Úcar <iucar@fedoraproject.org> - 2.11.4-3
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 21 2020 Jerry James <loganjerry@gmail.com> - 2.11.4-1
- Release 2.11.4
- Drop unnecessary -underlink patch

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
- Make doc package arch-dependent

* Fri Aug 16 2019 Jerry James <loganjerry@gmail.com> - 2.11.3-2
- Fix the pkgconfig file again

* Fri Aug 16 2019 Jerry James <loganjerry@gmail.com> - 2.11.3-1
- Release 2.11.3

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Jerry James <loganjerry@gmail.com> - 2.11.2-2
- Update project URL
- Eliminate unnecessary BRs and Rs
- Add -status patch to fix a segfault
- Build with openblas and glpk support
- Eliminate rpath from the library
- Force libtool to not defeat -Wl,--as-needed
- Be explicit about library versions as required by latest guidelines
- Filter out unnecessary Libs values from pkgconfig files
- Package doxygen tag file to enable cross-linking

* Mon Apr 22 2019 Antonio Trande <sagitter@fedoraproject.org> - 2.11.2-1
- Release 2.11.2
- Avoid mixed use of %%doc and %%_pkgdocdir
- Exclude installation of coin/DATA directory

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 01 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.10.14-2
- Fix dependence of packages

* Thu Nov 01 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.10.14-1
- Release 2.10.14

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 22 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.10.13-8
- Add gcc gcc-c++ BR

* Fri Feb 16 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.10.13-7
- Use %%ldconfig_scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Mar 11 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.10.13-1
- Update to latest upstream release (#1301938)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 11 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.10.11-1
- Update to latest upstream release (#1270498)

* Fri Sep 25 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.10.10-1
- Update to latest upstream release (#1257924)

* Sat Jun 20 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.10.8-3
- Full rebuild or coin-or stack.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.10.8-1
- Update to latest upstream release

* Sun Apr 12 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.10.7-1
- Update to latest upstream release

* Thu Apr 09 2015 David Tardon <dtardon@redhat.com> - 2.10.3-4
- ensure all -devel deps are installed

* Sat Feb 21 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.10.3-3
- Rebuild to ensure using latest C++ abi changes.

* Sat Feb 14 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.10.3-2
- Rebuild.

* Mon Feb  9 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.10.3-1
- Update to latest upstream release.

* Sun Feb 08 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.10.2-1
- Update to latest upstream release (#1157434).

* Sat Aug 30 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.15-1
- Update to latest upstream release (#1089925#c2).

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.12-1
- Update to latest upstream release (#1089925).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 16 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.7-3
- Correct build with -Werror=format-security (#1037021)

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.7-2
- Use proper _smp_flags macro (#894586#c6).
- Make package owner of /usr/include/coin (#894586#c6)

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.7-1
- Update to latest upstream release.

* Wed Aug  7 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.0-3
- Switch to unversioned docdir (#993706)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.0-1
- Update to latest upstream release.
- Switch to the new upstream tarballs without bundled dependencies.
- Split documentation in a new subpackage (#894585#3)
- Correct undefined non weak symbols (#894585#3)
- Removed unneeded atlas, blas, glpk and lapack build requires (#894585#3)

* Mon Jan 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.8-1
- Add coin-or-Sample to build requires (#894610#c4).
- Update to latest upstream release.

* Sat Jan 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.7-3
- Rename repackaged tarball.

* Sun Nov 18 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.7-2
- Rename package to coin-or-CoinUtils
- Do not package Thirdy party data or data without clean license.

* Wed Sep 26 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.7-1
- Initial coinor-CoinUtils spec.
