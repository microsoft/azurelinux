# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2015 - 2018 Intel Corporation
# Copyright (c) 2018 Fraunhofer SIT sponsored by Infineon Technologies AG
# All rights reserved.

-include $(top_srcdir)/git.mk

### Initialize global variables used throughout the file ###
INCLUDE_DIRS    = -I$(srcdir)/src -I$(srcdir)/include/tss2
ACLOCAL_AMFLAGS = -I m4 --install
AM_CFLAGS       = $(INCLUDE_DIRS) $(EXTRA_CFLAGS) $(CODE_COVERAGE_CFLAGS) \
				  $(SANITIZER_CFLAGS)
AM_LDFLAGS      = $(EXTRA_LDFLAGS) $(CODE_COVERAGE_LIBS) $(SANITIZER_LDFLAGS)

# Initialize empty variables to be extended throughout
lib_LTLIBRARIES =
noinst_LTLIBRARIES =
EXTRA_DIST =
DISTCLEANFILES =
CLEANFILES =
MOSTLYCLEANFILES =
noinst_PROGRAMS =
MAINTAINERCLEANFILES = \
    $(DIST_ARCHIVES) \
    AUTHORS

TSS_GITIGNOREFILES = \
    $(GITIGNORE_MAINTAINERCLEANFILES_TOPLEVEL) \
    $(GITIGNORE_MAINTAINERCLEANFILES_MAKEFILE_IN) \
    $(GITIGNORE_MAINTAINERCLEANFILES_M4_LIBTOOL) \
    src_vars.mk \
    Makefile-fuzz-generated.am \
    aminclude_static.am \
    m4/ax_ac_append_to_file.m4 \
    m4/ax_ac_print_to_file.m4 \
    m4/ax_add_am_macro_static.m4 \
    m4/ax_add_fortify_source.m4 \
    m4/ax_am_macros_static.m4 \
    m4/ax_check_compile_flag.m4 \
    m4/ax_check_enable_debug.m4 \
    m4/ax_check_gnu_make.m4 \
    m4/ax_check_link_flag.m4 \
    m4/ax_check_preproc_flag.m4 \
    m4/ax_code_coverage.m4 \
    m4/ax_file_escapes.m4 \
    m4/ax_is_release.m4 \
    m4/ax_normalize_path.m4 \
    m4/ax_prog_doxygen.m4 \
    m4/ax_valgrind_check.m4 \
    m4/pkg.m4

GITIGNOREFILES = ""
### Add ax_* rules ###
# ax_code_coverage
if AUTOCONF_CODE_COVERAGE_2019_01_06
include $(top_srcdir)/aminclude_static.am
clean-local: code-coverage-clean
distclean-local: code-coverage-dist-clean
else
@CODE_COVERAGE_RULES@
endif
GITIGNOREFILES += $(TSS_GITIGNOREFILES)
CODE_COVERAGE_DIRECTORY = $(top_builddir)/src $(top_builddir)/test

# ax_valgrind_check
@VALGRIND_CHECK_RULES@

# ax_doxygen
@DX_RULES@
MOSTLYCLEANFILES += $(DX_CLEANFILES)

if DOXYMAN
DOXYMAN3 = \
    doxygen-doc/man/ESYS_CONTEXT.3 \
    doxygen-doc/man/ESYS_TR.3 \
    doxygen-doc/man/ESYS_TR_defines.3 \
    doxygen-doc/man/Esys_ActivateCredential.3 \
    doxygen-doc/man/Esys_Certify.3 \
    doxygen-doc/man/Esys_CertifyCreation.3 \
    doxygen-doc/man/Esys_ChangeEPS.3 \
    doxygen-doc/man/Esys_ChangePPS.3 \
    doxygen-doc/man/Esys_Clear.3 \
    doxygen-doc/man/Esys_ClearControl.3 \
    doxygen-doc/man/Esys_ClockRateAdjust.3 \
    doxygen-doc/man/Esys_ClockSet.3 \
    doxygen-doc/man/Esys_Commit.3 \
    doxygen-doc/man/Esys_ContextLoad.3 \
    doxygen-doc/man/Esys_ContextSave.3 \
    doxygen-doc/man/Esys_Create.3 \
    doxygen-doc/man/Esys_CreatePrimary.3 \
    doxygen-doc/man/Esys_DictionaryAttackLockReset.3 \
    doxygen-doc/man/Esys_DictionaryAttackParameters.3 \
    doxygen-doc/man/Esys_Duplicate.3 \
    doxygen-doc/man/Esys_ECC_Parameters.3 \
    doxygen-doc/man/Esys_ECDH_KeyGen.3 \
    doxygen-doc/man/Esys_ECDH_ZGen.3 \
    doxygen-doc/man/Esys_EC_Ephemeral.3 \
    doxygen-doc/man/Esys_EncryptDecrypt.3 \
    doxygen-doc/man/Esys_EventSequenceComplete.3 \
    doxygen-doc/man/Esys_EvictControl.3 \
    doxygen-doc/man/Esys_FlushContext.3 \
    doxygen-doc/man/Esys_GetCapability.3 \
    doxygen-doc/man/Esys_GetCommandAuditDigest.3 \
    doxygen-doc/man/Esys_GetRandom.3 \
    doxygen-doc/man/Esys_GetSessionAuditDigest.3 \
    doxygen-doc/man/Esys_GetTestResult.3 \
    doxygen-doc/man/Esys_GetTime.3 \
    doxygen-doc/man/Esys_Hash.3 \
    doxygen-doc/man/Esys_HashSequenceStart.3 \
    doxygen-doc/man/Esys_HierarchyChangeAuth.3 \
    doxygen-doc/man/Esys_HierarchyControl.3 \
    doxygen-doc/man/Esys_HMAC.3 \
    doxygen-doc/man/Esys_HMAC_Start.3 \
    doxygen-doc/man/Esys_Import.3 \
    doxygen-doc/man/Esys_IncrementalSelfTest.3 \
    doxygen-doc/man/Esys_Load.3 \
    doxygen-doc/man/Esys_LoadExternal.3 \
    doxygen-doc/man/Esys_MakeCredential.3 \
    doxygen-doc/man/Esys_NV_Certify.3 \
    doxygen-doc/man/Esys_NV_ChangeAuth.3 \
    doxygen-doc/man/Esys_NV_DefineSpace.3 \
    doxygen-doc/man/Esys_NV_Extend.3 \
    doxygen-doc/man/Esys_NV_GlobalWriteLock.3 \
    doxygen-doc/man/Esys_NV_Increment.3 \
    doxygen-doc/man/Esys_NV_Read.3 \
    doxygen-doc/man/Esys_NV_ReadLock.3 \
    doxygen-doc/man/Esys_NV_ReadPublic.3 \
    doxygen-doc/man/Esys_NV_SetBits.3 \
    doxygen-doc/man/Esys_NV_UndefineSpace.3 \
    doxygen-doc/man/Esys_NV_UndefineSpaceSpecial.3 \
    doxygen-doc/man/Esys_NV_Write.3 \
    doxygen-doc/man/Esys_NV_WriteLock.3 \
    doxygen-doc/man/Esys_ObjectChangeAuth.3 \
    doxygen-doc/man/Esys_PCR_Allocate.3 \
    doxygen-doc/man/Esys_PCR_Event.3 \
    doxygen-doc/man/Esys_PCR_Extend.3 \
    doxygen-doc/man/Esys_PCR_Read.3 \
    doxygen-doc/man/Esys_PCR_Reset.3 \
    doxygen-doc/man/Esys_PCR_SetAuthPolicy.3 \
    doxygen-doc/man/Esys_PCR_SetAuthValue.3 \
    doxygen-doc/man/Esys_PolicyAuthorize.3 \
    doxygen-doc/man/Esys_PolicyAuthValue.3 \
    doxygen-doc/man/Esys_PolicyCommandCode.3 \
    doxygen-doc/man/Esys_PolicyCounterTimer.3 \
    doxygen-doc/man/Esys_PolicyCpHash.3 \
    doxygen-doc/man/Esys_PolicyDuplicationSelect.3 \
    doxygen-doc/man/Esys_PolicyGetDigest.3 \
    doxygen-doc/man/Esys_PolicyLocality.3 \
    doxygen-doc/man/Esys_PolicyNameHash.3 \
    doxygen-doc/man/Esys_PolicyNV.3 \
    doxygen-doc/man/Esys_PolicyNvWritten.3 \
    doxygen-doc/man/Esys_PolicyOR.3 \
    doxygen-doc/man/Esys_PolicyPassword.3 \
    doxygen-doc/man/Esys_PolicyPCR.3 \
    doxygen-doc/man/Esys_PolicyPhysicalPresence.3 \
    doxygen-doc/man/Esys_PolicyRestart.3 \
    doxygen-doc/man/Esys_PolicySecret.3 \
    doxygen-doc/man/Esys_PolicySigned.3 \
    doxygen-doc/man/Esys_PolicyTicket.3 \
    doxygen-doc/man/Esys_PP_Commands.3 \
    doxygen-doc/man/Esys_Quote.3 \
    doxygen-doc/man/Esys_ReadClock.3 \
    doxygen-doc/man/Esys_ReadPublic.3 \
    doxygen-doc/man/Esys_Rewrap.3 \
    doxygen-doc/man/Esys_RSA_Decrypt.3 \
    doxygen-doc/man/Esys_RSA_Encrypt.3 \
    doxygen-doc/man/Esys_SelfTest.3 \
    doxygen-doc/man/Esys_SequenceComplete.3 \
    doxygen-doc/man/Esys_SequenceUpdate.3 \
    doxygen-doc/man/Esys_SetAlgorithmSet.3 \
    doxygen-doc/man/Esys_SetCommandCodeAuditStatus.3 \
    doxygen-doc/man/Esys_SetPrimaryPolicy.3 \
    doxygen-doc/man/Esys_Shutdown.3 \
    doxygen-doc/man/Esys_Sign.3 \
    doxygen-doc/man/Esys_StartAuthSession.3 \
    doxygen-doc/man/Esys_Startup.3 \
    doxygen-doc/man/Esys_StirRandom.3 \
    doxygen-doc/man/Esys_TestParms.3 \
    doxygen-doc/man/Esys_Unseal.3 \
    doxygen-doc/man/Esys_Vendor_TCG_Test.3 \
    doxygen-doc/man/Esys_VerifySignature.3 \
    doxygen-doc/man/Esys_ZGen_2Phase.3
$(DOXYMAN3): doxygen-doc
else #DOXYMAN
DOXYMAN3 =
endif #DOXYMAN

### Include make files ###
# Add source code files from bootstrap
include src_vars.mk

# Add test definitions
include Makefile-test.am

# Add fuzz definitions
include Makefile-fuzz.am

### Distribution files ###
# Add udev rule
udevrules_DATA   = dist/tpm-udev.rules

# Adding user and developer information
EXTRA_DIST += \
    CHANGELOG.md \
    CONTRIBUTING.md \
    INSTALL.md \
    LICENSE \
    MAINTAINERS \
    README.md \
    RELEASE.md \
    VERSION

# Windows code / core build files
EXTRA_DIST += \
    include/tss2/tss2_tcti_tbs.h \
    lib/tss2-tcti-tbs.def \
    src/tss2-tcti/tcti-tbs.c \
    src/tss2-tcti/tcti-tbs.h \
    src/tss2-tcti/tss2-tcti-tbs.vcxproj \
    tpm2-tss.sln

# tss2-dlopen wrappers
EXTRA_DIST += \
    tss2-dlopen/tss2-dlopen-rc.c \
    tss2-dlopen/tss2-dlopen-tctildr.c \
    tss2-dlopen/tss2-dlopen-mu.c \
    tss2-dlopen/tss2-dlopen-esys.c \
    tss2-dlopen/tss2-dlopen-fapi.c

# Generate the AUTHORS file from git log
AUTHORS :
	$(AM_V_GEN)git log --format='%aN <%aE>' | grep -v 'users.noreply.github.com' | sort | \
	    uniq -c | sort -nr | sed 's/^\s*//' | cut -d" " -f2- > $@
EXTRA_DIST += AUTHORS

# pkg-config setup. pc-file declarations happen in the corresponding modules
pkgconfig_DATA =
DISTCLEANFILES += $(pkgconfig_DATA)

# Base TSS2 headers
tss2dir = $(includedir)/tss2
tss2_HEADERS = \
    $(srcdir)/include/tss2/tss2_common.h \
    $(srcdir)/include/tss2/tss2_tcti.h \
    $(srcdir)/include/tss2/tss2_tpm2_types.h

### Internal utility library
libutil = libutil.la
noinst_LTLIBRARIES += $(libutil)
libutil_la_SOURCES = $(UTIL_SRC)

### TCG TSS Marshaling/Unmarshaling spec library ###
libtss2_mu = src/tss2-mu/libtss2-mu.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_mu.h
lib_LTLIBRARIES += $(libtss2_mu)
pkgconfig_DATA += lib/tss2-mu.pc
EXTRA_DIST += lib/tss2-mu.map lib/tss2-mu.def src/tss2-mu/tss2-mu.vcxproj

# Bump sys soname revision due to change in TPMU_CAPABILITY ABI
src_tss2_mu_libtss2_mu_la_LDFLAGS = -version-info 0:1:0

if HAVE_LD_VERSION_SCRIPT
src_tss2_mu_libtss2_mu_la_LDFLAGS += -Wl,--version-script=$(srcdir)/lib/tss2-mu.map
endif # HAVE_LD_VERSION_SCRIPT

src_tss2_mu_libtss2_mu_la_LIBADD = $(libutil)
src_tss2_mu_libtss2_mu_la_SOURCES = $(TSS2_MU_SRC)

### TCG TSS TCTI spec libraries ###
# tcti loader library
libtss2_tctildr = src/tss2-tcti/libtss2-tctildr.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_tctildr.h
lib_LTLIBRARIES += $(libtss2_tctildr)
pkgconfig_DATA += lib/tss2-tctildr.pc
EXTRA_DIST += lib/tss2-tctildr.map

src_tss2_tcti_libtss2_tctildr_la_CFLAGS = $(AM_CFLAGS)
if HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tctildr_la_LDFLAGS = \
    -Wl,--version-script=$(srcdir)/lib/tss2-tctildr.map
endif # HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tctildr_la_LIBADD = $(libutil)
src_tss2_tcti_libtss2_tctildr_la_SOURCES = \
    src/tss2-tcti/tctildr.c src/tss2-tcti/tctildr.h \
    src/tss2-tcti/tctildr-interface.h
if NO_DL
src_tss2_tcti_libtss2_tctildr_la_LIBADD += $(libtss2_tcti_device) $(libtss2_tcti_mssim)
src_tss2_tcti_libtss2_tctildr_la_SOURCES += src/tss2-tcti/tctildr-nodl.c src/tss2-tcti/tctildr-nodl.h
else
src_tss2_tcti_libtss2_tctildr_la_LIBADD += $(LIBADD_DL)
src_tss2_tcti_libtss2_tctildr_la_SOURCES += src/tss2-tcti/tctildr-dl.c src/tss2-tcti/tctildr-dl.h
endif

# tcti device library
if ENABLE_TCTI_DEVICE
libtss2_tcti_device = src/tss2-tcti/libtss2-tcti-device.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_tcti_device.h
lib_LTLIBRARIES += $(libtss2_tcti_device)
pkgconfig_DATA += lib/tss2-tcti-device.pc

if HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_device_la_LDFLAGS  = -Wl,--version-script=$(srcdir)/lib/tss2-tcti-device.map
endif # HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_device_la_LIBADD   = $(libtss2_mu) $(libutil)
src_tss2_tcti_libtss2_tcti_device_la_SOURCES  = \
    src/tss2-tcti/tcti-common.c \
    src/tss2-tcti/tcti-device.c
endif # ENABLE_TCTI_DEVICE
EXTRA_DIST += lib/tss2-tcti-device.map

# tcti library for swtpm
if ENABLE_TCTI_SWTPM
libtss2_tcti_swtpm = src/tss2-tcti/libtss2-tcti-swtpm.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_tcti_swtpm.h
lib_LTLIBRARIES += $(libtss2_tcti_swtpm)
pkgconfig_DATA += lib/tss2-tcti-swtpm.pc

if HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_swtpm_la_LDFLAGS  = -Wl,--version-script=$(srcdir)/lib/tss2-tcti-swtpm.map
endif # HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_swtpm_la_LIBADD   = $(libtss2_mu) $(libutil)
src_tss2_tcti_libtss2_tcti_swtpm_la_SOURCES  = \
    src/tss2-tcti/tcti-common.c \
    src/tss2-tcti/tcti-swtpm.c \
    src/tss2-tcti/tcti-swtpm.h
endif # ENABLE_TCTI_SWTPM
EXTRA_DIST += lib/tss2-tcti-swtpm.map lib/tss2-tcti-swtpm.def src/tss2-tcti/tss2-tcti-swtpm.vcxproj

# tcti library for Microsoft TPM2 simulator
if ENABLE_TCTI_MSSIM
libtss2_tcti_mssim = src/tss2-tcti/libtss2-tcti-mssim.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_tcti_mssim.h
lib_LTLIBRARIES += $(libtss2_tcti_mssim)
pkgconfig_DATA += lib/tss2-tcti-mssim.pc

if HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_mssim_la_LDFLAGS  = -Wl,--version-script=$(srcdir)/lib/tss2-tcti-mssim.map
endif # HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_mssim_la_LIBADD   = $(libtss2_mu) $(libutil)
src_tss2_tcti_libtss2_tcti_mssim_la_SOURCES  = \
    src/tss2-tcti/tcti-common.c \
    src/tss2-tcti/tcti-mssim.c
endif # ENABLE_TCTI_MSSIM
EXTRA_DIST += lib/tss2-tcti-mssim.map \
              lib/tss2-tcti-mssim.def \
              src/tss2-tcti/tss2-tcti-mssim.vcxproj

# tcti pcap library
if ENABLE_TCTI_PCAP
libtss2_tcti_pcap = src/tss2-tcti/libtss2-tcti-pcap.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_tcti_pcap.h
lib_LTLIBRARIES += $(libtss2_tcti_pcap)
pkgconfig_DATA += lib/tss2-tcti-pcap.pc

if HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_pcap_la_LDFLAGS  = -Wl,--version-script=$(srcdir)/lib/tss2-tcti-pcap.map
endif # HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_pcap_la_LIBADD   = $(libtss2_tctildr) $(libtss2_mu) $(libutil)
src_tss2_tcti_libtss2_tcti_pcap_la_SOURCES  = \
    src/tss2-tcti/tcti-common.c \
    src/tss2-tcti/tcti-pcap-builder.c \
    src/tss2-tcti/tcti-pcap.c
endif # ENABLE_TCTI_PCAP
EXTRA_DIST += lib/tss2-tcti-pcap.map

# tcti libtpms library
if ENABLE_TCTI_LIBTPMS
libtss2_tcti_libtpms = src/tss2-tcti/libtss2-tcti-libtpms.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_tcti_libtpms.h
lib_LTLIBRARIES += $(libtss2_tcti_libtpms)
pkgconfig_DATA += lib/tss2-tcti-libtpms.pc

if HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_libtpms_la_LDFLAGS  = -Wl,--version-script=$(srcdir)/lib/tss2-tcti-libtpms.map
endif # HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_libtpms_la_LIBADD   = $(libtss2_mu) $(libutil)
src_tss2_tcti_libtss2_tcti_libtpms_la_SOURCES  = \
    src/tss2-tcti/tcti-common.c \
    src/tss2-tcti/tcti-libtpms.c \
    src/tss2-tcti/tcti-libtpms.h
endif # ENABLE_TCTI_LIBTPMS
EXTRA_DIST += lib/tss2-tcti-libtpms.map

# tcti library for sub-process commands
if ENABLE_TCTI_CMD
libtss2_tcti_cmd = src/tss2-tcti/libtss2-tcti-cmd.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_tcti_cmd.h
lib_LTLIBRARIES += $(libtss2_tcti_cmd)
pkgconfig_DATA += lib/tss2-tcti-cmd.pc

if HAVE_LD_VERSION_SCRIPT
if !UNIT
src_tss2_tcti_libtss2_tcti_cmd_la_LDFLAGS  = -Wl,--version-script=$(srcdir)/lib/tss2-tcti-cmd.map
endif # UNIT
endif # HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_cmd_la_LIBADD   = $(libutil) $(libtss2_mu)
src_tss2_tcti_libtss2_tcti_cmd_la_SOURCES  = \
    src/tss2-tcti/tcti-common.c \
    src/tss2-tcti/tcti-cmd.c \
    src/tss2-tcti/tcti-cmd.h
endif # ENABLE_TCTI_CMD
EXTRA_DIST += lib/tss2-tcti-cmd.map \
              lib/tss2-tcti-cmd.def

# tcti library for spi connected tpms
if ENABLE_TCTI_SPI_HELPER
libtss2_tcti_spi_helper = src/tss2-tcti/libtss2-tcti-spi-helper.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_tcti_spi_helper.h
lib_LTLIBRARIES += $(libtss2_tcti_spi_helper)
pkgconfig_DATA += lib/tss2-tcti-spi-helper.pc
EXTRA_DIST += lib/tss2-tcti-spi-helper.map \
              lib/tss2-tcti-spi-helper.def

if HAVE_LD_VERSION_SCRIPT
if !UNIT
src_tss2_tcti_libtss2_tcti_spi_helper_la_LDFLAGS  = -Wl,--version-script=$(srcdir)/lib/tss2-tcti-spi-helper.map
endif # UNIT
endif # HAVE_LD_VERSION_SCRIPT
src_tss2_tcti_libtss2_tcti_spi_helper_la_LIBADD   = $(libutil) $(libtss2_mu)
src_tss2_tcti_libtss2_tcti_spi_helper_la_SOURCES  = \
    src/tss2-tcti/tcti-common.c \
    src/tss2-tcti/tcti-spi-helper.c \
    src/tss2-tcti/tcti-spi-helper.h
endif # ENABLE_TCTI_SPI_HELPER

### TCG TSS SYS spec library ###
libtss2_sys = src/tss2-sys/libtss2-sys.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_sys.h
lib_LTLIBRARIES += $(libtss2_sys)
pkgconfig_DATA += lib/tss2-sys.pc

src_tss2_sys_libtss2_sys_la_CFLAGS = $(AM_CFLAGS) -I$(srcdir)/src/tss2-sys
src_tss2_sys_libtss2_sys_la_LDFLAGS = $(AM_LDFLAGS) $(LIBSOCKET_LDFLAGS)

if HAVE_LD_VERSION_SCRIPT
src_tss2_sys_libtss2_sys_la_LDFLAGS += -Wl,--version-script=$(srcdir)/lib/tss2-sys.map
endif # HAVE_LD_VERSION_SCRIPT

# Bump sys soname current due to commit 1414f73902cd0c64e447522c64c8e439fa2074b7
# Breaking the backwards compatibility of Tss2_Sys_ReadClock call.
# Bump sys soname revision due to change in TPMU_CAPABILITY ABI
src_tss2_sys_libtss2_sys_la_LDFLAGS += -version-info 1:1:0

src_tss2_sys_libtss2_sys_la_LIBADD = $(libtss2_mu)
src_tss2_sys_libtss2_sys_la_SOURCES = $(TSS2_SYS_SRC) \
	src/util/log.c
EXTRA_DIST += lib/tss2-sys.map lib/tss2-sys.def src/tss2-sys/tss2-sys.vcxproj

### TCG TSS ESYS spec library ###
if ESYS
libtss2_esys = src/tss2-esys/libtss2-esys.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_esys.h
lib_LTLIBRARIES += $(libtss2_esys)
pkgconfig_DATA += lib/tss2-esys.pc

if ESYS_OSSL
TSS2_ESYS_SRC_CRYPTO = src/tss2-esys/esys_crypto_ossl.h src/tss2-esys/esys_crypto_ossl.c
endif
if ESYS_MBED
TSS2_ESYS_SRC_CRYPTO = src/tss2-esys/esys_crypto_mbed.h src/tss2-esys/esys_crypto_mbed.c
endif

src_tss2_esys_libtss2_esys_la_CFLAGS  = $(AM_CFLAGS) -I$(srcdir)/src/tss2-esys \
    $(TSS2_ESYS_CFLAGS_CRYPTO)
src_tss2_esys_libtss2_esys_la_LIBADD  = $(libtss2_sys) $(libtss2_mu) $(libutil)

src_tss2_esys_libtss2_esys_la_LDFLAGS = $(AM_LDFLAGS) $(LIBSOCKET_LDFLAGS) \
                                        $(TSS2_ESYS_LDFLAGS_CRYPTO)
if HAVE_LD_VERSION_SCRIPT
src_tss2_esys_libtss2_esys_la_LDFLAGS += -Wl,--version-script=$(srcdir)/lib/tss2-esys.map
endif # HAVE_LD_VERSION_SCRIPT

# Bump sys soname due to change in TPMU_CAPABILITY ABI
src_tss2_esys_libtss2_esys_la_LDFLAGS += -version-info 0:1:0

src_tss2_esys_libtss2_esys_la_SOURCES = $(TSS2_ESYS_SRC) $(TSS2_ESYS_SRC_CRYPTO) \
    src/tss2-tcti/tctildr.c src/tss2-tcti/tctildr.h \
    src/tss2-tcti/tctildr-interface.h
if NO_DL
src_tss2_esys_libtss2_esys_la_LIBADD += $(libtss2_tcti_device) $(libtss2_tcti_mssim) $(libtss2_tcti_cmd)
src_tss2_esys_libtss2_esys_la_SOURCES += src/tss2-tcti/tctildr-nodl.c src/tss2-tcti/tctildr-nodl.h
else
src_tss2_esys_libtss2_esys_la_LIBADD += $(LIBADD_DL)
src_tss2_esys_libtss2_esys_la_SOURCES += src/tss2-tcti/tctildr-dl.c src/tss2-tcti/tctildr-dl.h
endif
EXTRA_DIST += lib/tss2-esys.map \
              lib/tss2-esys.def \
              src/tss2-esys/tss2-esys.vcxproj
endif #ESYS

### TCG TSS error decoding spec library ###
libtss2_rc = src/tss2-rc/libtss2-rc.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_rc.h
lib_LTLIBRARIES += $(libtss2_rc)
pkgconfig_DATA += lib/tss2-rc.pc
EXTRA_DIST += lib/tss2-rc.map lib/tss2-rc.def

if HAVE_LD_VERSION_SCRIPT
src_tss2_rc_libtss2_rc_la_LDFLAGS = -Wl,--version-script=$(srcdir)/lib/tss2-rc.map
endif # HAVE_LD_VERSION_SCRIPT
src_tss2_rc_libtss2_rc_la_SOURCES = $(TSS2_RC_SRC)

### TSS Policy library ###
if POLICY
libtss2_policy = src/tss2-policy/libtss2-policy.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_policy.h
lib_LTLIBRARIES += $(libtss2_policy)
pkgconfig_DATA += lib/tss2-policy.pc

src_tss2_policy_libtss2_policy_la_CFLAGS = $(AM_CFLAGS) -I$(srcdir)/src/tss2-policy -I$(srcdir)/src/tss2-fapi \
    $(JSONC_CFLAGS)
src_tss2_policy_libtss2_policy_la_LIBADD  = $(libtss2_esys) $(libtss2_mu) $(libutil) $(JSONC_LIBS) $(UUID_LIBS)

if HAVE_LD_VERSION_SCRIPT
src_tss2_policy_libtss2_policy_la_LDFLAGS = -Wl,--version-script=$(srcdir)/lib/tss2-policy.map
endif # HAVE_LD_VERSION_SCRIPT

src_tss2_policy_libtss2_policy_la_SOURCES = $(TSS2_POLICY_SRC) \
    src/tss2-fapi/fapi_crypto.c \
    src/tss2-fapi/ifapi_eventlog.c \
    src/tss2-fapi/ifapi_ima_eventlog.c \
    src/tss2-fapi/ifapi_eventlog_system.c \
    src/tss2-fapi/ifapi_helpers.c \
    src/tss2-fapi/ifapi_io.c \
    src/tss2-fapi/ifapi_json_deserialize.c \
    src/tss2-fapi/ifapi_json_serialize.c \
    src/tss2-fapi/tpm_json_deserialize.c \
    src/tss2-fapi/tpm_json_serialize.c \
    src/tss2-fapi/ifapi_json_eventlog_serialize.c \
    src/tss2-fapi/ifapi_policy.c \
    src/tss2-fapi/ifapi_policy_calculate.c \
    src/tss2-fapi/ifapi_policy_execute.c \
    src/tss2-fapi/ifapi_policy_instantiate.c  \
    src/tss2-fapi/ifapi_policy_json_deserialize.c \
    src/tss2-fapi/ifapi_policy_json_serialize.c \
    src/tss2-fapi/ifapi_keystore.c \
    src/tss2-fapi/ifapi_policy_store.c

EXTRA_DIST += lib/tss2-policy.map lib/tss2-policy.def
endif

### TCG TSS FAPI spec library ###
if FAPI
fapiconfdir = @sysconfdir@/tpm2-tss
fapiconf_DATA = fapi-config.json

CLEANFILES += fapi-config.json \
              man/man5/fapi-config.5 \
              man/man5/fapi-profile.5

# We have to do this ourselves, in order to get absolute paths
fapi-config.json: dist/fapi-config.json.in
	$(AM_V_GEN) $(SED) \
		-e 's|[@]prefix@|$(prefix)|g' \
		-e 's|[@]datarootdir@|$(datarootdir)|g' \
		-e 's|[@]datadir@|$(datadir)|g' \
		-e 's|[@]sysconfdir@|$(sysconfdir)|g' \
		-e 's|[@]sharedstatedir@|$(sharedstatedir)|g' \
		-e 's|[@]localstatedir@|$(localstatedir)|g' \
		-e 's|[@]runstatedir@|$(runstatedir)|g' \
		-e 's|[@]userstatedir@|$(userstatedir)|g' \
		-e 's|[@]imameasurements@|$(imameasurements)|g' \
		-e 's|[@]sysmeasurements@|$(sysmeasurements)|g' \
		< "$<" > "$@"

sysusers_DATA = dist/sysusers.d/tpm2-tss.conf
tmpfiles_DATA = tpm2-tss-fapi.conf

CLEANFILES += tpm2-tss-fapi.conf

# We have to do this ourselves, in order to get absolute paths
tpm2-tss-fapi.conf: dist/tmpfiles.d/tpm2-tss-fapi.conf.in
	$(AM_V_GEN) $(SED) \
		-e 's|[@]localstatedir@|$(localstatedir)|g' \
		-e 's|[@]runstatedir@|$(runstatedir)|g' \
		< "$<" > "$@"

fapiprofilesdir = @sysconfdir@/tpm2-tss/fapi-profiles
fapiprofiles_DATA = dist/fapi-profiles/P_RSA2048SHA256.json \
                    dist/fapi-profiles/P_ECCP256SHA256.json

libtss2_fapi = src/tss2-fapi/libtss2-fapi.la
tss2_HEADERS += $(srcdir)/include/tss2/tss2_fapi.h
lib_LTLIBRARIES += $(libtss2_fapi)
pkgconfig_DATA += lib/tss2-fapi.pc
EXTRA_DIST +=  \
    dist/fapi-config.json.in \
    dist/fapi-profiles/P_RSA2048SHA256.json \
    dist/fapi-profiles/P_ECCP256SHA256.json \
    dist/sysusers.d/tpm2-tss.conf \
    dist/tmpfiles.d/tpm2-tss-fapi.conf.in \
    doc/fapi-config.md \
    doc/fapi-profile.md \
    lib/tss2-fapi.map \
    lib/tss2-fapi.def \
    man/fapi-config.5.in \
    man/fapi-profile.5.in \
    man/man-postlude-fapi.troff \
    test/data/fapi/P_RSA_EK_persistent.json \
    test/data/fapi/P_RSA.json \
    test/data/fapi/P_RSA2.json \
    test/data/fapi/P_RSA_nameAlg_sha1.json \
    test/data/fapi/P_ECC_sh_eh_policy.json \
    test/data/fapi/P_ECC_error.json \
    test/data/fapi/P_RSA_sh_policy.json \
    test/data/fapi/P_RSA256.json \
    test/data/fapi/P_ECC.json \
    test/data/fapi/P_ECC384.json \
    test/data/fapi/P_ECC_system.json \
    test/data/fapi/policy/pol_pcr16_0.json \
    test/data/fapi/policy/pol_pcr16_0_rsa_authorized.json \
    test/data/fapi/policy/pol_pcr16_0_ecc_authorized.json \
    test/data/fapi/policy/pol_pcr16_0_fail.json \
    test/data/fapi/policy/pol_pcr16_0_or.json \
    test/data/fapi/policy/pol_pcr8_0.json \
    test/data/fapi/policy/pol_nv.json \
    test/data/fapi/policy/pol_nv_tpm_idx.json \
    test/data/fapi/policy/pol_nv_counter.json \
    test/data/fapi/policy/pol_nv_written.json \
    test/data/fapi/policy/pol_signed.json \
    test/data/fapi/policy/pol_signed_keyedhash.json \
    test/data/fapi/policy/pol_signed_ecc.json \
    test/data/fapi/policy/pol_authorize.json \
    test/data/fapi/policy/pol_authorize_rsa_pem.json \
    test/data/fapi/policy/pol_authorize_ecc_pem.json \
    test/data/fapi/policy/pol_authorize_outer.json \
    test/data/fapi/policy/pol_authorize_nv.json \
    test/data/fapi/policy/pol_authorize_nv_tpms.json \
    test/data/fapi/policy/pol_authorize_nv_complex_tpm2b.json \
    test/data/fapi/policy/pol_secret.json \
    test/data/fapi/policy/pol_secret_key.json \
    test/data/fapi/policy/pol_password.json \
    test/data/fapi/policy/pol_auth_value.json \
    test/data/fapi/policy/pol_command_code.json \
    test/data/fapi/policy/pol_locality.json \
    test/data/fapi/policy/pol_physical_presence.json \
    test/data/fapi/policy/pol_duplicate.json \
    test/data/fapi/policy/pol_nv_change_auth.json \
    test/data/fapi/policy/pol_countertimer.json \
    test/data/fapi/policy/pol_name_hash.json \
    test/data/fapi/policy/pol_pcr16_read.json \
    test/data/fapi/policy/pol_action.json \
    test/data/fapi/policy/pol_cphash.json \
    test/data/fapi/policy/pol_or_read_write_secret.json \
    test/data/fapi/policy/pol_ek_high_range_sha256.json \
    test/data/fapi/P_ECC_sh_eh_policy_sha384.json \
    test/data/fapi/policy/pol_authorize_ecc_pem_sha384.json \
    test/data/fapi/policy/pol_authorize_nv_complex_tpm2b_sha384.json \
    test/data/fapi/policy/pol_authorize_nv_tpms_sha384.json \
    test/data/fapi/policy/pol_authorize_nv_sha384.json \
    test/data/fapi/policy/pol_cphash_sha384.json \
    test/data/fapi/policy/pol_pcr16_0_ecc_authorized_sha384.json \
    test/data/fapi/policy/pol_template.json \
    test/data/fapi/eventlog/binary_measurements_nuc.b64 \
    test/data/fapi/eventlog/binary_measurements_pc_client.b64 \
    test/data/fapi/eventlog/event.b64 \
    test/data/fapi/eventlog/event-uefiaction.b64 \
    test/data/fapi/eventlog/event-uefiservices.b64 \
    test/data/fapi/eventlog/event-uefivar.b64 \
    test/data/fapi/eventlog/specid-vendordata.b64 \
    test/data/fapi/eventlog/sml-ima-ng-sha1.b64 \
    test/data/fapi/eventlog/sml-ima-sha1.b64 \
    test/data/fapi/eventlog/sml-ima-sig-sha256.b64 \
    test/data/fapi/eventlog/sml-ima-ng-sha1-invalidated.b64 \
    test/data/fapi/eventlog/sml-ima-ng-sha1-invalidated.b64 \
    test/data/fapi/eventlog/sml-ima-sig-sha256-invalidated.b64 \
    test/data/fapi/eventlog/sml-ima-sha1-invalidated.b64

src_tss2_fapi_libtss2_fapi_la_LIBADD  = $(libtss2_sys) $(libtss2_mu) $(libtss2_esys) \
    $(libutil) $(libtss2_tctildr)

src_tss2_fapi_libtss2_fapi_la_SOURCES = $(TSS2_FAPI_SRC)
src_tss2_fapi_libtss2_fapi_la_CFLAGS  = $(AM_CFLAGS) -I$(srcdir)/src/tss2-fapi $(CRYPTO_CFLAGS) $(JSONC_CFLAGS) $(CURL_CFLAGS)
src_tss2_fapi_libtss2_fapi_la_LDFLAGS = $(AM_LDFLAGS) $(CRYPTO_LIBS) $(JSONC_LIBS) $(CURL_LIBS) $(UUID_LIBS)
if HAVE_LD_VERSION_SCRIPT
src_tss2_fapi_libtss2_fapi_la_LDFLAGS += -Wl,--version-script=$(srcdir)/lib/tss2-fapi.map
endif # HAVE_LD_VERSION_SCRIPT

# Bump soname current due to commit e0636dd6fbec4f286cc908117ecef4d820a50f79 breaking
# The API and ABI of Fapi_CB_{Auth,Sign,Branch,PolicyAction}
src_tss2_fapi_libtss2_fapi_la_LDFLAGS += -version-info 1:0:0

if DOXYMAN
DOXYMAN3 += \
    doxygen-doc/man/Fapi_AuthorizePolicy.3 \
    doxygen-doc/man/Fapi_ChangeAuth.3 \
    doxygen-doc/man/Fapi_CreateKey.3 \
    doxygen-doc/man/Fapi_CreateNv.3 \
    doxygen-doc/man/Fapi_CreateSeal.3 \
    doxygen-doc/man/Fapi_Decrypt.3 \
    doxygen-doc/man/Fapi_Delete.3 \
    doxygen-doc/man/Fapi_Encrypt.3 \
    doxygen-doc/man/Fapi_ExportKey.3 \
    doxygen-doc/man/Fapi_ExportPolicy.3 \
    doxygen-doc/man/Fapi_Finalize.3 \
    doxygen-doc/man/Fapi_Free.3 \
    doxygen-doc/man/Fapi_GetAppData.3 \
    doxygen-doc/man/Fapi_GetCertificate.3 \
    doxygen-doc/man/Fapi_GetDescription.3 \
    doxygen-doc/man/Fapi_GetInfo.3 \
    doxygen-doc/man/Fapi_GetPlatformCertificates.3 \
    doxygen-doc/man/Fapi_GetPollHandles.3 \
    doxygen-doc/man/Fapi_GetRandom.3 \
    doxygen-doc/man/Fapi_GetTcti.3 \
    doxygen-doc/man/Fapi_GetTpmBlobs.3 \
    doxygen-doc/man/Fapi_Import.3 \
    doxygen-doc/man/Fapi_Initialize.3 \
    doxygen-doc/man/Fapi_List.3 \
    doxygen-doc/man/Fapi_NvExtend.3 \
    doxygen-doc/man/Fapi_NvIncrement.3 \
    doxygen-doc/man/Fapi_NvRead.3 \
    doxygen-doc/man/Fapi_NvSetBits.3 \
    doxygen-doc/man/Fapi_NvWrite.3 \
    doxygen-doc/man/Fapi_PcrExtend.3 \
    doxygen-doc/man/Fapi_PcrRead.3 \
    doxygen-doc/man/Fapi_Provision.3 \
    doxygen-doc/man/Fapi_Quote.3 \
    doxygen-doc/man/Fapi_SetAppData.3 \
    doxygen-doc/man/Fapi_SetAuthCB.3 \
    doxygen-doc/man/Fapi_SetBranchCB.3 \
    doxygen-doc/man/Fapi_SetCertificate.3 \
    doxygen-doc/man/Fapi_SetDescription.3 \
    doxygen-doc/man/Fapi_SetSignCB.3 \
    doxygen-doc/man/Fapi_Sign.3 \
    doxygen-doc/man/FapiTestgroup.3 \
    doxygen-doc/man/Fapi_Unseal.3 \
    doxygen-doc/man/Fapi_VerifyQuote.3 \
    doxygen-doc/man/Fapi_VerifySignature.3 \
    doxygen-doc/man/Fapi_WriteAuthorizeNv.3
endif #DOXYMAN

endif #FAPI

### Helper Functions ###
define make_parent_dir
    if [ ! -d $(dir $1) ]; then mkdir -p $(dir $1); fi
endef

define make_tss_user_and_group
    if test -z "${DESTDIR}"; then \
        if type -p groupadd > /dev/null; then \
            id -g tss 2>/dev/null || groupadd --system tss; \
        else \
            id -g tss 2>/dev/null || \
            addgroup --system tss; \
        fi && \
        if type -p useradd > /dev/null; then \
            id -u tss 2>/dev/null || \
            useradd --system --home-dir / --shell `type -p nologin` \
                             --no-create-home -g tss tss; \
        else \
            id -u tss 2>/dev/null || \
            adduser --system --home / --shell `type -p nologin` \
                    --no-create-home --ingroup tss tss; \
        fi; \
    fi
endef

define make_tss_dir
    ($(call make_parent_dir,$1))
endef

define set_tss_permissions
    (chown -R tss:tss "$1") && \
    (chmod -R 2775 "$1") && \
    (setfacl -m default:group:tss:rwx "$1")
endef

define make_fapi_dirs
    ($(call make_tss_dir,$(DESTDIR)$(runstatedir)/tpm2-tss/eventlog/) || true) && \
    ($(call make_tss_dir,$(DESTDIR)$(localstatedir)/lib/tpm2-tss/system/keystore/))
endef

define set_fapi_permissions
    if test -z "${DESTDIR}"; then \ e
        ($(call set_tss_permissions,$(DESTDIR)$(runstatedir)/tpm2-tss)) && \
        ($(call set_tss_permissions,$(DESTDIR)$(localstatedir)/lib/tpm2-tss)) \
    fi
endef

define check_dir
    if [ ! -d "$1" ]; then echo "WARNING Directory $1 could not be created"; fi
endef

define check_fapi_dirs
    if test -z "${DESTDIR}"; then \
        ($(call check_dir,$(DESTDIR)$(runstatedir)/tpm2-tss/eventlog/)) && \
        ($(call check_dir,$(DESTDIR)$(localstatedir)/lib/tpm2-tss/system/keystore/)) \
    fi;
endef

### Man Pages
man3_MANS = \
    man/man3/Tss2_Tcti_Cmd_Init.3 \
    man/man3/Tss2_Tcti_Device_Init.3 \
    man/man3/Tss2_Tcti_Mssim_Init.3 \
    man/man3/Tss2_TctiLdr_Finalize.3 \
    man/man3/Tss2_TctiLdr_FreeInfo.3 \
    man/man3/Tss2_TctiLdr_GetInfo.3 \
    man/man3/Tss2_TctiLdr_Initialize.3 \
    $(DOXYMAN3)

man7_MANS = \
    man/man7/tss2-tcti-device.7 \
    man/man7/tss2-tcti-swtpm.7 \
    man/man7/tss2-tcti-mssim.7 \
    man/man7/tss2-tcti-cmd.7 \
    man/man7/tss2-tctildr.7

if FAPI
man5_MANS = \
    man/man5/fapi-config.5 \
    man/man5/fapi-profile.5
endif #FAPI

man/man3/%.3 : man/%.3.in $(srcdir)/man/man-postlude.troff
	$(AM_V_GEN)$(call make_man,$@,$<,$(srcdir)/man/man-postlude.troff)

man/man7/%.7 : man/%.7.in $(srcdir)/man/man-postlude.troff
	$(AM_V_GEN)$(call make_man,$@,$<,$(srcdir)/man/man-postlude.troff)

if FAPI
man/man5/%.5 : man/%.5.in $(srcdir)/man/man-postlude-fapi.troff
	$(AM_V_GEN)$(call make_man,$@,$<,$(srcdir)/man/man-postlude-fapi.troff)
install-man-fapi: install-man3 install-man5 install-man7
	$(LN_S) -f Tss2_TctiLdr_Initialize.3 $(DESTDIR)$(man3dir)/Tss2_TctiLdr_Initialize_Ex.3
else
install-man: install-man3 install-man7
	$(LN_S) -f Tss2_TctiLdr_Initialize.3 $(DESTDIR)$(man3dir)/Tss2_TctiLdr_Initialize_Ex.3
endif #FAPI

EXTRA_DIST += dist/tpm-udev.rules

install-dirs:
if HOSTOS_LINUX
if SYSD_SYSUSERS
	@test -n "$(DESTDIR)" || echo "systemd-sysusers $(sysusersdir)/tpm2-tss.conf"
	@test -n "$(DESTDIR)" || ( systemd-sysusers $(sysusersdir)/tpm2-tss.conf || echo "WARNING Failed to create the tss user and group" )
else
	@echo "call make_tss_user_and_group"
	@$(call make_tss_user_and_group) || echo "WARNING Failed to create the tss user and group"
endif
if SYSD_TMPFILES
	@test -n "$(DESTDIR)" || echo "systemd-tmpfiles --create $(tmpfilesdir)/tpm2-tss-fapi.conf"
	@test -n "$(DESTDIR)" || ( systemd-tmpfiles --create $(tmpfilesdir)/tpm2-tss-fapi.conf|| echo "WARNING Failed to create the FAPI directories with the correct permissions" )
	@test -z "$(DESTDIR)" || echo "(call make_fapi_dirs)"
	@test -z "$(DESTDIR)" || $(call make_fapi_dirs)
else
	@echo "(call make_fapi_dirs) && (call set_fapi_permissions)"
	@-$(call make_fapi_dirs) && $(call set_fapi_permissions) || echo "WARNING Failed to create the FAPI directories with the correct permissions"
endif
	@test -n "$(DESTDIR)" || echo "call check_fapi_dirs"
	@test -n "$(DESTDIR)" || $(call check_fapi_dirs)
endif

install-data-hook: install-dirs
	-if [ ! -z "$(udevrulesprefix)" ]; then \
		mv $(DESTDIR)$(udevrulesdir)/tpm-udev.rules $(DESTDIR)$(udevrulesdir)/$(udevrulesprefix)tpm-udev.rules; \
	fi

uninstall-local:
	-rm $(DESTDIR)$(udevrulesdir)/$(udevrulesprefix)tpm-udev.rules
	cd $(DESTDIR)$(man3dir) && \
		[ -L Tss2_TctiLdr_Initialize_Ex.3 ] && \
			rm -f Tss2_TctiLdr_Initialize_Ex.3 || true

EXTRA_DIST += \
    doc/doxygen.dox \
    doc/coding_standard_c.md \
    doc/logging.md \
    doc/fuzzing.md \
    doc/TSS_block_diagram.png \
    man/man-postlude.troff \
    man/Tss2_Tcti_Cmd_Init.3.in \
    man/Tss2_Tcti_Device_Init.3.in \
    man/Tss2_Tcti_Mssim_Init.3.in \
    man/Tss2_TctiLdr_Finalize.3.in \
    man/Tss2_TctiLdr_FreeInfo.3.in \
    man/Tss2_TctiLdr_GetInfo.3.in \
    man/Tss2_TctiLdr_Initialize.3.in \
    man/tss2-tcti-pcap.7.in \
    man/tss2-tcti-device.7.in \
    man/man7/tss2-tcti-swtpm.7 \
    man/tss2-tcti-mssim.7.in \
    man/tss2-tcti-cmd.7.in \
    man/tss2-tctildr.7.in

CLEANFILES += \
    $(man3_MANS) \
    $(man7_MANS)

# function to transform man .in files to man pages
# $1: target
# $2: .in file
# $3: man postlude file
define make_man
    $(call make_parent_dir,$1) && \
    cat $2 $3 > "$1_tmp" && \
    $(SED) 's/[@]VERSION[@]/$(PACKAGE_VERSION)/g' "$1_tmp" > $1 && \
    rm "$1_tmp"
endef
