
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to S.u.S.E. GmbH Fuerth (c) 1996                                */
/*                                                                            */
/* Time-stamp:                                                                */
/* Project:    fillup                                                         */
/* Module:     file                                                           */
/* Filename:   file.h                                                         */
/* Author:     Joerg Dippel (jd )                                             */
/* Description:                                                               */
/*                                                                            */
/*             export interface                                               */
/*                                                                            */
/*----------------------------------------------------------------------------*/

#ifndef __FILE_H__
#define __FILE_H__

/*--------------------------------- IMPORTS ----------------------------------*/

#include "parameters.h"

/*---------------------------------- TYPES -----------------------------------*/

typedef enum
{
    FileOperationsSuccessful,
    FileOperationsFailed
} File_t;

/*-------------------------------- FUNCTIONS ---------------------------------*/

File_t
readFile 
(
    ParameterSpecification_t    fileSpecifier, /* in */
    const char                * filename       /* in */
);

/*----------------------------------------------------------------------------*/

#endif  /* __FILE_H__ */

