## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global relnum 43
%global Bg_Name F43
%global bgname %(t="%{Bg_Name}";echo ${t,,})

# Disable Extras subpackages by default
%bcond          extras 0

Name:           %{bgname}-backgrounds
Version:        %{relnum}.0.4
Release:        %autorelease
Summary:        Fedora %{relnum} default desktop background

License:        CC-BY-SA-4.0
URL:            https://fedoraproject.org/wiki/Design
Source0:        https://github.com/fedoradesign/backgrounds/releases/download/v%{version}/%{name}-%{version}.tar.xz


BuildArch:      noarch

BuildRequires:  kde-filesystem
BuildRequires:  make
BuildRequires:  ImageMagick

Requires:       %{name}-budgie = %{version}-%{release}
Requires:       %{name}-gnome = %{version}-%{release}
Requires:       %{name}-kde = %{version}-%{release}
Requires:       %{name}-xfce = %{version}-%{release}
Requires:       %{name}-mate = %{version}-%{release}


%description
This package contains desktop backgrounds for the Fedora  %{relnum} default
theme.  Pulls in themes for GNOME, KDE, Mate and Xfce desktops.

%package        base
Summary:        Base images for Fedora  %{relnum} default background
License:        CC-BY-SA-4.0
# Ensure JXL loaders are installed for GTK and Qt
Requires:       (jxl-pixbuf-loader if gdk-pixbuf2)
Requires:       (kf6-kimageformats if qt6-qtbase-gui)

%description    base
This package contains base images for Fedora  %{relnum} default background.

%package        budgie
Summary:        Fedora  %{relnum} default wallpaper for Budgie
Requires:       %{name}-base = %{version}-%{release}
Recommends:	%{name}-gnome = %{version}-%{release}

%description    budgie
This package contains Budgie desktop wallpaper for the
Fedora  %{relnum} default theme.

%package        gnome
Summary:        Fedora  %{relnum} default wallpaper for Gnome and Cinnamon
Requires:       %{name}-base = %{version}-%{release}

%description    gnome
This package contains Gnome/Cinnamon desktop wallpaper for the
Fedora  %{relnum} default theme.

%package        kde
Summary:        Fedora  %{relnum} default wallpaper for KDE
Requires:       %{name}-base = %{version}-%{release}
Requires:       kde-filesystem

%description    kde
This package contains KDE desktop wallpaper for the Fedora  %{relnum}
default them

%package        mate
Summary:        Fedora %{relnum} default wallpaper for Mate
Requires:       %{name}-base = %{version}-%{release}

%description    mate
This package contains Mate desktop wallpaper for the Fedora  %{relnum}
default theme.

%package        xfce
Summary:        Fedora  %{relnum} default background for XFCE4

Requires:       %{name}-base = %{version}-%{release}
%if 0%{?fedora}
Requires:       xfdesktop
%endif 

%description    xfce
This package contains XFCE4 desktop background for the Fedora  %{relnum}
default theme.

%if %{with extras}
%package        extras-base
Summary:        Base images for  Extras Backgrounds
License:        CC-BY-4.0 AND CC-BY-SA-4.0 AND CC0-1.0

%description    extras-base
This package contains base images for  supplemental
wallpapers.

%package        extras-gnome
Summary:        Extra  Wallpapers for Gnome and Cinnamon

Requires:       %{name}-extras-base = %{version}-%{release}

%description    extras-gnome
This package contains  supplemental wallpapers for Gnome
and Cinnamon

%package        extras-mate
Summary:        Extra  Wallpapers for Mate

Requires:       %{name}-extras-base = %{version}-%{release}

%description    extras-mate
This package contains  supplemental wallpapers for Mate

%package        extras-kde
Summary:        Extra  Wallpapers for KDE

Requires:       %{name}-extras-base = %{version}-%{release}

%description    extras-kde
This package contains  supplemental wallpapers for Gnome

%package        extras-xfce
Summary:        Extra  Wallpapers for XFCE

Requires:       %{name}-extras-base = %{version}-%{release}

%description    extras-xfce
This package contains  supplemental wallpapers for XFCE
%endif

%prep
%autosetup -n %{name}-%{version}


%build
%make_build %{?with_extras:SUBDIRS="default extras"}

%install
%make_install %{?with_extras:SUBDIRS="default extras"}
# Fix permission
chmod 644 %{buildroot}%{_datadir}/wallpapers/%{Bg_Name}/metadata.json

%files
%doc

%files base
%license CC-BY-SA-4.0 Attribution
%dir %{_datadir}/backgrounds/%{bgname}
%dir %{_datadir}/backgrounds/%{bgname}/default
%{_datadir}/backgrounds/%{bgname}/default/%{bgname}*.{jxl,xml}

%files kde
%{_datadir}/wallpapers/%{Bg_Name}/

%files gnome
%{_datadir}/gnome-background-properties/%{bgname}.xml
%dir %{_datadir}/gnome-background-properties/

%files budgie
%{_datadir}/gnome-background-properties/%{bgname}-budgie.xml

%files mate
%{_datadir}/mate-background-properties/%{bgname}.xml
%dir %{_datadir}/mate-background-properties/

%files xfce
%{_datadir}/xfce4/backdrops/%{bgname}*.jxl
%if %{with extras}
%exclude %{_datadir}/xfce4/backdrops/%{bgname}-extras*.png
%endif
%dir %{_datadir}/xfce4/
%dir %{_datadir}/xfce4/backdrops/

%if %{with extras}
%files extras-base
%license CC-BY-SA-4.0 Attribution
%{_datadir}/backgrounds/%{bgname}/extras/

%files extras-gnome
%{_datadir}/gnome-background-properties/%{bgname}-extras.xml

%files extras-kde
%{_datadir}/wallpapers/%{Bg_Name}_*/

%files extras-mate
%{_datadir}/mate-background-properties/%{bgname}-extras.xml

%files extras-xfce
%{_datadir}/xfce4/backdrops/%{bgname}-extras*.png
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 43.0.4-2
- Latest state for f43-backgrounds

* Thu Jan 22 2026 Luya Tshimbalanga <luya@fedoraproject.org> - 43.0.4-1
- Update to 43.0.4

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 43.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Sep 19 2025 Luya Tshimbalanga <luya@fedoraproject.org> - 43.0.3-1
- Update to 43.0.3 removing transparency in default wallpapers

* Wed Sep 17 2025 Luya Tshimbalanga <luya@fedoraproject.org> - 43.0.2-1
- Update to 43.0.2 with DP3 display support

* Sun Aug 24 2025 Luya Tshimbalanga <luya@fedoraproject.org> - 43.0.1-2
- Drop unavailable xfdesktop dependency for EPEL10

* Fri Aug 15 2025 Luya Tshimbalanga <luya@fedoraproject.org> - 43.0.1-1
- Update to 43.0.1 with minor bug fix

* Thu Aug 14 2025 Luya Tshimbalanga <luya@fedoraproject.org> - 43.0.0-1
- Initial import
## END: Generated by rpmautospec
