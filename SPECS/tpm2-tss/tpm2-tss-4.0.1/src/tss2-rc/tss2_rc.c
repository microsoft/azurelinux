/* SPDX-License-Identifier: BSD-2-Clause */
#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include <assert.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#include "tss2_rc.h"
#include "tss2_sys.h"
#include "util/aux_util.h"

/**
 * The maximum size of a layer name.
 */
#define TSS2_ERR_LAYER_NAME_MAX  (16 + 1)

/**
 * The maximum size for layer specific error strings.
 */
#define TSS2_ERR_LAYER_ERROR_STR_MAX  512

/**
 * Concatenates (safely) onto a static buffer given a format and varaidic
 * arguments similar to sprintf.
 * @param b
 *   The static buffer to concatenate onto.
 * @param fmt
 *   The format specifier as understood by printf followed by the variadic
 *   parameters for the specifier.
 */
#define catbuf(b, fmt, ...) _catbuf(b, sizeof(b), fmt, ##__VA_ARGS__)

/**
 * Clears out a static buffer by setting index 0 to the null byte.
 * @param buffer
 *  The buffer to clear out.
 */
static void
clearbuf(char *buffer)
{
    buffer[0] = '\0';
}

/**
 * Prints to a buffer using snprintf(3) using the supplied fmt
 * and varaiadic arguments.
 * @param buf
 *  The buffer to print into.
 * @param len
 *  The length of that buffer.
 * @param fmt
 *  The format string
 * @warning
 *  DO NOT CALL DIRECTLY, use the catbuf() macro.
 */
static void COMPILER_ATTR(format (printf, 3, 4))
_catbuf(char *buf, size_t len, const char *fmt, ...)
{
    va_list argptr;
    va_start(argptr, fmt);
    size_t offset = strlen(buf);
    vsnprintf(&buf[offset], len - offset, fmt, argptr);
    va_end(argptr);
}

/**
 * Number of error layers
 */
#define TPM2_ERROR_TSS2_RC_LAYER_COUNT (TSS2_RC_LAYER_MASK >> TSS2_RC_LAYER_SHIFT)

/**
 * Mask for the error bits of tpm2 compliant return code.
 */
#define TPM2_ERROR_TSS2_RC_ERROR_MASK 0xFFFF

/**
 * Retrieves the error bits from a TSS2_RC. The error bits are
 * contained in the first 2 octets.
 * @param rc
 *  The rc to query for the error bits.
 * @return
 *  The error bits.
 */
static inline UINT16
tpm2_error_get(TSS2_RC rc)
{
    return ((rc & TPM2_ERROR_TSS2_RC_ERROR_MASK));
}

/**
 * Retrieves the layer number. The layer number is in the 3rd
 * octet and is thus 1 byte big.
 *
 * @param rc
 *  The rc to query for the layer number.
 * @return
 *  The layer number.
 */
static inline UINT8
tss2_rc_layer_number_get(TSS2_RC rc)
{
    return ((rc & TSS2_RC_LAYER_MASK) >> TSS2_RC_LAYER_SHIFT);
}

/**
 * Queries a TPM format 1 error codes N field. The N field
 * is a 4 bit field located at bits 8:12.
 * @param rc
 *  The rc to query the N field for.
 * @return
 *  The N field value.
 */
static inline UINT8
tpm2_rc_fmt1_N_get(TPM2_RC rc)
{
    return ((rc & (0xF << 8)) >> 8);
}

/**
 * Queries the index bits out of the N field contained in a TPM format 1
 * error code. The index bits are the low 3 bits of the N field.
 * @param rc
 *  The TPM format 1 error code to query for the index bits.
 * @return
 *  The index bits from the N field.
 */
static inline UINT8
tpm2_rc_fmt1_N_index_get(TPM2_RC rc)
{
    return (tpm2_rc_fmt1_N_get(rc) & 0x7);
}

/**
 * Determines if the N field in a TPM format 1 error code is
 * a handle or not.
 * @param rc
 *  The TPM format 1 error code to query.
 * @return
 *  True if it is a handle, false otherwise.
 */
static inline bool
tpm2_rc_fmt1_N_is_handle(TPM2_RC rc)
{
    return ((tpm2_rc_fmt1_N_get(rc) & 0x8) == 0);
}

static inline UINT8
tpm2_rc_fmt1_P_get(TPM2_RC rc)
{
    return ((rc & (1 << 6)) >> 6);
}

static inline UINT8
tpm2_rc_fmt1_error_get(TPM2_RC rc)
{
    return (rc & 0x3F);
}

static inline UINT8
tpm2_rc_fmt0_error_get(TPM2_RC rc)
{
    return (rc & 0x7F);
}

static inline UINT8
tpm2_rc_tpm_fmt0_V_get(TPM2_RC rc)
{
    return ((rc & (1 << 8)) >> 8);
}

static inline UINT8
tpm2_rc_fmt0_T_get(TPM2_RC rc)
{
    return ((rc & (1 << 10)) >> 8);
}

static inline UINT8
tpm2_rc_fmt0_S_get(TSS2_RC rc)
{
    return ((rc & (1 << 11)) >> 8);
}

/**
 * Helper macro for adding a layer handler to the layer
 * registration array.
 */
#define ADD_HANDLER(name, handler) \
    { name, handler }

/**
 * Same as ADD_HANDLER but sets it to NULL. Used as a placeholder
 * for non-registered indexes into the handler array.
 */
#define ADD_NULL_HANDLER ADD_HANDLER("\0", NULL)

const char *
tss2_fmt1_err_strs_get(TSS2_RC error)
{
    /*
     * format 1 error codes start at 1, so
     * add a NULL entry to index 0.
     */
    static const char *fmt1_err_strs[] = {
        /* 0x0 - EMPTY */
        NULL,
        /* 0x1 - TPM2_RC_ASYMMETRIC */
        "asymmetric algorithm not supported or not correct",
        /* 0x2 - TPM2_RC_ATTRIBUTES */
        "inconsistent attributes",
        /* 0x3 - TPM2_RC_HASH */
        "hash algorithm not supported or not appropriate",
        /* 0x4 - TPM2_RC_VALUE */
        "value is out of range or is not correct for the context",
        /* 0x5 - TPM2_RC_HIERARCHY */
        "hierarchy is not enabled or is not correct for the use",
        /* 0x6 - EMPTY */
        NULL,
        /* 0x7 - TPM2_RC_KEY_SIZE */
        "key size is not supported",
        /* 0x8 - TPM2_RC_MGF */
        "mask generation function not supported",
        /* 0x9 - TPM2_RC_MODE */
        "mode of operation not supported",
        /* 0xA - TPM2_RC_TYPE */
        "the type of the value is not appropriate for the use",
        /* 0xB - TPM2_RC_HANDLE */
        "the handle is not correct for the use",
        /* 0xC - TPM2_RC_KDF */
        "unsupported key derivation function or function not appropriate for "
        "use",
        /* 0xD - TPM2_RC_RANGE */
        "value was out of allowed range",
        /* 0xE - TPM2_RC_AUTH_FAIL */
        "the authorization HMAC check failed and DA counter incremented",
        /* 0xF - TPM2_RC_NONCE */
        "invalid nonce size or nonce value mismatch",
        /* 0x10 - TPM2_RC_PP */
        "authorization requires assertion of PP",
        /* 0x11 - EMPTY */
        NULL,
        /* 0x12 - TPM2_RC_SCHEME */
        "unsupported or incompatible scheme",
        /* 0x13 - EMPTY */
        NULL,
        /* 0x14 - EMPTY */
        NULL,
        /* 0x15 - TPM2_RC_SIZE */
        "structure is the wrong size",
        /* 0x16 - TPM2_RC_SYMMETRIC */
        "unsupported symmetric algorithm or key size or not appropriate for"
        " instance",
        /* 0x17 - TPM2_RC_TAG */
        "incorrect structure tag",
        /* 0x18 - TPM2_RC_SELECTOR */
        "union selector is incorrect",
        /* 0x19 - EMPTY */
        NULL,
        /* 0x1A - TPM2_RC_INSUFFICIENT */
        "the TPM was unable to unmarshal a value because there were not enough"
        " octets in the input buffer",
        /* 0x1B - TPM2_RC_SIGNATURE */
        "the signature is not valid",
        /* 0x1C - TPM2_RC_KEY */
        "key fields are not compatible with the selected use",
        /* 0x1D - TPM2_RC_POLICY_FAIL */
        "a policy check failed",
        /* 0x1E - EMPTY */
        NULL,
        /* 0x1F - TPM2_RC_INTEGRITY */
        "integrity check failed",
        /* 0x20 - TPM2_RC_TICKET */
        "invalid ticket",
        /* 0x21 - TPM2_RC_RESERVED_BITS */
        "reserved bits not set to zero as required",
        /* 0x22 - TPM2_RC_BAD_AUTH */
        "authorization failure without DA implications",
        /* 0x23 - TPM2_RC_EXPIRED */
        "the policy has expired",
        /* 0x24 - TPM2_RC_POLICY_CC */
        "the commandCode in the policy is not the commandCode of the command"
        " or the command code in a policy command references a command that"
        " is not implemented",
        /* 0x25 - TPM2_RC_BINDING */
        "public and sensitive portions of an object are not cryptographically bound",
        /* 0x26 - TPM2_RC_CURVE */
        "curve not supported",
        /* 0x27 - TPM2_RC_ECC_POINT */
        "point is not on the required curve",
    };

    if (error < ARRAY_LEN(fmt1_err_strs)) {
        return fmt1_err_strs[error];
    }

    return NULL;
}

const char *
tss2_fmt0_err_strs_get(TSS2_RC rc)
{
    /*
     * format 0 error codes start at 1, so
     * add a NULL entry to index 0.
     * Thus, no need to offset the error bits
     * and fmt0 and fmt1 arrays can be used
     * in-place of each other for lookups.
     */
    static const char *fmt0_warn_strs[] = {
            /* 0x0 - EMPTY */
            NULL,
            /* 0x1 - TPM2_RC_CONTEXT_GAP */
            "gap for context ID is too large",
            /* 0x2 - TPM2_RC_OBJECT_MEMORY */
            "out of memory for object contexts",
            /* 0x3 - TPM2_RC_SESSION_MEMORY */
            "out of memory for session contexts",
            /* 0x4 - TPM2_RC_MEMORY */
            "out of shared objectsession memory or need space for internal"
            " operations",
            /* 0x5 - TPM2_RC_SESSION_HANDLES */
            "out of session handles",
            /* 0x6 - TPM2_RC_OBJECT_HANDLES */
            "out of object handles",
            /* 0x7 - TPM2_RC_LOCALITY */
            "bad locality",
            /* 0x8 - TPM2_RC_YIELDED */
            "the TPM has suspended operation on the command forward progress"
            " was made and the command may be retried",
            /* 0x9 - TPM2_RC_CANCELED */
            "the command was canceled",
            /* 0xA - TPM2_RC_TESTING */
            "TPM is performing selftests",
            /* 0xB - EMPTY */
            NULL,
            /* 0xC - EMPTY */
            NULL,
            /* 0xD - EMPTY */
            NULL,
            /* 0xE - EMPTY */
            NULL,
            /* 0xF - EMPTY */
            NULL,
            /* 0x10 - TPM2_RC_REFERENCE_H0 */
            "the 1st handle in the handle area references a transient object"
            " or session that is not loaded",
            /* 0x11 - TPM2_RC_REFERENCE_H1 */
            "the 2nd handle in the handle area references a transient object"
            " or session that is not loaded",
            /* 0x12 - TPM2_RC_REFERENCE_H2 */
            "the 3rd handle in the handle area references a transient object"
            " or session that is not loaded",
            /* 0x13 - TPM2_RC_REFERENCE_H3 */
            "the 4th handle in the handle area references a transient object"
            " or session that is not loaded",
            /* 0x14 - TPM2_RC_REFERENCE_H4 */
            "the 5th handle in the handle area references a transient object"
            " or session that is not loaded",
            /* 0x15 - TPM2_RC_REFERENCE_H5 */
            "the 6th handle in the handle area references a transient object"
            " or session that is not loaded",
            /* 0x16 - TPM2_RC_REFERENCE_H6 */
            "the 7th handle in the handle area references a transient object"
            " or session that is not loaded",
            /* 0x17 - EMPTY, */
            NULL,
            /* 0x18 - TPM2_RC_REFERENCE_S0 */
            "the 1st authorization session handle references a session that"
            " is not loaded",
            /* 0x19 - TPM2_RC_REFERENCE_S1 */
            "the 2nd authorization session handle references a session that"
            " is not loaded",
            /* 0x1A - TPM2_RC_REFERENCE_S2 */
            "the 3rd authorization session handle references a session that"
            " is not loaded",
            /* 0x1B - TPM2_RC_REFERENCE_S3 */
            "the 4th authorization session handle references a session that"
            " is not loaded",
            /* 0x1C - TPM2_RC_REFERENCE_S4 */
            "the 5th session handle references a session that"
            " is not loaded",
            /* 0x1D - TPM2_RC_REFERENCE_S5 */
            "the 6th session handle references a session that"
            " is not loaded",
            /* 0x1E - TPM2_RC_REFERENCE_S6 */
            "the 7th authorization session handle references a session that"
            " is not loaded",
            /* 0x1F - EMPTY, */
            NULL,
            /* 0x20 -TPM2_RC_NV_RATE */
            "the TPM is rate limiting accesses to prevent wearout of NV",
            /* 0x21 - TPM2_RC_LOCKOUT */
            "authorizations for objects subject to DA protection are not"
            " allowed at this time because the TPM is in DA lockout mode",
            /* 0x22 - TPM2_RC_RETRY */
            "the TPM was not able to start the command",
            /* 0x23 - TPM2_RC_NV_UNAVAILABLE */
            "the command may require writing of NV and NV is not current"
            " accessible",
    };

    /*
     * format 1 error codes start at 0, so
     * no need to offset the error bits.
     */
    static const char *fmt0_err_strs[] = {
        /* 0x0 - TPM2_RC_INITIALIZE */
        "TPM not initialized by TPM2_Startup or already initialized",
        /* 0x1 - TPM2_RC_FAILURE */
        "commands not being accepted because of a TPM failure",
        /* 0x2 - EMPTY */
        NULL,
        /* 0x3 - TPM2_RC_SEQUENCE */
        "improper use of a sequence handle",
        /* 0x4 - EMPTY */
        NULL,
        /* 0x5 - EMPTY */
        NULL,
        /* 0x6 - EMPTY */
        NULL,
        /* 0x7 - EMPTY */
        NULL,
        /* 0x8 - EMPTY */
        NULL,
        /* 0x9 - EMPTY */
        NULL,
        /* 0xA - EMPTY */
        NULL,
        /* 0xB - TPM2_RC_PRIVATE */
        "not currently used",
        /* 0xC - EMPTY */
        NULL,
        /* 0xD - EMPTY */
        NULL,
        /* 0xE - EMPTY */
        NULL,
        /* 0xF - EMPTY */
        NULL,
        /* 0x10 - EMPTY */
        NULL,
        /* 0x11 - EMPTY */
        NULL,
        /* 0x12 - EMPTY */
        NULL,
        /* 0x13 - EMPTY */
        NULL,
        /* 0x14 - EMPTY */
        NULL,
        /* 0x15 - EMPTY */
        NULL,
        /* 0x16 - EMPTY */
        NULL,
        /* 0x17 - EMPTY */
        NULL,
        /* 0x18 - EMPTY */
        NULL,
        /* 0x19 - TPM2_RC_HMAC */
        "not currently used",
        /* 0x1A - EMPTY */
        NULL,
        /* 0x1B - EMPTY */
        NULL,
        /* 0x1C - EMPTY */
        NULL,
        /* 0x1D - EMPTY */
        NULL,
        /* 0x1E - EMPTY */
        NULL,
        /* 0x1F - EMPTY */
        NULL,
        /* 0x20 - TPM2_RC_DISABLED */
        "the command is disabled",
        /* 0x21 - TPM2_RC_EXCLUSIVE */
        "command failed because audit sequence required exclusivity",
        /* 0x22 - EMPTY */
        NULL,
        /* 0x23 - EMPTY, */
        NULL,
        /* 0x24 - TPM2_RC_AUTH_TYPE */
        "authorization handle is not correct for command",
        /* 0x25 - TPM2_RC_AUTH_MISSING */
        "command requires an authorization session for handle and it is"
        " not present",
        /* 0x26 - TPM2_RC_POLICY */
        "policy failure in math operation or an invalid authPolicy value",
        /* 0x27 - TPM2_RC_PCR */
        "PCR check fail",
        /* 0x28 - TPM2_RC_PCR_CHANGED */
        "PCR have changed since checked",
        /* 0x29 - EMPTY */
        NULL,
        /* 0x2A - EMPTY */
        NULL,
        /* 0x2B - EMPTY */
        NULL,
        /* 0x2C - EMPTY */
        NULL,
        /* 0x2D - TPM2_RC_UPGRADE */
        "For all commands, other than TPM2_FieldUpgradeData, "
        "this code indicates that the TPM is in field upgrade mode. "
        "For TPM2_FieldUpgradeData, this code indicates that the TPM "
        "is not in field upgrade mode",
        /* 0x2E - TPM2_RC_TOO_MANY_CONTEXTS */
        "context ID counter is at maximum",
        /* 0x2F - TPM2_RC_AUTH_UNAVAILABLE */
        "authValue or authPolicy is not available for selected entity",
        /* 0x30 - TPM2_RC_REBOOT */
        "a _TPM_Init and StartupCLEAR is required before the TPM can"
        " resume operation",
        /* 0x31 - TPM2_RC_UNBALANCED */
        "the protection algorithms hash and symmetric are not reasonably"
        " balanced. The digest size of the hash must be larger than the key"
        " size of the symmetric algorithm.",
        /* 0x32 - EMPTY */
        NULL,
        /* 0x33 - EMPTY */
        NULL,
        /* 0x34 - EMPTY */
        NULL,
        /* 0x35 - EMPTY */
        NULL,
        /* 0x36 - EMPTY */
        NULL,
        /* 0x37 - EMPTY */
        NULL,
        /* 0x38 - EMPTY */
        NULL,
        /* 0x39 - EMPTY */
        NULL,
        /* 0x3A - EMPTY */
        NULL,
        /* 0x3B - EMPTY */
        NULL,
        /* 0x3C - EMPTY */
        NULL,
        /* 0x3D - EMPTY */
        NULL,
        /* 0x3E - EMPTY */
        NULL,
        /* 0x3F - EMPTY */
        NULL,
        /* 0x40 - EMPTY */
        NULL,
        /* 0x41 - EMPTY */
        NULL,
        /* 0x42 - TPM2_RC_COMMAND_SIZE */
        "command commandSize value is inconsistent with contents of the"
        " command buffer. Either the size is not the same as the octets"
        " loaded by the hardware interface layer or the value is not large"
        " enough to hold a command header",
        /* 0x43 - TPM2_RC_COMMAND_CODE */
        "command code not supported",
        /* 0x44 - TPM2_RC_AUTHSIZE */
        "the value of authorizationSize is out of range or the number of"
        " octets in the Authorization Area is greater than required",
        /* 0x45 - TPM2_RC_AUTH_CONTEXT */
        "use of an authorization session with a context command or another"
        " command that cannot have an authorization session",
        /* 0x46 - TPM2_RC_NV_RANGE */
        "NV offset+size is out of range",
        /* 0x47 - TPM2_RC_NV_SIZE */
        "Requested allocation size is larger than allowed",
        /* 0x48 - TPM2_RC_NV_LOCKED */
        "NV access locked",
        /* 0x49 - TPM2_RC_NV_AUTHORIZATION */
        "NV access authorization fails in command actions",
        /* 0x4A - TPM2_RC_NV_UNINITIALIZED */
        "an NV Index is used before being initialized or the state saved"
        " by TPM2_ShutdownSTATE could not be restored",
        /* 0x4B - TPM2_RC_NV_SPACE */
        "insufficient space for NV allocation",
        /* 0x4C - TPM2_RC_NV_DEFINED */
        "NV Index or persistent object already defined",
        /* 0x4D - EMPTY */
        NULL,
        /* 0x4E - EMPTY */
        NULL,
        /* 0x4F - EMPTY */
        NULL,
        /* 0x50 - TPM2_RC_BAD_CONTEXT */
        "context in TPM2_ContextLoad is not valid",
        /* 0x51 - TPM2_RC_CPHASH */
        "cpHash value already set or not correct for use",
        /* 0x52 - TPM2_RC_PARENT */
        "handle for parent is not a valid parent",
        /* 0x53 - TPM2_RC_NEEDS_TEST */
        "some function needs testing",
        /* 0x54 - TPM2_RC_NO_RESULT */
        "returned when an internal function cannot process a request due to"
        " an unspecified problem. This code is usually related to invalid"
        " parameters that are not properly filtered by the input"
        " unmarshaling code",
        /* 0x55 - TPM2_RC_SENSITIVE */
        "the sensitive area did not unmarshal correctly after decryption",
    };

    UINT8 errnum = tpm2_rc_fmt0_error_get(rc);
    /* is it a warning (version 2 error string) or is it a 1.2 error? */
    size_t len = tpm2_rc_fmt0_S_get(rc) ? ARRAY_LEN(fmt0_warn_strs) : ARRAY_LEN(fmt0_err_strs);
    const char **selection = tpm2_rc_fmt0_S_get(rc) ? fmt0_warn_strs : fmt0_err_strs;
    if (errnum >= len) {
        return NULL;
    }

    return selection[errnum];
}

static const char *
tpm2_err_handler_fmt1(TPM2_RC rc)
{
    static __thread char buf[TSS2_ERR_LAYER_ERROR_STR_MAX + 1];

    clearbuf(buf);

    /* Print whether or not the error is caused by a bad
     * handle or parameter. On the case of a Handle (P == 0)
     * then the N field top bit will be set. Un-set this bit
     * to get the handle index by subtracting 8 as N is a 4
     * bit field.
     *
     * the lower 3 bits of N indicate index, and the high bit
     * indicates
     */
    UINT8 index = tpm2_rc_fmt1_N_index_get(rc);

    bool is_handle = tpm2_rc_fmt1_N_is_handle(rc);
    const char *m = tpm2_rc_fmt1_P_get(rc) ? "parameter" :
                    is_handle ? "handle" : "session";
    catbuf(buf, "%s", m);

    if (index) {
        catbuf(buf, "(%u):", index);
    } else {
        catbuf(buf, "%s", "(unk):");
    }

    UINT8 errnum = tpm2_rc_fmt1_error_get(rc);
    m = tss2_fmt1_err_strs_get(errnum);
    if (m) {
        catbuf(buf, "%s", m);
    } else {
        catbuf(buf, "unknown error num: 0x%X", errnum);
    }

    return buf;
}

static const char *
tpm2_err_handler_fmt0(TSS2_RC rc)
{
    static __thread char buf[TSS2_ERR_LAYER_ERROR_STR_MAX + 1];

    clearbuf(buf);

    char *e = tpm2_rc_fmt0_S_get(rc) ? "warn" : "error";
    char *v = tpm2_rc_tpm_fmt0_V_get(rc) ? "2.0" : "1.2";
    catbuf(buf, "%s(%s): ", e, v);

    UINT8 errnum = tpm2_rc_fmt0_error_get(rc);
    /* We only have version 2.0 spec codes defined */
    if (tpm2_rc_tpm_fmt0_V_get(rc)) {
        /* TCG specific error code */
        if (tpm2_rc_fmt0_T_get(rc)) {
            catbuf(buf, "Vendor specific error: 0x%X", errnum);
            return buf;
        }

        const char *m = tss2_fmt0_err_strs_get(rc);
        if (!m) {
            return NULL;
        }

        catbuf(buf, "%s", m);
        return buf;
    }

    catbuf(buf, "%s", "unknown version 1.2 error code");

    return buf;
}

/**
 * Retrieves the layer field from a TSS2_RC code.
 * @param rc
 *  The rc to query the layer index of.
 * @return
 *  The layer index.
 */
static inline UINT8
tss2_rc_layer_format_get(TSS2_RC rc)
{
    return ((rc & (1 << 7)) >> 7);
}

/**
 * Handler for tpm2 error codes. ie codes
 * coming from the tpm layer aka layer 0.
 * @param rc
 *  The rc to decode.
 * @return
 *  An error string.
 */
static const char *
tpm2_ehandler(TSS2_RC rc)
{
    bool is_fmt_1 = tss2_rc_layer_format_get(rc);

    return is_fmt_1 ? tpm2_err_handler_fmt1(rc) : tpm2_err_handler_fmt0(rc);
}

/**
 * The default system code handler. This handles codes
 * from the RM (itself and simulated tpm responses), the marshaling
 * library (mu), the tcti layers, sapi, esys and fapi.
 * @param rc
 *  The rc to decode.
 * @return
 *  An error string.
 */
static const char *
tss_err_handler (TSS2_RC rc)
{
    /*
     * subtract 1 from the error number
     * before indexing into this array.
     *
     * Commented offsets are for the corresponding
     * error number *before* subtraction. Ie error
     * number 4 is at array index 3.
     */
    static const char *errors[] =   {
        /* 1 - TSS2_BASE_RC_GENERAL_FAILURE */
        "Catch all for all errors not otherwise specified",
        /* 2 - TSS2_BASE_RC_NOT_IMPLEMENTED */
        "If called functionality isn't implemented",
        /* 3 - TSS2_BASE_RC_BAD_CONTEXT */
        "A context structure is bad",
        /* 4 - TSS2_BASE_RC_ABI_MISMATCH */
        "Passed in ABI version doesn't match called module's ABI version",
        /* 5 - TSS2_BASE_RC_BAD_REFERENCE */
        "A pointer is NULL that isn't allowed to be NULL.",
        /* 6 - TSS2_BASE_RC_INSUFFICIENT_BUFFER */
        "A buffer isn't large enough",
        /* 7 - TSS2_BASE_RC_BAD_SEQUENCE */
        "Function called in the wrong order",
        /* 8 - TSS2_BASE_RC_NO_CONNECTION */
        "Fails to connect to next lower layer",
        /* 9 - TSS2_BASE_RC_TRY_AGAIN */
        "Operation timed out; function must be called again to be completed",
        /* 10 - TSS2_BASE_RC_IO_ERROR */
        "IO failure",
        /* 11 - TSS2_BASE_RC_BAD_VALUE */
        "A parameter has a bad value",
        /* 12 - TSS2_BASE_RC_NOT_PERMITTED */
        "Operation not permitted.",
        /* 13 - TSS2_BASE_RC_INVALID_SESSIONS */
        "Session structures were sent, but command doesn't use them or doesn't"
        " use the specified number of them",
        /* 14 - TSS2_BASE_RC_NO_DECRYPT_PARAM */
        "If function called that uses decrypt parameter, but command doesn't"
        " support decrypt parameter.",
        /* 15 - TSS2_BASE_RC_NO_ENCRYPT_PARAM */
        "If function called that uses encrypt parameter, but command doesn't"
        " support decrypt parameter.",
        /* 16 - TSS2_BASE_RC_BAD_SIZE */
        "If size of a parameter is incorrect",
        /* 17 - TSS2_BASE_RC_MALFORMED_RESPONSE */
        "Response is malformed",
        /* 18 - TSS2_BASE_RC_INSUFFICIENT_CONTEXT */
        "Context not large enough",
        /* 19 - TSS2_BASE_RC_INSUFFICIENT_RESPONSE */
        "Response is not long enough",
        /* 20 - TSS2_BASE_RC_INCOMPATIBLE_TCTI */
        "Unknown or unusable TCTI version",
        /* 21 - TSS2_BASE_RC_NOT_SUPPORTED */
        "Functionality not supported",
        /* 22 - TSS2_BASE_RC_BAD_TCTI_STRUCTURE */
        "TCTI context is bad",
        /* 23 - TSS2_BASE_RC_MEMORY */
        "Failed to allocate memory",
        /* 24 - TSS2_BASE_RC_BAD_TR */
        "The ESYS_TR resource object is bad",
        /* 25 - TSS2_BASE_RC_MULTIPLE_DECRYPT_SESSIONS */
        "Multiple sessions were marked with attribute decrypt",
        /* 26 - TSS2_BASE_RC_MULTIPLE_ENCRYPT_SESSIONS */
        "Multiple sessions were marked with attribute encrypt",
        /* 27 - TSS2_BASE_RC_RSP_AUTH_FAILED */
        "Authorizing the TPM response failed",
        /* 28 - TSS2_BASE_RC_NO_CONFIG */
        "No config is available",
        /* 29 - TSS2_BASE_RC_BAD_PATH */
        "The provided path is bad",
        /* 30 - TSS2_BASE_RC_NOT_DELETABLE */
        "The object is not deletable",
        /* 31 - TSS2_BASE_RC_PATH_ALREADY_EXISTS */
        "The provided path already exists",
        /* 32 - TSS2_BASE_RC_KEY_NOT_FOUND */
        "The key was not found",
        /* 33 - TSS2_BASE_RC_SIGNATURE_VERIFICATION_FAILED */
        "Signature verification failed",
        /* 34 - TSS2_BASE_RC_HASH_MISMATCH */
        "Hashes mismatch",
        /* 35 - TSS2_BASE_RC_KEY_NOT_DUPLICABLE */
        "Key is not duplicatable",
        /* 36 - TSS2_BASE_RC_PATH_NOT_FOUND */
        "The path was not found",
        /* 37 - TSS2_BASE_RC_NO_CERT */
        "No certificate",
        /* 38 - TSS2_BASE_RC_NO_PCR */
        "No PCR",
        /* 39 - TSS2_BASE_RC_PCR_NOT_RESETTABLE */
        "PCR not resettable",
        /* 40 - TSS2_BASE_RC_BAD_TEMPLATE */
        "The template is bad",
        /* 41 - TSS2_BASE_RC_AUTHORIZATION_FAILED */
        "Authorization failed",
        /* 42 - TSS2_BASE_RC_AUTHORIZATION_UNKNOWN */
        "Authorization is unknown",
        /* 43 - TSS2_BASE_RC_NV_NOT_READABLE */
        "NV is not readable",
        /* 44 - TSS2_BASE_RC_NV_TOO_SMALL */
        "NV is too small",
        /* 45 - TSS2_BASE_RC_NV_NOT_WRITEABLE */
        "NV is not writable",
        /* 46 - TSS2_BASE_RC_POLICY_UNKNOWN */
        "The policy is unknown",
        /* 47 - TSS2_BASE_RC_NV_WRONG_TYPE */
        "The NV type is wrong",
        /* 48 - TSS2_BASE_RC_NAME_ALREADY_EXISTS */
        "The name already exists",
        /* 49 - TSS2_BASE_RC_NO_TPM */
        "No TPM available",
        /* 50 - TSS2_BASE_RC_BAD_KEY */
        "The key is bad",
        /* 51 - TSS2_BASE_RC_NO_HANDLE */
        "No handle provided",
        /* 52 - TSS2_BASE_RC_NOT_PROVISIONED */
        "Provisioning was not executed.",
        /* 53 - TSS2_FAPI_RC_ALREADY_PROVISIONED */
        "Already provisioned"
  };

    return (rc - 1u < ARRAY_LEN(errors)) ? errors[rc - 1u] : NULL;
}


static struct {
    char name[TSS2_ERR_LAYER_NAME_MAX];
    TSS2_RC_HANDLER handler;
} layer_handler[TPM2_ERROR_TSS2_RC_LAYER_COUNT + 1] = {
    ADD_HANDLER("tpm" , tpm2_ehandler),
    ADD_NULL_HANDLER,                       /* layer 1  is unused */
    ADD_NULL_HANDLER,                       /* layer 2  is unused */
    ADD_NULL_HANDLER,                       /* layer 3  is unused */
    ADD_NULL_HANDLER,                       /* layer 4  is unused */
    ADD_NULL_HANDLER,                       /* layer 5  is unused */
    ADD_HANDLER("fapi", tss_err_handler),   /* layer 6  is the fapi rc */
    ADD_HANDLER("esapi", tss_err_handler),  /* layer 7  is the esapi rc */
    ADD_HANDLER("sys", tss_err_handler),    /* layer 8  is the sys rc */
    ADD_HANDLER("mu",  tss_err_handler),    /* layer 9  is the mu rc */
                                            /* Defaults to the system handler */
    ADD_HANDLER("tcti", tss_err_handler),   /* layer 10 is the tcti rc */
                                            /* Defaults to the system handler */
    ADD_HANDLER("rmt", tpm2_ehandler),      /* layer 11 is the resource manager TPM RC */
                                            /* The RM usually duplicates TPM responses */
                                            /* So just default the handler to tpm2. */
    ADD_HANDLER("rm", NULL),                /* layer 12 is the rm rc */
    ADD_HANDLER("policy", tss_err_handler), /* layer 13 is the policy rc */
};

/**
 * If a layer has no handler registered, default to this
 * handler that prints the error number in hex.
 * @param rc
 *  The rc to print the error number of.
 * @return
 *  The string.
 */
static const char *
unknown_layer_handler(TSS2_RC rc)
{
    static __thread char buf[32];

    clearbuf(buf);
    catbuf(buf, "0x%X", rc);

    return buf;
}

/**
 * Register or unregister a custom layer error handler.
 * @param layer
 *  The layer in which to register a handler for.
 * @param name
 *  A friendly layer name. If the name is NULL or a
 *  length 0 string, then the name is output in base
 *  10 string of the layer number. If the length of
 *  name is greater than 16 characters, then the string
 *  is truncated to 16 characters.
 * @param handler
 *  The handler function to register or NULL to unregister.
 * @return
 *  True on success or False on error.
 */
TSS2_RC_HANDLER
Tss2_RC_SetHandler(UINT8 layer, const char *name,
                        TSS2_RC_HANDLER handler)
{
    TSS2_RC_HANDLER old = layer_handler[layer].handler;

    layer_handler[layer].handler = handler;

    if (handler && name) {
        snprintf(layer_handler[layer].name, sizeof(layer_handler[layer].name),
             "%s", name);
    } else {
        memset(layer_handler[layer].name, 0, sizeof(layer_handler[layer].name));
    }

    return old;
}

/**
 * Given a TSS2_RC return code, provides a static error string in the format:
 * <layer-name>:<layer-specific-msg>.
 *
 * The layer-name section will either be the friendly name, or if no layer
 * handler is registered, the base10 layer number.
 *
 * The "layer-specific-msg" is layer specific and will contain details on the
 * error that occurred or the error code if it couldn't look it up.
 *
 * Known layer specific substrings:
 * TPM - The tpm layer produces 2 distinct format codes that align with:
 *   - Section 6.6 of: https://trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-2-Structures-01.38.pdf
 *   - Section 39.4 of: https://trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-1-Architecture-01.38.pdf
 *
 *   The two formats are format 0 and format 1.
 *   Format 0 string format:
 *     - "<error|warn>(<version>): <description>
 *     - Examples:
 *       - error(1.2): bad tag
 *       - warn(2.0): the 1st handle in the handle area references a transient object or session that is not loaded
 *
 *   Format 1 string format:
 *      - <handle|session|parameter>(<index>):<description>
 *      - Examples:
 *        - handle(unk):value is out of range or is not correct for the context
 *        - tpm:handle(5):value is out of range or is not correct for the context
 *
 *   Note that passing TPM2_RC_SUCCESS results in the layer specific message of "success".
 *
 *   The System, TCTI and Marshaling (MU) layers, all define simple string
 *   returns analogous to strerror(3).
 *
 *   Unknown layers will have the layer number in decimal and then a layer specific string of
 *   a hex value representing the error code. For example: 9:0x3
 *
 * @param rc
 *  The error code to decode.
 * @return
 *  A human understandable error description string.
 */
const char *
Tss2_RC_Decode(TSS2_RC rc)
{
    static __thread char buf[TSS2_ERR_LAYER_NAME_MAX + TSS2_ERR_LAYER_ERROR_STR_MAX + 1];

    clearbuf(buf);

    UINT8 layer = tss2_rc_layer_number_get(rc);

    TSS2_RC_HANDLER handler = layer_handler[layer].handler;
    const char *lname = layer_handler[layer].name;

    if (lname[0]) {
        catbuf(buf, "%s:", lname);
    } else {
        catbuf(buf, "%u:", layer);
    }

    /*
     * Handlers only need the error bits. This way they don't
     * need to concern themselves with masking off the layer
     * bits or anything else.
     */
    if (handler) {
        UINT16 err_bits = tpm2_error_get(rc);
        const char *e = err_bits ? handler(err_bits) : "success";
        if (e) {
            catbuf(buf, "%s", e);
        } else {
            catbuf(buf, "0x%X", err_bits);
        }
    } else {
        /*
         * we don't want to drop any bits if we don't know what to do with it
         * so drop the layer byte since we we already have that.
         */
        const char *e = unknown_layer_handler(rc >> 8);
        assert(e);
        catbuf(buf, "%s", e);
    }

    return buf;
}

/** Function to extract information from a response code.
 *
 * This function decodes the different bitfields in TSS2_RC.
 *
 * @param[in]  rc the response code to decode.
 * @param[out] info the structure containing the decoded fields.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if info is a NULL pointer.
 */
TSS2_RC
Tss2_RC_DecodeInfo(TSS2_RC rc, TSS2_RC_INFO *info)
{
    UINT8 n;

    if (!info) {
        return TSS2_BASE_RC_BAD_REFERENCE;
    }

    memset(info, 0, sizeof(TSS2_RC_INFO));

    info->layer = tss2_rc_layer_number_get(rc);
    info->format = tss2_rc_layer_format_get(rc);

    if (info->format) {
        info->error = tpm2_rc_fmt1_error_get(rc) | TPM2_RC_FMT1;
        n = tpm2_rc_fmt1_N_index_get(rc);
        if (tpm2_rc_fmt1_P_get(rc)) {
	    info->parameter = n;
        } else if (tpm2_rc_fmt1_N_is_handle(rc)) {
            info->handle = n;
        } else {
          info->session = n;
        }
    } else {
        info->error = tpm2_error_get(rc);
    }

    return TSS2_RC_SUCCESS;
}

/** Function to get a human readable error from a TSS2_RC_INFO
 *
 * This function returns the human readable eror for the underlying
 * error, ignoring the layer, parameters, handles and sessions.
 *
 * @param[int] info the structure containing the decoded fields.
 * @retval A human understandable error description string.
 * @retval NULL if info is a NULL pointer.
 */
const char *
Tss2_RC_DecodeInfoError(TSS2_RC_INFO *info)
{
    static __thread char buf[TSS2_ERR_LAYER_ERROR_STR_MAX + 1];
    const char *m = NULL;

    if (!info) {
        return NULL;
    }
    clearbuf(buf);

    if (info->format) {
        m = tss2_fmt1_err_strs_get(info->error ^ TPM2_RC_FMT1);
    } else {
        m = tss2_fmt0_err_strs_get(info->error ^ TPM2_RC_VER1);
    }

    if (m) {
        catbuf(buf, "%s", m);
    } else {
        catbuf(buf, "0x%X", info->error);
    }

    return buf;
}
