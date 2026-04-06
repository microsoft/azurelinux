# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if ! (0%{?rhel})
%{bcond_without perl_Net_SSLeay_enables_optional_test}
%else
%{bcond_with perl_Net_SSLeay_enables_optional_test}
%endif

# OpenSSL ENGINE support deprecated in Fedora 41 onwards
# https://fedoraproject.org/wiki/Changes/OpensslDeprecateEngine
%if 0%{?fedora} > 40 || 0%{?rhel} > 9
%global _preprocessor_defines %{?_preprocessor_defines} -DOPENSSL_NO_ENGINE
%endif

Name:		perl-Net-SSLeay
Version:	1.94
Release:	11%{?dist}
Summary:	Perl extension for using OpenSSL
License:	Artistic-2.0
URL:		https://metacpan.org/release/Net-SSLeay
Source0:	https://cpan.metacpan.org/modules/by-module/Net/Net-SSLeay-%{version}.tar.gz
Patch0:		https://patch-diff.githubusercontent.com/raw/radiator-software/p5-net-ssleay/pull/514.patch
Patch10:	Net-SSLeay-1.90-pkgconfig.patch
# =========== Module Build ===========================
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	openssl
BuildRequires:	openssl-devel
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(constant)
BuildRequires:	perl(English)
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	perl(ExtUtils::PkgConfig)
BuildRequires:	perl(ExtUtils::MM)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(Symbol)
BuildRequires:	perl(Text::Wrap)
BuildRequires:	perl(utf8)
# =========== Module Runtime =========================
BuildRequires:	perl(AutoLoader)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Errno)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(MIME::Base64)
BuildRequires:	perl(Socket)
BuildRequires:	perl(vars)
BuildRequires:	perl(XSLoader)
# =========== Test Suite =============================
BuildRequires:	perl(base)
BuildRequires:	perl(Config)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(FindBin)
BuildRequires:	perl(HTTP::Tiny)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IO::Socket::INET)
BuildRequires:	perl(lib)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(SelectSaver)
BuildRequires:	perl(Storable)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::More) >= 0.61
BuildRequires:	perl(threads)
BuildRequires:	perl(warnings)
# =========== Optional Tests =========================
%if %{with perl_Net_SSLeay_enables_optional_test}
BuildRequires:	perl(Crypt::OpenSSL::Bignum)
# Test::Kwalitee 1.00 not used
BuildRequires:	perl(Test::Pod) >= 1.41
# Test::Pod::Coverage 1.00 not used
%endif
# =========== Module Dependencies ====================
Requires:	perl(MIME::Base64)
Requires:	perl(XSLoader)

# Don't "provide" private Perl libs or the redundant unversioned perl(Net::SSLeay) provide
%global __provides_exclude ^(perl\\(Net::SSLeay\\)$|SSLeay\\.so)

%description
This module offers some high level convenience functions for accessing
web pages on SSL servers (for symmetry, same API is offered for
accessing http servers, too), a sslcat() function for writing your own
clients, and finally access to the SSL API of SSLeay/OpenSSL package
so you can write servers or clients for more complicated applications.

%prep
%setup -q -n Net-SSLeay-%{version}

# Fix for test suite compatibility with OpenSSL 3.4
%patch -P 0 -p 1

# Get libraries to link against from pkg-config
# https://github.com/radiator-software/p5-net-ssleay/pull/127
%patch -P 10

# Fix permissions in examples to avoid bogus doc-file dependencies
chmod -c 644 examples/*

%build
unset OPENSSL_PREFIX
PERL_MM_USE_DEFAULT=1 perl Makefile.PL \
	INSTALLDIRS=vendor \
	NO_PACKLIST=1 \
	NO_PERLLOCAL=1 \
	OPTIMIZE="%{optflags}" < /dev/null
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

# Remove script we don't want packaged
rm -f %{buildroot}%{perl_vendorarch}/Net/ptrtstrun.pl

%check
unset RELEASE_TESTING
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING.md Credits QuickRef README examples/
%{perl_vendorarch}/auto/Net/
%dir %{perl_vendorarch}/Net/
%{perl_vendorarch}/Net/SSLeay/
%{perl_vendorarch}/Net/SSLeay.pm
%doc %{perl_vendorarch}/Net/SSLeay.pod
%{_mandir}/man3/Net::SSLeay.3*
%{_mandir}/man3/Net::SSLeay::Handle.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.94-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.94-10
- Perl 5.42 rebuild

* Wed Mar 26 2025 Paul Howarth <paul@city-fan.org> - 1.94-9
- Fix for test suite compatibility with OpenSSL 3.4
  (https://github.com/radiator-software/p5-net-ssleay/pull/514)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.94-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jul 23 2024 Paul Howarth <paul@city-fan.org> - 1.94-7
- Build without OpenSSL ENGINE support on Fedora 41 onwards

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.94-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul  9 2024 Paul Howarth <paul@city-fan.org> - 1.94-5
- BR: openssl-devel-engine on Fedora 41 onwards, at least for now, as the
  build fails in the absence of <openssl/engine.h> (rhbz#2295331)
  (https://fedoraproject.org/wiki/Changes/OpensslDeprecateEngine)

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.94-4
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.94-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.94-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan  8 2024 Paul Howarth <paul@city-fan.org> - 1.94-1
- Update to 1.94
  - Net::SSLeay now officially supports all stable releases of OpenSSL 3.1 and
    3.2, and LibreSSL 3.5-3.8
  - Many noisy compiler warnings have been silenced - if SSLeay.xs fails to
    compile, it should now be much easier to identify the cause
  - libcrypto's OPENSSL_init_crypto() function and libssl's OPENSSL_init_ssl()
    function are now exposed, enabling fine-grained control over the
    initialisation and configuration of both libraries
  - libssl functions implementing TLS 1.3 PSK authentication are now exposed,
    in particular SSL_CTX_set_psk_find_session_callback() (on the server side)
    and SSL_CTX_set_psk_use_session_callback() (on the client side)
  - libssl functions implementing server-side TLS 1.2 PSK authentication are
    now exposed, in particular SSL_CTX_set_psk_server_callback()
  - libssl's SSL_CTX_set_client_hello_cb() function is now exposed, allowing a
    TLS server to set a callback function that is executed when the server
    processes a ClientHello message
  - Many more libcrypto/libssl constants and functions are now exposed; see the
    release notes for the 1.93 developer releases for a full list

* Thu Aug  3 2023 Paul Howarth <paul@city-fan.org> - 1.92-10
- Rebuild for OpenSSL 3.1.1 in Rawhide

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.92-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.92-8
- Perl 5.38 rebuild

* Thu Apr  6 2023 Paul Howarth <paul@city-fan.org> - 1.92-7
- Update test suite to handle potential unavailability of sha1 algorithm
  https://github.com/radiator-software/p5-net-ssleay/pull/433
- Avoid deprecated patch syntax

* Fri Mar 17 2023 Michal Josef Špaček <mspacek@redhat.com> - 1.92-6
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.92-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.92-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.92-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Paul Howarth <paul@city-fan.org> - 1.92-1
- Update to 1.92
  - Net::SSLeay now supports stable releases of OpenSSL 3.0
    - OpenSSL 3.0.0 introduces the concept of "providers", which contain
      cryptographic algorithm implementations; many outdated, deprecated
      and/or insecure algorithms have been moved to the "legacy" provider,
      which may need to be loaded explicitly in order to use them with
      Net::SSLeay (see "Low level API: OSSL_LIB_CTX and OSSL_PROVIDER
      related functions" in the Net::SSLeay module documentation for details)
    - Net::SSLeay's built-in PEM_get_string_PrivateKey() function depends on
      algorithms that have moved to the legacy provider described above; if
      OpenSSL has been compiled without the legacy provider, the tests
      t/local/33_x509_create_cert.t and t/local/63_ec_key_generate_key.t will
      fail when the test suite is run
    - TLS 1.1 and below may only be used at security level 0 as of OpenSSL
      3.0.0; if a minimum required security level is imposed (e.g. in an
      OpenSSL configuration file managed by the operating system), the tests
      t/local/44_sess.t and t/local/45_exporter.t will fail when the test
      suite is run
  - Net::SSLeay now supports stable releases of LibreSSL from the 3.2-3.4
    series (with the exception of 3.2.2 and 3.2.3 - see "COMPATIBILITY" in
    the Net::SSLeay module documentation for details)
    - The TLS 1.3 implementation in LibreSSL 3.1-3.3, parts of which are
      enabled by default, is not fully compatible with the libssl API and may
      not function as expected with Net::SSLeay; see "KNOWN BUGS AND CAVEATS"
      in the Net::SSLeay module documentation for details
  - A number of new libcrypto/libssl constants and functions are now exposed,
    including SSL_CTX_set_keylog_callback() and SSL_CTX_set_msg_callback(),
    which are helpful when debugging TLS handshakes; see the release notes
    for the 1.91 developer releases (in the Changes file) for a full list of
    newly-exposed constants and functions

* Tue Oct  5 2021 Paul Howarth <paul@city-fan.org> - 1.90-7
- Fixes for OpenSSL 3.0.0 are now entirely from upstream

* Wed Sep 15 2021 Paul Howarth <paul@city-fan.org> - 1.90-6
- Add fixes (mainly from upstream) for OpenSSL 3.0.0

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.90-5
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.90-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.90-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Paul Howarth <paul@city-fan.org> - 1.90-1
- Update to 1.90
  - Formalised libssl version support policy: all stable versions of OpenSSL
    in the 0.9.8-1.1.1 branches (with the exception of 0.9.8-0.9.8b) and all
    stable releases of LibreSSL in the 2.0-3.1 series are supported
  - The LibreSSL 3.2 series is not yet fully supported because its TLSv1.3
    implementation is not currently libssl-compatible
  - Added support for LibreSSL on Windows when built with Visual C++
  - Exposed P_X509_CRL_add_extensions, several SSL_CIPHER functions, and
    several stack functions
  - Fixed crashes in the callback functions CTX_set_next_proto_select_cb and
    CTX_set_alpn_select_cb
  - The test suite is now compatible with OpenSSL 1.1.1e onwards, as well as
    OpenSSL security level 2 (the default on many Linux distributions)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.88-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.88-8
- Perl 5.32 rebuild

* Sat Mar 21 2020 Paul Howarth <paul@city-fan.org> - 1.88-7
- Add SSL_shutdown() calls in Net::SSLeay::sslcat() and t/local/07_sslecho.t
  to fix compatibility with OpenSSL 1.1.1e (GH#160, GH#161)

* Tue Mar 10 2020 Paul Howarth <paul@city-fan.org> - 1.88-6
- BR: perl(FindBin) for test suite

* Wed Feb 05 2020 Tom Stellard <tstellar@redhat.com> - 1.88-5
- Spec file cleanups: Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMaker

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.88-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.88-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.88-2
- Perl 5.30 rebuild

* Sat May 11 2019 Paul Howarth <paul@city-fan.org> - 1.88-1
- Update to 1.88
  Summary of major changes since version 1.85
  - Mike McCauley has stepped down as maintainer: the new maintainers are Chris
    Novakovic, Heikki Vatiainen and Tuure Vartiainen
  - The source code has moved from the now-defunct Debian Subversion server
    (alioth.debian.org) to GitHub
    (https://github.com/radiator-software/p5-net-ssleay)
  - Net-SSLeay is provided under the terms of the Artistic License 2.0; this
    has been the case since version 1.66, but references to other licenses
    remained in the source code, causing ambiguity
  - Perl 5.8.1 or newer is now required to use Net-SSLeay; this has already
    been the case for some time in practice, as the test suite hasn't fully
    passed on Perl 5.6 for several years
  - Much-improved compatibility with OpenSSL 1.1.1, and improved support for
    TLS 1.3
  - Fixed a long-standing bug in cb_data_advanced_put() that caused memory
    leaks when callbacks were frequently added and removed
  - Support in the test suite for "hardened" OpenSSL configurations that set a
    default security level of 2 or higher (e.g., in the OpenSSL packages that
    ship with recent versions of Debian, Fedora and Ubuntu)

* Thu Apr 18 2019 Petr Pisar <ppisar@redhat.com> - 1.86-0.3.09
- Replace expired test certificates (CPAN RT#129201)

* Fri Mar 29 2019 Paul Howarth <paul@city-fan.org> - 1.86-0.2.09
- Get libraries to link against from pkg-config
  https://github.com/radiator-software/p5-net-ssleay/pull/127

* Wed Mar 20 2019 Petr Pisar <ppisar@redhat.com> - 1.86-0.1.09
- Update to 1.86_09 (see Changes file for details)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.85-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Sep 29 2018 Paul Howarth <paul@city-fan.org> - 1.85-9
- OpenSSL 1.1.1 in Fedora disables SSL3 API, so stop trying to test it

* Wed Sep 19 2018 Paul Howarth <paul@city-fan.org> - 1.85-8
- Expose SSL_CTX_set_post_handshake_auth (#1630391)
  https://github.com/radiator-software/p5-net-ssleay/pull/68

* Fri Aug 17 2018 Petr Pisar <ppisar@redhat.com> - 1.85-7
- Revert retry in Net::SSLeay::write_partial() (bug #1614884)

* Wed Aug 15 2018 Petr Pisar <ppisar@redhat.com> - 1.85-6
- Revert retry in Net::SSLeay::{read,write}() (bug #1614884)

* Tue Aug 14 2018 Petr Pisar <ppisar@redhat.com> - 1.85-5
- Avoid SIGPIPE in t/local/36_verify.t (bug #1614884)

* Mon Aug 13 2018 Petr Pisar <ppisar@redhat.com> - 1.85-4
- Adapt to OpenSSL 1.1.1 (bug #1614884)
- Adapt tests to system-wide crypto policy (bug #1614884)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.85-2
- Perl 5.28 rebuild

* Wed Mar 14 2018 Paul Howarth <paul@city-fan.org> - 1.85-1
- Update to 1.85
  - Preparations for transferring maintenace to a new maintainer
  - Fixed test failure in t/local/33_x509_create_cert.t for some versions of
    OpenSSL
  - Fixed free() error that causes "Free to wrong pool ..." message on Windows

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.84-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Paul Howarth <paul@city-fan.org> - 1.84-1
- Update to 1.84
  - Fixed an error in t/local/04_basic.t causing a test failure if
    Test::Exception not installed

* Tue Jan 16 2018 Paul Howarth <paul@city-fan.org> - 1.83-1
- Update to 1.83
  - Fixed a problem with exporting OPENSSL_NO_NEXTPROTONEG even though they
    are not available on LibreSSL
  - Add support for SSL_set_default_passwd_cb* for OpenSSL 1.1.0f and later;
    LibreSSL does not support these functions, at least yet
  - Add new functions related to SSL_CTX_new
  - Add two new functions introduced in OpenSSL 1.1.0, a number of constants
    and a couple of const qualifiers to SSLeay.xs; tests and documentation .pod
    were also updated
  - Added support for SSL_use_certificate_chain_file function introduced in
    OpenSSL 1.1.0
  - Fixed LibreSSL version detection to correctly parse LibreSSL minor version
  - Fix memory leaks in OCSP handling
  - Add new functions for certificate verification introduced in OpenSSL 1.02,
    a number of constants, new test data files, new tests and updates to .pod
    documentation; the new functions provide access to the built-in wildcard
    check functionality available in OpenSSL 1.0.2 and later
  - Added X509_STORE_CTX_new and X509_verify_cert
  - SSL_OCSP_response_verify now clears the error queue if OCSP_basic_verify
    fails but the intermediate certificate succeeds

* Tue Oct 31 2017 Paul Howarth <paul@city-fan.org> - 1.82-1
- Update to 1.82
  - Added support for building under Linuxbrew (a linuxbrew version of MacOS
    Homebrew)
  - Implement SSL_CTX_set_psk_client_callback() and
    SSL_set_psk_client_callback()
  - Skip the NPN test if the SSL library is LibreSSL
  - Fixed a problem with a variable declaration in
    ssleay_session_secret_cb_invoke
  - Bugfix: tlsext_status_cb_invoke(...): free ocsp_response only when
    allocated; the same callback is used on a server side for OCSP stapling
    and in that case ocsp_response is NULL and not used
  - New feature: Added a binding
    SSL_set_session_ticket_ext_cb(ssl, callback, data); a callback used by
    EAP-FAST/EAP-TEAT to parse and process TLS session ticket
  - New feature: Added a binding SSL_set_session_ticket_ext(ssl, ticket); used
    by EAP-FAST/EAP-TEAP to define TLS session ticket value
  - Bugfix: tlsext_ticket_key_cb_invoke(...): allow SHA256 HMAC key to be 32
    bytes instead of 16 bytes (which OpenSSL will pad with zeros up to 32
    bytes)
  - New feature: Added following bindings:
    - X509_get_ex_data(cert, idx)
    - X509_get_ex_new_index(argl, argp, new_func, dup_func, free_func)
    - X509_get_app_data(cert)
    - X509_set_ex_data(cert, idx, data)
    - X509_set_app_data(cert, arg)
    - X509_STORE_CTX_get_ex_new_index(argl, argp, new_func, dup_func, free_func)
    - X509_STORE_CTX_get_app_data(x509_store_ctx)
    - X509_STORE_CTX_set_app_data(x509_store_ctx, arg)
  - New feature: Added an implementation for
    SSL_get_finished(ssl, buf, count=2*EVP_MAX_MD_SIZE)
  - New feature: Added an implementation for
    SSL_get_peer_finished(ssl, buf, count=2*EVP_MAX_MD_SIZE)
  - Bugfix: SSL_get_keyblock_size(s): Calculate key block size correctly also
    with AEAD ciphers, which don’t use digest functions
  - New feature: Added a binding SSL_set_tlsext_status_ocsp_resp(ssl, staple);
    used by a server side to include OCSP staple in ServerHello
  - Bugfix: SSL_OCSP_response_verify(ssl, rsp, svreq, flags): check that chain
    and last are not NULL before trying to use them
  - Bugfix: inc/Module/Install/PRIVATE/Net/SSLeay.pm: Don’t quote include and
    lib paths
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.81-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.81-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.81-2
- Perl 5.26 rebuild

* Tue Mar 28 2017 Paul Howarth <paul@city-fan.org> - 1.81-1
- Update to 1.81
  - Enable RSA_get_key_parameters with LibreSSL - again
  - Fixed memory leak in X509_get_subjectAltNames
  - Added . to lib path in Makefile.PL to accommodate people who are using a
    perl with -Ddefault_inc_excludes_dot
  - Fixed build failure if engine support not present
  - Improvements to get_my_thread_id to work around possibility of ERRSV not
    being defined, e.g. on OpenWRT

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan  5 2017 Paul Howarth <paul@city-fan.org> - 1.80-1
- Update to 1.80
  - Fix unexpected changes in the control flow of the Perl program that seemed
    to be triggered by the ticket key callback

* Tue Jan  3 2017 Paul Howarth <paul@city-fan.org> - 1.79-1
- Update to 1.79
  - Patch to fix a few inline variable declarations that cause errors for older
    compilers
  - Patch: Generated C code is not compatible with MSVC, AIX cc, probably
    others; added some PREINIT blocks and replaced 2 cases of INIT with PREINIT
  - Fix compile failure if the OpenSSL library it's built against has
    compression support compiled out
  - Added RSA_get_key_parameters() to return a list of pointers to RSA key
    internals (only available prior to OpenSSL 1.1)
  - Fix some documentation typos
  - Testing with openssl-1.1.0b

* Wed Oct 12 2016 Paul Howarth <paul@city-fan.org> - 1.78-2
- Rebuild for OpenSSL 1.1.0 in Fedora 26

* Sun Aug 14 2016 Paul Howarth <paul@city-fan.org> - 1.78-1
- Update to 1.78
  - Fixed broken (since 1.75) OCSP code and tests

* Thu Aug 11 2016 Paul Howarth <paul@city-fan.org> - 1.77-2
- Fix OCSP (CPAN RT#116795)

* Mon Aug  1 2016 Paul Howarth <paul@city-fan.org> - 1.77-1
- Update to 1.77
  - Fixed incorrect size to memset in tlsext_ticket_key_cb_invoke

* Sun Jul 31 2016 Paul Howarth <paul@city-fan.org> - 1.76-1
- Update to 1.76
  - Compatibility with OpenSSL 1.1, tested with openssl-1.1.0-pre5:
    - Conditionally remove threading locking code, not needed in 1.1
    - Rewrite code that accesses inside X509_ATTRIBUTE struct
    - SSL_CTX_need_tmp_RSA, SSL_CTX_set_tmp_rsa, SSL_CTX_set_tmp_rsa_callback,
      SSL_set_tmp_rsa_callback support not available in 1.1
    - SSL_session_reused is now native
    - SSL_get_keyblock_size modifed to use new API
    - OCSP functions modified to use new API under 1.1
    - SSL_set_state removed with 1.1
    - SSL_get_state and SSL_state are now equivalent and available in all
      versions
    - SSL_CTX_v2_new removed
    - SESSION_set_master_key removed with 1.1; code that previously used
      SESSION_set_master_key must now set $secret in the session_secret
      callback set with SSL_set_session_secret_cb
    - With 1.1, $secret in the session_secret callback set with
      SSL_set_session_secret_cb can be changed to alter the master key
      (required by EAP-FAST)
  - Added a function EC_KEY_generate_key similar to RSA_generate_key and a
    function EVP_PKEY_assign_EC_KEY similar to EVP_PKEY_assign_RSA; using
    these functions it is easy to create and use EC keys in the same way as RSA
    keys
  - Testing with LibreSSL 2.4.1
  - Provide support for cross context (and cross process) session sharing using
    the stateless TLS session tickets
  - Added documentation about downloading latest version from SVN
  - Added missing Module/install files to SVN

* Thu Jul 21 2016 Paul Howarth <paul@city-fan.org> - 1.74-3
- Fix FTBFS when perl isn't in the SRPM build root

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.74-2
- Perl 5.24 rebuild

* Tue Apr 12 2016 Paul Howarth <paul@city-fan.org> - 1.74-1
- Update to 1.74
  - README.OSX was missing from the distribution

* Mon Apr 11 2016 Paul Howarth <paul@city-fan.org> - 1.73-1
- Update to 1.73
  - Added X509_get_X509_PUBKEY
  - Added README.OSX with instructions on how to build for recent OS X
  - Added info about using OPENSSL_PREFIX to README.Win32
  - Added comments in POD about installation documentation
  - Added '/usr/local/opt/openssl/bin/openssl' to Openssl search path for
    latest version of OSX homebrew openssl
- Simplify find commands using -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.72-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Paul Howarth <paul@city-fan.org> - 1.72-2
- Prefer %%global over %%define

* Tue Sep 22 2015 Paul Howarth <paul@city-fan.org> - 1.72-1
- Update to 1.72
  - Fixed a problem where SvPVx_nolen was undefined in some versions of perl;
    replaced with SvPV_nolen
  - Fixed a cast warning on Darwin

* Fri Sep 18 2015 Paul Howarth <paul@city-fan.org> - 1.71-1
- Update to 1.71
  - Conditionalize support for MD4, MD5
  - Added support for linking libraries in /usr/local/lib64 for some flavours
    of Linux like RH Tikanga
  - Fixes to X509_check_host, X509_check_ip, SSL_CTX_set_alpn_protos, and
    SSL_set_alpn_protos so they will compile on MSVC and AIX cc
  - Fixed typos in documentation for X509_NAME_new and X509_NAME_hash
  - Version number in META.yml is now quoted
- Explicitly BR: perl-devel, needed for EXTERN.h

* Fri Jun 26 2015 Paul Howarth <paul@city-fan.org> - 1.70-1
- Update to 1.70
  - The new OpenSSL 1.0.2 X509_check_* functions are not available in current
    LibreSSL, so disable them in SSLeay.xs
  - Fixed a problem with building against OSX homebrew's openssl
  - Removed a test in t/local/33_x509_create_cert.t that fails due to changes
    in 1.0.1n and later

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.69-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.69-2
- Perl 5.22 rebuild

* Sun Jun  7 2015 Paul Howarth <paul@city-fan.org> - 1.69-1
- Update to 1.69
  - Testing with OpenSSL 1.0.2, 1.0.2a OK
  - Completed LibreSSL compatibility
  - Improved compatibility with OpenSSL 1.0.2a
  - Added the X509_check_* functions introduced in OpenSSL 1.0.2
  - Added support for X509_V_FLAG_TRUSTED_FIRST constant
  - Allow get_keyblock_size to work correctly with OpenSSL 1.0.1 onwards

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.68-3
- Perl 5.22 rebuild

* Mon May 18 2015 Paul Howarth <paul@city-fan.org> - 1.68-2
- SSLv3_method not dropped in OpenSSL 1.0.2, so revert that change (#1222521)

* Fri Jan 30 2015 Paul Howarth <paul@city-fan.org> - 1.68-1
- Update to 1.68
  - Improvements to inc/Module/Install/PRIVATE/Net/SSLeay.pm to handle the case
    where there are muliple OPENSSLs installed
  - Fixed a documentation error in get_peer_cert_chain
  - Fixed a problem with building on Windows that prevented correct OpenSSL
    directory detection with version 1.0.1j as delivered with Shining Light
    OpenSSL
  - Fixed a problem with building on Windows that prevented finding MT or MD
    versions of SSL libraries
  - Updated doc in README.Win32 to build with Microsoft Visual Studio 2010
    Express
  - Added Windows crypt32 library to Windows linking as some
    compilers/platforms seem to require it and it is innocuous otherwise
  - Fixed a failure in t/external/20_cert_chain.t where some platforms do not
    have HTTPS in /etc/services
  - Recent 1.0.2 betas have dropped the SSLv3_method function; we leave out
    the function on newer versions, much the same as the SSLv2 deprecation is
    handled
  - Fix the ALPN test, which was incorrectly failing on OpenSSL due to the
    LibreSSL check (earlier versions bailed out before that line)
  - Fixed a problem on OSX when macports openssl 1.x is installed: headers from
    macport were found but older OSX openssl libraries were linked, resulting
    in "Symbol not found: _EVP_MD_do_all_sorted"
  - Added notes about runtime error "no OPENSSL_Applink", when calling
    Net::SSLeay::P_PKCS12_load_file
- Don't change %%{__perl_provides} unless we need to

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.66-2
- Perl 5.20 mass

* Mon Sep  8 2014 Paul Howarth <paul@city-fan.org> - 1.66-1
- Update to 1.66
  - Fixed compile problem with perl prior to 5.8.8, similar to CPAN RT#76267
  - Fixed a problem with Socket::IPPROTO_TCP on early perls
  - After discussions with the community and the original author Sampo
    Kellomaki, the license conditions have been changed to "Perl Artistic
    License 2.0"
- License changed to Artistic 2.0
- Use %%license where possible

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.65-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Paul Howarth <paul@city-fan.org> - 1.65-1
- Update to 1.65
  - Added note to docs to make it clear that X509_get_subjectAltNames returns a
    packed binary IP address for type 7 - GEN_IPADD
  - Improvements to SSL_OCSP_response_verify to compile under non-c99 compilers
  - Port to Android, includes Android-specific version of RSA_generate_key
  - Added LibreSSL support
  - Patch that fixes the support for SSL_set_info_callback and adds
    SSL_CTX_set_info_callback and SSL_set_state; support for these functions is
    necessary to either detect renegotiation or to enforce renegotiation
  - Fixed a problem with SSL_set_state not available on some early OpenSSLs
  - Removed arbitrary size limits from calls to tcp_read_all in tcpcat() and
    http_cat()
  - Removed unnecessary Debian_CPANTS.txt from MANIFEST - again

* Wed Jun 11 2014 Paul Howarth <paul@city-fan.org> - 1.64-1
- Update to 1.64
  - Test ocsp.t now does not fail if HTTP::Tiny is not installed
  - Fixed repository in META.yml
  - Fixed a problem with SSL_get_peer_cert_chain: if the SSL handshake results
    in an anonymous authentication, like ADH-DES-CBC3-SHA, get_peer_cert_chain
    will not return an empty list, but instead return the SSL object
  - Fixed a problem where patch
    https://git.openssl.org/gitweb/?p=openssl.git;a=commit;h=3009244d
    caused a failed test in t/local/33_x509_create_cert.t

* Sun Jun  8 2014 Paul Howarth <paul@city-fan.org> - 1.63-3
- Fix failing test with openssl-1.0.1h (upstream commit 414, CPAN RT#96256)

* Sat Jun  7 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Paul Howarth <paul@city-fan.org> - 1.63-1
- Update to 1.63
  - Improvements to OCSP support: it turns out that some CAs (like Verisign)
    sign the OCSP response with the CA we have in the trust store and don't
    attach this certifcate in the response, but OpenSSL by itself only
    considers the certificates included in the response and
    SSL_OCSP_response_verify added the certificates in the chain too, so now
    we also add the trusted CA from the store which signed the lowest chain
    certificate, at least if we could not verify the OCSP response without
    doing it
  - Fixed some compiler warnings
- BR: perl(HTTP::Tiny) for test suite

* Mon May 12 2014 Paul Howarth <paul@city-fan.org> - 1.61-1
- Update to 1.61
  - Fixed a typo in an error message
  - Fixed a problem with building with openssl that does not support OCSP
  - Fixed some newly introduced warnings if compiled with -Wall
  - Fixed format string issue causing build failures
  - Changed calloc to Newx and free to Safefree, otherwise there might be
    problems because calloc is done from a different memory pool than free
    (depends on the build options for perl, but seen on Windows)

* Sat May 10 2014 Paul Howarth <paul@city-fan.org> - 1.59-1
- Update to 1.59
  - Fixed local/30_error.t so that tests do not fail if diagnostics are enabled
  - Fixed error messages about undefined strings used with length or split
  - Improvements to configuration of OPTIMIZE flags, to prevent overriding of
    perl's expected optimization flags
  - SSL_peek() now returns openssl error code as second item when called in
    array context, same as SSL_read
  - Fixed some warnings
  - Added support for tlsv1.1 tlsv1.2 via $Net::SSLeay::ssl_version
  - Improve examples in 'Using other perl modules based on Net::SSLeay'
  - Added support for OCSP
  - Added missing t/external/ocsp.t
- Add patch to stop gcc complaining about format string usage

* Wed Jan 15 2014 Paul Howarth <paul@city-fan.org> - 1.58-1
- Update to 1.58
  - Always use size_t for strlen() return value
  - t/external/20_cert_chain.t was missing from dist
  - Version number in META.yml was incorrect
  - Improvements to test t/external/20_cert_chain.t to provoke following bug:
    fixed crash due to SSL_get_peer_cert_chain incorrectly free'ing the chain
    after use
  - Fixed a problem when compiling against openssl where OPENSSL_NO_EC is set
- Drop Fedora/EL ECC support patch, no longer needed

* Sun Jan 12 2014 Paul Howarth <paul@city-fan.org> - 1.57-1
- Update to 1.57
  - Fixed remaining problems with test suite: pod coverage and kwalitee tests
    are only enabled with RELEASE_TESTING=1

* Wed Jan  8 2014 Paul Howarth <paul@city-fan.org> - 1.56-1
- Update to 1.56
  - Fixed a typo in documentation of BEAST Attack
  - Added LICENSE file copied from OpenSSL distribution to prevent complaints
    from various versions of kwalitee
  - Adjusted license: in META.yml to be 'openssl'
  - Adds support for the basic operations necessary to support ECDH for PFS,
    e.g. EC_KEY_new_by_curve_name, EC_KEY_free and SSL_CTX_set_tmp_ecdh
  - Improvements to t/handle/external/50_external.t to handle the case when a
    test connection was not possible
  - Added support for ALPN TLS extension
  - Fixed a use-after-free error
  - Fixed a problem with invalid comparison on OBJ_cmp result in
    t/local/36_verify.t
  - Added support for get_peer_cert_chain()
  - Fixed a bug that could cause stack faults: mixed up PUTBACK with SPAGAIN in
    ssleay_RSA_generate_key_cb_invoke(); a final PUTBACK is needed here
  - Fixed cb->data checks and wrong refcounts on &PL_sv_undef
  - Deleted support for SSL_get_tlsa_record_byname: it is not included in
    OpenSSL git master
- Drop upstreamed patch for CPAN RT#91215
- Skip the Pod Coverage test, as there are naked subroutines in this release
- ECC support not available in Fedora/EL until OpenSSL 1.0.1e, so patch the
  source accordingly to fix builds for F-12 .. F-17

* Fri Dec  6 2013 Paul Howarth <paul@city-fan.org> - 1.55-6
- Fix usage of OBJ_cmp in the test suite (CPAN RT#91215)

* Sun Dec  1 2013 Paul Howarth <paul@city-fan.org> - 1.55-5
- Drop the kwalitee test for now as it's too fussy for the current code

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.55-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.55-2
- Perl 5.18 rebuild

* Sat Jun  8 2013 Paul Howarth <paul@city-fan.org> - 1.55-1
- update to 1.55
  - added support for TLSV1_1 and TLSV1_2 methods with SSL_CTX_tlsv1_1_new(),
    SSL_CTX_tlsv1_2_new(), TLSv1_1_method() and TLSv1_2_method(), where
    available in the underlying openssl
  - added CRL support functions X509_CRL_get_ext(), X509_CRL_get_ext_by_NID(),
    X509_CRL_get_ext_count()
  - fixed a problem that could cause content with a value of '0' to be
    incorrectly encoded by do_httpx3 and friends (CPAN RT#85417)
  - added support for SSL_get_tlsa_record_byname() required for DANE support in
    openssl-1.0.2 and later
  - testing with openssl-1.0.2-stable-SNAP-20130521
  - added X509_NAME_new and X509_NAME_hash

* Sat Mar 23 2013 Paul Howarth <paul@city-fan.org> - 1.54-1
- update to 1.54
  - added support for SSL_export_keying_material where present (i.e. in OpenSSL
    1.0.1 and later)
  - changed t/handle/external/50_external.t to use www.airspayce.com instead of
    perldition.org, who no longer have an https server
  - patch to fix a crash: P_X509_get_crl_distribution_points on an X509
    certificate with values in the CDP extension that do not have an ia5 string
    would cause a segmentation fault when accessed
  - change in t/local/32_x509_get_cert_info.t to not use
    Net::SSLeay::ASN1_INTEGER_get, since it works differently on 32 and 64 bit
    platforms
  - updated author and distribution location details to airspayce.com
  - improvement to test 07_sslecho.t so that if set_cert_and_key fails we can
    tell why

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.52-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  9 2013 Paul Howarth <paul@city-fan.org> - 1.52-1
- update to 1.52
  - rebuild package with gnu format tar, to prevent problems with unpacking on
    other systems such as old Solaris

* Fri Dec 14 2012 Paul Howarth <paul@city-fan.org> - 1.51-1
- update to 1.51
  - fixed a problem where SSL_set_SSL_CTX is not available with
    OpenSSL < 0.9.8f (CPAN RT#81940)
- fix bogus date in spec changelog

* Thu Dec 13 2012 Paul Howarth <paul@city-fan.org> - 1.50-1
- update to 1.50
  - fixed a problem where t/handle/external/50_external.t would crash if any of
    the test sites were not contactable
  - now builds on VMS, added README.VMS
  - fixed a few compiler warnings in SSLeay.xs; most of them are just
    signed/unsigned pointer mismatches but there is one that actually fixes
    returning what would be an arbitrary value off the stack from
    get_my_thread_id if it happened to be called in a non-threaded build
  - added SSL_set_tlsext_host_name, SSL_get_servername, SSL_get_servername_type,
    SSL_CTX_set_tlsext_servername_callback for server side Server Name
    Indication (SNI) support
  - fixed a problem with C++ comments preventing builds on AIX and HPUX
  - perdition.org not available for tests, changed to www.open.com.au
  - added SSL_FIPS_mode_set
  - improvements to test suite so it succeeds with and without FIPS mode
    enabled
  - added documentation, warning not to pass UTF-8 data in the content
    argument to post_https

* Tue Sep 25 2012 Paul Howarth <paul@city-fan.org> - 1.49-1
- update to 1.49
  - fixed problem where on some platforms test t/local/07_tcpecho.t would bail
    out if it could not bind port 1212; it now tries a number of ports to bind
    to until successful
  - improvements to unsigned casting
  - improvements to Net::SSLeay::read to make it easier to use with
    non-blocking IO: it modifies Net::SSLeay::read() to return the result from
    SSL_read() as the second return value, if Net::SSLeay::read() is called in
    list context (its behavior should be unchanged if called in scalar or void
    context)
  - fixed a problem where t/local/kwalitee.t fails with
    Module::CPANTS::Analyse 0.86
  - fixed a number of typos
  - fixed a compiler warning from Compiling with gcc-4.4 and -Wall
  - Fixed problems with get_https4: documentation was wrong, $header_ref was
    not correctly set and $server_cert was not returned
  - fixed a problem that could cause a Perl exception about no blength method
    on undef (CPAN RT#79309)
  - added documentation about how to mitigate various SSL/TLS vulnerabilities
  - SSL_MODE_* are now available as constants
- drop upstreamed pod encoding patch

* Mon Aug 20 2012 Paul Howarth <paul@city-fan.org> - 1.48-6
- fix POD encoding (CPAN RT#78281)
- classify buildreqs by usage
- BR:/R: perl(XSLoader)

* Mon Aug 13 2012 Petr Pisar <ppisar@redhat.com> - 1.48-5
- specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.48-3
- perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.48-2
- perl 5.16 rebuild

* Wed Apr 25 2012 Paul Howarth <paul@city-fan.org> - 1.48-1
- update to 1.48
  - removed unneeded Debian_CPANTS.txt from MANIFEST
  - fixed incorrect documentation about the best way to call CTX_set_options
  - fixed problem that caused "Undefined subroutine utf8::encode" in
    t/local/33_x509_create_cert.t (on perl 5.6.2)
  - in examples and pod documentation, changed #!/usr/local/bin/perl
    to #!/usr/bin/perl
  - t/local/06_tcpecho.t now tries a number of ports to bind to until
    successful
- no longer need to fix shellbangs in examples

* Thu Apr 19 2012 Paul Howarth <paul@city-fan.org> - 1.47-3
- simplify Test::Kwalitee conditional

* Thu Apr 19 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.47-2
- make module Kwalitee conditional

* Wed Apr  4 2012 Paul Howarth <paul@city-fan.org> - 1.47-1
- update to 1.47
  - fixed overlong lines and spelling errors in pod
  - fixed extra "garbage" files in 1.46 tarball
  - fixed incorrect fail reports on some 64 bit platforms
  - fix to avoid FAIL reports from cpantesters with missing openssl
  - use my_snprintf from ppport.h to prevent link failures with perl 5.8 and
    earlier when compiled with MSVC

* Tue Apr  3 2012 Paul Howarth <paul@city-fan.org> - 1.46-1
- update to 1.46 (see Changes file for details)
- BR: openssl as well as openssl-devel, needed for building
- no longer need help to find openssl
- upstream no longer shipping TODO
- drop %%defattr, redundant since rpm 4.4

* Sat Feb 25 2012 Paul Howarth <paul@city-fan.org> - 1.45-1
- update to 1.45 (see Changes file for full details)
  - added thread safety and dynamic locking, which should complete thread
    safety work, making Net::SSLeay completely thread-safe
  - lots of improved documentation
- BR: perl(Test::Pod::Coverage)
- install Net/SSLeay.pod as %%doc

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.42-2
- use DESTDIR rather than PERL_INSTALL_ROOT
- use %%{_fixperms} macro rather than our own chmod incantation
- BR: perl(AutoLoader), perl(Exporter), perl(Socket)

* Mon Oct  3 2011 Paul Howarth <paul@city-fan.org> - 1.42-1
- update to 1.42
  - fixed incorrect documentation of how to enable CRL checking
  - fixed incorrect letter in Sebastien in Credits
  - changed order of the Changes file to be reverse chronological
  - fixed a compile error when building on Windows with MSVC6
- drop UTF8 patch, no longer needed

* Sun Sep 25 2011 Paul Howarth <paul@city-fan.org> - 1.41-1
- update to 1.41
  - fixed incorrect const signatures for 1.0 that were causing warnings; now
    have clean compile with 0.9.8a through 1.0.0
- BR: perl(Carp)

* Fri Sep 23 2011 Paul Howarth <paul@city-fan.org> - 1.40-1
- update to 1.40
  - fixed incorrect argument type in call to SSL_set1_param
  - fixed a number of issues with pointer sizes; removed redundant pointer cast
    tests from t/
  - added Perl version requirements to SSLeay.pm

* Wed Sep 21 2011 Paul Howarth <paul@city-fan.org> - 1.39-1
- update to 1.39
  - downgraded Module::Install to 0.93 since 1.01 was causing problems in the
    Makefile

* Fri Sep 16 2011 Paul Howarth <paul@city-fan.org> - 1.38-1
- update to 1.38
  - fixed a problem with various symbols that only became available in OpenSSL
    0.9.8 such as X509_VERIFY_PARAM and X509_POLICY_NODE, causing build
    failures with older versions of OpenSSL (CPAN RT#71013)

* Fri Sep 16 2011 Paul Howarth <paul@city-fan.org> - 1.37-1
- update to 1.37
  - added X509_get_fingerprint
  - added support for SSL_CTX_set1_param, SSL_set1_param and selected
    X509_VERIFY_PARAM_* OBJ_* functions
  - fixed the prototype for randomize()
  - fixed an uninitialized value warning in $Net::SSLeay::proxyauth
  - allow net-ssleay to compile if SSLV2 is not present
  - fixed a problem where sslcat (and possibly other functions) expect RSA
    keys and will not load DSA keys for client certificates
  - removed SSL_CTX_v2_new and SSLv2_method() for OpenSSL 1.0 and later
  - added CTX_use_PKCS12_file
- this release by MIKEM => update source URL

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.36-7
- Perl mass rebuild

* Thu Jul 14 2011 Paul Howarth <paul@city-fan.org> - 1.36-6
- BR: perl(Test::Kwalitee) if we're not bootstrapping
- explicitly BR: pkgconfig
- use a patch rather than a scripted iconv to fix the character encoding
- modernize provides filter
- stop running the tests in verbose mode
- nobody else likes macros for commands

* Wed Jul 13 2011 Iain Arnell <iarnell@gmail.com> - 1.36-5
- drop obsolete BRs Array::Compare, Sub::Uplevel, Tree::DAG_Node

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.36-3
- rebuild to fix problems with vendorarch/lib (#661697)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.36-2
- mass rebuild with perl-5.12.0

* Sun Jan 31 2010 Paul Howarth <paul@city-fan.org> - 1.36-1
- update to 1.36 (see Changes for details)
- drop svn patches

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.35-8
- rebuild against perl 5.10.1

* Sat Aug 22 2009 Paul Howarth <paul@city-fan.org> - 1.35-7
- update to svn trunk (rev 252), needed due to omission of MD2 functionality
  from OpenSSL 1.0.0 (CPAN RT#48916)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.35-6
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.35-5
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar  8 2009 Paul Howarth <paul@city-fan.org> - 1.35-4
- filter out unwanted provides for perl shared objects
- run tests in verbose mode

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.35-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.35-2
- rebuild with new openssl

* Mon Jul 28 2008 Paul Howarth <paul@city-fan.org> - 1.35-1
- update to 1.35
- drop flag and patch for enabling/disabling external tests - patch now upstream
- external hosts patch no longer needed as we don't do external tests
- filter out unversioned provide for perl(Net::SSLeay)
- use the distro openssl flags rather than guessing them

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.32-5
- rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.32-4
- autorebuild for GCC 4.3

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.32-3
- rebuild for new perl

* Wed Dec  5 2007 Paul Howarth <paul@city-fan.org> - 1.32-2
- rebuild with new openssl

* Wed Nov 28 2007 Paul Howarth <paul@city-fan.org> - 1.32-1
- update to 1.32, incorporate new upstream URLs
- cosmetic spec changes suiting new maintainer's preferences
- fix argument order for find with -depth
- remove patch for CVE-2005-0106, fixed upstream in 1.30 (#191351)
  (http://rt.cpan.org/Public/Bug/Display.html?id=19218)
- remove test patch, no longer needed
- re-encode Credits as UTF-8
- include TODO as %%doc
- add buildreqs perl(Array::Compare), perl(MIME::Base64), perl(Sub::Uplevel),
  perl(Test::Exception), perl(Test::NoWarnings), perl(Test::Pod),
  perl(Test::Warn), perl(Tree::DAG_Node)
- add patch needed to disable testsuite non-interactively
- run test suite but disable external tests by default; external tests can be
  enabled by using rpmbuild --with externaltests
- add patch to change hosts connected to in external tests

* Fri Nov 16 2007 Parag Nemade <panemade@gmail.com> - 1.30-7
- Merge Review (#226272) Spec cleanup

* Tue Nov  6 2007 Stepan Kasal <skasal@redhat.com> - 1.30-6
- fix a typo in description (#231756, #231757)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.30-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 21 2007 Warren Togami <wtogami@redhat.com> - 1.30-5
- rebuild

* Fri Jul 14 2006 Warren Togami <wtogami@redhat.com> - 1.30-4
- import into FC6

* Tue Feb 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.30-3
- Rebuild for FC5 (perl 5.8.8).

* Fri Jan 27 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.30-2
- CVE-2005-0106: patch from Mandriva
  http://wwwnew.mandriva.com/security/advisories?name=MDKSA-2006:023

* Sun Jan 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.30-1
- 1.30.
- Optionally run the test suite during build with "--with tests".

* Wed Nov  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.26-3
- Rebuild for new OpenSSL.
- Cosmetic cleanups.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.26-2
- rebuilt

* Mon Dec 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.26-1
- Drop fedora.us release prefix and suffix.

* Mon Oct 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.26-0.fdr.2
- Convert manual page to UTF-8.

* Tue Oct 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.26-0.fdr.1
- Update to unofficial 1.26 from Peter Behroozi, adds get1_session(),
  enables session caching with IO::Socket::SSL (bug 1859, bug 1860).
- Bring outdated test14 up to date (bug 1859, test suite still not enabled).

* Sun Jul 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.25-0.fdr.4
- Rename to perl-Net-SSLeay, provide perl-Net_SSLeay for compatibility
  with the rest of the world.

* Wed Jul  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.25-0.fdr.3
- Bring up to date with current fedora.us Perl spec template.
- Include examples in docs.

* Sun Feb  8 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.25-0.fdr.2
- Reduce directory ownership bloat.

* Fri Oct 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.25-0.fdr.1
- First build.
