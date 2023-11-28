# Got the intial spec from Fedora and modified it
Summary:        Internationalization library for Perl, compatible with gettext
Name:           perl-libintl-perl
Version:        1.33
Release:        1%{?dist}
License:        GPLv3+
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/libintl-perl/
Source:         https://cpan.metacpan.org/authors/id/G/GU/GUIDO/libintl-perl-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with_check}
BuildRequires:  perl(Test)
%endif

Requires:       perl-libs
Requires:       perl(Carp)
Requires:       perl(Encode::Alias)
Requires:       perl(POSIX)
Requires:       perl(I18N::Langinfo)

Provides:       perl(Locale::Messages) = %{version}-%{release}
Provides:       perl(Locale::Recode) = %{version}-%{release}
Provides:       perl(Locale::Recode::_Aliases) = %{version}-%{release}
Provides:       perl(Locale::Recode::_Conversions) = %{version}-%{release}
Provides:       perl(Locale::RecodeData) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ASMO_449) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ATARI_ST) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ATARI_ST_EURO) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::CP10007) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::CP1250) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::CP1251) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::CP1252) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::CP1253) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::CP1254) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::CP1256) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::CP1257) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::CSN_369103) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::CWI) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::DEC_MCS) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_AT_DE) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_AT_DE_A) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_CA_FR) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_DK_NO) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_DK_NO_A) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_ES) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_ES_A) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_ES_S) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_FI_SE) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_FI_SE_A) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_FR) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_IS_FRISS) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_IT) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_PT) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_UK) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::EBCDIC_US) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ECMA_CYRILLIC) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::GEORGIAN_ACADEMY) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::GEORGIAN_PS) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::GOST_19768_74) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::GREEK7) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::GREEK7_OLD) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::GREEK_CCITT) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::HP_ROMAN8) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM037) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM038) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM1004) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM1026) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM1047) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM256) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM273) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM274) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM275) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM277) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM278) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM280) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM281) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM284) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM285) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM290) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM297) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM420) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM423) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM424) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM437) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM500) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM850) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM851) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM852) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM855) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM857) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM860) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM861) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM862) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM863) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM864) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM865) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM866) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM868) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM869) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM870) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM871) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM874) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM875) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM880) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM891) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM903) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM904) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM905) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IBM918) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::IEC_P27_1) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::INIS) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::INIS_8) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::INIS_CYRILLIC) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_10367_BOX) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_2033_1983) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_5427) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_5427_EXT) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_5428) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_1) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_10) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_11) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_13) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_14) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_15) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_16) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_2) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_3) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_4) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_5) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_6) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_7) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_8) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::ISO_8859_9) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::KOI8_R) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::KOI8_RU) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::KOI8_T) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::KOI8_U) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::KOI_8) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::LATIN_GREEK) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::LATIN_GREEK_1) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MACARABIC) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MACCROATIAN) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MACCYRILLIC) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MACGREEK) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MACHEBREW) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MACICELAND) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MACINTOSH) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MACROMANIA) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MACTHAI) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MACTURKISH) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MACUKRAINE) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MAC_IS) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MAC_SAMI) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::MAC_UK) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::NATS_DANO) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::NATS_SEFI) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::NEXTSTEP) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::SAMI_WS2) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::TIS_620) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::US_ASCII) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::UTF_8) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::VISCII) = %{version}-%{release}
Provides:       perl(Locale::RecodeData::_Encode) = %{version}-%{release}
Provides:       perl(Locale::TextDomain) = %{version}-%{release}
Provides:       perl(Locale::Util) = %{version}-%{release}
Provides:       perl(Locale::gettext_dumb) = %{version}-%{release}
Provides:       perl(Locale::gettext_pp) = %{version}-%{release}
Provides:       perl(Locale::gettext_xs) = %{version}-%{release}
Provides:       perl(__TiedTextDomain) = %{version}-%{release}

%description
The package libintl-perl is an internationalization library for Perl that
aims to be compatible with the Uniforum message translations system as
implemented for example in GNU gettext.


%prep
%setup -q -n libintl-perl-%{version}
find -type f -exec chmod -x {} \;
find lib/Locale gettext_xs \( -name '*.pm' -o -name '*.pod' \) \
    -exec sed -i -e '/^#! \/bin\/false/d' {} \;

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name '*.bs' -size 0 \) -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%license COPYING
%{perl_vendorlib}/Locale/
%{perl_vendorarch}/auto/Locale/
%{_mandir}/man?/*

%changelog
* Mon Nov 27 2023 Andrew Phelps <anphel@microsoft.com> - 1.33-1
- Upgrade to 1.33

* Fri Jul 29 2022 Muhammad Falak <mwani@microsoft.com> - 1.32-2
- Add BR on `perl(ExtUtils::MakeMaker)` & `perl(Test)` to enable ptest

* Fri Apr 22 2022 Mateusz Malisz <mamalisz@microsoft.com> - 1.32-1
- Update to 1.32

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.29-6
- Adding 'BuildRequires: perl-generators'.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.29-5
- Use new perl package names.
- Provide perl(Locale::*).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.29-4
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.29-3
- Renaming perl-libintl to perl-libintl-perl

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.29-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.29-1
- Update to version 1.29

* Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 1.26-1
- upgrade for 2.0

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.24-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.24-1
- Upgraded to version 1.24

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.23-1
- Initial version.
