# `base` components

The .toml files in this directory tree define the set of *components* that
make up the `base` sub-project of the distro.

* Most components that are imported "as-is" are listed in [`components.toml`](components.toml).
* Imported components that require further customization or configuration, as well as those
  defined via locally stored `.spec` files are placed under their own directories.

This directory structure is expected to evolve over time; the .toml files use `includes`
keys to ensure that they're all loaded appropriately by `azldev`.
