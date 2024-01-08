%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(XML::Parser\\)$

# Optional tests, disabled due to missing dependencies.
%bcond_with perl_XML_XPath_enables_optional_test

Summary:        XPath parser and evaluator for Perl
Name:           perl-XML-XPath
Version:        1.48
Release:        1%{?dist}
# XML/XPath.pm, XML/XPath/PerlSAX.pm, REAME: GPL+ or Artistic
# Others: Artistic 2.0
License:        Artistic 2.0 AND (GPL+ OR Artistic)
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/XML-XPath
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MANWAR/XML-XPath-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(IO::File)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(XML::Parser) >= 2.23
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)

%if %{with_check}
BuildRequires:  perl(App::cpanminus)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(lib)
BuildRequires:  perl(open)
BuildRequires:  perl(utf8)
# Optional tests
%if %{with perl_XML_XPath_enables_optional_test}
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(Test::CPAN::Meta)
BuildRequires:  perl(Test::CPAN::Meta::JSON)
%endif
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(POSIX)
Requires:       perl(XML::Parser) >= 2.23
Requires:       perl(warnings)

%description
This module aims to comply exactly to the XPath specification at
http://www.w3.org/TR/xpath and yet allow extensions to be added in the
form of functions. Modules such as XSLT and XPointer may need to do
this as they support functionality beyond XPath.

%prep
%setup -q -n XML-XPath-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
%_fixperms %{buildroot}/*

mkdir -p %{buildroot}/%{_mandir}/man1/
cat >> %{buildroot}/%{_mandir}/man1/xpath.1 << EOF
.so man3/XML::XPath.3pm
EOF

%check
cpanm Path::Tiny
make test

%files
%license LICENSE
%doc Changes README TODO
%{_bindir}/xpath
%{perl_vendorlib}/XML
%{_mandir}/man1/xpath*
%{_mandir}/man3/*.3*

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.48-1
- Auto-upgrade to 1.48 - Azure Linux 3.0 - package upgrades

* Wed Jul 20 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.44-13
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-10
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 15 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-8
- Do not run optional test on RHEL

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-6
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 15 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-1
- 1.44 bump

* Thu Oct 11 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.43-1
- 1.43 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jul 31 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-1
- 1.42 bump

* Fri Jul 28 2017 Petr Pisar <ppisar@redhat.com> - 1.41-1
- 1.41 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.40-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.40-1
- 1.40 bump

* Wed Nov 09 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.39-1
- 1.39 bump

* Mon Oct 31 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.38-1
- 1.38 bump

* Thu Jun 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.37-1
- 1.37 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.36-2
- Perl 5.24 rebuild

* Thu Apr 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.36-1
- 1.36 bump

* Mon Apr 11 2016 Petr Pisar <ppisar@redhat.com> - 1.35-1
- 1.35 bump

* Fri Apr 08 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-2
- Add BR perl(CPAN::Meta) (BZ#1325123)

* Wed Mar 09 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-1
- 1.34 bump

* Mon Mar 07 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-1
- 1.33 bump

* Wed Feb 24 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.32-1
- 1.32 bump

* Mon Feb 22 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-1
- 1.31 bump

* Mon Feb 08 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-1
- 1.30 bump

* Thu Feb 04 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-1
- 1.29 bump

* Mon Feb 01 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-1
- 1.28 bump

* Tue Jan 26 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-1
- 1.26 bump

* Thu Jan 21 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-1
- 1.25 bump

* Wed Jan 20 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-1
- 1.24 bump

* Wed Jan 13 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-1
- 1.22 bump

* Tue Jan 12 2016 Petr Pisar <ppisar@redhat.com> - 1.21-1
- 1.21 bump

* Mon Jan 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-1
- 1.20 bump

* Fri Jan 08 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-1
- 1.19 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-27
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-26
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1.13-23
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.13-21
- revert the patch. It breaks backward compatibility for some apps. 
- the xpath has still man page installed.

* Fri Aug 24 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-20
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 1.13-18
- Perl 5.16 rebuild

* Fri Mar 16 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.13-17
- 680418 - missing man page for xpath
- applied debian patch, which added POD into xpath code, but also fix debian bug(#185292)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.13-15
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.13-13
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.13-12
- Mass rebuild with perl-5.12.0

* Thu Dec 10 2009 Marcela Maslanova <mmaslano@redhat.com> - 1.13-11
- 541668 fix requires for review

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.13-10
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 2  2008 Marcela Maslanova <mmaslano@redhat.com> - 1.13-7
- rebuild and remove ||: from check part

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-6
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.13-5
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.13-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.13-4
- bump for mass rebuild

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Jul 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.13-2
- Bring up to date with current fedora.us Perl spec template.

* Sun Oct 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.13-0.fdr.1
- First build.
