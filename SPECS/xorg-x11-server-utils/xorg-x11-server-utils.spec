# doesn't work yet, needs more nickle bindings
%global with_xkeystone 0
# Component versions
%global iceauth 1.0.8
%global rgb 1.0.6
%global sessreg 1.1.0
%global xgamma 1.0.6
%global xhost 1.0.7
%global xinput 1.6.3
%global xkill 1.0.5
%global xmodmap 1.0.9
%global xrandr 1.5.0
%global xrdb 1.1.1
%global xrefresh 1.0.6
%global xset 1.2.4
%global xsetpointer 1.0.1
%global xsetroot 1.1.2
%global xstdcmap 1.0.3
%global xisxwayland 1
Summary:        X.Org X11 X server utilities
Name:           xorg-x11-server-utils
Version:        7.7
Release:        37%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.x.org
Source0:        https://www.x.org/pub/individual/app/iceauth-%{iceauth}.tar.bz2
Source1:        https://www.x.org/pub/individual/app/rgb-%{rgb}.tar.bz2
Source2:        https://www.x.org/pub/individual/app/sessreg-%{sessreg}.tar.bz2
Source3:        https://www.x.org/pub/individual/app/xgamma-%{xgamma}.tar.bz2
Source4:        https://www.x.org/pub/individual/app/xhost-%{xhost}.tar.bz2
Source5:        https://www.x.org/pub/individual/app/xinput-%{xinput}.tar.bz2
Source6:        https://www.x.org/pub/individual/app/xkill-%{xkill}.tar.bz2
Source7:        https://www.x.org/pub/individual/app/xmodmap-%{xmodmap}.tar.bz2
Source8:        https://www.x.org/pub/individual/app/xrandr-%{xrandr}.tar.bz2
Source9:        https://www.x.org/pub/individual/app/xrdb-%{xrdb}.tar.bz2
Source10:       https://www.x.org/pub/individual/app/xrefresh-%{xrefresh}.tar.bz2
Source11:       https://www.x.org/pub/individual/app/xset-%{xset}.tar.bz2
Source13:       https://www.x.org/pub/individual/app/xsetpointer-%{xsetpointer}.tar.bz2
Source14:       https://www.x.org/pub/individual/app/xsetroot-%{xsetroot}.tar.bz2
Source15:       https://www.x.org/pub/individual/app/xstdcmap-%{xstdcmap}.tar.bz2
Source16:       https://www.x.org/pub/individual/app/xisxwayland-%{xisxwayland}.tar.xz
Patch0:         sessreg-1.1.0-get-rid-of-sed.patch
Patch2:         0001-sessreg-Replace-strncpy-calls-with-a-sane-version-that-alway.patch
Patch3:         0001-xrandr-suppress-misleading-indentation-warning.patch
Patch4:         0001-xrandr-init-the-name-to-0.patch
BuildRequires:  libtool
BuildRequires:  meson
BuildRequires:  pkg-config
BuildRequires:  xorg-x11-util-macros
BuildRequires:  pkgconfig(xbitmaps)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xtrans)
BuildRequires:  pkgconfig(xxf86vm)
# xrdb, sigh
Requires:       mcpp
Provides:       iceauth = %{iceauth}
Provides:       sessreg = %{sessreg}
Provides:       xgamma = %{xgamma}
Provides:       xhost = %{xhost}
Provides:       xinput = %{xinput}
Provides:       xkill = %{xkill}
Provides:       xmodmap = %{xmodmap}
Provides:       xrandr = %{xrandr}
Provides:       xrdb = %{xrdb}
Provides:       xrefresh = %{xrefresh}
Provides:       xset = %{xset}
Provides:       xsetpointer = %{xsetpointer}
Provides:       xsetroot = %{xsetroot}
Provides:       xstdcmap = %{xstdcmap}

%description
A collection of utilities used to tweak and query the runtime configuration of
the X server.

%package -n     rgb
Summary:        X color name database
Version:        %{rgb}
# rgb subpackaged from xorg-x11-server-utils-7.7-33.fc32, bug #1268295
Conflicts:      xorg-x11-server-utils < 7.7-33

%description -n rgb
This package includes both a list mapping X color names to RGB values
(rgb.txt) and an showrgb program to convert the text file into the source
format.

%if %{with_xkeystone}
%package -n     xkeystone
Summary:        X display keystone correction
Requires:       nickle

%description -n xkeystone
Utility to perform keystone adjustments on X screens.
%endif

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a13 -a14 -a15 -a16
%patch0
pushd sessreg-%{sessreg}
%patch2 -p1
popd
pushd xrandr-%{xrandr}
%patch3 -p1
%patch4 -p1
popd

%build

# Build all apps
{
   for app in * ; do
      pushd $app
      case $app in
         xrdb-*)
            autoreconf -vif
            %configure --disable-silent-rules --with-cpp=%{_bindir}/mcpp
            make %{?_smp_mflags}
            ;;
         xisxwayland-*)
            %meson
            %meson_build
            ;;
         *)
            autoreconf -vif
            %configure --disable-silent-rules
            make %{?_smp_mflags}
            ;;
      esac

      popd
   done
}

%install
# Install all apps
{
   for app in * ; do
      pushd $app
      case $app in
         xisxwayland-*)
            %meson_install
            ;;
         *)
            %make_install
            ;;
      esac
      popd
   done
}
%if !%{with_xkeystone}
rm -f %{buildroot}%{_bindir}/xkeystone
%endif

%files
# All licenses are MIT- packaging just one, since they all match
%license iceauth-%{iceauth}/COPYING
%{_bindir}/iceauth
%{_bindir}/sessreg
%{_bindir}/xgamma
%{_bindir}/xhost
%{_bindir}/xinput
%{_bindir}/xisxwayland
%{_bindir}/xkill
%{_bindir}/xmodmap
%{_bindir}/xrandr
%{_bindir}/xrdb
%{_bindir}/xrefresh
%{_bindir}/xset
%{_bindir}/xsetpointer
%{_bindir}/xsetroot
%{_bindir}/xstdcmap
%{_mandir}/man1/iceauth.1*
%{_mandir}/man1/sessreg.1*
%{_mandir}/man1/xgamma.1*
%{_mandir}/man1/xhost.1*
%{_mandir}/man1/xinput.1*
%{_mandir}/man1/xisxwayland.1*
%{_mandir}/man1/xkill.1*
%{_mandir}/man1/xmodmap.1*
%{_mandir}/man1/xrandr.1*
%{_mandir}/man1/xrdb.1*
%{_mandir}/man1/xrefresh.1*
%{_mandir}/man1/xset.1*
%{_mandir}/man1/xsetpointer.1*
%{_mandir}/man1/xsetroot.1*
%{_mandir}/man1/xstdcmap.1*

%files -n rgb
%license rgb-%{rgb}/COPYING
%{_bindir}/showrgb
%{_datadir}/X11/rgb.txt
%{_mandir}/man1/showrgb.1*

%if %{with_xkeystone}
%files -n xkeystone
%{_bindir}/xkeystone
%endif

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 7.7-37
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.7-36
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue May 19 2020 Peter Hutterer <peter.hutterer@redhat.com> 7.7-35
- xisxwayland 1

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Petr Pisar <ppisar@redhat.com> - 7.7-33
- Subpackage rgb (bug #1268295)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Peter Hutterer <peter.hutterer@redhat.com> 7.7-31
- xinput 1.6.3

* Thu Jun 20 2019 Adam Jackson <ajax@redhat.com> - 7.7-30
- Drop BuildRequires: pkgconfig(xxf86misc), X servers haven't implemented that
  extension in 10+ years.

* Thu Mar 21 2019 Adam Jackson <ajax@redhat.com> - 7.7-29
- Rebuild for xtrans 1.4.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 12 2018 Peter Hutterer <peter.hutterer@redhat.com> 7.7-27
- Fix a bunch of coverity warnings
- disable silent rules

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Adam Jackson <ajax@redhat.com> - 7.7-25
- iceauth 1.0.8
- xkill 1.0.5
- xrdb 1.1.1
- xrefresh 1.0.6
- xset 1.2.4
- xsetroot 1.1.2
- HTTPS URLs

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 26 2016 Peter Hutterer <peter.hutterer@redhat.com> 7.7-20
- Drop xsetmode. It's been broken for years

* Tue Feb 23 2016 Simone Caronni <negativo17@gmail.com> - 7.7-19
- xrandr 1.5.0

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Tue Oct 20 2015 Peter Hutterer <peter.hutterer@redhat.com> 7.7-17
- xinput 1.6.2

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 01 2015 Simone Caronni <negativo17@gmail.com> - 7.7-15
- xgamma 1.0.6
- xhost 1.0.7

* Thu Apr 30 2015 Simone Caronni <negativo17@gmail.com> - 7.7-14
- xmodmap 1.0.9
- Fix FTBFS Fedora 22 on sessreg.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 7.7-13
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Jan 20 2015 Simone Caronni <negativo17@gmail.com> - 7.7-12
- Update sessreg to 1.1.0.

* Sat Jan 17 2015 Simone Caronni <negativo17@gmail.com> - 7.7-11
- Update iceauth to 1.0.7.

* Mon Nov 10 2014 Simone Caronni <negativo17@gmail.com> - 7.7-10
- rgb 1.0.6

* Thu Oct 23 2014 Simone Caronni <negativo17@gmail.com> - 7.7-9
- Clean up SPEC file, fix rpmlint warnings.

* Wed Oct 01 2014 Adam Jackson <ajax@redhat.com> 7.7-8
- xrandr 1.4.3

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 Simone Caronni <negativo17@gmail.com> 7.7-6
- iceauth 1.0.6
- xhost 1.0.6
- xrandr 1.4.2
- xrefresh 1.0.5
- xset 1.2.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 16 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.7-4
- xinput 1.6.1

* Mon Sep 09 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.7-3
- xmodmap 1.0.8
- xkill 1.0.4
- xrdb 1.1.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Adam Jackson <ajax@redhat.com> 7.7-1
- rgb 1.0.5
- xsessreg 1.0.8
- xgamma 1.0.5
- xhost 1.0.5
- xmodmap 1.0.7
- xsetroot 1.1.1
- xstdcmap 1.0.3

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 7.5-17
- autoconf for aarch64

* Wed Feb 13 2013 Benjamin Tissoires <benjamin.tissoires@redhat.com> 7.5-16
- xrandr 1.4.0

* Wed Jan 30 2013 Adam Jackson <ajax@redhat.com> 7.5-15
- Print primary output in xrandr

* Wed Nov 14 2012 Adam Jackson <ajax@redhat.com> 7.5-14
- xinput 1.6.0

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Peter Hutterer <peter.hutterer@redhat.com> 7.5-12
- Add libXinerama-devel requires for new xinput

* Tue Apr 17 2012 Peter Hutterer <peter.hutterer@redhat.com> 7.5-11
- xinput 1.5.99.901

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Peter Hutterer <peter.hutterer@redhat.com> 7.5-9
- xinput 1.5.4

* Thu Nov 10 2011 Adam Jackson <ajax@redhat.com> 7.5-8
- Move xinput and xkill here from xorg-x11-apps

* Mon Oct 10 2011 Matěj Cepl <mcepl@redhat.com> - 7.5-7
- Fix BuildRequires ... xbitmaps-devel does not exist anymore (RHBZ #744751)
- Upgrade to the latest upstream iceauth, rgb, sessreg, and xrandr
