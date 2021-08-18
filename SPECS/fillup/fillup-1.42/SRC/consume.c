
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to SuSE Linux AG        (c) 2003                                */
/*                                                                            */
/* Project:    fillup                                                         */
/* Module:     consume                                                        */
/* Filename:   consume.c                                                      */
/* Author:     Joerg Dippel                                                   */
/* Description:                                                               */
/*                                                                            */
/*----------------------------------------------------------------------------*/

/*--------------------------------- IMPORTS ----------------------------------*/

#include <stdio.h>
#include <ctype.h>
#include "portab.h"

#include "parameters.h"
#include "consume.h"

/*----------------------------- IMPLEMENTATION -------------------------------*/

/*---------------- consumeSpaces ------------------*\
|  This function returns the number of read 
|  characters.
|  The characters are read from a stream/buffer and
|  the stream is length restricted and only white 
|  space are read.
\*---------------- consumeSpaces ------------------*/
long
consumeSpaces
(
    char           * buffer,                 /* in */
    long             lineLength              /* in */
)
{
    long             Counter;

    Counter = 0;
    while( ( Counter < lineLength ) && ( isspace( *buffer ) ) )
    {
        Counter++;
        buffer++;
    }

    return( Counter );
}

/*------------- consumeBlanksOrTabs ---------------*\
|  This function returns the number of read
|  characters.
|  The characters are read from a stream/buffer and
|  the stream is length restricted and only blanks or
|  tabulators are read.
\*------------- consumeBlanksOrTabs ---------------*/
long
consumeBlanksOrTabs
(
    char           * buffer,                 /* in */
    long             lineLength              /* in */
)
{
    long             Counter;

    Counter = 0;
    while( ( Counter < lineLength ) &&
           ( ( ' ' == *buffer ) || ( '\t' ==  *buffer ) ) )
    {
        Counter++;
        buffer++;
    }

    return( Counter );
}

/*---------- consumePossibleVariableName ----------*\
|  This function returns the number of read
|  characters which are part of a variable name
|  followed by the delimiter start.
|  The characters are read from a stream/buffer and
|  the stream is length restricted.
\*---------- consumePossibleVariableName ----------*/
long
consumePossibleVariableName
(
    char             delimiterStart,         /* in */
    char           * buffer,                 /* in */
    long             lineLength              /* in */
)
{
    long             Counter;

    if( ( isalpha( *buffer ) )  || ( *buffer == '_' ) )
    {
        Counter = 1;
        buffer++;
        while( ( Counter < lineLength )        &&
               ( ( isalnum( *buffer ) )   ||
                 ( *buffer == '_' )       ||
                 ( *buffer == '.' ) )          &&
               ( *buffer != delimiterStart ) )
        {
            Counter++;
            buffer++;
        }
    }
    else
    {
        Counter = 0;
    }

    return( Counter );
}

/*----------------- consumeUptoBreak ---------------*\
|  This function returns the number of read 
|  characters up to a line break or up to the end of 
|  file.
|  The characters are read from a stream/buffer and
|  the stream is length restricted.
\*----------------- consumeUptoBreak ---------------*/
long
consumeUptoBreak
(
    char           * buffer,                 /* in */
    long             length                  /* in */
)
{
    long             counter;

    counter = 0;
    while( length > 0 )
    {
        counter++;
        length--;

        if( *buffer == '\n' )
        {
            break;           /* line break detected */
        }
        else if( *buffer == EOF )
        {
            break;          /* End-Of-File detected */
        }
        else
        {
            buffer++;
        }
    }

    return( counter );
}

/*--------------- consumeCommentLines --------------*\
|  This function returns the number of read 
|  characters that are part of comment lines,
|  additionaly a prefix of white spaces.
|  The characters are read from a stream/buffer and
|  the stream is length restricted.
\*--------------- consumeCommentLines --------------*/
long
consumeCommentLines
(
    char           * buffer,                  /* in */
    long             length                   /* in */
)
{
    long             commentMarkerStringLength;
    long             consumedLength;
    long             sumOfConsumedLength;
    char           * markerString;

    queryStringParameter( CommentMarker, &markerString );
    commentMarkerStringLength = stringLength( markerString );
    sumOfConsumedLength = 0;

    while( length > 0 )
    {
        consumedLength = consumeSpaces( buffer, length );
        sumOfConsumedLength += consumedLength;
        length -= consumedLength;
        buffer += consumedLength;

        if( length > commentMarkerStringLength )
        {
            if( Equal ==
                compareStringsExactly( markerString, buffer ) )
            {
                /* this is a comment line           */

                consumedLength = consumeUptoBreak( buffer, length );
                sumOfConsumedLength += consumedLength;
                length -= consumedLength;
                buffer += consumedLength;
            }
            else
            {
                break;

                /* this is a line that does not        */
                /* start with a comment marker string. */
            }
        }
        else
        {
            break;
            /* content of buffer is to short to     */
            /* hold the comment marker string.      */
        }
    }

    return( sumOfConsumedLength );
}

/*----------------------------------------------------------------------------*/

