# No Mojolicious prior to Fedora 14
# Mojolicious in Fedora 14 is too old
# No Mojolicious in EPEL

%global have_mojo 1




# Run extra test
%if 0%{?rhel}
%bcond_with perl_MIME_Types_enables_extra_test
%else
%bcond_without perl_MIME_Types_enables_extra_test
%endif

Name:           perl-MIME-Types
Version:        2.17
Release:        9%{?dist}
Summary:        MIME types module for Perl
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/MIME-Types
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MARKOV/MIME-Types-%{version}.tar.gz#/perl-MIME-Types-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(List::Util)
%if %{have_mojo}
BuildRequires:  perl(Mojo::Base)
%endif
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
%if %{with perl_MIME_Types_enables_extra_test}
# Extra Tests
BuildRequires:  perl(Test::MinimumVersion)
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
MIME types are used in many applications, for instance as part of e-mail
and HTTP traffic, to indicate the type of content that is transmitted.

Sometimes detailed knowledge about a mime-type is need; however, this
module only knows about the file-name extensions that relate to some
file-type.  It can also be used to produce the right format: types that
are not registered at IANA need to use 'x-' prefixes.

%if %{have_mojo}
%package -n perl-MojoX-MIME-Types

Summary:        MIME Types for Mojolicious
Requires:       perl-MIME-Types = %{version}-%{release}

%description -n perl-MojoX-MIME-Types
This module is a drop-in replacement for Mojolicious::Types, but with a more
correct handling plus a complete list of types... a huge list of types.

Some methods ignore information they receive: those parameters are accepted
for compatibility with the Mojolicious::Types interface, but should not
contain useful information.

%endif

%prep
%setup -q -n MIME-Types-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
%if %{with perl_MIME_Types_enables_extra_test}
make test TEST_FILES="xt/*.t"
%endif

%files
%doc ChangeLog README README.md
%{perl_vendorlib}/MIME/
%{_mandir}/man3/MIME::Type.3*
%{_mandir}/man3/MIME::Types.3*

%if %{have_mojo}
%files -n perl-MojoX-MIME-Types
%{perl_vendorlib}/MojoX/
%{_mandir}/man3/MojoX::MIME::Types.3*
%else
%exclude %{perl_vendorlib}/MojoX/
%exclude %{_mandir}/man3/MojoX::MIME::Types.3*
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.17-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.17-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.17-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Paul Howarth <paul@city-fan.org> - 2.17-1
- Update to 2.17
  - When picking a preferred type for an extension, prefer the type with the
    same minor-name
  - Remove IANA obsoleted types

* Tue Jan 23 2018 Paul Howarth <paul@city-fan.org> - 2.16-1
- Update to 2.16
  - Collecting of IANA info had stalled: logic rewritten
  - Moved to git and GitHub
  - Move scripts and source files into MANIFEST.extra
  - Update types and extensions

* Fri Nov 10 2017 Paul Howarth <paul@city-fan.org> - 2.14-1
- Update to 2.14
  - MojoX should not die on missing types (CPAN RT#123298)
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.13-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.13-2
- Perl 5.24 rebuild

* Tue Mar  8 2016 Paul Howarth <paul@city-fan.org> - 2.13-1
- Update to 2.13
  - Not all information was extracted from the Apache tables
- Simplify find command using -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Paul Howarth <paul@city-fan.org> - 2.12-1
- Update to 2.12
  - Downgrade prereq perl to 5.6
  - Update IANA

* Fri Jun 26 2015 Paul Howarth <paul@city-fan.org> - 2.11-1
- Update to 2.11
  - Accept field 'q' weights
  - Introduce PERL_MIME_TYPE_DB (CPAN RT#104945)
  - Strict Perl 5.8 (CPAN RT#105267)
- Classify buildreqs by usage

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-2
- Perl 5.22 rebuild

* Mon Sep 15 2014 Paul Howarth <paul@city-fan.org> - 2.09-1
- Update to 2.09
  - Rename ::Type::isAscii() into ::Type::isText()
  - Add source table broofa (CPAN RT#98308)
  - Add source table freedesktop (CPAN RT#98309)
  - Update IANA types
  - Fix scan of freedesktop definitions (CPAN RT#98385)
  - MIME::Type::equals() did cmp not eq
  - New httpAccept() wth tests in t/21accept.t
  - New httpAcceptBest() and httpAcceptSelect() with tests in t/22accbest.t
  - Add MojoX::MIME::Types with tests in t/40mojo.t
  - Now depends on List::Util
  - Documentation fixes
- Sub-package MojoX::MIME::Types to avoid pulling in Mojolicious as a
  dependency for users of MIME::Types

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.04-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 12 2013 Paul Howarth <paul@city-fan.org> - 2.04-1
- Update to 2.04:
  - Fix one more localize $_ in ::Types::_read_db() (CPAN RT#87856)

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 2.03-1
- Update to 2.03:
  - Fix typo in docs (CPAN RT#88394)
  - Require perl 5.8.8, for <:encoding
  - Updated IANA
  - A bit more DESCRIPTION
- Update %%description

* Sun Aug 18 2013 Paul Howarth <paul@city-fan.org> - 2.02-1
- Update to 2.02:
  - Localize DB and $_ in ::Types::_read_db() (CPAN RT#87856)

* Sun Aug  4 2013 Paul Howarth <paul@city-fan.org> - 2.01-1
- Update to 2.01:
  - Add dummy ::Types::create_type_index() because
    Catalyst-Plugin-Static-Simple calls it :(

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug  2 2013 Paul Howarth <paul@city-fan.org> - 2.00-1
- Update to 2.00:
  - The mime information is now collected from various sources, amongst them
    IANA; hence, some types may use different x-'s
  - A separate table is built for the extension-to-type mapping
  - Number of types up from 995 to 2096
  - Number of extensions up from 734 to 1425
  - The memory footprint and start-up speed should have improved considerably
  - Added bin/collect_types
  - Fixed some typos (CPAN RT#86847)
  - Added ::Type::isVendor(), ::isExperimental(), ::isPersonal (CPAN RT#87062)
  - Added ::Types::listTypes()
  - Cleaned-up Exporter syntax of (very) old interface
- BR: perl(base), perl(File::Basename) and perl(File::Spec)
- Drop no-longer-needed UTF8 patch

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.38-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 11 2013 Paul Howarth <paul@city-fan.org> - 1.38-1
- Update to 1.38:
  - Add application/vnd.ms-excel.template.macroEnabled.12 and five related
    from https://filext.com/faq/office_mime_types.php (CPAN RT#82616)

* Fri Dec 21 2012 Paul Howarth <paul@city-fan.org> - 1.37-1
- Update to 1.37:
  - Remove text/x-perl, where we also have an application/x-perl
    (CPAN RT#82100)

* Wed Nov 21 2012 Petr Šabata <contyk@redhat.com> - 1.36-2
- Buildrequire perl(lib)

* Thu Nov  1 2012 Paul Howarth <paul@city-fan.org> - 1.36-1
- Update to 1.36:
  - xlsx and friends had encoding 'binary' (since version 1.30), but should
    have been 'base64' (CPAN RT#80529)

* Tue Jul 24 2012 Paul Howarth <paul@city-fan.org> - 1.35-1
- Update to 1.35:
  - Explain how to use MIME::Types in mod_perl; when you do not read the
    documentation about mod_perl/fork it will work as always, but
    inefficiently
  - subType() did not handle subType's with '+' in them
  - Added video/webm and audio/webm, although not (yet) IANA registered
- BR: perl(Carp) and perl(Exporter)
- BR: at least version 1.00 of  perl(Test::Pod)
- Use a patch rather than scripted iconv to fix character encooding
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4
- Use %%{_fixperms} macro rather than our own chmod incantation
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't use macros for commands
- Make %%files list more explicit

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.31-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.31-2
- Perl mass rebuild

* Tue Mar 15 2011 Paul Howarth <paul@city-fan.org> - 1.31-1
- Update to 1.31:
  - Added zillions of new types from debian's /etc/mime.types
  - Changed table format, hopefully to speed-up load times per type, slightly
    compensating for the increased list
  - Fix typo (CPAN RT#55655)
  - xlsx must be encoded binary
  - Added f4v, f4p, f4a, f4b extensions for mpeg4 (CPAN RT#55168)
  - Moved POD test to xt directory, reducing the number of dependencies

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.28-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.28-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.28-2
- rebuild against perl 5.10.1

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 1.28-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.27-1
- update to 1.27

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.24-1
- update to 1.24

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.23-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.23-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.23-1
- bump to 1.23

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-2
- license tag fix

* Wed Jun 13 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.20-1
- 1.20.
- Convert docs to UTF-8.

* Tue Apr 17 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.19-2
- BuildRequire perl(Test::More).

* Mon Mar 26 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.19-1
- 1.19.
- BuildRequire perl(ExtUtils::MakeMaker).

* Wed Nov 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.18-1
- 1.18.

* Fri Sep 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.17-2
- Rebuild.

* Tue Aug 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.17-1
- 1.17.

* Sun Oct  2 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.16-1
- 1.16.

* Fri Apr  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.15-2
- 1.15.

* Tue May 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.13-0.fdr.3
- Require perl(:MODULE_COMPAT_*) (bug 1649).

* Mon May 17 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.13-0.fdr.2
- Sync with IANA 20040517.
- Require perl >= 1:5.6.1 for vendor install dir support.
- Use pure_install to avoid perllocal.pod workarounds.

* Sat Apr 24 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.13-0.fdr.1
- Update to 1.13 + IANA 20040424.

* Sun Feb  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.12-0.fdr.2
- Reduce directory ownership bloat.

* Wed Jan 21 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.12-0.fdr.1
- Update to 1.12.

* Wed Jan 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.11-0.fdr.1
- Update to 1.11.

* Wed Dec 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.10-0.fdr.2
- BuildRequires perl(Test::More).

* Fri Dec 19 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.10-0.fdr.1
- Update to 1.10.

* Thu Nov  6 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.09-0.fdr.1
- Update to 1.09.

* Tue Nov  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.08-0.fdr.1
- Update to 1.08.

* Sat Oct 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.07-0.fdr.2
- Install into vendor dirs.
- Don't use fedora-rpm-helper.
- Specfile cleanup.

* Wed Jul 30 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.07-0.fdr.1
- Update to 1.07.
- Use fedora-rpm-helper.

* Tue Jun 24 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.06-0.fdr.1
- First build.
