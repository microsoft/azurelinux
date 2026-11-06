# DNF5 repository snapshot plugin

This component packages the public
[dnf5-plugin-repo-snapshot](https://github.com/microsoft/dnf5-plugin-repo-snapshot)
source from the versioned release selected in the spec. The local spec and component definition
retain only the Azure Linux build, dependency, and source-verification wiring.

See the [upstream README](https://github.com/microsoft/dnf5-plugin-repo-snapshot#readme)
for CLI options, usage, and behavior. The plugin requires Azure Linux's DNF5
post-setup hook and libdnf5 package-filetime feature dependencies.
