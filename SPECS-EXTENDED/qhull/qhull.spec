Summary: General dimension convex hull programs
Name: qhull
Version: 7.2.1
Release: 5%{?dist}
License: Qhull
Source0: https://github.com/qhull/qhull/archive/v%{version}.tar.gz#/qhull-%{version}.tar.gz

Patch1: 0001-Link-executables-against-shared-libs.patch
Patch2: 0002-Install-docs-into-subdirs.patch

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://www.qhull.org

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: chrpath

%description
Qhull is a general dimension convex hull program that reads a set
of points from stdin, and outputs the smallest convex set that contains
the points to stdout.  It also generates Delaunay triangulations, Voronoi
diagrams, furthest-site Voronoi diagrams, and halfspace intersections
about a point.

%package -n libqhull
Summary: -n libqhull

%description -n libqhull
%{summary}

%package -n libqhull_r
Summary: libqhull_r

%description -n libqhull_r
%{summary}

%package -n libqhull_p
Summary: libqhull_p

%description -n libqhull_p
%{summary}

%package devel
Summary: Development files for qhull
Requires: lib%{name}%{?_isa} = %{version}-%{release}
Requires: lib%{name}_r%{?_isa} = %{version}-%{release}
Requires: lib%{name}_p%{?_isa} = %{version}-%{release}

%description devel
Qhull is a general dimension convex hull program that reads a set
of points from stdin, and outputs the smallest convex set that contains
the points to stdout.  It also generates Delaunay triangulations, Voronoi
diagrams, furthest-site Voronoi diagrams, and halfspace intersections
about a point.

%prep
%setup -q
%patch 1 -p1
%patch 2 -p1

%build
mkdir -p build
cd build
%cmake ..
make VERBOSE=1 %{?_smp_mflags}
cd ..

%install
cd build
make VERBOSE=1 DESTDIR=$RPM_BUILD_ROOT install
cd ..

chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.*


%files
%{_pkgdocdir}
%exclude %{_pkgdocdir}/COPYING.txt
%exclude %{_pkgdocdir}/src/libqhull
%exclude %{_pkgdocdir}/src/libqhull_r
%license COPYING.txt
%{_bindir}/*
%{_mandir}/man1/*

%files -n libqhull
%{_libdir}/libqhull.so.*

%ldconfig_scriptlets -n libqhull


%files -n libqhull_r
%{_libdir}/libqhull_r.so.*

%ldconfig_scriptlets -n libqhull_r


%files -n libqhull_p
%{_libdir}/libqhull_p.so.*

%ldconfig_scriptlets -n libqhull_p


%files devel
%{_pkgdocdir}/src/libqhull
%{_pkgdocdir}/src/libqhull_r
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/libqhullcpp.a
%exclude %{_libdir}/libqhullstatic*.a


%changelog
* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 7.2.1-5
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:7.2.1-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 22 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:7.2.1-1
- Update to 7.2.1.
- Rebase patches.
- Add Epoch: due to upstream having changed their version numbering scheme.
- Reflect Source0: having changed.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2015.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2015.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2015.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2015.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2015.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2015.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 29 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2015.2-1
- Update to 2015.2-7.2.0.
- Split out libqhull, libqhull_p, libqhull_r packages.
- drop pkgconfig.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2003.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2003.1-27
- Remove %%defattr.
- Add %%license.
- Move docs into *-devel.
- Cleanup spec.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Jaromir Capik <jcapik@redhat.com> - 2003.1-23
- Fixing format-security flaws (#1037293)

* Tue Aug 06 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2003.1-22
- Reflect docdir changes (RHBZ #993921).
- Fix bogus %%changelog date.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 24 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2003.1-20
- Update config.sub,guess for aarch64 (RHBZ #926411).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 08 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2003.1-17
- Modernize spec.
- Add qhull.pc.
- Misc. 64bit fixes.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 02 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 2003.1-14
- Apply upstream's qh_gethash patch
- Silence %%setup.
- Remove rpath.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2003.1-11
- fix license tag

* Tue Mar 04 2008 Ralf Corsépius <rc040203@freenet.de> - 2003.1-10
- Add qhull-2003.1-alias.patch (BZ 432309)
  Thanks to Orion Poplawski (orion@cora.nwra.com).

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 2003.1-9
- Rebuild for gcc43.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 2003.1-8
- Mass rebuild.

* Wed Jun 20 2007 Ralf Corsépius <rc040203@freenet.de> - 2003.1-7
- Remove *.la.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 2003.1-6
- Mass rebuild.

* Fri Feb 17 2006 Ralf Corsépius <rc040203@freenet.de> - 2003.1-5
- Disable static libs.
- Fixup some broken links in doc.
- Add %%{?dist}.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2003.1-4
- rebuild on all arches

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Aug 08 2004 Ralf Corsepius <ralf[AT]links2linux.de>	- 2003.1-0.fdr.2
- Use default documentation installation scheme.

* Fri Jul 16 2004 Ralf Corsepius <ralf[AT]links2linux.de>	- 2003.1-0.fdr.1
- Initial Fedora RPM.
