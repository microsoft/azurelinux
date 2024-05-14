Summary:        A Program for Extracting, Verifying, and Fixing Audio Tracks from CDs
Name:           cdparanoia
Version:        10.2
Release:        1%{?dist}
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Productivity/Multimedia/CD/Grabbers
URL:            https://www.xiph.org/paranoia/index.html
Source:         https://downloads.xiph.org/releases/%{name}/%{name}-III-%{version}.src.tgz
Patch0:         010_build_system.patch
Patch1:         cdparanoia-III-ide_majors.patch
Patch2:         cdparanoia-III-c++.patch
Patch3:         050_all_build_only_shared_libraries.patch
Patch4:         cdparanoia-III-01-typos-and-spelling.patch
Patch5:         cdparanoia-III-05-gcc4.3.patch
Patch6:         cdparanoia-III-06-endian.patch
Patch7:         config-guess-sub-update.patch
BuildRequires:  autoconf
BuildRequires:  automake
Provides:       cdparano = %{version}
Obsoletes:      cdparano < %{version}

%package -n libcdda_interface0
Summary:        Library for Extracting, Verifying, and Fixing Audio Tracks from CDs
License:        LGPL-2.1-or-later
Group:          System/Libraries
Suggests:       ImageMagick-extra = %{version}

%package -n libcdda_paranoia0
Summary:        Library for Extracting, Verifying, and Fixing Audio Tracks from CDs
License:        LGPL-2.1-or-later
Group:          System/Libraries

%package devel
Summary:        Development files for cdparanoia, a library for extractnig audio tracks from CDs
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++
Requires:       libcdda_interface0 = %{version}
Requires:       libcdda_paranoia0 = %{version}

%description
This CDDA reader distribution ('cdparanoia') reads audio from the
CD-ROM directly as data and writes the data to a file or pipe as .wav,
.aifc, or raw 16-bit linear PCM.

%description devel
This CDDA reader distribution ('cdparanoia') reads audio from the
CD-ROM directly as data and writes the data to a file or pipe as .wav,
.aifc, or raw 16-bit linear PCM.

%description -n libcdda_interface0
This CDDA reader distribution ('cdparanoia') reads audio from the
CD-ROM directly as data and writes the data to a file or pipe as .wav,
.aifc, or raw 16-bit linear PCM.

%description -n libcdda_paranoia0
This CDDA reader distribution ('cdparanoia') reads audio from the
CD-ROM directly as data and writes the data to a file or pipe as .wav,
.aifc, or raw 16-bit linear PCM.

%prep
%autosetup -p1 -n %{name}-III-%{version}

%build
autoreconf -vfi

%configure
# Disabling "format-security" warnings enabled by default on Mariner.
%make_build OPT="%{optflags} -Wno-format-security"

%install
make prefix=%{buildroot}%{_prefix} \
     LIBDIR=%{buildroot}%{_libdir} \
     MANDIR=%{buildroot}%{_mandir} \
     BINDIR=%{buildroot}%{_bindir} \
     INCLUDEDIR=%{buildroot}%{_includedir} \
       install
JAPN_MANDIR=%{buildroot}%{_mandir}/ja/man1
mkdir -p $JAPN_MANDIR
install -m644 cdparanoia.1.jp $JAPN_MANDIR/cdparanoia.1

%post -n libcdda_interface0 -p /sbin/ldconfig
%postun -n libcdda_interface0 -p /sbin/ldconfig
%post -n libcdda_paranoia0 -p /sbin/ldconfig
%postun -n libcdda_paranoia0 -p /sbin/ldconfig

%files
%doc README
%license COPYING-GPL
%{_mandir}/man1/*
%{_mandir}/ja
%{_bindir}/*

%files -n libcdda_interface0
%license COPYING-LGPL
%{_libdir}/libcdda_interface.so.0
%{_libdir}/libcdda_interface.so.0.*

%files -n libcdda_paranoia0
%license COPYING-LGPL
%{_libdir}/libcdda_paranoia.so.0
%{_libdir}/libcdda_paranoia.so.0.*

%files devel
%{_includedir}/*
%{_libdir}/libcdda_paranoia.so
%{_libdir}/libcdda_interface.so

%changelog
* Wed Nov 23 2022 Sumedh Sharma <sumsharma@microsoft.com> - 10.2-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag)
- Converting the 'Release' tag to the '[number].[distribution]' format
- License verified

* Wed Apr 18 2018 jengelh@inai.de
- Update descriptions.

* Wed Apr 18 2018 tchvatal@suse.com
- Do not bother to talk about it being beta release as we
  are shipping this since 2008

* Wed Apr 18 2018 adam.majer@suse.de
- Adjust licenses to be installed with %%license not %%doc
- libraries are covered by LGPL-2.1-or-greater and the command-line
  tool is GPL-2.0-or-greater

* Tue Apr 17 2018 schwab@suse.de
- config-guess-sub-update.diff: update for RISC-V support

* Thu Oct 24 2013 tchvatal@suse.com
- Redo the buildsystem to use only shared libs and allow parallel
  building to have it faster in obs.
  * removed patches:
  - cdparanoia-III-dt_needed.patch
  - cdparanoia-large-pic.diff
  * added patches:
  - 010_build_system.patch
  - 050_all_build_only_shared_libraries.patch

* Tue May 21 2013 dmueller@suse.com
- add config-guess-sub-update.diff:
  * configure.guess/sub update for aarch64 support

* Thu Mar 21 2013 mmeister@suse.com
- Added url as source.
  Please see https://en.opensuse.org/SourceUrls

* Sun Jul 15 2012 coolo@suse.com
- own directories for japanese man pages, no need to buildrequire man
  for that

* Tue Dec 20 2011 coolo@suse.com
- remove call to suse_update_config (very old work around)

* Wed Oct  5 2011 uli@suse.com
- cross-build fixes: use %%configure macro, set bindir and include
  dir explicitly when installing

* Thu Jan  7 2010 jengelh@medozas.de
- Add baselibs.conf as a source
- Switch from -fpic to -fPIC, at least SPARC needs this

* Wed Aug  5 2009 vuntz@novell.com
- Make the devel package require libcdda_interface0 and
  libcdda_paranoia0 instead of cdparanoia.

* Thu Feb 26 2009 nadvornik@suse.cz
- updated to III-10.2
  * many patches merged upstream
- adapted according to shared library policy
  * new subpackage libcdda_interface0
  * new subpackage libcdda_paranoia0
  * new subpackage cdparanoia-devel
- added debian patches
  cdparanoia-III-01-typos-and-spelling.dpatch
  cdparanoia-III-05-gcc4.3.dpatch
  cdparanoia-III-06-endian.dpatch

* Wed Dec 10 2008 olh@suse.de
- use Obsoletes: -XXbit only for ppc64 to help solver during distupgrade
  (bnc#437293)

* Thu Oct 30 2008 olh@suse.de
- obsolete old -XXbit packages (bnc#437293)

* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support

* Wed Aug  8 2007 pgajdos@suse.cz
- solved 'Lack of SG_IO interface support' [#295308]
  * shortened gcc34.patch (leaved in hunks for utils.h only, removed
  hunks for scsi_interface.c)
  * new patch sgio.patch to solve error mentioned above
  * new patch gcc34-2.patch (avoid persisting problems with
    compilation -- memcpy macro)

* Fri Oct 27 2006 lnussel@suse.de
- remove resmgr patch

* Mon Jun 12 2006 dmueller@suse.de
- add DT_NEEDED for libcdda_interface to libccda_paranoia (#183849)

* Fri May 26 2006 schwab@suse.de
- Don't strip binaries.

* Tue May 23 2006 nadvornik@suse.cz
- check for all IDE major numbers

* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires

* Wed Aug 10 2005 nadvornik@suse.cz
- use RPM_OPT_FLAGS instead of hardcoded CFLAGS [#93874]
- fixed compiler warnings

* Mon Feb  7 2005 nadvornik@suse.cz
- do not dereference symlinks in resmgr device name [#44912]

* Wed Sep 15 2004 ro@suse.de
- don't use --host for configure

* Wed Jan 28 2004 schwab@suse.de
- Fix missing library dependency.

* Sat Jan 17 2004 meissner@suse.de
- fixed labels at end of compound statement problem.

* Sun Jan 11 2004 adrian@suse.de
- add %%run_ldconfig

* Mon May 19 2003 meissner@suse.de
- remove .a files, they are not packaged.

* Fri Feb 28 2003 meissner@suse.de
- Added resmgr support so cdparanoia can read audio CDs on
  SCSI CD-ROMs (and ide-scsi based IDE CD-ROMs).

* Tue Sep 24 2002 nadvornik@suse.cz
- fixed crash with k3b [#18282]

* Tue Sep 17 2002 ro@suse.de
- removed bogus self-provides

* Thu Apr 25 2002 coolo@suse.de
- use %%_libdir

* Wed Jun 13 2001 schwab@suse.de
- Fix stupid file names.

* Mon Apr  2 2001 bk@suse.de
- update to III-alpha9.8
- remove of static libs from filelist(shared libs are used by e.g. kde)

* Thu Nov  9 2000 nadvornik@suse.cz
- renamed cdparano -> cdparanoia

* Wed Apr 26 2000 nadvornik@suse.cz
- changed Group

* Mon Apr 10 2000 nadvornik@suse.cz
- added BuildRoot
- added URL

* Tue Feb 29 2000 uli@suse.de
- fixed filelist (this time for real)
- now builds with "-O2" instead of "-O20"

* Tue Feb 29 2000 ro@suse.de
- fixed filelist

* Mon Jan 17 2000 ro@suse.de
- update to III-alpha9.7
- man to /usr/share/man

* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.

* Fri Sep  3 1999 ro@suse.de
- update to III-alpha9.6

* Fri Jul  9 1999 ro@suse.de
- update to alpha9.5

* Tue Sep 22 1998 ro@suse.de
- update to alpha8 / define _GNU_SOURCE for compiling

* Tue Aug  4 1998 ro@suse.de
- update to alpha7

* Fri Apr 24 1998 ro@suse.de
- build initial package version 03alpha6
