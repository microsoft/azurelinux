Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hyphen-pt
Summary: Portuguese hyphenation rules
%global upstreamid 20140727
Version: 0.%{upstreamid}
Release: 11%{?dist}
# latest seen in Hifenizador section of https://pt-br.libreoffice.org/projetos/vero/
Source0: https://pt-br.libreoffice.org/assets/Uploads/PT-BR-Documents/VERO/hyphptBR-213.zip
# The contents of Source1 are the same rules that are currently (2022-05-16) in
# use for pt-PT at https://cgit.freedesktop.org/libreoffice/dictionaries/tree/pt_PT
# so we continue to use those rules in the absence of a contrary opinion
Source1: https://sourceforge.net/projects/openofficeorg.mirror/files/contrib/dictionaries/hyph_pt_PT.zip
URL: https://pt-br.libreoffice.org/projetos/vero/
License: LGPL-3.0-only AND GPL-1.0-or-later
BuildArch: noarch

Requires: hyphen
Supplements: (hyphen and langpacks-pt)

%description
Portuguese hyphenation rules.

%package BR
Summary: Brazilian Portuguese hyphenation rules
Requires: hyphen
Supplements: (hyphen and langpacks-pt_BR)

%description BR
Brazilian Portuguese hyphenation rules.

%prep
%autosetup -c
unzip -q -o %{SOURCE1}

# Fix world writable permission on files
chmod 644 hyph_pt_PT.dic README_hyph_pt_PT.txt

for i in README_hyph_pt_BR.txt; do
  if ! iconv -f utf-8 -t utf-8 -o /dev/null $i > /dev/null 2>&1; then
    iconv -f ISO-8859-1 -t UTF-8 $i > $i.new
    touch -r $i $i.new
    mv -f $i.new $i
  fi
  tr -d '\r' < $i > $i.new
  touch -r $i $i.new
  mv -f $i.new $i
done


%build
#nothing to build here

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p *.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen
pushd $RPM_BUILD_ROOT/%{_datadir}/hyphen/
pt_PT_aliases="pt_AO"
for lang in $pt_PT_aliases; do
        ln -s hyph_pt_PT.dic "hyph_"$lang".dic"
done

%files
%doc README_hyph_pt_PT.txt
%{_datadir}/hyphen/hyph_pt_*.dic
%exclude %{_datadir}/hyphen/hyph_pt_BR.dic

%files BR
%doc README_hyph_pt_BR.txt
%{_datadir}/hyphen/hyph_pt_BR.dic

%changelog
* Fri Nov 01 2024 Sreenivasulu Malavathula <v-smalavthu@@microsoft.com> - 0.20140727-11
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Tue Jul 23 2024 Parag Nemade <pnemade AT redhat DOT com> - 0.20140727-10
- Fix file hyph_pt_PT.dic permission

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140727-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140727-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140727-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140727-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 23 2023 Caolán McNamara <caolanm@redhat.com> - 0.20140727-5
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140727-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140727-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 16 2022 Caolán McNamara <caolanm@redhat.com> - 0.20140727-2
- provide a pt-BR subpackage for consistency with hunspell-pt-BR

* Mon May 16 2022 Caolán McNamara <caolanm@redhat.com> - 0.20140727-1
- rhbz#2085482 update to latest available hyphenation rules
- rhbz#2084587 add Supplements: langpacks-pt_BR

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20021021-17
- Update Source tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20021021-13
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20021021-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20021021-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20021021-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20021021-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20021021-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20021021-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Caolán McNamara <caolanm@redhat.com> - 0.20021021-6
- Angola

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20021021-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20021021-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20021021-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20021021-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Caolán McNamara <caolanm@redhat.com> - 0.20021021-1
- initial version
