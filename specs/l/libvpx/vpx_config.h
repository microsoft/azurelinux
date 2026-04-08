/* Provide a real file - not a symlink - as it would cause multiarch conflicts 
   (when multiple different arch releases are installed simultaneously. */

#if defined __x86_64__
# include "vpx_config-x86_64.h"
#elif defined __aarch64__
# include "vpx_config-aarch64.h"
#elif defined __arm__
# include "vpx_config-arm.h"
#elif defined __i386__
# include "vpx_config-x86.h"
#elif defined __powerpc64__
# include "vpx_config-ppc64.h"
#elif defined __s390__
# include "vpx_config-s390.h"
#else
# error "Unsupported arch"
#endif
