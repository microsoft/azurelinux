Name:           perl-Mojolicious
Version:        8.57
Release:        3%{?dist}
Summary:        A next generation web framework for Perl
License:        Artistic 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Mojolicious
Source0:        https://cpan.metacpan.org/authors/id/S/SR/SRI/Mojolicious-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.16.0
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Benchmark)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Raw::Zlib)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(CPAN::Meta::YAML)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Errno)
# EV 4.0 not used at tests
BuildRequires:  perl(experimental)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(feature)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::stat)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Hash::Util::FieldHash)
BuildRequires:  perl(integer)
BuildRequires:  perl(IO::Compress::Gzip)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Poll)
BuildRequires:  perl(IO::Socket::IP) >= 0.37
BuildRequires:  perl(IO::Socket::UNIX)
BuildRequires:  perl(IO::Uncompress::Gunzip)
BuildRequires:  perl(JSON::PP) >= 2.27103
BuildRequires:  perl(List::Util) >= 1.41
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(mro)
BuildRequires:  perl(overload)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(re)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Sub::Util)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(Time::Local) >= 1.2
BuildRequires:  perl(Unicode::Normalize)
BuildRequires:  perl(utf8)
# Optional run-time:
BuildRequires:  perl(Role::Tiny) >= 2.000001
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(lib)
# Test::Future::AsyncAwait::Awaitable not used
Requires:       perl(:MODULE_COMPAT_%(eval "`/usr/bin/perl -V:version`"; echo $version))
Suggests:       perl(Cpanel::JSON::XS) >= 4.09
Requires:       perl(experimental)
Requires:       perl(FindBin)
# Future::AsyncAwait 0.36 not yet packaged
Requires:       perl(IO::Socket::IP) >= 0.37
Suggests:       perl(IO::Socket::Socks) >= 0.64
Suggests:       perl(IO::Socket::SSL) >= 2.009
Requires:       perl(JSON::PP) >= 2.27103
# Net::DNS::Native 0.15 not yet packaged
Suggests:       perl(Role::Tiny) >= 2.000001
Requires:       perl(Time::Local) >= 1.2

%{?perl_default_filter}
# EV is just one supported reactor backend, Mojo can use others, and
# ithreads-based code actually cannot use EV:
# https://mojolicio.us/perldoc/Mojolicious/Guides/FAQ#What-does-the-error-EV-does-not-work-with-ithreads-mean
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}perl\\(VMS|perl\\(Win32|perl\\(EV
# Remove under-specified dependencies
%global __requires_exclude %{__requires_exclude}|^perl\\((IO::Socket::IP|JSON::PP|Time::Local)\\)$

%package -n perl-Test-Mojo
Summary:        Test::Mojo perl Module
Requires:       perl(:MODULE_COMPAT_%(eval "`/usr/bin/perl -V:version`"; echo $version))

%description -n perl-Test-Mojo
%{summary}

%description
Back in the early days of the web there was this wonderful Perl library
called CGI, many people only learned Perl because of it. It was simple
enough to get started without knowing much about the language and powerful
enough to keep you going, learning by doing was much fun. While most of the
techniques used are outdated now, the idea behind it is not. Mojolicious is
a new attempt at implementing this idea using state of the art technology.

%prep
%setup -q -n Mojolicious-%{version}
mv README.md lib/Mojolicious/

%build
/usr/bin/perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{make_build} test

%files
%license LICENSE
%doc Changes examples
%{_bindir}/mojo
%{_bindir}/hypnotoad
%{_bindir}/morbo
%{perl_vendorlib}/*
%exclude %{perl_vendorlib}/Test
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n perl-Test-Mojo
%{perl_vendorlib}/Test

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.57-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 26 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.57-1
- Update to 8.57

* Mon Jun 29 2020 Jitka Plesnikova <jplesnik@redhat.com> - 8.56-2
- Perl 5.32 re-rebuild updated packages

* Sun Jun 28 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.56-1
- Update to 8.56

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 8.53-2
- Perl 5.32 rebuild

* Sun Jun 14 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.53-1
- Update to 8.53

* Sun May 31 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.51-1
- Update to 8.51

* Sun May 31 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.50-1
- Update to 8.50

* Sun May 10 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.42-1
- Update to 8.42

* Sun May 03 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.41-1
- Update to 8.41

* Sun Apr 26 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.40-1
- Update to 8.40

* Sun Apr 19 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.37-1
- Update to 8.37

* Sun Apr 05 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.36-1
- Update to 8.36

* Sun Mar 22 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.35-1
- Update to 8.35

* Wed Mar 11 2020 Petr Pisar <ppisar@redhat.com> - 8.33-2
- Specify all dependencies

* Sun Feb 16 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.33-1
- Update to 8.33

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.32-1
- Update to 8.32

* Sun Jan 19 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.31-1
- Update to 8.31

* Sun Jan 12 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 8.30-1
- Update to 8.30

* Sun Dec 29 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.29-1
- Update to 8.29

* Sun Dec 08 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.27-1
- Update to 8.27

* Sun Nov 03 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.26-1
- Update to 8.26

* Sun Sep 29 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.25-1
- Update to 8.25

* Sun Sep 15 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.24-1
- Update to 8.24

* Sun Aug 18 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.23-1
- Update to 8.23
- Replace calls to %%{__perl} with /usr/bin/perl
- Replace calls to "make pure_install" with %%{make_install}
- Replace calls to "make" with %%{make_build}
- Pass NO_PERLLOCAL=1 to Makefile.PL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Adam Williamson <awilliam@redhat.com> - 8.22-1
- Update to 8.22

* Sun Jul 14 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.20-1
- Update to 8.20

* Sun Jun 30 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.18-1
- Update to 8.18

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 8.17-2
- Perl 5.30 rebuild

* Sun May 26 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.17-1
- Update to 8.17

* Sun May 19 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.16-1
- Update to 8.16

* Sun Apr 28 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.15-1
- Update to 8.15

* Sun Apr 21 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.14-1
- Update to 8.14

* Sun Mar 24 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.13-1
- Update to 8.13

* Sun Feb 03 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.12-1
- Update to 8.12

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 06 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 8.11-1
- Update to 8.11

* Sun Dec 23 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 8.10-1
- Update to 8.10

* Sun Dec 09 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 8.09-1
- Update to 8.09

* Sun Nov 25 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 8.07-1
- Update to 8.07

* Sun Nov 11 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 8.06-1
- Update to 8.06

* Sun Nov 04 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 8.05-1
- Update to 8.05

* Sun Oct 28 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 8.04-1
- Update to 8.04

* Sun Oct 21 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 8.03-1
- Update to 8.03

* Sun Oct 07 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 8.02-1
- Update to 8.02

* Sun Sep 16 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 8.0-1
- Update to 8.0

* Sun Sep 09 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.94-1
- Update to 7.94

* Sun Aug 19 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.93-1
- Update to 7.93

* Sun Aug 12 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.92-1
- Update to 7.92

* Sun Jul 15 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.88-1
- Update to 7.88

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 7.85-2
- Perl 5.28 rebuild

* Sun Jun 24 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.85-1
- Update to 7.85

* Sun Jun 10 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.84-1
- Update to 7.84

* Sun Jun 03 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.82-1
- Update to 7.82

* Sun May 27 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.81-1
- Update to 7.81

* Sun May 20 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.79-1
- Update to 7.79
- Change URL and Source to use metacpan
- Use DESTDIR instead of PERL_INSTALL_ROOT

* Sun May 13 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.78-1
- Update to 7.78

* Sun May 06 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.77-1
- Update to 7.77

* Sun Apr 29 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.76-1
- Update to 7.76

* Wed Apr 11 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.75-1
- Update to 7.75

* Sun Apr 08 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.74-1
- Update to 7.74

* Sun Mar 18 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.71-1
- Update to 7.71

* Thu Mar 01 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.70-1
- Update to 7.70

* Sun Feb 25 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.69-1
- Update to 7.69

* Tue Feb 20 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.67-1
- Update to 7.67

* Sun Feb 18 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.66-1
- Update to 7.66

* Thu Feb 08 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.64-1
- Update to 7.64

* Sun Feb 04 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.62-1
- Update to 7.62

* Sun Jan 21 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.61-1
- Update to 7.61

* Sun Jan 07 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 7.60-1
- Update to 7.60

* Sun Dec 24 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.59-1
- Update to 7.59

* Thu Dec 07 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.58-1
- Update to 7.58

* Sun Nov 19 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.57-1
- Update to 7.57

* Sun Nov 12 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.55-1
- Update to 7.55

* Sat Nov 04 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.52-1
- Update to 7.52

* Sun Oct 22 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.48-1
- Update to 7.48

* Sun Oct 15 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.47-1
- Update to 7.47

* Sun Sep 17 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.46-1
- Update to 7.46

* Fri Sep 08 2017 Adam Williamson <awilliam@redhat.com> - 7.45-1
- Update to 7.45

* Sun Aug 20 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.43-1
- Update to 7.43

* Sun Aug 06 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.39-1
- Update to 7.39

* Fri Jul 28 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.37-1
- Update to 7.37

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.36-1
- Update to 7.36

* Sun Jul 09 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.35-1
- Update to 7.35

* Sat Jun 10 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.33-1
- Update to 7.33

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 7.31-2
- Perl 5.26 rebuild

* Thu Apr 27 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.31-1
- Update to 7.31

* Sun Apr 09 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.30-1
- Update to 7.30

* Sun Mar 19 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.29-1
- Update to 7.29

* Thu Mar 09 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.28-1
- Update to 7.28

* Sun Mar 05 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.27-1
- Update to 7.27

* Sun Feb 26 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.26-1
- Update to 7.26

* Sun Feb 12 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.25-1
- Update to 7.25

* Mon Feb 06 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.24-1
- Update to 7.24

* Mon Jan 30 2017 Adam Williamson <awilliam@redhat.com> - 7.23-1
- Update to 7.23

* Sun Jan 29 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.22-1
- Update to 7.22

* Tue Jan 24 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.21-1
- Update to 7.21

* Sun Jan 22 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.20-1
- Update to 7.20

* Sun Jan 08 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 7.14-1
- Update to 7.14

* Sun Dec 25 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 7.12-1
- Update to 7.12

* Sun Dec 04 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 7.11-1
- Update to 7.11

* Sun Nov 06 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 7.10-1
- Update to 7.10

* Sun Oct 23 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 7.09-1
- Update to 7.09

* Sat Sep 24 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 7.08-1
- Update to 7.08

* Sun Sep 18 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 7.06-1
- Update to 7.06

* Sat Sep 03 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 7.05-1
- Update to 7.05

* Thu Aug 25 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 7.03-1
- Update to 7.03

* Sun Aug 07 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 7.01-1
- Update to 7.01

* Sat Jul 23 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 7.0-1
- Update to 7.0

* Sat Jun 18 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.66-1
- Update to 6.66

* Fri Jun 10 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.64-1
- Update to 6.64

* Sat Jun 04 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.63-1
- Update to 6.63

* Sat May 21 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.62-1
- Update to 6.62

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.61-2
- Perl 5.24 rebuild

* Fri May 06 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.61-1
- Update to 6.61

* Sun Mar 27 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.57-1
- Update to 6.57

* Fri Mar 11 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.55-1
- Update to 6.55

* Sat Mar 05 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.53-1
- Update to 6.53

* Fri Feb 19 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.46-1
- Update to 6.46

* Wed Feb 10 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.45-3
- Remove BuildRequires for Test::Mojo (BR don't apply to subpackages)

* Wed Feb 10 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.45-2
- Add Requires and BuildRequires to the Test::Mojo subpackage (#1306300)

* Wed Feb 10 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.45-1
- Update to 6.45

* Sun Feb 07 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.44-1
- Update to 6.44

* Thu Feb 04 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 6.42-2
- Split out Test::Mojo (Avoid runtime dep on Test::More, RHBZ#1304630).

* Sun Jan 31 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.42-1
- Update to 6.42

* Sun Jan 24 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.41-1
- Update to 6.41

* Fri Jan 15 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.40-1
- Update to 6.40

* Fri Jan 08 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 6.39-1
- Update to 6.39

* Mon Dec 28 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.38-1
- Update to 6.38

* Mon Dec 21 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.37-1
- Update to 6.37

* Fri Dec 11 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.36-1
- Update to 6.36

* Sun Dec 06 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.35-1
- Update to 6.35

* Sun Nov 29 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.33-1
- Update to 6.33

* Sun Nov 15 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.31-1
- Update to 6.31

* Sat Oct 31 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.27-1
- Update to 6.27

* Thu Oct 22 2015 Adam Williamson <awilliam@redhat.com> - 6.24-2
- don't require perl(EV) - it's optional and some things *cannot* use it

* Sun Oct 18 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.24-1
- Update to 6.24

* Fri Oct 09 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.23-1
- Update to 6.23

* Fri Oct 02 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.22-1
- Update to 6.22

* Fri Sep 25 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.21-1
- Update to 6.21

* Fri Sep 18 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.20-1
- Update to 6.20

* Sun Sep 06 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.18-1
- Update to 6.18

* Sun Aug 30 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.17-1
- Update to 6.17

* Sun Aug 16 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.15-1
- Update to 6.15

* Tue Jul 14 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.14-1
- Update to 6.14
- Add perl(Time::Local) as a BR (#1242789)

* Sun Jul 12 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.13-1
- Update to 6.13

* Fri Jun 19 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.12-1
- Update to 6.12

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.11-2
- Perl 5.22 rebuild

* Sun May 17 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.11-1
- Update to 6.11

* Sun May 10 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.10-1
- Update to 6.10

* Sun Apr 12 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.08-1
- Update to 6.08

* Sun Mar 29 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.05-1
- Update to 6.05

* Sun Mar 22 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.03-1
- Update to 6.03

* Sun Mar 15 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.02-1
- Update to 6.02

* Sun Mar 08 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.01-1
- Update to 6.01

* Sun Mar 01 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.0-2
- rebuilt

* Sun Mar 01 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 6.0-1
- Update to 6.0

* Sun Feb 22 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 5.81-1
- Update to 5.81

* Sun Feb 15 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 5.79-1
- Update to 5.79
- Cleanup spec file

* Sun Feb 08 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 5.77-1
- Update to 5.77

* Sun Feb 01 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 5.75-1
- Update to 5.75

* Sun Jan 25 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 5.74-1
- Update to 5.74

* Sun Jan 18 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 5.72-1
- Update to 5.72

* Sun Jan 04 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 5.71-1
- Update to 5.71

* Fri Dec 19 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.70-1
- Update to 5.70

* Sun Dec 14 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.69-1
- Update to 5.69

* Thu Dec 04 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.68-1
- Update to 5.68

* Fri Nov 28 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.67-1
- Update to 5.67

* Sat Nov 22 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.63-1
- Update to 5.63

* Sat Nov 15 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.61-1
- Update to 5.61

* Sun Nov 09 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.59-1
- Update to 5.59

* Sun Nov 02 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.56-1
- Update to 5.56

* Fri Oct 24 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.54-2
- Bump to rebuild

* Fri Oct 24 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.54-1
- Update to 5.54

* Sun Oct 19 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.52-1
- Update to 5.52

* Sun Oct 12 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.49-1
- Update to 5.49

* Sun Oct 05 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.47-1
- Update to 5.47

* Sat Sep 27 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.45-1
- Update to 5.45

* Sun Sep 21 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.42-1
- Update to 5.42

* Sun Sep 14 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.41-1
- Update to 5.41

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 5.38-2
- Perl 5.20 rebuild

* Sat Sep 06 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.38-1
- Update to 5.38

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 5.35-2
- Perl 5.20 rebuild

* Sun Aug 31 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.35-1
- Update to 5.35

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 5.29-2
- Perl 5.20 rebuild

* Sun Aug 17 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.29-1
- Update to 5.29
- Use %%license

* Sun Aug 03 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.24-1
- Update to 5.24

* Sun Jul 20 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.15-1
- Update to 5.15

* Sun Jul 06 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.12-1
- Update to 5.12
- Change upstream URL

* Sun Jun 29 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.10-1
- Update to 5.10

* Sun Jun 22 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.08-1
- Update to 5.08

* Sun Jun 15 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.07-1
- Update to 5.07

* Sun Jun 08 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.04-1
- Update to 5.04

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jun 01 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 5.02-1
- Update to 5.02

* Sun May 18 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.99-1
- Update to 4.99

* Sun May 11 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.98-1
- Update to 4.98

* Sun May 04 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.97-1
- Update to 4.97

* Sun Apr 27 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.95-1
- Update to 4.95

* Sun Apr 20 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.94-1
- Update to 4.94

* Sun Apr 13 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.93-1
- Update to 4.93

* Sun Mar 30 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.91-1
- Update to 4.91

* Sun Mar 23 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.90-1
- Update to 4.90

* Sun Mar 16 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.89-1
- Update to 4.89

* Sun Mar 09 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.87-1
- Update to 4.87

* Sun Mar 02 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.85-1
- Update to 4.85

* Sun Feb 23 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.84-1
- Update to 4.84

* Sun Feb 16 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.81-1
- Update to 4.81

* Sun Feb 09 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.78-1
- Update to 4.78

* Sun Feb 02 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.75-1
- Update to 4.75

* Sun Jan 26 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.69-1
- Update to 4.69

* Sun Jan 12 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.67-1
- Update to 4.67

* Sun Jan 05 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 4.66-1
- Update to 4.66

* Sun Dec 22 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.63-1
- Update to 4.63

* Sun Dec 15 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.59-1
- Update to 4.59

* Sun Nov 24 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.58-1
- Update to 4.58

* Sun Nov 17 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.57-1
- Update to 4.57

* Sun Nov 10 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.56-1
- Update to 4.56

* Sun Nov 03 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.53-1
- Update to 4.53

* Sun Oct 27 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.50-1
- Update to 4.50

* Sun Oct 20 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.49-1
- Update to 4.49

* Sun Oct 13 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.46-1
- Update to 4.46

* Sun Oct 06 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.44-1
- Update to 4.44

* Sun Sep 22 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.41-1
- Update to 4.41

* Sun Sep 15 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.37-1
- Update to 4.37

* Sun Sep 08 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.33-1
- Update to 4.33

* Sun Sep 01 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.29-1
- Update to 4.29

* Sun Aug 25 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.26-1
- Update to 4.26

* Sun Aug 18 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.25-1
- Update to 4.25

* Sat Aug 10 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.24-1
- Update to 4.24

* Mon Aug 05 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.23-1
- Update to 4.23
- Fix incorrect dates in the spec changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.18-2
- Perl 5.18 rebuild

* Sat Jul 13 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.18-1
- Update to 4.18

* Sun Jul 07 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.17-1
- Update to 4.17

* Sun Jun 23 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.16-1
- Update to 4.16

* Sun Jun 16 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.14-1
- Update to 4.14

* Sun Jun 09 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.13-1
- Update to 4.13

* Sun Jun 02 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.10-1
- Update to 4.10

* Sun May 26 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.07-1
- Update to 4.07

* Sun May 19 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 4.0-1
- Update to 4.0

* Sun Apr 28 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.97-1
- Update to 3.97

* Sun Apr 21 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.95-1
- Update to 3.95

* Sun Apr 07 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.93-1
- Update to 3.93

* Sun Mar 31 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.91-1
- Update to 3.91

* Sun Mar 17 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.90-1
- Update to 3.90

* Sun Mar 10 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.89-1
- Update to 3.89

* Sun Feb 24 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.87-1
- Update to 3.87

* Sun Feb 17 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.85-1
- Update to 3.85

* Sat Feb 02 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.84-1
- Update to 3.84

* Sun Jan 27 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.83-1
- Update to 3.83

* Sun Jan 20 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.82-1
- Update to 3.82

* Sun Jan 13 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.79-1
- Update to 3.79

* Sun Jan 06 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 3.72-1
- Update to 3.72

* Sun Dec 30 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.70-1
- Update to 3.70

* Sun Dec 23 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.69-2
- Fix the date of the previous entry in the changelog

* Sun Dec 23 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.69-1
- Update to 3.69
- Remove the Group macro (no longer used)

* Sun Dec 16 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.68-1
- Update to 3.68

* Sun Dec 09 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.65-1
- Update to 3.65

* Sun Dec 02 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.64-1
- Update to 3.64

* Sun Nov 25 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.61-1
- Update to 3.61

* Sun Nov 18 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.57-1
- Update to 3.57

* Sun Nov 11 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.56-1
- Update to 3.56

* Sun Nov 04 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.54-1
- Update to 3.54

* Sun Oct 28 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.52-1
- Update to 3.52

* Sun Oct 21 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.50-1
- Update to 3.50

* Sun Oct 14 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.47-1
- Update to 3.47

* Fri Oct 12 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.46-1
- Update to 3.46

* Sun Sep 30 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.44-1
- Update to 3.44

* Sun Sep 23 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.43-1
- Update to 3.43

* Sun Sep 16 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.41-1
- Update to 3.41

* Sun Sep 09 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.38-1
- Update to 3.38

* Tue Sep 04 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 3.36-1
- Update to 3.36
- Add perl default filter

* Tue Aug 14 2012 Yanko Kaneti <yaneti@declera.com> - 3.30-1
- Update to 3.30

* Mon Aug  6 2012 Yanko Kaneti <yaneti@declera.com> - 3.21-1
- Update to 3.21

* Thu Aug  2 2012 Yanko Kaneti <yaneti@declera.com> - 3.19-1
- Update to 3.19

* Wed Aug  1 2012 Yanko Kaneti <yaneti@declera.com> - 3.17-1
- Update to 3.17

* Mon Jul 30 2012 Yanko Kaneti <yaneti@declera.com> - 3.15-1
- Update to 3.15

* Wed Jul 25 2012 Yanko Kaneti <yaneti@declera.com> - 3.13-1
- Update to 3.13

* Fri Jul 20 2012 Yanko Kaneti <yaneti@declera.com> - 3.12-1
- Update to 3.12

* Wed Jul 18 2012 Yanko Kaneti <yaneti@declera.com> - 3.10-1
- Update to 3.10

* Fri Jul 13 2012 Yanko Kaneti <yaneti@declera.com> - 3.07-1
- Update to 3.07

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 3.0-2
- Perl 5.16 rebuild

* Tue Jun 26 2012 Yanko Kaneti <yaneti@declera.com> - 3.0-1
- Update to 3.0

* Wed Jun 20 2012 Yanko Kaneti <yaneti@declera.com> - 2.98-2
- Bump for build into f18-perl

* Wed Jun 20 2012 Yanko Kaneti <yaneti@declera.com> - 2.98-1
- Update to 2.98

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.95-2
- Perl 5.16 rebuild

* Fri May 11 2012 Yanko Kaneti <yaneti@declera.com> - 2.95-1
- Update to 2.95

* Wed May  2 2012 Yanko Kaneti <yaneti@declera.com> - 2.92-1
- Update to 2.92

* Sat Apr 21 2012 Yanko Kaneti <yaneti@declera.com> - 2.85-1
- Update to 2.85

* Sat Mar 31 2012 Yanko Kaneti <yaneti@declera.com> - 2.70-1
- Update to 2.70

* Wed Mar 28 2012 Yanko Kaneti <yaneti@declera.com> - 2.69-1
- Update to 2.69

* Fri Mar  2 2012 Yanko Kaneti <yaneti@declera.com> - 2.56-1
- Update to 2.56

* Mon Feb 20 2012 Yanko Kaneti <yaneti@declera.com> - 2.51-1
- Update to 2.51

* Tue Feb 14 2012 Yanko Kaneti <yaneti@declera.com> - 2.49-1
- Update to 2.49

* Wed Jan 25 2012 Robin Lee <cheeselee@fedoraproject.org> - 2.45-1
- Update to 2.45

* Wed Jan 18 2012 Yanko Kaneti <yaneti@declera.com> - 2.44-1
- Update to 2.44

* Wed Jan 11 2012 Yanko Kaneti <yaneti@declera.com> - 2.43-1
- Update to 2.43

* Tue Jan  3 2012 Yanko Kaneti <yaneti@declera.com> - 2.42-1
- Update to 2.42

* Fri Dec 30 2011 Yanko Kaneti <yaneti@declera.com> - 2.41-1
- Update to 2.41

* Mon Dec 26 2011 Yanko Kaneti <yaneti@declera.com> - 2.40-1
- Update to 2.40

* Thu Dec 22 2011 Yanko Kaneti <yaneti@declera.com> - 2.39-1
- Update to 2.39

* Mon Dec 19 2011 Yanko Kaneti <yaneti@declera.com> - 2.38-1
- Update to 2.38. Add Digest::MD5 dep.

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 1.99-1
- update to 1.99

* Thu Sep 15 2011 Yanko Kaneti <yaneti@declera.com> - 1.98-1
- Upstream update 1.98

* Fri Aug 26 2011 Robin Lee <cheeselee@fedoraproject.org> - 1.92-1
- Upstream update 1.92

* Tue Jul 26 2011 Yanko Kaneti <yaneti@declera.com> - 1.65-1
- Upstream update 1.65

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.46-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.46-2
- Perl mass rebuild

* Tue Jun 21 2011 Robin Lee <cheeselee@fedoraproject.org> - 1.46-1
- Upstream update 1.46

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.43-2
- Perl mass rebuild

* Mon Jun 13 2011 Yanko Kaneti <yaneti@declera.com> 1.43-1
- Upstream update 1.43.

* Fri Jun 10 2011 Yanko Kaneti <yaneti@declera.com> 1.42-1
- Upstream update 1.42.

* Fri Jun  3 2011 Yanko Kaneti <yaneti@declera.com> 1.41-1
- Latest from upstream - 1.41.

* Wed May 25 2011 Yanko Kaneti <yaneti@declera.com> 1.34-1
- Upstream update 1.34.

* Sat May 21 2011 Yanko Kaneti <yaneti@declera.com> 1.33-1
- Upstream update 1.33.

* Wed May 11 2011 Yanko Kaneti <yaneti@declera.com> 1.32-1
- Upstream update 1.32.

* Tue May 10 2011 Yanko Kaneti <yaneti@declera.com> 1.31-1
- Upstream update 1.31.

* Tue May  3 2011 Yanko Kaneti <yaneti@declera.com> 1.22-1
- Upstream update 1.22.

* Sun Apr 17 2011 Yanko Kaneti <yaneti@declera.com> 1.16-1
- Security bugfix 1.16.

* Sat Mar 19 2011 Yanko Kaneti <yaneti@declera.com> 1.15-1
- Serious bugfix... 1.15.

* Fri Mar 18 2011 Yanko Kaneti <yaneti@declera.com> 1.14-1
- New bugfix release from upstream 1.14.

* Mon Mar 14 2011 Yanko Kaneti <yaneti@declera.com> 1.13-1
- Update to latest upstream 1.13.

* Tue Feb 22 2011 Yanko Kaneti <yaneti@declera.com> 1.11-1
- Update to latest upstream 1.11.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 27 2010 Yanko Kaneti <yaneti@declera.com> 1.0-1
- Update to latest upstream 1.0.

* Mon Dec  6 2010 Yanko Kaneti <yaneti@declera.com> 0.999950-1
- Update to latest upstream 0.999950.
  New included experimental web server - hypnotoad.

* Mon Nov 22 2010 Yanko Kaneti <yaneti@declera.com> 0.999941-1
- Latest upstream release.

* Tue Nov 16 2010 Yanko Kaneti <yaneti@declera.com> 0.999940-1
- New upstream release. Turns off IPv6 support. Bugfixes.

* Wed Nov 10 2010 Yanko Kaneti <yaneti@declera.com> 0.999938-1
- New upstream release. MojoX is gone.

* Fri Nov  5 2010 Yanko Kaneti <yaneti@declera.com> 0.999936-1
- New upstream bugfix release.

* Thu Nov  4 2010 Yanko Kaneti <yaneti@declera.com> 0.999935-1
- Latest upstream release.
  https://search.cpan.org/src/KRAIH/Mojolicious-0.999935/Changes

* Thu Aug 19 2010 Yanko Kaneti <yaneti@declera.com> 0.999929-1
- Latest upstream release.
  https://search.cpan.org/src/KRAIH/Mojolicious-0.999929/Changes

* Mon Aug 16 2010 Yanko Kaneti <yaneti@declera.com> 0.999927-1
- Latest upstream release.
  https://search.cpan.org/src/KRAIH/Mojolicious-0.999927/Changes

* Tue Jun 22 2010 Petr Pisar <ppisar@redhat.com> 0.999926-2
- Rebuild against perl-5.12

* Wed Jun 16 2010 Yanko Kaneti <yaneti@declera.com> 0.999926-1
- Latest upstream release.
  https://search.cpan.org/src/KRAIH/Mojolicious-0.999926/Changes

* Fri Jun 11 2010 Yanko Kaneti <yaneti@declera.com> 0.999925-3
- Actually include the examples.

* Fri Jun 11 2010 Yanko Kaneti <yaneti@declera.com> 0.999925-2
- Initial import. Include examples as doc.

* Tue Jun 08 2010 Yanko Kaneti <yaneti@declera.com> 0.999925-1
- Specfile mostly autogenerated by cpanspec 1.78.
