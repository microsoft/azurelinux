Prepping the Build Environment
===
## Prev: [Intro](0_intro.md), Next: [Local Packages](2_local_packages.md)

- [The Makefile](#The-Makefile)
- [Toolchain](#Toolchain)
- [Chroot Worker](#Chroot-Worker)
- [Go Tools](#Go-Tools)
    - [Building Go Tools](#building-go-tools)
    - [Testing Go Tools](#testing-go-tools)
    - [Go Tools](#go-tools)
        - [boilerplate](#boilerplate)
        - [depsearch](#depsearch)
        - [grapher](#grapher)
        - [graphanalytics](#graphanalytics)
        - [graphpkgfetcher](#graphpkgfetcher)
        - [imageconfigvalidator](#imageconfigvalidator)
        - [imagepkgfetcher](#imagepkgfetcher)
        - [imager](#imager)
        - [isomaker](#isomaker)
        - [liveinstaller](#liveinstaller)
        - [pkgworker](#pkgworker)
        - [roast](#roast)
        - [specreader](#specreader)
        - [srpmpacker](#srpmpacker)
        - [scheduler](#scheduler)
        - [validatechroot](#validatechroot)

## The Makefile

The build system is based on `Make`. `Make` is a build tool most commonly used for compiling code, but can also be useful for more general build systems with hierarchical dependencies. In the case of this build system it is used to track changes in the various package, configuration, and input files.

At a high level `Make` will rebuild a file (target) if any of its dependencies are updated, as determined by modification time of the target and its dependencies. This implies that `Make` works best with individual, specific files on disk. There are several areas in the build system where this does not apply cleanly which are discussed in [Makefile Advanced Components](5_misc.md#makefile-advanced-components).

The make scripts are split into `*.mk` files under `./scripts` split by purpose.

A list of targets is given in [All Build Targets](../building/building.md#all-build-targets).

## Toolchain
To guarantee reliable, reproducible builds all packages are built using the same tools which are published as RPMs. The toolchain RPMs are used to create a `chroot` environment on the build machine which mimics the final OS environment. Normally these RPMs are simply downloaded from a remote server. If a local only build is desired the `REBUILD_TOOLCHAIN=y` variable can be used. If the `TOOLCHAIN_ARCHIVE=toolchain.tar.gz` variable is also set the toolchain packages are extracted from an archive.

If the `TOOLCHAIN_ARCHIVE` variable is not set, but `REBUILD_TOOLCHAIN=y` is, then a full local bootstrap will be performed. This uses the host system's tools to build intermediate copies of the toolchain packages inside a Docker container. These intermediate RPMs are then used to build clean copies of the final RPMs. (Refer to [Building Everything From Scratch](../building/building.md#building-everything-from-scratch))

## Chroot Worker
The chroot worker is an archive containing all the toolchain RPMs installed into a chroot environment. This archive can be extracted into a folder, then a chroot call can be made to switch into the environment. Once in the chroot environment only the RPM based tools and filesystem are available. This creates a clean build environment.

The chroot worker is used at several points to perform various tasks using the RPM packaged tools without interfering with the host system. The three major ones are:
1) Processing spec files using Mariner's RPM macros.
2) Using `tdnf` to download packages.
3) Building new packages using only the RPM based compilers/tools etc.

The build system creates the archive based on the RPMs created/downloaded by the toolchain targets. If any of these RPMs are changed the archive will be re-built.

See [Chroot](5_misc.md#chroot) for more details on the underlying chroot mechanism.

## Go Tools
The go tools can be re-built with the command `make go-tools REBUILD_TOOLS=y`. Each tool has a `--help` argument which lists details about the tool's arguments.

### Building Go Tools
See [Go Tools Compiling](5_misc.md#Go-Tools-Compiling) for an in depth discussion of how the go tools are built using the `makefiles`.

### Testing Go Tools
While all the tools will automatically run self tests, the target `go-test-coverage` can be used to manually run all self tests and export a html based test coverage report to `./../out/tools/test_coverage_report.html`.

### Go Tools
Below are the executable tools used as part of the build system.

#### boilerplate
The `boilerplate` tool is a sample go tool which shows a minimal implementation of the argument parsing and logging packages.

#### bldtracker
The `bldtracker` tool is used to initialize a JSONL file or record a new timestamp for shell scripts during the image-building process.

#### depsearch
The `depsearch` tool is used to list all packages which depend on another set of packages. The tool operates on dependency graphs (see [Dependency Graphing](3_package_building.md#dependency-graphing)) produced by the workplan creation system. Passing `--input=../build/pkg_artifacts/graph.dot --packges="pkg1 pkg2" --specs=./path/to/others.spec` will return a list of all packages which depend on the pkg1.rpm, pkg2.rpm, other*.rpm packages.

#### grapher
The `grapher` tool is responsible for creating the initial dependency graph from the parsed spec files (see [Dependency Graphing](3_package_building.md#dependency-graphing)). It outputs a graph based on all local packages and their dependencies. It makes no attempt to optimize the graph or find unresolved dependencies.
#### graphanalytics
`graphanalytics` is an optional tool that analyzes the built graph from `scheduler` and generates a summary with information regarding any packages that are blocked from building. The summary includes the packages that are most blocking other packages from building and the packages closest to being ready to build.
#### graphpkgfetcher
The `graphpkgfetcher` tool takes the output from the `grapher` tool and attempts to resolve any unresolved nodes (see [Stage 2: Graphpkgfetcher](3_package_building.md#stage-2-graphpkgfetcher)). It does this by looking for packages in the locally build environment, or failing that downloading them from a set of remote package servers.
#### imageconfigvalidator
The `imageconfigvalidator` tool checks if the selected configuration file is valid.
#### imagepkgfetcher
The `imagepkgfetcher` tool is similar to the `graphpkgfetcher` tool. It will find all the packages needed to compose an image, either from locally built and cached RPMs, or download them from the package servers.
#### imager
The `imager` tool is responsible for composing an image based on the selected configuration file. It creates partitions, installs packages, configures the users, etc. It can output either a `*.raw` file or a simple filesystem.
#### isomaker
The `isomaker` tool creates an installable ISO which can be booted from a CD or other device. The ISO contains the `initrd` used to boot from a read-only device, and all the packages needed to create a copy of the selected configuration on a new computer.
#### liveinstaller
The `liveinstaller` tool is included in the ISO `initrd` and is responsible for installing the requested image onto a new computer.
#### pkgworker
The `pkgworker` tool is responsible for creating a single chroot environment and building a package inside it (see [Stage 5: Pkgworker](3_package_building.md#stage-5-pkgworker)). The `pkgworker` tool will attempt to safely clean up the created chroot environment in the event of an error.
#### roast
The `roast` tool bakes raw images created by `imager` into the requested final artifact format.
#### specreader
The `specreader` tool scans all the `*.spec` files in a directory and generates a `*.json` files summarizing all the dependency information found in them. This output can be passed to the `grapher` tool to generate a graph. This tool runs using the [chroot worker](#Chroot-Worker) to support macros.
#### srpmpacker
The `srpmpacker` tool creates `.src.rpm` files from local specs and sources. The sources can be present locally, or downloaded from a source server. It is responsible for enforcing a matching hash for every source file. This tool runs using the [chroot worker](#Chroot-Worker) to support macros.
#### scheduler
The `scheduler` tool takes the output from the `grapher` tool and schedules builds for each local spec file using [pkgworker](###pkgworker) (see [Stage 3: Scheduler](3_package_building.md#stage-3-scheduler)). `scheduler` will skip building any spec if it and all of its dependencies have already been built. The `scheduler` tool bases its decisions on the currently selected image configuration.
#### validatechroot
A tool which double checks the worker chroot has all its dependencies correctly installed.

## Prev: [Intro](0_intro.md), Next: [Local Packages](2_local_packages.md)
