Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Locale-Maketext-Gettext
Version:        1.30
Release:        3%{?dist}
Summary:        Joins the gettext and Maketext frameworks
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Locale-Maketext-Gettext
Source0:        https://cpan.metacpan.org/authors/id/I/IM/IMACAT/Locale-Maketext-Gettext-%{version}.tar.gz#/perl-Locale-Maketext-Gettext-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(base)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Locale::Maketext)
BuildRequires:  perl(Module::Build)
# Module::Signature not used
BuildRequires:  perl(Socket)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  sed
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Convert getext parameters to maketext parameters (CPAN RT#97771)
Patch0:         gettexttomakettext.patch

%description
Locale::Maketext::Gettext joins the GNU gettext and Maketext frameworks. It
is a subclass of Locale::Maketext(3) that follows the way GNU gettext
works. It works seamlessly, both in the sense of GNU gettext and Maketext.
As a result, you enjoy both their advantages, and get rid of both their
problems, too.

%prep
%setup -q -n Locale-Maketext-Gettext-%{version}
%patch0 -p 1

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT/*

%check
rm -f debugsources.list debugfiles.list debuglinks.list
./Build test

%files
%license Artistic COPYING
%doc BUGS Changes README THANKS TODO
%{perl_vendorlib}/*
%{_mandir}/man3/*
%{_bindir}/maketext
%{_mandir}/man1/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.30-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 07 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-1
- 1.30 bump

* Tue Sep 10 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-1
- 1.29 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 21 2015 Petr Pisar <ppisar@redhat.com> - 1.28-3
- Remove signature test (bug #1260618)

* Wed Aug 26 2015 Petr Šabata <contyk@redhat.com> - 1.28-2
- Disable the signature tests, failing due to the patch

* Thu Aug 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-1
- 1.28 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-17
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-16
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.27-13
- Perl 5.18 rebuild

* Tue Mar 19 2013 Rüdiger Landmann <rlandman@redhat.com> 1.27-12
- Patch properly this time

* Mon Mar 18 2013 Rüdiger Landmann <rlandman@redhat.com> 1.27-11
- Add patch to convert gettext %1 to maketext [_1]

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.27-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.27-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.27-4
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.27-3
- Mass rebuild with perl-5.12.0

* Mon Sep 21 2009 Rüdiger Landmann <rlandman@redhat.com> 1.27-2
- added BuildRequires:  perl(Test::More) and BuildRequires:  perl(Test::Pod)

* Mon Sep 07 2009 Rüdiger Landmann <rlandman@redhat.com> 1.27-1
- Specfile autogenerated by cpanspec 1.78.
