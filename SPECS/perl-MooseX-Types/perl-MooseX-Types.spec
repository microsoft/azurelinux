# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-MooseX-Types
Version:        0.51
Release:        2%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Summary:        Organize your Moose types in libraries
URL:            https://metacpan.org/dist/MooseX-Types
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/MooseX-Types-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Module::Build::Tiny) >= 0.034
# Module Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Carp::Clan) >= 6.00
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(Moose) >= 1.06
BuildRequires:  perl(Moose::Exporter)
BuildRequires:  perl(Moose::Meta::TypeConstraint::Union)
BuildRequires:  perl(Moose::Util::TypeConstraints)
BuildRequires:  perl(namespace::autoclean) >= 0.16
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util) >= 1.19
BuildRequires:  perl(strict)
BuildRequires:  perl(Sub::Exporter)
BuildRequires:  perl(Sub::Exporter::ForMethods) >= 0.100052
BuildRequires:  perl(Sub::Install)
BuildRequires:  perl(Sub::Util)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(if)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Metadata)
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Needs)
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(Test::Moose)
# Dependencies
# (none)

%description
The types provided with the Moose man page are by design global. This
package helps you to organize and selectively import your own and the
built-in types in libraries. As a nice side effect, it catches typos at
compile-time too.

However, the main reason for this module is to provide an easy way to not
have conflicts with your type names, since the internal fully qualified
names of the types will be prefixed with the library's name.

This module will also provide you with some helper functions to make it
easier to use Moose types in your code.

%prep
%setup -q -n MooseX-Types-%{version}

# fix shebang
/usr/bin/perl -pi -e 's|^#!perl|#!/usr/bin/perl|' t/00-report-prereqs.t

%build
/usr/bin/perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

%check
./Build test

%files
%license LICENCE
%doc Changes CONTRIBUTING README t/
%{perl_vendorlib}/MooseX/
%{_mandir}/man3/MooseX::Types.3*
%{_mandir}/man3/MooseX::Types::Base.3*
%{_mandir}/man3/MooseX::Types::CheckedUtilExports.3*
%{_mandir}/man3/MooseX::Types::Combine.3*
%{_mandir}/man3/MooseX::Types::Moose.3*
%{_mandir}/man3/MooseX::Types::TypeDecorator.3*
%{_mandir}/man3/MooseX::Types::UndefinedType.3*
%{_mandir}/man3/MooseX::Types::Util.3*
%{_mandir}/man3/MooseX::Types::Wrapper.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Apr 20 2025 Emmanuel Seyman <emmanuel@seyman.fr> - 0.51-1
- Update to 0.51

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-17
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-14
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-11
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.50-2
- Perl 5.26 rebuild

* Wed Feb  8 2017 Paul Howarth <paul@city-fan.org> - 0.50-1
- Update to 0.50
  - Reverted the is_Foo and to_Foo refactoring again temporarily to resolve
    issues with Sub::Defer

* Sun Dec 25 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.49-1
- Update to 0.49

* Sun Dec 11 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.48-1
- Update to 0.48

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 17 2015 Paul Howarth <paul@city-fan.org> - 0.46-1
- Update to 0.46
  - Make use of Sub::Exporter::ForMethods's new rebless option

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-3
- Perl 5.22 rebuild

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-2
- Perl 5.20 mass

* Mon Sep  8 2014 Paul Howarth <paul@city-fan.org> - 0.45-1
- Update to 0.45
  - Increase the required versions of some prerequisites

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.44-2
- Perl 5.20 rebuild

* Fri Aug  1 2014 Paul Howarth <paul@city-fan.org> - 0.44-1
- Update to 0.44
  - Namespace improvements
  - Avoid use of deprecated Moose functionality
- Switch to Module::Build::Tiny flow
- Use %%license
- Classify buildreqs by usage
- Make %%files list more explicit

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.35-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.35-2
- Perl 5.16 rebuild

* Sat Jun 09 2012 Iain Arnell <iarnell@gmail.com> 0.35-1
- update to latest upstream version

* Thu Jan 12 2012 Iain Arnell <iarnell@gmail.com> 0.31-1
- update to latest upstream version

* Sat Oct 01 2011 Iain Arnell <iarnell@gmail.com> 0.30-1
- update to latest upstream version

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.27-2
- Perl mass rebuild

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> 0.27-1
- update to latest upstream version
- remove explicit requires

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 0.25-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Jul 04 2010 Iain Arnell <iarnell@gmail.com> 0.22-1
- update to latest upstream
- update BR perl(Moose) >= 1.06

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.21-3
- Mass rebuild with perl-5.12.0

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.21-2
- add perl_default_filter (and drop custom filtering scheme)
- PERL_INSTALL_ROOT => DESTDIR in install

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.21-1
- auto-update to 0.21 (by cpan-spec-update 0.01)
- altered br on perl(Moose) (0.61 => 0.93)
- altered req on perl(Moose) (0.61 => 0.93)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.20-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.20-1
- auto-update to 0.20 (by cpan-spec-update 0.01)

* Mon Aug 24 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- auto-update to 0.18 (by cpan-spec-update 0.01)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.16-1
- auto-update to 0.16 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- auto-update to 0.13 (by cpan-spec-update 0.01)
- added a new br on perl(Test::Moose) (version 0)

* Tue Jun 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- auto-update to 0.12 (by cpan-spec-update 0.01)
- added a new req on perl(Carp) (version 0)
- added a new req on perl(Carp::Clan) (version 6.00)
- added a new req on perl(Moose) (version 0.61)
- added a new req on perl(Scalar::Util) (version 1.19)
- added a new req on perl(Sub::Install) (version 0.924)
- added a new req on perl(Sub::Name) (version 0)
- added a new req on perl(namespace::clean) (version 0.08)

* Tue Jun 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11-2
- add br on CPAN for bundled version of M::I

* Mon May 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11-1
- auto-update to 0.11 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(Carp::Clan) (0 => 6.00)
- added a new br on perl(Scalar::Util) (version 1.19)
- added a new br on perl(Sub::Name) (version 0)
- altered br on perl(Test::More) (0.62 => 0.80)

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- update to 0.10

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08-2
- add br on Test::Exception

* Tue Dec 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- update to 0.08

* Mon Nov 10 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- update to 0.07, adjust BR accordingly.  Note especially dep on Moose >= 0.61

* Sun Oct 12 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-2
- bump

* Tue Oct 07 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.1)
