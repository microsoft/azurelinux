# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Tools to support ATM networking under Linux
Name: linux-atm
Version: 2.5.1
Release: 45%{?dist}
# The licensing here is a mess. This is as close to accurate as possible.
License: GPL-2.0-only AND GPL-2.0-or-later AND LGPL-2.0-or-later
URL: http://linux-atm.sourceforge.net/
Source0: http://downloads.sf.net/%{name}/%{name}-%{version}.tgz

BuildRequires: automake
BuildRequires: byacc
BuildRequires: flex
BuildRequires: flex-static
# Older kernel headers had broken ATM includes
BuildRequires: glibc-kernheaders >= 2.4-9.1.88
BuildRequires: libtool
BuildRequires: make

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

# Patch from Debian to sanify syslogging
Patch2: linux-atm-2.5.0-open-macro.patch
Patch3: linux-atm-2.5.0-disable-ilmidiag.patch
Patch4: linux-atm-gcc43.patch
Patch5: man-pages.patch
Patch6: add-string-formatting-to-build-with-gcc7.patch
Patch7: remove-define-hacks.patch
Patch8: siocgstamp.patch
# The ZeitNet ZN122x ATM driver was dropped in kernel 5.19, so the zntune binary
# can't be built anymore
# See: https://github.com/torvalds/linux/commit/052e1f01bfae8be6f31b61ed3a2356edfca855dc
Patch9: linux-atm-2.5.1-disable-zntune.patch
Patch10: linux-atm-c99.patch
Patch11: linux-atm-use_socklen_t.patch
Patch12: linux-atm-dont-use-bool-keyword.patch

%description
Tools to support ATM networking under Linux.

%package libs
Summary: Linux ATM API library
License: LGPL-2.0-or-later

%description libs
This package contains the ATM library required for user space ATM tools.

%package libs-devel
Summary: Development files for Linux ATM API library
Requires: linux-atm-libs = %{version}-%{release}
Requires: glibc-kernheaders >= 2.4-9.1.88

%description libs-devel
This package contains header files and libraries for development using the
Linux ATM API.

%prep
%autosetup -p1

iconv -f iso8859-1 -t utf8 < src/extra/ANS/e164_cc > src/extra/ANS/e164_cc.1
mv src/extra/ANS/e164_cc.1 src/extra/ANS/e164_cc
iconv -f iso8859-1 -t utf8 < doc/atm-linux-howto.txt > doc/atm-linux-howto.txt.1
mv doc/atm-linux-howto.txt.1 doc/atm-linux-howto.txt

%build
./autotools
CFLAGS="%optflags -D_LINUX_TIME_H"
%configure --disable-static
# Drop the default RPATH
# See: https://docs.fedoraproject.org/en-US/packaging-guidelines/#_beware_of_rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make

%install
#rm -rf $RPM_BUILD_ROOT _doc CVS ANS doc/{\.cvsignore,CVS} init-redhat/{CVS,\.cvsignore}
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/libatm.{a,la}
install -m 0644 src/config/hosts.atm $RPM_BUILD_ROOT/etc/
# Selectively sort what we want included in %%doc
mkdir _doc
cp -a doc/ src/config/init-redhat/ src/extra/ANS/ _doc/
rm -f _doc/Makefile* _doc/*/Makefile* _doc/doc/*.sgml
chmod 0644 src/extra/ANS/{atm,pdf2e164_cc.pl,hosts2ans.pl}
chmod 0644 _doc/{ANS/pdf2e164_cc.pl,ANS/hosts2ans.pl,init-redhat/atm,doc/atm-linux-howto.txt}

# remove CVS files from installation
rm -rf _doc/ANS
rm -rf _doc/doc/{.cvsignore,CVS}
rm -rf _doc/init-redhat/{CVS,.cvsignore}

%ldconfig_scriptlets libs

%files
%{!?_licensedir:%global license %%doc}
%license COPYING*
%doc AUTHORS BUGS ChangeLog NEWS README THANKS _doc/*
%config(noreplace) /etc/atmsigd.conf
%config(noreplace) /etc/hosts.atm
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man4/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING.LGPL
%{_libdir}/libatm.so.*

%files libs-devel
%{_includedir}/*
%{_libdir}/libatm.so

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 24 2025 Frantisek Sumsal <frantisek@sumsal.cz> - 2.5.1-44
- Update package license to make rpminspect happy

* Fri Jan 24 2025 Frantisek Sumsal <frantisek@sumsal.cz> - 2.5.1-43
- Fix FTBFS with gcc-15 (rhbz#2340776)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 2.5.1-41
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Frantisek Sumsal <frantisek@sumsal.cz> - 2.5.1-38
- Fix FTBFS with gcc-14

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr 16 2023 Florian Weimer <fweimer@redhat.com> - 2.5.1-35
- Port to C99

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 08 2022 Frantisek Sumsal <frantisek@sumsal.cz> - 2.5.1-32
- Disable zntune, since the respective driver was dropped in kernel 5.19
- Bring back autotools to make the new and previous patches actually work

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 03 2021 Frantisek Sumsal <frantisek@sumsal.cz> - 2.5.1-30
- Fix FTBFS by dropping the default RPATH (#1987671, #1999509)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 18 2019 Scott Talbert <swt@techie.net> - 2.5.1-24
- Include <linux/sockios.h> to fix another FTBFS with newer kernel headers

* Fri May 03 2019 Scott Talbert <swt@techie.net> - 2.5.1-23
- Remove _LINUX_NETDEVICE_H define hacks to fix FTBFS (#1675323)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun May 28 2017 Niko Kortstrom <niko.kortstrom@gmail.com> 2.5.1-17
- Add string formatting to build with GCC 7 using -Werror=format-security (#1456255)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 27 2016 Lubomir Rintel <lkundrak@v3.sk> - 2.5.1-15
- Fix FTBFS

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.5.1-12
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.5.1-10
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Petr Šabata <contyk@redhat.com> - 2.5.1-7
- Explicitly require our libs subpackage to be sure we always use the current version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 13 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.5.1-2
- fix few rpmlint warnings 226097

* Fri May 28 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.1-1
- update to 2.5.1
- disable static libs

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.0-8
- fix license tag

* Fri Apr 18 2008 David Woodhouse <dwmw2@infradead.org> - 2.5.0-7
- Fix GCC 4.3 compilation (#434069)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5.0-6
- Autorebuild for GCC 4.3

* Thu Jan 03 2008 David Woodhouse <dwmw2@infradead.org> - 2.5.0-5
- Update to 2.5.0 release

* Thu Aug 23 2007 David Woodhouse <dwmw2@infradead.org> - 2.5.0-4.20070823cvs
- Update from CVS

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> - 2.5.0-3.20050118cvs
- Update licence
- Handle open being a macro

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> - 2.5.0-2.20050118cvs
- Include <linux/types.h> before various other <linux/*.h> headers

* Thu Jul 13 2006 Jesse Keating <jkeating@redhat.com> - 2.5.0-1.20050118cvs
- fix release to meet guidelines

* Thu Jul 13 2006 Jesse Keating <jkeating@redhat.com> - 2.5.0-0.20050118.6
- rebuild
- add missing br automake libtool flex

* Tue May 30 2006 David Woodhouse <dwmw2@redhat.com> - 2.5.0-0.20050118.3.3
- BuildRequires: byacc

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.5.0-0.20050118.3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.5.0-0.20050118.3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 21 2005 David Woodhouse <dwmw2@redhat.com> 2.5.0-0.20050118.3
- Package cleanups from Matthias Saou (#172932):
-  Add missing /sbin/ldconfig calls for the libs package.
-  Tag atmsigd.conf config file as noreplace.
-  Remove INSTALL (dangling symlink) from %%doc.
-  Don't include Makefile* file from doc/.
-  Don't include both sgml and txt howto (only txt).
-  Minor spec file cleanups.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 2 2005 David Woodhouse <dwmw2@redhat.com> 2.5.0-0.20050118.2
- Rebuild with gcc 4

* Tue Jan 18 2005 David Woodhouse <dwmw2@redhat.com> 2.5.0-0.20050118.1
- Include stdlib.h for strtol prototype in sigd/cfg_y.y

* Tue Jan 18 2005 David Woodhouse <dwmw2@redhat.com> 2.5.0-0.20050118
- Update to v2_5_0 branch to get br2684ctl utility

* Wed Sep 29 2004 David Woodhouse <dwmw2@redhat.com> 2.4.1-4
- Fix duplicate files in libs and main packages

* Wed Sep 29 2004 David Woodhouse <dwmw2@redhat.com> 2.4.1-3
- Fix labels at end of compound statement

* Thu Jul 1 2004 David Woodhouse <dwmw2@redhat.com> 2.4.1-2
- Add patch to work around FC2 glibc-kernheaders breakage

* Wed Jun 30 2004 David Woodhouse <dwmw2@redhat.com> 2.4.1-1
- Build for Fedora

* Fri Sep 14 2001 Paul Schroeder <paulsch@us.ibm.com>
- First build of linux-atm RPM.
