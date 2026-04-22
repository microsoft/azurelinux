# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

# NOTE: This package contains only C source and header files and pkg-config
# *.pc files, and does not contain any ELF binaries or DSOs, so we disable
# debuginfo generation.
%global debug_package %{nil}

Summary: X.Org X11 developmental X transport library
Name: xorg-x11-xtrans-devel
Version: 1.5.2
Release: 4%{?dist}
License: HPND AND HPND-sell-variant AND MIT AND MIT-open-group AND X11
URL: http://www.x.org
BuildArch: noarch

Source0: https://xorg.freedesktop.org/archive/individual/lib/xtrans-%{version}.tar.gz

# Fedora specific patch
Patch1: xtrans-1.0.3-avoid-gethostname.patch

BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros

%description
X.Org X11 developmental X transport library

%prep
%setup -q -n xtrans-%{version}
%patch -P1 -p1 -b .my-name-is-unix

%build
# yes, this looks horrible, but it's to get the .pc file in datadir
%configure --libdir=%{_datadir} --disable-docs
# Running 'make' not needed.

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%files
%doc AUTHORS COPYING ChangeLog README.md
%dir %{_includedir}/X11
%dir %{_includedir}/X11/Xtrans
%{_includedir}/X11/Xtrans/Xtrans.c
%{_includedir}/X11/Xtrans/Xtrans.h
%{_includedir}/X11/Xtrans/Xtransint.h
%{_includedir}/X11/Xtrans/Xtranslcl.c
%{_includedir}/X11/Xtrans/Xtranssock.c
%{_includedir}/X11/Xtrans/Xtransutil.c
%{_includedir}/X11/Xtrans/transport.c
%{_datadir}/aclocal/xtrans.m4
%{_datadir}/pkgconfig/xtrans.pc

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 11 2024 José Expósito <jexposit@redhat.com> - 1.5.2-1
- xtrans 1.5.2

* Fri Oct 18 2024 José Expósito <jexposit@redhat.com> - 1.5.1-1
- xtrans 1.5.1

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 07 2023 José Expósito <jexposit@redhat.com> - 1.4.0-12
- SPDX Migration

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov  5 11:05:08 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-5
- Add BuildRequires for make

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 21 2019 Adam Jackson <ajax@redhat.com> - 1.4.0-1
- xtrans 1.4.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 23 2014 Adam Jackson <ajax@redhat.com> 1.3.5-1
- xtrans 1.3.5

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Hans de Goede <hdegoede@redhat.com> - 1.3.4-1
- xtrans 1.3.4

* Tue Jan 28 2014 Hans de Goede <hdegoede@redhat.com> - 1.3.3-1
- xtrans 1.3.3
- drop unnecessary autoreconf call

* Mon Dec  2 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.3.2-2
- Install docs to %%{_pkgdocdir} where available (#993878).

* Mon Nov 18 2013 Dave Airlie <airlied@redhat.com> 1.3.2-1
- xtrans 1.3.2

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> 1.3.0-1
- xtrans 1.3.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 1.2.7-4
- autoreconf for aarch64

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 09 2012 Adam Jackson <ajax@redhat.com> 1.2.7-1
- xtrans 1.2.7 (#806309)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 09 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.6-1
- xtrans 1.2.6

* Sat Sep 25 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.2.2-5
- Merge-review cleanup (#226656)

* Mon Aug 03 2009 Adam Jackson <ajax@redhat.com> 1.2.2-4
- Un-Requires xorg-x11-filesystem

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 09 2008 Adam Jackson <ajax@redhat.com> 1.2.2-1
- xtrans 1.2.2
- Move to BuildArch: noarch.

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.2.1-2
- Fix license tag.

* Wed Jul 02 2008 Adam Jackson <ajax@redhat.com> 1.2.1-1
- xtrans 1.2.1

* Tue May 06 2008 Bill Nottingham <notting@redhat.com> 1.1-2
- xtrans-1.1-abstract.patch: Don't worry about making /tmp/.X11-unix
  (or failure to do so) if you're using an abstract socket (#445303)

* Wed Mar 05 2008 Adam Jackson <ajax@redhat.com> 1.1-1
- xtrans 1.1

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.3-6
- Autorebuild for GCC 4.3

* Mon Oct 01 2007 Adam Jackson <ajax@redhat.com> 1.0.3-5
- xtrans-1.0.3-avoid-gethostname.patch: Don't trust gethostname() output
  when building networkIds for AF_UNIX sockets.  Fixes application launch
  delays and failures when dhclient changes your hostname from under you.

* Thu Sep 20 2007 Adam Jackson <ajax@redhat.com> 1.0.3-4
- Fix a bug in automatic port generation for abstract sockets.  Fixes fast
  user switching, among other things.

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> 1.0.3-3
- Abstract sockets for PF_UNIX.

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.0.3-2
- Don't install INSTALL

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1.0.3-1
- Update to 1.0.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-1.1
- rebuild

* Mon Jul 10 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1.fc6
- Update to xtrans-1.0.1
- Remove xtrans-1.0.0-setuid.diff as it is included in 1.0.1

* Tue Jun 20 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-4
- Added xtrans-1.0.0-setuid.diff to fix potential security issue (#195555)
- Use setup -n instead of -c, and remove extraneous calls to cd from build
  and install sections.
- Use "make install DESTDIR=$RPM_BUILD_ROOT" instead of makeinstall macro.
- Added "AUTHORS ChangeLog COPYING INSTALL NEWS README" to doc macro.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-3
- Bump and rebuild.

* Fri Dec 23 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bump and rebuild.

* Thu Dec 15 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update to xtrans-1.0.0 from X11R7 RC4 release.

* Tue Nov 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Add "Requires(pre): xorg-x11-filesystem >= 0.99.2-3" to avoid bug (#173384).

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Update to xtrans-0.99.2 from X11R7 RC2 release.

* Thu Oct 20 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Update to xtrans-0.99.1 from X11R7 RC1 release.
- This package contains only C source and header files and pkg-config
  *.pc files, and does not contain any ELF binaries or DSOs, so we disable
  debuginfo generation.

* Sun Oct 02 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Use Fedora-Extras style BuildRoot tag
- Add tarball URL

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
