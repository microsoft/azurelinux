%bcond_with trace
%global x11_app_defaults_dir %(pkg-config --variable appdefaultdir xt)

Summary:        Terminal emulator for the X Window System
Name:           xterm
Version:        380
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://invisible-island.net/xterm
Source0:        https://github.com/ThomasDickey/xterm-snapshots/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        https://ftp.invisible-island.net/archives/xterm/16colors.txt
Patch1:         xterm-defaults.patch
Patch2:         xterm-desktop.patch
Patch3:         xterm-man-paths.patch
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  libXaw-devel
BuildRequires:  libXext-devel
BuildRequires:  libXft-devel
BuildRequires:  libutempter-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig
BuildRequires:  xorg-x11-apps
Requires:       xterm-resize = %{version}-%{release}

%description
The xterm program is a terminal emulator for the X Window System. It
provides DEC VT102 and Tektronix 4014 compatible terminals for
programs that can't use the window system directly.

%package resize
Summary:        Set environment and terminal settings to current window size

%description resize
Prints a shell command for setting the appropriate environment variables to
indicate the current size of the window from which the command is run.

%prep
%autosetup -n %{name}-snapshots-%{name}-%{version} -p1

for f in THANKS; do
	iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
		touch -r ${f}{,_} && mv -f ${f}{_,}
done

%build
%configure \
	--enable-meta-sends-esc \
	--disable-backarrow-key \
	--enable-256-color \
	--enable-exec-xterm \
	--enable-luit \
%{?with_trace: --enable-trace} \
	--enable-warnings \
	--enable-wide-chars \
	--with-app-defaults=%{x11_app_defaults_dir} \
	--with-icon-theme=hicolor \
	--with-icondir=%{_datadir}/icons \
	--with-utempter \
	--with-tty-group=tty \
	--disable-full-tgetent \
	--enable-sixel-graphics

%make_build

%install
make DESTDIR=%{buildroot} install

cp -fp %{SOURCE1} 16colors.txt

desktop-file-install \
%if 0%{?fedora} && 0%{?fedora} < 19
	--vendor=fedora \
%endif
	--dir=%{buildroot}%{_datadir}/applications \
	xterm.desktop

mkdir -p %{buildroot}%{_datadir}/appdata
install -m644 -p xterm.appdata.xml %{buildroot}%{_datadir}/appdata

%files
%doc xterm.log.html ctlseqs.txt 16colors.txt README.i18n THANKS
%{_bindir}/xterm
%{_bindir}/koi8rxterm
%{_bindir}/uxterm
%{_mandir}/man1/koi8rxterm.1*
%{_mandir}/man1/uxterm.1*
%{_mandir}/man1/xterm.1*
%{_datadir}/appdata/xterm.appdata.xml
%{_datadir}/applications/*xterm.desktop
%{_datadir}/icons/hicolor/*/apps/*xterm*
%{_datadir}/pixmaps/*xterm*.xpm
%{x11_app_defaults_dir}/KOI8RXTerm*
%{x11_app_defaults_dir}/UXTerm*
%{x11_app_defaults_dir}/XTerm*

%files resize
%{_bindir}/resize
%{_mandir}/man1/resize.1*

%changelog
* Fri Aug 12 2022 Muhammad Falak <mwani@microsoft.com> - 380-1
- Bump version to address CVE-2022-45063 & CVE-2023-40359
- Refresh all patches to apply cleanly
- Use https instead of http for urls
- Switch to autosetup
- Switch to %make_build

* Fri Aug 12 2022 Muhammad Falak <mwani@microsoft.com> - 372-1
- Bump version to address CVE-2021-27135
- Refresh all patches to apply cleanly
- Switch url to `http` instead of `ftp`
- Cosmetic changes to spec formating
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 351-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 351-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Tomas Korbar <tkorbar@redhat.com> - 351-1
- update to 351

* Tue Nov 12 2019 Tomas Korbar <tkorbar@redhat.com> - 350-1
- update to 350

* Tue Oct 29 2019 Tomas Korbar <tkorbar@redhat.com> - 349-2
- enable sixel graphics (#1763712)

* Tue Sep 24 2019 Tomas Korbar <tkorbar@redhat.com> - 349-1
- update to 349

* Mon Aug 26 2019 Tomas Korbar <tkorbar@redhat.com> - 348-1
- update to 348

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 346-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 28 2019 Miroslav Lichvar <mlichvar@redhat.com> 346-1
- update to 346

* Tue May 14 2019 Miroslav Lichvar <mlichvar@redhat.com> 345-1
- update to 345

* Tue Feb 26 2019 Miroslav Lichvar <mlichvar@redhat.com> 344-1
- update to 344

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 334-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Miroslav Lichvar <mlichvar@redhat.com> 334-1
- update to 334

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 333-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 30 2018 Miroslav Lichvar <mlichvar@redhat.com> 333-2
- change default termName to xterm-256color (#1577159)

* Mon Apr 16 2018 Miroslav Lichvar <mlichvar@redhat.com> 332-1
- update to 332

* Thu Mar 29 2018 Miroslav Lichvar <mlichvar@redhat.com> 331-1
- update to 331
- add gcc to build requirements

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 330-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 330-4
- Remove obsolete scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 330-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 330-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Miroslav Lichvar <mlichvar@redhat.com> 330-1
- update to 330

* Mon Jun 12 2017 Miroslav Lichvar <mlichvar@redhat.com> 329-1
- update to 329

* Thu Jun 01 2017 Miroslav Lichvar <mlichvar@redhat.com> 328-1
- update to 328

* Mon Feb 06 2017 Miroslav Lichvar <mlichvar@redhat.com> 327-3
- recommend xorg-x11-fonts-misc (#487499)

* Wed Nov 16 2016 Jason L Tibbitts III <tibbs@math.uh.edu> 327-2
- move resize tool to a subpackage (#1349582)

* Mon Oct 10 2016 Miroslav Lichvar <mlichvar@redhat.com> 327-1
- update to 327

* Fri Oct 07 2016 Miroslav Lichvar <mlichvar@redhat.com> 326-1
- update to 326
- buildrequire xorg-x11-apps to get correct path of luit

* Wed Jun 08 2016 Miroslav Lichvar <mlichvar@redhat.com> 325-1
- update to 325

* Mon Mar 14 2016 Miroslav Lichvar <mlichvar@redhat.com> 324-1
- update to 324

* Tue Mar 08 2016 Miroslav Lichvar <mlichvar@redhat.com> 323-1
- update to 323

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 322-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Miroslav Lichvar <mlichvar@redhat.com> 322-1
- update to 322

* Thu Sep 03 2015 Miroslav Lichvar <mlichvar@redhat.com> 320-1
- update to 320

* Mon Aug 24 2015 Miroslav Lichvar <mlichvar@redhat.com> 319-1
- update to 319

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 318-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 16 2015 Miroslav Lichvar <mlichvar@redhat.com> 318-1
- update to 318

* Fri Mar 13 2015 Miroslav Lichvar <mlichvar@redhat.com> 316-1
- update to 316

* Tue Mar 03 2015 Miroslav Lichvar <mlichvar@redhat.com> 315-1
- update to 315

* Mon Jan 05 2015 Miroslav Lichvar <mlichvar@redhat.com> 314-1
- update to 314

* Mon Dec 08 2014 Adam Jackson <ajax@redhat.com> 313-2
- Don't BuildRequire: imake, we're not actually using it to build.

* Mon Dec 08 2014 Miroslav Lichvar <mlichvar@redhat.com> 313-1
- update to 313

* Mon Sep 29 2014 Miroslav Lichvar <mlichvar@redhat.com> 312-1
- update to 312

* Fri Sep 19 2014 Miroslav Lichvar <mlichvar@redhat.com> 311-1
- update to 311

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 310-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 29 2014 Miroslav Lichvar <mlichvar@redhat.com> 310-1
- update to 310

* Thu Jul 17 2014 Miroslav Lichvar <mlichvar@redhat.com> 309-1
- update to 309

* Mon Jun 23 2014 Miroslav Lichvar <mlichvar@redhat.com> 308-1
- update to 308

* Mon Jun 09 2014 Miroslav Lichvar <mlichvar@redhat.com> 306-1
- update to 306

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 305-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Miroslav Lichvar <mlichvar@redhat.com> 305-1
- update to 305

* Wed May 07 2014 Miroslav Lichvar <mlichvar@redhat.com> 304-1
- update to 304

* Tue Mar 11 2014 Miroslav Lichvar <mlichvar@redhat.com> 303-1
- update to 303

* Wed Mar 05 2014 Miroslav Lichvar <mlichvar@redhat.com> 302-1
- update to 302

* Tue Jan 21 2014 Miroslav Lichvar <mlichvar@redhat.com> 301-1
- update to 301

* Tue Dec 10 2013 Miroslav Lichvar <mlichvar@redhat.com> 300-1
- update to 300

* Tue Dec 03 2013 Miroslav Lichvar <mlichvar@redhat.com> 299-1
- update to 299

* Thu Nov 28 2013 Miroslav Lichvar <mlichvar@redhat.com> 298-1
- update to 298

* Thu Sep 19 2013 Miroslav Lichvar <mlichvar@redhat.com> 297-1
- update to 297

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 295-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Miroslav Lichvar <mlichvar@redhat.com> 295-1
- update to 295

* Wed May 29 2013 Miroslav Lichvar <mlichvar@redhat.com> 293-1
- update to 293

* Mon Apr 29 2013 Miroslav Lichvar <mlichvar@redhat.com> 292-1
- update to 292

* Thu Feb 28 2013 Miroslav Lichvar <mlichvar@redhat.com> 291-1
- update to 291

* Sun Feb 10 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 289-2
- Remove vendor tag from desktop file as per https://fedorahosted.org/fesco/ticket/1077

* Fri Feb 08 2013 Miroslav Lichvar <mlichvar@redhat.com> 289-1
- update to 289

* Thu Jan 10 2013 Miroslav Lichvar <mlichvar@redhat.com> 288-1
- update to 288

* Mon Nov 26 2012 Miroslav Lichvar <mlichvar@redhat.com> 287-1
- update to 287

* Tue Oct 30 2012 Miroslav Lichvar <mlichvar@redhat.com> 286-1
- update to 286

* Mon Oct 15 2012 Miroslav Lichvar <mlichvar@redhat.com> 284-1
- update to 284

* Wed Oct 10 2012 Miroslav Lichvar <mlichvar@redhat.com> 283-1
- update to 283
- install icon to hicolor theme and use it in desktop file (#804279)
- use new configure options to set some resource defaults (#819588)
- fix URL (#856957)
- remove obsolete macros

* Thu Oct 04 2012 Rex Dieter <rdieter@fedoraproject.org> 278-4
- revert bad -3 build

* Tue Sep 25 2012 Rex Dieter <rdieter@fedoraproject.org> 278-3
- xterm.desktop: +Path=$HOME

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 278-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 26 2012 Miroslav Lichvar <mlichvar@redhat.com> 278-1
- update to 278

* Mon Jan 09 2012 Miroslav Lichvar <mlichvar@redhat.com> 277-1
- update to 277

* Tue Oct 11 2011 Miroslav Lichvar <mlichvar@redhat.com> 276-1
- update to 276

* Mon Sep 12 2011 Miroslav Lichvar <mlichvar@redhat.com> 275-1
- update to 275

* Tue Aug 30 2011 Miroslav Lichvar <mlichvar@redhat.com> 273-1
- update to 273

* Fri Jul 15 2011 Miroslav Lichvar <mlichvar@redhat.com> 271-1
- update to 271

* Wed Apr 27 2011 Miroslav Lichvar <mlichvar@redhat.com> 270-1
- update to 270

* Mon Feb 21 2011 Miroslav Lichvar <mlichvar@redhat.com> 269-1
- update to 269

* Mon Feb 14 2011 Miroslav Lichvar <mlichvar@redhat.com> 268-1
- update to 268

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 267-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 23 2010 Miroslav Lichvar <mlichvar@redhat.com> 267-1
- update to 267

* Fri Nov 05 2010 Miroslav Lichvar <mlichvar@redhat.com> 266-1
- update to 266
- fix building with new libXaw

* Mon Oct 18 2010 Miroslav Lichvar <mlichvar@redhat.com> 264-1
- update to 264

* Tue Sep 07 2010 Miroslav Lichvar <mlichvar@redhat.com> 262-1
- update to 262

* Fri Jul 02 2010 Miroslav Lichvar <mlichvar@redhat.com> 261-2
- remove NoDisplay=true from desktop file, use upstream version (#607018)

* Tue Jun 29 2010 Miroslav Lichvar <mlichvar@redhat.com> 261-1
- update to 261

* Mon Jun 21 2010 Miroslav Lichvar <mlichvar@redhat.com> 260-1
- update to 260

* Thu Jun 10 2010 Miroslav Lichvar <mlichvar@redhat.com> 259-1
- update to 259
- link with -lICE
- convert THANKS to UTF-8

* Wed May 05 2010 Miroslav Lichvar <mlichvar@redhat.com> 258-1
- update to 258

* Tue Mar 09 2010 Miroslav Lichvar <mlichvar@redhat.com> 256-1
- update to 256
- enable XKB Bell support (#568748)

* Tue Feb 02 2010 Miroslav Lichvar <mlichvar@redhat.com> 255-1
- update to 255

* Fri Dec 11 2009 Miroslav Lichvar <mlichvar@redhat.com> 253-1
- update to 253

* Tue Dec 08 2009 Miroslav Lichvar <mlichvar@redhat.com> 252-1
- update to 252

* Thu Nov 19 2009 Miroslav Lichvar <mlichvar@redhat.com> 251-1
- update to 251

* Tue Oct 20 2009 Miroslav Lichvar <mlichvar@redhat.com> 250-1
- update to 250

* Thu Oct 08 2009 Miroslav Lichvar <mlichvar@redhat.com> 249-1
- update to 249

* Tue Sep 29 2009 Miroslav Lichvar <mlichvar@redhat.com> 248-2
- fix various bugs when display is scrolled up (#524503)

* Thu Sep 17 2009 Miroslav Lichvar <mlichvar@redhat.com> 248-1
- update to 248

* Tue Sep 01 2009 Miroslav Lichvar <mlichvar@redhat.com> 247-1
- update to 247

* Tue Aug 18 2009 Miroslav Lichvar <mlichvar@redhat.com> 246-1
- update to 246

* Thu Aug 13 2009 Miroslav Lichvar <mlichvar@redhat.com> 245-1
- update to 245

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 242-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 02 2009 Miroslav Lichvar <mlichvar@redhat.com> 242-3
- fix bell (#487829)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 242-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Miroslav Lichvar <mlichvar@redhat.com> 242-1
- update to 242
- use upstream default value for modifyFunctionKeys resource
- remove png suffix from icon name in desktop file

* Tue Jan 06 2009 Miroslav Lichvar <mlichvar@redhat.com> 238-1
- update to 238 (#479000, CVE-2008-2383)
- set default values of allowWindowOps and allowFontOps resources to false

* Tue Sep 16 2008 Miroslav Lichvar <mlichvar@redhat.com> 237-1
- update to 237

* Wed Jul 30 2008 Miroslav Lichvar <mlichvar@redhat.com> 236-1
- update to 236
- enable support for spawn-new-terminal action (#457130)

* Tue Apr 22 2008 Miroslav Lichvar <mlichvar@redhat.com> 235-1
- update to 235

* Mon Mar 03 2008 Miroslav Lichvar <mlichvar@redhat.com> 234-1
- update to 234

* Wed Feb 27 2008 Miroslav Lichvar <mlichvar@redhat.com> 233-1
- update to 233

* Thu Jan 31 2008 Miroslav Lichvar <mlichvar@redhat.com> 232-1
- update to 232

* Mon Jan 07 2008 Miroslav Lichvar <mlichvar@redhat.com> 231-1
- update to 231
- remove setgid utempter from xterm binary (#229360)

* Fri Jan 04 2008 Miroslav Lichvar <mlichvar@redhat.com> 230-1
- update to 230

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 229-2
- rebuild

* Mon Aug 13 2007 Miroslav Lichvar <mlichvar@redhat.com> 229-1
- update to 229

* Mon Jul 23 2007 Miroslav Lichvar <mlichvar@redhat.com> 228-1
- update to 228

* Fri Jun 29 2007 Miroslav Lichvar <mlichvar@redhat.com> 227-1
- update to 227

* Fri Jun 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 226-1
- update to 226

* Thu Apr 12 2007 Miroslav Lichvar <mlichvar@redhat.com> 225-2
- fix sections in man pages

* Tue Mar 27 2007 Miroslav Lichvar <mlichvar@redhat.com> 225-1
- update to 225

* Tue Mar 20 2007 Miroslav Lichvar <mlichvar@redhat.com> 224-2
- fix background color setting in alternate screen
- don't display xterm in menus (#231000)

* Fri Feb 16 2007 Miroslav Lichvar <mlichvar@redhat.com> 224-1
- update to 224
- drop utempter group before creating pty
- add Icon to desktop file (#227925)

* Wed Feb 07 2007 Miroslav Lichvar <mlichvar@redhat.com> 223-3
- spec cleanup (#226660)

* Thu Jan 18 2007 Miroslav Lichvar <mlichvar@redhat.com> 223-2
- make xterm binary sgid utempter (#222847)
- fix font size changes with -fa option (#222340)
- fix redrawing of internal border (#223027)
- enable metaSendsEscape resource and set modifyFunctionKeys to 0 by default

* Thu Dec 07 2006 Miroslav Lichvar <mlichvar@redhat.com> 223-1
- update to 223

* Thu Nov 23 2006 Miroslav Lichvar <mlichvar@redhat.com> 222-1
- update to 222
- link with libncurses instead of libtermcap
- spec cleanup

* Mon Sep 04 2006 Miroslav Lichvar <mlichvar@redhat.com> 215-3.fc6
- fix segfault when /etc/termcap is missing (#201246)

* Wed Jul 26 2006 Mike A. Harris <mharris@redhat.com> 215-2.fc6
- Replace BuildRequires utempter with libutempter-devel
- Change BuildRoot tag to comply with Fedora packaging guidelines
- Use pkg-config to autodetect the location of the system app-defaults dir
- Add BuildRequires: pkgconfig

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 215-1.fc6
- Upgrade to upstream version 215

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 213-2.1
- rebuild

* Tue Jul 11 2006 Adam Jackson <ajackson@redhat.com> - 213-2.fc6
- Use correct dist tag in Release string.

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 213-1
- Upgrade to upstream version 213 (fixes bug 192627)
- fix bug 189161 : make -r/-rv do reverseVideo with or without
  xterm*{fore,back}ground set

* Thu Apr 13 2006 Jason Vas Dias <jvdias@redhat.com> - 212-1
- Upgrade to upstream version 212
- fix bug 188031 : paths in man-page

* Wed Mar 29 2006 Jason Vas Dias <jvdias@redhat.com> - 211-4
- fix bug 186935: cursor GCs must be freed with XtReleaseGC

* Tue Mar 21 2006 Jason Vas Dias <jvdias@redhat.com> - 211-1
- Upgrade to upstream version 211 (fixes bug 186094).
- Enable new 'utf8Title' resource by default

* Tue Mar 07 2006 Jason Vas Dias <jvdias@redhat.com> - 209-4
- fix bug 183993: call set_cursor_gcs in ReverseVideo

* Wed Feb 22 2006 Jason Vas Dias <jvdias@redhat.com> - 209-2
- fix bug 182382: check for (VWindow(screen)!=0) in set_cursor_gcs
- further fix for bug 178302: allow *vt100*cursorColor to be same as fg

* Tue Feb 14 2006 Jason Vas Dias <jvdias@redhat.com> - 209-1
- Upgrade to upstream version 209 (fixes bug 180450)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 208-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 208-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Jason Vas Dias<jvdias@redhat.com> - 208-1
- Upgrade to upstream version 208
- Allow root user to grab the console, even if /dev/console 
  not owned by root
- restore Red Hat '*VT100*scrollBar:1' default Xresource

* Wed Dec 21 2005 Jason Vas Dias<jvdias@redhat.com> - 207-10
- Fix bug 164210: tek4014 support should be enabled by default

* Wed Dec 14 2005 Jason Vas Dias<jvdias@redhat.com> - 207-8
- Fix bug 175684: compile with --enable-256-color
- Fix bug 155538 addenda - restore '*VT100*backarrowKey:0'

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Jason Vas Dias<jvdias@redhat.com> - 207-5
- fix bug 173703: remove reference to /usr/X11R6/bin/luit :
  PROJECTROOT should be /usr, not /usr/X11R6

* Fri Nov 18 2005 Jason Vas Dias<jvdias@redhat.com> - 207-4
- fix bug 173541: better fix for freetype configuration problem

* Mon Nov 14 2005 Jason Vas Dias<jvdias@redhat.com> - 207-1
- Upgrade to upstream version 207
- Fix app-defaults directory for modular X11

* Sun Nov 13 2005 Jeremy Katz <katzj@redhat.com> - 206-4
- rebuild for newer modular X

* Fri Nov 04 2005 Jason Vas Dias <jvdias@redhat.com> 206-1
- Upgrade to upstream version 206

* Wed Oct 12 2005 Jason Vas Dias <jvdias@redhat.com> 205-1
- Upgrade to upstream version 205 
  fixes bugs: 124421, 129146, 159562, 161894, 169347

* Sat Sep 24 2005 Mike A. Harris <mharris@redhat.com> 200-10
- Updated xterm-resources-redhat.patch to add "xterm*ttyModes: erase ^?"
  resource to fix bug (#155538,160354,163812,162549)

* Wed Sep 14 2005 Mike A. Harris <mharris@redhat.com> 200-9
- Updated xterm-resources-redhat.patch to remove utf8 resource which was
  added in the 200-7 build, as it was incorrectly set to 'true' instead
  of '1', and bug #138681 turned out to be a gdm bug instead of an xterm
  bug.  This fixes bug (#163568).

* Mon Aug 29 2005 Mike A. Harris <mharris@redhat.com> 200-8
- Added --disable-tek4014 to ./configure flags, to disable tek support
  for bug (#164210)

* Mon May 2 2005 Mike A. Harris <mharris@redhat.com> 200-7
- Updated xterm-resources-redhat.patch to enable xterm utf8 resource by
  default, as our default OS environment is UTF-8, for bug (#138681)

* Sat Apr 16 2005 Mike A. Harris <mharris@redhat.com> 200-6
- Added option to spec file to allow easy rebuilding with 256 color option
  for those who prefer this non-default behaviour (#103402)

* Tue Mar 8 2005 Soeren Sandmann <sandmann@redhat.com> 200-5
- Ported xterm-resources-redhat.patch to newer xterms. (#126855)

* Sun Mar 6 2005 Mike A. Harris <mharris@redhat.com> 200-4
- Added libtermcap-devel and utempter to BuildRequires
- Changed BuildRequires from XFree86-devel to xorg-x11-devel

* Sun Mar 6 2005 Mike A. Harris <mharris@redhat.com> 200-3
- Rebuild with gcc 4 for FC4 development

* Mon Feb 7 2005 Mike A. Harris <mharris@redhat.com> 200-2
- Removed chmod from prep, and updated comment to refect (#128341c12)

* Mon Feb 7 2005 Mike A. Harris <mharris@redhat.com> 200-1
- Updated main tarball to xterm-200 for FC4 devel
- Disabled xterm-179-ppc-fix-bug-101472.patch for now, to see if the problem
  occurs on ppc still or not.

* Tue Jul 13 2004 Mike A. Harris <mharris@redhat.com> 192-1
- Updated main tarball to xterm-192 for FC3 devel
- Resolved bugs #126569,127132

* Fri Jun 18 2004 Mike A. Harris <mharris@redhat.com> 191-1
- Updated main tarball to xterm-191 for FC3 devel
- Disabled xterm-resources-redhat.patch to see what if anything breaks, as
  it no longer applies cleanly.  Hopefully we can just ship stock xterm
  resources now, although I realize that is more likely to be a pie in the
  sky fantasy once the bug reports trickle in from this change.  ;o)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 179-8
- rebuilt

* Thu Jun  3 2004 Mike A. Harris <mharris@redhat.com> 179-7
- Rebuilt for FC3 devel

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 179-6.EL
- rebuilt

* Mon Sep  8 2003 Mike A. Harris <mharris@redhat.com> 179-5.EL
- Rebuilt 179-5 for Taroon

* Mon Sep  8 2003 Mike A. Harris <mharris@redhat.com> 179-5
- Added xterm-179-ppc-fix-bug-101472.patch ifarch ppc ppc64 to fix bug (#101472)

* Wed Aug 27 2003 Bill Nottingham <notting@redhat.com> 179-4.1
- fix symlink
- rebuild

* Wed Aug 13 2003 Mike A. Harris <mharris@redhat.com> 179-3.EL
- Rebuilt for Taroon with symlink fixes.

* Wed Aug 13 2003 Mike A. Harris <mharris@redhat.com> 179-3
- Added symlink /usr/X11R6/bin/xterm pointing to _bindir/xterm so that apps
  and scripts which invoke xterm explicitly as /usr/X11R6/bin/xterm, will
  continue to work correctly without surprises (#101994)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 179-2.EL
- rebuilt

* Fri May 30 2003 Mike A. Harris <mharris@redhat.com> 179-1.EL
- Bump release to 1.EL for Red Hat Enterprise Linux build

* Mon May 26 2003 Mike A. Harris <mharris@redhat.com> 179-1
- Updated to upstream xterm 179
- [SECURITY] Added xterm-can-2003-0063.patch from XFree86 4.3.0-12 package
- Added Red Hat xterm-resources-redhat.patch from XFree86 4.3.0-12 package
- Added "chmod -R u+w *" after source is decompressed or else patches can not
  be applied due to upstream source being read only files
- Built xterm 179-1 in rawhide

* Mon May  5 2003 Mike A. Harris <mharris@redhat.com> 177-2.0.EL
- Bump release to 2.0.EL for Red Hat Enterprise Linux build

* Mon May  5 2003 Mike A. Harris <mharris@redhat.com> 177-2
- Build fix for lib64: _x11datadir == /usr/X11R6/lib
- Another lib64 build fix:  xterm uses /usr/%%{_lib}/X11/app-defaults when it
  should be using an arch-neutral dir {_x11datadir}/X11/app-defaults instead

* Tue Apr 15 2003 Mike A. Harris <mharris@redhat.com> 177-1
- Call configure with "--enable-luit --enable-warnings --enable-wide-chars
  --with-utempter"
- Initial build.
