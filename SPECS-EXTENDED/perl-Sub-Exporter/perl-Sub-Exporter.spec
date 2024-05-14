# Provides/Requires filtering is different from rpm 4.9 onwards
%global rpm49 %(rpm --version | perl -p -e 's/^.* (\\d+)\\.(\\d+).*/sprintf("%d.%03d",$1,$2) ge 4.009 ? 1 : 0/e' 2>/dev/null || echo 0)

# Run extra test
%if ! (0%{?rhel})
%bcond_without perl_Sub_Exporter_enables_extra_test
%else
%bcond_with perl_Sub_Exporter_enables_extra_test
%endif

Name:		perl-Sub-Exporter
Version:	0.987
Release:	22%{?dist}
Summary:	Sophisticated exporter for custom-built routines
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/Sub-Exporter
Source0:	https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Sub-Exporter-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(Data::OptList) >= 0.1
BuildRequires:	perl(Package::Generator)
BuildRequires:	perl(Params::Util) >= 0.14
BuildRequires:	perl(Sub::Install) >= 0.92
# Test suite
BuildRequires:	perl(base)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(lib)
BuildRequires:	perl(subs)
BuildRequires:	perl(Test::More) >= 0.94
# Extra tests
%if %{with perl_Sub_Exporter_enables_extra_test}
BuildRequires:	perl(Test::Pod) >= 1.41
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Package::Generator)

# Don't want doc-file provides or dependencies
%global our_docdir %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
%global __provides_exclude_from ^%{our_docdir}/
%global __requires_exclude_from ^%{our_docdir}/

%description
Sub::Exporter provides a sophisticated alternative to Exporter.pm. It allows
for renaming, currying/sub-generation, and other cool stuff.

ACHTUNG! If you're not familiar with Exporter or exporting, read
Sub::Exporter::Tutorial first!

%prep
%setup -q -n Sub-Exporter-%{version}

# Fix shellbangs
find t/ -type f -exec \
	perl -MExtUtils::MakeMaker -e 'ExtUtils::MM_Unix->fixin(qw{{}})' \;

# Filter bogus provides/requires if we don't have rpm ≥ 4.9
%if ! %{rpm49}
%global provfilt /bin/sh -c "%{__perl_provides} | grep -Ev '^perl[(]Test::SubExporter.*[)]'"
%global __perl_provides %{provfilt}
%global reqfilt /bin/sh -c "%{__perl_requires} | grep -Ev '^perl[(](base|Test::SubExporter.*)[)]'"
%global __perl_requires %{reqfilt}
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
%if %{with perl_Sub_Exporter_enables_extra_test}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%doc Changes README t/
%dir %{perl_vendorlib}/Sub/
%dir %{perl_vendorlib}/Sub/Exporter/
%{perl_vendorlib}/Sub/Exporter.pm
%{perl_vendorlib}/Sub/Exporter/Util.pm
%doc %{perl_vendorlib}/Sub/Exporter/Cookbook.pod
%doc %{perl_vendorlib}/Sub/Exporter/Tutorial.pod
%{_mandir}/man3/Sub::Exporter.3*
%{_mandir}/man3/Sub::Exporter::Cookbook.3*
%{_mandir}/man3/Sub::Exporter::Tutorial.3*
%{_mandir}/man3/Sub::Exporter::Util.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.987-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.987-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.987-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.987-19
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.987-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.987-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.987-16
- Perl 5.28 rebuild

* Thu Apr 12 2018 Paul Howarth <paul@city-fan.org> - 0.987-15
- Drop some support for older distributions
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section
  - Drop workarounds for building with Test::More < 0.94

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.987-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.987-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.987-12
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.987-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 22 2016 Petr Pisar <ppisar@redhat.com> - 0.987-10
- Adjust RPM version detection to SRPM build root without perl

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.987-9
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.987-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan  7 2016 Paul Howarth <paul@city-fan.org> - 0.987-7
- Don't use %%define

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.987-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.987-5
- Perl 5.22 rebuild

* Fri Jan 16 2015 Petr Pisar <ppisar@redhat.com> - 0.987-4
- Do not hard-code interpreter name

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.987-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.987-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Oct 19 2013 Paul Howarth <paul@city-fan.org> - 0.987-1
- Update to 0.987 (update bugtracker metadata)
- Update patches as needed

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.986-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Paul Howarth <paul@city-fan.org> - 0.986-3
- Handle filtering of provides/requires from unversioned doc-dirs from F-20

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.986-2
- Perl 5.18 rebuild

* Sat Jun 15 2013 Paul Howarth <paul@city-fan.org> - 0.986-1
- Update to 0.986 (typo fixes in docs)
- Use metacpan URLs

* Thu Feb 21 2013 Paul Howarth <paul@city-fan.org> - 0.985-1
- Update to 0.985 (documentation fixes)
- Add patch to support building with Test::More < 0.88
- Run the extra tests too
- BR: perl(File::Find) and perl(File::Temp) for test suite
- BR: perl(Test::Pod) for the extra tests

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.984-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Petr Pisar <ppisar@redhat.com> - 0.984-4
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.984-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.984-2
- Perl 5.16 rebuild

* Tue Jun  5 2012 Paul Howarth <paul@city-fan.org> - 0.984-1
- Update to 0.984 (documentation fixes)
- Add filters for provides/requires from the test suite
- BR: perl(base) and perl(Exporter) for the test suite

* Sun Mar 18 2012 Paul Howarth <paul@city-fan.org> - 0.982-11
- Drop %%defattr, redundant since rpm 4.4

* Sat Mar  3 2012 Paul Howarth <paul@city-fan.org> - 0.982-10
- Explicitly require perl(Package::Generator)
- Make %%files list more explicit
- Mark POD files as %%doc
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.982-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.982-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.982-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.982-4
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.982-1
- Update to 0.982

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.981-1
- Update to 0.981

* Thu Oct 23 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.980-1
- Update to 0.980

* Mon Jun 30 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.979-1
- Update to 0.979
- Drop BR's on: perl(Test::Pod::Coverage), perl(Test::Pod)

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.978-2
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.978-1
- Update to 0.978
- Fix license tag
- Rebuild for new perl

* Thu Aug 09 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.975-1
- Update to 0.975

* Fri Jun 01 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.974-1
- Update to 0.974

* Sat Dec 09 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.972-1
- Update to 0.972

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.970-2
- Bump

* Sat Sep 02 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.970-1
- Specfile autogenerated by cpanspec 1.69.1
