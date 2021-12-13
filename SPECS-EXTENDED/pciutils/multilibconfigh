#if defined(__x86_64__) || defined(__ia64__) || defined(__ppc64__) || defined(__powerpc64__) || defined(__s390x__) || defined(__aarch64__) || defined(__mips64)
#include "config.lib64.h"
#elif defined(__sparc__) && defined (__arch64__)
#include "config.lib64.h"
#elif defined(__i386__) || defined(__ppc__)  || defined(__powerpc__) || defined(__s390__) || defined(__alpha__) || defined(__sparc__) || defined(__sh__) || defined(__arm__) || defined(__mips)
#include "config.lib.h"
#else
#error Unknown Arch
#endif
