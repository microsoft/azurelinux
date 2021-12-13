Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:      Real-time software synthesizer
Name:         fluidsynth
Version:      1.1.11
Release:      8%{?dist}
URL:          http://www.fluidsynth.org/
Source0:      https://github.com/Fluidsynth/fluidsynth/archive/v%{version}/fluidsynth-%{version}.tar.gz
License:      LGPLv2+
Requires:     fluidsynth-libs%{?_isa} = %{version}-%{release}

# Re-fix multi-lib conflict RHBZ#528240
Patch0:       fluidsynth-no_date_footer.patch

BuildRequires: alsa-lib-devel
BuildRequires: cmake
BuildRequires: dbus-devel
BuildRequires: gcc
%if !0%{?flatpak}
BuildRequires: jack-audio-connection-kit-devel
%endif
BuildRequires: ladspa-devel
BuildRequires: libsndfile-devel
BuildRequires: ncurses-devel
BuildRequires: pkgconfig
# Disabled for now:
# http://sourceforge.net/apps/trac/fluidsynth/ticket/51
# To enable portaudio support one also has to pass
# -Denable-portaudio=on to cmake
# BuildRequires: portaudio-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: readline-devel

# For documentation:
BuildRequires: doxygen

%description
FluidSynth is a real-time software synthesizer based on the SoundFont 2 
specifications. It is a "software synthesizer". FluidSynth can read MIDI events
from the MIDI input device and render them to the audio device. It features 
real-time effect modulation using SoundFont 2.01 modulators, and a built-in
command line shell. It can also play MIDI files (note: FluidSynth was previously
called IIWU Synth).

%package libs
Summary:   Real-time software synthesizer run-time libraries

%description libs
FluidSynth is a real-time software synthesizer based on the SoundFont 2 
specifications. It is a "software synthesizer". This package holds the run-time
shared libraries.

%package devel
Summary:   Real-time software synthesizer development files
Requires:  fluidsynth-libs%{?_isa} = %{version}-%{release}

%description devel
FluidSynth is a real-time software synthesizer based on the SoundFont 2 
specifications. It is a "software synthesizer". This package holds header files
for building programs that link against fluidsynth.

%prep
%setup -q
%patch0 -p1 -b .no.date

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}

%if 0%{?flatpak}
%define enable_jack off
%else
%define enable_jack on
%endif

%{cmake}  -Denable-ladspa=on -Denable-jack=%{enable_jack} ..
popd

# build fluidsynth
make %{?_smp_mflags} -C %{_target_platform}

# build docs
make doxygen -C %{_target_platform}/doc


%install
make DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform} install


%files
%{_bindir}/fluid*
%{_mandir}/man1/fluidsynth*

%files libs
%license LICENSE
%doc AUTHORS NEWS README.md THANKS TODO doc/FluidSynth-LADSPA.pdf
%{_libdir}/libfluidsynth.so.1
%{_libdir}/libfluidsynth.so.1.*

%files devel
%doc %{_target_platform}/doc/api/html doc/*.c doc/*fluid*.txt doc/*.odt
%doc ChangeLog
%{_includedir}/fluidsynth.h
%{_includedir}/fluidsynth/
%{_libdir}/libfluidsynth.so
%{_libdir}/pkgconfig/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.11-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.11-5
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 18 2018 Owen Taylor <otaylor@redhat.com> - 1.1.11-3
- Disable hack for Flatpak builds - JACK isn't useful inside a sandbox, since
  there won't be enough privileges.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun May 06 2018 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.11-1
- Update to 1.1.11

* Sun Feb 25 2018 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.10-1
- Update to 1.1.10
- Drop upstreamed patches
- Drop ldconfig calls in post and postun

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 06 2018 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.9-1
- Update to 1.1.9
- Fix startup issue when an invalid soundfont file name is given as a command
  line argument RHBZ#1399896

* Mon Aug 14 2017 Pete Walter <pwalter@fedoraproject.org> - 1.1.6-12
- Disable lash support

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.6-8
- Rebuild for readline 7.x

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 21 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.6-1
- Update to 1.1.6

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.5-4
- Re-fix multilib confict RHBZ#528240
- Some specfile clean up

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.1.5-2
- Fix cmake usage even more. The .pc file was broken.

* Sun Sep 04 2011 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.1.5-1
- Update to 1.1.5

* Sat Aug 13 2011 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.1.4-1
- Update to 1.1.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.1.3-1
- Update to 1.1.3

* Fri Oct 01 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.1.2-2
- Fix garbled sound issues. Upstream ticket #87

* Wed Sep 01 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.1.2-1
- Update to 1.1.2 (with cmake)

* Sat Jan 30 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.1.1-1
- Update to 1.1.1

* Wed Dec 09 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.0.9-5
- Enable PulseAudio support (#538224, FESCo#265, also works around #500087)

* Wed Oct 28 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.0.9-4
- Fix doxygen doc multilib conflict (RHBZ#528240)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.0.9-2
- Disable portaudio support. It somehow messes up jack.

* Sun Jun 28 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.0.9-1
- Updated to 1.0.9
- Clean rpath
- Fix encoding issues
- Remove unnecessary direct library dependencies
- Add portaudio support

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.8-2
- fix license tag

* Tue Jul 08 2008 Anthony Green <green@redhat.com> 1.0.8-1
- Upgrade source.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.7-11.a
- Autorebuild for GCC 4.3

* Tue Oct 09 2007 Anthony Green <green@redhat.com> 1.0.7-10.a
- Rebuilt for new lash again.

* Mon Oct 08 2007 Anthony Green <green@redhat.com> 1.0.7-9.a
- Rebuilt for new lash.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> - 1.0.7-8.a
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Anthony Green <green@redhat.com> 1.0.7-7.a
- Rebuild.

* Mon Sep  4 2006 Anthony Green <green@redhat.com> 1.0.7-6.a
- devel package must Require pkgconfig.

* Thu Jul 13 2006 Anthony Green <green@redhat.com> 1.0.7-5.a
- Remove iiwusynth references.
- Don't install .la file.
- Add %%doc bits.
- Move non-numersion version component to release tag.
- Fix libs and devel package names.

* Sat May 27 2006 Anthony Green <green@redhat.com> 1.0.7a-4
- Remove e2fsprogs-devel BuildRequires.

* Tue Apr 25 2006 Anthony Green <green@redhat.com> 1.0.7a-3
- Port from ladcca to lash.
- Configure with --disable-static.
- Install sample soundfont.  Own /usr/share/soundfonts.
- Use $RPM_BUILD_ROOT
- Add Requires to libfluidsynth.
- Change fluidsynth Requires to point at libfluidsynth.

* Sat Apr 22 2006 Anthony Green <green@redhat.com> 1.0.7a-2
- Minor spec file improvements.

* Tue Apr 18 2006 Anthony Green <green@redhat.com> 1.0.7a-1
- Update sources.  Build for Fedora Extras.

* Tue Dec 21 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 
- spec file cleanup
* Fri Sep 24 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.0.5-1
- updated to 1.0.5
- ladcca patch no longer needed
* Wed May 19 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu>
- added defattr to libfluidsynth
* Wed May 12 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu>
- added buildrequires, made midishare optional
* Tue Feb 24 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.0.3-3
- enabled ladcca 0.4.0 support (patch0)
* Tue Oct 21 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.0.3-2
- enabled midishare support
* Tue Aug 26 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.0.3-1
- updated to 1.0.3, added release tags
* Fri Jul 25 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.0.2-1
- updated to 1.0.2
* Thu May  8 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.0.1-1
- changed over to new fluidsynth name
- we obsolete only iiwusynth and libiiwusynth-devel, we leave libiiwusynth
  there for now for older programs to use. We cannot install both iiwusynth
  and fluidsynth as there is a pkgconfig file in libiiwusynth-devel named
  fluidsynth.pc.
* Wed Apr  2 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2.4-4.cvs
- rebuild for jack 0.66.3, added explicit requires for it
* Fri Mar  7 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2.4-3.cvs
- added patches for jack buffer size callback and alsa snd_pcm_drop
* Thu Mar  6 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2.4-2.cvs
- cvs: 20030306.150630
* Thu Feb 27 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2.4-1
- changed over to cvs version, includes jack and ladcca support
- disable ladcca support under redhat 7.2/7.3, can't get it to 
  compile
- split libraries into separate packages (from mandrake spec file)
* Sun Nov 10 2002 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2.2-2
- added patch to rename jack alsa ports for jack >= 0.40
- added explicit dependency to jack
* Mon Oct 21 2002 Fernando Lopez Lezcano <nando@ccrma.stanford.edu>
- Initial build.


