# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Module-Load-Util
Version:        0.012
Release:        4%{?dist}
Summary:        Some utility routines related to module loading
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Module-Load-Util/
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PERLANCAR/Module-Load-Util-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(Regexp::Pattern::Perl::Module)
# Tests
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More) >= 0.98
Requires:       perl(Exporter) >= 5.57

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Exporter\\)\\s*$

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
This module contains some utility routines related to module loading.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Module-Load-Util-%{version}

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
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm %{buildroot}%{_libexecdir}/%{name}/t/author-*.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -r -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
unset AUTHOR_TESTING
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Module*
%{_mandir}/man3/Module::Load::Util*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 15 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-1
- 0.012 bump (rhbz#2280646)

* Mon Apr 15 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-1
- 0.011 bump (rhbz#2275028)

* Thu Jan 25 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-1
- 0.010 bump (rhbz#2260032)

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.009-1
- 0.009 bump (BZ#2220905)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-2
- Perl 5.36 rebuild

* Wed Mar 23 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-1
- 0.008 bump

* Wed Mar 02 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.007-1
- 0.007 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 01 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.006-1
- 0.006 bump

* Thu Sep 30 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.005-1
- 0.005 bump
- Package tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-2
- Perl 5.34 rebuild

* Wed Feb 10 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-1
- 0.004 bump

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 03 2020 Jitka Plesnikova <jplesnik@redhat.com> 0.003-1
- Specfile autogenerated by cpanspec 1.78.
