# Perform functional tests using FCGI::Client.
# RHEL does not include FCGI::Client due to its dependencies.
%bcond perl_FCGI_enables_client_tests %{undefined rhel}

Name:           perl-FCGI
Summary:        FastCGI Perl bindings
# needed to properly replace/obsolete fcgi-perl
Epoch:          1
Version:        0.82
Release:        12%{?dist}
# eg/echo.pl:   "See the LICENSE file"
# fastcgi.h:    "See the LICENSE file"
# FCGI.pm:      "See the LICENSE file"
# fcgiapp.c:    "See the LICENSE file"
# fcgiapp.h:    "See the LICENSE file"
# fcgimisc.h:   "See the LICENSE file
# fcgios.h:     "See the LICENSE file"
# LICENSE:      OML
# os_unix.c:    "See the LICENSE file"
# README:       "See the LICENSE file"
## Used at build time, but nonpackaged
# configure:    FSFUL
## Unused and nonpackaged
# os_win32.c:   "See the LICENSE file"
License:        OML
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/FCGI-%{version}.tar.gz 
# Fix CVE-2012-6687 in the bundled fcgi library, bug #1190294, CPAN RT#118405,
# patch copied from Debian's libfcgi-perl.
Patch0:         FCGI-0.78-CVE-2012-6687.patch
URL:            https://metacpan.org/release/FCGI
# bash for sh executed from Makefile.PL
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
# grep executed by configure
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
# ExtUtils::Liblist not used
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Copy)
# File::Spec not used on Linux
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
# sed executed by configure
BuildRequires:  sed
# Run-time:
# Carp not used at tests
BuildRequires:  perl(strict)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(Test)
%if %{with perl_FCGI_enables_client_tests}
BuildRequires:  perl(FCGI::Client)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(warnings)
%endif
Requires:       perl(Carp)
Requires:       perl(XSLoader)
# fcgiapp.c, os_unix.c, os_win32.c are copied and modified from FastCGI
# Developer's Kit of an unknown version, bug #736612
Provides:       bundled(fcgi)

%{?perl_default_filter}

%description
%{summary}.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n FCGI-%{version}
find . -type f -exec chmod -c -x {} +
%if %{without perl_FCGI_enables_client_tests}
rm -f t/02-unix_domain_socket.t
perl -i -ne 'print $_ unless m{^t/02-unix_domain_socket\.t}' MANIFEST
%endif
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 \
                 NO_PERLLOCAL=1
%make_build

%install
%make_install
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc ChangeLog eg README
%{perl_vendorarch}/auto/FCGI
%{perl_vendorarch}/FCGI.pm
%{_mandir}/man3/FCGI.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.82-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.82-11
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.82-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.82-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.82-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.82-7
- Perl 5.38 rebuild

* Mon Jun 12 2023 Petr Pisar <ppisar@redhat.com> - 1:0.82-6
- Specify all dependencies
- Package examples
- Package the tests

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.82-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.82-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.82-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Aug 01 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 1:0.82-1
- Update to 0.82

* Sun Jul 25 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 1:0.80-1
- Update to 0.80

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.79-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.79-7
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.79-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.79-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.79-4
- Perl 5.32 rebuild

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 1:0.79-3
- Spec file cleanups: Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMake

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


