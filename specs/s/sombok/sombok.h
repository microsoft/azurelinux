#if defined(__i386__)
#include "sombok-i386.h"
#elif defined(__ia64__)
#include "sombok-ia64.h"
#elif defined(__powerpc64__)
#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#include "sombok-ppc64.h"
#else
#include "sombok-ppc64le.h"
#endif
#elif defined(__powerpc__)
#include "sombok-ppc.h"
#elif defined(__s390x__)
#include "sombok-s390x.h"
#elif defined(__s390__)
#include "sombok-s390.h"
#elif defined(__x86_64__)
#include "sombok-x86_64.h"
#elif defined(__arm__)
#include "sombok-arm.h"
#elif defined(__alpha__)
#include "sombok-alpha.h"
#elif defined(__sparc__) && defined (__arch64__)
#include "sombok-sparc64.h"
#elif defined(__sparc__)
#include "sombok-sparc.h"
#elif defined(__aarch64__)
#include "sombok-aarch64.h"
#elif defined(__mips64) && defined(__MIPSEL__)
#include "sombok-mips64el.h"
#elif defined(__mips64)
#include "sombok-mips64.h"
#elif defined(__mips) && defined(__MIPSEL__)
#include "sombok-mipsel.h"
#elif defined(__mips)
#include "sombok-mips.h"
#elif defined(__riscv) && defined(__riscv_xlen) && __riscv_xlen == 64
#include "sombok-riscv64.h"
#else
#error "This sombok-devel package does not support your architecture."
#endif

