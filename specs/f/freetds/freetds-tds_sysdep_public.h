/*
 *  To avoid multiarch conflicts, we differentiate the 32/64 bit length
 *  specific header names. This file is a wrapper to include the proper
 *  arch-specific header at compile time.
 */

#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include <tds_sysdep_public_32.h>
#elif __WORDSIZE == 64
#include <tds_sysdep_public_64.h>
#else
#error "Unknown word size"
#endif
