Miscellaneous Topics
===
## Prev: [Image Generation](4_image_generation.md), Next: [Common Error Logs](6_logs.md)
- [Chroot](#chroot)
- [Makefile Advanced Components](#makefile-advanced-components)
    - [Config Tracking](#Config-Tracking)
    - [Folder Dependencies](#Folder-Dependencies)
    - [Go Tools Compiling](#Go-Tools-Compiling)
    - [Disabling shell commands during dry-run](#Disabling-shell-commands-during-dry-run)
- [Distroless Images](#distroless-images)

## Chroot
The change root (`chroot`) operation in linux instructs the kernel to enter a folder, and reset the root folder (`/`) to the current location.

This has the effect of completely swapping the local environment to a new one, rooted in the selected folder. The build system uses `chroot` to isolate the build process from the host tools and filesystem.

Initially a `chroot` environment is completely empty with no tools, to be useful the folder must be seeded with utilities and a filesystem prior to the `chroot` call. The `chroot_worker` (see [Chroot Worker](1_initial_prep.md#chroot_worker)) is an archive of all the critical components needed to perform basic operations inside the `chroot`. The primary requirement for the build system is to run `tdnf` to acquire additional packages. Once `tdnf` is available any other required packages can be installed normally.

Configuring the `chroot` initially (before `tdnf` can run) requires installing the packages from outside the environment. The `rpm` tool can be used to install packages into a different root using the `-i` and `--root` arguments. Ideally the number of packages installed this way is minimized since the process is different than would be found on a normal system.

### Mounting
Unfortunately some operations which need to be performed inside the `chroot` require access to important system resources like `/dev/`, `/proc`, `/sys`, etc. These must be mounted into the `chroot` environment prior to switching. It is critical to monitor the state of these mounts, and unmount them prior to cleaning up the chroot folder. Failure to unmount these directories can result in the host system operating abnormally. While the build system attempts to ensure no mount point is deleted prior to being unmounted it is possible to manually delete the folders.

If you see `bash: /dev/null: Permission denied` it is a strong indication an unmount failed, and the error was not caught before the folder was cleared. **A reboot of the host machine should fix this issue**.

### Safechroot
The go tools utilize the `safechroot` package to handle working with chroots. This wraps the various chroot operations in go code and should safely clean up after itself even in the event of an error.

## Makefile Advanced Components

In many cases targets have dependencies on entire folder trees, or on the contents of configuration variables. `Make` does not directly support those types of dependencies, so a few advanced patterns are used.

### Config Tracking

Configuration flags which change the behavior of the build may need to be tracked as dependencies, indicating a component needs to be rebuilt (such as `PACKAGE_BUILD_LIST` and the package build workplan).

In `utils.mk` there is a "Variable Dependency Tracking" section which fulfils this purpose. A list of variables to track is stored in `$(watch_vars)`, a set of `$(exec ...` calls is used to create dynamic makefile targets based on that list.

The idea is to store the last value of each tracked variable to a status file and compare against that stored value every time the build is run. If the value does not match a re-build of the affected components should be triggered.

The config tracking behavior consists of four components:

#### `variable_depends_on_phony`
> This is a meta target which is required to trick the build system into always checking the state of the tracked variables. `Phony` targets are always built, no matter what. Usually having a `phony` target as a dependency of a real target is a poor choice since the `phony` target is always 'out of date' since it doesn't actually exist. This means the real target is always re-built every time the build system runs.
>
> This behavior can be fixed with the use of an intermediate target which is a real file (the variable tracking targets). If the real file remains unchanged after its own recipe is run (and it will always run since it depends on a `phony`) then anything depending on it will not be rebuilt (assuming no other dependencies have been updated).

#### `depend_on_var`
> This is a define used for meta programming. It creates a set of targets, one for each of the variables listed in `$(watch_vars)`, of the form `$(STATUS_FLAGS_DIR)/$1_tracking_flag`. The `$1` is replaced by the variable name to be tracked. It also creates a variable `$(depend_$1)` which references this target.
>
> For example, the variable `CONFIG_FILE` will cause `$(depend_CONFIG_FILE)` and `$(STATUS_FLAGS_DIR)/CONFIG_FILE_tracking_flag` to be created.

#### `$(depend_$1)`
> Any target which wishes to depend on the value of a variable can add these as a dependency. For example, the scheduler step `$(STATUS_FLAGS_DIR)/build-rpms.flag:` relies on `$(depend_STOP_ON_PKG_FAIL)`. This variable actually maps to the associated status flag.

#### `$(STATUS_FLAGS_DIR)/$1_tracking_flag:`
> The actual logic to track the variables is present in this recipe. Every tracking flag depends on the phony target `variable_depends_on_phony`, so it will always be guaranteed to be updated. When the recipe runs it reads the current value of the tracking flag and compares it to the value of the variable. The tracking flag file is updated only if the current contents do not match the value of the variable
>
> Any target depending on this tracking flag will only update if the tracking flag file itself updates. So, assuming the variable is consistent between builds, the tracking flag will not be updated, and the depending target will not see a need to re-build.

### Folder Dependencies

`Make` does not work well with folders, it tracks the modification time of the folder itself but has no concept of the contents of the folder. When a file in the folder is modified the modification time of the folder does not change, only when a file is added/removed does it change. This is further obfuscated if the files are nested in sub-folders. Instead of tracking the actual folder, the entire contents of the folder must be tracked. This can be accomplished with a call to the `find` command: `folder_contents = $(shell find $(folder_name))`. This will create a space separated list of files and directories including the root directory which make can use as dependencies.

Unfortunately this still leaves a problem: How to write a recipe for the folder. Consider the naive approach of creating a target for the folder like:
```makefile
folder=/path/to/folder
$(folder): dependency1 dependency2
    mkdir -p $(folder)
    touch $(folder)/file1 && \
    touch $(folder)/file2 && \
    touch $(folder)/file3 && \
    exit -1  && \
    touch $(folder)/file4
```
Clearly the recipe will fail before creating `file4`, but the folder itself will have been created. The modification time of the folder will also be updated every time one of the files is touched. When the build is re-run `Make` will see the folder now exists, and is newer than anything depending on it, and will determine the folder recipe does not need to be re-run. There is no way to accurately detect partial failures in a rule that targets folders directly.

Instead a two part process is used. A target for the folder is used, but a meta target is used to actually operate on the contents of the folder.

#### `$(folder):`
> A very simple target and recipe is added for the actual folder:
> ```makefile
> folder=/path/to/folder
> $(folder): $(STATUS_FLAGS_DIR)/folder.flag
>   touch $@
> ```
> If this recipe is run it just updates the modification time of the folder. The target depends on a meta file, the `folder.flag` file.

#### `$(STATUS_FLAGS_DIR)/folder.flag:`
> This flag recipe contains all the actual logic used to update the contents of the associated folder:
> ```makefile
> $(STATUS_FLAGS_DIR)/folder.flag: dependency1 dependency2:
>   mkdir -p $(folder)
>   touch $(folder)/file1 && \
>   touch $(folder)/file2 && \
>   touch $(folder)/file3 && \
>   exit 1  && \
>   touch $(folder)/file4 && \
>   touch $@
> ```
> Note the final `touch $@` command which creates/updates the flag file. When the recipe fails, it will fail before updating the flag file. This means that during the next build the `$(folder):` target will see the flag is missing/out-of-date and re-run the flag recipe.
>
> Assuming the flag recipe succeeds, the folder recipe will then touch the folder, updating its timestamp. This leaves the timestamps in a good state: The folder is newer than the flag variables, and the flag variable is newer than any files in the folder which where created/updated.

### Go Tools Compiling

The various go tools found in `./tools/` (see [Go Tools](#go-tools)) are used to perform various steps in the package and image build process. They are split into two general groups, package build and image build. The tools are built from the `tools.mk` file.

##### `$(go_tool_list)`
This list tracks the available go tools. Any tool listed here should exist in a sub-folder of the same name in `./tools/`.
> For example, if `go_tool_list = tool1 tool2 ...`, then there should exists go programs in the folders `./tools/tool1/, ./tools/tool2/, ...` which will be compiled into executables `./out/tools/tool1, ./out/tools/tool2, ...`.

##### `$(go_tool_targets)`
`$(go_tool_targets)` is a list of all go tool executables.
> Continuing the above example, `go_tool_list = ./out/tools/tool1 ./out/tools/tool2 ...`

##### `go_util_rule`
For each entry in `$(go_tool_list)` the define `go_util_rule` is parsed and executed. It defines three things per go tool:
 - Variables to reference each tool: `$(go-tool1), $(go-tool2), ...`. These can be used to invoke the tool, or add it as a dependency.
 - `.PHONY` targets to manually build the tools `go-tool1, go-tool2, ...`
 - A set of dependencies for each tool: `$(go-tool1): $(shell find $(TOOLS_DIR)/$(notdir $(tool))/ -type f -name '*.go'), $(go-tool2): ...`

 Together these adds all the go files found in a given tools directory to its dependencies, and create a way to refer to the tools.
> For example:
> ```makefile
> go_tool1=./out/tools/tool1
> .PHONY: go-tool1
> go-tool1: ./out/tools/tool1
> ./out/tools/tool1: $(shell find $(TOOLS_DIR)/tool1/ -type f -name '*.go')
> ```

##### `$(TOOL_BINS_DIR)/%`
Assuming local tool rebuilding is enabled with `REBUILD_TOOLS=y` (by default the go executables are pre-built as part of the toolkit) this target will match any go executable of the form `./out/tools/tool1, ./out/tools/tool2, ...`.
```makefile
$(TOOL_BINS_DIR)/%: $(go_common_files)
    cd $(TOOLS_DIR)/$* && \
        go test -covermode=atomic -coverprofile=$(BUILD_DIR)/tools/$*.test_coverage ./... && \
        go build -o $(TOOL_BINS_DIR)
```
The meta programmed rules above add the tool specific dependencies while the variable `$(go_common_files)` tracks shared libraries and module files.

Each go tool will run a self test when it is built, if test files are available.

##### `$(go_common_files)`
This variable tracks all shared files which may be used by any go tool. Shared packages are found in `./tools/internal/` while the `./tools/go.mod` and `./tools/go.sum` files track external dependencies for the go tools. If any of these files change all the go tools will rebuild.

### Disabling shell commands during dry-run
The `shell_real_build_only` function is offered which will invoke `$(shell ...)` only if the makefile is actually being built. When tab competing, or doing other non-build operations (`-n|--dry-run`) make will still evaluate `$(shell ...)` commands. This can be very costly time-wise for things like `$(shell find $(some_dir)/ -type f)` which may contain large numbers of file. Instead invoking `$(call shell_real_build_only, find $(some_dir)/ -type f)` will only run the command for non-dry-run flows.

When Make is running with `--dry-run` or `-n` it will add the short-form flag `-n` to the automatic variable `$(MAKEFLAGS)`. If the `-n` flag is present the call to `shell_real_build_only` is a no-op, otherwise it pass the shell command through to `$(shell $1)`

## Distroless images

### RPM manifest file
Mariner distroless container images do not contain an RPM database. In order for Secure Composition Analysis tools to detect the contents of a Mariner distroless container image, the file `/var/lib/rpmmanifest/container-manifest-2` contains the output of the following command:

```bash
rpm --query --all --query-format "%{NAME}\t%{VERSION}-%{RELEASE}\t%{INSTALLTIME}\t%{BUILDTIME}\t%{VENDOR}\t%{EPOCH}\t%{SIZE}\t%{ARCH}\t%{EPOCHNUM}\t%{SOURCERPM}\n"
```

Note: The output of the above command also includes the `gpg-pubkey` which is not an RPM package. In order to filter it out, the output of the above command can be piped (i.e., `|`) to the following command:
```bash
grep -v gpg-pubkey
```

## Prev: [Image Generation](4_image_generation.md), Next: [Common Error Logs](6_logs.md)
