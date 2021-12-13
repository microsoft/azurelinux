Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           libshout
Version:        2.4.3
Release:        2%{?dist}
Summary:        Icecast source streaming library

# COPYING:              GPLv2 text
# include/shout/shout.h.in:     LGPLv2+
# README:               LGPLv2+
# src/codec_opus.c:     LGPLv2+
# src/codec_speex.c:    LGPLv2+
# src/codec_theora.c:   LGPLv2+
# src/codec_vorbis.c:   LGPLv2+
# src/common/avl/avl.c: MIT
# src/common/httpp/encoding.c:  LGPLv2+
# src/common/httpp/encoding.h:  LGPLv2+
# src/common/httpp/httpp.c:     LGPLv2+
# src/common/httpp/httpp.h:     LGPLv2+
# src/common/net/resolver.c:    LGPLv2+
# src/common/net/resolver.h:    LGPLv2+
# src/common/net/sock.c:        LGPLv2+
# src/common/net/sock.h:        LGPLv2+
# src/common/thread/thread.c:   LGPLv2+
# src/common/thread/thread.h:   LGPLv2+
# src/common/timing/timing.c:   LGPLv2+
# src/common/timing/timing.h:   LGPLv2+
# src/connection.c:     LGPLv2+
# src/format_mp3.c:     LGPLv2+
# src/format_ogg.c:     LGPLv2+
# src/format_ogg.h:     LGPLv2+
# src/format_webm.c:    LGPLv2+
# src/proto_http.c:     LGPLv2+
# src/proto_icy.c:      LGPLv2+
# src/proto_roaraudio.c:    LGPLv2+
# src/proto_xaudiocast.c:   LGPLv2+
# src/queue.c:          LGPLv2+
# src/shout.c:          LGPLv2+
# src/shout_private.h:  LGPLv2+
# src/tls.c:            LGPLv2+
# src/util.c:           LGPLv2+
# src/util.h:           LGPLv2+
## Not in a binary package
# aclocal.m4:           GPLv2+ with Autoconf exception and FSFULLR
# compile:              GPLv2+ with Autoconf exception
# config.guess:         GPLv3+ with Autoconf exception
# config.sub:           GPLv3+ with Autoconf exception
# configure:            GPLv2+ with Libtool exception and FSFUL
# depcomp:              GPLv2+ with Autoconf exception
# doc/Makefile.in:      FSFULLR
# examples/Makefile.in: FSFULLR
# include/Makefile.in:  FSFULLR
# include/shout/Makefile.in:    FSFULLR
# install-sh:           MIT
# ltmain.sh:            GPLv2+ with a Libtool exception
# m4/lt~obsolete.m4:    FSFULLR
# m4/ltoptions.m4:      FSFULLR
# m4/ltsugar.m4:        FSFULLR
# m4/ltversion.m4:      FSFULLR
# m4/libtool.m4:        GPLv2+ with Libtool exception and FSFULLR and FSFUL
# Makefile.in:          FSFULLR
# missing:              GPLv2+ with Autoconf exception
# src/common/avl/COPYING:       LGPLv2 text
# src/common/avl/Makefile.in:   FSFULLR
# src/common/httpp/COPYING:     LGPLv2 text
# src/common/httpp/Makefile.in: FSFULLR
# src/common/httpp/README:      LGPLv2+
# src/common/net/COPYING:       LGPLv2 text
# src/common/net/Makefile.in:   FSFULLR
# src/common/thread/COPYING:    LGPLv2 text
# src/common/thread/Makefile.in:    FSFULLR
# src/common/timing/COPYING:    LGPLv2 text
# src/common/timing/Makefile.in:    FSFULLR
# src/Makefile.in:      FSFULLR
# win32/Makefile.in:    FSFULLR
License:        LGPLv2+ and MIT
URL:            https://www.icecast.org/
Source:         https://downloads.us.xiph.org/releases/libshout/libshout-%{version}.tar.gz
# Fedora does not support ckport. Enable disabling it.
# <https://gitlab.xiph.org/xiph/icecast-libshout/issues/2314>
Patch0:         libshout-2.4.3-Allow-disabling-ckport-database-installation.patch
# Enforce a Fedora system-wide crypto policy
# <https://docs.fedoraproject.org/en-US/packaging-guidelines/CryptoPolicies/#_cc_applications>
Patch1:         libshout-2.4.3-Default-OpenSSL-cipher-list-is-PROFILE-SYSTEM.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(theora)
BuildRequires:  sed

%description
libshout is a library for communicating with and sending data to an
icecast server.  It handles the socket connection, the timing of the
data, and prevents most bad data from getting to the icecast server.

%package        devel
Summary:        Header files for %{name} development
License:        LGPLv2+
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The libshout-devel package contains the header files needed for developing
applications that send data to an icecast server.  Install libshout-devel if
you want to develop applications using libshout.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
autoreconf -fi

%build
%configure \
  --disable-ckport \
  --enable-examples \
  --enable-pkgconfig \
  --disable-silent-rules \
  --enable-shared \
  --enable-speex \
  --disable-static \
  --enable-theora \
  --enable-thread

# clean unused-direct-shlib-dependencies
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build

%install
%make_install

find $RPM_BUILD_ROOT -type f -name "*.la" -delete

rm -rf $RPM_BUILD_ROOT%{_docdir}

%files
%doc NEWS README
%license COPYING
%{_libdir}/libshout.so.3
%{_libdir}/libshout.so.3.*

%files devel
%doc examples/*.c doc/*.xml
%{_libdir}/libshout.so
%{_libdir}/pkgconfig/shout.pc
%{_includedir}/shout/
%{_datadir}/aclocal/shout.m4

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.3-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 10 2020 Petr Pisar <ppisar@redhat.com> - 2.4.3-1
- 2.4.3 bump

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Apr 29 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.2.2-19
- .spec cleanup

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2.2-3
- Autorebuild for GCC 4.3

* Fri Dec  7 2007 kwizart < kwizart at gmail.com > - 2.2.2-2
- Fix http://bugzilla.redhat.com/415121
- Add disable-static
- Don't use makeinstall macro
- Update License field

* Thu Sep 07 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.2.2-1
- updated to new release

* Fri Mar 17 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.2-3
- add Requires: to -devel package

* Fri Mar 17 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.2-2
- rebuild to please the extras repository

* Fri Mar 10 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.2-1
- new (incompatible) version, but deps are updated
- various cleanups

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.0.9-4
- rebuild on all arches

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.9-3
- Include headers directory entry in -devel package.

* Sat Feb 26 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.0.9-2
- Remove redundant explicit /sbin/ldconfig dependency.

* Wed Jun 04 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.9-0.fdr.1: initial RPM release
