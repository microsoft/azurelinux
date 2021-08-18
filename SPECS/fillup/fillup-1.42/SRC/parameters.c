
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to S.u.S.E. GmbH Fuerth (c) 1998                                */
/*                                                                            */
/* Time-stamp:                                                                */
/* Project:    fillup                                                         */
/* Module:     parameters                                                     */
/* Filename:   parameters.c                                                   */
/* Author:     Joerg Dippel (jd)                                              */
/* Description:                                                               */
/*                                                                            */
/*     administration of parameters read from command input.                  */
/*                                                                            */
/*----------------------------------------------------------------------------*/

/*--------------------------------- IMPORTS ----------------------------------*/

#include "portab.h"
#include "services.h"

#include "fillup_cfg.h"
#include "parameters.h"
#include "file.h"

/*---------------------------------- TYPES -----------------------------------*/

typedef enum
{
    IsSet,
    IsStillUndefined,
    IsOverwritten
} ParameterState_t;

/*-------------------------------- VARIABLES ---------------------------------*/

static  ParameterState_t       parameterDelimiter;
static  ParameterState_t       parameterCommentLines;
static  ParameterState_t       parameterVerbose;
static  ParameterState_t       parameterPut;
static  ParameterState_t       parameterGet;
static  ParameterState_t       parameterMaintain;
static  ParameterState_t       parameterExchange;
static  ParameterState_t       parameterRemove;
static  ParameterState_t       parameterParameters;
static  ParameterState_t       parameterQuiet;
static  ParameterState_t       parameterSuppress;
static  ParameterState_t       parameterCommentMarker;
static  ParameterState_t       parameterQuotingMarker;
static  ParameterState_t       parameterForbiddenFile;
static  ParameterState_t       parameterHelp;
static  ParameterState_t       parameterIgnoreEOF;
static  ParameterState_t       parameterIgnoreDefinites;
static  ParameterState_t       parameterTrailingComment;
static  ParameterState_t       parameterVersion;
static  ParameterState_t       parameterNoMetadata;
static  ParameterState_t       parameterDebuggingLogfile;
static  ParameterState_t       parameterDebuggingVariableName;
static  ParameterState_t       parameterBaseFile;
static  ParameterState_t       parameterAdditionalFile;
static  ParameterState_t       parameterOutputFile;
 
static  const char           * delimiterString;
static  const char           * commentLinesString;
static  const char           * commentMarkerString;
static  const char           * quotingMarkerString;
static  const char           * forbiddenFileName;
static  const char           * debuggingLogfile;
static  const char           * debuggingVariableName;
static  const char           * baseFileName;
static  const char           * additionalFileName;
static  const char           * outputFileName;
static  unsigned long          commentLinesValue;

/*-------------------------------- FUNCTIONS ---------------------------------*/

/*----------------------------- IMPLEMENTATION -------------------------------*/

/*---------------- initializeParameters -----------------*/

void
initializeParameters
(
    void
)
{
    setStringParameter( Delimiter, &cfg_delimiter[ 0 ] );
    parameterCommentLines = IsStillUndefined;
    parameterVerbose = IsStillUndefined;
    parameterPut = IsStillUndefined;
    parameterGet = IsStillUndefined;
    parameterMaintain = IsSet;
    parameterExchange = IsStillUndefined;
    parameterRemove = IsStillUndefined;
    parameterParameters = IsStillUndefined;
    parameterQuiet = IsStillUndefined;
    parameterSuppress = IsStillUndefined;
    setStringParameter( CommentMarker, &cfg_commentMarker[ 0 ] );
    setStringParameter( QuotingMarker, &cfg_quotingMarker[ 0 ] );
    setStringParameter( ForbiddenFile, "" );     /* only for initialization */
    parameterForbiddenFile = IsStillUndefined;
    parameterHelp = IsStillUndefined;
    parameterIgnoreEOF = IsStillUndefined;
    parameterIgnoreDefinites = IsStillUndefined;
    parameterTrailingComment = IsStillUndefined;
    parameterVersion = IsStillUndefined;
    parameterNoMetadata = IsStillUndefined;
    parameterDebuggingLogfile = IsStillUndefined;
    parameterDebuggingVariableName = IsStillUndefined;
    parameterBaseFile = IsStillUndefined;
    parameterAdditionalFile = IsStillUndefined;
    parameterOutputFile = IsStillUndefined;
}

/*------------------ setStringParamter ------------------*/

void
setStringParameter
(
    ParameterSpecification_t    parameterType,     /* in */
    const char                * parameterId        /* in */
)
{
    switch( parameterType )
    {
        case Delimiter:
           parameterDelimiter = IsSet;
           delimiterString = parameterId;
           break;

        case CommentMarker:
           parameterCommentMarker = IsSet;
           commentMarkerString = parameterId;
           break;

        case QuotingMarker:
           parameterQuotingMarker = IsSet;
           quotingMarkerString = parameterId;
           break;

        case ForbiddenFile:
           parameterForbiddenFile = IsSet;
           forbiddenFileName = parameterId;
           break;

        case DebuggingLogfile:
           parameterDebuggingLogfile = IsSet;
           debuggingLogfile = parameterId;
           break;

        case DebuggingVariableName:
           parameterDebuggingVariableName = IsSet;
           debuggingVariableName = parameterId;
           break;

        case BaseFile:
           parameterBaseFile = IsSet;
           baseFileName = parameterId;
           break;

        case AdditionalFile:
           parameterAdditionalFile = IsSet;
           additionalFileName = parameterId;
           break;

        case OutputFile:
           parameterOutputFile = IsSet;
           outputFileName = parameterId;
           break;

        default:
            fillup_exception( __FILE__, __LINE__, DefaultBranchException, 
                              "setStringParameter" );
            break;
    }
}

/*----------------- setNumericParameter -----------------*/

void
setNumericParameter
(
    ParameterSpecification_t    parameterType,     /* in */
    const char                * parameterId        /* in */
)
{
    switch( parameterType )
    {
        case CommentLines:
           parameterCommentLines = IsSet;
           commentLinesString = parameterId;
           ( void )getCardinal( parameterId, &commentLinesValue );
           break;

        default:
            fillup_exception( __FILE__, __LINE__, DefaultBranchException, 
                              "setNumericParameter" );
            break;
    }
}

/*------------------ setSimpleParamter ------------------*/

void
setSimpleParameter
(
    ParameterSpecification_t    parameterType      /* in */
)
{
    switch( parameterType )
    {
        case Verbose:
           parameterVerbose = IsSet;
           if( IsSet == parameterQuiet )
           {
               parameterQuiet = IsOverwritten;
           }
           break;

        case Put:
           parameterPut = IsSet;
           break;

        case Get:
           parameterGet = IsSet;
           break;

        case Maintain:
           parameterMaintain = IsSet;
           if( IsSet == parameterExchange )
           {
               parameterExchange = IsOverwritten;
           }
           break;

        case Exchange:
           parameterExchange = IsSet;
           if( IsSet == parameterMaintain )
           {
               parameterMaintain = IsOverwritten;
           }
           break;

        case Remove:
           parameterRemove = IsSet;
           break;

        case Parameters:
           parameterParameters = IsSet;
           break;

        case Quiet:
           parameterQuiet = IsSet;
           if( IsSet == parameterVerbose )
           {   
               parameterVerbose = IsOverwritten;
           }
           break;

        case Suppress:
           parameterSuppress = IsSet;
           break;

        case Help:
           parameterHelp = IsSet;
           break;

        case IgnoreEOF:
           parameterIgnoreEOF = IsSet;
           break;

        case IgnoreDefinites:
           parameterIgnoreDefinites = IsSet;
           break;

        case TrailingComment:
           parameterTrailingComment = IsSet;
           break;

        case Version:
           parameterVersion = IsSet;
           break;

        case NoMetadata:
           parameterNoMetadata = IsSet;
           break;

        default:
            fillup_exception( __FILE__, __LINE__, DefaultBranchException, 
                              "setSimpleParameter" );
            break;
    }
}

/*-------------------- queryParameter -------------------*/

BOOLEAN 
queryParameter
(
    ParameterSpecification_t    parameterType      /* in */
)
{
    BOOLEAN    returnValue;

    returnValue = FALSE;
    switch( parameterType )
    {
        case Parameters:
            if( parameterParameters == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        case Version:
            if( parameterVersion == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        case NoMetadata:
            if( parameterNoMetadata == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        case ForbiddenFile:
            if( parameterForbiddenFile == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        case TrailingComment:
            if( parameterTrailingComment == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        case Remove:
            if( parameterRemove == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        case Maintain:
            if( parameterMaintain == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        case Exchange:
            if( parameterExchange == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        case Verbose:
            if( parameterVerbose == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        case IgnoreDefinites:
            if( parameterIgnoreDefinites == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        case DebuggingLogfile:
            if( parameterDebuggingLogfile == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        case DebuggingVariableName:
            if( parameterDebuggingVariableName == IsSet )
            {
                returnValue = TRUE;
            }
            break;

        default:
            fillup_exception( __FILE__, __LINE__, DefaultBranchException, 
                              "queryParameter" );
            break;
    }

    return( returnValue );
}

/*----------------- queryStringParameter ----------------*/

void
queryStringParameter
(
    ParameterSpecification_t    parameterType,     /* in */
    char                     ** parameterString   /* out */
)
{
    switch( parameterType )
    {
        case Delimiter:
            *parameterString = ( char * )delimiterString;
            break;

        case CommentMarker:
            *parameterString = ( char * )commentMarkerString;
            break;

        case DebuggingLogfile:
            *parameterString = ( char * )debuggingLogfile;
            break;

        case DebuggingVariableName:
            *parameterString = ( char * )debuggingVariableName;
            break;

        case BaseFile:
            *parameterString = ( char * )baseFileName;
            break;

        case OutputFile:
            *parameterString = ( char * )outputFileName;
            break;

        default:
            fillup_exception( __FILE__, __LINE__, DefaultBranchException, 
                              "queryStringParameter" );
            break;
    }
}

/*------------------- displayParameters -----------------*/

void
displayParameters
(
    void
)
{
    if( parameterDelimiter == IsSet )
    {
        displayStderrString( "parameter Delimiter is set" );
        displayStderrString( delimiterString );
    }
    if( parameterCommentLines == IsSet )
    {
        displayStderrString( "parameter CommentLines is set to" );
        displayStderrString( commentLinesString );
    }
    if( parameterVerbose == IsSet )
    {
        displayStderrString( "parameter Verbose is set" );
    }
    if( parameterPut == IsSet )
    {
        displayStderrString( "parameter Put is set" );
    }
    if( parameterGet == IsSet )
    {
        displayStderrString( "parameter Get is set" );
    }
    if( parameterMaintain == IsSet )
    {
        displayStderrString( "parameter Maintain is set" );
    }
    if( parameterExchange == IsSet )
    {
        displayStderrString( "parameter Exchange is set" );
    }
    if( parameterRemove == IsSet )
    {
        displayStderrString( "parameter Remove is set" );
    }
    if( parameterParameters == IsSet )
    {
        displayStderrString( "parameter Parameters is set" );
    }
    if( parameterQuiet == IsSet )
    {
        displayStderrString( "parameter Quiet is set" );
    }
    if( parameterSuppress == IsSet )
    {
        displayStderrString( "parameter Suppress is set" );
    }
    if( parameterCommentMarker == IsSet )
    {
        displayStderrString( "parameter CommentMarker is set to" );
        displayStderrString( commentMarkerString );
    }
    if( parameterQuotingMarker == IsSet )
    {
        displayStderrString( "parameter QuotingMarker is set to" );
        displayStderrString( quotingMarkerString );
    }
    if( parameterHelp == IsSet )
    {
        displayStderrString( "parameter Help is set" );
    }
    if( parameterIgnoreEOF == IsSet )
    {
        displayStderrString( "parameter IgnoreEOF is set" );
    }
    if( parameterIgnoreDefinites == IsSet )
    {
        displayStderrString( "parameter IgnoreDefinites is set" );
    }
    if( parameterTrailingComment == IsSet )
    {
        displayStderrString( "parameter TrailingComment is set" );
    }
    if( parameterVersion == IsSet )
    {
        displayStderrString( "parameter Version is set" );
    }
    if( parameterNoMetadata == IsSet )
    {
        displayStderrString( "parameter NoMetadata is set" );
    }
    if( parameterBaseFile == IsSet )
    {
        displayStderrString( "parameter BaseFile is set to" );
        displayStderrString( baseFileName );
    }
    if( parameterAdditionalFile == IsSet )
    {
        displayStderrString( "parameter AdditionalFile is set to" );
        displayStderrString( additionalFileName );
    }
    if( parameterOutputFile == IsSet )
    {
        displayStderrString( "parameter OutputFile is set to" );
        displayStderrString( outputFileName );
    }
    if( parameterForbiddenFile == IsSet )
    {
        displayStderrString( "parameter ForbiddenFile is set to" );
        displayStderrString( forbiddenFileName );
    }
}

/*--------------- displayUsageInformation ---------------*/

void
displayUsageInformation
(
    void
)
{
    if( IsStillUndefined == parameterQuiet )
    {
        displayStderrString( "" );
        displayStderrString( "usage: fillup [options] <base file>"
                             " <additional file> <output file>" );
        displayStderrString( "  valid options are:" );
        displayStderrString( "      -h, --help               "
                             "this message" );
        displayStderrString( "      -e, --ignoreeof          "
                             "end of file allowed anywhere" );
        displayStderrString( "      -i, --ignoreDefinites    "
                             "dont write variables to the output if they are only defined in basefile" );
        displayStderrString( "      -q, --quiet              "
                             "no output to screen" );
        displayStderrString( "      -s, --suppress           "
                             "suppress output of comments" );
        displayStderrString( "      -t, --trailing           "
                             "save trailing comments at end of file" );
        displayStderrString( "      -v, --verbose            "
                             "maximum output to screen" );
        displayStderrString( "      -V, --version            "
                             "print fillup version and exit" );
        displayStderrString( "      -nometadata, --nometadata "
                             "no metadata information merged: keep fillup 1.10 functionalty" );
        displayStderrString( "      -f | --forbidden <file>  "
                             "use <file> to forbid changes for given variables" );
        displayStderrString( "      -c | --char <char>       "
                             "use <char> as comment marker" );
        displayStderrString( "      -l | --quote <char>      "
                             "use <char> as quoting marker" );
        displayStderrString( "      -d | --delim <char>      "
                             "use <char> as delimiter" );
        displayStderrString( "      -n, --num                "
                             "check for max comment lines" );
        displayStderrString( "      -p, --put                "
                             "check for substitution (put)" );
        displayStderrString( "      -g, --get                "
                             "check for extraction (get)" );
        displayStderrString( "      -m, --maintain           "
                             "check for maintaining the basefile" );
        displayStderrString( "      -x, --exchange           "
                             "check for exchange" );
        displayStderrString( "      -r, --remove             "
                             "check for removal within basefile" );
        displayStderrString( "      -a, --arguments          "
                             "check for passed arguments" );
        displayStderrString( "" );
        displayStderrString( "Please refer also to the related manpage." );
        displayStderrString( "Within the options section, there are hints" );
        displayStderrString( "to options which are not/no longer supported." );
        displayStderrString( "" );
    }
}

/*---------------- instantiateParameters ----------------*/

Service_t
instantiateParameters
(
    void
)
{
    Service_t    returnValue;

    if( FileOperationsSuccessful == readFile( BaseFile, baseFileName ) )
    {
        if( FileOperationsSuccessful == 
            readFile( AdditionalFile, additionalFileName ) )
        {
            if( parameterForbiddenFile != IsSet )
            {
                /* option --forbidden not defined */
                returnValue = Success;
            }
            else if( FileOperationsSuccessful == 
                     readFile( ForbiddenFile, forbiddenFileName ) )
            {
                 returnValue = Success;
            }
            else
            {
                returnValue = Error;
            }
        }
        else
        {
            /* here the buffer for baseFile has to be cleared               */
            /* but the program terminates without parsing - nothing is done */
            returnValue = Error;
        }
    }
    else
    {
        returnValue = Error;
    }

    return( returnValue );
}

/*----------------------------------------------------------------------------*/
