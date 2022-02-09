Adds the three packages for metal3 containers who components are written in
golang:

- metal3/ip-address-manager v0.0.4
- metal3/cluster-api-controller-metal3 v0.4.0
- metal3/baremetal-operator v0.4.0

Build steps are as close to the original Dockerfiles as possible. Two major
differences:

1. Instead of pinning the golang tools to a specific version, >= requirement is
used. v1.14 for BMO was specifically "not found" and there shouldn't be any harm
in using a higher backwards-compatible version.

2. BMO's Dockerfile uses an ldflag to set a variable storing the commit hash
being built. Since it's no longer trivial to obtain and is actually an unused
variable in the BMO code, it was left out of the spec file. (Dynamically setting
the Veresion variable was retained.)
