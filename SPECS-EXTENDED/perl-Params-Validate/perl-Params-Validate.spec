Summary:        Params-Validate Perl module
Name:           perl-Params-Validate
Version:        1.31
Release:        9%{?dist}
# One file is GPL-1.0-or-later OR Artistic-1.0-Perl (c/ppport.h)
License:        Artistic-2.0 AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/release/Params-Validate
Source0:        https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Params-Validate-%{version}.tar.gz


BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(Module::Implementation) >= 0.04
BuildRequires:  perl(Module::Build) >= 0.4227

# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util) >= 1.20
BuildRequires:  perl(warnings)
BuildRequires:  perl(vars)
BuildRequires:  perl(XSLoader)

# Required by the tests
BuildRequires:  perl(base)
BuildRequires:  perl(Devel::Peek)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(JSON::PP) >= 2.27300
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(Test::Taint) >= 0.02
BuildRequires:  perl(Tie::Array)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(Readonly) >= 1.03

%description
The Params::Validate module allows you to validate method or function
call parameters to an arbitrary level of specificity. At the simplest
level, it is capable of validating the required parameters were given
and that no unspecified additional parameters were passed in. It is
also capable of determining that a parameter is of a specific type,
that it is an object of a certain class hierarchy, that it possesses
certain methods, or applying validation callbacks to arguments.

%prep
%setup -q -n Params-Validate-%{version}

%build
%{__perl} Build.PL installdirs=vendor optimize="$RPM_OPT_FLAGS"
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes TODO
%license LICENSE
%{perl_vendorarch}/Params
%{perl_vendorarch}/auto/Params
%{_mandir}/man3/*

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-8
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-4
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.31-2
- Convert license to SPDX.
- Remove empty installed *.bs.

* Sun Oct 23 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.31-1
- Upgrade to 1.31.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 19 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.30-1
- Upgrade to 1.30.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-13
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-10
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug  9 2018 Tom Callaway <spot@fedoraproject.org> - 1.29-8
- correct license tag (bz#1376845)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-6
- Perl 5.28 rebuild

* Fri Mar 02 2018 Petr Pisar <ppisar@redhat.com> - 1.29-5
- Adapt to removing GCC from a build root (bug #1547165)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.29-1
- Update to 1.29.
- Spec file cosmetics.

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-2
- Perl 5.26 rebuild

* Mon May 08 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.28-1
- Update to 1.28.

* Thu May 04 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.27-1
- Update to 1.27.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 09 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.26-1
- Update to 1.26.
- Reflect upstream having reverted to Module::Build, again ;)

* Fri Sep 30 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.25-1
- Update to 1.25.
- Reflect upstream having switched to ExtUtils::MakeMaker.
- Simplify spec.

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-2
- Perl 5.24 rebuild

* Mon May 09 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.24-1
- Upsteam update.

* Wed Mar 30 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.23-1
- Upstream update.

* Sun Feb 14 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.22-1
- Upstream update.
- Reflect changes to BRs.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.21-2
- Modernise spec.

* Sun Jul 26 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.21-1
- Upstream update.
- Reflect Attribute::Params::Validate having been dropped from
  Params::Validate.
- Add %%license.

* Mon Jul 13 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.20-1
- Upstream update.

* Fri Jun 26 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.19-1
- Upstream update.
- Remove BR:  perl(Test::Version).

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.18-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.18-2
- Perl 5.22 rebuild

* Tue Feb 24 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.18-1
- Upstream update.
- BR: perl(Test::Version).

* Sun Feb 01 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.17-1
- Upstream update.

* Mon Jan 12 2015 Petr Pisar <ppisar@redhat.com> - 1.16-2
- Remove unused test-time dependency on Readonly:::XS

* Thu Jan 08 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.16-1
- Upstream update.
- Reflect upstream changes.

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 30 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.13-1
- Upstream update.

* Sat Jun 28 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.12-1
- Upstream update.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.10-1
- Upstream update.

* Wed May 07 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.09-1
- Upstream update.

* Wed May 07 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.08-8
- Use aspell-en instead of hunspell.

* Tue May 06 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.08-7
- Add "'globals" to Params-Validate-1.08.diff (FTBFS RHBZ #1094169).
- Remove %%defattr.

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-6
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1.08-4
- Perl 5.18 rebuild

* Thu Jul 18 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.08-3
- Adjust license tag (RHBZ #977787).

* Thu Jul 18 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.08-2
- Add %%bcond --without release-tests.
- Skip release tests when bootstrapping (RHBZ #982253).

* Tue Jun 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.08-1
- Upstream update.
- Update patch.
- Update BRs.
- Add %%bcond --with network.
- Fix up %%changelog dates.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.07-1
- Upstream update.

* Tue Aug 14 2012 Petr Pisar <ppisar@redhat.com> - 1.06-5
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.06-3
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 1.06-2
- Round Module::Build version to 2 digits

* Mon Mar 19 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.06-1
- Upstream update.

* Thu Feb 09 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.05-1
- Upstream update.

* Mon Feb 06 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.01-1
- Upstream update.
- Drop Params-Validate-1.00-no-pod-coverage.patch.
- Spec file cleanup.

* Sun Jan 22 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.00-5
- Add %%{perl_default_filter}.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.00-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.00-2
- Perl mass rebuild

* Thu Jun 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.00-1
- Upstream update.
- Deactivate t/release-pod-coverage.t 
  (Add Params-Validate-1.00-no-pod-coverage.patch).

* Thu Jun 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.99-3
- Fix up bogus Tue Jun 28 2011 changelog entry.
- Fix License (Artistic2.0).
- Add BR: perl(Test::CPAN:Changes).

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.99-2
- Perl mass rebuild
- remove unneeded Pod::Man 

* Tue May 31 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.99-1
- Upstream update.
- Rebase patch (Params-Validate-0.99.diff).

* Sat Apr 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.98-1
- Upstream update.
- Spec cleanup.
- Rework BR's.
- Reflect upstream having abandoned AUTHOR_TESTING.
- Make spell-checking tests working/work-around aspell/hunspell/perl(Test::Spelling)
  issues (add Params-Validate-0.98.diff).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.95-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.95-2
- Mass rebuild with perl-5.12.0

* Wed Mar 03 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.95-1
- Upstream update.

* Tue Dec 15 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.94-1
- Upstream update.
- Reflect upstream having reworked author tests to using AUTHOR_TESTING=1.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.92-2
- rebuild against perl 5.10.1

* Mon Nov 23 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.92-1
- Upstream update.
- Switch to Build.PL.
- Disable IS_MAINTAINER test.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jun 10 2008 Ralf Corsépius <rc040203@freenet.de> - 0.91-1
- Upstream update.
- Conditionally activate IS_MAINTAINER tests.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.89-4
- Rebuild for perl 5.10 (again)

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 0.89-3
- Rebuild for gcc43.

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.89-2
- rebuild for new perl

* Tue Nov 13 2007 Ralf Corsépius <rc040203@freenet.de> - 0.89-1
- Upstream update.

* Thu Sep 06 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-3
- Update license tag.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-2
- Mass rebuild.

* Mon Mar 12 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-1
- BR: perl(ExtUtils::MakeMaker).
- Upstream update.

* Sat Jan 20 2007 Ralf Corsépius <rc040203@freenet.de> - 0.87-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.86-2
- Mass rebuild.

* Sun Aug 13 2006 Ralf Corsépius <rc040203@freenet.de> - 0.86-1
- Upstream update.

* Wed Jun 28 2006 Ralf Corsépius <rc040203@freenet.de> - 0.85-1
- Upstream update.

* Mon Jun 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.84-1
- Upstream update.

* Sun May 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.82-1
- Upstream update.

* Tue Apr 04 2006 Ralf Corsépius <rc040203@freenet.de> - 0.81-1
- Upstream update.

* Mon Feb 20 2006 Ralf Corsépius <rc040203@freenet.de> - 0.80-2
- Rebuild.

* Wed Feb 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.80-1
- Upstream update.

* Sat Jan 14 2006 Ralf Corsépius <rc040203@freenet.de> - 0.79-1
- Upstream update.
- BR perl(Readonly), perl(Readonly::XS).

* Sun Aug 14 2005 Ralf Corsepius <ralf@links2linux.de> - 0.78-2
- Spec file cleanup.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 0.78-1
- FE submission.
