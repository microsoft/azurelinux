# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?rhel} >= 9
%bcond_with perl_IO_Socket_SSL_test_unused_idn
%bcond_with perl_IO_Socket_SSL_test_IO_Socket_INET6
%else
%bcond_without perl_IO_Socket_SSL_test_unused_idn
%bcond_without perl_IO_Socket_SSL_test_IO_Socket_INET6
%endif

Name:		perl-IO-Socket-SSL
Version:	2.095
Release: 3%{?dist}
Summary:	Perl library for transparent SSL
License:	(GPL-1.0-or-later OR Artistic-1.0-Perl) AND MPL-2.0
URL:		https://metacpan.org/release/IO-Socket-SSL
Source0:	https://cpan.metacpan.org/modules/by-module/IO/IO-Socket-SSL-%{version}.tar.gz
Patch0:		IO-Socket-SSL-2.089-use-system-default-cipher-list.patch
Patch1:		IO-Socket-SSL-2.094-use-system-default-SSL-version.patch
# A test for Enable-Post-Handshake-Authentication-TLSv1.3-feature.patch,
# bug #1632660, requires openssl tool
Patch2:		IO-Socket-SSL-2.087-Test-client-performs-Post-Handshake-Authentication.patch
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:	openssl-libs >= 0.9.8
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(constant)
BuildRequires:	perl(Errno)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(HTTP::Tiny)
BuildRequires:	perl(IO::Socket)
BuildRequires:	perl(IO::Socket::INET)
BuildRequires:	perl(IO::Socket::IP) >= 0.31
BuildRequires:	perl(Net::SSLeay) >= 1.46
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Socket) >= 1.95
BuildRequires:	perl(strict)
BuildRequires:	perl(URI::_idna)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
# Test Suite
# openssl tool required for Test-client-performs-Post-Handshake-Authentication.patch
BuildRequires:	openssl
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(FindBin)
BuildRequires:	perl(IO::Select)
%if %{with perl_IO_Socket_SSL_test_IO_Socket_INET6}
BuildRequires:	perl(IO::Socket::INET6) >= 2.62
%endif
# IPC::Run for Test-client-performs-Post-Handshake-Authentication.patch
BuildRequires:	perl(IPC::Run)
%if %{with perl_IO_Socket_SSL_test_unused_idn}
BuildRequires:	perl(Net::IDN::Encode)
BuildRequires:	perl(Net::LibIDN)
%endif
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(utf8)
BuildRequires:	procps
# Dependencies
Requires:	openssl-libs >= 0.9.8
Requires:	perl(Config)
Requires:	perl(HTTP::Tiny)
Requires:	perl(IO::Socket::INET)
Requires:	perl(IO::Socket::IP) >= 0.31
Requires:	perl(Socket) >= 1.95
Requires:	perl(URI::_idna)

%description
This module is a true drop-in replacement for IO::Socket::INET that
uses SSL to encrypt data before it is transferred to a remote server
or client. IO::Socket::SSL supports all the extra features that one
needs to write a full-featured SSL client or server application:
multiple SSL contexts, cipher selection, certificate verification, and
SSL version selection. As an extra bonus, it works perfectly with
mod_perl.

%prep
%setup -q -n IO-Socket-SSL-%{version}

# Use system-wide default cipher list to support use of system-wide
# crypto policy (#1076390, #1127577, CPAN RT#97816)
# https://fedoraproject.org/wiki/Changes/CryptoPolicy
%patch -P 0

# Use system-default SSL version too
%patch -P 1

# Add a test for PHA
%patch -P 2 -p1

%build
NO_NETWORK_TESTING=1 perl Makefile.PL \
	INSTALLDIRS=vendor \
	NO_PACKLIST=1 \
	NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
# GPL-1.0-or-later OR Artistic-1.0-Perl
%doc BUGS Changes README docs/ example/
%dir %{perl_vendorlib}/IO/
%dir %{perl_vendorlib}/IO/Socket/
%dir %{perl_vendorlib}/IO/Socket/SSL/
%doc %{perl_vendorlib}/IO/Socket/SSL.pod
%{perl_vendorlib}/IO/Socket/SSL.pm
%{perl_vendorlib}/IO/Socket/SSL/Intercept.pm
%{perl_vendorlib}/IO/Socket/SSL/Utils.pm
%{_mandir}/man3/IO::Socket::SSL.3*
%{_mandir}/man3/IO::Socket::SSL::Intercept.3*
%{_mandir}/man3/IO::Socket::SSL::Utils.3*
# MPL-2.0
%{perl_vendorlib}/IO/Socket/SSL/PublicSuffix.pm
%{_mandir}/man3/IO::Socket::SSL::PublicSuffix.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.095-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Paul Howarth <paul@city-fan.org> - 2.095-1
- Update to 2.095
  - Regression: make sysread set buffer to empty string again when returning EOF
    (GH#171)

* Thu Jun 19 2025 Paul Howarth <paul@city-fan.org> - 2.094-1
- Update to 2.094
  - Fix memory leak introduced in 2.092

* Tue Jun 17 2025 Paul Howarth <paul@city-fan.org> - 2.093-1
- Update to 2.093
  - Rework for one-sided SSL shutdown, to implement a useful and secure
    behavior without affecting existing applications

* Thu Jun 12 2025 Paul Howarth <paul@city-fan.org> - 2.091-1
- Update to 2.091
  - Fix behavior on one-sided SSL shutdown; if the application continued to
    read after half-closing the SSL connection, this could result in reading
    encrypted data (i.e. close notify, SSL session tickets...)
  - See documentation of stop_SSL for detailed description of handling
    half-closed SSL connections

* Tue Jun  3 2025 Paul Howarth <paul@city-fan.org> - 2.090-1
- Update to 2.090
  - Fix OCSP live test after Let's Encrypt has disabled OCSP support (GH#169)
  - public_suffix now preserves trailing dot (GH#167)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.089-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 29 2024 Paul Howarth <paul@city-fan.org> - 2.089-1
- Update to 2.089
  - New option SSL_force_fingerprint to enforce fingerprint matching even if
    certificate validation would be successful without
  - Document _get_ssl_object and _get_ctx_object for cases where direct use of
    Net::SSLeay functions is needed

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.088-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Paul Howarth <paul@city-fan.org> - 2.088-1
- Update to 2.088 (rhbz#2297795)
  - Minor fixes for use on ancient versions of perl and for building with newer
    versions of openssl

* Wed Jul 10 2024 Yanko Kaneti <yaneti@declera.com> - 2.087-2
- Pick an upstream fix for runtime warning

* Mon Jul  8 2024 Paul Howarth <paul@city-fan.org> - 2.087-1
- Update to 2.087
  - Internal optimzation: implement _touch_entry in session cache instead of
    using del+add
  - Support for PSK, see SSL_psk in documentation

* Tue Jan 23 2024 Paul Howarth <paul@city-fan.org> - 2.085-1
- Update to 2.085
  - Fix test that failed due to behavior changes in OpenSSL 3.2 (GH#147)
  - Update PublicSuffix
  - Add examples for TLS JA3/JA4 fingerprinting to tls_fingerprint/

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.084-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov  7 2023 Paul Howarth <paul@city-fan.org> - 2.084-1
- Update to 2.084
  - Various fixes for edge cases and build: GH#136, GH#141, GH#142, GH#143,
    GH#145
  - Update documentation to reflect default SSL_version

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.083-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.083-2
- Disable optional IO::Socket::INET6 tests on ELN

* Thu May 18 2023 Paul Howarth <paul@city-fan.org> - 2.083-1
- Update to 2.083
  - Fix t/protocol_version.t for OpenSSL versions that don't support SECLEVEL
    (regression from GH#122)

* Thu May 18 2023 Paul Howarth <paul@city-fan.org> - 2.082-1
- Update to 2.082
  - SSL_version default now TLS 1.2+ since TLS 1.1 and lower are deprecated
    (GH#122)
  - Fix output of alert string when debugging (GH#132)
  - Improve regex for hostname validation (GH#130, GH#126)
  - Add can_ciphersuites subroutine for feature checking (GH#127)
  - Utils::CERT_create - die if unexpected arguments are given instead of
    ignoring these
- Avoid use of deprecated patch syntax

* Wed Jan 25 2023 Paul Howarth <paul@city-fan.org> - 2.081-1
- Update to 2.081
  - New function set_msg_callback for user defined callback on each SSL message
  - Showcase function in example/ssl_client.pl and example/ssl_server.pl for
    computing JA3S/JA3 fingerprints
  - Fix tracing added in 2.076 to no longer include SSL3_RT_HEADER (noise)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.080-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Paul Howarth <paul@city-fan.org> - 2.080-1
- Update to 2.080
  - Move test certificates into t/ directory where they belong

* Mon Jan 16 2023 Paul Howarth <paul@city-fan.org> - 2.079-1
- Update to 2.079
  - Properly extract IPv6 address for verification from PeerAddr if
    not explicitly given as SSL_verifycn_name (GH#123)

* Mon Dec 12 2022 Paul Howarth <paul@city-fan.org> - 2.078-1
- Update to 2.078
  - Revert decision from 2014 to not verify hostname by default if hostname is
    IP address but no explicit verification scheme given (GH#121)

* Mon Nov 21 2022 Paul Howarth <paul@city-fan.org> - 2.077-1
- Update to 2.077
  - Fix memory leak in session cache (GH#118)
  - More race conditions in tests fixed (GH#97)

* Mon Nov 14 2022 Paul Howarth <paul@city-fan.org> - 2.076-1
- Update to 2.076
 - Added curl like tracing (based on GH#117)
 - Fixed race condition in t/sni_verify.t (GH#97)

* Sat Sep  3 2022 Paul Howarth <paul@city-fan.org> - 2.075-1
- Update to 2.075
  - Treat SSL_write returning 0 same as previously -1, as suggested by both
    OpenSSL and LibreSSL documentation
  - Propagate error from SSL_shutdown, unless the shutdown is caused by an outer
    SSL error, in which case keep the original error
  - Small test fixes
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.074-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.074-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.074-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan  8 2022 Paul Howarth <paul@city-fan.org> - 2.074-1
- Update to 2.074
  - Add SSL_ciphersuites option for TLS 1.3 ciphers
  - No longer use own default for ciphers: instead, use system default but
    disable some weak ciphers that might still be enabled on older systems

* Thu Dec 23 2021 Paul Howarth <paul@city-fan.org> - 2.073-1
- Update to 2.073
  - Fix behavior and tests for OpenSSL 3.0.1
  - Fix GH#110 - prevent internal error warning in some cases

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.072-2
- Rebuilt with OpenSSL 3.0.0

* Tue Aug 17 2021 Paul Howarth <paul@city-fan.org> - 2.072-1
- Update to 2.072
  - Add PEM_certs2file and PEM_file2certs in IO::Socket::SSL::Utils based on
    idea in GH#101
  - certs/*.p12 used for testing should now work with OpenSSL 3.0 too (GH#108)
  - Update public suffix database
- Drop patch for building with OpenSSL 1.1.1e

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.071-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 25 2021 Paul Howarth <paul@city-fan.org> - 2.071-1
- Update to 2.071
  - Fix t/nonblock.t race on some systems (fixes GH#102, maybe GH#98 too)

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.070-3
- Perl 5.34 rebuild

* Fri Mar 19 2021 Petr Pisar <ppisar@redhat.com> - 2.070-2
- Disable optional libidn tests on ELN

* Fri Feb 26 2021 Paul Howarth <paul@city-fan.org> - 2.070-1
- Update to 2.070
  - Changed bugtracker in Makefile.PL to GitHub, away from obsolete rt.cpan.org

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.069-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Paul Howarth <paul@city-fan.org> - 2.069-1
- Update to 2.069
  - IO::Socket::Utils CERT_asHash and CERT_create now support subject and
    issuer with multiple same parts (like multiple OU); in this case an array
    ref instead of a scalar is used as hash value (GH#95)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.068-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-2
- Perl 5.32 rebuild

* Tue Mar 31 2020 Paul Howarth <paul@city-fan.org> - 2.068-1
- Update to 2.068
  - Treat OpenSSL 1.1.1e as broken and refuse to build with it in order to
    prevent follow-up problems in tests and user code
    https://github.com/noxxi/p5-io-socket-ssl/issues/93
    https://github.com/openssl/openssl/issues/11388
    https://github.com/openssl/openssl/issues/11378
  - Update PublicSuffix with latest data from publicsuffix.org
- Patch out the refusal to build with OpenSSL 1.1.1e as the OpenSSL package in
  Fedora has had the problematic EOF-handling change reverted

* Sat Mar 21 2020 Paul Howarth <paul@city-fan.org> - 2.067-2
- Fix FTBFS with OpenSSL 1.1.1e
  https://github.com/noxxi/p5-io-socket-ssl/issues/93

* Sat Feb 15 2020 Paul Howarth <paul@city-fan.org> - 2.067-1
- Update to 2.067
  - Fix memory leak on incomplete handshake (GH#92)
  - Add support for SSL_MODE_RELEASE_BUFFERS via SSL_mode_release_buffers; this
    can decrease memory usage at the costs of more allocations (CPAN RT#129463)
  - More detailed error messages when loading of certificate file failed (GH#89)
  - Fix for ip_in_cn == 6 in verify_hostname scheme (CPAN RT#131384)
  - Deal with new MODE_AUTO_RETRY default in OpenSSL 1.1.1
  - Fix warning when no ecdh support is available
  - Documentation update regarding use of select and TLS 1.3
  - Various fixes in documentation (GH#81, GH#87, GH#90, GH#91)
  - Stability fix for t/core.t

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.066-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Petr Pisar <ppisar@redhat.com> - 2.066-7
- Default to PROFILE=SYSTEM cipher list (bug #1775167)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.066-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Paul Howarth <paul@city-fan.org> - 2.066-5
- Runtime openssl dependency should be on openssl-libs
- Always require preferred IPv6 back-end: IO::Socket::IP ≥ 0.31
- Always require preferred IDN back-end: URI::_idna
- Modernize spec using %%{make_build} and %%{make_install}

* Wed Jun 26 2019 Paul Howarth <paul@city-fan.org> - 2.066-4
- PublicSuffix.pm is licensed MPLv2.0 (#1724169)

* Mon Jun 17 2019 Petr Pisar <ppisar@redhat.com> - 2.066-3
- Skip a PHA test if Net::SSLeay does not expose the PHA (bug #1632660)

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.066-2
- Perl 5.30 rebuild

* Wed Mar  6 2019 Paul Howarth <paul@city-fan.org> - 2.066-1
- Update to 2.066
  - Make sure that Net::SSLeay::CTX_get0_param is defined before using
    X509_V_FLAG_PARTIAL_CHAIN; Net::SSLeay 1.85 defined only the second with
    LibreSSL 2.7.4 but not the first (CPAN RT#128716)
  - Prefer AES for server side cipher default since it is usually
    hardware-accelerated
  - Fix test t/verify_partial_chain.t by using the newly exposed function
    can_partial_chain instead of guessing (wrongly) if the functionality is
    available

* Mon Mar  4 2019 Paul Howarth <paul@city-fan.org> - 2.064-1
- Update to 2.064
  - Make algorithm for fingerprint optional, i.e. detect based on length of
    fingerprint (CPAN RT#127773)
  - Fix t/sessions.t and improve stability of t/verify_hostname.t on Windows
  - Use CTX_set_ecdh_auto when needed (OpenSSL 1.0.2) if explicit curves are
    set
  - Update fingerprints for live tests

* Sat Mar  2 2019 Paul Howarth <paul@city-fan.org> - 2.063-1
- Update to 2.063
  - Support for both RSA and ECDSA certificate on same domain
  - Update PublicSuffix
  - Refuse to build if Net::SSLeay is compiled with one version of OpenSSL but
    then linked against another API-incompatible version (i.e. more than just
    the patchlevel differs)

* Mon Feb 25 2019 Paul Howarth <paul@city-fan.org> - 2.062-1
- Update to 2.062
  - Enable X509_V_FLAG_PARTIAL_CHAIN if supported by Net::SSLeay (1.83+) and
    OpenSSL (1.1.0+); this makes leaf certificates or intermediate certificates
    in the trust store be usable as full trust anchors too

* Sat Feb 23 2019 Paul Howarth <paul@city-fan.org> - 2.061-1
- Update to 2.061
  - Support for TLS 1.3 session reuse (needs Net::SSLeay ≥ 1.86); note that
    the previous (and undocumented) API for the session cache has been changed
  - Support for multiple curves, automatic setting of curves and setting of
    supported curves in client (needs Net::SSLeay ≥ 1.86)
  - Enable Post-Handshake-Authentication (TLSv1.3 feature) client-side when
    client certificates are provided (needs Net::SSLeay ≥ 1.86)

* Thu Feb 07 2019 Petr Pisar <ppisar@redhat.com> - 2.060-4
- Client sends a post-handshake-authentication extension if a client key and
  a certificate are available (bug #1632660)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.060-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 24 2018 Petr Pisar <ppisar@redhat.com> - 2.060-2
- Prevent tests from dying on SIGPIPE (CPAN RT#126899)

* Mon Sep 17 2018 Paul Howarth <paul@city-fan.org> - 2.060-1
- Update to 2.060
  - Support for TLS 1.3 with OpenSSL 1.1.1 (needs Net::SSLeay ≥ 1.86); see
    also CPAN RT#126899
  - TLS 1.3 support is not complete yet for session reuse

* Tue Aug 21 2018 Petr Pisar <ppisar@redhat.com> - 2.059-2
- Adapt to OpenSSL 1.1.1, it requires patched Net-SSLeay (bug #1616198)

* Thu Aug 16 2018 Paul Howarth <paul@city-fan.org> - 2.059-1
- Update to 2.059
  - Fix memory leak when CRLs are used (CPAN RT#125867)
  - Fix memory leak when using stop_SSL and threads
    (https://rt.cpan.org/Ticket/Display.html?id=125867#txn-1797132)

* Thu Jul 19 2018 Paul Howarth <paul@city-fan.org> - 2.058-1
- Update to 2.058
  - Fix memory leak that occurred with explicit stop_SSL in connection with
    non-blocking sockets or timeout (CPAN RT#125867)
  - Fix redefine warnings in case Socket6 is installed but neither
    IO::Socket::IP nor IO::Socket::INET6 (CPAN RT#124963)
  - IO::Socket::SSL::Intercept - optional 'serial' argument can be starting
    number or callback to create serial number based on the original certificate
  - New function get_session_reused to check if a session got reused
  - IO::Socket::SSL::Utils::CERT_asHash: fingerprint_xxx now set to the correct
    value
  - Fix t/session_ticket.t: It failed with OpenSSL 1.1.* since this version
    expects the extKeyUsage of clientAuth in the client cert also to be allowed
    by the CA if CA uses extKeyUsage

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.056-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.056-2
- Perl 5.28 rebuild

* Mon Feb 19 2018 Paul Howarth <paul@city-fan.org> - 2.056-1
- Update to 2.056
  - Intercept: Fix creation of serial number (basing it on binary digest
    instead of treating hex fingerprint as binary), allow use of own serial
    numbers again
  - t/io-socket-ip.t: Skip test if no IPv6 support on system (CPAN RT#124464)
  - Update PublicSuffix

* Thu Feb 15 2018 Paul Howarth <paul@city-fan.org> - 2.055-1
- Update to 2.055
  - Use SNI also if hostname was given all-uppercase
  - Utils::CERT_create: Don't add authority key for issuer since Chrome does
    not like this
  - Intercept:
    - Change behavior of code-based cache to better support synchronizing
      within multiprocess/threaded set-ups
    - Don't use counter for serial number but somehow base it on original
      certificate in order to avoid conflicts with reuse of serial numbers
      after restart
  - Better support platforms without IPv6 (CPAN RT#124431)
  - Spelling fixes in documentation (CPAN RT#124306)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.054-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Paul Howarth <paul@city-fan.org> - 2.054-1
- Update to 2.054
  - Small behavior fixes
    - If SSL_fingerprint is used and matches, don't check for OCSP
    - Utils::CERT_create: Small fixes to properly specific purpose, ability to
      use predefined complex purpose but disable some features
  - Update PublicSuffix
  - Updates for documentation, especially regarding pitfalls with forking or
    using non-blocking sockets, spelling fixes
  - Test fixes and improvements
    - Stability improvements for live tests
    - Regenerate certificates in certs/ and make sure they are limited to the
      correct purpose; check in program used to generate certificates
    - Adjust tests since certificates have changed and some tests used
      certificates intended for client authentication as server certificates,
      which now no longer works

* Mon Oct 23 2017 Paul Howarth <paul@city-fan.org> - 2.052-1
- Update to 2.052
  - Disable NPN support if LibreSSL ≥ 2.6.1 is detected since they've replaced
    the functions with dummies instead of removing NPN completly or setting
    OPENSSL_NO_NEXTPROTONEG
  - t/01loadmodule.t shows more output helpful in debugging problems
  - Update fingerprints for external tests
  - Update documentation to make behavior of syswrite more clear

* Tue Sep  5 2017 Paul Howarth <paul@city-fan.org> - 2.051-1
- Update to 2.051
  - syswrite: If SSL_write sets SSL_ERROR_SYSCALL but not $! (as seen with
    OpenSSL 1.1.0 on Windows), set $! to EPIPE to propagate a useful error up
    (GH#62)

* Fri Aug 18 2017 Paul Howarth <paul@city-fan.org> - 2.050-1
- Update to 2.050
  - Removed unnecessary settings of SSL_version and SSL_cipher_list from tests
  - protocol_version.t can now deal when TLS 1.0 and/or TLS 1.1 are not
    supported, as is the case with openssl versions in latest Debian (buster)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.049-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Paul Howarth <paul@city-fan.org> - 2.049-1
- Update to 2.049
  - Fixed problem caused by typo in the context of session cache (GH#60)
  - Updated PublicSuffix information from publicsuffix.org

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.048-2
- Perl 5.26 rebuild

* Mon Apr 17 2017 Paul Howarth <paul@city-fan.org> - 2.048-1
- Update to 2.048
  - Fixed small memory leaks during destruction of socket and context
    (CPAN RT#120643)
- Drop support for EOL distributions prior to F-13
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Fri Feb 17 2017 Paul Howarth <paul@city-fan.org> - 2.047-1
- Update to 2.047
  - Better fix for problem which 2.046 tried to fix but broke LWP that way
- Update patches as needed

* Thu Feb 16 2017 Paul Howarth <paul@city-fan.org> - 2.046-1
- Update to 2.046
  - Clean up everything in DESTROY and make sure to start with a fresh
    %%{*self} in configure_SSL because it can happen that a GLOB gets used
    again without calling DESTROY
    (https://github.com/noxxi/p5-io-socket-ssl/issues/56)
- Update patches as needed

* Tue Feb 14 2017 Paul Howarth <paul@city-fan.org> - 2.045-1
- Update to 2.045
  - Fixed memory leak caused by not destroying CREATED_IN_THIS_THREAD for SSL
    objects (GH#55)
  - Optimization: don't track SSL objects and CTX in *CREATED_IN_THIS_THREAD if
    perl is compiled without thread support
  - Small fix in t/protocol_version.t to use older versions of Net::SSLeay with
    openssl build without SSLv3 support
  - When setting SSL_keepSocketOnError to true the socket will not be closed on
    fatal error (GH#53, modified)
- Update patches as needed

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.044-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Paul Howarth <paul@city-fan.org> - 2.044-1
- Update to 2.044
  - Protect various 'eval'-based capability detections at startup with a
    localized __DIE__ handler; this way, dynamically requiring IO::Socket::SSL
    as done by various third party software should cause less problems even if
    there is a global __DIE__ handler that does not properly deal with 'eval'
- Update patches as needed

* Fri Jan  6 2017 Paul Howarth <paul@city-fan.org> - 2.043-1
- Update to 2.043
  - Enable session ticket callback with Net::SSLeay ≥ 1.80
  - Make t/session_ticket.t work with OpenSSL 1.1.0; with this version the
    session no longer gets reused if it was not properly closed, which is now
    done using an explicit close by the client
- Update patches as needed

* Wed Jan  4 2017 Paul Howarth <paul@city-fan.org> - 2.041-1
- Update to 2.041
  - Leave session ticket callback off for now until the needed patch is
    included in Net::SSLeay (see
    https://rt.cpan.org/Ticket/Display.html?id=116118#txn-1696146)
- Update patches as needed

* Sun Dec 18 2016 Paul Howarth <paul@city-fan.org> - 2.040-1
- Update to 2.040
  - Fix detection of default CA path for OpenSSL 1.1.x
  - Utils::CERT_asHash now includes the signature algorithm used
  - Utils::CERT_asHash can now deal with large serial numbers
- Update patches as needed

* Mon Nov 21 2016 Paul Howarth <paul@city-fan.org> - 2.039-1
- Update to 2.039
  - OpenSSL 1.1.0c changed the behavior of SSL_read so that it now returns -1
    on EOF without proper SSL shutdown; since it looks like that this behavior
    will be kept at least for 1.1.1+, adapt to the changed API by treating
    errno=NOERR on SSL_ERROR_SYSCALL as EOF
- Update patches as needed

* Mon Sep 19 2016 Paul Howarth <paul@city-fan.org> - 2.038-1
- Update to 2.038
  - Restrict session ticket callback to Net::SSLeay 1.79+ since version before
    contains bug; add test for session reuse
  - Extend SSL fingerprint to pubkey digest, i.e. 'sha1$pub$xxxxxx....'
  - Fix t/external/ocsp.t to use different server (under my control) to check
    OCSP stapling
- Update patches as needed

* Tue Aug 23 2016 Paul Howarth <paul@city-fan.org> - 2.037-1
- Update to 2.037
  - Disable OCSP support when Net::SSLeay 1.75..1.77 is used (CPAN RT#116795)
  - Fix session cache del_session: it freed the session but did not properly
    remove it from the cache; further reuse caused crash
- Update patches as needed

* Thu Aug 11 2016 Paul Howarth <paul@city-fan.org> - 2.035-1
- Update to 2.035
  - Fixes for issues introduced in 2.034
    - Return with error in configure_SSL if context creation failed; this
      might otherwise result in a segmentation fault later
    - Apply builtin defaults before any (user configurable) global settings
      (i.e. done with set_defaults, set_default_context...) so that builtins
      don't replace user settings
- Update patches as needed

* Mon Aug  8 2016 Paul Howarth <paul@city-fan.org> - 2.034-1
- Update to 2.034
  - Move handling of global SSL arguments into creation of context, so that
    these get also applied when creating a context only
- Update patches as needed

* Sat Jul 16 2016 Paul Howarth <paul@city-fan.org> - 2.033-1
- Update to 2.033
  - Support for session ticket reuse over multiple contexts and processes (if
    supported by Net::SSLeay)
  - Small optimizations, like saving various Net::SSLeay constants into
    variables and access variables instead of calling the constant sub all the
    time
  - Make t/dhe.t work with openssl 1.1.0
- Update patches as needed

* Tue Jul 12 2016 Paul Howarth <paul@city-fan.org> - 2.032-1
- Update to 2.032
  - Set session id context only on the server side; even if the documentation
    for SSL_CTX_set_session_id_context makes clear that this function is server
    side only, it actually affects handling of session reuse on the client side
    too and can result in error "SSL3_GET_SERVER_HELLO:attempt to reuse session
    in different context" at the client

* Fri Jul  8 2016 Paul Howarth <paul@city-fan.org> - 2.031-1
- Update to 2.031
  - Utils::CERT_create - don't add given extensions again if they were already
    added; Firefox croaks with sec_error_extension_value_invalid if (specific?)
    extensions are given twice
  - Assume that Net::SSLeay::P_PKCS12_load_file will return the CA certificates
    with the reverse order as in the PKCS12 file, because that's what it does
  - Support for creating ECC keys in Utils once supported by Net::SSLeay
  - Remove internal sub session_cache and access cache directly (faster)
- Update patches as needed

* Tue Jun 28 2016 Paul Howarth <paul@city-fan.org> - 2.029-1
- Update to 2.029
  - Add del_session method to session cache
  - Use SSL_session_key as the real key for the cache and not some derivate of
    it, so that it works to remove the entry using the same key
- BR: perl-generators

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.027-2
- Perl 5.24 rebuild

* Thu Apr 21 2016 Paul Howarth <paul@city-fan.org> - 2.027-1
- Update to 2.027
  - Updated Changes file for 2.026

* Wed Apr 20 2016 Paul Howarth <paul@city-fan.org> - 2.026-1
- Update to 2.026
  - Upstream's default cipher lists updated (we use system default though)
- Update patches as needed

* Mon Apr  4 2016 Paul Howarth <paul@city-fan.org> - 2.025-1
- Update to 2.025
  - Resolved memleak if SSL_crl_file was used (CPAN RT#113257, CPAN RT#113530)
- Simplify find command using -delete

* Sun Feb  7 2016 Paul Howarth <paul@city-fan.org> - 2.024-1
- Update to 2.024
  - Work around issue where the connect fails on systems having only a loopback
    interface and where IO::Socket::IP is used as super class (default when
    available)
- Update patches as needed

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.023-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Paul Howarth <paul@city-fan.org> - 2.023-1
- Update to 2.023
  - OpenSSL 1.0.2f changed the behavior of SSL shutdown in case the TLS
    connection was not fully established, which somehow resulted in
    Net::SSLeay::shutdown returning 0 (i.e. keep trying) and hence an endless
    loop; it will now ignore this result in case the TLS connection was not
    yet established and consider the TLS connection closed instead
- Update patches as needed

* Thu Dec 10 2015 Paul Howarth <paul@city-fan.org> - 2.022-1
- Update to 2.022
  - Fix stringification of IPv6 inside subjectAltNames in Utils::CERT_asHash
    (CPAN RT#110253)

* Thu Dec  3 2015 Paul Howarth <paul@city-fan.org> - 2.021-1
- Update to 2.021
  - Fixes for documentation and typos
  - Update PublicSuffix with latest version from publicsuffix.org
- Update patches as needed

* Mon Sep 21 2015 Paul Howarth <paul@city-fan.org> - 2.020-1
- Update to 2.020
  - Support multiple directories in SSL_ca_path (CPAN RT#106711); directories
    can be given as array or as string with a path separator
  - Typos fixed (https://github.com/noxxi/p5-io-socket-ssl/pull/34)
- Update patches as needed

* Tue Sep  1 2015 Paul Howarth <paul@city-fan.org> - 2.019-1
- Update to 2.019
  - Work around different behavior of getnameinfo from Socket and Socket6 by
    using a different wrapper depending on which module is used for IPv6
- Update patches as needed

* Mon Aug 31 2015 Paul Howarth <paul@city-fan.org> - 2.018-1
- Update to 2.018
  - Checks for readability of files/dirs for certificates and CA no longer use
    -r because this is not safe when ACLs are used (CPAN RT#106295)
  - New method sock_certificate similar to peer_certificate (CPAN RT#105733)
  - get_fingerprint can now take optional certificate as argument and compute
    the fingerprint of it; useful in connection with sock_certificate
  - Check for both EWOULDBLOCK and EAGAIN since these codes are different on
    some platforms (CPAN RT#106573)
  - Enforce default verification scheme if nothing was specified, i.e. no
    longer just warn but accept; if really no verification is wanted, a scheme
    of 'none' must be explicitly specified
  - Support different cipher suites per SNI hosts
  - startssl.t failed on darwin with old openssl since server requested client
    certificate but offered also anon ciphers (CPAN RT#106687)
- Update patches as needed

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.016-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.016-2
- Perl 5.22 rebuild

* Sun Jun  7 2015 Paul Howarth <paul@city-fan.org> - 2.016-1
- Update to 2.016
  - Add flag X509_V_FLAG_TRUSTED_FIRST by default if available in OpenSSL
    (since 1.02) and available with Net::SSLeay (CPAN RT#104759)
  - Work around hanging prompt() with older perl in Makefile.PL
    (CPAN RT#104731)
  - Make t/memleak_bad_handshake.t work on cygwin and other systems having
    /proc/pid/statm (CPAN RT#104659)
  - Add better debugging

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.015-2
- Perl 5.22 rebuild

* Thu May 14 2015 Paul Howarth <paul@city-fan.org> - 2.015-1
- Update to 2.015
  - Work around problem with IO::Socket::INET6 on Windows, by explicitly using
    Domain AF_INET in the tests (CPAN RT#104226)

* Tue May  5 2015 Paul Howarth <paul@city-fan.org> - 2.014-1
- Update to 2.014
  - Utils::CERT_create - work around problems with authorityInfoAccess, where
    OpenSSL i2v does not create the same string as v2i expects
  - Intercept - don't clone some specific extensions that only make sense with
    the original certificate

* Fri May  1 2015 Paul Howarth <paul@city-fan.org> - 2.013-1
- Update to 2.013
  - Assign severities to internal error handling and make sure that follow-up
    errors like "configuration failed" or "certificate verify error" don't
    replace more specific "hostname verification failed" when reporting in
    sub errstr/$SSL_ERROR (CPAN RT#103423)
  - Enhanced documentation (https://github.com/noxxi/p5-io-socket-ssl/pull/26)

* Mon Feb  2 2015 Paul Howarth <paul@city-fan.org> - 2.012-1
- Update to 2.012
  - Fix t/ocsp.t in case no HTTP::Tiny is installed

* Sun Feb  1 2015 Paul Howarth <paul@city-fan.org> - 2.011-1
- Update to 2.011
  - Fix t/ocsp.t - don't count on revoked.grc.com using OCSP stapling
    (CPAN RT#101855)
  - Added option 'purpose' to Utils::CERT_create to get better control of the
    certificate's purpose; default is 'server,client' for non-CA (contrary to
    only 'server' before)
  - Removed RC4 from default cipher suites on the server side
    (https://github.com/noxxi/p5-io-socket-ssl/issues/22)
  - Refactoring of some tests using Test::More
- Note that this package still uses system-default cipher and SSL versions,
  which may have RC4 enabled
- Update patches as needed

* Thu Jan 15 2015 Paul Howarth <paul@city-fan.org> - 2.010-1
- Update to 2.010
  - New options SSL_client_ca_file and SSL_client_ca to let the server send the
    list of acceptable CAs for the client certificate
  - t/protocol_version.t - fix in case SSLv3 is not supported in Net::SSLeay
    (CPAN RT#101485)

* Mon Jan 12 2015 Paul Howarth <paul@city-fan.org> - 2.009-1
- Update to 2.009
  - Remove util/analyze.pl; this tool is now together with other SSL tools at
    https://github.com/noxxi/p5-ssl-tools
  - Added ALPN support (needs OpenSSL1.02, Net::SSLeay 1.56+) (CPAN RT#101452)

* Thu Dec 18 2014 Paul Howarth <paul@city-fan.org> - 2.008-1
- Update to 2.008
  - Work around recent OCSP verification errors for revoked.grc.com (badly
    signed OCSP response, Firefox also complains about it) in test
    t/external/ocsp.t
  - util/analyze.pl - report more details about preferred cipher for specific
    TLS versions

* Thu Nov 27 2014 Paul Howarth <paul@city-fan.org> - 2.007-1
- Update to 2.007
  - Make getline/readline fall back to super class if class is not sslified
    yet, i.e. behave the same as sysread, syswrite etc. (CPAN RT#100529)

* Sun Nov 23 2014 Paul Howarth <paul@city-fan.org> - 2.006-1
- Update to 2.006
  - Make SSLv3 available even if the SSL library disables it by default in
    SSL_CTX_new (like done in LibreSSL); default will stay to disable SSLv3
    so this will be only done when setting SSL_version explicitly
  - Fix possible segmentation fault when trying to use an invalid certificate
  - Use only the ICANN part of the default public suffix list and not the
    private domains; this makes existing exceptions for s3.amazonaws.com and
    googleapis.com obsolete
  - Fix t/protocol_version.t to deal with OpenSSL installations that are
    compiled without SSLv3 support
  - Make (hopefully) non-blocking work on windows by using EWOULDBLOCK instead
    of EAGAIN; while this is the same on UNIX it is different on Windows and
    socket operations return there (WSA)EWOULDBLOCK and not EAGAIN
  - Enable non-blocking tests on Windows too
  - Make PublicSuffix::_default_data thread safe
  - Update PublicSuffix with latest list from publicsuffix.org
- Note that this package still uses system-default cipher and SSL versions,
  which may have SSL3.0 enabled
- Classify buildreqs by usage

* Wed Oct 22 2014 Paul Howarth <paul@city-fan.org> - 2.002-1
- Update to 2.002
  - Fix check for (invalid) IPv4 when validating hostname against certificate;
    do not use inet_aton any longer because it can cause DNS lookups for
    malformed IP (CPAN RT#99448)
  - Update PublicSuffix with latest version from publicsuffix.org - lots of new
    top level domains
  - Add exception to PublicSuffix for s3.amazonaws.com (CPAN RT#99702)

* Tue Oct 21 2014 Paul Howarth <paul@city-fan.org> - 2.001-1
- Update to 2.001
  - Add SSL_OP_SINGLE_(DH|ECDH)_USE to default options to increase PFS security
  - Update external tests with currently expected fingerprints of hosts
  - Some fixes to make it still work on 5.8.1

* Thu Oct 16 2014 Paul Howarth <paul@city-fan.org> - 2.000-1
- Update to 2.000
  - Consider SSL3.0 as broken because of POODLE and disable it by default
  - Skip live tests without asking if environment NO_NETWORK_TESTING is set
  - Skip tests that require fork on non-default windows setups without proper
    fork (https://github.com/noxxi/p5-io-socket-ssl/pull/18)
- Note that this package still uses system-default cipher and SSL versions,
  which may have SSL3.0 enabled

* Fri Oct 10 2014 Paul Howarth <paul@city-fan.org> - 1.999-1
- Update to 1.999
  - Make sure we don't use version 0.30 of IO::Socket::IP
  - Make sure that PeerHost is checked in all places where PeerAddr is checked,
    because these are synonyms and IO::Socket::IP prefers PeerHost while others
    prefer PeerAddr; also accept PeerService additionally to PeerPort
    (https://github.com/noxxi/p5-io-socket-ssl/issues/16)
  - Add ability to use client certificates and to overwrite hostname with
    util/analyze-ssl.pl

* Mon Sep 22 2014 Paul Howarth <paul@city-fan.org> - 1.998-1
- Update to 1.998
  - Make client authentication work at the server side when SNI is in by use
    having CA path and other settings in all SSL contexts instead of only the
    main one (https://github.com/noxxi/p5-io-socket-ssl/pull/15)

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.997-4
- Perl 5.20 rebuild

* Thu Aug  7 2014 Paul Howarth <paul@city-fan.org> - 1.997-3
- Use system-default SSL version too

* Thu Aug  7 2014 Paul Howarth <paul@city-fan.org> - 1.997-2
- Use system-wide default cipher list to support use of system-wide
  crypto policy (#1076390, #1127577, CPAN RT#97816)
  https://fedoraproject.org/wiki/Changes/CryptoPolicy

* Mon Jul 14 2014 Paul Howarth <paul@city-fan.org> - 1.997-1
- Update to 1.997
  - Fix initialization and creation of OpenSSL-internals for perlcc
    compatibility (CPAN RT#95452)
  - Add refresh option for peer_certificate, so that it checks if the
    certificate changed in the mean time (on renegotiation)
  - Fix fingerprint checking - now applies only to top-most certificate
  - IO::Socket::SSL::Utils - accept extensions within CERT_create
  - Various documentation fixes

* Mon Jun 23 2014 Paul Howarth <paul@city-fan.org> - 1.994-1
- Update to 1.994
  - IO::Socket::SSL can now be used as dual-use socket, e.g. start plain,
    upgrade to SSL and downgrade again all with the same object; see
    documentation of SSL_startHandshake and chapter Advanced Usage
  - Try to apply SSL_ca* even if verify_mode is 0, but don't complain if this
    fails; this is needed if one wants to explicitly verify OCSP lookups even
    if verification is otherwise off, because otherwise the signature check
    would fail (this is mostly useful for testing)
  - Reorder documentation of attributes for new, so that the more important
    ones are at the top

* Sun Jun 15 2014 Paul Howarth <paul@city-fan.org> - 1.993-1
- Update to 1.993
  - Major rewrite of documentation, now in separate file
  - Rework error handling to distinguish between SSL errors and internal errors
    (like missing capabilities)
  - Fix handling of default_ca if given during the run of the program
    (Debian #750646)
  - util/analyze-ssl.pl - fix hostname check if SNI does not work

* Tue Jun 10 2014 Paul Howarth <paul@city-fan.org> - 1.992-1
- Update to 1.992
  - Set $! to undef before doing IO (accept, read...); on Windows a connection
    reset could cause an SSL read error without setting $!, so make sure we
    don't keep the old value and maybe thus run into an endless loop

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.991-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Paul Howarth <paul@city-fan.org> - 1.991-1
- Update to 1.991
  - New option SSL_OCSP_TRY_STAPLE to enforce staple request even if
    VERIFY_NONE
  - Work around for CPAN RT#96013 in peer_certificates

* Tue May 27 2014 Paul Howarth <paul@city-fan.org> - 1.990-1
- Update to 1.990
  - Added option SSL_ocsp_staple_callback to get the stapled OCSP response and
    verify it somewhere else
  - Try to fix warnings on Windows again (CPAN RT#95967)
  - Work around temporary OCSP error in t/external/ocsp.t

* Sun May 25 2014 Paul Howarth <paul@city-fan.org> - 1.989-1
- Update to 1.989
  - Fix warnings on Windows (CPAN RT#95881)

* Sat May 17 2014 Paul Howarth <paul@city-fan.org> - 1.988-1
- Update to 1.988
  - Allow IPv4 in common name, because browsers allow this too; only for scheme
    www/http though, not for rfc2818 (because RC2818 does not allow this; in
    default scheme IPv6 and IPv4 are allowed in CN)
  - Fix handling of public suffix; add exemption for *.googleapis.com
    wildcard, which should not be allowed according to public suffix list but
    actually is used
  - Add hostname verification test based on older test of chromium, but change
    some of the test expectations because we don't want to support IP as SAN
    DNS and because we enforce a public suffix list (and thus *.co.uk should
    not be allowed)
  - Fix t/verify_hostname_standalone.t on systems without usable IDNA or IPv6
    (CPAN RT#95719)
  - Enable IPv6 support only if we have a usable inet_pton
  - Remove stale entries from MANIFEST
  - Add transparent support for DER and PKCS#12 files to specify cert and key,
    e.g. it will autodetect the format
  - If SSL_cert_file is PEM and no SSL_key_file is given it will check if the
    key is in SSL_cert_file too

* Thu May 15 2014 Paul Howarth <paul@city-fan.org> - 1.985-1
- Update to 1.985
  - Make OCSP callback return 1 even if it was called on the server side
    because of bad setup of the socket; otherwise we get an endless calling of
    the OCSP callback
  - Consider an OCSP response that is not yet or no longer valid a soft error
    instead of a hard error
  - Fix skip in t/external/ocsp.t in case fingerprint does not match
  - Call EVP_PKEY_free not EVP_KEY_free in IO::Socket::SSL::Utils::KEY_free
    (CPAN RT#95633)
  - util/analyze.pl - with --show-chain check if chain with SNI is different
    from chain w/o SNI
- Drop ExtUtils::MakeMaker version requirement

* Wed May 14 2014 Paul Howarth <paul@city-fan.org> - 1.984-2
- Fix typo in Utils.pm (#1097640, CPAN RT#95633)

* Sat May 10 2014 Paul Howarth <paul@city-fan.org> - 1.984-1
- Update to 1.984
  - Added OCSP support:
    - Needs Net::SSLeay ≥ 1.59
    - For usage see documentation of IO::Socket::SSL (examples and anything
      with OCSP in the name)
  - New tool util/analyze-ssl.pl, which is intended to help in debugging of SSL
    problems and to get information about capabilities of server; it works also
    as an example of how to use various features (like OCSP, SNI...)
  - Fix peer_certificates (returns leaf certificate only once on client side)
  - Added timeout for stop_SSL (either with Timeout or with the default timeout
    for IO::Socket)
  - Fix IO::Socket::SSL::Utils mapping between ASN1_TIME and time_t when local
    time is not GMT; use Net::SSLeay::ASN1_TIME_timet if available
  - Fix t/external/usable_ca.t for system with junk in CA files

* Sun May  4 2014 Paul Howarth <paul@city-fan.org> - 1.983-1
- Update to 1.983
  - Fix public suffix handling: ajax.googleapis.com should be ok even if
    googleapis.com is in public suffix list (e.g. check one level less)
    (CPAN RT#95317)
  - usable_ca.t - update fingerprints after heartbleed attack
  - usable_ca.t - make sure we have usable CA for tested hosts in CA store

* Thu Apr 24 2014 Paul Howarth <paul@city-fan.org> - 1.982-1
- Update to 1.982
  - Fix for using subroutine as argument to set_args_filter_hack

* Tue Apr  8 2014 Paul Howarth <paul@city-fan.org> - 1.981-1
- Update to 1.981
  - Fix ecdhe test for openssl 1.0.1d (CPAN RT#95432)
  - Fix detection of openssl 1.0.1d (detected 1.0.1e instead)
  - New function can_ecdh in IO::Socket::SSL

* Tue Apr  8 2014 Paul Howarth <paul@city-fan.org> - 1.980-1
- Update to 1.980
  - Disable elliptic curve support for openssl 1.0.1d on 64-bit
    (http://rt.openssl.org/Ticket/Display.html?id=2975)
  - Fix certificate fingerprint calculation
- Add patch to skip elliptic curve test for openssl 1.0.1d on 64-bit
- Add patch to fix openssl version test

* Sun Apr  6 2014 Paul Howarth <paul@city-fan.org> - 1.979-1
- Update to 1.979
  - Hostname checking:
    - Configuration of 'leftmost' is renamed to 'full_label', but the old
      version is kept for compatibility reasons
    - Documentation of predefined schemes fixed to match reality

* Fri Apr  4 2014 Paul Howarth <paul@city-fan.org> - 1.978-1
- Update to 1.978
  - Added public prefix checking to verification of wildcard certificates, e.g.
    accept *.foo.com but not *.co.uk; see documentation of
    SSL_verifycn_publicsuffix and IO::Socket::SSL::PublicSuffix
  - Fix publicsuffix for IDNA, more tests with various IDNA libs
    (CPAN RT#94424)
  - Reuse result of IDN lib detection from PublicSuffix.pm in SSL.pm
  - Add more checks to external/usable_ca.t; now it is enough that at least one
    of the hosts verifies against the built-in CA store
  - Add openssl and Net::SSLeay version to diagnostics in load test
- Switch preferred IDN back-end from Net::LibIDN to URI::_idna as per upstream,
  falling back to Net::IDN::Encode on older distributions
- Add fix from upstream git to support building with Test::More < 0.88

* Wed Apr  2 2014 Paul Howarth <paul@city-fan.org> - 1.975-1
- Update to 1.975
  - BEHAVIOR CHANGE: work around TEA misfeature on OS X built-in openssl, e.g.
    guarantee that only the explicitly-given CA or the openssl default CA will
    be used; this means that certificates inside the OS X keyring will no
    longer be used, because there is no way to control the use by openssl
    (e.g. certificate pinning etc.)
  - Make external tests run by default to make sure default CA works on all
    platforms; it skips automatically on network problems like timeouts or SSL
    interception, and can also use http(s)_proxy environment variables

* Wed Apr  2 2014 Paul Howarth <paul@city-fan.org> - 1.974-1
- Update to 1.974
  - New function peer_certificates to get the whole certificate chain; needs
    Net::SSLeay ≥ 1.58
  - Extended IO::Socket::Utils::CERT_asHash to provide way more information,
    like issuer information, cert and pubkey digests, all extensions, CRL
    distribution points and OCSP uri

* Wed Mar 26 2014 Paul Howarth <paul@city-fan.org> - 1.973-1
- Update to 1.973
  - With SSL_ca, certificate handles can now be used in addition to
    SSL_ca_file and SSL_ca_path
  - No longer complain if SSL_ca_file and SSL_ca_path are both given;
    instead, add both as options to the CA store
  - Shortcut 'issuer' to give both issuer_cert and issuer_key in CERT_create

* Sun Mar 23 2014 Paul Howarth <paul@city-fan.org> - 1.972-1
- Update to 1.972
  - Make sure t/external/usable_ca.t works also with older openssl without
    support for SNI (CPAN RT#94117)

* Sat Mar 22 2014 Paul Howarth <paul@city-fan.org> - 1.971-1
- Update to 1.971
  - Try to use SSL_hostname for hostname verification if no SSL_verifycn_name
    is given; this way, hostname for SNI and verification can be specified in
    one step
  - New test program example/simulate_proxy.pl

* Wed Mar 19 2014 Paul Howarth <paul@city-fan.org> - 1.970-1
- Update to 1.970
  - Make sure sub default_ca uses a local $_ and not a version of an outer
    scope that might be read-only (CPAN RT#93987)

* Sun Mar 16 2014 Paul Howarth <paul@city-fan.org> - 1.969-1
- Update to 1.969
  - Fix set_defaults to match documentation regarding short names
  - New function set_args_filter_hack to make it possible to override bad SSL
    settings from other code at the last moment
  - Determine default_ca on module load (and not on first use in each thread)
  - Don't try default hostname verification if verify_mode 0
  - Fix hostname verification when reusing context

* Thu Mar 13 2014 Paul Howarth <paul@city-fan.org> - 1.968-1
- Update to 1.968
  - BEHAVIOR CHANGE: removed implicit defaults of certs/server-{cert,key}.pem
    for SSL_{cert,key}_file and ca/,certs/my-ca.pem for SSL_ca_file; these
    defaults were deprecated since 1.951 (July 2013)
  - Usable CA verification path on Windows etc.:
    - Do not use Net::SSLeay::CTX_set_default_verify_paths any longer to set
      system/build dependent default verification path, because there was no
      way to retrieve these default values and check if they contained usable
      CA
    - Instead, re-implement the same algorithm and export the results with
      public function default_ca() and make it possible to overwrite it
    - Also check for usable verification path during build; if no usable path
      is detected, require Mozilla::CA at build and try to use it at runtime

* Fri Feb  7 2014 Paul Howarth <paul@city-fan.org> - 1.967-1
- Update to 1.967
  - Verify the hostname inside a certificate by default with a superset of
    common verification schemes instead of not verifying identity at all; for
    now it will only complain if name verification failed but in the future it
    will fail certificate verification, forcing you to set the expected
    SSL_verifycn_name if you want to accept the certificate
  - New option SSL_fingerprint and new methods get_fingerprint and
    get_fingerprint_bin; together they can be used to selectively accept
    specific certificates that would otherwise fail verification, like
    self-signed, outdated or from unknown CAs
  - Utils:
    - Default RSA key length 2048
    - Digest algorithm to sign certificate in CERT_create can be given;
      defaults to SHA-256
    - CERT_create can now issue non-CA self-signed certificate
    - CERT_create add some more useful constraints to certificate
  - Spelling fixes

* Wed Jan 22 2014 Paul Howarth <paul@city-fan.org> - 1.966-1
- Update to 1.966
  - Fixed bug introduced in 1.964 - disabling TLSv1_2 no longer worked by
    specifying !TLSv12; only !TLSv1_2 worked
  - Fixed leak of session objects in SessionCache, if another session
    replaced an existing session (introduced in 1.965)

* Fri Jan 17 2014 Paul Howarth <paul@city-fan.org> - 1.965-1
- Update to 1.965
  - New key SSL_session_key to influence how sessions are inserted and looked
    up in the client's session cache, which makes it possible to share sessions
    over different ip:host (as is required with some FTPS servers)
  - t/core.t - handle case where default loopback source is not 127.0.0.1, like
    in FreeBSD jails

* Wed Jan 15 2014 Paul Howarth <paul@city-fan.org> - 1.964-1
- Update to 1.964
  - Disabling TLSv1_1 did not work, because the constant was wrong; now it gets
    the constants from calling Net::SSLeay::SSL_OP_NO_TLSv1_1 etc.
  - The new syntax for the protocols is TLSv1_1 instead of TLSv11, which matches
    the syntax from OpenSSL (the old syntax continues to work in SSL_version)
  - New functions get_sslversion and get_sslversion_int, which get the SSL
    version of the established session as string or int
  - Disable t/io-socket-inet6.t if Acme::Override::INET is installed

* Tue Jan 14 2014 Paul Howarth <paul@city-fan.org> - 1.963-1
- Update to 1.963
  - Fix behavior of stop_SSL: for blocking sockets it now enough to call it
    once, for non-blocking it should be called again as long as EAGAIN and
    SSL_ERROR is set to SSL_WANT_(READ|WRITE)
  - Don't call blocking if start_SSL failed and downgraded socket has no
    blocking method
  - Documentation enhancements:
    - Special section for differences to IO::Socket
    - Describe problem with blocking accept on non-blocking socket
    - Describe arguments to new_from_fd and make clear that for upgrading an
      existing IO::Socket, start_SSL should be used directly

* Thu Nov 28 2013 Paul Howarth <paul@city-fan.org> - 1.962-1
- Update to 1.962
  - Work around problems with older F5 BIG-IP by offering fewer ciphers on the
    client side by default, so that the client hello stays below 255 bytes

* Tue Nov 26 2013 Paul Howarth <paul@city-fan.org> - 1.961-1
- Update to 1.961
  - IO::Socket::SSL::Utils::CERT_create can now create CA-certificates that
    are not self-signed (by giving issuer_*)

* Wed Nov 13 2013 Paul Howarth <paul@city-fan.org> - 1.960-1
- Update to 1.960
  - Only documentation enhancements:
    - Clarify with text and example code, that within event loops not only
      select/poll should be used, but also pending has to be called
    - Better introduction into SSL; at least mention anonymous authentication as
      something you don't want and should take care with the right cipher
    - Make it more clear that it's better not to change the cipher list unless
      you really know what you're doing
- Adopt upstream's versioning scheme

* Tue Nov 12 2013 Paul Howarth <paul@city-fan.org> - 1.95.9-1
- Update to 1.959
  - Fix test t/core.t for Windows

* Mon Nov 11 2013 Paul Howarth <paul@city-fan.org> - 1.95.8-1
- Update to 1.958
  Lots of behavior changes for more secure defaults:
  - BEHAVIOR CHANGE: make default cipher list more secure, especially:
    - No longer support MD5 by default (broken)
    - No longer support anonymous authentication by default (vulnerable to
      man in the middle attacks)
    - Prefer ECDHE/DHE ciphers and add necessary ECDH curve and DH keys, so
      that it uses by default forward secrecy, if underlying
      Net::SSLeay/openssl supports it
    - Move RC4 to the end, i.e. 3DES is preferred (BEAST attack should
      hopefully have been fixed and now RC4 is considered less safe than 3DES)
    - Default SSL_honor_cipher_order to 1, e.g. when used as server it tries
      to get the best cipher even if the client prefers other ciphers; PLEASE
      NOTE that this might break connections with older, less secure
      implementations, in which case revert to 'ALL:!LOW:!EXP:!aNULL' or so
  - BEHAVIOR CHANGE: SSL_cipher_list now gets set on context, not SSL object,
    and thus gets reused if context gets reused; PLEASE NOTE that using
    SSL_cipher_list together with SSL_reuse_ctx no longer has any effect on
    the ciphers of the context
  - Rework hostname verification schemes:
    - Add RFC names as scheme (e.g. 'rfc2818', ...)
    - Add SIP, SNMP, syslog, netconf, GIST
    - BEHAVIOR CHANGE: fix SMTP - now accept wildcards in CN and subjectAltName
    - BEHAVIOR CHANGE: fix IMAP, POP3, ACAP, NNTP - now accept wildcards in CN
  - BEHAVIOR CHANGE: anywhere wildcards like www* now match only 'www1',
    'www2' etc.  but not 'www'
  - Anywhere wildcards like x* are no longer applied to IDNA names (which start
    with 'xn--')
  - Fix crash of Utils::CERT_free
  - Support TLSv11, TLSv12 as handshake protocols
  - Fixed t/core.t: test used cipher_list of HIGH, which includes anonymous
    authorization; with the DH param given by default since 1.956, old versions
    of openssl (like 0.9.8k) used cipher ADH-AES256-SHA (e.g. anonymous
    authorization) instead of AES256-SHA and thus the check for the peer
    certificate failed (because ADH does not exchange certificates) - fixed by
    explicitly specifying HIGH:!aNULL as cipher (CPAN RT#90221)
  - Cleaned up tests:
    - Remove ssl_settings.req and 02settings.t, because all tests now create a
      simple socket at 127.0.0.1 and thus global settings are no longer needed
    - Some tests did not have use strict(!); fixed it
    - Removed special handling for older Net::SSLeay versions that are less
      than our minimum requirement
    - Some syntax enhancements: removed some SSL_version and SSL_cipher_list
      options where they were not really needed
  - Cleanup: remove workaround for old IO::Socket::INET6 but instead require at
    least version 2.55 which is now 5 years old
  - Fix t/session.t to work with older openssl versions (CPAN RT#90240)

* Fri Oct 11 2013 Paul Howarth <paul@city-fan.org> - 1.95.5-1
- Update to 1.955
  - Support for perfect forward secrecy using ECDH, if the Net::SSLeay version
    supports it

* Sun Sep 15 2013 Paul Howarth <paul@city-fan.org> - 1.95.4-1
- Update to 1.954
  - Accept older versions of ExtUtils::MakeMaker and add meta information like
    link to repository only for newer versions

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.95.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.95.3-2
- Perl 5.18 rebuild

* Mon Jul 22 2013 Paul Howarth <paul@city-fan.org> - 1.95.3-1
- Update to 1.953
  - Precedence fixes for IO::Socket::SSL::Utils (CPAN RT#87052)

* Fri Jul 12 2013 Paul Howarth <paul@city-fan.org> - 1.95.2-1
- Update to 1.952
  - Fix t/acceptSSL-timeout.t on Win32 (CPAN RT#86862)

* Wed Jul  3 2013 Paul Howarth <paul@city-fan.org> - 1.95.1-1
- Update to 1.951
  (1.950)
  - MAJOR BEHAVIOR CHANGE:
    - ssl_verify_mode now defaults to verify_peer for client
    - Previously it used verify_none, but loudly complained since 1.79 about it
    - It will not complain any longer, but the connection will probably fail
    - Please don't simply disable ssl verification; instead, set SSL_ca_file
      etc. so that verification succeeds!
  - MAJOR BEHAVIOR CHANGE:
    - It will now complain if the built-in defaults of certs/my-ca.pem or ca/
      for CA and certs/{server,client}-{key,cert}.pem for cert and key are
      used, i.e. no certificates are specified explicitly
    - In the future these insecure (relative path!) defaults will be removed
      and the CA replaced with the system defaults
  (1.951)
  - Use Net::SSLeay::SSL_CTX_set_default_verify_paths to use openssl's built-in
    defaults for CA unless CA path/file was given (or IO::Socket::SSL built-ins
    used)

* Sat Jun  1 2013 Paul Howarth <paul@city-fan.org> - 1.94-1
- Update to 1.94
  - Makefile.PL reported wrong version of openssl if Net::SSLeay was not
    installed, instead of reporting a missing dependency of Net::SSLeay

* Fri May 31 2013 Paul Howarth <paul@city-fan.org> - 1.93-1
- Update to 1.93
  - Need at least OpenSSL version 0.9.8 now, since last 0.9.7 was released 6
    years ago; remove code to work around older releases
  - Changed AUTHOR in Makefile.PL from array back to string, because the array
    feature is not available in MakeMaker shipped with 5.8.9 (CPAN RT#85739)
- Set openssl version requirement to 0.9.8
- Drop ExtUtils::MakeMaker version requirement back to 6.46

* Thu May 30 2013 Paul Howarth <paul@city-fan.org> - 1.92-1
- Update to 1.92
  - Intercept: use sha1-fingerprint of original cert for id into cache unless
    otherwise given
  - Fix pod error in IO::Socket::SSL::Utils (CPAN RT#85733)

* Thu May 30 2013 Paul Howarth <paul@city-fan.org> - 1.91-1
- Update to 1.91
  - Added IO::Socket::SSL::Utils for easier manipulation of certificates and
    keys
  - Moved SSL interception into IO::Socket::SSL::Intercept and simplified it
    using IO::Socket::SSL::Utils
  - Enhance meta information in Makefile.PL
- Bump openssl version requirement to 0.9.8a
- Need at least version 6.58 of ExtUtils::MakeMaker (CPAN RT#85739)

* Wed May 29 2013 Paul Howarth <paul@city-fan.org> - 1.90-1
- Update to 1.90
  - Support more digests, especially SHA-2 (CPAN RT#85290)
  - Added support for easy SSL interception (man in the middle) based on ideas
    found in mojo-mitm proxy
  - Make 1.46 the minimal required version for Net::SSLeay, because it
    introduced lots of useful functions
- BR:/R: openssl ≥ 0.9.7e for P_ASN1_TIME_(get,set)_isotime in Net::SSLeay

* Tue May 14 2013 Paul Howarth <paul@city-fan.org> - 1.89-1
- Update to 1.89
  - If IO::Socket::IP is used it should be at least version 0.20; otherwise we
    get problems with HTTP::Daemon::SSL and maybe others (CPAN RT#81932)
  - Spelling corrections

* Thu May  2 2013 Paul Howarth <paul@city-fan.org> - 1.88-1
- Update to 1.88
  - Consider a value of '' the same as undef for SSL_ca_(path|file), SSL_key*
    and SSL_cert* - some apps like Net::LDAP use it that way

* Wed Apr 24 2013 Paul Howarth <paul@city-fan.org> - 1.87-1
- Update to 1.87
  - Complain if given SSL_(key|cert|ca)_(file|path) do not exist or if they are
    not readable (CPAN RT#84829)
  - Fix use of SSL_key|SSL_file objects instead of files, broken with 1.83

* Wed Apr 17 2013 Paul Howarth <paul@city-fan.org> - 1.86-1
- Update to 1.86
  - Don't warn about SSL_verify_mode when re-using an existing SSL context
    (CPAN RT#84686)

* Mon Apr 15 2013 Paul Howarth <paul@city-fan.org> - 1.85-1
- Update to 1.85
  - Probe for available modules with local __DIE__ and __WARN__handlers
    (CPAN RT#84574)
  - Fix warning, when IO::Socket::IP is installed and inet6 support gets
    explicitly requested (CPAN RT#84619)

* Sat Feb 16 2013 Paul Howarth <paul@city-fan.org> - 1.84-1
- Update to 1.84
  - Disabled client side SNI for openssl version < 1.0.0 because of
    CPAN RT#83289
  - Added functions can_client_sni, can_server_sni and can_npn to check
    availability of SNI and NPN features
  - Added more documentation for SNI and NPN

* Thu Feb 14 2013 Paul Howarth <paul@city-fan.org> - 1.83-2
- Update to 1.831
  - Separated documentation of non-blocking I/O from error handling
  - Changed and documented behavior of readline to return the read data on
    EAGAIN/EWOULDBLOCK in case of non-blocking socket
    (see https://github.com/noxxi/p5-io-socket-ssl/issues/1)
- Bumped release rather than version number to preserve likely upgrade path
  and avoid need for epoch or version number ugliness; may revisit this in
  light of upstream's future version numbering decisions

* Mon Feb  4 2013 Paul Howarth <paul@city-fan.org> - 1.83-1
- Update to 1.83
  - Server Name Indication (SNI) support on the server side (CPAN RT#82761)
  - Reworked part of the documentation, like providing better examples

* Mon Jan 28 2013 Paul Howarth <paul@city-fan.org> - 1.82-1
- Update to 1.82
  - sub error sets $SSL_ERROR etc. only if there really is an error; otherwise
    it will keep the latest error, which allows IO::Socket::SSL->new to report
    the correct problem, even if the problem is deeper in the code (like in
    connect)
  - Correct spelling (CPAN RT#82790)

* Thu Dec  6 2012 Paul Howarth <paul@city-fan.org> - 1.81-1
- Update to 1.81
  - Deprecated set_ctx_defaults; new name is set_defaults (the old name is
    still available)
  - Changed handling of default path for SSL_(ca|cert|key)* keys: if one of
    these keys is user defined, don't add defaults for the others, i.e.
    don't mix user settings and defaults
  - Cleaner handling of module defaults vs. global settings vs. socket
    specific settings; global and socket specific settings are both provided
    by the user, while module defaults are not
  - Make IO::Socket::INET6 and IO::Socket::IP specific tests both run, even
    if both modules are installed, by faking a failed load of the other module
- BR: perl(IO::Socket::INET6) and perl(Socket6) unconditionally

* Fri Nov 30 2012 Paul Howarth <paul@city-fan.org> - 1.80-1
- Update to 1.80
  - Removed some warnings in test (missing SSL_verify_mode => 0), which caused
    tests to hang on Windows (CPAN RT#81493)

* Sun Nov 25 2012 Paul Howarth <paul@city-fan.org> - 1.79-1
- Update to 1.79
  - Use getnameinfo instead of unpack_sockaddr_in6 to get PeerAddr and PeerPort
    from sockaddr in _update_peer, because this provides scope too
  - Work around systems that don't define AF_INET6 (CPAN RT#81216)
  - Prepare transition to a more secure default for SSL_verify_mode; the use of
    the current default SSL_VERIFY_NONE will cause a big warning for clients,
    unless SSL_verify_mode was explicitly set inside the application to this
    insecure value (in the near future the default will be SSL_VERIFY_PEER, and
    thus causing verification failures in unchanged applications)

* Thu Nov 15 2012 Petr Šabata <contyk@redhat.com> - 1.77-2
- Added some missing build dependencies

* Fri Oct  5 2012 Paul Howarth <paul@city-fan.org> - 1.77-1
- Update to 1.77
  - support _update_peer for IPv6 too (CPAN RT#79916)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.76-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.76-2
- Perl 5.16 rebuild

* Mon Jun 18 2012 Paul Howarth <paul@city-fan.org> - 1.76-1
- Update to 1.76
  - add support for IO::Socket::IP, which supports inet6 and inet4
    (CPAN RT#75218)
  - fix documentation errors (CPAN RT#77690)
  - made it possible to explicitly disable TLSv11 and TLSv12 in SSL_version
  - use inet_pton from either Socket.pm 1.95 or Socket6.pm
- Use IO::Socket::IP for IPv6 support where available, else IO::Socket::INET6
- Add runtime dependency for appropriate IPv6 support module so that we can
  ensure that we run at runtime what we tested with at build time

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.74-2
- Perl 5.16 rebuild

* Mon May 14 2012 Paul Howarth <paul@city-fan.org> - 1.74-1
- Update to 1.74
  - accept a version of SSLv2/3 as SSLv23, because older documentation could
    be interpreted like this

* Fri May 11 2012 Paul Howarth <paul@city-fan.org> - 1.73-1
- Update to 1.73
  - set DEFAULT_CIPHER_LIST to ALL:!LOW instead of HIGH:!LOW
  - make test t/dhe.t hopefully work with more versions of openssl

* Wed May  9 2012 Paul Howarth <paul@city-fan.org> - 1.71-1
- Update to 1.71
  - 1.70 done right: don't disable SSLv2 ciphers; SSLv2 support is better
    disabled by the default SSL_version of 'SSLv23:!SSLv2'

* Tue May  8 2012 Paul Howarth <paul@city-fan.org> - 1.70-1
- Update to 1.70
  - make it possible to disable protocols using SSL_version, and make
    SSL_version default to 'SSLv23:!SSLv2'

* Tue May  8 2012 Paul Howarth <paul@city-fan.org> - 1.69-1
- Update to 1.69 (changes for CPAN RT#76929)
  - if no explicit cipher list is given, default to ALL:!LOW instead of the
    openssl default, which usually includes weak ciphers like DES
  - new config key SSL_honor_cipher_order and document how to use it to fight
    BEAST attack
  - fix behavior for empty cipher list (use default)
  - re-added workaround in t/dhe.t

* Mon Apr 16 2012 Paul Howarth <paul@city-fan.org> - 1.66-1
- Update to 1.66
  - make it thread safer (CPAN RT#76538)

* Mon Apr 16 2012 Paul Howarth <paul@city-fan.org> - 1.65-1
- Update to 1.65
  - added NPN (Next Protocol Negotiation) support (CPAN RT#76223)

* Sat Apr  7 2012 Paul Howarth <paul@city-fan.org> - 1.64-1
- Update to 1.64
  - ignore die from within eval to make tests more stable on Win32
    (CPAN RT#76147)
  - clarify some behavior regarding hostname verification
- Drop patch for t/dhe.t, no longer needed

* Wed Mar 28 2012 Paul Howarth <paul@city-fan.org> - 1.62-1
- Update to 1.62
  - small fix to last version

* Tue Mar 27 2012 Paul Howarth <paul@city-fan.org> - 1.61-1
- Update to 1.61
  - call CTX_set_session_id_context so that server's session caching works with
    client certificates too (CPAN RT#76053)

* Tue Mar 20 2012 Paul Howarth <paul@city-fan.org> - 1.60-1
- Update to 1.60
  - don't make blocking readline if socket was set nonblocking, but return as
    soon no more data are available (CPAN RT#75910)
  - fix BUG section about threading so that it shows package as thread safe
    as long as Net::SSLeay ≥ 1.43 is used (CPAN RT#75749)
- BR: perl(constant), perl(Exporter) and perl(IO::Socket)

* Thu Mar  8 2012 Paul Howarth <paul@city-fan.org> - 1.59-1
- Update to 1.59
  - if SSLv2 is not supported by Net::SSLeay set SSL_ERROR with useful message
    when attempting to use it
  - modify constant declarations so that 5.6.1 should work again
- Drop %%defattr, redundant since rpm 4.4

* Mon Feb 27 2012 Paul Howarth <paul@city-fan.org> - 1.58-1
- Update to 1.58
  - fix t/dhe.t for openssl 1.0.1 beta by forcing TLSv1, so that it does not
    complain about the too small RSA key, which it should not use anyway; this
    workaround is not applied for older openssl versions, where it would cause
    failures (CPAN RT#75165)
- Add patch to fiddle the openssl version number in the t/dhe.t workaround
  because the OPENSSL_VERSION_NUMBER cannot be trusted in Fedora
- One buildreq per line for readability
- Drop redundant buildreq perl(Test::Simple)
- Always run full test suite

* Wed Feb 22 2012 Paul Howarth <paul@city-fan.org> - 1.56-1
- Update to 1.56
  - add automatic or explicit (via SSL_hostname) SNI support, needed for
    multiple SSL hostnames with the same IP (currently only supported for the
    client)
- Use DESTDIR rather than PERL_INSTALL_ROOT
- No need to delete empty directories from buildroot

* Mon Feb 20 2012 Paul Howarth <paul@city-fan.org> - 1.55-1
- Update to 1.55
  - work around IO::Socket's work around for systems returning EISCONN etc. on
    connect retry for non-blocking sockets by clearing $! if SUPER::connect
    returned true (CPAN RT#75101)

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 1.54-1
- Update to 1.54
  - return 0 instead of undef in SSL_verify_callback to fix uninitialized
    warnings (CPAN RT#73629)

* Mon Dec 12 2011 Paul Howarth <paul@city-fan.org> - 1.53-1
- Update to 1.53
  - kill child in t/memleak_bad_handshake.t if test fails (CPAN RT#73146)

* Wed Dec  7 2011 Paul Howarth <paul@city-fan.org> - 1.52-1
- Update to 1.52
  - fix for t/nonblock.t hangs on AIX (CPAN RT#72305)
  - disable t/memleak_bad_handshake.t on AIX, because it might hang
    (CPAN RT#72170)
  - fix syntax error in t/memleak_bad_handshake.t

* Fri Oct 28 2011 Paul Howarth <paul@city-fan.org> - 1.49-1
- Update to 1.49
  - another regression for readline fix: this time it failed to return lines
    at EOF that don't end with newline - extended t/readline.t to catch this
    case and the fix for 1.48

* Wed Oct 26 2011 Paul Howarth <paul@city-fan.org> - 1.48-1
- Update to 1.48
  - further fix for readline fix in 1.45: if the pending data were false (like
    '0'), it failed to read the rest of the line (CPAN RT#71953)

* Fri Oct 21 2011 Paul Howarth <paul@city-fan.org> - 1.47-1
- Update to 1.47
  - fix for 1.46 - check for mswin32 needs to be /i

* Tue Oct 18 2011 Paul Howarth <paul@city-fan.org> - 1.46-1
- Update to 1.46
  - skip signals test on Windows

* Thu Oct 13 2011 Paul Howarth <paul@city-fan.org> - 1.45-1
- Update to 1.45
  - fix readline to continue when getting interrupt waiting for more data
- BR: perl(Carp)

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.44-2
- Perl mass rebuild

* Fri May 27 2011 Paul Howarth <paul@city-fan.org> - 1.44-1
- Update to 1.44
  - fix invalid call to inet_pton in verify_hostname_of_cert when identity
    should be verified as ipv6 address because it contains a colon

* Wed May 11 2011 Paul Howarth <paul@city-fan.org> - 1.43-1
- Update to 1.43
  - add SSL_create_ctx_callback to have a way to adjust context on creation
    (CPAN RT#67799)
  - describe problem of fake memory leak because of big session cache and how
    to fix it (CPAN RT#68073)
  - fix t/nonblock.t
  - stability improvements for t/inet6.t

* Tue May 10 2011 Paul Howarth <paul@city-fan.org> - 1.41-1
- Update to 1.41
  - fix issue in stop_SSL where it did not issue a shutdown of the SSL
    connection if it first received the shutdown from the other side
  - try to make t/nonblock.t more reliable, at least report the real cause of
    SSL connection errors
- No longer need to re-code docs to UTF-8

* Mon May  2 2011 Paul Howarth <paul@city-fan.org> - 1.40-1
- Update to 1.40
  - fix in example/async_https_server
  - get IDN support from URI (CPAN RT#67676)
- Nobody else likes macros for commands

* Thu Mar  3 2011 Paul Howarth <paul@city-fan.org> - 1.39-1
- Update to 1.39
  - fixed documentation of http verification: wildcards in cn is allowed

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Paul Howarth <paul@city-fan.org> - 1.38-1
- Update to 1.38
  - fixed wildcards_in_cn setting for http, wrongly set in 1.34 to 1 instead of
    anywhere (CPAN RT#64864)

* Fri Dec 10 2010 Paul Howarth <paul@city-fan.org> - 1.37-1
- Update to 1.37
  - don't complain about invalid certificate locations if user explicitly set
    SSL_ca_path and SSL_ca_file to undef: assume that user knows what they are
    doing and will work around the problems themselves (CPAN RT#63741)

* Thu Dec  9 2010 Paul Howarth <paul@city-fan.org> - 1.36-1
- Update to 1.36
  - update documentation for SSL_verify_callback based on CPAN RT#63743 and
    CPAN RT#63740

* Mon Dec  6 2010 Paul Howarth <paul@city-fan.org> - 1.35-1
- Update to 1.35 (addresses CVE-2010-4334)
  - if verify_mode is not VERIFY_NONE and the ca_file/ca_path cannot be
    verified as valid, it will no longer fall back to VERIFY_NONE but throw an
    error (http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=606058)

* Tue Nov  2 2010 Paul Howarth <paul@city-fan.org> - 1.34-1
- Update to 1.34
  - schema http for certificate verification changed to wildcards_in_cn=1
  - if upgrading socket from inet to ssl fails due to handshake problems, the
    socket gets downgraded back again but is still open (CPAN RT#61466)
  - deprecate kill_socket: just use close()

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.33-2
- Mass rebuild with perl-5.12.0

* Wed Mar 17 2010 Paul Howarth <paul@city-fan.org> - 1.33-1
- Update to 1.33
  - attempt to make t/memleak_bad_handshake.t more stable
  - fix hostname checking: only check an IP against subjectAltName GEN_IPADD

* Tue Feb 23 2010 Paul Howarth <paul@city-fan.org> - 1.32-1
- Update to 1.32 (die in Makefile.PL if Scalar::Util has no dualvar support)
- Use %%{_fixperms} macro instead of our own %%{__chmod} incantation

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.31-2
- Rebuild against perl 5.10.1

* Sun Sep 27 2009 Paul Howarth <paul@city-fan.org> - 1.31-1
- Update to 1.31 (see Changes for details)

* Thu Aug 20 2009 Paul Howarth <paul@city-fan.org> - 1.30-1
- Update to 1.30 (fix memleak when SSL handshake failed)
- Add buildreq procps needed for memleak test

* Mon Jul 27 2009 Paul Howarth <paul@city-fan.org> - 1.27-1
- Update to 1.27
  - various regex fixes for i18n and service names
  - fix warnings from perl -w (CPAN RT#48131)
  - improve handling of errors from Net::ssl_write_all

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul  4 2009 Paul Howarth <paul@city-fan.org> - 1.26-1
- Update to 1.26 (verify_hostname_of_cert matched only the prefix for the
  hostname when no wildcard was given, e.g. www.example.org matched against a
  certificate with name www.exam in it [#509819])

* Fri Jul  3 2009 Paul Howarth <paul@city-fan.org> - 1.25-1
- Update to 1.25 (fix t/nonblock.t for OS X 10.5 - CPAN RT#47240)

* Thu Apr  2 2009 Paul Howarth <paul@city-fan.org> - 1.24-1
- Update to 1.24 (add verify hostname scheme ftp, same as http)

* Wed Feb 25 2009 Paul Howarth <paul@city-fan.org> - 1.23-1
- Update to 1.23 (complain when no certificates are provided)

* Sat Jan 24 2009 Paul Howarth <paul@city-fan.org> - 1.22-1
- Update to latest upstream version: 1.22

* Thu Jan 22 2009 Paul Howarth <paul@city-fan.org> - 1.20-1
- Update to latest upstream version: 1.20

* Tue Nov 18 2008 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to latest upstream version: 1.18
- BR: perl(IO::Socket::INET6) for extra test coverage

* Mon Oct 13 2008 Paul Howarth <paul@city-fan.org> - 1.17-1
- Update to latest upstream version: 1.17

* Mon Sep 22 2008 Paul Howarth <paul@city-fan.org> - 1.16-1
- Update to latest upstream version: 1.16

* Sat Aug 30 2008 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to latest upstream version: 1.15
- Add buildreq and req for perl(Net::LibIDN) to avoid croaking when trying to
  verify an international name against a certificate

* Wed Jul 16 2008 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to latest upstream version: 1.14
- BuildRequire perl(Net::SSLeay) >= 1.21

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-4
- Rebuild for perl 5.10 (again)

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-3
- Rebuild for new perl

* Wed Nov 28 2007 Paul Howarth <paul@city-fan.org> - 1.12-2
- Cosmetic spec changes suiting new maintainer's preferences

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 1.12-1
- Update to latest upstream version: 1.12
- Fix license tag
- Add BuildRequires for ExtUtils::MakeMaker and Test::Simple
- Fix package review issues:
- Source URL
- Resolves: bz#226264

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.02-1.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 1.02-1
- Upgrade to latest CPAN version: 1.02

* Mon Sep 18 2006 Warren Togami <wtogami@redhat.com> - 1.01-1
- 1.01 bug fixes (#206782)

* Sun Aug 13 2006 Warren Togami <wtogami@redhat.com> - 0.998-1
- 0.998 with more important fixes

* Tue Aug 01 2006 Warren Togami <wtogami@redhat.com> - 0.994-1
- 0.994 important bugfixes (#200860)

* Tue Jul 18 2006 Warren Togami <wtogami@redhat.com> - 0.991-1
- 0.991

* Wed Jul 12 2006 Warren Togami <wtogami@redhat.com> - 0.97-3
- Import into FC6

* Tue Feb 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.97-2
- Rebuild for FC5 (perl 5.8.8).
- Rebuild switch: "--with sessiontests".

* Mon Jul 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.97-1
- 0.97.
- Convert docs to UTF-8, drop some unuseful ones.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.96-4
- Rebuilt

* Tue Oct 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-3
- Disable session test suite even if Net::SSLeay >= 1.26 is available.

* Wed Jul  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-0.fdr.2
- Bring up to date with current fedora.us Perl spec template.
- Include examples in docs.

* Sat May  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-0.fdr.1
- Update to 0.96.
- Reduce directory ownership bloat.
- Require perl(:MODULE_COMPAT_*).

* Fri Oct 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.95-0.fdr.1
- First build.
