/*
 * SPDX-License-Identifier: BSD-2-Clause
 * Copyright 2019, Intel Corporation
 * All rights reserved.
 */
#ifndef TCTILDR_H
#define TCTILDR_H

#include "tss2_tpm2_types.h"
#include "tss2_tcti.h"

#define TCTI_SUFFIX ".so"
#define TCTI_SUFFIX_0 TCTI_SUFFIX".0"
#define LIB_PREFIX "lib"
#define TCTI_PREFIX LIB_PREFIX"tss2-tcti"
#define TCTI_NAME_TEMPLATE TCTI_PREFIX"-%s"TCTI_SUFFIX
#define TCTI_NAME_TEMPLATE_0 TCTI_PREFIX"-%s"TCTI_SUFFIX_0
#define DEFAULT_TCTI_LIBRARY_NAME TCTI_PREFIX"-default"TCTI_SUFFIX

#define TCTILDR_MAGIC 0xbc44a31ca74b4aafULL

typedef void* TSS2_TCTI_LIBRARY_HANDLE;
typedef struct {
    TSS2_TCTI_CONTEXT_COMMON_V2 v2;
    TSS2_TCTI_LIBRARY_HANDLE library_handle;
    TSS2_TCTI_INFO *info;
    TSS2_TCTI_CONTEXT *tcti;
} TSS2_TCTILDR_CONTEXT;

TSS2_RC
tcti_from_init(TSS2_TCTI_INIT_FUNC init,
               const char* conf,
               TSS2_TCTI_CONTEXT **tcti);
TSS2_RC
tctildr_conf_parse (const char *name_conf,
                    char *name,
                    char *conf);
TSS2_RC
tctildr_transmit (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t command_size,
    const uint8_t *command_buffer);
TSS2_RC
tctildr_receive (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *response_size,
    uint8_t *response_buffer,
    int32_t timeout);
void
tctildr_finalize (
    TSS2_TCTI_CONTEXT *tctiContext);
TSS2_RC
tctildr_cancel (
    TSS2_TCTI_CONTEXT *tctiContext);
TSS2_RC
tctildr_get_poll_handles (
    TSS2_TCTI_CONTEXT *tctiContext,
    TSS2_TCTI_POLL_HANDLE *handles,
    size_t *num_handles);
TSS2_RC
tctildr_set_locality (
    TSS2_TCTI_CONTEXT *tctiContext,
    uint8_t locality);
TSS2_RC
tctildr_make_sticky (
    TSS2_TCTI_CONTEXT *tctiContext,
    TPM2_HANDLE *handle,
    uint8_t sticky);
TSS2_RC
tcti_from_info (TSS2_TCTI_INFO_FUNC infof,
                const char *conf,
                TSS2_TCTI_CONTEXT **context);
TSS2_RC
copy_info (const TSS2_TCTI_INFO *info_src,
           TSS2_TCTI_INFO *info_dst);

#endif /* TCTILDR_H */
