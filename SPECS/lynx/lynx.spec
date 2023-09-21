#
# spec file for package lynx
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define tarbase 2.9.0dev.9
Summary:        A Text-Based WWW Browser
Name:           lynx
Version:        2.9.0~dev.9
Release:        5%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Productivity/Networking/Web/Browsers
URL:            https://lynx.invisible-island.net/
Source0:        https://invisible-mirror.net/archives/%{name}/tarballs/%{name}%{tarbase}.tar.bz2
# changing default configuration
Patch0:         lynx-charset.patch
Patch1:         lynx-enable_xli.patch
# bugs
Patch2:         lynx-proxy-empty-string.patch
BuildRequires:  dos2unix
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  slang-devel
BuildRequires:  unzip
BuildRequires:  zip
BuildRequires:  zlib-devel
Provides:       web_browser

%description
Lynx is an easy-to-use browser for HTML documents and other Internet
services like FTP, telnet, and news.  Lynx is fast.  It is purely text
based and therefore makes it possible to use WWW resources on text
terminals.

%prep
%autosetup -p1 -n %{name}%{tarbase}

%build
%configure --enable-debug --with-build-cflags="%{optflags} -DNO_BUILDSTAMP" \
	--with-ssl \
	--with-zlib \
	--with-bzlib \
	--enable-nls \
	--disable-default-colors \
	--disable-color-style \
	--with-screen=ncursesw \
	--enable-ipv6
%make_build

mv lynx lynx-bw
%make_build distclean
%configure --enable-debug --with-build-cflags="%{optflags}" \
	--with-ssl \
	--with-bzlib \
	--enable-nls \
	--enable-default-colors \
	--with-screen=ncursesw \
	--enable-ipv6
%make_build

%install
%make_install
%make_build clean
mv %{buildroot}%{_bindir}/lynx %{buildroot}%{_bindir}/lynx-color
install lynx-bw %{buildroot}%{_bindir}/lynx

chmod ogu-x scripts/conf.mingw.sh scripts/config.djgpp.sh

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_bindir}/lynx
%{_bindir}/lynx-color
%config %{_sysconfdir}/lynx.cfg
%config %{_sysconfdir}/lynx.lss
%{_mandir}/man1/lynx.1*
%doc AUTHORS CHANGES README README PROBLEMS
%doc lynx_help samples scripts

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.9.0~dev.9-5
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Dec 08 2021 Thomas Crain <thcrain@microsoft.com> - 2.9.0~dev.9-4
- Reformat patches, use autosetup
- License verified
- Lint spec

* Tue Dec 07 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9.0~dev.9-3
- Removing BR on 'postfix'.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9.0~dev.9-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Switching to using single-number 'Release' tags.

* Thu Aug 12 2021 pgajdos@suse.com
- version update to 2.9.0~dev.9 [bsc#1189354]
  * development version, see CHANGES for details
  namely:
  * strip user/password from ssl_host in HTLoadHTTP, incorrectly passed as
    part of the server name indicator (Debian #991971) -TD

* Sat Oct  6 2018 sean@suspend.net
- update to 2.8.9rel1.1:
  * documentation/metrics updates
  * fix an inconsistency in message for -listonly option
  * update test-packages to use current ncurses test-packages
  * improve portability for sockaddr structures used in HTTP and FTP, for IPv6 and SOCKS configurations
  * fix several minor warnings reported by Coverity
  * build-fix overlooked in 2.8.9dev.3 when INACTIVE_INPUT_STYLE_VH is defined, for problem introduced by 2.8.8dev.17 code-cleanup
  * trim unnecessary intllib symbols from src/chrtrans/makefile.in
  * when cross-compiling, trim LDFLAGS from makefile rule linking makeuctb
- dropped patches:
  lynx-helpfile.patch: latest documentation available online

* Mon Nov 20 2017 pgajdos@suse.com
- update to 2.8.9dev.16:
  * add a note in the comments for INCLUDE in lynx.cfg regarding the default
  directory searches LYOpenCFG(), added in 2.8.4dev.20 (Debian #818047) -TD
  * add a check to ensure that HTML_put_string() will not append a chunk onto
  itself (report by Ned Williamson) -TD
  * add note in lynx.cfg about default values (Debian #408448) -TD
  * amended Backes' change to the COLLAPSE_BR_TAGS feature for compatibility -TD
  + use ENABLE_LYNXRC to determine whether it is written to the .lynxrc file.
  + add command-line option, etc., for controlling whether blank lines are
    trimmed, e.g., trailing lines as well as the special case for collapsing
    br-tags.  Leading blank lines at the top of the document are untouched.
  + modify limit for trimmed lines to retain as little as 1 line; previously
    the trimming would go no smaller than 2 lines.
  * add command-line option and options-menu item for COLLAPSE_BR_TAGS (patch
  by Peter Backes).
  * correct logic in HTCopy() when re-reading a page (Debian #863008) -TD

* Tue Sep  5 2017 mgorse@suse.com
- Add --with-zlib and --with-bzip2 to configure, to allow
  decompressing directly via zlib and support bzip2.
- Add libbz2-devel and zlib-devel to BuildRequires

* Mon Jun 12 2017 pgajdos@suse.com
- update to 2.8.9dev.14 to build with openssl 1.1 [bsc#1042661]
- dropped patches
  . lynx-2.8.5.dif
  . lynx-no-build-date.patch
  . lynx-2.8.8-expired-cookie-crash.patch
  . lynx-CVE-2016-9179.patch
  . lynx-2.8.8-ncurses-6.0-20170318.patch
- renamed patches
  . lynx-2.8.7-enable_xli.patch to lynx-enable_xli.patch
  . lynx-2.8.5-charset.patch to lynx-charset.patch
  . lynx-2.8.5.dif split to lynx-helpfile.patch and
    lynx-proxy-empty-string.patch

* Mon Apr  3 2017 werner@suse.de
- Use upstream commit f0b064b47bfa046da941f5029cdc1b4c851553ce to
  replace workaround in patch lynx-2.8.8-ncurses-6.0-20170318.patch

* Fri Mar 31 2017 pgajdos@suse.com
- fix typo in url

* Thu Mar 30 2017 werner@suse.de
- Update project Url as well as Url path of source tar ball
- Add patch lynx-2.8.8-ncurses-6.0-20170318.patch to work
  around internal header definition of ncurses-6.0-20170318

* Mon Feb  6 2017 pgajdos@suse.com
- security update:
  * CVE-2016-9179 [bsc#1008642]
    + lynx-CVE-2016-9179.patch

* Thu Nov 27 2014 mgorse@suse.com
- Add lynx-2.8.8-expired-cookie-crash.patch: fix invalid read when
  removing an expired cookie (bnc#907539).

* Sat Mar 29 2014 andreas.stieger@gmx.de
- lynx 2.8.8rel.2
  * correct errata in test-files which cause broken links in
    break-out directory in lynx.isc.org server
  * amend change from 2.8.8pre.2, to ensure that MinGW libraries
    already declaring 'sleep()' will build
  * drop unused save/compress rules from makefile.in, because fixing
    umask for these is pointless
  * modify makefile.in to establish sane umask value in the
    "install-doc" rule
- lynx as an extra version element, append to version and adjust
  filename to make download_files pass

* Sat Feb 22 2014 andreas.stieger@gmx.de
- lynx 2.8.8rel.1
- user visible changes:
  * add internal URL scheme "LYNXEDITMAP:" field-editing help
  * correct formatting of large file-sizes in directory listing
  * add "submit" and "reset" commands
  * add "pwd" command, to show current working directory in the
    statusline
  * add option -unique-urls
  * add -list_inline option, which modifies -dump output to put
    links inline with the text rather than in a list at the end of
    the dump
  * GNUTLS to enable SNI (Server Name Indication)
  * improved HTML interpretation
  * improved handling and display of character sets
  * Full list of changes and improvements:
    http://lynx.isc.org/lynx2.8.8/features.html
- packaging changes:
  * fix self-obsoletion of lynxssl
  * removed patches:
    + lynx-openssl.patch, committed upstream
  * modified patches:
    + lynx-2.8.5-charset.patch adjust for upstream changes

* Fri Jan 10 2014 coolo@suse.com
- fix license - there is no 'or later' in the license

* Mon Feb 11 2013 crrodriguez@opensuse.org
- lynx-openssl.patch : just like in the "links" case, HTTPS
  clients must not:
  * Negotiate SSLv2
  * Attempt to use SSL compression (due to CVE-2012-4929)
- Fix debuginfo generation.

* Wed Dec 21 2011 coolo@suse.com
- remove call to suse_update_config (very old work around)

* Thu Jul 28 2011 vcizek@novell.com
- removed the very long list of authors from spec

* Tue Jul 26 2011 meissner@suse.de
- remove x bits from sample windows scripts

* Thu Mar 24 2011 vcizek@novell.com
- update to 2.8.7rel.2
  * add limit-check for too-long URIs in href's (RedHat #605286)
  * fix a few places still referring to "2-8-6"

* Sat Sep  4 2010 cristian.rodriguez@opensuse.org
- Do not include build date in binaries

* Sun Jan  3 2010 jengelh@medozas.de
- enable parallel build

* Fri Dec 11 2009 anicka@suse.cz
- update to 2.8.7
  * many bugfixes
  * added many new options
  * improved SSL support, cookie support, HTML interpretation
- removed -ipv6 patch (feature implemented upstream)
- removed CVE-2008-4690 patch (fixed upstream)

* Wed Oct 29 2008 kssingvo@suse.de
- fix for lynxcgi command execution CVE-2008-4690 (bnc#439149)
- not affected: .mailcap and .mime.types files read, CVE-2006-7234

* Wed Jul  4 2007 kssingvo@suse.de
- added official patch from lynx.isc.org:
  * correct loop-limit in print_crawl_to_fd(), which broke
    "lynx -crawl -dump" from 2.8.6dev.9 changes

* Tue Apr  3 2007 kssingvo@suse.de
- upgrade to final version of 2.8.6
- removed patch with final changes

* Thu Mar 29 2007 dmueller@suse.de
- add ncurses-devel BuildRequires

* Mon Nov 20 2006 kssingvo@suse.de
- added patch to have the 2.8.6 final version patches:
  * limit files set via PERSONAL_EXTENSION_MAP and PERSONAL_MAILCAP
    to be found relative to the user's home directory.
  * ensure that the configured values for GLOBAL_EXTENSION_MAP and
    GLOBAL_MAILCAP are absolute pathnames -TD
  * modify logic for reading PERSONAL_EXTENSION_MAP and
    PERSONAL_MAILCAP to ensure that they are files that are
    controlled only by the user.

* Tue Oct 31 2006 kssingvo@suse.de
- disabled color support for non-color lynx, enabled color support
  for lynx-color
- added helpful directories to pkg documentation: samples, scripts

* Mon Oct 16 2006 ssommer@suse.de
- updated to 2.8.6rel.2: Highligths:
  * broaden the conditions on which to reload the color-style info
  * documentation fixes

* Wed Oct  4 2006 ssommer@suse.de
- updated to 2.8.6pre.5: Highlights:
  * buildsystem fixes
  * updated files from ftp.unicode.org

* Tue Sep 19 2006 ssommer@suse.de
- updated to 2.8.6pre.4: Highlights:
  * add script samples/oldlynx, which gives the non-color-style
  scheme using an executable built for color-style
  * add DEFAULT_COLORS item to lynx.cfg to allow disabling the
  default colors feature at runtime, allowing better matching
  of old color scheme via a script

* Mon Sep 18 2006 ssommer@suse.de
- updated to 2.8.6pre.3: Highlights from the Changelog:
  * add NESTED_TABLES setting to lynx.cfg to allow site override of
  the built-in default
  * add check for failure to write to disk, e.g., on disk full
  * add presentation for text/css, to allow browsing ".css" files
  * add presentation type for application/xml and text/xml mime types
  * add presentation type for application/xhtml+xml mime type
  * add "Anonymous FTP Password" to Options menu
  * add command-line option -syslog-urls to allow syslog'ing of URLs
  to be optional
  * highlight the target and pause for 20 milliseconds when selecting
  a link with the mouse
  * add -stderr option to write error messages when doing a -dump -or
  - source.
  * add -nonumbers option, which modifies the output of -dump to
  suppress the link-numbering
  * add -listonly option, which modifies the output of -dump to show
  only the list of links
  * modify treatment of symbolic links for ftp-URLs to show the link
  target, as with the local directory editor
  * lynx accepts multiple URLs on the command line
  * modify logic for -dump so it can dump all pages listed on the
  command line
- removed obsolete patches and updated the remaining patches
- config files are stored in sysconfdir not in libdir
- added /etc/lynx.lss config file

* Wed May 17 2006 schwab@suse.de
- Don't strip binaries.

* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires

* Wed Jan 11 2006 kssingvo@suse.de
- added three official patches
- disabled (own) security patches, which are included now

* Mon Nov 14 2005 kssingvo@suse.de
- added fix for potential cgi_links hole (bugzilla#133645)

* Thu Oct 27 2005 kssingvo@suse.de
- 2nd fix for nntpserver buffer overflow (bugzilla#121926)

* Thu Oct 20 2005 kssingvo@suse.de
- fix for nntpserver buffer overflow CAN-2005-3120 (bugzilla#121926)

* Fri Oct  8 2004 ke@suse.de
- Apply lynx-2.8.5-charset.patch: Set LOCALE_CHARSET:TRUE for detecting
  UTF-8 automatically [# 46898].

* Thu Aug 12 2004 kssingvo@suse.de
- added official 2.8.5rel.2 patch

* Fri Jul 16 2004 kssingvo@suse.de
- linking against libncursesw to get umlauts in UTF-8 working (bugzilla#43086)

* Fri Mar 26 2004 mmj@suse.de
- Add postfix to # neededforbuild

* Thu Mar  4 2004 kssingvo@suse.de
- update to 2.8.5
- adapted local patches and enhancements

* Fri Jan  9 2004 adrian@suse.de
- use %%find_lang

* Tue Sep  2 2003 kssingvo@suse.de
-  strange things in certain locale fix (bugzilla#29772)

* Thu May 15 2003 coolo@suse.de
- use BuildRoot

* Tue Feb 18 2003 kssingvo@suse.de
- fixed (hopefully) problem with IPv6 addresses (bugzilla #20744)

* Wed Dec 11 2002 kssingvo@suse.de
- added offical patches a-d

* Fri Sep 27 2002 uli@suse.de
- ignore both unset and empty *_proxy variables (bug #20262)

* Thu Aug 22 2002 uli@suse.de
- moved config file from /usr/lib to /etc (bug #18179)

* Sun Jun  9 2002 olh@suse.de
- use suse_update_config for ppc64

* Mon May 27 2002 uli@suse.de
- assume local .php* files to be text/html (bug #15907)

* Mon Mar 18 2002 uli@suse.de
- backed out the aforementioned fix as it breaks important sites
  (e.g. freshmeat, slashdot; fixes bug #15065)

* Tue Feb 19 2002 uli@suse.de
- disabled default compressed handlers (fixes bug #13304)

* Mon Sep 17 2001 uli@suse.de
- enabled use of default colors (was disabled all the time, but it
  seems the disabling didn't work before 2.8.4)

* Thu Aug 16 2001 uli@suse.de
- update -> 2.8.4 rel. 1
- enabled IPv6 (Bug #8655)

* Fri Jul 27 2001 ke@suse.de
- update message files from
  http://www.iro.umontreal.ca/contrib/po/maint/lynx/ ; packed as
  po.tar.bz2.
  Fix [#8662].

* Wed Jun 27 2001 uli@suse.de
- update -> 2.8.3 final
- enabled NLS

* Tue May  8 2001 mfabian@suse.de
- bzip2 sources

* Thu Jan  4 2001 uli@suse.de
- changed lynxssl -> lynx in some paths

* Tue Dec 19 2000 lmuelle@suse.de
- remove unnecessary Provides: lynx2

* Mon Dec 18 2000 uli@suse.de
- "lynxssl" becomes "lynx" (non-SSL version will be dropped)

* Mon Nov 27 2000 uli@suse.de
- fixed neededforbuild
- uses passive FTP by default (req. by Andi Kleen)

* Wed Sep 27 2000 uli@suse.de
- new package with SSL support

* Fri Aug 18 2000 uli@suse.de
- fixed location of help file in lynx.cfg

* Fri Jun  2 2000 kukuk@suse.de
- Use doc macro

* Wed Mar  1 2000 schwab@suse.de
- Add group tag.
- /usr/man -> /usr/share/man

* Mon Sep 20 1999 ro@suse.de
- added Provides web_browser

* Wed Sep 15 1999 uli@suse.de
- update -> 2.8.3dev9
- scrapped Makefile.Linux
- added RPM_OPT_FLAGS to CFLAGS

* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.

* Mon Jul 27 1998 florian@suse.de
- add /usr/bin/lynx-color again, as there is no global
  configuration possibility

* Thu Jul 16 1998 florian@suse.de
- update to version 2.8
- no need to have an extra ncurses-color anymore as the
  ncurses-version has now also color support: "lynx -color"

* Wed Mar  4 1998 florian@suse.de
- update to version 2.7.2

* Fri Oct 17 1997 ro@suse.de
- ready for autobuild

* Tue Jul 29 1997 florian@suse.de
- add security-fix for lynx 2.7.1
- also include a "lynx-color" that is build with slang instead of ncurses
  future lynx-ncurses will also have color-support, but a separate
  lynx-color should be ok right now

* Mon Jun  2 1997 florian@suse.de
- update to version 2-7-1

* Sun Apr 13 1997 florian@suse.de
- update to new version 2.7

* Thu Jan  2 1997 florian@suse.de
- Update auf Version 2-6.
- Beim Aufruf des eingebauten Hilfesystems werden lokale Dateien
  aufgerufen und nicht die Internet-Version benuetzt.

* Thu Jan  2 1997 florian@suse.de
- Update auf neue Version 2-6. /usr/etc/mailcap sollte nun in aaa_base sein.
