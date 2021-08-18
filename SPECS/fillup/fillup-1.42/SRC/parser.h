
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to S.u.S.E. GmbH Fuerth (c) 1998                                */
/*                                                                            */
/* Time-stamp:                                                                */
/* Project:    fillup                                                         */
/* Module:     parser                                                         */
/* Filename:   parser.h                                                       */
/* Author:     Joerg Dippel (jd)                                              */
/* Description:                                                               */
/*                                                                            */
/*     export interface                                                       */
/*                                                                            */
/*----------------------------------------------------------------------------*/

#ifndef    __PARSER_H__
#define    __PARSER_H__

/*--------------------------------- IMPORTS ----------------------------------*/

#include <stdio.h>

#include "parameters.h"

/*------------------------------- FUNCTIONS ----------------------------------*/

void
associateBuffer
(   
    ParameterSpecification_t    parameterType,     /* in */
    long                        bufferLength,      /* in */
    char                     ** buffer             /* in */
);

void
displayVerboseString
( 
    char                       * verboseString  /* in */
);

void
displayVerboseBuffer
( 
    char      * verboseBuffer,               /* in */
    long        verboseLength                /* in */
);

void
startParser
(
    void
);

void
dumpBasefile
(
    FILE          * filePointer               /* in */
);

void
dumpAddfile
(
    FILE          * filePointer               /* in */
);

/*----------------------------------------------------------------------------*/

#endif  /* __PARSER_H__ */
