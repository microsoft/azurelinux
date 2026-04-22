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
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 43.0.0-3
- Latest state for desktop-backgrounds

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
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
