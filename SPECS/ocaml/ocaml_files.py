# Copyright 2022-3, Jerry James
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of Red Hat nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import os
import shutil
import string
import sys
from collections.abc import Iterable, Iterator
from enum import Enum, auto
from typing import Callable, final

# Version of this script
version=2

#
# BUILDROOT CATEGORIZATION
#

# Directories to ignore when generating %dir entries
root_dirs: set[str] = {
    '/',
    '/etc',
    '/usr',
    '/usr/bin',
    '/usr/lib',
    '/usr/lib/ocaml',
    '/usr/lib/ocaml/caml',
    '/usr/lib/ocaml/stublibs',
    '/usr/lib/ocaml/threads',
    '/usr/lib64',
    '/usr/lib64/ocaml',
    '/usr/lib64/ocaml/caml',
    '/usr/lib64/ocaml/stublibs',
    '/usr/lib64/ocaml/threads',
    '/usr/libexec',
    '/usr/sbin',
    '/usr/share',
    '/usr/share/doc'
}

def find_buildroot_toplevel(buildroot: str) -> list[str]:
    """Find toplevel files and directories in the buildroot.

    :param str buildroot: path to the buildroot
    :return: a list of toplevel files and directories in the buildroot
    """
    bfiles: list[str] = []
    for path, dirs, files in os.walk(buildroot):
        for i in range(len(dirs) - 1, -1, -1):
            d = os.path.join(path, dirs[i])[len(buildroot):]
            if d not in root_dirs and not d.startswith('/usr/share/man'):
                bfiles.append(d)
                del dirs[i]
        for f in files:
            realfile = os.path.join(path, f)[len(buildroot):]
            if realfile.startswith('/usr/share/man'):
                bfiles.append(realfile + '*')
            else:
                bfiles.append(realfile)
    return bfiles

# File suffixes that go into a devel subpackage
dev_suffixes: set[str] = {
    'a', 'cmo', 'cmt', 'cmti', 'cmx', 'cmxa', 'h', 'idl', 'ml', 'mli', 'o'
}

def is_devel_file(filname: str) -> bool:
    """Determine whether a file belongs to a devel subpackage.

    :param str filname: the filename to check
    :return: True if the file belongs to a devel subpackage, else False
    """
    return (filname == 'dune-package' or filname == 'opam' or
            (os.path.splitext(filname)[1][1:] in dev_suffixes
             and not filname.endswith('_top_init.ml')))

def find_buildroot_all(buildroot: str, devel: bool, add_star: bool) -> list[set[str]]:
    """Find all files and directories in the buildroot and optionally
    categorize them as 'main' or 'devel'.

    :param Namespace args: parsed command line arguments
    :param bool devel: True to split into 'main' and 'devel', False otherwise
    :param bool add_star: True to add a star to man page filenames
    :return: a list of files and directories, in this order: main files,
        main directories, devel files, and devel directories
    """
    bfiles: list[set[str]] = [set(), set(), set()]
    bdirs: set[str] = set()
    for path, dirs, files in os.walk(buildroot):
        for d in dirs:
            realdir = os.path.join(path, d)[len(buildroot):]
            if realdir not in root_dirs and not realdir.startswith('/usr/share/man'):
                bdirs.add(realdir)
        for f in files:
            realfile = os.path.join(path, f)[len(buildroot):]
            if devel and is_devel_file(os.path.basename(realfile)):
                bfiles[2].add(realfile)
            else:
                if add_star and realfile.startswith('/usr/share/man'):
                    bfiles[0].add(realfile + '*')
                else:
                    bfiles[0].add(realfile)
                parentdir = os.path.dirname(realfile)
                if parentdir in bdirs:
                    bfiles[1].add(parentdir)
                    bdirs.remove(parentdir)
                    # Catch intermediate directories, as in ocaml-mtime
                    parentdir = os.path.dirname(parentdir)
                    if parentdir in bdirs:
                        bfiles[1].add(parentdir)
                        bdirs.remove(parentdir)
    bfiles.append(bdirs)
    return bfiles

#
# INSTALL FILE LEXER AND PARSER
#

class TokenType(Enum):
    """The types of tokens that can appear in an opam *.install file."""
    ERROR  = auto()
    COLON  = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACK = auto()
    RBRACK = auto()
    STRING = auto()
    FIELD  = auto()

@final
class InstallFileLexer(Iterator[tuple[TokenType, str]]):
    """Convert an opam *.install file into a sequence of tokens."""
    __slots__ = ['index', 'text']

    def __init__(self, filname: str) -> None:
        """Create an opam *.install file lexer.

        :param str filname: the name of the file to read from
        """
        self.index = 0
        with open(filname, 'r') as f:
            # Limit reads to 4 MB in case this file is bogus.
            # Most install files are under 4K.
            self.text = f.read(4194304)

    def skip_whitespace(self) -> None:
        """Skip over whitespace in the input."""
        while self.index < len(self.text) and \
              (self.text[self.index] == '#' or
               self.text[self.index] in string.whitespace):
            if self.text[self.index] == '#':
                while (self.index < len(self.text) and
                       self.text[self.index] != '\n' and
                       self.text[self.index] != '\r'):
                    self.index += 1
            else:
                self.index += 1

    def __next__(self) -> tuple[TokenType, str]:
        """Get the next token from the opam *.install file.

        :return: a pair containing the type and text of the next token
        """
        self.skip_whitespace()
        if self.index < len(self.text):
            ch = self.text[self.index]
            if ch == ':':
                self.index += 1
                return (TokenType.COLON, ch)
            if ch == '{':
                self.index += 1
                return (TokenType.LBRACE, ch)
            if ch == '}':
                self.index += 1
                return (TokenType.RBRACE, ch)
            if ch == '[':
                self.index += 1
                return (TokenType.LBRACK, ch)
            if ch == ']':
                self.index += 1
                return (TokenType.RBRACK, ch)
            if ch == '"':
                start = self.index + 1
                end = start
                while end < len(self.text) and self.text[end] != '"':
                    end += 2 if self.text[end] == '\\' else 1
                self.index = end + 1
                return (TokenType.STRING, self.text[start:end])
            if ch in string.ascii_letters:
                start = self.index
                end = start + 1
                while (end < len(self.text) and
                       (self.text[end] == '_' or
                        self.text[end] in string.ascii_letters)):
                    end += 1
                self.index = end
                return (TokenType.FIELD, self.text[start:end])
            return (TokenType.ERROR, ch)
        else:
            raise StopIteration

@final
class InstallFileParser(Iterable[tuple[str, bool, str, str]]):
    """Parse opam *.install files."""

    __slots__ = ['pkgname', 'lexer', 'libdir']

    def __init__(self, filname: str, libdir: str) -> None:
        """Initialize an OCaml .install file parser.

        :param str filname: name of the .install file to parse
        :param str libdir: the OCaml library directory
        """
        self.pkgname = os.path.splitext(os.path.basename(filname))[0]
        self.lexer = InstallFileLexer(filname)
        self.libdir = libdir

    def __iter__(self) -> Iterator[tuple[str, bool, str, str]]:
        """Parse a .install file.
        If there are any parse errors, we assume this file is not really an
        opam .install file and abandon the parse.
        """
        # Map opam installer names to directories
        opammap: dict[str, str] = {
            'lib': os.path.join(self.libdir, self.pkgname),
            'lib_root': self.libdir,
            'libexec': os.path.join(self.libdir, self.pkgname),
            'libexec_root': self.libdir,
            'bin': '/usr/bin',
            'sbin': '/usr/sbin',
            'toplevel': os.path.join(self.libdir, 'toplevel'),
            'share': os.path.join('/usr/share', self.pkgname),
            'share_root': '/usr/share',
            'etc': os.path.join('/etc', self.pkgname),
            'doc': os.path.join('/usr/doc', self.pkgname),
            'stublibs': os.path.join(self.libdir, 'stublibs'),
            'man': '/usr/share/man'
        }

        # Parse the file
        try:
            toktyp, token = next(self.lexer)
            while toktyp == TokenType.FIELD:
                libname = token
                toktyp, token = next(self.lexer)
                if toktyp != TokenType.COLON:
                    return

                toktyp, token = next(self.lexer)
                if toktyp != TokenType.LBRACK:
                    return

                directory = opammap.get(libname)
                if not directory:
                    return

                toktyp, token = next(self.lexer)
                while toktyp == TokenType.STRING:
                    source = token
                    optional = source[0] == '?'
                    if optional:
                        source = source[1:]
                    nexttp, nexttk = next(self.lexer)
                    if nexttp == TokenType.LBRACE:
                        nexttp, nexttk = next(self.lexer)
                        if nexttp == TokenType.STRING:
                            filname = os.path.join(directory, nexttk)
                            bracetp, bractk = next(self.lexer)
                            if bracetp != TokenType.RBRACE:
                                return
                            nexttp, nexttk = next(self.lexer)
                        else:
                            return
                    elif libname == 'man':
                        index = token.rfind('.')
                        if index < 0:
                            return
                        mandir = os.path.join(directory, 'man' + token[index+1:])
                        filname = os.path.join(mandir, os.path.basename(token))
                    else:
                        filname = os.path.join(directory, os.path.basename(token))
                    toktyp, token = nexttp, nexttk
                    yield (self.pkgname, optional, source, filname)

                if toktyp != TokenType.RBRACK:
                    return
                toktyp, token = next(self.lexer)
        except StopIteration:
            return

def install_files(buildroot: str, libdir: str) -> None:
    """Install the files listed in opam .install files in the buildroot.

    For some projects, there are install files in both the project root
    directory and somewhere under "_build", so be careful not to parse the same
    install file twice.

    :param str buildroot: path to the buildroot
    :param str libdir: the OCaml library directory
    """
    install_files = set()
    for path, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.install') and f not in install_files:
                install_files.add(f)
                parser = InstallFileParser(os.path.join(path, f), libdir)
                for _, optional, source, filname in parser:
                    if not optional or os.path.exists(source):
                        installpath = os.path.join(buildroot, filname[1:])
                        os.makedirs(os.path.dirname(installpath), exist_ok=True)
                        shutil.copy2(source, installpath)

def get_package_map(buildroot: str, libdir: str, devel: bool) -> dict[str, set[str]]:
    """Create a map from package names to installed files from the opam .install
    files in the buildroot.

    For some projects, there are install files in both the project root
    directory and somewhere under "_build", so be careful not to parse the same
    install file twice."""

    pmap: dict[str, set[str]] = dict()
    install_files = set()

    def add_pkg(pkgname: str, filname: str) -> None:
        """Add a mapping from a package name to a filename.

        :param str pkgname: the package that acts as the map key
        :param str filname: the filename to add to the package set
        """
        if pkgname not in pmap:
            pmap[pkgname] = set()
        pmap[pkgname].add(filname)

    installed = find_buildroot_all(buildroot, devel, False)
    for path, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.install') and f not in install_files:
                install_files.add(f)
                parser = InstallFileParser(os.path.join(path, f), libdir)
                for pkgname, _, _, filname in parser:
                    if filname in installed[0]:
                        if filname.startswith('/usr/share/man'):
                            add_pkg(pkgname, filname + '*')
                        else:
                            add_pkg(pkgname, filname)
                            dirname = os.path.dirname(filname)
                            if dirname in installed[1]:
                                add_pkg(pkgname, '%dir ' + dirname)
                                installed[1].remove(dirname)
                    elif filname in installed[2]:
                        if filname.startswith('/usr/share/man'):
                            add_pkg(pkgname + '-devel', filname + '*')
                        else:
                            add_pkg(pkgname + '-devel', filname)
                            dirname = os.path.dirname(filname)
                            if dirname in installed[3]:
                                add_pkg(pkgname + '-devel', '%dir ' + dirname)
                                installed[3].remove(dirname)
    return pmap

#
# MAIN INTERFACE
#

def ocaml_files(no_devel: bool, separate: bool, install: bool, buildroot: str,
                libdir: str) -> None:
    """Generate %files lists from an installed buildroot.

    :param bool no_devel: False to split files into a main package and a devel
        package
    :param bool separate: True to place each OCaml module in an RPM package
    :param bool install: True to install files, False to generate %files
    :param str buildroot: the installed buildroot
    :param str libdir: the OCaml library directory
    """
    if install:
        install_files(buildroot, libdir)
    elif separate:
        pkgmap = get_package_map(buildroot, libdir, not no_devel)
        for pkg in pkgmap:
            with open('.ofiles-' + pkg, 'w') as f:
                for entry in pkgmap[pkg]:
                    f.write(entry + '\n')
    elif no_devel:
        with open('.ofiles', 'w') as f:
            for entry in find_buildroot_toplevel(buildroot):
                f.write(entry + '\n')
    else:
        files = find_buildroot_all(buildroot, True, True)
        with open('.ofiles', 'w') as f:
            for entry in files[0]:
                f.write(entry + '\n')
            for entry in files[1]:
                f.write('%dir ' + entry + '\n')
        with open('.ofiles-devel', 'w') as f:
            for entry in files[2]:
                f.write(entry + '\n')
            for entry in files[3]:
                f.write('%dir ' + entry + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Support for building OCaml RPM packages')
    parser.add_argument('-i', '--install',
                        action='store_true',
                        default=False,
                        help='install files instead of generating %files')
    parser.add_argument('-n', '--no-devel',
                        action='store_true',
                        default=False,
                        help='suppress creation of a devel subpackage')
    parser.add_argument('-s', '--separate',
                        action='store_true',
                        default=False,
                        help='separate packaging.  Each OCaml module is in a distinct RPM package.  All modules are in a single RPM package by default.')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=f'%(prog)s {str(version)}')
    parser.add_argument('buildroot', help='RPM build root')
    parser.add_argument('libdir', help='OCaml library directory')
    args = parser.parse_args()
    ocaml_files(args.no_devel,
                args.separate,
                args.install,
                args.buildroot,
                args.libdir)