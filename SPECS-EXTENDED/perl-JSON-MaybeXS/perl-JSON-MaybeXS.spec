# Note: this package takes the approach of adding a hard dependency on
# upstream's preferred back-end, Cpanel::JSON::XS, rather than using
# a virtual provides/requires arrangement so that any of the supported
# back-ends could be used. This is not only much simpler and does not
# involve modifications to the back-end packages, but it also makes for
# consistent results as we're always using the same, most-tested
# back-end.

Name:		perl-JSON-MaybeXS
Summary:	Use Cpanel::JSON::XS with a fallback to JSON::XS and JSON::PP
Version:	1.004008
Release:	2%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/JSON-MaybeXS
Source0:	https://cpan.metacpan.org/modules/by-module/JSON/JSON-MaybeXS-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	perl(lib)
BuildRequires:	perl(Text::ParseWords)
# Dependencies of bundled ExtUtils::HasCompiler
BuildRequires:	perl(Config)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(ExtUtils::Mksymlists)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
# Module Runtime
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
%if 0%{?fedora} > 36 || 0%{?rhel} > 9
BuildRequires:	perl(Cpanel::JSON::XS) >= 4.38
BuildRequires:	perl(experimental)
%else
BuildRequires:	perl(Cpanel::JSON::XS) >= 2.3310
%endif
BuildRequires:	perl(Exporter)
BuildRequires:	perl(if)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(JSON::PP) >= 2.27300
BuildRequires:	perl(JSON::XS) >= 3.0
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Test::Needs) >= 0.002006
# Dependencies
%if 0%{?fedora} > 36 || 0%{?rhel} > 9
Requires:	perl(Cpanel::JSON::XS) >= 4.38
Requires:	perl(experimental)
%else
Requires:	perl(Cpanel::JSON::XS) >= 2.3310
%endif

%description
This module first checks to see if either Cpanel::JSON::XS or JSON::XS
is already loaded, in which case it uses that module. Otherwise it tries
to load Cpanel::JSON::XS, then JSON::XS, then JSON::PP in order, and
either uses the first module it finds or throws an error.

It then exports the "encode_json" and "decode_json" functions from the
loaded module, along with a "JSON" constant that returns the class name
for calling "new" on.

If you're writing fresh code rather than replacing JSON.pm usage, you
might want to pass options as constructor args rather than calling
mutators, so we provide our own "new" method that supports that.

%prep
%setup -q -n JSON-MaybeXS-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/JSON/
%{_mandir}/man3/JSON::MaybeXS.3*

%changelog
* Tue Aug 13 2024 Paul Howarth <paul@city-fan.org> - 1.004008-2
- Fix runtime dependency on Cpanel::JSON::XS 4.38 (rhbz#2304277)

* Sun Aug 11 2024 Paul Howarth <paul@city-fan.org> - 1.004008-1
- Update to 1.004008
  - Improved boolean testing

* Sun Aug  4 2024 Paul Howarth <paul@city-fan.org> - 1.004007-1
- Update to 1.004007
  - is_bool() now recognizes core booleans (perl 5.36+); note that JSON::PP
   4.11 and Cpanel::JSON::XS 4.38 are required to properly encode them

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.004005-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.004005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.004005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.004005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr 30 2023 Paul Howarth <paul@city-fan.org> - 1.004005-1
- Update to 1.004005
  - to_json and from_json are now documented (GH#2)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.004004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 20 2022 Paul Howarth <paul@city-fan.org> - 1.004004-1
- Update to 1.004004
  - Slight speed optimization for is_bool()
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.004003-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.004003-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.004003-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.004003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.004003-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.004003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 13 2020 Paul Howarth <paul@city-fan.org> - 1.004003-1
- Update to 1.004003
  - Fix another test that fails when JSON::XS is installed, but below version
    3.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.004002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.004002-2
- Perl 5.32 rebuild

* Mon May 18 2020 Paul Howarth <paul@city-fan.org> - 1.004002-1
- Update to 1.004002
  - Fix test that fails when JSON::XS is installed, but below version 3.0
    (CPAN RT#132578)

* Sat May  2 2020 Paul Howarth <paul@city-fan.org> - 1.004001-1
- Update to 1.004001
  - Document when is_bool became available
  - Now favouring Cpanel::JSON::XS over JSON::XS in more situations (the former
    is always added to prereqs when a compiler is available, although JSON::XS
    is still used at runtime if new enough and Cpanel::JSON::XS is not
    installed); this makes boolean handling more predictable and consistent
- Package LICENSE file
- Use %%{make_build} and %%{make_install}

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.004000-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.004000-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.004000-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.004000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.004000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.004000-2
- Perl 5.28 rebuild

* Fri Apr 20 2018 Paul Howarth <paul@city-fan.org> - 1.004000-1
- Update to 1.004000
  - Added true and false subs so they can be used via JSON::MaybeXS rather than
    only JSON() exported sub

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.003010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Paul Howarth <paul@city-fan.org> - 1.003010-1
- Update to 1.003010
  - Use bundled ExtUtils::HasCompiler rather than ExtUtils::CBuilder to detect
    compiler availability
  - Clarify exported JSON in documentation
- This release by HAARG → update source URL

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.003009-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.003009-2
- Perl 5.26 rebuild

* Mon Feb 27 2017 Paul Howarth <paul@city-fan.org> - 1.003009-1
- Update to 1.003009
  - Fix tests to no longer rely on . being in @INC (CPAN RT#120404)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.003008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct  3 2016 Paul Howarth <paul@city-fan.org> - 1.003008-1
- Update to 1.003008
  - Added an INSTALLATION section to documentation, to clarify the use of
    dynamic prerequisites in Makefile.PL
  - Minimize prereqs listed in META.json to avoid giving the appearance of XS
    prerequisites, and confusing static inspection tools such as metacpan.org

* Mon Sep 12 2016 Paul Howarth <paul@city-fan.org> - 1.003007-1
- Update to 1.003007
  - Bump prereq on JSON::PP, to ensure we get the fix for parsing utf8-encoded
    values
  - We now always upgrade JSON::XS if it is installed and below version 3.0,
    due to changes in handling booleans
  - Remove test dependency on Test::Without::Module (CPAN RT#115394)
- Simplify find command using -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.003005-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.003005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.003005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.003005-2
- Perl 5.22 rebuild

* Mon Mar 23 2015 Paul Howarth <paul@city-fan.org> - 1.003005-1
- Update to 1.003005
  - Fix x_contributors metadata that was killing metacpan (see
    https://github.com/CPAN-API/cpan-api/issues/401)

* Sun Mar 15 2015 Paul Howarth <paul@city-fan.org> - 1.003004-1
- Update to 1.003004
  - Caveat added to documentation about type checking the object returned by
    new() (CPAN RT#102733)

* Mon Dec  8 2014 Paul Howarth <paul@city-fan.org> - 1.003003-1
- Update to 1.003003
  - Ensure an old Cpanel::JSON::XS is upgraded if it is too old, as it will
    always be used in preference to JSON::XS
  - Avoid "JSON::XS::Boolean::* redefined" warnings caused by an old JSON::XS
    loaded at the same time as a newer Cpanel::JSON::XS

* Sun Nov 16 2014 Paul Howarth <paul@city-fan.org> - 1.003002-1
- Update to 1.003002
  - Correctly fix boolean interoperability with older Cpanel::JSON::MaybeXS

* Thu Nov 13 2014 Paul Howarth <paul@city-fan.org> - 1.003001-1
- Update to 1.003001
  - Add :legacy tag to support legacy apps
  - Fix boolean interoperability with older Cpanel::JSON::MaybeXS

* Wed Oct 22 2014 Paul Howarth <paul@city-fan.org> - 1.002006-1
- Update to 1.002006
  - Add some additional test diagnostics, to help find bad version combinations
    of JSON backends

* Wed Oct 15 2014 Paul Howarth <paul@city-fan.org> - 1.002005-1
- Update to 1.002005
  - Fix "can I haz XS?" logic precedence in Makefile.PL
  - Added the ':all' export tag
  - Removed dependency on Safe::Isa
  - Repository moved to git://git.shadowcat.co.uk/p5sagit/JSON-MaybeXS.git

* Sun Oct 12 2014 Paul Howarth <paul@city-fan.org> - 1.002004-1
- Update to 1.002004
  - Support use of PUREPERL_ONLY in Makefile.PL to avoid adding an XS
    dependency
  - New is_bool() interface

* Wed Oct  8 2014 Paul Howarth <paul@city-fan.org> - 1.002003-1
- Update to 1.002003
  - Document how to use booleans

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.002002-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  9 2014 Paul Howarth <paul@city-fan.org> - 1.002002-2
- Sanitize for Fedora submission

* Thu Apr 24 2014 Paul Howarth <paul@city-fan.org> - 1.002002-1
- Update to 1.002002
  - More metadata fiddling, to remove the Cpanel::JSON::XS dependency visible
    to static analyzers (the prerequisites at install time remain unchanged)

* Wed Apr 23 2014 Paul Howarth <paul@city-fan.org> - 1.002001-1
- Update to 1.002001
  - Fix installation on older perls with an older ExtUtils::MakeMaker
    (CPAN RT#94964)
- Update patch for building with Test::More < 0.88

* Wed Apr 23 2014 Paul Howarth <paul@city-fan.org> - 1.002000-1
- Initial RPM version
