#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "forbuild-32.h"
#elif __WORDSIZE == 64
#include "forbuild-64.h"
#else
#error "Unknown word size"
#endif
