# Building the Go Tools

## Overview

This document details how to work on the Go tools that are used in the build system.

## Setup

Make sure you have the right version of go by [installing the necessary prerequisites here](../prerequisites.md).

### Managing root ownership of Go directories

> Since the build tools are run with `sudo`, and the tooling invokes `go build`, there are cases where Go modules are downloaded and owned by the root user. The tools try to avoid this as much as possible; however, this may occasionally happen. You can run `sudo chown -R $USER:$USER $(go env GOPATH)` to set ownership back to the current user.

### VSCode plugins

The [VSCode Go Extension](https://marketplace.visualstudio.com/items?itemName=golang.Go) is highly recommended for working with the Go files. Enable all the features by pressing `F1`, then running `Go: Install/Update Tools`. **If this command fails, please check [Managing root ownership of Go directories](#managing-root-ownership-of-go-directories).**

With the extension installed, you will get automatic formatting, syntax highlighting, linting, step-through debugging, easy-to-run unit tests, code coverage, and more.

### Building the Tools

The toolkit will try to use pre-compiled binaries by default, but if you are in the core repo, you will have to recompile the Go tools. This behavior is controlled via `REBUILD_TOOLS=y`.

```bash
# Build all the Go tools
sudo make go-tools REBUILD_TOOLS=y

# Build a specific tool
sudo make go-depsearch REBUILD_TOOLS=y
```

The compiled binaries will be placed into [toolkit/out/tools/](../../../out/tools/).

See [Go Tools Compiling](../../how_it_works/5_misc.md#go-tools-compiling) for a detailed explanation of how the Go build targets are defined in `Make`.

### Working on the Tools

Refer to the [Image Config Coding Guide](../../coding_guide/imageconfig.md) for some tips on working with the Go unit tests.

There are several dedicated build targets to help with the Go tools. Two of the most useful are:

```bash
# Autoformat and tidy the module files
make go-tidy-all

# Generate a coverage report at ../toolkit/out/tools/test_coverage_report.html
sudo make go-test-coverage
```
