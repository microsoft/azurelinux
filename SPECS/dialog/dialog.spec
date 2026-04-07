# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: A utility for creating TTY dialog boxes
Name: dialog
%global dialogsubversion 20250116
Version: 1.3
Release: 55.%{dialogsubversion}%{?dist}
License: LGPL-2.1-only
URL: https://invisible-island.net/dialog/dialog.html
Source0: https://invisible-mirror.net/archives/dialog/dialog-%{version}-%{dialogsubversion}.tgz
Source1: https://invisible-mirror.net/archives/dialog/dialog-%{version}-%{dialogsubversion}.tgz.asc
Source2: https://invisible-island.net/public/dickey@invisible-island.net-rsa3072.asc
BuildRequires: ncurses-devel gcc gettext findutils libtool gnupg2
BuildRequires: make
Patch2: dialog-multilib.patch
Patch3: dialog-libs.patch

%description
Dialog is a utility that allows you to show dialog boxes (containing
questions or messages) in TTY (text mode) interfaces.  Dialog is called
from within a shell script.  The following dialog boxes are implemented:
yes/no, menu, input, message, text, info, checklist, radiolist, and
gauge.  

Install dialog if you would like to create TTY dialog boxes.

%package devel 
Summary: Development files for building applications with the dialog library
Requires: %{name}%{?_isa} = %{version}-%{release} ncurses-devel

%description devel
Dialog is a utility that allows you to show dialog boxes (containing
questions or messages) in TTY (text mode) interfaces. This package 
contains the files needed for developing applications, which use the 
dialog library.

%prep
%{gpgverify} --keyring=%{SOURCE2} --signature=%{SOURCE1} --data=%{SOURCE0}
%setup -q -n dialog-%{version}-%{dialogsubversion}
%patch -P2 -p1 -b .multilib
%patch -P3 -p1 -b .libs

%build
%configure \
	--enable-nls \
	--enable-pc-files \
	--with-libtool \
	--with-libtool-opts="$(for opt in %{?_hardened_ldflags}; do \
				echo -n -Xcompiler $opt ''; done)" \
	--with-ncursesw \
	--includedir=%{_includedir}/dialog
make %{?_smp_mflags}

%install
# prepare packaged samples
rm -rf _samples
mkdir _samples
cp -a samples _samples
rm -rf _samples/samples/install
find _samples -type f -print0 | xargs -0 chmod a-x

make install DESTDIR=$RPM_BUILD_ROOT

chmod 755 $RPM_BUILD_ROOT%{_libdir}/libdialog.so.*.*.*
rm -f $RPM_BUILD_ROOT%{_libdir}/libdialog.{,l}a

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%doc COPYING dialog.lsm README _samples/samples
%{_bindir}/dialog
%{_libdir}/libdialog.so.15*
%{_mandir}/man1/dialog.*

%files devel
%{_bindir}/dialog-config
%{_includedir}/dialog
%{_libdir}/libdialog.so
%{_libdir}/pkgconfig/dialog.pc
%{_mandir}/man3/dialog.*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-55.20250116
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar 03 2025 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-54.20250116
- update to 1.3-20250116

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-53.20240619
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-52.20240619
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-51.20240619
- update to 1.3-20240619

* Wed Jan 31 2024 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-50.20240101
- update to 1.3-20240101

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-49.20231002
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-48.20231002
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 04 2023 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-47.20231002
- update to 1.3-20231002
- convert license tag to SPDX
- package pkgconfig file

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-46.20220526
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-45.20220526
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-44.20220526
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-43.20220526
- update to 1.3-20220526

* Thu Apr 21 2022 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-42.20220414
- update to 1.3-20220414

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-41.20220117
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-40.20220117
- update to 1.3-20220117

* Tue Dec 14 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-39.20211214
- update to 1.3-20211214

* Mon Nov 08 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-38.20211107
- update to 1.3-20211107

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-37.20210621
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-36.20210621
- update to 1.3-20210621

* Mon Jun 07 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-35.20210530
- update to 1.3-20210530

* Mon May 17 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-34.20210509
- update to 1.3-20210509

* Thu Mar 25 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-33.20210324
- update to 1.3-20210324

* Mon Mar 22 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-32.20210319
- update to 1.3-20210319

* Mon Mar 08 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-31.20210306
- update to 1.3-20210306

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-30.20210117
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-29.20210117
- update to 1.3-20210117

* Fri Nov 27 2020 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-28.20201126
- update to 1.3-20201126

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-27.20200327
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 31 2020 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-26.20200327
- update to 1.3-20200327

* Mon Mar 09 2020 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-25.20200228
- update to 1.3-20200228

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-24.20191210
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 11 2019 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-23.20191210
- update to 1.3-20191210

* Mon Nov 11 2019 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-22.20191110
- update to 1.3-20191110

* Mon Aug 12 2019 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-21.20190808
- update to 1.3-20190808

* Wed Aug 07 2019 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-20.20190806
- update to 1.3-20190806
- verify upstream signatures

* Mon Jul 29 2019 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-19.20190728
- update to 1.3-20190728

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-18.20190211
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 20 2019 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-17.20190211
- update to 1.3-20190211

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-16.20180621
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-15.20180621
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 22 2018 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-14.20180621
- update to 1.3-20180621

* Thu Mar 29 2018 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-13.20171209
- update to 1.3-20171209
- fix build with multiple options in hardened ldflags (#1548400)
- add gcc to build requirements
- use macro for ldconfig scriptlets

* Fri Feb 23 2018 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-12.20170509
- fix build to use hardened linker specs (#1548400)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-11.20170509
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-10.20170509
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-9.20170509
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 10 2017 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-8.20170509
- update to 1.3-20170509

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-7.20170131
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-6.20170131
- update to 1.3-20170131

* Wed Sep 07 2016 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-5.20160828
- update to 1.3-20160828

* Tue Apr 26 2016 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-4.20160424
- update to 1.3-20160424

* Wed Feb 10 2016 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-3.20160209
- update to 1.3-20160209

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2.20160126
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Miroslav Lichvar <mlichvar@redhat.com> - 1.3-1.20160126
- update to 1.3-20160126

* Tue Sep 22 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-17.20150528
- update to 1.2-20150920

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-16.20150528
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-15.20150528
- update to 1.2-20150528

* Fri May 15 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-14.20150513
- update to 1.2-20150513

* Thu Feb 26 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-13.20150225
- update to 1.2-20150225

* Thu Jan 29 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-12.20150125
- update to 1.2-20150125

* Fri Sep 12 2014 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-11.20140911
- update to 1.2-20140911

* Tue Sep 02 2014 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-10.20140901
- update to 1.2-20140901

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-9.20140219
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-8.20140219
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 20 2014 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-7.20140219
- update to 1.2-20140219

* Mon Jan 13 2014 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-6.20140112
- update to 1.2-20140112

* Mon Oct 07 2013 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-5.20130928
- update to 1.2-20130928

* Thu Sep 19 2013 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-4.20130902
- update to 1.2-20130902
- fix weekdays in changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3.20130523
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 24 2013 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-2.20130523
- update to 1.2-20130523

* Mon Mar 18 2013 Miroslav Lichvar <mlichvar@redhat.com> - 1.2-1.20121230
- update to 1.2-20121230

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-18.20120706
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-17.20120706
- update to 1.1-20120706
- remove unnecessary macros

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-16.20110707
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-15.20110707
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-14.20110707
- Rebuilt for glibc bug#747377

* Tue Jul 26 2011 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-13.20110707
- update to 1.1-20110707

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-12.20100428
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May 12 2010 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-11.20100428
- update to 1.1-20100428

* Thu Feb 04 2010 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-10.20100119
- update to 1.1-20100119

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-9.20080819
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8.20080819
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 25 2008 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-7.20080819
- update to 1.1-20080819

* Wed Jul 30 2008 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-6.20080727
- update to 1.1-20080727

* Fri Apr 11 2008 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-5.20080316
- update to 1.1-20080316

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1-4.20071028
- Autorebuild for GCC 4.3

* Mon Nov 05 2007 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-3.20071028
- update to 1.1-20071028
- fix multilib conflicts (#341001)
- use shared library, drop static
- merge review fixes (#225693)

* Fri Aug 17 2007 Harald Hoyer <harald@redhat.com> - 1.1-2.20070704
- changed license to LGPLv2

* Thu Jul  5 2007 Harald Hoyer <harald@redhat.com> - 1.1-1.20070704
- version 1.1-20070704

* Wed Jun 27 2007 Harald Hoyer <harald@redhat.com> - 1.1-1.20070604
- dialog-1.1-20070604

* Wed Feb 28 2007 Harald Hoyer <harald@redhat.com> - 1.1-1.20070227svn
- version 1.1-20070227
- added devel subpackage
- specfile fixes (bug#225693)
- Resolves: rhbz#225693

* Wed Jan 17 2007 Harald Hoyer <harald@redhat.com> - 1.0.20060221-1
- version 1.0-20060221

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.20051107-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.20051107-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.20051107-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 16 2005 Harald Hoyer <harald@redhat.com> 1.0-20051107-1
- version 1.0-20051107

* Mon Apr 18 2005 Harald Hoyer <harald@redhat.com> 1.0-20050306-1
- version 1.0-20050306

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com> 1.0-20050206-1
- new version 1.0-20050206

* Tue Dec 21 2004 Harald Hoyer <harald@redhat.com> 1.0-20041219-1
- new version 1.0-20041219

* Wed Oct 20 2004 Harald Hoyer <harald@redhat.com> 1.0-20040731-3
- rlandry@redhat.com refined his patch (bug 136374)

* Tue Oct 19 2004 Harald Hoyer <harald@redhat.com> 1.0-20040731-2
- added patch from rlandry@redhat.com which removes extra trailing
  spaces (bug 136374)

* Fri Aug 27 2004 Harald Hoyer <harald@redhat.com> 1.0-20040731-1
- new version 1.0-20040731

* Thu Jul 29 2004 Harald Hoyer <harald@redhat.com> 1.0-20040728-1
- new version 1.0-20040728

* Wed Jul 28 2004 Harald Hoyer <harald@redhat.de> 1.0-20040721-1
- new version 1.0-20040721

* Wed Jun 23 2004 Harald Hoyer <harald@redhat.de> 0.9b.20040606-1
- new version 0.9b-20040606
- new Version scheme

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec 08 2003 Harald Hoyer <harald@redhat.de> 0.9b-20031207.1
- version 20031207

* Thu Nov 27 2003 Harald Hoyer <harald@redhat.de> 0.9b-20031126.1
- version 20031126

* Mon Nov 24 2003 Harald Hoyer <harald@redhat.de> 0.9b-20031002.2
- added gettext BuildReq (#109192)

* Wed Oct  8 2003 Harald Hoyer <harald@redhat.de> 0.9b-20031002.1
- version 20031002

* Thu Sep 11 2003 Harald Hoyer <harald@redhat.de> 0.9b-20030910.1
- new version 20030910 which also fixes #104236

* Tue Aug 12 2003 Harald Hoyer <harald@redhat.de> 0.9b-20020814.5
- --with-ncursesw

* Fri Aug  8 2003 Elliot Lee <sopwith@redhat.com> 0.9b-20020814.4
- Rebuilt

* Tue Jun 17 2003 Harald Hoyer <harald@redhat.de> 0.9b-20020814.3
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 0.9b-20020814.2
- rebuild

* Tue Nov 05 2002 Harald Hoyer <harald@redhat.de> 0.9b-20020814.1
* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 22 2002 Harald Hoyer <harald@redhat.de> 0.9b-20020519.1
- update to dialog-0.9b-20020519

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 18 2001 Harald Hoyer <harald@redhat.de>
- update to 20010527
- added ncurses-devel dependency (#44733)
- removed perl dependency

* Tue Jan 09 2001 Harald Hoyer <harald@redhat.com>
- update to 20001217

* Mon Aug  7 2000 Bill Nottingham <notting@redhat.com>
- fix one of the examples (#14073)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Apr  5 2000 Bill Nottingham <notting@redhat.com>
- rebuild against current ncurses/readline

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Thu Jan 20 2000 Bill Nottingham <notting@redhat.com>
- fix loop patch for reading from pipe

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Thu May 7 1998 Michael Maher <mike@redhat.com> 
- Added Sean Reifschneider <jafo@tummy.com> patches for 
  infinite loop problems.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 15 1998 Erik Troan <ewt@redhat.com>
- built against new ncurses

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
