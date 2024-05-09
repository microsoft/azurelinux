Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:	A sophisticated file transfer program
Name:		lftp
Version:	4.9.2
Release:	2%{?dist}
License:	GPLv3+
Source0:	https://lftp.yar.ru/ftp/%{name}-%{version}.tar.xz
URL:		https://lftp.yar.ru/
BuildRequires:	ncurses-devel, gnutls-devel, perl-generators, pkgconfig, readline-devel, gettext
BuildRequires:	zlib-devel, gcc-c++
BuildRequires: desktop-file-utils

Patch1:  lftp-4.0.9-date_fmt.patch

%description
LFTP is a sophisticated ftp/http file transfer program. Like bash, it has job
control and uses the readline library for input. It has bookmarks, built-in
mirroring, and can transfer several files in parallel. It is designed with
reliability in mind.

%package scripts
Summary:	Scripts for lftp
Requires:	lftp >= %{version}-%{release}
BuildArch:	noarch

%description scripts
Utility scripts for use with lftp.

%prep
%setup -q

%patch 1 -p1 -b .date_fmt

#sed -i.rpath -e '/lftp_cv_openssl/s|-R.*lib||' configure
sed -i.norpath -e \
	'/sys_lib_dlsearch_path_spec/s|/usr/lib |/usr/lib /usr/lib64 /lib64 |' \
	configure

%build
%configure --with-modules --disable-static --with-gnutls --without-openssl --with-debug
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export tagname=CC
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/lftp/*
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/lftp/%{version}/*.so
iconv -f ISO88591 -t UTF8 NEWS -o NEWS.tmp
touch -c -r NEWS NEWS.tmp
mv NEWS.tmp NEWS
# Remove files from $RPM_BUILD_ROOT that we aren't shipping.
#rm $RPM_BUILD_ROOT%{_libdir}/lftp/%{version}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/liblftp-jobs.la
rm $RPM_BUILD_ROOT%{_libdir}/liblftp-tasks.la
rm $RPM_BUILD_ROOT%{_libdir}/liblftp-jobs.so
rm $RPM_BUILD_ROOT%{_libdir}/liblftp-tasks.so
desktop-file-install	\
--dir=%{buildroot}%{_datadir}/applications	\
%{buildroot}/%{_datadir}/applications/lftp.desktop

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%doc BUGS COPYING ChangeLog FAQ FEATURES README* NEWS THANKS TODO
%config(noreplace) %{_sysconfdir}/lftp.conf
%{_bindir}/*
%{_mandir}/*/*
%dir %{_libdir}/lftp
%dir %{_libdir}/lftp/%{version}
%{_libdir}/lftp/%{version}/cmd-torrent.so
%{_libdir}/lftp/%{version}/cmd-mirror.so
%{_libdir}/lftp/%{version}/cmd-sleep.so
%{_libdir}/lftp/%{version}/liblftp-network.so
%{_libdir}/lftp/%{version}/liblftp-pty.so
%{_libdir}/lftp/%{version}/proto-file.so
%{_libdir}/lftp/%{version}/proto-fish.so
%{_libdir}/lftp/%{version}/proto-ftp.so
%{_libdir}/lftp/%{version}/proto-http.so
%{_libdir}/lftp/%{version}/proto-sftp.so
%{_libdir}/liblftp-jobs.so.*
%{_libdir}/liblftp-tasks.so.*
%{_datadir}/applications/lftp.desktop
%{_datadir}/icons/hicolor/*/apps/*



%files scripts
%{_datadir}/lftp


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.9.2-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Aug 19 2020 Michal Ruprich <michalruprich@gmail.com> - 4.9.2-1
- New version 4.9.2

* Fri Apr 03 2020 Michal Ruprich <michalruprich@gmail.com> - 4.9.1-1
- New version 4.9.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 03 2020 Michal Ruprich <mruprich@redhat.com> - 4.9.0-1
- New version 4.9.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.8.4-3
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 01 2018 Michal Ruprich <mruprich@redhat.com> - 4.8.4-1
- New version 4.8.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 26 2018 Tomas Hozza <thozza@redhat.com> - 4.8.3-3
- Added gcc-c++ as an explicit BuildRequires

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 23 2017 Michal Ruprich <mruprich@redhat.com> - 4.8.3-1
- new version 4.8.3

* Mon Oct 09 2017 Michal Ruprich <mruprich@redhat.com> - 4.8.2-1
- new version 4.8.2

* Thu Sep 14 2017 Michal Ruprich <mruprich@redhat.com> - 4.8.1-1
- new version 4.8.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 14 2017 Michal Ruprich <mruprich@redhat.com> - 4.8.0-1
- new version 4.8.0

* Mon Mar 20 2017 Michal Ruprich <mruprich@redhat.com> - 4.7.7-1
- new version 4.7.7

* Mon Feb 20 2017 Michal Ruprich <mruprich@redhat.com> - 4.7.6-1
- new version 4.7.6

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.7.5-2
- Rebuild for readline 7.x

* Fri Jan 06 2017 Michal Ruprich <mruprich@redhat.com> - 4.7.5-1
- new version 4.7.5

* Mon Nov 28 2016 Michal Ruprich <mruprich@redhat.com> - 4.7.4-1
- new version 4.7.4

* Mon Jul 18 2016 Luboš Uhliarik <luhliari@redhat.com> - 4.7.3-1
- new version 4.7.3

* Thu May 19 2016 Luboš Uhliarik <luhliari@redhat.com> - 4.7.2-1
- new version 4.7.2

* Mon Apr 04 2016 Luboš Uhliarik <luhliari@redhat.com> - 4.7.1-1
- new version 4.7.1

* Wed Mar 30 2016 Luboš Uhliarik <luhliari@redhat.com> - 4.7.0-1
- new version 4.7.0

* Fri Feb 19 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 4.6.5-3
- Compile with "g++ -std=gnu++03" (F24FTBFS, RHBZ#1307711).

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Luboš Uhliarik <luhliari@redhat.com> - 4.6.5-1
- new version 4.6.5

* Mon Aug 24 2015 Luboš Uhliarik <luhliari@redhat.com> - 4.6.4-1
- new version 4.6.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.6.1-5
- Rebuilt for GCC 5 C++11 ABI change

* Thu Feb 26 2015 Tomas Hozza <thozza@redhat.com> - 4.6.1-4
- Don't auto accept remote host SSH fingerprint (new option auto-confirm) (#1180209)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 4.6.1-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Jan 13 2015 Tomas Hozza <thozza@redhat.com> - 4.6.1-2
- Fix mirror when there are multiple 302 redirections

* Mon Jan 05 2015 Tomas Hozza <thozza@redhat.com> - 4.6.1-1
- updated to latest upstream 4.6.1

* Tue Oct 14 2014 Jiri Skala <jskala@redhat.com> - 4.6.0-1
- updated to latest upstream 4.6.0

* Fri Sep 05 2014 Jiri Skala <jskala@redhat.com> - 4.5.5-1
- updated to latest upstream 4.5.5

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Jiri Skala <jskala@redhat.com> - 4.5.4-2
- corrected path to tarball in the spec file

* Thu Aug 07 2014 Jiri Skala <jskala@redhat.com> - 4.5.4-1
- updated to latest upstream 4.5.4

* Mon Jul 07 2014 Jiri Skala <jskala@redhat.com> - 4.5.3-1
- updated to latest upstream 4.5.3

* Thu Jun 12 2014 Jiri Skala <jskala@redhat.com> - 4.5.2-1
- updated to latest upstream 4.5.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Jiri Skala <jskala@redhat.com> - 4.5.1-1
- updated to latest upstream 4.5.1

* Fri May 23 2014 Jiri Skala <jskala@redhat.com> - 4.5.0-1
- updated to latest upstream 4.5.0

* Fri May 09 2014 Jiri Skala <jskala@redhat.com> - 4.4.16-1
- updated to latest upstream 4.4.16

* Mon Jan 27 2014 Jiri Skala <jskala@redhat.com> - 4.4.15-1
- updated to latest upstream 4.4.15

* Mon Jan 20 2014 Jiri Skala <jskala@redhat.com> - 4.4.14-2
- fixes #1045948 - adds new buildrequires zlib-devel

* Tue Dec 17 2013 Jiri Skala <jskala@redhat.com> - 4.4.14-1
- updated to latest upstream 4.4.14

* Thu Nov 28 2013 Jiri Skala <jskala@redhat.com> - 4.4.13-1
- updated to latest upstream 4.4.13
- added description of xfer:auto-rename option
- overwrite file when auto-rename and clobber options are enabled

* Mon Nov 18 2013 Jiri Skala <jskala@redhat.com> - 4.4.11-1
- updated to latest upstream 4.4.11

* Sat Oct 12 2013 Jiri Skala <jskala@redhat.com> - 4.4.10-1
- updated to latest upstream 4.4.10

* Wed Sep 04 2013 Jiri Skala <jskala@redhat.com> - 4.4.9-1
- updated to latest upstream 4.4.9

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.4.8-2
- Perl 5.18 rebuild

* Sat Jun 01 2013 Jiri Skala <jskala@redhat.com> - 4.4.8-1
- updated to latest upstream 4.4.8

* Fri May 24 2013 Jiri Skala <jskala@redhat.com> - 4.4.7-1
- updated to latest upstream 4.4.7

* Tue May 21 2013 Jiri Skala <jskala@redhat.com> - 4.4.6-1
- updated to latest upstream 4.4.6

* Fri Mar 15 2013 Jiri Skala <jskala@redhat.com> - 4.4.5-1
- updated to latest upstream 4.4.5

* Sun Feb 10 2013 Jiri Skala <jskala@redhat.com> - 4.4.3-1
- updated to latest upstream 4.4.3

* Mon Feb 04 2013 Jiri Skala <jskala@redhat.com> - 4.4.2-1
- updated to latest upstream 4.4.2

* Tue Jan 29 2013 Jiri Skala <jskala@redhat.com> - 4.4.1-1
- updated to latest upstream 4.4.1

* Mon Oct 01 2012 Jiri Skala <jskala@redhat.com> - 4.4.0-1
- updated to latest upstream 4.4.0

* Sun Jul 22 2012 Jiri Skala <jskala@redhat.com> - 4.3.8-1
- updated to latest upstream 4.3.8

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Jiri Skala <jskala@redhat.com> - 4.3.7-1
- updated to latest upstream 4.3.7

* Mon Apr 02 2012 Jiri Skala <jskala@redhat.com> - 4.3.6-1
- updated to latest upstream 4.3.6

* Tue Jan 24 2012 Jiri Skala <jskala@redhat.com> - 4.3.5-1
- updated to latest upstream 4.3.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 02 2012 Jiri Skala <jskala@redhat.com> - 4.3.4-1
- updated to latest upstream 4.3.4

* Wed Nov 16 2011 Jiri Skala <jskala@redhat.com> - 4.3.3-2
- fixes #666580 - Inaccurate timestamps

* Thu Oct 20 2011 Jiri Skala <jskala@redhat.com> - 4.3.3-1
- updated to latest upstream 4.3.3

* Tue Sep 20 2011 Jiri Skala <jskala@redhat.com> - 4.3.2-1
- updated to latest upstream 4.3.2

* Tue Jun 28 2011 Jiri Skala <jskala@redhat.com> - 4.3.1-1
- updated to latest upstream 4.3.1

* Mon Jun 20 2011 Jiri Skala <jskala@redhat.com> - 4.3.0-1
- updated to latest upstream 4.3.0

* Mon May 02 2011 Jiri Skala <jskala@redhat.com> - 4.2.3-1
- updated to latest upstream 4.2.3

* Tue Apr 12 2011 Jiri Skala <jskala@redhat.com> - 4.2.2-1
- updated to latest upstream 4.2.2

* Wed Mar 30 2011 Jiri Skala <jskala@redhat.com> - 4.2.1-1
- updated to latest upstream 4.2.1

* Mon Mar 14 2011 Jiri Skala <jskala@redhat.com> - 4.2.0-1
- updated to latest upstream 4.2.0
- fixes #675126 man page corrections

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Jiri Skala <jskala@redhat.com> - 4.1.3-1
- updated to latest upstream 4.1.3

* Mon Jan 03 2011 Jiri Skala <jskala@redhat.com> - 4.1.2-1
- updated to latest upstream 4.1.2

* Thu Dec 02 2010 Jiri Skala <jskala@redhat.com> - 4.1.1-1
- updated to latest upstream 4.1.1

* Tue Nov 23 2010 Jiri Skala <jskala@redhat.com> - 4.1.0-1
- updated to latest upstream 4.1.0

* Tue Sep 07 2010 Jiri Skala <jskala@redhat.com> - 4.0.10-1
- updated to latest upstream
- upstream changed tarball compression lzma -> xz

* Thu Jun 24 2010 Jiri Skala <jskala@redhat.com> - 4.0.9-3
- fixes issue when some servers require forcing SSL3.0
- corrected check for 'max time' used for fix #600218

* Tue Jun 22 2010 Jiri Skala <jskala@redhat.com> - 4.0.9-2
- fixes #600218 - [abrt] Process /usr/bin/lftp was killed by signal 1

* Mon Jun 14 2010 Jiri Skala <jskala@redhat.com> - 4.0.9-1
- updated to latest stable version

* Thu May 27 2010 Jiri Skala <jskala@redhat.com> - 4.0.8-1
- updated to latest stable version

* Wed May 05 2010 Jiri Skala <jskala@redhat.com> - 4.0.7-1
- updated to latest stable version

* Thu Apr 01 2010 Jiri Skala <jskala@redhat.com> - 4.0.6-1
- updated to latest stable version
- added man lftp.conf

* Thu Mar 04 2010 Jiri Skala <jskala@redhat.com> - 4.0.5-2
- fixes #566562 - lftp doesn't properly implement CCC

* Thu Feb 04 2010 Jiri Skala <jskala@redhat.com> - 4.0.5-1
- updated to latest stable version

* Sun Nov 22 2009 Jiri Skala <jskala@redhat.com> - 4.0.4-1
- updated to latest stable version

* Sun Oct 18 2009 Jiri Skala <jskala@redhat.com> - 4.0.2-1
- updated to latest stable version

* Mon Sep 14 2009 Jiri Skala <jskala@redhat.com> - 4.0.0-1
- updated to latest stable version

* Wed Sep 02 2009 Jiri Skala <jskala@redhat.com> - 3.7.15-1
- updated to latest upstream release

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 3.7.14-6
- Use lzma compressed upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Adam Jackson <ajax@redhat.com> 3.7.14-4
- Split utility scripts to subpackage to isolate perl dependency. (#510813)

* Wed Jun 10 2009 Jiri Skala <jskala@redhat.com> - 3.7.14-3
- fixed bug in ls via http - corrupted file names containing spaces

* Fri May 22 2009 Jiri Skala <jskala@redhat.com> - 3.7.14-1
- rebase to latest upstream release; among others fixes #474413

* Tue Apr 14 2009 Jiri Skala <jskala@redhat.com> - 3.7.11-3
- release number repaired

* Tue Apr 14 2009 Jiri Skala <jskala@redhat.com> - 3.7.11-1
- rebase to latest upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Jiri Skala <jskala@redhat.com> - 3.7.7-1
- rebase to latest upstream version
- resolves license conflict GPLv2 -> GPLv3+ due to gnulib

* Mon Sep 29 2008 Jiri Skala <jskala@redhat.com> - 3.7.4-1
- Resolves: #464420 re-base to 3.7.4
- replaced usage of OpenSSL by GNUTLS due to license conflict

* Wed Apr 23 2008 Martin Nagy <mnagy@redhat.com> - 3.7.1-1
- update to upstream version 3.7.1

* Thu Feb 28 2008 Martin Nagy <mnagy@redhat.com> - 3.6.3-2
- fix rpath

* Mon Feb 25 2008 Martin Nagy <mnagy@redhat.com> - 3.6.3-1
- update to newest version
- remove patches fixed in upstream: progress_overflow, empty_argument

* Tue Feb 12 2008 Martin Nagy <mnagy@redhat.com> - 3.6.1-2
- fix library paths (#432468)

* Mon Feb 11 2008 Martin Nagy <mnagy@redhat.com> - 3.6.1-1
- upgrade to upstream version 3.6.1
- remove rpath and make some spec file changes for review (#225984)
- remove old patches
- fix core dumping when html tag has its argument empty
- use own libtool

* Thu Dec 13 2007 Martin Nagy <mnagy@redhat.com> - 3.5.14-3
- Fixed coredumping when downloading (#414051)

* Tue Dec 04 2007 Martin Nagy <mnagy@redhat.com> - 3.5.14-2.1
- rebuild

* Mon Sep 17 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.14-2
- rebase
- deleted symlinks liblftp-jobs.so & liblftp-tasks.so

* Thu Sep 06 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.10-4
- rebuild

* Wed Apr 11 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.10-3
- Correct mistake removing devel package & calling chkconfig
- Resolves #235436
- Removing automake autoconf
- Resolves #225984

* Wed Apr 04 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.10-2
- Merge review fix
- Resolves #225984

* Wed Apr 04 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.10
- Upgrade to 3.5.10 from upstream

* Thu Jan 18 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.9
- Upgrade to 3.5.9 from upstream 

* Wed Aug 23 2006 Maros Barabas <mbarabas@redhat.com> - 3.5.1-2
- remove .a & .la from libdir

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 3.5.1-1.fc6
- Upgrade to 3.5.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.4.7-2.FC6.1
- rebuild

* Mon Jun 12 2006 Jason Vas Dias <jvdias@redhat.com> - 3.4.7-2
- Add BuildRequires for broken Brew

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 3.4.7-1
- Upgrade to upstream version 3.4.7

* Fri Apr 28 2006 Jason Vas Dias <jvdias@redhat.com> - 3.4.6-1
- Upgrade to upstream version 3.4.6

* Fri Apr 21 2006 Jason Vas Dias <jvdias@redhat.com> - 3.4.4-1
- Upgrade to upstream version 3.4.4

* Thu Mar 16 2006 Jason Vas Dias <jvdias@redhat.com> - 3.4.3-1
- Upgrade to upstream version 3.4.3

* Fri Mar 10 2006 Bill Nottingham <notting@redhat.com> - 3.4.2-5
- rebuild for ppc TLS issue (#184446)

* Thu Feb 16 2006 Jason Vas Dias<jvdias@redhat.com> - 3.4.2-4
- Apply upstream fix for bug 181694.

* Wed Feb 15 2006 Jason Vas Dias<jvdias@redhat.com> - 3.4.2-2
- fix bug 181694: segfault on redirection to non-existent location

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.4.2-1.1
- bump again for double-long bug on ppc(64)

* Wed Feb 08 2006 Jason Vas Dias<jvdias@redhat.com> - 3.4.2-1
- Upgrade to upstream version 3.4.2, that fixes 3.4.1's coredump

* Tue Feb 07 2006 Jason Vas Dias<jvdias@redhat.com> - 3.4.1-1
- Upgrade to upstream version 3.4.1
- fix core dump

* Fri Jan 13 2006 Jason Vas Dias<jvdias@redhat.com> - 3.4.0-1
- Upgrade to upstream version 3.4.0

* Wed Dec 21 2005 Jason Vas Dias<jvdias@redhat.com> - 3.3.5-4
- fix bug 176315: openssl libraries not being picked up - gnutls was instead
- improvements to bug 172376 fix

* Tue Dec 20 2005 Jason Vas Dias<jvdias@redhat.com> - 3.3.5-2
- fix bug 176175: perl-String-CRC32 now in separate RPM 

* Thu Dec 15 2005 Jason Vas Dias<jvdias@redhat.com> - 3.3.5-1
- Upgrade to version 3.3.5
- fix bug bz172376 : host lookups should use any address found after timeout 

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Jason Vas Dias <jvdias@redhat.com> - 3.3.3-1
- Upgrade to upstream 3.3.3 release, fixing bug 171884 .

* Tue Oct 18 2005 Jason Vas Dias <jvdias@redhat.com> - 3.3.2-1
- *** PLEASE COULD ANYONE MODIFYING lftp TEST IT BEFORE SUBMITTING! ***
  (and preferably contact the lftp package maintainer (me) first - thank you!)
  bug 171096 : 'mget files in lftp causes abort' (core dump actually)
  resulted from not doing so .
  See https://lftp.yar.ru :
	Recent events:2005-10-17: 
	lftp-3.3.2 released. Fixed a coredump caused by double-free.

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com> - 3.3.1-1
- 3.3.1

* Wed Aug 24 2005 Jason Vas Dias <jvdias@redhat.com> - 3.3.0-1
- Upgrade to upstream version 3.3.0

* Mon Aug  8 2005 Tomas Mraz <tmraz@redhat.com> - 3.2.1-2
- rebuild with new gnutls

* Thu Jun 30 2005 Warren Togami <wtogami@redhat.com> 3.2.1-1
- 3.2.1

* Mon Apr 25 2005 Jason Vas Dias <jvdias@redhat.com> 3.1.3-1
- Upgrade to upstream version 3.1.3

* Tue Mar  8 2005 Jason Vas Dias <jvdias@redhat.com> 3.1.0-1
- Upgrade to upstream verson 3.1.0; remove patch for broken libtool

* Tue Mar  8 2005 Joe Orton <jorton@redhat.com> 3.0.13-2
- rebuild

* Fri Jan 21 2005 Jason Vas Dias <jvdias@redhat.com> 3.0.13-1
- Upgrade to upstream version 3.0.13 .

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 3.0.6-4
- Rebuilt for new readline.

* Mon Oct 18 2004 Jason Vas Dias <jvdias@redhat.com> 3.0.6-3
- rebuilding for current FC3 glibc fixes bug 136109
 
* Mon Aug 16 2004 Nalin Dahyabhai <nalin@redhat.com> 3.0.6-2
- rebuild

* Tue Jun 15 2004 Nalin Dahyabhai <nalin@redhat.com> 3.0.6-1
- update to 3.0.6

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 12 2004 Nalin Dahyabhai <nalin@redhat.com> 2.6.12-1
- update to 2.6.12

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.6.10-3
- add patch to avoid DoS when connecting to HTTP servers (or "HTTP" "servers")
  which don't provide status headers, or provide empty lines instead of status
  headers

* Fri Dec 12 2003 Nalin Dahyabhai <nalin@redhat.com> 2.6.10-2
- rebuild

* Fri Dec 12 2003 Nalin Dahyabhai <nalin@redhat.com> 2.6.10-1
- update to 2.6.10, which folds in the previous patches
- configure with --with-debug so that we get useful debug info

* Tue Dec  9 2003 Nalin Dahyabhai <nalin@redhat.com> 2.6.9-1
- include patch based on patch from Ulf Härnhammar to fix unsafe use of
  sscanf when reading http directory listings (CAN-2003-0963)
- include patch based on patch from Ulf Härnhammar to fix compile warnings
  modified based on input from Solar Designer

* Mon Dec  8 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.6.9

* Wed Aug  6 2003 Elliot Lee <sopwith@redhat.com>
- Fix libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.6.3-2
- rebuild

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- use openssl's pkg-config data, if available

* Thu Nov 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.6.3-1
- update to 2.6.3

* Tue Nov 12 2002 Tim Powers <timp@redhat.com> 2.6.2-2
- remove files we aren't including from the $$RPM_BUILD_ROOT

* Fri Oct  4 2002 Nalin Dahyabhai <nalin@redhat.com> 2.6.2-1
- build with the system's libtool

* Thu Sep 26 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.6.2

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 2.5.2-4
- build using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.5.2-3
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com> 2.5.2-2
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 2.5.2-1
- update to 2.5.2

* Fri Feb 22 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.9-1
- update to 2.4.9

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.8-1
- update to 2.4.8

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 2.4.0-3
- automated rebuild

* Thu Aug 16 2001 Nalin Dahyabhai <nalin@redhat.com> 2.4.0-2
- remove the .la files from the final package -- these aren't libraries
  people link with anyway

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com> 2.4.0-1
- update to 2.4.0 (fixes some memory leaks and globbing cases)

* Thu Jul  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- langify

* Fri Jun 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- explicitly list the modules which are built when the package compiles, so
  that module build failures (for whatever reason) get caught

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- merge in changes from ja .spec file

* Wed May 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.3.11

* Fri Apr 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.3.9

* Fri Mar  2 2001 Tim Powers <timp@redhat.com>
- rebuilt against openssl-0.9.6-1

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.3.7

* Thu Jan  4 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.3.6

* Fri Dec  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.3.5

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Thu Jul 13 2000 Tim Powers <timp@redhat.com>
- patched to build with gcc-2.96
- use gcc instead of c++ for CXX, otherwise you expose an ICE in gcc when
  using g++ on two files, one being a C++ source, and the other a C source.
  Using gcc does the correct thing.

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jun 8 2000 Tim Powers <timp@redhat.com>
- fix man page location
- use %%makeinstall
- use predefined macros wherever possible

* Mon May 15 2000 Tim Powers <timp@redhat.com>
- updated to 2.2.2
- added locales tofiles list
- built for 7.0

* Thu Jan 27 2000 Tim Powers <timp@redhat.com>
- fixed package description etc.

* Fri Jan 21 2000 Tim Powers <timp@redhat.com>
- ughh. didn't include /usr/lib/lftp in files list, fixed

* Thu Jan 13 2000 Tim Powers <timp@redhat.com>
- initial build for Powertools
