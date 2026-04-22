# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Pass --without tests to skip building composer-cli-tests
%bcond_without tests
# Pass --without signed to skip gpg signed tar.gz (DO NOT DO THAT IN PRODUCTION)
%bcond_without signed

%global goipath         github.com/osbuild/weldr-client/v2

Name:      weldr-client
Version:   36.1
Release: 2%{?dist}
# Upstream license specification: Apache-2.0
License:   Apache-2.0
Summary:   Command line utility to control osbuild-composer

%gometa
Url:       %{gourl}
Source0:   https://github.com/osbuild/weldr-client/releases/download/v%{version}/%{name}-%{version}.tar.gz
%if %{with signed}
Source1:   https://github.com/osbuild/weldr-client/releases/download/v%{version}/%{name}-%{version}.tar.gz.asc
Source2:   https://keys.openpgp.org/vks/v1/by-fingerprint/117E8C168EFE3A7F#/gpg-117E8C168EFE3A7F.key
%endif

Obsoletes: composer-cli < 35.0
Provides: composer-cli = %{version}-%{release}

Requires: diffutils

BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
%if 0%{?fedora}
BuildRequires:  golang(github.com/BurntSushi/toml)
BuildRequires:  golang(github.com/spf13/cobra)
# Required for tests and %check
BuildRequires:  golang(github.com/stretchr/testify/assert)
BuildRequires:  golang(github.com/stretchr/testify/require)
%endif

BuildRequires: git-core
BuildRequires: make
BuildRequires: gnupg2


%description
Command line utility to control osbuild-composer

%prep
%if %{with signed}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%endif
%if 0%{?rhel}
%forgeautosetup -p1
%else
%goprep
%endif

%build
export LDFLAGS="-X %{goipath}/cmd/composer-cli/root.Version=%{version} "

%if 0%{?rhel}
GO_BUILD_PATH=$PWD/_build
install -m 0755 -vd $(dirname $GO_BUILD_PATH/src/%{goipath})
ln -fs $PWD $GO_BUILD_PATH/src/%{goipath}
cd $GO_BUILD_PATH/src/%{goipath}
install -m 0755 -vd _bin
export PATH=$PWD/_bin${PATH:+:$PATH}
export GOPATH=$GO_BUILD_PATH:%{gopath}
export GOFLAGS=-mod=vendor
%else
export GOPATH="%{gobuilddir}:${GOPATH:+${GOPATH}:}%{?gopath}"
export GO111MODULE=off
%endif
%gobuild -o composer-cli %{goipath}/cmd/composer-cli


## TODO
##make man

%if %{with tests} || 0%{?rhel}
export BUILDTAGS="integration"

# Build test binaries with `go test -c`, so that they can take advantage of
# golang's testing package. The RHEL golang rpm macros don't support building them
# directly. Thus, do it manually, taking care to also include a build id.
#
# On Fedora go modules have already been turned off, and the path set to the one into which
# the golang-* packages install source code.
export LDFLAGS="${LDFLAGS:-} -linkmode=external -compressdwarf=false -B 0x$(od -N 20 -An -tx1 -w100 /dev/urandom | tr -d ' ')"
go test -c -tags=integration -buildmode pie -compiler gc -ldflags="${LDFLAGS}" -o composer-cli-tests %{goipath}/weldr
%endif

%install
make DESTDIR=%{buildroot} install

%if %{with tests} || 0%{?rhel}
make DESTDIR=%{buildroot} install-tests
%endif

%check
%if 0%{?fedora}
export GOPATH="%{gobuilddir}:${GOPATH:+${GOPATH}:}%{?gopath}"
export GO111MODULE=off
%endif

# Run the unit tests
export LDFLAGS="-X %{goipath}/cmd/composer-cli/root.Version=%{version} "
make test


%files
%license LICENSE
%doc examples HACKING.md README.md
%{_bindir}/composer-cli
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/composer-cli
%{_mandir}/man1/composer-cli*

%if %{with tests} || 0%{?rhel}
%package tests
Summary:    Integration tests for composer-cli

Requires: createrepo_c

%description tests
Integration tests to be run on a pristine-dedicated system to test the
composer-cli package.

%files tests
%license LICENSE
%{_libexecdir}/tests/composer-cli/
%endif


%changelog
* Fri Oct 31 2025 Brian C. Lane <bcl@redhat.com> - 36.1-1
- New release: 36.1 (bcl)
- build(deps): bump actions/setup-go from 5 to 6 (49699333+dependabot[bot])
- build(deps): bump github.com/spf13/cobra from 1.9.1 to 1.10.1 (49699333+dependabot[bot])
- test: iot-qcow2-image does not support packages (bcl)
- test: qcow2 renamed to server-qcow2 (bcl)
- build(deps): bump github.com/stretchr/testify from 1.10.0 to 1.11.1 (49699333+dependabot[bot])
- build(deps): bump actions/checkout from 4 to 5 (49699333+dependabot[bot])
- tests: Use current host arch in info and list tests (bcl)
