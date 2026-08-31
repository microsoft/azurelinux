# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# NOTE: This library has been deprecated in RHEL and Fedora for some
# time now.  While we have removed the word "deprecated" from the package
# name in modular X, the library does remain deprecated and will be
# removed from a future OS release at some point.  Developers should
# refrain from using this library in new software, and should migrate
# software which currently uses libXp to another printing interface such
# as gnome-print.  We may decide to stop shipping the development headers
# prior to removing libXp from the OS.

Summary: X.Org X11 libXp runtime library
Name: libXp
Version: 1.0.4
Release: 9%{?dist}
License: X11 AND X11-distribute-modifications-variant
URL: http://www.x.org

Source0: https://www.x.org/pub/individual/lib/%{name}-%{version}.tar.xz

BuildRequires: make
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXau-devel
BuildRequires: libtool automake autoconf gettext

Patch0: add-proto-files.patch

%description
X.Org X11 libXp runtime library

%package devel
Summary: X.Org X11 libXp development package
Requires: libXau-devel pkgconfig
Requires: %{name} = %{version}-%{release}

# needed by xp.pc
BuildRequires: xorg-x11-proto-devel

%description devel
X.Org X11 libXp development package

%prep
%setup -q
%patch -P0 -p1 -b .add-proto-files

%build
CPPFLAGS="$CPPFLAGS -I$RPM_BUILD_ROOT%{_includedir}"
export CPPFLAGS

autoreconf -v --install

%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Don't encourage people to use the deprecated Xprint APIs.
rm -rf $RPM_BUILD_ROOT%{_mandir}

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%ldconfig_post
%ldconfig_postun

%files
%doc AUTHORS COPYING ChangeLog
%{_libdir}/libXp.so.6
%{_libdir}/libXp.so.6.2.0

%files devel
%{_includedir}/X11/extensions/Print.h
%{_includedir}/X11/extensions/Printstr.h
%{_libdir}/pkgconfig/printproto.pc
%{_libdir}/libXp.so
%{_libdir}/pkgconfig/xp.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 06 2023 Benjamin Tissoires <benjamin.tissoires@redhat.com> - 1.0.4-4
- SPDX migration

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 04 2022 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.0.4-1
- libXp 1.0.4-1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov  5 12:15:51 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.3-8
- Add BuildRequires for make

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Adam Jackson <ajax@redhat.com> - 1.0.3-3
- Fix a memory leak

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Adam Jackson <ajax@redhat.com> - 1.0.3-1
- libXp 1.0.3

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 1.0.2-11
- Use ldconfig scriptlet macros

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 01 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.0.2-1
- libXp 1.0.2. Drags in a bunch of general cleanup, code changes are quite
  limited and CVE-2013-2062 (#960362)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Adam Jackson <ajax@redhat.com>
- Remove BuildRoot.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.0-14
- Un-require xorg-x11-filesystem

* Thu Feb 26 2009 Adam Jackson <ajax@redhat.com> 1.0.0-13
- Rebuild for new libtool.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0-11
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 parag <paragn@fedoraproject.org> - 1.0.0-10
- Merge-Review #226082
- Removed XFree86-libs, xorg-x11-libs XFree86-devel, xorg-x11-devel as Obsoletes
- Removed xorg-x11-deprecated-libs xorg-x11-deprecated-libs-devel as Obsoletes

* Mon Jan 14 2008 parag <paragn@fedoraproject.org> - 1.0.0-9
- Merge-Review #226082
- Removed BR:pkgconfig
- Removed zero-length README file

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.0-8
- Rebuild for build id

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0-8
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0.7
- Add requires for the devel package on libXau-devel (173530)

* Fri Aug 18 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0-6
- Add the proto files directly instead of attempting to build a separate
  tarball. Also remove last traces of printproto-1.0.3.tar.gz

* Fri Aug 18 2006 Soren Sandmann <sandmann@redhat.com>
- Remove printproto source. 

* Fri Aug 18 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0-6
- BuildRequire autoconf automake libtool gettext

* Fri Aug 18 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0-6
- Run autoreconf to make sure changes to configure.ac take effect

* Fri Aug 18 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0-6
- Add patch to not check for printproto.pc. (Since it's part of this
  package now, it isn't installed at the time libXp is configured).

* Thu Aug 17 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0-5
- Moved Print.h, Printstr.h and printproto.pc into the devel package here
  (they used to be in xorg-x11-proto-devel). 

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Mon Jul 10 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-4
- Renamed libXp_deprecated rpm macro to "with_devel" to avoid confusion.  This
  library is still deprecated, we just decided to remove the word "deprecated"
  from the package name for library naming consistency.

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-3
- Replace "makeinstall" with "make install DESTDIR=..."
- Added "Requires: xorg-x11-proto-devel" to devel for xp.pc
- Remove package ownership of mandir/libdir/etc.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libXp to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXp to version 0.99.2 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-3
- Added "Obsoletes: xorg-x11-deprecated-libs" to runtime package, and
  "Obsoletes: xorg-x11-deprecated-libs-devel" to devel package.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libXp to version 0.99.1 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
