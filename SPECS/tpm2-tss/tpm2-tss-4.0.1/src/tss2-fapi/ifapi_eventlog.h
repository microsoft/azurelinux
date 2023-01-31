/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef IFAPI_EVENTLOG_H
#define IFAPI_EVENTLOG_H

#include <json-c/json.h>

#include "tss2_tpm2_types.h"
#include "ifapi_io.h"
#include "efi_event.h"
#include "ifapi_ima_eventlog.h"
#include "ifapi_eventlog_system.h"

#define CONTENT_TYPE "content_type"
#define CONTENT "content"

/** Type of event
 */
typedef UINT32 IFAPI_EVENT_TYPE;
#define IFAPI_TSS_EVENT_TAG            2    /**< Tag for TSS FAPI events */
#define IFAPI_IMA_EVENT_TAG            3    /**< Tag for IMA type "ima" */
#define IFAPI_IMA_NG_EVENT_TAG         4    /**< Tag for IMA type "ima-ng" */
#define IFAPI_IMA_SIG_EVENT_TAG        5    /**< Tag for IMT type "sig"*/
#define IFAPI_PC_CLIENT                6    /**< Tag for PC_Client firmware events */
#define IFAPI_CEL_TAG                  8    /**< Tag for comment event log management
                                                 event. */
/* Definition of TPMI_CELMGTTYPE Type */
typedef UINT32 TPMI_CELMGTTYPE;
#define CEL_VERSION  1
#define FIRMWARE_END 2
#define CEL_TIMESTAMP 80
#define STATE_TRANS 81

/* Structures of canonical event log format. */

/* Definition of TPMS_CEL_VERSION Structure */
typedef struct {
    UINT16 major;     /* The major version */
    UINT16 minor;     /* The minor version */
} TPMS_CEL_VERSION;

/* Definition of TPMU_CAPABILITIES Union <OUT> */
typedef union {
    TPMS_CEL_VERSION cel_version;
    TPMS_EMPTY firmware_end;
    UINT64 cel_timestamp;
} TPMU_CELMGT;

/* Definition of TPMS_EVENT_CELMGT Structure*/
typedef struct {
    TPMI_CELMGTTYPE type;      /* type of the cel event structure */
    TPMU_CELMGT data;          /* the type-specific cel event information */
} TPMS_EVENT_CELMGT;

/** TSS event information
 */
typedef struct {
    TPM2B_EVENT                                    data;    /**< The event data */
    char                                         *event;    /**< TSS event information */
} IFAPI_TSS_EVENT;

/** Type for representing sub types of FAPI events
 */
typedef union {
    IFAPI_TSS_EVENT                           tss_event;    /**< TSS event information */
    IFAPI_IMA_EVENT                           ima_event;    /**< IMA event information */
    IFAPI_FIRMWARE_EVENT                 firmware_event;    /**< Firmware event information */
    TPMS_EVENT_CELMGT                         cel_event;    /**< Cononical eventlol management
                                                                 event. */
} IFAPI_EVENT_UNION;

/** Type for representing a FAPI event
 */
typedef struct IFAPI_EVENT {
    UINT32                                       recnum;    /**< Number of event */
    TPM2_HANDLE                                     pcr;    /**< PCR register */
    TPML_DIGEST_VALUES                          digests;    /**< The digest list of the event */
    IFAPI_EVENT_TYPE                       content_type;    /**< Selector for object type */
    IFAPI_EVENT_UNION                           content;    /**< The event data */
    bool                                         verify;    /**< Switch whether digest can be
                                                                 verified. */
} IFAPI_EVENT;

enum IFAPI_EVENTLOG_STATE {
    IFAPI_EVENTLOG_STATE_INIT = 0,
    IFAPI_EVENTLOG_STATE_READING,
    IFAPI_EVENTLOG_STATE_APPENDING,
    IFAPI_EVENTLOG_STATE_WRITING
};

typedef struct IFAPI_EVENTLOG {
    enum IFAPI_EVENTLOG_STATE state;
    char *log_dir;
    const char *firmware_log_file;
    const char *ima_log_file;
    struct IFAPI_EVENT event;
    TPM2_HANDLE pcrList[TPM2_MAX_PCRS];
    size_t pcrListSize;
    size_t pcrListIdx;
    json_object *log;
} IFAPI_EVENTLOG;

TSS2_RC
ifapi_eventlog_initialize(
    IFAPI_EVENTLOG *eventlog,
    const char *log_dir,
    const char *firmware_log_file,
    const char *ima_log_file);

TSS2_RC
ifapi_eventlog_get_async(
    IFAPI_EVENTLOG *eventlog,
    IFAPI_IO *io,
    const TPM2_HANDLE *pcrList,
    size_t pcrListSize);

TSS2_RC
ifapi_eventlog_get_finish(
    IFAPI_EVENTLOG *eventlog,
    IFAPI_IO *io,
    char **log);

TSS2_RC
ifapi_eventlog_append_check(
    IFAPI_EVENTLOG *eventlog,
    IFAPI_IO *io);

TSS2_RC
ifapi_eventlog_append_finish(
    IFAPI_EVENTLOG *eventlog,
    IFAPI_IO *io,
    const IFAPI_EVENT *event);

void
ifapi_cleanup_event(
    IFAPI_EVENT * event);

#endif /* IFAPI_EVENTLOG_H */
