
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to S.u.S.E. GmbH Fuerth (c) 1998                                */
/*                                                                            */
/* Time-stamp:                                                                */
/* Project:    fillup                                                         */
/* Module:     variableblock                                                  */
/* Filename:   variableblock.c                                                */
/* Author:     Joerg Dippel (jd)                                              */
/* Description:                                                               */
/*                                                                            */
/*     defines a datastructure block variable and member functions            */
/*                                                                            */
/*----------------------------------------------------------------------------*/

/*--------------------------------- IMPORTS ----------------------------------*/

#include "variableblock.h"

/*---------------------------------- TYPES -----------------------------------*/
/*----------------------------- IMPLEMENTATION -------------------------------*/


/*--------------- setVClassifier -----------------*/

void
setVClassifier
(
    VariableBlock_t      * outputBuffer,     /* in */
    BlockClass_t           Classifier        /* in */
)
{
    outputBuffer->Classifier = Classifier;
}

/*--------------- getVClassifier -----------------*/

BlockClass_t
getVClassifier
(
    VariableBlock_t      * outputBuffer      /* in */
)
{
    return( outputBuffer->Classifier );
}

/*------------- setVEvaluationClass --------------*/

void
setVEvaluationClass
(
    VariableBlock_t      * outputBuffer,     /* in */
    Eval_t                 EvaluationClass   /* in */
)
{
    outputBuffer->EvaluationClass = EvaluationClass;
}

/*------------- getVEvaluationClass --------------*/

Eval_t
getVEvaluationClass
(
    VariableBlock_t      * outputBuffer      /* in */
)
{
    return( outputBuffer->EvaluationClass );
}

/*--------------- setVAssociation ----------------*/

void
setVAssociation
(
    VariableBlock_t      * outputBuffer,     /* in */
    VariableBlock_t      * associatedBuffer  /* in */
)
{
    outputBuffer->association = associatedBuffer;
}

/*--------------- getVAssociation ----------------*/

VariableBlock_t *
getVAssociation
(
    VariableBlock_t      * outputBuffer      /* in */
)
{
    return( outputBuffer->association );
}


/*----------------- setVBeginOfBlock -------------------*/

void
setVBeginOfBlock
(
    VariableBlock_t      * outputBuffer,         /* in */
    char                 * beginOfVariableBlock  /* in */
)
{
    outputBuffer->beginOfVariableBlock = beginOfVariableBlock;
}

/*----------------- getVBeginOfBlock -------------------*/

void
getVBeginOfBlock
(
    VariableBlock_t      * outputBuffer,         /* in */
    char                ** beginOfVariableBlock  /* out */
)
{
    *beginOfVariableBlock = outputBuffer->beginOfVariableBlock;
}

/*----------------- setVLength -------------------*/

void
setVLength
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   length            /* in */
)
{
    outputBuffer->lengthOfBlock = length;
}

/*----------------- addVLength -------------------*/

void
addVLength
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   additionalLength  /* in */
)
{
    outputBuffer->lengthOfBlock = outputBuffer->lengthOfBlock + additionalLength;
}

/*----------------- getVLength -------------------*/

long
getVLength
(
    VariableBlock_t      * outputBuffer      /* in */
)
{
    return( outputBuffer->lengthOfBlock );
}

/*---------- setVOffsetOfVariableName ------------*/

void
setVOffsetOfVariableName
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   offset            /* in */
)
{
    outputBuffer->offsetVariableName = offset;
}

/*---------- getVOffsetOfVariableName ------------*/

long
getVOffsetOfVariableName
(
    VariableBlock_t      * outputBuffer      /* in */
)
{
    return( outputBuffer->offsetVariableName );
}

/*------------ setVOffsetOfDelimiter -------------*/

void
setVOffsetOfDelimiter
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   offset            /* in */
)
{
    outputBuffer->offsetDelimiter = offset;
}

/*------------ getVOffsetOfDelimiter -------------*/

long
getVOffsetOfDelimiter
(
    VariableBlock_t      * outputBuffer      /* in */
)
{
    return( outputBuffer->offsetDelimiter );
}

/*----------- setVNumberOfEmptyLines -------------*/

void
setVNumberOfEmptyLines
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   value             /* in */
)
{
    outputBuffer->numberOfEmptyLines = value;
}

/*----------- incVNumberOfEmptyLines -------------*/

void
incVNumberOfEmptyLines
(
    VariableBlock_t      * outputBuffer      /* in */
)
{
    outputBuffer->numberOfEmptyLines = outputBuffer->numberOfEmptyLines + 1;
}

/*----------- setVNumberOfCommentLines ------------*/

void
setVNumberOfCommentLines
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   value             /* in */
)
{
    outputBuffer->numberOfCommentLines = value;
}

/*----------- getVNumberOfCommentLines ------------*/

long
getVNumberOfCommentLines
(
    VariableBlock_t      * outputBuffer      /* in */
)
{
    return( outputBuffer->numberOfCommentLines );
}

/*----------- incVNumberOfCommentLines ------------*/

void
incVNumberOfCommentLines
(
    VariableBlock_t      * outputBuffer      /* in */
)
{
   outputBuffer->numberOfCommentLines = outputBuffer->numberOfCommentLines + 1;
}

/*------------------- setVPred --------------------*/

void
setVPred
(
    VariableBlock_t      * outputBuffer,     /* in */
    VariableBlock_t      * pointer           /* in */
)
{
    outputBuffer->pred = pointer;
}

/*------------------- getVPred --------------------*/

VariableBlock_t * 
getVPred
(
    VariableBlock_t      * outputBuffer      /* in */
)
{
    return( outputBuffer->pred );
}

/*------------------- setVSucc --------------------*/

void
setVSucc
(
    VariableBlock_t      * outputBuffer,     /* in */
    VariableBlock_t      * pointer           /* in */
)
{
    outputBuffer->succ = pointer;
}

/*------------------- getVSucc --------------------*/

VariableBlock_t * 
getVSucc
(
    VariableBlock_t      * outputBuffer      /* in */
)
{
    return( outputBuffer->succ );
}

/*----------------------------------------------------------------------------*/

