/*
 *  GRUB  --  GRand Unified Bootloader
 *  Copyright (C) 2016 Free Software Foundation, Inc.
 *
 *  GRUB is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  GRUB is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with GRUB.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <grub/test.h>
#include <grub/dl.h>

GRUB_MOD_LICENSE ("GPLv3+");

static void
strtoull_testcase (const char *input, int base, unsigned long long expected,
		   int num_digits, grub_err_t error)
{
  char *output;
  unsigned long long value;
  grub_errno = 0;
  value = grub_strtoull(input, &output, base);
  grub_test_assert (grub_errno == error,
		    "unexpected error. Expected %d, got %d. Input \"%s\"",
		    error, grub_errno, input);
  if (grub_errno)
    {
      grub_errno = 0;
      return;
    }
  grub_test_assert (input + num_digits == output,
		    "unexpected number of digits. Expected %d, got %d, input \"%s\"",
		    num_digits, (int) (output - input), input);
  grub_test_assert (value == expected,
		    "unexpected return value. Expected %llu, got %llu, input \"\%s\"",
		    expected, value, input);
}

static void
strtoull_test (void)
{
  strtoull_testcase ("9", 0, 9, 1, GRUB_ERR_NONE);
  strtoull_testcase ("0xaa", 0, 0xaa, 4, GRUB_ERR_NONE);
  strtoull_testcase ("0xff", 0, 0xff, 4, GRUB_ERR_NONE);
  strtoull_testcase ("0", 10, 0, 1, GRUB_ERR_NONE);
  strtoull_testcase ("8", 8, 0, 0, GRUB_ERR_BAD_NUMBER);
  strtoull_testcase ("38", 8, 3, 1, GRUB_ERR_NONE);
  strtoull_testcase ("7", 8, 7, 1, GRUB_ERR_NONE);
  strtoull_testcase ("1]", 16, 1, 1, GRUB_ERR_NONE);
  strtoull_testcase ("18446744073709551616", 10, 0, 0, GRUB_ERR_OUT_OF_RANGE);
}


GRUB_FUNCTIONAL_TEST (strtoull_test, strtoull_test);
