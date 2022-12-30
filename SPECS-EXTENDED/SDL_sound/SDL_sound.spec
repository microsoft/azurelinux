Summary:        Library handling decoding of several popular sound file formats
Name:           SDL_sound
Version:        1.0.3
Release:        32%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.icculus.org/SDL_sound
Source0:        https://icculus.org/SDL_sound/downloads/%{name}-%{version}.tar.gz
BuildRequires:  make
BuildRequires:  SDL-devel
BuildRequires:  flac-devel
BuildRequires:  speex-devel 
BuildRequires:  libvorbis-devel
BuildRequires:  libogg-devel
BuildRequires:  libmikmod-devel
BuildRequires:  libmodplug-devel
BuildRequires:  physfs-devel
BuildRequires:  doxygen
# SDL_sound uses a very stripped down mpg123-libs called mpglib
Provides:       bundled(mpglib)
Provides:       bundled(mpg123-libs)

%description
SDL_sound is a library that handles the decoding of several popular sound file
formats, such as .WAV and .OGG.

It is meant to make the programmer's sound playback tasks simpler. The
programmer gives SDL_sound a filename, or feeds it data directly from one of
many sources, and then reads the decoded waveform data back at her leisure.
If resource constraints are a concern, SDL_sound can process sound data in
programmer-specified blocks. Alternately, SDL_sound can decode a whole sound
file and hand back a single pointer to the whole waveform. SDL_sound can
also handle sample rate, audio format, and channel conversion on-the-fly
and behind-the-scenes, if the programmer desires.

%package        devel
Summary:        %{summary}
Requires:       %{name} = %{version}-%{release}
Requires:       SDL-devel

%description    devel
%{description}

This package contains the headers and libraries for SDL_sound development.

%prep
%autosetup -p1 -n %{name}-%{version}
# Avoid lib64 rpaths
#sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
rm -r PBProjects.tar.gz

%build
export CFLAGS="%{optflags} -D__EXPORT__= -Wno-pointer-sign -Wno-deprecated-declarations"
# no smpeg because of patents!
%configure --disable-dependency-tracking --disable-static \
    --disable-smpeg --enable-mpglib --enable-mikmod --enable-ogg \
    --enable-modplug --enable-speex --enable-flac --enable-midi
%make_build
doxygen Doxyfile


%install
%make_install
# Avoid conflict with SDL2_sound, users who want this should use SDL2_sound
rm %{buildroot}/%{_bindir}/playsound*

# Add namespaces to man pages (livna bug #1181)
cp -a docs/man/man3 man3
pushd man3
mv actual.3 Sound_Sample::actual.3
mv author.3 Sound_DecoderInfo::author.3
mv buffer.3 Sound_Sample::buffer.3
mv buffer_size.3 Sound_Sameple::buffer_size.3
mv channels.3 Sound_AudioInfo::channels.3
mv decoder.3 Sound_Sample::decoder.3
mv description.3 Sound_DecoderInfo::description.3
mv desired.3 Sound_Sample::desired.3
mv extensions.3 Sound_DecoderInfo::extensions.3
mv flags.3 Sound_Sample::flags.3
mv format.3 Sound_AudioInfo::format.3
mv major.3 Sound_Version::major.3
mv minor.3 Sound_Version::minor.3
mv opaque.3 Sound_Sample::opaque.3
mv patch.3 Sound_Version::patch.3
mv rate.3 Sound_AudioInfo::rate.3
mv url.3 Sound_DecoderInfo::url.3
popd

mkdir -p %{buildroot}/%{_mandir}
mv man3 %{buildroot}/%{_mandir}

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%ldconfig_scriptlets

%files
%license COPYING
%doc README TODO
%{_libdir}/libSDL_sound-1.0.so.*

%files devel
%doc docs/html
%{_libdir}/libSDL_sound*.so
%{_includedir}/SDL/SDL_sound.h
%{_mandir}/man3/*

%changelog
* Tue Dec 13 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.0.3-32
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr  2 2022 Hans de Goede <hdegoede@redhat.com> - 1.0.3-30
- Remove /usr/bin/playsound* from the package to avoid conflict with SDL2_sound,
  users who want this should use SDL2_sound (#2069453)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 28 2018 Hans de Goede <j.w.r.degoede@hhs.nl> - 1.0.3-21
- Fix FTBFS (rhbz#1555579)
- Enable mp3 support now that it is allowed in Fedora (rhbz#1561308)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec  9 2011 Tom Callaway <spot@fedoraproject.org> - 1.0.3-8
- rebuild again

* Fri Dec  9 2011 Tom Callaway <spot@fedoraproject.org> - 1.0.3-7
- rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun  1 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.0.3-5
- Rebuild.

* Thu Aug 20 2009 Warren Togami <wtogami@redhat.com> - 1.0.3-4
- rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Apr 21 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.3-1
- New upstream release 1.0.3

* Sun Feb 17 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.1-9
- Rebuild for new libmikmod
- Rebuild with gcc 4.3
- Stop shipping pre-generated doxygen docs, now that doxygen is fixed to no
  longer cause multilib conflicts 

* Sun Oct 28 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.1-8
- Stop unnecessary linking to libvorbisenc (bz 355811)

* Sun Oct 28 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.1-7
- Remove support for patented sound formats (not used by any package in the
  Fedora-verse), submit to Fedora
- Only include html version of doxygen docs (not latex source)
- Update license tag for new licensing guidelines compliance
- Use prebuild doxygen docs to avoid multilib conflicts

* Sat Mar  3 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.0.1-6
- Rebuild for devel

* Sun Dec  3 2006 Christopher Stone <chris.stone@gmail.com> 1.0.1-5
- Fix livna bug #1181
- Add physfs-devel to BR

* Sat Dec  2 2006 Christopher Stone <chris.stone@gmail.com> 1.0.1-4
- Fix bug #1297
- Whitespace cleanup

* Fri Oct  6 2006 Dams <anvil[AT]livna.org> - 1.0.1-3
- Disabled static
- devel packages Requires:SDL-devel because SDL_sound.h requires SDL.h
- a bit of cleanup

* Fri Oct  6 2006 Dams <anvil[AT]livna.org> - 1.0.1-2
- Added disttag

* Sat Feb 18 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0:1.0.1-1
- drop epoch, 0.lvn

* Fri Nov 21 2003 Panu Matilainen <pmatilai@welho.com> 0:1.0.1-0.lvn.1
- Initial RPM release.
