Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package bouncycastle
#
# Copyright (c) 2020 SUSE LLC
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


%global ver  1.66
%global shortver 166
%global gittag r1rv66
%global archivever jdk15on-%{shortver}
%global classname org.bouncycastle.jce.provider.BouncyCastleProvider
Name:           bouncycastle
Version:        %{ver}
Release:        2%{?dist}
Summary:        Bouncy Castle Cryptography APIs for Java
License:        MIT AND Apache-2.0
Group:          Development/Libraries/Java
URL:            https://www.bouncycastle.org
Source0:        https://github.com/bcgit/bc-java/archive/%{gittag}.tar.gz#/%{name}-%{version}.tar.gz
# POMs from Maven Central
Source1:        https://repo1.maven.org/maven2/org/%{name}/bcprov-jdk15on/%{version}/bcprov-jdk15on-%{version}.pom
Source2:        https://repo1.maven.org/maven2/org/%{name}/bcpkix-jdk15on/%{version}/bcpkix-jdk15on-%{version}.pom
Source3:        https://repo1.maven.org/maven2/org/%{name}/bcpg-jdk15on/%{version}/bcpg-jdk15on-%{version}.pom
Source4:        https://repo1.maven.org/maven2/org/%{name}/bcmail-jdk15on/%{version}/bcmail-jdk15on-%{version}.pom
Source5:        https://repo1.maven.org/maven2/org/%{name}/bctls-jdk15on/%{version}/bctls-jdk15on-%{version}.pom
Patch0:         bouncycastle-javadoc.patch
Patch1:         bouncycastle-osgi.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  fdupes
BuildRequires:  javamail
BuildRequires:  javapackages-local-bootstrap
Requires(post): javapackages-tools
Requires(postun): javapackages-tools
Provides:       bcprov = %{version}-%{release}
BuildArch:      noarch

%description
The Bouncy Castle Crypto package is a Java implementation of cryptographic
algorithms. This jar contains JCE provider and lightweight API for the
Bouncy Castle Cryptography APIs for JDK 1.5 to JDK 1.8.

%package pkix
Summary:        Bouncy Castle PKIX, CMS, EAC, TSP, PKCS, OCSP, CMP, and CRMF APIs
License:        MIT
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}

%description pkix
The Bouncy Castle Java APIs for CMS, PKCS, EAC, TSP, CMP, CRMF, OCSP, and
certificate generation. This jar contains APIs for JDK 1.5 to JDK 1.8. The
APIs can be used in conjunction with a JCE/JCA provider such as the one
provided with the Bouncy Castle Cryptography APIs.

%package pg
Summary:        Bouncy Castle OpenPGP API
License:        MIT AND Apache-2.0
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}

%description pg
The Bouncy Castle Java API for handling the OpenPGP protocol. This jar
contains the OpenPGP API for JDK 1.5 to JDK 1.8. The APIs can be used in
conjunction with a JCE/JCA provider such as the one provided with the
Bouncy Castle Cryptography APIs.

%package mail
Summary:        Bouncy Castle S/MIME API
License:        MIT
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}
Requires:       %{name}-pkix = %{version}

%description mail
The Bouncy Castle Java S/MIME APIs for handling S/MIME protocols. This jar
contains S/MIME APIs for JDK 1.5 to JDK 1.8. The APIs can be used in
conjunction with a JCE/JCA provider such as the one provided with the Bouncy
Castle Cryptography APIs. The JavaMail API and the Java activation framework
will also be needed.

%package tls
Summary:        Bouncy Castle JSSE provider and TLS/DTLS API
License:        MIT
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}

%description tls
The Bouncy Castle Java APIs for TLS and DTLS, including a provider for the
JSSE.

%package javadoc
Summary:        Javadoc for %{name}
License:        MIT
Group:          Development/Libraries/Java

%description javadoc
API documentation for the Bouncy Castle Cryptography APIs.

%prep
%setup -q -n bc-java-%{gittag}
%patch0 -p1
%patch1 -p1

# Remove provided binaries
find . -type f -name "*.class" -exec rm -f {} \;
find . -type f -name "*.jar" -exec rm -f {} \;

%build
echo "package.version:\ %{version}" >> bc-build.properties
echo "bundle.version:\ %{version}.0" >> bc-build.properties
ant -f ant/jdk15+.xml \
  -Dbc.javac.source=6 -Dbc.javac.target=6 \
  -Djunit.jar.home=$(build-classpath junit) \
  -Dmail.jar.home=$(build-classpath javax.mail) \
  -Dactivation.jar.home= \
  -Drelease.debug=true \
  clean build-provider build

# Not shipping the "lcrypto" jar, so don't ship the javadoc for it
rm -rf build/artifacts/jdk1.5/javadoc/lcrypto

%install
install -dm 755 %{buildroot}%{_sysconfdir}/java/security/security.d
touch %{buildroot}%{_sysconfdir}/java/security/security.d/2000-%{classname}

install -dm 0755 %{buildroot}%{_javadir}
install -dm 0755 %{buildroot}%{_mavenpomdir}
for bc in bcprov bcpkix bcpg bcmail bctls ; do
  install -pm 0644 build/artifacts/jdk1.5/jars/$bc-%{archivever}.jar %{buildroot}%{_javadir}/$bc.jar
  install -pm 0644 %{_sourcedir}/$bc-jdk15on-%{version}.pom %{buildroot}%{_mavenpomdir}/$bc.pom
  %add_maven_depmap $bc.pom $bc.jar -a "org.bouncycastle:$bc-jdk16,org.bouncycastle:$bc-jdk15" -f $bc
done

install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -r build/artifacts/jdk1.5/javadoc/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%post
{
  # Rebuild the list of security providers in classpath.security
  suffix=security/classpath.security
  secfiles="%{_prefix}/lib/$suffix %{_prefix}/lib64/$suffix"

  for secfile in $secfiles
  do
    # check if this classpath.security file exists
    [ -f "$secfile" ] || continue

    sed -i '/^security\.provider\./d' "$secfile"

    count=0
    for provider in $(ls %{_sysconfdir}/java/security/security.d)
    do
      count=$((count + 1))
      echo "security.provider.${count}=${provider#*-}" >> "$secfile"
    done
  done
} || :

%postun
if [ $1 -eq 0 ] ; then

  {
    # Rebuild the list of security providers in classpath.security
    suffix=security/classpath.security
    secfiles="%{_prefix}/lib/$suffix %{_prefix}/lib64/$suffix"

    for secfile in $secfiles
    do
      # check if this classpath.security file exists
      [ -f "$secfile" ] || continue

      sed -i '/^security\.provider\./d' "$secfile"

      count=0
      for provider in $(ls %{_sysconfdir}/java/security/security.d)
      do
        count=$((count + 1))
        echo "security.provider.${count}=${provider#*-}" >> "$secfile"
      done
    done
  } || :

fi

%files -f .mfiles-bcprov
%license build/artifacts/jdk1.5/bcprov-jdk15on-*/LICENSE.html
%doc docs/ core/docs/ *.html
%config(noreplace) %{_sysconfdir}/java/security/security.d/2000-%{classname}

%files pkix -f .mfiles-bcpkix
%license build/artifacts/jdk1.5/bcpkix-jdk15on-*/LICENSE.html

%files pg -f .mfiles-bcpg
%license build/artifacts/jdk1.5/bcpg-jdk15on-*/LICENSE.html

%files mail -f .mfiles-bcmail
%license build/artifacts/jdk1.5/bcmail-jdk15on-*/LICENSE.html

%files tls -f .mfiles-bctls
%license build/artifacts/jdk1.5/bctls-jdk15on-*/LICENSE.html

%files javadoc
%{_javadocdir}/%{name}
%license LICENSE.html

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.66-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.66-1.3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Jul 28 2020 Pedro Monreal <pmonreal@suse.com>
- Version update to 1.66
  * Defects Fixed:
  - EdDSA verifiers now reset correctly after rejecting overly long signatures.
  - BCJSSE: SSLSession.getPeerCertificateChain could throw NullPointerException.
  - qTESLA-I verifier would reject some valid signatures.
  - qTESLA verifiers now reject overly long signatures.
  - PGP regression caused failure to preserve existing version header when
    headers were reset.
  - PKIXNameConstraintValidator had a bad cast preventing use of multiple
    OtherName constraints.
  - Serialisation of the non-CRT RSA Private Key could cause a NullPointerException.
  - An extra 4 bytes was included in the start of HSS public key encodings.
  - CMS with Ed448 using a direct signature was using id-shake256-len
    rather than id-shake256.
  - Use of GCMParameterSpec could cause an AccessControlException under
    some circumstances.
  - DTLS: Fixed high-latency HelloVerifyRequest handshakes.
  - An encoding bug for rightEncoded() in KMAC has been fixed.
  - For a few values the cSHAKE implementation would add unnecessary pad bytes
    where the N and S strings produced encoded data that was block aligned.
  - There were a few circumstances where Argon2BytesGenerator might hit an
    unexpected null. These have been removed.
  * Additional Features and Functionality
  - The qTESLA signature algorithm has been updated to v2.8 (20191108).
  - BCJSSE: Client-side OCSP stapling now supports status_request_v2 extension.
  - Support has been added for "ocsp.enable", "ocsp.responderURL" and
    PKIXRevocationChecker for users of Java 8 and later.
  - Support has been added for "org.bouncycastle.x509.enableCRLDP" to the PKIX validator.
  - BCJSSE: Now supports system property 'jsse.enableFFDHE'
  - BCJSSE: Now supports system properties 'jdk.tls.client.SignatureSchemes'
    and 'jdk.tls.server.SignatureSchemes'.
  - Multi-release support has been added for Java 11 XECKeys.
  - Multi-release support has been added for Java 15 EdECKeys.
  - The MiscPEMGenerator will now output general PrivateKeyInfo structures.
  - A new property "org.bouncycastle.pkcs8.v1_info_only" has been added to
    make the provider only produce version 1 PKCS8 PrivateKeyInfo structures.
  - The PKIX CertPathBuilder will now take the target certificate from the target
    constraints if a specific certificate is given to the selector.
  - BCJSSE: A range of ARIA and CAMELLIA cipher suites added to supported list.
  - BCJSSE: Now supports the PSS signature schemes from RFC 8446 (TLS 1.2 onwards).
  - Performance of the Base64 encoder has been improved.
  - The PGPPublicKey class will now include direct key signatures when checking
    for key expiry times.
  * NOTES:
  - The qTESLA update breaks compatibility with previous versions.
    Private keys now include a hash of the public key at the end,
    and signatures are no longer interoperable with previous versions.
* Wed Apr 29 2020 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Version update to 1.65
  * Defects Fixed:
  - DLExternal would encode using DER encoding for tagged SETs.
  - ChaCha20Poly1305 could fail for large (>~2GB) files.
  - ChaCha20Poly1305 could fail for small updates when used via the provider.
  - Properties.getPropertyValue could ignore system property when other
    local overrides set.
  - The entropy gathering thread was not running in daemon mode, meaning there
    could be a delay in an application shutting down due to it.
  - A recent change in Java 11 could cause an exception with the BC Provider's
    implementation of PSS.
  - BCJSSE: TrustManager now tolerates having no trusted certificates.
  - BCJSSE: Choice of credentials and signing algorithm now respect the peer's
    signature_algorithms extension properly.
  - BCJSSE: KeyManager for KeyStoreBuilderParameters no longer leaks memory.
  * Additional Features and Functionality:
  - LMS and HSS (RFC 8554) support has been added to the low level library and
    the PQC provider.
  - SipHash128 support has been added to the low level library and the JCE provider.
  - BCJSSE: BC API now supports explicitly specifying the session to resume.
  - BCJSSE: Ed25519, Ed448 are now supported when TLS 1.2 or higher is
    negotiated (except in FIPS mode).
  - BCJSSE: Added support for extended_master_secret system properties:
    jdk.tls.allowLegacyMasterSecret, jdk.tls.allowLegacyResumption,
    jdk.tls.useExtendedMasterSecret .
  - BCJSSE: Ed25519, Ed448 are now supported when TLS 1.2 or higher is
    negotiated (except in FIPS mode).
  - BCJSSE: KeyManager and TrustManager now check algorithm constraints for
    keys and certificate chains.
  - BCJSSE: KeyManager selection of server credentials now prefers matching
    SNI hostname (if any).
  - BCJSSE: KeyManager may now fallback to imperfect credentials (expired,
    SNI mismatch).
  - BCJSSE: Client-side OCSP stapling support (beta version: via status_request
    extension only, provides jdk.tls.client.enableStatusRequestExtension, and
    requires CertPathBuilder support).
  - TLS: DSA in JcaTlsCrypto now falls back to stream signing to work around
    NoneWithDSA limitations in default provider.
* Wed Mar 25 2020 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * bouncycastle-osgi.patch
    + Add OSGi manifests to the distributed jars so that they can
    be used from eclipse
* Wed Nov  6 2019 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Fix arch dependent macros in noarch package [bsc#1109539]
* Sat Oct 12 2019 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Update pom files with those from Maven repository.
* Thu Oct 10 2019 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Version update to 1.64 [bsc#1153385, CVE-2019-17359]
  [bsc#1096291, CVE-2018-1000180][bsc#1100694, CVE-2018-1000613]
  * Security Advisory:
  - CVE-2019-17359: A change to the ASN.1 parser in 1.63 introduced
    a regression that can cause an OutOfMemoryError to occur on
    parsing ASN.1 data.
  * Defects Fixed:
  - OpenSSH: Fixed padding in generated Ed25519 private keys.
  - GOST3410-2012-512 now uses the GOST3411-2012-256 as its KDF digest.
  - Validation of headers in PemReader now looks for tailing dashes in header.
  - Some compatibility issues around the signature encryption algorithm
    field in CMS SignedData and the GOST algorithms have been addressed.
  * Additional Features and Functionality:
  - PKCS12 key stores containing only certificates can now be created
    without the need to provide passwords.
  - BCJSSE: Initial support for AlgorithmConstraints; protocol versions
    and cipher suites.
  - BCJSSE: Initial support for 'jdk.tls.disabledAlgorithms'; protocol
    versions and cipher suites.
  - BCJSSE: Add SecurityManager check to access session context.
  - BCJSSE: Improved SunJSSE compatibility of the NULL_SESSION.
  - BCJSSE: SSLContext algorithms updated for SunJSSE compatibility
    (default enabled protocols).
  - The digest functions Haraka-256 and Haraka-512 have been added to
    the provider and the light-weight API
  - XMSS/XMSS^MT key management now allows for allocating subsets of the
    private key space using the extraKeyShard() method. Use of
    StateAwareSignature is now deprecated.
  - Support for Java 11's NamedParameterSpec class has been added
    (using reflection) to the EC and EdEC KeyPairGenerator implementations.
* Thu Oct 10 2019 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Version update to 1.63
  * Defects Fixed:
  - The ASN.1 parser would throw a large object exception for some objects
    which could be safely parsed.
  - GOST3412-2015 CTR mode was unusable at the JCE level.
  - The DSTU MACs were failing to reset fully on doFinal().
  - The DSTU MACs would throw an exception if the key was a multiple of the
    size as the MAC's underlying buffer size.
  - EdEC and QTESLA were not previously usable with the post Java 9 module structure.
  - ECNR was not correctly bounds checking the input and could produce invalid signatures.
  - ASN.1: Enforce no leading zeroes in OID branches (longer than 1 character).
  - TLS: Fix X448 support in JcaTlsCrypto.
  - Fixed field reduction for secp128r1 custom curve.
  - Fixed unsigned multiplications in X448 field squaring.
  - Some issues over subset Name Constraint validation in the CertPath analyser
  - TimeStampResponse.getEncoded() could throw an exception if the TimeStampToken was null.
  - Unnecessary memory usage in the ARGON2 implementation has been removed.
  - Param-Z in the GOST-28147 algorithm was not resolving correctly.
  - It is now possible to specify different S-Box parameters for the GOST 28147-89 MAC.
  * Additional Features and Functionality:
  - QTESLA is now updated with the round 2 changes. Note: the security catergories,
    and in some cases key generation and signatures, have changed. The round 1 version is
    now moved to org.bouncycastle.pqc.crypto.qteslarnd1, this package will be deleted in
    1.64. Please keep in mind that QTESLA may continue to evolve.
  - Support has been added for generating Ed25519/Ed448 signed certificates.
  - A method for recovering the message/digest value from an ECNR signature has been added.
  - Support for the ZUC-128 and ZUC-256 ciphers and MACs has been added to the provider
    and the lightweight API.
  - Support has been added for ChaCha20-Poly1305 AEAD mode from RFC 7539.
  - Improved performance for multiple ECDSA verifications using same public key.
  - Support for PBKDF2withHmacSM3 has been added to the BC provider.
  - The S/MIME API has been fixed to avoid unnecessary delays due to DNS resolution of a
    hosts name in internal MimeMessage preparation.
  - The valid path for EST services has been updated to cope with the characters used in
    the Aruba clearpass EST implementation.
- Version update to 1.62
  * Defects Fixed:
  - DTLS: Fixed infinite loop on IO exceptions.
  - DTLS: Retransmission timers now properly apply to flights monolithically.
  - BCJSSE: setEnabledCipherSuites ignores unsupported cipher suites.
  - BCJSSE: SSLSocket implementations store passed-in 'host' before connecting.
  - BCJSSE: Handle SSLEngine closure prior to handshake.
  - BCJSSE: Provider now configurable using security config under Java 11 and later.
  - EdDSA verifiers now reject overly long signatures.
  - XMSS/XMSS^MT OIDs now using the values defined in RFC 8391.
  - XMSS/XMSS^MT keys now encoded with OID at start.
  - An error causing valid paths to be rejected due to DN based name constraints
    has been fixed in the CertPath API.
  - Name constraint resolution now includes special handling of serial numbers.
  - Cipher implementations now handle ByteBuffer usage where the ByteBuffer has
    no backing array.
  - CertificateFactory now enforces presence of PEM headers when required.
  - A performance issue with RSA key pair generation that was introduced in 1.61
    has been mostly eliminated.
  * Additional Features and Functionality:
  - Builders for X509 certificates and CRLs now support replace and remove extension methods.
  - DTLS: Added server-side support for HelloVerifyRequest.
  - DTLS: Added support for an overall handshake timeout.
  - DTLS: Added support for the heartbeat extension (RFC 6520).
  - DTLS: Improve record seq. behaviour in HelloVerifyRequest scenarios.
  - TLS: BasicTlsPSKIdentity now reusable (returns cloned array from getPSK).
  - BCJSSE: Improved ALPN support, including selectors from Java 9.
  - Lightweight RSADigestSigner now support use of NullDigest.
  - SM2Engine now supports C1C3C2 mode.
  - SHA256withSM2 now added to provider.
  - BCJSSE: Added support for ALPN selectors (including in BC extension API for earlier JDKs).
  - BCJSSE: Support 'SSL' algorithm for SSLContext (alias for 'TLS').
  - The BLAKE2xs XOF has been added to the lightweight API.
  - Utility classes added to support journaling of SecureRandom and algorithms to allow
    persistance and later resumption.
  - PGP SexprParser now handles some unprotected key types.
  - NONEwithRSA support added to lightweight RSADigestSigner.
  - Support for the Ethereum flavor of IES has been added to the lightweight API.
- Version update to 1.61
  * Defects Fixed:
  - Use of EC named curves could be lost if keys were constructed.
    via a key factory and algorithm parameters.
  - RFC3211WrapEngine would not properly handle messages longer than 127 bytes.
  - The JCE implementations for RFC3211 would not return null AlgorithmParameters.
  - TLS: Don't check CCS status for hello_request.
  - TLS: Tolerate unrecognized hash algorithms.
  - TLS: Tolerate unrecognized SNI types.
  - Incompatibility issue in ECIES-KEM encryption in cofactor fixed.
  - Issue with XMSS/XMSSMT private key loading which could result in invalid signatures fixed.
  - StateAwareSignature.isSigningCapable() now returns false when the
    key has reached it's maximum number of signatures.
  - The McEliece KeyPairGenerator was failing to initialize the underlying
    class if a SecureRandom was explicitly passed.
  - The McEliece cipher would sometimes report the wrong value on a call
    to Cipher.getOutputSize(int).
  - CSHAKEDigest.leftEncode() was using the wrong endianness for multi byte values.
  - Some ciphers, such as CAST6, were missing AlgorithmParameters implementations.
  - An issue with the default "m" parameter for 1024 bit Diffie-Hellman keys which
    could result in an exception on key pair generation has been fixed.
  - The SPHINCS256 implementation is now more tolerant of parameters wrapped with a
    SecureRandom and will not throw an exception if it receives one.
  - A regression in PGPUtil.writeFileToLiteralData() which could cause corrupted
    literal data has been fixed.
  - Several parsing issues related to the processing of CMP PKIPublicationInfo.
  - The ECGOST curves for id-tc26-gost-3410-12-256-paramSetA and
    id-tc26-gost-3410-12-512-paramSetC had incorrect co-factors.
  * Additional Features and Functionality:
  - The qTESLA signature algorithm has been added to PQC light-weight API and the PQC provider.
  - The password hashing function, Argon2 has been added to the lightweight API.
  - BCJSSE: Added support for endpoint ID validation (HTTPS, LDAP, LDAPS).
  - BCJSSE: Added support for 'useCipherSuitesOrder' parameter.
  - BCJSSE: Added support for ALPN.
  - BCJSSE: Various changes for improved compatibility with SunJSSE.
  - BCJSSE: Provide default extended key/trust managers.
  - TLS: Added support for TLS 1.2 features from RFC 8446.
  - TLS: Removed support for EC point compression.
  - TLS: Removed support for record compression.
  - TLS: Updated to RFC 7627 from draft-ietf-tls-session-hash-04.
  - TLS: Improved certificate sig. alg. checks.
  - TLS: Finalised support for RFC 8442 cipher suites.
  - Support has been added to the main Provider for the Ed25519 and Ed448 signature algorithms.
  - Support has been added to the main Provider for the X25519 and X448 key agreement algorithms.
  - Utility classes have been added for handling OpenSSH keys.
  - Support for processing messages built using GPG and Curve25519 has been added to the OpenPGP API.
  - The provider now recognises the standard SM3 OID.
  - A new API for directly parsing and creating S/MIME documents has been added to the PKIX API.
  - SM2 in public key cipher mode has been added to the provider API.
  - The BCFKSLoadStoreParameter has been extended to allow the use of certificates and digital
    signatures for verifying the integrity of BCFKS key stores.
* Tue Sep 24 2019 Fridrich Strba <fstrba@suse.com>
- Package also the bcpkix bcpg bcmail bctls artifacts in separate
  sub-packages
- Revert to building with source/target 6, since it is still
  possible
- Added patch:
  * bouncycastle-javadoc.patch
    + fix javadoc build
* Thu Jul 19 2018 tchvatal@suse.com
- Version update to 1.60 bsc#1100694:
  * CVE-2018-1000613 Use of Externally-ControlledInput to Select Classes or Code
  * CVE-2018-1000180: issue around primality tests for RSA key pair generation
    if done using only the low-level API [bsc#1096291]
  * Release notes:
    http://www.bouncycastle.org/releasenotes.html
* Mon Jun 11 2018 abergmann@suse.com
- Version update to 1.59:
  * CVE-2017-13098: Fix against Bleichenbacher oracle when not
    using the lightweight APIs (boo#1072697).
  * CVE-2016-1000338: Fix DSA ASN.1 validation during encoding of
    signature on verification (boo#1095722).
  * CVE-2016-1000339: Fix AESEngine key information leak via lookup
    table accesses (boo#1095853).
  * CVE-2016-1000340: Fix carry propagation bugs in the
    implementation of squaring for several raw math classes
    (boo#1095854).
  * CVE-2016-1000341: Fix DSA signature generation vulnerability to
    timing attack (boo#1095852).
  * CVE-2016-1000342: Fix ECDSA ASN.1 validation during encoding of
    signature on verification (boo#1095850).
  * CVE-2016-1000343: Fix week default settings for private DSA key
    pair generation (boo#1095849).
  * CVE-2016-1000344: Remove DHIES from the provider to disable the
    unsafe usage of ECB mode (boo#1096026).
  * CVE-2016-1000345: Fix DHIES/ECIES CBC mode padding oracle
    attack (boo#1096025).
  * CVE-2016-1000346: Fix other party DH public key validation
    (boo#1096024).
  * CVE-2016-1000352: Remove ECIES from the provider to disable the
    unsafe usage of ECB mode (boo#1096022).
  * Release notes:
    http://www.bouncycastle.org/releasenotes.html
- Removed patch:
  * ambiguous-reseed.patch
* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
* Fri Sep 15 2017 fstrba@suse.com
- Version update to 1.58
- Added patch:
  * ambiguous-reseed.patch
    + Upstream fix for an ambiguous overload
* Thu Sep  7 2017 fstrba@suse.com
- Set java source and target to 1.6 to allow building with jdk9
* Fri May 19 2017 pcervinka@suse.com
- New build dependency: javapackages-local
- Fixed requires
- Spec file cleaned
* Sat Feb 20 2016 tchvatal@suse.com
- Version update to 1.54:
  * No obvious changelog to be found
  * Fixes bnc#967521 CVE-2015-7575
* Fri Oct 23 2015 tchvatal@suse.com
- Version update to 1.53 (latest upstream)
  * No obvious changelog
  * Fixes bnc#951727 CVE-2015-7940
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Fri Feb 20 2015 tchvatal@suse.com
- Disable tests on obs as they hang
* Tue Feb 10 2015 tchvatal@suse.com
- Version bump to 1.50 to match Fedora
- Cleanup with spec-cleaner
* Mon Jul  7 2014 tchvatal@suse.com
- Depend on junit not junit4
* Thu May 15 2014 darin@darins.net
- disable bytecode check on sle_11
* Thu Nov 14 2013 mvyskocil@suse.com
- Don't own /etc/java/security to not clash with javapackages-tools
- Don't mark random files as config
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Wed Aug 28 2013 mvyskocil@suse.com
- use add_maven_depmap from recent javapackages-tools
- temporary mozilla-nss to BT: in order to pass a tests
* Fri May 18 2012 mvyskocil@suse.cz
- bumb target to 1.6
* Mon Jan 16 2012 mvyskocil@suse.cz
- Initial packaging for SUSE
  from Fedora's bouncycastle 1.46
