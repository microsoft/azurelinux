Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-PAR-Dist
Version:        0.51
Release:        2%{?dist}
Summary:        Toolkit for creating and manipulating Perl PAR distributions
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/PAR-Dist
Source0:        https://cpan.metacpan.org/authors/id/R/RS/RSCHUPP/PAR-Dist-%{version}.tar.gz#/perl-PAR-Dist-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(Archive::Zip)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
# perl(ExtUtils::Install) not tested
BuildRequires:  perl(ExtUtils::MY)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
# perl(LWP::Simple) not tested
# perl(Module::Signature) >= 0.25 not tested
BuildRequires:  perl(YAML::Tiny)
# Tests:
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Archive::Zip)
Requires:       perl(Cwd)
Requires:       perl(ExtUtils::Install)
Requires:       perl(ExtUtils::MY)
Requires:       perl(File::Copy)
Requires:       perl(File::Find)
Requires:       perl(File::Path)
Requires:       perl(LWP::Simple)
Requires:       perl(Module::Signature) >= 0.25
Requires:       perl(YAML::Tiny)

%description
This module creates and manipulates PAR distributions. They are architecture-
specific PAR files, containing everything under blib/ of CPAN distributions
after their make or Build stage, a META.yml describing metadata of the
original CPAN distribution, and a MANIFEST detailing all files within it.
Digitally signed PAR distributions will also contain a SIGNATURE file.

%prep
%setup -q -n PAR-Dist-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test PERL_TEST_POD=1

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.51-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Dec 01 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.51-1
- 0.51 bump

* Wed Nov 18 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-1
- 0.50 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-18
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-15
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-12
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-10
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-7
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.49-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 24 2012 Petr Pisar <ppisar@redhat.com> - 0.49-1
- 0.49 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.47-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.47-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Steven Pritchard <steve@kspei.com> 0.47-1
- Update to 0.47.

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.46-4
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.46-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.46-2
- rebuild against perl 5.10.1

* Mon Sep 21 2009 Stepan Kasal <skasal@redhat.com> - 0.46-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Steven Pritchard <steve@kspei.com> 0.43-1
- Update to 0.43.
- Explicitly require Archive::Zip and YAML::Tiny.

* Fri Jan 16 2009 Steven Pritchard <steve@kspei.com> 0.42-1
- Update to 0.42.

* Mon Dec 15 2008 Steven Pritchard <steve@kspei.com> 0.40-1
- Update to 0.40.
- BR Archive::Zip and YAML::Tiny for t/03merge_meta.

* Thu Sep 25 2008 Marcela Maslanova <mmaslano@redhat.com> 0.34-2
- forgot apply source

* Thu Sep 25 2008 Marcela Maslanova <mmaslano@redhat.com> 0.34-1
- update to 0.34 -> it was needed for perl-PAR

* Sat May 31 2008 Steven Pritchard <steve@kspei.com> 0.31-1
- Update to 0.31.
- BR Test::Pod and Test::Pod::Coverage.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.29-2
- Rebuild for perl 5.10 (again)

* Thu Feb 21 2008 Steven Pritchard <steve@kspei.com> 0.29-1
- Update to 0.29.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to match cpanspec output.

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com>  - 0.25-4
- rebuild (again) for new perl

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com>  - 0.25-3
- rebuild for new perl

* Mon Aug  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.25-2
- License: GPL+ or Artistic

* Mon Jul 30 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.25-1
- 0.25.

* Sun Jul 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.24-1
- 0.24.

* Mon Jun 25 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.23-1
- 0.23.

* Sun May  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.22-1
- 0.22.

* Tue Apr 17 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.21-2
- BuildRequire perl(ExtUtils::MakeMaker) and perl(Test::More).

* Sun Oct 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.21-1
- 0.21.

* Thu Oct 12 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.20-1
- 0.20.

* Sun Sep 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.19-1
- 0.19.

* Mon Aug 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.18-1
- 0.18.

* Tue Aug 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.16-1
- 0.16.

* Sat Jul 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.15-1
- 0.15.

* Sun Jul 23 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.14-1
- 0.14.

* Thu Jul 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.11-1
- 0.11.
- Fix order of options to find(1) in %%install.

* Thu Jun  8 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.10-1
- 0.10.

* Fri Feb 24 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.08-1
- 0.08.
- Specfile cleanups.

* Thu Mar 17 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.07-3
- Avoid running signature test during build.
- Sync with fedora-rpmdevtools' Perl spec template.

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.07-0.fdr.2
- Require perl(:MODULE_COMPAT_*).

* Sat Mar 27 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.07-0.fdr.1
- First build.
