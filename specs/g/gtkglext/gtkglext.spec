# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define api_version		1.0

Summary:	OpenGL Extension to GTK
Name:		gtkglext
Version:	1.2.0
Release: 52%{?dist}

License:	GPL-2.0-or-later OR LGPL-2.0-or-later
URL:		http://gtkglext.sourceforge.net/
Source0:	ftp://ftp.gnome.org/pub/gnome/sources/gtkglext/1.2/gtkglext-%{version}.tar.bz2
# Upstream changes, addressing BZ 677457
Patch0:		0001-gtkglext-1.2.0-bz677457.patch
Patch1:		0002-GCC-8-fixes.patch
# HACK: Disable pangox features
Patch2:		gtkglext-1.2.0-no-pangox.patch
Patch3:		gtkglext-1.2.0-fedora-c99.patch

BuildRequires:  gcc
BuildRequires:	gtk2-devel
BuildRequires:	libGLU-devel
BuildRequires:	libGL-devel
# Conditional build feature
BuildRequires:	libXmu-devel
# The configure script checks for X11/Intrinsic.h
BuildRequires:	libXt-devel
BuildRequires: make
# BuildRequires:  pangox-compat-devel

Requires(postun):	/sbin/ldconfig
Requires(post):		/sbin/ldconfig

%description
GtkGLExt is an OpenGL extension to GTK. It provides the GDK objects
which support OpenGL rendering in GTK, and GtkWidget API add-ons to
make GTK+ widgets OpenGL-capable.

%package libs
Summary:	OpenGL Extension to GTK
License:	LGPL-2.0-or-later

%description libs
GtkGLExt is an OpenGL extension to GTK. It provides the GDK objects
which support OpenGL rendering in GTK, and GtkWidget API add-ons to
make GTK+ widgets OpenGL-capable.

%package devel
Summary:	Development tools for GTK-based OpenGL applications
License:	LGPL-2.0-or-later

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	gtk2-devel
Requires:	libGL-devel
Requires:	libGLU-devel
Requires:	libXmu-devel

%description devel
The gtkglext-devel package contains the header files, static libraries,
and developer docs for GtkGLExt.

%prep
%setup -q -n gtkglext-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1 -b .nopangox
%patch -P3 -p1

%build
%configure --disable-gtk-doc --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{make_build}

%install
%{make_install}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%files libs
%doc AUTHORS ChangeLog README TODO
%license COPYING COPYING.LIB
%{_libdir}/libgdkglext-x11-%{api_version}.so.*
%{_libdir}/libgtkglext-x11-%{api_version}.so.*

%files devel
%{_includedir}/*
%{_libdir}/gtkglext-%{api_version}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*
%doc %{_datadir}/gtk-doc/html/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar  2 2023 DJ Delorie <dj@redhat.com> - 1.2.0-45
- Port configure script to C99

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.0-43
- Modernize spec.
- Convert license to SPDX.
- Update sources to sha512.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Callaway <spot@fedoraproject.org> - 1.2.0-37
- patch out pangox support to get this building again.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 15 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.0-32
- BR: gcc-c.
- Add 0002-GCC-8-fixes.patch (Fix F28FTBFS).
- Rebase patches.
- Modernize spec.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.0-26
- Add %%license.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 28 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.0-22
- Update config.sub|guess from automake-1.13.4 for aarch64
  (Add gtkglext-1.2.0-config.diff; RHBZ#925512).

* Tue Aug 27 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.0-21
- Add BR: pangox-compat-devel (RHBZ#850813, F19FTBFS RHBZ#914061, F20FTBFS RHBZ#992448).
- Spec cleanup.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.0-18
- Remove hard-coded rpath (BZ 828527).
- Reflect Source0:-URL having changed.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.2.0-15
- Rebuild for new libpng

* Thu Feb 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.0-14
- Apply %%patch0.

* Thu Feb 17 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.2.0-13
- Fix dependency in gtkglext-devel (-> gtkglext-libs).

* Wed Feb 16 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.0-12
- Add gtkglext-1.2.0-bz677457.diff (BZ 677457).
- Spec file cleanup.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 07 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-8
- Rebuild for pkgconfig provides

* Tue Jun 03 2008 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-7
- Use 0%%{?fedora} conditionals instead of "%%{fedora}" (BZ 449635).

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-6
- Rebuild for gcc43.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-5
- Don't install *.la's for fedora >= 8.
- Update license tags.
- Split out *-libs.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-4
- Mass rebuild.

* Mon Aug 14 2006 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-3
- BR: libXmu-devel (Braden McDaniel).
- *-devel: R: libXmu-devel. 
- *-devel: R: pkgconfig.

* Tue Feb 14 2006 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-2
- Require: libGLU-devel (PR 181018)

* Mon Feb 06 2006 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-1
- Upstream update.
- Spec file cleanup.
- Disable static libs.

* Thu Jan 05 2006 Ralf Corsepius <ralf@links2linux.de> - 1.0.6-3
- Add %%dist.
- Adaptations to modular X .
- Remove gcc-c++ (Already in default deps).

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Jun 07 2004 Ralf Corsepius <ralf@links2linux.de> - 1.0.6-0.fdr.1
- Spec cleanups.

* Fri Jun 04 2004 Ralf Corsepius <ralf@links2linux.de> - 1.0.6-0.fdr.0
- Initial fedora rpm spec, loosely derived from the version shipped
  with gtkglext.
