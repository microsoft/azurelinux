# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Pod-Readme
Version:        1.2.3
Release: 21%{?dist}
Summary:        Intelligently generate a README file from POD
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Pod-Readme
Source0:        https://cpan.metacpan.org/modules/by-module/Pod/Pod-Readme-v%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  sed
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Method::Modifiers) >= 2.00
BuildRequires:  perl(CPAN::Changes) >= 0.30
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.56
BuildRequires:  perl(feature)
BuildRequires:  perl(File::Slurp)
BuildRequires:  perl(Hash::Util)
BuildRequires:  perl(IO)
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl(Module::Load)
BuildRequires:  perl(Moo) >= 1.004005
BuildRequires:  perl(Moo::Role)
BuildRequires:  perl(MooX::HandlesVia)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Path::Tiny) >= 0.018
BuildRequires:  perl(Pod::Simple)
BuildRequires:  perl(Role::Tiny)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(Type::Tiny) >= 1.000000
BuildRequires:  perl(Types::Standard)
BuildRequires:  perl(warnings)
# Script Runtime
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(Getopt::Long::Descriptive)
BuildRequires:  perl(IO::Handle)
# Test Suite
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::String)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Metadata)
BuildRequires:  perl(Pod::Simple::Text)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Exception)
# Pod::Readme::Test::Kit not actually used
#BuildRequires: perl(Test::Kit)
BuildRequires:  perl(Test::More) >= 0.88
# Dependencies
Requires:       perl(Role::Tiny)

%description
This module filters POD to generate a README file, by using POD commands to
specify which parts are included or excluded from the README file.

%prep
%setup -q -n Pod-Readme-v%{version}

# Fix script interpreter
sed -i -e 's|#!/usr/bin/env perl|#!/usr/bin/perl|' bin/pod2readme

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README.pod
%{_bindir}/pod2readme
%{perl_vendorlib}/Pod/
%{_mandir}/man1/pod2readme.1*
%{_mandir}/man3/Pod::Readme.3*
%{_mandir}/man3/Pod::Readme::Filter.3*
%{_mandir}/man3/Pod::Readme::Plugin.3*
%{_mandir}/man3/Pod::Readme::Plugin::changes.3*
%{_mandir}/man3/Pod::Readme::Plugin::requires.3*
%{_mandir}/man3/Pod::Readme::Plugin::version.3*
%{_mandir}/man3/Pod::Readme::Types.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.3-12
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.3-9
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.3-6
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.3-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov  1 2018 Paul Howarth <paul@city-fan.org> - 1.2.3-1
- Update to 1.2.3
  - Updated POD with regard to format types
  - Fixed typos in Changes
  - Added explicit requirements for Pod::Simple as well as recommended modules
  - Remove explicit core dependencies from prereqs list
  - Updated list of contributors in distribution metadata
  - Increased minimum version of Type::Tiny to 1.000000

* Wed Oct 31 2018 Paul Howarth <paul@city-fan.org> - 1.2.1-1
- Update to 1.2.1
  - Restore license to "Perl_5" that was inadvertently changed in the
    conversion to use Dist::Zilla (GH#25)
- Package the LICENSE file

* Tue Oct 30 2018 Paul Howarth <paul@city-fan.org> - 1.2.0-1
- Update to 1.2.0
  - Remove use of Module::Install (GH#21)
  - Use Dist::Zilla to build the distribution.
  - Removed DistZilla type from Pod::Readme::Types, as it was not necessary
  - Specify minimum version of List::Util (GH#22)
  - Added "md" as an alias for "markdown" in pod2readme
  - Added "github" or "gfm" for Github Flavored Markdown in pod2readme (GH#15)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.2-13
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.2-10
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.2-8
- Perl 5.24 rebuild

* Wed Apr 20 2016 Paul Howarth <paul@city-fan.org> - 1.1.2-7
- Don't assume that EU::MM will generate Pod::README manpage
- Simplify find command using -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 10 2015 Petr Pisar <ppisar@redhat.com> - 1.1.2-5
- Do not install Pod::README (bug #1259389)

* Wed Sep 02 2015 Petr Šabata <contyk@redhat.com> - 1.1.2-4
- The latest EU::MM no longer manifies README.pod
- Added some more build deps, mostly the required Module::Install modules

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.2-2
- Perl 5.22 rebuild

* Tue Dec  9 2014 Paul Howarth <paul@city-fan.org> - 1.1.2-1
- Update to 1.1.2
  - Regex in changes plugin fixed to work with Perl 5.21 deprecated syntax

* Thu Dec  4 2014 Paul Howarth <paul@city-fan.org> - 1.1.1-1
- Update to 1.1.1
  - The changes plugin will work with Dist::Zilla {{$NEXT}} tokens

* Thu Dec  4 2014 Paul Howarth <paul@city-fan.org> - 1.1.0-1
- Update to 1.1.0
  - Fixed typos in POD for requires plugin
  - Pod::Readme::Filter has a zilla attribute for Dist::Zilla objects
  - The requires plugin will use metadata from the Dist::Zilla object
    if it is set, rather than looking for a META.yml file (which will
    not exist, if this is used in a Dist::Zilla plugin)

* Tue Nov 11 2014 Paul Howarth <paul@city-fan.org> - 1.0.3-1
- Update to 1.0.3
  - Fixed bug with minimum version of Class::Method::Modifiers

* Tue Oct 14 2014 Paul Howarth <paul@city-fan.org> - 1.0.2-1
- Update to 1.0.2
  - This is a complete rewrite, using modern Perl with Moo
  - Added support for plugins, along with plugins to insert the module version,
    prerequisites and the latest changes
  - Added the ability to generate a README in a variety of formats, such as
    POD, Markdown, HTML, RTF, etc.
  - Added command-line options to the pod2readme script, including the ability
    to specify the output format
  - Switched to semantic versioning
  - The documentation has been updated accordingly
  - This is no longer a subclass of a POD parser, although it has some wrapper
    methods for compatibility with software known to use it
- This release by RRWO → update source URL
- Modernize spec since this version will never run on EL-5
- Unbundle the Module::Install stuff and use the system version instead

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.110-11
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.110-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.110-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.110-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Steven Pritchard <steve@kspei.com> 0.110-1
- Update to 0.11.
- Update Source0 URL.
- Switch back to building with ExtUtils::MakeMaker/Makefile.PL.
- BR Test::More.

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.090-8
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.090-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.090-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.090-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.090-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.090-3
- rebuild for new perl

* Tue Nov 27 2007 Steven Pritchard <steve@kspei.com> 0.090-2
- Update License tag.
- Drop explicit dependencies on Test::* modules (#232736).

* Sat Dec 09 2006 Steven Pritchard <steve@kspei.com> 0.090-1
- Update to 0.09.
- Use fixperms macro instead of our own chmod incantation.
- BR: Regexp::Common.
- Switch back to using Module::Build.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.081-3
- Fix find option order.

* Fri May 12 2006 Steven Pritchard <steve@kspei.com> 0.081-2
- Use Makefile.PL temporarily to work around Module::Build breakage.

* Fri May 12 2006 Steven Pritchard <steve@kspei.com> 0.081-1
- Specfile autogenerated by cpanspec 1.66.
- Remove explicit perl dep.
- Set DEVEL_TESTS for "Build test".
- Add bindir and man1 to file list.
