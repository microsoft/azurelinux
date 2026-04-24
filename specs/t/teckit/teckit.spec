# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           teckit
Version:        2.5.13
Release: 3%{?dist}
Summary:        Encoding conversion library and mapping compiler
# COPYING:                      links to license/LICENSING.txt
# license/License_CPLv05.txt:   CPL-1.0 text, "0.5" version in the license
#                               title is irrelevant
#                               <https://gitlab.com/fedora/legal/fedora-license-data/-/issues/160>
# license/License_LGPLv21.txt:  LGPL-2.1 text
# license/LICENSING.txt:        license declarations
# SFconv/UtfCodec.cpp:      LGPL-2.1-or-later OR GPL-2.0-or-later OR MPL-2.0 (bundled Graphite2)
# SFconv/UtfCodec.h:        LGPL-2.1-or-later OR GPL-2.0-or-later OR MPL-2.0 (bundled Graphite2)
#                           MPL version clarified at <https://github.com/silnrsi/graphite/issues/58>,
# source/Engine.cpp:        LGPL-2.1-or-later OR CPL-1.0, CPL-1.0 identifier already
#                           encompases "or later" choice
#                           <https://gitlab.com/fedora/legal/fedora-license-data/-/issues/160>
# source/TECkit_Format.h:   LGPL-2.1-or-later OR CPL-0.5-or-later
## Not in any binary package
# debian-src/copyright: LGPL-2.0-or-later
# perl_binaries:        precompiled source/Perl
# repackage.sh:         GPL-2.0-or-later
# SFconv/SFconv_ver.rc: LGPL-2.1-or-later OR CPL-0.5-or-later
# source/Compiler_ver.rc:   LGPL-2.1-or-later OR CPL-0.5-or-later
# source/Sample-tools/TECkit_Compile_ver.rc:    LGPL-2.1-or-later OR CPL-0.5-or-later
# source/Sample-tools/TxtConv_ver.rc:           LGPL-2.1-or-later OR CPL-0.5-or-later
# source/Sample-tools/version_defs.h:           LGPL-2.1-or-later OR CPL-0.5-or-later
# source/teckitjni/COPYING:     GPL-2.0 text
# source/teckitjni/java/org/sil/scripts/teckit/TecKitJni.java:  LGPL-2.1-or-later OR CPL-0.5-or-later
# source/teckitjni/ltmain.sh:   GPL-2.0-or-later WITH Autoconf-exception-generic
# source/teckitjni/missing:     GPL-2.0-or-later WITH Autoconf-exception-generic
# source/teckitjni/src/teckitjniTest.cpp:   GPL-2.0-or-later
# source/teckitjni/templates/cpp:           GPL-2.0-or-later
# source/teckitjni/templates/h:             GPL-2.0-or-later
# source/version_defs.h:        LGPL-2.1-or-later OR CPL-0.5-or-later
# test/NormalizationTest.txt:   Unicode-3.0
## Unbundled
# SFconv/expat/xmlparse/hashtable.c:    MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlparse/hashtable.h:    MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlparse/Makefile.in:    NPL-1.1
# SFconv/expat/xmlparse/makefile.win:   NPL-1.1
# SFconv/expat/xmlparse/xmlparse.c:     MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlparse/xmlparse.h:     MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmltok/iasciitab.h:      MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmltok/Makefile.in:      NPL-1.1
# SFconv/expat/xmltok/makefile.win:     NPL-1.1
# SFconv/expat/xmltok/utf8tab.h:        MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmltok/xmldef.h:         MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmltok/xmlrole.h:        MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmltok/xmltok.h:         MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmltok/xmltok_impl.c:    MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmltok/xmltok_impl.h:    MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlwf/codepage.c:        MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlwf/codepage.h:        MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlwf/filemap.h:         MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlwf/readfilemap.c:     MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlwf/unixfilemap.c:     MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlwf/win32filemap.c:    MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlwf/xmlfile.c:         MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlwf/xmlfile.h:         MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlwf/xmltchar.h:        MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# SFconv/expat/xmlwf/xmlwf.c:           MPL-1.1 OR GPL-1.0-or-later (bundled expat)
# zlib-1.2.3:           "sse copyright notice in zlib.h"
# zlib-1.2.13/contrib/ada/*.adb:        "see zlib.ads"
# zlib-1.2.13/contrib/ada/zlib.ads:     GPL-2.0-or-later WITH GNAT-exception
# zlib-1.2.13/contrib/blast/blast.c:    "see blast.h"
# zlib-1.2.13/contrib/blast/blast.h:    Zlib
# zlib-1.2.13/contrib/dotzlib:  BSL-1.0
# zlib-1.2.13/contrib/gcc_gvmat64/gvmat64.S:    Zlib
# zlib-1.2.13/doc/rfc1950.txt:  ??? permissive
# zlib-1.2.13/zlib.h:    Zlib
## Removed when repackaging
# mac-installer/Resources/License.rtf:  "non-commercial"
#                                       <https://github.com/silnrsi/teckit/issues/34>
License:        (LGPL-2.1-or-later OR CPL-1.0) AND (LGPL-2.1-or-later OR GPL-2.0-or-later OR MPL-2.0)
SourceLicense:  %{license} AND LGPL-2.0-or-later AND GPL-2.0-or-later AND GPL-2.0-or-later WITH Autoconf-exception-generic AND Unicode-3.0 AND (MPL-1.1 OR GPL-1.0-or-later) AND NPL-1.1 AND GPL-2.0-or-later WITH GNAT-exception AND Zlib AND BSL-1.0
URL:            https://software.sil.org/teckit/
# Archive repackaged with ./repackage.sh tool because of a bad license
# <https://github.com/silnrsi/teckit/issues/34>.
# Original URL is https://github.com/silnrsi/teckit/releases/download/v%%{version}/teckit-%%{version}.tar.xz
Source0:        teckit-%{version}_repackaged.tar.xz
Source1:        https://github.com/silnrsi/teckit/releases/download/v%{version}/teckit-%{version}.tar.xz.asc
# Exported from ppisar's keyring
Source2:        gpgkey-15D41BC02EB807D405EFFAF6C9183BEA0288CDEE.gpg
Source3:        repackage.sh
BuildRequires:  autoconf >= 2.69
BuildRequires:  automake >= 1.11
BuildRequires:  coreutils
BuildRequires:  expat-devel
# gcc is not needed, the only source/NormalizationData.c is included into
# a C++ source/Engine.cpp compilation unit.
BuildRequires:  gcc-c++
# gnupg2 not used because of repackaging.
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  zlib-devel
# Tests:
BuildRequires:  perl-interpreter
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Provides:       bundels(graphite2)

%description
TECkit is a low-level toolkit intended to be used by other applications that
need to perform encoding conversions (e.g., when importing legacy data into
a Unicode-based application). The primary component of the TECkit package is
therefore a library that performs conversions; this is the "TECkit engine".
The engine relies on mapping tables in a specific binary format (for which
documentation is available); there is a compiler that creates such tables from
a human-readable mapping description (a simple text file).

%package devel
Summary:        Developmental files for TECkit library
License:        LGPL-2.1-or-later OR CPL-1.0
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files, pkg-config module, and documentation for developing application
that use TECkit, a character encoding and mapping, library.

%prep
%dnl verification skipped because of repackaging
%dnl %{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1
# Remove bundled libraries
rm -r zlib-*/*.{c,h} SFconv/expat
# Remove pre-build executables
rm -r perl_binaries

%build
# Regenerate a build script
autoreconf -fi
%configure \
    --disable-debug \
    --disable-final \
    --without-old-lib-names \
    --disable-profile \
    --disable-profilefn \
    --enable-shared \
    --disable-static \
    --with-system-zlib \
    --disable-tetex-build
%{make_build}

%install
%{make_install}
rm -f %{buildroot}%{_libdir}/*.la

%check
%{make_build} check

%files
# COPYING is unhelpful
%license license/*
# ChangeLog is unhelpful
%doc AUTHORS NEWS README
%{_bindir}/sfconv
%{_bindir}/teckit_compile
%{_bindir}/txtconv
%{_libdir}/libTECkit.so.0
%{_libdir}/libTECkit.so.0.*
%{_libdir}/libTECkit_Compiler.so.0
%{_libdir}/libTECkit_Compiler.so.0.*
%{_mandir}/man1/sfconv.*
%{_mandir}/man1/teckit_compile.*
%{_mandir}/man1/txtconv.*

%files devel
%doc docs/*.pdf
%{_includedir}/teckit
%{_libdir}/libTECkit.so
%{_libdir}/libTECkit_Compiler.so
%{_libdir}/pkgconfig/teckit.pc

%changelog
* Tue Jan 20 2026 Petr Pisar <ppisar@redhat.com> - 2.5.13-2
- Fix CI gating configuration

* Tue Jan 20 2026 Petr Pisar <ppisar@redhat.com> - 2.5.13-1
- 2.5.13 bump

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 28 2023 Petr Pisar <ppisar@redhat.com> - 2.5.12-1
- 2.5.12 bump
- Correct a license tag to "(LGPL-2.1-or-later OR CPL-1.0) AND
  (LGPL-2.1-or-later OR GPL-2.0-or-later OR MPL-2.0)"

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Feb 20 2023 Petr Pisar <ppisar@redhat.com> - 2.5.11-1
- 2.5.11 bump

* Mon Feb 20 2023 Petr Pisar <ppisar@redhat.com> - 2.5.9-12
- Correct a license tag to "(LGPL-2.1-or-later OR CPL-1.0) AND
  (LGPL-2.1-or-later OR GPL-2.0-or-later OR MPL-2.0 OR MPL-1.1)"

* Sat Feb 18 2023 Than Ngo <than@redhat.com> - 2.5.9-11
- migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.9-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 12 2019 Petr Pisar <ppisar@redhat.com> - 2.5.9-2
- Modernize spec file
- License corrected to
  ((LGPLv2+ or CPL) and (LGPLv2+ or GPLv2+ or MPLv2.0 or MPLv1.1))

* Sat Aug 10 2019 Tom Callaway <spot@fedoraproject.org> - 2.5.9-1
- update to 2.5.9

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 12 2017 Tom Callaway <spot@fedoraproject.org> - 2.5.7-1
- update to 2.5.7

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.5.1-13
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-7
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 05 2009 Caolán McNamara <caolanm@redhat.com> - 2.5.1-3
- include stdio.h for sprintf

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Jindrich Novy <jnovy@redhat.com> 2.5.1-1
- update to 2.5.1

* Tue Jan 08 2008 Jindrich Novy <jnovy@redhat.com> 2.2.1-3
- gcc-4.3 fixes

* Thu Aug 23 2007 Jindrich Novy <jnovy@redhat.com> 2.2.1-2
- update License
- rebuild for ppc32

* Tue Jul 17 2007 Jindrich Novy <jnovy@redhat.com> 2.2.1-1
- first Fedora build

* Wed Jul 11 2007 Jindrich Novy <jnovy@redhat.com> 2.2.1-0.3
- add missing licenses as documentation

* Wed Jul 11 2007 Jindrich Novy <jnovy@redhat.com> 2.2.1-0.2
- review fixes (#247615)
- add libtool BR
- enable parallel build
- fix filelist
- run ldconfig in post

* Tue Jul 10 2007 Jindrich Novy <jnovy@redhat.com> 2.2.1-0.1
- port TECkit to Fedora
- remove static libs

* Fri Jun 22 2007 David Walluck <walluck@mandriva.org> 2.2.1-3mdv2008.0
+ Revision: 42653
- workaround broken fix-eol rpm-helper script
- bump release
- BuildRequires: libexpat-devel
- Import teckit

* Thu Jun 21 2007 David Walluck <walluck@mandriva.org> 0:2.2.1-1mdv2008.0
- release
