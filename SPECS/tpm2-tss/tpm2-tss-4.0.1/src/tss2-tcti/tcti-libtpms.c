/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2019, Fraunhofer SIT, Infineon Technologies AG, Intel Corporation
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <dlfcn.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/syscall.h>
#include <netinet/in.h>
#include "tss2_tcti_libtpms.h"

#include "tcti-libtpms.h"
#include "tcti-common.h"
#define LOGMODULE tcti
#include "util/log.h"

/*
 * libtpms API calls need to be wrapped. We set the current active TCTI module
 * for this thread. This is needed because libtpms may call callbacks and these
 * need to know which TCTI context they have to operate on.
 *
 * This macro assumes that int ret is declared. Jumps to fail_label on error. In
 * this case, rc contains the respective error code.
 */
#define LIBTPMS_API_CALL(fail_label, tcti_libtpms, function, ...) \
    current_tcti_libtpms = tcti_libtpms; \
    ret = tcti_libtpms->function(__VA_ARGS__); \
    if (ret != TPM_SUCCESS) { \
        LOG_ERROR("libtpms function " #function "() failed with return code 0x%" PRIx32, ret); \
        rc = TSS2_TCTI_RC_GENERAL_FAILURE; \
        goto fail_label; \
    } \
    current_tcti_libtpms = NULL;

static __thread TSS2_TCTI_LIBTPMS_CONTEXT *current_tcti_libtpms = NULL;

/*
 * Map the state file for this context into memory and allocate disk space. The
 * file descriptor is closed again. Once this context reaches the end of its
 * lifetime, the memory must be unmapped and the file must be truncated to its
 * real size (rather than the allocated size).
 */
static TSS2_RC
tcti_libtpms_map_state_file(TSS2_TCTI_LIBTPMS_CONTEXT *tcti_libtpms)
{
    TSS2_RC rc;
    int ret;
    int state_fd = -1;
    ssize_t file_len = 0;

    /* if no/empty state path, skip */
    if (tcti_libtpms->state_path == NULL) {
        LOG_DEBUG("No state path. Skip mapping state file.");
        return TPM2_RC_SUCCESS;
    }
    LOG_DEBUG("Mapping state file: %s", tcti_libtpms->state_path);

    tcti_libtpms->state_mmap_len = STATE_MMAP_CHUNK_LEN;

    /* open file */
    state_fd = open(tcti_libtpms->state_path, O_RDWR | O_CREAT, 0644);
    if(state_fd == -1){
        LOG_ERROR("open failed on file %s: %s",
                    tcti_libtpms->state_path,
                    strerror(errno));
        return TSS2_TCTI_RC_IO_ERROR;
    }

    /* get file size (to detect if state does already exist). */
    file_len = lseek(state_fd, 0L, SEEK_END);
    if(file_len < 0){
        LOG_ERROR("lseek failed on file %s: %s",
                    tcti_libtpms->state_path,
                    strerror(errno));
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto cleanup_fd;
    }
    tcti_libtpms->state_mmap_len = (file_len / STATE_MMAP_CHUNK_LEN + 1) * STATE_MMAP_CHUNK_LEN;

    /* allocate disk space */
    ret = posix_fallocate(state_fd, 0, tcti_libtpms->state_mmap_len);
    if (ret != 0) {
        LOG_ERROR("fallocate failed on file %s: %d",tcti_libtpms->state_path, ret);
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto cleanup_fd;
    }


    /* map memory (either backed by file or not) */
    tcti_libtpms->state_mmap = mmap(NULL,
                                    tcti_libtpms->state_mmap_len,
                                    PROT_READ | PROT_WRITE,
                                    MAP_SHARED,
                                    state_fd,
                                    0);
    if (tcti_libtpms->state_mmap == MAP_FAILED){
        tcti_libtpms->state_mmap_len = 0;
        LOG_ERROR("mmap failed on file %s: %s",
                  tcti_libtpms->state_path,
                  strerror(errno));
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto cleanup_fd;
    }

    tcti_libtpms->state_len = file_len;

    rc = TPM2_RC_SUCCESS;

cleanup_fd:
    if (state_fd != -1) {
        /* file can always be closed, this does not unmap the region */
        close(state_fd);
    }

    return rc;
}

/*
 * If the mapped memory for the state file does not suffice, reallocate.
 */
static TSS2_RC
tcti_libtpms_ensure_state_len(
    TSS2_TCTI_LIBTPMS_CONTEXT *tcti_libtpms,
    size_t state_len)
{
    int ret;
    char *new_state_mmap;
    size_t new_state_mmap_len;
    int state_fd;

    if (state_len > tcti_libtpms->state_mmap_len)
    {
        new_state_mmap_len = (state_len / STATE_MMAP_CHUNK_LEN + 1) * STATE_MMAP_CHUNK_LEN;
        LOG_DEBUG("Mapped memory region is too small: %zu > %zu. Reallocating to %zu...",
                  state_len,
                  tcti_libtpms->state_mmap_len,
                  new_state_mmap_len);
        new_state_mmap = mremap(tcti_libtpms->state_mmap,
                                tcti_libtpms->state_mmap_len,
                                new_state_mmap_len,
                                MREMAP_MAYMOVE);
        if (new_state_mmap == MAP_FAILED) {
            LOG_ERROR("mremap failed on file %s: %s",
                      tcti_libtpms->state_path,
                      strerror(errno));
            return TSS2_TCTI_RC_IO_ERROR;
        }
        tcti_libtpms->state_mmap = new_state_mmap;
        tcti_libtpms->state_mmap_len = new_state_mmap_len;

        LOG_DEBUG("Successfully mapped state file to %zu bytes.",
                  tcti_libtpms->state_mmap_len);

        /* allocate more disk space */
        if (tcti_libtpms->state_path) {
            state_fd = open(tcti_libtpms->state_path, O_RDWR | O_CREAT, 0644);
            if(state_fd == -1){
                LOG_ERROR("open failed on file %s: %s",
                        tcti_libtpms->state_path,
                        strerror(errno));
                return TSS2_TCTI_RC_IO_ERROR;
            }

            ret = posix_fallocate(state_fd, 0, tcti_libtpms->state_mmap_len);
            if (ret != 0) {
                LOG_ERROR("fallocate failed on file %s: %d",tcti_libtpms->state_path, ret);
                close(state_fd);
                return TSS2_TCTI_RC_IO_ERROR;
            }

            close(state_fd);
        }
    }

    return TSS2_RC_SUCCESS;
}

/*
 * Retrieve libtpms state and save it to the state file.
 */
static TSS2_RC
tcti_libtpms_store_state(TSS2_TCTI_LIBTPMS_CONTEXT *tcti_libtpms)
{
    TSS2_RC rc;
    int ret;
    unsigned char *permanent_buf, *volatile_buf;
    uint32_t permanent_buf_len, volatile_buf_len;
    uint32_t permanent_buf_len_be, volatile_buf_len_be;
    size_t offset = 0;
    size_t size;

    /* if no state file, skip loading */
    if (tcti_libtpms->state_path == NULL) {
        LOG_DEBUG("No state file. Skip storing state file.");
        return TPM2_RC_SUCCESS;
    }
    LOG_DEBUG("Storing state to file: %s", tcti_libtpms->state_path);

    /* get states */
    LIBTPMS_API_CALL(fail,
                     tcti_libtpms,
                     TPMLIB_GetState,
                     TPMLIB_STATE_PERMANENT,
                     &permanent_buf,
                     &permanent_buf_len);
    LIBTPMS_API_CALL(cleanup_permanent,
                     tcti_libtpms,
                     TPMLIB_GetState,
                     TPMLIB_STATE_VOLATILE,
                     &volatile_buf,
                     &volatile_buf_len);

    /* check if enough memory is allocated first */
    size = sizeof(uint32_t) + permanent_buf_len + sizeof(uint32_t) + volatile_buf_len;
    rc = tcti_libtpms_ensure_state_len(tcti_libtpms, size);
    if (rc != TSS2_RC_SUCCESS) {
        goto cleanup_volatile;
    }

    /* write permanent buffer length (big endian) */
    size = sizeof(permanent_buf_len_be);
    permanent_buf_len_be = htonl(permanent_buf_len);
    memcpy(tcti_libtpms->state_mmap + offset,
           &permanent_buf_len_be,
           size);
    offset += size;

    /* write permanent buffer */
    size = permanent_buf_len;
    memcpy(tcti_libtpms->state_mmap + offset,
           permanent_buf,
           size);
    offset += size;

    /* write volatile buffer length (big endian) */
    size = sizeof(volatile_buf_len_be);
    volatile_buf_len_be = htonl(volatile_buf_len);
    memcpy(tcti_libtpms->state_mmap + offset,
           &volatile_buf_len_be,
           size);
    offset += size;

    /* write volatile buffer */
    size = volatile_buf_len;
    memcpy(tcti_libtpms->state_mmap + offset,
           volatile_buf,
           size);
    offset += size;

    tcti_libtpms->state_len = offset;

    rc = TPM2_RC_SUCCESS;

cleanup_volatile:
    free(volatile_buf);

cleanup_permanent:
    free(permanent_buf);

fail:
    return rc;
}

/*
 * Load the libtpms state from the mapped memory (state file). This has to be
 * called after TPMLIB_ChooseTPMVersion and before TPMLIB_MainInit.
 */
static TSS2_RC
tcti_libtpms_load_state(TSS2_TCTI_LIBTPMS_CONTEXT *tcti_libtpms)
{
    TSS2_RC rc;
    int ret;
    unsigned char *permanent_buf, *volatile_buf;
    uint32_t permanent_buf_len, volatile_buf_len;
    size_t offset = 0;

    /* if no/empty state file, skip loading */
    if (tcti_libtpms->state_path == NULL || tcti_libtpms->state_len == 0) {
        LOG_DEBUG("No/empty state file found. Skip loading state file.");
        return TPM2_RC_SUCCESS;
    }
    LOG_DEBUG("Loading from state file: %s", tcti_libtpms->state_path);

    tcti_libtpms->state_len = 0;

    /* permanent buffer length (big endian) */
    memcpy(&permanent_buf_len, tcti_libtpms->state_mmap, sizeof(permanent_buf_len));
    permanent_buf_len = ntohl(permanent_buf_len);
    offset += sizeof(permanent_buf_len);

    /* permanent buffer */
    permanent_buf = (unsigned char *) tcti_libtpms->state_mmap + offset;
    offset += permanent_buf_len;

    /* volatile buffer length (big endian) */
    memcpy(&volatile_buf_len, tcti_libtpms->state_mmap + offset, sizeof(volatile_buf_len));
    volatile_buf_len = ntohl(volatile_buf_len);
    offset += sizeof(volatile_buf_len);

    /* volatile buffer */
    volatile_buf = (unsigned char *) tcti_libtpms->state_mmap + offset;
    offset += volatile_buf_len;

    LIBTPMS_API_CALL(fail, tcti_libtpms, TPMLIB_SetState, TPMLIB_STATE_PERMANENT,
                                                          permanent_buf,
                                                          permanent_buf_len);
    LIBTPMS_API_CALL(fail, tcti_libtpms, TPMLIB_SetState, TPMLIB_STATE_VOLATILE,
                                                          volatile_buf,
                                                          volatile_buf_len);

    tcti_libtpms->state_len = offset;

    rc = TPM2_RC_SUCCESS;

fail:
    return rc;
}

/*
 * This function wraps the "up-cast" of the opaque TCTI context type to the
 * type for the mssim TCTI context. If passed a NULL context the function
 * returns a NULL ptr. The function doesn't check magic number anymore
 * It should checked by the appropriate tcti_common_checks.
 */
static TSS2_TCTI_LIBTPMS_CONTEXT*
tcti_libtpms_context_cast(TSS2_TCTI_CONTEXT *tcti_ctx)
{
    if (tcti_ctx == NULL)
        return NULL;

    return (TSS2_TCTI_LIBTPMS_CONTEXT*) tcti_ctx;
}

/*
 * This function down-casts the libtpms TCTI context to the common context
 * defined in the tcti-common module.
 */
static TSS2_TCTI_COMMON_CONTEXT*
tcti_libtpms_down_cast(TSS2_TCTI_LIBTPMS_CONTEXT *tcti_libtpms)
{
    if (tcti_libtpms == NULL) {
        return NULL;
    }
    return &tcti_libtpms->common;
}

/*
 * Transmits and gets the response. The response buffer was allocated by
 * libtpms, is referenced by the libtpms TCTI context and needs to be freed once
 * it is not needed anymore (i.e. at the end of tcti_libtpms_receive()).
 */
TSS2_RC
tcti_libtpms_transmit(
    TSS2_TCTI_CONTEXT *tcti_ctx,
    size_t size,
    const uint8_t *cmd_buf)
{
    TSS2_TCTI_LIBTPMS_CONTEXT *tcti_libtpms = tcti_libtpms_context_cast(tcti_ctx);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_libtpms_down_cast(tcti_libtpms);
    tpm_header_t header;
    TSS2_RC rc;
    TPM_RESULT ret;

    rc = tcti_common_transmit_checks(tcti_common, cmd_buf, TCTI_LIBTPMS_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }
    rc = header_unmarshal(cmd_buf, &header);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }
    if (header.size != size) {
        LOG_ERROR("Buffer size parameter: %zu, and TPM2 command header size "
                  "field: %" PRIu32 " disagree.", size, header.size);
        return TSS2_TCTI_RC_BAD_VALUE;
    }

    LOGBLOB_DEBUG(cmd_buf, size, "Sending command with TPM_CC 0x%" PRIx32, header.size);
    LIBTPMS_API_CALL(fail, tcti_libtpms, TPMLIB_Process, &tcti_libtpms->response_buffer,
                                                         (uint32_t *) &tcti_libtpms->response_len,
                                                         (uint32_t *) &tcti_libtpms->response_buffer_len,
                                                         (uint8_t *) cmd_buf,
                                                         size);
    rc = tcti_libtpms_store_state(tcti_libtpms);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Failed to store state file");
        return TSS2_TCTI_RC_IO_ERROR;
    }

    tcti_common->state = TCTI_STATE_RECEIVE;

    return TSS2_RC_SUCCESS;

fail:
    return TSS2_TCTI_RC_IO_ERROR;
}

TSS2_RC
tcti_libtpms_cancel(
    TSS2_TCTI_CONTEXT *tctiContext)
{
    (void) (tctiContext);
    return TSS2_TCTI_RC_NOT_IMPLEMENTED;
}

TSS2_RC
tcti_libtpms_set_locality(
    TSS2_TCTI_CONTEXT *tctiContext,
    uint8_t locality)
{
    TSS2_TCTI_LIBTPMS_CONTEXT *tcti_libtpms = tcti_libtpms_context_cast(tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_libtpms_down_cast(tcti_libtpms);
    TSS2_RC rc;

    rc = tcti_common_set_locality_checks(tcti_common, TCTI_LIBTPMS_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    tcti_common->locality = locality;
    return TSS2_RC_SUCCESS;
}

TSS2_RC
tcti_libtpms_get_poll_handles(
    TSS2_TCTI_CONTEXT *tctiContext,
    TSS2_TCTI_POLL_HANDLE *handles,
    size_t *num_handles)
{
    (void)(tctiContext);
    (void)(handles);
    (void)(num_handles);
    return TSS2_TCTI_RC_NOT_IMPLEMENTED;
}

void
tcti_libtpms_finalize(
    TSS2_TCTI_CONTEXT *tctiContext)
{
    int ret;
    TSS2_TCTI_LIBTPMS_CONTEXT *tcti_libtpms = tcti_libtpms_context_cast(tctiContext);

    if (tcti_libtpms == NULL) {
        return;
    }

    tcti_libtpms->TPMLIB_Terminate();

    /* close libtpms library handle */
    dlclose(tcti_libtpms->libtpms);

    if (tcti_libtpms->state_mmap != NULL) {
        /* unmap memory (may be backed by a state file) */
        munmap(tcti_libtpms->state_mmap, tcti_libtpms->state_mmap_len);
    }

    if (tcti_libtpms->state_path != NULL) {
        /* truncate state file to its real size */
        ret = truncate(tcti_libtpms->state_path, tcti_libtpms->state_len);
        if (ret != 0) {
            LOG_WARNING("truncate failed on file %s: %s",
                        tcti_libtpms->state_path,
                        strerror(errno));
        }
    }

    if (tcti_libtpms->state_path != NULL) {
        free(tcti_libtpms->state_path);
    }

    if (tcti_libtpms->response_buffer) {
        free(tcti_libtpms->response_buffer);
    }
}

TSS2_RC
tcti_libtpms_receive(
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *response_size,
    unsigned char *response_buffer,
    int32_t timeout)
{
#ifdef TEST_FAPI_ASYNC
    /* Used for simulating a timeout. */
    static int wait = 0;
#endif

    TSS2_TCTI_LIBTPMS_CONTEXT *tcti_libtpms = tcti_libtpms_context_cast(tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_libtpms_down_cast(tcti_libtpms);
    TSS2_RC rc;

    rc = tcti_common_receive_checks(tcti_common, response_size, TCTI_LIBTPMS_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    if (timeout != TSS2_TCTI_TIMEOUT_BLOCK) {
        LOG_TRACE("Asynchronous I/O not actually implemented.");
#ifdef TEST_FAPI_ASYNC
        if (wait < 1) {
            LOG_TRACE("Simulating Async by requesting another invocation.");
            wait += 1;
            return TSS2_TCTI_RC_TRY_AGAIN;
        } else {
            LOG_TRACE("Sending the actual result.");
            wait = 0;
        }
#endif /* TEST_FAPI_ASYNC */
    }

    if (response_buffer == NULL) {
        *response_size = tcti_libtpms->response_len;
        return TSS2_RC_SUCCESS;
    }

    if (*response_size < tcti_libtpms->response_len) {
        *response_size = tcti_libtpms->response_len;
        return TSS2_TCTI_RC_INSUFFICIENT_BUFFER;
    }
    *response_size = tcti_libtpms->response_len;

    memcpy(response_buffer, tcti_libtpms->response_buffer, tcti_libtpms->response_len);

    LOGBLOB_DEBUG(response_buffer, *response_size, "Response received:");

    free(tcti_libtpms->response_buffer);
    tcti_libtpms->response_buffer = NULL;
    tcti_libtpms->response_buffer_len = 0;
    tcti_libtpms->response_len = 0;

    tcti_common->state = TCTI_STATE_TRANSMIT;

    return TSS2_RC_SUCCESS;
}

static void
tcti_libtpms_init_context_data(TSS2_TCTI_COMMON_CONTEXT *tcti_common)
{
    TSS2_TCTI_MAGIC (tcti_common) = TCTI_LIBTPMS_MAGIC;
    TSS2_TCTI_VERSION (tcti_common) = TCTI_VERSION;
    TSS2_TCTI_TRANSMIT (tcti_common) = tcti_libtpms_transmit;
    TSS2_TCTI_RECEIVE (tcti_common) = tcti_libtpms_receive;
    TSS2_TCTI_FINALIZE (tcti_common) = tcti_libtpms_finalize;
    TSS2_TCTI_CANCEL (tcti_common) = tcti_libtpms_cancel;
    TSS2_TCTI_GET_POLL_HANDLES (tcti_common) = tcti_libtpms_get_poll_handles;
    TSS2_TCTI_SET_LOCALITY (tcti_common) = tcti_libtpms_set_locality;
    TSS2_TCTI_MAKE_STICKY (tcti_common) = tcti_make_sticky_not_implemented;
    tcti_common->state = TCTI_STATE_TRANSMIT;
    memset(&tcti_common->header, 0, sizeof(tcti_common->header));
}

TSS2_RC
tcti_libtpms_dl(TSS2_TCTI_LIBTPMS_CONTEXT *tcti_libtpms)
{
    const char *names[] = {"libtpms.so", "libtpms.so.0"};

    for (size_t i = 0; i < ARRAY_LEN(names); i++) {
        tcti_libtpms->libtpms = dlopen(names[i], RTLD_LAZY | RTLD_LOCAL);
        if (tcti_libtpms->libtpms != NULL) {
            break;
        }
    }
    if (tcti_libtpms->libtpms == NULL) {
        LOG_ERROR("Could not load libtpms library: %s", dlerror());
        return TSS2_TCTI_RC_GENERAL_FAILURE;
    }

    tcti_libtpms->TPMLIB_ChooseTPMVersion = dlsym(tcti_libtpms->libtpms, "TPMLIB_ChooseTPMVersion");
    if (tcti_libtpms->TPMLIB_ChooseTPMVersion == NULL) {
        LOG_ERROR("Could not resolve libtpms symbol TPMLIB_ChooseTPMVersion(): %s", dlerror());
        goto cleanup_dl;
    }

    tcti_libtpms->TPMLIB_RegisterCallbacks = dlsym(tcti_libtpms->libtpms, "TPMLIB_RegisterCallbacks");
    if (tcti_libtpms->TPMLIB_RegisterCallbacks == NULL) {
        LOG_ERROR("Could not resolve libtpms symbol TPMLIB_RegisterCallbacks(): %s", dlerror());
        goto cleanup_dl;
    }

    tcti_libtpms->TPMLIB_GetState = dlsym(tcti_libtpms->libtpms, "TPMLIB_GetState");
    if (tcti_libtpms->TPMLIB_GetState == NULL) {
        LOG_ERROR("Could not resolve libtpms symbol TPMLIB_GetState(): %s", dlerror());
        goto cleanup_dl;
    }

    tcti_libtpms->TPMLIB_MainInit = dlsym(tcti_libtpms->libtpms, "TPMLIB_MainInit");
    if (tcti_libtpms->TPMLIB_MainInit == NULL) {
        LOG_ERROR("Could not resolve libtpms symbol TPMLIB_MainInit(): %s", dlerror());
        goto cleanup_dl;
    }

    tcti_libtpms->TPMLIB_Process = dlsym(tcti_libtpms->libtpms, "TPMLIB_Process");
    if (tcti_libtpms->TPMLIB_Process == NULL) {
        LOG_ERROR("Could not resolve libtpms symbol TPMLIB_Process(): %s", dlerror());
        goto cleanup_dl;
    }

    tcti_libtpms->TPMLIB_SetState = dlsym(tcti_libtpms->libtpms, "TPMLIB_SetState");
    if (tcti_libtpms->TPMLIB_SetState == NULL) {
        LOG_ERROR("Could not resolve libtpms symbol TPMLIB_SetState(): %s", dlerror());
        goto cleanup_dl;
    }

    tcti_libtpms->TPMLIB_Terminate = dlsym(tcti_libtpms->libtpms, "TPMLIB_Terminate");
    if (tcti_libtpms->TPMLIB_Terminate == NULL) {
        LOG_ERROR("Could not resolve libtpms symbol TPMLIB_Terminate(): %s", dlerror());
        goto cleanup_dl;
    }

    return TPM2_RC_SUCCESS;

cleanup_dl:
    dlclose(tcti_libtpms->libtpms);
    return TSS2_TCTI_RC_GENERAL_FAILURE;
}

/****************** libtpms callbacks ******************
 * Override the libtpms callbacks. This is needed to implement localities and to
 * prevent the NVChip file from being created. The other callbacks are
 * implemented as per advice from the libtpms man pages and/or as a placeholder
 * for future features.
 *
 * Using tcti_libtpms_get_current_tcti(), one can retrieve the currently active
 * libtpms TCTI instance.
 */

TPM_RESULT
tcti_libtpms_cb_nvram_init(void)
{
    LOG_TRACE("tcti-libtpms callback nvram_init() called.");

    return TPM_SUCCESS;
}

TPM_RESULT
tcti_libtpms_cb_nvram_loaddata(
    unsigned char **data MAYBE_UNUSED,
    uint32_t *length MAYBE_UNUSED,
    uint32_t tpm_number MAYBE_UNUSED,
    const char *name MAYBE_UNUSED)
{
    LOG_TRACE("tcti-libtpms callback nvram_loaddata() called: "
              "data=0x%" PRIxPTR ", "
              "length=0x%" PRIxPTR ", "
              "tpm_number=%" PRIu32 ", "
              "name=%s",
               (uintptr_t) data, (uintptr_t) length, tpm_number, name);

    return TPM_RETRY;
}

TPM_RESULT
tcti_libtpms_cb_nvram_storedata(
    const unsigned char *data MAYBE_UNUSED,
    uint32_t length MAYBE_UNUSED,
    uint32_t tpm_number MAYBE_UNUSED,
    const char *name MAYBE_UNUSED)
{
    LOG_TRACE("tcti-libtpms callback nvram_storedata() called: "
              "data=0x%" PRIxPTR ", "
              "length=%" PRIu32 ", "
              "tpm_number=%" PRIu32 ", "
              "name=%s",
               (uintptr_t) data, length, tpm_number, name);

    return TPM_SUCCESS;
}

TPM_RESULT
tcti_libtpms_cb_nvram_deletename(
    uint32_t tpm_number MAYBE_UNUSED,
    const char *name MAYBE_UNUSED,
    TPM_BOOL must_exist MAYBE_UNUSED)
{
    LOG_TRACE("tcti-libtpms callback nvram_deletename() called: "
              "tpm_number=%" PRIu32 ", "
              "name=%s, "
              "must_exist=%d",
               tpm_number, name, must_exist);

    LOG_ERROR("Not implemented");

    return TPM_FAIL;
}

TPM_RESULT
tcti_libtpms_cb_io_init(void)
{
    LOG_TRACE("tcti-libtpms callback io_init() called.");

    return TPM_SUCCESS;
}

TPM_RESULT
tcti_libtpms_cb_io_getlocality(
    TPM_MODIFIER_INDICATOR *locality_modifer,
    uint32_t tpm_number MAYBE_UNUSED)
{
    TSS2_TCTI_COMMON_CONTEXT *tcti_common;

    LOG_TRACE("tcti-libtpms callback io_getlocality() called: "
              "locality_modifer=0x%" PRIxPTR ", "
              "tpm_number=%" PRIu32,
               (uintptr_t) locality_modifer, tpm_number);

    if (locality_modifer == NULL) {
        return TPM_FAIL;
    }

    if (current_tcti_libtpms == NULL) {
        LOG_ERROR("No TCTI registered as currently active before libtpms API call.");
        return TPM_FAIL;
    }
    tcti_common = tcti_libtpms_down_cast(current_tcti_libtpms);
    *locality_modifer = tcti_common->locality;

    return TPM_SUCCESS;
}

TPM_RESULT
tcti_libtpms_cb_io_getphysicalpresence(
    TPM_BOOL *physical_presence MAYBE_UNUSED,
    uint32_t tpm_number MAYBE_UNUSED)
{
    LOG_TRACE("tcti-libtpms callback io_getphysicalpresence() called: "
              "physical_presence=0x%" PRIxPTR ", "
              "tpm_number=%" PRIu32,
               (uintptr_t) physical_presence, tpm_number);

    LOG_ERROR("Not implemented");

    return TPM_FAIL;
}
/*************** end: libtpms callbacks ****************/

TSS2_RC
Tss2_Tcti_Libtpms_Init(
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    const char *conf)
{
    TSS2_TCTI_LIBTPMS_CONTEXT *tcti_libtpms = (TSS2_TCTI_LIBTPMS_CONTEXT*)tctiContext;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_libtpms_down_cast(tcti_libtpms);
    TSS2_RC rc;
    TPM_RESULT ret;
    (void)(conf);

    LOG_TRACE("tctiContext: 0x%" PRIxPTR ", size: 0x%" PRIxPTR ", conf: %s",
               (uintptr_t)tctiContext, (uintptr_t)size, conf);
    if (size == NULL) {
        return TSS2_TCTI_RC_BAD_VALUE;
    }
    if (tctiContext == NULL) {
        *size = sizeof(TSS2_TCTI_LIBTPMS_CONTEXT);
        return TSS2_RC_SUCCESS;
    }

    tcti_libtpms_init_context_data(tcti_common);

    rc = tcti_libtpms_set_locality(tctiContext, 0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_WARNING ("Could not set locality: 0x%" PRIx32, rc);
        return rc;
    }

    rc = tcti_libtpms_dl(tcti_libtpms);
    if (rc != TPM2_RC_SUCCESS) {
        return rc;
    }
    LOG_TRACE("Successfully loaded libtpms and resolved symbols.");

    /* copy state path given in conf */
    if (conf == NULL || strlen(conf) == 0) {
        tcti_libtpms->state_path = NULL;
    } else {
        tcti_libtpms->state_path = strdup(conf);
        if (tcti_libtpms->state_path == NULL) {
            LOG_ERROR("Out of memory.");
            rc = TSS2_TCTI_RC_MEMORY;
            goto cleanup_dl;
        }
    }

    rc = tcti_libtpms_map_state_file(tcti_libtpms);
    if (rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("Could not create and map state file.");
        goto cleanup_state_path;
    }
    LOG_TRACE("Successfully opened memory-mapped libtpms state file: %s",
                tcti_libtpms->state_path);

    struct libtpms_callbacks callbacks = {
        .sizeOfStruct               = sizeof(struct libtpms_callbacks),
        .tpm_nvram_init             = tcti_libtpms_cb_nvram_init,
        .tpm_nvram_loaddata         = tcti_libtpms_cb_nvram_loaddata,
        .tpm_nvram_storedata        = tcti_libtpms_cb_nvram_storedata,
        .tpm_nvram_deletename       = tcti_libtpms_cb_nvram_deletename,
        .tpm_io_init                = tcti_libtpms_cb_io_init,
        .tpm_io_getlocality         = tcti_libtpms_cb_io_getlocality,
        .tpm_io_getphysicalpresence = tcti_libtpms_cb_io_getphysicalpresence
    };
    LIBTPMS_API_CALL(cleanup_state_mmap, tcti_libtpms, TPMLIB_ChooseTPMVersion, TPMLIB_TPM_VERSION_2);
    LIBTPMS_API_CALL(cleanup_state_mmap, tcti_libtpms, TPMLIB_RegisterCallbacks, &callbacks);
    rc = tcti_libtpms_load_state(tcti_libtpms);
    if (rc != TPM2_RC_SUCCESS) {
        goto cleanup_state_mmap;
    }
    LIBTPMS_API_CALL(cleanup_state_mmap, tcti_libtpms, TPMLIB_MainInit);

    tcti_libtpms->response_buffer = NULL;
    tcti_libtpms->response_buffer_len = 0;
    tcti_libtpms->response_len = 0;

    return TSS2_RC_SUCCESS;

cleanup_state_mmap:
    if (tcti_libtpms->state_path != NULL) {
        munmap(tcti_libtpms->state_mmap, tcti_libtpms->state_mmap_len);
    }

cleanup_state_path:
    if (tcti_libtpms->state_path != NULL) {
        free(tcti_libtpms->state_path);
    }

cleanup_dl:
    dlclose(tcti_libtpms->libtpms);

    return rc;
}

/* public info structure */
const TSS2_TCTI_INFO tss2_tcti_info = {
    .version = TCTI_VERSION,
    .name = "tcti-libtpms",
    .description = "TCTI module for communication with the libtpms library.",
    .config_help = "Path to the state file. NULL for no state file.",
    .init = Tss2_Tcti_Libtpms_Init,
};

const TSS2_TCTI_INFO *
Tss2_Tcti_Info(void)
{
    return &tss2_tcti_info;
}
