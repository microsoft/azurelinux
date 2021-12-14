Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-FCGI
Summary:        FastCGI Perl bindings
Version:        0.79
Release:        4%{?dist}
# same as fcgi
License:        OML

Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/FCGI-%{version}.tar.gz 
# Fix CVE-2012-6687 in the bundled fcgi library, bug #1190294, CPAN RT#118405,
# patch copied from Debian's libfcgi-perl.
Patch0:         FCGI-0.78-CVE-2012-6687.patch
URL:            https://metacpan.org/release/FCGI
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
# ExtUtils::Liblist not used
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Copy)
# File::Spec not used on Linux
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
# Run-time:
# Carp not used at tests
BuildRequires:  perl(strict)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(XSLoader)
# fcgiapp.c, os_unix.c, os_win32.c are copied and modified from FastCGI
# Developer's Kit of an unknown version, bug #736612
Provides:       bundled(fcgi)

%{?perl_default_filter}

%description
%{summary}.

%prep
%setup -q -n FCGI-%{version}
%patch0 -p1
find . -type f -exec chmod -c -x {} +

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc ChangeLog README
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.79-4
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.79-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.79-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 15 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 1:0.79-1
- Update to 0.79

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.78-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.78-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.78-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Petr Pisar <ppisar@redhat.com> - 1:0.78-11
- Document an fcgi library is bundled (bug #736612)
- Fix CVE-2012-6687 in the bundled fcgi library (bug #1190294)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.78-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.78-9
- Perl 5.28 rebuild

* Sun Mar 11 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 1:0.78-8
- Add missing build-requirements

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.78-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.78-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.78-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.78-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.78-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.78-2
- Perl 5.24 rebuild

* Fri Mar 11 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 1:0.78-1
- Update to 0.78
- Pass NO_PACKLIST to Makefile.PL
- Drop Obsolete Obsoletes

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.77-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.77-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.77-5
- Perl 5.22 rebuild

* Wed Jan 14 2015 Petr Pisar <ppisar@redhat.com> - 1:0.77-4
- Specify all dependencies

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.77-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug 17 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1:0.77-1
- Update to 0.77
- Use %%license

* Sun Jul 20 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1:0.75-1
- Update to 0.75
- Remove the Group macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.74-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 02 2013 Petr Pisar <ppisar@redhat.com> - 1:0.74-10
- Correct tests sub-package obsoleteness
- Old fcgi-perl provides removed

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.74-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1:0.74-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.74-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Petr Šabata <contyk@redhat.com> - 1:0.74-6
- Add missing buildtime dependencies
- Drop command macros
- Drop the tests subpackage

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.74-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1:0.74-4
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 1:0.74-3
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 24 2011 Iain Arnell <iarnell@gmail.com> 1:0.74-1
- update to latest upstream
- drop cve-2011-2766 patch

* Fri Sep 23 2011 Iain Arnell <iarnell@gmail.com> 1:0.73-3
- patch to resolve rhbz#736604 cve-2011-2766

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.73-2
- Perl mass rebuild

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.73-1
- update to 0.73, clean spec file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.71-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.71-4
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 15 2010 Chris Weyl <cweyl@alumni.drew.edu> 1:0.71-3
- and fix our tests subpackage included files

* Sat May 15 2010 Chris Weyl <cweyl@alumni.drew.edu> 1:0.71-2
- fix license: BSD => OML

* Sat May 08 2010 Chris Weyl <cweyl@alumni.drew.edu> 1:0.71-1
- specfile by Fedora::App::MaintainerTools 0.006


