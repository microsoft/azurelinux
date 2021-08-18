
/**************************************************************************************/
/*                                                             			      */
/* PORTAB.H                                                    			      */
/*                                                             			      */
/* Use of this file may make your code compatible with all C   			      */
/* compilers listed.                                           			      */
/*                                                             			      */
/**************************************************************************************/

/**************************************************************************************/
/* ENVIRONMENT                                                 			      */
/**************************************************************************************/

#ifndef __PORTAB_H__
#define __PORTAB_H__

/**************************************************************************************/
/* STANDARD TYPE DEFINITIONS                                    		      */
/**************************************************************************************/

#define VOID    void		/* no return value		      		      */
#define CHAR    char		/* signed char                 			      */
#define UCHAR   unsigned char	/* unsigned character				      */
#define LONG    long int	/* Signed long (32 bits)       			      */
#define ULONG   unsigned long	/* Unsigned long               			      */

#define UBYTE   unsigned char	/* same as UCHAR				      */
#define BYTE    char		/* same as CHAR					      */

#define BOOLEAN int		/* 2 valued (true/false)       			      */

#define FLOAT   float		/* Single precision float      			      */
#define DOUBLE  double		/* Double precision float      			      */

#define INT     int		/* A machine dependent int     			      */
#define UINT    unsigned int	/* A machine dependent uint    			      */

#define REG     register	/* Register variable           			      */
#define AUTO    auto		/* Local to function           			      */
#define EXTERN  extern		/* External variable           			      */
#define LOCAL   static		/* Local to module             			      */
#define MLOCAL  LOCAL		/* Local to module             			      */
#define GLOBAL			/* Global variable (extern or nothing declaration)    */


/**************************************************************************************/
/* COMPILER DEPENDENT DEFINITIONS                              			      */
/**************************************************************************************/

#if HPC | GCC			/* ANSI compilers        			      */
#define ANSI 1
#define _(params) params        /* Parameter checking          			      */
#else
#define ANSI 0
#define _(params) ()            /* No parameter checking       			      */
#endif

#if GCC
#define INLINE __inline__
#else
#define INLINE
#endif


/**************************************************************************************/
/* MISCELLANEOUS DEFINITIONS                                  			      */
/**************************************************************************************/

#ifndef FALSE
#define FALSE   (BOOLEAN)0	/* Function FALSE value        			      */
#endif

#ifndef TRUE
#define TRUE    (BOOLEAN)1	/* Function TRUE  value        			      */
#endif

#define FAIL    (-1)		/* return-value of a failed function 		      */
#define FAILURE (-1)		/* Function failure return val 			      */
#define SUCCESS 0		/* Function success return val 			      */
#define FOREVER for (;;)	/* Infinite loop declaration   			      */
#define EOS     '\0'		/* End of string value         			      */

#define EOL         '\n'	/* End Of Line                    		      */
#define WHITE_SPACE " \t\n"	/* chars seen as blanks       		      	      */


#ifndef NULL
#define NULL    0L		/* Null long value             			      */
#endif

#ifndef EOF
#define EOF     (-1)		/* EOF value                   			      */
#endif

#endif /* __PORTAB_H__ */

/*------------------------------ end module portab.h ---------------------------------*/

