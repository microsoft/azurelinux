/*
 * This luaconf.h is a wrapper include file for the original luaconf.h, 
 * which has been renamed to luaconf-<arch>.h. There are conflicts for the 
 * original luaconf.h on multilib systems, which result from arch-specific
 * configuration options. Please do not use the arch-specific file directly.
 *
 * Copyright (C) 2015 Tom Callaway <spot@fedoraproject.org>
 */

/**
 *  \file luaconf.h
 */

#ifdef luaconf_wrapper_h
#error "luaconf_wrapper_h should not be defined!"
#endif
#define luaconf_wrapper_h

#if defined(__i386__)
#include "luaconf-i386.h"
#elif defined(__ia64__)
#include "luaconf-ia64.h"
#elif defined(__powerpc64__)
# if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#include "luaconf-ppc64.h"
# else
#include "luaconf-ppc64le.h"
# endif
#elif defined(__powerpc__)
#include "luaconf-ppc.h"
#elif defined(__s390x__)
#include "luaconf-s390x.h"
#elif defined(__s390__)
#include "luaconf-s390.h"
#elif defined(__x86_64__)
#include "luaconf-x86_64.h"
#elif defined(__arm__)
#include "luaconf-arm.h"
#elif defined(__alpha__)
#include "luaconf-alpha.h"
#elif defined(__sparc__) && defined (__arch64__)
#include "luaconf-sparc64.h"
#elif defined(__sparc__)
#include "luaconf-sparc.h"
#elif defined(__aarch64__)
#include "luaconf-aarch64.h"
#elif defined(__mips64) && defined(__MIPSEL__)
#include "luaconf-mips64el.h"
#elif defined(__mips64)
#include "luaconf-mips64.h"
#elif defined(__mips) && defined(__MIPSEL__)
#include "luaconf-mipsel.h"
#elif defined(__mips)
#include "luaconf-mips.h"
#elif defined(__riscv)
#include "luaconf-riscv64.h"
#else
#error "The lua-devel package is not usable with the architecture."
#endif

#undef luaconf_wrapper_h
