/* qt3dcore-config_p.h */
/* This file is here to prevent a file conflict on multiarch systems.  A
 * conflict will occur because qt3dcore-config_p.h has arch-specific definitions.
 *
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#ifndef Q3DCONFIG_MULTILIB_H
#define Q3DCONFIG_MULTILIB_H

#ifndef __WORDSIZE
#include <bits/wordsize.h>
#endif

#if __WORDSIZE == 32
#include "Qt3DCore/private/qt3dcore-config-32_p.h"
#elif __WORDSIZE == 64
#include "Qt3DCore/private/qt3dcore-config-64_p.h"
#else
#error "unexpected value for __WORDSIZE macro"
#endif

#endif
