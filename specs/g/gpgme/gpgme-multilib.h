/* gpgme-multilib.h */
/* This file is here to prevent a file conflict on multiarch systems.  A
 * conflict will occur because gpgme.h has arch-specific definitions.
 *
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#ifndef GPGME_MULTILIB_H
#define GPGME_MULTILIB_H
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "gpgme-32.h"
#elif __WORDSIZE == 64
#include "gpgme-64.h"
#else
#error "unexpected value for __WORDSIZE macro"
#endif

#endif

