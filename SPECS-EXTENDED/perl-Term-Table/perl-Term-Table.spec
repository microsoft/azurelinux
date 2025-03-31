# Recognize terminal size
%bcond_without perl_Term_Table_enables_terminal
# Respect Unicode rules when breaking lines
%bcond_without perl_Term_Table_enables_unicode

Name:           perl-Term-Table
Version:        0.022
Release:        1%{?dist}
Summary:        Format a header and rows into a table
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Term-Table
Source0:        https://cpan.metacpan.org/authors/id/E/EX/EXODIST/Term-Table-%{version}.tar.gz
# Unbundle Object::HashBase
Patch0:         Term-Table-0.022-Use-system-Object-HashBase.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Object::HashBase) >= 0.008
BuildRequires:  perl(Scalar::Util)
# Optional run-time:
%if %{with perl_Term_Table_enables_terminal}
# Term::ReadKey 2.32 not used if Term::Size::Any is available
# Prefer Term::Size::Any over Term::ReadKey
BuildRequires:  perl(Term::Size::Any) >= 0.002
%endif
%if %{with perl_Term_Table_enables_unicode}
BuildRequires:  perl(Unicode::GCString) >= 2013.10
%endif
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(Test2::API)
BuildRequires:  perl(Test2::Tools::Tiny) >= 1.302097
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
%if %{with perl_Term_Table_enables_terminal}
Suggests:       perl(Term::ReadKey) >= 2.32
# Prefer Term::Size::Any over Term::ReadKey
Recommends:     perl(Term::Size::Any) >= 0.002
%endif
%if %{with perl_Term_Table_enables_unicode}
Recommends:     perl(Unicode::GCString) >= 2013.10
%endif

%description
This Perl module is able to format rows of data into tables.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Term-Table-%{version}
%patch -P0 -p1
# Delete bundled Object::HashBase
for F in lib/Term/Table/HashBase.pm t/HashBase.t; do
    perl -e 'unlink $ARGV[0] or die $!' "$F"
    perl -i -s -ne 'print $_ unless m{\A\Q$file\E\b}' -- -file="$F" MANIFEST
done
# Help generators to recognize Perl scripts
for F in t/*.t t/Table/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
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
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -r -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
unset TABLE_TERM_SIZE
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Aug 16 2024 Michal Josef Špaček <mspacek@redhat.com> - 0.022-1
- 0.022 bump

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.018-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.018-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 23 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.018-1
- 0.018 bump

* Fri Sep 15 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.017-1
- 0.017 bump
- Fix %patch macro

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 10 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.016-5
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.016-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.016-1
- 0.016 bump
- Package tests
- Unify macros

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.015-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.015-7
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.015-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.015-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.015-4
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.015-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 21 2019 Petr Pisar <ppisar@redhat.com> - 0.015-2
- Unbundle Object::HashBase

* Tue Nov 19 2019 Petr Pisar <ppisar@redhat.com> - 0.015-1
- 0.015 bump

* Wed Oct 16 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-1
- 0.014 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Petr Pisar <ppisar@redhat.com> - 0.013-1
- 0.013 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 20 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-1
- 0.012 bump

* Wed Oct 11 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-1
- 0.011 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-2
- Perl 5.26 rebuild

* Mon Mar 20 2017 Petr Pisar <ppisar@redhat.com> - 0.008-1
- 0.008 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Petr Pisar <ppisar@redhat.com> - 0.006-1
- 0.006 bump

* Mon Jan 02 2017 Petr Pisar <ppisar@redhat.com> - 0.005-1
- 0.005 bump

* Wed Dec 21 2016 Petr Pisar <ppisar@redhat.com> - 0.004-1
- 0.004 bump

* Tue Dec 20 2016 Petr Pisar <ppisar@redhat.com> 0.002-1
- Specfile autogenerated by cpanspec 1.78.
