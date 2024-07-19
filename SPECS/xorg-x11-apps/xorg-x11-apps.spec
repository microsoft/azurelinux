# Component versions
%global oclock 1.0.4
%global x11perf 1.6.0
%global xclipboard 1.1.3
%global xclock 1.0.9
%global xconsole 1.0.6
%global xcursorgen 1.0.6
%global xeyes 1.1.2
%global xfd 1.1.2
%global xfontsel 1.0.6
%global xload 1.1.3
%global xlogo 1.0.4
%global xmag 1.0.6
%global xmessage 1.0.5
%global xpr 1.0.5
%global xvidtune 1.0.3
%global xwd 1.0.7
%global xwud 1.0.5

Summary:        X.Org X11 applications
Name:           xorg-x11-apps
Version:        7.7
Release:        29%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.x.org
Source0:        https://www.x.org/pub/individual/app/oclock-%{oclock}.tar.bz2
Source1:        https://www.x.org/pub/individual/app/x11perf-%{x11perf}.tar.bz2
Source2:        https://www.x.org/pub/individual/app/xclipboard-%{xclipboard}.tar.bz2
Source3:        https://www.x.org/pub/individual/app/xclock-%{xclock}.tar.bz2
Source4:        https://www.x.org/pub/individual/app/xconsole-%{xconsole}.tar.bz2
Source5:        https://www.x.org/pub/individual/app/xcursorgen-%{xcursorgen}.tar.bz2
Source6:        https://www.x.org/pub/individual/app/xeyes-%{xeyes}.tar.bz2
Source7:        https://www.x.org/pub/individual/app/xfd-%{xfd}.tar.bz2
Source8:        https://www.x.org/pub/individual/app/xfontsel-%{xfontsel}.tar.bz2
Source9:        https://www.x.org/pub/individual/app/xload-%{xload}.tar.bz2
Source10:       https://www.x.org/pub/individual/app/xlogo-%{xlogo}.tar.bz2
Source11:       https://www.x.org/pub/individual/app/xmag-%{xmag}.tar.bz2
Source12:       https://www.x.org/pub/individual/app/xmessage-%{xmessage}.tar.bz2
Source13:       https://www.x.org/pub/individual/app/xpr-%{xpr}.tar.bz2
Source14:       https://www.x.org/pub/individual/app/xvidtune-%{xvidtune}.tar.bz2
Source15:       https://www.x.org/pub/individual/app/xwd-%{xwd}.tar.bz2
Source16:       https://www.x.org/pub/individual/app/xwud-%{xwud}.tar.bz2

Patch0:         x11perf-1.6.0-x11perf-datadir-cleanups.patch

BuildRequires:  gettext
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(fontenc)
BuildRequires:  libpng-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xaw7)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xorg-macros) >= 1.8
BuildRequires:  pkgconfig(xrender) >= 0.4
BuildRequires:  pkgconfig(xt) >= 1.1
BuildRequires:  pkgconfig(xxf86vm)

Provides:       oclock = %{oclock}
Provides:       x11perf = %{x11perf}
Provides:       xclipboard = %{xclipboard}
Provides:       xclock = %{xclock}
Provides:       xconsole = %{xconsole}
Provides:       xcursorgen = %{xcursorgen}
Provides:       xeyes = %{xeyes}
Provides:       xfd = %{xfd}
Provides:       xfontsel = %{xfontsel}
Provides:       xload = %{xload}
Provides:       xlogo = %{xlogo}
Provides:       xmag = %{xmag}
Provides:       xmessage = %{xmessage}
Provides:       xpr = %{xpr}
Provides:       xvidtune = %{xvidtune}
Provides:       xwd = %{xwd}
Provides:       xwud = %{xwud}

%description
A collection of common X Window System applications.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -a15 -a16
%patch0  -b .x11perf-datadir-cleanup

%build
# Build all apps
{
for app in * ; do
    pushd $app
        autoreconf -v --install
        %configure
        make %{?_smp_mflags}
    popd
done
}

%install
# Install all apps
{
    for app in * ; do
        pushd $app
            %make_install
        popd
    done
}

# Removing documentation
rm -r %{buildroot}%{_mandir}/man1

%files
%{_bindir}/oclock
%{_bindir}/x11perf
%{_bindir}/x11perfcomp
%{_bindir}/xclipboard
%{_bindir}/xclock
%{_bindir}/xconsole
%{_bindir}/xcursorgen
%{_bindir}/xcutsel
%{_bindir}/xdpr
%{_bindir}/xeyes
%{_bindir}/xfd
%{_bindir}/xfontsel
%{_bindir}/xload
%{_bindir}/xlogo
%{_bindir}/xmag
%{_bindir}/xmessage
%{_bindir}/xpr
%{_bindir}/xvidtune
%{_bindir}/xwd
%{_bindir}/xwud
%{_datadir}/X11/app-defaults/Clock-color
%{_datadir}/X11/app-defaults/XClipboard
%{_datadir}/X11/app-defaults/XClock
%{_datadir}/X11/app-defaults/XClock-color
%{_datadir}/X11/app-defaults/XConsole
%{_datadir}/X11/app-defaults/Xfd
%{_datadir}/X11/app-defaults/XFontSel
%{_datadir}/X11/app-defaults/XLoad
%{_datadir}/X11/app-defaults/XLogo
%{_datadir}/X11/app-defaults/XLogo-color
%{_datadir}/X11/app-defaults/Xmag
%{_datadir}/X11/app-defaults/Xmessage
%{_datadir}/X11/app-defaults/Xmessage-color
%{_datadir}/X11/app-defaults/Xvidtune
%{_datadir}/X11/x11perfcomp

%changelog
* Mon Jan 18 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.7-29
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified.
- Removed 'luit' to drop run-time dependency on 'xorg-x11-fonts-misc' not present in CBL-Mariner.
- Removed 'xbiff' to drop run-time dependency on 'xbitmaps' not present in CBL-Mariner.
- Removed documentation.
- Switched "pkgconfig(libpng)" BR to "libpng-devel" due to CBL-Mariner's misconfiguration.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Adam Jackson <ajax@redhat.com> - 7.7-25
- xbiff 1.0.4
- xclock 1.0.9

* Wed Feb 13 2019 Dave Airlie <airlied@redhat.com - 7.7-24
- Rebuilt for rebuild of rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Adam Jackson <ajax@redhat.com> - 7.7-21
- oclock 1.0.4
- xeyes 1.1.2
- xfontsel 1.0.6
- xload 1.1.3
- xmessage 1.0.5
- xpr 1.0.5
- xwd 1.0.7
- xwud 1.0.5

* Thu Mar 01 2018 Adam Jackson <ajax@redhat.com> - 7.7-20
- Change URLs to https

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 30 2015 Simone Caronni <negativo17@gmail.com> - 7.7-13
- x11perf 1.6.0
- xmag 1.0.6

* Tue Nov 04 2014 Simone Caronni <negativo17@gmail.com> - 7.7-12
- Clean up SPEC file, fix rpmlint warnings.
- Simplify build requirements.
- Xprint has been removed everywhere.
- xclipboard 1.1.3
- xclock 1.0.7
- xconsole 1.0.6
- xfd 1.1.2
- xfontsel 1.0.5
- xload 1.1.2
- xwd 1.0.6
- xwud 1.0.4

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 19 2014 Hans de Goede <hdegoede@redhat.com> - 7.7-10
- Add Requires: xorg-x11-fonts-misc (rhbz#1046341)

* Wed Jul  9 2014 Hans de Goede <hdegoede@redhat.com> - 7.7-9
- xcursorgen 1.0.6

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.7-6
- Require xorg-x11-xbitmaps for xbiff (#474258)
- fix rpmlint complaints
- update sources to http sources, ftp fails too often

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.7-4
- upload xfontsel tarball, drop duplicate xlogo sources

* Mon Jan 14 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.7-3
- luit 1.1.1
- oclock 1.0.3
- xclock 1.0.6
- xbiff 1.0.3
- xpr 1.0.4
- xcursorgen 1.0.5
- xclipboard 1.1.2
- xfontsel 1.0.4
- xfd 1.1.1
- xlogo 1.0.4
- xvidtune 1.0.3

* Mon Jan 14 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.7-2
- xconsole 1.0.5
- xmessage 1.0.4
- xmag 1.0.5

* Thu Jan 03 2013 Adam Jackson <ajax@redhat.com> 7.7-1
- Superstition bump to 7.7
- Drop old streams patch

* Wed Sep 12 2012 Dave Airlie <airlied@redhat.com> 7.6-7
- x11perf 1.5.4 - fixes CVE-2011-2504

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Adam Jackson <ajax@redhat.com> 7.6-4
- Move xinput and xkill to xorg-x11-server-utils

* Mon Nov 07 2011 Adam Jackson <ajax@redhat.com> 7.6-3
- Rebuild for libpng 1.5

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Adam Jackson <ajax@redhat.com> 7.6-1
- x11perf 1.5.3
