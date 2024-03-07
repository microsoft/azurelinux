%global debug_package %{nil}
# When releasing a xorg-x11-proto-devel version with updated keysyms,
# rebuild libX11
Summary:        X.Org X11 Protocol headers
Name:           xorg-x11-proto-devel
Version:        2023.2
Release:        1%{?dist}
License:        MIT AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.x.org
Source0:        https://www.x.org/pub/individual/proto/xorgproto-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  xorg-x11-util-macros

%description
X.Org X11 Protocol headers

%prep
%autosetup -n xorgproto-%{version}

%build
autoreconf -f -i -v
%configure --disable-specs
make %{?_smp_mflags}


%install
%make_install

# trim some fat
for i in apple windows trap ; do
    rm -f %{buildroot}%{_includedir}/X11/extensions/*${i}*
    rm -f %{buildroot}%{_datadir}/pkgconfig/*${i}*
done

# keep things building even if you have the html doc tools for xmlto installed
rm -f %{buildroot}%{_docdir}/*/*.{html,svg}

%files
%license COPYING-*
%doc *.txt
%dir %{_includedir}/GL
%{_includedir}/GL/glxint.h
%{_includedir}/GL/glxmd.h
%{_includedir}/GL/glxproto.h
%{_includedir}/GL/glxtokens.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/glcore.h
%dir %{_includedir}/X11
%{_includedir}/X11/DECkeysym.h
%{_includedir}/X11/HPkeysym.h
%{_includedir}/X11/Sunkeysym.h
%{_includedir}/X11/X.h
%{_includedir}/X11/XF86keysym.h
%{_includedir}/X11/XWDFile.h
%{_includedir}/X11/Xalloca.h
%{_includedir}/X11/Xarch.h
%{_includedir}/X11/Xatom.h
%{_includedir}/X11/Xdefs.h
%{_includedir}/X11/Xfuncproto.h
%{_includedir}/X11/Xfuncs.h
%{_includedir}/X11/Xmd.h
%{_includedir}/X11/Xos.h
%{_includedir}/X11/Xos_r.h
%{_includedir}/X11/Xosdefs.h
%{_includedir}/X11/Xpoll.h
%{_includedir}/X11/Xproto.h
%{_includedir}/X11/Xprotostr.h
%{_includedir}/X11/Xthreads.h
%{_includedir}/X11/Xw32defs.h
%{_includedir}/X11/Xwindows.h
%{_includedir}/X11/Xwinsock.h
%{_includedir}/X11/ap_keysym.h
%dir %{_includedir}/X11/dri
%{_includedir}/X11/dri/xf86dri.h
%{_includedir}/X11/dri/xf86driproto.h
%{_includedir}/X11/dri/xf86dristr.h
%dir %{_includedir}/X11/extensions
%{_includedir}/X11/extensions/EVI.h
%{_includedir}/X11/extensions/EVIproto.h
%{_includedir}/X11/extensions/XI.h
%{_includedir}/X11/extensions/XI2.h
%{_includedir}/X11/extensions/XI2proto.h
%{_includedir}/X11/extensions/XIproto.h
%{_includedir}/X11/extensions/XKB.h
%{_includedir}/X11/extensions/XKBproto.h
%{_includedir}/X11/extensions/XKBsrv.h
%{_includedir}/X11/extensions/XKBstr.h
%{_includedir}/X11/extensions/XResproto.h
%{_includedir}/X11/extensions/Xv.h
%{_includedir}/X11/extensions/XvMC.h
%{_includedir}/X11/extensions/XvMCproto.h
%{_includedir}/X11/extensions/Xvproto.h
%{_includedir}/X11/extensions/ag.h
%{_includedir}/X11/extensions/agproto.h
%{_includedir}/X11/extensions/bigreqsproto.h
%{_includedir}/X11/extensions/bigreqstr.h
%{_includedir}/X11/extensions/composite.h
%{_includedir}/X11/extensions/compositeproto.h
%{_includedir}/X11/extensions/cup.h
%{_includedir}/X11/extensions/cupproto.h
%{_includedir}/X11/extensions/damageproto.h
%{_includedir}/X11/extensions/damagewire.h
%{_includedir}/X11/extensions/dbe.h
%{_includedir}/X11/extensions/dbeproto.h
%{_includedir}/X11/extensions/dmx.h
%{_includedir}/X11/extensions/dmxproto.h
%{_includedir}/X11/extensions/dpmsconst.h
%{_includedir}/X11/extensions/dpmsproto.h
%{_includedir}/X11/extensions/dri2proto.h
%{_includedir}/X11/extensions/dri2tokens.h
%{_includedir}/X11/extensions/dri3proto.h
%{_includedir}/X11/extensions/ge.h
%{_includedir}/X11/extensions/geproto.h
%{_includedir}/X11/extensions/lbx.h
%{_includedir}/X11/extensions/lbxproto.h
%{_includedir}/X11/extensions/mitmiscconst.h
%{_includedir}/X11/extensions/mitmiscproto.h
%{_includedir}/X11/extensions/multibufconst.h
%{_includedir}/X11/extensions/multibufproto.h
%{_includedir}/X11/extensions/panoramiXproto.h
%{_includedir}/X11/extensions/presentproto.h
%{_includedir}/X11/extensions/presenttokens.h
%{_includedir}/X11/extensions/randr.h
%{_includedir}/X11/extensions/randrproto.h
%{_includedir}/X11/extensions/recordconst.h
%{_includedir}/X11/extensions/recordproto.h
%{_includedir}/X11/extensions/recordstr.h
%{_includedir}/X11/extensions/render.h
%{_includedir}/X11/extensions/renderproto.h
%{_includedir}/X11/extensions/saver.h
%{_includedir}/X11/extensions/saverproto.h
%{_includedir}/X11/extensions/secur.h
%{_includedir}/X11/extensions/securproto.h
%{_includedir}/X11/extensions/shapeconst.h
%{_includedir}/X11/extensions/shapeproto.h
%{_includedir}/X11/extensions/shapestr.h
%{_includedir}/X11/extensions/shm.h
%{_includedir}/X11/extensions/shmproto.h
%{_includedir}/X11/extensions/shmstr.h
%{_includedir}/X11/extensions/syncconst.h
%{_includedir}/X11/extensions/syncproto.h
%{_includedir}/X11/extensions/syncstr.h
%{_includedir}/X11/extensions/xcmiscproto.h
%{_includedir}/X11/extensions/xcmiscstr.h
%{_includedir}/X11/extensions/xf86bigfont.h
%{_includedir}/X11/extensions/xf86bigfproto.h
%{_includedir}/X11/extensions/xf86bigfstr.h
%{_includedir}/X11/extensions/xf86dga.h
%{_includedir}/X11/extensions/xf86dga1const.h
%{_includedir}/X11/extensions/xf86dga1proto.h
%{_includedir}/X11/extensions/xf86dga1str.h
%{_includedir}/X11/extensions/xf86dgaconst.h
%{_includedir}/X11/extensions/xf86dgaproto.h
%{_includedir}/X11/extensions/xf86dgastr.h
%{_includedir}/X11/extensions/xf86vm.h
%{_includedir}/X11/extensions/xf86vmproto.h
%{_includedir}/X11/extensions/xf86vmstr.h
%{_includedir}/X11/extensions/xfixesproto.h
%{_includedir}/X11/extensions/xfixeswire.h
%{_includedir}/X11/extensions/xtestconst.h
%{_includedir}/X11/extensions/xtestext1const.h
%{_includedir}/X11/extensions/xtestext1proto.h
%{_includedir}/X11/extensions/xtestproto.h
%{_includedir}/X11/extensions/xwaylandproto.h
%dir %{_includedir}/X11/fonts
%{_includedir}/X11/fonts/FS.h
%{_includedir}/X11/fonts/FSproto.h
%{_includedir}/X11/fonts/font.h
%{_includedir}/X11/fonts/fontproto.h
%{_includedir}/X11/fonts/fontstruct.h
%{_includedir}/X11/fonts/fsmasks.h
%{_includedir}/X11/keysym.h
%{_includedir}/X11/keysymdef.h
%{_datadir}/pkgconfig/bigreqsproto.pc
%{_datadir}/pkgconfig/compositeproto.pc
%{_datadir}/pkgconfig/damageproto.pc
%{_datadir}/pkgconfig/dmxproto.pc
%{_datadir}/pkgconfig/dpmsproto.pc
%{_datadir}/pkgconfig/dri2proto.pc
%{_datadir}/pkgconfig/dri3proto.pc
%{_datadir}/pkgconfig/fixesproto.pc
%{_datadir}/pkgconfig/fontsproto.pc
%{_datadir}/pkgconfig/glproto.pc
%{_datadir}/pkgconfig/inputproto.pc
%{_datadir}/pkgconfig/kbproto.pc
%{_datadir}/pkgconfig/presentproto.pc
%{_datadir}/pkgconfig/randrproto.pc
%{_datadir}/pkgconfig/recordproto.pc
%{_datadir}/pkgconfig/renderproto.pc
%{_datadir}/pkgconfig/resourceproto.pc
%{_datadir}/pkgconfig/scrnsaverproto.pc
%{_datadir}/pkgconfig/videoproto.pc
%{_datadir}/pkgconfig/xcmiscproto.pc
%{_datadir}/pkgconfig/xextproto.pc
%{_datadir}/pkgconfig/xf86bigfontproto.pc
%{_datadir}/pkgconfig/xf86dgaproto.pc
%{_datadir}/pkgconfig/xf86driproto.pc
%{_datadir}/pkgconfig/xf86vidmodeproto.pc
%{_datadir}/pkgconfig/xineramaproto.pc
%{_datadir}/pkgconfig/xproto.pc
%{_datadir}/pkgconfig/xwaylandproto.pc
%{_docdir}/xorgproto/*

%changelog
* Mon Oct 23 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 2023.2-1
- Update to v2023.2

* Fri Apr 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 2019.1-6
- Remove explicit pkgconfig provides that are now automatically generated by RPM

* Thu Jan 07 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2019.1-5
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified.
- Added explicit "Provides" for 26 "pkgconfig(*)".

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 20 2019 Peter Hutterer <peter.hutterer@redhat.com> 2019.1-1
- xorgproto 2019.1
- drop files for xf86misc and proxy management proto, they're legacy now

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 Adam Jackson <ajax@redhat.com> - 2018.4-1
- xorgproto 2018.4

* Wed Feb 21 2018 Adam Jackson <ajax@redhat.com> - 2018.3-1
- xorgproto 2018.3

* Mon Feb 12 2018 Adam Jackson <ajax@redhat.com> - 2018.2-1
- xorgproto 2018.2

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Adam Jackson <ajax@redhat.com> - 2018.1-1
- Switch to merged protocol headers
- Drop evie headers
- Pre-F18 changelog trim

* Tue Nov 07 2017 Adam Jackson <ajax@redhat.com> - 7.7-24
- Drop bootstrap hack (that had been enabled for like nine years anyway)
- Use https URLs

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Hans de Goede <hdegoede@redhat.com> - 7.7-22
- Add xproto patches from upstream adding XF86Keyboard and XF86RFKill keysyms

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 26 2016 Adam Jackson <ajax@redhat.com> - 7.7-20
- xproto 7.0.31

* Mon Apr 04 2016 Peter Hutterer <peter.hutterer@redhat.com> 7.7-19
- inputproto 2.3.2

* Fri Mar 11 2016 Adam Jackson <ajax@redhat.com> 7.7-18
- videoproto 2.3.3

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Wed Jul 01 2015 Adam Jackson <ajax@redhat.com> 7.7-16
- xproto 7.0.28

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Dave Airlie <airlied@redhat.com> 7.7-14
- randrproto-1.5.0

* Wed Apr 01 2015 Dave Airlie <airlied@redhat.com> 7.7-13
- randrproto-1.4.1

* Thu Jun 12 2014 Hans de Goede <hdegoede@redhat.com> - 7.7-12
- inputproto-2.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Hans de Goede <hdegoede@redhat.com> - 7.7-10
- fontsproto-2.1.3
- videoproto-2.3.2
- xextproto-7.3.0
- xproto-7.0.26
- Cherry pick some unreleased fixes from upstream git

* Thu Jan 23 2014 Adam Jackson <ajax@redhat.com> 7.7-9
- Backport pointer-to-void* changes

* Tue Dec 10 2013 Adam Jackson <ajax@redhat.com> 7.7-8
- glproto 1.4.17

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> 7.7-7
- presentproto 1.0
- dri3proto 1.0
- xextproto 7.2.99.901

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 02 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.7-5
- xproto 7.0.24

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 7.7-4
- autoreconf for aarch64

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> 7.7-3
- inputproto 2.3

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 08 2013 Adam Jackson <ajax@redhat.com> 7.7-1
- inputproto 2.2.99.1

* Thu Jul 26 2012 Peter Hutterer <peter.hutterer@redhat.com> 7.6-24
- bigregsproto 1.1.2
- compositeproto 0.4.2
- damageproto 1.2.1
- fontsproto 2.1.2
- inputproto 2.2
- kbproto 1.0.6
- recordproto 1.14.2
- scrnsaverproto 1.2.2
- xcmiscproto 1.2.2
- xextproto 7.2.1

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
