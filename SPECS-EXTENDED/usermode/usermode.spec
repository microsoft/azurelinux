# Add `--without gtk' option (enable gtk by default):
# No GTK 2 in RHEL 10
%if 0%{?rhel} > 9
%bcond_with gtk
%else
%bcond_without gtk
%endif

Summary: Tools for certain user account management tasks
Name: usermode
Version: 1.114
Release: 10%{?dist}
License: GPL-2.0-or-later
URL: https://pagure.io/%{name}/
Source: https://releases.pagure.org/%{name}/%{name}-%{version}.tar.xz
Source1: config-util
Requires: pam, passwd, util-linux
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/IJFYI5Q2BYZKIGDFS2WLOBDUSEGWHIKV/
BuildRequires: make
BuildRequires: gcc
BuildRequires: gettext, glib2-devel, intltool
%if %{with gtk}
BuildRequires: desktop-file-utils, gtk2-devel, startup-notification-devel, libSM-devel
%endif
BuildRequires: libblkid-devel, libselinux-devel, libuser-devel
BuildRequires: pam-devel, perl-XML-Parser
BuildRequires: util-linux

%if %{with gtk}
%package gtk
Summary: Graphical tools for certain user account management tasks
Requires: %{name} = %{version}-%{release}
%endif

%global _hardened_build 1

%description
The usermode package contains the userhelper program, which can be
used to allow configured programs to be run with superuser privileges
by ordinary users.

%if %{with gtk}
%description gtk
The usermode-gtk package contains several graphical tools for users:
userinfo, usermount and userpasswd.  Userinfo allows users to change
their finger information.  Usermount lets users mount, unmount, and
format file systems.  Userpasswd allows users to change their
passwords.

Install the usermode-gtk package if you would like to provide users with
graphical tools for certain account management tasks.
%endif

%prep
%setup -q

%build
%configure --with-selinux --without-fexecve %{!?with_gtk:--without-gtk}

%make_build

%install
%make_install

%if %{with gtk}
# make userformat symlink to usermount
ln -sf usermount $RPM_BUILD_ROOT%{_bindir}/userformat
ln -s usermount.1 $RPM_BUILD_ROOT%{_mandir}/man1/userformat.1
%endif

mkdir -p $RPM_BUILD_ROOT/etc/security/console.apps
install -p -m 644 %{SOURCE1} \
	$RPM_BUILD_ROOT/etc/security/console.apps/config-util

%if %{with gtk}
for i in redhat-userinfo.desktop redhat-userpasswd.desktop \
	redhat-usermount.desktop; do
	echo 'NotShowIn=GNOME;KDE;' >>$RPM_BUILD_ROOT%{_datadir}/applications/$i
	desktop-file-install --vendor redhat --delete-original \
		--dir $RPM_BUILD_ROOT%{_datadir}/applications \
		$RPM_BUILD_ROOT%{_datadir}/applications/$i
done
%endif

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc ChangeLog NEWS README
%attr(4711,root,root) /usr/sbin/userhelper
%{_bindir}/consolehelper
%{_mandir}/man8/userhelper.8*
%{_mandir}/man8/consolehelper.8*
%config(noreplace) /etc/security/console.apps/config-util

%if %{with gtk}
%files gtk
%{_bindir}/usermount
%{_mandir}/man1/usermount.1*
%{_bindir}/userformat
%{_mandir}/man1/userformat.1*
%{_bindir}/userinfo
%{_mandir}/man1/userinfo.1*
%{_bindir}/userpasswd
%{_mandir}/man1/userpasswd.1*
%{_bindir}/consolehelper-gtk
%{_mandir}/man8/consolehelper-gtk.8*
%{_bindir}/pam-panel-icon
%{_mandir}/man1/pam-panel-icon.1*
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%endif

%changelog
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.114-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.114-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.114-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.114-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 06 2023 Tomas Popela <tpopela@redhat.com> - 1.114-6
- Don't build GTK 2 bits on RHEL 10 as GTK 2 won't be available there

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.114-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.114-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.114-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 16 2021 Jiri Kucera <jkucera@redhat.com> - 1.114-2
- Do not use fexecve
  Script executed via fexecve has a file descriptor number in
  argv[0]. This results in unexpected output: when displaying
  the script help, a user see "Usage: <number> [options]"
  instead of "Usage: <scriptname> [options]".
  Resolves: #1969918

* Tue May 04 2021 Jiri Kucera <jkucera@redhat.com> - 1.114-1
- Update to usermode-1.114
- Allow to optionally disable GTK

* Mon May 03 2021 Jiri Kucera <jkucera@redhat.com> - 1.113-1
- Update to usermode-1.113

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.112-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 09 2020 Jiri Kucera <jkucera@redhat.com> - 1.112-9
- Do not use deprecated selinux headers
  Resolves #1865598

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.112-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.112-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.112-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.112-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.112-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Jiri Kucera <jkucera@redhat.com> - 1.112-3
- Dropped need to run autotools
- <sys/sysmacros.h> must be now included manually
  Resolves #1606624
- Fixed bad FSF address

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.112-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 22 2018 Jiri Kucera <jkucera@redhat.com> - 1.112-1
- Update to usermode-1.112
  Resolves #1269643

* Wed Feb 21 2018 Jiri Kucera <jkucera@redhat.com> - 1.111-14
- Added missing gcc dependency

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.111-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.111-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.111-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 24 2017 Miloslav Trmač <mitr@redhat.com> - 1.111-10
- Fix a FBFS with  -Werror=format-security
  Resolves #1444750
- Fix inconsistent dates in %%changelog

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.111-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.111-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.111-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.111-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.111-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.111-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Miloslav Trmač <mitr@redhat.com> - 1.111-3
- Enable hardened build
  Resolves: #965471

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.111-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Sep 22 2012 Miloslav Trmač <mitr@redhat.com> - 1.111-1
- Update to usermode-1.111

* Tue Aug 21 2012 Miloslav Trmač <mitr@redhat.com> - 1.110-2
- Drop no longer necessary %%clean and %%defattr commands.

* Mon Aug 20 2012 Miloslav Trmač <mitr@redhat.com> - 1.110-1
- Update to usermode-1.110.
  Note that this drops halt/poweroff/reboot helpers, the respective
  implementations in systemd now include PolicyKit support.  Spec file change
  based on a patch by Lennart Poettering <lpoetter@redhat.com>.
  Resolves: #804088, #849208

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.109-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar  3 2012 Miloslav Trmač <mitr@redhat.com> - 1.109-1
- Update to usermode-1.109

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.108-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct  3 2011 Miloslav Trmač <mitr@redhat.com> - 1.108-1
- Update to usermode-1.108
  Resolves: #622813, #716524

* Thu Mar 31 2011 Miloslav Trmač <mitr@redhat.com> - 1.107-1
- Update to usermode-1.107
  Resolves: #668731
- Add UGROUPS=wheel to config-util
  Resolves: #688690

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.106.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.106.1-2
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Miloslav Trmač <mitr@redhat.com> - 1.106.1-1
- Update to usermode-1.106.1

* Thu Aug 26 2010 Miloslav Trmač <mitr@redhat.com> - 1.106-1
- Update to usermode-1.106

* Thu Apr  8 2010 Miloslav Trmač <mitr@redhat.com> - 1.105-1
- Update to usermode-1.105
  Resolves: #578124
  Resolves: #580481

* Fri Mar 26 2010 Miloslav Trmač <mitr@redhat.com> - 1.104.2-1
- Update to usermode-1.104.2

* Thu Mar  4 2010 Miloslav Trmač <mitr@redhat.com> - 1.104.1-1
- Update to usermode-1.104.1
- Drop no longer necessary references to BuildRoot:

* Thu Feb 25 2010 Miloslav Trmač <mitr@redhat.com> - 1.104-1
- Update to usermode-1.104
  Resolves: #567117

* Tue Feb 16 2010 Miloslav Trmač <mitr@redhat.com> - 1.103-1
- Update to usermode-1.103

* Fri Feb  5 2010 Miloslav Trmač <mitr@redhat.com> - 1.102-2
- Use %%{?_smp_mflags}
- Use the four-parameter version of %%defattr
- Be more paranoid about dropping privileges
  Resolves: #562194
- Set PAM_TTY
  Resolves: #562195

* Mon Oct  5 2009 Miloslav Trmač <mitr@redhat.com> - 1.102-1
- Update to usermode-1.102

* Tue Sep 15 2009 Miloslav Trmač <mitr@redhat.com> - 1.101-1
- Update to usermode-1.101

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.100-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Miloslav Trmač <mitr@redhat.com> - 1.100-3
- Require libblkid-devel instead of e2fsprogs-devel

* Tue Apr 14 2009 Miloslav Trmač <mitr@redhat.com> - 1.100-2
- Add BuildRequires: intltool

* Tue Apr 14 2009 Miloslav Trmač <mitr@redhat.com> - 1.100-1
- Update to usermode-1.100

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.99-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Miloslav Trmač <mitr@redhat.com> - 1.99-2
- Fix problems pointed out in merge review:
  - Drop Conflicts: SysVinit < very-old
  - Remove very old version requirements from Requires and BuildRequires
  - Make /etc/security/console.apps/* %%config(noreplace)
  - Update BuildRoot

* Tue Nov 11 2008 Miloslav Trmač <mitr@redhat.com> - 1.99-1
- Update to usermode-1.99
  Resolves: #470834

* Thu Nov  6 2008 Miloslav Trmač <mitr@redhat.com> - 1.98.1-2
- Hide usermount from GNOME and KDE menus
  Resolves: #440029
- Only hide userinfo and userpasswd in GNOME and KDE

* Tue Oct 28 2008 Miloslav Trmač <mitr@redhat.com> - 1.98.1-1
- Update to usermode-1.98.1-1

* Sun Aug  3 2008 Miloslav Trmač <mitr@redhat.com> - 1.98-1
- Support dialogs with no text entries
- Preserve timestamps of some installed files
  Resolves: #456749
- Remove /usr/X11R6/bin from the default path.
  Resolves: #446849
- Left-justify messages
- Preserve file timestamps where possible.

* Thu May  1 2008 Miloslav Trmač <mitr@redhat.com> - 1.97-1
- Fix display of '_' in prompts
  Resolves: #444545

* Thu Apr 10 2008 Miloslav Trmač <mitr@redhat.com> - 1.96.1-1
- New release with updated translations

* Fri Feb 29 2008 Miloslav Trmač <mitr@redhat.com> - 1.96-1
- Remove code that overrides SELinux contexts of processes started by
  userhelper.
  Related: #247967
- Delete the WITH_SELINUX variable.

* Mon Feb 25 2008 Miloslav Trmač <mitr@redhat.com> - 1.95-1
- New home page at https://fedorahosted.org/usermode/
- Correctly preserve exit code when SESSION=yes
- Fix minor errors in the .desktop files
- Ship documentation

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.94-2
- Autorebuild for GCC 4.3

* Thu Jan 10 2008 Miloslav Trmač <mitr@redhat.com> - 1.94-1
- Add support for including files from wrapper configuration files.  Original
  patch by Carlo de Wolf.
  Resolves: #426095
- Add /etc/security/console.apps/config-util for use by system-config-*
- Rename sr@Latn.po to sr@latin.po
  Resolves: #425842

* Tue Oct 16 2007 Miloslav Trmač <mitr@redhat.com> - 1.93.1-1
- New release with updated translations
  Resolves: #332441
- Build with startup notification
  Resolves: #294591

* Wed Sep  5 2007 Miloslav Trmač <mitr@redhat.com> - 1.93-1
- Fix handling of PAM conversations with no questions
  Resolves: #267361
- Update License:

* Mon Jun 11 2007 Miloslav Trmač <mitr@redhat.com> - 1.92-1
- Fix userhelper hangs in non-UTF8 locales
  Resolves: #242420
- Clean up menu categories in desktop files

* Sat Jun  9 2007 Miloslav Trmač <mitr@redhat.com> - 1.91.2-1
- Show the user we're authenticating as in an i18n-safe way.
  Resolves: #233210
- Remove BuildRequires: libattr-devel

* Thu Apr 19 2007 Miloslav Trmac <mitr@redhat.com> - 1.91.1-1
- New release with updated translations

* Tue Mar 27 2007 Matthias Clasen <mclasen@redhat.com> 1.91-2
- Clean up desktop files

* Mon Mar 19 2007 Miloslav Trmac <mitr@redhat.com> - 1.91-1
- Preserve environment variables in consolehelper if specified in the service
  config file
  Related: #213402

* Wed Mar 14 2007 Miloslav Trmac <mitr@redhat.com> - 1.90-1
- Fix GUI=no handling
  Resolves: #110701
- Add a dialog caption when changing user password
  Resolves: #154861
- Fix an use of PAM data after free
  Resolves: #176992
- Support "user", "users", LABEL= and UUID= in usermount and userformat
  Resolves: #189907
- Use less memory in pam-panel-icon until the icon is actually displayed
- Don't use deprecated GTK+ widgets

* Fri Mar  9 2007 Miloslav Trmac <mitr@redhat.com> - 1.89-1
- Preserve application exit code in consolehelper
  Resolves: #178991, #210893
- Drop the historical build6x spec file variable
- Fix some rpmlint warnings

* Mon Dec 11 2006 Martin Bacovsky <mbacovsk@redhat.com> - 1.88-3.el5
- Updated translations
- Resolves: #216622

* Fri Dec  1 2006 Martin Bacovsky <mbacovsk@redhat.com> - 1.88-2.el5
- Updated translations
- Resolves: #216622

* Thu Nov 30 2006 Martin Bacovsky <mbacovsk@redhat.com> - 1.88-1.el5
- Updated translations
- Resolves: #216622

* Tue Oct  3 2006 Martin Bacovsky <mbacovsky@redhat.com> 1.87-3
- Repackaging with new translations

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.87-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Martin Bacovsky <mbacovsky@redhat.com> 1.87-1
- pam-panel-icon is now transparent on GTK+ >2.10 (#207181),
  thanks to Bill Nottingham

* Wed Aug 30 2006 Martin Bacovsky <mbacovsky@redhat.com> 1.86-1
- fix userpasswd - Query window pops up three times if cancelling passwd (#202924)
- Serbian latin script translation added (#203003)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.85-2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.85-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.85-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Jindrich Novy <jnovy@redhat.com> 1.85-2
- add gettext, libattr-devel, libSM-devel dependencies

* Tue Jan  3 2006 Jindrich Novy <jnovy@redhat.com> 1.85-1
- fix userpasswd - don't crash if pam produces multi-line output (#175735)
  Thanks to toddp@bestweb.net
- added Serbian translation (#176152)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Jindrich Novy <jnovy@redhat.com> 1.84-1
- usermode-gtk dialog stays always on top, thanks to Pierre Ossman (#80634)

* Tue Nov 15 2005 Jindrich Novy <jnovy@redhat.com> 1.83-1
- accept gecos information on commandline for userinfo,
  patch by mclasen@redhat.com (#173232)
- update translations

* Wed Oct 26 2005 Jindrich Novy <jnovy@redhat.com> 1.82-1
- don't use pam_stack.so
- introduce userformat to better handle device formatting
  and removing usermount from menus (#132559)

* Tue Aug 16 2005 Jindrich Novy <jnovy@redhat.com> 1.81-1
- apply SELinux functionality enhancement patch from Dan Walsh
- rebuilt because of the new cairo

* Thu Aug 11 2005 Ray Strode <rstrode@redhat.com> 1.80-4
- rebuild

* Tue Jul 12 2005 Jindrich Novy <jnovy@redhat.com> 1.80-3
- rebuild again because of libwnck change

* Tue Jul 12 2005 Jindrich Novy <jnovy@redhat.com> 1.80-2
- rebuild because of broken libwnck dependency

* Wed May 11 2005 Jindrich Novy <jnovy@redhat.com> 1.80-1
- fix "Unknown error" when password is mistyped in userpasswd (#135500)
- add icons to windows for usermode-gtk applications (#155867)
- add missing checks for some PAM error codes
- fix ungettextized error message
- update translations

* Tue Mar 15 2005 Matthias Clasen <mclasen@redhat.com> 1.79-2
- rebuild against new libwnck

* Wed Mar 02 2005 Jindrich Novy <jnovy@rdhat.com> 1.79-1
- fix problem with root passwords starting with space (#124980)

* Wed Feb 16 2005 Jindrich Novy <jnovy@rdhat.com> 1.78-2
- add $RPM_OPT_FLAGS to CFLAGS

* Thu Jan 27 2005 Jindrich Novy <jnovy@redhat.com> 1.78-1
- pam-panel-icon has popup menu to choose to forget/keep
  authentization by right clicking as usual for other panel applets (#75845)
- fix race condition (#142254)

* Thu Jan 20 2005 Jindrich Novy <jnovy@redhat.com> 1.77-1
- preserve LANGUAGE environment variable in userhelper (#82300)
- use badge instead of keyring icon for pam-panel-icon (#122487)
- icon is not showed in the panel when logged as root (#75234)
- use new environment variable USERHELPER_UID to identify
  an user who executed an application via userhelper  (#116186)

* Thu Dec 02 2004 Jindrich Novy <jnovy@redhat.com> 1.76-1
- fix dependencies to Perl-XML-Parser #124170
- use pamconsole instead of user in /etc/fstab to let
  usermount work with hal #139820

* Tue Nov 16 2004 Jindrich Novy <jnovy@redhat.com>
- update libuser interface to libuser-0.6

* Wed Nov 10 2004 Jindrich Novy <jnovy@redhat.com> 1.75-1
- make pam-panel-icon using localized strings (#138609)
- update translations
- fix usermount to use "-I" option only for vfat and msdos fs
- fix Makefile.am to not to use "Release" from spec to name dist tarballs

* Wed Oct 20 2004 Jindrich Novy <jnovy@redhat.com> 1.74-1
- add patch from Mathew Miller (mattdm@mattdm.org) to use
  own user's password instead of root's in authentization
  (the user must be a member of specific group to enable it)

* Mon Oct 04 2004 Jindrich Novy <jnovy@redhat.com> 1.73-1
- add support to configure.in for more languages
- update translations from upstream
- generate build scripts by autogen.sh

* Tue Sep 28 2004 Rik van Riel <riel@redhat.com> 1.72-2
- add dependency on passwd (bz #125010)
- make sure the Release: isn't part of the path name and tarball name

* Mon Sep 27 2004 Ray Strode <rstrode@redhat.com> 1.72-1
- remove X-Red-Hat-Base category from userinfo.desktop
- fix `make distcheck'
- use proper value types for Terminal keys in desktop entries
- remove upstreamed mkfs patch

* Fri Sep 24 2004 Jindrich Novy <jnovy@redhat.com> 1.71-4
- updated dependencies to SELinux

* Wed Sep 22 2004 Jindrich Novy <jnovy@redhat.com> 1.71-3
- installation to Preferences/More Preferences as a request
  of Ray Strode (rstrode@redhat.com) and #131605

* Mon Sep 20 2004 Jindrich Novy <jnovy@redhat.com> 1.71-2
- added "-I" option to mkfs in the .mkfs patch (#117793)

* Thu Aug 26 2004 Alexander Larsson <alexl@redhat.com> - 1.71-1
- consolehelper: work if root is readonly

* Mon Jul 12 2004 Dan Walsh <dwalsh@redhat.com> 1.70-8
- Additional diffs from NSA
- Clean up comments

* Thu Jul 8 2004 Dan Walsh <dwalsh@redhat.com> 1.70-7
- More fixes for SELinux.  roll back to only use root for auth.
- Add getenforce checks
- Add root_passwd check

* Thu Jul 1 2004 Dan Walsh <dwalsh@redhat.com> 1.70-6
- More fixes to make targeted policy work correctly

* Thu Jul 1 2004 Dan Walsh <dwalsh@redhat.com> 1.70-5
- Fix to use root if user not defined

* Tue May 25 2004 Dan Walsh <dwalsh@redhat.com> 1.70-4
- Support new policy files

* Thu May 20 2004 Dan Walsh <dwalsh@redhat.com> 1.70-3
- Change user context to default name if username context not in passwd file

* Thu Apr 1 2004 Dan Walsh <dwalsh@redhat.com> 1.70-1
- Change user context to "root" if username context "user_t" not in passwd file

* Wed Mar 31 2004 Nalin Dahyabhai <nalin@redhat.com> 1.70-1
- fix accidental mixup of role and type setting up new selinux context
- log the new selinux context if we're running an app in a new selinux context

* Sat Feb 21 2004 Dan Walsh <dwalsh@redhat.com> 1.69-5
- Change to fall back to root auth if selinux user does not exist

* Tue Jan 27 2004 Dan Walsh <dwalsh@redhat.com> 1.69-4
- fix call to is_selinux_enabled

* Mon Dec  8 2003 Nalin Dahyabhai <nalin@redhat.com>
- fix warning in userinfo which would cause random early exit (#111409)
- clean up warnings

* Tue Nov 25 2003 Dan Walsh <dwalsh@redhat.com> 1.69-3.sel
- Fix handling of roles from console file

* Fri Nov 14 2003 Nalin Dahyabhai <nalin@redhat.com>
- don't disable use of deprecated GLib and GTK+ APIs, reported by the
  mysterious Pierre-with-no-last-name

* Thu Oct 30 2003 Dan Walsh <dwalsh@redhat.com> 1.69-2.sel
- Turn on sleinux

* Thu Oct 23 2003 Nalin Dahyabhai <nalin@redhat.com> 1.69-1
- all around: cleanups
- consolehelper: coalesce multiple messages from PAM again
- usermount: handle user-not-allowed-to-control-mounts error correctly (#100457)
- userhelper: trim off terminating commas when changing chfn info

* Mon Oct 6 2003 Dan Walsh <dwalsh@redhat.com> 1.68-8

* Wed Oct 1 2003 Dan Walsh <dwalsh@redhat.com> 1.68-7.sel
- Fix to use /etc instead of /usr/etc

* Thu Sep 25 2003 Dan Walsh <dwalsh@redhat.com> 1.68-6.sel
- turn on selinux
- add default userhelper context file

* Thu Sep 25 2003 Nalin Dahyabhai <nalin@redhat.com> 1.68-6
- make selinux a configure option to avoid screwing with makefiles

* Thu Sep 25 2003 Nalin Dahyabhai <nalin@redhat.com> 1.68-5
- rebuild

* Mon Sep 8 2003 Dan Walsh <dwalsh@redhat.com> 1.68-4
- turn off selinux

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 1.68-3.sel
- turn on selinux

* Tue Jul 29 2003 Dan Walsh <dwalsh@redhat.com> 1.68-2
- Add SELinux support

* Wed Apr 16 2003 Nalin Dahyabhai <nalin@redhat.com> 1.68-1
- update translations
- suppress the error dialog from user cancel

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 20 2003 Nalin Dahyabhai <nalin@redhat.com> 1.67-1
- work around GTK+ clearing DESKTOP_STARTUP_ID at gtk_init() time, so that
  startup notification actually works (#84684)

* Wed Feb 19 2003 Nalin Dahyabhai <nalin@redhat.com> 1.66-1
- consolehelper-gtk: complete startup notification at startup
- userhelper: pass startup notification data to consolehelper-gtk
- consolehelper-gtk: setup startup notification for children if userhelper
  requests it

* Mon Jan 27 2003 Nalin Dahyabhai <nalin@redhat.com> 1.65-2
- rebuild

* Mon Jan 20 2003 Nalin Dahyabhai <nalin@redhat.com> 1.65-1
- pass-through DESKTOP_STARTUP_ID

* Mon Jan  6 2003 Nalin Dahyabhai <nalin@redhat.com> 1.64-1
- set the requesting user PAM item to the invoking user's name (#81255)

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.63-2
- remove directory names from PAM config files, allowing the same config
  files to work for both arches on multilib boxes
- translation updates

* Wed Sep  4 2002 Nalin Dahyabhai <nalin@redhat.com> 1.63-1
- userhelper: swallow the exec'd program's exit status, which would be
  misinterpreted by consolehelper anyway

* Tue Sep  3 2002 Nalin Dahyabhai <nalin@redhat.com> 1.62-1
- consolehelper: suppress dialog on successful execution
- userhelper: return 0 on success, not 1 (what was I *thinking*?)

* Mon Sep  2 2002 Nalin Dahyabhai <nalin@redhat.com> 1.61-1
- userinfo: exit properly on escape. handle site_info field properly. go
  insensitive while running child process.
- userpasswd: exit properly on cancel.
- all of the above: reap the child instead of checking for pipe close -- this
  way is more robust (#68578,72684).
- usermount: run mount/umount synchronously. capture stderr and display in a
  dialog. desensitize action buttons when no filesystems are selected.
- consolehelper: display errors if we're attempting to run bogus programs
  (#72127)
- translation updates (#70278)

* Wed Aug 14 2002 Nalin Dahyabhai <nalin@redhat.com> 1.60-1
- reconnect the "cancel" and "ok" buttons in userinfo
- heed the cancel button when prompting for passwords in userinfo (#68578)
- translation update

* Wed Aug 14 2002 Nalin Dahyabhai <nalin@redhat.com> 1.59-2
- change "forget password" to "forget authorization", because we don't actually
  remember the password (that would be scary, #71476)
- translation update

* Tue Aug 13 2002 Nalin Dahyabhai <nalin@redhat.com> 1.59-1
- pam-panel-icon: overhaul, change the 'locked' icon to keyring-small, nix the
  'unlocked' icon
- consolehelper-gtk: properly set up the dialog buttons (should be 'cancel/ok'
  when we're asking questions, was always 'close')
- disappear pam_timestamp_init

* Wed Aug  7 2002 Nalin Dahyabhai <nalin@redhat.com> 1.58-2
- install the new 'unlocked' icon

* Tue Aug  6 2002 Jonathan Blandford <jrb@redhat.com>
- New version.

* Mon Aug  5 2002 Nalin Dahyabhai <nalin@redhat.com> 1.57-1
- add support for BANNER and BANNER_DOMAIN in the userhelper configuration

* Mon Aug  5 2002 Nalin Dahyabhai <nalin@redhat.com> 1.56-4
- mark strings in the .glade file as translatable (#70278)
- translation updates

* Wed Jul 31 2002 Nalin Dahyabhai <nalin@redhat.com> 1.56-3
- add icons for userpasswd and usermount

* Wed Jul 24 2002 Nalin Dahyabhai <nalin@redhat.com> 1.56-2
- actually include the icons
- translation updates

* Tue Jul 23 2002 Nalin Dahyabhai <nalin@redhat.com> 1.56-1
- userinfo: prevent users from selecting "nologin" as a shell (#68579)
- don't strip binaries by default; leave that to the buildroot policy
- use desktop-file-install

* Wed Jun 19 2002 Havoc Pennington <hp@redhat.com>
- put pam-panel-icon in file list

* Mon May 20 2002 Nalin Dahyabhai <nalin@redhat.com> 1.55-2
- don't strip binaries which have no special privileges

* Wed May 15 2002 Nalin Dahyabhai <nalin@redhat.com> 1.55-1
- remove the pixmap we don't use any more (we use stock pixmaps now)
- update translations

* Tue Apr 16 2002 Nalin Dahyabhai <nalin@redhat.com> 1.54-1
- suppress even error messages from Xlib when consolehelper calls
  gtk_init_check() to see if the display is available

* Mon Apr 15 2002 Nalin Dahyabhai <nalin@redhat.com> 1.53-2
- refresh translations

* Thu Apr 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.53-1
- refresh shell variable code from authconfig (#63175)

* Tue Apr  9 2002 Nalin Dahyabhai <nalin@redhat.com> 1.52-2
- refresh translations

* Mon Apr  1 2002 Nalin Dahyabhai <nalin@redhat.com> 1.52-1
- attempt to make prompts at the console more meaningful
- when falling back, reset the entire environment to the user's

* Thu Mar 28 2002 Nalin Dahyabhai <nalin@redhat.com>
- stop giving the user chances to enter the right password if we get a
  conversation error reading a response (appears to be masked by libpam)
  (#62195)
- always center consolehelper dialog windows

* Wed Mar 27 2002 Nalin Dahyabhai <nalin@redhat.com> 1.51-1
- patch to make gettext give us UTF-8 strings (which GTK needs) from ynakai

* Fri Mar 22 2002 Nalin Dahyabhai <nalin@redhat.com> 1.50-6
- update translations
- actually include the glade files (#61665)

* Mon Mar 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.50-5
- update translations

* Mon Feb 25 2002 Nalin Dahyabhai <nalin@redhat.com> 1.50-4
- rebuild

* Fri Feb 22 2002 Nalin Dahyabhai <nalin@redhat.com> 1.50-3
- update translations

* Thu Jan 31 2002 Nalin Dahyabhai <nalin@redhat.com> 1.50-2
- rebuild to fix dependencies

* Thu Jan 31 2002 Nalin Dahyabhai <nalin@redhat.com> 1.50-1
- fix userpasswd dialog message being incorrect for password changes
- use a dumb conversation function when text mode is invoked without a tty -- if
  the service's configuration doesn't call for prompts, then it'll still work
- port from pwdb to libuser
- catch child-exit errors correctly again
- fix keyboard-grabbing

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 1.49-3
- add default locations for certain binaries to configure.in

* Thu Jan  3 2002 Nalin Dahyabhai <nalin@redhat.com> 1.49-2
- munge glade file to use stock items for buttons where possible

* Mon Dec 10 2001 Nalin Dahyabhai <nalin@redhat.com> 1.49-1
- the console.apps configs shouldn't be missingok
- fix buildprereqs for gtk2/libglade2

* Tue Dec  4 2001 Nalin Dahyabhai <nalin@redhat.com>
- more gtk2 changes
- split off a -gtk subpackage with all of the gtk-specific functionality

* Wed Nov 28 2001 Nalin Dahyabhai <nalin@redhat.com>
- the grand libglade/gtk2 overhaul
- allow disabling display of GUI windows by setting "GUI=false" in the
  console.apps configuration file (default: TRUE)
- allow disabling display of GUI windows by recognizing a magic option
  on the command-line of the program being wrapped (NOXOPTION, no default)

* Fri Nov  9 2001 Nalin Dahyabhai <nalin@redhat.com> 1.46-1
- restore the previous XAUTHORITY setting before opening PAM sessions

* Fri Nov  2 2001 Nalin Dahyabhai <nalin@redhat.com> 1.45-1
- propagate environment variables from libpam to applications

* Wed Oct  3 2001 Nalin Dahyabhai <nalin@redhat.com> 1.44-1
- only try to call gtk_main_quit() if we've got a loop to get out of (#54109)
- obey RPM_OPT_FLAGS, obey

* Tue Aug 28 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.43-1
- Update translations

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add build requirements on glib-devel, gtk+-devel, pam-devel (#49726)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Feb 14 2001 Preston Brown <pbrown@redhat.com>
- final translation merge.

* Wed Feb 14 2001 Nalin Dahyabhai <nalin@redhat.com>
- clear the supplemental groups list before running binaries as root (#26851)

* Wed Feb  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- set XAUTHORITY if we fall back to regular behavior (#26343)
- make the suid helper 04711 instead of 04755

* Mon Feb  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- refresh translations

* Mon Jan 29 2001 Preston Brown <pbrown@redhat.com>
- use lang finding script.

* Thu Jan 25 2001 Yukihiro Nakai <ynakai@redhat.com>
- Some fix for Japanese environment.
- Use gtk_set_locale() instead of setlocale()
- Copyright update.

* Sun Jan  7 2001 Yukihiro Nakai <ynakai@redhat.com>
- Add gettextized

* Thu Nov  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix segfault in userhelper (#20027)

* Tue Oct 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- /sbin/shutdown, not /usr/sbin/shutdown (#19034)

* Fri Oct  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- don't pass on arguments to halt and reboot, because they error out

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix the /usr/bin/shutdown wrapper so that root can call shutdown
- only include the /usr/bin/shutdown wrapper on 6.x
- also sanitize LC_MESSAGES
- tweak sanitizing checks (from mkj)

* Wed Oct  4 2000 Jakub Jelinek <jakub@redhat.com>
- fix a security bug with LC_ALL/LANG variables (#18046)

* Mon Aug 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- mark defined strings translateable (#17006)

* Thu Aug 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix incorrect user name
- add a shell wrapper version of /usr/bin/shutdown
- build for 6.x errata
- bump revision to upgrade the errata

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix stdin/stdout redirection shenanigans (#11706)
- fix authentication and execution as users other than root
- make sure the right descriptors are terminals before dup2()ing them
- cut out an extra-large CPU waster that breaks GUI apps

* Mon Aug 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix typo (#16664)

* Sun Aug 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- previous fix, part two

* Sat Aug 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix inadvertent breakage of the shell-changing code

* Fri Aug 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix the "run unprivileged" option

* Mon Aug 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- actually use the right set of translations

* Fri Aug 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove the shutdown command from the list of honored commands

* Wed Aug  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- merge in updated translations
- set XAUTHORITY after successful authentication (#11006)

* Wed Aug  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- install translations
- fixup a messy text string
- make "Mount"/"Unmount" translatable
- stop prompting for passwords to shut down -- we can hit ctrl-alt-del anyway,
  and gdm users can just shut down without logging in

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- attempt to add i18n support

* Wed Jul 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- attempt to get a usable icon for userhelper-wrap (#13616, #13768)

* Wed Jul  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix them right this time

* Mon Jul  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix verbosity problems

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- strip all binaries by default
- add the name of the program being run to the userhelper dialog
- add a graphic to the userhelper-wrap package
- add a button to jump straight to nonprivileged operation when supported

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- rebuilt to see if we get stripped binaries

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- move man pages to %%{_mandir}

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify PAM setup to use system-auth
- bzip2 compress tarball

* Fri Mar 17 2000 Ngo Than <than@redhat.de>
- fix problem with LANG and LC_ALL
- compress source with bzip2

* Thu Mar 09 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix problem parsing userhelper's -w flag with other args

* Wed Mar 08 2000 Nalin Dahyabhai <nalin@redhat.com>
- ignore read() == 0 because the child exits

* Tue Mar 07 2000 Nalin Dahyabhai <nalin@redhat.com>
- queue notice messages until we get prompts in userhelper to fix bug #8745

* Thu Feb 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- free trip through the build system

* Tue Jan 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- grab keyboard input focus for dialogs

* Fri Jan 07 2000 Michael K. Johnson <johnsonm@redhat.com>
- The root exploit fix created a bug that only showed up in certain
  circumstances.  Unfortunately, we didn't test in those circumstances...

* Mon Jan 03 2000 Michael K. Johnson <johnsonm@redhat.com>
- fixed local root exploit

* Thu Sep 30 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed old complex broken gecos parsing, replaced with simple working parsing
- can now blank fields (was broken by previous fix for something else...)

* Tue Sep 21 1999 Michael K. Johnson <johnsonm@redhat.com>
- FALLBACK/RETRY in consolehelper/userhelper
- session management fixed for consolehelper/userhelper SESSION=true
- fix memory leak and failure to close in error condition (#3614)
- fix various bugs where not all elements in userinfo got set

* Mon Sep 20 1999 Michael K. Johnson <johnsonm@redhat.com>
- set $HOME when acting as consolehelper
- rebuild against new pwdb

* Tue Sep 14 1999 Michael K. Johnson <johnsonm@redhat.com>
- honor "owner" flag to mount
- ask for passwords with username

* Tue Jul 06 1999 Bill Nottingham <notting@redhat.com>
- import pam_console wrappers from SysVinit, since they require usermode

* Mon Apr 12 1999 Michael K. Johnson <johnsonm@redhat.com>
- even better check for X availability

* Wed Apr 07 1999 Michael K. Johnson <johnsonm@redhat.com>
- better check for X availability
- center windows to make authentication easier (improve later with
  transients and embedded windows where possible)
- applink -> applnk
- added a little padding, especially important when running without
  a window manager, as happens when running from session manager at
  logout time

* Wed Mar 31 1999 Michael K. Johnson <johnsonm@redhat.com>
- hm, need to be root...

* Fri Mar 19 1999 Michael K. Johnson <johnsonm@redhat.com>
- updated userhelper.8 man page for consolehelper capabilities
- moved from wmconfig to desktop entries

* Thu Mar 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- added consolehelper
- Changed conversation architecture to follow PAM spec

* Wed Mar 17 1999 Bill Nottingham <notting@redhat.com>
- remove gdk_input_remove (causing segfaults)

* Tue Jan 12 1999 Michael K. Johnson <johnsonm@redhat.com>
- fix missing include files

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries
- use defattr
- fix spec file ( rm -rf $(RPM_BUILD_ROOT) is a stupid thing to do ! )

* Tue Oct 06 1998 Preston Brown <pbrown@redhat.com>
- fixed so that the close button on window managers quits the program properly

* Thu Apr 16 1998 Erik Troan <ewt@redhat.com>
- use gtk-config during build
- added make archive rule to Makefile
- uses a build root

* Fri Nov  7 1997 Otto Hammersmith <otto@redhat.com>
- new version that fixed memory leak bug.

* Mon Nov  3 1997 Otto Hammersmith <otto@redhat.com>
- updated version to fix bugs

* Fri Oct 17 1997 Otto Hammersmith <otto@redhat.com>
- Wrote man pages for userpasswd and userhelper.

* Tue Oct 14 1997 Otto Hammersmith <otto@redhat.com>
- Updated the packages... now includes userpasswd for changing passwords
  and newer versions of usermount and userinfo.  No known bugs or
  misfeatures. 
- Fixed the file list...

* Mon Oct 6 1997 Otto Hammersmith <otto@redhat.com>
- Created the spec file.
