/*
 * This autoconf.h is a wrapper include file for the original libecap/common/autoconf.h,
 * which has been renamed to autoconf-<arch>.h. There are conflicts for the
 * original autoconf.h on multilib systems, which result from arch-specific
 * configuration options. Please do not use the arch-specific file directly.
 */

/*
 * This wrapped is addpated from SDL's one:
 * http://pkgs.fedoraproject.org/cgit/SDL.git/tree/SDL_config.h
 */

#ifdef libecap_autoconf_wrapper_h
#error "libecap_autoconf_wrapper_h should not be defined!"
#endif
#define libecap_autoconf_wrapper_h

#if defined(__i386__)
#include "libecap/common/autoconf-i386.h"
#elif defined(__ia64__)
#include "libecap/common/autoconf-ia64.h"
#elif defined(__powerpc64__)
#include <endian.h>
#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#include "libecap/common/autoconf-ppc64.h"
#else
#include "libecap/common/autoconf-ppc64le.h"
#endif
#elif defined(__powerpc__)
#include "libecap/common/autoconf-ppc.h"
#elif defined(__s390x__)
#include "libecap/common/autoconf-s390x.h"
#elif defined(__s390__)
#include "libecap/common/autoconf-s390.h"
#elif defined(__x86_64__)
#include "libecap/common/autoconf-x86_64.h"
#elif defined(__arm__)
#include "libecap/common/autoconf-arm.h"
#elif defined(__alpha__)
#include "libecap/common/autoconf-alpha.h"
#elif defined(__sparc__) && defined (__arch64__)
#include "libecap/common/autoconf-sparc64.h"
#elif defined(__sparc__)
#include "libecap/common/autoconf-sparc.h"
#elif defined(__aarch64__)
#include "libecap/common/autoconf-aarch64.h"
#else
#error "The libecap-devel package is not usable with the architecture."
#endif

#undef libecap_autoconf_wrapper_h 
