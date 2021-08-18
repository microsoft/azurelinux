
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to S.u.S.E. GmbH Fuerth (c) 1998                                */
/* Copyrights to SuSE GmbH            (c) until 2001                          */
/* Copyrights to SuSE Linux AG        (c) 2002,2003                           */
/*                                                                            */
/* Project:    fillup                                                         */
/* Module:     services                                                       */
/* Filename:   services.c                                                     */
/* Author:     Joerg Dippel                                                   */
/* Description:                                                               */
/*                                                                            */
/*     Standard library functions are not called directly. To avoid           */
/*     problems in sublayers there are service function that call these       */
/*     standard library functions.                                            */
/*                                                                            */
/*----------------------------------------------------------------------------*/

/*--------------------------------- IMPORTS ----------------------------------*/

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
#include <errno.h>

#include "portab.h"

#include "fillup_cfg.h"
#include "parameters.h"
#include "services.h"

/*----------------------------- IMPLEMENTATION -------------------------------*/

static long watchdogLength;

static void
callWatchdog
(
    long            length                    /* in */
);

/*------------- compareStringsExactly --------------*/

StringOrder_t
compareStringsExactly
(
    const char    * firstString,              /* in */
    const char    * secondString              /* in */
)
{
    BOOLEAN    returnValue;

    if( strncmp( firstString, secondString, strlen( firstString ) ) == 0 )
    {
        returnValue = Equal;
    }
    else
    {
        returnValue = Different;
    }

    return( returnValue );
}
/*------------- compareStringsByLength -------------*/

StringOrder_t
compareStringsByLength
(
    const char    * firstString,              /* in */
    const char    * secondString,             /* in */
    const long      length                    /* in */
)
{
    BOOLEAN    returnValue;

    if( strncmp( firstString, secondString, length ) == 0 )
    {
        returnValue = Equal;
    }
    else
    {
        returnValue = Different;
    }

    return( returnValue );
}

/*----------------- compareStrings -----------------*/

StringOrder_t
compareStrings
(
    const char    * firstString,              /* in */
    const char    * secondString              /* in */
)
{
    int             serviceResult;
    StringOrder_t   returnValue;

    serviceResult = strcmp( firstString, secondString );

    if( serviceResult < 0 )
    {
        returnValue = Smaller;
    }
    else if( serviceResult == 0 )
    {
        returnValue = Equal;
    }
    else
    {
        returnValue = Greater;
    }

    return( returnValue );
}

/*------------------ stringLength ------------------*/

long
stringLength
(
    const char    * String                    /* in */
)
{
    return( ( long )strlen( String ) );
}

/*------------- createNewBaseFileName --------------*/

Service_t
createNewBaseFileName
(
    const char    * oldString,                /* in */
          char    * newString                 /* in */
)
{
    StringOrder_t          returnValue;
    static const char    * extentionOfBaseFile = ".new";

    if( ( strlen( oldString ) + strlen( extentionOfBaseFile ) + 1 ) < 
        cfg_MaxVariableLength )
    {
        ( void )strcpy( newString, oldString );
        ( void )strcat( newString, extentionOfBaseFile );

        returnValue = Success;
    }
    else
    {
        fillup_exception( __FILE__, __LINE__, ConfigurationException,
                          "createNewBaseFileName" );
        exitOnFailure( );
        returnValue = Error;
    }

    return( returnValue );
}

/*----------------- exitOnFailure ------------------*/

void
exitOnFailure
(
    void
)
{
    exit( EXIT_FAILURE );
}

/*--------------- fillup_exception -----------------*/

void
fillup_exception
(
    const char    * fileName,                 /* in */
          int       lineNumber,               /* in */
    Exception_t     exceptionType,            /* in */
    const char    * description               /* in */
)
{
    ( void )fprintf( stderr, 
                     "\tfillup: Exception in %s, line %d concerning %s\n", 
                     fileName, 
                     lineNumber, 
                     description );
}

/*------------ fillupDumpFileCreated ---------------*/

void
fillupDumpFileCreated
(
    void
)
{
    ( void )fprintf( stderr, "\tfillup: Dumping infos into temporary file\n" );
}


/*-------------- displayStderrString ---------------*/

void
displayStderrString
(
    const char    * string                    /* in */
)
{
    if( ( int )strlen( string ) != ( fprintf( stderr, "%s\n", string ) - 1 ) )
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "displayStderrString" );
        exitOnFailure( );
    }
}

/*----------------- displayString ------------------*/

void
displayString
(
    const char    * string                   /* in */
)
{
    if( ( int )strlen( string ) != fprintf( stderr, "%s", string ) )
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "displayString" );
        exitOnFailure( );
    }
}

/*----------------- displayValue -------------------*/

void
displayValue
(
    long            value                    /* in */
)
{
    ( void )fprintf( stderr, "%ld", value );
}

/*--------------- displayCharacter -----------------*/

void
displayCharacter
(
    char            character                /* in */
)
{
    ( void )fputc( character, stderr );
}

/*---------------- displayVersion ------------------*/

void
displayVersion
(
    void
)
{
    static const char *versionString = 
                      "This is fillup, version %1.2f, compiled on %s\n\n";

    if( ( int )( strlen( versionString ) + strlen( __DATE__ ) - 3 ) != 
        fprintf( stderr, versionString, VERSION, __DATE__ ) )
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "displayVersion" );
        exitOnFailure( );
    }
}

/*------------------ getCardinal -------------------*/

Service_t
getCardinal
(
    const char       * string,               /* in */
    unsigned long    * cardinalValue         /* out */
)
{
    StringOrder_t      returnValue;
    long               Value;

    Value = strtol( string, ( char ** )NULL, 10 );
    if( errno == ERANGE )
    {
        if( Value == LONG_MIN )
        {
            fillup_exception( __FILE__, __LINE__, ServiceException, 
                              "value overflow in getCardinal" );
        }
        else
        {
            fillup_exception( __FILE__, __LINE__, ServiceException, 
                              "value underflow in getCardinal" );
        }

        errno = 0;     /* reset of errno variable */
        returnValue = Error;
    }
    else if( Value < 0 )
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "negative value in getCardinal" );
        returnValue = Error;
    }
    else
    {
        returnValue = Success;
    }

    if( Success == returnValue )
    {
        *cardinalValue = ( unsigned long )Value;
    }
    else
    {
        *cardinalValue = ( unsigned long )0;
        exitOnFailure( );
    }

    return( returnValue );
}

/*-------------- openFileForReading ----------------*/

Service_t
openFileForReading
(
    const char    * filename,                 /* in */
    FILE         ** filePointer              /* out */
)
{
    Service_t       returnValue;

    *filePointer = fopen( filename, "r" );
    if( *filePointer == NULL )
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "file not opened" );
        returnValue = FileOpenError;
    }
    else
    {
        returnValue = FileOpened;
    }

    return( returnValue );
}

/*-------------- openFileForWriting ----------------*/

Service_t
openFileForWriting
(
    const char    * filename,                 /* in */
    FILE         ** filePointer              /* out */
)
{
    Service_t       returnValue;

    *filePointer = fopen( filename, "w" );
    if( *filePointer == NULL )
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "file not opened" );
        returnValue = FileOpenError;
    }
    else
    {
        returnValue = FileOpened;
    }

    return( returnValue );
}

/*------------------- closeFile --------------------*/

void
closeFile
(
    FILE          * filePointer               /* in */
)
{
    if( 0 != fclose( filePointer ) )
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "file not closed" );
    }
}

/*----------------- getFileLength ------------------*/

Service_t
getFileLength
(
    FILE          * filePointer,              /* in */
    long          * fileLength               /* out */
)
{
    Service_t       returnValue;

    if( 0 == fseek( filePointer, 0L, SEEK_END ) )
    {
        *fileLength = ftell( filePointer );
        if( *fileLength < 0 )
        {
            fillup_exception( __FILE__, __LINE__, ServiceException, 
                              "ftell" );
            returnValue = Error;
        }
        else
        {
            /* change within specification: empty files are now valid */
            returnValue = Success;
        }
    }
    else
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "fseek" );
        returnValue = Error;
    }

    return( returnValue );
}

/*--------------- readFileToBuffer -----------------*/

Service_t
readFileToBuffer
(
    FILE          * filePointer,              /* in */
    long            fileLength,               /* in */
    char         ** fileBuffer               /* out */
)
{
    Service_t       returnValue;

    if( 0 == fseek( filePointer, 0L, SEEK_SET ) )
    {
        if( fileLength == 
            ( long )fread( *fileBuffer, sizeof( char ), fileLength, filePointer ) )
        {
            returnValue = Success;
        }
        else
        {
            fillup_exception( __FILE__, __LINE__, ServiceException, 
                              "fread" );
            returnValue = Error;
        }
    }
    else
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "fseek" );
        returnValue = Error;
    }
   
    return( returnValue );
}

/*----------------- initWatchdog -------------------*/
void
initWatchdog
(
    void
)
{
    watchdogLength = 0;
}

/*----------------- addToWatchdog ------------------*/
void
addToWatchdog
(
    long            length                    /* in */
)
{
    /* For removal, the output is written and the   */
    /* basefile removed by defined variables.       */
    /* Therefor there are two passes for writing.   */
    if( TRUE == queryParameter( Remove) ) length *=2;

    watchdogLength += length;
}

/*----------------- callWatchdog -------------------*/

static void
callWatchdog
(
    long            length                    /* in */
)
{
    /* for merging not more than the sum of bytes   */
    /* defined for basefile and addfile can be      */
    /* written.                                     */
    /* watchdogLength is assigned that sum, and any */
    /* writeBlock() call decreases the sum.         */

    if( ( watchdogLength - length ) < 0 )
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "callWatchdog" );
    }
    else
    {
        watchdogLength -= length;
    }
}

/*------------------ writeBlock --------------------*/
void
writeBlock
(
    char          * buffer,                   /* in */
    long            length,                   /* in */
    FILE          * filePointer               /* in */
)
{
    callWatchdog( length );
    if( length != 
        ( long )fwrite( buffer, sizeof( char ), length, filePointer ) )
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "fwrite" );
    }
}

/*------------------- dumpBlock --------------------*/
/* same as writeBlock but no watchdog call          */
/*------------------- dumpBlock --------------------*/
void
dumpBlock
(
    char          * buffer,                   /* in */
    long            length,                   /* in */
    FILE          * filePointer               /* in */
)
{
    if( length !=
        ( long )fwrite( buffer, sizeof( char ), length, filePointer ) )
    {
        fillup_exception( __FILE__, __LINE__, ServiceException,
                          "fwrite" );
    }
}

/*------------------ allocateBuffer -----------------*/

Service_t
allocateBuffer
(
    long            fileLength,                /* in */
    void         ** buffer                    /* out */
)
{
    Service_t       returnValue;

    *buffer = malloc( fileLength + 1 );
    if( *buffer == NULL )
    {
        fillup_exception( __FILE__, __LINE__, ServiceException, 
                          "malloc" );
        returnValue = Error;
    }
    else
    {
        /* reset the buffer */
        ( void )memset( *buffer, EOF, fileLength + 1 );

        returnValue = Success;
    }
   
    return( returnValue );
}

/*-------------------- freeBuffer -------------------*/

Service_t
freeBuffer
(
    char                     ** buffer         /* in */
)
{
    Service_t       returnValue;

    free( *buffer );
    returnValue = Success;
   
    return( returnValue );
}

/*----------------------------------------------------------------------------*/
