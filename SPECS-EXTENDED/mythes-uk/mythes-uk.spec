Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: mythes-uk
Summary: Ukrainian thesaurus
Version: 1.6.5
Release: 19%{?dist}
Source: https://downloads.sourceforge.net/ispell-uk/spell-uk-%{version}.tgz
URL: https://sourceforge.net/projects/ispell-uk
#unused myspell dicts are under GPLv2+ or LGPLv2+ or MPLv1.1
#unused hyphenation dicts are under GPLv2+
#toplevel is GPLv2+ or LGPLv2+
License: (GPLv2+ or LGPLv2+) and (GPLv2+ or LGPLv2+ or MPLv1.1) and GPLv2+
BuildRequires: perl-interpreter, mythes-devel
BuildArch: noarch
Requires: mythes
Supplements: (mythes and langpacks-uk)

%description
Ukrainian thesaurus.

%prep
%autosetup -n spell-uk-%{version}

%build
cd src/thesaurus
mv -f th_uk_UA.dat th_uk_UA_v2.dat
th_gen_idx.pl < th_uk_UA_v2.dat > th_uk_UA_v2.idx

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mythes
cp -p src/thesaurus/th_uk_UA_v2.* $RPM_BUILD_ROOT/%{_datadir}/mythes


%files
%doc README README.uk Copyright
%license COPYING.GPL COPYING.LGPL
%{_datadir}/mythes/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.5-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 1.6.5-14
- Mark Source as dead now

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.6.5-10
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Caolán McNamara <caolanm@redhat.com> - 1.6.5-4
- clarify license

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun May 22 2011 Caolán McNamara <caolanm@redhat.com> - 1.6.5-1
- latest version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Apr 04 2010 Caolan McNamara <caolanm@redhat.com> - 1.6.0-2
- mythes now owns /usr/share/mythes

* Tue Aug 18 2009 Caolán McNamara <caolanm@redhat.com> - 1.6.0-1
- latest version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 06 2009 Caolán McNamara <caolanm@redhat.com> - 1.5.7-1
- initial version
