# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global cionly 0

%global _fontname google-noto
%global fontname %{_fontname}
%global fontconf %{_fontname}
%global common_desc Noto fonts aims to remove tofu from web by providing fonts for all \
Unicode supported scripts. Its design goal is to achieve visual harmonization\
between multiple scripts. Noto family supports almost all scripts available\
in Unicode.\
%{nil}

%global srcver	2025.11.01
%global majorver	%{lua: v, _ = string.gsub(rpm.expand("%{srcver}"), "(%d+)%.%d+%.%d+", "%1"); print(v)}
%global minorver	%{lua: v, _ = string.gsub(rpm.expand("%{srcver}"), "%d+%.(%d+)%.%d+", "%1"); print(v)}
%global patchver	%{lua: v, _ = string.gsub(rpm.expand("%{srcver}"), "%d+%.%d+%.(%d+)", "%1"); print(v)}
%global rpmver	%{lua: print(string.format("%04d%02d%02d", tonumber(rpm.expand("%{majorver}")), tonumber(rpm.expand("%{minorver}")), tonumber(rpm.expand("%{patchver}"))))}
# for default font
%global hprio	56
# for default font but static
%global	shprio	57
# for non-default
%global mprio	58
# for non-default and rarely used font
%global lprio	62
# for non-latin and default
%global	nlat_hprio	65-0
# for non-latin and default but static
%global	nlat_shprio	65-2
# for non-latin and non-default
%global	nlat_mprio	66
# for non-latin and non-default and rarely used font
%global	nlat_lprio	67

Name:           %{fontname}-fonts
Version:        %{rpmver}
Release: 3%{?dist}
Summary:        Hinted and Non Hinted OpenType fonts for Unicode scripts
License:        OFL-1.1
URL:            https://notofonts.github.io/
Source0:        https://github.com/notofonts/notofonts.github.io/archive/refs/tags/noto-monthly-release-%{srcver}.zip
Source1:        google-noto-sans-math-vf.conf
Source2:        google-noto-sans-math.conf
Source3:        google-noto-naskh-arabic-ex.conf
Source4:        google-noto-znamenny-musical-notation.conf
Source8:	google-noto-sans-sinhala-ex.conf

BuildArch:      noarch
BuildRequires:  fonts-rpm-macros
Requires:       fontpackages-filesystem

%description
%common_desc


%package common
Summary:        Common files for Noto fonts

%description common
Common files for Google Noto fonts.

%{lua:
-- To make lua-mode happy: '
local group = {}
group["sans-serif"] = "Noto Sans"
group["serif"] = "Noto Serif"
group["monospace"] = "Noto Sans Mono"

--
--alias: string: generic alias name
--family: string: font family name
--lang: array: lang code font family support
--fcconffile: string: fontconfig config file to package instead of auto-generated
--fcconfexfile: string: extra fontconfig config file to be added to auto-generated
--obsoletes: array: outdated package name to replace by
--default: bool: Wheter font is default or not
--variable: bool: Wheter font is variable or not
--priority: int: priority number for fontconfig config file
--fallback: array: alias name for fallback. similarly work for 'alias' but no rules for family->alias
--
local subpackages = {
    { alias="cursive",    family="Nastaliq Urdu", lang={ "ur" } },
    { alias="cursive",    family="Rashi Hebrew", lang={ "he" },
      default=true
    },

    { alias="fangsong",   family="Fangsong KSS Rotated" },
    { alias="fangsong",   family="Fangsong KSS Vertical" },

    { alias="fantasy",    family="Music" },
    { alias="fantasy",    family="Sans Symbols" },
    { alias="fantasy",    family="Sans Symbols 2",
      obsoletes={ "sans-symbols2" },
    },

    { alias="sans-serif", family="Kufi Arabic" },

    { alias="sans-serif", family="Sans",
      obsoletes={ "sans-ui", "sans-display" },
      default=true
    },
    { alias="sans-serif", family="Sans Adlam" },
    { alias="sans-serif", family="Sans Adlam Unjoined" },
    { alias="sans-serif", family="Sans Anatolian Hieroglyphs",
      obsoletes={ "sans-anatolian-hieroglyphs-vf" }
    },
    { alias="sans-serif", family="Sans Arabic",
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Arabic UI",
      priority=rpm.expand('%{lprio}'), nogroup=1,
    },
    { alias="sans-serif", family="Sans Armenian", lang={ "hy" },
      default=true
    },
    { alias="sans-serif", family="Sans Avestan",
      obsoletes={ "sans-avestan-vf" }
    },
    { alias="sans-serif", family="Sans Balinese", lang={ "ban" } },
    { alias="sans-serif", family="Sans Bamum", lang={ "bax" } },
    { alias="sans-serif", family="Sans Bassa Vah" },
    { alias="sans-serif", family="Sans Batak", lang={ "bbc" } },
    { alias="sans-serif", family="Sans Bengali", lang={ "as", "bn", "mni" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Bengali UI", lang={ "as", "bn", "mni" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
      obsoletes={ "sans-bengali-ui-vf" },
    },
    { alias="sans-serif", family="Sans Bhaiksuki" },
    { alias="sans-serif", family="Sans Brahmi" },
    { alias="sans-serif", family="Sans Buginese", lang={ "bug" },
      obsoletes={ "sans-buginese-vf" }
    },
    { alias="sans-serif", family="Sans Buhid", lang={ "bku" },
      obsoletes={ "sans-buhid-vf" }
    },
    { alias="sans-serif", family="Sans Canadian Aboriginal", lang={ "iu" },
      default=true
    },
    { alias="sans-serif", family="Sans Caucasian Albanian" },
    { alias="sans-serif", family="Sans Carian",
      obsoletes={ "sans-carian-vf" }
    },
    { alias="sans-serif", family="Sans Chakma" },
    { alias="sans-serif", family="Sans Cham", lang={ "cjm" } },
    { alias="sans-serif", family="Sans Cherokee", lang={ "chr" },
      default=true
    },
    { alias="sans-serif", family="Sans Chorasmian" },
    { alias="sans-serif", family="Sans Coptic", lang={ "cop" } },
    { alias="sans-serif", family="Sans Cuneiform", lang={ "slv" },
      obsoletes={ "sans-cuneiform-vf" }
    },
    { alias="sans-serif", family="Sans Cypriot",
      obsoletes={ "sans-cypriot-vf" }
    },
    { alias="sans-serif", family="Sans Cypro Minoan" },
    { alias="sans-serif", family="Sans Deseret",
      obsoletes={ "sans-deseret-vf" }
    },
    { alias="sans-serif", family="Sans Devanagari", lang={ "bh", "bho", "brx", "doi", "hi", "hne", "kok", "ks@devanagari", "mai", "mr", "ne", "sa", "sat", "sd@devanagari" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Devanagari UI", lang={ "bh", "bho", "brx", "doi", "hi", "hne", "kok", "ks@devanagari", "mai", "mr", "ne", "sa", "sat", "sd@devanagari" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
      obsoletes={ "sans-devanagari-ui-vf" }
    },
    { alias="sans-serif", family="Sans Duployan" },
    { alias="sans-serif", family="Sans Egyptian Hieroglyphs",
      obsoletes={ "sans-egyptian-hieroglyphs-vf" }
    },
    { alias="sans-serif", family="Sans Elbasan" },
    { alias="sans-serif", family="Sans Elymaic",
      obsoletes={ "sans-elymaic-vf" }
    },
    { alias="sans-serif", family="Sans Ethiopic", lang={ "am", "byn", "gez", "sid", "ti-er", "ti-et", "tig", "wal" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Georgian", lang={ "ka" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Glagolitic" },
    { alias="sans-serif", family="Sans Gothic", lang={ "got" },
      obsoletes={ "sans-gothic-vf" }
    },
    { alias="sans-serif", family="Sans Grantha" },
    { alias="sans-serif", family="Sans Gujarati", lang={ "gu" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Gujarati UI", lang={ "gu" },
      priority=rpm.expand('%{lprio}'), nogroup=1
    },
    { alias="sans-serif", family="Sans Gunjala Gondi" },
    { alias="sans-serif", family="Sans Gurmukhi", lang={ "pa" },
      default=true
    },
    { alias="sans-serif", family="Sans Gurmukhi UI", lang={ "pa" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
      obsoletes={ "sans-gurmukhi-ui-vf" },
    },
    { alias="sans-serif", family="Sans Hanifi Rohingya" },
    { alias="sans-serif", family="Sans Hanunoo", lang={ "hnn" },
      obsoletes={ "sans-hanunno" }
    },
    { alias="sans-serif", family="Sans Hatran",
      obsoletes={ "sans-hatran-vf" }
    },
    { alias="sans-serif", family="Sans Hebrew", lang={ "he", "yi" },
      obsoletes={ "sans-hebrew-droid", "sans-hebrew-new" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Imperial Aramaic",
      obsoletes={ "sans-imperial-aramaic-vf" }
    },
    { alias="sans-serif", family="Sans Indic Siyaq Numbers" },
    { alias="sans-serif", family="Sans Inscriptional Pahlavi" },
    { alias="sans-serif", family="Sans Inscriptional Parthian" },
    { alias="sans-serif", family="Sans Javanese" },
    { alias="sans-serif", family="Sans Kaithi" },
    { alias="sans-serif", family="Sans Kannada", lang={ "kn" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Kannada UI", lang={ "kn" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
    },
    { alias="sans-serif", family="Sans Kawi" },
    { alias="sans-serif", family="Sans Kayah Li" },
    { alias="sans-serif", family="Sans Kharoshthi" },
    { alias="sans-serif", family="Sans Khmer", lang={ "km" },
      obsoletes={ "sans-khmer-ui" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Khojki" },
    { alias="sans-serif", family="Sans Khudawadi" },
    { alias="sans-serif", family="Sans Lao", lang={ "lo" },
      obsoletes={ "sans-lao-ui" },
      default=true
    },
    { alias="sans-serif", family="Sans Lao Looped", lang={ "lo" }, nogroup=1,
      obsoletes={ "looped-lao", "looped-lao-ui" },
    },
    { alias="sans-serif", family="Sans Lepcha", lang={ "lep" } },
    { alias="sans-serif", family="Sans Limbu", lang={ "lif" } },
    { alias="sans-serif", family="Sans Linear A",
      obsoletes={ "sans-linear-a-vf" }
    },
    { alias="sans-serif", family="Sans Linear B",
      obsoletes={ "sans-linearb", "sans-linear-b-vf" }
    },
    { alias="sans-serif", family="Sans Lisu" },
    { alias="sans-serif", family="Sans Lycian",
      obsoletes={ "sans-lycian-vf" }
    },
    { alias="sans-serif", family="Sans Lydian",
      obsoletes={ "sans-lydian-vf" }
    },
    { alias="sans-serif", family="Sans Mahajani" },
    { alias="sans-serif", family="Sans Malayalam", lang={ "ml" } },
    { alias="sans-serif", family="Sans Malayalam UI", lang={ "ml" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
    },
    { alias="sans-serif", family="Sans Mandaic",
      obsoletes={ "sans-mandaic-vf" }
    },
    { alias="sans-serif", family="Sans Manichaean" },
    { alias="sans-serif", family="Sans Marchen",
      obsoletes={ "sans-marchen-vf" }
    },
    { alias="sans-serif", family="Sans Masaram Gondi" },
    { alias="sans-serif", family="Sans Math",
      priority=rpm.expand('%{lprio}'),
      obsoletes={ "sans-math-vf" }
    },
    { alias="sans-serif", family="Sans Mayan Numerals",
      obsoletes={ "sans-mayan-numerals-vf" }
    },
    { alias="sans-serif", family="Sans Meetei Mayek",
      obsoletes={ "sans-meeteimayek" }
    },
    { alias="sans-serif", family="Sans Medefaidrin" },
    { alias="sans-serif", family="Sans Mende Kikakui" },
    { alias="sans-serif", family="Sans Meroitic" },
    { alias="sans-serif", family="Sans Miao" },
    { alias="sans-serif", family="Sans Modi" },
    { alias="sans-serif", family="Sans Mongolian", lang={ "mn-cn" } },
    { alias="monospace",  family="Sans Mono",
      obsoletes={ "mono" },
      default=true
    },
    { alias="sans-serif", family="Sans Mro",
      obsoletes={ "sans-mro-vf" }
    },
    { alias="sans-serif", family="Sans Multani",
      obsoletes={ "sans-multani-vf" }
    },
    { alias="sans-serif", family="Sans Myanmar", lang={ "my" },
      obsoletes={ "sans-myanmar-ui" },
    },
    { alias="sans-serif", family="Sans Nabataean",
      obsoletes={ "sans-nabataean-vf" }
    },
    { alias="sans-serif", family="Sans Nag Mundari" },
    { alias="sans-serif", family="Sans Nandinagari" },
    { alias="sans-serif", family="Sans New Tai Lue", lang={ "khb" } },
    { alias="sans-serif", family="Sans Newa" },
    { alias="sans-serif", family="Sans NKo", lang={ "nqo" } },
    { alias="sans-serif", family="Sans NKo Unjoined", lang={ "nqo" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
    },
    { alias="sans-serif", family="Sans Nushu" },
    { alias="sans-serif", family="Sans Ogham", lang={ "pgl" },
      obsoletes={ "sans-ogham-vf" }
    },
    { alias="sans-serif", family="Sans Ol Chiki" },
    { alias="sans-serif", family="Sans Old Hungarian" },
    { alias="sans-serif", family="Sans Old Italic" },
    { alias="sans-serif", family="Sans Old North Arabian" },
    { alias="sans-serif", family="Sans Old Permic" },
    { alias="sans-serif", family="Sans Old Persian" },
    { alias="sans-serif", family="Sans Old Sogdian" },
    { alias="sans-serif", family="Sans Old South Arabian" },
    { alias="sans-serif", family="Sans Old Turkic" },
    { alias="sans-serif", family="Sans Oriya", lang={ "or" },
      obsoletes={ "sans-oriya-ui" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Osage" },
    { alias="sans-serif", family="Sans Osmanya",
      obsoletes={ "sans-osmanya-vf" }
    },
    { alias="sans-serif", family="Sans Pahawh Hmong" },
    { alias="sans-serif", family="Sans Palmyrene" },
    { alias="sans-serif", family="Sans Pau Cin Hau" },
    { alias="sans-serif", family="Sans PhagsPa",
      obsoletes={ "sans-phags-pa" },
    },
    { alias="sans-serif", family="Sans Phoenician",
      obsoletes={ "sans-phoenician-vf" }
    },
    { alias="sans-serif", family="Sans Psalter Pahlavi" },
    { alias="sans-serif", family="Sans Rejang", lang={ "rej" } },
    { alias="sans-serif", family="Sans Runic", lang={ "gem" },
      obsoletes={ "sans-runic-vf" },
    },
    { alias="sans-serif", family="Sans Samaritan" },
    { alias="sans-serif", family="Sans Saurashtra", lang={ "saz" } },
    { alias="sans-serif", family="Sans Sharada" },
    { alias="sans-serif", family="Sans Shavian", lang={ "en@shaw" },
      obsoletes={ "sans-shavian-vf" }
    },
    { alias="sans-serif", family="Sans Siddham" },
    { alias="sans-serif", family="Sans SignWriting" },
    { alias="sans-serif", family="Sans Sinhala", lang={ "si" },
      default=true, fallback={ "monospace" },
      fcconfexfile=rpm.expand('%{SOURCE8}')
    },
    { alias="sans-serif", family="Sans Sinhala UI", lang={ "si" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
      obsoletes={ "sans-sinhala-ui-vf" },
    },
    { alias="sans-serif", family="Sans Sogdian" },
    { alias="sans-serif", family="Sans Sora Sompeng" },
    { alias="sans-serif", family="Sans Soyombo",
      obsoletes={ "sans-soyombo-vf" }
    },
    { alias="sans-serif", family="Sans Sundanese" },
    { alias="sans-serif", family="Sans Sunuwar", lang={ "suz" } },
    { alias="sans-serif", family="Sans Syloti Nagri" },
    { alias="sans-serif", family="Sans Syriac", lang={ "syr" },
      obsoletes={ "sans-syriac-estrangela" }
    },
    { alias="sans-serif", family="Sans Syriac Eastern", lang={ "syr" } },
    { alias="sans-serif", family="Sans Syriac Western", lang={ "syr" } },
    { alias="sans-serif", family="Sans Tagalog" },
    { alias="sans-serif", family="Sans Tagbanwa", lang={ "twb" },
      obsoletes={ "sans-tagbanwa-vf" }
    },
    { alias="sans-serif", family="Sans Takri",
      obsoletes={ "sans-takri-vf" }
    },
    { alias="sans-serif", family="Sans Tai Le" },
    { alias="sans-serif", family="Sans Tai Tham" },
    { alias="sans-serif", family="Sans Tai Viet",
      obsoletes={ "sans-tai-viet-vf" },
    },
    { alias="sans-serif", family="Sans Tamil", lang={ "ta" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Tamil Supplement", lang={ "ta" },
      excludeci=true, nogroup=1
    },
    { alias="sans-serif", family="Sans Tamil UI", lang={ "ta" },
      priority=rpm.expand('%{lprio}'), nogroup=1
    },
    { alias="sans-serif", family="Sans Tangsa" },
    { alias="sans-serif", family="Sans Telugu", lang={ "te" },
      default=true, fallback= { "monospace" }
    },
    { alias="sans-serif", family="Sans Telugu UI", lang={ "te" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
    },
    { alias="sans-serif", family="Sans Thaana", lang={ "dv" },
      default=true
    },
    { alias="sans-serif", family="Sans Thai", lang={ "th" },
      obsoletes={ "sans-thai-ui" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", family="Sans Thai Looped", lang={ "th" },
      obsoletes={ "looped-thai", "looped-thai-ui" }
    },
    { alias="sans-serif", family="Sans Tifinagh", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tifinagh APT", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tifinagh Adrar", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tifinagh Agraw Imazighen", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tifinagh Ahaggar", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tifinagh Air", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tifinagh Azawagh", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tifinagh Ghat", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tifinagh Hawad", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tifinagh Rhissa Ixa", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tifinagh SIL", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tifinagh Tawellemmet", lang={ "ber-ma" } },
    { alias="sans-serif", family="Sans Tirhuta" },
    { alias="sans-serif", family="Sans Ugaritic",
      obsoletes={ "sans-ugaritic-vf" }
    },
    { alias="sans-serif", family="Sans Vai", lang={ "vai" },
      obsoletes={ "sans-vai-vf" }
    },
    { alias="sans-serif", family="Sans Vithkuqi" },
    { alias="sans-serif", family="Sans Wancho",
      obsoletes={ "sans-wancho-vf" }
    },
    { alias="sans-serif", family="Sans Warang Citi",
      obsoletes={ "sans-warang-citi-vf" }
    },
    { alias="sans-serif", family="Sans Yi",
      obsoletes={ "sans-yi-vf" }
    },
    { alias="sans-serif", family="Sans Zanabazar Square",
      obsoletes={ "sans-zanabazar-square-vf" },
    },

    { alias="serif",      family="Naskh Arabic",
      fcconfexfile=rpm.expand('%{SOURCE3}'),
      default=true
    },
    { alias="serif",      family="Naskh Arabic UI",
      priority=rpm.expand('%{lprio}')
    },
    { alias="serif",      family="Serif",
      obsoletes={ "serif-display" },
      default=true
    },
    { alias="serif",      family="Serif Ahom" },
    { alias="serif",      family="Serif Armenian", lang={ "hy" },
      default=true
    },
    { alias="serif",      family="Serif Balinese", lang={ "ban" },
      obsoletes={ "sans-balinese" }
    },
    { alias="serif",      family="Serif Bengali", lang={ "as", "bn", "mni" },
      default=true
    },
    { alias="serif",      family="Serif Devanagari", lang={ "bh", "bho", "brx", "doi", "hi", "hne", "kok", "ks@devanagari", "mai", "mr", "ne", "sa", "sat", "sd@devanagari" },
      default=true
    },
    { alias="serif",      family="Serif Dives Akuru" },
    { alias="serif",      family="Serif Dogra",
      obsoletes={ "serif-dogra-vf" },
    },
    { alias="serif",      family="Serif Ethiopic", lang={ "am", "byn", "gez", "sid", "ti-er", "ti-et", "tig", "wal" },
      default=true
    },
    { alias="serif",      family="Serif Georgian", lang={ "ka" },
      default=true
    },
    { alias="serif",      family="Serif Grantha" },
    { alias="serif",      family="Serif Gujarati", lang={ "gu" },
      default=true
    },
    { alias="serif",      family="Serif Gurmukhi", lang={ "pa" },
      default=true
    },
    { alias="serif",      family="Serif Hebrew", lang={ "he", "yi" } },
    { alias="serif",      family="Serif Hentaigana" },
    { alias="serif",      family="Serif Kannada", lang={ "kn" },
      default=true
    },
    { alias="serif",      family="Serif Khitan Small Script" },
    { alias="serif",      family="Serif Khmer", lang={ "km" },
      default=true
    },
    { alias="serif",      family="Serif Khojki" },
    { alias="serif",      family="Serif Lao", lang={ "lo" },
      default=true
    },
    { alias="serif",      family="Serif Makasar" },
    { alias="serif",      family="Serif Malayalam", lang={ "ml" } },
    { alias="serif",      family="Serif Myanmar", lang={ "my" } },
    { alias="serif",      family="Serif NP Hmong",
      obsoletes={ "serif-nyiakeng-puachue-hmong" },
    },
    { alias="serif",      family="Serif Old Uyghur" },
    { alias="serif",      family="Serif Oriya", lang={ "or" },
      default=true
    },
    { alias="serif",      family="Serif Ottoman Siyaq" },
    { alias="serif",      family="Serif Sinhala", lang={ "si" },
      default=true
    },
    { alias="serif",      family="Serif Tamil", lang={ "ta" },
      obsoletes={ "serif-tamil-slanted" },
      default=true
    },
    { alias="serif",      family="Serif Tangut",
      obsoletes={ "serif-tangut-vf" }
    },
    { alias="serif",      family="Serif Telugu", lang={ "te" },
      default=true
    },
    { alias="serif",      family="Serif Thai", lang={ "th" },
      default=true
    },
    { alias="serif",      family="Serif Tibetan", lang={ "bo", "dz" },
      obsoletes={ "sans-tibetan" }
    },
    { alias="serif",      family="Serif Todhri" },
    { alias="serif",      family="Serif Toto" },
    { alias="serif",      family="Serif Vithkuqi" },
    { alias="serif",      family="Serif Yezidi" },
    { alias="serif",      family="Traditional Nushu" },
    -- It may be symbol but is a part of. no alias is intentional.
    { alias="",           family="Znamenny Musical Notation",
      priority=rpm.expand('%{lprio}'), nogroup=1,
      fcconffile=rpm.expand('%{SOURCE4}'),
    },

    { alias="cursive",    variable=true, family="Nastaliq Urdu", lang={ "ur" } },
    { alias="cursive",    variable=true, family="Rashi Hebrew", lang={ "he" },
      default=true
    },

    { alias="fantasy",    variable=true, family="Sans Symbols" },

    { alias="sans-serif", variable=true, family="Kufi Arabic" },

    { alias="sans-serif", variable=true, family="Sans",
      obsoletes={ "sans-display-vf" },
      default=true
    },
    { alias="sans-serif", variable=true, family="Sans Adlam" },
    { alias="sans-serif", variable=true, family="Sans Adlam Unjoined" },
    { alias="sans-serif", variable=true, family="Sans Arabic",
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Arabic UI",
      priority=rpm.expand('%{lprio}'), nogroup=1,
    },
    { alias="sans-serif", variable=true, family="Sans Armenian", lang={ "hy" },
      default=true
    },
    { alias="sans-serif", variable=true, family="Sans Balinese", lang={ "ban" } },
    { alias="sans-serif", variable=true, family="Sans Bamum", lang={ "bax" } },
    { alias="sans-serif", variable=true, family="Sans Bassa Vah" },
    { alias="sans-serif", variable=true, family="Sans Bengali", lang={ "as", "bn", "mni" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Canadian Aboriginal", lang={ "iu" },
      default=true
    },
    { alias="sans-serif", variable=true, family="Sans Cham", lang={ "cjm" } },
    { alias="sans-serif", variable=true, family="Sans Cherokee", lang={ "chr" },
      default=true
    },
    { alias="sans-serif", variable=true, family="Sans Devanagari", lang={ "bh", "bho", "brx", "doi", "hi", "hne", "kok", "ks@devanagari", "mai", "mr", "ne", "sa", "sat", "sd@devanagari" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Ethiopic", lang={ "am", "byn", "gez", "sid", "ti-er", "ti-et", "tig", "wal" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Georgian", lang={ "ka" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Gujarati", lang={ "gu" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Gunjala Gondi" },
    { alias="sans-serif", variable=true, family="Sans Gurmukhi", lang={ "pa" },
      obsoletes={ "sans-gurkukhi-ui-vf" },
      default=true
    },
    { alias="sans-serif", variable=true, family="Sans Hanifi Rohingya" },
    { alias="sans-serif", variable=true, family="Sans Hebrew", lang={ "he", "yi" },
      obsoletes={ "sans-hebrew-droid-vf", "sans-hebrew-new-vf" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Javanese" },
    { alias="sans-serif", variable=true, family="Sans Kannada", lang={ "kn" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Kannada UI", lang={ "kn" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
      fontname="SansKannada-UI",
    },
    { alias="sans-serif", variable=true, family="Sans Kayah Li" },
    { alias="sans-serif", variable=true, family="Sans Kawi" },
    { alias="sans-serif", variable=true, family="Sans Khmer", lang={ "km" },
      obsoletes={ "sans-khmer-ui-vf" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Lao", lang={ "lo" },
      obsoletes={ "sans-lao-ui-vf" },
      default=true
    },
    { alias="sans-serif", variable=true, family="Sans Lao Looped", lang={ "lo" },
      obsoletes={ "looped-lao-vf", "looped-lao-ui-vf" }, nogroup=1,
    },
    { alias="sans-serif", variable=true, family="Sans Lisu" },
    { alias="sans-serif", variable=true, family="Sans Nag Mundari" },
    { alias="sans-serif", variable=true, family="Sans Malayalam", lang={ "ml" } },
    { alias="sans-serif", variable=true, family="Sans Malayalam UI", lang={ "ml" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
      fontname="SansMalayalam-UI",
    },
    { alias="sans-serif", variable=true, family="Sans Medefaidrin" },
    { alias="sans-serif", variable=true, family="Sans Meetei Mayek",
      obsoletes={ "sans-meeteimayek-vf" },
    },
    { alias="monospace", variable=true, family="Sans Mono",
      default=true
    },
    { alias="sans-serif", variable=true, family="Sans Myanmar", lang={ "my" },
      obsoletes={ "serif-myanmar-vf", "sans-myanmar-ui-vf" }
    },
    { alias="sans-serif", variable=true, family="Sans New Tai Lue", lang={ "khb" } },
    { alias="sans-serif", variable=true, family="Sans NKo Unjoined", lang={ "nqo" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
    },
    { alias="sans-serif", variable=true, family="Sans Ol Chiki" },
    { alias="sans-serif", variable=true, family="Sans Oriya", lang={ "or" },
      obsoletes={ "sans-oriya-ui-vf" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Sinhala", lang={ "si" },
      default=true, fallback={ "monospace" },
      fcconfexfile=rpm.expand('%{SOURCE8}')
    },
    { alias="sans-serif", variable=true, family="Sans Sora Sompeng" },
    { alias="sans-serif", variable=true, family="Sans Sundanese" },
    { alias="sans-serif", variable=true, family="Sans Syriac", lang={ "syr" } },
    { alias="sans-serif", variable=true, family="Sans Syriac Eastern", lang={ "syr" } },
    { alias="sans-serif", variable=true, family="Sans Syriac Western", lang={ "syr" } },
    { alias="sans-serif", variable=true, family="Sans Tai Tham" },
    { alias="sans-serif", variable=true, family="Sans Tamil", lang={ "ta" },
      obsoletes={ "sans-tamil-supplement-vf" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Tamil UI", lang={ "ta" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
      fontname="SansTamil-UI",
    },
    { alias="sans-serif", variable=true, family="Sans Tangsa" },
    { alias="sans-serif", variable=true, family="Sans Telugu", lang={ "te" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Telugu UI", lang={ "te" },
      priority=rpm.expand('%{lprio}'), nogroup=1,
      fontname="SansTelugu-UI",
    },
    { alias="sans-serif", variable=true, family="Sans Thaana", lang={ "dv" },
      default=true
    },
    { alias="sans-serif", variable=true, family="Sans Thai", lang={ "th" },
      obsoletes={ "sans-thai-ui-vf" },
      default=true, fallback={ "monospace" }
    },
    { alias="sans-serif", variable=true, family="Sans Thai Looped", lang={ "th" },
      obsoletes={ "sansthai-looped-vf",  "looped-thai-vf", "looped-thai-ui-vf" }
    },
    { alias="sans-serif", variable=true, family="Sans Vithkuqi" },
    { alias="serif",      variable=true, family="Naskh Arabic",
      fcconfexfile=rpm.expand('%{SOURCE3}'),
      default=true
    },
    { alias="serif",      variable=true, family="Naskh Arabic UI",
      priority=rpm.expand('%{lprio}'), nogroup=1
    },
    { alias="serif",      variable=true, family="Serif",
      obsoletes={ "serif-display-vf" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Armenian", lang={ "hy" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Bengali", lang={ "as", "bn", "mni" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Devanagari", lang={ "bh", "bho", "brx", "doi", "hi", "hne", "kok", "ks@devanagari", "mai", "mr", "ne", "sa", "sat", "sd@devanagari" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Ethiopic", lang={ "am", "byn", "gez", "sid", "ti-er", "ti-et", "tig", "wal" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Georgian", lang={ "ka" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Gujarati", lang={ "gu" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Gurmukhi", lang={ "pa" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Hebrew", lang={ "he", "yi" } },
    { alias="serif",      variable=true, family="Serif Hentaigana" },
    { alias="serif",      variable=true, family="Serif Kannada", lang={ "kn" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Khmer", lang={ "km" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Khojki" },
    { alias="serif",      variable=true, family="Serif Lao", lang={ "lo" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Malayalam", lang={ "ml" } },
    { alias="serif",      variable=true, family="Serif Myanmar", lang={ "my" } },
    { alias="serif",      variable=true, family="Serif NP Hmong",
      obsoletes={ "serif-nyiakeng-puachue-hmong-vf" },
    },
    { alias="serif",      variable=true, family="Serif Oriya", lang={ "or" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Sinhala", lang={ "si" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Tamil", lang={ "ta" },
      obsoletes={ "serif-tamil-slanted-vf" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Telugu", lang={ "te" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Thai", lang={ "th" },
      default=true
    },
    { alias="serif",      variable=true, family="Serif Tibetan", lang={ "bo", "dz" } },
    { alias="serif",      variable=true, family="Serif Toto" },
    { alias="serif",      variable=true, family="Serif Vithkuqi" },
    { alias="serif",      variable=true, family="Serif Yezidi" },
    { alias="serif",      variable=true, family="Traditional Nushu" },

}
local _fcconflist = ''
local _metafilelist = ''
local _fcconfbuild = ''
local _metainfobuild = ''
local _filelistbuild = ''

local function is_nonlatin(table)
    latin_langs = { "af", "ar", "az", "bs", "ca", "cs", "cy", "da", "de", "en", "es", "et", "fil", "fi", "fo", "fr", "ga", "gd", "gl", "hr", "hu", "id", "is", "it", "ka", "kk", "ky", "lb", "lt", "lv", "mk", "mont", "ms", "mt", "nl", "no", "pl", "pt", "ro", "sk", "sl", "sq", "sr", "sv", "sw", "tg", "tk", "tr", "uz" }
    if table.lang then
        for i = 1, #table.lang do
            for j = 1, #latin_langs do
                if table.lang[i] == latin_langs[j] then
                    return false
                end
            end
        end
    else
      return false
    end
    return true
end

local function _genfcconf(alias, family, lang, reverse)
    local ret = ""
    local generic = [[
    <test name="family">\
      <string>]] .. alias .. [[</string>\
    </test>\
    <edit name=\"family\" mode=\"prepend\">\
      <string>Noto ]] .. family .. [[</string>\
    </edit>\]]
    if lang then
        for i = 1, #lang do
            ret = ret .. [[  <match>\
    <test name=\"lang\" compare=\"contains\">\
      <string>]] .. lang[i] .. [[</string>\
    </test>\
]] .. generic .. "\n" .. [[
  </match>\
]]
        end
    else
        ret = ret .. [[  <match>\
]] .. generic .. "\n" .. [[
  </match>\
]]
    end
    if reverse then
        ret = ret .. [[
  <alias>\
    <family>Noto ]] .. family .. [[</family>\
    <default>\
      <family>]] .. alias .. [[</family>\
    </default>\
  </alias>\
]]
    end
    return ret
end

local function genfcconf(table)
    local extra = "\\\n"
    if table.fcconfexfile then
        local f = io.open(table.fcconfexfile, "r")
        if f then
            for line in f:lines() do
                extra = extra .. line:gsub("\n$", ""):gsub("$", "\\\n")
            end
            extra = extra:gsub("\n\n$", "\n")
            f:close()
        else
            error("Unable to open " .. table.fcconfexfile)
        end
    end
    local xml = [[
<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
<!DOCTYPE fontconfig SYSTEM \"urn:fontconfig:fonts.dtd\">\
<fontconfig>\
]]
    xml = xml .. _genfcconf(table.alias, table.family, table.lang, true)
    if table.fallback then
        for i = 1, #table.fallback do
            xml = xml .. _genfcconf(table.fallback[i], table.family, table.lang, false)
        end
    end
    xml = xml .. extra .. [[
</fontconfig>\
]]
    if table.fcconffile then
        local f = io.open(table.fcconffile, "r")
        if f then
            xml = ""
            for line in f:lines() do
                xml = xml .. line:gsub("\n$", ""):gsub("$", "\\\n")
            end
            xml = xml:gsub("\n\n$", "\n")
            f:close()
        else
            error("Unable to open " .. table.fcconffile)
        end
    end
    _fcconfbuild = _fcconfbuild .. "cat<<_EOL_>" .. table.fcconf .. "\\\n" .. xml .. "_EOL_\\\n"
end

-- Borrowed from fonts-rpm-macros
-- koji doesn't sasisfy BR during generating srpm yet.
-- We can't add a dependant code to fonts-rpm-macros at this stage.

-- https://github.com/rpm-software-management/rpm/issues/566
-- Reformat a text intended to be used used in a package description, removing
-- rpm macro generation artefacts.
-- – remove leading and ending empty lines
-- – trim intermediary empty lines to a single line
-- – fold on spaces
-- Should really be a %%{wordwrap:…} verb
local function wordwrap(text)
  text = rpm.expand(text .. "\n")
  text = string.gsub(text, "\t",              "  ")
  text = string.gsub(text, "\r",              "\n")
  text = string.gsub(text, " +\n",            "\n")
  text = string.gsub(text, "\n+\n",           "\n\n")
  text = string.gsub(text, "^\n",             "")
  text = string.gsub(text, "\n( *)[-*—][  ]+", "\n%1– ")
  output = ""
  for line in string.gmatch(text, "[^\n]*\n") do
    local pos = 0
    local advance = ""
    for word in string.gmatch(line, "%s*[^%s]*\n?") do
      local wl, bad = utf8.len(word)
      if not wl then
        print("%{warn:Invalid UTF-8 sequence detected in:}" ..
              "%{warn:" .. word .. "}" ..
              "%{warn:It may produce unexpected results.}")
        wl = bad
      end
      if (pos == 0) then
        advance, n = string.gsub(word, "^(%s*– ).*", "%1")
        if (n == 0) then
          advance = string.gsub(word, "^(%s*).*", "%1")
        end
        advance = string.gsub(advance, "– ", "  ")
        pos = pos + wl
      elseif  (pos + wl  < 81) or
             ((pos + wl == 81) and string.match(word, "\n$")) then
        pos = pos + wl
      else
        word = advance .. string.gsub(word, "^%s*", "")
        output = output .. "\n"
        pos = utf8.len(word)
      end
      output = output .. word
      if pos > 80 then
        pos = 0
        if not string.match(word, "\n$") then
          output = output .. "\n"
        end
      end
    end
  end
  output = string.gsub(output, "\n*$", "\n")
  return output
end

-- A helper to close AppStream XML runs
local function closetag(oldtag, newtag)
  if (oldtag == nil) then
    return ""
  else
    local output = "]]></" .. oldtag .. ">"
    if (oldtag == "li") and (newtag ~= oldtag) then
      output = output .. "</ul>"
    end
    return output
  end
end

-- A helper to open AppStream XML runs
local function opentag(oldtag, newtag)
  if (newtag == nil) then
    return ""
  else
    local output = "<" .. newtag .. "><![CDATA["
    if (newtag == "li") and (newtag ~= oldtag) then
      output = "<ul>" .. output
    end
    return output
  end
end

-- A helper to switch AppStream XML runs
local function switchtag(oldtag, newtag)
  return closetag(oldtag, newtag) .. opentag(oldtag, newtag)
end

-- Reformat some text into something that can be included in an AppStream
-- XML description
local function txt2xml(text)
  local        text = wordwrap(text)
  local      output = ""
  local     oldtag  = nil
  local oldadvance  = nil
  local      newtag = nil
  text = string.gsub(text, "^\n*", "")
  text = string.gsub(text, "\n*$", "\n")
  for line in string.gmatch(text, "[^\n]*\n") do
    local change = true
    local advance, n = string.gsub(line, "^(%s*– ).*", "%1")
    if (n == 1) then
      newtag = "li"
    else
      advance = string.gsub(line, "^(%s*).*", "%1")
      if (line == "\n") then
        newtag = nil
      elseif (advance ~= oldadvance) then
        newtag = "p"
      else
        change = false
      end
    end
    local result = ""
    if change then
      result     = string.gsub(line, "^" .. advance, switchtag(oldtag,newtag))
      oldtag     = newtag
      oldadvance = string.gsub(advance, "– ", "  ")
    else
      result = string.gsub(line, "^" .. advance, " ")
    end
    result = string.gsub(result, "\n$", "")
    output = output .. result
  end
  output = output .. closetag(oldtag, nil)
  return output
end

local function genmetainfo(table)
local xmlfontname = '$(cmd=$(for f in $(cd %{buildroot}/' .. table.fontdir .. ' && find -regex \'./' .. table.filename .. '\' -print); do fc-scan "%{buildroot}' .. table.fontdir .. '$f" -f "echo \\\\\"    <font>%{fullname[0]}</font>\\\\\";"; sync; done); if test x"$cmd" != x; then echo "echo \\\\\"  <provides>\\\\\"; $cmd echo \\\\\"  </provides>\\\\\""|sh; fi|grep -v "font></font")'
local xmlfontlang = '$(cmd=$(for f in $(cd %{buildroot}/' .. table.fontdir .. ' && find -regex \'./' .. table.filename .. '\' -print); do fc-scan "%{buildroot}' .. table.fontdir .. '$f" -f "%{[]lang{echo \\\\\"    <lang>%{lang}</lang>\\\\\";}}"; sync; done); if test x"$cmd" != x; then echo "echo \\\\\"  <languages>\\\\\"; ($cmd)|sort -u; echo \\\\\"  </languages>\\\\\""|sh; fi)'
local xml = [[
<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
<!-- $PDX-License-Identifier: MIT -->\
<component type=\"font\">\
  <id>]] .. rpm.expand("%{fontorg}.") .. table.pkgname .. [[</id>\
  <metadata_license>MIT</metadata_license>\
  <project_license>]] .. rpm.expand("%{license}") .. [[</project_license>\
  <name>Noto ]] .. table.family .. [[</name>\
  <summary><![CDATA[Noto ]] .. table.summary .. [[\]\]></summary>\
  <description>\
]] .. txt2xml(table.description) .. "\\\n" .. [[
  </description>\
  <updatecontact>]] .. rpm.expand("%{fontcontact}") .. [[</updatecontact>\
  <url type=\"homepage\">]] .. rpm.expand("%{url}") .. [[</url>\
  <releases>\
    <release version=\"]] .. rpm.expand("%{version}") .. [[\" date=\"$(date -d @$SOURCE_DATE_EPOCH -u --rfc-3339=d)\"/>\
  </releases>]] .. "\\\n" .. xmlfontname .. "\\\n" .. xmlfontlang .. "\\\n" .. [[
</component>\]]
    _metainfobuild = (_metainfobuild ~= '' and _metainfobuild .. "\n" or '') .. "cat<<_EOL_>" .. table.metainfo .. "\\\n" .. xml .. "\n_EOL_\\\nif ! grep provides " .. table.metainfo .. " > /dev/null 2>&1; then echo \"" .. table.pkgname .. ": No family names provided\"; exit 1; fi\\"
end

local function has_value(table, value)
    for _,v in ipairs(table) do
        if v == value then
            return true
        end
    end
    return false
end

local function genfilelist(table)
    local flist = '$(for f in $(cd %{buildroot}/' .. table.fontdir .. ' && find -regex \'./' .. table.filename .. '\' -print); do echo "' .. table.fontdir .. '$f"; done)' .. '\\\n'
    _filelistbuild = _filelistbuild .. "cat<<_EOL_>" .. table.pkgname .. ".list\\\n" .. flist .. "_EOL_\\\n"
end

local function notopkg(table)
    local _pname = string.lower(table.family):gsub(' ', '-')
    local pname = _pname .. (table.variable and '-vf' or '')
    local pkgname = rpm.expand('%{_fontname}-') .. pname .. '-fonts'
    local prio = (table.priority and table.priority or rpm.expand('%{mprio}'))

    if table.default == true then
        prio = (table.variable and rpm.expand('%{hprio}') or rpm.expand('%{shprio}'))
    end
    if is_nonlatin(table) then
        if prio == rpm.expand('%{hprio}') then
            prio = rpm.expand('%{nlat_hprio}')
        elseif prio == rpm.expand('%{shprio}') then
            prio = rpm.expand('%{nlat_shprio}')
        elseif prio == rpm.expand('%{mprio}') then
            prio = rpm.expand('%{nlat_mprio}')
        elseif prio == rpm.expand('%{lprio}') then
            prio = rpm.expand('%{nlat_lprio}')
        else
            io.stderr:write("Unknown priority")
        end
    end
    prio = tostring(prio)
    local fcconf = prio .. '-' .. rpm.expand('%{fontconf}') .. '-' .. pname .. '.conf'
    local fontdir = rpm.expand('%{_fontbasedir}') .. '/google-noto' .. (table.variable and '-vf/' or '/')
    local fontname = 'Noto' .. (table.fontname and table.fontname or string.gsub(table.family, ' ', '')) .. (table.variable and '\\\\(\\\\(-[A-Za-z]*\\\\)?\\\\[.*\\\\]\\\\|-VF\\\\).*tf' or '-\\\\([^\\\\[\\\\]]\\\\|[^-VF]\\\\)*.*tf')
    local metaname = rpm.expand('%{fontorg}.') .. pkgname .. '.metainfo.xml'

    table.fcconf = fcconf
    table.pkgname = pkgname
    table.fontdir = fontdir
    table.filename = fontname
    table.summary = 'Noto ' .. table.family .. (table.variable and ' variable' or '') .. ' font'
    table.description = rpm.expand('%{common_desc}') .. [[
Noto ]] .. table.family .. (table.variable and ' variable' or '') .. " font."
    table.metainfo = metaname
    _fcconflist = (_fcconflist ~= '' and _fcconflist .. ':' or '') .. fcconf
    _metafilelist = (_metafilelist ~= '' and _metafilelist .. ':' or '') .. metaname

    local obsoletes = ''

    if table.obsoletes then
        for i = 1, #table.obsoletes do
            obsoletes = obsoletes .. "Obsoletes: %{_fontname}-" .. table.obsoletes[i] .. "-fonts < %{version}-%{release}\n" .. "Provides: %{_fontname}-" .. table.obsoletes[i] .. "-fonts = %{version}-%{release}\n"
	end
    end
    print(rpm.expand([[

%package -n ]] .. table.pkgname .. "\n" .. [[
Summary:    ]] .. table.summary .. "\n" .. [[
Requires:   fontpackages-filesystem
Requires:   %{name}-common = %{version}-%{release}
]] .. obsoletes .. [[

%description -n ]] .. table.pkgname .. "\n" .. table.description .. "\n" .. [[

%files -n ]] .. pkgname .. " -f " .. pkgname .. ".list\n" .. [[
%dir ]] .. fontdir .. "\n" .. [[
%config(noreplace) %{_fontconfig_confdir}/]] .. fcconf .. "\n" .. [[
%{_fontconfig_templatedir}/]] .. fcconf .. "\n" .. [[
%{_metainfodir}/]] .. metaname .. "\n"))
end

local all_deps = ''
local all_vf_deps = ''
local all_static_deps = ''

for i = 1, #subpackages do
    notopkg(subpackages[i])
    all_deps = all_deps .. "Requires: " .. subpackages[i].pkgname .. " = %{version}-%{release}\n"
    if subpackages[i].variable then
      all_vf_deps = all_vf_deps .. "Requires: " .. subpackages[i].pkgname .. " = %{version}-%{release}\n"
    else
      all_static_deps = all_static_deps .. "Requires: " .. subpackages[i].pkgname .. " = %{version}-%{release}\n"
    end
    if rpm.expand("%{cionly}") ~= 0 then
        genfcconf(subpackages[i])
        genmetainfo(subpackages[i])
        genfilelist(subpackages[i])
    else
        _fcconfbuild = "false"
        _metainfobuild = "false"
        _filelistbuild = "false"
    end
end

print(rpm.expand([[

%package -n google-noto-fonts-all
Summary:    All the Noto font families
]] .. all_deps .. [[

%description -n google-noto-fonts-all
A meta package for all Noto font families

%files -n google-noto-fonts-all

%package -n google-noto-fonts-all-vf
Summary:    All the Noto variable font families
]] .. all_vf_deps .. [[

%description -n google-noto-fonts-all-vf
A meta package for all Noto variable font families

%files -n google-noto-fonts-all-vf

%package -n google-noto-fonts-all-static
Summary:    All the Noto static font families
]] .. all_static_deps .. [[

%description -n google-noto-fonts-all-static
A meta package for all Noto static font families

%files -n google-noto-fonts-all-static
]]))

rpm.define("noto_fcconflist " .. _fcconflist)
rpm.define("noto_metafilelist " .. _metafilelist)
local f = io.open("debug-noto-fcconf-build.sh", "w")
if f then
    f:write(_fcconfbuild)
    f:close()
end
local f = io.open("debug-noto-metainfo-build.sh", "w")
if f then
    f:write(_metainfobuild)
    f:close()
end

rpm.define("notobuild_fcconf " .. _fcconfbuild .. "\n")
rpm.define("notobuild_metainfo " .. _metainfobuild .. "\n")
rpm.define("notobuild_filelist " .. _filelistbuild .. "\n")
} ## end of lua

%prep
%setup -q -c -n noto-fonts-%{srcver}


%build
%if %{cionly}
exit 1
%endif
%{notobuild_fcconf}


%install
install -m 0755 -d %{buildroot}%{_fontbasedir}/google-noto
for f in */fonts/*/unhinted/ttf/Noto*.ttf */fonts/*/hinted/ttf/Noto*.ttf; do
  install -m 0644 -p $f %{buildroot}%{_fontbasedir}/google-noto/
done
install -m 0755 -d %{buildroot}%{_fontbasedir}/google-noto-vf
install -m 0644 -p */fonts/*/unhinted/slim-variable-ttf/Noto*.ttf %{buildroot}%{_fontbasedir}/google-noto-vf/

# remove display fonts. this isn't shipped in upstream anymore.
rm %{buildroot}%{_fontbasedir}/google-noto/NotoSansDisplay*.ttf \
   %{buildroot}%{_fontbasedir}/google-noto/NotoSans-Display*.ttf \
   %{buildroot}%{_fontbasedir}/google-noto/NotoSerifDisplay*.ttf \
   %{buildroot}%{_fontbasedir}/google-noto-vf/NotoSansDisplay*.ttf \
   %{buildroot}%{_fontbasedir}/google-noto-vf/NotoSerifDisplay*.ttf || :
rm %{buildroot}%{_fontbasedir}/google-noto/Noto*Test-*.ttf \
   %{buildroot}%{_fontbasedir}/google-noto-vf/Noto*Test*.ttf || :
# Noto Sans Phags Pa has been renamed to Noto Sans PhagsPa but shipped in the archive somehow
#   https://github.com/notofonts/phags-pa/commit/b85e2b0a38ad21d0196104e791e0b15bafedaf66
rm %{buildroot}%{_fontbasedir}/google-noto/NotoSansPhags-Pa*.ttf || :

# fc-scan in script expects fonts are already installed
%{notobuild_metainfo}
%{notobuild_filelist}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir} \
                   %{buildroot}%{_metainfodir}

IFS=":"
for f in $(echo %{noto_fcconflist}); do
    install -m 0644 -p $f %{buildroot}%{_fontconfig_templatedir}/$f
    ln -s $(realpath --relative-to=%{_fontconfig_confdir}/ %{_fontconfig_templatedir}/$f) \
	  %{buildroot}%{_fontconfig_confdir}/$f
done
for f in $(echo %{noto_metafilelist}); do
    install -m 0644 -p $f %{buildroot}%{_metainfodir}/$f
done


%check
IFS=":"
for f in $(echo %{noto_fcconflist}); do
    xmllint --loaddtd --valid --nonet %{buildroot}%{_fontconfig_templatedir}/$f
done
for f in $(echo %{noto_metafilelist}); do
    appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/$f || (cat $f; exit 1)
done

%files common
%license */LICENSE
%doc */README.md


%changelog
* Wed Nov 12 2025 Akira TAGOH <tagoh@redhat.com> - 20251101-2
- Change the config priority for Georgian to avoid unexpected overwritten with
  dejavu-sans-mono-fonts for example.
  Resolves: rhbz#2402647

* Thu Nov  6 2025 Akira TAGOH <tagoh@redhat.com> - 20251101-1
- Updates to monthly release of 2025.11.01.
- New sub packages added: google-noto-serif-hentaigana-fonts,
  google-noto-serif-hentaigana-vf-fonts, google-noto-serif-todhri-fonts

* Mon Oct  6 2025 Akira TAGOH <tagoh@redhat.com> - 20251001-1
- Updates to monthly release of 2025.10.01.

* Wed Sep  3 2025 Akira TAGOH <tagoh@redhat.com> - 20250901-1
- Updates to monthly release of 2025.09.01.

* Mon Aug  4 2025 Akira TAGOH <tagoh@redhat.com> - 20250801-1
- Updates to monthly release of 2025.08.01.

* Mon Jul 28 2025 Akira TAGOH <tagoh@redhat.com> - 20250701-4
- Fix a typo in Obsolete.
  Resolves: rhbz#2382600

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Akira TAGOH <tagoh@redhat.com> - 20250701-2
- Add fallback config of monospace for following languages. See
  https://fedoraproject.org/wiki/Changes/SetDefaultMonospaceFallbackFont
  - Arabic
  - Bengali
  - Devanagari
  - Ethiopic
  - Georgian
  - Gujarati
  - Hebrew
  - Kannada
  - Khmer
  - Oriya
  - Sinhala
  - Tamil
  - Telugu
  - Thai

* Fri Jul  4 2025 Akira TAGOH <tagoh@redhat.com> - 20250701-1
- Updates to monthly release of 2025.07.01.
- Add new subpackage google-noto-sans-sunuwar-fonts

* Tue May 13 2025 Akira TAGOH <tagoh@redhat.com> - 20250501-1
- Updates to monthly release of 2025.05.01.

* Wed Apr 16 2025 Akira TAGOH <tagoh@redhat.com> - 20250401-1
- Updates to monthly release of 2025.04.01.

* Tue Mar  4 2025 Akira TAGOH <tagoh@redhat.com> - 20250301-1
- Updates to monthly release of 2025.03.01.
- Add back google-noto-sans-thai-looped-vf-fonts.

* Wed Feb 12 2025 Akira TAGOH <tagoh@redhat.com> - 20250201-1
- Updates to monthly release of 2025.02.01.

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan  7 2025 Akira TAGOH <tagoh@redhat.com> - 20250101-1
- Updates to monthly release of 2025.01.01.

* Tue Sep  3 2024 Akira TAGOH <tagoh@redhat.com> - 20240901-1
- Updates to monthly release of 24.9.1.

* Tue Aug  6 2024 Akira TAGOH <tagoh@redhat.com> - 20240801-1
- Updates to monthly release of 24.8.1.

* Fri Jul 26 2024 Akira TAGOH <tagoh@redhat.com> - 20240701-3
- Use Noto * Hebrew for Yiddish.
  References: rhbz#2284093

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul  8 2024 Akira TAGOH <tagoh@redhat.com> - 20240701-1
- Updates to monthly release of 24.7.1
- Fix a typo in config.
- Rename google-noto-sans-symbols2-fonts to google-noto-sans-symbols-2-fonts
- Rename google-noto-sans-meeteimayek-vf-fonts to google-noto-sans-meetei-mayek-vf-fonts

* Thu Jun 13 2024 Akira TAGOH <tagoh@redhat.com> - 20240601-1
- Updates to monthly release of 24.6.1
- Add google-noto-znamenny-musical-notation-fonts

* Thu Apr  4 2024 Akira TAGOH <tagoh@redhat.com> - 20240401-1
- Updates to monthly release of 24.4.1

* Thu Mar 21 2024 Akira TAGOH <tagoh@redhat.com> - 20240301-3
- Add google-noto-fonts-all, google-noto-fonts-all-vf, and
  google-noto-fonts-all-static meta packages.

* Mon Mar 11 2024 Akira TAGOH <tagoh@redhat.com> - 20240301-2
- Add Obsoletes: google-noto-looped-thai-fonts in google-noto-sans-thai-looped-fonts.

* Fri Mar  8 2024 Akira TAGOH <tagoh@redhat.com> - 20240301-1
- Updates to monthly release of 24.3.1

* Wed Feb 21 2024 Akira TAGOH <tagoh@redhat.com> - 20240201-2
- Add Obsolsetes: google-noto-sans-phags-pa-fonts in google-noto-sans-phagspa-fonts
  Resolves: rhbz#2265259

* Fri Feb  9 2024 Akira TAGOH <tagoh@redhat.com> - 20240201-1
- Updates to monthly release of 24.2.1

* Wed Jan 31 2024 Akira TAGOH <tagoh@redhat.com> - 20240101-4
- Updates to monthly release of 24.1.1
- Remove substitute config for Symbol.
  Resolves: rhbz#2259962

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov  2 2023 Akira TAGOH <tagoh@redhat.com> - 20230801-4
- Add binding="same" for Noto Sans Symbols to prevent lower priority than
  urw-base35-standard-symbols-ps-fonts even though priority number in fontconfig is higher than it.
  Resolves: rhbz#2088665

* Thu Aug 31 2023 Akira TAGOH <tagoh@redhat.com> - 20230801-3
- Add Noto Sans Sinhala as monospace for a workaround that
  Noto Serif Sinhala is picked up for monospace.
  Resolves: rhbz#2236485

* Thu Aug  3 2023 Akira TAGOH <tagoh@redhat.com> - 20230801-2
- Make some Indic families default
  https://fedoraproject.org/wiki/Changes/Indic_Noto_fonts

* Wed Aug  2 2023 Akira TAGOH <tagoh@redhat.com> - 20230801-1
- Updates to monthly release of 23.8.1
- Add google-noto-sans-kawi{,-vf}-fonts and google-noto-sans-nko-unjoined{,-vf}-fonts packages.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Akira TAGOH <tagoh@redhat.com> - 20230601-3
- Use Noto Bengali for mni
  Resolves: rhbz#2214982

* Thu Jun  8 2023 Akira TAGOH <tagoh@redhat.com> - 20230601-2
- Increase a priority a bit for static fonts but still lower than variable fonts.
- Fix priority for some languages.

* Thu Jun  1 2023 Akira TAGOH <tagoh@redhat.com> - 20230601-1
- Updates to monthly release of 23.6.1
- Allow Assamese in Noto * Bengali.

* Thu May 18 2023 Akira TAGOH <tagoh@redhat.com> - 20230501-1
- Updates to monthly release of 23.5.1

* Thu Feb  2 2023 Akira TAGOH <tagoh@redhat.com> - 20230201-1
- Updates to monthly release of 23.2.1
- Update priority for google-noto-{sans,serif}-{khmer,thai}-vf-fonts for
  https://fedoraproject.org/wiki/Changes/NotoFontsForMoreLang

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Akira TAGOH <tagoh@redhat.com> - 20201206^1.git0c78c8329-9
- Drop unnecessary config.

* Thu Dec  1 2022 Akira TAGOH <tagoh@redhat.com> - 20201206-1.git0c78c8329-8
- Convert License tag to SPDX.

* Fri Nov 25 2022 Akira TAGOH <tagoh@redhat.com> - 20201206-1.git0c78c8329-7
- Add an alias for Symbol font to Noto Sans Symbols/Symbols2.
  Resolves: rhbz#2088665

* Thu Nov 24 2022 Akira TAGOH <tagoh@redhat.com> - 20201206-1.git0c78c8329-6
- Drop Noto Sans Display and Noto Serif Display fonts.
  These fonts isn't shipped from upstream anymore.
  Resolves: rhbz#2143521

* Fri Sep 30 2022 Akira TAGOH <tagoh@redhat.com> - 20201206-1.git0c78c8329-5
- Update Noto Sinhala fonts to the latest to fix some rendering issue in Sinhala scripts.
  Resolves: rhbz#2129619

* Thu Sep 15 2022 Akira TAGOH <tagoh@redhat.com> - 20201206-1.git0c78c8329-4
- Add Provides lines for Obsoletes packages.
  Resolves: rhbz#2126575

* Wed Aug 31 2022 Akira TAGOH <tagoh@redhat.com> - 20201206-1.git0c78c8329-3
- Drop lang="ar" for Kufi/Naskh Arabic fonts.
- Adjust priority for Noto Thai fonts.

* Tue Aug  2 2022 Akira TAGOH <tagoh@redhat.com> - 20201206-1.git0c78c8329-2
- Fix wrong alias for Noto Rashi Hebrew.
  Resolves: rhbz#2113077

* Wed Jul 27 2022 Akira TAGOH <tagoh@redhat.com> - 20201206^1.git0c78c8329-1
- Update to snapshot from git 0c78c8329.
  Resolves: rhbz#2098555

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar  7 2022 Akira TAGOH <tagoh@redhat.com> - 20201206-9
- Fix config to set Naskh Arabic as serif for fallback.

* Fri Feb  4 2022 Akira TAGOH <tagoh@redhat.com> - 20201206-8
- Fix the priority for Indic fonts.
  We postponed to replace Lohit with Noto this time.
  Resolves: rhbz#2050477

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20201206-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Akira TAGOH <tagoh@redhat.com> - 20201206-6
- Update the priority of fontconfig config for Noto Sans, Noto Serif and Noto Sans Mono to make them default.

* Tue Dec 14 2021 Akira TAGOH <tagoh@redhat.com> - 20201206-5
- Fix a typo in the package name.
  google-noto-sansthai-looped-vf-fonts should be google-noto-sans-thai-looped-vf-fonts.

* Tue Nov 16 2021 Akira TAGOH <tagoh@redhat.com> - 20201206-4
- Have higher priority google-noto-sans-gurmukhi-vf-fonts than google-noto-sans-gurmukhi-fonts.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20201206-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 12 2021 Akira TAGOH <tagoh@redhat.com> - 20201206-2
- Add some Obsoletes lines for dropped sub packages.

* Fri Apr  9 2021 Akira TAGOH <tagoh@redhat.com> - 20201206-1
- Updates to 20201206.
  Resolves: rhbz#1899847
- Refactoring spec file.
- Fix invalid metainfo files.
  Resolves: rhbz#1830709

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20181223-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20181223-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20181223-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 12 2019 Akira TAGOH <tagoh@redhat.com> - 20181223-6
- Make variable fonts priority more than non variable fonts. (#1739976)

* Fri Jul 26 2019 Parag Nemade <pnemade AT redhat DOT com> - 20181223-5
- Resolves:rh#1554988 - google-noto-sans-gurmkukhi-fonts default for pa_IN locale

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181223-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun  4 2019 Akira TAGOH <tagoh@redhat.com> - 20181223-3
- Install metainfo files under %%{_metainfodir}.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181223-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 27 2018 Akira TAGOH <tagoh@redhat.com> - 20181223-1
- Updates to 20181223.
- Add new sub-packages for variable fonts.

* Mon Dec 17 2018 Akira TAGOH <tagoh@redhat.com> - 20181130-2
- Make Display and UI fonts lower priority.
- Add more languages to google-noto-*-devanagari.conf, google-noto-sans-ethiopic.conf,
  and google-noto-sans-hebrew.conf

* Fri Dec  7 2018 Akira TAGOH <tagoh@redhat.com> - 20181130-1
- Updates to 20181130.
- Noto Sans Balinese is now Noto Serif Balinese.
- Add new sub-packages: google-noto-music-fonts,
  google-noto-sans-bassa-vah-fonts, google-noto-sans-bhaiksuki-fonts,
  google-noto-sans-caucasian-albanian-fonts, google-noto-sans-duployan-fonts,
  google-noto-sans-elbasan-fonts, google-noto-sans-grantha-fonts,
  google-noto-sans-hatran-fonts, google-noto-sans-khojki-fonts,
  google-noto-sans-khudawadi-fonts, google-noto-sans-linear-a-fonts,
  google-noto-sans-mahajani-fonts, google-noto-sans-manichaean-fonts,
  google-noto-sans-marchen-fonts, google-noto-sans-mende-kikakui-fonts,
  google-noto-sans-meroitic-fonts, google-noto-sans-miao-fonts,
  google-noto-sans-modi-fonts, google-noto-sans-mro-fonts,
  google-noto-sans-multani-fonts, google-noto-sans-nabataean-fonts,
  google-noto-sans-newa-fonts, google-noto-sans-old-hungarian-fonts,
  google-noto-sans-old-north-arabian-fonts, google-noto-sans-old-permic-fonts,
  google-noto-sans-pahawh-hmong-fonts, google-noto-sans-palmyrene-fonts,
  google-noto-sans-pau-cin-hau-fonts, google-noto-sans-psalter-pahlavi-fonts,
  google-noto-sans-sharada-fonts, google-noto-sans-sora-sompeng-fonts,
  google-noto-sans-syriac-fonts, google-noto-sans-takri-fonts,
  google-noto-sans-tirhuta-fonts, google-noto-sans-warang-citi-fonts,
  google-noto-serif-ahom-fonts, google-noto-serif-gurmukhi-fonts,
  google-noto-serif-tamil-slanted-fonts, google-noto-serif-tibetan-fonts

* Fri Sep 21 2018 Akira TAGOH <tagoh@redhat.com> - 20180905-1
- Updates to 20180905.
- Remove Group tag.
- Don't call fc-cache in scriptlets. this isn't needed anymore.
- Drop BR: fontforge.
- Generate fontconfig config files in macro for simple one.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20161022-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr  5 2018 Jens Petersen <petersen@redhat.com> - 20161022-7
- change the Sinhala fontconfig priority to 65 (#1450802)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20161022-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Jens Petersen <petersen@redhat.com> - 20161022-5
- use _font_pkg

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161022-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul  5 2017 Jens Petersen <petersen@redhat.com> - 20161022-3
- add a fontconfig priority option to the notopkg macro,
  which allows overriding the default 66 priority

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 07 2016 Pravin Satpute <psatpute@redhat.com> - 20161022-1
- Resolves #1321685 - Added Noto Mono font.
- License changed from ASL 2.0 to OFL.
- New package addition: Mono, Serif Bengali, Serif Devanagari
- Serif Gujarari, Serif Malayalam, Serif Tamil and Serif Telugu.

* Wed Aug 24 2016 Pravin Satpute <psatpute@redhat.com> - 20150929-2
- Resolves #1368772 - Fixes issue with LICENSE file.

* Thu Apr 28 2016 Pravin Satpute <psatpute@redhat.com> - 20150929-1
- Resolves #1269404 - Update to new git release 20150929
- Upstream divided google-noto-fonts package into noto-cjk-font and noto-emoji
- Removed packages: google-noto-color-emoji-fonts, google-noto-sans (cjk-fonts,
- japanese-fonts, simplified-chinese-fonts and traditional-chinese-fonts)
- Replaced by google-noto-cjk-fonts and google-noto-emoji-fonts
- New subpackages - google-noto-nastaliq-urdu-fonts and google-noto-sans-tibetan-fonts

* Thu Feb 04 2016 Parag Nemade <pnemade AT redhat DOT com> - 20150417-4
- Fix for python2 fonttools

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20150417-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150417-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 17 2015 Pravin Satpute <psatpute@redhat.com> - 20150417-1
- Updating to git snapshot d47480343178.
- Remove Thaana and Oriya from under-development list.
- Add Syriac requirements from Unicode Core Specification.

* Fri Mar 27 2015 Pravin Satpute <psatpute@redhat.com> - 20150325-1
- Updating to git snapshot 762640379a51.
- Added 2 new packages Oriya and Oriya-UI.
- Update Hebrew, Georgian, and Ethiopic fonts.
- Fix cmap of U+06F7 to Urdu form of digit 7.

* Tue Jan 13 2015 Pravin Satpute <psatpute@redhat.com> - 20141117-6
- Resolves #1162341: Packaged Noto Color Emoji

* Mon Dec 15 2014 Jens Petersen <petersen@redhat.com> - 20141117-5
- improve generated font subpackage descriptions
- it is Hanunoo not Hanuno!
- specify font filenames more precisely

* Mon Dec 15 2014 Jens Petersen <petersen@redhat.com> - 20141117-4
- add obsoletes to cover the change of package names for Hanuno, Linear B,
  and Meetei Mayek

* Tue Dec  2 2014 Jens Petersen <petersen@redhat.com> - 20141117-3
- create the fonts subpackages with a macro

* Fri Nov 21 2014 Jens Petersen <petersen@redhat.com> - 20141117-2
- move cjk fonts fontconfig priority from 65-0 to 66
- generate the appinfo metainfo for the subpackages
- use a single for-loop to install the font config and appdata files
- move parent appinfo metainfo to common (Parag Nemade)

* Thu Nov 20 2014 Jens Petersen <petersen@redhat.com> - 20141117-1
- update to latest git (aae16d0cd626)
- package Japanese, Korean, and CJK fonts
- add Thaana font
- add common subpackage for license and doc files
- order spec subpackages lexically

* Wed Nov 19 2014 Peng Wu <pwu@redhat.com> - 20141001-5
- Rename Chinese sub-packages

* Wed Nov 12 2014 Peng Wu <pwu@redhat.com> - 20141001-4
- Add Chinese fonts

* Tue Nov 11 2014 Parag Nemade <pnemade AT redhat DOT com> - 20141001-3
- Add metainfo file to show this font in gnome-software

* Mon Nov 03 2014 Pravin Satpute <psatpute@redhat.com> - 20141001-2
- Resolves #1159562: Typo in fontconfig file

* Wed Oct 01 2014 Pravin Satpute <psatpute@redhat.com> - 20141001-1
- Google stops release tarball. Zip file derived from git Download zip.
- 45 new packages added as follows.
- kufi-arabic-fonts, naskh-arabic-fonts, naskh-arabic-ui-fonts, sans-balinese-fonts,
- sans-bamum-fonts, sans-batak-fonts, sans-buginese-fonts, sans-buhid-fonts,
- sans-canadian-aboriginal-fonts, sans-cham-fonts, sans-cuneiform-fonts, sans-cypriot-fonts,
- sans-gothic-fonts, sans-gurmukhi-fonts, sans-gurmukhi-ui-fonts,
- sans-inscriptional-pahlavi-fonts, sans-inscriptional-parthian-fonts, sans-javanese-fonts,
- sans-lepcha-fonts, sans-limbu-fonts, sans-linearb-fonts, sans-mongolian-fonts,
- sans-myanmar-fonts, sans-myanmar-ui-fonts, sans-new-tai-lue-fonts, sans-ogham-fonts,
- sans-ol-chiki-fonts, sans-old-italic-fonts, sans-old-persian-fonts, sans-phags-pa-fonts,
- sans-rejang-fonts, sans-runic-fonts, sans-samaritan-fonts, sans-saurashtra-fonts,
- sans-sinhala-fonts, sans-sundanese-fonts, sans-syloti-nagri-fonts, sans-syriac-eastern-fonts,
- sans-syriac-estrangela-fonts, sans-syriac-western-fonts, sans-tagbanwa-fonts,
- sans-tai-le-fonts, sans-tifinagh-fonts, sans-yi-fonts
- Resolves #1148413

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130807-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Pravin Satpute <psatpute@redhat.com> - 20130807-1
- Upstream new release of 20130807 tarball.
- Packages Non Hinted upstream tarball.
- This pulled fonts for number of missing Unicode scripts in Fedora

* Tue Jul 16 2013 Pravin Satpute <psatpute@redhat.com> - 20130624-1
- Resolved #984459 :- Upstream new release.
- Added new package google-noto-serif-khmer-fonts

* Mon Jun 24 2013 Pravin Satpute <psatpute@redhat.com> - 20130411-5
- Resolved #971886 :- Georgian Serif fontconfig file error

* Mon Jun 10 2013 Pravin Satpute <psatpute@redhat.com> - 20130411-4
- Resolved #971886 :- Georgian fontconfig file error

* Mon May 06 2013 Pravin Satpute <psatpute@redhat.com> - 20130411-3
- Initial import
- Updated spec file

* Fri Apr 19 2013 Pravin Satpute <psatpute@redhat.com> - 20130411-2
- Updated package as per 3rd comment on review request #953859

* Fri Apr 19 2013 Pravin Satpute <psatpute@redhat.com> - 20130411-1
- Initial packaging
