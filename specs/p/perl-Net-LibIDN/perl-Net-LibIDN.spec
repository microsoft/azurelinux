# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkgname Net-LibIDN

Summary:        Perl bindings for GNU LibIDN
Name:           perl-Net-LibIDN
Version:        0.12
Release: 55%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/%{pkgname}
Source:         https://cpan.metacpan.org/authors/id/T/TH/THOR/%{pkgname}-%{version}.tar.gz
# Use distribution CFLAGS for tests, bug #1242794, CPAN RT#105853
Patch0:         Net-LibIDN-0.12-Respect-Config-s-cc-ccflags-and-ldflags.patch
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libidn-devel >= 0.4.0
BuildRequires:  perl-interpreter >= 5.8.0
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Getopt::Long)
# Run-time:
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Tests:
BuildRequires:  perl(Test)

# Filter the Perl extension module
%{?perl_default_filter}

%description
Provides perl bindings for GNU Libidn, a C library for handling
Internationalized Domain Names according to IDNA (RFC 3490), in
a way very much inspired by Turbo Fredriksson's PHP-IDN.

%prep
%setup -q -n %{pkgname}-%{version}
%patch -P0 -p1
# Change man page encoding into UTF-8
for F in _LibIDN.pm; do
    iconv -f latin1 -t utf-8 < "$F" > "${F}.utf"
    sed -i -e '/^=encoding\s/ s/latin1/utf-8/' "${F}.utf"
    touch -r "$F" "${F}.utf"
    mv "${F}.utf" "$F"
done;

%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} +
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} +
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%license Artistic
%doc Changes README
%{_mandir}/man3/*.3pm*
%{perl_vendorarch}/Net
%{perl_vendorarch}/auto/Net

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-53
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-50
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-46
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-43
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-40
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-37
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-34
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-31
- Perl 5.28 rebuild

* Tue May 15 2018 Paul Howarth <paul@city-fan.org> - 0.12-30
- Rebuild for libidn 1.35

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-26
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-24
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 14 2015 Petr Pisar <ppisar@redhat.com> - 0.12-22
- Use distribution CFLAGS for Makefile.PL's tests (bug #1242794)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-20
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-19
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.12-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Petr Pisar <ppisar@redhat.com> - 0.12-13
- Modernize spec file

* Mon Aug 13 2012 Petr Pisar <ppisar@redhat.com> - 0.12-12
- Build-require Carp

* Mon Aug 13 2012 Petr Pisar <ppisar@redhat.com> - 0.12-11
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 0.12-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-5
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.12-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 03 2009 Robert Scheck <robert@fedoraproject.org> 0.12-1
- Upgrade to 0.12

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 0.11-2
- Rebuilt against gcc 4.4 and rpm 4.6

* Sun Jan 25 2009 Robert Scheck <robert@fedoraproject.org> 0.11-1
- Upgrade to 0.11

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-2
- Rebuild for new perl

* Sun Feb 10 2008 Robert Scheck <robert@fedoraproject.org> 0.10-1
- Upgrade to 0.10

* Wed Aug 29 2007 Robert Scheck <robert@fedoraproject.org> 0.09-4
- Updated the license tag according to the guidelines

* Mon May 07 2007 Robert Scheck <robert@fedoraproject.org> 0.09-3
- Rebuild

* Thu Apr 26 2007 Robert Scheck <robert@fedoraproject.org> 0.09-2
- Added build requirement to perl(ExtUtils::MakeMaker)

* Sun Sep 03 2006 Robert Scheck <robert@fedoraproject.org> 0.09-1
- Upgrade to 0.0.9 and rebuild for Fedora Core 6

* Fri Jun 23 2006 Robert Scheck <robert@fedoraproject.org> 0.08-5
- Changes to match with Fedora Packaging Guidelines (#193960)

* Sun Dec 25 2005 Robert Scheck <robert@fedoraproject.org> 0.08-4
- Rebuilt against gcc 4.1 and libidn 0.6.0

* Fri Apr 01 2005 Robert Scheck <robert@fedoraproject.org> 0.08-3
- Some spec file cleanup

* Mon Mar 14 2005 Robert Scheck <robert@fedoraproject.org> 0.08-2
- Rebuilt against gcc 4.0

* Thu Jan 20 2005 Robert Scheck <robert@fedoraproject.org> 0.08-1
- Upgrade to 0.0.8

* Sun Oct 03 2004 Robert Scheck <robert@fedoraproject.org> 0.07-2
- Use perl(:MODULE_COMPAT_*) as requirement for perl
- Lots of spec file cleanups

* Mon May 24 2004 Robert Scheck <robert@fedoraproject.org> 0.07-1
- Upgrade to 0.0.7

* Mon Apr 05 2004 Robert Scheck <robert@fedoraproject.org> 0.06-1
- Upgrade to 0.0.6
- Initial spec file for Red Hat Linux and Fedora Core
