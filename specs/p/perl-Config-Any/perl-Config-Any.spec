# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Config-Any
Summary:        Load configuration from different file formats, transparently
Version:        0.33
Release:        7%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Config-Any
Source0:        https://cpan.metacpan.org/modules/by-module/Config/Config-Any-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Pluggable::Object) >= 3.6
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Optional Functionality
BuildRequires:  perl(Config::General) >= 2.48
BuildRequires:  perl(Config::Tiny)
BuildRequires:  perl(Cpanel::JSON::XS)
BuildRequires:  perl(XML::NamespaceSupport)
BuildRequires:  perl(XML::Simple)
BuildRequires:  perl(YAML::XS)
BuildRequires:  perl(YAML)
# Test Suite
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(lib)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
# Optional Tests
BuildRequires:  perl(XML::LibXML) >= 1.59
# Dependencies
Requires:       perl(Config::General) >= 2.48
Requires:       perl(Config::Tiny)
Requires:       perl(Cpanel::JSON::XS)
Requires:       perl(XML::NamespaceSupport)
Requires:       perl(XML::Simple)
Requires:       perl(YAML::XS)
Requires:       perl(YAML)

%description
Config::Any provides a facility for Perl applications and libraries to
load configuration data from multiple different file formats. It supports
XML, YAML, JSON, Apache-style configuration, Windows INI files, and even
Perl code.

%prep
%setup -q -n Config-Any-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
# conf/ for examples of different config types
%doc Changes README t/conf/
%{perl_vendorlib}/Config/
%{_mandir}/man3/Config::Any.3*
%{_mandir}/man3/Config::Any::Base.3*
%{_mandir}/man3/Config::Any::General.3*
%{_mandir}/man3/Config::Any::INI.3*
%{_mandir}/man3/Config::Any::JSON.3*
%{_mandir}/man3/Config::Any::Perl.3*
%{_mandir}/man3/Config::Any::XML.3*
%{_mandir}/man3/Config::Any::YAML.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May  3 2023 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33
  - Update docs to describe which modules are needed for which formats
  - Update Config::General requirement for conf files to a non-broken version
    (2.48)
  - Don't try to upgrade old Config::General versions
  - Fix is_supported method verifying the version of required modules
  - Documentation clean-ups
- Package LICENSE file

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-18
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-15
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-12
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 30 2019 Paul Howarth <paul@city-fan.org> - 0.32-10
- Spec tidy-up
  - Use author-independent source URL
  - Classify buildreqs by usage
  - Cpanel::JSON::XS is now upstream's preferred JSON backend
  - Drop redundant use of %%{?perl_default_filter}
  - Use %%{make_build} and %%{make_install}
  - Fix permissions verbosely
  - Make %%files list more explicit

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-2
- Perl 5.26 rebuild

* Thu Apr 27 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 0.32-1
- Update to 0.32

* Sun Apr 02 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 0.30-1
- Update to 0.30

* Sat Mar 04 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 0.29-1
- Update to 0.29

* Sun Feb 26 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 0.28-1
- Update to 0.28

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-2
- Perl 5.24 rebuild

* Tue Apr 05 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.27-1
- Update to 0.27

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-2
- Perl 5.22 rebuild

* Sun May 10 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.26-1
- Update to 0.26
- Tighten file listing

* Sat Apr 25 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.25-1
- Update to 0.25
- Clean up spec file

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Feb 15 2014 Robin Lee <cheeselee@fedoraproject.org> - 0.24-2
- Drop tests subpackage

* Thu Sep 26 2013 Robin Lee <cheeselee@fedoraproject.org> - 0.24-1
- Update to 0.24

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.23-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 0.23-2
- Perl 5.16 rebuild

* Fri Jan 13 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.23-1
- Update to 0.23
- BR: add perl(Test::Pod::Coverage)

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.20-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.20-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Aug 27 2010 Iain Arnell <iarnell@gmail.com> 0.20-1
- update to latest upstream

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.19-2
- Mass rebuild with perl-5.12.0

* Mon Mar 01 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.19-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- added a new br on perl(ExtUtils::MakeMaker) (version 6.42)
- dropped old BR on perl(JSON::Syck)
- added manual BR on perl(JSON::XS)
- added a new req on perl(Module::Pluggable) (version 3.01)
- dropped old requires on perl(JSON::Syck)
- added manual requires on perl(JSON::XS)

* Mon Jan 11 2010 Iain Arnell <iarnell@gmail.com> 0.18-1
- update to latest upstream version
- prefer YAML::XS over YAML::Syck

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.17-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- update to 0.17

* Sat Dec 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.16-1
- update to 0.16

* Thu Sep 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- update to 0.14
- add XML::LibXML to br's

* Wed May 21 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- update to 0.12

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-2
- rebuild for new perl

* Tue Oct 23 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- update to 0.08
- license tag update: GPL -> GPL+
- Module::Build -> Module::Install

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.07-4
- bump

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.07-3
- add entirety of t/ to %%doc

* Tue Apr 10 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.07-2
- Additional requires not documented added

* Tue Apr 10 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- Specfile autogenerated by cpanspec 1.70.
