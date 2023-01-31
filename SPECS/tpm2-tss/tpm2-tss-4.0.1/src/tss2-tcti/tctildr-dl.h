/*
 * SPDX-License-Identifier: BSD-2-Clause
 * Copyright 2019, Intel Corporation
 */
#ifndef TCTILDR_DL_H
#define TCTILDR_DL_H

#include "tss2_tpm2_types.h"
#include "tss2_tcti.h"

const TSS2_TCTI_INFO*
info_from_handle (void *dlhandle);
TSS2_RC
info_from_name (const char *name,
                const TSS2_TCTI_INFO **info,
                void **data);
TSS2_RC
handle_from_name(const char *file,
                 void **handle);
TSS2_RC
tcti_from_file(const char *file,
               const char* conf,
               TSS2_TCTI_CONTEXT **tcti,
               void **dlhandle);
TSS2_RC
get_info_default(TSS2_TCTI_INFO **info,
                 void **dlhandle);
TSS2_RC
tctildr_get_default(TSS2_TCTI_CONTEXT ** tcticontext, void **dlhandle);

#endif /* TCTILDR_DL_H */
