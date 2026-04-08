/* This file is here to prevent a file conflict on multiarch systems. */
#ifdef ffitarget_wrapper_h
#error "Do not define ffitarget_wrapper_h!"
#endif
#define ffitarget_wrapper_h

#if defined(__i386__)
#include "ffitarget-i386.h"
#elif defined(__powerpc64__)
#include "ffitarget-ppc64.h"
#elif defined(__powerpc__)
#include "ffitarget-ppc.h"
#elif defined(__s390x__)
#include "ffitarget-s390x.h"
#elif defined(__s390__)
#include "ffitarget-s390.h"
#elif defined(__x86_64__)
#include "ffitarget-x86_64.h"
#else
#error "The libffi-devel package is not usable with the architecture."
#endif

#undef ffitarget_wrapper_h
