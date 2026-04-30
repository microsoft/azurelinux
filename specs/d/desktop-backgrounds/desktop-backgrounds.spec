## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global rh_backgrounds_version 15
%global waves_version 0.1.2
%global fedora_release_name f43
%global gnome_default default
%global picture_ext jxl

Name:           desktop-backgrounds
Version:        43.0.0
Release:        %autorelease
Summary:        Desktop backgrounds

License:        LicenseRef-Fedora-Public-Domain AND GPL-1.0-or-later
Source0:        redhat-backgrounds-%{rh_backgrounds_version}.tar.bz2
Source2:        Propaganda-1.0.0.tar.gz
Source3:        README.Propaganda
Source5:        waves-%{waves_version}.tar.bz2
Source6:        FedoraWaves-metadata.desktop
BuildArch:      noarch
%if "x%{?picture_ext}" != "xjxl"
BuildRequires:   ImageMagick
BuildRequires:   %{fedora_release_name}-backgrounds-base
%endif

%description
The desktop-backgrounds package contains artwork intended to be used as
desktop background image.


%package        basic
Summary:        Desktop backgrounds
Provides:       desktop-backgrounds = %{version}-%{release}
Obsoletes:      desktop-backgrounds < %{version}-%{release}

%description    basic
The desktop-backgrounds-basic package contains artwork intended to be used as
desktop background image.

%package        budgie
Summary:        The default Fedora wallpaper from Budgie desktop
Requires:       %{fedora_release_name}-backgrounds-budgie
Requires:       gsettings-desktop-schemas >= 2.91.92
Provides:       system-backgrounds-budgie = %{version}-%{release}

%description    budgie
The desktop-backgrounds-budgie package sets default background in budgie.

%package        gnome
Summary:        The default Fedora wallpaper from GNOME desktop
Requires:       %{fedora_release_name}-backgrounds-gnome
# starting with this release, gnome uses picture-uri instead of picture-filename
# see gnome bz #633983
Requires:       gsettings-desktop-schemas >= 2.91.92
Provides:       system-backgrounds-gnome = %{version}-%{release}

%description    gnome
The desktop-backgrounds-gnome package sets default background in gnome.

%package        kde
Summary:        The default Fedora wallpaper from KDE Plasma desktop
Requires:       %{fedora_release_name}-backgrounds-kde
Provides:       system-backgrounds-kde = %{version}-%{release}

%description    kde
The desktop-backgrounds-kde package sets default background in KDE Plasma.

%package        compat
Summary:        The default Fedora wallpaper for less common DEs
Requires:       %{fedora_release_name}-backgrounds-base
Provides:       system-backgrounds-compat = %{version}-%{release}

%description    compat
The desktop-backgrounds-compat package contains file-names used
by less common Desktop Environments such as LXDE to set up the
default wallpaper.

%package        waves
Summary:        Desktop backgrounds for the Waves theme

%description    waves
The desktop-backgrounds-waves package contains the "Waves" desktop backgrounds
which were used in Fedora 9.


%prep
%autosetup -n redhat-backgrounds-%{rh_backgrounds_version}

# move things where %%doc can find them
cp -a %{SOURCE3} .
mv images/space/*.ps .
mv images/space/README* .

# add propaganda
(cd tiles && tar zxf %{SOURCE2})

# add waves
tar xjf %{SOURCE5}

%install
mkdir -p %{buildroot}%{_prefix}/share/backgrounds
cd %{buildroot}%{_prefix}/share/backgrounds

cp -a %{_builddir}/redhat-backgrounds-%{rh_backgrounds_version}/images .
cp -a %{_builddir}/redhat-backgrounds-%{rh_backgrounds_version}/tiles .

mkdir waves
# copy actual image files
cp -a %{_builddir}/redhat-backgrounds-%{rh_backgrounds_version}/waves-%{waves_version}/*.png waves
# copy animation xml file
cp -a %{_builddir}/redhat-backgrounds-%{rh_backgrounds_version}/waves-%{waves_version}/waves.xml waves

mkdir -p %{buildroot}%{_datadir}/gnome-background-properties
cp -a %{_builddir}/redhat-backgrounds-%{rh_backgrounds_version}/desktop-backgrounds-basic.xml %{buildroot}%{_prefix}/share/gnome-background-properties
cp -a %{_builddir}/redhat-backgrounds-%{rh_backgrounds_version}/waves-%{waves_version}/desktop-backgrounds-waves.xml %{buildroot}%{_prefix}/share/gnome-background-properties

mkdir -p %{buildroot}%{_datadir}/mate-background-properties
sed -e '/DOCTYPE/s/gnome/mate/' \
    %{_builddir}/redhat-backgrounds-%{rh_backgrounds_version}/desktop-backgrounds-basic.xml \
    > %{buildroot}%{_prefix}/share/mate-background-properties/desktop-backgrounds-basic.xml
sed -e '/DOCTYPE/s/gnome/mate/' \
    %{_builddir}/redhat-backgrounds-%{rh_backgrounds_version}/waves-%{waves_version}/desktop-backgrounds-waves.xml \
    > %{buildroot}%{_prefix}/share/mate-background-properties/desktop-backgrounds-waves.xml

bgdir=%{buildroot}%{_datadir}/backgrounds
for I in tiles/Propaganda images/dewdop_leaf.jpg images/dragonfly.jpg images/frosty_pipes.jpg images/in_flight.jpg images/leaf_veins.jpg \
        images/leafdrops.jpg images/lightrays-transparent.png images/lightrays.png images/lightrays2.png images/raingutter.jpg images/riverstreet_rail.jpg \
        images/sneaking_branch.jpg images/space images/yellow_flower.jpg; do
        rm -rf ${bgdir}/${I}
done

# FedoraWaves theme for KDE4
mkdir -p %{buildroot}%{_datadir}/wallpapers/Fedora_Waves/contents/images
install -m 644 -p %{SOURCE6} %{buildroot}%{_datadir}/wallpapers/Fedora_Waves/metadata.desktop
(cd %{buildroot}%{_datadir}/wallpapers/Fedora_Waves/contents/;
ln -s ../../../backgrounds/waves/waves-eeepc-3-night.png screenshot.png
cd %{buildroot}%{_datadir}/wallpapers/Fedora_Waves/contents/images
ln -s ../../../../backgrounds/waves/waves-normal-3-night.png 1024x768.png
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1280x800.png
# FIXME: there doesn't seem to be a 5:4 image in the latest iteration
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1280x1024.png
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1440x900.png
ln -s ../../../../backgrounds/waves/waves-normal-3-night.png 1600x1200.png
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1920x1200.png
)

# Defaults for various desktops:

#   for Budgie, sets for: gnome desktop, gnome screensaver, and slick-greeter
#   set to 30, 20 is used by upstream and budgie branding package uses 10

mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas
/bin/echo '[org.gnome.desktop.background:Budgie]' > \
    %{buildroot}%{_datadir}/glib-2.0/schemas/30_budgie_org.gnome.desktop.background.fedora.gschema.override
/bin/echo "picture-uri='file://%{_datadir}/backgrounds/%{fedora_release_name}/%{gnome_default}/%{fedora_release_name}-01-day.%{picture_ext}'" >> \
    %{buildroot}%{_datadir}/glib-2.0/schemas/30_budgie_org.gnome.desktop.background.fedora.gschema.override
/bin/echo "picture-uri-dark='file://%{_datadir}/backgrounds/%{fedora_release_name}/%{gnome_default}/%{fedora_release_name}-01-night.%{picture_ext}'" >> \
    %{buildroot}%{_datadir}/glib-2.0/schemas/30_budgie_org.gnome.desktop.background.fedora.gschema.override

/bin/echo '[org.gnome.desktop.screensaver:Budgie]' > \
    %{buildroot}%{_datadir}/glib-2.0/schemas/30_budgie_org.gnome.desktop.screensaver.fedora.gschema.override
/bin/echo "picture-uri='file://%{_datadir}/backgrounds/%{fedora_release_name}/%{gnome_default}/%{fedora_release_name}-01-day.%{picture_ext}'" >> \
    %{buildroot}%{_datadir}/glib-2.0/schemas/30_budgie_org.gnome.desktop.screensaver.fedora.gschema.override
/bin/echo "picture-uri-dark='file://%{_datadir}/backgrounds/%{fedora_release_name}/%{gnome_default}/%{fedora_release_name}-01-night.%{picture_ext}'" >> \
    %{buildroot}%{_datadir}/glib-2.0/schemas/30_budgie_org.gnome.desktop.screensaver.fedora.gschema.override

/bin/echo '[x.dm.slick-greeter:Budgie]' > \
    %{buildroot}%{_datadir}/glib-2.0/schemas/30_budgie_x.dm.slick_greeter.fedora.gschema.override
/bin/echo "background='file://%{_datadir}/backgrounds/%{fedora_release_name}/%{gnome_default}/%{fedora_release_name}-01-day.%{picture_ext}'" >> \
    %{buildroot}%{_datadir}/glib-2.0/schemas/30_budgie_x.dm.slick_greeter.fedora.gschema.override

#   for GNOME

mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas
/bin/echo '[org.gnome.desktop.background]' > \
    %{buildroot}%{_datadir}/glib-2.0/schemas/10_org.gnome.desktop.background.fedora.gschema.override
/bin/echo "picture-uri='file://%{_datadir}/backgrounds/%{fedora_release_name}/%{gnome_default}/%{fedora_release_name}-01-day.%{picture_ext}'" >> \
    %{buildroot}%{_datadir}/glib-2.0/schemas/10_org.gnome.desktop.background.fedora.gschema.override
/bin/echo "picture-uri-dark='file://%{_datadir}/backgrounds/%{fedora_release_name}/%{gnome_default}/%{fedora_release_name}-01-night.%{picture_ext}'" >> \
    %{buildroot}%{_datadir}/glib-2.0/schemas/10_org.gnome.desktop.background.fedora.gschema.override

# Use the Fedora background on the GNOME lockscreen as well. Would be awesome to
# have a separate image here to complement the default Fedora background, rather
# than using the same image in both places, but previously we've mixed Fedora
# desktop backgrounds with GNOME lockscreens, and they just do not match at all.

/bin/echo '[org.gnome.desktop.screensaver]' > \
    %{buildroot}%{_datadir}/glib-2.0/schemas/10_org.gnome.desktop.screensaver.fedora.gschema.override
/bin/echo "picture-uri='file://%{_datadir}/backgrounds/%{fedora_release_name}/%{gnome_default}/%{fedora_release_name}-01-day.%{picture_ext}'" >> \
    %{buildroot}%{_datadir}/glib-2.0/schemas/10_org.gnome.desktop.screensaver.fedora.gschema.override
/bin/echo "picture-uri-dark='file://%{_datadir}/backgrounds/%{fedora_release_name}/%{gnome_default}/%{fedora_release_name}-01-night.%{picture_ext}'" >> \
    %{buildroot}%{_datadir}/glib-2.0/schemas/10_org.gnome.desktop.screensaver.fedora.gschema.override

#   for KDE

(cd %{buildroot}%{_datadir}/wallpapers;
ln -s F%{sub %{fedora_release_name} 2 -1} Default
)

#   for XFCE, LXDE, etc.

%if "x%{?picture_ext}" == "xjxl"
  (cd %{buildroot}%{_datadir}/backgrounds/images;
  ln -s ../%{fedora_release_name}/default/%{fedora_release_name}-01-day.%{picture_ext} \
      default.%{picture_ext}
  ln -s ../%{fedora_release_name}/default/%{fedora_release_name}-01-day.%{picture_ext} \
      default-5_4.%{picture_ext}
  ln -s ../%{fedora_release_name}/default/%{fedora_release_name}-01-day.%{picture_ext} \
      default-16_9.%{picture_ext}
  ln -s ../%{fedora_release_name}/default/%{fedora_release_name}-01-day.%{picture_ext} \
      default-16_10.%{picture_ext}

  ln -s ../%{fedora_release_name}/default/%{fedora_release_name}-01-night.%{picture_ext} \
      default-dark.%{picture_ext}
  ln -s ../%{fedora_release_name}/default/%{fedora_release_name}-01-night.%{picture_ext} \
      default-dark-5_4.%{picture_ext}
  ln -s ../%{fedora_release_name}/default/%{fedora_release_name}-01-night.%{picture_ext} \
      default-dark-16_9.%{picture_ext}
  ln -s ../%{fedora_release_name}/default/%{fedora_release_name}-01-night.%{picture_ext} \
      default-dark-16_10.%{picture_ext}

  cd ..
  ln -s ./%{fedora_release_name}/default/%{fedora_release_name}-01-day.%{picture_ext} \
      default.%{picture_ext}
  ln -s ./%{fedora_release_name}/default/%{fedora_release_name}-01-night.%{picture_ext} \
      default-dark.%{picture_ext}
  )
%else
  (cd %{buildroot}%{_datadir}/backgrounds/images;
  convert %{_datadir}/backgrounds/%{fedora_release_name}/default/%{fedora_release_name}.%{picture_ext} \
        -alpha off default.jxl
  convert %{_datadir}/backgrounds/%{fedora_release_name}/default/%{fedora_release_name}.%{picture_ext} \
        -alpha off default-5_4.jxl
  convert %{_datadir}/backgrounds/%{fedora_release_name}/default/%{fedora_release_name}.%{picture_ext} \
        -alpha off default-16_9.jxl
  convert %{_datadir}/backgrounds/%{fedora_release_name}/default/%{fedora_release_name}.%{picture_ext} \
        -alpha off default-16_10.jxl
  )
%endif

# symlink for a default.xml background
  cd %{buildroot}%{_datadir}/backgrounds;
  ln -s %{fedora_release_name}/default/%{fedora_release_name}.xml\
      default.xml

%files basic
%dir %{_datadir}/backgrounds
%dir %{_datadir}/backgrounds/tiles
%dir %{_datadir}/backgrounds/images
%{_datadir}/backgrounds/tiles/*.png
%{_datadir}/backgrounds/tiles/*jpg
%{_datadir}/backgrounds/images/earth_from_space.jpg
%{_datadir}/backgrounds/images/flowers_and_leaves.jpg
%{_datadir}/backgrounds/images/ladybugs.jpg
%{_datadir}/backgrounds/images/stone_bird.jpg
%{_datadir}/backgrounds/images/tiny_blast_of_red.jpg
%dir %{_datadir}/gnome-background-properties
%{_datadir}/gnome-background-properties/desktop-backgrounds-basic.xml
%dir %{_datadir}/mate-background-properties
%{_datadir}/mate-background-properties/desktop-backgrounds-basic.xml
%dir %{_datadir}/wallpapers

%files waves
%dir %{_datadir}/backgrounds/waves
%{_datadir}/backgrounds/waves/*.png
%{_datadir}/backgrounds/waves/waves.xml
%{_datadir}/gnome-background-properties/desktop-backgrounds-waves.xml
%{_datadir}/mate-background-properties/desktop-backgrounds-waves.xml
%{_datadir}/wallpapers/Fedora_Waves

%files budgie
%{_datadir}/glib-2.0/schemas/30_budgie_org.gnome.desktop.background.fedora.gschema.override
%{_datadir}/glib-2.0/schemas/30_budgie_org.gnome.desktop.screensaver.fedora.gschema.override
%{_datadir}/glib-2.0/schemas/30_budgie_x.dm.slick_greeter.fedora.gschema.override

%files gnome
%{_datadir}/glib-2.0/schemas/10_org.gnome.desktop.background.fedora.gschema.override
%{_datadir}/glib-2.0/schemas/10_org.gnome.desktop.screensaver.fedora.gschema.override

%files kde
%dir %{_datadir}/wallpapers
%{_datadir}/wallpapers/Default

%files compat
%dir %{_datadir}/backgrounds/images/
%{_datadir}/backgrounds/images/default*
%{_datadir}/backgrounds/default.%{picture_ext}
%{_datadir}/backgrounds/default-dark.%{picture_ext}
%{_datadir}/backgrounds/default.xml

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 43.0.0-3
- test: add initial lock files

* Wed Jan 07 2026 Yaakov Selkowitz <yselkowi@redhat.com> - 43.0.0-2
- Add desktop-backgrounds-kde

* Thu Aug 14 2025 Luya Tshimbalanga <luya@fedoraproject.org> - 43.0.0-1
- Enable Fedora 43 theme

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 42.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Feb 19 2025 Miroslav Suchý <msuchy@redhat.com> - 42.0.0-3
- correct license and migrate to SPDX

* Fri Feb 14 2025 Luya Tshimbalanga <luya@fedoraproject.org> - 42.0.0-2
- Fix symlink for compat subpackage

* Thu Feb 13 2025 Luya Tshimbalanga <luya@fedoraproject.org> - 42.0.0-1
- Switch to Fedora 42 theme with jxl format support

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 41.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 14 2024 Luya Tshimbalanga <luya@fedoraproject.org> - 41.0.0-1
- Enable F41 theme

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 40.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Mar 07 2024 Luya Tshimbalanga <luya@fedoraproject.org> - 40.0.0-1
- Enable F40 theme

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 39.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 39.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 08 2023 Neal Gompa <ngompa@fedoraproject.org> - 39.0.0-3
- No-change rebuild for merging Bodhi updates for Budgie backgrounds

* Wed Sep 06 2023 Joshua Strobl <me@joshuastrobl.com> - 39.0.0-2
- Implement a budgie backgrounds sub-package and start symlinking dark
  variant

* Sat Sep 02 2023 Adam Williamson <awilliam@redhat.com> - 39.0.0-1
- Bump to 39 for Fedora 39

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 38.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 14 2023 Luya Tshimbalanga <luya@fedoraproject.org> - 38.0.0-2
- Migrate to SPDX license

* Sat Feb 11 2023 Luya Tshimbalanga <luya@fedoraproject.org> - 38.0.0-1
- Enable F38 theme

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 37.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Oct 07 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 37.0.0-5
- Revert build requirement change for compat subpackage

* Fri Oct 07 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 37.0.0-4
- Revert build requirement change for compat subpackage

* Mon Oct 03 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 37.0.0-3
- Revert changes for MATE, XFCE and LXDE

* Tue Sep 27 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 37.0.0-2
- Switch to webp format by default for Fedora backgrounds

* Thu Aug 11 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 37.0.0-1
- Enable F37 theme

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 36.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar 10 2022 Adam Williamson <awilliam@redhat.com> - 36.0.0-3
- Set GNOME defaults to day and night images, not the animated XML

* Thu Mar 10 2022 Adam Williamson <awilliam@redhat.com> - 36.0.0-2
- Drop source7 and source8, the spec no longer uses them

* Wed Feb 16 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 36.0.0-1
- Enable F36 theme

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 35.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 26 2021 Luya Tshimbalanga <luya@fedoraproject.org> - 35.0.0-1
- Enable F35 theme

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 34.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Apr 01 2021 Luya Tshimbalanga <luya@fedoraproject.org> - 34.0.0-3
- Adding a default.xml background Resolves: fedora#1928383

* Wed Mar 31 2021 raveit65 <mate@raveit.de> - 34.0.0-2
- adding a default.xml background

* Mon Feb 08 2021 Luya Tshimbalanga <luya@fedoraproject.org> - 34.0.0-1
- Enable F34 theme

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 33.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 Luya Tshimbalanga <luya@fedoraproject.org> - 33.0.0-1
- Enable F33 theme Clean up spec file Drop all old subfolders
  (standard,normalish,wide) in favor of single default source folder

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 32.0.0-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Apr 04 2020 Björn Esser <besser82@fedoraproject.org> - 32.0.0-44
- Fix conditional

* Thu Apr 02 2020 Björn Esser <besser82@fedoraproject.org> - 32.0.0-43
- Bump release

* Thu Apr 02 2020 Björn Esser <besser82@fedoraproject.org> - 32.0.0-42
- Fix string quoting for rpm >= 4.16

* Sat Mar 07 2020 Adam Williamson <awilliam@redhat.com>
- Fix up -compat symlinks for removal of aspect ratio-specific images

* Fri Mar 06 2020 Adam Williamson <awilliam@redhat.com>
- Fix fedora_release_name which was not updated in -1

* Thu Mar 05 2020 Luya Tshimbalanga <luya@fedoraproject.org>
- Enable F32 theme

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 04 2019 Luya Tshimbalanga <luya@fedoraproject.org>
- Enable F31 theme

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 18 2019 Luya Tshimbalanga <luya@fedoraproject.org>
- Add 16:9 wide ratio background and set it as default (#1689409)

* Mon Mar 04 2019 Luya Tshimbalanga <luya@fedoraproject.org>
- Enable F30 theme

* Thu Feb 28 2019 Robin Lee <cheeselee@fedoraproject.org>
- Own %%{_datadir}/backgrounds/images/

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 06 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
- Remove obsolete scriptlets

* Tue Aug 28 2018 Luya Tshimbalanga <luya@fedoraproject.org>
- Enable F29 theme

* Tue Aug 28 2018 Luya Tshimbalanga <luya@fedoraproject.org>
- Enable F29 theme

* Tue Mar 06 2018 Luya Tshimbalanga <luya@fedoraproject.org>
- Enable F28 theme

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Miroslav Suchý <msuchy@redhat.com>
- use modern macro _builddir

* Wed Nov 08 2017 Miroslav Suchý <msuchy@redhat.com>
- use modern macro buildroot

* Wed Nov 08 2017 Miroslav Suchý <msuchy@redhat.com>
- preserve attributes

* Mon Sep 11 2017 Luya Tshimbalanga <luya@fedoraproject.org>
- Enable F27 theme

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 23 2017 Luya Tshimbalanga <luya@fedoraproject.org>
- Enable F26 theme

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 28 2016 Yaakov Selkowitz <yselkowi@redhat.com>
- Enable support for MATE desktop (#1395507)

* Mon Sep 26 2016 Adam Williamson <awilliam@redhat.com>
- bump to f25, committing for finalzone

* Mon Mar 21 2016 Stephen Gallagher <sgallagh@redhat.com>
- Enable F24 theme

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 30 2015 Michael Catanzaro <mcatanzaro@gnome.org>
- Use Fedora theme for GNOME lockscreen as well.

* Wed Sep 30 2015 Michael Catanzaro <mcatanzaro@gnome.org>
- Use Fedora theme for GNOME lockscreen as well.

* Wed Aug 05 2015 Adam Williamson <awilliam@redhat.com>
- Switch to F23 theme.

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Martin Sourada <mso@fedoraproject.org>
- And another typo.

* Thu Feb 26 2015 Martin Sourada <mso@fedoraproject.org>
- Fix year in changelog.

* Thu Feb 26 2015 Martin Sourada <mso@fedoraproject.org>
- Switch to F22 theme.

* Wed Aug 27 2014 Martin Sourada <mso@fedoraproject.org>
- switch to new backgrounds.

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 10 2013 Martin Sourada <mso@fedoraproject.org>
- Merge branch 'master' of ssh://pkgs.fedoraproject.org/desktop-backgrounds

* Tue Sep 10 2013 Martin Sourada <mso@fedoraproject.org>
- Update to Heisenbug.

* Wed May 22 2013 Martin Sourada <mso@fedoraproject.org>
- Rebuild against new backgrounds.

* Tue Mar 12 2013 Martin Sourada <mso@fedoraproject.org>
- Update to schroedinger's cat. Drop -xfce subpackage, because xfce uses
  -compat.

* Wed Feb 13 2013 Dennis Gilmore <dennis@ausil.us> - 18.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Aug 19 2012 Martin Sourada <mso@fedoraproject.org> - 18.0.0-1
- Switch to Spherical Cow. Add nn_ to filename of gschema overrida. Drop
  old now non-unused conditionals.

* Wed Jul 18 2012 Dennis Gilmore <dennis@ausil.us> - 17.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 07 2012 Martin Sourada <mso@fedoraproject.org> - 17.0.0-1
- switch to beefy miracle.

* Fri Jan 13 2012 Dennis Gilmore <dennis@ausil.us> - 16.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 29 2011 Martin Sourada <mso@fedoraproject.org> - 16.0.0-2
- Fix a mistake.

* Thu Jul 28 2011 Martin Sourada <mso@fedoraproject.org> - 16.0.0-1
- Prepare for Verne release.

* Sat Apr 02 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-10
- some fixes to the spec file.

* Sat Apr 02 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-9
- Merge branch 'master' into f15/master

* Sat Apr 02 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-8
- Merge branch 'master' into f15/master

* Tue Mar 22 2011 Tom "spot" Callaway <tcallawa@redhat.com> - 15.0.0-7
- use actual uri

* Tue Mar 22 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-6
- Prepare for gnome-desktop3-2.91.92.

* Mon Mar 21 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-5
- set default wallpaper for gnome (rhbz #683179).

* Mon Mar 07 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 15.0.0-4
- * Mon Mar 07 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 15.0.0-4 - Drop
  unused -kde subpackage, we set the default through kde-settings & pull it
  in through system-plasma-desktoptheme, which is Provided by lovelock-kde-
  theme

* Tue Feb 08 2011 Dennis Gilmore <dennis@ausil.us> - 15.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-2
- The file-names should not contain the word fedora for the system-
  backgrounds* virtual provides to be more effective

* Mon Feb 07 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-1
- Provide file-names for default wallpapers * new subpackages -gnome, -kde,
  xfce for the various DEs * -compat subpackage is really for setting the
  default wallpaper for the other desktops like LXDE, adjust the
  description and summary * use correct suffix in file-names in -compat
  subpackage - Sync version with Fedora release

* Thu Aug 12 2010 Martin Sourada <mso@fedoraproject.org> - 9.0.0-18
- * Thu Aug 12 2010 Martin Sourada <mso@fedoraproject.org> - 9.0.0-15 -
  Rebuild, add dist tag. - Properly versioned provides/obsoletes for the
  -basic subpackage

* Wed Aug 04 2010 Christoph Wickert <cwickert@fedoraproject.org> - 9.0.0-17
- * Thu Aug 05 2010 Christoph Wickert <cwickert@fedoraproject.org> -
  9.0.0-14 - Update for F14 Laughlin artwork

* Wed Jul 28 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.0-16
- dist-git conversion

* Thu Mar 18 2010 Christoph Wickert <cwickert@fedoraproject.org> - 9.0.0-15
- Update for F13 Goddard artwork

* Tue Mar 02 2010 Matthias Clasen <mclasen@fedoraproject.org> - 9.0.0-14
- bump rev

* Tue Mar 02 2010 Matthias Clasen <mclasen@fedoraproject.org> - 9.0.0-13
- fix a directory ownership issue

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 9.0.0-12
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Sun Nov 01 2009 Christoph Wickert <cwickert@fedoraproject.org> - 9.0.0-11
- Update for F12 constantine artwork

* Fri Jul 24 2009 Jesse Keating <jkeating@fedoraproject.org> - 9.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Tom Callaway <spot@fedoraproject.org> - 9.0.0-9
- fix compat packages

* Tue Feb 24 2009 Jesse Keating <jkeating@fedoraproject.org> - 9.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 21 2008 Matthias Clasen <mclasen@fedoraproject.org> - 9.0.0-7
- Tweak descriptions

* Tue Nov 04 2008 Ray Strode <rstrode@fedoraproject.org> - 9.0.0-6
- Fix compat links after solar-backgrounds restructuring (bug 469789)

* Tue Oct 28 2008 Ray Strode <rstrode@fedoraproject.org> - 9.0.0-5
- Make compat subpackage depend on solar backgrounds (bug 468749)

* Tue Oct 21 2008 Ray Strode <rstrode@fedoraproject.org> - 9.0.0-4
- Move waves wallpapers to a subpackage

* Wed Oct 08 2008 Than Ngo <than@fedoraproject.org> - 9.0.0-3
- own /usr/share/wallpapers

* Tue Apr 15 2008 Ray Strode <rstrode@fedoraproject.org> - 9.0.0-2
- update changelog entry version 9.0.0 to match build version

* Fri Apr 11 2008 Ray Strode <rstrode@fedoraproject.org> - 9.0.0-1
- Update wallpapers to latest iteration from art team - Add compat
  subpackage to provide compat-links for all the cruft that's accumulated
  over the years

* Fri Apr 11 2008 Than Ngo <than@fedoraproject.org> - 8.92-5
- Add Fedora_Waves theme for KDE4

* Mon Apr 07 2008 Matthias Clasen <mclasen@fedoraproject.org> - 8.92-4
- Rename FCV5-era backgrounds

* Sun Apr 06 2008 Matthias Clasen <mclasen@fedoraproject.org> - 8.92-3
- Drop infinity backgrounds, they will be moved to a separate package

* Sun Mar 30 2008 Matthias Clasen <mclasen@fedoraproject.org> - 8.92-2
- Make waves animation work

* Sat Mar 29 2008 Matthias Clasen <mclasen@fedoraproject.org> - 8.92-1
- Add waves

* Mon Oct 15 2007 Bill Nottingham <notting@fedoraproject.org> - 7.92-14
- makefile update to properly grab makefile.common

* Thu Oct 11 2007 Ray Strode <rstrode@fedoraproject.org> - 7.92-13
- Scale images

* Tue Oct 09 2007 Ray Strode <rstrode@fedoraproject.org> - 7.92-12
- Upgrade desktop backgrounds to higher fidelity versions, given by Máirín
  Duffy

* Wed Sep 26 2007 Máirín Duffy <duffy@fedoraproject.org> - 7.92-11
- wallpapers redone so there is no more banding - wallpapers renamed -
  infinity animated file bugs fixed (hopefully)

* Wed Sep 26 2007 Máirín Duffy <duffy@fedoraproject.org> - 7.92-10
- remove old file

* Wed Sep 26 2007 Máirín Duffy <duffy@fedoraproject.org> - 7.92-9
- wallpapers redone so there is no more banding - wallpapers renamed -
  infinity animated file bugs fixed (hopefully)

* Wed Sep 26 2007 Máirín Duffy <duffy@fedoraproject.org> - 7.92-8
- wallpapers redone so there is no more banding - wallpapers renamed -
  infinity animated file bugs fixed (hopefully)

* Thu Sep 20 2007 Ray Strode <rstrode@fedoraproject.org> - 7.92-7
- fix symlinks again

* Thu Sep 06 2007 Bill Nottingham <notting@fedoraproject.org> - 7.92-6
- fix symlinks

* Wed Sep 05 2007 Ray Strode <rstrode@fedoraproject.org> - 7.92-5
- revert some weirdness where I changed a version I shouldn't have

* Wed Sep 05 2007 Ray Strode <rstrode@fedoraproject.org> - 7.92-4
- create links for default.png etc until more artwork shows up - start
  animated backgrounds at midnight

* Tue Sep 04 2007 Ray Strode <rstrode@fedoraproject.org> - 7.92-3
- create links for default.png etc until more artwork shows up

* Thu Aug 30 2007 Jeremy Katz <katzj@fedoraproject.org> - 7.92-2
- need to include less infinity backgrounds for now; the space usage kill
  livecds

* Wed Aug 29 2007 Máirín Duffy <duffy@fedoraproject.org> - 7.92-1
- Add Infinity background

* Wed Aug 29 2007 Máirín Duffy <duffy@fedoraproject.org> - 2.0-75
- remove old artwork

* Wed Aug 08 2007 Matthias Clasen <mclasen@fedoraproject.org> - 2.0-74
- update license field

* Wed Sep 06 2006 John (J5) Palmieri <johnp@fedoraproject.org> - 2.0-73
- Backgrounds are now changed to jpgs and 4:3 has been replaced by a 5:4
  aspect image

* Fri Jul 28 2006 John (J5) Palmieri <johnp@fedoraproject.org> - 2.0-72
- Add 4:3 aspect ration version of background

* Fri Jul 28 2006 John (J5) Palmieri <johnp@fedoraproject.org> - 2.0-71
- Upload new redhat-background sources

* Fri Jul 28 2006 John (J5) Palmieri <johnp@fedoraproject.org> - 2.0-70
- Add dual screen backgrounds

* Wed Jul 26 2006 Alexander Larsson <alexl@fedoraproject.org> - 2.0-69
- Added wide default desktop background

* Wed Jul 26 2006 Alexander Larsson <alexl@fedoraproject.org> - 2.0-68
- update sources

* Tue Jun 06 2006 Matthias Clasen <mclasen@fedoraproject.org> - 2.0-67
- really remove default background

* Tue Jun 06 2006 Matthias Clasen <mclasen@fedoraproject.org> - 2.0-66
- Really remove the default background

* Mon Jun 05 2006 Matthias Clasen <mclasen@fedoraproject.org> - 2.0-65
- fix file lists

* Mon Jun 05 2006 Matthias Clasen <mclasen@fedoraproject.org> - 2.0-64
- remove branded images

* Mon Dec 19 2005 Ray Strode <rstrode@fedoraproject.org> - 2.0-63
- replace default fedora background with new one from Diana Fong

* Sat Dec 10 2005 Jesse Keating <jkeating@fedoraproject.org> - 2.0-62
- bad bump fix

* Fri Dec 09 2005 Jesse Keating <jkeating@fedoraproject.org>
- gcc update bump

* Thu Oct 06 2005 Matthias Clasen <mclasen@fedoraproject.org> - 2.0-60
- Fix #163345

* Wed Apr 27 2005 John (J5) Palmieri <johnp@fedoraproject.org> - 2.0-59
- update to redhat-backgrounds-9 which readds the earth_from_space.jpg

* Wed Apr 27 2005 John (J5) Palmieri <johnp@fedoraproject.org> - 2.0-58
- Add translations - redhat-backgrounds-8

* Mon Apr 04 2005 Elliot Lee <sopwith@fedoraproject.org> - 2.0-57
- fixes

* Mon Apr 04 2005 Elliot Lee <sopwith@fedoraproject.org> - 2.0-56
- fixes

* Tue Feb 22 2005 Elliot Lee <sopwith@fedoraproject.org> - 2.0-55
- shrink it

* Wed Feb 02 2005 Matthias Clasen <mclasen@fedoraproject.org> - 2.0-54
- Move xml descriptions to where the background capplet looks

* Mon Oct 18 2004 Alexander Larsson <alexl@fedoraproject.org> - 2.0-53
- RHEL build

* Mon Oct 18 2004 Alexander Larsson <alexl@fedoraproject.org> - 2.0-52
- New background

* Thu Sep 30 2004 Alexander Larsson <alexl@fedoraproject.org> - 2.0-51
- RHEL build

* Thu Sep 30 2004 Alexander Larsson <alexl@fedoraproject.org> - 2.0-50
- New default background infrastructure.

* Mon Sep 27 2004 Matthias Clasen <mclasen@fedoraproject.org> - 2.0-49
- Don't package duplicate images.

* Mon Sep 27 2004 Matthias Clasen <mclasen@fedoraproject.org> - 2.0-48
- Add a small set of default images to prepopulate the list in the
  background changer.

* Wed Sep 15 2004 Elliot Lee <sopwith@fedoraproject.org> - 2.0-47
- aaaaaargh

* Wed Sep 15 2004 Elliot Lee <sopwith@fedoraproject.org> - 2.0-46
- aaaaaargh

* Thu Sep 09 2004 Elliot Lee <sopwith@fedoraproject.org> - 2.0-45
- Change the default background

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.0-44
- auto-import changelog data from desktop-backgrounds-2.0-21.src.rpm Wed
  Jul 07 2004 Elliot Lee <sopwith@redhat.com> 2.0-21 - Change background
  for FC3test1

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.0-43
- auto-import changelog data from desktop-backgrounds-2.0-20.src.rpm Thu
  May 06 2004 Jeremy Katz <katzj@redhat.com> - 2.0-20 - background from
  Garrett for FC2 Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> - rebuilt

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.0-42
- auto-import changelog data from desktop-backgrounds-2.0-18.1.src.rpm Fri
  Jan 30 2004 Jonathan Blandford <jrb@redhat.com> 2.0-18.1 - rhel 4 alpha
  background

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.0-41
- auto-import changelog data from desktop-backgrounds-2.0-18.src.rpm Sun
  Nov 02 2003 Elliot Lee <sopwith@redhat.com> 2.0-18 - redhat-backgrounds-6
  Wed Oct 29 2003 Havoc Pennington <hp@redhat.com> 2.0-17 - redhat-
  backgrounds-5

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.0-40
- auto-import changelog data from desktop-backgrounds-2.0-16.src.rpm Tue
  Sep 23 2003 Michael Fulbright <msf@redhat.com> 2.0-16 - new fedora
  background Thu Jul 17 2003 Havoc Pennington <hp@redhat.com> 2.0-15 -
  background for the beta

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.0-39
- auto-import changelog data from desktop-backgrounds-2.0-14.src.rpm Fri
  Feb 21 2003 Havoc Pennington <hp@redhat.com> 2.0-14 - some background
  tweaks from Garrett Wed Jan 22 2003 Tim Powers <timp@redhat.com> -
  rebuilt Fri Dec 06 2002 Havoc Pennington <hp@redhat.com> - rebuild -
  update redhat-backgrounds version

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.0-38
- auto-import changelog data from desktop-backgrounds-2.0-10.src.rpm Tue
  Sep 03 2002 Havoc Pennington <hp@redhat.com> - new redhat-backgrounds
  from CVS with new default

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.0-37
- auto-import changelog data from desktop-backgrounds-2.0-9.src.rpm Tue Aug
  27 2002 Than Ngo <than@redhat.com> 2.0-9 - add missing kdebase desktop
  backgrounds (bug #72508)

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from desktop-backgrounds-2.0-8.src.rpm Wed Aug
  21 2002 Havoc Pennington <hp@redhat.com> - drop the beta placeholder in
  favor of final background

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from desktop-backgrounds-2.0-7.src.rpm Tue Aug
  13 2002 Havoc Pennington <hp@redhat.com> - new redhat-backgrounds with
  wallpapers moved to tiles - overwrite default.png with a placeholder

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from desktop-backgrounds-2.0-6.src.rpm Fri Aug
  09 2002 Havoc Pennington <hp@redhat.com> - new redhat-backgrounds with
  default.png Mon Jul 22 2002 Havoc Pennington <hp@redhat.com> - new
  redhat-backgrounds from CVS with default.jpg Tue Jul 16 2002 Havoc
  Pennington <hp@redhat.com> - new images from Garrett added to -extra Fri
  Jun 21 2002 Tim Powers <timp@redhat.com> - automated rebuild Sun Jun 16
  2002 Havoc Pennington <hp@redhat.com> - redo it, now it includes the
  tile/image collection redhat-backgrounds from CVS, plus propaganda - move
  things to datadir/share/backgrounds/images and
  datadir/share/backgrounds/wallpapers - split into a small basic package
  and an extra package, so we can have packages require the basic package
  without sucking in huge images - move space images into devserv CVS -
  move nautilus and kdebase tiles into devserv CVS Thu May 23 2002 Tim
  Powers <timp@redhat.com> - automated rebuild Wed Jan 09 2002 Tim Powers
  <timp@redhat.com> - automated rebuild

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from desktop-backgrounds-1.1-4.src.rpm Wed Jul
  12 2000 Prospector <bugzilla@redhat.com> - automatic rebuild Thu Jun 29
  2000 Dave Mason <dcm@redhat.com> - updated spec file to RPM guidelines
  Thu Jun 29 2000 Than Ngo <than@redhat.de> - FHS fixes Tue Feb 01 2000
  Preston Brown <pbrown@redhat.com> - new space backgrounds Fri Apr 02 1999
  Jonathan Blandford <jrb@redhat.com> - added propaganda tiles. Spruced it
  up a bit - moved README files out of tarball, and into docs dir. Fri Mar
  19 1999 Michael Fulbright <drmike@redhat.com> - First attempt

* Tue Mar 22 2011 Tom "spot" Callaway <tcallawa@redhat.com> - 15.0.0-32
- use actual uri

* Sat Apr 02 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-31
- Use stripes version of the wallpaper in f15's gnome.

* Sat Aug 03 2013 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 06 2018 Luya Tshimbalanga <luya@fedoraproject.org>
- Enable F28 theme

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Miroslav Suchý <msuchy@redhat.com>
- use modern macro _builddir

* Wed Nov 08 2017 Miroslav Suchý <msuchy@redhat.com>
- use modern macro buildroot

* Wed Nov 08 2017 Miroslav Suchý <msuchy@redhat.com>
- preserve attributes

* Mon Sep 11 2017 Luya Tshimbalanga <luya@fedoraproject.org>
- Enable F27 theme

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 23 2017 Luya Tshimbalanga <luya@fedoraproject.org>
- Enable F26 theme

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 28 2016 Yaakov Selkowitz <yselkowi@redhat.com>
- Enable support for MATE desktop (#1395507)

* Mon Sep 26 2016 Adam Williamson <awilliam@redhat.com>
- bump to f25, committing for finalzone

* Mon Mar 21 2016 Stephen Gallagher <sgallagh@redhat.com>
- Enable F24 theme

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 30 2015 Michael Catanzaro <mcatanzaro@gnome.org>
- Use Fedora theme for GNOME lockscreen as well.

* Wed Sep 30 2015 Michael Catanzaro <mcatanzaro@gnome.org>
- Use Fedora theme for GNOME lockscreen as well.

* Wed Aug 05 2015 Adam Williamson <awilliam@redhat.com>
- Switch to F23 theme.

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Martin Sourada <mso@fedoraproject.org>
- And another typo.

* Thu Feb 26 2015 Martin Sourada <mso@fedoraproject.org>
- Fix year in changelog.

* Thu Feb 26 2015 Martin Sourada <mso@fedoraproject.org>
- Switch to F22 theme.

* Wed Aug 27 2014 Martin Sourada <mso@fedoraproject.org>
- switch to new backgrounds.

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 10 2013 Martin Sourada <mso@fedoraproject.org>
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
