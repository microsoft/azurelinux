Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# note this duplicates native anthy IMEs
%bcond_with anthy

Name:           m17n-lib
Version:        1.8.0
Release:        8%{?dist}
Summary:        Multilingual text library

License:        LGPLv2+
URL:            https://www.nongnu.org/m17n/
Source0:        https://download.savannah.gnu.org/releases/m17n/%{name}-%{version}.tar.gz
Patch0:         %{name}-1.8.0-multilib.patch
Patch1:         Fix-segmentation-fault-when-using-ibus-m17n-with-vi-telex-in-gedit-in-wayland.patch

BuildRequires:  m17n-db-devel libthai-devel
BuildRequires:  libxml2-devel
BuildRequires:  fontconfig-devel freetype-devel
BuildRequires:  fribidi-devel gd-devel
BuildRequires:  libotf-devel
BuildRequires:  autoconf gettext-devel
BuildRequires:  automake libtool

# The upstream source contains part of gnulib
# library which includes directories intl and m4
Provides: bundled(gnulib)

%if %{with anthy}
BuildRequires:  anthy-devel
%endif

Requires:       m17n-db

%description
m17n-lib is a multilingual text library used primarily to allow
the input of many languages with the input table maps from m17n-db.

The package provides the core and input method backend libraries.

%package  anthy
Summary:  Anthy module for m17n
Requires: %{name}%{?_isa} = %{version}-%{release}

%description anthy
Anthy module for %{name} allows ja-anthy.mim to support input conversion.


%package  devel
Summary:  Development files for %{name}
Requires: %{name}-tools = %{version}-%{release}

%description devel
Development files for %{name}.


%package  tools
Summary:  The m17n GUI Library tools
Requires: m17n-db-extras
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to test M17n GUI widget library.


%prep
%autosetup -p1

%build
#autoreconf -ivf
%configure --disable-rpath --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# parallel make usage with make command fails build on koji
make

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

# fix bug rh#680363
rm %{buildroot}%{_libdir}/m17n/1.0/libmimx-ispell.so

find %{buildroot} -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets

%ldconfig_scriptlets tools

%files
%doc AUTHORS NEWS ChangeLog README
%license COPYING
#Own module directory path
%dir %{_libdir}/m17n
%dir %{_libdir}/m17n/1.0
%{_bindir}/m17n-conv
%{_libdir}/libm17n.so.*
%{_libdir}/libm17n-core.so.*
%{_libdir}/libm17n-flt.so.*

#Anthy module
%files anthy
%{_libdir}/m17n/1.0/libmimx-anthy.so

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%files tools
%{_bindir}/m17n-date
%{_bindir}/m17n-dump
%{_bindir}/m17n-edit
%{_bindir}/m17n-view
%{_libdir}/m17n/1.0/libm17n-X.so
%{_libdir}/m17n/1.0/libm17n-gd.so
%{_libdir}/libm17n-gui.so.*

%changelog
* Fri Mar 26 2021 Henry Li <lihl@microsoft.com> - 1.8.0-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove x11-related depdendencies
- Disable depending on anthy, which wil cause build cycle 

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 30 2019 Mike FABIAN <mfabian@redhat.com> - 1.8.0-5
- Fix segmentation fault when using ibus-m17n with vi-telex in gedit in Gnome Wayland
- Resolves: rhbz#1704156

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 26 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.8.0-3
- Added Provides: bundled(gnulib)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Feb 10 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.8.0-1
- Update to 1.8.0 version (#1543670)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-0.2.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.8.0-0.1.RC1
- Update to 1.8.0 (#1523968)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 26 2015 Mike FABIAN <mfabian@redhat.com> - 1.7.0-4
- Fix "Transliteration not working on Marathi language" (it crashed).
- Resolves: rhbz#1256244

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.7.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Dec 22 2014 Parag Nemade <pnemade AT redhat DOT com> - 1.7.0-1
- update to 1.7.0
- Drop aarch64 patch and use autoreconf

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 07 2014 Parag Nemade <pnemade AT redhat DOT com> - 1.6.4-12
- Resolves:rh#1127583 - Add missing BuildRequires

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 1.6.4-9
- rebuild for new GD 2.1.0

* Sun Mar 24 2013 Parag Nemade <pnemade AT redhat DOT com> - 1.6.4-8
- Resolves:rh#926108 - Does not support aarch64 in f19 and rawhide

* Thu Mar 14 2013 Hans de Goede <hdegoede@redhat.com> - 1.6.4-7
- Fix m17n-config not working on non x86_* archs (rh#921189)

* Mon Mar 11 2013 Parag Nemade <pnemade AT redhat DOT com> - 1.6.4-6
- Resolves:rh#907488 - shell syntax error in m17n-config

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Parag Nemade <pnemade AT redhat DOT com> - 1.6.4-4
- Resolves:rh#880957 - m17n-lib doesn't uninstall properly

* Tue Nov 20 2012 Parag Nemade <pnemade AT redhat DOT com> - 1.6.4-3
- m17n-lib to own %%{_libdir}/m17n

* Tue Nov 20 2012 Parag Nemade <pnemade AT redhat DOT com> - 1.6.4-2
- Resolves:rh#877925 - drop m17n-lib-flt provides
- Fix bogus date in %%changelog
- Make sure not to attempt to use parallel make as it fails the build

* Tue Sep 18 2012 Parag Nemade <pnemade AT redhat DOT com> - 1.6.4-1
- update to 1.6.4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Parag Nemade <pnemade AT redhat DOT com> - 1.6.3-1
- update to 1.6.3

* Tue Mar 22 2011 Parag Nemade <pnemade AT redhat DOT com> - 1.6.2-3
- Resolves: rh#680363 - Remove m17n-lib-ispell subpackage
- Resolves: rh#677866 - m17n*.pc reports wrong moduledir on x86_64 system

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 06 2010 Parag Nemade <pnemade AT redhat.com> - 1.6.2-1
- update to new upstream release 1.6.2

* Mon Sep 13 2010 Parag Nemade <pnemade AT redhat.com> - 1.6.1-5
- Fix some packaging issue
- Change Requires: m17n-db-datafiles to m17n-db-extras

* Fri Sep 10 2010 Daiki Ueno <dueno@redhat.com> - 1.6.1-4
- supply libotf cflags/libs manually, since the current libotf package
  does not ship with "libotf-config" and m17n-lib cannot detect those
  values
- fix paths for modules used by GUI support

* Wed Aug 11 2010 Adam Jackson <ajax@redhat.com> 1.6.1-3
- Fix Obsoletes: so upgrades actually work (1.5.5-3 < 1.5.5-3.fc13)

* Wed Jul 07 2010 Parag Nemade <pnemade@redhat.com> - 1.6.1-2
- Resolves: rh#602029:-m17n-lib-devel multilib conflict 
- Fix rpmlint rpath error.

* Tue Apr 27 2010 Parag Nemade <pnemade AT redhat.com> - 1.6.1-1
- update to new upstream release 1.6.1

* Wed Apr 07 2010 Parag Nemade <pnemade AT redhat.com> - 1.6.0-1
- update to new upstream release 1.6.0

* Wed Dec 23 2009 Jens Petersen <petersen@redhat.com> - 1.5.5-2
- add bcond for otf, anthy, and gui
- subpackage flt for emacs, etc
- add subpackages for anthy and ispell modules
- disable new gui subpackage (and hence ispell)

* Mon Aug 17 2009 Parag Nemade <pnemade@redhat.com> - 1.5.5-1
- update to new upstream release 1.5.5

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Parag Nemade <pnemade@redhat.com> -1.5.4-1
- Update to new upstream release 1.5.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 21 2008 Parag Nemade <pnemade@redhat.com> -1.5.3-1.fc10
- Update to new upstream release 1.5.3

* Thu Jul 03 2008 Parag Nemade <pnemade@redhat.com> -1.5.2-1
- Update to new upstream release 1.5.2

* Thu Feb 07 2008 Parag Nemade <pnemade@redhat.com> -1.5.1-1.fc9
- Update to new upstream release 1.5.1

* Fri Dec 28 2007 Parag Nemade <pnemade@redhat.com> -1.5.0-1.fc9
- Update to new upstream release 1.5.0
- Added missing internal-flt.h file as Source1

* Wed Aug 22 2007 Parag Nemade <pnemade@redhat.com> - 1.4.0-2
- rebuild against new rpm package
- update license tag

* Thu Jul 19 2007 Jens Petersen <petersen@redhat.com>
- buildrequire and require m17n-db >= 1.4.0

* Thu Jul 19 2007 Parag Nemade <pnemade@redhat.com> - 1.4.0-1
- Updated to new upstream release 1.4.0

* Wed Jan 10 2007 Mayank Jain <majain@redhat.com> - 1.3.4-1.1.fc7
- rebuild for m17n-lib-1.3.4 version
- Updated m17n-lib-nobuild-examples.patch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.3-1.1.fc6
- rebuild

* Wed Jul 12 2006 Mayank Jain <majain@redhat.com> - 1.3.3-1.fc6
- Updated spec file for changes mentioned in RH bug 193524, comment 4
- Thanks to Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>

* Thu Mar  2 2006 Jens Petersen <petersen@redhat.com> - 1.3.3-1
- update to 1.3.3 minor bugfix release

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.2-1.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Jens Petersen <petersen@redhat.com> - 1.3.2-1
- update to 1.3.2 bugfix release
  - m17n-lib-no-gui-headers.patch is now upstream

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Jens Petersen <petersen@redhat.com> - 1.3.1-1
- update to 1.3.1 release
  - rename use_otf and use_anthy macros to with_gui and with_examples
  - build --with-gui=no and replace m17n-lib-1.2.0-core-libs-only.patch
    with m17n-lib-no-gui-headers.patch and m17n-lib-nobuild-examples.patch

* Fri Dec 16 2005 Jens Petersen <petersen@redhat.com> - 1.2.0-2
- import to Fedora Core
- buildrequire autoconf

* Thu Nov 10 2005 Jens Petersen <petersen@redhat.com> - 1.2.0-1
- do not build static lib and .la files (Warren Togami)

* Wed Oct  5 2005 Jens Petersen <petersen@redhat.com>
- initial packaging for Fedora Extras

* Sat Jan 15 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp>
- modify spec for fedora
