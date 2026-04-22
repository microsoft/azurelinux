# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# Important notes regarding the package:
# ======================================
# This package contains 35 fonts defined as PostScript Level 2 Core Font Set:
# > https://en.wikipedia.org/wiki/PostScript_fonts#Core_Font_Set
#
# This package is the replacement for previous 'urw-fonts' package (obsolete now).
#
# However, there are currently several issues that needed to be adressed:
# 1) This font set is owned by company (URW)++ [https://www.urwpp.de/en/], but
#    the company Artifex Software [http://www.artifex.com/] has negotiated with
#    (URW)++ the Open Source release of several fonts that (URW)++ owns, which
#    can be used as Level 2 Core Font Set.
#
#    Artifex Software is the owner/creator of Ghostscript software, and they use
#    those fonts as part of Ghostscript's resources.
#
#    However, (URW++) company does not provide any way to download those fonts.
#    So right now, we are using the fonts which Artifex Software company uses
#    in Ghostscript, and made available. They do not officially provide them,
#    but they have become the 'de facto' standard across Linux distributions.
#
#    Therefore, from now on, I will refer to Artifex Software as to 'upstream'.
#
# 2) Upstream has its own git repository for Core Font Set Level 2 sources:
#    > https://github.com/ArtifexSoftware/urw-base35-fonts
#
#    Here you can find 4 types of files (regarding the fonts):
#    *.t1  - https://en.wikipedia.org/wiki/PostScript_fonts#Type_1
#    *.afm - https://de.wikipedia.org/wiki/Adobe_Font_Metrics
#    *.ttf - https://en.wikipedia.org/wiki/TrueType
#    *.otf - https://en.wikipedia.org/wiki/OpenType
#
#    According to upstream, Ghostscript needs only Type 1 fonts to work properly.
#    It can use TTF or OTF fonts as substitutions as well in case the Type 1
#    fonts are missing, but the substitution is not (and can't be) guaranteed to
#    be absolutely flawless, unless the fonts use the CFF outlines:
#    > https://en.wikipedia.org/wiki/PostScript_fonts#Compact_Font_Format
#
#    And even though the OTF font files have CFF outlines embedded inside them,
#    those OTF fonts still cause problems when they are used with Ghostscript's
#    'pdfwrite' device as substitutions. This can break printing or conversions
#    for many users out there using Ghostscript. At the moment, upstream does
#    not have reason/motivation to fix the 'pdfwrite' device in the near future.
#
#    The AFM (Adobe Font Metrics) are useful for layout purposes of other
#    applications, and they contain general font information and font metrics.
#    These AFM files were distributed in the previous 'urw-fonts' package, so in
#    order to avoid possible regressions in the future, we need to continue
#    distributing them.
#
#    However, distributing AFM files would not be possible if we would create
#    this package from Ghostscript source package only. It does not contain
#    these AFM files, because as stated above - Ghostscript requires only T1
#    fonts. Therefore, we're using the archive with fonts provided from upstream.
#
#
# 3) The previous package 'urw-fonts' shipped the fonts in different format:
#    *.pfb - Printer Font Binary (compressed Type 1 fonts, which require an
#            8-bit transmission method)
#    *.pfm - Printer Font Metrics (same as *.afm files according to upstream)
#
#    These formats were basically replaced with T1 and AFM formats, currently
#    used by upstream.
#
# 4) (URW)++ does not have any sane versioning procedure. After reaching
#    version 1.10, they returned to version 1.00. That is the reason why
#    upstream switched to using git snapshot dates for versioning, and we
#    are sticking to that after discussion at fedora-devel mailing list.
#
# 5) The package scheme is this:
#
#    * urw-base35-fonts        -- Metapackage which does not contain anything,
#                                 but requires all its font subpackages. This
#                                 is a wrapper package to ease-up installation
#                                 of all fonts.
#
#    * urw-base35-fonts-common -- Package that contains only the license file,
#                                 to avoid duplication of it and to make the
#                                 font packages size smaller.
#
#    * urw-base35-[***]-fonts  -- Subpackage of base35 fonts, containing only
#                                 one font family, as required by FPG.
#
#    * urw-base35-fonts-devel  -- Devel subpackage that provides useful RPM
#                                 macro(s), so other packages can more easily
#                                 build against base35 fonts.
#
#    ==========================================================================
#
#    urw-base35-fonts ----- urw-base35-fonts-common
#                       |             |
#                       |             |
#                       \-- urw-base35-[***]-fonts
#
#    ==========================================================================
#
#    NOTE: Fedora Packaging Guidelines (FPG) requires to use OTF or TTF format:
#          https://fedoraproject.org/wiki/Choosing_the_right_font_format_to_package
#
#          However, there are several packages in Fedora that still hadn't been
#          updated to work with OTF/TTF formats, and thus still require the
#          Type1 font format to work correctly. These packages include e.g.:
#           * ghostscript
#           * ImageMagick
#           * hylafax+
#
#          On the other hand, more and more software (e.g. LibreOffice) is
#          moving away from Type1 format completely and dropping its support.
#
#          As a result, we currently need to ship both OTF and Type1/AFM formats.
#          In case all the packages depending on base35 fonts will finally start
#          supporting the OTF, then we will make complete switch to OTF only.
#
#    ==========================================================================

# GLOBAL MACROS:
# --------------
%global fontname            urw-base35
%global fontconfig_prio     61
%global urw_fonts_vers      3:2.4-25
%global legacydir           %{_datadir}/X11/fonts/urw-fonts


# By redefining the '_docdir_fmt' macro we override the default location of
# documentation or license files. Instead of them being located in
# 'urw-base35-fonts-common', they are located in 'urw-base35-fonts' folder.
%global _docdir_fmt         %{name}


%global common_desc \
The Level 2 Core Font Set is a PostScript specification of 35 base fonts that \
can be used with any PostScript file. These fonts are provided freely \
by (URW)++ company, and are mainly utilized by applications using Ghostscript.

# =============================================================================

Name:             %{fontname}-fonts
Summary:          Core Font Set containing 35 freely distributable fonts from (URW)++
Version:          20200910
Release: 27%{?dist}

# NOTE: (URW)++ holds the copyright, but Artifex Software has obtained rights to
#       release these fonts under GNU Affero General Public License (version 3).
#       Also contains subpackage legacy with older version of the fonts (with GPLv2.0+ license) still needed by a few applications.
License:          AGPL-3.0-only AND GPL-2.0-or-later

URL:              https://www.urwpp.de/en/
Source:           https://github.com/ArtifexSoftware/urw-base35-fonts/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:          urw-fonts-1.0.7pre44.tar.bz2

BuildArch:        noarch

Patch01:          urw-base35-fonts-20200910-dont-config-d050000l-as-fantasy-font.patch
Patch02:					urw-base35-fonts-20200910-Nimbus-Mono-substitution.patch
Patch03:					urw-base35-fonts-20200910-add-alias-to-Century.patch

BuildRequires:    fontpackages-devel
BuildRequires:    libappstream-glib

BuildRequires:    git
BuildRequires:    sed

# ---------------

Provides:         urw-fonts = %{urw_fonts_vers}
Obsoletes:        urw-fonts < %{urw_fonts_vers}

# This is metapackage for installation all font subpackages, require them:
Requires:         %{name}-common = %{version}-%{release}
Requires:         %{fontname}-bookman-fonts
Requires:         %{fontname}-c059-fonts
Requires:         %{fontname}-d050000l-fonts
Requires:         %{fontname}-gothic-fonts
Requires:         %{fontname}-nimbus-mono-ps-fonts
Requires:         %{fontname}-nimbus-roman-fonts
Requires:         %{fontname}-nimbus-sans-fonts
Requires:         %{fontname}-p052-fonts
Requires:         %{fontname}-standard-symbols-ps-fonts
Requires:         %{fontname}-z003-fonts

# Upstream patches -- official upstream patches released by upstream since the
# ----------------    last rebase that are necessary for any reason:

%description
%{common_desc}

This meta-package will install all the 35 fonts from the %{name}.

# =============================================================================

# Macro for creating a subpackage for a given font family.
#
# USAGE: font_subpkg [-c] [-o old_subpackage_name]
#  -c    Make this subpackage conflict with the previous versions of URW fonts.
#  -o    Marks this supbackage to obsolete (& provide) other previous subpackage.
%define fontfamily_subpkg(co:)                                                 \
                                                                               \
%define ff_filename   %(echo %{*} | tr --delete " ")                           \
%define subpkg_name   %(echo %{*} | tr "A-Z " "a-z-" | sed -e 's/urw-//')      \
                                                                               \
%package -n       %{fontname}-%{subpkg_name}-fonts                             \
Summary:          %{*} font family [part of Level 2 Core Font Set]             \
Requires:         %{name}-common = %{version}-%{release}                       \
                                                                               \
Requires(post):   coreutils                                                    \
                                                                               \
                                                                               \
# The section below will be only added if the '-c' option was specified:       \
%{-c:                                                                          \
Conflicts:        urw-fonts < %{urw_fonts_vers} }                              \
                                                                               \
%description -n   %{fontname}-%{subpkg_name}-fonts                             \
This package contains %{*} font family,                                        \
which is part of Level 2 Core Font Set.                                        \
                                                                               \
%{common_desc}                                                                 \
                                                                               \
# Remove after C11S release and F43 EOL                                        \
%postun -n %{fontname}-%{subpkg_name}-fonts                                    \
if [ $1 -gt 0 ]                                                                \
then                                                                           \
  rm -rf /var/lib/rpm-state/urw-base35-fonts || :                              \
fi                                                                             \
                                                                               \
# Remove after C11S release and F43 EOL                                        \
%posttrans -n %{fontname}-%{subpkg_name}-fonts                                 \
if [ $1 -gt 1 ]                                                                \
then                                                                           \
  rm -rf /var/lib/rpm-state/urw-base35-fonts || :                              \
fi                                                                             \
                                                                               \
%files -n %{fontname}-%{subpkg_name}-fonts                                     \
%{_fontdir}/%{ff_filename}*.t1                                                 \
%{_fontdir}/%{ff_filename}*.afm                                                \
%{_fontdir}/%{ff_filename}*.otf                                                \
%{_datadir}/appdata/de.urwpp.%{ff_filename}.metainfo.xml                       \
%{_datadir}/fontconfig/conf.avail/%{fontconfig_prio}-urw-%{subpkg_name}.conf   \
%{_sysconfdir}/fonts/conf.d/%{fontconfig_prio}-urw-%{subpkg_name}.conf         \

# =============================================================================

%package common
Summary:          Common files of the (URW)++ Level 2 Core Font Set
Requires:         filesystem
Requires:         fontpackages-filesystem

%description common
%{common_desc}

This package contains the necessary license files for this font set.

# ---------------

%package devel
Summary:          RPM macros related to (URW)++ Level 2 Core Font Set
Requires:         %{name} = %{version}-%{release}

%description devel
%{common_desc}

This package is useful for development purposes only. It installs RPM
macros useful for building packages against %{name},
as well as all the fonts contained in this font set.

# ---------------

%package legacy
Summary:          Legacy version of (URW)++ Level 2 Core Font Set
Requires(post):   mkfontscale mkfontdir
Requires(postun): mkfontscale mkfontdir

%description legacy
%{common_desc}

This package provides previous (legacy) versions of these fonts, which are still
required by some of the software, like e.g. xfig, X11, etc.

# =============================================================================
# NOTE: When making an update, make sure to check if any font families were
#       added/removed. We always need to pack all the fonts into subpackages.
# =============================================================================

%fontfamily_subpkg C059
%fontfamily_subpkg D050000L
%fontfamily_subpkg Nimbus Mono PS -c
%fontfamily_subpkg Nimbus Roman -c
%fontfamily_subpkg Nimbus Sans -c
%fontfamily_subpkg P052
%fontfamily_subpkg Standard Symbols PS -c
%fontfamily_subpkg URW Bookman -c
%fontfamily_subpkg URW Gothic -c
%fontfamily_subpkg Z003

# =============================================================================

# We need to ship the legacy fonts for now as well (BZ #1551219):
%prep
%autosetup -N -S git

mkdir -p legacy
tar --directory=legacy/ -xf %{SOURCE1}
rm -f legacy/ChangeLog legacy/README* legacy/fonts*

# Amend all the files to the initial commit, and patch the sources:
git add --all --force
git commit --all --amend --no-edit > /dev/null
%autopatch -p1

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0755 -d %{buildroot}%{_datadir}/appdata
install -m 0755 -d %{buildroot}%{_datadir}/fontconfig/conf.avail
install -m 0755 -d %{buildroot}%{_sysconfdir}/fonts/conf.d
install -m 0755 -d %{buildroot}%{legacydir}
install -m 0755 -d %{buildroot}%{_datadir}/licenses/urw-fonts

install -m 0644 -p fonts/*.t1  %{buildroot}%{_fontdir}
install -m 0644 -p fonts/*.afm %{buildroot}%{_fontdir}
install -m 0644 -p fonts/*.otf %{buildroot}%{_fontdir}
install -m 0644 -p legacy/*.afm legacy/*.pfm legacy/*.pfb %{buildroot}%{legacydir}
install -m 0644 -p legacy/COPYING %{buildroot}%{_datadir}/licenses/urw-fonts

install -m 0644 -p appstream/*.metainfo.xml %{buildroot}%{_datadir}/appdata/

# Install the fontconfig files with correct priority for our distribution:
for file in fontconfig/*.conf; do
  DISTRO_FILENAME="%{fontconfig_prio}-$(basename $file)"
  install -m 0644 -p $file %{buildroot}%{_datadir}/fontconfig/conf.avail/$DISTRO_FILENAME
  ln -sf %{_datadir}/fontconfig/conf.avail/$DISTRO_FILENAME %{buildroot}%{_sysconfdir}/fonts/conf.d/$DISTRO_FILENAME
done

# Some of the fontconfig files are not to be shipped:
#  * urw-fallback-specifics.conf - these mappings are already provided by fontconfig
#  * urw-fallback-generics.conf - no use-cases for this as far as we know
rm -f %{buildroot}%{_datadir}/fontconfig/conf.avail/%{fontconfig_prio}-urw-fallback-{specifics,generics}.conf
rm -f %{buildroot}%{_sysconfdir}/fonts/conf.d/%{fontconfig_prio}-urw-fallback-{specifics,generics}.conf

# We need to touch these files -- otherwise running 'rpm --setperms' would
# result in these files having incorrect permissions like this: [-------.]
#touch %{buildroot}%{_fontdir}/fonts.dir
#touch %{buildroot}%{_fontdir}/fonts.scale
touch %{buildroot}%{legacydir}/fonts.dir
touch %{buildroot}%{legacydir}/fonts.scale

# Install the symlink for the X11 Logical Font Description to actually work:
install -m 0755 -d %{buildroot}%{_sysconfdir}/X11/fontpath.d
#ln -sf %{_fontdir} %{buildroot}%{_sysconfdir}/X11/fontpath.d/%{name}
ln -sf %{legacydir} %{buildroot}%{_sysconfdir}/X11/fontpath.d/urw-fonts

# Generate the macro containing the path to our fonts:
install -m 0755 -d %{buildroot}%{_rpmconfigdir}/macros.d

cat > %{buildroot}%{_rpmconfigdir}/macros.d/macros.%{name} << _EOF
%%urw_base35_fontpath    %{_fontdir}
_EOF

# Check that the AppStream files are valid and safe. Otherwise they might not
# get used in Gnome Software...
%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/*.metainfo.xml

%post legacy
mkfontscale %{legacydir}
mkfontdir   %{legacydir}

%postun legacy
mkfontscale %{legacydir}
mkfontdir   %{legacydir}

# =============================================================================

%files
%{_datadir}/appdata/de.urwpp.URWCoreFontSetLevel2.metainfo.xml

# ---------------

%files common
%license LICENSE COPYING

%dir %{_fontdir}
%{_datadir}/fontconfig/conf.avail/%{fontconfig_prio}-urw-fallback-backwards.conf
%{_sysconfdir}/fonts/conf.d/%{fontconfig_prio}-urw-fallback-backwards.conf

# ---------------

%files devel
%{_rpmconfigdir}/macros.d/macros.%{name}

# ---------------

%files legacy
%dir %{_datadir}/licenses/urw-fonts
%license %{_datadir}/licenses/urw-fonts/COPYING
%ghost %verify (not md5 size mtime) %{legacydir}/fonts.dir
%ghost %verify (not md5 size mtime) %{legacydir}/fonts.scale
%{_sysconfdir}/X11/fontpath.d/urw-fonts
%dir %{legacydir}
%{legacydir}/*.afm
%{legacydir}/*.pfm
%{legacydir}/*.pfb

# =============================================================================

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20200910-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 11 2025 Zbigniew Jedrzejewski-Szmek  <zbyszek@in.waw.pl> - 20200910-25
- Drop noop scriptlets

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20200910-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20200910-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 28 2024 Zdenek Dohnal <zdohnal@redhat.com> - 20200910-22
- one more dir to cover

* Mon May 20 2024 Zdenek Dohnal <zdohnal@redhat.com> - 20200910-21
- 2280981 - The directory /usr/share/X11/fonts/urw-fonts/ is not in the RPM database

* Tue Apr 16 2024 Zdenek Dohnal <zdohnal@redhat.com> - 20200910-20
- 2268363 - StandardSymbolsPS.otf MISSING in urw-base35-standard-symbols-ps-fonts

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20200910-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20200910-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 16 2023 Richard Lescak <rlescak@redhat.com> - 20200910-17
- SPDX migration

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20200910-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20200910-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Adam Williamson <awilliam@redhat.com> - 20200910-14
- Require coreutils instead of fontconfig

* Fri Jun 24 2022 Adam Williamson <awilliam@redhat.com> - 20200910-13
- Put fontconfig requirement back to fix Rawhide compose

* Thu Jun 23 2022 Richard Lescak <rlescak@redhat.com> 20200910-12
- Remove fontconfig requirement (#2093177)

* Wed May 18 2022 Richard Lescak <rlescak@redhat.com> 20200910-11
- Substituted badly monospaced Nimbus Mono PS with Dejavu Sans Mono (#2021366)
- added substitution for Century 

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20200910-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 07 2021 Richard Lescak <rlescak@redhat.com> 20200910-9
- Recorrected typo in License field

* Tue Sep 07 2021 Richard Lescak <rlescak@redhat.com> 20200910-8
- Corrected typo in License field

* Mon Sep 06 2021 Richard Lescak <rlescak@redhat.com> 20200910-7
- Added GPL2.0+ license into tag (old legacy fonts), removed old obsoletes/provides from macro

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200910-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 09 2021 Richard Lescak <rlescak@redhat.com> 20200910-5
- Remove definition of D050000L font as fantasy in D050000L.conf file (#1909382)

* Wed Mar 10 2021 Peter Hutterer <peter.hutterer@redhat.com> 20200910-4
- Require mkfontscale and mkfontdir directly (#1937125)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200910-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Anna Khaitovich <akhaitov@redhat.com> - 20200910-2
- Fix some X11-related packaging bugs (#1918947)

* Thu Oct 22 2020 Anna Khaitovich <akhaitov@redhat.com> - 20200910-1
- Rebase to 20200910 version (#1877974)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20170801-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 10 2020 Zdenek Dohnal <zdohnal@redhat.com> - 20170801-15
- do not mention specific OS in description

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20170801-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20170801-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20170801-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170801-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20170801-10
- fc-cache call dropped (from scriptlets)

* Fri Apr 06 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20170801-9
- *-legacy subpackage introduced (temporary workaround for BZ #1551219)

* Wed Feb 28 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20170801-8
- copy-paste error fixed in de.urwpp.URWCoreFontSetLevel2.metainfo.xml file

* Wed Feb 21 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20170801-7
- added %%check section for validation of AppStream files

* Mon Feb 19 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20170801-6
- temporary workaround for BZ #1534206

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170801-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20170801-4
- added missing Obsoletes/Provides for *-nimbus-sans-narrow subpackage

* Wed Dec 13 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> 20170801-3
- *-devel subpackage added
- typos & syntax fixed for AppStream files
- NimbusSansNarrow-BdOblique.* renamed to *-BoldOblique
- *-nimbus-sans-narrow subpackage dropped
- priority/ordering decreased [60->61]
- ship *.otf format files as well

* Mon Sep 25 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20170801-2
- urw-base35-fonts-20170801-000-split-urw-fallback.patch added
- decrease the fontconfig priority/ordering value to 60 (bug #1494850)
- set same priority value for urw-fallback.conf as for other files (bug #1495199)

* Fri Sep 22 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20170801-1
- rebase to 20170801 version
- removed urw-* string from subpackages
- fontconfig priority value updated to 35
- error messages from 'xset fp rehash' suppressed (bug #1466254)
- AppStream files added into (sub)packages
- fontconfig files added into (sub)packages
- fixed fonts path during %%install
- source location updated to point at github.com

* Mon Jun 05 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 20160926-1
- %%description line in 'fontfamily_subpkg' macro split
- requirement for 'fontpackages-filesystem' added
- mark 'font.dir' and 'font.scale' as %%ghost files
- fix the upgrading process (for Obsoletes|Provides|Conflicts)
- simplify creation of the subpackages with auxiliary %%fontfamily_subpkg macro
- update the fontconfig cache and X11 Logical Font Description database
  (during install/update/erase)
- initial version of specfile created
