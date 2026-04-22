#!/usr/bin/python3
# Copyright 2015 Tomas Popela <tpopela@redhat.com>
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import re

def append_sources (input_sources, output_sources):

  # Get the source files.
  source_files = re.findall(r"\"(.*?)\"", input_sources)
  output_sources += source_files


def parse_sources(input_sources, output_sources, arch_not_arm):

  # Get the type of sources in one group and sources itself in the other one.
  blocks = re.findall(r"(ffmpeg[^\s]*).*?\[(.*?)]", input_sources, re.DOTALL)
  for block in blocks:
    if (arch_not_arm):
      if not 'ffmpeg_gas_sources' in block[0]:
        append_sources (block[1], output_sources)
    else:
      append_sources (block[1], output_sources)


def parse_ffmpeg_gni_file(gni_path, arch_not_arm):

  with open(gni_path, "r") as input_file:
    content = input_file.read().replace('\n', '')

  output_sources = []
  # Get all the sections.
  sections = re.findall(r"if (.*?})", content, re.DOTALL)
  for section in sections:
    # Get all the conditions (first group) and sources (second group) for the
    # current section.
    blocks = re.findall(r"(\(.*?\))\s\{(.*?)\}", section, re.DOTALL)
    for block in blocks:
      conditions = re.findall(r"\(?\((.*?)\)", block[0])
      inserted = False
      for condition in conditions:
        if inserted:
          break
        limitations = ['ffmpeg_branding == "Chrome"', 'ffmpeg_branding == "ChromeOS"']
        if ('use_linux_config' in condition) and not any(limitation in condition for limitation in limitations):
          if (arch_not_arm):
            if ('x64' in condition) or ('x86' in condition) or ('use_linux_config' in condition):
              parse_sources (block[1], output_sources, arch_not_arm)
              inserted = True
          else:
            parse_sources (block[1], output_sources, arch_not_arm)
            inserted = True

  if len(output_sources) == 0:
    sys.stderr.write("Something went wrong, no sources parsed!\n")
    sys.exit(1)

  print(' '.join(output_sources))


if __name__ == "__main__":

  path = "%s/third_party/ffmpeg/ffmpeg_generated.gni" % sys.argv[1]
  parse_ffmpeg_gni_file (path, False if sys.argv[2] == "0" else True)
