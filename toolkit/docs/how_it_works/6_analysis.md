Build Analysis
===
## Prev: [Miscellaneous Topics](5_misc.md)
- [Built packages list](#Built-packages-list)
  - [Generating a "fake" list](#Fake-list)
- [sodiff](#sodiff)
  - [Implementation](#Implementation)
  - [Artifacts](#Artifacts)

## Built packages list
A `built-packages-summary` target checks the build logs and creates a file with a list of packages that have been built locally (which might be different from a list of packages present, e.g. downloaded toolchain packages). The file is used later for sodiff analysis.

### Fake list
If no packages has been built, a target `fake-built-packages-list` can be run to generate a list as if all the packages in the rpm output folder were built locally.

## sodiff
sodiff is a process which looks for new versions of `.so` files and provides a list of packages that need to be rebuilt due to the change.

To provide a list of packages that need to be rebuilt, simply run `sodiff-check` target. The target will fail if no packages has been built. In that case, one can run `fake-built-packages-list` target before making a sodiff check. This will allow to analyze all RPMs except just the locally built ones.

### Implementation
 - sodiff uses RPM repositories to obtain package information. The RPM repositories included by default come from the base Mariner .repo files. They are concatenated and packaged during toolkit generation.
 - Optional .repo files can be passed added by specifying them with `SODIFF_OPTIONAL_SOURCES` variable. The location of .repo files is relative to the `$(SPECS_DIR)/mariner-repos/` directory.

### Artifacts
The artifacts are available in the `$(SODIFF_OUTPUT_FOLDER)`, which is `build/sodiff` by default.
The results of sodiff check are:
    - `summary.txt` file, containing a list of source rpm names (without the extension part) of packages that need to be rebuilt due to `.so` version change,
    - `sodiff.log` file, updated throughout the build with names of packages that are currently processed (use `tail -f` to track progress of the check).
    - Files following a naming format: `require_$SOFILE`, where `$SOFILE` is a full name of a `.so` file with updated version. It contains a list of packages that depend on that file.

## Prev: [Miscellaneous Topics](5_misc.md)
