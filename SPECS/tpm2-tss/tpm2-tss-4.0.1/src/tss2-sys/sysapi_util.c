/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2015-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <string.h>

#include "tss2_mu.h"
#include "sysapi_util.h"
#include "util/tss2_endian.h"
#define LOGMODULE sys
#include "util/log.h"

void InitSysContextFields(_TSS2_SYS_CONTEXT_BLOB *ctx)
{
    ctx->decryptAllowed = 0;
    ctx->encryptAllowed = 0;
    ctx->decryptNull = 0;
    ctx->authAllowed = 0;
    ctx->nextData = 0;
}

void InitSysContextPtrs(
    _TSS2_SYS_CONTEXT_BLOB *ctx,
    size_t contextSize)
{
    ctx->cmdBuffer = (UINT8 *)ctx + sizeof(_TSS2_SYS_CONTEXT_BLOB);
    ctx->maxCmdSize = contextSize - sizeof(_TSS2_SYS_CONTEXT_BLOB);
}

UINT32 GetCommandSize(_TSS2_SYS_CONTEXT_BLOB *ctx)
{
    return BE_TO_HOST_32(req_header_from_cxt(ctx)->commandSize);
}

TSS2_RC CopyCommandHeader(_TSS2_SYS_CONTEXT_BLOB *ctx, TPM2_CC commandCode)
{
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    ctx->nextData = 0;

    rval = Tss2_MU_TPM2_ST_Marshal(TPM2_ST_NO_SESSIONS, ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    req_header_from_cxt(ctx)->commandCode = HOST_TO_BE_32(commandCode);
    ctx->nextData = sizeof(TPM20_Header_In);
    return rval;
}

static int GetNumCommandHandles(TPM2_CC commandCode);
static int GetNumResponseHandles(TPM2_CC commandCode);

TSS2_RC CommonPreparePrologue(
    _TSS2_SYS_CONTEXT_BLOB *ctx,
    TPM2_CC commandCode)
{
    int numCommandHandles;
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    InitSysContextFields(ctx);

    /* Need to check stage here. */
    if (ctx->previousStage != CMD_STAGE_INITIALIZE &&
        ctx->previousStage != CMD_STAGE_RECEIVE_RESPONSE &&
        ctx->previousStage != CMD_STAGE_PREPARE)
        return TSS2_SYS_RC_BAD_SEQUENCE;

    rval = CopyCommandHeader(ctx, commandCode);
    if (rval)
        return rval;

    ctx->commandCode = commandCode;
    ctx->numResponseHandles = GetNumResponseHandles(commandCode);
    ctx->rspParamsSize = (UINT32 *)(ctx->cmdBuffer + sizeof(TPM20_Header_Out) +
                         (GetNumResponseHandles(commandCode) * sizeof(UINT32)));

    numCommandHandles = GetNumCommandHandles(commandCode);
    ctx->cpBuffer = ctx->cmdBuffer + ctx->nextData +
                                     (numCommandHandles * sizeof(UINT32));
    return rval;
}

TSS2_RC CommonPrepareEpilogue(_TSS2_SYS_CONTEXT_BLOB *ctx)
{
    ctx->cpBufferUsedSize = ctx->cmdBuffer + ctx->nextData - ctx->cpBuffer;
    req_header_from_cxt(ctx)->commandSize = HOST_TO_BE_32(ctx->nextData);
    ctx->previousStage = CMD_STAGE_PREPARE;

    return TSS2_RC_SUCCESS;
}

TSS2_RC CommonComplete(_TSS2_SYS_CONTEXT_BLOB *ctx)
{
    UINT32 rspSize;
    TPM2_ST tag;
    size_t next = 0;
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rspSize = BE_TO_HOST_32(resp_header_from_cxt(ctx)->responseSize);

    if(rspSize > ctx->maxCmdSize) {
        return TSS2_SYS_RC_MALFORMED_RESPONSE;
    }

    if (ctx->previousStage != CMD_STAGE_RECEIVE_RESPONSE)
        return TSS2_SYS_RC_BAD_SEQUENCE;

    ctx->nextData = (UINT8 *)ctx->rspParamsSize - ctx->cmdBuffer;

    rval = Tss2_MU_TPM2_ST_Unmarshal(ctx->cmdBuffer,
                                    ctx->maxCmdSize,
                                    &next, &tag);
    if (rval)
        return rval;

    /* Skipping over response params size field */
    if (tag == TPM2_ST_SESSIONS)
        rval = Tss2_MU_UINT32_Unmarshal(ctx->cmdBuffer,
                                        ctx->maxCmdSize,
                                        &ctx->nextData,
                                        NULL);

    return rval;
}

TSS2_RC CommonOneCall(
    _TSS2_SYS_CONTEXT_BLOB *ctx,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray)
{
    TSS2_RC rval;

    if (cmdAuthsArray) {
        rval = Tss2_Sys_SetCmdAuths((TSS2_SYS_CONTEXT *)ctx, cmdAuthsArray);
        if (rval)
            return rval;
    }

    rval = Tss2_Sys_Execute((TSS2_SYS_CONTEXT *)ctx);
    if (rval)
        return rval;

    if (ctx->rsp_header.responseCode)
        return ctx->rsp_header.responseCode;

    if (BE_TO_HOST_16(resp_header_from_cxt(ctx)->tag) ==
            TPM2_ST_SESSIONS && rspAuthsArray)
        rval = Tss2_Sys_GetRspAuths((TSS2_SYS_CONTEXT *)ctx, rspAuthsArray);

    return rval;
}

static int GetNumHandles(TPM2_CC commandCode, bool req)
{
    static const COMMAND_HANDLES commandArray[] =
    {
        { TPM2_CC_Startup, 0, 0 },
        { TPM2_CC_Shutdown, 0, 0 },
        { TPM2_CC_SelfTest, 0, 0 },
        { TPM2_CC_IncrementalSelfTest, 0, 0 },
        { TPM2_CC_GetTestResult, 0, 0 },
        { TPM2_CC_StartAuthSession, 2, 1 },
        { TPM2_CC_PolicyRestart, 1, 0 },
        { TPM2_CC_Create, 1, 0 },
        { TPM2_CC_Load, 1, 1 },
        { TPM2_CC_LoadExternal, 0, 1 },
        { TPM2_CC_ReadPublic, 1, 0 },
        { TPM2_CC_ActivateCredential, 2, 0 },
        { TPM2_CC_MakeCredential, 1, 0 },
        { TPM2_CC_Unseal, 1, 0 },
        { TPM2_CC_ObjectChangeAuth, 2, 0 },
        { TPM2_CC_Duplicate, 2, 0 },
        { TPM2_CC_Rewrap, 2, 0 },
        { TPM2_CC_Import, 1, 0 },
        { TPM2_CC_RSA_Encrypt, 1, 0 },
        { TPM2_CC_RSA_Decrypt, 1, 0 },
        { TPM2_CC_ECDH_KeyGen, 1, 0 },
        { TPM2_CC_ECDH_ZGen, 1, 0 },
        { TPM2_CC_ECC_Parameters, 0, 0 },
        { TPM2_CC_ZGen_2Phase, 1, 0 },
        { TPM2_CC_EncryptDecrypt, 1, 0 },
        { TPM2_CC_EncryptDecrypt2, 1, 0 },
        { TPM2_CC_Hash, 0, 0 },
        { TPM2_CC_HMAC, 1, 0 },
        { TPM2_CC_GetRandom, 0, 0 },
        { TPM2_CC_StirRandom, 0, 0 },
        { TPM2_CC_HMAC_Start, 1, 1 },
        { TPM2_CC_HashSequenceStart, 0, 1 },
        { TPM2_CC_SequenceUpdate, 1, 0 },
        { TPM2_CC_SequenceComplete, 1, 0 },
        { TPM2_CC_EventSequenceComplete, 2, 0 },
        { TPM2_CC_Certify, 2, 0 },
        { TPM2_CC_CertifyCreation, 2, 0 },
        { TPM2_CC_Quote, 1, 0 },
        { TPM2_CC_GetSessionAuditDigest, 3, 0 },
        { TPM2_CC_GetCommandAuditDigest, 2, 0 },
        { TPM2_CC_GetTime, 2, 0 },
        { TPM2_CC_Commit, 1, 0 },
        { TPM2_CC_EC_Ephemeral, 0, 0 },
        { TPM2_CC_VerifySignature, 1, 0 },
        { TPM2_CC_Sign, 1, 0 },
        { TPM2_CC_SetCommandCodeAuditStatus, 1, 0 },
        { TPM2_CC_PCR_Extend, 1, 0 },
        { TPM2_CC_PCR_Event, 1, 0 },
        { TPM2_CC_PCR_Read, 0, 0 },
        { TPM2_CC_PCR_Allocate, 1, 0 },
        { TPM2_CC_PCR_SetAuthPolicy, 1, 0 },
        { TPM2_CC_PCR_SetAuthValue, 1, 0 },
        { TPM2_CC_PCR_Reset, 1, 0 },
        { TPM2_CC_PolicySigned, 2, 0 },
        { TPM2_CC_PolicySecret, 2, 0 },
        { TPM2_CC_PolicyTicket, 1, 0 },
        { TPM2_CC_PolicyOR, 1, 0 },
        { TPM2_CC_PolicyPCR, 1, 0 },
        { TPM2_CC_PolicyLocality, 1, 0 },
        { TPM2_CC_PolicyNV, 3, 0 },
        { TPM2_CC_PolicyNvWritten, 1, 0 },
        { TPM2_CC_PolicyCounterTimer, 1, 0 },
        { TPM2_CC_PolicyCommandCode, 1, 0 },
        { TPM2_CC_PolicyPhysicalPresence, 1, 0 },
        { TPM2_CC_PolicyCpHash, 1, 0 },
        { TPM2_CC_PolicyNameHash, 1, 0 },
        { TPM2_CC_PolicyDuplicationSelect, 1, 0 },
        { TPM2_CC_PolicyAuthorize, 1, 0 },
        { TPM2_CC_PolicyAuthValue, 1, 0 },
        { TPM2_CC_PolicyPassword, 1, 0 },
        { TPM2_CC_PolicyGetDigest, 1, 0 },
        { TPM2_CC_PolicyTemplate, 1, 0 },
        { TPM2_CC_CreatePrimary, 1, 1 },
        { TPM2_CC_HierarchyControl, 1, 0 },
        { TPM2_CC_SetPrimaryPolicy, 1, 0 },
        { TPM2_CC_ChangePPS, 1, 0 },
        { TPM2_CC_ChangeEPS, 1, 0 },
        { TPM2_CC_Clear, 1, 0 },
        { TPM2_CC_ClearControl, 1, 0 },
        { TPM2_CC_HierarchyChangeAuth, 1, 0 },
        { TPM2_CC_DictionaryAttackLockReset, 1, 0 },
        { TPM2_CC_DictionaryAttackParameters, 1, 0 },
        { TPM2_CC_PP_Commands, 1, 0 },
        { TPM2_CC_SetAlgorithmSet, 1, 0 },
        { TPM2_CC_FieldUpgradeStart, 2, 0 },
        { TPM2_CC_FieldUpgradeData, 0, 0 },
        { TPM2_CC_FirmwareRead, 0, 0 },
        { TPM2_CC_ContextSave, 1, 0 },
        { TPM2_CC_ContextLoad, 0, 1 },
        { TPM2_CC_FlushContext, 0, 0 },
        { TPM2_CC_EvictControl, 2, 0 },
        { TPM2_CC_ReadClock, 0, 0 },
        { TPM2_CC_ClockSet, 1, 0 },
        { TPM2_CC_ClockRateAdjust, 1, 0 },
        { TPM2_CC_GetCapability, 0, 0 },
        { TPM2_CC_TestParms, 0, 0 },
        { TPM2_CC_NV_DefineSpace, 1, 0 },
        { TPM2_CC_NV_UndefineSpace, 2, 0 },
        { TPM2_CC_NV_UndefineSpaceSpecial, 2, 0 },
        { TPM2_CC_NV_ReadPublic, 1, 0 },
        { TPM2_CC_NV_Write, 2, 0 },
        { TPM2_CC_NV_Increment, 2, 0 },
        { TPM2_CC_NV_Extend, 2, 0 },
        { TPM2_CC_NV_SetBits, 2, 0 },
        { TPM2_CC_NV_WriteLock, 2, 0 },
        { TPM2_CC_NV_GlobalWriteLock, 1, 0 },
        { TPM2_CC_NV_Read, 2, 0 },
        { TPM2_CC_NV_ReadLock, 2, 0 },
        { TPM2_CC_NV_ChangeAuth, 1, 0 },
        { TPM2_CC_NV_Certify, 3, 0 },
        { TPM2_CC_CreateLoaded, 1, 1 },
        { TPM2_CC_PolicyAuthorizeNV, 3, 0 },
        { TPM2_CC_AC_GetCapability, 1, 0 },
        { TPM2_CC_AC_Send, 3, 0 },
        { TPM2_CC_Policy_AC_SendSelect, 1, 0 },
        { TPM2_CC_ACT_SetTimeout, 1, 0 },
        { TPM2_CC_CertifyX509, 2, 0 }
    };

    uint8_t i;

    for (i = 0; i < sizeof(commandArray) / sizeof(COMMAND_HANDLES); i++) {
        if (commandCode == commandArray[i].commandCode) {
            if (req)
                return commandArray[i].numCommandHandles;
            else
                return commandArray[i].numResponseHandles;
        }
    }

    return 0;
}

static int GetNumCommandHandles(TPM2_CC commandCode)
{
    return GetNumHandles(commandCode, 1);
}

static int GetNumResponseHandles(TPM2_CC commandCode)
{
    return GetNumHandles(commandCode, 0);
}

#ifdef DISABLE_WEAK_CRYPTO
bool IsAlgorithmWeak(TPM2_ALG_ID algorithm, TPM2_KEY_SIZE key_size)
{
    switch (algorithm) {
        case TPM2_ALG_RSA:
            if (key_size < 2048) {
                LOG_ERROR("Error: weak algorithm");
                return true;
            }
        break;
        case TPM2_ALG_AES:
        case TPM2_ALG_SM4:
        case TPM2_ALG_CAMELLIA:
        case TPM2_ALG_SYMCIPHER:
            if (key_size < 128) {
                LOG_ERROR("Error: weak algorithm");
                return true;
            }
        break;
        case TPM2_ALG_SHA1:
            LOG_ERROR("Error: weak algorithm");
            return true;
        break;
    }

    return false;
}

TSS2_RC ValidatePublicTemplate(const TPM2B_PUBLIC *pub)
{
    const TPMT_PUBLIC *tmpl = &pub->publicArea;

    switch (tmpl->type) {
        case TPM2_ALG_RSA:
            if (IsAlgorithmWeak(tmpl->type, tmpl->parameters.rsaDetail.keyBits) ||
                IsAlgorithmWeak(tmpl->parameters.rsaDetail.symmetric.algorithm,
                               tmpl->parameters.rsaDetail.symmetric.keyBits.sym))
                return TSS2_SYS_RC_BAD_VALUE;
        break;
        case TPM2_ALG_ECC:
            if (IsAlgorithmWeak(tmpl->parameters.eccDetail.symmetric.algorithm,
                               tmpl->parameters.eccDetail.symmetric.keyBits.sym))
                return TSS2_SYS_RC_BAD_VALUE;
        break;
        case TPM2_ALG_AES:
        case TPM2_ALG_SM4:
        case TPM2_ALG_CAMELLIA:
        case TPM2_ALG_SYMCIPHER:
            if (IsAlgorithmWeak(tmpl->type,
                               tmpl->parameters.symDetail.sym.keyBits.sym))
                return TSS2_SYS_RC_BAD_VALUE;
        break;
        default:
            if (IsAlgorithmWeak(tmpl->type, 0))
                return TSS2_SYS_RC_BAD_VALUE;

        if (IsAlgorithmWeak(tmpl->nameAlg, 0))
            return TSS2_SYS_RC_BAD_VALUE;

    }
    return TSS2_RC_SUCCESS;
}

TSS2_RC ValidateNV_Public(const TPM2B_NV_PUBLIC *nv_public_info)
{
    const TPMS_NV_PUBLIC *nv_public = &nv_public_info->nvPublic;

    if (IsAlgorithmWeak(nv_public->nameAlg, 0))
        return TSS2_SYS_RC_BAD_VALUE;

    return TSS2_RC_SUCCESS;
}

TSS2_RC ValidateTPML_PCR_SELECTION(const TPML_PCR_SELECTION *pcr_selection)
{

    UINT16 i;

    for (i = 0; i < pcr_selection->count; i++) {
        const TPMS_PCR_SELECTION *selection = &pcr_selection->pcrSelections[i];

        if (IsAlgorithmWeak(selection->hash, 0))
            return TSS2_SYS_RC_BAD_VALUE;
    }

    return TSS2_RC_SUCCESS;
}
#endif
