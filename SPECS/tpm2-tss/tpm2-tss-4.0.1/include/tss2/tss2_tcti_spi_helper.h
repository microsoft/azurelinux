/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright 2020 Fraunhofer SIT. All rights reserved.
 */
#ifndef TSS2_TCTI_SPI_HELPER_HELPER_H
#define TSS2_TCTI_SPI_HELPER_HELPER_H

#include <stdbool.h>
#include "tss2_tcti.h"

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Forward declaration
 *
 * See doc/tcti-spi-helper.md for example platform method implementations.
 */
typedef struct TSS2_TCTI_SPI_HELPER_PLATFORM TSS2_TCTI_SPI_HELPER_PLATFORM;

/*
 * Sleeps for the specified amount of milliseconds
 */
typedef TSS2_RC (*TSS2_TCTI_SPI_HELPER_PLATFORM_SLEEP_MS_FUNC) (void* user_data, int milliseconds);

/*
 * Starts a timeout timer which expires in the specified amount of milliseconds.
 * This can be done by storing the expire time (now + milliseconds) in the userdata.
 */
typedef TSS2_RC (*TSS2_TCTI_SPI_HELPER_PLATFORM_START_TIMEOUT_FUNC) (void* user_data, int milliseconds);

/*
 * Returns true if the timeout started previously by START_TIMEOUT_FUNC already has expired, false otherwise.
 * This can be done e.g. by comparing the current time and the stored timer expire time.
 * This method will be called often when waiting for timeouts and should be fast.
 */
typedef TSS2_RC (*TSS2_TCTI_SPI_HELPER_PLATFORM_TIMEOUT_EXPIRED_FUNC) (void* user_data, bool *result);

/*
 * Reserves the SPI bus until the transaction is over and SPI_RELEASE_FUNC is called.
 * Make sure the chip select stays pulled the entire time over multiple calls to SPI_TRANSFER_FUNC
 * until SPI_RELEASE_FUNC is called in the end!!!
 */
typedef TSS2_RC (*TSS2_TCTI_SPI_HELPER_PLATFORM_SPI_ACQUIRE_FUNC) (void* user_data);

/*
 * Stops pulling chip select and releases the SPI bus again.
 */
typedef TSS2_RC (*TSS2_TCTI_SPI_HELPER_PLATFORM_SPI_RELEASE_FUNC) (void* user_data);

/*
 * Transfers cnt bytes from data_out to the SPI slave. Reads the response into data_in.
 */
typedef TSS2_RC (*TSS2_TCTI_SPI_HELPER_PLATFORM_SPI_TRANSFER_FUNC) (void* user_data, const void *data_out, void *data_in, size_t cnt);

/*
 * Is called by Tss2_Tcti_Finalize right before the TCTI context is destroyed and
 * should free user_data and all resources inside like e.g. SPI device handles.
 */
typedef void (*TSS2_TCTI_SPI_HELPER_PLATFORM_FINALIZE) (void* user_data);

/*
 * Contains user implemented platform methods for the SPI TCTI.
 *
 * See doc/tcti-spi-helper.md for example implementations.
 */
struct TSS2_TCTI_SPI_HELPER_PLATFORM {
    void* user_data;
    TSS2_TCTI_SPI_HELPER_PLATFORM_SLEEP_MS_FUNC sleep_ms;
    TSS2_TCTI_SPI_HELPER_PLATFORM_START_TIMEOUT_FUNC start_timeout;
    TSS2_TCTI_SPI_HELPER_PLATFORM_TIMEOUT_EXPIRED_FUNC timeout_expired;
    TSS2_TCTI_SPI_HELPER_PLATFORM_SPI_ACQUIRE_FUNC spi_acquire;
    TSS2_TCTI_SPI_HELPER_PLATFORM_SPI_RELEASE_FUNC spi_release;
    TSS2_TCTI_SPI_HELPER_PLATFORM_SPI_TRANSFER_FUNC spi_transfer;
    TSS2_TCTI_SPI_HELPER_PLATFORM_FINALIZE finalize;
};

/*
 * Initializes the SPI TCTI with a context pointer and platform methods.
 * When the tctiContext pointer is NULL, the needed buffer size is written to *size.
 * platform_conf contains platform methods implemented by the user for SPI
 * communication and timeout handling.
 *
 * See doc/tcti-spi-helper.md for example implementations.
 */
TSS2_RC Tss2_Tcti_Spi_Helper_Init (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    TSS2_TCTI_SPI_HELPER_PLATFORM *platform_conf);

#ifdef __cplusplus
}
#endif

#endif /* TSS2_TCTI_SPI_HELPER_HELPER_H */
