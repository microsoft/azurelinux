%global cpan_version 6.57
# Filter underspecified dependencies
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(AnyEvent\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(AnyEvent\\) >= 4.800001$
%global __requires_exclude %{__requires_exclude}|^perl\\(AnyEvent::AIO\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(AnyEvent::BDB\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(EV\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(Event\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(Guard\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(Storable\\)$
%global __provides_exclude %{?__provides_exclude:__provides_exclude|}^perl\\(Coro\\)$

Summary:        The only real threads in perl
Name:           perl-Coro
Version:        6.570
Release:        5%{?dist}
# Coro/libcoro:    GPLv2 or BSD
# Rest of package: GPL+ or Artistic
License:        (GPL+ OR Artistic) AND (GPLv2 OR BSD)
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Coro
Source0:        https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/Coro-%{cpan_version}.tar.gz
Patch0:         %{name}-5.25-ucontext-default.patch
# Do not disable hardening
Patch1:         Coro-6.512-Disable-disabling-FORTIFY_SOURCE.patch

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  libecb-static
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  sed
# Run-time:
BuildRequires:  perl(AnyEvent) >= 7
# AnyEvent::AIO >= 1 not used at tests
# AnyEvent::BDB >= 1 not used at tests
# AnyEvent::DNS not used at tests
BuildRequires:  perl(AnyEvent::Socket)
BuildRequires:  perl(AnyEvent::Util)
BuildRequires:  perl(Canary::Stability)
# BDB not used at tests
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(EV) >= 4
BuildRequires:  perl(EV::MakeMaker)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Event) >= 1.08
BuildRequires:  perl(Event::MakeMaker) >= 6.76
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.52
BuildRequires:  perl(Guard) >= 0.5
# IO::AIO >= 3.1 not used at tests
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Storable) >= 2.15
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(base)
BuildRequires:  perl(common::sense)
# Net::Config not used at tests
# Net::FTP not used at tests
# Net::HTTP not used at tests
# Net::NNTP not used at tests
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Export correct required versions
Requires:       perl(AnyEvent) >= 7
Requires:       perl(AnyEvent::AIO) >= 1
Requires:       perl(AnyEvent::BDB) >= 1
Requires:       perl(EV) >= 4
Requires:       perl(Event) >= 1.08
Requires:       perl(Guard) >= 0.5
Requires:       perl(Storable) >= 2.15
Requires:       perl(warnings)
%{?perl_default_filter}

%description
This module collection manages continuations in general, most often in the
form of cooperative threads (also called coros, or simply "coro" in the
documentation). They are similar to kernel threads but don't (in general) run
in parallel at the same time even on SMP machines. The specific flavor of
thread offered by this module also guarantees you that it will not switch
between threads unless necessary, at easily-identified points in your
program, so locking and parallel access are rarely an issue, making thread
programming much safer and easier than using other thread models.

%prep
%setup -q -n Coro-%{cpan_version}

%ifnarch %{ix86} x86_64 %{arm}
# use ucontext backend on non-x86 (setjmp didn't work on s390(x))
%patch0 -p1 -b .ucontext-default
%endif
%patch1 -p1

# Unbundle libecb
rm Coro/ecb.h
perl -i -lne 'print $_ unless m{\ACoro/ecb\.h\z}' MANIFEST
perl -i -pe 's/ecb\.h//' Coro/Makefile.PL

# Correct shebangs
for F in Coro/jit-*.pl; do
    perl -i -ne 'print $_ unless m{\A#!}' "$F"
    chmod -x "$F"
done
%fix_shbang_line eg/myhttpd


%build
# Interactive configuration. Use default values.
perl Makefile.PL INSTALLDIRS=perl NO_PACKLIST=1 NO_PERLLOCAL=1 \
    OPTIMIZE="%{optflags}" </dev/null
%make_build

%install
%make_install
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

%check
%make_build test

%files
%license COPYING Coro/libcoro/LICENSE
%doc Changes README README.linux-glibc
%doc doc/* eg
%{perl_archlib}/auto/Coro
%{perl_archlib}/Coro
%{perl_archlib}/Coro.pm
%{_mandir}/man3/Coro*.3pm*

%changelog
* Thu Jan 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.570-5
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.570-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 6.570-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.570-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Petr Pisar <ppisar@redhat.com> - 6.570-1
- 6.57 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.550-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.550-4
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.550-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.550-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Petr Pisar <ppisar@redhat.com> - 6.550-1
- 6.55 bump

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.540-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.540-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 19 2018 Petr Pisar <ppisar@redhat.com> - 6.540-1
- 6.42 bump

* Wed Aug 15 2018 Petr Pisar <ppisar@redhat.com> - 6.520-1
- 6.52 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.514-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 08 2018 Carl George <carl@george.computer> - 6.514-4
- Avoid NO_PACKLIST usage to work with EL7's MakeMaker

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.514-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.514-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 01 2017 Petr Pisar <ppisar@redhat.com> - 6.514-1
- 6.514 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.513-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.513-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Petr Pisar <ppisar@redhat.com> - 6.513-1
- 6.513 bump

* Fri Jul 14 2017 Petr Pisar <ppisar@redhat.com> - 6.512-1
- 6.512 bump

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.511-4
- Perl 5.26 rebuild

* Tue May 23 2017 Petr Pisar <ppisar@redhat.com> - 6.511-3
- Restore compatibility with Perl 5.26.0 (CPAN RT#121836)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.511-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 27 2016 Petr Pisar <ppisar@redhat.com> - 6.511-1
- 6.511 bump

* Fri May 20 2016 Petr Pisar <ppisar@redhat.com> - 6.49-4
- Make Coro compatible with Perl 5.24 (bug #1338707)

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.49-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 19 2015 Petr Pisar <ppisar@redhat.com> - 6.49-1
- 6.49 bump

* Mon Oct 05 2015 Petr Pisar <ppisar@redhat.com> - 6.48-1
- 6.48 bump

* Mon Jul 13 2015 Petr Pisar <ppisar@redhat.com> - 6.47-1
- 6.47 bump

* Wed Jul 01 2015 Petr Pisar <ppisar@redhat.com> - 6.46-1
- 6.46 bump

* Tue Jun 30 2015 Petr Pisar <ppisar@redhat.com> - 6.45-1
- 6.45 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.43-2
- Perl 5.22 rebuild

* Mon Jun 08 2015 Petr Pisar <ppisar@redhat.com> - 6.43-1
- 6.43 bump

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.42-2
- Perl 5.22 rebuild

* Wed Feb 18 2015 Petr Pisar <ppisar@redhat.com> - 6.42-1
- 6.42 bump

* Wed Oct 29 2014 Petr Pisar <ppisar@redhat.com> - 6.41-1
- 6.41 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.39-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Petr Pisar <ppisar@redhat.com> - 6.39-1
- 6.39 bump

* Wed Mar 05 2014 Petr Pisar <ppisar@redhat.com> - 6.37-1
- 6.37 bump

* Tue Nov 19 2013 Petr Pisar <ppisar@redhat.com> - 6.33-1
- 6.33 bump

* Wed Nov 06 2013 Petr Pisar <ppisar@redhat.com> - 6.32-1
- 6.32 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 6.31-2
- Perl 5.18 rebuild

* Mon May 13 2013 Petr Pisar <ppisar@redhat.com> - 6.31-1
- 6.31 bump

* Thu May 09 2013 Petr Pisar <ppisar@redhat.com> - 6.29-1
- 6.29 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Petr Pisar <ppisar@redhat.com> - 6.23-1
- 6.23 bump

* Mon Oct 22 2012 Petr Pisar <ppisar@redhat.com> - 6.10-3
- Do not mark this package as bundling libecb

* Mon Oct 22 2012 Petr Pisar <ppisar@redhat.com> - 6.10-2
- Unbundle libecb (bug #863988)

* Fri Oct 12 2012 Petr Pisar <ppisar@redhat.com> - 6.10-1
- 6.10 bump

* Mon Oct 08 2012 Petr Pisar <ppisar@redhat.com> - 6.09-2
- Fix building on big endian system (bug #863991)

* Sun Oct 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 6.09-1
- Update to 4.09

* Fri Aug  3 2012 Jitka Plesnikova <jplesnik@redhat.com> - 6.08-4
- Update BR

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 6.08-2
- Perl 5.16 rebuild

* Mon Apr 16 2012 Petr Pisar <ppisar@redhat.com> - 6.08-1
- 6.08 bump

* Tue Feb 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 6.07-3
- Add patch to fix build on ARM. RHBZ 750805

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Petr Pisar <ppisar@redhat.com> - 6.07-1
- 6.07 bump

* Thu Nov 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 6.06-2
- Fix ucontext on ARM - rhbz750805

* Fri Aug 12 2011 Petr Sabata <contyk@redhat.com> - 6.06-1
- 6.06 bump

* Fri Aug 05 2011 Petr Sabata <contyk@redhat.com> - 6.05-1
- 6.05 bump

* Thu Aug 04 2011 Petr Sabata <contyk@redhat.com> - 6.04-1
- 6.04 bump

* Fri Jul 29 2011 Petr Pisar <ppisar@redhat.com> - 6.02-1
- 6.02 bump
- Major version 6 breaks compatibility: Unreferenced coro objects will now be
  destroyed and cleaned up automatically (e.g. async { schedule }).

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 5.372-4
- Perl mass rebuild

* Fri Apr 08 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 5.372-3
- Added explicit versionned Requires: on perl(EV)
- Removed automatically added unversionned Requires: on perl(EV)

* Thu Apr 07 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 5.372-2
- Rebuild with EV support.

* Mon Mar 07 2011 Petr Pisar <ppisar@redhat.com> - 5.372-1
- 5.372 bump

* Mon Feb 21 2011 Petr Pisar <ppisar@redhat.com> - 5.37-1
- 5.37 bump
- Fix State.xs syntax (RT#65991)
- Version unversioned Provides

* Mon Feb 14 2011 Petr Pisar <ppisar@redhat.com> - 5.26-1
- 5.26 bump

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Mathieu Bridon <bochecha@fedoraproject.org> 5.25-3
- Allow building on systems without %%fix_shbang_line macro (needed for EL6)

* Mon Jan 10 2011 Dan Horák <dan[at]danny.cz> 5.25-2
- use ucontext backend on non-x86

* Tue Jan 04 2011 Petr Pisar <ppisar@redhat.com> 5.25-1
- 5.25 import
- Disable perl(EV) support as it's not packaged yet
