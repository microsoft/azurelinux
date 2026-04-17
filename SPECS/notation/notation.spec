Summary:        Notary Project notation CLI with dm-verity layer signing support
Name:           notation
Version:        2.0.0~alpha.1.azl1
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/notaryproject/notation
# Source0 is a self-contained tarball produced from the Microsoft fork that
# also bundles the matching notation-core-go and notation-go forks under
# _deps/ together with a populated vendor/ directory.
#
# How to regenerate (from a checkout where /root/source/notation,
# /root/source/notation-core-go, and /root/source/notation-go all sit at
# the desired commits):
#
#   1. WORKDIR=/tmp/notation-rpm-build
#      VERSION=%{version}
#      SRCDIR=$WORKDIR/notation-${VERSION}
#      rm -rf $WORKDIR && mkdir -p $WORKDIR
#      git -C /root/source/notation archive HEAD --prefix=notation-${VERSION}/ | tar -x -C $WORKDIR
#      mkdir $SRCDIR/_deps
#      cp -a /root/source/notation-core-go $SRCDIR/_deps/
#      cp -a /root/source/notation-go $SRCDIR/_deps/
#   2. cd $SRCDIR
#      go mod edit \
#        -replace github.com/notaryproject/notation-core-go=./_deps/notation-core-go \
#        -replace github.com/notaryproject/notation-go=./_deps/notation-go
#      go mod tidy
#      GOFLAGS=-mod=mod go mod vendor
#   3. cd $WORKDIR
#      tar --sort=name --owner=0 --group=0 --numeric-owner \
#          -czf notation-${VERSION}.tar.gz notation-${VERSION}/
Source0:        %{name}-%{version}.tar.gz

# Go binaries don't generate useful per-file debuginfo for rpm's stripping;
# disable the debug subpackage to avoid empty debugfiles.list errors.
%global debug_package %{nil}

BuildRequires:  golang

# dm-verity subcommand shells out to mkfs.erofs and veritysetup at runtime
Requires:       erofs-utils
Requires:       cryptsetup

%description
notation is the Notary Project CLI for signing and verifying OCI artifacts.

This Azure Linux build adds a "dmverity" command group that splits the existing
"sign --dm-verity" workflow into two operations:

  notation dmverity prepare <ref> --output-dir <dir>
    Computes a dm-verity root hash for each layer of an OCI image and writes
    the hashes plus sidecar metadata to disk for an external signer (HSM, KMS,
    Azure ESRP, etc.) to sign in place.

  notation dmverity push <ref> --signatures-dir <dir>
    Reads the signed root hashes and pushes the OCI referrer manifest
    (artifactType application/vnd.cncf.notary.dmverity.v1) to the registry,
    matching the manifest produced by "sign --dm-verity".

The output is consumed by the containerd erofs-snapshotter for kernel-level
dm-verity verification.

%prep
%autosetup -p1

%build
go build -mod=vendor -ldflags="-s -w" -o bin/notation ./cmd/notation

%install
install -D -m0755 bin/notation %{buildroot}%{_bindir}/notation

%check
./bin/notation version

%files
%license LICENSE
%doc README.md
%{_bindir}/notation

%changelog
* Fri Apr 17 2026 Dallas Delaney <dadelan@microsoft.com> - 2.0.0~alpha.1.azl1-1
- Initial Azure Linux package of notation with dm-verity ESRP support
- Bundles Microsoft fork of notation, notation-core-go, and notation-go
- Adds "notation dmverity prepare" and "notation dmverity push" subcommands
  for use with external detached signers (e.g., Azure ESRP)
