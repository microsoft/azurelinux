Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Net-Daemon
Version:        0.49
Release:        14%{?dist}
Summary:        Perl extension for portable daemons

License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Net-Daemon
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/Net-Daemon-%{version}.tar.gz#/perl-Net-Daemon-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl-doc
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl-Pod-Perldoc
BuildRequires:  sed
# Run-time:
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
%{?_with_network_tests:
BuildRequires:  perl(Sys::Syslog)
}
# Thread not used at tests
# threads not used at tests
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(Test::More)
# Network tests:
%{?_with_network_tests:
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(lib)
BuildRequires:  perl(Socket)
}
Suggests:       perl(Sys::Syslog)
# threads is prefered over Threads
Suggests:       perl(threads)
Requires:       perl(threads::shared)

%{?perl_default_filter}

%description
Net::Daemon is an abstract base class for implementing portable server 
applications in a very simple way. The module is designed for Perl 5.006 and 
ithreads (and higher), but can work with fork() and Perl 5.004.

The Net::Daemon class offers methods for the most common tasks a daemon 
needs: Starting up, logging, accepting clients, authorization, restricting 
its own environment for security and doing the true work. You only have to 
override those methods that aren't appropriate for you, but typically 
inheriting will safe you a lot of work anyways.


%prep
%setup -q -n Net-Daemon-%{version}
# Convert EOL
/usr/bin/sed -i 's/\r//' README

# generate our other two licenses...
/usr/bin/perldoc perlgpl > LICENSE.GPL
/usr/bin/perldoc perlartistic > LICENSE.Artistic


%build
/usr/bin/perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}


%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*


%check
%{?!_with_network_tests:
# Disable tests which will fail under mock
  rm t/config*
  rm t/fork*
  rm t/ithread*
  rm t/loop*
  rm t/single.t
  rm t/unix.t
}

%{make_build} test


%files
%doc ChangeLog README
%license LICENSE.*
%{perl_vendorlib}/Net*
%{_mandir}/man3/Net*.3*


%changelog
* Mon Dec 16 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 0.49-14
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-7
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-4
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 22 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 0.49-2
- Specify fill path to programs used in spec file
- Use the %%{_fixperms} macro

* Sun Sep 27 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 0.49-1
- Update to 0.49
- Pass NO_PACKLIST=1 NO_PERLLOCAL=1 to Makefile.PL
- Use %%{make_install} instead of "make pure_install"
- Use %%{make_build} instead of make
- Replace %%{__perl} with /usr/bin/perl

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-26
- Perl 5.32 rebuild

* Tue Mar 10 2020 Petr Pisar <ppisar@redhat.com> - 0.48-25
- Specify all dependencies

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-22
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-19
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-16
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-14
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-11
- Perl 5.22 rebuild

* Tue Oct 21 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.48-10
- Remove no-longer-needed macros
- Use the %%license tag
- Be more specific when listing files
- Add perl default filter

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-9
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.48-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Petr Pisar <ppisar@redhat.com> - 0.48-4
- Specify all dependencies
- Correct README end-of-lines

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 0.48-2
- Perl 5.16 rebuild

* Mon Jan 16 2012 Petr Lautrbach <plautrba@redhat.com> 0.48-1
- Update to 0.48 version
- Fix build requires

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.44-13
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.44-12
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.44-10
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.44-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.44-8
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 13 2008 Petr Lautrbach <plautrba@redhat.com> 0.44-5
- "--with network_tests" - don't remove network tests 
* Mon Oct  6 2008 Petr Lautrbach <plautrba@redhat.com> 0.44-4
- Description and License fixed
- Patch without backup 
* Mon Oct  6 2008 Petr Lautrbach <lautrba@redhat.com> 0.44-3
- Requires: fixed 
* Fri Oct  3 2008 Petr Lautrbach <lautrba@redhat.com> 0.44-2
- only-ithreads patch added
- disabled tests which fail under mock
* Fri Sep 26 2008 Petr Lautrbach <lautrba@redhat.com>
- initial rpm release
