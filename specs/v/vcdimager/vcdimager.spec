# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: VideoCD (pre-)mastering and ripping tool
Name:    vcdimager
Version: 2.0.1
Release: 23%{?dist}
License: GPL-2.0-or-later
URL:     http://www.gnu.org/software/vcdimager/
Source:  https://ftp.gnu.org/pub/gnu/vcdimager/vcdimager-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: libcdio-devel >= 0.72
BuildRequires: libxml2-devel >= 2.3.8
BuildRequires: pkgconfig >= 0.9
BuildRequires: popt-devel
BuildRequires: zlib-devel

Requires:        %{name}-libs%{?_isa} = %{version}-%{release}


%description
VCDImager allows you to create VideoCD BIN/CUE CD images from MPEG
files. These can be burned with cdrdao or any other program capable of
burning BIN/CUE files.

Also included is VCDRip which does the reverse operation, that is to
rip MPEG streams from images or burned VideoCDs and to show
information about a VideoCD.

%package libs
Summary: Libraries for %{name}

%description libs
The %{name}-libs package contains shared libraries for %{name}.

%package devel
Summary:  Header files and library for VCDImager
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: libcdio-devel

%description devel
VCDImager allows you to create VideoCD BIN/CUE CD images from mpeg
files which can be burned with cdrdao or any other program capable of
burning BIN/CUE files.

This package contains the header files and a library to develop
applications that will use VCDImager.


%prep
%autosetup -p1


%build
%configure --disable-static --disable-dependency-tracking
%make_build V=1


%install
%make_install
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

# Sometimes this file gets created... but we don't want it!
rm -f %{buildroot}%{_infodir}/dir


%ldconfig_scriptlets libs


%files
%doc AUTHORS BUGS ChangeLog* FAQ NEWS README THANKS TODO
%doc frontends/xml/videocd.dtd
%license COPYING
%{_bindir}/cdxa2mpeg
%{_bindir}/vcd-info
%{_bindir}/vcdimager
%{_bindir}/vcdxbuild
%{_bindir}/vcdxgen
%{_bindir}/vcdxminfo
%{_bindir}/vcdxrip
%{_infodir}/vcdxrip.info*
%{_infodir}/vcdimager.info*
%{_infodir}/vcd-info.info*
%{_mandir}/man1/cdxa2mpeg.1*
%{_mandir}/man1/vcd-info.1*
%{_mandir}/man1/vcdimager.1*
%{_mandir}/man1/vcdxbuild.1*
%{_mandir}/man1/vcdxgen.1*
%{_mandir}/man1/vcdxminfo.1*
%{_mandir}/man1/vcdxrip.1*

%files libs
%{_libdir}/libvcdinfo.so.0*

%files devel
%doc HACKING
%{_includedir}/libvcd/
%{_libdir}/libvcdinfo.so
%{_libdir}/pkgconfig/libvcdinfo.pc


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 03 2024 Xavier Bachelot <xavier@bachelot.org> - 2.0.1-20
- Change Source: URL to https
- Drop EL7 conditionals
- Sort BR:s

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 08 2023 Xavier Bachelot <xavier@bachelot.org> - 2.0.1-16
- Use SPDX for License: tag
- Use glob for manpages encoding

* Wed Mar 08 2023 Xavier Bachelot <xavier@bachelot.org> - 2.0.1-15
- Review fixes

* Tue Mar 07 2023 Xavier Bachelot <xavier@bachelot.org> - 2.0.1-14
- Drop Group: Tags
- Specify soname

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Apr 10 2020 Leigh Scott <leigh123linux@gmail.com> - 2.0.1-8
- Rebuild for new libcdio version

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.0.1-4
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.0.1-1
- Update to 2.0.1

* Sat Jan 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.7.24-13
- Rebuild for new libcdio
- Clean up spec file

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.7.24-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.7.24-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 18 2016 Adrian Reber <adrian@lisas.de> - 0.7.24-10
- Rebuilt for libcdio-0.94

* Fri Jul 08 2016 Sérgio Basto <sergio@serjux.com> - 0.7.24-9
- Bump release for unretire in F23

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 0.7.24-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Feb 21 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-7
- Rebuilt

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-6
- Rebuilt for new libcdio

* Wed May 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-5
- Remove static statement in the devel sub-package - rfbz#2312

* Tue Apr 17 2012 Matthias Saou <matthias@saou.eu> 0.7.24-4
- Minor spec file cleanups.

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-2
- Rebuilt for libcdio update

* Thu Jun 09 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-1
- Update to 0.7.24

* Sun Jan 24 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.7.23-13
- Rebuild for libcdio

* Wed Nov 25 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.7.23-11
- Rebuild for F-12

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.7.23-10
- rebuild for new F11 features

* Thu Jan 15 2009 kwizart < kwizart at gmail.com > - 0.7.23-9
- Rebuild for libcdio 

* Thu Sep  4 2008 kwizart < kwizart at gmail.com > - 0.7.23-8
- Fix URL
- vcdimager-devel Requires libcdio-devel
- Split libs (multilibs compliance)

* Sat Aug 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.7.23-7
- merge a few bits from livna spec

* Fri May 16 2008 Matthias Saou <http://freshrpms.net/> 0.7.23-6
- Rebuild for Fedora 9.
- Add missing ldconfig calls and scriplet info requirements.

* Sun Sep 24 2006 Matthias Saou <http://freshrpms.net/> 0.7.23-5
- Rebuild against new libcdio.

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 0.7.23-4
- Release bump to drop the disttag number in FC5 build.

* Fri Jan 13 2006 Matthias Saou <http://freshrpms.net/> 0.7.23-3
- Silence install-info scriplets.

* Sat Jul 30 2005 Matthias Saou <http://freshrpms.net/> 0.7.23-2
- Rebuild against new libcdio.

* Tue Jul 12 2005 Matthias Saou <http://freshrpms.net/> 0.7.23-1
- Update to 0.7.23.
- Update libcdio-devel requirement to >= 0.72.
- Change source location from vcdimager.org to gnu.org for this release...

* Tue Jun 28 2005 Matthias Saou <http://freshrpms.net/> 0.7.22-2
- Prevent scriplets from failing if the info calls return an error.

* Tue May 17 2005 Matthias Saou <http://freshrpms.net/> 0.7.22-1
- Update to 0.7.22.

* Sun Apr 17 2005 Matthias Saou <http://freshrpms.net/> 0.7.21-1
- Update to 0.7.21 at last.
- Split off new -devel package.
- Added libcdio build requirement.
- Update Source URL, it's not "UNSTABLE" anymore.
- Remove vcddump.info and add vcd-info.info. Remove .gz from scriplets.

* Mon Aug 30 2004 Matthias Saou <http://freshrpms.net/> 0.7.14-4
- Added missing install-info calls.

* Mon May 24 2004 Matthias Saou <http://freshrpms.net/> 0.7.14-3
- Tried and update to 0.7.20, but the looping libcd* deps are a problem.
- Rebuild for Fedora Core 2.

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 0.7.14-2
- Rebuild for Fedora Core 1.

* Fri May  2 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.7.14.
- Remove infodir/dir, thanks to Florin Andrei.
- Updated URL/Source.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Fri Feb 28 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.7.13.
- Removed the now unnecessary libxml fix.

* Tue Jan 14 2003 Matthias Saou <http://freshrpms.net/>
- Fix xmlversion.h include path in configure since xml is disabled otherwise,
  thanks to Rudolf Kastl for spotting the problem.

* Fri Jan  3 2003 Matthias Saou <http://freshrpms.net/>
- Let's try the 1 year old 0.7 development branch!

* Mon Dec  9 2002 Matthias Saou <http://freshrpms.net/>
- Spec file cleanup.

* Sat Jan 20 2001 Herbert Valerio Riedel <hvr@gnu.org>
- added THANKS file as doc

* Thu Jan  4 2001 Herbert Valerio Riedel <hvr@gnu.org>
- fixed removal of info pages on updating packages

* Sat Dec 23 2000 Herbert Valerio Riedel <hvr@gnu.org>
- added vcdrip
- removed glib dependancy

* Sat Aug 26 2000 Herbert Valerio Riedel <hvr@gnu.org>
- spec file improvements

* Mon Aug 14 2000 Herbert Valerio Riedel <hvr@gnu.org>
- first spec file

