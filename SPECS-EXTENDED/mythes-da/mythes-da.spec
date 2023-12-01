Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: mythes-da
Summary: Danish thesaurus
%global upstreamid 20100629.15.16
Version: 0.%{upstreamid}
Release: 20%{?dist}
Source0: https://excellmedia.dl.sourceforge.net/project/aoo-extensions/1388/12/danskesynonymer.oxt
Source1: %{name}-LICENSE.txt
URL: https://extensions.openoffice.org/fr/project/danske-synonymer
License: GPLv2 or LGPLv2 or MPLv1.1
BuildArch: noarch
Requires: mythes
Supplements: (mythes and langpacks-da)

%description
Danish thesaurus.

%prep
%autosetup -c
cp %{SOURCE1} ./LICENSE.txt

%build
for i in README_th_da_DK.txt README_th_da_DK.txt README_th_en-US.txt; do
  tr -d '\r' < $i > $i.new
  touch -r $i $i.new
  mv -f $i.new $i
done

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mythes
cp -p th_da_DK.dat $RPM_BUILD_ROOT/%{_datadir}/mythes/th_da_DK_v2.dat
cp -p th_da_DK.idx $RPM_BUILD_ROOT/%{_datadir}/mythes/th_da_DK_v2.idx


%files
%license LICENSE.txt
%doc README_th_da_DK.txt README_th_en-US.txt release_note.txt
%{_datadir}/mythes/*

%changelog
* Fri Dec 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.20100629.15.16-20
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20100629.15.16-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20100629.15.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20100629.15.16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20100629.15.16-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20100629.15.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20100629.15.16-14
- Update Source and URL tags

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20100629.15.16-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20100629.15.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20100629.15.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20100629.15.16-10
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20100629.15.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100629.15.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100629.15.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100629.15.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100629.15.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100629.15.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100629.15.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100629.15.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 02 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100629.15.16
- latest version

* Sat Apr 03 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100126.13.05-2
- mythes now owns /usr/share/mythes

* Thu Jan 28 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100126.13.05-1
- latest version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090522-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090522-2
- tidy spec

* Sat May 23 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090522-1
- latest version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-0.2.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Caolán McNamara <caolanm@redhat.com> - 0.1.9-0.1.beta
- initial version
