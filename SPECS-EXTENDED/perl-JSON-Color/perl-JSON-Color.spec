%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Term::ANSIColor)\\)\s*$

Summary:        Encode to colored JSON
Name:           perl-JSON-Color
Version:        0.133
Release:        3%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/JSON-Color/
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PERLANCAR/JSON-Color-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.10.1
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

# Run-time
BuildRequires:  perl(Color::ANSI::Util)
BuildRequires:  perl(ColorTheme::NoColor)
BuildRequires:  perl(ColorThemeBase::Static::FromStructColors)
BuildRequires:  perl(ColorThemeRole::ANSI)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Graphics::ColorNamesLite::WWW)
BuildRequires:  perl(Module::Load::Util) >= 0.004
BuildRequires:  perl(Role::Tiny)
BuildRequires:  perl(Term::ANSIColor) >= 3.00
BuildRequires:  perl(parent)

%if %{with_check}
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(blib)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(ColorTheme::NoColor)
Requires:       perl(Module::Load::Util) >= 0.004
Requires:       perl(Role::Tiny)
Requires:       perl(Term::ANSIColor) >= 3.00
Recommends:     perl(Scalar::Util::LooksLikeNumber)

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
%make_build

# Help file to recognise the Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%install
%make_install
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
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.133-3
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

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
