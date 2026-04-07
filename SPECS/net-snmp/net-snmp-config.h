/* This file is here to prevent a file conflict on multiarch systems.  A
 * conflict will frequently occur because arch-specific build-time
 * configuration options are stored (and used, so they can't just be stripped
 * out) in net-snmp-config.h.  The original net-snmp-config.h has been renamed.
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#ifdef net_snmp_config_multilib_redirection_h
#error "Do not define net_snmp_config_multilib_redirection_h!"
#endif
#define net_snmp_config_multilib_redirection_h

#if defined(__i386__)
#include "net-snmp-config-i386.h"
#elif defined(__ia64__)
#include "net-snmp-config-ia64.h"
#elif defined(__powerpc64__)
#include "net-snmp-config-ppc64.h"
#elif defined(__powerpc__)
#include "net-snmp-config-ppc.h"
#elif defined(__s390x__)
#include "net-snmp-config-s390x.h"
#elif defined(__s390__)
#include "net-snmp-config-s390.h"
#elif defined(__x86_64__)
#include "net-snmp-config-x86_64.h"
#elif defined(__alpha__)
#include "net-snmp-config-alpha.h"
#elif defined(__sparc__) && defined (__arch64__)
#include "net-snmp-config-sparc64.h"
#elif defined(__sparc__)
#include "net-snmp-config-sparc.h"
#elif defined(__aarch64__)
#include "net-snmp-config-aarch64.h"
#else
#error "net-snmp-devel package does not work on your architecture"
#endif

#undef net_snmp_config_multilib_redirection_h
