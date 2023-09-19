Summary:        Recompression utilities for .png, .mng, .zip and .gz files
Name:           advancecomp
Version:        2.5
Release:        1%{?dist}
# Source file headers all specify GPL-2.0-or-later (see source file headers),
# except:
#
#   The bundled and forked 7z (7-Zip code) in 7z/ is under the “LGPL” license.
#   Based on https://www.7-zip.org/license.txt, and the absence of any mention
#   of license changes in https://www.7-zip.org/history.txt, 7-Zip has always
#   been licensed under LGPL-2.1-or-later, specifically; we thus assume this is
#   the intended specific license for the contents of the 7z/ directory. None
#   of the sources that would be covered by the “unRAR license restriction” or
#   the BSD-3-Clause license for LZFSE are present in this fork.
#
#   Certain build-system files, which do not contribute to the license of the
#   binary RPM, are under other permissible licenses.
#
# However, in version 1.17, the COPYING file was updated to GPLv3, with a
# changelog message (in HISTORY and elsewhere) of “Changes to GPL3.” We
# interpret this as an overall license of GPL-3.0-only.
License:        GPL-3.0-only AND GPL-2.0-or-later AND LGPL-2.1-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.advancemame.it/
Source0:        https://github.com/amadvance/advancecomp/archive/v%{version}/advancecomp-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  dos2unix
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig
# System library supported by upstream
BuildRequires:  zlib-devel
BuildRequires:  zopfli-devel
# Unbundled downstream
BuildRequires:  pkgconfig(libdeflate)
# From 7z/README:
#
#   This directory contains some source files from the
#   7z archive utility. (www.7-zip.org)
#
#   All the files in this directory was originally released
#   with the LGPL license.
#
#   All the modifications made on the original files must
#   be considered Copyright (C) 2002 Andrea Mazzoleni and
#   released under the LGPL license.
#
# It is not clear which version was forked. Because 7-Zip does not provide a
# library, and because the implementation is modified, there is no possibility
# of unbundling. Note that this was forked from the original 7-Zip, not from
# p7zip.
Provides:       bundled(7zip)

%description
AdvanceCOMP contains recompression utilities for your .zip archives,
.png images, .mng video clips and .gz files.

The official site of AdvanceCOMP is:

  https://www.advancemame.it

This package contains:
  advzip - Recompression and test utility for zip files
  advpng - Recompression utility for png files
  advmng - Recompression utility for mng files
  advdef - Recompression utility for deflate streams in .png, .mng and .gz files

%prep
%autosetup -p1
dos2unix -k doc/*.txt

# Patch out bundled libdeflate
rm -rvf libdeflate
sed -r -i '/libdeflate[\/_]/d' Makefile.am
# Fix up #include paths. The find-then-modify pattern keeps us from discarding
# mtimes on any sources that do not need modification.
find . -type f -exec gawk \
    '/^[[:blank:]]*#include.*libdeflate/ { print FILENAME; nextfile }' \
    '{}' '+' |
  xargs -r -t sed -r -i 's@^([[:blank:]]*#include.*)libdeflate/@\1@'

# Patch out bundled zopfli
rm -rvf zopfli
sed -r -i \
    -e '/zopfli[\/_]/d' \
    -e 's/((\(7z_SOURCES\)|WindowOut\.h).*)[[:blank:]]*\\/\1/' \
    Makefile.am
# Fix up #include paths. The find-then-modify pattern keeps us from discarding
# mtimes on any sources that do not need modification.
find . -type f -exec gawk \
    '/^[[:blank:]]*#include.*zopfli/ { print FILENAME; nextfile }' \
    '{}' '+' |
  xargs -r -t sed -r -i -e 's@^([[:blank:]]*#include.*)zopfli/@\1@'


%build
%{set_build_flags}
autoreconf --force --install --verbose

# Link against system libdeflate
export CFLAGS="$(pkgconf --cflags libdeflate) ${CFLAGS-}"
export CXXFLAGS="$(pkgconf --cflags libdeflate) ${CXXFLAGS-}"
export LDFLAGS="$(pkgconf --libs libdeflate) ${LDFLAGS-}"

# Link against system zopfli
export LDFLAGS="-lzopfli ${LDFLAGS-}"

%configure
%make_build


%install
%make_install


# We don’t run upstream tests (%%make_build check) because they are too
# brittle, expecting recompressed outputs to be identical. Across platforms,
# compilers, and unbundled library versions, this doesn’t hold up.


%files
%license COPYING
%doc AUTHORS
%doc HISTORY
%doc README
%doc doc/adv{def,mng,png,zip}.txt

%{_bindir}/adv{def,mng,png,zip}
%{_mandir}/man1/adv{def,mng,png,zip}.1*

%changelog
* Tue Sep 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.5-1
- Auto-upgrade to 2.5 - CVE-2023-2961

* Wed Jan 18 2023 Suresh Thelkar <sthelkar@microsoft.com> - 2.4-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Thu Nov 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.4-1
- Update to 2.4 (close RHBZ#2145023)
- Security fix for CVE-2022-35014, CVE-2022-35015, CVE-2022-35016,
  CVE-2022-35017, CVE-2022-35018, CVE-2022-35019, CVE-2022-35020

* Thu Nov 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> 2.3-5
- Identify bundled 7-Zip as “7zip” rather than “7z”

* Thu Nov 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> 2.3-4
- Add a comment about upstream tests

* Thu Nov 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> 2.3-3
- Stricter file globs

* Wed Sep 28 2022 Benjamin A. Beasley <code@musicinmybrain.net> 2.3-2
- Drop EPEL conditionals from Fedora branches

* Wed Sep 28 2022 Benjamin A. Beasley <code@musicinmybrain.net> 2.3-1
- Update to 2.3 (close RHBZ#2075857)

* Wed Sep 28 2022 Benjamin A. Beasley <code@musicinmybrain.net> 2.1-29
- Update License to SPDX

* Wed Sep 28 2022 Benjamin A. Beasley <code@musicinmybrain.net> 2.1-28
- Drop {authors,history,readme}.txt

* Sat Sep 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.1-21
- Spec file formatting tweaks
- Convert URLs from HTTP to HTTPS
- Use modern spec file macros (make_build/make_install/etc.)
- Unbundle libdeflate
- Unbundle zopfli where it is available as a system library (i.e., Fedora)
- Remove unnecessary BR on tofrodos
- Properly document bundled 7z code

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-16
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Jeff Law <law@redhat.com> - 2.1-15
- Force C++14 as the code is not ready for C++17

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 Than Ngo <than@redhat.com> - 2.1-11
- Backport for #1708563, CVE-2019-8383 - denial of service in function adv_png_unfilter_8

* Wed Mar 06 2019 Than Ngo <than@redhat.com> - 2.1-10
- Backport, fix a buffer overflow with image of invalid size

* Fri Mar 01 2019 Than Ngo <than@redhat.com> - 2.1-9
- fixed CVE-2019-9210 advancecomp: integer overflow in png_compress in pngex.cc

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Matthias Saou <matthias@saou.eu> 2.1-7
- Fix doc EOL.
- Minor cosmetic updates (summary, description...).

* Sat Jul 14 2018 Christian Dersch <lupinix@fedoraproject.org> - 2.1-6
- BuildRequires: gcc-c++

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Than Ngo <than@redhat.com> - 2.1-4
- updated to 2.1 (fix CVE-2018-1056)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 28 2017 Christian Dersch <lupinix@mailbox.org> - 1.23-1
- new version

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 13 2016 Christian Dersch <lupinix@mailbox.org> - 1.20-3
- revert to 1.20, 1.22 does not build and also needs unbundling of libdeflate first

* Sun Nov 13 2016 Christian Dersch <lupinix@mailbox.org> - 1.22-1
- new version

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 05 2015 Christian Dersch <lupinix@fedoraproject.org> - 1.20-1
- new version 1.20
- use license tag

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.19-4
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Christopher Meng <rpm@cicku.me> - 1.19-1
- Update to 1.19

* Mon Feb 10 2014 Christopher Meng <rpm@cicku.me> - 1.18-1
- Update to 1.18

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.15-16
- Add disttag, modernise spec file

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-15
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.15-10
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 1.15-9
- Rebuild for new BuildID feature.

* Fri Aug  3 2007 Matthias Saou <http://freshrpms.net/> 1.15-8
- Update License field.
- Remove dist tag, since the package will seldom change.

* Thu Mar 29 2007 Matthias Saou <http://freshrpms.net/> 1.15-7
- Switch to using DESTDIR install method.

* Thu Mar 29 2007 Matthias Saou <http://freshrpms.net/> 1.15-6
- Switch to use downloads.sf.net source URL.
- Tweak defattr.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 1.15-5
- FC6 rebuild, remove gcc-c++ build requirement (it's a default).

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 1.15-4
- FC5 rebuild.

* Wed Feb  8 2006 Matthias Saou <http://freshrpms.net/> 1.15-3
- Rebuild for new gcc/glibc.

* Tue Jan 24 2006 Matthias Saou <http://freshrpms.net/> 1.15-2
- Rebuild for FC5.

* Wed Nov  2 2005 Matthias Saou <http://freshrpms.net/> 1.15-1
- Update to 1.15, includes 64bit fixes.

* Fri May 27 2005 Matthias Saou <http://freshrpms.net/> 1.14-5
- Update 64bit patch to a cleaner approach as Ralf suggested.

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 1.14-4
- fix build on 64bit arches

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.14-3
- rebuild on all arches

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.14-2
- rebuilt

* Wed Feb 23 2005 Matthias Saou <http://freshrpms.net/> 1.14-1
- Update to 1.14.

* Mon Nov 29 2004 Matthias Saou <http://freshrpms.net/> 1.13-1
- Update to 1.13.

* Tue Nov  2 2004 Matthias Saou <http://freshrpms.net/> 1.12-1
- Update to 1.12.

* Tue Aug 24 2004 Matthias Saou <http://freshrpms.net/> 1.11-1
- Update to 1.11.

* Mon May 17 2004 Matthias Saou <http://freshrpms.net/> 1.10-1
- Update to 1.10.

* Mon Nov  3 2003 Matthias Saou <http://freshrpms.net/> 1.7-2
- Rebuild for Fedora Core 1.
- Added missing build dependencies, thanks to mach.

* Tue Aug 26 2003 Matthias Saou <http://freshrpms.net/>
- Update to 1.7.

* Thu May 22 2003 Matthias Saou <http://freshrpms.net/>
- Initial RPM release.
