Name:           perl-Type-Tiny
Version:        2.008002
Release:        2%{?dist}
Summary:        Tiny, yet Moo(se)-compatible type constraint
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Type-Tiny
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Type-Tiny-%{version}.tar.gz#/perl-Type-Tiny-%{version}.tar.gz
BuildArch:      noarch
 
# --with reply_plugin
#	Default: --without
# Marked as unstable (cf. lib/Reply/Plugin/TypeTiny.pm)
%bcond_with reply_plugin
 
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  sed
BuildRequires:  %{__make}
BuildRequires:  %{__perl}
 
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(:VERSION) >= 5.6.1
 
BuildRequires:  perl(B)
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(CPAN::Meta::Requirements)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
%if "%{version}" >= "2.000001"
BuildRequires:  perl(Exporter::Tiny) >= 1.004001
%else
BuildRequires:  perl(Exporter::Tiny) >= 0.040
%endif
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.17
%if "%{version}" >= "2.000001"
BuildRequires:  perl(experimental)
%endif
BuildRequires:  perl(feature)
BuildRequires:  perl(lib)
BuildRequires:  perl(Math::BigFloat)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Fatal)
#BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(Test::Tester) >= 0.109
%if "%{version}" >= "2.000001"
BuildRequires:  perl(Test::Deep)
%endif
BuildRequires:  perl(Text::Balanced)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(threads)
BuildRequires:  perl(Tie::Array)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(Tie::Scalar)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
 
Requires:       perl(B::Deparse)
Requires:       perl(Carp)
Requires:       perl(Data::Dumper)
 
Recommends:	perl(Type::Tiny::XS)
 
%description
Type::Tiny is a tiny class for creating Moose-like type constraint objects
which are compatible with Moo, Moose and Mouse.
 
%package -n perl-Test-TypeTiny
Summary: Test::TypeTiny module
 
%description -n perl-Test-TypeTiny
Test::TypeTiny module.
 
%prep
%setup -q -n Type-Tiny-%{version}
# Remove bundled modules
rm -r ./inc
sed -i -e '/^inc\//d' MANIFEST
 
%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}
 
%install
%{make_install} DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*
 
%check
%{__make} test
 
%files
%doc Changes CREDITS NEWS README
%license LICENSE COPYRIGHT
%{perl_vendorlib}/*
%{!?with_reply_plugin:%exclude %{perl_vendorlib}/Reply}
%{_mandir}/man3/*
%exclude %{perl_vendorlib}/Test
%exclude %{_mandir}/man3/Test::TypeTiny.3pm*
 
%files -n perl-Test-TypeTiny
%{perl_vendorlib}/Test
%{_mandir}/man3/Test::TypeTiny.3pm*
 
%changelog
* Mon May 12 2025 Kanishk Bansal <kanbansal@microsoft.com> - 2.008002-2
- Initial Azure Linux import from Fedora 43 (license: MIT)
- License verified

* Mon May 05 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.008002-1
- 2.008002 bump (rhbz#2357958)
 
* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.006000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
 
* Tue Oct 01 2024 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.006000-1
- Update to 2.006000.
- Reflect perl(Reply::Plugin) having been added to Fedora.
- Remove references to perl-Type-Tie.
 
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.004000-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild
 
* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.004000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.004000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.004000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Mon Apr 24 2023 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.004000-1
- Update to 2.004000.
 
* Mon Jan 30 2023 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.002001-1
- Update to 2.002001.
 
* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.002000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Wed Jan 04 2023 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.002000-1
- Update to 2.002000.
 
* Sat Nov 19 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.000001-3
- Don't BR: perl(Type::Tiny::XS) if bootstrapping.
 
* Wed Nov 16 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.000001-2
- Add perl(Type::Tiny::XS)
 
* Tue Oct 04 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.000001-1
- Update to 2.000001.
 
* Mon Sep 12 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.016010-1
- Update to 1.016010.
 
* Mon Aug 22 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.016008-2
- Re-add BR: perl(Data::Constraint).
 
* Thu Aug 18 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.016008-1
- Update to 1.016008.
 
* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.014000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Mon Jul 11 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.014000-1
- Update to 1.014000.
 
* Fri Jul 01 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.012005-3
- Add BR: perl(MouseX::Types::Common).
- Address BR-cycle (RHBZ#2096309#c2).
 
* Mon Jun 13 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.012005-2
- Add and comment out BR: perl(Data::Constraint),
  BR: perl(MooseX::Types::DBIx::Class), BR: perl(Types::ReadOnly)
 
* Mon Jun 13 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.012005-1
- Upstream update to 1.012005.
- Add BR: perl(MooX::TypeTiny).
 
* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.012004-4
- Perl 5.36 re-rebuild of bootstrapped packages
 
* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.012004-3
- Perl 5.36 rebuild
 
* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.012004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Mon Sep 13 2021 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.012004-1
- Update to 1.012004.
 
* Sun Sep 12 2021 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.012003-1
- Cleanup Jitka's broken git-merger.
- Update to 1.012003.
 
* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.012001-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.012001-3
- Perl 5.34 re-rebuild of bootstrapped packages
 
* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.012001-2
- Perl 5.34 rebuild
 
* Tue Apr 27 2021 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.012001-1
- Update to 1.012001.
- Add BR: perl(Devel::Refcount).
 
* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.010006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Thu Sep 17 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.010006-1
- Update to 1.010006.
 
* Thu Sep 17 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.010005-1
- Update to 1.010005.
 
* Fri Aug 21 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.010004-1
- Update to 1.010004.
- Add BR:  perl(match::simple).
 
* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.010002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.010002-3
- Perl 5.32 re-rebuild of bootstrapped packages
 
* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.010002-2
- Perl 5.32 rebuild
 
* Wed May 06 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.010002-1
- Update to 1.010002.
 
* Thu Mar 26 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.010001-1
- Update to 1.010001.
 
* Thu Mar 05 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.010000-1
- Update to 1.010000.
 
* Wed Feb 12 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.008005-1
- Update to 1.008005.
 
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.008003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Fri Jan 17 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.008003-1
- Update to 1.008003.
 
* Tue Jan 14 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.008002-1
- Update to 1.008002.
- Add BR: perl(Specio), perl(Specio::Library::Builtins,
  perl(Test::Memory::Cycle).
 
* Thu Dec 19 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.008000-1
- Update to 1.008000.
 
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.004004-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.004004-4
- Perl 5.30 re-rebuild of bootstrapped packages
 
* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.004004-3
- Perl 5.30 rebuild
 
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.004004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Fri Jan 11 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.004004-1
- Update to 1.004004.
 
* Tue Aug 07 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.004002-1
- Update to 1.004002.
- Add BR: perl(IO::String).
- Add and comment out BR: perl(MouseX::Types::Common).
 
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.002002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
 
* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.002002-3
- Perl 5.28 re-rebuild of bootstrapped packages
 
* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.002002-2
- Perl 5.28 rebuild
 
* Mon May 21 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.002002-1
- Update to 1.002002.
- Add BR: perl(Ref::Util::XS).
 
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.002001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.002001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
 
* Wed Jun 21 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.002001-1
- Update to 1.002001.
 
* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.002000-2
- Perl 5.26 re-rebuild of bootstrapped packages
 
* Wed Jun 07 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.002000-1
- Update to 1.002000.
 
* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.000006-7
- Perl 5.26 rebuild
 
* Mon Mar 20 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000006-6
- Don't BR: perl(Return::Type), perl(Types::Path::Tiny) if perl_bootstrapping
  (From ppisar@redhat.com, RHBZ#1433344)
 
* Mon Feb 13 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000006-5
- Add further optional part of testsuites: BR: perl(Validation::Class),
  perl(Validation::Class::Simple).
 
* Fri Feb 10 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000006-4
- Add further optional part of testsuite: BR: perl(Return::Type).
 
* Thu Feb 09 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000006-3
- Add further optional part of testsuite: BR: perl(Type::Tie).
 
* Thu Feb 09 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000006-2
- Add more optional parts of testsuite:
  - BR: perl(Sub::Exporter::Lexical).
  - BR: perl(Types::Path::Tiny).
 
* Thu Feb 02 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000006-1
- Update to 1.000006.
- Add BuildRequires: perl(Function::Parameters)
 
* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.000005-7
- Perl 5.24 rebuild
 
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.000005-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
 
* Fri Jan 29 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000005-5
- Modernize spec.
- Add COPYRIGHT to %%license.
* Tue Jul 21 2015 Petr Pisar <ppisar@redhat.com> - 1.000005-4
- Specify all dependencies (bug #1245096)
 
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
 
* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.000005-2
- Perl 5.22 rebuild
 
* Mon Oct 27 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000005-1
- Upstream update.
 
* Thu Sep 04 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.000004-2
- Perl 5.20 rebuild
 
* Thu Sep 04 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000004-1
- Upstream update.
 
* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.000003-2
- Perl 5.20 rebuild
 
* Sun Aug 31 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000003-1
- Upstream update.
 
* Fri Aug 22 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000002-1
- Upstream update.
- Update deps.
 
* Mon Aug 18 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.000000-1
- Upstream update.
 
* Thu Jul 24 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.046-1
- Upstream update.
 
* Mon Jun 23 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.044-1
- Upstream update.
- Spec file cosmetics.
- BR: perl(Test::Moose), perl(MooseX::Getopt).
 
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.042-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
 
* Tue Apr 08 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.042-1
- Upstream update.
- Split out perl(Test::TypeTiny) to avoid deps on perl(Test::*).
 
* Fri Mar 21 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.040-1
- Initial Fedora package.
