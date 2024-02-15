import argparse
import fnmatch
import json
import os

from collections import defaultdict
from keyword import iskeyword
from pathlib import PosixPath, PurePosixPath
from importlib.metadata import Distribution


# From RPM's build/files.c strtokWithQuotes delim argument
RPM_FILES_DELIMETERS = ' \n\t'

# See the comment in the macro that wraps this script
RPM_PERCENTAGES_COUNT = int(os.getenv('RPM_PERCENTAGES_COUNT', '2'))

# RPM hardcodes the lists of manpage extensions and directories,
# so we have to maintain separate ones :(
# There is an issue for RPM to provide the lists as macros:
# https://github.com/rpm-software-management/rpm/issues/1865
# The original lists can be found here:
# https://github.com/rpm-software-management/rpm/blob/master/scripts/brp-compress
MANPAGE_EXTENSIONS = ['gz', 'Z', 'bz2', 'xz', 'lzma', 'zst', 'zstd']
MANDIRS = [
    '/man/man*',
    '/man/*/man*',
    '/info',
    '/share/man/man*',
    '/share/man/*/man*',
    '/share/info',
    '/kerberos/man',
    '/X11R6/man/man*',
    '/lib/perl5/man/man*',
    '/share/doc/*/man/man*',
    '/lib/*/man/man*',
    '/share/fish/man/man*',
]


class BuildrootPath(PurePosixPath):
    """
    This path represents a path in a buildroot.
    When absolute, it is "relative" to a buildroot.

    E.g. /usr/lib means %{buildroot}/usr/lib
    The object carries no buildroot information.
    """

    @staticmethod
    def from_real(realpath, *, root):
        """
        For a given real disk path, return a BuildrootPath in the given root.

        For example::

            >>> BuildrootPath.from_real(PosixPath('/tmp/buildroot/foo'), root=PosixPath('/tmp/buildroot'))
            BuildrootPath('/foo')
        """
        return BuildrootPath("/") / realpath.relative_to(root)

    def to_real(self, root):
        """
        Return a real PosixPath in the given root

        For example::

            >>> BuildrootPath('/foo').to_real(PosixPath('/tmp/buildroot'))
            PosixPath('/tmp/buildroot/foo')
        """
        return root / self.relative_to("/")

    def normpath(self):
        """
        Normalize all the potential /../ parts of the path without touching real files.

        PurePaths don't have .resolve().
        Paths have .resolve() but it touches real files.
        This is an alternative. It assumes there are no symbolic links.

        Example:

            >>> BuildrootPath('/usr/lib/python/../pypy').normpath()
            BuildrootPath('/usr/lib/pypy')
        """
        return type(self)(os.path.normpath(self))


def pycache_dir(script):
    """
    For a script BuildrootPath, return a BuildrootPath of its __pycache__ directory.

    Example:

        >>> pycache_dir(BuildrootPath('/whatever/bar.py'))
        BuildrootPath('/whatever/__pycache__')

        >>> pycache_dir(BuildrootPath('/opt/python3.10/foo.py'))
        BuildrootPath('/opt/python3.10/__pycache__')
    """
    return script.parent / "__pycache__"


def pycached(script, python_version):
    """
    For a script BuildrootPath, return a list with that path and its bytecode glob.
    Like the %pycached macro.

    The glob is represented as a BuildrootPath.

    Examples:

        >>> pycached(BuildrootPath('/whatever/bar.py'), '3.8')
        [BuildrootPath('/whatever/bar.py'), BuildrootPath('/whatever/__pycache__/bar.cpython-38{,.opt-?}.pyc')]

        >>> pycached(BuildrootPath('/opt/python3.10/foo.py'), '3.10')
        [BuildrootPath('/opt/python3.10/foo.py'), BuildrootPath('/opt/python3.10/__pycache__/foo.cpython-310{,.opt-?}.pyc')]
    """
    assert script.suffix == ".py"
    pyver = "".join(python_version.split(".")[:2])
    pycname = f"{script.stem}.cpython-{pyver}{{,.opt-?}}.pyc"
    pyc = pycache_dir(script) / pycname
    return [script, pyc]


def add_file_to_module(paths, module_name, module_type, files_dirs, *files):
    """
    Helper procedure, adds given files to the module_name of a given module_type
    """
    for module in paths["modules"][module_name]:
        if module["type"] == module_type:
            if files[0] not in module[files_dirs]:
                module[files_dirs].extend(files)
            break
    else:
        paths["modules"][module_name].append(
            {"type": module_type, "files": [], "dirs": [], files_dirs: list(files)}
        )


def add_py_file_to_module(paths, module_name, module_type, path, python_version,
                          *, include_pycache_dir):
    """
    Helper procedure, adds given .py file to the module_name of a given module_type
    Always also adds the bytecode cache.
    If include_pycache_dir is set, also include the __pycache__ directory.
    """
    add_file_to_module(paths, module_name, module_type, "files", *pycached(path, python_version))
    if include_pycache_dir:
        add_file_to_module(paths, module_name, module_type, "dirs", pycache_dir(path))


def add_lang_to_module(paths, module_name, path):
    """
    Helper procedure, divides lang files by language and adds them to the module_name

    Returns True if the language code detection was successful
    """
    for i, parent in enumerate(path.parents):
        if parent.name == 'LC_MESSAGES':
            lang_country_code = path.parents[i+1].name
            break
    else:
        return False
    # convert potential en_US to plain en
    lang_code = lang_country_code.partition('_')[0]
    if module_name not in paths["lang"]:
        paths["lang"].update({module_name: defaultdict(list)})
    paths["lang"][module_name][lang_code].append(path)
    return True


def prepend_mandirs(prefix):
    """
    Return the list of man page directories prepended with the given prefix.
    """
    return [str(prefix) + mandir for mandir in MANDIRS]


def normalize_manpage_filename(prefix, path):
    """
    If a path is processed by RPM's brp-compress script, strip it of the extension
    (if the extension matches one of the listed by brp-compress),
    append '*' to the filename and return it. If not, return the unchanged path.
    Rationale: https://docs.fedoraproject.org/en-US/packaging-guidelines/#_manpages

    Examples:

        >>> normalize_manpage_filename(PosixPath('/usr'), BuildrootPath('/usr/share/man/de/man1/linkchecker.1'))
        BuildrootPath('/usr/share/man/de/man1/linkchecker.1*')

        >>> normalize_manpage_filename(PosixPath('/usr'), BuildrootPath('/usr/share/doc/en/man/man1/getmac.1'))
        BuildrootPath('/usr/share/doc/en/man/man1/getmac.1*')

        >>> normalize_manpage_filename(PosixPath('/usr'), BuildrootPath('/usr/share/man/man8/abc.8.zstd'))
        BuildrootPath('/usr/share/man/man8/abc.8*')

        >>> normalize_manpage_filename(PosixPath('/usr'), BuildrootPath('/usr/kerberos/man/dir'))
        BuildrootPath('/usr/kerberos/man/dir')

        >>> normalize_manpage_filename(PosixPath('/usr'), BuildrootPath('/usr/kerberos/man/dir.1'))
        BuildrootPath('/usr/kerberos/man/dir.1*')

        >>> normalize_manpage_filename(PosixPath('/usr'), BuildrootPath('/usr/bin/getmac'))
        BuildrootPath('/usr/bin/getmac')
    """

    prefixed_mandirs = prepend_mandirs(prefix)
    for mandir in prefixed_mandirs:
        # "dir" is explicitly excluded by RPM
        # https://github.com/rpm-software-management/rpm/blob/rpm-4.17.0-release/scripts/brp-compress#L24
        if fnmatch.fnmatch(str(path.parent), mandir) and path.name != "dir":
            # "abc.1.gz2" -> "abc.1*"
            if path.suffix[1:] in MANPAGE_EXTENSIONS:
                return BuildrootPath(path.parent / (path.stem + "*"))
            # "abc.1 -> abc.1*"
            else:
                return BuildrootPath(path.parent / (path.name + "*"))
    else:
        return path


def is_valid_module_name(s):
    """Return True if a string is considered a valid module name and False otherwise.

    String must be a valid Python name, not a Python keyword and must not
    start with underscore - we treat those as private.
    Examples:

        >>> is_valid_module_name('module_name')
        True

        >>> is_valid_module_name('12module_name')
        False

        >>> is_valid_module_name('module-name')
        False

        >>> is_valid_module_name('return')
        False

        >>> is_valid_module_name('_module_name')
        False
    """
    if (s.isidentifier() and not iskeyword(s) and not s.startswith("_")):
        return True
    return False


def module_names_from_path(path):
    """Get all importable module names from given path.

    Paths containing ".py" and ".so" files are considered importable modules,
    and so their respective directories (ie. "foo/bar/baz.py": "foo", "foo.bar",
    "foo.bar.baz").
    Paths containing invalid Python strings are discarded.

    Return set of all valid possibilities.
    """
    # Discard all files that are not valid modules
    if path.suffix not in (".py", ".so"):
        return set()

    parts = list(path.parts)

    # Modify the file names according to their suffixes
    if path.suffix == ".py":
        parts[-1] = path.stem
    elif path.suffix == ".so":
        # .so files can have two suffixes - cut both of them
        parts[-1] = PosixPath(path.stem).stem

    # '__init__' indicates a module but we don't want to import the actual file
    # It's unclear whether there can be __init__.so files in the Python packages.
    # The idea to implement this file was raised in 2008 on Python-ideas mailing list
    # (https://mail.python.org/pipermail/python-ideas/2008-October/002292.html)
    # and there are a few reports of people compiling their __init__.py to __init__.so.
    # However it's not officially documented nor forbidden,
    # so we're checking for the stem after stripping the suffix from the file.
    if parts[-1] == "__init__":
        del parts[-1]

    # For each part of the path check whether it's valid
    # If not, discard the whole path - return an empty set
    for path_part in parts:
        if not is_valid_module_name(path_part):
            return set()
    else:
        return {'.'.join(parts[:x+1]) for x in range(len(parts))}


def is_license_file(path, license_files, license_directories):
    """
    Check if the given BuildrootPath path matches any of the "License-File" entries.
    The path is considered matched when resolved from any of the license_directories
    matches string-wise what is stored in any "License-File" entry (license_files).

    Examples:
        >>> site_packages = BuildrootPath('/usr/lib/python3.12/site-packages')
        >>> distinfo = site_packages / 'foo-1.0.dist-info'
        >>> license_directories = [distinfo / 'licenses', distinfo]
        >>> license_files = ['LICENSE.txt', 'AUTHORS.md']
        >>> is_license_file(distinfo / 'AUTHORS.md', license_files, license_directories)
        True
        >>> is_license_file(distinfo / 'licenses/LICENSE.txt', license_files, license_directories)
        True
        >>> # we don't match based on directory only
        >>> is_license_file(distinfo / 'licenses/COPYING', license_files, license_directories)  
        False
        >>> is_license_file(site_packages / 'foo/LICENSE.txt', license_files, license_directories)
        False
    """
    if not license_files or not license_directories:
        return False
    for license_dir in license_directories:
        if (path.is_relative_to(license_dir) and
                str(path.relative_to(license_dir)) in license_files):
            return True
    return False


def classify_paths(
    record_path, parsed_record_content, metadata, sitedirs, python_version, prefix
):
    """
    For each BuildrootPath in parsed_record_content classify it to a dict structure
    that allows to filter the files for the %files and %check section easier.

    For the dict structure, look at the beginning of this function's code.

    Each "module" is a dict with "type" ("package", "script", "extension"), and "files" and "dirs".
    """
    distinfo = record_path.parent
    paths = {
        "metadata": {
            "files": [],  # regular %file entries with dist-info content
            "dirs": [distinfo],  # %dir %file entries with dist-info directory
            "docs": [],  # to be used once there is upstream way to recognize READMEs
            "licenses": [],  # %license entries parsed from dist-info METADATA file
        },
        "lang": {}, # %lang entries: [module_name or None][language_code] lists of .mo files
        "modules": defaultdict(list),  # each importable module (directory, .py, .so)
        "module_names": set(),  # qualified names of each importable module ("foo.bar.baz")
        "other": {"files": []},  # regular %file entries we could not parse :(
    }

    license_files = metadata.get_all('License-File')
    license_directory = distinfo / 'licenses'  # See PEP 639 "Root License Directory"
    # setuptools was the first known build backend to implement License-File.
    # Unfortunately they don't put licenses to the license directory (yet):
    #     https://github.com/pypa/setuptools/issues/3596
    # Hence, we check licenses in both licenses and dist-info
    license_directories = (license_directory, distinfo)

    # In RECORDs generated by pip, there are no directories, only files.
    # The example RECORD from PEP 376 does not contain directories either.
    # Hence, we'll only assume files, but TODO get it officially documented.
    for path in parsed_record_content:
        if path.suffix == ".pyc":
            # we handle bytecode separately
            continue

        if distinfo in path.parents:
            if path.parent == distinfo and path.name in ("RECORD", "REQUESTED"):
                # RECORD and REQUESTED files are removed in %pyproject_install
                # See PEP 627
                continue
            if is_license_file(path, license_files, license_directories):
                paths["metadata"]["licenses"].append(path)
            else:
                paths["metadata"]["files"].append(path)
            # nested directories within distinfo
            index = path.parents.index(distinfo)
            for parent in list(path.parents)[:index]:  # no direct slice until Python 3.10
                if parent not in paths["metadata"]["dirs"]:
                    paths["metadata"]["dirs"].append(parent)
            continue

        for sitedir in sitedirs:
            if sitedir in path.parents:
                # Get only the part without sitedir prefix to classify module names
                relative_path = path.relative_to(sitedir)
                paths["module_names"].update(module_names_from_path(relative_path))
                if path.parent == sitedir:
                    if path.suffix == ".so":
                        # extension modules can have 2 suffixes
                        name = BuildrootPath(path.stem).stem
                        add_file_to_module(paths, name, "extension", "files", path)
                    elif path.suffix == ".py":
                        name = path.stem
                        # we add the .pyc files, but not top-level __pycache__
                        add_py_file_to_module(
                            paths, name, "script", path, python_version,
                            include_pycache_dir=False
                        )
                    else:
                        paths["other"]["files"].append(path)
                else:
                    # this file is inside a dir, we add all dirs upwards until sitedir
                    index = path.parents.index(sitedir)
                    module_dir = path.parents[index - 1]
                    for parent in list(path.parents)[:index]:  # no direct slice until Python 3.10
                        add_file_to_module(paths, module_dir.name, "package", "dirs", parent)
                    is_lang = False
                    if path.suffix == ".mo":
                        is_lang = add_lang_to_module(paths, module_dir.name, path)
                    if not is_lang:
                        if path.suffix == ".py":
                            # we add the .pyc files, and their __pycache__
                            add_py_file_to_module(
                                paths, module_dir.name, "package", path, python_version,
                                include_pycache_dir=True
                            )
                        else:
                            add_file_to_module(paths, module_dir.name, "package", "files", path)
                break
        else:
            if path.suffix == ".mo":
                add_lang_to_module(paths, None, path) or paths["other"]["files"].append(path)
            else:
                path = normalize_manpage_filename(prefix, path)
                paths["other"]["files"].append(path)

    return paths


def escape_rpm_path(path):
    """
    Escape special characters in string-paths or BuildrootPaths

    E.g. a space in path otherwise makes RPM think it's multiple paths,
    unless we put it in "quotes".
    Or a literal % symbol in path might be expanded as a macro if not escaped.

    Due to limitations in RPM,
    some paths with spaces and other special characters are not supported.

    Examples:

        >>> escape_rpm_path(BuildrootPath('/usr/lib/python3.9/site-packages/setuptools'))
        '/usr/lib/python3.9/site-packages/setuptools'

        >>> escape_rpm_path('/usr/lib/python3.9/site-packages/setuptools/script (dev).tmpl')
        '"/usr/lib/python3.9/site-packages/setuptools/script (dev).tmpl"'

        >>> escape_rpm_path('/usr/share/data/100%valid.path')
        '/usr/share/data/100%%valid.path'

        >>> escape_rpm_path('/usr/share/data/100 % valid.path')
        '"/usr/share/data/100 %% valid.path"'

        >>> escape_rpm_path('/usr/share/data/1000 %% valid.path')
        '"/usr/share/data/1000 %%%% valid.path"'

        >>> escape_rpm_path('/usr/share/data/spaces and "quotes"')
        Traceback (most recent call last):
          ...
        NotImplementedError: ...

        >>> escape_rpm_path('/usr/share/data/spaces and [square brackets]')
        Traceback (most recent call last):
          ...
        NotImplementedError: ...
    """
    orig_path = path = str(path)
    if "%" in path:
        path = path.replace("%", "%" * RPM_PERCENTAGES_COUNT)
    if any(symbol in path for symbol in RPM_FILES_DELIMETERS):
        if '"' in path:
            # As far as we know, RPM cannot list such file individually
            # See this thread http://lists.rpm.org/pipermail/rpm-list/2021-June/002048.html
            raise NotImplementedError(f'" symbol in path with spaces is not supported by %pyproject_save_files: {orig_path!r}')
        if "[" in path or "]" in path:
            # See https://bugzilla.redhat.com/show_bug.cgi?id=1990879
            # and https://github.com/rpm-software-management/rpm/issues/1749
            raise NotImplementedError(f'[ or ] symbol in path with spaces is not supported by %pyproject_save_files: {orig_path!r}')
        return f'"{path}"'
    return path


def generate_file_list(paths_dict, module_globs, include_others=False):
    """
    This function takes the classified paths_dict and turns it into lines
    for the %files section. Returns list with text lines, no Path objects.

    Only includes files from modules that match module_globs, metadata and
    optionaly all other files.

    It asserts that all globs match at least one module, raises ValueError otherwise.
    Multiple globs matching identical module(s) are OK.
    """
    files = set()

    if include_others:
        files.update(f"{escape_rpm_path(p)}" for p in paths_dict["other"]["files"])
        try:
            for lang_code in paths_dict["lang"][None]:
                files.update(f"%lang({lang_code}) {escape_rpm_path(p)}" for p in paths_dict["lang"][None][lang_code])
        except KeyError:
            pass

    files.update(f"{escape_rpm_path(p)}" for p in paths_dict["metadata"]["files"])
    for macro in "dir", "doc", "license":
        files.update(f"%{macro} {escape_rpm_path(p)}" for p in paths_dict["metadata"][f"{macro}s"])

    modules = paths_dict["modules"]
    done_modules = set()
    done_globs = set()

    for glob in module_globs:
        for name in modules:
            if fnmatch.fnmatchcase(name, glob):
                if name not in done_modules:
                    try:
                        for lang_code in paths_dict["lang"][name]:
                            files.update(f"%lang({lang_code}) {escape_rpm_path(p)}" for p in paths_dict["lang"][name][lang_code])
                    except KeyError:
                        pass
                    for module in modules[name]:
                        files.update(f"%dir {escape_rpm_path(p)}" for p in module["dirs"])
                        files.update(f"{escape_rpm_path(p)}" for p in module["files"])
                    done_modules.add(name)
                done_globs.add(glob)

    # Users using '*' don't care about the files in the package, so it's ok
    # not to fail the build when no modules are detected
    # There can be legitimate reasons to create a package without Python modules
    if not modules and fnmatch.fnmatchcase("", glob):
        done_globs.add(glob)

    missed = module_globs - done_globs
    if missed:
        missed_text = ", ".join(sorted(missed))
        raise ValueError(f"Globs did not match any module: {missed_text}")

    return sorted(files)


def generate_module_list(paths_dict, module_globs):
    """
    This function takes the paths_dict created by the classify_paths() function and
    reads the modules names from it.
    It filters those whose top-level module names match any of the provided module_globs.

    Returns list with matching qualified module names.

    Examples:

        >>> generate_module_list({'module_names': {'foo', 'foo.bar', 'baz'}}, {'foo'})
        ['foo', 'foo.bar']

        >>> generate_module_list({'module_names': {'foo', 'foo.bar', 'baz'}}, {'*foo'})
        ['foo', 'foo.bar']

        >>> generate_module_list({'module_names': {'foo', 'foo.bar', 'baz'}}, {'foo', 'baz'})
        ['baz', 'foo', 'foo.bar']

        >>> generate_module_list({'module_names': {'foo', 'foo.bar', 'baz'}}, {'*'})
        ['baz', 'foo', 'foo.bar']

        >>> generate_module_list({'module_names': {'foo', 'foo.bar', 'baz'}}, {'bar'})
        []

    Submodules aren't discovered:

        >>> generate_module_list({'module_names': {'foo', 'foo.bar', 'baz'}}, {'*bar'})
        []
    """

    module_names = paths_dict['module_names']
    filtered_module_names = set()

    for glob in module_globs:
        for name in module_names:
            # Match the top-level part of the qualified name, eg. 'foo.bar.baz' -> 'foo'
            top_level_name = name.split('.')[0]
            if fnmatch.fnmatchcase(top_level_name, glob):
                filtered_module_names.add(name)

    return sorted(filtered_module_names)


def parse_varargs(varargs):
    """
    Parse varargs from the %pyproject_save_files macro

    Arguments starting with + are treated as a flags, everything else is a glob

    Returns as set of globs, boolean flag whether to include all the other files

    Raises ValueError for unknown flags and globs with dots (namespace packages).

    Good examples:

        >>> parse_varargs(['*'])
        ({'*'}, False)

        >>> mods, auto = parse_varargs(['requests*', 'kerberos', '+auto'])
        >>> auto
        True
        >>> sorted(mods)
        ['kerberos', 'requests*']

        >>> mods, auto = parse_varargs(['tldr', 'tensorf*'])
        >>> auto
        False
        >>> sorted(mods)
        ['tensorf*', 'tldr']

        >>> parse_varargs(['+auto'])
        (set(), True)

    Bad examples:

        >>> parse_varargs(['+kinkdir'])
        Traceback (most recent call last):
          ...
        ValueError: Invalid argument: +kinkdir

        >>> parse_varargs(['good', '+bad', '*ugly*'])
        Traceback (most recent call last):
          ...
        ValueError: Invalid argument: +bad

        >>> parse_varargs(['+bad', 'my.bad'])
        Traceback (most recent call last):
          ...
        ValueError: Invalid argument: +bad

        >>> parse_varargs(['mod', 'mod.*'])
        Traceback (most recent call last):
          ...
        ValueError: Attempted to use a namespaced package with . in the glob: mod.*. ...

        >>> parse_varargs(['my.bad', '+bad'])
        Traceback (most recent call last):
          ...
        ValueError: Attempted to use a namespaced package with . in the glob: my.bad. ...

        >>> parse_varargs(['mod/submod'])
        Traceback (most recent call last):
          ...
        ValueError: Attempted to use a namespaced package with / in the glob: mod/submod. ...
    """
    include_auto = False
    globs = set()
    namespace_error_template = (
        "Attempted to use a namespaced package with {symbol} in the glob: {arg}. "
        "That is not (yet) supported. Use {top} instead and see "
        "https://bugzilla.redhat.com/1935266 for details."
    )
    for arg in varargs:
        if arg.startswith("+"):
            if arg == "+auto":
                include_auto = True
            else:
                raise ValueError(f"Invalid argument: {arg}")
        elif "." in arg:
            top, *_ = arg.partition(".")
            raise ValueError(namespace_error_template.format(symbol=".", arg=arg, top=top))
        elif "/" in arg:
            top, *_ = arg.partition("/")
            raise ValueError(namespace_error_template.format(symbol="/", arg=arg, top=top))
        else:
            globs.add(arg)

    return globs, include_auto


def load_parsed_record(pyproject_record):
    parsed_record = {}
    with open(pyproject_record) as pyproject_record_file:
        content = json.load(pyproject_record_file)

    if len(content) > 1:
        raise FileExistsError("%pyproject_install has found more than one *.dist-info/RECORD file. "
                              "Currently, %pyproject_save_files supports only one wheel → one file list mapping. "
                              "Feel free to open a bugzilla for pyproject-rpm-macros and describe your usecase.")

    # Redefine strings stored in JSON to BuildRootPaths
    for record_path, files in content.items():
        parsed_record[BuildrootPath(record_path)] = [BuildrootPath(f) for f in files]

    return parsed_record


def dist_metadata(buildroot, record_path):
    """
    Returns distribution metadata (email.message.EmailMessage), possibly empty
    """
    real_dist_path = record_path.parent.to_real(buildroot)
    dist = Distribution.at(real_dist_path)
    return dist.metadata


def pyproject_save_files_and_modules(buildroot, sitelib, sitearch, python_version, pyproject_record, prefix, assert_license, varargs):
    """
    Takes arguments from the %{pyproject_save_files} macro

    Returns tuple: list of paths for the %files section and list of module names
    for the %check section

    Raises ValueError when assert_license is true and no License-File (PEP 639)
    is found.
    """
    # On 32 bit architectures, sitelib equals to sitearch
    # This saves us browsing one directory twice
    sitedirs = sorted({sitelib, sitearch})

    globs, include_auto = parse_varargs(varargs)
    parsed_records = load_parsed_record(pyproject_record)

    final_file_list = []
    final_module_list = []

    # we assume OK when not asserting
    license_ok = not assert_license

    for record_path, files in parsed_records.items():
        metadata = dist_metadata(buildroot, record_path)
        paths_dict = classify_paths(
            record_path, files, metadata, sitedirs, python_version, prefix
        )
        license_ok = license_ok or bool(paths_dict["metadata"]["licenses"])

        final_file_list.extend(
            generate_file_list(paths_dict, globs, include_auto)
        )
        final_module_list.extend(
            generate_module_list(paths_dict, globs)
        )

    if not license_ok:
        raise ValueError(
            "No License-File (PEP 639) in upstream metadata found. "
            "Adjust the upstream metadata "
            "if the project's build backend supports PEP 639 "
            "or use `%pyproject_save_files -L` "
            "and include the %license file in %files manually."
        )

    return final_file_list, final_module_list


def main(cli_args):
    file_section, module_names = pyproject_save_files_and_modules(
        cli_args.buildroot,
        cli_args.sitelib,
        cli_args.sitearch,
        cli_args.python_version,
        cli_args.pyproject_record,
        cli_args.prefix,
        cli_args.assert_license,
        cli_args.varargs,
    )

    cli_args.output_files.write_text("\n".join(file_section) + "\n", encoding="utf-8")
    cli_args.output_modules.write_text("\n".join(module_names) + "\n", encoding="utf-8")


def argparser():
    parser = argparse.ArgumentParser(
        description="Create %{pyproject_files} for a Python project.",
        prog="%pyproject_save_files",
        add_help=False,
        # custom usage to add +auto
        usage="%(prog)s  [-l|-L] MODULE_GLOB [MODULE_GLOB ...] [+auto]",
    )
    parser.add_argument(
        '--help', action='help',
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS,
    )
    r = parser.add_argument_group("required arguments")
    r.add_argument("--output-files", type=PosixPath, required=True, help=argparse.SUPPRESS)
    r.add_argument("--output-modules", type=PosixPath, required=True, help=argparse.SUPPRESS)
    r.add_argument("--buildroot", type=PosixPath, required=True, help=argparse.SUPPRESS)
    r.add_argument("--sitelib", type=BuildrootPath, required=True, help=argparse.SUPPRESS)
    r.add_argument("--sitearch", type=BuildrootPath, required=True, help=argparse.SUPPRESS)
    r.add_argument("--python-version", type=str, required=True, help=argparse.SUPPRESS)
    r.add_argument("--pyproject-record", type=PosixPath, required=True, help=argparse.SUPPRESS)
    r.add_argument("--prefix", type=PosixPath, required=True, help=argparse.SUPPRESS)
    parser.add_argument(
        "-l", "--assert-license", action="store_true", default=False,
        help="Fail when no License-File (PEP 639) is found.",
    )
    parser.add_argument(
        "-L", "--no-assert-license", action="store_false", dest="assert_license",
        help="Don't fail when no License-File (PEP 639) is found (the default).",
    )
    parser.add_argument(
        "varargs", nargs="+", metavar="MODULE_GLOB",
        help="Shell-like glob matching top-level module names to save into %%{pyproject_files}",
    )
    return parser


if __name__ == "__main__":
    cli_args = argparser().parse_args()
    main(cli_args)
