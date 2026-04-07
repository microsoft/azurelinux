# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OpenSSL ENGINE support deprecated in Fedora 41 onwards
# https://fedoraproject.org/wiki/Changes/OpensslDeprecateEngine
%if 0%{?fedora} > 40 || 0%{?rhel} > 9
%global _preprocessor_defines %{?_preprocessor_defines} -DOPENSSL_NO_ENGINE
%endif

Name:		libssh2
Version:	1.11.1
Release:	4%{?dist}
Summary:	A library implementing the SSH2 protocol
License:	BSD-3-Clause
URL:		https://www.libssh2.org/
Source0:	https://libssh2.org/download/libssh2-%{version}.tar.gz
Source1:	https://libssh2.org/download/libssh2-%{version}.tar.gz.asc
# Daniel Stenberg's GPG keys; linked from https://daniel.haxx.se/address.html
Source2:	https://daniel.haxx.se/mykey.asc

BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	gnupg2
BuildRequires:	make
BuildRequires:	openssl-devel > 1:1.0.2
BuildRequires:	pkgconfig
BuildRequires:	sed
BuildRequires:	zlib-devel
BuildRequires:	/usr/bin/man

# Test suite requirements
# Full groff (not just groff-base) needed for the mansyntax check
BuildRequires:	groff
# We run the OpenSSH server and try to connect to it
BuildRequires:	openssh-server
# Need a valid locale to run the mansyntax check
BuildRequires:	glibc-langpack-en

%description
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).

%package	devel
Summary:	Development files for libssh2
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description	devel
The libssh2-devel package contains libraries and header files for
developing applications that use libssh2.

%package	docs
Summary:	Documentation for libssh2
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	docs
The libssh2-docs package contains man pages and examples for
developing applications that use libssh2.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q

# Replace hard wired port number in the test suite to avoid collisions
# between 32-bit and 64-bit builds running on a single build-host
sed -i s/4711/47%{?__isa_bits}/ tests/{openssh_fixture.c,test_ssh{2.c,d.test}}

%build
%configure \
	--disable-rpath \
	--disable-silent-rules \
	--disable-static \
	--enable-shared \
	--disable-docker-tests
%{make_build}

%install
%{make_install} INSTALL="install -p"
find %{buildroot} -name '*.la' -delete

# Clean things up a bit for packaging
make -C example clean
find example/ -type f \
	'(' -name '*.am' -o -name '*.in' -o -name CMakeLists.txt ')' \
	-print -delete

# Remove redundant references to libdir in pkg-config file
sed -i	-e 's|-L%{_libdir} ||g' \
	-e 's|-L[$]{libdir} ||g' %{buildroot}%{_libdir}/pkgconfig/libssh2.pc

# Avoid multilib conflict on libssh2-devel
mv -v example example.%{_arch}

%check
LC_ALL=en_US.UTF-8 make -C tests check

%ldconfig_scriptlets

%files
%license COPYING
%doc docs/AUTHORS README RELEASE-NOTES
%{_libdir}/libssh2.so.1
%{_libdir}/libssh2.so.1.*

%files docs
%doc docs/BINDINGS.md docs/HACKING.md docs/TODO NEWS
%{_mandir}/man3/libssh2_*.3*

%files devel
%doc example.%{_arch}/
%{_includedir}/libssh2.h
%{_includedir}/libssh2_publickey.h
%{_includedir}/libssh2_sftp.h
%{_libdir}/libssh2.so
%{_libdir}/pkgconfig/libssh2.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 16 2024 Paul Howarth <paul@city-fan.org> - 1.11.1-1
- Update to 1.11.1 (rhbz#2319104)
  - This is an enhancement and bugfix release - see RELEASE_NOTES for details
  - Note also that various algorithms are now deprecated and not built by
    default, which affects this package

* Sat Jul 27 2024 Paul Howarth <paul@city-fan.org> - 1.11.0-8
- Fix test suite failures with OpenSSH 9.8p1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Paul Howarth <paul@city-fan.org> - 1.11.0-6
- Build without OpenSSL ENGINE support from Fedora 41 onwards

* Tue Apr 02 2024 Zhao Jiasheng <JasenChao@gmail.com> - 1.11.0-5
- Fix rpath on riscv64

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun  1 2023 Paul Howarth <paul@city-fan.org> - 1.11.0-1
- Update to 1.11.0 (rhbz#2211200)
  - Adds support for encrypt-then-mac (ETM) MACs
  - Adds support for AES-GCM crypto protocols
  - Adds support for sk-ecdsa-sha2-nistp256 and sk-ssh-ed25519 keys
  - Adds support for RSA certificate authentication
  - Adds FIDO support with *_sk() functions
  - Adds RSA-SHA2 key upgrading to OpenSSL, WinCNG, mbedTLS, OS400 backends
  - Adds Agent Forwarding and libssh2_agent_sign()
  - Adds support for Channel Signal message libssh2_channel_signal_ex()
  - Adds support to get the user auth banner message libssh2_userauth_banner()
  - Adds LIBSSH2_NO_{MD5, HMAC_RIPEMD, DSA, RSA, RSA_SHA1, ECDSA, ED25519,
    AES_CBC, AES_CTR, BLOWFISH, RC4, CAST, 3DES} options
  - Adds direct stream UNIX sockets with libssh2_channel_direct_streamlocal_ex()
  - Adds wolfSSL support to CMake file
  - Adds mbedTLS 3.x support
  - Adds LibreSSL 3.5 support
  - Adds support for CMake "unity" builds
  - Adds CMake support for building shared and static libs in a single pass
  - Adds symbol hiding support to CMake
  - Adds support for libssh2.rc for all build tools
  - Adds .zip, .tar.xz and .tar.bz2 release tarballs
  - Enables ed25519 key support for LibreSSL 3.7.0 or higher
  - Improves OpenSSL 1.1 and 3 compatibility
  - Now requires OpenSSL 1.0.2 or newer
  - Now requires CMake 3.1 or newer
  - SFTP: Adds libssh2_sftp_open_ex_r() and libssh2_sftp_open_r() extended APIs
  - SFTP: No longer has a packet limit when reading a directory
  - SFTP: Now parses attribute extensions if they exist
  - SFTP: No longer will busy loop if SFTP fails to initialize
  - SFTP: Now clear various errors as expected
  - SFTP: No longer skips files if the line buffer is too small
  - SCP: Add option to not quote paths
  - SCP: Enables 64-bit offset support unconditionally
  - Now skips leading \r and \n characters in banner_receive()
  - Enables secure memory zeroing with all build tools on all platforms
  - No longer logs SSH_MSG_REQUEST_FAILURE packets from keepalive
  - Speed up base64 encoding by 7x
  - Assert if there is an attempt to write a value that is too large
  - WinCNG: fix memory leak in _libssh2_dh_secret()
  - Added protection against possible null pointer dereferences
  - Agent now handles overly large comment lengths
  - Now ensure KEX replies don't include extra bytes
  - Fixed possible buffer overflow when receiving SSH_MSG_USERAUTH_BANNER
  - Fixed possible buffer overflow in keyboard interactive code path
  - Fixed overlapping memcpy()
  - Fixed Windows UWP builds
  - Fixed DLL import name
  - Renamed local RANDOM_PADDING macro to avoid unexpected define on Windows
  - Support for building with gcc versions older than 8
  - Improvements to CMake, Makefile, NMakefile, GNUmakefile, autoreconf files
  - Restores ANSI C89 compliance
  - Enabled new compiler warnings and fixed/silenced them
  - Improved error messages
  - Now uses CIFuzz
  - Numerous minor code improvements
  - Improvements to CI builds
  - Improvements to unit tests
  - Improvements to doc files
  - Improvements to example files
  - Removed "old gex" build option
  - Removed no-encryption/no-mac builds
  - Removed support for NetWare and Watcom wmake build files
- Avoid use of deprecated patch syntax
- Build static library but don't package it since it's required for the
  test suite (https://github.com/libssh2/libssh2/issues/1056)
- Remove redundant references to %%{_libdir} from pkgconfig file
- Add patch to work around strict permissions issues for sshd tests

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Oct 28 2022 Todd Zullinger <tmz@pobox.com> - 1.10.0-6
- Verify upstream release signatures

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jan 23 2022 Paul Howarth <paul@city-fan.org> - 1.10.0-4
- In 8.8 OpenSSH disabled sha1 rsa-sha keys out of the box,
  so we need to re-enable them as a workaround for the test
  suite until upstream updates the tests
  See: https://github.com/libssh2/libssh2/issues/630
- Drop other test workarounds, none of them being needed any longer

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.10.0-2
- Rebuilt with OpenSSL 3.0.0

* Mon Aug 30 2021 Paul Howarth <paul@city-fan.org> - 1.10.0-1
- Update to 1.10.0
  - Adds agent forwarding support
  - Adds OpenSSH Agent support on Windows
  - Adds ECDSA key support using the Mbed TLS backend
  - Adds ECDSA cert authentication
  - Adds diffie-hellman-group14-sha256, diffie-hellman-group16-sha512,
    diffie-hellman-group18-sha512 key exchanges
  - Adds support for PKIX key reading when using ed25519 with OpenSSL
  - Adds support for EWOULDBLOCK on VMS systems
  - Adds support for building with OpenSSL 3
  - Adds support for using FIPS mode in OpenSSL
  - Adds debug symbols when building with MSVC
  - Adds support for building on the 3DS
  - Adds unicode build support on Windows
  - Restores os400 building
  - Increases min, max and opt Diffie Hellman group values
  - Improves portability of the make file
  - Improves timeout behaviour with 2FA keyboard auth
  - Various improvements to the Wincng backend
  - Fixes reading partial packet replies when using an agent
  - Fixes Diffie Hellman key exchange on Windows 1903+ builds
  - Fixes building tests with older versions of OpenSSL
  - Fixes possible multiple definition warnings
  - Fixes potential cast issues _libssh2_ecdsa_key_get_curve_type()
  - Fixes potential use after free if libssh2_init() is called twice
  - Improved linking when using Mbed TLS
  - Fixes call to libssh2_crypto_exit() if crypto hasn't been initialized
  - Fixes crash when loading public keys with no id
  - Fixes possible out of bounds read when exchanging keys
  - Fixes possible out of bounds read when reading packets
  - Fixes possible out of bounds read when opening an X11 connection
  - Fixes possible out of bounds read when ecdh host keys
  - Fixes possible hang when trying to read a disconnected socket
  - Fixes a crash when using the delayed compression option
  - Fixes read error with large known host entries
  - Fixes various warnings
  - Fixes various small memory leaks
  - Improved error handling, various detailed errors will now be reported
  - Builds are now using OSS-Fuzz
  - Builds now use autoreconf instead of a custom build script
  - cmake now respects install directory
  - Improved CI backend
  - Updated HACKING-CRYPTO documentation
  - Use markdown file extensions
  - Improved unit tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar 27 2020 Paul Howarth <paul@city-fan.org> - 1.9.0-5
- Switch to https:// upstream URLs
- Full groff (not just groff-base) needed for the mansyntax check

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 30 2019 Kamil Dudka <kdudka@redhat.com> - 1.9.0-3
- Fix integer overflow in SSH_MSG_DISCONNECT logic (CVE-2019-17498)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 20 2019 Paul Howarth <paul@city-fan.org> - 1.9.0-1
- Update to 1.9.0
  - Fixed integer overflow leading to out-of-bounds read (CVE-2019-13115)
  - Adds ECDSA keys and host key support when using OpenSSL
  - Adds ED25519 key and host key support when using OpenSSL 1.1.1
  - Adds OpenSSH style key file reading
  - Adds AES CTR mode support when using WinCNG
  - Adds PEM passphrase protected file support for libgcrypt and WinCNG
  - Adds SHA256 hostkey fingerprint
  - Adds libssh2_agent_get_identity_path() and libssh2_agent_set_identity_path()
  - Adds explicit zeroing of sensitive data in memory
  - Adds additional bounds checks to network buffer reads
  - Adds the ability to use the server default permissions when creating sftp directories
  - Adds support for building with OpenSSL no engine flag
  - Adds support for building with LibreSSL
  - Increased sftp packet size to 256k
  - Fixed oversized packet handling in sftp
  - Fixed building with OpenSSL 1.1
  - Fixed a possible crash if sftp stat gets an unexpected response
  - Fixed incorrect parsing of the KEX preference string value
  - Fixed conditional RSA and AES-CTR support
  - Fixed a small memory leak during the key exchange process
  - Fixed a possible memory leak of the ssh banner string
  - Fixed various small memory leaks in the backends
  - Fixed possible out of bounds read when parsing public keys from the server
  - Fixed possible out of bounds read when parsing invalid PEM files
  - No longer null terminates the scp remote exec command
  - Now handle errors when Diffie Hellman key pair generation fails
  - Fixed compiling on Windows with the flag STDCALL=ON
  - Improved building instructions
  - Improved unit tests
- Needs OpenSSL ≥ 1.0.1 now as ECC support is assumed
- Modernize spec somewhat as EL-6 can no longer be supported

* Tue Mar 26 2019 Paul Howarth <paul@city-fan.org> - 1.8.2-1
- Update to 1.8.2
  - Fixed the misapplied userauth patch that broke 1.8.1
  - Moved the MAX size declarations from the public header

* Tue Mar 19 2019 Paul Howarth <paul@city-fan.org> - 1.8.1-1
- Update to 1.8.1
  - Fixed possible integer overflow when reading a specially crafted packet
    (CVE-2019-3855)
  - Fixed possible integer overflow in userauth_keyboard_interactive with a
    number of extremely long prompt strings (CVE-2019-3863)
  - Fixed possible integer overflow if the server sent an extremely large
    number of keyboard prompts (CVE-2019-3856)
  - Fixed possible out of bounds read when processing a specially crafted
    packet (CVE-2019-3861)
  - Fixed possible integer overflow when receiving a specially crafted exit
    signal message channel packet (CVE-2019-3857)
  - Fixed possible out of bounds read when receiving a specially crafted exit
    status message channel packet (CVE-2019-3862)
  - Fixed possible zero byte allocation when reading a specially crafted SFTP
    packet (CVE-2019-3858)
  - Fixed possible out of bounds reads when processing specially crafted SFTP
    packets (CVE-2019-3860)
  - Fixed possible out of bounds reads in _libssh2_packet_require(v)
    (CVE-2019-3859)
- Fix mis-applied patch in the fix of CVE-2019-3859
  - https://github.com/libssh2/libssh2/issues/325
  - https://github.com/libssh2/libssh2/pull/327

* Mon Feb  4 2019 Paul Howarth <paul@city-fan.org> - 1.8.0-10
- Explicitly run the test suite in the en_US.UTF-8 locale to work around flaky
  locale settings in mock builders

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.0-6
- Switch to %%ldconfig_scriptlets

* Tue Sep 12 2017 Paul Howarth <paul@city-fan.org> - 1.8.0-5
- scp: Do not NUL-terminate the command for remote exec (#1489736, GH#208)
- Make devel package dependency on main package arch-specific
- Drop EL-5 support
  - noarch sub-packages always available now
  - Drop legacy Group: and BuildRoot: tags
  - Drop explicit buildroot cleaning
  - %%{__isa_bits} always defined now

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 25 2016 Paul Howarth <paul@city-fan.org> - 1.8.0-1
- Update to 1.8.0
  - Added a basic dockerised test suite
  - crypto: Add support for the mbedTLS backend
  - See RELEASE-NOTES for details of bug fixes

* Thu Oct 20 2016 Kamil Dudka <kdudka@redhat.com> - 1.7.0-7
- Make curl test-suite work again with valgrind enabled

* Tue Oct 11 2016 Tomáš Mráz <tmraz@redhat.com> - 1.7.0-6
- Rebuild with OpenSSL 1.1.0

* Sun Mar  6 2016 Paul Howarth <paul@city-fan.org> - 1.7.0-5
- Revert parts of previous change that broke EL-5 compatibility
- Include NEWS in docs package, it's much more than RELEASE-NOTES

* Sat Mar  5 2016 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.0-4
- Modernise spec (no we really don't care about el4/fc4)
- Don't ship ChangeLog/NEWS, duplicates of RELEASE-NOTES

* Wed Feb 24 2016 Paul Howarth <paul@city-fan.org> - 1.7.0-3
- Drop UTF-8 patch, which breaks things rather than fixes them

* Wed Feb 24 2016 Kamil Dudka <kdudka@redhat.com> - 1.7.0-2
- diffie_hellman_sha1: Convert bytes to bits (additional fix for CVE-2016-0787)

* Tue Feb 23 2016 Paul Howarth <paul@city-fan.org> - 1.7.0-1
- Update to 1.7.0
  - diffie_hellman_sha256: Convert bytes to bits (CVE-2016-0787); see
    http://www.libssh2.org/adv_20160223.html
  - libssh2_session_set_last_error: Add function
  - See RELEASE-NOTES for details of bug fixes

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Paul Howarth <paul@city-fan.org> - 1.6.0-3
- Fix pkg-config --libs output (#1279966)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Paul Howarth <paul@city-fan.org> - 1.6.0-1
- Update to 1.6.0
  - Added CMake build system
  - Added libssh2_userauth_publickey_frommemory()
  - See RELEASE-NOTES for details of bug fixes

* Wed Mar 11 2015 Paul Howarth <paul@city-fan.org> - 1.5.0-1
- Update to 1.5.0
  - See RELEASE-NOTES for details of bug fixes and enhancements
  - Security Advisory for CVE-2015-1782, using SSH_MSG_KEXINIT data unbounded

* Fri Oct 10 2014 Kamil Dudka <kdudka@redhat.com> 1.4.3-16
- prevent a not-connected agent from closing STDIN (#1147717)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 1.4.3-14
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Kamil Dudka <kdudka@redhat.com> 1.4.3-12
- Fix curl's excessive memory consumption during scp download

* Mon Feb 17 2014 Paul Howarth <paul@city-fan.org> - 1.4.3-11
- The aarch64 buildroot seems to have the same locale issue as the PPC one

* Mon Feb 17 2014 Karsten Hopp <karsten@redhat.com> 1.4.3-10
- Next attempt to work around a self check problem on PPC*

* Mon Feb 17 2014 Karsten Hopp <karsten@redhat.com> 1.4.3-9
- Skip self checks on ppc*

* Wed Aug 14 2013 Kamil Dudka <kdudka@redhat.com> 1.4.3-8
- Fix very slow sftp upload to localhost
- Fix a use after free in channel.c

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  9 2013 Paul Howarth <paul@city-fan.org> 1.4.3-6
- Revert 'Modernize the spec file' so as to retain EL-5 spec compatibility

* Tue Apr  9 2013 Richard W.M. Jones <rjones@redhat.com> 1.4.3-5
- Add three patches from upstream git required for qemu ssh block driver
- Modernize the spec file:
  * Remove BuildRoot
  * Remove Group
  * Remove clean section
  * Don't need to clean up buildroot before installing

* Wed Apr  3 2013 Paul Howarth <paul@city-fan.org> 1.4.3-4
- Avoid polluting libssh2.pc with linker options (#947813)

* Tue Mar 26 2013 Kamil Dudka <kdudka@redhat.com> 1.4.3-3
- Avoid collisions between 32-bit and 64-bit builds running on a single build
  host

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Paul Howarth <paul@city-fan.org> 1.4.3-1
- Update to 1.4.3
  - compression: add support for zlib@openssh.com
  - sftp_read: return error if a too large package arrives
  - libssh2_hostkey_hash.3: update the description of return value
  - Fixed MSVC NMakefile
  - examples: use stderr for messages, stdout for data
  - openssl: do not leak memory when handling errors
  - improved handling of disabled MD5 algorithm in OpenSSL
  - known_hosts: Fail when parsing unknown keys in known_hosts file
  - configure: gcrypt doesn't come with pkg-config support
  - session_free: wrong variable used for keeping state
  - libssh2_userauth_publickey_fromfile_ex.3: mention publickey == NULL
  - comp_method_zlib_decomp: handle Z_BUF_ERROR when inflating
- Drop upstreamed patches

* Wed Nov 07 2012 Kamil Dudka <kdudka@redhat.com> 1.4.2-4
- examples: use stderr for messages, stdout for data (upstream commit b31e35ab)
- Update libssh2_hostkey_hash(3) man page (upstream commit fe8f3deb)

* Wed Sep 26 2012 Kamil Dudka <kdudka@redhat.com> 1.4.2-3
- Fix basic functionality of libssh2 in FIPS mode
- Skip SELinux-related quirks on recent distros to prevent a test-suite failure

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Paul Howarth <paul@city-fan.org> 1.4.2-1
- Update to 1.4.2
  - Return LIBSSH2_ERROR_SOCKET_DISCONNECT on EOF when reading banner
  - userauth.c: fread() from public key file to correctly detect any errors
  - configure.ac: add option to disable build of the example applications
  - added 'Requires.private:' line to libssh2.pc
  - SFTP: filter off incoming "zombie" responses
  - gettimeofday: no need for a replacement under cygwin
  - SSH_MSG_CHANNEL_REQUEST: default to want_reply
  - win32/libssh2_config.h: remove hardcoded #define LIBSSH2_HAVE_ZLIB

* Fri Apr 27 2012 Paul Howarth <paul@city-fan.org> 1.4.1-2
- Fix multi-arch conflict again (#816969)

* Thu Apr  5 2012 Paul Howarth <paul@city-fan.org> 1.4.1-1
- Update to 1.4.1
  - Build error with gcrypt backend
  - Always do "forced" window updates to avoid corner case stalls
  - aes: the init function fails when OpenSSL has AES support
  - transport_send: finish in-progress key exchange before sending data
  - channel_write: acknowledge transport errors
  - examples/x11.c: make sure sizeof passed to read operation is correct
  - examples/x11.c: fix suspicious sizeof usage
  - sftp_packet_add: verify the packet before accepting it
  - SFTP: preserve the original error code more
  - sftp_packet_read: adjust window size as necessary
  - Use safer snprintf rather then sprintf in several places
  - Define and use LIBSSH2_INVALID_SOCKET instead of INVALID_SOCKET
  - sftp_write: cannot return acked data *and* EAGAIN
  - sftp_read: avoid data *and* EAGAIN
  - libssh2.h: add missing prototype for libssh2_session_banner_set()
- Drop upstream patches now included in release tarball

* Mon Mar 19 2012 Kamil Dudka <kdudka@redhat.com> 1.4.0-4
- Don't ignore transport errors when writing to channel (#804150)

* Sun Mar 18 2012 Paul Howarth <paul@city-fan.org> 1.4.0-3
- Don't try to use openssl's AES-CTR functions
  (http://www.libssh2.org/mail/libssh2-devel-archive-2012-03/0111.shtml)

* Fri Mar 16 2012 Paul Howarth <paul@city-fan.org> 1.4.0-2
- fix libssh2 failing key re-exchange when write channel is saturated (#804156)
- drop %%defattr, redundant since rpm 4.4

* Wed Feb  1 2012 Paul Howarth <paul@city-fan.org> 1.4.0-1
- update to 1.4.0
  - added libssh2_session_supported_algs()
  - added libssh2_session_banner_get()
  - added libssh2_sftp_get_channel()
  - libssh2.h: bump the default window size to 256K
  - sftp-seek: clear EOF flag
  - userauth: provide more informations if ssh pub key extraction fails
  - ssh2_exec: skip error outputs for EAGAIN
  - LIBSSH2_SFTP_PACKET_MAXLEN: increase to 80000
  - knownhost_check(): don't dereference ext if NULL is passed
  - knownhost_add: avoid dereferencing uninitialized memory on error path
  - OpenSSL EVP: fix threaded use of structs
  - _libssh2_channel_read: react on errors from receive_window_adjust
  - sftp_read: cap the read ahead maximum amount
  - _libssh2_channel_read: fix non-blocking window adjusting
- add upstream patch fixing undefined function reference in libgcrypt backend
- BR: /usr/bin/man for test suite

* Sun Jan 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.3.0-4
- skip the ssh test on ARM too

* Fri Jan 13 2012 Paul Howarth <paul@city-fan.org> 1.3.0-3
- make docs package noarch where possible
- example includes arch-specific bits, so move to devel package
- use patch rather than scripted iconv to fix character encoding
- don't make assumptions about SELinux context types used for the ssh server
  in the test suite
- skip the ssh test if /dev/tty isn't present, as in some versions of mock
- make the %%files list more explicit
- use tabs for indentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.3.0-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 08 2011 Kamil Dudka <kdudka@redhat.com> 1.3.0-1
- update to 1.3.0

* Sat Jun 25 2011 Dennis Gilmore <dennis@ausil.us> 1.2.7-2
- sshd/loopback test fails in the sparc buildsystem

* Tue Oct 12 2010 Kamil Dudka <kdudka@redhat.com> 1.2.7-1
- update to 1.2.7 (#632916)
- avoid multilib conflict on libssh2-docs
- avoid build failure in mock with SELinux in the enforcing mode (#558964)

* Fri Mar 12 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.4-1
- update to 1.2.4
- drop old patch0
- be more aggressive about keeping .deps from intruding into -docs

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.2-5
- pkgconfig dep should be with -devel, not -docs

* Mon Jan 18 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.2-4
- enable tests; conditionalize sshd test, which fails with a funky SElinux
  error when run locally

* Mon Jan 18 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.2-3
- patch w/1aba38cd7d2658146675ce1737e5090f879f306; not yet in a GA release

* Thu Jan 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.2-2
- correct bad file entry under -devel

* Thu Jan 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.2-1
- update to 1.2.2
- drop old patch now in upstream
- add new pkgconfig file to -devel

* Mon Sep 21 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.2-2
- patch based on 683aa0f6b52fb1014873c961709102b5006372fc
- disable tests (*sigh*)

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.2-1
- update to 1.2

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0-4
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.0-1
- update to 1.0

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.18-8
- rebuild with new openssl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.18-7
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-6
- rebuild for new openssl...

* Tue Nov 27 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-5
- bump

* Tue Nov 27 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-4
- add INSTALL arg to make install vs env. var

* Mon Nov 26 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-3
- run tests; don't package test

* Sun Nov 18 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-2
- split docs into -docs (they seemed... large.)

* Tue Nov 13 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- update to 0.18

* Sun Oct 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- update to 0.17
- many spec file changes

* Wed May 23 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.15-0.2.20070506
- Fix release tag
- Move manpages to -devel package
- Add Examples dir to -devel package

* Sun May 06 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.15-0.20070506.1
- Initial build
