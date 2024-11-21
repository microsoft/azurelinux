Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-es
Summary: Spanish hunspell dictionaries
Version: 2.3
Release: 8%{?dist}
Source0: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_AR.oxt
Source1: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_BO.oxt
Source2: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_CL.oxt
Source3: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_CO.oxt
Source4: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_CR.oxt
Source5: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_CU.oxt
Source6: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_DO.oxt
Source7: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_EC.oxt
Source8: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_ES.oxt
Source9: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_GT.oxt
Source10: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_HN.oxt
Source11: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_MX.oxt
Source12: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_NI.oxt
Source13: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_PA.oxt
Source14: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_PE.oxt
Source15: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_PR.oxt
Source16: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_PY.oxt
Source17: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_SV.oxt
Source18: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_UY.oxt
Source19: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_US.oxt
Source20: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_VE.oxt

URL: https://github.com/sbosio/rla-es/
License: LGPLv3+ or GPLv3+ or MPLv1.1
BuildArch: noarch

Requires: hunspell
Requires: hunspell-es-AR = %{version}-%{release}
Requires: hunspell-es-BO = %{version}-%{release}
Requires: hunspell-es-CL = %{version}-%{release}
Requires: hunspell-es-CO = %{version}-%{release}
Requires: hunspell-es-CR = %{version}-%{release}
Requires: hunspell-es-CU = %{version}-%{release}
Requires: hunspell-es-DO = %{version}-%{release}
Requires: hunspell-es-EC = %{version}-%{release}
Requires: hunspell-es-ES = %{version}-%{release}
Requires: hunspell-es-GT = %{version}-%{release}
Requires: hunspell-es-HN = %{version}-%{release}
Requires: hunspell-es-MX = %{version}-%{release}
Requires: hunspell-es-NI = %{version}-%{release}
Requires: hunspell-es-PA = %{version}-%{release}
Requires: hunspell-es-PE = %{version}-%{release}
Requires: hunspell-es-PR = %{version}-%{release}
Requires: hunspell-es-PY = %{version}-%{release}
Requires: hunspell-es-SV = %{version}-%{release}
Requires: hunspell-es-UY = %{version}-%{release}
Requires: hunspell-es-US = %{version}-%{release}
Requires: hunspell-es-VE = %{version}-%{release}
Supplements: (hunspell and langpacks-es)

%description
Spanish (Spain, Mexico, etc.) hunspell dictionaries.

%package        AR
Requires:       hunspell
Summary:        Argentine Spanish hunspell dictionary

%description    AR
Argentine Spanish hunspell dictionary

%package        BO
Requires:       hunspell
Summary:        Bolivian Spanish hunspell dictionary

%description    BO
Bolivian Spanish hunspell dictionary

%package        CL
Requires:       hunspell
Summary:        Chilean Spanish hunspell dictionary

%description    CL
Chilean Spanish hunspell dictionary

%package        CO
Requires:       hunspell
Summary:        Colombian Spanish hunspell dictionary

%description    CO
Colombian Spanish hunspell dictionary

%package        CR
Requires:       hunspell
Summary:        Costa Rican Spanish hunspell dictionary

%description    CR
Costa Rican Spanish hunspell dictionary

%package        CU
Requires:       hunspell
Summary:        Cuban Spanish hunspell dictionary

%description    CU
Cuban Spanish hunspell dictionary

%package        DO
Requires:       hunspell
Summary:        Dominican Spanish hunspell dictionary

%description    DO
Dominican Spanish hunspell dictionary

%package        EC
Requires:       hunspell
Summary:        Ecuadorian Spanish hunspell dictionary

%description    EC
Ecuadorian Spanish hunspell dictionary

%package        ES
Requires:       hunspell
Summary:        European Spanish hunspell dictionary

%description    ES
European Spanish hunspell dictionary

%package        GT
Requires:       hunspell
Summary:        Guatemalan Spanish hunspell dictionary

%description    GT
Guatemalan Spanish hunspell dictionary

%package        HN
Requires:       hunspell
Summary:        Honduran Spanish hunspell dictionary

%description    HN
Honduran Spanish hunspell dictionary

%package        MX
Requires:       hunspell
Summary:        Mexican Spanish hunspell dictionary

%description    MX
Mexican Spanish hunspell dictionary

%package        NI
Requires:       hunspell
Summary:        Nicaraguan Spanish hunspell dictionary

%description    NI
Nicaraguan Spanish hunspell dictionary

%package        PA
Requires:       hunspell
Summary:        Panamanian Spanish hunspell dictionary

%description    PA
Panamanian Spanish hunspell dictionary

%package        PE
Requires:       hunspell
Summary:        Peruvian Spanish hunspell dictionary

%description    PE
Peruvian Spanish hunspell dictionary

%package        PR
Requires:       hunspell
Summary:        Puerto Rican Spanish hunspell dictionary

%description    PR
Puerto Rican Spanish hunspell dictionary

%package        PY
Requires:       hunspell
Summary:        Paraguayan Spanish hunspell dictionary

%description    PY
Paraguayan Spanish hunspell dictionary

%package        SV
Requires:       hunspell
Summary:        Salvadoran Spanish hunspell dictionary

%description    SV
Salvadoran Spanish hunspell dictionary

%package        US
Requires:       hunspell
Summary:        US Spanish hunspell dictionary

%description    US
US Spanish hunspell dictionary

%package        UY
Requires:       hunspell
Summary:        Uruguayan Spanish hunspell dictionary

%description    UY
Uruguayan Spanish hunspell dictionary

%package        VE
Requires:       hunspell
Summary:        Venezuelan Spanish hunspell dictionary

%description    VE
Venezuelan Spanish hunspell dictionary

%define es_REGIONS es_ES es_AR es_BO es_CL es_CO es_CR es_CU es_DO es_EC es_GT es_HN es_MX es_NI es_PA es_PE es_PR es_PY es_SV es_US es_UY es_VE

%prep
%setup -q -c -n hunspell-es

for REGION in %{es_REGIONS}; do
    unzip -q -o %{_sourcedir}/${REGION}.oxt
done

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell

# supported Spanish language regions:
for REGION in %{es_REGIONS}; do
    cp -p $REGION.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/
    cp -p $REGION.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/
done

%files

%files ES
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_ES.*


%files AR
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_AR.*


%files BO
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_BO.*


%files CL
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_CL.*


%files CO
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_CO.*


%files CR
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_CR.*


%files CU
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_CU.*


%files DO
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_DO.*


%files EC
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_EC.*


%files GT
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_GT.*


%files HN
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_HN.*


%files MX
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_MX.*


%files NI
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_NI.*


%files PA
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_PA.*


%files PE
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_PE.*


%files PR
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_PR.*


%files PY
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_PY.*


%files SV
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_SV.*


%files US
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_US.*


%files UY
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_UY.*


%files VE
%doc README.txt Changelog.txt
%license GPLv3.txt MPL-1.1.txt LGPLv3.txt
%{_datadir}/myspell/es_VE.*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.3-8
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:2.3-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 8 2018 Ismael Olea <ismael@olea.org> - 1:2.3-1
- update to v2.3
- using license tag

* Tue Jan 2 2018 Ismael Olea <ismael@olea.org> - 1:2.2-3
- use upstream all Spanish variants supported by RLA-ES project

* Fri Aug 18 2017 Caolán McNamara <caolanm@redhat.com> - 1:2.2-2
- use upstream es_MX for Mexican variant

* Thu Aug 17 2017 Caolán McNamara <caolanm@redhat.com> - 1:2.2-1
- update to 2.2

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 1:0.7-6
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Caolán McNamara <caolanm@redhat.com> - 1:0.7-1
- update to 0.7

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Ismael Olea <ismael@olea.org> - 1:0.6-1
- update to 0.6

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20081215-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20081215-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20081215-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20081215-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 16 2008 Caolan McNamara <caolanm@redhat.com> - 0.20081215-1
- latest version

* Mon Sep 29 2008 Caolan McNamara <caolanm@redhat.com> - 0.20051031-3
- add es_CU as Cuba for OOo

* Tue Jul 08 2008 Caolan McNamara <caolanm@redhat.com> - 0.20051031-2
- add es_US

* Mon Aug 20 2007 Caolan McNamara <caolanm@redhat.com> - 0.20051031-1
- latest version
- clarify license version

* Thu Aug 09 2007 Caolan McNamara <caolanm@redhat.com> - 0.20050510-2
- clarify license version

* Thu Dec 07 2006 Caolan McNamara <caolanm@redhat.com> - 0.20050510-1
- initial version
