/*
  Simple DirectMedia Layer
  Copyright (C) 1997-2020 Sam Lantinga <slouken@libsdl.org>

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.
*/

/*
 * This SDL_revision.h is a wrapper include file for the original SDL_revision.h,
 * which has been renamed to SDL_revision-<arch>.h. There are conflicts for the
 * original SDL_revision.h on multilib systems, which result from REVISION
 * inconsistency between architecture builds, though, I'm not sure why.
 * Computers are weird.
 *
 * Copyright (C) 2021 Tom Callaway <spotrh@gmail.com>
 */

/**
 *  \file SDL_revision.h
 */

#ifdef SDL_revision_wrapper_h
#error "SDL_revision_wrapper_h should not be defined!"
#endif
#define SDL_revision_wrapper_h

#if defined(__i386__)
#include "SDL_revision-i386.h"
#elif defined(__ia64__)
#include "SDL_revision-ia64.h"
#elif defined(__powerpc64__)
# if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#include "SDL_revision-ppc64.h"
# else
#include "SDL_revision-ppc64le.h"
# endif
#elif defined(__powerpc__)
#include "SDL_revision-ppc.h"
#elif defined(__s390x__)
#include "SDL_revision-s390x.h"
#elif defined(__s390__)
#include "SDL_revision-s390.h"
#elif defined(__x86_64__)
#include "SDL_revision-x86_64.h"
#elif defined(__arm__)
#include "SDL_revision-arm.h"
#elif defined(__alpha__)
#include "SDL_revision-alpha.h"
#elif defined(__sparc__) && defined (__arch64__)
#include "SDL_revision-sparc64.h"
#elif defined(__sparc__)
#include "SDL_revision-sparc.h"
#elif defined(__aarch64__)
#include "SDL_revision-aarch64.h"
#elif defined(__mips64) && defined(__MIPSEL__)
#include "SDL_revision-mips64el.h"
#elif defined(__mips64)
#include "SDL_revision-mips64.h"
#elif defined(__mips) && defined(__MIPSEL__)
#include "SDL_revision-mipsel.h"
#elif defined(__mips)
#include "SDL_revision-mips.h"
#elif defined(__riscv) && defined(__riscv_xlen) && __riscv_xlen == 64
#include "SDL_revision-riscv64.h"
#else
#error "The SDL2-devel package is not usable with the architecture."
#endif

#undef SDL_revision_wrapper_h
