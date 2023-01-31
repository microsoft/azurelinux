This file contains instructions to build and install the TSS libraries.

# Dependencies
To build and install the tpm2-tss software the following software packages
are required. In many cases dependencies are platform specific and so the
following sections describe them for the supported platforms.

## GNU/Linux:
* GNU Autoconf
* GNU Autoconf Archive, version >= 2017.03.21
* GNU Automake
* GNU Libtool
* C compiler
* C library development libraries and header files
* pkg-config
* doxygen
* OpenSSL development libraries and header files, version >= 1.1.0
* libcurl development libraries
* Access Control List utility (acl)
* JSON C Development library

The following are dependencies only required when building test suites.
* Integration test suite (see ./configure option --enable-integration):
    - uthash development libraries and header files
    - ps executable (usually in the procps package)
    - ss executable (usually in the iproute2 package)
    - tpm_server executable (from https://sourceforge.net/projects/ibmswtpm2/)
* Unit test suite (see ./configure option --enable-unit):
    - cmocka unit test framework, version >= 1.0
* Code coverage analysis:
    - lcov

Most users will not need to install these dependencies.

### Ubuntu
```
$ sudo apt -y update
$ sudo apt -y install \
  autoconf-archive \
  libcmocka0 \
  libcmocka-dev \
  procps \
  iproute2 \
  build-essential \
  git \
  pkg-config \
  gcc \
  libtool \
  automake \
  libssl-dev \
  uthash-dev \
  autoconf \
  doxygen \
  libjson-c-dev \
  libini-config-dev \
  libcurl4-openssl-dev \
  libuuid-dev \
  libltdl-dev
```
Note: In some Ubuntu versions, the lcov and autoconf-archive packages are incompatible with each other. It is recommended to download autoconf-archive directly from upstream and copy `ax_code_coverage.m4` and `ax_prog_doxygen.m4` to the `m4/` subdirectory of your tpm2-tss directory.

### Fedora

There is a package already, so the package build dependencies information can be
used to make sure that the needed packages to compile from source are installed:

```
$ sudo dnf builddep tpm2-tss
```

## Windows
Windows dlls built using the Clang/LLVM "Platform Toolset" are currently
prototypes. We have only tested using Visual Studio 2017 with the Universal
C Runtime (UCRT) version 10.0.16299.0. Building the type marshaling library
(tss2-mu.dll) and the system API (tss2-sapi.dll) should be as simple as
loading the tpm2-tss solution (tpm2-tss.sln) with a compatible and properly
configured version of Visual Studio 2017 and pressing the 'build' button.

### References
Visual Studio 2017 with "Clang for Windows": https://blogs.msdn.microsoft.com/vcblog/2017/03/07/use-any-c-compiler-with-visual-studio/
Universal CRT overview & setup instructions: https://docs.microsoft.com/en-us/cpp/porting/upgrade-your-code-to-the-universal-crt

# Building From Source
## Bootstrapping the Build
To configure the tpm2-tss source code first run the bootstrap script, which
generates list of source files, and creates the configure script:
```
$ ./bootstrap
```

Any options specified to the bootstrap command are passed to `autoreconf(1)`.

## Configuring the Build
Then run the configure script, which generates the makefiles:
```
$ ./configure
```

### Custom `./configure` Options
In many cases you'll need to provide the `./configure` script with additional
information about your environment. Typically you'll either be telling the
script about some location to install a component, or you'll be instructing
the script to enable some additional feature or function. We'll cover each
in turn.

Invoking the configure script with the `--help` option will display
all supported options.

The default values for GNU installation directories are documented here:
https://www.gnu.org/prep/standards/html_node/Directory-Variables.html

### udev Rules
The typical operation for the `tpm2-abrmd` is for it to communicate directly
with the Linux TPM driver using `libtcti-device` from the TPM2.0-TSS project.
This requires that the user account that's running the `tpm2-abrmd` have both
read and write access to the TPM device node `/dev/tpm[0-9]`. But users could
also access the TPM directly so the udev rule is installed by `tpm2-tss`.

#### `--with-udevrulesdir`
This requires that `udev` be instructed to set the owner and group for this
device node when its created. We provide such a udev rule that is installed to
`${libdir}/udev/rules.d`. If your distro stores these rules elsewhere you will
need to tell the build about this location.

Using Debian as an example we can instruct the build to install the udev
rules in the right location with the following configure option:
```
--with-udevrulesdir=/etc/udev/rules.d
```

#### `--with-udevrulesprefix`
It is common for Linux distros to prefix udev rules files with a numeric
string (e.g. "70-"). This allows for the rules to be applied in a predictable
order. This option allows for the name of the installed udev rules file to
have a string prepended to the file name when it is installed.

## Compiling the Libraries
Then compile the code using make:
```
$ make -j$(nproc)
```

## Installing the Libraries
Once you've built the tpm2-tss software it can be installed with:
```
$ sudo make install
```

This will install the libraries to a location determined at configure time.
See the output of ./configure --help for the available options. Typically you
won't need to do much more than provide an alternative --prefix option at
configure time, and maybe DESTDIR at install time if you're packaging for a
distro.

# Post-install

## udev
Once you have this udev rule installed in the right place for your distro
you'll need to instruct udev to reload its rules and apply the new rule.
Typically this can be accomplished with the following command:
```
$ sudo udevadm control --reload-rules && sudo udevadm trigger
```

If this doesn't work on your distro please consult your distro's
documentation for UDEVADM(8).

## ldconfig

It may be necessary to run ldconfig (as root) to update the run-time
bindings before executing a program that links against libsapi or a TCTI
library:
```
$ sudo ldconfig
```

## Building In A Container

If you are having trouble installing the dependencies on your machine you can
build in a container.

```
$ docker build -t tpm2 .
$ docker run --name temp tpm2 /bin/true
$ docker cp temp:/tmp/tpm2-tss tpm2-tss
$ docker rm temp
```

tpm2-tss is now in your working directory and contains all the built files.

To rebuild using your local changes mount your tpm2-tss directory as a volume.

```console
$ docker run --rm -ti -v $PWD:/tmp/tpm2-tss tpm2-tss \
  sh -c 'make -j$(nproc) check'
```

## Doxygen Documentation

To build Doxygen documentation files, first install package Doxygen.
Then generate the documentation with:

```
$ ./configure --enable-doxygen-doc
$ make doxygen-doc
```

The generated documentation will appear here:
* doxygen-doc/html HTML format (start with file doxygen-doc/html/index.html)
* doxygen-doc/rtf/refman.rtf RTF format
