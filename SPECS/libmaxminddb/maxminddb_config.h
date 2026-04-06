#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "maxminddb_config-32.h"
#elif __WORDSIZE == 64
#include "maxminddb_config-64.h"
#else
#error "Unknown word size"
#endif
