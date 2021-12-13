Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Mozilla-CA
# You do not need to back-port a new version for updating a list of the
# certificates. They are taken from ca-certificates package instead
# per bug #738383.
Version:        20200520
Release:        2%{?dist}
Summary:        Mozilla's CA certificate bundle in PEM format
# README:                       MPLv2.0
## Unbundled
# mk-ca-bundle.pl:              MIT
# lib/Mozilla/CA/cacert.pem:    MPLv2.0
License:        MPLv2.0
URL:            https://metacpan.org/release/Mozilla-CA
Source0:        https://cpan.metacpan.org/authors/id/A/AB/ABH/Mozilla-CA-%{version}.tar.gz#/perl-Mozilla-CA-%{version}.tar.gz
# Use a CA bundle from ca-certificates package, bug #738383
Patch0:         Mozilla-CA-20200520-Redirect-to-ca-certificates-bundle.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  ca-certificates
BuildRequires:  perl(strict)
BuildRequires:  perl(File::Spec)
# Tests:
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       ca-certificates

%description
Mozilla::CA provides a path to ca-certificates copy of Mozilla's bundle of
certificate authority certificates in a form that can be consumed by modules
and libraries based on OpenSSL.

%prep
%setup -q -n Mozilla-CA-%{version}
%patch0 -p1
# Remove a bundled CA bundle for sure
rm lib/Mozilla/CA/cacert.pem
# Do not distribute Mozilla downloader, we take certificates from
# ca-certificates package
rm mk-ca-bundle.pl
perl -i -ne 'print $_ unless m{^mk-ca-bundle\.pl$}' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200520-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed May 20 2020 Petr Pisar <ppisar@redhat.com> - 20200520-1
- 20200520 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20180117-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180117-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 20180117-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180117-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180117-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 20180117-2
- Perl 5.28 rebuild

* Fri Mar 02 2018 Petr Pisar <ppisar@redhat.com> - 20180117-1
- 20180117 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20160104-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160104-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 20160104-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160104-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 20160104-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20160104-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Petr Pisar <ppisar@redhat.com> - 20160104-1
- 20160104 bump

* Wed Aug 26 2015 Petr Pisar <ppisar@redhat.com> - 20150826-1
- 20150826 bump
- License changed from (MPLv1.1 or LGPLv2+ or GPLv2+) to (MPLv2.0)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20141217-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 20141217-2
- Perl 5.22 rebuild

* Fri Jan 02 2015 Petr Pisar <ppisar@redhat.com> - 20141217-1
- 20141217 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 20130114-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130114-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 16 2014 Petr Pisar <ppisar@redhat.com> - 20130114-5
- Specify all dependencies

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130114-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 20130114-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130114-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Petr Pisar <ppisar@redhat.com> - 20130114-1
- 20130114 bump

* Thu Aug 23 2012 Petr Pisar <ppisar@redhat.com> - 20120823-1
- 20120823 bump

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 20120822-1
- 20120822 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120309-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 20120309-2
- Perl 5.16 rebuild

* Wed Mar 14 2012 Petr Pisar <ppisar@redhat.com> - 20120309-1
- 20120309 bump

* Wed Jan 18 2012 Petr Pisar <ppisar@redhat.com> - 20120118-1
- 20120118 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20111025-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 25 2011 Petr Pisar <ppisar@redhat.com> - 20111025-1
- 20111025 bump
- Remove defattr from spec code

* Fri Sep 16 2011 Petr Pisar <ppisar@redhat.com> - 20110914-2
- Redirect to ca-certificates bundle (bug #738383)

* Thu Sep 15 2011 Petr Pisar <ppisar@redhat.com> - 20110914-1
- 20110914 bump

* Mon Sep 05 2011 Petr Pisar <ppisar@redhat.com> - 20110904-1
- 20110904 bump

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 20110409-2
- Perl mass rebuild

* Mon Apr 11 2011 Petr Pisar <ppisar@redhat.com> - 20110409-1
- 20110409 bump

* Mon Mar 28 2011 Petr Pisar <ppisar@redhat.com> 20110301-1
- Specfile autogenerated by cpanspec 1.78.
- Correct License tag
- Remove BuildRoot stuff
