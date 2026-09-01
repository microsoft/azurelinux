# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform an optional test
%bcond_without perl_Inline_enables_optional_test

Name:           perl-Inline
Version:        0.87
Release:        1%{?dist}
Summary:        Inline Perl module
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Url:            https://metacpan.org/release/Inline
Source0:        https://cpan.metacpan.org/authors/id/I/IN/INGY/Inline-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Find)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Spec) >= 0.80
BuildRequires:  perl(File::Spec::Unix)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Socket)
BuildRequires:  perl(utf8)
BuildRequires:  perl(version) >= 0.82
# Tests only
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Inline::Files)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
# Test::Pod 1.41 not used
BuildRequires:  perl(Test::Warn) >= 0.23
%if %{with perl_Inline_enables_optional_test}
# Optional tests
BuildRequires:  perl(diagnostics)
%endif
Requires:       perl(Digest::MD5)
Requires:       perl(DynaLoader)
Requires:       perl(File::Spec) >= 0.80
Requires:       perl(FindBin)
Requires:       perl(Socket)
Requires:       perl(version) >= 0.82

%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((File::Spec|version)\\)$
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}^perl\\(Inline\\)$
# Remove private modules
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((TestInlineSetup|TestML::Bridge)\\)$
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
The Inline module allows you to put source code from other programming
languages directly "inline" in a Perl script or module. The code is
automatically compiled as needed, and then loaded for immediate access
from Perl.

Inline saves you from the hassle of having to write and compile your
own glue code using facilities like XS or SWIG. Simply type the code
where you want it and run your Perl as normal. All the hairy details
are handled for you. The compilation and installation of your code
chunks all happen transparently; all you will notice is the delay of
compilation on the first run.

The Inline code only gets compiled the first time you run it (or
whenever it is modified) so you only take the performance hit
once. Code that is Inlined into distributed modules (like on the CPAN)
will get compiled when the module is installed, so the end user will
never notice the compilation time.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Inline-%{version}
find example -type f -exec chmod 0644 {} +
# Help generators to recognize Perl scripts
for F in t/*.t; do
    if [ "$F" != "t/03errors.t" ] && [ "$F" != "t/09perl5lib.t" ]; then
        perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    fi
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
# Remove author tests
rm -f %{buildroot}%{_libexecdir}/%{name}/t/000*
rm -f %{buildroot}%{_libexecdir}/%{name}/t/author-pod-syntax.t
# XXX Not running
rm -f %{buildroot}%{_libexecdir}/%{name}/t/03errors.t
rm -f %{buildroot}%{_libexecdir}/%{name}/t/09perl5lib.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
unset PERL_INLINE_DIRECTORY PERL5LIB PERL5OPT
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
unset AUTHOR_TESTING PERL_INLINE_DIRECTORY PERL5LIB PERL5OPT
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING example README
%{perl_vendorlib}/Inline*
%{_mandir}/man3/*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Tue Aug 05 2025 Michal Josef Špaček <mspacek@redhat.com> - 0.87-1
- 0.87 bump
  Bundle TestML back, in Inline is developer release of TestML.

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 07 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.86-13
- Fix required packages in *-tests package

* Wed Dec 07 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.86-12
- Remove provided packages in *-tests package

* Fri Dec 02 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.86-11
- Package tests
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-9
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Petr Pisar <ppisar@redhat.com> - 0.86-1
- 0.86 bump

* Tue Jan 07 2020 Petr Pisar <ppisar@redhat.com> - 0.85-1
- 0.85 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.83-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.83-2
- Perl 5.30 rebuild

* Mon Apr 29 2019 Petr Pisar <ppisar@redhat.com> - 0.83-1
- 0.83 bump

* Wed Apr 03 2019 Petr Pisar <ppisar@redhat.com> - 0.82-1
- 0.82 bump

* Mon Feb 04 2019 Petr Pisar <ppisar@redhat.com> - 0.81-1
- 0.81 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.80-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.80-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.80-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.80-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.80-2
- Perl 5.22 rebuild

* Wed Mar 18 2015 Petr Šabata <contyk@redhat.com> - 0.80-1
- 0.80 bump

* Wed Feb 18 2015 Petr Šabata <contyk@redhat.com> - 0.79-1
- 0.79 bump, Win32 fixes only

* Fri Dec 05 2014 Petr Šabata <contyk@redhat.com> - 0.78-1
- 0.78 bump

* Mon Sep 29 2014 Petr Šabata <contyk@redhat.com> - 0.77-1
- 0.77 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.76-2
- Perl 5.20 rebuild

* Wed Aug 20 2014 Petr Šabata <contyk@redhat.com> - 0.76-1
- 0.76 bump

* Thu Aug 14 2014 Petr Šabata <contyk@redhat.com> - 0.68-2
- Don't require Filters or Struct when bootstrapping

* Tue Aug 12 2014 Petr Šabata <contyk@redhat.com> - 0.68-1
- 0.68 bump

* Fri Aug 08 2014 Petr Pisar <ppisar@redhat.com> - 0.67-1
- 0.67 bump

* Fri Aug 01 2014 Petr Šabata <contyk@redhat.com> - 0.66-1
- 0.66 bump

* Wed Jul 16 2014 Petr Šabata <contyk@redhat.com> - 0.62-1
- 0.62 bump
- Remove Inline::C from distribution

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Petr Šabata <contyk@redhat.com> - 0.55-1
- 0.55 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.53-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.53-4
- Perl 5.18 rebuild

* Sat Jul 20 2013 Petr Šabata <contyk@redhat.com> - 0.53-3
- Correcting the Licence tag; C-Cookbook.pod is Artistic only
- Fix a bogus date in changelog

* Sat Jul 20 2013 Petr Šabata <contyk@redhat.com> - 0.53-2
- Add some missing dependencies

* Thu May 02 2013 Petr Šabata <contyk@redhat.com> - 0.53-1
- 0.53 bump, marker regexp enhancements

* Thu Mar 07 2013 Petr Šabata <contyk@redhat.com> - 0.52-1
- 0.52 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Petr Šabata <contyk@redhat.com> - 0.51-2
- Use DESTDIR
- Don't remove the nonexistent empty directories

* Mon Oct 15 2012 Petr Šabata <contyk@redhat.com> - 0.51-1
- 0.51 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 0.50-2
- Perl 5.16 rebuild

* Tue Feb 07 2012 Petr Šabata <contyk@redhat.com> - 0.50-1
- 0.50 bump
- Minor cleanup

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Marcela Mašláňová <mmaslano@redhat.com> 0.49-1
- bump to 0.49
- add BR: perl(Carp), perl(File::Spec), perl(Test::More)
- add R: perl(Data::Dumper)

* Wed Nov 09 2011 Iain Arnell <iarnell@gmail.com> 0.48-3
- R/BR perl(Digest::MD5)

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.48-2
- Perl mass rebuild
- fix filter macro

* Mon Mar  7 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.48-1
- update to 0.48
- add Test::Warn into BR

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.47-1
- 671863 update to 0.47

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.46-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jul 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.46-1
- update to 0.46

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.44-24
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.44-23
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.44-19
- rebuild for new perl

* Mon Nov 19 2007 Robin Norwood <rnorwood@redhat.com> - 0.44-18
- Add BR: perl(Inline::Files)

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 0.44-17
- Various fixes from package review

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.44-16
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.44-15.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Apr 21 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.44-15
- BuildArch correction (noarch). (#155811)
- Bring up to date with current Fedora.Extras perl spec template.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Chip Turner <cturner@redhat.com> 0.44-10
- rebuild

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Chip Turner <cturner@redhat.com> 0.44-8
- rebuild

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild
- update to 0.44

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Thu Jun 27 2002 Chip Turner <cturner@redhat.com>
- description update

* Fri Jun 07 2002 cturner@redhat.com
- Specfile autogenerated

