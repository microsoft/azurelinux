
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to SuSE Linux AG        (c) 2003                                */
/*                                                                            */
/* Project:    fillup                                                         */
/* Module:     consume                                                       */
/* Filename:   consume.h                                                     */
/* Author:     Joerg Dippel (jd )                                             */
/* Description:                                                               */
/*                                                                            */
/*             export interface                                               */
/*                                                                            */
/*----------------------------------------------------------------------------*/

#ifndef __CONSUME_H__
#define __CONSUME_H__

/*--------------------------------- IMPORTS ----------------------------------*/

/*-------------------------------- FUNCTIONS ---------------------------------*/

long
consumeSpaces
(
    char           * buffer,                 /* in */
    long             lineLength              /* in */
);

long
consumeBlanksOrTabs
(
    char           * buffer,                 /* in */
    long             lineLength              /* in */
);

long
consumePossibleVariableName
(  
    char             delimiterStart,         /* in */
    char           * buffer,                 /* in */
    long             lineLength              /* in */
);

long
consumeUptoBreak
(
    char           * buffer,                 /* in */
    long             length                  /* in */
);

long
consumeCommentLines
(
    char           * buffer,                  /* in */
    long             length                   /* in */
);

/*----------------------------------------------------------------------------*/

#endif  /* __CONSUME_H__ */

