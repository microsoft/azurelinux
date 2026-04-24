# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global         rc_subver     rc5
%global         optflags      %{optflags} -std=gnu17

Summary:        ASCII art library
Name:           aalib
Version:        1.4.0
Release: 1.56.%{rc_subver}%{?dist}
License:        LGPL-2.1-or-later
URL:            http://aa-project.sourceforge.net/aalib/
Source0:        http://download.sourceforge.net/aa-project/%{name}-1.4%{rc_subver}.tar.gz
Patch0:         aalib-aclocal.patch
Patch1:         aalib-config-rpath.patch
Patch2:         aalib-1.4rc5-bug149361.patch
Patch3:         aalib-1.4rc5-rpath.patch
Patch4:         aalib-1.4rc5-x_libs.patch
Patch5:         aalib-1.4rc5-libflag.patch
Patch6:         aalib-c99.patch
Patch7:         https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/aalib/files/aalib-1.4_rc5-free-offset-pointer.patch
Patch8:         https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/aalib/files/aalib-1.4_rc5-fix-aarender.patch
# Modern ncurses has an opaque WINDOW structure (you cannot address its members directly)
# Use the getmaxx() and getmaxy() functions provided by ncurses instead.
Patch9:		aalib-1.4rc5-opaque-ncurses-fix.patch

BuildRequires:  autoconf
BuildRequires:  gpm-devel
BuildRequires:  libtool
BuildRequires:  libXt-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  slang-devel

%description
AA-lib is a low level gfx library just as many other libraries are. The
main difference is that AA-lib does not require graphics device. In
fact, there is no graphical output possible. AA-lib replaces those
old-fashioned output methods with a powerful ASCII art renderer. The API
is designed to be similar to other graphics libraries.

%package libs
Summary:        Library files for aalib
%description libs
This package contains library files for aalib.

%package devel
Summary:        Development files for aalib
Requires:       %{name}-libs = %{version}-%{release}

%description devel
This package contains header files and other files needed to develop
with aalib.


%prep
%setup -q
%patch -P0 -p0
%patch -P1 -p0
%patch -P2 -p1 -b .bug149361
%patch -P3 -p1 -b .rpath
%patch -P4 -p1 -b .x_libs
%patch -P5 -p0 -b .libflag
%patch -P6 -p1
%patch -P7 -p1 -b .free-offset-pointer
%patch -P8 -p1 -b .fix-aarender
%patch -P9 -p1 -b .opaque-ncurses-fix
# included libtool is too old, we need to rebuild
autoreconf -v -f -i

%build
%configure --disable-static  --with-curses-driver=yes --with-ncurses

%make_build


%install
%make_install
rm -f $RPM_BUILD_ROOT{%{_libdir}/libaa.la,%{_infodir}/dir}

# clean up multilib conflicts
touch -r NEWS $RPM_BUILD_ROOT%{_bindir}/aalib-config $RPM_BUILD_ROOT%{_datadir}/aclocal/aalib.m4

%ldconfig_scriptlets libs

%files
%{_bindir}/aafire
%{_bindir}/aainfo
%{_bindir}/aasavefont
%{_bindir}/aatest
%{_mandir}/man1/aafire.1*

%files libs
%doc README ChangeLog NEWS
%license COPYING
%{_libdir}/libaa.so.1*

%files devel
%{_bindir}/aalib-config
%{_mandir}/man3/*
%{_libdir}/libaa.so
%{_includedir}/aalib.h
%{_infodir}/aalib.info*
%{_datadir}/aclocal/aalib.m4

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.56.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar  3 2025 Tom Callaway <spot@fedoraproject.org> - 1.4.0-0.55.rc5
- force std=gnu17 (it does not support C23)
- fixes FTBFS

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.54.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Xavier Bachelot <xavier@bachelot.org> - 1.4.0-0.53.rc5
- Re-enable gpm on EL10

* Fri Oct 04 2024 Xavier Bachelot <xavier@bachelot.org> - 1.4.0-0.52.rc5
- Do not BuildRequires gpm-devel on EL10
- Specfile clean up

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.51.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 10 2024 Tom Callaway <spot@fedoraproject.org> - 1.4.0-0.50.rc5
- apply two fixes from gentoo
- fix aalib to handle opaque WINDOW in ncurses
- fix license tag
- fix patch macro syntax
- fixes FTBFS

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.49.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.48.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.47.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 06 2023 Florian Weimer <fweimer@redhat.com> - 1.4.0-0.46.rc5
- Port to C99

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.45.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.44.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.43.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.42.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.41.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.40.rc5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.39.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.38.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.37.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.36.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.35.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.34.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.0-0.33.rc5
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.32.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.31.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.30.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-0.29.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Tom Callaway <spot@fedoraproject.org> - 1.4.0-0.28.rc5
- spec cleanups

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.27.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.26.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.25.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 28 2013 Tom Callaway <spot@fedoraproject.org> - 1.4.0-0.24.rc5
- rebuild to drop ancient obsoletes

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.23.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.22.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.21.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.20.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.19.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.18.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.17.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 18 2008 Caolán McNamara <caolanm@redhat.com> 1.4.0-0.16.rc5
- rebuild for new libgpm

* Mon Mar 24 2008 Garrick Staples <garrick@usc.edu> 1.4.0-0.15.rc5
- remove unnecessary link bloat from aalib-config
- libs package doesn't need to require base package
- move docs to libs package

* Thu Feb 14 2008 Garrick Staples <garrick@usc.edu> 1.4.0-0.14.rc5
- fix multilib conflicts by splitting out libs package and fix
  timestamps and aalib-config

* Wed Aug 15 2007 Garrick Staples <garrick@usc.edu> 1.4.0-0.13.rc5
- correct License: tag

* Fri May  4 2007 Bill Nottingham <notting@redhat.com> 1.4.0-0.12.rc5
- remove some dainbramage in ltconfig so it builds shared libs on ppc64

* Thu Oct 19 2006 Garrick Staples <garrick@usc.edu> 1.4.0-0.11.rc5
- incorrect subversion in previous two changelog entries

* Thu Oct 19 2006 Garrick Staples <garrick@usc.edu> 1.4.0-0.10.rc6
- Rebuild with ncurses support

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-0.8.rc6
- FE6 Rebuild

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-0.8.rc5
- Taking over as maintainer since Anvil has other priorities
- Long long due rebuild with new gcc for FC-5 (bug 185870)
- Add %%{?dist} tag
- Make release field comply with the Package Naming guidelines for
  pre releases. Luckily according to rpm 8 > rc5 so this can be done.
- Fix some rpmlint warnings
- Fix (remove) use of rpath

* Mon Nov 28 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.4.0-0.rc5.7
- Fix modular X dependencies.
- Rebuild against new slang.
- Disable static lib, not shipping it anyway.
- Prune unneeded libs from aalib-config (and corresponding deps from -devel).
- Don't use %%exclude.

* Mon Nov 21 2005 Warren Togami <wtogami@redhat.com> - 1.4.0-0.rc5.6
- remove .a
- XFree86-devel -> libX11-devel

* Fri Jul  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.4.0-0.rc5.5
- fix missing return value (#149361)

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.4.0-0.rc5.4
- rebuilt

* Thu Dec 16 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 1.4.0-0.rc5.3
- If Epoch is dropped, %%epoch must not be used anywhere else.

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 1.4.0-0.rc5.2
- Bump release for compatibility (still, it'll break *sigh*).
- Fix possible non zero exit status from %%install.
- Fix owning the entire man3/ directory.
- Pending possible changes : --with-ncurses & ncurses-devel build dep.

* Fri Jul 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.4.0-0.fdr.0.9.rc5
- Fix underquoted definition in aalib.m4 to appease aclocal >= 1.8.
- Avoid rpath in aalib-config.
- Split Requires for post and postun into two to work around a rpm bug.
- Other minor specfile improvements.

* Thu Aug 21 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.8.rc5
- devel package now requires info
- Rewrote scriplets
- buildroot -> RPM_BUILD_ROOT
- Moved info files into devel package

* Tue Aug  5 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.7.rc5
- Removed '-p /sbin/ldconfig' in post scriptlet

* Thu Apr 10 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.6.rc5
- Added missing gpm-devel *Requires

* Mon Apr  7 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.5.rc5
- Moved configure from prep to build section.
- Modified post* and pre* scriplets

* Thu Apr  3 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.4.rc5
- Fix things between exclude, rm -f, lib*.la, and infodir/dir things
- Added URL in Source0.

* Thu Apr  3 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.3.rc5
- Modified devel Requires:
- Removed gcc as requirement

* Wed Apr  2 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.2.rc5
- Applied spec modifications from Adrian Reber

* Tue Apr  1 2003 Dams <anvil[AT]livna.org>
- Initial build.
