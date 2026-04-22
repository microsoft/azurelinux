## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Building the extra print profiles requires colprof, +4Gb of RAM and
# quite a lot of time. Don't enable this for test builds.
%define enable_print_profiles 0

# SANE is pretty insane when it comes to handling devices, and we get AVCs
# popping up all over the place.
%define enable_sane 0

Summary:   Color daemon
Name:      colord
Version:   1.4.8
Release:   %autorelease
License:   GPL-2.0-or-later AND LGPL-2.1-or-later
URL:       https://www.freedesktop.org/software/colord/
Source0:   https://www.freedesktop.org/software/colord/releases/%{name}-%{version}.tar.xz

%if !0%{?rhel}
BuildRequires:  pkgconfig(bash-completion)
%endif
BuildRequires: color-filesystem
BuildRequires: docbook5-style-xsl
BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel
BuildRequires: libxslt
BuildRequires: meson
BuildRequires: vala
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(gusb) >= 0.2.7
BuildRequires: pkgconfig(lcms2) >= 2.6
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(polkit-gobject-1) >= 0.103
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(systemd)

# for SANE support
%if 0%{?enable_sane}
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(sane-backends)
%endif

Requires: color-filesystem
BuildRequires: systemd, systemd-rpm-macros
%{?systemd_requires}
Requires: colord-libs%{?_isa} = %{version}-%{release}

# Self-obsoletes to fix the multilib upgrade path
Obsoletes: colord < 0.1.27-3

# obsolete separate profiles package
Obsoletes: shared-color-profiles <= 0.1.6-2
Provides: shared-color-profiles

%description
colord is a low level system activated daemon that maps color devices
to color profiles in the system context.

%package libs
Summary: Color daemon library

%description libs
colord is a low level system activated daemon that maps color devices
to color profiles in the system context.

%package devel
Summary: Development package for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Obsoletes: colorhug-client-devel <= 0.1.13

%description devel
Files for development with %{name}.

%package devel-docs
Summary: Developer documentation package for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description devel-docs
Documentation for development with %{name}.

%package extra-profiles
Summary: More color profiles for color management that are less commonly used
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

# obsolete separate profiles package
Obsoletes: shared-color-profiles-extra <= 0.1.6-2
Provides: shared-color-profiles-extra

%description extra-profiles
More color profiles for color management that are less commonly used.
This may be useful for CMYK soft-proofing or for extra device support.

%package tests
Summary: Data files for installed tests

%description tests
Data files for installed tests.

%prep
%autosetup -p1

%build
# Set ~2 GiB limit so that colprof is forced to work in chunks when
# generating the print profile rather than trying to allocate a 3.1 GiB
# chunk of RAM to put the entire B-to-A tables in.
ulimit -Sv 2000000

%meson \
    -Dtests=false \
    -Dvapi=true \
    -Dinstalled_tests=true \
    -Dprint_profiles=false \
%if 0%{?enable_sane}
    -Dsane=true \
%endif
%if 0%{?rhel}
    -Dbash_completion=false \
    -Dargyllcms_sensor=false \
%endif
%if !0%{?rhel}
    -Dlibcolordcompat=true \
%endif
    -Ddaemon_user=colord

%meson_build

%install
%meson_install

# databases
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/colord/mapping.db
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/colord/storage.db

%find_lang %{name}


%post
%systemd_post colord.service

%preun
%systemd_preun colord.service

%postun
%systemd_postun colord.service

%ldconfig_scriptlets libs

%files -f %{name}.lang
%doc README.md AUTHORS NEWS
%license COPYING
%{_libexecdir}/colord
%attr(755,colord,colord) %dir %{_localstatedir}/lib/colord
%attr(755,colord,colord) %dir %{_localstatedir}/lib/colord/icc
%{_bindir}/*
%{_datadir}/glib-2.0/schemas/org.freedesktop.ColorHelper.gschema.xml
%{_datadir}/dbus-1/system.d/org.freedesktop.ColorManager.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorManager*.xml
%{_datadir}/polkit-1/actions/org.freedesktop.color.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.ColorManager.service
%{_datadir}/metainfo/org.freedesktop.colord.metainfo.xml
%{_mandir}/man1/*.1*
%{_datadir}/colord
%if !0%{?rhel}
%{_datadir}/bash-completion/completions/colormgr
%endif
/usr/lib/udev/rules.d/*.rules
/usr/lib/tmpfiles.d/colord.conf
%{_libdir}/colord-sensors
%{_libdir}/colord-plugins
%ghost %attr(-,colord,colord) %{_localstatedir}/lib/colord/*.db
%{_unitdir}/colord.service
%{_sysusersdir}/colord-sysusers.conf

# session helper
%{_libexecdir}/colord-session
%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorHelper.xml
%{_datadir}/dbus-1/services/org.freedesktop.ColorHelper.service
%{_userunitdir}/colord-session.service

# sane helper
%if 0%{?enable_sane}
%{_libexecdir}/colord-sane
%endif

# common colorspaces
%dir %{_icccolordir}/colord
%{_icccolordir}/colord/AdobeRGB1998.icc
%{_icccolordir}/colord/ProPhotoRGB.icc
%{_icccolordir}/colord/Rec709.icc
%{_icccolordir}/colord/SMPTE-C-RGB.icc
%{_icccolordir}/colord/sRGB.icc

# monitor test profiles
%{_icccolordir}/colord/Bluish.icc

# named color profiles
%{_icccolordir}/colord/x11-colors.icc

%files libs
%doc COPYING
%{_libdir}/libcolord.so.2*
%{_libdir}/libcolordprivate.so.2*
%{_libdir}/libcolorhug.so.2*
%if !0%{?rhel}
%{_libdir}/libcolordcompat.so
%endif

%{_libdir}/girepository-1.0/*.typelib

%files extra-profiles
# other colorspaces not often used
%{_icccolordir}/colord/AppleRGB.icc
%{_icccolordir}/colord/BestRGB.icc
%{_icccolordir}/colord/BetaRGB.icc
%{_icccolordir}/colord/BruceRGB.icc
%{_icccolordir}/colord/CIE-RGB.icc
%{_icccolordir}/colord/ColorMatchRGB.icc
%{_icccolordir}/colord/DonRGB4.icc
%{_icccolordir}/colord/ECI-RGBv1.icc
%{_icccolordir}/colord/ECI-RGBv2.icc
%{_icccolordir}/colord/EktaSpacePS5.icc
%{_icccolordir}/colord/Gamma*.icc
%{_icccolordir}/colord/NTSC-RGB.icc
%{_icccolordir}/colord/PAL-RGB.icc
%{_icccolordir}/colord/SwappedRedAndGreen.icc
%{_icccolordir}/colord/WideGamutRGB.icc

# other named color profiles not generally useful
%{_icccolordir}/colord/Crayons.icc

%files devel
%{_includedir}/colord-1
%{_libdir}/libcolord.so
%{_libdir}/libcolordprivate.so
%{_libdir}/libcolorhug.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/colord.vapi
%{_datadir}/vala/vapi/colord.deps

%files devel-docs
%dir %{_datadir}/gtk-doc/html/colord
%{_datadir}/gtk-doc/html/colord/*

%files tests
%dir %{_libexecdir}/installed-tests/colord
%{_libexecdir}/installed-tests/colord/*
%dir %{_datadir}/installed-tests/colord
%{_datadir}/installed-tests/colord/*

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 1.4.8-3
- Latest state for colord

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 23 2025 Richard Hughes <richard@hughsie.com> - 1.4.8-1
- New upstream release

* Sat Jun 21 2025 Adam Williamson <awilliam@redhat.com> - 1.4.7-8
- Backport PR #183 to fix crash on first start

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.7-7
- Drop call to %%sysusers_create_compat

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 20 2024 ZhengYu He <hezhy472013@gmail.com> - 1.4.7-4
- Use pkgconfig for package bash-completion

* Mon Jan 29 2024 Richard Hughes <richard@hughsie.com> - 1.4.7-3
- Backport a patch to fix ProtectSystem=strict

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Richard Hughes <richard@hughsie.com> - 1.4.7-1
- New upstream release

* Mon Jan 22 2024 Richard Hughes <richard@hughsie.com> - 1.4.6-10
- Fix mass-rebuild failure

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Oct 01 2023 Daan De Meyer <daan.j.demeyer@gmail.com> - 1.4.6-8
- Provide a sysusers.d file to get user() and group() provides

* Fri Aug 18 2023 David King <amigadave@amigadave.com> - 1.4.6-7
- Rebuild for glib2 symbol export fix (#2232723)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 02 2023 David King <amigadave@amigadave.com> - 1.4.6-5
- Use pkgconfig for BuildRequires

* Wed Feb 22 2023 Richard Hughes <richard@hughsie.com> - 1.4.6-4
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 16 2022 Richard Hughes <richard@hughsie.com> - 1.4.6-1
- New upstream version

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 02 2020 Richard Hughes <richard@hughsie.com> - 1.4.5-1
- New upstream version

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 14 2020 Jeff Law <law@redhat.com> - 1.4.4-5
- Fix date in changelog

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Richard Hughes <richard@hughsie.com> - 1.4.4-3
- Remove the BR for argyllcms as it is now orphaned

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 Richard Hughes <richard@hughsie.com> - 1.4.4-1
- New upstream version

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 1.4.3-4
- Update BRs for vala packaging changes

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 18 2018 Richard Hughes <richard@hughsie.com> - 1.4.3-1
- New upstream version

* Mon Mar 12 2018 Richard Hughes <richard@hughsie.com> - 1.4.2-1
- New upstream version

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.1-6
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.1-4
- Switch to %%ldconfig_scriptlets

* Thu Jan 25 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.1-3
- Fix systemd executions/requirements

* Sat Jan 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.1-2
- Remove obsolete scriptlets

* Mon Aug 21 2017 Richard Hughes <richard@hughsie.com> - 1.4.1-1
- New upstream version

* Wed Aug 09 2017 Richard Hughes <richard@hughsie.com> - 1.4.0-1
- New upstream version

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-3
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 27 2017 Richard Hughes <richard@hughsie.com> - 1.3.5-1
- New upstream version

* Thu Feb 23 2017 Kalev Lember <klember@redhat.com> - 1.3.4-4
- Use macros for systemd system and user unit dirs

* Thu Feb 23 2017 Kalev Lember <klember@redhat.com> - 1.3.4-3
- Use same -fno-strict-aliasing option as the RHEL build does

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 21 2016 Richard Hughes <richard@hughsie.com> - 1.3.4-1
- New upstream version

* Mon Nov 21 2016 Richard Hughes <richard@hughsie.com> - 1.3.3-2
- Install the libcolordcompat.so in the main -libs package

* Wed Jul 27 2016 Richard Hughes <richard@hughsie.com> - 1.3.3-1
- New upstream version

* Tue Mar 22 2016 Richard Hughes <richard@hughsie.com> - 1.3.2-1
- New upstream version

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Dan Horák <dan@danny.cz> - 1.3.1-3
- fix bogus date in changelog

* Fri Jan 29 2016 Dan Horák <dan@danny.cz> - 1.3.1-2
- fix non-Fedora build

* Fri Nov 27 2015 Richard Hughes <richard@hughsie.com> - 1.3.1-1
- New upstream version

* Wed Aug 19 2015 Richard Hughes <richard@hughsie.com> - 1.2.12-1
- New upstream version

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 1.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Richard Hughes <richard@hughsie.com> - 1.2.11-1
- New upstream version

* Wed Apr 08 2015 Richard Hughes <richard@hughsie.com> - 1.2.10-1
- New upstream version

* Sun Mar 29 2015 Richard Hughes <richard@hughsie.com> - 1.2.9-2
- Fix a crash when calibrating

* Fri Feb 20 2015 Richard Hughes <richard@hughsie.com> - 1.2.9-1
- New upstream version

* Thu Jan 15 2015 Richard Hughes <richard@hughsie.com> - 1.2.8-1
- New upstream version

* Tue Dec 02 2014 Richard Hughes <richard@hughsie.com> - 1.2.7-1
- New upstream version

* Mon Nov 24 2014 Richard Hughes <richard@hughsie.com> - 1.2.6-2
- trivial: Require argyllcms for spotread detection

* Mon Nov 24 2014 Richard Hughes <richard@hughsie.com> - 1.2.6-1
- New upstream version

* Mon Nov 10 2014 Richard Hughes <richard@hughsie.com> - 1.2.5-1
- New upstream version

* Mon Oct 27 2014 Richard Hughes <richard@hughsie.com> - 1.2.4-3
- Disable the print profiles on rawhide

* Mon Oct 27 2014 Richard Hughes <richard@hughsie.com> - 1.2.4-2
- Backport a patch to fix calibration using the helper

* Sun Oct 12 2014 Richard Hughes <richard@hughsie.com> - 1.2.4-1
- New upstream version

* Sun Sep 14 2014 Kalev Lember <kalevlember@gmail.com> - 1.2.3-3
- Fix the build

* Sun Sep 14 2014 Richard Hughes <richard@hughsie.com> - 1.2.3-2
- Enable the print profile generation

* Fri Sep 12 2014 Richard Hughes <richard@hughsie.com> - 1.2.3-1
- New upstream version

* Mon Aug 18 2014 Richard Hughes <richard@hughsie.com> - 1.2.2-1
- New upstream version

* Sat Aug 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.2.1-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Richard Hughes <richard@hughsie.com> - 1.2.1-1
- New upstream version

* Sat Apr 05 2014 Richard Hughes <richard@hughsie.com> - 1.2.0-1
- New upstream version

* Fri Feb 28 2014 Richard Hughes <richard@hughsie.com> - 1.1.7-1
- New upstream version

* Fri Feb 28 2014 Rex Dieter <rdieter@math.unl.edu> - 1.1.6-4
- revert Conflicts: icc-profiles-openicc pending (hopefully) better
  solution (#1069672)

* Tue Jan 21 2014 Richard Hughes <richard@hughsie.com> - 1.1.6-3
- We don't actually need the valgrind BR...

* Tue Jan 21 2014 Dan Horák <dan@danny.cz> - 1.1.6-2
- valgrind is available only on selected arches

* Mon Jan 20 2014 Richard Hughes <richard@hughsie.com> - 1.1.6-1
- New upstream version

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.1.5-4
- Move ldconfig %%post* scriptlets to -libs.
- Run test suite during build.
- Fix bogus date in %%changelog.

* Thu Dec 19 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.1.5-3
- Drop tarball from git.

* Wed Dec 11 2013 Richard Hughes <richard@hughsie.com> - 1.1.5-2
- Add conflict on icc-profiles-openicc

* Wed Dec 11 2013 Richard Hughes <richard@hughsie.com> - 1.1.5-1
- New upstream version

* Tue Nov 19 2013 Richard Hughes <richard@hughsie.com> - 1.1.4-1
- New upstream version

* Wed Oct 30 2013 Richard Hughes <richard@hughsie.com> - 1.1.3-1
- New upstream version

* Fri Sep 13 2013 Richard Hughes <richard@hughsie.com> - 1.1.2-1
- New upstream version

* Tue Jul 30 2013 Richard Hughes <richard@hughsie.com> - 1.1.1-1
- New upstream version

* Thu Jul 18 2013 Matthias Clasen <mclasen@redhat.com> - 1.0.2-2
- Add an archful dep

* Sun Jul 07 2013 Richard Hughes <richard@hughsie.com> - 1.0.2-1
- New upstream version

* Tue Jun 18 2013 Richard Hughes <richard@hughsie.com> - 1.0.1-2
- Disable bash-completion on RHEL -- harder

* Tue Jun 11 2013 Richard Hughes <richard@hughsie.com> - 1.0.1-1
- New upstream version

* Mon May 13 2013 Richard Hughes <richard@hughsie.com> - 1.0.0-1
- New upstream version

* Tue May 07 2013 Richard Hughes <richard@hughsie.com> - 0.1.34-4
- argyllcms is not available on RHEL

* Tue May 07 2013 Richard Hughes <richard@hughsie.com> - 0.1.34-3
- bash-completion is not available on RHEL

* Wed May 01 2013 Richard Hughes <richard@hughsie.com> - 0.1.34-2
- Fix BRs

* Wed May 01 2013 Richard Hughes <richard@hughsie.com> - 0.1.34-1
- New upstream version
- Add a ICC transform object for simple RGB conversions
- Add a warning for RGB profiles with unlikely whitepoint values
- Add Qt DBus annotations
- Allow clients to call org.freedesktop.DBus.Peer
- Correct a lot more company names when creating devices
- Do not automatically add EDID profiles with warnings to devices
- Increase the delay between patches in the session-helper
- Install the bash completion support into /usr

* Wed Apr 24 2013 Václav Pavlín <vpavlin@redhat.com> - 0.1.33-2
- Add new systemd macros (#856659)

* Tue Apr 16 2013 Richard Hughes <richard@hughsie.com> - 0.1.33-1
- New upstream version
- Add some translated profile descriptions for the CMYK profiles
- Add the FOGRA45L and FOGRA47L CMYK and eciRGBv1 profiles
- Check the generated CCMX matrix for invalid data
- Do not print a warning if the DBus property does not exist
- Ensure mbstowcs() has an LC_CTYPE of 'en_US.UTF-8'
- Always write C-locale floating point values in IT8 files
- Initialize the value of the CCMX matrix
- Never promote localized v2 ICC profiles to v4
- Rename ISOnewspaper26 to IFRA26S_2004_newsprint

* Thu Mar 28 2013 Richard Hughes <richard@hughsie.com> - 0.1.32-1
- New upstream version
- Add a new tool 'cd-iccdump' that can dump V4 and V2 profiles
- Add translated descriptions to the ICC profiles

* Mon Mar 18 2013 Richard Hughes <richard@hughsie.com> - 0.1.31-1
- New upstream version
- Calculate the display calibration based on the Lab and target display
  gamma
- Interpolate the gamma data to the VCGT size using Akima
- Add some more display vendor names to the display fixup table
- Fix the argyll sensor driver when using the ColorMunki Smile
- Fix the gamut warning to check primaries wider than CIERGB and ProPhoto
- Move the private sensor libraries out of the pure lib space

* Sun Feb 17 2013 Richard Hughes <richard@hughsie.com> - 0.1.30-1
- New upstream version
- Append -private to the driver libraries as they have no headers installed
- Do not show duplicate profiles when icc-profiles-openicc is installed
- Speed up the daemon loading and use less I/O at startup

* Mon Feb 04 2013 Richard Hughes <richard@hughsie.com> - 0.1.29-1
- New upstream version
- Add a --verbose and --version argument to colormgr
- Add DTP94 native sensor support
- Allow profiles to have a 'score' which affects the standard space
- Change the Adobe RGB description to be 'Compatible with Adobe RGB (1998)'
- Detect profiles from adobe.com and color.org and add metadata
- Do not auto-add profiles due to device-id metadata if they have been
  removed
- Ensure profiles with MAPPING_device_id get auto-added to devices
- Install various helper libraries for access to hardware
- Set the additional 'OwnerCmdline' metadata on each device

* Fri Jan 18 2013 Richard Hughes <richard@hughsie.com> - 0.1.28-2
- Backport some fixes from upstream for gnome-settings-daemon.

* Wed Jan 16 2013 Richard Hughes <richard@hughsie.com> - 0.1.28-1
- New upstream version
- Add some default GSetting schema values for the calibration helper
- Add the sensor images as metadata on the D-Bus interface
- Quit the session helper if the device or sensor was not found

* Mon Jan 14 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-17
- Regenerate Makefiles because of patch 0, harder

* Mon Jan 14 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-16
- Regenerate Makefiles because of patch 0, harder

* Mon Jan 14 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-15
- Regenerate Makefiles because of patch 0

* Mon Jan 14 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-14
- Add BR systemd-devel so the seat tracking stuff works
- Build with full compiler output
- Do not build the profiles in parallel, backported from upstream
- Limit the memory allocation to 2GiB when building profiles
- Do not attempt to build the print profiles on ARM or PPC hardware

* Mon Jan 14 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-13
- Do not attempt to build the print profiles on ARM hardware

* Mon Jan 14 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-12
- Limit the memory allocation to 2GiB when building profiles

* Mon Jan 14 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-11
- Do not build the profiles in parallel, backported from upstream

* Mon Jan 14 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-10
- Build with full compiler output

* Mon Jan 14 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-9
- Add BR systemd-devel so the seat tracking stuff works

* Fri Jan 11 2013 Kalev Lember <kalevlember@gmail.com> - 0.1.27-8
- Self-obsoletes to fix the multilib upgrade path

* Thu Jan 10 2013 Kalev Lember <kalevlember@gmail.com> - 0.1.27-7
- Split out libcolord to colord-libs subpackage so that the daemon package
  doesn't get multilibbed.

* Thu Jan 10 2013 Kalev Lember <kalevlember@gmail.com> - 0.1.27-6
- Remove unneeded defattr() lines

* Wed Jan 09 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-5
- Add BR color-filesystem for _icccolordir

* Wed Jan 09 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-4
- Don't enable the print profiles at this time

* Tue Jan 08 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-3
- trivial: Fix a %%changelog date

* Tue Jan 08 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-2
- ...and with the tarball uploaded.

* Tue Jan 08 2013 Richard Hughes <richard@hughsie.com> - 0.1.27-1
- New upstream version
- Add some more calibration attach images
- Import shared-color-profiles into colord
- Install a header with all the session helper defines

* Tue Jan 08 2013 Matthias Clasen <mclasen@redhat.com> - 0.1.26-2
- harden the build

* Wed Dec 19 2012 Richard Hughes <richard@hughsie.com> - 0.1.26-1
- New upstream version
- Add a session helper that can be used to calibrate the screen
- Add some defines for the Spyder4 display colorimeter
- Add support for reading and writing .cal files to CdIt8
- Add the ability to 'disable' a device from a color POV
- Create ICCv2 profiles when using cd-create-profile
- Use enumerated error values in the client library
- Use spotread when there is no native sensor driver

* Mon Nov 26 2012 Richard Hughes <richard@hughsie.com> - 0.1.25-1
- New upstream version
- Add a create-standard-space sub-command to cd-create-profile
- Add a profile metadata key of 'License'
- Add a set-version command to the cd-fix-profile command line tool
- Create linear vcgt tables when using create-x11-gamma
- Fix GetStandardSpace so it can actually work
- Move the named color examples to shared-color-profiles

* Wed Nov 21 2012 Richard Hughes <richard@hughsie.com> - 0.1.24-2
- Apply a patch from upstream so we can use cd-fix-profile in

* Fri Oct 26 2012 Richard Hughes <richard@hughsie.com> - 0.1.24-1
- New upstream version
- Fix a critical warning when user tries to dump a non-icc file
- Remove libsane support and rely only on udev for scanner information
- Set the seat for devices created in the session and from udev

* Wed Aug 29 2012 Richard Hughes <richard@hughsie.com> - 0.1.23-2
- Fix file lists

* Wed Aug 29 2012 Richard Hughes <richard@hughsie.com> - 0.1.23-1
- New upstream version
- Assorted documentation fixes
- Do not try to add duplicate sysfs devices

* Wed Jul 18 2012 Dennis Gilmore <dennis@ausil.us> - 0.1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Richard Hughes <richard@hughsie.com> - 0.1.22-1
- New upstream version
- Split out colord-gtk to a new sub-project to prevent a dep loop
- Add many generic introspection type arguments
- Check any files in /usr/share/color/icc have the content type
- Do not create the same object paths if two sensors are plugged in
- Fix the udev rules entry for the i1Display3

* Tue May 22 2012 Richard Hughes <richard@hughsie.com> - 0.1.21-1
- New upstream version
- Do not install any parts of colord-sane if --disable-sane is specified
- Fix InstallSystemWide() by not writing a private file
- Save the CCMX and ITx files to be compatible with argyllcms
- The ColorHug has a new VID and PID

* Wed May 09 2012 Richard Hughes <richard@hughsie.com> - 0.1.20-1
- New upstream version
- Add a sensor-set-options command to the colormgr tool
- Add the concept of 'options' on each color sensor device
- Enable gtk-doc in the default distro build

* Tue Apr 17 2012 Richard Hughes <richard@hughsie.com> - 0.1.19-1
- New upstream version
- Add a user suffix to the object path of user-created devices and profiles

* Thu Mar 29 2012 Richard Hughes <richard@hughsie.com> - 0.1.18-2
- Disable PrivateNetwork=1 as it breaks sensor hotplug.

* Thu Mar 15 2012 Richard Hughes <richard@hughsie.com> - 0.1.18-1
- New upstream version
- Add a Manager.CreateProfileWithFd() method for QtDBus
- Split out the SANE support into it's own process
- Fix a small leak when creating devices and profiles in clients
- Fix cd-fix-profile to add and remove metadata entries
- Install per-machine profiles in /var/lib/colord/icc

* Wed Feb 22 2012 Richard Hughes <richard@hughsie.com> - 0.1.17-1
- New upstream version
- Add an LED sample type
- Add PrivateNetwork and PrivateTmp to the systemd service file
- Fix InstallSystemWide() when running as the colord user

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 0.1.16-6
- bump rev

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 0.1.16-5
- more fixes

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 0.1.16-4
- More fixes

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 0.1.16-3
- fix patch

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 0.1.16-2
- fix a gsd crash

* Tue Jan 17 2012 Richard Hughes <richard@hughsie.com> - 0.1.16-1
- New upstream version Now runs as a colord user rather than as root.
  Support more ICC metadata keys Install a systemd service file Support 2nd
  generation Huey hardware

* Thu Jan 12 2012 Dennis Gilmore <dennis@ausil.us> - 0.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Richard Hughes <richard@hughsie.com> - 0.1.15-1
- New upstream version This release fixes an important security bug:
  CVE-2011-4349. Do not crash the daemon if adding the device to the db
  failed Fix a memory leak when getting properties from a device

* Tue Nov 01 2011 Richard Hughes <richard@hughsie.com> - 0.1.14-1
- New upstream version Remove upstreamed patches

* Mon Oct 03 2011 Richard Hughes <richard@hughsie.com> - 0.1.13-1
- New upstream version Ensure uid 0 can always create devices and profiles
  Reduce the CPU load of clients when assigning profiles

* Tue Aug 30 2011 Richard Hughes <richard@hughsie.com> - 0.1.12-1
- New upstream version

* Mon Aug 01 2011 Richard Hughes <richard@hughsie.com> - 0.1.11-2
- Remove the sedding libtool's internals as it breaks generation of the
  GObject Introspection data.

* Mon Aug 01 2011 Richard Hughes <richard@hughsie.com> - 0.1.11-1
- New upstream version

* Wed Jul 06 2011 Richard Hughes <richard@hughsie.com> - 0.1.10-1
- New upstream version

* Mon Jun 13 2011 Richard Hughes <richard@hughsie.com> - 0.1.9-1
- New upstream version

* Thu Jun 02 2011 Richard Hughes <richard@hughsie.com> - 0.1.8-1
- New upstream version Add a webcam device kind Add a timestamp when making
  profiles default Add support for reading and writing ICC profile metadata
  Allow the client to pass file descriptors out of band to CreateProfile
  Prettify the device vendor and model names Split out the sensors into
  runtime-loadable shared objects Provide some GIO async variants for the
  methods in CdClient Ensure GPhoto2 devices get added to the device list

* Fri May 06 2011 Richard Hughes <richard@hughsie.com> - 0.1.7-1
- New upstream version. Create /var/lib/colord at buildtime not runtime for
  SELinux Ensure profiles with embedded profile checksums are parsed
  correctly Move the colorimeter rules to be run before 70-acl.rules Stop
  watching the client when the sensor is finalized Ensure the source is
  destroyed when we unref CdUsb to prevent a crash Only enable the volume
  mount tracking when searching volumes

* Tue Apr 26 2011 Richard Hughes <richard@hughsie.com> - 0.1.6-2
- Own /var/lib/colord and /var/lib/colord/*.db

* Sun Apr 24 2011 Richard Hughes <richard@hughsie.com> - 0.1.6-1
- New upstream version.

* Thu Mar 31 2011 Richard Hughes <richard@hughsie.com> - 0.1.5-1
- New upstream version.

* Wed Mar 09 2011 Richard Hughes <richard@hughsie.com> - 0.1.4-1
- New upstream version.

* Mon Feb 28 2011 Richard Hughes <richard@hughsie.com> - 0.1.3-1
- New upstream version.

* Tue Feb 08 2011 Dennis Gilmore <dennis@ausil.us> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Richard Hughes <richard@hughsie.com> - 0.1.1-2
- Rebuild in the vain hope koji isn't broken today.

* Wed Jan 26 2011 Richard Hughes <richard@hughsie.com> - 0.1.1-1
- New upstream version.

* Thu Jan 13 2011 Richard Hughes <richard@hughsie.com> - 0.1.0-1
- Initial version for Fedora package review.
## END: Generated by rpmautospec
