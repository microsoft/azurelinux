/* qvglobal_p.h */
/* This file is here to prevent a file conflict on multiarch systems.  A
 * conflict will occur because qconfig.h has arch-specific definitions.
 *
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#ifndef MULTILIB_QV4GLOBAL_H
#define MULTILIB_QV4GLOBAL_H

#ifndef __WORDSIZE
#include <bits/wordsize.h>
#endif

#if __WORDSIZE == 32
#include <private/qv4global_p-32.h>
#elif __WORDSIZE == 64
#include <private/qv4global_p-64.h>
#else
#error "unexpected value for __WORDSIZE macro"
#endif

#endif

