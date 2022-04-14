Summary:        See Your Data in the Nude
Name:           perl-XXX
Version:        0.38
Release:        2%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/XXX
Source0:        https://cpan.metacpan.org/authors/id/I/IN/INGY/XXX-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(JSON::Color)
BuildRequires:  perl(YAML::PP) >= 0.018
BuildRequires:  perl(base)

%if %{with_check}
# Tests
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Test::More)
# Test::Pod - optional
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(Data::Dumper)
Requires:       perl(YAML::PP) >= 0.018
# Optional, not package yet
# perl(Enbugger)
%endif

%description
XXX.pm exports a function called XXX that you can put just about
anywhere in your Perl code to make it die with a YAML dump of the
arguments to its right.

The charm of XXX-debugging is that it is easy to type and rarely
requires parens and stands out visually so that you remember to remove
it.

XXX.pm also exports WWW, YYY and ZZZ which do similar debugging things.

To use Data::Dumper instead of YAML:
   use XXX -dumper;

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(JSON::Color)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n XXX-%{version}

# Help file to recognise the Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm %{buildroot}%{_libexecdir}/%{name}/t/author-pod-syntax.t
# Needed XXX.pm in lib directory
rm %{buildroot}%{_libexecdir}/%{name}/t/000-compile-modules.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset AUTHOR_TESTING
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.38-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Thu Sep 02 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-1
- 0.38 bump

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-1
- 0.37 bump
- Package tests

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-7
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-5
- Replace requirement YAML by YAML::PP, it is default now

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-1
- 0.35 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-1
- 0.33 bump

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-1
- 0.32 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-1
- 0.31 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-2
- Perl 5.24 rebuild

* Thu Apr 28 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-1
- 0.30 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-2
- Perl 5.22 rebuild

* Mon Oct 13 2014 Petr Šabata <contyk@redhat.com> - 0.29-1
- 0.29 bump

* Wed Sep 10 2014 Petr Šabata <contyk@redhat.com> - 0.28-1
- 0.28 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-2
- Perl 5.20 rebuild

* Wed Aug 20 2014 Petr Šabata <contyk@redhat.com> - 0.27-1
- 0.27 bump

* Fri Aug 08 2014 Petr Šabata <contyk@redhat.com> - 0.24-1
- 0.24 bump

* Fri Aug 01 2014 Petr Šabata <contyk@redhat.com> - 0.23-1
- 0.23 bump

* Mon Jun 23 2014 Petr Šabata <contyk@redhat.com> - 0.21-1
- 0.21 bump; no code changes

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.18-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 0.18-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 05 2011 Petr Sabata <contyk@redhat.com> - 0.18-1
- 0.18 bump
- Remove now obsolete BuildRoot and defattr

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.17-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Sep 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-1
- 633760 update

* Fri May 14 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.12-7
- Bump release for perl-5.12.0 rebuild.

* Tue Apr 27 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.12-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Marcela Mašláňová <mmaslano@redhat.com> 0.12-2
- add BR Test::More and ExtUtils::MakeMaker

* Tue Apr 14 2009 Marcela Mašláňová <mmaslano@redhat.com> 0.12-1
- initial packaging
