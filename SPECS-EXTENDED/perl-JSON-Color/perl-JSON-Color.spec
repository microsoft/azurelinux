Name:           perl-JSON-Color
Version:        0.134
Release:        6%{?dist}
Summary:        Encode to colored JSON
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

URL:            https://metacpan.org/release/JSON-Color/
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PERLANCAR/JSON-Color-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.10.1
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(Color::ANSI::Util)
BuildRequires:  perl(ColorTheme::NoColor)
BuildRequires:  perl(ColorThemeBase::Static::FromStructColors)
BuildRequires:  perl(ColorThemeRole::ANSI)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Graphics::ColorNamesLite::WWW)
BuildRequires:  perl(Module::Load::Util) >= 0.009
BuildRequires:  perl(parent)
BuildRequires:  perl(Role::Tiny)
# Not used for tests - Scalar::Util::LooksLikeNumber
BuildRequires:  perl(Term::ANSIColor) >= 3.00
# Tests
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More) >= 0.98
Requires:       perl(ColorTheme::NoColor)
Requires:       perl(Module::Load::Util) >= 0.009
Requires:       perl(Role::Tiny)
Requires:       perl(Term::ANSIColor) >= 3.00
Recommends:     perl(Scalar::Util::LooksLikeNumber)

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Term::ANSIColor)\\)\s*$

%description
This module generates JSON, colorized with ANSI escape sequences.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n JSON-Color-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

# Help file to recognise the Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%install
%{make_install}
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm %{buildroot}%{_libexecdir}/%{name}/t/author*
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
unset AUTHOR_TESTING
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/ColorTheme*
%{perl_vendorlib}/JSON*
%{_mandir}/man3/ColorTheme::JSON::Color::*
%{_mandir}/man3/JSON::Color*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed Mar 19 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 0.134.6
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.134-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.134-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.134-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.134-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.134-1
- 0.134 bump (BZ#2219181)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.133-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.133-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.133-4
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.133-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.133-2
- Added missing requires perl(ColorTheme::NoColor)

* Mon Nov 29 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.133-1
- 0.133 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.131-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.131-2
- Perl 5.34 rebuild

* Fri May 14 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.131-1
- 0.131 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.130-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.130-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.130-2
- Specify all dependencies

* Fri Jul 03 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.130-1
- 0.130 bump

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-7
- Perl 5.32 rebuild

* Fri Feb 28 2020 Petr Pisar <ppisar@redhat.com> - 0.12-6
- Build-require blib for tests

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-1
- Specfile autogenerated by cpanspec 1.78.
