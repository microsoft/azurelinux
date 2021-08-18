
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to S.u.S.E. GmbH Fuerth (c) 1998                                */
/*                                                                            */
/* Time-stamp:                                                                */
/* Project:    fillup                                                         */
/* Module:     metadata                                                       */
/* Filename:   metadata.h                                                     */
/* Author:     Joerg Dippel (jd)                                              */
/* Description:                                                               */
/*                                                                            */
/*     export interface for metadata                                          */
/*                                                                            */
/*----------------------------------------------------------------------------*/

#ifndef __METADATA_H__
#define __METADATA_H__

/*--------------------------------- IMPORTS ----------------------------------*/

#include "variableblock.h"

/*---------------------------------- TYPES -----------------------------------*/

typedef enum
{
    Metadata_Path,
    Metadata_Description,
    Metadata_Type,
    Metadata_Default,
    Metadata_Config,
    Metadata_ServiceReload,
    Metadata_ServiceRestart,
    Metadata_Command,
    Metadata_PreSaveCommand,
    Metadata_Number
} MetadataKeyword_t;

typedef struct MetadataVariable
{
    char                    * beginOfMetadataVariable;
    long                      lengthOfMetadataVariable;
} MetadataVariable_t;

typedef struct Metadata
{
    char                    * beginOfMetadataBlock;
    long                      lengthOfMetadata;
    MetadataVariable_t        variable[ Metadata_Number ];
} Metadata_t;

/*------------------- FUNCTION DECLARATIONS (PROTOTYPES) ---------------------*/

void
setMetadataInfo
(
    VariableBlock_t            * variableBlock    /* in */
);

void
printMetadataInfo
(
    VariableBlock_t            * variableBlock    /* in */
);

void
writeMetadataInfo
(
    VariableBlock_t            * variableBlock,   /* in */
    FILE                       * filePointera     /* in */
);

/*----------------------------------------------------------------------------*/

#endif  /* __METADATA_H__ */
