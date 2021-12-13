Vendor:         Microsoft Corporation
Distribution:   Mariner
%global build_api_doc 1

Name:           python-nss
Version:        1.0.1
Release:        19%{?dist}
Summary:        Python bindings for Network Security Services (NSS)

License:        MPLv2.0 or GPLv2+ or LGPLv2+
URL:            https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS/Python_binding_for_NSS
Source0:        https://ftp.mozilla.org/pub/mozilla.org/security/python-nss/releases/PYNSS_RELEASE_1_0_1/src/python-nss-%{version}.tar.bz2

Patch1: sphinx.patch

%global docdir %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}

# we don't want to provide private python extension libs in python3 dirs
%global __provides_exclude_from ^(%{python3_sitearch})/.*\\.so$

BuildRequires: gcc
BuildRequires: nspr-devel
BuildRequires: nss-devel
BuildRequires: python3-devel
BuildRequires: python3-sphinx

%global _description\
This package provides Python bindings for Network Security Services\
(NSS) and the Netscape Portable Runtime (NSPR).\
\
NSS is a set of libraries supporting security-enabled client and\
server applications. Applications built with NSS can support SSL v2\
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3\
certificates, and other security standards. Specific NSS\
implementations have been FIPS-140 certified.

%description %_description

%package -n python3-nss

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-sphinx

%{?python_provide:%python_provide python3-nss}

Summary: Python3 bindings for Network Security Services (NSS)

%description -n python3-nss %_description

%package doc
Summary: API documentation and examples

%description doc
API documentation and examples

%prep
%setup -q
%patch1 -p1

%build
%py3_build

%if %{build_api_doc}
%{__python3} setup.py build_doc
%endif


%install
%py3_install
%{__python3} setup.py install_doc --docdir %{docdir} --skip-build --root $RPM_BUILD_ROOT

# Remove execution permission from any example/test files in docdir
find $RPM_BUILD_ROOT/%{docdir} -type f | xargs chmod a-x

# Set correct permissions on .so files
chmod 0755 $RPM_BUILD_ROOT/%{python3_sitearch}/nss/*.so

%files -n python3-nss
%{python3_sitearch}/*
%doc %{docdir}/ChangeLog
%doc %{docdir}/LICENSE.gpl
%doc %{docdir}/LICENSE.lgpl
%doc %{docdir}/LICENSE.mpl
%doc %{docdir}/README

%files doc
%doc %{docdir}/examples
%doc %{docdir}/test
%if %{build_api_doc}
%doc %{docdir}/api
%endif

%changelog
* Fri Jul 23 2021 Thomas Crain <thcrain@microsoft.com> - 1.0.1-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove python2 support, build with python3 by default

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-17
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-16
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018  <jdennis@redhat.com> - 1.0.1-12
- add gcc as a build requirement

* Fri Jul  6 2018  <jdennis@redhat.com> - 1.0.1-11
- Move documentation generator from epydoc to Sphinx autodoc
- Modify py2/py3 build logic to comply with new guidelines

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-10
- Rebuilt for Python 3.7

* Mon May 14 2018  <jdennis@redhat.com> - 1.0.1-9
- rebuild due to missing changelog entry

* Mon May 14 2018  <jdennis@redhat.com> - 1.0.1-8
- update URL tag and SOURCE0 to current upstream URL's

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.0.1-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.1-5
- Python 2 binary package renamed to python2-nss
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.0.1-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Tue Feb 28 2017 John Dennis <jdennis@redhat.com> - 1.0.1-1
  * Add TLS 1.3 cipher suites.

  * ssl_cipher_info.py now attempts to enable TLS 1.3.

  * Fix build issue in setup.py. python-nss can now be build
    as Python wheel, e.g. `pip wheel -w dist .`

  * The following constants were added:

    - ssl.TLS_AES_128_GCM_SHA256
    - ssl.TLS_AES_256_GCM_SHA384
    - ssl.TLS_CHACHA20_POLY1305_SHA256

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-3
- Rebuild for Python 3.6

* Tue Sep 27 2016 John Dennis <jdennis@redhat.com> - 1.0.0-2
- remove reference to unused tls_chacha20-poly1305-constants.patch

* Thu Sep  1 2016 John Dennis <jdennis@redhat.com> - 1.0.0-1
- Offical 1.0.0 release, only minor tweaks from 1.0.0beta1

- Allow custom include root in setup.py as command line arg

- Remove checks for whether a socket is open for reading. It's not
  possible for the binding to know in all cases, especially if the
  socket is created from an external socket passed in.

  * The following module functions were added:
      - nss.get_all_tokens

* Mon Aug 15 2016 John Dennis <jdennis@redhat.com> - 1.0.0-beta1.2.3
- add tls chacha20 poly1305 constants

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-beta1.2.2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-beta1.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-beta1.2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Nov  6 2015 John Dennis <jdennis@redhat.com> - 1.0.0-beta1.1
- Resolves: bug #985290 Port to Python3
- Upgrade to upstream 1.0.0-beta1
  python-nss now supports both Py2 and Py3, see ChangeLog for details
  When built for Py2:
   - text will be a Unicode object
   - binary data will be a str object
   - ints will be Python long object
  When built for Py3:
   - text will be a str object
   - binary data will be a bytes object
   - ints will be a Python int object

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 28 2014 John Dennis <jdennis@redhat.com> - 0.16.0-0
  The primary enhancements in this version is adding support for the
  setting trust attributes on a Certificate, the SSL version range API,
  information on the SSL cipher suites and information on the SSL connection.

  * The following module functions were added:

    - ssl.get_ssl_version_from_major_minor
    - ssl.get_default_ssl_version_range
    - ssl.get_supported_ssl_version_range
    - ssl.set_default_ssl_version_range
    - ssl.ssl_library_version_from_name
    - ssl.ssl_library_version_name
    - ssl.get_cipher_suite_info
    - ssl.ssl_cipher_suite_name
    - ssl.ssl_cipher_suite_from_name

  * The following deprecated module functions were removed:

    - ssl.nssinit
    - ssl.nss_ini
    - ssl.nss_shutdown

  * The following classes were added:

    - SSLCipherSuiteInfo
    - SSLChannelInfo

  * The following class methods were added:

    - Certificate.trust_flags
    - Certificate.set_trust_attributes

    - SSLSocket.set_ssl_version_range
    - SSLSocket.get_ssl_version_range
    - SSLSocket.get_ssl_channel_info
    - SSLSocket.get_negotiated_host
    - SSLSocket.connection_info_format_lines
    - SSLSocket.connection_info_format
    - SSLSocket.connection_info_str
	
    - SSLCipherSuiteInfo.format_lines
    - SSLCipherSuiteInfo.format

    - SSLChannelInfo.format_lines
    - SSLChannelInfo.format

  * The following class properties were added:

    - Certificate.ssl_trust_flags
    - Certificate.email_trust_flags
    - Certificate.signing_trust_flags

    - SSLCipherSuiteInfo.cipher_suite
    - SSLCipherSuiteInfo.cipher_suite_name
    - SSLCipherSuiteInfo.auth_algorithm
    - SSLCipherSuiteInfo.auth_algorithm_name
    - SSLCipherSuiteInfo.kea_type
    - SSLCipherSuiteInfo.kea_type_name
    - SSLCipherSuiteInfo.symmetric_cipher
    - SSLCipherSuiteInfo.symmetric_cipher_name
    - SSLCipherSuiteInfo.symmetric_key_bits
    - SSLCipherSuiteInfo.symmetric_key_space
    - SSLCipherSuiteInfo.effective_key_bits
    - SSLCipherSuiteInfo.mac_algorithm
    - SSLCipherSuiteInfo.mac_algorithm_name
    - SSLCipherSuiteInfo.mac_bits
    - SSLCipherSuiteInfo.is_fips
    - SSLCipherSuiteInfo.is_exportable
    - SSLCipherSuiteInfo.is_nonstandard

    - SSLChannelInfo.protocol_version
    - SSLChannelInfo.protocol_version_str
    - SSLChannelInfo.protocol_version_enum
    - SSLChannelInfo.major_protocol_version
    - SSLChannelInfo.minor_protocol_version
    - SSLChannelInfo.cipher_suite
    - SSLChannelInfo.auth_key_bits
    - SSLChannelInfo.kea_key_bits
    - SSLChannelInfo.creation_time
    - SSLChannelInfo.creation_time_utc
    - SSLChannelInfo.last_access_time
    - SSLChannelInfo.last_access_time_utc
    - SSLChannelInfo.expiration_time
    - SSLChannelInfo.expiration_time_utc
    - SSLChannelInfo.compression_method
    - SSLChannelInfo.compression_method_name
    - SSLChannelInfo.session_id

  * The following files were added:

    - doc/examples/cert_trust.py
    - doc/examples/ssl_version_range.py

  * The following constants were added:
    - nss.CERTDB_TERMINAL_RECORD
    - nss.CERTDB_VALID_PEER
    - nss.CERTDB_TRUSTED
    - nss.CERTDB_SEND_WARN
    - nss.CERTDB_VALID_CA
    - nss.CERTDB_TRUSTED_CA
    - nss.CERTDB_NS_TRUSTED_CA
    - nss.CERTDB_USER
    - nss.CERTDB_TRUSTED_CLIENT_CA
    - nss.CERTDB_GOVT_APPROVED_CA
    - ssl.SRTP_AES128_CM_HMAC_SHA1_32
    - ssl.SRTP_AES128_CM_HMAC_SHA1_80
    - ssl.SRTP_NULL_HMAC_SHA1_32
    - ssl.SRTP_NULL_HMAC_SHA1_80
    - ssl.SSL_CK_DES_192_EDE3_CBC_WITH_MD5
    - ssl.SSL_CK_DES_64_CBC_WITH_MD5
    - ssl.SSL_CK_IDEA_128_CBC_WITH_MD5
    - ssl.SSL_CK_RC2_128_CBC_EXPORT40_WITH_MD5
    - ssl.SSL_CK_RC2_128_CBC_WITH_MD5
    - ssl.SSL_CK_RC4_128_EXPORT40_WITH_MD5
    - ssl.SSL_CK_RC4_128_WITH_MD5
    - ssl.SSL_FORTEZZA_DMS_WITH_FORTEZZA_CBC_SHA
    - ssl.SSL_FORTEZZA_DMS_WITH_NULL_SHA
    - ssl.SSL_FORTEZZA_DMS_WITH_RC4_128_SHA
    - ssl.SSL_RSA_OLDFIPS_WITH_3DES_EDE_CBC_SHA
    - ssl.SSL_RSA_OLDFIPS_WITH_DES_CBC_SHA
    - ssl.TLS_DHE_DSS_EXPORT_WITH_DES40_CBC_SHA
    - ssl.TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA
    - ssl.TLS_DHE_DSS_WITH_AES_128_GCM_SHA256
    - ssl.TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA
    - ssl.TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA
    - ssl.TLS_DHE_DSS_WITH_DES_CBC_SHA
    - ssl.TLS_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA
    - ssl.TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA
    - ssl.TLS_DHE_RSA_WITH_AES_128_CBC_SHA256
    - ssl.TLS_DHE_RSA_WITH_AES_128_GCM_SHA256
    - ssl.TLS_DHE_RSA_WITH_AES_256_CBC_SHA256
    - ssl.TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA
    - ssl.TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA
    - ssl.TLS_DHE_RSA_WITH_DES_CBC_SHA
    - ssl.TLS_DH_ANON_WITH_CAMELLIA_128_CBC_SHA
    - ssl.TLS_DH_ANON_WITH_CAMELLIA_256_CBC_SHA
    - ssl.TLS_DH_DSS_EXPORT_WITH_DES40_CBC_SHA
    - ssl.TLS_DH_DSS_WITH_3DES_EDE_CBC_SHA
    - ssl.TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA
    - ssl.TLS_DH_DSS_WITH_CAMELLIA_256_CBC_SHA
    - ssl.TLS_DH_DSS_WITH_DES_CBC_SHA
    - ssl.TLS_DH_RSA_EXPORT_WITH_DES40_CBC_SHA
    - ssl.TLS_DH_RSA_WITH_3DES_EDE_CBC_SHA
    - ssl.TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA
    - ssl.TLS_DH_RSA_WITH_CAMELLIA_256_CBC_SHA
    - ssl.TLS_DH_RSA_WITH_DES_CBC_SHA
    - ssl.TLS_DH_anon_EXPORT_WITH_DES40_CBC_SHA
    - ssl.TLS_DH_anon_EXPORT_WITH_RC4_40_MD5
    - ssl.TLS_DH_anon_WITH_3DES_EDE_CBC_SHA
    - ssl.TLS_DH_anon_WITH_AES_128_CBC_SHA
    - ssl.TLS_DH_anon_WITH_AES_256_CBC_SHA
    - ssl.TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA
    - ssl.TLS_DH_anon_WITH_CAMELLIA_256_CBC_SHA
    - ssl.TLS_DH_anon_WITH_DES_CBC_SHA
    - ssl.TLS_DH_anon_WITH_RC4_128_MD5
    - ssl.TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
    - ssl.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
    - ssl.TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
    - ssl.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
    - ssl.TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256
    - ssl.TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256
    - ssl.TLS_EMPTY_RENEGOTIATION_INFO_SCSV
    - ssl.TLS_FALLBACK_SCSV
    - ssl.TLS_NULL_WITH_NULL_NULL
    - ssl.TLS_RSA_EXPORT_WITH_DES40_CBC_SHA
    - ssl.TLS_RSA_EXPORT_WITH_RC2_CBC_40_MD5
    - ssl.TLS_RSA_EXPORT_WITH_RC4_40_MD5
    - ssl.TLS_RSA_WITH_3DES_EDE_CBC_SHA
    - ssl.TLS_RSA_WITH_AES_128_CBC_SHA256
    - ssl.TLS_RSA_WITH_AES_128_GCM_SHA256
    - ssl.TLS_RSA_WITH_AES_256_CBC_SHA256
    - ssl.TLS_RSA_WITH_CAMELLIA_128_CBC_SHA
    - ssl.TLS_RSA_WITH_CAMELLIA_256_CBC_SHA
    - ssl.TLS_RSA_WITH_DES_CBC_SHA
    - ssl.TLS_RSA_WITH_IDEA_CBC_SHA
    - ssl.TLS_RSA_WITH_NULL_MD5
    - ssl.TLS_RSA_WITH_NULL_SHA
    - ssl.TLS_RSA_WITH_NULL_SHA256
    - ssl.TLS_RSA_WITH_RC4_128_MD5
    - ssl.TLS_RSA_WITH_RC4_128_SHA
    - ssl.TLS_RSA_WITH_SEED_CBC_SHA
    - ssl.SSL_VARIANT_DATAGRAM
    - ssl.SSL_VARIANT_STREAM
    - ssl.SSL_LIBRARY_VERSION_2
    - ssl.SSL_LIBRARY_VERSION_3_0
    - ssl.SSL_LIBRARY_VERSION_TLS_1_0
    - ssl.SSL_LIBRARY_VERSION_TLS_1_1
    - ssl.SSL_LIBRARY_VERSION_TLS_1_2
    - ssl.SSL_LIBRARY_VERSION_TLS_1_3
    - ssl.ssl2
    - ssl.ssl3
    - ssl.tls1.0
    - ssl.tls1.1
    - ssl.tls1.2
    - ssl.tls1.3

   * The following methods were missing thread locks, this has been fixed.

     - nss.nss_initialize
     - nss.nss_init_context
     - nss.nss_shutdown_context

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 0.15.0-4
- Replace python-setuptools-devel BR with python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  2 2014 John Dennis <jdennis@redhat.com> - 0.15.0-2
- resolves bug #1087031, bad parameter spec for check_ocsp_status

* Fri Jan 31 2014 John Dennis <jdennis@redhat.com> - 0.15.0-1
- fix fedora bug 1060314, CSR extensions sometimes not found
  Also adds support for accessing CSR attributes.
  See doc/Changelog for details

* Wed Nov 13 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.14.0-3
- Install docs to %%{_pkgdocdir} where available (#994060).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 John Dennis <jdennis@redhat.com> - 0.14-1
  External Changes:
  -----------------

  The primary enhancements in this version is support of certifcate
  validation, OCSP support, and support for the certificate "Authority
  Information Access" extension.

  Enhanced certifcate validation including CA certs can be done via
  Certificate.verify() or Certificate.is_ca_cert(). When cert
  validation fails you can now obtain diagnostic information as to why
  the cert failed to validate. This is encapsulated in the
  CertVerifyLog class which is a iterable collection of
  CertVerifyLogNode objects. Most people will probablby just print the
  string representation of the returned CertVerifyLog object. Cert
  validation logging is handled by the Certificate.verify() method.
  Support has also been added for the various key usage and cert type
  entities which feature prominently during cert validation.


  * Certificate() constructor signature changed from

    Certificate(data=None, der_is_signed=True)

    to

    Certificate(data, certdb=cert_get_default_certdb(), perm=False, nickname=None)

    This change was necessary because all certs should be added to the
    NSS temporary database when they are loaded, but earlier code
    failed to to that. It's is not likely that an previous code was
    failing to pass initialization data or the der_is_signed flag so
    this change should be backwards compatible.

  * Fix bug #922247, PKCS12Decoder.database_import() method. Importing into
    a NSS database would sometimes fail or segfault.

  * Error codes and descriptions were updated from upstream NSPR & NSS.

  * The password callback did not allow for breaking out of a password
    prompting loop, now if None is returned from the password callback
    the password prompting is terminated.

  * nss.nss_shutdown_context now called from InitContext destructor,
    this assures the context is shutdown even if the programmer forgot
    to. It's still best to explicitly shut it down, this is just
    failsafe.

  * Support was added for shutdown callbacks.

  * The following classes were added:
    - nss.CertVerifyLogNode
    - nss.CertVerifyLog
    - error.CertVerifyError (exception)
    - nss.AuthorityInfoAccess
    - nss.AuthorityInfoAccesses


  * The following class methods were added:
    - nss.Certificate.is_ca_cert
    - nss.Certificate.verify
    - nss.Certificate.verify_with_log
    - nss.Certificate.get_cert_chain
    - nss.Certificate.check_ocsp_status
    - nss.PK11Slot.list_certs
    - nss.CertVerifyLogNode.format_lines
    - nss.CertVerifyLog.format_lines
    - nss.CRLDistributionPts.format_lines

  * The following class properties were added:
    - nss.CertVerifyLogNode.certificate
    - nss.CertVerifyLogNode.error
    - nss.CertVerifyLogNode.depth
    - nss.CertVerifyLog.count

  * The following module functions were added:
    - nss.x509_cert_type
    - nss.key_usage_flags
    - nss.list_certs
    - nss.find_certs_from_email_addr
    - nss.find_certs_from_nickname
    - nss.nss_get_version
    - nss.nss_version_check
    - nss.set_shutdown_callback
    - nss.get_use_pkix_for_validation
    - nss.set_use_pkix_for_validation
    - nss.enable_ocsp_checking
    - nss.disable_ocsp_checking
    - nss.set_ocsp_cache_settings
    - nss.set_ocsp_failure_mode
    - nss.set_ocsp_timeout
    - nss.clear_ocsp_cache
    - nss.set_ocsp_default_responder
    - nss.enable_ocsp_default_responder
    - nss.disable_ocsp_default_responder

  * The following files were added:
      src/py_traceback.h
      doc/examples/verify_cert.py
      test/test_misc.py

  * The following constants were added:
    - nss.KU_DIGITAL_SIGNATURE
    - nss.KU_NON_REPUDIATION
    - nss.KU_KEY_ENCIPHERMENT
    - nss.KU_DATA_ENCIPHERMENT
    - nss.KU_KEY_AGREEMENT
    - nss.KU_KEY_CERT_SIGN
    - nss.KU_CRL_SIGN
    - nss.KU_ENCIPHER_ONLY
    - nss.KU_ALL
    - nss.KU_DIGITAL_SIGNATURE_OR_NON_REPUDIATION
    - nss.KU_KEY_AGREEMENT_OR_ENCIPHERMENT
    - nss.KU_NS_GOVT_APPROVED
    - nss.PK11CertListUnique
    - nss.PK11CertListUser
    - nss.PK11CertListRootUnique
    - nss.PK11CertListCA
    - nss.PK11CertListCAUnique
    - nss.PK11CertListUserUnique
    - nss.PK11CertListAll
    - nss.certUsageSSLClient
    - nss.certUsageSSLServer
    - nss.certUsageSSLServerWithStepUp
    - nss.certUsageSSLCA
    - nss.certUsageEmailSigner
    - nss.certUsageEmailRecipient
    - nss.certUsageObjectSigner
    - nss.certUsageUserCertImport
    - nss.certUsageVerifyCA
    - nss.certUsageProtectedObjectSigner
    - nss.certUsageStatusResponder
    - nss.certUsageAnyCA
    - nss.ocspMode_FailureIsVerificationFailure
    - nss.ocspMode_FailureIsNotAVerificationFailure

  * cert_dump.py extended to print NS_CERT_TYPE_EXTENSION

  * cert_usage_flags, nss_init_flags now support optional repr_kind parameter

  Internal Changes:
  -----------------

  * Reimplement exception handling
    - NSPRError is now derived from StandardException instead of
      EnvironmentError. It was never correct to derive from
      EnvironmentError but was difficult to implement a new subclassed
      exception with it's own attributes, using EnvironmentError had
      been expedient.

    - NSPRError now derived from StandardException, provides:
      * errno (numeric error code)
      * strerror (error description associated with error code)
      * error_message (optional detailed message)
      * error_code (alias for errno)
      * error_desc (alias for strerror)

    - CertVerifyError derived from NSPRError, extends with:
      * usages (bitmask of returned usages)
      * log (CertVerifyLog object)

  * Expose error lookup to sibling modules

  * Use macros for bitmask_to_list functions to reduce code
    duplication and centralize logic.

  * Add repr_kind parameter to cert_trust_flags_str()

  * Add support for repr_kind AsEnumName to bitstring table lookup.

  * Add cert_type_bitstr_to_tuple() lookup function

  * Add PRTimeConvert(), used to convert Python time values
    to PRTime, centralizes conversion logic, reduces duplication

  * Add UTF8OrNoneConvert to better handle unicode parameters which
    are optional.

  * Add Certificate_summary_format_lines() utility to generate
    concise certificate identification info for output.

  * Certificate_new_from_CERTCertificate now takes add_reference parameter
    to properly reference count certs, should fix shutdown busy problems.

  * Add print_traceback(), print_cert() debugging support.

* Mon Feb 18 2013 John Dennis <jdennis@redhat.com> - 0.13-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct  8 2012 John Dennis <jdennis@redhat.com> - 0.13-0
- Update to version 0.13
  Introduced in 0.13:

  * Fix NSS SECITEM_CompareItem bug via workaround.

  * Fix incorrect format strings in PyArg_ParseTuple* for:
    - GeneralName
    - BasicConstraints
    - cert_x509_key_usage

  * Fix bug when decoding certificate BasicConstraints extension

  * Fix hang in setup_certs.

  * For NSS >= 3.13 support CERTDB_TERMINAL_RECORD

  * You can now query for a specific certificate extension
    Certficate.get_extension()

  * The following classes were added:
    - RSAGenParams

  * The following class methods were added:
    - nss.nss.Certificate.get_extension
    - nss.nss.PK11Slot.generate_key_pair
    - nss.nss.DSAPublicKey.format
    - nss.nss.DSAPublicKey.format_lines

  * The following module functions were added:
    - nss.nss.pub_wrap_sym_key

  * The following internal utilities were added:
    - PyString_UTF8
    - SecItem_new_alloc()

  * The following class constructors were modified to accept
    intialization parameters

    - KEYPQGParams (DSA generation parameters)

  * The PublicKey formatting (i.e. format_lines) was augmented
    to format DSA keys (formerly it only recognized RSA keys).

  * Allow lables and values to be justified when printing objects

  * The following were deprecated:
    - nss.nss.make_line_pairs (replaced by nss.nss.make_line_fmt_tuples)

    Deprecated Functionality:
    -------------------------
    - make_line_pairs() has been replaced by make_line_fmt_tuples()
      because 2-valued tuples were not sufficently general. It is
      expected very few programs will have used this function, it's mostly
      used internally but provided as a support utility.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 John Dennis <jdennis@redhat.com> - 0.12-2
- add patch python-nss-0.12-rsapssparams.patch to fix build problem
  which appears only with nss 3.13 and later.

* Mon Jun  6 2011 John Dennis <jdennis@redhat.com> - 0.12-1
  * Major new enhancement is additon of PKCS12 support and
    AlgorithmID's.

  * setup.py build enhancements
    - Now searches for the NSS and NSPR header files rather
      than hardcoding their location. This makes building friendlier
      on other systems (i.e. debian)
    - Now takes optional command line arguments, -d or --debug
      will turn on debug options during the build.

  * Fix reference counting bug in PK11_password_callback() which
    contributed to NSS not being able to shutdown due to
    resources still in use.

  * Add UTF-8 support to ssl.config_server_session_id_cache()

  * Added unit tests for cipher, digest, client_server.

  * All unittests now run, added test/run_tests to invoke
    full test suite.

  * Fix bug in test/setup_certs.py, hardcoded full path to
    libnssckbi.so was causing failures on 64-bit systems,
    just use the libnssckbi.so basename, modutil will find
    it on the standard search path.

  * doc/examples/cert_dump.py uses new AlgorithmID class to
    dump Signature Algorithm

  * doc/examples/ssl_example.py now can cleanly shutdown NSS.

  * Exception error messages now include PR error text if available.

  * The following classes were replaced:
    - SignatureAlgorithm replaced by new class AlgorithmID

  * The following classes were added:
    - AlgorithmID
    - PKCS12DecodeItem
    - PKCS12Decoder

  * The following class methods were added:
    - PK11Slot.authenticate()
    - PK11Slot.get_disabled_reason()
    - PK11Slot.has_protected_authentication_path()
    - PK11Slot.has_root_certs()
    - PK11Slot.is_disabled()
    - PK11Slot.is_friendly()
    - PK11Slot.is_internal()
    - PK11Slot.is_logged_in()
    - PK11Slot.is_removable()
    - PK11Slot.logout()
    - PK11Slot.need_login()
    - PK11Slot.need_user_init()
    - PK11Slot.user_disable()
    - PK11Slot.user_enable()
    - PKCS12DecodeItem.format()
    - PKCS12DecodeItem.format_lines()
    - PKCS12Decoder.database_import()
    - PKCS12Decoder.format()
    - PKCS12Decoder.format_lines()

  * The following class properties were added:
    - AlgorithmID.id_oid
    - AlgorithmID.id_str
    - AlgorithmID.id_tag
    - AlgorithmID.parameters
    - PKCS12DecodeItem.certificate
    - PKCS12DecodeItem.friendly_name
    - PKCS12DecodeItem.has_key
    - PKCS12DecodeItem.shroud_algorithm_id
    - PKCS12DecodeItem.signed_cert_der
    - PKCS12DecodeItem.type
    - SignedData.data
    - SignedData.der

  * The following module functions were added:
    - nss.nss.dump_certificate_cache_info()
    - nss.nss.find_slot_by_name()
    - nss.nss.fingerprint_format_lines()
    - nss.nss.get_internal_slot()
    - nss.nss.is_fips()
    - nss.nss.need_pw_init()
    - nss.nss.nss_init_read_write()
    - nss.nss.pk11_disabled_reason_name()
    - nss.nss.pk11_disabled_reason_str()
    - nss.nss.pk11_logout_all()
    - nss.nss.pkcs12_cipher_from_name()
    - nss.nss.pkcs12_cipher_name()
    - nss.nss.pkcs12_enable_all_ciphers()
    - nss.nss.pkcs12_enable_cipher()
    - nss.nss.pkcs12_export()
    - nss.nss.pkcs12_map_cipher()
    - nss.nss.pkcs12_set_nickname_collision_callback()
    - nss.nss.pkcs12_set_preferred_cipher()
    - nss.nss.token_exists()
    - nss.ssl.config_mp_server_sid_cache()
    - nss.ssl.config_server_session_id_cache_with_opt()
    - nss.ssl.get_max_server_cache_locks()
    - nss.ssl.set_max_server_cache_locks()
    - nss.ssl.shutdown_server_session_id_cache()

  * The following constants were added:
    - nss.nss.int.PK11_DIS_COULD_NOT_INIT_TOKEN
    - nss.nss.int.PK11_DIS_NONE
    - nss.nss.int.PK11_DIS_TOKEN_NOT_PRESENT
    - nss.nss.int.PK11_DIS_TOKEN_VERIFY_FAILED
    - nss.nss.int.PK11_DIS_USER_SELECTED
    - nss.nss.int.PKCS12_DES_56
    - nss.nss.int.PKCS12_DES_EDE3_168
    - nss.nss.int.PKCS12_RC2_CBC_128
    - nss.nss.int.PKCS12_RC2_CBC_40
    - nss.nss.int.PKCS12_RC4_128
    - nss.nss.int.PKCS12_RC4_40

  * The following files were added:
    - test/run_tests
    - test/test_cipher.py (replaces cipher_test.py)
    - test/test_client_server.py
    - test/test_digest.py (replaces digest_test.py)
    - test/test_pkcs12.py

  * The following were deprecated:
    - SignatureAlgorithm

* Tue Mar 22 2011 John Dennis <jdennis@redhat.com> - 0.11-2
- Resolves: #689059
  Add family parameter to Socket constructors in examples and doc.
  Mark implicit family parameter as deprecated.
  Raise exception if Socket family does not match NetworkAddress family.
  Add --server-subject to setup_certs.py (made testing IPv6 easier without DNS)

* Mon Feb 21 2011 John Dennis <jdennis@redhat.com> - 0.11-1
  * Better support for IPv6

  * Add AddrInfo class to support IPv6 address resolution. Supports
    iteration over it's set of NetworkAddress objects and provides
    hostname, canonical_name object properties.

  * Add PR_AI_* constants.

  * NetworkAddress constructor and NetworkAddress.set_from_string() added
    optional family parameter. This is necessary for utilizing
    PR_GetAddrInfoByName().

  * NetworkAddress initialized via a string paramter are now initalized via
    PR_GetAddrInfoByName using family.

  * Add NetworkAddress.address property to return the address sans the
    port as a string. NetworkAddress.str() includes the port. For IPv6 the
    a hex string must be enclosed in brackets if a port is appended to it,
    the bracketed hex address with appended with a port is unappropriate
    in some circumstances, hence the new address property to permit either
    the address string with a port or without a port.

  * Fix the implementation of the NetworkAddress.family property, it was
    returning bogus data due to wrong native data size.

  * HostEntry objects now support iteration and indexing of their
    NetworkAddress members.

  * Add io.addr_family_name() function to return string representation of
    PR_AF_* constants.

  * Modify example and test code to utilize AddrInfo instead of deprecated
    NetworkAddress functionality. Add address family command argument to
    ssl_example.

  * Fix pty import statement in test/setup_certs.py

    Deprecated Functionality:
    -------------------------

  * NetworkAddress initialized via a string paramter is now
    deprecated. AddrInfo should be used instead.

  * NetworkAddress.set_from_string is now deprecated. AddrInfo should be
    used instead.

  * NetworkAddress.hostentry is deprecated. It was a bad idea,
    NetworkAddress objects can support both IPv4 and IPv6, but a HostEntry
    object can only support IPv4. Plus the implementation depdended on
    being able to perform a reverse DNS lookup which is not always
    possible.

  * HostEntry.get_network_addresses() and HostEntry.get_network_address()
    are now deprecated. In addition their port parameter is now no longer
    respected. HostEntry objects now support iteration and
    indexing of their NetworkAddress and that should be used to access
    their NetworkAddress objects instead.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 John Dennis <jdennis@redhat.com> - 0.10-3
- Fix all rpmlint warnings
- doc for license, changelog etc. now in main package,
  doc subpackage now only contains api doc, examples, test, etc.
- Filter provides for .so files
- Remove execute permission on everything in docdir
- Capitalize description

* Tue Jan 11 2011 John Dennis <jdennis@redhat.com> - 0.10-2
- split documentation out into separate doc sub-package
  and make building api documentation optional

* Mon Jan 10 2011 John Dennis <jdennis@redhat.com> - 0.10-1
- The following classes were added:
    InitParameters
    InitContext

-The following module functions were added:
    nss.nss.nss_initialize()
    nss.nss.nss_init_context()
    nss.nss.nss_shutdown_context()
    nss.nss.nss_init_flags()

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 16 2010 John Dennis <jdennis@redhat.com> - 0.9-8
- add nss_is_initialized()

* Thu Jul  8 2010 John Dennis <jdennis@redhat.com> - 0.9-7
- Remove nss_init_nodb() when nss modules loads from previous version
  apparently this prevents subsequent calls to nss_init with a
  database to silently fail.
- Clean up some cruft in doc/examples/verify_server.py

* Thu Jun 24 2010 John Dennis <jdennis@redhat.com> - 0.9-6
- Invoke nss_init_nodb() when nss modules loads, this prevents segfaults
  in NSS if Python programmer forgot to call one of the NSS
  initialization routines.

- Rename the classes X500Name, X500RDN, X500AVA to DN, RDN, AVA
  respectively.

- DN and RDN objects now return a list of their contents when indexed by
  type, this is to support multi-valued items.

- Fix bug where AVA object's string representation did not include it's
  type.

- Enhance test/test_cert_components.py unit test to test for above
  changes.

- Add CertificateRequest object

* Mon Jun 14 2010 John Dennis <jdennis@redhat.com> - 0.9-5
- Fix incomplete read bug (due to read ahead buffer bookkeeping).
- Remove python-nss specific httplib.py, no longer needed
  python-nss now compatible with standard library
- Rewrite httplib_example.py to use standard library and illustrate
  ssl, non-ssl, connection class, http class usage

* Wed Jun  9 2010 John Dennis <jdennis@redhat.com> - 0.9-4
- add nss.cert_usage_flags(), use it in ssl_example.py

* Sun Jun  6 2010 John Dennis <jdennis@redhat.com> - 0.9-3
- Add format_lines() & format() methods to the new certificate extension objects.
- Add printing of certificate extensions.
- Add BasicContstraints certificate extension.
- Fix several reference counting and memory problems discovered with valgrind.

* Tue Jun  1 2010 John Dennis <jdennis@redhat.com> - 0.9-2
- fold in more ref counting patches from Miloslav Trmač <mitr@redhat.com>
  into upstream.
  Did not bump upstream version, just bumped release ver in this spec file.

* Fri May 28 2010 John Dennis <jdennis@redhat.com> - 0.9-1
- Unicode objects now accepted as well as str objects for
  interfaces expecting a string.

- Sockets were enhanced thusly:
    - Threads will now yield during blocking IO.
    - Socket.makefile() reimplemented
          file object methods that had been missing (readlines(), sendall(),
          and iteration) were implemented, makefile now just returns the same
          Socket object but increments an "open" ref count. Thus a Socket
          object behaves like a file object and must be closed once for each
          makefile() call before it's actually closed.
    - Sockets now support the iter protocol
    - Add Socket.readlines(), Socket.sendall()

- The following classes were added:
    AuthKeyID
    BasicConstraints
    CRLDistributionPoint
    CRLDistributionPts
    CertificateExtension
    GeneralName
    SignedCRL
    X500AVA
    X500Name
    X500RDN

- The following module functions were added:
    nss.nss.cert_crl_reason_from_name()
    nss.nss.cert_crl_reason_name()
    nss.nss.cert_general_name_type_from_name()
    nss.nss.cert_general_name_type_name()
    nss.nss.cert_usage_flags()
    nss.nss.decode_der_crl()
    nss.nss.der_universal_secitem_fmt_lines()
    nss.nss.import_crl()
    nss.nss.make_line_pairs()
    nss.nss.oid_dotted_decimal()
    nss.nss.oid_str()
    nss.nss.oid_tag()
    nss.nss.oid_tag_name()
    nss.nss.read_der_from_file()
    nss.nss.x509_alt_name()
    nss.nss.x509_ext_key_usage()
    nss.nss.x509_key_usage()

- The following class methods and properties were added:
  Note: it's a method if the name is suffixed with (), a propety otherwise
    Socket.next()
    Socket.readlines()
    Socket.sendall()
    SSLSocket.next()
    SSLSocket.readlines()
    SSLSocket.sendall()
    AuthKeyID.key_id
    AuthKeyID.serial_number
    AuthKeyID.get_general_names()
    CRLDistributionPoint.issuer
    CRLDistributionPoint.get_general_names()
    CRLDistributionPoint.get_reasons()
    CertDB.find_crl_by_cert()
    CertDB.find_crl_by_name()
    Certificate.extensions
    CertificateExtension.critical
    CertificateExtension.name
    CertificateExtension.oid
    CertificateExtension.oid_tag
    CertificateExtension.value
    GeneralName.type_enum
    GeneralName.type_name
    GeneralName.type_string
    SecItem.der_to_hex()
    SecItem.get_oid_sequence()
    SecItem.to_hex()
    SignedCRL.delete_permanently()
    X500AVA.oid
    X500AVA.oid_tag
    X500AVA.value
    X500AVA.value_str
    X500Name.cert_uid
    X500Name.common_name
    X500Name.country_name
    X500Name.dc_name
    X500Name.email_address
    X500Name.locality_name
    X500Name.org_name
    X500Name.org_unit_name
    X500Name.state_name
    X500Name.add_rdn()
    X500Name.has_key()
    X500RDN.has_key()

- The following module functions were removed:
  Note: use nss.nss.oid_tag() instead
    nss.nss.sec_oid_tag_from_name()
    nss.nss.sec_oid_tag_name()
    nss.nss.sec_oid_tag_str()

- The following files were added:
    doc/examples/cert_dump.py
    test/test_cert_components.py

- Apply patches from  Miloslav Trmač <mitr@redhat.com>
  for ref counting and threading support. Thanks Miloslav!

- Review all ref counting, numerous ref counting fixes

- Implement cyclic garbage collection support by
  adding object traversal and clear methods

- Identify static variables, move to thread local storage


* Wed Mar 24 2010 John Dennis <jdennis@redhat.com> - 0.8-2
- change %%define to %%global

* Mon Sep 21 2009 John Dennis <jdennis@redhat.com> - 0.8-1
- The following methods, properties  and functions were added:
  SecItem.type SecItem.len, SecItem.data
  PK11SymKey.key_data, PK11SymKey.key_length, PK11SymKey.slot
  create_context_by_sym_key
  param_from_iv
  generate_new_param
  get_iv_length
  get_block_size
  get_pad_mechanism
- SecItem's now support indexing and slicing on their data
- Clean up parsing and parameter validation of variable arg functions

* Fri Sep 18 2009 John Dennis <jdennis@redhat.com> - 0.7-1
- add support for symmetric encryption/decryption
  more support for digests (hashes)

  The following classes were added:
  PK11SymKey PK11Context

  The following methods and functions were added:
  get_best_wrap_mechanism          get_best_key_length
  key_gen                          derive
  get_key_length                   digest_key
  clone_context                    digest_begin
  digest_op                        cipher_op
  finalize                         digest_final
  read_hex                         hash_buf
  sec_oid_tag_str                  sec_oid_tag_name
  sec_oid_tag_from_name            key_mechanism_type_name
  key_mechanism_type_from_name     pk11_attribute_type_name
  pk11_attribute_type_from_name    get_best_slot
  get_internal_key_slot            create_context_by_sym_key
  import_sym_key                   create_digest_context
  param_from_iv                    param_from_algid
  generate_new_param               algtag_to_mechanism
  mechanism_to_algtag

  The following files were added:
  cipher_test.py digest_test.py

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 John Dennis <jdennis@redhat.com> - 0.6-2
- restore nss.nssinit(), make deprecated

* Wed Jul  8 2009 John Dennis <jdennis@redhat.com> - 0.6-1
- fix bug #510343 client_auth_data_callback seg faults if False
  is returned from callback

* Wed Jul  1 2009 John Dennis <jdennis@redhat.com> - 0.5-1
- restore ssl.nss_init and ssl.nss_shutdown but make them deprecated
  add __version__ string to nss module

* Tue Jun 30 2009 John Dennis <jdennis@redhat.com> - 0.4-1
- add binding for NSS_NoDB_Init(), bug #509002
  move nss_init and nss_shutdown from ssl module to nss module

* Thu Jun  4 2009 John Dennis <jdennis@redhat.com> - 0.3-1
- installed source code in Mozilla CVS repository
  update URL tag to point to CVS repositoy
  (not yet a valid URL, still have to coordinate with Mozilla)
  minor tweak to src directory layout

* Mon Jun  1 2009 John Dennis <jdennis@redhat.com> - 0.2-1
- Convert licensing to MPL tri-license
- apply patch from bug #472805, (Miloslav Trmač)
  Don't allow closing a socket twice, that causes crashes.
  New function nss.io.Socket.new_socket_pair()
  New function nss.io.Socket.poll()
  New function nss.io.Socket.import_tcp_socket()
  New method nss.nss.Certificate.get_subject_common_name()
  New function nss.nss.generate_random()
  Fix return value creation in SSLSocket.get_security_status
  New function nss.ssl.SSLSocket.import_tcp_socket()

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1-2
- Rebuild for Python 2.6

* Tue Sep  9 2008 John Dennis <jdennis@redhat.com> - 0.1-1
- clean up ssl_example.py, fix arg list in get_cert_nicknames,
   make certdir cmd line arg consistent with other NSS tools
- update httplib.py to support client auth, add httplib_example.py which illustrates it's use
- fix some documentation
- fix some type usage which were unsafe on 64-bit

* Wed Jul  9 2008 John Dennis <jdennis@redhat.com> - 0.0-2
- add docutils to build requires so restructured text works

* Fri Jun 27 2008 John Dennis <jdennis@redhat.com> - 0.0-1
- initial release
