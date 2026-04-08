# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Test-Pod
Version:        1.52
Release:        23%{?dist}
Summary:        Test POD files for correctness
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Test-Pod
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/Test-Pod-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(warnings)
BuildRequires:  perl(strict)
# Run-time
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Pod::Simple) >= 3.05
BuildRequires:  perl(Test::Builder)
# Tests
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Builder::Tester) >= 1.02
BuildRequires:  perl(Test::More) >= 0.62
Requires:       perl(File::Find)
Requires:       perl(Pod::Simple) >= 3.05
Requires:       perl(Test::More) >= 0.62

# Remove under-specified dependcies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Pod::Simple\\)$
# Remove Test::Pod dependecy from *tests package
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
Check POD files for errors or warnings in a test file, using Pod::Simple to do
the heavy lifting.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Test-Pod-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cp -a lib %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
LC_ALL=C make test

%files
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Pod.3pm*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 18 2024 Michal Josef Špaček <mspacek@redhat.com> - 1.52-21
- Package tests

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.52-14
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.52-11
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.52-8
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.52-5
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.52-2
- Perl 5.28 rebuild

* Fri Apr 20 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.52-1
- 1.52 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.51-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.51-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.51-6
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.51-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.51-4
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.51-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 07 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.51-2
- Updated dependencies

* Mon Jul  6 2015 Tom Callaway <spot@fedoraproject.org> - 1.51-1
- update to 1.51

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.50-2
- Perl 5.22 rebuild

* Mon Jun 01 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.50-1
- 1.50 bump

* Thu May 14 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.49-1
- 1.49 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.48-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 17 2014 Petr Pisar <ppisar@redhat.com> - 1.48-5
- Declare run-time dependency on File::Find (bug #1066006)

* Thu Feb 13 2014 Petr Pisar <ppisar@redhat.com> - 1.48-4
- Clarify license (bug #1064447)
- Remove run-time dependency on Test::Builder::Tester (bug #1064743)
- Remove under-specified dependencies

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.48-2
- Perl 5.18 rebuild

* Mon May 06 2013 Petr Šabata <contyk@redhat.com> - 1.48-1
- 1.48 bump, Pod::Simple compatibility enhancements

* Mon Feb 18 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-1
- 1.46 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.45-5
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 1.45-4
- Round Module::Build version to 2 digits

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.45-2
- Perl mass rebuild

* Thu Mar 10 2011 Petr Sabata <psabata@redhat.com> - 1.45-1
- 1.45 bump
- Buildroot garbage cleanup

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Karsten Hopp <karsten@redhat.com> 1.44-3
- bump release and rebuild to fix dependency issues on s390x

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.44-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Jul 31 2010 Paul Howarth <paul@city-fan.org> - 1.44-1
- update to 1.44:
  - use Module::Build::Compat's "traditional" configuration
  - loosen version requirements for Test::More and Pod::Simple
  - add File::Spec to the list of prereqs
- drop perl(Test::More) version requirement to 0.62
- drop perl(Pod::Simple) version requirement to 3.05

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.42-2
- Mass rebuild with perl-5.12.0

* Thu Mar 11 2010 Paul Howarth <paul@city-fan.org> - 1.42-1
- update to 1.42
- new upstream maintainer
- use Module::Build flow
- include README
- use less generic %%description and %%summary
- use _fixperms macro instead of our own chmod incantation
- bump Test::More build requirement to 0.70
- add versioned requires for Pod::Simple, Test::Builder::Tester and Test::More

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.40-2
- rebuild against perl 5.10.1

* Fri Oct 30 2009 Stepan Kasal <skasal@redhat.com> - 1.40-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-6
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-5
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.26-4
- rebuild for perl 5.10 (again)

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.26-3
- rebuild for new perl

* Thu Dec 20 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.26-2
- license tag fix

* Fri Jul 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.26-1
- Update to 1.26.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.24-2
- Rebuild for FC5 (perl 5.8.8).

* Fri Feb  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.24-1
- Update to 1.24.

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.22-1
- Update to 1.22.

* Thu May 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-3
- Add dist tag.

* Thu May 12 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.20-2
- rebuilt

* Thu Jun 24 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.20-0.fdr.1
- Update to 1.20.

* Wed May 12 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.16-0.fdr.2
- Avoid creation of the perllocal.pod file (make pure_install).

* Mon May  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.16-0.fdr.1
- Update to 1.16, dir handling patch applied upstream.

* Fri Apr 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.14-0.fdr.1
- Update to 1.14.
- Require perl(:MODULE_COMPAT_*).
- Add patch to avoid warnings from all_pod_files().

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.12-0.fdr.1
- Update to 1.12.

* Thu Jan 22 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.08-0.fdr.1
- Update to 1.08.
- Use %%{perl_vendorlib}.

* Wed Nov  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-0.fdr.1
- First build.
