# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global		module		Cgl

Name:		coin-or-%{module}
Summary:	Cut Generation Library
Version:	0.60.9
Release:	4%{?dist}

# The project as a whole is licensed EPL-2.0.  However, many source files still
# claim to be licensed EPL-1.0.  This is probably an upstream oversight.
License:	EPL-2.0 AND EPL-1.0
URL:		https://github.com/coin-or/%{module}
VCS:		git:%{url}.git
Source0:	%{url}/archive/releases/%{version}/%{module}-%{version}.tar.gz
BuildRequires:	coin-or-CoinUtils-doc
BuildRequires:	doxygen
BuildRequires:	gcc-c++
BuildRequires:	make
BuildRequires:	pkgconfig(clp)
BuildRequires:	pkgconfig(dylp)
BuildRequires:	pkgconfig(vol)

# Install documentation in standard rpm directory
Patch0:		%{name}-docdir.patch

# Fix use of uninitialized variables
Patch1:		%{name}-uninit.patch

# Avoid implicit function declarations in the configure script
Patch2:		%{name}-configure-c99.patch

# Soplex lets a macro named EPS leak into the global namespace
Patch3:		%{name}-undef-EPS.patch

%description
The COIN-OR Cut Generation Library (Cgl) is a collection of cut generators
that can be used with other COIN-OR packages that make use of cuts, such as,
among others, the linear solver Clp or the mixed integer linear programming
solvers Cbc or BCP.

%package	devel
Summary:	Development files for %{name}
Requires:	coin-or-Osi-devel%{?_isa}
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

%build
export CPPFLAGS='-DNDEBUG'
%configure

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
rm -f %{buildroot}%{_docdir}/%{name}/{LICENSE,cgl_addlibs.txt}
cp -a README.md doxydoc/{html,*.tag} %{buildroot}%{_docdir}/%{name}

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test

%files
%license LICENSE
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/README.md
%{_libdir}/libCgl.so.1
%{_libdir}/libCgl.so.1.*

%files		devel
%{_includedir}/coin/*
%{_libdir}/libCgl.so
%{_libdir}/pkgconfig/cgl.pc

%files		doc
%{_docdir}/%{name}/html
%{_docdir}/%{name}/cgl_doxy.tag

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 29 2024 Antonio Trande <sagitter@fedoraproject.org> - 0.60.9-2
- Rebuild for MUMPS-5.7.3

* Mon Sep 23 2024 Jerry James <loganjerry@gmail.com> - 0.60.9-1
- Version 0.60.9

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 31 2024 Jerry James <loganjerry@gmail.com> - 0.60.8-1
- Version 0.60.8
- Change License from EPL-1.0 to EPL-2.0 AND EPL-1.0
- Verify that the license is valid SPDX
- Avoid build failure due to SoPlex macro named EPS
- Build with NDEBUG for efficiency of the generated code

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 25 2022 Florian Weimer <fweimer@redhat.com> - 0.60.3-8
- Port configure script to C99

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Antonio Trande <sagitter@fedoraproject.org> - 0.60.3-4
- Rebuild for MUMPS-5.4.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 21 2020 Jerry James <loganjerry@gmail.com> - 0.60.3-1
- Version 0.60.3

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Jerry James <loganjerry@gmail.com> - 0.60.2-1
- Update to latest upstream release (bz 1461036)
- Update project URL
- Change License from EPL to EPL-1.0
- Eliminate unnecessary BRs and Rs
- Eliminate rpath from the library
- Force libtool to not defeat -Wl,--as-needed
- Be explicit about library versions as required by latest guidelines
- Filter out unnecessary Libs values from pkgconfig files
- Package doxygen tag file to enable cross-linking

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.59.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.59.9-8
- Rebuild with fixed binutils

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.59.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.59.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.59.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.59.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.59.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.59.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Mar 11 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.59.9-1
- Update to latest upstream release (#1308282)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.59.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 25 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.59.7-1
- Update to latest upstream release (#1257927)

* Sat Jun 20 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.59.5-4
- Full rebuild of coin-or stack.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.59.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 12 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.59.5-2
- Rebuild to ensure built after all dependencies available.

* Sun Apr 12 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.59.5-1
- Update to latest upstream release (#1227749)

* Sun Apr 12 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.59.4-1
- Update to latest upstream release (#1201066)

* Sat Feb 21 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.59.1-2
- Rebuild to ensure using latest C++ abi changes.

* Sun Feb  8 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.59.1-1
- Update to latest upstream release (#1159474).

* Sun Aug 31 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.9-2
- Rebuild to ensure packages are built in proper order.

* Sat Aug 30 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.9-1
- Update to latest upstream release (#1133490#c1).

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.7-1
- Update to latest upstream release (#1089922).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan  8 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.5-1
- Update to latest upstream release.
- Remove "missing" patch applied upstream.

* Mon Nov  4 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.2-4
- Correct source url path (#894587#c7).
- Add coin-or-CoinUtils-devel requires to the devel package (#894587#c7).

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.2-3
- Install missing header file required by other coin-or modules.

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.2-2
- Use proper _smp_flags macro (#894586#c6).

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.2-1
- Update to latest upstream release.

* Mon Jan 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.57.4-1
- Update to latest upstream release.

* Sat Jan 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.57.3-3
- Rename repackaged tarball.

* Sun Nov 18 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.57.3-2
- Rename package to coin-or-Cgl.
- Do not package Thirdy party data or data without clean license.

* Thu Sep 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.57.3-1
- Initial coinor-Cgl spec.
