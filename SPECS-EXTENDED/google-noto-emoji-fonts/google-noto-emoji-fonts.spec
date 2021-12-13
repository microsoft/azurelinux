Vendor:         Microsoft Corporation
Distribution:   Mariner
%global commit0 d5e261484286d33a1fe8a02676f5907ecc02106f
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global fontname google-noto-emoji

%if (0%{?fedora} > 25)
%global buildfont 1
%else
%global buildfont 0
%endif


Name:           %{fontname}-fonts
Version:        20200723
Release:        2%{?dist}
Summary:        Google “Noto Emoji” Black-and-White emoji font

# In noto-emoji-fonts source
## noto-emoji code is in ASL 2.0 license
## Emoji fonts are under OFL license
### third_party color-emoji code is in BSD license
### third_party region-flags code is in Public Domain license
# In nototools source
## nototools code is in ASL 2.0 license
### third_party ucd code is in Unicode license
License:        OFL and ASL 2.0
URL:            https://github.com/googlei18n/noto-emoji
Source0:        https://github.com/googlei18n/noto-emoji/archive/%{commit0}.tar.gz#/noto-emoji-%{shortcommit0}.tar.gz
Source2:        %{fontname}.metainfo.xml
Source3:        %{fontname}-color.metainfo.xml

Patch0:         noto-emoji-build-all-flags.patch
Patch1:         noto-emoji-use-gm.patch
Patch2:         noto-emoji-use-system-pngquant.patch
Patch3:         noto-emoji-check-sequence.patch

BuildArch:      noarch
BuildRequires:  gcc
BuildRequires:  fontpackages-devel
%if %buildfont
BuildRequires:  fonttools
BuildRequires:  python3-fonttools
BuildRequires:  nototools
BuildRequires:  python3-nototools
BuildRequires:  python3-devel
BuildRequires:  GraphicsMagick
BuildRequires:  pngquant
BuildRequires:  zopfli
BuildRequires:  cairo-devel
%endif

Requires:       fontpackages-filesystem

Obsoletes:      google-noto-color-emoji-fonts < 20150617
Provides:       google-noto-color-emoji-fonts = 20150617

%description
This package provides the Google “Noto Emoji” Black-and-White emoji font.

%package -n     %{fontname}-color-fonts
Summary:        Google “Noto Color Emoji” colored emoji font
Requires:       fontpackages-filesystem
Obsoletes:      google-noto-color-emoji-fonts < 20150617
Provides:       google-noto-color-emoji-fonts = 20150617

%description -n %{fontname}-color-fonts
This package provides the Google “Noto Color Emoji” colored emoji font.

%prep
%setup -n noto-emoji-%{commit0}
%patch0 -p1 -b .noto-emoji-build-all-flags
%patch1 -p1 -b .noto-emoji-use-gm.patch
%patch2 -p1 -b .noto-emoji-use-system-pngquant
%patch3 -p1 -b .noto-emoji-check-sequence

rm -rf third_party/pngquant

%build
%if %buildfont
# Work around UTF-8
export LANG=C.UTF-8

%make_build OPT_CFLAGS="$RPM_OPT_FLAGS" BYPASS_SEQUENCE_CHECK='True'
%endif

%install
install -m 0755 -d %{buildroot}%{_fontdir}

%if %buildfont
# Built by us from the supplied pngs:
install -m 0644 -p NotoColorEmoji.ttf %{buildroot}%{_fontdir}
%else
# Pre-built, and included with the source:
install -m 0644 -p fonts/NotoColorEmoji.ttf %{buildroot}%{_fontdir}
%endif

# Pre-built, and included with the source:
install -m 0644 -p fonts/NotoEmoji-Regular.ttf %{buildroot}%{_fontdir}

mkdir -p %{buildroot}%{_datadir}/appdata
install -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/appdata
install -m 0644 -p %{SOURCE3} %{buildroot}%{_datadir}/appdata

%_font_pkg NotoEmoji-Regular.ttf
%license LICENSE
%doc AUTHORS CONTRIBUTING.md CONTRIBUTORS README.md
%{_datadir}/appdata/google-noto-emoji.metainfo.xml

%_font_pkg -n color NotoColorEmoji.ttf
%license LICENSE
%doc AUTHORS CONTRIBUTING.md CONTRIBUTORS README.md
%{_datadir}/appdata/google-noto-emoji-color.metainfo.xml


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200723-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jul 21 2020 Mike FABIAN <mfabian@redhat.com> - 20200723-1
- Update to upstream snapshot tarball (Unicode 13.0.0 support)

* Thu Apr 02 2020 Mike FABIAN <mfabian@redhat.com> - 20200402-1
- Update to upstream snapshot tarball (fixes U+1F9D1 U+200D U+1F3A8 "artist"
  and many other sequences)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20191019-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 19 2019 Mike FABIAN <mfabian@redhat.com> - 20191019-1
- Update to upstream snapshot tarball (Fixes for people holding hands)

* Thu Aug 29 2019 Mike FABIAN <mfabian@redhat.com> - 20190829-1
- Update to upstream snapshot tarball (Fixes FR and NL flags)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190709-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 09 2019 Mike FABIAN <mfabian@redhat.com> - 20190709-1
- Update to upstream snapshot tarball (Contains the new emoji added in Unicode 12.0.0,
  also fixes the "people holding hands" sequence.
- Port to Python3 and build using Python3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180814-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 14 2018 Mike FABIAN <mfabian@redhat.com> - 20180814-1
- Update to upstream snapshot tarball (Contains the new emoji added in Unicode 11.0.0)

* Mon Jul 23 2018 Mike FABIAN <mfabian@redhat.com> - 20180508-6
- Fix build in rawhide
- Resolves: rhbz#1604247

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180508-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Peng Wu <pwu@redhat.com> - 20180508-4
- Fixes buildfont macro

* Tue Jun 19 2018 Peng Wu <pwu@redhat.com> - 20180508-3
- Only build emoji color font since Fedora 26

* Wed May 23 2018 Peng Wu <pwu@redhat.com> - 20180508-2
- Use GraphicsMagick instead of ImageMagick

* Tue May 08 2018 Mike FABIAN <mfabian@redhat.com> - 20180508-1
- Update to upstream snapshot tarball (color emoji font version 2.011)
- Add patch to build all country flags (Resolves: rhbz#1574195)

* Wed Mar 07 2018 Mike FABIAN <mfabian@redhat.com> - 20180307-1
- Update to upstream snapshot tarball (color emoji font version 2.004)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170928-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb  5 2018 Peng Wu <pwu@redhat.com> - 20170928-3
- Use nototools package to build google-noto-emoji-fonts

* Wed Nov  8 2017 Peter Oliver <rpm@mavit.org.uk> - 20170928-2
- Prefer zopflipng to optipng, since it should yield smaller files.
- Use the font we built, rather than the one included with the source.

* Thu Sep 28 2017 Mike FABIAN <mfabian@redhat.com> - 20170828-1
- Update to upstream snapshot tarball
- split black-and-white and color fonts into different sub-packages.

* Mon Aug 28 2017 Mike FABIAN <mfabian@redhat.com> - 20170827-1
- Update to upstream snapshot tarball
- Update color emoji font to version 2.001, new design.
- Contains the new emoji added in Unicode 10.0.0.

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170608-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 08 2017 Mike FABIAN <mfabian@redhat.com> - 20170608-1
- Update to upstream snapshot tarball

* Tue May 23 2017 Mike FABIAN <mfabian@redhat.com> - 20170523-1
- Update to upstream snapshot tarball
- This fixes the skin tones of the light/medium light male cook emoji,
  which had been swapped.

* Wed Apr 26 2017 Mike FABIAN <mfabian@redhat.com> - 20170426-1
- Update to upstream snapshot tarball
  (fixes the family emoji sequences:
  kiss: woman, man U+1F469 U+200D U+2764 U+FE0F U+200D U+1F48B U+200D U+1F468
  couple with heart: woman, man U+1F469 U+200D U+2764 U+FE0F U+200D U+1F468)

* Thu Feb 23 2017 Peng Wu <pwu@redhat.com> - 20170223-1
- Update to upstream snapshot tarball

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160406-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri May  6 2016 Peng Wu <pwu@redhat.com> - 20160406-5
- Avoid to use python setup.py

* Fri Apr 29 2016 Peng Wu <pwu@redhat.com> - 20160406-4
- Replace google-noto-color-emoji-fonts package

* Mon Apr 25 2016 Peng Wu <pwu@redhat.com> - 20160406-3
- Add google-noto-emoji.metainfo.xml

* Wed Apr 20 2016 Peng Wu <pwu@redhat.com> - 20160406-2
- Use system pngquant

* Wed Apr 20 2016 Peng Wu <pwu@redhat.com> - 20160406-1
- Initial packaging
