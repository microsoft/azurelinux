#!/usr/bin/python3
#
# Copyright 2021-2026, Than Ngo <than@redhat.com>
# Copyright 2010,2015-2019 Tom Callaway <tcallawa@redhat.com>
# Copyright 2013-2016 Tomas Popela <tpopela@redhat.com>
#
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

try:
  import argparse
  optparse = False
except ImportError:
  from optparse import OptionParser
  optparse = True
import csv
import glob
import hashlib
import locale
import os
import shutil
import io
import sys
import urllib.request, urllib.parse, urllib.error

chromium_url = "http://commondatastorage.googleapis.com/chromium-browser-official/"

chromium_root_dir = "."
version_string = "stable"

name = 'Chromium Latest'
script_version = 0.9
my_description = '{0} {1}'.format(name, script_version)


def dlProgress(count, blockSize, totalSize):

  if (totalSize <= blockSize):
    percent = int(count * 100)
  else:
    percent = int(count * blockSize * 100 / totalSize)
  sys.stdout.write("\r" + "Downloading ... %d%%" % percent)
  sys.stdout.flush()


def delete_chromium_dir(ch_dir):

  full_dir = "%s/%s" % (latest_dir, ch_dir)
  print('Deleting %s ' % full_dir)
  if os.path.isdir(full_dir):
    shutil.rmtree(full_dir)
    print('[DONE]')
  else:
    print('[NOT FOUND]')


def delete_chromium_files(files):

  full_path = "%s/%s" % (latest_dir, files)
  print('Deleting ' + full_path + ' ', end=' ')
  for filename in glob.glob(full_path):
    if os.path.isfile(filename):
      os.remove(filename)
      print('[DONE]')
    else:
      print('[NOT FOUND]')

def check_omahaproxy(channel="stable"):

  version = 0
  status_url = "http://omahaproxy.appspot.com/all?os=linux&channel=" + channel

  usock = urllib.request.urlopen(status_url)
  status_dump = usock.read().decode('utf-8')
  usock.close()
  status_list = io.StringIO(status_dump)
  status_reader = list(csv.reader(status_list, delimiter=','))
  linux_channels = [s for s in status_reader if "linux" in s]
  linux_channel = [s for s in linux_channels if channel in s]
  version = linux_channel[0][2]

  if version == 0:
    print('I could not find the latest %s build. Bailing out.' % channel)
    sys.exit(1)
  else:
    print('Latest Chromium Version on %s at %s is %s' % (channel, status_url, version))
    return version


def remove_file_if_exists(filename):

  if os.path.isfile("./%s" % filename):
    try:
      os.remove(filename)
    except Exception:
      pass


def download_file_and_compare_hashes(file_to_download):

  hashes_file = '%s.hashes' % file_to_download

  if (args.clean):
    remove_file_if_exists(file_to_download)
    remove_file_if_exists(hashes_file)

  # Let's make sure we haven't already downloaded it.
  tarball_local_file = "./%s" % file_to_download
  if os.path.isfile(tarball_local_file):
    print("%s already exists!" % file_to_download)
  else:
    path = '%s%s' % (chromium_url, file_to_download)
    print("Downloading %s" % path)
    # Perhaps look at using python-progressbar at some point?
    info=urllib.request.urlretrieve(path, file_to_download, reporthook=dlProgress)[1]
    urllib.request.urlcleanup()
    print("")
    if (info["Content-Type"] != "application/x-tar"):
      print('Chromium tarballs for %s are not on servers.' % file_to_download)
      remove_file_if_exists (file_to_download)
      sys.exit(1)

  hashes_local_file = "./%s" % hashes_file
  if not os.path.isfile(hashes_local_file):
    path = '%s%s' % (chromium_url, hashes_file)
    print("Downloading %s" % path)
    # Perhaps look at using python-progressbar at some point?
    info=urllib.request.urlretrieve(path, hashes_file, reporthook=dlProgress)[1]
    urllib.request.urlcleanup()
    print("")

  if os.path.isfile(hashes_local_file):
    with open(hashes_local_file, "r") as input_file:
      md5sum = input_file.readline().split()[1]
      md5 = hashlib.md5()
      with open(tarball_local_file, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
          md5.update(block)
        if (md5sum == md5.hexdigest()):
          print("MD5 matches for %s!" % file_to_download)
        else:
          print("MD5 mismatch for %s!" % file_to_download)
          sys.exit(1)
  else:
    print("Cannot compare hashes for %s!" % file_to_download)


def download_version(version):

  download_file_and_compare_hashes ('chromium-%s-lite.tar.xz' % version)

  if (args.tests):
    download_file_and_compare_hashes ('chromium-%s-testdata.tar.xz' % version)

def nacl_versions(version):

  if sys.version_info[0] == 2 and sys.version_info[1] == 6:
    return

  myvars = {}
  chrome_dir = './chromium-%s' % version
  with open(chrome_dir + "/native_client/tools/REVISIONS") as myfile:
      for line in myfile:
          name, var = line.partition("=")[::2]
          myvars[name] = var
  print("nacl-binutils commit: %s" % myvars["NACL_BINUTILS_COMMIT"])
  print("nacl-gcc commit: %s" % myvars["NACL_GCC_COMMIT"])
  print("nacl-newlib commit: %s" % myvars["NACL_NEWLIB_COMMIT"])

  # Parse GIT_REVISIONS dict from toolchain_build.py

  sys.path.append(os.path.abspath(chrome_dir + "/native_client/toolchain_build"))
  from toolchain_build import GIT_REVISIONS
  print("nacl-arm-binutils commit: %s" % GIT_REVISIONS['binutils']['rev'])
  print("nacl-arm-gcc commit: %s" % GIT_REVISIONS['gcc']['rev'])


def download_chrome_latest_rpm(arch):

  chrome_rpm = 'google-chrome-%s_current_%s.rpm' % (version_string, arch)
  path = 'https://dl.google.com/linux/direct/%s' % chrome_rpm

  if (args.clean):
    remove_file_if_exists(chrome_rpm)

  # Let's make sure we haven't already downloaded it.
  if os.path.isfile("./%s" % chrome_rpm):
    print("%s already exists!" % chrome_rpm)
  else:
    print("Downloading %s" % path)
    # Perhaps look at using python-progressbar at some point?
    info=urllib.request.urlretrieve(path, chrome_rpm, reporthook=dlProgress)[1]
    urllib.request.urlcleanup()
    print("")
    if (info["Content-Type"] != "binary/octet-stream" and info["Content-Type"] != "application/x-redhat-package-manager"):
      print('Chrome %s rpms are not on servers.' % version_string)
      remove_file_if_exists (chrome_rpm)
      sys.exit(1)

# This is where the magic happens
if __name__ == '__main__':

  # Locale magic
  locale.setlocale(locale.LC_ALL, '')

  # Create the parser object
  if optparse:
    parser = OptionParser(description=my_description)
    parser_add_argument = parser.add_option
  else:
    parser = argparse.ArgumentParser(description=my_description)
    parser_add_argument = parser.add_argument

  parser_add_argument(
      '--ffmpegarm', action='store_true',
      help='Leave arm sources when cleaning ffmpeg')
  parser_add_argument(
      '--beta', action='store_true',
      help='Get the latest beta Chromium source')
  parser_add_argument(
      '--clean', action='store_true',
      help='Re-download all previously downloaded sources')
  parser_add_argument(
      '--cleansources', action='store_true',
      help='Get the latest Chromium release from given channel and clean various directories to from unnecessary or unwanted stuff')
  parser_add_argument(
      '--dev', action='store_true',
      help='Get the latest dev Chromium source')
  parser_add_argument(
      '--ffmpegclean', action='store_true',
      help='Get the latest Chromium release from given channel and cleans ffmpeg sources from proprietary stuff')
  parser_add_argument(
      '--ffmpegremove', action='store_true',
      help='Get the latest Chromium release from given channel and remove ffmpeg sources')
  parser_add_argument(
      '--chrome', action='store_true',
      help='Get the latest Chrome rpms for the given channel')
  parser_add_argument(
      '--prep', action='store_true',
      help='Prepare everything, but don\'t compress the result')
  parser_add_argument(
      '--stable', action='store_true',
      help='Get the latest stable Chromium source')
  parser_add_argument(
      '--tests', action='store_true',
      help='Get the additional data for running tests')
  parser_add_argument(
      '--version',
      help='Download a specific version of Chromium')
  parser_add_argument(
      '--naclvers',
      help='Display the commit versions of nacl toolchain components')

  # Parse the args
  if optparse:
    args, options = parser.parse_args()
  else:
    args = parser.parse_args()

  if args.stable:
    version_string = "stable"
  elif args.beta:
    version_string = "beta"
  elif args.dev:
    version_string = "dev"
  elif (not (args.stable or args.beta or args.dev)):
    if (not args.version):
      print('No version specified, downloading STABLE')
    args.stable = True

  chromium_version = args.version if args.version else check_omahaproxy(version_string)

  if args.dev:
    version_string = "unstable"

  if args.chrome:
    if args.version:
      print('You cannot specify a Chrome RPM version!')
      sys.exit(1)
    latest = 'google-chrome-%s_current_i386' % version_string
    download_chrome_latest_rpm("i386")
    latest = 'google-chrome-%s_current_x86_64' % version_string
    download_chrome_latest_rpm("x86_64")
    if (not (args.ffmpegclean or args.tests)):
      sys.exit(0)

  latest = 'chromium-%s-lite.tar.xz' % chromium_version

  download_version(chromium_version)

  # Lets make sure we haven't unpacked it already
  latest_dir = "%s/chromium-%s" % (chromium_root_dir, chromium_version)
  if (args.clean and os.path.isdir(latest_dir)):
    shutil.rmtree(latest_dir)

  if os.path.isdir(latest_dir):
    print("%s already exists, perhaps %s has already been unpacked?" % (latest_dir, latest))
  else:
    print("Unpacking %s into %s, please wait." % (latest, latest_dir))
    if (os.system("tar -xJf %s" % latest) != 0):
      print("%s is possibly corrupted, exiting." % (latest))
      sys.exit(1)

  if (args.naclvers):
    nacl_versions(chromium_version)

  if (args.cleansources):
    junk_dirs = ['build/linux/debian_bullseye_amd64-sysroot',
                 'build/linux/debian_bullseye_i386-sysroot',
                 'third_party/node/linux/node-linux-x64',
                 'third_party/rust-toolchain',
                 'third_party/rust-src',
                 'third_party/devtools-frontend/src/third_party/esbuild',
                 'third_party/enterprise_companion/chromium_linux64',
                 'third_party/enterprise_companion/chromium_mac_amd64',
                 'third_party/enterprise_companion/chromium_mac_arm64',
                 'third_party/enterprise_companion/chromium_win_x86',
                 'third_party/enterprise_companion/chromium_win_x86_64']
    junk_files = ['third_party/node/linux/node-linux-x64.tar.gz',
                  'buildtools/third_party/eu-strip/bin/eu-strip',
                  'buildtools/linux64/gn']

    # First, the dirs:
    for directory in junk_dirs:
      delete_chromium_dir(directory)
    # Remove junk files
    for file in junk_files:
      delete_chromium_files(file)

  # There has got to be a better, more portable way to do this.
  os.system("find %s -depth -name reference_build -type d -exec rm -rf {} \\;" % latest_dir)

  # I could not find good bindings for xz/lzma support, so we system call here too.
  chromium_clean_xz_file = "chromium-" + chromium_version + "-clean.tar.xz"

  remove_file_if_exists(chromium_clean_xz_file)

  if (args.ffmpegclean):
    print("Cleaning ffmpeg from proprietary things...")
    os.system("./clean_ffmpeg.sh %s %d" % (latest_dir, 0 if args.ffmpegarm else 1))
    print("Cleaning openh264 from proprietary things...")
    os.system("find %s/third_party/openh264/* -type d | xargs rm -rf" % latest_dir)
    print("Done!")

  if (args.ffmpegremove):
    print("Removing ffmpeg source...")
    os.system("find %s/third_party/ffmpeg/* -type d | xargs rm -rf" % latest_dir)
    print("Cleaning openh264 from proprietary things...")
    os.system("find %s/third_party/openh264/* -type d | xargs rm -rf" % latest_dir)
    print("Done!")

  if (not args.prep):
    print("Compressing cleaned tree, please wait...")
    os.chdir(chromium_root_dir)
    os.system("tar --exclude=\\.svn -cf - chromium-%s | xz -6 -T0 -f > %s" % (chromium_version, chromium_clean_xz_file))

  print("Finished!")
