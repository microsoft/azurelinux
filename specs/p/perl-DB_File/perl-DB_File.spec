# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_DB_File_enables_optional_test
%else
%bcond_with perl_DB_File_enables_optional_test
%endif

Name:           perl-DB_File
Version:        1.859
Release:        516%{?dist}
Summary:        Perl5 access to Berkeley DB version 1.x
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/DB_File
Source0:        https://cpan.metacpan.org/authors/id/P/PM/PMQS/DB_File-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  libdb-devel
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::Constant)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# File::Copy not needed if ExtUtils::Constant is available
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Carp)
# DynaLoader not needed if XSLoader is available
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(lib)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
%if %{with perl_DB_File_enables_optional_test} && !%{defined perl_bootstrap}
# Optional tests:
# Data::Dumper not useful
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::CPAN::Meta)
BuildRequires:  perl(Test::CPAN::Meta::JSON)
%endif
Requires:       perl(Fcntl)
Requires:       perl(XSLoader)

%{?perl_default_filter}

%description
DB_File is a module which allows Perl programs to make use of the facilities
provided by Berkeley DB version 1.x (if you have a newer version of DB, you
will be limited to functionality provided by interface of version 1.x). The
interface defined here mirrors the Berkeley DB interface closely.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(threads)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n DB_File-%{version}
find -type f -exec chmod -x {} +
perl -MConfig -pi -e 's|^#!.*perl|$Config{startperl}|' dbinfo

# Help file to recognise the Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
# Remove author tests
rm %{buildroot}%{_libexecdir}/%{name}/t/pod.t
rm %{buildroot}%{_libexecdir}/%{name}/t/meta-*.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset PERL_CORE
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes dbinfo README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/DB_File*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.859-516
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.859-515
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.859-514
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.859-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.859-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.859-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.859-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.859-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.859-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 23 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.859-1
- 1.859 bump (rhbz#2233072)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.858-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.858-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.858-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.858-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.858-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.858-3
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.858-2
- Perl 5.36 rebuild

* Fri May 13 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.858-1
- 1.858 bump

* Mon Feb 28 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.857-1
- 1.857 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.856-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.856-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.856-1
- 1.856 bump
- Package tests

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.855-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.855-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.855-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 14 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.855-1
- 1.855 bump

* Wed Sep 16 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.854-1
- 1.854 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.853-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.853-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.853-456
- Increase release to favour standalone package

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.853-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Petr Pisar <ppisar@redhat.com> - 1.853-1
- 1.853 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.852-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.852-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.852-2
- Perl 5.30 rebuild

* Tue Apr 23 2019 Petr Pisar <ppisar@redhat.com> - 1.852-1
- 1.852 bump

* Fri Apr 05 2019 Petr Pisar <ppisar@redhat.com> - 1.851-1
- 1.851 bump

* Wed Apr 03 2019 Petr Pisar <ppisar@redhat.com> - 1.850-1
- 1.850 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.843-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 05 2018 Petr Pisar <ppisar@redhat.com> - 1.843-1
- 1.843 bump

* Mon Jul 16 2018 Petr Pisar <ppisar@redhat.com> - 1.842-1
- 1.842 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.841-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.841-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.841-2
- Perl 5.28 rebuild

* Tue Apr 03 2018 Petr Pisar <ppisar@redhat.com> - 1.841-1
- 1.841 bump

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.840-398
- Add build-require gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.840-397
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.840-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.840-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.840-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.840-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.840-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Petr Pisar <ppisar@redhat.com> - 1.840-1
- 1.840 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.838-2
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Petr Pisar <ppisar@redhat.com> - 1.838-1
- 1.838 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.835-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.835-348
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.835-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.835-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.835-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.835-2
- Perl 5.22 rebuild

* Fri Jan 02 2015 Petr Pisar <ppisar@redhat.com> - 1.835-1
- 1.835 bump

* Thu Dec 11 2014 Petr Pisar <ppisar@redhat.com> - 1.834-1
- 1.834 bump

* Wed Dec 10 2014 Petr Pisar <ppisar@redhat.com> - 1.833-1
- 1.833 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.831-311
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.831-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.831-7
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.831-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Petr Pisar <ppisar@redhat.com> - 1.831-5
- Build-require Test::More always because of the new thread tests

* Thu Aug 07 2014 Petr Pisar <ppisar@redhat.com> - 1.831-4
- Initialize db_DESTROY return variable (bug #1107732)

* Thu Aug 07 2014 Petr Pisar <ppisar@redhat.com> - 1.831-3
- Destroy DB_File objects only from original thread context (bug #1107732)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.831-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 19 2013 Petr Pisar <ppisar@redhat.com> - 1.831-1
- 1.831 bump

* Mon Nov 04 2013 Petr Pisar <ppisar@redhat.com> - 1.830-1
- 1.830 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.829-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.829-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.829-2
- Perl 5.18 rebuild

* Wed Jul 10 2013 Petr Pisar <ppisar@redhat.com> - 1.829-1
- 1.829 bump

* Thu May 09 2013 Petr Pisar <ppisar@redhat.com> - 1.828-1
- 1.828 bump

* Thu Mar 21 2013 Petr Pisar <ppisar@redhat.com> 1.827-1
- Specfile autogenerated by cpanspec 1.78.
