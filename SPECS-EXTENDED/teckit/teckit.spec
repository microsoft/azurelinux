Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           teckit
Version:        2.5.9
Release:        4%{?dist}
Summary:        Conversion library and mapping compiler
# COPYING:                      links to license/LICENSING.txt
# license/License_CPLv05.txt:   CPLv0.5 text
# license/License_LGPLv21.txt:  LGPLv2 text
# license/LICENSING.txt:        license declarations
# SFconv/UtfCodec.cpp:      LGPLv2+ or GPLv2+ or MPL(?version) (bundled Graphite2)
# SFconv/UtfCodec.h:        LGPLv2+ or GPLv2+ or MPL(?version) (bundled Graphite2)
#                           <https://github.com/silnrsi/graphite/issues/58>,
#                           graphite2 package uses "MPL"
# source/Engine.cpp:        LGPLv2+ or CPL
# source/TECkit_Format.h:   LGPLv2+ or CPL
## Not in any binary package
# aclocal.m4:           FSFULLR
# compile:              GPLv2+ with exceptions
# config.guess:         GPLv3+ with exceptions
# config.sub:           GPLv3+ with exceptions
# configure:            FSFUL and GPLv2+ with exceptions
# depcomp:              GPLv2+ with exceptions
# install-sh:           MIT
# lib/Makefile.in:      FSFULLR
# ltmain.sh:            GPLv2+ with exceptions and GPLv3+ with exceptions and GPLv3+
# m4/libtool.m4:        FSFULL and FSFULLR and GPLv2+ with exceptions
# m4/ltoptions.m4:      FSFULLR
# m4/ltsugar.m4:        FSFULLR
# m4/ltversion.m4:      FSFULLR
# m4/lt~obsolete.m4:    FSFULLR
# Makefile.in:          FSFULLR
# missing:              GPLv2+ with exceptions
# test-driver:          GPLv2+ with exceptions
# test/Makefile.in:     FSFULLR
## Unbundled
# SFconv/expat/xmlparse/hashtable.c:    MPLv1.1 of GPL+ (bundled expat)
# SFconv/expat/xmlparse/xmlparse.c:     MPLv1.1 of GPL+ (bundled expat)
# zlib-1.2.3:           zlib (see nonexistent zlib.h, reported to
#                       <https://github.com/silnrsi/teckit/issues/22>)
License:        (LGPLv2+ or CPL) and (LGPLv2+ or GPLv2+ or MPLv2.0 or MPLv1.1)
URL:            https://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=teckit
Source0:        https://github.com/silnrsi/teckit/releases/download/v%{version}/teckit-%{version}.tar.gz
Source1:        https://github.com/silnrsi/teckit/releases/download/v%{version}/teckit-%{version}.tar.gz.asc
# Exported from ppisar's keyring
Source2:        gpgkey-15D41BC02EB807D405EFFAF6C9183BEA0288CDEE.gpg
# Fix a compiler warning about a misindentation,
# <https://github.com/silnrsi/teckit/pull/23>
Patch0:         teckit-2.5.9-Correct-indentation.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  expat-devel
# gcc is not needed, the only source/NormalizationData.c is included into
# a C++ source/Engine.cpp compilation unit.
BuildRequires:  gcc-c++
BuildRequires:  gnupg2
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
License:        LGPLv2+ or CPL
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files, pkg-config module, and documentation for developing application
that use TECkit, a character encoding and mapping, library.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q
%patch0 -p1
# Remove bundled libraries
rm -r zlib-*/*.c SFconv/expat
# Regenerate build script
autoreconf -fi

%build
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
%{_mandir}/man1/*

%files devel
%doc docs/*.pdf
%{_includedir}/teckit/
%{_libdir}/libTECkit.so
%{_libdir}/libTECkit_Compiler.so
%{_libdir}/pkgconfig/teckit.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.5.9-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
