Common error logs
===
## Prev: [Misc](5_misc.md)
- [Unresolvable circular dependencies](#unresolvable-circular-dependencies)
    - [Example](#example)
    - [Explanation](#explanation)
    - [How to fix](#how-to-fix)
    - [More info about the `RUN` and `BUILD` nodes](#more-info-about-the-run-and-build-nodes)

## Unresolvable circular dependencies
### Example

```
ERRO[0011][grapher] Unfixable circular dependency found:	{bpftool-6.6.2.1-2.azl3-RUN<Meta>} --> {systemd-devel-255-2.azl3-BUILD<Build>} --> {systemd-devel-255-2.azl3-RUN<Meta>} --> {grub2-rpm-macros-2.06-13.azl3-BUILD<Build>} --> {grub2-rpm-macros-2.06-13.azl3-RUN<Meta>} --> {bpftool-6.6.2.1-2.azl3-BUILD<Build>} --> {bpftool-6.6.2.1-2.azl3-RUN<Meta>}	error: cycle can't be resolved with prebuilt/PMC RPMs. Unresolvable
```

After extraction of the interesting part:

```
Unfixable circular dependency found:
{bpftool-6.6.2.1-2.<dist_tag>-RUN<Meta>} --> {systemd-devel-255-2.<dist_tag>-BUILD<Build>} -->
{systemd-devel-255-2.<dist_tag>-RUN<Meta>} --> {grub2-rpm-macros-2.06-13.<dist_tag>-BUILD<Build>} -->
{grub2-rpm-macros-2.06-13.<dist_tag>-RUN<Meta>} --> {bpftool-6.6.2.1-2.<dist_tag>-BUILD<Build>}
```

### Explanation

This is a build-time dependency cycle. The toolkit doesn't allow circular **build-time** dependencies (circular **run-time** dependencies are allowed).

These errors may be better understood if read from the back:
- `{grub2-rpm-macros-2.06-13.<dist_tag>-RUN<Meta>} --> {bpftool-6.6.2.1-2.<dist_tag>-BUILD<Build>}`: `bpftool` (1) depends on `grub2-rpm-macros` (2) to build
- `{systemd-devel-255-2.<dist_tag>-RUN<Meta>} --> {grub2-rpm-macros-2.06-13.<dist_tag>-BUILD<Build>}`: `grub2-rpm-macros` (2) depends on `systemd-devel` (3) to build
- `{bpftool-6.6.2.1-2.<dist_tag>-RUN<Meta>} --> {systemd-devel-255-2.<dist_tag>-BUILD<Build>}`: `systemd-devel` (3) depends on `bpftool` (1) to build and that closes the cycle.

The logs print specific packages, not specs or SRPMs.

### How to fix

The fix is to remove the dependency of one of the packages on the other. Ideas:
- Double-check the declared build-time dependencies of the packages (`BuildRequires` in the spec files) are actually necessary to build the package.
- Split one of the packages into a bootstrap and regular version, where the bootstrap doesn't create circular dependencies. Then have the other packages from the cycle depend on the bootstrap version.
  This happens in case of some compilers, which in newer version depend on themselves. Another example is our `systemd` package, which has its `systemd-bootstrap` counterpart.

### More info about the `RUN` and `BUILD` nodes

These are nodes of the dependency graph created during the build. The `RUN` nodes represent a runnable package, while the `BUILD` nodes represent a package that needs to be built.

The dependencies are encoded by the edges:
- Run-time dependencies are the `-->` going from `RUN` nodes to other `RUN` nodes.
- Build-time dependencies are the `-->` going from `RUN` nodes to `BUILD` nodes.
- The `{XXX-BUILD<Build>} --> {XXX-RUN<Meta>}` edges represent the fact that in order to use package `XXX` at run-time, it needs to be built first.

Examples:
- `{XXX-RUN<Meta>} --> {YYY-RUN<Build>}`: `XXX` is a run-time dependencies of package `YYY`.
- `{XXX-RUN<Meta>} --> {YYY-BUILD<Build>}`: `XXX` is a build-time dependencies of package `YYY`.
- `{XXX-BUILD<Build>} --> {XXX-RUN<Meta>}`: `XXX` needs to be built before it can be used at run-time.

For more information about the build system, please check out [How the Build System Works](0_intro.md).

## Prev: [Misc](5_misc.md)
