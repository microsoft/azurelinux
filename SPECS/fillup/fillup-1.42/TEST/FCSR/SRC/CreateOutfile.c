
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
    long      mask;
    long      maintainance;
    size_t    numberOfKeywords;
    size_t    index;
    char      metadataVariableName[64]; 

    if( argc > 1 )
    {
        argument = atol( argv[ 1 ] );
        maintainance = argument & 0x1L;
        numberOfKeywords = sizeof( metadataKeyword ) / sizeof( char * ); 
        mask = 0x1L;
        mask = mask << ( ( 2 * numberOfKeywords ) + 2 );
        mask = mask - 1;

        printf( "\n" );
        index = 0;
        argument = argument >> 2;
        argument &= mask;
        while( ( index < numberOfKeywords ) && ( argument > 0 ) )
        {
            if( ( argument & 0x2L ) == 0x02L )
            {
                CreateName( metadataVariableName, index, '2' );
                printf( "## %s: \"This is the value of metadata variable: %s\"\n", metadataKeyword[ index ], metadataVariableName );
            }
            else if( ( ! maintainance ) && ( ( argument & 0x1L ) == 0x01L ) )
            {
                CreateName( metadataVariableName, index, '1' );
                printf( "## %s: \"This is the value of metadata variable: %s\"\n", metadataKeyword[ index ], metadataVariableName );
            }

            argument = argument >> 2;
            argument &= mask;
            index++;
        }
        printf( "# \n");
        printf( "# This is a comment for automatically generated %s\n", ( maintainance ) ? "addfile" : "basefile");
        printf( "# \n");
        printf( "TESTVARIABLE=ShiftRegister of %s\n\n", ( maintainance ) ? "addfile" : "basefile" );
    }

    return( 0 );
}

