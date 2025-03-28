#include <bits/wordsize.h>

#if __WORDSIZE == 32
# ifdef LIBBSD_OVERLAY
#  include "sys/cdefs-32.h"
# else
#  include "cdefs-32.h"
# endif
#elif __WORDSIZE == 64
# ifdef LIBBSD_OVERLAY
#  include "sys/cdefs-64.h"
# else
#  include "cdefs-64.h"
# endif
#else
# error "Unknown word size"
#endif
