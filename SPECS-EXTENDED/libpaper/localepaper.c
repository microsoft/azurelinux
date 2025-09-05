/*
 * localepaper: print the dimensions in mm of the current locale's
 * paper size, if possible.
 *
 * Based on a patch by Caolan McNamara:
 * http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=481213
 *
 * Copyright (C) Reuben Thomas <rrt@sc3d.org>, 2013.
 *
 * Copying and distribution of this file, with or without modification,
 * are permitted in any medium without royalty provided the copyright
 * notice and this notice are preserved.
 */

#include <config.h>

#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#if defined LC_PAPER && defined _GNU_SOURCE
#include <langinfo.h>
#endif

#include "progname.h"

int main(int argc, char *argv[])
{
  set_program_name(argv[0]);
  argc = argc; /* Avoid a compiler warning. */

#if defined LC_PAPER && defined _GNU_SOURCE
  setlocale(LC_ALL, "");

#define NL_PAPER_GET(x) \
  ((union { char *string; unsigned word; })nl_langinfo(x)).word

  printf("%d %d\n", NL_PAPER_GET(_NL_PAPER_WIDTH), NL_PAPER_GET(_NL_PAPER_HEIGHT));
  return EXIT_SUCCESS;

#else
  printf("%s: locale paper size information is not supported on this system", program_name);
  return EXIT_FAILURE;
#endif
}
