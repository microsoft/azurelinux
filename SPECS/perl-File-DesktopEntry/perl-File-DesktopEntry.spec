# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional tests
%if ! (0%{?rhel})
%{bcond_without perl_File_DesktopEntry_enables_optional_test}
%else
%{bcond_with perl_File_DesktopEntry_enables_optional_test}
%endif

Name:           perl-File-DesktopEntry
Version:        0.22
Release:        29%{?dist}
Summary:        Object to handle .desktop files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/File-DesktopEntry
Source0:        https://cpan.metacpan.org/authors/id/M/MI/MICHIELB/File-DesktopEntry-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::BaseDir) >= 0.03
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Test::More) 
BuildRequires:  perl(utf8)
%if %{with perl_File_DesktopEntry_enables_optional_test} && !%{defined perl_bootstrap}
# Optional tests
# Build cycle: perl-CPAN-Changes → perl-Path-Tiny → perl-Unicode-UTF8
# → perl-Module-Install-ReadmeFromPod → perl-IO-All → perl-File-MimeInfo
# → perl-File-DesktopEntry → perl-CPAN-Changes
BuildRequires:  perl(Test::CPAN::Changes)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
%endif

Requires:       perl(Cwd)
Requires:       perl(File::Path)

%description
This module is used to work with .desktop files. The format of these files
is specified by the freedesktop "Desktop Entry" specification. This module
can parse these files but also knows how to run the applications defined by
these files. For this module version 1.0 of the specification was used.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n File-DesktopEntry-%{version}
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
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a MANIFEST t %{buildroot}%{_libexecdir}/%{name}
rm %{buildroot}%{_libexecdir}/%{name}/t/*_pod*
rm %{buildroot}%{_libexecdir}/%{name}/t/06_changes.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes
%{perl_vendorlib}/File*
%{_mandir}/man3/File::DesktopEntry*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed Aug 13 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-29
- Package tests

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-20
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-17
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-14
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-8
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-1
- 0.22 bump

* Thu Nov 26 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-1
- 0.21 bump

* Tue Nov 24 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-1
- 0.20 bump

* Mon Jun 22 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-1
- 0.12 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-1
- 0.11 bump

* Tue Jun 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-2
- Perl 5.22 rebuild

* Tue Jun 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-1
- 0.10 bump

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-4
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 08 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-1
- 0.08 bump
- Update patch and BR

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.05-2
- Perl 5.18 rebuild

* Fri Jun 07 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-1
- 0.05 bump
- Clean up spec
- Update source URL

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.04-17
- Perl 5.16 rebuild

* Fri Apr 27 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.04-15
- apply patch from MozBug for fixing encoding of utf-8 files 816809, cpan#76843

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.04-14
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-12
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-11
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-10
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.04-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.02-2
- rebuild for new perl

* Thu Dec 27 2007 Patrice Dumas <pertusus@free.fr> 0.04-5
- update to 0.04

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.02-1.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.02-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Wed Oct 11 2006 Patrice Dumas <pertusus@free.fr> 0.02-1
- Specfile autogenerated by cpanspec 1.69.
