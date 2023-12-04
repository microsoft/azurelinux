Summary:        RPM Perl dependencies generators
Name:           perl-generators
Version:        1.15
Release:        1%{?dist}
License:        GPL+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://jplesnik.fedorapeople.org/generators
Source0:        %{url}/generators-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        LICENSE.PTR

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  sed
%if %{with_check}
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Fedora::VSP)
BuildRequires:  perl(Test::More)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Per Perl packaging guidelines, build-requiring perl-generators should
# deliver Perl macros
%if %{defined perl_bootstrap}
# Supply run-time dependencies manually when perl-generators is not available
Requires:       perl(Fedora::VSP)
%endif

BuildArch:      noarch

%description
This package provides RPM Perl dependencies generators which are used for
getting provides and requires from Perl binaries and modules.

%prep
%autosetup -n generators-%{version}
cp %{SOURCE1} .

%build
perl Makefile.PL \
    INSTALLDIRS=vendor \
    INSTALLVENDORSCRIPT=%{_rpmconfigdir} \
    NO_PACKLIST=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

mkdir -p %{buildroot}%{_rpmconfigdir}/fileattrs/
install -p -m 644 fileattrs/* '%{buildroot}%{_rpmconfigdir}/fileattrs'

%check
make test

%files
%license LICENSE.PTR
%doc Changes TODO
%{_rpmconfigdir}/perl.*
%{_rpmconfigdir}/fileattrs/perl*.attr

%changelog
* Mon Nov 27 2023 Andrew Phelps <anphel@microsoft.com> - 1.15-1
- Upgrade to version 1.15

* Mon Aug 01 2022 Muhammad Falak <mwani@microsoft.com> - 1.11-9
- Add BR on `perl(Fedora::VSP)` to fix ptest build

* Fri Apr 01 2022 Andrew Phelps <anphel@microsoft.com> - 1.11-8
- Fix perl BR

* Tue Mar 20 2022 Muhammad Falak <mwani@microsoft.com> - 1.11-7
- Add an explicit BR on `perl{(ExtUtils::MakeMaker), (Test::More)}` to fix ptest build

* Mon Aug 30 2021 Bala <balakumaran.kannan@microsoft.com> - 1.11-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-2
- Perl 5.30 rebuild

* Thu May 23 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-1
- 1.11 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-9
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-8
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 1.10-5
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 12 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-1
- 1.10 bump

* Thu Jun 23 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.09-1
- 1.09 bump

* Wed Jun 15 2016 Petr Pisar <ppisar@redhat.com> - 1.08-4
- Run-require perl-macros to provide the Perl macros for building Perl packages

* Wed Jun 01 2016 Petr Pisar <ppisar@redhat.com> - 1.08-3
- Supply run-time depenencies manually when perl-generators is not available on
  bootstrap

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-2
- Perl 5.24 rebuild

* Mon Mar 21 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-1
- 1.08 bump; Resolves BZ#1318658

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-2
- Add epoch to perl BR

* Tue Oct 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-1
- 1.07 bump
- Return perl version as normalized perl(:VERSION) symbol

* Tue Oct 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-1
- 1.06 bump

* Tue Sep 29 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-1
- 1.05 bump
- Resolves: bug #1267267

* Wed Jul 29 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-1
- 1.04 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-2
- Perl 5.22 rebuild

* Mon Feb 02 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-1
- 1.03 bump
- Update parcing of here-doc and quoted section

* Fri Dec 12 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.02-1
- 1.02 bump

* Tue Oct 21 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-1
- 1.01 bump

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-2
- Perl 5.20 rebuild

* Mon Jun 16 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-1
- Introduce Perl generators as a standalone package
