#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "IlmBaseConfig-32.h"
#elif __WORDSIZE == 64
#include "IlmBaseConfig-64.h"
#else
#error "Unknown word size"
#endif

