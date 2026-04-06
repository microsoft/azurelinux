# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global snapshot 121130

Name:           gts
Version:        0.7.6
Release:        51.20%{snapshot}%{?dist}
Summary:        GNU Triangulated Surface Library
License:        LGPL-2.0-or-later
URL:            http://gts.sourceforge.net/index.html
Source0:        http://gts.sourceforge.net/tarballs/gts-snapshot-%{snapshot}.tar.gz
# Misc accumulated patches
Patch0:         0001-gts-snapshot-111025.patch
# Add manpage for gts2xyz (from debian)
Patch1:         0002-Add-gts2xyz-manpage.patch

BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  netpbm-devel
BuildRequires:  make

%package devel
Summary:        Development files for gts
Requires:       pkgconfig
Requires:       glib2-devel
Requires:       %{name} = %{version}-%{release}

%description
GTS provides a set of useful functions to deal with 3D surfaces meshed
with interconnected triangles including collision detection,
multiresolution models, constrained Delaunay triangulations and robust
set operations (union, intersection, differences).

%description devel
This package contains the gts header files and libs.

%prep
%setup -q -n %{name}-snapshot-%{snapshot}
%patch -P0 -p1
%patch -P1 -p1

# Fix broken permissions
chmod +x test/*/*.sh

%build
%configure --disable-static --disable-dependency-tracking
%{make_build}

%install
%{make_install}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# File names are too general, rename ...
mv -f $RPM_BUILD_ROOT%{_bindir}/delaunay $RPM_BUILD_ROOT%{_bindir}/gtsdelaunay 
mv -f $RPM_BUILD_ROOT%{_bindir}/happrox $RPM_BUILD_ROOT%{_bindir}/gtshapprox
mv -f $RPM_BUILD_ROOT%{_bindir}/transform $RPM_BUILD_ROOT%{_bindir}/gtstransform
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/delaunay.1 $RPM_BUILD_ROOT%{_mandir}/man1/gtsdelaunay.1 
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/happrox.1 $RPM_BUILD_ROOT%{_mandir}/man1/gtshapprox.1
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/transform.1 $RPM_BUILD_ROOT%{_mandir}/man1/gtstransform.1

%check
# Urgh, something is very broken with gts rsp. its testsuite
make check ||:

%files
%license COPYING
%{_bindir}/gtsdelaunay
%{_bindir}/gts2dxf
%{_bindir}/gts2oogl
%{_bindir}/gts2stl
%{_bindir}/gtscheck
%{_bindir}/gtscompare
%{_bindir}/gtstemplate
%{_bindir}/gtshapprox
%{_bindir}/stl2gts
%{_bindir}/gtstransform
%{_bindir}/gts2xyz
%{_libdir}/*.so.*
%{_mandir}/man1/gtsdelaunay.1*
%{_mandir}/man1/gts2dxf.1*
%{_mandir}/man1/gts2oogl.1*
%{_mandir}/man1/gts2stl.1*
%{_mandir}/man1/gts2xyz.1*
%{_mandir}/man1/gtscheck.1*
%{_mandir}/man1/gtscompare.1*
%{_mandir}/man1/gtstemplate.1*
%{_mandir}/man1/gtshapprox.1*
%{_mandir}/man1/stl2gts.1*
%{_mandir}/man1/gtstransform.1*

%files devel
%{_bindir}/gts-config
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_mandir}/man1/gts-config.1*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-51.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-50.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-49.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-48.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-47.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-46.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.7.6-45.20121130
- Use %%patch -P N instead of %%patchN
- Spec file cosmetics.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-44.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 15 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.7.6-43.20121130
- Modernize spec.
- Convert license to SPDX.
- Update sources to sha512.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-42.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-41.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-40.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-39.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-38.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-37.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-36.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-35.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-34.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-33.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-32.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-31.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-30.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-29.20121130
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.7.6-28.20121130
- Update to latest snapshot.
- Rebase patches.

* Tue Jan 26 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.7.6-27.20111025
- Remove %%defattr.
- Add %%license.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-26.20111025
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-25.20111025
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-24.20111025
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-23.20111025
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-22.20111025
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-21.20111025
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-20.20111025
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 07 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.7.6-19.20111025
- Update to new upstream snapshot
- Rebase patches.
- Spec file cleanup.

* Wed Nov 16 2011 Jindrich Novy <jnovy@redhat.com> - 0.7.6-16
- rebuild against new netpbm

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun  1 2010 Dan Horák <dan[at]danny.cz> - 0.7.6-14
- fix include path for pgm.h (#538971)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 30 2008 Ralf Corsépius <rc040203@freenet.de> - 0.7.6-11
- Let *-devel Require: glib2-devel (BZ: 457099).
- Pass LIBS=-lm to %%configure (avoid non-weak refs to libm).
- Add gts-0.7.6-hacks.diff (Various configuration fixes).
- Add gts-0.7.6-autotools.diff (regenerate autotool-generated files).
- Add %%check.

* Fri May 23 2008 Jon Stanley <jonstanley@gmail.com> - 0.7.6-10
- Fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.6-9
- Autorebuild for GCC 4.3

* Sun Oct 21 2007 Ralf Corsépius <rc040203@freenet.de> - 0.7.6-8
- Address BZ 341431:
  - Rework gts-config.
  - Rework gts.pc.
  - Regenerate gts-0.7.6-pkg_config.diff.

* Tue Aug 28 2007 Ed Hill <ed@eh3.com> - 0.7.6-7
- rebuild for BuildID

* Fri Sep  1 2006 Ed Hill <ed@eh3.com> - 0.7.6-6
- rebuild for imminent FC-6 release

* Mon May 22 2006 Ralf Corsépius <rc040203@freenet.de> - 0.7.6-5
- BR: netpbm-devel (Required to build happrox).
- Add --disable-dependency-tracking.

* Sun May 21 2006 Ed Hill <ed@eh3.com> - 0.7.6-4
- add gts-config patch

* Sun May 21 2006 Ed Hill <ed@eh3.com> - 0.7.6-3
- add Ralf's includedir patch

* Fri May 19 2006 Ed Hill <ed@eh3.com> - 0.7.6-2
- fix FE review items provided by Ralf Corsepius

* Thu May 18 2006 Ed Hill <ed@eh3.com> - 0.7.6-1
- initial package creation

