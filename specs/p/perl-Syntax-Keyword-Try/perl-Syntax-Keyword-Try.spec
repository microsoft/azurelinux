# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%{bcond_without perl_Syntax_Keyword_Try_enables_extra_tests}
%else
%{bcond_with perl_Syntax_Keyword_Try_enables_extra_tests}
%endif

Name:           perl-Syntax-Keyword-Try
Version:        0.30
Release:        4%{?dist}
Summary:        try/catch/finally syntax for perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Syntax-Keyword-Try/
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Syntax-Keyword-Try-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(strict)
BuildRequires:  perl(XS::Parse::Keyword::Builder) >= 0.35
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(:VERSION) >= 5.14
BuildRequires:  perl(B)
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(XS::Parse::Keyword) >= 0.35
# Tests
BuildRequires:  perl(overload)
BuildRequires:  perl(Test2::IPC)
BuildRequires:  perl(Test2::V0)
# Optional
%if %{with perl_Syntax_Keyword_Try_enables_extra_tests}
BuildRequires:  perl(Future)
BuildRequires:  perl(Future::AsyncAwait)
BuildRequires:  perl(Syntax::Keyword::Defer)
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
BuildRequires:  perl(threads)

Requires:       perl(XS::Parse::Keyword) >= 0.35

%description
This module provides a syntax plugin that implements exception-handling
semantics in a form familiar to users of other languages, being built on a
block labeled with the try keyword, followed by at least one of a catch or
finally block.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if %{with perl_Syntax_Keyword_Try_enables_extra_tests}
Requires:       perl(Future)
Requires:       perl(Future::AsyncAwait)
%endif
Requires:       perl(threads)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Syntax-Keyword-Try-%{version}

%if %{without perl_Syntax_Keyword_Try_enables_extra_tests}
for F in t/80await+SKT.t t/80defer+SKT.t t/99pod.t; do
    rm "$F"
    perl -i -ne 'print $_ unless m{\A\Q'"$F"'\E\b}' MANIFEST
done
%endif

# Help file to recognise the Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Build.PL --installdirs=vendor --optimize="$RPM_OPT_FLAGS"
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm -f %{buildroot}%{_libexecdir}/%{name}/t/99pod.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
./Build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorarch}/auto/Syntax*
%{perl_vendorarch}/Syntax*
%{_mandir}/man3/Syntax::Keyword::Try*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-3
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 03 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-1
- 0.30 bump (rhbz#2309128)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-5
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-1
- 0.29 bump (rhbz#2222620)

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-3
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-1
- 0.28 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-2
- Perl 5.36 rebuild

* Mon Feb 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-1
- 0.27 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 14 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-1
- 0.26 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-2
- Add run-requires perl(XS::Parse::Keyword)

* Thu Jun 03 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-1
- 0.25 bump

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-2
- Perl 5.34 rebuild

* Tue May 11 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-1
- 0.24 bump

* Mon Mar 29 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-1
- 0.23 bump

* Fri Mar 26 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-1
- 0.22 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-1
- 0.21 bump

* Tue Nov 24 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-1
- 0.20 bump

* Mon Aug 03 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-1
- 0.18 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Petr Pisar <ppisar@redhat.com> - 0.16-1
- 0.16 bump

* Tue Jul 21 2020 Petr Pisar <ppisar@redhat.com> - 0.15-1
- 0.15 bump

* Wed Jul 08 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-1
- 0.14 bump

* Tue Jun 30 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-1
- 0.13 bump

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 09 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-1
- 0.11 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 18 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-1
- 0.10 bump

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-1
- Specfile autogenerated by cpanspec 1.78.
