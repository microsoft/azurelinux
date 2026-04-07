/* This file is here to prevent a file conflict on multiarch systems.  A
 * conflict will occur because apr.h has arch-specific definitions.
 *
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#if defined(__i386__)
#include "apr-i386.h"
#elif defined(__ia64__)
#include "apr-ia64.h"
#elif defined(__powerpc64__)
#include "apr-ppc64.h"
#elif defined(__powerpc__)
#include "apr-ppc.h"
#elif defined(__s390x__)
#include "apr-s390x.h"
#elif defined(__s390__)
#include "apr-s390.h"
#elif defined(__x86_64__)
#include "apr-x86_64.h"
#else
#error "This apr-devel package does not work your architecture?"
#endif
