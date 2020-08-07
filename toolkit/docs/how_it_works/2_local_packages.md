Local Packages
===
## Prev: [Initial Prep](1_initial_prep.md), Next: [Package Building](3_package_building.md)
## SPEC Files

A CBL-Mariner repository normally consists of a SPECS folder (specified with `$(SPEC_DIR)`), a set of image configurations (`$(CONFIG_FILE)`), and this toolkit. The SPECS folder is a root directory containing subdirectories for each local package which will be available to a build. The subdirectories avoid name collisions between sources files.

Each SPEC file is accompanied by a `*.signature.json` file which records the expected hashes for every source file used in the package.

## Creating SRPMs
The build system operates on `*.src.rpm` files, or SRPMs. SRPMs include both the SPEC file which defines the package, and all associated source files used to build the binary package. These sources could include archives of source code, patches, configuration files, etc.

The build system monitors `$(SPEC_DIR)` for changes to SPEC files or sources and builds all the dependent files if they are changed.
> Note: The graph optimizer step will skip rebuilding a package if it thinks it is up-to-date, see [Working on Packages](../building/building.md#working-on-packages) for tips on iterating on a single package.

The intermediate SRPMs can be built using the `input-srpms` target.

### SRPM Packing
The `srpmpacker` tool's job is to convert SPEC files into SRPMs. To do this it parses the SPEC files, determines which source files it needs, checks for matching files locally, and failing that searches the online source server for them. `srpmpacker` will only accept a source file if it matches the hash recorded in the associated `*.signature.json` file.

#### File Hashes
Each source file should have a matching entry in the `*.signature.json` file for its SPEC file. If a source file's hash does not match the entry in the file the build system will attempt to find a matching file from the source server. If that fails `srpmpacker` will return a `404` error.

The behavior of the hash checking code is controlled with `$(SRPM_FILE_SIGNATURE_HANDLING)`. The options are `enforce`, `skip`, `update`. The build system defaults to `enforce`.
##### `enforce`
Only package source files which match the listed hash. Attempt to find missing files from the online package server if needed.
##### `skip`
Make no attempt to validate the source file hashes. Find any file with a matching name.
##### `update`
If a local source file is included in the SPEC file add its hash to the `*.signature.json`

### Intermediate SRPMs
Once `srpmpacker` has determined a given SPEC file must be re-packaged into an SRPM it calls `rpmbuild -sb` on the SPEC file. This will generate an SRPM in `./../build/INTERMEDIATE_SRPMS/`.

## Creating SPECS
Having SPEC files available is useful for calculating dependency information, so a canonical copy of the SPEC files as stored in the SRPMs are extracted and placed into `./../build/INTERMEDIATE_SPECS/`.

The intermediate SPECs can be extracted with the `expand-specs` target.

## Prev: [Initial Prep](1_initial_prep.md), Next: [Package Building](3_package_building.md)