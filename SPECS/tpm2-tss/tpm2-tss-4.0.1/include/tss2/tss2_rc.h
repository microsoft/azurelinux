/* SPDX-License-Identifier: BSD-2-Clause */

#ifndef TSS2_RC_H
#define TSS2_RC_H

#include <stdint.h>

#include "tss2_tpm2_types.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef const char *(*TSS2_RC_HANDLER)(TSS2_RC rc);

const char *Tss2_RC_Decode(TSS2_RC rc);

TSS2_RC_HANDLER Tss2_RC_SetHandler(uint8_t layer, const char *name, TSS2_RC_HANDLER handler);

typedef struct TSS2_RC_INFO TSS2_RC_INFO;
struct TSS2_RC_INFO {
    UINT8 layer;
    UINT8 format;
    TSS2_RC error;
    UINT8 parameter;
    UINT8 session;
    UINT8 handle;
};

TSS2_RC Tss2_RC_DecodeInfo(TSS2_RC, TSS2_RC_INFO *info);

const char *Tss2_RC_DecodeInfoError(TSS2_RC_INFO *info);

#ifdef __cplusplus
}
#endif

#endif
