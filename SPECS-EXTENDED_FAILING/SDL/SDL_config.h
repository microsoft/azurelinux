/*
    SDL - Simple DirectMedia Layer
    Copyright (C) 1997-2006 Sam Lantinga

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

    Sam Lantinga
    slouken@libsdl.org
*/

/*
 * This SDL_config.h is a wrapper include file for the original SDL_config.h, 
 * which has been renamed to SDL_config-<arch>.h. There are conflicts for the 
 * original SDL_config.h on multilib systems, which result from arch-specific
 * configuration options. Please do not use the arch-specific file directly.
 *
 * Copyright (C) 2006 Red Hat, Inc.
 * Thomas Woerner <twoerner@redhat.com>
 */

#ifdef SDL_config_wrapper_h
#error "SDL_config_wrapper_h should not be defined!"
#endif
#define SDL_config_wrapper_h

#if defined(__i386__)
#include "SDL_config-i386.h"
#elif defined(__ia64__)
#include "SDL_config-ia64.h"
#elif defined(__powerpc64__)
#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#include "SDL_config-ppc64.h"
#else
#include "SDL_config-ppc64le.h"
#endif
#elif defined(__powerpc__)
#include "SDL_config-ppc.h"
#elif defined(__s390x__)
#include "SDL_config-s390x.h"
#elif defined(__s390__)
#include "SDL_config-s390.h"
#elif defined(__x86_64__)
#include "SDL_config-x86_64.h"
#elif defined(__arm__)
#include "SDL_config-arm.h"
#elif defined(__alpha__)
#include "SDL_config-alpha.h"
#elif defined(__sparc__) && defined (__arch64__)
#include "SDL_config-sparc64.h"
#elif defined(__sparc__)
#include "SDL_config-sparc.h"
#elif defined(__aarch64__)
#include "SDL_config-aarch64.h"
#elif defined(__mips64) && defined(__MIPSEL__)
#include "SDL_config-mips64el.h"
#elif defined(__mips64)
#include "SDL_config-mips64.h"
#elif defined(__mips) && defined(__MIPSEL__)
#include "SDL_config-mipsel.h"
#elif defined(__mips)
#include "SDL_config-mips.h"
#elif defined(__riscv) && defined(__riscv_xlen) && __riscv_xlen == 64
#include "SDL_config-riscv64.h"
#else
#error "The SDL-devel package is not usable with the architecture."
#endif

#undef SDL_config_wrapper_h
