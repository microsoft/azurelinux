#
# spec file for package boringssl
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%define _binaries_in_noarch_packages_terminate_build 0
%define sover 1
%define libname libboringssl%{sover}
%define src_install_dir %{_prefix}/src/%{name}
Summary:        An SSL/TLS protocol implementation
Name:           boringssl
Version:        20200921
Release:        3%{?dist}
License:        OpenSSL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Sources
URL:            https://boringssl.googlesource.com/boringssl/
#Source0:       https://boringssl.googlesource.com/boringssl/+archive/3743aafdacff2f7b083615a043a37101f740fa53.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         0002-crypto-Fix-aead_test-build-on-aarch64.patch
Patch1:         0003-enable-s390x-builds.patch
Patch2:         0004-fix-alignment-for-ppc64le.patch
Patch3:         0005-fix-alignment-for-arm.patch
BuildRequires:  cmake >= 3.0
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  go
BuildRequires:  libunwind-devel
BuildRequires:  ninja-build
BuildRequires:  patchelf
ExclusiveArch:  x86_64 aarch64

%description
BoringSSL is an implementation of the Secure Sockets Layer (SSL) and
Transport Layer Security (TLS) protocols, derived from OpenSSL.

%package -n %{libname}
Summary:        An SSL/TLS protocol implementation
Group:          System/Libraries
Recommends:     ca-certificates-mozilla

%description -n %{libname}
BoringSSL is an implementation of the Secure Sockets Layer (SSL) and
Transport Layer Security (TLS) protocols, derived from OpenSSL.

%package devel
Summary:        Development files for BoringSSL
Group:          Development/Libraries/C and C++
Requires:       %{libname} = %{version}

%description devel
Development files for BoringSSL - an implementation of the Secure
Sockets Layer (SSL) and Transport Layer Security (TLS) protocols,
derived from OpenSSL.

%package source
Summary:        Source code of BoringSSL
Group:          Development/Sources
BuildArch:      noarch

%description source
Source files for BoringSSL implementation

%prep
%setup -q -c -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%cmake \
  -DCMAKE_SHARED_LINKER_FLAGS="%{?build_ldflags} -Wl,--as-needed -Wl,-z,now"
%cmake_build

%install
# Install libraries
install -D -m0755 ./libcrypto.so %{buildroot}%{_libdir}/libboringssl_crypto.so.%{sover}
install -D -m0755 ./libssl.so %{buildroot}%{_libdir}/libboringssl_ssl.so.%{sover}
# Add SOVER to SONAME fields in libraries
patchelf --set-soname libboringssl_crypto.so.%{sover} %{buildroot}%{_libdir}/libboringssl_crypto.so.%{sover}
patchelf --set-soname libboringssl_ssl.so.%{sover} %{buildroot}%{_libdir}/libboringssl_ssl.so.%{sover}
# Create links from *.so to *.so.SOVER
ln -sf libboringssl_crypto.so.%{sover} %{buildroot}%{_libdir}/libboringssl_crypto.so
ln -sf libboringssl_ssl.so.%{sover} %{buildroot}%{_libdir}/libboringssl_ssl.so

# Install sources
rm -rf build/
mkdir -p %{buildroot}%{src_install_dir}
cp -r * %{buildroot}%{src_install_dir}
%fdupes %{buildroot}%{src_install_dir}
# Fix arch-independent-package-contains-binary-or-object
find %{buildroot}%{src_install_dir} -type f \( -name "*.a" -o -name "*.lib" -o -name "*.o" \) -exec rm -f "{}" +
# Fix non-executable-script warning.
find %{buildroot}%{src_install_dir} -type f -name "*.sh" -exec chmod +x "{}" +
# Fix env-script-interpreter error.
find %{buildroot}%{src_install_dir} -type f -name "*.pl" -exec sed -i 's|#!.*/usr/bin/env perl|#!%{_bindir}/perl|' "{}" +
find %{buildroot}%{src_install_dir} -type f -name "*.py" -exec sed -i 's|#!.*/usr/bin/env python.*|#!%{_bindir}/python3|' "{}" +
find %{buildroot}%{src_install_dir} -type f -name "*.sh" -exec sed -i 's|#!.*/usr/bin/env bash|#!/bin/bash|' "{}" +

# To avoid conflicts with openssl development files, change all includes from
# openssl to boringssl.
# BoringSSL headers provided by this pachage are installed in
# /usr/include/boringssl for the same reason.
find src/include/openssl -type f -exec sed -i 's/openssl/boringssl/' "{}" +

find src/include/openssl -type f -execdir install -D -m0644 "{}" "%{buildroot}%{_includedir}/boringssl/{}" \;

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%doc src/README.md
%license LICENSE
%{_libdir}/libboringssl_crypto.so.%{sover}
%{_libdir}/libboringssl_ssl.so.%{sover}

%files devel
%{_includedir}/boringssl
%{_libdir}/libboringssl_crypto.so
%{_libdir}/libboringssl_ssl.so

%files source
%{src_install_dir}

%changelog

* Tue Nov 30 2021 Mateusz Malisz <mamalisz@microsoft.com> - 20200921-3
- Unify macro syntax used in the spec.

* Tue Oct 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200921-2
- Switching to using a single digit for the 'Release' tag.

* Thu Jun 10 2021 Henry Li <lihl@microsoft.com> - 20200921-1.2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License Verified
- Fix Source URL
- Change build requirement from ninja to ninja-build
- Modify location of shared library files
- Add _binaries_in_noarch_packages_terminate_build definition to resolve arch dependent binary error
- Remove unsupported architectures in CBL-Mariner from ExclusiveArch list

* Mon May 17 2021 mrostecki@suse.com
- Update to version 20200921 (fixes bsc#1183836, bsc#1181866):
  * Add SSL_CIPHER_get_protocol_id.
  * Add TrustTokenV2.
  * Add X509_get_pathlen and X509_REVOKED_get0_extensions.
  * Add some accommodations for FreeRDP
  * Require non-NULL store in X509_STORE_CTX_init.
  * Const-correct X509V3_CONF_METHOD.
  * Avoid unions in X509_NAME logic.
  * Bump OPENSSL_VERSION_NUMBER to 1.1.1.
  * Document more of x509.h.
  * Fix potential leak in bssl::Array::Shrink.
  * Remove ASN1_STRING_length_set.
  * Revert "Check AlgorithmIdentifier parameters for RSA and ECDSA signatures."
  * Implement PSK variants of HPKE setup functions.
  * acvp: support working with files.
  * Document a few more functions in x509.h.
  * Add subject key ID and authority key ID accessors.
  * Remove sxnet and pkey_usage_period extensions.
  * Const-correct various X509 functions.
  * Make X509_set_not{Before,After} functions rather than macros.
  * Add X509_get0_uids from OpenSSL 1.1.0.
  * Bound RSA and DSA key sizes better.
  * Add set1 versions of X509 timestamp setters.
  * Consistently sort generated build files.
  * delocate: use 64-bit GOT offsets in the large memory model.
  * Update HPKE implementation and test vectors to draft-irtf-cfrg-hpke-05.
  * Handle NULL arguments in some i2d_* functions.
  * aarch64: support BTI and pointer authentication in assembly
  * Support delegated credentials verison 06
  * delocation: large memory model support.
  * Enforce presence of ALPN when QUIC is in use.
  * Fix the naming of alert error codes.
  * Use golang.org/x/crypto in runner.
  * Disable ClientHello padding for QUIC.
  * Add X509_SIG_get0 and X509_SIG_getm.
  * Implement HPKE.
  * Disallow TLS 1.3 compatibility mode in QUIC.
  * Switch clang-format IncludeBlocks to Preserve.
  * Fix unterminated clang-format off.
  * Add line number to doc.go error messages.
  * Kick the bots.
  * Add a JSON output to generate_build_files.py.
  * Add details of 20190808 FIPS certification.
  * Link to ws2_32 more consistently.
  * Allow explicitly-encoded X.509v1 versions for now.
  * Opaquify PKCS8_PRIV_KEY_INFO.
  * Implement i2d_PUBKEY and friends without crypto/asn1.
  * Remove TRUST_TOKEN_experiment_v0.
  * Clarify in-place rules for low-level AES mode functions.
  * acvp: add CMAC-AES support.
  * acvp: add SP800-108 KDF support.
  * Remove x509->name.
  * Maybe build for AArch64 Windows.
  * sha1-x86_64: fix CFI.
  * Use |crypto_word_t| and |size_t| more consistently in ECC scalar recoding.
  * Enable shaext path for sha1.
  * Avoid relying on SSL_get_session's behavior during the handshake.
  * Add a -wait-for-debugger flag to runner.
  * Add missing OPENSSL_EXPORT to X509_get_X509_PUBKEY.
  * Const-correct various functions in crypto/asn1.
  * Remove uneeded switch statement.
  * Convert X.509 accessor macros to proper functions.
  * Remove X509_CINF_get_issuer and X509_CINF_get_extensions.
  * Remove X509_get_signature_type.
  * clang-format x509.h and run comment converter.
  * Check AlgorithmIdentifier parameters for RSA and ECDSA signatures.
  * Remove some unimplemented prototypes.
  * Check the X.509 version when parsing.
  * Fix x509v3_cache_extensions error-handling.
  * Work around Windows command-line limits in embed_test_data.go.
  * Move crypto/x509 test data into its own directory.
  * Test resumability of same, different, and default ticket keys.
  * Fixes warning when redefining PATH_MAX when building with MINGW.
  * Abstract fd operations better in tool.
  * Use CMAKE_SIZEOF_VOID_P instead of CMAKE_CL_64
  * Enforce the keyUsage extension in TLS 1.2 client certs.
  * Reword some comments.
  * Add “Z Computation” KAT.
  * acvptool: handle negative sizeConstraint.
  * Let memory hooks override the size prefix.
  * acvptool: go fmt
  * Assert md_size > 0.
  * Remove -enable-ed25519 compat hack.
  * Add a |SSL_process_tls13_new_session_ticket|.
  * Use ctr32 optimizations for AES_ctr128_encrypt.
  * Test AES mode wrappers.
  * Bump minimum CMake version.
  * Modify how QUIC 0-RTT go/no-go decision is made.
  * Remove RAND_set_urandom_fd.
  * Document that getrandom support must be consistent.
  * Fix docs link for SSL_CTX_load_verify_locations
  * Fix TRUST_TOKEN experiment_v1 SRR map.
  * Add CRYPTO_pre_sandbox_init.
  * Still query getauxval if reading /proc/cpuinfo fails.
  * Add missing header to ec/wnaf.c
  * Fix OPENSSL_TSAN typo.
  * Fix p256-x86_64-table.h indentation.
  * Enable avx2 implementation of sha1.
  * Trim Z coordinates from the OPENSSL_SMALL P-256 tables.
  * Use public multi-scalar mults in Trust Tokens where applicable.
  * Use batched DLEQ proofs for Trust Token.
  * Restrict when 0-RTT will be accepted in QUIC.
  * Disable TLS 1.3 compatibility mode for QUIC.
  * Use a 5-bit comb for some Trust Tokens multiplications.
  * Use a (mostly) constant-time multi-scalar mult for Trust Tokens.
  * Batch inversions in Trust Tokens.
  * Rearrange the DLEQ logic slightly.
  * Use token hash to encode private metadata for Trust Token Experiment V1.
  * Introduce an EC_AFFINE abstraction.
  * Make the fuzzer PRNG thread-safe.
  * Disable fork-detect tests under TSAN.
  * Introduce TRUST_TOKENS_experiment_v1.
  * Route PMBToken calls through TRUST_TOKEN_METHOD.
  * Introduce a TRUST_TOKEN_METHOD hook to select TRUST_TOKEN variations.
  * fork_detect: be robust to qemu.
  * Move serialization of points inside pmbtoken.c.
  * Introduce PMBTOKENS key abstractions.
  * Fix the types used in token counts.
  * Remove unused code from ghash-x86_64.pl.
  * Switch the P-384 hash-to-curve to draft-07.
  * Add hash-to-curve code for P384.
  * Write down the expressions for all the NIST primes.
  * Move fork_detect files into rand/
  * Harden against fork via MADV_WIPEONFORK.
  * Fix typo in comment.
  * Use faster addition chains for P-256 field inversion.
  * Tidy up third_party/fiat.
  * Prefix g_pre_comp in p256.c as well.
  * Add missing curve check to ec_hash_to_scalar_p521_xmd_sha512.
  * Add a tool to compare the output of bssl speed.
  * Benchmark ECDH slightly more accurately.
  * Align remaining Intel copyright notice.
  * Don't retain T in PMBTOKEN_PRETOKEN.
  * Check for trailing data in TRUST_TOKEN_CLIENT_finish_issuance.
  * Properly namespace everything in third_party/fiat/p256.c.
  * Update fiat-crypto.
  * Add missing ERR_LIB_TRUST_TOKEN constants.
  * Add bssl speed support for hashtocurve and trusttoken.
  * Implement DLEQ checks for Trust Token.
  * Fix error-handling in EVP_BytesToKey.
  * Fix Trust Token CBOR.
  * Match parameter names between header and source.
  * Trust Token Implementation.
  * Include mem.h for |CRYPTO_memcmp|
  * acvptool: add subprocess tests.
  * Add SHA-512-256.
  * Make ec_GFp_simple_cmp constant-time.
  * Tidy up CRYPTO_sysrand variants.
  * Do a better job testing EC_POINT_cmp.
  * Follow-up comments to hash_to_scalar.
  * Add a hash_to_scalar variation of P-521's hash_to_field.
  * Add SSL_SESSION_copy_without_early_data.
  * Double-check secret EC point multiplications.
  * Make ec_felem_equal constant-time.
  * Fix hash-to-curve comment.
  * Make ec_GFp_simple_is_on_curve constant-time.
  * Implement draft-irtf-cfrg-hash-to-curve-06.
  * Update list of tested SDE configurations.
  * Only draw from RDRAND for additional_data if it's fast.
  * Generalize bn_from_montgomery_small.
  * Remove BIGNUM from uncompressed coordinate parsing.
  * Add EC_RAW_POINT serialization function.
  * Base EC_FELEM conversions on bytes rather than BIGNUMs.
  * runner: Replace supportsVersions calls with allVersions.
  * Enable QUIC for some perMessageTest runner tests
  * Move BN_nnmod calls out of low-level group_set_curve.
  * Clean up various EC inversion functions.
  * Start to organize ec/internal.h a little.
  * Fix CFI for AVX2 ChaCha20-Poly1305.
  * Remove unused function prototype.
  * Enable more runner tests for QUIC
  * Require QUIC method with Transport Parameters and vice versa
  * acvptool: support non-interactive mode.
  * Add is_quic bit to SSL_SESSION
  * Update SDE.
  * Update tools.
  * Add simpler getters for DH and DSA.
  * Don't define default implementations for weak symbols.
  * Don't automatically run all tests for ABI testing.
  * Fix test build with recent Clang.
  * Remove LCM dependency from RSA_check_key.
  * Simplify bn_sub_part_words.
  * No-op commit to test Windows SDE bots.
  * ABI-test each AEAD.
  * Add memory tracking and sanitization hooks
  * Add X509_STORE_CTX_get0_chain.
  * Add DH_set_length.
  * Static assert that CRYPTO_MUTEX is sufficiently aligned.
  * [bazel] Format toplevel BUILD file with buildifier
  * Add |SSL_CTX_get0_chain|.
  * Configure QUIC secrets inside set_{read,write}_state.
  * Allow setting QUIC transport parameters after parsing the client's
  * Fix comment for |BORINGSSL_self_test|.
  * Trust Token Key Generation.
  * Revise QUIC encryption secret APIs.
  * Fix ec_point_mul_scalar_public's documentation.
  * Don't infinite loop when QUIC tests fail.
  * Tidy up transitions out of 0-RTT keys on the client.
  * Remove bn_sub_part_words assembly.
  * Keep the encryption state and encryption level in sync.
  * Add ECDSA_SIG_get0_r and ECDSA_SIG_get0_s.
  * Fix a couple of comment typos.
  * Const-correct various X509_NAME APIs.
  * Ignore old -enable-ed25519 flag.
  * Provide __NR_getrandom fillins in urandom test too.
  * Skip RSATest.DISABLED_BlindingCacheConcurrency in SDE.
  * Fix client handling of 0-RTT rejects with cipher mismatch.
  * runner: Tidy up 0-RTT support.
  * Add X509_getm_notBefore and X509_getm_notAfter.
  * Clean up TLS 1.3 handback logic.
  * Require handshake flights end at record boundaries.
  * Delete unreachable DTLS check.
  * Rename TLS-specific functions to tls_foo from ssl3_foo.
  * Rename ssl3_choose_cipher.
  * SSL_apply_handback: don't choke on trailing data.
  * ssl_test: test early data with split handshakes.
  * Check for overflow in massive mallocs.
  * Add more convenient RSA getters.
  * Remove SSL_CTX_set_ed25519_enabled.
  * Improve signature algorithm tests.
  * bazel: explicitly load C++ rules
  * Check enum values in handoff.
  * Restore fuzz/cert_corpus.
  * Add a -sigalgs option to bssl client.
  * Add SSL_set_verify_algorithm_prefs.
  * Switch verify sigalg pref functions to SSL_HANDSHAKE.
  * Add SSL_AD_NO_APPLICATION_PROTOCOL
  * Refresh corpora due to TLS 1.3 changes in handoff serialization.
  * handoff: set |enable_early_data| as part of handback.
  * Add 109 and 120 to SSL_alert_desc_string_long
  * runner: enable split handshake tests for TLS 1.3.
  * Make TLS 1.3 split handshakes work with early data.
  * Split half-RTT tickets out into a separate TLS 1.3 state.
  * Use BCryptGenRandom when building as Windows UWP app.

* Thu May 28 2020 Jan Engelhardt <jengelh@inai.de>
- Rectify groups.

* Wed May 27 2020 Michał Rostecki <mrostecki@suse.com>
- Remove patch for enabling shared linking - it was enabled
  upstream.
  * 0001-add-soversion-option.patch
- Add boringssl-source subpackage.

* Wed May 27 2020 mrostecki@suse.com
- Update to version 20200122:
  * Define EVP compatibility constants for X448 and Ed448.
  * Allow shared libraries in the external CMake build.
  * Add a few little-endian functions to CBS/CBB.
  * Move iOS asm tricks up in external CMake build.
  * Try again to deal with expensive tests.
  * Restore ARM CPU variation tests on builders.
  * Remove SSL_CTX_set_rsa_pss_rsae_certs_enabled.
  * Work around another NULL/0 C language bug.
  * Use the MAYBE/DISABLED pattern in RSATest.BlindingCacheConcurrency.
  * Switch an #if-0-gated test to DISABLED_Foo.
  * Proxy: send whole SSL records through the handshaker.
  * Disable Wycheproof primality test cases on non-x86 (too slow)
  * test_state.cc: serialize the test clock.
  * Output after every Wycheproof primality test.
  * Maybe fix generated-CMake build on Android and iOS.
  * Detect the NDK path from CMAKE_TOOLCHAIN_FILE.
  * Tell Go to build for GOOS=android when running on Android.
  * Reland bitsliced aes_nohw implementation.
  * Add bssl client option to load a hashed directory of cacerts.
  * No-op change to run the new NO_SSE2 builders.
  * Clarify that we perform the point-on-curve check.
  * Reduce size of BlindingCacheConcurrency test under TSAN.
  * Compare vpaes/bsaes conversions against a reference implementation.
  * Enable the SSE2 Poly1305 implementation on clang-cl.
  * Remove alignment requirement on CRYPTO_poly1305_finish.
  * Fix double-free under load.
  * Add some XTS tests.
  * Add EncodeHex and DecodeHex functions to test_util.h.
  * Revert "Replace aes_nohw with a bitsliced implementation."
  * Replace aes_nohw with a bitsliced implementation.
  * Switch HRSS inversion algorithm.
  * Run EVP_CIPHER tests in-place.
  * Add an option to disable SSE2 intrinsics for testing.
  * Dummy change to trigger master-with-bazel builder.
  * Drop use of alignas(64) in aead_test.cc
  * Add standalone CMake build to generate_build_files.py
  * TLS 1.3 split handshake initial support.
  * Import Wycheproof primality tests.
  * Split BN_prime_checks into two constants for generation and validation.
  * Add some Miller-Rabin tests from Wycheproof.
  * Import Wycheproof PKCS#1 decrypt tests.
  * Import Wycheproof OAEP tests.
  * Import Wycheproof PKCS#1 signing tests.
  * Skip JWK keys when converting Wycheproof tests.
  * Import Wycheproof's size-specific RSA PKCS#1 verifying tests.
  * Handle "acceptable" Wycheproof inputs unambiguously.
  * Import Wycheproof XChaCha20-Poly1305 tests.
  * Import Wycheproof HMAC tests.
  * Import Wycheproof HKDF tests.
  * bytestring: add methods for int64.
  * Update Wycheproof test vectors.
  * Add mock QUIC transport to runner
  * Add test vectors for CVE-2019-1551 (not affected).
  * Fix check_bn_tests.go.
  * Fix MSan error in SSLTest.Handoff test.
  * SSLTest.Handoff: extend to include a session resumption.
  * inject_hash preserves filemode
  * Move TLS 1.3 state machine constants to internal.h.
  * Add a ppc64le ABI tester.
  * Allocate small TLS read buffers inline.
  * Remove unused labels from ARM ABI test assembly.
  * Update AAPCS and AAPCS64 links.
  * Fix EVP_has_aes_hardware on ppc64le.
  * Remove remnants of end_of_early_data alert from tests.
  * Add a test for ERR_error_string_n.
  * Remove post-quantum experiment signal extension.
  * Give ERR_error_string_n a return value for convenience.
  * Defer early keys to QUIC clients to after certificate reverification.
  * Defer releasing early secrets to QUIC servers.
  * Halve the size of the kNIDsIn* constants
  * modulewrapper: manage buffer with |unique_ptr|.
  * Add missing boringssl_prefix_symbols_asm.h include.
  * acvptool: add support for ECDSA
  * Inline gcm_init_4bit into gcm_init_ssse3.
  * Vectorize gcm_mul32_nohw and replace gcm_gmult_4bit_mmx.
  * Add a constant-time fallback GHASH implementation.
  * Conditionally define PTRACE_O_EXITKILL in urandom_test.cc
  * Fix build warning if _SCL_SECURE_NO_WARNINGS is defined globally
  * modulewrapper: use a raw string.
  * acvptool: add license headers.
  * Enable TLS 1.3 by default.
  * acvptool: Add support for DRBG
  * Discard user_canceled alerts in TLS 1.3.
  * Work around more C language bugs with empty spans.
  * No-op commit to test the new builder.
  * acvptool: Add support for HMAC
  * Add stub functions for RSA-PSS keygen parameters.
  * HelloRetryRequest getter
  * Add break-tests-android.sh script.
  * Add compatibility functions for sigalgs
  * Run AES-192-GCM in CAVP tests.
  * Rename a number of BUF_* functions to OPENSSL_*.
  * List bn_div fuzzer in documentation.
  * Reenable bn_div fuzzer.
  * Drop CECPQ2b code.
  * Add urandom_test to all_tests.json
  * Fix the standalone Android FIPS build.
  * Add sanity checks to FIPS module construction.
  * Correct relative path.
  * Add test for urandom.c
  * break-hash.go: Search ELF dynamic symbols if symbols not found.
  * Fix $OPENSSL_ia32cap handling.
  * Switch probable_prime to rejection sampling.
  * Rename the last remnants of the early_data_info extension.
  * Fix up BN_GENCB_call calls.
  * Do fewer trial divisions for larger RSA keygens.
  * Fix GRND_NONBLOCK flag when calling getrandom.
  * Simplify bn_miller_rabin_iteration slightly.
  * Add some notes on RSA key generation performance.
  * Break early on composites in the primality test.
  * Extract and test the deterministic part of Miller-Rabin.
  * Fix the FIPS + fuzzing build.
  * FIPS.md: document some recent Android changes.
  * Add a function to derive an EC key from some input secret.
  * Fix run_android_tests.go with shared library builds.
  * No-op change to test new builders.
  * Move no-exec-stack sections outside of #ifs.
  * Add |SSL_get_min_proto_version| and |SSL_get_max_proto_version|
  * Make FIPS build work for Android cross-compile.
  * Enable optional GRND_RANDOM flag to be passed to getrandom on Android.
  * Switch cert_compression_algs to GrowableArray.
  * Add GrowableArray<T> to ssl/internal.h.
  * Fixed quic_method lookup in TLS 1.3 server side handshake.
  * Add .note.GNU-stack at the source level.
  * -Wno-vla -> -Wvla
  * Add an option for explicit renegotiations.
  * tool: add -json flag to |speed|
  * Set -Wno-vla.
  * Use a pointer to module_hash in boringssl_fips_self_test() args.
  * Use a smaller hex digest in FIPS flag files when SHA-256 used.
  * Switch to using SHA-256 for FIPS integrity check on Android.
  * Use getentropy on macOS 10.12 and later.
  * Move #include of "internal.h", which defines |OPENSSL_URANDOM|.
  * Style nit.
  * Assert that BN_CTX_end is actually called.
  * Test some known large primes.
  * Test some Euler pseudoprimes.
  * Be consistent about Miller-Rabin vs Rabin-Miller.
  * fix build with armv6  Error: .size expression for _vpaes_decrypt_consts does not evaluate to a constant
  * Mark ssl_early_data_reason_t values stable.
  * Make the dispatch tests opt-in.
  * Bound the number of API calls in ssl_ctx_api.cc.
  * Only attempt to mprotect FIPS module for AArch64.
  * Opportunistically read entropy from the OS in FIPS mode.
  * Update INSTANTIATE_TEST_SUITE_P calls missing first argument.
  * Ignore build32 and build64 subdirectories.
  * Add page protection logic to BCM self test.
  * Disable unwind tests in FIPS mode.
  * Disable RDRAND on AMD family 0x17, models 0x70–0x7f.
  * Don't allow SGC EKUs for server certificates.
  * Add |SSL_CIPHER_get_value| to get the IANA number of a cipher suite.
  * Add XOF compilation compatibility flags
  * Replace BIO_printf with ASN1_STRING_print in GENERAL_NAME_print
  * Trigger a build on the ARM mode builder.
  * Fix vpaes-armv7.pl in ARM mode.
  * Add AES-192-GCM support to EVP_AEAD.
  * Add AES-256 CFB to libdecrepit.
  * Parse explicit EC curves more strictly.
  * Use the Go 1.13 standard library ed25519.
  * Update build tools.
  * Use ScopedEVP_AEAD_CTX in ImplDispatchTest.AEAD_AES_GCM.
  * Use a mix of bsaes and vpaes for CTR on NEON.
  * Use vpaes + conversion to setup CBC decrypt on NEON.
  * Add NEON vpaes-to-bsaes key converters.
  * Add vpaes-armv7.pl and replace non-parallel modes.
  * Correct comments for x86_64 _vpaes_encrypt_core_2x.
  * Add benchmarks for AES block operations.
  * Only write self test flag files if an environment variable is set.
  * Const-correct EC_KEY_set_public_key_affine_coordinates.
  * Revert "Fix VS build when assembler is enabled"
  * Support compilation via emscripten
  * Fix cross-compile of Android on Windows.
  * Move the config->async check into RetryAsync.
  * Clear *out in ReadHandshakeData's empty case.
  * Add initial support for 0-RTT with QUIC.
  * Have some more fun with spans.
  * Add OPENSSL_FALLTHROUGH to a few files.
  * Limit __attribute__ ((fallthrough)) to Clang >= 5.
  * Make |EVP_CIPHER_CTX_reset| return one.
  * Add Fallthru support for clang 10.
  * Add self-test suppression flag file for Android FIPS builds.
  * Align 0-RTT and resumption state machines slightly
  * Require getrandom in Android FIPS builds.
  * acvp: allow passing custom subprocess I/O.
  * Add a function to convert SSL_ERROR_* values to strings.
  * Fold SSL_want constants into SSL_get_error constants.
  * Use spans for the various TLS 1.3 secrets.
  * Switch another low-level function to spans.
  * Switch tls13_enc.cc to spans.
  * Check the second ClientHello's PSK binder on resumption.
  * Introduce libcrypto_bcm_sources for Android.
  * Remove stale TODO.
  * Add an android-cmake option to generate_build_files.py
  * Add a QUIC test for HelloRetryRequest.
  * Add missing ".text" to Windows code for dummy_chacha20_poly1305_asm
  * Update TODO to note that Clang git doesn't have the POWER bug.
  * Fix paths in break-tests.sh.
  * Fix POWER build with OPENSSL_NO_ASM.
  * Workaround Clang bug on POWER.
  * Add assembly support for -fsanitize=hwaddress tagged globals.
  * Fix typo in valgrind constant-time annotations.
  * acvp: add support for AES-ECB and AES-CBC.
  * Fix misspelled TODO.
  * Move CCM fragments out of the FIPS module.
  * Add EVP_PKEY_base_id.
  * Add some project links to README.md.
  * Make alert_dispatch into a bool.
  * Trim some more per-connection memory.
  * Remove SSL_export_early_keying_material.
  * Add EVP_PKEY support for X25519.
  * Make EVP_PKEY_bits return 253 for Ed25519.
  * Make SSL_get_servername work in the early callback.

* Tue Mar 10 2020 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Fix arm build:
  * 0005-fix-alignment-for-arm.patch

* Wed Dec  4 2019 Klaus Kämpf <kkaempf@suse.com>
- fix s390x and ppc64le build
  * 0003-enable-s390x-builds.patch
  * 0004-fix-alignment-for-ppc64le.patch
- rename add-soversion-option.patch
    to 0001-add-soversion-option.patch
- rename 0001-crypto-Fix-aead_test-build-on-aarch64.patch
    to 0002-crypto-Fix-aead_test-build-on-aarch64.patch

* Thu Oct 17 2019 Richard Brown <rbrown@suse.com>
- Remove obsolete Groups tag (fate#326485)

* Mon Oct 14 2019 Martin Pluskal <mpluskal@suse.com>
- Update to version 20190916:
  * Revert "Fix VS build when assembler is enabled"
  * Only bypass the signature verification itself in fuzzer mode.
  * Move the PQ-experiment signal to SSL_CTX.
  * Name cipher suite tests in runner by IETF names.
  * Align TLS 1.3 cipher suite names with OpenSSL.
  * Prefix all the SIKE symbols.
  * Rename SIKE's params.c.
  * Add post-quantum experiment signal extension.
  * Fix shim error message endings.
  * Add initial draft of ACVP tool.
  * Implements SIKE/p434
  * Add SipHash-2-4.
  * Remove android_tools checkout
  * Support key wrap with padding in CAVP.
  * Add android_sdk checkout
  * Move fipstools/ to util/fipstools/cavp
  * Factor out TLS cipher selection to ssl_choose_tls_cipher.
  * Emit empty signerInfos in PKCS#7 bundles.
  * Clarify language about default SSL_CTX session ticket key behavior.
  * Add an API to record use of delegated credential
  * Fix runner tests with Go 1.13.
  * Add a value barrier to constant-time selects.
  * Avoid leaking intermediate states in point doubling special case.
  * Split p224-64.c multiplication functions in three.
  * Add AES-KWP
  * Discuss the doubling case in windowed Booth representation.
  * Update build tools.
  * Set a minimum CMake version of 3.0.
  * Replace addc64,subc64,mul64 in SIKE Go code with functions from math/bits
  * Eliminate some superfluous conditions in SIKE Go code.
  * Fix various typos.
  * Fix name clash in test structures
  * bcm: don't forget to cleanup HMAC_CTX.
  * Handle fips_shared_support.c getting built in other builds.
  * Fix various mistakes in ec_GFp_nistp_recode_scalar_bits comment.
  * Fix filename in comment.
  * Split EC_METHOD.mul into two operations.
  * Split ec_point_mul_scalar into two operations.
  * Add FIPS shared mode.
  * delocate: add test for .file handling.
  * delocate: translate uleb128 and sleb128 directives
  * Integrate SIKE with TLS key exchange.
  * Convert ecdsa_p224_key.pem to PKCS#8.

* Wed Sep  4 2019 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Re-enable build on aarch64

* Tue Sep  3 2019 Martin Pluskal <mpluskal@suse.com>
- Update to version 20190523:
  * Disable RDRAND on AMD chips before Zen.
  * Always store early data tickets.
  * Align PKCS12_parse closer to OpenSSL.
  * Support PKCS#12 KeyBags.
  * Support PKCS#8 blobs using PBES2 with HMAC-SHA256.
  * Make EVP_PKEY_keygen work for Ed25519.
  * Sync aesp8-ppc.pl with upstream.
  * Update generate_build_files.py for SIKE.
  * Fix the last casts in third_party/sike.
  * Remove no-op casts around tt1.
  * Define p503 with crypto_word_t, not uint64_t.
  * Add support for SIKE/p503 post-quantum KEM
  * tool: fix speed tests.
  * Add an option to skip crypto_test_data.cc in GN too.
  * Save and restore errors when ignoring ssl_send_alert result.
  * Reject obviously invalid DSA parameters during signing.
  * Make expect/expected flag and variable names match.
  * clang-format Flag arrays in test_config.cc.
  * Rename remnants of ticket_early_data_info.
  * Enforce the ticket_age parameter for 0-RTT.
  * Add SSL_get_early_data_reason.
  * Remove implicit -on-resume for -expect-early-data-accept.
  * Use weak symbols only on supported platforms
  * Fix spelling in comments.
  * Add functions for "raw" EVP_PKEY serializations.
  * Remove stray underscores.
  * Add a compatibility EVP_DigestFinalXOF function.
  * Fix up EVP_DigestSign implementation for Ed25519.
  * Check for errors when setting up X509_STORE_CTX.
  * Convert a few more things from int to bool.
  * Compute the delegated credentials length prefix with CBB.
  * Convert the rest of ssl_test to GTest.
  * Check for x18 usage in aarch64 assembly.
  * Handle errors from close in perlasm scripts.
  * Hold off flushing NewSessionTicket until write.
  * Predeclare enums in base.h
  * Require certificates under name constraints use SANs.
  * Make X509_verify_cert_error_string thread-safe.
  * Disable the common name fallback on *any* SAN list.
  * Silently ignore X509_CHECK_FLAG_ALWAYS_CHECK_SUBJECT.
  * Add X509_CHECK_FLAG_NEVER_CHECK_SUBJECT.
  * Give ENGINE_free a return value.
  * Output a ClientHello during handoff.
  * Fix and test EVP_PKEY_CTX copying.
  * Test copying an EVP_MD_CTX.
  * Fix EVP_CIPHER_CTX_copy for AES-GCM.
  * Check key sizes in AES_set_*_key.
  * Add missing nonce_len check to aead_aes_gcm_siv_asm_open.
  * Test AES-GCM-SIV with OPENSSL_SMALL.
  * Handle CBB_cleanup on child CBBs more gracefully.
  * Update third_party/googletest.
  * Rename 'md' output parameter to 'out' and add bounds.
  * Update other build tools.
  * Update SDE to 8.35.0-2019-03-11.
  * nit: Update references to draft-ietf-tls-subcerts.
  * Support get versions with get_{min,max}_proto_version for context
  * Update ImplDispatchTest for bsaes-x86_64 removal.
  * Unwind the large_inputs hint in aes_ctr_set_key.
  * Add an optimized x86_64 vpaes ctr128_f and remove bsaes.
  * Add 16384 to the default bssl speed sizes.
  * Rewrite BN_CTX.
  * Save a temporary in BN_mod_exp_mont's w=1 case.
  * Reject long inputs in c2i_ASN1_INTEGER.
  * Harden the lower level parts of crypto/asn1 against overflows.
  * Remove d2i_ASN1_UINTEGER.
  * Drop some unused bsaes to aes_nohw dependencies.
  * Adapt gcm_*_neon to aarch64.
  * Patch out the aes_nohw fallback in bsaes_cbc_encrypt.
  * Patch out the aes_nohw fallback in bsaes_ctr32_encrypt_blocks.
  * Implement sk_find manually.
  * Make vpaes-armv8.pl compatible with XOM.
  * Support three-argument instructions on x86-64.
  * Correct outdated comments
  * Remove SSL_get_structure_sizes.
  * Prefer vpaes over bsaes in AES-GCM-SIV and AES-CCM.
  * Tell ASan about the OPENSSL_malloc prefix.
  * modes/asm/ghash-armv4.pl: address "infixes are deprecated" warnings.
  * Enable vpaes for aarch64, with CTR optimizations.
  * Check in vpaes-armv8.pl from OpenSSL unused and unmodified.
  * silence unused variable warnings when using OPENSSL_clear_free
  * Handle NULL public key in |EC_KEY_set_public_key|.
  * Add a 32-bit SSSE3 GHASH implementation.
  * Also include abi_test.cc in ssl_test_files.
  * Don't pull abi_test.cc into non-GTest targets.
  * Update *_set_cert_cb documentation regarding resumption
  * Add a reference for Linux ARM ABI.
  * Remove __ARM_ARCH__ guard on gcm_*_v8.
  * Fix bsaes-armv7.pl getting disabled by accident.
  * Add an option to configure bssl speed chunk size.
  * Appease GCC's uninitialized value warning.
  * Set VPAES flags in x86-64 code.
  * Enable vpaes for AES_* functions.
  * Avoid double-dispatch with AES_* vs aes_nohw_*.
  * Add uint64_t support in CBS and CBB.
  * Clear out a bunch of -Wextra-semi warnings.
  * Add compiled python files to .gitignore.
  * Fix x86_64-xlate.pl comment regex.
  * Add go 1.11 to go.mod.
  * Remove STRICT_ALIGNMENT code from modes.
  * Remove non-STRICT_ALIGNMENT code from xts.c.
  * Patch XTS out of ARMv7 bsaes too.
  * Remove stray prototype.
  * Always define GHASH.
  * Update delegated credentials to draft-03
  * Use Windows symbol APIs in the unwind tester.
  * Unwind RDRAND functions correctly on Windows.
  * Patch out unused aesni-x86_64 functions.
  * Add ABI tests for aesni-gcm-x86_64.pl.
  * Add ABI tests for x86_64-mont5.pl.
  * sync EVP_get_cipherbyname with EVP_do_all_sorted
  * Hyperlink DOI to preferred resolver
  * Remove stray semicolons.
  * Remove separate default group list for servers.
  * Enable all curves (inc CECPQ2) during fuzzing.
  * Implement ABI testing for aarch64.
  * Fix ABI error in bn_mul_mont on aarch64.
  * Implement ABI testing for ARM.
  * Fix the order of Windows unwind codes.
  * Implement unwind testing for Windows.
  * Tolerate spaces when parsing .type directives.
  * runner: Don't generate an RSA key on startup.
  * Don't use bsaes over vpaes for CTR-DRBG.
  * perlasm/x86_64-xlate.pl: refine symbol recognition in .xdata.
  * Add instructions for debugging on Android with gdb.
  * Enforce key usage for RSA keys in TLS 1.2.
  * Remove infra/config folder in master branch.
  * Avoid SCT/OCSP extensions in SH on {Omit|Empty}Extensions
  * Test and fix an ABI issue with small parameters.
  * Add RSAZ ABI tests.
  * Better document RSAZ and tidy up types.
  * Add ABI testing for 32-bit x86.
  * Add a very roundabout EC keygen API.
  * Add some Node compatibility functions.
  * Implement server support for delegated credentials.
  * Add a constant-time pshufb-based GHASH implementation.
  * Tweak some slightly fragile tests.
  * Make 256-bit ciphers a preference for CECPQ2, not a requirement.
  * Update comments around JDK11 workaround.
  * Add a RelWithAsserts build configuration.
  * Remove union from |SHA512_CTX|.
  * Avoid unwind tests on libc functions.
  * Don't pass NULL,0 to qsort.
  * Fix signed left-shifts in curve25519.c.
  * Add an option to build with UBSan.
  * Fix undefined pointer casts in SHA-512 code.
  * HRSS: flatten sample distribution.
  * Add test of assembly code dispatch.
  * Simplify HRSS mod3 circuits.
  * Add SSL_OP_NO_RENEGOTIATION
  * Rename Fiat include files to end in .h
  * Switch to new fiat pipeline.
  * Don't look for libunwind if cross-compiling.
  * Mark some unmarked array sizes in curve25519.c.
  * Revert "Fix protos_len size in SSL_set_alpn_protos and SSL_CTX_set_alpn_protos"
  * Add ABI tests for GCM.
  * Fix SSL_R_TOO_MUCH_READ_EARLY_DATA.
  * Test CRYPTO_gcm128_tag in gcm_test.cc.
  * Remove pointer cast in P-256 table.
  * Ignore new fields in forthcoming Wycheproof tests.
  * Fix RSAZ's OPENSSL_cleanse.
  * Allow configuring QUIC method per-connection
  * Fix header file for _byteswap_ulong and _byteswap_uint64 from MSVC CRT
  * Add ABI tests for HRSS assembly.
  * Add AES ABI tests.
  * Move aes_nohw, bsaes, and vpaes prototypes to aes/internal.h.
  * Add direction flag checking to CHECK_ABI.
  * Add ABI tests for ChaCha20_ctr32.
  * Add ABI tests for MD5.
  * Refresh fuzzer corpus.
  * Delete the variants/draft code.
  * Update tools.
  * Fix protos_len size in SSL_set_alpn_protos and SSL_CTX_set_alpn_protos
  * Use handshake parameters to decide if cert/key are available
  * Add ABI tests for bn_mul_mont.
  * Add ABI tests for SHA*.
  * Make pkg-config optional.
  * Add DEPS rules to checkout Windows SDE.
  * Add ABI tests for rdrand.
  * Set NIDs for Blowfish and CAST.
  * Add a CFI tester to CHECK_ABI.
  * Fix some size_t to long casts.
  * Add EVP_CIPHER support for Blowfish and CAST to decrepit.
  * Be less clever with CHECK_ABI.
  * Update SDE and add the Windows version.
  * Remove pooling of PRNG state.
  * Add EC_KEY_key2buf for OpenSSL compatibility
  * Remove bundled copy of android-cmake.
  * Clarify build requirements.
  * Add EC_GROUP_order_bits for OpenSSL compatibility
  * Annotate leaf functions with .cfi_{startproc,endproc}
  * Fix beeu_mod_inverse_vartime CFI annotations and preamble.
  * Fix CFI annotations in p256-x86_64-asm.pl.
  * Add a comment about ecp_nistz256_point_add_affine's limitations.
  * Refresh p256-x86_64_tests.txt.
  * Fix some indentation nits.
- Build using ninja
- Update dependencies
- Bump soversion
- Limit building only to supported architectures

* Fri Aug 30 2019 Martin Pluskal <mpluskal@suse.com>
- Disable lto to fix build failure

* Thu Apr 25 2019 Michał Rostecki <mrostecki@opensuse.org>
- Add patch which fixes build on aarch64.
  * 0001-crypto-Fix-aead_test-build-on-aarch64.patch

* Thu Apr 25 2019 dmueller@suse.com
- Update to version 20181228:
  * Use thread-local storage for PRNG states if fork-unsafe buffering is enabled.
  * Add Win64 SEH unwind codes for the ABI test trampoline.
  * Translate .L directives inside .byte too.
  * Add an ABI testing framework.
  * Use same HKDF label as TLS 1.3 for QUIC as per draft-ietf-quic-tls-17
  * Add |SSL_key_update|.
  * HRSS: omit reconstruction of ciphertext.
  * Add start of infrastructure for checking constant-time properties.
  * Don't enable intrinsics on x86 without ABI support.
  * HRSS: be strict about unused bits being zero.
  * Disable AES-GCM-SIV assembly on Windows.
  * Fix typo in AES-GCM-SIV comments.
  * Fix HRSS build error on ARM
  * Fix thread-safety bug in SSL_get_peer_cert_chain.
  * Remove HRSS confirmation hash.
  * Drop NEON assembly for HRSS.
  * Add |SSL_export_traffic_secrets|.
  * Patch out the XTS implementation in bsaes.
  * Remove .file and .loc directives from HRSS ARM asm.
  * Do not allow AES_128_GCM_SHA256 with CECPQ2.
  * Always 16-byte align |poly| elements.
  * Fix bug in HRSS tests.
  * Add initial HRSS support.
  * Forbid empty CertificateRequestsupported_signature_algorithms in TLS 1.2.
  * Eliminate |OPENSSL_ia32cap_P| in C code in the FIPS module.
  * Fix d2i_*_bio on partial reads.
  * Fix |BN_HEX_FMT2|.
  * Remove XOP code from sha512-x86_64.pl.
  * Pretend AMD XOP was never a thing.
  * Drop some explicit SSLKeyShare destructors.
  * Assume hyper-threading-like vulnerabilities are always present.
  * Replace the last CRITICAL_SECTION with SRWLOCK.
  * Validate ClientHellos in tests some more.
  * Re-enable AES-NI on 32-bit x86 too.
  * Make symbol-prefixing work on 32-bit x86.
  * Make Windows symbol-prefixing work.
  * Support Windows-style ar files.
  * Move __.SYMDEF handling to ar.go.
  * Fix stack_test.cc in the prefixed build.
  * Don't double-mangle C++ symbols on macOS.
  * Make read_symbols.go a bit more idiomatic.
  * Unexport and rename hex_to_string, string_to_hex, and name_cmp.
  * Satisfy golint.
  * Add a note that generated files are generated.
  * Work around a JDK 11 TLS 1.3 bug.
  * Move ARM cpuinfo functions to the header.
  * Regenerate obj_dat.h
  * go fmt
  * Support execute-only memory for AArch64 assembly.
  * Remove cacheline striping in copy_from_prebuf.
  * Tidy up type signature of BN_mod_exp_mont_consttime table.
  * No longer set CQ-Verified label on CQ success/failure.
  * Print a message when simulating CPUs.
  * Move JSON test results code into a common module.
  * In 0RTT mode, reverify the server certificate before sending early data.
  * Support assembly building for arm64e architecture.
  * Simulate other ARM CPUs when running tests.
  * Merge P-224 contract into serialisation.
  * Contract P-224 elements before returning them.
  * Add post-handshake support for the QUIC API.
  * Speculatively remove __STDC_*_MACROS.
  * Modernize OPENSSL_COMPILE_ASSERT, part 2.
  * Switch docs to recommending NASM.
  * Mark the |e| argument to |RSA_generate_key_ex| as const.
  * Clean up EC_POINT to byte conversions.
  * Need cpu.h for |OPENSSL_ia32cap_P|.
  * Rename EC_MAX_SCALAR_*.
  * Use EC_RAW_POINT in ECDSA.
  * Optimize EC_GFp_mont_method's cmp_x_coordinate.
  * Optimize EC_GFp_nistp256_method's cmp_x_coordinate.
  * Remove unreachable code.
  * Also accept __ARM_NEON
  * Remove some easy BN_CTXs.
  * Push BIGNUM out of the cmp_x_coordinate interface.
  * Push BIGNUM out of EC_METHOD's affine coordinates hook.
  * Fix r = p-n+epsilon ECDSA tests.
  * Don't include openssl/ec_key.h under extern "C".
  * Abstract hs_buf a little.
  * Inline ec_GFp_simple_group_get_degree.
  * Better test boundary cases of ec_cmp_x_coordinate.
  * Fix build when bcm.c is split up.
  * Revert "Revert "Speed up ECDSA verify on x86-64.""
  * Make SSL_get_current_cipher valid during QUIC callbacks.
  * Devirtualize ec_simple_{add,dbl}.
  * Refresh fuzzer corpora for changes to split-handshake serialization.
  * Serialize SSL curve list in handoff and check it on application.
  * Revert "Speed up ECDSA verify on x86-64."
  * Route the tuned add/dbl implementations out of EC_METHOD.
  * Speed up ECDSA verify on x86-64.
  * Include details about latest FIPS certification.
  * Serialize SSL configuration in handoff and check it on application.
  * Don't overflow state->calls on 16TiB RAND_bytes calls.
  * Buffer up QUIC data within a level internally.
  * Add an interface for QUIC integration.
  * Remove OPENSSL_NO_THREADS.
  * Minor fixes to bytestring.h header.
  * Test CBC padding more aggressively.
  * Restore CHECKED_CAST.
  * Fix EVP_tls_cbc_digest_record is slow using SHA-384 and short messages
  * Tidy up dsa_sign_setup.
  * Fix the build on glibc 2.15.
  * Modernize OPENSSL_COMPILE_ASSERT.
  * Fix redefinition of AEAD asserts in e_aes.c.
  * Guard sys/auxv.h include on !BORINGSSL_ANDROID.
  * Flatten EVP_AEAD_CTX
  * Implement SSL_get_tlsext_status_type
  * Fix documentation sectioning.
  * Remove support for GCC 4.7.
  * Print the name of the binary when blocking in getrandom.
  * Undo recent changes to |X509V3_EXT_conf_nid|.
  * Add a compatibility EVP_CIPH_OCB_MODE value.
  * [util] Mark srtp.h as an SSL header file
  * [rand] Disable RandTest.Fork on Fuchsia
  * Remove -fsanitize-cfi-icall-generalize-pointers.
  * Fix undefined function pointer casts in LHASH.
  * Use proper functions for lh_*.
  * Better handle AVX-512 assembly syntax.
  * Always push errors on BIO_read_asn1 failure.
  * Add a per-SSL TLS 1.3 downgrade enforcement option and improve tests.
  * Fix div.c to divide BN_ULLONG only if BN_CAN_DIVIDE_ULLONG defined.
  * Include aes.h in mode/internal.h
  * Fix section header capitalization.
  * Fix build in consumers that flag unused parameters.
  * [perlasm] Hide OPENSSL_armcap_P in assembly
  * Test the binary search more aggressively.
  * Opaquify CONF.
  * Bring Mac and iOS builders back to the CQ.
  * Remove LHASH_OF mention in X509V3_EXT_conf_nid.
  * Inline functions are apparently really complicated.
  * Actually disable RandTest.Fork on iOS.
  * Mostly fix undefined casts around STACK_OF's comparator.
  * Fix undefined casts in sk_*_pop_free and sk_*_deep_copy.
  * Take iOS builders out of the CQ rotation too.
  * Rewrite PEM_X509_INFO_read_bio.
  * Fix undefined block128_f, etc., casts.
  * Fix undefined function pointer casts in {d2i,i2d}_Foo_{bio,fp}
  * Fix undefined function pointer casts in IMPLEMENT_PEM_*.
  * Always print some diagnostic information when POST fails.
  * Disable RandTest.Fork on iOS.
  * Const-correct sk_find and sk_delete_ptr.
  * Add a test for STACK_OF(T).
  * Rename inject-hash: Bazel does not like hyphens.
  * Rename OPENSSL_NO_THREADS, part 1.
  * Fix ERR_GET_REASON checks.
  * Add a basic test for PEM_X509_INFO_read_bio.
  * Replace BIO_new + BIO_set_fp with BIO_new_fp.
  * Remove Mac try jobs from the CQ.
  * Add util/read_symbols.go
  * Tighten up getrandom handling.
  * Remove SHA384_Transform from sha.h.
  * Push an error on sigalg mismatch in X509_verify.
  * Sync bundled bits of golang.org/x/crypto.
  * Use Go modules with delocate.
  * Keep the GCM bits in one place.
  * Trim 88 bytes from each AES-GCM EVP_AEAD.
  * Set up Go modules.
  * Use sdallocx, if available, when deallocating.
  * Remove the add_alert hook.
  * Fix doc.go error capitalization.
  * Don't include quotes in heredocs.
  * Add missing bssl::UpRef overloads.
  * Roll back clang revision.
  * Update tools.
  * Fix BORINGSSL_NO_CXX.
  * Fix check of the pointer returned by BN_CTX_get
  * Include newlines at the end of generated asm.
  * Automatically disable assembly with MSAN.
  * Mark the C version of md5_block_data_order static.
  * Reorder some extensions to better match Firefox.
  * Make symbol-prefixing work on ARM.
  * Document alternative functions to BIO_f_base64.
  * Another batch of bools.
  * Add some RAND_bytes tests.
  * Support symbol prefixes
  * Fill in a fake session ID for TLS 1.3.
  * Create output directories for perlasm.
  * Fix Fiat path.
  * Fix GCC (8.2.1) build error.
  * Some more bools.
  * Flatten most of the crypto target.
  * Flatten assembly files.
  * Flatten the decrepit target.
  * Clarify "reference" and fix typo.
  * Fix corner case in cpuinfo parser.
  * Add some about ownership to API-CONVENTIONS.
  * Tidy up docs for #defines.
  * No negative moduli.
  * Document that ED25519_sign only fails on allocation failure
  * Clarify thread-safety of key objects.
  * shim: don't clear environment when invoking handshaker.
  * Switch the default TLS 1.3 variant to tls13_rfc.
  * Switch to Clang 6.0's fuzzer support.

* Tue Dec 11 2018 Jan Engelhardt <jengelh@inai.de>
- Trim redundant wording. Use multi-file find -exec invocation.

* Fri Nov 16 2018 Michał Rostecki <mrostecki@suse.de>
- To avoid conflicts with openssl development files, change all
  includes from openssl to boringssl.

* Fri Nov  9 2018 Martin Pluskal <mpluskal@suse.com>
- Use optflags when building
- Do not create empty package

* Thu Nov  8 2018 Michał Rostecki <mrostecki@suse.de>
- Update to version 20181026:
  * Automatically disable assembly with MSAN.
  * Switch the default TLS 1.3 variant to tls13_rfc.

* Wed Nov  7 2018 Michał Rostecki <mrostecki@suse.de>
- Update to version 20181106:
  * Make SSL_get_current_cipher valid during QUIC callbacks.
  * Devirtualize ec_simple_{add,dbl}.
  * Refresh fuzzer corpora for changes to split-handshake serialization.
  * Serialize SSL curve list in handoff and check it on application.
  * Revert "Speed up ECDSA verify on x86-64."
  * Route the tuned add/dbl implementations out of EC_METHOD.
  * Speed up ECDSA verify on x86-64.
  * Include details about latest FIPS certification.
  * Serialize SSL configuration in handoff and check it on application.
  * Don't overflow state->calls on 16TiB RAND_bytes calls.
- Use tar_scm service for fetching sources and versioning.

* Wed Nov  7 2018 Michał Rostecki <mrostecki@suse.de>
- Initial release - 0.0.0+git7499.6ec9e4
- Add add-soversion-option.patch - required to build libraries with
  soversion
