/* This file is here to prevent a file conflict on multiarch systems.  A
 * conflict will frequently occur because arch-specific build-time
 * configuration options are stored (and used, so they can't just be stripped
 * out) in configuration.h.  The original configuration.h has been renamed.
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#ifdef openssl_conf_multilib_redirection_h
#error "Do not define openssl_conf_multilib_redirection_h!"
#endif
#define openssl_conf_multilib_redirection_h

#if defined(__i386__)
#include "configuration-i386.h"
#elif defined(__ia64__)
#include "configuration-ia64.h"
#elif defined(__mips64) && defined(__MIPSEL__)
#include "configuration-mips64el.h"
#elif defined(__mips64)
#include "configuration-mips64.h"
#elif defined(__mips) && defined(__MIPSEL__)
#include "configuration-mipsel.h"
#elif defined(__mips)
#include "configuration-mips.h"
#elif defined(__powerpc64__)
#include <endian.h>
#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#include "configuration-ppc64.h"
#else
#include "configuration-ppc64le.h"
#endif
#elif defined(__powerpc__)
#include "configuration-ppc.h"
#elif defined(__s390x__)
#include "configuration-s390x.h"
#elif defined(__s390__)
#include "configuration-s390.h"
#elif defined(__sparc__) && defined(__arch64__)
#include "configuration-sparc64.h"
#elif defined(__sparc__)
#include "configuration-sparc.h"
#elif defined(__x86_64__)
#include "configuration-x86_64.h"
#else
#error "The openssl-devel package does not work your architecture?"
#endif

#undef openssl_conf_multilib_redirection_h
