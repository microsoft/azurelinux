
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to S.u.S.E. GmbH Fuerth (c) 1998                                */
/*                                                                            */
/* Time-stamp: 11/18/98                                                       */
/* Project:    fillup                                                         */
/* Module:     services                                                       */
/* Filename:   services.h                                                     */
/* Author:     Joerg Dippel (jd)                                              */
/* Description:                                                               */
/*                                                                            */
/*     export interface for services                                          */
/*                                                                            */
/*----------------------------------------------------------------------------*/

#ifndef __SERVICES_H__
#define __SERVICES_H__

/*--------------------------------- IMPORTS ----------------------------------*/

#include <stdio.h>

#include "portab.h"

/*---------------------------------- TYPES -----------------------------------*/

typedef enum
{
    FormatException,
    NumberOfFormatException,
    DefaultBranchException,
    ConfigurationException,
    ServiceException
} Exception_t;

typedef enum
{
    Success,
    Error,
    FileOpened,
    FileOpenError
} Service_t;

typedef enum
{
    Smaller,
    Equal,
    Greater,
    Different
} StringOrder_t;

/*------------------- FUNCTION DECLARATIONS (PROTOTYPES) ---------------------*/

StringOrder_t
compareStrings
(
    const char    * firstString,              /* in */
    const char    * secondString              /* in */
);

StringOrder_t
compareStringsExactly
(    
    const char    * firstString,              /* in */
    const char    * secondString              /* in */
);

StringOrder_t
compareStringsByLength
(
    const char    * firstString,              /* in */
    const char    * secondString,             /* in */
    const long      length                    /* in */
);

long
stringLength
(
    const char    * String                    /* in */
);

Service_t
createNewBaseFileName
(
    const char    * oldString,                /* in */
          char    * newString                 /* in */
);

void
exitOnFailure
(
    void
);

void
fillup_exception
(
    const char    * fileName,                 /* in */
          int       lineNumber,               /* in */
    Exception_t     exceptionType,            /* in */
    const char    * description               /* in */
);

void
fillupDumpFileCreated
(
    void
);

void
displayStderrString
(
    const char    * string                    /* in */
);

void
displayString
(
    const char    * string                   /* in */
);

void
displayValue
(
    long            value                    /* in */
);

void
displayCharacter
(   
    char            character                /* in */
);

void
displayVersion
(
    void
);

Service_t
getCardinal
(
    const char       * string,                /* in */
    unsigned long    * cardinalValue         /* out */
);

Service_t
openFileForReading
(
    const char    * filename,                 /* in */
    FILE         ** filePointer              /* out */
);

Service_t
openFileForWriting
(
    const char    * filename,                 /* in */
    FILE         ** filePointer              /* out */
);

void
closeFile
(
    FILE          * filePointer               /* in */
);

Service_t
getFileLength
(
    FILE          * filePointer,              /* in */
    long          * fileLength               /* out */
);

Service_t
readFileToBuffer
(
    FILE          * filePointer,              /* in */
    long            fileLength,               /* in */
    char         ** fileBuffer               /* out */
);

void
initWatchdog
(
    void
);

void
addToWatchdog
(
    long            length                    /* in */
);

void
writeBlock
(
    char          * buffer,                   /* in */
    long            length,                   /* in */
    FILE          * filePointer               /* in */
);

void
dumpBlock
(
    char          * buffer,                   /* in */
    long            length,                   /* in */
    FILE          * filePointer               /* in */
);

Service_t
allocateBuffer
(
    long            fileLength,               /* in */
    void         ** buffer                   /* out */
);

Service_t
freeBuffer
(
    char                     ** buffer         /* in */
);

/*----------------------------------------------------------------------------*/

#endif  /* __SERVICES_H__ */
