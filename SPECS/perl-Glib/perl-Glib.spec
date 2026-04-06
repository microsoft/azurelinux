# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Glib_enables_optional_test
%else
%bcond_with perl_Glib_enables_optional_test
%endif

Name:           perl-Glib
Version:        1.3294
Release:        8%{?dist}
Summary:        Perl interface to GLib
License:        LGPL-2.1-or-later
URL:            https://metacpan.org/release/Glib
Source0:        https://cpan.metacpan.org/authors/id/X/XA/XAOC/Glib-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  glibc-common
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.0
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::Depends) >= 0.300
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(ExtUtils::PkgConfig) >= 1.00
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
# Config not used by tests
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
# Gtk2 not used and optional
BuildRequires:  perl(IO::File)
BuildRequires:  perl(overload)
# POSIX not used by tests
BuildRequires:  perl(Storable)
BuildRequires:  perl(vars)
# Tests
BuildRequires:  perl(Config)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(utf8)
# Optional tests:
%if %{with perl_Glib_enables_optional_test}
BuildRequires:  perl(I18N::Langinfo)
BuildRequires:  perl(Test::ConsistentVersion)
%endif
Requires:       perl(Config)

# Do not export private modules and libraries
%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(MY\\)

%description
This module provides perl access to GLib and GLib's GObject libraries.
GLib is a portability and utility library; GObject provides a generic
type system with inheritance and a powerful signal system.  Together
these libraries are used as the foundation for many of the libraries
that make up the Gnome environment, and are used in many unrelated
projects.

%package devel
Summary:    Development part of Perl interface to GLib
Requires:   %{name} = %{version}-%{release}

%description devel
Development part of package perl-Glib, the Perl module providing interface
to GLib and GObject libraries.

%prep
%setup -q -n Glib-%{version}
for F in AUTHORS; do
    iconv -f ISO-8859-1 -t UTF-8 < "$F" > "${F}.utf8"
    touch -r "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" \
    NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -delete
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%license LICENSE
%doc AUTHORS ChangeLog.pre-git NEWS README TODO
%{perl_vendorarch}/auto/Glib/
%{perl_vendorarch}/Glib*
%{_mandir}/man3/*.3pm*
%exclude %{perl_vendorarch}/Glib/*/*.h
%exclude %{perl_vendorarch}/Glib/MakeHelper.pm
%exclude %{perl_vendorarch}/Glib/devel.pod
%exclude %{perl_vendorarch}/Glib/xsapi.pod
%exclude %{_mandir}/man3/Glib::MakeHelper.3pm.gz
%exclude %{_mandir}/man3/Glib::devel.3pm.gz
%exclude %{_mandir}/man3/Glib::xsapi.3pm.gz

%files devel
%{perl_vendorarch}/Glib/*/*.h
%{perl_vendorarch}/Glib/MakeHelper.pm
%{perl_vendorarch}/Glib/devel.pod
%{perl_vendorarch}/Glib/xsapi.pod
%{_mandir}/man3/Glib::MakeHelper.3pm.gz
%{_mandir}/man3/Glib::devel.3pm.gz
%{_mandir}/man3/Glib::xsapi.3pm.gz

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3294-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.3294-7
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3294-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3294-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.3294-4
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3294-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3294-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 24 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.3294-1
- 1.3294 bump (rhbz#2235632)
- Update license to SPDX format

* Tue Aug 1 2023 Tom Callaway <spot@fedoraproject.org> - 1.3293-13
- fix issue with comment check and glib 2.77+ (thanks to Petr Pisar)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3293-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.3293-11
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3293-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3293-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.3293-8
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3293-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3293-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.3293-5
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3293-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3293-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.3293-2
- Perl 5.32 rebuild

* Wed Jun 10 2020 Tom Callaway <spot@fedoraproject.org> - 1.3293-1
- update to 1.3293

* Tue Feb 18 2020 Tom Callaway <spot@fedoraproject.org> - 1.3292-1
- update to 1.3292

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3291-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 27 2019 Tom Callaway <spot@fedoraproject.org> - 1.3291-1
- update to 1.3291

* Mon Jul 29 2019 Tom Callaway <spot@fedoraproject.org> - 1.329-4
- adjust linebreaks patch to do runtime version checking

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.329-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.329-2
- Perl 5.30 rebuild

* Wed Feb  6 2019 Tom Callaway <spot@fedoraproject.org> - 1.329-1
- update to 1.329

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.328-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan  4 2019 Tom Callaway <spot@fedoraproject.org> - 1.328-2
- fix t/g.t for new comment parsing in glib2 2.59.0 (bz1663499)

* Thu Oct  4 2018 Tom Callaway <spot@fedoraproject.org> - 1.328-1
- update to 1.328

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.327-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.327-2
- Perl 5.28 rebuild

* Tue May 22 2018 Tom Callaway <spot@fedoraproject.org> - 1.327-1
- update to 1.327

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.326-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.326-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.326-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Tom Callaway <spot@fedoraproject.org> - 1.326-1
- update to 1.326

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.325-2
- Perl 5.26 rebuild

* Tue May 23 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.325-1
- Update to 1.325

* Thu May 18 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.324-3
- Fix building on Perl without '.' in @INC

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.324-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan  3 2017 Tom Callaway <spot@fedoraproject.org> - 1.324-1
- update to 1.324

* Thu Sep 29 2016 Tom Callaway <spot@fedoraproject.org> - 1.323-1
- update to 1.323

* Fri Aug 26 2016 Tom Callaway <spot@fedoraproject.org> - 1.322-1
- update to 1.322

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.321-2
- Perl 5.24 rebuild

* Tue Feb  2 2016 Tom Callaway <spot@fedoraproject.org> - 1.321-1
- update to 1.321

* Fri Jan 15 2016 Tom Callaway <spot@fedoraproject.org> - 1.320-1
- update to 1.320

* Tue Oct 13 2015 Tom Callaway <spot@fedoraproject.org> - 1.314-1
- 1.314

* Fri Sep 11 2015 Tom Callaway <spot@fedoraproject.org> - 1.313-1
- 1.313 

* Tue Jul 21 2015 Petr Pisar <ppisar@redhat.com> - 1.312-1
- 1.312 bump

* Wed Jul 15 2015 Tom Callaway <spot@fedoraproject.org> - 1.311-1
- update to 1.311

* Tue Jun 30 2015 Rafael Fonseca <rdossant@redhat.com> - 1.310-4
- Fix GVariant tests for big endian machines (#1235709)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.310-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.310-2
- Perl 5.22 rebuild

* Fri Mar 20 2015 Tom Callaway <spot@fedoraproject.org> - 1.310-1
- update to 1.310

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.305-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.305-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul  8 2014 Tom Callaway <spot@fedoraproject.org> - 1.305-1
- update to 1.305

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.304-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 09 2014 Petr Pisar <ppisar@redhat.com> - 1.304-1
- 1.304 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.280-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.280-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.280-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Tom Callaway <spot@fedoraproject.org> - 1.280-1
- update to 1.280

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.260-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 1.260-2
- Perl 5.16 rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.260-1
- 1.260 bump

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.241-4
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 1.241-3
- Do not export private modules and libraries

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.241-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Tom Callaway <spot@fedoraproject.org> - 1.241-1
- update to 1.241

* Thu Oct 20 2011 Tom Callaway <spot@fedoraproject.org> - 1.240-1
- update to 1.240

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.223-3
- Perl mass rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.223-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jul 01 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.223-1
- update to 1.223

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.201-5
- Mass rebuild with perl-5.12.0

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.201-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Stepan Kasal <skasal@redhat.com> - 1.201-3
- create devel subpackage, so that the main one does not require
  the whole perl-devel (#509419)

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.201-2
- dont run the tests on ppc

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.201-1
- update to 1.201

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.183-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.183-1
- update to 1.183

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.162-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.162-4
- Autorebuild for GCC 4.3

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.162-3
- rebuild for new perl

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.162-2
- disable smp_mflags, they break on massively SMP boxes (bz 428911)

* Mon Dec 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.162-1
- 1.162

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.144-1.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.144-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Mon Feb 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.144-1
- Update to 1.144.

* Sun Feb 11 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.143-1
- Update to 1.143.

* Thu Dec  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.142-1
- Update to 1.142.

* Wed Nov 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.141-1
- Update to 1.141.

* Wed Sep  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.140-1
- Update to 1.140.

* Tue Mar 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.120-1
- Update to 1.120.

* Mon Feb 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.105-2
- make tag problem.

* Mon Feb 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.105-1
- Update to 1.105.

* Mon Feb  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.104-1
- Update to 1.104 (fails one test in perl 5.8.8).

* Thu Jan 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.103-1
- Update to 1.103.
- Provides list: filtered out perl(MY) (#177956).

* Wed Nov 30 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.102-1
- Update to 1.102.

* Thu Oct  6 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.101-1
- Update to 1.101.

* Thu Sep  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.100-1
- Update to 1.100.

* Mon Jun 27 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.082-1
- Update to 1.082.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Mar  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.080-1
- Update to 1.080.

* Tue Feb 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.062-1
- Update to 1.062.

* Mon Oct 18 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.061-0.fdr.2
- Removed irrelevant documentation file - Glib.exports.

* Sun Oct  3 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.061-0.fdr.1
- Update to 1.061.

* Sun Jul 18 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.043-0.fdr.1
- First build.
