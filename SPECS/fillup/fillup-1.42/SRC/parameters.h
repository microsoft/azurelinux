
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to S.u.S.E. GmbH Fuerth (c) 1998                                */
/*                                                                            */
/* Time-stamp:                                                                */
/* Project:    fillup                                                         */
/* Module:     parameters                                                     */
/* Filename:   parameters.h                                                   */
/* Author:     Joerg Dippel (jd)                                              */
/* Description:                                                               */
/*                                                                            */
/*     export interface for parameter administration                          */
/*                                                                            */
/*----------------------------------------------------------------------------*/

#ifndef     __PARAMETERS_H__
#define     __PARAMETERS_H__

/*--------------------------------- IMPORTS ----------------------------------*/

#include <stdio.h>

#include "portab.h"
#include "parameters.h"
#include "services.h"

/*---------------------------------- TYPES -----------------------------------*/

typedef enum
{
    Delimiter,
    CommentLines,
    Verbose,
    Put,
    Get,
    Maintain,
    Exchange,
    Remove,
    Parameters,
    Quiet,
    Suppress,
    CommentMarker,
    QuotingMarker,
    ForbiddenFile,
    Help,
    IgnoreEOF,
    IgnoreDefinites,
    TrailingComment,
    Version,
    NoMetadata,
    DebuggingLogfile,
    DebuggingVariableName,
    BaseFile,
    AdditionalFile,      /* NewFile or DefinitionFile */
    OutputFile
} ParameterSpecification_t;

/*-------------------------------- FUNCTIONS ---------------------------------*/

void
initializeParameters
(
    void
);

void
setStringParameter
(
    ParameterSpecification_t    parameterType,     /* in */
    const char                * parameterId        /* in */
);

void
setNumericParameter
(
    ParameterSpecification_t    parameterType,     /* in */
    const char                * parameterId        /* in */
);

void
setSimpleParameter
(
    ParameterSpecification_t    parameterType      /* in */
);

BOOLEAN
queryParameter
(
    ParameterSpecification_t    parameterType      /* in */
);

void
queryStringParameter
(
    ParameterSpecification_t    parameterType,     /* in */
    char                     ** parameterString   /* out */
);

void
displayUsageInformation
(
    void
);

void
displayParameters
(
    void
);

Service_t
instantiateParameters
(
    void
);

/*----------------------------------------------------------------------------*/

#endif  /*  __PARAMETERS_H__ */
