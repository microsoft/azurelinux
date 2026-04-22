# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without tests


%global desc %{expand:
Python library for parsing and manipulating RPM spec files.
Main focus is on modifying existing spec files, any change should result
in a minimal diff.}


%global base_version 0.39.1
#global prerelease   rc1

%global package_version %{base_version}%{?prerelease:~%{prerelease}}
%global pypi_version    %{base_version}%{?prerelease}


Name:           python-specfile
Version:        %{package_version}
Release: 2%{?dist}

Summary:        A library for parsing and manipulating RPM spec files
License:        MIT
URL:            https://github.com/packit/specfile

Source0:        %{pypi_source specfile %{pypi_version}}

BuildArch:      noarch

BuildRequires:  python3-devel
%if %{with tests}
# tests/unit/test_guess_packager.py
BuildRequires:  git-core
%endif


%description
%{desc}


%package -n python%{python3_pkgversion}-specfile
Summary:        %{summary}


%description -n python%{python3_pkgversion}-specfile
%{desc}


%prep
%autosetup -p1 -n specfile-%{pypi_version}

# since we are building from PyPI source, we don't need git-archive
# support in setuptools_scm
sed -i 's/setuptools_scm\[toml\]>=7/setuptools_scm[toml]/' pyproject.toml


%generate_buildrequires
%pyproject_buildrequires %{?with_tests: -x testing}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files specfile


%if %{with tests}
%check
%pytest --verbose tests/unit tests/integration
%endif


%files -n python%{python3_pkgversion}-specfile -f %{pyproject_files}
%doc README.md


%changelog
* Sat Feb 14 2026 Packit <hello@packit.dev> - 0.39.1-1
- Fixed whitespace padding of day of month in changelog entries. (#511)
- Resolves: rhbz#2393435

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jan 08 2026 Packit <hello@packit.dev> - 0.38.0-1
- A bug leading to incorrect EVR expansion has been fixed. (#492)
- Prevented side-effects during condition evaluation that could occur when expanding macros that manipulate other macros, leading to misinterpreted validity of condition branches. (#499)

* Fri Oct 03 2025 Packit <hello@packit.dev> - 0.37.1-1
- We have solved a FutureWarning in our codebase. (#485)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.37.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Sep 05 2025 Packit <hello@packit.dev> - 0.37.0-1
- Added support for Elbrus E2K CPU architectures. (#484)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.36.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.36.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 0.36.0-3
- Rebuilt for Python 3.14

* Fri May 30 2025 Packit <hello@packit.dev> - 0.36.0-1
- We have fixed a bug that caused specfile to traceback when section names with conditional macro expansions containing spaces were present in the spec file. (#476)

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.35.1-2
- Rebuilt for Python 3.14

* Fri May 16 2025 Packit <hello@packit.dev> - 0.35.1-1
- We have fixed a bug that caused changes to get lost when a spec file passed as a path was replaced or deleted. (#470)

* Sun Apr 13 2025 Packit <hello@packit.dev> - 0.35.0-1
- Added support for creating Specfile instances from file objects and strings. (#458)
- The `context_management` type stubs now use `ParamSpec` from `typing_extensions` to support Python < 3.10. (#466)

* Tue Mar 18 2025 Packit <hello@packit.dev> - 0.34.2-1
- context_management: add a type stub override to fix typing. Type checkers like mypy and pyright can now correctly determine the types for `.sources()`, `.sections()`, and the other `Specfile` methods that return context managers. (#457)

* Fri Feb 07 2025 Packit <hello@packit.dev> - 0.34.1-1
- Removed the usage of a walrus operator for Python 3.6 compatibility. (#450)

* Mon Jan 27 2025 Packit <hello@packit.dev> - 0.34.0-1
- Added support for detached (open)SUSE style changelogs (#444)
- Resolves: rhbz#2342178

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.33.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 16 2024 Packit <hello@packit.dev> - 0.33.0-1
- There is a new convenience method `Sections.get_or_create()` that allows you to manipulate a section
  without checking if it exists first. If a section doesn't exist, it will be appended to the end. (#441)
  For example, this will work properly even on spec files without `%%changelog`:

  ```
  with spec.sections() as sections:
      changelog = sections.get_or_create("changelog")
      changelog[:] = ["%%autochangelog"]
  ```
- Resolves: rhbz#2332288

* Wed Nov 13 2024 Packit <hello@packit.dev> - 0.32.6-1
- New minor release for testing in CBS Koji

* Sat Oct 26 2024 Packit <hello@packit.dev> - 0.32.5-1
- We have fixed our parser to take in account the deprecations introduced in Python 3.8 (#420)

* Fri Oct 11 2024 Packit <hello@packit.dev> - 0.32.4-1
- NEVR and NEVRA classes are now hashable (#416)

* Mon Sep 30 2024 Packit <hello@packit.dev> - 0.32.3-1
- specfile can now handle multi-line tag values (enclosed in a macro body, e.g. `%%shrink`). (#412)
- Resolves: rhbz#2299289

* Sun Sep 15 2024 Packit <hello@packit.dev> - 0.32.2-1
- Explicitly invalidate the global parse hash when a SpecParser instance is created to prevent this issue. (#409)

* Mon Jul 29 2024 Packit <hello@packit.dev> - 0.32.1-1
- Fixed two issues related to condition parsing. (#405)

* Mon Jul 22 2024 Packit <hello@packit.dev> - 0.32.0-1
- It is now possible to bump a release in a manner similar to `rpmdev-bumpspec` using `Specfile.bump_release()` method. (#399)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Packit <hello@packit.dev> - 0.31.0-1
- Value of a `Tag` no longer includes trailing whitespace (if any). (#393)
- specfile now tries to expand macros before processing conditions to be able to resolve conditional expressions defined by macros, for example OpenSUSE Tumbleweed defines `%%ifpython3` macro as `%%if "%%{python_flavor}" == "python3"`. (#394)
- Resolves: rhbz#2294393

* Wed Jun 26 2024 Packit <hello@packit.dev> - 0.30.0-1
- Fixed an exception that occured when accessing the `Specfile.has_autochangelog` property while having unparseable lines (e.g. lines ending with unescaped `%`) in `%%changelog`. (#387)

* Mon Jun 17 2024 Packit <hello@packit.dev> - 0.29.0-1
- Improved compatibility with RPM 4.20 (alpha version is currently in Fedora Rawhide). (#380)
- Resolves: rhbz#2282962

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 0.28.3-2
- Rebuilt for Python 3.13

* Thu May 23 2024 Packit <hello@packit.dev> - 0.28.3-1
- Fixed several minor issues such as processing seemingly commented-out macro definitions (e.g. `#%%global prerel rc1`) and treating `SourceLicense` tag as a source. (#374, #376)
- Made `EVR`, `NEVR` and `NEVRA` objects comparable. (#379)

* Mon Apr 08 2024 Packit <hello@packit.dev> - 0.28.2-1
- Handling of trailing newlines in the macro defintions has been improved. (#361)
- Resolves: rhbz#2271583

* Tue Mar 26 2024 Packit <hello@packit.dev> - 0.28.1-1
- We have fixed an issue in `%%prep` section processing. For instance, if the `%%patches` macro appeared there, it would have been converted to `%%patch es`, causing failure when executing `%%prep` later. (#356)

* Sun Mar 17 2024 Packit <hello@packit.dev> - 0.28.0-1
- A trailing newline is no longer added to spec files without one upon saving. (#353)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Packit <hello@packit.dev> - 0.27.0-1
- Improved handling of commented-out macro definitions and fixed related logic in `Specfile.update_value()`. (#338)

* Mon Nov 20 2023 Packit <hello@packit.dev> - 0.25.0-1
- There is a new method, `Specfile.update_version()`, that allows updating spec file version even if it is a pre-release. (#317)

* Mon Nov 06 2023 Packit <hello@packit.dev> - 0.24.0-1
- Improved type annotations for `UserList` subclasses. (#299)
- Macro definitions gained a new `commented_out` property indicating that a macro definition is commented out. Another new property, `comment_out_style`, determines if it is achieved by using a `%%dnl` (discard next line) directive (e.g. `%%dnl %%global prerelease beta2`) or by replacing the starting `%` with `#` (e.g. `#global prerelease beta2`). (#298)

* Mon Oct 30 2023 Packit <hello@packit.dev> - 0.23.0-1
- Sources now have a `valid` property that indicates whether a source is valid in the current context, meaning it is not present in a false branch of any condition. (#295)

* Fri Oct 06 2023 Packit <hello@packit.dev> - 0.22.1-1
- Removed dependency on setuptools-scm-git-archive. (#290)

* Fri Sep 01 2023 Packit <hello@packit.dev> - 0.22.0-1
- Macro definitions and tags gained a new `valid` attribute. A macro definition/tag is considered valid if it doesn't appear in a false branch of any condition appearing in the spec file. (#276)

* Fri Aug 11 2023 Nikola Forró <nforro@redhat.com> - 0.21.0-1
- `specfile` no longer tracebacks when some sources are missing and can't be _emulated_. In such case the spec file is parsed without them at the cost of `%%setup` and `%%patch` macros potentially expanding differently than with the sources present. (#271)
- Specfile's license in RPM spec file is now confirmed to be SPDX compatible. (#269)

* Mon Jul 31 2023 Packit <hello@packit.dev> - 0.20.2-1
- Fixed Packit config to work properly with `propose-downstream` and `pull-from-upstream` jobs. (#261)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Packit <hello@packit.dev> - 0.20.0-1
- Fixed infinite loop when removing macros with `%` in the name. (#244)
- Added a possibility to undefine system macros by setting a macro value to `None` in the `macros` argument of the `Specfile` constructor. (#244)
- Fixed a bug in processing options of `%%prep` macros. For instance, when a quoted string appeared inside an expression expansion, it could lead to improper parsing, rendering the spec file invalid after accessing the options. (#253)

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 0.19.0-2
- Rebuilt for Python 3.12

* Thu Jun 22 2023 Packit <hello@packit.dev> - 0.19.0-1
- Parsing has been optimized so that even spec files with hundreds of thousands of lines can be processed in reasonable time. (#240)

* Fri May 26 2023 Packit <hello@packit.dev> - 0.18.0-1
- Specfile library now handles multiple `%%changelog` sections. (#230)

* Thu May 11 2023 Packit <hello@packit.dev> - 0.17.0-1
- Added a new `guess_packager()` function that uses similar heuristics as `rpmdev-packager`, meaning that the `Specfile.add_changelog_entry()` method no longer requires `rpmdev-packager` to guess the changelog entry author. (#220)
- The `Specfile.add_changelog_entry()` method now uses dates based on UTC instead of the local timezone. (#223)

* Thu Apr 20 2023 Packit <hello@packit.dev> - 0.16.0-1
- Added `Specfile.has_autorelease` property to detect if a spec file uses the `%%autorelease` macro. (#221)

* Fri Mar 10 2023 Packit <hello@packit.dev> - 0.15.0-1
- Parsing the spec file by RPM is now performed only if really necessary, greatly improving performance in certain scenarios. (#212)
- Checked that license is a valid SPDX license.

* Thu Feb 23 2023 Packit <hello@packit.dev> - 0.14.0-1
- Fixed a bug that broke parsing in case spec file contained conditionalized macro definitions or similar constructs. (#209)
- Specfile no longer depends on rpm-py-installer, it now depends directly on rpm. (#207)

* Mon Jan 30 2023 Packit <hello@packit.dev> - 0.13.2-1
- Fixed infinite loop that occured when section options were followed by whitespace. (#197)

* Mon Jan 23 2023 Packit <hello@packit.dev> - 0.13.1-1
- Fixed a bug in section parsing that caused sections to be ignored when there were macro definitions spread across the spec file and not cumulated at the top. (#191)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 20 2023 Packit <hello@packit.dev> - 0.13.0-1
- Added `Section.options` attribute for convenient manipulation of section options. (#183)
- specfile now supports single-line sections where section content is represented by a macro starting with a newline. (#182)
- Added `evr` argument to `Specfile.add_changelog_entry()`. This allows adding a changelog entry with an EVR value that's different from the current specfile's value. This makes it easier to reconstruct a specfile's `%changelog` based on another source using the higher level interface. (#181)

* Fri Jan 06 2023 Packit <hello@packit.dev> - 0.12.0-1
- All classes including `Specfile` itself can now be copied using the standard `copy()` and `deepcopy()` functions from `copy` module. (#176)
- `Section.name` attribute has been renamed to a more fitting `Section.id`. (#167)
- `setup.cfg` now uses `license_files` instead of deprecated `license_file`. (#162)

* Wed Dec 14 2022 Packit <hello@packit.dev> - 0.11.1-1
- Tags enclosed in conditional macro expansions are not ignored anymore. (#156)
- Fixed context managers being shared between Specfile instances. (#157)

* Fri Dec 09 2022 Packit <hello@packit.dev> - 0.11.0-1
- Context managers (`Specfile.sections()`, `Specfile.tags()` etc.) can now be nested and combined together (with one exception - `Specfile.macro_definitions()`), and it is also possible to use tag properties (e.g. `Specfile.version`, `Specfile.license`) inside them. It is also possible to access the data directly, avoiding the `with` statement, by using the `content` property (e.g. `Specfile.tags().content`), but be aware that no modifications done to such data will be preserved. You must use `with` to make changes. (#153)

* Wed Nov 30 2022 Packit <hello@packit.dev> - 0.10.0-1
- Fixed an issue that caused empty lines originally inside changelog entries to appear at the end. (#140)
- Renamed the `ignore_missing_includes` option to a more general `force_parse`. If specified, it allows to attempt to parse the spec file even if one or more sources required to be present at parsing time are not available. Such sources include sources referenced from shell expansions in tag values and sources included using the `%include` directive. (#137)

* Sat Nov 12 2022 Packit <hello@packit.dev> - 0.9.1-1
- `specfile` now supports localized tags (e.g. `Summary(fr)`) and tags with qualifiers (e.g. `Requires(post)`).
  It also follows more closely rpm parsing logic and doesn't fail on invalid section names. (#132)

* Tue Oct 25 2022 Packit <hello@packit.dev> - 0.9.0-1
- Added utility classes for working with (N)EVR. (#113)
- Fixed an issue with multiple instances of `Specfile` not expanding macros in the right context. (#117)

* Fri Oct 14 2022 Packit <hello@packit.dev> - 0.8.0-1
- Added `Specfile.update_tag()` method that allows updating tag values while trying to preserve macro expansions. You can watch a demo on [YouTube](https://youtu.be/yzMfBPdFXZY). (#101)

* Fri Oct 07 2022 Packit <hello@packit.dev> - 0.7.0-1
- It is now possible to filter changelog entries by specifying lower bound EVR, upper bound EVR or both. (#104)
- Added support for filenames specified in source URL fragments, for example: `https://example.com/foo/1.0/download.cgi#/%{name}-%{version}.tar.gz` (#100)

* Thu Aug 25 2022 Packit <hello@packit.dev> - 0.6.0-1
- Switched to our own implementation of working with `%changelog` timestamps and removed dependency on arrow (#88)
- Fixed requires of EPEL 8 rpm (#86)

* Wed Aug 10 2022 Packit <hello@packit.dev> - 0.5.1-1
- Added new `%conf` section (#74)
- Switched to rpm-py-installer (#75)
- Fixed detecting extended timestamp format in `%changelog` (#77, #81)

* Fri Jul 22 2022 Packit <hello@packit.dev> - 0.5.0-1
- Strict optional typing is now enforced (#68)
- Fixed deduplication of tag names (#69)
- Sources and patches can now be removed by number (#69)
- Number of digits in a source number is now expressed the same way as packit does it (#69)
- Empty lines are now compressed when deleting tags (#69)
- Added convenience property for getting texts of tag comments (#69)
- Added convenience method for adding a patch (#69)

* Tue Jun 21 2022 Packit <hello@packit.dev> - 0.4.0-1
- Added convenience properties for most used tags (#63)
- Hardened linting by ignoring only specific mypy errors (#64)
- Fixed list of valid tag names and ensured newly added tags are not part of a condition block (#66)
- Initial patch number and its default number of digits are now honored (#66)
- Fixed a bug in `%prep` macro stringification (#67)

* Mon Jun 20 2022 Python Maint <python-maint@redhat.com> - 0.3.0-2
- Rebuilt for Python 3.11

* Mon May 16 2022 Packit <hello@packit.dev> - 0.3.0-1
- Made `Sources` a `MutableSequence` (#36)
- Started using consistent terminology for source numbers and added the option to insert a source with a specific number (#47)
- Added support for implicit source numbering (#48)
- Documented sources and `%prep` macros in README (#49)
- Implemented high-level manipulation of version and release (#54)
- Added support for `* Mon May 16 2022 John Doe <packager@example.com> - 0.3.0-1.fc35
- local build` (#56)
- Added `remote` property to sources and enabled addition of `Sources` (#59)
- Implemented mid-level manipulation of `%prep` section, including modification of `%prep` macros (#37, #52)


* Thu Mar 31 2022 Packit <hello@packit.dev> - 0.2.0-1
- Enabled Zuul CI (#8)
- Switched from git:// to https:// for rebase hook (#22)
- Updated pre-commit configuration and adapted to type changes brought by new version of mypy (#24)
- Non-lowercase section names are now supported (#26)
- Added `Sections.get()` convenience method (#29)
- Added packit configuration and enabled packit (#25)
- Fixed infinite recursion when deep-copying instances of `Sections` and `Tags` (#30)
- Updated Fedora and EPEL spec files (#32)
- Fixed issues caused by older versions of dependencies on EPEL 8 (#33)
- Implemented high-level manipulation of sources and patches (#20, #36)
- It is now possible to parse spec files with missing local sources (#23)

* Mon Feb 21 2022 Nikola Forró <nforro@redhat.com> - 0.1.1-1
- New upstream release 0.1.1

* Tue Feb 08 2022 Nikola Forró <nforro@redhat.com> - 0.1.0-1
- Initial package
