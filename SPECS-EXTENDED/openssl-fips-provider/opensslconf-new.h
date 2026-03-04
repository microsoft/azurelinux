/* This file is here to prevent a file conflict on multiarch systems.  A
 * conflict will frequently occur because arch-specific build-time
 * configuration options are stored (and used, so they can't just be stripped
 * out) in opensslconf.h.  The original opensslconf.h has been renamed.
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#ifdef openssl_opensslconf_multilib_redirection_h
#error "Do not define openssl_opensslconf_multilib_redirection_h!"
#endif
#define openssl_opensslconf_multilib_redirection_h

#if defined(__i386__)
#include "opensslconf-i386.h"
#elif defined(__ia64__)
#include "opensslconf-ia64.h"
#elif defined(__mips64) && defined(__MIPSEL__)
#include "opensslconf-mips64el.h"
#elif defined(__mips64)
#include "opensslconf-mips64.h"
#elif defined(__mips) && defined(__MIPSEL__)
#include "opensslconf-mipsel.h"
#elif defined(__mips)
#include "opensslconf-mips.h"
#elif defined(__powerpc64__)
#include <endian.h>
#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#include "opensslconf-ppc64.h"
#else
#include "opensslconf-ppc64le.h"
#endif
#elif defined(__powerpc__)
#include "opensslconf-ppc.h"
#elif defined(__s390x__)
#include "opensslconf-s390x.h"
#elif defined(__s390__)
#include "opensslconf-s390.h"
#elif defined(__sparc__) && defined(__arch64__)
#include "opensslconf-sparc64.h"
#elif defined(__sparc__)
#include "opensslconf-sparc.h"
#elif defined(__x86_64__)
#include "opensslconf-x86_64.h"
#else
#error "This openssl-devel package does not work your architecture?"
#endif

#undef openssl_opensslconf_multilib_redirection_h
