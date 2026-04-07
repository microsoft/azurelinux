/*
 * Copyright (C) 2023 Red Hat, Inc.
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
 *
 * This code is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License version 2 only, as
 * published by the Free Software Foundation.  Red Hat designates this
 * particular file as subject to the "Classpath" exception as provided
 * by Red Hat in the LICENSE file that accompanied this code.
 *
 * This code is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * version 2 for more details (a copy is included in the LICENSE file that
 * accompanied this code).
 *
 * You should have received a copy of the GNU General Public License version
 * 2 along with this work; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 */

#include <errno.h>
#include <libgen.h>
#include <linux/limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <unistd.h>

/* Per task speculation control */
#ifndef PR_GET_SPECULATION_CTRL
# define PR_GET_SPECULATION_CTRL    52
#endif
#ifndef PR_SET_SPECULATION_CTRL
# define PR_SET_SPECULATION_CTRL    53
#endif
/* Speculation control variants */
#ifndef PR_SPEC_STORE_BYPASS
# define PR_SPEC_STORE_BYPASS          0
#endif
/* Return and control values for PR_SET/GET_SPECULATION_CTRL */

#ifndef PR_SPEC_NOT_AFFECTED
# define PR_SPEC_NOT_AFFECTED          0
#endif
#ifndef PR_SPEC_PRCTL
# define PR_SPEC_PRCTL                 (1UL << 0)
#endif
#ifndef PR_SPEC_ENABLE
# define PR_SPEC_ENABLE                (1UL << 1)
#endif
#ifndef PR_SPEC_DISABLE
# define PR_SPEC_DISABLE               (1UL << 2)
#endif
#ifndef PR_SPEC_FORCE_DISABLE
# define PR_SPEC_FORCE_DISABLE         (1UL << 3)
#endif
#ifndef PR_SPEC_DISABLE_NOEXEC
# define PR_SPEC_DISABLE_NOEXEC        (1UL << 4)
#endif

static void set_speculation() {
#if defined(__linux__) && defined(__x86_64__)
  // PR_SPEC_DISABLE_NOEXEC doesn't survive execve, so we can't use it
  //  if ( prctl(PR_SET_SPECULATION_CTRL,
  //           PR_SPEC_STORE_BYPASS,
  //           PR_SPEC_DISABLE_NOEXEC, 0, 0) == 0 ) {
  //  return;
  // }
  prctl(PR_SET_SPECULATION_CTRL, PR_SPEC_STORE_BYPASS, PR_SPEC_DISABLE, 0, 0);
#else
#warning alt-java requested but SSB mitigation not available on this platform.
#endif
}

int main(int argc, char **argv) {
  set_speculation();

  char our_name[PATH_MAX], java_name[PATH_MAX];
  ssize_t len = readlink("/proc/self/exe", our_name, PATH_MAX - 1);
  if (len < 0) {
    perror("I can't find myself");
    exit(2);
  }

  our_name[len] = '\0'; // readlink(2) doesn't append a null byte
  char *path = dirname(our_name);
  strncpy(java_name, path, PATH_MAX - 1);

  size_t remaining_bytes = PATH_MAX - strlen(path) - 1;
  strncat(java_name, "/java", remaining_bytes);

  execv(java_name, argv);
  fprintf(stderr, "%s failed to launch: %s\n", java_name, strerror(errno));

  exit(1);
}

