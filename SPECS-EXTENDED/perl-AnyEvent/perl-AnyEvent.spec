#global subver 1

# A noarch-turned-arch package should not have debuginfo
%global debug_package %{nil}

# Use weak dependencies where available
%global have_weak_deps 0%{?fedora} > 20 || 0%{?rhel} > 7

Name:           perl-AnyEvent
Version:        7.17
Release:        3%{?dist}
Summary:        Framework for multiple event loops
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/AnyEvent
Source0:        https://cpan.metacpan.org/modules/by-module/AnyEvent/AnyEvent-%{version}%{?subver}.tar.gz#/perl-AnyEvent-%{version}%{?subver}.tar.gz

# Build requirements
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter >= 3:5.8.1
BuildRequires:  perl(Canary::Stability)
BuildRequires:  perl(ExtUtils::MakeMaker)

# Module requirements
BuildRequires:  perl(B)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Guard)
BuildRequires:  perl(integer)
BuildRequires:  perl(JSON::XS)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Storable)
BuildRequires:  perl(strict)
BuildRequires:  perl(Sys::Syslog)
BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(Unicode::Normalize)

# Test suite requirements
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Net::SSLeay) >= 1.33
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)

# Event loop testing
#
# Many of these modules require or build-require AnyEvent themselves,
# so don't do event loop testing when bootstrapping
#
# Cocoa, FLTK and UV are not in Fedora/EPEL
# AnyEvent::AIO, EV and IO::Async::Loop are not (yet) in EPEL-7
# Test suite does not currently test the Qt event loop
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(Event)
BuildRequires:  perl(Glib) >= 1.210
BuildRequires:  perl(POE) >= 1.312
BuildRequires:  perl(Tk)

BuildRequires:  perl(AnyEvent::AIO)
BuildRequires:  perl(EV) >= 4.00
BuildRequires:  perl(IO::AIO) >= 4.13
BuildRequires:  perl(IO::Async::Loop) >= 0.33

%endif

# Runtime requires
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::Temp)
%if %{have_weak_deps}
# Optional but recommended
Recommends:     perl(Guard)
Recommends:     perl(Storable)
Recommends:     perl(Sys::Syslog)
Recommends:     perl(Task::Weaken)
Recommends:     perl(Unicode::Normalize)
# Heavier optional modules
Suggests:       perl(CBOR::XS)
Suggests:       perl(Coro)
Suggests:       perl(Coro::Debug)
Suggests:       perl(JSON::XS)
Suggests:       perl(Net::SSLeay) >= 1.33
%else
Requires:       perl(Guard)
Requires:       perl(Storable)
Requires:       perl(Sys::Syslog)
Requires:       perl(Task::Weaken)
Requires:       perl(Unicode::Normalize)
%endif

# Optional dependencies we don't want to require
%global optional_deps                  AnyEvent::AIO
%global optional_deps %{optional_deps}|Cocoa::EventLoop
%global optional_deps %{optional_deps}|EV
%global optional_deps %{optional_deps}|Event
%global optional_deps %{optional_deps}|Event::Lib
%global optional_deps %{optional_deps}|EventLoop
%global optional_deps %{optional_deps}|FLTK
%global optional_deps %{optional_deps}|Glib
%global optional_deps %{optional_deps}|IO::AIO
%global optional_deps %{optional_deps}|IO::Async::Loop
%global optional_deps %{optional_deps}|Irssi
%global optional_deps %{optional_deps}|POE
%global optional_deps %{optional_deps}|Qt
%global optional_deps %{optional_deps}|Qt::isa
%global optional_deps %{optional_deps}|Qt::slots
%global optional_deps %{optional_deps}|Tk
%global optional_deps %{optional_deps}|UV

# Don't include optional dependencies
%global __requires_exclude ^perl[(](%{optional_deps})[)]

# Filter unversioned and bogus provides
# AnyEvent::Impl::{Cocoa,FLTK,UV} are filtered as the required
# underlying modules are not currently available in Fedora
%global __provides_exclude ^perl[(](AnyEvent(::Impl::(Cocoa|FLTK|UV))?|DB)[)]$


%description
AnyEvent provides an identical interface to multiple event loops. This allows
module authors to utilize an event loop without forcing module users to use the
same event loop (as multiple event loops cannot coexist peacefully at any one
time).


%prep
%setup -q -n AnyEvent-%{version}%{?subver}


%build
PERL_CANARY_STABILITY_NOPROMPT=1 perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}


%check
# PERL_ANYEVENT_NET_TESTS shouldn't be set to avoid network tests
# on our builder.
export PERL_ANYEVENT_LOOP_TESTS=1
make test


%files
%license COPYING
%doc Changes README
%{perl_vendorarch}/AE.pm
%{perl_vendorarch}/AnyEvent.pm
%{perl_vendorarch}/AnyEvent/
%{_mandir}/man3/AE.3*
%{_mandir}/man3/AnyEvent.3*
%{_mandir}/man3/AnyEvent::DNS.3*
%{_mandir}/man3/AnyEvent::Debug.3*
%{_mandir}/man3/AnyEvent::FAQ.3*
%{_mandir}/man3/AnyEvent::Handle.3*
%{_mandir}/man3/AnyEvent::Impl::Cocoa.3*
%{_mandir}/man3/AnyEvent::Impl::EV.3*
%{_mandir}/man3/AnyEvent::Impl::Event.3*
%{_mandir}/man3/AnyEvent::Impl::EventLib.3*
%{_mandir}/man3/AnyEvent::Impl::FLTK.3*
%{_mandir}/man3/AnyEvent::Impl::Glib.3*
%{_mandir}/man3/AnyEvent::Impl::IOAsync.3*
%{_mandir}/man3/AnyEvent::Impl::Irssi.3*
%{_mandir}/man3/AnyEvent::Impl::POE.3*
%{_mandir}/man3/AnyEvent::Impl::Perl.3*
%{_mandir}/man3/AnyEvent::Impl::Qt.3*
%{_mandir}/man3/AnyEvent::Impl::Tk.3*
%{_mandir}/man3/AnyEvent::Impl::UV.3*
%{_mandir}/man3/AnyEvent::Intro.3*
%{_mandir}/man3/AnyEvent::IO.3*
%{_mandir}/man3/AnyEvent::IO::IOAIO.3*
%{_mandir}/man3/AnyEvent::IO::Perl.3*
%{_mandir}/man3/AnyEvent::Log.3*
%{_mandir}/man3/AnyEvent::Loop.3*
%{_mandir}/man3/AnyEvent::Socket.3*
%{_mandir}/man3/AnyEvent::Strict.3*
%{_mandir}/man3/AnyEvent::TLS.3*
%{_mandir}/man3/AnyEvent::Util.3*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.17-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 18 2019 Paul Howarth <paul@city-fan.org> - 7.17-1
- Update to 7.17
  - Work around antique openssl version in RHEL-7 by formatting dh parameters
    differently
  - Add t/13_weaken.t

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 Paul Howarth <paul@city-fan.org> - 7.16-1
- Update to 7.16
  - Add ffdhe group dh parameters from RFC 7919, and use ffdhe3072 as new
    default, instead of schmorp1539
  - AnyEvent::Log did not re-assess logging status of AnyEvent::Log::loggers
    when contexts were changed with ->attach/detach/slaves, causing them not to
    log even though a recent attach should have caused them to log
  - Added some more logging configuration examples
  - Mention RFC 8482 in AnyEvent::DNS
- ffdhe group dh parameters require OpenSSL ≥ 1.0.2 (CPAN RT#130116)

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 7.15-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 7.15-2
- Perl 5.30 rebuild

* Tue Feb 26 2019 Paul Howarth <paul@city-fan.org> - 7.15-1
- Update to 7.15
  - INCOMPATIBLE CHANGE: AnyEvent::Handle's tls_detect documentation gave
    separate major and minor versions, while code passed only a single value;
    this version follows the documentation and now passes separate major and
    minor values
  - Work around Net::SSLeay not having been ported to openssl 1.1, but many
    distributions compiling it against openssl 1.1, which unfortunately
    succeeds and results in a very broken module
  - AnyEvent::DNS::dns_unpack now stores the original DNS packet in the __
    member, to allow decoding of undecodable resource records containing
    compressed domain names
  - AnyEvent::Socket::parse_ipv6 would NOT, as advertised, accept ipv4
    addresses; it now does and converts them to ipv4 mapped addresses
  - Support CAA records
  - Add freenom and cloudflare nameservers as DNS fallback
  - AnyEvent::Strict would not properly ward against io watchers on files when
    the handle passed was a file descriptor
  - Document "internal" variables used by the DNS en-/decoder to allow
    enterprising users to extend them in a semi-official way

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 7.14-6
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 7.14-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 24 2017 Paul Howarth <paul@city-fan.org> - 7.14-1
- Update to 7.14
  - Fix a crash bug in AnyEvent::Handle with openssl 1.1.0
  - AnyEvent::Handle->keepalive was documented (and defined) twice
  - AnyEvent::Socket::tcp_bind/tcp_server would immediately unlink a unix
    listening socket unless a guard is used; change this so that no clean-up
    will be performed unless a guard is used and document this more clearly
  - Make tcp_bind/tcp_server error messages more regular
  - Fix building on Perl without '.' in @INC
  - Add TCP_FASTOPEN/MSG_FASTOPEN and MSG_NOSIGNAL/MSG_MORE/MSG_DONTWAIT to
    constants
  - Update warnings to common::sense 3.74 standards

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 7.13-8
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 7.13-7
- Perl 5.26 rebuild

* Wed May 17 2017 Jitka Plesnikova <jplesnik@redhat.com> - 7.13-6
- Fix building on Perl without '.' in @INC

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 25 2016 Paul Howarth <paul@city-fan.org> - 7.13-4
- Fix segfault in SSL handling that manifests on OpenSSL 1.1.0 x86_64
  (CPAN RT#118584, RHBZ#1390468)

* Tue Nov  1 2016 Paul Howarth <paul@city-fan.org> - 7.13-3
- Avoid interactive prompt during build (#1390463)
- For now, BuildConflict with perl-Net-SSLeay on Rawhide (#1390468)

* Mon Oct 17 2016 Paul Howarth <paul@city-fan.org> - 7.13-2
- Add some optional dependencies (#1385642)
- Work around SSL issues in Rawhide (possibly due to ongoing upgrade to
  OpenSSL 1.1.0)

* Mon Sep 19 2016 Paul Howarth <paul@city-fan.org> - 7.13-1
- Update to 7.13
  - Only call tlsext_host_name for non-empty common names
  - Log a (single) notice message if SNI is not supported
  - Upgrade to UTS-46:9.0.0 draft and switch to non-transitional behaviour
    (see also https://bugzilla.mozilla.org/show_bug.cgi?id=1218179)
  - It turns out that the UTS-46 IDNA testcase failures were indeed bugs in the
    testcases and the specification and not in the code - the post-9.0.0
    unicode files have all known problems fixed, so finally the AnyEvent IDNA
    implementation can pass the full IDNA testsuite - without needing a single
    fix
  - Guarantee (and document) that condvar callbacks will be removed on
    invocation - important to avoid circular references
- Simplify find command using -delete
- Use %%license unconditionally

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 7.12-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 7.12-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Paul Howarth <paul@city-fan.org> - 7.12-1
- Update to 7.12
  - Use common name as hostname for TLS connects, if Net::SSLeay supports SNI
  - Fix documentation of tls_autostart read type in AnyEvent::Handle

* Wed Aug 26 2015 Petr Šabata <contyk@redhat.com> - 7.11-2
- Prevent FTBFS by adding a missing build time dependency

* Fri Jul 17 2015 Paul Howarth <paul@city-fan.org> - 7.11-1
- Update to 7.11
  - AnyEvent::Socket::parse_ipv6 could accept malformed ipv6 addresses (extra
    "::" at end and similar cases)
  - Add a more explicit warning to AnyEvent::Handle that it doesn't work on
    files; people keep getting confused
  - New function AnyEvent::Socket::tcp_bind
  - New functions AnyEvent::fh_block and AnyEvent::fh_unblock
  - Aligned ipv6 address formatting with RFC 5952 (by not shortening a single
    :0: to ::)
  - Added stability canary support

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 7.09-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 7.09-2
- Perl 5.22 rebuild

* Sat May  2 2015 Paul Howarth <paul@city-fan.org> - 7.09-1
- Update to 7.09
  - AnyEvent::Debug called an internal function (AnyEvent::Log::ft) that was
    renamed to AnyEvent::Log:format_time, under its old name
  - Update AnyEvent::DNS fallback resolver addresses: it seems google
    effectively killed most other free dns resolvers, so remove them, but add
    Cable and Wireless (ecrc) since it was stable for 20 years or so, official
    or not, and there should be an alternative to google
  - perl5porters broke Windows error codes in 5.20, and mapped WSAEWOULDBLOCK
    on the (different) EWOULDBLOCK error code, and WSAEINPROGRESS into the
    incompatible ERINPROGRESS code (there may be others too); this version
    only works around the WSAEWOULDBLOCK issue, because I don't have a nice
    way to work around the WSAEINPROGRESS bug

* Wed Dec 10 2014 Paul Howarth <paul@city-fan.org> - 7.08-1
- Update to 7.08:
  - Work around a newly introduced bug in Socket 2.011 (an erroneous sun_length
    check)
  - AnyEvent::TLS didn't load (but refer to) AnyEvent::Socket
  - AnyEvent::Strict will now confess, not croak, in line with it being a
    development/debugging tool
  - Work around a number of libglib bugs (debug builds of libglib enforce
    certain undocumented behaviour patterns such as not being able to remove a
    child watch source after it has fired, which we will try to emulate to
    avoid "criticals"; what were they thinking?)
  - Mention json security issues in AnyEvent::Handle
  - Changed default DNS resolver "max_outstanding" value from 1 to 10, the
    latter being the intended value all along
  - Added new "AnyEvent::Impl::UV" interface module to the UV event lib

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 7.07-6
- Perl 5.20 re-rebuild of bootstrapped packages

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 7.07-5
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 21 2014 Paul Howarth <paul@city-fan.org> - 7.07-3
- Avoid some optional test dependencies for EPEL builds so that we can get
  an EPEL-7 build done
- Use %%license where possible

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 17 2013 Paul Howarth <paul@city-fan.org> - 7.07-1
- Update to 7.07:
  - The documentation for custom tls verify schemes was wrong; make it agree
    with the code
  - Added cbor read and write types to AnyEvent::Handle (using CBOR::XS)
  - Work around an API change in openssl that could cause wrong tls connection
    aborts, likely on windows only
  - Calling AnyEvent->now_update with AnyEvent::Impl::Perl caused an endless
    loop
  - Add tlsv1_1 and tlsv1_2 protocols to AnyEvent::TLS
  - Document AnyEvent::Impl::IOAsync::set_loop and
    $AnyEvent::Impl::IOAsync::LOOP; though only documented now, this
    functionality has always been available
  - Force a toplevel domain name in t/81_hosts.t
  - Document that AnyEvent::Log uses AnyEvent::IO
  - Warn about AnyEvent::Filesys::Notify performance
  - Praise the joys of AnyEvent::Fork::*
  - Time for an =encoding directive
  - No longer use JSON to create a default json coder; use JSON::XS or JSON::PP
    directly

* Wed Aug 21 2013 Paul Howarth <paul@city-fan.org> - 7.05-1
- Update to 7.05:
   - uts46data.pl couldn't be found due to wrong naming of the file
   - Handle lone \015's properly in AE::Handle's default line read
   - Untaint IP addresses found in /etc/hosts
   - The memleak fix in 7.03 caused resolving via /etc/hosts always to fail on
     first use
   - Expose AnyEvent::Log::format_time, and allow users to redefine it
   - Expose AnyEvent::Log::default_format, and allow redefinition
   - Expose AnyEvent::Log::fatal_exit, to allow redefinition
   - AnyEvent::Debug shell can now run coro shell commands, if available
   - t/63* tests were wrongly in MANIFEST
   - kernel.org's finger server went MIA, switch to freebsd.org and icculus.org
   - Clarify that IO::AIO and AnyEvent::AIO are needed for AnyEvent::IO to
     function asynchronously
   - Hard-disable $^W in most tests; it generates too much garbage output
   - Use a (hopefully) more future-proof method to emulate common::sense
   - Upgrade to UTS-46:6.2.0
   - Switch to INSTLIB from INSTLIBDIR, as INSTLIBDIR was wrongly documented;
     should not affect anything
- Don't BR: perl(Event::Lib) as that back-end is not tested
- BR: perl(IO::Async::Loop) for the test suite now that there's a new enough
  version available
- BR: perl(File::Temp) for the test suite

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 7.04-5
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 7.04-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Paul Howarth <paul@city-fan.org> - 7.04-1
- Update to 7.04:
  - AnyEvent::Socket::inet_aton did not work when DNS resolution was used to
    find the addresses
  - Fix a memory leak in the /etc/hosts lookup code when hosts don't resolve
    and are not in hosts

* Tue Aug 21 2012 Paul Howarth <paul@city-fan.org> - 7.02-1
- Update to 7.02:
  - AnyEvent::Util::run_cmd could block indefinitely
  - Verified that AnyEvent::Socket follows RFC5952
  - Try to parse "ADDR#PORT" in addition to "ADDR PORT"
- Make %%files list more explicit

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 7.01-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 7.01-2
- Perl 5.16 rebuild

* Sun May 13 2012 Paul Howarth <paul@city-fan.org> - 7.01-1
- Update to 7.01:
  - Fail with EPROTO in AnyEvent::Handle when TLS is requested but not
    available, instead of throwing an exception
  - Use File::Spec to get the tmpdir in t/*, to avoid needless failures on
    (most, not mine :) windows boxes
  - New handle read types: tls_detect and tls_autostart
- BR: perl(File::Spec)

* Thu Apr 26 2012 Paul Howarth <paul@city-fan.org> - 7.0-1
- Update to 7.0
- Package generates no debuginfo, so avoid creation of debuginfo sub-package
- Add explicit build requirements for the module's needs
- Add build requirements for as much event loop testing as is possible in
  Fedora, breaking potential build dependency cycles by use of the
  %%{perl_bootstrap} macro
- Clean up spec for modern rpmbuild:
  - Drop %%defattr, redundant since rpm 4.4
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Drop buildroot definition and cleaning
  - Drop requires/provides filters for rpm versions prior to 4.9
- Simplify requires/provides filtering
- Explicitly require perl(Task::Weaken) as per upstream recommendation

* Mon Apr 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 6.14-2
- Filter requires perl(FLTK) perl(Cocoa) - rhbz#815496
- Filter perl(IO::Async::Loop) to reintroduce later.
- Remove filter on perl(AnyEvent::Impl::Qt) since there is perl(Qt)

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 6.14-1
- Update to 6.14
- Make the package arch specific

* Mon Jan 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 6.13-1
- Update to 6.13

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jul 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.34-1
- Update to 5.34

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 5.27-6
- RPM 4.9 dependency filtering added

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 5.27-5
- Perl mass rebuild

* Thu Feb 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.27-4
- Rewritten to new filtering rules
 https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering#Perl

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.27-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Aug 22 2010 Nicolas Chauvet <kwizart@gmail.com> - 5.27-1
- Update to 5.271 (rpm version : 5.27)

* Thu Apr 29 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 5.26-1
- Update to 5.261 (rpm version : 5.26)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.24-2
- Mass rebuild with perl-5.12.0

* Tue Jan 19 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 5.24-1
- Update to 5.24  (rpm version : 5.24)

* Mon Dec 7 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 5.22-1
- Update to 5.22  (rpm version : 5.22)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 5.11-3
- rebuild against perl 5.10.1

* Mon Aug 31 2009 kwizart < kwizart at gmail.com > - 5.11-2
- Update to 5.112   (rpm version : 5.11 )

* Mon Jul 27 2009 kwizart < kwizart at gmail.com > - 4.870-1
- Update to 4.87   (rpm version : 4.870 )
- Add more filter requires to workaround rhbz#512553

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.820-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 kwizart < kwizart at gmail.com > - 4.820-1
- Update to 4.82   (rpm version : 4.820 )

* Fri May 29 2009 kwizart < kwizart at gmail.com > - 4.410-1
- Update to 4.41   (rpm version : 4.41 )

* Wed Apr 22 2009 kwizart < kwizart at gmail.com > - 4.352-1
- Update to 4.352   (rpm version : same )

* Fri Apr  3 2009 kwizart < kwizart at gmail.com > - 4.350-1
- Update to 4.35   (rpm version : 4.350 )

* Thu Mar  5 2009 kwizart < kwizart at gmail.com > - 4.340-1
- Update to 4.34   (rpm version : 4.340 )

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.331-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 kwizart < kwizart at gmail.com > - 4.331-1
- Update to 4.331   (rpm version : same )

* Fri Oct 17 2008 kwizart < kwizart at gmail.com > - 4.300-1
- Update to 4.3   (rpm version : 4.300 )

* Tue Oct 14 2008 kwizart < kwizart at gmail.com > - 4.3-1
- Update to 4.3

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 4.231-1
- Update to 4.231 (rpm version : match )

* Fri Jul 18 2008 kwizart < kwizart at gmail.com > - 4.220-1
- Update to 4.22 (rpm version : 4.220 )

* Fri Jul 18 2008 kwizart < kwizart at gmail.com > - 4.21-1
- Update to 4.21

* Fri Jul  4 2008 kwizart < kwizart at gmail.com > - 4.161-1
- Update to 4.161

* Mon Jun 23 2008 kwizart < kwizart at gmail.com > - 4.152-1
- Update to 4.152

* Mon Jun  9 2008 kwizart < kwizart at gmail.com > - 4.151-1
- Update to 4.151

* Thu Jun  5 2008 kwizart < kwizart at gmail.com > - 4.13-1
- Update to 4.13

* Tue Jun  3 2008 kwizart < kwizart at gmail.com > - 4.12-1
- Update to 4.12

* Thu May 29 2008 kwizart < kwizart at gmail.com > - 4.1-1
- Update to 4.1

* Tue May 27 2008 kwizart < kwizart at gmail.com > - 3.5-1
- Update to 3.5

* Wed Apr 30 2008 kwizart < kwizart at gmail.com > - 3.3-1
- Initial package for Fedora

