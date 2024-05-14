Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-sr
Summary: Serbian hunspell dictionaries
%global upstreamid 20130330
Version: 0.%{upstreamid}
Release: 15%{?dist}
Source: https://downloads.sourceforge.net/project/aoo-extensions/1572/10/dict-sr.oxt
URL: https://extensions.services.openoffice.org/project/dict-sr
License: LGPLv3
BuildArch: noarch
Requires: hunspell
Supplements: (hunspell and langpacks-sr)
Provides: hunspell-bs = %{version}-%{release}

%description
Serbian hunspell dictionaries.

%package -n hyphen-sr
Requires: hyphen
Summary: Serbian hyphenation rules
Provides: hyphen-bs = %{version}-%{release}
Supplements: (hyphen and langpacks-sr)

%description -n hyphen-sr
Serbian hyphenation rules.

%prep
%autosetup -c

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p sr.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/sr_YU.dic
cp -p sr.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/sr_YU.aff
cp -p sr-Latn.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/sh_YU.dic
cp -p sr-Latn.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/sh_YU.aff

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p hyph_sr.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen/hyph_sr_YU.dic
cp -p hyph_sr-Latn.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen/hyph_sh_YU.dic

sr_YU_aliases="sr_ME sr_RS"
sh_YU_aliases="sh_ME sh_RS bs_BA"

pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
for lang in $sr_YU_aliases; do
	ln -s sr_YU.aff $lang.aff
	ln -s sr_YU.dic $lang.dic
done
for lang in $sh_YU_aliases; do
	ln -s sh_YU.aff $lang.aff
	ln -s sh_YU.dic $lang.dic
done
popd

pushd $RPM_BUILD_ROOT/%{_datadir}/hyphen/
for lang in $sr_YU_aliases; do
	ln -s hyph_sr_YU.dic "hyph_"$lang".dic"
done
for lang in $sh_YU_aliases; do
	ln -s hyph_sh_YU.dic "hyph_"$lang".dic"
done
popd


%files
%doc registration/license*.txt
%{_datadir}/myspell/*

%files -n hyphen-sr
%doc registration/license*.txt
%{_datadir}/hyphen/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20130330-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130330-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130330-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130330-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130330-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 08 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20130330-10
- Update Source tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130330-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130330-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130330-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20130330-6
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130330-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130330-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130330-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130330-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 05 2013 Caolán McNamara <caolanm@redhat.com> - 0.20130330-1
- latest version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100920-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Caolán McNamara <caolanm@redhat.com> - 0.20100920-5
- clarify license

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100920-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100920-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100920-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 21 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100920-1
- latest version

* Thu Aug 19 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100818-1
- latest version

* Thu Jul 08 2010 Caolán McNamara <caolanm@redhat.com> - 0.20090511-4
- include licences in all subpackages

* Tue Jan 05 2010 Caolán McNamara <caolanm@redhat.com> - 0.20090511-3
- fix rpmlint warning

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090511-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090511-1
- latest version

* Tue May 05 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090213-1
- latest version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20080711-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 11 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080711-1
- initial version
