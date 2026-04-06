# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           gnome-common
Version:        3.18.0
Release:        22%{?dist}
Summary:        Useful things common to building GNOME packages from scratch
BuildArch:      noarch
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            https://wiki.gnome.org/Projects/GnomeCommon
Source0:        https://download.gnome.org/sources/%{name}/3.18/%{name}-%{version}.tar.xz

BuildRequires: make

# This will pull in the latest version; if your package requires something older,
# well, BuildRequire it in that spec.  At least until such time as we have a
# build system that is intelligent enough to inspect your source code
# and auto-inject those requirements.
Requires:       automake
Requires:       autoconf
Requires:       autoconf-archive
Requires:       gettext
Requires:       libtool
Requires:       pkgconfig
Requires:       yelp-tools

%description
This package contains sample files that should be used to develop pretty much
every GNOME application.  The programs included here are not needed for running
GNOME apps or building ones from distributed tarballs.  They are only useful
for compiling from git sources or when developing the build infrastructure for
a GNOME application.

%prep
%setup -q

%build
%configure --with-autoconf-archive
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL="install -p" install

%files
%doc ChangeLog README
%license COPYING
%{_bindir}/gnome-autogen.sh
%{_datadir}/aclocal/*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 3.18.0-20
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 21 2015 David King <amigadave@amigadave.com> - 3.18.0-1
- Update to 3.18.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Feb 15 2015 Christopher Meng <rpm@cicku.me> - 3.14.0-2
- Drop conflicting macros and depend on autoconf-archive (#1192754)
- Use license macro for COPYING

* Mon Sep 22 2014 David King <amigadave@amigadave.com> - 3.14.0-1
- Update to 3.14.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 24 2014 David King <amigadave@amigadave.com> - 3.12.0-1
- Update to 3.12.0

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Thu Sep 19 2013 Bastien Nocera <bnocera@redhat.com> 3.7.4-5
- Require yelp-tools for the oft-used yelp.m4 file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  1 2013 Marek Kasik <mkasik@redhat.com> - 3.7.4-3
- Update license field and link to source archive

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Mon Jan 14 2013 Marek Kasik <mkasik@redhat.com> - 3.6.0-2
- Backport patch for support of automake-1.13

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Thu Jul 19 2012 Marek Kasik <mkasik@redhat.com> - 3.4.0.1-3
- Backport patch for support of automake-1.12

* Tue Jul 17 2012 Jiri Popelka <jpopelka@redhat.com> - 3.4.0.1-2
- Match actual license

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0.1-1
- Update to 3.4.0.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.0-1
- Update to 3.1.0

* Sun Apr  3 2011 Christopher Aillon <caillon@redhat.com> - 2.34.0-1
- Update to 2.34.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Mar 26 2010 Colin Walters <walters@verbum.org> - 2.28.0-2
- Readd Requires on components; optimizing for the case where
  you want to have gnome-common but not the autotools is total
  nonsense.  "automake" pulls in the latest which is good enough;
  if your package BuildRequires an older version, well add that
  to the package.

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-2
- Support automake 1.11

* Sun Mar 29 2009  Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 2.24.0-1
- Update to version 2.24.0

* Mon Apr 7 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 2.20.0-1
- Update to version 2.20.0.

* Sun Aug 12 2007 Toshio Kuratomi <a.badger@gmail.com> - 2.18.0-1
- Update to version that matches gnome-2.18.
- Update license tag to strict GPLv2.

* Wed Dec 06 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.12.0-4
- Add a patch from gnome-common cvs to address bug #218717 (gnome-common
  does not work with automake-1.10).

* Mon Sep 04 2006 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.12.0-3
- Bump and rebuild for FC6.

* Thu Feb 16 2006 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.12.0-2
- Bump and rebuild for FC5.

* Tue Oct 18 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.12.0-1
- Upgrade to 2.12.0.
- Add dist tag.

* Thu May 12 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.8.0-3
- Bump and rebuild to get versions synced across architectures.

* Fri Mar 18 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.8.0-2
- Rebuild for FC4t1

* Tue Sep 14 2004 Toshio Kuratomi <toshio-tiki-lounge.com> - 0:2.8.0-1
- Update to 2.8.0
  + This release supports automake thru version 1.9 and has had a lot of
    deprecated stuff cleaned out.
- Removed BuildRequires.  A base mach build environment will build it now.
- Removed Requires.  Although gnome-common still requires autoconf and
  friends, it doesn't require a specific version of them.  There's no virtual
  provides in the automake14,15,16,17 automake packages that could help here.

* Mon Mar 22 2004 Toshio Kuratomi <toshio-tiki-lounge.com> - 0:2.4.0-0.fdr.3
- Add COPYING file to the docs
- Add bin/Changelog to the docs as ChangeLog.bin

* Sun Dec 28 2003 Toshio Kuratomi <toshio-tiki-lounge.com> - 0:2.4.0-0.fdr.2
- Update the Requires line (rpm doesn't automatically detect most of the
  dependencies.)
- Remove the AUTHORS file as it's currently empty

* Fri Dec 19 2003 Toshio Kuratomi <toshio-tiki-lounge.com> - 0:2.4.0-0.fdr.1
- Initial RPM release.
