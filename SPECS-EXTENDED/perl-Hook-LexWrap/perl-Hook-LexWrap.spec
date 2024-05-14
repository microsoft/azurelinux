Name:           perl-Hook-LexWrap
Version:        0.26
Release:        11%{?dist}
Summary:        Lexically scoped subroutine wrappers
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Hook-LexWrap
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/Hook-LexWrap-%{version}.tar.gz#/perl-Hook-LexWrap-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Hook::LexWrap allows you to install a pre- or post-wrapper (or both)
around an existing subroutine. Unlike other modules that provide this
capacity (e.g. Hook::PreAndPost and Hook::WrapSub), Hook::LexWrap
implements wrappers in such a way that the standard `caller' function
works correctly within the wrapped subroutine.

%prep
%setup -q -n Hook-LexWrap-%{version}

%build
PERL_MM_FALLBACK_SILENCE_WARNING=1 perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes CONTRIBUTING README demo/
%{perl_vendorlib}/Hook/
%{_mandir}/man3/Hook::LexWrap.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.26-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-2
- Perl 5.26 rebuild

* Thu Feb 23 2017 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26
  - Properly wrap CORE::caller for @DB::args (CPAN RT#103186)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-2
- Perl 5.22 rebuild

* Tue Oct 21 2014 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25
  - Fix for perl 5.21.4: ensure barewords are parsed properly (CPAN RT#99021,
    Perl RT#122757)
- This release by ETHER → update source URL
- Package new upstream documentation and license file
- No longer need to fix line endings
- Classify buildreqs by usage
- Silence bogus warning about not having bleeding edge build modules

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.24-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 24 2012 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - Add Build.PL
  - Better support for debugger
  - Makefile.PL fixed
  - New test added
- BR: perl(Carp)
- Include demo files as %%doc
- Fix line endings on documentation
- Upstream release is now a tarball rather than a zipfile
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Use %%{_fixperms} macro rather than our own chmod incantation
- Don't use macros for commands
- Make %%files list more explicit

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.22-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.22-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.22-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Ralf Corsepius <corsepiu@fedoraproject.org> - 0.22-1
- Upstream update.
- Reflect upstream having fixed CPAN RT#38892:
  Remove Hook-LexWrap-0.21-cpan-rt-38892.diff.
- Reflect upstream having fixed permissions.

* Mon Nov 10 2008 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
- New upstream maintainer => new source URL
- Add buildreqs perl(Test::More) and perl(Test::Pod)
- Update patch for CPAN RT#38892 to apply without fuzz
- Fix argument order for find with -depth

* Mon Oct 06 2008 Ralf Corsepius <corsepiu@fedoraproject.org> - 0.20-6
- Add Hook-LexWrap-0.20-cpan-rt-38892.diff to fix
  https://rt.cpan.org/Public/Bug/Display.html?id=38892
  (Bugs shows while building rt3).

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.20-5
- Rebuild for perl 5.10 (again)

* Sat Jan 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.20-4.2
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.20-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-4
- Rebuild for FC6.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-3
- Rebuild for FC5 (perl 5.8.8).

* Fri Sep  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-2
- Comment about license files location.

* Fri Aug 26 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-1
- First build.
