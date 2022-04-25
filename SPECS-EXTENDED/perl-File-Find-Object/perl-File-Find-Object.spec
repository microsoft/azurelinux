Name:           perl-File-Find-Object
Version:        0.3.5
Release:        3%{?dist}
Summary:        Object oriented File::Find replacement
License:        GPLv2+ or Artistic 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/File-Find-Object
Source0:        https://cpan.metacpan.org/modules/by-module/File/File-Find-Object-%{version}.tar.gz#/perl-File-Find-Object-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::XSAccessor)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(integer)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(File::Path)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(lib)
BuildRequires:  perl(blib)
BuildRequires:  perl(Test::More) >= 0.88
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
File::Find::Object does the same job as File::Find but works like an object
and with an iterator. As File::Find is not object oriented, one cannot
perform multiple searches in the same application. The second problem of
File::Find is its file processing: after starting its main loop, one cannot
easily wait for another event and so get the next result.

%prep
%setup -qn File-Find-Object-%{version}
chmod -c 644 examples/tree

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
%doc Changes README.md examples/
%{perl_vendorlib}/File/
%{_mandir}/man3/File::Find::Object.3*
%{_mandir}/man3/File::Find::Object::Base.3*
%{_mandir}/man3/File::Find::Object::PathComp.3*
%{_mandir}/man3/File::Find::Object::Result.3*

%changelog
* Fri Apr 22 2022 Muhammad Falak <mwani@microsoft.com>- 0.3.5-3
- Add an explicit BR on `perl(blib)` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.5-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Tue Jan 28 2020 Paul Howarth <paul@city-fan.org> - 0.3.5-1
- Update to 0.3.5
  - Rebuild for order of 'NAME' and 'VERSION' sections in the generated POD
    documentation (VERSION used to appear before NAME)
- Use %%{make_build} and %%{make_install}

* Mon Aug 26 2019 Paul Howarth <paul@city-fan.org> - 0.3.4-1
- Update to 0.3.4
  - Now at https://github.com/shlomif/perl-file-find-object
  - tidyall
  - Add *~ files to MANIFEST.SKIP (GH#1)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.3.2-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.3.2-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.3.2-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 15 2017 Paul Howarth <paul@city-fan.org> - 0.3.2-1
- Update to 0.3.2
  - Made the version number consistent across the .pm files
    (https://bitbucket.org/shlomif/perl-file-find-object/issues/1/wrong-version-number)

* Mon Jan  9 2017 Paul Howarth <paul@city-fan.org> - 0.3.1-1
- Update to 0.3.1
  - Fixed an issue with tracking the depth of the inodes when detecting a
    symlink loop

* Mon Sep 12 2016 Paul Howarth <paul@city-fan.org> - 0.3.0-1
- Update to 0.3.0
  - Converted the build system to Dist-Zilla
- Switch to ExtUtils::MakeMaker-based flow

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.13-5
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.13-4
- Perl 5.24 rebuild

* Mon Feb 29 2016 Paul Howarth <paul@city-fan.org> - 0.2.13-3
- Spec clean-up

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 24 2015 Petr Pisar <ppisar@redhat.com> - 0.2.13-1
- 0.2.13 bump
- License changed to (GPLv2+ or Artistic 2.0)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.11-6
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.11-5
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.11-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.11-3
- Perl 5.20 rebuild

* Wed Jul 23 2014 Petr Pisar <ppisar@redhat.com> - 0.2.11-2
- Break dependency cycle perl-File-Find-Object → perl-Test-TrailingSpace →
  perl-File-Find-Object-Rule

* Wed Jun 11 2014 Christopher Meng <rpm@cicku.me> - 0.2.11-1
- Update to 0.2.11

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.2.7-3
- Perl 5.18 rebuild

* Wed Jul 03 2013 Christopher Meng <rpm@cicku.me> - 0.2.7-2
- Fix the license.
- Fix the files permissions.
- Fill up the BRs.

* Sun May 26 2013 Christopher Meng <rpm@cicku.me> - 0.2.7-1
- Initial Package.
