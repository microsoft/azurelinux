# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-XML-LibXML-Simple
Version:        1.01
Release:        18%{?dist}
Summary:        Read XML strings or files
# Automatically converted from old format: GPL+ or Artistic - review is highly recommended.
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/XML-LibXML-Simple
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MARKOV/XML-LibXML-Simple-%{version}.tar.gz
BuildArch:      noarch
BuildRequires: make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Test::More) >= 0.54
BuildRequires:  perl(XML::LibXML) >= 1.64
Requires:       perl(XML::LibXML) >= 1.64

# drop unversioned Requires on XML::LibXML
%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude|%__requires_exclude|}^perl\\(XML::LibXML\\)$

%description
This Perl module reads XML from strings or files.  It is a blunt rewrite
of XML::Simple (by Grant McLean) to use the XML::LibXML parser for XML
structures, where the original uses plain Perl or SAX parsers.

%prep
%setup -q -n XML-LibXML-Simple-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc ChangeLog README README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 06 2024 Miroslav Suchý <msuchy@redhat.com> - 1.01-16
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-9
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Colin B. Macdonald <cbm@m.fsf.org> - 1.00-2
- Update to 1.01 (#1791320)

* Wed Jan 15 2020 Colin B. Macdonald <cbm@m.fsf.org> - 1.00-1
- Update to 1.00 (#1791320)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.99-6
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.99-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 27 2017 Colin B. Macdonald <cbm@m.fsf.org> - 0.99-1
- Version bump (#1524758)

* Thu Nov 09 2017 Colin B. Macdonald <cbm@m.fsf.org> - 0.98-1
- Version bump (#1511253)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.97-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 23 2016 Colin B. Macdonald <cbm@m.fsf.org> - 0.97-1
- Version bump (#1397143)

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.96-2
- Perl 5.24 rebuild

* Wed Mar 30 2016 Colin B. Macdonald <cbm@m.fsf.org> - 0.96-1
- Version bump (#1317106)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.95-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.95-2
- Perl 5.22 rebuild

* Wed Jun 10 2015 Colin B. Macdonald <cbm@m.fsf.org> 0.95-1
- Version bump

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.94-4
- Perl 5.22 rebuild

* Wed Nov 19 2014 Colin B. Macdonald <cbm@m.fsf.org> 0.94-3
- clean-up following further review.

* Wed Nov 19 2014 Colin B. Macdonald <cbm@m.fsf.org> 0.94-2
- clean-up following review, better summary/description.

* Thu Jun 26 2014 Colin B. Macdonald <cbm@m.fsf.org> 0.94-1
- Specfile autogenerated by cpanspec 1.78.

* Wed Aug 22 2012 Mary Ellen Foster <mefoster@gmail.com> 0.91-1
- Specfile autogenerated by cpanspec 1.78.
