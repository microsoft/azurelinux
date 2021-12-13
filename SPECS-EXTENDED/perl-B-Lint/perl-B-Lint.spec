Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-B-Lint
Version:        1.20
Release:        18%{?dist}
Summary:        Perl lint
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/B-Lint
Source0:        https://cpan.metacpan.org/authors/id/R/RJ/RJBS/B-Lint-%{version}.tar.gz#/perl-B-Lint-%{version}.tar.gz
# Work around for Perl 5.22, bug #1231112, CPAN RT#101115
Patch0:         B-Lint-1.20-Skip-a-bare-sub-test.patch
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  sed
# Run-Time:
BuildRequires:  perl(B) 
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
%if 0%(perl -e 'print $] > 5.017')
BuildRequires:  perl(deprecate)
%endif
BuildRequires:  perl(if)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Module::Pluggable)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
# Tests:
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(O)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(constant)
%if 0%(perl -e 'print $] > 5.017')
Requires:       perl(deprecate)
%endif

%description
The B::Lint module is equivalent to an extended version of the -w option of
perl. It is named after the program lint which carries out a similar process
for C programs.

%prep
%setup -q -n B-Lint-%{version}
%patch0 -p1
# Install into architecture-agnostic path, CPAN RT#83049
sed -i '/PM *=>/,/}/d' Makefile.PL

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
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-12
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Petr Pisar <ppisar@redhat.com> - 1.20-4
- Work around an incompatibility with Perl 5.22 (bug #1231112)

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-3
- Perl 5.22 rebuild

* Wed Oct 29 2014 Petr Pisar <ppisar@redhat.com> - 1.20-2
- Do not build-require version module

* Mon Oct 27 2014 Petr Pisar <ppisar@redhat.com> - 1.20-1
- 1.20 bump

* Tue Sep 30 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.18-1
- 1.18 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.17-293
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-292
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1.17-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.17-3
- Perl 5.18 rebuild

* Tue May 28 2013 Petr Pisar <ppisar@redhat.com> - 1.17-2
- Correct typo in dependencies

* Wed Jan 30 2013 Petr Pisar <ppisar@redhat.com> 1.17-1
- Specfile autogenerated by cpanspec 1.78.
