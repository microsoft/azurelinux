
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to SuSE Linux AG        (c) 2003                                */
/*                                                                            */
/* Project:    fillup                                                         */
/* Module:     validate                                                       */
/* Filename:   validate.h                                                     */
/* Author:     Joerg Dippel (jd )                                             */
/* Description:                                                               */
/*                                                                            */
/*             export interface                                               */
/*                                                                            */
/*----------------------------------------------------------------------------*/

#ifndef __VALIDATE_H__
#define __VALIDATE_H__

/*--------------------------------- IMPORTS ----------------------------------*/

#include "portab.h"

/*-------------------------------- FUNCTIONS ---------------------------------*/

BOOLEAN
validateVariable
(
    char           * varibaleName,            /* in */
    char           * buffer,                  /* in */
    long             length                   /* in */
);

/*----------------------------------------------------------------------------*/

#endif  /* __VALIDATE_H__ */

