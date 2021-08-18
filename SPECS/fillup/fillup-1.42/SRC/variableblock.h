
/*----------------------------------------------------------------------------*/
/*                                                                            */
/* Copyrights to S.u.S.E. GmbH Fuerth (c) 1998                                */
/*                                                                            */
/* Time-stamp:                                                                */
/* Project:    fillup                                                         */
/* Module:     variableblock                                                  */
/* Filename:   variableblock.h                                                */
/* Author:     Joerg Dippel (jd)                                              */
/* Description:                                                               */
/*                                                                            */
/*     export interface for datastructure variable block                      */
/*                                                                            */
/*----------------------------------------------------------------------------*/

#ifndef __VARIABLEBLOCK_H__
#define __VARIABLEBLOCK_H__

/*--------------------------------- IMPORTS ----------------------------------*/


/*---------------------------------- TYPES -----------------------------------*/

typedef enum
{
    UndefinedBlock,
    CompleteVariableBlock,
    CommentedVariableBlock,
    TrailingCommentBlock,
    AssignmentBlock,
    VariableNameBlock
} BlockClass_t;

typedef enum
{
    Undefined,
    Ignored,
    IgnoredButRemoved,
    Output,
    OutputButRemoved
} Eval_t;

typedef struct VariableBlock
{
    BlockClass_t              Classifier;
    Eval_t                    EvaluationClass;
    struct VariableBlock    * association;
    char                    * beginOfVariableBlock;
    long                      lengthOfBlock;
    long                      offsetVariableName;
    long                      offsetDelimiter;
    long                      numberOfEmptyLines;
    long                      numberOfCommentLines;
    struct VariableBlock    * pred;
    struct VariableBlock    * succ;
} VariableBlock_t;

/*--------------------------- FUNCTION PROTOTYPES ----------------------------*/

void
setVClassifier
(
    VariableBlock_t      * outputBuffer,     /* in */
    BlockClass_t           Classifier        /* in */
);

BlockClass_t
getVClassifier
(
    VariableBlock_t      * outputBuffer      /* in */
);

void
setVEvaluationClass
(
    VariableBlock_t      * outputBuffer,     /* in */
    Eval_t                 EvaluationClass   /* in */
);

Eval_t
getVEvaluationClass
(
    VariableBlock_t      * outputBuffer      /* in */
);

void
setVAssociation
(
    VariableBlock_t      * outputBuffer,     /* in */
    VariableBlock_t      * associatedBuffer  /* in */
);

VariableBlock_t *
getVAssociation
(
    VariableBlock_t      * outputBuffer      /* in */
);

void
setVBeginOfBlock
(
    VariableBlock_t      * outputBuffer,         /* in */
    char                 * beginOfVariableBlock  /* in */
);

void
getVBeginOfBlock
(
    VariableBlock_t      * outputBuffer,         /* in */
    char                ** beginOfVariableBlock /* out */
);

void
setVLength
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   length            /* in */
);

void
addVLength
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   additionalLength  /* in */
);

long
getVLength
(
    VariableBlock_t      * outputBuffer      /* in */
);

void
setVOffsetOfVariableName
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   offset            /* in */
);

long
getVOffsetOfVariableName
(
    VariableBlock_t      * outputBuffer      /* in */
);

long
getVOffsetOfDelimiter
(
    VariableBlock_t      * outputBuffer      /* in */
);

void
setVOffsetOfDelimiter
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   offset            /* in */
);

void
setVNumberOfEmptyLines
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   value             /* in */
);

void
incVNumberOfEmptyLines
(
    VariableBlock_t      * outputBuffer      /* in */
);

void
setVNumberOfCommentLines
(
    VariableBlock_t      * outputBuffer,     /* in */
    long                   value             /* in */
);

long
getVNumberOfCommentLines
(
    VariableBlock_t      * outputBuffer      /* in */
);

void
incVNumberOfCommentLines
(
    VariableBlock_t      * outputBuffer      /* in */
);

void
setVPred
(
    VariableBlock_t      * outputBuffer,     /* in */
    VariableBlock_t      * pointer           /* in */
);

VariableBlock_t *
getVPred
(
    VariableBlock_t      * outputBuffer      /* in */
);

void
setVSucc
(
    VariableBlock_t      * outputBuffer,     /* in */
    VariableBlock_t      * pointer           /* in */
);

VariableBlock_t *
getVSucc
(
    VariableBlock_t      * outputBuffer      /* in */
);

/*----------------------------------------------------------------------------*/

#endif /* __VARIABLEBLOCK_H__ */
