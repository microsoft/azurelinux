Summary:        SASL Authentication framework for Perl
Name:           perl-Authen-SASL
Version:        2.16
Release:        22%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Authen-SASL
Source0:        https://cpan.metacpan.org/authors/id/G/GB/GBARR/Authen-SASL-%{version}.tar.gz#/perl-Authen-SASL-%{version}.tar.gz
Source1:        LICENSE.PTR
# Update the function WRITE to properly handle string which is shorter than
# provided length
Patch0:         Authen-SASL-RT85294-Fix-WRITE.patch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  sed
BuildRequires:  perl(Carp)
BuildRequires:  perl(Digest::HMAC_MD5)
BuildRequires:  perl(Digest::MD5)
# Tests
BuildRequires:  perl(FindBin)
BuildRequires:  perl(GSSAPI)
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl(Module::Install::Makefile)
BuildRequires:  perl(Module::Install::Metadata)
BuildRequires:  perl(Module::Install::WriteAll)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Handle)
# Run-time
BuildRequires:  perl(bytes)
BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildArch:      noarch

%description
SASL is a generic mechanism for authentication used by several network
protocols. Authen::SASL provides an implementation framework that all
protocols should be able to share.

%prep
%setup -q -n Authen-SASL-%{version}
%patch0 -p1

# Remove bundled libraries
rm -r inc
sed -i -e '/^inc\// d' MANIFEST

chmod -c a-x example_pl

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}

cp %{SOURCE1} .

%check
make test

%files
%license LICENSE.PTR
%doc api.txt Changes example_pl
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Nov 8 2022 Aadhar Agarwal <aadagarwal@microsoft.com> - 2.16-22
- Moved from extended to core.

* Thu Jan 13 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.16-21
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.16-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-17
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-14
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-11
- Perl 5.26 rebuild

* Mon May 15 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-10
- Fix building on Perl without '.' in @INC
- Modernize spec and unbundled 'inc'

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-8
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-5
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-2
- Fixed SASL and GSSAPI error (RT#85294)

* Tue Oct  1 2013 Paul Howarth <paul@city-fan.org> - 2.16-1
- Update to 2.16
  - SASL.pod: fix typo
  - Perl.pm: avoid warning on "uninitialized value"
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.15-10
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Jitka Plesnikova <jplesnik@redhat.com> - 2.15-8
- Specify all dependencies
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 2.15-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.15-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.15-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun Dec 12 2010 Steven Pritchard <steve@kspei.com> 2.15-1
- Update to 2.15.
- Add example_pl to docs.

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.13-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.13-2
- rebuild against perl 5.10.1

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 2.13-1
- new upstream version, BR Test::More

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 01 2008 Steven Pritchard <steve@kspei.com> 2.12-1
- Update to 2.12.

* Thu May 15 2008 Steven Pritchard <steve@kspei.com> 2.11-1
- Update to 2.11.
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to resemble cpanspec output.
- Drop explicit perl build dependency.

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10-2
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat Apr 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.10-1
- Update to 2.10.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-4
- Rebuild for FC5 (perl 5.8.8).

* Sat May 14 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-3
- Add dist tag.

* Tue Apr 26 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-2
- Update to 2.09.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Apr  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.08-1
- Drop Epoch: 0 and 0.fdr release prefix.

* Wed Jul 21 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.08-0.fdr.1
- Update to 2.08.
- Bring up to date with current fedora.us Perl spec template.

* Fri Jan 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.06-0.fdr.1
- First build.
