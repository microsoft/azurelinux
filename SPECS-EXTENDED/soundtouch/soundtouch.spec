Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           soundtouch
Version:        2.1.1
Release:        5%{?dist}
Summary:        Audio Processing library for changing Tempo, Pitch and Playback Rates
License:        LGPLv2+
URL:            https://www.surina.net/soundtouch/
Source0:        https://gitlab.com/soundtouch/soundtouch/-/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  autoconf automake libtool

%description
SoundTouch is a LGPL-licensed open-source audio processing library for
changing the Tempo, Pitch and Playback Rates of audio streams or
files. The SoundTouch library is suited for application developers
writing sound processing tools that require tempo/pitch control
functionality, or just for playing around with the sound effects.

The SoundTouch library source kit includes an example utility
SoundStretch which allows processing .wav audio files from a
command-line interface.


%package devel
Summary:  Libraries, includes, etc to develop soundtouch applications
Requires: soundtouch = %{version}-%{release}
Requires: pkgconfig

%description devel
Libraries, include files, etc you can use to develop soundtouch applications.


%prep
%autosetup -p1
# Remove -O3 because we have our default optimizations.
sed -i 's|-O3||' source/SoundTouch/Makefile.*
sed -i 's|-O3||' source/SoundStretch/Makefile.*
autoreconf -iv
# set correct version for .so build
%define ltversion %(echo %{version} | tr '.' ':')
sed -i 's/-rpath $(libdir)/-rpath $(libdir) -version-number %{ltversion}/' \
  source/SoundTouch/Makefile.in
# cleanup a bit
sed -i 's|\r||g' README.html source/SoundTouch/RateTransposer.cpp


%build
%configure --disable-dependency-tracking --disable-static --enable-shared
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make V=1 %{?_smp_mflags}


%install
%make_install
rm %{buildroot}%{_libdir}/*.la

# remove redundant installed docs
rm -rf %{buildroot}%{_docdir}/%{name}

# pkgconfig compat links for compat with older (API compatible) releases
# dunno why upstream keeps changing the pkgconfig name
# Update 2016-02-13: now looks like that is soundtouch.pc without version
ln -s soundtouch.pc %{buildroot}%{_libdir}/pkgconfig/libSoundTouch.pc
ln -s soundtouch.pc %{buildroot}%{_libdir}/pkgconfig/soundtouch-1.0.pc

## soundtouch installs an autoheader generated header file which could very
## well conflict with other autoheader generated header files, so we override
## this with our own version which contains only the bare minimum:
#echo '#define FLOAT_SAMPLES 1' \
#  > %{buildroot}%{_includedir}/soundtouch/soundtouch_config.h


%ldconfig_scriptlets


%files
%doc README.html
%license COPYING.TXT
%{_bindir}/soundstretch
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}
%{_datadir}/aclocal/%{name}.m4


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.1-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 14 2018 Sérgio Basto <sergio@serjux.com> - 2.1.1-1
- Update to 2.1.1
  Bugfixes: Fixed potential buffer overwrite bugs in WavFile routines. Replaced asserts with runtime exceptions.
  Android: Migrated the SoundTouch Android example to new Android Studio
  Automake: unset ACLOCAL in bootstrap script to avoid error in case earlier build script has set it

* Sat Oct 06 2018 Sérgio Basto <sergio@serjux.com> - 2.1.0-1
- Update to 2.1.0

* Tue Aug 14 2018 Hans de Goede <hdegoede@redhat.com> - 2.0.0-6
- The last round of security fixes also fixes CVE-2018-14044, CVE-2018-14045
  (rhbz#1601618, rhbz#1601620, rhbz#1601624, rhbz#1601625)

* Tue Aug 14 2018 Hans de Goede <hdegoede@redhat.com> - 2.0.0-5
- Security fix for CVE-2018-1000223 (rhbz#1609193, rhbz#1609194)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Hans de Goede <hdegoede@redhat.com> 2.0.0-3
- Security fix for CVE-2017-9258, CVE-2017-9259, CVE-2017-9260 (rhbz#1475759)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 28 2017 Sérgio Basto <sergio@serjux.com> - 2.0.0-1
- Update soundtouch to 2.0.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb 13 2016 Sérgio Basto <sergio@serjux.com> - 1.9.2-3
- fix pkgconfig links

* Sat Feb 13 2016 Sérgio Basto <sergio@serjux.com> - 1.9.2-2
- Add license tag.
- Add back sed on -O3 .
- Not modify soundtouch_config.h because looks correct, just have one line !.

* Tue Feb 09 2016 Sérgio Basto <sergio@serjux.com> - 1.9.2-1
- Update to 1.9.2 (#961876).
- Modernize spec file.
- Makefile.am handles mmx and sse flags well, so no need patch 01 and sed anymore.
- Patch 02 disabled, I hope we already have asm fixed on X86_64.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.0-12
- Rebuilt for GCC 5 C++11 ABI change

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.4.0-11
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Hans de Goede <hdegoede@redhat.com> 1.4.0-1
- New upstream release 1.4.0

* Sat Dec 20 2008 Hans de Goede <hdegoede@redhat.com> 1.3.1-11
- Fix compilation with libtool 2.x

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.1-10
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-9
- Fix compilation with gcc 4.3

* Wed Aug 22 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-8
- Rebuild for buildId
- Update license tag for new license guidelines compliance

* Mon Feb 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-7
- Fix building with automake-1.10

* Tue Aug 29 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-6
- FE6 Rebuild

* Wed Aug  2 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-5
- Patch makefiles so that our RPM_OPT_FLAGS get used instead of the custom
  upstream CFLAGS.

* Mon Jul 31 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-4
- Add Requires: pkgconfig to -devel subpackage
- Replace installed autoheader generated header file with our own version
  which contains only the nescesarry soundtouch specific defines, thus avoiding
  possible conflicts with other autoheader generated headers.

* Mon Jul 31 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.3.1-3
- Add BR libtool

* Mon Jul 31 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-2
- Add BR: automake, because upstream uses symlinks to instead of copies of some
  needed automake files.

* Sat Jul 29 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-1
- New upstream version 1.3.1
- Minor specfile cleanups for livna submission.
- Give the .so a proper version instead of 0.0.0
- Don't use rpath in soundstretch binary

* Thu Aug 26 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.2.1-1
- initial build.
