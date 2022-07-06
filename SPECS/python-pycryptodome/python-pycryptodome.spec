#
# spec file for package python-pycryptodome
#
# Copyright (c) 2022 SUSE LLC
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

%{?!python_module:%define python_module() python-%{**} python3-%{**}}
%define oldpython python
Name:           python-pycryptodome
Version:        3.14.1
Release:        3
Summary:        Cryptographic library for Python
License:        BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://www.pycryptodome.org
Source:         https://github.com/Legrandin/pycryptodome/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  fdupes
BuildRequires:  python-rpm-macros
%if !0%{?_no_weakdeps}
# PyCryptodome uses gmp via cffi as runtime optimization
# would be better, if libgmp* would provide gmp
Suggests:       libgmp10
Suggests:       python-cffi
%endif
Provides:       python-pycrypto = %{version}
Obsoletes:      python-pycrypto < %{version}

%description
PyCryptodome is a self-contained Python package of low-level
cryptographic primitives.

PyCryptodome is a fork of PyCrypto, residing in the `Crypto`
namespace for better drop-in compatibility, while it brings several
enhancements with respect to the last official version of PyCrypto
(2.6.1), for instance:

* Authenticated encryption modes (GCM, CCM, EAX, SIV, OCB)
* Accelerated AES on Intel platforms via AES-NI
* First class support for PyPy
* Elliptic curves cryptography (NIST P-256 curve only)
* Better and more compact API (`nonce` and `iv` attributes for
  ciphers, automatic generation of random nonces and IVs, simplified
  CTR cipher mode, and more)
* SHA-3 (including SHAKE XOFs), SHA-512/t and BLAKE2 hash algorithms
* Salsa20 and ChaCha20 stream ciphers
* Poly1305 MAC
* ChaCha20-Poly1305 authenticated cipher
* scrypt and HKDF
* Deterministic (EC)DSA
* Password-protected PKCS#8 key containers
* Shamir's Secret Sharing scheme
* Random numbers get sourced directly from the OS (and not from a
  CSPRNG in userspace)
* Simplified install process, including better support for Windows
* Cleaner RSA and DSA key generation (largely based on FIPS 186-4)
* Major clean ups and simplification of the code base

PyCryptodome is not a wrapper to a separate C library like *OpenSSL*.
To the largest possible extent, algorithms are implemented in pure
Python. Only the pieces that are extremely critical to performance
(e.g. block ciphers) are implemented as C extensions.

%prep
%autosetup -n pycryptodome-%{version}

%build
export LC_ALL=en_US.UTF-8
export CFLAGS="%{optflags}"
%py3_build

%install
export LC_ALL=en_US.UTF-8
%py3_install
%fdupes %{buildroot}%{$python3_sitearch}

%check
export LC_ALL=en_US.UTF-8
%{pushd %{buildroot}%{python3_sitearch}
PYTHONPATH=%{buildroot}%{python3_sitearch} $python -m Crypto.SelfTest
popd}

%files
%license LICENSE.rst
%doc AUTHORS.rst Changelog.rst README.rst
%{python3_sitearch}/Crypto/
%{python3_sitearch}/pycryptodome-%{version}-py*.egg-info

%changelog
* Thu Jun 23 2022 Sumedh Sharma <sumsharma@microsoft.com> - 3.14.1-3
- Initial CBL-Mariner import from OpenSuse Tumbleweed (License: BSD-2-Clause)
- Adding as run dependency for package cassandra medusa
- License Verified
* Wed Mar  9 2022 pgajdos@suse.com
- do not use setup.py test construct
  https://trello.com/c/me9Z4sIv/121-setuppy-test-leftovers
* Tue Feb 15 2022 Dirk Müller <dmueller@suse.com>
- update to 3.14.1:
  * GH#595: Fixed memory leak for GMP integers.
  * Add support for curve NIST P-192.
  * Add support for curve NIST P-224.
  * GH#590: Fixed typing info for ``Crypto.PublicKey.ECC``.
  * Relaxed ECDSA requirements for FIPS 186 signatures and accept any SHA-2 or
  * SHA-3 hash.  ``sign()`` and ``verify()`` will be performed even if the hash is stronger
    than the ECC key.
* Sat Dec 11 2021 Dirk Müller <dmueller@suse.com>
- update to 3.12.0:
  * ECC keys in the SEC1 format can be exported and imported.
  * Add support for KMAC128, KMAC256, TupleHash128, and TupleHash256 (NIST SP-800 185).
  * Add support for KangarooTwelve.
  * GH#563: An asymmetric key could not be imported as a ``memoryview``.
  * GH#566: cSHAKE128/256 generated a wrong output for customization strings
  * GH#582: CBC decryption generated the wrong plaintext when the input and the output were the same buffer.
* Sat Oct 16 2021 Dirk Müller <dmueller@suse.com>
- update to 3.11.0:
  * GH#512: Especially for very small bit sizes, ``Crypto.Util.number.getPrime()`` was
    occasionally generating primes larger than given the bit size.
  * GH#552: Correct typing annotations for ``PKCS115_Cipher.decrypt()``.
  * GH#555: ``decrypt()`` method of a PKCS#1v1.5 cipher returned a ``bytearray`` instead of ``bytes``.
  * GH#557: External DSA domain parameters were accepted even when the modulus (``p``) was not prime.
    This affected ``Crypto.PublicKey.DSA.generate()`` and ``Crypto.PublicKey.DSA.construct()``.
  * Added cSHAKE128 and cSHAKE256 (of SHA-3 family).
  * GH#558: The flag RTLD_DEEPBIND passed to ``dlopen()`` is not well supported by
    `address sanitizers <https://github.com/google/sanitizers/issues/611>`_.
    It is now possible to set the environment variable ``PYCRYPTDOME_DISABLE_DEEPBIND``
    to drop that flag and allow security testing.
* Thu Mar  4 2021 Dirk Müller <dmueller@suse.com>
- update to 3.10.1:
  * Fixed a potential memory leak when initializing block ciphers.
  * GH#466: ``Crypto.Math.miller_rabin_test()`` was still using the system random
    source and not the one provided as parameter.
  * GH#469: RSA objects have the method ``public_key()`` like ECC objects.
    The old method ``publickey()`` is still available for backward compatibility.
  * GH#476: ``Crypto.Util.Padding.unpad()`` was raising an incorrect exception
    in case of zero-length inputs. Thanks to Captainowie.
  * GH#491: better exception message when ``Counter.new()`` is called with an integer
    ``initial_value`` than doesn't fit into ``nbits`` bits.
  * GH#496: added missing ``block_size`` member for ECB cipher objects. Thanks to willem.
  * GH#500: ``nonce`` member of an XChaCha20 cipher object was not matching the original nonce.
* Tue Dec  1 2020 Hans-Peter Jansen <hpj@urpla.net>
- update to 3.9.9:
  * GH#435: Fixed Crypto.Util.number.size for negative numbers
* Tue Aug  4 2020 Dirk Mueller <dmueller@suse.com>
- update to 3.9.8:
  * GH#426: The Shamir's secret sharing implementation is not actually compatible with ``ssss``.
  Added an optional parameter to enable interoperability.
  * GH#427: Skip altogether loading of ``gmp.dll`` on Windows.
  * GH#420: Fix incorrect CFB decryption when the input and the output are the same buffer.
  * Speed up Shamir's secret sharing routines. Thanks to ncarve.
* Thu Mar 19 2020 Marketa Calabkova <mcalabkova@suse.com>
- Update to 3.9.7
  * Align stack of functions using SSE2 intrinsics to avoid crashes,
    when compiled with gcc on 32-bit x86 platforms.
  * Prevent key_to_english from creating invalid data when fed with
    keys of length not multiple of 8.
  * Fix blocking RSA signing/decryption when key has very small factor.
  * fixed memory leak for operations that use memoryviews when cffi
    is not installed.
  * RSA OAEP decryption was not verifying that all PS bytes are zero.
  * Fixed wrong ASN.1 OID for HMAC-SHA512 in PBE2.
* Sun Nov 10 2019 Hans-Peter Jansen <hpj@urpla.net>
- Update to 3.9.2 (10 November 2019):
  + New features
  * Add Python 3.8 wheels for Mac.
  + Resolved issues
  * GH#308: Avoid allocating arrays of __m128i on the stack, to
    cope with buggy compilers.
  * GH#322: Remove blanket -O3 optimization for gcc and clang, to
    cope with buggy compilers.
  * GH#337: Fix typing stubs for signatures.
  * GH#338: Deal with gcc installations that don't have
    x86intrin.h.
- Update to version 3.9.1 (1 November 2019):
  + New features
  * Add Python 3.8 wheels for Linux and Windows.
  + Resolved issues
  * GH#328: minor speed-up when importing RSA.
- Add export LC_ALL=en_US.UTF-8 to %%build, %%install and %%check to
  fix the build on older distros
  (as done from Thomas Bechtold in python-pycryptodomex)
* Tue Sep 10 2019 Tomáš Chvátal <tchvatal@suse.com>
- Update to 3.9.0:
  * Add support for loading PEM files encrypted with AES256-CBC.
  * Add support for XChaCha20 and XChaCha20-Poly1305 ciphers.
  * Add support for bcrypt key derivation function (Crypto.Protocol.KDF.bcrypt).
  * Add support for left multiplication of an EC point by a scalar.
  * Add support for importing ECC and RSA keys in the new OpenSSH format.
* Thu May 30 2019 Martin Liška <mliska@suse.cz>
- Update Source to point to github.
* Thu May 30 2019 Martin Liška <mliska@suse.cz>
- Update to 3.8.2
  * GH#291: fix strict aliasing problem, emerged with GCC 9.1.
* Fri May 24 2019 Martin Liška <mliska@suse.cz>
-  Use -fno-strict-aliasing in order to bypass:
  https://github.com/Legrandin/pycryptodome/issues/291.
* Tue May 14 2019 Marketa Calabkova <mcalabkova@suse.com>
- Update to 3.8.1
  * Add support for loading PEM files encrypted with AES192-CBC,
    AES256-CBC, and AES256-GCM.
  * When importing ECC keys, ignore EC PARAMS section that was
    included by some openssl commands.
  * repr() did not work for ECC.EccKey.
  * Minimal length for Blowfish cipher is 32 bits, not 40 bits.
  3.8.0
  * Speed-up ECC performance. ECDSA is 33 times faster on the
    NIST P-256 curve.
  * Added support for NIST P-384 and P-521 curves.
  * EccKey has new methods size_in_bits() and size_in_bytes().
  * Support HMAC-SHA224, HMAC-SHA256, HMAC-SHA384, and HMAC-SHA512
    in PBE2/PBKDF2.
  * DER objects were not rejected if their length field had
    a leading zero.
  * Allow legacy RC2 ciphers to have 40-bit keys.
  * point_at_infinity() becomes an instance method for
    Crypto.PublicKey.ECC.EccKey, from a static one.
  3.7.3
  * GH#258: False positive on PSS signatures when externally
    provided salt is too long.
* Wed Jan  9 2019 Jonathan Brownell <jbrownell@suse.com>
- Protect older platforms from encountering "Suggests:" keyword
* Sun Jan  6 2019 Hans-Peter Jansen <hpj@urpla.net>
- fix tarball: use the one from PyPI...
* Thu Nov 29 2018 Hans-Peter Jansen <hpj@urpla.net>
- Update to 3.7.2
  - Resolved issues
  * GH#242: Fixed compilation problem on ARM platforms.
- Update to 3.7.1
  - New features
  * Added type stubs to enable static type checking with mypy.
    Thanks to Michael Nix.
  * New ``update_after_digest`` flag for CMAC.
  - Resolved issues
  * GH#232: Fixed problem with gcc 4.x when compiling
    ``ghash_clmul.c``.
  * GH#238: Incorrect digest value produced by CMAC after cloning
    the object.
  * Method ``update()`` of an EAX cipher object was returning the
    underlying CMAC object, instead of the EAX object itself.
  * Method ``update()`` of a CMAC object was not throwing an
    exception after the digest was computed (with ``digest()`` or
    ``verify()``).
* Thu Nov 29 2018 Hans-Peter Jansen <hpj@urpla.net>
- checked in python-pycrytodomex as separate package on request of
  Dirk Müller
* Sun Nov 25 2018 Hans-Peter Jansen <hpj@urpla.net>
- fixed source url
* Thu Nov  1 2018 Hans-Peter Jansen <hpj@urpla.net>
- Update to 3.7.0
  - New features
  * Added support for Poly1305 MAC (with AES and ChaCha20 ciphers
    for key derivation).
  * Added support for ChaCha20-Poly1305 AEAD cipher.
  * New parameter output for Crypto.Util.strxor.strxor,
    Crypto.Util.strxor.strxor_c, encrypt and decrypt methods in
    symmetric ciphers (Crypto.Cipher package). output is a
    pre-allocated buffer (a bytearray or a writeable memoryview)
    where the result must be stored. This requires less memory for
    very large payloads; it is also more efficient when encrypting
    (or decrypting) several small payloads.
  - Resolved issues
  * GH#266: AES-GCM hangs when processing more than 4GB at a time
    on x86 with PCLMULQDQ instruction.
  - Breaks in compatibility
  * Drop support for Python 3.3.
  * Remove Crypto.Util.py3compat.unhexlify and
    Crypto.Util.py3compat.hexlify.
  * With the old Python 2.6, use only ctypes (and not cffi) to
    interface to native code.
- Clean up spec
- pycryptodomex package spec added
* Fri Oct 19 2018 Dirk Mueller <dmueller@suse.com>
- remove pycryptodomex copy in this package container
* Mon Sep  3 2018 Marketa Calabkova <mcalabkova@suse.com>
- Update to 3.6.6
  - Resolved issues:
  * Fix vulnerability on AESNI ECB with payloads smaller than
    16 bytes.
- Update to 3.5.5
  - Resolved issues
  * Fixed incorrect AES encryption/decryption with AES
    acceleration on x86 due to gcc’s optimization and strict
    aliasing rules.
  * More prime number candidates than necessary where discarded
    as composite due to the limited way D values were searched
    in the Lucas test.
  * Fixed ResouceWarnings and DeprecationWarnings.
- Update to 3.5.4
  - New features:
  * Build Python 3.7 wheels on Linux, Windows and Mac.
  - Resolved issues:
  * More meaningful exceptions in case of mismatch in IV length
    (CBC/OFB/CFB modes).
* Tue Jul  3 2018 hpj@urpla.net
- Update to 3.6.3 (21 June 2018)
  - Resolved issues
  * GH#175: Fixed incorrect results for CTR encryption/decryption
    with more than 8 blocks.
- Update to 3.6.2 (19 June 2018)
  - New features
  * ChaCha20 accepts 96 bit nonces (in addition to 64 bit nonces)
    as defined in RFC7539.
  * Accelerate AES-GCM on x86 using PCLMULQDQ instruction.
  * Accelerate AES-ECB and AES-CTR on x86 by pipelining AESNI
    instructions.
  * As result of the two improvements above, on x86 (Broadwell):
  - AES-ECB and AES-CTR are 3x faster
  - AES-GCM is 9x faster
  - Resolved issues
  * On Windows, MPIR library was stilled pulled in if renamed to
    ``gmp.dll``.
  - Breaks in compatibility
  * In ``Crypto.Util.number``, functions ``floor_div`` and
    ``exact_div`` have been removed. Also, ``ceil_div`` is limited
    to non-negative terms only.
- suggesting libgmp10 and python-cffi
- add license file tag
* Wed May 16 2018 tchvatal@suse.com
- Provide/obsolete also python-crypto for py2 package
* Mon May  7 2018 hpj@urpla.net
- fix condition to act as drop in replacement for python-pycrypto
* Fri May  4 2018 hpj@urpla.net
- Update to 3.6.1 (15 April 2018)
  - New features
  * Added Google Wycheproof tests (https://github.com/google/wycheproof)
    for RSA, DSA, ECDSA, GCM, SIV, EAX, CMAC.
  * New parameter ``mac_len`` (length of MAC tag) for CMAC.
  - Resolved issues
  * In certain circumstances (at counter wrapping, which happens on average after
    32 GBi) AES GCM produced wrong ciphertexts.
  * Method ``encrypt()`` of AES SIV cipher could be still called,
    whereas only ``encrypt_and_digest()`` should be allowed.
- Update to 3.6.0 (8 April 2018)
  - New features
  * Introduced ``export_key`` and deprecated ``exportKey`` for DSA and RSA key
    objects.
  * Ciphers and hash functions accept ``memoryview`` objects in input.
  * Added support for SHA-512/224 and SHA-512/256.
  - Resolved issues
  * Reintroduced `Crypto.__version__` variable as in PyCrypto.
  * Fixed compilation problem with MinGW.
- Update to 3.5.1 (8 March 2018)
  - Resolved issues
  * GH#142. Fix mismatch with declaration and definition of addmul128.
- Update to 3.5.0 (7 March 2018)
  - New features
  * Import and export of ECC curves in compressed form.
  * The initial counter for a cipher in CTR mode can be a byte string
    (in addition to an integer).
  * Faster PBKDF2 for HMAC-based PRFs (at least 20x for short passwords,
    more for longer passwords). Thanks to Christian Heimes for pointing
    out the implementation was under-optimized.
  * The salt for PBKDF2 can be either a string or bytes (GH#67).
  * Ciphers and hash functions accept data as `bytearray`, not just
    binary strings.
  * The old SHA-1 and MD5 hash functions are available even when Python's
    own `hashlib` does not include them.
  - Resolved issues
  * Without libgmp, modular exponentiation (since v3.4.8) crashed
    on 32-bit big-endian systems.
  - Breaks in compatibility
  * Removed support for Python < 2.6.
- Update to 3.4.12 (5 February 2018)
  - Resolved issues
  * GH#129. pycryptodomex could only be installed via wheels.
- Update to 3.4.11 (5 February 2018)
  - Resolved issues
  * GH#121. the record list was still not correct due to PEP3147
    and __pycache__ directories. Thanks again to John O'Brien.
- Update to 3.4.10 (2 February 2018)
  - Resolved issues
  * When creating ElGamal keys, the generator wasn't a square residue:
    ElGamal encryption done with those keys cannot be secure under
    the DDH assumption. Thanks to Weikeng Chen.
- Update to 3.4.9 (1 February 2018)
  - New features
  * More meaningful error messages while importing an ECC key.
  - Resolved issues
  * GH#123 and #125. The SSE2 command line switch was not always passed on
    32-bit x86 platforms.
  * GH#121. The record list (--record) was not always correctly filled for
    the pycryptodomex package. Thanks to John W. O'Brien.
- Update to 3.4.8 (27 January 2018)
  - New features
  * Added a native extension in pure C for modular exponentiation, optimized
    for SSE2 on x86.
    In the process, we drop support for the arbitrary arithmetic library MPIR
    on Windows, which is painful to compile and deploy.
    The custom  modular exponentiation is 130%% (160%%) slower on an Intel CPU
    in 32-bit (64-bit) mode, compared to MPIR. Still, that is much faster
    that CPython's own `pow()` function which is 900%% (855%%) slower than MPIR.
    Support for the GMP library on Unix remains.
  * Added support for *manylinux* wheels.
  * Support for Python 3.7.
  - Resolved issues
  * The DSA parameter 'p' prime was created with 255 bits cleared
    (but still with the correct strength).
  * GH#106. Not all docs were included in the tar ball.
    Thanks to Christopher Hoskin.
  * GH#109. ECDSA verification failed for DER encoded signatures.
    Thanks to Alastair Houghton.
  * Human-friendly messages for padding errors with ECB and CBC.
* Mon Sep 18 2017 hpj@urpla.net
- provide python-crypto 2.6.1
* Wed Sep  6 2017 toddrme2178@gmail.com
- Initial version
