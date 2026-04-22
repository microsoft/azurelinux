## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 16;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Version: 33.003
Release: %autorelease
URL:     https://rastikerdar.github.io/vazirmatn

%global fontlicense       OFL-1.1
%global fontlicenses      OFL.txt
%global fontdocs          AUTHORS.txt *.md
%global fontdocsex        %{fontlicenses}

%global common_description %{expand:
Vazirmatn (formerly known as Vazir), is a Persian/Arabic typeface family with
a simple and smooth form usable in most contexts. For Latin glyphs, Vazirmatn
is combined with Roboto font, however there is also a version without Latin
glyphs (Non-Latin).
}

# Declaration for the subpackage containing the main font family. Also used as
# source rpm info.
%global fontfamily0       Vazirmatn
%global fontsummary0      A simple and legible Persian/Arabic typeface
%global fontpkgheader0    %{expand:
}
%global fonts0            fonts/ttf/*.ttf
%global fontconfs0        %{SOURCE10}
%global fontdescription0  %{expand: %{common_description}
}

# Declaration for the subpackage containing the NL font family.
%global fontfamily1       Vazirmatn NL
%global fontsummary1      Non-Latin Vazirmatn font
%global fontpkgheader1    %{expand:
}
%global fonts1            misc/Non-Latin/fonts/ttf/*.ttf
%global fontconfs1        %{SOURCE11}
%global fontdescription1  %{expand: %{common_description}

This is the version of the font without Latin glyphs.
}

# Declaration for the subpackage containing the UI font family.
%global fontfamily2       Vazirmatn UI
%global fontsummary2      Vazirmatn UI font
%global fontpkgheader2    %{expand:
}
%global fonts2            misc/UI/fonts/ttf/*.ttf
%global fontconfs2        %{SOURCE12}
%global fontdescription2  %{expand: %{common_description}

This version of the font provides generally smaller height to be more suitable
for UI.
}

# Declaration for the subpackage containing the UI NL font family.
%global fontfamily3       Vazirmatn UI NL
%global fontsummary3      Non-Latin Vazirmatn UI font
%global fontpkgheader3    %{expand:
}
%global fonts3            misc/UI-Non-Latin/fonts/ttf/*.ttf
%global fontconfs3        %{SOURCE13}
%global fontdescription3  %{expand: %{common_description}

This version of the font provides generally smaller height to be more suitable
for UI and without Latin glyphs.
}

# Declaration for the subpackage containing the RD font family.
%global fontfamily4       Vazirmatn RD
%global fontsummary4      A variant of Vazirmatn using round dots instead of cubic ones
%global fontpkgheader4    %{expand:
}
%global fonts4            Round-Dots/fonts/ttf/*.ttf
%global fontconfs4        %{SOURCE14}
%global fontdescription4  %{expand: %{common_description}

This variant uses round dots including the dots used over or under letters
rather than cubic dots used in original variant.
}

# Declaration for the subpackage containing the RD NL font family.
%global fontfamily5       Vazirmatn RD NL
%global fontsummary5      Non-Latin Vazirmatn RD font
%global fontpkgheader5    %{expand:
}
%global fonts5            Round-Dots/misc/Non-Latin/fonts/*/*.ttf
%global fontconfs5        %{SOURCE15}
%global fontdescription5  %{expand: %{common_description}

This variant uses round dots including the dots used over or under letters
rather than cubic dots used in original variant. It also comes without Latin
glyphs.
}

# Declaration for the subpackage containing the RD UI font family.
%global fontfamily6       Vazirmatn RD UI
%global fontsummary6      Vazirmatn RD UI font
%global fontpkgheader6    %{expand:
}
%global fonts6            Round-Dots/misc/UI/fonts/*/*.ttf
%global fontconfs6        %{SOURCE16}
%global fontdescription6  %{expand: %{common_description}

This version of the font provides generally smaller height to be more suitable
for UI.
}

# Declaration for the subpackage containing the RD UI NL font family.
%global fontfamily7       Vazirmatn RD UI NL
%global fontsummary7      Non-Latin Vazirmatn RD UI font
%global fontpkgheader7    %{expand:
}
%global fonts7            Round-Dots/misc/UI-Non-Latin/fonts/*/*.ttf
%global fontconfs7        %{SOURCE17}
%global fontdescription7  %{expand: %{common_description}

This version of the font provides generally smaller height to be more suitable
for UI and without Latin glyphs.
}

# Declaration for the subpackages of the variable versions
%global fontfamily8       %{fontfamily0} VF
%global fontsummary8      %{fontsummary0} (variable version)
%global fontpkgheader8    %{fontpkgheader0}
%global fonts8            fonts/variable/*.ttf
%{lua:
function conf2vf(conf, n)
  local vfconf = conf:gsub("-fonts.conf", "-vf-fonts.conf")
  rpm.define("fontconfs" .. tostring(n) .. " " .. vfconf)
end
conf2vf(rpm.expand("%{fontconfs0}"), 8)
}
%global fontdescription8  %{expand:
%{fontdescription0}
This is the variable version of this font.
}

%global fontfamily9       %{fontfamily1} VF
%global fontsummary9      %{fontsummary1} (variable version)
%global fontpkgheader9    %{fontpkgheader1}
%global fonts9            misc/Non-Latin/fonts/variable/*.ttf
%{lua:
conf2vf(rpm.expand("%{fontconfs1}"), 9)
}
%global fontdescription9  %{expand:
%{fontdescription1}
This is the variable version of this font.
}

%global fontfamily10       %{fontfamily4} VF
%global fontsummary10      %{fontsummary4} (variable version)
%global fontpkgheader10    %{fontpkgheader4}
%global fonts10            Round-Dots/fonts/variable/*.ttf
%{lua:
conf2vf(rpm.expand("%{fontconfs4}"), 10)
}
%global fontdescription10  %{expand:
%{fontdescription4}
This is the variable version of this font.
}

%global fontfamily11       %{fontfamily5} VF
%global fontsummary11      %{fontsummary5} (variable version)
%global fontpkgheader11    %{fontpkgheader5}
%global fonts11            Round-Dots/misc/Non-Latin/fonts/variable/*.ttf
%{lua:
conf2vf(rpm.expand("%{fontconfs5}"), 11)
}
%global fontdescription11  %{expand:
%{fontdescription5}
This is the variable version of this font.
}

Source0:  https://github.com/rastikerdar/vazirmatn/releases/download/v%{version}/vazirmatn-v%{version}.zip
Source10: 55-%{fontpkgname0}.conf
Source11: 55-%{fontpkgname1}.conf
Source12: 62-%{fontpkgname2}.conf
Source13: 62-%{fontpkgname3}.conf
Source14: 55-%{fontpkgname4}.conf
Source15: 55-%{fontpkgname5}.conf
Source16: 62-%{fontpkgname6}.conf
Source17: 62-%{fontpkgname7}.conf

# Generate the font subpackage headers
%fontpkg -a

# Generate a font meta(sub)package header for all the font subpackages generated in this spec.
%fontmetapkg

%prep
%setup -q -c
cp %{fontconfs0} %{fontconfs8}
cp %{fontconfs1} %{fontconfs9}
cp %{fontconfs4} %{fontconfs10}
cp %{fontconfs5} %{fontconfs11}
%linuxtext *.txt

%build
%fontbuild -a
sed -i 's/VF/(Variable)/' org*.xml

%install
%fontinstall -a

%check
%fontcheck -a

%fontfiles -a

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 33.003-16
- Latest state for vazirmatn-fonts

* Mon Aug 18 2025 Akira TAGOH <akira@tagoh.org> - 33.003-15
- ci: fix a typo

* Tue Aug 12 2025 Akira TAGOH <akira@tagoh.org> - 33.003-14
- ci: Add monospace fallback tmt for vazirmatn-vf-fonts

* Fri Aug 01 2025 Akira TAGOH <akira@tagoh.org> - 33.003-13
- Fix Installability:downgrade CI test

* Thu Jul 31 2025 Akira TAGOH <akira@tagoh.org> - 33.003-12
- Add fallback rule of monospace for ar, pa-pk, ur not to change current
  behavior

* Thu Jul 31 2025 Akira TAGOH <akira@tagoh.org> - 33.003-11
- Add a fallback rule of monospace

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 33.003-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 33.003-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 33.003-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Akira TAGOH <akira@tagoh.org> - 33.003-7
- ci: Use tmt based test cases

* Wed May 22 2024 Akira TAGOH <tagoh@redhat.com> - 33.003-6
- Update License field to SPDX

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 33.003-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 33.003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 33.003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 33.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 25 2022 Hedayat Vatankhah <hedayat.fwd@gmail.com> - 33.003-1
- Update to latest upstream version: 33.003, and increase the priority of
  vazirmatn font so that it'll be used in Qt apps in fa locale too

* Sat Jun 04 2022 Hedayat Vatankhah <hedayat.fwd@gmail.com> - 32.102-1
- Update to latest upstream version 32.102 with some bug fixes and hinting
  enhancements, closing fedora#2093583

* Sat Jun 04 2022 Hedayat Vatankhah <hedayat.fwd@gmail.com> - 32.101-5
- Try to fix the automatic release number!

* Sat Jun 04 2022 Hedayat Vatankhah <hedayat.fwd@gmail.com> - 32.101-3
- Try to fix the automatic release number!

* Thu Jun 02 2022 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 32.101-3
- Enhance package descriptions

* Fri May 20 2022 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 32.101-2
- Create separate package for VF fonts & cleanup most template comments

* Sat Apr 23 2022 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 32.101-1
- Initial version


## END: Generated by rpmautospec
