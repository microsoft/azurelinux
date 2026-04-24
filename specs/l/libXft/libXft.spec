# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: X.Org X11 libXft runtime library
Name: libXft
Version: 2.3.8
Release: 10%{?dist}
License: HPND-sell-variant
URL: http://www.x.org

Source0: https://www.x.org/pub/individual/lib/%{name}-%{version}.tar.xz

# Bug report: https://bugzilla.redhat.com/show_bug.cgi?id=2154735
# Upstream issue: https://gitlab.freedesktop.org/xorg/lib/libxft/-/issues/19
# Upstream fix: https://gitlab.freedesktop.org/xorg/lib/libxft/-/merge_requests/26
Patch:   fix_font_loading.patch

BuildRequires: make
BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool
BuildRequires: pkgconfig(xrender)
BuildRequires: freetype-devel >= 2.1.9-2
BuildRequires: fontconfig-devel >= 2.2-1

Requires: fontconfig >= 2.2-1

%description
X.Org X11 libXft runtime library

%package devel
Summary: X.Org X11 libXft development package
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXft development package

%prep
%autosetup -p1

%build
autoreconf -v --install --force

%configure --disable-static
make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%ldconfig_post
%ldconfig_postun

%files
%doc AUTHORS COPYING README.md ChangeLog
%{_libdir}/libXft.so.2*

%files devel
%dir %{_includedir}/X11/Xft
%{_includedir}/X11/Xft/Xft.h
%{_includedir}/X11/Xft/XftCompat.h
%{_libdir}/libXft.so
%{_libdir}/pkgconfig/xft.pc
%{_mandir}/man3/Xft*.3*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 06 2023 Benjamin Tissoires <benjamin.tissoires@redhat.com> - 2.3.8-4
- SPDX Migration

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 02 2023 Lumír Balhar <lbalhar@redhat.com> - 2.3.8-2
- Fix font loading
Resolves: rhbz#2154735

* Mon Apr 24 2023 Benjamin Tissoires <benjamin.tissoires@redhat.com> - 2.3.8-1
- libXft 2.3.8-1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 04 2022 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.3.6-1
- libXft 2.3.6-1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 21 2021 Benjamin Tissoires <benjamin.tissoires@redhat.com> - 2.3.4-1
- libXft 2.3.4

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov  5 11:25:22 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.3-5
- Add BuildRequires for make

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 20 2019 Adam Jackson <ajax@redhat.com> - 2.3.3-1
- libXft 2.3.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Adam Jackson <ajax@redhat.com> - 2.3.2-10
- Drop useless %%defattr

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 2.3.2-9
- Use ldconfig scriptlet macros

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.3.2-1
- libXft 2.3.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 12 2014 Dennis Gilmore <dennis @ausil.us> - 2.3.1-6
- add patch to fix FTBFS due to freetype changes

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.1-4
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.3.1-1
- libXft 2.3.1

* Mon Mar 12 2012 Adam Jackson <ajax@redhat.com> 2.3.0-2
- libXft-2.3.0-bold-fix.patch: Fix bold fonts.

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 2.3.0-1
- libXft 2.3.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adam Jackson <ajax@redhat.com> 2.2.0-1
- libXft 2.2.0

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 2.1.14-1
- libXft 2.1.14

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 2.1.13-3
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 04 2008 Adam Jackson <ajax@redhat.com> 2.1.13-1
- libXft 2.1.13

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.12-5
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 parag <paragn@fedoraproject.org> - 2.1.12-4
- Merge-Review #226074
- Removed XFree86-libs, xorg-x11-libs XFree86-devel, xorg-x11-devel as Obsoletes
- Removed BR:pkgconfig
- Removed zero-length NEWS file

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 2.1.12-3
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 2.1.12-2
- Don't install INSTALL

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 2.1.12-1.fc7
- Update to 2.1.12

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 2.1.10
- Updated libXft to version 2.1.10
- Specify freetype dependencies as >= 2.1.9-1
- Futureproof builds by adding release number to fontconfig dependencies.

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 2.1.8.2-4
- Replace "makeinstall" with "make install DESTDIR=..."

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 2.1.8.2-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 2.1.8.2-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Mike A. Harris <mharris@redhat.com> 2.1.8.2-3
- Added missing dependencies to devel subpackage to fix (#176744)

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 2.1.8.2-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 2.1.8.2-1
- Updated libXft to version 2.1.8.2 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 2.1.8.1-1
- Updated libXft to version 2.1.8.1 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.
- Added "Requires: libXrender-devel" to -devel subpackage for (#175465)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 2.1.8-2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 2.1.8-1
- Updated libXft to version 2.1.8 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-5
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro
- Fix BuildRequires to use new style X library package names

* Sun Sep 04 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-4
- Added "BuildRequires: fontconfig-devel >= 2.2" dependency that was
  previously missed.  Also added "Requires: fontconfig >= 2.2" runtime
  dependency.
- Added missing defattr to devel subpackage.

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-3
- Added freetype-devel build dependency.

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-1
- Initial build.
