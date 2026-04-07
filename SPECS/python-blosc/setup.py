# -*- coding: utf-8 -*-
########################################################################
#
#       License: BSD 3-clause
#       Created: September 22, 2010
#       Author:  Francesc Alted - faltet@gmail.com
#
########################################################################

# flake8: noqa

from __future__ import print_function

import os
import platform
import re
import sys
import io

from setuptools import Extension
from setuptools import setup
from glob import glob
from distutils.version import LooseVersion
from distutils.command.build_ext import build_ext
from distutils.errors import CompileError
from textwrap import dedent


class BloscExtension(Extension):
    """Allows extension to carry architecture-capable flag options.

    Attributes:
        avx2_def (Dict[str]: List[str]):
            AVX2 support dictionary mapping Extension properties to a
            list of values. If compiler is AVX2 capable, then these will
            be appended onto the end of the Extension properties.
    """

    def __init__(self, *args, **kwargs):
        self.avx2_defs = kwargs.pop("avx2_defs", {})
        Extension.__init__(self, *args, **kwargs)


class build_ext_posix_avx2(build_ext):
    """build_ext customized to test for AVX2 support in posix compiler.

    This is because until distutils has actually started the build
    process, we can't be certain what compiler is being used.

    If compiler supports, then the avx2_defs dictionary on any given
    Extension will be used to extend the other Extension attributes.
    """

    def _test_compiler_flags(self, name, flags):
        # type: (List[str]) -> Bool
        """Test that a sample program can compile with given flags.

        Attr:
            flags (List[str]): the flags to test
            name (str): An identifier-like name to cache the results as

        Returns:
            (bool): Whether the compiler accepted the flags(s)
        """
        # Look to see if we have a written file to cache the result
        success_file = os.path.join(self.build_temp, "_{}_present".format(name))
        fail_file = os.path.join(self.build_temp, "_{}_failed".format(name))
        if os.path.isfile(success_file):
            return True
        elif os.path.isfile(fail_file):
            return False
        # No cache file, try to run the compile
        try:
            # Write an empty test file
            test_file = os.path.join(self.build_temp, "test_{}_empty.c".format(name))
            if not os.path.isfile(test_file):
                open(test_file, "w").close()
            objects = self.compiler.compile(
                [test_file], output_dir=self.build_temp, extra_postargs=flags
            )
            # Write a success marker so we don't need to compile again
            open(success_file, 'w').close()
            return True
        except CompileError:
            # Write a failure marker so we don't need to compile again
            open(fail_file, 'w').close()
            return False
        finally:
            pass

    def build_extensions(self):
        # Verify that the compiler supports requested extra flags
        if self._test_compiler_flags("avx2", ["-mavx2"]):
            # Apply the AVX2 properties to each extension
            for extension in self.extensions:
                if hasattr(extension, "avx2_defs"):
                    # Extend an existing attribute with the stored values
                    for attr, defs in extension.avx2_defs.items():
                        getattr(extension, attr).extend(defs)
        else:
            print("AVX2 Unsupported by compiler")

        # Call up to the superclass to do the actual build
        build_ext.build_extensions(self)


if __name__ == '__main__':

    with io.open('README.rst', encoding='utf-8') as f:
        long_description = f.read()

    try:
        import cpuinfo
        cpu_info = cpuinfo.get_cpu_info()
    except Exception:
        # newer cpuinfo versions fail to import on unsupported architectures
        cpu_info = None

    ########### Check versions ##########
    def exit_with_error(message):
        print('ERROR: %s' % message)
        sys.exit(1)

    # Check for Python
    if sys.version_info[0] == 2:
        if sys.version_info[1] < 7:
            exit_with_error("You need Python 2.7 or greater to install blosc!")
    elif sys.version_info[0] == 3:
        if sys.version_info[1] < 4:
            exit_with_error("You need Python 3.4 or greater to install blosc!")
    else:
        exit_with_error("You need Python 2.7/3.4 or greater to install blosc!")

    tests_require = ['numpy', 'psutil']

    ########### End of checks ##########

    # Read the long_description from README.rst
    with open('README.rst') as f:
        long_description = f.read()

    # Blosc version
    VERSION = open('VERSION').read().strip()
    # Create the version.py file
    open('blosc/version.py', 'w').write('__version__ = "%s"\n' % VERSION)

    # Global variables
    CFLAGS = os.environ.get('CFLAGS', '').split()
    LFLAGS = os.environ.get('LFLAGS', '').split()
    # Allow setting the Blosc dir if installed in the system
    BLOSC_DIR = os.environ.get('BLOSC_DIR', '')

    # Check for USE_CODEC environment variables
    try:
        INCLUDE_LZ4 = os.environ['INCLUDE_LZ4'] == '1'
    except KeyError:
        INCLUDE_LZ4 = True
    try:
        INCLUDE_SNAPPY = os.environ['INCLUDE_SNAPPY'] == '1'
    except KeyError:
        INCLUDE_SNAPPY = False  # Snappy is disabled by default
    try:
        INCLUDE_ZLIB = os.environ['INCLUDE_ZLIB'] == '1'
    except KeyError:
        INCLUDE_ZLIB = True
    try:
        INCLUDE_ZSTD = os.environ['INCLUDE_ZSTD'] == '1'
    except KeyError:
        INCLUDE_ZSTD = True


    # Handle --blosc=[PATH] --lflags=[FLAGS] --cflags=[FLAGS]
    args = sys.argv[:]
    for arg in args:
        if arg.find('--blosc=') == 0:
            BLOSC_DIR = os.path.expanduser(arg.split('=')[1])
            sys.argv.remove(arg)
        if arg.find('--lflags=') == 0:
            LFLAGS = arg.split('=')[1].split()
            sys.argv.remove(arg)
        if arg.find('--cflags=') == 0:
            CFLAGS = arg.split('=')[1].split()
            sys.argv.remove(arg)


    # Blosc sources and headers

    # To avoid potential namespace collisions use build_clib.py for each codec
    # instead of co-compiling all sources files in one setuptools.Extension object.
    clibs = [] # for build_clib, libraries TO BE BUILT

    # Below are parameters for the Extension object
    sources = ["blosc/blosc_extension.c"]
    inc_dirs = []
    lib_dirs = []
    libs = []  # Pre-built libraries ONLY, like python36.so
    def_macros = []
    builder_class = build_ext  # To swap out if we have AVX capability and posix
    avx2_defs = {}  # Definitions to build extension with if compiler supports AVX2

    if BLOSC_DIR != '':
        # Using the Blosc library
        lib_dirs += [os.path.join(BLOSC_DIR, 'lib')]
        inc_dirs += [os.path.join(BLOSC_DIR, 'include')]
        libs += ['blosc']
    else:

        # Configure the Extension
        # Compiling everything from included C-Blosc sources
        sources += [f for f in glob('c-blosc/blosc/*.c')
                    if 'avx2' not in f and 'sse2' not in f]

        inc_dirs += [os.path.join('c-blosc', 'blosc')]
        inc_dirs += glob('c-blosc/internal-complibs/*')

        # Codecs to be built with build_clib
        if INCLUDE_LZ4:
            clibs.append( ('lz4', {'sources': glob('c-blosc/internal-complibs/lz4*/*.c')} ) )
            inc_dirs += glob('c-blosc/internal-complibs/lz4*')
            def_macros += [('HAVE_LZ4',1)]

        # Tried and failed to compile Snappy with gcc using 'cflags' on posix
        # setuptools always uses gcc instead of g++, as it only checks for the 
        # env var 'CC' and not 'CXX'.
        if INCLUDE_SNAPPY:
            clibs.append( ('snappy', {'sources': glob('c-blosc/internal-complibs/snappy*/*.cc'), 
                                    'cflags': ['-std=c++11', '-lstdc++'] } ) )
            inc_dirs += glob('c-blosc/internal-complibs/snappy*')
            def_macros += [('HAVE_SNAPPY',1)]

        if INCLUDE_ZLIB:
            clibs.append( ('zlib', {'sources': glob('c-blosc/internal-complibs/zlib*/*.c')} ) )
            def_macros += [('HAVE_ZLIB',1)]

        if INCLUDE_ZSTD:
            clibs.append( ('zstd', {'sources': glob('c-blosc/internal-complibs/zstd*/*/*.c'), 
                        'include_dirs': glob('c-blosc/internal-complibs/zstd*') + glob('c-blosc/internal-complibs/zstd*/common') } ) )
            inc_dirs += glob('c-blosc/internal-complibs/zstd*/common')
            inc_dirs += glob('c-blosc/internal-complibs/zstd*')
            def_macros += [('HAVE_ZSTD',1)]


        # Guess SSE2 or AVX2 capabilities
        # SSE2
        if 'DISABLE_BLOSC_SSE2' not in os.environ and cpu_info != None and 'sse2' in cpu_info.get('flags', {}):
            print('SSE2 detected')
            CFLAGS.append('-DSHUFFLE_SSE2_ENABLED')
            sources += [f for f in glob('c-blosc/blosc/*.c') if 'sse2' in f]
            if os.name == 'posix':
                CFLAGS.append('-msse2')
            elif os.name == 'nt':
                def_macros += [('__SSE2__', 1)]
        # AVX2
        if 'DISABLE_BLOSC_AVX2' not in os.environ and cpu_info != None and 'sse2' in cpu_info.get('flags', {}):
            if os.name == 'posix':
                print("AVX2 detected")
                avx2_defs = {
                    "extra_compile_args": ["-DSHUFFLE_AVX2_ENABLED", "-mavx2"],
                    "sources": [f for f in glob("c-blosc/blosc/*.c") if "avx2" in f]
                }
                # The CPU supports it but the compiler might not..
                builder_class = build_ext_posix_avx2
            elif(os.name == 'nt' and
                    LooseVersion(platform.python_version()) >= LooseVersion('3.5.0')):
                # Neither MSVC2008 for Python 2.7 or MSVC2010 for Python 3.4 have
                # sufficient AVX2 support
                # Since we don't rely on any special compiler capabilities,
                # we don't need to rely on testing the compiler
                print('AVX2 detected')
                CFLAGS.append('-DSHUFFLE_AVX2_ENABLED')
                sources += [f for f in glob('c-blosc/blosc/*.c') if 'avx2' in f]
                def_macros += [('__AVX2__', 1)]
        # TODO: AVX512

    classifiers = dedent("""\
    Development Status :: 5 - Production/Stable
    Intended Audience :: Developers
    Intended Audience :: Information Technology
    Intended Audience :: Science/Research
    License :: OSI Approved :: BSD License
    Programming Language :: Python
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7
    Topic :: Software Development :: Libraries :: Python Modules
    Topic :: System :: Archiving :: Compression
    Operating System :: Microsoft :: Windows
    Operating System :: Unix
    """)

    setup(name = "blosc",
        version = VERSION,
        description = 'Blosc data compressor',
        long_description = long_description,
        classifiers = [c for c in classifiers.split("\n") if c],
        author = 'Francesc Alted, Valentin Haenel',
        author_email = 'faltet@gmail.com, valentin@haenel.co',
        maintainer = 'Francesc Alted, Valentin Haenel',
        maintainer_email = 'faltet@gmail.com, valentin@haenel.co',
        url = 'http://github.com/blosc/python-blosc',
        license = 'https://opensource.org/licenses/BSD-3-Clause',
        platforms = ['any'],
        libraries = clibs,
        ext_modules = [
            BloscExtension( "blosc.blosc_extension",
                    include_dirs=inc_dirs,
                    define_macros=def_macros,
                    sources=sources,
                    library_dirs=lib_dirs,
                    libraries=libs,
                    extra_link_args=LFLAGS,
                    extra_compile_args=CFLAGS,
                    avx2_defs=avx2_defs
            ),
        ],
        tests_require=tests_require,
        zip_safe=False,
        packages = ['blosc'],
        cmdclass={'build_ext': builder_class},
        )
elif __name__ == '__mp_main__':
    # This occurs from `cpuinfo 4.0.0` using multiprocessing to interrogate the 
    # CPUID flags
    # https://github.com/workhorsy/py-cpuinfo/issues/108
    pass
