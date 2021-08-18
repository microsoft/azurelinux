
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to SuSE Linux AG (c) 2002                                       */
/*                                                                            */
/* Time-stamp:                                                                */
/* Project:    fillup                                                         */
/* Module:     metadata                                                       */
/* Filename:   metadata.c                                                     */
/* Author:     Joerg Dippel (jd)                                              */
/* Description:                                                               */
/*                                                                            */
/*     defines a datastructure for metadata variables and methods             */
/*                                                                            */
/*----------------------------------------------------------------------------*/

/*--------------------------------- IMPORTS ----------------------------------*/

#include <stdio.h>

#include "variableblock.h"
#include "services.h"
#include "parser.h"
#include "consume.h"
#include "validate.h"
#include "dump.h"
#include "metadata.h"

/*---------------------------------- TYPES -----------------------------------*/

/*-------------------------------- VARIABLES ---------------------------------*/

Metadata_t   basefileMetadata;
Metadata_t   addfileMetadata;

char       * metadataKeyword[] = { "Path", "Description", "Type", "Default",
                                   "Config", "ServiceReload", "ServiceRestart", "Command", "PreSaveCommand" };

/*---------------------------- LOCAL PROTOTYPES ------------------------------*/

static void
initializeMetadataInfo
(
    Metadata_t                 * metadata         /* in */
);

static BOOLEAN
checkForMetadata
(
    char                       * precedingComment,/* in */
    long                         variableLength   /* in */
);

static MetadataKeyword_t
checkForMetadataKeyword
(
    char                       * precedingComment,/* in */
    long                         variableLength,  /* in */
    long                       * length          /* out */
);

static long
consumeMetadataInformation
(
    char                       * precedingComment,/* in */
    long                         variableLength   /* in */
);

static MetadataKeyword_t
extractMetadataVariable
(
    char                       * precedingComment,/* in */
    long                         variableLength,  /* in */
    long                       * length          /* out */
);

static void
setSpecialMetadataInfo
(
    Metadata_t                 * metadata,        /* in */
    VariableBlock_t            * variableBlock    /* in */
);

static void
printSpecialMetadataInfo
(
    VariableBlock_t            * variableBlock    /* in */
);

static void
writeMetadataVariable
(
    MetadataVariable_t         * variable,        /* in */
    FILE                       * filePointer,     /* in */
    BOOLEAN                    * PrefixAllowed   /* in - out */
);

static void
writeMetadataInfoFixedSequence
(
    VariableBlock_t            * variableBlock,   /* in */
    FILE                       * filePointer      /* in */
);

/*----------------------------- IMPLEMENTATION -------------------------------*/

/*----------- initializeMetadataInfo -------------*/

static
void
initializeMetadataInfo
(
    Metadata_t                 * metadata         /* in */
)
{
    MetadataKeyword_t            loop;
    
    metadata->beginOfMetadataBlock = (char *)NULL;
    metadata->lengthOfMetadata = (long)0;
    for( loop=0; loop<Metadata_Number; loop++ )
    {
        metadata->variable[ loop ].beginOfMetadataVariable = (char *)NULL;
        metadata->variable[ loop ].lengthOfMetadataVariable = (long)0;
    }
}

/*-------------- checkForMetadata ----------------*/

static
BOOLEAN
checkForMetadata
(
    char                       * precedingComment,/* in */
    long                         variableLength   /* in */
)
{
    BOOLEAN                      Result;
    long                         offset;

    offset = consumeBlanksOrTabs( precedingComment, variableLength );
    if( Equal == compareStringsExactly( "##", &precedingComment[ offset ] ) )
    {
        Result = TRUE;
    }
    else
    {
        Result = FALSE;
    }

    return( Result );
}

/*----------- checkForMetadataKeyword ------------*/

static
MetadataKeyword_t
checkForMetadataKeyword
(
    char                       * precedingComment,/* in */
    long                         variableLength,  /* in */
    long                       * length          /* out */
)
{
    MetadataKeyword_t            Result;
    MetadataKeyword_t            loop;
    long                         offset;

    offset = 0;
    offset += consumeBlanksOrTabs( &precedingComment[ offset ], variableLength - offset );
    for( loop=0; loop<Metadata_Number; loop++ )
    {
        if( Equal == compareStringsExactly( metadataKeyword[ (int)loop ],
                                            &precedingComment[ offset ] ) )
        {
            Result = loop;
            break;
        }
    }

    if( loop == Metadata_Number )
    {
        Result = Metadata_Number;
        *length = 0;
    }
    else
    {
        offset += stringLength( metadataKeyword[ (int)loop ] );
        if( ':' == precedingComment[ offset ] )
        {
            offset++;
            *length = offset;
        }
        else
        {
            /* after the keyword a ':' should follow immediately */
            Result = Metadata_Number;
            *length = 0;
        }
    }

    return( Result );
}

/*--------- consumeMetadataInformation -----------*/

static
long
consumeMetadataInformation
(
    char                       * precedingComment,/* in */
    long                         variableLength   /* in */
)
{
    long                         offset;

    offset = 0;
    while( ( offset < variableLength ) &&
           ( precedingComment[ offset ] != '\n' ) )
    {
        offset++;
    }
    if( precedingComment[ offset ] == '\n' ) offset++;

    return( offset );
}

/*---------- extractMetadataVariable -------------*/

MetadataKeyword_t
extractMetadataVariable
(
    char                       * precedingComment,/* in */
    long                         variableLength,  /* in */
    long                       * length          /* out */
)
{
    MetadataKeyword_t            Result;
    long                         offset;
    long                         prefix;
    MetadataKeyword_t            metadata;
    MetadataKeyword_t            checkedKeyword;

    Result = Metadata_Number;
  
    if( FALSE == checkForMetadata( precedingComment, variableLength ) )
    {
        /* no metadata prefix */
        *length = 0;
        Result = Metadata_Number;
    }
    else
    {
        offset = consumeBlanksOrTabs( precedingComment, variableLength ); 
        offset += 2;   /* string length of "##" */
        offset += consumeBlanksOrTabs( &precedingComment[ offset ], variableLength );
        precedingComment += offset;
        variableLength -= offset;
        *length = offset;
        
        metadata = checkForMetadataKeyword( precedingComment, variableLength, &offset );
        if( metadata < Metadata_Number )
        {
            offset += consumeMetadataInformation( &precedingComment[ offset ], variableLength );
            precedingComment += offset;
            variableLength -= offset;
            *length += offset;

            if( TRUE == checkForMetadata( precedingComment, variableLength ) )
            {
                offset = consumeBlanksOrTabs( precedingComment, variableLength );
                offset += 2;   /* string length of "##" */
                offset += consumeBlanksOrTabs( &precedingComment[ offset ], variableLength );
                precedingComment += offset;
                variableLength -= offset;
                prefix = offset;

                while( ( Metadata_Number <= 
                       ( checkedKeyword = 
                            checkForMetadataKeyword( precedingComment, variableLength, &offset ) ) ) ||
                       ( checkedKeyword == metadata ) )
                {
                    offset = consumeMetadataInformation( precedingComment, variableLength );
                    *length += prefix;
                    *length += offset;

                    precedingComment += offset;
                    variableLength -= offset;

                    if( FALSE == checkForMetadata( precedingComment, variableLength ) ) break;
                    else
                    { 
                        offset = consumeBlanksOrTabs( precedingComment, variableLength );
                        offset += 2;   /* string length of "##" */
                        offset += consumeBlanksOrTabs( &precedingComment[ offset ], variableLength );
                        precedingComment += offset;
                        variableLength -= offset;
                        prefix = offset;
                    }
                }
            }

            Result = metadata;
        }
        else
        {
            /* no metadata keyword */
            *length = 0;
            Result = Metadata_Number;
        }
    }
    
    return( Result );
}

/*-------------- setMetadataInfo -----------------*/

void
setMetadataInfo
(
    VariableBlock_t            * variableBlock    /* in */
)
{
    char                       * debuggingVariableName;
    char                       * variableName;
    char                       * filename;
    FILE                       * logfile;
    char                       * beginOfString;
    long                         lengthOfString;
    int                          loop;

    setSpecialMetadataInfo( &basefileMetadata, variableBlock );
    setSpecialMetadataInfo( &addfileMetadata, getVAssociation( variableBlock ) );

    /* ---------------------------------------------- *\
    |  An undocumented debugging feature:
    |  information about a special variable
    |     (given by --variable option on command line)
    |  is logged into a special file
    |     (determined by --logfile option on command line)
    |  Because it is for debugging, the file is opened, the
    |  info is written and the file is closed immediately.
    \* ---------------------------------------------- */

    if( TRUE == queryParameter( DebuggingVariableName ) )
    {
        queryStringParameter( DebuggingVariableName, &debuggingVariableName );
        getVBeginOfBlock( variableBlock, &variableName );
        variableName += getVOffsetOfVariableName( variableBlock );
    
        if( ( Equal == compareStringsExactly( debuggingVariableName, variableName ) ) &&
            ( TRUE == queryParameter( DebuggingLogfile ) ) )
        {
            queryStringParameter( DebuggingLogfile, &filename );
            if( FileOpened == openFileForWriting( filename, &logfile ) )
            {
                getVBeginOfBlock( variableBlock, &beginOfString );
                lengthOfString = getVLength( variableBlock );
    
                fprintf( logfile, "<basefile variable block>: <%ld>\n<", lengthOfString );
                writeBlock( beginOfString, lengthOfString, logfile );
                fprintf( logfile, ">\n" );
    
                for( loop=0; loop<Metadata_Number; loop++ )
                {
                    fprintf( logfile, "<basefile metadata %s>: <%ld>\n<", 
                                metadataKeyword[ loop ], 
                                basefileMetadata.variable[ loop ].lengthOfMetadataVariable );
                    writeBlock( basefileMetadata.variable[ loop ].beginOfMetadataVariable,
                                basefileMetadata.variable[ loop ].lengthOfMetadataVariable,
                                logfile );       
                    fprintf( logfile, ">\n" );
                }
    
                getVBeginOfBlock( getVAssociation( variableBlock ), &beginOfString );
                lengthOfString = getVLength( getVAssociation( variableBlock ) );
    
                fprintf( logfile, "\n<addfile variable block>: <%ld>\n<", lengthOfString );
                writeBlock( beginOfString, lengthOfString, logfile );
                fprintf( logfile, ">\n" );
    
                for( loop=0; loop<Metadata_Number; loop++ )
                {
                    fprintf( logfile, "<addfile metadata %s>: <%ld>\n<",
                                metadataKeyword[ loop ],
                                addfileMetadata.variable[ loop ].lengthOfMetadataVariable );
                    writeBlock( addfileMetadata.variable[ loop ].beginOfMetadataVariable,
                                addfileMetadata.variable[ loop ].lengthOfMetadataVariable,
                                logfile );
                    fprintf( logfile, ">\n\n" );
                }
    
                closeFile( logfile );
            }
        }
    }
}

/*----------- setSpecialMetadataInfo -------------*/

static
void
setSpecialMetadataInfo
(
    Metadata_t                 * metadata,        /* in */
    VariableBlock_t            * variableBlock    /* in */
)
{
    char                       * precedingComment;
    long                         length;
    long                         offset;
    long                         whiteSpacesOffset;
    MetadataKeyword_t            metadataVariable; 

    initializeMetadataInfo( metadata );
    length = getVLength( variableBlock );
    getVBeginOfBlock( variableBlock, &precedingComment );

    whiteSpacesOffset = consumeSpaces( precedingComment, length );
    /* the prefix of white spaces within add file will be preserved */
    /* only if metadata is available - by the way the prefix of     */
    /* white spaces within base file will be removed on writing ... */

    metadataVariable = 
        extractMetadataVariable( precedingComment + whiteSpacesOffset, 
                                 length - whiteSpacesOffset, &offset );

    if( Metadata_Number > metadataVariable )
    {
        metadata->beginOfMetadataBlock = precedingComment;
    }

    while( Metadata_Number > metadataVariable )
    {
        if( metadata->variable[ metadataVariable ].lengthOfMetadataVariable > 0 )
        {
            break;

            /* An already detected keyword is redefined => part of comment */
        }

        offset += whiteSpacesOffset;
        whiteSpacesOffset = 0;    /* assigned only once */

        metadata->variable[ metadataVariable ].beginOfMetadataVariable = 
            precedingComment;
        metadata->variable[ metadataVariable ].lengthOfMetadataVariable = 
            offset;

        metadata->lengthOfMetadata += offset;

        precedingComment += offset;
        length -= offset;
        metadataVariable =
            extractMetadataVariable( precedingComment, length, &offset );
    }
}

/*---------- printSpecialMetadataInfo ------------*/

void
printSpecialMetadataInfo
(
    VariableBlock_t            * variableBlock    /* in */
)
{
    Metadata_t                   printMetadata;
    MetadataKeyword_t            loop;

    setSpecialMetadataInfo( &printMetadata, variableBlock );
    if( printMetadata.beginOfMetadataBlock != (char *)NULL )
    {
        displayVerboseBuffer( 
            printMetadata.beginOfMetadataBlock, printMetadata.lengthOfMetadata );

        for( loop=0; loop<Metadata_Number; loop++ )
        {
            if( printMetadata.variable[ loop ].beginOfMetadataVariable != (char *)NULL )
            {
                displayVerboseString( metadataKeyword[ loop ] );
                displayVerboseString( "\n" );
                displayVerboseBuffer( 
                    printMetadata.variable[ loop ].beginOfMetadataVariable, 
                    printMetadata.variable[ loop ].lengthOfMetadataVariable );
            }
        }
    }
}

/*------------- printMetadataInfo ----------------*/

void
printMetadataInfo
(   
    VariableBlock_t            * variableBlock    /* in */
)
{   
    if( ( TRUE == queryParameter( Verbose ) )  && ( FALSE == queryParameter( NoMetadata ) ) )
    {
        displayVerboseString( "\n~~~~~~~~~~~~ metadata info ~~~~~~~~~~~~\n" );
        printSpecialMetadataInfo( variableBlock );
        displayVerboseString( "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" );
    }
}

/*----------------- getMinimum -------------------*/

/* this function has been called only in          */
/* writeMetadataInfoFirstBasefileThenAddfile() -  */
/* the function has been removed also             */

/*----------- writeMetadataVariable --------------*/

static
void
writeMetadataVariable
(
    MetadataVariable_t         * variable,        /* in */
    FILE                       * filePointer,     /* in */
    BOOLEAN                    * PrefixAllowed   /* in - out */
)
{
    long                         spaces;
    char                       * begin;
    long                         length;

    begin = variable->beginOfMetadataVariable;
    length = variable->lengthOfMetadataVariable;

    if( FALSE == *PrefixAllowed )
    {
        spaces = consumeSpaces( begin, length );
        begin += spaces;
        length -= spaces;
    }

    *PrefixAllowed = FALSE;
    writeBlock( begin, length, filePointer );
}

/*------ writeMetadataInfoFixedSequence ----------*/

static
void
writeMetadataInfoFixedSequence
(
    VariableBlock_t            * variableBlock,   /* in */
    FILE                       * filePointer      /* in */
)
{
    MetadataKeyword_t            loop;
    char                       * address;
    MetadataVariable_t         * metadataBaseVariable;
    MetadataVariable_t         * metadataAddVariable;
    long                         offset;
    long                         spaces;
    BOOLEAN                      PrefixSpacesAllowed;
    long                         variableNameOffset;
    char                       * variableName;

    PrefixSpacesAllowed = TRUE;
    offset = 0;
    for( loop=0; loop<Metadata_Number; loop++ )
    {
        metadataBaseVariable = &basefileMetadata.variable[ loop ];
        metadataAddVariable = &addfileMetadata.variable[ loop ];

        if( metadataBaseVariable->beginOfMetadataVariable != NULL )
        {
            if( metadataAddVariable->beginOfMetadataVariable != NULL )
            {
                writeMetadataVariable( metadataAddVariable, filePointer, &PrefixSpacesAllowed );
            }
            else
            {
                writeMetadataVariable( metadataBaseVariable, filePointer, &PrefixSpacesAllowed );
            }
            offset += metadataBaseVariable->lengthOfMetadataVariable;
        }
        else
        {
            if( metadataAddVariable->beginOfMetadataVariable != NULL )
            {
                writeMetadataVariable( metadataAddVariable, filePointer, &PrefixSpacesAllowed );
            }
        }
    }

    getVBeginOfBlock( variableBlock, &address );
    variableNameOffset = getVOffsetOfVariableName( variableBlock );
    variableName = &address[ variableNameOffset ];

    address += offset;
    offset = getVLength( variableBlock ) - offset;

    /* deleting possible white spaces between metadata and comment */
    if( FALSE == PrefixSpacesAllowed )
    {
        spaces = consumeSpaces( address, offset );
        address += spaces;
        offset -= spaces;
    }

    if( FALSE ==
        validateVariable( variableName, address, offset ) )
    {
        dump( variableBlock );
    }

    writeBlock( address, offset, filePointer );
}

/*------------- writeMetadataInfo ----------------*/

void
writeMetadataInfo
(
    VariableBlock_t            * variableBlock,   /* in */
    FILE                       * filePointer      /* in */
)
{
/*#   ifdef FixedSequenceOfMetadata */

    writeMetadataInfoFixedSequence( variableBlock, filePointer );

#if 0

    this should produce a syntax error because function
    writeMetadataInfoFirstBasefileThenAddfile( variableBlock, filePointer )
    has been broken for Bugzilla #25119

    The related function has been removed.

#endif
}

/*----------------------------------------------------------------------------*/

