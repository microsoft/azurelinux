/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2021, Fraunhofer SIT
 * All rights reserved.
 *******************************************************************************/

/**
 * The purpose of this file is to copy it into your project and
 * include it during compilation if you don't want to link against
 * libtss2-rc at compile time.
 * It will attempt to load libtss2-rc.so during runtime.
 * It will either work similarly to directly linking to libtss2-rc.so
 * at compile-time or return an error string or NULL.
 *
 * For new versions of this file, please check:
 * http://github.com/tpm2-software/tpm2-tss/tss2-dlopen
*/

#include <dlfcn.h>
#include <stdio.h>
#include <tss2/tss2_rc.h>

#define str(s) xstr(s)
#define xstr(s) #s

#ifdef ENABLE_WARN
#define WARN(str, ...) do { fprintf(stderr, "WARNING: " str "\n", ## __VA_ARGS__); } while (0)
#else /* ENABLE_WARN */
#define WARN(...) do { } while (0)
#endif /* ENABLE_WARN */

#define LIB "libtss2-rc.so.0"
static void *dlhandle = NULL;

static TSS2_RC
init_dlhandle(void)
{
    if (dlhandle)
        return TSS2_RC_SUCCESS;
    dlhandle = dlopen(LIB, RTLD_NOW | RTLD_LOCAL);
    if (!dlhandle) {
        WARN("Library " LIB " not found: %s.", dlerror());
        return TSS2_BASE_RC_NOT_IMPLEMENTED;
    }
    return TSS2_RC_SUCCESS;
}

static const char *error = LIB " not found.";

const char *
Tss2_RC_Decode(TSS2_RC rc)
{
    if (init_dlhandle() != TSS2_RC_SUCCESS)
        return error;

    static const char * (*sym) (TSS2_RC rc) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Tss2_RC_Decode");
    if (!sym) {
        WARN("Function Tss2_RC_Decode not found.");
        return error;
    }

    return sym(rc);
}

TSS2_RC_HANDLER
Tss2_RC_SetHandler(uint8_t layer, const char *name, TSS2_RC_HANDLER handler)
{
    if (init_dlhandle() != TSS2_RC_SUCCESS)
        return NULL;

    TSS2_RC_HANDLER (*sym) (uint8_t layer, const char *name, TSS2_RC_HANDLER handler) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Tss2_RC_SetHandler");
    if (!sym) {
        WARN("Function Tss2_RC_SetHandler not found.");
        return NULL;
    }

    return sym(layer, name, handler);
}
