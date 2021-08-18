
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to SuSE Linux AG        (c) 2003                                */
/*                                                                            */
/* Project:    fillup                                                         */
/* Module:     validate                                                       */
/* Filename:   validate.c                                                     */
/* Author:     Joerg Dippel                                                   */
/* Description:                                                               */
/*                                                                            */
/*----------------------------------------------------------------------------*/

/*--------------------------------- IMPORTS ----------------------------------*/

#include "parser.h"
#include "parameters.h"
#include "services.h"
#include "consume.h"
#include "validate.h"

/*----------------------------- IMPLEMENTATION -------------------------------*/

/*---------------- validateVariable ----------------*/
BOOLEAN
validateVariable
(
    char           * variableName,           /* in */
    char           * buffer,                 /* in */
    long             length                  /* in */
)
{
    long             consumedLength;
    char           * delimiterString;
    BOOLEAN          returnValue;

    while( ( consumedLength = consumeCommentLines( buffer, length ) ) > 0 )
    {
        length -= consumedLength;
        buffer += consumedLength;
    }

    /* now buffer should point to an uncommented    */
    /* variable name                                */
    /* or a trailing comment has been consumed      */

    queryStringParameter( Delimiter, &delimiterString );
    if( length > 0 )
    {
        consumedLength =
            consumePossibleVariableName( delimiterString[ 0 ], buffer, length );

        if( consumedLength <= length )
        {
            /* line starts with variable name       */
            /* ... seems to be okay ...             */

            if( Equal == 
                compareStringsByLength( variableName, buffer, consumedLength ) )
            { 
                returnValue = TRUE;
            }
            else
            { 
                returnValue = FALSE;
            }
        }
        else
        {
            returnValue = FALSE;
        }
    }
    else
    {
        /* this is the trailing comment             */

        returnValue = TRUE;
    }

    return( returnValue );
}

/*----------------------------------------------------------------------------*/

