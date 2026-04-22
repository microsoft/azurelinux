# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-JSON-XS
Summary:        JSON serializing/de-serializing, done correctly and fast
Epoch:          1
Version:        4.04
Release: 2%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/JSON-XS
Source0:        https://cpan.metacpan.org/modules/by-module/JSON/JSON-XS-%{version}.tar.gz
# Build
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Canary::Stability)
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  sed
# Module Runtime
BuildRequires:  perl(common::sense)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Types::Serialiser)
BuildRequires:  perl(XSLoader)
# Script Runtime
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Storable)
BuildRequires:  perl(strict)
# Test Suite
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Array)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
# Dependencies
# (none)

%{?perl_default_filter}

%description
This module converts Perl data structures to JSON and vice versa. Its
primary goal is to be correct and its secondary goal is to be fast. To
reach the latter goal it was written in C.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n JSON-XS-%{version}

sed -i 's/\r//' t/*
perl -MConfig -pi -e 's|^#!/opt/bin/perl|$Config{startperl}|' eg/*
chmod -c -x eg/*

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1 </dev/null
%{make_build}

%install
%{make_install}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
# Correct permissions
%{_fixperms} -c %{buildroot}

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes README eg/
%license COPYING
%{_bindir}/json_xs
%{perl_vendorarch}/auto/JSON/
%{perl_vendorarch}/JSON/
%{_mandir}/man1/json_xs.1*
%{_mandir}/man3/JSON::XS.3*
%{_mandir}/man3/JSON::XS::Boolean.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Sep 08 2025 Emmanuel Seyman <emmanuel@seyman.fr> - 1:4.04-1
- Update to 4.04

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.03-17
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.03-14
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.03-10
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.03-7
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.03-4
- Perl 5.34 rebuild

* Mon Feb 22 2021 Petr Pisar <ppisar@redhat.com> - 1:4.03-3
- Package tests manually

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 Paul Howarth <paul@city-fan.org> - 1:4.03-1
- Update to 4.03
- Use %%{make_build} and %%{make_install}
- Simplify files list a bit

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.02-5
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:4.02-2
- Perl 5.30 rebuild

* Wed Mar  6 2019 Paul Howarth <paul@city-fan.org> - 1:4.02-1
- Update to 4.02

* Mon Feb 25 2019 Paul Howarth <paul@city-fan.org> - 1:4.01-1
- Update to 4.01

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Paul Howarth <paul@city-fan.org> - 1:4.0-1
- Update to 4.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.04-4
- Perl 5.28 rebuild

* Wed Feb 21 2018 Paul Howarth <paul@city-fan.org> - 1:3.04-3
- Specify all dependencies

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 20 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 1:3.04-1
- Update to 3.04

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.03-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 20 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 1:3.03-2
- Update to 3.03

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.02-2
- Perl 5.24 rebuild

* Fri Mar 11 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 1:3.02-1
- Update to 3.02
- Add needed BuildRequires
- PAss NO_PACKLIST to Makefile.PL
- Use %%license macro

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.01-5
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.01-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Nov 03 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 1:3.01-1
- Update to 3.01

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1:2.34-2
- Perl 5.18 rebuild

* Sun May 26 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 1:2.34-1
- Update to 2.34

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 02 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1:2.33-1
- Update to 2.33

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1:2.32-2
- Perl 5.16 rebuild
- Specify all dependencies

* Thu Jan 12 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1:2.32-1
- Update to 2.32
- Clean up spec file

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:2.30-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1:2.30-1
- update

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:2.27-2
- Mass rebuild with perl-5.12.0

* Sat Feb 27 2010 Chris Weyl <cweyl@alumni.drew.edu> 1:2.27-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- added a new br on perl(common::sense) (version 0)
- added a new req on perl(common::sense) (version 0)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:2.24-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.24-1
- auto-update to 2.24 (by cpan-spec-update 0.01)

* Thu Mar 26 2009 Chris Weyl <cweyl@alumni.drew.edu> - 2.2311-4
- Stripping bad provides of private Perl extension libs

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2311-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2311-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.2311-1
- update to 2.2311

* Sun Sep 07 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.2222-1
- update to the increasingly silly version of 2.2222
- update files to include bin

* Wed Jun 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.21-1
- update to 2.21

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.2-1
- update to 2.2

* Sun Mar 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.01-1
- update to 2.x series before F9

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.52-3
Rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.52-2
- Autorebuild for GCC 4.3

* Wed Oct 17 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.52-1
- update to 1.52
- license tag update: GPL -> GPL+

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.43-2
- bump

* Thu Aug 09 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.43-1
- update to 1.43

* Fri Jun 01 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.22-1
- update to 1.22

* Mon May 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.21-3
- bump

* Mon May 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.21-2
- add eg/ to doc

* Sun May 13 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.21-1
- Specfile autogenerated by cpanspec 1.71.
