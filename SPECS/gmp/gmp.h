/* Definitions for GNU multiple precision functions.   -*- mode: c -*-

Copyright 1991, 1993, 1994, 1995, 1996, 1997, 1999, 2000, 2001, 2002, 2003,
2004, 2005, 2006, 2007, 2008, 2009 Free Software Foundation, Inc.

This file is part of the GNU MP Library.

The GNU MP Library is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 3 of the License, or (at your
option) any later version.

The GNU MP Library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
License for more details.

You should have received a copy of the GNU Lesser General Public License
along with the GNU MP Library.  If not, see http://www.gnu.org/licenses/.  */

/*
 * This gmp.h is a wrapper include file for the original gmp.h, which has been
 * renamed to gmp-<arch>.h. There are conflicts for the original gmp.h on
 * multilib systems, which result from arch-specific configuration options.
 * Please do not use the arch-specific file directly.
 *
 * Copyright (C) 2006 Red Hat, Inc.
 * Thomas Woerner <twoerner@redhat.com>
 */

#ifdef gmp_wrapper_h
#error "gmp_wrapper_h should not be defined!"
#endif
#define gmp_wrapper_h

#if defined(__arm__)
#include "gmp-arm.h"
#elif defined(__i386__)
#include "gmp-i386.h"
#elif defined(__ia64__)
#include "gmp-ia64.h"
#elif defined(__powerpc64__)
# if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#include "gmp-ppc64.h"
# else
#include "gmp-ppc64le.h"
# endif
#elif defined(__powerpc__)
# if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#include "gmp-ppc.h"
# else
#include "gmp-ppcle.h"
# endif
#elif defined(__s390x__)
#include "gmp-s390x.h"
#elif defined(__s390__)
#include "gmp-s390.h"
#elif defined(__x86_64__)
#include "gmp-x86_64.h"
#elif defined(__alpha__)
#include "gmp-alpha.h"
#elif defined(__sh__)
#include "gmp-sh.h"
#elif defined(__sparc__) && defined (__arch64__)
#include "gmp-sparc64.h"
#elif defined(__sparc__)
#include "gmp-sparc.h"
#elif defined(__aarch64__)
#include "gmp-aarch64.h"
#elif defined(__mips64) && defined(__MIPSEL__)
#include "gmp-mips64el.h"
#elif defined(__mips64)
#include "gmp-mips64.h"
#elif defined(__mips) && defined(__MIPSEL__)
#include "gmp-mipsel.h"
#elif defined(__mips)
#include "gmp-mips.h"
#elif defined(__riscv)
#if __riscv_xlen == 64
#include "gmp-riscv64.h"
#else
#error "No support for riscv32"
#endif
#else
#error "The gmp-devel package is not usable with the architecture."
#endif

#undef gmp_wrapper_h
