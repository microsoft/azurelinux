Name:           perl-MIME-Lite
Version:        3.033
Release:        11%{?dist}
Summary:        MIME::Lite - low-calorie MIME generator
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/MIME-Lite
Source0:        https://cpan.metacpan.org/authors/id/R/RJ/RJBS/MIME-Lite-%{version}.tar.gz
BuildArch:      noarch
BuildRequires: make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Email::Date::Format)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(lib)
BuildRequires:  perl(Mail::Address)
BuildRequires:  perl(MIME::Types) >= 1.28
BuildRequires:  perl(Net::SMTP)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# not detected by automated find-requires:
Requires:       perl(Email::Date::Format)
Requires:       perl(MIME::Types) >= 1.28

%{?perl_default_filter}

%description
MIME::Lite is intended as a simple, standalone module for generating (not 
parsing!) MIME messages... Specifically, it allows you to output a simple,
decent single- or multi-part message with text or binary attachments.  It does
not require that you have the Mail:: or MIME:: modules installed.

%prep
%setup -q -n MIME-Lite-%{version}
sed -i 's/\r//' examples/*
sed -i 's/\r//' contrib/*
sed -i 's/\r//' COPYING README
chmod a-x examples/* contrib/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +

%check
make test

%files
%doc changes.pod README examples contrib COPYING LICENSE
%exclude %{perl_vendorlib}/MIME/changes.pod
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.033-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.033-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.033-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.033-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 27 2023 Michal Josef Špaček <mspacek@redhat.com> - 3.033-7
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.033-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.033-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.033-4
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.033-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 14 2021 Jan Pazdziora <jpazdziora@redhat.com> - 3.033-1
- 1971173 - Rebase to upstream version 3.033.

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.031-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.031-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.031-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.031-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.031-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Jan Pazdziora <jpazdziora@redhat.com> - 3.031-1
- 1765833 - Rebase to upstream version 3.031.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.030-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.030-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.030-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.030-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.030-12
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.030-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.030-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.030-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.030-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.030-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.030-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.030-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.030-4
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.030-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.030-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 04 2013 Petr Šabata <contyk@redhat.com> - 3.030-1
- 3.030 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.029-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 3.029-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.029-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Petr Šabata <contyk@redhat.com> - 3.029-2
- Filter out doc file dependencies
- Modernize the spec a bit

* Wed Aug 22 2012 Petr Šabata <contyk@redhat.com> - 3.029-1
- 3.029 bump
- Fix deps, drop command macros
- Correct line-endings and file permissions

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.028-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 3.028-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.028-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Petr Sabata <contyk@redhat.com> - 3.028-1
- 3.028 bump
- Remove now obsolete BuildRoot and defattr

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.027-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.027-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.027-5
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.027-4
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Marcela Mašláňová <mmaslano@redhat.com> - 3.027-3
- make rpmlint happy 

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.027-2
- rebuild against perl 5.10.1

* Mon Nov  2 2009 Stepan Kasal <skasal@redhat.com> - 3.027-1
- new upstream version

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 3.26-2
- no need to search for *.bs files in noarch rpm

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 3.26-1
- new upstream version
- fix buildrequires
- add requires not detected automatically

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.01-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.01-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep  5 2008 Paul Howarth <paul@city-fan.org> 3.01-7
- fix FTBFS (#449558)

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.01-6
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.01-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Sep 10 2006 Mike McGrath <imlinux@gmail.com> 3.01-5
- Rebuild

* Thu Mar 30 2006 Mike McGrath <imlinux@gmail.com> 3.01-4
- New maintainer

* Thu Jun 23 2005 Ralf Corsepius <ralf@links2linux.de> 3.01-3
- Add %%{dist}.

* Wed Apr 06 2005 Hunter Matthews <thm@duke.edu> 3.01-2
- Review suggestions from José Pedro Oliveira

* Fri Mar 18 2005 Hunter Matthews <thm@duke.edu> 3.01-1
- Initial packageing.
