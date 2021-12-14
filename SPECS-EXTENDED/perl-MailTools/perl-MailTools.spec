Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:	Various ancient mail-related perl modules
Name:		perl-MailTools
Version:	2.21
Release:	5%{?dist}
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/MailTools
Source0:	https://cpan.metacpan.org/authors/id/M/MA/MARKOV/MailTools-%{version}.tar.gz#/perl-MailTools-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	sed
# Module Runtime
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(Date::Format)
BuildRequires:	perl(Date::Parse)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(Net::Domain) >= 1.05
BuildRequires:	perl(Net::NNTP)
BuildRequires:	perl(Net::SMTP) >= 1.03
BuildRequires:	perl(Net::SMTP::SSL)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
# Test Suite
BuildRequires:	perl(Test::More)
BuildRequires:	perl(warnings)
# Extra Tests
BuildRequires:	perl(Test::Pod)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Net::Domain) >= 1.05
Requires:	perl(Net::NNTP)

%description
MailTools is a set of ancient Perl modules related to mail applications.

%prep
%setup -q -n MailTools-%{version}

# Set up example scripts
cd examples
for file in *.PL; do
	perl $file
done
chmod -c -x *_demo
# Remove example-generation scripts, no longer needed
rm *.PL
cd -
sed -i -e '/^examples\/.*\.PL/d' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
make test TEST_FILES="xt/*.t"

%files
%doc ChangeLog README* examples/
%dir %{perl_vendorlib}/Mail/
%dir %{perl_vendorlib}/Mail/Field/
%dir %{perl_vendorlib}/Mail/Mailer/
%doc %{perl_vendorlib}/Mail/Address.pod
%doc %{perl_vendorlib}/Mail/Cap.pod
%doc %{perl_vendorlib}/Mail/Field.pod
%doc %{perl_vendorlib}/Mail/Field/AddrList.pod
%doc %{perl_vendorlib}/Mail/Field/Date.pod
%doc %{perl_vendorlib}/Mail/Field/Generic.pod
%doc %{perl_vendorlib}/Mail/Filter.pod
%doc %{perl_vendorlib}/Mail/Header.pod
%doc %{perl_vendorlib}/Mail/Internet.pod
%doc %{perl_vendorlib}/Mail/Mailer.pod
%doc %{perl_vendorlib}/Mail/Send.pod
%doc %{perl_vendorlib}/Mail/Util.pod
%doc %{perl_vendorlib}/MailTools.pod
%{perl_vendorlib}/Mail/Address.pm
%{perl_vendorlib}/Mail/Cap.pm
%{perl_vendorlib}/Mail/Filter.pm
%{perl_vendorlib}/Mail/Header.pm
%{perl_vendorlib}/Mail/Internet.pm
%{perl_vendorlib}/Mail/Field.pm
%{perl_vendorlib}/Mail/Mailer.pm
%{perl_vendorlib}/Mail/Send.pm
%{perl_vendorlib}/Mail/Util.pm
%{perl_vendorlib}/Mail/Field/AddrList.pm
%{perl_vendorlib}/Mail/Field/Date.pm
%{perl_vendorlib}/Mail/Field/Generic.pm
%{perl_vendorlib}/Mail/Mailer/qmail.pm
%{perl_vendorlib}/Mail/Mailer/rfc822.pm
%{perl_vendorlib}/Mail/Mailer/sendmail.pm
%{perl_vendorlib}/Mail/Mailer/smtp.pm
%{perl_vendorlib}/Mail/Mailer/smtps.pm
%{perl_vendorlib}/Mail/Mailer/testfile.pm
%{perl_vendorlib}/MailTools.pm
%{_mandir}/man3/Mail::Address.3*
%{_mandir}/man3/Mail::Cap.3*
%{_mandir}/man3/Mail::Field.3*
%{_mandir}/man3/Mail::Field::AddrList.3*
%{_mandir}/man3/Mail::Field::Date.3*
%{_mandir}/man3/Mail::Field::Generic.3*
%{_mandir}/man3/Mail::Filter.3*
%{_mandir}/man3/Mail::Header.3*
%{_mandir}/man3/Mail::Internet.3*
%{_mandir}/man3/Mail::Mailer.3*
%{_mandir}/man3/Mail::Send.3*
%{_mandir}/man3/Mail::Util.3*
%{_mandir}/man3/MailTools.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.21-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.21-2
- Perl 5.30 rebuild

* Tue May 21 2019 Paul Howarth <paul@city-fan.org> - 2.21-1
- Update to 2.21
  - Fix metadata
  - Add more to the README
  - Add Mail::Mailer option StartSSL for smtp backend (CPAN RT#125871)
  - Deprecate Mail::Mailer backend smtps
  - Document need for escaping docs for Mail::Send (CPAN RT#129627)
  - Document limit on parameters for Mail::Send::new() (CPAN RT#129633)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Paul Howarth <paul@city-fan.org> - 2.20-1
- Update to 2.20
  - Rewrite doc syntax to my current standard style
  - Text corrections (CPAN RT#123823, CPAN RT#123824)
  - Convert to git
  - Move to GitHub

* Wed Aug 23 2017 Paul Howarth <paul@city-fan.org> - 2.19-1
- Update to 2.19
  - Block namespace MailTools (CPAN RT#120905)
- Add "ancient" to %%summary and %%description
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.18-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 19 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.18-2
- Perl 5.24 re-rebuild of bootstrapped packages

* Thu May 19 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.18-1
- Update to 2.18
  - Mail::Header should accept \r in empty line which ends the
    header (CPAN RT#114382)

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.17-2
- Perl 5.24 rebuild

* Thu May 12 2016 Paul Howarth <paul@city-fan.org> - 2.17-1
- Update to 2.17
  - Mail::Header should only accept totally empty lines as header terminator,
    not to break MIME::Tools regression tests (CPAN RT#113918)

* Tue Apr 19 2016 Paul Howarth <paul@city-fan.org> - 2.16-1
- Update to 2.16
  - Mail::Header continues reading after wrongly folded line (CPAN RT#113464)
  - Mail::Mailer::open call of exec() explained
  - Fix example in Mail::Address
  - Fix Mail::Header file parsing regression in 2.15 (CPAN RT#113874)
- Simplify find command using -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.14-2
- Perl 5.22 rebuild

* Fri Nov 21 2014 Paul Howarth <paul@city-fan.org> - 2.14-1
- Update to 2.14
  - Fix threads and Mail::Field initiation (CPAN RT#99153)
  - Warn when loading of some Mail::Field::* fails
- Classify buildreqs by usage
- Silence warnings from MakeMaker about files we delete in %%prep

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.13-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan  6 2014 Paul Howarth <paul@city-fan.org> 2.13-1
- Update to 2.13
  - Optional 'from' and 'on' component in in-reply-to are comments
    (CPAN RT#89371)
  - mailcap \\\\ -> \\ (CPAN RT#89802)
  - Fix typos (CPAN RT#87188)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.12-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Paul Howarth <paul@city-fan.org> 2.12-1
- Update to 2.12
  - Default for Mail::Header::new(Modify) is 'false', not 'true'
    (CPAN RT#79985)
  - Mail::Address take username with rindex(), a bit better than index() but
    still poor (CPAN RT#82056)
  - Check for bad folding of header lines (CPAN RT#79993)
  - Add a note about better to avoid Mail::Address->name() (CPAN RT#81459)
- Drop UTF8 patch, no longer needed

* Wed Aug 29 2012 Paul Howarth <paul@city-fan.org> 2.11-1
- Update to 2.11
  - Fix typo in Mail::Mailer::smtp, which only shows up in Perl > 5.14

* Tue Aug 28 2012 Paul Howarth <paul@city-fan.org> 2.10-1
- Update to 2.10
  - Mail::Mailer::smtp set from address twice (CPAN RT#77161)
  - Mail::Mailer::smtps did not support the From option (CPAN RT#77161)
  - Mail::Util::mailaddress has now an optional parameter to set the returned
    value explicitly (CPAN #75975)
- BR: perl(base)
- Drop BR: perl(Config) and perl(POSIX), not dual-lived
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.09-2
- Perl 5.16 rebuild

* Sat Feb 25 2012 Paul Howarth <paul@city-fan.org> - 2.09-1
- Update to 2.09
  - Remove dependency to Test::Pod by moving 99pod.t from t/ to xt/
    (CPAN RT#69918)
- BR: perl(Net::Domain) ≥ 1.05 and perl(Net::SMTP) ≥ 1.03
- Explicitly run xt/ tests

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 2.08-3
- Use DESTDIR rather than PERL_INSTALL_ROOT
- One buildreq per line for readability
- Add buildreqs for core perl modules, which might be dual-lived

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.08-2
- Perl mass rebuild

* Wed Jun  1 2011 Paul Howarth <paul@city-fan.org> - 2.08-1
- Update to 2.08 (#709697)
  - Respect errors on closing a Mail::Mailer::smtp/::smtps connection
  - Mail::Internet should accept Net::SMTP::SSL as well (CPAN RT#68590)
  - Document that Mail::Mailer::smtps needs Authen::SASL
- Use patch rather than iconv to convert docs to UTF8 encoding
- Nobody else likes macros for commands

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct  1 2010 Paul Howarth <paul@city-fan.org> 2.07-1
- Update to 2.07
  - Document perl 5.8.1 requirement in README (CPAN RT#61753)
  - Add "MAIL FROM" to Mail::Mailer::smtp

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.06-2
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Paul Howarth <paul@city-fan.org> 2.06-1
- Update to 2.06 (add support for smtps via Net::SMTP::SSL)
- Use %%{_fixperms} macro instead of our own chmod incantation

* Mon Dec 21 2009 Paul Howarth <paul@city-fan.org> 2.05-1
- Update to 2.05
  - Fix de-ref error when index out of range in Mail::Header::get()
  - Repair fixed selection of smtp for non-unix systems
  - Do not run pod.t in devel environment
  - Set default output filename for Mail::Mailer::testfile::PRINT
  - Warn when no mailers were found (CPAN RT#52901)
- Tidy up %%files list

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 2.04-4
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 30 2008 Paul Howarth <paul@city-fan.org> 2.04-1
- Update to 2.04

* Tue Apr 15 2008 Paul Howarth <paul@city-fan.org> 2.03-1
- Update to 2.03

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.02-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.02-2
- rebuild for new perl

* Mon Dec  3 2007 Paul Howarth <paul@city-fan.org> 2.02-1
- Update to 2.02
- Remove buildreqs perl(Net::SMTP) and perl(Net::Domain), bundled with perl
- Add buildreqs perl(Date::Format), perl(Date::Parse), perl(Test::More), and
  perl(Test::Pod)
- Remove patch for CPAN RT#20726, now fixed upstream
- Buildreq perl >= 5.8.1
- Tweak files list to mark pod files as %%doc
- Fix character encoding for ChangeLog

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 1.77-2
- Clarify license as GPL v1 or later, or Artistic (same as perl)
- Unexpand tabs in spec file

* Fri May 11 2007 Paul Howarth <paul@city-fan.org> 1.77-1
- Update to 1.77

* Tue Apr 10 2007 Paul Howarth <paul@city-fan.org> 1.76-1
- Update to 1.76
- Add comment text about the patch for fixing CPAN RT#20726
- BuildRequire perl(ExtUtils::MakeMaker) rather than perl-devel

* Thu Mar  8 2007 Paul Howarth <paul@city-fan.org> 1.74-4
- Buildrequire perl-devel for Fedora 7 onwards
- Fix argument order for find with -depth

* Wed Aug 30 2006 Paul Howarth <paul@city-fan.org> 1.74-3
- FE6 mass rebuild

* Fri Jul 28 2006 Paul Howarth <paul@city-fan.org> 1.74-2
- cosmetic spec file changes
- fix CPAN RT#20726 (RH #200450), allowing Mail::Util::read_mbox() to open
  files with weird names

* Wed Mar  1 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.74-1
- 1.74.

* Sun Jan 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.73-1
- 1.73.

* Wed Jan 18 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.72-1
- 1.72.

* Fri Jan  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.71-1
- 1.71.

* Wed Dec 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.67-2
- Fix demo scripts.
- Sync with fedora-rpmdevtools' perl spec template.

* Fri Jul  1 2005 Paul Howarth <paul@city-fan.org> - 1.67-1
- update to 1.67 (#161830)
- assume perl_vendorlib is set
- license is same as perl (GPL or Artistic) according to README
- don't include module name in summary
- use macros consistently
- add dist tag

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.66-2
- rebuilt

* Sat Jan 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.66-1
- Update to 1.66.

* Wed Aug 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.64-0.fdr.1
- Update to 1.64, patch applied upstream.
- Bring up to date with current fedora.us Perl spec template.

* Sat Mar 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.61-0.fdr.2
- Add patch to complete test.pm -> testfile.pm change introduced in 1.61.

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.61-0.fdr.1
- Update to 1.61.
- Reduce directory ownership bloat.
- Run tests in the %%check section.

* Thu Sep 25 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.60-0.fdr.1
- Update to 1.60.
- Install into vendor dirs.
- Spec cleanups.

* Sat Jul 12 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.5
- Package is now noarch

* Fri Jul 11 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.4
- Changed group tag
- Making test in build section

* Tue Jul  1 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.3
- Modified files section

* Tue Jun 17 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.2
- Added forgotten description
- Modified Summary according to Michael Schwendt suggestion
- Modified tarball permissions to 0644

* Sun Jun 15 2003 Dams <anvil[AT]livna.org>
- Initial build.
