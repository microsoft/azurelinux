Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-sv
Summary: Swedish hunspell dictionaries
Version: 2.28
Release: 13%{?dist}
Source: https://extensions.libreoffice.org/extension-center/swedish-spelling-dictionary-den-stora-svenska-ordlistan/releases/2.28/ooo_swedish_dict_2-28.oxt
URL: https://dsso.se/
License: LGPLv3
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-sv)

%description
Swedish hunspell dictionaries.

%prep
%setup -q -c -n hunspell-sv

%build
sed -i 's/\r$//' LICENSE_sv_SE.txt
sed -i 's/\r$//' LICENSE_en_US.txt

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p dictionaries/*.dic dictionaries/*.aff $RPM_BUILD_ROOT/%{_datadir}/myspell


%files
%doc LICENSE_sv_SE.txt LICENSE_en_US.txt

%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.28-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 2.28-5
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Caolán McNamara <caolanm@redhat.com> - 2.28-1
- Resolves: rhbz#1102536 latest version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Caolán McNamara <caolanm@redhat.com> - 2.10-1
- Resolves: rhbz#868507 latest version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 08 2011 Caolán McNamara <caolanm@redhat.com> - 1.48-1
- latest version

* Wed Nov 16 2011 Caolán McNamara <caolanm@redhat.com> - 1.47-1
- latest version

* Wed Jun 29 2011 Caolán McNamara <caolanm@redhat.com> - 1.46-1
- latest version

* Thu Jun 09 2011 Caolán McNamara <caolanm@redhat.com> - 1.45-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Caolán McNamara <caolanm@redhat.com> - 1.44-1
- latest version

* Mon Jul 05 2010 Caolán McNamara <caolanm@redhat.com> - 1.43-1
- latest version

* Wed Apr 07 2010 Caolán McNamara <caolanm@redhat.com> - 1.42-2
- clarify licence

* Tue Feb 02 2010 Caolán McNamara <caolanm@redhat.com> - 1.42-1
- latest version

* Thu Jan 14 2010 Caolán McNamara <caolanm@redhat.com> - 1.41-1
- latest version

* Tue Nov 17 2009 Caolán McNamara <caolanm@redhat.com> - 1.40-2
- prefer .zip

* Tue Nov 03 2009 Caolán McNamara <caolanm@redhat.com> - 1.40-1
- latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Caolán McNamara <caolanm@redhat.com> - 1.39-1
- latest version

* Thu Jun 04 2009 Caolán McNamara <caolanm@redhat.com> - 1.38-1
- latest version

* Mon Jun 01 2009 Caolán McNamara <caolanm@redhat.com> - 1.37-1
- latest version

* Tue May 26 2009 Caolán McNamara <caolanm@redhat.com> - 1.35-1
- latest version

* Fri May 22 2009 Caolán McNamara <caolanm@redhat.com> - 1.33-1
- latest version

* Tue May 19 2009 Caolán McNamara <caolanm@redhat.com> - 1.32-1
- latest version

* Mon May 11 2009 Caolán McNamara <caolanm@redhat.com> - 1.31-1
- latest version

* Mon Apr 13 2009 Caolán McNamara <caolanm@redhat.com> - 1.30-1
- latest version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Aug 23 2008 Caolán McNamara <caolanm@redhat.com> - 1.29-1
- latest version
`
* Tue Jun 17 2008 Caolán McNamara <caolanm@redhat.com> - 1.28-1
- latest version

* Wed May 28 2008 Caolán McNamara <caolanm@redhat.com> - 1.27-1
- latest version

* Tue May 13 2008 Caolán McNamara <caolanm@redhat.com> - 1.26-1
- latest version

* Thu Mar 13 2008 Caolán McNamara <caolanm@redhat.com> - 1.25-1
- latest version

* Wed Mar 05 2008 Caolán McNamara <caolanm@redhat.com> - 1.23-1
- latest version

* Fri Aug 03 2007 Caolán McNamara <caolanm@redhat.com> - 1.22-2
- clarify license version

* Fri Jul 06 2007 Caolán McNamara <caolanm@redhat.com> - 1.22-1
- move to dsso.se dictionaries

* Fri Jul 06 2007 Caolán McNamara <caolanm@redhat.com> - 1.3.8.6b-1
- latest version

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 1.3.8.6-1
- initial version
