# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Unicode-String
Version:        2.10
Release:        32%{?dist}

Summary:        Perl modules to handle various Unicode issues

# in CharName.pm is mentioned use of Unicode table, but fonts are not used
# so here can't be UCD license
# in String.xs is mentioned "same terms as Perl itself" which is this
# Automatically converted from old format: GPL+ or Artistic - review is highly recommended.
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Unicode-String
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAAS/Unicode-String-%{version}.tar.gz
Patch0:         perl-Unicode-String-2.09-utf8doc.patch

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Test)
# not detected by auto provide scripts:
Requires:       perl(MIME::Base64)

%{?perl_default_filter}

%description
%{summary}.


%prep
%setup -q -n Unicode-String-%{version}

# Recode documentation as UTF-8
# Can't just use iconv because README includes an example of
# character code conversion that would be wrong if simply recoded
%patch -P0 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"


%install
make install \
  DESTDIR=$RPM_BUILD_ROOT \
  INSTALLARCHLIB=$RPM_BUILD_ROOT%{perl_archlib}
find $RPM_BUILD_ROOT -type f \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -empty -exec rmdir {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%files
%doc Changes README
%{perl_vendorarch}/auto/Unicode
%{perl_vendorarch}/Unicode
%{_mandir}/man3/*.3*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-31
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 06 2024 Miroslav Suchý <msuchy@redhat.com> - 2.10-29
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-27
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-23
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-20
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-17
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-14
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-11
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-8
- Perl 5.28 rebuild

* Tue Mar 13 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 2.10-7
- Add missing build-requirements

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Sep 10 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 2.10-1
- Update to 2.10
- Drop upstreamed patch
- Truncate changelog entry

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-37
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-34
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-33
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.09-29
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-27
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 2.09-25
- Perl 5.16 rebuild

* Sun Jun 24 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 2.09-24
- Really add the patch

* Sun Jun 24 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 2.09-23
- Add patch to suppress warnings (#834867)
- Clean up spec file

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.09-22
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Iain Arnell <iarnell@gmail.com> 2.09-20
- use perl_default_filter

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.09-19
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.09-17
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Jul 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.09-16
- apply ppisar hints from 558743

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.09-15
- Mass rebuild with perl-5.12.0

* Thu Feb 18 2010 Paul Howarth <paul@city-fan.org> - 2.09-14
- carefully convert documentation to UTF-8 encoding
- add :MODULE_COMPAT_* dependency

* Wed Feb 17 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.09-13
- fix license

* Tue Jan 26 2010 Stepan Kasal <skasal@redhat.com> - 2.09-12
- better buildroot
- no need to define perl_vendorarch

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun 05 2008 Aurelien Bompard <abompard@fedoraproject.org> 2.09-9
- fix build

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.09-8
- Rebuild for perl 5.10 (again)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.09-7
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.09-6
- rebuild for new perl

* Thu Sep 27 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.09-5
- fix license tag again (thanks Tom)

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.09-4
- fix license tag (like perl itself)

* Mon Aug 13 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.09-3
- BR: perl-devel

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 2.09-2
- rebuild

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 2.09-1
- version 2.09

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 2.07-6
- rebuild for FC5
