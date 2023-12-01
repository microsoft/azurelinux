Vendor:         Microsoft Corporation
Distribution:   Mariner
%global priority    68
%global fontname    baekmuk-ttf
%global archivename %{fontname}-%{version}
%global common_desc \
This package provides the free Korean TrueType fonts.

%global catalogue      %{_sysconfdir}/X11/fontpath.d
%{!?_metainfodir: %global _metainfodir %{_datadir}/metainfo}

Name:           %{fontname}-fonts
Version:        2.2
Release:        52%{?dist}
Summary:        Free Korean TrueType fonts

License:        Baekmuk
URL:            http://kldp.net/projects/baekmuk/
Source0:        http://kldp.net/baekmuk/release/865-%{archivename}.tar.gz#/%{archivename}.tar.gz
Source3:        baekmuk-ttf-batang.conf
Source4:        baekmuk-ttf-dotum.conf
Source5:        baekmuk-ttf-gulim.conf
Source6:        baekmuk-ttf-hline.conf
Source7:        %{fontname}-batang.metainfo.xml
Source8:        %{fontname}-dotum.metainfo.xml
Source9:        %{fontname}-gulim.metainfo.xml
Source10:       %{fontname}-hline.metainfo.xml
Source11:       %{fontname}.metainfo.xml

Obsoletes:      fonts-korean <= 2.2-23
Provides:       fonts-korean = %{version}-%{release}

BuildArch:      noarch
BuildRequires:  fontpackages-devel >= 1.13 , xorg-x11-font-utils
BuildRequires:  ttmkfdir >= 3.0.6

%description
%common_desc

%package -n %{fontname}-batang-fonts
Summary:        Korean Baekmuk TrueType Batang typeface
Obsoletes:      %{name}-batang < 2.2-13
Provides:       %{name}-batang = %{version}-%{release}
Requires:       %{fontname}-fonts-common = %{version}-%{release}

%description -n %{fontname}-batang-fonts
%common_desc

Batang is Korean TrueType font in Serif typeface.

%_font_pkg -n batang -f *-%{fontname}-batang*.conf batang.ttf
%{_metainfodir}/%{fontname}-batang.metainfo.xml

%package -n %{fontname}-dotum-fonts
Summary:        Korean Baekmuk TrueType Dotum typeface
Obsoletes:      %{name}-dotum < 2.2-13 
Provides:       %{name}-dotum = %{version}-%{release}
Requires:       %{fontname}-fonts-common = %{version}-%{release}

%description -n %{fontname}-dotum-fonts
%common_desc

Dotum is Korean TrueType font in San-serif typeface.

%_font_pkg -n dotum -f *-%{fontname}-dotum*.conf dotum.ttf
%{_metainfodir}/%{fontname}-dotum.metainfo.xml

%package -n %{fontname}-gulim-fonts
Summary:        Korean Baekmuk TrueType Gulim typeface
Obsoletes:      %{name}-gulim < 2.2-13
Provides:       %{name}-gulim = %{version}-%{release}
Requires:       %{fontname}-fonts-common = %{version}-%{release}

%description -n %{fontname}-gulim-fonts
%common_desc

Gulim is Korean TrueType font in Monospace typeface.

%_font_pkg -n gulim -f *-%{fontname}-gulim*.conf gulim.ttf
%{_metainfodir}/%{fontname}-gulim.metainfo.xml

%package -n %{fontname}-hline-fonts
Summary:        Korean Baekmuk TrueType Headline typeface
Obsoletes:      %{name}-hline < 2.2-13
Provides:       %{name}-hline = %{version}-%{release}
Requires:       %{fontname}-fonts-common = %{version}-%{release}

%description -n %{fontname}-hline-fonts
%common_desc

Headline is Korean TrueType font in Black face.

%_font_pkg -n hline -f *-%{fontname}-hline*.conf hline.ttf
%{_metainfodir}/%{fontname}-hline.metainfo.xml

%package -n %{fontname}-fonts-common
Summary:        Common files for Korean Baekmuk TrueType fonts
Obsoletes:      ttfonts-ko < 1.0.11-33, fonts-korean < 2.2-5
Obsoletes:      baekmuk-ttf-common-fonts < 2.2-17
Obsoletes:      %{fontname}-fonts-ghostscript < 2.2-44
Provides:       baekmuk-ttf-common-fonts = %{version}-%{release}
Provides:       fonts-korean = %{version}-%{release}
Provides:       ttfonts-ko = %{version}-%{release}
Provides:       %{fontname}-fonts-ghostscript = %{version}-%{release}
Requires:       fontpackages-filesystem >= 1.13
BuildRequires:  fontpackages-filesystem >= 1.13

%description -n %{fontname}-fonts-common
%common_desc

This is common files for Baekmuk Korean TrueType fonts.

%files -n %{fontname}-fonts-common
%doc README
%license COPYRIGHT COPYRIGHT.ko
%dir %{_fontdir}
%verify(not md5 size mtime) %{_fontdir}/fonts.dir
%verify(not md5 size mtime) %{_fontdir}/fonts.scale
%verify(not md5 size mtime) %{catalogue}/%{fontname}
%{_metainfodir}/%{fontname}.metainfo.xml

%prep
%setup -q -n %{archivename}

%build
%{nil}

%install
# font
%__install -d -m 0755 %{buildroot}%{_fontdir}
for i in batang dotum gulim hline; do
  %__install -p -m 0644 ttf/$i.ttf %{buildroot}%{_fontdir}
done

# fontconfig conf
%__install -m 0755 -d %{buildroot}%{_fontconfig_templatedir}
%__install -m 0755 -d %{buildroot}%{_fontconfig_confdir}
cd ../
for fconf in %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6}
do
    %__install -m 0644 $fconf %{buildroot}%{_fontconfig_templatedir}/%{priority}-$(basename $fconf)
    %__ln_s %{_fontconfig_templatedir}/%{priority}-$(basename $fconf) \
        %{buildroot}%{_fontconfig_confdir}/%{priority}-$(basename $fconf)
done
cd -

# fonts.{scale,dir}
%{_bindir}/ttmkfdir -d %{buildroot}%{_fontdir} \
  -o %{buildroot}%{_fontdir}/fonts.scale
%{_bindir}/mkfontdir %{buildroot}%{_fontdir}

# catalogue
%__install -d -m 0755 %{buildroot}%{catalogue}
%__ln_s %{_fontdir} %{buildroot}%{catalogue}/%{fontname}

# convert Korean copyright file to utf8
%{_bindir}/iconv -f EUC-KR -t UTF-8 COPYRIGHT.ks > COPYRIGHT.ko

# Add AppStream metadata
install -Dm 0644 -p %{SOURCE7} \
        %{buildroot}%{_metainfodir}/%{fontname}-batang.metainfo.xml
install -Dm 0644 -p %{SOURCE8} \
        %{buildroot}%{_metainfodir}/%{fontname}-dotum.metainfo.xml
install -Dm 0644 -p %{SOURCE9} \
        %{buildroot}%{_metainfodir}/%{fontname}-gulim.metainfo.xml
install -Dm 0644 -p %{SOURCE10} \
        %{buildroot}%{_metainfodir}/%{fontname}-hline.metainfo.xml
install -Dm 0644 -p %{SOURCE11} \
        %{buildroot}%{_metainfodir}/%{fontname}.metainfo.xml

%changelog
* Fri Jul 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.2-52
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add %%_metainfodir definition at top of spec, if not already defined

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun  3 2019 Akira TAGOH <tagoh@redhat.com> - 2.2-49
- Install metainfo files into %%{_metainfodir}.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 24 2018 Peng Wu <pwu@redhat.com> - 2.2-47
- Update Source URL

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jan 30 2018 Akira TAGOH <tagoh@redhat.com> - 2.2-45
- Update the priority to change the default font to Noto.

* Mon Jan 22 2018 Peng Wu <pwu@redhat.com> - 2.2-44
- Drop baekmuk-ttf-fonts-ghostscript subpackage

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan  7 2016 Daiki Ueno <dueno@redhat.com> - 2.2-40
- replace %%define uses with %%global

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 07 2014 Parag Nemade <pnemade AT redhat DOT com> - 2.2-38
- Add metainfo file to show this font in gnome-software
- Remove buildroot which is optional now
- Remove group tag

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul  4 2012 Daiki Ueno <dueno@redhat.com> - 2.2-33
- fix <test> usage in fontconfig files (Closes: #837526)

* Mon Feb  6 2012 Daiki Ueno <dueno@redhat.com> - 2.2-32
- Update the priority.
  nhn-nanum-fonts -> 65-0, un-core-fonts -> 65-1, baekmuk-ttf-fonts -> 65-2
- Drop buildroot cleanup.
- Drop %%defattr(0644,root,root,0755) from %%files.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May 26 2010 Akira TAGOH <tagoh@redhat.com> - 2.2-29
- Improve the fontconfig config file to match ko-kr as well. (#586306)
- sync NVR and fixes from RHEL-6.
- Update the priority.

* Wed Apr 21 2010 Caius 'kaio' Chance <k at kaio.me> - 2.2-25
- Resolves: rhbz#578017 (Remove binding="same" from conf files.)

* Wed Jan 13 2010 Caius 'kaio' Chance <k at kaio.me> - 2.2-24.el6
- Fixed rpmlint errors.
- Synchronized version number with another tree.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 08 2009 Caius 'kaio' Chance <cchance@redhat.com> - 2.2-21.fc11
- Resolves: rhbz#483327 (Fixed unowned directories.)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 03 2009 Caius Chance <cchance@redhat.com> - 2.2-19.fc11
- Resolves: rhbz#483327
- Reowned font directory by subpackage -common.
- Splited ghostscript files to subpackage -ghostscript.
- Updated paths in ghostscript files.

* Mon Feb 02 2009 Caius Chance <cchance@redhat.com> - 2.2-18.fc11
- Updated fontconfig .conf files based on fontpackages templates.

* Tue Jan 27 2009 Caius Chance <cchance@redhat.com> - 2.2-17.fc11
- Resolves: rhbz#477332
- Fixed obsoletion of baekmuk-ttf-common-fonts.

* Thu Jan 22 2009 Caius Chance <cchance@redhat.com> - 2.2-16.fc11
- Resolves: rhbz#477332
- Refined dependencies.

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.2-15.fc11
- Fix busted inter-subpackage dependencies

* Tue Jan 20 2009 Caius Chance <cchance@redhat.com> - 2.2-14.fc11
- Resolves: rhbz#477332
- Refined according to Mailhot's comments (477410) on liberaton fonts.

* Mon Jan 19 2009 Caius Chance <cchance@redhat.com> - 2.2-13.fc11
- Resolves: rhbz#477332
- Package renaming for post-1.13 fontpackages.

* Fri Jan 16 2009 Caius Chance <cchance@redhat.com> - 2.2-12.fc11
- Resolves: rhbz#477332 (Repatched buildsys error.)

* Fri Jan 16 2009 Caius Chance <cchance@redhat.com> - 2.2-11.fc11
- Resolves: rhbz#477332 (Included macro _font_pkg and created fontconfig .conf files.)

* Fri Jan 09 2009 Caius Chance <cchance@redhat.com> - 2.2-10.fc11
- Resolves: rhbz#477332 (Converted to new font packaging guidelines.)

* Mon Jun 30 2008 Caius Chance <cchance@redhat.com> - 2.2-9.fc10
- Refine obsoletes tag version-release specific.

* Mon Jun 30 2008 Caius Chance <cchance@redhat.com> - 2.2-8.fc10
- Resolves: rhbz#453080 (fonts-korean is deprecated and should be removed.)

* Wed Nov 14 2007 Jens Petersen <petersen@redhat.com> - 2.2-7
- better url
- use fontname and fontdir macros

* Mon Sep 24 2007 Jens Petersen <petersen@redhat.com> - 2.2-6
- convert Korean copyright file to utf8 (Mamoru Tasaka, #300651)

* Mon Sep 24 2007 Jens Petersen <petersen@redhat.com> - 2.2-5
- more fixes from Mamoru Tasaka, #300651:
- make common subpackage own ghostscript conf.d
- conflict with previous fonts-korean
- update CID font maps

* Mon Sep 24 2007 Jens Petersen <petersen@redhat.com> - 2.2-4
- preserve timestamps of installed files (Mamoru Tasaka, #300651)
- add a common subpackage for shared files (Mamoru Tasaka, #300651)

* Mon Sep 24 2007 Jens Petersen <petersen@redhat.com> - 2.2-3
- do not provide ttfonts-ko in subpackages (Mamoru Tasaka, #300651)

* Sat Sep 22 2007 Jens Petersen <petersen@redhat.com> - 2.2-2
- license is now designated Baekmuk

* Sat Sep 22 2007 Jens Petersen <petersen@redhat.com> - 2.2-1
- new package separated from fonts-korean (#253155)
