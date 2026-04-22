#ifndef CLAMAV_TYPES_H_MULTILIB
#define CLAMAV_TYPES_H_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "clamav-types-32.h"
#elif __WORDSIZE == 64
# include "clamav-types-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
