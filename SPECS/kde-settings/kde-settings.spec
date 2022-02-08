
Summary:        Config files for kde
Name:           kde-settings
Version:        36.0
Release:        1%{?dist}
License:        MIT
Url:            https://pagure.io/fedora-kde/kde-settings
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pagure.io/fedora-kde/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        COPYING

BuildArch: noarch

BuildRequires: systemd

# when kdebugrc was moved here
Conflicts: kf5-kdelibs4support < 5.7.0-3

Obsoletes: kde-settings-ksplash < 24-2
Obsoletes: kde-settings-minimal < 24-3

# /etc/pam.d/ ownership
Requires: pam

%description
%{summary}.

%package -n qt-settings
Summary: Configuration files for Qt
# qt-graphicssystem.* scripts use lspci
%description -n qt-settings
%{summary}.


%prep
%setup -q

# omit crud
rm -fv Makefile


%build
# Intentionally left blank.  Nothing to see here.


%install
mkdir -p %{buildroot}{/usr/share/config,/etc/kde/kdm}

tar cpf - . | tar --directory %{buildroot} -xvpf -

if [ %{_prefix} != /usr ] ; then
   pushd %{buildroot}
   mv %{buildroot}/usr %{buildroot}%{_prefix}
   mv %{buildroot}/etc %{buildroot}%{_sysconfdir}
   popd
fi


cp -p %{SOURCE1} .

# omit kdm stuff
rm -rfv %{buildroot}%{_sysconfdir}/{kde/kdm,logrotate.d/kdm,pam.d/kdm*}
rm -fv %{buildroot}%{_localstatedir}/lib/kdm/backgroundrc
# we don't use %%{_tmpfilesdir} and %%{_unitdir} because they don't follow %{_prefix}
rm -fv %{buildroot}%{_prefix}/lib/tmpfiles.d/kdm.conf
rm -fv %{buildroot}%{_prefix}/lib/systemd/system/kdm.service

## unpackaged files
# formerly known as -minimal
rm -fv %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/20-kdedirs-minimal.sh
rm -fv %{buildroot}%{_sysconfdir}/profile.d/qt-graphicssystem.*

# Unpackaged for Mariner builds
rm -fv %{buildroot}%{_sysconfdir}/kde/env/fedora-bookmarks.sh
rm -fv %{buildroot}%{_datadir}/polkit-1/rules.d/11-fedora-kde-policy.rules
rm -rfv %{buildroot}%{_libdir}/rpm
rm -rfv %{buildroot}%{_datadir}/kde-settings/kde-profile

# Removed 'plasma' subpackage
rm -fv %{buildroot}%{_datadir}/plasma/shells/org.kde.plasma.desktop/contents/updates/00-start-here-2.js
rm -fv %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/env.sh
rm -fv %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/gtk2_rc_files.sh
rm -fv %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/gtk3_scrolling.sh
rm -fv %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/shutdown/kuiserver5.sh
rm -fv %{buildroot}%{_datadir}/plasma/look-and-feel/org.fedoraproject.fedora.desktop/contents/plasmoidsetupscripts/org.kde.plasma.kicker.js
rm -fv %{buildroot}%{_datadir}/plasma/look-and-feel/org.fedoraproject.fedora.desktop/contents/plasmoidsetupscripts/org.kde.plasma.kickerdash.js
rm -fv %{buildroot}%{_datadir}/plasma/look-and-feel/org.fedoraproject.fedora.desktop/contents/plasmoidsetupscripts/org.kde.plasma.kickoff.js

%files
%license COPYING
%config(noreplace) %{_sysconfdir}/profile.d/kde.*
%{_sysconfdir}/kde/env/env.sh
%{_sysconfdir}/kde/env/gpg-agent-startup.sh
%{_sysconfdir}/kde/shutdown/gpg-agent-shutdown.sh
%{_sysconfdir}/kde/env/gtk2_rc_files.sh
%config(noreplace) %{_sysconfdir}/xdg/kcm-about-distrorc
%config(noreplace) %{_sysconfdir}/xdg/kdebugrc
%config(noreplace) %{_sysconfdir}/pam.d/kcheckpass
%config(noreplace) %{_sysconfdir}/pam.d/kscreensaver
# drop noreplace, so we can be sure to get the new kiosk bits
%config %{_sysconfdir}/kderc
%config %{_sysconfdir}/kde4rc
%{_datadir}/applications/kde-mimeapps.list

%files -n qt-settings
%license COPYING
%config(noreplace) %{_sysconfdir}/Trolltech.conf


%changelog
* Tue Feb 08 2022 Cameron Baird <cameronbaird@microsoft.com> 36.0-1
- Update source to v36.0
- License verified

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 30.0-3
- Renaming Linux-PAM to pam

* Fri Apr 03 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 30.0-2
- Initial CBL-Mariner import from Fedora 30 (license: MIT).
- Removed 'fedora' and 'rhel' macro references.
- Removed Requires: 'kde-filesystem', 'xdg-user-dirs', 'breeze-icon-theme'.
- Removed BuildRequires: 'kde-filesystem'.
- Replaced Requires 'pam' with 'Linux-PAM'.
- Removed '%%package minimal', '%%package plasma' and '%%package pulseaudio', since they are not used.

* Thu Mar 14 2019 Rex Dieter <rdieter@fedoraproject.org> - 30.0-1
- 30.0 (#1688925)

* Thu Mar  7 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 29.0-4
- Remove obsolete requirement for %%post scriptlet

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 29.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 20 2018 Owen Taylor <otaylor@redhat.com> - 29.0-2
- Handle %%{_prefix} != /usr
- Fix double-listed files in %%{_datadir}/kde-settings/

* Thu Sep 13 2018 Rex Dieter <rdieter@fedoraproject.org> - 29.0-1
- 29.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Rex Dieter <rdieter@fedoraproject.org> - 28.0-2
- -plasma: Requires: f28-backgrounds-kde

* Mon Mar 12 2018 Rex Dieter <rdieter@fedoraproject.org> - 28.0-1
- Update for Fedora 28

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 27-1.3
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 27-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 25 2017 Troy Dawson <tdawson@redhat.com> - 27-1.1
- Cleanup spec file conditionals

* Thu Sep 21 2017 Jan Grulich <jgrulich@redhat.com> - 27-1
- Properly update for Fedora 27 (updated tarball)

* Wed Sep 20 2017 Jan Grulich <jgrulich@redhat.com> - 26-1.2
- Update for Fedora 27

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 26-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 26-1
- init kde-settings-26

* Thu Apr 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 25-6
- baloofilerc: drop explicit folders= key (use default set in kf5-baloo)

* Thu Mar 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 25-5.1
- drop Requires: polkit-js-engine

* Mon Mar 27 2017 Adam Williamson <awilliam@redhat.com> - 25-5
- Patch another thing needed to get correct F26 theme

* Mon Mar 27 2017 Adam Williamson <awilliam@redhat.com> - 25-4
- Bump to F26 backgrounds

* Wed Mar 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 25-3
- mimeapps: prefer plasma-discover (over apper)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 25-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 25-2
- init kde-settings-25

* Wed Jul 06 2016 Rex Dieter <rdieter@fedoraproject.org> - 24-7
- better start-here scriplet

* Tue Apr 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 24-6
- drop 00-start-here-kde-fedora-2.js

* Wed Mar 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 24-5
- plasmarc: Theme=F24
- drop remnants of -ksplash subpkg

* Tue Mar 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 24-4
- drop -kdm (superceded by kdm-settings subpkg of kde-workspace)
- ksmserverrc: disable session management

* Tue Mar 29 2016 Rex Dieter <rdieter@fedoraproject.org> 24-3.2
- -kdm: Requires: s/redhat-logos/system-logos/

* Thu Mar 24 2016 Rex Dieter <rdieter@fedoraproject.org> 24-3.1
- omit qt-graphicssystem.* shell hacks (#1306524)

* Mon Mar 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 24-3
- drop -minimal
- drop deprecated kde4 bits
- generic theming (for now)

* Sat Mar 12 2016 Rex Dieter <rdieter@fedoraproject.org> 24-1.3
- (re)enable -kdm (dropping needswork)

* Fri Mar 11 2016 Rex Dieter <rdieter@fedoraproject.org> 24-1.2
- drop -kdm, -ksplash

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 24-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Rex Dieter <rdieter@fedoraproject.org> 24-1
- init v24, kde-mimeapps.list: adjust to kf5 versions of ark, dragon, gwenview

* Thu Jan 07 2016 Rex Dieter <rdieter@fedoraproject.org> 23-10
- revert prior commit, use prefix/plasma/shells/<package>/contents/updates instead

* Mon Nov 16 2015 Rex Dieter <rdieter@fedoraproject.org> 23-9
- copy plasma update scripts to canonical $XDG_DATA_DIRS/plasma/shells/<package>/contents/updates
  (needed when plasma-5.5 lands)

* Sun Nov 08 2015 Rex Dieter <rdieter@fedoraproject.org> 23-8
- add kcm-about-distrorc (#1279221)

* Thu Oct 08 2015 Rex Dieter <rdieter@fedoraproject.org> 23-7
- workaround lingering kuiserver processes (kde#348123)

* Tue Oct 06 2015 Rex Dieter <rdieter@fedoraproject.org> 23-6
- restore gtk3 scrolling workaround (#1226465)

* Sat Oct 03 2015 Rex Dieter <rdieter@fedoraproject.org> 23-5
- baloofilerc: index only well-known document-centric dirs by default (#1235026)

* Mon Sep 21 2015 Rex Dieter <rdieter@fedoraproject.org> - 23-4
- support XDG_CONFIG_DIR (/usr/share/kde-settings/kde-profile/default/xdg)
- kcminputrc,kdeglobals,plasmarc: explicitly set theming elements

* Tue Sep 01 2015 Rex Dieter <rdieter@fedoraproject.org> 23-3
- kde-mimeapps.list: s/kde-dolphin.desktop/org.kde.dolphin.desktop/

* Wed Aug 26 2015 Rex Dieter <rdieter@fedoraproject.org> 23-2
- kde-mimeapps.list: add calligra words,sheets,stage, fix text/plain

* Wed Aug 26 2015 Rex Dieter <rdieter@fedoraproject.org> 23-1
- init for f23

* Tue Jun 16 2015 Rex Dieter <rdieter@fedoraproject.org> - 22-11
- env: set GDK_CORE_DEVICE_EVENTS=1 to workaround gtk3 scrolling issues (#1226465)
- env: omit gpg-agent management, no longer needed (#1229918)

* Wed May 20 2015 Rex Dieter <rdieter@fedoraproject.org> 22-10
- qt-settings: /etc/xdg/QtProject/qtlogging.ini

* Wed May 20 2015 Rex Dieter <rdieter@fedoraproject.org> 22-9
- qt-settings: qtlogging.ini: disable *.debug logging

* Wed May 20 2015 Rex Dieter <rdieter@fedoraproject.org> 22-8
- kcminputrc: explicitly set breeze_cursors theme default (#1199521)

* Wed May 13 2015 Jan Grulich <jgrulich@redhat.com> - 22-7
- update kickoff icon from working location

* Wed May 13 2015 Jan Grulich <jgrulich@redhat.com> - 22-6
- use fedora icon in kickoff

* Wed Apr 22 2015 Rex Dieter <rdieter@fedoraproject.org> 22-4
- kdmrc: fix kdm theme #1214323)

* Wed Apr 15 2015 Rex Dieter <rdieter@fedoraproject.org> - 22-3.1
- -plasma: move plasmarc plasma-workspace/{env,shutdown} here
- omit kde4 ksplashrc, plasmarc

* Tue Mar 10 2015 Rex Dieter <rdieter@fedoraproject.org> 22-3
- plasmarc: F22 theme default

* Mon Mar 09 2015 Rex Dieter <rdieter@fedoraproject.org> 22-2.2
- s/-plasma-desktoptheme/-plasma-theme/ for consistency

* Thu Mar 05 2015 Rex Dieter <rdieter@fedoraproject.org> 22-2.1
- Conflicts: kf5-kdelibs4support < 5.7.0-3 (#1199108)

* Tue Mar 03 2015 Rex Dieter <rdieter@fedoraproject.org> - 22-2
- kdeburc: disable debug output
- kdeglobals: use Sans/Monospace fonts, breeze widgets/icons
- default gtk config to adwaita (replaces oxygen-gtk)

* Sun Feb 08 2015 Rex Dieter <rdieter@fedoraproject.org> 22-1.1
- %%config(noreplace) /etc/xdg/kdeglobals

* Sun Feb 08 2015 Rex Dieter <rdieter@fedoraproject.org> 22-1
- init for f22/plasma5, needs more love

* Thu Jan 01 2015 Rex Dieter <rdieter@fedoraproject.org> 21-2
- kwalletrc: empty most of [Wallet] section
- fixes problems on initial wallet creation with pam_kwallet (#1177991)

* Tue Sep 02 2014 Rex Dieter <rdieter@fedoraproject.org> 21-1
- branch for f21 (and new theming)

* Wed Aug 06 2014 Rex Dieter <rdieter@fedoraproject.org> 20-17
- add kf5/plasma5 support (/etc/xdg/plasma-workspace)

* Thu Jul 03 2014 Rex Dieter <rdieter@fedoraproject.org> 20-16
- QT_PLUGIN_PATH contains repeated paths (#1115268)

* Wed Jul 02 2014 Rex Dieter <rdieter@fedoraproject.org> 20-15
- kwalletrc: disable autoclose

* Mon Jun 30 2014 Rex Dieter <rdieter@fedoraproject.org> 20-14
- baloo default config: index only well-known dirs (#1114216)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20-13.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Rex Dieter <rdieter@fedoraproject.org> 20-13
- /etc/pam.d/kdm: pam-kwallet support

* Tue Nov 26 2013 Rex Dieter <rdieter@fedoraproject.org> 20-12
- kwalletrc: [Auto Allow] kdewallet=+KDE Daemon

* Tue Nov 26 2013 Rex Dieter <rdieter@fedoraproject.org> 20-11
- kwalletrc: whitelist/trust a few well-known trusted apps by default

* Tue Nov 26 2013 Rex Dieter <rdieter@fedoraproject.org> 20-10
- kwalletrc: +Silently Create Initial Wallet=true

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 20-9
- plasma4.req: fix bogus self-auto-Requires being generated for script engines

* Tue Nov 19 2013 Rex Dieter <rdieter@fedoraproject.org> 20-8
- cleanup/fix gpg-agent startup/shutdown

* Fri Nov 08 2013 Rex Dieter <rdieter@fedoraproject.org> 20-7
- kdmrc: ServerAttempts=2,ServerTimeout=60 (#967521)

* Thu Nov 07 2013 Rex Dieter <rdieter@fedoraproject.org> 20-6
- kmixrc: VolumeFeedback=true
- kdmrc: ConfigVersion 2.4
- gpg-agent isn't started automatically with KDE anymore (#845492)

* Mon Oct 14 2013 Rex Dieter <rdieter@fedoraproject.org> 20-4
- drop -sddm

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 20-3.1
- -sddm: add/fix %%description, *really* own /var/run/sddm

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 20-3
- -sddm: create/own /var/run/sddm (#1010590)

* Mon Sep 16 2013 Martin Briza <mbriza@redhat.com> - 20-2
- typo in system-kde-theme version

* Mon Sep 16 2013 Martin Briza <mbriza@redhat.com> - 20-2
- sddm subpackage - added the config containing the Heisenbug artwork

* Tue Sep 10 2013 Jaroslav Reznik <jreznik@fedoraproject.org> - 20-1
- reset Version to match target fedora release (20)
- default to Heisenbug artwork

* Mon Jul 29 2013 Martin Briza <mbriza@redhat.com> - 19-23.1
- Fixed a typo in systemd_preun (#989145)

* Fri May 31 2013 Martin Briza <mbriza@redhat.com> - 19-23
- remove Console login menu option from KDM (#966095)

* Wed May 22 2013 Than Ngo <than@redhat.com> - 19-22
- disable java by default

* Tue May 21 2013 Rex Dieter <rdieter@fedoraproject.org> 19-21
- cleanup systemd macros
- kde-settings-kdm is misusing preset files (#963898)
- prune %%changelog

* Mon May 13 2013 Rex Dieter <rdieter@fedoraproject.org> 19-20
- plymouth-quit-wait service fails resulting in very long boot time (#921785)

* Wed Apr 24 2013 Martin Briza <mbriza@redhat.com> 19-19
- Return to the usual X server invocation in case there's no systemd provided wrapper

* Wed Apr 24 2013 Daniel Vrátil <dvratil@redhat.com> 19-18
- remove Mugshot from Konqueror bookmarks (#951279)

* Mon Apr 15 2013 Martin Briza <mbriza@redhat.com> 19-17.2
- so depending on /lib/systemd/systemd-multi-seat-x is considered a broken dependency - kdm depends on systemd instead

* Sat Apr 13 2013 Rex Dieter <rdieter@fedoraproject.org> 19-17.1
- use %%_tmpfilesdir macro

* Thu Apr 11 2013 Martin Briza <mbriza@redhat.com> 19-17
- Use /lib/systemd/systemd-multi-seat-x as the X server in KDM

* Wed Apr 03 2013 Martin Briza <mbriza@redhat.com> 19-16
- Fedora release number was wrong in /etc/kde/kdm/kdmrc

* Wed Apr 03 2013 Martin Briza <mbriza@redhat.com> 19-15
- Fixed KDM theme name in /etc

* Thu Mar 28 2013 Martin Briza <mbriza@redhat.com> 19-14
- Changed the strings in the settings to Schrödinger's Cat instead of Spherical Cow

* Mon Feb 04 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> 19-13.1
- Requires: polkit-js-engine

* Mon Jan 28 2013 Rex Dieter <rdieter@fedoraproject.org> 19-13
- +fedora-kde-display-handler kconf_update script

* Wed Dec 05 2012 Rex Dieter <rdieter@fedoraproject.org> 19-12
- plasma4.req: be more careful wrt IFS

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> 19-11
- plasma4.req: allow for > 1 scriptengine

* Tue Nov 27 2012 Dan Vratil <dvratil@redhat.com> 19-10
- provide kwin rules to fix maximization of some Gtk2 apps

* Sun Nov 11 2012 Rex Dieter <rdieter@fedoraproject.org> 19-9.1
- fixup kdmrc for upgraders who had UserAuthDir=/var/run/kdm

* Thu Nov 08 2012 Rex Dieter <rdieter@fedoraproject.org> 19-9
- tighten permissions on /var/run/kdm
- support /var/run/xdmctl

* Fri Oct 12 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 19-8
- kslideshow.kssrc: use xdg-user-dir instead of hardcoding $HOME/Pictures

* Fri Oct 12 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 19-7
- port 11-fedora-kde-policy from old pkla format to new polkit-1 rules (#829881)
- nepomukstrigirc: index translated xdg-user-dirs (dvratil, #861129)

* Thu Sep 27 2012 Dan Vratil <dvratil@redhat.com> 19-5
- fix indexing paths in nepomukstrigirc (#861129)

* Mon Sep 24 2012 Rex Dieter <rdieter@fedoraproject.org> 19-4
- -minimal subpkg

* Tue Sep 04 2012 Dan Vratil <dvratil@redhat.com> 19-3
- add 81-fedora-kdm-preset (#850775)
- start kdm.service after livesys-late.service

* Wed Aug 29 2012 Rex Dieter <rdieter@fedoraproject.org> - 19-1
- reset Version to match target fedora release (19)
- kdm.pam: pam_gnome_keyring.so should be loaded after pam_systemd.so (#852723)

* Tue Aug 21 2012 Martin Briza <mbriza@redhat.com> 4.9-5
- Change strings to Fedora 18 (Spherical Cow)
- bump system_kde_theme_ver to 17.91

* Sat Aug 11 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-2.1
- -kdm: drop old stuff, fix systemd scriptlets

* Thu Aug 09 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-2
- /etc/pam.d/kdm missing: -session optional pam_ck_connector.so (#847114)

* Wed Aug 08 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9-1
- adapt kdm for display manager rework feature (#846145)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8-16.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-16
- qt-graphicssystem.csh: fix typo s|/usr/bin/lspci|/usr/sbin/lspci| (#827440)

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-15.1
- kde-settings-kdm conflicts with gdm (#819254)

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-15
- qt-settings does NOT fully quallify path to lspci in /etc/profile.d/qt-graphicssystem.{csh,sh} (#827440)

* Fri May 25 2012 Than Ngo <than@redhat.com> - 4.8-14.1
- rhel/fedora condtion

* Wed May 16 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-14
- Pure Qt applications can't use KDE styles outside of KDE (#821062)

* Tue May 15 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-13
- kdmrc: GUIStyle=Plastique (#810161)

* Mon May 14 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-12
- drop hack/workaround for bug #750423
- move /etc/tmpfiles.d => /usr/lib/tmpfiles.d

* Thu May 10 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-10
- +qt-settings: move cirrus workaround(s) here (#810161)

* Wed May 09 2012 Than Ngo <than@redhat.com> - 4.8-8.2
- fix rhel condition

* Tue May 08 2012 Than Ngo <than@redhat.com> - 4.8-8.1
- add workaround for cirrus

* Mon Apr 30 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-8
- fix application/x-rpm mimetype defaults

* Wed Apr 18 2012 Than Ngo <than@redhat.com> - 4.8-7.1
- add rhel condition

* Mon Mar 19 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-7
- plasma4.prov: change spaces in runner names to underscores

* Tue Feb 28 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-6
- kslideshow.kssrc: include some sane/working defaults

* Tue Feb 14 2012 Jaroslav Reznik <jreznik@redhat.com> 4.8-5
- fix plasmarc Beefy Miracle reference

* Tue Feb 14 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-4
- kdmrc: GreetString=Fedora 17 (Beefy Miracle)
- kdmrc, ksplashrc, plasmarc: s/Verne/BeefyMiracle/g (for the artwork themes)
- bump system_kde_theme_ver to 16.91

* Mon Jan 16 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-3
- merge the plasma-rpm tarball into the SVN trunk and thus the main tarball

* Mon Jan 16 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-2
- allow org.kde.kcontrol.kcmclock.save without password for wheel again
- Requires: polkit (instead of polkit-desktop-policy)

* Mon Jan 16 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-1
- kwinrc: drop [Compositing] Enabled=false

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-14.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 19 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-14
- add explicit apper defaults
- add script to init $XDG_DATA_HOME (to workaround bug #750423)

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.4
- make new-subpkgs Requires: %%name for added safety

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.3
- -ksplash: Requires: system-ksplash-theme >= 15.90
- -plasma: Requires: system-plasma-desktoptheme >= 15.90

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.2
- -kdm: Requires: system-kdm-theme >= 15.90

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.1
- -kdm: Requires: verne-kdm-theme (#651305)

* Fri Oct 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13
- s/kpackagekit/apper/ configs
- drop gpg-agent scripts (autostarts on demand now)

* Sat Oct 15 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-12
- disable the default Plasma digital-clock's displayEvents option by default

* Wed Oct 12 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-11
- krunnerrc: org.kde.events_runnerEnabled=false
- follow Packaging:Tmpfiles.d guildelines

* Wed Oct 05 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-10
- don't spam syslog if pam-gnome-keyring is not present (#743044)

* Fri Sep 30 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-9
- -kdm: add explicit Requires: xorg-x11-xinit

* Tue Sep 27 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-8
- plasma4.prov: don't trust the Name of script engines, always use the API

* Thu Sep 22 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-7
- ship the Plasma RPM dependency generators only on F17+
- use xz tarball
- don't rm Makefile, no longer in the tarball
- set up a folder view on the desktop by default for new users (#740676)
- kdmrc: set MinShowUID=-1 (use /etc/login.defs) instead of 500 (#717115)
- -kdm: Requires: kdm >= 4.7.1-2 (required for MinShowUID=-1)

* Wed Aug 31 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-6
- put under the MIT license as agreed with the other contributors

* Sun Aug 21 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-5
- fix the RPM dependency generators to also accept ServiceTypes= (#732271)

* Sun Aug 21 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-4
- add the RPM dependency generators for Plasma (GSoC 2011), as Source1 for now

* Tue Aug 02 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7-3
- update to Verne theming/branding

* Wed Jul 13 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-2
- kmixrc: [Global] startkdeRestore=false

* Thu Mar 24 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-10
- konq webbrowsing profile: start.fedoraproject.org
- konq tabbedbrowsing : start.fedoraproject.org, fedoraproject.org/wiki/KDE

* Tue Mar 22 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.6-9
- Requires: polkit-desktop-policy

* Thu Mar 10 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-8
- s/QtCurve/oxygen-gtk/

* Mon Mar 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-7
- use adwaita-cursor-theme

* Mon Mar 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-6
- use lovelock-kdm-theme
- /var/log/kdm.log is never clean up (logrotate) (#682761)
- -kdm, move xterm dep to comps (#491251)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-4
- de-Laughlin-ize theming, be genericish/upstream (for now)
- kcminputrc: theme=dmz-aa, Requires: dmz-cursor-themes (#675509)

* Tue Feb 01 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-3
- add support for the postlogin PAM stack to kdm (#665060)

* Wed Dec 08 2010 Rex Dieter <rdieter@fedoraproject.org> 4.6-2.1
- %%post kdm : sed -e 's|-nr|-background none|' kdmrc (#659684)
- %%post kdm : drop old stuff

* Fri Dec 03 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6-2
- drop old Conflicts
- Xserver-1.10: Fatal server error: Unrecognized option: -nr (#659684)

* Mon Nov 29 2010 Rex Dieter <rdieter@fedoraproject.org> 4.6-1
- init 4.6
- /var/run/kdm/ fails to be created on boot (#657785)

* Thu Nov 11 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-11
- kdebugrc: DisableAll=true (#652367)

* Fri Oct 29 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-10
- kdmrc: UserList=false

* Thu Oct 14 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-9
- drop plasma-{desktop,netbook}-appletsrc
- plasmarc: set default plasma(-netbook) themes (#642763)

* Sat Oct 09 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-8
- rename 00-start-here script to ensure it runs (again).

* Fri Oct 08 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-7
- make 00-start-here-kde-fedora.js look for simplelauncher too (#615621)

* Tue Sep 28 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-6
- move plasma-desktop bits into kde-settings/kde-profile instead

* Tue Sep 28 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-5
- 00-start-here-kde-fedora.js plasma updates script (#615621)

* Fri Sep 03 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-4
- kdeglobals : drop [Icons] Theme=Fedora-KDE (#615621)

* Tue Aug 03 2010 Jaroslav Reznik <jreznik@redhat.com> 4.5-3
- laughlin kde theme as default

* Mon Apr 26 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-2
- kde-settings-kdm depends on xorg-x11-xdm (#537608)

* Tue Apr 13 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-1.1
- -kdm: own /var/spool/gdm (#551310,#577482)

* Tue Feb 23 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-1
- 4.5 branch for F-14
- (re)enable kdebug

* Tue Feb 23 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-13
- disable kdebug by default (#560508)

* Mon Feb 22 2010 Jaroslav Reznik <jreznik@redhat.com> 4.4-12
- added dist tag to release

* Mon Feb 22 2010 Jaroslav Reznik <jreznik@redhat.com> 4.4-11
- goddard kde theme as default

* Sat Jan 30 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-10
- move /etc/kde/kdm/backgroundrc => /var/lib/kdm/backgroundrc (#522513)
- own /var/lib/kdm (regression, #442081)

* Fri Jan 29 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-9
- krunnerrc: disable nepomuksearch plugin by default (#559977)

* Wed Jan 20 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-8
- plasma-netbook workspace has no wallpaper configured (#549996)

* Tue Jan 05 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-7
- externalize fedora-kde-icon-theme (#547701)

* Wed Dec 30 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-6.1
- -kdm: Requires: kdm

* Fri Dec 25 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-6
- use qtcurve-gtk2 by default (#547700)

* Wed Dec 23 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-4
- enable nepomuk, with some conservative defaults (#549436)

* Tue Dec 01 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-3
- kdmrc: ServerArgsLocal=-nr , for better transition from plymouth

* Tue Dec 01 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-2
- kdmrc: revert to ServerVTs=-1 (#475890)

* Sun Nov 29 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-1
- -pulseaudio: drop xine-lib-pulseaudio (subpkg no longer exists)
