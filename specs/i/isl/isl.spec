# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Integer point manipulation library
Name: isl
Version: 0.16.1
License: MIT
URL: http://isl.gforge.inria.fr/

%global libmajor 15
%global libversion %{libmajor}.1.1

%global oldversion 0.14
%global oldlibmajor 13
%global oldlibversion %{oldlibmajor}.1.0

# Please set buildid below when building a private version of this rpm to
# differentiate it from the stock rpm.
#
# % global buildid .local

Release: 24%{?buildid}%{?dist}

BuildRequires:  gcc
BuildRequires: gmp-devel
BuildRequires: pkgconfig
BuildRequires: make
Provides: isl = %{oldversion}

Source0: http://isl.gforge.inria.fr/isl-%{version}.tar.xz

# Current gcc requires exactly 0.14
Source1: http://isl.gforge.inria.fr/isl-%{oldversion}.tar.xz

%description
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints.  Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.  It also includes an ILP solver based on generalized
basis reduction, transitive closures on maps (which may encode infinite
graphs), dependence analysis and bounds on piecewise step-polynomials.

%package devel
Summary: Development for building integer point manipulation library
Requires: isl%{?_isa} == %{version}-%{release}
Requires: gmp-devel%{?_isa}

%description devel
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints.  Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.  It also includes an ILP solver based on generalized
basis reduction, transitive closures on maps (which may encode infinite
graphs), dependence analysis and bounds on piecewise step-polynomials.

%prep
%global docdir isl-%{version}
%setup -a 1 -q -n isl -c

%build
cd isl-%{oldversion}
%configure
%make_build
cd ..

cd isl-%{version}
%configure
%make_build

%install
cd isl-%{oldversion}
%make_install install-libLTLIBRARIES
cd ..

cd isl-%{version}
%make_install
rm -f %{buildroot}/%{_libdir}/libisl.a
rm -f %{buildroot}/%{_libdir}/libisl.la
mkdir -p %{buildroot}/%{_datadir}
%global gdbprettydir %{_datadir}/gdb/auto-load/%{_libdir}
mkdir -p %{buildroot}/%{gdbprettydir}
mv %{buildroot}/%{_libdir}/*-gdb.py* %{buildroot}/%{gdbprettydir}

%check
cd isl-%{oldversion}
#make check
cd ..

cd isl-%{version}
#make check

%ldconfig_scriptlets

%files
%{_libdir}/libisl.so.%{libmajor}
%{_libdir}/libisl.so.%{libversion}
%{_libdir}/libisl.so.%{oldlibmajor}
%{_libdir}/libisl.so.%{oldlibversion}
%{gdbprettydir}/*
%license %{docdir}/LICENSE
%doc %{docdir}/AUTHORS %{docdir}/ChangeLog %{docdir}/README

%files devel
%{_includedir}/*
%{_libdir}/libisl.so
%{_libdir}/pkgconfig/isl.pc
%doc %{docdir}/doc/manual.pdf


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Tom Stellard <tstellar@redhat.com> - 0.16.1-11
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.16.1-6
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 15 2017 Troy Dawson <tdawson@redhat.com> - 0.16.1-4
- Fix %%setup options

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 02 2017 David Howells <dhowells@redhat.com> - 0.16.1-1
- Move to version 0.16.1.
- Build and install just the libraries from 0.14 so that gcc can work.

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 0.14-6
- Add missing %%license macro (#1418512)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 5 2015 David Howells <dhowells@redhat.com> - 0.14-3
- Initial packaging.
