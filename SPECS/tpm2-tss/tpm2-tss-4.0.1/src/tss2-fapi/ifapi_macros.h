/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef IFAPI_MACROS_H
#define IFAPI_MACROS_H

#define strdup_check(dest, str, r, label) \
    if (str) {                             \
       dest = strdup(str); \
       if (!dest) { \
          r = TSS2_FAPI_RC_MEMORY; \
          LOG_ERROR("Out of memory.");          \
          goto label; \
       } \
    } else { \
        dest = NULL; \
    }

#define calloc_check(dest, size, r, label) \
    {                             \
       dest = callock(size,1);     \
       if (!dest) { \
          r = TSS2_FAPI_RC_MEMORY; \
          LOG_ERROR("Out of memory.");          \
          goto label; \
       } \
    }

#define goto_if_null2(p,msg, r, ec, label, ...) \
    if ((p) == NULL) { \
        LOG_ERROR(TPM2_ERROR_FORMAT " " msg, TPM2_ERROR_TEXT(ec), ## __VA_ARGS__); \
        r = (ec); \
        goto label;  \
    }

#define goto_if_error2(r,msg,label, ...)             \
    if (r != TSS2_RC_SUCCESS) { \
        LOG_ERROR(TPM2_ERROR_FORMAT " " msg, TPM2_ERROR_TEXT(r), ## __VA_ARGS__); \
        goto label;  \
    }

#define return_if_error2(r,msg, ...)                \
    if (r != TSS2_RC_SUCCESS) { \
        LOG_ERROR(TPM2_ERROR_FORMAT " " msg, TPM2_ERROR_TEXT(r), ## __VA_ARGS__); \
        return r;  \
    }

#define try_again_or_error(r,msg, ...)                \
    if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN) \
        return TSS2_FAPI_RC_TRY_AGAIN; \
    if (r != TSS2_RC_SUCCESS) { \
        LOG_ERROR(TPM2_ERROR_FORMAT " " msg, TPM2_ERROR_TEXT(r), ## __VA_ARGS__); \
        return r;  \
    }

#define try_again_or_error_goto(r,msg, label, ...)            \
    if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN) \
        return TSS2_FAPI_RC_TRY_AGAIN; \
    if (r != TSS2_RC_SUCCESS) { \
        LOG_ERROR(TPM2_ERROR_FORMAT " " msg, TPM2_ERROR_TEXT(r), ## __VA_ARGS__); \
        goto label;  \
    }

#define return_error2(r,msg, ...) {               \
    LOG_ERROR(TPM2_ERROR_FORMAT " " msg, TPM2_ERROR_TEXT(r), ## __VA_ARGS__); \
    return (r); }


#define return_if_error_reset_state(r,msg, ...)     \
    if (r != TSS2_RC_SUCCESS) { \
        LOG_ERROR(TPM2_ERROR_FORMAT " " msg, TPM2_ERROR_TEXT(r), ## __VA_ARGS__); \
        context->state = _FAPI_STATE_INIT; \
        return r;  \
    }

#define goto_if_error_reset_state(r,msg,label, ...) \
    if (r != TSS2_RC_SUCCESS) { \
        LOG_ERROR(TPM2_ERROR_FORMAT " " msg, TPM2_ERROR_TEXT(r), ## __VA_ARGS__); \
        context->state = _FAPI_STATE_INIT; \
        goto label;  \
    }

#define goto_error_reset_state(r,v,msg,label) {  \
    r = v; \
    LOG_ERROR("%s " TPM2_ERROR_FORMAT, msg, TPM2_ERROR_TEXT(r));    \
    context->state = _FAPI_STATE_INIT;                              \
    goto label; }

#define goto_if_null_reset_state(p,msg,r,ec,label)  \
    if ((p) == NULL) { \
        LOG_ERROR("%s ", (msg)); \
        context->state = _FAPI_STATE_INIT;      \
        (r) = (ec);                             \
        goto label;  \
    }

#define return_try_again(r) \
    if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN) { \
        LOG_TRACE("Received TRY_AGAIN; returning TRY_AGAIN"); \
        return TSS2_FAPI_RC_TRY_AGAIN; \
    }

#define check_not_null(X) \
    if (X == NULL) { \
        LOG_ERROR(str(X) " is NULL: BAD_REFERENCE"); \
        return TSS2_FAPI_RC_BAD_REFERENCE; \
    }

#define check_oom(X) \
    if (X == NULL) { \
        LOG_ERROR("Out of memory"); \
        return TSS2_FAPI_RC_MEMORY; \
    }

#if defined __GNUC__ && __GNUC__ < 7
#define fallthrough { }
#else
#define fallthrough __attribute__((fallthrough))
#endif

#define statecase(VAR, STATE) \
    case STATE: \
        LOG_TRACE("State " str(VAR) " reached " str(STATE)); \
        VAR=STATE;

#define general_failure(VAR) \
    default: \
        LOG_ERROR("Bad state for " str(VAR)); \
        return TSS2_FAPI_RC_GENERAL_FAILURE;

#define statecasedefault(VAR) \
    default: \
        LOG_ERROR("Bad state for " str(VAR)); \
        return TSS2_FAPI_RC_BAD_SEQUENCE;

#define statecasedefault_error(VAR, r, label)         \
    default: \
        LOG_ERROR("Bad state for " str(VAR)); \
        r = TSS2_FAPI_RC_BAD_SEQUENCE; \
        goto label;

#endif /* IFAPI_MACROS_H */
