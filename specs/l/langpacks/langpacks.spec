# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:      langpacks
Version:   4.2
Release: 6%{?dist}
Summary:   Langpacks meta-package

License:   GPL-2.0-or-later
BuildArch: noarch
BuildRequires: python3 fontconfig
Source4:   normlang.py

# to split up the AppStream file
BuildRequires: libappstream-glib >= 0.5.10

%description
Langpack meta-package to provide individual langpacks packages.

# The following language list is generated based on
# 1) take the languages where anaconda translations are available
# ls /usr/share/locale/*/LC_MESSAGES/anaconda.mo
# Then pick those languages which provides at least a single langpack
# Now, Added exception for dz and ku languages which have no anaconda.mo
# 2) Added br ga he nn nr ss tn ts ve xh
# as per requested in https://bugzilla.redhat.com/show_bug.cgi?id=1310538
# 3) Enabled en langpack https://bugzilla.redhat.com/show_bug.cgi?id=1312890
# 4) Enabled eo langpack https://bugzilla.redhat.com/show_bug.cgi?id=1644736
# 5) Enabled bo, dz, ka, km, ku, my, yi
# 6) Enabled zh_HK to set its own input method
# 7) Enabled chr, dv, hy, iu, lo so that its default font be installed at least

# package list
#
# Writing this in LUA to make it more visible and easy to maintain.
#
# lang: language identifier
# fclang: language identifier in fontconfig. lang will be used if not present
# default: default font sets
#  face: default typeface for default-fonts-<language code>.
#  sans: default sans-serif font package
#  serif: default serif font package
#  mono: default monospace font package
# recommends: recommended font packages to be installed
#             only activated for Fedora
# inputmethod: input method to be pulled by core meta package
# meta: dependencies foe langpacks meta package
#  requires: required packages by meta package
#  recommends: recommended packages by meta package
#
# Adding fedora_ prefix to inputmethod and meta.requires/meta.recommends will be available for Fedora only.
#
# See defcorepkg, deffontpkg, and defmetapkg for package template
%{lua:
local core_font_package_list
if tonumber(rpm.expand("0%{?rhel}")) ~= 0 and tonumber(rpm.expand("0%{?rhel}")) > 9 then
core_font_package_list = {
  default={
    sans={ "redhat-text-vf-fonts", "google-noto-sans-vf-fonts" },
    serif={ "google-noto-serif-vf-fonts" },
    mono={ "redhat-mono-vf-fonts", "google-noto-sans-mono-vf-fonts" },
    emoji={ "google-noto-emoji-color-fonts" },
    math={ "google-noto-sans-math-fonts", "stix-fonts", "google-noto-sans-symbols-vf-fonts", "google-noto-sans-symbols-2-fonts" }
  },
  cjk={
    sans={ "google-noto-sans-cjk-vf-fonts" },
    serif={ "google-noto-serif-cjk-vf-fonts" },
    mono={ "google-noto-sans-mono-cjk-vf-fonts" },
  },
}
else
core_font_package_list = {
  default={
    sans={ "abattis-cantarell-vf-fonts", "google-noto-sans-vf-fonts" },
    serif={ "google-noto-serif-vf-fonts" },
    mono={ "google-noto-sans-mono-vf-fonts" },
    emoji={ "google-noto-emoji-color-fonts" },
    math={ "google-noto-sans-math-fonts", "stix-fonts", "google-noto-sans-symbols-vf-fonts", "google-noto-sans-symbols-2-fonts" }
  },
  cjk={
    sans={ "google-noto-sans-cjk-vf-fonts" },
    serif={ "google-noto-serif-cjk-vf-fonts" },
    mono={ "google-noto-sans-mono-cjk-vf-fonts" },
  },
}
end
local langpacks_package_list = {
 { lang="af", fclang="", langname="Afrikaans", default={
                sans="",
                serif="",
                mono="" },
   recommends={},
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="am", fclang="", langname="Amharic", default={
                sans="google-noto-sans-ethiopic-vf-fonts",
                serif="google-noto-serif-ethiopic-vf-fonts",
                mono="" },
   recommends={ "senamirmir-washra-fantuwua-fonts",
                "senamirmir-washra-fonts",
                "senamirmir-washra-hiwua-fonts",
                "senamirmir-washra-jiret-fonts",
                "senamirmir-washra-tint-fonts",
                "senamirmir-washra-wookianos-fonts",
                "senamirmir-washra-yebse-fonts",
                "senamirmir-washra-yigezu-bisrat-goffer-fonts",
                "senamirmir-washra-yigezu-bisrat-gothic-fonts",
                "senamirmir-washra-zelan-fonts",
                "xorg-x11-fonts-ethiopic",
                "sil-abyssinica-fonts"
                },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ar", fclang="", langname="Arabic", default={
                sans="google-noto-sans-arabic-vf-fonts",
                serif="google-noto-naskh-arabic-vf-fonts",
                mono="" },
   recommends={ "paktype-naqsh-fonts",
                "paktype-tehreer-fonts",
                "kacst-art-fonts",
                "kacst-book-fonts",
                "kacst-decorative-fonts",
                "kacst-digital-fonts",
                "kacst-farsi-fonts",
                "kacst-letter-fonts",
                "kacst-naskh-fonts",
                "kacst-office-fonts",
                "kacst-one-fonts",
                "kacst-pen-fonts",
                "kacst-poster-fonts",
                "kacst-qurn-fonts",
                "kacst-screen-fonts",
                "kacst-title-fonts",
                "kacst-titlel-fonts"
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="as", fclang="", langname="Assamese", default={
                sans="google-noto-sans-bengali-vf-fonts",
                serif="google-noto-serif-bengali-vf-fonts",
                mono="" },
   recommends={ "google-noto-sans-bengali-ui-vf-fonts",
                "lohit-assamese-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ast", fclang="", langname="Asturian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="be", fclang="", langname="Belarusian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="bg", fclang="", langname="Bulgarian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="bn", fclang="", langname="Bengali", default={
                sans="google-noto-sans-bengali-vf-fonts",
                serif="google-noto-serif-bengali-vf-fonts",
                mono="" },
   recommends={ "google-noto-sans-bengali-ui-vf-fonts",
                "lohit-bengali-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="bo", fclang="", langname="Tibetan", default={
                sans="jomolhari-fonts",
                serif="",
                mono="" },
   recommends={ "tibetan-machine-uni-fonts"
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="br", fclang="", langname="Breton", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="bs", fclang="", langname="Bosnian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ca", fclang="", langname="Catalan", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="chr", fclang="", langname="Cherokee", default={
                sans="google-noto-sans-cherokee-vf-fonts",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="cs", fclang="", langname="Czech", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="cy", fclang="", langname="Welsh", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="da", fclang="", langname="Danish", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="de", fclang="", langname="German", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="dv", fclang="", langname="Divehi", default={
                sans="google-noto-sans-thaana-vf-fonts",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="dz", fclang="", langname="Bhutanese", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="el", fclang="", langname="Greek", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="en", fclang="", langname="English", default={
                sans="", -- Do not add anything here. default-fonts-en is equivalent to default-fonts-core-sans
                serif="",
                mono="" },
   recommends={ "liberation-sans-fonts",
                "liberation-serif-fonts",
                "liberation-mono-fonts",
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="en_GB", fclang="en", langname="English (United Kingdom)", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="eo", fclang="", langname="Esperanto", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="es", fclang="", langname="Spanish", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="et", fclang="", langname="Estonian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="eu", fclang="", langname="Basque", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="fa", fclang="", langname="Persian", default={
                sans="vazirmatn-vf-fonts",
                serif="google-noto-naskh-arabic-vf-fonts",
                mono="" },
   recommends={ "google-noto-naskh-arabic-vf-fonts"
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="fi", fclang="", langname="Finnish", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="fr", fclang="", langname="French", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ga", fclang="", langname="Irish", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="gl", fclang="", langname="Galician", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="got", fclang="", langname="Gothic", default={
                sans="google-noto-sans-gothic-fonts",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="gu", fclang="", langname="Gujarati", default={
                sans="google-noto-sans-gujarati-vf-fonts",
                serif="google-noto-serif-gujarati-vf-fonts",
                mono="" },
   recommends={ "google-noto-sans-gujarati-ui-fonts",
                "lohit-gujarati-fonts",
                "samyak-gujarati-fonts"
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="he", fclang="", langname="Hebrew", default={
                sans="google-noto-sans-hebrew-vf-fonts",
                serif="google-noto-serif-hebrew-vf-fonts",
                mono="" },
   recommends={ "culmus-aharoni-clm-fonts",
                "culmus-caladings-clm-fonts",
                "culmus-david-clm-fonts",
                "culmus-drugulin-clm-fonts",
                "culmus-ellinia-clm-fonts",
                "culmus-frank-ruehl-clm-fonts",
                "culmus-hadasim-clm-fonts",
                "culmus-keteryg-fonts",
                "culmus-miriam-clm-fonts",
                "culmus-miriam-mono-clm-fonts",
                "culmus-nachlieli-clm-fonts",
                "culmus-simple-clm-fonts",
                "culmus-stamashkenaz-clm-fonts",
                "culmus-stamsefarad-clm-fonts",
                "culmus-yehuda-clm-fonts",
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="hi", fclang="", langname="Hindi", default={
                sans="google-noto-sans-devanagari-vf-fonts",
                serif="google-noto-serif-devanagari-vf-fonts",
                mono="" },
   recommends={ "google-noto-sans-devanagari-ui-vf-fonts",
                "lohit-devanagari-fonts",
                "samyak-devanagari-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="hr", fclang="", langname="Croatian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="hu", fclang="", langname="Hungarian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="hy", fclang="", langname="Armenian", default={
                sans="google-noto-sans-armenian-vf-fonts",
                serif="google-noto-serif-armenian-vf-fonts",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ia", fclang="", langname="Interlingua", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="id", fclang="", langname="Indonesian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="is", fclang="", langname="Icelandic", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="it", fclang="", langname="Italian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="iu", fclang="", langname="Inuktitut", default={
                sans="google-noto-sans-canadian-aboriginal-vf-fonts",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ja", fclang="", langname="Japanese", default={
                sans="", -- Use core_font_package_list if you want to have common fonts for CJK
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="ibus-anthy",
   meta={ requires={},
          recommends={},
           fedora_recommends={ "(uim-anthy if uim)" }
   },
 },
 { lang="kab", fclang="", langname="Kabyle", default={
                 sans="",
                 serif="",
                 mono="" },
   recommends={ "google-noto-sans-tifinagh-fonts" },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ka", fclang="", langname="Georgian", default={
                sans="google-noto-sans-georgian-vf-fonts",
                serif="google-noto-serif-georgian-vf-fonts",
                mono="" },
   recommends={ "bpg-chveulebrivi-fonts",
                "bpg-courier-fonts",
                "bpg-glaho-fonts",
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="kk", fclang="", langname="Kazakh", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="km", fclang="", langname="Khmer", default={
                sans="google-noto-sans-khmer-vf-fonts",
                serif="google-noto-serif-khmer-vf-fonts",
                mono="" },
   recommends={ "khmer-os-system-fonts",
                "khmer-os-battambang-fonts",
                "khmer-os-bokor-fonts",
                "khmer-os-content-fonts",
                "khmer-os-fasthand-fonts",
                "khmer-os-freehand-fonts",
                "khmer-os-handwritten-fonts",
                "khmer-os-metal-chrieng-fonts",
                "khmer-os-muol-fonts-all",
                "khmer-os-siemreap-fonts",
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="kn", fclang="", langname="Kannada", default={
                sans="google-noto-sans-kannada-vf-fonts",
                serif="google-noto-serif-kannada-vf-fonts",
                mono="" },
   recommends={ "google-noto-sans-kannada-ui-vf-fonts",
                "gubbi-fonts",
                "lohit-kannada-fonts",
                "navilu-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ko", fclang="", langname="Korean", default={
                sans="", -- Use core_font_package_list if you want to have common fonts for CJK
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="ibus-hangul",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ku", fclang="", langname="Kurdish", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="lo", fclang="", langname="Lao", default={
                sans="google-noto-sans-lao-vf-fonts",
                serif="google-noto-serif-lao-vf-fonts",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="lt", fclang="", langname="Lithuanian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="lv", fclang="", langname="Latvian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="mai", fclang="", langname="Maithili", default={
                sans="google-noto-sans-devanagari-vf-fonts",
                serif="google-noto-serif-devanagari-vf-fonts",
                mono="" },
   recommends={ "google-noto-sans-devanagari-ui-vf-fonts",
                "lohit-devanagari-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="mk", fclang="", langname="Macedonian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ml", fclang="", langname="Malayalam", default={
                sans="rit-meera-new-fonts",
                serif="rit-rachana-fonts",
                mono="" },
   recommends={ "google-noto-sans-malayalam-vf-fonts",
                "google-noto-sans-malayalam-ui-vf-fonts",
                "google-noto-serif-malayalam-vf-fonts",
                "lohit-malayalam-fonts",
                "samyak-malayalam-fonts",
                "smc-anjalioldlipi-fonts",
                "smc-dyuthi-fonts",
                "smc-raghumalayalamsans-fonts",
                "smc-suruma-fonts",
                "rit-sundar-fonts",
                "rit-panmana-fonts",
                "rit-ezhuthu-fonts",
                "rit-tn-joy-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="mni", fclang="", langname="Manipuri", default={
                sans="google-noto-sans-meetei-mayek-vf-fonts",
                serif="",
                mono="" },
   recommends={ "",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="mr", fclang="", langname="Marathi", default={
                sans="google-noto-sans-devanagari-vf-fonts",
                serif="google-noto-serif-devanagari-vf-fonts",
                mono="" },
   recommends={ "google-noto-sans-devanagari-ui-vf-fonts",
                "lohit-marathi-fonts",
                "samyak-devanagari-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ms", fclang="", langname="Malay", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="my", fclang="", langname="Burmese", default={
                sans="sil-padauk-fonts",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="nb", fclang="", langname="Norwegian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ne", fclang="", langname="Nepali", default={
                sans="madan-fonts",
                serif="",
                mono="" },
   recommends={ "google-noto-sans-devanagari-vf-fonts",
                "google-noto-sans-devanagari-ui-vf-fonts",
                "google-noto-serif-devanagari-vf-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="nl", fclang="", langname="Dutch", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="nn", fclang="", langname="Nynorsk", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="nqo", fclang="", langname="N'Ko", default={
                 sans="google-noto-sans-nko-fonts",
                 serif="",
                 mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="nr", fclang="", langname="Southern Ndebele", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="nso", fclang="", langname="Northern Sotho", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="or", fclang="", langname="Odia", default={
                sans="google-noto-sans-oriya-vf-fonts",
                serif="google-noto-serif-oriya-vf-fonts",
                mono="" },
   recommends={ "samyak-odia-fonts",
                "lohit-odia-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="pa", fclang="", langname="Punjabi", default={
                sans="google-noto-sans-gurmukhi-vf-fonts",
                serif="google-noto-serif-gurmukhi-vf-fonts",
                mono="" },
   recommends={ "saab-fonts",
                "lohit-gurmukhi-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="pl", fclang="", langname="Polish", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="pt_BR", fclang="pt", langname="Portuguese (Brazil)", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="pt", fclang="", langname="Portuguese", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ro", fclang="", langname="Romanian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ru", fclang="", langname="Russian", default={
                sans="",
                serif="",
                mono="" },
   recommends={ "pt-sans-fonts",
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="sat", fclang="", langname="Santali", default={
                sans="google-noto-sans-ol-chiki-vf-fonts",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="si", fclang="", langname="Sinhala", default={
                sans="google-noto-sans-sinhala-vf-fonts",
                serif="google-noto-serif-sinhala-vf-fonts",
                mono="" },
   recommends={
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="sk", fclang="", langname="Slovak", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="sl", fclang="", langname="Slovenian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="sq", fclang="", langname="Albanian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="sr", fclang="", langname="Serbian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ss", fclang="", langname="Swati", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="sv", fclang="", langname="Swedish", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="syr", fclang="", langname="Syriac", default={
                 sans="google-noto-sans-syriac-vf-fonts",
                 serif="",
                 mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ta", fclang="", langname="Tamil", default={
                sans="google-noto-sans-tamil-vf-fonts",
                serif="google-noto-serif-tamil-vf-fonts",
                mono="" },
   recommends={ "google-noto-sans-tamil-ui-vf-fonts",
                "lohit-tamil-fonts",
                "samyak-tamil-fonts",
                "serafettin-cartoon-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="te", fclang="", langname="Telugu", default={
                sans="google-noto-sans-telugu-vf-fonts",
                serif="google-noto-serif-telugu-vf-fonts",
                mono="" },
   recommends={ "google-noto-sans-telugu-ui-vf-fonts",
                "lohit-telugu-fonts",
                "pothana2000-fonts",
                "vemana2000-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="th", fclang="", langname="Thai", default={
                sans="google-noto-sans-thai-vf-fonts",
                serif="google-noto-serif-thai-vf-fonts",
                mono="" },
   recommends={ "tlwg-garuda-fonts",
                "tlwg-kinnari-fonts",
                "tlwg-laksaman-fonts",
                "tlwg-loma-fonts",
                "tlwg-mono-fonts",
                "tlwg-norasi-fonts",
                "tlwg-purisa-fonts",
                "tlwg-sawasdee-fonts",
                "tlwg-typewriter-fonts",
                "tlwg-typist-fonts",
                "tlwg-typo-fonts",
                "tlwg-umpush-fonts",
                "tlwg-waree-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="tn", fclang="", langname="Tswana", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="tr", fclang="", langname="Turkish", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ts", fclang="", langname="Tsonga", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="uk", fclang="", langname="Ukrainian", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ur", fclang="", langname="Urdu", default={
                sans="paktype-naskh-basic-fonts",
                serif="google-noto-naskh-arabic-vf-fonts",
                mono="" },
   recommends={ "nafees-nastaleeq-fonts",
                "nafees-web-naskh-fonts",
              },
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="ve", fclang="", langname="Venda", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="vi", fclang="", langname="Vietnamese", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   fedora_inputmethod="ibus-unikey",
   inputmethod="ibus-m17n",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="xh", fclang="", langname="Xhosa", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="yi", fclang="", langname="Yiddish", default={
                sans="google-noto-sans-hebrew-vf-fonts",
                serif="google-noto-serif-hebrew-vf-fonts",
                mono="" },
   recommends={ "culmus-aharoni-clm-fonts",
                "culmus-caladings-clm-fonts",
                "culmus-david-clm-fonts",
                "culmus-drugulin-clm-fonts",
                "culmus-ellinia-clm-fonts",
                "culmus-frank-ruehl-clm-fonts",
                "culmus-hadasim-clm-fonts",
                "culmus-keteryg-fonts",
                "culmus-miriam-clm-fonts",
                "culmus-miriam-mono-clm-fonts",
                "culmus-nachlieli-clm-fonts",
                "culmus-simple-clm-fonts",
                "culmus-stamashkenaz-clm-fonts",
                "culmus-stamsefarad-clm-fonts",
                "culmus-yehuda-clm-fonts",
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="zh_CN", fclang="", langname="Simplified Chinese", default={
                sans="", -- Use core_font_package_list if you want to have common fonts for CJK
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="ibus-libpinyin",
   meta={ requires={},
          recommends={}
   },
 },
 { lang="zh_HK", fclang="", langname="Hong Kong Traditional Chinese", default={
                sans="", -- Use core_font_package_list if you want to have common fonts for CJK
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="ibus-table-chinese-cangjie",
   meta={ requires={},
          recommends={ "ibus-table-chinese-quick" },
          fedora_recommends={ "ibus-table-chinese-quick",
                              "ibus-cangjie-engine-cangjie",
                              "ibus-cangjie-engine-quick",
                            }
   },
 },
 { lang="zh_TW", fclang="", langname="Taiwan", default={
                sans="", -- Use core_font_package_list if you want to have common fonts for CJK
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="ibus-chewing",
   meta={ requires={},
          recommends={ "ibus-table-chinese-cangjie",
                       "ibus-table-chinese-quick"
          }
   },
 },
 { lang="zu", fclang="", langname="Zulu", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
--[[
 { lang="", fclang="", langname="", default={
                sans="",
                serif="",
                mono="" },
   recommends={
              },
   inputmethod="",
   meta={ requires={},
          recommends={}
   },
 },
]]
}

--Miscellaneous functions
local function is_nonlatin(lang)
  local latinlang = { "af", "az", "bs", "ca", "cs", "cy", "da", "de", "en", "es", "et", "fil", "fi", "fo", "fr", "ga", "gd", "gl", "hr", "hu", "id", "is", "it", "kk", "ky", "lb", "lt", "lv", "mk", "mont", "ms", "mt", "nl", "no", "pl", "pt", "ro", "sk", "sl", "sq", "sr", "sv", "sw", "tg", "tk", "tr", "uz" }

  for i = 1, #latinlang do
    n, _ = string.find(lang, latinlang[i] .. "[_%a]*")
      if n == 1 then
        return false
      end
  end
  return true
end

local function is_cjk(lang)
  local pat = { "ja", "ko", "zh" }
  for i = 1, #pat do
    n, _ = string.find(lang, pat[i] .. "[_%a]*")
    if n == 1 then
      return true
    end
  end
  return false
end

local function build_deps(deps, tag, pkgs)
  local ret = ""
  for i = 1, #pkgs do
    ret = ret .. (pkgs[i] ~= "" and (tag .. ":   " .. pkgs[i] .. "\n") or "")
  end
  return deps .. ret
end

local function drop_duplicate(pkgs)
  local hash = {}
  local ret = {}
  for _, v in ipairs(pkgs) do
    if (not hash[v]) then
      table.insert(ret, v)
      hash[v] = true
    end
  end
  return ret
end

local function append_fontprov(deps, lang)
  return deps .. (lang ~= "" and ("Provides:   font(:lang=" .. lang .. ")\n") or "")
end

local function append_obsolete(deps, pkg)
  return deps .. build_deps("", "Obsoletes", {pkg .. " < %{version}-%{release}"}) .. build_deps("", "Provides", {pkg .. " = %{version}-%{release}"})
end

--
--Package template for langpacks-core-<lang>
--
local function defcorepkg(lang, fontlang, langname, inputmethod)
  local templ = [[
%package core-%{_lang}
Summary: %{_langname} langpacks core meta-package
Requires: default-fonts-%{_fontlang}
%{?_req}

%description core-%{_lang}
This package provides %{_langname} core langpacks packages.

%files core-%{_lang}
%{_datadir}/metainfo/org.fedoraproject.LangPack-Core-%{_lang}.metainfo.xml

]]
  inputmethod = (not(inputmethod) and "" or inputmethod)
  rpm.define("_lang " .. lang)
  rpm.define("_fontlang " .. string.gsub(fontlang, "-", "_"))
  rpm.define("_langname " .. langname)
  if inputmethod ~= "" then
    rpm.define("_req " .. "Requires: (" .. inputmethod .. " if service(graphical-login))\n")
  end
  print(rpm.expand(templ))
  rpm.undefine("_lang")
  rpm.undefine("_fontlang")
  rpm.undefine("_langname")
  rpm.undefine("_req")
end

--
--Package template for fonts metapackage like default-fonts-*
--
local function _deffontpkg(pkgname, summary1, summary2, deps, files)
  local templ = [[
%package -n %{_pkgname}
Summary:    Metapackage to install %{_summary1} for %{_summary2}
%{?_req}

%description -n %{_pkgname}
This package provides %{_summary1} package set(s) for %{_summary2}

%files -n %{_pkgname}
%{_files}

]]
  local f = table.concat(files, "\n")
  rpm.define("_pkgname " .. pkgname)
  rpm.define("_summary1 " .. summary1)
  rpm.define("_summary2 " .. summary2)
  rpm.define("_files %{expand:" .. f .. "}")
  if req ~= "" then
    rpm.define("_req %{expand:" .. deps .. "}")
  end
  print(rpm.expand(templ))
  rpm.undefine("_files")
  rpm.undefine("_summary1")
  rpm.undefine("_summary2")
  rpm.undefine("_pkgname")
  rpm.undefine("_req")
end

local function deffontpkg(pkgname, summary1, summary2, deps)
  _deffontpkg(pkgname, summary1, summary2, deps,
              {"%{_datadir}/metainfo/org.fedoraproject.%{_pkgname}.metainfo.xml"})
end

local function defsansfontpkg(cat, summary, target_langs, deps)
  local req = ""
  local files = {"%{_datadir}/metainfo/org.fedoraproject.default-fonts-" .. cat .. "-sans.metainfo.xml"}
  for i = 1, #target_langs do
    -- Add Provides: font(:lang=LL) and Obsoletes/Provides: default-fonts-LL
    req = append_obsolete(append_fontprov(req, target_langs[i]), "default-fonts-" .. target_langs[i])
    req = append_obsolete(req, "langpacks-core-font-" .. target_langs[i])
    table.insert(files, "%{_datadir}/metainfo/org.fedoraproject.default-fonts-" .. target_langs[i] .. ".metainfo.xml")
  end
  _deffontpkg("default-fonts-" .. cat .. "-sans", "default sans-serif fonts", summary, build_deps(req, "Requires", drop_duplicate(deps)), files)
end

--
--Package template for langpacks-<lang>
--
local function defmetapkg(lang, fontlang, langname, deps)
  local templ = [[
%package %{_lang}
Summary: %{_langname} langpacks meta-package
Requires: %{name}-core-%{_lang}
Requires: %{name}-fonts-%{_fontlang}
%{?_req}

%description %{_lang}
This package provides %{_langname} langpacks meta-package.

%files %{_lang}
%{_datadir}/metainfo/org.fedoraproject.LangPack-%{_lang}.metainfo.xml

]]
  rpm.define("_lang " .. lang)
  rpm.define("_fontlang " .. string.gsub(fontlang, "-", "_"))
  rpm.define("_langname " .. langname)
  if deps ~= "" then
    rpm.define("_req %{expand:" .. deps .. "}")
  end
  print(rpm.expand(templ))
  rpm.undefine("_lang")
  rpm.undefine("_fontlang")
  rpm.undefine("_langname")
  rpm.undefine("_req")
end

--
--AppStream template
--
local function defappstream_open(fname)
  return "cat <<_EOL_>" .. fname .. "\\\n" .. [[
<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
<components origin=\"langpacks\">\
]]
end

local function defappstream_close(f)
  local s = f .. [[</components>\
_EOL_
]]
  return s
end

local function defappstream_body(f, component, id, lang, fclang, name, summary, desc)
  if lang ~= fclang and fclang ~= "" then
    return f
  end
  local _id = (lang == "" and id or id .. "-" .. lang)
  local _summary = (lang == "" and summary or summary .. " for " .. name)
  local s = f .. [[
  <component type=\"]] .. component .. [[\">\
    <metadata_license>CC0-1.0</metadata_license>\
    <id>org.fedoraproject.]] .. _id .. [[</id>\
    <name>]] .. name .. [[</name>\
    <summary>]] .. _summary .. [[</summary>\
    <description>\
      <p>\
        ]] .. desc .. [[\
      </p>\
    </description>\
  </component>\
]]
  return s
end

local function defappstream_metabody(f, id, name)
  f = defappstream_body(f, "font", "default-fonts-" .. id, "sans", "", name, "sans-serif default font", "sans-serif font package to install default font for " .. name .. " languages.")
  f = defappstream_body(f, "font", "default-fonts-" .. id, "serif", "", name, "serif default font", "serif font package to install default font for " .. name .. " languages.")
  f = defappstream_body(f, "font", "default-fonts-" .. id, "mono", "", name, "monospace default font", "monospace font package to install default font for " .. name .. " languages.")
  return f
end

local function defappstream(table)
  local slpc = defappstream_open("org.fedoraproject.LangPacks-Core.xml")
  local slp = defappstream_open("org.fedoraproject.LangPacks.xml")
  local sdf = defappstream_open("org.fedoraproject.default-fonts.xml")
  local slf = defappstream_open("org.fedoraproject.langpacks-fonts.xml")

  --
  -- default-fonts
  --
  sdf = defappstream_body(sdf, "font", "default-fonts", "", "", "default-fonts", "All default fonts for all the languages", "Meta-package to install all the default fonts for all the languages.")
  --
  -- default-fonts-core
  --
  sdf = defappstream_body(sdf, "font", "default-fonts", "core", "", "Latin", "All variants default fonts", "sans-serif/serif/monospace/emoji/math font packages to install default fonts for Latin.")
  sdf = defappstream_metabody(sdf, "core", "Latin")
  sdf = defappstream_body(sdf, "font", "default-fonts-core", "emoji", "", "Emoji", "default font", "emoji font package to install default font.")
  sdf = defappstream_body(sdf, "font", "default-fonts-core", "math", "", "Math", "default font", "math font package to install default font.")
  --
  -- default-fonts-other
  --
  sdf = defappstream_body(sdf, "font", "default-fonts", "other", "", "non-CJK", "All variants default fonts", "sans-serif/serif/monospace font packages to install default fonts for non-CJK languages.")
  sdf = defappstream_metabody(sdf, "other", "non-CJK")
  --
  -- default-fonts-cjk
  --
  sdf = defappstream_body(sdf, "font", "default-fonts", "cjk", "", "Chinese/Japanese/Korean", "All variants default fonts", "sans-serif/serif/monospace font packages to install default fonts for CJK languages.")
  sdf = defappstream_metabody(sdf, "cjk", "Chinese/Japanese/Korean")

  for i = 1, #table do
    slpc = defappstream_body(slpc, "localization", "LangPack-Core", table[i]["lang"], table[i]["lang"], table[i]["langname"], "Core Localization support", "Core Meta-package to install default font, glibc locale and input-method if available.")
    slp = defappstream_body(slp, "localization", "LangPack", table[i]["lang"], table[i]["lang"], table[i]["langname"], "Localization support", "Meta-package to install available langpacks for the language available for the installed packages.")
    sdf = defappstream_body(sdf, "font", "default-fonts", table[i]["lang"], table[i]["fclang"], table[i]["langname"], "Localization Font support", "Core font package to install default font.")
    slf = defappstream_body(slf, "font", "langpacks-fonts", table[i]["lang"], table[i]["fclang"], table[i]["langname"], "Localization Font support", "Meta-package to install extra font.")
  end

  rpm.define("langpacks_metainfo_lpc " .. defappstream_close(slpc))
  rpm.define("langpacks_metainfo_lp " .. defappstream_close(slp))
  rpm.define("langpacks_metainfo_df " .. defappstream_close(sdf))
  rpm.define("langpacks_metainfo_lf " .. defappstream_close(slf))
end

local other_deps = { sans={}, serif={}, mono={} }
local cjk_deps = { sans={}, serif={}, mono={} }
local face = { "sans", "serif", "mono" }
local core_langs = {}
local core_deps = {}
local cjk_langs = {}
local cjk_sans_deps = {}

for i = 1, #langpacks_package_list do
  -- dependency list for default-fonts-<lang>
  local default_deps = {}
  -- dependency list for langpacks-fonts-<lang>
  local extra_deps = {}
  local lang = langpacks_package_list[i]["lang"]
  rpm.define("langcode " .. lang .. "\n")
  local orth = rpm.expand("%(python3 %{SOURCE4} %{langcode})")
  rpm.undefine("langcode")
  local lowerorth = string.lower(orth)
  local normlang = string.gsub(string.lower(lang), "_", "-")
  local langname = langpacks_package_list[i]["langname"]
  local im = (tonumber(rpm.expand("0%{?fedora}")) ~= 0 and langpacks_package_list[i]["fedora_inputmethod"] ~= nil and langpacks_package_list[i]["fedora_inputmethod"] or langpacks_package_list[i]["inputmethod"])
  local fclang = (langpacks_package_list[i]["fclang"] == "" and string.gsub(lang, "_", "-") or langpacks_package_list[i]["fclang"])
  local prov = ""

  if orth ~= "" then
    --Try to validate orth in table
    if fclang ~= orth then
      print(rpm.expand("%{error:fclang value is invalid for " .. lang .. "}"))
    end
  end

  if langpacks_package_list[i]["default"] ~= nil then
    local has_default = false
    local default_face = langpacks_package_list[i]["default"]["face"] and langpacks_package_list[i]["default"]["face"] or "sans"
    for j = 1, #face do
      local current = {langpacks_package_list[i]["default"][face[j]]}
      if current[1] ~= "" then
        has_default = true
      end
    end
    for j = 1, #face do
      local current = (has_default and {langpacks_package_list[i]["default"][face[j]]} or (is_cjk(lang) and core_font_package_list["cjk"][face[j]] or core_font_package_list["default"][face[j]]))

      -- Only install a font which is set by "face" or "sans" if not, for default-fonts-<language code>
      if face[j] == default_face then
        for k = 1, #current do
          table.insert(default_deps, current[k])
        end
        -- Make sure default-fonts-<language code> pulled in by langpacks-fonts-<language code>
        table.insert(extra_deps, "default-fonts-" .. string.gsub(fclang, "-", "_") .. " = %{version}-%{release}")
        -- Provide font(:lang=) deps for default face only
        prov = append_fontprov("", lowerorth)

        if is_nonlatin(lang) then
          if is_cjk(lang) then
            table.insert(cjk_deps[face[j]], "default-fonts-" .. string.gsub(fclang, "-", "_") .. " = %{version}-%{release}")
          else
            table.insert(other_deps[face[j]], "default-fonts-" .. string.gsub(fclang, "-", "_") .. " = %{version}-%{release}")
          end
        end
      else
        for k = 1, #current do
          table.insert(extra_deps, current[k])

          if is_cjk(lang) then
            table.insert(cjk_deps[face[j]], current[k])
          else
            table.insert(other_deps[face[j]], current[k])
          end
        end
      end
    end

    default_deps = build_deps(prov, "Requires", drop_duplicate(default_deps))
    extra_deps = build_deps("", "Requires", drop_duplicate(extra_deps))
  end
  if (tonumber(rpm.expand("0%{?fedora}")) ~= 0 and langpacks_package_list[i]["recommends"] ~= nil) then
    extra_deps = build_deps(extra_deps, "Recommends", drop_duplicate(langpacks_package_list[i]["recommends"]))
  end

  --Generate extra font package only when lang is recognized by fontconfig
  if lowerorth == normlang then
    -- Integrate default-fonts-<language code> into default-fonts-core-sans
    -- if it is a latin language and no default fonts is set
    if not is_nonlatin(lang) then
      if has_default then
        -- We may need to take care of them separately.
        table.insert(core_deps, "default-fonts-" .. lang .. " = %{version}-%{release}")
      else
        table.insert(core_langs, lang)
      end
    else
      if is_cjk(lang) then
        if has_default then
          -- We may need to take care of them separately.
          table.insert(cjk_sans_deps, "default-fonts-" .. lang .. " = %{version}-%{release}")
          deffontpkg("default-fonts-" .. lang, "default fonts", langname, append_obsolete(default_deps, "langpacks-core-font-" .. lang))
        else
          table.insert(cjk_langs, lang)
        end
      else
        deffontpkg("default-fonts-" .. lang, "default fonts", langname, append_obsolete(default_deps, "langpacks-core-font-" .. lang))
      end
    end
    deffontpkg("langpacks-fonts-" .. lang, "extra fonts", langname, append_obsolete(extra_deps, "default-fonts-extra-" .. lang))
  end
  defcorepkg(lang, fclang, langname, im)

  --Generate langpacks-* meta packages
  local metadeps = (tonumber(rpm.expand("0%{?fedora}")) ~= 0 and langpacks_package_list[i]["meta"]["fedora_requires"] ~= nil and langpacks_package_list[i]["meta"]["fedora_requires"] or langpacks_package_list[i]["meta"]["requires"])
  local metarecd = (tonumber(rpm.expand("0%{?fedora}")) ~= 0 and langpacks_package_list[i]["meta"]["fedora_recommends"] ~= nil and langpacks_package_list[i]["meta"]["fedora_recommends"] or langpacks_package_list[i]["meta"]["recommends"])
  local deps = build_deps("", "Requires", drop_duplicate(metadeps))
  deps = build_deps(deps, "Recommends", drop_duplicate(metarecd))
  defmetapkg(lang, fclang, langname, deps)
end

--Generate AppStream files
defappstream(langpacks_package_list)

--Special care of cjk-sans to reduce extra sub-packages and dependencies like core-sans
for i = 1, #core_font_package_list["cjk"]["sans"] do
  table.insert(cjk_sans_deps, core_font_package_list["cjk"]["sans"][i])
end
defsansfontpkg("cjk", "CJK languages", cjk_langs, cjk_sans_deps)

for i = 1, #face do
  deffontpkg("default-fonts-other-" .. face[i], "default " .. face[i] .. " fonts", "non-CJK languages", build_deps("", "Requires", drop_duplicate(other_deps[face[i]])))
  if face[i] ~= "sans" then
    deffontpkg("default-fonts-cjk-" .. face[i], "default " .. face[i] .. " fonts", "CJK languages", build_deps("", "Requires", drop_duplicate(cjk_deps[face[i]])))
  end
end

--core font packages except sans - core-sans may want to have special deps to default-fonts-<language code>
for i = 1, #core_font_package_list["default"]["sans"] do
  table.insert(core_deps, core_font_package_list["default"]["sans"][i])
end
defsansfontpkg("core", "Western characters", core_langs, core_deps)

local coreface = { "serif", "mono", "emoji", "math" }
for i = 1, #coreface do
  local sum1 = "default " .. coreface[i] .. " fonts"
  local sum2 = "Western characters"
  if coreface[i] == "emoji" or coreface[i] == "math" then
    sum1 = "default fonts"
    sum2 = coreface[i]:gsub("^%l", string.upper)
  end
  deffontpkg("default-fonts-core-" .. coreface[i], sum1, sum2, build_deps("", "Requires", drop_duplicate(core_font_package_list["default"][coreface[i]])))
end
} # %%{lua:}

%package -n default-fonts
Summary: Meta package to install all the default fonts
Requires: default-fonts-core = %{version}-%{release}
Requires: default-fonts-cjk = %{version}-%{release}
Requires: default-fonts-other = %{version}-%{release}

%description -n default-fonts
This package provides easier way to install all the default fonts meta packages
for all the languages.

%files -n default-fonts
%{_datadir}/metainfo/org.fedoraproject.default-fonts.metainfo.xml

%package -n default-fonts-core
Summary: Meta package to install sans/serif/mono/emoji/math default fonts meta packages for Western characters
Requires: default-fonts-core-sans = %{version}-%{release}
Requires: default-fonts-core-serif = %{version}-%{release}
Requires: default-fonts-core-mono = %{version}-%{release}
Requires: default-fonts-core-emoji = %{version}-%{release}
Requires: default-fonts-core-math = %{version}-%{release}

%description -n default-fonts-core
This package provides easier way to install all variants of default fonts
meta packages for Western characters.

%files -n default-fonts-core
%{_datadir}/metainfo/org.fedoraproject.default-fonts-core.metainfo.xml

%package -n default-fonts-cjk
Summary: Meta package to install sans/serif/mono/emoji/math default fonts meta packages for CJK
Requires: default-fonts-cjk-sans = %{version}-%{release}
Requires: default-fonts-cjk-serif = %{version}-%{release}
Requires: default-fonts-cjk-mono = %{version}-%{release}

%description -n default-fonts-cjk
This package provides easier way to install all variants of default fonts
meta packages for CJK languages.

%files -n default-fonts-cjk
%{_datadir}/metainfo/org.fedoraproject.default-fonts-cjk.metainfo.xml

%package -n default-fonts-other
Summary: Meta package to install sans/serif/mono/emoji/math default fonts meta packages for non-CJK
Requires: default-fonts-other-sans = %{version}-%{release}
Requires: default-fonts-other-serif = %{version}-%{release}
Requires: default-fonts-other-mono = %{version}-%{release}

%description -n default-fonts-other
This package provides easier way to install all variants of default fonts
meta packages for non-CJK languages.

%files -n default-fonts-other
%{_datadir}/metainfo/org.fedoraproject.default-fonts-other.metainfo.xml


%prep
# nothing to prep

%build
%{langpacks_metainfo_lpc}
%{langpacks_metainfo_lp}
%{langpacks_metainfo_df}
%{langpacks_metainfo_lf}


%install
# Explode the metainfo files into the subpackages so they get added to the
# distro-specific AppStream metadata
mkdir -p %{buildroot}/usr/share/metainfo
DESTDIR=%{buildroot} appstream-util split-appstream org.fedoraproject.LangPacks-Core.xml
DESTDIR=%{buildroot} appstream-util split-appstream org.fedoraproject.LangPacks.xml
DESTDIR=%{buildroot} appstream-util split-appstream org.fedoraproject.default-fonts.xml
DESTDIR=%{buildroot} appstream-util split-appstream org.fedoraproject.langpacks-fonts.xml

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jan 21 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 4.2-4
- Recommend ibus-cangjie only on Fedora

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 14 2024 Mike FABIAN <mfabian@redht.com> - 4.2-2
- Resolves: rhbz#2310426 Add ibus-cangjie-engine-cangjie and ibus-cangjie-engine-quick as recommends for zh_HK

* Tue Oct 22 2024 Akira TAGOH <tagoh@redhat.com> - 4.2-1
- Add sub-packages:
  - got for Gothic
  - kab for Kabyle
  - nqo for N'Ko
  - syr for Syriac

* Tue Aug 13 2024 Akira TAGOH <tagoh@redhat.com> - 4.1-3
- Update package names for renaming
  google-noto-sans-symbols2-fonts -> google-noto-sans-symbols-2-fonts
  google-noto-sans-meeteimayek-vf-fonts -> google-noto-sans-meetei-mayek-vf-fonts

* Wed Jul 17 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.1-2
- zh_TW: change default inputmethod to ibus-chewing
  https://fedoraproject.org/wiki/Changes/IBusChewingForZhTW

* Wed Jun 19 2024 Jens Petersen <petersen@redhat.com> - 4.1-1
- make IME installation condition on service(graphical-login)
  instead of xorg-x11-server-Xorg (RHEL-36747)

* Fri Jun  7 2024 Jens Petersen <petersen@redhat.com> - 4.0-14
- drop sil-mingzat-fonts recommends from fonts-en
- use Hebrew fonts for Yiddish (#2284093)

* Thu Apr 25 2024 Akira TAGOH <tagoh@redhat.com> - 4.0-13
- Add some conditional for RHEL.

* Fri Feb 02 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.0-12
- Added langpacks for sat and mni languages (#2259991 and #2259995)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 23 2023 Akira TAGOH <tagoh@redhat.com> - 4.0-9
- Drop google-noto-naskh-arabic-vf-fonts from langpacks-fonts-pa.
  Resolves: rhbz#2225410

* Fri Aug 11 2023 Peng Wu <pwu@redhat.com> - 4.0-8
- Update for the tlwg-fonts package

* Fri Aug  4 2023 Akira TAGOH <tagoh@redhat.com> - 4.0-7
- Update Indic fonts.
  https://fedoraproject.org/wiki/Changes/Indic_Noto_fonts

* Thu Jul 27 2023 Akira TAGOH <tagoh@redhat.com> - 4.0-6
- Add google-noto-sans-mono-cjk-vf-fonts as mono for CJK.

* Mon Jul 24 2023 Akira TAGOH <tagoh@redhat.com> - 4.0-5
- Simplified sub-packages and dependencies for CJK.
- Update serif font to google-noto-serif-gurmukhi-vf-fonts for Punjabi.
  the original serif font for Punjabi, google-noto-naskh-arabic-vf-fonts was
  figured out for Punjabi(Pakistan). but we don't have langpacks-pa_pk.
  So updating based on Punjabi(Indic).

* Fri Jul 21 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.0-4
- Fix wrong deps in langpacks-LL (zh languages) by Akira Tagoh

* Fri Jul 21 2023 Akira TAGOH <tagoh@redhat.com> - 4.0-3
- Drop extra dependencies for ELN which is a regression.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Akira TAGOH <tagoh@redhat.com> - 4.0-1
- Bump the version to 4.0.
  https://fedoraproject.org/wiki/Changes/ImproveDefaultFontHandling
- New default-fonts metapackages.
- Remove langpacks-core-font-* metapackages.

* Tue Jun 13 2023 Peng Wu <pwu@redhat.com> - 3.0-35
- Rename thai-scalable-fonts to tlwg-fonts

* Thu Jun  8 2023 Jens Petersen <petersen@redhat.com> - 3.0-34
- revert Urdu default font to paktype-naskh-basic-fonts

* Wed Jun 07 2023 Parag Nemade <pnemade AT redhat DOT Com > - 3.0-33
- Resolves:rhbz#2213106 - Fix rawhide compose by changing default sans for ur language

* Fri Apr  7 2023 Peng Wu <pwu@redhat.com> - 3.0-32
- Rebuild the langpacks package for Fedora 38

* Wed Feb  8 2023 Peng Wu <pwu@redhat.com> - 3.0-31
- Update for Noto CJK Variable Fonts
- https://fedoraproject.org/wiki/Changes/Noto_CJK_Variable_Fonts

* Fri Feb 03 2023 Akira TAGOH <tagoh@redhat.com> - 3.0-30
- Update for https://fedoraproject.org/wiki/Changes/NotoFontsForMoreLang
- Drop outdated google-noto-fonts packages.

* Thu Jan 19 2023 Parag Nemade <pnemade AT redhat DOT com> - 3.0-29
- Add serif fonts to some langpacks packages

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Parag Nemade <pnemade AT redhat DOT com> - 3.0-27
- Update license tag to SPDX format

* Wed Aug 03 2022 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 3.0-26
- langpacks-fa: use vazirmatn-vf-fonts as the default font and recommends Noto
  Naskh font

* Tue Aug  2 2022 Jens Petersen <petersen@redhat.com> - 3.0-25
- Hebrew: recommend Noto Serif not Rashi (#2113077)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 17 2022 Jens Petersen <petersen@redhat.com> - 3.0-23
- langpacks-en recommends Noto Serif and Noto Sans Mono fonts

* Tue Mar 08 2022 Akira TAGOH <tagoh@redhat.com> - 3.0-22
- langpacks-ar: Requires: google-noto-naskh-arabic-vf-fonts instead of
  google-noto-sans-arabic-vf-fonts.
- langpacks-ar: Add Recommends: google-noto-sans-arabic-vf-fonts.

* Tue Feb 01 2022 Mike FABIAN <mfabian@redhat.com> - 3.0-21
- zh_HK: add ibus-table-chinese-quick
- zh_TW: add ibus-table-chinese-cangjie, add ibus-table-chinese-quick

* Mon Jan 24 2022 Parag Nemade <pnemade AT redhat DOT com> - 3.0-20
- langpacks-th: Add Recommends: thai-scalable-laksaman-fonts (#2035607)

* Fri Jan 21 2022 Akira TAGOH <tagoh@redhat.com> - 3.0-19
- Replace dejavu to google-noto (#2041929)
  https://fedoraproject.org/wiki/Changes/DefaultToNotoFonts
- Add more sub-packages to make sure the upgrade-path for Noto Default:
  Cherokee, Divehi, Armenian, Inuktitut, Lao

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 03 2022 Rajeesh K V <rajeeshknambiar AT fedoraproject DOT org> - 3.0-17
- Update default fonts for Malayalam (#2036378)

* Tue Nov 30 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.0-16
- Resolves: Change pa language default font, https://pagure.io/i18n/issue/146

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 10 2021 Jens Petersen <petersen@redhat.com> - 3.0-14
- ja: use ibus-anthy
- zh_HK: use ibus-table-chinese-cangjie

* Mon Mar  8 2021 Jens Petersen <petersen@redhat.com> - 3.0-13
- add subpackages for Hong Kong (zh_HK)

* Tue Feb 23 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.0-12
- Revert previous ibus-unikey change for RHEL

* Mon Feb 22 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.0-11
- Move Vietnamese to use ibus-unikey as default IME (#1913431)

* Sat Feb 20 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.0-10
- Add more entries to previous commit

* Thu Feb 18 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.0-9
- Don't Recommends: packages in RHEL which are not available

* Mon Feb 15 2021 Parag Nemade <pnemade AT redhat DOT com> - 3.0-8
- Change default for Sinhala and Vietnamese to use ibus-m17n keymaps for Fedora

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 17 2020 Parag Nemade <pnemade AT redhat DOT com> - 3.0-6
- Change default for Sinhala and Vietnamese to use ibus-m17n keymaps

* Wed Sep 16 2020 Parag Nemade <pnemade AT redhat DOT com> - 3.0-5
- Resolves: Fix broken dependency for langpacks-core-font-km (#1879141)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 11 2020 Akira TAGOH <tagoh@redhat.com> - 3.0-3
- Stop shipping core-font sub-packages in lowercase and keep same naming as others.

* Tue Feb  4 2020 Akira TAGOH <tagoh@redhat.com> - 3.0-2
- Revert font(familyname) dependency to fix some regressions.

* Wed Jan 22 2020 Parag Nemade <pnemade AT redhat DOT com> - 3.0-1
- Added AppStream metainfo files for -core and -core-font subpackages
- Use fontconfig API to normalize the langcode
  and sub-package core-font based on ortho (By Akira Tagoh)
- Use dependencies as font(familyname) instead of actual package names
- Added Provides: in langcore_pkg macro (#1792463)
- Added -core-font-xx subpackages

* Wed Sep 11 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.0-7
- Fix typo (#1751242)

* Thu Aug 29 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.0-6
- Fix the issue detected in rpmdeplint report

* Mon Aug 12 2019 Akira TAGOH <tagoh@redhat.com> - 2.0-5
- Replace non variable fonts to variable fonts. (#1739976)

* Mon Jul 29 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.0-4
- Resolves:rh#1733929 - 'Requires:' to 'Recommends:' for additional fonts in base langpacks

* Fri Jul 26 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.0-3
- Resolves:rh#1554988 - google-noto-sans-gurmkukhi-fonts default for Punjabi

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.0-1
- Should have bumped the version to 2.0 in last build

* Mon Jul 22 2019 Parag Nemade <pnemade AT redhat DOT com> - 1.0-18
- Implement F31 Change (rh#1732123)
- Improve langname expansion macro from Jens Petersen
- macronize langpacks-core-* subpackages
- Correct the fonts entry for -core packages
- for now no Recommends: but Requires:

* Fri Apr 12 2019 Parag Nemade <pnemade AT redhat DOT com> - 1.0-17
- Resolves: rh#1699210 - langpack-pa: add "Recommends: google-noto-sans-gurmukhi-fonts"

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Parag Nemade <pnemade AT redhat DOT com> - 1.0-15
- Added few new subpackages for bo, dz, ka, km, ku, my, yi
- Added entry for above languages in org.fedoraproject.LangPacks.xml
- Enhance few langpacks to pull input-method packages
- Enhance few langpacks to pull font packages

* Thu Nov 08 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.0-14
- Resolves:rh#1644736: Added eo (Esperanto) language

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 01 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.0-11
- Added description in appdata metainfo files (rh#1538105)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 15 2016 Richard Hughes <richard@hughsie.com> - 1.0-8
- Use a specific AppStream component type of localization.

* Mon Feb 29 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.0-7
- Resolves:rh#1312890: langpacks-en should be added

* Fri Feb 26 2016 Richard Hughes <richard@hughsie.com> - 1.0-6
- Explode the metainfo files into the subpackages so they get added to the
  distro-specific AppStream metadata.
- This allows us to add and remove languages in GNOME Software.

* Tue Feb 23 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.0-5
- Resolves:rh#1310538: Added br ga he nn nr ss tn ts ve xh languages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.0-3
- Removed %%files to disable langpacks.noarch package

* Tue Jan 26 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.0-2
- Changed metapackage -> meta-package
- Added information about how we chose language list

* Thu Jan 21 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.0-1
- Initial packaging
