# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-perlfaq
Version:        5.20250619
Release:        520%{?dist}
Summary:        Frequently asked questions about Perl
# Code examples are Public Domain
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND LicenseRef-Fedora-Public-Domain
URL:            https://metacpan.org/release/perlfaq
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/perlfaq-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More)
Conflicts:      perl < 4:5.22.0-347

%description
The perlfaq comprises several documents that answer the most commonly asked
questions about Perl and Perl programming.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n perlfaq-%{version}

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
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/perlfaq*
%{perl_vendorlib}/perlglossary*
%{_mandir}/man3/perlfaq*
%{_mandir}/man3/perlglossary*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.20250619-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5.20250619-519
- Increase release to favour standalone package

* Mon Jun 23 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5.20250619-1
- 5.20250619 bump (rhbz#2374272)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.20240218-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.20240218-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.20240218-510
- Increase release to favour standalone package

* Mon Feb 26 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.20240218-1
- 5.20240218 bump (rhbz#2265230)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.20230812-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.20230812-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 24 2023 Jitka Plesnikova <jplesnik@redhat.com> - 5.20230812-1
- 5.20230812 bump (rhbz#2231653)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.20230701-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 5.20230701-2
- Perl 5.38 rebuild

* Mon Jul 10 2023 Jitka Plesnikova <jplesnik@redhat.com> - 5.20230701-1
- 5.20230701 bump (rhbz#2219017)
- Package tests

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.20210520-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.20210520-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 5.20210520-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.20210520-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.20210520-478
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 5.20210520-477
- Increase release to favour standalone package

* Thu May 20 2021 Jitka Plesnikova <jplesnik@redhat.com> - 5.20210520-1
- 5.20210520 bump

* Mon Apr 12 2021 Jitka Plesnikova <jplesnik@redhat.com> - 5.20210411-1
- 5.20210411 bump

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.20201107-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 09 2020 Jitka Plesnikova <jplesnik@redhat.com> - 5.20201107-1
- 5.20201107 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.20200523-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 5.20200523-456
- Increase release to favour standalone package

* Fri May 22 2020 Petr Pisar <ppisar@redhat.com> - 5.20200523-1
- 5.20200523 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.20200125-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Petr Pisar <ppisar@redhat.com> - 5.20200125-1
- 5.20200125 bump

* Mon Nov 04 2019 Petr Pisar <ppisar@redhat.com> - 5.20191102-1
- 5.20191102 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.20190126-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 5.20190126-438
- Increase release to favour standalone package

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.20190126-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Petr Pisar <ppisar@redhat.com> - 5.20190126-1
- 5.20190126 bump

* Mon Sep 17 2018 Petr Pisar <ppisar@redhat.com> - 5.20180915-1
- 5.20180915 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.20180605-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 5.20180605-2
- Perl 5.28 rebuild

* Tue Jun 05 2018 Petr Pisar <ppisar@redhat.com> - 5.20180605-1
- 5.20180605 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.021011-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.021011-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 5.021011-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.021011-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 5.021011-2
- Perl 5.24 rebuild

* Mon Mar 07 2016 Petr Pisar <ppisar@redhat.com> - 5.021011-1
- 5.021011 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.021010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 29 2015 Petr Pisar <ppisar@redhat.com> - 5.021010-1
- 5.021010 bump

* Thu Jul 02 2015 Petr Pisar <ppisar@redhat.com> 5.021009-348
- Specfile autogenerated by cpanspec 1.78.
