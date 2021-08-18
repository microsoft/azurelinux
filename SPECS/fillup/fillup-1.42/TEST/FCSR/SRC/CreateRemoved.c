
#include <stdlib.h>
#include <stdio.h>

static char *metadataKeyword[] = 
    { "Path", "Description", "Type", "Default", 
      "Config", "ServiceReload", "ServiceRestart", "Command", "PreSaveCommand" };

static void
CreateName
(
    char    *buffer,
    int      characterOffset,
    char     fileSelector
)
{
    *buffer++ = 'A' + characterOffset;
    *buffer++ = fileSelector;
    *buffer++ = 'a' + characterOffset;
    *buffer++ = 'a' + characterOffset;
    *buffer++ = fileSelector;
    *buffer++ = fileSelector;
    *buffer++ = fileSelector;
    *buffer++ = 'a' + characterOffset;
    *buffer++ = 'a' + characterOffset;
    *buffer++ = 'a' + characterOffset;
    *buffer++ = 'a' + characterOffset;
    *buffer++ = 'a' + characterOffset;
    *buffer = '\0';
}

int main
(
    int       argc,
    char     *argv[]
)
{
    long      argument;
    size_t    numberOfKeywords;
    size_t    index;
    char      metadataVariableName[64]; 

    if( argc > 1 )
    {
        argument = atol( argv[ 1 ] );
        numberOfKeywords = sizeof( metadataKeyword ) / sizeof( char * ); 

        printf( "\n" );
        index = 0;

        if( argument & 0x2L ) return;   /* single variable but removed */

        argument = argument >> 2;
        while( ( index < numberOfKeywords ) && ( argument > 0 ) )
        {
            if( ( argument & 0x1L ) == 0x01L )
            {
                CreateName( metadataVariableName, index, '1' );
                printf( "## %s: \"This is the value of metadata variable: %s\"\n", metadataKeyword[ index ], metadataVariableName );
            }
            argument = argument >> 2;
            index++;
        }
        printf( "# \n");
        printf( "# This is a comment for automatically generated basefile\n" );
        printf( "# \n");
        printf( "TESTVARIABLE=ShiftRegister of basefile\n\n");
    }

    return( 0 );
}

