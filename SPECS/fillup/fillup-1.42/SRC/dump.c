
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to SuSE Linux AG        (c) 2003                                */
/*                                                                            */
/* Project:    fillup                                                         */
/* Module:     dump                                                           */
/* Filename:   dump.c                                                         */
/* Author:     Joerg Dippel                                                   */
/* Description:                                                               */
/*                                                                            */
/*----------------------------------------------------------------------------*/

/*--------------------------------- IMPORTS ----------------------------------*/

#include <stdio.h>
#include <stdlib.h>

#include "getArguments.h"
#include "variableblock.h"
#include "services.h"
#include "parser.h"
#include "dump.h"

/*----------------------------- IMPLEMENTATION -------------------------------*/

/*---------------------- dump ----------------------*/
void
dump
(
   VariableBlock_t           * variable       /* in */
)
{
    FILE         *filePointer;
    char         *option;
    char         *variableblock;

    /* generates a unique temporary filename using the */
    /* path prefix P_tmpdir defined in <stdio.h> */
    if( ( filePointer = tmpfile( ) ) != NULL )
    {
        fillupDumpFileCreated( );

        initializeAccessToParameters();
        dumpBlock( "\n--- dumping options for fillup call --- \n\tfillup", 
                   49, filePointer );

        while( ( option = getAccessToParameters() ) != ( char * )NULL )
        {
             dumpBlock( " ", 1, filePointer );
             dumpBlock( option, stringLength( option), filePointer );
        }
        dumpBlock( "\n\n", 2, filePointer );

        dumpBlock( "\n--- dumping input file <basefile> --- \n", 40, filePointer );
        dumpBasefile( filePointer );
        dumpBlock( "\n--- <basefile> ---\n", 20, filePointer );
  
        dumpBlock( "\n--- dumping input file <addfile> --- \n", 39, filePointer );
        dumpAddfile( filePointer );
        dumpBlock( "\n--- <addfile> ---\n", 19, filePointer );
  
        dumpBlock( "\n--- dumping variable --- \n", 27, filePointer );
        getVBeginOfBlock( variable, &variableblock );
        dumpBlock( variableblock, getVLength( variable ), filePointer );
        dumpBlock( "\n--- variable dumped --- \n", 26, filePointer );

        fclose( filePointer );
    }
}

/*----------------------------------------------------------------------------*/

