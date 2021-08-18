
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to S.u.S.E. GmbH Fuerth (c) 1998                                */
/*                                                                            */
/* Time-stamp:                                                                */
/* Project:    fillup                                                         */
/* Module:     fillup                                                         */
/* Filename:   getArguments.c                                                 */
/* Author:     Joerg Dippel (jd)                                              */
/* Description:                                                               */
/*                                                                            */
/*     fillup takes two files (basefile and addfile) for                      */
/*     variables and creates a new file (outputfile) containing variables.    */
/*     If basefile and outputfile are named identically only two parameters   */
/*     are necessary -- this supports the old form of fillup (1.04)           */
/*                                                                            */
/*     Each variable name is assigned one value. This assignment composes an  */
/*     entity with its related comment - the comment may be empty.            */
/*     This entity is named 'variable block'.                                 */
/*                                                                            */
/*     basefile, addfile and outputfile are files containing variable blocks. */
/*     addfile may contain only variable names if variable                    */
/*     blocks should be retrieved -- or only assignments if there should be   */
/*     assignment substitutions.                                              */
/*                                                                            */
/*     fillup now provides different kinds of functionality to create the     */
/*     outputfile. The content of the variable blocks is handled as           */
/*     transparent (this means no information is evaluated):                  */
/*     -- Variable blocks of basefile remain unchanged and                    */
/*        all variable blocks of basefile are added to the outputfile.        */
/*        Variable blocks of newfile are added to the outputfile only if      */
/*        they are not in the basefile.                                       */
/*        (This is the former functionality of fillup-1.04.)                  */
/*        Testseries 1XX: parameter -m (implicitely)                          */
/*     -- Variable blocks of basefile are deleted from the original basefile  */
/*        but all variable blocks of original basefile are added to the       */
/*        outputfile.                                                         */
/*        Variable blocks of newfile are added to the outputfile only if      */
/*        they are not in the original basefile.                              */
/*        Testseries 4XX: parameter -r                                        */
/*     -- Variable blocks of newfile remain unchanged and                     */
/*        all variable blocks of newfile are added to the outputfile.         */
/*        Variable blocks of basefile are added to the outputfile only if     */
/*        they are not in the newfile.                                        */
/*        Testseries 2XX: parameter -x                                        */
/*     -- Variable blocks of newfile remain unchanged and                     */
/*        all variable blocks of newfile are added to the outputfile.         */
/*        Variable blocks of original basefile are added to the outputfile    */
/*        only if they are not in the newfile. If that happens they are       */
/*        deleted from the original basefile.                                 */
/*        Testseries 5XX: parameter -x -r                                     */
/*     -- Variable blocks of basefile remain unchanged and a variable block   */
/*        of basefile is added to the outputfile only if there is a variable  */
/*        defined in the addfile with the same name -- otherwise the variable */
/*        is ignored.                                                         */
/*        Variable blocks of newfile are added to the outputfile only if      */
/*        they are not in the basefile.                                       */
/*        Testseries 3XX: parameter -i                                        */
/*                                                                            */
/*     Furthermore fillup now provides a functionality for substitution of    */
/*     assignments. The basefile is transformed into the outputfile --        */
/*     Within the transformation for each variable name which is not part     */
/*     of an assignment within the definition file the related variable       */
/*     block is transparently copied to the outputfile.                       */
/*     Otherwise if a variable name is part of an assignment within the       */
/*     definition file the assignment of the basefile is substituted by the   */
/*     assignment of the definitionfile and this new variable block is        */
/*     copied to the outputfile.                                              */
/*                                                                            */
/*     Starting with version 1.20 handling of metadata for /etc/sysconfig     */
/*     files is included. Metadata is part of preceding comment, each         */
/*     metadata line begins with double hash ("##"). A metadata line con­     */
/*     tains a pair <keyword>:<value>. The value itself can be described      */
/*     on several lines, each beginning with double hash and the optional     */
/*     keyword.                                                               */
/*                                                                            */
/*----------------------------------------------------------------------------*/

/*--------------------------------- IMPORTS ----------------------------------*/

#include <stdlib.h>

#include "portab.h"
#include "parameters.h"
#include "services.h"
#include "parser.h"
#include "getArguments.h"

/*--------------------------------- DEFINES ----------------------------------*/

#define   numberOfMandatoryParameters       2 
#define   numberOfSimpleParameter           1
#define   numberOfPairParameter             2

/*----------------------------- LOCAL VARIABLES ------------------------------*/

static int     staticArgc;
static char  **staticArgv;

static int     currentOptionCounter;

/*-------------------------------- FUNCTIONS ---------------------------------*/

/*----------------------------- IMPLEMENTATION -------------------------------*/

/*--------------- checkArgument ----------------*/
static BOOLEAN 
checkArgument
( 
    const char *argument,                /* in */
    const char *firstAlternative,        /* in */
    const char *secondAlternative        /* in */
)
{
    BOOLEAN     returnValue;

    if( compareStrings( argument, firstAlternative ) == Equal ) 
    {
        returnValue = TRUE;
    }
    else if( compareStrings( argument, secondAlternative ) == Equal ) 
    {
        returnValue = TRUE;
    }
    else
    {
        returnValue = FALSE;
    }

    return( returnValue );
}

/*------- initializeAccessToParameters ---------*/
void
initializeAccessToParameters
(
    void
)
{
    currentOptionCounter = 1;    
}
/*----------- getAccessToParameters ------------*/
char *
getAccessToParameters
(
    void
)
{
    char    *returnValue;

    if( currentOptionCounter < staticArgc )
    {
        returnValue = staticArgv[ currentOptionCounter ]; 
        currentOptionCounter++;
    }
    else
    {
        returnValue = ( char * )NULL;
    }

    return( returnValue );
}

/*-------------------- main --------------------*/
int 
main 
(
    int     argc,                        /* in */
    char  **argv                         /* in */
) 
{  
    BOOLEAN   parsingState;
    BOOLEAN   InterruptCausingExceptionState;
    /* for exceptions the sequence of option has to be rebuild */
    int       localArgc;
    char    **localArgv;

    staticArgc = argc;
    staticArgv = argv;
    localArgc = argc;
    localArgv = argv;

    /* parse command line */
    initializeParameters( );
    if( localArgc > 1 ) /* there are arguments */
    {
        localArgv++;
        localArgc--;
        parsingState = TRUE;
        InterruptCausingExceptionState = TRUE;
    }
    else
    {
        parsingState = FALSE;
        InterruptCausingExceptionState = FALSE;
    }
    while( ( localArgc >= 0 ) && ( parsingState == TRUE ) )
    {
      /* check for delimiter */
      if( checkArgument( *localArgv, "-d", "--delim" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfPairParameter ) )
          {
              localArgv++;
              setStringParameter( Delimiter, *localArgv );
              localArgv++;
              localArgc -= 2;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                               "delimiter" );
              parsingState = FALSE;
          }
      }
      /* check for max comment lines */
      else if( checkArgument( *localArgv, "-n", "--num" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfPairParameter ) )
          {
              localArgv++;
              setNumericParameter( CommentLines, *localArgv );
              localArgv++;
              localArgc -= 2;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                                "comment lines" );
              parsingState = FALSE;
          }
      }
      /* check for verbose */
      else if( checkArgument( *localArgv, "-v", "--verbose" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( Verbose );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, "verbose" );
              parsingState = FALSE;
          }
      }
      /* check for substitution (put) */
      else if( checkArgument( *localArgv, "-p", "--put" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( Put );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                               "substitution (put)" );
              parsingState = FALSE;
          }
      }
      /* check for extraction (get) */
      else if( checkArgument( *localArgv, "-g", "--get" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( Get );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                               "extraction (get)" );
              parsingState = FALSE;
          }
      }
      /* check for maintaining the basefile */
      else if( checkArgument( *localArgv, "-m", "--maintain" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( Maintain );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, "maintain" );
              parsingState = FALSE;
          }
      }
      /* check for exchange */
      else if( checkArgument( *localArgv, "-x", "--exchange" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( Exchange );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, "exchange" );
              parsingState = FALSE;
          }
      }
      /* check for removal within basefile */
      else if( checkArgument( *localArgv, "-r", "--remove" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( Remove );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, "remove" );
              parsingState = FALSE;
          }
      }
      /* check for protocolize parameters (passes arguments) */
      else if( checkArgument( *localArgv, "-a", "--arguments" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( Parameters );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                                "protocol parameters" );
              parsingState = FALSE;
          }
      }
      /* check for quiet mode */
      else if( checkArgument( *localArgv, "-q", "--quiet" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( Quiet );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, "quiet" );
              parsingState = FALSE;
          }
      }
      /* suppress comments */
      else if( checkArgument( *localArgv, "-s", "--suppress" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( Suppress );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                                "suppress comments" );
              parsingState = FALSE;
          }
      }
      /* check for comment marker */
      else if( checkArgument( *localArgv, "-c", "--char" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfPairParameter ) )
          {
              localArgv++;
              setStringParameter( CommentMarker, *localArgv );
              localArgv++;
              localArgc -= 2;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                                "comment marker" );
              parsingState = FALSE;
          }
      }
      /* check for quoting marker */
      /* l stands for lift - because other prefixes are already used */
      else if( checkArgument( *localArgv, "-l", "--quote" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfPairParameter ) )
          {
              localArgv++;
              setStringParameter( QuotingMarker, *localArgv );
              localArgv++;
              localArgc -= 2;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                                "quoting marker" );
              parsingState = FALSE;
          }
      }
      /* check for file, that denies (forbid) any changes for given variables */
      else if( checkArgument( *localArgv, "-f", "--forbidden" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfPairParameter ) )
          {
              localArgv++;
              setStringParameter( ForbiddenFile, *localArgv );
              localArgv++;
              localArgc -= 2;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                                "forbidden file name" );
              parsingState = FALSE;
          }
      }
      /* check for help */
      else if( checkArgument( *localArgv, "-h", "--help" ) == TRUE )
      {
          if( localArgc >= numberOfSimpleParameter )
          {
              setSimpleParameter( Help );
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, "help" );
          }
          parsingState = FALSE;
          InterruptCausingExceptionState = FALSE;
      }
      /* ignore end of file condition */
      else if( checkArgument( *localArgv, "-e", "--ignoreeof" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( IgnoreEOF );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                                "ignore EOF" );
              parsingState = FALSE;
          }
      }
      /* don't write variable blocks if they are defined only within base file */
      else if( checkArgument( *localArgv, "-i", "--ignoreDefinites" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( IgnoreDefinites );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                                "ignore Definites" );
              parsingState = FALSE;
          }
      }
      /* save trailing comments at the end of the file */
      else if( checkArgument( *localArgv, "-t", "--trailing" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( TrailingComment );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                                "trailing comment" );
              parsingState = FALSE;
          }
      }
      /* display current version */
      else if( checkArgument( *localArgv, "-V", "--version" ) == TRUE )
      {
          if( localArgc >= numberOfSimpleParameter )
          {
              setSimpleParameter( Version );
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                                "current version" );
          }
          parsingState = FALSE;
          localArgc = 0;
      }
      /* check whether metadata handling should be ignored */
      else if( checkArgument( *localArgv, "-nometadata", "--nometadata" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfSimpleParameter ) )
          {
              setSimpleParameter( NoMetadata );
              localArgv++;
              localArgc--;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException,
                                "current version" );
              parsingState = FALSE;
          }
      }
      /* check for logfile for special debugging - not commented feature */
      else if( checkArgument( *localArgv, "-logfile", "--logfile" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfPairParameter ) )
          {
              localArgv++;
              setStringParameter( DebuggingLogfile, *localArgv );
              localArgv++;
              localArgc -= 2;
          }
          else 
          {
              fillup_exception( __FILE__, __LINE__, FormatException,
                                "debugging log file" );
              parsingState = FALSE;
          }
      }
      /* check for debugging variable name - not commented feature */
      else if( checkArgument( *localArgv, "-variable", "--variable" ) == TRUE )
      {
          if( localArgc >= ( numberOfMandatoryParameters + numberOfPairParameter ) )
          {
              localArgv++;
              setStringParameter( DebuggingVariableName, *localArgv );
              localArgv++;
              localArgc -= 2;
          }
          else 
          {
              fillup_exception( __FILE__, __LINE__, FormatException,
                                "debuggin variable name" );
              parsingState = FALSE;
          }
      }
      /* check for unknown option */
      else if( compareStringsExactly( "-", *localArgv ) == Equal )
      {
          fillup_exception( __FILE__, __LINE__, FormatException, 
                            "invalid option" );
          parsingState = FALSE;
      }
      else
      {
          /* there are only the mandatory parameters */
          if( localArgc == ( numberOfMandatoryParameters + 1 ) )
          {
              setStringParameter( BaseFile, *localArgv );
              localArgv++;
              setStringParameter( AdditionalFile, *localArgv );
              localArgv++;
              setStringParameter( OutputFile, *localArgv );
              localArgc = 0;
          }
          /* presume that this is the old version of fillup */
          else if( localArgc == numberOfMandatoryParameters )
          {
              setStringParameter( BaseFile, *localArgv );
              setStringParameter( OutputFile, *localArgv );
              localArgv++;
              setStringParameter( AdditionalFile, *localArgv );
              localArgc = 0;
          }
          else
          {
              fillup_exception( __FILE__, __LINE__, FormatException, 
                                "mandatory  parameters" );
          }
          parsingState = FALSE;
      }
    }

    if( localArgc > 0)
    {
        displayUsageInformation( );
        if( InterruptCausingExceptionState == TRUE )
        {
            fillup_exception( __FILE__, __LINE__, NumberOfFormatException, 
                              "number of arguments" );
        }
        displayParameters( );
    }
    else
    {
        if( queryParameter( Parameters ) == TRUE )
        {
            displayParameters( );
        }

        if( queryParameter( Version ) == TRUE )
        {
            displayVersion( );
        }
        else
        {
            initWatchdog( );
            if( Success == instantiateParameters( ) )
            {
                startParser( );
            }
        }
    }

    return( EXIT_SUCCESS );
}

/*----------------------------------------------------------------------------*/
