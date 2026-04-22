# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Disable leak tests
%bcond_with perl_DBD_MariaDB_enables_leak_test
# Perform optional net_ssleay tests
%if 0%{?rhel}
%bcond_with perl_DBD_MariaDB_enables_net_ssleay_test
%else
%bcond_without perl_DBD_MariaDB_enables_net_ssleay_test
%endif

Name:           perl-DBD-MariaDB
Version:        1.24
Release: 4%{?dist}
Summary:        MariaDB and MySQL driver for the Perl5 Database Interface (DBI)
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/DBD-MariaDB/
Source0:        https://cpan.metacpan.org/authors/id/P/PA/PALI/DBD-MariaDB-%{version}.tar.gz
Source1:        test-setup.t
Source2:        test-clean.t
Source3:        test-env.sh
Patch0:         DBD-MariaDB-1.23-Run-test-setup-and-clean.patch
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  mariadb-connector-c
BuildRequires:  mariadb-connector-c-devel
BuildRequires:  openssl-devel
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBI) >= 1.608
BuildRequires:  perl(DBI::DBD)
BuildRequires:  perl(Devel::CheckLib) >= 1.12
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
BuildRequires:  sscg
# Tests
BuildRequires:  hostname
BuildRequires:  mariadb
BuildRequires:  mariadb-server
BuildRequires:  perl(B)
BuildRequires:  perl(bigint)
BuildRequires:  perl(constant)
# Required to process t/testrules.yml
BuildRequires:  perl(CPAN::Meta::YAML)
BuildRequires:  perl(DBI::Const::GetInfoType)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More) >= 0.90
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(vars)
# Optional tests
%if %{with perl_DBD_MariaDB_enables_net_ssleay_test}
BuildRequires:  perl(Net::SSLeay)
%endif
%if %{with perl_DBD_MariaDB_enables_leak_test}
BuildRequires:  perl(Proc::ProcessTable)
BuildRequires:  perl(Storable)
%endif


# Filter private modules for tests
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(lib.pl\\)

%description
DBD::MariaDB is the Perl5 Database Interface driver for MariaDB and MySQL
databases. In other words: DBD::MariaDB is an interface between the Perl
programming language and the MariaDB/MySQL programming API that comes with
the MariaDB/MySQL relational database management system. Most functions
provided by this programming API are supported. Some rarely used functions
are missing, mainly because no-one ever requested them.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       hostname
Requires:       mariadb
Requires:       mariadb-server
# Required to process t/testrules.yml
Requires:       perl(CPAN::Meta::YAML)
# Optional tests
%if %{with perl_DBD_MariaDB_enables_net_ssleay_test}
Requires:       perl(Net::SSLeay)
%endif
%if %{with perl_DBD_MariaDB_enables_leak_test}
Requires:       perl(Proc::ProcessTable)
Requires:       perl(Storable)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n DBD-MariaDB-%{version}
%patch -P0 -p1
cp %{SOURCE1} %{SOURCE2} t/

# Create certificates for tests
mkdir t/certs
sscg --hostname=localhost --ca-mode=0644 --ca-key-mode=0640 --cert-key-mode=0640 --no-dhparams-file
mv ca.crt service-key.pem service.pem t/certs

# Help file to recognise the Perl scripts and normalize shebangs
for F in t/*.t t/*.pl; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

# Remove release tests
for F in t/pod.t t/manifest.t; do
    rm "$F"
    perl -i -ne 'print $_ unless m{^\Q'"$F"'\E}' MANIFEST
    perl -i -ne 'print $_ unless m{\Q'"$F"'\E}' t/testrules.yml
done

%if %{without perl_DBD_MariaDB_enables_leak_test}
# Remove unused tests
for F in t/60leaks.t t/rt86153-reconnect-fail-memory.t; do
    rm "$F"
    perl -i -ne 'print $_ unless m{^\Q'"$F"'\E}' MANIFEST
    perl -i -ne 'print $_ unless m{\Q'"$F"'\E}' t/testrules.yml
done
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cp %{SOURCE3} %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/usr/bin/bash
set -e
unset RELEASE_TESTING

# The tests write to temporary database which is placed in $DIR/t/testdb
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./

# Load the variables
. $DIR/$(basename %{SOURCE3})

# Run tests
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
# Set MariaDB and DBD::MariaDB test environment
. %{SOURCE3}

unset RELEASE_TESTING
make test %{?with_perl_DBD_MariaDB_enables_leak_test:EXTENDED_TESTING=1}

%files
%license LICENSE
%doc Changes Changes.historic
%{perl_vendorarch}/auto/DBD*
%{perl_vendorarch}/DBD*
%{_mandir}/man3/DBD::MariaDB*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-2
- Perl 5.42 rebuild

* Mon May 05 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-1
- 1.24 bump (rhbz#2363982)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-7
- Generate SSL needed for tests since mariadb-connector-c 3.4.x

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-5
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 19 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-2
- Replace using mysql by mariadb in setup script

* Mon Sep 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-1
- 1.23 bump (rhbz#2238227)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-5
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-2
- Perl 5.36 rebuild

* Tue Apr 26 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-1
- 1.22 bump

* Thu Feb 17 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-16
- Fix test for mariadb-connector-c 3.2.x

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-13
- Perl 5.34 rebuild

* Tue May 04 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-12
- Update tests

* Fri Mar 12 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-11
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-8
- Perl 5.32 rebuild

* Fri Apr 17 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-7
- Update setup script due to Pali's comments

* Tue Feb 04 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-6
- Update setup script to work with MariaDB 10.4

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-3
- Run setup as part of tests

* Wed Jun 26 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-2
- Enable tests

* Thu Jun 13 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-1
- Specfile autogenerated by cpanspec 1.78.
