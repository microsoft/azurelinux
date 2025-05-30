Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Object-HashBase
Version:        0.013
Release:        3%{?dist}
Summary:        Build hash-based classes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Object-HashBase
Source0:        https://cpan.metacpan.org/authors/id/E/EX/EXODIST/Object-HashBase-%{version}.tar.gz#/perl-Object-HashBase-%{version}.tar.gz
# Correct shebangs
Patch0:         Object-HashBase-0.008-Normalize-shebang.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(File::Temp)
Suggests:       perl(Class::XSAccessor)

# Remove under-specified dependenices
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(Test::More\\)$
# Remove private modules
%global __requires_exclude %{__requires_exclude}|^perl\\(Object::HashBase::Test::HBase.*
%global __requires_exclude %{__requires_exclude}|^perl\\(My::Prefix::HashBase\\)$

%description
This package is used to generate classes based on hash references. Using this
class will give you a new() method, as well as generating accessors you
request.  Generated accessors will be getters, set_ACCESSOR setters will also
be generated for you. You also get constants for each accessor (all caps)
which return the key into the hash for that accessor. Single inheritance is
also supported.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%package tools
Summary:        Generate inlined Object::HashBase Perl module
Requires:       %{name} = %{version}-%{release}
Requires:       perl(Test::More) >= 0.98

%description tools
hashbase_inc.pl script generates a Perl module that contains
a Object::HashBase module mangled into a name space of your choice. It can
also generate the tests for it.

%prep
%setup -q -n Object-HashBase-%{version}
%patch -P0 -p1
# Help generators to recognize Perl scripts
for F in t/*.t; do
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
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%exclude %{perl_vendorlib}/Object/HashBase
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%files tools
%{_bindir}/hashbase_inc.pl
%{perl_vendorlib}/Object/HashBase

%changelog
* Wed Dec 18 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 0.013-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 22 2024 Michal Josef Špaček <mspacek@redhat.com> - 0.013-1
- 0.013 bump

* Thu Mar 21 2024 Michal Josef Špaček <mspacek@redhat.com> - 0.012-1
- 0.012 bump

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 23 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.010-1
- 0.010 bump
- Update %patch macro usage

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.009-11
- Package tests
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.009-9
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.009-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.009-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Petr Pisar <ppisar@redhat.com> - 0.009-1
- 0.009 bump

* Tue Nov 19 2019 Petr Pisar <ppisar@redhat.com> 0.008-1
- Specfile autogenerated by cpanspec 1.78.
