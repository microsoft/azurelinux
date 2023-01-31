# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2015 - 2020 Intel Corporation
# Copyright (c) 2018 - 2020 Fraunhofer SIT sponsored by Infineon Technologies AG
# All rights reserved.

AC_INIT([tpm2-tss],
        [m4_esyscmd_s([cat ./VERSION])],
        [https://github.com/tpm2-software/tpm2-tss/issues],
        [],
        [https://github.com/tpm2-software/tpm2-tss])
AC_CONFIG_MACRO_DIR([m4])
AM_INIT_AUTOMAKE([foreign
                  subdir-objects])
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])]) #Backward compatible setting of "silent-rules"

AC_CONFIG_HEADERS([config.h])

AC_CONFIG_FILES([Makefile Doxyfile lib/tss2-sys.pc lib/tss2-esys.pc lib/tss2-mu.pc lib/tss2-tcti-device.pc lib/tss2-tcti-mssim.pc lib/tss2-tcti-swtpm.pc lib/tss2-tcti-pcap.pc lib/tss2-tcti-libtpms.pc lib/tss2-rc.pc lib/tss2-tctildr.pc lib/tss2-fapi.pc lib/tss2-tcti-cmd.pc lib/tss2-policy.pc lib/tss2-tcti-spi-helper.pc])

# propagate configure arguments to distcheck
AC_SUBST([DISTCHECK_CONFIGURE_FLAGS],[$ac_configure_args])

AC_CANONICAL_HOST

AX_IS_RELEASE(dash-version)
AX_CHECK_ENABLE_DEBUG([info])

AC_PROG_CC
AC_PROG_CXX
AC_PROG_LN_S
AC_USE_SYSTEM_EXTENSIONS
LT_INIT()
LT_LIB_DLLOAD
PKG_INSTALLDIR()

# Check OS and set library and compile flags accordingly
case "${host_os}" in
    *nto-qnx*)
        HOSTOS='QNX'
        ADD_COMPILER_FLAG([-D_QNX_SOURCE])
        LIBSOCKET_LDFLAGS="-lsocket"
        ;;
    *bsd* | *BSD*)
        HOSTOS='BSD'
        LIBSOCKET_LDFLAGS=""
        ;;
    *)
        #Assume linux
        HOSTOS='Linux'
        LIBSOCKET_LDFLAGS=""
        ;;
esac
AC_SUBST([LIBSOCKET_LDFLAGS])
AC_SUBST([HOSTOS])

AM_CONDITIONAL(HOSTOS_LINUX, [test x"$HOSTOS" = xLinux])

IMA_MEASUREMENTS="/sys/kernel/security/ima/binary_runtime_measurements"

AS_IF([ test -e "$IMA_MEASUREMENTS"], [imameasurements_std="$IMA_MEASUREMENTS" ],
      [imameasurements_std="/dev/null" ] )
AC_SUBST(imameasurements_std)

AC_ARG_WITH([imameasurements],
            [AS_HELP_STRING([--with-imameasurements=<file>],
                            [sets file with the IMA measurements")])],,
            [with_imameasurements=$imameasurements_std])
AC_SUBST(imameasurements, $with_imameasurements)

SYSTEM_MEASUREMENTS="/sys/kernel/security/tpm0/binary_bios_measurements"

AS_IF([test -e "$SYSTEM_MEASUREMENTS"], [sysmeasurements_std="$SYSTEM_MEASUREMENTS" ],
      [sysmeasurements_std="/dev/null" ] )
AC_SUBST(sysmeasurements_std)


AC_ARG_WITH([sysmeasurements],
            [AS_HELP_STRING([--with-sysmeasurements=<file>],
                            [sets file with the binary bios measurements")])],,
            [with_sysmeasurements=$sysmeasurements_std])
AC_SUBST(sysmeasurements, $with_sysmeasurements)

# runstatedir is only defined in the yet unreleased Autoconf 2.70
AC_ARG_WITH([runstatedir],
            AS_HELP_STRING([--with-runstatedir=<dir>],
                           [replacement for --runstatedir in Autoconf <2.70]),
            [runstatedir="$withval"])
AS_IF([test -z "$runstatedir"], [runstatedir="${localstatedir}/run"])
AC_SUBST([runstatedir])

AX_RECURSIVE_EVAL([$sysconfdir], [SYSCONFDIR])
AC_DEFINE_UNQUOTED([SYSCONFDIR], ["$SYSCONFDIR"], [System config dir])

AC_ARG_WITH([userstatedir],
            [AS_HELP_STRING([--with-userstatedir=<dir>],
                            [sets the relative path in the user's home (default is ".local/share")])],,
            [with_userstatedir=.local/share])
AC_SUBST(userstatedir, $with_userstatedir)

AC_ARG_WITH([sysusersdir],
            [AS_HELP_STRING([--with-sysusersdir=<dir>],
                            [sets the sysusers.d directory (default is "${sysconfdir}/sysusers.d")])],,
            [with_sysusersdir="${sysconfdir}/sysusers.d"])
AC_SUBST(sysusersdir, $with_sysusersdir)

AC_ARG_WITH([tmpfilesdir],
            [AS_HELP_STRING([--with-tmpfilesdir=<dir>],
                            [sets the tmpfiles.d directory (default is "${sysconfdir}/tmpfiles.d")])],,
            [with_tmpfilesdir="${sysconfdir}/tmpfiles.d"])
AC_SUBST(tmpfilesdir, $with_tmpfilesdir)

AC_ARG_ENABLE([unit],
            [AS_HELP_STRING([--enable-unit],
                            [build cmocka unit tests])],,
            [enable_unit=no])
m4_define([cmocka_min_version], [1.0])
m4_define([cmocka_err], [Unit test enabled, but cmocka missing or version requirements not met. cmocka version must be >= cmocka_min_version])
AS_IF([test "x$enable_unit" != xno],
      [PKG_CHECK_MODULES([CMOCKA],
                         [cmocka >= cmocka_min_version],,
                         [AC_MSG_ERROR([cmocka_err])])])
AM_CONDITIONAL([UNIT], [test "x$enable_unit" != xno])
AS_IF([test "x$enable_unit" != xno],
    [AC_DEFINE(UNIT, 1, [Enable for UNIT testing])])

AC_ARG_ENABLE([esys],
            [AS_HELP_STRING([--disable-esys],
                            [don't build the esys layer])],,
            [enable_esys=yes])

AM_CONDITIONAL(ESYS, test "x$enable_esys" = "xyes")

AC_CHECK_FUNC([strndup],[],[AC_MSG_ERROR([strndup function not found])])
AC_CHECK_FUNCS([reallocarray])
AC_ARG_ENABLE([fapi],
            [AS_HELP_STRING([--enable-fapi],
                            [build the fapi layer (default is yes)])],
            [enable_fapi=$enableval],
            [enable_fapi=yes])

AM_CONDITIONAL(FAPI, test "x$enable_fapi" = "xyes")


AC_ARG_ENABLE([fapi-async-tests],
    AS_HELP_STRING([--enable-fapi-async-tests],
               [Force fapi to spin asynchronously. (NOT FOR PRODUCTION!)]),,
    [enable_fapi_async_tests=no])
AS_IF([test "x$enable_fapi_async_tests" = "xyes"],
    [AC_DEFINE([TEST_FAPI_ASYNC], [1], [FAPI forced async spinning])])
AS_IF([test "x$enable_fapi_async_tests" = "xyes"],
    [AC_MSG_WARN("FAPI compiled with asynchronous spinning testing. NOT FOR PRODUCTION!")])

AC_ARG_ENABLE([policy],
            [AS_HELP_STRING([--enable-policy],
                            [build the tss2-policy library (default is yes)])],
            [enable_policy=$enableval],
            [enable_policy=yes])

AM_CONDITIONAL(POLICY, test "x$enable_policy" = "xyes")

AC_ARG_WITH([crypto],
            [AS_HELP_STRING([--with-crypto={ossl,mbed,none}],
                            [sets the ESYS crypto backend (default is OpenSSL)])],,
            [with_crypto=ossl])

AM_CONDITIONAL(ESYS_OSSL, test "x$with_crypto" = "xossl")
AM_CONDITIONAL(ESYS_MBED, test "x$with_crypto" = "xmbed")

AC_ARG_ENABLE([vendor],
            [AS_HELP_STRING([--enable-vendor],
                            [build vendor specific extensions (default is yes)])],
            [enable_vendor=$enableval],
            [enable_vendor=yes])

AM_CONDITIONAL(VENDOR, test "x$enable_vendor" = "xyes")
# Negative logic since code by default should build with vendor extensions
# we don't want to require folks to have to pass a define to enable vendor
# extensions in the header files, only to remove them.
AS_IF([test "x$enable_vendor" != "xyes"],
    [AC_DEFINE([DISABLE_VENDOR], [1], [Disable Vendor Extensions])])


m4_define([ossl_min_version], [1.1.0])
m4_define([ossl_err], [OpenSSL libcrypto is missing or version requirements not met. OpenSSL version must be >= ossl_min_version])
AS_IF([test "x$enable_esys" = xyes],
      [AS_IF([test "x$with_crypto" = xossl], [
           PKG_CHECK_MODULES([CRYPTO],
                             [libcrypto >= ossl_min_version],,
                             [AC_MSG_ERROR([ossl_err])])
           AC_DEFINE([OSSL], [1], [OpenSSL cryptographic backend])
           AC_CHECK_LIB(crypto,[EVP_sm3], [
               AC_DEFINE([HAVE_EVP_SM3], [1], [Support EVP_sm3 in openssl])],
                [])
           TSS2_ESYS_CFLAGS_CRYPTO="$CRYPTO_CFLAGS"
           TSS2_ESYS_LDFLAGS_CRYPTO="$CRYPTO_LIBS"
       ], [test "x$with_crypto" = xmbed], [
           AC_CHECK_HEADER(mbedtls/md.h, [], [AC_MSG_ERROR([Missing required mbedTLS library])])
           AC_DEFINE([MBED], [1], [mbedTLS cryptographic backend])
           TSS2_ESYS_CFLAGS_CRYPTO="$LIBMBED_CFLAGS"
           TSS2_ESYS_LDFLAGS_CRYPTO="-lmbedcrypto"
       ], [test "x$with_crypto" = xnone], [
           AC_MSG_NOTICE([No crypto backend selected! Users must set crypto functions!])
       ], [AC_MSG_ERROR([Bad value for --with-crypto $with_crypto])])])
AC_SUBST([TSS2_ESYS_CFLAGS_CRYPTO])
AC_SUBST([TSS2_ESYS_LDFLAGS_CRYPTO])

AS_IF([test "x$enable_fapi" != xno && test "x$enable_esys" = "xno"],
    [AC_MSG_ERROR([ESYS has to be enabled to compile FAPI.])])

AS_IF([test "x$enable_fapi" != xno && test "x$with_crypto" != "xossl"],
    [AC_MSG_ERROR([FAPI has to be compiled with OpenSSL])])

AS_IF([test "x$enable_policy" != xno && test "x$with_crypto" != "xossl"],
    [AC_MSG_ERROR([libpolicy has to be compiled with OpenSSL])])

AS_IF([test "x$enable_fapi" = xyes -o "x$enable_policy" = xyes ],
      [PKG_CHECK_MODULES([JSONC], [json-c])])

AS_IF([test "x$enable_fapi" = xyes ],
      [PKG_CHECK_MODULES([CURL], [libcurl])])
AC_CHECK_LIB([curl], [curl_url_strerror], [AC_DEFINE([HAVE_CURL_URL_STRERROR],[1], [If lib curl has curl_url_strerror function])])

AS_IF([test "x$enable_fapi" = xyes -o "x$enable_policy" = xyes ],
      [PKG_CHECK_MODULES([UUID], [uuid])])

AC_ARG_WITH([tctidefaultmodule],
            [AS_HELP_STRING([--with-tctidefaultmodule],
[The default TCTI module for ESYS. (Default: libtss2-tcti-default.so)])],
            [AC_DEFINE_UNQUOTED([ESYS_TCTI_DEFAULT_MODULE],
                                ["$with_tctidefaultmodule"],
                                ["The default TCTI library file"])],
	    [with_tctidefaultmodule=libtss2-tcti-default.so])

AC_ARG_WITH([tctidefaultconfig],
            [AS_HELP_STRING([--with-tctidefaultconfig],
                            [The default tcti module's configuration.])],
            [AC_DEFINE_UNQUOTED([ESYS_TCTI_DEFAULT_CONFIG],
                                ["$with_tctidefaultconfig"],
                                ["The default TCTIs configuration string"])])

AC_ARG_ENABLE([tcti-device],
            [AS_HELP_STRING([--disable-tcti-device],
                            [don't build the tcti-device module])],,
            [enable_tcti_device=yes])
AM_CONDITIONAL([ENABLE_TCTI_DEVICE], [test "x$enable_tcti_device" != xno])
AS_IF([test "x$enable_tcti_device" = "xyes"],
	[AC_DEFINE([TCTI_DEVICE],[1], [TCTI FOR DEV TPM])])

AC_ARG_ENABLE([tcti-mssim],
            [AS_HELP_STRING([--disable-tcti-mssim],
                            [don't build the tcti-mssim module])],,
            [enable_tcti_mssim=yes])
AM_CONDITIONAL([ENABLE_TCTI_MSSIM], [test "x$enable_tcti_mssim" != xno])
AS_IF([test "x$enable_tcti_mssim" = "xyes"],
	[AC_DEFINE([TCTI_MSSIM],[1], [TCTI FOR MS SIMULATOR])])

AC_ARG_ENABLE([tcti-swtpm],
            [AS_HELP_STRING([--disable-tcti-swtpm],
                            [don't build the tcti-swtpm module])],,
            [enable_tcti_swtpm=yes])
AM_CONDITIONAL([ENABLE_TCTI_SWTPM], [test "x$enable_tcti_swtpm" != xno])
AS_IF([test "x$enable_tcti_swtpm" = "xyes"], [AC_DEFINE([TCTI_SWTPM],[1], [TCTI FOR SWTPM])])

AC_ARG_ENABLE([tcti-pcap],
            [AS_HELP_STRING([--disable-tcti-pcap],
                            [don't build the tcti-pcap module])],,
            [enable_tcti_pcap=yes])
AM_CONDITIONAL([ENABLE_TCTI_PCAP], [test "x$enable_tcti_pcap" != xno])

AC_ARG_ENABLE([tcti-libtpms],
            [AS_HELP_STRING([--disable-tcti-libtpms],
                            [don't build the tcti-libtpms module])],
            [AS_IF([test "x$enable_tcti_libtpms" = "xyes"],
                   [AC_CHECK_HEADER(libtpms/tpm_library.h, [], [AC_MSG_ERROR([library libtpms missing])])])],
            [AC_CHECK_HEADER(libtpms/tpm_library.h, [enable_tcti_libtpms=yes],
                                                    [enable_tcti_libtpms=no]
                                                    [AC_MSG_WARN([library libtpms missing])])])
AM_CONDITIONAL([ENABLE_TCTI_LIBTPMS], [test "x$enable_tcti_libtpms" != xno])

AC_ARG_ENABLE([tcti-cmd],
            [AS_HELP_STRING([--disable-tcti-cmd],
                            [don't build the tcti-cmd module])],,
            [enable_tcti_cmd=yes])

AM_CONDITIONAL([ENABLE_TCTI_CMD], [test "x$enable_tcti_cmd" != xno])
AS_IF([test "x$enable_tcti_cmd" = "xyes"],
	[AC_DEFINE([TCTI_CMD],[1], [TCTI FOR COMMAND BASED ACCESS TO TPM2 DEVICE])])

AC_ARG_ENABLE([tcti-spi-helper],
            [AS_HELP_STRING([--disable-tcti-spi-helper],
                            [don't build the tcti-spi-helper module])],,
            [enable_tcti_spi_helper=yes])

AM_CONDITIONAL([ENABLE_TCTI_SPI_HELPER], [test "x$enable_tcti_spi_helper" != xno])
AS_IF([test "x$enable_tcti_spi_helper" = "xyes"],
	[AC_DEFINE([TCTI_SPI_HELPER],[1], [TCTI HELPER FOR SPI BASED ACCESS TO TPM2 DEVICE])])

AC_ARG_ENABLE([tcti-fuzzing],
            [AS_HELP_STRING([--enable-tcti-fuzzing],
                            [build the tcti-fuzzing module])],,
            [enable_tcti_fuzzing=no])
AM_CONDITIONAL([ENABLE_TCTI_FUZZING], [test "x$enable_tcti_fuzzing" != xno])
AS_IF([test "x$enable_tcti_fuzzing" = "xyes"],
	[AC_DEFINE([TCTI_FUZZING],[1], [TCTI FOR FUZZING])])

AC_ARG_ENABLE([nodl],
              [AS_HELP_STRING([--enable-nodl],
                              [link against TCTIs directly, do not use dlopen])],
              [],
              [enable_nodl=no])
AM_CONDITIONAL([NO_DL], [test "x$enable_nodl" = "xyes"])
AS_IF([test "x$enable_nodl" = "xyes"],
      [AC_DEFINE([NO_DL],[1], [disable use of dlopen])])

#
# udev
#
AC_ARG_WITH([udevrulesdir],
            [AS_HELP_STRING([--with-udevrulesdir=DIR],[udev rules directory])],,
            [with_udevrulesdir=${libdir}/udev/rules.d])
AX_NORMALIZE_PATH([with_udevrulesdir])
AC_SUBST([udevrulesdir], [$with_udevrulesdir])
AC_ARG_WITH([udevrulesprefix],
            [AS_HELP_STRING([--with-udevrulesprefix=XY],[prefix for udev rules file])],
            [AC_SUBST([udevrulesprefix],[$with_udevrulesprefix])])
AM_CONDITIONAL(WITH_UDEVRULESPREFIX, [test -n "$with_udevrulesprefix"])

dnl ---------  Physical TPM device for testing -----------------------

AC_ARG_WITH([device],
            [AS_HELP_STRING([--with-device=<device>],[TPM device for testing])],
            [AS_IF([test -w "$with_device" && test -r "$with_device"],
                   [AC_MSG_RESULT([success])
                    AX_NORMALIZE_PATH([with_device])
                    with_device_set=yes],
                   [AC_MSG_ERROR([TPM device provided does not exist or is not writable])])],
            [with_device_set=no])
AM_CONDITIONAL([TESTDEVICE],[test "x$with_device_set" = xyes])

AC_ARG_WITH([devicetests],
            [AS_HELP_STRING([--with-devicetests=<case>],[Comma-separated values of possible tests: destructive,mandatory,optional] default is mandatory)],
            [AS_IF([test "x" =  x$(echo $with_devicetests | sed 's/destructive//g'  | sed 's/mandatory//g'  | sed 's/optional//g' | sed 's/,//g') ],
                   [AC_MSG_RESULT([success])
                    with_devicetests_set=yes],
                   [AC_MSG_ERROR([Illegal test type for device tests.])])],
            [with_devicetests="mandatory"])

if echo $with_devicetests | grep destructive > /dev/null; then
    enable_device_destructive="yes"
fi
AM_CONDITIONAL([DEVICEDESTRUCTIVE],[test "x$enable_device_destructive" = "xyes"])

if echo $with_devicetests | grep optional > /dev/null; then
    enable_device_optional="yes"
fi
AM_CONDITIONAL([DEVICEOPTIONAL],[test "x$enable_device_optional" = "xyes"])

if echo $with_devicetests | grep mandatory > /dev/null; then
    enable_device_mandatory="yes"
fi
AM_CONDITIONAL([DEVICEMANDATORY],[test "x$enable_device_mandatory" = "xyes"])

#
# enable integration tests and check for simulator binary
#
AC_ARG_ENABLE([integration],
    [AS_HELP_STRING([--enable-integration],
        [build and execute integration tests])],,
    [enable_integration=no])
AS_IF([test "x$enable_integration" = "xyes"],
     [AS_IF([test "$HOSTOS" = "Linux"],
           [ERROR_IF_NO_PROG([ss])],
           [ERROR_IF_NO_PROG([sockstat])])
       ERROR_IF_NO_PROG([echo])
       ERROR_IF_NO_PROG([kill])
       ERROR_IF_NO_PROG([stdbuf])
       ERROR_IF_NO_PROG([sleep])
       ERROR_IF_NO_PROG([cat])
       ERROR_IF_NO_PROG([realpath])
       ERROR_IF_NO_PROG([dirname])
       ERROR_IF_NO_PROG([basename])
       ERROR_IF_NO_PROG([mktemp])
       ERROR_IF_NO_PROG([od])
       ERROR_IF_NO_PROG([awk])
       ERROR_IF_NO_PROG([expr])
       ERROR_IF_NO_PROG([grep])
       ERROR_IF_NO_PROG([env])
       ERROR_IF_NO_PROG([rm])
       AS_IF([test "x$with_crypto" != xossl || test "x$enable_esys" != xyes],
           [PKG_CHECK_MODULES([CRYPTO],[libcrypto])])
       AC_CHECK_HEADER(uthash.h, [], [AC_MSG_ERROR([Can not find uthash.h. Please install uthash-dev])])

       # choose tcti for testing and look for TPM simulator binary
       integration_tcti="none"
       integration_args=""
       AS_IF([test "x$with_device_set" = xyes],
             [# use device if --with-device was passed
              integration_tcti=device
              integration_args="--device=$with_device"
              AC_MSG_WARN([Using physical TPM for integration testing])])
       AS_IF([test "x$integration_tcti" = "xnone" && test "x$enable_tcti_swtpm" != xyes && test "x$enable_tcti_mssim" != xyes],
             [AC_MSG_ERROR([No suitable TCTI for testing enabled. Please use option --enable-tcti-swtpm (recommended) or --enable-tcti-mssim (fallback) to enable a suitable TCTI or disable testing with --disable-integration.])])
       AS_IF([test "x$integration_tcti" = "xnone" && test "x$enable_tcti_swtpm" = "xyes"],
             [# check for swtpm binary
              AC_CHECK_PROG([result_swtpm], [swtpm], [yes], [no])
              AS_IF([test "x$result_swtpm" = "xyes"],
                    [integration_tcti=swtpm],
                    [AC_MSG_WARN([Executable swtpm not found in PATH.])])])
       AS_IF([test "x$integration_tcti" = "xnone" && test "x$enable_tcti_mssim" = "xyes"],
             [# check for mssim binary
              AC_MSG_NOTICE([Falling back to testing with tcti-mssim.])
              AC_CHECK_PROG([result_tpm_server], [tpm_server], [yes], [no])
              AS_IF([test "x$result_tpm_server" = "xyes"],
                    [integration_tcti=mssim
                     AC_DEFINE([INTEGRATION_TCTI_MSSIM], [1], [use mssim TCTI for integration tests])],
                    [AC_MSG_WARN([Executable tpm_server not found in PATH (fallback)])])])
       AS_IF([test "x$integration_tcti" = "xnone"],
             [AC_MSG_ERROR([No simulator executable found in PATH for testing TCTI.])])
       AC_SUBST([INTEGRATION_TCTI], [$integration_tcti])
       AC_SUBST([INTEGRATION_ARGS], [$integration_args])
       AC_SUBST([ENABLE_INTEGRATION], [$enable_integration])])
AM_CONDITIONAL([ENABLE_INTEGRATION],[test "x$enable_integration" = "xyes"])
#
# sanitizer compiler flags
#
AC_ARG_WITH([sanitizer],
            [AS_HELP_STRING([--with-sanitizer={none,address,undefined}],
                            [build with the given sanitizer])],,
            [with_sanitizer=none])
AS_CASE(["x$with_sanitizer"],
        ["xnone"],
        [],
        ["xaddress"],
        [
            SANITIZER_CFLAGS="-fsanitize=address -fno-omit-frame-pointer"
            SANITIZER_LDFLAGS="-lasan"
        ],
        ["xundefined"],
        [
            SANITIZER_CFLAGS="-fsanitize=undefined"
            SANITIZER_LDFLAGS="-lubsan"
        ],
        ["xundefined,address"],
        [
            SANITIZER_CFLAGS="-fsanitize=undefined,address -fno-omit-frame-pointer"
            SANITIZER_LDFLAGS="-lasan -lubsan"
        ],
        [AC_MSG_ERROR([Bad value for --with-sanitizer])])
AC_SUBST([SANITIZER_CFLAGS])
AC_SUBST([SANITIZER_LDFLAGS])
#
# fuzz testing
#
AC_ARG_WITH([fuzzing],
            [AS_HELP_STRING([--with-fuzzing={none,libfuzzer,ossfuzz}],
                            [fuzzing to build with (default is none)])],,
            [with_fuzzing=none])
AS_CASE(["x$with_fuzzing"],
        ["xnone"],
        [],
        ["xlibfuzzer"],
        [ADD_FUZZING_FLAG([-fsanitize=fuzzer])],
        ["xossfuzz"],
        [AS_IF([test "x$LIB_FUZZING_ENGINE" = "x"],
               [AC_MSG_ERROR([OSS Fuzz testing requires LIB_FUZZING_ENGINE environment variable be set])])
         ADD_FUZZING_FLAG([-lFuzzingEngine])],
        [AC_MSG_ERROR([Bad value for --with-fuzzing])])
AM_CONDITIONAL([ENABLE_FUZZING],[test "x$with_fuzzing" != "xnone"])
AS_IF([test "x$with_fuzzing" != "xnone"],
      [AS_IF([test "x$enable_tcti_fuzzing" = xno],
             [AC_MSG_ERROR([Fuzz tests can not be enabled without the TCTI_FUZZING module])])
       AS_IF([test "x$GEN_FUZZ" != "x1"],
             [AC_MSG_ERROR([Fuzz tests can not be enabled without "GEN_FUZZ=1" variable])])])

AX_VALGRIND_CHECK

gl_LD_VERSION_SCRIPT

AC_ARG_ENABLE([log-file],
            [AS_HELP_STRING([--disable-log-file],
                            [write logging to stderr only])],,
            [enable_log_file=yes])
AS_IF([test "x$enable_log_file" != xno],
	[AC_DEFINE([LOG_FILE_ENABLED],[1], [Support for writing to a log file is enabled])])

AC_ARG_WITH([maxloglevel],
            [AS_HELP_STRING([--with-maxloglevel={none,error,warning,info,debug,trace}],
                            [sets the maximum log level (default is trace)])],,
            [with_maxloglevel=trace])
AS_CASE(["x$with_maxloglevel"],
        ["xnone"],
        [AC_DEFINE_UNQUOTED([MAXLOGLEVEL], [0], ["Logging disabled"])],
        ["xerror"],
        [AC_DEFINE_UNQUOTED([MAXLOGLEVEL], [2], ["Error log level"])],
        ["xwarning"],
        [AC_DEFINE_UNQUOTED([MAXLOGLEVEL], [3], ["Warning log level"])],
        ["xinfo"],
        [AC_DEFINE_UNQUOTED([MAXLOGLEVEL], [4], ["Info log level"])],
        ["xdebug"],
        [AC_DEFINE_UNQUOTED([MAXLOGLEVEL], [5], ["Debug log level"])],
        ["xtrace"],
        [AC_DEFINE_UNQUOTED([MAXLOGLEVEL], [6], ["Trace log level"])],
        [AC_MSG_ERROR([Bad value for --with-maxloglevel])])

AC_ARG_ENABLE([defaultflags],
              [AS_HELP_STRING([--disable-defaultflags],
                              [Disable default preprocessor, compiler, and linker flags.])],,
              [enable_defaultflags=yes])
AS_IF([test "x$enable_defaultflags" = "xyes"],
      [
      AS_IF([test "x$enable_debug" = "xno"],
            [ADD_COMPILER_FLAG([-O2])
             AX_ADD_FORTIFY_SOURCE])
      ADD_COMPILER_FLAG([-std=c99])
      ADD_COMPILER_FLAG([-Wall])
      ADD_COMPILER_FLAG([-Wextra])
      ADD_COMPILER_FLAG([-Wformat-security])
      AS_IF([test "x$ax_is_release" = "xno"],
          [ADD_COMPILER_FLAG([-Werror])])
      ADD_COMPILER_FLAG([-fstack-protector-all])
      ADD_COMPILER_FLAG([-fpic])
      ADD_COMPILER_FLAG([-fPIC])
      # work around GCC bug #53119
      #   https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53119
      ADD_COMPILER_FLAG([-Wno-missing-braces])
      ADD_COMPILER_FLAG([-Wstrict-overflow=5])
      ADD_LINK_FLAG([-Wl,--no-undefined])
      ADD_LINK_FLAG([-Wl,-z,noexecstack])
      ADD_LINK_FLAG([-Wl,-z,now])
      ADD_LINK_FLAG([-Wl,-z,relro])
      ])

AC_ARG_ENABLE([weakcrypto],
    [AS_HELP_STRING([--disable-weakcrypto],
	           [Disable crypto algorithms considered weak])],,
    [enable_weakcrypto=no])
AS_IF([test "x$enable_weakcrypto" = "xyes"],
	[AC_DEFINE([DISABLE_WEAK_CRYPTO],[1],[DISABLE WEAK CRYPTO ALGORITHMS])])

AC_ARG_ENABLE([self-generated-certificate],
            [AS_HELP_STRING([--enable-self-generated-certificate],
                            [Alllow usage of self generated root certifcate])],,
            [enable_self_generated_certificate=no])
AS_IF([test "x$enable_self_generated_certificate" = xyes],
	[AC_DEFINE([SELF_GENERATED_CERTIFICATE], [1], [Allow usage of self generated root certificate])],
	[AS_IF([test "x$integration_tcti" != "xdevice"], [AC_DEFINE([FAPI_TEST_EK_CERT_LESS], [1], [Perform integration tests without EK certificate verification])])])

AS_IF([test "x$enable_integration" = "xyes" && test "x$enable_self_generated_certificate" != "xyes" && test "x$integration_tcti" != "xdevice"],
      [AC_MSG_WARN([Running integration tests without EK certificate verification, use --enable-self-generated-certificate for full test coverage])])

# Check for systemd helper tools used by make install
AC_CHECK_PROG(systemd_sysusers, systemd-sysusers, yes)
AM_CONDITIONAL(SYSD_SYSUSERS, test "x$systemd_sysusers" = "xyes")
AC_CHECK_PROG(systemd_tmpfiles, systemd-tmpfiles, yes)
AM_CONDITIONAL(SYSD_TMPFILES, test "x$systemd_tmpfiles" = "xyes")

# Check all tools used by make install
AS_IF([test "$HOSTOS" = "Linux" && test "x$systemd_sysusers" != "xyes"],
    [ AC_CHECK_PROG(useradd, useradd, yes)
      AC_CHECK_PROG(groupadd, groupadd, yes)
      AC_CHECK_PROG(adduser, adduser, yes)
      AC_CHECK_PROG(addgroup, addgroup, yes)
      AS_IF([test "x$addgroup" != "xyes" && test "x$groupadd" != "xyes" ],
         [AC_MSG_ERROR([addgroup or groupadd are needed.])])
      AS_IF([test "x$adduser" != "xyes" && test "x$useradd" != "xyes" ],
         [AC_MSG_ERROR([adduser or useradd are needed.])])])

AC_SUBST([PATH])

dnl --------- Doxy Gen -----------------------
DX_DOXYGEN_FEATURE(ON)
DX_DOT_FEATURE(OFF)
DX_HTML_FEATURE(ON)
DX_CHM_FEATURE(OFF)
DX_CHI_FEATURE(OFF)
DX_MAN_FEATURE(ON)
DX_RTF_FEATURE(ON)
DX_XML_FEATURE(OFF)
DX_PDF_FEATURE(OFF)
DX_PS_FEATURE(OFF)
DX_INIT_DOXYGEN($PACKAGE_NAME, [Doxyfile], [doxygen-doc])

AM_CONDITIONAL(DOXYMAN, [test $DX_FLAG_doc -eq 1])
AS_IF([test $DX_FLAG_doc -ne 1],
	[AS_IF([test "x$enable_doxygen_doc" = xyes],
                     [ERROR_IF_NO_PROG([doxygen])])])

AX_CODE_COVERAGE
m4_ifdef([_AX_CODE_COVERAGE_RULES],
         [AM_CONDITIONAL(AUTOCONF_CODE_COVERAGE_2019_01_06, [true])],
         [AM_CONDITIONAL(AUTOCONF_CODE_COVERAGE_2019_01_06, [false])])
AX_ADD_AM_MACRO_STATIC([])

AM_COND_IF([ENABLE_TCTI_DEVICE], [],
           [AM_COND_IF([ENABLE_TCTI_MSSIM], [],
                       [AM_COND_IF([ENABLE_TCTI_SWTPM], [],
                                   [AM_COND_IF([ENABLE_TCTI_FUZZING], [],
                                               [AC_MSG_WARN("No build-in TCTI module enabled")])])])])

AM_COND_IF([ENABLE_TCTI_FUZZING], [
            AM_COND_IF([ENABLE_TCTI_DEVICE],
                       AC_MSG_ERROR([Fuzzing TCTI is meant to be built as the only TCTI: use --disable-tcti-device --disable-tcti-mssim --disable-tcti-swtpm]))
            AM_COND_IF([ENABLE_TCTI_MSSIM],
                       AC_MSG_ERROR([Fuzzing TCTI is meant to be built as the only TCTI: use --disable-tcti-device --disable-tcti-mssim --disable-tcti-swtpm]))
            AM_COND_IF([ENABLE_TCTI_SWTPM],
                       AC_MSG_ERROR([Fuzzing TCTI is meant to be built as the only TCTI: use --disable-tcti-device --disable-tcti-mssim --disable-tcti-swtpm]))
            AS_CASE([$CC],
                    [*clang*], [AC_MSG_NOTICE("Building fuzzing tests with $CC")],
                    [AC_MSG_ERROR("Fuzzing TCTI can only be used with clang")])
            ], [])

AC_ARG_WITH([default-test-fapi-profile],
            [AS_HELP_STRING([--with-default-test-fapi-profile=PROFILE],
                            [sets the default FAPI profile used in tests])],,
            [with_default_test_fapi_profile=P_ECC])
AC_DEFINE_UNQUOTED([DEFAULT_TEST_FAPI_PROFILE], ["$with_default_test_fapi_profile"], [Default FAPI profile used for testing])

AC_OUTPUT

AC_MSG_RESULT([
    $PACKAGE_NAME $VERSION
    esys:               $enable_esys
    fapi:               $enable_fapi
    policy:             $enable_policy
    tctidefaultmodule:  $with_tctidefaultmodule
    tctidefaultconfig:  $with_tctidefaultconfig
    unit:               $enable_unit
    integration:        $enable_integration
    testing backend:    $integration_tcti
    fapi test profile:  $with_default_test_fapi_profile
    fuzzing:            $with_fuzzing
    debug:              $enable_debug
    maxloglevel:        $with_maxloglevel
    doxygen:            $DX_FLAG_doc $enable_doxygen_doc
    crypto backend:     $with_crypto
    sysconfdir:         $sysconfdir
    localstatedir:      $localstatedir
    runstatedir:        $runstatedir
    sysusersdir:        $sysusersdir
    tmpfilesdir:        $tmpfilesdir
    userstatedir:       [\$HOME/]$with_userstatedir
    sysmeasurements:    $sysmeasurements
    imameasurements:    $imameasurements
])
