# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           azurelinux-icons
Summary:        Azure Linux - related brand icons, logos, and boot graphics
Version:        4.0.0
Release: 2%{?dist}
License:        MIT
URL:            https://github.com/microsoft/azurelinux

# License
Source0:        LICENSE

# Desktop icon assets — scalable SVG
Source10:       azurelinux-logo.svg

# Desktop icon assets — sized PNGs (generated from Azure Linux brand icon)
#We dont have a 36x36 icon we dont have any current customers that consume this size.
Source11:       azurelinux-logo-16.png
Source12:       azurelinux-logo-22.png
Source13:       azurelinux-logo-24.png
Source14:       azurelinux-logo-32.png
Source15:       azurelinux-logo-48.png
Source16:       azurelinux-logo-96.png
Source17:       azurelinux-logo-256.png

# Bootloader assets (Apple EFI / rEFInd)
Source20:       azurelinux.icns
Source21:       azurelinux.vol
Source22:       azurelinux-media.vol

# Plymouth theme assets
Source30:       azurelinux-watermark.png
Source31:       azurelinux-charge-logo.png

# Replace generic-logos as the system branding package
Provides:       system-logos = %{version}-%{release}
Provides:       redhat-logos = %{version}-%{release}
Provides:       gnome-logos = %{version}-%{release}
Obsoletes:      generic-logos < 19.0.0
Obsoletes:      redhat-logos
Conflicts:      fedora-logos
Conflicts:      generic-logos >= 19.0.0

Requires(post): coreutils
BuildArch:      noarch

%description
The azurelinux-icons package contains Azure Linux brand icons, logos,
and Plymouth boot splash assets. The Azure Linux icon package contains
images and files that may not be distributed with anything but
unmodified packages from Azure Linux.


%package httpd
Summary:        Azure Linux icons for httpd and web servers
Provides:       system-logos-httpd = %{version}-%{release}
Provides:       system-logos(httpd-logo-ng)
Obsoletes:      generic-logos-httpd < 19.0.0
Conflicts:      fedora-logos-httpd
Conflicts:      generic-logos-httpd >= 19.0.0
BuildArch:      noarch

%description httpd
The azurelinux-icons-httpd package contains the "Powered by Azure Linux"
image used by httpd, nginx, and other web servers. The azurelinux-icons-httpd
The Azure Linux icon package contains images and files that may not be
distributed with anything but unmodified packages from Azure Linux.

%prep
# Nothing to prep — all sources are pre-built assets

%build
# noarch, no compilation needed

%install
rm -rf %{buildroot}

# License
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}
install -p -m 644 %{SOURCE0} %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

# === Desktop Icons (hicolor theme) ===

# Scalable SVG
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 %{SOURCE10} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/azurelinux-logo-icon.svg
ln -s azurelinux-logo-icon.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/start-here.svg

# Sized PNGs into hicolor theme
for size in 16 22 24 32 48 96 256 ; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
done
install -p -m 644 %{SOURCE11} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/azurelinux-logo-icon.png
install -p -m 644 %{SOURCE12} %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/azurelinux-logo-icon.png
install -p -m 644 %{SOURCE13} %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/azurelinux-logo-icon.png
install -p -m 644 %{SOURCE14} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/azurelinux-logo-icon.png
install -p -m 644 %{SOURCE15} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/azurelinux-logo-icon.png
install -p -m 644 %{SOURCE16} %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/azurelinux-logo-icon.png
install -p -m 644 %{SOURCE17} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/azurelinux-logo-icon.png

# start-here symlinks (used by desktop environments for menu branding)
for size in 16 22 24 32 48 96 256 ; do
  ln -s azurelinux-logo-icon.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/start-here.png
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/places
  ln -s ../apps/start-here.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/places/start-here.png
done

# Scalable places symlink
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/places
ln -s ../apps/start-here.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/places/start-here.svg

# General pixmaps (for applications that look here)
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -p -m 644 %{SOURCE10} %{buildroot}%{_datadir}/pixmaps/azurelinux-logo.svg
install -p -m 644 %{SOURCE15} %{buildroot}%{_datadir}/pixmaps/azurelinux-logo.png

# Compatibility symlinks for consumers that expect generic-logos / fedora-logos filenames
# plymouth, sddm, gnome-control-center use system-logo-white.png
install -p -m 644 %{SOURCE15} %{buildroot}%{_datadir}/pixmaps/system-logo-white.png
# gdm uses fedora-gdm-logo.png
ln -s azurelinux-logo.png %{buildroot}%{_datadir}/pixmaps/fedora-gdm-logo.png
# general fedora-logo compat (wsl-setup references fedora-logo.ico path)
ln -s azurelinux-logo.png %{buildroot}%{_datadir}/pixmaps/fedora-logo.png
ln -s azurelinux-logo.png %{buildroot}%{_datadir}/pixmaps/fedora-logo-small.png
ln -s azurelinux-logo.svg %{buildroot}%{_datadir}/pixmaps/fedora-logo-sprite.svg

# Compatibility: fedora-logo-icon.svg in hicolor scalable (mate-desktop expects this)
ln -s azurelinux-logo-icon.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/fedora-logo-icon.svg

# Favicon symlink
mkdir -p %{buildroot}%{_sysconfdir}
ln -s %{_datadir}/icons/hicolor/16x16/apps/azurelinux-logo-icon.png %{buildroot}%{_sysconfdir}/favicon.png

# === Bootloader (Apple EFI / rEFInd) ===
# Installed as fedora.icns/fedora.vol for compatibility with bootloader tooling
mkdir -p %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 %{SOURCE20} %{buildroot}%{_datadir}/pixmaps/bootloader/fedora.icns
install -p -m 644 %{SOURCE21} %{buildroot}%{_datadir}/pixmaps/bootloader/fedora.vol
install -p -m 644 %{SOURCE22} %{buildroot}%{_datadir}/pixmaps/bootloader/fedora-media.vol

# === Plymouth boot splash ===
mkdir -p %{buildroot}%{_datadir}/plymouth/themes/charge
install -p -m 644 %{SOURCE31} %{buildroot}%{_datadir}/plymouth/themes/charge/logo.png
mkdir -p %{buildroot}%{_datadir}/plymouth/themes/spinner
install -p -m 644 %{SOURCE30} %{buildroot}%{_datadir}/plymouth/themes/spinner/watermark.png

# === httpd subpackage — "Powered by" image ===
# httpd expects poweredby.png at /usr/share/pixmaps/poweredby.png
install -p -m 644 %{SOURCE15} %{buildroot}%{_datadir}/pixmaps/poweredby.png

%post
touch --no-create %{_datadir}/icons/hicolor || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor || :
  if [ -x /usr/bin/gtk-update-icon-cache ]; then
    if [ -f %{_datadir}/icons/hicolor/index.theme ]; then
      gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
    fi
  fi
fi

%posttrans
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  if [ -f %{_datadir}/icons/hicolor/index.theme ]; then
    gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
fi

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%{_sysconfdir}/favicon.png
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/places/*
%{_datadir}/pixmaps/azurelinux-logo.svg
%{_datadir}/pixmaps/azurelinux-logo.png
%{_datadir}/pixmaps/system-logo-white.png
%{_datadir}/pixmaps/fedora-gdm-logo.png
%{_datadir}/pixmaps/fedora-logo.png
%{_datadir}/pixmaps/fedora-logo-small.png
%{_datadir}/pixmaps/fedora-logo-sprite.svg
%{_datadir}/pixmaps/bootloader/*
%{_datadir}/plymouth/themes/charge/logo.png
%{_datadir}/plymouth/themes/spinner/watermark.png

%files httpd
%license %{_datadir}/licenses/%{name}/LICENSE
%{_datadir}/pixmaps/poweredby.png

%changelog
