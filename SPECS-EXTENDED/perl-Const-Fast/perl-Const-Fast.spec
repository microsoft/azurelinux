# Perform optional tests
%bcond_without perl_Const_Fast_enables_optional_test

Name:           perl-Const-Fast
Version:        0.014
Release:        21%{?dist}
Summary:        Facility for creating read-only scalars, arrays, and hashes
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Const-Fast
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/Const-Fast-%{version}.tar.gz#/perl-Const-Fast-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8
BuildRequires:  perl(Module::Build::Tiny) >= 0.021
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable)
BuildRequires:  perl(strict)
BuildRequires:  perl(Sub::Exporter::Progressive) >= 0.001007
BuildRequires:  perl(warnings)
# Tests
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
%if %{with perl_Const_Fast_enables_optional_test}
# Optional tests
# Pod::Coverage::TrustPod not used
# Test::Pod not used
# Test::Pod::Coverage not used
BuildRequires:  perl(Test::Script) >= 1.05
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
This the only function of this module and it is exported by default. It takes
a scalar, array or hash left-value as first argument, and a list of one or
more values depending on the type of the first argument as the value for the
variable. It will set the variable to that value and subsequently make it
read-only. Arrays and hashes will be made deeply read-only.


%prep
%setup -q -n Const-Fast-%{version}


%build
perl Build.PL --installdirs vendor
./Build


%install
./Build install --destdir $RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -delete
%{_fixperms} $RPM_BUILD_ROOT/*


%check
unset RELEASE_TESTING
./Build test


%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.014-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Petr Pisar <ppisar@redhat.com> - 0.014-19
- Correct dependencies

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-17
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-14
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-11
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-9
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.014-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-6
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.014-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.014-2
- Perl 5.18 rebuild

* Sun Jun 02 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.014-1
- Update to 0.014
- Drop the Group declaration
- Switch to Module::Build::Tiny as building mecanism

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 06 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 0.013-1
- Update to 0.013
- Add perl default filter

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.011-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.011-2
- Perl 5.16 rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.011-1
- 0.011 bump

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.006-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.006-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 08 2010 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> 0.006-1
- Specfile autogenerated by cpanspec 1.78.
