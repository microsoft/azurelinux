Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: openoffice-lv
Summary: Latvian linguistic dictionaries
Version: 1.0.0
Release: 12%{?dist}
Source: https://dict.dv.lv/download/lv_LV-%{version}.oxt
URL: https://dict.dv.lv/
License: LGPLv2+
BuildArch: noarch

%description
Latvian linguistic dictionaries.

%package -n hunspell-lv
Summary: Latvian hunspell dictionaries
Requires: hunspell

%description -n hunspell-lv
Latvian hunspell dictionaries.

%package -n hyphen-lv
Summary: Latvian hyphenation rules
Requires: hyphen

%description -n hyphen-lv
Latvian hyphenation rules.

%package -n mythes-lv
Summary: Latvian thesaurus
Requires: mythes

%description -n mythes-lv
Latvian thesaurus.

%prep
%autosetup -c

%build
for i in README_lv_LV.txt README_hyph_lv_LV.txt; do
  if ! iconv -f utf-8 -t utf-8 -o /dev/null $i > /dev/null 2>&1; then
    iconv -f ISO-8859-4 -t UTF-8 $i > $i.new
    touch -r $i $i.new
    mv -f $i.new $i
  fi
  tr -d '\r' < $i > $i.new
  touch -r $i $i.new
  mv -f $i.new $i
done
chmod -x *.dic

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mythes
cp -p lv_LV.dic lv_LV.aff $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p hyph_lv_LV.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p th_lv_LV_v2.* $RPM_BUILD_ROOT/%{_datadir}/mythes

%files -n hunspell-lv
%doc README_lv_LV.txt
%license license.txt
%{_datadir}/myspell/*

%files -n hyphen-lv
%doc README_hyph_lv_LV.txt
%license license.txt
%{_datadir}/hyphen/*

%files -n mythes-lv
%doc package-description.txt
%license license.txt
%{_datadir}/mythes/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 1.0.0-7
- Update to current Fedora packaging guidelines
- Dropped Group and defattr tag
- Added license tag

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Sep 19 2014 Caolán McNamara <caolanm@redhat.com> - 1.0.0-1
- latest version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jul 25 2013 Caolán McNamara <caolanm@redhat.com> - 0.9.6-1
- latest version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar 18 2011 Caolán McNamara <caolanm@redhat.com> - 0.9.4-1
- latest version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Sep 05 2010 Caolán McNamara <caolanm@redhat.com> - 0.9.3-1
- latest version

* Tue Aug 17 2010 Caolán McNamara <caolanm@redhat.com> - 0.9.2-1
- latest version

* Thu Jul 08 2010 Caolán McNamara <caolanm@redhat.com> - 0.9.1-2
- add licence.txt to all subpackages

* Sun Apr 25 2010 Caolán McNamara <caolanm@redhat.com> - 0.9.1-1
- latest version

* Mon Apr 19 2010 Caolán McNamara <caolanm@redhat.com> - 0.9.0-1
- latest version

* Sun Apr 04 2010 Caolán McNamara <caolanm@redhat.com> - 0.8.2-2
- mythes now owns /usr/share/mythes

* Sat Sep 19 2009 Caolán McNamara <caolanm@redhat.com> - 0.8.2-1
- latest version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-0.3.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.8-0.2.b1
- tidy spec

* Mon May 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.8-0.1.b1
- latest version

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 23 2008 Caolán McNamara <caolanm@redhat.com> - 0.7.4-1
- latest version

* Sat Sep 20 2008 Caolán McNamara <caolanm@redhat.com> - 0.7.3-1
- initial version
