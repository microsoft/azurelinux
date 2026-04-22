# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# According to documentation, module using Coro is just:
# A PROOF-OF-CONCEPT IMPLEMENTATION FOR EXPERIMENTATION.
# Omit Coro support on bootsrap bacause perl-DBI is pulled in by core
# perl-CPANPLUS.
%if %{defined perl_bootstrap} || 0%{?rhel} >= 7
%bcond_with perl_DBI_enables_coro
%else
%bcond_without perl_DBI_enables_coro
%endif

%if 0%{?rhel}
# Test with and suggest Clone Perl module for better multithreading
%bcond_with perl_DBI_enables_Clone
# Test with and suggest DB_File Perl module
%bcond_with perl_DBI_enables_DB_File
# Test with and suggest MLDBM Perl module for arbitrary mulicolumn databases
%bcond_with perl_DBI_enables_MLDBM
%else
%bcond_without perl_DBI_enables_Clone
%bcond_without perl_DBI_enables_DB_File
%bcond_without perl_DBI_enables_MLDBM
%endif
# Test with and suggest SQL::Statement Perl module for more serialization
# formats
# SQL::Statement is optional, and it is in build-cycle with DBI
%if %{defined perl_bootstrap} || 0%{?rhel}
%bcond_with perl_DBI_enables_SQL_Statement
%else
%bcond_without perl_DBI_enables_SQL_Statement
%endif

Name:           perl-DBI
Version:        1.647
Release: 5%{?dist}
Summary:        A database access API for perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            http://dbi.perl.org/
Source0:        https://cpan.metacpan.org/modules/by-module/DBI/DBI-%{version}.tgz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-common
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Find)
BuildRequires:  perl(strict)
BuildRequires:  sed
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
BuildRequires:  perl(constant)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
%if %{with perl_DBI_enables_coro}
# Coro Not needed by tests
# Coro::Handle not needed by tests
# Coro::Select not needed by tests
%endif
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(threads)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
# Optional run-time:
%if %{with perl_DBI_enables_Clone}
BuildRequires:  perl(Clone) >= 0.34
%endif
%if %{with perl_DBI_enables_DB_File}
BuildRequires:  perl(DB_File)
%endif
%if %{with perl_DBI_enables_MLDBM}
BuildRequires:  perl(MLDBM)
%endif
# Do not build-require optional Params::Util to test the fall-back code
%if %{with perl_DBI_enables_SQL_Statement}
BuildRequires:  perl(SQL::Statement) >= 1.402
%endif
# Tests
BuildRequires:  perl(blib)
BuildRequires:  perl(B)
BuildRequires:  perl(Benchmark)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Simple) >= 0.90
%if %{with perl_DBI_enables_Clone}
Suggests:       perl(Clone) >= 0.34
%endif
%if %{with perl_DBI_enables_DB_File}
Suggests:       perl(DB_File)
%endif
Requires:       perl(bytes)
Requires:       perl(FileHandle)
Requires:       perl(Math::BigInt)
%if %{with perl_DBI_enables_MLDBM}
Suggests:       perl(MLDBM)
%endif
%if %{with perl_DBI_enables_SQL_Statement}
Suggests:       perl(SQL::Statement) >= 1.402
%endif

# Filter unwanted dependencies
%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(RPC::\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(DBI::db\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(DBI::st\\)

%description 
DBI is a database access Application Programming Interface (API) for
the Perl Language. The DBI API Specification defines a set of
functions, variables and conventions that provide a consistent
database interface independent of the actual database being used.

%if %{with perl_DBI_enables_coro}
%package Coro
Summary:        Asynchronous DBD::Gofer stream transport using Coro

%description Coro
This is an experimental asynchronous DBD::Gofer stream transport for DBI
implemented on top of Coro. The BIG WIN from using Coro is that it enables
the use of existing DBI frameworks like DBIx::Class.
%endif

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
# Optional run-time:
%if %{with perl_DBI_enables_Clone}
Requires:       perl(Clone) >= 0.34
%endif
%if %{with perl_DBI_enables_DB_File}
Requires:       perl(DB_File)
%endif
%if %{with perl_DBI_enables_MLDBM}
Requires:       perl(MLDBM)
%endif
# Do not build-require optional Params::Util to test the fall-back code
%if %{with perl_DBI_enables_SQL_Statement}
Requires:       perl(SQL::Statement) >= 1.402
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n DBI-%{version}
for F in lib/DBD/Gofer.pm; do
    iconv -f ISO-8859-1 -t UTF-8 < "$F" > "${F}.utf8"
    touch -r "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done
# Fix shell bangs
for F in dbixs_rev.pl ex/corogofer.pl; do
    perl -MExtUtils::MakeMaker -e "ExtUtils::MM_Unix->fixin(q{$F})"
done
chmod 0644 ex/*
chmod 0755 dbixs_rev.pl
%if %{without perl_DBI_enables_coro}
rm lib/DBD/Gofer/Transport/corostream.pm
perl -i -ne 'print $_ unless m{^lib/DBD/Gofer/Transport/corostream.pm}' MANIFEST

%endif
# Remove RPC::Pl* reverse dependencies due to security concerns,
# CVE-2013-7284, bug #1051110
for F in lib/Bundle/DBI.pm lib/DBD/Proxy.pm lib/DBI/ProxyServer.pm \
        dbiproxy.PL t/80proxy.t; do
    rm "$F"
    perl -i -ne 'print $_ unless m{^\Q'"$F"'\E}' MANIFEST
done
perl -pi -e 's/"dbiproxy\$ext_pl",//' Makefile.PL
# Remove Win32 specific files to avoid unwanted dependencies
for F in lib/DBI/W32ODBC.pm lib/Win32/DBIODBC.pm; do
    rm "$F"
    perl -i -ne 'print $_ unless m{^\Q'"$F"'\E}' MANIFEST
done

# Help generators to recognize Perl scripts
for F in t/*.t t/*.pl; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" \
  NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} '%{buildroot}'/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
# Remove using of blib
perl -i -ne 'print $_ unless m{^use.*blib/}' %{buildroot}%{_libexecdir}/%{name}/t/1*.t
perl -pi -e 's/\-Mblib=\$getcwd\/blib//' %{buildroot}%{_libexecdir}/%{name}/t/85gofer.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
make test

%files
# Changes already packaged as DBI::Changes
%doc README.md ex/perl_dbi_nulls_test.pl ex/profile.pl
%{_bindir}/dbipro*
%{_bindir}/dbilogstrip
%{perl_vendorarch}/*.p*
%{perl_vendorarch}/DBD/
%if %{with perl_DBI_enables_coro}
%exclude %{perl_vendorarch}/DBD/Gofer/Transport/corostream.pm
%endif
%{perl_vendorarch}/DBI/
%{perl_vendorarch}/auto/DBI/
%{_mandir}/man1/dbi*.1*
%{_mandir}/man3/DBD*.3*
%{_mandir}/man3/DBI*.3*

%if %{with perl_DBI_enables_coro}
%files Coro
%doc ex/corogofer.pl
%{perl_vendorarch}/DBD/Gofer/Transport/corostream.pm
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.647-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.647-3
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.647-2
- Perl 5.42 rebuild

* Mon Jan 20 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.647-1
- 1.647 bump (rhbz#2338980)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.646-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.646-1
- 1.646 bump (rhbz#2337138)

* Tue Sep 03 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.645-1
- 1.645 bump (rhbz#2309389)

* Tue Aug 27 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.644-1
- 1.644 bump (rhbz#2307636)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.643-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-24
- Perl 5.40 re-rebuild of bootstrapped packages

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-23
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.643-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.643-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 26 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-20
- Fix CVE-2014-10401 and CVE-2014-10402

* Tue Sep 19 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-19
- Package tests

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.643-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-17
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-16
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.643-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.643-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-13
- Perl 5.36 re-rebuild of bootstrapped packages

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-12
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.643-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.643-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-9
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-8
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.643-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.643-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-5
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-4
- Perl 5.32 rebuild

* Thu Mar 12 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-3
- Add BR: perl(FileHandle)

* Mon Feb 10 2020 Petr Pisar <ppisar@redhat.com> - 1.643-2
- Build-require blib for tests

* Wed Feb 05 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.643-1
- 1.643 bump

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 1.642-7
- Spec file cleanups: Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMake

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.642-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.642-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.642-4
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.642-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.642-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.642-1
- 1.642 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.641-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.641-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.641-2
- Perl 5.28 rebuild

* Tue Mar 20 2018 Petr Pisar <ppisar@redhat.com> - 1.641-1
- 1.641 bump

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.640-3
- Add build-require gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.640-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.640-1
- 1.640 bump

* Mon Jan 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.639-1
- 1.639 bump

* Thu Aug 17 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.637-1
- 1.637 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.636-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.636-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.636-6
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.636-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.636-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.636-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.636-2
- Perl 5.24 rebuild

* Tue Apr 26 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.636-1
- 1.636 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.634-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 23 2015 Petr Pisar <ppisar@redhat.com> - 1.634-2
- Correct dependency filter

* Tue Aug 04 2015 Petr Pisar <ppisar@redhat.com> - 1.634-1
- 1.634 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.633-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.633-5
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.633-4
- Perl 5.22 rebuild

* Thu Mar 12 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.633-3
- Remove script strip_FAQ.sh from sources

* Mon Mar 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.633-2
- Repackage source tarball to remove non-free DBI/FAQ.pm (bug #1199532)

* Tue Jan 13 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.633-1
- 1.633 bump

* Fri Dec 12 2014 Petr Pisar <ppisar@redhat.com> - 1.632-2
- Improve specification file

* Wed Nov 12 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.632-1
- 1.632 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.631-7
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.631-6
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.631-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.631-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Petr Pisar <ppisar@redhat.com> - 1.631-3
- Remove RPC::Pl* reverse dependencies due to security concerns (CVE-2013-7284)
  (bug #1051110)

* Wed Jan 22 2014 Petr Pisar <ppisar@redhat.com> - 1.631-2
- Split DBD::Gofer::Transport::corostream into sub-package

* Tue Jan 21 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.631-1
- 1.631 bump

* Tue Nov 26 2013 Petr Pisar <ppisar@redhat.com> - 1.630-2
- Add a security warning about use of RPC::PlClient (bug #1030578)

* Tue Oct 29 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.630-1
- 1.630 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.628-3
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.628-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 1.628-1
- 1.628 bump

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1.627-2
- Perl 5.18 rebuild

* Mon May 20 2013 Petr Pisar <ppisar@redhat.com> - 1.627-1
- 1.627 bump

* Thu May 16 2013 Petr Pisar <ppisar@redhat.com> - 1.626-1
- 1.626 bump

* Tue Apr 02 2013 Petr Šabata <contyk@redhat.com> - 1.625-1
- 1.625 bump, perl5.17 fixes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.623-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Petr Šabata <contyk@redhat.com> - 1.623-1
- 1.623 bump

* Mon Aug 27 2012 Petr Pisar <ppisar@redhat.com> - 1.622-6
- Disable Coro properly

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.622-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.622-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 27 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.622-3
- Conditionalize usage of Coro, which is used in experimental module
  and MLDB and SLQ::Statement. 
 
* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.622-2
- Perl 5.16 rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.622-1
- 1.622 bump

* Fri Apr 27 2012 Petr Šabata <contyk@redhat.com> - 1.620-1
- 1.620 bump
- Removing some perl-provided explicit dependencies

* Fri Apr  6 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.618-3
- 810370 apply Paul's bootstrap macro

* Mon Feb 27 2012 Petr Pisar <ppisar@redhat.com> - 1.618-2
- Build-require optional Test::Pod::Coverage

* Mon Feb 27 2012 Petr Pisar <ppisar@redhat.com> - 1.618-1
- 1.618 bump

* Tue Jan 31 2012 Petr Šabata <contyk@redhat.com> - 1.617-1
- 1.617 bump
- Modernize spec
- Remove now obsolete perl(DBI) Provides

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.616-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.616-4
- Perl mass rebuild

* Tue Mar 15 2011 Ville SkyttÃ¤ <ville.skytta@iki.fi> - 1.616-3
- Adapt dependency filtering for rpmbuild >= 4.9.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.616-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan  4 2011 Petr Sabata <psabata@redhat.com> - 1.616-1
- 1.616 version bump

* Wed Sep 29 2010 jkeating - 1.615-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Petr Sabata <psabata@redhat.com> - 1.615-1
- 1.615 version bump

* Mon Sep 20 2010 Petr Sabata <psabata@redhat.com> - 1.614-1
- 1.614 version bump

* Mon Aug  2 2010 Petr Sabata <psabata@redhat.com> - 1.613-1
- 1.613 version bump

* Mon Jun  7 2010 Petr Pisar <ppisar@redhat.com> - 1.611-1
- 1.611 bump
- Add BuildRequires perl(RPC::PlClient) to cover some optional tests
- Fix indentation

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.609-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.609-4
- rebuild against perl 5.10.1

* Thu Sep 24 2009 Stepan Kasal <skasal@redhat.com> - 1.609-3
- provide versioned perl(DBI)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.609-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Stepan Kasal <skasal@redhat.com> - 1.609-1
- new upstream version
- drop unneeded build patch
- move the iconv to convert the source

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.607-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 28 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.607-1
- update

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.601-4
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.601-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.601-2
- rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 1.601-1
- Update to latest CPAN version: 1.601
- Fix some issues from package review:
  - patch to change #! line in script
  - make script executable
  - fix requires and buildrequires

* Mon Aug 27 2007 Robin Norwood <rnorwood@redhat.com> - 1.58-2
- Rebuild

* Mon Aug 13 2007 Robin Norwood <rnorwood@redhat.com> - 1.58-1
- Update to latest CPAN version: 1.58

* Thu Jun 07 2007 Robin Norwood <rnorwood@redhat.com> - 1.56-1
- Update to latest CPAN version: 1.56
- Move the filter requires step into %%prep
- Remove very old patch (for perl 5.8.1)
- Fix a couple of rpmlint issues (non-UTF8 manpage and script with
  incorrect shebang line

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 1.53-1
- Upgrade to latest CPAN version: 1.53

* Thu Aug 24 2006 Robin Norwood <rnorwood@redhat.com> - 1.52-1
- Upgrade to 1.52 for bug #202310
        
* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 1.51-1
- Upgrade to 1.51

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.50-3
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.50-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.50-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.50-2
- rebuild for new perl-5.8.8 / gcc / glibc

* Mon Dec 19 2005 Jason Vas Dias<jvdias@redhat.com> - 1.50-1
- upgrade to 1.50

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Wed Apr 13 2005 Jose Pedro Oliveira <jpo@di.uminho.pt> - 1.48-4
- (#154762)
- License information: GPL or Artistic
- Removed the Time::HiRes building requirement (see Changes)
- Removed the empty .bs file
- Corrected file permissions

* Mon Apr 04 2005 Warren Togami <wtogami@redhat.com> 1.48-3
- filter perl(Apache) (#153673)

* Fri Apr 01 2005 Robert Scheck <redhat@linuxnetz.de> 1.48-2
- spec file cleanup (#153164)

* Thu Mar 31 2005 Warren Togami <wtogami@redhat.com> 1.48-1
- 1.48

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.40-1
- update to 1.40

* Fri Dec 19 2003 Chip Turner <cturner@redhat.com> 1.39-1
- update to 1.39

* Mon Jul  7 2003 Chip Turner <cturner@redhat.com> 1.37-1
- upgrade to 1.37

* Wed Apr  2 2003 Chip Turner <cturner@redhat.com> 1.32-6
- add buildrequires on perl-Time-HiRes

* Tue Feb 18 2003 Chip Turner <cturner@redhat.com>
- update dependency filter to remove dependency on perl(Apache) that
- crept in (#82927)

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Sat Dec 14 2002 Chip Turner <cturner@redhat.com>
- don't use rpm internal dep generator

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild

* Wed Aug  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.30-1
- 1.30. 

* Tue Jun 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.28-1
- 1.28
- Building it also fixes #66304

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.23-2
- Tweak dependency finder - filter out a dependency found within the 
  doc section of a module

* Tue Jun  4 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.23-1
- 1.23
- Some changes to integrate with new Perl
- Update URL

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.21-2
- Rebuild

* Fri Feb 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.21-1
- 1.21

* Fri Feb  8 2002 Chip Turner <cturner@redhat.com>
- filter out "soft" dependencies: perl(RPC::PlClient) and perl(Win32::ODBC)

* Thu Feb  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.201-2
- Rebuild

* Tue Jan 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.201-1
- 1.201

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.20-1
- 1.20
- Proper URL

* Sat Jun 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.18

* Wed May 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.16
- change group to Applications/Databases from Applications/CPAN

* Tue May  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.15

* Tue Feb 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Cleanups

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- build for main distribution
- use %%{_tmppath}
- change name of specfile
- don't use a find script to generate file lists
- general cleanup
- add descriptive summary and description

* Mon Aug 14 2000 Tim Powers <timp@redhat.com>
- Spec file was autogenerated. 
