# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           wildmidi
Version:        0.4.6
Release: 6%{?dist}
Summary:        Softsynth midi player
License:        GPL-3.0-or-later
URL:            https://github.com/Mindwerks/wildmidi
Source0:        https://github.com/Mindwerks/%{name}/archive/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  alsa-lib-devel cmake
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
WildMidi is a software midi player which has a core softsynth library that can
be used with other applications.


%package libs
Summary:        WildMidi Midi Wavetable Synth Lib
License:        LGPL-3.0-or-later
Requires:       timidity++-patches

%description libs
This package contains the WildMidi core softsynth library. The library is
designed to process a midi file and stream out the stereo audio data
through a buffer which an external program can then process further.


%package        devel
Summary:        Development files for %{name}
License:        LGPL-3.0-or-later
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n %{name}-%{version}


%build
%cmake
%cmake_build


%install
%cmake_install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
ln -s ../timidity.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.cfg


%ldconfig_scriptlets libs


%files
%license docs/license/GPLv3.txt
%{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_mandir}/man1/*

%files libs
%license docs/license/LGPLv3.txt
%{_libdir}/libWildMidi.so.2*
%{_mandir}/man5/*

%files devel
%{_includedir}/*
%{_libdir}/cmake/WildMidi
%{_libdir}/libWildMidi.so
%{_libdir}/pkgconfig/wildmidi.pc
%{_mandir}/man3/*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Miroslav Suchý <msuchy@redhat.com> - 0.4.6-2
- convert license to SPDX

* Tue Apr 16 2024 Karel Volný <kvolny@redhat.com> - 0.4.6-1
- New upstream release 0.4.6 (rhbz#2274687)
- Updated URL

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Karel Volný <kvolny@redhat.com> - 0.4.5-1
- New upstream release 0.4.5 (rhbz#2161010)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 09 2021 Karel Volný <kvolny@redhat.com> - 0.4.4-1
- New upstream release 0.4.4 (rhbz#1941415)
- Adds cmake configfiles in devel

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 30 2018 Karel Volný <kvolny@redhat.com> - 0.4.3-1
- New upstream release 0.4.3 (rhbz#1653548)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Hans de Goede <hdegoede@redhat.com> - 0.4.2-1
- New upstream release 0.4.2 (rhbz#1433550)
- Fixes CVE-2017-11661 CVE-2017-11662 CVE-2017-11663 CVE-2017-11664 (#1479315)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 26 2016 Hans de Goede <hdegoede@redhat.com> - 0.4.0-1
- New upstream release 0.4.0 (rhbz#1354068)

* Fri Apr 08 2016 Hans de Goede <hdegoede@redhat.com> - 0.3.9-1
- New upstream release 0.3.9 (rhbz#1078135)
- Fixes crash on bad midi files

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 29 2015 Hans de Goede <hdegoede@redhat.com> - 0.3.8-1
- New upstream release 0.3.8 (rhbz#1078135)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun  6 2014 Hans de Goede <hdegoede@redhat.com> - 0.3.7-2
- Upstream has respun the tarbal, update to the new tarbal

* Fri May 30 2014 Hans de Goede <hdegoede@redhat.com> - 0.3.7-1
- New upstream release 0.3.7 (rhbz#1078135)

* Sun Apr  6 2014 Hans de Goede <hdegoede@redhat.com> 0.3.6-1
- New upstream release 0.3.6 (rhbz#1078135)

* Thu Mar 20 2014 Hans de Goede <hdegoede@redhat.com> 0.3.5-1
- New upstream release 0.3.5 (rhbz#1078135)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.2.3.4-2
- Rebuilt for gcc bug 634757

* Sun Sep 12 2010 Hans de Goede <hdegoede@redhat.com> 0.2.3.4-1
- New upstream release 0.2.3.4-1

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-6
- Fixup Summary

* Mon Jul  7 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-5
- Fix wildmidi cmdline player sound output on bigendian archs (bz 454198),
  patch by Ian Chapman

* Sat Feb  9 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-4
- Change alsa output code to use regular write mode instead of mmap to make
  it work with pulseaudio (bz 431846)

* Sun Oct 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-3
- Require timidity++-patches instead of timidity++ itself so that we don't
  drag in arts and through arts, qt and boost.

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-2
- Put the lib in a seperate -libs subpackage
- Update License tags for new Licensing Guidelines compliance

* Sat Jul 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-1
- Initial Fedora Extras version
