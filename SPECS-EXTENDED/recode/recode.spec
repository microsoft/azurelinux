Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:       recode
Version:    3.7.7
Release:    2%{?dist}
Summary:    Conversion between character sets and surfaces
# COPYING:              GPLv3 text
# COPYING-LIB:          LGPLv3 text
# doc/recode.info:      OFSFDL
# doc/recode.texi:      OFSFDL
# lib/error.h:              GPLv3+
# lib/strerror-override.c:  GPLv3+
# lib/vasnprintf.c:         GPLv3+
# src/ansellat1.l:      BSD
# src/lat1asci.c:       GPLv3+
# src/merged.c:         BSD
# src/recode.h:         LGPLv3+
# src/ucs.c:            LGPLv3+
## Not in any binary package
# aclocal.m4:               FSFULLR
# build-aux/bootstrap.in:   MIT or GPLv3+ (bundled gnulib-modules/bootstrap)
# build-aux/compile:        GPLv2+ with exceptions
# build-aux/config.guess:   GPLv3+ with exceptions
# build-aux/config.rpath:   FSFULLR
# build-aux/config.sub:     GPLv3+ with exceptions
# build-aux/depcomp:        GPLv2+ with exceptions
# build-aux/extract-trace:  MIT or GPLv3+ (bundled gnulib-modules/bootstrap)
# build-aux/funclib.sh:     MIT or GPLv3+ (bundled gnulib-modules/bootstrap)
# build-aux/inline-source:  MIT or GPLv3+ (bundled gnulib-modules/bootstrap)
# build-aux/install-sh:     MIT
# build-aux/ltmain.sh:      GPLv2+ with exceptions and GPLv3+ with exceptions
#                           and GPLv3+
# build-aux/mdate-sh:       GPLv2+ with exceptions
# build-aux/missing:        GPLv2+ with exceptions
# build-aux/options-parser: MIT or GPLv3+ (bundled gnulib-modules/bootstrap)
# build-aux/texinfo.tex:    GPLv3+ with exceptions
# config.rpath:         FSFULLR
# configure:            FSFUL and GPLv2+ with exceptions
# doc/Makefile.am:      GPLv3+
# doc/Makefile.in:      FSFULLR and GPLv3+
# doc/texinfo.tex:      GPLv2+ with exceptions
# INSTALL:              FSFAP
# Makefile.am:          GPLv3+
# m4/gettext.m4:        FSFULLR
# m4/gnulib-cache.m4:   GPLv3+ with exceptions
# m4/libtool.m4:        GPLv2+ with exceptions and FSFUL
# m4/mbstate_t.m4:      FSFULLR
# m4/minmax.m4:         FSFULLR
# m4/ssize_t.m4:        FSFULLR
# m4/sys_stat_h.m4:     FSFULLR
# tables.py:            GPLv3+
# tests/Makefile.am:    GPLv3+
# tests/Makefile.in:    FSFULLR and GPLv3+
# tests/Recode.pyx:     GPLv3+
License:    GPLv3+ and LGPLv3+ and BSD and OFSFDL
URL:        https://github.com/rrthomas/recode
Source:     %{url}/releases/download/v%{version}/recode-%{version}.tar.gz
# Make internal hash function identifiers unique
Patch0:     recode-3.7.1-Rename-coliding-hash-functions.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gettext-devel
# help2man is executed from ./src/Makefile if main.c or configure.ac is newer
# than recode.1.
BuildRequires:  make
BuildRequires:  libtool
BuildRequires:  texinfo
# Tests:
BuildRequires:  python3-Cython
BuildRequires:  python3-devel >= 3.7.5

%description
The recode tool and library convert files between character sets and surfaces.
It recognizes or produces over 200 different character sets (or about 300 if
combined with an iconv library) and transliterates files between almost any
pair. When exact transliteration is not possible, it gets rid of the offending
character or falls back on an approximations.

%package devel
Summary:    Header files for development using recode library
# Header files are LGPLv3+
License:    LGPLv3+
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the header files for a recode library.

%prep
%setup -q
%patch0 -p1
autoreconf -fi

%build
export PYTHON=%{__python3}
%configure \
    --without-dmalloc \
    --disable-gcc-warnings \
    --enable-largefile \
    --enable-nls \
    --disable-rpath \
    --enable-shared \
    --disable-static
%{make_build}

%check
make check

%install
%{make_install}
%find_lang %{name}

# remove unpackaged file from the buildroot
rm -r $RPM_BUILD_ROOT%{_infodir}/dir

# remove libtool archives
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%files -f %{name}.lang
%license COPYING COPYING-LIB
# Changelog is not helpful
%doc AUTHORS NEWS README THANKS TODO
%{_mandir}/*/*
%{_infodir}/recode.info*
%{_bindir}/*
%{_libdir}/librecode.so.3
%{_libdir}/librecode.so.3.*

%files devel
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.7.7-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jul 30 2020 Petr Pisar <ppisar@redhat.com> - 3.7.7-1
- 3.7.7 bump

* Wed Jul 29 2020 Petr Pisar <ppisar@redhat.com> - 3.7.6-3
- Correct a description

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 13 2019 Petr Pisar <ppisar@redhat.com> - 3.7.6-1
- 3.7.6

* Thu Sep 12 2019 Petr Pisar <ppisar@redhat.com> - 3.7.5-1
- 3.7.5 bump
- Fix a possible buffer overflow in transform_utf16_java()
- Fix a type mismatch in tests

* Mon Sep 02 2019 Petr Pisar <ppisar@redhat.com> - 3.7.4-1
- 3.7.4 bump

* Mon Sep 02 2019 Petr Pisar <ppisar@redhat.com> - 3.7.3-1
- 3.7.3 bump

* Tue Aug 20 2019 Petr Pisar <ppisar@redhat.com> - 3.7.2-1
- 3.7.2 bump
- Change a soname because recode-3.7 changed an ABI
  (https://github.com/rrthomas/recode/issues/22)

* Fri Aug 16 2019 Petr Pisar <ppisar@redhat.com> - 3.7.1-1
- 3.7.1 bump (bug #1379055)
- License changed to GPLv3+ and LGPLv3+ and BSD and OFSFDL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6-47
- Escape macros in %%changelog

* Tue Oct 03 2017 Zoltan Kota <zoltank[AT]gmail.com> - 3.6-46
- Apply patch to fix bug #1422550

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 18 2013 Jiri Popelka <jpopelka@redhat.com> - 3.6-38
- Fix FTBFS if "-Werror=format-security" flag is used (#1037305).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Zoltan Kota <zoltank[AT]gmail.com> 3.6-36
- Fix failed Fedora_19_Mass_Rebuild [bug #914431].

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Zoltan Kota <zoltank[AT]gmail.com> 3.6-34
- Add patch for fixing build with new automake.
  (Fixes failed Fedora_18_Mass_Rebuild.)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Zoltan Kota <zoltank[AT]gmail.com> 3.6-32
- Corrected summary of the devel subpackage. Fixing bug #817947.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 7 2010 Zoltan Kota <z.kota[AT]gmx.net> 3.6-29
- Fix build on x86_64. Run autoreconf to update config files.
  autoconf >= 2.64 needs to patch the flex.m4 file.
  Fixing FTBFS bug #564601.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.6-26
- Autorebuild for GCC 4.3

* Wed Jan 16 2008 Zoltan Kota <z.kota[AT]gmx.net> 3.6-25
- add patch for gcc43

* Wed Aug 22 2007 Zoltan Kota <z.kota[AT]gmx.net> 3.6-24
- update license tag
- rebuild

* Tue Apr 03 2007 Zoltan Kota <z.kota[AT]gmx.net> 3.6-23
- rebuild

* Fri Sep 01 2006 Zoltan Kota <z.kota[AT]gmx.net> 3.6-22
- rebuild

* Mon Feb 13 2006 Zoltan Kota <z.kota[AT]gmx.net> 3.6-21
- rebuild

* Thu Dec 22 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-20
- rebuild

* Fri Aug 26 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-19
- fix requires
- disable static libs and remove libtool archives
- add %%doc

* Fri Aug 26 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-18
- add dist tag
- specfile cleanup

* Thu May 26 2005 Bill Nottingham <notting@redhat.com> 3.6-17
- rebuild for Extras

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 3.6-16
- cleanup

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 3.6-15
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 3.6-14
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Than Ngo <than@redhat.com> 3.6-11 
- add a patch file from kota@szbk.u-szeged.hu (bug #115524)

* Thu Nov 20 2003 Thomas Woerner <twoerner@redhat.com> 3.6-10
- Fixed RPATH (missing make in %%build)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 3.6-7
- rebuild on all arches
- remove unpackaged file from the buildroot

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 15 2002 Bill Nottingham <notting@redhat.com> 3.6-4
- add ldconfig %%post/%%postun

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 3.6-3
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov 13 2001 Than Ngo <than@redhat.com> 3.6-1
- initial RPM for 8.0
