%global srcname paramiko

Name:          python-%{srcname}
Version:       2.11.0
Release:       2%{?dist}
Summary:       SSH2 protocol library for python
License:       LGPLv2+
Distribution:  Mariner
Vendor:        Microsoft Corporation
URL:           https://github.com/paramiko/paramiko
Source0:       %{url}/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

# Remove pytest-relaxed, which depends on pytest4
# Can be removed when https://github.com/paramiko/paramiko/pull/1665/ is released
Patch1:        0001-remove-pytest-relaxed-dep.patch

# Avoid use of deprecated python-mock by using unittest.mock instead
# Can be removed when https://github.com/paramiko/paramiko/pull/1666/ is released
Patch2:        0002-remove-mock-dep.patch

BuildArch:     noarch

%global paramiko_desc \
Paramiko (a combination of the Esperanto words for "paranoid" and "friend") is\
a module for python 2.3 or greater that implements the SSH2 protocol for secure\
(encrypted and authenticated) connections to remote machines. Unlike SSL (aka\
TLS), the SSH2 protocol does not require hierarchical certificates signed by a\
powerful central authority. You may know SSH2 as the protocol that replaced\
telnet and rsh for secure access to remote shells, but the protocol also\
includes the ability to open arbitrary channels to remote services across an\
encrypted tunnel (this is how sftp works, for example).

%description
%{paramiko_desc}

%package -n python3-%{srcname}
Summary:       SSH2 protocol library for python
BuildRequires: python3-sphinx
BuildRequires: python3-devel
BuildRequires: python3-bcrypt
BuildRequires: python3-cryptography
BuildRequires: python3-pyasn1
BuildRequires: python3-pynacl
BuildRequires: python3-setuptools
BuildRequires: python3-six
Requires:      python3-bcrypt
Requires:      python3-cryptography
Requires:      python3-pynacl
Requires:      python3-six

%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif

Recommends:    %{py3_dist pyasn1} >= 0.1.7

%description -n python%{python3_pkgversion}-%{srcname}
%{paramiko_desc}

%prep
%autosetup -p1 -n %{srcname}-%{version}

chmod -c a-x demos/*
sed -i -e '/^#!/,1d' demos/*

%build
%py3_build

%install
%py3_install

sphinx-build-3 -b html sites/docs/ html/
rm html/.buildinfo

%check
%{python3} -m pip install atomicwrites attrs docutils pluggy pygments six more-itertools invoke
PYTHONPATH=%{buildroot}%{python3_sitelib} pytest3

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc NEWS README.rst
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/

%changelog
* Thu Jun 23 2022 Sumedh Sharma <sumsharma@microsoft.com> - 2.11.0-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- Adding as build dependency for apache-libcloud needed by cassandra-medusa.
- Removing subpackage doc.
- License verified

* Tue May 17 2022 Paul Howarth <paul@city-fan.org> - 2.11.0-1
- Update to 2.11.0
  - Align signature verification algorithm with OpenSSH re: zero-padding
    signatures that don't match their nominal size/length; this shouldn't
    affect most users, but will help Paramiko-implemented SSH servers handle
    poorly behaved clients such as PuTTY (GH#1933)
  - OpenSSH 7.7 and older has a bug preventing it from understanding how to
    perform SHA2 signature verification for RSA certificates (specifically
    certs - not keys), so when we added SHA2 support it broke all clients using
    RSA certificates with these servers; this has been fixed in a manner similar
    to what OpenSSH's own client does - a version check is performed and the
    algorithm used is downgraded if needed (GH#2017)
  - Recent versions of Cryptography have deprecated Blowfish algorithm support;
    in lieu of an easy method for users to remove it from the list of
    algorithms Paramiko tries to import and use, we've decided to remove it
    from our "preferred algorithms" list, which will both discourage use of a
    weak algorithm, and avoid warnings (GH#2038, GH#2039)
  - Windows-native SSH agent support as merged in 2.10 could encounter
    'Errno 22' 'OSError' exceptions in some scenarios (e.g. server not cleanly
    closing a relevant named pipe); this has been worked around and should be
    less problematic (GH#2008, GH#2010)
  - Add SSH config token expansion (eg '%%h', '%%p') when parsing 'ProxyJump'
    directives (GH#1951)
  - Apply unittest 'skipIf' to tests currently using SHA1 in their critical
    path, to avoid failures on systems starting to disable SHA1 outright in
    their crypto backends (e.g. RHEL 9) (GH#2004, GH#2011)

* Tue Apr 26 2022 Paul Howarth <paul@city-fan.org> - 2.10.4-1
- Update to 2.10.4
  - Update 'camelCase' method calls against the 'threading' module to be
    'snake_case'; this and related tweaks should fix some deprecation warnings
    under Python 3.10 (GH#1838, GH#1870, GH#2028)
  - '~paramiko.pkey.PKey' instances' '__eq__' did not have the usual safety
    guard in place to ensure they were being compared to another 'PKey' object,
    causing occasional spurious 'BadHostKeyException', among other things
    (GH#1964, GH#2023, GH#2024)
  - Servers offering certificate variants of hostkey algorithms (e.g.
    'ssh-rsa-cert-v01@openssh.com') could not have their host keys verified by
    Paramiko clients, as it only ever considered non-cert key types for that
    part of connection handshaking (GH#2035)

* Mon Mar 21 2022 Paul Howarth <paul@city-fan.org> - 2.10.3-2
- Skip tests that would fail without SHA-1 signing support in backend, such as
  on EL-9 (GH#2011)

* Sat Mar 19 2022 Paul Howarth <paul@city-fan.org> - 2.10.3-1
- Update to 2.10.3
  - Certificate-based pubkey auth was inadvertently broken when adding SHA2
    support in version 2.9.0 (GH#1963, GH#1977)
  - Switch from module-global to thread-local storage when recording thread IDs
    for a logging helper; this should avoid one flavor of memory leak for
    long-running processes (GH#2002, GH#2003)

* Tue Mar 15 2022 Paul Howarth <paul@city-fan.org> - 2.10.2-1
- Update to 2.10.2
  - Fix Python 2 compatibility breakage introduced in 2.10.1 (GH#2001)
- Re-enable sftp tests, no longer failing under mock

* Sun Mar 13 2022 Paul Howarth <paul@city-fan.org> - 2.10.1-1
- Update to 2.10.1
  - CVE-2022-24302: Creation of new private key files using
    '~paramiko.pkey.PKey' subclasses was subject to a race condition between
    file creation and mode modification, which could be exploited by an
    attacker with knowledge of where the Paramiko-using code would write out
    such files; this has been patched by using 'os.open' and 'os.fdopen' to
    ensure new files are opened with the correct mode immediately (we've left
    the subsequent explicit 'chmod' in place to minimize any possible
    disruption, though it may get removed in future backwards-incompatible
    updates)
  - Add support for the '%%C' token when parsing SSH config files (GH#1976)
  - Add support for OpenSSH's Windows agent as a fallback when Putty/WinPageant
    isn't available or functional (GH#1509, GH#1837, GH#1868)
  - Significantly speed up low-level read/write actions on
    '~paramiko.sftp_file.SFTPFile' objects by using 'bytearray'/'memoryview'
    (GH#892); this is unlikely to change anything for users of the higher level
    methods like 'SFTPClient.get' or 'SFTPClient.getfo', but users of
    'SFTPClient.open' will likely see orders of magnitude improvements for
    files larger than a few megabytes in size
  - Add 'six' explicitly to install-requires; it snuck into active use at some
    point but has only been indicated by transitive dependency on 'bcrypt'
    until they somewhat-recently dropped it (GH#1985); this will be short-lived
    until we drop Python 2 support

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Paul Howarth <paul@city-fan.org> - 2.9.2-2
- Avoid use of deprecated python-mock by using unittest.mock instead
  https://github.com/paramiko/paramiko/pull/1666

* Sat Jan  8 2022 Paul Howarth <paul@city-fan.org> - 2.9.2-1
- Update to 2.9.2
  - Connecting to servers that support 'server-sig-algs' but which have no
    overlap between that list and what a Paramiko client supports, now raise
    an exception instead of defaulting to 'rsa-sha2-512' (since the use of
    'server-sig-algs' allows us to know what the server supports)
  - Enhanced log output when connecting to servers that do not support
    'server-sig-algs' extensions, making the new-as-of-2.9 defaulting to SHA2
    pubkey algorithms more obvious when it kicks in

* Sat Dec 25 2021 Paul Howarth <paul@city-fan.org> - 2.9.1-1
- Update to 2.9.1
  - Server-side support for 'rsa-sha2-256' and 'ssh-rsa' wasn't fully operable
    after 2.9.0's release (signatures for RSA pubkeys were always run through
    'rsa-sha2-512' instead) (GH#1935)

* Fri Dec 24 2021 Paul Howarth <paul@city-fan.org> - 2.9.0-1
- Update to 2.9.0
  - Add support for SHA-2 variants of RSA key verification algorithms (as
    described in RFC 8332) as well as limited SSH extension negotiation (RFC
    8308) (GH#1326, GH#1643, GH#1644, GH#1925)
    How SSH servers/clients decide when and how to use this functionality can be
    complicated; Paramiko's support is as follows:
    - Client verification of server host key during key exchange will now prefer
      rsa-sha2-512, rsa-sha2-256, and legacy ssh-rsa algorithms, in that order,
      instead of just ssh-rsa
    - Note that the preference order of other algorithm families such as
      ed25519 and ecdsa has not changed; for example, those two groups are still
      preferred over RSA
    - Server mode will now offer all 3 RSA algorithms for host key verification
      during key exchange, similar to client mode, if it has been configured
      with an RSA host key
    - Client mode key exchange now sends the ext-info-c flag signaling support
      for MSG_EXT_INFO, and support for parsing the latter (specifically, its
      server-sig-algs flag) has been added
    - Client mode, when performing public key authentication with an RSA key or
      cert, will act as follows:
      - In all cases, the list of algorithms to consider is based on the new
        preferred_pubkeys list and disabled_algorithms; this list, like with
        host keys, prefers SHA2-512, SHA2-256 and SHA1, in that order
      - When the server does not send server-sig-algs, Paramiko will attempt
        the first algorithm in the above list; clients connecting to legacy
        servers should thus use disabled_algorithms to turn off SHA2
      - When the server does send server-sig-algs, the first algorithm
        supported by both ends is used, or if there is none, it falls back to
        the previous behavior
    - SSH agent support grew the ability to specify algorithm flags when
      requesting private key signatures; this is now used to forward SHA2
      algorithms when appropriate
    - Server mode is now capable of pubkey auth involving SHA-2 signatures from
      clients, provided one's server implementation actually provides for doing
      so; this includes basic support for sending MSG_EXT_INFO (containing
      server-sig-algs only) to clients advertising ext-info-c in their key
      exchange list
    In order to implement the above, the following API additions were made:
    - 'PKey.sign_ssh_data <paramiko.pkey.PKey>': Grew an extra, optional
      'algorithm' keyword argument (defaulting to 'None' for most subclasses,
      and to "ssh-rsa" for '~paramiko.rsakey.RSAKey')
    - A new '~paramiko.ssh_exception.SSHException' subclass was added,
      '~paramiko.ssh_exception.IncompatiblePeer', and is raised in all spots
      where key exchange aborts due to algorithmic incompatibility; like all
      other exceptions in that module, it inherits from 'SSHException', and as
      nothing else was changed about the raising (i.e. the attributes and
      message text are the same) this change is backwards compatible
    - '~paramiko.transport.Transport' grew a '_preferred_pubkeys' attribute and
      matching 'preferred_pubkeys' property to match the other, kex-focused,
      such members; this allows client pubkey authentication to honor the
      'disabled_algorithms' feature

* Mon Nov 29 2021 Paul Howarth <paul@city-fan.org> - 2.8.1-1
- Update to 2.8.1
  - Fix listdir failure when server uses a locale (GH#985, GH#992); now on
    Python 2.7 SFTPAttributes will decode abbreviated month names correctly
    rather than raise 'UnicodeDecodeError'
  - Deleting items from '~paramiko.hostkeys.HostKeys' would incorrectly raise
    'KeyError' even for valid keys, due to a logic bug (GH#1024)
  - Update RSA and ECDSA key decoding subroutines to correctly catch exception
    types thrown by modern versions of Cryptography (specifically 'TypeError'
    and its internal 'UnsupportedAlgorithm') (GH#1257, GH#1266); these
    exception classes will now become '~paramiko.ssh_exception.SSHException'
    instances instead of bubbling up
  - Update '~paramiko.pkey.PKey' and subclasses to compare ('__eq__') via
    direct field/attribute comparison instead of hashing (while retaining the
    existing behavior of '__hash__' via a slight refactor) (GH#908)
    Warning:
    This fixes a security flaw! If you are running Paramiko on 32-bit systems
    with low entropy (such as any 32-bit Python 2, or a 32-bit Python 3 that is
    running with 'PYTHONHASHSEED=0') it is possible for an attacker to craft a
    new keypair from an exfiltrated public key, which Paramiko would consider
    equal to the original key.
    This could enable attacks such as, but not limited to, the following:
    - Paramiko server processes would incorrectly authenticate the attacker
      (using their generated private key) as if they were the victim. We see
      this as the most plausible attack using this flaw.
    - Paramiko client processes would incorrectly validate a connected server
      (when host key verification is enabled) while subjected to a
      man-in-the-middle attack. This impacts more users than the server-side
      version, but also carries higher requirements for the attacker, namely
      successful DNS poisoning or other MITM techniques.

* Mon Oct 11 2021 Paul Howarth <paul@city-fan.org> - 2.8.0-1
- Update to 2.8.0
  - Administrivia overhaul, including but not limited to:
    - Migrate CI to CircleCI
    - Primary dev branch is now 'main' (renamed)
    - Many README edits for clarity, modernization etc.; including a bunch more
      (and consistent) status badges and unification with main project site
      index
    - PyPI page much more fleshed out (long_description is now filled in with
      the README; sidebar links expanded; etc.)
    - flake8, pytest configs split out of setup.cfg into their own files
    - Invoke/invocations (used by maintainers/contributors) upgraded to modern
      versions
  - Newer server-side key exchange algorithms not intended to use SHA1
    (diffie-hellman-group14-sha256, diffie-hellman-group16-sha512) were
    incorrectly using SHA1 after all, due to a bug causing them to ignore the
    'hash_algo' class attribute; this has been corrected (GH#1452, GH#1882)
  - Add a 'prefetch' keyword argument to 'SFTPClient.get'/'SFTPClient.getfo' so
    that users who need to skip SFTP prefetching are able to conditionally turn
    it off (GH#1846)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.7.2-5
- Rebuilt for Python 3.10

* Wed Mar  3 2021 Paul Howarth <paul@city-fan.org> - 2.7.2-4
- Drop invoke dependencies as it requires ancient pytest and we can't expect
  it to remain around

* Tue Mar 02 2021 Dan Radez <dradez@redhat.com> - 2.7.2-3
- Removing the python-relax dep using upstream patch
  https://github.com/paramiko/paramiko/pull/1665/

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 31 2020 Paul Howarth <paul@city-fan.org> - 2.7.2-1
- Update to 2.7.2
  - Update our CI to catch issues with sdist generation, installation and
    testing
  - Add missing test suite fixtures directory to MANIFEST.in, reinstating the
    ability to run Paramiko's tests from an sdist tarball (GH#1727)
  - Remove leading whitespace from OpenSSH RSA test suite static key fixture,
    to conform better to spec. (GH#1722)
  - Fix incorrect string formatting causing unhelpful error message annotation
    when using Kerberos/GSSAPI
  - Fix incorrectly swapped order of 'p' and 'q' numbers when loading
    OpenSSH-format RSA private keys; at minimum this should address a slowdown
    when using such keys, and it also means Paramiko works with Cryptography
    3.1 and above, which complains strenuously when this problem appears
    (GH#1723)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 30 2020 Paul Howarth <paul@city-fan.org> - 2.7.1-4
- Avoid FTBFS with pytest 5 (pytest-relaxed pulls in pytest 4)
- Drop explicit dependencies for things that the python dependency generator
  finds by itself

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 2.7.1-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 11 2019 Paul Howarth <paul@city-fan.org> - 2.7.1-1
- Update to 2.7.1
  - The new-style private key format (added in 2.7.0) suffered from an
    unpadding bug that had been fixed earlier for Ed25519 (as that key type has
    always used the newer format); that fix has been refactored and applied to
    the base key class (GH#1567)
  - Fix a bug in support for ECDSA keys under the newly-supported OpenSSH key
    format (GH#1565, GH#1566)

* Wed Dec  4 2019 Paul Howarth <paul@city-fan.org> - 2.7.0-1
- Update to 2.7.0
  - Implement support for OpenSSH 6.5-style private key files (typically
    denoted as having 'BEGIN OPENSSH PRIVATE KEY' headers instead of PEM
    format's 'BEGIN RSA PRIVATE KEY' or similar); if you were getting any sort
    of weird auth error from "modern" keys generated on newer operating system
    releases (such as macOS Mojave), this is the first update to try (GH#602,
    GH#618, GH#1313, GH#1343)
  - Token expansion in 'ssh_config' used a different method of determining the
    local username ('$USER' environment variable), compared to what the (much
    older) client connection code does ('getpass.getuser', which includes
    '$USER' but may check other variables first, and is generally much more
    comprehensive); both modules now use 'getpass.getuser'
  - A couple of outright '~paramiko.config.SSHConfig' parse errors were
    previously represented as vanilla 'Exception' instances; as part of recent
    feature work a more specific exception class,
    '~paramiko.ssh_exception.ConfigParseError', has been created; it is now
    also used in those older spots, which is naturally backwards compatible
  - Implement support for the 'Match' keyword in 'ssh_config' files;
    previously, this keyword was simply ignored and keywords inside such blocks
    were treated as if they were part of the previous block (GH#717)
    - Note: this feature adds a new optional install dependency 'Invoke'
      (https://www.pyinvoke.org), for managing 'Match exec' subprocesses
  - Additional installation 'extras_require' "flavors" ('ed25519', 'invoke',
    and 'all') have been added to our packaging metadata
  - Paramiko's use of 'subprocess' for 'ProxyCommand' support is conditionally
    imported to prevent issues on limited interpreter platforms like Google
    Compute Engine; however, any resulting 'ImportError' was lost instead of
    preserved for raising (in the rare cases where a user tried leveraging
    'ProxyCommand' in such an environment); this has been fixed
  - Perform deduplication of 'IdentityFile' contents during 'ssh_config'
    parsing; previously, if your config would result in the same value being
    encountered more than once, 'IdentityFile' would contain that many copies
    of the same string
  - Implement most 'canonical hostname' 'ssh_config' functionality
    ('CanonicalizeHostname', 'CanonicalDomains', 'CanonicalizeFallbackLocal',
    and 'CanonicalizeMaxDots'; 'CanonicalizePermittedCNAMEs' has *not* yet
    been implemented) - all were previously silently ignored (GH#897)
  - Explicitly document which ssh_config features we currently support;
    previously users just had to guess, which is simply no good
  - Add new convenience classmethod constructors to
    '~paramiko.config.SSHConfig': '~paramiko.config.SSHConfig.from_text',
    '~paramiko.config.SSHConfig.from_file', and
    '~paramiko.config.SSHConfig.from_path'; no more annoying two-step process!
- Add Recommends: of python3-invoke and python3-pyasn1 for optional
  functionality

* Sun Oct 06 2019 Othman Madjoudj <athmane@fedoraproject.org> - 2.6.0-5
- Drop python2 subpackage since it's eol-ed

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Paul Howarth <paul@city-fan.org> - 2.6.0-1
- Update to 2.6.0
  - Add a new keyword argument to 'SSHClient.connect' and
    '~paramiko.transport.Transport', 'disabled_algorithms', which allows
    selectively disabling one or more kex/key/cipher/etc algorithms; this can
    be useful when disabling algorithms your target server (or client) does not
    support cleanly, or to work around unpatched bugs in Paramiko's own
    implementation thereof (GH#1463)
  - Tweak many exception classes so their string representations are more
    human-friendly; this also includes incidental changes to some 'super()'
    calls (GH#1440, GH#1460)
  - Add backwards-compatible support for the 'gssapi' GSSAPI library, as the
    previous backend ('python-gssapi') has become defunct (GH#584, GH#1166,
    GH#1311)
  - 'SSHClient.exec_command' now returns a new subclass,
    '~paramiko.channel.ChannelStdinFile', rather than a naïve
    '~paramiko.channel.ChannelFile' object for its 'stdin' value, which fixes
    issues such as hangs when running remote commands that read from stdin
    (GH#322)
- Drop gssapi patch as it's no longer needed
- Drop pytest-relaxed patch as it's no longer needed

* Thu Jun 27 2019 Paul Howarth <paul@city-fan.org> - 2.5.1-1
- Update to 2.5.1
  - Fix Ed25519 key handling so certain key comment lengths don't cause
    'SSHException("Invalid key")' (GH#1306, GH#1400)

* Mon Jun 10 2019 Paul Howarth <paul@city-fan.org> - 2.5.0-1
- Update to 2.5.0
  - Add support for encrypt-then-MAC (ETM) schemes and two newer Diffie-Hellman
    group key exchange algorithms ('group14', using SHA256; and 'group16',
    using SHA512)
  - Add support for Curve25519 key exchange
  - Raise Cryptography dependency requirement to version 2.5 (from 1.5) and
    update some deprecated uses of its API
  - Add support for the modern (as of Python 3.3) import location of
    'MutableMapping' (used in host key management) to avoid the old location
    becoming deprecated in Python 3.8
- Drop hard dependency on pyasn1 as it's only needed for optional GSSAPI
  functionality

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct  9 2018 Paul Howarth <paul@city-fan.org> - 2.4.2-1
- Update to 2.4.2
  - Fix exploit (GH#1283, CVE-2018-1000805) in Paramiko’s server mode (not
    client mode) where hostile clients could trick the server into thinking
    they were authenticated without actually submitting valid authentication
  - Modify protocol message handling such that Transport does not respond to
    MSG_UNIMPLEMENTED with its own MSG_UNIMPLEMENTED; this behavior probably
    didn’t cause any outright errors, but it doesn’t seem to conform to the
    RFCs and could cause (non-infinite) feedback loops in some scenarios
    (usually those involving Paramiko on both ends)
  - Add *.pub files to the MANIFEST so distributed source packages contain
    some necessary test assets (GH#1262)
- Test suite now requires mock ≥ 2.0.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 Miro Hrončok <mhroncok@redhat.com> - 2.4.1-4
- Rebuilt for Python 3.7
- Remove dependency on on pytest-relaxed

* Fri Mar 16 2018 Paul Howarth <paul@city-fan.org> - 2.4.1-1
- Update to 2.4.1
  - Fix a security flaw (GH#1175, CVE-2018-7750) in Paramiko's server mode
    (this does not impact client use) where authentication status was not
    checked before processing channel-open and other requests typically only
    sent after authenticating
  - Ed25519 auth key decryption raised an unexpected exception when given a
    unicode password string (typical in python 3) (GH#1039)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Nov 18 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2.4.0-2
- Add gssapi patch back since 2.4.0 still not compatible
- Add missing BR (lost during merge)

* Fri Nov 17 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0

* Wed Nov 15 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0 (rhbz #1513208)
- Revamp check section

* Sun Oct 29 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2.3.1-3
- Add a patch to disable gssapi on unsupported version (rhbz #1507174)

* Tue Sep 26 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2.3.1-2
- Remove weak deps, paramiko does not support recent gssapi (rhbz #1496148)

* Sat Sep 23 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1 (rhbz #1494764)

* Wed Sep 20 2017 Paul Howarth <paul@city-fan.org> - 2.3.0-1
- 2.3.0.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Paul Howarth <paul@city-fan.org> - 2.2.1-1
- 2.2.1.

* Sun Jun 11 2017 Paul Howarth <paul@city-fan.org> - 2.2.0-1
- 2.2.0.

* Wed Feb 22 2017 Paul Howarth <paul@city-fan.org> - 2.1.2-1
- 2.1.2.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.1.1-2
- Rebuild for Python 3.6

* Fri Dec 16 2016 Jon Ciesla <limburgher@gmail.com> - 2.1.1-1
- 2.1.1.

* Fri Dec 09 2016 Jon Ciesla <limburgher@gmail.com> - 2.1.0-1
- 2.1.0.

* Fri Dec 09 2016 Jon Ciesla <limburgher@gmail.com> - 2.0.2-1
- 2.0.2.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Apr 29 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.0.0-1
- Update to 2.0.0 (RHBZ #1331737)

* Sun Mar 27 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.16.0-1
- Update to 1.16.0
- Adopt to new packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 22 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.15.2-2
- Use %%license
- Move duplicated docs to single doc sub package
- Remove old F-15 conditionals

* Tue Dec 23 2014 Athmane Madjoudj <athmane@fedoraproject.org> 1.15.2-1
- Update to 1.15.2

* Mon Nov 24 2014 Athmane Madjoudj <athmane@fedoraproject.org> 1.15.1-5
- Add conditional to exclude EL since does not have py3

* Sat Nov 15 2014 Athmane Madjoudj <athmane@fedoraproject.org> 1.15.1-4
- py3dir creation should be in prep section

* Fri Nov 14 2014 Athmane Madjoudj <athmane@fedoraproject.org> 1.15.1-3
- Build each pkg in a clean dir

* Fri Nov 14 2014 Athmane Madjoudj <athmane@fedoraproject.org> 1.15.1-2
- Add support for python3
- Add BR -devel for python macros.

* Fri Oct 17 2014 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.15.1-1
- Update to 1.15.1

* Fri Jun 13 2014 Orion Poplawski <orion@cora.nwra.com> - 1.12.4-1
- Update to 1.12.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Orion Poplawski <orion@cora.nwra.com> - 1.12.2-1
- Update to 1.12.2

* Wed Jan 22 2014 Orion Poplawski <orion@cora.nwra.com> - 1.11.3-1
- Update to 1.11.3

* Mon Oct 21 2013 Orion Poplawski <orion@cora.nwra.com> - 1.11.0-1
- Update to 1.11.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May  9 2013 Jeffrey Ollie <jeff@ocjtech.us> - 1.10.1-1
- Update to 1.10.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Jeffrey Ollie <jeff@ocjtech.us> - 1.9.0-1
- Update to 1.9.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul  6 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.7.1-1
- v1.7.7.1 (George) 21may11
- -------------------------
-   * Make the verification phase of SFTP.put optional (Larry Wright)
-   * Patches to fix AIX support (anonymous)
-   * Patch from Michele Bertoldi to allow compression to be turned on in the
-     client constructor.
-   * Patch from Shad Sharma to raise an exception if the transport isn't active
-     when you try to open a new channel.
-   * Stop leaking file descriptors in the SSH agent (John Adams)
-   * More fixes for Windows address family support (Andrew Bennetts)
-   * Use Crypto.Random rather than Crypto.Util.RandomPool
-     (Gary van der Merwe, #271791)
-   * Support for openssl keys (tehfink)
-   * Fix multi-process support by calling Random.atfork (sugarc0de)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 4 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.6-3
- Patch to address deprecation warning from pycrypto
- Simplify build as shown in new python guidelines
- Enable test suite

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Nov  2 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.6-1
- v1.7.6 (Fanny) 1nov09
- ---------------------
-  * fixed bugs 411099 (sftp chdir isn't unicode-safe), 363163 & 411910 (more
-    IPv6 problems on windows), 413850 (race when server closes the channel),
-    426925 (support port numbers in host keys)

* Tue Oct 13 2009 Jeremy Katz <katzj@fedoraproject.org> - 1.7.5-2
- Fix race condition (#526341)

* Thu Jul 23 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.5-1
- v1.7.5 (Ernest) 19jul09
- -----------------------
-  * added support for ARC4 cipher and CTR block chaining (Denis Bernard)
-  * made transport threads daemonize, to fix python 2.6 atexit behavior
-  * support unicode hostnames, and IP6 addresses (Maxime Ripard, Shikhar
-    Bhushan)
-  * various small bug fixes

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.4-4
- Add demos as documentation. BZ#485742

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.7.4-3
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.4-2
- fix license tag

* Sun Jul  6 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.4-1
- Update to 1.7.4

* Mon Mar 24 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.3-1
- Update to 1.7.3.

* Tue Jan 22 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.2-1
- Update to 1.7.2.
- Remove upstreamed patch.

* Mon Jan 14 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-3
- Update to latest Python packaging guidelines.
- Apply patch that fixes insecure use of RandomPool.

* Thu Jul 19 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-2
- Bump rev

* Thu Jul 19 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-1
- Update to 1.7.1

* Sat Dec 09 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 1.6.4-1
- Update to 1.6.4
- Upstream is now shipping tarballs
- Bump for python 2.5 in devel

* Mon Oct  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.2-1
- Update to 1.6.2

* Sat Sep 16 2006 Shahms E. King <shahms@shahms.com> 1.6.1-3
- Rebuild for FC6

* Fri Aug 11 2006 Shahms E. King <shahms@shahms.com> 1.6.1-2
- Include, don't ghost .pyo files per new guidelines

* Tue Aug 08 2006 Shahms E. King <shahms@shahms.com> 1.6.1-1
- Update to new upstream version

* Fri Jun 02 2006 Shahms E. King <shahms@shahms.com> 1.6-1
- Update to new upstream version
- ghost the .pyo files

* Fri May 05 2006 Shahms E. King <shahms@shahms.com> 1.5.4-2
- Fix source line and rebuild

* Fri May 05 2006 Shahms E. King <shahms@shahms.com> 1.5.4-1
- Update to new upstream version

* Wed Apr 12 2006 Shahms E. King <shahms@shahms.com> 1.5.3-1
  - Initial package
