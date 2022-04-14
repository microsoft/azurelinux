Vendor:         Microsoft Corporation
Distribution:   Mariner
%global out out123
%global fmt fmt123

Name:           mpg123
Version:        1.25.12
Release:        4%{?dist}
Summary:        Real time MPEG 1.0/2.0/2.5 audio player/decoder for layers 1, 2 and 3

License:        LGPLv2+
URL:            http://mpg123.org
Source0:        %{url}/download/%{name}-%{version}.tar.bz2

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

BuildRequires:  gcc
BuildRequires:  pkgconfig(alsa)

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}


%global enable_jack 1
%global enable_portaudio 1


%global _summary %{summary}

%global _description \
Real time MPEG 1.0/2.0/2.5 audio player/decoder for layers 1, 2 and 3 (most\
commonly MPEG 1.0 layer 3 aka MP3), as well as re-usable decoding and output\
libraries.

%description %{_description}

%package plugins-pulseaudio
Summary:        Pulseaudio output plug-in for %{name}
BuildRequires:  pkgconfig(libpulse-simple)
Requires:       %{name}%{?_isa} = %{version}-%{release}

Supplements:    (mpg123%{?_isa} and pulseaudio%{?_isa})


%description plugins-pulseaudio %{_description}

Pulseaudio output plug-in.

%if 0%{?enable_jack}
%package plugins-jack
Summary:        JACK output plug-in for %{name}
BuildRequires:  pkgconfig(jack)
Requires:       %{name}%{?_isa} = %{version}-%{release}

Supplements:    (mpg123%{?_isa} and jack-audio-connection-kit%{?_isa})

Obsoletes:      %{name}-plugins-extras < 1.23.4-1

%description plugins-jack %{_description}

JACK output plug-in.
%endif

%if 0%{?enable_portaudio}
%package plugins-portaudio
Summary:        PortAudio output plug-in for %{name}
BuildRequires:  pkgconfig(portaudio-2.0)
Requires:       %{name}%{?_isa} = %{version}-%{release}

Supplements:    (mpg123%{?_isa} and portaudio%{?_isa})


%description plugins-portaudio %{_description}

PortAudio output plug-in.
%endif

%package libs
Summary:        %{_summary}
Provides:       lib%{name} = %{version}-%{release}
Provides:       lib%{name}%{?_isa} = %{version}-%{release}
Obsoletes:      lib%{name} < 1.23.4-1

%description libs %{_description}

%package devel
Summary:        %{_summary}
BuildRequires:  /usr/bin/doxygen
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       lib%{name}-devel = %{version}-%{release}
Provides:       lib%{name}-devel%{?_isa} = %{version}-%{release}
Obsoletes:      lib%{name}-devel < 1.23.4-1
Obsoletes:      %{name}-libs-devel < 1.23.8-3

%description devel %{_description}

Development files for decoding and output libraries.

%prep
%autosetup

%build
autoreconf -vfi
%configure --enable-modules=yes --with-default-audio=alsa \
	--with-audio=alsa,%{?enable_jack:jack},pulse,oss,%{?enable_portaudio:portaudio}
%make_build
pushd doc
  doxygen doxygen.conf
popd

%install
%make_install
rm %{buildroot}%{_libdir}/*.la

%ldconfig_scriptlets libs

%files
%doc doc/README.remote
%{_bindir}/%{name}
%{_bindir}/%{name}-id3dump
%{_bindir}/%{name}-strip
%{_bindir}/%{out}
%doc %{_mandir}/man1/%{name}.1*
%doc %{_mandir}/man1/%{out}.1*
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/output_alsa.*
%{_libdir}/%{name}/output_dummy.*
%{_libdir}/%{name}/output_oss.*

%files plugins-pulseaudio
%{_libdir}/%{name}/output_pulse.*

%if 0%{?enable_jack}
%files plugins-jack
%{_libdir}/%{name}/output_jack.*
%endif

%if 0%{?enable_portaudio}
%files plugins-portaudio
%{_libdir}/%{name}/output_portaudio.*
%endif

%files libs
%license COPYING
%doc NEWS
%{_libdir}/lib%{name}.so.0*
%{_libdir}/lib%{out}.so.0*

%files devel
%doc NEWS.lib%{name} doc/html doc/examples doc/BENCHMARKING doc/README.gain
%{_includedir}/%{name}.h
%{_includedir}/%{out}.h
%{_includedir}/%{fmt}.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{out}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_libdir}/pkgconfig/lib%{out}.pc

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 1.25.12-4
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.25.12-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 27 2019 Wim Taymans <wtaymans@redhat.com> - 1.25.12-1
- update to 1.25.12 (rhbz#1742097)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 17 2018 Wim Taymans <wtaymans@redhat.com> - 1.25.10-1
- update to 1.25.10
- Fix summary (#1494838)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Wim Taymans <wtaymans@redhat.com> - 1.25.6-4
- Only enable jack and portaudio plugins on fedora

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.25.6-2
- Switch to %%ldconfig_scriptlets

* Sun Sep 17 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.25.6-1
- Update to upstream release 1.25.6

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.23.8-4
- Fix subpackages' Supplements tags (#1397479)

* Fri Nov 11 2016 Wim Taymans <wtaymans@redhat.com> - 1.23.8-3
- Remove pointless Enhances:
- Fix splelling mistake
- change package name from libs-devel to devel and add Obsolete:
- see rhbz#1394147 

* Fri Nov 11 2016 Wim Taymans <wtaymans@redhat.com> - 1.23.8-2
- Flip Recommends: with rich dependencies to Supplements:

* Tue Nov  8 2016 Wim Taymans <wtaymans@redhat.com> - 1.23.8-1
- Update to upstream release 1.23.8

* Mon Sep  5 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.23.6-3
- Do not remove output plugin .la files so that libout123 can actually
  find them

* Tue Jul 26 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.23.6-2
- Provide old name for libs and libs-devel subpkgs

* Sat Jul 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.23.6-1
- Update to 1.23.6

* Mon Jun 27 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.23.4-1
- Update to 1.23.4
- Use weak and rich deps for plugins
- rename libmpg123 to mpg123-libs
- Drop usage of alternatives (nothing uses it actually)
- Correct license

* Sat Oct 31 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.22.4-1
- New upstream release 1.22.4 (rf3802)

* Mon Jun 22 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.22.2-2
- Fix playback of files with apetags

* Sun Jun 21 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.22.2-1
- New upstream release 1.22.2

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Apr  6 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.19.0-1
- Update to 1.19.0
- Enable (optional) use of NEON on arm
- Add missing %%{?_isa} to libmpg123 Requires in -devel (rf#3194)

* Sat Mar 01 2014 Michael Kuhn <suraia@ikkoku.de> - 1.18.1-1
- Update to 1.18.1.

* Sat Jan 04 2014 Michael Kuhn <suraia@ikkoku.de> - 1.17.0-1
- Update to 1.17.0.

* Sun Oct 13 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.16.0-1
- New upstream release 1.16.0

* Sun Mar 10 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.15.1-1
- New upstream release 1.15.1 (rf#2716)
- Drop obsolete esound and arts plugins from mpg123-plugins-extras

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.14.3-2
- Mass rebuilt for Fedora 19 Features

* Mon Jul 02 2012 Richard Shaw <hobbes1069@gmail.com> - 1.14.3-1
- Update to latest upstream release.
- Move README and README.remote to correct package. Fixes #1898.

* Wed Apr  4 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.13.7-1
- New upstream bugfix release 1.13.7
- Properly build and install development documentation (rf#2257)

* Sun Jan 29 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.13.4-1
- New upstream release 1.13.4

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 24 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.12.3-1
- New upstream release 1.12.3

* Fri Jul 16 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.12.1-4
- Put the pulseaudio and jack output plugins in their own subpackages (rf#1278)

* Mon Jun 21 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.12.1-3
- Move mpg123 (and its manpage) to mpg123.bin and use alternatives, so as to
  peacefully co-exist with mpg321 (rf#1278)

* Fri Jun 18 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.12.1-2
- Add arts-devel BuildRequire and add the arts output plug-in to the
  mpg123-plugins-extras package

* Mon Jun 14 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.12.1-1
- Update to 1.12.1
- Put libmpg123 into its own package
- Put some less often used output plugins into their own mpg123-plugins-extras
  package

* Thu May 29 2008 Matthias Saou <http://freshrpms.net/> 1.4.2-2
- Don't remove plugins *.la files, as they're required to run.

* Mon May 12 2008 Matthias Saou <http://freshrpms.net/> 1.4.2-1
- Update to 1.4.2.
- Obolete mpg321 up to last known version, as it's pretty much dead.
- Add libtool-ltdl-devel build req, without a copy is installed.
- Add scriplets for new library.

* Mon Jun 04 2007 Dag Wieers <dag@wieers.com> - 0.66-1
- Updated to release 0.66.

* Wed Feb 07 2007 Dag Wieers <dag@wieers.com> - 0.65-1
- Updated to release 0.65.

* Tue Jan 16 2007 Dag Wieers <dag@wieers.com> - 0.64-1
- Updated to release 0.64.

* Mon Jan 15 2007 Dag Wieers <dag@wieers.com> - 0.63-1
- Updated to release 0.63.

* Sun Oct 22 2006 Dag Wieers <dag@wieers.com> - 0.61-1
- Updated to release 0.61.

* Mon Sep  4 2006 Matthias Saou <http://freshrpms.net/> 0.60-1
- Update to 0.60 final.
- Add support for all available compatible outputs, unfortunately it's a build
  time choice, so default to alsa.
- Obsolete mpg321 up to the last know package version.

* Tue Jul 25 2006 Matthias Saou <http://freshrpms.net/> 0.60-0.1.beta2
- Initial RPM release, now that mpg123 is maintained again and went GPL/LGPL.
- Audio output type is not (yet?) plugin-based, so use libao (for ALSA).
