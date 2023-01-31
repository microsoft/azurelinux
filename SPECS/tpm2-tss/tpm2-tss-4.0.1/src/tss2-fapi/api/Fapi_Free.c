/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

/** Frees a FAPI allocated return buffer.
 *
 * Fapi_Free is a helper function that is a wrapper around free().
 * This allows programs that are built using a different version
 * of the C runtime to free memory that has been allocated by the
 * esys library on Windows.
 *
 * @param[in] ptr A pointer to the object that is to be freed.
 */
void
Fapi_Free(void *ptr)
{
    if (ptr != NULL) {
        free(ptr);
    }
}
