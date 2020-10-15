Building Packages
===
## Prev: [Local Packages](2_local_packages.md), Next: [Image Generation](4_image_generation.md)
## Initial Dependency Information
Once the intermediate SPEC files are extracted (see [Creating SPECS](#2_local_packages.md#creating_specs)) the dependency information from them needs to be extracted. The `specreader` tool scans each SPEC file in the intermediate SPECs folder and uses `rpmspec -q` to list the dependencies for each package found in the SPEC file.

Each SPEC file will have one base package, and may have additional virtual packages. Each of these packages is recorded as a `Provides` entry, along with a version and release if set.

All packages from a SPEC file share the same build requirements (as builds occur at the granularity of a SPEC file), but may have different run-time requirements. For each package a list of `BuildRequires` enumerates all the packages which much be available before building the current package. A `Requires` list similarly enumerates all the packages which must be available to install the package.

For example, a very simple SPEC may be parsed to give:
```json
{
    "Provides": {
        "Name": "example",
        "Version": "1.0.0-1.cm1",
        "Condition": "=",
        "SVersion": "",
        "SCondition": ""
    },
    "SrpmPath": "build/INTERMEDIATE_SRPMS/x86_64/example-1.0.0-1.cm1.src.rpm",
    "SourceDir": "build/INTERMEDIATE_SPECS/example-1.0.0-1.cm1",
    "SpecPath": "build/INTERMEDIATE_SPECS/example-1.0.0-1.cm1/example.spec",
    "Architecture": "x86_64",
    "Requires": [
        {
            "Name": "nano",
            "Version": "",
            "Condition": "",
            "SVersion": "",
            "SCondition": ""
        }
    ],
    "BuildRequires": null
},
{
    "Provides": {
        "Name": "example-devel",
        "Version": "1.0.0-1.cm1",
        "Condition": "=",
        "SVersion": "",
        "SCondition": ""
    },
    "SrpmPath": "build/INTERMEDIATE_SRPMS/x86_64/example-1.0.0-1.cm1.src.rpm",
    "SourceDir": "build/INTERMEDIATE_SPECS/example-1.0.0-1.cm1",
    "SpecPath": "build/INTERMEDIATE_SPECS/example-1.0.0-1.cm1/example.spec",
    "Architecture": "x86_64",
    "Requires": null,
    "BuildRequires": null
}
```
The single SPEC provides the base package `example`, but also provides a virtual package `example-devel`. Both packages share the same input files and build requirements, and will be produced as a single atomic operation.

All package dependency information is written to `./../build/pkg_artifacts/specs.json`.

### Or Clauses
Spec files can have `(a or b)` style requirements. When the build system encounters such a requirement it will record both options into the graph so that all possible requirements will be made available to pick from during package install allowing for maximum flexibility. This means that the build system requires all optional RPMs to be available to build/download even if they will not be used for a specific configuration.

#### Warning:
The build system will print a warning (`'OR' clause found (...), please refer to 'docs/how_it_works/3_package_building.md#or-clauses' for explanation of limitations.`) when it encounters an `or` clause. If be build fails make sure all conditional packages are available locally/online, or remove the unavailable conditional packages from the SPEC file.

## Dependency Graphing

A critical component of package building is ensuring that the packages are built in such a way that:
1) no package build is started before its build dependencies are available
2) no package is used as a dependency before its run-time requirements are satisfied

### Types of Nodes
The graph contains several types of nodes, with various states. As the graph is processed by each tool nodes are updated, pruned, or added as needed.
#### TypeBuild
> This represents a local package which may be passed to the build worker to generate an RPM from.
> It can be either:
>
> `StateBuild`: Should be built
> 
> `StateUpToDate`: Package is already available locally

#### TypeRun
> This node represents a package which is may be installed or used as a dependency.
> Run nodes are always:
>
> `StateMeta`: Organizational node used to impose ordering on other nodes

#### TypeGoal
> Special node which is used to group packages together. If the goal node is satisfied then all the packages which are part of the goal are available to install.
> Goal nodes are always:
>
> `StateMeta`: Organizational node used to impose ordering on other nodes

#### TypeRemote
> This node represents a package which is unknown to the local build system, but has been requested as a dependency. It will need to be resolved from a remote source. `TypeRemote` nodes are considered equivalent to `TypeRun` nodes in most cases.
> Remote nodes may be either:
>
> `StateUnresolved`: No known source has been found yet
>
> `StateCached`: A remote source was found and the package should now be available locally.

#### TypePureMeta
> This is a purely organizational node with no special meaning. Used to do things like resolve intra-package cycles which would normally break the dependency graph.
> PureMeta nodes are always:
>
> `StateMeta`: Organizational node used to impose ordering on other nodes

### File Format
The graphs are exported as `graphviz` `dot` formatted files. These files are exported in such a way as to offer enough human readable information to help debugging.

The files can be ingested into the `graphviz` tools to visualize them, although the graphs of a large build are often impractically large.
```bash
# Visualize the file 'graph.dot' using the basic dot tool
dot -Tpng -o visualized.png < graph.dot
```

### Stage 1: Grapher

The `grapher` tool reads the `specs.json` file and converts it into an acyclic directed graph. Inter-package dependencies are represented by directed edges in the graph.

The `grapher` tool outputs `./../build/pkg_artifacts/graph.dot`

#### Graph Generation

Each `provides` entry in `specs.json` is converted to two vertices in the graph, a `build` node and a `run` node. Each node represents exactly one package (with specific version if available). Two packages cannot both provide a node with the same name and version (same name with different versions is fine).

Edges in the graph represent dependencies. A package cannot be installed (`run`) until it has been compiled (`build`). An edge is automatically added from the `run` node to the `build` node of each package to represent this dependency.

Once all packages have been added to the graph, the inter-package dependencies are added. For each `BuildRequires` in a package an edge is created from the current `build` node to the `run` node associated with the required package. The same is done for each `Requires`, but from the current `run` node instead of the `build` node.

#### Package Lookup
A critical part of adding edges is finding the correct node to connect to. Package dependencies can specify their requirements with varying levels of detail. The most basic dependency is just a package name. The dependency can be further refined by setting a limit on the version (`Requires: example >= 1.0.0`), or double conditionals (`Requires: example >= 1.0.0`, `Requires: example < 2.0.0 `). A dependency can also require a specific version (`Requires: example = 1.0.0`)

The `grapher` program will try to find the best matching package it knows about to satisfy dependencies. To assist with this a set of sorted lookup lists are maintained for each package, storing every version encountered so far. The highest version package which satisfies the requirements is selected. If no node in the lookup list satisfies the version requirements an unresolved node is added to the graph.

##### Version Compare
Versions are split into two components: the version and the release number. Generally packages do not specify a specific release number in their requirements, so the release is not considered unless both versions under comparison explicitly contain one.

Versions are stored internally as intervals with maximum and minimum supported versions (versions must be a single range, ex. `ver < 3, ver > 4` is not supported). Each interval records an upper and lower bound. Those bounds may be inclusive or exclusive depending on the version comparison operator (`<, <=, =, >=, >`)

#### Cycle Resolving
In general cycles in the dependency graph are considered an unrecoverable error, but there are special cases where they can be fixed. Some packages create cycles with their own virtual packages which are not an issue. Since all the packages from a given SPEC file build at the same time the fact they rely on each other is not a problem.

To solve this a `TypePureMeta` node is inserted which consolidates all the dependencies of the cycle nodes into a single node. The nodes in the cycle are then disconnected from each other and instead depend on the new meta node. This only works if all the nodes in the cycle are from the same SPEC file, and the dependencies are all run-time dependencies.

In the example below nodes `A-a` and `A-b` are from the same spec file and require each other. Since they are part of the same package this cycle can be fixed. A meta node (`ID=8`) is added which consolidates all the requirements. Notice that `A-a` required `B`, while `A-b` required `C`. Now the meta node requires both `B` and `C` and the two `A` packages require the meta node instead.

![Cycle Before](images/cycle_before.png)
![Cycle Before](images/cycle_after.png)

#### Default Goal Node
The `grapher` tool automatically adds an "ALL" goal node to the graph which links to every node. Building this node will case every known package to be built.

### Stage 2: Graphoptimizer
The `grapher` tool makes no attempt to avoid rebuilds of up-to-date or unneeded packages. The `graphoptimizer` tool takes a pair of arguments which are used to narrow the focus of the build: `--packages` and `--image-config-file`.

The `graphoptimizer` tool outputs `./../build/pkg_artifacts/scrubbed_graph.dot`

##### `--packages`
This is a space separated list of package names which should be built. The build system will make sure these packages, and all runtime dependencies for them, are built. Normally blank, this can be set via the `Make` argument `PACKAGE_BUILD_LIST=` at build time.

##### `--image-config-file`
The `graphoptimizer` tool will parse the currently selected config file to determine what packages are needed to compose the image. It will only build the subset of packages needed for the image. This is set with `CONFIG_FILE=` at build time.

#### Trimming
Depending on which packages have been selected for building only some parts of the full graph are needed. The `graphoptimizer` tool adds a `TypeGoal` node to the graph which depends on all the high level packages it has been asked to make available. It then creates a sub-graph rooted at that goal node and continues processing the sub-graph.

#### Marking as Up-To-Date
A node which is `TypeBuild`/`StateBuild` will be marked as `StateUpToDate` if `graphoptimizer` is able to find all the expected output packages with the correct version numbers. `Graphoptimizer` WILL NOT trigger rebuilds due to changes in the timestamps of SPEC files and packages. If a package must be rebuilt its base package name (name of SPEC file) should be passed via the variable `PACKAGE_REBUILD_LIST=`. This will cause `graphoptimizer` to never mark the packages as up-to-date.

`Graphoptimizer` is also able to detect changes in dependencies which should trigger a rebuild of other packages. For example if package `A` depends on package `B`, and package `B` is rebuilt, then package `A` will also be marked for rebuild.

Sometimes packages fail to build correctly, or are otherwise not suitable for building in the build system. `Graphoptimizer` would normally complain that they are missing, possibly causing undesired rebuilds. The `PACKAGE_IGNORE_LIST=` variable can be used to set the `--ignore-packages` argument which instructs `graphoptimizer` to never worry about the listed packages (again using the package base name).

### Stage 3: Graphpkgfetcher
The `graphpkgfetcher` tool's job is to resolve unresolved remote nodes. Unresolved nodes occur when a local package has `Requires` or `BuildRequires` which are not available from another local package.

The tool uses the `worker_chroot` (see [Chroot Worker](1_initial_prep.md#chroot_worker)) to locate packages. The worker will search in six locations: 1) the local chroot environment, 2) already build RPMs in `./../out/RPMS/`, 3) the upstream base repository 4) the upstream update repository if `$(USE_UPDATE_REPO)` is set to `y` 5) the upstream preview repository if `$(USE_PREVIEW_REPO)` is set to `y` 6) any remote repo listed in `REPO_LIST ?=`. If `$(DISABLE_UPSTREAM_REPOS)` is set to `y`, any repo that is accessed through the network is disabled.

The worker will run the `tdnf` command to search for each missing package. `tdnf` will prioritize local packages over pulling them from a remote location.

The worker is able to access the local packages through a mounted overlay in the chroot environment, and output newly cached RPMs through another writable mount. For `tdnf` to read the local packages the folder must be converted into a repository, but since it is mounted as an overlay the changes are not persisted out of the chroot.

Once the packages are cached they are copied into `./../out/RPMs` for use in further stages of the build and any satisfied nodes are marked as `StateCached`.

The `graphpkgfetcher` tool outputs `./../build/pkg_artifacts/cached_graph.dot`

### Stage 4: Unravel
The `unravel` tool's job is to convert the dependency graph into something which can be consumed by a build system to successfully build the requested packages.

`Unravel` implements a modular setup which can output different formats. The most basic format is a simple topologically sorted list of packages which can be build sequentially. Only `TypeBuild` nodes need to be printed as all other node types are simply to enforce ordering in the grpah.

The more useful system, and what is used in further steps by the build system, is a recursive `Makefile`. Since the build system is already using `Make` it is reasonably straight forward to make recursive calls into `Make`, and use its own build ordering algorithms.

The `unravel` tool outputs `./../build/pkg_artifacts/workplan.mk`

#### Workplan Makefile
`Unravel` creates a workplan which encodes both the ordering information and the build instructions for each package to be built. It creates a `.PHONY` target and recipe for every node in the graph. Many of these recipes are empty (i.e. `GOAL_PackagesToBuild: ;`), but any `TypeBuild` node with `StateBuild` will be given an actual build command invoking the `pkgworker` tool. The dependencies between nodes are encoded as dependencies between targets.

A very simple workplan might look like:
```makefile
.PHONY: GOAL_PackagesToBuild
GOAL_PackagesToBuild: ;
GOAL_PackagesToBuild:  RUN_0_./../build/INTERMEDIATE_SRPMS/x86_64/example-1.0.0-1.cm1.src.rpm_example

.PHONY: RUN_0_./../build/INTERMEDIATE_SRPMS/x86_64/example-1.0.0-1.cm1.src.rpm_example
RUN_0_/home/damcilva/repos/demo/build/INTERMEDIATE_SRPMS/x86_64/example-1.0.0-1.cm1.src.rpm_example: ;
RUN_0_/home/damcilva/repos/demo/build/INTERMEDIATE_SRPMS/x86_64/example-1.0.0-1.cm1.src.rpm_example:  BUILD_./../build/INTERMEDIATE_SRPMS/x86_64/example-1.0.0-1.cm1.src.rpm

.PHONY: BUILD_./../build/INTERMEDIATE_SRPMS/x86_64/example-1.0.0-1.cm1.src.rpm
BUILD_./../build/INTERMEDIATE_SRPMS/x86_64/example-1.0.0-1.cm1.src.rpm:
	MAKEFLAGS= $(go-pkgworker) --input=./../build/INTERMEDIATE_SRPMS/x86_64/example-1.0.0-1.cm1.src.rpm --work-dir=$(CHROOT_DIR) ... >> $(LOGS_DIR)/pkggen/failures.txt 
```

The entry point is `GOAL_PackagesToBuild`, which depends on the run node for the desired package (since run nodes indicate a package can be installed). Each run node will list its dependencies.

In this case the example package has no other dependencies, so it only depends on its own build node. That build node invokes the `pkgworker` tool to actually build the `*.rpm` file.

### Stage 5: Pkgworker
The `pkgworker` tool is not invoked directly by the build system, instead it is invoked from a recursive `Make` call to the dynamically generated `workplan.mk` file.

`Pkgworker` uses the `worker_chroot` (see [Chroot Worker](1_initial_prep.md#chroot_worker)) environment to build each package independently. First it creates an empty folder to build in (one for each package to build) and extracts the chroot archive into it. This preps the environment with all the toolchain packages which were made available during the prep stage (see [Toolchain](1_initial_prep.md#toolchain)). It then mounts the local RPM folder into the environment so the worker can access any build dependencies it has. Using `tdnf` and `rpmbuild` the worker installs the build dependencies from the local packages, then builds the require package. Once the build is complete the freshly build pacakge is placed into the `./../out/RPMS/` folder to be available to future workers.

Because the dependency information has been encoded in `workplan.mk` it is possible to build multiple pacakges in parallel. `Make` will guarantee that no package is built before its `BuildRequires` are all satisfied as encoded in the graph.

## Prev: [Initial Prep](2_local_packages.md), Next: [Image Generation](4_image_generation.md)