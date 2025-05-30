Summary:        Theora video compression codec
Name:           libtheora
Version:        1.1.1
Release:        1%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Productivity/Multimedia/Other
URL:            https://www.theora.org/
Source0:        https://ftp.osuosl.org/pub/xiph/releases/theora/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  libogg-devel
BuildRequires:  libtool
BuildRequires:  libvorbis-devel
BuildRequires:  pkgconf-pkg-config

%description
Theora is a free and open video compression format from the Xiph.org Foundation. Like all our
multimedia technology it can be used to distribute film and video online and on disc without
the licensing and royalty fees or vendor lock-in associated with other formats.

%package -n libtheora0
Summary:        Theora video compression codec
Group:          System/Libraries
Provides:       %{name} = %{version}
Obsoletes:      %{name} <= %{version}

%description -n libtheora0
Theora is a free and open video compression format from the Xiph.org Foundation. Like all our
multimedia technology it can be used to distribute film and video online and on disc without
the licensing and royalty fees or vendor lock-in associated with other formats.

Theora scales from postage stamp to HD resolution, and is considered particularly competitive
at low bitrates. It is in the same class as MPEG-4/DiVX, and like the Vorbis audio codec it
has lots of room for improvement as encoder technology develops.

Theora is in full public release as of November 3, 2008. The bitstream format for Theora I
was frozen Thursday, 2004 July 1. All bitstreams encoded since that date will remain compatible
with future releases.

The package contains the library that can decode and encode Theora streams. Theora is also
able to playback VP3 streams.

%package -n libtheoradec1
Summary:        Theora video decompression library
Group:          System/Libraries

%description -n libtheoradec1
Theora is a free and open video compression format from the Xiph.org Foundation. Like all our
multimedia technology it can be used to distribute film and video online and on disc without
the licensing and royalty fees or vendor lock-in associated with other formats.

This subpackage contains the decoder library.

%package -n libtheoraenc1
Summary:        Theora video compression library
Group:          System/Libraries

%description -n libtheoraenc1
Theora is a free and open video compression format from the Xiph.org Foundation. Like all our
multimedia technology it can be used to distribute film and video online and on disc without
the licensing and royalty fees or vendor lock-in associated with other formats.

This subpackage contains the encoder library.

%package devel
Summary:        Theora video compression codec
Group:          Development/Libraries/C and C++
Requires:       libogg-devel
Requires:       libtheora0 = %{version}
Requires:       libtheoradec1 = %{version}
Requires:       libtheoraenc1 = %{version}

%description devel
Theora is a free and open video compression format from the Xiph.org Foundation. Like all our
multimedia technology it can be used to distribute film and video online and on disc without
the licensing and royalty fees or vendor lock-in associated with other formats.

Theora scales from postage stamp to HD resolution, and is considered particularly competitive
at low bitrates. It is in the same class as MPEG-4/DiVX, and like the Vorbis audio codec it
has lots of room for improvement as encoder technology develops.

Theora is in full public release as of November 3, 2008. The bitstream format for Theora I
was frozen Thursday, 2004 July 1. All bitstreams encoded since that date will remain compatible
with future releases.

The package contains the library that can decode and encode Theora streams. Theora is also
able to playback VP3 streams.

%prep
%autosetup -n %{name}-%{version}

%build
ACLOCAL="aclocal -I m4" autoreconf -f -i
%configure --disable-examples \
    --disable-static \
    --with-pic
make %{?_smp_mflags} docdir=%{_docdir}/%{name}

%install
%make_install docdir=%{_docdir}/%{name}
install -d %{buildroot}%{_bindir}
# Install remaining parts of documentation.
cp -a AUTHORS CHANGES COPYING LICENSE README %{buildroot}%{_docdir}/%{name}

%check
make check

%post   -n libtheora0 -p /sbin/ldconfig
%postun -n libtheora0 -p /sbin/ldconfig
%post   -n libtheoradec1 -p /sbin/ldconfig
%postun -n libtheoradec1 -p /sbin/ldconfig
%post   -n libtheoraenc1 -p /sbin/ldconfig
%postun -n libtheoraenc1 -p /sbin/ldconfig

%files
%license COPYING
%doc README

%files -n libtheora0
%defattr(-,root,root)
%{_libdir}/libtheora.so.0*

%files -n libtheoradec1
%defattr(-,root,root)
%{_libdir}/libtheoradec.so.1*

%files -n libtheoraenc1
%defattr(-,root,root)
%{_libdir}/libtheoraenc.so.1*

%files devel
%defattr(-,root,root)
%doc %dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/*
%{_includedir}/theora
%{_libdir}/*.so
%{_libdir}/pkgconfig/theoradec.pc
%{_libdir}/pkgconfig/theoraenc.pc
%{_libdir}/pkgconfig/theora.pc
%exclude %{_libdir}/*.la

%changelog
* Tue Nov 22 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.1.1-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag)
- Converting the 'Release' tag to the '[number].[distribution]' format
- Disabled subpackage examples and devel-docs
- Remove sources for obsolete -XXBit packages
- Enable check section
- License verified

* Mon Jun 21 2021 Matej Cepl <mcepl@suse.com>
- Remove completely unnecessary python BR

* Sat Aug 30 2014 jengelh@inai.de
- Split libtheoradec/enc from libtheora0 as they have different
  SO numbers
- Trim huge description; improve on RPM group classificaiton

* Thu May 23 2013 idonmez@suse.com
- Update descriptions, thanks to Perry Werneck

* Sun Nov 20 2011 coolo@suse.com
- add libtool as buildrequire to avoid implicit dependency

* Mon Aug 29 2011 crrodriguez@opensuse.org
- remove examples that fail to build, also SDL and png
  are only needed for those, so remove from buildrequires.

* Wed Jul 27 2011 crrodriguez@opensuse.org
- remove fno-strict-aliasing from CFLAGS as it is no longer
  needed and will slow down things.

* Mon May 23 2011 crrodriguez@opensuse.org
- Disable doxygen documentation to avoid build dates in
  - devel packages.
- add missing BuildRequires libpng-devel

* Fri Dec 18 2009 jengelh@medozas.de
- add baselibs.conf as a source

* Wed Oct  7 2009 adrian@suse.de
- update to version 1.1.1
  * minor bugfixes

* Sat Sep 26 2009 adrian@suse.de
- update to version 1.1.0
  * minor fixes since beta 3

* Thu Aug 27 2009 adrian@suse.de
- update to version 1.1 beta 3
  * Much better encoder
    (faster and more details at same compressions level)
  * Playback received speed improvements, but bitstream format is
    untouched
- no package split yet for dec/enc/legacy libs due to 11.2 freeze

* Fri Jul 17 2009 adrian@suse.de
- update to version 1.0 final
  * new additional encoder and decoder libs with new api.

* Wed Jan  7 2009 olh@suse.de
- obsolete old -XXbit packages (bnc#437293)

* Wed May 21 2008 cthiel@suse.de
- fix baselibs.conf

* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support

* Thu Dec 13 2007 crrodriguez@suse.de
- fix package version numbers 1.0beta1 --> 1.0.beta2
- libtheora 1.0.beta2
  - Fix a crash bug on char-is-unsigned architectures (PowerPC)
  - Fix a buffer sizing issue that caused rare encoder crashes
  - Fix a buffer alignment issue
  - Improved format documentation.
- removed unneeded patch, use --with-pic configure option instead.

* Thu Nov  8 2007 adrian@suse.de
- fix compiling with gcc 4.3 on ia32

* Wed Sep 26 2007 adrian@suse.de
- update to 1.0beta1
  From official changelog:
  * Granulepos scheme modified to match other codecs. This bumps
  the bitstream revision to 3.2.1. Bitstreams marked 3.2.0 are
  handled correctly by this decoder. Older decoders will show
  a one frame sync error in the less noticable direction.
  * Switch to new spec compliant decoder from theora-exp branch.
  Written by Dr. Timothy Terriberry.
  * Add support to the encoder for using quantization settings
  provided by the application.
  * more assembly optimizations

* Wed Aug 15 2007 coolo@suse.de
- fixing upgrade (#293401)

* Sat Aug 11 2007 crrodriguez@suse.de
- fix build in x86_64
- use library packaging policy
- run make check in the check section
- add missing call to ldconfig

* Wed Mar 28 2007 sbrabec@suse.cz
- Updated to version 1.0alpha7:
  * Enable mmx assembly by default
  * Avoid some relocations that caused problems on SELinux
  * Other build fixes
  * time testing mode (-f) for the dump_video example
  * Merge theora-mmx simd acceleration (x86_32 and x86_64)
  * Major RTP payload specification update
  * Minor format specification updates
  * Fix some spurious calls to free() instead of _ogg_free()
  * Fix invalid array indexing in PixelLineSearch()
  * Improve robustness against invalid input
  * General warning cleanup
  * The offset_y member meaning fix.
- Use incremental versioning scheme.
- Documentation repackaged.
- Use less vague names for binaries.

* Tue Aug  1 2006 dmueller@suse.de
- Reenable test suite run with valgrind.

* Fri Jul 28 2006 aj@suse.de
- Disable test suite run with valgrind.

* Fri Mar 10 2006 bk@suse.de
- libtheora-devel: add libogg-devel to Requires (found by .la check)

* Mon Feb  6 2006 adrian@suse.de
- add -fstack-protector
- enable test suite run with valgrind

* Sun Jan 29 2006 aj@suse.de
- Fix BuildRequires.

* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires

* Wed Oct 19 2005 adrian@suse.de
- update to version 1.0 alpha 5
- enable test suite
- generate API documentation with doxygen

* Thu Apr 14 2005 sbrabec@suse.cz
- Added audiofile-devel to neededforbuild.

* Wed Jan  5 2005 adrian@suse.de
- update to version 1.0 alpha 4

* Tue Oct 26 2004 adrian@suse.de
- remove .svn directories

* Mon Oct 18 2004 adrian@suse.de
- update to current cvs to get pc file

* Thu Aug 19 2004 adrian@suse.de
- create -devel package

* Tue Jun 29 2004 adrian@suse.de
- do not install the libtool scripts ...

* Sat Apr 24 2004 adrian@suse.de
- use xorg-x11 packages

* Wed Apr 21 2004 adrian@suse.de
- compile with -fno-strict-aliasing

* Sun Mar 21 2004 adrian@suse.de
- update to alpha 3 release
  on disc format is still not frozen, so this remain an internal package

* Wed Feb  4 2004 adrian@suse.de
- remove binaries from example dir (they get installed anyway)

* Fri Jan 30 2004 adrian@suse.de
- initial package of current snapshot (post alpha2)
- internal package only atm
