/* This file is here to prevent a file conflict on multiarch systems. */
#ifdef ffi_wrapper_h
#error "Do not define ffi_wrapper_h!"
#endif
#define ffi_wrapper_h

#if defined(__i386__)
#include "ffi-i386.h"
#elif defined(__powerpc64__)
#include "ffi-ppc64.h"
#elif defined(__powerpc__)
#include "ffi-ppc.h"
#elif defined(__s390x__)
#include "ffi-s390x.h"
#elif defined(__s390__)
#include "ffi-s390.h"
#elif defined(__x86_64__)
#include "ffi-x86_64.h"
#else
#error "The libffi-devel package is not usable with the architecture."
#endif

#undef ffi_wrapper_h
