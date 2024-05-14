Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global ver_date 2014-11-08

Summary: Arabic hunspell dictionaries
Name: hunspell-ar
Version: 3.5
Release: 12%{?dist}
License: GPLv2 or LGPLv2 or MPLv1.1
URL: https://ayaspell.sourceforge.net/
Source: https://sourceforge.net/projects/ayaspell/files/hunspell-ar_%{version}.%{ver_date}.zip

BuildArch: noarch
Requires: hunspell
Supplements: (hunspell and langpacks-ar)

%description
Arabic (Egypt, Algeria, etc.) hunspell dictionaries.

%prep
%setup -q -c

%build
chmod -x *

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p ar.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/ar_TN.dic
cp -p ar.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/ar_TN.aff

pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
ar_TN_aliases="ar_AE ar_BH ar_DJ ar_DZ ar_EG ar_ER ar_IL ar_IN ar_IQ ar_JO ar_KM ar_KW ar_LB ar_LY ar_MA ar_MR ar_OM ar_PS ar_QA ar_SA ar_SD ar_SO ar_SY ar_TD ar_YE"
for lang in $ar_TN_aliases; do
    ln -s ar_TN.aff $lang.aff
    ln -s ar_TN.dic $lang.dic
done
popd

%files
%doc AUTHORS ChangeLog-ar COPYING README-* THANKS
%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.5-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.5-4
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 9 2014 Mosaab Alzoubi <moceap@hotmail.com> - 3.5-1
- Add ver_date to source link
- Update to 3.5

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 13 2014 Caolán McNamara <caolanm@redhat.com> - 3.2-1
- latest version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20080110-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20080110-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Peter Schiffer <pschiffe@redhat.com> - 0.20080110-8
- .spec file cleanup

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20080110-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20080110-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20080110-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20080110-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 06 2009 Caolán McNamara <caolanm@redhat.com> - 0.20080110-3
- extend aliases

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20080110-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Apr 28 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080110-1
- use the much lighter ayaspell data instead of Buckwalter

* Wed Jun 06 2007 Caolán McNamara <caolanm@redhat.com> - 0.20060208-1
- initial version
