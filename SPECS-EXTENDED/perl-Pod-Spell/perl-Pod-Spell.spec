Name:           perl-Pod-Spell
Version:        1.27
Release:        1%{?dist}
Summary:        A formatter for spell-checking POD
License:        Artistic-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Pod-Spell
Source0:        https://cpan.metacpan.org/modules/by-module/Pod/Pod-Spell-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::ShareDir::Install) >= 0.06
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Class::Tiny)
BuildRequires:  perl(constant)
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Lingua::EN::Inflect)
BuildRequires:  perl(locale)
BuildRequires:  perl(parent)
BuildRequires:  perl(Pod::Simple)
BuildRequires:  perl(Text::Wrap)
# Optional run-time:
# I18N::Langinfo not used at tests
# POSIX not used at tests
# Tests:
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Temp) >= 0.17
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(utf8)
Requires:       perl(File::ShareDir)
Recommends:     perl(I18N::Langinfo)
Recommends:     perl(POSIX)

%description
Pod::Spell is a Pod formatter whose output is good for spell-checking.
Pod::Spell rather like Pod::Text, except that it doesn't put much
effort into actual formatting, and it suppresses things that look like
Perl symbols or Perl jargon (so that your spell-checking program won't
complain about mystery words like "$thing" or "Foo::Bar" or "hashref").

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
 
%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Pod-Spell-%{version}

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
mkdir -p %{buildroot}%{_libexecdir}/%{name}/bin
ln -s %{_bindir}/podspell %{buildroot}%{_libexecdir}/%{name}/bin
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{_bindir}/podspell
%{perl_vendorlib}/Pod/
%{perl_vendorlib}/auto/share/dist/Pod-Spell/
%{_mandir}/man1/podspell.1*
%{_mandir}/man3/Pod::Spell.3*
%{_mandir}/man3/Pod::Wordlist.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Feb 27 2025 Sumit Jena <v-sumitjena@microsoft.com> - 1.27-1
- Update to version 1.27
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep  6 2019 Paul Howarth <paul@city-fan.org> - 1.20-13
- Use author-independent source URL
- Bump version of File::Temp dependency to 0.17, needed for ->seek
- Enumerate man pages in %%files list

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-8
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-3
- Perl 5.24 rebuild

* Tue Apr 26 2016 Petr Pisar <ppisar@redhat.com> - 1.20-2
- Fix run-time dependencies (bug #1330601)

* Mon Apr 25 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-1
- 1.20 bump

* Mon Feb 22 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-1
- 1.19 bump

* Mon Feb 08 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.18-1
- 1.18 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.17-2
- Perl 5.22 rebuild

* Thu Mar 12 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.17-1
- 1.17 bump

* Wed Feb 25 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-2
- Specify all dependencies

* Wed Feb 25 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-1
- 1.16 bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-1
- 1.15 bump

* Tue Feb 18 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.14-1
- 1.14 bump

* Sun Nov 03 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-1
- 1.13 bump

* Fri Oct 18 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-1
- 1.12 bump

* Tue Oct 01 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-2
- Added test BR perl(utf8)

* Sat Sep 28 2013 Paul Howarth <paul@city-fan.org> - 1.10-1
- 1.10 bump

* Thu Sep 26 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.09-1
- 1.09 bump

* Wed Sep 25 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-1
- 1.08 bump

* Fri Sep 20 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-1
- 1.07 bump

* Tue Sep 10 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-1
- 1.06 bump
- Update dependencies

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 1.05-3
- Do not use env in podspell shebang

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 1.05-2
- Perl 5.18 rebuild

* Wed Jul 10 2013 Petr Šabata <contyk@redhat.com> - 1.05-1
- 1.05 bump

* Tue Jun 25 2013 Petr Pisar <ppisar@redhat.com> - 1.04-2
- Specify all dependencies

* Thu May 09 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-1
- 1.04 bump
- Update source URL and BR

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Petr Pisar <ppisar@redhat.com> - 1.01-15
- Specify all dependencies
- Convert README to UTF-8

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 1.01-13
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.01-11
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-9
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.01-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-4
- Rebuild for perl 5.10 (again)

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Mon Dec 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-2
- find: fixed arguments order.

* Sun Dec 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- First build.
