# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-utf8-all
Version:        0.024
Release:        25%{?dist}
Summary:        Turn on Unicode everywhere
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/utf8-all
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAYOBAAN/utf8-all-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(charnames)
BuildRequires:  perl(Config)
BuildRequires:  perl(Encode)
BuildRequires:  perl(feature)
BuildRequires:  perl(Import::Into)
BuildRequires:  perl(open)
BuildRequires:  perl(parent)
BuildRequires:  perl(PerlIO::utf8_strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(utf8)
# Tests:
BuildRequires:  perl(autodie)
BuildRequires:  perl(blib)
BuildRequires:  perl(constant)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(locale)
BuildRequires:  perl(PerlIO)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(version) >= 0.77
# Dependencies:

%description
Pragma utf8 allows you to write your Perl encoded in UTF-8. That means UTF-8
strings, variable names, and regular expressions. utf8::all goes further, and
makes @ARGV encoded in UTF-8, and file handles are opened with UTF-8 encoding
turned on by default (including STDIN, STDOUT, STDERR), and character names
are imported so \N{...} sequences can be used to compile Unicode characters
based on names. If you don't want UTF-8 for a particular file handle, you'll
have to set binmode $filehandle.

%prep
%setup -q -n utf8-all-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -delete
%{_fixperms} -c $RPM_BUILD_ROOT

%check
make test

%files
%license LICENSE
%doc Changes README.mkdn
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Oct 29 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.024-18
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.024-16
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.024-13
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.024-10
- Perl 5.32 rebuild

* Tue Mar 10 2020 Paul Howarth <paul@city-fan.org> - 0.024-9
- BR: perl(blib) for t/00-compile.t

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.024-6
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.024-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.024-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan  5 2018 Paul Howarth <paul@city-fan.org> - 0.024-1
- 0.024 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.023-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.023-2
- Perl 5.26 rebuild

* Mon May 29 2017 Paul Howarth <paul@city-fan.org> - 0.023-1
- 0.023 bump

* Sun Apr 23 2017 Paul Howarth <paul@city-fan.org> - 0.022-1
- 0.022 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.021-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 02 2016 Petr Pisar <ppisar@redhat.com> - 0.021-1
- 0.021 bump

* Mon Aug 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.020-1
- 0.020 bump

* Thu Aug 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.019-1
- 0.019 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.017-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.017-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Petr Pisar <ppisar@redhat.com> - 0.017-1
- 0.017 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.016-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.016-2
- Perl 5.22 rebuild

* Mon Jan 19 2015 Petr Pisar <ppisar@redhat.com> - 0.016-1
- 0.016 bump

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.015-2
- Perl 5.20 rebuild

* Fri Aug 29 2014 Petr Pisar <ppisar@redhat.com> - 0.015-1
- 0.015 bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-2
- Perl 5.20 rebuild

* Fri Aug 22 2014 Petr Pisar <ppisar@redhat.com> - 0.013-1
- 0.013 bump

* Tue Aug 05 2014 Petr Pisar <ppisar@redhat.com> - 0.012-1
- 0.012 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Petr Pisar <ppisar@redhat.com> - 0.011-1
- 0.011 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 29 2013 Petr Pisar <ppisar@redhat.com> - 0.010-2
- Perl 5.18 rebuild

* Thu Feb 14 2013 Petr Pisar <ppisar@redhat.com> 0.010-1
- Specfile autogenerated by cpanspec 1.78.
