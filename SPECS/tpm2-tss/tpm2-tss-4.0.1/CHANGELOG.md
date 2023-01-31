# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)

## [4.0.1] - 2023-01-23
### Fixed:
 - A buffer overflow in tss2-rc as CVE-2023-22745.

## [4.0.0] - 2023-01-02
### Fixed
  - tcti-ldr: Use heap instead of stack when tcti initialize
 - Fix usage of NULL pointer if Esys_TR_SetAuth is calles with ESYS_TR_NONE.
 - Conditionally check user/group manipulation commands.
 - Store VERSION into the release tarball.
 - When using DESTDIR for make einstall, do not invoke systemd-sysusers and systemd-tmpfiles.
 - esys_iutil: fix possible NPD.
 - Tss2_Sys_Flushcontext: flushHandle was encoded as a handleArea handle and not as parameter one, this affected the contents of cpHash.
- esys: fix allow usage of HMAC sessions for Esys_TR_FromTPMPublic.
- fapi: fix usage of policy_nv with a TPM nv index.
- linking tcti for libtpms against tss2-tctildr. It should be linked against tss2-mu.
- build: Remove erroneous trailing comma in linker option. Bug #2391.
- fapi: fix encoding of complex tpm2bs in authorize nv, duplication select and policy template policies. Now the complex and TPMT or TPMS representations can be used. Bug #2383
- The error message for unsupported FAPI curves was in hex without a leading 0x, make it integer output to clarify.
- Documentation that had various scalar out pointers as "callee allocated".
- test: build with opaque FILE structure like in musl libc.
- Transient endorsement keys were not recreated according to the EK credential profile.
- Evict control for a persistent EK failed during provisioning if an auth value for the storage hierarchy was set.
- The authorization of the storage hierarchy is now added. Fixes FAPI: Provisioning error if an auth value is needed for the
   storage hierarchy  #2438.
- Usage of a second profile in a path was not possible because the default profile was always used.
- The setting of an empty auth value for Fapi_Provision was fixed.
- JSON encoding of a structure TPMS_POLICYAUTHORIZATION used the field keyPEMhashAlg instead of hashAlg as
   defined in "TCG TSS 2.0 JSON Data Types and Policy Language Specification".  Rename to hashAlg but preserve support
   for reading keyPEMhashAlg for backwards compatibility.
- fapi: PolicySecret did not work with keys as secret object.
- Esys_PCR_SetAuthValue: remembers the auth like other SetAutg ESAPI functions.
- tests: esys-pcr-auth-value.int moved to destructive tests.
- FAPI: Fix double free if keystore is corrupted.
- Marshaling of TPMU_CAPABILITIES data, only field intelPttProperty was broken before.a
- Spec deviation in Fapi_GetDescription caused description to be NULL when it should be empty string.
  This is API breaking but considered a bug since it deviated from the FAPI spec.
- FAPI: undefined reference to curl_url_strerror when using curl less than 7.80.0.
- FAPI: Fixed support for EK templates in NV inidices per the spec, see #2518 for details.
- FAPI: fix NPD in ifapi_curl logging.
- FAPI: Improve documentation fapi-profile
- FAPI: Fix CURL HTTP handling.
- FAPI: Return FAPI_RC_IO_ERROR if a policy does not exist in keystore.

### Added
- TPM version 1.59 support.
- ci: ubuntu-22.04 added.
- mbedTLS 3.0 is supported by ESAPI.
- Add CreationHash to JSON output for usage between applications not using the FAPI keystore, like command line tools.
- Reduced code size for SAPI.
- Support for Runtime Switchable ESAPI Crypto Backend via `Esys_SetCryptoCallbacks`.
- Testing for TCG EK Credential Profile TPM 2.0, Version 2.4 Rev. 3, 2021 for the low and high address range of EK templates.
- tss2-rc: Tss2_RC_DecodeInfo function for parsing TSS2_RC into the various bit fields.
- FAPI support for P_ECC384 profile.
- tss2-rc: Tss2_RC_DecodeInfoError: Function to get a human readable error from a TSS2_RC_INFO returned by
  Tss2_RC_DecodeInfo
- tcti: Generic SPI driver, implementors only need to connect to acquire/release, transmit/receive, and sleep/timeout functions.
- FAPI: Add event logging for Firmware and IMA Events. See #2170 for details.
- FAPI: Fix Fapi_ChangeAuth updates on hierarchy objects not being reflected across profiles.
- FAPI: Allow keyedhash keys in PolicySigned.
- ESAPI: Support sha512 for mbedtls crypto backend.
- TPM2B_MAX_CAP_BUFFER and mu routines
- vendor field to TPMU_CAPABILTIIES
- FAPI: support for PolicyTemplate

### Changed
- libmu soname from 0:0:0 to 0:1:0.
- tss2-sys soname from 1:0:0 to 1:1:0
- tss2-esys: from 0:0:0 to 0:1:0
- FAPI ignores vendor properties on Fapi_GetInfo
- FAPI Event Logging JSON format, See #2170 for details.

### Removed
- Dead struct TPMS_ALGORITHM_DESCRIPTION
- Dead field intelPttProperty from TPMU_CAPABILITIES
- Dead code Tss2_MU_TPMS_ALGORITHM_DESCRIPTION_Marshal
- Dead code Tss2_MU_TPMS_ALGORITHM_DESCRIPTION_Unmarshal

## [3.2.0] - 2022-02-18
### Fixed
- FAPI: fix curl_url_set call
- FAPI: Fix usage of curl url (Should fix Ubuntu 22.04)
- Fix buffer upcast leading to misalignment
- Fix check whether SM3 is available
- Update git.mk to support R/O src-dir
- Fixed file descriptor leak when tcti initialization failed.
- 32 Bit builds of the integration tests.
- Primary key creation, in some cases the unique field was not cleared before calling create primary.
- Primary keys was used for signing the object were cleared after loading. So access e.g. to the certificate did not work.
- Primary keys created with Fapi_Create with an auth value, the auth_value was not used in inSensitive to recreate the primary key. Now the auth value callback is used to initialize inSensitive.
- The not possible usage of policies for primary keys generated with Fapi_CreatePrimary has been fixed.
- An infinite loop when parsing erroneous JSON was fixed in FAPI.
- A buffer overflow in ESAPI xor parameter obfuscation was fixed.
- Certificates could be read only once in one application The setting the init state of the state automaton for getting certificates was fixed.
- A double free when executing policy action was fixed.
- A leak in Fapi_Quote was fixed.
- The  wrong file locking in FAPI IO was fixed.
- Enable creation of tss group and user on systems with busybox for fapi.
- One fapi integration test did change the auth value of the storage hierarchy.
- A leak in fapi crypto with ossl3 was fixed.
- Add initial camelia support to FAPI
- Fix tests of fapi PCR
- Fix tests of ACT functionality if not supported by pTPM
- Fix compiler (unused) warning when building without debug logging
- Fix leaks in error cases of integration tests
- Fix memory leak after ifapi_init_primary_finish failed
- Fix double-close of stream in FAPI
- Fix segfault when ESYS_TR_NONE is passed to Esys_TR_GetName
- Fix the authorization of hierarchy objects used in policy secret.
- Fix check of qualifying data in Fapi_VerifyQuote.
- Fix some  leaks in FAPI error cases.
- Make scripts compatible with non-posix shells where `test` does not know `-a` and `-o`.
- Fix usage of variable not initialized when fapi keystore is empty.

### Added
- Add additional IFX root CAs
- Added support for SM2, SM3 and SM4.
- Added support for OpenSSL 3.0.0.
- Added authPolicy field to the TPMU_CAPABILITIES union.
- Added actData field to the TPMU_CAPABILITIES union.
- Added TPM2_CAP_AUTH_POLICIES
- Added TPM2_CAP_ACT constants.
- Added updates to the marshalling and unmarshalling of the TPMU_CAPABILITIES union.
- Added updated to the FAPI serializations and deserializations of the TPMU_CAPABILITIES union and associated types.
- Add CODE_OF_CONDUCT
- tcti-mssim and tcti-swtpm gained support for UDX communication
- Missing constant for TPM2_RH_PW

### Removed
- Removed support for OpenSSL < 1.1.0.
- Marked TPMS_ALGORITHM_DESCRIPTION and corresponding MU routines as deprecated.
  Those were errorous typedefs that are not use and not useful. So we will remove this with 3.3
- Marked TPM2_RS_PW as deprecated. Use TPM2_RH_PW instead.

## [3.1.0] - 2021-05-17
### Fixed
- Fixed possible access outside the array in ifapi_calculate_tree.
- Fix CVE-2020-24455 FAPI PolicyPCR not instatiating correctly
  Note: that all TPM object created with a PolicyPCR with the currentPcrs
  and currentPcrsAndBank options have been created with an incorrect policy
  that ommits PCR checks. All these objects have to be recreated!
- Fixed segfault in Fapi_Finalize where a free of a constant string could occur.
- Fixed binding to ESYS_TR_RH_NULL for ESYS auth sessions.
- Fixed read eagain error handling for freeBSD.
- Fixed error cleanup for key loading and policy execution.
- Fixed initialization of default log_dir.
- Fixed cleanup in several error cases in Fapi.
- Added initialise 'out' parameter in ifapi_json_IFAPI_CONFIG_deserialize.
- Fixed Regression in Fapi_List.
- Fixed memory leak in policy calculation.
- Fixed setting of the system flag of NV objects:
  This will let NV object metadata be created system-wide always instead of
  locally in the user. Existing metadata will remain in the user directory.
  It can be moved to the corresponding systemstore manually if needed.
- Fixed fapi policy searching, when a policyRef was provided.
- Fapi accepts EK-Certs without CRL dist point.
- Fixed bad return codes in Fapi_List.
- Fixed memleak in Fapi policy execution.
- Fixed coverity NULL-pointer check in Fapi.
- Fixed the written flag of NV objects in FAPI PolicyNV commands being unset.
- Fixed deleting of policy files.
- Fixed wrong file loading during object search.
- Fixed a memory leak in async keystore load.
- Fixed bug in FAPI NV creation with custom index values.
- Fixed leftover sessions in error cases in FAPI.
- Fixed execution of FAPI policies in some cases.
- Fixed  handling 0x hex prefixes for TPMU_HA in JSON encoding.
- Fixed fix doxygen header of function iesys_update_session_flags.
- Fixed issue where nonceTPM was included twice in HMAC.
- Fixed issue of unused variable when enabling lower default log levels.
- Fixed 'partial' may be used uninitialized in tcti-device.

### Added
- Added two new TPM commands TPM2_CC_CertifyX509 and TPM2_CC_ACT_SetTimeout
  along with SYS and ESYS API calls, new structures definitions, and marshal
  funtions for them. This make the TSS2 alligned with TPM2 1.59 specification.
- Support for auth values larger than an objects nameAlg for NV and key objects.
- Async mode of operation for mssim TCTI module
- Added pcap TCTI.
- Added GlobalSign TPM Root CA certs to FAPI cert store.
- Added support for auth value sizes bigger than the size of the name hash alg.
  for keys and NV objects.
- Added better error messages in several FAPI errors.
- Added checks to FAPI policy paths.
- Added checks if FAPI is correctly provisioned.

### Changed
- Changed CI from Travis to GH actions
- Changed the default hash algorithm from sha1 to sha256 in all FAPI
  integration tests
- Changed tests to use SHA256 over SHA1.
- Changed EncryptDecrypt mode type to align with TPM2.0 spec 1.59.


## [3.0.0] - 2020-08-05
### Changed or Fixed
- Added setgid perms and ACL for FAPI keystore to allow r/w access for tss group
- Fixed duoble json_object_put call in event log processing.
- Added TSS root dir to include path in CFLAGS
- Switch default FAPI profile to ECC.
- Enabled all PCR registers for SHA256 bank in the distribution profiles.
- Added fix computation of PCR logs and PCR digest of PCR logs.
- Added fix size check for Fapi_Encrypt.
- Improved log messages in FAPI
- Introduced new FAPI return codes FAPI_RC_ALREADY_PROVISIONED,
  TSS2_BASE_RC_NOT_PROVISIONED, and TSS2_FAPI_RC_NOT_PROVISIONED.
- Added missing retry in Fapi_Initialize_Finish.
- Added man pages for FAPI config files
- Deleted invalid keys from the null hierarchy.
- Fixed check of auth state for lockout set.
- Fixed check of directory access rights in Fapi_Initialize.
- Enabled usage of NULL hierarchy in FAPI.
- Added address sanitizer to CI for gcc.
- Added asserts to callback functions in integration tests
- Added check event log file before Fapi_PcrExtend.
- Fixed hierarchy usage and authentication in Fapi_Provision,
  Fapi_GetCertificate, and Fapi_Delete.
- Added description for primary keys to profile.
- Fixed non async call of Esys_ContextSave in Fapi_GetEsysBlobs.
- Added check for hierarchy needed for EvictControl for deleting objects.
- Fixed copying the primary during key loading.
- Added a check that prevents deleting of default directories.
- Added verification to provisioning.
- Fixed usage of persistent handles.
- Added missing selectors for some TPMU types in marshal
- Added handling for invalid selector when (um)marshal TPMU types
- Improved presentation of Fapi_GetInfo.
- Fixed computation of the size of a PCR selection.
- Added a check for valid pathnames in keystore module.
- Added a check for deleting of the SRK.
- Fixed computation of random value for objects used for sealing.
- Fixed return code for event parsing errors.
- Added content of the config file to FAPI Info.
- Fixed NV index and path handling in NV creation.
- Fixed path checking for keys.
- Fixed version retrieval method in Fapi_GetInfo.
- Fixed path usage in Fapi_Import.
- Fixed settings of default flags for keys creation.
- Fixed handle usage in Fapi_ChangeAuth
- Fixed systemd-sysusers/-tmpfiles invocation
- Changed FAPI callback API.
- Fixed initialization of app data in Esys_Initialize
- Fixed certificate handling for TPMs without stored certificate.
- Replaced strtok with strtok_r
- Changed return codes from tcti macros according to the spec
- Added check that prevents overwriting objects in key store.
- Added session usage to FAPI provisioning.
- Enabled CI for FreeBSD
- Changed hierarchy param type of Esys_Hash(), Esys_HierarchyControl(),
  Esys_LoadExternal(), and Esys_SequenceComplete() calls along with
  their Async versions according to the spec.
  The can accept both types TPM2_RH and ESYS_TRs as then don't collide.
- Changed Tss2_Sys_ReadClock to allow audit session to be consistent
  with the rev 1.38 version of the TPM2.0 architecture spec.
  Note: This change brakes ABI backwards compatibility.
- Silenced expected errors from Esys_TestParams.
- Many improvements for CI builds on Travis and Cirrus, unit tests
  and integration test code

### Added
- Added SWTPM-TCTI
- Added mbedTLS ESYS crypto backend
- Added the Command TCTI
- Added new API function Fapi_GetEsysBlobs.
- Added new feature for importing keys with Fapi_Import.

### Removed
- Removed libgcrypt ESYS crypto backend
- Removed dev-tcti partial read mode configuration flag
- Removed dev-tcti async mode configuration flag
- Removed obsolete LIBDL_LDFLAGS and replaced broken @LIBDL_LDFLAGS@ with @LIBADD_DL@
- Removed deprecated OpenSSL functions from FAPI and ESYS

## [2.4.0] - 2020-03-11
### Added
- Added a new Feature API (FAPI) implementation
- Added Esys_TRSess_GetAuthRequired() ESAPI function
- Added Esys_TR_GetTpmHandle() SAPI function
- Added Esys_GetSysContext() SAPI function
- Added the with-sanitizer configure option
- Added CI for FreeBSD
- Added tcti-cmd

### Changed
- Changed MSSIM TCTI to be async capable
- Removed TCTI loaders from ESYS dependencies in pkg-config
- Changed getPollHandles to allow num_handles query
- Improved CI builds
- Converted builds to docker builds
- Number of fixes and improvements in the test code
- Changed tcti-device in non-async mode to allways block

### Fixed
- Fixed hmac calculation for tpm2_clear command in ESAPI
- Fixed mixing salted and unsalted sessions in the same ESAPI context
- Removed use of VLAs from TPML marshal code
- Fixed setting C++ compiler for non-fuzzing builds at configure
- Fixed setting the name of session objects
- Fixed page alignment errors in Sys_Get/SetAuths functions
- Fixed potential buffer overflow in tcti_mssim_receive
- Fixed invalid memory alloc failure in Tss2_TctiLdr_Initialize
- Fixed list of exported symbols map for libtss2-mu
- Fixed resource name calculation in Esys_CreateLoaded
- Fixed keysize of ECC curve TPM2_ECC_NISTP224
- Fixed segmentation fault in tctildr if name_conf was too big
- Fixed memory leak in tctildr-tcti tests
- Fixed HMAC generation for policy sessions
- Added check for object node before calling compute_session_value function
- Fixed auth calculation in Esys_StartAuthSession called with optional parameters
- Fixed compute_encrypted_salt error handling in Esys_StartAuthSession
- Fixed exported symbols map for libtss2-mu

### Removed
- Remove duplicate ESYS entries from map file
- Removed the private implementation of strndup from tctildr

## [2.3.0] - 2019-08-13
### Added
- tss2-tctildr: A new library that helps with tcti initialization
  Recommend to use this in place of custom tcti loading code now !
- tss2-rc: A new library that provides textual representations for return codes
- Added release and maintainance info (~3 per year and latest 2 are supported)
- Support for building on VxWorks.
- Option to disable NIST-deprecated crypto (--disable-weak-crypto)
- Support Esys_TR_FromTPMPublic on sessions (for use in Esys_FlushContext)
- Better Windows/VS Support
- Fuzz-Testing and Valgrind-Testing
- map-files with correct symbol lists for tss2-sys and tss2-esys
  This may lead to unresolved symbols in linked applications

### Changed
- Several further minor fixes and cleanups
- Support to call Tss2_Sys_Execute repeatedly on certain errors
- Reduced RAM consumption in Esys due to Tss2_Sys_Execute change
- Automated session attribution clearing for esys (decrypt and encrypt) per cmd
- Switched to git.mk, many ax_ makros and away from gnulib
- Switched to config.h and autoheaders

### Removed
- Removed libtss2-mu from "Requires" field of libtss2-esys.pc
  Needs to be added explicitely now

### Fixed
- All fixes from 2.2.1, 2.2.2 and 2.2.3
- SPDX License Identifiers
- Null-pointer problems in tcti-tbs
- Default locality for tcti-mssim set to LOC_0
- coverity and valgrind leaks detected in test programs (not library code)

## [2.2.3] - 2019-05-28
### Fixed
 - Fix computation of session name
 - Fixed PolicyPassword handling of session Attributes
 - Fixed windows build from dist ball
 - Fixed default tcti configure option
 - Fixed nonce size calculation in ESYS sessions

## [2.2.2] - 2019-03-28
### Fixed
 - Fixed wrong encryption flag in EncryptDecrypt
 - Fixing openssl engine invocation

## [2.2.1] - 2019-02-28
### Fixed
 - Forced RAND_bytes method to software implementation to avoid session spoofing
 - Fixed OpenSSL symbolic naming conflict
 - Fixed leaks of local point variables and BN_ctx
 - Fixed memory leaks related to using regular free on gcrypt allocated objects
 - Fixed leak of rsa->n in iesys_cryptossl_pk_encrypt
 - Fixed memory leaks in iesys_cryptossl_pk_encrypt
 - Fixed possible NULL dereference of big number

## [2.2.0] - 2019-02-04
### Fixed
- Fixed leak of hkey on success in iesys_cryptossl_hmac_start
- Fixed NULL ptr issues in Esys_HMAC_Start, Esys_HierarchyChangeAuth and Esys_NV_ChangeAuth
- Fixed NULL ptr issue in sequenceHandleNode
- Fixed NULL ptr auth handling in Esys_TR_SetAuth
- Fixed NULL auth handling in iesys_compute_session_value
- Fixed marshaling of TPM2Bs with sub types.
- Fixed NULL ptr session handling in Esys_TRSess_SetAttributes
- Fixed the way size of the hmac value of a session without authorization
- Added missing MU functions for TPM2_NT type
- Added missing MU functions for TPMA_ID_OBJECT type
- Added missing type TPM2_NT into tss2_tpm2_types.h
- Fixed wrong typename _ID_OBJECT in tss2_tpm2_types.h
- Fixed build breakage when --with-maxloglevel is not 'trace'
- Fixed build breakage in generated configure script when CFLAGS is set
- Fixed configure scritp ERROR_IF_NO_PROG macro
- Changed TPM2B type unmarshal to use sizeof of the dest buffer instead of dest
- Fixed unmarshaling of the TPM2B type with invalid size
- Removed dead code defect detected by coverity from Esys_TRSess_GetNonceTPM

### Added
- Added support for QNX build
- Added support for partial reads in device TCTI

## [2.1.1] - 2019-02-04
### Fixed
- Fixed leak of hkey on success in iesys_cryptossl_hmac_start
- Fixed NULL ptr issues in Esys_HMAC_Start, Esys_HierarchyChangeAuth and Esys_NV_ChangeAuth
- Fixed NULL ptr issue in sequenceHandleNode
- Fixed NULL ptr auth handling in Esys_TR_SetAuth
- Fixed NULL auth handling in iesys_compute_session_value
- Fixed marshaling of TPM2Bs with sub types.
- Fixed NULL ptr session handling in Esys_TRSess_SetAttributes
- Fixed the way size of the hmac value of a session without authorization
- Added missing MU functions for TPM2_NT type
- Added missing MU functions for TPMA_ID_OBJECT type
- Added missing type TPM2_NT into tss2_tpm2_types.h
- Fixed wrong typename _ID_OBJECT in tss2_tpm2_types.h
- Fixed build breakage when --with-maxloglevel is not 'trace'
- Fixed build breakage in generated configure script when CFLAGS is set
- Fixed configure scritp ERROR_IF_NO_PROG macro
- Changed TPM2B type unmarshal to use sizeof of the dest buffer instead of dest
- Fixed unmarshaling of the TPM2B type with invalid size
- Removed dead code defect detected by coverity from Esys_TRSess_GetNonceTPM

## [2.1.0]
### Fixed
- Fixed handling of the default TCTI
- Changed logging to be ISO-C99 compatible
- Fixed leak of dlopen handle
- Fixed logging of a response header tag in Tss2_Sys_Execute
- Fixed marshaling of TPM2B parameters in SAPI commands
- Fixed unnecessary warning in Esys_Startup
- Fixed warnings in doxygen documentation

### Added
- Added Esys_Free wrapper function for systems using different C runtime libraries
- Added Windows TBS TCTI
- Added non-blocking mode of operation in tcti-device
- Added tests for Esys_HMAC and Esys_Hash
- Enabled integration tests on physical TPM device
- Added openssl libcrypto backend
- Added Doxygen documentation to integration tests

### Changed
- Refactored SetDecryptParam
- Enabled OpenSSL crypto backend by default

## [2.0.2] - 2019-02-04
### Fixed
- Fixed NULL ptr issues in Esys_HMAC_Start, Esys_HierarchyChangeAuth and Esys_NV_ChangeAuth
- Fixed NULL ptr issue in sequenceHandleNode
- Fixed NULL ptr auth handling in Esys_TR_SetAuth
- Fixed NULL auth handling in iesys_compute_session_value
- Fixed marshaling of TPM2Bs with sub types.
- Fixed NULL ptr session handling in Esys_TRSess_SetAttributes
- Fixed the way size of the hmac value of a session without authorization
- Added missing MU functions for TPM2_NT type
- Added missing MU functions for TPMA_ID_OBJECT type
- Added missing type TPM2_NT into tss2_tpm2_types.h
- Fixed wrong typename _ID_OBJECT in tss2_tpm2_types.h
- Fixed build breakage when --with-maxloglevel is not 'trace'
- Fixed build breakage in generated configure script when CFLAGS is set
- Fixed configure scritp ERROR_IF_NO_PROG macro
- Changed TPM2B type unmarshal to use sizeof of the dest buffer instead of dest
- Fixed unmarshaling of the TPM2B type with invalid size
- Removed dead code defect detected by coverity from Esys_TRSess_GetNonceTPM

## [2.0.1] - 2018-08-10
### Fixed
- Fixed problems with doxygan failing make distcheck
- Fixed conversion of gcrypt mpi numbers to binary data
- Fixed an error in parsing socket address in MSSIM TCTI
- Fixed compilation error with --disable-tcti-mssim
- Added initialization function for gcrypt to suppress warning
- Fixed invalid type base type while marshaling TPMI_ECC_CURVE in Tss2_Sys_ECC_Parameters
- Fixed invalid RSA encryption with exponent equal to 0
- Fixed checking of return codes in ESAPI commands
- Added checks for programs required by the test harness @ configure time
- Fixed warning on TPM2_RC_INITIALIZE rc after a Startup in Esys_Startup
- Checked for 1.2 TPM type response
- Changed constants values in esys header file to unsigned

## [2.0.0] - 2018-06-20
### Added
- Implementation of the Marshal/Unmarshal library (libtss2-mu)
- Implementation of the Enhanced System API (libtss2-esys aka ESAPI)
- New implemetation of the TPM Command Transmission Interface (TCTI) for:
  - communication with Linux TPM2 device driver: libtss2-tcti-device
  - communication with Microsoft software simulator: libtss2-tcti-mssim
- New directory layout (API break)
- Updated documentation with new doxygen and updated man pages
- Support for Windows build with Visual Studio and clang, currently limited
to libtss2-mu and libtss2-sys
- Implementation of the new Attached Component (AC) commands
- Implementation of the new TPM2_PolicyAuthorizeNV command
- Implementation of the new TPM2_CreateLoaded command
- Implementation of the new TPM2_PolicyTemplate command
- Addition of _Complete functions to all TPM commands
- New logging framework
- Added const qualifiers to API input pointers (API break)
- Cleaned up headers and remove implementation.h and tpm2.h (API break)
### Changed
- Converted all cpp files to c, removed dependency on C++ compiler.
- Cleaned out a number of marshaling functions from the SAPI code.
- Update Linux / Unix OS detection to use non-obsolete macros.
- Changed TCTI macros to CamelCase (API break)
- Changed TPMA_types to unsigned int with defines instead of bitfield structs (API/ABI break)
- Changed Get/SetCmd/RspAuths to new parameter types (API/ABI break)
- Fixed order of parameters in AC commands: Input command authorizations
now come after the input handles, but still before the command parameters.
### Removed
- Removed all sysapi/sysapi_utils/*arshal_TPM*.c files
### Fixed
- Updated invalid number of handles in TPM2_PolicyNvWritten and TPM2_TestParms
- Updated PlatformCommand function from libtss2-tcti-mssim to no longer send
CANCEL_OFF before every command.
- Expanded TPM2B macros and removed TPM2B_TYPE1 and TPM2B_TYPE2 macros
- Fixed wrong return type for Tss2_Sys_Finalize (API break).

## [1.4.0] - 2018-03-02
### Added
- Attached Component commands from the last public review spec.
### Fixed
- Essential files missing from release tarballs are now included.
- Version string generation has been moved from configure.ac to the
bootstrap script. It is now stored in a file named `VERSION` that is
shipped in the release tarball.
- We've stopped shipping the built man page for InitSocketTcti.3 and now
ship the source.

## [1.3.0] - 2017-12-07
### Added
- Implementation of the EncryptDecrypt2 command.
- Coding standard documentation.
- Support for latest TPM2 simulator v974 (only changes in test harness).
- Check cmocka version for compatibility with 1.0 API.
### Fixed
- Definition of HMAC_SESSION_LAST and POLICY_SESSION_LAST.
- Drop cast from TPM_ALG_XXX definitions
- Use mock functions with built-in cast to avoid compiler warnings from
manual cast.
- Free memory correctly on error condition return paths in InitSysContext
& SockServer.

## [1.2.0] - 2017-08-25
### Added
- Support for PTT-specific capabilities.
- Manuals with overviews for SAPI and TCTI layers & TCTI init functions.
- Further decomposition of the tpmclient program into an integration test
harness based on the automake infrastructure.
### Changed
- File list generated by bootstrap script is now sorted to play nice with
reproducible builds.
- Test harness now supports parallel execution of integration tests.
- libtcti-socket interrupted syscalls now resume.
- Additional hardening of compiler / linker flags.
- All options supported by `tpmclient` executable now removed.
- Unimplemented TCTI functions now return NOT_IMPLEMENTED RC.
### Fixed
- NULL dereference bugs in TCTI modules.
- Cleanup & structure initialization to keep coverity scans happy.
- Fixed memory leak in integration test harness.

## [1.1.0] - 2017-05-10
### Changed
- tpmclient, disabled all tests that rely on the old resourcemgr.
### Fixed
- Fixed definition of PCR_LAST AND TRANSIENT_LAST macros.
### Removed
- tpmtest
- resourcemgr, replacement is in new repo: https://github.com/01org/tpm2-abrmd

## [1.0] - 2016-11-01
### Added
- Travis-CI integration with GitHub
- Unit tests for primitive (un)?marshal functions.
- Example systemd unit for resourcemgr.
- Allow for unit tests to be enabled selectively.
- added pkg-config files for libraries
### Changed
- move simulator initialization code to socket TCTI init function.
- socket TCTI finalize no longer frees context
- rename libtss2 to libsapi
- rename libtcti_device to libtcti-device
- rename libtcti_socket to libtcti-socket
- move $(includedir)/tss to $(includedir)/sapi
- Move default compiler flags to config.site file.
### Fixed
- Fix run away resourcemgr threads by closing client sockets when resourcemgr
recv() call returns 0.
- Set MSG_NOSIGNAL for client connections to avoid SIGPIPE killing
resourcemgr.
- Fixes to handling of persistent objects by resourcemgr.
### Removed
- Semicolon from TPMA_* macros definitions.
- Windows build files.
- SAPI_CLIENT macro tests.
### Security
- Fix buffer overflow in resourcemgr.

## [0.98] - 2015-07-28
### Added
- Added ability for resource manager to communicate with a real TPM via
/dev/tpm0 (Linux only). Added command line switch to select simulator if not
communicating with a real TPM.
### Changed
- Rearranged directory structure in a more logical fashion.
- Changed name of Linux makefiles from "makefile.linux" to makefile. This was
done in preparation for autotools porting (future enhancement).
- Changed tpm library's windows makefile from "makefile" to "windows.mak".
- Changed all makefiles and Visual Studio solution and project files to work
with new directory structure.
- Split out debug and TPM platform command code in tpmsockets.cpp into
separate files. This code didn't belong in this file.

## [0.97] - 2015-??-??
### Added
- Added code to save context in RM table when an object is context loaded.
- Added code to get hierarchy from context when object is context loaded.
- Added targeted test to tpmclient.cpp to make sure that hierarchy is saved
- Added code to print level-specific messages when errors occur.
- Added test for EvictControl.Fixed TestEncryptDecryptSession to work with
1.22 simulator.
- Added code to check that TPM2B output parameters' size fields are set to 0
for following structures: TPM2B_ECC_POINT, TPM2B_PUBLIC, TPM2B_NV_PUBLIC, and
TPM2B_CREATION_DATA.
### Changed
- Fixed resource manager issues with leaving objects and session contexts in
TPM memory. This was causing a 902 error on 2nd pass of PolicyTests. And it
could have caused issues when error conditions occurred, because in those
cases, the contexts weren't being evicted.
- Changed TAB/RM into a separate executable (daemon).
- Fixed bug: if LoadContext fails when loading objects it should exit
ResourceMgrSendTpmCommand immediately. Instead it was loading other objects
and proceeding through the rest of ResourceMgrSendTpmCommand function.
correctly for ContextLoad command.
- Fixed issues with TCTI: opaque data shouldn't be defined in tss2_tcti.h
file.
- Fixed makefile issue: under Windows, it was using mkdir command instead of
md.
- Fixed issue with definition of TSS2_TCTI_POLL_HANDLE in tss2_tcti.h file.
- Fixed bug: wasn't handling case for TPM errors correctly in CheckPassed.
- Changed CheckOverflow to return SAPI error level for errors. Other levels of
TSS that call this function will alter the error level field.
- Fixed resource manager to properly handle EvictControl commands. Before, if
a persistent object was needed, the RM would give a 0xc0002 error.
- Fixed printf's in resource manager so that they only print the right # of
characters.
- Fixed TestShutdown to work with 1.22 simulator.

## [0.96] - 2015-04-16
### Added
- Added buffer overrun checks to all SAPI code.
- Added buffer overrun checks to resource manager code.
- Added code to Part 3 functions to properly handle null pointers for output
parameters.
### Changed
- Auto-generated most of the SAPI code from the TPM 2.0 specification.

## [0.95.1] - 2015-01-26
### Added
- Added code to dynamically work around simulator 1.19 bugs:
- Added code to RM and simDriver to support timeout on receive calls.
- Added code to properly handle TPM errors in ExecuteFinish. Previously it was
ignoring these errors, which meant that the rest of the _Complete call would
try to unmarshal non-existent response data. Added test case for this.
- Added support for cancel commands and tests for this.
- Added help text for command line options.
- Added code to reset dictionary attacks to start of tpmclient tests: this
works around an issue where the simulator doesn't seem to completely clear the
dictionary attack counter.
- Added support for TCTI setLocality to resource manager and sim driver and
made test app use this.
- Added RM tests.
- Added code to RM to evict contexts for objects, sequences, and sessions
whose handles are returned by commands.
- Added code to properly support ContextSave.
- Added proper error code levels to all RM errors.
- Added code to LoadContext function to output TPM formatted error codes.
- For Create and Load commands, added proper handling of errors if parent
handle not found.
- Added tests for bad session handle, both in handle area and in authorization
area.
- Added command line option to run the StartAuthSession tests by themselves.
- Added support for command line control of debug message levels.
- Added new error level for resource manager for errors received from TPM from
commands sent by RM.
- Added error return for insufficiently sized response to ExecuteFinish
function.
- Added gap support to resource manager.
- Added support to resource manager for kicking out oldest session if max
sessions have been started and a new one is being created.
- Added getCap calls to RM init function for getting max sessions and gap
limit.
- Added code to teardown the RM.
- Added test for session gapping.
- Added code to proactively detect MAX_ACTIVE_SESSIONS.
- Added SAPI library subproject to test app project. This allows a one-touch
build in Visual Studio.
- Added changes to return error codes from TAB/RM and layers underneath in a
response byte stream.
### Changed
- Fixed bug in CreatePrimary and Create: for one-call and decrypt session
case, they were copying first parameter from incorrect pointer.
- For CopyCreationDataOut, CopyECCPointOut, CopyNvPublicOut, CopyPublicOut
added placeholder for return code if size != 0 when called. To be filled in
when TSS WG decides on error code.
- Fixed bugs in CopySensitiveCreateIn and CopySensitiveIn: they shouldn't look
at the size.
- Fixed bugs in CopyECCPointIn, CopyNvPublicIn, CopyPublicIn, CopySensitiveIn,
and CopySensitiveCreateIn: not handling NULL outpul parameters correctly.
- Changes all instances of calls to ExecuteFinish to a timeout that works for
all cases including communicating with the simulator over the network.
- Fixed call to LoadExternal in TestUnseal: needed to pass in a NULL pointer
for the inSensitive parameter.
- Fixed bug in CreatePrimary: not passing correct pointer for inSensitive.
- Fixed timeouts for all ExecuteFinish calls in test application.
- Fixed bugs in RM: cases where I wasn't handling errors and then parsing data
that hadn't been received. Caused seg faults under Linux.
- Fixed timeout for async Startup test.
- Fixed SocketReceiveTpmResponse for blocking case.
- Fixed bug in ExecuteFinish: BAD_SEQUENCE error generated early in function
was getting overwritten by INSUFFICIENT_RESPONSE error.
- Fixed bug in ExecuteFinish: it was always setting timeout to 0 instead of
TSS2_TCTI_TIMEOUT_BLOCK.
- Fixed bug in resource manager: error level for non-TPM errors was getting
overwritten with resource manager error level.
- Replace Implementation.h with implementation.h.
- Changed name of TPMB.h tpmb.h
- GetCapability with bad property returns different error code.
- Shutdown with bad value for shutdownValue causes TPM to go into failure
mode.
- Fixed overlap in error codes: TSS2_BASE_RC_NOT_SUPPORTED and
TSS2_BASE_RC_BAD_TCTI_STRUCTURE had same value.
- Cleaned up all app level error codes.
- Fixed bug with ordering of -startAuthSessionTest command line parameter: if
it was not the last option, tpmclient would fail.
- Fixed bugs related to ContextLoad.
- Fixed bug in EvictContext: it was updating lastSessionSequenceNum even if
the ContextSave command failed.
- Fixed handling of RM errors that occur during command send.
- Fixed bug in simDriver init function. A second TCTI context being
initialized was re-initing the whole driver.
- Updated to latest 1.19 header files.
- Fixed bugs in resource manager:
- FindOldestSession wasn't working correctly: it was just finding the first
one.
- HandleGap needed to un-gap all the session contexts from the older interval.
It wasn't doing that.
- Fixed bug in handling of command line options: specifying none would cause
program to error out.
- Fixed issues in cleanup of TestStartAuthSession test. It was leaving some
sessions alive.
- Updated copyright notices on all files.
- Changed test app to use linked list of session structures instead of fixed
array. This fixed a host of issues.
- Fixed bugs in Certify, CertifyCreation, Commit, Create, CreatePrimary, and
GetCapability: if null used for return parameters, the function would fail.
- Fixed bug in SimpleHmacOrPolicyTest where it was re-creating the global
sysContext causing failures in later tests because the context was too small.
- Fixed a bug in ExecuteFinish. If response is too small, code was just using
the command buffer as the response buffer instead of returning an error.
- Fixed some places in test app where I wasn't deleting entries from the
sessions table.
- Fixed build warnings related to size mismatch of connectionId.
- Changed TeardownSysContext to zero out freed context pointer.
- This helps prevent double free errors.
- Fixed bug in EncryptDecryptXOR: wasn't setting the size of the outputData
buffer.
### Removed
- Removed 'extern "C"' statement from resourcemgr.c file. Not needed and
causes problems with some compilers.
- Removed unneeded includes from resource manager source.

## [0.95] - 2014-10-17
### Added
- Added support for Shutdown/Startup and effects on saved contexts.
- Added support for stClear bit objects. On a TPM Restart, objects with this
bit set will be removed from the TAB/RM entry list.
- Added TCTI teardown function.
- Added TAB functionality.
- Added TCTI layer below RM to talk to driver. This allows making calls into
the SAPI library from the RM without recursing into the RM again. With the
separate TCTI context, the RM can route SAPI calls to talk directly to the
driver. This fixed the virtual/real handle mess that was occurring with
recursively entering the RM.
- Added function pointers to TAB/RM for functions that might need to be
different based on the environment that TAB/RM is running in: malloc, free,
printf.
- Added and corrected error codes to match latest SAPI spec.
- Added MAX_NV_BUFFER_SIZE and used for max size of MAX_NV_BUFFER_2B.
- Added code to TestHash to calculate and validate a hash.
- Added code to TestHash to force a flush of an active sequence and then use
it to finish the hash calculation.
- Added code to SimpleHMACTest to read the NV index back.
- Added SimpleHMACOrPolicyTest function which helps illustrate the difference
between HMAC and policy sessions.
### Changed
- Fixed intermittent access violation bug with GetSetDecryptParamTests
function. I was reading off the end of the nvWrite buffer.
- Fixed bug in Tss2_Sys_GetContextSize function: it was getting the requested
size only, not the requested size plus the context blob's size. Problem was an
associativity issue with ternary conditional ?: operator.
- Re-architected TAB/RM:
- Changed RM from reactive mode to proactive mode. Now instead of reacting to
error codes from the TPM that indicate no enough slots, it guarantees that the
TPM is always ready for each command (all slots freed after execution of each
command).
- Replaced the fixed length arrays of RM structures with linked list
structures and appropriate functions.
- Fixed some cases of using pointers before checking that they're not NULL.
- Fixed bugs in marshaling/unmarshaling routines and added some missing
unmarshaling functions.
- Fixed hash sequence test.
- Fixed bugs in CopyCapabilityDataOut function for algorithms.
- Fixed bug with ExecuteAsync: passed in BE size to transmit call. Needs to be
host-endian.
- Changed on bit fields in TPM2 data structures to unsigned int. Previously
the compiler was generating incorrect code because these were int bit fields.
- Cleaned up TestHash function.
### Removed
- Removed most instances of sysContext in tpmclient.cpp. Now most tests use
the global one.
- Removed pack pragma from header files for external interfaces.

## [0.93] - 2014-08-01
### Added
- Added IsSession routine and fixed all instances in resource manager where a
handle is checked for being a session handle (some were incorrect).
- Added RollNonces function and used for all tests for HMAC and policy
sessions.
- Added TCTI malformed response error code.
- Added simple HMAC test.
- Added test for session parameter encryption and decryption.
- Added more descriptive error codes to StartAuthSession function.
- Added TpmHashSequence function. Used this build password/PCR policy.
- Added more policy tests: password/PCR, authValue, password
- Added code to flush context of session handles I'm not using.
- Added GetTestResult functions (had missed these previously)
- Added tests for asynchronous and synchronous non-one call to Startup tests.
- Added GetTestResult tests.
- Added test to create a bunch of sessions. This test found some resource
manager issues.
### Changed
- Fixed bad parameters on call to GetEncryptParam. This only failed on Linux
systems.
- Fixed minor build errors under Linux.
- Eliminated unneeded code in TestPolicy.
- Changed how nonce's are setup after StartAuthSession. Before they were being
inherently rolled in preparation for first command. Now the RollNonces routine
will need to be called before the first command. This makes handling of the
nonces consistent for all code that needs to roll them.
- Fixed bug in StartAuthSession: wasn't marshaling symmetric parameter
properly if algorithm was TPM_ALG_XOR.
- Fixed bug in SetDecryptParam: when inserting a decrypt param, the code
wasn't updating the command size field.
- Fixed bug in ExecuteFinish: wasn't returning TPM error code if no other
errors had occurred.
- Fixed bug in KDFa function: if key size was zero, this was just returning
success, but not generating a key. That behavior is specific to session key
generation not to the underlying KDFa function. Upleveled that code into
StartAuthSession function so that it only occurs in the session key generation
case.
- Changed NV attributes for all NV indices to add orderly attribute. This
helps, but doesn't entirely relieve, NV wearout issues with the tests.
- Changed NV attributes for all NV indices to add orderly attribute. This
helps, but doesn't entirely relieve, NV wearout issues with the tests.
- Fixed a bunch of resource manager issues. Many of these were exposed by the
new policy tests.
- Updated resource manager to properly handle sessions. Before we were not
swapping them in as needed.
- Updated readme.docx file. Now tests can run with V1.15 version of MS
simulator.
- Made test app work with MS simulator version 1.15. Had to add command to
turn on NV. Before this change, when running against MS simulator,
TPM2_Startup would fail with 0x923 error: "ERROR: WARNING,
TPM_RC_NV_UNAVAILABLE: the command may require writing of NV and NV is not
current accessible."
- Changed NO_RESPONSE_RECEIVED error code to IO_ERROR.
- Cleaned up defines for MS simulator commands.
### Removed?
- Removed an unused input parameter from ComputeCommandHmacs and
CheckResponseHmacs.
- Removed an unused input parameter from ComputeCommandHmacs and
CheckResponseHmacs.
- Removed DRIVER_NOT_FOUND and DRIVERINFO_NOT_FOUND error codes.

## [0.92] - 2014-06-17
### Changed
- Fixed bugs in sockets send and receive code. Needed to account for actual
bytes sent/received instead of assuming them. This was causing intermittent
errors when looping continuously on the tests and running the tests remotely
(on a different host system than the simulator was running on).
- Fixed SAPI and test app builds to not fail if directories are already
present. Suppressed error messages related to mkdir.
- Turned on compiler warnings and fixed all issues when building under Ubuntu
Linux.
- Fixed error in readme.docx file. I was specifying the wrong version of the
simulator.
- Fixed error handling if sockets interface fails to connect.
- Fixed build error: now I make directories that are needed.

## [0.91] - 2014-06-04
### Added
- Added code optimized builds to System API library code
- Added warning flags to compiler command lines.
### Changed
- Fixed all compiler warnings when built under Windows and Linux.

## [0.90] - 2014-05-28
### Added
- Added support for encrypt/decrypt sessions with one-call functions.
- Added cleaned up and reorganized header files that comply with latest SAPI
specification.
- Added changes for supporting get/set encrypt/decrypt functions.
- Added latest header file that corresponds to version 1.03 of TPM 2.0
specification.
- Added debug display of command string for each command being run.
- Added command line flag to slow down test display for demo purposes.
- Added option to loop the tests continuously.
### Changed
- Ported existing functionality to latest SAPI spec.
- Cleaned up and added comments to PasswordTest.
- Fixed problem of hang when looping through tests. Sessions table was running
out of entries because we weren't removing sessions that were closed.
- Fixed issue with resource manager. All virtual handles had the high nibble
set to 0xff. Now the high nibble is left intact so that applications can
determine the type of the handle.
### Notes
1. Testing is not comprehensive. See test code to see what's tested. Please
report any bugs found so that fixes can be rolled out.
2. Range checks within SAPI code not yet implemented.
3. Still need to add support for separate debug and production builds.
Production build will be optimized for code size.

## [0.82] - 2013-12-16
### Added
- Added support for building and running system API code and tests under
Linux.
- Added command line options for host name and port to test application.
### Notes
HMAC and cpHash calculations are only supported for NV Read and NV Write
commands currently. The system API changes to support this have been
prototyped for these commands and are awaitingTSS approval before being ported
to all the other commands.

## [0.81] - 2013-12-02
### Added
- Added support for TPM2_PolicyNvWritten command.
### Changed
- Altered tests to work with 1.01 simulator.
- Fixed errors in readme.docx.
### Notes
HMAC and cpHash calculations are only supported for NV Read and NV Write
commands currently. The system API changes to support this have been
prototyped for these commands and are awaitingTSS approval before being ported
to all the other commands.

## [0.80] - 2013-11-19
### Added
- Added code to create a new session for reading/writing the NV index after
it's first written. This tests the other case for bound sessions.
- Added routine to start policy sessions.
- Added policy test code: not used currently.
### Changed
- Fixed bugs in resource manager.
- Fixed bugs with salted session tests.
- Ported tests to work with 0.99 sim's version of support for bound sessions.
- Fixed bugs in test code, with how key is generated for encrypting the salt
for salted session tests.
- Fixed a rather serious bug in HmacSessionTest: CopyNvPublicIn is called to
copy a structure, but is had the side effect of modifying the first parameter.
This function really wasn't designed to be used the way it is. Worked around
the problem by resetting the pointer after calling CopyNvPublicIn. This
problem showed up as a stack corruption issue that occurred during the 4th
test. Basically the pointer moved enough after the first 3 tests to start
corrupting other variables on the stack.
- Automated runtime setup of key for salted tests.
- Developed changes for NVRead/Write commands to use new 2-stage method for
handling HMAC calculations.
- Changed CopyPcrSelectionIn function so that it can be used by applications
to generate policy hashes.
- Fixed build error: changes in header files weren't causing TPM 2.0 library
functions to be rebuilt.
- Created CalcPHash helper function.
- Changed HMAC session code to new architecture that doesn't use any helper
function pointers.
- Changed return code type form UINT32 to TPM_RC in tss_sysapi.h.
- Changed "authHandle" to "sessionHandle" in sample code.
- Debugged and fixed StartAuthSession2 function in test code.
- Debugged and fixed first policy test.
- Used new NvDefine function to help abstract some of the details of creating
NV indices.
- Used non-MS header file to build system API.
- Cleaned up and reorganized files and directories.
### Notes
HMAC and cpHash calculations are only supported for NV Read and NV Write
commands currently. The system API changes to support this have been
prototyped for these commands and are awaitingTSS approval before being ported
to all the other commands.

## [0.67] - 2013-08-07
### Added
- Plumbed in a resource mgr (doesn't actually do anything other than pass
through at this time).
- Added BOUND and SALTED HMAC session tests. BOUND test works, but SALTED
doesn't yet work.
- Added code to delete an entity from the entity table.
- Added code to work around an NV index anomaly with TPM simulator 0.98 and
previous versions: after the first NV index write, the name changes. This
causes the TPM's HMAC calculation to treat the index as if it's never the
BOUND entity, even if it is. This is expected (but weird) behavior which will
be fixed in 0.99 simulator.
- Created two helper functions pointers for system API and used them for HMAC
sessions.
- Added support for HMAC session for NV read/write APIs.Added HMAC tests for
unbounded/unsalted sessions.Fixed context save/restore functions.Created
CopyNvPublicIn function and altered Tpm2_DefineSpace function to use it.
- Created TpmHash function
- Created TpmHandleToName function
- Added HMAC tests for unbounded/unsalted sessions.
- Created CopyNvPublicIn function and altered Tpm2_DefineSpace function to use
it.
- Created TpmHash function
- Created TpmHandleToName function
- Documented helper function pointers in the system API header file.
- Added tests for TpmHandleToName function.
- Added functionality needed for KDFa functions ConcatSizedByteBuffer,
CopySizedByteBuffer
- Added KDFa function in preparation for HMAC session test. Not tested yet.
- Added LoadExternalHMACKey function. This function is called by TPM HMAC
function.
### Changed
- Updated headers with Intel license text.
- Split sockets driver into separate code module.
- SALTED session test fixes:
  * Fixed CopyRSAEncryptIon function: wasn't handling some cases correctly.
  * Backed out change to make parameterSize passed to ComputeSessionHmacPtr
function a UINT16. Needs to be UINT32.
  * For ComputeSessionHmacPtr, changed parameterSize to UINT16 to fix build
warning.
- Fixed bugs in KDFa().
- Altered all APIs to use pointers to TPM input/output buffers.
- Fixed context save/restore functions.
- Fixed formatting of prints of sized byte buffers in test app.
- Fixed bug in TpmHmac function: needed to set size of result to 0 in case an
error occurs.
- Fixed bugs in CopySensitiveIn function: uninitialized size field, bad
pointers, and incorrect increment of otherData at end of function.
- Altered TpmHMAC function to call LoadExternalHMAC key function. This
allows a better HMAC function pointer, one that complies with normal HMAC
calling convention. Before it was TPM-specific.
- Bumped up TPMBUF_LEN to 32k in tpmclient.cpp. This fixed overwriting
problems during context save/restore function.
- Fixed bugs in ContextLoad function: otherData wasn't initialized before it
was used.
- Fixed bug in Tpm20LoadExternal command: it wasn't properly marshaling the
inPrivate data.
### Removed
- Removed tis.h file. Not needed.
- Eliminated salted session test (because it doesn't work yet), and changed
out.good file to match.
- Reorganized directories and moved files to make more logical sense.
### Notes
HMAC helper function callouts are only being done for NV Read and NV
Write commands currently. The system API changes to support this are still
being prototyped. After they are finalized, these changes will be extended to
all functions that use sessions.

## [0.66] - 2013-??-??
### Added
- Added CertifyCreation function
- Added EcEphemeral function
- Added test for tspi_sys_TPM2_HashStart
### Changed
- Cleaned up for general TCG release

## [0.65] - 2013-04-10
### Added
- All TPM 2.0 functions now supported.
- Limited testing done on following functions:
- tspi_sys_TPM2_Startup
- tspi_sys_Tpm2_SelfTest
- tspi_sys_TPM2_GetCapability
- tspi_sys_TPM2_Clear-tested
- tspi_sys_TPM2_StartAuthSession
- tspi_sys_TPM2_ClearControl
- tspi_sys_TPM2_ChangeEPS
- tspi_sys_TPM2_HierarchyChangeAuth
- tspi_sys_TPM2_Extend
- tspi_sys_TPM2_HashSequenceStart
- tspi_sys_TPM2_SequenceUpdate
- tspi_sys_TPM2_SequenceComplete
- tspi_sys_TPM2_EventSequenceComplete
- tspi_sys_TPM2_GetRandom
- tspi_sys_TPM2_SaveState
- tspi_sys_TPM2_PcrRead
- tspi_sys_TPM2_NVRead
- tspi_sys_TPM2_NVWrite
- tspi_sys_TPM2_Unseal
- tspi_sys_TPM2_PcrAllocate
- tspi_sys_TPM2_DictionaryAttackLockReset
- tspi_sys_TPM2_NV_Writelock
- tspi_sys_TPM2_PolicyCommandCode
- tspi_sys_TPM2_PolicyGetDigest
- tspi_sys_TPM2_PolicyOr
- tspi_sys_TPM2_PolicyRestart
- tspi_sys_TPM2_LoadExternal
- tspi_sys_TPM2_HierarchyControl
- tspi_sys_TPM2_NV_UndefineSpace
- tspi_sys_TPM2_Create
- tspi_sys_TPM2_Load
- tspi_sys_TPM2_Quote
- tspi_sys_TPM2_NV_ReadPublic
- tspi_sys_TPM2_ChangePPS
- tspi_sys_TPM2_NV_DefineSpace
- tspi_sys_TPM2_PolicyLocality
- tspi_sys_TPM2_PolicyPCR
- tspi_sys_TPM2_CreatePrimary
- tspi_sys_TPM2_Shutdown
- tspi_sys_TPM2_PCR_Event
- tspi_sys_TPM2_PolicyNV
- tspi_sys_TPM2_NV_ReadLock
- tspi_sys_TPM2_NV_UndefineSpaceSpecial
No testing done on all other 61 functions

## [0.60] - 2013-03-29
### Added
- Added changes to make it comply with TSS 2.0 system library API
### Removed
- Cleaned up and removed unneeded files.
