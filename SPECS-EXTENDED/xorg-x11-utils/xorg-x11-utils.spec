Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Component versions
%global xdpyinfo 1.3.2
%global xev 1.2.2
%global xlsatoms 1.1.2
%global xlsclients 1.1.4
%global xlsfonts 1.0.6
%global xprop 1.2.3
%global xvinfo 1.1.3
%global xwininfo 1.1.5

Summary:    X.Org X11 X client utilities
Name:       xorg-x11-utils
Version:    7.5
Release:    35%{?dist}
License:    MIT
URL:        https://www.x.org

Source0:    https://www.x.org/pub/individual/app/xdpyinfo-%{xdpyinfo}.tar.bz2
Source1:    https://www.x.org/pub/individual/app/xev-%{xev}.tar.bz2
Source2:    https://www.x.org/pub/individual/app/xlsatoms-%{xlsatoms}.tar.bz2
Source3:    https://www.x.org/pub/individual/app/xlsclients-%{xlsclients}.tar.bz2
Source4:    https://www.x.org/pub/individual/app/xlsfonts-%{xlsfonts}.tar.bz2
Source5:    https://www.x.org/pub/individual/app/xprop-%{xprop}.tar.bz2
Source6:    https://www.x.org/pub/individual/app/xvinfo-%{xvinfo}.tar.bz2
Source7:    https://www.x.org/pub/individual/app/xwininfo-%{xwininfo}.tar.bz2

BuildRequires:  gettext-devel
BuildRequires:  libtool

BuildRequires:  pkgconfig(dmx)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb) >= 1.6
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xorg-macros) >= 1.8
BuildRequires:  pkgconfig(xrandr) >= 1.2
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(xxf86vm)

Provides:   edid-decode
Provides:   xdpyinfo = %{xdpyinfo}
Provides:   xev = %{xev}
Provides:   xlsatoms = %{xlsatoms}
Provides:   xlsclients = %{xlsclients}
Provides:   xlsfonts = %{xlsfonts}
Provides:   xprop = %{xprop}
Provides:   xvinfo = %{xvinfo}
Provides:   xwininfo = %{xwininfo}

%description
A collection of client utilities which can be used to query the X server for
various information.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4 -a5 -a6 -a7

%build
# Build all apps
{
    for app in * ; do
        pushd $app
        if [ -e configure ] ; then
            autoreconf -vif
            %configure
        else
            export CFLAGS="%{optflags}"
            export LDFLAGS="%{?__global_ldflags}"
        fi
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

%files
%{_bindir}/xdpyinfo
%{_bindir}/xev
%{_bindir}/xlsatoms
%{_bindir}/xlsclients
%{_bindir}/xlsfonts
%{_bindir}/xprop
%{_bindir}/xvinfo
%{_bindir}/xwininfo
%{_mandir}/man1/xdpyinfo.1*
%{_mandir}/man1/xev.1*
%{_mandir}/man1/xlsatoms.1*
%{_mandir}/man1/xlsclients.1*
%{_mandir}/man1/xlsfonts.1*
%{_mandir}/man1/xprop.1*
%{_mandir}/man1/xvinfo.1*
%{_mandir}/man1/xwininfo.1*

%changelog
* Fri Jul 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.5-35
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removing unused BR on 'pkgconfig(xxf86dga)'.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 26 2019 Adam Jackson <ajax@redhat.com> - 7.5-33
- Drop edid-decode since upstream has moved away from X.org

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Adam Jackson <ajax@redhat.com> - 7.5-32
- xwininfo 1.1.5

* Thu Jun 20 2019 Adam Jackson <ajax@redhat.com> - 7.5-31
- Drop BuildRequires: pkgconfig(xxf86misc), X servers haven't implemented that
  extension in 10+ years.

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Adam Jackson <ajax@redhat.com> - 7.5-28
- xlsclients 1.1.4
- xlsfonts 1.0.6
- xprop 1.2.3
- xwininfo 1.1.3
- HTTPS URLs

* Wed Mar 07 2018 Adam Jackson <ajax@redhat.com> - 7.5-27
- New edid-decode snapshot

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 11 2017 Adam Jackson <ajax@redhat.com> - 7.5-23
- new edid-decode snapshot

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 01 2015 Simone Caronni <negativo17@gmail.com> - 7.5-19
- xvinfo 1.1.3

* Thu Apr 30 2015 Simone Caronni <negativo17@gmail.com> - 7.5-18
- xlsfonts 1.0.5
- xlsatoms 1.1.2
- xev 1.2.2
- xdpyinfo 1.3.2
- Use git commit id for edid-decode-snapshot.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 7.5-17
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Nov 04 2014 Simone Caronni <negativo17@gmail.com> - 7.5-16
- Clean up SPEC file, fix rpmlint warnings.
- Update xslclients to 1.1.3.
- Simplify build requirements.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 29 2014 Adam Jackson <ajax@redhat.com> 7.5-13
- New edid-decode snapshot

* Fri Aug 09 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.5-12
- Update sources for latest tarballs, some changes got lost before the commit
- require gettext-devel for AM_ICONV (now required by xwininfo)

* Fri Aug 09 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.5-11
- xprop 1.2.2
- xwininfo 1.1.2
- xdpyinfo 1.3.1
- xvinfo 1.1.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 7.5-9
- autoreconf for aarch64

* Wed Jan 30 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.5-8
- xev 1.2.1
- xlsatoms 1.1.1
- xlsfonts 1.0.4
- xwininfo 1.1.2

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Adam Jackson <ajax@redhat.com> 7.5-5
- xlsclients 1.1.2
- Rebuild for new xcb-util

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com> 7.5-4
- xdpyinfo 1.3.0

* Mon Sep 12 2011 Adam Jackson <ajax@redhat.com> 7.5-3
- xprop 1.2.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
