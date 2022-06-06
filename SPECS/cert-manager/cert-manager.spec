Summary:        Automatically provision and manage TLS certificates in Kubernetes
Name:           cert-manager
Version:        1.5.3
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/jetstack/cert-manager
#Source0:       https://github.com/jetstack/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated external dependencies from this tarball, since network is disabled during build time.
#   1. wget https://github.com/jetstack/%{name}/archive/refs/tags/v%{version}.tar.gz -o %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. patch -p1 < Fix-dependency-checksum.patch
#   5. mkdir -p BAZEL_CACHE
#   6. bazel fetch --repository_cache=BAZEL_CACHE //...
#   7. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz BAZEL_CACHE
Source1:        %{name}-%{version}-vendor.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated GO dependencies from this tarball, since network is disabled during build time.
#   1. wget https://github.com/jetstack/%{name}/archive/refs/tags/v%{version}.tar.gz -o %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod download
#   5. cd $HOME
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-gocache.tar.gz go
Source2:        %{name}-%{version}-gocache.tar.gz
Patch0:         Fix-dependency-checksum.patch
Patch1:         Fix-os-WriteFile.patch
BuildRequires:  bazel
BuildRequires:  git
BuildRequires:  golang
BuildRequires:  patch

%description
cert-manager is a Kubernetes add-on to automate the management and issuance
of TLS certificates from various issuing sources.

%prep
%autosetup -p1
%setup -q -T -D -a 1

%build
export GO111MODULE=off
mkdir -p %{_topdir}/go
export GOPATH=%{_topdir}/go
pushd $GOPATH
tar -xvf %{SOURCE2} --strip-components=1 --no-same-owner
popd

export GO_REPOSITORY_USE_HOST_CACHE=1

git config --global user.email you@example.com
git config --global user.name "Your Name"
git init
git add .
GIT_AUTHOR_DATE=2000-01-01T01:01:01 GIT_COMMITTER_DATE=2000-01-01T01:01:01 \
git commit -m "Dummy commit just to satisfy bazel" &> /dev/null

for cmd in cmd/* ; do
  if [ "$cmd" != cmd/util ]; then
    bazel --batch build --repository_cache=BAZEL_CACHE //$cmd
  fi
done

%install
mkdir -p %{buildroot}%{_bindir}
%ifarch aarch64
install -D -m0755 bazel-out/aarch64-fastbuild-ST-4c64f0b3d5c7/bin/cmd/ctl/kubectl-cert_manager %{buildroot}%{_bindir}/
%else
install -D -m0755 bazel-out/k8-fastbuild-ST-4c64f0b3d5c7/bin/cmd/ctl/kubectl-cert_manager %{buildroot}%{_bindir}/
%endif
install -D -m0755 bazel-bin/cmd/webhook/webhook_/webhook %{buildroot}%{_bindir}/
install -D -m0755 bazel-bin/cmd/controller/controller_/controller %{buildroot}%{_bindir}/
install -D -m0755 bazel-bin/cmd/cainjector/cainjector_/cainjector %{buildroot}%{_bindir}/
install -D -m0755 bazel-bin/cmd/acmesolver/acmesolver_/acmesolver %{buildroot}%{_bindir}/

%files
%license LICENSE
%doc README.md
%{_bindir}/*

%changelog
* Fri Sep 10 2021 Henry Li <lihl@microsoft.com> - 1.5.3-1
- Original version for CBL-Mariner
- License Verified