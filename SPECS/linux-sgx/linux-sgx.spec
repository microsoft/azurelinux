## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 10;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


# The enclave code must be built with very specific build
# flags, that are different from what is used to build
# native code. Thus we cannot globally set the CFLAGS etc
%undefine _auto_set_build_flags

# When -flto is set, something (possibly cmake related)
# causes the build of psw/ae/aesm_service to add -fpie
# to the build flags. This conflicts with the need to
# build everything with -fPIC, and causes linker failures
#
# /usr/bin/ld: /tmp/ccWKJhwL.ltrans0.ltrans.o: warning: relocation against `stdout@@GLIBC_2.2.5' in read-only section `.text.sgx_proc_log_report'
# /usr/bin/ld: /tmp/ccWKJhwL.ltrans0.ltrans.o: relocation R_X86_64_PC32 against symbol `_Z16aesm_thread_procPv' can not be used when making a shared object; recompile with -fPIC
%global _lto_cflags %nil

############################################################
#
# Note about the approach to bundling...
#
# The linux-sgx project build system is written with the assumption
# that a monolithic repo is being used with all dependencies
# present at specific versions and in particular locations.
#
# Fully untangling this is impractical/unsustainable, because the
# build system in fact has circular dependencies between what might
# otherwise look like independent projects. ie linux-sgx depends
# on headers from dcap, but dcap depends on headers from linux-sgx.
# In addition, some of the 3rd party projects that are consumed are
# patched with SGX enclave specific changes.
#
# For enclave builds, there will be no ability to share existing
# binaries built for native Fedora, as everything must be built
# for the enclave environment, with its own C runtime. Thus trying
# to unbundle has little benefit for enclave related dependencies.
#
# This package is thus written such
#
#   * All the SGX related projects provided by Intel are bundled
#     whether used for enclave or native OS code.
#   * SGX enclave code is built with bundled 3rd party projects.
#   * Native OS code is built with system packages for non-SGX
#     related dependancies.
#
# Focusing on unbundling only 3rd party projects involved in native
# builds maximises the benefits of system package usage, without an
# unreasonable burden fighting the build system for enclave pieces.

%global with_aesm 0
%global with_host_tinyxml2 0
%if 0%{?fedora}
%global with_aesm 1
%global with_host_tinyxml2 1
%endif

%global with_sysusers_scripts 0
%if 0%{?rhel} <= 10
%global with_sysusers_scripts 1
%endif

# Change after running pccs-nodejs-bundler
%define node_modules_date 20260204

############################################################
#
# A note about versions
#
# When rebasing to new linux-sgx releases, bump all the following
# versions based on what the new release depends on (see various
# "git submodule status --recursive" tags and/or code files).
#
# The 'download.sh' script can be used to automate downloading
# of new tarballs after updating the versions, as well as stripping
# non-permitted content from some tarballs.
#
%global linux_sgx_version 2.27
# From submodule: external/dcap_source
%global dcap_version 1.24
# From submodule: external/dcap_source/QuoteVerification/QVL
# NB: follows DCAP versioning, but may skip releases
%global dcap_qvl_version 1.24
# From script: external/sgxssl/prepare_sgxssl.sh
# Should match: external/dcap_source/QuoteVerification/prepare_sgxssl.sh
%global sgx_ssl_version 3.0_Rev5.1
# From submodule: external/ippcp_internal/ipp-crypto
%global ipp_crypto_version 2021.12.1
# From submodule: external/sgx-emm/emm_src
%global sgx_emm_version 1.0.3
# From submodule: external/dcap_source/QuoteGeneration/pccs
# NB: follows DCAP versioning, but may skip releases
%global pccs_version 1.24

# From script: external/sgxssl/prepare_sgxssl.sh
# Should match: external/dcap_source/QuoteVerification/prepare_sgxssl.sh
%global openssl_version 3.0.17
# From submodule: external/cbor/libcbor
%global libcbor_version 0.10.2
# From submodule: external/protobuf/protobuf_code/third_party/abseil-cpp
%global abseil_cpp_version 20230125.3
# From submodule: external/dcap_source/external/jwt-cpp
%global jwt_cpp_version 0.6.0
# From submodule: external/dcap_source/external/wasm-micro-runtime
%global wamr_version 2.4.3
# From code: external/tinyxml2/
%global tinyxml2_version 10.0.0

# From docs: external/epid-sdk/CHANGELOG.md
%global epid_version 6.0.0
# From script: external/rdrand/src/configure.ac
%global rdrand_version 1.1
%global vtune_version 2018

# enclaves from prebuilt_dcap_NNN.tar.gz - DCAP version numbers,
# except for pce, which is actually an SGX enclave just bundled
# with the DCAP enclaves.
%global enclave_pce_version 2.25
%global enclave_ide_version 1.22
%global enclave_qe3_version 1.22
%global enclave_tdqe_version 1.22
%global enclave_qve_version 1.24

# Whether to build & ship unsigned enclaves with latest distro
# tool-chain, as opposed to a reproducible build done in other
# packages
%global with_enclaves 1

# Provisioning Certification Enclave. Required. ECDSA quote signing
%global with_enclave_pce 1

# ID Enclave. Required. Hardware identification
%global with_enclave_ide 1

# Quoting Enclave. Required for non-TDX usage. ECDSA quote generation
%global with_enclave_qe3 1

# Quoting Enclave. Required for TDX usage. ECDSA quote generation
%global with_enclave_tdqe 1

# Quote Verification Enclave. Optional. ECDSA quote verification
#
# Note this package has removed the unapproved crypto this
# enclave links to in upstream builds, to make it possible
# to ship in Fedora.
%global with_enclave_qve 1


%global _with_enclave_pce %{expr:%{with_enclaves} ? %{with_enclave_pce} : 0}
%global _with_enclave_ide %{expr:%{with_enclaves} ? %{with_enclave_ide} : 0}
%global _with_enclave_qe3 %{expr:%{with_enclaves} ? %{with_enclave_qe3} : 0}
%global _with_enclave_tdqe %{expr:%{with_enclaves} ? %{with_enclave_tdqe} : 0}
%global _with_enclave_qve %{expr:%{with_enclaves} ? %{with_enclave_qve} : 0}


# We prefer deployments using the pre-built enclaves
# signed by Intel, but permit replacing with enclaves
# signed by a different party
%global enclave_requires() \
Requires: sgx-enclave(%1:signed) >= %2 \
Recommends: sgx-enclave(%1:signed:prebuilt) >= %2

Name:           linux-sgx
Version:        %{linux_sgx_version}
Release:        %autorelease
Summary:        Intel Linux SGX SDK and Platform Software

# The project pulls together source from a wide variety of places,
# so while the license of the combined work is declared to be
# BSD-3-Clause, there is actually a huge set of licenses to track
License: %{shrink:
  %dnl node_modules
  0BSD AND

  %dnl sdk/tlibcxx, external/ippcp_internal, external/epid-sdk, node_modules
  Apache-2.0 AND

  %dnl node_modules
  BlueOak-1.0.0 AND

  %dnl sdk/cpprt, sdk/tlibc, node_modules
  BSD-2-Clause AND

  %dnl external/dcap_source, sdk/*, node_modules
  BSD-3-Clause AND

  %dnl sdk/tlibc
  BSD-4-Clause AND

  %dnl sdk/tlibc
  BSD-4-Clause-UC AND

  %dnl psd/urts/linux/isgx_user.h
  GPL-2.0-only AND

  %dnl sdk/tlibc, sdk/pthread, node_modules
  ISC AND

  %dnl external/cbor/libcbor, sdk/*, node_modules
  MIT AND

  %dnl sdk/tlibc/stdlib/malloc.c
  MIT-0 AND

  %dnl sdk/compiler-rt
  NCSA AND

  %dnl sdk/protected_code_loader
  OpenSSL AND

  %dnl sdk/tlibc/gdtoa
  SMLNJ AND

  %dnl sdk/tlibc/math
  SunPro AND

  %dnl node_modules
  Unlicense AND

  %dnl node_modules
  WTFPL AND

  %dnl sdk/tlibc
  LicenseRef-Fedora-Public-Domain
}

URL:            https://github.com/intel/linux-sgx


############################################################
# SGX related projects SourceN for N in (0..9)

Source0: https://github.com/intel/linux-sgx/archive/refs/tags/sgx_%{linux_sgx_version}.tar.gz#/linux-sgx-%{linux_sgx_version}.tar.gz

# repack.sh purges all the prebuilt AE's that we ship in a different RPM
# as well as 'prebuilt/' content (openssl / OPA binaries) that we must
# not distribute.
Source1: repack.sh

Source2: https://github.com/intel/confidential-computing.tee.dcap/archive/refs/tags/DCAP_%{dcap_version}.tar.gz
Provides: bundled(dcap) = %{dcap_version}

# Upload tarball is:
#
#   https://download.01.org/intel-sgx/sgx-dcap/%{dcap_version}/linux/prebuilt_dcap_%{dcap_version}.tar.gz
#
# but is then post-processed using repack.sh to create this
Source3: prebuilt_dcap_%{dcap_version}-repacked.tar.gz

Source4: https://github.com/intel/intel-sgx-ssl/archive/refs/tags/%{sgx_ssl_version}.tar.gz#/intel-sgx-ssl-%{sgx_ssl_version}.tar.gz
Provides: bundled(sgxssl) = %{sgx_ssl_version}

Source5: https://github.com/intel/ipp-crypto/archive/refs/tags/ippcp_%{ipp_crypto_version}.tar.gz
Provides: bundled(ipp-crypto) = %{ipp_crypto_version}

Source6: https://github.com/intel/sgx-emm/archive/refs/tags/sgx-emm-%{sgx_emm_version}.tar.gz
Provides: bundled(sgx-emm) = %{sgx_emm_version}

Source7: https://github.com/intel/confidential-computing.tee.dcap.qvl/archive/refs/tags/DCAP_%{dcap_qvl_version}.tar.gz#/dcap-qvl-%{dcap_qvl_version}.tar.gz
Provides: bundled(dcap-qvl) = %{dcap_qvl_version}

Source8: https://github.com/intel/confidential-computing.tee.dcap.pccs/archive/refs/tags/DCAP_%{pccs_version}.tar.gz#/pccs-%{pccs_version}.tar.gz
Provides: bundled(pccs) = %{pccs_version}


############################################################
# 3rd party projects SourceN for N in (10..19)

Source10: https://www.openssl.org/source/openssl-%{openssl_version}.tar.gz
Provides: bundled(openssl) = %{openssl_version}

Source11: https://github.com/PJK/libcbor/archive/refs/tags/v%{libcbor_version}.tar.gz#/libcbor-%{libcbor_version}.tar.gz
Provides: bundled(libcbor) = %{libcbor_version}

# XXX unbundle me, only used in native code, or also in enclaves ?
Source12: https://github.com/Thalhammer/jwt-cpp/archive/refs/tags/v%{jwt_cpp_version}.tar.gz#/jwt-cpp-%{jwt_cpp_version}.tar.gz
Provides: bundled(jwt-cpp) = %{jwt_cpp_version}

Source13: https://github.com/bytecodealliance/wasm-micro-runtime/archive/refs/tags/WAMR-%{wamr_version}.tar.gz#/wasm-micro-runtime-%{wamr_version}.tar.gz
Provides: bundled(wasm-micro-runtime} = %{wamr_version}

Source14: https://github.com/leethomason/tinyxml2/archive/refs/tags/%{tinyxml2_version}.tar.gz#/tinyxml2-%{tinyxml2_version}.tar.gz
%if ! %{with_host_tinyxml2}
Provides: bundled(tinyxml2) = %{tinyxml2_version}
%endif


############################################################
# Misc distro integration files SourceN in (40..59)

Source40: aesmd.sysusers.conf
Source41: aesmd.service

Source42: sgxprv.sysusers.conf
Source43: 92-sgx-provision.rules

Source44: qgs.sysusers.conf
Source45: qgs.service
Source46: qgs.sysconfig

Source48: mpa_registration.service

Source50: pccs.sysusers.conf
Source51: pccs.service
# RPM build doesn't run this, but we want it in the src.rpm
# as record of what was used to create Source54
Source52: pccs-nodejs-bundler
# Pre-created using Source53
Source53: pccs-%{dcap_version}-%{node_modules_date}-node-modules.tar.xz

############################################################
# External projects that have been copied in tarballs as bundles

# In external/epid-sdk/
Provides: bundled(epid-sdk) = 6.0.0
# In external/rdrand/
Provides: bundled(RdRand) = 1.1
# In external/vtune/
Provides: bundled(vtune) = 2018

############################################################
# Distro integration patches

# 0000-0099 -> against confidential-computing.sgx-sgx.git
#
# Maintained in: https://github.com/berrange/linux-sgx/tree/dist-git-%{linux_sgx_version}-hostsw
#
Patch0000: 0000-Add-support-for-building-against-host-openssl-crypto.patch
Patch0001: 0001-Add-support-for-building-against-host-tinyxml2-lib.patch
Patch0002: 0002-Add-support-for-building-against-host-CppMicroServic.patch
# https://github.com/intel/linux-sgx/pull/1055
Patch0003: 0003-Improve-make-debuggability.patch
Patch0004: 0004-Support-disabling-use-of-git-for-ippcp-code.patch
Patch0005: 0005-disable-openmp-protobuf-sample_crypto-builds.patch
# https://github.com/intel/linux-sgx/pull/1056
Patch0006: 0006-Fix-escaping-of-regexes-in-sgx-asm-pp.patch
# https://github.com/intel/linux-sgx/pull/1064
Patch0007: 0007-psw-prefer-dev-sgx_provision-dev-sgx_enclave.patch
Patch0008: 0008-psw-fix-soname-for-libuae_service.so-library.patch
Patch0009: 0009-pcl-remove-redundant-use-of-bool-type.patch
Patch0010: 0010-sdk-honour-CFLAGS-LDFLAGS-set-from-environment.patch
Patch0011: 0011-psw-make-aesm_service-build-verbose.patch
Patch0012: 0012-Fix-modern-C-function-prototype-compliance.patch
Patch0013: 0013-Add-wrapper-for-nasm-to-fix-cmake-compat.patch
Patch0014: 0014-fix-BOM-for-pccs-with-DCAP.patch
Patch0015: 0015-sdk-avoid-failure-due-to-attribute-regparam-with-GCC.patch
Patch0016: 0016-Add-impl-of-__cxa_call_terminate.patch
Patch0017: 0017-fix-BOM-for-mpa_manage-mpa_registration-files.patch
# Optional patches
Patch0050: 0050-Disable-inclusion-of-AESM-in-installer.patch


# 0100-0199 -> against confidential-computing.tee.dcap.git
#
# Maintained in https://github.com/berrange/SGXDataCenterAttestationPrimitives/tree/dist-git-%{dcap_version}-hostsw
#
Patch0100: 0100-Drop-use-of-bundled-pre-built-openssl.patch
Patch0101: 0101-Improve-debuggability-of-build-system.patch
# https://github.com/intel/SGXDataCenterAttestationPrimitives/pull/437
Patch0102: 0102-Support-build-time-setting-of-enclave-load-directory.patch 
# https://github.com/intel/SGXDataCenterAttestationPrimitives/pull/434
Patch0103: 0103-Look-for-versioned-sgx_urts-library-in-PCKRetrievalT.patch
# https://github.com/intel/SGXDataCenterAttestationPrimitives/pull/429
Patch0104: 0104-pcsclient-only-import-pypac-module-on-Windows.patch
Patch0105: 0105-Look-for-PCKRetrievalTool-config-file-in-etc.patch
Patch0106: 0106-Honour-CFLAGS-CXXFLAGS-LDFLAGS-for-various-tools-and.patch
# https://github.com/intel/SGXDataCenterAttestationPrimitives/pull/428
Patch0107: 0107-qgs-add-space-between-program-name-first-arg-in-usag.patch
Patch0108: 0108-qgs-protect-against-format-strings-in-QL-log-message.patch
Patch0109: 0109-qgs-add-debug-parameter-to-control-logging.patch
Patch0110: 0110-pcsclient-remove-leftover-debugging-print-args-state.patch
Patch0111: 0111-Fix-soname-version-for-libsgx_qe3_logic.so-library.patch
Patch0112: 0112-Workaround-broken-GCC-15.patch
Patch0113: 0113-Don-t-disable-cf-protection-for-qgs.patch
Patch0114: 0114-Delete-broken-checks-for-GCC-version-that-break-fsta.patch
#Patch0115: 0115-Use-distro-provided-rapidjson-package.patch
Patch0116: 0116-Don-t-stomp-on-VERBOSE-variable.patch
Patch0117: 0117-qgs-add-m-MODE-parameter-for-UNIX-socket-mode.patch
Patch0118: 0118-pcsclient-make-keyring-module-optional.patch
Patch0119: 0119-pcsclient-convert-from-asn1-to-pyasn1-python-module.patch
Patch0120: 0120-pcsclient-fully-switch-to-pycryptography-for-CRL-ver.patch
Patch0121: 0121-pcsclient-use-more-of-pycryptography-instead-of-pyop.patch
Patch0122: 0122-pcsclient-prefer-pycryptography-over-pyopenssl.patch
Patch0123: 0123-pcsclient-add-fallback-for-when-pyopenssl-is-not-ava.patch
Patch0124: 0124-pcsclient-ignore-errors-trying-to-clear-the-keyring.patch
# https://github.com/intel/confidential-computing.tee.dcap/pull/485
Patch0125: 0125-PCS-Client-Tool-Migrate-from-deprecated-pkg_resource.patch
# https://github.com/intel/confidential-computing.tee.dcap/pull/487
Patch0126: 0126-qgs-add-compat-for-boost-1.87-which-drops-asio-io_se.patch
Patch0127: 0127-qgs-add-compat-for-boost-1.89-which-deprecated-deadl.patch
Patch0128: 0128-use-system-gtest-gmock-libraries.patch
Patch0129: 0129-Disable-PcsClientTool-package-build.patch
Patch0130: 0130-disable-building-of-WASM-SIMDE-code.patch
Patch0131: 0131-pcsclient-fix-name-of-input-file-in-cache-command-he.patch


# 0200-0299 -> against intel-sgx-ssl.git
#
# Maintained in https://github.com/berrange/intel-sgx-ssl/tree/dist-git-%{sgx_ssl_version}
#
Patch0200: 0200-Enable-pointing-sgxssl-build-to-alternative-glibc-he.patch
Patch0201: 0201-Workaround-missing-output-directory.patch
Patch0202: 0202-Disable-various-EC-crypto-features.patch
Patch0203: 0203-Disable-sm2-and-sm4-crypto-algorithms.patch


# 0300-0399 -> against ipp-crypto.git
#
# Maintained in https://github.com/berrange/ipp-crypto/tree/dist-git-%{ipp_crypto_version}
#
Patch0300: 0300-Drop-min-openssl-from-3.0.8-to-3.0.7.patch
Patch0301: 0301-Drop-Werror-from-build-flags.patch


# 0400-0499 -> against confidential-computing.tee.dcap.pccs.git
#
# Maintained in https://github.com/berrange/confidential-computing.tee.dcap.pccs/tree/dist-git-%{pccs_version}
#
Patch0400: 0400-service-sanitize-paths-to-all-resources.patch
Patch0401: 0401-pccsadmin-remove-leftover-debugging-print-args-state.patch
Patch0402: 0402-pccsadmin-make-keyring-module-optional.patch
Patch0403: 0403-pccsadmin-ignore-errors-trying-to-clear-the-keyring.patch
Patch0404: 0404-service-force-override-tar-module-to-7.0.0-series.patch

BuildRequires: sgx-rpm-macros
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: binutils
BuildRequires: chrpath
BuildRequires: libtool
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: cmake
BuildRequires: ocaml
BuildRequires: ocaml-ocamlbuild
BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: libcurl-devel
BuildRequires: python3-devel
BuildRequires: perl-generators
BuildRequires: perl-interpreter
BuildRequires: perl-devel
BuildRequires: perl(FindBin)
BuildRequires: perl(lib)
BuildRequires: perl(IPC::Cmd)
BuildRequires: nasm
# XXX nodejs-packaging needs fixing to auto-add 'Requires: nodejs(abi) == XX'
# then this can be reduced to only 'BuildRequires: nodejs, /usr/bin/node'
# See also https://src.fedoraproject.org/rpms/linux-sgx/pull-request/6
# Match this version with later 'Requires: nodejsXX' against sgx-pccs
%if 0%{?fedora} >= 44 || 0%{?rhel} >= 11
BuildRequires: nodejs24-devel, /usr/bin/node, /usr/bin/npm
%else
# npm in RHEL 9, nodejs-npm in RHEL 10 and F<44
BuildRequires: nodejs-devel, /usr/bin/node, /usr/bin/npm
%endif
BuildRequires: nodejs-packaging
BuildRequires: python-unversioned-command
BuildRequires: sqlite-devel
BuildRequires: systemd-rpm-macros
%if %{with_host_tinyxml2}
BuildRequires: tinyxml2-devel
%endif
%if %{with_aesm}
BuildRequires: CppMicroServices-devel
%endif
#BuildRequires: rapidjson-devel
BuildRequires: protobuf-compiler
BuildRequires: protobuf-devel
BuildRequires: boost-devel
BuildRequires: gtest-devel
BuildRequires: gmock-devel

# If dpkg-architecture exists in $PATH, the Makefile
# will change all the install paths, breaking this
# spec's expected locations
BuildConflicts: dpkg-dev

# SGX is a technology that only exists in Intel x86 CPUs
ExclusiveArch: x86_64

%description
The Intel SGX SDK is a collection of APIs, libraries, documentations and
tools that allow software developers to create and debug Intel SGX 
enabled applications in C/C++.

%package -n sgx-common
Summary: Intel SGX SDK & runtime common

%description -n sgx-common
Common files for the Intel SGX SDK & runtime

# We only provide the unsigned enclaves. The pre-built
# signed enclaves and shipped separately for ease of
# updating
%global do_package() \
%if %2 \
%package -n sgx-enclave-latest-%1-unsigned \
Summary: SGX %1 enclave (unsigned, latest tool-chain) \
\
Provides: sgx-enclave(%1:unsigned) = %3 \
Provides: sgx-enclave(%1:unsigned:latest) = %3 \
Requires: sgx-common = %{version}-%{release} \
\
%description -n sgx-enclave-latest-%1-unsigned \
This package contains the unsigned SGX %1 enclave, \
built with latest tool-chain and libraries. \
\
%endif

%do_package pce %{_with_enclave_pce} %{linux_sgx_version}
%do_package ide %{_with_enclave_ide} %{dcap_version}
%do_package qe3 %{_with_enclave_qe3} %{dcap_version}
%do_package tdqe %{_with_enclave_tdqe} %{dcap_version}
%do_package qve %{_with_enclave_qve} %{dcap_version}

%package -n sgx-enclave-devel
Summary: SGX enclave libraries development
Requires: sgx-libs = %{version}-%{release}

%description -n sgx-enclave-devel
This package contains the header files, libraries and tools required
to create SGX enclaves.


%package -n sgx-devel
Summary: SGX platform libraries development
Requires: sgx-libs = %{version}-%{release}

%description -n sgx-devel
This package contains the header files, libraries and tools required
to build applications that interact with SGX enclaves on the platform.


%package -n sgx-libs
Summary: SGX platform libraries runtime
Requires: sgx-common = %{version}-%{release}

%description -n sgx-libs
This package contains the runtime libraries and tools required
to run applications that interact with SGX enclaves on the platform.


%if %{with_aesm}
%package -n sgx-aesm
Summary: SGX platform Architectural Enclave Service Manager
Requires: CppMicroServices
Requires: sgx-libs = %{version}-%{release}

Suggests: sgx-enclave(pce:signed) >= %{enclave_pce_version}
Suggests: sgx-enclave(qe3:signed) >= %{enclave_qe3_version}
Suggests: sgx-enclave(qve:signed) >= %{enclave_qve_version}
Suggests: sgx-enclave(ide:signed) >= %{enclave_ide_version}
Suggests: sgx-enclave(tdqe:signed) >= %{enclave_tdqe_version}

%description -n sgx-aesm
This package contains the  Architectural Enclave Service Manager
(AESM) daemon.
%endif


%package -n sgx-pccs
Summary: SGX Provisioning Certificate Caching Service
%if 0%{?fedora} >= 44 || 0%{?rhel} >= 11
Requires: nodejs24
%else
Requires: nodejs
%endif
Requires: sgx-common = %{version}-%{release}

%description -n sgx-pccs
SGX Provisioning Certificate Caching Service


%package -n sgx-pccs-admin
Summary: SGX Provisioning Certificate Caching Service Admin Tool
%if 0%{?fedora}
Requires: python3-keyring
%endif
Requires: python3-requests
Requires: python3-urllib3
Requires: python3-packaging
Requires: sgx-common = %{version}-%{release}
# pccs admin tool can be used against a remote pccs
# so don't force a hard dep
Recommends: sgx-pccs = %{version}-%{release}

%description -n sgx-pccs-admin
SGX Provisioning Certificate Caching Service Admin Tool


%package -n sgx-pcs-client
Summary: SGX Provisioning Certificate Service Client Tool
Requires: python3-pyasn1
Requires: python3-cryptography
%if 0%{?fedora}
Requires: python3-keyring
%endif
Requires: python3-requests
Requires: python3-urllib3
Requires: python3-packaging
%if 0%{?rhel}
Requires: openssl
%endif

%description -n sgx-pcs-client
SGX Provisioning Certificate Service Client Tool


%package -n sgx-pckid-tool
Summary: SGX PCK Cert ID Retrieval Tool
Requires: sgx-libs = %{version}-%{release}
%enclave_requires ide %{enclave_ide_version}
%enclave_requires pce %{enclave_pce_version}

%description -n sgx-pckid-tool
SGX PCK Cert ID Retrieval Tool


%package -n sgx-mpa
Summary: SGX Multi-package Registration Agent
Requires: sgx-libs = %{version}-%{release}

%description -n sgx-mpa
SGX Multi-package Registration Agent


%package -n tdx-qgs
Summary: TDX Quoting Generation Service
Requires: sgx-libs = %{version}-%{release}
# mpa provides auto-registration of the platform, if it
# is enabled in EFI. If not enabled, it is a no-op so
# safe to have installed by default regardless, but use
# weak dep to allow skipping for optimized installs
Recommends: sgx-mpa = %{version}-%{release}
# If auto-registration is not enabled, the pckid-tool
# is needed for manual registration; it is also useful
# misc admin tasks
Recommends: sgx-pckid-tool = %{version}-%{release}
# In internet isolated hosts pccs can be used to
# provide pre-cached certs, either running it on
# localhost or on the LAN. Weak dep though as it
# is expected that LAN deployment is more common
Suggests: sgx-pccs = %{version}-%{release}

%enclave_requires ide %{enclave_ide_version}
%enclave_requires pce %{enclave_pce_version}
%enclave_requires tdqe %{enclave_tdqe_version}


%description -n tdx-qgs
TDX Quoting Generation Service


%package -n tdx-attest-libs
Summary: TDX attestation libraries
Requires: sgx-common = %{version}-%{release}

%description -n tdx-attest-libs
TDX attestation libraries

This assists guest applications in attesting
their virtual machine environment.


%package -n tdx-attest-devel
Summary: TDX attestation libraries development
Requires: tdx-attest-libs = %{version}-%{release}

%description -n tdx-attest-devel
TDX attestation libraries development

This enables integration of support for attestation
in applications


%prep
%setup -q -n confidential-computing.sgx-sgx_%{linux_sgx_version}

%autopatch -m 0 -M 49 -p1
%if !%{with_aesm}
%autopatch -m 50 -M 99 -p1
%endif

############################################################
#
# 'make preparation' is required first build step, and would
# pull in many git submodules, apply patches for various
# things, download pre-built enclaves, etc.
#
# What follows simulates 'make preparation' with functionally
# equivalent actions to get the source tree setup in the
# expected manner for performing the build
#
############################################################

# Will use system package instead
rm -rf external/CppMicroServices
%if %{with_host_tinyxml2}
rm -rf external/tinyxml2
%endif

# Don't intend to package these optional bits since none of
# the required enclaves need this, and thus we can cut down
# on bundling some 3rd party code
rm -rf external/{dnnl,openmp,protobuf} sdk/sample_libcrypto

############################################################
# dcap
(
  cd external/dcap_source

  tar zxf %{SOURCE2} --strip 1

  %autopatch -m 100 -M 199 -p1

  (
    mkdir QuoteVerification/sgxssl
    cd QuoteVerification/sgxssl

    tar zxf %{SOURCE4} --strip 1
    %autopatch -m 200 -M 299 -p1

    cp %{SOURCE10} openssl_source/
  )

  (
    cd QuoteVerification/QVL

    tar zxf %{SOURCE7} --strip 1
  )

  (
    cd external/jwt-cpp

    tar zxf %{SOURCE12} --strip 1
    patch -p1 < ../0001-Add-a-macro-to-disable-time-support-in-jwt-for-SGX.patch
  )

  (
    cd external/wasm-micro-runtime

    tar zxf %{SOURCE13} --strip 1
  )
)

############################################################
# sgxssl
(
  cd external/sgxssl
  tar zxf %{SOURCE4} --strip 1
  %autopatch -m 200 -M 299 -p1

  cp %{SOURCE10} openssl_source/
)

############################################################
# ippcrypto
(
  # XXX sanity check that all ipp-crypto is permitted by Fedora
  cd external/ippcp_internal/ipp-crypto
  tar zxf %{SOURCE5} --strip 1
  %autopatch -m 300 -M 399 -p1
)

############################################################
# pccs
(
  cd external/dcap_source/QuoteGeneration/pccs
  tar zxf %{SOURCE8} --strip 1
  %autopatch -m 400 -M 499 -p1
)

############################################################
# sgx-emm
(
  cd external/sgx-emm/emm_src
  tar zxf %{SOURCE6} --strip 1
)
./external/sgx-emm/create_symlink.sh

############################################################
# libcbor
(
  cd external/cbor/libcbor
  tar zxf %{SOURCE11} --strip 1
  cd ..
  cp -a libcbor sgx_libcbor
  cd libcbor
  patch -p1 < ../raw_cbor.patch
  cd .. 
  cd sgx_libcbor
  patch -p1 < ../sgx_cbor.patch
)


############################################################
# tinyxml2
%if ! %{with_host_tinyxml2}
(
  cd external/tinyxml2
  tar zxf %{SOURCE14} --strip 1
)
%endif

############################################################
# prebuilt enclaves

# repack.sh strips pre-built enclaves we don't ship, but
# the build process still looks for them, so pretend
# everything exists
mkdir -p psw/ae/data/prebuilt/
touch psw/ae/data/prebuilt/libsgx_{le,qe,pve,pce}.signed.so

(
  cd external/dcap_source/QuoteGeneration
  tar zxf %{SOURCE3}

  # Again just pretend everything exists to placate build
  touch psw/ae/data/prebuilt/libsgx_{pce,id_enclave,qe3,tdqe,qve}.signed.so

  # the header files need to be up 1 level
  #
  # XXX these headers shouldn't really be needed, since DCAP
  # already unpacks & build openssl as a side effect of
  # sgxssl. Somewhere the headers from that build are discarded
  # and QuoteVerification makefiles are set to look at these
  # pre-built headers instead. This is a bug in DCAP that needs
  # fixing and sending upstream
  mkdir -p ../prebuilt/openssl/inc ../prebuilt/opa_bin
  mv prebuilt/openssl/inc/* ../prebuilt/openssl/inc/

  # Source3 contains a pre-built policy.wasm file which repack.sh
  # purges. There are no instructions for how to create this file
  # but the build system needs it to exist, so we touch it. Despite
  # all this it never gets installed as while it was added to the
  # BOM in dcap, it was missed from the BOMs in linux-sgx.
  # https://github.com/intel/SGXDataCenterAttestationPrimitives/issues/427
  touch ../prebuilt/opa_bin/policy.wasm
)

# Sanity check that upstream hasn't include more prebuilt
# files that we're not expecting and thus failed to purge
# in the repack.sh script.
find -name '*.a' -o -name '*.o' > prebuilt.txt
if test -s prebuilt.txt
then
  echo "ERROR: Found pre-built files in source tree."
  echo "ERROR: The following files must be removed from the source archives:"
  cat prebuilt.txt
  exit 1
fi

%build

# Workaround for cmake >= 4.0 which drops compat with
# cmake_minimum_required(VERSION 3.0.0)
export CMAKE_POLICY_VERSION_MINIMUM=3.5

############################################################
# First, build the SDK

# IPP Crypto needs to be pre-built for the SDK.
# Note, that the 'make clean' doesn't delete the
# output '.a' files we need, only the '.o' files
# So when complete we have 3 builds of IPP Crypto
# in external/ippcp_internal/lib/linux/intel64/
for mitigation in '' LOAD CF
do
  %__make %{?_smp_mflags} \
    -C external/ippcp_internal \
    IPP_USE_GIT=0 \
    clean

  %__make %{?_smp_mflags} \
    -C external/ippcp_internal \
    MITIGATION-CVE-2020-0551=$mitigation \
    IPP_USE_GIT=0
done

# Now we can build the actual SDK
for mitigation in LOAD CF ''
do
  %__make %{?_smp_mflags} \
    -C sdk/ V=1 \
    MITIGATION-CVE-2020-0551=$mitigation \
    clean

  %__make %{?_smp_mflags} \
    -C external/dcap_source/QuoteVerification/dcap_tvl \
    MITIGATION-CVE-2020-0551=$mitigation \
    clean

  # XXX temp override -j1 due to race conditions that have not yet been diagnosed
  %__make %{?_smp_mflags} -j1 \
    -C sdk/ V=1 \
    MITIGATION-CVE-2020-0551=$mitigation \
    USE_HOST_OPENSSL_CRYPTO=1 \
    USE_HOST_TINYXML2=%{with_host_tinyxml2}

  %__make %{?_smp_mflags} \
    -C external/dcap_source/QuoteVerification/dcap_tvl \
    MITIGATION-CVE-2020-0551=$mitigation
done

NATIVE="sign_tool/SignTool"
NATIVE="$NATIVE encrypt_enclave"
NATIVE="$NATIVE libcapable/linux"
NATIVE="$NATIVE debugger_interface/linux"
NATIVE="$NATIVE simulation"

# Most of 'sdk/' is enclave code, but there's some
# important native code we must now re-build with
# proper flags enabled to get distro hardening.
for dir in $NATIVE
do
  %__make %{?_smp_mflags} \
    -C sdk/$dir clean

  # XXX temp override -j1 due to race conditions that have not yet been diagnosed
  CFLAGS="%{build_cflags}" \
  CXXFLAGS="%{build_cxxflags}" \
  LDFLAGS="%{build_ldflags}" \
  %__make %{?_smp_mflags} -j1 \
    -C sdk/$dir V=1 \
    MITIGATION-CVE-2020-0551= \
    USE_HOST_OPENSSL_CRYPTO=1 \
    USE_HOST_TINYXML2=%{with_host_tinyxml2}
done

############################################################
# Second, install the SDK into a temporary tree, since this
# dir tree is needed by the next build phase.

%global vroot build/vroot

./linux/installer/bin/build-installpkg.sh sdk cve-2020-0551
./linux/installer/bin/sgx_linux_x64_sdk_*.bin --prefix=%{vroot}


############################################################
# Third, build the AEs (Architectural Enclaves).

# XXX temp override -j1 due to race condition setting up sgxssl headers with QvE
%global do_build() \
%if %1 \
  %if "%3" == "qve.so" \
    %make_build -C %2 \\\
      SGX_SDK=$(pwd)/%{vroot}/sgxsdk \\\
      %3 -j1 \
  %else \
    %make_build -C %2 \\\
      SGX_SDK=$(pwd)/%{vroot}/sgxsdk \\\
      %3 \
  %endif \
%endif

%do_build %{_with_enclave_pce} psw/ae/pce pce.so
%do_build %{_with_enclave_ide} external/dcap_source/QuoteGeneration/quote_wrapper/quote/id_enclave/linux id_enclave.so
%do_build %{_with_enclave_qe3} external/dcap_source/QuoteGeneration/quote_wrapper/quote/enclave/linux qe3.so
%do_build %{_with_enclave_tdqe} external/dcap_source/QuoteGeneration/quote_wrapper/tdx_quote/enclave/linux tdqe.so
%do_build %{_with_enclave_qve} external/dcap_source/QuoteVerification/QvE qve.so


############################################################
# Fourth, build the Platform Software

# XXX temp override -j1 due to race conditions that have not yet been diagnosed
#
# Perhaps 20% of the time it will fail with error like:
#
# /usr/bin/ld: /builddir/build/BUILD/linux-sgx-2.26-build/linux-sgx-sgx_2.26/common/se_wrapper_psw/libwrapper.a: error adding symbols: file format not recognized
CFLAGS="%{build_cflags}" \
CXXFLAGS="%{build_cxxflags}" \
LDFLAGS="%{build_ldflags}" \
%__make %{?_smp_mflags} -j1 \
  -C psw/ V=1 VERBOSE=1 \
  SGX_SDK=$(pwd)/%{vroot}/sgxsdk \
  SGX_ENCLAVE_PATH=%{sgx_libdir} \
  USE_HOST_OPENSSL_CRYPTO=1 \
  USE_HOST_CPPMICROSERVICES=1

# XXX temp override -j1 due to race conditions that have not yet been diagnosed
CFLAGS="%{build_cflags}" \
CXXFLAGS="%{build_cxxflags}" \
LDFLAGS="%{build_ldflags}" \
%__make %{?_smp_mflags} -j1 \
  -C external/dcap_source/ V=1 VERBOSE=1 \
  SGX_SDK=$(pwd)/%{vroot}/sgxsdk \
  SGX_ENCLAVE_PATH=%{sgx_libdir}

(
    # PCCS NodeJS deps bundle

    cd external/dcap_source/QuoteGeneration/pccs
    tar Jxvf %{SOURCE53}

    cd service

    perl -i -p -e 's,"sqlite%":"internal","sqlite%":"/usr",' node_modules/sqlite3/binding.gyp
    perl -i -p -e 's,\(sqlite\)/lib,(sqlite)/lib64,' node_modules/sqlite3/binding.gyp

    for pkg in node_modules/*
    do
      (
        cd $pkg
        npm run install --if-present --nodedir=/usr
      )
    done

    # Keep brp-mangle-shebangs happy
    find node_modules -type f -exec chmod -x {} \;

    chrpath --delete node_modules/sqlite3/build/Release/node_sqlite3.node
)


# SDK provides dummy stub libraries to deal with a circular
# build dependancy problem where the PSW wants these libs
# before it has built its own real copies. Delete them now,
# since we've done the PSW build and don't want these dummy
# stubs installed
for i in epid launch quote_ex uae_service urts
do
  rm -f %{vroot}/sgxsdk/lib64/libsgx_$i.so
done
rm -f %{vroot}/sgxsdk/lib64/libsgx_urts.so.2


# Pull together all license files relevant to the code that is shipped
# Err on the side of pulling in much too much, rather than miss something
mkdir licenses
for f in $(find -type f | grep -E -i '(license|copying)')
do
  d=$(dirname $f)
  mkdir -p licenses/$d
  cp $f licenses/$f
done

%install

############################################################
# Install phase
#
# There's nothing useful like 'make install' to install
# everything in the right place :-(

# Dirs for host OS software
%__install -d %{buildroot}%{_bindir}
%__install -d %{buildroot}%{_libdir}/pkgconfig
%__install -d %{buildroot}%{_libexecdir}
%__install -d %{buildroot}%{_datadir}
%__install -d %{buildroot}%{_includedir}
%__install -d %{buildroot}%{_unitdir}
%__install -d %{buildroot}%{_sysusersdir}
%__install -d %{buildroot}%{_udevrulesdir}

# Dirs for enclave software
%__install -d %{buildroot}%{sgx_includedir}
%__install -d %{buildroot}%{sgx_libdir}

############################################################
# First the SDK stuff we put into the 'vroot' earlier

mv %{vroot}/sgxsdk/bin/sgx* %{buildroot}%{_bindir}/
mv %{vroot}/sgxsdk/bin/x64/sgx* %{buildroot}%{_bindir}/
mv %{vroot}/sgxsdk/include/* %{buildroot}%{sgx_includedir}/
mv %{vroot}/sgxsdk/lib64/libsgx*.a %{buildroot}%{sgx_libdir}/
mv %{vroot}/sgxsdk/lib64/libtdx*.a %{buildroot}%{sgx_libdir}/
mv %{vroot}/sgxsdk/lib64/libsgx*.so* %{buildroot}%{_libdir}/
mv %{vroot}/sgxsdk/lib64/gdb-sgx-plugin %{buildroot}%{_datadir}/sgx-gdb-plugin
mv %{vroot}/sgxsdk/pkgconfig/libsgx*pc %{buildroot}%{_libdir}/pkgconfig/

rm -rf %{vroot}/sgxsdk/SampleCode

############################################################
# Second the (unsigned) architectural enclaves

# @arg1: boolean condition for whether to ship this enclave
# @arg2: base name of the enclave
# @arg3: directory containing locally built enclave
# @arg4: directory containing pre-bult enclave
# @arg5: symbol name that defines the enclave SO version
%global do_install() \
%if %1 \
%__install -m 0755 %3/%2.so %{buildroot}%{sgx_libdir}/libsgx_%2.so \
%endif

version_file=common/inc/internal/se_version.h
%do_install %{_with_enclave_pce} pce psw/ae/pce psw/ae/data/prebuilt PCE_VERSION

version_file=external/dcap_source/QuoteGeneration/common/inc/internal/se_version.h
%do_install %{_with_enclave_ide} id_enclave external/dcap_source/QuoteGeneration/quote_wrapper/quote/id_enclave/linux external/dcap_source/QuoteGeneration/psw/ae/data/prebuilt IDE_VERSION
%do_install %{_with_enclave_qe3} qe3 external/dcap_source/QuoteGeneration/quote_wrapper/quote/enclave/linux external/dcap_source/QuoteGeneration/psw/ae/data/prebuilt QE3_VERSION
%do_install %{_with_enclave_tdqe} tdqe external/dcap_source/QuoteGeneration/quote_wrapper/tdx_quote/enclave/linux external/dcap_source/QuoteGeneration/psw/ae/data/prebuilt TDQE_VERSION
%do_install %{_with_enclave_qve} qve external/dcap_source/QuoteVerification/QvE external/dcap_source/QuoteGeneration/psw/ae/data/prebuilt QVE_VERSION


############################################################
# Third the Platform Software
#
# Neither of these fully installs all of the software, so we
# have to run both. There's a little overlap in what they
# install but that's harmless as duplicated content should
# match between them. For further info go to the source
# and compare:
#
#   $ cd linux/installer/common
#   $ diff -rup psw-dcap/BOM_install/ psw-tdx/BOM_install/
sed -i '/libCppMicroServices/g' linux/installer/common/psw-dcap/BOM_install/sgx-aesm-service.txt
%__make -I linux/installer/common/psw-dcap -f linux/installer/common/psw-dcap/Makefile SRCDIR=. DESTDIR=%{vroot}/psw install
%__make -I linux/installer/common/psw-tdx -f linux/installer/common/psw-tdx/Makefile SRCDIR=. DESTDIR=%{vroot}/psw install

# The above commands don't actually install into a single
# usable tree, instead they create multiple top level FS
# trees, each of which reflects the non-upstream Debian/RPM
# packages that Intel propose. These RPMs don't reflect the
# Fedora packaging guidelines, so we're ignoring their layout
# and re-arranging things in a more normal manner.
#
# First merge all the top level dirs together into one
# tree under the final build root
mkdir %{vroot}/root
for dir in %{vroot}/psw/*
do
  cp -a $dir/* %{vroot}/root/
done
cp -a %{vroot}/root/ %{buildroot}/root


# Second, re-arrange the content to match the normal tree
# layout Fedora expects. We rm/rmdir any bits we don't
# want, such that RPM will warn about any files left in
# the build root that aren't listed as 'files', so we catch
# new files appearing in future versions

############################################################
# Host AESM service

%if %{with_aesm}
%__install -d %{buildroot}%{_sysconfdir}/aesmd
%__install -d %{buildroot}%{_libdir}/aesmd
%__install -d %{buildroot}%{_datadir}/aesmd
%__install -d %{buildroot}%{_sharedstatedir}/aesmd
%__install -d %{buildroot}%{_rundir}/aesmd
%endif

# Enclaves to be provided by a separate package, so we purge these
rm -f %{buildroot}/root/opt/intel/sgx-aesm-service/aesm/*signed.so*

%if %{with_aesm}
rm -f %{buildroot}/root/opt/intel/sgx-aesm-service/aesm/linksgx.sh
rm -f %{buildroot}/root/opt/intel/sgx-aesm-service/aesm/libsgx_urts.so.2
rm -f %{buildroot}/root/opt/intel/sgx-aesm-service/startup.sh
rm -f %{buildroot}/root/opt/intel/sgx-aesm-service/cleanup.sh


mv %{buildroot}/root/opt/intel/sgx-aesm-service/aesm/le_prod_css.bin %{buildroot}%{_datadir}/aesmd/
mv %{buildroot}/root/var/opt/aesmd/data/white_list_cert_to_be_verify.bin %{buildroot}%{_datadir}/aesmd/
rmdir %{buildroot}/root/var/opt/aesmd/data/
rmdir %{buildroot}/root/var/opt/aesmd

mv %{buildroot}/root/opt/intel/sgx-aesm-service/aesm/* %{buildroot}%{_libdir}/aesmd/
rmdir %{buildroot}/root/opt/intel/sgx-aesm-service/aesm
rmdir %{buildroot}/root/opt/intel/sgx-aesm-service

mv %{buildroot}/root/etc/aesmd.conf %{buildroot}%{_sysconfdir}/

# Workarounds for code that assumes all files are in the same dir
# XXX patch the source to just look in the right place to begin with
ln -s ../../..%{_sysconfdir}/aesmd.conf \
   %{buildroot}%{_libdir}/aesmd/aesmd.conf
ln -s ../../..%{_datadir}/aesmd/le_prod_css.bin \
   %{buildroot}%{_libdir}/aesmd/le_prod_css.bin
ln -s ../../..%{_datadir}/aesmd/white_list_cert_to_be_verify.bin \
   %{buildroot}%{_libdir}/aesmd/white_list_cert_to_be_verify.bin

# XXX it looks for files relative to its binary, so we
# need this wrapper. Patch the source and kill this
cat >> %{buildroot}%{_bindir}/aesmd <<EOF
#!/bin/sh

export LD_LIBRARY_PATH=%{_libdir}/aesmd/
exec %{_libdir}/aesmd/aesm_service "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/aesmd

rm -f %{buildroot}/root/lib/systemd/system/aesmd.service
%__install %{SOURCE40} %{buildroot}%{_sysusersdir}/aesmd.conf
%__install %{SOURCE41} %{buildroot}%{_unitdir}/aesmd.service
%else
rm -f %{buildroot}/root/opt/intel/sgx-aesm-service/aesm/le_prod_css.bin
rmdir %{buildroot}/root/opt/intel/sgx-aesm-service/aesm
rmdir %{buildroot}/root/opt/intel/sgx-aesm-service
%endif


############################################################
# Host PCCS service

# Home dir for 'pccs' user
%__install -d %{buildroot}%{_sharedstatedir}/pccs
%__install -d %{buildroot}%{_localstatedir}/log/pccs
%__install -d %{buildroot}%{_sysconfdir}/pccs
%__install -d %{buildroot}%{_sysconfdir}/pccs/ssl
%__install -d %{buildroot}%{nodejs_sitearch}/pccs

mv external/dcap_source/tools/PCKCertSelection/out/libPCKCertSelection.so \
   %{buildroot}%{_libdir}/libPCKCertSelection.so.1
ln -s libPCKCertSelection.so.1 %{buildroot}%{_libdir}/libPCKCertSelection.so

mv %{buildroot}/root/opt/intel/sgx-dcap-pccs/config/default.json \
  %{buildroot}%{_sysconfdir}/pccs/default.json
rmdir %{buildroot}/root/opt/intel/sgx-dcap-pccs/config
rm -f %{buildroot}/root/lib/systemd/system/pccs.service

mv %{buildroot}/root/opt/intel/sgx-dcap-pccs/* \
   %{buildroot}%{nodejs_sitearch}/pccs
rmdir %{buildroot}/root/opt/intel/sgx-dcap-pccs

(
    # Node JS deps bundle
    cd external/dcap_source/QuoteGeneration/pccs/service
    rm -f install.sh README.md

    # So find-debuginfo processes it
    chmod +x node_modules/sqlite3/build/Release/node_sqlite3.node

    cp -a node_modules %{buildroot}%{nodejs_sitearch}/pccs/node_modules
)

cat >>%{buildroot}%{_bindir}/pccs <<EOF
#!/usr/bin/sh

exec node %{nodejs_sitearch}/pccs/pccs_server.js
EOF
chmod +x %{buildroot}%{_bindir}/pccs

%__install -m 0644 %{SOURCE50} %{buildroot}%{_sysusersdir}/pccs.conf
%__install -m 0644 %{SOURCE51} %{buildroot}%{_unitdir}/pccs.service


############################################################
# Host PCCS admin tool

%__install -d %{buildroot}%{_datadir}/pccsadmin
cp external/dcap_source/QuoteGeneration/pccs/PccsAdminTool/pccsadmin.py %{buildroot}%{_datadir}/pccsadmin/pccsadmin.py
cp -a external/dcap_source/QuoteGeneration/pccs/PccsAdminTool/lib %{buildroot}%{_datadir}/pccsadmin/lib

cat > %{buildroot}%{_bindir}/pccsadmin <<EOF
#!/bin/sh

exec python3 %{_datadir}/pccsadmin/pccsadmin.py "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/pccsadmin


############################################################
# Host PCS client tool

%__install -d %{buildroot}%{_datadir}/pcsclient
cp external/dcap_source/tools/PcsClientTool/pcsclient.py %{buildroot}%{_datadir}/pcsclient/pcsclient.py
cp -a external/dcap_source/tools/PcsClientTool/lib %{buildroot}%{_datadir}/pcsclient/lib

cat > %{buildroot}%{_bindir}/pcsclient <<EOF
#!/bin/sh

exec python3 %{_datadir}/pcsclient/pcsclient.py "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/pcsclient


############################################################
# Host PCK ID tool

%__install -d %{buildroot}%{_sysconfdir}/PCKIDRetrievalTool/
# XXX must patch source to look in sysconfdir
mv %{buildroot}/root/opt/intel/sgx-pck-id-retrieval-tool/PCKIDRetrievalTool \
   %{buildroot}%{_bindir}/
mv %{buildroot}/root/opt/intel/sgx-pck-id-retrieval-tool/network_setting.conf \
   %{buildroot}%{_sysconfdir}/PCKIDRetrievalTool/network_setting.conf
rm -f %{buildroot}/root/opt/intel/sgx-pck-id-retrieval-tool/License.txt
rm -f %{buildroot}/root/opt/intel/sgx-pck-id-retrieval-tool/README.txt
# Enclaves to be provided by a separate package, so we purge these
rm -f %{buildroot}/root/opt/intel/sgx-pck-id-retrieval-tool/libsgx_pce.signed.so.1
rm -f %{buildroot}/root/opt/intel/sgx-pck-id-retrieval-tool/libsgx_id_enclave.signed.so.1
rmdir %{buildroot}/root/opt/intel/sgx-pck-id-retrieval-tool


############################################################
# Registration agent

mv %{buildroot}/root/opt/intel/sgx-ra-service/mpa_manage \
   %{buildroot}%{_bindir}/mpa_manage
mv %{buildroot}/root/opt/intel/sgx-ra-service/mpa_registration \
   %{buildroot}%{_bindir}/mpa_registration
mv %{buildroot}/root/etc/mpa_registration.conf \
   %{buildroot}%{_sysconfdir}/mpa_registration.conf
rm -f %{buildroot}/root/opt/intel/sgx-ra-service/mpa_registration_tool.conf
rm -f %{buildroot}/root/opt/intel/sgx-ra-service/mpa_registration_tool.service
rm %{buildroot}/root/opt/intel/sgx-ra-service/startup.sh
rm %{buildroot}/root/opt/intel/sgx-ra-service/cleanup.sh
rmdir %{buildroot}/root/opt/intel/sgx-ra-service

%__install -m 0644 %{SOURCE48} %{buildroot}%{_unitdir}/mpa_registration.service

mv %{buildroot}/root/usr/include/{mp*,MP*,MultiPackageDefs}.h \
   %{buildroot}%{_includedir}/
mv %{buildroot}/root/usr/lib64/libmpa*.so* \
   %{buildroot}%{_libdir}/


############################################################
# Host TDX quote generation service

%__install -d %{buildroot}%{_sharedstatedir}/qgs
# XXX patch source to just 'qgs' instead of 'tdx-qgs' ?
%__install -d %{buildroot}%{_rundir}/tdx-qgs
%__install -d %{buildroot}%{_sysconfdir}/sysconfig

mv %{buildroot}/root/etc/qgs.conf \
   %{buildroot}%{_sysconfdir}/qgs.conf
mv %{buildroot}/root/opt/intel/tdx-qgs/qgs \
   %{buildroot}%{_bindir}/qgs

# Switch from vsock to unix socket to avoid exposing it
# to all VMs unconditionally
sed -i -e 's/^port/#port/' %{buildroot}%{_sysconfdir}/qgs.conf

rm -f %{buildroot}/root/opt/intel/tdx-qgs/linksgx.sh
rm -f %{buildroot}/root/opt/intel/tdx-qgs/cleanup.sh
rm -f %{buildroot}/root/opt/intel/tdx-qgs/startup.sh
rmdir %{buildroot}/root/opt/intel/tdx-qgs


%__install -m 0644 %{SOURCE44} %{buildroot}%{_sysusersdir}/qgs.conf
%__install -m 0644 %{SOURCE45} %{buildroot}%{_unitdir}/qgs.service
%__install -m 0644 %{SOURCE46} %{buildroot}%{_sysconfdir}/sysconfig/qgs


############################################################
# Common libraries

# Enclaves to be provided by a separate package, so we purge these
rm -f %{buildroot}/root/usr/lib64/lib*signed.so*

# Normal host libraries
mv %{buildroot}/root/usr/lib64/lib* %{buildroot}/%{_libdir}/

# Some overlap with what's in %{sgx_includedir}, but that dir is
# intended exclusively for building enclave code, while
# %{_includedir} is for stuff that's exclusively host code
mv %{buildroot}/root/usr/include/*.h %{buildroot}/%{_includedir}/
# Wierdly missing, but required by other headers that are present
for i in 3 4 5
do
  cp %{buildroot}%{sgx_includedir}/sgx_quote_$i.h  %{buildroot}/%{_includedir}/
done

mv %{buildroot}/root/etc/sgx_default_qcnl.conf \
   %{buildroot}%{_sysconfdir}/

# Default to the public API service. If users do deploy pccs
# it probably makes more sense to do so on the LAN, so don't
# assume localhost deployment. This also allows out of the box
# usage without having to create a local x509 CA for PCCS.
perl -i -p -e 's,https://localhost:10801/sgx/certification/v4/,https://api.trustedservices.intel.com/sgx/certification/v4/,' \
   %{buildroot}%{_sysconfdir}/sgx_default_qcnl.conf

%__install %{SOURCE42} %{buildroot}%{_sysusersdir}/sgxprv.conf
%__install %{SOURCE43} %{buildroot}%{_udevrulesdir}/92-sgx-provision.rules


############################################################
# Misc cleanup

# Irrelevant for Fedora context
rm -f %{buildroot}/root/usr/lib/systemd/system/remount-dev-exec.service

# We apply our own unit files for services
rm -f %{buildroot}/root/lib/systemd/system/mpa_registration_tool.service
rm -f %{buildroot}/root/lib/systemd/system/qgsd.service
rm -rf %{buildroot}/root/sample
rm -f %{buildroot}/root/etc/udev/rules.d/93-sgx-provision.rules
rm -f %{buildroot}/root/etc/udev/rules.d/91-sgx-enclave.rules
rm -f %{buildroot}/root/License.txt

# Intentionally not recursive delete, as we want build to fail
# to alert us if a future release adds more files that need handling
rmdir %{buildroot}/root/etc/udev/rules.d/
rmdir %{buildroot}/root/etc/udev
rmdir %{buildroot}/root/etc/
rmdir %{buildroot}/root/lib/systemd/system
rmdir %{buildroot}/root/lib/systemd
rmdir %{buildroot}/root/lib
rmdir %{buildroot}/root/usr/lib/systemd/system
rmdir %{buildroot}/root/usr/lib/systemd
rmdir %{buildroot}/root/usr/lib/
rmdir %{buildroot}/root/usr/lib64
rmdir %{buildroot}/root/usr/include
rmdir %{buildroot}/root/usr/
%if %{with_aesm}
rmdir %{buildroot}/root/var/opt
rmdir %{buildroot}/root/var
%endif
rmdir %{buildroot}/root/opt/intel
rmdir %{buildroot}/root/opt
rmdir %{buildroot}/root


############################################################
# Fix ups - for some reason the PSW BOM files miss a few bits

cp ./external/dcap_source/tools/PCKCertSelection/include/pck_cert_selection.h %{buildroot}%{_includedir}
cp ./external/dcap_source/QuoteGeneration/qpl/inc/sgx_default_quote_provider.h %{buildroot}%{_includedir}
cp ./external/dcap_source/QuoteGeneration/quote_wrapper/quote/inc/sgx_ql_core_wrapper.h %{buildroot}%{_includedir}

mv %{buildroot}%{_libdir}/libsgx_qe3_logic.so \
   %{buildroot}%{_libdir}/libsgx_qe3_logic.so.1.0.0
ln -s libsgx_qe3_logic.so.1.0.0 %{buildroot}%{_libdir}/libsgx_qe3_logic.so.1
ln -s libsgx_qe3_logic.so.1 %{buildroot}%{_libdir}/libsgx_qe3_logic.so

%if %{with_sysusers_scripts}
%pre -n sgx-libs
%sysusers_create_compat %{SOURCE42}
%endif

%post -n sgx-libs
if [ -S /run/udev/control ]; then
    udevadm control --reload
    udevadm trigger --property-match=DEVNAME=/dev/sgx_provision
fi

%if %{with_aesm}
%if %{with_sysusers_scripts}
%pre -n sgx-aesm
%sysusers_create_compat %{SOURCE40}
%endif

%post -n sgx-aesm
%systemd_post aesmd.service

%preun -n sgx-aesm
%systemd_preun aesmd.service

%postun -n sgx-aesm
%systemd_postun_with_restart aesmd.service
%endif


%post -n sgx-mpa
%systemd_post mpa_registration.service

%preun -n sgx-mpa
%systemd_preun mpa_registration.service

%postun -n sgx-mpa
%systemd_postun_with_restart mpa_registration.service


%if %{with_sysusers_scripts}
%pre -n sgx-pccs
%sysusers_create_compat %{SOURCE50}
%endif

%post -n sgx-pccs
%systemd_post pccs.service

%preun -n sgx-pccs
%systemd_preun pccs.service

%postun -n sgx-pccs
%systemd_postun_with_restart pccs.service


%if %{with_sysusers_scripts}
%pre -n tdx-qgs
%sysusers_create_compat %{SOURCE44}
%endif

%post -n tdx-qgs
%systemd_post qgs.service

%preun -n tdx-qgs
%systemd_preun qgs.service

%postun -n tdx-qgs
%systemd_postun_with_restart qgs.service


%global do_files() \
%if %3 \
%files -n sgx-enclave-latest-%1-unsigned \
%dir %{sgx_prefix} \
%dir %{sgx_libdir} \
%{sgx_libdir}/libsgx_%2.so \
%endif

%do_files pce pce %{_with_enclave_pce}
%do_files ide id_enclave %{_with_enclave_ide}
%do_files qe3 qe3 %{_with_enclave_qe3}
%do_files tdqe tdqe %{_with_enclave_tdqe}
%do_files qve qve %{_with_enclave_qve}

%files -n sgx-common
%license licenses/

%files -n sgx-enclave-devel

%{_bindir}/sgx_edger8r
%{_bindir}/sgx_sign
%{_bindir}/sgx_encrypt
%{_bindir}/sgx-gdb
%{_bindir}/sgx_config_cpusvn

%dir %{_datadir}/sgx-gdb-plugin/
%{_datadir}/sgx-gdb-plugin/gdb_sgx_cmd
%{_datadir}/sgx-gdb-plugin/gdb_sgx_plugin.py
%{_datadir}/sgx-gdb-plugin/load_symbol_cmd.py
%{_datadir}/sgx-gdb-plugin/printers.py
%{_datadir}/sgx-gdb-plugin/readelf.py
%{_datadir}/sgx-gdb-plugin/sgx_emmt.py

%dir %{sgx_prefix}

%dir %{sgx_includedir}/
%{sgx_includedir}/libcxx/
%{sgx_includedir}/stdc++/
%{sgx_includedir}/tlibc/

%{sgx_includedir}/sgx.h
%{sgx_includedir}/sgx_attributes.h
%{sgx_includedir}/sgx_capable.h
%{sgx_includedir}/sgx_cpuid.h
%{sgx_includedir}/sgx_dcap_qae_tvl.h
%{sgx_includedir}/sgx_dcap_qal.h
%{sgx_includedir}/sgx_dcap_tvl.h
%{sgx_includedir}/sgx_defs.h
%{sgx_includedir}/sgx_dh.h
%{sgx_includedir}/sgx_ecp_types.h
%{sgx_includedir}/sgx_edger8r.h
%{sgx_includedir}/sgx_eid.h
%{sgx_includedir}/sgx_enclave_common.h
%{sgx_includedir}/sgx_error.h
%{sgx_includedir}/sgx_intrin.h
%{sgx_includedir}/sgx_key.h
%{sgx_includedir}/sgx_key_exchange.h
%{sgx_includedir}/sgx_lfence.h
%{sgx_includedir}/sgx_mm.h
%{sgx_includedir}/sgx_pce.h
%{sgx_includedir}/sgx_pcl_guid.h
%{sgx_includedir}/sgx_ql_lib_common.h
%{sgx_includedir}/sgx_ql_quote.h
%{sgx_includedir}/sgx_quote.h
%{sgx_includedir}/sgx_quote_3.h
%{sgx_includedir}/sgx_quote_4.h
%{sgx_includedir}/sgx_quote_5.h
%{sgx_includedir}/sgx_qve_header.h
%{sgx_includedir}/sgx_report.h
%{sgx_includedir}/sgx_report2.h
%{sgx_includedir}/sgx_rsrv_mem_mngr.h
%{sgx_includedir}/sgx_secure_align.h
%{sgx_includedir}/sgx_secure_align_api.h
%{sgx_includedir}/sgx_spinlock.h
%{sgx_includedir}/sgx_tcrypto.h
%{sgx_includedir}/sgx_thread.h
%{sgx_includedir}/sgx_tkey_exchange.h
%{sgx_includedir}/sgx_tprotected_fs.h
%{sgx_includedir}/sgx_trts.h
%{sgx_includedir}/sgx_trts_aex.h
%{sgx_includedir}/sgx_trts_exception.h
%{sgx_includedir}/sgx_tseal.h
%{sgx_includedir}/sgx_ttls.h
%{sgx_includedir}/sgx_uae_epid.h
%{sgx_includedir}/sgx_uae_launch.h
%{sgx_includedir}/sgx_uae_quote_ex.h
%{sgx_includedir}/sgx_uae_service.h
%{sgx_includedir}/sgx_ukey_exchange.h
%{sgx_includedir}/sgx_urts.h
%{sgx_includedir}/sgx_uswitchless.h
%{sgx_includedir}/sgx_utils.h
%{sgx_includedir}/sgx_utls.h

%{sgx_includedir}/sgx_dcap_tvl.edl
%{sgx_includedir}/sgx_pthread.edl
%{sgx_includedir}/sgx_tkey_exchange.edl
%{sgx_includedir}/sgx_tprotected_fs.edl
%{sgx_includedir}/sgx_tstdc.edl
%{sgx_includedir}/sgx_tswitchless.edl
%{sgx_includedir}/sgx_ttls.edl

%{sgx_includedir}/ipp/


%dir %{sgx_libdir}/

%{sgx_libdir}/libsgx_capable.a
%{sgx_libdir}/libsgx_dcap_tvl.a
%{sgx_libdir}/libsgx_ossl_fips.a
%{sgx_libdir}/libsgx_pcl.a
%{sgx_libdir}/libsgx_pclsim.a
%{sgx_libdir}/libsgx_pthread.a
%{sgx_libdir}/libsgx_tcmalloc.a
%{sgx_libdir}/libsgx_tcrypto.a
%{sgx_libdir}/libsgx_tcxx.a
%{sgx_libdir}/libsgx_tkey_exchange.a
%{sgx_libdir}/libsgx_tprotected_fs.a
%{sgx_libdir}/libsgx_trts.a
%{sgx_libdir}/libsgx_trts_sim.a
%{sgx_libdir}/libsgx_tservice.a
%{sgx_libdir}/libsgx_tservice_sim.a
%{sgx_libdir}/libsgx_tstdc.a
%{sgx_libdir}/libsgx_tswitchless.a
%{sgx_libdir}/libsgx_ttls.a
%{sgx_libdir}/libsgx_ukey_exchange.a
%{sgx_libdir}/libsgx_uprotected_fs.a
%{sgx_libdir}/libsgx_uswitchless.a
%{sgx_libdir}/libsgx_utls.a
%{sgx_libdir}/libtdx_tls.a

%{_libdir}/libsgx_capable.so
%{_libdir}/libsgx_epid_sim.so
%{_libdir}/libsgx_launch_sim.so
%{_libdir}/libsgx_ptrace.so
%{_libdir}/libsgx_quote_ex_sim.so
%{_libdir}/libsgx_uae_service_sim.so
%{_libdir}/libsgx_urts_sim.so

%{_libdir}/pkgconfig/libsgx_epid_sim.pc
%{_libdir}/pkgconfig/libsgx_launch_sim.pc
%{_libdir}/pkgconfig/libsgx_quote_ex_sim.pc
%{_libdir}/pkgconfig/libsgx_uae_service_sim.pc
%{_libdir}/pkgconfig/libsgx_urts_sim.pc


%files -n sgx-devel
%{_includedir}/MPNetwork.h
%{_includedir}/MPNetworkDefs.h
%{_includedir}/MPUefi.h
%{_includedir}/MultiPackageDefs.h
%{_includedir}/mp_network.h
%{_includedir}/mp_uefi.h
%{_includedir}/pck_cert_selection.h
%{_includedir}/sgx_attributes.h
%{_includedir}/sgx_dcap_ql_wrapper.h
%{_includedir}/sgx_dcap_quoteverify.h
%{_includedir}/sgx_default_quote_provider.h
%{_includedir}/sgx_defs.h
%{_includedir}/sgx_eid.h
%{_includedir}/sgx_enclave_common.h
%{_includedir}/sgx_error.h
%{_includedir}/sgx_key.h
%{_includedir}/sgx_pce.h
%{_includedir}/sgx_ql_core_wrapper.h
%{_includedir}/sgx_ql_lib_common.h
%{_includedir}/sgx_ql_quote.h
%{_includedir}/sgx_quote.h
%{_includedir}/sgx_quote_3.h
%{_includedir}/sgx_quote_4.h
%{_includedir}/sgx_quote_5.h
%{_includedir}/sgx_qve_header.h
%{_includedir}/sgx_report.h
%{_includedir}/sgx_uae_epid.h
%{_includedir}/sgx_uae_launch.h
%{_includedir}/sgx_uae_quote_ex.h
%{_includedir}/sgx_urts.h
%{_includedir}/td_ql_wrapper.h
%{_libdir}/libmpa_network.so
%{_libdir}/libmpa_uefi.so
%{_libdir}/libdcap_quoteprov.so
%{_libdir}/libsgx_dcap_ql.so
%{_libdir}/libsgx_dcap_quoteverify.so
%{_libdir}/libsgx_default_qcnl_wrapper.so
%{_libdir}/libsgx_enclave_common.so
%{_libdir}/libsgx_epid.so
%{_libdir}/libsgx_launch.so
%{_libdir}/libsgx_pce_logic.so
%{_libdir}/libsgx_qe3_logic.so
%{_libdir}/libsgx_quote_ex.so
%{_libdir}/libsgx_tdx_logic.so
%{_libdir}/libsgx_uae_service.so
%{_libdir}/libsgx_urts.so
%{_libdir}/libPCKCertSelection.so
%{_libdir}/pkgconfig/libsgx_epid.pc
%{_libdir}/pkgconfig/libsgx_launch.pc
%{_libdir}/pkgconfig/libsgx_quote_ex.pc
%{_libdir}/pkgconfig/libsgx_uae_service.pc
%{_libdir}/pkgconfig/libsgx_urts.pc


%files -n sgx-libs
%config(noreplace) %{_sysconfdir}/sgx_default_qcnl.conf
%{_sysusersdir}/sgxprv.conf
%dir %{_udevrulesdir}
%{_udevrulesdir}/92-sgx-provision.rules
%{_libdir}/libdcap_quoteprov.so.1*
%{_libdir}/libmpa_network.so.1*
%{_libdir}/libmpa_uefi.so.1*
%{_libdir}/libsgx_default_qcnl_wrapper.so.1*
%{_libdir}/libsgx_dcap_ql.so.1*
%{_libdir}/libsgx_dcap_quoteverify.so.1*
%{_libdir}/libsgx_enclave_common.so.1*
%{_libdir}/libsgx_epid.so.1*
%{_libdir}/libsgx_launch.so.1*
%{_libdir}/libsgx_pce_logic.so.1*
%{_libdir}/libsgx_qe3_logic.so.1*
%{_libdir}/libsgx_quote_ex.so.1*
%{_libdir}/libsgx_tdx_logic.so.1*
%{_libdir}/libsgx_uae_service.so.2*
%{_libdir}/libsgx_urts.so.2*
%{_libdir}/libPCKCertSelection.so.1*


%if %{with_aesm}
%files -n sgx-aesm
%{_bindir}/aesmd
%{_unitdir}/aesmd.service
%config(noreplace) %{_sysconfdir}/aesmd.conf
%dir %{_libdir}/aesmd
%dir %{_libdir}/aesmd/bundles
%{_libdir}/aesmd/aesm_service
%{_libdir}/aesmd/bundles/libecdsa_quote_service_bundle.so
%{_libdir}/aesmd/bundles/libepid_quote_service_bundle.so
%{_libdir}/aesmd/bundles/lible_launch_service_bundle.so
%{_libdir}/aesmd/bundles/liblinux_network_service_bundle.so
%{_libdir}/aesmd/bundles/libpce_service_bundle.so
%{_libdir}/aesmd/bundles/libquote_ex_service_bundle.so
%{_libdir}/aesmd/aesmd.conf
%{_libdir}/aesmd/le_prod_css.bin
%{_libdir}/aesmd/liboal.so
%{_libdir}/aesmd/libipc.so
%{_libdir}/aesmd/libutils.so
%{_libdir}/aesmd/liburts_internal.so
%{_libdir}/aesmd/white_list_cert_to_be_verify.bin
%dir %{_datadir}/aesmd/
%{_datadir}/aesmd/white_list_cert_to_be_verify.bin
%{_datadir}/aesmd/le_prod_css.bin
%attr(0700,aesmd,aesmd) %{_sharedstatedir}/aesmd
%{_sysusersdir}/aesmd.conf
%attr(0700,aesmd,aesmd) %{_rundir}/aesmd
%endif


%files -n sgx-pccs
%{_bindir}/pccs
%dir %{_sysconfdir}/pccs
%attr(0750,root,pccs) %dir %{_sysconfdir}/pccs/ssl
%config(noreplace) %{_sysconfdir}/pccs/default.json
%{_unitdir}/pccs.service
%{nodejs_sitearch}/pccs
%{_sysusersdir}/pccs.conf
%attr(0700,pccs,pccs) %dir %{_sharedstatedir}/pccs
%attr(0700,pccs,pccs) %dir %{_localstatedir}/log/pccs


%files -n sgx-pccs-admin
%{_bindir}/pccsadmin
%{_datadir}/pccsadmin


%files -n sgx-pcs-client
%{_bindir}/pcsclient
%{_datadir}/pcsclient


%files -n sgx-pckid-tool
%doc external/dcap_source/tools/PCKRetrievalTool/README_standalone.txt
%dir %{_sysconfdir}/PCKIDRetrievalTool
%config(noreplace) %{_sysconfdir}/PCKIDRetrievalTool/network_setting.conf
%{_bindir}/PCKIDRetrievalTool


%files -n sgx-mpa
%{_bindir}/mpa_manage
%{_bindir}/mpa_registration
%{_unitdir}/mpa_registration.service
%config(noreplace) %{_sysconfdir}/mpa_registration.conf


%files -n tdx-qgs
%config(noreplace) %{_sysconfdir}/sysconfig/qgs
%{_bindir}/qgs
%{_unitdir}/qgs.service
%config(noreplace) %{_sysconfdir}/qgs.conf
%{_sysusersdir}/qgs.conf
%attr(0700,qgs,qgs) %dir %{_sharedstatedir}/qgs
%ghost %attr(0755,qgs,qgs) %dir %{_rundir}/tdx-qgs


%files -n tdx-attest-libs
%{_libdir}/libtdx_attest.so.1*


%files -n tdx-attest-devel
%{_includedir}/tdx_attest.h
%{_libdir}/libtdx_attest.so


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 2.27-10
- Latest state for linux-sgx

* Fri Feb 13 2026 Daniel P. Berrangé <berrange@redhat.com> - 2.27-9
- Fix socket mode handling

* Tue Feb 10 2026 Daniel P. Berrangé <berrange@redhat.com> - 2.27-8
- Relax sgx-pccs dep

* Tue Feb 10 2026 Daniel P. Berrangé <berrange@redhat.com> - 2.27-7
- Fix syntax of bundled provides

* Thu Feb 05 2026 Yaakov Selkowitz <yselkowi@redhat.com> - 2.27-6
- Drop duplicate nodejs dependencies

* Wed Feb 04 2026 Daniel P. Berrangé <berrange@redhat.com> - 2.27-3
- Fix name of input file in pcsclient 'cache' command

* Wed Feb 04 2026 Daniel P. Berrangé <berrange@redhat.com> - 2.27-2
- Switch to versioned node modules archive

* Wed Feb 04 2026 Daniel P. Berrangé <berrange@redhat.com> - 2.27-1
- Update to SGX 2.27 / DCCAP 1.24

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jan 15 2026 Daniel P. Berrangé <berrange@redhat.com> - 2.26-30
- fix build for boost 1.90 update api breakage

* Wed Jan 07 2026 Daniel P. Berrangé <berrange@redhat.com> - 2.26-28
- Fixes for GCC 16 build failures

* Tue Jan 06 2026 Miro Hrončok <miro@hroncok.cz> - 2.26-26
- sgx-pccs-admin: Migrate from deprecated pkg_resources to packaging

* Tue Jan 06 2026 Daniel P. Berrangé <berrange@redhat.com> - 2.26-25
- Drop dep from pccs to mpa_registration

* Wed Dec 10 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-24
- Improve pycryptography port & drop pccs port number change

* Mon Dec 08 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-23
- Add sgx-common dep from pccs

* Mon Dec 08 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-22
- Make npm dep conditional for RHEL-9

* Thu Dec 04 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-21
- Fix traceback when clearing keyring if none exists

* Thu Dec 04 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-20
- Drop sgx-mpa dep from sgx-pccs

* Thu Dec 04 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-19
- Port to pycryptography and pyasn1 and make keyring optional

* Thu Dec 04 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-18
- Add systemd & sysusers scriptlets for PCCS

* Thu Dec 04 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-17
- Enable pccsadmin everywhere

* Tue Dec 02 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.26-16
- Use chrpath to remove RPATH

* Tue Nov 18 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-15
- Set execute on node_sqlite3.node for debuginfo

* Tue Nov 18 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-14
- Add patchelf as a build dep

* Tue Nov 18 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-13
- Purge nodejs sqlite3 rpath instead of disabling rpath checks

* Tue Nov 18 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-12
- Drop obsolete perl mangling cmd that is failing

* Tue Nov 18 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-11
- Re-add tinyxml2 bundling to be used in RHEL rebuilds

* Tue Nov 18 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-10
- Wildcard ignore more tarballs

* Tue Nov 18 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-9
- Stop using _sbindir for services

* Tue Nov 18 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-8
- Add newline in pccs.service

* Wed Nov 12 2025 Vít Ondruch <vondruch@redhat.com> - 2.26-7
- Rebuild for nodejs-packaging

* Wed Nov 12 2025 Vít Ondruch <vondruch@redhat.com> - 2.26-6
- Rebuild for nodejs-packaging

* Thu Oct 09 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-5
- Trigger udev to set /dev/sgx_provision access

* Sat Aug 23 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.26-4
- Rebuilt for tinyxml2 11.0.0

* Fri Aug 01 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.26-3
- Use rust-toolset on RHEL

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.26-1
- Rebase to DCAP 1.23 / SGX 2.26, re-adding PCCS

* Thu Jun 05 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.25-12
- Fix chmod patch and drop unlink patch

* Wed Jun 04 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.25-11
- ghost the qgs rundir and remove post stop socket deletion

* Thu May 22 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.25-10
- Switch to use systemd runtimedir & delete sockets on startup/shutdown

* Tue May 13 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.25-9
- Always set QGS_ARGS

* Tue May 13 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.25-8
- Add ability to control the socket mode

* Wed Apr 16 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.25-7
- Honour CFLAGS/LDFLAGS during build

* Wed Mar 19 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.25-6
- Change way we override SMP flags for qve.so

* Mon Mar 10 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.25-5
- Use vendored tinyxml2 for RHEL builds

* Mon Mar 10 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.25-4
- Workaround for cmake4 incompatibility

* Fri Mar 07 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.25-3
- Disable pccsadmin on RHEL to avoid python deps from EPEL

* Tue Feb 18 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.25-2
- Update .service units to use /usr/bin instead of /usr/sbin

* Fri Feb 14 2025 Daniel P. Berrangé <berrange@redhat.com> - 2.25-1
- Initial import
## END: Generated by rpmautospec
