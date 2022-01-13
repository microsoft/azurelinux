Name:           perl-MIME-Charset
Version:        1.012.2
Release:        12%{?dist}
Summary:        Charset Informations for MIME
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/MIME-Charset
Source0:        https://cpan.metacpan.org/authors/id/N/NE/NEZUMI/MIME-Charset-%{version}.tar.gz#/perl-MIME-Charset-%{version}.tar.gz
# Disable Module::AutoInstall
Patch0:         MIME-Charset-1.012-Do-not-install-modules-from-the-Internet.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(FindBin)
BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl(Module::Install::Metadata)
BuildRequires:  perl(Module::Install::Win32)
BuildRequires:  perl(Module::Install::WriteAll)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Encode::Encoding)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Optional run-time:
# Encode::JISX0213 0.03 not yet packaged
# Encode::HanExtra 0.20 not needed at tests
BuildRequires:  perl(Encode::EUCJPASCII) >= 0.02
# Tests:
# Encode::CN not used
# Encode::JP not used
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  sed
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Filter under-specified symbols
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(MIME::Charset\\)$

%description
MIME::Charset provides information about character sets used for MIME
messages on Internet.

%prep
%setup -q -n MIME-Charset-%{version}
%patch0 -p1
# Remove bundled modules
rm -rf ./inc
sed -i -e '/^inc\//d' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%license ARTISTIC COPYING
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Jan 13 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.012.2-12
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.012.2-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.012.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.012.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.012.2-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.012.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.012.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.012.2-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.012.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.012.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.012.2-2
- Perl 5.26 rebuild

* Fri Apr 14 2017 Xavier Bachelot <xavier@bachelot.org> - 1.012.2-1
- Update to 1.012.2.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.012-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.012-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 25 2015 Petr Pisar <ppisar@redhat.com> - 1.012-1
- 1.012 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.011.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.011.1-4
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.011.1-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.011.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 16 2013 Xavier Bachelot <xavier@bachelot.org> 1.011.1-1
- Update to 1.011.1.

* Wed Aug 28 2013 Xavier Bachelot <xavier@bachelot.org> 1.010.1-1
- Update to 1.010.1.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 1.010-2
- Perl 5.18 rebuild

* Wed Apr 10 2013 Xavier Bachelot <xavier@bachelot.org> 1.010-1
- Update to 1.010.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.009.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.009.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.009.2-2
- Perl 5.16 rebuild

* Mon Jun 04 2012 Xavier Bachelot <xavier@bachelot.org> 1.009.2-1
- Update to 1.009.2.

* Fri Jan 06 2012 Xavier Bachelot <xavier@bachelot.org> 1.009.1-5
- Add BR: for perl(Encode::EUCJPASCII) for better test coverage.

* Wed Dec 21 2011 Xavier Bachelot <xavier@bachelot.org> 1.009.1-4
- Add BR: for perl(Encode::JIS2K) and perl(Encode::HanExtra) for better test
  coverage.

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.009.1-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.009.1-2
- Perl mass rebuild

* Fri Jul 08 2011 Xavier Bachelot <xavier@bachelot.org> 1.009.1-1
- Update to 1.009.1.

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.008.2-2
- Perl mass rebuild

* Mon May 30 2011 Xavier Bachelot <xavier@bachelot.org> 1.008.2-1
- Update to 1.008.2.

* Thu May 12 2011 Xavier Bachelot <xavier@bachelot.org> 1.008.1-1
- Update to 1.008.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.008-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Dec 14 2010 Xavier Bachelot <xavier@bachelot.org> 1.008-1
- Update to 1.008.
- Update Source0 URL.
- More BRs for better tests coverage.

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.006.2-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.006.2-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.006.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 28 2009 Xavier Bachelot <xavier@bachelot.org> 1.006.2-2
- Filter duplicate Provides:.

* Fri Apr 24 2009 Xavier Bachelot <xavier@bachelot.org> 1.006.2-1
- Specfile autogenerated by cpanspec 1.77.
- Fix license.
