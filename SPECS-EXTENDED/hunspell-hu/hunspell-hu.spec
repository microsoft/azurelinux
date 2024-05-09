Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-hu
Summary: Hungarian hunspell dictionaries
Version: 1.6.1
Release: 18%{?dist}
Source0: https://downloads.sourceforge.net/magyarispell/hu_HU-%{version}.tar.gz
Source1: %{name}-LICENSE.txt
URL: https://magyarispell.sourceforge.net
License: LGPLv2+ or GPLv2+ or MPLv1.1
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-hu)

%description
Hungarian hunspell dictionaries.

%prep
%setup -q -n hu_HU-%{version}
cp %{SOURCE1} ./LICENSE.txt

%build
chmod -x *

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p *.dic *.aff $RPM_BUILD_ROOT/%{_datadir}/myspell


%files
%license LICENSE.txt
%doc README_hu_HU.txt LEIRAS.txt
%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.1-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.6.1-10
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar 31 2010 Caolan McNamara <caolanm@redhat.com> - 1.6.1-1
- latest version

* Sat Feb 06 2010 Caolan McNamara <caolanm@redhat.com> - 1.6-1
- latest version

* Thu Nov 05 2009 Caolan McNamara <caolanm@redhat.com> - 1.5-2
- source audit shows content changed silently upstream

* Thu Sep 17 2009 Caolan McNamara <caolanm@redhat.com> - 1.5-1
- latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 23 2008 Caolan McNamara <caolanm@redhat.com> - 1.4-1
- latest version

* Mon Mar 17 2008 Caolan McNamara <caolanm@redhat.com> - 1.3-1
- latest version

* Mon Nov 05 2007 Caolan McNamara <caolanm@redhat.com> - 1.2.2-1
- latest version

* Tue Oct 02 2007 Caolan McNamara <caolanm@redhat.com> - 1.2.1-1
- latest version

* Fri Aug 03 2007 Caolan McNamara <caolanm@redhat.com> - 1.2-2
- clarify that this is tri-licenced

* Fri Jun 01 2007 Caolan McNamara <caolanm@redhat.com> - 1.2-1
- next version

* Sat May 05 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.1-1
- latest canonical version

* Wed Feb 14 2007 Caolan McNamara <caolanm@redhat.com> - 0.20061105-2
- match licence

* Thu Dec 07 2006 Caolan McNamara <caolanm@redhat.com> - 0.20061105-1
- initial version
