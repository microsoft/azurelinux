# SPDX-License-Identifier: MIT

%global commit0 22e564626297b4df0a40570ad81d6c05cc7c38bd
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global fontname google-noto-emoji

%if (0%{?fedora} > 25)
%global buildfont 1
%else
%global buildfont 0
%endif

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
BuildRequires:  make

Version: 20241008
Release: 1%{?dist}
URL:     https://github.com/googlefonts/noto-emoji

%global foundry           Google
# In noto-emoji-fonts source
## noto-emoji code is in ASL 2.0 license
## Emoji fonts are under OFL license
### third_party color-emoji code is in BSD license
### third_party region-flags code is in Public Domain license
# In nototools source
## nototools code is in ASL 2.0 license
### third_party ucd code is in Unicode license
%global fontlicense       OFL-1.1 AND Apache-2.0
%global fontlicenses      LICENSE OFL.txt
%global fontdocs          AUTHORS CONTRIBUTING.md CONTRIBUTORS README.md README.txt

%global fontfamily0       Noto Emoji
%global fontsummary0      Google “Noto Emoji” Black-and-White emoji font
%global fonts0            NotoEmoji-Regular.ttf
%global fontdescription0  %{expand:
This package provides the Google “Noto Emoji” Black-and-White emoji font.
}

%global fontfamily1       Noto Color Emoji
%global fontsummary1      Google “Noto Color Emoji” colored emoji font
%global fontpkgheader1    %{expand:
Obsoletes:      google-noto-emoji-color-fonts < 20220916-6
Provides:       google-noto-emoji-color-fonts = %{version}-%{release}
}
%global fonts1            NotoColorEmoji.ttf
%global fontdescription1  %{expand:
This package provides the Google “Noto Color Emoji” colored emoji font.
}

Source0:        https://github.com/googlefonts/noto-emoji/archive/%{commit0}.tar.gz#/noto-emoji-%{shortcommit0}.tar.gz
Source4:        Noto_Emoji.zip

Patch0:         noto-emoji-build-all-flags.patch
Patch1:         noto-emoji-use-gm.patch
Patch2:         noto-emoji-use-system-pngquant.patch

%fontpkg -a


%prep
%autosetup -p1 -a 4 -n noto-emoji-%{commit0}

rm -rf third_party/pngquant

cp -p static/NotoEmoji-Regular.ttf .

%build

%if %buildfont
# Work around UTF-8
export LANG=C.UTF-8

%make_build OPT_CFLAGS="$RPM_OPT_FLAGS" BYPASS_SEQUENCE_CHECK='True'
%else
cp -p fonts/NotoColorEmoji.ttf .
%endif

%fontbuild -a

%install
%fontinstall -a

%check
%fontcheck -a

%fontfiles -a


%changelog
* Tue Oct 08 2024 Mike FABIAN <mfabian@redhat.com> - 20241008-1
- Update to v2.047 (Unicode 16.0)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20231130-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Peng Wu <pwu@redhat.com> - 20231130-1
- Update to v2.042

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220916-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220916-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20220916-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 25 2023 Peng Wu <pwu@redhat.com> - 20220916-6
- Update to follow New Fonts Packaging Guidelines

* Mon May 22 2023 Peng Wu <pwu@redhat.com> - 20220916-5
- Migrate to SPDX license

* Thu Mar 16 2023 Peng Wu <pwu@redhat.com> - 20220916-4
- Use metainfodir macro for metainfo files

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20220916-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 28 2022 Peng Wu <pwu@redhat.com> - 20220916-2
- Update Upstream URL

* Tue Sep 27 2022 Peng Wu <pwu@redhat.com> - 20220916-1
- Update to v2.038

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20211102-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 21 2022 Peng Wu <pwu@redhat.com> - 20211102-1
- Update to v2.034

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210716-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 28 2021 Peng Wu <pwu@redhat.com> - 20210716-1
- Update to v2.028

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200916-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200916-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 24 2020 Peng Wu <pwu@redhat.com> - 20200916-1
- Update to upstream snapshot tarball (Unicode 13.1.0 support)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200723-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Mike FABIAN <mfabian@redhat.com> - 20200723-1
- Update to upstream snapshot tarball (Unicode 13.0.0 support)

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 20200402-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

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
