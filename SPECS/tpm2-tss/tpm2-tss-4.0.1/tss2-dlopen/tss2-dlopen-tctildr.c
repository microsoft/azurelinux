/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2021, Fraunhofer SIT
 * All rights reserved.
 *******************************************************************************/

/**
 * The purpose of this file is to copy it into your project and
 * include it during compilation if you don't want to link against
 * libtss2-tctildr at compile time.
 * It will attempt to load libtss2-esys.so during runtime.
 * It will either work similarly to directly linking to libtss2-tctildr.so
 * at compile-time or return a NOT_IMPLEMENTED error.
 *
 * For new versions of this file, please check:
 * http://github.com/tpm2-software/tpm2-tss/tss2-dlopen
*/

#include <dlfcn.h>
#include <stdio.h>
#include <tss2/tss2_tctildr.h>

#define str(s) xstr(s)
#define xstr(s) #s

#ifdef ENABLE_WARN
#define WARN(str, ...) do { fprintf(stderr, "WARNING: " str "\n", ## __VA_ARGS__); } while (0)
#else /* ENABLE_WARN */
#define WARN(...) do { } while (0)
#endif /* ENABLE_WARN */

#define LIB "libtss2-tctildr.so.0"
static void *dlhandle = NULL;

static TSS2_RC
init_dlhandle(void)
{
    if (dlhandle)
        return TSS2_RC_SUCCESS;
    dlhandle = dlopen(LIB, RTLD_NOW | RTLD_LOCAL);
    if (!dlhandle) {
        WARN("Library " LIB " not found: %s.", dlerror());
        return TSS2_TCTI_RC_NOT_IMPLEMENTED;
    }
    return TSS2_RC_SUCCESS;
}

TSS2_RC
Tss2_TctiLdr_Initialize_Ex (const char *name,
                            const char *conf,
                            TSS2_TCTI_CONTEXT **context)
{
    if (init_dlhandle() != TSS2_RC_SUCCESS)
        return TSS2_TCTI_RC_NOT_IMPLEMENTED;

    static TSS2_RC (*sym) (const char *name, const char *conf, TSS2_TCTI_CONTEXT **context) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Tss2_TctiLdr_Initialize_Ex");
    if (!sym) {
        WARN("Function Tss2_TctiLdr_Initialize_Ex not found.");
        return TSS2_TCTI_RC_NOT_IMPLEMENTED;
    }

    return sym(name, conf, context);
}

TSS2_RC
Tss2_TctiLdr_Initialize (const char *nameConf,
                         TSS2_TCTI_CONTEXT **context)
{
    if (init_dlhandle() != TSS2_RC_SUCCESS)
        return TSS2_TCTI_RC_NOT_IMPLEMENTED;

    static TSS2_RC (*sym) (const char *nameConf, TSS2_TCTI_CONTEXT **context) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Tss2_TctiLdr_Initialize");
    if (!sym) {
        WARN("Function Tss2_TctiLdr_Initialize not found.");
        return TSS2_TCTI_RC_NOT_IMPLEMENTED;
    }

    return sym(nameConf, context);
}

TSS2_RC
Tss2_TctiLdr_GetInfo (const char *name,
                      TSS2_TCTI_INFO **info)
{
    if (init_dlhandle() != TSS2_RC_SUCCESS)
        return TSS2_TCTI_RC_NOT_IMPLEMENTED;

    static TSS2_RC (*sym) (const char *name, TSS2_TCTI_INFO **info) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Tss2_TctiLdr_GetInfo");
    if (!sym) {
        WARN("Function Tss2_TctiLdr_GetInfo not found.");
        return TSS2_TCTI_RC_NOT_IMPLEMENTED;
    }

    return sym(name, info);
}


void
Tss2_TctiLdr_Finalize (TSS2_TCTI_CONTEXT **context)
{
    if (!context || !*context)
        return;
    static void (*sym) (TSS2_TCTI_CONTEXT **context) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Tss2_TctiLdr_Finalize");
    if (!sym) {
        WARN("Function Tss2_TctiLdr_Finalize not found.");
        return;
    }

    sym(context);
}

void
Tss2_TctiLdr_FreeInfo (TSS2_TCTI_INFO **info)
{
    if (!info || !*info)
        return;
    static void (*sym) (TSS2_TCTI_INFO **info) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Tss2_TctiLdr_FreeInfo");
    if (!sym) {
        WARN("Function Tss2_TctiLdr_FreeInfo not found.");
        return;
    }

    sym(info);
}
