/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * Copyright 2019, Intel Corporation
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <dlfcn.h>
#include <limits.h>
#include <stdio.h>

#include "tss2_tcti.h"
#include "tctildr-interface.h"
#include "tctildr.h"
#define LOGMODULE tcti
#include "util/log.h"

#define ARRAY_SIZE(X) (sizeof(X)/sizeof(X[0]))

struct {
    char *file;
    char *conf;
    char *description;
} tctis[] = {
    {
        .file = "libtss2-tcti-default.so",
        .description = "Access libtss2-tcti-default.so",
    },
    {
        .file = "libtss2-tcti-tabrmd.so.0",
        .description = "Access libtss2-tcti-tabrmd.so",
    },
    {
        .file = "libtss2-tcti-device.so.0",
        .conf = "/dev/tpmrm0",
        .description = "Access libtss2-tcti-device.so.0 with /dev/tpmrm0",
    },
    {
        .file = "libtss2-tcti-device.so.0",
        .conf = "/dev/tpm0",
        .description = "Access libtss2-tcti-device.so.0 with /dev/tpm0",
    },
    {
        .file = "libtss2-tcti-swtpm.so.0",
        .description = "Access to libtss2-tcti-swtpm.so",
    },
    {
        .file = "libtss2-tcti-mssim.so.0",
        .description = "Access to libtss2-tcti-mssim.so",
    },
};

const TSS2_TCTI_INFO*
info_from_handle (void *dlhandle)
{
    TSS2_TCTI_INFO_FUNC info_func;

    if (dlhandle == NULL)
        return NULL;

    info_func = dlsym  (dlhandle, TSS2_TCTI_INFO_SYMBOL);
    if (info_func == NULL) {
        LOG_ERROR ("Failed to get reference to TSS2_TCTI_INFO_SYMBOL: %s",
                   dlerror());
        return NULL;
    }

    return info_func ();
}
TSS2_RC
handle_from_name(const char *file,
                 void **handle)
{
    char *file_xfrm = NULL;
    size_t size;
    size_t len;

    if (handle == NULL) {
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }
    *handle = dlopen(file, RTLD_NOW);
    if (*handle != NULL) {
        return TSS2_RC_SUCCESS;
    } else {
        LOG_DEBUG("Could not load TCTI file: \"%s\": %s", file, dlerror());
    }

    len = snprintf(NULL, 0, TCTI_NAME_TEMPLATE_0, file);
    if (len >= PATH_MAX) {
        LOG_ERROR("TCTI name truncated in transform.");
        return TSS2_TCTI_RC_BAD_VALUE;
    }
    file_xfrm = calloc(len + 1, sizeof(char));
    if (file_xfrm == NULL) {
        return TSS2_TCTI_RC_MEMORY;
    }
    /* 'name' alone didn't work, try libtss2-tcti-<name>.so.0 */
    size = snprintf(file_xfrm,
                    len + 1,
                    TCTI_NAME_TEMPLATE_0,
                    file);
    if (size >= (len + 1)) {
        LOG_ERROR("TCTI name truncated in transform.");
        SAFE_FREE(file_xfrm);
        return TSS2_TCTI_RC_BAD_VALUE;
    }
    *handle = dlopen(file_xfrm, RTLD_NOW);
    if (*handle != NULL) {
        SAFE_FREE(file_xfrm);
        return TSS2_RC_SUCCESS;
    } else {
        LOG_DEBUG("Could not load TCTI file \"%s\": %s", file, dlerror());
    }
    /* libtss2-tcti-<name>.so.0 didn't work, try libtss2-tcti-<name>.so */
    size = snprintf(file_xfrm,
                    len + 1,
                    TCTI_NAME_TEMPLATE,
                    file);
    if (size >= (len + 1)) {
        LOG_ERROR("TCTI name truncated in transform.");
        SAFE_FREE(file_xfrm);
        return TSS2_TCTI_RC_BAD_VALUE;
    }
    *handle = dlopen(file_xfrm, RTLD_NOW);
    if (*handle == NULL) {
        LOG_DEBUG("Failed to load TCTI for name \"%s\": %s", file, dlerror());
        SAFE_FREE(file_xfrm);
        return TSS2_TCTI_RC_NOT_SUPPORTED;
    }

    SAFE_FREE(file_xfrm);
    return TSS2_RC_SUCCESS;
}
TSS2_RC
tcti_from_file(const char *file,
               const char* conf,
               TSS2_TCTI_CONTEXT **tcti,
               void **dlhandle)
{
    TSS2_RC r;
    void *handle;
    TSS2_TCTI_INFO_FUNC infof;

    LOG_TRACE("Attempting to load TCTI file: %s", file);
    if (tcti == NULL) {
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }
    r = handle_from_name(file, &handle);
    if (r != TSS2_RC_SUCCESS) {
        return r;
    }

    infof = (TSS2_TCTI_INFO_FUNC) dlsym(handle, TSS2_TCTI_INFO_SYMBOL);
    if (infof == NULL) {
        LOG_ERROR("Info not found in TCTI file: %s", file);
        dlclose(handle);
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }

    r = tcti_from_info(infof, conf, tcti);
    if (r != TSS2_RC_SUCCESS) {
        LOG_ERROR("Could not initialize TCTI file: %s", file);
        dlclose(handle);
        return r;
    }

    if (dlhandle)
        *dlhandle = handle;

    LOG_DEBUG("Initialized TCTI file: %s", file);

    return TSS2_RC_SUCCESS;
}
TSS2_RC
get_info_default(const TSS2_TCTI_INFO **info,
                 void **dlhandle)
{
    void *handle = NULL;
    const TSS2_TCTI_INFO *info_src;
    char *name = NULL;
    TSS2_RC rc = TSS2_TCTI_RC_GENERAL_FAILURE;

    LOG_DEBUG("%s", __func__);
    if (info == NULL || dlhandle == NULL) {
        LOG_ERROR("parameters cannot be NULL");
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }
#ifdef ESYS_TCTI_DEFAULT_MODULE
    name = ESYS_TCTI_DEFAULT_MODULE;
    LOG_DEBUG("name: %s", name);
    rc = handle_from_name (name, &handle);
    if (rc != TSS2_RC_SUCCESS)
        return rc;
    else if (handle == NULL)
        return TSS2_TCTI_RC_IO_ERROR;
#else
    size_t i;
    for (i = 0; i < ARRAY_SIZE(tctis); i++) {
        name = tctis[i].file;
        LOG_DEBUG("name: %s", name);
        if (name == NULL) {
            continue;
        }
        rc = handle_from_name (name, &handle);
        if (rc != TSS2_RC_SUCCESS || handle == NULL) {
            LOG_DEBUG("Failed to get handle for TCTI with name: %s", name);
            continue;
        }

        break;
    }
#endif /* ESYS_TCTI_DEFAULT_MODULE */

    info_src = info_from_handle (handle);
    if (info_src != NULL) {
        *info = info_src;
    } else {
        tctildr_finalize_data (&handle);
        rc = TSS2_TCTI_RC_GENERAL_FAILURE;
    }
    *dlhandle = handle;

    return rc;
}

TSS2_RC
tctildr_get_default(TSS2_TCTI_CONTEXT ** tcticontext, void **dlhandle)
{
    if (tcticontext == NULL) {
        LOG_ERROR("tcticontext must not be NULL");
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }
    *tcticontext = NULL;
#ifdef ESYS_TCTI_DEFAULT_MODULE

#ifdef ESYS_TCTI_DEFAULT_CONFIG
    const char *config = ESYS_TCTI_DEFAULT_CONFIG;
#else /* ESYS_TCTI_DEFAULT_CONFIG */
    const char *config = NULL;
#endif /* ESYS_TCTI_DEFAULT_CONFIG */

    LOG_DEBUG("Attempting to initialize TCTI defined during compilation: %s:%s",
              ESYS_TCTI_DEFAULT_MODULE, config);
    return tcti_from_file(ESYS_TCTI_DEFAULT_MODULE, config, tcticontext,
                          dlhandle);

#else /* ESYS_TCTI_DEFAULT_MODULE */

    TSS2_RC r;
    size_t i;

    for (i = 0; i < ARRAY_SIZE(tctis); i++) {
        LOG_DEBUG("Attempting to connect using standard TCTI: %s",
                  tctis[i].description);
        r = tcti_from_file(tctis[i].file, tctis[i].conf, tcticontext,
                           dlhandle);
        if (r == TSS2_RC_SUCCESS)
            return TSS2_RC_SUCCESS;
        LOG_DEBUG("Failed to load standard TCTI number %zu", i);
    }

    LOG_ERROR("No standard TCTI could be loaded");
    return TSS2_TCTI_RC_IO_ERROR;

#endif /* ESYS_TCTI_DEFAULT_MODULE */
}
TSS2_RC
info_from_name (const char *name,
                const TSS2_TCTI_INFO **info,
                void **data)
{
    TSS2_RC rc;

    if (data == NULL || info == NULL)
        return TSS2_TCTI_RC_BAD_REFERENCE;
    rc = handle_from_name (name, data);
    if (rc != TSS2_RC_SUCCESS)
        return rc;
    *info = info_from_handle (*data);
    if (*info == NULL) {
        tctildr_finalize_data (data);
        return TSS2_TCTI_RC_IO_ERROR;
    }
    return rc;
}
TSS2_RC
tctildr_get_info(const char *name,
                 const TSS2_TCTI_INFO **info,
                 void **data)
{
    if (info == NULL) {
        LOG_ERROR("info must not be NULL");
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }
    if (name != NULL) {
        return info_from_name (name, info, data);
    } else {
        return get_info_default (info, data);
    }
}
TSS2_RC
tctildr_get_tcti(const char *name,
                 const char* conf,
                 TSS2_TCTI_CONTEXT **tcti,
                 void **data)
{
    LOG_DEBUG("name: \"%s\", conf: \"%s\"", name, conf);
    if (tcti == NULL) {
        LOG_ERROR("tcticontext must not be NULL");
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }
    *tcti = NULL;
    if (name == NULL) {
        return tctildr_get_default (tcti, data);
    }

    return tcti_from_file (name, conf, tcti, data);
}

void
tctildr_finalize_data (void **data)
{
    if (data != NULL && *data != NULL) {
        dlclose(*data);
        *data = NULL;
    }
}
