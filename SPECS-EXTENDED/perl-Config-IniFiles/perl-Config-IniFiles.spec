Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Config-IniFiles
Version:        3.000002
Release:        6%{?dist}
Summary:        A module for reading .ini-style configuration files
# LICENSE:                              GPL+ or Artistic
# lib/Config/IniFiles.pm:               GPL+ or Artistic
## Not distributed in a binary package
# t/30parameters-with-empty-values.t:   MIT
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Config-IniFiles
Source0:        https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Config-IniFiles-%{version}.tar.gz#/perl-Config-IniFiles-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build) >= 0.36
# Module::Build::Compat not used, we run Build.PL
BuildRequires:  perl(strict)
# Test::Run::CmdLine::Iface not used
BuildRequires:  perl(warnings)
BuildRequires:  sed
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Scalar) >= 2.109
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(Symbol)
BuildRequires:  perl(vars)
# Tests:
%if 0%{?with_check}
BuildRequires:  perl(English)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(base)
BuildRequires:  perl(blib)
BuildRequires:  perl(lib)
BuildRequires:  perl(parent)
%endif
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Not autodetected. Found in lib/Config/IniFiles.pm:2761
Requires:       perl(IO::Scalar) >= 2.109
# Also not autodetected
Requires:       perl(List::Util) >= 1.33

# Filter under-specified requires
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(List::MoreUtils\\)$

%description
Config::IniFiles provides a way to have readable configuration files
outside your Perl script. Configurations can be imported (inherited,
stacked,...), sections can be grouped, and settings can be accessed
from a tied hash.

%prep
%setup -q -n Config-IniFiles-%{version}
# Normalize end-of-lines
sed -i -e 's/\r$//' Changes OLD-Changes.txt

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%license LICENSE
%doc Changes OLD-Changes.txt README
%{perl_vendorlib}/Config/
%{_mandir}/man3/*.3pm*

%changelog
* Thu Sep 01 2022 Muhammad Falak <mwani@microsoft.com> - 3.000002-6
- Add BR on `perl(blib)` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.000002-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.000002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.000002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.000002-2
- Perl 5.30 rebuild

* Thu Mar 21 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.000002-1
- 3.000002 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.000001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 18 2019 Tom Callaway <spot@fedoraproject.org> - 3.000001-1
- 3.000001

* Wed Oct 03 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.000000-1
- 3.000000 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.98-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.98-2
- Perl 5.28 rebuild

* Fri May 11 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.98-1
- 2.98 bump

* Thu Apr 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.96-1
- 2.96 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.94-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.94-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.94-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.94-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec  1 2016 Tom Callaway <spot@fedoraproject.org> - 2.94-1
- update to 2.94

* Mon Jul 25 2016 Tom Callaway <spot@fedoraproject.org> - 2.93-1
- update to 2.93

* Fri Jun 17 2016 Tom Callaway <spot@fedoraproject.org> - 2.92-1
- update to 2.92

* Mon Jun  6 2016 Tom Callaway <spot@fedoraproject.org>- 2.91-1
- update to 2.91

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.89-2
- Perl 5.24 rebuild

* Tue May  3 2016 Tom Callaway <spot@fedoraproject.org> - 2.89-1
- update to 2.89

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.88-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 10 2015 Tom Callaway <spot@fedoraproject.org> - 2.88-1
- update to 2.88

* Tue Jun 16 2015 Tom Callaway <spot@fedoraproject.org> - 2.87-1
- update to 2.87

* Thu Jun 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.86-2
- Perl 5.22 rebuild

* Wed Jun 10 2015 Petr Pisar <ppisar@redhat.com> - 2.86-1
- 2.86 bump

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.83-4
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.83-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 13 2014 Tom Callaway <spot@fedoraproject.org> - 2.83-1
- update to 2.83

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 2.82-2
- Perl 5.18 rebuild

* Thu May 23 2013 Tom Callaway <spot@fedoraproject.org> - 2.82-1
- update to 2.82

* Fri May 17 2013 Tom Callaway <spot@fedoraproject.org> - 2.81-1
- update to 2.81

* Tue May  7 2013 Tom Callaway <spot@fedoraproject.org> - 2.79-1
- update to 2.79

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Tom Callaway <spot@fedoraproject.org> - 2.78-1
- update to 2.78

* Mon Jul 30 2012 Tom Callaway <spot@fedoraproject.org> - 2.77-1
- update to 2.77

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.72-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 2.72-2
- Perl 5.16 rebuild

* Fri May 11 2012 Tom Callaway <spot@fedoraproject.org> - 2.72-1
- update to 2.72
- notable fix: SECURITY BUG FIX: Config::IniFiles used to write 
  to a temporary filename with a predictable name 
  ("${filename}-new") which opens the door for potential
  exploits.
  Fixes CVE-2012-2451

* Tue Feb 21 2012 Tom Callaway <spot@fedoraproject.org> - 2.68-3
- add missing Requires: perl(IO::Scalar) >= 2.109 (bz 791078)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Tom Callaway <spot@fedoraproject.org> - 2.68-1
- update to 2.68

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.58-5
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.58-4
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.58-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.58-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jun 28 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.58-1
- update to 2.58

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.47-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.47-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.47-1
- Upstream update.
- Add Changes to %%doc.

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.40-0.1.20081120svn88
- Update to svn checkout, since 2.39 doesn't appear to be accurate.

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.39-6
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.39-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.39-5
- Rebuild for FC6.
- Convert man page to utf8.

* Wed Feb 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.39-4
- Rebuild for FC5 (perl 5.8.8).

* Sat May 14 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.39-3
- Add dist tag.

* Fri Apr 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.39-2
- Update to 2.39.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue May 25 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.38-2
- Patch URI generated from the RT entry as suggested (bug 1625)

* Thu May 20 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.38-0.fdr.1
- Patch: https://rt.cpan.org/NoAuth/Bug.html?id=2584
- First build.
