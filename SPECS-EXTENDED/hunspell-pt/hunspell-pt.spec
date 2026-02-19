Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%if 0%{?fedora} > 35
%global dict_dirname hunspell 
%else
%global dict_dirname myspell
%endif
Name: hunspell-pt
Summary: Portuguese hunspell dictionaries
%global upstreamid 20131030
Version: 0.%{upstreamid}
Release: 14%{?dist}
Source0: http://natura.di.uminho.pt/download/sources/Dictionaries/hunspell/hunspell-pt_PT-20130125.tar.gz
Source1: https://pt-br.libreoffice.org/assets/Uploads/PT-BR-Documents/VERO/ptBR-2013-10-30AOC-2.zip
URL: https://pt-br.libreoffice.org/projetos/vero
# pt_BR dicts are under LGPLv3 or MPL, pt_PT under GPLv2 or LGPLv2 or MPLv1.1
License: ( ( LGPL-3.0-only OR MPL-1.1 ) AND LGPL-2.1-only ) AND ( GPL-2.0-only OR LGPL-2.1-only OR MPL-1.1 )
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-pt)

%description
Portuguese hunspell dictionaries.

%package BR
Summary: Brazilian Portuguese hunspell dictionaries
Requires: hunspell
Supplements: (hunspell and langpacks-pt_BR)

%description BR
Brazilian Portuguese hunspell dictionaries

%prep
%setup -q -n hunspell-pt_PT-20130125
unzip -q -o %{SOURCE1}
for i in README_pt_BR.TXT README_pt_PT.txt; do
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

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
cp -p pt*.dic pt*.aff $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}

pushd $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}/
pt_PT_aliases="pt_AO"
for lang in $pt_PT_aliases; do
        ln -s pt_PT.aff $lang.aff
        ln -s pt_PT.dic $lang.dic
done
popd


%files
%doc README_pt_PT.txt
%license COPYING
%{_datadir}/%{dict_dirname}/*
%exclude %{_datadir}/%{dict_dirname}/pt_BR.*

%files BR
%doc README_pt_BR.TXT README_en.TXT
%{_datadir}/%{dict_dirname}/pt_BR.*

%changelog
* Fri Dec 20 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> - 0.20131030-14
- AzureLinux import from Fedora 41 .
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20131030-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20131030-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20131030-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20131030-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 22 2023 Caolán McNamara <caolanm@redhat.com> - 0.20131030-9
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20131030-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20131030-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 16 2022 Caolán McNamara <caolanm@redhat.com> - 0.20131030-6
- Related: rhbz#2084587 provide a pt-BR subpackage

* Fri May 13 2022 Caolán McNamara <caolanm@redhat.com> - 0.20131030-5
- Related: rhbz#2084587 try (pt or pt-BR)

* Thu May 12 2022 Caolán McNamara <caolanm@redhat.com> - 0.20131030-4
- Resolves: rhbz#2084587 add Supplements: langpacks-pt_BR

* Fri Feb 11 2022 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 0.20131030-3
- rename install directory name from myspell to hunspell
- https://fedoraproject.org/wiki/Changes/Hunspell_dictionary_dir_change

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20131030-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 12 2021 Caolán McNamara <caolanm@redhat.com> - 0.20131030-1
- Related: rhbz#2013265 upgrade to the latest pt_BR version and update URL

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130125-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130125-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130125-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130125-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130125-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130125-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130125-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 08 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20130125-10
- Mark Source1 as dead link

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130125-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130125-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130125-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20130125-6
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130125-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130125-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130125-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 29 2013 Caolán McNamara <caolanm@redhat.com> - 0.20130317-1
- latest pt_BR version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130125-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jan 31 2013 Caolán McNamara <caolanm@redhat.com> - 0.20130125-1
- latest pt_PT version

* Wed Sep 12 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120911-1
- latest pt_PT version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120611-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120611-1
- latest pt_PT version

* Tue May 08 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120312-2
- alias pt_AO to pt_PT instead

* Tue Apr 10 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120312-1
- latest pt_PT and pt_BR versions
- alias pt_AO to pt_BR (post-1990 orthographic accord)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20111102-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Caolán McNamara <caolanm@redhat.com> - 0.20111102-1
- latest pt_PT version

* Mon Oct 17 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110928-1
- latest pt_PT version

* Fri Aug 26 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110823-1
- latest pt_PT version

* Thu Jun 09 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110608-1
- latest pt_PT and pt_BR versions

* Sat Apr 02 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110331-1
- latest pt_PT version

* Fri Mar 18 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110318-1
- latest pt_PT version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20101214-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101214-1
- latest pt_PT version

* Wed Nov 10 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101104-1
- latest pt_PT version

* Wed Nov 03 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101031-1
- latest pt_PT version

* Sun Oct 31 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101030-1
- latest pt_PT version

* Thu Oct 28 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101027-1
- latest pt_PT version

* Wed Jun 09 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100907-1
- latest pt_BR version

* Wed Jun 09 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100109-2
- Resolves: rhbz#602193 clarify licences

* Sun Jan 10 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100109-1
- latest pt_BR version

* Thu Oct 15 2009 Caolán McNamara <caolanm@redhat.com> - 0.20091013-1
- latest pt_PT version

* Tue Oct 06 2009 Caolán McNamara <caolanm@redhat.com> - 0.20091004-1
- latest pt_BR version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090702-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090702-2
- tidy spec

* Fri Jul 03 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090702-1
- latest pt_BR version

* Thu Apr 30 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090330-1
- latest pt_BR version

* Tue Mar 10 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090309-1
- latest pt_PT version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20081113-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 23 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081113-1
- latest pt_PT version

* Tue Jul 08 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080707-1
- latest pt_BR version

* Mon Jul 07 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080705-1
- latest pt_PT version

* Tue Jun 10 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080610-1
- latest version

* Fri Mar 21 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080320-1
- latest version

* Thu Feb 21 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080221-1
- latest version

* Fri Feb 15 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080210-1
- latest version

* Fri Dec 14 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071212-1
- latest version

* Sun Nov 11 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071106-1
- latest version

* Mon Nov 05 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071101-1
- latest version

* Fri Oct 05 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071003-1
- next version

* Tue Oct 02 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071001-1
- next version

* Tue Aug 28 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070823-2
- source file audit shows that pt_BR-2007-04-11.zip silently changed
  content, updating to match

* Thu Aug 23 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070823-1
- latest version

* Fri Aug 03 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070709-2
- clarify licences

* Wed Jul 18 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070709-1
- latest pt_PT version

* Sun May 06 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070411-1
- latest versions

* Wed Feb 14 2007 Caolán McNamara <caolanm@redhat.com> - 0.20061026-2
- disambiguate readmes

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 0.20061026-1
- initial version
