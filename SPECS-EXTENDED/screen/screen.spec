%bcond_with multiuser
%global _hardened_build 1

Summary:        A screen manager that supports multiple logins on one terminal
Name:           screen
Version:        4.9.1
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gnu.org/software/screen
Source0:        https://ftp.gnu.org/gnu/screen/screen-%{version}.tar.gz
Source1:        screen.pam
Patch1:         screen-4.3.1-libs.patch
Patch2:         screen-4.3.1-screenrc.patch
Patch3:         screen-E3.patch
Patch4:         screen-4.3.1-suppress_remap.patch
Patch5:         screen-4.3.1-crypt.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libutempter-devel
BuildRequires:  ncurses-devel
BuildRequires:  pam-devel
# for %%_tmpfilesdir macro
BuildRequires:  systemd
BuildRequires:  texinfo
Requires(pre):  %{_sbindir}/groupadd

%description
The screen utility allows you to have multiple logins on just one
terminal. Screen is useful for users who telnet into a machine or are
connected via a dumb terminal, but want to use more than just one
login.

Install the screen package if you need a screen manager that can
support multiple logins on one terminal.

%prep
%autosetup -p1

%build
autoreconf -i

%configure \
	--enable-pam \
	--enable-colors256 \
	--enable-rxvt_osc \
	--enable-use-locale \
	--enable-telnet \
	--with-pty-mode=0620 \
	--with-pty-group=$(getent group tty | cut -d : -f 3) \
	--with-sys-screenrc="%{_sysconfdir}/screenrc" \
	--with-socket-dir="%{_rundir}/screen"

# We would like to have braille support.
sed -i -e 's/.*#.*undef.*HAVE_BRAILLE.*/#define HAVE_BRAILLE 1/;' config.h

sed -i -e 's/\(\/usr\)\?\/local\%{_sysconfdir}/\%{_sysconfdir}/g;' doc/screen.{1,texinfo}

for i in doc/screen.texinfo; do
    iconv -f iso8859-1 -t utf-8 < $i > $i.utf8 && mv -f ${i}{.utf8,}
done

rm -f doc/screen.info*

# fails with %{?_smp_mflags}
make

%install
make install DESTDIR=%{buildroot}
mv -f %{buildroot}%{_bindir}/screen{-%{version},}

mkdir -p %{buildroot}%{_sysconfdir}
install -m 0644 etc/etcscreenrc %{buildroot}%{_sysconfdir}/screenrc
cat etc/screenrc >> %{buildroot}%{_sysconfdir}/screenrc

# Better not forget to copy the pam file around
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/screen

# Create the socket dir
mkdir -p %{buildroot}%{_rundir}/screen

# And tell systemd to recreate it on start with tmpfs
mkdir -p %{buildroot}%{_tmpfilesdir}
cat <<EOF > %{buildroot}%{_tmpfilesdir}/screen.conf
# screen needs directory in /run
%if %{with multiuser}
d %{_rundir}/screen 0755 root root
%else
d %{_rundir}/screen 0775 root screen
%endif
EOF

# Remove files from the buildroot which we don't want packaged
rm -f %{buildroot}%{_infodir}/dir

%pre
%{_sbindir}/groupadd -g 84 -r -f screen
:

%files
%doc README doc/FAQ doc/README.DOTSCREEN ChangeLog
%license COPYING
%{_mandir}/man1/screen.*
%{_infodir}/screen.info*
%{_datadir}/screen
%config(noreplace) %{_sysconfdir}/screenrc
%config(noreplace) %{_sysconfdir}/pam.d/screen
%{_tmpfilesdir}/screen.conf
%if %{with multiuser}
%attr(4755,root,root) %{_bindir}/screen
%attr(755,root,root) %{_rundir}/screen
%else
%attr(2755,root,screen) %{_bindir}/screen
%attr(775,root,screen) %{_rundir}/screen
%endif

%changelog
* Thu Aug 31 2023 Muhammad Falak <mwani@microsoft.com> - 4.9.1-1
- Upgrade version to adress CVE-2021-20230
- Lint spec

* Wed Nov 09 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.9.0-1
- Auto-upgrade to 4.9.0 - CVE-2021-26937

* Tue Mar 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.8.0-4
- Using "autoreconf -i" to fix build issues.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.8.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 24 2020 Vaclav Dolezal <vdolezal@redhat.com> - 4.8.0-2
- fix insufficient size of struct display::d_xtermosc

* Fri Feb 07 2020 Vaclav Dolezal <vdolezal@redhat.com> - 4.8.0-1
- New upstream release 4.8.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Vaclav Dolezal <vdolezal@redhat.com> - 4.7.0-1
- New upstream release 4.7.0 (#1757638)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 4.6.2-7
- Rebuilt for libcrypt.so.2 (#1666033)

* Thu Aug 16 2018 Václav Doležal <vdolezal@redhat.com> - 4.6.2-6
- Change license in .spec to GPLv3+

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 Josef Ridky <jridky@redhat.com> - 4.6.2-4
- Add gcc dependency

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 4.6.2-2
- Rebuilt for switch to libxcrypt

* Wed Nov 08 2017 Josef Ridky <jridky@redhat.com> - 4.6.2-1
- New upstream release 4.6.2 (#1508250)
- Remove xterm patch (#1493505)

* Sun Sep 10 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 4.6.1-4
- Cleanup spec

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 11 2017 Josef Ridky <jridky@redhat.com> - 4.6.1-1
- New upstream release 4.6.1 (#1469323)

* Thu Jun 29 2017 Josef Ridky <jridky@redhat.com> - 4.6.0-1
- New upstream release 4.6.0 (#1466080)

* Thu May 25 2017 Josef Ridky <jridky@redhat.com> - 4.5.1-2
- fix typos in info doc file (#1434671)
- fix screenrc configuration to cover xterm-* terminals (#1428337)
- update spec file (#1429174)

* Wed Mar 01 2017 Josef Ridky <jridky@redhat.com> - 4.5.1-1
- New upstream release 4.5.1 (#1426871)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Josef Ridky <jridky@redhat.com> - 4.5.0-1
- New upstream release 4.5.0 (#1414185)

* Wed Nov  2 2016 Josef Ridky <jridky@redhat.com> - 4.4.0-4
- revert changes from previous update (4.4.0-3)

* Tue Sep 20 2016 Josef Ridky <jridky@redhat.com> - 4.4.0-3
- fix problem with deleting multiple lines by pressing ctrl+arrow keys (#1123369)

* Wed Sep 14 2016 Josef Ridky <jridky@redhat.com> - 4.4.0-2
- fix problem with crash on new window when the terminal type is very long (#1350549)
- upstream fix terminal type length in option parsing

* Wed Jun 22 2016 Petr Hracek <phracek@redhat.com> - 4.4.0-1
- New upstream release 4.4.0 (#1348015)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 31 2015 Petr Hracek <phracek@redhat.com> - 4.3.1-3
- Remove NEWS file, Change COPYING to LICENSE (#1242963)

* Tue Jul 21 2015 Petr Hracek <phracek@redhat.com> - 4.3.1-2
- Packaging ChangeLog (#1242963)

* Tue Jun 30 2015 Petr Hracek <phracek@redhat.com> - 4.3.1-1
- New upstream version 4.3.1 (#1237109)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Petr Hracek <phracek@redhat.com> - 4.2.1-5
- Rebuild because of rpm (#1212918)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 23 2014 Rex Dieter <rdieter@fedoraproject.org> 4.2.1-3
- comply with http://fedoraproject.org/wiki/Packaging:Tmpfiles.d (#1112016)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Petr Hracek <phracek@redhat.com> - 4.2.1-1
- New upstream version (#1090031)

* Fri Apr 18 2014 Petr Hracek <phracek@redhat.com> - 4.1.0-0.19.20120314git3c2946
- Screen installs content to /var/run (#1053195)

* Tue Apr 08 2014 Petr Hracek <phracek@redhat.com> - 4.1.0-0.18.20120314git3c2946
- Man page update (#1023953)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-0.17.20120314git3c2946
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Petr Hracek <phracek@redhat.com> - 4.1.0-0.16.20120314git3c2946
- Fix: Segfault in alternate screen handling (#948617)

* Fri Apr 05 2013 Petr Hracek <phracek@redhat.com> - 4.1.0-0.15.20120314git3c2946
- correct missing help options

* Tue Feb 05 2013 Petr Hracek <phracek@redhat.com> - 4.1.0-0.14.20120314git3c2946
- Fix (#907472) xterm too long - sorry

* Wed Dec 05 2012 Lukáš Nykrýn <lnykryn@redhat.com> - 4.1.0-0.13.20120314git3c2946
- Use hardened build

* Mon Sep 03 2012 Lukáš Nykrýn <lnykryn@redhat.com> - 4.1.0-0.12.20120314git3c2946
- PIE and RELRO (#853191)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-0.11.20120314git3c2946
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 28 2012 Lukáš Nykrýn <lnykryn@redhat.com> - 4.1.0-0.10.20120314git3c2946
- check crypt output (#815605)

* Wed Mar 28 2012 Lukáš Nykrýn <lnykryn@redhat.com> - 4.1.0-0.9.20120314git3c2946
- fix for resuming screen in screen (#752622)

* Wed Mar 14 2012 Lukáš Nykrýn <lnykryn@redhat.com> - 4.1.0-0.8.20120314git3c2946
- rebase to latest git snapshot
- fix a crash when switching from altscreen after window resize (#784504)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-0.7.20110819git450e8f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Lukáš Nykrýn <lnykryn@redhat.com> - 4.1.0-0.6.20110819git450e8f
- rebase to latest git snapshot

* Tue Dec 20 2011 Lukáš Nykrýn <lnykryn@redhat.com> - 4.1.0-0.5.20110328git8cf5ef
- fix for nonworking ^a backspace (#708698)

* Tue Jul 19 2011 Miroslav Lichvar <mlichvar@redhat.com> - 4.1.0-0.4.20110328git8cf5ef
- update to git snapshot 20110328git8cf5ef
- clear scrollback buffer before locking linux terminal (#683733)

* Thu Feb 10 2011 Miroslav Lichvar <mlichvar@redhat.com> - 4.1.0-0.3.20101110git066b098
- move sockets back to /var/run/screen (#676663)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-0.2.20101110git066b098
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Miroslav Lichvar <mlichvar@redhat.com> - 4.1.0-0.1.20101110git066b098
- update to git snapshot 20101110git066b098
- fix potential problems for Common Criteria certification
- apply some xterm tweaks in default config also to xterm-* (#474064)
- change socket directory to $HOME/.screen (#667252)
- add bcond macro to build with multiuser support
- convert info to UTF-8

* Fri Nov 12 2010 Miroslav Lichvar <mlichvar@redhat.com> - 4.0.3-16
- create socket directory on start with tmpfs (#652348)
- add -4 and -6 options to man page (#650321)

* Fri Sep 25 2009 Miroslav Lichvar <mlichvar@redhat.com> - 4.0.3-15
- fix crash when resizing (#515055)
- try to improve default config (#523647, #506256, #492729)
- suppress install-info errors (#515999)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri May 16 2008 Miroslav Lichvar <mlichvar@redhat.com> - 4.0.3-12
- fix multiuser support (#446049)
- fix building with new autoconf

* Mon Apr 07 2008 Miroslav Lichvar <mlichvar@redhat.com> - 4.0.3-11
- don't include stropts.h (#440803)
- fix compiler warnings in ipv6 patch

* Tue Feb 26 2008 Miroslav Lichvar <mlichvar@redhat.com> - 4.0.3-10
- don't set xterm function keys in default config (#151556)
- always return 0 in scriptlet (#433882)
- fix pty permissions
- enable utempter support
- link with libtinfo, don't link with libutil
- spec cleanup

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.0.3-9
- Autorebuild for GCC 4.3

* Fri Aug 24 2007 Marcela Maslanova <mmaslano@redhat.com> - 4.0.3-8
- check licence & rebuilt for mass rebuild
- add gawk to requires

* Tue May 22 2007 Marcela Maslanova <mmaslano@redhat.com> - 4.0.3-7
- revert binding (patch9)
- Resolves: rhbz#238122

* Mon Mar 26 2007 Marcela Maslanova <mmaslano@redhat.com> - 4.0.3-5
- rebuilt (change in spec file)

* Mon Mar 19 2007 Marcela Maslanova <mmaslano@redhat.com> - 4.0.3-4
- rebuilt (change in spec file)

* Tue Feb 6 2007 Marcela Maslanova <mmaslano@redhat.com> - 4.0.3-3
- rebuilt (change in spec file)

* Fri Jan 5 2007 Marcela Maslanova <mmaslano@redhat.com> - 4.0.3-2
- rebuilt (change in spec file)

* Sun Oct 15 2006 Marcela Maslanova <mmaslano@redhat.com> - 4.0.3-1
- new version from upstream
- ipv6 patch #198410

* Wed Aug 16 2006 Jesse Keating <jkeating@redhat.com> - 4.0.2-16
- Don't use %%makeinstall, instead make install.
- Change DDESTDIR to DESTDIR to do the right thing.
- Comment out utf patch as it is no longer necessary.
- Add dist tag
- Change PreReq to correct Requires(pre), Requires(post), Requires(preun) 
- Don't use RPM_SOURCE_DIR, reference the source file directly
- Do the compiling (make) in %%build, not %%install
- Don't replace /etc/screenrc if the user has modified it
- Ditto /etc/pam.d/screen
- Change the buildroot to follow guidelines

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.0.2-15.1
- rebuild

* Mon Jul 10 2006 Petr Rockai <prockai@redhat.com> - 4.0.2-15
- bump MAXSTR (string buffer size) to 4k (from 256 bytes), fixes
  status line issues with window list in status line and too many
  windows (and possibly other issues with long strings)

* Tue May 30 2006 Petr Rockai <prockai@redhat.com> - 4.0.2-14
- put /usr/share/screen into the package (so the package owns the
  directory as well, not only the files below); fixes BR 192852

* Fri Feb 24 2006 Petr Rockai <prockai@redhat.com> - 4.0.2-12
- detect libutil(s).a even if it is only present in lib64 (#182407)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.0.2-11.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.0.2-11.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Petr Rockai <prockai@redhat.com> - 4.0.2-11
- change the default lockscreen shortcut to ^aX to make
  it harder to hit by accident, as per BR 157821

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 10 2005 Tomas Mraz <tmraz@redhat.com> - 4.0.2-10
- use include instead of pam_stack in pam config

* Fri May 27 2005 Bill Nottingham <notting@redhat.com> - 4.0.2-9
- don't use utmp group for socket dir; use a dedicated screen gid

* Tue Mar 29 2005 Petr Rockai <prockai@redhat.com> - 4.0.2-8
- fix BR 150392 by implementing the setgid/utmp scheme for socket directory

* Wed Mar 02 2005 Petr Rockai <prockai@redhat.com> - 4.0.2-7
- rebuild

* Tue Feb 15 2005 Petr Rockai <prockai@redhat.com> - 4.0.2-6
- fix BR 136234 by carrying out the suggested change in /etc/screenrc
- drop screen-4.0.2-logname.patch (merged into screen-4.0.2-screenrc.patch)
- grant wish 130674 by adding a (commented out) caption statement to default
  screenrc

* Fri Sep 10 2004 Warren Togami <wtogami@redhat.com> 4.0.2-5
- #132321 and some minor spec cleanups

* Fri Aug  6 2004 Daniel Reed <djr@redhat.com> 4.0.2-4
- remove extra entries in "sources" file

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 28 2004 Daniel Reed <djr@redhat.com> 4.0.2-2
- Add patch -logname to correct #121875

* Mon Apr 05 2004 Daniel Reed <djr@redhat.com> 4.0.2-1
- Version bump (4.0.2)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Lon Hohberger <lhh@redhat.com> 4.0.1-3
- Rebuild

* Mon Dec 08 2003 Lon Hohberger <lhh@redhat.com> 4.0.1-2
- Build for Fedora

* Mon Dec 08 2003 Lon Hohberger <lhh@redhat.com> 4.0.1-1
- Import of 4.0.1 from upstream.
- Removed screen-homedir hack introduced in 3.9.15-8.  (I
was unable to reproduce the behavior described in #98320,
and thus, the patch isn't necessary.)
- Fix for buffer overflow from Timo Strainen (patch 7).
- Fix for #111084 - we now require texinfo to build.
- Comment out lines in screenrc causing screen to complain
at startup.

* Thu Jul 10 2003 Lon Hohberger <lhh@redhat.com> 3.9.15-11
- Rebuilt 

* Thu Jul 10 2003 Lon Hohberger <lhh@redhat.com> 3.9.15-10
- Put the bindkey back in for now.

* Tue Jul 01 2003 Lon Hohberger <lhh@redhat.com> 3.9.15-9
- Rebuilt

* Tue Jul 01 2003 Lon Hohberger <lhh@redhat.com> 3.9.15-8
- Change screen's behavior to do the following: Attempt to use
~/.screen as the screen directory.  Failing that (ie, on files
systems without Unix sockets support), try using /tmp/screen-<USER>.
This prevents a user from creating /tmp/screens (which inherits
the sticky bit from /tmp, preventing other users from using screen),
as well as *tries* to be more secure.

* Tue Jul 01 2003 Lon Hohberger <lhh@redhat.com> 3.9.15-7
- Rebuilt

* Tue Jul 01 2003 Lon Hohberger <lhh@redhat.com> 3.9.15-6
- Disable system-wide read/write dir in /tmp; use user's ~/.screen
directory for screen sessions. (#98320)

* Mon Jun 16 2003 Lon Hohberger <lhh@redhat.com> 3.9.15-5
- Rebuilt

* Fri Jun 13 2003 Lon Hohberger <lhh@redhat.com> 3.9.15-4
- Removed bindkey entry; stty `tput kbs` sets this correctly for
the screen terminal type.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 16 2003 Lon Hohberger <lhh@redhat.com> 3.9.15-2
- Rebuilt

* Wed Apr 16 2003 Lon Hohberger <lhh@redhat.com> 3.9.15-1
- Import of 3.9.15 from upstream.

* Fri Feb 14 2003 Lon Hohberger <lhh@redhat.com> 3.9.13-5
- Closes a potential window to raise the warning noted
in #84232.

* Fri Feb 14 2003 Lon Hohberger <lhh@redhat.com> 3.9.13-4
- Fix for #84232

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 05 2002 Lon Hohberger <lhh@redhat.com> 3.9.13-2
- Fixed up patches; aggregated screenrc + status patches into one
for build 2.

* Thu Dec 05 2002 Lon Hohberger <lhh@redhat.com> 3.9.13-1
- Import of 3.9.13 source tree.  UTF-8 no longer dooms us.

* Mon Dec 02 2002 Lon Hohberger <lhh@redhat.com> 3.9.11-14
- Fix for #78423

* Tue Nov 12 2002 Lon Hohberger <lhh@redhat.com> 3.9.11-13
- Fixed Makefile, bumped to 3.9.11-13

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 3.9.11-12
- obey RPM_OPT_FLAGS always

* Mon Nov 11 2002 Bill Nottingham <notting@redhat.com>
- remove hardcoded paths from pam config file

* Wed Aug 14 2002 Philip Copeland <bryce@redhat.com> 3.9.11-10
- #65344 - doomed by utf8

* Mon Aug 12 2002 Philip Copeland <bryce@redhat.com> 3.9.11-9
- #60597 - what /shall/ we make the defaults today?

* Wed Jul 17 2002 Philip Copeland <bryce@redhat.com> 3.9.11-8
- Prevent the makefile from stripping the binary
- Really get rid of the libelf dependancy

* Thu Jun 27 2002 Philip Copeland <bryce@redhat.com> 3.9.11-7
- Get rid of libelf dependancy

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 3.9.11-6
- automated rebuild

* Tue May 28 2002 Philip Copeland <bryce@redhat.com> 3.9.11-5
- Missing bindkey to allow backspace to work
- Rebuilt due to rpm bug

* Thu Apr 18 2002 Bill Nottingham <notting@redhat.com>
- fix starting in non-en_US locales (#61835)

* Mon Apr 15 2002 Philip Copeland <bryce@redhat.com>
- Various fixups including remembering to enable pam support

* Sat Feb 16 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.9.11
- patch0/patch4 is not necessary anymore
- do not compress man-pages/info-files in spec file
- use configure to set telnet/screenrc instead of sed
- add a hack to correctly install the new screenencodings
- try to build up a better global /etc/screenrc instead of
  /etc/skel/.screenrc

* Fri Aug  3 2001 Crutcher Dunnavant <crutcher@redhat.com> 3.9.9-3
- fixed screenrc path sed command; #50046
- added ncurses-devel build dep; #49692
- fix typo in specfile that broke screenrc, #49535

* Tue Jul 10 2001 Tim Powers <timp@redhat.com>
- gzip manpage

* Mon Jun 25 2001 Crutcher Dunnavant <crutcher@redhat.com>
- itterate to 3.9.9
- fixed FAQ
- added electro@mrduck.net's PAM patch, crazy :)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Feb 13 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix configure.in to use correct code to check for select()

* Wed Jan 10 2001 Tim Waugh <twaugh@redhat.com>
- Rebuild, which will hopefully fix bug #22537

* Sun Oct 01 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.9.8
- change the .jbj patch and add some more "user" -> "auser" cases

* Tue Aug 15 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Patched the documentation to change the 'C-a C-\' to 'C-a \',
- which is what is the real behaviour. this fixes bug #16103

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Fixed my fix, so that the hack goes in the /global/ file :)

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Stuck an entry into the default screenrc file that forces
- '^?' (backspace) to send '^H'.
- Its an ugly fix for a termcap inheritance problem,
- but it works, if anyone REALLY needs '^?' they can change it,
- and I think we anger less people with this than the way it 
- currently behaves. (Read: vi and emacs work now)
- POST NOTE (Aug 15): emacs is NOT happy with ^H, BUT screen thinks
- that this is what backspace is supposed to do, so we don't change it.

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Fixed some conflicting descriptions in the documentation

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- got a patch from rzm@icm.edu.pl to fix bug #10353
- which caused screen to crash when copying to a file buffer

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- rebuild, FHS tweaks

* Sat May  6 2000 Bill Nottingham <notting@redhat.com>
- fix build for ia64

* Mon Apr  3 2000 Bernhard Rosenkränzer <bero@redhat.com>
- rebuild with new ncurses

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Tue Feb 15 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix MD5 password support (Bug #9463)

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Fri Dec 10 1999 Bill Nottingham <notting@redhat.com>
- update to 3.9.5

* Wed Oct 20 1999 Bill Nottingham <notting@redhat.com>
- you know, we weren't just patching in Unix98 pty support for fun.

* Wed Aug 18 1999 Bill Nottingham <notting@redhat.com>
- put screendir in ~

* Wed Aug 18 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.9.4.

* Wed Jun 16 1999 Bill Nottingham <notting@redhat.com>
- force tty permissions/group

* Sat Jun 5 1999 Dale Lovelace <dale@redhat.com>
- permissions on /etc/skel/.screenrc to 644

* Mon Apr 26 1999 Bill Nottingham <notting@redhat.com>
- take out warning of directory permissions so root can still use screen

* Wed Apr 07 1999 Bill Nottingham <notting@redhat.com>
- take out warning of directory ownership so root can still use screen

* Wed Apr 07 1999 Erik Troan <ewt@redhat.com>
- patched in utempter support, turned off setuid bit

* Fri Mar 26 1999 Erik Troan <ewt@redhat.com>
- fixed unix98 pty support

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Mar 11 1999 Bill Nottingham <notting@redhat.com>
- add patch for Unix98 pty support

* Mon Dec 28 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.7.6.

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- upgraded to 3.7.4

* Wed Oct 08 1997 Erik Troan <ewt@redhat.com>
- removed glibc 1.99 specific patch

* Tue Sep 23 1997 Erik Troan <ewt@redhat.com>
- added install-info support

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
