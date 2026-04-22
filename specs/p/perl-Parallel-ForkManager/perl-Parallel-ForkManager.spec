# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Parallel-ForkManager
Version:        2.03
Release: 4%{?dist}
Summary:        Simple parallel processing fork manager
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Parallel-ForkManager
Source0:        https://cpan.metacpan.org/authors/id/Y/YA/YANICK/Parallel-ForkManager-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  glibc-common
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  sed
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Moo) >= 1.001000
BuildRequires:  perl(Moo::Role)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Storable)
# Tests
BuildRequires:  perl(blib)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More) >= 0.94
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(utf8::all)


%description
This module is intended for use in operations that can be done in parallel
where the number of processes to be forked off should be limited. Typical
use is a downloader which will be retrieving hundreds/thousands of files.

%prep
%setup -q -n Parallel-ForkManager-%{version}

# Prepare the example scripts for inclusion as documentation, as they are not
# generally useful and have additional dependencies.
sed -i -e '1d' examples/*.pl
chmod 644 examples/*.pl

i=lib/Parallel/ForkManager.pm
iconv -f iso-8859-1 -t utf-8 < $i > $i. && touch -r $i $i. && mv -f $i. $i

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes examples/
%{perl_vendorlib}/Parallel
%{_mandir}/man3/Parallel::ForkManager*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.03-1
- 2.03 bump (rhbz#2307732)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 01 2023 Michal Josef Špaček <mspacek@redhat.com> - 2.02-16
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-13
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-10
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-7
- Perl 5.32 rebuild

* Wed Mar 18 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-6
- Add perl(blib) for tests

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.02-1
- Update to 2.02.
- Add new runtime dependencies (Moo and Moo::Role).
- Remove RHEL conditionals.

* Thu Jul 19 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.20-1
- Update to 1.20.
- Add CPAN::Meta build dependency.
- Fix RHEL conditional to be version-limited.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 26 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-1
- 1.19 bump

* Mon Jun 27 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.18-5
- Oops, wrong build dep.

* Thu Jun 23 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.18-4
- Change build dependencies to new recommended usage.

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.18-3
- Perl 5.24 rebuild

* Thu Mar 31 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.18-2
- Run iconv on the right file.

* Tue Mar 29 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.18-1
- Update to 1.18.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.17-2
- Remove pointless %%defattr statement.

* Wed Dec 02 2015 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.17-1
- Update to 1.17.

* Thu Oct 08 2015 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.16-1
- Update to 1.16; rhbz#1270082.  Add new Test::Warn build dep.

* Fri Aug 07 2015 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.15-2
- Add a couple of build dependencies that dropped out of the dep tree.

* Wed Jul 08 2015 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.15-1
- Update to latest upstream version.

* Tue Jun 23 2015 Marianne Lombard <jehane@fedoraproject.org> - 1.14
- Update to latest upstream version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-2
- Perl 5.22 rebuild

* Tue Feb 24 2015 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.12-1
- Update to latest upstream version.
- Use most direct download location.

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 17 2013 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.05-1
- Update to 1.05; new source location, additional build deps.  Should fix the
  longstanding security bug, 751886.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.7.9-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.7.9-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.7.9-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.7.9-1
- Update to current upstream version.
- Handle new upstream treatment of the examples.
- Update to modern packaging guidelines.

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.7.5-7
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.7.5-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.7.5-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.7.5-2
Rebuild for new perl

* Wed Jan 16 2008 Jason Tibbitts <tibbs@math.uh.edu> 0.7.5-1
- Specfile autogenerated by cpanspec 1.74.
- Make the .pl files documentation instead of installing them to avoid
  additional dependencies.  Also remove their shebang lines to quiet rpmlint.
