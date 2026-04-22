# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global		module		Osi

Name:		coin-or-%{module}
Summary:	COIN-OR Open Solver Interface Library
Version:	0.108.11
Release: 5%{?dist}

# The project as a whole is licensed EPL-2.0.  However, many source files still
# claim to be licensed EPL-1.0.  This is probably an upstream oversight.
License:	EPL-2.0 AND EPL-1.0
URL:		https://github.com/coin-or/%{module}
VCS:		git:%{url}.git
Source0:	%{url}/archive/releases/%{version}/%{module}-%{version}.tar.gz
# Install documentation in standard rpm directory
Patch0:		%{name}-docdir.patch
# Fix build with glpk > 4.48
Patch1:		%{name}-glpk.patch
# Fix non-C99 constructs in the configure script
Patch2:		%{name}-configure-c99.patch
# Fix build with SoPlex >= 1.7
Patch3:		%{name}-soplex.patch
# Upstream fix for objective offset being ignored when reading a .lp file
# https://github.com/coin-or/Osi/commit/4071468cf9629d39660e49e4a28e1a91fe41018b
Patch4:		%{name}-objective-offset.patch

BuildRequires:	coin-or-CoinUtils-doc
BuildRequires:	coin-or-Data-Netlib
BuildRequires:	doxygen
BuildRequires:	gcc-c++
BuildRequires:	glpk-devel
%ifnarch %{ix86}
BuildRequires:	libsoplex-devel
%endif
BuildRequires:	make
BuildRequires:	pkgconfig(coinutils)

%description
The COIN-OR Open Solver Interface Library is a collection of solver
interfaces (SIs) that provide a common interface --- the OSI API --- for all
the supported solvers.

%package	devel
Summary:	Development files for %{name}
Requires:	coin-or-CoinUtils-devel%{?_isa}
Requires:	glpk-devel%{?_isa}
%ifnarch %{ix86}
Requires:	libsoplex-devel%{?_isa}
%endif
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Documentation files for %{name}
Requires:	coin-or-CoinUtils-doc
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
This package contains the documentation for %{name}.

%prep
%autosetup -p1 -n %{module}-releases-%{version}

# The pkgconfig file lists transitive dependencies.  Those are necessary when
# using static libraries, but not with shared libraries.
sed -i 's/ @OSILIB_PCLIBS@/\nLibs.private:&/' Osi/osi.pc.in

# Change dependencies on zlib to dependencies on zlib-ng
sed -i 's/-lz/-lz-ng/' Osi/src/OsiSpx/Makefile.{am,in}

%build
export CPPFLAGS='-DNDEBUG'
%configure \
%ifnarch %{ix86}
  --with-soplex-incdir=%{_includedir}/soplex --with-soplex-lib=-lsoplex \
%endif
  --with-glpk-incdir=%{_includedir} --with-glpk-lib=-lglpk

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
rm -f %{buildroot}%{_docdir}/%{name}/{LICENSE,osi_addlibs.txt}
cp -a doxydoc/{html,*.tag} README.md Osi/CHANGELOG %{buildroot}%{_docdir}/%{name}

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test

%files
%license LICENSE
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/README.md
%{_libdir}/libOsi.so.1
%{_libdir}/libOsi.so.1.*
%{_libdir}/libOsiCommonTests.so.1
%{_libdir}/libOsiCommonTests.so.1.*
%{_libdir}/libOsiGlpk.so.1
%{_libdir}/libOsiGlpk.so.1.*
%ifnarch %{ix86}
%{_libdir}/libOsiSpx.so.1
%{_libdir}/libOsiSpx.so.1.*
%endif

%files		devel
%{_includedir}/coin/*
%{_libdir}/libOsi.so
%{_libdir}/libOsiCommonTests.so
%{_libdir}/libOsiGlpk.so
%{_libdir}/pkgconfig/osi.pc
%{_libdir}/pkgconfig/osi-glpk.pc
%{_libdir}/pkgconfig/osi-unittests.pc
%ifnarch %{ix86}
%{_libdir}/libOsiSpx.so
%{_libdir}/pkgconfig/osi-soplex.pc
%endif

%files		doc
%{_docdir}/%{name}/CHANGELOG
%{_docdir}/%{name}/html/
%{_docdir}/%{name}/osi_doxy.tag

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec  3 2024 Jerry James <loganjerry@gmail.com> - 0.108.11-2
- Rebuild for soplex 7.1.2

* Mon Sep 23 2024 Jerry James <loganjerry@gmail.com> - 0.108.11-1
- Version 0.108.11

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Jerry James <loganjerry@gmail.com> - 0.108.10-1
- Version 0.108.10
- Drop upstreamed register storage class patch

* Wed Mar 13 2024 Jerry James <loganjerry@gmail.com> - 0.108.9-2
- Rebuild for soplex 7.0.0

* Tue Jan 30 2024 Jerry James <loganjerry@gmail.com> - 0.108.9-1
- Version 0.108.9
- Update the License from EPL-1.0 to EPL-2.0 AND EPL-1.0
- Verify the license is valid SPDX
- Enable the SoPlex interface, except on 32-bit x86
- Define NDEBUG when building to exclude assertions
- Add upstream patch to remove the register storage class specifier
- Add upstream patch to fix reading objective offset from lp files

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 26 2023 Florian Weimer <fweimer@redhat.com> - 0.108.6-8
- Port configure script to C99

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 21 2020 Jerry James <loganjerry@gmail.com> - 0.108.6-1
- Version 0.108.6

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 16 2019 Jerry James <loganjerry@gmail.com> - 0.108.5-1
- Update to latest upstream release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.108.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Jerry James <loganjerry@gmail.com> - 0.108.4-1
- Update to latest upstream release (bz 1461042)
- Update project URL
- Change License from EPL to EPL-1.0
- Eliminate unnecessary BRs and Rs
- Add -glpk patch to fix build with glpk > 4.48
- Eliminate rpath from the library
- Force libtool to not defeat -Wl,--as-needed
- Be explicit about library versions as required by latest guidelines
- Package doxygen tag file to enable cross-linking

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.107.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.107.8-8
- Rebuild with fixed binutils

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.107.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.107.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.107.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.107.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr  5 2017 Jerry James <loganjerry@gmail.com> - 0.107.8-3
- Rebuild for glpk 4.61

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.107.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Mar 11 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.107.8-1
- Update to latest upstream release (#1308287)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.107.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 25 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.107.6-1
- Update to latest upstream release (#1257932)

* Sat Jun 20 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.107.4-3
- Full rebuild or coin-or stack.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.107.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 12 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.107.4-1
- Update to latest upstream release (#1199722)

* Sat Feb 21 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.107.2-3
- Rebuild to ensure using latest C++ abi changes.

* Sat Feb 14 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.107.2-2
- Rebuild.

* Mon Feb  9 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.107.2-1
- Update to latest upstream release (#1190730).

* Mon Feb  9 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.107.0-3
- Rebuild with latest bugfixes release coin-or-CoinUtils-2.10.3

* Sun Feb 08 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.107.0-2
- Rebuild with updated coin-or-CoinUtils.

* Sat Feb 07 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.107.0-1
- Update to latest upstream release (#1159476).

* Sun Aug 31 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.106.9-2
- Rebuild to ensure packages are built in proper order.

* Sat Aug 30 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.106.9-1
- Update to latest upstream release (#1133197#c3).

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.106.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.106.7-1
- Update to latest upstream release (#1089928).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.106.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.106.2-3
- Use proper _smp_flags macro (#894586#c6).

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.106.2-2
- Correct missing bzip2 build requires (#894586#c4).
- Use unversioned docdir (#894586#c4).

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.106.2-1
- Update to latest upstream release.

* Wed May 8 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.105.7-2
- Split documentation in a new subpackage.
- Switch to the new upstream tarballs without bundled dependencies.

* Mon Jan 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.105.7-1
- Update to latest upstream release.

* Sat Jan 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.105.5-3
- Rename repackaged tarball.

* Sun Nov 18 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.105.5-2
- Rename package to coin-or-Osi.
- Do not package Thirdy party data or data without clean license.

* Wed Sep 26 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.105.5-1
- Initial coinor-Osi spec.
