%global cpan_name DBD-mysql

# Disable leak tests
%bcond_with perl_DBD_MySQL_enables_leak_test

%global mysqlname mysql

Name:           perl-DBD-MySQL
Version:        5.011
Release:        1%{?dist}
Summary:        A MySQL interface for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/%{cpan_name}
Source0:        https://cpan.metacpan.org/authors/id/D/DV/DVEEDEN/%{cpan_name}-%{version}.tar.gz
Source1:        test-setup.t
Source2:        test-clean.t
Source3:        testrules.yml
Source4:        test-env.sh

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
# DBD::mysql v5.x requires MySQL 8.x client libraries for building
BuildRequires:  %{mysqlname}-devel
BuildRequires:  openssl-devel
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBI::DBD)
BuildRequires:  perl(Devel::CheckLib) >= 1.09
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
BuildRequires:  zlib-devel
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(DBI) >= 1.609
BuildRequires:  perl(DBI::Const::GetInfoType)
BuildRequires:  perl(DynaLoader)
# Tests
BuildRequires:  %{mysqlname}
BuildRequires:  %{mysqlname}-server
BuildRequires:  perl(B)
BuildRequires:  perl(bigint)
# Required to process t/testrules.yml
BuildRequires:  perl(CPAN::Meta::YAML)
BuildRequires:  perl(Encode)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(vars)
# Optional tests
%if %{with perl_DBD_MySQL_enables_leak_test}
BuildRequires:  perl(Proc::ProcessTable)
BuildRequires:  perl(Storable)
%endif

Provides:       perl-DBD-mysql = %{version}-%{release}

%{?perl_default_filter}

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(.*lib.pl\\)

%description 
DBD::mysql is the Perl5 Database Interface driver for the MySQL database. In
other words: DBD::mysql is an interface between the Perl programming language
and the MySQL programming API that comes with the MySQL relational database
management system.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       coreutils
Requires:       shadow-utils
Requires:       %{mysqlname}
Requires:       %{mysqlname}-server
# Required to process t/testrules.yml
Requires:       perl(CPAN::Meta::YAML)
# Optional tests
%if %{with perl_DBD_MariaDB_enables_leak_test}
Requires:       perl(Proc::ProcessTable)
Requires:       perl(Storable)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n %{cpan_name}-%{version}

# Correct file permissions
find . -type f | xargs chmod -x

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} t/
cp %{SOURCE4} .

# Help file to recognise the Perl scripts and normalize shebangs
for F in t/*.t t/*.pl; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
. %{SOURCE4}
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" \
  NO_PACKLIST=1 NO_PERLLOCAL=1 \
  --testdb=$DBD_MYSQL_TESTDB \
  --testuser=$DBD_MYSQL_TESTUSER \
  --testpassword=$DBD_MYSQL_TESTPASSWORD \
  --testhost=$DBD_MYSQL_TESTHOST \
  --testsocket=$DBD_MYSQL_TESTSOCKET
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cp %{SOURCE4} %{buildroot}%{_libexecdir}/%{name}
# Replace build dir by template
perl -i -pe 's{%{_builddir}/.*mysql.sock}{_TEST_SOCKET_}' %{buildroot}%{_libexecdir}/%{name}/t/mysql.mtest
# Remove release tests
rm %{buildroot}%{_libexecdir}/%{name}/t/manifest.t
rm %{buildroot}%{_libexecdir}/%{name}/t/pod.t

cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/usr/bin/bash
set -e
# The tests write to temporary database which is placed in $DIR/t/testdb
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
. $DIR/$(basename %{SOURCE4})
%{!?with_perl_DBD_MySQL_enables_leak_test:unset EXTENDED_TESTING}
perl -i -pe "s{_TEST_SOCKET_}{$DBD_MYSQL_TESTSOCKET}" $DIR/t/mysql.mtest

# Test setup and tests have to be executed by non-root user
if [ `id -u` -ne 0 ]; then
    prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
else
    getent group $DBD_MYSQL_TESTUSER >/dev/null || \
        groupadd -r $DBD_MYSQL_TESTUSER
    getent passwd $DBD_MYSQL_TESTUSER >/dev/null || \
        useradd -g $DBD_MYSQL_TESTUSER $DBD_MYSQL_TESTUSER
    chown -hR $DBD_MYSQL_TESTUSER:$DBD_MYSQL_TESTUSER $DIR
    su $DBD_MYSQL_TESTUSER -c "prove -I . -j \"$(getconf _NPROCESSORS_ONLN)\""
    chown -hR root:root $DIR
    getent passwd $DBD_MYSQL_TESTUSER &>/dev/null && userdel -r $DBD_MYSQL_TESTUSER
    getent group $DBD_MYSQL_TESTUSER &>/dev/null && groupdel $DBD_MYSQL_TESTUSER
fi

popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
# Set MySQL and DBD::mysql test environment
. %{SOURCE4}
unset RELEASE_TESTING
make test %{?with_perl_DBD_MySQL_enables_leak_test:EXTENDED_TESTING=1}

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/auto/DBD/
%{_mandir}/man3/DBD::mysql*.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Jan 06 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5.011-1
- 5.011 bump (rhbz#2335778)

* Tue Nov 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.010-1
- 5.010 bump (rhbz#2325333)

* Mon Sep 23 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.009-1
- 5.009 bump (rhbz#2313530)

* Mon Aug 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.008-1
- 5.008 bump (rhbz#2301565)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.007-1
- 5.007 bump (rhbz#2295347)

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.006-2
- Perl 5.40 rebuild

* Wed Jun 05 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.006-1
- 5.006 bump (rhbz#2290474)

* Mon May 06 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.005-1
- 5.005 bump (rhbz#2278129)

* Wed Mar 27 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.004-2
- community-mysql was replaced by mysql
- remove using of %%{eln} macro (rhbz#2271821)

* Tue Mar 19 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.004-1
- 5.004 bump (rhbz#2270256)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 01 2023 Jitka Plesnikova <jplesnik@redhat.com> - 5.003-1
- 5.003 bump (rhbz#2252375)

* Tue Oct 24 2023 Jitka Plesnikova <jplesnik@redhat.com> - 5.002-1
- 5.002 bump (rhbz#2245834)

* Thu Oct 19 2023 Jitka Plesnikova <jplesnik@redhat.com> - 5.001-2
- Use community-mysql also for ELN

* Wed Oct 04 2023 Jitka Plesnikova <jplesnik@redhat.com> - 5.001-1
- 5.001 bump (rhbz#2242077)
  Since this version, MySQL 8.x has to be used for build
- Package tests

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.050-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4.050-17
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.050-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.050-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4.050-14
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.050-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.050-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.050-11
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.050-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.050-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.050-8
- Perl 5.32 rebuild

* Fri Mar 13 2020 Petr Pisar <ppisar@redhat.com> - 4.050-7
- Remove a useless shebang (bug #1813195)

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 4.050-6
- Use make_build/make_install macros
  
* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.050-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.050-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.050-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.050-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.050-1
- 4.050 bump

* Mon Nov 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.049-1
- 4.049 bump

* Mon Sep 17 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.048-1
- 4.048 bump

* Mon Sep 10 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.047-1
- 4.047 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.046-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.046-3
- Perl 5.28 rebuild

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.046-2
- Add build-require gcc

* Fri Feb 09 2018 Petr Pisar <ppisar@redhat.com> - 4.046-1
- 4.046 bump

* Thu Feb 08 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.045-1
- 4.045 bump

* Tue Jan 23 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.044-1
- 4.044 bump

* Tue Dec 19 2017 Petr Pisar <ppisar@redhat.com> - 4.043-7
- Fix building against mariadb-5.5.56

* Mon Dec 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.043-6
- Fixed CVE-2017-10789 (bug #1467600)

* Tue Sep 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.043-5
- Replace mariadb/-devel by mariadb-connector-c/-devel

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.043-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.043-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.043-2
- Fix for new version of MariaDB 10.2 (bug #1470196)

* Fri Jun 30 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.043-1
- 4.043 bump
- Fixed CVE-2017-10788 (bug #1467600)

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.042-2
- Perl 5.26 rebuild

* Thu Mar 09 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.042-1
- 4.042 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.041-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 29 2016 Petr Pisar <ppisar@redhat.com> - 4.041-1
- 4.041 bump (fixes CVE-2016-1251)

* Mon Nov 21 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.040-1
- 4.040 bump

* Wed Nov 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.039-1
- 4.039 bump

* Thu Oct 20 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.038-1
- 4.038 bump

* Mon Oct 03 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.037-1
- 4.037 bump

* Mon Aug 29 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.036-1
- 4.036 bump

* Thu Aug 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.035-3
- Remove using of iconv, because it is not needed (bug #1368046)

* Tue Aug 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.035-2
- Fix default value for nossl option (bug #1366773)

* Mon Jul 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.035-1
- 4.035 bump

* Thu Jul 07 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.034-1
- 4.034 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.033-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 27 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.033-1
- 4.033 bump

* Wed Jul 22 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.032-1
- 4.032 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.031-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.031-2
- Perl 5.22 rebuild

* Thu Mar 12 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.031-1
- 4.031 bump

* Thu Dec 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.029-1
- 4.029 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.028-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.028-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.028-1
- 4.028 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.027-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.027-1
- 4.027 bump

* Tue Jan 21 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.026-1
- 4.026 bump

* Tue Nov 05 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4.025-1
- 4.025 bump

* Thu Sep 19 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4.024-1
- 4.024 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.023-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 4.023-3
- Perl 5.18 rebuild

* Mon Apr 29 2013 Petr Šabata <contyk@redhat.com> - 4.023-2
- Force MariaDB dependency as a workaround for f19 compose

* Mon Apr 15 2013 Petr Pisar <ppisar@redhat.com> - 4.023-1
- 4.023 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 30 2012 Petr Šabata <contyk@redhat.com> - 4.022-1
- 4.022 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.021-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 4.021-2
- Perl 5.16 rebuild

* Wed May 02 2012 Petr Šabata <contyk@redhat.com> - 4.021-1
- 4.021 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.020-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Petr Sabata <contyk@redhat.com> - 4.020-1
- 4.020 bump

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.019-3
- Perl mass rebuild

* Fri May 13 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.019-2
- apply tested patch from F-15 (is_prefix replaced by strncmp) #703185
- remove deffattr

* Mon May  9 2011 Petr Sabata <psabata@redhat.com> - 4.019-1
- 4.019 bump
- Removing the clean section
- Adding DynaLoader to BR

* Tue Mar 22 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.018-3
- rebuilt for libmysqlclient

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.018-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4.018-1
- update

* Thu Aug 12 2010 Petr Pisar <ppisar@redhat.com> - 4.017-1
- 4.017 bump (bug #623614)
- Preserve time stamps while converting character set

* Mon Jul 12 2010 Petr Pisar <ppisar@redhat.com> - 4.016-1
- 4.016 bump (bug #597759)

* Mon May 31 2010 Petr Pisar <ppisar@redhat.com> - 4.014-1
- 4.014 bump (bug #597759)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.013-5
- Mass rebuild with perl-5.12.0

* Sun Mar 07 2010 Chris Weyl <cweyl@alumni.drew.edu> - 4.013-4
- add perl_default_filter (remove mysql.so provides)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4.013-3
- rebuild against perl 5.10.1

* Mon Oct 26 2009 Stepan Kasal <skasal@redhat.com> - 4.013-2
- new upstream version

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.011-3
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Stepan Kasal <skasal@redhat.com> - 4.011-1
- new upstream version
- apply iconv on primary source

* Mon Apr  6 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4.010-1
- update to the latest version

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.005-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.005-9
- respin (mysql)

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4.005-8
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.005-7
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4.005-6
- rebuild for new perl

* Wed Dec  5 2007 Robin Norwood <rnorwood@redhat.com> - 4.005-5
- Rebuild for new openssl

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 4.005-4
- Fix utf-8 rpmlint warning

* Tue Oct 23 2007 Robin Norwood <rnorwood@redhat.com> - 4.005-3
- Use fixperms macro
- Remove BR: perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 4.005-2.1
- add BR: perl(ExtUtils::MakeMaker)

* Fri Aug 24 2007 Robin Norwood <rnorwood@redhat.com> - 4.005-2
- rebuild

* Mon Aug 13 2007 Robin Norwood <rnorwood@redhat.com> - 4.005-1
- New version from CPAN: 4.005

* Thu Jun 07 2007 Robin Norwood <rnorwood@redhat.com> - 4.004-1
- New version from CPAN: 4.004
- Move requires filter into spec file

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 3.0008-1
- New version from CPAN: 3.0008

* Fri Sep 29 2006 Robin Norwood <rnorwood@redhat.com> - 3.0007-1
- Bugzilla: 208633
- Upgrade to upstream version 3.0007 version to fix some minor bugs.

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 3.0006-1.FC6
- Upgrade to 3.0006

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 3.0004-1.FC6
- upgrade to upstream version 3.0004

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.0002-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.0002-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 3.0002-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> - 3.0002-2
- rebuilt against new openssl

* Mon Jul 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.0002-1
- Update to 3.0002.

* Wed Apr 27 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.9007-1
- Update to 2.9007. (#156059)

* Thu Apr 14 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.9006-1
- Update to 2.9006.
- Specfile cleanup. (#154755)

* Thu Nov 25 2004 Miloslav Trmac <mitr@redhat.com> - 2.9004-4
- Convert man page to UTF-8

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 2.9003-1
- update to 2.9003

* Mon Jul  7 2003 Chip Turner <cturner@redhat.com> 2.9002-1
- move to 2.9002

* Thu Jul  3 2003 Chip Turner <cturner@redhat.com> 2.1021-5
- rebuild

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Wed Jan  1 2003 Chip Turner <cturner@redhat.com>
- turn ssl on and allow Makefile.PL to yse mysql_config to find proper link flags
- update to 2.1021

* Sat Dec 14 2002 Chip Turner <cturner@redhat.com>
- don't use internal rpm dep generator

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild

* Wed Aug  7 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 2.1017-3
- Rebuild

* Tue Jun 25 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 2.1017-2
- Rebuild, to fix #66304

* Wed Jun  5 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 2.1017-1
- New version - no longer integrated into msql-mysql modules

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Feb 22 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 1.2219-6
- Rebuild

* Fri Feb  8 2002 Chip Turner <cturner@minbar.devel.redhat.com>
- filter out "soft" dependencies: perl(Data::ShowTable)

* Thu Feb  7 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 1.2219-4
- Rebuild

* Tue Jan 22 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 1.2219-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 1.2219-1
- 1.2219

* Fri Jul 20 2001 Trond Eivind GlomsrÃ¸d <teg@redhat.com>
- Add zlib-devel to buildrequires (#49536)

* Sun Jul  1 2001 Trond Eivind GlomsrÃ¸d <teg@redhat.com>
- Add perl and perl-DBI to BuildRequires

* Wed May 30 2001 Trond Eivind GlomsrÃ¸d <teg@redhat.com>
- Change Group to Applications/Databases

* Tue May  1 2001 Trond Eivind GlomsrÃ¸d <teg@redhat.com>
- 1.2216
- Add doc files
- Minor cleanups

* Thu Nov 30 2000 Trond Eivind GlomsrÃ¸d <teg@redhat.com>
- First cut
