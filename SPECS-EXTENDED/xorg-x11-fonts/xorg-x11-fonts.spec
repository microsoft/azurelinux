Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global _catalogue /etc/X11/fontpath.d
# NOTE: Fonts strictly intended for X core fonts, should be installed into _x11fontdir.
%global _x11fontdir %{_datadir}/X11/fonts

Summary:    X.Org X11 fonts
Name:       xorg-x11-fonts
Version:    7.5
Release:    25%{?dist}
License:    MIT and Lucida and Public Domain
URL:        https://www.x.org

BuildArch:  noarch

Source0:    https://www.x.org/pub/individual/font/encodings-1.0.5.tar.bz2
Source1:    https://www.x.org/pub/individual/font/font-adobe-100dpi-1.0.3.tar.bz2
Source2:    https://www.x.org/pub/individual/font/font-adobe-75dpi-1.0.3.tar.bz2
Source3:    https://www.x.org/pub/individual/font/font-adobe-utopia-100dpi-1.0.4.tar.bz2
Source4:    https://www.x.org/pub/individual/font/font-adobe-utopia-75dpi-1.0.4.tar.bz2
Source5:    https://www.x.org/pub/individual/font/font-adobe-utopia-type1-1.0.4.tar.bz2
Source6:    https://www.x.org/pub/individual/font/font-alias-1.0.3.tar.bz2
Source7:    https://www.x.org/pub/individual/font/font-arabic-misc-1.0.3.tar.bz2
Source8:    https://www.x.org/pub/individual/font/font-bh-100dpi-1.0.3.tar.bz2
Source9:    https://www.x.org/pub/individual/font/font-bh-75dpi-1.0.3.tar.bz2
Source10:   https://www.x.org/pub/individual/font/font-bh-lucidatypewriter-100dpi-1.0.3.tar.bz2
Source11:   https://www.x.org/pub/individual/font/font-bh-lucidatypewriter-75dpi-1.0.3.tar.bz2
Source12:   https://www.x.org/pub/individual/font/font-bitstream-100dpi-1.0.3.tar.bz2
Source13:   https://www.x.org/pub/individual/font/font-bitstream-75dpi-1.0.3.tar.bz2
Source14:   https://www.x.org/pub/individual/font/font-bitstream-type1-1.0.3.tar.bz2
Source15:   https://www.x.org/pub/individual/font/font-cronyx-cyrillic-1.0.3.tar.bz2
Source16:   https://www.x.org/pub/individual/font/font-cursor-misc-1.0.3.tar.bz2
Source17:   https://www.x.org/pub/individual/font/font-daewoo-misc-1.0.3.tar.bz2
Source18:   https://www.x.org/pub/individual/font/font-dec-misc-1.0.3.tar.bz2
Source19:   https://www.x.org/pub/individual/font/font-isas-misc-1.0.3.tar.bz2
Source20:   https://www.x.org/pub/individual/font/font-jis-misc-1.0.3.tar.bz2
Source21:   https://www.x.org/pub/individual/font/font-micro-misc-1.0.3.tar.bz2
Source22:   https://www.x.org/pub/individual/font/font-misc-cyrillic-1.0.3.tar.bz2
Source23:   https://www.x.org/pub/individual/font/font-misc-ethiopic-1.0.3.tar.bz2
Source24:   https://www.x.org/pub/individual/font/font-misc-misc-1.1.2.tar.bz2
Source25:   https://www.x.org/pub/individual/font/font-mutt-misc-1.0.3.tar.bz2
Source26:   https://www.x.org/pub/individual/font/font-schumacher-misc-1.1.2.tar.bz2
Source27:   https://www.x.org/pub/individual/font/font-screen-cyrillic-1.0.4.tar.bz2
Source28:   https://www.x.org/pub/individual/font/font-sony-misc-1.0.3.tar.bz2
Source29:   https://www.x.org/pub/individual/font/font-sun-misc-1.0.3.tar.bz2
Source30:   https://www.x.org/pub/individual/font/font-winitzki-cyrillic-1.0.3.tar.bz2
Source31:   https://www.x.org/pub/individual/font/font-xfree86-type1-1.0.4.tar.bz2

# Luxi fonts are under a bad license
# https://www.x.org/pub/individual/font/font-bh-ttf-1.0.0.tar.bz2
# https://www.x.org/pub/individual/font/font-bh-type1-1.0.0.tar.bz2

# IBM refused to relicense ibm-type1 fonts with permission to modify
# https://www.x.org/pub/individual/font/font-ibm-type1-1.0.0.tar.bz2

# Meltho Syrian fonts (misc-meltho) have a bad license, upstream did not respond
# to request for relicensing
# https://www.x.org/pub/individual/font/font-misc-meltho-1.0.0.tar.bz2

BuildRequires:  bdftopcf
BuildRequires:  font-util >= 1.1.0
BuildRequires:  pkgconfig(xorg-macros) >= 1.3
BuildRequires:  ucs2any

%description
X.Org X Window System fonts.

%package misc
Summary:            misc bitmap fonts for the X Window System
Requires(post):     fontconfig
Requires(post):     mkfontdir
Requires(postun):   fontconfig
Requires(postun):   mkfontdir
# Still required by xfig-common, xosd, xtide
Obsoletes:          xorg-x11-fonts-base <= %{version}-%{release}
Provides:           xorg-x11-fonts-base = %{version}-%{release}

%description misc
This package contains misc bitmap Chinese, Japanese, Korean, Indic, and Arabic
fonts for use with X Window System.

%package Type1
Summary:            Type1 fonts provided by the X Window System
Requires(post):     fontconfig
Requires(post):     mkfontdir
Requires(post):     ttmkfdir
Requires(postun):   fontconfig
Requires(postun):   mkfontdir
Requires(postun):   ttmkfdir

%description Type1
A collection of Type1 fonts which are part of the core X Window System
distribution.

%package ethiopic
Summary:            Ethiopic fonts
Requires(post):     fontconfig
Requires(post):     mkfontdir
Requires(post):     mkfontscale
Requires(post):     ttmkfdir
Requires(postun):   fontconfig
Requires(postun):   mkfontdir
Requires(postun):   mkfontscale
Requires(postun):   ttmkfdir

%description ethiopic
Ethiopic fonts which are part of the core X Window System distribution.

%package 75dpi
Summary:            A set of 75dpi resolution fonts for the X Window System
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description 75dpi
A set of 75 dpi fonts used by the X window system.

%package 100dpi
Summary:            A set of 100dpi resolution fonts for the X Window System
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description 100dpi
A set of 100 dpi fonts used by the X window system.

%package ISO8859-1-75dpi
Summary:            A set of 75dpi ISO-8859-1 fonts for X
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description ISO8859-1-75dpi
Contains a set of 75dpi fonts for ISO-8859-1.

%package ISO8859-1-100dpi
Summary:            A set of 100dpi ISO-8859-1 fonts for X
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description ISO8859-1-100dpi
Contains a set of 100dpi fonts for ISO-8859-1.

%package ISO8859-2-75dpi
Summary:            A set of 75dpi Central European language fonts for X
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description ISO8859-2-75dpi
Contains a set of 75dpi fonts for Central European languages.

%package ISO8859-2-100dpi
Summary:            A set of 100dpi Central European language fonts for X
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description ISO8859-2-100dpi
Contains a set of 100dpi fonts for Central European languages.

%package ISO8859-9-75dpi
Summary:            ISO8859-9-75dpi fonts
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description ISO8859-9-75dpi
Contains a set of 75dpi fonts for the Turkish language.

%package ISO8859-9-100dpi
Summary:            ISO8859-9-100dpi fonts
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description ISO8859-9-100dpi
Contains a set of 100dpi fonts for the Turkish language.

%package ISO8859-14-75dpi
Summary:            ISO8859-14-75dpi fonts
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description ISO8859-14-75dpi
Contains a set of 75dpi fonts in the ISO8859-14 encoding which provide Welsh
support.

%package ISO8859-14-100dpi
Summary:            ISO8859-14-100dpi fonts
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description ISO8859-14-100dpi
Contains a set of 100dpi fonts in the ISO8859-14 encoding which provide Welsh
support.

%package ISO8859-15-75dpi
Summary:            ISO8859-15-75dpi fonts
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description ISO8859-15-75dpi
Contains a set of 75dpi fonts in the ISO8859-15 encoding which provide Euro
support.

%package ISO8859-15-100dpi
Summary:            ISO8859-15-100dpi fonts
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description ISO8859-15-100dpi
Contains a set of 100dpi fonts in the ISO8859-15 encoding which provide Euro
support.

%package cyrillic
Summary:            Cyrillic fonts for X
Requires(post):     mkfontdir
Requires(postun):   mkfontdir

%description cyrillic
Contains a set of Cyrillic fonts.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -a15 -a16 -a17 -a18 -a19 -a20 -a21 -a22 -a23 -a24 -a25 -a26 -a27 -a28 -a29 -a30 -a31

%build
# Build all apps
{
    for app in * ; do
        pushd $app
            autoreconf -vif
            case $app in
                font-adobe-100dpi-*|font-adobe-75dpi-*|font-adobe-utopia-100dpi-*|font-adobe-utopia-75dpi-*|font-bh-*)
                    %configure --with-fontrootdir=%{_x11fontdir} \
                        --disable-iso8859-3 \
                        --disable-iso8859-4 \
                        --disable-iso8859-10 \
                        --disable-iso8859-13
                    ;;
                font-misc-misc-*|font-schumacher-misc-*)
                    %configure --with-fontrootdir=%{_x11fontdir} \
                        --disable-iso8859-3 \
                        --disable-iso8859-4 \
                        --disable-iso8859-10 \
                        --disable-iso8859-11 \
                        --disable-iso8859-13 \
                        --disable-iso8859-16
                    ;;
                *)
                    %configure --with-fontrootdir=%{_x11fontdir}
                    ;;
            esac
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

# Install catalogue symlinks
mkdir -p $RPM_BUILD_ROOT%{_catalogue}
for f in misc:unscaled:pri=10 75dpi:unscaled:pri=20 100dpi:unscaled:pri=30 Type1 TTF OTF cyrillic; do
    ln -fs %{_x11fontdir}/${f%%%%:*} $RPM_BUILD_ROOT%{_catalogue}/xorg-x11-fonts-$f
done

# Create fake ghost files for file manifests.
{
    # Make ghost fonts.alias, fonts.dir, encodings.dir files
    FONTDIR=$RPM_BUILD_ROOT%{_x11fontdir}
    # Create fake %%ghost fonts.alias
    for subdir in TTF OTF ; do
        touch $FONTDIR/$subdir/fonts.{alias,scale}
        chmod 0644 $FONTDIR/$subdir/fonts.{alias,scale}
    done
    # Create fake ghost encodings.dir, fonts.dir, fonts.scale, fonts.cache-*
    for subdir in Type1 TTF OTF 100dpi 75dpi cyrillic misc ; do
        rm -f $FONTDIR/$subdir/{encodings,fonts}.dir
        touch $FONTDIR/$subdir/{encodings,fonts}.dir
        chmod 0644 $FONTDIR/$subdir/{encodings,fonts}.dir
        touch $FONTDIR/$subdir/fonts.scale
        chmod 0644 $FONTDIR/$subdir/fonts.scale

        # Create bogus fonts.cache-* files
        # Create somewhat future-proofed ghosted fonts.cache-* files so that
        # the font packages own these files.
        for fcver in $(seq 1 9) ; do
            touch $FONTDIR/$subdir/fonts.cache-$fcver
            chmod 0644 $FONTDIR/$subdir/fonts.cache-$fcver
        done
    done
}


# xorg-x11-fonts-update-dirs is provided by xorg-x11-font-utils to deduplicate
# stuff run in %%post

%post misc
{
# Only run fc-cache in the Type1 dir, gzipped pcf's take forever
  xorg-x11-fonts-update-dirs --skip-fontscale %{_x11fontdir}/misc
}

%postun misc
{
  # Rebuild fonts.dir when uninstalling package. (exclude the local, CID dirs)
  if [ "$1" = "0" -a -d %{_x11fontdir}/misc ]; then
    xorg-x11-fonts-update-dirs --skip-fontscale %{_x11fontdir}/misc
  fi
}

%post Type1
{
  xorg-x11-fonts-update-dirs %{_x11fontdir}/Type1
} 

%postun Type1
{
  FONTDIR=%{_x11fontdir}/Type1
  if [ "$1" = "0" -a -d $FONTDIR ]; then
    xorg-x11-fonts-update-dirs $FONTDIR
  fi
}

%post ethiopic
{
  xorg-x11-fonts-update-dirs --skip-fontscale --need-ttmkfdir %{_x11fontdir}/TTF
  xorg-x11-fonts-update-dirs %{_x11fontdir}/OTF
}

%postun ethiopic
{
  FONTDIR=%{_x11fontdir}/TTF
  if [ "$1" = "0" -a -d $FONTDIR ]; then
    xorg-x11-fonts-update-dirs --skip-fontscale --need-ttmkfdir $FONTDIR
  fi
  FONTDIR=%{_x11fontdir}/OTF
  if [ "$1" = "0" -a -d $FONTDIR ]; then
    xorg-x11-fonts-update-dirs $FONTDIR
  fi
}

%post 75dpi
mkfontdir %{_x11fontdir}/75dpi

%post 100dpi
mkfontdir %{_x11fontdir}/100dpi

%post ISO8859-1-75dpi
mkfontdir %{_x11fontdir}/75dpi

%post ISO8859-1-100dpi
mkfontdir %{_x11fontdir}/100dpi

%post ISO8859-2-75dpi
mkfontdir %{_x11fontdir}/75dpi

%post ISO8859-2-100dpi
mkfontdir %{_x11fontdir}/100dpi

%post ISO8859-9-75dpi
mkfontdir %{_x11fontdir}/75dpi

%post ISO8859-9-100dpi
mkfontdir %{_x11fontdir}/100dpi

%post ISO8859-14-75dpi
mkfontdir %{_x11fontdir}/75dpi

%post ISO8859-14-100dpi
mkfontdir %{_x11fontdir}/100dpi

%post ISO8859-15-75dpi
mkfontdir %{_x11fontdir}/75dpi

%post ISO8859-15-100dpi
mkfontdir %{_x11fontdir}/100dpi

%post cyrillic
mkfontdir %{_x11fontdir}/cyrillic

%postun 75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun 100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun ISO8859-1-75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun ISO8859-1-100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun ISO8859-2-75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun ISO8859-2-100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi  ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun ISO8859-9-75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun ISO8859-9-100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi  ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun ISO8859-14-75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun ISO8859-14-100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi  ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun ISO8859-15-75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun ISO8859-15-100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi  ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun cyrillic
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/cyrillic ]; then
    mkfontdir %{_x11fontdir}/cyrillic
  fi
}


%files misc
%{_catalogue}/xorg-x11-fonts-misc:unscaled:pri=10
%dir %{_x11fontdir}/misc
%{_x11fontdir}/misc/*
%dir %{_x11fontdir}/encodings
%dir %{_x11fontdir}/encodings/large
%{_x11fontdir}/encodings/*.enc.gz
%ghost %verify(not md5 size mtime) %{_x11fontdir}/encodings/encodings.dir
%{_x11fontdir}/encodings/large/*.enc.gz
%ghost %verify(not md5 size mtime) %{_x11fontdir}/encodings/large/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.cache-*

%files ethiopic
%{_catalogue}/xorg-x11-fonts-TTF
%{_catalogue}/xorg-x11-fonts-OTF
# TTF fonts
%dir %{_x11fontdir}/TTF
# font-misc-ethiopic
%{_x11fontdir}/TTF/GohaTibebZemen.ttf
%ghost %verify(not md5 size mtime) %{_x11fontdir}/TTF/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/TTF/fonts.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/TTF/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/TTF/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/TTF/fonts.cache-*
# OTF fonts
%dir %{_x11fontdir}/OTF
%{_x11fontdir}/OTF/GohaTibebZemen.otf
%ghost %verify(not md5 size mtime) %{_x11fontdir}/OTF/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/OTF/fonts.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/OTF/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/OTF/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/OTF/fonts.cache-*

%files 75dpi
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??.pcf*
%{_x11fontdir}/75dpi/courBO??.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??.pcf*
%{_x11fontdir}/75dpi/helvBO??.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??.pcf*
%{_x11fontdir}/75dpi/ncenBI??.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??.pcf*
%{_x11fontdir}/75dpi/timBI??.pcf*
%{_x11fontdir}/75dpi/symb??.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??.pcf*
%{_x11fontdir}/75dpi/UTRG__??.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??.pcf*
%{_x11fontdir}/75dpi/lubBI??.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??.pcf*
# font-bitstream-75dpi
%{_x11fontdir}/75dpi/char[BIR]??.pcf*
%{_x11fontdir}/75dpi/charBI??.pcf*
%{_x11fontdir}/75dpi/tech14.pcf*
%{_x11fontdir}/75dpi/techB14.pcf*
%{_x11fontdir}/75dpi/term14.pcf*
%{_x11fontdir}/75dpi/termB14.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files 100dpi
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??.pcf*
%{_x11fontdir}/100dpi/courBO??.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??.pcf*
%{_x11fontdir}/100dpi/helvBO??.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??.pcf*
%{_x11fontdir}/100dpi/ncenBI??.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??.pcf*
%{_x11fontdir}/100dpi/timBI??.pcf*
%{_x11fontdir}/100dpi/symb??.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??.pcf*
%{_x11fontdir}/100dpi/UTRG__??.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??.pcf*
%{_x11fontdir}/100dpi/lubBI??.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??.pcf*
# font-bitstream-100dpi
%{_x11fontdir}/100dpi/char[BIR]??.pcf*
%{_x11fontdir}/100dpi/charBI??.pcf*
%{_x11fontdir}/100dpi/tech14.pcf*
%{_x11fontdir}/100dpi/techB14.pcf*
%{_x11fontdir}/100dpi/term14.pcf*
%{_x11fontdir}/100dpi/termB14.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files ISO8859-1-75dpi
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/courBO??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/helvBO??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/ncenBI??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/timBI??-ISO8859-1.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/UTRG__??-ISO8859-1.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/lubBI??-ISO8859-1.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??-ISO8859-1.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files ISO8859-1-100dpi
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/courBO??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/helvBO??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/ncenBI??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/timBI??-ISO8859-1.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/UTRG__??-ISO8859-1.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/lubBI??-ISO8859-1.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??-ISO8859-1.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files ISO8859-2-75dpi
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/courBO??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/helvBO??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/ncenBI??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/timBI??-ISO8859-2.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/UTRG__??-ISO8859-2.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/lubBI??-ISO8859-2.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??-ISO8859-2.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files ISO8859-2-100dpi
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/courBO??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/helvBO??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/ncenBI??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/timBI??-ISO8859-2.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/UTRG__??-ISO8859-2.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/lubBI??-ISO8859-2.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??-ISO8859-2.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files ISO8859-9-75dpi
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/courBO??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/helvBO??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/ncenBI??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/timBI??-ISO8859-9.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/UTRG__??-ISO8859-9.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/lubBI??-ISO8859-9.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??-ISO8859-9.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files ISO8859-9-100dpi
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/courBO??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/helvBO??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/ncenBI??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/timBI??-ISO8859-9.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/UTRG__??-ISO8859-9.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/lubBI??-ISO8859-9.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??-ISO8859-9.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files ISO8859-14-75dpi
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/courBO??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/helvBO??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/ncenBI??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/timBI??-ISO8859-14.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/UTRG__??-ISO8859-14.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/lubBI??-ISO8859-14.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??-ISO8859-14.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files ISO8859-14-100dpi
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/courBO??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/helvBO??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/ncenBI??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/timBI??-ISO8859-14.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/UTRG__??-ISO8859-14.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/lubBI??-ISO8859-14.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??-ISO8859-14.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files ISO8859-15-75dpi
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/courBO??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/helvBO??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/ncenBI??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/timBI??-ISO8859-15.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/UTRG__??-ISO8859-15.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/lubBI??-ISO8859-15.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??-ISO8859-15.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files ISO8859-15-100dpi
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/courBO??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/helvBO??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/ncenBI??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/timBI??-ISO8859-15.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/UTRG__??-ISO8859-15.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/lubBI??-ISO8859-15.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??-ISO8859-15.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files Type1
%{_catalogue}/xorg-x11-fonts-Type1
%dir %{_x11fontdir}/Type1
# font-adobe-utopia-type1
%{_x11fontdir}/Type1/UT??____.[ap]f[ma]
# font-bitstream-type1
%{_x11fontdir}/Type1/c0???bt_.[ap]f[mb]
# font-ibm-type1
# Pulled for licensing reasons (see bz 317641)
# %%{_x11fontdir}/Type1/cour*.afm
# %%{_x11fontdir}/Type1/cour*.pfa
#font-xfree86-type1
%{_x11fontdir}/Type1/cursor.pfa
%ghost %verify(not md5 size mtime) %{_x11fontdir}/Type1/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/Type1/fonts.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/Type1/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/Type1/fonts.cache-*

%files cyrillic
%{_catalogue}/xorg-x11-fonts-cyrillic
%dir %{_x11fontdir}/cyrillic
# font-cronyx-cyrillic
%{_x11fontdir}/cyrillic/crox[1-6]*.pcf*
%{_x11fontdir}/cyrillic/koi10x16b.pcf*
%{_x11fontdir}/cyrillic/koi10x20.pcf*
%{_x11fontdir}/cyrillic/koi6x10.pcf*
%{_x11fontdir}/cyrillic/koinil2.pcf*
# font-misc-cyrillic
%{_x11fontdir}/cyrillic/koi12x24*.pcf*
%{_x11fontdir}/cyrillic/koi6x13.pcf*
%{_x11fontdir}/cyrillic/koi6x13b.pcf*
%{_x11fontdir}/cyrillic/koi6x9.pcf*
%{_x11fontdir}/cyrillic/koi[5789]x*.pcf*
# font-screen-cyrillic
%{_x11fontdir}/cyrillic/screen8x16*.pcf*
# font-winitzki-cyrillic
%{_x11fontdir}/cyrillic/proof9x16.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/cyrillic/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/cyrillic/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/cyrillic/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/cyrillic/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/cyrillic/fonts.cache-*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.5-25
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Adam Jackson <ajax@redhat.com> - 7.5-22
- encodings 1.0.5
- Change to HTTPS URLs

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 10 2014 Simone Caronni <negativo17@gmail.com> - 7.5-14
- Update build requirements.

* Mon Nov 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 7.5-13
- Fix requires on ttmkfdir (#1162089)

* Sun Nov 09 2014 Simone Caronni <negativo17@gmail.com> - 7.5-12
- Clean up SPEC file, remove obsolete tags, fix all rpmlint warnings.
- Rework build/install section to be like other xorg packages.
- Remove all obsolete provides/obsoletes/conflicts.
- Simplify build requirements.
- Simplify build, it has not changed since 2008.

* Thu Oct 23 2014 Hans de Goede <hdegoede@redhat.com> - 7.5-11
- Update most fonts:
   -encodings-1.0.4
   -font-adobe-100dpi-1.0.3
   -font-adobe-75dpi-1.0.3
   -font-adobe-utopia-100dpi-1.0.4
   -font-adobe-utopia-75dpi-1.0.4
   -font-adobe-utopia-type1-1.0.4
   -font-arabic-misc-1.0.3
   -font-bh-100dpi-1.0.3
   -font-bh-75dpi-1.0.3
   -font-bh-lucidatypewriter-100dpi-1.0.3
   -font-bh-lucidatypewriter-75dpi-1.0.3
   -font-bitstream-100dpi-1.0.3
   -font-bitstream-75dpi-1.0.3
   -font-bitstream-type1-1.0.3
   -font-cronyx-cyrillic-1.0.3
   -font-cursor-misc-1.0.3
   -font-daewoo-misc-1.0.3
   -font-dec-misc-1.0.3
   -font-isas-misc-1.0.3
   -font-jis-misc-1.0.3
   -font-micro-misc-1.0.3
   -font-misc-cyrillic-1.0.3
   -font-misc-ethiopic-1.0.3
   -font-misc-misc-1.1.2
   -font-mutt-misc-1.0.3
   -font-schumacher-misc-1.1.2
   -font-screen-cyrillic-1.0.4
   -font-sony-misc-1.0.3
   -font-sun-misc-1.0.3
   -font-winitzki-cyrillic-1.0.3
   -font-xfree86-type1-1.0.4
- Fix a bug in jisx0201.1976-0.enc (#1009350)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 7.5-8
- autoreconf for aarch64

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 28 2011 Matěj Cepl <mcepl@redhat.com> - 7.5-4
- Fix call of xorg-x11-fonts-update-dirs (#726267)

* Fri Nov 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-3
- Rely on a script provided in xorg-x11-font-utils for mkfontscale and
  friends (#634039)

* Fri Nov 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-2
- This time with tarballs

* Fri Nov 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-1
- Update fonts to latest upstream releases

* Tue Jun 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.2-11
- Require xorg-x11-font-utils >= 7.2-11 for font-utils 1.1.0
- Fix bashism in spec file (&>)
- Remove perl hack for DEFAULT_FONTS_DIR, fixed upstream 
- Remove perl and autoconf requirement.
- Create %%ghost files {misc|705dpi|...}/fonts.scale.
- Drop fontdir alias patches
- Update a few fonts (well, all of them)
    - encodings-1.0.3
    - font-adobe-100dpi-1.0.1
    - font-adobe-75dpi-1.0.1
    - font-adobe-utopia-100dpi-1.0.2
    - font-adobe-utopia-75dpi-1.0.2
    - font-adobe-utopia-type1-1.0.2
    - font-alias-1.0.2
    - font-arabic-misc-1.0.1
    - font-bh-100dpi-1.0.1
    - font-bh-75dpi-1.0.1
    - font-bh-lucidatypewriter-100dpi-1.0.1
    - font-bh-lucidatypewriter-75dpi-1.0.1
    - font-bitstream-100dpi-1.0.1
    - font-bitstream-75dpi-1.0.1
    - font-bitstream-type1-1.0.1
    - font-cronyx-cyrillic-1.0.1
    - font-cursor-misc-1.0.1
    - font-daewoo-misc-1.0.1
    - font-dec-misc-1.0.1
    - font-isas-misc-1.0.1
    - font-jis-misc-1.0.1
    - font-micro-misc-1.0.1
    - font-misc-cyrillic-1.0.1
    - font-misc-ethiopic-1.0.1
    - font-misc-misc-1.1.0
    - font-mutt-misc-1.0.1
    - font-schumacher-misc-1.1.0
    - font-screen-cyrillic-1.0.2
    - font-sony-misc-1.0.1
    - font-sun-misc-1.0.1
    - font-winitzki-cyrillic-1.0.1
    - font-xfree86-type1-1.0.2

* Fri Mar 05 2010 Matěj Cepl <mcepl@redhat.com> - 7.2-10
- Fixed bad directory ownership of /etc//X11/fontpath.d
