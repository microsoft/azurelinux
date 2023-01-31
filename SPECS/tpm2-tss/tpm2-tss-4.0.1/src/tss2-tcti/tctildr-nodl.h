/*
 * SPDX-License-Identifier: BSD-2-Clause
 * Copyright 2019, Intel Corporation
 */
#ifndef TCTILDR_NODL_H
#define TCTILDR_NODL_H

#include "tss2_tpm2_types.h"
#include "tss2_tcti.h"

TSS2_RC
tctildr_get_default (TSS2_TCTI_CONTEXT **tcti,
                     void **data);

#endif /* TCTILDR_NODL_H */
